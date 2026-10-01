---
name: property-based-testing
description: Viết, review và gỡ lỗi property test bằng hypothesis (Python) — chọn tính chất (roundtrip, idempotence, invariant, oracle…), thiết kế strategy, phân loại khi hypothesis thu nhỏ được phản ví dụ. Dùng khi viết/review test hypothesis cho hàm tất định trong src/core (validator, idempotency, token, warranty, range km/ngày), khi thêm @given vào test có sẵn, hoặc khi một property test vừa fail. KHÔNG dùng cho test API/DB/LLM, test e2e/Playwright, fuzz nhị phân hay benchmark; quy trình task chung theo start-task.
---

## Luật nhóm P-073 (ưu tiên hơn nội dung bên dưới)

- Thư viện: **chỉ `hypothesis`** đã có trong `requirements.txt`. Không thêm thư viện PBT/fuzz khác, không sửa `requirements.txt` vì skill này.
- Phạm vi: hàm thuần trong `src/core/` (Python thuần, không I/O). Test nằm trong `tests/test_core/test_<module>.py`; tên `test_<đơn vị>_<tình huống>_<kỳ vọng>`.
- Ngân sách CI: mặc định `@settings(max_examples=100, deadline=None)`; tối đa 200 cho hàm rất rẻ. Không để test hypothesis làm `pytest tests/` chậm quá vài giây mỗi file. Profile dài (1000+) chỉ chạy tay, không đưa vào CI.
- Không dùng thời gian thật trong property: truyền `now`/`clock` qua tham số; datetime luôn có timezone (`VN_TZ`). Không mạng, không DB, không LLM.
- Biên nghiệp vụ (đúng ngưỡng km, đúng ngày hết hạn, token hết hạn đúng giây) ghim bằng `@example(...)` lấy từ `contracts/fixtures/demo_world.yaml` hoặc tự tính tay — không tính kỳ vọng bằng chính hàm đang test.
- Gợi ý tính chất cho dự án:
  - validator: tham số hợp lệ → luôn đạt; đổi đúng 1 trường sang không hợp lệ → luôn bị từ chối với mã lỗi đúng.
  - idempotency key: cùng đầu vào → cùng key (tất định); khác bất kỳ tham số → khác key.
  - token xác nhận: `verify(sign(x)) is True`; sửa 1 byte / đổi params / quá hạn → `False`.
  - warranty: đơn điệu theo km và theo ngày (km tăng không làm "còn hạn" trở lại).
  - range/khoảng thời gian: kết quả nằm trong biên, không chồng lấn, bất biến khi đảo thứ tự đầu vào.
- Phản ví dụ thật → viết test tái hiện (fail) rồi sửa code theo `start-task`; không nới strategy để test xanh.

# Property-Based Testing

An example test asserts one point. A property asserts a rule over the whole input
domain and lets the generator hunt for the counterexample. That trade is worth making
when the code has an algebraic shape — an inverse, an invariant, an oracle — and not
otherwise. Code with no such shape gets example tests; saying so is a valid outcome.

Check first whether the shape is missing or merely buried. A calculation wrapped in I/O,
a string built by concatenation, an in-place mutation — each has a property and no seam
to assert it through. See [references/refactoring.md](references/refactoring.md) before
concluding there is nothing to assert.

## Property catalog

| Property | Formula | Where it applies |
|---|---|---|
| Roundtrip | `decode(encode(x)) == x` | Serialization, conversion pairs |
| Inverse | `f(g(x)) == x` | encrypt/decrypt, compress/decompress |
| Oracle | `new(x) == reference(x)` | Optimization, refactoring, reimplementation |
| Idempotence | `f(f(x)) == f(x)` | Normalization, formatting, sorting |
| Invariant | Holds before and after | Any transformation |
| Easy to verify | `is_sorted(sort(x))` | Complex algorithms with cheap checkers |
| Commutativity | `f(a, b) == f(b, a)` | Binary and set operations |
| Associativity | `f(f(a,b), c) == f(a, f(b,c))` | Combining operations |
| Identity | `f(x, e) == x` | Operations with a neutral element |

Strength ordering, weakest to strongest:
`no crash → type preservation → invariant → idempotence → roundtrip / oracle`.

Assert the strongest property the code supports. "No crash" alone rarely justifies a
property test — if that is all you can find, either a small rearrangement exposes something
stronger, or the honest report is that this code is a poor PBT candidate. Rule out the
first before settling for the second.

## The two ways a property test asserts nothing

- **Tautology.** `assert add(a, b) == a + b` restates the implementation; no bug they
  share can fail it. Pick a property that constrains the function without recomputing
  it. Note the exception: `f(x) == f(x)` is a genuine determinism property when `f`
  is not obviously pure — serializers over dicts or sets, hashing, anything reading
  the clock.
- **Vacuity.** `assume()` that filters out nearly every input passes without
  exercising anything, and self-contradictory `assume()` passes having run zero cases.
  Push constraints into the strategy so the generator produces valid inputs directly.

## Where to look next

Load the one that matches the task in front of you:

| Task | File |
|---|---|
| Writing new tests, designing strategies | [references/generating.md](references/generating.md) |
| The code has no property to assert yet | [references/refactoring.md](references/refactoring.md) |
| Reviewing existing property tests | [references/reviewing.md](references/reviewing.md) |
| A property test just failed | [references/interpreting-failures.md](references/interpreting-failures.md) |
| Hypothesis specifics (detecting usage, settings profiles) | [references/libraries.md](references/libraries.md) |

## Introducing PBT to a project that lacks it

Not applicable here: this project already uses Hypothesis (see team rules above). Write
the tests in it; do not propose another library.
