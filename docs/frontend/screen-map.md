# Screen map

Which screens exist on each surface, what each is for, what it shows, and where its data comes from. Visual rules live in
[design-system/proactive-care/MASTER.md](../../design-system/proactive-care/MASTER.md) and the page files; journeys through these
screens are in [journeys.md](journeys.md). Data references are to `P-073/contracts/api.yaml` (v0.2.0); nothing here changes the contract.

## 1. Surfaces and the current spec

Spec §20 defines one demo page with four panels plus a trace. The owner brief of 2026-10-03 defines three surfaces. They reconcile as follows:

| Spec §20 panel | Surface in this map | Notes |
|---|---|---|
| Chat khách (điện thoại) | Customer: C6 Trợ lý AI, inside the customer app, which opens on C1 | Rendered in a phone frame inside the Demo stage. Home-first rather than chat-first (D-13) |
| Việc của tôi | Customer: C1 (home), with C2 and C3 for one case | Six-step JourneyStepper ("tiến độ 6 bước") in C2 "Tiến độ sửa chữa" |
| Console nhân viên | CSKH: K2 Hàng ưu tiên with K4 Chi tiết ca beside it | Handoff card, callback deadline, "Nhận", "Chốt phương án". The console adds K1, K3, K5 and K6 (D-15) |
| Demo panel | Demo stage: D1 | Follows CSKH page rules |
| Agent trace | Demo stage: D1 | Follows CSKH page rules |
| (not in spec) | Landing: L1 | New with the owner brief; spec §20 to be updated (open decision D-01) |

The Demo stage is a **composition**, not a fourth visual language: each region keeps the page rules of the surface it shows.

## 2. Navigation

```text
Landing (L1) ──► "Khám phá trải nghiệm khách hàng" ──► Customer tabs: C1 Việc của tôi ⇄ C4 Thông báo ⇄ C5 Xe của tôi
     │                                                    C1, C4, C5 ─► C2 Chi tiết việc ─► C3 Tiến trình xử lý
     │                                                    C1, C2 ─► C6 Trợ lý AI;  C4, C5 ─► C8 Cài đặt thông báo
     │                                                    C7 safety state can appear over any customer screen
     ├────────► "Khám phá trải nghiệm CSKH" ──────► CSKH: K1 Tổng quan ─► K2 Hàng ưu tiên + K4 Chi tiết ca; K3 Ma sát, K5 Khách hàng, K6 Nhật ký from the header
     └────────► "Xem cả hai phía cùng lúc" ► D1 Demo stage (DemoPanel, the customer app in a phone frame, K2 + K4 compact, AgentTrace)
```

Every customer screen carries "Gặp nhân viên" in the same place; every surface carries the theme switch and the skip link.

## 3. Landing

One long page, L1, in ten sections. The full specification (purpose, copy, structure, interaction, motion, responsive behavior,
accessibility, anti-patterns) is [landing-story.md](landing-story.md); motion is [landing-motion-map.md](landing-motion-map.md).
This table is only the inventory.

| ID | Section | Job | Key components | Motion |
|---|---|---|---|---|
| S01 | Mở đầu | "Đừng đợi khách hàng phải hỏi.": the help arrives before the question; the two doors | ComponentFigure (CareCard), CareTrace axis, CounterfactualMark, SurfaceDoor | None |
| S02 | Vấn đề | The reactive model: the customer starts everything and waits | ShiftTimeline (reactive state) | M1 |
| S03 | Chuyển dịch | Earlier start, burden on the system; the appointment is one intervention | ShiftTimeline (proactive state) | M1 |
| S04 | Bộ máy | One signal through six stages, with layer tags | EngineSequence | M2 |
| S05 | UC1 | The synthetic scenario from both sides | StoryChapter | M3 |
| S06 | Vì sao cần Agent | Rules detect, the agent reasons, people decide | ContrastPair | None |
| S07 | Dùng AI có chọn lọc | Not every event needs an LLM | LayerSieve | None |
| S08 | Hai trải nghiệm | Two doors with real previews | SurfaceDoor with ComponentFigures | Feedback only |
| S09 | Tin cậy và an toàn | What the AI does and does not do | TrustGate | None |
| S10 | Bắt đầu | One last choice | SurfaceDoor | Feedback only |

Door labels everywhere: "Khám phá trải nghiệm khách hàng", "Khám phá trải nghiệm CSKH"; Demo stage link "Xem cả hai phía cùng lúc" (D-09).

## 4. Customer

Full specification (purpose, hierarchy, actions, states, empty, loading, error, responsive behavior, accessibility) is
[customer-screen-spec.md](customer-screen-spec.md); the journey is [customer-journey.md](customer-journey.md); motion is
[customer-motion-map.md](customer-motion-map.md). This table is only the inventory.

| ID | Screen | Brief's IA item | Purpose | Key components | Live states | Data |
|---|---|---|---|---|---|---|
| C1 | Việc của tôi | Customer Home | Does anything need me, and is everything else in hand? | Status sentence, CareCard (summary), JobCard (compact), BottomNav | All, as chips and sentences | `GET /api/v1/jobs/{customer_id}` → `Journey[]`. **Gaps:** case state (D-04), "needs the customer" and deadline (D-14) |
| C2 | Chi tiết việc | Customer Active Care | One case in the brief's order, with the decision one tap away | CareCard (full), CareTrace (horizontal, condensed), EvidenceList, OptionList, DecisionBlock, ActionScope, ConfirmationReceipt, JourneyStepper, VerificationMeter, HelpAction | All | `ChatEvent`, `POST /api/v1/confirm`, `Journey`. **Gaps:** customer-screen-spec.md §3.5 |
| C3 | Tiến trình xử lý | Customer Journey | What happened, who did it, and why each step followed | CareTrace (vertical, full, with cause lines) | All, with history | `/trace/{trace_id}` covers one agent run. **Gap:** case-level timeline with actor, time and cause (D-06, D-14) |
| C4 | Thông báo | Notifications | Everything the system sent, each with why, each leading to its case | NotificationRow, update control | n/a (shows each case's current state) | Live `ChatEvent` stream only. **Gap:** notifications list and read state (D-14) |
| C5 | Xe của tôi | Vehicle and service context | The vehicle, its service record, and what the assistant knows and may do | Vehicle facts (`dl`), receipts, MemoryList, ActionScope, data-sharing switch | n/a | **Gap:** no vehicle, warranty, maintenance, consent or memory endpoint (D-14) |
| C6 | Trợ lý AI | (spec §20 "Chat khách") | Ask in one's own words, about a case or anything else | ChatThread, CareCard (message), DecisionBlock, Composer | INVESTIGATING (customer-started), RECOMMENDING, WAITING FOR CUSTOMER, EXECUTING, ESCALATED | `POST /api/v1/chat/stream`, `GET /api/v1/stream/{customer_id}`, `POST /api/v1/confirm` |
| C7 | Cảnh báo an toàn | (safety) | Safety, over every screen | Safety Banner, "Gọi cứu hộ 24/7", StaffByline once assigned | ESCALATED (safety) | Pushed through `/stream/{customer_id}`. **Gap:** no safety flag on `ChatEvent` (D-06) |
| C8 | Cài đặt thông báo | (proposal §09 right to refuse) | Turn AI-written proactive messages off (safety excepted); channel; theme on phones | Switches, SegmentedControl, ThemeSwitch | n/a | **Not in the contract or spec** (D-12) |

Every customer screen: "Gặp nhân viên" in the header, loading skeleton, empty state, error with "Thử lại", connection banner.
BottomNav ("Việc", "Thông báo", "Xe") on C1, C4 and C5 on phones.

## 5. CSKH

Full specification (purpose, hierarchy, actions, every state, empty, loading, error, responsive behavior, accessibility) is
[cskh-screen-spec.md](cskh-screen-spec.md); structure, action model and priority model are
[cskh-information-architecture.md](cskh-information-architecture.md); motion is [cskh-motion-map.md](cskh-motion-map.md).
This table is only the inventory.

| ID | Screen | Brief item | Purpose | Key components | Live states | Data |
|---|---|---|---|---|---|---|
| K1 | Tổng quan | Overview | The shift at a glance: what needs me, what was promised, what the AI is handling, what just finished | Tables of the first queue rows and promises due; counts by state as links | All, as counts and rows | Handoffs only. **Gaps:** counts by state, promises due, shift (D-05, D-16) |
| K2 | Hàng ưu tiên | Priority Queue | The ordered work list, with the open case beside it (three panes at `xl`) | QueueList and QueueRow, view menu ("Cần tôi xử lý" default, "Chờ duyệt", "Chờ khách xác nhận", "AI đang xử lý", "Đang xác minh", "Đã xong hôm nay"), update control, AlertSlot | All | `GET /api/v1/handoffs` → `Handoff[]`; `POST /api/v1/handoffs/{id}/accept`. **Gap:** every active case (D-05) |
| K3 | Ma sát đang diễn ra | Active Friction | Friction across customers that the system is already handling, and contacts it held back | FrictionTable, cluster detail with QueueRows | DETECTED to VERIFYING | **Gap:** clusters and suppressed candidates (D-16) |
| K4 | Chi tiết ca | Case Detail | The nine questions in order, on the spine, with the decision pane | CaseFile, EvidenceList, InvestigationSteps, ActionPolicyTable, ValidationList, VerificationMeter, AuditLog, HandoffCard briefing, DecisionBar, CopilotSuggestion, PresenceTag | All | `Handoff.card`, `GET /api/v1/trace/{trace_id}`. **Gaps:** state, signals, verdicts, validator results, actions, verification, staff actions (D-04, D-06, D-16) |
| K5 | Khách hàng | Customers | Find a customer and see vehicles, rights, open cases, promises and consents | Search, results table, profile sections | n/a | **Gap:** search and profile with access logging (D-16) |
| K6 | Truy vết và nhật ký | Trace / Audit | The immutable record and the AI runs | AuditLog, TraceStep table, LayerTag | n/a | `/trace/{trace_id}` covers one agent run. **Gap:** case-level audit (D-06) |
| K7 | Phím tắt | (keyboard) | The shortcut list and the switch to turn shortcuts off | Dialog | n/a | Local setting |

The ten K4 sections answer the brief's nine questions in order (why the case exists, what was detected, evidence, investigation,
proposal, what policy allows, what a person must decide, what happened, whether it worked) plus the audit (components.md §7).

## 6. Demo stage

| ID | Screen | Composition | Rules |
|---|---|---|---|
| D1 | Sân khấu demo | Spec §20 layout: DemoPanel across the top; the customer app in a phone frame (opens on C1; C2 and C6 reachable); beside it, C3 for the active case in place of the separate "Việc của tôi" panel (proposal, D-13); K1 in compact form; AgentTrace collapsible at the bottom | Each region follows its own surface's page file; one theme for the whole page; "Chế độ demo" banner; all data from `contracts/fixtures/demo_world.yaml` and marked "Dữ liệu mẫu". Data: `POST /api/v1/events/inject`, `POST /api/v1/clock/advance`, `POST /api/v1/reset`, `GET /api/v1/trace/{trace_id}` |

## 7. Proposed routes

Proposed only; final routes are an implementation decision for the frontend owner.

| Route | Screen |
|---|---|
| `/` | L1 Landing |
| `/khach` | C1 Việc của tôi |
| `/khach/viec/:journeyId` | C2 Chi tiết việc (sections have anchors, customer-screen-spec.md C2) |
| `/khach/viec/:journeyId/tien-trinh` | C3 Tiến trình xử lý |
| `/khach/thong-bao` | C4 Thông báo |
| `/khach/xe`, `/khach/xe/:vin` | C5 Xe của tôi |
| `/khach/tro-ly` (`?viec=:journeyId` with a case) | C6 Trợ lý AI |
| `/khach/cai-dat` | C8 Cài đặt thông báo |
| `/cskh` | K1 Tổng quan |
| `/cskh/hang` | K2 Hàng ưu tiên (view, filters and open case in the query string: `?xem=can-toi&ca=:caseId`) |
| `/cskh/ma-sat`, `/cskh/ma-sat/:clusterId` | K3 Ma sát đang diễn ra |
| `/cskh/ca/:caseId` | K4 Chi tiết ca as its own view |
| `/cskh/khach`, `/cskh/khach/:customerId` | K5 Khách hàng |
| `/cskh/nhat-ky` (`?ca=:caseId`) | K6 Truy vết và nhật ký |
| `/demo` | D1 Sân khấu demo |

## 8. Out of scope for v1.0

Manager dashboard ("Dashboard quản lý", taste-rules rule 13), technician copilot and the insights agent (proposal PL-C) are not designed
here. When they are, they start from MASTER and add their own page file; the manager dashboard would most likely follow CSKH rules.
