# Quy ước code chung

Mỗi mục: một luật + một ví dụ đúng. AI coding agent viết code mới theo đúng các mẫu này.
Muốn đổi quy ước → PR sửa file này trước, rồi mới đổi code.

## 1. Cấu trúc (theo template BTC, repo P-073)

```
src/
  main.py  config.py            # template — giữ /health, /api/v1 prefix, get_settings()
  api/routes.py                 # endpoint /api/v1/*
  agents/  graph.py state.py nodes/ subgraphs/ prompts/ tools/   # LangGraph; tools/ = tool ĐỌC (@tool)
  services/llm.py               # get_llm("chat" | "reason" | "lite")
  models/schemas.py             # Pydantic API + output LLM
  core/                         # luật tất định (không I/O)
  executor/                     # nơi duy nhất được ghi
  tools/  mcp_servers/          # adapter + tool GHI + MCP
  sim/ detect/ kb/ db/          # giả lập · detector · knowledge base · DB
tests/test_<module>/            # CI BTC chỉ chạy tests/
frontend/  eval/  contracts/  docs/architecture/  migrations/
```
Import tuyệt đối `from src.core.warranty import ...`. Chiều phụ thuộc cho phép:
`api → agents → agents.tools (đọc)` · `api / agents.confirm → executor → tools (ghi) → sim` · `mọi nơi → core`. `agents` KHÔNG import `src.tools`.

## 2. Cấu hình: một chỗ, có kiểu

Dùng `get_settings()` trong `src/config.py` (template, pydantic-settings, có cache). Thêm trường mới **có giá trị mặc định**
(CI BTC chỉ đặt `APP_ENV=test`, `OPENAI_API_KEY=test-key`). `APP_ENV` chỉ nhận `development | production | test`.
`src/core/` nhận giá trị qua tham số hàm, không gọi `get_settings()`.

## 3. Kiểu dữ liệu & thời gian

- Pydantic v2 ở mọi biên. `model_config = ConfigDict(frozen=True)` cho kết quả của `core/`.
- Thời gian luôn có timezone: `datetime.now(tz=VN_TZ)` với `VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")`. Lưu DB dạng UTC.
- Trạng thái dùng `Literal[...]` hoặc `StrEnum`, không dùng chuỗi tự do.
- Tiền: `int` (đồng). Quãng đường: `float` km. Tên trường có đơn vị: `odometer_km`, `soc_pct`, `duration_min`.

## 4. Lỗi

- Giữa các module: trả kết quả có cấu trúc, không raise lỗi trần.
```python
class ToolError(BaseModel):
    code: str            # MÃ_VIẾT_HOA, liệt kê trong contracts/tools.yaml
    message: str         # cho người đọc log, không hiện nguyên văn cho khách
    retryable: bool = False
```
- Chỉ raise ở biên API (`raise HTTPException(...) from e`) hoặc lỗi lập trình (`ValueError` khi vi phạm tiền điều kiện).
- Không `except Exception: pass`. Bắt lỗi cụ thể; không bắt được thì log + chuyển người.

## 5. Log & trace

```python
import structlog
log = structlog.get_logger()

log.info("proposal.created", journey_id=j.id, option_count=len(opts))   # tên sự kiện dạng a.b, dữ liệu là field
```
- JSON, luôn có `trace_id` (gắn qua contextvars ở middleware), có `journey_id`/`job_id` khi có.
- KHÔNG log: tên, số điện thoại, biển số, nội dung tin nhắn khách. Log id thay vì dữ liệu.
- Mỗi node LangGraph và mỗi tool là một span OTel có tên `node.<tên>` / `tool.<tên>`.

## 6. Async & gọi ra ngoài

```python
async with asyncio.TaskGroup() as tg:                      # song song khi độc lập
    v = tg.create_task(get_vehicle_status(vin))
    p = tg.create_task(get_parts_availability(ws, parts))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(0.2, max=2),
       retry=retry_if_exception_type(TransientError))    # chỉ retry lỗi retryable
async def call_upstream(...): ...
```
- Mọi lời gọi mạng/LLM có timeout (`asyncio.timeout(…)`). Không `requests`, không `time.sleep` trong async.
- Ghi dữ liệu: idempotency key; nhiều bước → saga trong `executor/`.

## 7. Test

- Tên test mô tả hành vi: `test_<khi_nào>_<thì_sao>` — vd. `test_odometer_over_limit_returns_expired`.
- Fixture chung ở `tests/conftest.py` (template có `client`, `mock_llm`; đội thêm `seeded_world`, `clock`). Coverage ≥ 60% (`make test-cov`).
- Unit test không gọi model thật, không gọi mạng. Test gọi model thật đánh dấu `@pytest.mark.llm` (chỉ chạy trong eval).
- Luật nghiệp vụ trong `core/`: thêm property test (hypothesis) cho biên (đúng ngưỡng km, đúng ngày hết hạn).
- Bug fix: viết test tái hiện (fail) trước, rồi sửa.

## 8. Prompt

- Ở `src/agents/prompts/<tên>_vi.md`, dòng đầu `<!-- v<số> · <ngày> · <người> -->`.
- Đổi prompt = PR có bảng eval-smoke trước/sau. Không nhúng prompt dài trong code Python.
- Chính sách, giá, ngày giờ KHÔNG nằm trong prompt — lấy từ tool/KB lúc chạy.

## 9. Frontend

- Kiểu dữ liệu API sinh từ `contracts/api.yaml` bằng `openapi-typescript` → `frontend/src/api/types.ts`. Không viết tay kiểu trùng. Dark mode + responsive + loading state bắt buộc.
- Gọi API qua TanStack Query hook trong `src/api/`. Component không gọi `fetch` trực tiếp.
- Chuỗi hiển thị ở `src/i18n/vi.ts`. Nút Xác nhận hiển thị đủ tham số hành động (việc, xe, giờ, xưởng, thời lượng).

## 10. Git & PR

- Nhánh `develop` là trục chính; nhánh việc `<người>/<mã-task>-<mô-tả>` (vd. `b/B1.04-seed-world`) sống < 1 ngày, PR < ~300 dòng vào `develop`; `develop → main` ở mỗi mốc (30/9, 4/10, 11/10, 18/10).
- Squash merge. Conventional Commits: `feat(core): luật bảo hành xe dịch vụ`, `fix(agents): …`, `docs: …`. Commit đều mỗi ngày (BTC xem git history).
- Chạy nhiều AI agent song song → mỗi task một `git worktree`, không để 2 agent sửa cùng thư mục.
- File dùng chung dễ xung đột (`contracts/`, `migrations/`, `src/agents/state.py`, `tests/conftest.py`, `requirements.txt`, `src/config.py`): báo nhóm trước khi sửa.

## 11. Python bổ sung (2026-10-01)

Bổ sung, không thay các mục trên. Bảo mật → skill `security-review`; DB → skill `db-migration`.

1. **Async hygiene.** Hàm chặn (CPU, thư viện sync) trong async → `await asyncio.to_thread(fn, ...)`. Gọi song song ra ngoài có giới hạn: `asyncio.Semaphore(n)`. Bắt `asyncio.CancelledError` thì phải `raise` lại (không nuốt — timeout/huỷ request dựa vào nó).
```python
async with sem:                                   # sem = asyncio.Semaphore(4) ở cấp module
    try:
        return await asyncio.wait_for(call_llm(p), timeout=20)
    except asyncio.CancelledError:
        log.info("llm.cancelled", journey_id=jid)
        raise
```
2. **Retry đúng 1 tầng.** Đã bọc `tenacity` thì tắt retry của client: `ChatOpenAI(..., max_retries=0)` (đặt trong `src/services/llm.py`), tương tự httpx/SDK khác. Hai tầng retry = số lần gọi nhân lên và vượt timeout.
3. **Không gọi LLM / HTTP / MCP trong transaction DB.** Gọi xong mới mở transaction (`db-migration` luật 1).
4. **Thời gian trong DB là `timestamptz`** (`sa.DateTime(timezone=True)`); cấm `datetime.utcnow()`.
5. **Idempotency bằng `UNIQUE(idempotency_key)` + `INSERT … ON CONFLICT DO NOTHING RETURNING`**, không select-rồi-insert (`db-migration` luật 5).
6. **Không trả ORM/SQLModel table model ra API.** Endpoint khai `response_model=<Schema>` (Pydantic trong `src/models/schemas.py`) và map tường minh — tránh lộ cột nội bộ/PII.
7. **Python 3.11:** không dùng cú pháp 3.12+ — `class Box[T]:`, `def f[T](x: T)`, `type Alias = ...`. Dùng `TypeVar`/`Generic`, `TypeAlias`.
8. **Docstring kiểu Google** cho hàm public (`Args:`, `Returns:`, `Raises:` khi có).
```python
def check_warranty(odometer_km: float, start: date, today: date) -> WarrantyResult:
    """Kiểm điều kiện bảo hành sơ bộ theo km và thời hạn.

    Args:
        odometer_km: Số km hiện tại của xe.
        start: Ngày kích hoạt bảo hành.
        today: Ngày kiểm (truyền vào, không đọc đồng hồ).

    Returns:
        Kết quả sơ bộ kèm lý do.
    """
```
9. **structlog với contextvars.** Cấu hình processor `structlog.contextvars.merge_contextvars`; middleware gọi `structlog.contextvars.bind_contextvars(trace_id=...)` đầu request và `clear_contextvars()` cuối. Log lỗi bằng `error_type=type(e).__name__` (+ mã lỗi), **không** `str(e)` (có thể chứa input khách/PII); stack trace chỉ ở log server (`log.exception`) khi cần.
10. **Test API async dùng `httpx.ASGITransport`** — `AsyncClient(app=...)` đã bị bỏ (httpx 0.28).
```python
async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
    r = await client.get("/health")
```
11. **Không SQLite trong test.** Test chạm DB dùng Postgres thật (pgvector) trên DB tạm; unit test `core/` không cần DB.
