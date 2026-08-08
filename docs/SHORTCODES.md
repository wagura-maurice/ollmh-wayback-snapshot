# Shortcodes

> This document defines all custom shortcodes for the OLLMH WordPress
> theme and plugins — their parameters, output, and usage examples.
>
> **Related:** [`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md) for
> theme structure, [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md)
> for plugin structure.

---

## 1. Shortcode policy

- Shortcodes are used to **embed dynamic content** in pages and posts that
  would otherwise be static HTML
- All shortcodes are registered in `ollmh-core/includes/class-ollmh-shortcodes.php`
- Shortcodes are **self-contained** — they query the database, render HTML,
  and return a string (never `echo`)
- Shortcodes are **cache-safe** — they work with WP Rocket page caching
  (dynamic content is loaded via AJAX where needed, or the shortcode output
  is cached with the page)
- Shortcodes use **semantic class names** prefixed with `ollmh-` (e.g.
  `ollmh-clinic-schedule`, `ollmh-staff-grid`)

---

## 2. Shortcode inventory

| Shortcode | Purpose | Used on |
|---|---|---|
| `[ollmh_clinic_schedule]` | Display clinic days and schedule table | `/clinic-days/` |
| `[ollmh_department_list]` | List all departments with links | `/ollmh-departments/` |
| `[ollmh_staff_grid]` | Display staff members in a grid | `/hr-capacity-staff/` |
| `[ollmh_ward_status]` | Display ward bed availability | `/wards/` |
| `[ollmh_contact_form]` | Render the contact form | `/contacts/` |
| `[ollmh_appointment_form]` | Render the appointment booking form | `/out-patient-dept/` |
| `[ollmh_application_form]` | Render the nursing school application form | `/medical-school-application-form/` |
| `[ollmh_event_registration]` | Render event registration form | Event single pages |
| `[ollmh_newsletter_form]` | Render newsletter signup form | Footer, sidebar |
| `[ollmh_upcoming_events]` | Display upcoming events list | Home page, sidebar |
| `[ollmh_latest_news]` | Display latest news articles | Home page, sidebar |
| `[ollmh_social_links]` | Display social media icon links | Header, footer, sidebar |
| `[ollmh_hospital_hours]` | Display operating hours | Contacts, footer |
| `[ollmh_breadcrumbs]` | Display breadcrumb navigation | All inner pages |
| `[ollmh_gallery]` | Display photo gallery grid | `/ollmh-outlook/` |

---

## 3. Detailed shortcode reference

### 3.1 `[ollmh_clinic_schedule]`

Displays the clinic schedule as a responsive table, sourced from the
`wp_clinic_schedules` table (or `clinic` CPT).

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `clinic_id` | int | `null` | Show schedule for a specific clinic only. If omitted, shows all clinics. |
| `day` | string | `null` | Filter by day of week (`monday`, `tuesday`, etc.). If omitted, shows all days. |
| `limit` | int | `0` | Maximum number of rows to show. `0` = no limit. |

**Usage:**
```html
<!-- Show all clinic schedules -->
[ollmh_clinic_schedule]

<!-- Show schedule for clinic ID 5 only -->
[ollmh_clinic_schedule clinic_id="5"]

<!-- Show only Wednesday clinics -->
[ollmh_clinic_schedule day="wednesday"]
```

**Output:**
```html
<div class="ollmh-clinic-schedule">
  <table class="clinic-schedule-table">
    <thead>
      <tr>
        <th>Clinic</th>
        <th>Day</th>
        <th>Time</th>
        <th>Department</th>
        <th>Doctor</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Antenatal Clinic</td>
        <td>Monday</td>
        <td>8:00 AM – 12:00 PM</td>
        <td>Maternity</td>
        <td>Dr. Wanjiku</td>
      </tr>
      <!-- More rows... -->
    </tbody>
  </table>
</div>
```

---

### 3.2 `[ollmh_department_list]`

Displays all departments as a grid of cards, each linking to the
department's single page.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `columns` | int | `3` | Number of columns in the grid (1–4) |
| `show_description` | bool | `true` | Show department description in the card |
| `show_head` | bool | `true` | Show department head name |
| `exclude` | string | `''` | Comma-separated department IDs to exclude |

**Usage:**
```html
[ollmh_department_list columns="4" show_description="false"]
```

**Output:**
```html
<div class="ollmh-department-grid grid grid-4">
  <div class="department-card">
    <img src="..." alt="Outpatient Department" class="department-image">
    <h3><a href="/departments/outpatient/">Outpatient Department</a></h3>
    <p class="department-head">Head: Dr. John Mwangi</p>
    <p class="department-description">General consultations, diagnosis...</p>
  </div>
  <!-- More cards... -->
</div>
```

---

### 3.3 `[ollmh_staff_grid]`

Displays staff members in a grid of portrait cards.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `department` | string | `''` | Filter by department slug |
| `columns` | int | `4` | Number of columns (1–6) |
| `limit` | int | `0` | Maximum number of staff to show. `0` = all |
| `show_title` | bool | `true` | Show job title |
| `show_qualifications` | bool | `true` | Show qualifications |
| `show_bio` | bool | `false` | Show short bio |
| `orderby` | string | `menu_order` | Sort order: `menu_order`, `title`, `date` |

**Usage:**
```html
<!-- Show all staff in 4 columns -->
[ollmh_staff_grid columns="4"]

<!-- Show only maternity staff, limited to 8 -->
[ollmh_staff_grid department="maternity" limit="8"]
```

**Output:**
```html
<div class="ollmh-staff-grid grid grid-4">
  <div class="staff-card">
    <img src="..." alt="Dr. Wanjiku Kamau" class="staff-photo">
    <h4>Dr. Wanjiku Kamau</h4>
    <p class="staff-title">Gynaecologist</p>
    <p class="staff-qualifications">MBChB, MMed (Obs/Gyn)</p>
  </div>
  <!-- More cards... -->
</div>
```

---

### 3.4 `[ollmh_ward_status]`

Displays current ward bed availability. This data is loaded via AJAX to
ensure it's always up-to-date even with page caching.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ward_id` | int | `null` | Show status for a specific ward only. If omitted, shows all wards. |
| `show_capacity` | bool | `true` | Show total bed capacity |
| `show_available` | bool | `true` | Show available beds |

**Usage:**
```html
[ollmh_ward_status]

[ollmh_ward_status ward_id="3"]
```

**Output:**
```html
<div class="ollmh-ward-status" data-ward-status>
  <table class="ward-status-table">
    <thead>
      <tr>
        <th>Ward</th>
        <th>Total Beds</th>
        <th>Occupied</th>
        <th>Available</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Maternity Ward</td>
        <td>20</td>
        <td>15</td>
        <td>5</td>
        <td><span class="status-badge status-available">Available</span></td>
      </tr>
      <tr>
        <td>Male Ward</td>
        <td>15</td>
        <td>15</td>
        <td>0</td>
        <td><span class="status-badge status-full">Full</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

The `[data-ward-status]` attribute triggers an AJAX call to refresh the
data every 5 minutes (configurable via `cache_ward_status_ttl_seconds`
setting).

---

### 3.5 `[ollmh_contact_form]`

Renders the contact form (see [`FRONT-END-FORMS.md`](./FRONT-END-FORMS.md)
→ Contact form).

**Parameters:** None.

**Usage:**
```html
[ollmh_contact_form]
```

This shortcode outputs the HTML form and enqueues the forms JS and
Turnstile script.

---

### 3.6 `[ollmh_appointment_form]`

Renders the appointment booking form (see [`FRONT-END-FORMS.md`](./FRONT-END-FORMS.md)
→ Appointment booking).

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `both` | Pre-select appointment type: `opd`, `clinic`, or `both` (user chooses) |
| `department` | string | `''` | Pre-select a department by slug |

**Usage:**
```html
[ollmh_appointment_form]

[ollmh_appointment_form type="opd" department="maternity"]
```

---

### 3.7 `[ollmh_application_form]`

Renders the multi-step nursing school application form (see
[`FRONT-END-FORMS.md`](./FRONT-END-FORMS.md) → Nursing school application).

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `programme` | string | `''` | Pre-select a programme (e.g. `krchn`, `en`). If omitted, user chooses. |
| `intake` | string | `''` | Pre-select an intake month (e.g. `september`). If omitted, user chooses. |

**Usage:**
```html
[ollmh_application_form]

[ollmh_application_form programme="krchn" intake="september"]
```

---

### 3.8 `[ollmh_event_registration]`

Renders the event registration form for a specific event. Used on event
single pages.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `event_id` | int | **required** | The event post ID. Required — if omitted, shows an error. |
| `show_event_details` | bool | `true` | Show event title, date, and location above the form |

**Usage:**
```html
[ollmh_event_registration event_id="42"]
```

On the event single template (`single-event.php`), this is rendered
automatically with the current event ID:
```php
echo do_shortcode('[ollmh_event_registration event_id="' . get_the_ID() . '"]');
```

---

### 3.9 `[ollmh_newsletter_form]`

Renders the newsletter signup form (used in the footer Band 2 and
optionally in a sidebar widget).

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `heading` | string | `Stay Updated` | Heading text above the form |
| `description` | string | `Get the latest news...` | Description text |
| `button_text` | string | `Subscribe` | Button label |

**Usage:**
```html
[ollmh_newsletter_form]

[ollmh_newsletter_form heading="Join Our Mailing List" button_text="Join Now"]
```

---

### 3.10 `[ollmh_upcoming_events]`

Displays a list of upcoming events, sorted by date.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | int | `5` | Maximum number of events to show |
| `show_date` | bool | `true` | Show event date |
| `show_location` | bool | `true` | Show event location |
| `show_excerpt` | bool | `false` | Show event excerpt |
| `category` | string | `''` | Filter by event category slug |

**Usage:**
```html
<!-- Show 5 upcoming events (home page sidebar) -->
[ollmh_upcoming_events limit="5"]

<!-- Show 3 community events -->
[ollmh_upcoming_events limit="3" category="community"]
```

**Output:**
```html
<div class="ollmh-upcoming-events">
  <article class="event-item">
    <time class="event-date" datetime="2024-03-15">Mar 15, 2024</time>
    <h4><a href="/events/annual-health-fair/">Annual Health Fair</a></h4>
    <p class="event-location">OLLMH Main Grounds</p>
  </article>
  <!-- More events... -->
</div>
```

---

### 3.11 `[ollmh_latest_news]`

Displays a list of the latest news articles.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | int | `5` | Maximum number of articles |
| `show_date` | bool | `true` | Show article date |
| `show_excerpt` | bool | `false` | Show article excerpt |
| `show_thumbnail` | bool | `true` | Show featured image thumbnail |
| `category` | string | `''` | Filter by news category slug |

**Usage:**
```html
<!-- Show 4 latest news on home page -->
[ollmh_latest_news limit="4" show_excerpt="true"]
```

---

### 3.12 `[ollmh_social_links]`

Displays social media icon links as inline SVGs (see
[`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md) → Icons).

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `size` | int | `20` | Icon size in pixels |
| `class` | string | `''` | Additional CSS class for the container |

**Usage:**
```html
[ollmh_social_links]

[ollmh_social_links size="32" class="footer-social"]
```

**Output:**
```html
<div class="ollmh-social-links footer-social">
  <a href="https://facebook.com/ollmh" aria-label="Facebook" target="_blank" rel="noopener noreferrer">
    <svg class="icon icon-facebook" width="32" height="32" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="..."/>
    </svg>
  </a>
  <a href="https://youtube.com/ollmh" aria-label="YouTube" target="_blank" rel="noopener noreferrer">
    <svg class="icon icon-youtube" ...>...</svg>
  </a>
  <a href="https://x.com/ollmh" aria-label="X (Twitter)" target="_blank" rel="noopener noreferrer">
    <svg class="icon icon-twitter" ...>...</svg>
  </a>
</div>
```

---

### 3.13 `[ollmh_hospital_hours]`

Displays the hospital's operating hours, sourced from `wp_settings`
(`opd_operating_hours`, `emergency_hours`, `clinic_hours` settings).

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `show_emergency` | bool | `true` | Show emergency hours |
| `show_clinic` | bool | `true` | Show clinic hours |

**Usage:**
```html
[ollmh_hospital_hours]
```

---

### 3.14 `[ollmh_breadcrumbs]`

Displays breadcrumb navigation (rendered by `class-ollmh-breadcrumbs.php`).

**Parameters:** None. Breadcrumbs are auto-generated based on the current
page hierarchy.

**Usage:**
```html
[ollmh_breadcrumbs]
```

Usually rendered in the theme template (`header.php` or a `breadcrumbs.php`
template part) rather than in content:
```php
echo do_shortcode('[ollmh_breadcrumbs]');
```

---

### 3.15 `[ollmh_gallery]`

Displays a photo gallery grid with lightbox functionality (GLightbox).

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `album_id` | int | `null` | Show photos from a specific `outlook_album` post. If omitted, shows all albums. |
| `columns` | int | `3` | Number of columns (2–5) |
| `limit` | int | `0` | Maximum photos to show. `0` = all |
| `show_caption` | bool | `true` | Show photo caption below thumbnail |

**Usage:**
```html
<!-- Show all gallery photos in 4 columns -->
[ollmh_gallery columns="4"]

<!-- Show photos from album ID 7 only -->
[ollmh_gallery album_id="7"]
```

**Output:**
```html
<div class="ollmh-gallery grid grid-3">
  <a href="full-image-url.jpg" class="gallery-lightbox" data-gallery="ollmh-gallery">
    <img src="thumbnail-url.jpg" alt="Photo caption" loading="lazy" class="gallery-thumbnail">
    <p class="gallery-caption">Photo caption</p>
  </a>
  <!-- More photos... -->
</div>
```

---

## 4. Registration code

All shortcodes are registered in `ollmh-core/includes/class-ollmh-shortcodes.php`:

```php
<?php
if (!defined('ABSPATH')) {
    exit;
}

class OLLMH_Shortcodes {

    public static function init(): void {
        add_shortcode('ollmh_clinic_schedule',     [self::class, 'clinic_schedule']);
        add_shortcode('ollmh_department_list',     [self::class, 'department_list']);
        add_shortcode('ollmh_staff_grid',          [self::class, 'staff_grid']);
        add_shortcode('ollmh_ward_status',         [self::class, 'ward_status']);
        add_shortcode('ollmh_contact_form',        [self::class, 'contact_form']);
        add_shortcode('ollmh_appointment_form',    [self::class, 'appointment_form']);
        add_shortcode('ollmh_application_form',    [self::class, 'application_form']);
        add_shortcode('ollmh_event_registration',  [self::class, 'event_registration']);
        add_shortcode('ollmh_newsletter_form',     [self::class, 'newsletter_form']);
        add_shortcode('ollmh_upcoming_events',     [self::class, 'upcoming_events']);
        add_shortcode('ollmh_latest_news',         [self::class, 'latest_news']);
        add_shortcode('ollmh_social_links',        [self::class, 'social_links']);
        add_shortcode('ollmh_hospital_hours',      [self::class, 'hospital_hours']);
        add_shortcode('ollmh_breadcrumbs',         [self::class, 'breadcrumbs']);
        add_shortcode('ollmh_gallery',             [self::class, 'gallery']);
    }

    public static function clinic_schedule(array $atts): string {
        $args = shortcode_atts([
            'clinic_id' => null,
            'day'       => null,
            'limit'     => 0,
        ], $atts);

        // Query wp_clinic_schedules or clinic CPT
        // Build and return HTML table
        ob_start();
        include OLLMH_PLUGIN_DIR . 'templates/shortcodes/clinic-schedule.php';
        return ob_get_clean();
    }

    public static function staff_grid(array $atts): string {
        $args = shortcode_atts([
            'department'           => '',
            'columns'              => 4,
            'limit'                => 0,
            'show_title'           => true,
            'show_qualifications'  => true,
            'show_bio'             => false,
            'orderby'              => 'menu_order',
        ], $atts);

        $query_args = [
            'post_type'      => 'staff_member',
            'posts_per_page' => (int) $args['limit'] ?: -1,
            'orderby'        => $args['orderby'],
            'order'          => 'ASC',
        ];
        if (!empty($args['department'])) {
            $query_args['tax_query'] = [[
                'taxonomy' => 'department',
                'field'    => 'slug',
                'terms'    => $args['department'],
            ]];
        }
        $staff = new WP_Query($query_args);

        ob_start();
        include OLLMH_PLUGIN_DIR . 'templates/shortcodes/staff-grid.php';
        wp_reset_postdata();
        return ob_get_clean();
    }

    // ... other shortcode methods follow the same pattern
}
```

Each shortcode method:
1. Parses attributes via `shortcode_atts()`
2. Queries the database (via `WP_Query` for CPTs, or `$wpdb` for custom tables)
3. Includes a template file from `templates/shortcodes/` for the HTML output
4. Returns the HTML string (via output buffering)

---

## 5. Template files

Shortcode HTML templates live in `ollmh-core/templates/shortcodes/`:

```
ollmh-core/
└── templates/
    └── shortcodes/
        ├── clinic-schedule.php
        ├── department-list.php
        ├── staff-grid.php
        ├── ward-status.php
        ├── contact-form.php
        ├── appointment-form.php
        ├── application-form.php
        ├── event-registration.php
        ├── newsletter-form.php
        ├── upcoming-events.php
        ├── latest-news.php
        ├── social-links.php
        ├── hospital-hours.php
        ├── breadcrumbs.php
        └── gallery.php
```

These templates are overridable by the theme — a theme can copy any
template to `wp-content/themes/ollmh-theme/templates/shortcodes/` to
customize the output without modifying the plugin.
