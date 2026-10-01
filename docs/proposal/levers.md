# PL-B · 10 đòn bẩy AI cho CSKH — Đối chiếu với khung 10 đòn bẩy năng suất CSKH

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Khung của Fin (Intercom) liệt kê 10 cách AI nâng năng suất CSKH, kèm chỉ số và kiểu thất bại cần chặn. Bảng dưới cho thấy đề xuất đã cover cả 10 — và chặn kiểu thất bại bằng cơ chế cụ thể, không chỉ bằng lời hứa.

| Đòn bẩy | Trong đề xuất | Chỉ số theo dõi | Kiểu thất bại → cách chặn |
| --- | --- | --- | --- |
| 1. Tự giải quyết tầng 1 | Lõi hội thoại + tool (§06) | Task completion, tỷ lệ chuyển người, CES cho phần tự động | Bịa chính sách → nguồn sự thật + claim check |
| 2. Tiếp nhận + phân loại | L1 triage: chủ đề, mức khẩn từ dữ liệu xe (§05) | Thời gian đến hành động có ý nghĩa đầu tiên, routing accuracy | Bỏ sót khẩn cấp → mức khẩn lấy từ SoC, vị trí, mã lỗi, không chỉ từ lời khách |
| 3. RAG cho nhân viên | Copilot CVDV / tổng đài (§05) | Thời gian xử lý, tỷ lệ mở lại, điểm QA | Nội dung cũ được coi là đúng → KB sống, ngày hiệu lực, phát hiện mâu thuẫn (§06-G) |
| 4. Soạn nháp câu trả lời | Copilot gợi ý, nhân viên gửi | Tỷ lệ chấp nhận gợi ý, mức nhân viên phải sửa, điểm QA | Nháp quá tự tin, lệch quy định → claim check cả với bản nháp |
| 5. Tóm tắt + tự hoàn tất sau contact | Handoff card; tự ghi chú, gắn nhãn lý do liên hệ khi kết thúc | Thời gian làm việc sau contact, độ đầy đủ hồ sơ | Tóm tắt sai gây làm lại → tóm tắt có trích nguồn, nhân viên xác nhận khi nhận |
| 6. Gợi ý bước tiếp theo | "Đề xuất" trong handoff card, phương án UC1 | Tỷ lệ chuyển tiếp, tỷ lệ giải quyết, tuân thủ SOP | Gợi ý chung chung bị bỏ qua → gợi ý dựa trên dữ liệu cụ thể (kho, slot, khoảng cách) |
| 7. Phát hiện cảm xúc + rủi ro | Cảm xúc trong goal stack; bộ phát hiện khiếu nại (UIT-ViOCD) | Tỷ lệ chuyển tiếp, tỷ lệ khiếu nại, tỷ lệ giữ chân | Báo động quá nhiều → ngưỡng theo phân khúc, gộp cảnh báo, đo precision |
| 8. Tín hiệu proactive | Lõi khác biệt: T0 + in-flight (§04, §07, PL-A) | Contact per khách hoạt động, Contacts per Job | Nhắm sai gây nhiễu → Decision Engine có lựa chọn "không làm gì", Contact Arbitration |
| 9. Định tuyến + dự báo nhân lực | Định tuyến theo kỹ năng; **dự báo làn sóng contact từ lịch sự kiện** (triệu hồi, kết thúc sạc miễn phí 30/6/2027) để xếp ca trước | SLA, tuổi tồn đọng, mức tải nhân viên | Tối ưu tốc độ hơn chất lượng → đo cùng lúc QA và Contacts per Job |
| 10. Governance + đánh giá | §09, QA tự động, kiểm thử hồi quy | Tỷ lệ chấp nhận gợi ý của nhân viên, tỷ lệ lỗi | Niềm tin thấp → ít dùng → không ROI → shadow mode, hiển thị bằng chứng mỗi đề xuất |
