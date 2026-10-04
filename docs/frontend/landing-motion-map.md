# Landing motion map

Every movement on the landing page, why it exists, and what replaces it when motion is off. Sections and copy are in
[landing-story.md](landing-story.md). Rules: [motion.md](../../design-system/proactive-care/motion.md) §4 and deviation L-02 in
[pages/landing.md](../../design-system/proactive-care/pages/landing.md). Motion direction follows emil-design-eng, used selectively.
No code here; values are tokens from [tokens.md](../../design-system/proactive-care/tokens.md).

**Status.** The three sequences below are blocked until amendment A-02 is merged ([design-governance.md](design-governance.md) §9).
The static final states are not blocked and are the baseline the page is built on first.

## 1. What motion has to explain

| Meaning (owner brief) | Where it is shown | How |
|---|---|---|
| Causality | M2, stages 2 to 5; M1 | Each stage's output visibly becomes the next stage's input; three warnings merge into one candidate; the start of care moves earlier |
| State transitions | M3; M2 rail | The phone goes from quiet, to a message, to confirmed, to verified; the rail's current node changes holder |
| System progression | M2 | The case packet travels along the six-stage rail and relabels at each stage |
| Detection | M2, stage 2; M1 "Phát hiện" node | Repetition turns into one candidate |
| Reasoning | M2, stage 4 | The decision gate takes the "cần Agent" exit; options appear; one is excluded with its reason |
| Intervention | M2, stage 5; M3, beat 6 | A checked message arrives and waits for a person before anything happens |
| Resolution | M2, stage 6; M3, beat 7 | A verification window fills day by day and ends in one settle of the green node |

## 2. Budget

Three narrative sequences, all scroll-scrubbed. Everything else is still, or reacts only to the visitor's own input.

| Moment | Section | Kind | Focal element |
|---|---|---|---|
| M1, "The start moves earlier" | S02 into S03 | Scroll-scrubbed sequence | The time track |
| M2, "One signal, six steps" | S04 | Scroll-scrubbed sequence with stage navigation | The artifact panel and case packet |
| M3, "The quiet phone" | S05 | Scroll-scrubbed beats | The phone (the console changes instantly) |
| Feedback | S01, S08, S10, header | Hover and press on doors and buttons | The control under the pointer |
| Emphasis | S06, S07 | Instant highlight on hover, focus or selection | The selected row or chip |

## 3. Page rules

- **Tiers** (landing-story.md §3): sequences run only in the full tier, at least 1024px wide and 700px tall. The compact and phone
  tiers show each stage, beat and track in its final state, with no sticky figures and no scrubbing.
- **Technique**: CSS scroll-driven animations (view timelines shared from the text blocks to the sticky panel) where supported;
  otherwise an IntersectionObserver switches discrete states with `--dur-base` and `--ease-out`. No scroll listeners, no library.
- **Scrubbed means reversible**: scrolling back plays everything backwards. Nothing is triggered once and left behind.
- **Active band**: a stage or beat is active while its text block's heading sits in the middle band of the viewport (40% to 60% of
  its height). Within an active block, progress `q` runs from 0 to 1 as the block crosses the band.
- **One moving focal element at a time.** When the packet moves, the panel only crossfades.
- **Each figure moves like its own surface.** The phone follows the customer catalogue. The CSKH console changes state instantly,
  as the product does for changes its own user causes (K-03; cskh-motion-map.md rule 2). Real components keep their own rules, except that loops are off on this page: the EXECUTING loader
  in a figure is a static icon.
- **Jumps are instant.** Stage navigation and anchor links jump without smooth scrolling, so intermediate sequences never play in fast-forward.
- **Movement is transform and opacity only.** Lines "draw" by moving a cover element away (a transform), so dash patterns never stretch.
- **Nothing exceeds `--dur-slow`** in any time-based change, and nothing moves on load.

## 4. M1, "The start moves earlier" (S02 into S03)

**Purpose.** Make two ideas felt rather than read: in reactive care the customer starts everything and waits; in proactive care
the start moves earlier and the burden moves to the system.

**Trigger.** The S02 and S03 text blocks scroll past one sticky time track; progress `p` runs from 0 to 1 across both sections.

| `p` | Focal element | Change | Explains |
|---|---|---|---|
| 0.00 to 0.10 | "Khách tự nhận ra" (amber diamond) | Appears from `--enter-scale` with opacity | The customer starts it |
| 0.10 to 0.22 | Connector, then "Gọi tổng đài" | Connector drawn by moving its cover; node appears | The customer acts again |
| 0.22 to 0.40 | The "Chờ" span | The dashed span is uncovered to twice its first length; "chờ gọi lại" appears at 0.30 | Waiting felt as distance |
| 0.40 to 0.52 | "Nhân viên tìm hiểu lại" (ink square) and the "kể lại từ đầu" loop | Node appears; loop appears | Staff start from zero; the customer retells |
| 0.52 to 0.58 | "Mới bắt đầu xử lý" | Appears | Action comes last |
| 0.58 to 0.62 | Nothing | Hold while the S03 heading reaches the band | A beat of stillness before the shift |
| 0.62 to 0.72 | The start marker | Slides earlier along the axis to "Tín hiệu từ xe" (translate) | Care starts before the customer notices |
| 0.72 to 0.76 | The reactive track | Crossfades from solid to its dashed ghost layer | The old path becomes a counterfactual |
| 0.76 to 0.92 | The proactive nodes | Phát hiện, Kiểm tra, Can thiệp, Khách xác nhận, Xác minh appear in order with their connectors | The burden moves to the system |
| 0.92 to 0.97 | The "Can thiệp" inset | The four intervention types appear; "Đặt lịch xưởng" is one of them | The appointment is one intervention |
| 0.97 to 1.00 | The verified node | Settles once from `--enter-scale` | Resolution |

**Static final state.** Both tracks on one axis: the reactive track dashed and labelled "Nếu chờ khách hỏi", the proactive track
solid, the start marker at "Tín hiệu từ xe", the intervention list open, the legend under the axis.

**Accessibility.** The steps and the key line are text in S02 and S03; the track is `aria-hidden` with a caption, so nothing is lost
when motion is off.

## 5. M2, "One signal, six steps" (S04)

**Purpose.** Show the mechanism as one continuous transformation, and show exactly where a model is used.

**Trigger.** Six stage blocks scroll past the sticky panel. On becoming active, a stage changes discretely; within it, sub-steps
scrub with `q`.

| Stage | When it becomes active | Within the stage (scrubbed by `q`) | Explains |
|---|---|---|---|
| 1 Tín hiệu | Rail node 1 becomes current; the packet appears ("1 cảnh báo"); the event card fades in | None | A signal enters |
| 2 Phát hiện | The packet moves to node 2 (`--dur-slow`, `--ease-in-out`) and relabels "1 ứng viên"; node 1 turns neutral | 0 to 0.5: two earlier warnings slide in beside the first, a stack of three; 0.5 to 0.8: the stack merges into one candidate card; 0.8 to 1: the arbitration line appears | Repetition becomes a candidate, at 0 token |
| 3 Ngữ cảnh | Packet to node 3, "5 nguồn đã đọc" | Evidence rows enter one per fifth of `q` (`--rise-sm`) | Context gathered, each fact with its source |
| 4 Suy luận AI | Packet to node 4, "2 phương án" | 0 to 0.3: the decision gate with three exits; 0.3 to 0.5: the "cần Agent" exit is emphasized, the others dim; 0.5 to 1: reasoning steps, then options; the excluded option turns muted with its reason | Reasoning is selective and shows its work |
| 5 Can thiệp | Packet to node 5, "1 tin đã gửi" | 0 to 0.3: ValidationList "Đạt"; 0.3 to 0.5: the CareCard enters (`--rise-md`); 0.5 to 0.7: the amber waiting state; 0.7 to 0.85: "Đang đặt lịch…"; 0.85 to 1: the receipt "Đã đặt lịch" | A checked message, a person's confirmation, then action |
| 6 Xác minh | Packet to node 6 | 0 to 0.3: the guard checklist; 0.3 to 0.9: seven segments fill one by one; 0.9 to 1: the verified node settles once; the packet relabels "Đã xác minh" | Done only when real data says so |

**Interaction.** Stage navigation links and "Bước trước" / "Bước sau" jump instantly to a stage block. The panel then shows that stage at
`q` = 0. After a jump, focus moves to the stage heading and the stage name is announced once.

**Static final state.** Six stage blocks, each with its artifact inline in its final form (stage 2 shows the candidate card, stage 4 the
options with the excluded one, stage 6 the verified meter). No packet.

## 6. M3, "The quiet phone" (S05)

**Purpose.** Let the visitor feel the customer's side of proactive care: nothing to do, until help arrives. Meanwhile the CSKH side is
visibly busy.

**Trigger.** Seven beat blocks scroll past two sticky figures; the active beat sets both figures and the clock label.

| Beat | Phone (customer catalogue) | Console (instant) | Clock label | Explains |
|---|---|---|---|---|
| 1 | Still: "Chưa có tin mới" | Empty "AI đang xử lý" view | Trước 29/09 | Nothing has happened for the customer |
| 2 | Still | New row with the DETECTED chip | Thứ Ba 29/09, 08:15 | Detection |
| 3 | Still | Rule and arbitration lines in the trace | 08:15 | The candidate |
| 4 | Still | Evidence section filled | 08:15 | Context |
| 5 | Still | Recommendation; the "chỉ theo dõi" branch muted | 08:16 | The agent judges intervention justified |
| 6 | `q` 0: the CareCard enters (`--rise-md`, `--dur-base`, `--ease-out`); 0.5: "Đang đặt lịch…"; 0.8: the receipt | "Chờ khách xác nhận", then "Đã đặt lịch" | 08:16 | Help arrives before the question |
| 7 | 0 to 0.85: seven verification segments fill; 0.85: RESOLVED settles once | "Đã xác minh" at 0.85 | Sau khi sửa | Resolution |

The phone is the only thing that moves in M3, and only in beats 6 and 7. The stillness of beats 1 to 5 is deliberate.

**Static final state.** Each beat followed by compact snapshots of both sides in that beat's final state; on small screens beats 1 to 5 replace
the phone with the line "Điện thoại của anh Minh: chưa có tin."

## 7. Interaction feedback

| Element | Response | Tokens |
|---|---|---|
| Doors and buttons (S01, S08, S10) | Hover: border and fill color change, fine pointers only. Press: scale | `--dur-fast`; `--press-scale` over `--dur-press` |
| Stage navigation (S04) | Current link marked instantly | None |
| Evidence rows (S06) | Hover or focus emphasizes the connector and the outcome clause; others unchanged | Instant |
| Event chips (S07) | Selection emphasizes the path and reason; other chips turn `--muted` | Instant, or `--dur-fast` opacity |
| Theme switch | The whole page changes theme at once, with no color transition | None |
| Header chapter label | Text swaps as chapters change | None |

## 8. What never moves

S01 entirely, including the CareCard figure and the axis. Every heading and paragraph. S06 and S07 layouts. Both S08 figures. S09 and S10. The
header (it never hides or shrinks on scroll) and the footer. The CSKH console figure in any section. Numbers (nothing counts up). Backgrounds.

## 9. Rejected motion ideas

| Idea | Source | Why not |
|---|---|---|
| Hero entrance animation ("motion claimed, motion shown") | taste-skill §5 | Taste-rules rule 10 and motion.md: nothing moves on load. MOTION 8 is shown by the three sequences instead |
| Parallax, magnetic buttons, perpetual pulse, typewriter, shimmer | taste-skill §5, MOTION 8 to 10 | Rule 10; vestibular risk; these are the AI-landing clichés the brief bans |
| Pinned sticky-stack or horizontal pan through GSAP | taste-skill §5.A, §5.B | Scroll hijacking and a library dependency |
| Smooth scrolling for in-page links | ui-ux-pro-max (smooth scroll) | It would fast-forward the scrubbed sequences; jumps stay instant |
| Shared-element page transitions into the product | ui-ux-pro-max (GSAP Flip) | Library dependency; the doors are ordinary navigation |
| A pulsing "live" signal or continuous data streams | Common AI-landing pattern | Loops; implies live monitoring of a real vehicle |
| Numbers counting up | Common landing pattern | Implies measured data; fake precision |
| Auto-advancing the engine | Common demo pattern | Takes control from the reader; WCAG 2.2.2 |
| Confetti or a celebration on RESOLVED | Common pattern | Trivializes a fixed fault; MASTER §12: one settle only |

## 10. Test checklist

- [ ] Full tier: each sequence plays forwards and backwards with scrolling; one focal element moves at a time.
- [ ] Compact and phone tiers: no sticky figures, no scrubbing, every final state complete.
- [ ] Reduced motion: identical to the compact tier's final states; nothing moves except instant emphasis.
- [ ] No scroll-timeline support: IntersectionObserver states switch correctly in both directions.
- [ ] Stage navigation: instant jumps; focus lands on the stage heading; the stage name is announced once.
- [ ] 200% zoom on a 1280px screen falls back to the compact tier; sticky figures never cover the focused element.
- [ ] Keyboard only and a screen reader (NVDA with Chrome, VoiceOver with Safari): the story is complete without the figures.
- [ ] Performance during scroll: no long tasks, INP under 200ms, CLS under 0.1; only transform and opacity change.
- [ ] Both themes; diacritic test strings in every display statement.
