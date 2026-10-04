# Spacing and layout

Part of the Proactive Care Design System v1.0. Start at [MASTER.md](MASTER.md). Values: [tokens.md](tokens.md) §3 to §4.

## 1. Scale

One 4px-based scale with Tailwind-compatible names (`--space-1` to `--space-32`). No value outside the scale, no negative margins
for "overlap" effects on Customer or CSKH, and no arbitrary values in component code.

Proximity rule: the space between a heading and its own content is always smaller than the space between that block and the next
block. Grouping is shown by space and hairlines before boxes.

## 2. Density modes

One scale, three modes. A surface's mode is fixed by its DENSITY dial (MASTER §2.1); components read the mode from their context, so
the same component is airy on the Landing page and compact in the console.

| Measure | Airy (Landing, D3) | Comfortable (default, Customer, D4) | Compact (CSKH, D8) |
|---|---|---|---|
| Between page sections | `--space-24` to `--space-32` | `--space-12` to `--space-16` | `--space-6` to `--space-8` |
| Between blocks in a section | `--space-12` | `--space-6` | `--space-4` |
| Inside a block (padding) | `--space-8` | `--space-4` to `--space-5` | `--space-3` |
| Between items in a list | `--space-6` | `--space-4` | `--space-2` with a hairline |
| Between label and value | `--space-2` | `--space-2` | `--space-1` |
| Single-line row height | n/a | `--control-h` | `--row-h` |

Floors that no mode may cross: targets at least `--target-min` (44px) on both axes with `--target-gap` (8px) between targets
(taste-rules rule 7); text at least `--text-sm`. Compact mode removes air, never target size or legibility.

## 3. Layout per surface

### 3.1 Landing

- 12-column fluid grid inside `--w-page`, column gap `--space-6`, side gutters `--gutter-sm` / `--gutter-md` / `--gutter-lg`.
- Asymmetric splits are allowed (L-05): 7 + 5, 8 + 4, offset starts. Every asymmetric section declares its single-column form below `md`.
- Running text stays within `--measure` even inside wide columns.
- Navigation height at most 72px and on one line at `lg` (taste-skill §4.7).

### 3.2 Customer

- One column, `--w-customer` wide at most, centered on larger screens; side gutter `--gutter-sm`.
- The primary action sits in a sticky bottom bar on phones (C-03), with safe-area insets and with scroll padding equal to the bar
  height so it never hides the focused element.
- The same layout is used inside the Demo stage's phone frame; the components respond to the frame, not the window.

### 3.3 CSKH

Designed for `xl` (1280px) and wider (K-08):

| Width | Layout |
|---|---|
| 1280px and up | Three panes: queue (`--pane-queue`), case file (fluid, at least 520px, which is what remains at 1280px), decision pane (`--pane-action`) |
| 1024 to 1279px | Two panes: queue and case file; the decision pane docks as a sticky bar at the bottom of the case file, and its briefing (promises, "Không nên") moves to the top of the case file |
| Below 1024px | One pane at a time with explicit back navigation; nothing scrolls horizontally except data tables in their own container |

Pane borders are hairlines (`--border`). Panes scroll independently; the page itself does not scroll at `xl`.

## 4. Alignment and rhythm

- Everything aligns to the grid or to a shared baseline of `--space-1`. Optical nudges are not allowed in component code.
- Numbers right-align in columns; text left-aligns; nothing is centered except dialog content and empty states (taste-skill §4.3 anti-center bias).
- Icons align to the first line of the text they accompany, not to the block center.
- Trace nodes align to a single vertical axis in vertical traces, and the connector runs through node centers.
