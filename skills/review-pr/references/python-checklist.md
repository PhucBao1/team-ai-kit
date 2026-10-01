# Checklist review Python (P-073)

Đọc khi diff có file `.py`. Luật nhóm (`rules/AGENTS.md`, `docs/conventions.md`) luôn thắng file này.
Mỗi dòng: điều cần soát → cách đúng. Thấy vi phạm → ghi phát hiện kèm `file:dòng`.

## DB & ranh giới dữ liệu
- [ ] Không gọi LLM / HTTP / MCP bên trong transaction DB (giữ khoá + kết nối lâu, rollback nửa vời). Gọi ra ngoài trước, mở transaction ngắn sau.
- [ ] Không trả model SQLModel `table=True` thẳng ra API / tool / LLM (lộ cột nội bộ, lazy-load ngoài session). Chuyển sang schema Pydantic: `Out.model_validate(obj, from_attributes=True)`.
- [ ] Input từ khách / LLM được validate bằng Pydantic ở biên trước khi vào tool hay `core/`.
- [ ] Batch nhiều phần tử: một phần tử lỗi không làm mất kết quả các phần tử khác — trả về cả danh sách thành công lẫn thất bại.
- [ ] Tài nguyên (session DB, client HTTP, file) mở bằng `with` / `async with`, không tự `close()` tay.

## Retry & timeout
- [ ] Retry đúng **một tầng**. Bọc LLM bằng tenacity → `ChatOpenAI(max_retries=0)` (SDK mặc định đã tự retry → nhân số lần gọi).
- [ ] Mẫu tenacity: `wait=wait_exponential_jitter(...)`, `stop=stop_after_attempt(3) | stop_after_delay(<giây>)`, `retry=retry_if_exception_type(<lỗi tạm thời>)`, `before_sleep=` log cảnh báo.
- [ ] Chỉ retry lỗi tạm thời (timeout, 429, 5xx, `ToolError.retryable=True`); không retry 4xx / lỗi validate.
- [ ] Mọi lời gọi mạng / LLM / MCP có timeout (`asyncio.timeout(...)`); vòng lặp gọi LLM có max vòng + ngân sách token.
- [ ] Logic retry/timeout gom ở một chỗ (decorator / `services/`), không rải `try/sleep` khắp nơi.

## Async
- [ ] Không blocking call trong `async def`: `time.sleep`, `requests`, đọc file lớn, SDK sync, PhoBERT / model local → `await asyncio.to_thread(fn, ...)`.
- [ ] Fan-out gọi LLM song song có giới hạn: `asyncio.Semaphore(n)` bao quanh lời gọi.
- [ ] Không nuốt `asyncio.CancelledError`: nếu bắt (kể cả qua `except BaseException`) thì dọn dẹp rồi `raise` lại.
- [ ] Không quên `await` (coroutine chưa await = không chạy). Task tạo ra được giữ tham chiếu / dùng `TaskGroup`.

## Kiểu & phiên bản (Python 3.11)
- [ ] Không dùng cú pháp 3.12: `class X[T]:`, `def f[T](...)`, `type X = ...`. Dùng `TypeVar`, `Generic[T]`, `TypeAlias`.
- [ ] Type hints mọi hàm; collection có tham số kiểu (`list[str]`, `dict[str, int]`), không `list` trần.
- [ ] Pydantic v2: không `.dict()`, `.json()`, `.from_orm()`, `parse_obj`, `class Config:`. Dùng `model_dump()`, `model_dump_json()`, `model_validate(..., from_attributes=True)`, `model_config = ConfigDict(...)`.
- [ ] `datetime` luôn có timezone (`datetime.now(tz=VN_TZ)`, lưu DB UTC). Cấm `datetime.utcnow()` và `datetime.now()` không tz.
- [ ] Trạng thái dùng `Literal` / `StrEnum`; tiền `int` đồng; tên trường có đơn vị (`odometer_km`).

## Lỗi
- [ ] Không `except:` trần, không `except Exception: pass`. Bắt lỗi cụ thể.
- [ ] Đổi lỗi thì giữ nguyên nhân: `raise HTTPException(...) from e`, `raise DomainError(...) from e`.
- [ ] Giữa module trả lỗi có cấu trúc (`ToolError(code, message, retryable)`), `code` có trong `contracts/tools.yaml`.
- [ ] Không có nhánh "lỗi thì trả giá trị mặc định" làm khách tưởng đã thành công.

## Log & dữ liệu nhạy cảm
- [ ] Log lỗi bằng `error_type=type(e).__name__` (+ mã lỗi), KHÔNG `str(e)` / `repr(e)` — thông điệp có thể chứa lời khách, SĐT, biển số.
- [ ] structlog, tên sự kiện `a.b`, dữ liệu là field; có `trace_id`, `journey_id` khi có. Không `print`.
- [ ] Không log tên, SĐT, biển số, nội dung tin nhắn; log id.

## Bảo mật & cấu hình
- [ ] So HMAC / token bằng `hmac.compare_digest(a, b)`, không `==`.
- [ ] Cấm giá trị mặc định nguy hiểm cho secret: `os.environ.get("SECRET", "dev")`, `secret: str = "changeme"`. Secret thiếu ở production → lỗi khi khởi động.
- [ ] Không đọc env rải rác: mọi cấu hình qua `get_settings()`; `src/core/` không đọc env.
- [ ] Tên model chỉ trong `src/config.py`; LLM lấy qua `get_llm(kind)`.

## Chất lượng (chấm Code Quality)
- [ ] Hàm ≤ 30 dòng, ≤ 3 tham số (hơn → gom vào model Pydantic).
- [ ] Docstring Google style cho hàm public: mô tả 1 dòng + `Args:`, `Returns:`, `Raises:` (khi có raise).
- [ ] Logic nghiệp vụ không trộn với I/O: phần tính toán ở `src/core/` (thuần), I/O ở adapter.
- [ ] Test có đường lỗi + biên, không chỉ đường đẹp; mock chỉ ở tầng ngoài.

---
Ý tưởng tham khảo (diễn đạt lại, không chép nguyên văn): wshobson/agents (MIT) — plugin python-development,
skills python-anti-patterns, python-resilience, async-python-patterns, python-error-handling, python-observability
(commit 156b7a5e7a). Phần còn lại là quy ước riêng của đội P-073.
