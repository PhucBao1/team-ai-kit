# 17 · Lõi tất định & Executor — Bốn module quyết định mọi thứ quan trọng — không có LLM bên trong

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

```python
# core/warranty.py
def warranty_precheck(v: Vehicle, policies: list[Policy], maint: list[Maint], now: date) -> WarrantyResult:
    p = pick_policy(policies, v.model, v.usage_type, on=now)          # theo phiên bản + ngày hiệu lực
    if p is None:
        return WarrantyResult("UNKNOWN", "chưa có chính sách cho dòng xe này", None)
    age_years = (now - v.purchase_date).days / 365.25
    if age_years > p.years or v.odometer_km > p.km:
        return WarrantyResult("EXPIRED", f"vượt {p.years} năm / {p.km:,} km", p.version)
    if missed_services(v, maint, now) > 0:                            # 1.000 km/1 tháng, rồi 5.000 km/6 tháng
        return WarrantyResult("NEEDS_WORKSHOP", "có kỳ bảo dưỡng bị lỡ", p.version)
    return WarrantyResult("ELIGIBLE_PRELIM", "trong thời hạn, bảo dưỡng đúng lịch", p.version)

# core/range.py — xưởng có đi tới được với pin hiện tại không
SAFETY = 1.3
def reachable(v: Vehicle, ws: Workshop, kwh_per_km: float, battery_kwh: float) -> bool:
    need_kwh = road_km(v, ws) * kwh_per_km * SAFETY
    return v.soc_pct / 100 * battery_kwh >= need_kwh

# core/validator.py — chạy trước mọi tool ghi (mức 2)
CHECKS = [customer_verified, owner_or_can_book, part_matches_vin,
          technician_certified, part_reserved, slot_locked, confirmation_valid]
def validate(action: WriteAction, ctx: Ctx) -> list[str]:
    return [c.__name__ for c in CHECKS if not c(action, ctx)]         # rỗng = được ghi

# core/claim_check.py — chặn câu trả lời có con số không có nguồn
PATTERNS = [DATE, TIME, KM, MONEY, PERCENT, CODE_RO, CODE_APPT, PLATE]
def claim_check(reply: str, evidence: list[str]) -> list[str]:
    found = extract(reply, PATTERNS)
    corpus = normalize(" ".join(evidence))                             # kết quả tool + đoạn KB của lượt này
    return [f for f in found if normalize(f) not in corpus]           # rỗng = an toàn để gửi
```

### Confirmation token

Khi agent đưa phương án, API tạo token ký HMAC chứa {option_id, params_hash, customer_id, exp=10 phút} gắn vào nút Xác nhận. Chỉ khi **khách bấm**, frontend gửi token cho tool ghi. Đổi bất kỳ tham số nào → hash khác → token vô hiệu. LLM không bao giờ thấy token.

### Unit test bắt buộc (ngày 28/9)

- 3 xe mẫu → đúng ELIGIBLE_PRELIM / EXPIRED / NEEDS_WORKSHOP
- Pin 8%, xưởng 35 km → không reachable
- Thiếu token / token hết hạn / đổi giờ → validator từ chối
- "Lịch 10:00" khi evidence chỉ có 09:00 → claim_check bắt lỗi
