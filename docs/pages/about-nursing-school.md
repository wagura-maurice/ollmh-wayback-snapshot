# About The Nursing School (`/about-nursing-school.html`)

> Intended to describe Our Lady of Lourdes School of Nursing, but the archived page is only a placeholder stub — content was not captured by the Wayback Machine.

## 1. Current State Mapping

- **Page title:** browser title and in-body `h1` both read **"About The Nursing School"**.
- **Actual content:** this snapshot is a **placeholder stub**, not the real page. The body contains only:
  - Heading "About The Nursing School".
  - A single paragraph: *"This page was not available in the Wayback Machine archive. Content will be added soon."*
  - A "← Back to Home" link to `index.html`.
- **Reduced chrome:** unlike other pages, this file ships a stripped template — only the logo (`id="top"`) and a minimal megamenu containing just the **Home** item. No full navigation, search box, footer columns, slideshow, or Print/Email actions.
- **No images, lists, tables, or forms** are present.
- **Related content exists elsewhere:** the `news-events.html` page and the "Nursing Sch-" menu group carry the substantive nursing-school narrative and the application-form link, so this page is expected to become the canonical "About" page for the school.

## 2. Gap Analysis & Feature Enhancements

**Content gaps (the page is essentially empty)**
- Author the real "About the School of Nursing" content: history, accreditation (e.g. Nursing Council of Kenya), mission/vision, programmes offered (Diploma in Nursing, etc.), duration, intake schedule, entry requirements, fees, facilities (classrooms, skills lab, dormitory, library), and faculty.
- Add a campus/facilities gallery (school bus, dormitories, labs) and student life highlights.
- Surface clear CTAs: "Apply now" (link to the application form) and "Contact admissions".

**UX/UI**
- Restore the full site chrome (navigation, footer, search) so the page is consistent with the rest of the site.
- Programme cards, an admissions timeline, and an FAQ accordion.

**Functionality & integrations**
- Downloadable prospectus/brochure and an online enquiry form.
- Testimonials from alumni/current students; graduation statistics.
- Link to the online application workflow and intake announcements.

**Accessibility & SEO**
- Proper meta title/description, `EducationalOrganization`/`Course` schema.org markup, and `alt` text for all imagery.

## 3. Database Schema Design

```sql
-- Core profile for the School of Nursing (single canonical record per page)
CREATE TABLE wp_nursing_school_profile (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  name          VARCHAR(191)    NOT NULL DEFAULT 'Our Lady of Lourdes School of Nursing',
  overview      MEDIUMTEXT      NULL,
  history       MEDIUMTEXT      NULL,
  mission       TEXT            NULL,
  vision        TEXT            NULL,
  accreditation VARCHAR(255)    NULL,   -- e.g. "Nursing Council of Kenya"
  hero_media_id BIGINT UNSIGNED NULL,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_nsp_page (page_id),
  CONSTRAINT fk_nsp_page FOREIGN KEY (page_id)       REFERENCES wp_pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_nsp_hero FOREIGN KEY (hero_media_id) REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Programmes/courses offered by the school
CREATE TABLE wp_nursing_programmes (
  id                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  school_profile_id BIGINT UNSIGNED NOT NULL,
  name              VARCHAR(191)    NOT NULL,  -- e.g. "Diploma in Nursing (KRCHN)"
  slug              VARCHAR(191)    NOT NULL,
  level             ENUM('certificate','diploma','higher_diploma','degree') NOT NULL DEFAULT 'diploma',
  duration_months   SMALLINT UNSIGNED NULL,
  entry_requirements TEXT           NULL,
  tuition_fee       DECIMAL(12,2)   NULL,
  description       MEDIUMTEXT      NULL,
  is_active         TINYINT(1)      NOT NULL DEFAULT 1,
  sort_order        INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_prog_slug (slug),
  KEY idx_prog_school (school_profile_id, sort_order),
  CONSTRAINT fk_prog_school FOREIGN KEY (school_profile_id) REFERENCES wp_nursing_school_profile (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Facilities / campus features to showcase
CREATE TABLE wp_nursing_facilities (
  id                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  school_profile_id BIGINT UNSIGNED NOT NULL,
  name              VARCHAR(191)    NOT NULL,  -- e.g. "Skills Lab", "Dormitory"
  description       TEXT            NULL,
  media_id          BIGINT UNSIGNED NULL,
  sort_order        INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_fac_school (school_profile_id, sort_order),
  CONSTRAINT fk_fac_school FOREIGN KEY (school_profile_id) REFERENCES wp_nursing_school_profile (id) ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_fac_media  FOREIGN KEY (media_id)          REFERENCES wp_media_assets (id)           ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Admission intake windows
CREATE TABLE wp_nursing_intakes (
  id                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  programme_id      BIGINT UNSIGNED NOT NULL,
  intake_label      VARCHAR(100)    NOT NULL,  -- e.g. "September 2026"
  opens_on          DATE            NULL,
  closes_on         DATE            NULL,
  seats_available   SMALLINT UNSIGNED NULL,
  is_open           TINYINT(1)      NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_intake_prog (programme_id, opens_on),
  CONSTRAINT fk_intake_prog FOREIGN KEY (programme_id) REFERENCES wp_nursing_programmes (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `wp_nursing_school_profile.page_id → wp_pages.id` makes this page the canonical home for the school (one profile per page).
- `wp_nursing_programmes` and `wp_nursing_facilities` hang off `wp_nursing_school_profile` (cascade delete); `wp_nursing_intakes` hang off programmes.
- Media everywhere references the shared **`wp_media_assets`** library; `hero_media_id`/`media_id` use `ON DELETE SET NULL`.
- `wp_nursing_programmes` are the natural target for the application workflow defined in [`medical-school-application-form.md`](./medical-school-application-form.md) (`wp_applications.programme_id → wp_nursing_programmes.id`) and for intake announcements in [`news-wp_events.md`](./news-wp_events.md).
