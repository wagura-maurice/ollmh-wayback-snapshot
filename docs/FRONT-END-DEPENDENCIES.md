# Front-End Dependencies

> This document defines all front-end CSS and JavaScript dependencies for
> the OLLMH WordPress theme — what libraries to use, what to avoid, and
> how to load them.
>
> **Related:** [`JAVASCRIPT-INTERACTIVITY.md`](./JAVASCRIPT-INTERACTIVITY.md)
> for component specs, [`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md)
> for theme structure.

---

## 1. Dependency policy

- **Minimize dependencies.** Every external library adds page weight and
  maintenance burden. Use vanilla JS and CSS where possible.
- **No jQuery for theme code.** WordPress bundles jQuery, but the OLLMH
  theme is written in vanilla ES6+ JS. jQuery is only loaded if a
  third-party plugin requires it.
- **No Bootstrap, Tailwind, or Bulma.** The theme uses custom CSS with
  CSS custom properties (variables) and CSS Grid/Flexbox. A framework is
  unnecessary overhead for a site with a fixed design.
- **No build step required.** The theme works without npm/webpack. Sass
  and JS minification are optional optimizations (see
  [`ENVIRONMENT-SETUP.md`](./ENVIRONMENT-SETUP.md) → Front-end build tools).
- **CDN for third-party libraries.** Swiper.js and GLightbox are loaded
  via CDN with `SRI` (Subresource Integrity) hashes for security.
  Alternatively, download and bundle locally for production.

---

## 2. CSS dependencies

| Dependency | Version | Purpose | Load method | Pages |
|---|---|---|---|---|
| Theme CSS (custom) | 1.0.0 | All styling | `wp_enqueue_style` | All pages |
| Swiper CSS | 11.0+ | Slideshow styling | `wp_enqueue_style` (CDN) | Home page only |
| GLightbox CSS | 3.3+ | Gallery lightbox styling | `wp_enqueue_style` (CDN) | Gallery page only |
| Turnstile CSS | — | Captcha widget | Cloudflare auto-injects | Form pages only |

**No other CSS dependencies.** The theme does not load:
- Bootstrap
- Tailwind CSS
- Font Awesome (use SVG icons instead — see below)
- Google Fonts (use system font stack — see [`FONT-SCHEMA.md`](./FONT-SCHEMA.md))

---

## 3. JavaScript dependencies

| Dependency | Version | Purpose | Load method | Pages | jQuery? |
|---|---|---|---|---|---|
| Theme JS (custom) | 1.0.0 | Menu, tabs, scroller, general UI | `wp_enqueue_script` (footer) | All pages | No |
| Swiper.js | 11.0+ | Home page slideshow | `wp_enqueue_script` (CDN, footer) | Home page only | No |
| GLightbox | 3.3+ | Gallery lightbox | `wp_enqueue_script` (CDN, footer) | Gallery page only | No |
| Turnstile API | — | Bot protection | `<script async defer>` | Form pages only | No |
| Forms JS (custom) | 1.0.0 | AJAX form submission | `wp_enqueue_script` (footer) | Form pages only | No |

**No other JS dependencies.** The theme does not load:
- jQuery (unless a third-party plugin requires it)
- MooTools (removed from archived site)
- Lodash or Underscore
- React, Vue, or Alpine.js (not needed for this site)
- jQuery UI
- Moment.js or Day.js (use native `Intl.DateTimeFormat`)

---

## 4. Loading via `wp_enqueue_script`

### Swiper.js (home page only)

```php
// ollmh-theme/includes/class-ollmh-assets.php

public static function enqueue_slideshow(): void {
    if (!is_front_page()) {
        return;
    }
    wp_enqueue_style(
        'swiper',
        'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css',
        [],
        '11.1.0'
    );
    wp_enqueue_script(
        'swiper',
        'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js',
        [],
        '11.1.0',
        true  // Load in footer
    );
    wp_enqueue_script(
        'ollmh-slideshow',
        OLLMH_THEME_URI . '/assets/js/slideshow.js',
        ['swiper'],
        OLLMH_THEME_VERSION,
        true
    );
}
add_action('wp_enqueue_scripts', ['OLLMH_Assets', 'enqueue_slideshow']);
```

### GLightbox (gallery page only)

```php
public static function enqueue_gallery(): void {
    if (!is_page('ollmh-outlook') && !is_post_type_archive('outlook_album')) {
        return;
    }
    wp_enqueue_style(
        'glightbox',
        'https://cdn.jsdelivr.net/npm/glightbox/dist/css/glightbox.min.css',
        [],
        '3.3.0'
    );
    wp_enqueue_script(
        'glightbox',
        'https://cdn.jsdelivr.net/npm/glightbox/dist/js/glightbox.min.js',
        [],
        '3.3.0',
        true
    );
    wp_enqueue_script(
        'ollmh-gallery',
        OLLMH_THEME_URI . '/assets/js/gallery.js',
        ['glightbox'],
        OLLMH_THEME_VERSION,
        true
    );
}
```

### Turnstile (form pages only)

```php
public static function enqueue_turnstile(): void {
    if (!is_page('contacts') && !is_page('out-patient-dept') &&
        !is_page('medical-school-application-form') && !is_singular('event')) {
        return;
    }
    $site_key = OLLMH_Helpers::get_setting('turnstile_site_key');
    if (!$site_key) {
        return;
    }
    wp_enqueue_script(
        'cloudflare-turnstile',
        'https://challenges.cloudflare.com/turnstile/v0/api.js',
        [],
        null,
        true
    );
    wp_localize_script('cloudflare-turnstile', 'ollmhTurnstile', [
        'siteKey' => $site_key,
    ]);
}
```

### Theme main JS (all pages)

```php
public static function enqueue_main(): void {
    wp_enqueue_script(
        'ollmh-main',
        OLLMH_THEME_URI . '/assets/js/main.js',
        [],
        OLLMH_THEME_VERSION,
        true  // Footer
    );
    wp_localize_script('ollmh-main', 'ollmhConfig', [
        'ajaxUrl' => admin_url('admin-ajax.php'),
        'restUrl' => esc_url_raw(rest_url('ollmh/v1')),
        'nonce'   => wp_create_nonce('wp_rest'),
    ]);
}
```

---

## 5. Icons

**No icon font library** (no Font Awesome, no Material Icons). Use inline
SVG icons instead — they are lighter, more accessible, and styleable via
CSS.

### SVG icon system

```html
<!-- Inline SVG icon -->
<svg class="icon" width="20" height="20" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
  <path d="M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0z"/>
</svg>
```

Store commonly used icons as PHP includes:

```php
// ollmh-theme/includes/icons.php
function ollmh_icon(string $name, int $size = 20): string {
    $icons = [
        'phone'   => '<path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>',
        'email'   => '<path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>',
        'clock'   => '<path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/><path d="M12.5 7H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>',
        'location' => '<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>',
        'facebook' => '<path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H8v-3h2V9.5C10 7.57 11.57 6 13.5 6H16v3h-2c-.55 0-1 .45-1 1v2h3v3h-3v6.95c5.05-.5 9-4.76 9-9.95z"/>',
        'youtube'  => '<path d="M21.58 7.19c-.23-.86-.91-1.54-1.77-1.77C18.25 5 12 5 12 5s-6.25 0-7.81.42c-.86.23-1.54.91-1.77 1.77C2 8.75 2 12 2 12s0 3.25.42 4.81c.23.86.91 1.54 1.77 1.77C5.75 19 12 19 12 19s6.25 0 7.81-.42c.86-.23 1.54-.91 1.77-1.77C22 15.25 22 12 22 12s0-3.25-.42-4.81zM10 15V9l5.2 3-5.2 3z"/>',
    ];
    return sprintf(
        '<svg class="icon icon-%s" width="%d" height="%d" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s</svg>',
        esc_attr($name),
        $size,
        $size,
        $icons[$name] ?? ''
    );
}
```

---

## 6. Fonts

The OLLMH theme uses a **system font stack** (no web fonts loaded):

```css
--font-serif: Georgia, 'Times New Roman', Times, serif;
--font-sans: 'Helvetica Neue', Helvetica, Arial, sans-serif;
```

**Rationale:**
- Zero font loading delay (no FOUT/FOIT)
- No external requests to Google Fonts
- Consistent with the archived site's typography (see [`FONT-SCHEMA.md`](./FONT-SCHEMA.md))
- Smaller page weight

If a custom font is desired later, use `font-display: swap` and preload
only the weights actually used.

---

## 7. Version pinning and SRI

All CDN-loaded libraries use pinned versions (not `@latest`) and include
SRI hashes for security:

```php
wp_enqueue_script(
    'swiper',
    'https://cdn.jsdelivr.net/npm/swiper@11.1.0/swiper-bundle.min.js',
    [],
    '11.1.0',
    true
);
// Add SRI hash via script_loader_tag filter
add_filter('script_loader_tag', function($tag, $handle) {
    if ($handle === 'swiper') {
        $tag = str_replace(
            ' src=',
            ' integrity="sha384-..." crossorigin="anonymous" src=',
            $tag
        );
    }
    return $tag;
}, 10, 2);
```

---

## 8. What we explicitly avoid

| Library | Reason for avoidance |
|---|---|
| Bootstrap 5 | Unnecessary — custom CSS is lighter and more specific |
| Tailwind CSS | Utility-first CSS doesn't match the documented design system approach |
| jQuery UI | Not needed — tabs and sliders use Swiper.js and vanilla JS |
| Font Awesome | 300KB+ for icons we can do with 5KB of inline SVG |
| Google Fonts | Adds external request and FOUT; system fonts are sufficient |
| Moment.js | Deprecated; use native `Intl.DateTimeFormat` |
| Lodash | Most utilities are now native in ES6+ |
| React/Vue/Alpine | Not needed — the site is server-rendered with progressive enhancement |
| GSAP | Overkill for the simple animations needed |
| AOS (Animate On Scroll) | Use CSS `@media (prefers-reduced-motion)` and simple transitions |
