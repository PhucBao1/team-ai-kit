# NOTICE

- Dự án gốc: Playwright CLI (Microsoft) — skill `playwright-cli`
- Repo: https://github.com/microsoft/playwright-cli
- Commit: b85c7a736bb473bf55b584e54a09ffa698d6d871
- Đường dẫn gốc: `skills/playwright-cli/` (`SKILL.md`, `references/*.md`)
- License: Apache-2.0 — bản gốc y nguyên ở `LICENSE`. Mỗi file đã sửa có dòng đầu `<!-- Modified by P-073 team, 2026-10-01: … -->`.

Đã sửa:
- `SKILL.md`: viết lại `description` tiếng Việt (hẹp: tự kiểm màn frontend local, debug `frontend/e2e/*.spec.ts`; không cho backend); bỏ `allowed-tools`;
  thêm khối "Luật nhóm P-073" (gọi qua `cd frontend && npx --no-install playwright cli`, cấm cài global / `npm init playwright@latest`,
  quy trình chụp sáng / tối / 390×844, `.playwright-cli/` trong `.gitignore`, ảnh chỉ đính PR qua `review-pr`, test ở `frontend/e2e/`, kế hoạch trong card);
  bỏ mục WebMCP, các lệnh `attach --extension` / `attach --cdp` / `detach`, mục "URLs with & on Windows";
  thay mục Installation (không cài gì, báo người); rút gọn mục đính PR; bỏ mục Mouse, ví dụ multi-tab, ví dụ tracing trùng; rút gọn mục Storage.
- `references/test-generation.md`: kế hoạch ghi trong card thay vì `specs/*.plan.md`; test / seed ở `frontend/e2e/`; bỏ `npm init playwright@latest`; seed dùng app local + reset thế giới giả lập.
- `references/playwright-tests.md`: thêm ghi chú chạy trong `frontend/` (giữ `attach tw-…` vì đó là gắn vào phiên debug của test, không phải `--cdp/--extension`).
- `references/session-management.md`: bỏ mục "Attaching to a Running Browser".
- `references/pr-attachments.md`: chỉ đính qua `review-pr`, không commit, không dữ liệu khách thật; cổng `5173`; bỏ mục "From CI" (CI thuộc BTC).
- `references/video-recording.md`: mục đính PR → chỉ qua `review-pr`.
- `references/running-code.md`: bỏ ví dụ chờ `networkidle`.
- Giữ nguyên: `references/element-attributes.md`, `request-mocking.md`, `storage-state.md`, `tracing.md`.
