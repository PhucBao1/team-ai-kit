---
name: add-mcp-tool
description: Thêm hoặc sửa một tool (đọc hoặc ghi) theo contracts/tools.yaml — tool đọc @tool trong src/agents/tools, tool ghi trong src/tools chỉ executor gọi, kèm test và MCP server. Dùng khi task nói "thêm tool", "agent cần tra/ghi X", sửa chữ ký tool, hoặc sửa src/agents/tools, src/tools, contracts/tools.yaml.
---

# Thêm / sửa tool

Spec: `../team-ai-kit/docs/spec/11-tools.md`, `12-mcp.md`, `17-core.md`. Tool sai = agent sai — làm đủ bước.

## Bước
1. **Phân loại** theo `level`: 0 đọc · 1 ghi nội bộ · 2 ảnh hưởng khách (đặt / đổi lịch, ticket, đổi trả, sửa thông tin) → bắt buộc `confirmation_token`.
2. **Hợp đồng trước code**: thêm mục vào `contracts/tools.yaml` theo `templates/contract_entry.yaml` (name, level, milestone, module, description, input, output, errors).
   Sửa mục đã có → PR riêng + ADR (skill `write-adr`) vì A, C phụ thuộc.
3. **Code đúng chỗ**:
   - level 0 → `src/agents/tools/<miền>.py`, hàm có `@tool` (langchain_core) như `example_tool.py` của template — mẫu `templates/read_tool.py`.
   - level 1–2 → `src/tools/<miền>.py` (hàm thường, Pydantic input/output, `idempotency_key`) — mẫu `templates/write_tool.py`.
     Thêm nhánh xử lý trong `src/executor/` (+ bước bù nếu trong saga). **Không** đăng ký vào danh sách tool của agent.
4. Lấy dữ liệu từ `src/sim/` qua adapter; trả lỗi có cấu trúc (`code`, `message`, `retryable`).
5. **Mô tả cho model** (docstring của tool đọc): làm gì, khi nào KHÔNG dùng, 1 ví dụ tham số — đây là prompt.
6. **Test** ở `tests/test_tools/` (đọc) hoặc `tests/test_executor/` (ghi) theo `templates/test_tool.py`: đúng, sai input, không tìm thấy, gọi trùng.
7. **MCP (từ tuần 1)**: đăng ký trong `src/tools/mcp_servers/<miền>_server.py` (FastMCP), đúng tên + mô tả như contract. Đọc `references/mcp-conventions.md` khi tạo/sửa server.
   - Thư viện: **`fastmcp` 4.0.10** (kèm `mcp` 2.2.0): `from fastmcp import FastMCP, Client` · `from fastmcp.exceptions import ToolError` · `from mcp.types import ToolAnnotations`. Không dùng `mcp.server.fastmcp` (1.x) hay code mẫu cũ.
   - `requirements.txt` đang `fastmcp>=2.0.0` (quá lỏng, 2.x→4.x đổi API) → nhắc **D** pin `fastmcp>=4.0,<5` (PR riêng, báo nhóm).
   - Tên server `{service}_mcp`, tool có tiền tố service; annotation theo `level`: 0 → `read_only_hint=True`; 1–2 → `destructive_hint=True` và tool MCP **chỉ trả proposal + token**, ghi thật vẫn qua `src/executor/`.
   - Input Pydantic `extra="forbid"`; lỗi `ToolError("MÃ: … <agent nên làm gì tiếp>")`; `FastMCP(..., mask_error_details=True)`; policy theo vai trò kiểm trong server (annotation chỉ là gợi ý).
   - Transport: stdio local (chỉ log ra stderr) · streamable HTTP trên Cloud Run (không public); HTTP local bind `127.0.0.1` + kiểm Origin. Thử tay: `npx @modelcontextprotocol/inspector`.
8. Kiểm: `make -f ../team-ai-kit/kit.mk contracts` · `ruff check src/ tests/` · `pytest tests/`.

## Kiểm tra trước khi xong
- [ ] `check_contracts` xanh (tên + input khớp code; level 2 có `confirmation_token`)
- [ ] Không file nào trong `src/agents/` (ngoài `tools/`) nhắc tên tool level 2; không import `src.tools`
- [ ] Không trả PII thừa cho model
- [ ] MCP: annotation đúng `level`; tool ghi qua MCP không ghi trực tiếp; test `Client(mcp)` in-memory có ca trường thừa bị từ chối; stdio server không ghi ra stdout
