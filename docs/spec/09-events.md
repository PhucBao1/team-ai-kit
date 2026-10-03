# 09 · Sự kiện & detector — Một định dạng sự kiện chung, rule tất định

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

```text
# Định dạng sự kiện (CloudEvents-style) — giữ nguyên khi chuyển sang Pub/Sub
{
  "id": "evt_01J…", "type": "vehicle.dtc.raised",
  "source": "telematics", "time": "2026-09-29T08:15:00+07:00",
  "data": { "vin": "VF8-4821", "code": "BATT-COOL-01", "severity": "WARNING",
            "odometer_km": 38420, "soc_pct": 42 }      # giả lập
}

# Các loại sự kiện MVP / tuần 1
vehicle.dtc.raised          # telematics: vin, code, severity, odometer, soc
parts.reservation.cancelled # ERP — tín hiệu lập lại phương án của UC3 (lịch đã xác nhận mất linh kiện)
parts.eta.changed           # ERP — như trên
appointment.changed         # DMS
chat.handoff.requested      # chatbot — đường khẩn của UC2 (tuần 2)
repair_order.closed         # DMS — mở vòng 5 xác minh; tái phát → UC6

# Đề xuất cho UC2 / UC4 / UC5 (chưa vào contracts/events.yaml — B + D chốt qua PR + ADR khi implement)
charging.session.failed     # CSMS / telematics — UC2
charging.session.completed  # CSMS — verify UC2
billing.charge.created      # billing — UC4 (spec)
warranty.claim.state_changed # warranty portal giả lập — UC5 (spec)
```
```python
# detect/rules.py — L0, không gọi LLM
def on_reservation_cancelled(evt, db, now):                 # UC3: nhánh lập lại phương án
    appt = db.appointment(evt.data["appointment_id"])
    if appt and appt.status == "confirmed" and appt.start_at - now < timedelta(hours=72):
        return Candidate(type="T1_PARTS_APPOINTMENT", journey_id=appt.journey_id,
                         priority="high" if db.dtc_severity(appt.vin) != "INFO" else "normal")
    return None

def on_dtc_raised(evt, db, now):
    sev = db.dtc(evt.data["code"]).severity
    if sev == "CRITICAL":
        return SafetyPath(evt)            # mẫu tin duyệt sẵn + chuyển 24/7, không qua LLM
    if sev == "WARNING":                  # UC1: một lần đơn lẻ là nhiễu; lặp lại + chưa có case mới là friction
        vin, system = evt.data["vin"], db.dtc(evt.data["code"]).system
        n = db.count_dtc(vin, system, days=14)
        if n >= 3 and not db.open_case(vin, system):
            return Candidate(type="UC1_PREEMPTIVE_FRICTION", vin=vin, system=system, count=n)
    return None                           # INFO / WARNING đơn lẻ: gộp, không candidate, 0 token
```
