# 02 · Vấn đề — Ca hậu mãi không xong trong một lần: khách phải giục, phải kể lại, không chắc quyền lợi

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

> **Sửa 06/10 (lead, sau [business discovery lại](../research/2026-10-06-business-discovery.md)).** Tiêu đề cũ "Phần lớn lần khách liên hệ là vì
> doanh nghiệp đã làm rơi việc" **chưa có số liệu Việt Nam** — số duy nhất tìm được về tỷ lệ cuộc gọi hỏi tiến độ là của vendor (Numa, không mẫu số).
> Failure demand dưới đây là **khung phân tích, không phải tỷ lệ đã đo**. Hai pain còn bằng chứng: (P-A) yêu cầu bị chuyển bộ phận không ai giữ, không hạn;
> (P-B) khách không chắc quyền lợi đúng cho xe mình vì chính sách đổi theo ngày mua. Bảng "đến xưởng rồi phải về 1–4%" ở cuối là **giả định của đội**,
> không pitch như số đo; VinFast cam kết cấp phụ tùng trong 24 giờ từ 01/9/2024 nên kịch bản này cần dữ liệu mới trước khi dùng.

Với chủ xe điện, một cuộc hội thoại hiếm khi dừng ở một câu hỏi: hỏi đèn cảnh báo → hỏi có được bảo hành không → đặt lịch → hỏi tiến độ sửa → khiếu nại khi đến xưởng mà không có linh kiện. Nếu chatbot trả lời từng câu độc lập và không nối với dữ liệu, khách phải lặp lại thông tin — và vẫn phải tự đi giục.

Chủ xe

"Tôi đã đặt lịch rồi, đến nơi lại bảo chưa có linh kiện."

- Kể lại tình trạng xe mỗi lần liên hệ
- Không biết xe sửa đến đâu
- Không chắc có được bảo hành, sạc miễn phí không
- Kẹt ở trạm sạc lỗi, không ai phản hồi
Cố vấn dịch vụ / CSKH

"Nhân viên đang nối hệ thống thay vì chăm sóc khách."

- Tra xe, lịch, kho, bảo hành ở 5 hệ thống
- Gọi báo giá, nhắc lịch thủ công
- Claim bảo hành bị trả về mà không biết
- Tiếp khách đang bực vì lỗi của hệ thống
Doanh nghiệp

"Trả tiền cho những contact đáng lẽ không xảy ra."

- Contact giục tiến độ, hỏi lại, báo lỗi lần hai
- Slot xưởng bị lãng phí vì khách đến không sửa được
- Xe quay lại vì sửa chưa triệt để
- Niềm tin vào thương hiệu xe điện mới bị bào mòn

### Failure demand — nhu cầu sinh ra do thất bại

Khái niệm của phương pháp Vanguard (John Seddon): chia mọi lượt liên hệ thành hai loại.

#### Value demand

Khách cần một điều mới.

- "Đèn cảnh báo này là gì?"
- "Tôi muốn đặt lịch bảo dưỡng."
- "Trạm sạc gần nhất ở đâu?"

#### Failure demand

Khách liên hệ vì doanh nghiệp chưa làm, hoặc làm chưa đúng.

- "Xe tôi sửa đến đâu rồi?" — giục
- "Sao đến xưởng lại không có linh kiện?"
- "Tôi được miễn phí sạc sao lại bị trừ tiền?"
- "Đèn lại sáng dù vừa sửa xong."
**Chatbot trả lời failure demand nhanh hơn. Agent này làm failure demand không xảy ra.**

### Tâm lý chờ đợi (David Maister, 1985)

- Chờ không biết bao lâu thấy dài hơn chờ có thời hạn → mọi tin nhắn có **mốc thời gian**.
- Chờ không được giải thích thấy dài hơn → nói **đang ở bước nào, vì sao**.
- Lo lắng làm thời gian chờ dài ra → cảnh báo trên xe, kẹt ở trạm sạc cần phản hồi **trong vài phút**.

Khách giục vì **bất định**, không hẳn vì chậm.

### Khe front-office / back-office

```yaml
KHÁCH → CSKH / App / Tổng đài    Xưởng · Kho · Bảo hành hãng · V-Green
         sở hữu: khách, kênh         sở hữu: công việc, hệ thống
         KPI: AHT, CSAT             KPI: năng suất, tồn kho, duyệt claim
                 └──────── KHE ────────┘
            lịch hẹn lệch kho, claim bị trả về,
            lời hứa gọi lại — không KPI nào đo
```

Agent đóng vai **promise keeper**: giữ lời hứa end-to-end với khách, không thay kỹ thuật viên làm việc chuyên môn.

### Quy mô vấn đề — một phép tính từ số liệu công khai

VinFast bàn giao **175.099 ô tô điện tại Việt Nam trong năm 2025** (công bố 1/2026). Theo lịch bảo dưỡng công khai (6 tháng / lần), riêng lứa xe này tạo khoảng **350.000 lượt bảo dưỡng mỗi năm** — chưa tính sửa chữa, bảo hành, triệu hồi và các lứa xe trước.

| Giả định "đến xưởng rồi phải về" | Thấp · 1% | Cơ sở · 2% | Cao · 4% |
| --- | --- | --- | --- |
| Lượt đi lại lãng phí / năm | ~3.500 | ~7.000 | ~14.000 |
| Ngày công của khách mất đi (½ ngày / lượt) | ~1.750 | ~3.500 | ~7.000 |
| Contact phát sinh (giả định 2 / lượt: gọi hỏi + khiếu nại) | ~7.000 | ~14.000 | ~28.000 |
| Slot xưởng bị lãng phí | ~3.500 | ~7.000 | ~14.000 |

Chỉ tính một nhóm friction (lịch hẹn lệch kho — nhánh lập lại của UC3), một lứa xe, chỉ bảo dưỡng định kỳ. Tỷ lệ 1–4% là giả định — kiểm chứng bằng phỏng vấn cố vấn dịch vụ và stall audit. Không tách được xe cá nhân và đội xe dịch vụ từ số liệu công khai.

### Đây là bài CSKH và CX — vận hành chỉ là phương tiện

| Lớp | Trong bài này | Câu hỏi đo |
| --- | --- | --- |
| **Customer Service** | Hội thoại nhiều bước, tra cứu, đặt lịch, ticket, đổi/trả, chuyển người kèm tóm tắt | Khách có được giải quyết đúng, không phải lặp lại? |
| **Customer Experience** | Chủ động, in-flight, giữ lời hứa end-to-end, giảm công sức của khách | Khách có phải đi giục, đi lại, lo lắng không? |
| Service operations | Xưởng, kho, bảo hành, trạm sạc — agent chạm vào để tạo kết quả cho khách | Việc phía sau có thật sự xong không? |

**Nguyên tắc trình bày:** mọi use case được *mô tả* bằng trải nghiệm của khách ("đèn cảnh báo cứ lặp lại", "đến xưởng rồi phải về") nhưng được **kích hoạt bởi tín hiệu hệ thống, không bởi hành động của khách** — và kết thúc bằng một kết quả khách cảm nhận được và đã được xác minh: một tin nhắn đúng lúc, một lịch hẹn giữ được, một lần không phải đi giục.

### Bài này nằm ở đâu trên bản đồ 8 chức năng CSKH

| Chức năng | Sắc thái | Trong bài |
| --- | --- | --- |
| **Customer Support** | Xử lý sự cố, ticket, kỹ thuật | Lõi — UC1 → UC3, luồng 6 quyết định |
| **Customer Service** | Phục vụ nói chung | Lõi — hội thoại theo đề, 4 tool |
| **Customer Operations** | Quy trình, dữ liệu, hiệu quả | Lõi — lệnh sửa chữa, kho, SLA, QA |
| **Customer Experience** | Toàn bộ hành trình | Kết quả mà ba lõi tạo ra — đo bằng CES, Contacts per Job |
| Customer Care | Chăm sóc, duy trì quan hệ | Mở rộng — nhắc bảo dưỡng, memory, hỏi thăm sau sửa |
| Customer Success | Adoption, retention | Mở rộng — "90 ngày đầu làm chủ xe điện" (PL-E) |
| Client Services | B2B | Mở rộng — đội xe dịch vụ, đại lý là khách B2B của hãng (PL-E) |
| Customer Engagement | Tương tác, loyalty | Roadmap — tầng tăng trưởng của Spectrum (PL-D) |
