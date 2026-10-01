# 46 · Rủi ro & dự phòng — Chuẩn bị cho những gì chắc chắn sẽ trục trặc

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Rủi ro | Dấu hiệu | Dự phòng |
| --- | --- | --- |
| LLM chậm hoặc lỗi khi demo | Phản hồi > 5 giây | Model nhanh cho hội thoại; timeout + thông báo lịch sự; **video dự phòng** |
| Agent gọi sai tool / sai thứ tự | Kịch bản tay fail | Mô tả tool rõ hơn; ép bước bằng code (ví dụ: book chỉ nhận option_id vừa sinh) |
| Tiếng Việt thiếu tự nhiên | Người đọc thấy gượng | Mẫu tin cho tin chủ động; LLM chỉ điền vào chỗ trống |
| Quota / billing GCP | Lỗi 429 / 403 | Bật billing và xin quota tối 27/9; key dự phòng của nhà cung cấp khác sau cùng interface |
| Tích hợp FE–BE trễ | C vẫn dùng mock chiều 29/9 | API contract chốt sáng 28/9; D ưu tiên các endpoint C cần |
| Phạm vi phình to | Ai đó làm việc không có trong §43 | Luật cắt 21:00; mọi thứ ngoài danh sách đưa vào backlog tuần 1 |
| Dữ liệu thật / cá nhân | — | MVP chỉ dùng dữ liệu giả lập; không đưa dữ liệu khách thật vào bất kỳ đâu |

### Checklist GCP tối nay

```text
gcloud projects create ev-cx-agent-demo
gcloud billing projects link ev-cx-agent-demo --billing-account=XXXX
gcloud services enable run.googleapis.com sqladmin.googleapis.com \
    secretmanager.googleapis.com artifactregistry.googleapis.com \
    aiplatform.googleapis.com cloudbuild.googleapis.com
# tuần 1: pubsub.googleapis.com cloudtrace.googleapis.com
# chọn region gần nhất có đủ dịch vụ (ví dụ asia-southeast1); kiểm tra model khả dụng ở region đó
# mỗi người: service account riêng cho dev, không commit key — dùng Secret Manager / ADC
```Dữ liệu định danh thật (khi có) phải tuân thủ quy định bảo vệ dữ liệu cá nhân của Việt Nam — hiện chưa có region GCP tại Việt Nam. MVP và bản 14/10 chỉ dùng dữ liệu giả lập nên không vướng; kiến trúc production giữ dữ liệu định danh trong nước (xem proposal §PL-D).
