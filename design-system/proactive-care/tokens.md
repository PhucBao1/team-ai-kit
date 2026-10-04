# Tokens

Part of the Proactive Care Design System v1.0. Start at [MASTER.md](MASTER.md).

This file is the **only** place where raw values are defined. Every other file in the design system, every page file and every
component refers to tokens by name. Color values (hex, rgba) appear nowhere else. Other files may quote a size or duration for
readability only next to its token name, for example "`--target-min` (44px)"; if the two ever disagree, this file wins. Token names that already exist in
`taste-rules.md` rule 4 (`--bg`, `--fg`, `--muted`, `--accent`, `--danger`, `--ok`, `--border`, `--focus`) keep their names and meaning.

Names are CSS custom properties. Implementation maps them into the Tailwind theme (taste-rules rule 4). Values are set once on the
root for each theme; components never pick a theme value directly.

## 1. Color

Contrast for every pair below is recorded in [color.md](color.md) §6. Changing any value means re-running that check.

### 1.1 Neutrals and ink

| Token | Light | Dark | Role |
|---|---|---|---|
| `--bg` | `#F2F4F3` | `#0F1413` | Page canvas |
| `--surface` | `#FBFCFB` | `#161C1B` | Raised surfaces: cards that earn elevation, panes, popovers |
| `--sunken` | `#E6EAE8` | `#0A0E0D` | Wells: evidence blocks, code, disabled fills, selected rows |
| `--fg` | `#141B19` | `#E5EAE8` | Primary text, ink |
| `--muted` | `#4D5955` | `#A1ADA9` | Secondary text (still AA on every surface) |
| `--border` | `#D2D9D6` | `#28312F` | Decorative hairlines and dividers (no contrast duty) |
| `--border-strong` | `#77847F` | `#68756F` | Control borders, future trace segments (≥ 3:1) |

### 1.2 Action and human

| Token | Light | Dark | Role |
|---|---|---|---|
| `--accent` | `#141B19` | `#E5EAE8` | The one accent: primary action fill, selected state. Ink, by design |
| `--accent-hover` | `#2C3633` | `#C9D1CE` | Primary action hover |
| `--on-accent` | `#F2F4F3` | `#0F1413` | Text and icons on `--accent` |
| `--focus` | `#141B19` | `#E5EAE8` | Focus ring |
| `--human` | `#141B19` | `#E5EAE8` | Alias of `--fg`: human-owned state fill (ESCALATED chip, square node) |
| `--on-human` | `#F2F4F3` | `#0F1413` | Alias of `--bg`: text on `--human` |

### 1.3 State families

Each family has a text/icon token (AA on `--bg`, `--surface` and its own tint) and a tint for chips and banners.

| Token | Light | Dark | Role |
|---|---|---|---|
| `--ai` | `#13646E` | `#70C6D0` | AI and system at work: AI-state text, icons, nodes, active trace segment, AI byline mark |
| `--ai-surface` | `#DCEEF0` | `#12333A` | AI-state chip tint |
| `--attn` | `#7C5212` | `#E8B762` | Waiting for a person's decision, warnings: text and icons |
| `--attn-line` | `#A56C14` | `#E8B762` | Amber graphics only (diamond nodes, chip borders). Never carries text |
| `--attn-surface` | `#FAEACB` | `#3A2A10` | Amber chip and banner tint |
| `--ok` | `#1D6A3F` | `#72CB93` | Confirmed by a system of record: verified outcome, server receipt, validator pass |
| `--ok-surface` | `#DCEEE2` | `#133222` | Green chip tint |
| `--danger` | `#AE2C22` | `#EE9384` | Failure, safety, overdue, validator fail, destructive action |
| `--danger-surface` | `#FAE2DF` | `#3E1814` | Red banner and chip tint |
| `--on-danger` | `#FBFCFB` | `#0F1413` | Text on a `--danger` fill (destructive button, safety banner bar) |

### 1.4 Overlay

| Token | Light | Dark | Role |
|---|---|---|---|
| `--scrim` | `rgba(20, 27, 25, 0.45)` | `rgba(5, 8, 7, 0.65)` | Behind dialogs and sheets |

## 2. Typography

| Token | Value | Notes |
|---|---|---|
| `--font-sans` | `"Be Vietnam Pro", system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif` | Self-hosted woff2, see [typography.md](typography.md) §1 |
| `--font-mono` | `ui-monospace, "SF Mono", "Cascadia Mono", "Roboto Mono", Menlo, Consolas, "Liberation Mono", monospace` | System fonts only, nothing downloaded. Identifiers only |
| `--weight-regular` | `400` | Body |
| `--weight-strong` | `600` | Headings, labels, emphasis |

| Token | Size | Line height | Weight | Role |
|---|---|---|---|---|
| `--text-sm` | `14px` | `1.6` | 400 / 600 | Floor size: captions, metadata, CSKH data cells, chips |
| `--text-md` | `16px` | `1.6` | 400 | Body (Landing, CSKH), controls |
| `--text-lg` | `18px` | `1.6` | 400 | Customer body |
| `--text-xl` | `20px` | `1.6` | 400 / 600 | Lead paragraphs, h3 |
| `--text-2xl` | `24px` | `1.3` | 600 | h2; CSKH maximum heading |
| `--text-3xl` | `30px` | `1.3` | 600 | h1 below 768px |
| `--text-4xl` | `36px` | `1.25` | 600 | h1 at 768px and above |
| `--text-display` | `clamp(2.25rem, 1.6rem + 2.4vw, 3rem)` (36 to 48px) | `1.15` | 600 | Landing only (deviation L-03) |
| `--text-display-lg` | `clamp(2.5rem, 1.4rem + 4.4vw, 4.5rem)` (40 to 72px) | `1.15` | 600 | Landing opening statement only (deviation L-03) |
| `--tracking-display` | `-0.01em` | | | Display sizes only. Every other size: `0`. Never positive |

## 3. Space

Tailwind-compatible names on a 4px base.

| Token | Value | | Token | Value |
|---|---|---|---|---|
| `--space-1` | `4px` | | `--space-10` | `40px` |
| `--space-2` | `8px` | | `--space-12` | `48px` |
| `--space-3` | `12px` | | `--space-16` | `64px` |
| `--space-4` | `16px` | | `--space-20` | `80px` |
| `--space-5` | `20px` | | `--space-24` | `96px` |
| `--space-6` | `24px` | | `--space-32` | `128px` |
| `--space-8` | `32px` | | | |

Density modes pick from this scale; see [spacing.md](spacing.md) §2.

## 4. Size

| Token | Value | Role |
|---|---|---|
| `--target-min` | `44px` | Minimum touch / pointer target, both axes (taste-rules rule 7) |
| `--target-gap` | `8px` | Minimum gap between two targets |
| `--control-h` | `44px` | Buttons, inputs, selects |
| `--control-h-lg` | `52px` | Customer primary action (deviation C-03) |
| `--row-h` | `44px` | CSKH single-line rows |
| `--chip-h` | `28px` | State chip, non-interactive |
| `--chip-h-sm` | `24px` | State chip inside CSKH rows |
| `--icon-sm` | `16px` | With `--text-sm`; stroke 2 |
| `--icon-md` | `20px` | Default; stroke 1.75 |
| `--icon-lg` | `24px` | Standalone, headers; stroke 1.5 |
| `--node-sm` | `12px` | Trace node, compact |
| `--node-md` | `16px` | Trace node, default |
| `--node-lg` | `24px` | Trace node, Landing figures and diagrams |
| `--measure` | `65ch` | Running text line length (hard maximum 70ch) |
| `--w-customer` | `640px` | Customer content column |
| `--w-reading` | `720px` | Long-form reading column |
| `--w-page` | `1280px` | Landing and console page maximum |
| `--pane-queue` | `360px` | CSKH queue pane |
| `--pane-action` | `384px` | CSKH decision pane |
| `--gutter-sm` | `16px` | Side gutter below 768px |
| `--gutter-md` | `24px` | Side gutter 768 to 1279px |
| `--gutter-lg` | `32px` | Side gutter 1280px and above |

## 5. Shape

| Token | Value | Role |
|---|---|---|
| `--radius-sm` | `4px` | Chips, tags, square trace nodes, inline code |
| `--radius-md` | `6px` | Controls: buttons, inputs, selects, segmented controls |
| `--radius-lg` | `8px` | Containers: cards, panes, dialogs, sheets, toasts. The maximum for any container |
| `--radius-full` | `9999px` | Circular things only: avatars, radio, switch track, circle nodes |
| `--border-w` | `1px` | All borders and dividers |
| `--trace-w` | `2px` | Care Trace line |
| `--focus-w` | `2px` | Focus ring width |
| `--focus-offset` | `2px` | Gap between element and focus ring |

## 6. Elevation

One layer per shadow (taste-rules rule 5), tinted with the ink hue, never pure black.

| Token | Light | Dark | Used by |
|---|---|---|---|
| `--shadow-1` | `0 4px 16px rgba(20, 27, 25, 0.10)` | `none` (use `--surface` + `--border`) | Menus, popovers, toasts, sticky action bars |
| `--shadow-2` | `0 12px 40px rgba(20, 27, 25, 0.16)` | `none` (use `--surface` + `--border`) | Dialogs, sheets |

## 7. Motion

| Token | Value | Role |
|---|---|---|
| `--dur-press` | `120ms` | Press feedback |
| `--dur-fast` | `150ms` | Hover, small state changes, exits |
| `--dur-base` | `200ms` | Enters of small elements, chips, rows |
| `--dur-slow` | `250ms` | Sheets, dialogs, panels. The maximum for any time-based UI motion |
| `--stagger` | `50ms` | Delay between items entering together (never above 80ms) |
| `--ease-out` | `cubic-bezier(0.23, 1, 0.32, 1)` | Enter and exit |
| `--ease-in-out` | `cubic-bezier(0.77, 0, 0.175, 1)` | Movement of something already on screen |
| `--ease-drawer` | `cubic-bezier(0.32, 0.72, 0, 1)` | Bottom sheets |
| `--ease-linear` | `linear` | Spinner rotation, scroll-scrubbed sequences |
| `--rise-sm` | `4px` | Enter offset, small elements |
| `--rise-md` | `8px` | Enter offset, blocks |
| `--press-scale` | `0.98` | Press feedback scale |
| `--enter-scale` | `0.95` | Popover and dialog start scale (never 0) |

## 8. Layers

| Token | Value | Role |
|---|---|---|
| `--z-sticky` | `10` | Sticky headers, sticky action bars |
| `--z-dropdown` | `20` | Menus, popovers, tooltips |
| `--z-overlay` | `30` | Scrim |
| `--z-dialog` | `40` | Dialogs, sheets |
| `--z-toast` | `50` | Toasts |
| `--z-skip` | `60` | Skip link when focused |

## 9. Breakpoints and test widths

Breakpoints are not CSS variables (media queries cannot read them); use these values in the Tailwind config.

| Name | Min width |
|---|---|
| `sm` | `480px` |
| `md` | `768px` |
| `lg` | `1024px` |
| `xl` | `1280px` |
| `2xl` | `1536px` |

Every screen is checked at **320, 390, 768, 1024, 1280 and 1440px**, in both themes, and at 200% zoom.

Layout thresholds. Like breakpoints, these are values for media and container queries, not CSS variables; they are named here so no
implementation invents its own.

| Name | Value | Used by |
|---|---|---|
| `short-viewport` | height below `600px` | Customer sticky action bar stops being sticky (C-03) |
| `landing-full` | width at least `1024px` and height at least `700px` | Landing full tier: sticky figures and scroll sequences (L-02) |
| `case-pane-min` | `520px` | CSKH case pane minimum width beside the queue and decision panes ([spacing.md](spacing.md) §3.3) |
