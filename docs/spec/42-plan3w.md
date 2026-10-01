# 42 · Kế hoạch 3 tuần — Tuần 1 dựng xương sống, tuần 2 làm đủ, tuần 3 cải thiện

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

|  | Tuần 1 · 28/9 → 4/10 MVP 30/9 + xương sống đầy đủ | Tuần 2 · 5/10 → 11/10 Đủ toàn bộ phạm vi | Tuần 3 · 12/10 → 18/10 Chỉ cải thiện |
| --- | --- | --- | --- |
| **A · Agent / AI** | MVP (§43) · tách Coordinator / PolicyQA / Scheduler / Writer–Critic · đủ 6 quyết định UC1 · chủ xe ≠ người lái · memory | UC3, UC5 đầy đủ; UC2, UC4, UC6 rút gọn · copilot + auto-wrap · 5 loại handoff · tinh chỉnh theo eval | **PhoBERT triage + cascade** (§18) · tối ưu router, prompt caching · GraphRAG |
| **B · Dữ liệu / tools** | MVP · MCP servers · Pub/Sub + schema + dead-letter + detector worker · KB có phiên bản + RAG pipeline · thế giới giả lập 200 xe + lỗi tiêm | Arbitration · luồng VED / ACN-Data · pipeline gán nhãn, dữ liệu tổng hợp, DVC, embedding blue/green (§27) · cỡ mẫu + ngưỡng detector (§28 A–B) · gold BigQuery tối thiểu (§08) | Dự báo contact, survival, uplift (§28 C–E) · dataset triage_vi cho PhoBERT · lakehouse bronze/silver Iceberg (§08) |
| **C · Frontend** | MVP · SSE tự nối lại · "Việc của tôi" đầy đủ · trace panel | Console + copilot · design system · accessibility · dashboard metric · Vitest + visual regression · giao diện kiểm thử người dùng | Hiệu năng · hoàn thiện theo phản hồi người dùng |
| **D · Nền tảng / chất lượng** | MVP · Executor + saga + outbox · Terraform + CI · OTel → Cloud Trace + Langfuse · runner eval + 40 kịch bản | ~150 kịch bản + RAG eval + red-team · eval gate · policy check + sàng lọc injection · SLO · tải + chaos · runbook | **MLflow + registry + drift** cho PhoBERT · ablation B3 + τ-bench bộ con (§23) · Temporal cho workflow nhiều ngày · tối ưu chi phí |
| **Cả nhóm** | Chốt chữ ký tool sáng 28/9 · demo MVP 30/9 | Mystery shopping · 5 người dùng thử · **demo đầy đủ 11/10** | Báo cáo số đo cuối · demo cuối 18/10 |

**Cổng 4/10:** 40 kịch bản tự động, 0 vi phạm hard gate · deploy bằng Terraform · mỗi câu trả lời có trace · 6 quyết định UC1 chạy trên giả lập.**Cổng 11/10:** mọi thành phần Phần B–C chạy và có số đo, đặt cạnh baseline B0–B2 · 6 use case trong demo · báo cáo eval + người dùng thử + mystery shopping.**Nếu tuần 2 trễ**, cắt theo thứ tự: (1) UC2/UC4/UC6 rút gọn chỉ còn detector + tin + handoff → (2) visual regression, accessibility nâng cao → (3) luồng VED/ACN (dùng dữ liệu tổng hợp) → (4) chaos. Không cắt: eval + hard gate, UC1 đầy đủ, handoff, bảo mật cơ bản.
