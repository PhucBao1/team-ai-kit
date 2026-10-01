# AGENTS.md — EV CX Agent (Vin Smart Future · repo P-073)

Luật chung cho MỌI AI coding agent của đội (Claude Code, Cursor, Codex, Copilot, Gemini CLI…).
File này KHÔNG nằm trong repo BTC: nó được `team-ai-kit/install.sh` gắn vào máy từng người và giấu khỏi git.
Thư mục con có `AGENTS.md` riêng → luật ở đó bổ sung / ưu tiên hơn file này.

**Tài liệu (đọc đúng mục cần, không đọc cả thư mục)** — nằm trong `team-ai-kit/` (cùng cấp với repo):
- Spec: `../team-ai-kit/docs/spec/README.md` · nghiệp vụ & use case: `../team-ai-kit/docs/proposal/README.md`
- Quy ước code: `../team-ai-kit/docs/conventions.md` · kế hoạch & task: `../team-ai-kit/plan/`
- Trong repo: hợp đồng `contracts/` · sơ đồ `docs/architecture/` · hướng dẫn BTC `docs/guide/` (chỉ đọc)

## 1. Dự án trong 3 câu
AI agent CSKH hậu mãi xe điện: hiểu ý định cả cuộc hội thoại, tra KB có trích dẫn, dùng tool có phân quyền,
chủ động phát hiện việc bị kẹt (proactive), chuyển nhân viên kèm tóm tắt. Ràng buộc gốc: KHÔNG bịa chính sách /
giá / trạng thái; hành động ảnh hưởng khách phải được khách XÁC NHẬN trước. Dữ liệu là GIẢ LẬP.

## 2. Lệnh chuẩn
| Việc | Lệnh |
|---|---|
| Cài | `pip install -r requirements.txt` (Python **3.11**) · `bash ../team-ai-kit/install.sh` |
| Chạy | `make db` (Postgres + Redis) · `make run` (API :8000, Swagger `/docs`) |
| Đúng như CI của BTC | `ruff check src/ tests/` · `pytest tests/ -v` |
| Coverage (≥ 60%) | `make test-cov` |
| Type | `make typecheck` |
| Kiểm của đội | `make -f ../team-ai-kit/kit.mk check` (contracts, sơ đồ, guardrails) |

## 3. Kiến trúc — ranh giới KHÔNG được phá
1. **Agent chỉ đề xuất, không ghi.** `src/agents/**` không import `src.tools` (adapter + tool GHI). Tool ĐỌC ở `src/agents/tools/` (`@tool`).
   Mọi thao tác ghi đi qua `src/executor/` (confirmation token + validator + idempotency key). Bước `confirm_and_execute` (chuẩn bị token → `interrupt()` → thực thi) là chỗ duy nhất gọi executor — skill `langgraph-human-in-the-loop`.
2. **`src/core/` là Python thuần, tất định**: không import LLM, HTTP, DB, không đọc env. Mọi hàm public có test trong `tests/test_core/`.
3. **Chính sách, giá, trạng thái, ngày giờ, số km chỉ lấy từ tool / KB**, kèm trích dẫn. Không hard-code vào prompt hay câu trả lời.
4. **Hợp đồng là nguồn sự thật:** `contracts/tools.yaml`, `contracts/api.yaml`, `contracts/events.yaml`. Đổi mục đã có = PR riêng + ADR.
5. **Một framework điều phối: LangGraph.** LLM lấy qua `src/services/llm.py::get_llm(kind)`; không hard-code tên model ngoài `src/config.py`.
6. **Giữ cấu trúc template BTC:** code trong `src/`, test trong `tests/test_<module>/`, frontend trong `frontend/`, eval trong `eval/`.

## 4. Cấm
- Sửa file của BTC: `docs/guide/`, `.github/`, `scripts/log_*.py`, `scripts/setup_hooks*`, `scripts/_pyrun*`, các file hook
  (`.claude/settings.json`, `.gemini/settings.json`, `.cursor/`, `.codex/`, `.agents/hooks.json`, `.agents/rules/`). Cần đổi → hỏi người.
- Sửa / xoá `.ai-log/`; tự chạy `scripts/log_*.py` (trừ log thủ công cho ChatGPT/web: `scripts/log_manual.py`); `git push --no-verify`.
- Commit file của team-ai-kit vào repo này (AGENTS.md, CLAUDE.md, skills…) — pre-commit sẽ chặn.
- Dữ liệu khách thật, PII, secret trong code / test / log. `APP_ENV` chỉ nhận `development | production | test`.
- Sửa `eval/golden/` hoặc kỳ vọng eval để test pass; tắt test; hạ ngưỡng; `# type: ignore` hàng loạt.
- Viết "được bảo hành" chắc chắn — chỉ "đủ điều kiện sơ bộ" kèm lý do từ `check_warranty`.
- Vòng lặp gọi LLM không có giới hạn (luôn có max vòng, timeout, ngân sách token).

## 5. Quy ước code (chấm điểm Code Quality)
- Python 3.11, async đầu-cuối; **type hints mọi hàm**; **docstring cho hàm public**; **hàm ≤ 30 dòng, ≤ 3 tham số** (gom vào model nếu hơn).
- Pydantic v2 ở mọi biên; lỗi có cấu trúc, không `except:` trần; log bằng `logging`/structlog, không `print`.
- Commit: `feat(core): …`, `fix(agents): …`, `docs: …`, `test: …`, `chore: …`. PR nhỏ, một mục đích, vào `develop`.
- Frontend: TypeScript strict, React + Vite + Tailwind, **dark mode + responsive + loading state** (tiêu chí UI/UX).

## 6. Cách làm việc
- MỌI task theo skill `start-task`, đọc card `../team-ai-kit/plan/tasks/<mã>.md`. Chỉ tick `[x]` khi `python3 ../team-ai-kit/plan/verify.py <mã>` ĐẠT; ghi 1 dòng `WORKLOG.md`.
- Skill theo việc: `bootstrap-module` · `add-mcp-tool` · `add-langgraph-node` · `langgraph-human-in-the-loop` · `add-eval-scenario` · `add-kb-document` ·
  `db-migration` · `property-based-testing` · `inject-fault` · `run-eval-compare` · `write-adr` · `write-task-card` · `review-pr` · `security-review` ·
  `debug-failure` · `update-architecture-diagram` · `update-deliverables` · `deploy-live` · frontend: `add-frontend-screen` · `web-accessibility` · `playwright-cli`.
- Skill gốc bên ngoài (có `NOTICE.md`) đã được vá cho dự án; luật trong file này luôn thắng nội dung của chúng.
- Không chắc nghiệp vụ (bảo hành, SOP, pháp lý, câu chữ gửi khách) → hỏi người. AI sai cùng lỗi 2 lần → ghi `../team-ai-kit/docs/agent-lessons.md`.

## 7. Sở hữu
A: `graph.py` + `state.py` (chỉ A sửa), node / prompt chính, `src/services/` · B: `src/sim/ detect/ kb/ ml/`, `src/agents/tools/`, subgraph `charging` / `post_repair`
· C: `frontend/`, node `offer` · D: `src/core/ executor/ tools/ api/ db/`, `src/main.py`, `contracts/`, `eval/` runner, deploy.
B, C viết phần agent dưới dạng module riêng, A nối vào graph. Từng file theo tuần: mục **File** của card; kiểm `python3 ../team-ai-kit/plan/check_conflicts.py`.

## 8. Definition of done (mọi PR)
- [ ] `ruff check src/ tests/` + `pytest tests/` xanh (đúng CI BTC); `make test-cov` không tụt; test mới cho hành vi mới
- [ ] `make -f ../team-ai-kit/kit.mk check` xanh; không PII / secret
- [ ] Đổi hợp đồng / kiến trúc → ADR + cập nhật `docs/architecture/`; đổi hành vi với khách → cập nhật kịch bản eval
- [ ] Ghi `WORKLOG.md` (ai · task · kết quả · giờ); tick task trong `plan/<tên>.md`
