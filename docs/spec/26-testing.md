# 26 · Chiến lược kiểm thử — Bảy tầng kiểm thử, từ hàm thuần đến sự cố LLM

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Tầng | Kiểm gì | Công cụ | Khi nào |
| --- | --- | --- | --- |
| Unit | core/ (bảo hành, quãng đường, validator, claim check) | pytest, hypothesis | Mỗi commit |
| Contract | Chữ ký tool / MCP, schema sự kiện, API frontend | pytest + schema | Mỗi PR |
| Integration | API + DB + tools + Pub/Sub emulator | docker compose, emulator | Mỗi PR |
| Agent eval | Kịch bản YAML, khách ảo, hard/soft | eval/ runner | PR đụng agent/core/kb; hằng đêm đầy đủ |
| E2E | Luồng demo trên trình duyệt | Playwright | Trước deploy staging / prod |
| Tải | Hội thoại đồng thời, làn sóng sự kiện (triệu hồi) | Locust | Tuần 2, trước production |
| Chaos | Model lỗi / chậm, MCP lỗi, DB chậm → hệ thống suy giảm có kiểm soát | Fault injection | Tuần 2 |
