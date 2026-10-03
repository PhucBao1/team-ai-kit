# 04 · Định vị & in-flight proactive — Proactive đã là xu hướng. Khác biệt nằm ở thời điểm và loại vấn đề.

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Salesforce · 01/2026

#### Proactive Service

Detect → Resolve → Optimize trên dữ liệu hợp nhất, chủ động gửi hướng dẫn cho khách.

→ Outreach cho sự kiện đã biết đã có sản phẩm thương mại.Dreamforce · 09/2026

#### Outcome-based pricing

Chỉ tính phí agent CSKH khi vấn đề được giải quyết; governance theo từng task.

→ "Resolved" phải được đo chặt — metric của đề xuất khớp mô hình này.Gartner · 06/2025

#### >40% dự án agentic bị huỷ trước 2027

Chi phí leo thang, giá trị không rõ, kiểm soát rủi ro yếu.

→ Cost-aware, outcome metric, guardrail tất định trả lời ba điểm này.

### Can thiệp ở mốc nào?

T0

#### Sự cố xảy ra

Xe báo mã lỗi, trụ sạc hỏng, xe thuộc diện triệu hồi. Khách chưa biết.

Agent: cảnh báo + đề xuấtT1 → T2

#### Việc đang chạy dở

Đã đặt lịch, xe đang ở xưởng, claim đang chờ duyệt, lời hứa gọi lại. Workflow âm thầm dừng.

← Khác biệt chính (cùng với T0 đang hình thành)T2

#### Khách phải giục

"Xe tôi sửa đến đâu rồi?" — failure demand.

Chatbot thông thườngT3

#### Khiếu nại

Khiếu nại, mạng xã hội, mất niềm tin vào thương hiệu.

Xử lý khiếu nại**Agent không chờ khách hỏi** — tín hiệu đến từ xe, trạm sạc, xưởng, kho, bảo hành. Giá trị nằm ở hai cửa sổ: **T0 đang hình thành** — friction nổi lên từ nhiều tín hiệu lặp lại khi khách chưa tạo case nào (UC1, UC2); và **T1–T2** — việc đã chạy dở, doanh nghiệp đã hứa, workflow âm thầm dừng (UC3 lập lại, UC5, UC6). Khác với outreach cho sự kiện đã biết: không gửi tin cho mọi event, mà phát hiện friction bằng cơ chế rẻ, chỉ gọi LLM khi cần suy luận, và xác minh kết quả.

| Trục | Chatbot CSKH | Proactive outreach | Đề xuất này |
| --- | --- | --- | --- |
| Kích hoạt | Khách nhắn | Sự kiện đã biết | Khách nhắn *và* tín hiệu hệ thống, cùng một bộ não |
| Kết thúc khi | Hội thoại kết thúc | Tin được gửi | Việc của khách được xác minh là xong |
| Loại vấn đề | Câu hỏi, tác vụ đơn | Sự cố hệ thống biết | Cả lỗi ngầm liên hệ thống mà hệ thống không tự biết |
| Xác minh | CSAT sau chat | Tỷ lệ mở tin | Dữ liệu thật: lịch, kho, và telematics xác nhận lỗi đã hết |

### Big enterprise đang làm gì — và điểm mới thật của đề xuất

| Doanh nghiệp | Đã làm | Bài học / liên hệ |
| --- | --- | --- |
| **BMW Proactive Care** (9/2023, toàn cầu) | Xe gửi mã lỗi, chẩn đoán lốp, nhu cầu bảo dưỡng về đại lý (có đồng ý); AI soạn đề xuất; liên hệ qua app, trong xe, email, đại lý, cứu hộ; mẹo tự xử lý, cập nhật phần mềm từ xa, hỗ trợ đi lại, video dịch vụ cá nhân hoá, thanh toán online | Tiền lệ cho ① phân loại từ xa và hỗ trợ đi lại |
| **Tesla** (từ 2019) | Xe tự chẩn đoán và gửi trước linh kiện tới xưởng khách hay dùng trước khi xe đến | Tiền lệ cho ④ dự đoán linh kiện |
| **Rivian** (2026) | Mở rộng Remote Care; tăng 50% xe dịch vụ lưu động (hình thức khách thích nhất); giảm 35% thời gian chờ đặt lịch | Tiền lệ cho "sửa từ xa trước, lưu động trước xưởng" |
| **Verizon** (8/2026) | AI xử lý phần lớn cuộc gọi và chat đến; chuyển người kèm đủ ngữ cảnh; điều kiện tiên quyết là nhiều năm hợp nhất dữ liệu | Nền dữ liệu phải có trước AI |
| **Bank of America** (7/2026) | EricaAssist hỗ trợ 18.000+ nhân viên CSKH: tóm tắt lý do gọi, gợi ý bước tiếp theo < 3 giây, giảm ~1 phút mỗi cuộc gọi | Bắt đầu bằng copilot cho nhân viên — rủi ro thấp |
| **Klarna** (2024–2026) | AI làm việc tương đương 700 nhân viên, giảm nhân sự ngoài từ 3.000 xuống 2.300 → CSAT giảm mạnh ở ca phức tạp → tuyển lại đội 100 chuyên gia | Không hứa cắt người; CSAT là điều kiện cứng |
| **Ngân hàng Việt Nam** | Chatbot Vietcombank ~500.000 yêu cầu/tháng, đáp ứng ~70% nhu cầu cơ bản; ~15% ngân hàng dùng AI ở mức trung bình, chưa ai triển khai AI agent quy mô lớn; 65% chưa có kho dữ liệu tập trung (Tạp chí Ngân hàng) | Khoảng trống có thật ở Việt Nam; dữ liệu phân mảnh là rào cản chính |

**Nói thẳng:** chẩn đoán từ xa, gửi trước linh kiện và ưu tiên dịch vụ lưu động là **thực hành đã được chứng minh** ở BMW, Tesla, Rivian — đề xuất dùng lại chúng có chủ đích. Điểm mới của đề xuất nằm ở bốn chỗ: **(1)** phát hiện friction đang hình thành từ tín hiệu lặp lại *và* cứu việc đang chạy dở giữa các hệ thống (in-flight: lịch lệch kho, claim kẹt, tín hiệu quay lại sau sửa) — các hãng trên chủ yếu dừng ở phát hiện lỗi xe; **(2)** một bộ não cho cả hội thoại theo đề bài lẫn chủ động, với xác nhận và guardrail tất định; **(3)** "xong" được xác minh bằng dữ liệu xe; **(4)** bối cảnh Việt Nam và hệ sinh thái nhiều đơn vị.

### Reactive AI vs Proactive AI — và đề xuất này ở đâu

| Đặc điểm | Reactive AI | Proactive AI (theo Parloa / ngành) | Đề xuất này |
| --- | --- | --- | --- |
| Kích hoạt | Chờ câu hỏi, click, cuộc gọi | Theo dõi tín hiệu liên tục, hành động trước khi được hỏi | Cả hai cửa vào, cùng một bộ não |
| Dữ liệu | Chỉ input hiện tại | Lịch sử + telemetry thời gian thực | Telematics, CSMS, DMS, ERP, claim + hội thoại |
| Memory | Không có hoặc chỉ trong phiên | Hồ sơ khách dài hạn + kết quả | Journey state + memory sở thích có đồng ý (§06-H) |
| Logic quyết định | Rule if-then | Lập kế hoạch theo mục tiêu + dự đoán | Rule tất định trước, LLM chỉ khi mơ hồ, validator trước khi ghi |
| Học | Rule tĩnh, sửa tay | Vòng phản hồi liên tục | Learn có người duyệt: đề xuất ngưỡng, SOP, root cause — không tự sửa policy |
| Thời gian phản hồi | Tức thì | Vài giây, có tính toán trước | Hội thoại: 1–3 giây · Proactive: bất đồng bộ, đúng thời điểm (không cần tức thì, cần *kịp*) |
| Phạm vi vấn đề | Câu hỏi của khách | Sự kiện đã biết (churn, outage, fraud) | Thêm friction đang hình thành (T0) và lỗi ngầm liên hệ thống trong cửa sổ in-flight |
