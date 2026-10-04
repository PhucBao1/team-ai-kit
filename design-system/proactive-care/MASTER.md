# Proactive Care Design System: MASTER

| | |
|---|---|
| Version | 1.0.1, 2026-10-03 |
| Status | **Design contract.** Passed the design review of 2026-10-03 ([design-review.md](../../docs/frontend/design-review.md)) with all 28 required changes applied. Binding for every frontend implementation of P-073; §18 is the contract |
| Conditions | L-01 and L-02 (the Landing opening and its narrative motion) stay blocked until amendments A-01 and A-02 are merged; until then Landing ships static. Screens that depend on contract gaps (D-04, D-05, D-06, D-14, D-16) render only what the API returns. The three surface architectures await product confirmation (D-01, D-13, D-15) |
| Sign-off | Design review: approved with changes, 2026-10-03. Frontend owner (C): signature pending. Product owner: pending for D-01, D-13, D-15 |
| Covers | Landing (story), Customer experience, CSKH console, and the Demo stage that composes them |
| Precedence | Level 2, "internal design system", together with `taste-rules.md`. See [design-governance.md](../../docs/frontend/design-governance.md) |

**How to read this system.** MASTER defines the one visual language. [pages/](pages/) lists the only deviations each surface may
take, each one justified and bounded. Raw values live only in [tokens.md](tokens.md). Detail files:
[typography](typography.md) · [color](color.md) · [spacing](spacing.md) · [components](components.md) · [motion](motion.md) ·
[content](content.md) · [accessibility](accessibility.md). Screens and journeys: [screen-map](../../docs/frontend/screen-map.md),
[journeys](../../docs/frontend/journeys.md). Surface specifications: Landing [story](../../docs/frontend/landing-story.md) and
[motion](../../docs/frontend/landing-motion-map.md); Customer [journey](../../docs/frontend/customer-journey.md),
[screens](../../docs/frontend/customer-screen-spec.md) and [motion](../../docs/frontend/customer-motion-map.md); CSKH
[architecture](../../docs/frontend/cskh-information-architecture.md), [screens](../../docs/frontend/cskh-screen-spec.md) and
[motion](../../docs/frontend/cskh-motion-map.md). The record of the review: [design-review.md](../../docs/frontend/design-review.md).
Retrieval order for any agent: MASTER §18, then the rest of MASTER, then `pages/<surface>.md`, then the surface specification;
anything a page file does not list follows MASTER.

**Inheritance.** This system extends `skills/add-frontend-screen/references/taste-rules.md` (15 rules) and complies with all of
them. Two Landing deviations need a rule amendment first (A-01 for rule 15, A-02 for rule 10). Until those are merged, the rule wins.

---

## 0. The idea

Proactive care asks people to trust a system that acted before they asked. People trust what they can see, so this language makes
the AI's work visible and accountable. Every claim sits next to its evidence. Every case shows who holds it now. The interface
stays calm until a person is needed.

One signature element carries this across all three surfaces: **the Care Trace**, a line of nodes that records what happened, who
acted, and what comes next. The Landing page teaches it, the customer follows their own case on it, and CSKH staff audit cases with it.
The Landing page is, in effect, the legend for the product.

**The story** (frozen, F-02). Every surface tells the same sequence: a system signal, detection, investigation, an intervention,
verification. The intervention may be advice, a remote update, mobile service or a workshop appointment. An appointment is one
possible intervention: never the starting point, never the opening image, never "the AI rescued my booking". Done means verified by
system data, not a booking made or a ticket closed.

Design Read (taste-skill format): *Reading this as: a trust-first enterprise product with one consumer-facing surface, for car owners
(some elderly), service staff and decision makers, with an instrument-precise, evidence-first language, leaning toward a custom
token system on Be Vietnam Pro, hairline structure and one signature element.*

## 1. Design philosophy

Six principles in priority order. When two conflict, the earlier one wins.

1. **Safety and truth first.** Safety overrides every other rule on every surface. Nothing is shown as done before a system of
   record confirms it. Nothing is invented: no numbers, dates, prices or policies that a tool did not return.
2. **Show the work.** Any AI statement a person might act on is paired with its evidence, its source and its time.
3. **Make the holder visible.** At any moment the interface answers two questions: who has this case now, and what do they need?
4. **Calm by default.** Color and motion mark only the present state and exceptions. Loudness is reserved for safety.
5. **One language, three densities.** Surfaces differ in density, motion and variance (the dials), never in vocabulary, tokens or type.
6. **Plain Vietnamese, human voice.** Short sentences, concrete verbs, named people. Internal system terms stay out of customer view.

## 2. Visual personality

**Calm instrument, human hand.**

- *Instrument*: exact alignment, hairline structure, tabular figures, timestamps and sources everywhere a claim is made.
- *Human hand*: plain language, people named with their role, generous reading sizes, and ink (the human color) as the color of action.
- *Not*: mascot, magic, glow, futurism, "AI brain" imagery.

Mood references (moods, not brands to imitate): a service logbook, transit wayfinding, an instrument cluster, engineering
documentation. No OEM brand marks, colors or logos are used without written permission.

### 2.1 Design dials (authoritative values)

Scale from taste-skill: VARIANCE 1 = perfect symmetry, 10 = artsy chaos; MOTION 1 = static, 10 = cinematic; DENSITY 1 = gallery, 10 = cockpit.
**MASTER defaults equal the Customer dials.** The customer is the most sensitive audience, so the base language is tuned for them;
Landing amplifies it and CSKH compresses it. Page files hold the bounded consequences of each dial.

| Surface | VARIANCE | MOTION | DENSITY | Rationale |
|---|---|---|---|---|
| Landing | 7 | 8 | 3 | Visitors arrive cold and decide in seconds whether this is credible and distinct. Asymmetric editorial composition signals intent; 7, not 9, because enterprise credibility beats spectacle. The product's idea is a sequence in time, and motion is the most honest way to explain a sequence, so motion is high in *choreography* (tied to the reader's scroll), never in duration, looping or decoration. One idea per screen, so density is low. |
| Customer (MASTER default) | 5 | 5 | 4 | Recognizably the same product, with a few editorial moments such as the state statement at the top of a case, but predictable on a phone for older readers. Customers are not watching continuously, so motion confirms that something changed (a message arrived, a step completed). One task at a time, large type. |
| CSKH | 3 | 2 | 8 | Predictability is speed: fixed panes and a fixed section order build muscle memory. Staff use the console hundreds of times a day, and the motion rule for that frequency is "no animation": the employee's own actions never move, and changes arriving from the server get only a faint opacity cue (K-03). A handoff must be understood in about 10 seconds (proposal §08), so everything is visible and scannable, with no cards. |

Frozen in v1.0 (§18.1, F-04). D-11 allows one adjustment after the first prototype review, through §18.5; a page may not move its own dial.

## 3. Typography

Decisions (full spec in [typography.md](typography.md)):

- One family, **Be Vietnam Pro**, built for Vietnamese diacritics; self-hosted; weights 400 and 600 only.
- System monospace only for machine identifiers (VIN, appointment and trace ids); never for prose or headings.
- Body `--text-md` (16px); Customer body `--text-lg` (18px); nothing below `--text-sm` (14px). Running text line height 1.6.
- No uppercase, no positive letter-spacing, display line height at least 1.15 so stacked diacritics never collide.
- Hierarchy comes from weight and space before size. Display sizes exist only on Landing.

## 4. Color semantics

Decisions (full spec and contrast record in [color.md](color.md)):

- **Mineral neutrals**: cool grey with a faint green undertone. This deliberately avoids both the warm-cream default and blue-slate SaaS.
- **Ink is the human color**: primary actions, selection, focus, human-owned states. The one accent (taste-rules rule 5) is ink.
- **Teal is the machine**: AI and system work only. Never a button, link, focus ring or decoration.
- **Amber means a person must decide**: waiting for the customer or for staff, and warnings.
- **Green means confirmed by a system of record**: a verified outcome, a server receipt, a validator pass. Never a prediction or eligibility.
- **Red means failure or safety.**
- **Color marks the present.** Completed history in a trace is neutral; only the current state and exceptions carry hue.
- No gradients, glows, neon or pure black, anywhere.

## 5. Spacing

Decisions (full spec in [spacing.md](spacing.md)): 4px base with Tailwind-compatible names; three density modes from one scale
(airy for Landing, comfortable as the default, compact for CSKH); targets at least `--target-min` (44px) with `--target-gap` (8px) on every surface.
Density changes the space between things, never the size of targets or text below the floors.

## 6. Radius

| Token | Used for |
|---|---|
| `--radius-sm` | Chips, tags, square trace nodes, inline code |
| `--radius-md` | Buttons, inputs, selects, segmented controls |
| `--radius-lg` | Cards, panes, dialogs, sheets, toasts. Nothing larger exists |
| `--radius-full` | Only things that are circular by meaning: avatars, radio, switch track, circle nodes |

No pill-shaped buttons or chips; no container radius above `--radius-lg`; nested elements never get a larger radius than their parent.

## 7. Border and shadow philosophy

- **Hairlines before boxes.** Structure comes from `--border` dividers, alignment and space. A container earns a box only when it is
  a distinct object the person acts on (a proactive message, an option, a dialog).
- **Two surface steps, not shadows, for hierarchy on the page**: `--bg` and `--surface`; `--sunken` for wells.
- **Shadows only for things that float** above content (menus, popovers, toasts, sticky action bars, dialogs, sheets): `--shadow-1`
  and `--shadow-2`, single layer, ink-tinted. In dark theme, floating layers use `--surface` plus `--border` instead.
- Control borders use `--border-strong` (at least 3:1). Decorative borders use `--border` and carry no meaning.
- No glow, colored shadow, inner shadow, blur or glass on any surface.

## 8. Iconography

- One set: `lucide-react` (taste-rules rule 5). Stroke scales with size: 2 at `--icon-sm`, 1.75 at `--icon-md`, 1.5 at `--icon-lg`.
- An icon on an action is always paired with a visible text label. Icon-only buttons exist only in CSKH dense toolbars and carry a
  Vietnamese `aria-label` plus a tooltip.
- Icons are `aria-hidden` when text says the same thing.
- State icons are fixed by §12 and may not be substituted.
- Banned as AI markers: sparkles, magic wand, robot head, brain, glowing orb. AI is identified by the words "Trợ lý AI" and the teal circle node.
- Trace node shapes (circle, diamond, square, triangle) are CSS geometry, not icons, and are defined in [components.md](components.md).

## 9. Component language

Full inventory in [components.md](components.md). The grammar every component follows:

- **Built from the same primitives everywhere.** The CareCard a customer sees, the figure on the Landing page and the case in the
  CSKH console render the same components with different density settings. There are no Landing-only fake versions.
- **The node grammar.** Shape says who holds the ball: circle = AI or system, diamond = waiting for a person's decision,
  square = a named human owns it, filled circle with check = verified, triangle = failure or safety event.
- **Fixed reading order for anything AI produced**: what happened, why you are seeing it, what was checked, what is proposed,
  what is needed from you, and then the outcome.
- **One primary action per step**, in `--accent`; everything else is secondary (outlined) or a link.
- **Every component has its loading, empty and error forms** designed, not improvised (taste-rules rule 6).
- **Illustration policy.** No stock photography, no generated images of people or vehicles, no decorative SVG. Landing illustrations
  are real product components rendered inert with fixture data and labelled "Dữ liệu mẫu", plus diagrams drawn in the node grammar.

## 10. Interaction patterns

| Pattern | Rule |
|---|---|
| Summary first | Lead with one sentence; details sit behind a disclosure that states what it holds ("Em đã kiểm tra 4 nguồn"). CSKH inverts this (K-10) |
| Confirm with parameters | Level-2 actions show every parameter as a label/value list right above one specific primary button (taste-rules rule 8). Any change to a parameter requires confirming again |
| Honest progress | On confirm, the button locks and says what is happening ("Đang đặt lịch…"). Success appears only after the server confirms; failure says what is true now and offers "Thử lại" |
| No dead ends | "Gặp nhân viên" is present on every screen and every proactive message, in the same place each time (WCAG 3.2.6) |
| Never ask twice | Anything the system already knows is prefilled or shown, not asked again (WCAG 3.3.7) |
| Explain on demand | Every recommendation, option and proactive message answers "Vì sao?" from the decision log, not from generated prose |
| Live updates without disruption | Server-sent updates never move focus, never scroll the page, never reorder a list under the pointer. New items wait behind a "3 ca mới" control |
| Deadlines, not countdowns | Customers see absolute deadlines ("trước 18:00 hôm nay"), never ticking countdowns. Expired confirmations explain and offer "Tạo lại phương án" |
| Reversal | Reversible actions are reversed through explicit actions ("Đổi lịch", "Huỷ lịch"), not undo toasts |
| Opt-out | "Vì sao anh/chị nhận tin này" links to the setting for turning off AI-written proactive messages (safety alerts excepted) |
| Keyboard | Everything reachable and operable by keyboard; dialogs trap and return focus; single-key shortcuts exist only in CSKH (K-07) |

## 11. Status semantics

General statuses, outside the nine case states. Every status is text plus icon, never color alone (taste-rules rule 11).

| Meaning | Family | Icon | Examples |
|---|---|---|---|
| Neutral fact | `--fg` / `--muted` | `info` | Warranty precheck results, "Dữ liệu mẫu", an excluded option and its reason |
| AI or system acting | `--ai` | per §12 | AI states, "Đang kết nối…" in CSKH tools |
| A person must decide, or a warning | `--attn` | `triangle-alert` or per §12 | Waiting states, "Sắp đến hạn gọi lại", "Đang kết nối lại…" |
| Confirmed by a system of record | `--ok` | `circle-check` | Verified outcome, "Đã đặt lịch" receipt from the server, validator "Đạt" |
| Failure, risk, overdue | `--danger` | `circle-alert` | Tool failure, validator "Không đạt", "Quá hạn 3 phút", lost connection |
| Safety | `--danger`, banner | `siren` | Safety path. Overrides every other status on the screen |
| Human-owned | `--human` | per §12 | ESCALATED |

Fixed mappings that are easy to get wrong:

| Data | Shown as | Why |
|---|---|---|
| Warranty `ELIGIBLE_PRELIM` | Neutral "Đủ điều kiện sơ bộ", plus the reason | Never green: the workshop concludes, not the AI |
| Warranty `NEEDS_WORKSHOP` / `EXPIRED` / `UNKNOWN` | Neutral "Cần xưởng xác nhận" / "Hết hạn theo chính sách" / "Chưa đủ dữ liệu" | Facts, not verdicts; never red |
| Validator pass / fail / not run | `--ok` "Đạt" / `--danger` "Không đạt: <rule>" / neutral "Chưa kiểm" | |
| Callback deadline | Neutral, then `--attn` within 5 minutes, then `--danger` when overdue | CSKH only (K-09) |
| Sentiment `calm` / `worried` / `annoyed` / `angry` | Neutral / neutral / `--attn` / `--danger`, always with the word | Prioritization aid, never the only signal |
| Connection | Nothing when connected; `--attn` banner when reconnecting; `--danger` banner when offline | 21-fe: connection state is visible |
| Option excluded (UC3) | Muted, not selectable, reason in words ("Loại: pin không đủ đi tới xưởng này") | Exclusion is information, not an error |

## 12. AI-state semantics

The shared vocabulary for the lifecycle of one case. Every surface uses these nine states, these words, shapes and icons. Surfaces
differ only in which states they show live and how dense the presentation is.

**Two axes, never mixed.** The *journey step* answers "where is my job?" (for a service journey: Đặt lịch, Giữ linh kiện, Chờ hẹn,
Chẩn đoán, Sửa, Xác minh; shown by the JourneyStepper). The *AI state* answers "who is acting and what do they need?" (shown by the
StateChip and the CareTrace). Example: after the parts for a booked appointment are reallocated, the job still sits at "Chờ hẹn"
while the case moves to WAITING FOR CUSTOMER, because the replan needs a new confirmation.

### 12.1 Overview

| State | Vietnamese label (customer / CSKH) | Pipeline stages | Ball with | Family | Node | Icon |
|---|---|---|---|---|---|---|
| DETECTED | Đã phát hiện / Phát hiện | Signal, Deterministic Detection, Candidate Friction, Arbitration passed | System | `--ai` | circle | `activity` |
| INVESTIGATING | Đang kiểm tra / Đang điều tra | Context, Selective Agent Reasoning | AI | `--ai` | circle | `file-search` |
| RECOMMENDING | Đề xuất / Đề xuất | Intervention, pre-send Validation | AI | `--ai` | circle | `route` |
| WAITING FOR CUSTOMER | Chờ anh/chị xác nhận / Chờ khách xác nhận | Validation gate, level 2 | Customer | `--attn` | diamond | `user-round` |
| WAITING FOR HUMAN | Chờ nhân viên duyệt / Cần duyệt | Validation gate, level 3 | Staff | `--attn` | diamond | `stamp` |
| EXECUTING | Đang thực hiện / Đang thực hiện | Execution | System | `--ai` | circle | `play` |
| VERIFYING | Đang theo dõi / Đang xác minh | Verification | System | `--ai` | circle | `gauge` |
| RESOLVED | Đã xử lý xong / Đã xác minh | Resolution | Done | `--ok` | filled circle + check | `circle-check` |
| ESCALATED | Nhân viên đang xử lý / Đã chuyển người | Handoff | Named staff | `--human` | square | `headset` |

Icon names are lucide concepts; confirm each against the pinned `lucide-react` version and keep the concept if a name changed.

### 12.2 Each state

**DETECTED.** The system turned signals into a candidate friction for this customer and arbitration allowed contact. Deterministic
(L0), no model involved, nobody contacted yet.
- Visual: teal circle node; CSKH chip "Phát hiện".
- Motion: Customer and Landing figures: enters once (fade, `--rise-sm`, `--dur-base`, `--ease-out`). CSKH: appears instantly, with the change mark if it arrives while on screen (K-03). No loop.
- Accessible alternative: the chip text and the trace item text ("Phát hiện: …"); in the CSKH queue, one polite announcement for the batch ("2 ca mới").
- Visibility: CSKH live. Customer: history only, inside "Em đã kiểm tra gì?". Landing: story chapter 1.
- Copy: CSKH "Phát hiện: BATT-COOL-01 (WARNING) lặp lại 3 lần trong 14 ngày. Chưa có lịch hoặc ticket." Customer (history): "Xe gửi cảnh báo hệ thống làm mát pin 3 lần trong 14 ngày."

**INVESTIGATING.** Context is being gathered with read-only tools, and reasoning runs only if needed (L0 rule, L1 triage or L2 agent).
- Visual: teal circle node with its ring; evidence rows fill in below as each check finishes.
- Motion: Customer: each finished check row enters (fade, `--dur-fast`). CSKH: rows appear instantly with the change mark (K-03). No spinner, no pulse, no typing dots. If no step arrives for 2 seconds, show elapsed time in text.
- Accessible alternative: progress as text ("Đã kiểm tra 3 trên 5 nguồn"); announced politely on completion, not per row.
- Visibility: CSKH live with layer tags. Customer live only in a conversation the customer started; for proactive cases, history only. Landing: chapter 2.
- Copy: Customer "Em đang kiểm tra lịch sử bảo dưỡng và phiên bản phần mềm của xe…" CSKH "Đang điều tra (L2): đã đọc 3 trên 5 nguồn."

**RECOMMENDING.** An intervention was selected and passed pre-send validation (claim check, forbidden phrases, rules, arbitration
re-check). For a proactive case this is the first moment the customer sees.
- Visual: teal circle node; the recommendation block and its options.
- Motion: Customer: the block enters (fade, `--rise-md`, `--dur-base`) and options follow with `--stagger`. CSKH: instant, with the change mark if it arrives while on screen.
- Accessible alternative: recommendation heading in the reading order; each option a labelled radio with its reason in text.
- Visibility: all surfaces.
- Copy: Customer "Em đề xuất kiểm tra hệ thống làm mát pin tại xưởng. Có 2 lịch phù hợp, linh kiện có sẵn tại cả hai xưởng." CSKH "Đề xuất (L2): xưởng Gia Lâm, 09:00 thứ Bảy 03/10. Lý do: còn linh kiện, có khoang pin cao áp, pin đủ đi tới."

**WAITING FOR CUSTOMER.** A level-2 action (affects the customer, reversible) needs the customer to confirm the exact parameters. The ball is with the customer.
- Visual: amber diamond node; heading "Đến lượt anh/chị"; the DecisionBlock.
- Motion: none. Waiting is never animated; reminders follow the message frequency rules, not motion.
- Accessible alternative: the heading, the parameter list (`dl`) and the deadline in text; one polite announcement when the state begins.
- Visibility: Customer live (primary). CSKH live as "Chờ khách xác nhận" with time sent. Landing: chapter 3.
- Copy: Customer "Đến lượt anh/chị. Lịch được giữ đến 18:00 hôm nay." Primary button "Xác nhận đặt lịch". CSKH "Chờ khách xác nhận (mức 2). Đã gửi 14:02."

**WAITING FOR HUMAN.** A level-3 action (money, safety, identity, policy exception) needs a staff decision. The AI only prepared the file.
- Visual: amber diamond node; CSKH DecisionBar with "Duyệt", "Sửa rồi duyệt", "Từ chối" (reason required).
- Motion: none.
- Accessible alternative: the reason for approval in text ("Mức 3: bù đắp chi phí"); the deadline in text.
- Visibility: CSKH live (primary). Customer live as an expectation, not a task.
- Copy: Customer "Phương án này cần nhân viên duyệt. Bên em sẽ báo lại trước 16:00." CSKH "Cần duyệt. Mức 3: ngoại lệ chính sách. Hạn 16:00."

**EXECUTING.** An authorized action is being carried out by the Executor (validator re-check, idempotent tool call).
- Visual: teal circle node; the locked primary button with a loader icon and a specific label.
- Motion: the loader icon in the locked button rotates (`--ease-linear`, one turn per second). This is the **only looping animation allowed** on Customer and CSKH; under reduced motion it is a static icon.
- Accessible alternative: the button label changes ("Đang đặt lịch…") and `aria-busy` is set on the region; the result is announced once.
- Visibility: all surfaces. Never followed by success copy until the server confirms (21-fe).
- Copy: Customer "Đang đặt lịch…"; failure "Chưa đặt được lịch vì hệ thống xưởng chưa phản hồi. Em đang kiểm tra lại, anh/chị chưa cần làm gì." CSKH "Đang thực hiện: đặt lịch, lần thử 1 trên 3."

**VERIFYING.** The action is done and the system is watching for the real outcome. Not counted as success yet. Two phases:
*guard*, from booking until the visit (the appointment stays feasible: reservation held, slot kept; flow loop 5, AppointmentGuard),
and *window*, after the fix (7, 14 or 30 days by fault type; the next charging session for UC2).
- Visual: teal circle node; the VerificationMeter, a determinate count of days or sessions in text plus segments (window phase); the guard phase shows the conditions being watched as a short checklist.
- Motion: none while waiting (the window lasts days). A segment change: Customer `--dur-base`; CSKH `--dur-fast` (K-03).
- Accessible alternative: the sentence carries the meaning ("Đã theo dõi 3 trên 7 ngày, xe chưa báo lại lỗi."); the meter is `aria-hidden`.
- Visibility: all surfaces.
- Copy: Customer, guard "Bên em đang theo dõi để lịch hẹn và linh kiện luôn sẵn sàng đến ngày hẹn."; window "Đang theo dõi kết quả: 3 trên 7 ngày, xe chưa báo lại lỗi." CSKH "Xác minh: cửa sổ 7 ngày (lỗi liên tục), ngày 3, 0 lần tái phát."

**RESOLVED.** Verification passed: the outcome is confirmed by system evidence, not by closing a ticket or a customer tapping "hài lòng".
- Visual: green filled circle with check; the trace line ends.
- Motion: Customer only, once, and only when witnessed: the node settles (from `--enter-scale` with fade, `--dur-base`). CSKH: no settle; the chip crossfades over `--dur-fast` (K-03). No confetti, ever.
- Accessible alternative: the sentence with the evidence ("không báo lại lỗi trong 7 ngày theo dõi"); announced once.
- Visibility: all surfaces.
- Copy: Customer "Đã xử lý xong. Xe không báo lại lỗi trong 7 ngày theo dõi." CSKH "Đã xác minh: 0 lần tái phát trong 7 ngày. Đóng 10/10, 09:00."

**ESCALATED.** A named person owns the case: the customer asked, the AI was unsure or failed twice, a policy exception, rising negative
sentiment, a level-3 matter needing full human handling, a complaint, or safety. The AI stops acting on its own and may assist the staff member.
- Visual: square node and inverse chip in `--human` / `--on-human`, with the person's name and role.
- Motion: crossfade into place (`--dur-fast`). Never an alarm.
- Accessible alternative: the person's name, role and promised time in text.
- Visibility: all surfaces.
- Copy: Customer "Anh Hải, cố vấn dịch vụ xưởng Long Biên, đang trực tiếp xử lý và sẽ gọi anh/chị trước 14:21." CSKH "Đã chuyển người. Gọi lại trước 14:21."
- **Safety variant.** For a CRITICAL fault or a dangerous description, the case goes straight to ESCALATED with the safety flag: a
  `--danger` banner carrying the pre-approved template, a "Gọi cứu hộ 24/7" action, no AI recommendation and no AI diagnosis. CSKH
  shows the case at the top of every queue view.

### 12.3 Transitions

| From | To | When |
|---|---|---|
| DETECTED | INVESTIGATING, or RECOMMENDING directly | Deterministic path is enough (decision gate) |
| INVESTIGATING | RECOMMENDING, ESCALATED | Evidence gathered / AI unsure or failed twice |
| RECOMMENDING | WAITING FOR CUSTOMER, WAITING FOR HUMAN, EXECUTING | Level 2 / level 3 / level 0 to 1 needs no confirmation |
| WAITING FOR CUSTOMER | EXECUTING, RECOMMENDING, ESCALATED | Confirmed / a parameter changed or "Chọn phương án khác" / "Gặp nhân viên" |
| WAITING FOR HUMAN | EXECUTING, RECOMMENDING, ESCALATED | Approved / approved with changes (customer confirms again) / rejected, human takes over |
| EXECUTING | VERIFYING, ESCALATED | Server confirmed / failed after limited retries |
| VERIFYING | RESOLVED, DETECTED (new linked case), ESCALATED | Window passed clean / recurrence (UC6, at most 2 automatic cycles) / unclear |
| ESCALATED | EXECUTING, VERIFYING | Staff finalized; the AI takes the journey back (flow D, step 7) |

**Events are not states.** The trace can also show events between states: a failure (triangle node, `--danger`), a parameter change
needing re-confirmation (amber), a reminder sent (neutral), a suppressed candidate (CSKH only, neutral, with the arbitration reason).
A case that ends without action (declined, expired) has no state in this vocabulary yet; see the governance doc, open decision D-03.

### 12.4 Completed steps in the customer timeline

The Customer labels in §12.1 name the present. In the customer timeline ("Tiến trình xử lý"), a completed step is named by what it
achieved, in the past tense, so the history reads as a sequence of finished things. The current step keeps its §12.1 label; CSKH
keeps its own labels in history. Each completed step also names its actor, time and cause ([customer-journey.md](../../docs/frontend/customer-journey.md) §3).

| State | Completed form | Forms that name the outcome |
|---|---|---|
| DETECTED | Đã phát hiện | Names what was detected: "Phát hiện cảnh báo lặp lại" |
| INVESTIGATING | Đã kiểm tra | "Trợ lý AI đã kiểm tra 4 nguồn" |
| RECOMMENDING | Đã đề xuất | "Đã đề xuất kiểm tra tại xưởng", "Đã đề xuất lịch mới" |
| WAITING FOR CUSTOMER | Anh/chị đã xác nhận | "Anh/chị chọn phương án khác", "Anh/chị chọn gặp nhân viên", "Hết hạn giữ chỗ" |
| WAITING FOR HUMAN | Nhân viên đã duyệt | "Nhân viên đã duyệt có thay đổi", "Nhân viên không duyệt" with the reason |
| EXECUTING | Đã thực hiện | Names the action: "Đã đặt lịch", "Đã đổi lịch", "Đã cập nhật phần mềm" |
| VERIFYING | Đã theo dõi xong | "Đã theo dõi đủ 7 ngày" |
| RESOLVED | Đã xử lý xong | The final item; nothing follows it |
| ESCALATED | Nhân viên đã xử lý | Names the person and the outcome: "Anh Hải đã chốt lịch mới" |

## 13. Responsive principles

- Test at 320, 390, 768, 1024, 1280 and 1440px, both themes, and at 200% zoom. No horizontal page scroll at 320px.
- Customer is mobile-first. Landing is fluid; asymmetric compositions collapse to a single column below 768px. CSKH is designed
  desktop-first for 1280px and wider (K-08), yet still reflows to one column with back navigation.
- **Components respond to their container, not the viewport.** The same CareCard works in a phone, in the Demo stage's phone frame
  and as a Landing figure.
- Full-height screens use dynamic viewport units; sticky bars respect safe-area insets and never cover the focused element (WCAG 2.4.11).
- Only CSKH data tables may scroll horizontally, inside their own container with a sticky first column.

## 14. Content and copy principles

Decisions (full spec in [content.md](content.md)): "anh/chị, bên em" voice; the AI introduces itself and refers to itself as "em";
the labels "Trợ lý AI", "Tin tự động", "Gặp nhân viên" and "Vì sao anh/chị nhận tin này" are mandatory where they apply (legal and
governance requirements); every proactive message has its five parts; "đủ điều kiện sơ bộ", never "được bảo hành"; no invented numbers;
sample data says "Dữ liệu mẫu"; no em or en dashes in interface text.

## 15. Motion principles

Full specification in [motion.md](motion.md); every movement per surface in the
[landing](../../docs/frontend/landing-motion-map.md), [customer](../../docs/frontend/customer-motion-map.md) and
[CSKH](../../docs/frontend/cskh-motion-map.md) motion maps. Binding rules (design review §G):

1. **Motion explains a change**: feedback, state change, spatial continuity, and on Landing the explanation of a sequence. Nothing decorates.
2. **Witnessed change only.** Nothing moves on load; a change that happened while the person was away is shown finished and marked in words.
3. **Frequency decides.** Frequent actions do not animate; keyboard-initiated actions get no feedback motion; overlays opened from the keyboard appear by opacity only.
4. **Confirmation never animates.** The parameters of a level-2 action change instantly; success appears only after the server confirms.
5. **Short and decisive.** At most `--dur-slow`; `--ease-out` to enter, `--ease-in-out` to move; exits faster than enters; never ease-in, bounce or elastic; never from scale 0.
6. **Transform and opacity only**, plus hover or selection color over `--dur-fast`; never `transition: all`.
7. **Interruptible.** Transitions for anything that can repeat; keyframes only for one-shot entrances.
8. **One loop**: the EXECUTING loader inside the locked button, static under reduced motion.
9. **Per surface.** Landing: scroll-scrubbed choreography in three sequences, full tier only, static first (L-02). Customer: one beat of at most `--dur-base` per update; the focal element rises; one settle on a witnessed RESOLVED. CSKH: the employee's own actions never move; server-driven changes get one opacity cue; no settle (K-03).
10. **No cascades.** One update, one beat; at most six staggered items; more than six changed elements on CSKH get static marks.
11. **Nothing under the pointer moves.** Lists never reorder in place; alerts never shift panes; a server-driven change to CSKH decision buttons ignores clicks for `--dur-slow`.
12. **Urgency is never motion.** Safety, errors and overdue deadlines appear at once, in words; no pulse, shake or flash.
13. **Reduced motion is a full design.** Every movement becomes instant or a plain opacity change; every loop stops; Landing shows final states; CSKH cues become the static "Vừa đổi" mark.
14. **No libraries, no scroll listeners** (taste-rules rule 10): CSS transitions and keyframes, the Web Animations API, IntersectionObserver and scroll-driven animations only.
15. **Every movement is listed** in motion.md §2 and the surface's motion map; anything not listed does not move.

## 16. Accessibility principles

Full specification in [accessibility.md](accessibility.md), including the web interface rules of §9. Binding rules (design review §H):

1. **Floor**: WCAG 2.2 AA plus the team floors, audited with the pinned web-design-guidelines rules and web-accessibility.
2. **Language and structure**: `lang="vi"`; skip link first; landmarks; one `h1` per page, including combined panes; headings in order.
3. **Semantics before ARIA**: buttons for actions, links for navigation; real tables in CSKH, `dl` on Customer, lists for queues and timelines.
4. **Contrast**: AA in both themes, 4.5:1 for text including muted, placeholder and disabled text, 3:1 for controls, focus and nodes; no outlined control on a state tint.
5. **State** never by color alone: shape, icon and word together; deadlines and verdicts in words.
6. **Focus**: a visible ring on `:focus-visible` (`:focus-within` for compound controls), never covered by sticky chrome; anchored headings carry `scroll-margin-top`; dialogs trap and return focus; live updates never move focus.
7. **Keyboard**: every journey works without a pointer; single-key shortcuts only in CSKH regions, never in text fields, with a switch; no single key for consequential decisions.
8. **Targets** at least `--target-min` with `--target-gap` on every surface; the Customer primary action `--control-h-lg`.
9. **Text** at least `--text-sm`, `--text-md` on Customer and in every input; zoom never disabled; 200% zoom and 320px reflow without loss.
10. **Announcements**: one polite live region per screen; atomic, short and in words; batched on CSKH; streamed text announced once complete; safety as `role="alert"`.
11. **Forms**: visible labels, never placeholder as label; correct type, inputmode and autocomplete; paste allowed; spellcheck off for codes; errors in words next to the field and focus to the first error; drafts kept.
12. **Time**: no time limits on customer input; customers see absolute deadlines, never countdowns; toasts stay at least 5 seconds and pause on hover or focus.
13. **Help**: "Gặp nhân viên" on every customer screen, in the same place; no dead ends.
14. **Theming**: both themes complete; `color-scheme` and `theme-color` follow the theme; forced colors keep meaning through shape, icon and text.
15. **Identifiers** carry `translate="no"`.
16. **Long lists**: `content-visibility: auto` first; virtualized lists keep set size, position and keyboard movement.
17. **Touch**: no gesture-only action; `touch-action: manipulation`; `overscroll-behavior: contain` in overlays.
18. **Test protocol**: accessibility.md §7 on every screen before review.

## 17. Anti-patterns

Banned on every surface unless a page file lists a bounded deviation.

| Area | Banned |
|---|---|
| Surface | Gradients of any kind; glassmorphism and backdrop blur; neon, glow, colored or stacked shadows; pure black; the warm cream plus espresso palette; purple or blue "AI" gradients; noise and grain; containers rounder than `--radius-lg`; pill buttons; cards inside cards |
| AI clichés | Floating orbs, particles, waveforms as decoration; sparkles, wand, robot or brain icons; "thinking" dots or fake delays; an avatar or human persona for the AI; unexplained confidence percentages (show the basis instead: "7 trên 9 ca tương tự") |
| Layout | Dashboard-as-landing (metric grids, charts on the Landing page); centered hero; three equal feature cards; bento grids; zigzag image/text more than twice; eyebrow labels over every section; split headers with filler text; decorative status dots; scroll cues |
| Motion | Animation on load; parallax; scroll hijacking; looping decoration; animated gradients; bounce or elastic easing; scale from 0; `transition: all`; motion on keyboard actions; anything without a reduced-motion path |
| Content | Em or en dashes in interface text; invented numbers, dates or prices; testimonials and logo walls; "được bảo hành"; diagnosis; internal system terms shown to customers; filler words ("đột phá", "liền mạch", "thông minh vượt trội"); "Oops"; bare error codes; generic names |
| Interaction | Success shown before the server confirms; a hidden or moving "Gặp nhân viên"; countdowns, urgency badges or "HOT" on offers (taste-rules rule 9); auto-advancing carousels; toasts as the only record of something important; placeholder as label; disabled controls without a reason |
| Trust | AI presented as a person; removing the "Trợ lý AI" or "Tin tự động" label; showing a recommendation without its reason; div-built fake product screens; model reasoning text or the `analysis` field shown anywhere |
| Story | An appointment as the opening image or the start of the story; "rescue" framing; "done" before verification; a booking presented as the outcome; cards around things that ask nothing of the person |

## 18. The design contract

v1.0. The design review of 2026-10-03 ([design-review.md](../../docs/frontend/design-review.md)) is the record behind this section.

### 18.1 Frozen decisions

These change only through §18.5.

| # | Decision | Where |
|---|---|---|
| F-01 | Proactive care made visible and accountable; "calm instrument, human hand"; the Care Trace as the one signature element | §0, §2 |
| F-02 | The story: signal, detection, investigation, intervention, verification; an appointment is one intervention, never the start | §0 |
| F-03 | Precedence: product requirements, internal design system, taste-skill, ui-ux-pro-max, emil-design-eng, web-design-guidelines | design-governance.md §2 |
| F-04 | Dials: Landing 7/8/3, Customer 5/5/4, CSKH 3/2/8 | §2.1 |
| F-05 | Be Vietnam Pro 400 and 600, self-hosted; mono for identifiers only; no uppercase; display line height at least 1.15; floors 14px, 16px on Customer; Customer body 18px | §3 |
| F-06 | Color roles: mineral neutrals; ink for people and action; teal only for the AI; amber when a person must decide; green for system-of-record confirmation; red for failure and safety; color marks the present | §4 |
| F-07 | The token set, the contrast record and the layout thresholds | tokens.md, color.md §6 |
| F-08 | One spacing scale, three density modes, 44px targets everywhere | §5 |
| F-09 | Radius 4, 6, 8, full; no pills; nothing larger than `--radius-lg` | §6 |
| F-10 | Hairlines before boxes; cards only for objects that ask for action; shadows only for floating layers | §7 |
| F-11 | lucide icons; fixed state icons; banned AI icons; a label on every action icon outside CSKH toolbars | §8 |
| F-12 | The node grammar | §9 |
| F-13 | The nine states with both label sets, shapes, icons, families, transitions and completed forms; two axes; authorization verdicts as a separate vocabulary | §12 |
| F-14 | Mandatory labels and the voice "anh/chị, bên em" | §14 |
| F-15 | Interaction patterns | §10 |
| F-16 | The proactive care card: the four-question head with a "Việc của anh/chị" line that is never empty, then the brief's order | customer-screen-spec.md §3 |
| F-17 | The case file: the nine questions plus the audit, on a spine, in fixed order | cskh-screen-spec.md K4 |
| F-18 | The CSKH priority model; nothing reorders under the pointer | cskh-information-architecture.md §6 |
| F-19 | The motion rules (§15) and the accessibility rules (§16) | §15, §16 |
| F-20 | The architectures: Landing S01 to S10, Customer C1 to C8, CSKH K1 to K7 (product confirmation pending) | screen-map.md |
| F-21 | Illustration policy: real components with fixture data labelled "Dữ liệu mẫu"; no stock, no generated images | §9 |

### 18.2 Shared components

One implementation each, reading density from its container; a surface-specific copy is a defect (components.md §1). Shared across
surfaces: TraceNode, CareTrace, StateChip, JourneyStepper, VerificationMeter, LayerTag, AIByline, StaffByline, EvidenceList,
SourceRef, InvestigationSteps, ValidationList, OptionCard and OptionList, DecisionBlock, ConfirmationReceipt, PromiseLine, CareCard,
JobCard, CaseFile, HandoffCard, QueueRow, and every foundation in components.md §10. Where each appears: design-review.md §E.

### 18.3 Surface exceptions

27 deviations, and only these: Landing L-01 to L-09 (L-01 and L-02 blocked until A-01 and A-02), Customer C-01 to C-06, CSKH K-01
to K-12. The page files in [pages/](pages/) are the only place an exception may exist; none touches an invariant
(design-governance.md §7).

### 18.4 What every implementation must do

1. Use only the tokens in `tokens.md`, Be Vietnam Pro (400 and 600, self-hosted) and lucide icons; no other UI dependency without an ADR.
2. Present case progress with the nine states of §12, with the label set of the surface, the node shape, icon and color family, never color alone; keep the journey step and the AI state apart; show what policy allows as authorization verdicts, never as states.
3. Use ink for action and people, teal only for the AI, amber only for waiting on a person, green only for what a system of record confirmed, red only for failure and safety.
4. Label AI content "Trợ lý AI" and proactive messages "Tin tự động"; give every proactive message its parts including "Vì sao anh/chị nhận tin này"; keep "Gặp nhân viên" on every customer screen in the same place.
5. Show evidence and its source behind every AI recommendation; never invent numbers, dates, prices, policy, warranty outcomes or diagnoses; never show model reasoning text or the `analysis` field.
6. Confirm level-2 actions with every parameter visible and one specific primary button; never animate those parameters; never show success before the server confirms.
7. Tell the story signal first (F-02): no appointment as the starting point or the opening image.
8. Design loading, empty and error forms for every view.
9. Use the shared components of §18.2.
10. Move only as §15 and the surface's motion map allow.
11. Meet §16 and accessibility.md in both themes.
12. Take surface-specific liberties only from that surface's page file.
13. Render Landing illustrations as real components with fixture data labelled "Dữ liệu mẫu".
14. Pass the conformance checks in design-governance.md §6 and attach the evidence to the pull request.

### 18.5 Changing the contract

| Change | Needs | Version |
|---|---|---|
| A frozen decision (§18.1) | A design pull request with the reason, agreed by the frontend owner and the product owner; the design review re-run for the affected checks | 2.0 |
| A new token, component, state detail or rule that changes no frozen decision | The change process in design-governance.md §4 | 1.x |
| A new or changed deviation | design-governance.md §7 | 1.x |
| A contract gap closed (a field added to `api.yaml`) | Remove the gap marker in the components and screens it affects | 1.x |
| Copy within content.md's rules, sample data | A normal pull request | none |

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0.1 | 2026-10-03 | Editorial, no rule changed: version labels in the detail files and status lines in the surface specifications updated from draft and v0.x to v1.0, before the first export to P-073 `docs/design/` |
| 1.0 | 2026-10-03 | Design contract after the design review (design-review.md): 28 changes applied (product story in §0 and journeys, Landing door previews, the CSKH origin chain, card use on Customer Home, contrast record and the state-tint rule, layout thresholds, surface-explicit motion in §12, keyboard and confirmation motion rules, CSKH update control and cue cap, web interface rules in accessibility.md §9, the policy example); §15 and §16 rewritten as binding rules; §17 adds the story row; new §18 with frozen decisions, shared components, exceptions, implementation duties and change control. Frontend owner signature pending |
| 0.4 | 2026-10-03 | CSKH console specified from the fourth owner brief: six screens K1 to K7 (screen-map §5, D-15); the action model separating lifecycle states from authorization verdicts; `pages/cskh.md` K-02, K-04, K-06, K-10 bounds revised, K-03 rewritten (own actions never animate; server-driven changes get one opacity cue), K-11 (header alert slot) and K-12 (theme switch in the account menu) added; components.md: ReasoningSteps renamed InvestigationSteps, CaseFile rebuilt on the nine questions and the spine, QueueRow, DecisionBar and AppHeader revised, new ActionPolicyTable, FrictionTable, PresenceTag, CopilotSuggestion, AlertSlot; motion.md: CSKH column and the row change mark; spacing.md: case pane minimum 520px at 1280px (560px did not fit beside the queue and decision panes); accessibility.md: CSKH keyboard map and patterns; new docs `cskh-information-architecture.md`, `cskh-screen-spec.md`, `cskh-motion-map.md` |
| 0.3 | 2026-10-03 | Customer experience specified from the third owner brief: home-first information architecture with screens C1 to C8 (screen-map §4, D-13); `pages/customer.md` C-02 and C-03 bounds revised, C-05 (conversation stays at the newest message) and C-06 (theme switch in settings on phones) added; §12.4 completed-step wording for the customer timeline; components.md: CareCard rewritten around the four-question head, CareTrace "Horizontal, condensed" variant and customer timeline rules, new BottomNav, NotificationRow, ActionScope, MemoryList, Sheet and AppHeader notes; motion.md: principle 6 extended to witnessed change only, catalogue rows for switch, in-app notice, sticky action bar and state chip change; content.md: the four questions; accessibility.md: count and update-control announcements, BottomNav and NotificationRow patterns; new docs `customer-journey.md`, `customer-screen-spec.md`, `customer-motion-map.md` |
| 0.2 | 2026-10-03 | Landing story specified from the second owner brief (ten sections): `pages/landing.md` L-01, L-02, L-05, L-06 revised, L-08 (counterfactuals) and L-09 (holder-colored diagrams) added; components.md §8 Landing composites replaced (CounterfactualMark, ShiftTimeline, EngineSequence, StoryChapter, ContrastPair, LayerSieve, TrustGate, SurfaceDoor, ChapterLabel; ComparisonTimeline, PipelineDiagram and UseCaseIndex removed); motion.md §4 limited to three sequences; new docs `landing-story.md` and `landing-motion-map.md` |
| 0.1 | 2026-10-03 | First draft. Built from the owner brief of 2026-10-03, specs 05/13/19/20/21, proposal 06/07/08/09, `taste-rules.md`, and the four design skills in their roles (log in design-governance.md §5) |
