# PL-A2 · DEMO-READY — UC2 — Charging Friction Prevention

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Phiên sạc thất bại lặp lại: đường tất định khi nguyên nhân rõ, Agent khi mơ hồ; verify bằng phiên sạc kế tiếp.

**UC2 — demo-ready.** Chứng minh engine UC1 dùng lại được cho một miền khác (sạc), và chứng minh **hai đường**: tất định khi nguyên nhân rõ, Agent khi mơ hồ. Mọi kịch bản là *Synthetic / illustrative scenario for MVP*.

### Goal

Ngăn friction sạc leo thang: khi khách thất bại sạc lặp lại mà chưa liên hệ, hệ thống tìm hiểu nguyên nhân khả dĩ, đưa lối ra thực tế (thử lại đúng cách, trạm khác, đề xuất dịch vụ, người) và xác minh phiên sạc kế tiếp.

### Customer Pain

Cắm sạc không được, thử lại vẫn không được, không biết do trạm, do xe hay do tài khoản. Nếu pin thấp hoặc sắp có chuyến đi, mỗi lần thử lại là mất thời gian và niềm tin vào xe điện. Khách thường chỉ gọi hotline sau khi đã thử nhiều lần.

### Why Proactive?

- Dữ liệu phiên sạc thất bại nằm sẵn ở CSMS / telematics — hệ thống thấy **trước** khi khách gọi.
- Cửa sổ giá trị là *ngay lúc khách đang đứng ở trạm*: gợi ý đúng việc trong vài phút rẻ hơn rất nhiều so với cứu hộ hay khiếu nại.
- Tương quan "cùng xe thất bại ở nhiều trạm, trong khi trạm khoẻ" là bằng chứng mà khách không tự thấy được.

### Trigger Signals

| Tín hiệu | Nguồn | Vai trò |
| --- | --- | --- |
| `charging.session.failed` (mã lỗi, trạm, cổng, SoC) | CSMS / telematics | Tín hiệu chính |
| Tình trạng trạm / cổng và tỉ lệ phiên thành công gần đây | CSMS | Tương quan trạm |
| Lịch sử sạc thất bại của cùng xe 30 ngày | Telematics | Ngữ cảnh |
| Chuyến đi / nhu cầu sạc sắp tới | App **[ASSUMPTION]** | Ngữ cảnh mức khẩn |
| Không có khiếu nại / ticket đang mở | CRM | Điều kiện loại trừ |

### What Happens Before the Customer Contacts Support

Sau lần thất bại thứ hai, trước khi khách bấm gọi: hệ thống đã biết trạm khoẻ hay hỏng, xe này đã thất bại ở đâu trước đó, trạm thay thế nào đi tới được với SoC hiện tại. Khách nhận một tin chỉ rõ việc nên làm ngay.

### L0 Detector — NO LLM

| Bước | Rule |
| --- | --- |
| 1 | ≥ **2** phiên thất bại, cùng xe, trong **30 phút** (cùng hoặc khác cổng) |
| 2 | Tương quan trạm: tỉ lệ phiên thành công của cổng đó trong 60 phút qua → gắn nhãn `station_health` = `faulted` (CSMS báo lỗi hoặc ≥ 3 xe khác cũng thất bại) / `healthy` (còn xe khác sạc được) / `unknown` |
| 3 | Dedupe `(vin, station, hour)`; cooldown 6 giờ sau một tin UC2 |
| 4 | Không có khiếu nại / ticket sạc đang mở |
| 5 | Mức khẩn: SoC ≤ 10% **và** không ở trạm đang hoạt động → `priority = urgent` (luồng 24/7) |

Kết quả: `CandidateFriction(UC2)` kèm `station_health`, `vehicle_failures_30d`, `soc`. **Không LLM.** Sau đó arbitration như UC1 (urgent được bỏ qua giờ yên tĩnh).

### Context / Evidence Required

Trạng thái phiên sạc hiện tại · lịch sử sạc 30 ngày của xe (`get_charging_history` **[mới]**) · tình trạng trạm (`get_station_status` **[mới]**) · trạm thay thế đi tới được với SoC (`find_chargers` + `core.range`) · lịch sử dịch vụ gần đây liên quan sạc (cập nhật phần mềm, thay linh kiện cổng sạc) · chuyến đi sắp tới nếu có · KB hướng dẫn thử lại.

### Why an Agent Is Necessary

**Hai đường:**

- **Đường tất định (không Agent):** `station_health = faulted` và có trạm thay thế đi tới được → gửi mẫu tin khẩn + trạm gần nhất + hỏi cần cứu hộ không. Đây là phần lớn ca; chi phí LLM = 0.
- **Đường Agent:** `station_health = healthy` mà xe này vẫn thất bại, hoặc dấu hiệu mâu thuẫn (thất bại ở nhiều trạm, vừa cập nhật phần mềm, tài khoản có cờ lạ). Rule không phân biệt được nguyên nhân khả dĩ → cần Agent so sánh giả thuyết và chọn can thiệp.

### Exact Agent Reasoning Task

Agent xếp hạng **5 giả thuyết** với bằng chứng và độ tin cậy, **không kết luận chắc chắn**:

|  | Giả thuyết | Bằng chứng ủng hộ khả dĩ |
| --- | --- | --- |
| A | Lỗi phía trạm | Cổng khác cùng trạm cũng lỗi; CSMS báo Faulted |
| B | Friction phía xe / tài khoản | Trạm khoẻ; xe thất bại ở ≥ 2 trạm; lịch sử cùng mã lỗi |
| C | Sự cố nhất thời | Lần đầu; thử lại thành công ở cổng khác |
| D | Cần can thiệp dịch vụ | B lặp lại + lịch sử sửa cổng sạc / phần mềm liên quan |
| E | Cần người | SoC thấp, bằng chứng mâu thuẫn, khách bực / khẩn |

Đầu ra: giả thuyết xếp hạng + can thiệp tương ứng + mức tin cậy. Nếu bằng chứng không đủ, tin phải nói *"chưa xác định được nguyên nhân"* và chọn can thiệp an toàn nhất. Agent **không** khẳng định lỗi kỹ thuật.

### Tools the Agent May Call

Mức 0: `get_vehicle_status` · `find_chargers(lat, lng, soc)` · `get_charging_history` **[mới]** · `get_station_status` **[mới]** · `explain_dtc` (nếu có mã) · `list_jobs` · `find_options` (chỉ khi cân nhắc dịch vụ → UC3). Mức 1: `create_handoff` (kể cả luồng khẩn 24/7). **Không** tool ghi mức 2; không tự gọi cứu hộ.

### Decision / Intervention Options

| Giả thuyết | Can thiệp | Xác nhận khách |
| --- | --- | --- |
| A, C | Hướng dẫn thử lại (cổng khác / cắm lại) từ KB · **trạm thay thế** đi tới được | Không |
| B | Thử lại + trạm thay thế + **chuẩn bị đề xuất dịch vụ** (chuyển UC3) | Có, nếu đặt lịch / tạo support case |
| D | Đề xuất dịch vụ có phương án | **Có (mức 2)** |
| E hoặc SoC khẩn | Handoff **24/7** kèm tóm tắt + hỏi cứu hộ | Cứu hộ: **có** — không tự gọi |

### Validation Rules

`claim_check` (trạm, khoảng cách, số cổng trống phải khớp tool) · trạm thay thế phải qua `core.range` (đi tới được với SoC hiện tại) · không khẳng định nguyên nhân khi `confidence` thấp · không hứa "sẽ sạc được" · urgent: handoff tạo owner trong **2 phút**.

### Customer Confirmation Requirement

Gợi ý trạm / thử lại: không cần xác nhận. Gọi cứu hộ, tạo support case, đặt lịch dịch vụ: **có** (mức 2). Handoff khẩn: thông báo cho khách, khách có thể từ chối cứu hộ.

### Executor / Write Actions

Mức 1: `create_handoff` (24/7), tạo support case ở trạng thái *chuẩn bị*. Mức 2 (sau xác nhận): đặt lịch dịch vụ qua UC3; yêu cầu cứu hộ. Mọi ghi qua Executor, idempotency, audit.

### Verification Loop

| Kiểm tra | Bằng chứng | Kết quả |
| --- | --- | --- |
| Phiên sạc kế tiếp thành công | CSMS `charging.session.completed` (kWh > 0) trong **60 phút** | `resolved` |
| Trạm thay thế dùng được | Phiên sạc mới ở trạm đề xuất thành công | `resolved` |
| Vẫn lỗi | Thêm thất bại sau tin | `failed` → retry 1 lần (hướng dẫn khác) → handoff |
| Khách chấp nhận can thiệp | Phản hồi / xác nhận | `step_done` |
| Tổng đài gọi trong **5 phút** (luồng khẩn) | `handoff.accepted_at` | SLA đạt / vi phạm |

### Failure / Retry / Handoff

- Retry tối đa **1** chu kỳ hướng dẫn; thất bại tiếp → handoff (không vòng lặp vô hạn).
- `station_health = unknown` → coi như mơ hồ → Agent, hoặc handoff nếu urgent.
- Queue nhân viên đóng ngoài giờ → **24/7** (khẩn) hoặc ticket có hẹn giờ cụ thể (thường); **không** để handoff rơi.
- Khách muốn gặp người, bực, hoặc SoC khẩn → handoff ngay.

### Customer UX

Tin ngắn gọn: *điều đã xảy ra (2 lần thất bại, trạm cách bao xa) · việc nên làm ngay · thời hạn · người phụ trách · vì sao nhận tin*. Bản đồ trạm thay thế + khoảng cách + số cổng trống (nguồn CSMS, giờ). Trạng thái "đang theo dõi phiên sạc kế tiếp". Nút Gặp nhân viên và Cần cứu hộ.

### CSKH / Staff UX

Handoff khẩn hiện: SoC, vị trí (nếu có đồng ý), trạm, số lần thất bại, giả thuyết xếp hạng + bằng chứng, trạm thay thế đã gửi, việc đã hứa. Bảng điều khiển trạm: trụ thất bại lặp lại → ticket bảo trì (root cause).

### Synthetic Data Required

*Synthetic / illustrative scenario for MVP.*

- Xe **VF 6 "anh Tuấn"**, SoC 18%, 2 lần `PLUG_HANDSHAKE_FAIL` **[SYNTHETIC — mã lỗi giả lập]** trong 12 phút tại trạm Thanh Xuân; trạm có 7/8 phiên gần đây thành công (`healthy`).
- Lịch sử: 2 lần handshake thất bại ở 2 trạm khác trong 30 ngày; cập nhật phần mềm 09/9.
- 5 trạm CSMS giả lập (1 `faulted`, 4 `healthy`), cổng trống thay đổi theo thời gian.
- Kịch bản đối chứng: trạm `faulted` (đường tất định, 0 token); SoC 6% (urgent → 24/7).
- Chuyến đi thứ Bảy đã lưu **[ASSUMPTION]**.

### Concrete Demo Scenario

*Synthetic / illustrative scenario for MVP.* Anh Tuấn, VF 6, thứ Sáu 20:42 — chưa gọi ai.

| Bước | Thời điểm | Chuyện gì xảy ra | Đầu vào → Đầu ra | LLM? |
| --- | --- | --- | --- | --- |
| **T0** | 20:42 | Phiên sạc thứ 1 thất bại tại trạm Thanh Xuân #4 | `charging.session.failed` | Không |
| **T+10 phút** | 20:52 | Phiên thứ 2 thất bại (cùng xe, 10 phút sau) | `charging.session.failed` | Không |
| **T+10 phút, 0,2 s** Detector | 20:52 | ≥ 2 thất bại / 30 phút ✓ · `station_health = healthy` (7/8 phiên khác thành công) · 2 thất bại ở trạm khác trong 30 ngày · không khiếu nại · SoC 18% (không urgent) | → `CandidateFriction(UC2, station_health=healthy)` | **Không** |
| Candidate + Arbitration | 20:52 | 20:52 ngoài giờ yên tĩnh; 0/3 tin tuần này | → `allowed` | Không |
| Ngữ cảnh | 20:52 | `get_charging_history`, `get_station_status`, `find_chargers` (đi tới được với 18%), KB thử lại, chuyến đi thứ Bảy | → `ContextBundle` | Không |
| Decision gate | 20:52 | Trạm khoẻ nhưng xe thất bại lặp lại → rule tất định **không đủ** | → `escalate_to_L2` | Không |
| **Agent được gọi** | 20:53 | Xếp hạng: B (xe / tài khoản) cao nhất · C thấp · D chưa đủ bằng chứng. Chọn: *thử cổng khác* + *trạm thay thế 2,1 km* + *chuẩn bị đề xuất dịch vụ*, nói rõ "chưa xác định được nguyên nhân" | → `InterventionProposal` | L2 (~2.200 token) |
| Validator | 20:53 | `claim_check` ✓ (2,1 km, 3 cổng trống khớp CSMS) · `core.range` ✓ · không khẳng định nguyên nhân ✓ | → `approved_to_send` | Không |
| Tin gửi | 20:53 | Hướng dẫn thử cổng #2 + trạm thay thế + "vì sao anh nhận tin" + nút Gặp nhân viên | → app + push | Mẫu tin |
| Khách phản hồi | 20:58 | Anh Tuấn thử cổng #2: thành công | `charging.session.completed` | Không |
| **Verify** | 20:59 | Phiên mới `completed`, kWh > 0 trong 60 phút | `VerificationResult(resolved)` | Không |
| Resolved | 21:00 | Đóng journey. **Vẫn ghi** lịch sử 3 lần thất bại → nếu lặp lần 4 trong 30 ngày, tạo `prepare_service_option` (UC3) | — | — |

**Biến thể tất định (không Agent):** trạm `faulted` → đường 1 → mẫu tin + trạm gần nhất, 0 token, vẫn verify bằng phiên sạc kế tiếp. **Biến thể khẩn:** SoC 6% → `priority=urgent` → handoff 24/7 trong 2 phút kèm trạm gần nhất, **không** chờ Agent.

### Cost Tier

**TB / CAO — chỉ khi mơ hồ.** Đường tất định: 0 token. Đường Agent: chỉ khi trạm khoẻ mà xe vẫn lỗi lặp lại.

### Success Criteria

Mục tiêu thiết kế — chưa đo: handoff khẩn có owner trong **2 phút** · tổng đài gọi trong **5 phút** · tỉ lệ phiên sạc kế tiếp thành công sau can thiệp (đo trên giả lập) · **0** câu khẳng định nguyên nhân khi confidence thấp · đường tất định dùng 0 token · 0 tự gọi cứu hộ khi chưa đồng ý.

### Out of Scope / Safety Boundaries

Không chẩn đoán kỹ thuật chắc chắn; không tự gọi cứu hộ; không điều khiển trạm hay xe từ xa; không dữ liệu khách thật; không tích hợp CSMS V-Green thật. Dấu hiệu nguy hiểm (khói, mùi khét, nhiệt độ bất thường) → SafetyPath.

### A/B/C/D Ownership

|  | Việc cần làm cho UC2 |
| --- | --- |
| **A** | Prompt 5 giả thuyết + mức tin cậy · chọn can thiệp · tin có "chưa xác định được nguyên nhân" · handoff khẩn |
| **B** | Sự kiện phiên sạc + CSMS giả lập · `find_chargers` · `get_charging_history` / `get_station_status` · rule detector + cooldown + tương quan trạm · tiêm kịch bản (trạm khoẻ / hỏng / SoC thấp) |
| **C** | Màn hình trạm thay thế · tin khẩn · "đang theo dõi phiên sạc" · console handoff khẩn |
| **D** | Luồng 24/7 + SLA 2 / 5 phút · verifier phiên sạc · validator `core.range` · eval 3 biến thể · đo token từng đường |
