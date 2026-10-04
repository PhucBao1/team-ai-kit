# Customer motion map

Every movement on the customer surface, why it exists, and what replaces it when motion is off. Screens are in
[customer-screen-spec.md](customer-screen-spec.md); the journey is [customer-journey.md](customer-journey.md). The catalogue and
the rules are [motion.md](../../design-system/proactive-care/motion.md); this file maps customer moments onto them. Values are tokens
from [tokens.md](../../design-system/proactive-care/tokens.md). Motion direction follows emil-design-eng. No code here.

## 1. What MOTION 5 means on this surface

MOTION is 5 on Customer (MASTER §2.1): motion confirms that something changed. It never decorates, never waits, never loops (except
the EXECUTING loader), and never runs longer than `--dur-slow`. Landing (8) tells a story with motion; CSKH (2) changes instantly;
the customer sits between: each change they witness gets one short movement, and nothing else moves.

The decision per moment follows emil-design-eng's frequency framework:

| How often the customer meets it | Moments | Decision |
|---|---|---|
| Many times per visit: navigation, tabs, scrolling, typing | F4, typing in C6 | No motion |
| Several times per visit: hover, press, disclosures, choosing | F1, F2, F3, A1, A2 | Feedback only, at most `--dur-fast` (press `--dur-press`) |
| Occasional: a notification, a state change, a confirmation, progress | N, S, A3 to A5, P, V | One beat of at most `--dur-base` |
| Rare: a case resolved | R1 | One settle, still `--dur-base`, once |

The brief's six uses map to groups: notifications (N), state changes (S), confirmations (A), progress (P), verification (V),
resolved state (R). Feedback (F) is the baseline every surface has.

## 2. Rules

1. **Witnessed change only.** Motion is for a change that happens while the customer is looking. A change that happened while they
   were away is shown finished, marked in words ("Mới", "Cập nhật lúc 14:18"); nothing replays on arrival (motion.md principle 6).
2. **One beat per update.** Everything one server event changes lands within one beat of at most `--dur-base` (stagger aside). The
   element that answers "what changed?" is the focal element and may rise; everything else crossfades or changes instantly.
3. **Focal priority.** Action result, then state chip, then a new timeline item, then counts. If an update both progresses and
   resolves a case, only the resolution moves.
4. **Waiting never moves.** WAITING FOR CUSTOMER, WAITING FOR HUMAN and VERIFYING between updates are still. Deadlines are text.
5. **Urgency is never motion.** Safety appears instantly; errors do not shake; nothing pulses.
6. **Navigation is instant.** Tabs, pushes, back, and anchor jumps from notifications.
7. **Keyboard actions do not animate**, including arrow-key choice in an option group and Enter on a button.
8. **Interruptible.** Anything that can repeat (notices, chips, switches) uses transitions, not keyframes.
9. **Transform and opacity only**, plus selection color over `--dur-fast` (motion.md principle 4).
10. **Reduced motion is complete.** Rises become opacity over `--dur-fast` or instant; staggers become simultaneous; the loader is a
    static icon; the settle is instant (motion.md §5).

## 3. Moments

### 3.1 Notifications (N)

| ID | Moment | Where | Motion | Reduced motion | Announcement |
|---|---|---|---|---|---|
| N1 | New notification while the app is open | C2, C3, C5, C6, C8 | In-app notice: enters from the top edge under the header, `--rise-md` and opacity, `--dur-base`, `--ease-out`; leaves the way it came, `--dur-fast`. Stays at least 5 seconds, pauses while hovered or focused; a second notice replaces the text with a crossfade, never stacks; "Đóng" closes it; tapping opens the case | Opacity only | "Tin mới từ Trợ lý AI: " plus the first sentence, through the screen's polite region (the notice itself is not a live region) |
| N2 | New notification while C4 is open | C4 | At the top of the list: the row enters, `--rise-sm`, `--dur-base`. Scrolled down: a "1 thông báo mới" control enters instead and nothing moves under the reader | Instant | "1 thông báo mới" |
| N3 | Unread count changes | BottomNav | None. The number changes in a fixed-width slot | None | Once per arrival, in words: "Thông báo: 2 tin chưa đọc" |
| N4 | A new case, or one that should change section | C1 | The control "1 việc mới cần anh/chị. Hiện ngay" enters (`--rise-sm`, `--dur-base`). On press: sections update instantly and the new summary card enters (`--rise-md`, `--dur-base`); focus moves to its heading | Instant | "1 việc mới" |
| N5 | Safety | Every screen | None. The banner appears instantly | None | `role="alert"`, once |

### 3.2 State changes (S)

| ID | Moment | Where | Motion | Reduced motion | Announcement |
|---|---|---|---|---|---|
| S1 | The case's state changes | C1 cards, C2, C3 header | StateChip crossfade, `--dur-fast`. The condensed strip's current node changes instantly (color marks the present) | Instant | "Trạng thái: " plus the label |
| S2 | A head line changes ("Bên em đang làm", "Việc của anh/chị") | C1, C2 | The changed line crossfades, `--dur-fast`, without rise (rising text would jitter the lines below); unchanged lines stay still | Instant | Part of S1's announcement when the state changed; otherwise none |
| S3 | A new timeline item | C3 | The item enters, `--rise-sm`, `--dur-base`; the previous current node turns neutral instantly; the connector appears with the item, never drawn | Instant | None beyond S1 |
| S4 | A person takes over (ESCALATED) | C1, C2 | The StaffByline and the new lines crossfade in, `--dur-fast` (motion.md, ESCALATED change) | Instant | "Trạng thái: Nhân viên đang xử lý. Anh Hải sẽ gọi trước 14:21." |
| S5 | The plan must change (J2) | C2 | The change line enters as the focal element, `--rise-md`, `--dur-base`; the old receipt fades out over `--dur-fast`, overlapping; the new options follow with `--stagger`; the action bar enters (F7) | Change line and options appear together; bar instant | "Lịch hẹn cần đổi: " plus the change line |
| S6 | A hold expires | C2 | S1 and S2 only; options become muted instantly; the bar's label changes instantly to "Tạo lại phương án" | Instant | "Phương án đã hết hạn giữ chỗ." |

### 3.3 Confirmations (A)

| ID | Moment | Where | Motion | Reduced motion | Announcement |
|---|---|---|---|---|---|
| A1 | An option is chosen | C2, C6 | The option's border and radio change color over `--dur-fast`; the DecisionBlock values change instantly (parameters being confirmed are never in a half-faded state; emil-design-eng team rule); the bar's choice line and label ("Chọn lịch" to "Xác nhận đặt lịch") change instantly. By keyboard: all instant | Instant | None (the radio's own state is read) |
| A2 | The confirm button is pressed | C2, C6 | `--press-scale` over `--dur-press`, pointer only | None | None |
| A3 | The action starts | C2, C6 | The button locks at once and its label changes instantly to "Đang đặt lịch…"; the loader icon appears in it (P2). No overlay, no dimming | Static icon | None until the result |
| A4 | The server confirms | C2, C6 | The ConfirmationReceipt replaces the DecisionBlock: the receipt enters, `--rise-md`, `--dur-base`; the DecisionBlock fades out over `--dur-fast`, overlapping; the action bar leaves (F7). Focus moves to the receipt heading, scrolled into view without smooth scrolling | Receipt by opacity, bar instant | "Đã đặt lịch: Long Biên, 14:00 thứ Sáu 02/10." |
| A5 | The server refuses or fails | C2, C6 | The error message enters, `--rise-sm`, `--dur-base`; the button unlocks instantly as "Thử lại". No shake, no red flash | Instant | `role="alert"` with the error sentence |

### 3.4 Progress (P)

| ID | Moment | Where | Motion | Reduced motion | Announcement |
|---|---|---|---|---|---|
| P1 | The AI checks sources for a question the customer asked | C6 | Each finished check row enters, opacity over `--dur-fast`, as it completes; after 2 seconds without news, elapsed time appears as text. No spinner, pulse or typing dots | Instant rows | "Đã kiểm tra 3 trên 5 nguồn", once on completion |
| P2 | EXECUTING | Locked button | Loader icon rotation, `--ease-linear`, one turn per second, until the result. The only loop on the surface | Static loader icon; the label carries the meaning | `aria-busy` on the region; the result is announced (A4, A5) |
| P3 | A streamed reply | C6 | A static text-shaped skeleton before the first words; words appear as they arrive, with no per-word animation | Same | The whole reply, once complete |

### 3.5 Verification (V)

| ID | Moment | Where | Motion | Reduced motion | Announcement |
|---|---|---|---|---|---|
| V1 | A guard condition changes (the reservation is lost) | C2 | The checklist item's text crossfades, `--dur-fast`; the change itself is S5 | Instant | Through S5 |
| V2 | Days of the window pass while the customer looks (or the demo clock advances) | C2, C3 | Newly filled segments change opacity together, `--dur-base`: one beat however many days passed; the sentence crossfades (S2). No counting numbers | Instant | "Đã theo dõi 3 trên 7 ngày, xe chưa báo lại lỗi." |
| V3 | The warning returns during the window (UC6) | C2, C3 | The event enters as the focal element, `--rise-md`, `--dur-base`; the meter does not drain or shake, it stops | Instant | "Cảnh báo quay lại. Bên em đã mở lại việc." |

### 3.6 Resolved (R)

| ID | Moment | Where | Motion | Reduced motion | Announcement |
|---|---|---|---|---|---|
| R1 | The case resolves while the customer looks | C2, C3 | The verified node settles once from `--enter-scale` with opacity, `--dur-base`, `--ease-out` (motion.md, RESOLVED settle); the chip crossfades (S1); the outcome sentence crossfades (S2). Nothing else: no confetti, glow, color flash, sound or vibration | Instant | "Đã xử lý xong. Xe không báo lại lỗi trong 7 ngày theo dõi.", once |
| R2 | The case resolved while the customer was away | C1, C2, C3, C4 | None. The screen opens finished; "Mới" marks the case in C1 and C4 until viewed | None | None |

### 3.7 Feedback (F)

| ID | Moment | Motion | Reduced motion |
|---|---|---|---|
| F1 | Press on a button or a whole-row link | `--press-scale` over `--dur-press`, pointer only | None |
| F2 | Hover | Color and border only, `--dur-fast`, only under `(hover: hover) and (pointer: fine)` | Instant |
| F3 | Disclosure ("Em đã kiểm tra 4 nguồn", "Điều em chưa biết") | Opened by pointer: chevron rotates over `--dur-fast`. Opened by keyboard: instant. Content appears without height animation | Instant |
| F4 | Tabs, push, back, anchor jumps | None | None |
| F5 | Switch (C5 data sharing, C8) | By pointer: thumb moves over `--dur-fast`, `--ease-out`; on a failed save it moves back the same way. By keyboard: instant | Instant |
| F6 | Dialog ("Huỷ lịch", "Xoá ghi nhớ") | From `--enter-scale` with opacity over `--dur-slow`; leaves over `--dur-fast` | Opacity only |
| F7 | The sticky action bar appears or leaves while the customer looks | Enters from below by its own height with opacity, `--dur-base`, `--ease-out`; leaves the same way over `--dur-fast`. A screen opened in a decision state shows the bar already in place | Instant |

## 4. Budget per screen

| Screen | May move | Never moves |
|---|---|---|
| C1 Việc của tôi | N4, S1, S2, S4, F1, F2 | Section order, cards under the reader, the status sentence's position, BottomNav |
| C2 Chi tiết việc | N1, S1, S2, S4, S5, S6, A1 to A5, P2, V1 to V3, R1, F1 to F3, F6, F7 | The head's position, the header, "Gặp nhân viên", sections that did not change |
| C3 Tiến trình xử lý | N1, S1, S3, V2, V3, R1, F3 | History items |
| C4 Thông báo | N2, F1, F2 | Read and unread changes (weight changes instantly), day headings |
| C5 Xe của tôi | N1, F1 to F3, F5, F6 | Everything else |
| C6 Trợ lý AI | N1, P1, P2, P3, A1 to A5; new messages enter with `--rise-sm`, `--dur-base`; C-05 keeps a reader at the newest message with an instant jump | Earlier messages; the composer |
| C7 Cảnh báo an toàn | Nothing | Everything |
| C8 Cài đặt thông báo | N1, F5 | Everything else |

## 5. In the Demo stage

The Demo stage (D1) is where witnessed changes happen on purpose: the presenter drives events while the phone frame shows the
customer surface live. Only this map's motion runs there; the demo adds none of its own.

| Demo action | What moves in the phone |
|---|---|
| "Linh kiện bị điều đi" (inject `parts.reservation.cancelled`) | N1 or N4, then S5 on C2 |
| "Tua +2 ngày" during the window | V2, one beat |
| "Tua +14 ngày" | R1 only: the window completes and resolves in one update, so the segments fill instantly and the settle is the focal element |
| "Đặt lại" | Nothing; the screens reload in their initial state |

## 6. What never moves

Page load and first paint; navigation between screens; the header and "Gặp nhân viên"; waiting states; deadlines; numbers counting;
the unread count; history in the timeline; safety; anything under the reader's pointer that a live update would push; any element
while the customer types.

## 7. Rejected ideas

| Idea | Why not |
|---|---|
| Confetti, glow or a color flash on RESOLVED | A trust product, not a game; MASTER §12 forbids it; one settle is enough |
| A pulsing amber diamond while waiting for the customer | Waiting is never animated; pulsing creates urgency (taste-rules rule 9) |
| Typing dots or a "thinking" animation | Fakes activity; MASTER §17 |
| Counting-up numbers in the VerificationMeter | Days are facts, not a show; the sentence carries the meaning |
| An indeterminate progress bar while EXECUTING | Claims progress the system cannot measure; the locked button says what is happening |
| Slide transitions between screens | Frequent navigation; older readers lose their place; emil: never animate the frequent |
| Shake on error | Alarming and inaccessible; the message and "Thử lại" are enough |
| Skeleton shimmer | Skeletons are static (components.md §10) |
| Toasts that close after 3 seconds (ui-ux-pro-max default) | Older readers need time; at least 5 seconds with pause on hover or focus |
| Replaying a resolution the customer missed | Motion only for witnessed change; a replay would be decoration |

## 8. Test checklist

- [ ] Every movement on a customer screen is listed in §3 and in the motion.md catalogue for Customer.
- [ ] Nothing moves on first paint, on navigation, or when a screen opens on a state that changed while the customer was away.
- [ ] One server event produces one beat; only the focal element rises.
- [ ] The loader is the only loop, and it stops with the result.
- [ ] Keyboard-only run: no press scale, no animated choice, focus lands on the receipt after confirming.
- [ ] Reduced motion: every row of §3 matches its "Reduced motion" column; nothing loops.
- [ ] In-app notices last at least 5 seconds, pause on hover and focus, never stack, and never cover "Gặp nhân viên".
- [ ] Demo stage: "Tua +14 ngày" produces R1 only.
- [ ] Screen reader: each announcement in §3 is heard once, in words, never word by word.
