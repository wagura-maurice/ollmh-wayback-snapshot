# Upcoming Projects (`/upcoming-projects.html`)

> Announces the hospital's newest and forthcoming facilities — most notably the CT-Scan diagnostic centre and the nursing school tuition block.

## 1. Current State Mapping

- **Page title (`h1.title`):** "Upcoming Projects".
- **CT-SCAN section:** Heading "CT-SCAN" with a paragraph stating the **CT-Scan unit has already been finished and launched**, and the hospital now has a **fully equipped S.M.I Diagnostic Centre with a 16-slice Sensation CT Scan.** The text includes a "SEE" pointer linking to the **DIAGNOSTIC CENTRE** article (internal Joomla article link).
- **Nursing School Tuition Block section:** Heading "Nursing school Tuition block" with a paragraph stating the **building has undergone completion of its first phase, which is now operational**, and that the remaining part will be finished as soon as possible.
- **Links present in the body:**
  - "DIAGNOSTIC CENTRE" → internal Joomla content article (id 75) describing the diagnostic centre.
  - Standard Print / Email article actions (boilerplate).
- **Images / gallery:** No content images were embedded in the article body of this page (text-only, aside from shared theme/boilerplate imagery).
- **Interactive/boilerplate elements (ignored):** header megamenu, Print/Email actions, Prev (Self-Sustainability) / Next (Community Support) navigation, footer columns.

**Notes on fidelity:** Despite the "Upcoming" title, both listed items are described as substantially complete/operational (CT-Scan launched; tuition block phase 1 operational), so the page mixes recently completed and in-progress works. No lists, tables or forms are present.

## 2. Gap Analysis & Feature Enhancements

### Content & structure
- Model each item as an **upcoming/ongoing project** with a clear **status** (planned / in progress / phase complete / launched) and **phase tracking** (the tuition block explicitly has phases).
- Add **target completion dates, budget, funding needs**, and equipment specs (e.g., "16-slice Siemens Sensation CT").
- Convert the inline "SEE DIAGNOSTIC CENTRE" reference into a proper linked related-page relationship.

### Media & storytelling
- Add construction-progress galleries and renderings; descriptive alt/captions.
- Provide a **roadmap / timeline** view distinguishing planned vs. completed phases.

### Engagement & impact
- **"Fund this project" / donation CTAs** with progress bars toward a funding goal.
- **Progress percentage indicators** per phase and email-update subscription.
- Announcement/news integration so launches surface as news items.

### Technical / SEO / a11y
- Structured data (`Project`), meta descriptions, accessible progress components.
- Cross-links to Development Projects and the Diagnostic Centre / Special Medical Services pages.

## 3. Database Schema Design

```sql
-- Upcoming / in-progress projects announced on this page
CREATE TABLE upcoming_projects (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  department_id  BIGINT UNSIGNED NULL,          -- e.g. Diagnostic/Radiology, Nursing School
  related_page_id BIGINT UNSIGNED NULL,         -- e.g. Diagnostic Centre detail page
  slug           VARCHAR(191)    NOT NULL,
  title          VARCHAR(255)    NOT NULL,
  summary        VARCHAR(512)    NULL,
  description    TEXT            NULL,
  project_status ENUM('planned','in_progress','phase_complete','launched','on_hold') NOT NULL DEFAULT 'planned',
  target_date    DATE            NULL,
  budget_amount  DECIMAL(14,2)   NULL,
  funding_goal   DECIMAL(14,2)   NULL,
  funds_raised   DECIMAL(14,2)   NOT NULL DEFAULT 0.00,
  progress_pct   TINYINT UNSIGNED NOT NULL DEFAULT 0,   -- 0-100
  cover_media_id BIGINT UNSIGNED NULL,
  sort_order     INT UNSIGNED    NOT NULL DEFAULT 0,
  status         ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  published_at   DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at     TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_upproj_slug (slug),
  KEY idx_upproj_page (page_id),
  KEY idx_upproj_status (project_status, status),
  CONSTRAINT fk_upproj_page    FOREIGN KEY (page_id)         REFERENCES pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_upproj_dept    FOREIGN KEY (department_id)   REFERENCES departments (id)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_upproj_related FOREIGN KEY (related_page_id) REFERENCES pages (id)        ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_upproj_cover   FOREIGN KEY (cover_media_id)  REFERENCES media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Construction phases / milestones (the tuition block has phase 1 complete)
CREATE TABLE upcoming_project_phases (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  project_id   BIGINT UNSIGNED NOT NULL,
  phase_no     INT UNSIGNED    NOT NULL DEFAULT 1,
  title        VARCHAR(255)    NOT NULL,
  phase_status ENUM('planned','in_progress','complete') NOT NULL DEFAULT 'planned',
  description  TEXT            NULL,
  completed_on DATE            NULL,
  sort_order   INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_upphase (project_id, phase_no),
  CONSTRAINT fk_upphase_project FOREIGN KEY (project_id) REFERENCES upcoming_projects (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Progress-gallery images per project from the shared media library
CREATE TABLE upcoming_project_media (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  project_id BIGINT UNSIGNED NOT NULL,
  media_id   BIGINT UNSIGNED NOT NULL,
  caption    VARCHAR(512)    NULL,
  sort_order INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_upproj_media (project_id, media_id),
  CONSTRAINT fk_upm_project FOREIGN KEY (project_id) REFERENCES upcoming_projects (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_upm_media   FOREIGN KEY (media_id)   REFERENCES media_assets (id)      ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Optional donation pledges toward an upcoming project's funding goal
CREATE TABLE upcoming_project_pledges (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  project_id   BIGINT UNSIGNED NOT NULL,
  donor_name   VARCHAR(191)    NULL,
  donor_email  VARCHAR(191)    NULL,
  amount       DECIMAL(14,2)   NOT NULL,
  currency     CHAR(3)         NOT NULL DEFAULT 'KES',
  pledge_status ENUM('pledged','received','cancelled') NOT NULL DEFAULT 'pledged',
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_uppledge_project (project_id),
  CONSTRAINT fk_uppledge_project FOREIGN KEY (project_id) REFERENCES upcoming_projects (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `upcoming_projects.page_id` → `pages.id` binds each project to the `/upcoming-projects.html` page.
- `upcoming_projects.department_id` → `departments.id` links a project to its owning department (e.g., Diagnostic Centre, Nursing School).
- `upcoming_projects.related_page_id` → `pages.id` models the inline "SEE DIAGNOSTIC CENTRE" cross-reference to a detail page.
- `upcoming_projects.cover_media_id` and `upcoming_project_media.media_id` → `media_assets.id` reuse the shared media library.
- `upcoming_project_phases.project_id` → `upcoming_projects.id` tracks phased delivery (e.g., tuition block phase 1 complete).
- `upcoming_project_pledges.project_id` → `upcoming_projects.id` records donations toward funding goals.
