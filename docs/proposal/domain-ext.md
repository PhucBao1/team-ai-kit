# PL-E · Nghiệp vụ mở rộng — Phân khúc, bảo hiểm, Customer Success, Client Services, đặc thù xe điện & Việt Nam

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

### Ba phân khúc khách, ba cách chăm sóc

| Phân khúc | Họ quan tâm | Chính sách khác biệt (công khai) | Agent điều chỉnh |
| --- | --- | --- | --- |
| **Khách cá nhân** | Yên tâm, ít công sức, được đối xử tôn trọng | Bảo hành tiêu chuẩn theo dòng xe; miễn phí sạc đến 30/6/2027 | Giọng văn ấm, giải thích kỹ, ưu tiên xưởng gần nhà |
| **Đội xe dịch vụ** (taxi, gọi xe, giao hàng) | Thời gian xe chạy được — mỗi ngày nằm xưởng là mất doanh thu | Bảo hành ngắn hơn cho xe kinh doanh vận tải; chính sách sạc riêng (miễn phí 22:00–06:00, giảm 50% giờ khác) | Báo cáo cho quản lý đội xe (B2B), ưu tiên slot ngoài giờ chạy, gom nhiều xe một lượt, đo thời gian xe dừng |
| **Chủ xe thứ hai** (xe đã sang tên) | Quyền lợi còn lại là gì | Quyền lợi theo xe và thời hạn còn lại (cần xác nhận theo chính sách) | Kiểm tra liên kết tài khoản – xe khi sang tên (UC4); chào mừng chủ mới, giải thích quyền lợi còn lại |

### Luồng nhiều bên nhất: tai nạn → bảo hiểm → đồng sơn

```text
Khách báo tai nạn ─► Cứu hộ kéo xe ─► Xưởng đồng sơn tiếp nhận ─► Giám định bảo hiểm
      ─► Báo giá gửi hãng bảo hiểm ─► Bảo hiểm duyệt (có thể trả về) ─► Chờ linh kiện ─► Sửa ─► Bàn giao
Bên tham gia: khách · cứu hộ · xưởng · hãng bảo hiểm · giám định viên · kho · (ngân hàng nếu xe trả góp)
Lỗi ngầm: hồ sơ nằm chờ giám định; bảo hiểm trả về báo giá không ai nhận — cùng dạng T3 như UC5
```

Đặt ở Wave 3: cùng cơ chế với UC5 nhưng thêm một tổ chức bên ngoài (hãng bảo hiểm), cần thoả thuận chia sẻ trạng thái hồ sơ.

### Customer Success cho khách cá nhân — "90 ngày đầu làm chủ xe điện"

Customer Success vốn là khái niệm B2B: giúp khách đạt kết quả và ở lại. Áp dụng cho người mới chuyển từ xe xăng sang xe điện: họ chưa quen thói quen sạc, lo quãng đường, chưa dùng hết tính năng app, và dễ lỡ bảo dưỡng lần đầu (1.000 km hoặc 1 tháng) — trong khi bảo dưỡng đúng lịch là điều kiện giữ bảo hành.

| Mốc "làm chủ thành công" | Tín hiệu | Agent làm gì nếu chậm mốc |
| --- | --- | --- |
| Kết nối app, bật thông báo dịch vụ | Tài khoản, liên kết xe | Hướng dẫn một lần, không nhắc lại quá 2 lần |
| Lần sạc đầu thành công | Phiên sạc đầu tiên | Gợi ý trạm gần nhà / nơi làm, cách sạc |
| Bảo dưỡng lần đầu đúng hạn | Odometer ~1.000 km hoặc 1 tháng | Nhắc kèm lý do (giữ quyền bảo hành), đặt lịch có xác nhận |
| Không có "sự cố quãng đường" | Pin thấp xa trạm | Hướng dẫn lập lộ trình có trạm sạc |

Chỉ số: tỷ lệ bảo dưỡng lần đầu đúng hạn, CES 90 ngày, tỷ lệ giới thiệu / mua tiếp. Tuân thủ chính sách liên hệ chủ động — đây là Education, không phải quảng cáo.

### Client Services — hai loại khách B2B

| Khách B2B | Họ cần | Agent hỗ trợ |
| --- | --- | --- |
| **Đội xe dịch vụ** (taxi, gọi xe, giao hàng) | Thời gian xe chạy được; báo cáo; một đầu mối | Báo cáo thời gian xe dừng theo xe / tuần cho account manager; ưu tiên slot ngoài giờ chạy; gom nhiều xe một lượt; sửa từ xa trước |
| **Mạng lưới đại lý / xưởng** (khách B2B của hãng) | Claim được duyệt nhanh, linh kiện đúng hẹn, thông tin kỹ thuật mới | UC5 chính là bài toán Client Services giữa hãng và đại lý: claim bị trả về có người nhận, bằng chứng tự đính kèm, thông báo kỹ thuật đến đúng xưởng |

### Đặc thù xe điện & Việt Nam

| Chủ đề | Vì sao đặc thù | Agent làm gì |
| --- | --- | --- |
| Mùa mưa, ngập | Ngập nước là trường hợp loại trừ bảo hành theo chính sách công khai | Trước bão: nhắc an toàn, chỗ đỗ cao. Sau ngập: mời kiểm tra theo khu vực bị ảnh hưởng |
| Tết, lễ dài ngày | Đi xa đồng loạt, trạm sạc cao tốc quá tải | Gợi ý lịch sạc, trạm trên lộ trình; dự báo nhân lực tổng đài và cứu hộ |
| Lắp sạc tại nhà ở chung cư | Cần hãng, thợ điện và ban quản lý toà nhà duyệt | Hành trình liên đơn vị (VinFast · V-Green · Vinhomes): theo dõi từng bước duyệt, không để hồ sơ rơi |
| Lo lắng về pin | Pin là tài sản lớn nhất của xe, ảnh hưởng giá bán lại | Báo cáo sức khoẻ pin định kỳ; giải thích điều kiện bảo hành pin theo chính sách chính thức |
| Nắng nóng | Nhiệt độ cao ảnh hưởng pin và tốc độ sạc | Hướng dẫn sạc và đỗ xe mùa nóng |
| Sau cập nhật phần mềm | Tính năng đổi, có lỗi phát sinh (ví dụ diễn đàn chủ xe có thảo luận "mất bản đồ sau cập nhật FOTA") | KB theo phiên bản; phát hiện làn sóng câu hỏi sau cập nhật → báo Insights |

### Trải nghiệm — các điểm bổ sung

| Chủ đề | Đề xuất |
| --- | --- |
| Trung tâm tuỳ chỉnh thông báo | Khách chọn kênh, khung giờ, loại tin, tần suất; tuỳ chọn "chỉ báo khi tôi cần làm gì"; cảnh báo an toàn không tắt được |
| Khách lớn tuổi, ít dùng app | Giữ kênh tổng đài như cửa vào ngang hàng; chữ lớn, câu ngắn; xác nhận mức 2 bằng giọng nói có đọc lại tham số |
| Giọng vùng miền | Nhận dạng giọng nói phải được kiểm thử với giọng Bắc, Trung, Nam và lời nói ấp úng (PhoATIS_Disfluency) |
| Bản tin sáng cho cố vấn dịch vụ | "Hôm nay có 3 việc sắp gãy" — xếp theo mức ưu tiên, kèm handoff card sẵn; giảm việc đi tìm vấn đề |
