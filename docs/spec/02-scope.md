# 02 · Phạm vi & mốc — Hai tuần làm đủ, tuần 3 chỉ cải thiện

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Mốc | Ngày | Phải có |
| --- | --- | --- |
| MVP | Thứ Tư 30/9 | Chat nhiều bước (tín hiệu lặp → agent chủ động nhắn → bảo hành → đặt lịch có xác nhận, UC1 → UC3) · 1 sự kiện "linh kiện bị điều đi" → UC3 lập lại 2 phương án · chuyển người với handoff card · "Việc của tôi" cơ bản · demo panel (bơm sự kiện, tua thời gian) |
| Tuần 1 | 28/9 → 4/10 | MVP + engine chăm sóc chủ động (detector registry · arbitration · context builder · Agent chọn lọc · verifier) + đủ 6 quyết định (UC1 → UC3) · tách multi-agent + Executor · MCP · Pub/Sub + detector worker · RAG có phiên bản · memory · Terraform + CI · trace OTel · 40 kịch bản eval |
| Tuần 2 — đủ phạm vi | 5/10 → 11/10 | **Toàn bộ phạm vi build**: 6 use case: UC1 đầy đủ · UC2, UC3 demo-ready (tích hợp cùng engine) · UC4–UC6 spec + kịch bản khung (không build) · copilot + auto-wrap · 5 loại handoff · Contact Arbitration · bảo mật (policy, sàng lọc injection) · eval ~150 kịch bản + RAG eval + red-team · **baseline B0–B2** (§23) · eval gate · dashboard · pipeline dữ liệu (gán nhãn, tổng hợp, DVC) · cỡ mẫu + ngưỡng detector · tải + chaos · 5 người dùng thử + mystery shopping · **demo đầy đủ 11/10** |
| Tuần 3 — cải thiện | 12/10 → 18/10 | Chỉ cải thiện, không thêm phạm vi: **model triage PhoBERT + chuỗi MLOps** · data science nâng cao (dự báo contact, survival, uplift) · tối ưu chi phí / độ trễ · chuyển workflow nhiều ngày sang Temporal · GraphRAG · tinh chỉnh theo kết quả eval và người dùng thử |

**"Đủ phạm vi" nghĩa là:** mọi thành phần trong Phần B và C chạy được trên thế giới giả lập, có phép đo, có trong demo 11/10.**Chỉ ở mức thiết kế production** (không build trong cuộc thi): Dataflow, vLLM tự host, A2A với đơn vị thật, đa region, identity vault trong nước với dữ liệu thật, tích hợp DMS/ERP thật.**Luật cắt phạm vi:** 21:00 mỗi tối kiểm tra; việc không kịp đẩy sang mốc sau, không kéo dài ngày. Không bao giờ hy sinh: tín hiệu hệ thống → can thiệp chủ động → xác nhận → xác minh → chuyển người (cùng chat đa mục đích), và các hard gate (§22). Hai tuần cho 4 người là dày — §42 có thứ tự cắt khi trễ.
