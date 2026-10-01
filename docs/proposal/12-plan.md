# 12 · Stall audit & kế hoạch — 3 tuần: MVP 30/9, đủ phạm vi 11/10, cải thiện đến 18/10

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Khi có dữ liệu thật, bước 0 là **stall audit**: chạy detector L0 hồi tố trên 3–6 tháng dữ liệu (không tốn LLM) để đếm lịch hẹn lệch kho, claim bị trả về, comeback — ra chi phí lỗi ngầm mỗi tháng trước khi xây. Trong cuộc thi, thế giới giả lập đóng vai trò này. Nguyên tắc chia việc: **2 tuần đầu phải phủ toàn bộ nội dung của bài** (mọi yêu cầu đề + UC1 đủ 6 quyết định + proactive + đánh giá); **tuần 3 chỉ làm phần cải thiện**, bỏ đi thì demo vẫn đủ.

28–30/9

#### MVP

- KB chính sách công khai (bảo hành, bảo dưỡng, sạc, triệu hồi) có phiên bản
- Thế giới giả lập tối thiểu (xe, chủ xe, xưởng, kho, trạm sạc) + lỗi T1 có nhãn
- Chat: tra đơn/lịch, xác nhận trước khi ghi, handoff card
- UC1 lát mỏng: detector → đề xuất → khách xác nhận → đổi lịch

→ Demo MVP 30/9Tuần 1 · 28/9–4/10

#### Nền & lõi

- Phỏng vấn 5–10 chủ xe + 1–2 CVDV; intent taxonomy từ phỏng vấn, diễn đàn VinFast, CSConDa, NHTSA → 10 câu chuyện thật
- Knowledge graph mã lỗi (giả định); telematics từ VED, phiên sạc từ ACN; bộ tiêm lỗi T1–T5 có nhãn
- Tách coordinator + sub-agent + Executor; goal stack, tool gateway
- MCP tools, Pub/Sub + detector, arbitration
- RAG hybrid + rerank, lọc theo phiên bản phần mềm
- Validator 7 kiểm tra, claim check, xác nhận 4 mức, memory
- Terraform + CI, trace OTel

→ Lõi hội thoại đạt đủ yêu cầu đềTuần 2 · 5–11/10

#### Đủ phạm vi

- UC1 đủ 6 quyết định + UC3, UC5 verify
- Writer ⇄ Critic, "Việc của tôi", màn hình nhân viên, copilot
- Eval 5 tầng: RAG, agent (pass^k), E2E ~300 hội thoại + lỗi tiêm chạy k lần, red-team; hồi quy tự động khi KB/SOP đổi
- Đo 9 metric + ACRC; báo cáo cho vòng chấm
- Data science nền: ngưỡng detector theo chi phí, cỡ mẫu pilot
- Kiểm thử trải nghiệm với 5 người dùng: chat, "Việc của tôi", màn hình nhân viên — đo CES, ghi chỗ bối rối

→ Demo đầy đủ 11/10, có số đoTuần 3 · 12–18/10

#### Cải thiện (tuỳ chọn)

- PhoBERT triage + MLOps: MLflow, shadow → canary, drift
- Data science nâng cao: CUPED, dự báo sóng liên hệ, survival, uplift
- Tối ưu chi phí/độ trễ: cache, ONNX, cascade
- Temporal cho việc kéo dài nhiều ngày; GraphRAG

→ Số đo trước/sau cải thiện

Phân công 4 người, backlog, đường găng và tiêu chí hoàn thành từng tuần: file technical §42 (kế hoạch 3 tuần), §44 (backlog), §48 (definition of done).

**Lộ trình hai làn (theo cách big enterprise làm):**  
**Làn 0 — Nền dữ liệu:** hợp nhất trạng thái lịch, kho, lệnh sửa chữa, claim, dữ liệu xe thành Journey State Graph. Verizon mất nhiều năm cho bước này; ở Việt Nam, dữ liệu phân mảnh là rào cản số một. Trong cuộc thi, thế giới giả lập đóng vai trò này.  
**Làn 1 — Copilot trước:** CVDV và tổng đài viên dùng handoff card, gợi ý bước tiếp theo, auto-wrap (như EricaAssist của Bank of America). Rủi ro thấp, xây niềm tin, thu dữ liệu nhãn.  
**Làn 2 — Tự động có điều kiện:** chỉ bật cho từng loại hành động khi precision đạt ngưỡng *và* CSAT không giảm so với nhóm đối chứng.

### Tech stack

Xem §05.1: năm vòng lặp, harness, stack theo lớp cho MVP và production. MVP dùng: LangGraph + Gemini, MCP (FastMCP), Postgres + pgvector, Pub/Sub, Cloud Run, Langfuse + OpenTelemetry GenAI, harness eval kiểu τ-bench, React. Bảng đầy đủ mọi công nghệ và việc mỗi cái giải quyết: file technical §33.

### Rủi ro

|  |  |
| --- | --- |
| Chính sách công khai thay đổi | KB phiên bản, ghi ngày truy cập |
| Giả lập không giống thực tế | Neo vào VED/ACN/NHTSA; ghi rõ giới hạn |
| Hội thoại tiếng Việt thiếu tự nhiên | Người review; biến thể không dấu |
| Phạm vi phình to | 2 tuần đầu chỉ UC1 (6 quyết định) + UC3 + lõi hội thoại; ML/tối ưu để tuần 3; use case còn lại ở phụ lục |
