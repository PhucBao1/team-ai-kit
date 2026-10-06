# 04 · Định vị & in-flight proactive — Proactive đã là thực hành chung. Khác biệt (giả thuyết) nằm ở phần sau khi báo.

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

Xử lý khiếu nại**Agent không chờ khách hỏi** — tín hiệu đến từ xe, trạm sạc, xưởng, kho, bảo hành. Cửa sổ **T0** (lỗi lặp khi khách chưa tạo case — UC1) là **cửa vào**, hãng đã có tính năng tương tự. Trọng tâm là **T1–T2 — việc bị kẹt**: điều kiện lịch hẹn thay đổi (UC3 lập lại), ca chuyển người quá hạn hoặc chưa ai nhận, việc sau sửa chưa có kết quả rõ. Khác với outreach cho sự kiện đã biết: không gửi tin cho mọi event, phát hiện bằng cơ chế rẻ (rule, 0 token), chỉ gọi LLM khi cần suy luận, nói đúng trạng thái và theo việc tới kết quả. UC2 (sạc), UC4 (hoá đơn), UC5 (claim), UC6 (tái phát) giữ ở mức spec.

| Trục | Chatbot CSKH | Proactive outreach | Đề xuất này |
| --- | --- | --- | --- |
| Kích hoạt | Khách nhắn | Sự kiện đã biết | Khách nhắn *và* tín hiệu hệ thống, cùng một bộ não |
| Kết thúc khi | Hội thoại kết thúc | Tin được gửi | Việc đi hết vòng đời: đã xác nhận → đã sửa xong → đã theo dõi, chưa thấy lỗi (hoặc mở lại) |
| Loại vấn đề | Câu hỏi, tác vụ đơn | Sự cố hệ thống biết | Cả lỗi ngầm liên hệ thống mà hệ thống không tự biết |
| Theo kết quả | CSAT sau chat | Tỷ lệ mở tin | Dữ liệu thật: lịch, kho, lệnh sửa, telematics. "Đã xác minh" chỉ khi dữ liệu đầy đủ + xe đã chạy lại + khách xác nhận hết triệu chứng — không có mã lỗi mới là chưa đủ |

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
| **VinFast** (VF e34, công bố 05/2021) | Xe tự gửi mã lỗi về trung tâm bảo hành; lỗi phần mềm sửa từ xa; lỗi phần cứng báo lên màn hình + app; nhắc bảo dưỡng, đặt lịch một chạm ([bài đăng lại](https://vinfastdienchau.vn/news/tinh-nang-ho-tro-cham-soc-khach-hang-tu-dong-tu-xa-cua-vinfast-vf-e34/)). Có giao nhận xe tận nhà, mượn xe miễn phí ([VTV 11/2025](https://vtv.vn/giao-nhan-xe-tan-nha-cuu-ho-24-7-muon-xe-mien-phi-hau-mai-vinfast-tao-su-khac-biet-tren-thi-truong-100251127182754514.htm)) | **Giám khảo biết điều này** — không pitch "phát hiện trước" là điểm mới |
| **NIO** (Trung Quốc) | Chuyên viên dịch vụ theo trọn ca, tiến độ real-time trong app (bằng người) | "Có người giữ ca" đã có — khác biệt là làm bằng agent + hạn hồi đáp đo được |
| **Toyota Việt Nam** (đại lý) | Đặt lịch dịch vụ qua Zalo OA (nhân viên chat) | Zalo đã là kênh quen; agent xử lý trọn ca trên Zalo mới là chưa thấy |

**Nói thẳng (viết lại 06/10 sau [business discovery](../research/2026-10-06-business-discovery.md)):** chẩn đoán từ xa, báo lỗi cho khách,
gửi trước linh kiện, dịch vụ lưu động, người theo trọn ca là **thực hành đã có** — kể cả VinFast (VF e34, 2021) — nên đề xuất **không** tuyên bố
"phát hiện trước" là điểm mới. Chuỗi đề xuất giữ: **chủ động phát hiện → kiểm tra → thông báo → đề xuất → xác nhận / thực hiện → chuyển người → theo kết quả.**

Các khác biệt dưới đây là **giả thuyết cần kiểm chứng** (chưa tìm thấy ai làm trong ≈20 lượt search; nhiều nguồn bị chặn, chưa thử kênh VinFast):

| # | Khác biệt (giả thuyết) | Bằng chứng nhu cầu | Card |
| --- | --- | --- | --- |
| 1 | Trả lời quyền lợi **theo chính chiếc xe và ngày mua** (bảo hành, sạc miễn phí, pin, chương trình còn hạn), có trích dẫn đúng phiên bản | Chính sách VinFast đổi ≥ 4 lần trong 18 tháng; KB của chính đội từng trả bản đã hết hiệu lực | A2.20, A2.21 |
| 2 | **Có người giữ việc + hạn cập nhật**; tách "đã chuyển" với "đã có người nhận"; phát hiện ca quá hạn chưa ai nhận | Ca VF9 (10/2024): VinFast kỷ luật 4 nhân sự vì chậm xử lý; Pied Piper 2025: 56% lần AI chuyển người thất bại | A2.22, A2.25, A2.26 |
| 3 | **Nói đúng trạng thái khi lỗi** — không báo "đã chuyển" khi chưa chuyển, không tự hứa giờ mới | Moffatt v. Air Canada 2024: doanh nghiệp chịu trách nhiệm lời bot | A2.22, A2.26 |
| 4 | **Không đóng việc sai** — vòng đời đã xác nhận → đã sửa xong → đã theo dõi / mở lại | J.D. Power CSI 2025 (Mỹ): 12% không sửa đúng lần đầu | A2.23 |
| 5 | Một bộ não cho cả hội thoại theo đề bài lẫn chủ động, có xác nhận và guardrail tất định | Yêu cầu bắt buộc của đề BTC | đã có |

Roadmap riêng (không thuộc chuỗi chính): kênh Zalo thật, gọi điện bằng AI, chụp ảnh đèn taplo, giao nhận xe qua agent, upsell.

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
