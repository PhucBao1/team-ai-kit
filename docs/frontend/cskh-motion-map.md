# CSKH motion map

Every movement in the employee console, why it exists, and what replaces it when motion is off. Screens are in
[cskh-screen-spec.md](cskh-screen-spec.md); structure in [cskh-information-architecture.md](cskh-information-architecture.md). The
catalogue and rules are [motion.md](../../design-system/proactive-care/motion.md) and deviation K-03 in
[pages/cskh.md](../../design-system/proactive-care/pages/cskh.md). Values are tokens from
[tokens.md](../../design-system/proactive-care/tokens.md). Motion direction follows emil-design-eng. No code here. Moment IDs are local to this file.

## 1. What MOTION 2 means here

**Motion is a change detector, not feedback.** The employee's own actions never animate: they repeat hundreds of times a shift, many
from the keyboard, and any delay makes the console feel slow (emil-design-eng). Changes that arrive from the server, which the
employee did not cause, get one faint cue so the eye finds them, and nothing changes position.

| How often | Moments | Decision |
|---|---|---|
| Hundreds per shift: `j`/`k`, `Enter`, section jumps, typing, hover, pressing buttons, opening cases | F, E2, E3 | No motion |
| Dozens per shift: server updates to rows and to the open case | Q, S, P2, V | One opacity cue: the change mark or a crossfade |
| Occasional: dialogs, expanding a raw payload with the pointer | E1, E4 | Dialog fade over `--dur-fast`; chevron over `--dur-fast` |
| While waiting on the Executor | P1 | The loader, the only loop |
| Completion and resolution | R | The same cue as any status change; no settle (MASTER §12) |

The brief's six uses map to groups: queue changes (Q), status changes (S), expansion (E), progress (P), verification (V), completion (R).
Feedback (F) is listed to make clear that it does not move.

## 2. Rules

1. **Opacity only.** Nothing changes position, size or order by animation; there is no rise, slide, scale or stagger in CSKH.
2. **Own actions never animate**, by pointer or keyboard: press, selection, navigation, section jumps, opening a case, applying the update control.
3. **One cue per changed element per update**, and only for changes the server made while the element was on screen. When one
   update changes more than six elements (the same cap as `--stagger`), none fades: they all get the static "Vừa đổi" mark.
4. **Nothing on load, nothing replays.** A case opened after it changed shows the change as static text ("Vừa đổi 14:06"); motion.md principle 6.
5. **The click guard.** When a server update changes the DecisionBar's actions, any click arriving within `--dur-slow` of the change is
   ignored, and the bar's status line says what changed. No consequential button can be pressed by a click aimed at the button before it.
6. **Safety and errors never move.** They appear at once, in words, with their color and icon.
7. **Two durations.** Crossfades take `--dur-fast`. The row change mark takes `--dur-slow`, the longest cue in the console, because it
   must register in peripheral vision while the employee reads another pane.
8. **Reduced motion.** Every cue becomes the static "Vừa đổi" mark; the loader is a static icon; nothing else changes (motion.md §5).

**The change mark.** A one-shot overlay in `--sunken` over the changed row or section, fading from opaque to clear over `--dur-slow`,
plus a static "Vừa đổi 14:06" in `--muted` that stays until the employee opens or focuses the element. On an already selected row
(`--sunken`) only the text appears. It never uses a state color: amber, teal or green flashes would collide with their meanings.

## 3. Moments

### 3.1 Queue changes (Q)

| ID | Moment | Where | Motion | Reduced motion | Announcement |
|---|---|---|---|---|---|
| Q1 | New or re-ranked cases arrive | K2 queue | The update control "2 ca mới, 1 thay đổi. Hiện" fades in over `--dur-fast`; rows do not move | Appears instantly | "2 ca mới", batched, at most every 30 seconds |
| Q2 | The employee applies the update control | K2 queue | The list re-renders instantly (own action); inserted and re-ranked rows carry the change mark and "Mới" | Static marks | The new count of the view |
| Q3 | A visible row's content changes (state, owner, presence, deadline threshold) | K2 queue, K3 rows, K6 tail | Change mark on the row; StateChip crossfade over `--dur-fast` if the state changed; deadline color and words change instantly | Static mark | Deadline thresholds only (accessibility.md §3) |
| Q4 | A row leaves the view (resolved, reassigned, filtered out) | K2 queue | Muted instantly with "Đã rời danh sách này"; it stays in place until Q2 or until focus moves past it | Same | None |
| Q5 | A safety case arrives | Alert slot, every view | No motion. The alert slot text appears at once; the pinned row is inserted at the top as soon as the pointer is not over the queue pane | Same | `role="alert"`, once |
| Q6 | Overview counts change | K1 | None. The number changes in place | Same | None (not watched continuously) |

### 3.2 Status changes (S)

| ID | Moment | Where | Motion | Reduced motion | Announcement |
|---|---|---|---|---|---|
| S1 | The open case changes state | K4 header, spine, index | StateChip and the "Tiếp theo" line crossfade over `--dur-fast`; the spine's current node and the index's "(hiện tại)" change instantly; the section that became current gets the change mark | Static mark | "Trạng thái: " plus the CSKH label, once |
| S2 | The DecisionBar's actions change from the server | K4 decision pane | Instant re-render, the click guard (rule 5), and the status line "Trạng thái vừa đổi: Đang thực hiện" with the change mark | Static mark; guard unchanged | Through S1 |
| S3 | Assignment or presence changes ("Lan đang xử lý ca này") | K4 header, row | Text changes instantly; the change mark on the header line | Static mark | "Lan đã nhận ca này", once |
| S4 | A new signal, evidence row or investigation step arrives while the case is open | K4 sections 2 to 4 | The row appears instantly at its place in the table with the change mark; the section's first line updates | Static mark | None, except the investigation's completion |
| S5 | ESCALATED | K4, row | As S1 (motion.md: ESCALATED change, `--dur-fast` crossfade); no alarm, no color flash | Instant | As S1 |

### 3.3 Expansion (E)

| ID | Moment | Motion | Reduced motion |
|---|---|---|---|
| E1 | A raw payload opened by pointer (K6, section 4) | Chevron rotates over `--dur-fast`; the content appears without height animation. Opened by keyboard: instant | Instant |
| E2 | Section index jump, `1` to `0` | None; no smooth scrolling | None |
| E3 | View menu, filter popover, account menu, tooltips | None (K-03) | None |
| E4 | Dialogs ("Chốt phương án", "Duyệt", "Từ chối", "Nhận xử lý", "Mở lại ca") | Opacity in and out over `--dur-fast`, no scale (motion.md, Dialog, CSKH) | Instant |

Sections are never collapsed (K-10), so there is no section expansion to animate.

### 3.4 Progress (P)

| ID | Moment | Where | Motion | Reduced motion |
|---|---|---|---|---|
| P1 | The employee's action is executing | DecisionBar | The button locks and its label changes instantly ("Đang đổi lịch…"); the loader rotates, `--ease-linear`, one turn per second. Queue rows show the chip "Đang thực hiện" and no loader | Static loader icon |
| P2 | Retry count changes ("lần thử 2 trên 3") | DecisionBar status line, section 8 | Text changes instantly with the change mark | Static mark |
| P3 | Investigation progress ("đã đọc 3 trên 5 nguồn") | K4 header, section 4 | Text changes instantly; no spinner, pulse or dots | Same |

### 3.5 Verification (V)

| ID | Moment | Where | Motion | Reduced motion |
|---|---|---|---|---|
| V1 | A day of the window passes while the case is open | K4 section 9 | New segments by opacity over `--dur-fast` (motion.md, Verification segment); the sentence updates instantly; one beat however many days passed | Instant |
| V2 | Recurrence | K4 sections 2 and 9, row | The triangle event appears instantly with the change mark; S1 if the state changes | Static mark |
| V3 | A guard condition breaks (reservation lost) | K4 section 9 | The event row with the change mark; the checklist item's words change instantly | Static mark |

### 3.6 Completion (R)

| ID | Moment | Where | Motion | Reduced motion |
|---|---|---|---|---|
| R1 | The employee's own action is confirmed by the server | DecisionBar, section 8 | The locked button is replaced by the result line ("Đã chốt lúc 14:18 · A-20931") by a `--dur-fast` crossfade; section 8 gains its row with the change mark; focus moves to the result line, because the focused button is gone | Instant |
| R2 | The completed case leaves the employee's view | K2 queue | The row stays in place, muted, "Đã xong với bạn", until the employee moves on or applies the update control | Same |
| R3 | RESOLVED | K4, row | StateChip crossfade over `--dur-fast`; the check node appears instantly; no settle (MASTER §12) | Instant |

### 3.7 Feedback (F)

Hover changes color and border instantly, only for fine pointers; there is no press scale; the focus ring appears instantly; a
selected row turns `--sunken` with its `--accent` bar instantly; opening a case and switching views are instant.

## 4. Budget per screen

| Screen | May move | Never moves |
|---|---|---|
| K1 Tổng quan | E4 | Counts, rows, blocks |
| K2 Hàng ưu tiên | Q1 to Q5, and K4 inside it | Row positions, the pane layout, the header |
| K3 Ma sát | Q3 on cluster rows, E4 | Table order, filters |
| K4 Chi tiết ca | S1 to S5, E1, E4, P1 to P3, V1 to V3, R1 to R3 | The header's position, the section order, the spine, the briefing, "Không nên" |
| K5 Khách hàng | E4 | Everything else (profiles are not live) |
| K6 Truy vết và nhật ký | Q3 on new rows appended at the end (no scrolling), E1 | Existing rows |
| K7 Phím tắt | E4 | Everything else |

## 5. In the Demo stage and on Landing

**Demo stage.** The console region is compact and follows this map. "Linh kiện bị điều đi" produces Q1 (or Q3 and S1 on an open case);
"Tua +2 ngày" produces V1; "Tua +14 ngày" produces R3 only. AgentTrace rows appear instantly.

**Landing figures.** A scroll-scrubbed figure changes because the reader scrolled, which is the reader's own action, so the console
figure changes instantly (rule 2; landing-motion-map.md §3).

## 6. What never moves

Row order and position; panes and the header; the alert slot; the spine and the section order; "Không nên" and the agent's promises;
deadlines (their words and color change, nothing animates); counts; anything the employee just did; anything on load.

## 7. Rejected ideas

| Idea | Why not |
|---|---|
| Rows sliding to new positions when the order changes | Moves targets under the pointer; position must keep meaning priority |
| Pulsing or flashing overdue deadlines | Words and color carry urgency; flashing causes alarm fatigue and risks WCAG 2.3.1 |
| Toasts for new cases | Cover panes and duplicate the update control and the alert slot |
| A colored highlight (amber, teal, green) for changes | Collides with state colors; the change mark uses `--sunken` only |
| A slide-in case pane | Opening a case happens hundreds of times a shift |
| Smooth scrolling to sections | Slows the jump the employee asked for |
| Count-up numbers on the Overview | Counts are facts |
| An animated progress bar while executing | Claims progress nobody can measure |
| Skeleton shimmer | Skeletons are static (components.md §10) |
| A settle on RESOLVED, as on Customer | MASTER §12: CSKH has none; resolution is routine for staff |

## 8. Test checklist

- [ ] Keyboard-only shift: `j`, `k`, `Enter`, `1` to `0`, `n` and every dialog produce no animation except the dialog fade.
- [ ] Server updates during a session: each changed element shows one cue; no row moves; the update control batches arrivals.
- [ ] Click guard: a click within `--dur-slow` of a DecisionBar change is ignored and the status line explains it.
- [ ] Safety: the alert slot and pinned row appear without motion and without shifting panes; `role="alert"` heard once.
- [ ] The loader is the only loop and stops with the result.
- [ ] Reduced motion: every cue is the static "Vừa đổi" mark; nothing fades or rotates.
- [ ] Forced colors: the change mark's text remains; states remain distinguishable by shape, icon and word.
