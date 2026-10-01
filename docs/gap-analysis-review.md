# Soát lại gap analysis P-073 — bổ sung & sửa

Ngày 28/9/2026 · Đã đối chiếu trực tiếp với `P-073.zip` (110 file, 3 commit: Initial · Setup logs hooks · PRD docx của nhóm).

**Kết luận:** báo cáo của Claude Code **đúng về nội dung và đáng dùng** — mọi yêu cầu chính của BTC đều được bắt, phần lớn nguồn trích đúng
(một vài số dòng lệch nhẹ, vd. "đừng tái cấu trúc" ở `chapter-02.md:534` chứ không phải 516). Đồng ý với đề xuất X1–X6.
Nhưng có **4 trạng thái cần sửa** và **9 điểm bị sót**, trong đó 3 điểm sẽ làm hỏng PR đầu tiên nếu không xử lý.

---

## A. Sửa trạng thái trong ma trận

| # | Báo cáo ghi | Thực tế trong repo | Sửa thành |
|---|---|---|---|
| 11, 12 | JOURNAL / WORKLOG ❌ thiếu | `JOURNAL.md`, `WORKLOG.md` **đã có khung** ở gốc repo | ⚠️ có khung, chưa điền — việc là điền đều, không phải tạo |
| 5 | Architecture ⚠️ lệch vị trí | `docs/architecture_diagram.md` **đã có**, nhưng là sơ đồ mẫu chung (GPT-4o, ChromaDB) | ⚠️ phải **thay nội dung** — để nguyên thì giám khảo thấy sơ đồ template |
| 25 | Thiếu `/health` | `src/main.py` **đã có** `GET /health`; Dockerfile + compose healthcheck gọi nó | ✅ code có; chỉ cần thêm vào `contracts/api.yaml` |
| 17 | Chuyển luật ruff nhóm vào `ruff.toml` | Đã chạy thử: làm vậy thì **CI BTC đỏ ngay, 4 lỗi trên code mẫu** — `print()` ở `src/main.py:13,15` (T201), `raise HTTPException(...)` không `from e` ở `src/api/routes.py:19` (B904), `app_host = "0.0.0.0"` ở `src/config.py:19` (S104) | ⚠️ gộp luật **và sửa code mẫu trong cùng PR**: `print` → logger, thêm `from e`, bỏ qua S104 riêng cho `src/config.py` (bind 0.0.0.0 là cố ý trong container) |

## B. Điểm bị sót

### Sẽ làm hỏng PR đầu tiên
1. **`APP_ENV` sai giá trị.** `src/config.py` chỉ nhận `development | production | test`; `.env.example` của nhóm đặt `APP_ENV=dev` → app không khởi động được.
   → Dùng `APP_ENV=development`. Các biến mới của nhóm (`MODEL_CHAT`, `CONFIRM_TOKEN_SECRET`…) phải có **giá trị mặc định** trong `Settings`, vì CI BTC chỉ có `OPENAI_API_KEY=test-key`.
2. **Test phải nằm trong `tests/`.** CI BTC chỉ chạy `pytest tests/` và `ruff check src/ tests/`. Kit đặt test trong `core/tests/` → CI không chạy, **coverage tính ra ~0%** (tiêu chí Code Quality cần ≥ 60%).
   → Mọi test về `tests/test_<module>/`; sửa `make test-core` và skill `bootstrap-module` theo.
3. **`/api/v1/chat` đang là JSON có test.** `tests/test_api/test_routes.py` gọi `/api/v1/chat` (JSON, `ChatResponse`) và `/api/v1/status`. Báo cáo đề xuất sửa test mẫu — rủi ro hơn cần thiết.
   → **Giữ `/api/v1/chat` trả JSON** (test BTC xanh, Swagger dễ demo) và **thêm `/api/v1/chat/stream`** (SSE) cho giao diện. Cập nhật `contracts/api.yaml` + ADR.

### Ảnh hưởng thiết kế
4. **Vị trí tool.** Template đặt tool ở `src/agents/tools/` (`@tool`, LLM nhìn thấy). Báo cáo map `tools/ → src/tools/` — mất quy ước template và làm guardrail "agent không được gọi tool ghi" khó viết.
   → **Tool đọc** ở `src/agents/tools/` (đúng template) · **adapter hệ thống + tool ghi + MCP servers** ở `src/tools/` · **Executor** ở `src/executor/`.
   Guardrail mới: file trong `src/agents/**` **không được import `src.tools`**; chỉ node `confirm_and_execute` được gọi `src.executor.run`. Ranh giới nằm ngay ở cấu trúc thư mục.
5. **Trọng số chấm điểm.** `chapter-09.md` / `checklist.md`: 5 tiêu chí × 20% — Product · System Design · **UI/UX** · **DevOps** · Code Quality (mục tiêu top: 8+/mỗi tiêu chí), cộng phần "AI Usage" chấm qua log.
   Kế hoạch nhóm đang dồn sức vào agent (Product + System ≈ 40%). **UI/UX và DevOps chiếm 40%** mà mỗi thứ chỉ có 1 người.
   → Tuần 1: deploy `/health` lên Cloud Run **ngay 28/9** (tip "deploy sớm"), LangSmith + structured logging. Tuần 2: một người hỗ trợ C làm dark mode, loading state, thông báo lỗi thân thiện, responsive.
   Code Quality: type hints mọi hàm, docstring public, hàm ≤ 30 dòng (`code-style/python.md:26`), coverage ≥ 60%.
6. **Lộ trình chính thức 6 tuần.** `chapter-01.md:62-71` ghi lộ trình 6 tuần; kế hoạch nhóm 3 tuần (30/9 · 11/10 · 18/10). Báo cáo có hỏi ngày Demo Day nhưng chưa nêu hệ quả.
   → Giữ MVP 30/9 và đủ phạm vi 11/10. Nếu Demo Day xa hơn 18/10, tuần 3 giãn ra cho deliverables (video, pitch, eval report, user test), **không** mở thêm phạm vi.
7. **`/docs/` thuộc CODEOWNERS của BTC** (`/docs/ @AI20K-Build-Phase/book-maintainers`). Kit đặt spec, proposal, sơ đồ… đều trong `docs/`. Nếu `main` bật "require code owner review", mọi PR đụng `docs/` phải chờ BTC.
   → Hỏi BTC (câu 1). Phương án dự phòng: deliverable bắt buộc vẫn ở `docs/architecture_diagram.md`; tài liệu nhóm chuyển sang `design/` (`design/spec/`, `design/proposal/`, `design/architecture/`).
8. **Hook git của BTC.** `scripts/setup_hooks.sh` ghi `.git/hooks/pre-push` để đẩy log AI. Kit dùng `pre-commit` (hook pre-commit) → không đè nhau, **nhưng**:
   chạy `setup_hooks.sh` **trước**; không bao giờ cài pre-commit cho stage `pre-push`; bỏ dòng `git config core.hooksPath` trong `scripts/setup-agent-links.sh`.
9. **`.agents/rules/ai-log-hook.md` của BTC** dặn AI agent không tự gọi script log. Kit không mâu thuẫn, nhưng nên thêm 1 dòng vào `AGENTS.md` mục 4: "Không sửa `.ai-log/`, không chạy `scripts/log_*.py` thủ công (trừ ChatGPT/web qua `log_manual.py`)".

## C. Xung đột — cập nhật đề xuất

| | Báo cáo | Sau soát lại |
|---|---|---|
| X1 cấu trúc | A — đưa vào `src/` | **A**, sửa map tool như điểm 4; test về `tests/` (điểm 2); frontend ở `frontend/`; harness eval ở `eval/` (BTC đã có `eval/results/`) |
| X2 câu chuyện | A — giữ EV proactive, mở đầu bằng đề | **A**. PRD docx (20/9) và proposal cùng ràng buộc gốc → ghi rõ "PRD = đề chung, proposal = lời giải ở miền hậu mãi xe điện"; thêm tool `update_contact_info` để phủ đủ 4 workflow PRD |
| X3 Python | A — viết tương thích 3.11 | **A** |
| X4 gói | A — uv + `requirements.txt` sinh ra | **A**; lưu ý `uv.lock` trong kit resolve cho 3.12 → **resolve lại với 3.11** |
| X5 AI logs | A — bật LangSmith + giữ Langfuse | **A** |
| X6 cấu hình AI tool | gộp, giữ hook BTC | **Đồng ý** + điểm 8, 9 |
| **X7 mới** | — | `/api/v1/chat` JSON giữ nguyên + `/api/v1/chat/stream` SSE (điểm 3) |
| **X8 mới** | — | Vị trí tài liệu nhóm: `docs/` hay `design/` — chờ BTC (điểm 7) |

## D. Thứ tự PR gộp (thay mục 4 của báo cáo ở phần thứ tự)

1. **Mỗi người:** `bash scripts/setup_hooks.sh` + điền `AI_LOG_API_KEY` → gõ 1 prompt → thấy dòng mới trong `.ai-log/session.jsonl`. **Làm trước mọi việc khác** — log mất là mất hẳn.
2. **PR 1 `chore/bootstrap` (D):** gộp config (`.claude`, `.gemini`, `.env.example`, compose, Makefile, `ruff.toml` + sửa code mẫu, `requirements.txt` từ `uv export` với 3.11), `AGENTS.md` + skills đã sửa đường dẫn `src/`, guardrails/check_* theo cấu trúc mới, `/health` + `/api/v1` vào contracts. Điều kiện merge: `ruff check src/ tests/` và `pytest tests/` xanh đúng như `ci.yml`.
3. **PR 2 `docs/deliverables` (D):** thay `docs/architecture_diagram.md` bằng sơ đồ 01–04 · README từ `README_boilerplate.md` (bản đầu) · khung `eval/results/report.md` · ngày đầu tiên trong `WORKLOG.md`.
4. **Sau đó** mới tách nhánh làm M-03… theo `day1-plan.md`.

## E. Câu hỏi gửi BTC — giữ 7 câu của báo cáo, ưu tiên hỏi trước

1. `main` có bật "require code owner review" không? Đội được sửa `.github/`, `CODEOWNERS`, `ci.yml` và thêm tài liệu vào `docs/` không?
2. Ngày Demo Day và hạn từng deliverable (lộ trình sách ghi 6 tuần)?
3. Vị trí chuẩn của journal, worklog, pitch deck, architecture (README/checklist và chương 9 ghi khác nhau)?

