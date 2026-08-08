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

## 1. Theme type: Classic (PHP) theme

The OLLMH theme is a **classic PHP theme** (not a block/FSE theme). Rationale:

- The site has complex custom layouts (home page slideshow + tabs + news
  scroller + department columns, ward bed-status tables, clinic schedule
  grids, application multi-step forms, photo galleries) that are easier to
  build with PHP templates than block patterns.
- The hospital staff who will manage content are non-technical — they need
  CPT admin screens (handled by plugins, see
  [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md)), not the block
  editor for layout.
- Classic themes have a larger ecosystem of compatible plugins (Rank Math,
  Site Kit, Redirection, WP Rocket, Broken Link Checker — all confirmed
  compatible).
- The archived site's layout is fixed and well-documented in
  [`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md) — there is
  no need for editorial layout flexibility.

**WordPress version target:** 6.4+ (minimum 6.2 for stability).

---

## 2. Theme directory structure

```
ollmh-theme/
├── style.css                  # Theme header + front-end CSS entry point
├── theme.json                 # Color palette + font variables (WP 6.x)
├── functions.php              # Theme bootstrap (loads includes/)
├── index.php                  # Fallback template (last in hierarchy)
├── front-page.php             # Home page template
├── header.php                 # Site header (logo, nav, top bar)
├── footer.php                 # Site footer (links, contact, social)
├── sidebar.php                # Sidebar (if used — likely not for OLLMH)
├── searchform.php             # Custom search form markup
├── 404.php                    # 404 not found page
├── page.php                   # Generic page template
├── single.php                 # Generic single post template
├── archive.php                # Generic archive/listing template
│
├── page-templates/            # Custom page templates (selectable per page)
│   ├── page-about.php         # About / Location page
│   ├── page-contacts.php      # Contact page (form + map + channels)
│   ├── page-departments.php   # Departments grid page
│   ├── page-wards.php         # Wards & inpatient page
│   ├── page-opd.php           # Outpatient department page
│   ├── page-clinic-days.php   # Clinic days schedule page
│   ├── page-special-services.php  # Special medical services page
│   ├── page-philosophy.php    # Philosophy of care page
│   ├── page-administration.php    # Administration / governance page
│   ├── page-hr-capacity.php   # HR capacity / staff page
│   ├── page-nursing-school.php    # Nursing school page
│   ├── page-application-form.php  # Application form page (multi-step)
│   ├── page-projects.php      # Projects overview (dev + sustainability + upcoming)
│   ├── page-community.php     # Community / SMI page
│   ├── page-gallery.php       # Photo gallery (Outlook) page
│   └── page-news-events.php   # News & Events combined listing page
│
├── template-parts/            # Reusable template parts
│   ├── content-news-article.php   # Single news article card
│   ├── content-event.php          # Single event card
│   ├── content-department.php     # Department card (grid item)
│   ├── content-staff-member.php   # Staff profile card
│   ├── content-ward.php           # Ward info block
│   ├── content-clinic-schedule.php # Clinic schedule table
│   ├── content-project.php        # Project card
│   ├── content-community-program.php # Community program card
│   ├── content-gallery-item.php   # Gallery image item
│   ├── home-slideshow.php         # Home page hero slideshow
│   ├── home-feature-blocks.php    # Home page feature blocks
│   ├── home-in-focus.php          # Home page "In Focus" section
│   ├── home-news-scroller.php     # Home page news scroller
│   ├── home-dept-columns.php      # Home page department columns
│   ├── section-breadcrumbs.php    # Breadcrumb bar
│   ├── section-hero.php           # Page hero (title + intro + image)
│   ├── section-sidebar.php        # Page sidebar (related links)
│   └── section-cta.php            # Call-to-action band
│
├── includes/                  # PHP classes/functions (loaded by functions.php)
│   ├── class-ollmh-theme.php      # Theme setup (supports, menus, image sizes)
│   ├── class-ollmh-assets.php     # CSS/JS enqueuing
│   ├── class-ollmh-menu.php       # Menu walkers (mega-menu, footer menu)
│   ├── class-ollmh-helpers.php    # Template helpers (get_setting, render_section)
│   ├── class-ollmh-schema.php     # Schema.org JSON-LD output
│   └── class-ollmh-breadcrumbs.php # Breadcrumb generator
│
├── assets/                    # Static assets
│   ├── css/
│   │   ├── base.css            # Reset, variables, typography
│   │   ├── layout.css          # Grid, containers, header/footer
│   │   ├── components.css      # Buttons, cards, tables, forms, sliders
│   │   ├── pages.css           # Page-specific styles
│   │   ├── responsive.css      # @media queries
│   │   └── print.css           # Print styles
│   ├── js/
│   │   ├── main.js             # General interactions (menu toggle, smooth scroll)
│   │   ├── slideshow.js        # Home page slideshow
│   │   ├── tabs.js             # Tabbed content sections
│   │   ├── news-scroller.js    # News ticker/scroller
│   │   ├── gallery.js          # Lightbox/gallery
│   │   └── forms.js            # Form validation + AJAX submission
│   ├── images/                 # Theme images (logo, icons, backgrounds)
│   └── fonts/                  # If any web fonts are added (currently system fonts)
│
├── screenshot.png             # Theme preview (1200×900px)
└── README.md                  # Theme documentation
```

---

## 3. Template hierarchy mapping

Each OLLMH page type maps to a specific WordPress template:

| Page type | WordPress template | CPT/archive? |
|---|---|---|
| Home | `front-page.php` | — |
| About / Location | `page-templates/page-about.php` | — |
| Contacts | `page-templates/page-contacts.php` | — |
| Departments listing | `page-templates/page-departments.php` | `archive-department.php` (CPT) |
| Single department | `single-department.php` | CPT |
| Wards & Inpatient | `page-templates/page-wards.php` | — |
| OPD | `page-templates/page-opd.php` | — |
| Clinic Days | `page-templates/page-clinic-days.php` | — |
| Special Medical Services | `page-templates/page-special-services.php` | — |
| Philosophy of Care | `page-templates/page-philosophy.php` | — |
| Administration | `page-templates/page-administration.php` | — |
| HR Capacity / Staff | `page-templates/page-hr-capacity.php` | `archive-staff_member.php` (CPT) |
| Nursing School | `page-templates/page-nursing-school.php` | — |
| Application Form | `page-templates/page-application-form.php` | — |
| Projects overview | `page-templates/page-projects.php` | — |
| Development projects | `archive-development_project.php` | CPT |
| Sustainability projects | `archive-sustainability_project.php` | CPT |
| Upcoming projects | `archive-upcoming_project.php` | CPT |
| Community / SMI | `page-templates/page-community.php` | — |
| Gallery (Outlook) | `page-templates/page-gallery.php` | `archive-outlook_album.php` (CPT) |
| News listing | `archive-news_article.php` | CPT |
| Single news article | `single-news_article.php` | CPT |
| Events listing | `archive-event.php` | CPT |
| Single event | `single-event.php` | CPT |
| Search results | `search.php` | — |
| 404 | `404.php` | — |

**Note:** CPT single/archive templates (`single-news_article.php`,
`archive-news_article.php`, etc.) take precedence over `single.php` and
`archive.php` in the WordPress template hierarchy. The custom
`page-templates/*.php` files are selected via the Page Attributes meta box
when editing a page.

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
