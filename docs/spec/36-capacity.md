# 36 · Tải & chi phí (ước tính) — Một phép tính để biết kiến trúc có đủ và có lãi không

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Đại lượng | Giả định | Kết quả |
| --- | --- | --- |
| Xe kết nối | Riêng lứa bàn giao 2025 tại VN: 175.099 xe (công bố) | ~175.000 |
| Sự kiện nghiệp vụ / ngày | Giả định 3 sự kiện / xe / ngày (mã lỗi, sạc, lịch, kho…) | ~525.000 / ngày ≈ 6 / giây |
| Qua được L0 | Giả định 1% | ~5.000 candidate / ngày |
| Cần LLM (sau L1, arbitration) | Giả định 40% | ~2.000 lượt / ngày |
| Hội thoại | Giả định 2% chủ xe nhắn / ngày, 6 lượt | ~21.000 lượt / ngày |

Toàn bộ là **giả định để định cỡ**, thay bằng số đo thật khi có. Kết luận định tính: lưu lượng sự kiện nhỏ với Pub/Sub; chi phí chủ yếu nằm ở hội thoại, không phải proactive — vì L0 lọc gần hết. Chi phí thật được đo bằng ACRC trên dashboard; phần dưới là ước tính bằng tiền để định ngân sách.

### Chi phí bằng tiền (ước tính theo giá niêm yết, tra ngày 27/9/2026)

Tỷ giá dùng: 1 USD ≈ 26.200 đ (giá bán Vietcombank 25/9/2026 là 26.180). Giá model lấy theo mức **sau khuyến mãi** để không đánh giá thấp: dòng Flash mới đang giảm 50% đến 31/12/2026. Số token mỗi bước là giả định thiết kế, sẽ thay bằng số đo từ trace (Langfuse) sau tuần 1.

| Model (Gemini) | Dùng cho | Input / 1M token | Output / 1M token | Input đã cache |
| --- | --- | --- | --- | --- |
| Flash (dòng 3.6–3.8) | Coordinator, PolicyQA, Writer, LLM chấm | $1,50 (đang KM $0,75) | $7,50 (đang KM $3,75) | $0,15 |
| Flash-Lite 3.1 | Triage, claim check, Critic, handoff card, khách ảo | $0,25 | $1,50 | $0,025 |
| Pro 3.1 (preview) | Scheduler lập phương án UC3 | $2,00 | $12,00 | $0,20 |

### Một hội thoại (6 lượt)

| Bước / lượt | Token (in / out) | USD |
| --- | --- | --- |
| Triage (Flash-Lite) | 800 / 50 | 0,0003 |
| Coordinator × 2 lần gọi (Flash, 3k cache) | 6.000 / 250 mỗi lần | 0,0137 |
| PolicyQA, 40% số lượt (Flash) | 4.000 / 300 | 0,0025 |
| Claim check (Flash-Lite) | 1.500 / 100 | 0,0005 |
| **Cộng mỗi lượt** |  | **0,017** |
| **Một hội thoại** (6 lượt + handoff 15%) |  | **≈ $0,10 ≈ 2.700 đ** |
| Sau tối ưu (xem dưới) |  | **≈ $0,05 ≈ 1.300 đ** |

### Một ca proactive lên L2

| Bước | Token (in / out) | USD |
| --- | --- | --- |
| Triage (Flash-Lite) | 1.500 / 100 | 0,0005 |
| Scheduler (Pro, có suy luận) | 8.000 / 1.500 | 0,0340 |
| Writer (Flash) × 1,3 vòng | 3.000 / 300 | 0,0088 |
| Critic (Flash-Lite) × 1,3 vòng | 2.000 / 150 | 0,0009 |
| **Một ca** |  | **≈ $0,044 ≈ 1.160 đ** |

Detector L0 và arbitration là code, gần như 0 đồng. Ca bị L0 loại không tốn LLM.

### Chi phí trong 3 tuần cuộc thi

| Khoản | Cách tính | Ước tính |
| --- | --- | --- |
| Cloud SQL Postgres (db-g1-small + 10 GB SSD) | $25,76 + $1,70 / tháng | ≈ $28 / tháng |
| Cloud Run (api, agent, mcp, detector, web) | Trả theo request; demo chủ yếu nằm trong free tier hằng tháng | $0–10 |
| Một lần chạy eval đầy đủ | 300 kịch bản (bộ mở rộng; bộ 150 của tuần 2 ≈ ½) × k = 4 × (hội thoại $0,10 + LLM chấm $0,011 + khách ảo $0,003) | ≈ $139 ≈ 3,6 triệu đ (giá KM hiện tại: ≈ ½) |
| Eval trong CI | Bộ con 50 kịch bản × k = 1 mỗi PR | ≈ $6 / lần |
| Dev hằng ngày (4 người) | Giả định | $5–15 / ngày |
| **Tổng 3 tuần** | ~4 lần eval đầy đủ + CI + dev + hạ tầng | **≈ $500–1.000 ≈ 13–26 triệu đ** (thấp nếu dùng giá KM) |

Giảm: dùng giá Flash khuyến mãi đến hết 2026; LLM chấm chạy qua Batch API (rẻ hơn gọi trực tiếp); chỉ chạy eval đầy đủ ở mốc 30/9, 11/10, 18/10 và khi đổi model. Tài khoản GCP mới có tín dụng dùng thử — kiểm tra điều kiện.

### Chi phí production (theo định cỡ ở bảng trên)

| Khoản / tháng | Cách tính | USD |
| --- | --- | --- |
| LLM — hội thoại | 21.000 lượt/ngày ÷ 6 × 30 ≈ 105.000 hội thoại × $0,05–0,10 | 5.200–10.700 |
| LLM — proactive | 2.000 ca/ngày × 30 = 60.000 ca × $0,044 | ≈ 2.650 |
| AlloyDB (HA, 4 vCPU / 32 GB, 100 GB) | (4 × $0,066 + 32 × $0,0112) × 730 giờ × 2 node + lưu trữ | ≈ 940 |
| Cloud Run (~8 instance luôn chạy, 1 vCPU / 2 GB) | Tính theo instance, chưa kể scale theo tải | ≈ 460 |
| Memorystore, Pub/Sub, BigQuery, Logging/Trace, GKE (Temporal) | Ước lượng thô, cần Pricing Calculator | 1.000–1.500 |
| **Tổng** |  | **≈ $10.000–16.000 ≈ 270–430 triệu đ / tháng** |
| **Mỗi việc** (hội thoại hoặc ca proactive) | Tổng ÷ ~165.000 việc/tháng, đã gồm hạ tầng | **≈ $0,06–0,10 ≈ 1.600–2.600 đ** |

**Đọc con số thế nào:** chi phí chủ yếu nằm ở LLM của hội thoại, cụ thể là coordinator — nên tối ưu ở đó trước. Gartner dự báo chi phí mỗi lần giải quyết bằng GenAI vượt $3 vào 2030; thiết kế nhiều tầng (L0 code, triage rẻ, chỉ ca khó mới lên model lớn) giữ mức này ở vài xu. Lợi ích so sánh là một lượt xe đến xưởng rồi phải về (UC3 · nhánh lập lại) hay một cuộc gọi hỏi lại được tránh — con số đó cần dữ liệu thật, đo bằng ACRC, không ước ở đây.

### Đòn bẩy giảm chi phí (thứ tự làm)

| Đòn bẩy | Tác động ước tính | Khi nào |
| --- | --- | --- |
| Router: lượt đơn giản (chào, xác nhận, hỏi trạng thái) dùng Flash-Lite thay Flash | Hội thoại $0,10 → ~$0,05 (cùng với cache) | Tuần 2 |
| Prompt caching phần tĩnh (system prompt, mô tả tool, chính sách hay dùng) | Phần input cache rẻ bằng 1/10 | Tuần 1 |
| Rerank chỉ giữ 3–5 đoạn thay vì nhồi 20 | Giảm input PolicyQA; tăng độ chính xác | Tuần 1–2 |
| Giới hạn ≤ 8 tool call / lượt, ngân sách token theo loại việc | Chặn ca chạy vòng tốn tiền | Tuần 1 |
| PhoBERT triage (cascade) | Bỏ ~70% lượt gọi LLM ở triage; lợi chính là độ trễ | Tuần 3 |
| Batch API cho LLM chấm, insights, VoC ban đêm | Rẻ hơn gọi trực tiếp | Tuần 3 |
| Model open-weight tự host (vLLM) cho khối lượng lớn | Chỉ lợi khi tải đủ lớn để GPU luôn bận | Production |
