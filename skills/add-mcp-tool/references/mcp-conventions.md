# Quy ước MCP server (P-073)

Đọc khi: tạo/sửa `src/tools/mcp_servers/<miền>_server.py`, đổi transport, hoặc kiểm MCP bằng Inspector.
Nguồn ý tưởng: Anthropic `skills/mcp-builder` (`reference/mcp_best_practices.md`, `SKILL.md`; Apache-2.0; https://github.com/anthropics/skills @ `8a1541c4a3`) — diễn đạt lại, áp vào dự án; **không** dùng code mẫu FastMCP 1.x (`mcp.server.fastmcp`) của bản gốc. Luật nhóm và `contracts/tools.yaml` ưu tiên hơn.

## Thư viện (đã kiểm trên máy nhóm 2026-10-01)
- `fastmcp` **4.0.10** (kéo theo `mcp` 2.2.0). Import: `from fastmcp import FastMCP, Client` · `from fastmcp.exceptions import ToolError` · `from mcp.types import ToolAnnotations`.
- KHÔNG dùng `from mcp.server.fastmcp import FastMCP` (bản 1.x trong SDK) — API khác.
- `mcp` 2.x đổi tên trường annotation sang snake_case: viết `ToolAnnotations(read_only_hint=True, destructive_hint=…)`, đọc `.read_only_hint` (`.readOnlyHint` còn chạy nhưng báo deprecated). Trên dây (JSON) vẫn là `readOnlyHint`.
- `requirements.txt` đang ghi `fastmcp>=2.0.0` → quá lỏng (2.x/3.x/4.x khác API). Nhắc **D** pin `fastmcp>=4.0,<5` (file dùng chung → báo nhóm, PR riêng).

## Tên
- Server: `{service}_mcp` trong code (`FastMCP("service_mcp")`); spec gọi `service-mcp` — cùng một thứ. Một hệ thống gốc = một server (`docs/spec/12-mcp.md`).
- Tool: snake_case, động từ đầu, **có tiền tố service** khi phơi qua MCP: `service_find_options`, `warranty_check_warranty` → tránh trùng khi client nối nhiều server. Ánh xạ 1-1 với tên trong `contracts/tools.yaml` (ghi ánh xạ trong docstring server).
- Mô tả tool = mô tả trong contract (một nguồn sự thật); mô tả là prompt → review như code.

## Annotation theo `level` trong contract
| level | Annotation | Hành vi tool MCP |
|---|---|---|
| 0 (đọc) | `readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False` | trả dữ liệu tối thiểu, che PII |
| 1–2 (ghi) | `readOnlyHint=False, destructiveHint=True, idempotentHint=True` (có idempotency key) | **CHỈ trả proposal + `confirmation_token`** để khách xác nhận; ghi thật vẫn đi qua `src/executor/` (không gọi thẳng `src/tools/` từ handler MCP) |

Annotation chỉ là **gợi ý** cho client, không phải kiểm soát. Policy theo vai trò (khách / nhân viên xưởng / hệ thống) kiểm **trong server** từ danh tính của phiên, không tin tham số do LLM đưa (`customer_id`, `vehicle_id` lấy từ phiên).

## Input / output
- Input là model Pydantic `model_config = ConfigDict(extra="forbid")` + ràng buộc (`Field(min_length=…, max_length=…)`, `Literal`). FastMCP 4 từ chối trường thừa trước khi vào hàm.
- Danh sách: luôn có `limit` (mặc định 20, tối đa 50) + `has_more`/`next_cursor`.
- Output: model Pydantic → JSON có cấu trúc; chỉ trường cần cho model (không SĐT/email/biển số thừa).

## Lỗi
- Lỗi nghiệp vụ → `raise ToolError("<MÃ_LỖI>: <chuyện gì xảy ra>. <agent nên làm gì tiếp>")`, mã lấy từ `errors` trong contract. Vd. `"SLOT_TAKEN: khung giờ đã có người đặt. Gọi lại service_find_options để lấy phương án mới."`
- Tạo server với `FastMCP(..., mask_error_details=True)` để lỗi ngoài dự kiến không lộ traceback/chi tiết nội bộ cho client.
- Không đưa input của khách nguyên văn vào thông báo lỗi.

## Transport
- **stdio** cho chạy local / Claude Desktop / Inspector. stdout là kênh giao thức → **chỉ log ra stderr** (structlog/logging cấu hình stream `sys.stderr`); không `print`.
- **Streamable HTTP** trên Cloud Run (`mcp.run(transport="http", host="0.0.0.0", port=int(os.environ["PORT"]))` hoặc mount `mcp.http_app()` vào ASGI). Service Cloud Run **không public** (`--no-allow-unauthenticated`), gọi bằng ID token của service account.
- Chạy HTTP **local**: bind `127.0.0.1`, kiểm Origin chống DNS rebinding: `run_http_async(host="127.0.0.1", allowed_origins=[...], allowed_hosts=[...])` (tham số có trong FastMCP 4.0.10). Không dùng SSE (đã thay bằng streamable HTTP).

## Khung tối thiểu (FastMCP 4)
```python
"""service_mcp — bọc tool DMS xưởng theo contracts/tools.yaml."""
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, Field

mcp = FastMCP("service_mcp", mask_error_details=True)
READ = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)


class FindOptionsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    workshop_id: str = Field(min_length=1, max_length=64)
    limit: int = Field(default=20, ge=1, le=50)


@mcp.tool(name="service_find_options", annotations=READ)
async def find_options(params: FindOptionsInput) -> dict:
    """<mô tả lấy từ contracts/tools.yaml>."""
    ...  # gọi adapter đọc; lỗi nghiệp vụ → raise ToolError("MÃ: … Hãy …")
```

## Kiểm
- Test trong `tests/test_tools/` gọi server in-memory, không mạng:
  ```python
  async with Client(mcp) as c:
      tools = {t.name: t for t in await c.list_tools()}
      assert tools["service_find_options"].annotations.read_only_hint is True
      res = await c.call_tool("service_find_options", {"params": {...}}, raise_on_error=False)
  ```
  Ca phải có: đúng · trường thừa bị từ chối · lỗi nghiệp vụ có "nên làm gì tiếp" · tool ghi không có token chỉ trả proposal (không có dòng mới trong DB).
- Thử tay: `npx @modelcontextprotocol/inspector python -m src.tools.mcp_servers.service_server` (stdio) hoặc trỏ Inspector tới URL HTTP local. `npx` chạy tạm, không cài global.
