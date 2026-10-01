# 04 · Năm vòng lặp — Mỗi vòng: nằm ở đâu trong code, dừng khi nào, tốn bao nhiêu

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Vòng | Module | Kích hoạt | Điều kiện dừng | Ngân sách / giới hạn |
| --- | --- | --- | --- | --- |
| 1 · Agent | agent/ (LangGraph graph) | Mỗi lượt chat / mỗi candidate | Model trả lời cuối hoặc gọi handoff | ≤ 8 tool call / lượt · ≤ 20 giây · ngân sách token theo loại việc |
| 2 · Verification | core/claim_check, core/validator, hook trước/sau tool | Trước khi gửi tin · trước mọi tool ghi | Sạch lỗi, hoặc 2 lần sửa thất bại → handoff | ≤ 2 lần sửa; rubric giọng văn chỉ chạy mẫu 10% (chi phí) |
| 3 · Event-driven | detect/ worker + Arbitration | Pub/Sub message | Candidate đã xử lý hoặc bị chặn có lý do | Giới hạn tốc độ gửi / khách / ngày; hàng đợi ưu tiên khi làn sóng (triệu hồi) |
| 4 · Hill-climbing | improve/ job hằng tuần | Lịch tuần + khi metric giảm | Đề xuất đã được người duyệt / từ chối | Chỉ tạo pull request cho SOP / KB / ngưỡng; **không** tự merge; phải qua eval gate |
| 5 · Outcome | Temporal workflows (workflows/) | Journey mở | Xác minh xong / khách huỷ / chuyển người | Timer bền; mỗi bước là activity có retry + timeout |

### Workflow nhiều ngày (loop 5) — Temporal

```python
# workflows/appointment_guard.py — phác thảo
@workflow.defn
class AppointmentGuard:
    # sống từ lúc đặt lịch đến khi xe sửa xong và được xác minh
    @workflow.run
    async def run(self, appt_id: str):
        while not self.done:
            # chờ tín hiệu (reservation huỷ, ETA đổi, khách đổi lịch) hoặc mốc kiểm tra
            await workflow.wait_condition(lambda: self.signal_pending, timeout=timedelta(hours=12))
            state = await workflow.execute_activity(check_appointment_health, appt_id, ...)
            if state.parts_at_risk:
                await workflow.execute_activity(start_rescue, appt_id, ...)   # → luồng B
            if state.hours_to_start <= 36 and not self.reminded:
                await workflow.execute_activity(send_reminder, appt_id, ...); self.reminded = True
            self.done = state.repair_closed
        await workflow.execute_child_workflow(VerifyFix.run, appt_id)        # 7–30 ngày theo loại lỗi

@workflow.defn
class VerifyFix:
    @workflow.run
    async def run(self, appt_id: str):
        window = await workflow.execute_activity(verification_window, appt_id, ...)
        await workflow.sleep(window)                                          # timer bền, không mất khi restart
        recurred = await workflow.execute_activity(dtc_recurred, appt_id, ...)
        await workflow.execute_activity(close_or_reopen, appt_id, recurred, ...)   # UC5 nếu tái phát
```

MVP / tuần 1 dùng đồng hồ giả lập + job định kỳ thay Temporal; tuần 2 (nếu kịp) hoặc production chuyển sang Temporal. Giao diện activity giữ nguyên.
