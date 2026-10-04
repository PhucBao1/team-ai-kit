# Typography

Part of the Proactive Care Design System v1.0. Start at [MASTER.md](MASTER.md). Values: [tokens.md](tokens.md) §2.

## 1. Families

**Be Vietnam Pro** for everything a person reads. It was designed for Vietnamese diacritics, which makes it the honest choice for a
Vietnamese product rather than a neutral default. It satisfies taste-rules rule 1 and avoids the "Inter by default" tell taste-skill flags.

| Decision | Rule |
|---|---|
| Source | Self-hosted woff2 in `frontend/src/assets/fonts/`; never Google Fonts or any CDN at runtime (taste-rules rules 1 and 15) |
| Weights | 400 and 600 only. Rule 1 also permits 700; it is not loaded, saving one file per subset |
| Styles | Upright only. Italic files are not loaded; emphasis uses weight 600 |
| Subsets | latin, latin-ext, vietnamese |
| Loading | `font-display: swap`; preload the 400 file, and the 600 file only where it is above the fold; a metric-matched fallback (`size-adjust`) to keep layout shift under 0.1 |
| License | SIL Open Font License; keep the license file next to the fonts |

**Monospace** (`--font-mono`) is the system stack only, so nothing is downloaded. It is used for machine identifiers: VIN, appointment,
repair-order and reservation ids, trace ids, tool names and code references. Never for prose, headings, numbers in sentences or
license plates (people read plates, machines read VINs).

## 2. Roles and scale

| Role | Token | Weight | Line height | Where |
|---|---|---|---|---|
| Display, large | `--text-display-lg` | 600 | 1.15 | Landing opening statement only (L-03) |
| Display | `--text-display` | 600 | 1.15 | Landing chapter statements only (L-03) |
| h1 | `--text-3xl`, `--text-4xl` from `md` | 600 | 1.3 / 1.25 | One per screen (taste-rules rule 14) |
| h2 | `--text-2xl` | 600 | 1.3 | Section headings; the largest heading in CSKH (K-04) |
| h3, lead | `--text-xl` | 600 for h3, 400 for lead | 1.6 | Sub-sections; lead paragraph under a heading |
| Body, customer | `--text-lg` | 400 | 1.6 | Customer running text (C-01) |
| Body | `--text-md` | 400 | 1.6 | Landing and CSKH running text, all controls |
| Label | `--text-md` | 600 | 1.6 | Buttons, form labels, chip text in Customer |
| Small | `--text-sm` | 400 / 600 | 1.6 | Captions, timestamps, source references, CSKH data cells and chips. The floor |

- Nothing is ever smaller than `--text-sm` (14px), including axis labels, legal text and badges (taste-rules rule 2). Customer raises the floor to `--text-md` (C-02).
- Hierarchy comes from weight and space before size. A screen uses at most three sizes in its main column.
- Headings of up to three lines use balanced wrapping; paragraphs use pretty wrapping where supported. Both are progressive
  enhancements: copy is never rewritten or hard-broken to force a line.
- Line length: `--measure` (65ch), never beyond 70ch.

## 3. Vietnamese rules

| Rule | Why |
|---|---|
| No `text-transform: uppercase`, no small caps, anywhere | Stacked diacritics collide and the words become hard to read (taste-rules rule 2) |
| Letter-spacing 0 at every size; display sizes may use `--tracking-display` (-0.01em) and nothing tighter | Horns and hooks on ư, ơ, ừ need room; positive spacing is banned by rule 2, strong negative spacing makes marks touch |
| Display line height at least 1.15, never "leading-none" | Two lines of display text with marks above (Ặ, Ễ) and below (ậ, ỵ) must not touch |
| No automatic hyphenation | Vietnamese syllables are written separately; breaking inside one is wrong |
| Acronyms stay as written (VIN, SLA, CSKH, CVDV) | They are not uppercase styling; they are spelled that way |
| Test strings in every review | `Ặ Ẫ Ỡ Ữ Ỹ ặ ẫ ỡ ữ ỹ` and `Xác nhận đặt lịch bảo dưỡng hệ thống làm mát pin`, at the largest and smallest size on the screen, both themes, 200% zoom |

## 4. Numbers, dates and units

All formatting goes through `Intl` with locale `vi-VN` (taste-rules rule 11). Numbers in columns, comparisons and meters use tabular
figures. If Be Vietnam Pro does not provide tabular figures in the shipped build, numeric columns fall back to `--font-mono` (open decision D-08).

| Kind | Format | Example |
|---|---|---|
| Money | Grouping dots, the đồng sign after a non-breaking space | 1.250.000 ₫ |
| Distance, odometer | Grouping dots, unit after a non-breaking space | 38.420 km |
| Percent | No space | 42% |
| Date | Weekday when it helps planning | Thứ Bảy, 03/10/2026 |
| Time | 24-hour | 09:00 |
| Relative time | Words, with the absolute time available on hover, focus and in the accessible name | 5 phút trước |
| Ranges in sentences | "đến" | 09:00 đến 11:00 |
| Ranges in compact data | Hyphen | 09:00-11:00 |

## 5. Punctuation in interface text

- Ellipsis is one character: `…`. Loading and in-progress labels end with it ("Đang đặt lịch…").
- Quotation marks are typographic: “ ”.
- No em dash and no en dash in any interface string (taste-skill §9.G). Use a period, a comma, a colon or parentheses; use a hyphen for ranges and compounds.
- The middle dot (`·`) is rationed to one per line in metadata strips.
- No exclamation marks in system copy. A single one is acceptable in a customer greeting written by a person.

## 6. Emphasis and links

- Emphasis: weight 600. Never italic (not loaded), never color alone, never underline (reserved for links).
- Links in running text: `--fg`, underlined, underline offset so it clears descenders and the dot below (ạ, ậ). Visited links look the same.
- Links that navigate use real anchors; actions use buttons (web-design-guidelines).
