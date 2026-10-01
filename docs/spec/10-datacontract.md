# 10 · Hợp đồng dữ liệu & chất lượng — Sự kiện sai định dạng có thể làm detector báo sai hàng loạt

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Lớp | Kiểm tra | Công cụ |
| --- | --- | --- |
| Biên (ingest) | Schema sự kiện, trường bắt buộc, kiểu, enum severity | Pub/Sub schema; Pydantic |
| Nghiệp vụ | VIN tồn tại; appointment thuộc đúng VIN; thời gian không ở tương lai xa; odometer không giảm | Validator tuỳ chỉnh |
| Thống kê (hằng ngày) | Tỷ lệ mỗi loại sự kiện so với trung bình; tỷ lệ dead-letter | BigQuery + cảnh báo; Great Expectations / Pandera cho bảng phân tích |
| Xử lý lỗi | Dead-letter topic, replay theo khoảng thời gian, không mất sự kiện | Pub/Sub retention + seek |
