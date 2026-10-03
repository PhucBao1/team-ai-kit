# A — Agent / AI lead · tên: ______ · tải: NẶNG (~35 giờ/tuần · tổng ~103,5h)

Sở hữu: `src/agents/` (graph, state, coordinator, critic, prompts — trừ `tools/` và các file B, C làm dưới đây), `src/services/llm.py`, `src/config.py` (tuần 3). Làm thêm phần data: reranker + `rag_golden` (A2.15), user test vòng 2 (A3.10), lỗi tiêm demo cuối (A3.11). Review chéo với D; review PR agent của B, C.
Skill hay dùng: `start-task` · `add-langgraph-node` · `add-eval-scenario` · `debug-failure` · `update-architecture-diagram`.
Mọi task có card chi tiết (bấm mã task); card tuần 2–3 là **bản nháp**. **Chỉ tick `[x]` khi `python3 ../team-ai-kit/plan/verify.py <mã>` báo ĐẠT** + PR đã merge + 1 dòng `WORKLOG.md`. Tối Chủ nhật mỗi người soát card tuần sau bằng skill `write-task-card` (sửa đường dẫn / lệnh kiểm cho khớp code thật), người cặp review. "Chờ" = cần phần của người khác; "mock" = cách làm tiếp không phải chờ.

## Tuần 1 · 28/9 → 4/10 · ~38,5h

### MVP (28–30/9)
- [ ] **[A1.01](tasks/A1.01.md)** · 0,5h · 28/9 — Cài hook log AI (`bash scripts/setup_hooks.sh`, điền `AI_LOG_API_KEY`) + `bash ../team-ai-kit/install.sh`. **Xong khi:** gõ 1 prompt → `.ai-log/session.jsonl` có dòng mới; `git status` sạch.
- [ ] **[A1.02](tasks/A1.02.md)** · 1,5h · 28/9 sáng — Cùng B, D **duyệt** `contracts/` + model trong `src/models/schemas.py` (đã có sẵn trong PR bootstrap: Option, HandoffCard, Promise, ChatEvent, Proposal, CriticVerdict) — chỉ sửa nếu thấy sai, rồi đóng băng. **Xong khi:** `tests/test_interfaces.py` xanh, cả 3 người approve. *(đường găng)*
- [ ] **[A1.03](tasks/A1.03.md)** · 1h · 28/9 — Bật LangSmith (3 biến env) + chọn provider/model trong `.env`; `get_llm("chat")` gọi được. **Xong khi:** 1 trace hiện trên LangSmith.
- [x] **[A1.04](tasks/A1.04.md)** · 4h · 28/9 — `graph.py`: state mới + system prompt 7 luật (`prompts/system_vi.md`) + nối 4 tool đọc. Giữ `agent`, `build_graph()`. **Chờ:** B1.04 · **mock:** stub tool trả dữ liệu mẫu. **Xong khi:** `/api/v1/chat` trả lời "xe tôi báo lỗi làm mát pin, có được bảo hành không" có trích dẫn; test mẫu BTC xanh.
- [x] **[A1.05](tasks/A1.05.md)** · 2h · 29/9 — Test `tests/test_agents/` với `mock_llm`: tool được gọi đúng, không bịa khi tool lỗi. **Xong khi:** `pytest tests/test_agents` xanh.
- [x] **[A1.06](tasks/A1.06.md)** · 3h · 29/9 — Luồng phương án → `proposal` → node `confirm_and_execute` (`interrupt()`) → `src.executor`. **Chờ:** B1.05, D1.09 · **mock:** executor giả. **Xong khi:** hội thoại đặt lịch chạy hết, không ghi khi chưa bấm Xác nhận. *(đường găng)*
- [x] **[A1.07](tasks/A1.07.md)** · 3h · 29/9 — Nhận candidate proactive → tin 5 phần (đã xảy ra · phương án · hạn · người phụ trách · vì sao nhận tin). **Chờ:** B1.06 · **mock:** candidate JSON. **Xong khi:** `/api/v1/events/inject` → tin xuất hiện ở `/api/v1/stream/{customer_id}`.
- [x] **[A1.08](tasks/A1.08.md)** · 4h · 30/9 — `handoff_builder`: HandoffCard lắp từ state + audit + promises; LLM chỉ viết `one_line_summary`, `sentiment`. **Xong khi:** "cho tôi gặp người" → card đủ trường trong `/api/v1/handoffs`. *(đường găng)*
- [ ] **[A1.09](tasks/A1.09.md)** · 2h · 30/9 — Tinh chỉnh giọng văn + chạy 10 câu demo; kịch bản nói 5 phút cho demo MVP (cùng C). **Xong khi:** 10/10 câu không bịa, không ghi khi chưa xác nhận.

### 1–4/10
- [x] **[A1.10](tasks/A1.10.md)** · 4h — Tách **Coordinator** + subgraph **PolicyQA** (RAG có trích dẫn, lọc phiên bản) dùng retriever của B. **Chờ:** B1.09 · **mock:** retriever trả 3 đoạn cố định.
- [x] **[A1.11](tasks/A1.11.md)** · 4h — Subgraph **Scheduler** (năng lực của UC3): 6 quyết định UC1 → UC3 (sửa từ xa trước · bảo hành sơ bộ · KB theo phiên bản phần mềm · linh kiện · quãng đường · xác minh sau sửa) gọi `src/core` của D.
- [x] **[A1.12](tasks/A1.12.md)** · 3h — **Writer ⇄ Critic**: `claim_check` (D1.10) + rubric, tối đa 2 vòng rồi handoff. **Xong khi:** câu có số không nguồn bị chặn trong test.
- [x] **[A1.13](tasks/A1.13.md)** · 2h — Node **triage** (rule → `get_llm("lite")`) + **safety path** (mã CRITICAL, "khói, mùi khét" → mẫu duyệt sẵn + handoff, không LLM).
- [x] **[A1.14](tasks/A1.14.md)** · 2h — Checkpoint Postgres theo `thread_id` (cùng D1.14) + chủ xe ≠ người lái (quyền theo xe).
- [ ] **[A1.17](tasks/A1.17.md)** · 1h — Chủ nhật: xem báo cáo 40 kịch bản của D, ghi 3 lỗi agent ưu tiên tuần 2 vào mục `### Lỗi ưu tiên từ eval tuần 1` (đầu tuần 2 của file này).
- [x] **[A1.16](tasks/A1.16.md)** · 1,5h — Cập nhật `docs/architecture/04-agent-flow.md` + khối Mermaid trong `docs/architecture_diagram.md` cho khớp graph thật (`kit.mk diagrams-export`). *(trả lại)*

## Tuần 2 · 5/10 → 11/10 · ~35h — đủ phạm vi

- [x] **[A2.01](tasks/A2.01.md)** · 4h — Đủ 4 workflow PRD trong hội thoại: tra việc/đơn (`list_jobs`), đặt/đổi lịch, **đổi/trả + ticket** (`request_return`, `create_ticket`), **cập nhật thông tin** (`update_contact_info`) — đều qua xác nhận. **Chờ:** D2.01.
- [x] **[A2.02](tasks/A2.02.md)** · 3h — Đổi mục đích giữa chừng không mất ngữ cảnh (goal stack): 5 kịch bản chuyển ý.
- [ ] **[A2.05](tasks/A2.05.md)** · 1,5h — UC2 đường Agent (sạc thất bại lặp lại, trạm khoẻ: giả thuyết + trạm thay thế + handoff khẩn); UC4–UC6 chỉ spec + prompt nháp (không build — dành giờ cho upsell).
- [x] **[A2.06](tasks/A2.06.md)** · 3,5h — **Copilot** cho nhân viên: hàm gợi ý bước tiếp theo có nguồn + auto-wrap ghi chú (route do D2.14 mở cho C2.01).
- [x] **[A2.07](tasks/A2.07.md)** · 2h — 5 loại handoff (khách yêu cầu · bực · thất bại 2 lần · an toàn · khiếu nại) + định tuyến ngoài giờ.
- [x] **[A2.08](tasks/A2.08.md)** · 3h — Router model theo việc + prompt caching phần tĩnh; đo token / độ trễ trên LangSmith (p95 < 3s cho câu đơn giản — tiêu chí BTC).
- [ ] **[A2.10](tasks/A2.10.md)** · 4h — Sửa theo eval 150 kịch bản (D2.05): 5 lỗi nặng nhất; không overfit prompt cho 1 kịch bản.
- [ ] **[A2.11](tasks/A2.11.md)** · 2h — Rubric LLM chấm + 20 mẫu người chấm để hiệu chỉnh (cùng D).
- [ ] **[A2.12](tasks/A2.12.md)** · 3h — Nội dung pitch: slide Problem · Solution · Architecture · Traction (số eval) — gửi C thiết kế.
- [ ] **[A2.13](tasks/A2.13.md)** · 2h — Kịch bản demo 11/10 (UC1 proactive → UC3, UC2 + 1 workflow PRD + handoff) + chạy thử 2 lần trên Live URL.
- [x] **[A2.15](tasks/A2.15.md)** · 3h — KB thêm FAQ + SOP (đổi/trả, đặt lịch, cập nhật thông tin — đúng 4 workflow PRD) + reranker; `rag_golden` 50 câu có đáp án + đoạn nguồn. *(đổi: B → A: chất lượng tìm kiếm quyết định PolicyQA)*
- [ ] **[A2.09](tasks/A2.09.md)** · 3h — Thêm 40 kịch bản (tổng hội thoại ~60): đa bước, đổi/trả, cập nhật thông tin, red-team. *(trả lại)*
- [ ] **[A2.17](tasks/A2.17.md)** · 1h — Nối subgraph `charging` (B2.14), `post_repair` (B2.15), node `offer` (C2.13) vào `graph.py` — chỉ A sửa `graph.py` / `state.py`. **Chờ:** B2.14, B2.15, C2.13.
- [ ] **[A2.18](tasks/A2.18.md)** · 3h — UC1 agent làm gọn: candidate UC1 (alias `T0_DTC_WARNING`), tin chủ động "lặp N lần trong X ngày" từ `get_recent_events`, `InterventionProposal` điền tất định. **Chờ:** B2.17. *(mới 03/10)*
- [ ] **[A2.19](tasks/A2.19.md)** · 1,5h — Nội dung phiếu tiền chẩn đoán khi khách xác nhận lịch (ký trong params cho D2.16). *(mới 03/10)*

## Tuần 3 · 12/10 → 18/10 · ~30h — chỉ cải thiện

- [ ] **[A3.02](tasks/A3.02.md)** · 3h — Cascade: PhoBERT chắc → dùng luôn, không chắc → LLM lite; đo độ trễ / chi phí trước-sau.
- [ ] **[A3.03](tasks/A3.03.md)** · 3h — ONNX INT8 cho triage; tích hợp sau cờ cấu hình (tắt được).
- [ ] **[A3.04](tasks/A3.04.md)** · 2h — Cờ ablation `ablate_critic / version_filter / memory` trong agent (D3.02 chạy đo + ghi báo cáo).
- [ ] **[A3.05](tasks/A3.05.md)** · 4h — Sửa theo feedback người dùng thử (B2.07) — ưu tiên hiểu nhầm ý định, câu trả lời dài.
- [ ] **[A3.06](tasks/A3.06.md)** · 3h — Kiểm an toàn cuối: 20 câu tấn công, PII trong log, câu chữ bảo hành.
- [ ] **[A3.07](tasks/A3.07.md)** · 3h — Lời thoại video + tập pitch ≥ 3 lần (cùng cả nhóm).
- [ ] **[A3.08](tasks/A3.08.md)** · 2h — Cập nhật sơ đồ Agent Flow + ADR cho thay đổi tuần 3.
- [ ] **[A3.09](tasks/A3.09.md)** · 3h — Tối ưu chi phí / độ trễ: cache, giới hạn tool call, đo trước-sau; ghi vào report. *(từ D3.03 — cờ và code nằm trong `src/agents`, `src/config.py` mà tuần 3 chỉ A sửa)*
- [ ] **[A3.10](tasks/A3.10.md)** · 4h — User test vòng 2 (sau khi sửa) → so điểm vòng 1 → `eval/usertest/summary_r2.md` (D3.02 đưa vào report). *(đổi: B → A: kiểm chính các sửa của A3.05)*
- [ ] **[A3.11](tasks/A3.11.md)** · 3h — Lỗi tiêm thêm cho demo cuối + kiểm lại toàn bộ kịch bản `src/sim/scenarios/`. *(đổi: B → A: lỗi tiêm cho demo agent)*
