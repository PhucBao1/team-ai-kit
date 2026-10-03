# 10 · Metrics & economics — Đo trải nghiệm khách trước, rồi mới đến vận hành

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Hàng đầu là chỉ số trải nghiệm khách (CX), tiếp theo là ràng buộc của đề, cuối cùng là chỉ số proactive và an toàn. Ngưỡng là **mục tiêu đề xuất** cho MVP, không phải kết quả đã đạt. Khảo sát CES/CSAT gộp vào tin nhắn kết thúc việc, không gửi riêng.

Customer Effort Score (CES)↑ vs holdout"Giải quyết việc này dễ hay khó?" — khảo sát 1 câu sau khi việc xongCX · TARGETCSAT sau can thiệp chủ động≥ 4,3 / 5đánh giá của khách với tin nhắn / phương án agent chủ động đưa raCX · TARGETContacts per Job↓ vs holdoutsố lần khách phải tự liên hệ cho một việc (sửa xe, claim, phí sạc)CX · FAILURE DEMANDService Retention Rate↑ vs holdoutkhách quay lại xưởng ủy quyền cho lần bảo dưỡng tiếp theo (điều kiện giữ bảo hành)GIÁ TRỊ · TARGETCopilot Acceptance Rate≥ 60%gợi ý của copilot được nhân viên dùng (có / không sửa)NIỀM TIN · TARGETRouting Accuracy≥ 90%yêu cầu đến đúng người / đúng mức khẩn ngay lần đầuTRIAGE · TARGETFirst-Time Fix Rate↑ vs holdoutxe sửa xong, không quay lại cùng lỗi trong 30 ngày / tổng xe sửaXƯỞNG · COPILOTParts-Ready Arrival≥ 90%xe đến xưởng đã có sẵn linh kiện dự kiến / lượt sửa cần linh kiệnXƯỞNG · COPILOTTime-to-Detect Emerging Issue↓ vs báo cáo thángtừ tín hiệu đầu tiên đến khi đội chất lượng nhận cảnh báo đã xác nhậnHÃNG · VoCTask Completion Rate≥ 85%tác vụ hoàn tất đúng (đặt lịch, tra cứu, tạo ticket…) / tác vụ khách yêu cầuHỘI THOẠI · TARGETGrounding Violation Rate0câu trả lời chứa chính sách / giá / trạng thái không có trong tool/KBRÀNG BUỘC ĐỀ · HARD GATEConfirmation Compliance100%hành động mức 2–3 có xác nhận hợp lệ trước khi ghiRÀNG BUỘC ĐỀ · HARD GATERe-ask Rate≤ 5%lần agent / nhân viên hỏi lại thông tin khách đã cung cấpHANDOFF · TARGETWasted Visit Rate↓ vs holdoutkhách đến xưởng nhưng không sửa được / tổng lượt hẹnPROACTIVE · UC1 · UC3Pre-Chase Recovery≥ 70%việc kẹt được xử lý trước khi khách phải liên hệ / việc kẹt thậtPROACTIVE · TARGETDetection Precision / Recall≥ 95% / ≥ 80%đo trên lỗi tiêm có nhãn trong giả lậpDETECTION · TARGETComeback Rate↓ vs holdoutxe báo lại cùng mã lỗi ≤ 30 ngày sau sửa (telematics)OUTCOME · UC6Unsafe Action Rate0ghi sai, vượt quyền, hoặc tư vấn ngoài luồng an toànSAFETY · HARD GATE

### Target đặt cạnh số thật của big enterprise

| Chỉ số | Tham chiếu công bố | Target đề xuất cho MVP |
| --- | --- | --- |
| Tự giải quyết không cần người | Salesforce Help: 76% · Klarna: ~2/3 ticket | Task Completion ≥ 85% cho *các tác vụ trong phạm vi* (hẹp hơn toàn bộ contact) |
| Tỷ lệ chuyển người | Salesforce Help: 5% | Không đặt mục tiêu thấp — chuyển đúng lúc quan trọng hơn chuyển ít |
| Thời gian xử lý của nhân viên | Bank of America EricaAssist: −1 phút / cuộc gọi | Đo với copilot CVDV ở Làn 1 |
| Thời gian chờ đặt lịch | Rivian: −35% (2025) | Đo Time-to-Recovery và Wasted Visit Rate |
| CSAT | Klarna: giảm khi tự động hoá quá nhanh | Không thấp hơn nhóm đối chứng — điều kiện cứng |

### Chi phí trên mỗi việc được giải quyết (ACRC)

```text
ACRC = (LLM + tool + hạ tầng)
       ÷ số việc được khôi phục & xác minh
```

Khớp xu hướng tính phí theo outcome 2026: chỉ tính khi việc được xác minh là xong.

### Giá trị ròng

```text
Net = contact tránh được + slot xưởng không lãng phí
    + comeback giảm − chi phí agent − chi phí can thiệp sai
```

Gartner khuyến nghị chuyển trọng tâm từ cắt giảm chi phí sang tạo giá trị (giữ chân, mua lại, trung thành) — vì vậy có Service Retention Rate. Gartner (8/2026) phân tích 432 use case AI CSKH: chỉ 25% có ROI dương, 42% không đo được ROI. Vì vậy avoided cost đo bằng **nhóm đối chứng** (5–10% việc kẹt rủi ro thấp xử lý theo quy trình cũ) — không bao giờ holdout case an toàn hay tiền.
