# Responsive Design

> This document defines the responsive design strategy for the OLLMH
> WordPress rebuild — breakpoints, mobile menu, grid system, and
> mobile-first approach.
>
> **Related:** [`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md) for
> theme structure, [`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md)
> for header/footer layout.

---

## 1. Archived site responsive analysis

The archived Joomla site (TX Finnix template) was **desktop-first** with
these breakpoints:

| Breakpoint | Target | Container width | Notes |
|---|---|---|---|
| ≤480px | Small mobile | auto | Columns stack, forms adapt |
| ≤524px | Menu mobile | auto | Hamburger menu appears (checkbox hack) |
| ≤767px | Mobile / portrait tablet | auto | Grid stacks, mobile menu active |
| 768–979px | Tablet landscape | 744px | Reduced grid widths |
| ≥1200px | Large desktop | 960px | Full grid |

**Problems with the archived approach:**
- Desktop-first (mobile is an afterthought, not the baseline)
- Fixed container widths (not fluid)
- Bootstrap 2-style grid (`.grid1`–`.grid12`, `.row-fluid`)
- CSS checkbox hack for mobile menu (no JS, but poor UX)
- No sticky header
- No off-canvas navigation
- IE polyfills loaded (Respond.js, Selectivizr — no longer needed)

---

## 2. New responsive strategy

The OLLMH WordPress rebuild uses a **mobile-first** approach:

1. **Base styles target mobile** (smallest screens first)
2. **`@media (min-width: ...)` queries enhance** for larger screens
3. **CSS Grid and Flexbox** for layout (no Bootstrap grid needed)
4. **Fluid container** with `max-width` (not fixed width)
5. **JavaScript mobile menu** (not CSS checkbox hack)
6. **Sticky header** on all screen sizes
7. **No IE polyfills** (target modern browsers only)

---

## 3. Breakpoints

| Breakpoint | Name | Target devices | Container width |
|---|---|---|---|
| Base (0px) | Mobile | Phones (< 640px) | 100% (with 16px padding) |
| `min-width: 640px` | Large mobile | Large phones, small tablets | 600px |
| `min-width: 768px` | Tablet | Portrait tablets | 720px |
| `min-width: 1024px` | Desktop | Laptops, desktops | 960px |
| `min-width: 1280px` | Large desktop | Large monitors | 1200px |

**Rationale:** These breakpoints align with common device widths and are
simpler than the archived site's 5-breakpoint system. The jump from 768px
to 1024px covers the tablet-to-desktop transition cleanly.

---

## 4. Container and grid

### Container

```css
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;  /* 16px on mobile */
}

@media (min-width: 768px) {
  .container { padding: 0 1.5rem; }  /* 24px on tablet+ */
}

@media (min-width: 1024px) {
  .container { padding: 0 2rem; }  /* 32px on desktop+ */
}
```

### Grid system (CSS Grid)

```css
/* Base: single column on mobile */
.grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: 1fr;
}

/* Tablet: 2 columns */
@media (min-width: 768px) {
  .grid-2 { grid-template-columns: repeat(2, 1fr); }
  .grid-3 { grid-template-columns: repeat(2, 1fr); }  /* 2 of 3 on tablet */
}

/* Desktop: full columns */
@media (min-width: 1024px) {
  .grid-2 { grid-template-columns: repeat(2, 1fr); }
  .grid-3 { grid-template-columns: repeat(3, 1fr); }
  .grid-4 { grid-template-columns: repeat(4, 1fr); }
}
```

### Content + sidebar layout

```css
/* Mobile: content first, sidebar below */
.content-sidebar {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

/* Desktop: content left, sidebar right */
@media (min-width: 1024px) {
  .content-sidebar {
    grid-template-columns: 1fr 300px;
  }
}
```

---

## 5. Header behavior

### Mobile (≤ 1023px)

- **Logo:** Left-aligned, scaled down
- **Hamburger button:** Right-aligned, toggles mobile nav
- **Mobile nav:** Full-width dropdown panel below header
- **Sticky:** Header sticks to top on scroll
- **Search:** Inside mobile nav panel (not visible in header)

### Desktop (≥ 1024px)

- **Logo:** Left-aligned
- **Main menu:** Center or right-aligned, horizontal with mega dropdowns
- **Top bar:** Phone, email, social links (hidden on mobile)
- **Search:** In top bar or header right zone
- **Sticky:** Header sticks to top on scroll

### Sticky header implementation

```css
.site-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: var(--color-white);
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: box-shadow 0.3s ease;
}

/* Add stronger shadow when scrolled */
.site-header.is-scrolled {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
```

```javascript
// Add 'is-scrolled' class when page is scrolled
window.addEventListener('scroll', () => {
  const header = document.querySelector('.site-header');
  header.classList.toggle('is-scrolled', window.scrollY > 10);
}, { passive: true });
```

---

## 6. Mobile menu

### Implementation

The mobile menu is a **slide-down panel** that appears below the header
when the hamburger is tapped:

```css
.mobile-nav {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--color-white);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  max-height: calc(100vh - 60px);
  overflow-y: auto;
}

.mobile-nav.is-open { display: block; }

@media (min-width: 1024px) {
  .mobile-nav { display: none !important; }
  .mobile-menu-toggle { display: none; }
}
```

### Behavior

- Tap hamburger → menu slides down
- Tap hamburger again → menu slides up
- Tap a menu item with children → submenu expands inline (accordion)
- Tap outside menu → menu closes
- Menu items are full-width, stacked vertically
- Body scroll is locked when menu is open (`overflow: hidden` on `<body>`)

### Hamburger button

```html
<button class="mobile-menu-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Toggle menu">
  <span class="hamburger-line"></span>
  <span class="hamburger-line"></span>
  <span class="hamburger-line"></span>
</button>
```

```css
.mobile-menu-toggle {
  display: flex;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.hamburger-line {
  width: 24px;
  height: 3px;
  background: var(--color-primary);
  border-radius: 2px;
  transition: transform 0.3s, opacity 0.3s;
}

/* Animate to X when open */
.mobile-menu-toggle[aria-expanded="true"] .hamburger-line:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}
.mobile-menu-toggle[aria-expanded="true"] .hamburger-line:nth-child(2) {
  opacity: 0;
}
.mobile-menu-toggle[aria-expanded="true"] .hamburger-line:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}
```

---

## 7. Responsive images

All images use responsive `srcset` and `sizes` attributes (WordPress
generates these automatically for images inserted via the editor):

```html
<img src="image-800x600.jpg"
     srcset="image-400x300.jpg 400w, image-600x450.jpg 600w, image-800x600.jpg 800w, image-1200x800.jpg 1200w"
     sizes="(max-width: 600px) 100vw, (max-width: 1024px) 50vw, 33vw"
     alt="Description"
     loading="lazy"
     width="800" height="600">
```

**CSS:**
```css
img { max-width: 100%; height: auto; }
```

**Custom image sizes** registered by the theme (see
[`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md) → Image sizes):
- `ollmh-hero`: 1920×600 (slideshow)
- `ollmh-card`: 600×400 (cards)
- `ollmh-thumbnail`: 300×200 (thumbnails)
- `ollmh-staff`: 400×400 (portraits)
- `ollmh-gallery`: 1200×800 (gallery, no crop)

---

## 8. Responsive tables

Tables (ward bed status, clinic schedules) need to be scrollable on mobile:

```css
.table-responsive {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.table-responsive table {
  min-width: 600px;  /* Prevent squishing */
}
```

For very wide tables, consider a card layout on mobile:

```css
@media (max-width: 767px) {
  .clinic-schedule-table tr {
    display: block;
    margin-bottom: 1rem;
    border: 1px solid var(--color-light);
    border-radius: 4px;
    padding: 1rem;
  }
  .clinic-schedule-table td {
    display: block;
    text-align: right;
  }
  .clinic-schedule-table td::before {
    content: attr(data-label);
    float: left;
    font-weight: 600;
  }
}
```

---

## 9. Responsive forms

Forms stack vertically on mobile and use 2-column layouts on desktop:

```css
.form-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .form-row-2 { grid-template-columns: 1fr 1fr; }
  .form-row-3 { grid-template-columns: 1fr 1fr 1fr; }
}
```

Inputs are at least 44px tall for touch targets (Apple HIG recommendation):

```css
input, select, textarea {
  min-height: 44px;
  font-size: 16px;  /* Prevents iOS zoom on focus */
}
```

---

## 10. Responsive typography

Use `clamp()` for fluid typography that scales with viewport width:

```css
h1 { font-size: clamp(1.75rem, 4vw, 2.5rem); }
h2 { font-size: clamp(1.5rem, 3vw, 2rem); }
h3 { font-size: clamp(1.25rem, 2.5vw, 1.75rem); }
p  { font-size: clamp(1rem, 1.5vw, 1.125rem); }
```

This eliminates the need for breakpoint-specific font sizes — the text
scales smoothly from mobile to desktop.

---

## 11. Viewport meta tag

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

**Do not** add `user-scalable=no` or `maximum-scale=1` — these prevent
pinch-to-zoom and violate WCAG accessibility guidelines (see
[`ACCESSIBILITY.md`](./ACCESSIBILITY.md)).

---

## 12. Browser support

| Browser | Minimum version | Notes |
|---|---|---|
| Chrome | 110+ | All features supported |
| Firefox | 110+ | All features supported |
| Safari | 16+ | All features supported |
| Edge | 110+ | All features supported |
| Samsung Internet | 20+ | All features supported |
| Opera | 95+ | All features supported |

**Not supported:** Internet Explorer (any version), Chrome/Firefox/Safari
versions older than 110. These browsers have negligible market share in
Kenya (target audience).
