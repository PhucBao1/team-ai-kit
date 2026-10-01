# 05 · Kiến trúc — Một bộ não, hai cửa vào

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Tin nhắn của khách và tín hiệu hệ thống cùng đi vào một Decision Engine: cùng goal stack, cùng tool, cùng guardrail. Bên trong, Decision Engine là một coordinator (LangGraph) điều phối vài sub-agent chuyên việc; agent chỉ đề xuất, còn mọi thao tác ghi đi qua một Executor tất định. Phần lớn tín hiệu dừng ở tầng rẻ, tất định; chỉ phần mơ hồ mới lên LLM.

```text
  CỬA 1 · KHÁCH (mọi kênh)                 CỬA 2 · TÍN HIỆU HỆ THỐNG
  App · Zalo · Tổng đài · Ảnh               Telematics · CSMS · DMS · ERP kho · Bảo hành
           │                                          │  (Pub/Sub, schema + dead-letter)
           ▼                                          ▼
  ┌──────────────────┐                    ┌──────────────────────┐
  │ Xác thực · PII   │                    │ L0 DETECTOR tất định │  ~0 token
  │ che trước LLM    │                    │ → ARBITRATION        │  gộp · chống spam
  └────────┬─────────┘                    └──────────┬───────────┘
           └───────────────┬─────────────────────────┘
                           ▼
       ┌───────────────────────────────────────────┐
       │ L1 TRIAGE CASCADE  rule → model nhỏ → LLM │  tuần 3: PhoBERT
       └─────────────────────┬─────────────────────┘
                             ▼
       ┌───────────────────────────────────────────┐
       │ CONTEXT BUILDER  journey state · memory   │  đọc song song
       └─────────────────────┬─────────────────────┘
                             ▼
       ┌───────────────────────────────────────────┐
       │ L2 COORDINATOR AGENT (LangGraph)          │
       │  ├ PolicyQA   RAG có phiên bản + trích dẫn│
       │  ├ Scheduler  6 quyết định UC1            │
       │  ├ Handoff    thẻ tóm tắt cho nhân viên   │
       │  └ Proactive  Writer ⇄ Critic (tối đa 2)  │
       │  chỉ ĐỀ XUẤT — không tự ghi hệ thống      │
       └─────────────────────┬─────────────────────┘
                             ▼
       CLAIM CHECK → KHÁCH XÁC NHẬN (token) → VALIDATOR 7 kiểm tra
                             ▼
       ┌───────────────────────────────────────────┐
       │ EXECUTOR tất định  — nơi DUY NHẤT được ghi│
       │ idempotency · saga · outbox → MCP tools   │
       └─────────────────────┬─────────────────────┘
                             ▼
       VERIFY bằng dữ liệu xe → LEARN (eval, người duyệt)   ·   L3: chuyển người
```

Chi tiết từng khối, luồng dữ liệu và bản đồ GCP ở file technical: §03 tổng quan, §05 luồng, §06 kiến trúc, §07 GCP, §13–15 agent/multi-agent/router.

L0

#### Rule / detector tất định

Ví dụ: ON part_reservation.cancelled → IF appointment.status = confirmed AND start − now < 72h THEN candidate. Cảnh báo an toàn mức nguy hiểm đi thẳng luồng mẫu tin đã duyệt, không qua LLM.

L1

#### Triage rẻ

Classifier nhỏ / điểm số: mức nghiêm trọng mã lỗi, mức khẩn (SoC thấp + đang ở trạm), chủ đề tin nhắn. Chỉ case vượt ngưỡng lên L2.

L2

#### Reasoning agent

Nhiều nguồn mâu thuẫn, lập phương án nhiều bước (xưởng nào, khi nào, linh kiện nào), hội thoại mơ hồ, trích lời hứa từ transcript.

L3

#### Con người

Hoàn tiền, ngoại lệ bảo hành, khách đang bực, lỗi an toàn, khiếu nại pháp lý. Tối ưu cho outcome, không phải tự chủ tối đa.

### Cửa vào của khách: đa kênh, đa phương thức

| Kênh | Cách hoạt động | Lưu ý nghiệp vụ |
| --- | --- | --- |
| **Chat** (app, Zalo OA, web) | Như §06 | Zalo là kênh quen thuộc nhất của khách Việt; app có sẵn xác thực |
| **Giọng nói — tổng đài** | Giọng nói → văn bản → cùng Decision Engine → văn bản → giọng nói; cho phép khách ngắt lời | Khách lớn tuổi vẫn gọi tổng đài. Lời nói có ấp úng, sửa lời (dùng PhoATIS_Disfluency để kiểm thử). Xác nhận mức 2 bằng cách đọc lại tham số và chờ "đồng ý" rõ ràng |
| **Trong xe** (trợ lý giọng nói trên xe, nếu có) | Cùng bộ não, giao diện rút gọn | **An toàn trước tiên:** khi xe đang chạy chỉ dùng giọng nói, câu ngắn; việc cần đọc nhiều hoặc xác nhận mức 2 hoãn đến khi xe dừng |
| **Ảnh / video** | Khách chụp đèn cảnh báo trên màn hình xe, gửi qua Zalo → model thị giác nhận diện → đối chiếu dữ liệu xe | Nếu ảnh và dữ liệu xe mâu thuẫn → tin dữ liệu xe, hỏi lại khách, hoặc đề nghị kiểm tra tại xưởng. Không chẩn đoán chỉ từ ảnh |
| **Copilot cho nhân viên** | Sau handoff, AI tiếp tục gợi ý cho CVDV / tổng đài viên: câu trả lời có nguồn, bước tiếp theo | Gợi ý cũng đi qua claim check; nhân viên là người gửi |

### Phạm vi IoT — rõ ràng từ đầu

**Có làm:** nhận cảnh báo đã được nền tảng telematics / CSMS chuẩn hoá ({vin, dtc, severity, odometer, time}, {charger_id, status}) và quyết định làm gì với khách và quy trình.**Không làm:** xử lý tín hiệu cảm biến thô hay dự đoán hỏng hóc bằng ML (predictive maintenance) — đó là bài toán của đội telematics. Vị trí xe chỉ dùng khi khách đã đồng ý.

### Model router

| Việc | Cách làm |
| --- | --- |
| Trạng thái lịch, kho, claim, trụ sạc, quyền ưu đãi | API / DB / rule tất định |
| Mức nghiêm trọng mã lỗi | Tra knowledge graph mã lỗi (tất định) |
| Phân loại chủ đề, tóm tắt ngắn, soạn tin từ mẫu | Model nhỏ |
| Hội thoại nhiều mục đích, lập phương án đổi lịch, trích lời hứa | Reasoning model — có chọn lọc |
| Kiểm tra câu trả lời trước khi gửi | Tất định: đối chiếu con số với kết quả tool/KB |

Vì sao cost-aware không phải chi tiết kỹ thuật: Gartner (1/2026) dự báo đến 2030, chi phí GenAI cho mỗi lần giải quyết có thể vượt **$3** — cao hơn nhiều nhân viên offshore — do chi phí hạ tầng, nhà cung cấp chuyển sang có lãi và use case phức tạp hơn. Kiến trúc để phần lớn tín hiệu không bao giờ chạm LLM là điều kiện để agent còn có lãi.
