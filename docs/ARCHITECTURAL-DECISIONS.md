# Architectural Decisions

> This document records the formal architectural decisions for the OLLMH
> WordPress rebuild. Each decision includes the context, the decision
> itself, the rationale, and the implications for the implementation.
>
> These decisions supersede any conflicting guidance in other
> documentation files. Where a conflict exists, this document is
> authoritative.

---

## ADR-001: Child theme extending Twenty Twenty-Five (block/FSE)

**Status:** Approved
**Date:** 2024
**Supersedes:** THEME-ARCHITECTURE.md §1 (previously: standalone classic
PHP theme)

### Context

The OLLMH WordPress rebuild needs a theme that:
- Presents the hospital's content (services, departments, news, events,
  nursing school, projects) in a professional, accessible layout
- Supports custom post types (news articles, events, departments, staff,
  projects, gallery albums) with custom layouts
- Is maintainable by the client's ICT team after handover
- Stays compatible with the latest WordPress core updates

The initial documentation proposed a standalone classic PHP theme with
custom `header.php`, `footer.php`, `single-*.php`, and `page-templates/`
files. On review, this approach places the full maintenance burden on the
client's team — every WordPress core update, every deprecation, every
new block editor feature requires manual integration into the custom
theme.

### Decision

The OLLMH theme will be a **custom child theme extending the official
WordPress Twenty Twenty-Five theme** (the default block theme shipped
with WordPress 6.7+).

Twenty Twenty-Five is a **block theme / Full Site Editing (FSE) theme**.
The child theme inherits:

- Block-based template structure (`templates/*.html`)
- `theme.json` design token system (colors, typography, spacing)
- Site Editor compatibility for layout adjustments
- Block patterns for reusable content layouts
- WordPress core's block rendering, styling, and responsive behavior

The child theme adds:

- A `theme.json` that overrides the parent's color palette with the
  OLLMH brand colors (see [`COLOR-SCHEMA.md`](./COLOR-SCHEMA.md)) and
  the OLLMH font stack (see [`FONT-SCHEMA.md`](./FONT-SCHEMA.md))
- Custom block templates / template parts for OLLMH-specific page layouts
  (home page, departments grid, staff grid, clinic schedule, gallery,
  news listing, events listing)
- A `functions.php` that enqueues custom CSS and vanilla JS, registers
  custom image sizes, and provides theme-level helpers (breadcrumbs,
  schema output, template helpers)
- Classic PHP template files for complex CPT pages where block templates
  are insufficient (multi-step application form, single news article with
  custom layout, single event with registration form) — WordPress
  supports this hybrid approach: PHP template files take precedence over
  block templates in the template hierarchy
- Custom block patterns for OLLMH-specific content blocks (department
  card, staff card, clinic schedule table, ward status table, news
  scroller, hero slideshow)

### Rationale

1. **Reduced maintenance burden:** The parent theme (Twenty Twenty-Five)
   is maintained by the WordPress core team. Core updates, security
   patches, and block editor improvements flow to the child theme
   automatically. The client's ICT team maintains only the overrides,
   not the entire theme.
2. **WordPress core alignment:** Extending the official default theme
   ensures maximum compatibility with current and future WordPress core
   releases. The child theme inherits the parent's tested template
   structure, block markup, and responsive behavior.
3. **Block editor support:** Hospital staff can use the Site Editor to
   make minor layout adjustments (reorder sections, change hero images,
   edit text) without touching PHP code — appropriate for non-technical
   content managers.
4. **Hybrid flexibility:** Where block templates are insufficient (complex
   forms, custom CPT layouts), classic PHP template files override the
   block templates. This gives the best of both worlds: block editor
   simplicity for standard pages, PHP power for complex pages.
5. **Design token inheritance:** The child theme's `theme.json` extends
   the parent's, so the block editor's color picker, font size selector,
   and spacing controls all use OLLMH brand values — no custom CSS needed
   for block styling.

### Implications

- **THEME-ARCHITECTURE.md is updated:** §1 (theme type) and §2
  (directory structure) are rewritten to reflect the child theme
  architecture. The template hierarchy mapping (§3) is updated —
  standard pages use block templates, CPT pages use PHP templates.
- **`functions.php` is retained:** The child theme has a `functions.php`
  that loads PHP classes for asset enqueuing, image sizes, breadcrumbs,
  schema output, and template helpers. This is standard for block child
  themes — `functions.php` works the same in classic and block themes.
- **Custom CSS is retained:** The child theme enqueues custom CSS via
  `wp_enqueue_style()` for styling that `theme.json` cannot express
  (complex layouts, animations, third-party library styling). See
  ADR-003 below.
- **Vanilla JS is retained:** The child theme enqueues vanilla ES6+ JS
  via `wp_enqueue_script()`. See ADR-002 below.
- **Block patterns replace some template parts:** Reusable content
  layouts (department card, staff card, hero section, CTA band) are
  registered as block patterns rather than PHP template parts, making
  them available in the Site Editor.
- **CPT registration stays in the plugin:** Custom post types and
  taxonomies are registered in `ollmh-core` (the plugin), not the theme.
  This is unchanged — CPTs survive theme switches regardless of theme
  type.

### WordPress version target

WordPress 6.7+ (Twenty Twenty-Five is the default theme for WP 6.7,
released November 2024). The child theme requires the block editor
infrastructure introduced in WP 5.0 and refined through 6.x.

---

## ADR-002: Cloudflare Turnstile with vanilla JavaScript

**Status:** Approved
**Date:** 2024

### Context

All public-facing forms on the OLLMH site (contact, appointment booking,
nursing school application, event registration, newsletter signup) require
bot protection to prevent spam submissions, credential stuffing, and
abuse of the M-Pesa payment trigger.

The site must remain on the client's existing cPanel shared hosting
infrastructure. The bot protection solution must not require DNS changes,
CDN proxying, or migration to Cloudflare's network.

### Decision

The OLLMH site uses **Cloudflare Turnstile** for bot protection on all
public forms. The Turnstile widget is integrated using **vanilla
JavaScript** (no jQuery dependency) to optimize performance and minimize
front-end dependencies.

Turnstile is a standalone product from Cloudflare that:
- Does **not** require the site to be proxied through Cloudflare's CDN
- Does **not** require DNS changes or nameserver migration
- Works on any hosting environment (cPanel shared, VPS, dedicated)
- Requires only a free Cloudflare account to obtain API keys (site key
  and secret key)
- Provides an invisible, privacy-friendly challenge (no image selection,
  no checkbox — users never see it unless suspicious)

### Implementation

**Front-end rendering** (vanilla JS, no jQuery):

```html
<!-- Turnstile API script — enqueued via wp_enqueue_script() -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

<!-- Inside each form -->
<div class="cf-turnstile" data-sitekey="SITE_KEY" data-theme="light"></div>
```

The `data-sitekey` is populated from the `turnstile_site_key` setting
(retrieved via the public settings REST API endpoint).

**Token handling** (vanilla JS form handler):

```javascript
// assets/js/forms.js — vanilla ES6+, no jQuery

document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('.ollmh-form');

  forms.forEach((form) => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const turnstileToken = form.querySelector('[name="cf-turnstile-response"]')?.value;
      if (!turnstileToken) {
        showError('turnstile', 'Please complete the bot verification.');
        return;
      }

      // Include token in API request body
      const payload = getFormData(form);
      payload.turnstile_token = turnstileToken;

      try {
        const response = await fetch(ollmhConfig.restUrl + form.dataset.endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-WP-Nonce': ollmhConfig.nonce,
          },
          body: JSON.stringify(payload),
        });
        // ... handle response
      } catch (err) {
        // ... handle error
      }
    });
  });
});
```

**Server-side verification:**

Each REST API endpoint that accepts form submissions calls the internal
`Turnstile::verify()` method, which POSTs to Cloudflare's `siteverify`
endpoint with the secret key and token. If verification fails, the
endpoint returns HTTP 400 with an error message. See
[`REST-API-SPEC.md`](./REST-API-SPEC.md) §3.7 for the verification
endpoint specification.

**Reset after submission:**

After a successful or failed submission, the Turnstile widget is reset
so the user can submit again:

```javascript
turnstile.reset(form.querySelector('.cf-turnstile'));
```

### Rationale

1. **No infrastructure changes:** Turnstile works on the existing cPanel
   hosting without DNS changes, nameserver migration, or CDN proxying.
   The client's ICT team requirement to remain on their existing
   infrastructure is fully satisfied.
2. **Vanilla JS for performance:** The OLLMH child theme uses vanilla
   ES6+ JavaScript throughout (see [`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md)).
   The Turnstile integration follows this standard — no jQuery dependency
   is introduced. This keeps the JS bundle minimal and avoids loading
   jQuery solely for form handling.
3. **Privacy-friendly:** Turnstile does not use Google tracking cookies
   and does not require users to solve image challenges. This aligns
   with the Kenya Data Protection Act 2019 compliance strategy (see
   [`COOKIE-CONSENT.md`](./COOKIE-CONSENT.md)) — Turnstile is classified
   as an essential cookie and does not require consent under advertising
   or analytics categories.
4. **User experience:** Turnstile's invisible challenge means legitimate
   users never see a captcha widget. Only suspicious traffic is
   challenged. This is superior to reCAPTCHA v2 (checkbox + image
   selection) and comparable to reCAPTCHA v3 (score-based) without
   Google's tracking overhead.

### Settings

Turnstile configuration is stored in `wp_settings` → `security` group
(see [`SETTINGS.md`](./SETTINGS.md)):

| Setting | Description |
|---|---|
| `turnstile_site_key` | Turnstile site key (public, returned by settings API) |
| `turnstile_secret_key` | Turnstile secret key (private, encrypted, never exposed to front-end) |
| `captcha_on_contact_form` | Enable/disable captcha on the contact form |
| `captcha_on_appointment_booking` | Enable/disable captcha on the appointment form |
| `captcha_on_application_form` | Enable/disable captcha on the application form |

### Child theme compatibility

The Turnstile integration is fully compatible with the child theme
extending Twenty Twenty-Five:

- The Turnstile API script is enqueued via `wp_enqueue_script()` in the
  child theme's `functions.php` → `class-ollmh-assets.php`, loaded only
  on pages that contain forms
- The Turnstile widget `<div>` is rendered inside form templates —
  whether the form is in a block template (block pattern) or a classic
  PHP template (CPT single page), the widget renders identically
- The vanilla JS form handler is enqueued via `wp_enqueue_script()` and
  works regardless of whether the page is rendered via block templates
  or PHP templates — the JS queries the DOM by class name, not by
  template type
- No block editor integration is needed — Turnstile is a front-end-only
  widget that does not interact with the block editor

---

## ADR-003: No Tailwind CSS — pure CSS and native WordPress styling

**Status:** Approved
**Date:** 2024

### Context

The OLLMH child theme needs a CSS architecture that is lightweight,
maintainable, and compatible with the WordPress block editor (Gutenberg)
and Full Site Editing (FSE) introduced by the Twenty Twenty-Five parent
theme.

### Decision

The OLLMH project will **not** use Tailwind CSS or any external CSS
framework. The CSS architecture relies on:

1. **`theme.json` design tokens** — the primary styling mechanism for
   block editor content. The child theme's `theme.json` extends the
   parent's with OLLMH brand colors, font families, font sizes, and
   spacing scales. These tokens automatically style all core blocks
   (paragraphs, headings, buttons, columns, groups, images, etc.) in
   the block editor and on the front end.
2. **Pure CSS (custom properties + Grid + Flexbox)** — for styling that
   `theme.json` cannot express: complex layouts (home page slideshow +
   tabs + news scroller + department columns), third-party library
   styling (Swiper, GLightbox, Turnstile), animations, and
   page-specific styles. These are enqueued via `wp_enqueue_style()`.
3. **WordPress native styling** — the child theme leverages WordPress
   core's built-in CSS classes (`wp-block-*`, `has-*-color`,
   `has-*-font-size`, `is-layout-*`, etc.) and the block editor's
   responsive behavior. No CSS framework overrides are needed.

### What is explicitly excluded

| Excluded | Reason |
|---|---|
| **Tailwind CSS** | Utility-first CSS requires a build step (PostCSS), adds ~3MB+ of generated CSS, and conflicts with WordPress core's block styling conventions. The utility class approach is redundant when `theme.json` provides the same design tokens natively. |
| **Bootstrap** | Component framework adds ~25KB+ gzipped CSS and imposes its own grid system, button styles, and JavaScript components. Conflicts with WordPress block styles and the Twenty Twenty-Five parent theme's responsive system. |
| **Bulma** | Same issues as Bootstrap — imposes external component styles that conflict with WordPress core block styling. |
| **Foundation** | Same issues as Bootstrap and Bulma. |
| **Font Awesome** | Icon font adds ~70KB+ and HTTP requests. Use inline SVG icons instead (see [`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md) → Icons). |

### Rationale

1. **Lightweight performance:** No CSS framework means no framework
   overhead. The child theme ships only the CSS it needs — `theme.json`
   tokens for block styling + a small custom CSS file for complex
   layouts. Total CSS budget remains under 16KB gzipped (see
   [`PERFORMANCE-BUDGET.md`](./PERFORMANCE-BUDGET.md)).
2. **WordPress core alignment:** `theme.json` is WordPress core's
   native styling mechanism for block themes. Using it ensures the
   block editor's color picker, font size selector, and spacing controls
   all use OLLMH brand values — no custom CSS needed for standard block
   styling. This is the WordPress-recommended approach for block child
   themes.
3. **No build step:** Pure CSS and `theme.json` require no compilation,
   no PostCSS, no Tailwind config, no purge step. The client's ICT team
   can edit CSS directly without a Node.js toolchain.
4. **No framework conflicts:** External CSS frameworks (Tailwind,
   Bootstrap) impose their own reset, grid system, and component styles
   that conflict with WordPress core's block styles and the Twenty
   Twenty-Five parent theme's responsive system. Pure CSS avoids this
   entirely.
5. **Maintainability:** `theme.json` is a single declarative file that
   defines all design tokens. Custom CSS is organized into small,
   focused files (base, layout, components, pages, responsive). No
   utility class sprawl, no `@apply` directives, no framework-specific
   patterns to learn.

### CSS file structure (child theme)

```
ollmh-child/
├── theme.json                 # Design tokens (colors, fonts, spacing) — extends parent
├── assets/
│   └── css/
│       ├── base.css           # Reset, custom properties, typography overrides
│       ├── layout.css         # Grid, containers, header/footer overrides
│       ├── components.css     # Buttons, cards, tables, forms, sliders, Turnstile
│       ├── pages.css          # Page-specific styles (home, departments, gallery, etc.)
│       ├── responsive.css     # @media queries for mobile/tablet
│       └── print.css          # Print styles
```

Each CSS file is enqueued via `wp_enqueue_style()` in the child theme's
`functions.php` → `class-ollmh-assets.php`, with appropriate versioning
for cache busting.

### `theme.json` structure (child theme)

The child theme's `theme.json` extends the parent's. It only needs to
override the values that differ from Twenty Twenty-Five's defaults:

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "color": {
      "palette": [
        { "slug": "primary",    "color": "#0056b3", "name": "Primary Blue" },
        { "slug": "secondary",  "color": "#00875a", "name": "Secondary Green" },
        { "slug": "accent",     "color": "#d4a017", "name": "Accent Gold" },
        { "slug": "background", "color": "#ffffff", "name": "Background" },
        { "slug": "text",       "color": "#1a1a1a", "name": "Text" },
        { "slug": "muted",      "color": "#6c757d", "name": "Muted Text" }
      ]
    },
    "typography": {
      "fontFamilies": [
        {
          "slug": "body",
          "name": "Body Font",
          "fontFamily": "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
        },
        {
          "slug": "heading",
          "name": "Heading Font",
          "fontFamily": "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
        }
      ]
    }
  }
}
```

See [`COLOR-SCHEMA.md`](./COLOR-SCHEMA.md) for the full color palette
and [`FONT-SCHEMA.md`](./FONT-SCHEMA.md) for the font stack.

---

## ADR-004: M-Pesa Daraja (G2) API — optional modular integration

**Status:** Pending client approval
**Date:** 2024

### Context

The OLLMH nursing school accepts student applications via an online
application form. The application process requires payment of a
non-refundable application fee. The current documentation describes
M-Pesa integration as a core plugin (`ollmh-payments`), but the client
has not yet confirmed whether online payment is required for the initial
launch.

M-Pesa is the dominant mobile payment platform in Kenya, operated by
Safaricom. The Safaricom Daraja API (Generation 2) provides STK Push
(Lipa Na M-Pesa Online) functionality, which allows a merchant to
initiate a payment request that appears as a prompt on the customer's
phone — the customer enters their M-Pesa PIN to complete the payment
without leaving the website.

### Decision

The M-Pesa payment integration is an **optional, modular feature** that
is **not part of the core WordPress functionality**. It is documented
and architected as a standalone plugin (`ollmh-payments`) that can be
activated or deactivated independently of the core system.

**Implementation is pending client approval.** Development will proceed
once the client has finalized the application form design and confirmed
that online payment is required.

### Technical feasibility

The technical feasibility of implementing the M-Pesa Daraja (G2) API
integration on cPanel shared hosting has been **confirmed**. The Daraja
G2 API operates over standard HTTPS and requires only:

| Requirement | cPanel shared hosting | Status |
|---|---|---|
| Outbound HTTPS requests (PHP `curl` / `wp_remote_post()`) | Supported | ✅ Confirmed |
| Publicly accessible HTTPS callback URL for Daraja webhooks | Available via cPanel AutoSSL (Let's Encrypt) | ✅ Confirmed |
| PHP 7.4+ with cURL extension | Standard on modern cPanel hosting | ✅ Confirmed |
| MySQL 5.7+ / MariaDB 10.3+ | Standard on modern cPanel hosting | ✅ Confirmed |
| WordPress REST API (for callback endpoint) | Core WordPress functionality | ✅ Confirmed |

**No DNS changes, server migration, or special infrastructure is
required.** The Daraja API callback URL is a standard WordPress REST API
endpoint (`/wp-json/ollmh/v1/payments/callback`) accessible over HTTPS.

### Integration architecture (when approved)

The `ollmh-payments` plugin implements the M-Pesa Daraja G2 API STK Push
workflow:

```
Application Form → STK Push Initiated → Customer Enters PIN on Phone
                                              ↓
                                    Daraja API Sends Callback
                                              ↓
                                    Payment Status Updated
                                              ↓
                                    Application Status → Screening
```

**STK Push flow (Lipa Na M-Pesa Online):**

1. Applicant completes the nursing school application form and enters
   their M-Pesa phone number
2. The `ollmh-payments` plugin calls the Daraja G2 API's STK Push
   endpoint, triggering a payment prompt on the applicant's phone
3. The applicant enters their M-Pesa PIN to authorize the payment
4. Safaricom's Daraja API sends an HTTP POST callback to the WordPress
   site's callback URL (`/wp-json/ollmh/v1/payments/callback`)
5. The callback handler verifies the transaction result and updates the
   `wp_application_payments` table with the payment status
6. If successful → application status is updated to `screening` and
   notifications are sent (email to applicant, email/SMS to admin)
7. If failed → the application remains in `submitted` status and the
   applicant can retry the payment

**Fallback mechanism:** If the Daraja callback is not received within
5 minutes (due to network delays), a WP-Cron job polls the Daraja
`QueryTransactionStatus` API to check the transaction status
asynchronously. This ensures payment confirmation is not lost even if
the callback fails.

### Plugin structure (when developed)

```
ollmh-payments/
├── ollmh-payments.php                    # Main plugin file (activation/deactivation hooks)
├── includes/
│   ├── class-ollmh-mpesa.php             # Daraja G2 API client (STK Push, transaction query)
│   ├── class-ollmh-mpesa-auth.php        # OAuth token management (caches access token)
│   ├── class-ollmh-payment-handler.php   # Payment processing logic
│   ├── class-ollmh-payment-callback.php  # Callback URL handler (Daraja webhook receiver)
│   └── class-ollmh-payment-query.php     # Transaction status polling (cron-triggered fallback)
├── assets/
│   ├── css/payment.css                   # Payment UI styling (pure CSS, no framework)
│   └── js/payment.js                     # STK Push status polling (vanilla JS, no jQuery)
└── logs/
    └── .gitkeep                          # M-Pesa transaction logs (gitignored)
```

### Settings (when activated)

M-Pesa configuration is stored in `wp_settings` → `financial` group
(see [`SETTINGS.md`](./SETTINGS.md)):

| Setting | Description |
|---|---|
| `mpesa_environment` | `sandbox` or `production` |
| `mpesa_consumer_key` | Daraja API consumer key (encrypted) |
| `mpesa_consumer_secret` | Daraja API consumer secret (encrypted) |
| `mpesa_shortcode` | Paybill or till number |
| `mpesa_passkey` | STK Push passkey (encrypted) |
| `mpesa_initiator_username` | Initiator username (for B2C if needed) |
| `mpesa_initiator_password` | Initiator password (encrypted) |
| `mpesa_callback_url` | STK Push callback URL (HTTPS) |

When the `ollmh-payments` plugin is **not activated**, these settings
are not used and the application form operates without online payment
(applicants pay offline via bank deposit or in-person M-Pesa).

### Rationale

1. **Modular design:** M-Pesa is a payment integration, not a content
   feature. Making it a standalone plugin means it can be activated only
   when needed, deactivated without affecting the rest of the site, and
   updated independently.
2. **Client approval gate:** The client has not confirmed whether online
   payment is required for the initial launch. Documenting it as optional
   ensures the core site can launch without it, and the payment module
   can be added later without rework.
3. **cPanel compatibility confirmed:** The Daraja G2 API uses standard
   HTTPS REST calls — no WebSocket, no long-running connections, no
   server-side daemons. cPanel shared hosting with PHP and cURL is
   sufficient.
4. **Fallback for callback reliability:** The WP-Cron polling fallback
   ensures payment confirmation is not lost if the Daraja callback fails
   — a known issue on shared hosting where transient 503/504 errors can
   occur under load.

### Implications for other documentation

- [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md) §4: M-Pesa
  section is updated to mark the plugin as **optional** and
  **pending client approval**
- [`SETTINGS.md`](./SETTINGS.md) `financial` group: settings are marked
  as **conditional** (only used when `ollmh-payments` plugin is active)
- [`REST-API-SPEC.md`](./REST-API-SPEC.md) §3.4 (M-Pesa callback):
  endpoint is marked as **conditional** (only registered when plugin is
  active)
- [`DEPLOYMENT.md`](./DEPLOYMENT.md): cPanel shared hosting is confirmed
  as feasible for the M-Pesa integration; the VPS recommendation is
  downgraded from "required" to "preferred for performance, not required
  for functionality"

---

## ADR-005: WP-CLI available in development only, not production

**Status:** Approved
**Date:** 2024

### Context

WP-CLI (WordPress Command-Line Interface) is a powerful tool for
WordPress administration — it enables scripted content migration, bulk
database operations, plugin/theme management, cache clearing, test
scaffolding, and performance monitoring from the command line.

The OLLMH project has two environments:

| Environment | Hosting | SSH access | WP-CLI |
|---|---|---|---|
| **Development** | Docker Compose (local) or VPS | Full SSH access | ✅ Available |
| **Production** | cPanel shared hosting | Limited or no SSH | ❌ Not available |

The client's production cPanel shared hosting environment does **not**
provide WP-CLI. Most cPanel shared hosting plans do not offer SSH access,
and even those that do typically do not install WP-CLI (it requires PHP
CLI SAPI and command-line execution, which many shared hosts disable for
security). The client's ICT team has confirmed that WP-CLI will not be
available on production.

### Decision

**WP-CLI is used in the development environment only.** All WP-CLI-based
workflows are documented as development-only procedures with
production-safe alternatives documented for every task.

### Tasks and their production alternatives

Every task currently documented with WP-CLI has an equivalent
production-safe method that works through the WordPress admin UI, REST
API, or cPanel File Manager / phpMyAdmin:

| Task | WP-CLI (dev only) | Production alternative |
|---|---|---|
| **Content migration** (importing archived pages into WordPress) | `wp eval-file scripts/migrate-content.php` | Run migration in dev → export via WP export (Tools → Export) → import on production via Tools → Import. Or: run migration script as a WP-CLI-style PHP file accessed via browser with a secret token. |
| **Asset migration** (importing images into media library) | `wp eval-file scripts/migrate-assets.php` | Same as content migration — run in dev, then export/import. Or: use the WordPress media uploader manually for small batches. |
| **Database table creation** (plugin activation) | `wp plugin activate ollmh-core` | Activate plugin via WP admin → Plugins page. The `register_activation_hook()` creates all tables identically. |
| **Plugin/theme activation** | `wp plugin activate ollmh-core` / `wp theme activate ollmh-child` | WP admin → Plugins → Activate; Appearance → Themes → Activate. |
| **Cache clearing** | `wp cache flush` / `wp w3-total-cache flush` | WP admin → Performance → Empty All Caches (W3 Total Cache). |
| **Database size monitoring** | `wp db size` | phpMyAdmin → database name → size column; or a custom admin dashboard widget that queries `SUM(data_length + index_length)` from `information_schema.TABLES`. |
| **User management** | `wp user create` / `wp user list` | WP admin → Users → Add New / All Users. |
| **Rewrite rules flush** | `wp rewrite flush` | WP admin → Settings → Permalinks → Save (flushes rewrite rules). |
| **Test scaffolding** | `wp scaffold plugin-tests ollmh-core` | Dev only — tests are run in dev, not on production. |
| **Redirect management** (Redirection plugin) | `wp redirection ...` | WP admin → Tools → Redirection → manage redirects via UI. |
| **Search/replace in DB** | `wp search-replace 'old.com' 'new.com'` | Use the "Better Search Replace" plugin (WP admin → Tools → Better Search Replace) or run a SQL query via phpMyAdmin (with serialized data caution). |
| **WordPress core update** | `wp core update` | WP admin → Dashboard → Updates → Update Now. |
| **Plugin/theme updates** | `wp plugin update --all` | WP admin → Dashboard → Updates → Update plugins/themes. |

### Rationale

1. **Environment separation:** Development uses Docker Compose with full
   WP-CLI access for rapid iteration, scripted migrations, and automated
   testing. Production uses cPanel shared hosting where WP-CLI is not
   available — this is a common and well-understood constraint.
2. **No production dependency on WP-CLI:** Every WP-CLI command in the
   documentation has a production-safe alternative via the WordPress
   admin UI, REST API, or cPanel tools (phpMyAdmin, File Manager). The
   site is fully operable without WP-CLI.
3. **Migration strategy:** Content and asset migration (the heaviest
   WP-CLI usage) is performed entirely in the development environment.
   The migrated content is then deployed to production via WordPress
   export/import (XML) for content, and via file upload (tar/zip via
   cPanel File Manager) for media assets. This is a one-time operation
   during initial deployment.
4. **Monitoring alternative:** Database size monitoring (the only
   recurring WP-CLI use on production) is replaced with a custom admin
   dashboard widget that displays database size using a standard SQL
   query — no WP-CLI needed.

### Migration workflow (dev → production)

Since WP-CLI is not available on production, the migration from
development to production follows this workflow:

```
DEVELOPMENT (Docker, WP-CLI available)          PRODUCTION (cPanel, no WP-CLI)
========================================        ====================================

1. Run content migration via WP-CLI
   wp eval-file scripts/migrate-content.php

2. Run asset migration via WP-CLI
   wp eval-file scripts/migrate-assets.php

3. Verify content in dev WP admin

4. Export content (WP admin → Tools → Export)   →  5. Import content (WP admin → Tools → Import)
    - All pages, posts, CPTs                         - Upload WXR XML file
    - Media (if "Download media" checked)            - Or upload media separately via File Manager

6. Export database (WP-CLI or phpMyAdmin)       →  7. Import database (phpMyAdmin → Import)
   wp db export ollmh-dev.sql                       - Upload .sql file
   - Or: phpMyAdmin → Export                            - phpMyAdmin → Import
   - Search/replace URLs if domain differs          - Run search/replace via Better Search Replace plugin

8. Deploy theme + plugins (Git or tar)          →  9. Upload via cPanel File Manager
   tar -czf ollmh-theme.tar.gz ollmh-child/         - Upload to wp-content/themes/
   tar -czf ollmh-plugins.tar.gz ollmh-*/            - Upload to wp-content/plugins/
                                                     - Extract via cPanel

                                                10. Activate theme + plugins (WP admin)
                                                    - Appearance → Themes → Activate ollmh-child
                                                    - Plugins → Activate all

                                                11. Flush rewrite rules
                                                    - Settings → Permalinks → Save

                                                12. Configure settings (WP admin → OLLMH Settings)
                                                    - Enter production values for all settings
```

### Custom admin dashboard widget for database monitoring

Since `wp db size` is not available on production, a custom dashboard
widget provides the same information:

```php
<?php
// ollmh-core/includes/class-ollmh-dashboard-widget.php

class OLLMH_Dashboard_Widget {

    public static function init(): void {
        add_action('wp_dashboard_setup', [self::class, 'add_widget']);
    }

    public static function add_widget(): void {
        wp_add_dashboard_widget(
            'ollmh_db_stats',
            __('OLLMH Database Statistics', 'ollmh'),
            [self::class, 'render']
        );
    }

    public static function render(): void {
        global $wpdb;

        $size = $wpdb->get_var(
            "SELECT SUM(data_length + index_length)
             FROM information_schema.TABLES
             WHERE table_schema = DATABASE()"
        );

        $size_mb = $size ? round($size / 1024 / 1024, 2) : 0;
        $size_gb = $size ? round($size / 1024 / 1024 / 1024, 4) : 0;

        $table_count = $wpdb->get_var(
            "SELECT COUNT(*) FROM information_schema.TABLES
             WHERE table_schema = DATABASE()"
        );

        $largest_tables = $wpdb->get_results(
            "SELECT table_name,
                    ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
             FROM information_schema.TABLES
             WHERE table_schema = DATABASE()
             ORDER BY (data_length + index_length) DESC
             LIMIT 5"
        );

        echo '<ul>';
        echo '<li><strong>Database size:</strong> ' . esc_html($size_mb) . ' MB (' . esc_html($size_gb) . ' GB)</li>';
        echo '<li><strong>Tables:</strong> ' . esc_html($table_count) . '</li>';
        echo '</ul>';

        if ($size_mb > 1024) {
            echo '<p class="notice notice-warning inline"><p>⚠️ Database exceeds 1 GB — consider archiving old records.</p></p>';
        }

        echo '<h4>Largest tables</h4><ul>';
        foreach ($largest_tables as $table) {
            echo '<li>' . esc_html($table->table_name) . ': ' . esc_html($table->size_mb) . ' MB</li>';
        }
        echo '</ul>';
    }
}
```

This widget appears on the WordPress admin dashboard and shows the same
information that `wp db size` would provide — no WP-CLI needed.

### Implications for other documentation

- [`DEPLOYMENT.md`](./DEPLOYMENT.md): deployment workflow updated to
  document the dev → production migration without WP-CLI; cPanel File
  Manager and phpMyAdmin are the production tools
- [`CONTENT-MIGRATION.md`](./CONTENT-MIGRATION.md): WP-CLI migration
  script marked as **dev-only**; production import via WP export/import
- [`ASSET-MIGRATION.md`](./ASSET-MIGRATION.md): WP-CLI migration script
  marked as **dev-only**; production import via file upload + media
  library
- [`PERFORMANCE-BUDGET.md`](./PERFORMANCE-BUDGET.md): database size
  monitoring changed from WP-CLI to custom admin dashboard widget
- [`ENVIRONMENT-SETUP.md`](./ENVIRONMENT-SETUP.md): WP-CLI usage
  clarified as dev-only
- [`TESTING-PLAN.md`](./TESTING-PLAN.md): WP-CLI test scaffolding
  clarified as dev-only (tests are never run on production)
- [`SEO-STRATEGY.md`](./SEO-STRATEGY.md): Redirection plugin's WP-CLI
  support noted as dev-only; production uses the admin UI

---

## ADR-006: Data architecture — WordPress-native (CPT + postmeta + taxonomies), custom tables only for operational data

**Status:** Approved
**Date:** 2024

### Context

The earlier schema documentation modelled ~80 bespoke SQL tables (see
[`ERD.md`](./ERD.md), [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md), and the
per-page files under [`pages/`](./pages/)). At the same time,
[`CPT-REGISTRATION-CODE.md`](./CPT-REGISTRATION-CODE.md) registered 15 Custom
Post Types and 4 taxonomies for the **same entities** (news, events,
departments, wards, clinics, staff, projects, etc.).

This is a contradiction: WordPress stores post content in `wp_posts` +
`wp_postmeta` and classification in `wp_terms`/`wp_term_taxonomy`/
`wp_term_relationships`. Defining a CPT **and** a parallel custom table for the
same entity means two competing sources of truth with no sync strategy — the
data model cannot be implemented as written. A decision is required before any
schema or plugin code is generated.

### Decision

**The OLLMH data layer is WordPress-native.** Every entity is classified into
exactly one storage mechanism:

1. **Core WordPress objects** — pages, media, users, navigation menus,
   comments, and revisions use core tables (`wp_posts`, `wp_postmeta`,
   `wp_users`/`wp_usermeta`, `wp_terms*`, `wp_comments`). No custom tables are
   created for these.
2. **Custom Post Types (CPTs)** — editable content entities that benefit from
   the block editor, revisions, and REST API.
3. **Taxonomies** — classification/grouping terms.
4. **Post meta / attachments / block content** — attributes and child
   collections of a CPT (structured fields as postmeta, image galleries as
   attachments with `post_parent`, curated homepage sections as block
   patterns/templates authored in the Site Editor).
5. **Custom tables** — retained **only** for high-volume, transactional, or
   operational data that is a poor fit for `wp_postmeta` (form submissions,
   bookings/appointments, application workflow, payments, notification queue,
   reference/scheduling resources, and the `wp_settings` config store).

**The `CREATE TABLE` blocks in the per-page docs and [`ERD.md`](./ERD.md) are
retained as _field specifications_** — the column list defines the fields an
entity needs. For entities classified as CPT/taxonomy/meta below, those columns
map to post fields, postmeta keys, taxonomy terms, or attachments — **they are
NOT created as SQL tables.** Only the tables in the "Retained custom tables"
list below are created as real SQL tables (via `dbDelta()` in the
`ollmh-core` activation hook). This ADR is the source of truth and supersedes
the standalone table listings elsewhere.

### Entity classification (all ~80 tables)

**CPTs (15)** — post type slugs per [`CPT-REGISTRATION-CODE.md`](./CPT-REGISTRATION-CODE.md):

| Old table | CPT slug |
|---|---|
| `wp_departments` | `department` |
| `wp_staff` | `staff_member` |
| `wp_news_articles` | `news_article` |
| `wp_events` | `event` |
| `wp_nursing_programmes` | `nursing_programme` |
| `wp_wards` | `ward` |
| `wp_clinics` | `clinic` |
| `wp_special_medical_services` | `special_service` |
| `wp_development_projects` | `development_project` |
| `wp_upcoming_projects` | `upcoming_project` |
| `wp_sustainability_projects` | `sustainability_project` |
| `wp_community_programs` | `community_program` |
| `wp_smi_community_events` | `smi_event` |
| `wp_job_vacancies` | `job_vacancy` |
| `wp_outlook_albums` | `outlook_album` |

**Taxonomies (4):**

| Old table | Taxonomy slug | Attached to |
|---|---|---|
| `wp_news_categories` | `news_category` | `news_article` |
| `wp_news_tags` | `news_tag` | `news_article` |
| `wp_event_categories` | `event_category` | `event` |
| `wp_staff_cadres` | `staff_cadre` | `staff_member` |

**Handled by core WordPress (no custom table):**
`wp_pages` → core Pages · `wp_media_assets`, `wp_page_media`,
`wp_*_media`, `wp_*_photos`, `wp_outlook_gallery_items` → Media Library
attachments (`post_parent` / featured image / gallery blocks) ·
`wp_users` → core Users · `wp_menu_items` → nav menus / Navigation block ·
`wp_news_comments` → core comments · `wp_news_article_revisions` → core
revisions · `wp_news_article_tags` → term relationships.

**Post meta / attachments / block content (folded into the owning CPT or page):**
`wp_home_slides`, `wp_home_in_focus_items`, `wp_home_feature_blocks`,
`wp_home_news_promos` (front-page block patterns + query blocks);
`wp_department_showcase`, `wp_opd_facilities`, `wp_opd_operating_hours`,
`wp_inpatient_dept_sections`, `wp_service_specialists`, `wp_service_equipment`,
`wp_mortuary_services`, `wp_nursing_school_profile`, `wp_nursing_facilities`,
`wp_development_strategic_plans`, `wp_development_project_plan_links`,
`wp_development_project_metrics`, `wp_upcoming_project_phases`,
`wp_community_outreach_events`, `wp_smi_community_profile`, `wp_smi_facilities`,
`wp_about_facts`, `wp_about_milestones`, `wp_location_info`,
`wp_governance_bodies`, `wp_governance_members`, `wp_care_statements`,
`wp_care_values`, `wp_hr_capacity_stats`, `wp_contact_channels`,
`wp_application_form_downloads` (postmeta/attachments/block content on the
owning CPT or WordPress page; `wp_contact_channels`/`wp_location_info` overlap
with the `contact` settings group in [`SETTINGS.md`](./SETTINGS.md)).

**Retained custom tables (~26, created via `dbDelta()` in `ollmh-core`):**

| Table | Why it stays a custom table |
|---|---|
| `wp_settings` | Config key-value store (already seeded — see [`SETTINGS.md`](./SETTINGS.md)) |
| `wp_newsletter_subscribers` | Operational mailing list |
| `wp_event_registrations` | Transactional (event sign-ups) |
| `wp_applicants` | PII applicant records (application workflow) |
| `wp_applications` | Transactional application records |
| `wp_application_documents` | Uploaded-file references per application |
| `wp_application_status_history` | Audit trail |
| `wp_application_referees` | Application child data |
| `wp_application_reviews` | Reviewer workflow |
| `wp_application_payments` | M-Pesa transactions (optional — ADR-004) |
| `wp_application_notifications` | Per-application notification log |
| `wp_nursing_intakes` | Scheduling/capacity counters referenced by applications |
| `wp_opd_consultation_rooms` | Bookable resource referenced by appointments |
| `wp_opd_appointments` | Transactional bookings |
| `wp_clinic_schedules` | Recurring schedules referenced by bookings |
| `wp_clinic_schedule_exceptions` | Schedule overrides |
| `wp_clinic_bookings` | Transactional bookings |
| `wp_ward_bed_status` | Frequently-updated operational status |
| `wp_inpatient_admission_enquiries` | Form submissions |
| `wp_service_enquiries` | Form submissions |
| `wp_smi_vocation_enquiries` | Form submissions |
| `wp_community_volunteer_signups` | Form submissions |
| `wp_contact_submissions` | Form submissions |
| `wp_upcoming_project_pledges` | Transactional pledges/donations |
| `wp_sustainability_production_records` | Time-series operational data |

### Rationale

1. **One source of truth per entity.** Each entity is a CPT **or** a custom
   table, never both — removing the central contradiction.
2. **Leverage the platform.** CPT content gets the block editor, revisions,
   media handling, search, REST API, and plugin compatibility (Rank Math SEO,
   Redirection, etc.) for free. Re-implementing these on bespoke tables would
   be costly and lower quality.
3. **Custom tables where they earn their place.** Form submissions, bookings,
   payments, and audit logs are high-volume/transactional and query poorly as
   `wp_postmeta`; keeping them as normalized custom tables is the same pattern
   mature plugins (WooCommerce, Gravity Forms, The Events Calendar) use.
4. **Field specs are preserved.** No analysis is lost — the documented columns
   become the postmeta/field map for each CPT, so the per-page docs remain
   useful as field references.

### Implications for other documentation

- [`ERD.md`](./ERD.md), [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md), and
  [`pages/`](./pages/): the `CREATE TABLE` blocks are field specifications;
  only the "Retained custom tables" list above is created as SQL. A banner at
  the top of these files points here.
- [`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md): CPT/taxonomy entities appear as
  native WordPress admin menus; retained custom tables get bespoke admin
  screens. The "81 custom tables" framing is superseded by this classification.
- [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md): `ollmh-core` activation
  creates only the ~26 retained custom tables via `dbDelta()`; CPTs and
  taxonomies are registered on `init` (no table creation).
- [`CPT-REGISTRATION-CODE.md`](./CPT-REGISTRATION-CODE.md): remains the
  canonical registration for the 15 CPTs and 4 taxonomies.

---

## Decision summary

| ADR | Decision | Status |
|---|---|---|
| ADR-001 | Child theme extending Twenty Twenty-Five (block/FSE) | Approved |
| ADR-002 | Cloudflare Turnstile with vanilla JavaScript | Approved |
| ADR-003 | No Tailwind CSS — pure CSS and native WordPress styling | Approved |
| ADR-004 | M-Pesa Daraja G2 API — optional modular integration | Pending client approval |
| ADR-005 | WP-CLI available in development only, not production | Approved |
| ADR-006 | Data architecture — WordPress-native (CPT + postmeta + taxonomies); custom tables only for operational data | Approved |
