# Customer journey

How a customer lives through one case, from the first signal to a verified result. Screens are specified in
[customer-screen-spec.md](customer-screen-spec.md); motion in [customer-motion-map.md](customer-motion-map.md). Built on
[MASTER](../../design-system/proactive-care/MASTER.md) §12 (the nine states) and the Customer deviations in
[pages/customer.md](../../design-system/proactive-care/pages/customer.md). Cross-surface journeys, with the CSKH side at every
step, are in [journeys.md](journeys.md); this document is the customer side in depth. No code; nothing here changes P-073.

**Status.** Part of design contract v1.0 (MASTER §18), 2026-10-03. Several things the journey needs are not in the contract yet (D-04, D-06, D-14). Where data is
missing the interface shows less; it never guesses.

**Sample data.** People, vehicles, codes and workshops come from `P-073/contracts/fixtures/demo_world.yaml` and
[journeys.md](journeys.md). Times that neither source gives are illustrative. All of it is "Dữ liệu mẫu".

---

## 1. The four questions

Whenever a customer looks at a case, the screen answers four questions, in this order, before any scrolling at 390 by 844:

| # | Question (owner brief) | Answered by | Example: UC1, waiting for the customer |
|---|---|---|---|
| 1 | What did the AI detect? | The case title, plus the "Phát hiện" line on the case screen | "Hệ thống làm mát pin báo lỗi lặp lại." / "Xe gửi cảnh báo hệ thống làm mát pin 3 lần trong 14 ngày." |
| 2 | Why am I receiving this? | "Vì sao anh/chị nhận tin này" | "Cảnh báo lặp lại và xe chưa có lịch kiểm tra." |
| 3 | What is the AI doing? | StateChip plus "Bên em đang làm" | "Chờ anh/chị xác nhận" and "Em đã tìm 2 lịch còn linh kiện, giữ chỗ đến 18:00 hôm nay." |
| 4 | What do I need to do? | "Việc của anh/chị" | "Chọn một lịch và xác nhận trước 18:00 hôm nay." |

Rules:

- **One wording everywhere.** These four lines are the head of the proactive care card ([customer-screen-spec.md](customer-screen-spec.md) §3).
  Home, the case screen and the conversation use the same words; Notifications shows the first two.
- **Line 4 is never empty.** When nothing is needed it says so: "Anh/chị chưa cần làm gì." Knowing that nothing is needed is an
  answer, and the most common one.
- **Line 2 for a case the customer started** reads "Bắt đầu từ tin nhắn của anh/chị lúc 09:12" instead of the proactive label.
- **Plain words only.** No line names a code, a layer, a model or an internal term (content.md §4).

## 2. The journey model

The owner brief's timeline has seven phases. Each phase is one of the nine states of MASTER §12; the customer never sees the
state names, only the Customer labels (current) and the completed forms of MASTER §12.4 (history).

| Phase | State (MASTER §12) | Ball with | Customer sees it live? | Node | Completed, in the timeline | Customer is notified? |
|---|---|---|---|---|---|---|
| Signal detected | DETECTED | System | No for proactive cases: history only | circle | "Phát hiện cảnh báo lặp lại" | No |
| AI investigated | INVESTIGATING | AI | No for proactive cases; yes in a conversation the customer started | circle | "Trợ lý AI đã kiểm tra 4 nguồn" | No |
| Recommendation | RECOMMENDING | AI | Yes. The first moment a proactive case becomes visible | circle | "Đã đề xuất kiểm tra tại xưởng" | Yes: the proactive message |
| Customer confirmation | WAITING FOR CUSTOMER (level 2); WAITING FOR HUMAN in its place for level 3 | Customer (or staff) | Yes | diamond | "Anh/chị đã xác nhận lịch" | Only reminders within the contact rules (§7) |
| Action | EXECUTING | System | Yes | circle | Names the action: "Đã đặt lịch" | Receipt, when the customer is not on screen |
| Verification | VERIFYING, guard phase then window phase | System | Yes | circle | "Đã theo dõi đủ 7 ngày" | Visit reminder (only if promised); window start in Notifications only |
| Resolved | RESOLVED | Done | Yes | filled circle with check | "Đã xử lý xong" | Yes, once |

Anywhere along the line:

| Interruption | State or event | Node | Example |
|---|---|---|---|
| A person takes over | ESCALATED | square, with name and role | "Anh Hải, cố vấn dịch vụ xưởng Long Biên, đang trực tiếp xử lý." |
| Something failed | Event | triangle | "Linh kiện giữ cho anh/chị ở Long Biên được điều đi." |
| A parameter changed and needs a new confirmation | Event, then WAITING FOR CUSTOMER again | amber diamond | "Lịch phải đổi." |
| Something happened in a system of record | Event, neutral | small circle | "Xưởng Gia Lâm báo đã sửa xong." |

**Two axes, kept apart.** The phases are the AI-state axis (who holds the case). The service job has its own steps (Đặt lịch, Giữ
linh kiện, Chờ hẹn, Chẩn đoán, Sửa, Xác minh), shown by the JourneyStepper in "Tiến độ sửa chữa" on the case screen. Job milestones
enter the timeline only as neutral events from the system of record, never as phases.

**Phase names stay in documents.** The interface does not show "Signal detected" or "Phase 4". It shows the current state label,
the completed forms for history, and concrete expectations for the future ("Tiếp theo: đặt lịch tại xưởng anh/chị chọn").

## 3. Causality: how each step says why

The timeline ([customer-screen-spec.md](customer-screen-spec.md) C3) makes causality readable by giving every item the same five parts:

| Part | Rule | Example |
|---|---|---|
| Label | Completed form (MASTER §12.4), naming the outcome | "Đã đề xuất lịch mới" |
| Actor | In words: "Hệ thống (tự động)", "Trợ lý AI", "Anh/chị", "Anh Hải, cố vấn dịch vụ", "Xưởng Gia Lâm", "Kho linh kiện" | "Trợ lý AI" |
| Time | Absolute, under the label | "13:58, thứ Tư 30/09" |
| What happened | One sentence | "Còn 2 lịch có linh kiện: Hoài Đức 09:00 thứ Năm 01/10 và Gia Lâm 09:00 thứ Bảy 03/10." |
| Cause | One clause beginning "Vì", "Dựa trên", "Theo" or "Sau khi", pointing at the item before it or an outside event | "Vì lịch cũ không còn linh kiện." |

Cause line rules:

1. It points at something the customer can see: an earlier item on the same timeline, the evidence, or their own action. Never at
   internal reasoning.
2. It is built from structured data: the event type, the decision log's reasons, `Option.why`. It is not generated prose (D-14).
3. When the cause is the customer's own choice, it says so: "Theo lựa chọn của anh/chị."
4. When the company caused the problem, it says so plainly, once, with one apology on the case (content.md §4): "Vì linh kiện ở
   Long Biên được điều đi cho xe thuộc diện triệu hồi."
5. When the cause is not known yet, the item has no cause line. It never says "do hệ thống" or similar filler.

### 3.1 Worked example: UC1 with the replan (J1 and J2), as the customer sees it on 10/10

| Time | Node | Label | Actor | What happened | Cause |
|---|---|---|---|---|---|
| 08:15, thứ Ba 29/09 | circle | Phát hiện cảnh báo lặp lại | Hệ thống (tự động) | Xe gửi cảnh báo hệ thống làm mát pin lần thứ 3 trong 14 ngày. | Theo dữ liệu xe gửi về |
| 08:16 | circle | Trợ lý AI đã kiểm tra 4 nguồn | Trợ lý AI | Dữ liệu xe, lịch sử bảo dưỡng, phiên bản phần mềm, chính sách bảo hành. | Dựa trên cảnh báo vừa phát hiện |
| 08:16 | circle | Đã đề xuất kiểm tra tại xưởng | Trợ lý AI | Lỗi không sửa từ xa được; có lịch còn linh kiện. | Vì cảnh báo lặp lại và chưa có lịch kiểm tra |
| 08:41 | diamond | Anh/chị đã xác nhận lịch | Anh/chị | Xưởng Long Biên, 14:00 thứ Sáu 02/10. | Theo lựa chọn của anh/chị |
| 08:41 | circle | Đã đặt lịch | Hệ thống (tự động) | Xưởng Long Biên xác nhận lịch hẹn A-20931; linh kiện được giữ. | Sau khi anh/chị xác nhận |
| 08:41 | circle | Bắt đầu theo dõi lịch hẹn | Hệ thống (tự động) | Theo dõi để lịch hẹn và linh kiện luôn sẵn sàng đến ngày hẹn. | Sau khi đặt lịch |
| 13:55, thứ Tư 30/09 | triangle | Linh kiện bị điều đi | Kho linh kiện | Linh kiện giữ cho anh/chị ở Long Biên được điều đi cho xe thuộc diện triệu hồi. | Phát hiện khi đang theo dõi lịch hẹn |
| 13:58 | circle | Đã đề xuất lịch mới | Trợ lý AI | Còn 2 lịch có linh kiện: Hoài Đức 09:00 thứ Năm 01/10 và Gia Lâm 09:00 thứ Bảy 03/10. Long Biên không còn linh kiện. | Vì lịch cũ không còn linh kiện |
| 14:06 | diamond | Anh/chị chọn gặp nhân viên | Anh/chị | | Theo yêu cầu của anh/chị |
| 14:06 | square | Nhân viên tiếp nhận | Anh Hải, cố vấn dịch vụ xưởng Long Biên | Hẹn gọi lại trước 14:21. | Vì anh/chị muốn trao đổi với người |
| 14:18 | square | Anh Hải đã chốt lịch mới | Anh Hải | Gia Lâm, 09:00 thứ Bảy 03/10. Anh/chị đồng ý qua điện thoại. | Theo trao đổi với anh/chị |
| 14:18 | circle | Đã đổi lịch | Hệ thống (tự động) | Xưởng Gia Lâm xác nhận lịch hẹn; linh kiện được giữ. | Sau khi anh Hải chốt |
| Thứ Bảy 03/10 | small circle | Xưởng báo đã sửa xong | Xưởng Gia Lâm | | Theo lịch hẹn 09:00 |
| Thứ Bảy 03/10 | circle | Bắt đầu theo dõi kết quả | Hệ thống (tự động) | Theo dõi 7 ngày xem xe có báo lại lỗi không. | Sau khi sửa xong |
| 09:00, thứ Bảy 10/10 | filled check | Đã xử lý xong | Hệ thống (tự động) | Xe không báo lại lỗi trong 7 ngày theo dõi. | Dựa trên dữ liệu xe 7 ngày qua |

Each "what happened" for the AI's own steps opens its evidence (sources and read times) behind a disclosure; nothing opens its reasoning.

## 4. Moment by moment: UC1

What the customer meets at each moment, on which screen, and what changes. Screen IDs are in [customer-screen-spec.md](customer-screen-spec.md) §1;
motion IDs in [customer-motion-map.md](customer-motion-map.md) §3.

| # | Moment | State | Notification | Home (C1) | Case (C2) | Customer does | Motion |
|---|---|---|---|---|---|---|---|
| 1 | 08:15 to 08:16, detection and checks | DETECTED, INVESTIGATING | None | Unchanged | Not reachable yet | Nothing; the phone stays quiet | None |
| 2 | 08:16, the message | WAITING FOR CUSTOMER | "Tin tự động" in the preferred channel and in C4 | A summary card under "Cần anh/chị": the four answers and "Xem và chọn lịch" | The full card | Opens the case | N1 or N4 |
| 3 | Reads and inspects | WAITING FOR CUSTOMER | | | Optionally opens "Em đã kiểm tra 4 nguồn", "Vì sao em đề xuất lịch này", "Điều em chưa biết" | Reads | F3 |
| 4 | Chooses Long Biên, 14:00 thứ Sáu 02/10 | WAITING FOR CUSTOMER | | | The parameters fill in: việc, xe, xưởng, ngày giờ, chi phí "theo báo giá của xưởng"; the action bar shows the choice | Selects an option | A1 |
| 5 | Confirms | EXECUTING | | | "Đang đặt lịch…" in the locked button | Taps "Xác nhận đặt lịch" | A2, A3, P2 |
| 6 | The workshop system confirms | VERIFYING (guard) | Receipt in C4 | The case moves to "Bên em đang xử lý" on the next visit | ConfirmationReceipt "Đã đặt lịch", "Đổi lịch", "Huỷ lịch"; "Việc của anh/chị: đưa xe tới xưởng Long Biên lúc 14:00 thứ Sáu 02/10." | Nothing more | A4 |
| 7 | 13:58 thứ Tư, parts reallocated (J2) | WAITING FOR CUSTOMER | "Lịch hẹn của anh/chị cần đổi" | Back under "Cần anh/chị" | Change line with one apology; new options; Long Biên listed as excluded with its reason | Reads; is annoyed | S5 |
| 8 | 14:06, asks for a person | ESCALATED | | "Anh Hải sẽ gọi trước 14:21" | "Việc của anh/chị: nghe máy khi anh Hải gọi, trước 14:21." The options stay visible, read-only, so both sides talk about the same choices | Taps "Gặp nhân viên" | S4 |
| 9 | 14:18, staff finalizes | VERIFYING (guard) | "Đã đổi lịch" | Under "Bên em đang xử lý" | Receipt for Gia Lâm; "Thay đổi gần nhất (14:18, thứ Tư 30/09): đổi sang xưởng Gia Lâm vì linh kiện ở Long Biên được điều đi. Anh/chị đồng ý qua điện thoại." | Nothing | S1, A4 |
| 10 | Thứ Bảy 03/10, repaired | VERIFYING (window) | "Bên em bắt đầu theo dõi kết quả" in C4 only | "Đang theo dõi kết quả: 0 trên 7 ngày" | VerificationMeter | Nothing | S1 |
| 11 | Day 3 of 7 | VERIFYING (window) | None | "3 trên 7 ngày" | One more segment | Nothing | V2 |
| 12 | 10/10, clean window | RESOLVED | "Đã xử lý xong" | Under "Đã xong gần đây" | "Đã xử lý xong. Xe không báo lại lỗi trong 7 ngày theo dõi." | Nothing | R1 or R2 |

The first contact happens at moment 2. Before that, the customer is not asked anything; that is the product's promise.

## 5. Other paths

What changes for the customer on the other journeys. Everything not listed follows §4.

| Path | Journey | What is different for the customer |
|---|---|---|
| Level-0 advice (UC2, charging) | J4 | No confirmation. "Việc của anh/chị: không bắt buộc. Nếu cần sạc ngay, trạm … còn trống." The result is checked on the next charging session: "Bên em sẽ kiểm tra lần sạc tiếp theo của xe." |
| Remote fix first (VF6-2290, 3% charge) | J7 | Workshops listed as excluded: "Loại: pin không đủ đi tới xưởng này." The DecisionBlock carries the condition "xe đang đỗ". Warranty shown neutrally: "Cần xưởng xác nhận" with the reason. Window 14 days |
| Level 3, a person decides | J3 | "Bên em đang làm: phương án này cần nhân viên duyệt. Bên em sẽ báo lại trước 16:00." "Việc của anh/chị: chưa cần làm gì." The outcome is never promised before approval |
| Execution failed | MASTER §12 | "Chưa đặt được lịch vì hệ thống xưởng chưa phản hồi. Em đang kiểm tra lại, anh/chị chưa cần làm gì." After the limited retries the case goes to a named person |
| Confirmation expired | MASTER §10 | "Phương án đã hết hạn giữ chỗ lúc 18:00." Primary "Tạo lại phương án". How the case ends if nothing follows is open (D-03) |
| Customer says no ("Không cần lúc này") | Proposed | Shown only once D-03 decides the ending and the product sets when the topic may be raised again (CQ-1) |
| Driver without booking rights (Trần Thu Hà, VF9-3055) | J1 alternate | Safety and charging messages arrive as for an owner. For a booking: "Chỉ chủ xe xác nhận được lịch hẹn cho xe này. Bên em đã gửi đề xuất cho chủ xe." No DecisionBlock, no prices, no invoices (proposal §06 D2) |
| Safety (`HV-ISO-99`) | J5 | Screen state C7 over everything: the pre-approved message, "Gọi cứu hộ 24/7", no AI text, no options, no evidence, no motion. The staff member's name and role appear once assigned |
| Recurrence during the window (UC6) | J6 | A triangle on the timeline: "Cảnh báo quay lại sau 4 ngày. Bên em đã mở lại việc và ưu tiên kiểm tra." A new card that names the first repair. After two automatic cycles a person owns the case |
| The customer started it (conversation) | | INVESTIGATING is visible live in C6: each finished check appears as it completes. Line 2 reads "Bắt đầu từ tin nhắn của anh/chị lúc …" |
| Opted out of AI-written proactive messages | Proposal §09 | No proactive cards from the AI. Safety alerts and updates on cases already open still arrive; anything staff start carries their StaffByline |

## 6. Trust: what the customer can inspect

The customer can check the system's work without reading its reasoning. Each kind of inspection sits where the question arises.

| The customer can see | Where | Shown as | Built from |
|---|---|---|---|
| What the AI knows about this case | C2 "Em đã kiểm tra N nguồn" | EvidenceList: the fact in plain words, the source name, the time it was read | `HandoffCard.facts`, `ChatEvent.citations` mapped to source names; read times are a gap (D-14) |
| What the AI knows about me | C5 "Trợ lý AI dùng thông tin gì" | Data sharing consent; MemoryList with "Sửa" and "Xoá"; what is never stored | Proposal §06 H; no endpoint yet (D-14) |
| What it checked, step by step | C3, each AI step | The step's evidence behind a disclosure | As above |
| Why this recommendation | C2 "Vì sao em đề xuất lịch này" | The reasons as short facts ("còn linh kiện", "có khoang pin cao áp", "pin đủ đi tới", "7,1 km"), then the options not chosen with their reason | `Option.why`; excluded options are a gap (D-14) |
| What it does not know | C2 "Điều em chưa biết" | Each open question with who will answer it: "Nguyên nhân chính xác: xưởng kết luận khi kiểm tra." "Chi phí: theo báo giá của xưởng." "Bảo hành chính thức: xưởng xác nhận." | Fixed per intervention type in `vi.ts` until a contract field exists (D-14) |
| What requires confirmation | C2 "Sau khi anh/chị xác nhận"; C5 "Trợ lý AI được làm gì" | ActionScope: what the AI does alone, what needs the customer, what needs staff | Confirmation levels, proposal §06 C |
| When a human is involved | C2 "Ai đang phụ trách"; C3 square nodes; StaffByline on messages | Name, role, what they promised and by when | `Journey.owner`, `Journey.promises`, `Handoff.assignee` (display name is a gap, D-06) |

**Never shown to customers.** Reasoning steps, prompts, model or layer names, token counts, confidence scores or rankings, raw tool
inputs and outputs, raw source ids (`kb:…`), arbitration decisions, suppressed candidates, the staff's "Không nên" list, internal
notes, and the sentiment estimate. A decision summary is assembled from the decision log's structured reasons; it is not a
paraphrase of the model's reasoning, and it never says "em nghĩ rằng".

## 7. Notifications along the journey

Contact rules come from proposal §09 and apply before any notification is sent: at most 1 proactive message per job per day and
3 per customer per week (safety excepted); between 08:00 and 20:00 (outside only for safety or a stranded customer); never while
the customer is driving (non-urgent messages wait until the car is parked), while a staff member is talking with them, or while a
complaint is open.

| Moment | Kind label | In app | Preferred channel (app, Zalo, phone) | Text pattern |
|---|---|---|---|---|
| Proactive message | Tin tự động | C4 row; C1 card; in-app notice if the app is open | Yes | "{Phát hiện}. {Đề xuất}." "Xe của anh/chị báo lỗi làm mát pin lặp lại. Bên em đề xuất kiểm tra tại xưởng." |
| Reminder before a hold expires | Nhắc | C4 row | Only within the frequency rule | "Lịch được giữ đến 18:00 hôm nay." |
| Receipt | Cập nhật | C4 row | Only if the customer was not on screen | "Đã đặt lịch: xưởng Long Biên, 14:00 thứ Sáu 02/10." |
| Change needed | Tin tự động | C4 row; C1 card; in-app notice | Yes | "Lịch hẹn của anh/chị cần đổi vì linh kiện chưa sẵn sàng." |
| A person takes over | Cập nhật | C4 row; in-app notice | Yes | "Anh Hải, cố vấn dịch vụ, sẽ gọi anh/chị trước 14:21." |
| Visit reminder | Nhắc lịch | C4 row | Yes, only if a promise says so | From the `Promise` text, never composed on the fly |
| Verification starts | Cập nhật | C4 row only | No | "Bên em bắt đầu theo dõi kết quả trong 7 ngày." |
| Resolved | Cập nhật | C4 row; in-app notice | Yes | "Đã xử lý xong: xe không báo lại lỗi trong 7 ngày theo dõi." |
| Safety | An toàn | C7 banner; pinned in C4 | Every channel, any hour | The pre-approved template only |

Rules for anything shown outside the app (push preview, Zalo, lock screen):

- AI-written proactive messages begin with "Trợ lý AI · Tin tự động".
- The preview names the kind and the vehicle model only: no plate, VIN, location, price or staff phone number.
- No notification carries a confirm action. Level-2 actions are confirmed in the app, with every parameter visible.
- Every notification opens its case (C2) at the part it is about, through a deep link. A notification never opens a blank chat.

## 8. Done when

The customer, without help, can:

1. say what was detected and why they were contacted;
2. say what the system is doing now and whether they need to act;
3. confirm once, with every parameter visible, and see the server's receipt;
4. find who is responsible and what was promised;
5. see later that the result was verified by vehicle data, not only that a ticket closed.

Test with the five user sessions of task C2.12: a five-second look at C1 followed by questions 1 and 2, then the UC1 flow, with time
to confirm, abandonment and "Gặp nhân viên" taps recorded as the UX events of spec §21.
