# 03.1 · Anchor case — "Xe cảnh báo lặp lại, tôi chưa kịp làm gì — rồi đến xưởng lại bảo chưa có linh kiện"

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Hãng đã có kênh nhận mã lỗi từ xe (VinFast công bố cho VF e34 từ 05/2021: báo lỗi lên màn hình + app, khuyên mang xe tới xưởng), còn phần **sau khi báo** (nối cảnh báo với quyền lợi, lịch hẹn, người xử lý và kết quả sửa) là chỗ đội **giả thuyết** có thể bị đứt — *chưa kiểm chứng tại xưởng VinFast*. **Kịch bản giả lập để kiểm khả năng phục hồi:** linh kiện của một lịch đã xác nhận bị điều cho xe khác; nếu lịch và kho không nối với nhau thì lịch vẫn "đã xác nhận" tới khi khách tới nơi. VinFast đã công bố cam kết cấp phụ tùng trong 24 giờ từ 01/9/2024, nên đây là **ngoại lệ giả lập**, không phải tỷ lệ thực. Anchor case có **hai điểm gãy giả định**: cảnh báo lặp chưa được nối thành một việc chăm sóc (UC1 — cửa vào), và điều kiện của lịch đã đặt đổi sau khi khách xác nhận (nhánh lập lại của UC3). *(Sửa 06/10 sau review: bỏ các câu "không hệ thống nào nhìn thấy", "khách tự lo" vì chưa có bằng chứng; cần đồng bộ file HTML gốc.)*

### Quy trình giả định (cần kiểm chứng tại xưởng VinFast)

```text
1. Xe báo mã lỗi lần 1, 2, 3 — xe tự cảnh báo; chưa rõ có ai gom thành một việc chăm sóc
2. Khách để ý (hoặc không); tự đặt lịch / gọi hỏi
3. Chẩn đoán sơ bộ → xác định linh kiện theo số khung
4. Đặt lịch theo công suất xưởng
5. Giữ linh kiện cho lệnh sửa chữa
6. Linh kiện có mặt trước ngày hẹn
7. Sửa, chạy thử, bàn giao
8. Theo dõi sau sửa: mã lỗi có quay lại không, khách còn triệu chứng không
```

### Hai bước có thể gãy (giả thuyết — dùng cho kịch bản giả lập)

- **Bước 1:** tín hiệu lặp có thể chưa được nối với lịch sử sửa thành một việc có người giữ — chưa có số liệu VinFast.
- **Bước 5:** kho điều linh kiện cho xe ưu tiên cao hơn (ví dụ xe triệu hồi) mà không kiểm tra lịch hẹn.
- **Bước 5:** hàng về trễ, ETA cập nhật trong ERP nhưng không sang hệ thống lịch; giữ sai mã linh kiện so với đời xe; khách tự đổi lịch trong app, giữ linh kiện vẫn ở ngày cũ.

Hệ quả **nếu** gãy: khách mất một chuyến đi, slot xưởng lãng phí, lần liên hệ tiếp theo là lời phàn nàn. Với agent: UC1 báo trước ở bước 1; UC3 lập lại phương án ở bước 5; bước 8 theo dõi bằng dữ liệu xe khi **đủ dữ liệu** (A2.27) và hỏi khách còn triệu chứng (A2.23) — không gọi là "đã xác minh".

### Service blueprint — nhánh lập lại của UC3 (lịch đã đặt mất linh kiện): hôm nay và với agent

|  | Nhận cảnh báo | Đặt lịch | Chờ đến ngày | ⚠ Linh kiện bị điều đi | Đến xưởng | Sau sửa |
| --- | --- | --- | --- | --- | --- | --- |
| **Khách làm gì** | Thấy đèn vàng, lo lắng | Gọi / đặt trong app | Sắp xếp nghỉ làm | *Không biết gì* | Đến xưởng | Lái xe, để ý đèn |
| **Điểm chạm** frontstage | Màn hình xe | App / tổng đài | Tin nhắc lịch | — → agent: tin 2 phương án | CVDV tiếp nhận | — → agent: hỏi thăm / comeback |
| **Phía sau** backstage | — | Điều phối xếp slot | Kho giữ linh kiện | Kho điều cho xe triệu hồi *(giả lập)* | CVDV phát hiện thiếu linh kiện | Chưa rõ ai theo dõi *(cần kiểm chứng)* |
| **Hệ thống** | Telematics | DMS | ERP kho | ERP ≠ DMS (lệch) | DMS | Telematics |
| **Cảm xúc khách** | Lo lắng | Yên tâm | Yên tâm | Yên tâm (chưa biết) | Bực hôm nay · được báo trước với agent | Lo lắng hôm nay · được theo dõi với agent |

Blueprint 4 tầng (hành động khách · điểm chạm · việc phía sau · hệ thống) là công cụ chuẩn của thiết kế dịch vụ. Điểm gãy giả định nằm ở cột mà khách *không nhìn thấy* — agent nhìn được tầng hệ thống có thể can thiệp sớm hơn; hiệu quả cần đo so với quy trình hiện tại (cố vấn dịch vụ, app).
