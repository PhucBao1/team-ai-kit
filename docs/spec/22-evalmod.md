# 22 · Chiến lược đánh giá 5 tầng — Đo ở năm tầng: module → agent → end-to-end → hệ thống → kinh doanh

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Module | Chỉ số | Bộ dữ liệu | Cách đo | Ngưỡng |
| --- | --- | --- | --- | --- |
| Tầng 1 · Module tất định | | | | |
| warranty_precheck | Đúng tuyệt đối | 60 xe có nhãn (biên: đúng ngày hết hạn, đúng km) | pytest + property test | 100% |
| range / find_options | Phương án khả thi; khoảng cách tới tối ưu | 200 tình huống pin / khoảng cách / kho | So với bộ giải vét cạn | 100% khả thi |
| validator | Chặn đúng, không chặn nhầm | Ma trận check × tình huống | pytest | 100% |
| claim_check | Tỷ lệ bắt số bịa; tỷ lệ chặn nhầm | 300 câu trả lời có số bịa gieo sẵn + 300 câu sạch | Tự động | Bắt ≥ 99% · chặn nhầm ≤ 3% |
| Detector L0 | Precision / recall | Lỗi tiêm có nhãn trong thế giới giả lập | Tự động | ≥ 95% / ≥ 80% |
| Arbitration | Chặn đúng khi có việc mở / khiếu nại / quá ngân sách | 50 tình huống | Tự động | 100% |
| Tầng 2 · Module AI | | | | |
| Triage | Accuracy ý định; **recall mức khẩn** | 500 câu tiếng Việt (có không dấu, viết tắt) | Tự động, confusion matrix | ≥ 90% · khẩn ≥ 99% |
| Retrieval | Recall@5, MRR, nDCG; context precision | 150 câu hỏi chính sách có đoạn đúng gán nhãn | Ragas / tự viết | Recall@5 ≥ 90% |
| Trả lời chính sách | Faithfulness, answer relevancy, trích dẫn đúng | Cùng bộ trên | Ragas / DeepEval + người kiểm 5% | Faithfulness ≥ 0,95 |
| Tool calling | Chọn đúng tool; tham số đúng; trajectory khớp | 100 lượt có trajectory mẫu | So trajectory từ state LangGraph (runner của nhóm / agentevals) | ≥ 95% |
| Scheduler | Phương án hợp lệ; mọi phương án bị loại có lý do; khách chọn phương án đầu | Kịch bản UC3 | Tự động + online | 100% hợp lệ |
| Writer (tin chủ động) | Đủ 5 phần; giọng văn; độ dài | 100 tin | Rubric LLM, hiệu chỉnh với người | 5/5 phần · giọng ≥ 4/5 |
| Handoff card | Đủ trường; đúng nguồn; Re-ask Rate | 50 hội thoại | Tự động + NV chấm | Re-ask ≤ 5% |
| Tầng 3 · End-to-end agent | | | | |
| Hội thoại theo đề | Task success, pass^k (k=3), số lượt tới xong | ~150 kịch bản, khách ảo | Runner kịch bản | ≥ 85% · pass^3 ≥ 75% |
| Detector + Agent chọn lọc (UC1) | Detector P/R trên bộ có nhãn + kịch bản đối chứng (1 lần đơn lẻ, đã có case); llm_call_rate = L2 / event; token mỗi event không phải candidate = 0 | Lỗi tiêm có nhãn + kịch bản đối chứng | Runner | Không candidate sai từ CRITICAL · 0 token ngoài candidate |
| Proactive UC1 | Pre-chase recovery, time-to-recovery | Lỗi tiêm + tua thời gian | Runner | ≥ 70% |
| Hard gates | Grounding violation, ghi không xác nhận, unsafe action | Tất cả kịch bản + nhóm tấn công | Tự động | 0 |
| Tầng 4 · Hệ thống | | | | |
| Hiệu năng | p50/p95 độ trễ, lỗi, throughput | Tải Locust | Tải + SLO | §29 |
| Chi phí | Token / lượt, ACRC, llm_call_rate theo use case | Trace thật | Langfuse | Theo ngân sách |
| Chống chịu | Hành vi khi model / MCP lỗi | Chaos | Fault injection | Suy giảm có kiểm soát |
| Tầng 5 · Người dùng & kinh doanh | | | | |
| Trải nghiệm | CES, SUS, thời gian hoàn thành | 5 người dùng thử (tuần 2) | Kiểm thử người dùng | — |
| Kinh doanh | Wasted visit, contacts per job, CSAT vs nhóm đối chứng | Pilot thật | Holdout | Không kém đối chứng |

### Quản lý bộ đánh giá

- Golden set có phiên bản, nằm trong repo; phân tầng: chuẩn · mơ hồ · tấn công · không dấu · chủ xe / người lái
- Lỗi thật ở production → thành kịch bản mới (loop 4)
- LLM-as-judge phải **hiệu chỉnh với người**: độ đồng thuận (Cohen's kappa) ≥ 0,7 mới dùng
- So sánh hai phiên bản bằng khoảng tin cậy bootstrap, không nhìn một con số

### Offline, online, và khi nào chạy

- **Mỗi PR:** tầng 1 + tập con tầng 2–3 liên quan
- **Hằng đêm:** toàn bộ tầng 1–3, k = 3
- **Online:** lấy mẫu 5–10% trace thật, chấm tự động hằng ngày
- **Trước release:** tầng 4 (tải, chaos)
- **Pilot:** tầng 5 với nhóm đối chứng
