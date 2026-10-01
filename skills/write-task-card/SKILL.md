---
name: write-task-card
description: Viết task card chi tiết (plan/tasks/<mã>.md) cho task mới phát sinh, hoặc soát card nháp tuần 2–3 — mục tiêu, file, đầu vào→đầu ra theo fixture, test phải viết, lệnh kiểm cho verify.py và prompt cho AI agent. Dùng khi lập kế hoạch tuần sau (tối Chủ nhật), hoặc khi một dòng task trong plan còn chung chung.
---

# Viết task card

## Khi nào
- Tối Chủ nhật: mỗi người soát card nháp tuần sau của mình (đã có sẵn trong `plan/tasks/`), sửa file / lệnh kiểm cho khớp code thật; người cùng cặp review (A⇄D, B⇄C). Xoá dòng "Bản nháp" khi đã soát.
- Task mới phát sinh hoặc task > 4h → tách và viết card trước khi code.

## Cách viết
1. Copy `../team-ai-kit/plan/tasks/_TEMPLATE.md` → `plan/tasks/<MÃ>.md` (mã theo dòng trong `plan/<người>.md`, vd. `A2.03`).
2. Đọc dòng task + mục spec liên quan (`../team-ai-kit/docs/spec/`) + chữ ký interface có sẵn trong `src/` (không đổi chữ ký nếu không có ADR).
3. **Interfaces**: `Dùng:` chữ ký CHÍNH XÁC (tên, tham số, kiểu trả) của hàm / endpoint / tool task này lấy vào, kèm file và mã task tạo ra nó · `Tạo ra:` chữ ký task này xuất ra cho task khác dùng. Agent làm task chỉ thấy card của mình — khối này là cách nó biết tên và kiểu của task bên cạnh. Không có → ghi `—`.
4. **Đầu vào → đầu ra** phải dùng dữ liệu thật trong `contracts/fixtures/demo_world.yaml` (VIN, mã khách, xưởng, số km…). Thiếu dữ liệu → thêm vào fixture trong cùng PR và ghi rõ.
5. **Test phải viết**: tên test cụ thể `tests/.../file.py::test_<đơn vị>_<tình huống>_<kỳ vọng>`, mỗi test một hành vi, có ít nhất 1 test đường lỗi. Có luật tất định → thêm 1 test hypothesis.
6. **Kiểm xong**: mỗi dòng `$ ` là một lệnh phải thoát 0, chạy được từ gốc repo, không cần mạng/key thật (env mặc định `APP_ENV=test OPENAI_API_KEY=test-key`). Dòng cuối luôn `$ ruff check src/ tests/`. Việc máy không kiểm được → `- [ ]` ở "Kiểm bằng tay".
7. Liên kết mã task trong `plan/<người>.md`: `**[A2.05](tasks/A2.05.md)**`.

**Mỗi dòng phải quyết một điều cụ thể.** Cấm dòng "chưa quyết": `TBD`, `…`, "xử lý các trường hợp biên", "thêm validate phù hợp", "viết test cho phần trên", tên hàm/kiểu không task nào định nghĩa.
Thay bằng điều đã quyết: "odometer = 100 000 km → `expired`", "VIN không có trong fixture → `ToolError(code="VEHICLE_NOT_FOUND")`". Chưa quyết được → hỏi người trước, không để agent tự đoán.

## Tự kiểm card
- `python3 ../team-ai-kit/plan/check_conflicts.py` → **0 xung đột**: file trong mục File không được trùng với file người khác sửa cùng tuần. Trùng → chuyển phần đó cho người sở hữu file (xem bảng "Được sửa" trong PLAN.md §2) và ghi "Chờ".
- Mục File chỉ ghi file mình SỬA; file chỉ đọc thì ghi ở Các bước, không để trong dấu `.
- `python3 ../team-ai-kit/plan/verify.py <MÃ>` phải **CHƯA ĐẠT** trước khi làm (nếu đạt ngay → lệnh kiểm quá yếu, sửa lại).
- Tìm `TBD`, `…`, "phù hợp", "các trường hợp" trong card → còn thì viết lại thành điều cụ thể. Mỗi tên trong `Dùng:` phải có thật trong `src/` hoặc ở `Tạo ra:` của card khác.
- Card đọc riêng vẫn hiểu được; ước tính ≤ 4h; có "Vì sao" trỏ tới bước demo hoặc tiêu chí chấm.
- Không đưa thông tin khách thật, key, hay nội dung team-ai-kit vào code P-073.

---
Ý tưởng tham khảo (diễn đạt lại): obra/superpowers (MIT) — writing-plans (khối Interfaces, cấm dòng chưa quyết).
