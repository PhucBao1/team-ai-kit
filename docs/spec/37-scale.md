# 37 · Các bước scale — Năm giai đoạn — mỗi giai đoạn một nút thắt khác nhau

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Giai đoạn | Quy mô | Nút thắt chính | Thay đổi kiến trúc |
| --- | --- | --- | --- |
| **0 · Demo** | 1 khách mẫu, giả lập | Độ ổn định demo | 1 Cloud Run, SQLite/Cloud SQL, đồng hồ giả lập |
| **1 · Pilot 1 xưởng** | Vài trăm khách, 1 xưởng | Tích hợp hệ thống thật, niềm tin của NV | MCP adapter thật cho DMS / kho; **Làn 1 copilot**; shadow mode; identity vault trong nước |
| **2 · Vùng** | Vài nghìn khách, 5–10 xưởng | Chất lượng dữ liệu, xung đột lịch, tải hội thoại giờ cao điểm | Pub/Sub + outbox; Temporal; optimistic locking; autoscale Cloud Run; eval online; tự động hoá bật theo loại hành động |
| **3 · Toàn quốc** | Hàng trăm nghìn xe | Luồng sự kiện liên tục; làn sóng (triệu hồi); chi phí model; quota | Dataflow cho detector; partition bảng sự kiện theo ngày; read replica; hàng đợi ưu tiên + load leveling; quota model dự trữ / throughput cam kết; model open-weight tự host cho việc khối lượng lớn |
| **4 · Hệ sinh thái / đa thị trường** | Nhiều đơn vị, nhiều nước | Quản trị dữ liệu chéo pháp nhân, ngôn ngữ, quy định | A2A giữa đơn vị; Contact Arbitration chung; KB & SOP theo thị trường; triển khai đa region theo yêu cầu dữ liệu |

**Nguyên tắc scale:** không có trạng thái trong process (mọi trạng thái ở DB / Redis / Temporal) → nhân bản ngang tự do; khoá phân vùng theo VIN (Pub/Sub ordering key, partition) → sự kiện cùng xe xử lý tuần tự, khác xe song song; tách đường nóng (hội thoại) khỏi đường nền (detector, VoC, loop 4) để làn sóng nền không làm chậm khách đang chat.
