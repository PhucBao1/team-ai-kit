# 47 · Quyết định kiến trúc (ADR) — Ghi lại vì sao — để trả lời giám khảo và để không cãi lại

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| # | Quyết định | Lý do | Phương án đã loại |
| --- | --- | --- | --- |
| 001 | Logic bảo hành, quãng đường, validator là code tất định | Sai ở đây gây khiếu nại nặng nhất; cần test được | Để LLM tự suy luận |
| 002 | Ghi dữ liệu cần confirmation token do khách tạo | Ràng buộc "xác nhận trước" của đề phải được cưỡng chế bằng code | Dặn trong prompt |
| 003 | LangGraph + Gemini, chạy trên GCP | Nhóm chọn LangGraph: trạng thái dạng đồ thị rõ, interrupt chờ người duyệt, checkpoint bền, tài liệu nhiều; chạy trên Cloud Run, gọi Gemini qua Vertex AI. Chỉ dùng **một** framework điều phối để trạng thái, trace và eval không bị chia đôi | Google ADK (GCP-native); dùng cả hai cùng lúc (bỏ: hai nơi giữ trạng thái) |
| 004 | Handoff card lắp từ dữ liệu có cấu trúc | Tóm tắt tự do dễ sai, khó kiểm | LLM tóm tắt toàn bộ hội thoại |
| 005 | Cloud Run trước, GKE chỉ khi cần | Ít vận hành, scale về 0 ở dev | GKE cho mọi thứ |
| 006 | Dữ liệu định danh ở vault trong nước, GCP dùng token giả | Chưa có region GCP tại Việt Nam; yêu cầu dữ liệu trong nước cần pháp chế xác nhận | Đưa định danh thẳng lên region nước ngoài |
| 007 | Loop 4 chỉ tạo đề xuất, người duyệt | Agent không tự sửa chính sách của mình | Tự động áp dụng thay đổi |
| 008 | Không fine-tune trong 2 tuần | Chưa có dữ liệu nhãn; eval quan trọng hơn | Fine-tune model nhỏ cho triage |
