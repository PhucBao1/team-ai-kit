# PL-A1 · flagship · FULL — UC1 — Preemptive Service Friction Rescue

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Khách chưa đặt lịch, chưa mở ticket, chưa hỏi — hệ thống đã thấy friction dịch vụ đang hình thành, điều tra, chủ động can thiệp và xác minh.

> **Ghi chú 06/10:** mọi mã lỗi (`BATT-COOL-01`…) và ngưỡng (3 lần / 14 ngày, cooldown 7 ngày) trong UC1 là **giả lập cho demo**, chưa có xác nhận kỹ thuật. Cảnh báo của xe (do xe tự hiện) khác với outreach CSKH (do agent gửi). Mã lỗi không đủ để kết luận bộ phận hỏng — xưởng kiểm tra mới kết luận. VinFast đã công bố báo lỗi từ xa cho VF e34 từ 2021 → UC1 là cửa vào, không phải điểm mới.

**UC1 là flagship.** Khách chưa đặt lịch, chưa mở ticket, chưa khiếu nại, chưa hỏi trợ lý — nhưng hệ thống đã thấy một chuỗi tín hiệu cho thấy friction dịch vụ đang hình thành. Mọi kịch bản dưới đây là *Synthetic / illustrative scenario for MVP*.

### Goal

Chăm sóc khách **trước khi** họ phải tự đặt lịch hoặc mở case: phát hiện friction dịch vụ đang hình thành từ tín hiệu lặp lại của xe, điều tra bằng ngữ cảnh liên quan, chọn can thiệp rẻ nhất mà vẫn an toàn, và xác minh kết quả.

### Customer Pain

Cảnh báo không nguy hiểm cứ lặp lại nhưng khách không biết có nghiêm trọng không, có cần đi xưởng không, đi lúc nào thì đỡ mất công. Khách thường chỉ hành động khi cảnh báo trở nên khó chịu hoặc sát một chuyến đi — lúc đó thường phải chen lịch, chờ linh kiện, hoặc bị từ chối.

### Why Proactive?

- Cửa sổ rẻ nhất để can thiệp là **trước** khi khách tạo case: còn thời gian chọn slot, giữ linh kiện, hướng dẫn tự xử lý.
- Tín hiệu đã nằm sẵn trong telematics — khách không phải kể lại gì.
- Một tín hiệu đơn lẻ là nhiễu; **lặp lại + có lịch sử liên quan + sắp ảnh hưởng nhu cầu dùng xe** mới là friction. Con người không theo dõi nổi quy mô này, rule tất định thì làm được rẻ.

### Trigger Signals

Sự kiện bắt đầu là **tín hiệu hệ thống**, không phải hành động của khách:

| Tín hiệu | Nguồn | Vai trò |
| --- | --- | --- |
| `vehicle.dtc.raised` mức WARNING, cùng hệ thống, lặp lại | Telematics | Tín hiệu chính |
| `repair_order` / `maintenance_history` liên quan hệ thống đó | DMS | Ngữ cảnh |
| Kế hoạch dùng xe sắp tới (chuyến đi đã lưu, có đồng ý chia sẻ) | App | Ngữ cảnh — vì sao friction sắp quan trọng **[ASSUMPTION]** |
| Không có `appointment`, `ticket`, `handoff`, khiếu nại đang mở | DMS / CRM | Điều kiện loại trừ |

### What Happens Before the Customer Contacts Support

Khách **không** làm gì cả. Hệ thống tự: đếm tín hiệu lặp → tạo candidate → kiểm tra có được phép liên hệ không → gom ngữ cảnh → quyết định cần suy luận hay không → (nếu cần) Agent điều tra → gửi một tin chủ động có giải thích "vì sao anh nhận tin này" kèm lựa chọn. Khách chỉ **phản hồi** khi đã có sẵn phương án.

### L0 Detector — NO LLM

Rule tất định, đăng ký trong `detect/rules.py`. **Không gọi LLM.** Ngưỡng bên dưới là **[POLICY]** khởi đầu, chỉnh bằng dữ liệu giả lập (§28).

| Bước | Rule | Nếu không đạt |
| --- | --- | --- |
| 1. Độ nghiêm trọng | `severity = WARNING`. CRITICAL → **SafetyPath** (mẫu duyệt sẵn + 24/7, không đi UC1). INFO → gộp, không tạo candidate | Dừng |
| 2. Tín hiệu lành tính đã biết | Mã có cờ `known_safe_transient` và tự xoá ≤ 1 lần → bỏ qua **[ASSUMPTION: cột mới trong `dtc_codes`]** | Dừng |
| 3. Ngưỡng + cửa sổ | ≥ **3** lần cùng hệ thống trong **14 ngày**, lần cuối ≤ 24 giờ | Dừng |
| 4. Dedupe | `dedupe_key = (vin, system, iso_week)`; cooldown 7 ngày sau một tin UC1 cho cùng khoá | Dừng, ghi `suppressed: duplicate` |
| 5. Không có case | Không có appointment / RO / ticket / handoff mở cho cùng hệ thống; không có khiếu nại trong 7 ngày | Dừng, ghi `suppressed: active_case` |

Kết quả: `CandidateFriction(uc_type=UC1)` (trong code: `Candidate` ở `src/models/schemas.py`, `type="UC1_SERVICE_FRICTION"`, agent giữ alias `T0_DTC_WARNING` — B2.17, A2.18). Sau đó **Contact Arbitration** (cũng không LLM): khách không đang chat với nhân viên · không trong giờ yên tĩnh (**21:00–08:00**, trừ an toàn) · ngân sách chú ý **≤ 1 tin / việc / ngày** và **≤ 2 tin / khách / ngày** (khớp B2.04; trần theo tuần chỉ áp cho upsell để không chặn tin cứu lịch khẩn; tin quảng cáo còn phải theo NĐ 91/2020: 07:00–22:00, ≤ 3 tin / 24 h, có đồng ý trước — xem `../research/2026-10-03-nghiep-vu-vinfast.md`) · đã đồng ý nhận thông báo dịch vụ. Bị chặn → ghi `suppressed` + lý do, thử lại theo lịch.

### Context / Evidence Required

`ContextBundle` gồm (mỗi fact có nguồn, thiếu thì ghi "chưa có"):

- Trạng thái xe: model, odometer, SoC, `sw_version`, DTC đang có (`get_vehicle_status`)
- Các lần xuất hiện gần đây của tín hiệu: thời điểm, odometer, SoC (`get_recent_events`)
- Giải thích mã: severity, `remote_fixable`, `self_help`, `kb_ref` (`explain_dtc`)
- Lịch sử dịch vụ / bảo dưỡng liên quan hệ thống đó (`get_maintenance_history` — **sau MVP**; MVP dùng lý do bảo dưỡng trong kết quả `check_warranty`)
- Hành trình của khách và lời hứa đang mở (`list_jobs`); chuyến đi sắp tới nếu có đồng ý
- Bảo hành **sơ bộ** nếu cần cho quyết định (`check_warranty` → "đủ điều kiện sơ bộ" + lý do, không kết luận)
- Năng lực dịch vụ / linh kiện / slot — **chỉ** khi Agent cân nhắc can thiệp xưởng (qua `find_options`, thuộc UC3)

### Why an Agent Is Necessary

Detector chỉ biết "lặp 3 lần, chưa có case". Quyết định *làm gì cho khách này* cần cân nhiều nguồn cùng lúc, không có rule đơn giản:

- Cùng một mã lặp có thể cần *hướng dẫn tự xử lý* (KB cho phép) hoặc *kiểm tra tại xưởng* — tuỳ phiên bản phần mềm, lịch sử sửa, khả năng sửa từ xa.
- Có chuyến đi sắp tới hay không làm thay đổi mức khẩn **về mặt trải nghiệm** (không phải mức an toàn).
- Phải chọn kênh, giọng điệu, mức chi tiết, và quyết định có nên đề xuất phương án xưởng hay chỉ giải thích.
- Phải nhận ra khi bằng chứng không đủ → hỏi thêm hoặc chuyển người thay vì đoán.

**Nếu rule đủ** (ví dụ mã cho phép sửa từ xa bằng cập nhật phần mềm **và xe đủ điều kiện FOTA của VinFast: pin > 20 %, đỗ, không sạc** — pin thấp thì hướng dẫn sạc trước; khách đã đồng ý trước đó) → đi đường tất định, **không gọi Agent**.

### Exact Agent Reasoning Task

Agent nhận `ContextBundle` và phải trả `InterventionProposal` trả lời đủ 8 câu hỏi (mỗi câu có `evidence_refs`):

1. Đây có thực sự là friction đáng can thiệp không?
2. Bằng chứng nào ủng hộ đánh giá đó?
3. Mức khẩn theo **chính sách** (không phải chẩn đoán kỹ thuật)?
4. Hướng dẫn tự xử lý (từ KB) có đủ không?
5. Có cần can thiệp tại xưởng không?
6. Nếu cần: phương án nào thoả mọi ràng buộc (xe, vấn đề, linh kiện, kỹ thuật viên, ràng buộc của khách)? → gọi UC3, không tự xếp lịch ở đây.
7. Khách có cần xác nhận không?
8. Có nên chuyển người không?

**Agent không được:** kết luận chẩn đoán xe (chỉ trình bày "hệ thống ghi nhận cảnh báo X lặp N lần", nguyên nhân do xưởng kết luận) · kết luận bảo hành (chỉ "đủ điều kiện sơ bộ" + lý do) · tự đưa lời khuyên an toàn ngoài KB · ghi dữ liệu trực tiếp.

### Tools the Agent May Call

Chỉ tool **đọc** (mức 0). Tên đã có trong §11: `get_vehicle_status` · `explain_dtc` · `check_warranty` · `list_jobs` · `find_options` (chỉ để kiểm tra khả thi; khoá slot tạm). Tool mới **[đề xuất, chưa có trong contract]**: `get_recent_events(vin, window)` · `get_maintenance_history(vin)` · `get_planned_trips(customer_id)` (cần consent). `create_handoff` (mức 1) khi chuyển người. Agent **không** có `book_appointment` / `reschedule` / `trigger_remote_update`: các tool ghi chỉ chạy qua Executor sau khi khách xác nhận.

### Decision / Intervention Options

| `intervention_type` | Khi nào | Cần xác nhận khách? |
| --- | --- | --- |
| `explain` | Friction thật nhưng chưa cần hành động; khách chỉ cần biết và được trấn an đúng mức | Không |
| `self_help` | KB có hướng dẫn cho mã này, bằng chứng nghiêng về tự xử lý | Không (khách tự làm) |
| `prepare_service_option` | Cần xưởng; chuẩn bị 2–3 phương án **chưa ghi** | Không (chỉ chuẩn bị) |
| `ask_confirmation` + `service_action` | Khách chọn phương án → UC3 đặt lịch | **Có (mức 2, token)** |
| `handoff` | Bằng chứng mâu thuẫn, khách muốn gặp người, tín hiệu nghi ngờ an toàn, confidence thấp | Không |
| `no_action` | Đánh giá không đủ ý nghĩa; ghi lý do và đóng | Không |

### Validation Rules

Chạy sau Agent, trước khi gửi / ghi (D sở hữu validator; **không LLM**):

- `claim_check(message, evidence)`: mọi con số, mã, ngày trong tin phải khớp kết quả tool; lỗi → trả lỗi cụ thể cho Agent sửa (≤ 2 lần) rồi handoff.
- Cụm từ cấm: kết luận bảo hành chắc chắn, khẳng định nguyên nhân hỏng, lời khuyên an toàn không có trong KB.
- Severity vẫn không phải CRITICAL tại thời điểm gửi (nếu đã tăng → SafetyPath).
- Arbitration (code của B) được gọi lại ngay trước khi gửi (khách có thể vừa mở chat).
- Tin có đủ 5 phần: điều đã xảy ra · phương án · thời hạn · người phụ trách · **vì sao anh/chị nhận tin này**.
- Với hành động ghi: 6 check của validator đặt lịch (proposal §08, chi tiết ở UC3): (`customer_verified` · `part_matches_vin` · `technician_certified` · `part_reserved` · `slot_locked` · `customer_confirmed`).

### Customer Confirmation Requirement

- **Gửi tin chủ động, giải thích, self-help:** không cần xác nhận — nhưng phải qua arbitration và có "vì sao nhận tin", có nút "Gặp nhân viên", có quyền tắt tin chủ động.
- **Đặt / đổi lịch, giữ linh kiện, cập nhật từ xa:** **bắt buộc** confirmation token do khách tạo khi bấm Xác nhận, sau khi tin nhắc lại đủ tham số (việc, xe, giờ, xưởng, thời lượng).
- **Chuyển người:** khách có thể yêu cầu bất kỳ lúc nào; Agent cũng chủ động chuyển theo điều kiện handoff.

### Executor / Write Actions

Agent **không ghi**. Sau khi khách xác nhận: `POST /confirm {token}` → validator → Executor gọi tool ghi mức 2 (`book_appointment` / `reschedule`, idempotency_key = hash(option_id, token)) → saga nếu nhiều hệ thống. Ghi mức 1 (tạo journey `proactive_friction`, promise "hệ thống sẽ kiểm tra lại sau N ngày", `create_handoff`) đi qua Executor tất định, không cần token. Mọi ghi vào `audit_log` append-only.

### Verification Loop

| Kiểm tra | Bằng chứng | Khi nào | Kết quả |
| --- | --- | --- | --- |
| Tin đến khách và khách thấy | Trạng thái gửi + mở tin | Ngay | `pending` → tiếp |
| Khách chọn hành động | Phản hồi trong app; không phản hồi sau 24 giờ → nhắc 1 lần (qua arbitration); 72 giờ không phản hồi → đóng `no_response`, không nhắc thêm | 24–72 giờ | `pending` / `closed` |
| Lịch đã đặt thật (nếu có) | Đọc lại appointment + reservation đúng mã, đúng xưởng | Sau ghi | `resolved_step` |
| Friction thật sự hết | Telematics: không còn tín hiệu cùng hệ thống trong **14 ngày** sau xử lý (hoặc sau tin nếu khách chỉ tự xử lý) | +14 ngày (đồng hồ giả lập) | `resolved` |
| Tái phát | Tín hiệu xuất hiện lại trong cửa sổ | trong 14–30 ngày | `recurred` → **UC6** |

### Failure / Retry / Handoff

| Tình huống | Hành vi |
| --- | --- |
| Arbitration chặn | Ghi `suppressed`, thử lại theo lịch; không tạo thêm LLM call |
| `claim_check` thất bại 2 lần | Handoff, không gửi tin |
| Khách không phản hồi | Nhắc 1 lần, rồi đóng; không spam |
| Ghi thất bại / timeout | **Không** báo "đã đặt"; đọc lại trạng thái; retry có giới hạn; báo đúng tình trạng |
| Tín hiệu leo thang CRITICAL | SafetyPath ngay, bỏ qua mọi luồng khác |
| Khách muốn gặp người / bực / Agent thất bại 2 lần | `create_handoff` với HandoffCard lắp từ dữ liệu có cấu trúc |
| Verify thất bại sau can thiệp | Retry tối đa 1 chu kỳ → chuyển UC6 / người |

### Customer UX

- Tin chủ động 5 phần (xem mẫu ở kịch bản). Có dòng **"Vì sao anh nhận tin này"**: *"xe ghi nhận cảnh báo này 3 lần trong 14 ngày và anh đã bật thông báo dịch vụ"*.
- Nút: Xem phương án · Gặp nhân viên · Tắt tin chủ động loại này.
- Màn hình "Việc của tôi" hiện journey `proactive_friction` với bước Xác minh ở cuối.
- Hiển thị nguồn của mỗi dữ kiện (KB mã lỗi vX · telematics · giờ).

### CSKH / Staff UX

Nếu handoff: HandoffCard (tóm tắt 1 câu · dữ kiện có nguồn · đã nói / hứa gì · việc tiếp theo gợi ý · **không làm**) + trace của quyết định (candidate → detector rule → evidence → Agent proposal). Nhân viên thấy vì sao hệ thống chủ động liên hệ, nên không hỏi lại biển số hay tình trạng xe.

### Synthetic Data Required

*Synthetic / illustrative scenario for MVP.*

- Xe **VF 8 "anh Minh"**: cá nhân, mua 14/03/2024, 38.420 km, SoC 42%, bảo dưỡng đủ (02/2026) — dùng lại seed §08.
- Mã làm mát pin (WARNING, không sửa từ xa, linh kiện dự kiến "bơm làm mát pin") với **3 lần xuất hiện** trong 14 ngày (23/9, 26/9, 29/9).
- Không có appointment / ticket / handoff cho hệ thống đó.
- Chuyến đi đã lưu thứ Bảy 3/10 (có consent) **[ASSUMPTION]**.
- Hai kịch bản đối chứng: (a) chỉ 1 lần xuất hiện → **không** candidate; (b) đã có appointment mở → `suppressed: active_case`.
- Tiêm sự kiện qua `/events/inject`, tua thời gian qua `/clock/advance`.

### Concrete Demo Scenario

*Synthetic / illustrative scenario for MVP.* Anh Minh, VF 8, chưa làm gì.

| Bước | Thời điểm | Chuyện gì xảy ra | Đầu vào → Đầu ra | LLM? |
| --- | --- | --- | --- | --- |
| **T0** Hệ thống nhận tín hiệu | Thứ Ba 29/9 08:15 | Telematics gửi `vehicle.dtc.raised` (mã làm mát pin, WARNING, 38.420 km, SoC 42%) | event → Pub/Sub `ops-events` | Không |
| **T+0,2 s** Detector đánh giá | 08:15 | Rule UC1: WARNING ✓ · không known-safe ✓ · lần thứ **3** trong 14 ngày (23/9, 26/9, 29/9) ✓ · dedupe mới ✓ · không có appointment / RO / ticket ✓ | 3 event → quyết định `candidate` | **Không** (0 token) |
| **T+0,2 s** Candidate tạo | 08:15 | `CandidateFriction(UC1, vin=VF8-…, count=3, window=14d, priority=normal)` | → hàng đợi arbitration | Không |
| **T+0,3 s** Arbitration qua | 08:15 | Không đang chat · 08:15 ngoài giờ yên tĩnh · 0/3 tin tuần này · có consent thông báo | candidate → `allowed` | Không |
| **T+1 s** Ngữ cảnh gom xong | 08:15 | Tool đọc: trạng thái xe, 3 lần xuất hiện, `explain_dtc` (không sửa từ xa), lịch sử bảo dưỡng, bảo hành sơ bộ, chuyến đi thứ Bảy | → `ContextBundle` (~1.500 token) | Không |
| **T+1 s** Decision gate | 08:15 | Rule tất định đủ? **Không**: nhiều nguồn + lựa chọn can thiệp. L1 triage: *không có dấu hiệu an toàn, cần xem xét dịch vụ* | bundle → `escalate_to_L2` | L1 (~300 token) |
| **T+3 s** **Agent được gọi** | 08:15 | Agent trả lời 8 câu: friction có ý nghĩa ✓ (lặp 3 lần + chuyến đi thứ Bảy) · mức khẩn bình thường · KB không có self-help đủ → cần xưởng · gọi `find_options` kiểm khả thi · cần xác nhận · chưa cần người | bundle → `InterventionProposal(prepare_service_option + ask_confirmation)` | L2 (~2.500 token) |
| **T+5 s** Validator | 08:15 | `claim_check` ✓ (mọi số khớp tool) · không có cụm từ cấm ✓ · severity còn WARNING ✓ · arbitration kiểm lại ✓ | proposal → `approved_to_send` | Không |
| **T+6 s** Tin chủ động gửi | 08:15 | Tin 5 phần + "vì sao anh nhận tin" + 2 phương án + nút Gặp nhân viên. Journey `proactive_friction` = *chờ khách chọn* | → app + push | Soạn tin (~300 token) |
| **T+8 phút** Khách xác nhận | 08:23 | Anh Minh chọn phương án, bấm Xác nhận | `POST /confirm {token}` | Không |
| **T+8 phút** Validator + Executor | 08:23 | 6 check ✓ → `book_appointment(option_id, token)` → giữ linh kiện, ghi promise | → `appointment_id`, đọc lại để xác nhận | Không |
| **T+4 ngày** Sửa xong | Thứ Bảy 3/10 11:30 | Xưởng đóng RO; journey chuyển *đang xác minh* | `repair_order.closed` | Không |
| **T+18 ngày** Xác minh | 17/10 (tua đồng hồ) | Telematics 14 ngày không ghi nhận lại mã | `VerificationResult(resolved)` | Không |
| **Kết quả** Resolved / handoff | — | `resolved` → đóng journey. Nếu tái phát → **UC6**. Nếu khách chọn "Gặp nhân viên" → handoff kèm card | — | — |

Phần xếp lịch ở bước T+3 s và bước T+8 phút chính là **UC3**. Nhánh "linh kiện bị điều đi sau khi đã đặt" được mô tả trong UC3.

**Demo story:** *Khách chưa hề nhờ giúp. Hệ thống phát hiện friction đang hình thành, điều tra bằng bằng chứng liên quan, chủ động can thiệp và xác minh kết quả.*

### Cost Tier

**CAO — nhưng chỉ cho candidate thật.** Mọi event đi qua L0 (0 token). Chỉ candidate qua ngưỡng + arbitration mới tới L1 / L2. Số liệu token ở trên là minh hoạ. Đo `llm_call_rate`, token / độ trễ theo tầng, chi phí cho mỗi việc được giải quyết và xác minh.

### Success Criteria

Mục tiêu thiết kế — **chưa đo**; đo bằng eval trên thế giới giả lập:

- **Tiêu chí chính:** khách được báo / hỗ trợ **trước khi** tự tạo appointment hoặc ticket (Pre-chase recovery ≥ 70% trên kịch bản tiêm lỗi, §22).
- Detector P/R trên bộ kịch bản có nhãn; **0** candidate sinh ra từ tín hiệu CRITICAL đi nhầm vào UC1.
- **0** tin chủ động vi phạm arbitration; **0** ghi không có xác nhận; **0** tin kết luận chẩn đoán / bảo hành.
- `llm_call_rate` được báo cáo; mọi event không phải candidate dùng 0 token.
- Verify đóng được vòng bằng đồng hồ giả lập.

### Out of Scope / Safety Boundaries

- Không chẩn đoán xe, không kết luận bảo hành, không khuyên an toàn ngoài KB, không thay kỹ thuật viên.
- CRITICAL hoặc mô tả nguy hiểm (khói, mùi khét) → SafetyPath, không qua UC1, không qua LLM.
- Không dữ liệu khách thật; không tích hợp VinFast thật; không chia sẻ vị trí khi chưa có đồng ý.
- Không "đặt lịch cho mọi vấn đề": đặt lịch là hành động do khách xác nhận.
- Mọi ngưỡng là **[POLICY]** / **[ASSUMPTION]** khởi đầu.

### A/B/C/D Ownership

|  | Việc cần làm cho UC1 |
| --- | --- |
| **A — Agent / AI** | Prompt 8 câu hỏi + `InterventionProposal` · chọn can thiệp · tin chủ động 5 phần · handoff trigger · bộ kiểm "Agent không chẩn đoán / không kết luận bảo hành" · tiêu chí thành công của Agent (đúng can thiệp, không bịa) |
| **B — Data / Tools / Giả lập** | Schema `vehicle.dtc.raised` đủ trường · rule UC1 + ngưỡng + dedupe + `known_safe_transient` · **arbitration** · context builder · tool `get_recent_events` / `get_maintenance_history` / `get_planned_trips` · seed 3 lần xuất hiện + 2 kịch bản đối chứng · `/events/inject` |
| **C — Frontend** | Thông báo chủ động + "Vì sao anh nhận tin này" · nguồn / provenance · chọn phương án + Xác nhận · journey `proactive_friction` + bước Xác minh · tắt tin chủ động · console + trace candidate → rule → evidence → proposal |
| **D — Core / API / Eval** | Validator + `claim_check` + cụm từ cấm · Executor + token + idempotency · verifier (đồng hồ giả lập) · API / Pub/Sub plumbing · eval UC1 (có kịch bản đối chứng) + hard gate · đo `llm_call_rate`, token, độ trễ |
