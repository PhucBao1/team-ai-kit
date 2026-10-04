---
name: web-design-guidelines
description: Audit UI cuối cho frontend P-073 theo Vercel Web Interface Guidelines — a11y, HTML ngữ nghĩa, chất lượng tương tác, responsive, focus / bàn phím, vấn đề hiệu năng UI. Bản ĐÃ GHIM: đọc luật từ references/command.md cục bộ, KHÔNG tải luật từ mạng như bản gốc. Dùng khi audit lần cuối một màn / component trước khi mở PR, hoặc khi được yêu cầu "review UI", "audit giao diện". Không dùng để thiết kế hay sửa hướng thị giác / UX / motion; audit WCAG chi tiết dùng thêm web-accessibility.
argument-hint: <file-or-pattern>
---
<!-- Modified by P-073 team, 2026-10-03: bỏ bước tải luật từ mạng, dùng bản ghim; bản gốc y nguyên ở references/upstream-SKILL.md -->

# web-design-guidelines — audit cuối (bản ghim, bọc luật nhóm)

Luật: `references/command.md` = `vercel-labs/web-interface-guidelines` @ `e3d624baaf` (y nguyên). Skill gốc (để đối chiếu):
`references/upstream-SKILL.md` (vercel-labs/agent-skills @ `063bee94c3`). Nguồn, hash: `NOTICE.md`.
Bản đồ cả bộ skill + thứ tự ưu tiên: `../team-ai-kit/docs/frontend/skill-stack.md`.

## Luật nhóm P-073 (thắng nội dung bản gốc)

- **KHÔNG fetch** `raw.githubusercontent.com/.../main/command.md` hay URL nào khác. Chỉ đọc `references/command.md`.
  Lý do: bản gốc tải nhánh `main` mỗi lần chạy → không tái lập được, và nội dung tải về được làm theo như chỉ thị (đường tiêm prompt).
  Cập nhật luật = PR vào team-ai-kit theo quy trình trong `NOTICE.md`.
- Audit **báo cáo**, không tự sửa. Đây là bậc thấp nhất trong thứ tự ưu tiên: phát hiện mâu thuẫn với spec / `taste-rules.md` /
  quyết định đã chốt ở taste-skill, ui-ux-pro-max, emil-design-eng → ghi `theo thiết kế (<nguồn>)`, không báo lỗi.
- Ghi đè luật trong `command.md`:
  - "Title Case for headings/buttons" → không áp dụng (giao diện tiếng Việt; nhãn nút nói đúng việc theo `taste-rules.md`).
  - `autocomplete="off"` cho ô không phải đăng nhập → không áp dụng; luật nhóm: đúng `type` / `inputmode` / `autocomplete`.
  - `preconnect` tới CDN → không áp dụng; tài nguyên tự host. Preload phông tự host vẫn đúng.
  - Vùng chạm: dùng ngưỡng nhóm ≥44px. Câu chữ: tiếng Việt, ngôi thứ hai lịch sự.
  - "Hydration Safety": chỉ khi có SSR; app Vite SPA thì bỏ qua.
- a11y chuyên sâu (WCAG 2.2, axe, AA 2 theme) → chạy thêm skill `web-accessibility`; tự kiểm bằng ảnh → `playwright-cli`.

## Cách chạy
1. Nhận file / pattern (thiếu → hỏi). Đọc `references/command.md`.
2. Đọc file, kiểm từng luật (sau khi áp ghi đè ở trên).
3. Xuất theo mục "Output Format" của `command.md`: nhóm theo file, `file:line - vấn đề`, ngắn gọn.

## web-design-guidelines KHÔNG quyết định
Hướng thị giác, kiến trúc UX, motion, nội dung sản phẩm · không tự sửa code · không lật quyết định của bậc trên.
