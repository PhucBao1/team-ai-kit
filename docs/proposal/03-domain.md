# 03 · Bối cảnh nghiệp vụ — Hành trình chủ xe điện: nhiều bên, nhiều hệ thống, nhiều mốc có hệ quả thật

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Một chủ ô tô điện đi qua nhiều năm sử dụng và chạm vào ít nhất 7 hệ thống, 6 bộ phận. Khác với nhiều ngành, **chiếc xe tự phát tín hiệu** — doanh nghiệp thường biết có vấn đề trước khách.

```text
KÊNH        App VinFast · Tổng đài 1900 23 23 89 · Zalo OA · Website · Showroom/xưởng
               │
HỆ THỐNG    Telematics (IoT xe) · CSMS trạm sạc (IoT, OCPP) · DMS xưởng/lệnh sửa chữa
            ERP kho phụ tùng · Warranty portal hãng · Billing sạc · CRM · Hồ sơ xe & chủ xe
               │
CON NGƯỜI   CSKH · Cố vấn dịch vụ (CVDV) · Kỹ thuật viên · Kho · Bảo hành hãng · Vận hành V-Green
               │
            Không ai sở hữu toàn bộ hành trình của một chiếc xe
```

### Chính sách công khai làm nền nghiệp vụ

BẢO HÀNH · công khai

#### Theo dòng xe & loại hình sử dụng

VF 8, VF 9: 10 năm hoặc 200.000 km; VF 3, 5, 6, 7: 8 năm hoặc 160.000 km. Xe kinh doanh vận tải: thời hạn ngắn hơn (ví dụ 3 năm hoặc 100.000 km với một số dòng). Loại trừ: không bảo dưỡng đúng lịch, linh kiện không chính hãng, tai nạn, ngập nước…

→ "Xe tôi còn bảo hành không?" cần: dòng xe + ngày mua + odometer + loại hình sử dụng + lịch sử bảo dưỡngBẢO DƯỠNG · công khai

#### 1.000 km / 1 tháng, sau đó 5.000 km / 6 tháng

Nhắc lịch trước 10 ngày; đặt lịch online hoặc qua tổng đài. Bảo dưỡng đúng lịch tại xưởng ủy quyền là nghĩa vụ để giữ quyền bảo hành.

→ Nhắc theo odometer thực từ telematics chính xác hơn theo lịch; bỏ bảo dưỡng ảnh hưởng quyền lợi bảo hànhSẠC · công khai

#### Miễn phí sạc đến 30/6/2027

Khách hàng cá nhân được miễn phí sạc tại trạm V-Green; xe kinh doanh vận tải: miễn phí 22:00–06:00, giảm 50% khung giờ khác (theo công bố 12/2024).

→ Quyền ưu đãi phụ thuộc hồ sơ xe – chủ xe – loại hình sử dụng ở các hệ thống khác nhauTRIỆU HỒI · công khai

#### 5/2024: 2.097 xe, 3 nhóm lỗi

VF e34, VF 5 Plus, VF 6 Plus, VF 8, VF 9; kiểm tra và thay thế miễn phí; liên hệ từng chủ xe; thực hiện 24/5–24/9/2024.

→ Chiến dịch triệu hồi = lọc theo số khung, liên hệ, đặt lịch, giữ linh kiện, theo dõi tỷ lệ hoàn thànhHẠ TẦNG SẠC · công khai

#### V-Green: siêu trạm 150 kW

Kế hoạch 99 siêu trạm sạc trên quốc lộ, trụ 150 kW chuẩn CCS2; trạm đô thị phục vụ 50–60 xe cùng lúc.

→ Trạng thái trụ sạc thời gian thực là tín hiệu IoT cho proactiveGIẢ ĐỊNH

#### Quy trình nội bộ

Luồng lệnh sửa chữa, giữ linh kiện, duyệt claim giữa đại lý và hãng, SLA nội bộ, công suất xưởng trong tài liệu này là giả định để minh hoạ.

→ Xác nhận lại với nghiệp vụ thật khi có cơ hội

### Bản đồ điểm gãy theo giai đoạn

| Giai đoạn | Tín hiệu có sẵn | Yêu cầu thường gặp | Điểm gãy ngầm | Use case |
| --- | --- | --- | --- | --- |
| **1. Mua & nhận xe** | Đơn hàng, đăng ký, bàn giao | Tiến độ giao xe, giấy tờ | Sang tên / loại hình sử dụng không đồng bộ sang tài khoản sạc | UC4 |
| **2. Sử dụng & sạc** | Telematics, CSMS trạm sạc | Trạm gần nhất, sạc không nhận, phí sạc | Trạm lỗi khi khách đang kẹt; handoff ngoài giờ rơi; tính phí sai | UC3 · UC4 |
| **3. Bảo dưỡng định kỳ** | Odometer, lịch hẹn | Đặt lịch, báo giá, tiến độ | Lời hứa báo giá bị quên; xe nằm chờ | UC2 |
| **4. Sự cố & bảo hành** | Mã lỗi, lệnh sửa chữa, kho, claim | "Có được bảo hành không?", đặt lịch sửa | Lịch lệch kho linh kiện; claim bị hãng trả về không ai nhận; lỗi quay lại sau sửa | UC1 · UC5 · UC6 |
| **5. Triệu hồi / cập nhật phần mềm** | Danh sách số khung, OTA | "Xe tôi có trong diện triệu hồi không?" | Chủ xe chưa liên hệ được; lịch triệu hồi thiếu linh kiện | Spectrum |

### Vòng đời lệnh sửa chữa — xương sống của hậu mãi

Mỗi lần xe vào xưởng là một lệnh sửa chữa (RO) đi qua 9 trạng thái. Mỗi trạng thái có người sở hữu, SLA và một câu khách muốn biết. Lỗi ngầm xảy ra ở chỗ chuyển trạng thái. SLA giả định

| Trạng thái | Người sở hữu | SLA | Khách muốn biết | Lỗi ngầm hay gặp | Agent theo dõi |
| --- | --- | --- | --- | --- | --- |
| 1. Tiếp nhận | CVDV | 15 phút sau khi xe đến | "Xe tôi đã được nhận chưa?" | Khách đến đúng hẹn nhưng lịch không có trong DMS | Lịch hẹn ↔ check-in |
| 2. Chẩn đoán | Kỹ thuật viên | 2 giờ | "Xe bị gì?" | Chờ kỹ thuật viên có chứng chỉ pin cao áp | Thời gian ở trạng thái, kỹ năng |
| 3. Báo giá | CVDV | 1 giờ sau chẩn đoán | "Hết bao nhiêu, có bảo hành không?" | Báo giá lập xong nhưng không ai liên hệ (UC2) | RO chờ duyệt + liên lạc ra |
| 4. Khách duyệt | Khách | Trong ngày | "Tôi duyệt thế nào?" | Khách duyệt qua điện thoại, không ghi vào DMS | Duyệt trong app / ghi nhận |
| 5. Chờ linh kiện | Kho | Theo ETA | "Khi nào có linh kiện?" | Linh kiện bị điều đi, ETA đổi không báo (UC1) | Reservation ↔ RO |
| 6. Chờ duyệt bảo hành | Bảo hành hãng | 2 ngày làm việc | "Có được bảo hành không?" | Claim bị trả về, không ai nhận (UC6) | Trạng thái claim |
| 7. Sửa chữa | Kỹ thuật viên | Theo định mức | "Bao giờ xong?" | Vượt định mức không cập nhật giờ trả xe | Giờ công thực tế vs định mức |
| 8. Kiểm tra chất lượng | Tổ trưởng | 30 phút | — | Bỏ qua chạy thử khi xưởng đông | Có bản ghi QC |
| 9. Bàn giao & theo dõi | CVDV | Theo hẹn | "Lấy xe lúc mấy giờ?" · "Đã hết lỗi chưa?" | Lỗi quay lại sau khi đóng RO (UC5) | Telematics 14–30 ngày |

Quy tắc hỗ trợ đi lại (giả định): xe nằm xưởng quá **3 ngày** vì lỗi thuộc bảo hành hoặc chờ linh kiện → agent đề xuất cho CVDV phương án hỗ trợ đi lại (xe thay thế hoặc chuyến đi) theo chính sách, và báo khách chủ động. Đây là yếu tố CX lớn nhất khi sửa lâu.

### Khiếu nại có nghĩa vụ pháp lý

Luật Bảo vệ quyền lợi người tiêu dùng 2023 (hiệu lực 1/7/2024) quy định trách nhiệm tiếp nhận và giải quyết khiếu nại của doanh nghiệp. Vì vậy agent phải nhận ra khi một tin nhắn **đã là khiếu nại** (bộ phát hiện khiếu nại huấn luyện từ UIT-ViOCD + từ khoá), và khi đó: không tự trả lời cho xong, không gửi tin bán hàng, ghi nhận chính thức, chuyển bộ phận xử lý khiếu nại kèm toàn bộ lịch sử, và báo khách thời hạn phản hồi. Quy trình cụ thể do pháp chế doanh nghiệp xác định.

### Vì sao lỗi ngầm xảy ra: KPI lệch nhau

| Bộ phận | KPI thường gặp | Hành vi hợp lý theo KPI | Lỗi ngầm với khách |
| --- | --- | --- | --- |
| Kho phụ tùng | Vòng quay tồn kho, ưu tiên triệu hồi | Điều linh kiện cho xe ưu tiên cao | Lịch hẹn của khách khác mất linh kiện (UC1) |
| Cố vấn dịch vụ | Số xe tiếp nhận, doanh thu dịch vụ | Ưu tiên khách đang đứng trước mặt | Lời hứa gọi lại bị quên (UC2) |
| Kỹ thuật viên | Giờ công, số xe hoàn thành | Đóng lệnh nhanh | Lỗi quay lại sau sửa (UC5) |
| Bảo hành hãng | Tỷ lệ claim hợp lệ, chi phí bảo hành | Trả về claim thiếu chứng từ | Xe nằm xưởng chờ (UC6) |
| CSKH | AHT, CSAT cuộc gọi | Kết thúc cuộc gọi nhanh, lịch sự | Không ai theo việc đến cùng |

Mỗi bộ phận đều làm đúng theo KPI của mình. Lỗi nằm ở chỗ **không ai có KPI "việc của khách đã thật sự xong"** — đó là vai trò promise keeper của agent, và là lý do metric Contacts per Job, Promise Kept Rate nên được báo cáo cấp liên phòng ban.
