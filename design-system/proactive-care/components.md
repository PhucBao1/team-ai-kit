# Components

Part of the Proactive Care Design System v1.0. Start at [MASTER.md](MASTER.md). This is a specification, not code: names, anatomy,
variants, states, data and accessibility. Implementation lives in P-073 `frontend/` and must match it.

## 1. Rules for every component

1. **One implementation, every surface.** Landing figures, the Demo stage and the real screens render the same components with
   fixture data. A Landing-only lookalike is a defect (taste-skill §9.E: no div-built fake screens).
2. **Density comes from context.** Components read the density mode (airy, comfortable, compact) from their container; they never
   hardcode spacing for one surface. See [spacing.md](spacing.md) §2.
3. **Every component designs its loading, empty and error forms** (taste-rules rule 6). Loading is a skeleton in the shape of the real
   content; empty says what will appear and how; error says what happened in Vietnamese and offers "Thử lại".
4. **Data comes from the contract** (`P-073/contracts/api.yaml`), with types generated, never hand-written. Where a component needs a field
   the contract lacks, it is listed under "Gap" and in the governance doc (D-06); the component must not invent the value.
5. **Tokens only.** No raw values; no new colors, radii, shadows or fonts.

## 2. The node grammar and the Care Trace

### 2.1 TraceNode

The atom of the signature element. Shape is CSS geometry, not an icon.

| Node | Shape | Fill | Meaning |
|---|---|---|---|
| AI / system, current | circle, `--radius-full` | `--ai` with a 2px ring of `--ai` at `--space-1` distance | AI or system holds the case now |
| Waiting for a person, current | diamond (square rotated 45°) | `--attn-line` | A person must decide |
| Human-owned, current | square, `--radius-sm` | `--human` | A named person owns the case |
| Verified | circle | `--ok`, with a check cut out | RESOLVED |
| Event: failure or safety | triangle | `--danger` | Something failed, or safety |
| Event: neutral | small circle | `--border-strong` | Reminder sent, suppressed (CSKH), parameter change logged |
| Past (any holder) | its own shape | `--fg` at small size, no ring | History is neutral (color marks the present) |
| Future | its own shape | hollow, `--border-strong` outline | Expected next step |

Sizes: `--node-sm` (compact rows), `--node-md` (default), `--node-lg` (Landing figures and diagrams).

### 2.2 CareTrace

**Purpose.** Show the life of one case: what happened, who acted, what is next. The product's signature element.

**Anatomy.** A connector of `--trace-w` through node centers; per node: state or event label (always visible), actor (AI layer,
staff name, customer, system), time, and optionally one line of detail and a link to its evidence.
Connector segments: past = `--border-strong` solid; current = holder hue solid; future = `--border-strong` dashed.

| Variant | Where | Notes |
|---|---|---|
| Vertical, full | Customer timeline (C3); CSKH case file timeline | Labels right of the axis; times right-aligned in CSKH. Customer: time, actor and a cause line under each label, grouped by day, completed steps in the forms of MASTER §12.4, expected next steps as future nodes ([customer-journey.md](../../docs/frontend/customer-journey.md) §3) |
| Vertical, compact | CSKH queue preview, Demo stage | `--node-sm`, one line per node |
| Horizontal | Landing story and architecture | Labels below nodes; wraps to vertical below `md` |
| Horizontal, condensed | Customer case header (C2) | The seven customer phases as nodes only, the current one in its holder's shape and color, then the link "Xem tiến trình"; `aria-hidden`, because the StateChip and the state sentence carry the meaning |

**States.** Loading: skeleton of three nodes. Empty: never empty (a case starts at DETECTED). Error: "Chưa tải được tiến trình. Thử lại."

**Data.** Today only partially available: `Journey.current_step`, `Journey.last_change`, `TraceStep[]` from `/trace/{trace_id}`.
**Gap:** no case-state field, no per-step actor, layer or timestamp in `TraceStep`. Until the contract has them, the trace shows
only what the API returns and never infers states (D-04, D-06).

**Accessibility.** An ordered list; the current item has `aria-current="step"`; shapes and connector are `aria-hidden`; each item's
text reads as "Trạng thái, người thực hiện, thời gian". Customer label for the whole list: "Tiến trình xử lý"; CSKH: "Dòng thời gian".

**Motion.** New node: enters with `--dur-base`, `--ease-out`, `--rise-sm` (Customer); appears instantly (CSKH, K-03); scroll-scrubbed
drawing on Landing (L-02). History never re-animates.

## 3. State vocabulary components

| Component | Purpose | Anatomy and rules | Surfaces |
|---|---|---|---|
| **StateChip** | The current state in a word | Icon (per MASTER §12) + label on the family tint, text in the family color; `--chip-h` (Customer, Landing) or `--chip-h-sm` (CSKH rows); `--radius-sm`; ESCALATED is inverse (`--human` / `--on-human`). Non-interactive; if used as a filter it becomes a 44px toggle button | All |
| **JourneyStepper** | Where the job is (domain steps, not AI states) | Ordered steps with names, never "Bước 1" (taste-skill §9.F); for a service journey: Đặt lịch, Giữ linh kiện, Chờ hẹn, Chẩn đoán, Sửa, Xác minh. Current step in `--fg` 600 with a filled marker; done steps muted with check; future hollow. Horizontal from `md`, vertical below | Customer, CSKH, Landing figures |
| **VerificationMeter** | Progress of VERIFYING (MASTER §12) | Guard phase: the watched conditions as a short checklist ("Linh kiện đang được giữ", "Lịch hẹn còn hiệu lực"). Window phase: sentence first ("Đã theo dõi 3 trên 7 ngày, xe chưa báo lại lỗi."), then N segments, filled = elapsed clean days or sessions; no background track on Landing (taste-skill §9.F). **Gap:** phase, window length and progress are not in the contract | Customer, CSKH |
| **DeadlineTimer** | The callback deadline a staff member owes | Absolute time plus remaining minutes ("Gọi lại trước 14:21, còn 14 phút"); neutral, then `--attn` at 5 minutes or less, `--danger` when overdue ("Quá hạn 3 phút"); text updates once a minute, no animation; announced only when crossing a threshold | CSKH only (K-09). Customers never see countdowns |
| **LayerTag** | Which layer produced a step | `L0` (rule), `L1` (small model), `L2` (agent), `Validator`, `Người` (staff); `--text-sm` 600 on `--sunken`; tooltip explains the layer in one sentence. **Gap:** `TraceStep` has no layer field | CSKH, Demo, Landing architecture (L-06) |

## 4. Provenance components

| Component | Purpose | Anatomy and rules | Surfaces |
|---|---|---|---|
| **AIByline** | Says plainly that the AI wrote this | Small teal circle node + "Trợ lý AI"; on proactive messages also "Tin tự động"; time. Always visible, never collapsible (legal requirement, proposal §09) | All |
| **StaffByline** | Says which person wrote or owns this | Small ink square node + name + role ("Hải, cố vấn dịch vụ"); time | All |
| **EvidenceList** | What was checked | One row per fact: the fact in plain words, a SourceRef, the time it was read. Customer: collapsed behind "Em đã kiểm tra N nguồn" (summary first); CSKH: expanded (K-10). Facts come from `HandoffCard.facts {text, source}` and `ChatEvent.citations` | All |
| **SourceRef** | Where a fact came from | Source system and time in `--text-sm` `--muted` ("Dữ liệu xe, 14:02", "Lịch sử bảo dưỡng", "Chính sách bảo hành bản 2026.03"); in CSKH also the raw reference in `--font-mono` (`kb:warranty_v2026.03§2.1`, `SA-20931`). Customers never see raw ids | All |
| **InvestigationSteps** | What the AI did to reach the proposal, as steps, never as reasoning text | A table: step, LayerTag, tool, what was asked, what came back, where it was used; the decision gate as a row with its structured reason; "Đã loại trừ" rows naming the rule or source that ruled each possibility out. Never model reasoning text, reasoning tokens or the `analysis` field. Tokens and ms in the Demo stage only. Formerly ReasoningSteps | CSKH, Demo |
| **ValidationList** | Which gates the action passed | One row per check (customer verified, owner or can book, part matches VIN, technician certified, part reserved, slot locked, confirmation valid) with Đạt / Không đạt / Chưa kiểm. **Gap:** validator results are not exposed by the API | CSKH |

## 5. Decision components

| Component | Purpose | Anatomy and rules | Surfaces |
|---|---|---|---|
| **OptionCard** / **OptionList** | Choose between feasible options (UC3) | Radio-group semantics. Each option: workshop, date and time, distance, "Linh kiện có sẵn" / "Pin đủ đi tới" as text with icons, and its reason (`why`). Excluded options are listed after, muted, not selectable, with the reason ("Loại: …"). Data: `Option` | Customer, CSKH |
| **DecisionBlock** | Confirm a level-2 action | Heading ("Việc anh/chị cần làm"), a `dl` of every parameter (việc gì, xe with plate and short VIN, xưởng, ngày giờ, chi phí "theo báo giá xưởng" when unknown), the deadline, one primary button with a specific label ("Xác nhận đặt lịch"), a secondary "Chọn phương án khác", and the HelpAction. Changing any parameter resets confirmation (taste-rules rule 8, proposal §06). States: ready, locked ("Đang đặt lịch…", EXECUTING), confirmed (becomes a ConfirmationReceipt), failed (inline `--danger` message + "Thử lại"), expired ("Phương án đã hết hạn giữ chỗ" + "Tạo lại phương án") | Customer |
| **ConfirmationReceipt** | Proof that the server confirmed | `--ok` check + "Đã đặt lịch" + the confirmed parameters + id (`appointment_id`) + "Đổi lịch" and "Huỷ lịch". Appears only from a successful `ConfirmResult` | Customer, CSKH |
| **DecisionBar** | Staff decision on a case | The actions valid in the current state and for the employee's rights (cskh-screen-spec.md §6): "Nhận", "Nhận xử lý", "Gọi khách", "Chốt phương án", "Duyệt" / "Sửa rồi duyệt" / "Từ chối" (reason required), "Chuyển người khác", "Trả lại cho AI", "Thử lại", "Mở lại ca". One primary at a time; a missing right is stated in words with the way forward. Consequential actions open a Dialog with every parameter. Pinned to the bottom of the decision pane, or docked at the bottom of the case below `xl`. A server-driven change of its actions ignores clicks for `--dur-slow` and says what changed. **Gap:** only accept exists in the API (D-06, D-16) | CSKH |

## 6. Customer composites

| Component | Purpose | Anatomy and rules |
|---|---|---|
| **CareCard** | A case the system brings to the customer, which they can understand and act on | Full anatomy, variants and slots by state in [customer-screen-spec.md](../../docs/frontend/customer-screen-spec.md) §3. A **head** that answers four questions in the same words everywhere: what was detected (title), why you are receiving this (always visible, links to the opt-out setting), what the AI is doing (StateChip and one sentence), what you need to do (never empty: "Anh/chị chưa cần làm gì."). Then, in fixed order: what was checked (EvidenceList, collapsed), what is proposed (OptionList, reasons, options not chosen, "Điều em chưa biết"), your action (DecisionBlock and ActionScope, then the ConfirmationReceipt), the result (how it will be verified, then the verified outcome), who is responsible, HelpAction. Variants: full (C2), summary (C1), message (C6). One card per case; later states update it. The five required parts of spec §13 (what happened, options, deadline, owner, why) are all present |
| **ChatThread**, **ChatBubble**, **Composer** | The conversation | Customer bubbles right-aligned on `--sunken`; AI messages left with AIByline, on `--surface`; staff messages left with StaffByline. Streaming text appears as it arrives with a text-shaped skeleton before the first token; no typing dots. The composer stays reachable above the keyboard and never covers the focused message. Connection state per MASTER §11 |
| **JobCard** | One open job in "Việc của tôi" | Title, vehicle, StateChip, JourneyStepper, current appointment (date, time, workshop), owner ("Phụ trách: …"), the latest change with its reason and time ("Thay đổi gần nhất: …"), open promises (PromiseLine), actions ("Đổi lịch", HelpAction). Compact form on C1: a hairline-separated row, not a card (title, vehicle, StateChip, the state sentence, the next commitment, "Xem chi tiết"). Data: `Journey`. **Gap:** steps list and case state are not in `Journey` |
| **BottomNav** | The customer's top-level places on phones | Three items: "Việc" (`list-checks`), "Thông báo" (`bell`), "Xe" (`car`); icon above a one-line label at `--text-md`; current item `aria-current="page"` with an `--accent` indicator; the unread count sits in a fixed-width slot and is part of the link name in words ("Thông báo, 2 tin chưa đọc"), in neutral ink, never red. Only on C1, C4 and C5; from `md` up the same links sit in the AppHeader |
| **NotificationRow** | One sent message in "Thông báo" (C4) | Sender (compact AIByline, StaffByline, or "Bên em"), kind ("Tin tự động", "Cập nhật", "Nhắc lịch", "An toàn"), time; the title sentence, 600 with a "Mới" tag while unread; the "Vì sao anh/chị nhận tin này" line or the reason for the update; the case's current state in words. The whole row is one link to the case. Hairline-separated rows, not cards. **Gap:** no notifications endpoint (D-14) |
| **ActionScope** | What the assistant may do alone, and what needs a person | Three short lists from the confirmation levels (proposal §06 C): "Bên em tự làm" (read, report, remind), "Cần anh/chị xác nhận" (book, change or cancel an appointment, change workshop), "Cần nhân viên duyệt" (money, warranty conclusions, safety, identity). Per case on C2 ("Sau khi anh/chị xác nhận"), in full on C5 |
| **MemoryList** | What the assistant remembers about the customer (proposal §06 H) | One row per remembered item with "Sửa" and "Xoá" ("Xoá" confirms in a Dialog naming the item); a closing line on what is never stored. **Gap:** no endpoint (D-14) |
| **PromiseLine** | A commitment someone made | Who promised, what, by when ("Bên em sẽ nhắc trước 10 ngày"). Data: `Promise {made_by, text, due_at}`. A broken promise is shown, not hidden: `--danger` text with the new commitment |
| **OfferCard** | An optional suggestion | Same surface and border as any card; a "Vì sao gợi ý" line naming the data it is based on; "Bỏ qua" beside the accept button with equal size; price only from the API. No gradient, glow, badge, countdown or motion (taste-rules rule 9) |
| **HelpAction** | The way out | "Gặp nhân viên", a secondary button, in the same position on every screen and inside every CareCard. Never hidden in a menu, never disabled |

## 7. CSKH composites

| Component | Purpose | Anatomy and rules |
|---|---|---|
| **QueueList**, **QueueRow** | What needs attention, in order | Two lines of `--text-sm` per row, taller than `--target-min`, hairline separated, no cards (K-05). Line 1: marker (safety or overdue only, words and icon), customer, vehicle with VIN in `--font-mono`, DeadlineTimer. Line 2: StateChip (compact), one-line summary (full text in the accessible name), owner and presence. Fixed priority order (cskh-information-architecture.md §6); safety pinned in every view. Selected row: `--sunken` with a 2px `--accent` bar. New and re-ranked cases wait behind a "N ca mới" control; changed rows carry the change mark (K-03); rows never move under the pointer. Data: `Handoff[]`; every active case needs D-05 |
| **CaseFile** | Everything about one case, as a chain of causes | Sticky header: one-line summary (`h1`), StateChip, assignment, DeadlineTimer, SentimentTag, safety marker, presence, customer and vehicle, "Tiếp theo". A sticky section index. Ten sections on a vertical spine, one node per section in the node grammar (color only on the current one), always in this order and always expanded (K-10), each headed by its question with a plain first line: 1 Vì sao có ca này, 2 Hệ thống phát hiện gì, 3 Bằng chứng (EvidenceList), 4 AI đã điều tra gì (InvestigationSteps), 5 AI đề xuất gì (options with reasons and exclusions), 6 Chính sách cho phép gì (ActionPolicyTable), 7 Người cần quyết định gì, 8 Đã thực hiện gì, 9 Có hiệu quả không (VerificationMeter), 10 Nhật ký (AuditLog, last rows). A section with no data says so in one line; it is never removed. Full spec: cskh-screen-spec.md K4 |
| **HandoffCard** | The 10-second briefing | From the contract schema: `one_line_summary`; customer; goals done and pending; facts with sources; what the agent said or promised (`agent_said_promised`), visually prominent because staff must honor it; `sentiment`; `next_best_action`; `do_not` (shown as "Không nên", with `circle-slash` icons, never collapsed); `deadline_at` |
| **AuditLog** | The immutable record | Append-only rows: time, actor (LayerTag or staff name or customer or system), action, short input summary, result, link to evidence. No edit or delete affordances. Filters by actor. Ids in `--font-mono`. **Gap:** a case-level audit endpoint does not exist; `/trace/{trace_id}` covers one agent run |
| **SentimentTag** | How the customer feels, per the model | The word ("Bình tĩnh", "Lo lắng", "Bực", "Rất bực") with color per MASTER §11; a tooltip says it is a model estimate |
| **ActionPolicyTable** | What policy allows for each proposed action | One row per action: action and parameters, confirmation level, the policy or SOP and version it rests on, the validator (passes counted, every other check named), the verdict ("Được phép (mức 0 or 1)", "Cần khách xác nhận", "Cần nhân viên duyệt ({vai trò})", "Không được phép: {luật}" in `--danger`), and the action's current state. Verdicts are neutral text with icons (`shield-check`, `user-round`, `stamp`, `circle-slash`), never chips, so they are not confused with case states. **Gap:** verdicts and validator results are not in the API (D-06) |
| **FrictionTable** | Friction the system is handling across customers (K3) | One row per cluster: plain name and code, type, scope (customers, vehicles, appointments), cases by state in words, first and latest signal, contacts held back by arbitration with the reason. Real table with the cluster as row header. **Gap:** D-16 |
| **PresenceTag** | Who else is on this case | Text only: "Lan đang xem" (informational) or "Lan đang xử lý ca này từ 14:07" (locks actions for others; "Nhận thay" requires a reason and notifies). **Gap:** D-16 |
| **CopilotSuggestion** | A reply the AI suggests to staff (task C2.01) | Labelled "Trợ lý AI gợi ý", with its sources as SourceRefs; "Dùng gợi ý" inserts it into the composer for the employee to edit and send; it never sends by itself |
| **AlertSlot** | Safety and connection status without shifting panes (K-11) | A fixed-width region in the CSKH header: icon and words, `--danger` for safety and offline, `--attn` for reconnecting; safety wins, with "+1" for more; links to the case |

## 8. Landing composites

Landing renders real components as figures; these composites arrange them. Section by section use is in
[landing-story.md](../../docs/frontend/landing-story.md); motion in [landing-motion-map.md](../../docs/frontend/landing-motion-map.md).

| Component | Purpose | Anatomy and rules |
|---|---|---|
| **ComponentFigure** | Show the real product as illustration | A real component (CareCard, JobCard, HandoffCard, CaseFile section, CareTrace) rendered with fixture data, `inert`, inside a `figure` with a caption and a visible "Dữ liệu mẫu" label (L-07). Never a screenshot of a mock and never div drawings |
| **CounterfactualMark** | Show what reactive care would have looked like | Dashed `--border-strong` outline, `--muted` text, a label in words ("Nếu chờ khách hỏi", "Không cần gửi", "Chỉ có luật"); never interactive, never inside a ComponentFigure (L-08). Used on the S01 axis, the S02 track and the S06 rule-only outcome |
| **ShiftTimeline** | Reactive versus proactive on one time axis (S02, S03) | One axis; the reactive track (counterfactual) and the proactive track in the node grammar, colored by holder (L-09); a movable start marker; a "Chờ" span; the "Can thiệp" node opens into the four intervention types; a one-line legend. Vertical below `md` |
| **EngineSequence** | One signal through six stages (S04) | Stage navigation links; a six-node stage rail (color marks the present); a case packet that relabels per stage; one artifact panel showing a real component per stage; LayerTags on every stage. Compact and phone tiers: stages stacked with artifacts inline, no packet |
| **StoryChapter** | The UC1 story from both sides (S05) | A beats column beside two sticky figures (the phone at customer density, the console at compact density) and a shared clock label; the scenario label above. Compact and phone tiers: beats stacked with compact snapshots |
| **ContrastPair** | Rules detect, the agent reasons (S06) | Two columns divided by a hairline; a worked example as evidence rows with sources and connectors to two outcomes (rule-only as a CounterfactualMark, agent outcome solid); hover or focus emphasis only |
| **LayerSieve** | Each event stops at the cheapest tier (S07) | Four tiers (L0, L1, L2, Người) indented, not funnel-shaped; event chips as toggle buttons placed at their stopping tier with the reason in text; selection emphasizes a path. No percentages |
| **TrustGate** | What stops the AI from acting wrongly (S09) | A gate sequence in the node grammar (AI circle, Validator circle, decision diamond, execution circle, verified node) with a square branch to a person; a legend; a two-column ledger "Luôn có" and "Không bao giờ" |
| **SurfaceDoor** | Enter the product (S01, S08, S10) | One link per door with the fixed label; in S08 a one-line promise and a ComponentFigure (customer: CareCard summary of UC1; CSKH: the UC1 CaseFile header and sections 1 to 3), never an appointment as the opening image; in S01 and S10 a plain button-styled link; a quieter Demo stage link (D-09) |
| **ChapterLabel** | Where the reader is (header) | The current section name as plain text at `lg` and up; changes instantly; not announced |

## 9. Demo composites

| Component | Purpose | Anatomy and rules |
|---|---|---|
| **DemoPanel** | Drive the scripted world | Top bar with "Đặt lại", scenario buttons (from `contracts/events.yaml`), "Tua +2 ngày", "Tua +14 ngày"; a persistent "Chế độ demo" banner; follows CSKH rules. Data: `/events/inject`, `/clock/advance`, `/reset` |
| **AgentTrace** | Prove that most steps use no model | Collapsible table of `TraceStep` rows: step, LayerTag, tool, tokens, ms; totals at the end. CSKH rules |

## 10. Foundations

| Component | Rules |
|---|---|
| **Button** | Variants: primary (`--accent` fill, `--on-accent` text), secondary (`--border-strong` outline, `--fg` text), tertiary (text with underline on hover), danger (`--danger` fill, `--on-danger` text, destructive confirm only). Height `--control-h` (Customer primary `--control-h-lg`), `--radius-md`, label `--text-md` 600, one line at desktop, specific verb + object. Press: `--press-scale` over `--dur-press` (Customer and Landing only). Disabled: `--sunken` + `--muted`, with the reason stated next to it. Loading: locked, label changes, loader icon |
| **IconButton** | CSKH toolbars only; 44px target; Vietnamese `aria-label`; tooltip with the same words |
| **Link** | Real anchors for navigation; underlined in running text |
| **TextField**, **Select**, **Textarea** | Label above, hint below the label, error below the field with icon and words (taste-rules rule 7); correct `type`, `inputmode`, `autocomplete` (OTP: `one-time-code`, paste allowed); `--border-strong` border; never placeholder as label |
| **Checkbox**, **RadioGroup** | Label and control share one hit area of at least 44px |
| **SegmentedControl** | Used for the theme switch ("Sáng", "Tối", "Theo máy") and CSKH view filters; radio-group semantics |
| **Tabs** | Underline indicator in `--accent`; selection follows focus only when content is light; URL reflects the tab (web-design-guidelines) |
| **Disclosure** | The summary line says what is inside and how many ("Em đã kiểm tra 4 nguồn"); chevron rotates (Customer) or switches instantly (CSKH) |
| **Dialog** | For level-3 confirmations and destructive actions only; `--shadow-2`, `--radius-lg`, `--scrim`; focus trapped and returned; enters from `--enter-scale` with fade over `--dur-slow`, exits over `--dur-fast` |
| **Sheet** | Customer bottom sheet on phones for secondary content that must not leave the screen; `--ease-drawer`; swipe to close always has a "Đóng" button too (WCAG 2.5.7). The v0.3 customer screens keep options and evidence inline in the case and use no sheet |
| **Toast** | Transient confirmation of something also recorded on screen; `role="status"`; stays at least 5 seconds and pauses on hover or focus; never the only place important information appears |
| **Banner** | Persistent page-level status: connection, demo mode, safety. Safety banner: `--danger` bar with `--on-danger` text, `siren` icon, `role="alert"`, the pre-approved message and the 24/7 action |
| **Tooltip** | Supplementary only (glossary terms in CSKH); keyboard reachable; never the only source of required information |
| **Skeleton** | Shapes of the real content in `--sunken`; static, no shimmer |
| **EmptyState** | One sentence of explanation plus the next step (taste-rules rule 6) |
| **ErrorState** | What happened, in Vietnamese, and "Thử lại"; never "Oops", never a bare code |
| **SkipLink** | "Bỏ qua tới nội dung chính", first focusable element (taste-rules rule 14) |
| **AppHeader** | Product name (or, on pushed customer screens, a back link naming its destination), surface name, ThemeSwitch (Customer below `md`: in settings, C-06; CSKH: in the account menu, K-12), HelpAction (Customer, always at the right end); in CSKH also the five destinations, customer search and the AlertSlot (K-11); one line, at most 72px tall |

## 11. Shared components named in spec §21

| Spec name | This system |
|---|---|
| thẻ việc | JobCard |
| thanh tiến độ | JourneyStepper (domain progress) and CareTrace (AI state) |
| card handoff | HandoffCard |
| bong bóng chat | ChatBubble |
