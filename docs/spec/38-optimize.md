# 38 · Tối ưu — Độ trễ, chi phí, chất lượng — đo trước, tối ưu sau

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Mục tiêu | Kỹ thuật | Khi nào | Rủi ro cần canh |
| --- | --- | --- | --- |
| **Độ trễ** | Stream token đầu tiên sớm; câu mở đầu ngắn từ model nhanh | MVP | — |
| Gọi tool song song; prefetch dữ liệu xe khi khách mở chat | Tuần 1 | Prefetch thừa tốn tài nguyên |
| Prompt caching (phần tĩnh đặt đầu) | Tuần 1 | Đổi thứ tự prompt làm mất cache |
| Context nhỏ (nén, cắt kết quả tool) | Tuần 1 | Cắt mất bằng chứng → eval phải bắt |
| Đặt service cùng region với endpoint model; min-instances | Production | Chi phí chạy nền |
| **Chi phí** | Router: model nhỏ cho triage / writer | Tuần 1 | Chất lượng tụt → eval theo module |
| L0 tất định lọc trước LLM | MVP | Rule lỗi thời → theo dõi recall |
| Batch API cho việc không gấp (loop 4, VoC, chấm eval) | Tuần 2 | — |
| Semantic cache chỉ cho câu chính sách chung | Production | Cache sai phiên bản → khoá theo version |
| Distill model nhỏ tự host cho triage | Roadmap | Cần dữ liệu nhãn đủ; drift |
| **Chất lượng** | Contextual retrieval + rerank | Tuần 1–2 | Chi phí nạp KB tăng |
| Lặp prompt theo bộ eval (eval-driven development) | Liên tục | Quá khớp bộ eval → luôn thêm lỗi thật |
| Tối ưu prompt tự động | Roadmap | Khó giải thích thay đổi |
| **Độ tin cậy** | Model dự phòng; suy giảm có kiểm soát; hàng đợi bền | Tuần 2 | Model dự phòng trả lời khác phong cách |
