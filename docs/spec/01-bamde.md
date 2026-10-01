# 01 · Bám đề — Có lạc đề không? — truy vết từ yêu cầu của đề đến code và phép đo

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Đề Vin Smart Future yêu cầu một AI Agent hiểu mục đích của khách xuyên suốt hội thoại, tra cứu knowledge base, dùng công cụ để hoàn thành quy trình nhiều bước, chuyển nhân viên kèm tóm tắt, không tự tạo chính sách / giá / trạng thái, và xác nhận trước mọi hành động ảnh hưởng khách. Bảng dưới cho thấy mỗi yêu cầu nằm ở thành phần nào, được đo ở đâu, xong khi nào.

| Yêu cầu của đề | Thành phần | Đo ở | Xong |
| --- | --- | --- | --- |
| Hiểu mục đích xuyên suốt hội thoại | Coordinator + goal stack (§13, §14) · triage (§15; model riêng ở §18) | Goal-tracking accuracy, Re-ask rate (§25) | Tuần 1 |
| Tra cứu knowledge base | RAG có phiên bản (§16) · "tool trước, RAG sau" (§34) | Recall@5, faithfulness, version accuracy (§24) | Tuần 1 |
| Dùng công cụ cho quy trình nhiều bước (tra đơn, đặt lịch, ticket, đổi/trả) | Tools & MCP (§11, §12) · Executor (§17) | Tool selection, trạng thái cuối (§25) | MVP → tuần 1 |
| Chuyển nhân viên kèm tóm tắt đầy đủ | Handoff builder + console (§05-D, §20) | Re-ask rate của NV, độ đầy đủ card (§22, §25) | MVP |
| Không tự tạo chính sách, giá, trạng thái | claim_check (§17) · tool trước RAG (§34) | Grounding violation = 0 (§22) | MVP |
| Hành động ảnh hưởng khách phải được xác nhận | Confirmation token + validator + Executor (§05-C, §17) | Ghi không xác nhận = 0 (§22) | MVP |
| *Mở rộng theo mentor:* chủ động, không chờ khách hỏi | Sự kiện → detector → proactive pipeline (§05-B, §09, §14) | Detection P/R, Pre-chase recovery (§22) | MVP → tuần 2 |

**Kết luận:** lõi không lạc đề — cả sáu yêu cầu của đề đều có thành phần, phép đo và mốc hoàn thành, và đều nằm trong MVP / tuần 1. Phần chủ động là mở rộng theo góp ý mentor, dùng chung một bộ não. Các phần rộng hơn (model ML riêng, data science nâng cao, production trên GCP) đều **phục vụ** lõi này — triage cho "hiểu mục đích", đo lường cho "chứng minh", hạ tầng cho "chạy thật" — và được xếp vào tuần 3 hoặc thiết kế production, không lấn vào phạm vi chính.**Khi trình bày:** luôn mở bằng đề bài và kịch bản demo hội thoại → xác nhận → sự kiện chủ động → chuyển người. Kỹ thuật (multi-agent, MLOps, GCP) chỉ xuất hiện để trả lời câu hỏi "làm sao chắc chắn chạy đúng và chạy thật". Nếu mở bằng kỹ thuật, bài sẽ trông như lạc đề dù nội dung không lạc.

### Độ đầy đủ

| Hạng mục | Trạng thái |
| --- | --- |
| Nghiệp vụ, use case, CX (proposal) | Đủ ở mức thiết kế — thiếu bằng chứng thật (phỏng vấn, mystery shopping) → tuần 2 |
| Kiến trúc, thành phần, chất lượng, vận hành (tài liệu này) | Đủ |
| Pháp lý dữ liệu, dữ liệu thật, tích hợp hệ thống thật của hãng | Không thể hoàn tất trong cuộc thi — nói thẳng khi trình bày |
