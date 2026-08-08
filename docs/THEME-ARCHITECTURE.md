# Theme Architecture

> This document defines the WordPress theme architecture for the OLLMH
> rebuild — theme type, template hierarchy, file organization, and the
> division of labor between the theme (presentation) and plugins
> (functionality).
>
> **Related:** [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md) for the
> plugin side, [`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md)
> for the header/footer layout, [`COLOR-SCHEMA.md`](./COLOR-SCHEMA.md) and
> [`FONT-SCHEMA.md`](./FONT-SCHEMA.md) for the design system.

---

## 1. Theme type: Child theme extending Twenty Twenty-Five (block/FSE)

> **Architectural decision:** See
> [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md) → ADR-001
> for the full context, rationale, and implications.

The OLLMH theme is a **custom child theme extending the official
WordPress Twenty Twenty-Five theme** — the default block theme shipped
with WordPress 6.7+.

Twenty Twenty-Five is a **block theme / Full Site Editing (FSE) theme**.
The child theme inherits the parent's block template structure,
`theme.json` design token system, Site Editor compatibility, and block
patterns. The child theme adds OLLMH-specific overrides:

- A `theme.json` that overrides the parent's color palette with OLLMH
  brand colors and the OLLMH font stack
- Custom block templates / template parts for OLLMH-specific page layouts
- A `functions.php` for asset enqueuing, image sizes, breadcrumbs, schema
  output, and template helpers
- Classic PHP template files for complex CPT pages where block templates
  are insufficient (multi-step application form, single news article,
  single event with registration) — WordPress supports this hybrid
  approach: PHP template files take precedence over block templates
- Custom block patterns for OLLMH content blocks (department card, staff
  card, clinic schedule, ward status, hero section, CTA band)

**Why a child theme (not a standalone theme):**

- The parent theme is maintained by the WordPress core team — security
  patches, block editor improvements, and responsive behavior flow to
  the child theme automatically
- The client's ICT team maintains only the overrides, not the entire
  theme — reduced maintenance burden
- Extending the official default theme ensures maximum compatibility
  with current and future WordPress core releases
- Hospital staff can use the Site Editor for minor layout adjustments
  without touching PHP code

**Why hybrid (block templates + classic PHP templates):**

- Standard pages (home, about, contacts, departments listing, clinic
  days, philosophy, administration, projects, community, gallery) use
  block templates — editable in the Site Editor
- Complex CPT pages (multi-step application form, single news article
  with custom layout, single event with registration form) use classic
  PHP template files — these take precedence over block templates in
  the WordPress template hierarchy, giving full PHP control where needed

**WordPress version target:** 6.7+ (Twenty Twenty-Five is the default
theme for WP 6.7, released November 2024).

---

## 2. Theme directory structure

The child theme (`ollmh-child`) extends Twenty Twenty-Five. It contains
only overrides and additions — the parent theme provides the base block
templates, `theme.json`, and block patterns.

```
ollmh-child/
├── style.css                  # Child theme header (Template: twentytwentyfive)
├── theme.json                 # Overrides parent's colors, fonts, spacing
├── functions.php              # Theme bootstrap (loads includes/, enqueues assets)
├── screenshot.png             # Theme preview (1200×900px)
├── README.md                  # Theme documentation
│
├── templates/                 # Block templates (override parent's)
│   ├── front-page.html        # Home page (slideshow + tabs + news + departments)
│   ├── page-about.html        # About / Location page
│   ├── page-contacts.html     # Contact page (form + map + channels)
│   ├── page-departments.html  # Departments grid page
│   ├── page-wards.html        # Wards & inpatient page
│   ├── page-opd.html          # Outpatient department page
│   ├── page-clinic-days.html  # Clinic days schedule page
│   ├── page-special-services.html  # Special medical services page
│   ├── page-philosophy.html   # Philosophy of care page
│   ├── page-administration.html   # Administration / governance page
│   ├── page-hr-capacity.html  # HR capacity / staff page
│   ├── page-nursing-school.html   # Nursing school page
│   ├── page-projects.html     # Projects overview page
│   ├── page-community.html    # Community / SMI page
│   ├── page-gallery.html      # Photo gallery (Outlook) page
│   ├── page-news-events.html  # News & Events combined listing page
│   ├── page-faq.html          # FAQ page (accordion)
│   ├── page-patient-information.html  # Patient information page
│   ├── page-privacy-policy.html      # Privacy policy page
│   ├── page-terms-of-service.html    # Terms of service page
│   ├── page-data-protection.html     # Data protection page
│   ├── archive-news_article.html     # News listing (block template)
│   ├── archive-event.html           # Events listing (block template)
│   ├── archive-department.html      # Departments archive (block template)
│   ├── archive-development_project.html  # Development projects archive
│   ├── archive-sustainability_project.html  # Sustainability projects archive
│   ├── archive-upcoming_project.html      # Upcoming projects archive
│   ├── archive-outlook_album.html         # Gallery albums archive
│   ├── archive-staff_member.html          # Staff archive
│   ├── 404.html                            # 404 not found page
│   └── search.html                         # Search results page
│
├── parts/                     # Template parts (block markup)
│   ├── header.html            # Site header (logo, nav, top bar)
│   ├── footer.html            # Site footer (links, contact, social, newsletter)
│   ├── sidebar.html           # Sidebar (if used)
│   ├── breadcrumbs.html       # Breadcrumb bar
│   ├── hero.html              # Page hero (title + intro + image)
│   └── cta.html               # Call-to-action band
│
├── patterns/                  # Block patterns (registered for Site Editor)
│   ├── department-card.php    # Department card pattern
│   ├── staff-card.php         # Staff profile card pattern
│   ├── clinic-schedule.php    # Clinic schedule table pattern
│   ├── ward-status.php        # Ward status table pattern
│   ├── news-scroller.php      # News scroller pattern
│   ├── hero-slideshow.php     # Home page hero slideshow pattern
│   ├── feature-blocks.php     # Home page feature blocks pattern
│   └── dept-columns.php       # Home page department columns pattern
│
├── single-news_article.php    # Classic PHP: single news article (custom layout)
├── single-event.php           # Classic PHP: single event (with registration form)
├── single-department.php      # Classic PHP: single department (custom layout)
├── single-staff_member.php    # Classic PHP: single staff member profile
├── single-development_project.php  # Classic PHP: single project
├── single-outlook_album.php   # Classic PHP: single gallery album
├── page-application-form.php  # Classic PHP: multi-step application form
├── searchform.php             # Custom search form markup
│
├── includes/                  # PHP classes (loaded by functions.php)
│   ├── class-ollmh-theme.php      # Theme setup (supports, image sizes, block patterns)
│   ├── class-ollmh-assets.php     # CSS/JS enqueuing (vanilla JS, pure CSS)
│   ├── class-ollmh-menu.php       # Menu walkers (mega-menu, footer menu)
│   ├── class-ollmh-helpers.php    # Template helpers (get_setting, render_section)
│   ├── class-ollmh-schema.php     # Schema.org JSON-LD output
│   └── class-ollmh-breadcrumbs.php # Breadcrumb generator
│
└── assets/                    # Static assets
    ├── css/
    │   ├── base.css            # Reset, custom properties, typography overrides
    │   ├── layout.css          # Grid, containers, header/footer overrides
    │   ├── components.css      # Buttons, cards, tables, forms, sliders, Turnstile
    │   ├── pages.css           # Page-specific styles
    │   ├── responsive.css      # @media queries
    │   └── print.css           # Print styles
    ├── js/                     # Vanilla ES6+ (no jQuery — see ADR-002)
    │   ├── main.js             # General interactions (menu toggle, smooth scroll)
    │   ├── slideshow.js        # Home page slideshow
    │   ├── tabs.js             # Tabbed content sections
    │   ├── news-scroller.js    # News ticker/scroller
    │   ├── gallery.js          # Lightbox/gallery
    │   ├── forms.js            # Form validation + AJAX submission + Turnstile
    │   └── cookie-consent.js   # Cookie consent banner
    ├── images/                 # Theme images (logo, icons, backgrounds)
    └── fonts/                  # If any web fonts are added (currently system fonts)
```

**Key differences from a standalone theme:**

- `style.css` contains only the theme header (`Template: twentytwentyfive`)
  and minimal CSS — the parent theme provides the base styling
- `templates/*.html` are block templates that override the parent's —
  standard WordPress block markup, editable in the Site Editor
- `parts/*.html` are block template parts (header, footer, etc.) that
  override the parent's
- `patterns/*.php` register custom block patterns for the Site Editor
- `single-*.php` and `page-application-form.php` are classic PHP
  templates for complex CPT pages — these take precedence over block
  templates in the WordPress hierarchy
- `includes/` and `assets/` work identically to a standalone theme —
  `functions.php` loads the classes and enqueues CSS/JS the same way

---

## 3. Template hierarchy mapping

The child theme uses a **hybrid approach**: block templates (`.html`) for
standard pages and classic PHP templates (`.php`) for complex CPT pages.
PHP templates take precedence over block templates in the WordPress
template hierarchy.

| Page type | Template | Type |
|---|---|---|
| Home | `templates/front-page.html` | Block |
| About / Location | `templates/page-about.html` | Block |
| Contacts | `templates/page-contacts.html` | Block |
| Departments listing | `templates/archive-department.html` | Block (CPT archive) |
| Single department | `single-department.php` | Classic PHP (CPT) |
| Wards & Inpatient | `templates/page-wards.html` | Block |
| OPD | `templates/page-opd.html` | Block |
| Clinic Days | `templates/page-clinic-days.html` | Block |
| Special Medical Services | `templates/page-special-services.html` | Block |
| Philosophy of Care | `templates/page-philosophy.html` | Block |
| Administration | `templates/page-administration.html` | Block |
| HR Capacity / Staff | `templates/page-hr-capacity.html` + `templates/archive-staff_member.html` | Block |
| Single staff member | `single-staff_member.php` | Classic PHP (CPT) |
| Nursing School | `templates/page-nursing-school.html` | Block |
| Application Form | `page-application-form.php` | Classic PHP (multi-step form) |
| Projects overview | `templates/page-projects.html` | Block |
| Development projects | `templates/archive-development_project.html` | Block (CPT archive) |
| Sustainability projects | `templates/archive-sustainability_project.html` | Block (CPT archive) |
| Upcoming projects | `templates/archive-upcoming_project.html` | Block (CPT archive) |
| Single project | `single-development_project.php` | Classic PHP (CPT) |
| Community / SMI | `templates/page-community.html` | Block |
| Gallery (Outlook) | `templates/page-gallery.html` + `templates/archive-outlook_album.html` | Block |
| Single gallery album | `single-outlook_album.php` | Classic PHP (CPT) |
| News listing | `templates/archive-news_article.html` | Block (CPT archive) |
| Single news article | `single-news_article.php` | Classic PHP (CPT) |
| Events listing | `templates/archive-event.html` | Block (CPT archive) |
| Single event | `single-event.php` | Classic PHP (CPT, with registration form) |
| FAQ | `templates/page-faq.html` | Block |
| Patient Information | `templates/page-patient-information.html` | Block |
| Privacy Policy | `templates/page-privacy-policy.html` | Block |
| Terms of Service | `templates/page-terms-of-service.html` | Block |
| Data Protection | `templates/page-data-protection.html` | Block |
| Search results | `templates/search.html` | Block |
| 404 | `templates/404.html` | Block |

**Note:** Classic PHP templates (`single-*.php`, `page-application-form.php`)
take precedence over block templates in the WordPress template hierarchy.
This hybrid approach gives full PHP control for complex pages (forms,
custom CPT layouts) while leveraging block templates and the Site Editor
for standard content pages.

---

## 4. `functions.php` structure

The `functions.php` file is a **bootstrap only** — it does not contain
logic. All functionality is in classes under `includes/`:

```php
<?php
/**
 * OLLMH Theme functions.php
 * Bootstrap — loads class files, no logic here.
 */

if (!defined('ABSPATH')) {
    exit;
}

define('OLLMH_THEME_VERSION', '1.0.0');
define('OLLMH_THEME_DIR', get_template_directory());
define('OLLMH_THEME_URI', get_template_directory_uri());

// Load theme classes
require_once OLLMH_THEME_DIR . '/includes/class-ollmh-theme.php';
require_once OLLMH_THEME_DIR . '/includes/class-ollmh-assets.php';
require_once OLLMH_THEME_DIR . '/includes/class-ollmh-menu.php';
require_once OLLMH_THEME_DIR . '/includes/class-ollmh-helpers.php';
require_once OLLMH_THEME_DIR . '/includes/class-ollmh-schema.php';
require_once OLLMH_THEME_DIR . '/includes/class-ollmh-breadcrumbs.php';

// Initialize
OLLMH_Theme::init();
OLLMH_Assets::init();
OLLMH_Menu::init();
OLLMH_Schema::init();
```

---

## 5. `theme.json` — design tokens

The `theme.json` file registers the color palette and font variables from
[`COLOR-SCHEMA.md`](./COLOR-SCHEMA.md) and [`FONT-SCHEMA.md`](./FONT-SCHEMA.md)
so they are available in the block editor (for any blocks used) and as CSS
custom properties:

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 2,
  "settings": {
    "color": {
      "palette": [
        { "slug": "primary", "color": "#0046a8", "name": "Primary Blue" },
        { "slug": "secondary", "color": "#0099d3", "name": "Secondary Blue" },
        { "slug": "accent", "color": "#f7941e", "name": "Accent Orange" },
        { "slug": "dark", "color": "#1a1a1a", "name": "Dark" },
        { "slug": "gray", "color": "#666666", "name": "Gray" },
        { "slug": "light", "color": "#f5f5f5", "name": "Light" },
        { "slug": "white", "color": "#ffffff", "name": "White" }
      ]
    },
    "typography": {
      "fontFamilies": [
        {
          "fontFamily": "Georgia, 'Times New Roman', Times, serif",
          "slug": "serif",
          "name": "Serif (Headings)"
        },
        {
          "fontFamily": "'Helvetica Neue', Helvetica, Arial, sans-serif",
          "slug": "sans",
          "name": "Sans-serif (Body)"
        }
      ],
      "fontSizes": [
        { "slug": "small", "size": "0.875rem", "name": "Small" },
        { "slug": "normal", "size": "1rem", "name": "Normal" },
        { "slug": "medium", "size": "1.125rem", "name": "Medium" },
        { "slug": "large", "size": "1.5rem", "name": "Large" },
        { "slug": "x-large", "size": "2rem", "name": "Extra Large" },
        { "slug": "xx-large", "size": "2.5rem", "name": "XX Large" }
      ]
    },
    "layout": {
      "contentSize": "800px",
      "wideSize": "1200px"
    }
  }
}
```

> **Note:** The exact hex values should be pulled from
> [`COLOR-SCHEMA.md`](./COLOR-SCHEMA.md). The values above are examples
> based on the documented palette.

---

## 6. Image sizes

Register custom image sizes in `class-ollmh-theme.php`:

```php
add_image_size('ollmh-hero', 1920, 600, true);       // Home page slideshow
add_image_size('ollmh-feature', 400, 300, true);      // Feature blocks
add_image_size('ollmh-card', 600, 400, true);         // Department/news cards
add_image_size('ollmh-thumbnail', 300, 200, true);    // Small thumbnails
add_image_size('ollmh-staff', 400, 400, true);        // Staff portraits (square)
add_image_size('ollmh-gallery', 1200, 800, false);    // Gallery images (no crop)
add_image_size('ollmh-og', 1200, 630, true);          // Open Graph social image
```

---

## 7. Menu locations

Register three menu locations (see
[`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md)):

```php
register_nav_menus([
    'header_main'    => __('Header Main Menu', 'ollmh'),
    'header_top'     => __('Header Top Bar Links', 'ollmh'),
    'footer_main'    => __('Footer Main Links', 'ollmh'),
    'footer_bottom'  => __('Footer Bottom Links', 'ollmh'),
    'mobile'         => __('Mobile Menu', 'ollmh'),
]);
```

---

## 8. Widget areas

The OLLMH theme uses minimal widget areas (the archived site does not use
a traditional blog sidebar). Register:

| Widget area | Location | Purpose |
|---|---|---|
| `sidebar-main` | Right sidebar on inner pages | Related links, quick facts, CTA |
| `footer-column-1` | Footer column 1 | Quick links |
| `footer-column-2` | Footer column 2 | Services |
| `footer-column-3` | Footer column 3 | Contact info |
| `footer-column-4` | Footer column 4 | Social + newsletter |

---

## 9. Theme vs. plugin division of labor

| Concern | Lives in | Rationale |
|---|---|---|
| HTML templates (header, footer, page layouts) | **Theme** | Presentation — changes with design |
| CSS and JS assets | **Theme** | Presentation |
| `theme.json` (colors, fonts) | **Theme** | Design tokens |
| Image sizes | **Theme** | Presentation |
| Menu locations, widget areas | **Theme** | Presentation |
| Schema.org JSON-LD output | **Theme** (`class-ollmh-schema.php`) | Presentation — renders in `<head>` and body |
| Breadcrumbs | **Theme** (`class-ollmh-breadcrumbs.php`) | Presentation |
| Template helpers (`get_setting()`, `render_section()`) | **Theme** (`class-ollmh-helpers.php`) | Presentation utility |
| CPT registration (`register_post_type`) | **Plugin** (`ollmh-core` plugin) | Functionality — survives theme switches |
| Custom taxonomies | **Plugin** (`ollmh-core` plugin) | Functionality |
| Settings page (wp_settings admin UI) | **Plugin** (`ollmh-core` plugin) | Functionality |
| Form handlers (appointments, applications, contact) | **Plugin** (`ollmh-forms` plugin) | Functionality — REST API endpoints |
| M-Pesa integration | **Plugin** (`ollmh-payments` plugin) | Functionality |
| Email/SMS notifications | **Plugin** (`ollmh-notifications` plugin) | Functionality |
| Cron jobs / scheduled tasks | **Plugin** (`ollmh-core` plugin) | Functionality |
| Capability additions (`add_cap()`) | **Plugin** (`ollmh-core` plugin) | Functionality — see [`USER-ROLES.md`](./USER-ROLES.md) |
| Settings seeder | **Plugin** (`ollmh-core` plugin, activation hook) | Functionality — see [`seeders/`](../seeders/) |

**Principle:** If it survives a theme switch, it goes in a plugin. If it
changes with the design, it goes in the theme.

---

## 10. CSS architecture

The theme uses a **layered CSS architecture** with `base.css` →
`layout.css` → `components.css` → `pages.css` → `responsive.css`, loaded
in that order. All CSS is enqueued via `class-ollmh-assets.php` (not
`@import` — WordPress requires `wp_enqueue_style` for proper dependency
management and caching plugin compatibility).

CSS custom properties (variables) are defined in `base.css`:

```css
:root {
  --color-primary: #0046a8;
  --color-secondary: #0099d3;
  --color-accent: #f7941e;
  --color-dark: #1a1a1a;
  --color-gray: #666666;
  --color-light: #f5f5f5;
  --color-white: #ffffff;

  --font-serif: Georgia, 'Times New Roman', Times, serif;
  --font-sans: 'Helvetica Neue', Helvetica, Arial, sans-serif;

  --container-width: 1200px;
  --sidebar-width: 300px;
  --content-width: 800px;

  --spacing-unit: 1rem;
  --border-radius: 4px;
}
```

See [`COLOR-SCHEMA.md`](./COLOR-SCHEMA.md) for the full palette and
[`FONT-SCHEMA.md`](./FONT-SCHEMA.md) for the full typography stack.

---

## 11. JavaScript architecture

All JS is enqueued via `class-ollmh-assets.php` with proper dependencies
and versioning. No inline JS in templates (WordPress coding standards).

| File | Dependencies | Load | Purpose |
|---|---|---|---|
| `main.js` | jQuery | Footer | Menu toggle, smooth scroll, accordion, general UI |
| `slideshow.js` | jQuery, main.js | Footer (home only) | Home page hero slideshow |
| `tabs.js` | jQuery, main.js | Footer (where tabs used) | Tabbed content sections |
| `news-scroller.js` | jQuery, main.js | Footer (home only) | News ticker |
| `gallery.js` | jQuery, main.js | Footer (gallery page only) | Lightbox |
| `forms.js` | jQuery | Footer (form pages only) | AJAX form submission, validation, Turnstile |

See [`JAVASCRIPT-INTERACTIVITY.md`](./JAVASCRIPT-INTERACTIVITY.md) for the
detailed JS component specifications and
[`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md) for library
choices.

---

## 12. 404 page (`404.php`)

The 404 page is shown when a visitor requests a URL that doesn't exist.
It should be helpful, not alarming — guide the visitor back to relevant
content.

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  404                                                                         │
│  Page Not Found                                                              │
│                                                                              │
│  The page you're looking for doesn't exist or has been moved.                │
│                                                                              │
│  [ Search box: "Search OLLMH..." ]                                           │
│                                                                              │
│  Popular pages:                                                              │
│  • Home                                                                      │
│  • About OLLMH                                                               │
│  • Services                                                                  │
│  • Departments                                                               │
│  • Contact Us                                                                │
│  • News                                                                      │
│  • Events                                                                    │
│                                                                              │
│  Need help? Call us at +254-XXX-XXXX or email info@ollmh.org                 │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Elements

| Element | Description |
|---|---|
| Large "404" | Visually prominent, styled with `var(--color-primary)` |
| "Page Not Found" heading | `<h1>` |
| Description text | Friendly, non-technical explanation |
| Search box | WordPress search form (`get_search_form()`) — lets the user search for what they were looking for |
| Popular pages list | 7 most-visited pages as quick links |
| Contact help line | Hospital phone and email for visitors who need assistance |

### SEO

- 404 pages should return HTTP status `404` (not `200`) — WordPress
  handles this automatically
- Add `noindex` meta tag to prevent search engines from indexing 404 pages
- Do **not** redirect 404s to the homepage (bad for SEO — search engines
  need to see the 404 status to remove dead URLs from their index)
- Monitor 404s via Redirection plugin logs and Broken Link Checker

### Implementation

```php
<?php
// 404.php
get_header();
?>
<main id="main-content" class="error-404">
  <div class="container">
    <div class="error-404-content">
      <p class="error-code">404</p>
      <h1><?php _e('Page Not Found', 'ollmh'); ?></h1>
      <p><?php _e('The page you\'re looking for doesn\'t exist or has been moved.', 'ollmh'); ?></p>

      <div class="error-404-search">
        <?php get_search_form(); ?>
      </div>

      <div class="error-404-links">
        <h2><?php _e('Popular Pages', 'ollmh'); ?></h2>
        <ul>
          <li><a href="<?php echo esc_url(home_url('/')); ?>">Home</a></li>
          <li><a href="<?php echo esc_url(home_url('/about-ollmh-location/')); ?>">About OLLMH</a></li>
          <li><a href="<?php echo esc_url(home_url('/out-patient-dept/')); ?>">Services</a></li>
          <li><a href="<?php echo esc_url(home_url('/ollmh-departments/')); ?>">Departments</a></li>
          <li><a href="<?php echo esc_url(home_url('/contacts/')); ?>">Contact Us</a></li>
          <li><a href="<?php echo esc_url(home_url('/news/')); ?>">News</a></li>
          <li><a href="<?php echo esc_url(home_url('/events/')); ?>">Events</a></li>
        </ul>
      </div>

      <p class="error-404-help">
        <?php printf(
          __('Need help? Call us at %s or email %s', 'ollmh'),
          '<a href="tel:' . esc_attr($hospital_phone) . '">' . esc_html($hospital_phone) . '</a>',
          '<a href="mailto:' . esc_attr($hospital_email) . '">' . esc_html($hospital_email) . '</a>'
        ); ?>
      </p>
    </div>
  </div>
</main>
<?php get_footer(); ?>
```

---

## 13. Search results page (`search.php`)

The search results page displays results for user queries submitted via
the search form (in the header top bar and on the 404 page).

### Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Breadcrumbs: Home → Search Results                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Search results for: "maternity"                                             │
│  5 results found                                                             │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Maternity Ward                                                          │ │
│  │ /wards/                                                                 │ │
│  │ Our maternity ward provides comprehensive care for expectant mothers... │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Antenatal Clinic Schedule                                               │ │
│  │ /clinic-days/                                                           │ │
│  │ Antenatal clinics run every Monday from 8:00 AM to 12:00 PM...          │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│  ...                                                                         │
│                                                                              │
│  [ ← Previous ]  Page 1 of 2  [ Next → ]                                    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Search again: [ maternity ward                              ] [ Search ]│ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Elements

| Element | Description |
|---|---|
| Breadcrumbs | Home → Search Results |
| Search query display | "Search results for: {query}" — the query is escaped and displayed |
| Result count | "N results found" |
| Result cards | Each result shows: title (linked), URL/path, excerpt with highlighted search term |
| Pagination | WordPress default pagination (`the_posts_pagination()`) — 10 results per page |
| Search again box | Pre-filled with the current query, allows refining the search |

### Result types

WordPress search returns:
- Pages (`page` post type)
- News articles (`news_article` CPT)
- Events (`event` CPT)
- Departments (`department` CPT)
- Staff members (`staff_member` CPT)
- Job vacancies (`job_vacancy` CPT)
- Development/sustainability/upcoming projects
- Community programs / SMI events

Non-searchable (excluded from search):
- `ward` (non-public CPT)
- `clinic` (non-public CPT)
- `special_service` (non-public CPT)
- `outlook_album` (gallery — searched via separate gallery interface)

### Search customization

The default WordPress search is sufficient for the initial launch. If
enhanced search is needed later, consider:
- [SearchWP](https://searchwp.com/) — improves search relevance, supports
  custom weighting, PDF indexing
- [WP Search with Algolia](https://wordpress.org/plugins/wp-search-with-algolia/) —
  typo-tolerant, instant search, faceted filtering

### Implementation

```php
<?php
// search.php
get_header();
?>
<main id="main-content" class="search-results">
  <div class="container">
    <?php echo do_shortcode('[ollmh_breadcrumbs]'); ?>

    <h1>
      <?php printf(__('Search results for: %s', 'ollmh'), '<span>' . get_search_query() . '</span>'); ?>
    </h1>

    <?php if (have_posts()) : ?>
      <p class="search-count">
        <?php printf(__('%d results found', 'ollmh'), $wp_query->found_posts); ?>
      </p>

      <div class="search-results-list">
        <?php while (have_posts()) : the_post(); ?>
          <article class="search-result-item">
            <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
            <p class="search-result-url"><?php echo esc_html(wp_make_link_relative(get_permalink())); ?></p>
            <p class="search-result-excerpt"><?php the_excerpt(); ?></p>
          </article>
        <?php endwhile; ?>
      </div>

      <?php the_posts_pagination([
        'prev_text' => __('Previous', 'ollmh'),
        'next_text' => __('Next', 'ollmh'),
      ]); ?>

    <?php else : ?>
      <p><?php _e('No results found. Please try a different search term.', 'ollmh'); ?></p>
    <?php endif; ?>

    <div class="search-again">
      <?php get_search_form(); ?>
    </div>
  </div>
</main>
<?php get_footer(); ?>
```

### Excluding non-public CPTs from search

```php
// functions.php or class-ollmh-theme.php
add_filter('pre_get_posts', function($query) {
    if (!is_admin() && $query->is_search) {
        $query->set('post_type', [
            'page',
            'news_article',
            'event',
            'department',
            'staff_member',
            'job_vacancy',
            'development_project',
            'sustainability_project',
            'upcoming_project',
            'community_program',
            'smi_event',
        ]);
    }
    return $query;
});
```

---

## 14. WP_Query examples for CPT archives

The following examples show how to query custom post types for archive
pages, shortcodes, and widgets.

### 14.1 News articles (latest 6, with featured image)

```php
$news_query = new WP_Query([
    'post_type'      => 'news_article',
    'posts_per_page' => 6,
    'orderby'        => 'date',
    'order'          => 'DESC',
    'tax_query'      => [[
        'taxonomy' => 'news_category',
        'field'    => 'slug',
        'terms'    => 'announcements',
    ]],
]);
```

### 14.2 Upcoming events (sorted by event date meta)

```php
$events_query = new WP_Query([
    'post_type'      => 'event',
    'posts_per_page' => 5,
    'meta_key'       => '_event_start_date',
    'orderby'        => 'meta_value',
    'order'          => 'ASC',
    'meta_query'     => [[
        'key'     => '_event_start_date',
        'value'   => date('Y-m-d'),
        'compare' => '>=',
        'type'    => 'DATE',
    ]],
]);
```

### 14.3 Staff members by department

```php
$staff_query = new WP_Query([
    'post_type'      => 'staff_member',
    'posts_per_page' => -1,
    'orderby'        => 'menu_order',
    'order'          => 'ASC',
    'tax_query'      => [[
        'taxonomy' => 'department',
        'field'    => 'slug',
        'terms'    => 'maternity',
    ]],
]);
```

### 14.4 Departments (all, ordered by menu_order)

```php
$departments_query = new WP_Query([
    'post_type'      => 'department',
    'posts_per_page' => -1,
    'orderby'        => 'menu_order',
    'order'          => 'ASC',
]);
```

### 14.5 Job vacancies (open positions only)

```php
$jobs_query = new WP_Query([
    'post_type'      => 'job_vacancy',
    'posts_per_page' => -1,
    'meta_query'     => [[
        'key'     => '_job_status',
        'value'   => 'open',
        'compare' => '=',
    ]],
    'meta_key'       => '_job_closing_date',
    'orderby'        => 'meta_value',
    'order'          => 'ASC',
]);
```

### 14.6 Gallery albums (with photo count)

```php
$albums_query = new WP_Query([
    'post_type'      => 'outlook_album',
    'posts_per_page' => -1,
    'orderby'        => 'date',
    'order'          => 'DESC',
]);
```

### 14.7 Custom table query (clinic schedules)

For custom tables (not CPTs), use `$wpdb` directly:

```php
global $wpdb;
$schedules = $wpdb->get_results($wpdb->prepare(
    "SELECT cs.*, d.post_title AS department_name
     FROM {$wpdb->prefix}clinic_schedules cs
     LEFT JOIN {$wpdb->posts} d ON cs.department_id = d.ID
     WHERE cs.day_of_week = %s
     ORDER BY cs.start_time ASC",
    'monday'
));
```

### 14.8 Cached queries (using transients)

For expensive queries that don't change often (clinic schedules,
department lists), cache the results with WordPress transients:

```php
function ollmh_get_clinic_schedules(string $day = ''): array {
    $cache_key = 'ollmh_clinic_schedules_' . sanitize_key($day);
    $cached = get_transient($cache_key);

    if (false !== $cached) {
        return $cached;
    }

    global $wpdb;
    $query = "SELECT * FROM {$wpdb->prefix}clinic_schedules";
    if ($day) {
        $query .= $wpdb->prepare(" WHERE day_of_week = %s", $day);
    }
    $query .= " ORDER BY start_time ASC";
    $results = $wpdb->get_results($query);

    $ttl = (int) OLLMH_Helpers::get_setting('cache_clinic_schedule_ttl_seconds', 86400);
    set_transient($cache_key, $results, $ttl);

    return $results;
}
```

The transient is automatically cleared when a clinic schedule is updated
(via the `save_post` hook or a custom admin save handler).
