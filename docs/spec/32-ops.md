# 32 · Vận hành & runbook — Khi có sự cố, ai làm gì trong 15 phút đầu

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Sự cố | Phát hiện | Xử lý ngay |
| --- | --- | --- |
| Nhà cung cấp LLM gián đoạn | Tỷ lệ lỗi model > 5% | Router chuyển model dự phòng; nếu vẫn lỗi: chat chuyển người, L0 + luồng an toàn + mẫu tin vẫn chạy |
| Agent gửi tin sai hàng loạt | Khiếu nại tăng / QA phát hiện | **Kill switch** theo loại hành động; dừng outreach; xác định khách bị ảnh hưởng từ audit; gửi đính chính |
| Ghi dữ liệu sai | Validator / đối soát | Hành động bù (trả slot, trả reservation) từ snapshot; báo khách |
| Nghi rò dữ liệu | Cảnh báo DLP / audit | Khoá service account liên quan; quy trình sự cố dữ liệu theo pháp chế |
| Làn sóng sự kiện (triệu hồi, cập nhật lỗi) | Hàng đợi tăng | Hàng đợi ưu tiên; giới hạn tốc độ gửi; báo tổng đài tăng ca |
