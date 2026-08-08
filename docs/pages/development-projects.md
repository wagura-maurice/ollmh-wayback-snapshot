# Hospital Development (`/development-projects.html`)

> Showcases the hospital's completed and ongoing infrastructure development projects, framed by its 2009–2013 strategic plan.

## 1. Current State Mapping

- **Page title (`h1.title`):** "Hospital Development".
- **Intro / strategic context:** A lead heading "Hospital Development." followed by a paragraph explaining that, through the support of **CRS Kenya** (Catholic Relief Services), the hospital developed a **strategic plan** to give direction for the period **2009 to 2013**. The plan was built on the organization's experiences, its key achievements / lessons learnt, and the skills and competencies of the organization.
- **Project sub-sections (headings within the article body):**
  - **"Ourlady Of Lourdes Mwea Nursing School."** — presented as a development project (the nursing school building/facility).
  - **New (Modern) I.C.U facility** — captioned imagery of a "New (Modern) I.C.U Facility" and "Nurses Attending Patient In Recently Constructed I.C.U" (text is lightly garbled in the source: "Fercility", "I.C.Uew").
  - **"Enlarging Radiology Department."** — a project on expanding the radiology department.
- **Images / gallery (subjects, alt text empty in source):**
  - `ICU/ICU.JPG` — the newly constructed Intensive Care Unit facility.
  - `ICU/IcuA.JPG` — nurses attending a patient inside the recently constructed ICU.
  - `ICU/IcuB.JPG` — additional interior view of the new ICU.
  - `developmentsnachievments/radiologybld.jpg` — the radiology department building being enlarged.
- **Interactive/boilerplate elements (ignored for rebuild content):** shared header megamenu, Print/Email article actions, Prev/Next inter-page navigation, footer link columns.

**Notes on fidelity:** Image captions are laid out inline as run-together text in the archived HTML; alt attributes are empty. Subjects above are inferred from file paths and caption text. Content is thin and image-led, with no lists, tables or forms on the page.

## 2. Gap Analysis & Feature Enhancements

### Content & structure
- Break the single flat page into discrete **project records** (Nursing School, Modern ICU, Radiology Expansion) each with title, description, status, timeline, and its own gallery.
- Add **completion dates, funding partner attribution (CRS Kenya)**, and cost/capacity figures (e.g., ICU bed count, radiology equipment installed).
- Surface the underlying **2009–2013 Strategic Plan** as a downloadable document and link projects to their strategic objective.

### Media & storytelling
- Replace empty `alt` text with descriptive alt for accessibility; add real captions.
- Provide before/after image sliders and per-project photo galleries with lightbox.
- Add short impact narratives ("what this project changed for patients").

### Engagement & impact
- **Donation / "support this project" CTAs** tied to specific projects.
- **Progress/impact metrics** (beds added, patients served, milestones completed).
- Timeline / roadmap visualisation of past → present → future development.

### Technical / SEO / a11y
- Per-project meta titles/descriptions and structured data (`Project`/`MedicalOrganization`).
- Cross-link to Upcoming Projects and Self-Sustainability Projects pages.
- Responsive, lazy-loaded galleries; keyboard-accessible carousels.

## 3. Database Schema Design

```sql
-- Individual development / infrastructure projects shown on this page
CREATE TABLE development_projects (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  department_id  BIGINT UNSIGNED NULL,           -- e.g. Radiology, ICU dept
  slug           VARCHAR(191)    NOT NULL,
  title          VARCHAR(255)    NOT NULL,
  summary        VARCHAR(512)    NULL,
  description    TEXT            NULL,
  project_status ENUM('planned','ongoing','completed','on_hold') NOT NULL DEFAULT 'completed',
  start_date     DATE            NULL,
  completion_date DATE           NULL,
  cover_media_id BIGINT UNSIGNED NULL,
  sort_order     INT UNSIGNED    NOT NULL DEFAULT 0,
  status         ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  published_at   DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at     TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_devproj_slug (slug),
  KEY idx_devproj_page (page_id),
  KEY idx_devproj_status (project_status, status),
  CONSTRAINT fk_devproj_page  FOREIGN KEY (page_id)        REFERENCES pages (id)        ON DELETE CASCADE   ON UPDATE CASCADE,
  CONSTRAINT fk_devproj_dept  FOREIGN KEY (department_id)  REFERENCES departments (id)  ON DELETE SET NULL  ON UPDATE CASCADE,
  CONSTRAINT fk_devproj_cover FOREIGN KEY (cover_media_id) REFERENCES media_assets (id) ON DELETE SET NULL  ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- The strategic plan(s) that framed development (e.g. 2009-2013, CRS Kenya)
CREATE TABLE development_strategic_plans (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  title         VARCHAR(255)    NOT NULL,
  period_start  YEAR            NULL,
  period_end    YEAR            NULL,
  funding_partner VARCHAR(191)  NULL,             -- e.g. "CRS Kenya"
  description   TEXT            NULL,
  document_media_id BIGINT UNSIGNED NULL,          -- downloadable PDF
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_stratplan_page (page_id),
  CONSTRAINT fk_stratplan_page FOREIGN KEY (page_id)           REFERENCES pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_stratplan_doc  FOREIGN KEY (document_media_id) REFERENCES media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Link projects to the strategic objective(s) they fulfil
CREATE TABLE development_project_plan_links (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  project_id BIGINT UNSIGNED NOT NULL,
  plan_id    BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_projplan (project_id, plan_id),
  CONSTRAINT fk_ppl_project FOREIGN KEY (project_id) REFERENCES development_projects (id)        ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_ppl_plan    FOREIGN KEY (plan_id)    REFERENCES development_strategic_plans (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Per-project gallery images (ordered) drawn from the media library
CREATE TABLE development_project_media (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  project_id BIGINT UNSIGNED NOT NULL,
  media_id   BIGINT UNSIGNED NOT NULL,
  caption    VARCHAR(512)    NULL,
  sort_order INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_devproj_media (project_id, media_id),
  CONSTRAINT fk_dpm_project FOREIGN KEY (project_id) REFERENCES development_projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_dpm_media   FOREIGN KEY (media_id)   REFERENCES media_assets (id)         ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Optional quantified impact metrics per project (beds added, patients served...)
CREATE TABLE development_project_metrics (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  project_id   BIGINT UNSIGNED NOT NULL,
  metric_label VARCHAR(191)    NOT NULL,
  metric_value VARCHAR(100)    NOT NULL,
  unit         VARCHAR(50)     NULL,
  sort_order   INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_dpmetric_project (project_id),
  CONSTRAINT fk_dpmetric_project FOREIGN KEY (project_id) REFERENCES development_projects (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `development_projects.page_id` → `pages.id` binds every project to the `/development-projects.html` page (cascade delete with the page).
- `development_projects.department_id` → `departments.id` links projects such as ICU/Radiology to the responsible department (nullable, `SET NULL`).
- `development_projects.cover_media_id` and `development_project_media.media_id` → `media_assets.id` reuse the shared media library for cover images and galleries.
- `development_strategic_plans.page_id` → `pages.id` and `document_media_id` → `media_assets.id` store the strategic plan and its downloadable document.
- `development_project_plan_links` is the many-to-many bridge between `development_projects` and `development_strategic_plans`.
- `development_project_metrics.project_id` → `development_projects.id` attaches impact figures to each project.
