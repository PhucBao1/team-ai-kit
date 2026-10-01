# Audit mặc định không an toàn (insecure defaults)

Chuyển thể từ Trail of Bits `insecure-defaults` (commands/audit.md + references/*.md + *.json seeds), CC BY-SA 4.0 — xem `NOTICE.md`.
Bản gốc chạy bằng Workflow tool; bản này là checklist + lệnh `rg` chạy tay từ gốc repo P-073. Luật nhóm ưu tiên hơn file này.

## Cách làm
1. Chạy lệnh `rg` của từng nhóm dưới (phạm vi mặc định `src/ frontend/src/ Dockerfile* docker/ cloudbuild*.yaml .env.example`).
2. Mỗi kết quả là **ứng viên**, chưa phải phát hiện. Lần theo tới chỗ dùng: giá trị đó có đi tới quyết định bảo mật (ký token, xác thực, CORS, trả lỗi) không?
3. Chỉ báo khi có **cả hai**: (a) giá trị mặc định/hard-code chạy được và (b) đường lộ/khai thác. Ghi bằng chứng `file:dòng`.
4. Bỏ qua: `tests/`, fixture, tài liệu, giá trị chỉ làm cache key / correlation id.
5. Không có kết quả ≠ an toàn tuyệt đối — ghi "không thấy ứng viên với các mẫu trên".

```bash
RG() { rg -n -I -g '!tests/**' -g '!**/node_modules/**' -g '!eval/**' "$@"; }   # chạy 1 lần trong shell
```

## 1. Secret có fallback (fallback secrets)
**Báo khi:** env thiếu thì app vẫn chạy với secret biết trước, và secret đó dùng để ký/mã hoá/token.
Ví dụ xấu: `os.environ.get("CONFIRM_TOKEN_SECRET", "dev")`, `getenv("X") or "secret"`, trường Settings `confirm_token_secret: str = "change-me"`.
Đúng: trường không mặc định hoặc mặc định rỗng + validator chặn khi `APP_ENV=production` (CI BTC chỉ đặt `APP_ENV=test` nên phải cho test chạy được: dùng giá trị test trong `tests/conftest.py`, không trong `src/`).
```bash
RG "(getenv|environ\.get)\([^)]*,\s*['\"]" src/
RG "(getenv|environ\.get)\([^)]*\)\s*or\s*['\"]" src/
RG -i "(secret|token|key|salt|pepper)[a-z_]*\s*:\s*(str|SecretStr)\s*=\s*['\"][^'\"]+['\"]" src/config.py src/
```
Câu hỏi: nếu Secret Manager không gắn biến này, revision mới có khởi động không? Nếu có → phát hiện.

## 2. Credential mặc định
**Báo khi:** literal đăng nhập được thật (tài khoản seed nhân viên/admin, chuỗi kết nối DB có mật khẩu, API key trong code).
Bỏ qua: tài khoản seed tắt sẵn / buộc đổi; credential trong README/fixture test; `docker-compose` chỉ cho máy local (ghi chú, không báo).
```bash
RG -i "(password|passwd|pwd|secret|token)\s*[:=]\s*['\"][^'\"]{4,}['\"]" src/ frontend/src/
RG -i "(api[_-]?key|access[_-]?key|client[_-]?secret)\s*[:=]\s*['\"][^'\"]+['\"]" src/ frontend/src/
RG "(postgres(ql)?|redis)(\+[a-z]+)?://[^:@ ]+:[^@ ]+@" src/ Dockerfile* cloudbuild*.yaml
RG "VITE_[A-Z_]*(KEY|SECRET|TOKEN)" frontend/ .env.example
```

## 3. Fail-open (thiếu cấu hình = tắt bảo vệ)
**Báo khi:** trạng thái chưa cấu hình là trạng thái không an toàn. Đọc giá trị mặc định, không đọc tên cờ.
Ví dụ xấu: `REQUIRE_CONFIRM = getenv("REQUIRE_CONFIRM", "false")`; `if not settings.rate_limit_enabled: return`; `verify()` bắt mọi exception rồi `return True`; CORS lấy `"*"` khi thiếu `CORS_ORIGINS`.
```bash
RG -i "(auth|confirm|verify|csrf|rate_?limit|signature)[a-z_]*\s*[:=]\s*(False|['\"](false|0|off|no)['\"])" src/
RG "(verify|check_hostname)\s*=\s*False" src/
RG "(getenv|environ\.get)\([^)]*,\s*['\"]?(false|0|no|off|none|disabled)['\"]?\s*\)" src/
RG -A3 "except (Exception|\w+Error).*:" src/executor/ src/api/ | rg -n "return True|pass$"
```

## 4. Crypto yếu / so sánh không hằng thời gian
**Báo khi:** primitive yếu đứng ở vị trí bảo mật (ký token, sinh nonce, so chữ ký). Thuật toán một mình không phải phát hiện — `md5` cho cache key là ổn.
Đúng: `hmac.new(key, msg, hashlib.sha256)`, so bằng `hmac.compare_digest`, nonce bằng `secrets.token_urlsafe(16)`.
```bash
RG "(md5|sha1)\s*\(" src/
RG "hmac\.new\([^)]*(md5|sha1)" src/
RG -i "(token|nonce|secret|otp|key)[a-z_]*\s*=.*random\.(random|randint|choice)" src/
RG "(signature|sig|digest|token|mac)\w*\s*(==|!=)\s*\w+" src/executor/ src/core/ src/api/
```
Kết quả dòng cuối: mọi so sánh chữ ký/token bằng `==` → phát hiện (phải `hmac.compare_digest`).

## 5. Quyền quá rộng
**Báo khi:** cấp quyền cho bên không nên có — hard-code hoặc do fallback.
Ví dụ xấu: `allow_origins=["*"]` kèm `allow_credentials=True`; `allow_origin_regex=".*"`; Cloud Run worker/MCP deploy `--allow-unauthenticated`; service account mặc định Compute Engine; file key `0o666`.
Bỏ qua: API công khai có lý do ghi rõ; server dev bind loopback.
```bash
RG -i "(allow_origins|allow_origin_regex|Access-Control-Allow-Origin).{0,80}\*" src/
RG "allow_credentials\s*=\s*True" src/
RG -e "--allow-unauthenticated" -e "allUsers" Dockerfile* cloudbuild*.yaml Makefile scripts/ docker/ ../team-ai-kit/docs/ 2>/dev/null
RG "(^|[^0-9.])0o?(777|666)([^0-9]|$)" src/
```

## 6. Debug lộ ra ngoài
**Báo khi:** chi tiết nội bộ tới được response / cổng mở / log người ngoài đọc được: traceback hoặc `str(e)` trả cho client, `FastAPI(debug=True)`, `--reload` trong Dockerfile/CMD, `/docs` `/openapi.json` mở ở `APP_ENV=production`.
Bỏ qua: log chi tiết chỉ ở server (logger.exception) và trả lỗi generic cho client — đó là cách đúng.
```bash
RG "(traceback\.format_exc|format_exc\(|exc_info)" src/api/ src/main.py
RG "(detail|message|error)\s*=\s*(str\(e\)|f['\"].*\{e\})" src/api/ src/main.py
RG "debug\s*=\s*True|--reload|reload\s*=\s*True" src/ Dockerfile* Makefile
RG "docs_url|redoc_url|openapi_url" src/main.py
```
Kiểm `/docs`: nếu template BTC bật Swagger cho dev (AGENTS.md: `make run` có `/docs`) thì phải tắt theo `APP_ENV=production` (`docs_url=None if prod else "/docs"`) — không xoá hẳn.

## Mẫu ghi phát hiện
`ID-<nhóm>-<số> · mức · file:dòng · bằng chứng (đoạn code, đã che secret) · vì sao khai thác được · cách sửa tối thiểu · cần kiểm thêm gì nếu chưa chắc`.
