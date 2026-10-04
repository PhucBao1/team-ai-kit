# NOTICE

- Dự án gốc: UI/UX Pro Max (Next Level Builder) — skill `ui-ux-pro-max`, v2.13.0
- Repo: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Commit: 09170eec67eefd46a7ae85de61b40c194020f997 (2026-09-27)
- Đường dẫn gốc: `.claude/skills/ui-ux-pro-max/` → chép `data/`, `scripts/*.py`, `references/quick-reference.md`,
  `references/pro-rules.md` y nguyên; `SKILL.md` gốc → `references/upstream-SKILL.md` (y nguyên).
- sha256 `references/upstream-SKILL.md`: ea087c341bfb5b23195c7302027268ede86da802554c18a5c4896a6017b439f9
- sha256 cây (data + scripts/*.py + references, trừ upstream-SKILL.md; lệnh ở `docs/frontend/skill-stack.md`):
  7974f52d0eadae317289829d6783229bcda31f26688ee204e534e9599d237bb5
- License: MIT — bản gốc y nguyên ở `LICENSE`.
- Cách cài chính thức của upstream: `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill` + `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill`,
  hoặc `npm install -g ui-ux-pro-max-cli && uipro init --ai claude`. Kit KHÔNG dùng: cần Node / cài global, không ghim commit,
  ghi vào `.claude/` của repo BTC.

Đã sửa: không sửa file gốc nào. Thêm `SKILL.md` (lớp bọc): đường dẫn script tương đối (thay `${CLAUDE_PLUGIN_ROOT}`), `--persist` chỉ
vào `team-ai-kit/design-system/`, stack react, luật nhóm thắng bảng màu / phông / số liệu trong `data/`.
Không chép: `scripts/tests/` (320K), CLI `cli/`, `src/`, `preview/`, `gallery/`, ảnh, các skill khác (brand, slides, design, …).
Script chỉ dùng thư viện chuẩn Python, đọc CSV cục bộ, không gọi mạng (đã kiểm import ở commit trên).

Cập nhật: như quy trình trong `../taste-skill/NOTICE.md`; thêm: kiểm lại import của `scripts/*.py` (không `urllib.request`, `requests`, `socket`, `subprocess`).
