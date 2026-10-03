# D — Tech lead · Platform & Quality · tên: ______ · tải: NẶNG (~33 giờ/tuần · tổng ~98,5h)

Sở hữu: `src/core/ executor/ tools/ api/ db/`, `src/main.py`, `contracts/*.yaml`, `migrations/`, `docs/adr/`, `eval/` runner + `eval/load/` + `report.md`, `README.md` (từ tuần 2). Merge `develop → main` ở mỗi mốc. Review chéo với A.
Skill hay dùng: `start-task` · `add-mcp-tool` · `db-migration` · `deploy-live` · `run-eval-compare` · `update-deliverables` · `write-adr` · `review-pr`.
Mọi task có card chi tiết (bấm mã task); card tuần 2–3 là **bản nháp**. **Chỉ tick `[x]` khi `python3 ../team-ai-kit/plan/verify.py <mã>` báo ĐẠT** + PR đã merge + 1 dòng `WORKLOG.md`. Tối Chủ nhật mỗi người soát card tuần sau bằng skill `write-task-card` (sửa đường dẫn / lệnh kiểm cho khớp code thật), người cặp review.

## Tuần 1 · 28/9 → 4/10 · ~39h

### MVP (28–30/9)
- [ ] **[D1.01](tasks/D1.01.md)** · 0,5h · 28/9 — Hook log AI + `install.sh`. **Xong khi:** `.ai-log/` có dòng mới; `git status` sạch.
- [ ] **[D1.02](tasks/D1.02.md)** · 1h · 28/9 sáng — Squash-merge PR bootstrap (`git fetch bootstrap.bundle` → `git merge --squash`) vào `main`, tạo `develop`. **Xong khi:** CI BTC xanh trên GitHub.
- [ ] **[D1.03](tasks/D1.03.md)** · 1h · 28/9 sáng — Cùng A, B đóng băng `contracts/`. *(đường găng)*
- [ ] **[D1.04](tasks/D1.04.md)** · 2h · 28/9 — GCP project + billing + Secret Manager; deploy `/health` lên Cloud Run (skill `deploy-live`). **Xong khi:** Live URL trả `{"status":"ok"}` (deliverable #5 từ ngày 1).
- [ ] **[D1.05](tasks/D1.05.md)** · 2h · 28/9 — `src/core/warranty.py` + test (xe cá nhân 10 năm/200.000 km VF8/9 · 8 năm/160.000 km · xe dịch vụ 3 năm/100.000 km · lỡ bảo dưỡng). Trả `ELIGIBLE_PRELIM / NEEDS_WORKSHOP / EXPIRED / UNKNOWN` + lý do.
- [ ] **[D1.06](tasks/D1.06.md)** · 1,5h · 28/9 — `src/core/range.py` (xưởng đi tới được với pin hiện tại, hệ số an toàn 1,3) + property test.
- [ ] **[D1.07](tasks/D1.07.md)** · 1h · 28/9 — **Kiểm lại** endpoint mock đã có trong PR bootstrap (`src/api/mocks.py`, đánh dấu `MOCK — D1.11`) khớp `contracts/api.yaml`; chạy thử bằng Swagger cùng C. **Xong khi:** C gọi được mọi endpoint mock từ frontend.
- [ ] **[D1.08](tasks/D1.08.md)** · 3h · 29/9 — Tool ghi `book_appointment`, `reschedule` trong `src/tools/service.py` (idempotent, giải phóng slot cũ, ghi promise) trên thế giới của B. **Chờ:** B1.02 · **mock:** dict trong test. *(đường găng)*
- [ ] **[D1.09](tasks/D1.09.md)** · 4h · 29/9 — Confirmation token HMAC (hạn 10', gắn `params_hash`, `customer_id`) + `/api/v1/confirm` + validator 7 kiểm tra + `executor.run`. **Xong khi:** đổi 1 tham số → token vô hiệu (có test). *(đường găng)*
- [ ] **[D1.10](tasks/D1.10.md)** · 2h · 29/9 — `src/core/claim_check.py` (ngày, giờ, km, tiền, %, mã lịch, biển số không có trong bằng chứng → chặn) + test.
- [ ] **[D1.11](tasks/D1.11.md)** · 3h · 30/9 — Nối endpoint thật với agent (A) và sim (B): SSE `/chat/stream`, `/stream/{id}`, `/jobs`, `/handoffs` + accept, `/trace/{id}`.
- [ ] **[D1.12](tasks/D1.12.md)** · 1h · 30/9 — Sửa lỗi C1.15 báo; deploy MVP; `develop → main`. **Xong khi:** demo MVP chạy trên Live URL.

### 1–4/10
- [ ] **[D1.14](tasks/D1.14.md)** · 4h — Postgres thật: Alembic + `src/db/models.py` (journeys, appointments, reservations, promises, handoffs, audit_log) + LangGraph checkpoint Postgres; `docker compose up` chạy đủ backend + db + redis.
- [ ] **[D1.15](tasks/D1.15.md)** · 4h — Runner eval `eval/run.py` (YAML, kiểm "hard" bằng trạng thái thế giới, k lần, pass^k) + chạy 40 kịch bản (20 của B1.12, 10 của B, 10 của D).
- [ ] **[D1.16](tasks/D1.16.md)** · 2h — Saga + transactional outbox + `audit_log` append-only cho thao tác ghi nhiều bước.
- [ ] **[D1.17](tasks/D1.17.md)** · 2h — Structured logging (JSON, `trace_id` middleware, không log PII) — điểm DevOps.
- [ ] **[D1.18](tasks/D1.18.md)** · 2h — Coverage ≥ 60% (`make test-cov`) + `make typecheck` sạch; bổ sung test chỗ thiếu.
- [ ] **[D1.20](tasks/D1.20.md)** · 1,5h — ADR 001–003 trong `docs/adr/` (executor duy nhất ghi · pgvector · LangGraph) + bảng Design Decisions.
- [ ] **[D1.21](tasks/D1.21.md)** · 1,5h · 30/9 + CN 4/10 — `eval/results/report.md`: bản 0 (pytest + coverage) ngày 30/9; báo cáo 40 kịch bản + soát cổng 4/10. *(trả lại)*

## Tuần 2 · 5/10 → 11/10 · ~38,5h — đủ phạm vi

- [ ] **[D2.01](tasks/D2.01.md)** · 4h — Tool ghi `create_ticket`, `request_return`, `update_contact_info`, `trigger_remote_update` + nhánh executor + test. Bật `CONTRACT_STRICT` cho mốc MVP.
- [ ] **[D2.02](tasks/D2.02.md)** · 4h — MCP servers (FastMCP) bọc tool theo contracts; policy check theo vai trò (chủ xe / người lái).
- [ ] **[D2.05](tasks/D2.05.md)** · 5h — Suite `full` ≥ 150 kịch bản (A, B viết trong thư mục của mình) + chạy + báo cáo lỗi theo nhóm cho A.
- [ ] **[D2.06](tasks/D2.06.md)** · 4h — Baseline **B0** không AI · **B1** chatbot FAQ · **B2** single agent (cờ cấu hình) → bảng so sánh có khoảng tin cậy.
- [ ] **[D2.07](tasks/D2.07.md)** · 3h — Load test (Locust, 20 người đồng thời) + chaos (LLM timeout / lỗi → không ghi, báo đúng) + health check chi tiết. *(load test trả lại)*
- [ ] **[D2.08](tasks/D2.08.md)** · 3h — `eval/results/report.md` đủ 4 metric BTC (accuracy, latency < 3s, satisfaction, coverage) + baseline + feedback (từ B).
- [ ] **[D2.10](tasks/D2.10.md)** · 2h — ADR 004–007 (confirmation token · proactive arbitration · baseline · upsell có kiểm soát).
- [ ] **[D2.11](tasks/D2.11.md)** · 3h — Deploy bản đầy đủ + frontend (cùng C) + smoke 3 kịch bản demo trên URL thật; `develop → main` 11/10.
- [ ] **[D2.12](tasks/D2.12.md)** · 2h — Buffer sửa lỗi tích hợp trước demo 11/10.
- [ ] **[D2.13](tasks/D2.13.md)** · 3h — **Upsell**: `src/core/offers.py` (điều kiện + luật chặn) + tool ghi `create_quote` qua executor + sự kiện `offer_shown` / `offer_declined` trong contracts. **Chờ:** B2.12 · **mock:** offer viết tay.
- [ ] **[D2.14](tasks/D2.14.md)** · 2,5h — Route copilot/wrap (gọi hàm của A2.06) + CORS + deploy frontend; mọi sửa `src/api/`, `src/main.py`, `contracts/api.yaml` tuần 2 gom về D. *(từ C2.06 + phần route của A2.06)*
- [ ] **[D2.15](tasks/D2.15.md)** · 1,5h — `core.warranty`: pin thuê không thuộc bảo hành xe. **Chờ:** B2.18. *(mới 03/10)*
- [ ] **[D2.16](tasks/D2.16.md)** · 2h — Phiếu tiền chẩn đoán đính kèm lịch hẹn khi executor ghi. *(mới 03/10)*
- [ ] **[D2.09](tasks/D2.09.md)** · 3h — README đầy đủ (screenshot của C, bảng eval của D, API docs, Team, link video của C2.09). *(trả lại)*

## Tuần 3 · 12/10 → 18/10 · ~21h — chỉ cải thiện

- [ ] **[D3.02](tasks/D3.02.md)** · 5h — Chạy ablation bằng cờ của A3.04 → `ablation.md` + eval đầy đủ cuối (CI 95%) + gộp user test vòng 2 của B vào report.
- [ ] **[D3.04](tasks/D3.04.md)** · 4h — (Tuỳ chọn) workflow nhiều ngày sang Temporal — chỉ khi A3/D3 khác xong.
- [ ] **[D3.05](tasks/D3.05.md)** · 3h — Soát bảo mật: secret, PII trong log / trace, CORS, rate limit; `.env.example` đầy đủ.
- [ ] **[D3.06](tasks/D3.06.md)** · 3h — Chốt 10 deliverables theo checklist BTC (skill `update-deliverables`); README, architecture, report bản cuối.
- [ ] **[D3.08](tasks/D3.08.md)** · 3h — Luyện pitch ≥ 3 lần + trả lời câu hỏi kỹ thuật (System Design, DevOps).
- [ ] **[D3.09](tasks/D3.09.md)** · 3h — Soát README (sửa trực tiếp, nhúng video + GIF) · pitch / report: ghi lỗi vào `presentation/review-notes.md` cho C, D sửa. *(đổi: B → D: README thuộc D từ tuần 2)*
