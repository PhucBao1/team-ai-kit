# Frontend design governance

How the Proactive Care design language is owned, decided, changed and enforced. The language itself is in
[design-system/proactive-care/](../../design-system/proactive-care/MASTER.md); the skills that help produce it are described in
[skill-stack.md](skill-stack.md); screens and journeys are in [screen-map.md](screen-map.md) and [journeys.md](journeys.md).

## 1. What lives where

| Thing | Location | Owner |
|---|---|---|
| Product requirements | `docs/spec/` (§20 UI, §21 FE, §13 agent, §19 API), `docs/proposal/` (§06, §08, §09), task cards in `plan/tasks/`, `P-073/contracts/` | Product owner; contracts: B and D through PR + ADR |
| Team visual baseline (15 rules) | `skills/add-frontend-screen/references/taste-rules.md` | Frontend owner (C) |
| Design system | `design-system/proactive-care/`: MASTER, detail files, `pages/` | Frontend owner (C) |
| Governance, screens, journeys | `docs/frontend/` | Frontend owner (C) |
| Design skills (tools, not authorities) | `skills/{taste-skill,ui-ux-pro-max,emil-design-eng,web-design-guidelines}/`, pinned | Kit maintainer |
| Implementation | `P-073/frontend/` | Frontend owner (C) |

team-ai-kit is the source of truth for design. P-073 receives only the implementation; no design document is copied into it.

## 2. Precedence

```text
1. Product requirements           spec, proposal rules, task card, contracts, legal labels (Vietnam AI Law), safety rules
2. Internal design system         taste-rules.md (15 rules) + MASTER.md + its detail files + pages/<surface>.md
3. taste-skill                    Visual Art Director
4. ui-ux-pro-max                  Product UX and design-system architect
5. emil-design-eng                Motion Director
6. web-design-guidelines          Quality and accessibility auditor (reports, never decides)
```

- A higher level always wins. A lower level may propose a change upward only through a pull request a person approves.
- **Inside level 2**: `taste-rules.md` and MASTER are one layer; MASTER was written to comply with every taste rule. Where MASTER needs
  more than a taste rule allows, it is recorded as a pending amendment (§9) and **the taste rule keeps winning until the amendment is
  merged**. A page file may deviate from MASTER only as described in §7, and never from a taste rule without an amendment.
- No skill output, generated design system, or audit finding may silently override a higher level. When a suggestion is dropped
  for precedence reasons, the pull request says which suggestion and which rule won.
- Safety and truth rules (MASTER §1, principle 1) cannot be traded away by any level below 1.

## 3. Roles

| Role | Who | May | May not |
|---|---|---|---|
| Product owner | Team lead | Set product requirements, surfaces, audiences, the dials' starting targets | Change tokens or components directly without a design PR |
| Frontend owner | C | Approve MASTER, page files, tokens, amendments to `taste-rules.md`; final say on visual decisions within level 2 | Override product requirements or contracts |
| Reviewer | One other team member | Review design PRs for consistency and accessibility | Approve their own change |
| Visual Art Director | taste-skill | Propose Design Reads, dial values, typography and composition directions | Decide stack, fonts, colors outside tokens, motion details, audits |
| UX Architect | ui-ux-pro-max | Propose information architecture, flows, responsive structure, design-system drafts | Persist into `design-system/proactive-care/` (no `--persist`, no `--force` here); choose visual style or motion |
| Motion Director | emil-design-eng | Propose and review motion within motion.md | Add libraries, add motion to CSKH beyond K-03 |
| Auditor | web-design-guidelines (pinned) with web-accessibility | Report findings as `file:line` | Edit code, overturn a decision of a higher level (report "theo thiết kế" instead) |

## 4. Change process

| Change | Needs | Checks before merge |
|---|---|---|
| Token value | PR touching `tokens.md` and `color.md` §6 | Contrast re-run for every pair in color.md §6 in both themes; no hex outside `tokens.md` |
| New token, component, state or icon | PR touching MASTER or a detail file, with the reason | Name fits the grammar (MASTER §9, §12); no duplicate of an existing role |
| New or changed deviation | PR touching `pages/<surface>.md` | §7 criteria; the row has every column filled; the cited dial or audience actually justifies it |
| Dial value | PR touching MASTER §2.1, product owner and frontend owner agree | Every page deviation that cites the dial is re-checked |
| Amendment to `taste-rules.md` | PR by or approved by the frontend owner | The amendment text in §9 is applied verbatim or revised in the same PR; affected deviations change status to "Active" |
| Contract-dependent design (gaps in D-06) | A contract PR + ADR by B and D first (api.yaml header) | Design never invents a field the contract lacks |

Every merged change adds a line to the MASTER changelog. Versions follow MASTER §18.5. 1.0 is the design contract issued after the
design review of 2026-10-03; the frontend owner's signature is recorded in MASTER's header, and A-01 and A-02 gate only L-01 and L-02.

## 5. How the skills were used for v0.1

The skills are not loaded in sessions opened in team-ai-kit, so their pinned instructions were read directly, each in its role.

| Skill | Adopted | Rejected or overridden, and why |
|---|---|---|
| taste-skill | Design Read format; the three dials; anti-default discipline; **dropping the warm cream plus espresso palette** (its most common AI tell, which changed the palette to mineral); one accent, locked; cards only where elevation means something and none above density 7; one theme per page; opening-section discipline (bounds of L-01); at least four layout families; the AI-tells list (em dash ban in interface text, no div-built fake screens, no three equal cards, no scroll cues, no decorative dots, no fake-precise numbers) | "Avoid Inter, use Geist and similar" (team font is Be Vietnam Pro); tight tracking and `leading-none` display type (breaks Vietnamese diacritics); Next.js and RSC stack (team stack is Vite); Motion library and parallax (taste-rules rule 10); picsum and simpleicons (no runtime assets); "font-mono for all numbers" at high density (tabular figures instead, mono only for identifiers); "Lucide only on request" (team icon set is lucide); three-word CTA limit (taste-rules rule 8 asks for specific labels such as "Xác nhận đặt lịch") |
| ui-ux-pro-max | Landing skeleton (problem, solution, proof, call to action), with proof replaced by architecture and trust; progress indicators for multi-step work; submit feedback; label AI content; one atomic live status message; table handling at small widths; pre-delivery checks (both themes, focus, reduced motion, responsive widths) | Its generated design systems for both Landing and CSKH: "Hero + Testimonials" pattern (rule 15), "Organic Biophilic" style with 16 to 24px radii (excessive rounding), Lexend and Source Sans 3 from Google Fonts (rule 1), GSAP Flip and ScrollTrigger snippets (rule 10), a green and amber palette that collides with state semantics; toast auto-dismiss at 3 to 5 seconds (at least 5 seconds with pause here) |
| emil-design-eng | The decision framework (purpose, frequency, keyboard actions never animate); custom easing curves; durations under 300ms; exits faster than enters; stagger 30 to 80ms; never from scale 0; hover gated to fine pointers; CSS transitions for interruptibility; the review checklist | Springs and drag gestures (no use case that needs them); the "Initial Response" behavior (disabled in the wrapper) |
| web-design-guidelines | Its rule areas mapped to coverage in accessibility.md §8; it will audit implementations | Title Case, `autocomplete="off"`, CDN preconnect, 24px targets, hydration rules (team overrides in its wrapper) |

**v0.3, customer experience.** The same roles, applied to the customer brief:

| Skill | Adopted | Rejected or overridden, and why |
|---|---|---|
| ui-ux-pro-max (offline search, no persist) | Three to five bottom tabs (three chosen, so labels fit at 320px and `--text-md`); a stable slot for counts so badges never shift layout; contextual count announcements in words, not a bare number; error recovery with a next step and a help path; static skeletons that keep layout stable | Toast auto-dismiss after 3 to 5 seconds (at least 5 seconds with pause here); "Step 2 of 4" indicators (named steps, taste-skill §9.F) |
| emil-design-eng | The frequency framework as the basis of MOTION 5 (customer-motion-map.md §1); toasts enter and leave from the same edge; transitions rather than keyframes for anything that can repeat; never animate keyboard actions | "Can add delight" for rare moments, kept to one settle on RESOLVED (MASTER §12) |
| taste-skill | Dial values from MASTER §2.1 unchanged; no new visual elements; anti-patterns re-checked (no typing dots, no urgency badges, no fake-precise numbers) | None new |

**v0.4, CSKH console.**

| Skill | Adopted | Rejected or overridden, and why |
|---|---|---|
| ui-ux-pro-max (offline search, no persist) | Tables scroll inside their container rather than breaking the layout; contextual, atomic announcements for counts; essential text never truncated, with a full-detail path for anything that is; keyboard order equal to visual order | Bulk actions on cases (each decision needs its own evidence; KQ-8); "card layout" fallback for tables (K-05: no cards; stacked label and value rows instead) |
| emil-design-eng | The frequency framework as the basis of MOTION 2: the employee's own and keyboard actions never animate; transitions, not keyframes, for repeatable cues; no ease-in | Standard animation for "occasional" UI such as menus and popovers: instant here, because staff open them many times a shift (K-03) |
| taste-skill | DENSITY 8 rules: no cards above density 7, hairlines and panes; VARIANCE 3: fixed grids and fixed order | None new |

**v1.0, design review.** The review ([design-review.md](design-review.md)) used each skill in its role: taste-skill's anti-pattern
list for check 5; emil-design-eng's review checklist and its Before, After, Why format for check 6, plus the team rule that
confirmation parameters never animate; web-design-guidelines (`references/command.md`) as the accessibility authority for check 7,
which added accessibility.md §9. ui-ux-pro-max was not needed: the review changed no architecture.

## 6. Conformance checks for every implementation PR

- [ ] Tokens only: no hex, px, ms or curves that are not tokens; no new fonts, icon sets or UI libraries (taste-rules rule 15).
- [ ] The nine states use MASTER §12 labels, node shapes, icons and families; state never by color alone.
- [ ] Mandatory labels present where they apply (content.md §2).
- [ ] Loading, empty and error forms for every view (taste-rules rule 6).
- [ ] Level-2 actions show all parameters and never claim success before the server confirms.
- [ ] Motion only from the catalogue for that surface; reduced motion tested.
- [ ] Accessibility protocol (accessibility.md §7) run; axe zero violations in both themes.
- [ ] Screenshots at 390 by 844 (Customer) or 1280 wide (CSKH, Landing), both themes, attached to the PR through `review-pr`.
- [ ] `web-design-guidelines` audit on changed files; findings fixed or marked "theo thiết kế (<source>)".
- [ ] Any deviation from MASTER is already in the surface's page file; if not, stop and open a design PR first.

## 7. Deviation rules

A page file may deviate from MASTER only when all of these hold:

1. The deviation is justified by that surface's audience, task or dial, and the row says which.
2. It is bounded: the row states the limits that keep it inside the language.
3. It does not touch the invariants: safety and truth rules; legal and governance labels; the nine states (names, shapes, icons,
   families); tokens and the single typeface; accessibility floors; support for both themes; the position of "Gặp nhân viên".
4. It does not contradict a taste rule, or it is marked "Blocked" until an amendment is merged.

Format: one table, columns ID, MASTER rule, Default, On surface, Justification, Bounds, Status. Nothing else in a page file except
its header. Status is "Active" or "Blocked until amendment A-0n is merged".

## 8. Validation record, v1.0

Run on 2026-10-03 against every file in `design-system/proactive-care/` and the twelve `docs/frontend/` design documents (governance, screen map, journeys, landing story, landing motion map, customer journey, customer screen specification, customer motion map, CSKH information architecture, CSKH screen specification, CSKH motion map, design review). All pass. v1.0 re-ran every check after the design review applied its changes.

| Check | Result |
|---|---|
| Color values (hex, rgba) appear only in `tokens.md` | Pass |
| Every token referenced anywhere is defined in `tokens.md` | Pass |
| Dials in page headers equal MASTER §2.1, which is the single authority | Pass |
| Page files define no typeface, color or token | Pass |
| MASTER §12 has one overview row and one detail block for each of the nine states | Pass |
| Page files reference states but never redefine them | Pass |
| Page files contain only a header and one deviations table; every row cites a MASTER section or rule, a justification, bounds, and a valid status | Pass (27 deviations: Landing 9, Customer 6, CSKH 12) |
| Every deviation ID, amendment and open decision cited anywhere is defined | Pass |
| No em or en dash in any of these files | Pass |
| Relative links resolve | Pass |
| Contrast, recomputed from `tokens.md`: 27 text pairs at 4.5:1 and 12 non-text pairs at 3:1, both themes | Pass, 0 failures (color.md §6) |

Judgement checks, by review rather than script:

- **One visual language.** All three surfaces share the tokens, the typeface, the node grammar and the nine states with their labels,
  shapes, icons and color families, the radius scale, the border philosophy, the focus ring, the voice rules and the accessibility
  floors. The 27 deviations change only density, scale, motion amount, layout predictability, disclosure defaults, vocabulary
  exposure, control placement (Customer C-03, C-06; CSKH K-11, K-12), conversation scrolling (C-05), and on Landing the counterfactual and
  holder-colored diagrams; none touches an invariant listed in §7. The customer timeline's completed-step wording was added to MASTER
  §12.4 rather than to the page file, because state vocabulary is an invariant. The CSKH action model uses the nine states unchanged
  and adds authorization verdicts as a separate, neutral vocabulary, so no state is redefined.
- **Deviations justified.** Every deviation traces to an audience need or a dial in MASTER §2.1; two (L-01, L-02) are additionally
  blocked on amendments because they exceed a taste rule. Customer, the baseline, still has the fewest (6).

## 9. Pending amendments to taste-rules.md

Proposed text, ready to apply once the frontend owner approves. Until then the current rule wins and the deviation is blocked.

**A-01, rule 15** (unblocks L-01). Replace the second sentence of rule 15 with:
> Màn khách và console: không hero. Landing (trang giới thiệu): được một phần mở đầu theo `design-system/proactive-care/pages/landing.md` L-01 (vừa màn hình đầu, tiêu đề tối đa 2 dòng, đúng 2 lời mời "khách hàng" và "CSKH", hình minh hoạ là component thật có nhãn "Dữ liệu mẫu"). Mọi bề mặt: không sinh ảnh, không ảnh placeholder từ mạng, không "randomize" bố cục, không bịa ngày hay số liệu "trông thật", không logo wall, không testimonial.

**A-02, rule 10** (unblocks L-02). Append to rule 10:
> Ngoại lệ duy nhất: Landing được chuyển động kể chuyện gắn với vị trí cuộn (scroll-driven) theo `pages/landing.md` L-02 và `motion.md` §4: chỉ transform và opacity, chuyển động theo thời gian không quá 250ms, không parallax, không chiếm quyền cuộn, không lặp, không thư viện, tắt hoàn toàn khi `prefers-reduced-motion: reduce`.

Clarification, not blocking: rule 13 says the manager dashboard may be denser; the CSKH console's compact density (K-01) keeps every
floor in rules 2 and 7, so no amendment is needed. Mention it when rule 13 is next edited.

## 10. Open decisions

| ID | Decision needed | Why it matters | Owner |
|---|---|---|---|
| D-01 | Add the Landing surface to spec §20 (and to a task card) | Product requirements, level 1 of the precedence, are otherwise empty for Landing | Product owner |
| D-02 | Approve or revise amendments A-01 and A-02 | L-01 and L-02 are blocked until then; without them Landing is a static, headline-less page | Frontend owner |
| D-03 | A terminal state for cases that end without action (declined, expired, opted out). Proposal: CLOSED, neutral, hollow circle, "Đã đóng" | The nine states have no honest ending for these cases | Product owner |
| D-04 | Expose the case state in the contract (an enum of the nine states on `Journey` and `Handoff`) or define a deterministic mapping from existing fields | Today `current_step` and `Handoff.status` are free strings; the UI must not infer states | B and D (contract PR + ADR) |
| D-05 | CSKH queue scope: handoffs only (today's contract) or every active case | The "AI đang xử lý" and "Chờ duyệt" views need cases that are not handoffs | Product owner |
| D-06 | Contract gaps for the designed components: message author and origin (AI, staff, system, proactive) for the mandatory labels; a safety flag and a structured "why you received this" on messages; `steps`, case state, evidence and verification progress (phase, window, elapsed, recurrences) on `Journey`; layer, actor and timestamp on `TraceStep`; validator results; a case-level audit endpoint; approve, reject and finalize actions for staff; assignee display name for customers; the UC2 charging events | Each gap is marked in components.md and screen-map.md; components show only what exists until then | B and D (contract PR + ADR) |
| D-07 | Product name, logo, and any OEM brand use (written permission needed for marks) | Fills "{tên sản phẩm}" in the AI's introduction and the Landing opening | Product owner |
| D-08 | Confirm Be Vietnam Pro ships tabular figures in the self-hosted build; otherwise numeric columns use the mono stack | Columns of numbers must align | Frontend owner |
| D-09 | Whether the Demo stage is linked from the Landing doors and public | Judges benefit; a public demo control panel needs a "Chế độ demo" guard | Product owner |
| D-10 | Landing language: Vietnamese only, or an English version for non-Vietnamese judges and enterprise visitors | Copy, `lang`, and line lengths differ | Product owner |
| D-11 | Confirm or adjust the dial values after the first prototype review | They are starting targets (owner brief) | Product owner + frontend owner |
| D-12 | Customer notification and AI opt-out settings (screen C8) | Required by proposal §09 ("quyền từ chối"), absent from spec and contract | Product owner |
| D-13 | Home-first customer information architecture (C1 "Việc của tôi" as the hub, three tabs, the conversation reached in context) instead of spec §20's chat-first panel; update spec §20 and §21, the Demo stage layout and task cards C1.03, C1.04, C2.03 | Product requirements, level 1, still describe the chat as the customer's main panel | Product owner |
| D-14 | Customer-side contract gaps beyond D-06: a notifications list with kind, case link, anchor and read state; vehicle context (plate, warranty precheck, maintenance); data-sharing consent and assistant memory with edit and delete; per-case unknowns, excluded options with reasons, cause lines and the confirmation hold deadline; a "needs the customer" flag | C4, C5 and most of the care card can show only part of their design until these exist | B and D (contract PR + ADR) |
| D-15 | The six-screen CSKH console (K1 Tổng quan, K2 Hàng ưu tiên, K3 Ma sát, K4 Chi tiết ca, K5 Khách hàng, K6 Truy vết và nhật ký) instead of spec §20's single "Console nhân viên" panel; update spec §20 and §21, the Demo stage and task cards C1.06 and C2.01 | Product requirements, level 1, describe only the queue and handoff card | Product owner |
| D-16 | CSKH contract gaps beyond D-05 and D-06: friction clusters and suppressed candidates; overview counts and promises due; customer search and profile with access logging; presence and action locks; staff actions (call and call outcome, internal note, reassign, hand back to the AI, take over from the AI, reopen, staff message with templates, record a new request) | K1, K3, K5 and most staff actions can show only part of their design until these exist | B and D (contract PR + ADR) |

## 11. Design contract

The design contract is [MASTER §18](../../design-system/proactive-care/MASTER.md): frozen decisions (§18.1), shared components
(§18.2), surface exceptions (§18.3), what every implementation must do (§18.4) and how the contract changes (§18.5). It replaces the
twelve-point list that stood here before v1.0. The review behind it is [design-review.md](design-review.md).
