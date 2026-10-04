# NOTICE

- Dự án gốc: Taste Skill (Leonxlnx) — skill `taste-skill` (install name `design-taste-frontend`, v2)
- Repo: https://github.com/Leonxlnx/taste-skill
- Commit: ce26fc25c0e5e8cab638f883de62d9a86ee5e45b (2026-09-26)
- Đường dẫn gốc: `skills/taste-skill/SKILL.md` → `references/upstream-SKILL.md` (y nguyên)
- sha256 `references/upstream-SKILL.md`: aa194351b246b8b4799099d4ed7b033d29eab6e6e3d58d8d2172978be7b3ec89
- License: MIT — bản gốc y nguyên ở `LICENSE`.
- Cách cài chính thức của upstream: `npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"` (không ghim commit).
  Kit dùng bản chép ghim commit thay thế để tái lập được và để bọc luật nhóm.

Đã sửa: không sửa file gốc. Thêm `SKILL.md` (lớp bọc): tên `taste-skill`, description tiếng Việt hẹp phạm vi, khối luật nhóm
(thứ tự ưu tiên, phạm vi theo bề mặt, stack Vite thay Next.js, phông tự host, cấm tài nguyên ngoài lúc chạy, token 2 theme).
Không chép: các skill khác trong repo (gpt-tasteskill, soft-skill, brutalist-skill, imagegen-*, …), `research/`, ảnh.

Cập nhật: clone repo ở commit mới → so `diff` với `references/upstream-SKILL.md` → đọc toàn bộ thay đổi (tìm fetch mạng, lệnh cài,
chỉ thị lạ) → chép đè → cập nhật commit + sha256 ở đây và ở `docs/frontend/skill-stack.md` → `python3 guardrails/validate_kit.py`.
