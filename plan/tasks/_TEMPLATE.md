# <MÃ> · <tên ngắn, động từ đầu>

**Người:** <A|B|C|D> · **Ước tính:** <giờ, ≤ 4h — lớn hơn thì tách> · **Ngày:** <dd/mm> · **Skill:** `<skill chính>` [· **ĐƯỜNG GĂNG**]

## Mục tiêu
<1–2 câu: sau task này hệ thống làm được gì mà trước đó không làm được.>

## Vì sao
<Phục vụ bước nào trong plan/demo-mvp.md hoặc plan/demo-full.md, hay tiêu chí chấm nào của BTC.>

## File
- `<đường dẫn sẽ tạo/sửa>`

## Interfaces
<Chữ ký chính xác: tên, tham số có kiểu, kiểu trả. Không có → `—`.>
- Dùng: `<module.ham(tham_so: Kieu) -> KieuTra>` (`<file>`, từ <mã task | đã có>) · `<METHOD /api/v1/...>` → `<Schema>`
- Tạo ra: `<module.ham(tham_so: Kieu) -> KieuTra>` (`<file>`) — task khác dùng: <mã task | —>

## Đầu vào → đầu ra (dữ liệu demo `contracts/fixtures/demo_world.yaml`)
- <đầu vào cụ thể> → <kết quả mong đợi cụ thể, có số/ID>

## Các bước
1. <bước>

## Test phải viết
- `tests/<thư mục>/<file>.py::<tên_test>`

## Phụ thuộc / mock
- Chờ: <mã task hoặc —>
- Trong lúc chờ: <mock/fixture dùng tạm, hoặc —>

## Kiểm xong
Chạy `python3 ../team-ai-kit/plan/verify.py <MÃ>` từ gốc repo P-073. Chỉ tick `[x]` khi đạt.

```bash
$ APP_ENV=test OPENAI_API_KEY=test-key pytest tests/<...> -q
$ ruff check src/ tests/
```

Kiểm bằng tay (người review xác nhận):
- [ ] <điều máy không kiểm được, vd. giao diện dark mode nhìn rõ>

## Prompt cho AI agent
> Làm task <MÃ> theo file ../team-ai-kit/plan/tasks/<MÃ>.md và skill <skill>. Đọc AGENTS.md của thư mục sẽ sửa trước. Giữ nguyên chữ ký interface đã có. Viết test trước, chạy các lệnh ở mục 'Kiểm xong' cho tới khi đạt.
