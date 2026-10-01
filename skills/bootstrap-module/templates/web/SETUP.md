# Dựng frontend/ (người C)

```bash
npm create vite@latest frontend -- --template react-ts && cd frontend
npm i @tanstack/react-query
npm i -D tailwindcss @tailwindcss/vite openapi-typescript vitest @playwright/test eslint prettier
```
(Kiểm tra lại lệnh cài Tailwind theo docs hiện hành.)

1. `tsconfig.app.json`: bật `"strict": true, "noUncheckedIndexedAccess": true, "noImplicitOverride": true`.
2. `package.json` scripts:
   - `"gen:api": "openapi-typescript ../contracts/api.yaml -o src/api/types.ts"`
   - `"lint": "eslint . && prettier --check ."`, `"test": "vitest"`
3. Chạy `npm run gen:api`. Mọi kiểu dữ liệu API import từ `src/api/types.ts` — không viết tay.
4. Mock: `src/mocks/` trả dữ liệu đúng kiểu cho `/chat` (SSE giả), `/jobs`, `/handoffs` tới khi API xong.
5. Cấu trúc: `src/api/` (hook TanStack Query) · `src/screens/{chat,jobs,console,demo}/` · `src/i18n/vi.ts` · `e2e/`.
6. Nhãn "Trợ lý AI" luôn hiển thị trong chat.
7. Dark mode ngay từ đầu: Tailwind `darkMode: 'class'` + nút chuyển; mọi màu dùng biến / cặp `dark:` (tiêu chí UI/UX của BTC).
8. Build production: `npm run build`; deploy cùng skill `deploy-live`.
