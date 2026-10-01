# 41 · Cấu trúc repo — Một monorepo, ranh giới rõ để 4 người không giẫm chân

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

```text
ev-cx-agent/
├─ apps/
│  ├─ api/                    # FastAPI: /chat /events /jobs /handoff /clock
│  │  ├─ main.py
│  │  └─ routes/
│  └─ web/                    # React: chat · việc của tôi · console NV · demo panel
├─ agent/                     # [Người A] LangGraph graph, node, prompt, schema output
│  ├─ graph.py
│  ├─ subagents/              # triage · scheduler · writer (tuần 1)
│  ├─ prompts/                # system prompt, SOP dạng skill (markdown)
│  └─ schemas.py              # Pydantic: Decision, Options, HandoffCard, Promise
├─ tools/                     # [Người B] hàm tool; tuần 1 bọc thành MCP
│  ├─ vehicle.py  service.py  parts.py  warranty.py  charging.py  notify.py
│  └─ mcp_servers/            # tuần 1
├─ contracts/                 # tools.yaml · agents.yaml — hợp đồng, đổi phải có ADR
├─ executor/                  # [Người D] nơi DUY NHẤT được ghi: token · validator · saga · outbox
├─ core/                      # [Người B/D] logic tất định — KHÔNG import LLM
│  ├─ warranty.py  range.py  validator.py  claim_check.py  policy.py
│  └─ tests/                  # pytest, chạy < 5 giây
├─ detect/                    # detector L0: rule trên sự kiện
├─ sim/                       # [Người B] seed dữ liệu, bơm sự kiện, đồng hồ giả lập
│  ├─ seed.py  scenarios/  clock.py
├─ kb/                        # chính sách công khai (có URL, ngày truy cập, ngày hiệu lực)
├─ eval/                      # [Người D] kịch bản YAML, khách ảo, chấm điểm (tuần 2)
├─ infra/                     # Dockerfile, terraform/ (tuần 1)
├─ docs/                      # spec/ (markdown) · architecture/ (9 sơ đồ: draw.io + Mermaid) · adr/ · conventions.md
├─ AGENTS.md · CLAUDE.md      # luật cho AI coding agent (mọi tool) — thư mục con có AGENTS.md riêng
├─ .agents/skills/            # 13 skill dùng chung (chuẩn SKILL.md) — symlink sang .claude/ .github/
└─ scripts/guardrails.py      # luật tất định dùng chung cho hook, pre-commit, CI
```

| Người | Sở hữu | Giao tiếp với người khác qua |
| --- | --- | --- |
| **A · Agent** | agent/, prompt, luồng hội thoại, handoff card | Chữ ký hàm trong tools/ và schema trong agent/schemas.py |
| **B · Tools & thế giới giả lập** | tools/, sim/, detect/, DB schema | Chữ ký hàm tool (chốt sáng 28/9, không đổi tuỳ tiện) |
| **C · Frontend** | apps/web/ | API contract §19 — dùng mock JSON trước khi backend xong |
| **D · Core, API, hạ tầng, eval** | core/, apps/api/, infra/, eval/, kịch bản demo | Unit test của core là hợp đồng với A và B |

### Luật & skill cho AI coding agent của team

4 người dùng AI coding agent khác nhau (Claude Code, Cursor, Codex, Copilot…) nên luật phải nằm trong repo, theo chuẩn chung, và được **chặn bằng code** chứ không chỉ dặn. Bộ khởi tạo: ev-cx-agent-ai-kit.zip.

| Lớp | File | AI đọc / chạy khi nào | Nội dung |
| --- | --- | --- | --- |
| **Rules** | AGENTS.md gốc (≤ 150 dòng) + 6 file thư mục con; CLAUDE.md import lại | Mọi phiên | Lệnh chuẩn, ranh giới kiến trúc (agent chỉ đề xuất, core thuần, hợp đồng có ADR, một framework LangGraph), điều cấm, definition of done |
| **Skills** | .agents/skills/ (13): start-task · bootstrap-module · add-mcp-tool · add-langgraph-node · add-eval-scenario · add-kb-document · db-migration · inject-fault · run-eval-compare · write-adr · review-pr · debug-failure · update-architecture-diagram | Khi task khớp mô tả | Quy trình từng bước + template + checklist |
| **Ngữ cảnh** | docs/spec/*.md (spec này tách theo mục) · docs/proposal/*.md · contracts/ (tools, api, events) · docs/conventions.md | Khi task cần | AI đọc đúng mục thay vì cả file HTML; hợp đồng chốt sáng 28/9; quy ước config, lỗi, log, async, test, prompt, git |
| **Guardrails** | scripts/guardrails.py dùng chung cho hook Claude Code, pre-commit và CI; permissions; eval gate | Tự chạy | Chặn: core import LLM/HTTP/DB · agent import tool ghi · hard-code tên model · sửa golden/contracts không lý do · đọc .env · deploy prod · --no-verify |

Vòng cải tiến: AI sai cùng lỗi 2 lần → ghi docs/agent-lessons.md → PR thêm luật/skill; lỗi nguy hiểm → thêm vào guardrails kèm test. Đây là vòng hill-climbing (§04) áp dụng cho chính quy trình build — bằng chứng team dùng harness mình đề xuất.
