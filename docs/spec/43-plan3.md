# 43 · Chi tiết 3 ngày MVP (28–30/9) — Ngày nào cũng kết thúc bằng một thứ chạy được

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

**Tối nay (CN 27/9, 1 giờ):** tạo repo + GCP project, bật billing và API (Gemini/Agent Platform, Cloud Run, Cloud SQL, Secret Manager), mỗi người chạy được "hello agent" gọi Gemini trên máy mình. Chốt ai là A/B/C/D.**Thứ Hai 28/9 — Xương sống***mục tiêu: chat gọi được tool thật trên dữ liệu seed*

###### A · Agent

- graph.py (LangGraph) + system prompt 7 luật
- Nối 4 tool đọc: vehicle, dtc, warranty, list_jobs
- Session + goal stack tối thiểu

###### B · Tools & sim

- **Sáng: chốt chữ ký tool** (§11)
- Schema DB + seed.py (anh Minh, 3 xưởng, 8 mã lỗi)
- tools/ đọc từ DB; make reset

###### C · Frontend

- Khung trang demo 4 vùng
- Chat UI + SSE với mock JSON
- Nút phương án / Xác nhận

###### D · Core & API

- core/warranty, core/range + unit test
- FastAPI: /chat (SSE), /reset
- Dockerfile, deploy thử Cloud Run
Xong khi: gõ "xe tôi báo lỗi làm mát pin, có được bảo hành không?" → agent trả lời đúng mức WARNING + ELIGIBLE_PRELIM, có nguồn, trên URL Cloud Run.**Thứ Ba 29/9 — Hành động & chủ động***mục tiêu: đặt lịch có xác nhận + sự kiện kích hoạt agent*

###### A · Agent

- Luồng find_options → xác nhận → book
- Nhận candidate từ detector, soạn tin chủ động 5 phần
- Gọi create_handoff khi khách muốn gặp người

###### B · Tools & sim

- find_options (tồn kho + range + slot khoá tạm)
- book / reschedule idempotent, ghi promise
- detect/rules + /events/inject + đồng hồ giả lập

###### C · Frontend

- Nối API thật cho chat
- Màn hình "Việc của tôi" (6 bước)
- Demo panel: reset, bơm sự kiện, tua giờ

###### D · Core & API

- validator + confirmation token (HMAC)
- claim_check chạy trước khi gửi tin
- /confirm, /jobs, /stream, audit_log
Xong khi: chạy trọn luồng đến "linh kiện bị điều đi" → khách nhận 2 phương án trong chat; không có cách nào ghi lịch mà không bấm Xác nhận.**Thứ Tư 30/9 — Chuyển người, hoàn thiện, tập demo***mục tiêu: demo 5 phút chạy 3 lần liên tiếp không lỗi*

###### A · Agent

- Handoff card lắp từ dữ liệu có cấu trúc
- Tinh chỉnh giọng văn tiếng Việt
- Agent nhận lại việc sau khi NV chốt

###### B · Tools & sim

- Kịch bản demo cố định trong sim/scenarios
- Sửa lỗi dữ liệu; thêm 2 xe mẫu cho câu hỏi phụ

###### C · Frontend

- Console nhân viên (card + Nhận + Chốt)
- Trace panel thu gọn
- Chỉnh giao diện cho màn chiếu

###### D · Core, QA, demo

- Chạy 10 kịch bản tay, ghi lỗi
- **Quay video demo dự phòng** trước 15:00
- Viết kịch bản nói 5 phút
Xong khi: demo §45 chạy 3 lần liên tiếp trên URL Cloud Run; có video dự phòng; README đủ để người ngoài chạy lại.
