# NOTICE — nội dung ngoài trong thư mục này

Áp cho `langgraph-fundamentals-python.md` và `langgraph-persistence.md`.

- Dự án gốc: LangChain Skills — skill `langgraph-fundamentals` và `langgraph-persistence`
- Repo: https://github.com/langchain-ai/langchain-skills
- Commit: a76fef33ed87f23a1508a5d4f119996dfe0cd2b0
- Đường dẫn gốc:
  - `config/skills/langgraph-fundamentals/references/python.md` → `langgraph-fundamentals-python.md`
  - `config/skills/langgraph-persistence/SKILL.md` → `langgraph-persistence.md`
- License: MIT (Copyright (c) LangChain, Inc.) — bản gốc y nguyên ở `LICENSE` cùng thư mục.

Đã sửa — `langgraph-fundamentals-python.md`:
- Thêm dòng `<!-- Modified by P-073 team … -->` và khối "Luật nhóm P-073 (ưu tiên hơn nội dung bên dưới)".
- Bỏ câu trỏ `../SKILL.md` của skill gốc.
- Thêm cảnh báo Command + cạnh tĩnh (lấy từ `langgraph-fundamentals/SKILL.md` gốc) và cảnh báo `Command(update=...)` làm input.
- Thêm ghi chú langgraph 1.2.12: tham số `RetryPolicy`, `add_node(timeout=, error_handler=)`, `set_node_defaults`, mặc định `handle_tool_errors`,
  `recursion_limit` mặc định 10007 + cách đặt giới hạn.

Đã sửa — `langgraph-persistence.md`:
- Chỉ giữ phần Python; bỏ toàn bộ TypeScript, frontmatter, mục Store / long-term memory, `fix-store-injection`, ví dụ `create_agent` (parallel subgraph namespacing).
- Thêm khối luật nhóm, mục "Bẫy: update_state + reducer" (gồm `as_node`, đã kiểm trên 1.2.12), ghi chú chế độ checkpointer subgraph cho nhóm.
- Thêm mục "AsyncPostgresSaver + pool psycopg cho FastAPI" (lifespan, `AsyncConnectionPool`, `setup()` một lần ở bước deploy/migration).
- Sửa ví dụ `fix-inmemory-not-for-production`: bỏ `checkpointer.setup()` trong code chạy app.
