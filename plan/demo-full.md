# Kịch bản demo đầy đủ — CN 11/10 (≈ 8 phút) = bài kiểm end-to-end tuần 2

Thêm vào kịch bản MVP (`demo-mvp.md`). Mỗi dòng có kịch bản eval tự động tương ứng trong `eval/scenarios/`.

## Kịch bản trình diễn 11/10 — 9 màn (lead chốt 03/10, viết lại 06/10)

Một câu chuyện liền mạch: **chủ động phát hiện → kiểm tra → thông báo → đề xuất → xác nhận / thực hiện → chuyển người → theo kết quả**.
Proactive là cửa vào (VinFast đã có báo lỗi từ xa từ 2021 — không pitch là điểm mới); phần cần chứng minh là **sau khi báo**: trả lời đúng
quyền lợi theo xe, có người giữ việc + hạn, nói đúng trạng thái khi lỗi, không đóng việc sai (nguồn:
[`docs/research/2026-10-06-business-discovery.md`](../docs/research/2026-10-06-business-discovery.md),
[`docs/research/2026-10-03-nghiep-vu-vinfast.md`](../docs/research/2026-10-03-nghiep-vu-vinfast.md)). Mỗi màn có **nhánh lỗi** phải chạy được. Nhân vật: anh Minh,
VF8-4821, **chưa có lịch hẹn** (bối cảnh: bơm `appointment.changed` huỷ A-20931 trước khi bắt đầu). Bảng kiểm bên dưới vẫn
là danh sách tình huống phải chạy được (mỗi dòng có kịch bản eval).

| Màn | Người trình bày | Hệ thống phải làm (kiểm được) | Chứng minh yêu cầu đề | Task |
|---|---|---|---|---|
| 1 · Phát hiện + báo | Demo panel: bơm `vehicle.dtc.raised` BATT-COOL-01 (WARNING) 3 lần, tua đồng hồ giữa các lần. **`BATT-COOL-01` là mã giả lập; ngưỡng "3 lần / 14 ngày" là giả lập** | Lần 1–2: chưa gửi thêm tin CSKH (0 token) — **xe vẫn tự hiện cảnh báo theo quy trình của xe**, agent chỉ chưa tạo outreach. Lần 3: detector đủ ngưỡng, không có case mở, qua arbitration → tin 5 phần: "cảnh báo làm mát pin lặp 3 lần trong X ngày" · 2 phương án **lịch kiểm tra** đã kiểm quãng đường + linh kiện *dự kiến* (để xưởng chuẩn bị, **không** phải kết luận phải thay) · hạn giữ chỗ · người phụ trách · vì sao nhận tin; nói rõ **chưa kết luận nguyên nhân**; trích dẫn KB. **Nhánh lỗi:** chỉ 1 lần / đã có lịch → không gửi | Proactive (mở rộng theo mentor), detector trước LLM | B2.17 · A2.18 · B2.04 · C2.14 |
| 2 · Hai mục đích + quyền lợi theo xe | Khách: "Lỗi này có được bảo hành không? À mà xe anh còn sạc miễn phí tới khi nào?" | "Đủ điều kiện bảo hành sơ bộ" + lý do + trích dẫn; quyền sạc miễn phí **theo ngày mua của chính xe này** từ `kb:charging_v2026.02` (không phải bản cũ "30/6/2027"); rồi tự quay lại việc dở: "anh chọn phương án nào ạ?" — không hỏi lại VIN. **Nhánh lỗi:** KB không có nguồn → nói không có, chuyển người | Hiểu mục đích xuyên suốt, intent routing, RAG có trích dẫn, workflow **tra đơn** | A2.01 · A2.02 · A2.20 · D1.05 |
| 3 · Đặt lịch | Khách gõ: "Chọn Gia Lâm sáng thứ 7 nhé" → bấm Xác nhận | Thu hẹp đúng phương án, thẻ xác nhận đủ việc · xe · giờ · xưởng, chưa ghi; bấm → token + validator 7 kiểm tra → ghi; "Việc của tôi" có lịch; xưởng nhận **phiếu tiền chẩn đoán**. Phụ: bấm lại không đặt trùng, token sửa bị từ chối | Workflow **đặt lịch**, xác nhận trước khi hành động | A1.06 · D1.09 · A2.19 · D2.16 |
| 4 · Đổi / trả + ticket | Khách: "Bộ sạc mới nhận bị lỗi đèn, anh muốn đổi" | Trích chính sách đổi / trả từ KB, đề xuất yêu cầu đổi (tham số từ đơn) → Xác nhận → ticket có mã + hạn xử lý | Workflow **đổi / trả + ticket** | A2.01 · D2.01 · A2.15 |
| 5 · Đổi thông tin | Khách: "Đổi số điện thoại liên hệ giúp anh" | Nhắc lại thay đổi (số che bớt) → Xác nhận → ghi | Workflow **thay đổi thông tin**, che PII | A2.01 · D2.01 |
| 6 · Điều kiện lịch đổi + chuyển người | Demo panel: `parts.reservation.cancelled`; khách: "Sao lại thế… cho anh gặp người" | Tin chủ động phương án mới (UC3); HandoffCard đủ trường (tóm tắt, mục tiêu xong / dở, sự thật có nguồn, đã hứa gì, không được làm gì, hạn gọi lại 15') ở Console; "Việc của tôi" ghi **"Đã chuyển, chưa có người nhận"** → nhân viên bấm Nhận ca → **"{tên} đang xử lý, cập nhật trước HH:MM"**; copilot gợi ý có nguồn. **Nhánh lỗi:** ghi handoff thất bại → agent **không** nói "đã chuyển", đưa tổng đài | **Handover kèm tóm tắt** | A1.08 · A2.06 · A2.22 · A2.25 · C2.01 |
| 6b · Chuyển người quá hạn | Chuyển người lần nữa, **không** bấm Nhận ca; demo panel tua +20' | Ca chuyển sang hàng chờ **"Trưởng ca CSKH"** (vẫn chưa ai nhận), console có tin quá hạn ghi nơi chuyển trước/sau; khách nhận "đã chuyển yêu cầu tới hàng chờ trưởng ca, hiện chưa có người nhận", **không hứa giờ mới**; tua tiếp → không báo lặp. **Nhánh lỗi:** nhân viên nhận kịp → không báo; chuyển hàng chờ thất bại → báo "vẫn chưa có người nhận", lần sau thử lại | Không bịa trạng thái / lời hứa | A2.26 |
| 7 · Sau sửa | Demo panel: `repair_order.closed` VF8-4821 → bơm `vehicle.heartbeat` mỗi ngày (km tăng) → tua +14 ngày | "Việc của tôi": Đã xác nhận → **Đã sửa xong, đang theo dõi** → **"Trong dữ liệu nhận được sau sửa, chưa ghi nhận lại mã BATT-COOL-01"** + hỏi khách còn triệu chứng không (không nói "đã đóng" / "đã xác minh"). **Nhánh lỗi 1:** heartbeat ngày 1 rồi mất kết nối → ngày 14 **"Chưa đủ dữ liệu để đánh giá sau sửa"**, việc vẫn theo dõi; ngày 16 xe kết nối lại + báo BATT-COOL-01 → **mở lại đúng việc**. **Nhánh lỗi 2:** báo lại mã trong 14 ngày → mở lại | Theo việc tới kết quả, không đóng sai | A2.23 · A2.27 · B2.15 |
| 8 · Minh bạch + đo lường | Mở trace LangSmith + dashboard eval | Bước 0 token / bước gọi LLM / bước ghi qua executor; số eval: task accuracy, handover được **nhận** (không chỉ gửi), quá hạn được phát hiện, **hứa sai = 0**, **đóng sai = 0**, tỉ lệ có trích dẫn đúng phiên bản; so B0 (không AI) · đường tất định · B2 (một agent) để tách lợi ích proactive khỏi LLM | **Đo lường được** (tiêu chí 1.7 của đề) | A2.08 · A2.13 · D2.05 · D2.06 · C2.04 |

### Bổ sung 04/10 — chạy thử 7 màn với LLM thật (lead)

Chạy trên máy (backend + frontend chế độ **Agent thật**, LLM thật), chưa có Live URL. Mở 3 tab: `/khach` (khách),
`/cskh/hang` (CSKH), `/demo` (bảng điều khiển — chỉ để bấm, không cần chiếu). Mỗi bước dưới đây đã chạy qua HTTP
(script smoke của lead), độ trễ mỗi bước ≤ 2,7 s.

| Màn | Thao tác thật | Kết quả 04/10 | Còn thiếu |
|---|---|---|---|
| 0 · Chuẩn bị | `/demo` → **Đặt lại**; huỷ lịch A-20931 (`appointment.changed`, hiện chưa có nút — gọi API) | Việc chuyển "Lịch A-20931 đã huỷ" (sửa #45) | Nút "Khách huỷ lịch" trên bảng điều khiển |
| 1 · UC1 nhắn trước | `/demo` → **VF8 lỗi làm mát pin lặp 3 lần** (bơm 3 lần, mỗi lần +1 ngày giả lập) | ✅ Lần 1–2 im (0 token); lần 3 tin 5 phần "lặp 3 lần trong 2 ngày" + phương án; khách thấy việc trong "Cần anh/chị" | — |
| 2 · Hai mục đích | Khách gõ "Lỗi này có được bảo hành không? À mà đơn bộ sạc tuần trước tới đâu rồi?" | ❌ Agent chỉ trả một ý (danh sách việc) | Xử lý 2 ý trong 1 tin (A) + tra đơn `get_order` (#37 B2.18) |
| 3 · Đặt lịch | Khách gõ "Chọn Gia Lâm sáng thứ 7 nhé" → **Xác nhận** | ✅ Chỉ đề xuất Gia Lâm 09:00 03/10 (sửa #45); bấm lại không đặt trùng; "Việc của tôi" có lịch | Phiếu tiền chẩn đoán lưu cho xưởng (D2.16) |
| 4 · Đổi / trả + ticket | Khách gõ "Bộ sạc mới nhận bị lỗi đèn, anh muốn đổi" → **Xác nhận** | ✅ Phiếu T-7001, hạn phản hồi ≤ 3 ngày làm việc | Đổi theo mã đơn khi có `get_order` (#37) |
| 5 · Đổi thông tin | Khách gõ "Đổi số điện thoại liên hệ giúp anh thành 0912 345 678" → **Xác nhận** | ✅ Nhắc lại số đã che 091****678, ghi sau xác nhận | — |
| 6 · Sự cố + chuyển người | Khách gõ "Sao lại thế, phiền quá, cho anh gặp người" → tab CSKH **Nhận ca** → nhắn qua lại → **Đóng ca** | ✅ Thẻ đủ trường, cảm xúc "bực", hạn gọi lại 15'; nhân viên chat 2 chiều với khách (ADR 005) | Nút "Linh kiện bị điều đi" dùng R-7702 của A-20931 (đã huỷ ở màn 0) → cần sự cố gắn lịch mới; copilot gợi ý cho nhân viên (D2.14, C2.01) |
| 7 · Minh bạch + đo lường | Mở trace LangSmith project `ai20k-agent` | Trace có (LangSmith bật) | Runner eval + số liệu (D1.15, D2.05, D2.08); dashboard (C2.04) |

**Phụ (UC5, nếu dư giờ):** `/demo` → **VF8 sửa xong làm mát pin** → **Tua +14 ngày** → khách có việc "Đã theo dõi xong sau khi sửa";
hoặc **VF8 báo lại lỗi sau sửa** → việc "Lỗi quay lại sau khi sửa" ưu tiên cao.

**Trước 11/10 phải có:** Live URL (D1.04 · D2.11 — chạy lại toàn bộ bảng này trên URL, tick "Lần chạy" bên dưới), màn 2,
sự cố màn 6 gắn lịch mới, số eval cho màn 7.

**Không trình diễn (chỉ nêu trong pitch):** UC2 trạm sạc (làm tuần 3 nếu dư giờ), UC4 hoá đơn, UC5 claim bảo hành. Phần sau sửa (theo dõi, chưa đủ dữ liệu, mở lại — UC6) **có** trình diễn ở màn 7 (sửa 06/10).

## Bảng kiểm tình huống (giữ từ trước 03/10)

| # | Tình huống | Hệ thống phải làm | Task giao |
|---|---|---|---|
| 1 | Đổi ý giữa chừng: hỏi bảo hành → *"à mà đơn phụ kiện hôm trước tới đâu rồi"* → quay lại đặt lịch | Không mất ngữ cảnh, không hỏi lại VIN | A2.02 |
| 2 | 4 workflow PRD: tra việc / đơn · đặt lịch · **đổi-trả + ticket** · **cập nhật số điện thoại** | Mỗi hành động ghi đều qua nút Xác nhận; ticket có mã + hạn xử lý | A2.01 · D2.01 · C2.02 |
| 3 | VF6-2290 pin 3% cần đi xưởng | Không đưa lịch không đi tới được → gợi ý trạm sạc / dịch vụ lưu động (UC3: ràng buộc quãng đường; trạm sạc thuộc UC2) | B2.14 · A2.17 · B2.03 |
| 4 | ADAS-CAM-03 | Đề xuất cập nhật phần mềm từ xa trước khi đặt xưởng | A1.11 · D2.01 |
| 5 | HV-ISO-99 (CRITICAL) | Mẫu tin an toàn duyệt sẵn + chuyển người 24/7, không LLM chẩn đoán | A1.13 |
| 6 | Người lái VF9 (không có quyền) xin đặt lịch | Validator `owner_or_can_book` chặn, gợi ý mời chủ xe xác nhận | D1.09 · A1.14 |
| 7 | Nhân viên nhận handoff | Copilot gợi ý có nguồn, auto-wrap ghi chú, trả việc lại cho agent | A2.06 · C2.01 |
| 8 | Tua +14 ngày sau sửa | Không mã lỗi mới → "đã theo dõi, chưa thấy lỗi" + hỏi khách (chưa gọi là xác minh); tái phát → mở lại | B2.15 · A2.17 · A2.23 |
| 9 | Dashboard | Số từ eval: cứu trước hẹn, handoff đúng lúc, p95 độ trễ, so baseline B0–B2 | C2.04 · D2.06 |
| 0 | **UC1 flagship — bơm `vehicle.dtc.raised` ×3 trong 14 ngày (VF8, khách chưa làm gì, chưa có lịch / ticket)** | L0 tạo candidate (0 token) → arbitration → agent điều tra → tin chủ động có "vì sao anh nhận tin này" → khách xác nhận → UC3 đặt lịch → verify +14 ngày. Kịch bản đối chứng: chỉ 1 lần / đã có lịch → không candidate | E15 · E16 (card chưa tạo) |
| 10 | **Upsell có kiểm soát**: VF3-1107 hỏi lịch bảo dưỡng → sau đó khách đang bực hỏi lại | Lần 1: trả lời lịch + 1 thẻ "Gợi ý" bảo hành mở rộng (lý do, nguồn, giá giả lập, "Không quan tâm"); "Xem báo giá" đi qua Xác nhận · Lần 2 (bực): **không** gợi ý | B2.12 · D2.13 · C2.13 · C2.11 |

**Cổng 11/10:** 150 kịch bản · 0 vi phạm "hard" (gồm 4 kịch bản cấm gợi ý upsell) · baseline B0–B2 · 5 người dùng thử · dark mode + mobile · README + report cập nhật · pitch nháp.

## Lần chạy thử (A2.13 tick khi có ≥ 2 dòng `[x]`)
- [ ] Lần chạy 1 — ngày/giờ: ____ · Live URL · lỗi gặp: ____
- [ ] Lần chạy 2 — ngày/giờ: ____ · Live URL · lỗi gặp: ____
