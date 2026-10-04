# frontend/ — giao diện (owner: C) · spec `../team-ai-kit/docs/spec/20-ui.md`, `21-fe.md`

- React + Vite + TypeScript strict + Tailwind + TanStack Query. Kiểu API sinh từ `../contracts/api.yaml` (`npm run gen:api`) — không viết tay.
- Chưa có backend → mock trong `src/mocks/` đúng kiểu. Chat dùng `/api/v1/chat/stream` (SSE, tự nối lại); fallback `/api/v1/chat`.
- 4 màn: Chat khách · "Việc của tôi" · Console nhân viên · Demo panel. Nút Xác nhận hiển thị đủ tham số hành động.
- Chấm UI/UX: **responsive (mobile), dark mode, loading state cho mọi lời gọi LLM, thông báo lỗi thân thiện, accessibility**. Luôn có nhãn "Trợ lý AI".
- Chuỗi tiếng Việt ở `src/i18n/vi.ts`. Test: Vitest (logic) + Playwright (kịch bản demo).

## Skill cho frontend (luật nhóm thắng tài liệu ngoài)
- Dựng / sửa màn hình hoặc component → skill `add-frontend-screen` (quy trình + 15 luật gu thẩm mỹ, React, WCAG 2.2, test).
- Tự kiểm UI bằng mắt (chụp sáng / tối / 390×844) hoặc debug spec `e2e/*.spec.ts` → skill `playwright-cli` (`npx --no-install playwright cli`, không cài global).
- Audit a11y / kiểm WCAG một màn → skill `web-accessibility` (vùng chạm ≥44px, `lang="vi"`, AA cả 2 theme).
- Hướng thị giác / kiến trúc UX / motion / audit cuối → `taste-skill` > `ui-ux-pro-max` > `emil-design-eng` > `web-design-guidelines` (bản ghim, bọc luật nhóm). Phân vai + thứ tự ưu tiên: `../team-ai-kit/docs/frontend/skill-stack.md`.
- **Design system (bậc 2, cùng taste-rules):** `../team-ai-kit/design-system/proactive-care/MASTER.md`, rồi `pages/<landing|customer|cskh>.md` (chỉ chứa ngoại lệ). Chỉ dùng token trong `tokens.md`; 9 trạng thái AI theo MASTER §12. Quy trình sửa: `../team-ai-kit/docs/frontend/design-governance.md`.
