# 03.1 · Anchor case — "Tôi đã đặt lịch — đến xưởng lại bảo chưa có linh kiện"

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Lịch hẹn được xác nhận theo công suất xưởng. Linh kiện nằm ở một hệ thống khác. Khi linh kiện bị điều cho xe khác, lịch hẹn vẫn "đã xác nhận" — không hệ thống nào báo lỗi, vì mỗi hệ thống đều đúng theo góc nhìn của nó.

### Quy trình chuẩn (giả định)

```text
1. Xe báo mã lỗi / khách yêu cầu kiểm tra
2. Chẩn đoán sơ bộ → xác định linh kiện theo số khung
3. Đặt lịch theo công suất xưởng
4. Giữ linh kiện cho lệnh sửa chữa
5. Linh kiện có mặt trước ngày hẹn
6. Sửa, chạy thử, bàn giao
7. Theo dõi: mã lỗi không quay lại
```

### Vì sao bước 4 gãy

- Kho điều linh kiện cho xe ưu tiên cao hơn (ví dụ xe triệu hồi) mà không kiểm tra lịch hẹn.
- Hàng về trễ, ETA cập nhật trong ERP nhưng không sang hệ thống lịch.
- Giữ sai mã linh kiện so với đời xe.
- Khách tự đổi lịch trong app, giữ linh kiện vẫn ở ngày cũ.

Hệ quả: khách mất nửa ngày, slot xưởng lãng phí, và lần liên hệ tiếp theo là một lời phàn nàn.

### Service blueprint — UC1 hôm nay và với agent

|  | Nhận cảnh báo | Đặt lịch | Chờ đến ngày | ⚠ Linh kiện bị điều đi | Đến xưởng | Sau sửa |
| --- | --- | --- | --- | --- | --- | --- |
| **Khách làm gì** | Thấy đèn vàng, lo lắng | Gọi / đặt trong app | Sắp xếp nghỉ làm | *Không biết gì* | Đến xưởng | Lái xe, để ý đèn |
| **Điểm chạm** frontstage | Màn hình xe | App / tổng đài | Tin nhắc lịch | — → agent: tin 2 phương án | CVDV tiếp nhận | — → agent: hỏi thăm / comeback |
| **Phía sau** backstage | — | Điều phối xếp slot | Kho giữ linh kiện | Kho điều cho xe triệu hồi | CVDV phát hiện thiếu linh kiện | Không ai theo dõi |
| **Hệ thống** | Telematics | DMS | ERP kho | ERP ≠ DMS (lệch) | DMS | Telematics |
| **Cảm xúc khách** | Lo lắng | Yên tâm | Yên tâm | Yên tâm (chưa biết) | Bực hôm nay · được báo trước với agent | Lo lắng hôm nay · được theo dõi với agent |

Blueprint 4 tầng (hành động khách · điểm chạm · việc phía sau · hệ thống) là công cụ chuẩn của thiết kế dịch vụ. Điểm gãy nằm ở cột mà khách *không nhìn thấy* — vì vậy chỉ một agent nhìn được cả tầng hệ thống mới can thiệp kịp.
