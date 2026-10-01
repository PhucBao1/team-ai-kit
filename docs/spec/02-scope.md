# 02 · Phạm vi & mốc — Hai tuần làm đủ, tuần 3 chỉ cải thiện

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Mốc | Ngày | Phải có |
| --- | --- | --- |
| MVP | Thứ Tư 30/9 | Chat nhiều bước (cảnh báo → bảo hành → đặt lịch có xác nhận) · 1 sự kiện "linh kiện bị điều đi" → agent đưa 2 phương án · chuyển người với handoff card · "Việc của tôi" cơ bản · demo panel (bơm sự kiện, tua thời gian) |
| Tuần 1 | 28/9 → 4/10 | MVP + đủ 6 quyết định UC1 · tách multi-agent + Executor · MCP · Pub/Sub + detector worker · RAG có phiên bản · memory · Terraform + CI · trace OTel · 40 kịch bản eval |
| Tuần 2 — đủ phạm vi | 5/10 → 11/10 | **Toàn bộ phạm vi build**: 6 use case (UC1, UC3, UC5 đầy đủ; UC2, UC4, UC6 luồng rút gọn) · copilot + auto-wrap · 5 loại handoff · Contact Arbitration · bảo mật (policy, sàng lọc injection) · eval ~150 kịch bản + RAG eval + red-team · **baseline B0–B2** (§23) · eval gate · dashboard · pipeline dữ liệu (gán nhãn, tổng hợp, DVC) · cỡ mẫu + ngưỡng detector · tải + chaos · 5 người dùng thử + mystery shopping · **demo đầy đủ 11/10** |
| Tuần 3 — cải thiện | 12/10 → 18/10 | Chỉ cải thiện, không thêm phạm vi: **model triage PhoBERT + chuỗi MLOps** · data science nâng cao (dự báo contact, survival, uplift) · tối ưu chi phí / độ trễ · chuyển workflow nhiều ngày sang Temporal · GraphRAG · tinh chỉnh theo kết quả eval và người dùng thử |

**"Đủ phạm vi" nghĩa là:** mọi thành phần trong Phần B và C chạy được trên thế giới giả lập, có phép đo, có trong demo 11/10.**Chỉ ở mức thiết kế production** (không build trong cuộc thi): Dataflow, vLLM tự host, A2A với đơn vị thật, đa region, identity vault trong nước với dữ liệu thật, tích hợp DMS/ERP thật.**Luật cắt phạm vi:** 21:00 mỗi tối kiểm tra; việc không kịp đẩy sang mốc sau, không kéo dài ngày. Không bao giờ hy sinh: chat → xác nhận → sự kiện chủ động → chuyển người, và các hard gate (§22). Hai tuần cho 4 người là dày — §42 có thứ tự cắt khi trễ.
