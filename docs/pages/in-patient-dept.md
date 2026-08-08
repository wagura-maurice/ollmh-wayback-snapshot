# In Patient Dept (`/in-patient-dept.html`)

> Intended landing page for the hospital's Inpatient Department; the archived snapshot contains no real content and must be rebuilt from scratch.

## 1. Current State Mapping

- **Page title:** "In Patient Dept".
- **Archive status:** This route was **not captured** in the Wayback Machine. The snapshot file is a **placeholder stub** whose entire body is:
  - An `<h1>` heading: **"In Patient Dept"**.
  - A single paragraph: *"This page was not available in the Wayback Machine archive. Content will be added soon."*
  - A **"← Back to Home"** link.
- **No** genuine archived headings, paragraphs, images, galleries, lists, tables, or interactive elements exist for this page.
- **Related content note:** Actual inpatient/nursing narrative content was archived under the sibling **Special Medical Services** page (heading "Inpatient Department (Nursing Application)") and the **Wards** page; those can inform the rebuild of this page. See `special-medical-services.md` and `wards.md`.

## 2. Gap Analysis & Feature Enhancements

**Foundational content (everything is missing)**
- Author a full **Inpatient Department overview**: purpose, admission criteria, and scope of inpatient care.
- Link to the constituent **wards** (Maternity, Male, Children) documented on the Wards page.
- Describe the **admission → treatment → discharge** patient journey.
- Add **inpatient facilities & equipment**, care philosophy, and visiting hours.

**Interactivity & integrations**
- **Admission enquiry / pre-admission form**.
- **Bed availability** overview aggregated across inpatient wards.
- **Billing/insurance (NHIF and private)** information and cost estimates.
- Cross-links to Wards, Special Medical Services, and Out Patient Department.

**UX/UI, accessibility & SEO**
- Build a structured page with hero, service cards, and captioned galleries (with alt text).
- Unique meta title/description and `Hospital`/`MedicalDepartment` structured data.
- Ensure the placeholder is replaced with published, indexed content.

## 3. Database Schema Design

```sql
-- Inpatient department profile / feature blocks for the page
CREATE TABLE inpatient_dept_sections (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  department_id BIGINT UNSIGNED NULL,
  heading       VARCHAR(191)    NOT NULL,
  body          TEXT            NULL,
  section_type  ENUM('overview','admission','care','facilities','visiting','other') NOT NULL DEFAULT 'overview',
  hero_media_id BIGINT UNSIGNED NULL,
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  KEY idx_ipd_page (page_id, sort_order),
  CONSTRAINT fk_ipd_page  FOREIGN KEY (page_id)       REFERENCES pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_ipd_dept  FOREIGN KEY (department_id) REFERENCES departments (id)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_ipd_media FOREIGN KEY (hero_media_id) REFERENCES media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Pre-admission / admission enquiry submissions
CREATE TABLE inpatient_admission_enquiries (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  department_id  BIGINT UNSIGNED NULL,
  patient_name   VARCHAR(191)    NOT NULL,
  phone          VARCHAR(40)     NOT NULL,
  email          VARCHAR(191)    NULL,
  preferred_ward VARCHAR(191)    NULL,
  message        TEXT            NULL,
  status         ENUM('new','contacted','admitted','declined','closed') NOT NULL DEFAULT 'new',
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_ipd_enq_status (status, created_at),
  CONSTRAINT fk_ipd_enq_dept FOREIGN KEY (department_id) REFERENCES departments (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `inpatient_dept_sections.page_id` ties the rebuilt content to the shared **`pages`** row for `/in-patient-dept.html`.
- `department_id` on both tables links to the shared **`departments`** table (inpatient category), and section hero imagery references the shared **`media_assets`** library (with galleries via the platform `page_media` join).
- Admission enquiries feed the CMS workflow managed by shared **`users`**; wards themselves live in the Wards page schema (`wards` table) and can join here via `departments`.
