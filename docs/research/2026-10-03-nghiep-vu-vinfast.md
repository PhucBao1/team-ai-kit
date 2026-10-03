# Rà nghiệp vụ VinFast + so sánh hãng nước ngoài — 03/10/2026

> Người rà: A (lead) cùng AI coding agent. Nguồn truy cập ngày **03/10/2026** (danh sách cuối file). Dữ liệu dự án là
> GIẢ LẬP; mục đích là để luật nghiệp vụ trong giả lập **khớp thực tế công khai**, không đại diện quy trình nội bộ VinFast.
> Kết luận dùng cho: `plan/PLAN.md` (phạm vi "UC1 làm gọn"), card A2.18–A2.19, B2.17–B2.19, C2.14, D2.15–D2.16,
> mục "Bổ sung 3/10" của D2.01, và PR sửa nghiệp vụ trong P-073 (`a/w2-business-fixes`).

## 1. Sai sót nghiệp vụ tìm thấy trong P-073 (develop ngày 03/10)

| # | Mức | Vấn đề trong code / dữ liệu | Thực tế (nguồn) | Ảnh hưởng | Cách sửa · ai |
|---|---|---|---|---|---|
| 1 | Cao | Lịch bảo dưỡng trong fixture + hằng số `src/core/warranty.py` = 1.000 km / 1 tháng rồi 5.000 km / 6 tháng — đây là lịch **xe máy điện** | Ô tô (VF 8): **12.000 km hoặc 12 tháng**, điều kiện nào đến trước [V2][V3] | `warranty_precheck` xét "lỡ kỳ bảo dưỡng" sai; KB không trả lời được chu kỳ bảo dưỡng ô tô | Lịch bảo dưỡng lấy từ dữ liệu chính sách (không hard-code), fixture theo 12 tháng / 12.000 km — **lead sửa** (PR P-073); KB lịch ô tô — **B2.18** |
| 2 | Cao | Agent đề xuất **cập nhật phần mềm từ xa** cho VF6-2290 khi pin **3 %** | FOTA VinFast cần: xe bật nguồn, về N, đỗ có phanh tay, **SoC > 20 %**, ắc quy 12 V ≥ 12,3 V, **không đang sạc** [V4] | Đề xuất việc không thể làm ngay trong kịch bản demo | Agent: SoC ≤ 20 % → hướng dẫn sạc trước (sạc lưu động 24/7) — **lead sửa**; validator `trigger_remote_update` kiểm các điều kiện — **D2.01 (bổ sung)** |
| 3 | Cao (pháp lý) | `Customer.consent_vehicle_data` **mặc định True** | NĐ 13/2023: **im lặng / không phản hồi không phải là đồng ý**; đồng ý phải kiểm chứng được [L1] | Tin chủ động dựa trên dữ liệu xe khi chưa có đồng ý | Mặc định False, fixture ghi rõ khách demo đã đồng ý — **lead sửa** |
| 4 | Trung bình | Bảo hành không phân biệt **pin mua / pin thuê** | Pin thuê không thuộc bảo hành xe, theo hợp đồng thuê pin; pin mua có chế độ bảo hành pin riêng [V1] | Mã lỗi hệ thống pin (BATT-COOL-01) có thể báo "đủ điều kiện sơ bộ" sai | `Vehicle.battery_ownership` — **B2.18**; `core.warranty` xử lý — **D2.15** |
| 5 | Trung bình | Mẫu tin an toàn chỉ có "gọi 114" | Hướng dẫn EV: rời xe, đứng **đầu gió, chỗ cao hơn**, **không tự dập lửa**, không quay lại xe [S1][S2]; VinFast có cứu hộ **24/7 — 1900 23 23 89** [V5][V6] | Thiếu ý an toàn quan trọng; không dẫn kênh chính thức của hãng | Mẫu v2 (lead duyệt câu chữ) — **lead sửa** |
| 6 | Thấp | Thời hạn bảo hành **pin** chưa thống nhất (fixture ghi "8 năm là pin" cho VF 3/5/6/7; một nguồn tổng hợp nói pin mua đứt 10 năm không giới hạn km) | Trang chính thức chặn truy cập tự động (HTTP 403) → **chưa xác nhận** [V1] | Agent có thể nói sai thời hạn pin | Mở trang bằng trình duyệt, ghi ngày truy cập vào KB — **B2.18** |
| 7 | Thấp | Ticket khiếu nại chưa có hạn theo luật | Luật BVQLNTD 2023 (hiệu lực 01/7/2024): doanh nghiệp **thông báo đã tiếp nhận khiếu nại trong 3 ngày làm việc** [L3] | `create_ticket` (D2.01) chưa có | Ticket loại khiếu nại `sla_due_at` ≤ 3 ngày làm việc — **D2.01 (bổ sung)** |
| 8 | Thấp | SLA chuyển người lệch: card của agent 15' / 5', tool của D theo cảm xúc (2 h / 1 h / 30' / 15') | Proposal §08: "CVDV gọi anh trong 15 phút" | Hai luật khác nhau cho cùng một lời hứa với khách | Một bảng SLA thuần trong `src/core/sla.py` (15' thường, 5' an toàn) — **lead sửa** |

**Đã đúng:** bảo hành xe VF 8 / VF 9 **10 năm / 200.000 km**, VF 3 / 5 / 6 / 7 **7 năm / 160.000 km** [V1] (fixture đã sửa
ngày 02/10) · chỉ nói "đủ điều kiện **sơ bộ**" · luôn tự giới thiệu là AI — đúng Luật Trí tuệ nhân tạo 2025 (hiệu lực
01/3/2026: người dùng phải nhận biết đang tương tác với AI) [L2] · gợi ý dịch vụ lưu động / cứu hộ khi pin không đủ đi tới
xưởng — VinFast có cứu hộ và sạc pin lưu động 24/7 [V5][V6][V7].

## 2. VinFast hiện có gì (công khai)

- **Ứng dụng VinFast:** đặt lịch dịch vụ, theo dõi xe, cập nhật phần mềm từ xa (FOTA) [V4][V5].
- **Tổng đài CSKH + cứu hộ 24/7: 1900 23 23 89** (nhánh 1), miễn phí với hư hỏng thuộc bảo hành; có thể gọi qua app hoặc
  màn hình trung tâm của xe [V5][V6][V8].
- **Sạc pin lưu động 24/7** toàn quốc [V7].
- **Sạc miễn phí tại trụ V-Green:** khách cá nhân mua xe từ 10/2 đến hết 10/2/2029, tối đa 10 lần / tháng [V9].
- **Chưa thấy công bố** việc chủ động nhắn khách dựa trên mã lỗi telematics như Tesla / Rivian → khoảng trống dự án lấp vào.
  Khi pitch nói "chưa thấy công bố", **không** khẳng định "VinFast không có".

## 3. Các hãng nước ngoài làm gì — và dự án học được gì

| Hãng | Cách làm | Dự án đã có | Học thêm (card) |
|---|---|---|---|
| **Tesla** | Xe tự chẩn đoán từ xa, **gửi trước linh kiện** tới trung tâm dịch vụ, báo lên màn hình / app để khách đặt lịch [F1]; trung tâm chẩn đoán trước khi xe đến [F2] | Quyết định ④ "giữ linh kiện trước" | Phiếu tiền chẩn đoán gửi xưởng (A2.19, D2.16); giữ linh kiện sớm (tuần 3, qua executor) |
| **Rivian** | "Remote Care": theo dõi xe liên tục, **chủ động liên hệ** đề xuất cách xử lý; ưu tiên **cập nhật từ xa**; xe dịch vụ lưu động; xe mượn [F3][F4] | UC1 + "từ xa trước" | Cờ xe thay thế (tuỳ dữ liệu) |
| **Hyundai / Kia (Bluelink)** | Mã lỗi **tự gửi tới đại lý ưa thích**; khách xem slot, xác nhận trong app, xem xe mượn; nhắc bảo dưỡng theo thói quen lái [F5] | Đặt lịch có xác nhận | Xưởng ưa thích được ưu tiên (B2.19) |
| **Mercedes (Mercedes me)** | Xưởng **đọc dữ liệu xe từ xa trước khi khách đến**; nhắc bảo dưỡng [F6] | HandoffCard + copilot | Phiếu tiền chẩn đoán (A2.19, D2.16) |

## 4. Quyết định hướng đi (lead, 03/10)

**Proactive là cửa vào, hội thoại đa bước là thân bài.** Giữ lõi đề BTC (FAQ RAG có trích dẫn, phân loại ý định, 4 workflow
tool-calling, xác nhận trước khi ghi, handover kèm tóm tắt, đo lường); lấy UC1 của nhánh `hung` làm cú mở màn, **làm gọn**.

| Hạng mục | Quyết định | Lý do |
|---|---|---|
| UC1 detector lặp ≥ 3 lần / 14 ngày + đường tất định | **Làm** (B2.17, A2.18) | Dùng lại T0 / Scheduler / executor đã có; tạo điểm khác biệt |
| Node "InterventionProposal 8 câu hỏi" bằng LLM | **Bản nhẹ**: schema có `evidence_refs`, điền tất định, LLM chỉ viết câu | Luật đã trả lời phần lớn 8 câu; LLM tự đánh giá mức khẩn tăng rủi ro suy diễn; chính spec UC1 ghi "rule đủ → không gọi Agent" |
| UC2 trạm sạc | **Hoãn tuần 3** (B2.14 giữ, làm nếu dư giờ) | Cần dữ liệu trạm + tool + detector + subgraph mới; không thuộc 4 workflow đề chấm; câu chuyện chồng UC1 |
| UC4 / UC5 / UC6 | **Chỉ pitch** (UC6 có một phần qua B2.15) | Mỗi UC là miền dữ liệu mới (hoá đơn, claim, lịch sử sửa) |

Kịch bản demo 11/10 — 7 màn: xem `plan/demo-full.md`.

## Nguồn tham khảo (truy cập 03/10/2026)

**VinFast**
- [V1] Thông báo chính sách bảo hành ô tô điện VinFast — https://vinfastauto.com/vn_vi/thong-bao-chinh-sach-bao-hanh-o-to-dien-vinfast (trang chặn truy cập tự động — nội dung đối chiếu qua kết quả tìm kiếm và bản đăng lại https://vinfast.vn/thong-bao-chinh-sach-bao-hanh-o-to-dien-vinfast/)
- [V2] Các hạng mục bảo dưỡng xe ô tô VinFast — https://vinfastauto.com/vn_vi/bao-duong-xe-vinfast-dinh-ky
- [V3] Lịch bảo dưỡng định kỳ trên VF 8 — Cộng đồng VinFast — https://vinfast.vn/thu-vien/vf-8/lich-bao-duong-dinh-ky-tren-vf-8-cac-moc-can-nho-va-nhung-luu-y-chu-xe-nen-biet/
- [V4] Hướng dẫn cập nhật phần mềm từ xa FOTA cho VF 8 — https://vinfast.vn/huong-dan-cap-nhat-phan-mem-tu-xa-fota-cho-vf-8/
- [V5] Dịch vụ cứu hộ 24/7 của VinFast — https://vinfastauto.com/vn_vi/dich-vu-cuu-ho-247-cua-vinfast
- [V6] Tổng hợp các dịch vụ cứu hộ VinFast — https://vinfastauto.com/vn_vi/dich-vu-cuu-ho-vinfast
- [V7] VinFast triển khai dịch vụ sạc pin lưu động 24/7 — https://vinfast.vn/vinfast-trien-khai-dich-vu-sac-pin-luu-dong-24-7-tren-toan-quoc/
- [V8] Thông báo đường dây nóng CSKH và kênh tiếp nhận khiếu nại — https://vinfastauto.com/vn_vi/thong-bao-ve-duong-day-nong-cham-soc-khach-hang-va-kenh-tiep-nhan-khieu-nai-khach-hang
- [V9] Xe điện VinFast sạc pin miễn phí đến năm 2029 — VnExpress — https://vnexpress.net/xe-dien-vinfast-sac-pin-mien-phi-den-nam-2029-5016208.html

**Pháp luật Việt Nam**
- [L1] Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân — https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-dinh-13-2023-nd-cp-bao-ve-du-lieu-ca-nhan-119230516104357809.htm
- [L2] Luật Trí tuệ nhân tạo 2025 (số 134/2025/QH15, hiệu lực 01/3/2026) — https://luatvietnam.vn/linh-vuc-khac/luat-tri-tue-nhan-tao-2025-va-diem-dang-chu-y-883-105846-article.html
- [L3] Một số quy định mới tại Luật Bảo vệ quyền lợi người tiêu dùng 2023 — Bộ Công Thương — https://moit.gov.vn/tin-tuc/bao-chi-voi-nguoi-dan/mot-so-quy-dinh-moi-tai-luat-bao-ve-quyen-loi-nguoi-tieu-dung-nam-2023.html

**Hãng nước ngoài**
- [F1] Tesla vehicles can now diagnose themselves and even pre-order parts — Electrek — https://electrek.co/2019/05/06/tesla-diagnose-pre-order-parts-service/
- [F2] Tesla — Preparing for a Service Center Visit — https://www.tesla.com/en_qa/support/preparing-service-center-visit
- [F3] Rivian Service — Rivian Stories — https://stories.rivian.com/rivian-service
- [F4] Rivian Remote Care — InsideEVs — https://insideevs.com/news/498456/rivian-remote-care-convenient-servicing/
- [F5] Hyundai Vehicle Health / Bluelink — https://owners.hyundaiusa.com/us/en/page/vehicle-health
- [F6] The Mercedes-Benz app — https://www.mbusa.com/en/mercedes-benz-app

**An toàn xe điện**
- [S1] NHTSA — Interim Guidance for Electric and Hybrid-Electric Vehicles — https://www.nhtsa.gov/sites/nhtsa.gov/files/interimguide_electrichybridvehicles_012012_v3.pdf
- [S2] AAA — Expert Q&A: EV Fire Safety — https://ev.aaa.com/articles/expert-qa-evs-and-fire-safe/
