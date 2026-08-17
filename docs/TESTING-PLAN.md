# Testing Plan

> This document defines the testing strategy and verification checklist for
> the OLLMH WordPress site — pre-launch, launch, and post-launch.
>
> **Related:** [`MIGRATION-PLAN.md`](./MIGRATION-PLAN.md) Phase 7,
> [`DEPLOYMENT.md`](./DEPLOYMENT.md) for deployment.

---

## 1. Testing phases

| Phase | When | Environment | Goal |
|---|---|---|---|
| Unit testing | During development | Local | Verify PHP classes and functions work correctly |
| Integration testing | After each phase | Local/Staging | Verify components work together |
| UAT (User Acceptance) | Before launch | Staging | Hospital staff verify content and functionality |
| Pre-launch checklist | Before going live | Production | Final verification on production |
| Post-launch monitoring | 48 hours after launch | Production | Catch any live issues |

---

## 2. Unit testing

### Framework: PHPUnit + WP-CLI

> **Dev-only:** WP-CLI test scaffolding and PHPUnit tests run in the
> development environment only. Tests are never run on production (cPanel
> shared hosting, no WP-CLI) — see
> [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md) → ADR-005.

```bash
# Install WP-CLI testing framework
docker exec ollmh-wp wp scaffold plugin-tests ollmh-core --allow-root

# Run tests
docker exec ollmh-wp phpunit --allow-root
```

### What to test

| Component | Test cases |
|---|---|
| `OLLMH_Settings_Seeder` | Seeds all settings, doesn't overwrite customised values, handles re-runs |
| `OLLMH_CPT` | All 15 CPTs register without errors, taxonomies register, rewrite rules generate |
| `OLLMH_Capabilities` | Editor has `edit_news_article` but not `manage_options`, Author has `edit_news_article` but not `edit_others_news_article` |
| `OLLMH_Validation` | Email validation, phone validation, required fields, max length |
| `OLLMH_Turnstile` | Valid token passes, invalid token fails, missing token fails |
| `OLLMH_Mpesa` | STK Push request format, callback parsing, token caching |

---

## 3. Integration testing checklist

### Database

- [ ] All 81 tables created on plugin activation
- [ ] Settings seeder populates ~100 settings
- [ ] Content seeders populate departments, staff, pages, menus
- [ ] Tables use `utf8mb4` charset and `utf8mb4_unicode_ci` collation
- [ ] Foreign key constraints are valid
- [ ] `dbDelta()` runs without errors on re-activation

### CPTs and taxonomies

- [ ] All 15 CPTs appear in the admin sidebar
- [ ] All 4 taxonomies appear under their parent CPTs
- [ ] CPT archive URLs work (`/news/`, `/events/`, `/departments/`, etc.)
- [ ] CPT single URLs work (`/news/article-slug/`)
- [ ] Taxonomy archive URLs work (`/news/category/announcements/`)
- [ ] `has_archive` CPTs have archive pages
- [ ] Non-public CPTs (ward, clinic, special_service) don't have front-end archives

### Theme

- [ ] Home page renders with slideshow, tabs, news scroller, department columns
- [ ] Header renders with logo, main menu, top bar (hidden on mobile)
- [ ] Footer renders with link columns, contact info, social icons
- [ ] All 20 page templates render correctly
- [ ] Breadcrumbs display on inner pages
- [ ] 404 page renders for non-existent URLs
- [ ] Search results page renders
- [ ] Sidebar widgets display correctly

### Forms

- [ ] Contact form submits via AJAX and shows success message
- [ ] Contact form validation works (required fields, email format)
- [ ] Contact form saves to `wp_contact_submissions`
- [ ] Contact form sends email to `admin_email`
- [ ] Contact form sends auto-reply to submitter
- [ ] Appointment form validates date/time constraints
- [ ] Appointment form generates reference number
- [ ] Application form multi-step navigation works (step 1 → 2 → 3 → 4)
- [ ] Application form document upload works (file size, type validation)
- [ ] Application form M-Pesa STK Push triggers (sandbox)
- [ ] Event registration form works
- [ ] Turnstile widget renders on all forms
- [ ] Turnstile validation fails on invalid token
- [ ] Rate limiting works (5 contact submissions per 10 min per IP)

### Notifications

- [ ] Email notifications are queued (not sent synchronously)
- [ ] Cron job processes notification queue
- [ ] Appointment reminder emails send 24 hours before appointment
- [ ] Application status update emails send on status change
- [ ] SMS notifications send (if enabled)
- [ ] MailHog catches all emails in local dev

### Admin

- [ ] Admin sidebar shows all 20 top-level menus
- [ ] Settings page shows 19 group tabs
- [ ] Settings can be updated and saved
- [ ] `is_public=0` settings are not exposed via REST API
- [ ] `type=secret` settings are masked in the admin UI
- [ ] CPT list tables show custom columns
- [ ] CPT edit screens show custom meta boxes
- [ ] User role capabilities are correct (Editor can edit all CPTs, Author can edit own only)

---

## 4. Cross-browser testing

Test on these browsers (latest stable versions):

| Browser | OS | Priority |
|---|---|---|
| Chrome | Windows, macOS, Android | High |
| Safari | macOS, iOS | High |
| Firefox | Windows, macOS | Medium |
| Edge | Windows | Medium |
| Samsung Internet | Android | Medium (popular in Kenya) |
| Opera | Windows, Android | Low |

**Test on real devices where possible.** Use BrowserStack or LambdaTest
for cross-platform testing if physical devices aren't available.

### What to check per browser

- [ ] Page layout renders correctly (no broken grids)
- [ ] Slideshow auto-plays and navigation works
- [ ] Tabs switch correctly
- [ ] News scroller auto-advances
- [ ] Mobile menu toggles
- [ ] Forms submit and validate
- [ ] Turnstile widget renders
- [ ] Images load (no broken images)
- [ ] Fonts render (system font stack)

---

## 5. Mobile testing

Test on these screen sizes:

| Device | Width | Priority |
|---|---|---|
| iPhone SE | 375px | High |
| iPhone 12/13/14 | 390px | High |
| Samsung Galaxy S22 | 360px | High |
| iPad Mini | 768px | Medium |
| iPad Pro | 1024px | Medium |

### What to check per device

- [ ] Layout stacks correctly (single column on mobile)
- [ ] Mobile hamburger menu works
- [ ] Touch targets are ≥ 44px (buttons, links, form inputs)
- [ ] No horizontal scroll on any page
- [ ] Images are responsive (srcset works)
- [ ] Forms are usable (inputs are 16px font to prevent iOS zoom)
- [ ] Slideshow is touch-swipeable
- [ ] No layout shift on image load

---

## 6. SEO verification

- [ ] All pages have unique `<title>` tags
- [ ] All pages have meta descriptions
- [ ] Canonical URLs are set
- [ ] Open Graph tags are present (`og:title`, `og:description`, `og:image`)
- [ ] Twitter Card tags are present
- [ ] XML sitemap is generated at `/sitemap_index.xml`
- [ ] Robots.txt is correct (allows indexing, blocks `/wp-admin/`)
- [ ] `robots` meta tag matches `seo_robots_default` setting
- [ ] JSON-LD schema is present on all pages (Hospital, MedicalBusiness, BreadcrumbList)
- [ ] Breadcrumbs render and have BreadcrumbList schema
- [ ] All internal links use HTTPS
- [ ] No broken links (run Broken Link Checker)
- [ ] All 17 old `.html` URLs redirect with 301

---

## 7. Performance testing

- [ ] Run Google PageSpeed Insights on all key pages
- [ ] Mobile PageSpeed score ≥ 80
- [ ] Desktop PageSpeed score ≥ 90
- [ ] LCP (Largest Contentful Paint) < 2.5s
- [ ] FID (First Input Delay) < 100ms
- [ ] CLS (Cumulative Layout Shift) < 0.1
- [ ] Total page weight < 2MB (excluding cache)
- [ ] Images are optimized (WebP format, lazy loaded)
- [ ] CSS is minified
- [ ] JS is minified and loaded in footer
- [ ] W3 Total Cache is active
- [ ] Gzip/Brotli compression is enabled
- [ ] Browser caching headers are set

See [`PERFORMANCE-BUDGET.md`](./PERFORMANCE-BUDGET.md) for detailed targets.

---

## 8. Security testing

- [ ] SSL certificate is valid (no mixed content)
- [ ] `wp-config.php` is not publicly accessible
- [ ] `DISALLOW_FILE_EDIT` is set
- [ ] Admin login is protected (strong passwords, 2FA if enabled)
- [ ] `xmlrpc.php` is disabled or protected
- [ ] REST API requires authentication for non-public endpoints
- [ ] All form submissions are protected by Turnstile
- [ ] SQL injection protection (all queries use `$wpdb->prepare()`)
- [ ] XSS protection (all output is escaped with `esc_html`, `esc_attr`, `esc_url`)
- [ ] CSRF protection (all forms include WordPress nonce)
- [ ] File upload validation (MIME type, extension, size)
- [ ] `wp-content/uploads/` does not execute PHP
- [ ] Security headers are set (X-Frame-Options, X-Content-Type-Options, HSTS)

See [`SECURITY-HARDENING.md`](./SECURITY-HARDENING.md) for full details.

---

## 9. Accessibility testing

- [ ] All images have alt text (or `alt=""` for decorative images)
- [ ] Form fields have associated `<label>` elements
- [ ] Color contrast meets WCAG AA (4.5:1 for normal text, 3:1 for large text)
- [ ] Keyboard navigation works (Tab through all interactive elements)
- [ ] Focus indicators are visible
- [ ] Skip-to-content link is present
- [ ] ARIA landmarks are present (`role="banner"`, `role="main"`, `role="contentinfo"`)
- [ ] Heading hierarchy is correct (one `<h1>`, then `<h2>`, etc.)
- [ ] Screen reader test (NVDA on Windows or VoiceOver on macOS)
- [ ] `prefers-reduced-motion` is respected (disable animations)

See [`ACCESSIBILITY.md`](./ACCESSIBILITY.md) for full details.

---

## 10. Content verification

- [ ] All 20 pages have content (no empty pages)
- [ ] 3 placeholder pages have content (in-patient-dept, clinic-days, about-nursing-school)
- [ ] All images display (no broken images)
- [ ] All internal links work (no 404s)
- [ ] All external links are valid (no dead links)
- [ ] No Joomla-specific content remains (no `administrator/` links, no Joomla classes)
- [ ] No Wayback Machine artifacts remain
- [ ] Contact information is correct (phone, email, address)
- [ ] Social media links point to correct profiles
- [ ] Footer copyright year is current

---

## 11. User Acceptance Testing (UAT)

Have hospital staff (Administrator role) perform these tasks:

### Content management
- [ ] Create a new news article and publish it
- [ ] Edit an existing department page
- [ ] Upload a new staff member with a photo
- [ ] Create a new event
- [ ] Add a new gallery album with images

### Settings
- [ ] Update the hospital phone number in Platform Config
- [ ] Change the homepage hero title
- [ ] Toggle maintenance mode on and off
- [ ] Update social media links

### Form management
- [ ] View contact form submissions in the admin
- [ ] View appointment bookings in the admin
- [ ] Review a nursing school application and change its status
- [ ] Verify applicant received status update email

---

## 12. Post-launch monitoring (48 hours)

- [ ] Check `debug.log` for PHP errors every 4 hours
- [ ] Check Google Search Console for crawl errors
- [ ] Check Broken Link Checker for new broken links
- [ ] Monitor server resource usage (CPU, memory, disk)
- [ ] Check that cron jobs are running (WP Crontrol)
- [ ] Check that backups are running (backup plugin logs)
- [ ] Monitor Cloudflare analytics for traffic and threats
- [ ] Test all forms on production (contact, appointment, application)
- [ ] Verify M-Pesa payments in production mode
- [ ] Check email delivery (no bounce notifications)
