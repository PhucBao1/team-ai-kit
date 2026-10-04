# NOTICE

Hai nguồn (cùng tác giả Vercel Labs, MIT):

1. Skill `web-design-guidelines`
   - Repo: https://github.com/vercel-labs/agent-skills — commit 063bee94c3f4df8453406c830b0a7df0f2860278 (2026-08-28)
   - Đường dẫn gốc: `skills/web-design-guidelines/SKILL.md` → `references/upstream-SKILL.md` (y nguyên, chỉ để đối chiếu)
   - sha256: f4647ca866a3accf763777f83e7682954f0187cd6bea7eea0399796652414e8f
   - License: README ghi "MIT"; repo không có file LICENSE ở gốc tại commit này.
2. Bộ luật mà skill trên tải lúc chạy
   - Repo: https://github.com/vercel-labs/web-interface-guidelines — commit e3d624baaf29dc1fc645aff3e38f03e564d2d6b1 (2026-08-17)
   - Đường dẫn gốc: `command.md` → `references/command.md` (y nguyên)
   - sha256: 5a775e6411f790f518dbc9c1fa7c50a89e6873502d9a3530a6eb223a590bcfe8
   - License: MIT — bản gốc y nguyên ở `LICENSE` (Copyright (c) 2025 Vercel Labs).

Hành vi bản gốc: mỗi lần chạy, WebFetch `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
rồi làm theo "all the rules and output format instructions" trong nội dung tải về. Nhánh `main` thay đổi bất kỳ lúc nào →
kết quả audit không tái lập được, và ai sửa được file đó thì điều khiển được agent (tiêm prompt). Đây là lý do trước đây kit
không dùng skill này (xem `THIRD_PARTY.md`).

Đã sửa: `SKILL.md` viết lại (lớp bọc): bỏ bước fetch, đọc `references/command.md` cục bộ; description tiếng Việt; khối luật nhóm
(bậc thấp nhất, chỉ báo cáo; ghi đè Title Case, `autocomplete="off"`, preconnect CDN, vùng chạm 44px; SSR-only bỏ qua với Vite).

Cập nhật luật: clone web-interface-guidelines ở commit mới → `diff` với `references/command.md` → đọc toàn bộ thay đổi → chép đè →
cập nhật commit + sha256 ở đây và ở `docs/frontend/skill-stack.md` → PR có người duyệt.
