# NOTICE — nội dung bên ngoài trong `security-review/references/`

`SKILL.md` của skill và `llm-app-checks.md` do nhóm P-073 tự viết. Các file dưới đây chép hoặc chuyển thể từ nguồn ngoài.

## 1. OpenAI Skills — Apache License 2.0 (`LICENSE.txt`)
- Repo: https://github.com/openai/skills · commit `49f948faa9`
- `fastapi.md` ← `skills/.curated/security-best-practices/references/python-fastapi-web-server-security.md`
- `react.md` ← `skills/.curated/security-best-practices/references/javascript-typescript-react-web-frontend-security.md`
- `threat-model.md` ← `skills/.curated/security-threat-model/` (`SKILL.md`, `references/prompt-template.md`, `references/security-controls-and-assets.md`)

Đã sửa:
- `fastapi.md`: thêm dòng `Modified` + khối luật nhóm ở đầu; bỏ rule FASTAPI-AUTH-003, SESS-001, SESS-002, XSS-001, SSTI-001, FILES-001, FILES-002, UPLOAD-001, REDIRECT-001. Rule ID còn lại và nội dung giữ nguyên.
- `react.md`: thêm dòng `Modified` + khối luật nhóm; bỏ REACT-TT-001, SRI-001, 3P-001, SW-001, POSTMSG-001, FILE-001. Rule ID còn lại giữ nguyên.
- `threat-model.md`: viết lại rút gọn bằng tiếng Việt; bỏ bước bắt buộc dừng hỏi người khi card đủ ngữ cảnh; thêm ranh giới LLM (L1–L4), bảng tài sản/kẻ tấn công/đường lạm dụng/thang mức theo dự án, cột STRIDE; giữ mã TM-001 và quy tắc Mermaid.

## 2. wshobson/agents — MIT (`LICENSE-MIT-wshobson`)
- Repo: https://github.com/wshobson/agents · commit `156b7a5e7a`
- Nguồn ý: `plugins/security-scanning/skills/stride-analysis-patterns/SKILL.md` (bảng STRIDE: câu hỏi + họ biện pháp)
- Đã sửa: diễn đạt lại bằng tiếng Việt, gộp vào bảng STRIDE và cột STRIDE của `threat-model.md`.

## 3. Trail of Bits Skills — CC BY-SA 4.0 (`LICENSE-CC-BY-SA-4.0`)
- Repo: https://github.com/trailofbits/skills · commit `82fe822625` · tác giả: Trail of Bits
- `insecure-defaults.md` ← `plugins/insecure-defaults/` (`commands/audit.md`, `references/*.md`, `references/*.json` seeds)
- `sharp-edges-python.md` ← `plugins/sharp-edges/skills/sharp-edges/` (`SKILL.md`, `references/config-patterns.md`, `auth-patterns.md`, `lang-python.md`)

Đã sửa:
- `insecure-defaults.md`: bỏ quy trình Workflow tool/`${CLAUDE_PLUGIN_ROOT}`; chuyển 6 nhóm (fallback secrets, default credentials, fail-open, weak crypto + so sánh không hằng thời gian, permissive access, debug features) thành checklist tiếng Việt + lệnh `rg` chạy tay; regex seed điều chỉnh cho Python/FastAPI/Vite/Cloud Run; ví dụ theo dự án (`CONFIRM_TOKEN_SECRET`, CORS, `/docs`).
- `sharp-edges-python.md`: diễn đạt lại thành bộ câu hỏi cho token/validator/config của dự án; bỏ các ngôn ngữ khác, case study, agent.

Bản chuyển thể `insecure-defaults.md` và `sharp-edges-python.md` cũng theo CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/).
