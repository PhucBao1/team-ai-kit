# src/tools/ — adapter hệ thống + tool GHI + MCP servers (owner: D; adapter dữ liệu giả lập: B)

- Chữ ký theo `contracts/tools.yaml` (module `src/tools/*.py`). Tool ghi (level 1–2) bắt buộc `confirmation_token`; **chỉ `src/executor` gọi**.
- Lấy dữ liệu từ `src/sim/` (thế giới giả lập) qua lớp adapter — không gọi hệ thống thật.
- Trả lỗi có cấu trúc (`code`, `message`, `retryable`), không raise lỗi trần. MCP servers ở `mcp_servers/` (từ tuần 1).
- Test trong `tests/test_tools/`.
