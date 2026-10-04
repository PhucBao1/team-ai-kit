# CSKH information architecture

The structure of the customer-service employee console: who uses it, which screens exist, how an employee moves through them, and
the models every screen shares (actions, priority, evidence). Screens are specified in [cskh-screen-spec.md](cskh-screen-spec.md);
motion in [cskh-motion-map.md](cskh-motion-map.md). Built on [MASTER](../../design-system/proactive-care/MASTER.md) and the CSKH
deviations in [pages/cskh.md](../../design-system/proactive-care/pages/cskh.md). Source: owner brief of 2026-10-03 (CSKH console).
No code; nothing here changes P-073.

**Status.** Part of design contract v1.0 (MASTER §18). The console grows from spec §20's single "Console nhân viên" panel into six screens; the product owner confirms
this in D-15. Most of it needs data the contract does not have yet (D-05, D-06, D-16). Where data is missing, a section says so in
one line; nothing is inferred.

**Dials.** VARIANCE 3, MOTION 2, DENSITY 8 (MASTER §2.1, unchanged). An operational product: fixed panes, fixed section order,
everything visible, no decoration, no cards (K-05).

---

## 1. The work loop

The brief's loop, and where each step happens:

| Step | The employee's question | Where | What makes it fast |
|---|---|---|---|
| Scan | What needs me, and how urgent is it? | K1 Tổng quan, K2 Hàng ưu tiên | One fixed priority order; deadlines as words and times; safety pinned; nothing reorders under the pointer |
| Understand | Why does this case exist, and what is true? | K4 Chi tiết ca, sections 1 to 6 | The case reads top to bottom as a chain of causes, each section answering one question, all expanded (K-10) |
| Decide | What may happen, and what must a person decide? | K4 section 6 (policy) and 7 (decision); the decision pane | Every proposed action carries its authorization verdict; one primary action at a time |
| Act | Do it, and keep the promises | The decision pane: DecisionBar, call, message | Actions with the parameters shown; the agent's promises and "Không nên" beside the buttons |
| Verify | Did it work? | K4 sections 8 and 9; the queue view "Đang xác minh"; K6 | Outcomes verified by system data, not ticket closure; recurrences shown as events |

## 2. Who uses it

| Role | Typical work | Sees | Decides |
|---|---|---|---|
| CSKH agent (tổng đài viên) | Handoffs from the AI, callbacks, customer questions the AI could not answer | Cases routed to their skill group; customer profiles as their role allows | Level 2 on the customer's behalf after a call (flow D); accept, reassign, hand back to the AI |
| Service advisor (CVDV) at a workshop | Cases for vehicles booked at their workshop: replans, parts, visits | Their workshop's cases and appointments | As the agent, plus workshop-level choices |
| 24/7 line | Safety and stranded customers, any hour | Safety cases first, everywhere | Rescue routing, safety follow-up |
| Approver (trưởng xưởng, quản lý xưởng) | Level-3 approvals: compensation, policy exceptions | The "Chờ duyệt" view for their scope | "Duyệt", "Sửa rồi duyệt", "Từ chối" |

Routing is by skill (proposal §06 E: the CVDV of the vehicle's workshop, warranty, charging, 24/7). Rights are enforced by the server;
the console states a missing right in words ("Cần trưởng xưởng duyệt") and offers the way forward, never a silent hidden button.
Out of scope: the manager dashboard (taste-rules rule 13), the technician copilot (screen-map §8).

## 3. Screens

```text
Header (every screen): Tổng quan · Hàng ưu tiên · Ma sát · Khách hàng · Nhật ký · customer search · alert slot · account

K1 Tổng quan ──► K2 Hàng ưu tiên (a view) ──► K4 Chi tiết ca (opens beside the queue at xl)
     │                                              ├──► K5 Khách hàng (the customer's profile)
     ├──► K3 Ma sát đang diễn ra ──► cluster ──► K4 └──► K6 Truy vết và nhật ký (this case)
     └──► K4 directly (a callback due, an approval waiting)
K5 Khách hàng ──► profile ──► K4 ;   K6 ──► K4 ;   K7 Phím tắt: a dialog over any screen
```

| ID | Screen | Brief item | Answers | Proposed route |
|---|---|---|---|---|
| K1 | Tổng quan | Overview | What does my shift look like right now: what needs me, what I promised, what the AI is handling, what just finished? | `/cskh` |
| K2 | Hàng ưu tiên | Priority Queue | What should I work on next, in what order? At `xl` the open case sits beside it (the workspace) | `/cskh/hang?xem=can-toi` |
| K3 | Ma sát đang diễn ra | Active Friction | What is going wrong across customers that the system is already handling, before anyone calls? | `/cskh/ma-sat`, `/cskh/ma-sat/:clusterId` |
| K4 | Chi tiết ca | Case Detail | Why this case exists, what is true, what the AI did and proposes, what policy allows, what a person must decide, what happened, whether it worked | `/cskh/ca/:caseId`, or inside K2 as `?ca=:caseId` |
| K5 | Khách hàng | Customers | Who is this person, which vehicles and rights, what is open, what was promised, what did they consent to? | `/cskh/khach`, `/cskh/khach/:customerId` |
| K6 | Truy vết và nhật ký | Trace / Audit | Who did what, when, on what evidence, and which steps used a model? | `/cskh/nhat-ky?ca=:caseId` |
| K7 | Phím tắt | (keyboard) | How do I go faster, and how do I turn shortcuts off? | Dialog, `?` |

**Entry.** `/cskh` opens K1: the shift at a glance, with the most urgent items one step away. The Landing door "Khám phá trải nghiệm
CSKH" leads here. During the shift the employee lives in K2 with K4 beside it.

**URL holds the state** (web-design-guidelines): the view, filters and open case are in the query string, so a link to a case or a
view is shareable and the back button works.

## 4. Object model

```text
Friction cluster (K3)  ─ groups ─►  Case (K4)  ─ may become ─►  Handoff (contract: Handoff)
   e.g. "Linh kiện BATT-COOL-PUMP          one customer,           a named person owns it
    bị điều chuyển ở Long Biên"            one vehicle, one goal

Case ─ has ─► signals · evidence · investigation steps · proposed actions (each with an authorization verdict)
           · decisions · executed actions · verification · audit rows
Customer (K5) ─ has ─► vehicles (role: chủ xe or người lái, quyền đặt lịch) · cases · promises · consents
```

**Case, not only handoff.** Today's contract exposes only handoffs (`GET /api/v1/handoffs`). Views such as "AI đang xử lý", "Chờ khách
xác nhận" and "Đang xác minh", and the whole of K3, need every active case (D-05). Until then those views say "Chưa có dữ liệu cho
chế độ xem này." and only the handoff views work.

## 5. The action model

The brief's eight terms are two different things, and the console keeps them apart:

- **Lifecycle state**: where the case is now and who holds the ball. Exactly the nine states of MASTER §12, with their CSKH labels,
  node shapes, icons and color families. Shown by the StateChip and the case spine.
- **Authorization verdict**: what policy allows for one proposed action, from the confirmation level (proposal §06 C) and the
  validator. Shown per action in K4 section 6 (ActionPolicyTable). A verdict is a fact about an action, so it is neutral text with an
  icon; only "Không được phép" carries `--danger`, like a validator failure (MASTER §11).

| Brief term | Kind | MASTER mapping | CSKH label | Shape and icon | Next to act | Employee can |
|---|---|---|---|---|---|---|
| Recommended | State | RECOMMENDING | Đề xuất | teal circle, `route` | The system routes it by level | Read the proposal and its reasons; "Nhận xử lý" to take over |
| Allowed | Verdict | Level 0 or 1 with the validator passed: RECOMMENDING goes straight to EXECUTING | Được phép (mức 0 or mức 1) | neutral, `shield-check` | The system | See it logged; "Tạm dừng tự động cho ca này" to take over before it runs again |
| Needs Confirmation | State (and its verdict) | WAITING FOR CUSTOMER; verdict "Cần khách xác nhận" (level 2) | Chờ khách xác nhận | amber diamond, `user-round` | The customer | "Gọi khách"; "Chốt thay khách" after a call, with the verbal consent recorded (flow D) |
| Needs Human Approval | State (and its verdict) | WAITING FOR HUMAN; verdict "Cần nhân viên duyệt" (level 3) | Cần duyệt | amber diamond, `stamp` | A staff member with the right role | "Duyệt", "Sửa rồi duyệt", "Từ chối" with a reason; "Chuyển người có quyền" |
| Executing | State | EXECUTING | Đang thực hiện | teal circle, `play`, loader in the locked button | The system (Executor) | Wait; on failure, "Thử lại" or "Nhận xử lý" |
| Verifying | State | VERIFYING, guard then window | Đang xác minh | teal circle, `gauge` | The system | Read the guard checklist or window; "Mở lại" with a reason if they know something the data does not |
| Resolved | State | RESOLVED | Đã xác minh | green filled circle with check, `circle-check` | Nobody | "Mở lại ca" with a reason |
| Escalated | State | ESCALATED | Đã chuyển người | ink square, `headset` | The named staff member | "Nhận", "Gọi lại", "Chốt phương án", "Chuyển người khác", "Trả lại cho AI" |

Completing the vocabulary:

| Term | Kind | Label | Treatment |
|---|---|---|---|
| Not allowed | Verdict | Không được phép: {luật} | `--danger` text, `circle-slash`, the rule named ("Không được phép: hứa bù đắp trước khi duyệt") |
| Detected | State | Phát hiện | teal circle, `activity`; mostly seen in K3 and the "AI đang xử lý" view |
| Investigating | State | Đang điều tra | teal circle, `file-search`; progress as text ("đã đọc 3 trên 5 nguồn") |

Verdict wording uses "Cần" (requires) and state wording uses "Chờ" (waiting for): "Cần khách xác nhận" is what policy requires of an
action; "Chờ khách xác nhận" is what the case is doing now. The two never share a chip.

## 6. Priority model

One fixed order in every queue view, so position means the same thing all shift (VARIANCE 3). The rule is shown in a tooltip on
the view heading, in words.

| Rank | Group | Why |
|---|---|---|
| 1 | Safety | MASTER §12: pinned to the top of every view |
| 2 | Callback overdue | A promise to a customer is already broken |
| 3 | Callback due within 5 minutes | About to break (K-09 thresholds) |
| 4 | Waiting on me: unassigned handoffs in my skills, approvals in my scope | Nobody else will act |
| 5 | Assigned to me, by deadline | My open promises |
| 6 | Everything else in the view, by deadline, then by age | |

Within a group, a customer whose sentiment is "Rất bực" or "Bực" comes first; sentiment is a tie-breaker, never a rank of its own,
and always shown as a word (MASTER §11). The order never changes under the pointer: re-ranked and new cases wait behind a "3 ca mới"
control, except safety, which appears at once in the header's alert slot (cskh-screen-spec.md §1).

Views (left to right in the view menu, each with its count): "Cần tôi xử lý" (default), "Chờ duyệt", "Chờ khách xác nhận",
"AI đang xử lý", "Đang xác minh", "Đã xong hôm nay". Each view is a filter of states and assignment; the order inside is always the one above.

## 7. Evidence model

Evidence is what the system read, from where, and when. It is never what the model thought.

| Kind (brief) | Example (fixtures, "Dữ liệu mẫu") | Source shown | Raw reference (K-06) |
|---|---|---|---|
| Repeated event count | "BATT-COOL-01 (WARNING) 3 lần trong 14 ngày, gần nhất 08:15 29/09" | Dữ liệu xe | `telematics:VF8-4821` |
| Service history signal | "Bảo dưỡng đủ 5 kỳ; gần nhất 05/04/2026 ở 35.100 km" | Lịch sử bảo dưỡng | `dms:maintenance` |
| Charging state | "Pin 42% lúc 08:15, đủ đi tới cả 3 xưởng" / VF6-2290: "Pin 3%, cần ít nhất 2,8 kWh để tới xưởng gần nhất" | Dữ liệu xe | `telematics:soc` |
| Station status | "Trụ … lỗi với nhiều xe trong 2 giờ qua; xe này sạc bình thường ở trạm khác" (UC2) | Trạng thái trạm sạc | Charging events are not in the contract yet (D-06) |
| Customer journey context | "Lịch A-20931, 14:00 thứ Sáu 02/10, Long Biên; linh kiện R-7702 đang giữ; không có khiếu nại mở" | DMS, ERP | `dms:A-20931`, `erp:R-7702` |
| Policy result | "Bảo hành: đủ điều kiện sơ bộ (ELIGIBLE_PRELIM) theo WARR-PASS-L 2026.03: 10 năm hoặc 200.000 km, xe cá nhân; xe 2,5 năm, 38.420 km" | Chính sách bảo hành bản 2026.03 | `kb:warranty_v2026.03§2.1` |
| Validator result | "owner_or_can_book: Đạt"; "part_matches_vin: Đạt"; "slot_locked: Chưa kiểm" | Validator | rule id |

Each evidence row: the fact in words, the source, the time it was read, and in CSKH the raw reference in `--font-mono`. Rows are
grouped by kind and always expanded (K-10).

**Never shown, on any CSKH screen:** model reasoning text or reasoning tokens; the template's free-text `analysis` field
(`ChatResponse.analysis`); prompts; anything the model wrote that a tool did not return, except the outputs it is allowed to write
(the one-line summary and the sentiment estimate, proposal §06 E), which are labelled "Trợ lý AI tóm tắt" and "ước tính của mô hình".
How the AI got somewhere is shown as **investigation steps** (tool, layer, what was asked, what came back, what was ruled out and the
rule that ruled it out), never as narrative.

## 8. Navigation and keyboard

| Mechanism | Rule |
|---|---|
| Header navigation | Five destinations in one line; the current one marked with `aria-current="page"`; customer search always available |
| Queue to case | Selecting a row (click, or `j`/`k` then `Enter`) opens the case in the case pane at `xl`, or as its own view below `xl`, with "Về hàng ưu tiên" |
| Inside a case | The section index (numbers and short names) jumps instantly; `1` to `9`, `0` jump to sections 1 to 10 |
| Shortcuts | K-07 and accessibility.md §6; a switch turns them off; no single key for consequential decisions |
| Back | Always returns to the same view, filter and scroll position |

## 9. Data today and gaps

| Need | Today (`api.yaml` v0.2.0) | Gap |
|---|---|---|
| Queue of handoffs, accept | `GET /api/v1/handoffs`, `POST /api/v1/handoffs/{id}/accept` | |
| Every active case, by state | None | D-05 |
| Case state | `Handoff.status` (free string) | D-04 |
| Case content: summary, facts with sources, promises, sentiment, next action, "Không nên", deadline | `HandoffCard` | |
| Signals, evidence read times, investigation steps with layer and actor | `TraceStep[]` per agent run (step, tool, input, output, tokens, ms) | Layer, actor, timestamp per step; case-level timeline (D-06) |
| Authorization verdicts and validator results | None | D-06 |
| Approve, reject, finalize, reassign, hand back to the AI, call log, internal note, staff message | Accept only | D-06, D-16 |
| Verification progress | None | D-06 |
| Friction clusters and suppressed candidates (K3) | None | D-16 |
| Overview counts, promises due (K1) | None | D-16 |
| Customer search and profile, with access logging (K5) | None | D-16 |
| Presence (who has a case open) and conflict locks | None | D-16 |
| Case-level audit (K6) | `/trace/{trace_id}` covers one agent run | D-06 |

## 10. Open questions

| ID | Question | Related |
|---|---|---|
| KQ-1 | Confirm the six-screen console and update spec §20 and §21, the Demo stage and task cards C1.06 and C2.01 | D-15 |
| KQ-2 | Queue scope: handoffs only, or every active case (needed for three views and K3) | D-05 |
| KQ-3 | Roles and rights: which roles approve which level-3 actions, and what each role may see in K5 | |
| KQ-4 | Click-to-call: through which telephony system, and is the call outcome logged automatically? | D-16 |
| KQ-5 | Presence and locks: does opening a case lock it for others, or only show who is in it (proposed: show, lock only while acting) | D-16 |
| KQ-6 | May staff edit the HandoffCard (proposal §09: "nhân viên là người dạy agent"), and is the edit fed back to evaluation? | |
| KQ-7 | Does "Tạm dừng tự động cho ca này" exist, and does it pause only this case or this customer? | |
| KQ-8 | Bulk actions: none for decisions (proposed); is bulk reassignment needed at shift change? | |
