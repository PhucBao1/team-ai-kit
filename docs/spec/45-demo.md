# 45 · Kịch bản demo — Một câu chuyện, ba phía, mọi yêu cầu của đề

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Bảng dưới là demo MVP 30/9. Demo đầy đủ 11/10 giữ nguyên câu chuyện này và thêm: bảng số đo từ eval (hard gate = 0, task success, RAG faithfulness), một kịch bản UC3 (kẹt ở trạm sạc), trace multi-agent, và kết quả người dùng thử + mystery shopping. Demo 18/10 thêm triage PhoBERT so với LLM (độ chính xác, độ trễ, chi phí).

| Phút | Thao tác | Nói gì |
| --- | --- | --- |
| 0:00 | Mở trang, bấm Reset | "Anh Minh đi VF 8. Chúng tôi sẽ cho thấy cả ba phía: khách, nhân viên, và agent." |
| 0:20 | Bấm "Xe báo lỗi làm mát pin" | "Khách chưa hỏi gì — agent chủ động nhắn, nói rõ mức độ, và kiểm tra lỗi không sửa được từ xa." |
| 1:00 | Gõ: "đặt giúp anh cuối tuần, có được bảo hành không?" | "Hai mục đích trong một câu. Bảo hành do module tất định tính, không phải LLM đoán." |
| 1:45 | Chọn 9:00, bấm Xác nhận | "Không có nút này thì hệ thống không thể ghi — kể cả khi AI muốn." |
| 2:15 | Bấm "Tua +2 ngày", rồi "Linh kiện bị điều đi" | "Đây là lỗi ngầm giữa hai hệ thống. Hôm nay khách chỉ biết khi đến xưởng." |
| 2:45 | Chat hiện 2 phương án; màn hình "Việc của tôi" cập nhật | "Pin 42% đủ đi tới cả hai xưởng; Gia Lâm có sẵn linh kiện." |
| 3:15 | Gõ: "cho anh nói chuyện với người" | — |
| 3:30 | Console nhân viên hiện handoff card | "Nhân viên đọc 10 giây là nắm việc. Có cả ô 'không làm' — không hỏi lại biển số." |
| 4:00 | NV bấm Chốt phương án 1 → chat nhận xác nhận | "Agent nhận lại việc và tiếp tục theo dõi." |
| 4:30 | Mở trace panel | "Phần lớn bước không dùng LLM — đó là cách giữ chi phí và độ chính xác." |
