# 27 · AI data engineering — Dữ liệu cho AI cũng cần pipeline, phiên bản và kiểm soát chất lượng

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Pipeline | Nguồn → Đích | Kiểm soát |
| --- | --- | --- |
| **Gán nhãn từ vận hành** | NV sửa handoff card · chấp nhận / từ chối gợi ý copilot · sửa kết quả triage · lỗi eval → hàng đợi gán nhãn (Label Studio) | Hướng dẫn gán nhãn có ví dụ; 2 người gán 10% mẫu, đo độ đồng thuận (kappa) |
| **Sinh dữ liệu tổng hợp** | LLM sinh câu hỏi / hội thoại theo persona, ý định, biến thể không dấu | Lọc trùng (gần giống bằng embedding), đo độ đa dạng, LLM lọc chất lượng, người review mẫu 10%; gắn nhãn "synthetic" để không lẫn với dữ liệu thật |
| **Làm sạch dữ liệu cá nhân** | Mọi dataset từ trace thật | Sensitive Data Protection thay định danh bằng token trước khi vào kho dataset |
| **Phiên bản dataset** | Golden set, bộ test triage, bộ RAG, bộ huấn luyện | DVC trên GCS (hoặc bảng BigQuery snapshot có version); mọi kết quả eval / huấn luyện ghi dataset version |
| **Pipeline embedding** | KB đổi → chunk → contextual → embed → chỉ mục mới | Blue/green: dựng chỉ mục mới, chạy eval RAG, đạt mới chuyển; giữ chỉ mục cũ để rollback |
| **Lineage & catalog** | Từ nguồn → dataset → model / chỉ mục → release | OpenLineage / Dataplex: trả lời được "model này học từ dữ liệu nào" |

| Dataset | Kích thước (tuần 2) | Dùng cho |
| --- | --- | --- |
| triage_vi_v1 | ~3.000 câu (thật + tổng hợp) | Huấn luyện / test PhoBERT (§18) |
| rag_golden_v1 | ~150 câu + đoạn đúng | §24 |
| agent_scenarios_v1 | ~150 kịch bản YAML | §22, §25 |
| faults_labeled_v1 | Lỗi tiêm có nhãn trong thế giới giả lập | Detector P/R, ngưỡng (§28-B) |
| redteam_v1 | ~40 kịch bản tấn công | An toàn |
