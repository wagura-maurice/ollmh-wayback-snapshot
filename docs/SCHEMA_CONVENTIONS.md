# Platform Schema Conventions (Shared Reference)

> **⚠️ Read [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md) →
> ADR-006 first.** Per ADR-006 (Approved), the OLLMH data layer is
> **WordPress-native**. Most shared entities here map to core WordPress:
> `wp_pages` → core Pages, `wp_media_assets`/`wp_page_media` → the Media
> Library (attachments), `wp_users` → core Users, `wp_menu_items` → nav menus,
> `wp_departments` → the `department` CPT, and `wp_staff` → the `staff_member`
> CPT. Only `wp_settings` (and the operational tables listed in ADR-006) are
> created as real SQL tables. The `CREATE TABLE` blocks below are retained as
> **field specifications**; the conventions still apply to the retained custom
> tables and to CPT postmeta field design.

This document defines the **shared, platform-wide database tables** that every
per-page schema in [`docs/pages/`](./pages/) is expected to integrate with via
foreign keys. It exists so that the site can transition from a static Wayback
snapshot into a fully dynamic, database-driven application (the original site
was a Joomla install; this design is a clean, modern re-modelling).

All tables use the following conventions:

- **Engine / charset:** `InnoDB`, `utf8mb4` / `utf8mb4_unicode_ci`.
- **Primary keys:** `BIGINT UNSIGNED AUTO_INCREMENT` named `id`.
- **Timestamps:** every table has `created_at` and `updated_at`
  (`TIMESTAMP`, default `CURRENT_TIMESTAMP` / `ON UPDATE CURRENT_TIMESTAMP`).
- **Soft deletes:** content tables carry a nullable `deleted_at TIMESTAMP`.
- **Publishing:** content tables carry `status ENUM('draft','published','archived')`
  and `published_at DATETIME NULL`.
- **Slugs:** human-readable `VARCHAR(191)` `slug` columns are `UNIQUE`.
- **FK actions:** `ON DELETE RESTRICT ON UPDATE CASCADE` unless otherwise noted;
  optional links use `ON DELETE SET NULL`.

---

## Core shared tables

These are defined **once here**. Individual page files reference them (e.g.
`page_id BIGINT UNSIGNED` → `wp_pages.id`) rather than redefining them.

### `wp_pages`
The backbone of the dynamic site. Every navigable page/route is a row here.

```sql
CREATE TABLE wp_pages (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  slug          VARCHAR(191)    NOT NULL,
  title         VARCHAR(255)    NOT NULL,
  page_type     ENUM('home','about','service','department','ward','project',
                     'community','feature','news','contact','form','nursing',
                     'generic') NOT NULL DEFAULT 'generic',
  meta_title    VARCHAR(255)    NULL,
  meta_desc     VARCHAR(320)    NULL,
  hero_media_id BIGINT UNSIGNED NULL,
  body_intro    TEXT            NULL,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_pages_slug (slug),
  KEY idx_pages_type_status (page_type, status),
  CONSTRAINT fk_pages_hero_media FOREIGN KEY (hero_media_id)
    REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `wp_media_assets`
Central library for every image/document/video referenced anywhere on the site.

```sql
CREATE TABLE wp_media_assets (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  file_path    VARCHAR(512)    NOT NULL,
  mime_type    VARCHAR(100)    NOT NULL,
  media_type   ENUM('image','document','video','audio','other') NOT NULL DEFAULT 'image',
  alt_text     VARCHAR(255)    NULL,
  caption      VARCHAR(512)    NULL,
  width_px     INT UNSIGNED    NULL,
  height_px    INT UNSIGNED    NULL,
  file_size    BIGINT UNSIGNED NULL,
  uploaded_by  BIGINT UNSIGNED NULL,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_media_type (media_type),
  CONSTRAINT fk_media_uploader FOREIGN KEY (uploaded_by)
    REFERENCES wp_users (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `wp_page_media`
Join table associating pages with an ordered gallery of media.

```sql
CREATE TABLE wp_page_media (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id    BIGINT UNSIGNED NOT NULL,
  media_id   BIGINT UNSIGNED NOT NULL,
  role       ENUM('gallery','inline','thumbnail','banner') NOT NULL DEFAULT 'gallery',
  sort_order INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_page_media (page_id, media_id, role),
  CONSTRAINT fk_pm_page  FOREIGN KEY (page_id)  REFERENCES wp_pages (id)        ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_pm_media FOREIGN KEY (media_id) REFERENCES wp_media_assets (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `wp_users`
Admins/editors (CMS backend) and, where relevant, registered portal users.

```sql
CREATE TABLE wp_users (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name          VARCHAR(191)    NOT NULL,
  email         VARCHAR(191)    NOT NULL,
  password_hash VARCHAR(255)    NOT NULL,
  role          ENUM('super_admin','editor','author','viewer') NOT NULL DEFAULT 'author',
  is_active     TINYINT(1)      NOT NULL DEFAULT 1,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `wp_settings`
Central key-value store for all platform configuration — hospital identity,
contact details, clinical operations, nursing school, applications, SEO,
email/SMTP, M-Pesa, security, and reference data (dropdowns for patient
registration, staff records, and applications). See
[`SETTINGS.md`](./SETTINGS.md) for the full settings catalogue and
[`seeders/class-ollmh-settings-seeder.php`](../seeders/class-ollmh-settings-seeder.php)
for the PHP seeder.

```sql
CREATE TABLE wp_settings (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  item          VARCHAR(191)    NOT NULL,
  default_value LONGTEXT        NULL,
  current_value LONGTEXT        NULL,
  description   TEXT            NULL,
  type          ENUM('string','text','json','boolean','integer','decimal',
                     'url','email','secret','date','datetime','file')
                  NOT NULL DEFAULT 'string',
  group_name    VARCHAR(100)    NOT NULL DEFAULT 'general',
  is_public     TINYINT(1)      NOT NULL DEFAULT 0,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_settings_item (item),
  KEY idx_settings_group (group_name),
  KEY idx_settings_public (is_public)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Column notes:**

| Column | Purpose |
|---|---|
| `item` | Unique setting key (e.g. `hospital_name`, `mpesa_shortcode`, `profile_blood_types`). |
| `default_value` | Factory default. Set by the seeder. Never overwritten by the admin UI. |
| `current_value` | The live value. Set by the admin. If the admin never customised it, it equals `default_value`. |
| `description` | Human-readable explanation of what the setting controls. |
| `type` | Data type hint for the admin UI (render a text field, textarea, toggle, JSON editor, password field, etc.). `secret` values are stored encrypted and never exposed to the front-end. |
| `group_name` | Feature-area grouping for the admin settings page (e.g. `general`, `contact`, `clinical`, `seo`, `financial`). |
| `is_public` | 1 = safe to expose to the front-end (e.g. hospital name, phone, social links). 0 = admin-only (e.g. SMTP password, M-Pesa keys). The front-end settings API only returns rows where `is_public = 1`. |

**Upsert logic:** The seeder uses insert-only upsert — it sets
`current_value = default_value` on first insert, and never overwrites a
`current_value` that an admin has already customised. On re-runs, it
refreshes `default_value` and syncs `current_value` only if it is still
null, empty, or equal to the old default.

### `wp_menu_items`
Drives the header navigation megamenu and footer link columns.

```sql
CREATE TABLE wp_menu_items (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  menu_area   ENUM('header','footer','offcanvas') NOT NULL DEFAULT 'header',
  parent_id   BIGINT UNSIGNED NULL,
  label       VARCHAR(191)    NOT NULL,
  page_id     BIGINT UNSIGNED NULL,   -- internal target
  external_url VARCHAR(512)   NULL,   -- external target
  sort_order  INT UNSIGNED    NOT NULL DEFAULT 0,
  is_active   TINYINT(1)      NOT NULL DEFAULT 1,
  PRIMARY KEY (id),
  KEY idx_menu_area (menu_area, parent_id, sort_order),
  CONSTRAINT fk_menu_parent FOREIGN KEY (parent_id) REFERENCES wp_menu_items (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_menu_page   FOREIGN KEY (page_id)   REFERENCES wp_pages (id)      ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `wp_departments`
Referenced by service pages, ward pages, staff, and clinic schedules.

```sql
CREATE TABLE wp_departments (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name        VARCHAR(191)    NOT NULL,
  slug        VARCHAR(191)    NOT NULL,
  category    ENUM('inpatient','outpatient','clinical','support','administrative','community') NOT NULL DEFAULT 'clinical',
  page_id     BIGINT UNSIGNED NULL,
  description TEXT            NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_dept_slug (slug),
  CONSTRAINT fk_dept_page FOREIGN KEY (page_id) REFERENCES wp_pages (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `wp_staff`
Referenced by administration, HR-capacity, and department pages.

```sql
CREATE TABLE wp_staff (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  full_name     VARCHAR(191)    NOT NULL,
  title         VARCHAR(191)    NULL,      -- e.g. "Medical Superintendent"
  role_type     ENUM('management','board','clinical','nursing','support','volunteer') NOT NULL DEFAULT 'clinical',
  department_id BIGINT UNSIGNED NULL,
  photo_media_id BIGINT UNSIGNED NULL,
  bio           TEXT            NULL,
  email         VARCHAR(191)    NULL,
  phone         VARCHAR(40)     NULL,
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  is_active     TINYINT(1)      NOT NULL DEFAULT 1,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_staff_dept (department_id),
  CONSTRAINT fk_staff_dept  FOREIGN KEY (department_id)  REFERENCES wp_departments (id)   ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_staff_photo FOREIGN KEY (photo_media_id) REFERENCES wp_media_assets (id)  ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## How per-page files use these

Each file in `docs/pages/` defines **only the tables specific to that page's
content** and references the shared tables above by foreign key. For example, a
service page's `services` table carries `page_id → wp_pages.id` and
`department_id → wp_departments.id`; it does **not** redefine `wp_pages` or
`wp_departments`.

This keeps the schema normalized and lets every page plug into one coherent,
database-driven platform.
