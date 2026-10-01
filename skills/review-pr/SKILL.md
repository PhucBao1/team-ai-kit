---
name: review-pr
description: Review một diff/PR theo luật của repo — ranh giới kiến trúc, hợp đồng, an toàn dữ liệu, test, quy ước code — và trả danh sách phát hiện có mức độ; kèm cách xử lý góp ý review nhận được. Dùng khi tự review trước khi mở PR, khi review PR của người khác, khi nhận góp ý review cần sửa, hoặc khi task nói "review", "kiểm tra code", "soát PR".
---

# Review PR

Lấy diff: `git diff origin/develop...HEAD` (hoặc PR được chỉ định). Chỉ nhận xét dòng trong diff và hệ quả trực tiếp.

## Cách chạy
- Review bằng **sub-agent MỚI**, chỉ đưa: card `../team-ai-kit/plan/tasks/<mã>.md` + diff (+ file này). KHÔNG đưa lịch sử phiên làm việc — reviewer phải nhìn sản phẩm, không nhìn lý lẽ của người viết.
- Reviewer **chỉ đọc**: không sửa file, không commit, không `checkout`/`reset`/`stash` (không đổi HEAD). Cần xem revision khác → `git show <sha>:<file>` hoặc worktree tạm ngoài repo.
- Không có sub-agent → tự review nhưng đọc lại card trước, coi diff như code người khác viết.

## Soát theo thứ tự (dừng ở mục nghiêm trọng đầu tiên nếu thấy BLOCKER)
1. **Ranh giới (BLOCKER):** `src/agents/` import `src.tools` / nhắc tool ghi? `src/core/` có I/O, LLM, env? ghi hệ thống ngoài `src/executor/`? sửa file của BTC (`docs/guide/`, `.github/`, hook log) hoặc commit file team-ai-kit?
   thao tác ghi thiếu confirmation token / validator / idempotency key?
2. **Không bịa (BLOCKER):** chính sách, giá, ngày, km, trạng thái có lấy từ tool/KB không, hay nằm cứng trong prompt/code?
   văn bản gửi khách có khẳng định "được bảo hành"?
3. **Hợp đồng:** đổi chữ ký tool/API/sự kiện mà không cập nhật `contracts/` + ADR? Frontend kiểu viết tay trùng?
4. **Dữ liệu & bảo mật:** PII trong log/test/seed? secret? tên model hard-code? input của khách đi thẳng vào tham số tool?
5. **Độ tin cậy:** gọi mạng/LLM không timeout? vòng lặp không giới hạn? retry lỗi không retryable? blocking I/O trong async?
6. **Test:** hành vi mới có test trong `tests/`? bug fix có test tái hiện? coverage tụt? eval golden / kỳ vọng hard bị sửa? test mẫu BTC (`/health`, `/api/v1/chat`, `/api/v1/status`) còn xanh?
   test assert vào mock, hoặc kỳ vọng tính bằng chính hàm đang test? thiếu test đường lỗi?
7. **Quy ước (chấm Code Quality):** type hints mọi hàm, docstring public, hàm ≤ 30 dòng / ≤ 3 tham số, không `print`, không `except:` trần, timezone, tên trường có đơn vị (`../team-ai-kit/docs/conventions.md`).

### Cờ đỏ của diff (soát thêm khi diff XOÁ hoặc ĐỔI code có sẵn)
- Xoá validation / kiểm quyền / kiểm token mà không có cái thay thế → BLOCKER cho tới khi chứng minh được.
- Đụng code bảo mật (executor, validator, HMAC, auth, idempotency) → `git blame` / `git log -S "<đoạn bị xoá>"` xem dòng đó được thêm vì lỗi gì; xoá lại = có thể tái phát lỗi cũ.
- Đổi chữ ký / hành vi hàm dùng chung → đếm số chỗ gọi (`grep -rn "<tên_hàm>(" src/ tests/`) để ước phạm vi ảnh hưởng; nhiều chỗ gọi + rủi ro cao → đòi test cho các chỗ gọi chính.

### Săn lỗi im lặng
- `except Exception` / `except (A, B, ...)` quá rộng; bắt rồi `pass` hoặc `return None`.
- Fallback giấu lỗi: lỗi tool → trả giá trị mặc định như thể thành công; khách không biết hành động thất bại.
- Mock, dữ liệu giả, `TODO`, key `test-key`, giá trị cứng lọt vào code chạy thật (ngoài `tests/`, `src/sim/`).
- Lỗi bị log rồi nuốt (log xong không raise / không trả `ToolError` / không chuyển người).

### Tham khảo theo loại diff (đọc khi diff có loại code đó; luật nhóm thắng tài liệu tham khảo)
- Python: `references/python-checklist.md`. Frontend (`frontend/`): `references/frontend-checklist.md`.
- PR đụng `src/executor/`, token/HMAC, `src/api/`, `src/config.py` hoặc secret → chạy thêm skill `security-review`.

## Kiểm lại phát hiện trước khi báo
- Mỗi phát hiện được kiểm lại bằng **một lượt riêng**: mở lại đúng dòng + đường dữ liệu tới nó, cố BÁC BỎ (có validate ở tầng trên? có test bao? đúng là trong diff?). Không bác được → giữ; bác được → chuyển sang "Đã cân nhắc nhưng bỏ qua".
- Bỏ qua (không báo): lỗi có sẵn từ trước diff; thứ ruff/mypy/CI tự bắt; phỏng đoán chỉ xảy ra với input cụ thể mà không có bằng chứng input đó tới được; ý thích phong cách không có trong conventions.
- Mức độ theo thực tế, không thổi phồng: không phải gì cũng BLOCKER.

## Đầu ra
Bảng: `mức (BLOCKER | NÊN SỬA | GỢI Ý) · file:dòng · vấn đề · cách sửa`. Mỗi phát hiện phải chỉ được dòng cụ thể.
Không có BLOCKER/NÊN SỬA → ghi rõ "Không thấy vấn đề ở các mục 1–7" kèm những gì đã kiểm.
**Đã cân nhắc nhưng bỏ qua:** mỗi mục 1 dòng `điều đã xét · lý do bỏ` (rỗng → ghi "Không có").
**Kết luận:** `Merge được? Có / Không / Sau khi sửa` + 1–2 câu lý do.
Không tự sửa code khi được yêu cầu review — trừ khi được bảo sửa.

## Nhận review (khi mình là người viết PR)
- Đọc hết góp ý trước. Có mục chưa hiểu → **hỏi hết các mục chưa rõ TRƯỚC khi sửa bất kỳ mục nào** (các mục thường liên quan nhau).
- Kiểm từng góp ý với code thật: đúng với repo này không? phá gì không? có lý do cho cách làm hiện tại không (card, ADR)? Sai → phản biện bằng lý lẽ kỹ thuật, dẫn code/test.
- Góp ý kiểu "làm cho chuẩn / đầy đủ" → `grep` xem có ai gọi; không ai dùng → đề xuất bỏ (YAGNI) thay vì làm thêm.
- Sửa theo thứ tự: BLOCKER → sửa đơn giản → sửa phức tạp; chạy test sau mỗi mục.
- Trả lời ngay trong thread của góp ý đó: "Đã sửa: <gì> ở <file:dòng>" hoặc lý do không sửa. Không khen xã giao ("Ý hay quá!", "Cảm ơn…") — chỉ nói đã làm gì.
- Góp ý trái với card / quyết định của người sở hữu module → dừng, hỏi người.

---
Ý tưởng tham khảo (diễn đạt lại): obra/superpowers (MIT) — requesting-code-review, receiving-code-review; trailofbits/skills (CC BY-SA 4.0) — differential-review, fp-check (chỉ rút ý, không chép).
