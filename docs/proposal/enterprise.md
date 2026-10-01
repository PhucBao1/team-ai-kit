# PL-D · Enterprise & Proactive Spectrum — Sâu theo hành trình, rộng theo nền tảng — ở quy mô hệ sinh thái

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

### A. Proactive Spectrum: nền móng trước, tăng trưởng sau

XUYÊN SUỐT

#### Contact Arbitration

Mỗi khách, mỗi thời điểm: gửi tin nào — hay không gửi gì. Một ngân sách chú ý chung cho mọi chương trình.

TĂNG TRƯỞNG

#### Discovery

Tính năng app (điều khiển từ xa, lịch sạc), dịch vụ hệ sinh thái.

Phase 3 · CDP + rule

#### Upsell

Gói bảo dưỡng, phụ kiện, bộ sạc tại nhà — có đồng ý, không khi có việc mở.

Phase 3+ · recommenderPHÒNG THỦ

#### SLA Care

Tiến độ sửa xe, trụ sạc bảo trì, lịch triệu hồi — chỉ trên trạng thái đã xác minh.

Phase 2 · rule + model nhỏ

#### Education

Nhắc bảo dưỡng theo odometer (giữ quyền bảo hành); chuẩn bị khách trước khi chương trình sạc miễn phí kết thúc 30/6/2027.

Phase 2–3 · ruleNỀN MÓNG

#### Lõi hội thoại + Recovery (toàn vẹn trạng thái)

Không thể cập nhật tiến độ đúng cho khách khi lịch và kho đang lệch nhau. Mọi tầng phía trên chỉ đúng khi tầng này đúng.

Phase 1 · MVP**Một làn sóng failure demand có thể dự đoán:** khi chương trình sạc miễn phí kết thúc (30/6/2027 theo công bố), hàng loạt chủ xe sẽ hỏi "từ giờ tôi trả bao nhiêu?", "sao bị trừ tiền?". Education chủ động trước mốc này — với chính sách mới từ KB có phiên bản — là ví dụ rõ nhất về giảm failure demand ở quy mô lớn.

### B. Hệ sinh thái: một khách, nhiều đơn vị

```text
Khách sống ở Vinhomes · đi ô tô VinFast · sạc ở trụ V-Green dưới hầm toà nhà · thỉnh thoảng đi Xanh SM
   → 4 đơn vị · 4 bộ hệ thống · 1 khách

Ví dụ: trụ sạc tầng hầm toà S2 bảo trì 23:00–05:00
   V-Green   → cần báo cư dân có xe điện sạc qua đêm ở S2
   VinFast   → xe nào của cư dân S2 đang có SoC thấp? (dữ liệu xe, có đồng ý)
   Vinhomes  → cư dân đang có khiếu nại mở với BQL?
   Arbitration → 1 tin gộp, đúng người, đúng giờ; hoãn tin tiếp thị của mọi đơn vị
```

### C. Nền tảng dùng chung

```text
ĐƠN VỊ     VinFast hậu mãi   V-Green sạc     Vinhomes cư dân    Xanh SM đội xe
           lịch, kho, claim  trụ, phiên, phí  BQL, sửa chữa      xe kinh doanh vận tải
═══════════════════════ NỀN TẢNG DÙNG CHUNG ═══════════════════════
  Journey State Graph   Decision Engine    Contact Arbitration   Lõi hội thoại
  Identity & Consent    Tool Gateway (MCP) Eval + Holdout        Agent Registry · Policy-as-code · Audit
═════════════════════════════════════════════════════════════════════════
HỆ THỐNG GỐC  telematics · CSMS · DMS · ERP · warranty · CRM · billing  (đọc: event/CDC · ghi: tool có kiểm soát)
```

### Journey State Graph — lời hứa đang mở của một chiếc xe

```text
{
 "vin": "…4821", "model": "VF 8", "owner": "C-10293",
 "usage": "personal", "odometer": 38420,
 "journeys": [{
   "type": "service_repair", "appointment": "SA-20931",
   "promises": [
     {"by":"agent","what":"sửa 03/10 09:00 Long Biên"},
     {"by":"agent","what":"CVDV gọi trong 15 phút"}],
   "tasks": [
     {"sys":"DMS","state":"confirmed"},
     {"sys":"ERP","state":"reservation_cancelled"}],
   "divergence": [{"type":"T1","since":"Thu 14:02"}]
 }],
 "consent": {"vehicle_data":true,"location":true,"marketing":false},
 "other_bu": {"vinhomes_open_case": false}
}
```

### Ai chịu trách nhiệm (RACI)

| Hoạt động | Process owner | Digital Ops | CSKH | Pháp chế |
| --- | --- | --- | --- | --- |
| Duyệt quy tắc nghiệp vụ | A | R | C | C |
| Bật tự động cho một loại hành động | A | R | C | C |
| Duyệt mẫu tin (kể cả an toàn) | C | I | A/R | C |
| Sự cố agent làm sai | C | A/R | R | I |
| Dùng dữ liệu giữa các đơn vị | C | R | I | A |

R thực hiện · A chịu trách nhiệm cuối · C tham vấn · I được thông báo

**Đa thị trường, đa ngôn ngữ:** VinFast đã bán xe ở nhiều thị trường ngoài Việt Nam. Cùng Decision Engine và validator; KB, SOP, mẫu tin và quy định pháp lý (minh bạch AI, dữ liệu cá nhân) theo từng thị trường; claim check hoạt động độc lập ngôn ngữ vì đối chiếu con số và mã.

Mỗi đơn vị là một pháp nhân riêng: graph dùng chung về kỹ thuật, nhưng quyền đọc dữ liệu chéo theo đồng ý của khách và thoả thuận nội bộ.

### Mức sẵn sàng cho big enterprise — tự đánh giá

| Chiều | Trạng thái | Nội dung / việc còn thiếu |
| --- | --- | --- |
| Kiến trúc nhiều đơn vị, nền tảng dùng chung | Có trong thiết kế | Journey State Graph, Decision Engine, Arbitration dùng chung; mỗi đơn vị làm sâu hành trình riêng |
| Governance, RACI, audit, policy | Có trong thiết kế | Agent registry, SOP có chủ sở hữu, kill switch, quy trình sự cố |
| Tuân thủ pháp lý | Có trong thiết kế | Minh bạch AI, bảo vệ người tiêu dùng, đồng ý dữ liệu xe; *cần pháp chế xác nhận yêu cầu lưu trữ dữ liệu trong nước* |
| Đo giá trị có đối chứng | Có trong thiết kế | Holdout, ACRC, retention |
| Hoạt động khi LLM gặp sự cố | Cần bổ sung | **Suy giảm có kiểm soát:** nhà cung cấp LLM gián đoạn → L0 rule, luồng an toàn và mẫu tin vẫn chạy; hội thoại chuyển sang người; không mất tín hiệu nào (hàng đợi bền) |
| Không phụ thuộc một nhà cung cấp model | Cần bổ sung | Model router đổi được nhà cung cấp; model chạy nội bộ cho dữ liệu nhạy cảm; bộ đánh giá chạy lại khi đổi model |
| Yêu cầu phi chức năng (NFR) | Cần bổ sung | Mục tiêu đề xuất: hội thoại p95 < 3 giây; luồng an toàn không phụ thuộc LLM, sẵn sàng ≥ 99,95%; L0 xử lý luồng event của hàng trăm nghìn xe theo thời gian thực |
| Bảo mật | Cần bổ sung | SSO / phân quyền theo vai trò cho nhân viên và đại lý, mã hoá dữ liệu, kiểm thử xâm nhập, red-team định kỳ cho prompt injection |
| Tích hợp mạng lưới đại lý | Cần chứng minh | Đại lý có thể là doanh nghiệp độc lập với hệ thống riêng — cần thoả thuận dữ liệu và chuẩn API chung |
| Quản trị thay đổi, đào tạo | Cần chứng minh | Triển khai theo làn: 1 xưởng → 1 vùng → toàn quốc; đào tạo CVDV, kỹ thuật viên; đo tỷ lệ chấp nhận gợi ý |
| Kết quả thật | Cần chứng minh | Chỉ có sau pilot: WRR, Wasted Visit Rate, FTFR so với holdout |

**Kết luận:** ở mức thiết kế, đề xuất đạt tầm big enterprise. Ở mức bằng chứng, chưa — và không bài thi nào đạt được trước khi có pilot. Nói thẳng điều này khi trình bày thuyết phục hơn là tuyên bố "enterprise-ready".
