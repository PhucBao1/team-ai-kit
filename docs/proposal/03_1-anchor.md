# 03.1 · Anchor case — "Xe cảnh báo lặp lại, tôi chưa kịp làm gì — rồi đến xưởng lại bảo chưa có linh kiện"

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Hãng đã có kênh nhận mã lỗi từ xe (VinFast công bố cho VF e34 từ 05/2021: báo lỗi lên màn hình + app, khuyên mang xe tới xưởng), nhưng phần **sau khi báo** vẫn để khách tự lo: tự đặt lịch, tự giục; và ngay cả khi lịch đã đặt, linh kiện nằm ở một hệ thống khác. *(Sửa 06/10: câu cũ "không hệ thống nào nhìn thấy chuỗi tín hiệu lặp" mâu thuẫn với tính năng VinFast đã công bố; cần đồng bộ lại file HTML gốc.)* Khi linh kiện bị điều cho xe khác, lịch hẹn vẫn "đã xác nhận" — không hệ thống nào báo lỗi, vì mỗi hệ thống đều đúng theo góc nhìn của nó. Anchor case có **hai điểm gãy**: friction đang hình thành mà không ai thấy (UC1), và điều kiện của lịch đã đặt đổi sau khi khách xác nhận (nhánh lập lại của UC3).

### Quy trình hôm nay (khách phải tự khởi xướng)

```text
1. Xe báo mã lỗi lần 1, 2, 3 — không ai gom lại
2. Khách để ý (hoặc không); tự đặt lịch / gọi hỏi
3. Chẩn đoán sơ bộ → xác định linh kiện theo số khung
4. Đặt lịch theo công suất xưởng
5. Giữ linh kiện cho lệnh sửa chữa
6. Linh kiện có mặt trước ngày hẹn
7. Sửa, chạy thử, bàn giao
8. Theo dõi: mã lỗi không quay lại
```

### Vì sao hai bước đó gãy

- **Bước 1:** tín hiệu lặp nằm trong telematics, không ai đếm và nối với lịch sử sửa — khách chỉ hành động khi đã khó chịu hoặc sát chuyến đi.
- **Bước 5:** kho điều linh kiện cho xe ưu tiên cao hơn (ví dụ xe triệu hồi) mà không kiểm tra lịch hẹn.
- **Bước 5:** hàng về trễ, ETA cập nhật trong ERP nhưng không sang hệ thống lịch; giữ sai mã linh kiện so với đời xe; khách tự đổi lịch trong app, giữ linh kiện vẫn ở ngày cũ.

Hệ quả: khách mất nửa ngày, slot xưởng lãng phí, và lần liên hệ tiếp theo là một lời phàn nàn. Với agent: UC1 báo trước ở bước 1; UC3 lập lại phương án ở bước 5; bước 8 được xác minh bằng dữ liệu xe.

### Service blueprint — nhánh lập lại của UC3 (lịch đã đặt mất linh kiện): hôm nay và với agent

|  | Nhận cảnh báo | Đặt lịch | Chờ đến ngày | ⚠ Linh kiện bị điều đi | Đến xưởng | Sau sửa |
| --- | --- | --- | --- | --- | --- | --- |
| **Khách làm gì** | Thấy đèn vàng, lo lắng | Gọi / đặt trong app | Sắp xếp nghỉ làm | *Không biết gì* | Đến xưởng | Lái xe, để ý đèn |
| **Điểm chạm** frontstage | Màn hình xe | App / tổng đài | Tin nhắc lịch | — → agent: tin 2 phương án | CVDV tiếp nhận | — → agent: hỏi thăm / comeback |
| **Phía sau** backstage | — | Điều phối xếp slot | Kho giữ linh kiện | Kho điều cho xe triệu hồi | CVDV phát hiện thiếu linh kiện | Không ai theo dõi |
| **Hệ thống** | Telematics | DMS | ERP kho | ERP ≠ DMS (lệch) | DMS | Telematics |
| **Cảm xúc khách** | Lo lắng | Yên tâm | Yên tâm | Yên tâm (chưa biết) | Bực hôm nay · được báo trước với agent | Lo lắng hôm nay · được theo dõi với agent |

Blueprint 4 tầng (hành động khách · điểm chạm · việc phía sau · hệ thống) là công cụ chuẩn của thiết kế dịch vụ. Điểm gãy nằm ở cột mà khách *không nhìn thấy* — vì vậy chỉ một agent nhìn được cả tầng hệ thống mới can thiệp kịp.
