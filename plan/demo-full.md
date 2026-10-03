# Kịch bản demo đầy đủ — CN 11/10 (≈ 8 phút) = bài kiểm end-to-end tuần 2

Thêm vào kịch bản MVP (`demo-mvp.md`). Mỗi dòng có kịch bản eval tự động tương ứng trong `eval/scenarios/`.

## Kịch bản trình diễn 11/10 — 7 màn (lead chốt 03/10)

Một câu chuyện liền mạch: **proactive là cửa vào, hội thoại đa bước là thân bài** (lý do + nguồn:
[`docs/research/2026-10-03-nghiep-vu-vinfast.md`](../docs/research/2026-10-03-nghiep-vu-vinfast.md)). Nhân vật: anh Minh,
VF8-4821, **chưa có lịch hẹn** (bối cảnh: bơm `appointment.changed` huỷ A-20931 trước khi bắt đầu). Bảng kiểm bên dưới vẫn
là danh sách tình huống phải chạy được (mỗi dòng có kịch bản eval).

| Màn | Người trình bày | Hệ thống phải làm (kiểm được) | Chứng minh yêu cầu đề | Task |
|---|---|---|---|---|
| 1 · UC1 nhắn trước | Demo panel: bơm `vehicle.dtc.raised` BATT-COOL-01 (WARNING) 3 lần, tua đồng hồ giữa các lần | Lần 1–2: không làm gì (0 token). Lần 3: detector đủ ngưỡng, không có case mở, qua arbitration → tin 5 phần: "cảnh báo làm mát pin lặp 3 lần trong X ngày" · 2 phương án đã kiểm quãng đường + linh kiện · hạn giữ chỗ · người phụ trách · vì sao nhận tin; trích dẫn KB | Proactive (mở rộng theo mentor), detector trước LLM | B2.17 · A2.18 · B2.04 · C2.14 |
| 2 · Hai mục đích | Khách: "Lỗi này có được bảo hành không? À mà đơn bộ sạc tuần trước tới đâu rồi?" | "Đủ điều kiện bảo hành sơ bộ" + lý do + trích dẫn; trạng thái đơn từ tool; rồi tự quay lại việc dở: "anh chọn phương án nào ạ?" — không hỏi lại VIN | Hiểu mục đích xuyên suốt, intent routing, RAG có trích dẫn, workflow **tra đơn** | A2.01 · A2.02 · B2.18 · D1.05 |
| 3 · Đặt lịch | Khách gõ: "Chọn Gia Lâm sáng thứ 7 nhé" → bấm Xác nhận | Thu hẹp đúng phương án, thẻ xác nhận đủ việc · xe · giờ · xưởng, chưa ghi; bấm → token + validator 7 kiểm tra → ghi; "Việc của tôi" có lịch; xưởng nhận **phiếu tiền chẩn đoán**. Phụ: bấm lại không đặt trùng, token sửa bị từ chối | Workflow **đặt lịch**, xác nhận trước khi hành động | A1.06 · D1.09 · A2.19 · D2.16 |
| 4 · Đổi / trả + ticket | Khách: "Bộ sạc mới nhận bị lỗi đèn, anh muốn đổi" | Trích chính sách đổi / trả từ KB, đề xuất yêu cầu đổi (tham số từ đơn) → Xác nhận → ticket có mã + hạn xử lý | Workflow **đổi / trả + ticket** | A2.01 · D2.01 · A2.15 |
| 5 · Đổi thông tin | Khách: "Đổi số điện thoại liên hệ giúp anh" | Nhắc lại thay đổi (số che bớt) → Xác nhận → ghi | Workflow **thay đổi thông tin**, che PII | A2.01 · D2.01 |
| 6 · Sự cố + chuyển người | Demo panel: `parts.reservation.cancelled`; khách: "Sao lại thế… cho anh gặp người" | Tin chủ động phương án mới (UC3); HandoffCard đủ trường (tóm tắt, mục tiêu xong / dở, sự thật có nguồn, đã hứa gì, không được làm gì, hạn gọi lại 15') ở Console; nhân viên Nhận, copilot gợi ý có nguồn | **Handover kèm tóm tắt** | A1.08 · A2.06 · C2.01 |
| 7 · Minh bạch + đo lường | Mở trace LangSmith + dashboard eval | Bước 0 token / bước gọi LLM / bước ghi qua executor; số eval: task accuracy, handover đúng lúc, tỉ lệ có trích dẫn, so baseline | **Đo lường được** (tiêu chí 1.7 của đề) | A2.08 · D2.05 · C2.04 |

**Không trình diễn (chỉ nêu trong pitch):** UC2 trạm sạc (làm tuần 3 nếu dư giờ), UC4 / UC5 / UC6.

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
| 8 | Tua +14 ngày sau sửa | Xác minh bằng telematics → đóng việc; tái phát → mở lại (UC6) | B2.15 · A2.17 |
| 9 | Dashboard | Số từ eval: cứu trước hẹn, handoff đúng lúc, p95 độ trễ, so baseline B0–B2 | C2.04 · D2.06 |
| 0 | **UC1 flagship — bơm `vehicle.dtc.raised` ×3 trong 14 ngày (VF8, khách chưa làm gì, chưa có lịch / ticket)** | L0 tạo candidate (0 token) → arbitration → agent điều tra → tin chủ động có "vì sao anh nhận tin này" → khách xác nhận → UC3 đặt lịch → verify +14 ngày. Kịch bản đối chứng: chỉ 1 lần / đã có lịch → không candidate | E15 · E16 (card chưa tạo) |
| 10 | **Upsell có kiểm soát**: VF3-1107 hỏi lịch bảo dưỡng → sau đó khách đang bực hỏi lại | Lần 1: trả lời lịch + 1 thẻ "Gợi ý" bảo hành mở rộng (lý do, nguồn, giá giả lập, "Không quan tâm"); "Xem báo giá" đi qua Xác nhận · Lần 2 (bực): **không** gợi ý | B2.12 · D2.13 · C2.13 · C2.11 |

**Cổng 11/10:** 150 kịch bản · 0 vi phạm "hard" (gồm 4 kịch bản cấm gợi ý upsell) · baseline B0–B2 · 5 người dùng thử · dark mode + mobile · README + report cập nhật · pitch nháp.

## Lần chạy thử (A2.13 tick khi có ≥ 2 dòng `[x]`)
- [ ] Lần chạy 1 — ngày/giờ: ____ · Live URL · lỗi gặp: ____
- [ ] Lần chạy 2 — ngày/giờ: ____ · Live URL · lỗi gặp: ____
