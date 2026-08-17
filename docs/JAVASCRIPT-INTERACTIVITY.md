# JavaScript Interactivity

> This document specifies all JavaScript interactive components for the
> OLLMH WordPress rebuild — what the archived Joomla site used, what the
> new WordPress site will use, and the implementation details for each.
>
> **Related:** [`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md)
> for library choices, [`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md)
> for theme file structure.

---

## 1. Archived site JS inventory

The archived Joomla site used these JS libraries:

| Library | Version | Purpose | Replacement |
|---|---|---|---|
| jQuery | 1.11.3 | Core library | jQuery 3.7+ (bundled with WordPress) |
| jQuery Migrate | 1.2.1 | Compatibility | Not needed (jQuery 3.x) |
| MooTools | 1.4.5 | Search autocomplete | Remove (use jQuery or vanilla JS) |
| jQuery UI Core | — | UI utilities | Remove (not needed) |
| XpertSlider | 1.4 | Home page slideshow | **Swiper.js** |
| XpertTabs | 3.3 | Tabbed content | **CSS + vanilla JS** (or Bootstrap tabs) |
| XpertScroller | 3.10 | News scroller | **CSS scroll-snap + vanilla JS** |
| jQuery Easing | 1.3 | Slider animations | Swiper.js built-in |
| jQuery Mobile | — | Touch events | Swiper.js built-in |
| Breakpoints.js | 1.0 | Responsive breakpoints | CSS `@media` (no JS needed) |
| EqualHeight | — | Equal-height columns | **CSS Flexbox/Grid** |
| MaximenuCK | — | Mega menu (CSS-only) | **Custom CSS + JS toggle** |
| Autocompleter | — | Search autocomplete | **WordPress native search** |
| HTML5 Shim | — | IE6-8 support | Remove (not needed) |
| Respond.js | — | IE6-8 media queries | Remove (not needed) |
| Selectivizr | — | IE6-8 CSS3 selectors | Remove (not needed) |

**Key principle:** Remove all legacy libraries (MooTools, IE polyfills,
jQuery Migrate). Replace ThemeXpert components with modern equivalents.
Use CSS for layout (Flexbox/Grid) instead of JS equal-height hacks.

---

## 2. New JS components

### 2.1 Home page slideshow (replaces XpertSlider)

**Library:** [Swiper.js](https://swiperjs.com/) (v11+, vanilla JS, no jQuery dependency)

**Configuration:**
```javascript
const slideshow = new Swiper('.home-slideshow', {
  // Autoplay
  autoplay: {
    delay: 4150,              // Match archived site (4.15s)
    disableOnInteraction: false,
  },

  // Effects
  effect: 'fade',             // Use fade instead of 'random' (cleaner)
  fadeEffect: { crossFade: true },

  // Speed
  speed: 900,                 // Match archived site transPeriod

  // Navigation
  pagination: {
    el: '.slideshow-pagination',
    clickable: true,
  },
  navigation: {
    nextEl: '.slideshow-next',
    prevEl: '.slideshow-prev',
  },

  // Loop
  loop: true,

  // Lazy loading
  lazy: {
    loadPrevNext: true,
  },

  // Accessibility
  a11y: {
    prevSlideMessage: 'Previous slide',
    nextSlideMessage: 'Next slide',
    paginationBulletMessage: 'Go to slide {{index}}',
  },
});
```

**HTML structure:**
```html
<div class="swiper home-slideshow">
  <div class="swiper-wrapper">
    <div class="swiper-slide">
      <img src="..." alt="Description" class="swiper-lazy">
      <div class="slide-caption">
        <h2>Slide title</h2>
        <p>Slide description</p>
      </div>
    </div>
    <!-- More slides... -->
  </div>
  <div class="swiper-pagination slideshow-pagination"></div>
  <div class="swiper-button-next slideshow-next"></div>
  <div class="swiper-button-prev slideshow-prev"></div>
</div>
```

**Load condition:** Home page only (`is_front_page()`).

---

### 2.2 Tabbed content (replaces XpertTabs)

**Implementation:** CSS + vanilla JS (no library needed)

The archived site used XpertTabs (based on Bootstrap 2 tabs) for the home
page "About OLLMH / Philosophy / Services" tab section. The new
implementation uses the same data attributes for compatibility but with
vanilla JS.

**HTML structure:**
```html
<div class="tabs" data-tabs>
  <ul class="tab-nav" role="tablist">
    <li class="tab-item active" role="presentation">
      <button role="tab" data-tab-target="#tab-about" aria-selected="true" aria-controls="tab-about">
        About OLLMH
      </button>
    </li>
    <li class="tab-item" role="presentation">
      <button role="tab" data-tab-target="#tab-philosophy" aria-selected="false" aria-controls="tab-philosophy">
        Philosophy of Care
      </button>
    </li>
    <li class="tab-item" role="presentation">
      <button role="tab" data-tab-target="#tab-services" aria-selected="false" aria-controls="tab-services">
        Our Services
      </button>
    </li>
  </ul>

  <div class="tab-content">
    <div class="tab-pane active" id="tab-about" role="tabpanel">
      <!-- Tab content -->
    </div>
    <div class="tab-pane" id="tab-philosophy" role="tabpanel" hidden>
      <!-- Tab content -->
    </div>
    <div class="tab-pane" id="tab-services" role="tabpanel" hidden>
      <!-- Tab content -->
    </div>
  </div>
</div>
```

**JavaScript:**
```javascript
document.querySelectorAll('[data-tabs]').forEach((tabsContainer) => {
  const tabs = tabsContainer.querySelectorAll('[role="tab"]');
  const panes = tabsContainer.querySelectorAll('.tab-pane');

  tabs.forEach((tab) => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      const target = tab.getAttribute('data-tab-target');

      // Deactivate all tabs
      tabs.forEach((t) => {
        t.setAttribute('aria-selected', 'false');
        t.closest('.tab-item').classList.remove('active');
      });

      // Hide all panes
      panes.forEach((p) => {
        p.classList.remove('active');
        p.hidden = true;
      });

      // Activate clicked tab
      tab.setAttribute('aria-selected', 'true');
      tab.closest('.tab-item').classList.add('active');

      // Show target pane
      const targetPane = tabsContainer.querySelector(target);
      targetPane.classList.add('active');
      targetPane.hidden = false;
    });
  });
});
```

**CSS:**
```css
.tab-nav { display: flex; gap: 0; border-bottom: 2px solid var(--color-primary); }
.tab-item { list-style: none; }
.tab-item button {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: var(--color-gray);
}
.tab-item.active button { color: var(--color-primary); font-weight: 600; }
.tab-pane { display: none; padding: 1.5rem 0; }
.tab-pane.active { display: block; animation: fadeIn 0.3s ease; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
```

---

### 2.3 News scroller (replaces XpertScroller)

**Implementation:** CSS scroll-snap + vanilla JS auto-advance

The archived site used a vertical auto-scrolling news ticker (XpertScroller
with 8s interval). The new implementation uses CSS scroll-snap for smooth
scrolling and JS for auto-advance.

**HTML structure:**
```html
<div class="news-scroller" data-news-scroller>
  <div class="scroller-track">
    <article class="scroller-item">
      <img src="..." alt="..." loading="lazy">
      <h4><a href="/news/article-slug/">News headline</a></h4>
      <p class="scroller-excerpt">Short excerpt...</p>
    </article>
    <!-- More items... -->
  </div>
  <button class="scroller-prev" aria-label="Previous">‹</button>
  <button class="scroller-next" aria-label="Next">›</button>
</div>
```

**JavaScript:**
```javascript
document.querySelectorAll('[data-news-scroller]').forEach((scroller) => {
  const track = scroller.querySelector('.scroller-track');
  const interval = 8000; // Match archived site
  let autoScroll = setInterval(advance, interval);

  function advance() {
    const items = track.querySelectorAll('.scroller-item');
    const current = Math.round(track.scrollLeft / track.offsetWidth);
    const next = (current + 1) % items.length;
    track.scrollTo({ left: next * track.offsetWidth, behavior: 'smooth' });
  }

  // Manual navigation
  scroller.querySelector('.scroller-next')?.addEventListener('click', () => {
    clearInterval(autoScroll);
    advance();
    autoScroll = setInterval(advance, interval);
  });

  scroller.querySelector('.scroller-prev')?.addEventListener('click', () => {
    clearInterval(autoScroll);
    const items = track.querySelectorAll('.scroller-item');
    const current = Math.round(track.scrollLeft / track.offsetWidth);
    const prev = (current - 1 + items.length) % items.length;
    track.scrollTo({ left: prev * track.offsetWidth, behavior: 'smooth' });
    autoScroll = setInterval(advance, interval);
  });

  // Pause on hover
  scroller.addEventListener('mouseenter', () => clearInterval(autoScroll));
  scroller.addEventListener('mouseleave', () => {
    autoScroll = setInterval(advance, interval);
  });
});
```

**CSS:**
```css
.news-scroller { position: relative; overflow: hidden; }
.scroller-track {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
}
.scroller-track::-webkit-scrollbar { display: none; }
.scroller-item {
  flex: 0 0 300px;
  scroll-snap-align: start;
}
```

---

### 2.4 Mega menu (replaces MaximenuCK)

**Implementation:** CSS hover + JS for mobile toggle

The archived site used MaximenuCK with a CSS checkbox hack for mobile. The
new implementation uses CSS for desktop hover dropdowns and JS for the
mobile hamburger toggle.

**Desktop (CSS hover):**
```css
.nav-item-has-children > .dropdown { display: none; }
.nav-item-has-children:hover > .dropdown,
.nav-item-has-children:focus-within > .dropdown { display: block; }
```

**Mobile (JS toggle):**
```javascript
const mobileToggle = document.querySelector('.mobile-menu-toggle');
const mobileNav = document.querySelector('.mobile-nav');

mobileToggle?.addEventListener('click', () => {
  const expanded = mobileToggle.getAttribute('aria-expanded') === 'true';
  mobileToggle.setAttribute('aria-expanded', !expanded);
  mobileNav.classList.toggle('is-open');
  document.body.classList.toggle('nav-open'); // Prevent scroll
});

// Submenu toggles on mobile
document.querySelectorAll('.mobile-nav .submenu-toggle').forEach((toggle) => {
  toggle.addEventListener('click', (e) => {
    e.preventDefault();
    const parent = toggle.closest('.nav-item-has-children');
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', !expanded);
    parent.querySelector('.dropdown').classList.toggle('is-open');
  });
});
```

---

### 2.5 Equal-height columns (replaces EqualHeight plugin)

**Implementation:** CSS Flexbox/Grid (no JS needed)

The archived site used a jQuery EqualHeight plugin to make columns the
same height. Modern CSS makes this trivial:

```css
.equal-height-row { display: flex; flex-wrap: wrap; gap: 1.5rem; }
.equal-height-col { flex: 1 1 300px; display: flex; flex-direction: column; }
.equal-height-col .card-body { flex: 1; } /* Stretches to equal height */
```

Or with CSS Grid:
```css
.equal-height-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
```

---

### 2.6 Search (replaces Joomla Finder + MooTools Autocompleter)

**Implementation:** WordPress native search (no custom JS needed)

WordPress provides built-in search at `/?s=query`. The theme's
`searchform.php` renders the search input. No autocomplete is needed for
the initial launch — WordPress native search is sufficient.

If autocomplete is desired later, use the [SearchWP](https://searchwp.com/)
plugin or a simple jQuery UI Autocomplete integration with a custom REST
API endpoint (`/ollmh/v1/search?q=...`).

---

### 2.7 Form interactions

**Implementation:** Vanilla JS + Fetch API (see [`FRONT-END-FORMS.md`](./FRONT-END-FORMS.md))

All form submission, validation, and Turnstile integration is handled by
`assets/js/forms.js` (loaded only on pages with forms).

---

### 2.8 Gallery / Lightbox

**Implementation:** [GLightbox](https://biati.digital/glightbox/) (lightweight, no dependencies)

The archived site had no lightbox/gallery component, but the new gallery
page (replacing "OLLMH Outlook") needs one.

```javascript
const lightbox = GLightbox({
  selector: '.gallery-lightbox',
  touchNavigation: true,
  loop: true,
});
```

---

## 3. JS file loading strategy

| File | Loaded on | Dependencies | Load position |
|---|---|---|---|
| `main.js` | All pages | None (vanilla JS) | Footer |
| `slideshow.js` | Home page only | Swiper.js | Footer |
| `tabs.js` | Pages with tabs | None | Footer |
| `news-scroller.js` | Home page only | None | Footer |
| `gallery.js` | Gallery page only | GLightbox | Footer |
| `forms.js` | Pages with forms | None | Footer |

**No JS is loaded in `<head>`** except the Turnstile API script (which is
`async defer`). All theme JS loads in the footer for non-blocking rendering.

---

## 4. jQuery usage

WordPress bundles jQuery 3.7+. The OLLMH theme **does not enqueue jQuery**
unless a specific component requires it. All theme JS is written in vanilla
ES6+ JavaScript.

If a third-party plugin requires jQuery (e.g., a plugin's lazy load feature), it
will enqueue jQuery itself — the theme does not need to.

**Exception:** If Swiper.js is loaded via npm and bundled, it has no
jQuery dependency. If loaded via CDN, it also has no jQuery dependency.

---

## 5. Inline JS removal

The archived site had extensive inline JS (XpertSlider init, XpertScroller
init, equal height init, search autocomplete). The new site has **zero
inline JS** — all JS is in external files enqueued via `wp_enqueue_script`.
This follows WordPress coding standards and allows proper caching.

Component configuration (like slideshow settings) is passed via
`wp_localize_script()` or `data-*` attributes:

```php
wp_localize_script('ollmh-slideshow', 'ollmhSlideshowConfig', [
  'autoplayDelay' => 4150,
  'speed'         => 900,
]);
```
