# Location (`/about-ollmh-location.html`)

> Introduces Our Lady of Lourdes Mwea Hospital (OLLMH) — its Catholic ownership, history, mandate, physical location, and the disease burden it addresses.

## 1. Current State Mapping

**Page title:** "Location" (rendered from `<h1 class="title">`).

**Page actions:** Standard Joomla "Print" and "Email" icons in the article header (boilerplate, not core content).

**Textual content (faithful summary of the archived copy):**

- **Opening/identity paragraph:** *Our Lady of Lourdes Mwea Hospital* (OLLMH) is a Catholic institution run by the **Sisters of Mary Immaculate of Nyeri**, who are the sole proprietors of the facility, in collaboration with the **Catholic Diocese of Murang'a**. It is a registered **non-governmental organization (NGO)** with the mandate of delivering affordable and accessible health services to all, especially the poor and vulnerable. It is described as one of the largest **County Referral (Tier 3)** hospitals in **Kirinyaga County**, serving a large and diverse population of approximately **500,000**. History: started in **1962 as a dispensary**, promoted to a **health centre in 1968**, and grew into a **modern referral hospital after upgrading in 1979**. Includes an inline cross-reference/link to *Our Lady Of Lourdes Nursing School (OLLMNS)*.
- **Teaching/training paragraph:** Beyond healthcare, the hospital offers facilities for teaching/training of health professionals — **Diploma in Nursing**, an **internship centre** for Medicine students (Bachelors) and clinical medicine students (Diploma), and an **attachment centre** for pharmacist technologists, laboratory technologists, and social workers — plus research. It notes OLLMH's role in the region through partnerships with the community, public health, and other organizations.
- **Location paragraph:** OLLMH is located **along the Nairobi–Embu road, about 1.5 km from Ngurubani town**.
- **Sustainability context:** Situated in a rice-growing area, the hospital sustained itself by providing healthcare services to rice farmers.
- **Health impact paragraph:** Over the past decade the hospital reports eliminating up to **99%** of waterborne/water-related diseases (malaria, schistosomiasis, gastroenteritis, typhoid, cholera, amoebiasis, giardiasis, helminthiasis, tuberculosis) and raising standards in managing other conditions (HIV/AIDS/PTB, pneumonia, ARI, diabetes mellitus, heart disease, liver disease, renal pathology, cancers, skin diseases, anaemia, accidents/fractures/burns, dental/eye diseases, mental problems, abortions, arthritis). Ends with a **"Contact us"** link to `/contacts.html`.

**Images (three inline galleries, ~9 photos, all with empty `alt`):**
- Row 1: Administrator building/portrait (`Aministration/Administrator.jpg`), Dental Unit (`Dental_Unit_photos/DSCF7445.JPG`), miscellaneous select photo (`misc_Select/DSCF7459.JPG`).
- Row 2: Two miscellaneous department photos (`MiscDept/DSCF7407.JPG`, `MiscDept/DSCF7409.JPG`) and a developments/achievements photo (`DSC03927.JPG`).
- Row 3: Rice fields (`Sustainability_Projects/ollmhricefields2.gif`, `ricefield2.jpg`) and a misc department photo (`MiscDept/DSCF7388.JPG`).

**Interactive elements:** Inline hyperlinks (Nursing School reference and "Contact us"); Print/Email actions. No forms, tables, or embedded map on this page (despite the "Location" title).

## 2. Gap Analysis & Feature Enhancements

**Content Gaps**
- Title is "Location" but there is **no map, GPS coordinates, or directions** — the single most expected feature is missing.
- No structured "quick facts" (founding year timeline, bed capacity, catchment population, Tier level) despite the text mentioning them.
- Images have **empty alt text** and no captions, so their subjects (dental unit, rice fields, admin block) are undiscoverable.
- No public-transport / driving directions, parking, or landmark guidance from Ngurubani town.

**UX/UI**
- Convert the three photo blobs into a proper **responsive gallery/lightbox** with captions.
- Add an at-a-glance **fact sidebar** (established 1962, referral Tier 3, ~500,000 catchment, owner: Sisters of Mary Immaculate).
- Present the hospital history as a **visual timeline** (1962 → 1968 → 1979 → present).

**Functionality**
- Embed an **interactive Google/OpenStreetMap** with a pin, plus a "Get directions" button.
- "Get in touch" CTA wired to the contacts page / a lead form.

**Trust/Accessibility**
- Add meaningful `alt` text and `<figure>/<figcaption>` markup.
- Structured data (`MedicalOrganization` / `Hospital` schema.org) with geo, foundingDate, and areaServed for SEO and rich results.
- Cite the disease-elimination claims or soften to avoid unverifiable "99%" statistics.

## 3. Database Schema Design

```sql
-- Key facts / statistics shown on the About-Location page
CREATE TABLE wp_about_facts (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id     BIGINT UNSIGNED NOT NULL,
  label       VARCHAR(191)    NOT NULL,          -- e.g. "Catchment population"
  value       VARCHAR(255)    NOT NULL,          -- e.g. "~500,000"
  icon        VARCHAR(100)    NULL,
  sort_order  INT UNSIGNED    NOT NULL DEFAULT 0,
  status      ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at  TIMESTAMP       NULL,
  PRIMARY KEY (id),
  KEY idx_about_facts_page (page_id, sort_order),
  CONSTRAINT fk_about_facts_page FOREIGN KEY (page_id)
    REFERENCES wp_pages (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- History milestones (1962 dispensary, 1968 health centre, 1979 upgrade, ...)
CREATE TABLE wp_about_milestones (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id     BIGINT UNSIGNED NOT NULL,
  year        SMALLINT UNSIGNED NULL,
  headline    VARCHAR(191)    NOT NULL,
  description TEXT            NULL,
  media_id    BIGINT UNSIGNED NULL,
  sort_order  INT UNSIGNED    NOT NULL DEFAULT 0,
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_about_milestones_page (page_id, sort_order),
  CONSTRAINT fk_about_milestones_page  FOREIGN KEY (page_id)  REFERENCES wp_pages (id)        ON DELETE CASCADE   ON UPDATE CASCADE,
  CONSTRAINT fk_about_milestones_media FOREIGN KEY (media_id) REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Geographic location / map data for the hospital
CREATE TABLE wp_location_info (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  address_line   VARCHAR(255)    NULL,        -- "Along Nairobi-Embu road"
  landmark       VARCHAR(255)    NULL,        -- "~1.5km from Ngurubani town"
  town           VARCHAR(120)    NULL,        -- Ngurubani / Mwea
  county         VARCHAR(120)    NULL,        -- Kirinyaga
  country        VARCHAR(120)    NOT NULL DEFAULT 'Kenya',
  latitude       DECIMAL(10,7)   NULL,
  longitude      DECIMAL(10,7)   NULL,
  map_embed_url  VARCHAR(512)    NULL,
  directions     TEXT            NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_location_page (page_id),
  CONSTRAINT fk_location_page FOREIGN KEY (page_id)
    REFERENCES wp_pages (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `wp_about_facts.page_id`, `wp_about_milestones.page_id`, and `wp_location_info.page_id` all reference `pages(id)`, binding this content to the "Location" page row (`slug = about-ollmh-location`).
- `wp_about_milestones.media_id` and the page's gallery images reference `media_assets(id)`; the ordered photo galleries are stored via the shared `wp_page_media` join table (role `gallery`).
- `wp_location_info` is a 1:1 satellite of `wp_pages` (unique `page_id`) supplying map/geo data for the embedded map and directions CTA.
