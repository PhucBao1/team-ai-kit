# Nhật ký: AI coding agent sai gì → đã thêm luật gì

Quy tắc: cùng một lỗi lặp lại 2 lần → thêm 1 dòng vào đây và mở PR sửa luật (AGENTS.md / skill / hook).
Lỗi gây hỏng hệ thống hoặc lộ dữ liệu → thêm hook/CI, không chỉ thêm chữ. Đây chính là vòng hill-climbing (§04) áp dụng cho team.

| Ngày | Tool/agent | Lỗi | Lần | Đã sửa bằng | PR |
|---|---|---|---|---|---|
| 2026-09-28 | (ví dụ) | Agent gọi thẳng `book_appointment` trong node | 2 | Hook guardrails chặn import tool ghi trong agent/ | #— |
