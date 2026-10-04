# Design review

| | |
|---|---|
| Role | Design Director review of the whole design package |
| Date | 2026-10-03 |
| Scope | Every file in `design-system/proactive-care/` (MASTER, nine detail files, three page files) and the eleven design documents in `docs/frontend/` (governance, screen map, journeys, landing story, landing motion map, the three customer and the three CSKH documents) |
| Surfaces | Landing, Customer, CSKH (and the Demo stage, which composes them) |
| Method | Seven checks from the review brief. Mechanical checks: the design-system validator (11 checks), contrast recomputed from `tokens.md`, searches for banned aesthetics and vocabulary drift. Judgement checks against the pinned skills in their roles: taste-skill (anti-patterns), emil-design-eng (motion review checklist and team rules), web-design-guidelines (`references/command.md`, the accessibility authority) |
| Verdict | **Approved with changes.** The package reads as one product with three clearly different jobs. Twenty-eight changes were required; all are applied in this review. What remains are owner actions outside design (§B.2). MASTER is now v1.0, the design contract |

**Authority.** Sections D to H are restated as binding text in [MASTER](../../design-system/proactive-care/MASTER.md) §18. If this
document and MASTER ever differ, MASTER wins. This document is the record of why.

| Check | Verdict | Required changes |
|---|---|---|
| 1. Visual consistency | Pass after changes | R-01 to R-06 |
| 2. Purpose differentiation | Pass | None |
| 3. AI language | Pass | None (the motion lines of the states are in check 6) |
| 4. Proactive product story | Pass after changes | R-07 to R-11 |
| 5. Generic AI aesthetic | Pass after changes | R-12 |
| 6. Motion | Pass after changes | R-13 to R-17 |
| 7. Accessibility | Pass after changes | R-18 to R-27 |
| Truth (found during review) | Pass after changes | R-28 |

---

## A. PASS

**1. Visual consistency.** One product across the three surfaces:
- **Typography.** Be Vietnam Pro only, 400 and 600, self-hosted; monospace only for identifiers; no uppercase anywhere; floors of 14px
  (16px on Customer); display sizes only on Landing (L-03); CSKH caps headings at `--text-2xl` (K-04). No surface document names another
  typeface, weight or italic.
- **Spacing.** One 4px scale and three density modes (airy, comfortable, compact) chosen by the dials; 44px targets on every surface,
  including the compact console.
- **Color semantics.** Ink for people and action, teal only for the AI, amber only when a person must decide, green only for what a
  system of record confirmed, red for failure and safety; color marks the present on all three surfaces. Warranty eligibility is
  neutral everywhere. 27 recorded text pairs and 12 non-text pairs pass AA in both themes, plus the 13 pairs added by R-02.
- **Icons.** lucide only; the nine state icons are identical on every surface; the banned AI icons (sparkles, wand, robot, brain,
  orb) appear only in bans; action icons always carry a label, except CSKH toolbars.
- **Status language.** Customer documents use only the Customer labels and CSKH documents only the CSKH labels (searched both ways:
  no crossover). Status is always shape, icon and word.
- **Component shapes.** One radius scale (4, 6, 8, full), no pills, no container above `--radius-lg`; the five node shapes mean the
  same on the Landing diagrams, the customer timeline and the CSKH case spine.
- **Borders and shadows.** Hairlines before boxes everywhere; shadows only on floating layers; dark theme replaces shadows with borders.
- **Personality.** "Calm instrument, human hand" holds on each surface: evidence and timestamps beside every claim, named people,
  plain Vietnamese, no mascot or magic.

**2. Purpose differentiation.** The surfaces share a language, not a layout:

| | Landing | Customer | CSKH |
|---|---|---|---|
| Job | Story, explanation, persuasion | Clarity, trust, action | Speed, evidence, operations |
| Dials | 7 / 8 / 3 | 5 / 5 / 4 | 3 / 2 / 8 |
| Shape | Ten narrative sections, asymmetric, one idea per screen | Home-first, one column, one task per screen, sticky action | Fixed panes, real tables, everything expanded |
| Disclosure | The page teaches the trace | Summary first, details on demand | All sections expanded (K-10) |
| Motion | Scroll-scrubbed choreography (pending A-02) | One short cue for each witnessed change | Change cues only; own actions never move |
| What the Care Trace does | Explains the mechanism | Tells the customer's case with causes | Structures the case file as a spine |

None of the surfaces borrows the other's layout: Landing has no product chrome, Customer has no tables, CSKH has no cards.

**3. AI language.** The nine states are defined once (MASTER §12.1 and §12.2), with one overview row and one detail block each, and
used unchanged everywhere: the same names, both label sets, the same shapes, icons and color families. Completed steps on the customer
timeline have their own forms (MASTER §12.4). The CSKH brief's "Allowed" is kept out of the state set and expressed as an
authorization verdict, a separate neutral vocabulary (cskh-information-architecture.md §5), so no state is redefined. Transitions
(§12.3) are consistent with every journey.

**4. Proactive product story.** Landing makes the story explicit: S03's key line "Lịch hẹn không phải điểm bắt đầu. Nó chỉ là một
trong các cách can thiệp.", the four intervention types, and S04, where investigation explains why this case needs a workshop. The
customer timeline starts at the vehicle's signal and ends at verification, and closing a ticket is never "done". Remote-first (J7)
and charging advice (J4) show interventions that are not appointments. After R-07 to R-11 no opening image, journey title or primary
example implies "appointment, then AI rescue".

**5. Generic AI aesthetic.** No gradient, glass, glow, orb, particle field, neon or AI dashboard appears in any specification; every
mention of them is a ban (MASTER §17, color.md §5, landing-story §5). The CSKH Overview is counts in rows, not KPI tiles or charts.
Cards appear only where an object asks for action (after R-12).

**6. Motion.** Every surface uses one catalogue (motion.md §2); durations stay at or below `--dur-slow` (250ms, under emil's 300ms);
enters ease out and exits are faster; nothing starts from scale 0; popovers grow from their trigger and dialogs stay centered; hover
motion is gated to fine pointers; only transform and opacity move; repeatable motion uses transitions; the EXECUTING loader is the
only loop; reduced motion has a complete replacement on every surface; Landing sequences are scroll-scrubbed, reversible and static
first. Performance: no layout reads during scroll, compositor-only properties.

**7. Accessibility.** WCAG 2.2 AA plus team floors throughout; skip link on every page; landmarks and one `h1` per page; real
tables in CSKH and `dl` on Customer; state never by color alone; focus visible, never obscured, trapped and returned in dialogs;
announcements polite, atomic and batched, safety as `role="alert"`; 320px reflow and 200% zoom on every surface including CSKH;
targets 44px; consistent help ("Gặp nhân viên") in one place; no time limits on customer input; deadlines in words.

## B. CHANGES REQUIRED

### B.1 Design changes (all applied in this review)

| ID | Check | Where | Finding | Change applied |
|---|---|---|---|---|
| R-01 | 1 Color | color.md §5 | An outlined control on a state tint fails 3:1 in dark theme (`--border-strong` on `--attn-surface`: 2.87) | Rule: no outlined control on a state tint; an action in a tinted or filled banner is a filled `--surface` button with `--fg` text |
| R-02 | 1 Color | color.md §6 | The Customer and CSKH specifications introduced 13 pairs (state text and indicators on `--sunken` selected rows, the BottomNav and selection bars, nodes on `--surface`) that the record did not cover | Computed from `tokens.md` and recorded; all 13 pass in both themes. The disallowed pair of R-01 is recorded too |
| R-03 | 1 Icons | components.md §6, customer-screen-spec.md §2 | The customer BottomNav icons were unnamed | "Việc" `list-checks`, "Thông báo" `bell`, "Xe" `car` |
| R-04 | 1 Voice | content.md §1 | CSKH copy says "Của bạn", "Chờ bạn" while content.md said CSKH uses no pronoun | "bạn" allowed in CSKH only to say who owns or must act |
| R-05 | 1 Spacing | tokens.md §9 | Three layout thresholds lived only in prose (600px short viewport, the 1024 by 700 Landing tier, the 520px case pane) | Named in tokens.md §9 |
| R-06 | 1 Components | landing-story.md S01 | The hero CareCard predated the customer card anatomy and named no variant | The summary variant: the four-question head |
| R-07 | 4 Story | journeys.md J1 | Titled "proactive rescue … to a confirmed booking", and "done when the appointment is confirmed" | Retitled "from signal to intervention"; the journey ends at the confirmed intervention, says the booking follows from the investigation, and states the case is done only after verification |
| R-08 | 4 Story | landing-story.md S08, components.md §8 | Both door previews opened on appointments: a JobCard at "Chờ hẹn" and the J2 handoff about a disrupted booking | Customer door: the UC1 CareCard summary. CSKH door: the UC1 case header and sections 1 to 3, with a signal-first door line. LQ-4 updated |
| R-09 | 4 Story | cskh-screen-spec.md K3 | The Active Friction example led with a parts cluster described by the appointment it affects | Examples reordered signal first; the parts cluster is described as a cause with appointments affected |
| R-10 | 4 Story | cskh-screen-spec.md K4 §1 | The J2 example began at the disrupted appointment; the link back to the vehicle signal was a field among others | Section 1 opens with the origin chain from the first system signal to now |
| R-11 | 4 Story | MASTER §0 | The story was argued on Landing but not stated as a rule | MASTER §0 states it and §18 freezes it |
| R-12 | 5 Aesthetic | customer-screen-spec.md C1, components.md JobCard | Customer Home boxed every case, so the one case asking for action did not stand out | Only cases under "Việc cần anh/chị" are cards; cases in progress and resolved cases are hairline rows |
| R-13 to R-17 | 6 Motion | See §B.1.1 | | |
| R-18 | 7 Hierarchy | cskh-screen-spec.md K2, accessibility.md §9 | The CSKH workspace could carry two `h1` (view heading and case summary) | One `h1` per page: the open case's summary, or the view heading with no case open; side panes start at `h2` |
| R-19 | 7 Focus | accessibility.md §9 | No `scroll-margin-top` for headings reached by anchors or section indexes under sticky chrome | Required on Customer C2, CSKH K4 and Landing anchors |
| R-20 | 7 Focus | accessibility.md §9 | `:focus-visible` and `:focus-within` unspecified | Ring on `:focus-visible`; compound controls use `:focus-within` |
| R-21 | 7 Responsive | accessibility.md §9 | Zoom was never explicitly protected | Never `user-scalable=no` or `maximum-scale`; inputs at least `--text-md` |
| R-22 | 7 Theming | accessibility.md §9 | No `theme-color` meta; native select colors unspecified for Windows dark mode | `theme-color` equals `--bg` of the active theme; selects set explicit colors |
| R-23 | 7 Semantics | accessibility.md §9 | Identifiers could be garbled by automatic translation | `translate="no"` on VINs, codes, ids, tool and rule names, the product name |
| R-24 | 7 Performance and semantics | accessibility.md §9 | Spec §21 virtualizes the console list, with no rule for keeping it accessible | `content-visibility: auto` first; if virtualized, `aria-setsize` and `aria-posinset`, keyboard movement across unrendered rows, the selected row never unmounted |
| R-25 | 7 Forms | accessibility.md §9 | Unsent text could be lost on navigation | Drafts kept per case; leaving the app with unsent text asks first |
| R-26 | 7 Forms | accessibility.md §9, cskh-screen-spec.md §1 and K5 | Spellcheck on codes, placeholder style and error focus unspecified; the search placeholder lacked "…" and an example | Spellcheck off for VINs, plates, codes and search; placeholders end with "…" and show an example; focus moves to the first error on submit |
| R-27 | 7 Touch | accessibility.md §9 | `touch-action` and tap highlight unspecified | `touch-action: manipulation`; tap highlight replaced deliberately by focus and pressed styles |
| R-28 | Truth | cskh-screen-spec.md K4 ActionPolicyTable | The example had the AI propose a "mức trung bình" compensation for J2, which proposal §09's table classes as "nhẹ", and the AI may not pick a tier | The basis now reads: beyond "nhẹ" needs approval and the AI does not choose the tier |

#### B.1.1 Motion changes (emil-design-eng review format)

| ID | Before | After | Why |
|---|---|---|---|
| R-13 | Customer: DecisionBlock values crossfade over `--dur-fast` when an option changes | Values change instantly; only the option's own selection color transitions | The parameters being confirmed must never be half-faded (emil-design-eng team rule: no animation on confirmation parameters) |
| R-14 | Customer: disclosure chevron and switch thumb animate whatever the input | Pointer only; keyboard instant; an overlay opened from the keyboard appears by opacity only (motion.md principle 2) | "Keyboard-initiated actions never animate" was not applied consistently |
| R-15 | MASTER §12: the motion lines of DETECTED, INVESTIGATING, RECOMMENDING, VERIFYING and RESOLVED described Customer only | Each line names its Customer and CSKH behavior; motion.md §3 states how K-03 applies | MASTER contradicted K-03 by omission |
| R-16 | CSKH: the update control "fades in", with no catalogue row and not in K-03's list | Catalogue row "Update control"; K-03 lists it | "Anything not listed does not move" (motion.md §2) |
| R-17 | CSKH: applying the update control could fade dozens of rows at once | More than six changed elements in one update: static "Vừa đổi" marks only | Performance and noise; the same cap as `--stagger` |

### B.2 Owner actions (outside design; not blocking the contract except where stated)

| ID | Action | Owner | Effect until done |
|---|---|---|---|
| O-1 | Merge or revise amendments A-01 and A-02 to `taste-rules.md` (D-02) | Frontend owner | Landing opening (L-01) and narrative motion (L-02) stay blocked; the page ships static |
| O-2 | Confirm the three surface architectures in spec §20 and §21: Landing (D-01), Customer home-first (D-13), CSKH six screens (D-15) | Product owner | The design is frozen; the product requirement still describes the older panels |
| O-3 | Contract pull requests: case state (D-04), queue scope (D-05), component fields (D-06), customer fields (D-14), CSKH fields and actions (D-16) | B and D | Screens render only what the API returns; listed per screen |
| O-4 | Remaining decisions: D-03 (terminal state), D-07 (product name), D-08 (tabular figures), D-09 (public demo), D-10 (language), D-11 (dials after the first prototype), D-12 (opt-out settings) | Product and frontend owners | Placeholders as specified |
| O-5 | Sign MASTER v1.0 | Frontend owner (C) | Recorded as pending in MASTER's header |

## C. OPTIONAL IMPROVEMENTS

| ID | Improvement | Why |
|---|---|---|
| OI-1 | Make the first Playwright screenshots a Care Trace set: every node state at three densities in both themes | It is the signature element and the one most likely to drift between surfaces |
| OI-2 | One glossary for system terms, used by CSKH tooltips (K-06) and Landing glosses (L-06) | Two surfaces explain the same terms; one source keeps them identical |
| OI-3 | Name the remaining action icons (search, filter, call, message, note) in components.md | Completes the icon map before implementation starts |
| OI-4 | Decide CQ-6 (no preselected option) and CQ-7 (how long resolved cases stay on Home) from the five user sessions (task C2.12) | Both are behavior questions best answered with observation |
| OI-5 | A print style for the CSKH case file in its section order | Complaints and audits often need a paper or PDF record |
| OI-6 | Plan line lengths for an English Landing (D-10) before copy freeze | Display type at two lines behaves differently in English |
| OI-7 | A "Tới bước hiện tại" link on long customer timelines (UC6 cycles) | Saves scrolling on phones when a case has repeated |
| OI-8 | Put the motion map IDs into the PR template | Reviewers can tick moments instead of re-reading the maps |
| OI-9 | Use `@starting-style` for enter transitions where supported | Enter motion without script, as the emil-design-eng wrapper suggests |

## D. DESIGN DECISIONS TO FREEZE

Frozen from v1.0. A frozen decision changes only through the governance change process with both the frontend owner and the product
owner agreeing, and a MASTER version bump (MASTER §18.5).

| # | Decision | Source |
|---|---|---|
| F-01 | The idea: proactive care made visible and accountable; personality "calm instrument, human hand"; the Care Trace as the one signature element | MASTER §0, §2 |
| F-02 | The story: system signal, detection, investigation, intervention, verification. An appointment is one intervention, never the starting point or the opening image | MASTER §0 |
| F-03 | Precedence: product requirements, then the internal design system, then taste-skill, ui-ux-pro-max, emil-design-eng, web-design-guidelines | design-governance.md §2 |
| F-04 | Dials: Landing 7/8/3, Customer 5/5/4 (the MASTER default), CSKH 3/2/8 | MASTER §2.1 |
| F-05 | Typography: Be Vietnam Pro 400 and 600, self-hosted; mono for identifiers only; no uppercase; display line height at least 1.15; floors 14px and 16px on Customer; Customer body 18px | MASTER §3, typography.md |
| F-06 | Color roles: mineral neutrals; ink for people and action; teal only for the AI; amber only when a person must decide; green only for system-of-record confirmation; red for failure and safety; color marks the present; no gradient, glow, glass or pure black | MASTER §4, color.md |
| F-07 | The token set, the contrast record and the layout thresholds | tokens.md, color.md §6 |
| F-08 | One spacing scale, three density modes, 44px targets everywhere | MASTER §5, spacing.md |
| F-09 | Radius 4, 6, 8, full; no pills; nothing larger than `--radius-lg` | MASTER §6 |
| F-10 | Hairlines before boxes; cards only for objects that ask for action; shadows only for floating layers | MASTER §7 |
| F-11 | lucide icons; fixed state icons; banned AI icons; a label on every action icon outside CSKH toolbars | MASTER §8 |
| F-12 | The node grammar: circle AI or system, diamond a person must decide, square a named person, check verified, triangle failure or safety | MASTER §9 |
| F-13 | The nine states: names, both label sets, shapes, icons, families, transitions, completed forms; journey step and AI state as two axes; authorization verdicts as a separate vocabulary | MASTER §12, cskh-information-architecture.md §5 |
| F-14 | Mandatory labels ("Trợ lý AI", "Tin tự động", "Vì sao anh/chị nhận tin này", "Gặp nhân viên", "Dữ liệu mẫu") and the voice "anh/chị, bên em" | MASTER §14, content.md |
| F-15 | Interaction patterns: summary first (Customer) and everything expanded (CSKH); confirm with parameters; honest progress; help in one place; deadlines not countdowns; explain on demand | MASTER §10 |
| F-16 | The proactive care card: the four-question head with a "Việc của anh/chị" line that is never empty, then the brief's order | customer-screen-spec.md §3 |
| F-17 | The case file: the nine questions plus the audit, on a spine, in fixed order | cskh-screen-spec.md K4 |
| F-18 | The CSKH priority model and the rule that nothing reorders under the pointer | cskh-information-architecture.md §6 |
| F-19 | The motion rules (§G) and the accessibility rules (§H) | motion.md, accessibility.md |
| F-20 | The architectures: Landing S01 to S10; Customer C1 to C8; CSKH K1 to K7 (product confirmation pending, O-2) | screen-map.md |
| F-21 | Illustration policy: real components with fixture data labelled "Dữ liệu mẫu"; no stock, no generated images, no decorative SVG | MASTER §9 |

Not frozen: copy wording within content.md's rules, sample data, open decisions D-01 to D-16, and anything marked as a gap.

## E. COMPONENTS THAT MUST BE SHARED

One implementation each, in P-073 `frontend/`, reading density from its container (components.md §1). A surface-specific copy of any
of these is a defect.

| Component | Landing | Customer | CSKH | Demo |
|---|---|---|---|---|
| TraceNode, CareTrace | Figures and diagrams | Timeline, condensed strip | Case spine, queue preview | Yes |
| StateChip | Figures | Yes | Yes (compact) | Yes |
| JourneyStepper | Figures | C2 "Tiến độ sửa chữa" | Case file | |
| VerificationMeter | S04, S05 figures | C2, C3 | Section 9 | Yes |
| LayerTag | S04, S07 | Never | Sections 4, 10, K6 | AgentTrace |
| AIByline, StaffByline | Figures | Yes | Yes | Yes |
| EvidenceList, SourceRef | S04 | Collapsed, source names only | Expanded, with raw references | Yes |
| InvestigationSteps | S04 artifact | Never | Section 4 | Yes |
| ValidationList | S04 artifact | Never | Section 6 | Yes |
| OptionCard, OptionList | Figures | C2, C6 | Section 5 (table form) | Yes |
| DecisionBlock, ConfirmationReceipt | S04, S05 figures | C2, C6 | Receipt in section 8 | Yes |
| PromiseLine | | C1, C2 | K1, K5, briefing | |
| CareCard | S01, S04, S05, S08 figures | Full, summary, message | | Phone frame |
| JobCard | | C1 (compact rows) | | Phone frame |
| CaseFile | S05, S08 figures | | K4 | Compact |
| HandoffCard | | | Decision pane briefing | Yes |
| QueueRow | S05 figure | | K2, K3 detail, K5 | Compact |
| Foundations: Button, Link, TextField, Select, Textarea, Checkbox, RadioGroup, SegmentedControl, Tabs, Disclosure, Dialog, Banner, Tooltip, Skeleton, EmptyState, ErrorState, SkipLink, AppHeader, ThemeSwitch | Yes | Yes | Yes | Yes |

Single-surface by design (not shared): the Landing composites (components.md §8); Customer: BottomNav, NotificationRow, MemoryList,
HelpAction, Sheet, Toast; CSKH: DecisionBar, DeadlineTimer, AlertSlot, ActionPolicyTable, FrictionTable, PresenceTag, CopilotSuggestion,
SentimentTag, AuditLog (also in the Demo stage).

## F. PAGE-SPECIFIC EXCEPTIONS

The page files are the authority; this is the index. 27 deviations, each justified by its surface's audience or dial and bounded.

| Surface | ID | Exception | Status |
|---|---|---|---|
| Landing | L-01 | An opening section (hero) within strict bounds | Blocked until A-01 |
| | L-02 | Three scroll-scrubbed narrative sequences (M1, M2, M3) | Blocked until A-02 |
| | L-03 | Display type sizes | Active |
| | L-04 | Airy density | Active |
| | L-05 | Asymmetric layout families | Active |
| | L-06 | System terms shown with a gloss | Active |
| | L-07 | Real components rendered inert as figures | Active |
| | L-08 | Counterfactual elements, dashed and labelled | Active |
| | L-09 | Diagrams colored by holder, with a legend beyond two node kinds | Active |
| Customer | C-01 | Body text 18px | Active |
| | C-02 | Nothing below 16px | Active |
| | C-03 | 52px full-width primary action in a sticky bar on decision screens | Active |
| | C-04 | No data tables | Active |
| | C-05 | The conversation stays at the newest message for a reader already there | Active |
| | C-06 | Theme switch in settings on phones | Active |
| CSKH | K-01 | Compact density | Active |
| | K-02 | 14px data text | Active |
| | K-03 | Own actions never animate; server-driven changes get one opacity cue | Active |
| | K-04 | Strict pane grid; headings at most `--text-2xl` | Active |
| | K-05 | No cards | Active |
| | K-06 | System terms visible where audit needs them | Active |
| | K-07 | Single-key shortcuts | Active |
| | K-08 | Desktop-first | Active |
| | K-09 | Callback countdown for staff | Active |
| | K-10 | Everything expanded | Active |
| | K-11 | Header alert slot instead of banners | Active |
| | K-12 | Theme switch in the account menu | Active |

None of them touches an invariant (design-governance.md §7): safety and truth, legal labels, the nine states, tokens and typeface,
accessibility floors, both themes, the position of "Gặp nhân viên".

## G. MOTION RULES

1. **Motion explains a change.** Feedback, state change, spatial continuity, and on Landing the explanation of a sequence. Nothing decorates.
2. **Witnessed change only.** Nothing moves on load; a change that happened while the person was away is shown finished and marked in words.
3. **Frequency decides.** Frequent actions do not animate; keyboard-initiated actions get no feedback motion; overlays opened from the keyboard appear by opacity only.
4. **Confirmation never animates.** The parameters of a level-2 action change instantly; success appears only after the server confirms.
5. **Short and decisive.** At most `--dur-slow`; `--ease-out` to enter, `--ease-in-out` to move; exits faster than enters; never ease-in, bounce or elastic; never from scale 0.
6. **Transform and opacity only**, plus selection or hover color over `--dur-fast`; never `transition: all`.
7. **Interruptible.** Transitions for anything that can repeat; keyframes only for one-shot entrances.
8. **One loop.** The EXECUTING loader inside the locked button; under reduced motion a static icon.
9. **Per surface.** Landing: scroll-scrubbed choreography in three sequences, full tier only, static first (L-02, pending A-02). Customer: one beat of at most `--dur-base` per update, the focal element rises, one settle on a witnessed RESOLVED. CSKH: own actions never move; server-driven changes get one opacity cue; no settle (K-03).
10. **No cascades.** One update, one beat; at most six staggered items; more than six changed elements on CSKH get static marks.
11. **Nothing under the pointer moves.** Lists never reorder in place; alerts never shift panes; a server-driven change to CSKH decision buttons ignores clicks for `--dur-slow`.
12. **Urgency is never motion.** Safety, errors and overdue deadlines appear at once, in words; no pulse, shake or flash.
13. **Reduced motion is a full design.** Every movement becomes instant or a plain opacity change; every loop stops; Landing shows final states; CSKH cues become the static "Vừa đổi" mark.
14. **No libraries, no scroll listeners.** CSS transitions and keyframes, the Web Animations API, IntersectionObserver and scroll-driven animations only.
15. **Every movement is listed.** In motion.md §2 and the surface's motion map; anything not listed does not move.

## H. ACCESSIBILITY RULES

1. **Floor.** WCAG 2.2 AA plus the team floors, audited with the pinned web-design-guidelines rules and web-accessibility.
2. **Language and structure.** `lang="vi"`; skip link first; landmarks; one `h1` per page, including combined panes; headings in order.
3. **Semantics before ARIA.** Buttons for actions, links for navigation; real tables in CSKH, `dl` on Customer, lists for queues and timelines.
4. **Contrast.** AA in both themes for text (4.5:1) including muted, placeholder and disabled text, and 3:1 for controls, focus and nodes; no outlined control on a state tint.
5. **State.** Never by color alone: shape, icon and word together; deadlines and verdicts in words.
6. **Focus.** A visible ring on `:focus-visible` (and `:focus-within` for compound controls), never covered by sticky chrome; anchored headings carry `scroll-margin-top`; dialogs trap and return focus; live updates never move focus.
7. **Keyboard.** Every journey works without a pointer; single-key shortcuts only in CSKH regions, never in text fields, with a switch; no single key for consequential decisions.
8. **Targets.** At least 44px with 8px between, on every surface; the Customer primary action 52px.
9. **Text.** At least 14px, 16px on Customer; inputs at least 16px; never disable zoom; 200% zoom and 320px reflow without loss.
10. **Announcements.** One polite live region per screen; atomic, short and in words; batched on CSKH; streaming text announced once complete; safety as `role="alert"`.
11. **Forms.** Visible labels, never placeholder as label; correct type, inputmode and autocomplete; paste allowed; spellcheck off for codes; errors in words next to the field, focus to the first error on submit; drafts kept.
12. **Time.** No time limits on customer input; customers see absolute deadlines, never countdowns; toasts stay at least 5 seconds and pause on hover or focus.
13. **Help.** "Gặp nhân viên" on every customer screen in the same place; no dead ends.
14. **Theming.** Both themes complete; `color-scheme` and `theme-color` follow the theme; forced colors keep meaning through shape, icon and text.
15. **Identifiers.** `translate="no"` on VINs, codes, ids and the product name.
16. **Long lists.** `content-visibility: auto` first; virtualized lists keep set size, position and keyboard movement.
17. **Touch.** No gesture-only action; `touch-action: manipulation`; `overscroll-behavior: contain` in overlays.
18. **Test protocol.** accessibility.md §7 on every screen before review: axe at zero violations in both themes, keyboard-only run, screen readers per surface, zoom and reflow, reduced motion and forced colors, screenshots.
