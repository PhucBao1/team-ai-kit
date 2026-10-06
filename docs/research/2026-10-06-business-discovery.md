# Business discovery lại từ đầu — 06/10/2026

> Người làm: A (lead) cùng AI coding agent, phương pháp Next Move Theory (skill `nmt-market-research`, Deep mode).
> Báo cáo đầy đủ (HTML, 3 tầng, có nguồn): [2026-10-06-business-discovery-report.html](2026-10-06-business-discovery-report.html).
> Đây là nghiên cứu bàn giấy: **không có phỏng vấn, log tổng đài hay văn bản gốc đề BTC** — mọi tần suất là giả thuyết.
> Quyết định phạm vi rút ra: `plan/PLAN.md` mục "Bổ sung 06/10" · card A2.20–A2.24.

## 1. Kết luận: NARROW

Đề BTC đúng chỗ, nhưng proposal và report trước kéo bài toán ra xa khỏi chỗ có bằng chứng. Pain còn bằng chứng là **ca hậu mãi không xong trong một lần**:

- **P-A — chuyển rồi không ai giữ việc:** yêu cầu bị "chuyển bộ phận" không có người giữ, không có hạn; khách tự giục, kể lại.
- **P-B — không chắc quyền lợi đúng cho xe mình:** chính sách đổi nhiều lần theo ngày mua (bỏ hỗ trợ xe nằm xưởng 01/01/2025, dừng thuê pin 01/3/2025, chu kỳ bảo dưỡng 01/01/2026, sạc miễn phí 10/02/2026).

Hai pain này trùng lõi bắt buộc của đề (hội thoại nhiều bước, KB có trích dẫn, tool, chuyển người kèm tóm tắt, không bịa, xác nhận).
**Rủi ro quyết định:** phần lớn liên hệ có thể là ca đơn giản app + tổng đài đã xử lý tốt — chưa đo được.

## 2. Bằng chứng chính

| Bằng chứng | Nguồn |
|---|---|
| VinFast số hoá 92% và cơ sở vật chất 94% ở trải nghiệm bán hàng (p13, có nhãn). Bảng dịch vụ (p21): dòng số hoá 92% có kỹ thuật 70%, giá trị dịch vụ 64% — nhiều khả năng VinFast, **cần mở PDF xác nhận nhãn**. Nhiều hãng: chi phí 72%, chờ lâu 65%, upsell không cần thiết 46%, giao tiếp kém trong lúc dịch vụ 36% (p19); 78% dùng / định dùng xưởng ngoài (p22) | [InsightAsia 2025 công khai](https://insightasia.com/vietnam-automotive-customer-satisfaction-report/), n=762, khảo sát 12/2024–3/2025 |
| ~~PDF "InsightAsia 2026", n=1.247~~ do lead cung cấp — **không dùng số liệu**: không có bản công khai, trùng câu trích với bản 2025 nhưng khác số, tự mâu thuẫn | — |
| Ca VF9: chờ sửa bảo hành lâu; VinFast cho nghỉ 4 nhân sự vì "chậm trễ tiếp nhận và xử lý yêu cầu"; 2/10 comment chê "phải phàn nàn công khai mới được xử lý" | [otosaigon 12/10/2024](https://www.otosaigon.com/threads/vinfast-xu-ly-the-nao-khi-chu-xe-vf9-phan-anh-cho-doi-lau-trong-thoi-gian-sua-chua-bao-hanh.10025287/) |
| AI xử lý trọn 91% cuộc gọi dịch vụ, nhưng **56% lần chuyển AI → người thất bại** | Pied Piper 2025 (2.105 đại lý Mỹ) |
| 64% khách không muốn doanh nghiệp dùng AI trong CSKH; nỗi sợ số 1: khó gặp người | Gartner 07/2024 (n=5.728) |
| Doanh nghiệp chịu trách nhiệm cho chính sách chatbot bịa | Moffatt v. Air Canada, 02/2024 |
| VinFast đã công bố chẩn đoán từ xa VF e34: xe gửi mã lỗi về trung tâm bảo hành, báo lên màn hình + app, nhắc bảo dưỡng | [bài đăng lại 19/05/2021](https://vinfastdienchau.vn/news/tinh-nang-ho-tro-cham-soc-khach-hang-tu-dong-tu-xa-cua-vinfast-vf-e34/) |
| VinFast đã có giao nhận xe tận nhà, cứu hộ 24/7, mượn xe miễn phí | [VTV 27/11/2025](https://vtv.vn/giao-nhan-xe-tan-nha-cuu-ho-24-7-muon-xe-mien-phi-hau-mai-vinfast-tao-su-khac-biet-tren-thi-truong-100251127182754514.htm) |
| Lỗi KB của chính đội: sạc miễn phí còn ghi "đến 30/6/2027" (đã bị thay 09/02/2026); bảo hành VF 7 mâu thuẫn giữa các nguồn | báo cáo mục "Cập nhật 06/10" · card A2.20, A2.21 |

## 3. Pain bị loại hoặc hạ ưu tiên (kill test)

| Pain | Lý do loại |
|---|---|
| UC4 hoá đơn sạc / thuê pin sai | Không tìm thấy tranh chấp nào |
| Upsell / bán kèm | **Quyết định phạm vi** (đề không yêu cầu) — không phải bị bác bỏ; số phàn nàn 24% chỉ giảm ưu tiên |
| UC6 lỗi tái phát (vai trò pain cốt lõi) | Chỉ đoạn trích diễn đàn, không tần suất |
| Đến xưởng thiếu linh kiện (UC3, anchor cũ) | Bằng chứng 2025–26 yếu; VinFast cam kết phụ tùng 24 giờ từ 01/9/2024 |
| Thiếu kênh đặt lịch / theo dõi | **Hạ ưu tiên**: app VinFast đã có đặt lịch, duyệt báo giá, thời gian dự kiến; chưa biết ngoại lệ (lịch hỏng, tiến độ sai) được xử lý tốt tới đâu |
| Trạm sạc hỏng / xếp hàng | Gốc rễ hạ tầng, theo mùa; app V-Green có trạng thái real-time |
| Tay nghề kỹ thuật ở tỉnh | Có thật nhưng agent CSKH không giải được |

## 4. Điểm khác biệt

**(A) Giả thuyết khoảng trống — chưa tìm thấy ai làm** (≈20 lượt search, nhiều nguồn bị chặn, chưa thử kênh VinFast → **cần kiểm chứng**, không pitch là "chưa ai làm"):

| # | Điểm | Repo hiện có |
|---|---|---|
| A1 | Trả lời quyền lợi theo "xe này + hôm nay" (bảo hành, sạc, pin, chương trình còn hạn) có trích dẫn | Một phần → A2.20, A2.21 |
| A2 | Khách chụp ảnh đèn taplo, đối chiếu mã lỗi thật của xe | Chưa — roadmap |
| A3 | Theo dõi sau sửa bằng dữ liệu xe; chỉ gọi là *xác minh* khi dữ liệu đầy đủ + xe đã chạy lại + khách xác nhận hết triệu chứng (không có mã lỗi mới là chưa đủ) | Một phần (`post_repair`) → A2.23 làm bước trung thực "đã theo dõi, chưa thấy lỗi" |
| A4 | Một người giữ ca xuyên công ty Vingroup (VinFast · V-Green · Xanh SM) | Chưa — roadmap |
| A5 | AI agent xử lý trọn ca trên Zalo (Toyota VN mới đặt lịch qua Zalo bằng nhân viên) | Chưa (Zalo chỉ là trường dữ liệu) — roadmap |

**Đã loại khỏi "unique" vì có người làm:** phát hiện lỗi + báo khách (VinFast 2021, Tesla, GM, BMW, Rivian) · hỏi lại sau cảnh báo (Tesla app) ·
người giữ ca bằng nhân viên (NIO) · cảnh báo bão (Tesla) · đặt lịch qua Zalo (Toyota VN).

**(B) Người khác có, đội chưa có:** giao nhận / xe mượn qua agent (VinFast đã có dịch vụ → A2.24) · một người chịu trách nhiệm ca + hạn (NIO) ·
gọi điện bằng AI · ảnh / video kiểm tra kèm báo giá (myKaarma, Xtime) · sức khoẻ pin (Tesla 2024.20) · cảnh báo thời tiết · gửi linh kiện trước · khảo sát sau dịch vụ · thanh toán trong tin nhắn.

**Định vị (chốt 06/10):** *"Cố vấn hậu mãi chủ động: phát hiện nhu cầu từ dữ liệu xe, điều phối dịch vụ và theo việc tới kết quả bằng bằng chứng — biết việc nào đang kẹt, ai chịu trách nhiệm, điều gì đã được xác nhận và khi nào chưa đủ dữ liệu để kết luận."* Không nói "các hãng khác chưa có".
Proactive (UC1 → UC3) giữ làm **cửa vào**, không pitch là năng lực mới.

## 5. Còn thiếu để kết luận chắc hơn

1. Văn bản gốc đề BTC + rubric chấm.
2. **Tần suất:** xin mentor/BTC số lượt liên hệ theo lý do (log tổng đài) — đây là nguồn duy nhất đo được tỷ lệ.
3. **Cơ chế + thiệt hại:** đọc ~150 bài / review (group Facebook copy tay) và phỏng vấn — dùng để tìm tình huống, chỗ gãy, khách mất gì; **không** dùng mẫu này để đo tần suất hay đặt ngưỡng bỏ hướng (mẫu thiên về người đang bực).
4. Gọi thử tổng đài 5 câu hỏi chính sách × 2 lần — cho biết kênh có thể trả lời sai / chậm hay không, không đo tỷ lệ.
5. 8 phỏng vấn chủ xe vừa có ca sửa / bảo hành + 2–3 nhân viên CSKH (hỏi chuyện đã xảy ra) — để hiểu cơ chế, không đo mức phổ biến.
6. Hỏi mentor: app / tổng đài VinFast hiện làm được tới đâu với A1, A5, giao nhận xe.

> **Sửa sau review 06/10:** số liệu khảo sát đổi sang InsightAsia 2025 công khai (PDF 2026 chưa xác minh); bỏ ngưỡng 20% và 3/8; "khoảng trống" là giả thuyết;
> điểm số hoá cao chỉ giảm ưu tiên hướng đặt lịch; upsell bỏ vì phạm vi; mã lỗi và ngưỡng demo là giả lập; "xác minh sau sửa" cần dữ liệu đầy đủ + xe chạy lại + khách xác nhận.
