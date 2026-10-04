# Customer screen specification

Every customer screen: its purpose, hierarchy, actions, states and behavior. Built on [MASTER](../../design-system/proactive-care/MASTER.md)
and the Customer deviations in [pages/customer.md](../../design-system/proactive-care/pages/customer.md). The journey through these
screens is [customer-journey.md](customer-journey.md); motion is [customer-motion-map.md](customer-motion-map.md). Source: owner brief
of 2026-10-03 (customer experience). No code; nothing here changes P-073.

**Status.** Part of design contract v1.0 (MASTER §18). The information architecture changes the customer side of spec §20 from chat-first to home-first; the product
owner confirms this in D-13. Fields that the contract lacks are listed per screen and in D-04, D-06 and D-14; until they exist the
screens show only what the API returns.

**Audience.** Car owners and permitted drivers, some elderly, mostly on phones. Body `--text-lg`, nothing below `--text-md`
(C-01, C-02), primary action `--control-h-lg` (C-03), no data tables (C-04). Design width 390px; every screen also works at 320px.

---

## 1. Information architecture

```text
Bottom navigation (phones):   Việc (C1)        Thông báo (C4)        Xe (C5)

C1 Việc của tôi ──► C2 Chi tiết việc ──► C3 Tiến trình xử lý
      │                   └──► C6 Trợ lý AI, about this case ("Hỏi thêm về việc này")
      └──► C6 Trợ lý AI ("Có câu hỏi khác?")
C4 Thông báo ──► C2 (the part of the case the notification is about) ──► C8 Cài đặt thông báo
C5 Xe của tôi ──► C2 (the case behind an active warning)              ──► C8
C7 Cảnh báo an toàn: a state shown over any screen, not a destination
```

| ID | Screen (title in the interface) | Brief's IA item | Level | Proposed route | Reached from |
|---|---|---|---|---|---|
| C1 | Việc của tôi | Customer Home | Top | `/khach` | Tab "Việc"; Landing door; app start |
| C2 | Chi tiết việc (title: the case) | Customer Active Care | Pushed | `/khach/viec/:journeyId` | C1, C4, C5, external notifications |
| C3 | Tiến trình xử lý | Customer Journey | Pushed | `/khach/viec/:journeyId/tien-trinh` | C2 |
| C4 | Thông báo | Notifications | Top | `/khach/thong-bao` | Tab "Thông báo" |
| C5 | Xe của tôi | Vehicle and service context | Top | `/khach/xe`, `/khach/xe/:vin` with more than one vehicle | Tab "Xe"; vehicle line on C2 |
| C6 | Trợ lý AI | (spec §20 "Chat khách") | Pushed | `/khach/tro-ly`, `?viec=:journeyId` with a case | C1, C2 |
| C7 | Cảnh báo an toàn | (safety) | State over any screen | none | A safety event |
| C8 | Cài đặt thông báo | (proposal §09 right to refuse; D-12) | Pushed | `/khach/cai-dat` | C4, C5, the "Vì sao anh/chị nhận tin này" line |

**Why home-first.** The brief asks for a real customer product, not a chatbot demo. Proactive care is organized around cases, and the
customer's first question is "does anything need me?", which a list of cases answers and a chat thread does not. The conversation
stays (spec §20, task C1.03) as one way to act on a case, reached from where the question arises. Proactive cards appear in it too.

**Why three tabs.** Home, Notifications and Vehicle are the places a customer comes back to. At 320px three labels fit on one line
at `--text-md` (C-02); four do not ("Thông báo" alone needs about 80px). The conversation is reached in context, which also gives
the AI the case it is being asked about.

## 2. Shared frame

| Element | Rule |
|---|---|
| Skip link | "Bỏ qua tới nội dung chính", first focusable element |
| AppHeader | One line, at most 72px. Top-level screens: the product name (D-07). Pushed screens: a back link that names its destination ("Việc của tôi", "Thông báo"), never a bare arrow. "Gặp nhân viên" (HelpAction) at the right end on every screen, in the same position (WCAG 3.2.6). From `md` up, the three destinations sit in the header as text links |
| Banners | Directly under the header, in this order: safety (C7), connection (MASTER §11), demo mode (D1 only). Banners push content down and never cover the header |
| BottomNav | Phones only, on C1, C4 and C5. Three items ("Việc" `list-checks`, "Thông báo" `bell`, "Xe" `car`), icon above a one-line label, current item marked with `aria-current="page"` and an `--accent` indicator. The "Thông báo" item carries the unread count in a fixed-width slot, so a new count never shifts the layout |
| Sticky action bar | Only on C2 in a decision state, where no BottomNav is shown (C-03) |
| In-app notice | A toast under the header for a new notification while the customer is on C2, C3, C5, C6 or C8 (motion N1). Never on C1 (C1 uses its own update control) or C4 (the row itself appears). Never the only record: C4 keeps every notification |
| Theme | "Theo máy" by default; the switch lives in C8 below `md` and in the header from `md` up (C-06) |
| Width | One column, at most `--w-customer`, centered from `md`; side gutter `--gutter-sm` |
| Announcements | One polite live region per screen; errors and safety use `role="alert"` (accessibility.md §3) |
| Time | Absolute and in `vi-VN`: "08:16, thứ Ba 29/09"; "Hôm nay" and "Hôm qua" only as day group headings in C4 |

## 3. The proactive care card

The reusable pattern for anything the system brings to the customer. Component: CareCard ([components.md](../../design-system/proactive-care/components.md) §6).
It follows the brief's order: AI detected something, what happened, why we reached out, what we checked, what we recommend, the
customer's action, the result.

### 3.1 Anatomy

| # | Part | Label or heading | Content | Rules |
|---|---|---|---|---|
| 0 | Provenance | AIByline "Trợ lý AI · Tin tự động" and time; the vehicle line "VF 8 (…4821)" | Who wrote it, when, about which vehicle | Always visible; mandatory labels (content.md §2). A case started by staff carries a StaffByline instead |
| 1 | AI detected something | The title (`h1` on C2, `h3` in a summary) | What was detected, in at most 8 words, without codes | "Hệ thống làm mát pin báo lỗi lặp lại" |
| 2 | What happened | "Phát hiện" | One sentence with its source and time | "Xe gửi cảnh báo hệ thống làm mát pin 3 lần trong 14 ngày (dữ liệu xe, 08:15 hôm nay)." |
| 3 | Why we reached out | "Vì sao anh/chị nhận tin này" | One line, plus the link "Tắt tin chủ động" to C8 | Always visible; never collapsed. For a case the customer started: "Bắt đầu từ tin nhắn của anh/chị lúc …" |
| S | What the AI is doing | StateChip, then "Bên em đang làm" | The state and one sentence from MASTER §12 | Answers question 3 |
| Y | What you need to do | "Việc của anh/chị" | One line with an absolute deadline | Never empty: "Anh/chị chưa cần làm gì." |
| 4 | What we checked | Disclosure "Em đã kiểm tra N nguồn: …" (`h2` "Em đã kiểm tra" on C2) | EvidenceList: fact, source name, read time | The summary names the sources; collapsed by default |
| 5 | What we recommend | `h2` "Em đề xuất" | The recommendation sentence; the warranty line, neutral; OptionList; "Vì sao em đề xuất các lịch này"; the options not chosen, with reasons; "Điều em chưa biết" | No diagnosis, no price the API did not return, "đủ điều kiện sơ bộ", never "được bảo hành" |
| 6 | Your action | `h2` "Việc anh/chị cần làm" | DecisionBlock (every parameter, deadline, one primary, "Chọn phương án khác"); "Sau khi anh/chị xác nhận" (ActionScope for this case); after the server confirms, the ConfirmationReceipt | Level 2 only; level-0 advice shows the advice instead; when nothing is needed the section is one sentence |
| 7 | Result | `h2` "Kết quả" | Before: how the result will be verified. During: the guard checklist, then the VerificationMeter. After: the verified outcome with its evidence | "Done" means verified (MASTER §12) |
| 8 | Responsibility | `h2` "Ai đang phụ trách" | The owner, any staff involved with role and promise, HelpAction | Answers "when is a human involved?" |

The **head** (parts 0, 1, 3, S and Y, plus 2 on C2) answers the four questions of [customer-journey.md](customer-journey.md) §1 and
fits above the action bar at 390 by 844. The **body** (parts 4 to 8) is where the customer inspects and acts.

### 3.2 Variants

| Variant | Where | Shows | Primary action |
|---|---|---|---|
| Full | C2 | Every part | The DecisionBlock action, in the sticky bar on phones |
| Summary | C1 | 0 (compact), 1, S, 3, Y and one action | A link styled as a button that names the task: "Xem và chọn lịch" |
| Message | C6 thread | The head, 5 with the options, 6 inline, 4 collapsed, and "Xem chi tiết việc" | The DecisionBlock action, inline (the composer holds the bottom edge) |
| Row | C4 | Not a card: 0 (compact), 1 and 2 as the title, 3, the current state | The row is one link |
| Figure | Landing, Demo stage | As the surface it illustrates; inert on Landing | None on Landing |

One case has one card. Later states update the same card; the conversation can show several messages about one case, and each
links to the same C2.

### 3.3 Slots by state

UC1 copy unless noted. DETECTED and INVESTIGATING are not shown live for proactive cases (MASTER §12); in a conversation the customer
started, INVESTIGATING shows "Em đang kiểm tra lịch sử bảo dưỡng và phiên bản phần mềm của xe…" with "Anh/chị chưa cần làm gì."

| State or event | Bên em đang làm (S) | Việc của anh/chị (Y) | Em đề xuất (5) | Việc anh/chị cần làm (6) | Kết quả (7) |
|---|---|---|---|---|---|
| RECOMMENDING, level 0 (UC2) | "Em đã kiểm tra trụ sạc và lịch sử sạc của xe." | "Không bắt buộc. Nếu cần sạc ngay, trạm … còn trống." | The advice, with distance and reachability | One sentence: "Không cần xác nhận." | "Bên em sẽ kiểm tra lần sạc tiếp theo của xe." |
| WAITING FOR CUSTOMER | "Em đã tìm 2 lịch còn linh kiện, giữ chỗ đến 18:00 hôm nay." | "Chọn một lịch và xác nhận trước 18:00 hôm nay." | Options selectable; reasons; excluded options; unknowns | DecisionBlock ready; ActionScope | "Khi nào xong: sau khi sửa, bên em theo dõi 7 ngày. Xe không báo lại lỗi thì việc mới được đóng." |
| Change needed (event, J2) | "Lịch phải đổi vì linh kiện ở Long Biên được điều đi. Bên em xin lỗi vì sự thay đổi này." | "Chọn lịch mới trước 18:00 hôm nay." | New options; the old workshop listed as excluded with its reason | DecisionBlock ready; the old receipt is replaced by the change line | Unchanged |
| WAITING FOR HUMAN | "Phương án này cần nhân viên duyệt. Bên em sẽ báo lại trước 16:00." | "Anh/chị chưa cần làm gì." | What is being decided, without promising it | One sentence with the reason a person decides: "Vì có liên quan đến chi phí." | Unchanged |
| EXECUTING | "Đang đặt lịch…" | "Anh/chị chưa cần làm gì." | Collapsed to the chosen option | DecisionBlock locked | Unchanged |
| Execution failed (event) | "Chưa đặt được lịch vì hệ thống xưởng chưa phản hồi. Em đang kiểm tra lại." | "Anh/chị chưa cần làm gì." | Unchanged | DecisionBlock failed: the message inline and "Thử lại" | Unchanged |
| Expired (event) | "Phương án đã hết hạn giữ chỗ lúc 18:00." | "Tạo lại phương án nếu anh/chị vẫn muốn kiểm tra." | Options muted, not selectable | "Tạo lại phương án" | Unchanged |
| VERIFYING, guard | "Bên em đang theo dõi để lịch hẹn và linh kiện luôn sẵn sàng đến ngày hẹn." | "Đưa xe tới xưởng Long Biên lúc 14:00 thứ Sáu 02/10." | Collapsed: "Em đã đề xuất kiểm tra tại xưởng. Anh/chị chọn Long Biên." with "Xem các phương án đã đưa ra" | ConfirmationReceipt with "Đổi lịch" and "Huỷ lịch" | Guard checklist: "Linh kiện đang được giữ", "Lịch hẹn còn hiệu lực" |
| ESCALATED | "Anh Hải, cố vấn dịch vụ xưởng Long Biên, đang trực tiếp xử lý và sẽ gọi anh/chị trước 14:21." | "Nghe máy khi anh Hải gọi, trước 14:21." | Options read-only, so both sides talk about the same choices | One sentence: "Anh Hải sẽ chốt cùng anh/chị qua điện thoại." | Unchanged |
| VERIFYING, window | "Đang theo dõi kết quả: 3 trên 7 ngày, xe chưa báo lại lỗi." | "Anh/chị chưa cần làm gì." | Collapsed | "Đã sửa tại xưởng Gia Lâm, thứ Bảy 03/10." | VerificationMeter with the sentence first |
| Recurrence (event, UC6) | "Cảnh báo quay lại sau 4 ngày. Bên em đã mở lại việc và ưu tiên kiểm tra." | From the new linked case | Collapsed | Link to the new case | Meter stops; the sentence says why |
| RESOLVED | "Đã xử lý xong. Xe không báo lại lỗi trong 7 ngày theo dõi." | "Không còn việc gì cần làm." | Collapsed | Collapsed to the receipt line | The verified outcome in `--ok`, with "Dựa trên dữ liệu xe 7 ngày qua" |
| ESCALATED, safety | See C7 | From the pre-approved template | Not shown | Not shown | Not shown |

Copy for deadlines, times and windows comes from the API; the examples above are sample data.

### 3.4 Rules

1. **The order is fixed.** Parts never move between states; their content changes. A customer who learned where "Việc của anh/chị"
   is will find it there every time.
2. **No empty labels, no invented parts.** A part without data is left out, except parts 3 and Y, which are mandatory. With today's
   contract the card shows the message text in place of parts 2 and 3 (§3.5), never an empty "Phát hiện".
3. **One primary action per card**, specific to the task. When the customer has nothing to do, there is no primary action at all.
4. **Changes are told, not just shown.** When a later event changes the plan, a change line ("Thay đổi gần nhất (…): …") sits under
   the head until the next state, with one apology when the company caused it.
5. **The head fits.** At 390 by 844 the head ends above the sticky action bar (content.md §6). If copy grows past that, shorten the
   copy; do not move parts below the fold.

### 3.5 Data today and gaps

| Part | Today (`api.yaml` v0.2.0) | Gap |
|---|---|---|
| 0 Provenance | Arrival through `/stream/{customer_id}` implies a proactive message | Author and origin per message (D-06) |
| 1 Title | `Journey.title` | |
| 2, 3 What happened, why | Inside `ChatEvent.text` as prose | Structured "what happened" and "why" (D-06, D-14) |
| S State | `Journey.current_step` is a job step string, not a state | Case state (D-04) |
| Y Your part | Derivable: a `confirmation_token` with options means "choose and confirm" | The hold deadline (token expiry) (D-14) |
| 4 Evidence | `ChatEvent.citations` (raw references), mapped to source names by a fixed table in `vi.ts` | Read time per fact (D-14) |
| 5 Options | `ChatEvent.options` (`Option` with `why`, `parts_ready`, `range_ok`, `distance_km`) | Excluded options with reasons; unknowns (D-14) |
| 6 Action | `POST /api/v1/confirm` → `ConfirmResult` | Decline action (D-03, CQ-1) |
| 7 Result | None | Verification phase, window, progress (D-06) |
| 8 Responsibility | `Journey.owner`, `Journey.promises` | Staff display name and role for customers (D-06) |

## 4. Screens

### C1. Việc của tôi (Customer Home)

**Purpose.** Answer at a glance: does anything need me, and is everything else in hand?

**Hierarchy** (390px, top to bottom):
1. AppHeader: product name, "Gặp nhân viên".
2. Banners, if any.
3. `h1` "Việc của tôi", then one status sentence: "1 việc cần anh/chị xác nhận." / "Bên em đang lo 2 việc. Anh/chị chưa cần làm gì." / "Không có việc nào đang mở."
4. `h2` "Việc cần anh/chị": one CareCard summary per case waiting on the customer, earliest deadline first. Shown only when there is one.
5. `h2` "Bên em đang xử lý": compact JobCards as hairline-separated rows, not cards (title, vehicle, StateChip, the state sentence, the
   next commitment from a PromiseLine). Only the cases under "Việc cần anh/chị" are boxed, because only they ask something of the customer.
   ESCALATED first, because a person is about to call; then by latest change. At most 3, then "Xem tất cả 5 việc".
6. `h2` "Đã xong gần đây": the two most recent RESOLVED cases as rows with their verified sentence and date; "Xem việc đã xong" (C1 with `?xem=da-xong`).
7. "Có câu hỏi khác? Hỏi Trợ lý AI" (to C6).
8. BottomNav.

**Primary action.** The summary card's action for the first case under "Việc cần anh/chị", named for the task ("Xem và chọn lịch").
When nothing needs the customer there is no primary action; the screen is calm on purpose.

**Secondary actions.** "Xem chi tiết" on each JobCard; "Hỏi Trợ lý AI"; "Gặp nhân viên"; "Xem việc đã xong".

**System states.**

| Condition | Shows |
|---|---|
| A case waits on the customer | Its summary card under "Việc cần anh/chị"; the status sentence counts it |
| WAITING FOR HUMAN, EXECUTING, VERIFYING, ESCALATED | A compact JobCard under "Bên em đang xử lý"; ESCALATED shows the staff name and promised time |
| RESOLVED | Under "Đã xong gần đây" |
| A live update to a case already on screen | The card's content changes in place (motion S1, S2); cards never move under the reader |
| A new case, or a case that should change section | A control under the status sentence: "1 việc mới cần anh/chị. Hiện ngay" (motion N4). Applied when pressed, or on the next visit |
| Safety | C7: the safety card replaces the status sentence and comes first; other sections stay below |
| Driver without booking rights | A booking case appears under "Bên em đang xử lý" with "Chủ xe sẽ xác nhận lịch này.", not under "Việc cần anh/chị" |
| Opted out of AI proactive messages | One line under the status sentence: "Anh/chị đã tắt tin chủ động do Trợ lý AI soạn." with "Bật lại" (C8) |

**Empty.** "Chưa có việc nào. Khi anh/chị đặt lịch hoặc bên em phát hiện điều cần xử lý, tiến độ sẽ hiện ở đây." (content.md §5),
then "Xem xe của tôi" and "Hỏi Trợ lý AI". No illustration.

**Loading.** Header, BottomNav and `h1` render at once; a skeleton of the status sentence, one summary card and two compact rows,
static, in `--sunken`; `aria-busy` on `main`. No primary action renders until the data does.

**Error.** "Chưa tải được danh sách việc vì mạng đang yếu." with "Thử lại". If an earlier copy exists it stays visible with
"Cập nhật lúc 09:12", under the connection banner. "Gặp nhân viên" always works.

**Responsive.** 320 and 390: as above. From `md`: centered column at `--w-customer`; BottomNav moves into the header; the summary
card's action sits inline at its natural width.

**Accessibility.** One `h1`; each section an `h2`; each card an `article` labelled by its title. The status sentence is the first
text after the `h1`. The summary action's accessible name includes the case ("Xem và chọn lịch, hệ thống làm mát pin"). The update
control is announced once, politely ("1 việc mới"). BottomNav is a `nav` named "Điều hướng chính"; the unread count is part of the
link's name ("Thông báo, 2 tin chưa đọc").

**Data.** `GET /api/v1/jobs/{customer_id}` → `Journey[]`. Gaps: case state for sectioning (D-04); a "needs the customer" flag and deadline (D-14).

### C2. Chi tiết việc (Customer Active Care)

**Purpose.** Everything needed to understand one case and act on it, in the brief's order, with the decision one tap away.

**Hierarchy** (390px):
1. AppHeader: back link naming where the customer came from ("Việc của tôi", "Thông báo"), "Gặp nhân viên".
2. Banners.
3. Provenance: AIByline and time; the vehicle line as a link to C5.
4. `h1`: the case title.
5. StateChip; under it the condensed CareTrace strip (seven phase nodes, the current one in its holder's shape and color) and the link "Xem tiến trình" (C3).
6. The head: "Phát hiện", "Vì sao anh/chị nhận tin này" with "Tắt tin chủ động", "Bên em đang làm", "Việc của anh/chị".
7. The change line, when the latest event changed the plan.
8. `h2` "Em đã kiểm tra": the disclosure and EvidenceList.
9. `h2` "Em đề xuất": recommendation, warranty line, OptionList, "Vì sao em đề xuất các lịch này", excluded options, "Điều em chưa biết".
10. `h2` "Việc anh/chị cần làm": DecisionBlock or receipt; "Sau khi anh/chị xác nhận".
11. `h2` "Tiến độ sửa chữa", only once a service job exists: JourneyStepper and PromiseLines.
12. `h2` "Kết quả".
13. `h2` "Ai đang phụ trách": owner, staff involved, HelpAction.
14. "Xem toàn bộ tiến trình" (C3) and "Hỏi thêm về việc này" (C6).
15. Sticky action bar on phones, in decision states only.

Sections carry anchors (`#phat-hien`, `#da-kiem-tra`, `#de-xuat`, `#viec-can-lam`, `#ket-qua`, `#phu-trach`) so notifications open
the right part. Arriving at an anchor jumps; it never scrolls smoothly.

**Primary action.**

| State | Primary | Place on phones |
|---|---|---|
| WAITING FOR CUSTOMER, more than one option, none chosen | "Chọn lịch": moves focus to the option group | Action bar |
| WAITING FOR CUSTOMER, an option chosen (or only one exists) | Names the action: "Xác nhận đặt lịch", "Xác nhận đổi lịch", "Xác nhận cập nhật phần mềm". The bar shows the choice above the button: "Long Biên, 14:00 thứ Sáu 02/10" | Action bar |
| EXECUTING | Locked, "Đang đặt lịch…" | Action bar |
| Execution failed | "Thử lại" | Action bar |
| Expired | "Tạo lại phương án" | Action bar |
| Safety | "Gọi cứu hộ 24/7" | In the banner (C7) |
| Any other state | None | No bar |

No option is preselected when there are several (CQ-6): the customer chooses, the AI explains.

**Secondary actions.** "Chọn phương án khác" (asks for other options; the case returns to RECOMMENDING); "Đổi lịch" and "Huỷ lịch" on
the receipt ("Đổi lịch" asks for new options and comes back to this screen for a new confirmation; "Huỷ lịch" confirms in a Dialog
that repeats the appointment, with "Huỷ lịch hẹn" and "Giữ lịch"); "Hỏi thêm về việc này"; "Xem toàn bộ tiến trình"; "Gặp nhân viên".
Proposed, pending D-03: "Không cần lúc này" (CQ-1).

**System states.** All nine states and the events in §3.3, plus:

| Condition | Shows |
|---|---|
| Parameters changed on the server while the customer was choosing | "Lịch này vừa thay đổi. Anh/chị kiểm tra lại trước khi xác nhận." The confirmation resets (taste-rules rule 8) |
| Driver without booking rights | Section 6 reads "Chỉ chủ xe xác nhận được lịch hẹn cho xe này. Bên em đã gửi đề xuất cho chủ xe."; no prices or invoices |
| Offline | The last known case with "Cập nhật lúc …"; the primary is replaced by "Cần có mạng để xác nhận". Confirmations are never queued offline |
| The case was merged into another | "Việc này đã được gộp vào việc …" with a link |

**Empty.** Not applicable: a case always has content. An unknown or expired link shows "Không tìm thấy việc này. Có thể đường dẫn
đã cũ." with "Về Việc của tôi".

**Loading.** A skeleton in the shape of the head (byline, two title lines, chip, four answer rows). The action bar does not render
until the case loads: no button that might turn out wrong.

**Error.** Load failure: "Chưa tải được việc này." with "Thử lại"; "Gặp nhân viên" stays active. Confirmation failure: the
DecisionBlock's failed state, inline under the parameters, `role="alert"`, with what is true now ("Lịch chưa được đặt.") and "Thử lại".

**Responsive.** Phones: the action bar per C-03; it stops being sticky when the viewport is shorter than 600px. From `md`: the action
returns inline at the end of "Việc anh/chị cần làm"; still one column; options as a vertical list at every width.

**Accessibility.** The `h1` is the case title. The head is a `dl`. The condensed strip is `aria-hidden`; the StateChip and the
sentences carry its meaning. Options are a `radiogroup`, each named with workshop, time, distance and readiness; excluded options are
text after the group. The DecisionBlock region is `aria-busy` while executing. After a successful confirmation, focus moves to the
receipt heading (the customer's own action removed the button they were on). Disclosures use `aria-expanded` and name their count.
The action bar reserves scroll padding so it never covers the focused element. Every deadline is text.

**Data.** `ChatEvent` (options, `confirmation_token`, citations), `/confirm`, `Journey`. Gaps in §3.5.

### C3. Tiến trình xử lý (Customer Journey)

**Purpose.** Show what happened, in order, who did it, and why each step followed from the one before.

**Hierarchy:**
1. AppHeader: back link "Chi tiết việc", "Gặp nhân viên".
2. `h1` "Tiến trình xử lý"; the case title and vehicle under it.
3. "Hiện tại": the state label, the "Việc của anh/chị" line, and when the customer is needed, "Tới việc cần làm".
4. The timeline: one ordered list per day, under a day heading ("Thứ Ba 29/09"). Each item has a node, label, actor, time, what
   happened, cause line and, for AI steps, an evidence disclosure ([customer-journey.md](customer-journey.md) §3).
5. The expected next phases as hollow nodes: "Tiếp theo: đặt lịch tại xưởng anh/chị chọn", "Sau đó: theo dõi 7 ngày sau khi sửa".
6. "Cách đọc tiến trình": the legend in words (circle: Trợ lý AI hoặc hệ thống; diamond: chờ một người quyết định; square: nhân viên;
   circle with check: đã xác minh; triangle: sự cố).
7. Linked cases (UC6): "Việc này mở lại từ việc ngày 03/10." with a link.

**Primary action.** "Tới việc cần làm" (to `C2#viec-can-lam`) when the customer is needed; otherwise none.

**Secondary actions.** Evidence disclosures; the linked case; "Gặp nhân viên".

**System states.** Each state adds items; the current item carries the holder's color (color marks the present) and history is
neutral. ESCALATED adds a square with the staff member's name. Events add triangles (failure) or small neutral circles (system of
record). VERIFYING shows the guard checklist or a compact VerificationMeter inside its item. RESOLVED ends the line: no future nodes.
A driver sees only the steps their rights allow, with one line: "Một số bước chỉ chủ xe xem được."

**Empty.** Not applicable: a case starts with its first signal or message.

**Loading.** The CareTrace loading form: three skeleton nodes.

**Error.** "Chưa tải được tiến trình." with "Thử lại" (components.md §2.2).

**Responsive.** Vertical at every width, the time under each label. From `md` the column widens to `--w-customer`; nothing else changes.

**Accessibility.** Each day is an `h2` followed by an `ol`; the current item has `aria-current="step"`; nodes and connectors are
`aria-hidden`; each item reads as "label, actor, time", then what happened, then the cause. The legend is visible text, not a tooltip.

**Data.** `TraceStep[]` from `/trace/{trace_id}` covers one agent run only. Gaps: a case-level timeline with actor, time, event type
and cause per item (D-06, D-14).

### C4. Thông báo (Notifications)

**Purpose.** The record of everything the system sent, each with why, each leading to its case.

**Hierarchy:**
1. AppHeader.
2. `h1` "Thông báo", with "Cài đặt thông báo" (C8) beside it.
3. Active safety notifications, pinned first while the safety case is open.
4. Day groups ("Hôm nay", "Hôm qua", "Thứ Ba 29/09"), newest first.
5. NotificationRows: sender (compact AIByline, StaffByline, or "Bên em" for receipts), kind ("Tin tự động", "Cập nhật", "Nhắc lịch",
   "An toàn") and time; the title sentence, in 600 with a "Mới" tag while unread; for proactive messages the "Vì sao anh/chị nhận tin
   này" line, for updates the reason for the change; the case's current state in words ("Hiện tại: Đã xử lý xong").
6. "Xem thông báo cũ hơn" at the end (a button, no infinite scroll).
7. BottomNav.

**Primary action.** None; every row is a link to its case.

**Secondary actions.** "Đánh dấu tất cả đã đọc"; "Cài đặt thông báo"; "Xem thông báo cũ hơn".

**System states.** Unread or read (opening the row, or viewing that case, marks it read). A notification whose case was merged leads
to the merged case. A new notification while the list is at the top enters as a row (motion N2); otherwise a control appears:
"1 thông báo mới". Opted out: one line at the top, "Anh/chị đã tắt tin chủ động do Trợ lý AI soạn. Cảnh báo an toàn và cập nhật về
việc đang làm vẫn được gửi.", with "Bật lại".

**Empty.** "Chưa có thông báo nào. Khi xe cần chú ý hoặc việc của anh/chị có thay đổi, bên em sẽ báo ở đây."

**Loading.** Three skeleton rows under the `h1`.

**Error.** "Chưa tải được thông báo." with "Thử lại"; any cached list stays with "Cập nhật lúc …".

**Responsive.** Full-width rows at every width; from `md` the column centers.

**Accessibility.** Day groups are `h2`; rows are a `ul` of links whose names start with "Chưa đọc" while unread. The unread count
change is announced once, in words ("2 thông báo chưa đọc"). "Đánh dấu tất cả đã đọc" announces its result.

**Data.** Today only the live `ChatEvent` stream; no list, no read state. Gap: a notifications endpoint with kind, case link,
anchor and read state (D-14).

### C5. Xe của tôi (Vehicle and service context)

**Purpose.** The context the AI works from: the vehicle, its service record, and what the assistant knows and may do.

**Hierarchy:**
1. AppHeader.
2. `h1` "Xe của tôi"; a SegmentedControl to switch vehicles, only when there is more than one.
3. The vehicle: model ("VF 8"), plate (D-14), short VIN in `--font-mono` ("…4821"), odometer with its data time ("38.420 km, theo
   dữ liệu xe lúc 08:15"), software version, and the customer's role ("Chủ xe" or "Người lái").
4. `h2` "Đang cần chú ý": active warnings in plain words, each linking to its case; or "Xe không có cảnh báo nào đang mở."
5. `h2` "Lịch hẹn": upcoming appointments as receipts with "Đổi lịch" and "Huỷ lịch".
6. `h2` "Bảo hành": the precheck, neutral, with its reason and source: "Đủ điều kiện sơ bộ theo chính sách bảo hành bản 2026.03.
   Xưởng xác nhận khi kiểm tra." (MASTER §11 mappings for the other results).
7. `h2` "Lịch sử bảo dưỡng": newest first, three shown, then "Xem tất cả".
8. `h2` "Trợ lý AI dùng thông tin gì": the data-sharing consent with a switch and what the data is used for; MemoryList ("xưởng quen",
   "khung giờ hay chọn", "cách xưng hô") with "Sửa" and "Xoá"; the line "Bên em không lưu giấy tờ định danh, vị trí chi tiết hay suy
   đoán về đời tư." (proposal §06 H).
9. `h2` "Trợ lý AI được làm gì": ActionScope in full.
10. "Cài đặt thông báo" (C8).
11. BottomNav.

**Primary action.** None by default; this is a reference screen. When an active warning's case waits on the customer: "Xem việc cần làm".

**Secondary actions.** "Đổi lịch", "Huỷ lịch", "Sửa" and "Xoá" on memory items, the data-sharing switch, "Cài đặt thông báo".

**System states.**

| Condition | Shows |
|---|---|
| Driver | "Anh/chị là người lái xe này. Chủ xe chưa cấp quyền đặt lịch."; no costs or invoices; service history as far as rights allow |
| Data sharing off | "Anh/chị đã tắt chia sẻ dữ liệu xe. Bên em sẽ không thể phát hiện sớm cảnh báo của xe." Turning it off states this before the switch moves |
| Warranty results | `ELIGIBLE_PRELIM` "Đủ điều kiện sơ bộ"; `NEEDS_WORKSHOP` "Cần xưởng xác nhận" with the reason ("lỡ kỳ bảo dưỡng"); `EXPIRED` "Hết hạn theo chính sách"; `UNKNOWN` "Chưa đủ dữ liệu: thiếu …". All neutral, never green or red |
| Safety | C7 |

**Empty.** No vehicle: "Tài khoản chưa có xe nào. Khi xe được gắn với tài khoản, thông tin xe sẽ hiện ở đây." with "Gặp nhân viên".
No memory: "Bên em chưa ghi nhớ điều gì về anh/chị." No history: "Chưa có lần bảo dưỡng nào được ghi nhận."

**Loading.** Each section loads and fails on its own, with a skeleton in its shape; one slow source never blanks the screen.

**Error.** Per section: "Chưa tải được lịch sử bảo dưỡng." with "Thử lại".

**Responsive.** One column; label and value lists stack the label above the value on phones (C-04).

**Accessibility.** Sections are `h2`; facts are `dl`; the switch has a label and a description linked to it; "Xoá" confirms in a
Dialog that names the item ("Xoá ghi nhớ: xưởng quen Long Biên?") and returns focus to the list.

**Data.** No vehicle, warranty, maintenance, consent or memory endpoint in the contract; all exist in the fixtures. Gap (D-14).

### C6. Trợ lý AI (conversation)

**Purpose.** Ask in one's own words, about a case or anything else. This is spec §20's "Chat khách".

**Hierarchy:**
1. AppHeader: back link, title "Trợ lý AI", "Gặp nhân viên".
2. When opened from a case, a context line: "Đang hỏi về: hệ thống làm mát pin, VF 8", with "Hỏi việc khác" to clear it.
3. The thread: the AI's introduction first ("Em là trợ lý AI của {tên sản phẩm}…"), then messages oldest to newest. AI messages
   carry AIByline; staff messages StaffByline; proactive messages appear as the CareCard message variant.
4. The composer, sticky at the bottom: a labelled text field and "Gửi tin nhắn".

**Primary action.** "Gửi tin nhắn". When a DecisionBlock is the newest message, its own primary is inline in the thread.

**Secondary actions.** Options inside messages; "Xem chi tiết việc"; "Gặp nhân viên".

**System states.** INVESTIGATING is live here for questions the customer asked: each finished check appears as it completes, elapsed
time in text after 2 seconds without news, never typing dots. Streaming replies show a text-shaped skeleton before the first words.
A handoff introduces the staff member in the thread ("Em là Hải, cố vấn dịch vụ xưởng Long Biên."). "Em chưa có thông tin chính xác
về việc này." always comes with an offer of a person. New messages follow C-05.

**Empty.** First visit: the introduction and one sentence, "Anh/chị có thể hỏi về xe, lịch hẹn, bảo hành hoặc trạm sạc."

**Loading.** A thread skeleton; the composer is usable at once, and messages wait until the connection is up.

**Error.** Sending offline: the message stays in the thread marked "Chưa gửi. Tin sẽ tự gửi khi có mạng." (sent once, with an
idempotency key, spec §21). Reply failure: "Em chưa trả lời được vì hệ thống đang gián đoạn." with "Thử lại" and "Gặp nhân viên".

**Responsive.** The composer stays above the on-screen keyboard; from `md` the thread sits in the `--w-customer` column.

**Accessibility.** The thread is a `log` whose additions are announced once complete, never word by word; every message names its
sender; the composer field is labelled "Tin nhắn cho Trợ lý AI"; scroll padding keeps the focused message clear of the composer.

**Data.** `POST /api/v1/chat/stream`, `GET /api/v1/stream/{customer_id}`, `POST /api/v1/confirm`.

### C7. Cảnh báo an toàn (safety state)

**Purpose.** Safety overrides everything, on every screen.

**Hierarchy:**
1. The safety Banner first in reading order, under the header: `--danger`, `siren` icon, the pre-approved message, "Gọi cứu hộ 24/7".
2. On C1, a safety card replaces the status sentence: the template's title and instructions, "Gọi cứu hộ 24/7", and the staff
   member's name and role once assigned.
3. On C2, the case shows the template text, the staff byline and the timeline link; no recommendation, options, evidence or diagnosis.
4. "Gặp nhân viên" stays in the header.

**Primary action.** "Gọi cứu hộ 24/7", a `tel:` link held in the app shell so it works offline.

**Secondary actions.** "Gặp nhân viên"; "Xem chi tiết" (C2).

**System states.** Unassigned: the template only. Assigned: "{tên}, tổng đài 24/7, đang xử lý." Closed by staff: the banner goes; the
case stays in C3. Drivers receive it as owners do (proposal §06 D2).

**Empty.** Not applicable.

**Loading.** The banner renders from the pushed event alone, without waiting for any other data.

**Error.** If the live connection is down, the connection banner says so and "Gọi cứu hộ 24/7" still works from the shell; external
channels deliver the alert independently (J5).

**Responsive.** The banner text wraps; the button is full width on phones.

**Accessibility.** `role="alert"` once; focus is not moved; no motion; the text is the template, never AI-generated.

**Data.** Pushed through `/stream/{customer_id}`. Gap: no safety flag on `ChatEvent` (D-06).

### C8. Cài đặt thông báo (notification and AI settings)

**Purpose.** Let the customer decide how the system contacts them: the right to refuse (proposal §09).

**Hierarchy:**
1. AppHeader: back link, "Gặp nhân viên".
2. `h1` "Cài đặt thông báo".
3. "Nhận tin chủ động do Trợ lý AI soạn": switch, with "Cảnh báo an toàn và cập nhật về việc anh/chị đang làm vẫn được gửi."
4. "Luôn làm việc với nhân viên": switch, with "Mọi đề xuất sẽ do nhân viên gửi cho anh/chị."
5. "Kênh nhận tin": SegmentedControl "Ứng dụng", "Zalo", "Gọi điện".
6. "Giờ nhận tin": read-only, "08:00 đến 20:00. Cảnh báo an toàn được gửi bất cứ lúc nào."
7. "Giao diện": ThemeSwitch "Sáng", "Tối", "Theo máy" (below `md`, C-06).
8. "Trợ lý AI ghi nhớ gì" (to C5).

**Primary action.** None. Each control saves on change and shows its own result.

**Secondary actions.** Each control; the link to C5.

**System states.** Saving: "Đang lưu…" beside the control. Saved: "Đã lưu lúc 09:12". Failed: the control returns to its previous
value with "Chưa lưu được." and "Thử lại". A driver controls only their own preferences.

**Empty.** Not applicable.

**Loading.** Skeleton controls; switches are not operable until their real value is known.

**Error.** "Chưa tải được cài đặt." with "Thử lại".

**Responsive.** One column at every width.

**Accessibility.** Switches are labelled with their visible text and described by their note; results are announced politely; no
Dialog for reversible choices, because the consequence is stated before the change.

**Data.** Not in the contract or the spec (D-12).

## 5. States shared by every screen

| State | Treatment |
|---|---|
| Reconnecting, offline | MASTER §11 banner; cached content with "Cập nhật lúc …"; confirmations and saves are replaced by "Cần có mạng để xác nhận"; chat messages queue |
| Session expired | "Phiên đăng nhập đã hết hạn. Anh/chị đăng nhập lại để tiếp tục." The screen keeps what it showed; nothing is lost |
| No permission (driver) | Said in words where the action would be; actions are never silently hidden |
| Safety | C7 on every screen |
| Opted out | C1 and C4 show one line with "Bật lại" |
| Demo mode | In the Demo stage phone frame: the "Chế độ demo" banner and "Dữ liệu mẫu" |

## 6. Responsive summary

| Width | Navigation | Primary action | Layout |
|---|---|---|---|
| 320px | BottomNav, three items on one line | Sticky bar on C2 decision states | One column; header holds the back link or name plus "Gặp nhân viên" |
| 390px (design width) | As 320 | As 320 | The head of C2 ends above the action bar |
| 768px and up (`md`) | Text links in the header; no BottomNav | Inline | One centered column at `--w-customer` |
| Short viewport (under 600px tall), large text, 200% zoom | As the width | The bar stops being sticky (C-03) | Labels wrap; nothing truncates |

## 7. Summary

**Proposed information architecture.** Home-first: "Việc của tôi" (C1) is the hub, Notifications (C4) the record, Vehicle (C5) the
context, with the case (C2) and its timeline (C3) one step down and the conversation (C6) reached from where the question arises.

**The pattern that carries the experience.** The proactive care card (§3): a head that answers the four questions in the same words on
every screen, with "Việc của anh/chị" that is never empty, and a body in the brief's order where each trust question is answered in
place: evidence under "Em đã kiểm tra", unknowns under "Em đề xuất", consent under "Việc anh/chị cần làm", people under "Ai đang phụ trách".

**Open questions.**

| ID | Question | Related |
|---|---|---|
| CQ-1 | Offer "Không cần lúc này"? If so, what ends the case and when may the topic come back? | D-03 |
| CQ-2 | Confirm the home-first IA and update spec §20, §21 and task cards C1.03, C1.04, C2.03 | D-13 |
| CQ-3 | Contract for notifications, vehicle context, consent and memory, unknowns, excluded options, cause lines and the hold deadline | D-14 |
| CQ-4 | May a level-2 action be confirmed both in C6 and in C2? Proposed: yes, one token, one shared DecisionBlock state | |
| CQ-5 | Wording of AI labels in push and Zalo previews, for legal review under the AI Law | |
| CQ-6 | No preselected option when there are several (proposed), or preselect the AI's first choice | |
| CQ-7 | How long resolved cases stay under "Đã xong gần đây". Proposed: the two most recent, no time limit | |
| CQ-8 | Cases started by staff, not the AI: same card with a StaffByline (proposed)? | |
| CQ-9 | Who owns the 24/7 rescue number held in the app shell, and how it is updated | |
| CQ-10 | Product name for the header and the AI's introduction | D-07 |
