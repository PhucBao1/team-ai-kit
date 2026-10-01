# NOTICE

- Dự án gốc: Web Quality Skills (Addy Osmani) — skill `accessibility`
- Repo: https://github.com/addyosmani/web-quality-skills
- Commit: afa8da942115f2961fdbfa80807ea0b232ff6c00
- Đường dẫn gốc: `skills/accessibility/` (`SKILL.md`, `references/WCAG.md`, `references/A11Y-PATTERNS.md`)
- License: MIT — bản gốc y nguyên ở `LICENSE`.

Đã sửa (chỉ `SKILL.md`; hai file trong `references/` giữ nguyên):
- Đổi `name` thành `web-accessibility`; viết lại `description` tiếng Việt, hẹp phạm vi, trỏ `add-frontend-screen` / `playwright-cli`; bỏ khối `metadata`.
- Thêm dòng `<!-- Modified by P-073 team … -->` và khối "Luật nhóm P-073 (ưu tiên hơn nội dung bên dưới)": audit trên app Vite local, vùng chạm ≥44px, `lang="vi"`, AA cả 2 theme, định dạng báo cáo.
- Quy trình audit: axe qua `@axe-core/playwright` + `playwright-cli` là mặc định; Chrome DevTools MCP / Lighthouse thành tuỳ chọn.
- Mục kiểm tự động: bỏ `npm install @axe-core/cli -g`, thay bằng Playwright Test trong `frontend/e2e/`.
- Mức vùng chạm 24px → 44px (luật nhóm); ví dụ `lang="en"` → `lang="vi"`.
- Rút gọn: bảng mức tuân thủ, ví dụ media, timing (JS), consistent navigation, redundant entry, accessible authentication.
- Thêm 2 mục vào checklist kiểm tay (2 theme, text-spacing / reflow); bỏ link tới skill `web-quality-audit` (không chép vào kit).
