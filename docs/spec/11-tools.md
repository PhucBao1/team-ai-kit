# 11 · Tools — Chữ ký tool — chốt sáng 28/9

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Mức 0 = chỉ đọc · mức 2 = ảnh hưởng khách, **bắt buộc** có confirmation_token do khách tạo ra khi bấm Xác nhận. Tool ghi không nhận token hợp lệ thì từ chối — kể cả khi LLM gọi nhầm.

| Tool | Mức | Input → Output | Mốc |
| --- | --- | --- | --- |
| `get_vehicle_status(vin)` | 0 | → model, odometer, soc, sw_version, dtc đang có, vị trí (nếu đồng ý) | MVP |
| `explain_dtc(code, sw_version)` | 0 | → severity, giải thích từ KB, remote_fixable, self_help, kb_ref | MVP |
| `check_warranty(vin)` | 0 | → gọi core.warranty: status, lý do, policy_version | MVP |
| `find_options(vin, reason, window)` | 0 | → 2–3 phương án đã qua core.range + tồn kho + kỹ năng; mỗi phương án được **khoá slot tạm 15 phút** | MVP |
| `book_appointment(option_id, confirmation_token)` | 2 | → appointment_id; giữ linh kiện; ghi promise; idempotent theo option_id | MVP |
| `reschedule(appointment_id, option_id, confirmation_token)` | 2 | → lịch mới; giải phóng slot cũ | MVP |
| `create_handoff(journey_id, card)` | 1 | → handoff_id, assignee, deadline | MVP |
| `list_jobs(customer_id)` | 0 | → journeys + promises cho màn hình "Việc của tôi" | MVP |
| `trigger_remote_update(vin, confirmation_token)` | 2 | → mô phỏng cập nhật phần mềm từ xa | Tuần 1 |
| `create_ticket(...)`, `request_return(...)` | 2 | Đủ 4 tool của đề bài (đổi/trả phụ kiện) | Tuần 1 |
| `find_chargers(lat, lng, soc)` | 0 | → trạm còn cổng trống (UC3) | Tuần 2 |
