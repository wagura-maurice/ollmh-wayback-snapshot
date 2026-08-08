# Ollmh Departments (`/ollmh-departments.html`)

> A "Features" photo grid presenting the hospital's core administrative and training departments through captioned images.

## 1. Current State Mapping

- **Page title:** browser title "Ollmh Departments"; in-body `h1.title` reads **"Ollmh Departments"** (part of the "Features" menu group).
- **Structure:** a single `article-body` built as alternating caption paragraphs and rows of images — effectively a captioned department photo grid with no long-form prose.
- **Row 1 captions:** "Adminstration Block" · "Hospital C.E.O (Sr. Josephine Ndege)" with three images:
  - `MiscDept/adminB.JPG` (237×179) — administration block.
  - `MiscDept/Sr.Josephine.JPG` (336×177) — Hospital CEO, Sr. Josephine Ndege.
  - `MiscDept/DSCF7409.JPG` (249×168) — misc department view.
- **Row 2 captions:** "Hospital H.R" · "Accounting Department" with two images:
  - `MiscDept/DSCF7360.JPG` (324×178) — Human Resources.
  - `MiscDept/AcGikunju.JPG` (227×177) — Accounting department (Ac. Gikunju).
- **Row 3 captions:** "Nursing School Department" · "Nursing School Sudents" with three images:
  - `MiscDept/OLLS6.JPG` (159×182), `MiscDept/OLLS1.JPG` (241×181), `MiscDept/OLLS4.JPG` (244×183) — nursing school department and students.
- **Images have no `alt` text**; captions are loose paragraphs positioned above each image row.
- **Interactive elements:** only the shared template Print/Email actions, Prev/Next article pager, header megamenu, and footer columns. No page-specific interactivity.
- **Note:** injected foreign-language spam anchors (`megashop24.org`, `artvision.kiev.ua`) appear in the archived markup — template compromise artifacts, not real content.

## 2. Gap Analysis & Feature Enhancements

**Content & structure**
- The page conflates administrative units (Admin Block, HR, Accounting) with training units (Nursing School) and CEO portrait — split into a structured **department directory** with one card per department (name, description, location/block, head of department, contact, photo).
- Add descriptions of what each department does, opening hours, and services offered.
- Link each department to the relevant clinical service/ward pages.

**UX/UI**
- Replace fixed-pixel image rows with responsive **department cards** and a lightbox gallery per department.
- Provide filtering/search by category (Administrative, Clinical, Support, Training).
- Add an interactive campus/wayfinding map linking departments to their physical block.

**Accessibility & SEO**
- Descriptive `alt` text, figure/figcaption semantics, and per-department `MedicalOrganization`/`Photograph` schema.org markup.
- Page meta description.

**Functionality & integrations**
- Link department heads to the shared `staff` records; surface contact channels per department.
- "Contact this department" action wired to the platform's enquiry/contact system.

## 3. Database Schema Design

```sql
-- One card per department featured on the "Ollmh Departments" page.
-- Reuses the shared `departments` catalogue; this table holds the
-- page-presentation layer (ordering, featured photo, page association).
CREATE TABLE department_showcase (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  department_id  BIGINT UNSIGNED NOT NULL,
  head_staff_id  BIGINT UNSIGNED NULL,        -- e.g. CEO Sr. Josephine Ndege
  caption        VARCHAR(255)    NULL,        -- e.g. "Adminstration Block"
  summary        TEXT            NULL,
  block_location VARCHAR(191)    NULL,        -- physical block / wing
  cover_media_id BIGINT UNSIGNED NULL,
  sort_order     INT UNSIGNED    NOT NULL DEFAULT 0,
  status         ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at   DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at     TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_showcase_page_dept (page_id, department_id),
  KEY idx_showcase_page (page_id, sort_order),
  CONSTRAINT fk_showcase_page  FOREIGN KEY (page_id)        REFERENCES pages (id)         ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_showcase_dept  FOREIGN KEY (department_id)  REFERENCES departments (id)   ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_showcase_head  FOREIGN KEY (head_staff_id)  REFERENCES staff (id)         ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_showcase_cover FOREIGN KEY (cover_media_id) REFERENCES media_assets (id)  ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Additional per-department photos beyond the cover image.
CREATE TABLE department_photos (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  department_id BIGINT UNSIGNED NOT NULL,
  media_id      BIGINT UNSIGNED NOT NULL,
  caption       VARCHAR(255)    NULL,
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_dept_photo (department_id, media_id),
  KEY idx_dept_photo (department_id, sort_order),
  CONSTRAINT fk_deptphoto_dept  FOREIGN KEY (department_id) REFERENCES departments (id)  ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_deptphoto_media FOREIGN KEY (media_id)      REFERENCES media_assets (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `department_showcase.page_id → pages.id` binds the grid to the "Ollmh Departments" feature page (cascade delete).
- `department_showcase.department_id → departments.id` reuses the shared **`departments`** catalogue so the same unit is referenced consistently across service/ward pages.
- `department_showcase.head_staff_id → staff.id` links each department to its head (e.g. the CEO), reusing the shared **`staff`** table.
- `cover_media_id` and `department_photos.media_id` reference the shared **`media_assets`** library for centrally managed imagery/alt text.
