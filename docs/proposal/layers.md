# PL-C · Ba lớp: khách · xưởng · hãng — Không chỉ cứu việc bị kẹt — ngăn nó xảy ra, và đưa bài học về sản phẩm

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Agent CSKH chủ động là lõi. Hai trụ cột bổ trợ dùng chung Journey State Graph, KB và governance, nhưng phục vụ hai đối tượng khác: kỹ thuật viên ở xưởng và đội chất lượng / sản phẩm ở hãng.

```text
KHÁCH   ── Agent CSKH chủ động (lõi)   phát hiện & xử lý trước khi khách phải hỏi
              │  tín hiệu, lịch hẹn, mã lỗi, lời kể của khách
              ▼
XƯỞNG   ── Copilot kỹ thuật viên        chẩn đoán trước khi xe đến · sửa đúng ngay lần đầu
              │  kết quả sửa, comeback, linh kiện thay, thời gian
              ▼
HÃNG    ── Insights / VoC agent          vấn đề lặp lại theo dòng xe, lô xe, chính sách
              │  bài học → KB, SOP, chất lượng sản phẩm, tính năng app
              └──────────────► quay lại lớp KHÁCH (ít lỗi hơn, trả lời đúng hơn)
```

### Trụ cột 2 — Copilot kỹ thuật viên

**Vấn đề nghiệp vụ:** kỹ thuật viên chẩn đoán xe điện phải đọc log mã lỗi, lịch sử xe, tài liệu sửa chữa và thông báo kỹ thuật của hãng ở nhiều nơi. Chẩn đoán lâu hoặc sai → xe nằm xưởng lâu, thay nhầm linh kiện, lỗi quay lại (UC6).

**Điểm nối với lõi:** khi xe báo mã lỗi và khách đặt lịch, copilot **chẩn đoán sơ bộ trước khi xe đến** → dự đoán linh kiện cần → giữ linh kiện sớm. Đây là cách ngăn friction từ gốc (UC1) thay vì chỉ cứu khi đã lệch (nhánh lập lại UC3).

| Thành phần | Nội dung |
| --- | --- |
| Đầu vào | Log mã lỗi + dữ liệu lúc xảy ra lỗi, odometer, lịch sử sửa chữa của xe, tài liệu sửa chữa, thông báo kỹ thuật, các ca tương tự đã sửa thành công |
| Đầu ra | Quy trình chẩn đoán gợi ý theo thứ tự khả năng, linh kiện dự kiến, cảnh báo "xe này từng sửa hạng mục này 20 ngày trước" |
| Guardrail | Mọi bước trích đúng mục tài liệu chính thức; hạng mục pin cao áp chỉ theo quy trình hãng, chỉ kỹ thuật viên có chứng chỉ; kỹ thuật viên quyết định, copilot không tự đóng lệnh |
| Chỉ số | First-Time Fix Rate, thời gian chẩn đoán, comeback 30 ngày, tỷ lệ xe đến xưởng đã có sẵn linh kiện |

### Trụ cột 3 — Insights / VoC agent

**Vấn đề nghiệp vụ:** dữ liệu CSKH, xưởng và xe nằm rời rạc; vấn đề chất lượng mới nổi (một linh kiện, một lô xe, một bản cập nhật phần mềm) thường được nhận ra muộn, sau khi đã thành làn sóng khiếu nại.

**Giá trị với lãnh đạo hãng:** CSKH không chỉ là chi phí mà là **cảm biến chất lượng sản phẩm** — tín hiệu đến sớm hơn báo cáo bảo hành hàng tháng.

| Thành phần | Nội dung |
| --- | --- |
| Đầu vào | Lý do liên hệ đã gắn nhãn, tần suất mã lỗi theo dòng xe / đời xe / giai đoạn sản xuất, comeback, claim bảo hành, câu hỏi về chính sách |
| Đầu ra | Bản tin hằng tuần: vấn đề mới nổi kèm bằng chứng và mức tin cậy; điều khoản chính sách bị hiểu sai nhiều nhất; xưởng / hạng mục có comeback cao |
| Guardrail | Chỉ dữ liệu tổng hợp, ẩn danh; ngưỡng thống kê trước khi cảnh báo; chuyên viên phân tích xác nhận; agent **không** đề xuất hay quyết định triệu hồi — chỉ cung cấp tín hiệu |
| Chỉ số | Thời gian phát hiện vấn đề mới nổi, tỷ lệ cảnh báo được xác nhận, mức giảm contact theo chủ đề sau khi sửa |

**Không làm lại workflow:** hai trụ cột dùng chung Decision Engine, Journey State Graph, KB, tool gateway và governance. Copilot kỹ thuật viên là một bề mặt mới ở trạng thái 2 và 7 của lệnh sửa chữa; Insights agent tiêu thụ đầu ra của bước Learn. Vòng Perceive → Understand → Decide → Act → Verify → Learn giữ nguyên.
