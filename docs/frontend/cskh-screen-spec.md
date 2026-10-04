# CSKH screen specification

Every screen of the customer-service employee console: purpose, hierarchy, actions, states and behavior. The structure and the shared
models (action model, priority, evidence) are in [cskh-information-architecture.md](cskh-information-architecture.md); motion is in
[cskh-motion-map.md](cskh-motion-map.md). Built on [MASTER](../../design-system/proactive-care/MASTER.md) and the CSKH deviations in
[pages/cskh.md](../../design-system/proactive-care/pages/cskh.md). No code; nothing here changes P-073.

**Status.** Part of design contract v1.0 (MASTER §18), 2026-10-03. Screens K1, K3, K5 and most of K4 depend on data the contract lacks (D-05, D-06, D-16); each screen
lists what works with today's API.

**Audience and dials.** CSKH agents, service advisors, the 24/7 line and approvers, at desktop stations, many cases per shift.
VARIANCE 3, MOTION 2, DENSITY 8: compact density (K-01), data at `--text-sm` and narrative at `--text-md` (K-02), no cards (K-05),
real tables, everything expanded (K-10), targets still at least `--target-min`.

**Sample data.** All examples come from `P-073/contracts/fixtures/demo_world.yaml` and [journeys.md](journeys.md) (mostly J2, the
replan and handoff), and are "Dữ liệu mẫu". Times not given there are illustrative.

---

## 1. Shared frame

| Element | Rule |
|---|---|
| Skip link | "Bỏ qua tới nội dung chính", first focusable element |
| Header | One line, at most 72px: product name and "CSKH"; the five destinations (Tổng quan, Hàng ưu tiên, Ma sát, Khách hàng, Nhật ký) with `aria-current="page"`; customer search (label "Tìm khách", placeholder "Tên, SĐT, biển số hoặc VIN…", `type="search"`, spellcheck off); the alert slot; the account menu (name, role, skill group, theme switch per K-12, "Phím tắt", sign out) |
| Alert slot (K-11) | A fixed-width region in the header. Empty when all is well. Safety: `siren` icon and "An toàn: Nguyễn Văn Minh, VF8-4821, HV-ISO-99. Mở ca" in `--danger`. Reconnecting: "Đang kết nối lại…" in `--attn`. Offline: "Mất kết nối. Hành động tạm khoá." in `--danger`. With several alerts, safety wins and "+1" opens the list. Panes never shift because of an alert |
| Panes (workspace, K2 with K4) | 1280px and up: queue (`--pane-queue`), case (fluid, at least 520px), decision (`--pane-action`), hairline borders, each scrolling on its own; the page does not scroll. 1024 to 1279px: queue and case; the decision pane docks as a sticky bar at the bottom of the case and its briefing moves to the top of the case. Below 1024px: one pane at a time with "Về hàng ưu tiên" (K-08) |
| Full-width screens | K1, K3, K5, K6 use the page width up to `--w-page` in a strict 12-column grid; no offset compositions (K-04) |
| Live updates | Never move focus, never reorder rows under the pointer, never swap a button under the pointer (§7); one polite live region per screen, batched (accessibility.md §3) |
| Presence | Who else has a case open, as text ("Lan đang xem"); who is acting on it locks actions for others (§2, J) |
| Demo | In the Demo stage, the "Chế độ demo" banner and "Dữ liệu mẫu" (the only banner that pushes content, K-11 bounds) |

## 2. State inventory

Every state the console must render, and how. Screens refer to these tables instead of restating them.

### A. Case lifecycle (MASTER §12, CSKH labels)

| State | Chip | Where it lives in K2 | Case header "Tiếp theo" (example) | Current spine section | Decision pane primary |
|---|---|---|---|---|---|
| DETECTED | Phát hiện | "AI đang xử lý" | "AI đang xử lý: đã phát hiện, chưa liên hệ khách." | 2 | None ("Nhận xử lý" secondary) |
| INVESTIGATING | Đang điều tra | "AI đang xử lý" | "AI đang điều tra (L2): đã đọc 3 trên 5 nguồn." | 4 | None |
| RECOMMENDING | Đề xuất | "AI đang xử lý" | "AI đã đề xuất; đang kiểm tra trước khi gửi khách." | 5 | None |
| WAITING FOR CUSTOMER | Chờ khách xác nhận | "Chờ khách xác nhận" | "Chờ khách xác nhận (mức 2). Đã gửi 13:58; giữ chỗ đến 18:00." | 7 | None, or "Gọi khách" when the case is the employee's |
| WAITING FOR HUMAN | Cần duyệt | "Chờ duyệt" for approvers | "Chờ bạn duyệt (mức 3: bù đắp chi phí) trước 16:00." | 7 | "Duyệt" |
| EXECUTING | Đang thực hiện | Stays in its view; no loader in rows | "Đang thực hiện: đổi lịch, lần thử 1 trên 3." | 8 | Locked button with the loader |
| VERIFYING | Đang xác minh | "Đang xác minh" | Guard: "Đang giữ: linh kiện và lịch hẹn đến 03/10." Window: "Đang xác minh: ngày 3 trên 7, 0 lần tái phát." | 9 | None |
| RESOLVED | Đã xác minh | "Đã xong hôm nay" | "Đã xác minh: 0 lần tái phát trong 7 ngày. Đóng 10/10, 09:00." | 9 (check) | None ("Mở lại ca" secondary) |
| ESCALATED | Đã chuyển người | "Cần tôi xử lý" when unassigned in my skill, or mine | "Chờ bạn: nhận ca và gọi lại khách trước 14:21." | 7 | "Nhận", then "Gọi khách", then "Chốt phương án" |
| ESCALATED, safety | Đã chuyển người, with the "An toàn" marker | Pinned first in every view; alert slot | "An toàn: gọi khách ngay theo quy trình 24/7." | 7 | "Nhận", then "Gọi khách" |

### B. Authorization verdicts (per proposed action)

| Verdict | Label | Treatment |
|---|---|---|
| Level 0 or 1, validator passed | Được phép (mức 0) / Được phép (mức 1) | Neutral, `shield-check` |
| Level 2 | Cần khách xác nhận | Neutral, `user-round` |
| Level 3 | Cần nhân viên duyệt ({vai trò}) | Neutral, `stamp` |
| Blocked | Không được phép: {luật} | `--danger`, `circle-slash` |

### C. Events on the case (not states, MASTER §12.3)

| Event | Node | Example |
|---|---|---|
| Failure | triangle, `--danger` | "Đặt lịch thất bại: hệ thống xưởng không phản hồi (lần 1 trên 3)." |
| Parameter change needing re-confirmation | amber | "Đổi xưởng: Long Biên sang Gia Lâm; cần xác nhận lại." |
| Reminder sent | neutral | "Đã nhắc khách 16:00: giữ chỗ đến 18:00." |
| Suppressed candidate (arbitration) | neutral | "Không liên hệ: khách đang lái xe (08:02)." |
| Recurrence during verification | triangle | "Tái phát ngày 4 trên 7: BATT-COOL-01." |
| Customer reply | neutral | "Khách trả lời 14:06: muốn gặp nhân viên." |
| Call logged | square | "Hải gọi 14:12: khách đồng ý Gia Lâm, 09:00 03/10." |
| Internal note | neutral | "Hải: khách muốn được nhắc trước 1 ngày." |

### D. Assignment

"Chưa nhận" (in my skill group) · "Của bạn" · "Của {tên}" · "AI đang xử lý" · "Đã trả lại cho AI ({tên}, 14:20)" · "Cần người có quyền ({vai trò})".
Always words; the employee's own cases also carry the ink square node in the row.

### E. Callback deadline (K-09, MASTER §11)

| Condition | Text | Family |
|---|---|---|
| No deadline | Nothing | |
| Due | "Gọi lại trước 14:21, còn 14 phút" | Neutral |
| Within 5 minutes | "Gọi lại trước 14:21, còn 4 phút" | `--attn` |
| Overdue | "Quá hạn 3 phút (14:21)" | `--danger` |
| Met | "Đã gọi lúc 14:12" | Neutral |

### F. Validator check

"Đạt" (`--ok`) · "Không đạt: {luật}" (`--danger`) · "Chưa kiểm" (neutral). Checks: khách đã xác thực, chủ xe hoặc được quyền đặt lịch,
linh kiện khớp VIN, kỹ thuật viên đủ chứng chỉ, linh kiện đã giữ, slot đã khoá, xác nhận còn hiệu lực (components.md §4).

### G. Verification

Guard holding ("Linh kiện đang giữ", "Lịch hẹn còn hiệu lực") · guard broken (an event, then the case returns to replanning) ·
window "ngày n trên N" with the reason for N ("7 ngày: lỗi liên tục") · recurrence (event; cycle 2 opens a linked case; after two
automatic cycles a person owns it) · passed (RESOLVED).

### H. Customer flags (case header and K5)

"Đã tắt tin chủ động do AI soạn" · "Muốn làm việc với nhân viên" · "Người lái, không có quyền đặt lịch" · "Đang khiếu nại: không
liên hệ chủ động" · "Kênh ưa thích: Zalo" · sentiment "Bình tĩnh", "Lo lắng", "Bực", "Rất bực" with the tooltip "ước tính của mô hình".

### I. Presence and conflict

| Condition | Treatment |
|---|---|
| A colleague has the case open | "Lan đang xem" in the header and the row; nothing locked |
| A colleague is acting (accepted, in a call, finalizing) | Actions disabled with "Lan đang xử lý ca này từ 14:07."; "Nhận thay" requires a reason and notifies Lan |
| The AI is executing | Conflicting actions disabled with "Đang thực hiện: đổi lịch, lần thử 1 trên 3." |
| The case changed while open | The changed section carries the change mark (cskh-motion-map.md); the DecisionBar applies the click guard (§7) |

### J. Connection, permission, mode

Connected: nothing. Reconnecting and offline: the alert slot (K-11); offline also replaces every action with "Cần có mạng để thực
hiện" and shows "Cập nhật lúc 14:05" on data. Missing right: the action is replaced by its requirement in words and a way forward
("Cần trưởng xưởng duyệt. Chuyển trưởng xưởng"). Demo mode: banner and "Dữ liệu mẫu".

## 3. Screens

### K1. Tổng quan (Overview)

**Purpose.** The shift at a glance, so the employee can scan in seconds and go straight to what needs them.

**Hierarchy** (full width; main column 8, side column 4):
1. `h1` "Tổng quan" with the shift line: "Ca trực: Hải, CVDV xưởng Long Biên · 08:00 đến 17:00".
2. "An toàn", only when a safety case is open: its rows first, `--danger` marker.
3. Main: `h2` "Cần bạn ngay": the first five rows of "Cần tôi xử lý" in the queue's order, as a table (Ưu tiên, Khách và xe,
   Trạng thái, Hạn, Tóm tắt) with "Mở hàng ưu tiên (5)".
4. Main: `h2` "Lời hứa đến hạn hôm nay": promises owed by the employee or by the agent on their cases (PromiseLine table: ai hứa, hứa gì, hạn, ca).
5. Side: `h2` "Hệ thống đang xử lý": one line per state with its count and a link to the view ("Đang điều tra 2", "Chờ khách xác
   nhận 1", "Đang xác minh 3"). Counts only, no charts.
6. Side: `h2` "Ma sát mới": the three newest clusters from K3, one line each.
7. Side: `h2` "Kết quả gần đây": verified resolutions, recurrences and failed actions of the last shift, one line each, linked.

**Primary action.** "Mở hàng ưu tiên". If a callback is overdue, the overdue case's "Mở ca" takes the primary style instead.

**Secondary actions.** Each row and count links to its case or view; customer search.

**System states.** Safety (block 2 appears, alert slot); nothing needs the employee ("Cần bạn ngay" says "Không có ca nào cần bạn
lúc này." and the primary becomes "Mở hàng ưu tiên" in secondary style); counts change in place without motion; a count whose view is
not available yet says "Chưa có dữ liệu" (D-05).

**Empty.** Start of a quiet shift: each block says what will appear ("Ca cần bạn sẽ hiện ở đây kèm hạn gọi lại.").

**Loading.** Blocks load independently with static skeleton rows; the header and alert slot render first.

**Error.** Per block: "Chưa tải được lời hứa đến hạn." with "Thử lại"; other blocks stay.

**Responsive.** Below 1024px the side column follows the main column; tables become label and value rows below 768px.

**Accessibility.** One `h1`, one `h2` per block in reading order (main before side); counts are links whose names include the
state ("Chờ khách xác nhận: 1 ca"); count changes are not announced (the screen is not watched continuously).

**Data.** Handoffs only today. Gaps: counts by state, promises due, shift and skill data (D-05, D-16).

### K2. Hàng ưu tiên (Priority Queue, the workspace)

**Purpose.** The ordered list of work, with the open case beside it, so the employee moves from one decision to the next without
losing their place. Detailed design in §5.

**Hierarchy** (at `xl`):
1. Queue pane: the view menu ("Cần tôi xử lý (5)") with the order rule in a tooltip; "Lọc" (skill group, workshop, vehicle model,
   flags) with active filters listed as removable chips; the update control ("1 ca mới, 1 thay đổi. Hiện"); the rows; the footer count.
2. Case pane: K4 for the selected case, or, with none selected, a summary of the view ("5 ca cần bạn; hạn gần nhất 14:21.") and
   "Mở ca đầu tiên (Enter)".
3. Decision pane: K4's decision pane.

**Primary action.** Inside the decision pane, per state (§2 A). The queue pane itself has none.

**Secondary actions.** View switch, filters, "Hiện" on the update control, row selection.

**System states.** Views and order per the IA (§6); safety pinned; new and re-ranked cases behind the update control; a row that
changed carries the change mark and "Vừa đổi 14:06"; a row that left the view (resolved, reassigned) stays, muted, with "Đã rời
danh sách này" until the update control is applied or the employee moves on; presence and locks per §2 I.

**Empty.** Per view: "Không có ca nào cần bạn. Ca mới sẽ hiện ở đây kèm hạn gọi lại." (content.md §5); "Không có ca nào chờ duyệt.";
a filtered view: "Không có ca khớp bộ lọc." with "Xoá bộ lọc".

**Loading.** Six static skeleton rows; the case pane keeps the previous case until a new one is selected.

**Error.** "Chưa tải được hàng ưu tiên." with "Thử lại"; cached rows stay with "Cập nhật lúc …".

**Responsive.** Per §1 panes. Below 1024px the queue is its own screen and selecting a row opens K4 full width.

**Accessibility.** The queue is a list of links (or a grid with row headers when shown as a table); `j`/`k` move, `Enter` opens and
moves focus to the case heading; focus stays in the queue while moving; the update control is announced once, batched ("2 ca mới"),
at most every 30 seconds; the three panes are regions named "Hàng ưu tiên", "Chi tiết ca", "Quyết định". One `h1` per page: the open
case's summary (in "Chi tiết ca"), or with no case open the view heading ("Hàng ưu tiên: Cần tôi xử lý"); the queue pane and the
decision pane start at `h2`.

**Data.** `GET /api/v1/handoffs` (handoff views), `POST /api/v1/handoffs/{id}/accept`. Gaps: every active case by state (D-05), presence (D-16).

### K3. Ma sát đang diễn ra (Active Friction)

**Purpose.** Show what is going wrong across customers that the system is already handling, so staff see emerging friction before
customers call, and see why the AI did or did not contact someone.

**Hierarchy:**
1. `h1` "Ma sát đang diễn ra" and one sentence: "Hệ thống đang theo dõi 4 nhóm ma sát; 1 nhóm mới trong 24 giờ."
2. Filters: loại (xe, linh kiện, trạm sạc, lịch hẹn), xưởng, dòng xe, có ca cần người.
3. FrictionTable, newest first: Ma sát (plain name and code), Loại, Phạm vi (khách, xe, lịch hẹn affected), Ca theo trạng thái (counts
   with state words), Bắt đầu, Gần nhất, Đã chặn liên hệ (count).
4. Cluster detail (its own view): what the friction is and the rule that grouped it; affected cases as QueueRows; suppressed
   candidates with the arbitration reason ("Không liên hệ: ngoài 08:00 đến 20:00", "đã nhắn hôm nay", "khách đang lái"); the policies
   and SOPs in play.

Example rows, signal first: "BATT-COOL-01 lặp lại: 1 xe"; "ADAS-CAM-03, sửa được từ xa: 1 xe, pin 3%"; "Linh kiện BATT-COOL-PUMP bị
điều chuyển (thu hồi), xưởng Long Biên: 1 lịch hẹn bị ảnh hưởng".

**Primary action.** None; rows open cluster detail, and cluster detail opens cases.

**Secondary actions.** Filters; "Mở ca"; "Xem trong hàng ưu tiên" (the queue filtered to this cluster).

**System states.** A cluster that includes a safety case shows the marker and sorts first; a cluster entirely handled by the AI says
"AI đang xử lý, chưa cần người"; a cluster with suppressed contacts shows why each was held back.

**Empty.** "Không có nhóm ma sát nào đang mở. Khi tín hiệu từ xe, kho hoặc trạm sạc lặp lại, nhóm mới sẽ hiện ở đây."

**Loading.** Static skeleton rows. **Error.** "Chưa tải được nhóm ma sát." with "Thử lại".

**Responsive.** The table scrolls horizontally inside its container with the first column sticky; below 768px rows become stacked label and value lists.

**Accessibility.** A real table with column headers and the cluster name as row header; counts read with their state words; filters are labelled controls whose result count is announced politely.

**Data.** Nothing today. Gap: clusters and suppressed candidates (D-16), every active case (D-05).

### K4. Chi tiết ca (Case Detail)

**Purpose.** Answer, in order, the nine questions of the brief, so the employee can understand, decide and act on one case in about
10 seconds for the essentials (proposal §08) and audit it fully when needed.

**Hierarchy.** A sticky case header; a sticky section index; ten sections on a vertical spine, each a node in the node grammar, so
the case reads as a chain of causes; the decision pane beside it. MASTER §9's reading order holds: the header says what happened, then
section 1 says why, sections 2 to 4 hold what was checked, 5 what is proposed, 6 and 7 what is needed, 8 and 9 the outcome.

**Case header** (sticky, in this order):
1. `h1` at `--text-xl`: the one-line summary in plain words, labelled "Trợ lý AI tóm tắt" in its tooltip ("Linh kiện giữ cho lịch
   02/10 bị điều đi; khách bực và muốn gặp người.").
2. StateChip · assignment (§2 D) · DeadlineTimer · SentimentTag · safety marker · presence.
3. Customer (name, how verified, role) linked to K5 · vehicle (model, VIN in `--font-mono`, odometer) · customer flags (§2 H) · "Nhật ký" (K6).
4. "Tiếp theo": who must do what by when (§2 A).

**Section index** (sticky under the header): "1 Lý do · 2 Phát hiện · 3 Bằng chứng · 4 Điều tra · 5 Đề xuất · 6 Chính sách ·
7 Quyết định · 8 Thực hiện · 9 Hiệu quả · 10 Nhật ký"; the section where the case is now is marked "(hiện tại)" in text; jumps are
instant; keys `1` to `9`, `0`.

**The spine.** A vertical line through one node per section. Sections produced by the system or the AI (1 to 6, 8, 9) carry a
circle; section 7 carries a diamond while a person must decide and a square once a person decided; section 9 ends in the check when
verified; section 10 a small neutral circle. Color marks the present: only the current section's node carries its holder's hue;
history is neutral; sections not reached yet are hollow. Nodes are `aria-hidden`; the index says the same in words.

**Sections.** Each `h2` is the question; the first line under it is a plain-language answer; structured detail follows, always expanded (K-10).
A section with no data says so in one line and is never removed.

| # | `h2` | First line (J2 example) | Detail | Empty line |
|---|---|---|---|---|
| 1 | Vì sao có ca này | "Khách yêu cầu gặp nhân viên lúc 14:06, sau khi lịch hẹn phải đổi vì linh kiện bị điều đi." | The origin chain first, from the first system signal to now: "Tín hiệu xe BATT-COOL-01 (29/09) → đặt lịch Long Biên → linh kiện bị điều đi (30/09) → khách muốn gặp người (14:06)". Then a `dl`: trigger rule (`on_reservation_cancelled`, spec §09); origin case ("ca BATT-COOL-01 mở 08:15 29/09 theo `on_repeated_warning`"); contact arbitration ("được liên hệ: không lái xe, trong 08:00 đến 20:00, không có khiếu nại mở, chưa nhắn hôm nay"); routing ("CVDV xưởng Long Biên: xe có lịch tại đây"); linked cases | Never empty |
| 2 | Hệ thống phát hiện gì | "BATT-COOL-01 lặp 3 lần trong 14 ngày; linh kiện R-7702 bị điều đi lúc 13:55 30/09." | Signals table: Thời điểm, Sự kiện (`vehicle.dtc.raised`, `parts.reservation.cancelled`, `chat.handoff.requested`), Nguồn, Chi tiết. Repetition line: "Lặp 3 lần trong 14 ngày (ngưỡng của quy tắc: 3)". Suppressed signals as neutral rows with their reason | "Ca do nhân viên tạo, không có tín hiệu tự động." |
| 3 | Bằng chứng | "7 sự thật từ 5 nguồn; mới nhất đọc lúc 13:57." | EvidenceList grouped by kind (IA §7): fact, source, read time, raw reference in `--font-mono`. A fact read before the latest event carries "đọc trước thay đổi gần nhất" | "Chưa có bằng chứng nào được ghi nhận." |
| 4 | AI đã điều tra gì | "8 bước: 6 theo quy tắc (L0), 1 phân loại (L1), 1 xếp lịch (L2)." | InvestigationSteps table: #, Tầng (LayerTag), Công cụ (`find_options`, `get_vehicle_status`, `check_warranty`), Hỏi gì, Trả về gì, Dùng ở mục. The decision gate as a row: "Cổng quyết định: L0 chưa đủ vì có 2 phương án hợp lệ cần xếp theo nhiều ràng buộc; chuyển L2". "Đã loại trừ": khả năng, vì sao, luật hoặc nguồn ("Sửa từ xa: không áp dụng, BATT-COOL-01 không sửa từ xa được"; "Long Biên: tồn kho BATT-COOL-PUMP bằng 0 sau điều chuyển"). Tokens and milliseconds only in the Demo stage | "AI chưa điều tra ca này." |
| 5 | AI đề xuất gì | "Đổi lịch sang Gia Lâm, 09:00 thứ Bảy 03/10; dự phòng Hoài Đức, 09:00 thứ Năm 01/10." | Options table: Phương án, Xưởng, Thời gian, Khoảng cách, Linh kiện, Tầm đi, Khoang cao áp, Lý do (`Option.why`), Trạng thái. Excluded options muted with "Loại: …". The messages the AI sent are in section 8 | "AI chưa đề xuất." |
| 6 | Chính sách cho phép gì | "1 hành động cần khách xác nhận, 2 được phép, 1 cần duyệt, 1 không được phép." | ActionPolicyTable (below); then "Căn cứ": the policies and versions used ("SOP đổi lịch khi thiếu linh kiện v1.2", "Chính sách liên hệ chủ động", "Bảng bù đắp", "Chính sách bảo hành 2026.03") | "Chưa có hành động nào để kiểm tra." |
| 7 | Người cần quyết định gì | "Chờ bạn: chốt lịch mới với khách qua điện thoại trước 14:21." | `dl`: quyết định gì, ai (role or person), hạn, các lựa chọn, AI gợi ý (`next_best_action`: "Gọi lại, xin lỗi, ưu tiên phương án Gia Lâm"), vì sao cần người. Then "Quyết định đã có": Thời điểm, Người, Quyết định, Lý do | "Không có quyết định nào đang chờ người." |
| 8 | Đã thực hiện gì | "Chưa có hành động mới sau khi lịch cũ bị huỷ." (after: "Đã đổi lịch sang Gia Lâm lúc 14:18; đã gửi 2 tin cho khách.") | Actions table: Thời điểm, Hành động, Tham số, Ai cho phép (khách, Hải, tự động mức 1), Kết quả ("Hệ thống xác nhận", "Thất bại: …", "Đang thực hiện, lần 1 trên 3"), Mã (`A-20931`). Messages sent: mẫu, kênh, trạng thái gửi. Compensating actions (trả slot, trả reservation) as rows | "Chưa thực hiện hành động nào." |
| 9 | Có hiệu quả không | "Chưa bắt đầu xác minh." (later: "Đang xác minh: ngày 3 trên 7, 0 lần tái phát.") | VerificationMeter: the guard checklist, then the window with its reason ("7 ngày: lỗi liên tục"); recurrences; the closing rule ("Ca đóng khi: 7 ngày không tái phát"); promises to the customer, kept or broken; the outcome | Never removed; says what will be verified |
| 10 | Nhật ký | "14 dòng; gần nhất 14:06, khách." | The last five AuditLog rows; "Xem nhật ký đầy đủ" (K6) | Never empty |

**ActionPolicyTable** (section 6), J2 example. Columns: Hành động và tham số, Mức, Căn cứ, Validator, Kết luận, Trạng thái.

| Hành động và tham số | Mức | Căn cứ | Validator | Kết luận | Trạng thái |
|---|---|---|---|---|---|
| Đổi lịch: Gia Lâm, 09:00 03/10, VF8-4821 | 2 | SOP đổi lịch khi thiếu linh kiện v1.2 | 4 Đạt; Chưa kiểm: linh kiện đã giữ, slot đã khoá, xác nhận còn hiệu lực | Cần khách xác nhận | Chờ người quyết định |
| Gửi tin xin lỗi theo mẫu | 1 | Chính sách liên hệ chủ động | Đạt | Được phép (mức 1) | Đã gửi 13:58 |
| Ưu tiên khung giờ khách chọn | 1 | Bảng bù đắp: mức nhẹ | Đạt | Được phép (mức 1) | Đề xuất |
| Hỗ trợ đi lại cho lần sau | 3 | Bảng bù đắp: ngoài mức nhẹ thì cần duyệt; AI không tự chọn mức (proposal §09) | Chưa kiểm | Cần nhân viên duyệt (CVDV hoặc trưởng xưởng) | Đề xuất |
| Hứa “chắc chắn được bảo hành” | Không có | Luật 2 của trợ lý | Không đạt | Không được phép: kết luận bảo hành thuộc xưởng | Đã chặn |

Passing checks are counted; every check that did not pass is named in the cell, so nothing is hidden behind a disclosure (K-10).

**Decision pane** (top to bottom):
1. Briefing, from the HandoffCard: "Trợ lý AI tóm tắt"; "Đã nói, đã hứa với khách" (prominent, because staff must honor it:
   “Xưởng Gia Lâm có sẵn linh kiện”, “Nhân viên sẽ phản hồi trong 15 phút”); "Không nên" (never collapsed, `circle-slash`: "Hứa bù
   đắp trước khi được duyệt", "Đề xuất lại xưởng Long Biên cho lịch này", "Hỏi lại thông tin xe và lịch cũ"); sentiment with the
   customer's words ("Bực: “anh đã sắp xếp rồi”").
2. "Liên hệ khách": "Gọi khách", "Nhắn khách" (composer with templates); "Trợ lý AI gợi ý" (CopilotSuggestion: a suggested reply
   with its sources; "Dùng gợi ý" inserts it into the composer, never sends it); "Ghi chú nội bộ".
3. DecisionBar, sticky at the bottom of the pane: the actions valid for the state and the employee's rights (§6), one primary.

**Primary action.** Per state (§2 A). For J2: "Nhận" (`n`), then "Gọi khách", then "Chốt phương án".

**Secondary actions.** Per state: "Chuyển người khác", "Trả lại cho AI", "Nhận xử lý", "Mở lại ca", "Nhắn khách", "Ghi chú nội bộ".

**System states.** Everything in §2. In particular: a safety case shows only the template text in sections 5 and 8, no AI proposal, and
the 24/7 actions; a level-3 case without the employee's right shows the requirement in words; a locked case (§2 I) shows who holds it.

**Empty.** Not applicable; an unknown link says "Không tìm thấy ca này. Có thể ca đã được gộp." with "Về hàng ưu tiên".

**Loading.** The header and section index render from the queue row at once; sections load with static skeletons in their own
shape; the DecisionBar does not render until the state is known.

**Error.** Per section: "Chưa tải được bằng chứng." with "Thử lại"; the rest stays usable. An action failure appears in the
DecisionBar with what is true now ("Lịch chưa được đổi.") and in section 8 as a failure event.

**Responsive.** `xl`: as described. 1024 to 1279px: the briefing moves above section 1; the DecisionBar docks at the bottom of the case
pane. Below 1024px: the case is full width; the section index becomes a "Mục" menu; tables scroll inside their containers with a
sticky first column.

**Accessibility.** The case is a `main` region with one `h1` and ten `h2` in fixed order; the section index is a `nav`; tables have
column headers and the action or step as row header; the DecisionBar region has a heading and `aria-busy` while executing; state
changes announce "Trạng thái: …" once; nothing moves focus except the employee's own actions (opening a case focuses its `h1`).

**Data.** `Handoff.card` (summary, customer, goals, facts, `agent_said_promised`, sentiment, `next_best_action`, `do_not`, `deadline_at`),
`/trace/{trace_id}`, accept. Gaps: case state (D-04); signals, layers, verdicts, validator results, actions, verification, case audit (D-06); presence, call log, notes, reassign, hand back (D-16).

### K5. Khách hàng (Customers)

**Purpose.** Find a customer fast (an inbound call, a callback) and see who they are, what they own, what is open, what was promised
and what they consented to.

**Hierarchy:**
1. `h1` "Khách hàng"; the search field (name, phone, plate, VIN), also reachable from the header with `/`.
2. Results table: Khách, Xe và vai trò, Ca đang mở (state words), Liên hệ gần nhất, Kênh ưa thích.
3. Profile (its own view): header (name, how verified, phone masked "09xx xxx 821", address form "anh Minh", preferred channel, flags);
   `h2` "Xe và quyền" (VIN, dòng xe, vai trò, quyền đặt lịch); `h2` "Ca đang mở" (QueueRows); `h2` "Lời hứa" (open, kept, broken);
   `h2` "Ca trước đây" (with verified outcomes); `h2` "Liên hệ gần đây" (messages and calls, one line each); `h2` "Tuỳ chọn và đồng
   ý" (data sharing, AI proactive messages on or off, always human, channel, quiet hours); `h2` "Trợ lý AI ghi nhớ" (read-only for
   staff; the customer edits it in C5); `h2` "Ghi chú nội bộ".

**Primary action.** On a profile with an open case that needs the employee: "Mở ca". Otherwise none.

**Secondary actions.** "Gọi khách", "Nhắn khách", "Ghi nhận yêu cầu mới" (creates a case for an inbound request; D-16).

**System states.** Driver profiles show only what the owner allows (proposal §06 D2); a customer with an open complaint shows "Đang
khiếu nại: không liên hệ chủ động"; every profile view is written to the audit ("Hải xem hồ sơ lúc 14:07"), and the profile says so in one line.

**Empty.** No search yet: "Tìm theo tên, số điện thoại, biển số hoặc VIN." No result: "Không tìm thấy khách khớp “…”." with the hint to try the VIN.

**Loading.** Results as skeleton rows; profile sections load independently.

**Error.** "Chưa tìm được vì hệ thống đang gián đoạn." with "Thử lại".

**Responsive.** Results table to stacked rows below 768px; profile sections stack.

**Accessibility.** Search is a labelled `search` landmark (`type="search"`, spellcheck off, the placeholder ends with "…" and shows an example) with the result count announced politely; results are a table with the
name as row header; masked numbers have an accessible name that says they are masked.

**Data.** None today. Gap: customer search and profile with access logging (D-16). The fixtures hold customers, vehicles, drivers and roles.

### K6. Truy vết và nhật ký (Trace / Audit)

**Purpose.** The complete, immutable record: who did what, when, on what evidence, and which steps used a model.

**Hierarchy:**
1. `h1` "Truy vết và nhật ký", with the case or customer in scope ("Ca: Nguyễn Văn Minh, VF8-4821").
2. Tabs (URL reflects the tab): "Nhật ký ca" and "Lượt chạy AI".
3. Filters: tác nhân (L0, L1, L2, Validator, Người, Khách, Hệ thống), loại hành động, khoảng thời gian.
4. "Nhật ký ca": AuditLog table: Thời điểm, Tác nhân, Hành động, Đầu vào (tóm tắt), Kết quả, Bằng chứng (link), Mã. Rows are append-only.
5. "Lượt chạy AI": the TraceStep table per run: Bước, Tầng, Công cụ, Đầu vào, Đầu ra, ms; tokens in the Demo stage only; totals per run
   ("8 bước, 6 không dùng mô hình").
6. Raw payloads: collapsed per row with their size ("Dữ liệu gốc, 1,2 KB"), the only collapsed content in CSKH (K-10).

**Primary action.** None. **Secondary actions.** Filters, tabs, "Mở ca", copy a row link.

**System states.** A row whose actor is the AI shows its LayerTag; a staff row shows the name; a failure row shows the triangle; a
compensating action links to the action it compensates. The `analysis` field and any model rationale are never rendered (IA §7).

**Empty.** "Chưa có dòng nhật ký nào khớp bộ lọc." with "Xoá bộ lọc".

**Loading.** Skeleton rows. **Error.** "Chưa tải được nhật ký." with "Thử lại".

**Responsive.** Tables scroll inside their container with the time column sticky; filters wrap above the table.

**Accessibility.** Real tables; time cells carry the full date in the accessible name; tabs follow the tab pattern; expanding a payload is a disclosure button with `aria-expanded`.

**Data.** `GET /api/v1/trace/{trace_id}` for one agent run. Gap: case-level audit and actor or layer per step (D-06).

### K7. Phím tắt (Shortcuts)

**Purpose.** List the shortcuts and let the employee turn them off.

**Hierarchy.** A Dialog: the switch "Dùng phím tắt"; the table of keys and actions (accessibility.md §6); the rule "Không có phím tắt
cho quyết định có hệ quả".

**Primary action.** "Đóng". **Secondary actions.** The switch.

**System states.** On or off (stored per employee). **Empty, loading, error.** Not applicable; the list is local.

**Responsive.** Full screen below 768px. **Accessibility.** Dialog pattern; Escape closes; focus returns to the trigger.

## 4. Case-detail wireframe

`xl` (1280px), J2 at 14:07, Hải viewing, not yet accepted. Symbols stand for the node grammar: ● circle, ◆ diamond, ■ square, ○ not
reached. "(h1)" marks the heading level and is not on screen. The DecisionBar ("Quyết định") is pinned to the bottom of the decision
pane; the case pane scrolls under its sticky header and section index.

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│{Tên sản phẩm} CSKH  Tổng quan  [Hàng ưu tiên]  Ma sát  Khách hàng  Nhật ký   Tìm khách, SĐT, biển số, VIN   (ô cảnh báo)  Hải ▾        │
├────────────────────────────────────────┬────────────────────────────────────────────────────────┬──────────────────────────────────────┤
│Cần tôi xử lý (5)                      ▾│Linh kiện giữ cho lịch 02/10 bị điều đi; khách bực      │Trợ lý AI tóm tắt                     │
│Theo mức ưu tiên · 1 ca mới: Hiện       │và muốn gặp người.                              (h1)    │Linh kiện bị điều đi; khách đã sắp    │
│────────────────────────────────────────│■ Đã chuyển người · Chưa nhận · Bực · Lan đang xem      │xếp ngày, bực, muốn gặp người.        │
│▌Nguyễn Văn Minh · VF 8 VF8-4821        │Gọi lại trước 14:21, còn 14 phút                        │──────────────────────────────────────│
│▌■ Đã chuyển người                      │Nguyễn Văn Minh · xác thực qua app · chủ xe             │Đã nói, đã hứa với khách              │
│▌Gọi lại trước 14:21, còn 14 phút       │VF 8 · VF8-4821 · 38.420 km · Hồ sơ khách · Nhật ký     │• “Xưởng Gia Lâm có sẵn linh kiện”    │
│▌Linh kiện bị điều đi; khách bực, mu…   │Tiếp theo: chờ bạn nhận ca, gọi lại trước 14:21.        │• “Nhân viên phản hồi trong 15 phút”  │
│▌Chưa nhận · Lan đang xem               │────────────────────────────────────────────────────────│Không nên                             │
│────────────────────────────────────────│1 Lý do · 2 Phát hiện · 3 Bằng chứng · 4 Điều tra       │⊘ Hứa bù đắp trước khi được duyệt     │
│ Nguyễn Văn Minh · VF 8 VF8-4821        │5 Đề xuất · 6 Chính sách · 7 Quyết định (hiện tại)      │⊘ Đề xuất lại xưởng Long Biên         │
│ ◆ Cần duyệt · trước 16:00              │8 Thực hiện · 9 Hiệu quả · 10 Nhật ký                   │⊘ Hỏi lại thông tin xe và lịch cũ     │
│ Bù đắp sau khi lịch phải đổi (mức 3)   │────────────────────────────────────────────────────────│Cảm xúc: Bực (ước tính của mô hình)   │
│ Của bạn                                │● 1 Vì sao có ca này                                    │“anh đã sắp xếp rồi”                  │
│────────────────────────────────────────││   Khách muốn gặp người lúc 14:06, sau khi lịch phải   │──────────────────────────────────────│
│ Lê Quốc Bảo · VF 6 VF6-2290            ││   đổi. Quy tắc on_reservation_cancelled; ca gốc       │Liên hệ khách                         │
│ ◆ Chờ khách xác nhận · gửi 09:40       ││   on_repeated_warning (08:15 29/09).                  │[ Gọi khách ]  [ Nhắn khách ]         │
│ Cập nhật phần mềm từ xa; pin 3%        │● 2 Hệ thống phát hiện gì                               │Trợ lý AI gợi ý tin nhắn (2 nguồn) ▸  │
│ Của bạn                                ││   BATT-COOL-01 lặp 3 lần / 14 ngày (ngưỡng 3)         │Ghi chú nội bộ ▸                      │
│────────────────────────────────────────││   13:55 30/09  parts.reservation.cancelled R-7702     │                                      │
│ … 2 ca nữa                             ││   14:06 30/09  chat.handoff.requested                 │                                      │
│                                        │● 3 Bằng chứng: 7 sự thật, 5 nguồn                      │                                      │
│                                        ││   Bảo dưỡng đủ 5 kỳ          dms:maintenance  13:56   │                                      │
│                                        ││   Bảo hành sơ bộ: đủ         kb:warranty…§2.1 13:56   │                                      │
│                                        ││   Gia Lâm còn 2 linh kiện    erp:stock        13:57   │                                      │
│                                        ││   Pin 42%, đủ tới 3 xưởng    telematics:soc   13:57   │                                      │
│                                        │● 4 AI đã điều tra gì: 8 bước, 6 không dùng mô hình     │                                      │
│                                        ││   L0 find_options   Long Biên hết linh kiện           │                                      │
│                                        ││   L2 scheduler      Gia Lâm trước, Hoài Đức dự phòng  │                                      │
│                                        ││   Đã loại trừ: sửa từ xa (không áp dụng cho lỗi này)  │                                      │
│                                        │● 5 AI đề xuất gì                                       │                                      │
│                                        ││   Gia Lâm   09:00 03/10   7,1 km  có linh kiện        │                                      │
│                                        ││   Hoài Đức  09:00 01/10  27,1 km  có linh kiện        │                                      │
│                                        ││   Loại: Long Biên, không còn linh kiện                │                                      │
│                                        │● 6 Chính sách cho phép gì                              │                                      │
│                                        ││   Đổi lịch Gia Lâm   mức 2  Cần khách xác nhận        │                                      │
│                                        ││   Tin xin lỗi        mức 1  Được phép (đã gửi)        │                                      │
│                                        ││   Hỗ trợ đi lại      mức 3  Cần nhân viên duyệt       │                                      │
│                                        ││   Hứa chắc chắn bảo hành  Không được phép: luật 2     │                                      │
│                                        │◆ 7 Người cần quyết định gì                 (hiện tại)  │                                      │
│                                        ││   Bạn: chốt lịch mới với khách qua điện thoại,        │──────────────────────────────────────│
│                                        ││   trước 14:21. AI gợi ý: gọi lại, xin lỗi, Gia Lâm.   │Quyết định                            │
│                                        │○ 8 Đã thực hiện gì: chưa có hành động mới              │[        Nhận ca  (n)        ]        │
│────────────────────────────────────────│○ 9 Có hiệu quả không: chưa bắt đầu xác minh            │Chuyển người khác · Trả lại cho AI    │
│5 ca · cập nhật 14:07                   │○ 10 Nhật ký: 14 dòng · Xem đầy đủ                      │Hạn gọi lại: 14:21, còn 14 phút       │
└────────────────────────────────────────┴────────────────────────────────────────────────────────┴──────────────────────────────────────┘
```

## 5. Queue design

**Row anatomy.** Two lines of `--text-sm` with `--space-2` vertical padding, so every row is taller than `--target-min`, separated by hairlines; no cards (K-05).

```text
▌[marker] Nguyễn Văn Minh · VF 8 VF8-4821            Gọi lại trước 14:21, còn 14 phút
▌■ Đã chuyển người   Linh kiện bị điều đi; khách bực, muốn gặp người    Chưa nhận · Lan đang xem
```

| Part | Rule |
|---|---|
| Marker | Only for safety ("An toàn", `siren`, `--danger`) and overdue ("Quá hạn", `--danger`); words and icon, never a dot |
| Customer and vehicle | Name, model, VIN in `--font-mono` |
| Deadline | DeadlineTimer per §2 E, right-aligned; empty when none |
| State | StateChip (compact) with the CSKH label |
| Summary | One line; truncates with an ellipsis; the full text is in the row's accessible name and in the case header |
| Owner and presence | §2 D and I, right-aligned |
| Selected | `--sunken` with a 2px `--accent` bar |
| Changed | The change mark (cskh-motion-map.md) and "Vừa đổi 14:06", until the row is opened |
| Left the view | Muted, "Đã rời danh sách này", until the update control is applied |

Never in a row: avatars, colored dots, "HOT" or urgency badges, sentiment as color alone, more than one chip.

**Order.** The priority model (IA §6), fixed; the view heading's tooltip states it in words. Sorting is not user-editable in v1.0,
so position means the same thing to everyone on the shift.

**Views.** "Cần tôi xử lý" (default), "Chờ duyệt", "Chờ khách xác nhận", "AI đang xử lý", "Đang xác minh", "Đã xong hôm nay", each with
its count, in a menu at the top of the pane; the view and filters live in the URL.

**Live updates.** New, re-ranked and departed cases wait behind "2 ca mới, 1 thay đổi. Hiện"; applying it re-renders the list and
keeps the selected case and focus. Content changes to rows already shown apply in place with the change mark. Safety appears at once in
the alert slot and is inserted at the top as soon as the pointer is not over the queue pane.

**Keyboard.** `j`/`k` move the focus ring between rows instantly (no scroll animation); `Enter` opens; `n` accepts the open case;
`g q` returns to the queue from anywhere.

**Bulk actions.** None in v1.0: each decision needs its own evidence (KQ-8).

## 6. Key employee actions

| Action | Available when | Authority | Confirmation | Key | Result | Audit row |
|---|---|---|---|---|---|---|
| Nhận | ESCALATED, unassigned, in my skill | Any agent in the group | None | `n` | Owner set; the callback deadline is mine | "Hải nhận ca" |
| Nhận xử lý (from the AI) | DETECTED to WAITING FOR CUSTOMER, AI-held | Any agent in the group | Dialog with a reason | | ESCALATED to me; the AI stops acting and assists | "Hải nhận xử lý thay AI: {lý do}" |
| Gọi khách | Any case with a reachable customer | Agent | None | | Opens the call (D-16); then "Ghi kết quả cuộc gọi" | "Hải gọi khách" |
| Ghi kết quả cuộc gọi | After a call | Caller | None | | Outcome, consent if any, next step; meets the callback deadline | "Hải gọi 14:12: …" |
| Chốt phương án (thay khách) | ESCALATED or WAITING FOR CUSTOMER, mine, after a call | Agent, level 2 on the customer's behalf (flow D) | Dialog: every parameter, the recorded verbal consent with its time | | EXECUTING, then the receipt; the customer is told | "Hải chốt Gia Lâm 09:00 03/10; khách đồng ý qua điện thoại 14:12" |
| Duyệt / Sửa rồi duyệt | WAITING FOR HUMAN in my scope | Approver role | Dialog with the parameters; "Sửa rồi duyệt" returns the case to the customer if their parameters changed | | EXECUTING, or WAITING FOR CUSTOMER | "Trưởng xưởng duyệt: …" |
| Từ chối | WAITING FOR HUMAN in my scope | Approver role | Dialog; reason required | | ESCALATED to a named person | "Từ chối: {lý do}" |
| Chuyển người khác | Any case I hold | Agent | Pick a person or group; note | | Reassigned; the new owner is notified | "Chuyển cho Lan: {ghi chú}" |
| Trả lại cho AI | ESCALATED, mine, decision made | Agent | None | | The AI resumes the journey (flow D step 7) | "Hải trả lại cho AI" |
| Nhắn khách | Any case, within contact rules | Agent | Preview before sending | | Message in the customer's thread with StaffByline | "Hải gửi tin: {mẫu}" |
| Ghi chú nội bộ | Any case | Agent | None | | Note in section 8 and K5; never shown to the customer | "Hải ghi chú" |
| Thử lại | After an execution failure | Agent | None | | EXECUTING again with the same idempotency key | "Thử lại lần 2" |
| Mở lại ca | VERIFYING or RESOLVED | Agent | Dialog; reason required | | New linked case, DETECTED | "Mở lại: {lý do}" |

Consequential decisions ("Chốt phương án", "Duyệt", "Từ chối") have no single-key shortcut (K-07). Only accept exists in today's
API; the rest need D-06 and D-16.

## 7. Critical accessibility considerations

1. **Density never lowers the floors.** Text at least `--text-sm`, targets at least `--target-min` with `--target-gap`, AA contrast in both themes including muted and disabled text (K-01, K-02).
2. **State is never color alone.** Chip words and icons, deadline words ("còn 4 phút", "Quá hạn 3 phút"), verdict words, sentiment words; the spine is mirrored in the index text.
3. **Nothing moves under the pointer.** Rows never reorder in place, alerts never shift panes (K-11), and a server-driven change to the DecisionBar ignores any click that arrives within `--dur-slow` of the change, with the change mark explaining why. This protects consequential decisions from misclicks.
4. **Keyboard first.** The full loop (scan, open, read, decide, act) works without a pointer; shortcuts only in the queue and case regions, never in text fields, with a switch to turn them off (K-07); consequential decisions only through buttons and dialogs.
5. **Focus.** Visible in both themes and never covered by the sticky header, section index or DecisionBar (scroll padding); opening a case moves focus to its `h1`; dialogs trap and return focus; live updates never move it.
6. **Announcements are batched and meaningful.** New cases at most every 30 seconds ("2 ca mới"); deadlines only at thresholds; state changes of the open case once; safety with `role="alert"` once; never a bare number.
7. **Real structure.** Landmarks per pane (`region` with names), one `h1` and ten `h2` per case, real tables with row and column headers, `dl` for facts, lists for queue rows.
8. **Truncation never hides meaning.** Only the queue summary truncates, and its full text is in the accessible name and the case header; "Không nên", promises, deadlines and verdicts never truncate or collapse (K-10).
9. **Reflow.** At 200% zoom and down to 320px the console becomes one pane at a time with back navigation; tables scroll only inside their own container with a sticky first column (K-08).
10. **Reduced motion and forced colors.** The change cue becomes a static "Vừa đổi" mark; the loader is static; every state stays distinguishable in forced colors through shape, icon and word.
