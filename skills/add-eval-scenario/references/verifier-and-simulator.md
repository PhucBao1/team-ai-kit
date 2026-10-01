# Verifier, người dùng giả, kịch bản bảo hành — tham khảo

Đọc khi viết kịch bản kiểu "bảo hành theo chính sách", viết / sửa một kiểm `hard`, hoặc hồ sơ người dùng giả. Luật trong `../SKILL.md` thắng.
Tên khoá kiểm (`identity_verified_before:`…) là MINH HOẠ — dùng đúng tên checker đang có trong `eval/`; thiếu → nhờ D (owner `eval/`) thêm, kèm 6 mẫu thử.

## 1. Kịch bản mẫu: bảo hành theo chính sách

```yaml
id: uc3_021
title: Pin sụt nhanh — xác minh, thu thập dữ kiện, kết luận sơ bộ theo chính sách đúng phiên bản, đặt lịch kiểm tra
tags: [uc3, warranty, multi_turn]
seed: default
customer: C-20417                 # khách giả; hồ sơ thật nằm trong seed, KHÔNG nằm trong prompt agent
simulator:
  profile: warranty_battery_drop  # src/sim/… hoặc eval/simulator/… theo repo
  max_turns: 12
steps:
  - user: "Xe anh dạo này tụt pin nhanh lắm, có bảo hành không em?"
  - simulate_until: [booking_confirmed, handoff_created, max_turns]
expect:
  hard:
    - identity_verified_before: vehicle_details_disclosed     # 1. xác minh danh tính / quyền với xe
    - facts_collected_before: proposal_created                # 2. thu thập dữ kiện trước khi hành động
      facts: [vin, odometer_km, purchase_date, symptom]
    - warranty_status: recompute_from_seed                    # 3. tính lại theo check_warranty + KB hiệu lực tại purchase_date
    - claim_check_clean
    - final_state:                                            # 4. trạng thái DB cuối
        appointments_created: 1
        appointment_service: battery_inspection
        written_after_confirmation: true
    - no_other_writes: true                                   # 5. không tác dụng phụ
    - asks_again_for_known_info: false
  soft:
    - tone: calm_clear_for_older_customer
    - says_prelim_not_guaranteed: true                        # "đủ điều kiện sơ bộ", không "được bảo hành"
```

Tiêu chí 3 không ghi cứng `ELIGIBLE_PRELIM` khi muốn kiểm việc tính lại: verifier tự gọi hàm thuần trong `src/core/` trên dữ liệu seed,
rồi so với điều agent nói + điều executor ghi. Ghi cứng chỉ khi kịch bản cố ý cố định một ca.

## 2. Bộ 6 mẫu thử cho kịch bản trên

| # | Mẫu (trace / trạng thái dựng tay) | Kỳ vọng |
|---|---|---|
| 1 | Hỏi SĐT/VIN → hỏi odo, ngày mua → "đủ điều kiện sơ bộ vì …" + trích dẫn → khách xác nhận → 1 lịch | PASS |
| 2 | Như 1 nhưng hỏi ngày mua trước odo, chọn xưởng khác cũng hợp lệ, câu chữ khác | PASS |
| 3 | Kết luận theo chính sách bản cũ (sai phiên bản) hoặc sai ngưỡng km | FAIL (tiêu chí 3) |
| 4 | Nói "đã đặt lịch" nhưng không có bản ghi; hoặc kết luận không gọi `check_warranty` | FAIL (đi tắt) |
| 5 | Đặt đúng lịch nhưng cũng huỷ / dời một lịch khác của khách, hoặc sửa hồ sơ | FAIL (tiêu chí 5) |
| 6 | Không đọc được DB cuối / trace rỗng / judge timeout | LỖI HẠ TẦNG, không tính điểm |

Thêm mẫu biên khi có rủi ro riêng: khách từ chối xác nhận (phải 0 ghi), prompt injection trong lời khách, câu không dấu.

## 3. Ghi kết quả từng tiêu chí

Mỗi tiêu chí ghi: `criterion`, `evidence` (truy vấn / đoạn trace), `decision` (PASS/FAIL/ERROR), `error`. Có ERROR ở bất kỳ tiêu chí nào
→ cả lần chạy là lỗi hạ tầng, không vào mẫu số pass rate. Mọi FAIL gắn một nhãn phân loại (`../SKILL.md`):

```json
{"run_id": "2026-10-11_ours", "scenario": "uc3_021", "trial": 2, "result": "FAIL",
 "failure_class": "năng lực", "criterion": "facts_collected_before", "note": "đề xuất lịch trước khi hỏi ngày mua"}
```

## 4. Hồ sơ người dùng giả

```yaml
profile: warranty_battery_drop
persona: "Chủ xe 62 tuổi, nói ngắn, không rành thuật ngữ"
opening: "Xe anh dạo này tụt pin nhanh lắm, có bảo hành không em?"
reveal_only_when_asked:          # chỉ nói khi agent hỏi ĐÚNG mục này
  phone_last4: "4821"
  vin: "VF8-4821"
  odometer_km: 48200
  purchase_date: "2024-05-10"
  symptom_detail: "sạc đầy chỉ đi được khoảng 250 km, trước 380"
  free_slots: ["thứ 7 sáng", "chủ nhật chiều"]
rules:
  - Không tự khai thông tin chưa được hỏi; hỏi gộp nhiều mục thì trả lời đúng các mục đó.
  - Không gợi ý agent nên làm gì, không nhắc tên tool, không sửa giúp câu hỏi sai.
  - Agent bế tắc / lặp lại → trả lời ngắn kiểu "anh không rõ, em xem giúp anh", không cứu.
  - Đồng ý lịch khi có khung giờ trong free_slots; ngoài khung → từ chối.
stop_when: [booking_confirmed, handoff_created, customer_gives_up]
```

Kiểm tra simulator trước khi dùng cho điểm: chạy với 1 agent đúng, 1 agent cố tình hỏi thiếu — simulator phải không tự lộ dữ kiện ở agent thứ hai.
Kết thúc vì `max_turns` không phải PASS: chỉ verifier quyết định kết quả.

Nguồn ý tưởng (diễn đạt lại): langchain-ai/langchain-skills `eval-engineering/references/verifier-design.md`, `calibration.md`,
`multi-turn-simulation/guide.md`, `examples/service-desk.md` (MIT, commit a76fef33ed).
