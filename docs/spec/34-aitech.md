# 34 · Kỹ thuật AI & framework — Mỗi kỹ thuật có chỗ dùng cụ thể — và có kỹ thuật cố ý không dùng

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

### Nguyên tắc số 1: tool trước, RAG sau

Câu hỏi về **trạng thái** (lịch, kho, xe, bảo hành của xe này) luôn đi qua tool gọi hệ thống gốc — không bao giờ qua RAG. RAG chỉ dùng cho **chính sách, hướng dẫn, SOP, giải thích mã lỗi**. Đây là cách chặn loại lỗi phổ biến nhất của chatbot CSKH: trả lời trạng thái từ tài liệu cũ.

### Retrieval — chọn gì trong các kỹ thuật RAG 2026

| Kỹ thuật | Dùng? | Chỗ dùng / lý do |
| --- | --- | --- |
| Lọc metadata trước khi tìm | Có — bắt buộc | Dòng xe, loại hình sử dụng, phiên bản phần mềm, còn hiệu lực. Không lọc thì trả lời sai phiên bản chính sách |
| Hybrid retrieval (vector + BM25, gộp bằng RRF) | Có | Mã lỗi, mã linh kiện, tên điều khoản cần khớp từ khoá chính xác; câu hỏi tự nhiên cần vector |
| Cross-encoder reranking | Có | Lấy 20 → rerank → giữ 3–5 đoạn; tăng chính xác, giảm token |
| Chunk theo điều khoản + parent-child | Có | Tìm theo đoạn nhỏ, trả về cả điều khoản cha để không mất điều kiện đi kèm |
| Contextual retrieval (thêm ngữ cảnh vào chunk trước khi embed) | Có | "Thời hạn 3 năm" vô nghĩa nếu không biết là của xe kinh doanh vận tải — thêm ngữ cảnh tài liệu vào từng chunk |
| Adaptive RAG (định tuyến theo độ phức tạp) | Có | Triage quyết định: không cần tìm (câu xã giao / trạng thái → tool) · tìm một bước · tìm nhiều bước |
| GraphRAG / knowledge graph | Production | Mã lỗi → hệ thống → linh kiện → SOP → kỹ năng (§16). MVP dùng bảng quan hệ |
| Query rewriting / RAG fusion | Có giới hạn | Chỉ cho câu không dấu, viết tắt, teencode: khôi phục dấu + 2 cách diễn đạt, gộp kết quả |
| CRAG (thiếu tài liệu thì tìm web) | Không | Không lấy chính sách từ web. Thiếu tài liệu → nói chưa có thông tin → chuyển người + ghi lỗ hổng KB |
| HyDE, RAPTOR, Self-RAG (huấn luyện) | Không | Corpus nhỏ và có cấu trúc; không đáng độ phức tạp |

**Riêng tiếng Việt:** khôi phục dấu cho câu không dấu trước khi tìm; tách từ tiếng Việt cho BM25 (ví dụ thư viện underthesea); chọn model embedding bằng cách **đo trên bộ câu hỏi tiếng Việt của chính mình** (§22), không chọn theo bảng xếp hạng chung.

### Các kỹ thuật agent khác

| Kỹ thuật | Dùng ở đâu |
| --- | --- |
| Function calling + structured output (JSON schema) | Mọi tool, mọi quyết định, handoff card |
| Plan-then-execute | UC3: lập danh sách phương án trước, rồi mới gọi tool ghi sau xác nhận |
| Reflection / self-verification có phản hồi tất định | Loop 2: claim_check trả lỗi cụ thể để model sửa |
| Router + subagent (supervisor pattern) | Triage định tuyến tất định sang scheduler / writer; không dùng "bầy agent" tự do — chi tiết §14 |
| Memory 3 tầng | §16 |
| Guardrail đa tầng | Input screening → policy ở tool gateway → validator → claim check → output screening |
| Semantic cache | **Chỉ** cho câu trả lời chính sách chung, khoá theo phiên bản chính sách; **không bao giờ** cache câu trả lời cá nhân hay trạng thái |
| Multimodal (thị giác) | Ảnh đèn cảnh báo trên màn hình xe gửi qua Zalo (tuần 2 / production) |
| Speech: streaming ASR, VAD, cho phép ngắt lời | Kênh tổng đài (production) |
| Distillation / fine-tune model nhỏ | Roadmap: triage và writer, khi đã có vài nghìn nhãn từ trace (§49) |
| Prompt optimization tự động (kiểu DSPy) | Roadmap: tối ưu prompt triage / writer theo bộ eval |

Framework và thư viện cụ thể, kèm việc mỗi cái giải quyết: xem bảng tổng hợp §33.
