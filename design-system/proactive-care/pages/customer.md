# Customer experience: deviations from MASTER

| | |
|---|---|
| Surface | Customer experience: Việc của tôi (home), case, timeline, notifications, vehicle and service, conversation, safety, settings |
| Audience | Car owners and permitted drivers, some elderly, mostly on phones |
| Dials | VARIANCE 5, MOTION 5, DENSITY 4 (authoritative in [MASTER §2.1](../MASTER.md)). These are the MASTER defaults |
| Screens | [customer-screen-spec.md](../../../docs/frontend/customer-screen-spec.md) (C1 to C8); journey [customer-journey.md](../../../docs/frontend/customer-journey.md); motion [customer-motion-map.md](../../../docs/frontend/customer-motion-map.md); inventory [screen-map §4](../../../docs/frontend/screen-map.md) |

The customer surface is the baseline the whole system is tuned for, so it has the fewest deviations. Everything not listed below
follows [MASTER.md](../MASTER.md) and its detail files unchanged, including the default motion catalogue and comfortable density.

## Deviations

| ID | MASTER rule | Default | On Customer | Justification | Bounds | Status |
|---|---|---|---|---|---|---|
| C-01 | [typography.md](../typography.md) §2 (body `--text-md`) | Body `--text-md` | Body `--text-lg` | Older readers on phones; taste-rules rule 2 sets 18px for customer screens | Headings keep their sizes so hierarchy holds; running text within `--measure` | Active |
| C-02 | [typography.md](../typography.md) §2 (floor `--text-sm`) | Nothing below `--text-sm` | Nothing below `--text-md`, including timestamps, captions, source references, chips and navigation labels | Elderly readers, small screens, reading outdoors | Applies to every customer screen and to the customer region of the Demo stage; navigation labels wrap rather than shrink | Active |
| C-03 | [components.md](../components.md) §10 Button; [spacing.md](../spacing.md) §3.2 | Primary action `--control-h`, inline | Primary action `--control-h-lg`, full width, in a sticky bottom bar on phones, on the case screen (C2) in decision states | Thumb reach and motor precision; the one action per step is always findable | One primary action per screen; only where no BottomNav is shown, and never in the conversation (C6), where the composer holds the bottom edge and the action stays inline; the bar respects safe-area insets and reserves scroll padding so it never covers the focused element (WCAG 2.4.11); it stops being sticky when the viewport is shorter than 600px (landscape, large text, zoom); secondary actions stay inline above it; from `md` up the action returns inline | Active |
| C-04 | [components.md](../components.md) §1 (data tables available) | Data tables allowed | No data tables: label and value lists (`dl`) and stacked rows only | Tables do not reflow on phones and are hard to follow with a mobile screen reader | Applies to every customer screen, including the phone frame in the Demo stage | Active |
| C-05 | MASTER §10 (live updates never scroll the page) | Server updates never scroll | In the conversation (C6), a reader already at the newest message stays there as replies arrive | Chat convention: a customer waiting for a reply expects to see it, and scrolling for every reply is extra work for older readers | Only in C6; only when the reader is at the newest message and not typing or selecting; the jump is instant, never smooth; focus never moves; otherwise a "Tin mới" control appears and nothing scrolls | Active |
| C-06 | [components.md](../components.md) §10 AppHeader (theme switch in the header) | ThemeSwitch in the header | Below `md`, the theme switch lives in settings (C8, "Giao diện"); from `md` up it returns to the header | At 320px the header must hold the product name or back link and "Gặp nhân viên" on one line within 72px; a three-option switch does not fit beside them | The default stays "Theo máy"; C8 is one step from Notifications and Vehicle; the header never drops "Gặp nhân viên" to make room | Active |
