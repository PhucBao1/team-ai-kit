# Sharp edges — câu hỏi cho thiết kế token / validator / config (Python)

Rút ý từ Trail of Bits `sharp-edges` (SKILL.md, references/config-patterns.md, auth-patterns.md, lang-python.md), diễn đạt lại và áp vào P-073.
CC BY-SA 4.0 — xem `NOTICE.md`. Luật nhóm ưu tiên hơn file này.

Nguyên tắc: cách dùng an toàn phải là cách **dễ nhất**. Nếu người gọi phải nhớ một luật đặc biệt để không bị lỗi, API đó đã sai thiết kế.
Lý do bị loại: "đã ghi trong docstring", "không ai truyền 0 đâu", "chỉ là tuỳ chọn cấu hình" — cấu hình cũng là code, sẽ lên production.

## Giá trị 0 / rỗng / None
- `ttl_min=0` nghĩa là gì: hết hạn ngay, hay không bao giờ hết hạn? Âm thì sao? → ràng buộc `Field(ge=1, le=60)` (Settings đã có) VÀ kiểm lại trong hàm ký/verify (core nhận tham số, không tin caller).
- Key HMAC rỗng `""`: `hmac.new(b"", …)` vẫn chạy và ra chữ ký hợp lệ ai cũng tính được. Template có `confirm_token_secret: str = ""` → hàm ký phải từ chối key rỗng/ngắn (< 32 byte); production phải fail khi khởi động.
- `None` nghĩa là "bỏ qua kiểm"? vd. `allowed_workshops=None` → cho mọi xưởng? Dùng giá trị tường minh (`ALL` có tên) hoặc bắt buộc truyền.
- Chuỗi rỗng so với chuỗi rỗng: `"" == ""` → token rỗng khớp chữ ký rỗng. Kiểm độ dài/định dạng trước khi so.

## Kết quả verify
- `verify()` trả `False` im lặng cho mọi lỗi (hết hạn, sai chữ ký, sai params, đã dùng) → không biết vì sao bị từ chối, và dễ bị đảo logic. Trả kết quả có cấu trúc (`Literal["ok","expired","bad_signature","params_mismatch","replayed"]`) hoặc model Pydantic; caller phải xử lý từng nhánh.
- `try: … except Exception: return True` (fail-open) → cấm. Lỗi giải mã/parse = từ chối.
- Ngược lại: đừng raise lỗi chung cho kết quả nghiệp vụ dự kiến (conventions §4).

## So sánh
- Chữ ký/token so bằng `==` → rò thời gian; dùng `hmac.compare_digest` (hai vế cùng kiểu `bytes` hoặc `str` ASCII).
- `is` thay cho `==` với chuỗi/số → đúng ngẫu nhiên do interning; cấm trong code kiểm.
- So tiền/km bằng float `==` → dùng `int` (đồng) hoặc ngưỡng rõ ràng; km so `>=`/`>` theo đúng câu chữ chính sách (đúng ngưỡng là còn hay hết?) — ghim bằng `@example`.

## Chuỗi thay vì kiểu
- Action/trạng thái/vai trò là chuỗi tự do → gõ sai `"book_apointment"` vẫn qua; quyền kiểu `"admin" in role_str` khớp nhầm `"readonly_admin_viewer"`. Dùng `StrEnum`/`Literal` (conventions §3).
- Params hash từ `str(dict)` → thứ tự khoá/định dạng khác nhau ra hash khác/giống nhầm. Chuẩn hoá: `json.dumps(params, sort_keys=True, separators=(",", ":"), ensure_ascii=False)` sau khi qua Pydantic.
- Thời gian dạng chuỗi không timezone → so sai múi giờ; luôn `datetime` có tz.

## Thuật toán / tham số do bên ngoài chọn
- Không cho token mang trường `alg`/thuật toán; cố định SHA-256 trong code.
- Không cho LLM/khách chọn tham số bảo mật (ttl, phạm vi quyền, id khách) — xem `llm-app-checks.md` mục 2.

## Cấu hình
- Cờ tắt bảo vệ (`skip_confirm`, `disable_rate_limit`, `verify_ssl=False`) không nên tồn tại; nếu cần cho test → inject qua tham số/fixture, không qua env ở `src/`.
- Hai thiết lập mâu thuẫn (vd. `allow_origins=["*"]` + `allow_credentials=True`) → Settings validator từ chối khi khởi động.
- Thứ tự ưu tiên env > `.env` > mặc định phải rõ; secret không bao giờ có mặc định "dùng được".
- Giá trị ma thuật (`-1` = không giới hạn, `0` = tắt) cho `max_instances`, `rate_limit`, `max_tokens` → gây DoS; dùng `None` tường minh + validator, hoặc cấm.

## Python nói chung
- Đối số mặc định là list/dict dùng chung giữa các lần gọi (`def f(x, seen=[])`) → rò trạng thái giữa phiên khách.
- `except:` trần / nuốt lỗi; biến vòng lặp bị dùng lại sau vòng; closure trễ trong vòng lặp tạo callback.
- `str.format` với chuỗi định dạng do người dùng đưa → đọc được thuộc tính object (`{0.__class__}`); không dùng input khách làm format string (kể cả template prompt).
- Giải nén / duyệt cấu trúc người dùng gửi không giới hạn kích thước → DoS; giới hạn ở Pydantic (`max_length`).
- `subprocess(..., shell=True)`, `eval`, `pickle.loads` với dữ liệu ngoài → cấm.

## Đặt câu hỏi khi review một hàm token/validator/config
1. Giá trị 0, âm, rỗng, None, rất lớn của từng tham số làm gì?
2. Thiếu cấu hình thì hệ thống an toàn hay mở?
3. Mọi đường lỗi có dẫn tới "từ chối" không?
4. So sánh có hằng thời gian, đúng kiểu, đúng ngưỡng không?
5. Ai chọn được tham số bảo mật — code, cấu hình, khách, hay LLM?
