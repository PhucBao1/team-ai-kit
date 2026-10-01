# 19 · API contract — Frontend làm với mock ngay từ sáng 28/9

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Endpoint | Mô tả | Trả về |
| --- | --- | --- |
| `POST /chat` | {customer_id, text} — stream SSE | sự kiện message · options (kèm confirmation_token) · handoff · done |
| `POST /confirm` | {token} — khách bấm Xác nhận | kết quả tool ghi + tin xác nhận |
| `GET /stream/{customer_id}` | SSE cho tin chủ động đẩy vào chat | như /chat |
| `GET /jobs/{customer_id}` | Màn hình "Việc của tôi" | journeys[] với bước hiện tại, lời hứa, người phụ trách, thay đổi gần nhất |
| `GET /handoffs` · `POST /handoffs/{id}/accept` | Console nhân viên | HandoffCard + hạn gọi lại |
| `POST /events/inject` | Demo panel: bơm sự kiện theo kịch bản | candidate + trace_id |
| `POST /clock/advance` | {hours} — tua đồng hồ giả lập | thời gian mới; chạy các việc đến hạn |
| `POST /reset` | Đưa thế giới về seed | ok |
| `GET /trace/{trace_id}` | Xem từng bước agent (cho demo và debug) | danh sách bước: tool, input, output, token, ms |
