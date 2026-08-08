# S.M.I Community (`/smi-community.html`)

> Introduces the Sisters of Mary Immaculate (SMI) religious community that owns and manages the hospital, and their convent, infirmary and charism of service.

## 1. Current State Mapping

- **Page title (`h1.title`):** "S.M.I Community".
- **Charism / management intro:** A paragraph explaining that **Our Lady of Lourdes Mwea Hospital (OLLMH) is under the management of the Sisters of Mary Immaculate.** Their call is "to serve and not to be served." Within the hospital compound they have a **convent** where the sisters live as a community, and it is also where their **infirmary (the home of the old)** is located. The Sisters state they are determined to reach out to many in all dimensions of life as people come looking for physical healing, and they also aim for healing of the souls — quoting "Go out to the whole world proclaim the good news."
- **Captioned photo groups (inline):**
  - **Mary Immaculate Sisters** — group photo of the community.
  - **Cake cutting during the opening of OLLMH Nursing School** — sisters at the nursing-school opening ceremony.
  - **Catholic Women Association (C.W.A) members** during their visit to the OLLMH S.M.I sisters.
  - **"Happy Birthday" / the eldest in the S.M.I celebrating her 100 years birthday** — centenarian sister's birthday celebration.
- **Images / gallery (subjects inferred from paths; alt empty):**
  - `images/structure.jpg` — organizational/structure image.
  - `S.M.IMwea/SRSOpensch.JPG` — sisters at a school-opening event.
  - `S.M.IMwea/DSC09126.JPG` — community gathering photo.
  - `S.M.IMwea/srs_CA.JPG` — sisters with Catholic Women Association members.
  - `S.M.IMwea/JosewithSreldest.JPG` — photo with the eldest sister.
  - `S.M.IMwea/Sroldest.JPG` — the eldest sister (100th birthday).
- **Interactive/boilerplate elements (ignored):** header megamenu, Print/Email actions, Prev/Next navigation, footer columns.

**Notes on fidelity:** The page combines a mission/charism narrative with community-life photographs and event captions. There are no lists, tables or forms, and image `alt` attributes are empty.

## 2. Gap Analysis & Feature Enhancements

### Content & structure
- Model the **congregation profile** (name, motto/charism, founding, guiding scripture) as structured content rather than one prose block.
- Add distinct records for **community facilities** (convent, infirmary/home of the old) with descriptions and capacity.
- Curate **community events** (nursing-school opening, C.W.A visits, milestone birthdays) as an event timeline.

### Media & storytelling
- Descriptive alt/captions; event-based galleries and short sister profiles/testimonies.
- A brief history/timeline of the Sisters of Mary Immaculate at Mwea.

### Engagement & impact
- **Vocations enquiry / contact form** for those interested in joining or supporting the community.
- **Prayer-request and donation CTAs** supporting the infirmary/home of the old.
- Highlight the link between the congregation's charism and the hospital's mission.

### Technical / SEO / a11y
- Structured data (`Organization`/`Person`), meta descriptions, alt text, accessible galleries.
- Cross-links to Administration, Philosophy of Care, and Nursing School pages.

## 3. Database Schema Design

```sql
-- Profile of the religious congregation that manages the hospital
CREATE TABLE wp_smi_community_profile (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  name           VARCHAR(191)    NOT NULL,          -- "Sisters of Mary Immaculate"
  motto          VARCHAR(255)    NULL,              -- "To serve and not to be served"
  guiding_scripture VARCHAR(512) NULL,              -- "Go out to the whole world..."
  charism        TEXT            NULL,
  history        TEXT            NULL,
  cover_media_id BIGINT UNSIGNED NULL,
  status         ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  published_at   DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at     TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_smiprofile_page (page_id),
  CONSTRAINT fk_smiprofile_page  FOREIGN KEY (page_id)        REFERENCES wp_pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_smiprofile_cover FOREIGN KEY (cover_media_id) REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Facilities within the compound (convent, infirmary / home of the old)
CREATE TABLE wp_smi_facilities (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  slug           VARCHAR(191)    NOT NULL,
  name           VARCHAR(191)    NOT NULL,          -- "Convent", "Infirmary (Home of the Old)"
  facility_type  ENUM('convent','infirmary','chapel','other') NOT NULL DEFAULT 'other',
  description    TEXT            NULL,
  cover_media_id BIGINT UNSIGNED NULL,
  sort_order     INT UNSIGNED    NOT NULL DEFAULT 0,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_smifacility_slug (slug),
  KEY idx_smifacility_page (page_id),
  CONSTRAINT fk_smifacility_page  FOREIGN KEY (page_id)        REFERENCES wp_pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_smifacility_cover FOREIGN KEY (cover_media_id) REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Community life events (nursing school opening, C.W.A visit, 100th birthday...)
CREATE TABLE wp_smi_community_events (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id      BIGINT UNSIGNED NOT NULL,
  title        VARCHAR(255)    NOT NULL,
  event_type   ENUM('opening','visit','celebration','anniversary','other') NOT NULL DEFAULT 'other',
  event_date   DATE            NULL,
  description  TEXT            NULL,
  cover_media_id BIGINT UNSIGNED NULL,
  sort_order   INT UNSIGNED    NOT NULL DEFAULT 0,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_smievent_page (page_id),
  CONSTRAINT fk_smievent_page  FOREIGN KEY (page_id)        REFERENCES wp_pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_smievent_cover FOREIGN KEY (cover_media_id) REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Vocations / support enquiries submitted from this page
CREATE TABLE wp_smi_vocation_enquiries (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id      BIGINT UNSIGNED NOT NULL,
  full_name    VARCHAR(191)    NOT NULL,
  email        VARCHAR(191)    NULL,
  phone        VARCHAR(40)     NULL,
  enquiry_type ENUM('vocation','prayer_request','support','general') NOT NULL DEFAULT 'general',
  message      TEXT            NULL,
  enquiry_status ENUM('new','read','responded','closed') NOT NULL DEFAULT 'new',
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_smienq_page (page_id),
  CONSTRAINT fk_smienq_page FOREIGN KEY (page_id) REFERENCES wp_pages (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Gallery images tied to community events from the shared media library
CREATE TABLE wp_smi_event_media (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  event_id   BIGINT UNSIGNED NOT NULL,
  media_id   BIGINT UNSIGNED NOT NULL,
  caption    VARCHAR(512)    NULL,
  sort_order INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_smievent_media (event_id, media_id),
  CONSTRAINT fk_sem_event FOREIGN KEY (event_id) REFERENCES wp_smi_community_events (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_sem_media FOREIGN KEY (media_id) REFERENCES wp_media_assets (id)         ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `wp_smi_community_profile.page_id` → `wp_pages.id` (unique, one profile per page) binds the congregation profile to `/smi-community.html`.
- `wp_smi_facilities.page_id`, `wp_smi_community_events.page_id`, and `wp_smi_vocation_enquiries.page_id` all → `wp_pages.id`, grouping facilities, events and enquiries under the page.
- `cover_media_id` columns and `wp_smi_event_media.media_id` → `wp_media_assets.id` reuse the shared media library for imagery.
- `wp_smi_event_media.event_id` → `wp_smi_community_events.id` provides the ordered gallery per event.
- The congregation's staff/sisters can be represented via the shared `wp_staff` table (`role_type='management'/'volunteer'`), letting sister profiles integrate without a new table here.
