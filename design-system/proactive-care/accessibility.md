# Accessibility

Part of the Proactive Care Design System v1.0. Start at [MASTER.md](MASTER.md). The floor is WCAG 2.2 AA plus the team rules, which
are stricter in several places. Audits use the pinned skills `web-accessibility`, `web-design-guidelines` and `playwright-cli`.

## 1. Floors

| Topic | WCAG 2.2 AA minimum | This system |
|---|---|---|
| Target size (2.5.8) | 24 by 24px | `--target-min` (44px) both axes, `--target-gap` (8px) between targets; Customer primary `--control-h-lg` (52px) |
| Text contrast (1.4.3) | 4.5:1 | 4.5:1 in **both** themes, including placeholder and disabled text (color.md §6) |
| Non-text contrast (1.4.11) | 3:1 | 3:1 for control borders, focus ring, trace nodes and connectors in both themes |
| Text size | none | Nothing below `--text-sm` (14px); Customer nothing below `--text-md` (16px) |
| Resize (1.4.4), reflow (1.4.10) | 200%, 320px | 200% zoom without loss; 320px without horizontal page scroll on every surface, including CSKH |
| Use of color (1.4.1) | not the only means | Every state is shape plus icon plus word; color only speeds scanning |
| Language (3.1.1) | page language | `lang="vi"` on every page |

## 2. Criteria that shape this product

| Criterion | Design decision |
|---|---|
| 1.3.1 Info and relationships | Landmarks (`header`, `nav`, `main`, `aside`), one `h1` per screen, headings in order; CareTrace is an ordered list; DecisionBlock parameters are a `dl`; CSKH data uses real tables |
| 1.4.12 Text spacing | Layouts survive user overrides of line height, paragraph, letter and word spacing; no fixed-height text boxes |
| 1.4.13 Content on hover or focus | Tooltips are dismissible with Escape, hoverable, and persist until dismissed |
| 2.1.4 Character key shortcuts | Single-key shortcuts exist only in CSKH, can be turned off, and act only when focus is in the queue or case region (§6) |
| 2.2.1 Timing adjustable | No time limits on customer input. Expired confirmation tokens explain and offer "Tạo lại phương án". Toasts stay at least 5 seconds and pause on hover or focus |
| 2.2.2 Pause, stop, hide | Nothing autoplays or loops except the EXECUTING loader, which ends with the action |
| 2.4.1 Bypass blocks | "Bỏ qua tới nội dung chính" skip link on every page |
| 2.4.7 and 2.4.11 Focus visible, not obscured | `--focus` ring, `--focus-w` wide, `--focus-offset` away from the element, on every focusable element in both themes; sticky bars and the chat composer reserve scroll padding so they never cover the focused element |
| 2.5.3 Label in name | Accessible names start with the visible label ("Xác nhận đặt lịch, xưởng Gia Lâm, 09:00 thứ Bảy") |
| 2.5.7 Dragging movements | Every swipe or drag (sheet dismissal, any slider) has a button alternative |
| 3.2.6 Consistent help | "Gặp nhân viên" sits in the same place on every customer screen and in every proactive message |
| 3.3.1 to 3.3.3 Errors | Errors in words below the field with an icon, never color alone; say how to fix |
| 3.3.4 Error prevention | Level-2 actions show every parameter before confirming; level-3 actions go to a person; destructive actions confirm in a Dialog |
| 3.3.7 Redundant entry | Never ask for what the system already knows ("không hỏi lại") |
| 3.3.8 Accessible authentication | OTP fields accept paste and use `autocomplete="one-time-code"`; no cognitive puzzles |
| 4.1.3 Status messages | Live updates follow §3; errors and safety use `role="alert"` |

## 3. Announcements

Real-time updates arrive by server-sent events. Rules: never move focus, announce through one polite live region per surface, keep
each announcement atomic and short, and never announce token by token.

| Event | Politeness | Announcement |
|---|---|---|
| New proactive message | polite | "Tin mới từ Trợ lý AI: " plus the first sentence |
| Streaming AI reply | polite, once, when complete | The full reply is readable in the thread; nothing is announced while streaming |
| State change of the case in view | polite | "Trạng thái: " plus the state label (MASTER §12) |
| Action result | polite | "Đã đặt lịch: …" or the failure sentence |
| Form or action error | `role="alert"` | The error sentence |
| Connection reconnecting / lost | polite / `role="alert"` | "Đang kết nối lại…" / "Mất kết nối. Tin nhắn sẽ được gửi khi có mạng." |
| Safety | `role="alert"`, banner first in reading order (CSKH: the header alert slot, K-11) | The pre-approved safety message and the 24/7 action; focus is not moved |
| CSKH state change of the open case | polite, once | "Trạng thái: " plus the CSKH label; a change to the DecisionBar also states that clicks were paused |
| Customer unread count | polite, once per arrival | "Thông báo: 2 tin chưa đọc" (never a bare number) |
| Customer update control (C1, C4) | polite, once | "1 việc mới" / "1 thông báo mới" |
| CSKH new cases | polite, batched, at most once per 30 seconds | "2 ca mới" |
| CSKH deadline thresholds | polite | "Ca của Nguyễn Văn Minh: còn 5 phút để gọi lại" / "đã quá hạn" |

## 4. Component patterns for assistive technology

| Component | Pattern |
|---|---|
| CareTrace | `ol` with `aria-label` ("Tiến trình xử lý" / "Dòng thời gian"); current item `aria-current="step"`; shapes `aria-hidden`; each item reads state, actor, time |
| StateChip | Plain text; icon `aria-hidden`; not focusable unless it is a filter toggle |
| DecisionBlock | Region with heading; `dl` of parameters; the deadline in text; while executing, the region is `aria-busy` and the button label changes |
| OptionList | `radiogroup`; excluded options are listed as text after the group, not as disabled radios |
| EvidenceList | Disclosure button with `aria-expanded`; the summary names the count |
| VerificationMeter | The sentence carries the meaning; segments `aria-hidden` |
| DeadlineTimer | Text with the absolute time; minute updates are not announced except at thresholds (§3) |
| QueueList | A list of links or a table with row headers; `j`/`k` and arrow keys move within it; Enter opens the case and moves focus to its `h1`; each row's name holds the full summary, state, deadline and owner |
| CaseFile | `main` region with one `h1` (the summary) and ten `h2` sections in fixed order; the section index is a `nav` that names the current section in words; spine nodes are `aria-hidden` |
| ActionPolicyTable, FrictionTable | Real tables with column headers and the action or cluster as row header; verdicts and states read as words |
| DecisionBar (CSKH) | A region with a heading; `aria-busy` while executing; clicks are ignored for `--dur-slow` after a server-driven change of its actions, and the status line says so |
| AlertSlot (CSKH) | Fixed position in the header; safety uses `role="alert"` once; reconnecting is polite; the slot's link opens the case |
| AuditLog | A table with column headers; time cells carry the full date in the accessible name |
| ComponentFigure (Landing) | `figure` with `figcaption` describing what the figure shows; the component inside is `inert` and hidden from the accessibility tree, because the caption speaks for it |
| Dialog | `role="dialog"` with `aria-modal`, labelled by its heading; focus trapped; Escape closes; focus returns to the trigger |
| BottomNav (Customer) | `nav` named "Điều hướng chính"; links with `aria-current="page"`; the unread count is part of the link's name in words |
| NotificationRow (Customer) | Items of a `ul` under day headings (`h2`); each row is one link whose name starts with "Chưa đọc" while unread |
| CareCard head (Customer) | A `dl` of the four answers, directly after the `h1`; the condensed trace strip is `aria-hidden` |

## 5. Older customers and low vision

The Customer surface assumes some readers are elderly and on phones: body `--text-lg`, floor `--text-md`, primary action
`--control-h-lg` within thumb reach, one task per screen, absolute times instead of countdowns, no gesture-only actions, plain words, and
a human always one tap away. The same screens are checked at 200% zoom and with large system font settings.

## 6. CSKH keyboard model (with deviation K-07)

Shortcuts act only when focus is in the queue or the case regions and not in a text field; a "Phím tắt" switch turns them off; `?` opens
the list. Every shortcut also exists as a visible control.

| Key | Action |
|---|---|
| `j` / `k` | Next / previous case in the queue |
| `Enter` | Open the focused case |
| `g` then `o` / `q` / `f` / `c` / `a` | Go to Tổng quan / Hàng ưu tiên / Ma sát / Khách hàng / Nhật ký |
| `/` | Focus customer search |
| `n` | "Nhận" (accept) the open case |
| `1` to `9`, `0` | Jump to case file section 1 to 10 |
| `?` | Show shortcuts |

Decisions with consequences ("Duyệt", "Từ chối", "Chốt phương án") have no single-key shortcut.

## 7. Test protocol (every screen, before review)

1. Automated: axe through Playwright with the WCAG 2.0, 2.1 and 2.2 A and AA rule sets, zero violations, both themes.
2. Keyboard only: complete the screen's main journey without a pointer; focus always visible and never hidden.
3. Screen reader smoke test: NVDA with Chrome or Firefox (CSKH, Landing); VoiceOver with iOS Safari and TalkBack with Android Chrome (Customer).
4. Zoom and reflow: 200% and 320px wide; no loss, no horizontal page scroll.
5. Reduced motion and forced colors: all states still distinguishable; nothing loops.
6. Screenshots at 390 by 844, light and dark, with `playwright-cli`; diacritic test strings from typography.md §3 at the largest and smallest size.
7. Audit with `web-design-guidelines` (pinned rules, team overrides) and `web-accessibility`; findings recorded in the PR.

## 8. Coverage of the pinned web-design-guidelines rules

The auditor role checks implementations against `skills/web-design-guidelines/references/command.md`. This system already decides each area:

| Guideline area | Covered by |
|---|---|
| Accessibility, semantic HTML | §2, §4; components.md §10 |
| Focus states | §2 (2.4.7, 2.4.11); tokens.md §5 |
| Forms | components.md §10; content.md §5; §2 (3.3.x) |
| Animation | motion.md (reduced motion, transform and opacity, interruptible, no `transition: all`) |
| Typography (ellipsis, quotes, tabular numbers, balanced headings) | typography.md §2, §4, §5 |
| Content handling (long text, empty states) | components.md §1 rule 3; content.md §5 |
| Images | MASTER §9 illustration policy; figures have captions; any image has explicit dimensions |
| Performance (virtualized long lists, font preload) | spec §21 (virtualized console list); typography.md §1 |
| Navigation and state (URL reflects state) | components.md §10 Tabs; CSKH filters and the open case live in the URL |
| Touch and interaction | §1 targets; components.md §10 Sheet; `overscroll-behavior: contain` in sheets and dialogs |
| Safe areas and layout | spacing.md §3.2; MASTER §13 |
| Dark mode and theming | color.md §4; `color-scheme` matches the theme |
| Locale and i18n | typography.md §4 (`Intl`, `vi-VN`) |
| Hover and interactive states | components.md §10 Button; motion.md §2 |
| Content and copy | content.md. Team overrides: no Title Case (Vietnamese), specific action labels per taste-rules rule 8 |
| Hydration safety | Not applicable to the Vite single-page app |

## 9. Web interface rules added by the design review

The design review of 2026-10-03 ([design-review.md](../../docs/frontend/design-review.md) §B) audited this system against the pinned
`web-design-guidelines` rules and added these. They apply to every surface.

| Area | Rule |
|---|---|
| Anchored headings | Every heading reachable by an anchor or a section index has `scroll-margin-top` equal to the sticky chrome above it (header, CSKH case header and index), so a jump never lands under a sticky bar: Customer C2 sections, CSKH K4 sections, Landing anchors |
| Focus | The ring shows on `:focus-visible`, not on pointer focus; compound controls (OptionCard, radio cards, queue rows with inner links) show it with `:focus-within` |
| Heading hierarchy in panes | One `h1` per page even when panes are combined: in the CSKH workspace, the open case's summary, or the view heading when no case is open; side panes start at `h2` |
| Zoom | Never `user-scalable=no` or `maximum-scale`. Text inputs are at least `--text-md` on every surface, which also prevents automatic zoom on iOS |
| Theme | `color-scheme` matches the theme on `html`; `<meta name="theme-color">` equals `--bg` of the active theme; native selects set explicit background and text colors (Windows dark mode) |
| Identifiers | VINs, codes (`BATT-COOL-01`), appointment and reservation ids, tool and rule names, and the product name carry `translate="no"`, so automatic translation does not garble them |
| Long lists | The CSKH queue and audit tables render with `content-visibility: auto` first; if they must be virtualized (over about 200 rows), rows keep `aria-setsize` and `aria-posinset`, `j`/`k` move across unrendered rows, and the selected row is never unmounted |
| Drafts | Unsent text (the customer composer, CSKH messages, notes, decision reasons) is kept per case when the person navigates away; leaving the app with unsent text asks first |
| Fields | Correct `type`, `inputmode` and `autocomplete`; spellcheck off for VINs, plates, codes and customer search; placeholders end with "…" and show an example ("Tên, SĐT, biển số hoặc VIN…"); on submit with errors, focus moves to the first error |
| Touch | `touch-action: manipulation` on controls; the tap highlight is set deliberately (the focus and pressed styles replace it); `overscroll-behavior: contain` in dialogs and sheets |
| Team overrides kept | Sentence case, not Title Case (Vietnamese); the AI speaks as "em" in the first person (proposal §09 voice, product requirement level 1); 44px targets instead of 24px; no runtime CDN preconnect (fonts are self-hosted) |

