# Content and copy

Part of the Proactive Care Design System v1.0. Start at [MASTER.md](MASTER.md). Canonical state copy is in MASTER §12; this file
holds the rules for writing everything else. All strings live in `frontend/src/i18n/vi.ts` (rules/frontend/AGENTS.md).

## 1. Who speaks, and how

| Speaker | Refers to self as | Addresses the customer as | Example |
|---|---|---|---|
| Trợ lý AI | "em" | "anh/chị", or the stored preference ("anh Minh") | "Em đã kiểm tra lịch sử bảo dưỡng của xe." |
| The company (notifications, promises) | "bên em" | "anh/chị" | "Bên em sẽ nhắc anh/chị trước 10 ngày." |
| A staff member in chat | "em" plus name and role on first message | "anh/chị" | "Em là Hải, cố vấn dịch vụ xưởng Long Biên." |
| Interface chrome (labels, buttons, headings) | no pronoun | no pronoun | "Xác nhận đặt lịch", "Gặp nhân viên" |
| CSKH console | no pronoun, terse; "bạn" only to say who owns or must act ("Của bạn", "Chờ bạn: …") | n/a | "Chờ khách xác nhận (mức 2). Đã gửi 14:02." |
| Landing | descriptive, third person: "hệ thống", "trợ lý AI", "nhân viên CSKH" | the reader is addressed only in calls to action | "Hệ thống nhận ra trục trặc trước khi khách phải gọi." |

The address form is a variable in `vi.ts`, defaulting to "anh/chị", filled from the customer's stored preference when one exists
(proposal §06, memory). The voice is "anh/chị, bên em" (proposal §09).

## 2. Mandatory labels

| Label | Where | Source |
|---|---|---|
| "Trợ lý AI" | On every AI-written message and AI-produced block (AIByline) | Vietnam AI Law (in force 2026-03-01), proposal §09 |
| "Tin tự động" | On every proactive message | Proposal §09 |
| "Em là trợ lý AI của {tên sản phẩm}…" | First AI message of every conversation | Proposal §09, system prompt rule |
| "Vì sao anh/chị nhận tin này" | On every proactive message, always visible | Proposal §09, spec §13 rule 7 |
| "Gặp nhân viên" | On every customer screen and every proactive message, same position | Proposal §09 "không ngõ cụt", WCAG 3.2.6 |
| "Dữ liệu mẫu" | On any fixture or mock data shown: Landing figures, Demo stage, mocks | Taste-rules rule 12 |

When a customer asks whether they are talking to a person, the AI answers plainly that it is AI and offers a staff member.

## 3. The proactive message

Every proactive message has the five parts required by spec §13 rule 7, in the CareCard order (components.md §6). The questions
from the owner briefs map onto them:

| Customer question (brief) | CareCard part | Example |
|---|---|---|
| What did the AI detect? | Chuyện gì đã xảy ra | "Xe của anh/chị gửi cảnh báo hệ thống làm mát pin 3 lần trong 14 ngày qua." |
| Why am I getting this? | Vì sao anh/chị nhận tin này | "Vì sao anh/chị nhận tin này: cảnh báo lặp lại và xe chưa có lịch kiểm tra." |
| What was checked? | Em đã kiểm tra (evidence) | "Em đã kiểm tra 4 nguồn: dữ liệu xe, lịch sử bảo dưỡng, phiên bản phần mềm, chính sách bảo hành." |
| What do you recommend? | Đề xuất | "Em đề xuất kiểm tra hệ thống làm mát pin tại xưởng. Bảo hành: đủ điều kiện sơ bộ, xưởng sẽ xác nhận khi kiểm tra." |
| What do I need to do? | Việc anh/chị cần làm (with deadline) | "Chọn một lịch và bấm Xác nhận. Lịch được giữ đến 18:00 hôm nay." |
| (customer brief) What is the AI doing? | Bên em đang làm (with the StateChip) | "Em đã tìm 2 lịch còn linh kiện, giữ chỗ đến 18:00 hôm nay." |
| Was it resolved? | State updates on the same card | "Đã xử lý xong. Xe không báo lại lỗi trong 7 ngày theo dõi." |
| (spec) Who is responsible? | Phụ trách | "Phụ trách: Trợ lý AI. Cố vấn dịch vụ Hải theo dõi lịch này." |

**The four questions.** On Customer, the head of every CareCard answers four questions in this order and in the same words on every
screen: what was detected, why the customer is receiving this, what the AI is doing, what the customer needs to do
([customer-journey.md](../../docs/frontend/customer-journey.md) §1). The last answer is never empty; when nothing is needed it says
"Anh/chị chưa cần làm gì."

## 4. Words

| Write | Do not write | Why |
|---|---|---|
| "đủ điều kiện sơ bộ theo chính sách" plus the reason | "được bảo hành", "chắc chắn được bảo hành", "mất bảo hành" | Only the workshop concludes (taste-rules rule 12, proposal §06) |
| "xưởng sẽ kiểm tra và kết luận" | Any diagnosis ("xe bị hỏng bơm làm mát") | The AI does not diagnose |
| "Em chưa có thông tin chính xác về việc này." | A guess | No fabrication |
| "chi phí theo báo giá của xưởng" | A price the API did not return | Prices only from the API |
| "Đã đặt lịch" (after the server confirms) | "Đã đặt" while executing | 21-fe: never success before confirmation |
| "Đang theo dõi kết quả", then "Đã xử lý xong" | "Đã xong" before verification | Done means verified |
| A specific verb and object: "Xác nhận đặt lịch", "Đổi lịch", "Gọi cố vấn dịch vụ" | "OK", "Gửi", "Tiếp tục", "Đồng ý" as a primary label | Taste-rules rule 8 |
| Plain phrases to customers: "cảnh báo lặp lại", "kiểm tra", "tiến trình xử lý" | "candidate", "arbitration", "L0", "agent", "token", "trace", "journey" | Internal terms stay internal (Landing L-06 and CSKH K-06 are the bounded exceptions) |
| Concrete verbs | "đột phá", "liền mạch", "tối ưu trải nghiệm", "thông minh vượt trội", "cách mạng hoá", "giải pháp toàn diện", "nâng tầm" | Filler (taste-skill §9.D) |
| One specific apology when the company caused the problem: "Bên em xin lỗi vì lịch phải đổi do linh kiện chưa về kịp." | Repeated or vague apologies; blaming the customer | Proposal §09 |
| Realistic Vietnamese names from the fixtures | "Nguyễn Văn A", "John Doe" | Taste-skill §9.D |

## 5. Patterns

**State sentence.** State, then evidence, then next step or time: "Đang theo dõi kết quả: 3 trên 7 ngày, xe chưa báo lại lỗi."

**Error.** What happened, what is true now, what to do: "Chưa gửi được tin vì mạng đang yếu. Tin sẽ tự gửi lại khi có kết nối." plus
"Thử lại". Never "Oops", never a bare code, never a long apology (taste-rules rule 6).

**Empty.** What will appear here and how it gets here:
- Việc của tôi: "Chưa có việc nào. Khi anh/chị đặt lịch hoặc bên em phát hiện điều cần xử lý, tiến độ sẽ hiện ở đây."
- CSKH queue: "Không có ca nào cần xử lý. Ca mới sẽ hiện ở đây kèm hạn gọi lại."

**Change.** Every change says what changed, why and when, as one line: "Thay đổi gần nhất (14:18, thứ Tư 30/09): đổi sang xưởng Gia Lâm vì
linh kiện ở Long Biên được điều đi." (proposal §08: "nói thật khi thay đổi").

**Uncertainty.** Say what is missing, not that something is impossible: "Em chưa đủ dữ liệu để kiểm tra bảo hành: thiếu ngày mua xe."

## 6. Register per surface

| Surface | Register | Length rules |
|---|---|---|
| Landing | Plain editorial, one register throughout (taste-skill §4.9) | Opening headline at most 2 lines at desktop, subtext at most 3 lines; one idea per section; no invented figures |
| Customer | Warm and short; one idea per sentence; active voice; absolute times | A message body fits a 390px screen without scrolling before the first action |
| CSKH | Terse and scannable; noun phrases allowed; system terms allowed with a glossary tooltip (K-06) | Summaries are one line; detail lives in sections |

## 7. Self-audit before shipping copy

Adapted from taste-skill §4.9 and the team rules. Re-read every visible string and fix any that:

- [ ] is not grammatical Vietnamese, or has an unclear referent
- [ ] contains a number, date, price or policy not returned by a tool (or not labelled "Dữ liệu mẫu")
- [ ] contains an em or en dash, straight quotes, or three dots instead of "…"
- [ ] uses a generic label ("OK", "Gửi") for a primary action
- [ ] shows an internal system term to a customer
- [ ] claims success, warranty or a diagnosis that the system cannot stand behind
- [ ] is missing a mandatory label from §2
