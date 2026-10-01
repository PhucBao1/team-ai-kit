# 12 · MCP servers & A2A — Mỗi hệ thống gốc một MCP server, quyền theo người dùng thật

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| MCP server | Tool | Ghi? | Hệ thống gốc (production) |
| --- | --- | --- | --- |
| `vehicle-mcp` | get_vehicle_status · explain_dtc · trigger_remote_update | 1 tool | Nền tảng telematics / FOTA |
| `service-mcp` | find_options · book_appointment · reschedule · get_repair_order · list_jobs | 2 tool | DMS xưởng |
| `parts-mcp` | check_stock · reserve_part · release_part | 2 tool | ERP kho |
| `warranty-mcp` | check_warranty · get_claim · attach_evidence | 1 tool | Warranty portal |
| `charging-mcp` | find_chargers · get_session · flag_billing_issue | 1 tool | CSMS / billing sạc |
| `crm-mcp` | create_ticket · request_return · create_handoff · send_message | 4 tool | CRM · kênh gửi tin |

| Rủi ro (theo tinh thần OWASP MCP Top 10) | Biện pháp |
| --- | --- |
| Tool bị gọi vượt quyền | Mỗi lời gọi mang danh tính người dùng cuối (customer_id / staff_id) + vai trò; policy check ở gateway, không tin agent |
| Tool poisoning / mô tả tool bị sửa | Mô tả tool quản lý trong repo, review như code; server chỉ lấy từ registry nội bộ |
| Rò dữ liệu qua kết quả tool | Tool trả trường tối thiểu; che định danh trước khi vào context model bên ngoài |
| Ghi lặp / ghi nhầm | Idempotency key, confirmation token, validator |
| Lạm dụng tài nguyên | Rate limit theo khách, theo agent; circuit breaker khi hệ thống gốc lỗi |

**A2A (production):** agent của đơn vị khác (V-Green, Vinhomes) và trợ lý AI của khách giao tiếp qua A2A với agent card công bố năng lực; mọi hành động mức 2 vẫn cần xác nhận của chính chủ xe.
