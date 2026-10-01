# 09 · Sự kiện & detector — Một định dạng sự kiện chung, rule tất định

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

```text
# Định dạng sự kiện (CloudEvents-style) — giữ nguyên khi chuyển sang Pub/Sub
{
  "id": "evt_01J…", "type": "parts.reservation.cancelled",
  "source": "erp", "time": "2026-10-01T14:02:00+07:00",
  "data": { "reservation_id": "R-7702", "appointment_id": "SA-20931",
            "part_code": "BATT-COOL-PUMP", "reason": "reallocated_recall" }
}

# Các loại sự kiện MVP / tuần 1
vehicle.dtc.raised          # telematics: vin, code, severity, odometer, soc
parts.reservation.cancelled # ERP
parts.eta.changed           # ERP
appointment.changed         # DMS
chat.handoff.requested      # chatbot — UC3 (tuần 2)
repair_order.closed         # DMS — mở vòng 5 xác minh
```
```python
# detect/rules.py — L0, không gọi LLM
def on_reservation_cancelled(evt, db, now):
    appt = db.appointment(evt.data["appointment_id"])
    if appt and appt.status == "confirmed" and appt.start_at - now < timedelta(hours=72):
        return Candidate(type="T1_PARTS_APPOINTMENT", journey_id=appt.journey_id,
                         priority="high" if db.dtc_severity(appt.vin) != "INFO" else "normal")
    return None

def on_dtc_raised(evt, db, now):
    sev = db.dtc(evt.data["code"]).severity
    if sev == "CRITICAL":
        return SafetyPath(evt)            # mẫu tin duyệt sẵn + chuyển 24/7, không qua LLM
    if sev == "WARNING":
        return Candidate(type="T0_DTC_WARNING", vin=evt.data["vin"])
    return None                           # INFO: gộp vào lần liên hệ sau
```
