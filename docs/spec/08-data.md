# 08 · Mô hình dữ liệu — Schema tối thiểu cho UC1, đủ để mở rộng

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

```text
-- Khách, xe, quyền
customers(id, name, phone_masked, preferred_channel, preferred_hours, consent_vehicle_data, consent_marketing)
vehicles(vin, model, purchase_date, usage_type -- personal | commercial, owner_id, sw_version, odometer_km, soc_pct, lat, lng)
vehicle_drivers(vin, customer_id, role -- owner | driver, can_book, can_see_billing)

-- Xưởng, kỹ thuật viên, lịch
workshops(id, name, lat, lng, open_hours, has_hv_bay)
technicians(id, workshop_id, name, hv_certified)
slots(id, workshop_id, start_at, end_at, status -- free | held | booked, held_until)
appointments(id, vin, workshop_id, slot_id, reason, status -- confirmed | cancelled | done, created_via)

-- Linh kiện
parts(code, name, fits_models)
inventory(workshop_id, part_code, qty, eta_at)
reservations(id, part_code, workshop_id, appointment_id, status -- held | cancelled | consumed, reason)

-- Lệnh sửa chữa, bảo dưỡng, bảo hành
repair_orders(id, vin, appointment_id, state -- 9 trạng thái của vòng đời RO, dtc_codes, closed_at)
maintenance_history(vin, done_at, odometer_km, workshop_id)
warranty_policies(model, usage_type, years, km, version, effective_from, source_url)

-- Knowledge
dtc_codes(code, system, severity -- INFO | WARNING | CRITICAL, remote_fixable, self_help, likely_parts, kb_ref)
kb_docs(id, title, body, version, effective_from, source_url, accessed_at)

-- Trạng thái hành trình (Journey State Graph phiên bản MVP)
journeys(id, vin, customer_id, type, status, opened_at, verify_until)
promises(id, journey_id, made_by, text, due_at, status -- open | kept | rescheduled | broken)
events(id, type, payload_json, occurred_at, processed_at)
handoffs(id, journey_id, card_json, assignee, created_at, accepted_at)
audit_log(id, journey_id, actor -- agent | human | system, action, input_json, output_json, trace_id, at)
```

### Dữ liệu seed cho MVP (cố định, lặp lại được)

| Thực thể | Số lượng | Phải có để demo |
| --- | --- | --- |
| Khách / xe | 20 / 24 | Anh Minh — VF 8, cá nhân, mua 14/03/2024, 38.420 km, pin 42%, bảo dưỡng đủ. 1 xe VF 3 kinh doanh vận tải 3,5 năm. 1 xe VF 6 lỡ 2 kỳ bảo dưỡng. 1 xe có người lái phụ |
| Xưởng | 3 | Long Biên (4 km, có linh kiện ban đầu), Gia Lâm (6 km, có linh kiện + kỹ thuật viên pin cao áp), một xưởng xa 35 km (để test ràng buộc quãng đường) |
| Mã lỗi | 8 | 1 CRITICAL, 5 WARNING (1 sửa được từ xa), 2 INFO. Mã làm mát pin: WARNING, không sửa từ xa, linh kiện dự kiến "bơm làm mát pin" |
| Chính sách bảo hành | 3 dòng | VF 8/9 cá nhân 10 năm/200.000 km; VF 3/5/6/7 cá nhân 8 năm/160.000 km; xe kinh doanh vận tải 3 năm/100.000 km (theo chính sách công khai, ghi URL) |
| Slot | ~60 | Thứ Bảy 3/10 09:00 và 14:00 trống ở Long Biên và Gia Lâm |

Seed nằm trong sim/seed.py; lệnh make reset đưa thế giới về trạng thái đầu trong 1 giây — bắt buộc cho demo và eval.

### Tầng phân tích: lakehouse trên GCP — tách khỏi DB vận hành

Postgres (vận hành) chỉ giữ trạng thái đang chạy: lịch, hành trình, audit. Mọi thứ để **phân tích, đánh giá, huấn luyện** — sự kiện thô, telematics, transcript, trace, kết quả eval — đi sang lakehouse, để truy vấn nặng không làm chậm agent và dữ liệu thô giữ lâu với chi phí thấp. Trên GCP: **Lakehouse** (tên mới của BigLake từ 20/4/2026) — bảng Apache Iceberg lưu trên Cloud Storage, truy vấn bằng BigQuery hoặc Spark trên cùng một bản dữ liệu.

```text
Pub/Sub ──(subscription ghi thẳng Cloud Storage)──┐
Postgres ──Datastream (CDC)──────────────────────┤
Langfuse / OTel trace ─export──────────────────── ┤
                                                 ▼
 BRONZE  dữ liệu thô, bất biến (Iceberg trên GCS) — sự kiện, telematics, transcript, trace
    │  làm sạch · chuẩn hoá schema · thay định danh bằng token (Sensitive Data Protection)
    ▼
 SILVER  bảng chuẩn: journey, job, contact, alert, promise — một dòng một sự thật
    │  tổng hợp · join · tính metric
    ▼
 GOLD    mart metric CX (Contacts per Job, Pre-Chase Recovery, ACRC) · feature cho model
         · dataset eval / huấn luyện có phiên bản (§27) · VoC
    ▼
 Looker dashboard · notebook data science (§28) · huấn luyện PhoBERT (§18)
 Quản trị: Dataplex (catalog, lineage, chất lượng) · quyền theo cột cho dữ liệu nhạy cảm
```

| Mốc | Làm gì | Vì sao dừng ở đó |
| --- | --- | --- |
| MVP | Không có lakehouse. Metric đọc thẳng từ Postgres, kết quả eval ghi file JSON | Dữ liệu giả lập, vài nghìn dòng |
| T1–2 | **Gold tối thiểu trên BigQuery**: dataset analytics gồm eval_runs, scenario_results, metric_daily, trace_costs; job đẩy từ Postgres mỗi giờ | Đủ cho dashboard demo 11/10 và so sánh baseline (§23) |
| T3 | Thêm bronze/silver dạng Iceberg cho sự kiện giả lập + trace; dataset huấn luyện PhoBERT đọc từ gold | Chứng minh đường đi dữ liệu → model có lineage |
| Prod | Đầy đủ 3 tầng, CDC từ DMS/ERP, telematics khối lượng lớn, Dataplex, lưu theo quy định dữ liệu trong nước | Telematics hàng trăm nghìn xe; nhiều đội cùng dùng một bản dữ liệu |

Vì sao lakehouse (Iceberg) chứ không chỉ BigQuery: dữ liệu thô telematics và transcript rất lớn, lưu dạng mở trên Cloud Storage rẻ hơn và đọc được bằng nhiều engine (BigQuery cho phân tích, Spark cho huấn luyện). Phần gold vẫn dùng bảng BigQuery cho nhanh.
