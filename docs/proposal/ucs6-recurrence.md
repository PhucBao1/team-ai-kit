# PL-A6 · SPEC ONLY · closed-loop — UC6 — Recurrence / Return-of-Friction Prevention

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

> **Ghi chú 06/10 ([business discovery lại](../research/2026-10-06-business-discovery.md)):** lỗi tái phát ở VinFast chỉ có đoạn trích diễn đàn, chưa có tần suất —
> **không pitch như pain đã chứng minh**. Phần còn giá trị là "chỉ coi là xong khi đã xác minh" → card A2.23 (trạng thái "Đã xác minh").

Khép vòng chăm sóc: phát hiện tín hiệu quay lại sau khi case đã đóng, đánh giá lần can thiệp trước, can thiệp lại hoặc escalate.

**UC6 — spec / scenario only tuần này; khép vòng chăm sóc.** UC6 là điều làm cho "xong" nghĩa là *được xác minh*, không chỉ *đã đóng lệnh*. Mọi kịch bản là *Synthetic / illustrative scenario for MVP*.

### Goal

Phát hiện **friction quay lại** sau khi một case đã được đóng là resolved, trước khi khách phải gọi lại và kể lại từ đầu; đánh giá xem lần can thiệp trước có thật sự giải quyết vấn đề, rồi can thiệp lại hoặc escalate.

### Customer Pain

Vừa sửa xong vài ngày, cảnh báo lại sáng. Khách phải gọi, kể lại, và không biết có mất tiền không. Doanh nghiệp ghi "sửa đúng lần đầu" nhưng thực tế thì không.

### Why Proactive?

Tín hiệu tái phát nằm trong telematics — xưởng không thấy sau khi đóng lệnh. Khách có thể chưa để ý hoặc đang bực. Phát hiện sớm thì ưu tiên sửa lại và xin lỗi trước khi khách phải mở case; đồng thời sửa chỉ số chất lượng bị sai.

### Trigger Signals

| Tín hiệu | Nguồn | Vai trò |
| --- | --- | --- |
| `vehicle.dtc.raised` cùng hệ thống **sau** `repair_order.closed` | Telematics + DMS | Tín hiệu chính |
| Case cũ ở trạng thái `resolved` và còn trong `verify_until` | Journey | Điều kiện |
| Chi tiết lần xử lý trước (hạng mục, linh kiện, ghi chú kỹ thuật) | DMS | Ngữ cảnh |
| Không có case / lịch đang mở | CRM / DMS | Điều kiện loại trừ |

### What Happens Before the Customer Contacts Support

Hệ thống liên kết tín hiệu mới với lệnh sửa vừa đóng, so thời gian, và đã có đánh giá "lần trước có thể chưa triệt để" trước khi khách gọi. Khách nhận tin check-in có kèm xin lỗi và lựa chọn kiểm tra lại.

### L0 Detector — NO LLM

| Bước | Rule |
| --- | --- |
| 1 | Tồn tại RO đã `closed` / case `resolved` cho **cùng hệ thống**, trong **30 ngày** |
| 2 | Tín hiệu liên quan xuất hiện lại: WARNING ≥ 1 lần, hoặc INFO ≥ 2 lần (ngưỡng tái phát **[POLICY]**) |
| 3 | Dedupe `(vin, system, case_id)`; cooldown 7 ngày |
| 4 | Không có case / appointment mở cho hệ thống đó |
| 5 | CRITICAL → **SafetyPath**, không qua UC6 |

Kết quả: `CandidateFriction(UC6)` kèm `previous_case_id`, `days_since_closed`, `recurrence_count`. **Không LLM.**

### Context / Evidence Required

Case / RO trước: hạng mục đã sửa, linh kiện thay, ghi chú kỹ thuật, ngày đóng, người xử lý · tín hiệu mới: mã, lần xuất hiện, SoC / odometer · khoảng thời gian giữa hai lần · số lần tái phát · chính sách chi phí comeback **[ASSUMPTION: không tính phí]** · KB hướng dẫn.

### Why an Agent Is Necessary

Rule biết "cùng hệ thống, trong 30 ngày". Rule **không biết** lần can thiệp trước có đúng với nguyên nhân khả dĩ của tín hiệu mới hay không: phải so hạng mục đã sửa với mã mới, xem thời gian giữa hai lần, mức lặp lại, và quyết định *check-in nhẹ*, *đề nghị kiểm tra lại*, *mở lại có ưu tiên*, hay *escalate chất lượng*.

### Exact Agent Reasoning Task

(1) Tín hiệu mới có cùng hệ thống / cùng nguyên nhân khả dĩ với lần sửa trước không (so hạng mục, linh kiện)? (2) Khoảng thời gian và số lần tái phát nói gì về việc lần can thiệp trước **có thật sự giải quyết** không? (3) Can thiệp nào phù hợp: check-in, kiểm tra lại, mở lại, escalate? (4) Cần khách xác nhận không? (5) Cần người (trưởng kỹ thuật) không? Đầu ra: `InterventionProposal`. **Không** kết luận nguyên nhân gốc; **không** quy lỗi cho xưởng trong tin gửi khách.

### Tools the Agent May Call

Mức 0: `get_vehicle_status` · `explain_dtc` · `list_jobs` · `get_maintenance_history` (sau MVP) **[mới]** · `get_repair_order(ro_id)` **[mới]** · `find_options` (khi cân nhắc mở lại → UC3). Mức 1: `reopen_case` (chuẩn bị, trạng thái *chờ khách / chờ xưởng*) · `create_handoff`.

### Decision / Intervention Options

| Can thiệp | Khi nào | Xác nhận khách |
| --- | --- | --- |
| `explain` + check-in | Tái phát nhẹ, KB có hướng dẫn | Không |
| Đề nghị kiểm tra lại (`prepare_service_option`) | Tái phát lần 1 cùng hệ thống | **Có**, khi đặt lịch (qua UC3, mức 2) |
| `reopen_case` ưu tiên | Cùng hạng mục, < 30 ngày | Mở nội bộ mức 1; **đặt lịch cần khách xác nhận** |
| `handoff` / escalate | Tái phát **lần 2** hoặc bằng chứng mâu thuẫn | Không |
| `no_action` | Tín hiệu không liên quan | Không |

### Validation Rules

`claim_check` · tin xin lỗi phải **không** quy lỗi / khẳng định nguyên nhân · chi phí comeback chỉ theo chính sách (không hứa miễn phí nếu chưa có chính sách) · giới hạn **tối đa 2 chu kỳ tự động** cho một hệ thống rồi bắt buộc người xem xét · Executor idempotent theo `(case_id, cycle)`.

### Customer Confirmation Requirement

Tin check-in: không cần xác nhận. Đặt lịch kiểm tra lại: **bắt buộc (mức 2)** qua UC3. Mở lại hồ sơ nội bộ: mức 1 (khách không phải xác nhận) nhưng được thông báo.

### Executor / Write Actions

Mức 1: `reopen_case` (mở lại lệnh cũ, giữ slot ưu tiên chờ khách chọn) · `create_handoff` · journey cập nhật. Mức 2 (sau xác nhận): đặt lịch qua UC3. Audit append-only.

### Verification Loop

| Kiểm tra | Bằng chứng | Kết quả |
| --- | --- | --- |
| Khách được báo | Tin đã gửi + mở | `informed` |
| Kiểm tra lại đã xảy ra | `repair_order` mới / chạy thử | `rechecked` |
| Vấn đề hết | Telematics **30 ngày** không ghi nhận lại | `resolved` |
| Lại tái phát | Tín hiệu xuất hiện lại | `recurred` → chu kỳ kế (≤ 2) → escalate |

### Failure / Retry / Handoff

- Tái phát lần 2 → **handoff** trưởng kỹ thuật + báo cáo chất lượng, không tự mở lại lần 3.
- Khách không chọn giờ → nhắc 1 lần rồi giữ slot ưu tiên theo hạn.
- CRITICAL → SafetyPath.
- Khách bực / muốn người → handoff kèm card (có lịch sử lần trước, không làm khách kể lại).

### Customer UX

Tin xin lỗi, giải thích ngắn: *hệ thống ghi nhận cảnh báo X xuất hiện lại sau lần sửa ngày D*; hồ sơ đã mở lại ưu tiên; chọn giờ trong app. Vì sao nhận tin. "Việc của tôi" hiện **lịch sử lần trước** và bước Xác minh mới.

### CSKH / Staff UX

Card: lần sửa trước (hạng mục, linh kiện, ngày), tín hiệu mới, khoảng thời gian, số chu kỳ. Trưởng kỹ thuật thấy báo cáo comeback theo hạng mục / xưởng (chất lượng sửa chữa).

### Synthetic Data Required

*Synthetic / illustrative scenario for MVP.* Xe **VF 7 "chị Mai"**: RO-5402 sửa hệ thống điều hoà, đóng 20/9 · mã điều hoà xuất hiện lại 23/9 (3 ngày sau) · `verify_until` = 20/10 · không case mở · một kịch bản tái phát **lần 2** (escalate) · một kịch bản tín hiệu **không liên quan** (`no_action`).

### Concrete Demo Scenario

*Synthetic / illustrative scenario for MVP.* Chị Mai chưa liên hệ.

| Bước | Thời điểm | Chuyện gì xảy ra | Đầu vào → Đầu ra | LLM? |
| --- | --- | --- | --- | --- |
| **T0** | Thứ Tư 23/9 07:40 | `vehicle.dtc.raised` mã điều hoà (WARNING) | event | Không |
| **T+1 s** Detector | 07:40 | RO-5402 cùng hệ thống đóng 3 ngày trước ✓ · WARNING ≥ 1 ✓ · không case mở ✓ · dedupe ✓ | → `CandidateFriction(UC6, previous=RO-5402, days=3, count=1)` | **Không** |
| Arbitration | 07:40 | 07:40 đã qua giờ yên tĩnh (hết lúc 07:00) ✓ · 0/3 tin tuần này | `allowed` | Không |
| Ngữ cảnh | 07:41 | RO-5402 (hạng mục, linh kiện), lịch sử mã, KB | `ContextBundle` | Không |
| **Agent được gọi** | 07:41 | So hạng mục đã sửa với mã mới: cùng hệ thống, sau 3 ngày → *khả năng lần trước chưa giải quyết triệt để*; chọn `reopen_case` ưu tiên + kiểm tra lại; cần khách chọn giờ; chưa cần người (lần 1) | `InterventionProposal` | L2 (~2.000 token) |
| Validator | 07:42 | Tin xin lỗi không quy lỗi ✓ · `claim_check` ✓ · chu kỳ 1/2 ✓ | `approved` | Không |
| Executor (mức 1) | 07:42 | Mở lại RO-5402, giữ slot ưu tiên chờ khách | audit | Không |
| Tin khách | 08:00 | Xin lỗi + chọn giờ (đặt lịch = mức 2, qua UC3) | → app | Mẫu tin |
| Khách chọn | 08:20 | 9:00 thứ Hai tuần sau | `POST /confirm` | Không |
| **Verify** | +30 ngày | Sửa lần 2 xong; telematics 30 ngày không ghi nhận lại | `resolved` | Không |
| Resolved / handoff | — | Nếu **tái phát lần 2** → handoff trưởng kỹ thuật + báo cáo chất lượng (không mở lại lần 3 tự động) | — | — |

**Closed-loop care** (khép vòng chăm sóc): Detect → Act → Verify → Observe outcome → Detect recurrence. UC1 phát hiện và can thiệp; UC3 thực hiện; Verify đóng vòng; UC6 canh tín hiệu quay lại và mở vòng mới.

### Cost Tier

**TB / CAO.** Detector tất định; Agent cho suy luận tái phát. Giới hạn 2 chu kỳ chặn chi phí vô hạn.

### Success Criteria

Mục tiêu thiết kế — chưa đo: thời gian phát hiện comeback (từ tín hiệu tới tin) · Comeback Rate theo hạng mục / xưởng báo cáo được · **0** tin quy lỗi cho xưởng / khẳng định nguyên nhân · không vòng lặp tự động quá **2** chu kỳ · mọi `recurred` sau chu kỳ 2 chuyển người.

### Out of Scope / Safety Boundaries

Không kết luận nguyên nhân gốc, không quy lỗi, không hứa miễn phí ngoài chính sách · CRITICAL → SafetyPath · không tự chẩn đoán · không dữ liệu / DMS thật · chi phí comeback là **[ASSUMPTION]** chờ chính sách.

### A/B/C/D Ownership

Tuần này **chỉ tài liệu**. Backlog:

|  | Việc tương lai cho UC6 |
| --- | --- |
| **A** | Prompt so case cũ với tín hiệu mới · tin xin lỗi không quy lỗi · luật 2 chu kỳ |
| **B** | Case đóng + `verify_until` + rule tái phát + cooldown · seed chị Mai · `repair_order.closed` mở vòng xác minh |
| **C** | Tin check-in · hiển thị lịch sử lần trước · báo cáo comeback cho trưởng kỹ thuật |
| **D** | Giới hạn chu kỳ · verifier 30 ngày · escalate lần 2 · eval comeback |
