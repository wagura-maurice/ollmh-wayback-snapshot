# Self Sustainability Projects (`/self-sustainability-projects.html`)

> Presents the hospital's modern-agriculture ventures through which it pursues self-reliance and feeds patients and the wider community.

## 1. Current State Mapping

- **Page title (`h1.title`):** "Self Sustinabilbity Projects" (spelling as in source; human title: "Self Sustainability Projects").
- **Intro:** Heading "Self Sustainability Projects." with a statement that **Our Lady of Lourdes Mwea Hospital is the only health institution and community that has pursued self reliance through modern agriculture.**
- **Project sub-sections (headings + short paragraphs within the article body):**
  - **Rice Farming.** — the hospital uses the area's climate, which makes rice farming possible, to give patients fresh and healthy food from its own resources.
  - **Dairy Farming.** — an effort to achieve self-support in milk production for patients and the entire community of the hospital.
  - **Poultry Farming.** — poultry farming carried out at the hospital (short caption-style text).
  - **Maize Farming** — a maize-farming project (2013 maize farming imagery).
- **Images / gallery (subjects inferred from paths; alt text empty):**
  - `Sustainability_Projects/ollmhricefields2.gif` — the hospital's rice fields.
  - `Agriculture/SAM_3188.JPG`, `Agriculture/SAM_3186.JPG` — agriculture/dairy scenes.
  - `Sustainability_Projects/DSC07854.JPG`, `DSC07871.JPG`, `DSC07867.JPG` — poultry / farm activity photos.
  - `Sustainability_Projects/2013maizefarming/DSC06228.JPG`, `DSC06229.JPG`, `DSC06230.JPG` — 2013 maize farming photos.
- **Interactive/boilerplate elements (ignored):** header megamenu, Print/Email actions, Prev/Next navigation, footer columns.

**Notes on fidelity:** The page is image-heavy with brief captions per farming activity; no lists, tables or forms are present, and image `alt` attributes are empty.

## 2. Gap Analysis & Feature Enhancements

### Content & structure
- Model each venture (Rice, Dairy, Poultry, Maize) as a structured **sustainability project** with description, scale, yield, and gallery.
- Add **production/yield figures** (e.g., bags of rice/maize per season, litres of milk per day, number of birds) and how much feeds patients vs. is sold.
- Explain the **self-reliance financial model**: revenue reinvested into patient care.

### Media & storytelling
- Descriptive `alt` text and real captions; seasonal galleries and short video tours of the farm.
- Map/location context of the fields relative to the hospital.

### Engagement & impact
- **Impact metrics dashboard** (meals provided, cost savings, community members employed).
- Optional **farm-produce / support CTAs** and partnership enquiries.
- Seasonal updates / blog-style harvest logs.

### Technical / SEO / a11y
- Structured data (`Project`), descriptive meta, alt text, lazy-loaded responsive galleries.
- Cross-links to Development and Community Support pages.

## 3. Database Schema Design

```sql
-- Self-sustainability (agriculture) ventures: rice, dairy, poultry, maize...
CREATE TABLE wp_sustainability_projects (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  slug           VARCHAR(191)    NOT NULL,
  title          VARCHAR(255)    NOT NULL,
  category       ENUM('crop','dairy','poultry','livestock','other') NOT NULL DEFAULT 'crop',
  summary        VARCHAR(512)    NULL,
  description    TEXT            NULL,
  cover_media_id BIGINT UNSIGNED NULL,
  is_active      TINYINT(1)      NOT NULL DEFAULT 1,
  sort_order     INT UNSIGNED    NOT NULL DEFAULT 0,
  status         ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  published_at   DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at     TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_susproj_slug (slug),
  KEY idx_susproj_page (page_id),
  KEY idx_susproj_category (category),
  CONSTRAINT fk_susproj_page  FOREIGN KEY (page_id)        REFERENCES wp_pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_susproj_cover FOREIGN KEY (cover_media_id) REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seasonal production / yield records to support impact metrics
CREATE TABLE wp_sustainability_production_records (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  project_id BIGINT UNSIGNED NOT NULL,
  season_label VARCHAR(100)  NULL,               -- e.g. "2013 Long Rains"
  period_year YEAR           NULL,
  quantity   DECIMAL(12,2)   NULL,
  unit       VARCHAR(50)     NULL,               -- kg, bags, litres, birds
  notes      VARCHAR(512)    NULL,
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_susprod_project (project_id),
  CONSTRAINT fk_susprod_project FOREIGN KEY (project_id) REFERENCES wp_sustainability_projects (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Per-project gallery images from the shared media library
CREATE TABLE wp_sustainability_project_media (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  project_id BIGINT UNSIGNED NOT NULL,
  media_id   BIGINT UNSIGNED NOT NULL,
  caption    VARCHAR(512)    NULL,
  sort_order INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_susproj_media (project_id, media_id),
  CONSTRAINT fk_spm_project FOREIGN KEY (project_id) REFERENCES wp_sustainability_projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_spm_media   FOREIGN KEY (media_id)   REFERENCES wp_media_assets (id)            ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `wp_sustainability_projects.page_id` → `wp_pages.id` ties each venture to the `/self-sustainability-projects.html` page (cascades on page delete).
- `wp_sustainability_projects.cover_media_id` and `wp_sustainability_project_media.media_id` → `wp_media_assets.id` reuse the shared media library.
- `wp_sustainability_production_records.project_id` → `wp_sustainability_projects.id` records seasonal yields powering the impact metrics.
- `wp_sustainability_project_media` is the ordered gallery bridge between projects and `wp_media_assets`.
