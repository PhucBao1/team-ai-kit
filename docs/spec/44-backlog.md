# 44 · Backlog task — Nhận việc ngay — MVP chia theo ngày, tuần 1–2 theo epic

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

### MVP (28–30/9)

| ID | Task | Người | Giờ | Phụ thuộc | Ngày |
| --- | --- | --- | --- | --- | --- |
| M-01 | Repo, cấu trúc thư mục, Makefile (run, test, reset, deploy) | D | 1 | — | CN 27 |
| M-02 | GCP project, billing, bật API, service account dev | D | 1 | — | CN 27 |
| M-03 | Chốt chữ ký 8 tool MVP + schemas.py | A+B | 1,5 | — | 28 |
| M-04 | Schema DB (SQLModel) + migration | B | 2 | M-03 | 28 |
| M-05 | seed.py: anh Minh, 20 khách, 3 xưởng, 8 mã lỗi, 3 chính sách, slot | B | 3 | M-04 | 28 |
| M-06 | core/warranty + 3 test | D | 2 | M-04 | 28 |
| M-07 | core/range + test | D | 1,5 | M-04 | 28 |
| M-08 | Tool đọc: get_vehicle_status, explain_dtc, check_warranty, list_jobs | B | 3 | M-05, M-06 | 28 |
| M-09 | graph.py LangGraph + system prompt 7 luật + nối tool đọc | A | 4 | M-03 | 28 |
| M-10 | FastAPI /chat (SSE), /reset; Dockerfile; deploy Cloud Run | D | 3 | M-09 | 28 |
| M-11 | Khung trang demo 4 vùng + chat UI với mock SSE | C | 6 | API contract | 28 |
| M-12 | find_options (kho + range + kỹ năng + khoá slot) | B | 4 | M-07 | 29 |
| M-13 | book_appointment / reschedule idempotent + ghi promise + reservation | B | 3 | M-12 | 29 |
| M-14 | Confirmation token HMAC + /confirm + validator 7 check | D | 4 | M-13 | 29 |
| M-15 | claim_check trước khi gửi + test | D | 2 | M-10 | 29 |
| M-16 | Luồng agent: phương án → xác nhận → đặt lịch | A | 3 | M-12, M-14 | 29 |
| M-17 | detect/rules + /events/inject + đồng hồ giả lập /clock/advance | B | 3 | M-13 | 29 |
| M-18 | Agent xử lý candidate → tin chủ động 5 phần vào /stream | A | 3 | M-17 | 29 |
| M-19 | Nối chat với API thật; nút phương án / Xác nhận | C | 3 | M-14 | 29 |
| M-20 | Màn hình "Việc của tôi" từ /jobs | C | 3 | M-13 | 29 |
| M-21 | Demo panel: reset, bơm 2 sự kiện, tua +2 / +14 ngày | C | 2 | M-17 | 29 |
| M-22 | create_handoff + HandoffCard lắp từ dữ liệu có cấu trúc | A | 4 | M-16 | 30 |
| M-23 | /handoffs, accept, NV chốt phương án → agent nhận lại việc | D | 3 | M-22 | 30 |
| M-24 | Console nhân viên + trace panel thu gọn | C | 5 | M-23 | 30 |
| M-25 | Kịch bản demo cố định trong sim/scenarios + 2 xe phụ | B | 2 | M-17 | 30 |
| M-26 | Tinh chỉnh giọng văn, mẫu tin chủ động | A | 2 | M-18 | 30 |
| M-27 | 10 kịch bản tay + sửa lỗi | D | 3 | tất cả | 30 |
| M-28 | Quay video dự phòng (trước 15:00) + kịch bản nói 5 phút | D | 2 | M-27 | 30 |
| M-29 | README chạy lại từ đầu | B | 1 | — | 30 |

Tổng ~80 giờ cho 4 người × 3 ngày — vừa sức nếu không phát sinh. Việc đỏ (đường găng): M-03 → M-12 → M-13 → M-14 → M-16 → M-22.

### Tuần 1–3 theo epic

| Epic | Task chính | Người | Tuần |
| --- | --- | --- | --- |
| E1 · Đủ 6 quyết định (UC1 → UC3) | ① sửa từ xa (trigger_remote_update, SOP) · ③ KB theo phiên bản phần mềm · ④ bảng mã lỗi → linh kiện · subagent triage / scheduler / writer | A, B | 1 |
| E2 · MCP & tool đủ đề bài | 6 MCP server · create_ticket, request_return · policy check theo vai trò (chủ xe / người lái) | B, D | 1 |
| E3 · Sự kiện thật | Pub/Sub topic + schema + dead-letter · detector worker Cloud Run · Contact Arbitration cơ bản | B, D | 1 |
| E4 · Hạ tầng & quan sát | Terraform (Cloud Run, Cloud SQL, Pub/Sub, Secret Manager) · GitHub Actions · OTel GenAI → Cloud Trace + Langfuse · audit chuỗi hash | D | 1 |
| E5 · Thế giới giả lập đầy đủ | 200 xe / 5 xưởng / 60 linh kiện · tiêm lỗi có nhãn · KB chính sách công khai có phiên bản · luồng VED / ACN-Data | B | 1–2 |
| E6 · Eval | Runner YAML · 40 kịch bản (tuần 1) → 150 (tuần 2) · khách ảo · rubric + người hiệu chỉnh · eval gate trong CI | D | 1–2 |
| E7 · Memory & cá nhân hoá | Bảng sở thích có đồng ý · xem / xoá trong UI · "vì sao nhận tin này" | A, C | 1 |
| E8 · UC2 & copilot | find_chargers · handoff 24/7 theo mức khẩn · copilot gợi ý có nguồn · auto-wrap | A, C | 2 |
| E9 · Vòng 5 xác minh | Workflow xác minh 7–30 ngày bằng đồng hồ giả lập (tuần 2) · chuyển sang Temporal (tuần 3) · mở lại khi tái phát (UC6) | B, D | 2 · 3 |
| E11 · Model triage PhoBERT | Dataset triage_vi_v1 · baseline TF-IDF + LLM zero-shot · fine-tune 3 head · ONNX INT8 · cascade · MLflow registry · shadow | A, D | 3 |
| E12 · Data science | Tính cỡ mẫu nhóm đối chứng · ngưỡng detector theo chi phí · notebook dự báo contact + survival trên dữ liệu giả lập | B (+A) | 2 (A–B) · 3 (C–E) |
| E13 · AI data pipeline | Label Studio + hướng dẫn gán nhãn · sinh dữ liệu tổng hợp có lọc · DVC · embedding blue/green | B | 2 |
| E14 · Frontend engineering | SSE tự nối lại · cập nhật lạc quan an toàn · design system · accessibility AA · Vitest + visual regression | C | 1–2 |
| E15 · Engine chăm sóc chủ động | Detector registry + CandidateFriction · arbitration · context builder · decision gate (tất định / L1 / L2) · verifier · đo llm_call_rate | B, D (+A) | 1–2 |
| E16 · UC1 FULL | Rule UC1 + kịch bản đối chứng · InterventionProposal 8 câu hỏi **bản nhẹ** (điền tất định, LLM chỉ viết câu — lead 03/10) · tin chủ động "vì sao nhận" · journey proactive_friction · eval + hard gate | A, B, C, D | 1–2 |
| E17 · UC4–UC6 spec | Kịch bản YAML khung + tiêu chí chấp nhận (tài liệu tuần này; implement sau khi spec chốt) | B (+A) | 2 |
| E10 · Dashboard & bằng chứng | Dashboard metric · kiểm thử tải + chaos (LLM lỗi) · 5 người dùng thử · mystery shopping · bản demo cuối | C, cả nhóm | 2 |

### Use case × epic × người

Nhãn UC mới; card trong plan/tasks/ đã được đổi nhãn tương ứng (UC cũ → mới: proposal PL-A). Chi tiết phần việc từng người nằm cuối mỗi mục UC.

| UC | Mức tuần này | Epic / task chính | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| **UC1** Preemptive Service Friction | FULL | E15 · E16 · E1 (①–②) · M-17 · M-18 | Prompt suy luận, tin chủ động | Rule + arbitration + context builder, seed | Thông báo, "vì sao nhận", trace | Validator, verifier, eval |
| **UC2** Charging Friction | Tuần 3 nếu dư giờ (lead 03/10) | E8 · E15 · B2.14 | Suy luận 5 giả thuyết | CSMS giả lập, detector, find_chargers | Trạm thay thế, tin khẩn | Luồng 24/7, verifier phiên sạc |
| **UC3** Service Readiness | Demo-ready | E1 (③–⑤) · M-12 → M-16 · A1.11 | Scheduler đa ràng buộc | find_options, kho / kỹ năng / slot | Màn hình phương án, xác nhận | Validator 7 check, Executor + saga |
| **UC4** Billing Mismatch | Spec only | E17 | (tuỳ chọn) tổng hợp | Billing giả lập, R1–R3 | — | Ngưỡng tự sửa, duyệt mức 3 |
| **UC5** Claim Follow-up | Spec only | E17 | Trích lý do trả về | Claim state machine, SLA | — | Escalation, verifier |
| **UC6** Recurrence | Spec only | E17 · E9 · B2.15 | So case cũ / tín hiệu mới | verify_until, rule tái phát | — | Giới hạn 2 chu kỳ, verifier |
