# Test frontend P-073 — Vitest + Playwright Test

Đọc khi viết / sửa test trong `frontend/`. Luật nhóm; thắng gợi ý từ nguồn ngoài. Debug spec đỏ → skill `playwright-cli`.

## 1. Vitest (component, hook, logic)

`vitest.config.ts`: `environment: 'jsdom'`, `setupFiles: ['./src/test/setup.ts']`.

```ts
// src/test/setup.ts
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

// jsdom không có matchMedia (dark mode theo hệ thống) và ResizeObserver
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false, media: query, onchange: null,
    addEventListener: vi.fn(), removeEventListener: vi.fn(),
    addListener: vi.fn(), removeListener: vi.fn(), dispatchEvent: vi.fn(),
  })),
});
globalThis.ResizeObserver ??= class { observe() {} unobserve() {} disconnect() {} };

afterEach(() => { cleanup(); vi.restoreAllMocks(); localStorage.clear(); });
```

- Tương tác bằng `const user = userEvent.setup(); await user.click(…)` — không `fireEvent`.
- Truy vấn theo vai trò: `getByRole('button', { name: 'Xác nhận đặt lịch' })` > `getByLabelText` > `getByText` > `getByTestId`.
- Bọc component trong `QueryClientProvider` với `new QueryClient({ defaultOptions: { queries: { retry: false } } })` mới cho mỗi test.
- Mỗi view test đủ: loading (skeleton có `aria-busy`), empty (câu hướng dẫn), lỗi (thông báo + "Thử lại" gọi lại query), dữ liệu.
- axe cho component: `vitest-axe` (hoặc `jest-axe`) → `expect(await axe(container)).toHaveNoViolations()`. Chưa có trong
  `package.json` → thêm devDependency trong PR riêng, ghi lý do trong PR.
- Dark mode: test nút chuyển đổi đủ vòng (sáng → tối → theo máy → sáng), `document.documentElement.classList` đổi đúng, lựa chọn được nhớ.

## 2. Playwright Test (`frontend/e2e/*.spec.ts`, kịch bản demo)

```ts
import { test, expect, devices } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.beforeEach(async ({ page }) => {
  // Mock LLM / agent: demo tất định, không gọi model thật
  await page.route('**/api/v1/chat/stream', (route) =>
    route.fulfill({ status: 200, contentType: 'text/event-stream', body: SSE_FIXTURE }));
  await page.goto('/');            // baseURL trong playwright.config.ts
});

test('khách xác nhận đặt lịch', async ({ page }) => {
  await page.getByRole('button', { name: 'Xác nhận đặt lịch' }).click();
  await expect(page.getByRole('status')).toContainText('Đã đặt lịch');
});

test.describe('tối + điện thoại', () => {
  test.use({ ...devices['Pixel 7'], colorScheme: 'dark' });
  test('màn chat không vi phạm a11y', async ({ page }) => {
    const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
    expect(r.violations).toEqual([]);
  });
});
```

Luật:
- Locator: `getByRole` > `getByLabel` > `getByText` > `getByTestId`. KHÔNG CSS selector / XPath.
- Chỉ dùng assertion tự retry (`await expect(locator).toBeVisible()/toHaveText()…`). CẤM `page.waitForTimeout`, CẤM `networkidle`,
  không `expect(await locator.textContent())`.
- Mỗi kịch bản độc lập, bắt đầu từ seed: reset thế giới giả lập (endpoint reset của Demo panel theo `contracts/api.yaml`, hoặc mock
  `VITE_USE_MOCK=true`) trong `beforeEach`. Không phụ thuộc thứ tự test.
- Mock LLM / agent bằng `page.route` (fixture SSE trong `e2e/fixtures/`) để demo tất định; không gọi model thật trong e2e.
- Màn khách: chạy cả `colorScheme: 'light'` và `'dark'`, cả desktop và `devices['Pixel 7']`; axe `wcag2a` + `wcag2aa` = 0 vi phạm.
- Không làm yếu assertion / tăng timeout bừa để xanh. Lỗi đã biết, người đã xác nhận là bug → `test.fixme(…)` + comment link issue.
- Chạy: `cd frontend && PLAYWRIGHT_HTML_OPEN=never npx playwright test e2e/<tên>.spec.ts`.

## 3. QA inventory — trước khi báo "xong"

Lập bảng trong mô tả PR, mỗi tuyên bố "xong" ứng với 1 kiểm chức năng + 1 ảnh chụp đúng trạng thái:

| Tuyên bố | Kiểm chức năng (test / thao tác) | Ảnh |
|---|---|---|
| Hiện lỗi + Thử lại | Vitest `JobList.error` + bấm "Thử lại" trên app thật (mock 500 bằng `route`) | `jobs-loi-sang.png` |
| Dark mode | Toggle đủ vòng sáng → tối → sáng, reload vẫn nhớ | `jobs-toi.png` |
| Mobile | 390×844 không cuộn ngang, Tab không bị che | `jobs-390.png` |

- Ảnh tối thiểu mỗi màn: sáng 1280×800, tối 1280×800, mobile 390×844 (chụp bằng skill `playwright-cli`).
- Ảnh không commit vào repo; đính vào PR qua skill `review-pr`.
