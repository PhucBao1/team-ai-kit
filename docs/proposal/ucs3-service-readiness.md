# PL-A3 · DEMO-READY · xuôi dòng — UC3 — Service Readiness / Intervention Orchestration

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Nơi appointment xuất hiện: suy luận đa ràng buộc để có 2–3 phương án khả thi thật, sau khi can thiệp xưởng đã được chính đáng hoá.

**UC3 — demo-ready; là nơi appointment xuất hiện.** UC3 không bao giờ là điểm bắt đầu. Nó chạy **sau** khi UC1 / UC2 / UC6 (hoặc khách) đã chứng minh cần can thiệp tại xưởng. Mọi kịch bản là *Synthetic / illustrative scenario for MVP*.

### Goal

Biến một can thiệp xưởng **đã được chính đáng hoá** thành 2–3 phương án **khả thi thật** (không chỉ "slot trống đầu tiên"), để khách chọn, xác nhận, rồi đặt có kiểm soát và xác minh.

### Customer Pain

Lịch hẹn nhìn có vẻ ổn nhưng bỏ sót ràng buộc: linh kiện chưa về, xưởng không có kỹ thuật viên pin cao áp, pin không đủ đi tới, khách không rảnh giờ đó. Khách chỉ biết khi đã nghỉ làm, lái xe tới xưởng rồi phải về.

### Why Proactive?

UC3 là phần *thực hiện* của can thiệp chủ động: nếu UC1 đã báo cho khách mà phương án đưa ra không thực hiện được thì cả chuỗi mất giá trị. Kiểm tra ràng buộc **trước** khi hứa là phần proactive; và theo dõi reservation cho tới ngày hẹn là cách giữ lời hứa.

### Trigger Signals

Trigger là **một yêu cầu can thiệp (InterventionRequest)**, không phải appointment:

| Nguồn trigger | Điều kiện |
| --- | --- |
| UC1 | Agent kết luận cần can thiệp xưởng (`prepare_service_option`) |
| UC2 | Hypothesis D / B lặp lại, chuẩn bị đề xuất dịch vụ |
| UC6 | Tái phát → mở lại / chuẩn bị lệnh sửa |
| Khách trong chat | Khách tự yêu cầu đặt lịch (đường hội thoại cũ vẫn dùng chung UC3) |
| **Nhánh lập lại phương án** | `parts.reservation.cancelled` · `parts.eta.changed` · `appointment.changed` làm lịch **đã được xác nhận** mất điều kiện (còn < 72 giờ) → UC3 chạy lại |

### What Happens Before the Customer Contacts Support

Trước khi khách hỏi "có lịch nào không", UC3 đã kiểm tra các xưởng theo linh kiện, kỹ năng, slot, quãng đường và gợi ý giờ phù hợp. Sau khi khách chọn, hệ thống tiếp tục **canh** điều kiện (reservation, ETA) tới ngày hẹn và báo trước khi khách phải đến xưởng vô ích.

### L0 Detector — NO LLM

UC3 không có detector tín hiệu mới; L0 ở đây là **kiểm tra điều kiện đầu vào và ràng buộc cơ bản**, tất định:

- `InterventionRequest` hợp lệ: có `vin`, `issue_type`, `reason`, nguồn UC; `customer` có quyền đặt lịch cho xe (`owner_or_can_book`).
- Lọc cứng (core): `part_matches_vin` · khoảng cách và pin qua `core.range` · xưởng đang mở · slot `free`.
- **Nhánh lập lại:** rule `on_reservation_cancelled`: `appointment.status = confirmed` **và** `start − now < 72 giờ` → `CandidateFriction(UC3_REPLAN)`; quét hằng ngày: mọi lịch trong 72 giờ phải có reservation hợp lệ.

Tập ứng viên sau lọc cứng đi tới Agent. **Không LLM ở bước này.**

### Context / Evidence Required

Xe + vấn đề + linh kiện dự kiến (`explain_dtc` → likely_parts) · tồn kho + ETA từng xưởng · kỹ thuật viên và chứng chỉ (`hv_certified`) · slot trống · khoảng cách và pin hiện tại · ràng buộc của khách (giờ rảnh, kênh, xưởng ưa thích — từ memory có đồng ý) · bảo hành sơ bộ · ưu tiên (xe có cảnh báo an toàn được ưu tiên linh kiện).

### Why an Agent Is Necessary

Có ≥ 5 ràng buộc phụ thuộc lẫn nhau và **không có phương án thắng tuyệt đối**: xưởng gần nhất có thể thiếu linh kiện, xưởng có linh kiện có thể thiếu kỹ thuật viên, xưởng đủ cả hai có thể xa hơn pin cho phép. Phải **loại có lý do**, xếp hạng theo ý khách, rồi giải thích *vì sao* mỗi phương án hợp lệ. Đây là chỗ Agent chứng minh giá trị bằng suy luận đa ràng buộc + điều phối tool — một rule "slot sớm nhất" sẽ sai.

### Exact Agent Reasoning Task

Với mỗi xưởng, Agent đánh giá ràng buộc và trả về **phương án hợp lệ kèm lý do** và **phương án bị loại kèm lý do** (Option §13 + `rejected[]`):

| Ràng buộc | Câu hỏi |
| --- | --- |
| Linh kiện | Có đúng mã, đủ số lượng, hoặc ETA trước giờ hẹn? Đã được giữ cho lệnh này? |
| Kỹ thuật viên | Có người đủ chứng chỉ cho hạng mục (ví dụ pin cao áp) vào ca đó? |
| Slot | Còn trống, khoá tạm được 15 phút? |
| Quãng đường / pin | Pin hiện tại đi tới được không? Cần sạc dọc đường? |
| Khách | Giờ rảnh, xưởng ưa thích, người lái ≠ chủ xe? |

Đầu ra **2–3 phương án** xếp hạng + `why` + `rejected_with_reason`. Không chọn "slot đầu tiên" nếu bỏ sót ràng buộc.

### Tools the Agent May Call

Mức 0: `find_options(vin, reason, window)` (gom tồn kho + kỹ năng + slot + `core.range`, **khoá slot tạm 15 phút**) · `get_vehicle_status` · `check_warranty` · `find_chargers` (nếu cần sạc dọc đường) · `list_jobs`. Mức 1: `create_handoff`. **Không** `book_appointment` / `reschedule` — chỉ Executor sau xác nhận.

### Decision / Intervention Options

- **Trình bày 2–3 phương án khả thi** (xưởng · giờ · quãng đường · linh kiện sẵn sàng · vì sao hợp lệ).
- **Không có phương án khả thi** → nói thẳng, đề xuất thay đổi ràng buộc (dời ngày, dịch vụ lưu động nếu có), hoặc handoff.
- **Nhánh lập lại:** thông báo lịch cũ không còn đủ điều kiện + phương án mới; không tự đổi lịch.

### Validation Rules

Validator mức 2 (D, **không LLM**):

| Check | Quy tắc | Không đạt thì |
| --- | --- | --- |
| `customer_verified` | Phiên app / OTP; khách sở hữu xe | Dừng, yêu cầu xác thực |
| `owner_or_can_book` | Chủ xe hoặc người lái có `can_book` | Dừng / handoff |
| `part_matches_vin` | Mã linh kiện khớp đời xe | Chuyển CVDV |
| `technician_certified` | Đủ chứng chỉ | Loại phương án |
| `part_reserved` | Linh kiện giữ đúng lệnh, đúng xưởng | Loại phương án |
| `slot_locked` | Slot khoá tạm còn hiệu lực | Tìm slot khác |
| `customer_confirmed` | Token khớp phương án, tham số không đổi | Không ghi |

### Customer Confirmation Requirement

**Bắt buộc (mức 2).** Tin nhắc lại đủ: *việc · xe · giờ · xưởng · thời lượng*, cùng lý do chọn. API ký `confirmation_token` cho từng option (LLM không thấy token); hết hạn thì phải xác nhận lại.

### Executor / Write Actions

Sau `POST /confirm {token}`: Executor gọi `book_appointment` / `reschedule` (idempotent theo `hash(option_id, token)`), **saga** nếu nhiều hệ thống (giữ linh kiện mới + đặt slot mới + trả slot cũ). Thành công → giải phóng slot cũ, cập nhật reservation / promise / journey, ghi audit. Thất bại / timeout → **không** báo "đã đặt"; đọc lại trạng thái; retry có giới hạn; báo đúng tình trạng.

### Verification Loop

| Kiểm tra | Bằng chứng | Kết quả |
| --- | --- | --- |
| Đặt thành công | Đọc lại `appointment.status = confirmed`, đúng slot, đúng xưởng | `booked` |
| Linh kiện giữ đúng | `reservation` đúng mã, đúng xưởng, `held` | `held` |
| Điều kiện còn nguyên tới ngày hẹn | Theo dõi `reservations` / `eta` (sweep hằng ngày) | `ok` / `replan` |
| Sửa xong | `repair_order.closed` đúng hẹn | `done` |
| Friction hết | Telematics không lặp lại **14 ngày** | `resolved` / `recurred` → UC6 |

### Failure / Retry / Handoff

- Validator loại phương án → Agent thay phương án khác (≤ 2 lần) rồi handoff.
- **Nhánh lập lại:** `parts.reservation.cancelled` làm lịch confirmed mất linh kiện (còn < 72 giờ) → UC3 chạy lại → khách nhận phương án mới → khách bực / muốn người → handoff CVDV kèm card.
- Khách không chọn trong thời hạn → slot tạm tự nhả; nhắc 1 lần.
- Ghi thất bại → retry có giới hạn → báo trung thực → handoff.

### Customer UX

Màn hình phương án: mỗi thẻ có xưởng · giờ · quãng đường · pin · *"vì sao hợp lệ"* và (gấp lại) *"vì sao phương án khác bị loại"*. Nút Xác nhận nhắc đủ tham số; nút Gặp nhân viên. "Việc của tôi" hiển thị bước Đặt lịch → Giữ linh kiện → Chờ hẹn → Chẩn đoán → Sửa → Xác minh, kèm lý do mọi thay đổi.

### CSKH / Staff UX

Console: danh sách phương án + lý do loại + trace ràng buộc (linh kiện, kỹ thuật viên, slot, pin). Handoff card khi khách muốn người: phương án đã đề xuất, điều đã hứa, **không làm** (không hỏi lại biển số / lịch cũ; không hứa chắc chắn bảo hành; không hứa ưu đãi ngoài chính sách). Copilot gợi ý trong cuộc gọi, chỉ nhân viên thấy.

### Synthetic Data Required

*Synthetic / illustrative scenario for MVP.* Dùng seed §08: 3 xưởng (Long Biên 4 km · Gia Lâm 6 km có kỹ thuật viên pin cao áp · một xưởng xa 35 km), ~60 slot (thứ Bảy 3/10 09:00 và 14:00 trống ở Long Biên và Gia Lâm), tồn kho `BATT-COOL-PUMP` thay đổi theo thời gian. Cần thêm: một kịch bản **chỉ có đúng một phương án hợp lệ** · một kịch bản **không có phương án** · sự kiện `parts.reservation.cancelled` (lý do `reallocated_recall`) cho nhánh lập lại.

### Concrete Demo Scenario

*Synthetic / illustrative scenario for MVP.* Khớp với demo §08: anh Minh, VF 8; tiếp nối UC1 — anh Minh chọn "Xem phương án" lúc 08:16 thứ Ba 29/9. Hai giai đoạn: **(1) đặt lịch**, **(2) nhánh lập lại** khi linh kiện bị điều đi.

| Bước | Thời điểm | Chuyện gì xảy ra | Đầu vào → Đầu ra | LLM? |
| --- | --- | --- | --- | --- |
| **T0** | Thứ Ba 08:16 | `InterventionRequest(vin, issue=cooling_pump, source=UC1)` | → UC3 | Không |
| **L0** | 08:16 | Điều kiện hợp lệ · `part_matches_vin` ✓ · lọc cứng pin / quãng đường | → 3 xưởng ứng viên | **Không** |
| Ngữ cảnh | 08:16 | `find_options`: tồn kho, kỹ thuật viên, slot, khoảng cách; khoá slot tạm 15 phút | → `ContextBundle` | Không |
| **Agent được gọi** (giai đoạn 1) | 08:16 | **Long Biên:** linh kiện ✓ · kỹ thuật viên pin cao áp ✓ · slot 9:00 và 14:00 thứ Bảy · 4 km → **hợp lệ**. **Gia Lâm:** đủ cả, 6 km → hợp lệ, xếp sau vì xa hơn. **Xưởng 35 km:** *loại* — không có kỹ thuật viên pin cao áp ca thứ Bảy và pin 42% cần sạc dọc đường | → 2 phương án (Long Biên 9:00 / 14:00) + 1 lý do loại | L2 (~2.500 token) |
| Validator | 08:17 | `part_matches_vin` ✓ · `technician_certified` ✓ · `part_reserved` (tạm) ✓ · `slot_locked` ✓ | → `approved_to_show` | Không |
| Tin | 08:17 | 2 phương án + lý do + nút Xác nhận / Gặp nhân viên | → app | Mẫu tin |
| **Khách xác nhận** | 08:23 | Anh Minh chọn 9:00 thứ Bảy tại Long Biên, bấm Xác nhận | `POST /confirm {token}` | Không |
| Validator + Executor | 08:23 | 7 check ✓ → `book_appointment(option_id, token)` (idempotent) → giữ linh kiện + ghi promise | → `SA-20931` | Không |
| **Verify** | 08:23 | Đọc lại: `confirmed` · reservation `held` đúng mã đúng xưởng · journey = *chờ hẹn* | `VerificationResult(booked)` | Không |
| **Nhánh lập lại** | Thứ Năm 1/10 14:02 | Kho điều linh kiện đi cho xe triệu hồi: `parts.reservation.cancelled` (lịch còn 67 giờ) | event | Không |
| L0 phát hiện | 14:02 | `confirmed` + `start − now < 72 giờ` → `CandidateFriction(UC3_REPLAN)`; arbitration qua | → UC3 chạy lại | Không |
| **Agent lập lại** (giai đoạn 2) | 14:03 | **Long Biên:** slot thứ Bảy ✓ nhưng linh kiện đã bị điều đi → *loại (linh kiện)*. **Xưởng 35 km:** có linh kiện + slot nhưng không có kỹ thuật viên pin cao áp thứ Bảy → *loại (kỹ năng)*. **Gia Lâm:** linh kiện ✓ + kỹ thuật viên pin cao áp ✓ + 9:00 thứ Bảy + 6 km + pin 42% đủ + khách rảnh sáng thứ Bảy → **hợp lệ**. **Long Biên 9:00 thứ Ba 6/10** (linh kiện về thứ Hai) → hợp lệ nhưng muộn | → 2 phương án + 2 lý do loại | L2 (~2.500 token) |
| Validator + Tin | 14:04 | Như trên; tin xin lỗi + 2 phương án + Gặp nhân viên | → app | Mẫu tin |
| Khách | 14:06 | Khách bực: *"Cho anh nói chuyện với người"* | → handoff | Không |
| Handoff | 14:07 | CVDV Hải nhận card: phương án đã đề xuất, đã hứa gọi trong 15 phút, **không làm** (không hỏi lại biển số, không hứa chắc chắn bảo hành) | `create_handoff` | Tóm tắt 1 dòng |
| Executor + Verify | 14:21 | Khách chọn phương án 1 (Gia Lâm) qua CVDV → Executor `reschedule`: giữ slot + linh kiện mới, giải phóng slot Long Biên → đọc lại: `confirmed`, reservation `held` | → `booked` | Không |
| Resolved | Thứ Bảy 11:30 + 14 ngày | Sửa xong đúng hẹn; telematics 14 ngày không ghi nhận lại mã | `VerificationResult(resolved)`; tái phát → UC6 | Không |

### Cost Tier

**CAO — nhưng chỉ sau khi can thiệp xưởng đã chính đáng.** UC3 không bao giờ được gọi cho từng event; chỉ chạy khi có `InterventionRequest` hoặc điều kiện lịch hỏng.

### Success Criteria

Mục tiêu thiết kế — chưa đo: **100%** phương án đưa ra vượt validator · phương án đầu tiên khách chọn (đo, không ép) · **0** ghi không có xác nhận · nhánh lập lại: Pre-chase recovery ≥ 70% trên kịch bản tiêm lỗi (phát hiện và gửi tin trước ngày hẹn) · thời gian từ event tới tin chủ động p95 < 5 phút · mọi phương án bị loại đều có lý do trong trace.

### Out of Scope / Safety Boundaries

Không tự đổi lịch khi chưa có xác nhận · không bỏ qua ràng buộc để "lấp đầy slot" · không kết luận bảo hành (chỉ sơ bộ) · không chẩn đoán · không hứa ưu đãi / hỗ trợ đi lại ngoài chính sách (SOP-DV-12 **[ASSUMPTION]**) · không tích hợp DMS / ERP thật.

### A/B/C/D Ownership

|  | Việc cần làm cho UC3 |
| --- | --- |
| **A** | Subgraph Scheduler suy luận đa ràng buộc · `Option.why` + `rejected_with_reason` · tin phương án · xử lý nhánh lập lại |
| **B** | `find_options` đủ ràng buộc (kho + kỹ năng + slot + range, khoá tạm) · seed xưởng / tồn kho / kỹ thuật viên · `parts.reservation.cancelled` / `eta.changed` + sweep 72 giờ · `book_appointment` / `reschedule` idempotent |
| **C** | Màn hình phương án (hợp lệ / loại + lý do) · Xác nhận nhắc đủ tham số · "Việc của tôi" 6 bước · console handoff |
| **D** | Validator 7 check · confirmation token + `/confirm` · Executor + saga + outbox · verifier đọc lại · eval phương án hợp lệ + nhánh lập lại |
