# Color

Part of the Proactive Care Design System v1.0. Start at [MASTER.md](MASTER.md). Values: [tokens.md](tokens.md) §1 (the only place hex codes appear).

## 1. Concept: mineral and signal

The palette is **mineral neutrals, ink, and a small closed set of signal hues**.

- **Mineral neutrals** are cool greys with a faint green undertone (one hue family, hue 150 to 165, very low chroma). This is a
  deliberate step away from two defaults: the warm cream plus espresso palette that taste-skill flags as the most common AI tell, and
  the blue-slate greys of generic SaaS. Mineral reads as engineered material: brushed metal, concrete, instrument housings.
- **Ink** (`--fg`, also `--accent`) is the color of people and of action.
- **Signal hues** each mean one thing and appear only where that meaning applies. They are never decoration.

One palette for the whole product. No surface introduces a hue, a warmer grey or a gradient.

## 2. Roles

| Token(s) | Means | Use for | Never use for |
|---|---|---|---|
| `--bg`, `--surface`, `--sunken` | Ground | Canvas, raised objects that earn elevation, wells (evidence, code, disabled fills, selected rows) | Signalling state |
| `--fg`, `--muted` | Text | Primary and secondary text. Both pass AA on every ground and tint | Placeholder-grey text below AA (there is no third text color) |
| `--border`, `--border-strong` | Structure | Decorative dividers / control borders and future trace segments | `--border` on anything a person must perceive to operate |
| `--accent`, `--accent-hover`, `--on-accent` | The one accent (ink) | Primary action fill, selected state (tabs, selected row bar, selected option) | Status, decoration, large fills |
| `--focus` | Keyboard location | Focus ring only | Anything else |
| `--human`, `--on-human` | A named person owns this | ESCALATED chip (inverse), square trace node, staff byline mark | Buttons (buttons use `--accent`, same value, different meaning; never mix the two tokens) |
| `--ai`, `--ai-surface` | AI or system at work | AI-state chips and nodes, the active trace segment, the AI byline mark, evidence-in-progress | Buttons, links, focus, headings, decoration, charts |
| `--attn`, `--attn-line`, `--attn-surface` | A person must decide; warning | Waiting-state chips and diamond nodes, due-soon deadlines, reconnecting banner | Errors (use `--danger`), offers, urgency marketing |
| `--ok`, `--ok-surface` | Confirmed by a system of record | RESOLVED, server receipts ("Đã đặt lịch"), validator "Đạt" | Eligibility, predictions, "sent", anything not yet confirmed |
| `--danger`, `--danger-surface`, `--on-danger` | Failure, risk, safety | Errors, validator "Không đạt", overdue, lost connection, safety banner, destructive confirm | Exclusions, warranty "expired", sentiment below `angry` |
| `--scrim` | Modal context | Behind dialogs and sheets | Image overlays, decoration |

`--attn-line` is a graphics-only token: it fails as a text background (3.96:1 with `--fg`). Text on amber uses `--attn-surface`.

## 3. Semantics

### 3.1 Who holds the ball

The state hues answer one question, *who has this case now?*

| Holder | Hue | Shape (always together with hue) |
|---|---|---|
| AI or system | `--ai` teal | circle |
| A person must decide (customer or staff) | `--attn` amber | diamond |
| A named human owns it | `--human` ink, inverse | square |
| Confirmed done | `--ok` green | filled circle with check |
| Something failed, or safety | `--danger` red | triangle |

Shape, icon and words carry the meaning on their own; hue makes it faster to scan (taste-rules rule 11, WCAG 1.4.1).

### 3.2 Color marks the present

In any trace, list or queue, only the **current** state and any **exception** (failure, safety, overdue) carry hue. Completed history is
drawn in `--fg` and `--border-strong`. Future steps are hollow `--border-strong` with a dashed connector. A screen of finished history
is therefore almost colorless, and the one colored thing is where attention belongs.

### 3.3 Why the accent is ink

Taste-rules rule 5 allows one accent color for primary actions and selection. Making that accent ink has three effects:

1. Buttons can never be mistaken for states. Every signal hue stays free to mean exactly one thing.
2. It ties action to people: what a human presses, and what a human owns, is drawn in the same ink.
3. It reads as decisive and calm on mineral grey, with no "AI blue" connotation.

In dark theme the accent inverts to light ink on the dark ground with dark text, keeping the same role.

### 3.4 Interpretation of taste-skill's color consistency lock

taste-skill (§4.2) asks for one accent locked across a page and no stray status hues. This system meets it as follows: exactly one
accent (ink); the state hues form a closed, documented set that appears only inside state indicators (chips, nodes, banners, deadline
text); no hue is used decoratively; no gradients. A new hue requires a MASTER change.

## 4. Dark theme

- Same roles and token names; only values change. Default follows the system preference, with a "Sáng / Tối / Theo máy" switch that
  remembers the choice (taste-rules rule 4).
- The ground gets darker as it recedes (`--sunken` below `--bg` below `--surface`). Floating layers use `--surface` plus `--border`; shadows are off.
- State hues get lighter and tints become deep, low-chroma grounds, so chips never glow.
- No pure black anywhere; the darkest value is `--sunken`.
- One theme per page (taste-skill §4.11): sections never invert, including on the Landing page.

## 5. Things color never does

- No gradients, including "subtle" ones on buttons, cards or text.
- No glow, colored shadow, neon edge or tinted glass.
- No hue on large areas: a state tint never fills more than a chip, a banner or a row highlight.
- No outlined control on a state tint: `--border-strong` on `--attn-surface` falls to 2.87:1 in dark theme. An action inside a tinted
  or filled banner is a filled button in `--surface` with `--fg` text.
- No color-coded categories in charts that reuse state hues. Any future chart (for example a manager dashboard, not in v1.0 scope)
  uses `--fg`, `--muted` and `--ai` only, plus pattern and direct labels.
- Under forced-colors (Windows high contrast), meaning survives through shape, icon and text; nodes and chips fall back to system colors.

## 6. Contrast record

Computed 2026-10-03 from the values in [tokens.md](tokens.md) with the WCAG 2.x relative-luminance formula. Every row passes in both
themes. Re-run the check whenever a color token changes, and update this table in the same pull request.

| Pair | Kind | Min | Light | Dark |
|---|---|---|---|---|
| `--fg` on `--bg` | text | 4.5:1 | 15.83 | 15.28 |
| `--fg` on `--surface` | text | 4.5:1 | 17.01 | 14.20 |
| `--fg` on `--sunken` | text | 4.5:1 | 14.41 | 15.96 |
| `--muted` on `--bg` | text | 4.5:1 | 6.61 | 8.02 |
| `--muted` on `--surface` | text | 4.5:1 | 7.10 | 7.46 |
| `--muted` on `--sunken` | text | 4.5:1 | 6.02 | 8.38 |
| `--on-accent` on `--accent` | text | 4.5:1 | 15.83 | 15.28 |
| `--on-accent` on `--accent-hover` | text | 4.5:1 | 11.30 | 11.94 |
| `--on-human` on `--human` | text | 4.5:1 | 15.83 | 15.28 |
| `--on-danger` on `--danger` | text | 4.5:1 | 6.41 | 8.09 |
| `--ai` on `--bg` | text | 4.5:1 | 6.18 | 9.45 |
| `--ai` on `--surface` | text | 4.5:1 | 6.64 | 8.78 |
| `--ai` on `--ai-surface` | text | 4.5:1 | 5.70 | 6.84 |
| `--attn` on `--bg` | text | 4.5:1 | 6.19 | 10.07 |
| `--attn` on `--surface` | text | 4.5:1 | 6.65 | 9.36 |
| `--attn` on `--attn-surface` | text | 4.5:1 | 5.76 | 7.49 |
| `--ok` on `--bg` | text | 4.5:1 | 5.97 | 9.45 |
| `--ok` on `--surface` | text | 4.5:1 | 6.41 | 8.78 |
| `--ok` on `--ok-surface` | text | 4.5:1 | 5.45 | 7.09 |
| `--danger` on `--bg` | text | 4.5:1 | 5.97 | 8.09 |
| `--danger` on `--surface` | text | 4.5:1 | 6.41 | 7.52 |
| `--danger` on `--danger-surface` | text | 4.5:1 | 5.34 | 6.79 |
| `--fg` on `--ai-surface` | text | 4.5:1 | 14.60 | 11.07 |
| `--fg` on `--attn-surface` | text | 4.5:1 | 14.74 | 11.37 |
| `--fg` on `--ok-surface` | text | 4.5:1 | 14.47 | 11.46 |
| `--fg` on `--danger-surface` | text | 4.5:1 | 14.17 | 12.83 |
| `--muted` on `--ai-surface` | text | 4.5:1 | 6.10 | 5.81 |
| `--border-strong` on `--bg` | non-text | 3.0:1 | 3.53 | 3.86 |
| `--border-strong` on `--surface` | non-text | 3.0:1 | 3.79 | 3.59 |
| `--border-strong` on `--sunken` | non-text | 3.0:1 | 3.21 | 4.03 |
| `--focus` on `--bg` | non-text | 3.0:1 | 15.83 | 15.28 |
| `--focus` on `--surface` | non-text | 3.0:1 | 17.01 | 14.20 |
| `--accent` on `--bg` | non-text | 3.0:1 | 15.83 | 15.28 |
| `--accent-hover` on `--bg` | non-text | 3.0:1 | 11.30 | 11.94 |
| `--ai` on `--bg` | non-text | 3.0:1 | 6.18 | 9.45 |
| `--attn-line` on `--bg` | non-text | 3.0:1 | 4.00 | 10.07 |
| `--attn-line` on `--surface` | non-text | 3.0:1 | 4.29 | 9.36 |
| `--ok` on `--bg` | non-text | 3.0:1 | 5.97 | 9.45 |
| `--danger` on `--bg` | non-text | 3.0:1 | 5.97 | 8.09 |
| `--danger` on `--sunken` | text | 4.5:1 | 5.43 | 8.45 |
| `--attn` on `--sunken` | text | 4.5:1 | 5.63 | 10.52 |
| `--ok` on `--sunken` | text | 4.5:1 | 5.43 | 9.87 |
| `--ai` on `--sunken` | text | 4.5:1 | 5.62 | 9.87 |
| `--accent` on `--surface` | non-text | 3.0:1 | 17.01 | 14.20 |
| `--accent` on `--sunken` | non-text | 3.0:1 | 14.41 | 15.96 |
| `--attn-line` on `--sunken` | non-text | 3.0:1 | 3.64 | 10.52 |
| `--ai` on `--surface` | non-text | 3.0:1 | 6.64 | 8.78 |
| `--ai` on `--sunken` | non-text | 3.0:1 | 5.62 | 9.87 |
| `--ok` on `--surface` | non-text | 3.0:1 | 6.41 | 8.78 |
| `--danger` on `--surface` | non-text | 3.0:1 | 6.41 | 7.52 |
| `--focus` on `--sunken` | non-text | 3.0:1 | 14.41 | 15.96 |
| `--focus` on `--ai-surface` | non-text | 3.0:1 | 14.60 | 11.07 |
| `--border-strong` on `--attn-surface` | non-text | 3.0:1 | 3.28 | 2.87, not allowed: see §5 |
| `--border` on `--bg` | decorative | none | 1.30 | 1.39 |

The rows from `--danger` on `--sunken` onward were added by the design review of 2026-10-03 for the pairs the Customer and CSKH
specifications introduced (selected and changed queue rows, state text in selected rows, the BottomNav and selection indicators).

Disabled controls use `--sunken` with `--muted` text (6.02 light, 8.38 dark), so disabled text stays readable (taste-rules rule 3)
and the reason for disabling is stated next to the control. Placeholder text, where used at all, is `--muted`.
