# Journeys

How people move through the three surfaces, step by step, with the AI state at each step. Screens are defined in
[screen-map.md](screen-map.md); states, shapes and copy in [MASTER §12](../../design-system/proactive-care/MASTER.md). The customer
side in depth (the four questions, causality, notifications, other paths) is [customer-journey.md](customer-journey.md).

All people, vehicles, codes and times below come from `P-073/contracts/fixtures/demo_world.yaml` or the proposal's own examples.
They are **sample data** ("Dữ liệu mẫu"), not facts about real customers. Staff name "Hải" is the proposal's example advisor.

**One truth, two doors.** Customer and CSKH read the same case. At every step the customer view and the staff view show the same
state with different density; they never say two different things (proposal §08).

| Journey | Use case | Shows |
|---|---|---|
| J0 | n/a | A first-time visitor understands the product and enters it |
| J1 | UC1 flagship | From a repeated vehicle signal to a confirmed intervention; verification continues in J2 |
| J2 | UC3 replan, handoff | Parts reallocated, new options, the customer asks for a person, staff finalizes |
| J3 | Level-3 approval | WAITING FOR HUMAN: the AI prepares, a person decides |
| J4 | UC2 | Charging failure, deterministic path, verified by the next session |
| J5 | Safety | CRITICAL fault: no AI reasoning, straight to people |
| J6 | UC6 | Recurrence during verification opens a linked case |
| J7 | UC1 variant | Remote fix first; no workshop reachable on the current charge |

---

## J0. A first-time visitor (judge or decision maker)

Sections are specified in [landing-story.md](landing-story.md).

| # | Moment | Section | They see | They do |
|---|---|---|---|---|
| 1 | Arrive | S01 | "Đừng đợi khách hàng phải hỏi.", a real CareCard at 08:16 on a time axis, the customer's question days later marked "Không cần gửi", two doors | Read, or choose a door at once |
| 2 | Today's model | S02 | The reactive track: the customer notices, calls, waits, retells; action comes last | Scroll; the track builds with their scroll |
| 3 | The shift | S03 | The start moves earlier to the vehicle's signal; the burden moves to the system; the appointment is one of four interventions | Scroll |
| 4 | The mechanism | S04 | One warning becoming a verified outcome in six stages, with layer tags showing where a model is used | Scroll, or jump between stages |
| 5 | One real case | S05 | Minh's synthetic case: the phone stays quiet while CSKH sees each step, then help arrives and the fix is verified | Scroll back and forth at their own pace |
| 6 | Why an agent, and why not always | S06, S07 | Three conflicting signals only an agent can reconcile; sample events stopping at the cheapest tier | Hover or select to follow a path |
| 7 | Enter | S08 | Two doors with real previews; a quieter Demo stage link | Choose C1, K1 or D1 |
| 8 | Can I trust it? | S09 | Validation, controlled execution, verification, handoff; no diagnosis, no warranty decision | Read |
| 9 | Last choice | S10 | The same two doors | Enter C1, K1 or D1 |

**Done when** the visitor can say, unprompted, what the product does before a customer calls, and enters one surface.

## J1. UC1: from signal to intervention (Nguyễn Văn Minh, VF 8 `VF8-4821`)

Trigger: `vehicle.dtc.raised` `BATT-COOL-01` (WARNING) for the third time in 14 days, no appointment or ticket open (spec §09 rule).

| # | Moment | Screen | State | Customer sees | CSKH sees | Customer does |
|---|---|---|---|---|---|---|
| 1 | Third warning arrives, Tue 29/09 08:15 | (none) | DETECTED | Nothing yet | Queue view "AI đang xử lý": new case, rule and signal (if the scope includes it, D-05) | Nothing |
| 2 | Arbitration allows contact (not driving, within 08:00 to 20:00, no open complaint) | (none) | DETECTED | Nothing | Arbitration result in the AuditLog | Nothing |
| 3 | Context and reasoning: warranty precheck, software version, maintenance history, part prediction, reachable workshops | (none) | INVESTIGATING | Nothing (proactive case) | InvestigationSteps with LayerTags | Nothing |
| 4 | Message sent | C4, C1, C2 | RECOMMENDING then WAITING FOR CUSTOMER | CareCard: what happened, why they got it, 4 sources checked, the proposal ("kiểm tra hệ thống làm mát pin tại xưởng"), warranty "đủ điều kiện sơ bộ", options, the deadline | "Chờ khách xác nhận (mức 2)" | Opens "Em đã kiểm tra 4 nguồn" (optional) |
| 5 | Chooses Long Biên, Fri 02/10 14:00 | C2 | WAITING FOR CUSTOMER | DecisionBlock: việc, xe (30A-xxx.xx, VIN rút gọn), xưởng Long Biên, ngày giờ, chi phí "theo báo giá xưởng" | same | Taps "Xác nhận đặt lịch" |
| 6 | Executing | C2 | EXECUTING | Button locked: "Đang đặt lịch…" | "Đang thực hiện: đặt lịch" | Waits |
| 7 | Server confirms `A-20931`; part `R-7702` held | C2, C1 | VERIFYING (guard) | ConfirmationReceipt "Đã đặt lịch" with "Đổi lịch", "Huỷ lịch"; JobCard at "Chờ hẹn" | Case moves to guard | Nothing |

**This journey ends** when the server confirms the intervention. Here the intervention is a workshop booking, because investigation
found that `BATT-COOL-01` cannot be fixed remotely; the booking is a consequence of the signal, not the start of the story. The case
is not done: it is done only when verification passes (J2 step 9). The fixture world starts at the end of this journey: `A-20931` is
confirmed and `R-7702` is held. J2 continues the same case.

**Alternate path: the person is a driver without booking rights** (Trần Thu Hà on VF 9 `VF9-3055`). Step 5 fails the validator
`owner_or_can_book`. The driver sees, in words, that only the owner can confirm a booking and an action to ask the owner; nothing is
booked; the owner receives the level-2 confirmation (proposal §06, D2).

## J2. UC3 replan and handoff (same case)

Trigger: `parts.reservation.cancelled` for `R-7702` (reason: reallocated for a recall) while the confirmed appointment is less than
72 hours away (spec §09 rule `on_reservation_cancelled`).

| # | Moment | Screen | State | Customer sees | CSKH sees | Person does |
|---|---|---|---|---|---|---|
| 1 | ERP cancels the reservation, Wed 30/09 | (none) | Event (triangle), then DETECTED | Nothing yet | Event "Linh kiện bị điều đi (R-7702)" in the trace, high priority | n/a |
| 2 | Replan: options that are actually feasible | (none) | INVESTIGATING | Nothing yet | InvestigationSteps: Long Biên excluded (no part left), Gia Lâm and Hoài Đức have parts and a high-voltage bay | n/a |
| 3 | New message | C4, C1, C2 | WAITING FOR CUSTOMER | Honest change line ("lịch phải đổi vì linh kiện ở Long Biên được điều đi"), one apology, options: "Hoài Đức, 09:00 thứ Năm 01/10, 27,1 km" and "Gia Lâm, 09:00 thứ Bảy 03/10, 7,1 km"; Long Biên shown as excluded with its reason | "Chờ khách xác nhận" | Customer is annoyed: they had arranged their day |
| 4 | Customer asks for a person | C2 | ESCALATED | "Anh Hải, cố vấn dịch vụ xưởng Long Biên, sẽ gọi anh trước 14:21." | New handoff at the top: one-line summary, what the agent said and promised ("phản hồi trong 15 phút"), sentiment "Bực", "Không nên" items, DeadlineTimer | Taps "Gặp nhân viên" |
| 5 | Staff accepts | K2 | ESCALATED | Unchanged | "Nhận" sets the owner; the callback deadline starts | Hải presses "Nhận" (or `n`) |
| 6 | Call; staff finalizes Gia Lâm, Sat 03/10 09:00 | K2, K4 | EXECUTING | "Đang đổi lịch…" | DecisionBar "Chốt phương án" with the parameters | Hải confirms on the customer's behalf after the call (staff is the confirmer, flow D) |
| 7 | Server confirms | C2, C1 | VERIFYING (guard) | Receipt; JobCard: Gia Lâm, 09:00 thứ Bảy 3/10; "Thay đổi gần nhất (…): đổi sang xưởng Gia Lâm vì linh kiện ở Long Biên được điều đi. Anh đã đồng ý qua điện thoại." | Case returns to the AI (flow D step 7) | n/a |
| 8 | Repair closed, Sat 03/10 | C1, C2 | VERIFYING (window) | "Đang theo dõi kết quả: 0 trên 7 ngày" | Window 7 days | n/a |
| 9 | Seven clean days | C1, C2, C4 | RESOLVED | "Đã xử lý xong. Xe không báo lại lỗi trong 7 ngày theo dõi." | "Đã xác minh" | n/a |

**Done when** the vehicle data shows no recurrence through the window. Closing a ticket is not "done".

## J3. Level-3 approval (WAITING FOR HUMAN)

A decision involving money, safety, identity or a policy exception (proposal §06 level 3), for example a goodwill gesture under
the company's approved SOP after the disruption in J2. The AI may prepare it; it may not promise it (proposal §09: "không hứa bù đắp trước khi được duyệt").

| # | Moment | Screen | State | Customer sees | CSKH sees | Person does |
|---|---|---|---|---|---|---|
| 1 | AI prepares the file | (none) | RECOMMENDING | Nothing promised | Proposal with the SOP reference and its basis | n/a |
| 2 | Waiting for a decision | C2, K2 | WAITING FOR HUMAN | "Phương án này cần nhân viên duyệt. Bên em sẽ báo lại trước 16:00." | "Cần duyệt. Mức 3." in the "Chờ duyệt" view | n/a |
| 3 | Staff decides | K4 | EXECUTING or ESCALATED | Unchanged until a result exists | DecisionBar: "Duyệt", "Sửa rồi duyệt", "Từ chối" with a required reason | Staff decides |
| 4 | Result | C2 | VERIFYING or RESOLVED, per the action | The outcome in plain words, with who decided | Recorded in the AuditLog with the staff member as actor | n/a |

Gap: the contract has no approve or reject action (D-06). Until it exists this journey is design-only.

## J4. UC2: charging failure (Phạm Minh Anh, VF 9 `VF9-3055`, sample)

Trigger: a second failed charging session in a short period, no complaint open. The charging events are proposed in spec §09 but
not yet in `contracts/events.yaml` (D-06).

| # | Moment | Screen | State | Customer sees | CSKH sees |
|---|---|---|---|---|---|
| 1 | Second failure | (none) | DETECTED | Nothing yet | Case with the session failures |
| 2 | Deterministic path: the station is failing other vehicles too, this vehicle charged fine elsewhere | (none) | INVESTIGATING (L0) | Nothing | InvestigationSteps, no model used |
| 3 | Advice while they are still at the station | C4, C2 | RECOMMENDING | "Trụ này đang lỗi với nhiều xe. Trạm gần nhất còn trống, đi tới được với mức pin hiện tại: …" with distance; no confirmation needed (level 0) | Advice sent |
| 4 | Next session | C2 | VERIFYING (window: next session) | "Bên em sẽ kiểm tra lần sạc tiếp theo của xe." | Waiting for `charging.session.completed` |
| 5 | Session completes | C2, C3 | RESOLVED | "Lần sạc tiếp theo đã thành công. Đã xử lý xong." | "Đã xác minh" |

Ambiguous path: the vehicle fails at healthy stations; L2 investigates and may prepare a service option, which hands over to UC3 (J1 steps 4 to 7).

## J5. Safety (CRITICAL `HV-ISO-99` on `VF8-4821`)

| # | Moment | Screen | State | Customer sees | CSKH sees |
|---|---|---|---|---|---|
| 1 | CRITICAL code | C7 over any customer screen | ESCALATED (safety) | The pre-approved safety message in the `--danger` banner, "Gọi cứu hộ 24/7", no AI diagnosis, no options | Case pinned to the top of every view, safety marker, 24/7 routing |
| 2 | 24/7 staff takes it | C7 | ESCALATED (safety) | The staff member's name and what happens next | Owner set; callback deadline |

No model is involved at any step (spec §09, `SafetyPath`). Arbitration limits do not apply to safety messages.

## J6. UC6: recurrence during verification

| # | Moment | Screen | State | Customer sees | CSKH sees |
|---|---|---|---|---|---|
| 1 | Day 4 of 7: `BATT-COOL-01` again | C2, C3 | Event (triangle) | "Cảnh báo quay lại sau 4 ngày. Bên em đã mở lại việc và ưu tiên kiểm tra." | Recurrence event; new linked case, cycle 2 |
| 2 | Second cycle | C4, C2 | DETECTED onward | A new CareCard that references the first repair | Both cases linked in the trace |
| 3 | A second recurrence | C2 | ESCALATED | A named person takes over | Handoff with both cycles in the evidence |

At most two automatic cycles (spec §05 flow B, step 13); after that a person always owns the case.

## J7. Remote fix first, no workshop reachable (Lê Quốc Bảo, VF 6 `VF6-2290`)

The vehicle has `ADAS-CAM-03` (fixable remotely) and 3% charge, below what any workshop trip needs; warranty precheck is `NEEDS_WORKSHOP` (missed maintenance).

| # | Moment | Screen | State | Customer sees |
|---|---|---|---|---|
| 1 | Proposal | C4, C2 | RECOMMENDING | "Em đề xuất cập nhật phần mềm từ xa trước, xe không cần đến xưởng." Workshop options listed as excluded: "Loại: pin không đủ đi tới xưởng này"; nearest charging and mobile service offered. Warranty shown neutrally: "Cần xưởng xác nhận" with the reason |
| 2 | Confirm the update (level 2, the vehicle must be parked) | C2 | WAITING FOR CUSTOMER | DecisionBlock with the update, the vehicle and the condition "xe đang đỗ" |
| 3 | Update runs | C2 | EXECUTING | "Đang cập nhật phần mềm…" |
| 4 | Verification | C2 | VERIFYING (window: new version confirmed plus 14 days) | "Đã cập nhật. Bên em theo dõi thêm 14 ngày." |
| 5 | Clean window | C2, C3 | RESOLVED | "Đã xử lý xong." |
