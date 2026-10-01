# 11 · Dữ liệu & thế giới giả lập — Neo vào dữ liệu công khai thật, giả lập phần nội bộ

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Dữ liệu vận hành nội bộ (xe, xưởng, kho, bảo hành) không công khai ở bất kỳ doanh nghiệp nào, và Việt Nam chưa có dataset công khai về CSKH xe điện hay dữ liệu xe/trạm sạc. Cách làm: **chính sách thật của VinFast** làm knowledge base, **dữ liệu tiếng Việt** cho phần ngôn ngữ và hội thoại, **dataset quốc tế** cho tín hiệu (số liệu cảm biến không phụ thuộc ngôn ngữ), **phỏng vấn chủ xe Việt** cho kịch bản thật, và một thế giới giả lập có **lỗi tiêm có nhãn** để đo chất lượng.

### A. Thông tin công khai của VinFast / V-Green dùng trong KB

| Nội dung | Dùng cho | Nguồn |
| --- | --- | --- |
| Chính sách bảo hành theo dòng xe, loại hình sử dụng, loại trừ, nghĩa vụ chủ xe | KB bảo hành; rule kiểm tra điều kiện sơ bộ | [vinfastauto.com](https://vinfastauto.com/vn_vi/thong-tin-bao-hanh) |
| Lịch bảo dưỡng (1.000 km/1 tháng; 5.000 km/6 tháng), nhắc trước 10 ngày, kênh đặt lịch, tổng đài | KB bảo dưỡng; detector nhắc theo odometer | [vinfastauto.com](https://vinfastauto.com/vn_vi/lich-bao-duong-xe-vinfast) |
| Miễn phí sạc đến 30/6/2027 cho khách cá nhân; chính sách riêng cho xe kinh doanh vận tải | KB sạc có phiên bản; UC4 | [vinfastauto.com](https://vinfastauto.com/vn_vi/vinfast-mien-phi-sac-pin-cho-tat-ca-o-to-dien-den-ngay-30062027) |
| Triệu hồi 5/2024: 2.097 xe, 3 nhóm lỗi, khung thời gian thực hiện | Kịch bản chiến dịch triệu hồi; xung đột kho giữa triệu hồi và sửa chữa thường | [vinfastauto.com](https://vinfastauto.com/vn_vi/vinfast-trieu-hoi-2097-o-to-de-kiem-tra-va-thay-the-linh-kien-mien-phi) |
| Hạ tầng V-Green: siêu trạm 150 kW, CCS2 | Cấu hình trạm sạc giả lập | [VnExpress](https://vnexpress.net/99-sieu-tram-sac-v-green-buoc-tien-cua-ha-tang-xe-dien-5053027.html) |
| Ứng dụng VinFast cho ô tô điện: pin & trạng thái sạc, trạng thái / vị trí từ xa, đặt lịch xưởng & dịch vụ lưu động, theo dõi tiến độ sửa, E-call, cập nhật phần mềm từ xa (FOTA) | Xác định dữ liệu xe nào là thật / khả thi; phương án "dịch vụ lưu động" và "cập nhật từ xa" trong luồng 6 quyết định | [vinfastauto.com](https://vinfastauto.com/vn_vi/cau-hoi-thuong-gap/cau-hoi-xe-o-to/san-pham/ung-dung-vinfast) · [hướng dẫn FOTA](https://vinfast.vn/huong-dan-cap-nhat-phan-mem-tu-xa-fota-cho-vf-8/) |
| Hồ sơ triệu hồi & khiếu nại VinFast tại Mỹ | Văn bản khiếu nại thật để xây intent & kịch bản | [NHTSA](https://www.nhtsa.gov/nhtsa-datasets-and-apis) |

Mỗi tài liệu KB lưu kèm URL, ngày truy cập và ngày hiệu lực. Chính sách thay đổi thường xuyên — chính vì vậy agent không được trả lời từ trí nhớ của LLM.

### B. Dữ liệu tiếng Việt — phần ngôn ngữ và hội thoại

| Dataset | Là gì | Dùng cho | Lưu ý |
| --- | --- | --- | --- |
| [CSConDa](https://huggingface.co/datasets/ura-hcmut/Vietnamese-Customer-Support-QA) (ĐH Bách khoa TP.HCM) | Hơn 9.000 cặp hỏi–đáp từ tương tác thật giữa khách và nhân viên tư vấn của một công ty phần mềm Việt Nam | Cách khách Việt thật sự hỏi; bộ đánh giá giọng văn CSKH tiếng Việt | Domain phần mềm · Apache 2.0 |
| [UIT-ViOCD](https://huggingface.co/datasets/tarudesu/ViOCD) (ĐH CNTT, ĐHQG TP.HCM) | 5.485 đánh giá thương mại điện tử gán nhãn khiếu nại / không khiếu nại | Bộ phát hiện "khách đang bực" — một tín hiệu chuyển người | Chỉ dùng cho nghiên cứu |
| [PhoATIS](https://github.com/VinAIResearch/JointIDSF) · [PhoATIS_Disfluency](https://github.com/VinAIResearch/PhoATIS_Disfluency) (VinAI) | Intent + slot tiếng Việt; bản có lời nói ấp úng, sửa lời | Khuôn gán nhãn intent/slot cho domain xe điện; bản disfluency cho kênh tổng đài (giọng nói → văn bản) | Domain chuyến bay · dữ liệu của VinAI, trong hệ sinh thái Vingroup |
| [5CD-AI E-commerce Multi-turn Chat](https://huggingface.co/datasets/5CD-AI/Vietnamese-Ecommerce-Multi-turn-Chat) | ~1.500 hội thoại nhiều lượt tiếng Việt về sản phẩm | Mẫu định dạng hội thoại nhiều lượt | Có vẻ là dữ liệu sinh tự động |
| [UIT NLP datasets](https://nlp.uit.edu.vn/datasets/) | Nhiều bộ tiếng Việt về cảm xúc, phản hồi, hỏi đáp | Phân tích cảm xúc tiêu cực trong hội thoại | Kiểm tra giấy phép từng bộ |
| [Bud500](https://huggingface.co/datasets/linhtran92/viet_bud500) | Dữ liệu giọng nói tiếng Việt | Chỉ khi demo kênh tổng đài | Tuỳ chọn |

### C. Nguồn Việt Nam về xe điện — để đọc và dựng kịch bản

| Nguồn | Dùng cho | Lưu ý |
| --- | --- | --- |
| [Diễn đàn Cộng đồng VinFast](https://vinfast.vn/dien-dan/thao-luan/cach-su-dung-he-thong-den-xe-o-to/) (vinfast.vn) | Câu hỏi thật của chủ xe Việt về đèn cảnh báo, sạc, bảo dưỡng → danh sách intent và cách diễn đạt | Chỉ đọc để rút intent; không thu thập dữ liệu cá nhân; tuân thủ điều khoản trang |
| [Tài liệu hướng dẫn sử dụng VinFast](https://vinfastauto.com/vn_en/tai-lieu-xe-may-dien) | Công khai cho xe máy điện; nếu có sổ tay ô tô với mục đèn cảnh báo → thay KB mã lỗi giả định bằng nội dung thật | Chưa tìm thấy bản ô tô tải công khai |
| [Cục Đăng kiểm Việt Nam](https://www.vr.org.vn/Pages/thong-bao.aspx?Category=7) | Thông báo chính thức, bao gồm triệu hồi → kịch bản chiến dịch triệu hồi tại Việt Nam | Cần kiểm tra trực tiếp trên cổng |

### D. Dataset quốc tế cho tín hiệu

| Dataset | Dùng để | Hạn chế |
| --- | --- | --- |
| [VED — Vehicle Energy Dataset](https://github.com/gsoh/VED) | Hành trình, năng lượng, odometer thật → luồng telematics; tiêm mã lỗi lên trên | Dữ liệu Mỹ, trộn nhiều loại xe, không có mã lỗi |
| [ACN-Data](https://ev.caltech.edu/dataset) (Caltech) | Phiên sạc thật (giờ, kWh) → CSMS giả lập; tiêm phiên lỗi / tính phí sai | Trạm sạc nơi làm việc ở Mỹ |
| [Bitext customer support](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset) | Khung intent CSKH và biến thể diễn đạt | Tiếng Anh, một lượt |
| [τ²-bench](https://github.com/sierra-research/tau2-bench) | Khuôn môi trường tool + khách ảo + chấm điểm agent nhiều bước | Domain khác; dựng lại cho xe điện |

### E. Phỏng vấn chủ xe — dữ liệu Việt Nam "thật" nhất

Phỏng vấn **5–10 chủ ô tô điện** và, nếu được, **1–2 cố vấn dịch vụ** (15–20 phút mỗi người). Mười câu chuyện thật của khách Việt thuyết phục ban giám khảo hơn mọi dataset nước ngoài, và thay được các con số giả định trong bài.

- Kết quả dùng để: xác nhận 6 use case có thật, xếp lại thứ tự ưu tiên, lấy câu nói thật cho phần "Khách trải qua", và viết kịch bản đánh giá.
- Ẩn danh hoá; xin đồng ý trước khi ghi âm hoặc trích dẫn.
- Không hỏi thông tin định danh, biển số, số khung.
```text
BỘ CÂU HỎI GỢI Ý
Chủ xe
 1. Lần gần nhất anh/chị phải liên hệ hãng
    hoặc xưởng là vì việc gì?
 2. Anh/chị có phải hỏi lại, đi giục, hoặc
    kể lại từ đầu không? Mấy lần?
 3. Có lần nào đến xưởng mà không sửa được?
 4. Có điều gì anh/chị mong được báo trước?
 5. Nếu hãng nhắn chủ động, điều gì làm
    anh/chị thấy phiền?
Cố vấn dịch vụ
 6. Việc gì tốn thời gian nhất mà khách
    không nhìn thấy?
 7. Khi nào khách bực nhất khi đến xưởng?
```

### F. Thế giới giả lập (đề xuất)

| Thực thể | Quy mô | Chi tiết |
| --- | --- | --- |
| Chủ xe & xe | 150 chủ · 200 xe | VF 3/5/6/7/8/9; ~10% kinh doanh vận tải; một số chủ có 2 xe; một số xe đã sang tên |
| Xưởng dịch vụ | 5 xưởng | Công suất theo giờ, kỹ thuật viên có / không chứng chỉ pin cao áp, giờ làm |
| Kho phụ tùng | 60 mã linh kiện | Tồn kho theo xưởng, ETA, điều chuyển, ưu tiên xe triệu hồi |
| Trạm sạc | 40 trạm · 300 trụ | Trạng thái kiểu OCPP (Available / Charging / Faulted), phiên sạc từ ACN-Data |
| Luồng telematics | Từ VED | Odometer, SoC, vị trí (có đồng ý) + mã lỗi tiêm theo knowledge graph |
| Hội thoại tiếng Việt | ~300 kịch bản | Sinh bằng LLM từ câu chuyện phỏng vấn, câu hỏi trên diễn đàn VinFast, CSConDa và khiếu nại NHTSA đã bản địa hoá; người review; biến thể không dấu, viết tắt |
| **Lỗi tiêm có nhãn** | ~8% việc đang chạy | T1–T5 với ground truth → đo precision / recall thật; kèm case "không nên can thiệp" |

### G. Phối hợp các nguồn

| Phần của hệ thống | Nguồn |
| --- | --- |
| Tín hiệu xe, phiên sạc | VED, ACN-Data (quốc tế) + giả lập |
| Chính sách, knowledge base | VinFast / V-Green (Việt Nam, công khai) |
| Cách khách Việt hỏi và phàn nàn | Phỏng vấn chủ xe, diễn đàn VinFast, CSConDa |
| Phát hiện khách bực / khiếu nại | UIT-ViOCD |
| Nhãn intent / slot | PhoATIS làm khuôn, tự gán nhãn cho domain xe điện |
| Hội thoại đánh giá | Sinh từ các nguồn trên, người review, có biến thể không dấu |

Lợi thế của giả lập có nhãn: dữ liệu thật của doanh nghiệp không có sẵn nhãn "case này kẹt thật". Ở đây mỗi lỗi được tiêm có đáp án, nên chất lượng phát hiện đo được ngay từ tuần đầu.
