# 48 · Definition of Done & quy ước — Thế nào là "xong" cho một task

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

- Code merge vào main qua PR, có ít nhất 1 người review
- core/ có unit test; tool có contract test
- Không có secret trong code; biến môi trường trong .env.example
- Đụng agent / prompt / KB → chạy bộ kịch bản liên quan, không tụt
- Deploy lên dev và chạy được luồng demo
- Log có trace_id; hành động ghi có audit

- Nhánh: feat/M-12-find-options; commit theo Conventional Commits
- Python: ruff + mypy; FE: eslint + prettier
- Tên model, URL, khoá: chỉ qua config / Secret Manager
- Tiếng Việt trong prompt và mẫu tin; code và tên biến tiếng Anh
- Mọi quyết định kỹ thuật mới → một ADR 5 dòng
