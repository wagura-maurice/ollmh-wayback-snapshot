# Community Support (`/community-support.html`)

> Describes the hospital's community outreach initiatives — mobile medical teams, health education, volunteers, and the jiggers-elimination project.

## 1. Current State Mapping

- **Page title (`h1.title`):** "Community Support".
- **Outreach intro:** A paragraph explaining that, for the benefit of citizens' health, the hospital took the initiative to approach the community by setting up a **"medical service team" for citizens who cannot easily access hospital facilities**. The team goes into the community, works wherever required, and educates people on **preventive health care, including HIV issues.**
- **Health education paragraph:** States that the hospital cares not only about medical quality and service but also hopes to contribute to the health and well-being of mankind in the future, continuously demanding of itself the elevation of medical care quality and devotion to **medical education.**
- **Featured programs / captioned imagery (grouped inline):**
  - **OLLMH nurse giving a health talk** (community health education).
  - **OLLMH Health Volunteers** (community health volunteers, CHVs).
  - **Session with orphans / vulnerable children** — a training held in 2010.
  - **Administration chiefs and sub-chiefs of Mwea** at OLLMH during a resource-mobilization session.
- **Jiggers elimination project:** A paragraph stating that Our Lady of Lourdes Mwea Hospital recently launched a **jiggers elimination project** in its community; based on the findings, the hospital devised a serious strategy to participate in **eradication of poverty**, targeting mostly vulnerable citizens.
- **Images / gallery (subjects inferred from paths; alt empty):**
  - `CommunityProject/Faith giving health talk - Copy.JPG` — nurse "Faith" delivering a health talk.
  - `CommunityProject/COMMUNITY HEALTH VOLUNTEERS.JPG` — community health volunteers.
  - `CommunityProject/ORPHANS AND VENERABLE CHILDREN DURING ONE OF THE TRAININGS HELD IN 2010.JPG` — orphans and vulnerable children training (2010).
  - `CommunityProject/A TEAM OF LOCAL ADMINISTRATION CHIEFS AND SUB CHIEFS OF MWEA...RESOURCE MOBILIZAT.JPG` — local chiefs at a resource-mobilization session.
  - `CommunityProject/JiggersProject/DSC07763.JPG`, `DSC07766.JPG`, `DSC07771.JPG` — jiggers elimination project activities.
- **Interactive/boilerplate elements (ignored):** header megamenu, Print/Email actions, Prev/Next navigation, footer columns.

**Notes on fidelity:** The page is prose + captioned photos describing several distinct outreach programs; no lists, tables or forms are present and `alt` attributes are empty.

## 2. Gap Analysis & Feature Enhancements

### Content & structure
- Split into distinct **outreach program records** (Mobile Medical Service Team, Health Education, Community Health Volunteers, OVC support, Jiggers Elimination) each with description, target group, partners, and gallery.
- Add **dates, locations, and outcomes** (e.g., number of people reached, jiggers cases treated, 2010 OVC training figures).

### Media & storytelling
- Descriptive `alt`/captions; program-specific photo galleries and testimonials/beneficiary stories.
- A map of outreach catchment areas across Mwea.

### Engagement & impact
- **Volunteer sign-up / CHV recruitment form** and event calendar for outreach visits.
- **Donation / sponsorship CTAs** targeted at the jiggers and OVC programs.
- **Impact metrics** (people reached, villages visited, cases treated) and partner acknowledgements (chiefs, local administration).

### Technical / SEO / a11y
- Structured data (`GovernmentService`/`MedicalOrganization`), meta descriptions, alt text.
- Cross-link to Development, Self-Sustainability and SMI Community pages.

## 3. Database Schema Design

```sql
-- Distinct community outreach programs described on this page
CREATE TABLE wp_community_programs (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  department_id  BIGINT UNSIGNED NULL,          -- e.g. community/outpatient dept
  slug           VARCHAR(191)    NOT NULL,
  title          VARCHAR(255)    NOT NULL,
  program_type   ENUM('mobile_clinic','health_education','volunteers','ovc_support','disease_elimination','other') NOT NULL DEFAULT 'other',
  summary        VARCHAR(512)    NULL,
  description    TEXT            NULL,
  target_group   VARCHAR(255)    NULL,          -- e.g. "orphans & vulnerable children"
  launched_on    DATE            NULL,
  cover_media_id BIGINT UNSIGNED NULL,
  sort_order     INT UNSIGNED    NOT NULL DEFAULT 0,
  status         ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  published_at   DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at     TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_commprog_slug (slug),
  KEY idx_commprog_page (page_id),
  KEY idx_commprog_type (program_type),
  CONSTRAINT fk_commprog_page  FOREIGN KEY (page_id)        REFERENCES wp_pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_commprog_dept  FOREIGN KEY (department_id)  REFERENCES wp_departments (id)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_commprog_cover FOREIGN KEY (cover_media_id) REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Outreach events / visits associated with a program (dates, locations, reach)
CREATE TABLE wp_community_outreach_events (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  program_id   BIGINT UNSIGNED NOT NULL,
  title        VARCHAR(255)    NOT NULL,
  event_date   DATE            NULL,
  location     VARCHAR(255)    NULL,
  people_reached INT UNSIGNED  NULL,
  description  TEXT            NULL,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_commevent_program (program_id),
  CONSTRAINT fk_commevent_program FOREIGN KEY (program_id) REFERENCES wp_community_programs (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volunteer sign-ups (CHV recruitment) captured from this page
CREATE TABLE wp_community_volunteer_signups (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  program_id   BIGINT UNSIGNED NULL,
  full_name    VARCHAR(191)    NOT NULL,
  email        VARCHAR(191)    NULL,
  phone        VARCHAR(40)     NULL,
  message      TEXT            NULL,
  signup_status ENUM('new','contacted','approved','declined') NOT NULL DEFAULT 'new',
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_commvol_program (program_id),
  CONSTRAINT fk_commvol_program FOREIGN KEY (program_id) REFERENCES wp_community_programs (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Per-program gallery images from the shared media library
CREATE TABLE wp_community_program_media (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  program_id BIGINT UNSIGNED NOT NULL,
  media_id   BIGINT UNSIGNED NOT NULL,
  caption    VARCHAR(512)    NULL,
  sort_order INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_commprog_media (program_id, media_id),
  CONSTRAINT fk_cpm_program FOREIGN KEY (program_id) REFERENCES wp_community_programs (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_cpm_media   FOREIGN KEY (media_id)   REFERENCES wp_media_assets (id)       ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `wp_community_programs.page_id` → `wp_pages.id` binds each outreach program to the `/community-support.html` page.
- `wp_community_programs.department_id` → `wp_departments.id` associates programs with a community/outpatient department (nullable, `SET NULL`).
- `wp_community_programs.cover_media_id` and `wp_community_program_media.media_id` → `wp_media_assets.id` reuse the shared media library.
- `wp_community_outreach_events.program_id` → `wp_community_programs.id` logs individual visits and their reach metrics.
- `wp_community_volunteer_signups.program_id` → `wp_community_programs.id` captures volunteer applications (kept even if a program is removed, via `SET NULL`).
