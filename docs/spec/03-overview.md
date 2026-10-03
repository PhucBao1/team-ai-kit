# 03 · Kiến trúc tổng thể — Sáu tầng, một bộ não, một điểm ghi duy nhất

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

**North star — Proactive AI Customer Care.** AI chủ động phát hiện, điều tra và xử lý những customer friction đang hình thành trước khi khách hàng phải chủ động yêu cầu hỗ trợ: quan sát tín hiệu đủ điều kiện, phát hiện bằng cơ chế rẻ trước (L0 tất định), chỉ gọi LLM khi cần suy luận đa nguồn / nhiều bước, hành động có kiểm soát (validator + Executor + xác nhận) và **xác minh** kết quả. **LLM là tầng leo thang, không phải tầng xử lý event.** Appointment không phải điểm bắt đầu — chỉ là một hành động xuôi dòng (UC3). Sáu use case, owner A/B/C/D và phạm vi Final MVP: proposal PL-A (usecases.md). Mọi kịch bản là giả lập (Synthetic / illustrative scenario for MVP).```text
TẦNG TƯƠNG TÁC      App chat · Zalo OA · Tổng đài (sau) · Console NV · "Việc của tôi" · Demo panel      → §19 §20 §21
        │ tin nhắn khách                                   ▲ tin trả lời / tin chủ động
        ▼                                                  │
TẦNG QUYẾT ĐỊNH     Input guard → Triage cascade (LLM nhỏ; PhoBERT ở tuần 3) → Coordinator        → §13 §15 §18
                     ├─ PolicyQA agent ── RAG có phiên bản + memory                          → §14 §16
                     ├─ Scheduler (UC3) ── lập phương án đa ràng buộc (đọc)                 → §14
                     ├─ Handoff builder ── card từ state có cấu trúc                        → §05-D
                     └─ Writer ⇄ Critic (claim_check + rubric)                             → §14 §17
        │ đề xuất (không bao giờ ghi trực tiếp)
        ▼
TẦNG THỰC THI       Executor tất định: confirmation token → validator 7 check → saga + outbox      → §17 §35
                     Lõi tất định: warranty · range · validator · claim_check · policy         → §17
        │ lời gọi có danh tính người dùng + idempotency key
        ▼
TẦNG TÍCH HỢP       MCP servers: vehicle · service · parts · warranty · charging · crm          → §11 §12
                     (MVP: hàm Python cùng chữ ký — thế giới giả lập)
        ▲ sự kiện                                          │
TẦNG DỮ LIỆU        Pub/Sub ← telematics · ERP · DMS · CSMS → detector L0 → Arbitration → proactive pipeline   → §09 §10
                     Journey State Graph · promises · audit (chuỗi hash) · KB có phiên bản · memory             → §08 §16
                     Workflow nhiều ngày: đồng hồ giả lập (tuần 1–2) → Temporal (tuần 3)                         → §04
TẦNG CHẤT LƯỢNG     Eval 5 tầng · RAG eval · agent eval · red-team · trace OTel GenAI · SLO · eval gate CI     → Phần C
(xuyên suốt)        LLMOps: release registry (prompt · SOP · KB · router) · MLOps: registry model triage (tuần 3)
```

| Tầng | Trách nhiệm | Không được làm |
| --- | --- | --- |
| Tương tác | Hiển thị, thu xác nhận của khách, realtime | Tự quyết định nghiệp vụ |
| Quyết định (LLM) | Hiểu, lập phương án, diễn đạt | **Ghi dữ liệu**; kết luận bảo hành; trả lời trạng thái từ tài liệu |
| Thực thi (tất định) | Kiểm tra, ghi an toàn, bù khi lỗi | Gọi LLM |
| Tích hợp | Nói chuyện với hệ thống gốc, phân quyền theo người dùng | Trả dữ liệu thừa |
| Dữ liệu | Sự thật về trạng thái, sự kiện, lời hứa, audit | Mất sự kiện; sửa lịch sử |
| Chất lượng | Đo, chặn release kém, theo dõi | Để thay đổi chưa qua eval lên production |
