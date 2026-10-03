# 13 · Roadmap — Từ một lịch hẹn đến cả hệ sinh thái

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

#### Level 0 — Nền dữ liệu

Journey State Graph hợp nhất lịch, kho, lệnh sửa chữa, claim, dữ liệu xe; đồng ý dữ liệu xe. Bài học Verizon: AI chỉ tốt bằng nền dữ liệu bên dưới.

#### Level 1 — MVP

Lõi hội thoại đạt đủ yêu cầu đề + UC1 (flagship) với 6 quyết định đặc thù xe điện (phân loại từ xa, bảo hành, phiên bản phần mềm, dự đoán linh kiện, xếp lịch theo quãng đường, xác minh bằng dữ liệu xe) + UC2, UC3 demo-ready, trên thế giới giả lập có nhãn. Triển khai thật bắt đầu bằng **copilot cho CVDV**, tự động hoá bật dần theo ngưỡng.

#### Level 2 — Hậu mãi đầy đủ

UC6 tái phát verify bằng telematics (khép vòng chăm sóc); lời hứa báo giá (ý tưởng ngoài sáu UC); báo cáo root cause cho kho và xưởng. **Pilot copilot kỹ thuật viên tại 1 xưởng:** chẩn đoán trước khi xe đến, giữ linh kiện sớm.

#### Level 3 — Tiền & bảo hành

UC4 phí sạc (có người duyệt), UC5 claim bảo hành; SLA Care trên trạng thái đã xác minh. **Insights / VoC agent:** bản tin vấn đề mới nổi hằng tuần cho đội chất lượng; copilot kỹ thuật viên mở rộng toàn mạng lưới xưởng.

#### Level 4 — Education & chiến dịch

"90 ngày đầu làm chủ xe điện" (Customer Success); Client Services cho đội xe dịch vụ; mùa mưa ngập / Tết (PL-E). Nhắc bảo dưỡng theo odometer, chiến dịch triệu hồi, chuẩn bị trước mốc kết thúc sạc miễn phí; Contact Arbitration.

#### Level 4.5 — Giọng nói & trong xe

Kênh tổng đài giọng nói và trợ lý trên xe dùng chung bộ não; nhận ảnh đèn cảnh báo qua Zalo; copilot cho CVDV.

#### Level 5 — Hệ sinh thái

Stack production: Kafka + Flink, Temporal cho workflow nhiều ngày, policy engine tại tool gateway, model open-weight tự host, A2A giữa các đơn vị. V-Green, Vinhomes, Xanh SM dùng chung nền tảng; multi-agent (triage · chẩn đoán · lập lịch · outreach · chất lượng) với routing tất định trước LLM.

#### Level 6 — Khách hàng là máy

Trợ lý AI cá nhân của khách (ChatGPT, Gemini, Claude…) sẽ tự liên hệ doanh nghiệp thay khách. Mở API / MCP có xác thực và uỷ quyền rõ ràng để agent của khách tra tiến độ, đặt lịch — cùng validator, cùng quy tắc xác nhận (xác nhận do chính chủ xe uỷ quyền).
