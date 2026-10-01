# Gap analysis — repo mẫu BTC (AI20K template, P-073) ↔ context nhóm (ev-cx-agent-ai-kit)

Ngày: 28/9/2026 · Chế độ: chỉ đọc · Nguyên tắc: yêu cầu BTC thắng; lệch thì ghi để người quyết.
Repo BTC = `P-073/` (sinh từ template `AI20K-Build-Phase/starter-code-template`, + 1 commit của nhóm: `AI_Agent_CSKH_VSF_Brief_PRD_Wireframe.docx`).

> Lưu ý: tài liệu BTC tự mâu thuẫn ở vài chỗ (vị trí deliverable, cấu trúc thư mục, endpoint health). Nguồn ưu tiên khi lệch:
> code + README thật của repo > `docs/guide/deliverables/checklist.md` > các chương sách (`chapter-0x.md`, viết cho template cũ).

## Ma trận

| # | Yêu cầu BTC (nguồn) | Bắt buộc? | Nhóm đang có (nguồn) | Trạng thái | Việc cần làm | Ai / mốc |
|---|---|---|---|---|---|---|
| **Nộp bài** |
| 1 | Repo đội do hệ thống sinh trong org khoá; repo tự tạo ngoài org không được chấm (README.md:34-45, chapter-02.md:17) | Bắt buộc | Kit giả định "tạo repo, giải nén kit vào gốc" (day1-plan.md:7) | ⚠️ lệch | Làm việc trong repo P-073, KHÔNG tạo repo mới; sửa M-01 trong day1-plan | D / 28/9 |
| 2 | 10 deliverables Demo Day (README.md:135-148; checklist.md:7-57) | Bắt buộc | Kit chỉ lo code + docs kỹ thuật; không có mục nào map 10 deliverable | ❌ thiếu | Thêm bảng 10 deliverable → người phụ trách vào 44-backlog | D / 28/9 |
| 3 | #1 Source code trong `src/`, "follow template folder structure" (checklist.md:12-14; chapter-02.md:516 "đừng tái cấu trúc") | Bắt buộc (vị trí) / gợi ý (cấu trúc) | Monorepo top-level `agent/ core/ executor/ tools/ sim/ detect/ kb/ apps/api apps/web` (41-repo.md:5-35) | ⚠️ lệch | Quyết cấu trúc (xem Xung đột 1) | Cả nhóm / 28/9 sáng |
| 4 | #2 README theo `README_boilerplate.md` (Problem→Solution→Tech→Setup→Team, screenshot, env, API docs, Live URL) (README.md:140; chapter-09.md:84-95) | Bắt buộc | M-29 "README chạy lại từ đầu" (44-backlog.md:37); nội dung có ở proposal/ | ⚠️ lệch | Viết README theo đúng khung boilerplate, lấy nội dung từ proposal 01-04 | B / 30/9 bản đầu |
| 5 | #3 Architecture diagram tại `docs/architecture_diagram.md`, Mermaid (checklist.md:21-24); ch.9 lại nói PNG/SVG embed README (chapter-09.md:102) | Bắt buộc | 9 sơ đồ trong `docs/architecture/` (draw.io SVG + Mermaid) — tốt hơn yêu cầu | ⚠️ lệch (vị trí) | Viết `docs/architecture_diagram.md` nhúng 01-03 SVG + 04 Mermaid, link sang `docs/architecture/`; điền `ARCHITECTURE.md` gốc | D / 30/9 |
| 6 | #4 AI logs: LangSmith 3 biến env (README.md:142; .env.example:30-33; chapter-09.md:105-110, ≥5-10 trace) | Bắt buộc (deliverable) / LangSmith là gợi ý | Langfuse + OTel (33-stack.md:59; .env.example nhóm:20-23) | ⚠️ lệch | Chọn: bật LangSmith (0 code) song song Langfuse, hoặc hỏi BTC Langfuse có được chấp nhận | D / 29/9 |
| 7 | AI usage logging hook cho 6 tool, gửi grading server khi push; chạy `setup_hooks` 1 lần; không sửa `.ai-log/`, không `--no-verify` (README.md:161-179; chapter-02.md:556-620) | **Bắt buộc** (tính điểm "AI Usage") | Kit có `.claude/settings.json`, `.gemini/settings.json` riêng (không có hook log); guardrails cũng cấm `--no-verify` (guardrails.py:53) | ⚠️ lệch — **ghi đè sẽ mất log** | Gộp (merge) JSON, không chép đè; mỗi thành viên chạy `setup_hooks` + điền `AI_LOG_API_KEY` | Mọi người / 28/9 |
| 8 | #5 Live URL, sống tới Demo Day + 7 ngày, không sleep (chapter-09.md:56, 112-118); gợi ý Render/Vercel (README.md:143) | Bắt buộc (URL) / nền tảng là gợi ý | Cloud Run GCP (day1-plan.md:8, 23; 07-gcp.md) | ✅ khớp (nền tảng khác nhưng hợp lệ) | Đặt min-instances=1 hoặc ping; tính chi phí GCP tới Demo Day+7 | D / 28/9 deploy `/health` |
| 9 | #6 Video demo ≤5 phút, YouTube/Drive (checklist.md:34-37; presentation/README.md:21-26) | Bắt buộc | M-28 video dự phòng + kịch bản nói 5 phút (44-backlog.md:36; 45-demo.md) | ✅ khớp | Link video ghi vào README + `presentation/` | D / 30/9 bản thô, 11/10 bản cuối |
| 10 | #7 Pitch deck 10 slide: `presentation/pitch_deck.pptx` (checklist.md:39-42) **vs** `docs/pitch-deck.pdf` (chapter-09.md:130-132) | Bắt buộc | Không có | ❌ thiếu | Làm deck 10 slide theo chapter-09.md:410-462; nộp cả pptx + pdf cho chắc (hỏi BTC) | Cả nhóm / trước Demo Day |
| 11 | #8 `JOURNAL.md` hằng tuần (checklist.md:44-47) | Bắt buộc | `docs/agent-lessons.md` (chỉ lỗi AI) | ❌ thiếu | Điền JOURNAL.md mỗi tuần (lấy ADR + agent-lessons làm "bài học") | D / mỗi CN |
| 12 | #9 `WORKLOG.md` hằng ngày: ai làm gì (checklist.md:49-52) | Bắt buộc | Buổi 17:30 hằng ngày (day1-plan.md:24) nhưng không ghi file | ❌ thiếu | Thêm "cập nhật WORKLOG.md" vào buổi 17:30 | Mỗi người / hằng ngày từ 28/9 |
| 13 | #10 Eval evidence `eval/results/report.md`: accuracy >80%, latency <3s, satisfaction >4/5, coverage >60%, user feedback 3-5 người (eval/results/report.md:9-14; chapter-09.md:141-147) | Bắt buộc | Eval 5 tầng, harness YAML, baseline B0-B3, RAG eval, 5 người dùng thử (22..25-*.md, 02-scope.md:9) — vượt yêu cầu | ⚠️ lệch (định dạng) | Xuất kết quả eval của nhóm vào đúng template report.md; thêm `pytest-cov` để có số coverage | D / 11/10 |
| **Kỹ thuật** |
| 14 | Python 3.11 (README.md:26; ci.yml:19; Dockerfile:2; ruff.toml:1) | CI bắt buộc thực tế | Python 3.12, `requires-python >=3.12,<3.13` (pyproject.toml:5; .python-version) | ⚠️ lệch | Xung đột 3 | D / 28/9 |
| 15 | Quản lý gói bằng `requirements.txt` + pip; CI cài từ file này (ci.yml:22-23; chapter-02.md:487) | Bắt buộc thực tế (CI) | `uv` + `uv.lock`, "không ghim tay" (pyproject.toml:6) | ⚠️ lệch | Giữ uv cho dev nhưng `uv export --no-hashes > requirements.txt` và commit mỗi khi đổi dep (hoặc sửa CI dùng uv — hỏi BTC) | D / 28/9 |
| 16 | CI `ci.yml`: `ruff check src/ tests/` + `pytest tests/` (ci.yml:25-29) | Bắt buộc ("CI phải xanh", CONTRIBUTING.md:33; giữ nguyên CI, chapter-02.md:518) | `guardrails.yml` chạy `make lint/test/eval-smoke` bằng uv (guardrails.yml) | ⚠️ lệch | Giữ `ci.yml` BTC xanh; thêm `guardrails.yml` như workflow thứ hai; code ngoài `src/` sẽ không được lint/test bởi CI BTC | D / 28/9 |
| 17 | Ruff cấu hình ở `ruff.toml` (line 120, E F I N W UP) (ruff.toml) | Giữ nguyên (chapter-02.md:520) | `[tool.ruff]` trong pyproject (line 110, thêm B ASYNC S SIM RUF PT DTZ T20) | ⚠️ lệch — **`ruff.toml` thắng, luật nhóm bị bỏ qua lặng lẽ** | Chuyển luật nhóm vào `ruff.toml` (line 120, giữ N), bỏ `[tool.ruff]` khỏi pyproject | D / 28/9 |
| 18 | Makefile: `run test lint format typecheck check` (Makefile BTC) | Gợi ý (chapter-02.md:463-470) | Makefile khác hẳn: `setup dev test-core lint eval-* contracts diagrams…` | ⚠️ lệch | Gộp: giữ tên lệnh BTC, thêm lệnh nhóm; sửa đường dẫn | D / 28/9 |
| 19 | LLM: OpenAI `gpt-4o-mini` mặc định, đổi provider được qua `src/services/llm.py` (README.md:156; free-accounts.md:341-343) | Gợi ý (được đổi) | Gemini qua Vertex AI, 3 model qua env (33-stack.md:12; .env.example nhóm:7-12) | ✅ khớp (được phép) | Viết `get_llm()` trong `src/services/llm.py` đọc env; CI BTC chỉ có `OPENAI_API_KEY=test-key` → test không được gọi Vertex | A / 28/9 |
| 20 | Framework LangGraph + LangChain 0.3, FastAPI (README.md:150-159) | Template | LangGraph duy nhất, FastAPI + SSE (AGENTS.md:37; 33-stack.md) | ✅ khớp | — | — |
| 21 | Frontend Next.js hoặc Streamlit (README.md:157) — "không bắt buộc React" (chapter-03.md:72) | Gợi ý | React + Vite + Tailwind (AGENTS.md:53) | ✅ khớp | Đặt ở `frontend/` (hoặc `web/`) gốc repo | C / 28/9 |
| 22 | Docker multi-stage + compose chạy backend (Dockerfile; docker-compose.yml) | Điểm DevOps (chapter-09.md:190-196) | compose chỉ có db + redis (docker-compose.yml nhóm) | ⚠️ lệch | Gộp compose: `backend` (BTC) + `db` pgvector + `redis`; bỏ `version:` | D / 28/9 |
| 23 | Env vars theo `.env.example` BTC (OPENAI, DATABASE_URL, CHROMA, APP_*, LANGCHAIN_*, AI_LOG_*) | AI_LOG_* bắt buộc; còn lại mẫu | `.env.example` nhóm (DB_URL, REDIS, GOOGLE_*, MODEL_*, CONFIRM_TOKEN_*, LANGFUSE_*) | ⚠️ lệch | Gộp một file; giữ nguyên khối AI_LOG_* và LANGCHAIN_*; đổi `DB_URL` → `DATABASE_URL` cho khớp `src/config.py` | D / 28/9 |
| 24 | `.gitignore` bỏ qua `data/` (.gitignore:32) | Template | KB / seed / kịch bản có thể đặt dưới `data/` | ⚠️ rủi ro | Không đặt KB/seed/golden dưới `data/`; dùng `src/kb/`, `src/sim/`, `eval/` | B / khi tạo |
| **API & giao diện** |
| 25 | `GET /health` ở gốc, router prefix `/api/v1`, test mẫu gọi `/api/v1/chat` JSON + `/api/v1/status` (main.py:34-39; test_routes.py) | `/health` gần như bắt buộc (Dockerfile HEALTHCHECK, chapter-09.md:115) | `contracts/api.yaml` không có `/health`, không prefix; `/chat` trả SSE | ⚠️ lệch | Thêm `/health`; thêm `servers: [{url: /api/v1}]` vào api.yaml (đổi hợp đồng → ADR); cập nhật test mẫu | D / 28/9 |
| 26 | UX chấm: responsive, dark mode, accessibility, loading state (checklist.md:63; chapter-09.md:183-188) | Tiêu chí chấm | Responsive + AA, người lớn tuổi (21-fe.md); **không nhắc dark mode** | ❌ thiếu (dark mode) | Thêm dark mode vào 20-ui/21-fe + E14 | C / tuần 1 |
| **Dữ liệu & đề bài** |
| 27 | PRD nhóm đã commit vào repo BTC: CSKH đa bước cho "ứng dụng nhắn tin VSF" — tra đơn hàng, đặt lịch, đổi/trả, **cập nhật thông tin KH**; RAG + reranker; PostgreSQL; React; RAGAS/DeepEval; handover console 3 cột (AI_Agent_CSKH_VSF_Brief_PRD_Wireframe.docx §1.4, 2.3, 2.4.3, 3.3) | Là mô tả đề (không phải file BTC) | Kit chọn miền hậu mãi xe điện + proactive (proposal/01-brief.md:5-18); tool không có `update_customer_info` (contracts/tools.yaml) | ⚠️ lệch (phạm vi/miền) | Xung đột 2: thống nhất 1 câu chuyện; cân nhắc thêm tool cập nhật liên hệ | Cả nhóm / 28/9 sáng |
| 28 | Dữ liệu: BTC không cấp dataset, không quy định dữ liệu ngoài (không thấy trong repo) | — | Toàn bộ giả lập, cấm PII thật (AGENTS.md:16, 41) | ✅ khớp | Hỏi BTC nếu có dataset/đề chính thức | D |
| **Chất lượng code** |
| 29 | Type hints bắt buộc; hàm ≤30 dòng, ≤3 tham số; docstring public; không bare except; coverage ≥60% (code-style/python.md:9-26; chapter-09.md:198-204; chapter-08.md:64) | Tiêu chí chấm | Pydantic mọi biên, mypy strict core/executor, cấm print (conventions.md; pyproject.toml) | ✅ phần lớn / ⚠️ thiếu luật 30 dòng & coverage | Thêm 2 luật vào conventions.md; thêm `pytest-cov` | D / 29/9 |
| 30 | Commit Conventional Commits `feat: fix: docs:…` (CONTRIBUTING.md:26-27; chapter-09.md:392-396) | Gợi ý (CONTRIBUTING cho repo template) | `<phạm vi>: <việc>` (AGENTS.md:54) | ⚠️ lệch nhẹ | Dùng `feat(core): …` — khớp cả hai | Mọi người |
| 31 | Branch `develop` + ít nhất 1 commit tuần đầu (chapter-02.md:531) | Gợi ý | Tách nhánh từ `main` sau PR bootstrap (day1-plan.md:19) | ⚠️ lệch nhẹ | Tạo `develop`; PR vào `develop`, `develop`→`main` theo mốc | D / 28/9 |
| **Quản trị repo** |
| 32 | `.github/CODEOWNERS`: `*` và `/docs/`, `/.github/` thuộc `@AI20K-Build-Phase/book-maintainers` (CODEOWNERS:19-34) | Không rõ với repo đội | CODEOWNERS nhóm theo A/B/C/D | ⚠️ xung đột | Hỏi BTC trước khi thay (nếu main bật "require code owner review", mọi PR phải chờ BTC duyệt) | D / hỏi ngay |
| 33 | PR template `.github/PULL_REQUEST_TEMPLATE.md` | Template | `.github/pull_request_template.md` | ⚠️ trùng tên trên Windows (không phân biệt hoa thường → ghi đè) | Gộp nội dung vào 1 file `PULL_REQUEST_TEMPLATE.md` | D / khi gộp |
| **Nhóm có, BTC không đòi** |
| 34 | — | — | `AGENTS.md` + 6 AGENTS.md con + 13 skill + guardrails.py + pre-commit + gitleaks | ➕ | Giữ — bằng chứng dùng AI có kỷ luật (tiêu chí "AI Usage") | D |
| 35 | — | — | `contracts/` (tools, api, events) + check_contracts | ➕ | Giữ; sửa đường dẫn module | D |
| 36 | — | — | Spec 49 mục + proposal + ADR | ➕ | Giữ trong `docs/spec`, `docs/proposal`; tóm lại vào README/ARCHITECTURE.md | D |
| 37 | — | — | Proactive (sự kiện, detector, đồng hồ giả lập), executor + confirmation token, baseline B0-B3 | ➕ (rủi ro phạm vi) | Giữ làm điểm khác biệt nhưng không để lấn deliverable bắt buộc | A, B |

## 1. Xung đột phải quyết ngay

**X1 — Cấu trúc thư mục: `src/` của BTC hay monorepo top-level của nhóm**
- A. Đưa module nhóm vào `src/`: `agent/→src/agents/`, `tools/→src/tools/`, `core/→src/core/`, `executor/→src/executor/`, `apps/api/→src/api/` (+`src/main.py`), `sim/ detect/ kb/ → src/…`, `app_config.py → src/config.py`; test gom về `tests/test_<module>/`; web ở `frontend/`; import `from src.core… `. CI BTC chạy nguyên trạng.
- B. Giữ monorepo top-level, sửa `ci.yml` để lint/test cả thư mục mới. Kit ít phải sửa; nhưng lệch "follow template", đụng `.github/` (thuộc BTC theo CODEOWNERS) và giám khảo tìm code ở `src/`.
- Ảnh hưởng 3 tuần: A tốn ~2-3 giờ của D sáng 28/9 (sửa đường dẫn trong ~15 file kit), sau đó không phát sinh. B tiết kiệm lúc đầu nhưng mỗi lần CI BTC/ giám khảo chạy đều lệch.
- **Đề xuất: A.**

**X2 — Câu chuyện sản phẩm: PRD "CSKH app nhắn tin VSF" (đơn hàng/đổi trả/cập nhật thông tin) hay "hậu mãi xe điện chủ động"**
- A. Giữ EV proactive (mentor góp ý), nhưng README/pitch mở đầu bằng đúng đề (hội thoại đa bước, RAG + citation, tool-calling, handover) rồi mới "đi xa hơn"; map 4 workflow PRD sang tool nhóm (đơn = lệnh sửa chữa/đơn phụ kiện `list_jobs`, đặt lịch `book_appointment`, đổi/trả `request_return`, + thêm `update_contact_info`).
- B. Quay về PRD chung (không proactive) — bỏ phần lớn spec §04, §09, §17 proactive.
- Ảnh hưởng: B cắt được ~30% việc tuần 1-2 nhưng bỏ điểm khác biệt; A cần thống nhất PRD docx với proposal (docx nói PostgreSQL + reranker + RAGAS/DeepEval — đều có trong kit).
- **Đề xuất: A**, và cập nhật PRD docx (hoặc ghi rõ PRD là bản đề, proposal là bản giải).

**X3 — Python 3.11 (CI/Docker BTC) vs 3.12 (kit)**
- A. Viết code tương thích 3.11: `requires-python >=3.11`, ruff `target-version = "py311"`, mypy 3.11. Không đụng CI/Dockerfile BTC.
- B. Nâng CI + Dockerfile lên 3.12.
- **Đề xuất: A** (kit không dùng tính năng riêng của 3.12).

**X4 — Quản lý gói: pip `requirements.txt` vs `uv`**
- A. Dev dùng uv, `requirements.txt` sinh từ `uv export` và commit cùng `uv.lock`; `make lint` kiểm hai file khớp.
- B. Bỏ uv, dùng pip. C. Sửa CI BTC sang uv.
- **Đề xuất: A.**

**X5 — Tracing/AI logs: LangSmith vs Langfuse**
- A. Bật LangSmith cho deliverable #4 (chỉ 3 env var), Langfuse giữ cho eval online. B. Chỉ Langfuse + hỏi BTC.
- **Đề xuất: A** (rẻ, khỏi rủi ro chấm).

**X6 — File cấu hình AI tool (`.claude/settings.json`, `.gemini/settings.json`, `.agents/`)**
- Không có phương án B: phải **gộp**, giữ hook `UserPromptSubmit` / `BeforeAgent|AfterModel|SessionEnd` của BTC. Hook nhóm đổi `python3 …` → `bash scripts/_pyrun.sh …` (máy Windows không có `python3`).

## 2. Thiếu ảnh hưởng MVP 30/9 (theo đường găng M-03 → M-12 → M-13 → M-14 → M-16 → M-22)
1. **X1 + X3 + X4 chưa quyết → chặn M-01/bootstrap (10:00-12:00 28/9)** → chặn toàn bộ đường găng. Quyết trước 10:00.
2. `/health` + prefix `/api/v1` chưa có trong `contracts/api.yaml` → C làm mock sai URL (M-11, M-19). Chốt ở M-03.
3. Hook ghi log AI chưa cài trên máy từng người → mất log từ ngày đầu (không chặn MVP nhưng mất điểm không lấy lại được).
4. `requirements.txt` chưa có dep của nhóm (vertexai, sqlmodel, asyncpg, pgvector, sse-starlette…) → CI BTC đỏ ngay PR đầu.
5. `ruff.toml` che luật nhóm → guardrails "cấm print"/bảo mật không chạy; sửa trong PR bootstrap.
6. WORKLOG.md / JOURNAL.md chưa có người ghi — không chặn code nhưng là deliverable; gắn vào buổi 17:30.

## 3. Điểm cộng nhóm có mà BTC không đòi — cách trình bày
- **Luật + skill cho AI agent, guardrails chặn bằng code**: 1 slide "cách team dùng AI" + mục README "AI-assisted development" link `AGENTS.md`, `.agents/skills/`, `docs/agent-lessons.md`; khớp tiêu chí AI Usage mà BTC chấm qua log.
- **9 sơ đồ C4 draw.io + Mermaid** có CI kiểm: nhúng 01-03 vào `docs/architecture_diagram.md` và slide Architecture.
- **Eval 5 tầng + baseline B0-B3 + RAG eval**: đổ số vào `eval/results/report.md` đúng template, thêm bảng "so với chatbot FAQ" — ch.9 nói gần như không đội nào có.
- **Executor + confirmation token + claim_check**: trả lời câu hỏi giám khảo "làm sao giảm hallucination / hành động sai" (chapter-09.md:480).
- **Contracts + ADR**: README mục "Design decisions" link ADR (khớp bảng Design Decisions trong ARCHITECTURE.md).
- **Proactive (sự kiện → phương án)**: demo panel tua thời gian — điểm Product.

## 4. Kế hoạch gộp (giữ cấu trúc BTC — nếu X1 = A)
Tạo nhánh `chore/merge-ai-kit` từ `main` của P-073. Không đổi file BTC trừ khi ghi dưới đây.

**Chép nguyên (không trùng):** `AGENTS.md`, `CLAUDE.md`, `.agents/skills/` (thư mục `.agents/` đã có `hooks.json`, `rules/`, `workflows/` của BTC — chỉ thêm `skills/`), `contracts/`, `docs/spec/`, `docs/proposal/`, `docs/architecture/`, `docs/conventions.md`, `docs/agent-lessons.md`, `docs/day1-plan.md`, `docs/*.html`, `scripts/guardrails.py`, `scripts/ci/`, `scripts/diagrams/`, `scripts/docs/`, `scripts/hooks/after_edit.sh`, `scripts/setup-agent-links.sh`, `.pre-commit-config.yaml`, `.editorconfig`, `.prettierrc.json`, `.nvmrc`, `.mcp.json`, `.github/copilot-instructions.md`, `.github/workflows/guardrails.yml`, `pyproject.toml`, `uv.lock`.
AGENTS.md con: `agent/→src/agents/AGENTS.md`, `core/→src/core/`, `executor/→src/executor/`, `tools/→src/tools/`, `apps/web/→frontend/`, `eval/AGENTS.md` giữ.

**Gộp tay (trùng tên — KHÔNG chép đè):**
- `.claude/settings.json`: giữ `hooks.UserPromptSubmit` BTC + thêm `permissions`, `PreToolUse`, `PostToolUse` nhóm.
- `.gemini/settings.json`: giữ `hooks` BTC + thêm `"context": {"fileName": ["AGENTS.md"]}`.
- `.env.example`: khối BTC + khối nhóm; `DB_URL→DATABASE_URL`.
- `docker-compose.yml`: `backend` BTC + `db` + `redis`.
- `Makefile`: lệnh BTC (`run test lint format typecheck check clean`) + lệnh nhóm.
- `.gitignore`: nối `.gitignore.agent`.
- `ruff.toml`: thêm luật nhóm; xoá `[tool.ruff*]` khỏi pyproject.
- `.github/PULL_REQUEST_TEMPLATE.md`: nối nội dung template nhóm; không tạo file chữ thường.
- `.github/CODEOWNERS`: **chờ BTC trả lời**, tạm không sửa.
- `requirements.txt`: sinh từ `uv export`.

**Đường dẫn phải sửa (khi X1 = A):**
- `AGENTS.md` §3, §5, §7 (agent/ core/ executor/ apps/ → src/…; Python 3.11; lệnh make).
- `Makefile`: `core → src/core`, `executor → src/executor`, `apps/api/main.py → src/main.py`, `apps.api.main:app → src.main:app`, `apps/web → frontend`, `sim.seed → src.sim.seed`, `kb.ingest → src.kb.ingest`, `agent/graph.py → src/agents/graph.py`.
- `scripts/guardrails.py`: dòng 77 `core/`, 82 `agent/`, regex `from tools` → `from src.tools`, `_norm()` xử lý `\` trên Windows.
- `scripts/ci/check_contracts.py`: dòng 39 `ROOT/"tools"`, 66 `ROOT/"agent"`.
- `scripts/ci/check_diagrams.py`: dòng 42 `TRIGGERS`.
- `scripts/diagrams/export_langgraph.py`: dòng 16 `agent/graph.py`.
- `contracts/tools.yaml`: mọi `module: tools/*.py → src/tools/*.py`; `contracts/api.yaml`: thêm `servers` `/api/v1`, `/health`.
- `pyproject.toml`: `requires-python`, `[tool.pytest] testpaths = ["tests"]`, mypy override `src.core.*`, `src.executor.*`; per-file-ignores `sim/** → src/sim/**`.
- `.pre-commit-config.yaml`: `files: ^(core|executor)/ → ^src/(core|executor)/`, `mypy core executor → mypy src/core src/executor`.
- `.github/workflows/guardrails.yml`: `agent/graph.py → src/agents/graph.py`.
- `.claude/settings.json` (nhóm): `python3` → `bash scripts/_pyrun.sh`.
- `.mcp.json`: `tools.mcp_servers.sim_readonly → src.tools.mcp_servers.sim_readonly`.
- `.github/CODEOWNERS` (nếu được sửa), `docs/conventions.md` §1 (import `from src.core…`), `docs/spec/41-repo.md`, `docs/day1-plan.md` (M-01), templates trong `.agents/skills/bootstrap-module/`, `add-mcp-tool/`, `add-langgraph-node/`.

**Kiểm tra sau khi gộp:** `ruff check src/ tests/` + `pytest tests/` (đúng như ci.yml BTC) · `make lint` · `python scripts/ci/check_contracts.py` · `python scripts/ci/check_diagrams.py` · `python scripts/ci/validate_agent_files.py` · gõ 1 prompt trong Claude Code rồi xem `.ai-log/session.jsonl` có dòng mới.

## Câu hỏi gửi BTC
1. Repo đội có được sửa `.github/CODEOWNERS` (hiện `*` thuộc `@AI20K-Build-Phase/book-maintainers`) và `.github/workflows/ci.yml` không? `main` có bật "require code owner review" không?
2. Vị trí deliverable chuẩn: `JOURNAL.md`/`WORKLOG.md` ở gốc hay `docs/journal.md`/`docs/worklog.md`? Pitch deck `presentation/pitch_deck.pptx` hay `docs/pitch-deck.pdf`? Architecture ở `docs/architecture_diagram.md` hay `docs/architecture.md`? (README/checklist và chương 9 mâu thuẫn.)
3. AI logs (#4): Langfuse có được chấp nhận thay LangSmith không?
4. Được đổi cấu trúc ngoài `src/` (thêm `frontend/`, `eval/` harness) và đổi Python 3.12 / dùng `uv` trong CI không?
5. Ngày Demo Day và hạn nộp từng deliverable? Có rubric chi tiết cho phần "AI Usage" (log) không?
6. Đề bài chính thức có dataset / KB / mock API do BTC cấp không, hay đội tự giả lập? Miền "hậu mãi xe điện" có được coi là đúng đề "CSKH app nhắn tin VSF" không?
7. Có giới hạn chi phí / nhà cung cấp cloud (được dùng GCP Vertex AI + Cloud Run trả phí) không?
