# PL-A · 5 dạng lỗi & use cases — Năm dạng lỗi ngầm, sáu use case

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

T1

#### Lệch trạng thái

Hai hệ thống giữ hai sự thật khác nhau.

"Lịch nói có, kho nói không?"

UC1 · UC4

T2

#### Lời hứa bị quên

Cam kết trong hội thoại không có trong hệ thống.

"Ai hứa gì, hạn khi nào?"

UC2

T3

#### Rơi quyền sở hữu

Chuyển giao giữa bot, người, tổ chức bị mất.

"Việc này hiện ai chịu trách nhiệm?"

UC3 · UC6

T4

#### Đóng sớm

Hệ thống ghi "xong" nhưng vấn đề còn.

"Xe có báo lại cùng lỗi?"

UC5

T5

#### Trùng lặp

Một vấn đề thành nhiều case qua nhiều kênh.

"Những case này là một?"

Wave 3

| Use case | Dạng | Tín hiệu rõ | Cần LLM | Rủi ro ghi | Đo outcome | Thứ tự |
| --- | --- | --- | --- | --- | --- | --- |
| **UC1** Đến xưởng rồi phải về (lịch lệch kho) | T1 | ●●●●● | Trung bình (lập phương án) | Trung bình · khách xác nhận | ●●●●● | MVP |
| **UC3** Kẹt ở trạm sạc, không ai trả lời (handoff rơi) | T3 | ●●●●● | Gần như không | Thấp | ●●●●● | Quick win |
| **UC2** Chờ mãi không thấy gọi báo giá (lời hứa bị quên) | T2 | ●●●●● | Cao | Thấp | ●●●●● | Wave 2 |
| **UC5** Vừa sửa xong, đèn lỗi lại sáng (comeback) | T4 | ●●●●● | Trung bình | Trung bình | ●●●●● | Wave 2 |
| **UC6** Xe nằm xưởng, không ai nói vì sao (claim kẹt) | T3 | ●●●●● | Thấp | Thấp (nội bộ) | ●●●●● | Wave 3 |
| **UC4** Được miễn phí mà vẫn bị trừ tiền (billing lệch) | T1 | ●●●●● | Thấp–TB | Cao (tiền) | ●●●●● | Wave 3 · HITL |

**UC5** là điểm mạnh riêng của domain xe điện: outcome được xác minh bằng **dữ liệu thật của xe** (mã lỗi không quay lại), không chỉ dựa vào khảo sát khách.

Thời gian, token, tỷ lệ trong agent trace là minh hoạ (Illustrative). Quy trình nội bộ là giả định.
