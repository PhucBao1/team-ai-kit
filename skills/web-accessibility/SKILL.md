---
name: web-accessibility
description: Kiểm / sửa accessibility theo WCAG 2.2 AA trên một màn frontend P-073 đã render (app Vite local) — tương phản cả 2 theme, bàn phím, focus, nhãn, ARIA, live region, vùng chạm, lang="vi". Dùng khi được yêu cầu audit a11y / kiểm WCAG một màn, hoặc khi axe báo vi phạm cần sửa. Để DỰNG hoặc sửa màn mới dùng add-frontend-screen; để điều khiển trình duyệt dùng playwright-cli.
license: MIT
---
<!-- Modified by P-073 team, 2026-10-01: đổi name/description, thêm khối luật nhóm, Chrome DevTools MCP thành tuỳ chọn, cắt ví dụ thừa. Xem NOTICE.md. -->

# Accessibility (a11y)

## Luật nhóm P-073 (ưu tiên hơn nội dung bên dưới)
- Chỉ audit trên app chạy LOCAL: `cd frontend && npm run dev` (hoặc `npm run build && npm run preview`), mock bật `VITE_USE_MOCK=true`.
  Không audit Live URL production thay cho local; không gửi dữ liệu ra dịch vụ audit online.
- Công cụ mặc định: skill `playwright-cli` (snapshot cây a11y, Tab, `set-color-scheme dark`, `--mobile`) + `@axe-core/playwright`
  với `withTags(['wcag2a','wcag2aa'])` trong `frontend/e2e/`. Chrome DevTools MCP / Lighthouse chỉ là TUỲ CHỌN nếu máy có sẵn.
- **Vùng chạm ≥44×44px** (khách lớn tuổi) — dùng mức này thay cho 24×24px của WCAG 2.5.8 ở mọi chỗ bên dưới.
- `<html lang="vi">`; đoạn tiếng Anh bọc `lang="en"`. Chữ thân ≥16px (màn khách 18px), không chữ <14px.
- **AA ở CẢ HAI theme** (sáng và tối): chữ, placeholder, disabled, focus ring, viền điều khiển. Kiểm lần lượt từng theme.
- Điểm WCAG 2.2 riêng của app (token xác nhận hết hạn, xem lại trước khi ghi, header dính, "Gặp nhân viên" cùng chỗ):
  `../add-frontend-screen/references/a11y-wcag22.md`. Gu thẩm mỹ / câu chữ: `../add-frontend-screen/references/taste-rules.md`.
- Sửa lỗi theo luật của skill `add-frontend-screen` (token màu, `src/i18n/vi.ts`), kèm test (Vitest + axe hoặc e2e) chặn tái phát.
- Báo cáo: bảng `mức (Critical/Serious/Moderate) · màn · phần tử · tiêu chí WCAG · cách sửa` + ảnh sáng / tối / 390×844 trước–sau.
  Không ghi "đạt WCAG" chỉ vì axe = 0: axe chỉ bắt một phần lỗi.

Comprehensive accessibility guidelines based on WCAG 2.2 and Lighthouse accessibility audits. Goal: make content usable by everyone, including people with disabilities.

## Evidence-led audit workflow

When a rendered page is available:

1. Run axe on the rendered screen (`@axe-core/playwright`, tags `wcag2a` + `wcag2aa`) in light and dark, desktop and mobile. Optional: a Lighthouse Accessibility audit if Chrome DevTools MCP (`lighthouse_audit`) or Lighthouse is already available.
2. Use failed audit nodes to localize the relevant component or template instead of searching the whole repository for generic patterns.
3. Inspect a rendered accessibility-tree snapshot for names, roles, states, landmarks, and heading structure (`playwright-cli snapshot`). Exercise the affected flow with the keyboard (`playwright-cli press Tab`).
4. Fix the source, then re-run the same audit and manual interaction.

Complete the same manual checks whatever tool ran. Automated tools detect only a subset of accessibility barriers: a score of 100 is not WCAG conformance, and a low score does not replace issue-level evidence.

## WCAG Principles: POUR

| Principle | Description |
|-----------|-------------|
| **P**erceivable | Content can be perceived through different senses |
| **O**perable | Interface can be operated by all users |
| **U**nderstandable | Content and interface are understandable |
| **R**obust | Content works with assistive technologies |

Target for P-073: **WCAG 2.2 Level AA**.

---

## Perceivable

### Text alternatives (1.1)

**Images require alt text:**
```html
<!-- ❌ Missing alt -->
<img src="chart.png">

<!-- ✅ Descriptive alt -->
<img src="chart.png" alt="Bar chart showing 40% increase in Q3 sales">

<!-- ✅ Decorative image (empty alt) -->
<img src="decorative-border.png" alt="" role="presentation">

<!-- ✅ Complex image with longer description -->
<figure>
  <img src="infographic.png" alt="2024 market trends infographic" 
       aria-describedby="infographic-desc">
  <figcaption id="infographic-desc">
    <!-- Detailed description -->
  </figcaption>
</figure>
```

**Icon buttons need accessible names:**
```html
<!-- ❌ No accessible name -->
<button><svg><!-- menu icon --></svg></button>

<!-- ✅ Using aria-label -->
<button aria-label="Open menu">
  <svg aria-hidden="true"><!-- menu icon --></svg>
</button>

<!-- ✅ Using visually hidden text -->
<button>
  <svg aria-hidden="true"><!-- menu icon --></svg>
  <span class="visually-hidden">Open menu</span>
</button>
```

**Visually hidden class:**
```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### Color contrast (1.4.3, 1.4.6)

| Text Size | AA minimum | AAA enhanced |
|-----------|------------|--------------|
| Normal text (< 18px / < 14px bold) | 4.5:1 | 7:1 |
| Large text (≥ 18px / ≥ 14px bold) | 3:1 | 4.5:1 |
| UI components & graphics | 3:1 | 3:1 |

```css
/* ❌ Low contrast (2.5:1) */
.low-contrast {
  color: #999;
  background: #fff;
}

/* ✅ Sufficient contrast (7:1) */
.high-contrast {
  color: #333;
  background: #fff;
}

/* ✅ Focus states need contrast too (3:1 against background, WCAG 1.4.11) */
:focus-visible {
  outline: 2px solid currentColor;
  outline-offset: 2px;
}
```

**Don't rely on color alone:**
```html
<!-- ❌ Only color indicates error -->
<input class="error-border">
<style>.error-border { border-color: red; }</style>

<!-- ✅ Color + icon + text -->
<div class="field-error">
  <input aria-invalid="true" aria-describedby="email-error">
  <span id="email-error" class="error-message">
    <svg aria-hidden="true"><!-- error icon --></svg>
    Please enter a valid email address
  </span>
</div>
```

### Media alternatives (1.2)

Video needs captions (`<track kind="captions" srclang="vi">`); audio needs a transcript.

---

## Operable

### Keyboard accessible (2.1)

**All functionality must be keyboard accessible.** Prefer native interactive elements — `<button>`, `<a href>`, and form controls handle Enter/Space activation, focus, and assistive-tech semantics for free. Only add manual keyboard handling when you cannot use a native element.

```html
<!-- ❌ Non-interactive element with click only: not focusable, no keyboard activation -->
<div class="card" onclick="handleAction()">Open</div>

<!-- ✅ Best: use a native button -->
<button type="button" onclick="handleAction()">Open</button>
```

```javascript
// ✅ When you MUST use a non-interactive element (e.g. div with role="button"),
// make it focusable AND handle keyboard activation. Do NOT add this to a native
// <button> — Enter/Space already fire click, so you'd double-trigger.
element.setAttribute('role', 'button');
element.setAttribute('tabindex', '0');
element.addEventListener('click', handleAction);
element.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    handleAction();
  }
});
```

**No keyboard traps.** Users must be able to Tab into and out of every component. Use the [modal focus trap pattern](references/A11Y-PATTERNS.md#modal-focus-trap) for dialogs—the native `<dialog>` element handles this automatically.

### Focus visible (2.4.7)

```css
/* ❌ Never remove focus outlines */
*:focus { outline: none; }

/* ✅ Use :focus-visible for keyboard-only focus */
:focus {
  outline: none;
}

:focus-visible {
  outline: 2px solid currentColor; /* inherits text color → already contrast-checked */
  outline-offset: 2px;
}

/* ✅ Or pick a brand color and verify ≥3:1 contrast against every background it lands on */
button:focus-visible {
  box-shadow: 0 0 0 3px rgba(0, 95, 204, 0.5);
}
```

### Focus not obscured (2.4.11) — new in 2.2

When an element receives keyboard focus, it must not be entirely hidden by other author-created content such as sticky headers, footers, or overlapping panels. At Level AAA (2.4.12), no part of the focused element may be hidden.

```css
/* ✅ Account for sticky headers when scrolling to focused elements */
:target {
  scroll-margin-top: 80px;
}

/* ✅ Ensure focused items clear fixed/sticky bars */
:focus {
  scroll-margin-top: 80px;
  scroll-margin-bottom: 60px;
}
```

### Skip links (2.4.1)

Provide a skip link so keyboard users can bypass repetitive navigation. See the [skip link pattern](references/A11Y-PATTERNS.md#skip-link) for full markup and styles.

### Target size (2.5.8) — new in 2.2

Interactive targets must be at least **24 × 24 CSS pixels** (AA) — **P-073 uses 44 × 44 px**. Exceptions: inline text links, elements where the browser controls the size, and targets where a 24px circle centered on the bounding box does not overlap another target.

```css
/* ✅ P-073 target size (44×44) */
.touch-target {
  min-width: 44px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
```

### Dragging movements (2.5.7) — new in 2.2

Any action that requires dragging must have a single-pointer alternative (e.g., buttons, inputs). See the [dragging movements pattern](references/A11Y-PATTERNS.md#dragging-movements) for a sortable-list example.

### Timing (2.2)

Warn before a time limit expires and offer to extend it (P-073: confirmation token — warning + "Gia hạn" button, see `../add-frontend-screen/references/a11y-wcag22.md`).

### Motion (2.3)

```css
/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## Understandable

### Page language (3.1.1)

```html
<!-- ❌ No language specified -->
<html>

<!-- ✅ Language specified (P-073) -->
<html lang="vi">

<!-- ✅ Language changes within page -->
<p>Mã lỗi từ hệ thống: <span lang="en">Connection timeout</span>.</p>
```

### Consistent navigation (3.2.3)

Navigation repeated across screens keeps the same order; mark the current item with `aria-current="page"`.

### Consistent help (3.2.6) — new in 2.2

If a help mechanism (contact info, chat widget, FAQ link, self-help option) is repeated across multiple pages, it must appear in the **same relative order** each time. Users who rely on consistent placement shouldn't have to hunt for help on every page.

### Form labels (3.3.2)

Every input needs a programmatically associated label. See the [form labels pattern](references/A11Y-PATTERNS.md#form-labels) for explicit, implicit, and instructional examples.

### Error handling (3.3.1, 3.3.3)

Announce errors to screen readers with `role="alert"` or `aria-live`, set `aria-invalid="true"` on invalid fields, and focus the first error on submit. See the [error handling pattern](references/A11Y-PATTERNS.md#error-handling) for full markup and JS.

### Redundant entry (3.3.7) — new in 2.2

Don't force users to re-enter information they already provided in the same session. Auto-populate from earlier steps, or let users select from previously entered values. Exceptions: security re-confirmation and content that has expired.

### Accessible authentication (3.3.8) — new in 2.2

Login flows (staff console) must not rely on cognitive tests: allow paste / autofill in password fields (`autocomplete="current-password"`), or offer a passwordless alternative.

---

## Robust

### ARIA usage (4.1.2)

**Prefer native elements:**
```html
<!-- ❌ ARIA role on div -->
<div role="button" tabindex="0">Click me</div>

<!-- ✅ Native button -->
<button>Click me</button>

<!-- ❌ ARIA checkbox -->
<div role="checkbox" aria-checked="false">Option</div>

<!-- ✅ Native checkbox -->
<label><input type="checkbox"> Option</label>
```

**When ARIA is needed,** use the correct roles and states. See the [ARIA tabs pattern](references/A11Y-PATTERNS.md#aria-tabs) for a complete tablist example.

### Live regions (4.1.3)

Use `aria-live` regions to announce dynamic content changes without moving focus. See the [live regions pattern](references/A11Y-PATTERNS.md#live-regions-and-notifications) for markup and a `showNotification()` helper.

---

## Testing checklist

### Automated testing

P-073: axe through Playwright Test on the local app (no global installs):

```bash
cd frontend && npm run dev            # in background (or: npm run build && npm run preview)
cd frontend && PLAYWRIGHT_HTML_OPEN=never npx playwright test e2e/<screen>.spec.ts   # spec uses AxeBuilder withTags(['wcag2a','wcag2aa'])
```

Optional, only if already available on the machine: Lighthouse via Chrome DevTools MCP (`lighthouse_audit`) or `npx --no-install lighthouse http://localhost:5173 --only-categories=accessibility`.

### Manual testing

- [ ] **Keyboard navigation:** Tab through entire page, use Enter/Space to activate
- [ ] **Screen reader:** Test with VoiceOver (Mac), NVDA (Windows), or TalkBack (Android)
- [ ] **Zoom:** Content usable at 200% zoom
- [ ] **High contrast:** Test with Windows High Contrast Mode
- [ ] **Reduced motion:** Test with `prefers-reduced-motion: reduce`
- [ ] **Focus order:** Logical and follows visual order
- [ ] **Target size:** Interactive elements meet 44×44px (P-073)
- [ ] **Both themes:** Contrast checked in light AND dark
- [ ] **Text spacing / reflow:** No clipping with WCAG text-spacing; no horizontal scroll at 320px

See the [screen reader commands reference](references/A11Y-PATTERNS.md#screen-reader-commands) for VoiceOver and NVDA shortcuts.

---

## Common issues by impact

### Critical (fix immediately)
1. Missing form labels
2. Missing image alt text
3. Insufficient color contrast
4. Keyboard traps
5. No focus indicators

### Serious (fix before launch)
1. Missing page language
2. Missing heading structure
3. Non-descriptive link text
4. Auto-playing media
5. Missing skip links

### Moderate (fix soon)
1. Missing ARIA labels on icons
2. Inconsistent navigation
3. Missing error identification
4. Timing without controls
5. Missing landmark regions

## References

- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [Deque axe Rules](https://dequeuniversity.com/rules/axe/)
- [WCAG criteria reference](references/WCAG.md)
- [Accessibility code patterns](references/A11Y-PATTERNS.md)
