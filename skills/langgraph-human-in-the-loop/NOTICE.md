# NOTICE — nội dung ngoài trong thư mục này

- Dự án gốc: LangChain Skills — skill `langgraph-human-in-the-loop`
- Repo: https://github.com/langchain-ai/langchain-skills
- Commit: a76fef33ed87f23a1508a5d4f119996dfe0cd2b0
- Đường dẫn gốc: `config/skills/langgraph-human-in-the-loop/SKILL.md`
- License: MIT (Copyright (c) LangChain, Inc.) — bản gốc y nguyên ở `LICENSE` cùng thư mục.

Đã sửa:
- Viết lại `description` bằng tiếng Việt, hẹp phạm vi (bước Xác nhận / `interrupt()`), bỏ phần "handling errors / 4-tier error handling".
- Thêm khối "Luật nhóm P-073 (ưu tiên hơn nội dung bên dưới)" + mẫu 3 node (chuẩn bị token → hỏi xác nhận → thực thi) + ghi chú phiên bản langgraph 1.2.12.
- Bỏ toàn bộ ví dụ TypeScript và các thẻ `<python>` / `<typescript>` / `<ex-…>` bao quanh.
- Cập nhật kết quả in ra của `result["__interrupt__"]` theo 1.2 (`Interrupt(value, id, response_schema)`); thêm `AsyncPostgresSaver` vào danh sách checkpointer prod.
- Thay các chỗ trỏ "fundamentals skill" bằng `add-langgraph-node/references/langgraph-fundamentals-python.md`.
- Thêm ghi chú nhóm sau Approval Workflow, Validation Loop, Idempotency, Subgraph re-execution (đã kiểm trên 1.2.12) và 2 dòng (P-073) trong "What You Should NOT Do".
