# 01 · Đề bài & đối chiếu — Đáp ứng đủ đề bài — rồi đi xa hơn một bước

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Đề bài yêu cầu một AI Agent hiểu mục đích của khách xuyên suốt hội thoại, tra cứu knowledge base, dùng công cụ để hoàn thành quy trình nhiều bước, và chuyển nhân viên kèm tóm tắt. Theo góp ý của mentor, đề xuất mở rộng thành agent **chủ động**: hội thoại là một cửa vào, tín hiệu hệ thống là cửa vào thứ hai.

| Yêu cầu của đề | Cách đáp ứng | Ở đâu |
| --- | --- | --- |
| Hiểu mục đích xuyên suốt hội thoại | Goal stack: nhiều mục đích song song, chuyển chủ đề rồi quay lại, mang thông tin đã có sang mục đích sau | §06 |
| Tra cứu knowledge base | KB chính sách có phiên bản (bảo hành, bảo dưỡng, sạc, triệu hồi), trả lời kèm nguồn và ngày hiệu lực | §06 · §11 |
| Dùng công cụ cho quy trình nhiều bước | Tra đơn/lệnh sửa chữa, đặt & đổi lịch xưởng, tạo ticket, đổi/trả phụ kiện, tra trạm sạc — qua tool gateway có phân quyền | §05 · §07 |
| Chuyển nhân viên kèm tóm tắt đầy đủ | Handoff card chuẩn: mục đích đã xong/còn dở, dữ kiện từ tool, agent đã nói & hứa gì, cảm xúc, đề xuất bước tiếp | §06 · §08 |
| Không tự tạo chính sách, giá, trạng thái | Bảng nguồn sự thật + bước kiểm tra tất định: mọi con số, ngày, mã trong câu trả lời phải có trong kết quả tool/KB | §06 |
| Hành động ảnh hưởng khách phải được xác nhận | 4 mức xác nhận; nhắc lại chính xác tham số; đổi tham số thì xác nhận cũ mất hiệu lực | §06 · §09 |
| Tuân thủ pháp lý Việt Nam | Minh bạch "đang nói chuyện với AI" (Luật Trí tuệ nhân tạo, hiệu lực 1/3/2026); khiếu nại theo Luật Bảo vệ quyền lợi người tiêu dùng 2023; dữ liệu xe và vị trí theo đồng ý | §03 · §09 |
| *Mở rộng theo mentor:* chủ động, không chờ khách hỏi | Tín hiệu từ xe, trạm sạc, xưởng, kho, bảo hành đi vào cùng Decision Engine; agent theo dõi mọi việc tạo trong chat đến khi xong | §04 · §07 · PL-A |

Bối cảnh lấy cảm hứng từ hệ sinh thái VinFast / V-Green. Thông tin chính sách lấy từ nguồn công khai (ghi nguồn ở §11 và cuối trang). Mọi quy trình nội bộ, hệ thống, số liệu vận hành là **giả định** — không đại diện cho quy trình chính thức của VinFast.
