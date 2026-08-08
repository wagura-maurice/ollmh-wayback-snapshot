# Accessibility (WCAG Compliance)

> This document defines the accessibility requirements for the OLLMH
> WordPress site, targeting WCAG 2.1 Level AA compliance.
>
> **Related:** [`RESPONSIVE-DESIGN.md`](./RESPONSIVE-DESIGN.md) for
> responsive behavior, [`TESTING-PLAN.md`](./TESTING-PLAN.md) for
> accessibility testing checklist.

---

## 1. Compliance target

**WCAG 2.1 Level AA** — the standard for public-sector and healthcare
websites. This is also required by Kenya's Persons with Disabilities Act
and aligns with international best practice.

WCAG has 4 principles (POUR):
- **Perceivable:** Content must be presentable in ways users can perceive
- **Operable:** Interface components must be operable
- **Understandable:** Content and operation must be understandable
- **Robust:** Content must work with assistive technologies

---

## 2. Perceivable

### 2.1 Text alternatives

- All content images have descriptive `alt` text
- Decorative images have `alt=""` (empty alt, not omitted)
- Logo has `alt="Our Lady of Lourdes Mwea Hospital"`
- SVG icons have `aria-hidden="true"` (decorative) or `<title>` (meaningful)
- Form inputs have associated `<label>` elements

### 2.2 Captions and transcripts

- No audio/video content in the current site (none in archive)
- If video is added later, it must have captions and a transcript

### 2.3 Color contrast

| Element | Minimum ratio | Example |
|---|---|---|
| Normal text (< 18px) | 4.5:1 | Body text on white background |
| Large text (≥ 18px or ≥ 14px bold) | 3:1 | Headings on white background |
| UI components and graphical objects | 3:1 | Form borders, icons, focus indicators |

Verify contrast using the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/).

The OLLMH color palette (see [`COLOR-SCHEMA.md`](./COLOR-SCHEMA.md)):
- Primary blue `#0046a8` on white: **7.04:1** ✅ (passes AAA)
- Secondary blue `#0099d3` on white: **3.39:1** ⚠️ (passes AA for large text only — use for headings/icons, not body text)
- Accent orange `#f7941e` on white: **2.59:1** ❌ (fails — use only for large decorative elements, not text)
- Gray `#666666` on white: **5.74:1** ✅ (passes AA)
- White on primary blue: **7.04:1** ✅ (passes AAA)

### 2.4 Resize and zoom

- Site is usable at 200% browser zoom (no horizontal scroll, no overlapping)
- Site is usable at 200% text-only zoom (uses `rem`/`em` units, not `px` for font sizes)
- `viewport` meta tag does **not** include `user-scalable=no` or `maximum-scale=1`

### 2.5 Orientation

- Site works in both portrait and landscape orientations (no orientation lock)

---

## 3. Operable

### 3.1 Keyboard navigation

- All interactive elements are reachable via Tab key
- Tab order is logical (follows visual order, left-to-right, top-to-bottom)
- No keyboard traps (user can Tab out of any component)
- Skip-to-content link is the first focusable element:
  ```html
  <a href="#main-content" class="skip-link">Skip to main content</a>
  ```
  ```css
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: var(--color-primary);
    color: var(--color-white);
    padding: 8px 16px;
    z-index: 100;
  }
  .skip-link:focus { top: 0; }
  ```

### 3.2 Focus indicators

- All focusable elements have a visible focus indicator:
  ```css
  a:focus, button:focus, input:focus, select:focus, textarea:focus {
    outline: 2px solid var(--color-secondary);
    outline-offset: 2px;
  }
  ```
- Focus indicator has ≥ 3:1 contrast against adjacent colors
- Never use `outline: none` without a replacement focus style

### 3.3 Touch targets

- All interactive elements are at least 44×44px (Apple HIG, WCAG 2.5.5)
- Includes buttons, links, form inputs, checkbox/radio controls
- Spacing between touch targets is at least 8px

### 3.4 No time limits

- No content auto-refreshes or times out
- Slideshow auto-play can be paused (hover or focus pauses, per WCAG 2.2.2)
- News scroller pauses on hover

### 3.5 Navigation

- Breadcrumbs are present on all inner pages
- Breadcrumbs use semantic HTML (`<nav aria-label="Breadcrumb">`)
- Search is accessible from all pages
- Sitemap page (or footer link) provides an overview of site structure

---

## 4. Understandable

### 4.1 Language

- `<html lang="en">` is set (English is the primary language)
- Any content in Swahili or other languages uses `lang` attribute on the element:
  ```html
  <span lang="sw">Karibu</span>
  ```

### 4.2 Form labels and instructions

- Every form input has a visible `<label>` element
- Required fields are marked with both an asterisk (`*`) and `aria-required="true"`
- Error messages are:
  - Announced via `role="alert"` (screen readers announce immediately)
  - Associated with the field via `aria-describedby`
  - Descriptive ("Please enter a valid email address" not just "Error")
- Form submission status is announced via `role="status"`

### 4.3 Error prevention

- Form submissions are validated client-side and server-side
- Destructive actions (delete, cancel) require confirmation
- Application form has a review step before final submission

---

## 5. Robust

### 5.1 Semantic HTML

- Use HTML5 semantic elements: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`
- ARIA landmarks where HTML5 elements aren't sufficient:
  ```html
  <header role="banner">
  <nav role="navigation" aria-label="Main Menu">
  <main role="main" id="main-content">
  <footer role="contentinfo">
  ```
- Headings are hierarchical: one `<h1>` per page, then `<h2>`, `<h3>`, etc.
- Lists use `<ul>`/`<ol>` with `<li>` (not `<div>` with bullets)

### 5.2 ARIA usage

- Use ARIA only when HTML5 semantics are insufficient
- `aria-expanded` on toggle buttons (mobile menu, accordion):
  ```html
  <button aria-expanded="false" aria-controls="mobile-nav">Menu</button>
  ```
- `aria-selected` on tab buttons:
  ```html
  <button role="tab" aria-selected="true">Tab 1</button>
  ```
- `aria-label` on icon-only buttons:
  ```html
  <button aria-label="Close menu">×</button>
  ```
- `aria-current="page"` on the current page in navigation:
  ```html
  <a href="/about/" aria-current="page">About</a>
  ```

### 5.3 Assistive technology compatibility

Test with:
- **NVDA** (free, Windows) — most common screen reader in Kenya
- **VoiceOver** (built-in, macOS/iOS) — for Apple users
- **TalkBack** (built-in, Android) — for Android users
- **Keyboard only** (no mouse) — for motor disabilities

---

## 6. Motion and animation

### 6.1 Respect `prefers-reduced-motion`

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### 6.2 No flashing content

- No content flashes more than 3 times per second (WCAG 2.3.1 — photosensitive seizure)
- Slideshow transitions are fade or slide (not flash)

---

## 7. WordPress-specific accessibility

### 7.1 Theme accessibility

- Theme follows [WordPress Accessibility Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/accessibility/)
- `body_class()` and `post_class()` are used for semantic class injection
- `wp_get_attachment_image()` is used (generates `alt`, `srcset`, `sizes`)
- Navigation menus use `wp_nav_menu()` with proper ARIA

### 7.2 Admin accessibility

- Admin UI relies on WordPress core accessibility (WCAG 2.1 AA compliant since WP 5.5)
- Custom admin pages use WordPress admin UI components (buttons, forms, tables)
- Meta boxes use standard WordPress meta box markup

### 7.3 Plugin accessibility

- All custom forms use accessible markup (labels, ARIA, error handling)
- Turnstile widget is accessible (Cloudflare Turnstile is WCAG 2.1 AA compliant)
- Slideshow (Swiper.js) has built-in ARIA support and keyboard navigation

---

## 8. Accessibility testing tools

| Tool | Purpose | Cost |
|---|---|---|
| [WAVE](https://wave.webaim.org/) | Automated accessibility audit | Free |
| [axe DevTools](https://www.deque.com/axe/) | Browser extension for automated testing | Free |
| [Lighthouse](https://developers.google.com/web/tools/lighthouse) | Chrome DevTools accessibility audit | Free |
| [NVDA](https://www.nvaccess.org/) | Screen reader testing | Free |
| [Keyboard testing](https://webaim.org/techniques/keyboard/) | Manual keyboard-only testing | Free |
| [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) | Color contrast verification | Free |

### Automated testing workflow

1. Run **Lighthouse** accessibility audit on every page (Chrome DevTools)
2. Run **WAVE** on every page (enter URL at wave.webaim.org)
3. Run **axe DevTools** on every page (browser extension)
4. Fix all errors and warnings
5. Manually test with **keyboard only** (no mouse)
6. Manually test with **NVDA** screen reader
7. Test at **200% zoom** in the browser
