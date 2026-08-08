# Performance Budget

> This document defines page weight targets, image optimization strategy,
> and Core Web Vitals targets for the OLLMH WordPress site.
>
> **Related:** [`SEO-STRATEGY.md`](./SEO-STRATEGY.md) for SEO performance,
> [`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md) for
> dependency choices.

---

## 1. Core Web Vitals targets

Google's Core Web Vitals are the primary performance metrics. They affect
both SEO rankings and user experience.

| Metric | Target | Measurement | Weight |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s | Time until largest visible element renders | High |
| **INP** (Interaction to Next Paint) | < 200ms | Time until first user interaction is responded to | High |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Sum of layout shift scores | High |
| **FCP** (First Contentful Paint) | < 1.8s | Time until first content renders | Medium |
| **TTFB** (Time to First Byte) | < 800ms | Server response time | Medium |
| **TBT** (Total Blocking Time) | < 200ms | Sum of long tasks that block the main thread | Medium |

**Tools to measure:**
- [PageSpeed Insights](https://pagespeed.web.dev/) — Google's official tool
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) — Chrome DevTools
- [WebPageTest](https://www.webpagetest.org/) — Detailed waterfall analysis
- [Chrome UX Report](https://developer.chrome.com/docs/crux/) — Real user data

---

## 2. Page weight budget

| Asset type | Budget per page | Notes |
|---|---|---|
| HTML | < 50 KB | Server-rendered, gzipped |
| CSS | < 50 KB | Single minified file, gzipped |
| JS | < 80 KB | All JS combined, minified, gzipped |
| Images | < 500 KB | First viewport only; rest lazy-loaded |
| Fonts | 0 KB | System font stack (no web fonts) |
| **Total first view** | **< 700 KB** | Excluding cached assets |

**Pages with heavier content (gallery, slideshow):**
| Page | Budget | Notes |
|---|---|---|
| Home (with slideshow) | < 1.2 MB | Slideshow images are the main weight |
| Gallery | < 2 MB | Lazy-loaded thumbnails; full images on click |

---

## 3. Image optimization

### 3.1 Format strategy

| Format | Use case | Notes |
|---|---|---|
| **WebP** | All photos | 25-35% smaller than JPEG, supported by all modern browsers |
| **AVIF** | Future optimization | 50% smaller than JPEG, supported in Chrome/Firefox |
| **PNG** | Graphics with transparency | Logos, icons |
| **SVG** | Icons, simple graphics | Scalable, tiny file size |
| **GIF** | Avoid | Convert to MP4/WebM or replace with CSS animation |

### 3.2 WordPress image handling

- Use **ShortPixel** or **Imagify** plugin for automatic WebP conversion
- Register custom image sizes (see [`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md)):
  - `ollmh-hero`: 1920×600 (slideshow)
  - `ollmh-card`: 600×400 (cards)
  - `ollmh-thumbnail`: 300×200 (thumbnails)
  - `ollmh-staff`: 400×400 (portraits)
  - `ollmh-gallery`: 1200×800 (gallery, no crop)
  - `ollmh-og`: 1200×630 (Open Graph)
- WordPress auto-generates `srcset` for responsive images
- Use `loading="lazy"` on all below-the-fold images
- Use `fetchpriority="high"` on the LCP image (above-the-fold hero)

### 3.3 Slideshow optimization

The home page slideshow is the heaviest element. Optimize:

1. Preload only the first slide (`fetchpriority="high"`)
2. Lazy-load remaining slides (`loading="lazy"`)
3. Use WebP format for all slide images
4. Compress each slide to < 150 KB
5. Use Swiper.js lazy loading (`lazy: { loadPrevNext: true }`)

### 3.4 Gallery optimization

1. Display thumbnails (300×200) in a grid
2. Load full-size image (1200×800) only when lightbox is opened
3. Use `loading="lazy"` on all thumbnails
4. Use WebP format

---

## 4. CSS optimization

- **Single file:** All CSS concatenated into one file (`style.css` or
  `assets/dist/style.min.css`)
- **Minified:** Remove comments, whitespace, unnecessary semicolons
- **Gzip/Brotli:** Server compresses CSS before sending
- **Critical CSS:** Inline above-the-fold CSS for faster FCP (WP Rocket
  does this automatically)
- **No `@import`:** Use `wp_enqueue_style` with dependencies instead
- **No unused CSS:** Don't load Bootstrap/Tailwind if only using 5% of it

### CSS size breakdown (target)

| File | Unminified | Minified+gzip | Content |
|---|---|---|---|
| `base.css` | 8 KB | 2 KB | Reset, variables, typography |
| `layout.css` | 12 KB | 3 KB | Grid, header, footer |
| `components.css` | 20 KB | 5 KB | Buttons, cards, forms, tables |
| `pages.css` | 15 KB | 4 KB | Page-specific styles |
| `responsive.css` | 10 KB | 2 KB | Media queries |
| `print.css` | 2 KB | 0.5 KB | Print styles |
| **Total** | **67 KB** | **~16 KB** | |

---

## 5. JavaScript optimization

- **Minified:** All JS minified via Terser or WordPress's built-in minification
- **Footer loading:** All JS loads in the footer (`$in_footer = true`)
- **Deferred:** Use `defer` attribute for non-critical JS
- **No inline JS:** All JS in external files (allows caching)
- **Conditional loading:** Only load JS needed for the current page (slideshow on home, gallery on gallery page, forms on form pages)

### JS size breakdown (target)

| File | Minified+gzip | Loaded on |
|---|---|---|
| `main.js` | 5 KB | All pages |
| `slideshow.js` + Swiper | 40 KB | Home page only |
| `tabs.js` | 1 KB | Pages with tabs |
| `news-scroller.js` | 2 KB | Home page only |
| `gallery.js` + GLightbox | 20 KB | Gallery page only |
| `forms.js` | 8 KB | Form pages only |
| Turnstile API | ~15 KB | Form pages only |

---

## 6. Caching strategy

### 6.1 Page caching (WP Rocket)

- Cache all public pages as static HTML
- Cache lifetime: 24 hours (or until content changes)
- Auto-clear cache on post save/update
- Preload cache via sitemap (warm the cache for all pages)
- Mobile-specific cache (separate cache for mobile devices)

### 6.2 Object caching (Redis or Memcached)

- If using a VPS, install Redis and the Redis Object Cache plugin
- Caches database query results in memory
- Reduces TTFB by 30-50%

### 6.3 Browser caching

```nginx
# Nginx — static asset caching
location ~* \.(js|css|png|jpg|jpeg|gif|svg|webp|ico|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

```apache
# Apache .htaccess
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/css "access plus 1 year"
ExpiresByType application/javascript "access plus 1 year"
ExpiresByType image/jpeg "access plus 1 year"
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/webp "access plus 1 year"
ExpiresByType image/svg+xml "access plus 1 year"
</IfModule>
```

### 6.4 CDN (Cloudflare)

- Route all traffic through Cloudflare (free plan is sufficient)
- Cloudflare caches static assets at edge locations
- Reduces TTFB for international visitors
- Auto-minifies HTML, CSS, JS at the edge

---

## 7. Database optimization

- Use `wp_settings` for configuration (single-row reads, cached by WordPress object cache)
- Use WordPress transients for expensive queries (clinic schedules, department lists)
- Set `cache_clinic_schedule_ttl_seconds` to 86400 (24 hours) — clinic schedules rarely change
- Index all foreign key columns (already done in schema definitions)
- Run `OPTIMIZE TABLE` weekly (see [`CRON-JOBS.md`](./CRON-JOBS.md))
- Limit `WP_POST_REVISIONS` to 5 (prevents database bloat)

---

## 8. Server optimization

### PHP-FPM tuning

```ini
; /etc/php/8.2/fpm/php.ini
memory_limit = 256M
max_execution_time = 30
opcache.enable = 1
opcache.memory_consumption = 128
opcache.max_accelerated_files = 10000
opcache.revalidate_freq = 180
```

### MySQL tuning

```ini
; /etc/mysql/my.cnf
innodb_buffer_pool_size = 1G    ; 50-70% of available RAM
innodb_log_file_size = 256M
query_cache_size = 0            ; Remove in MySQL 8.0 (not needed)
max_connections = 100
```

### HTTP/2

Enable HTTP/2 on the web server (Nginx or Apache) for multiplexing —
allows the browser to download multiple assets in parallel over a single
connection.

---

## 9. Monitoring

| Metric | Tool | Frequency | Alert threshold |
|---|---|---|---|
| Core Web Vitals | PageSpeed Insights API | Weekly | LCP > 4s, CLS > 0.25 |
| TTFB | Uptime monitor | Every 5 min | > 2s |
| Page weight | Lighthouse | Weekly | > 2 MB |
| Server CPU | Server monitoring | Continuous | > 80% for 5 min |
| Server memory | Server monitoring | Continuous | > 90% for 5 min |
| Database size | Custom admin dashboard widget | Monthly | > 1 GB |

---

## 10. Performance checklist (pre-launch)

- [ ] WP Rocket is installed and configured
- [ ] Page caching is active
- [ ] CSS minification is enabled
- [ ] JS minification is enabled
- [ ] Lazy loading is enabled for images
- [ ] WebP conversion is enabled (ShortPixel or Imagify)
- [ ] Critical CSS is generated
- [ ] Database optimization is scheduled (weekly cron)
- [ ] Cloudflare CDN is configured
- [ ] Gzip/Brotli compression is enabled
- [ ] HTTP/2 is enabled
- [ ] OPcache is enabled
- [ ] Redis object cache is configured (if VPS)
- [ ] Mobile PageSpeed score ≥ 80
- [ ] Desktop PageSpeed score ≥ 90
- [ ] LCP < 2.5s on all key pages
- [ ] CLS < 0.1 on all key pages
- [ ] Total page weight < 700 KB (first view)
