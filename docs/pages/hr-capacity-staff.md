# HR-Capacity (Staff) (`/hr-capacity-staff.html`)

> Summarizes the hospital's human-resource capacity — the range of professional and support staff distributed across its departments.

## 1. Current State Mapping

**Page title:** "HR-Capacity (Staff)" (from `<h1 class="title">`).

**Page actions:** Joomla "Print" and "Email" icons (boilerplate).

**Textual content (faithful summary):**

- **Heading:** "HR CAPACITY" (bold lead-in).
- **Capacity paragraph:** The hospital maintains a good number of **professionals and support staff** distributed across its various departments. Key personnel listed (in prose) are **consultants** — i.e. **Surgeon, Physician, Paediatrician** — plus **doctors, nurses, clinical officers, laboratory technologists, pharmacy technologists, radiographers, and an ophthalmologist**, "etc."

**Images (3 inline photos, empty `alt`):**
- A miscellaneous select photo (`misc_Select/DSCF7461.JPG`).
- A developments/achievements photo (`developmentsnachievments/DSC00463.JPG`).
- A miscellaneous select photo (`misc_Select/DSCF7468.JPG`).

**Interactive elements:** None beyond Print/Email actions. No tables, structured staff counts, or forms — cadre types appear only in a single sentence.

## 2. Gap Analysis & Feature Enhancements

**Content Gaps**
- No **numbers** despite the page being titled "HR Capacity" — e.g. head-count per cadre, staff-to-patient ratios, department distribution.
- Cadres are listed in prose ending in "etc." — should be an explicit, complete, categorized list.
- No careers/recruitment content, even though HR is the topic.

**UX/UI**
- Replace prose with a **staff-capacity table or chart** (cadre → count per department).
- Add a **cadre directory grid** with icons and short role descriptions.
- Caption/alt the three photos so the depicted teams/facilities are identifiable.

**Functionality**
- A **Careers / Vacancies** module (job postings + online application form), highly relevant to an HR page.
- Filterable staff/cadre listing sourced from the shared `staff` and `departments` tables.
- Optional dashboard of aggregate capacity stats that updates as staff records change.

**Trust/Accessibility**
- Present capacity data with accessible table markup and figure captions.
- `Occupation`/`JobPosting` structured data for any vacancies; SEO around "careers at OLLMH".

## 3. Database Schema Design

```sql
-- Staff cadres / professional categories described on the HR page
CREATE TABLE staff_cadres (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id      BIGINT UNSIGNED NOT NULL,
  name         VARCHAR(191)    NOT NULL,        -- "Surgeon", "Nurse", "Radiographer"
  slug         VARCHAR(191)    NOT NULL,
  category     ENUM('consultant','medical','nursing','clinical','allied_health','support','administrative') NOT NULL DEFAULT 'clinical',
  description  TEXT            NULL,
  sort_order   INT UNSIGNED    NOT NULL DEFAULT 0,
  is_active    TINYINT(1)      NOT NULL DEFAULT 1,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_cadre_slug (slug),
  KEY idx_cadre_page (page_id, sort_order),
  CONSTRAINT fk_cadre_page FOREIGN KEY (page_id)
    REFERENCES pages (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Head-count capacity per cadre, optionally broken down by department
CREATE TABLE hr_capacity_stats (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  cadre_id      BIGINT UNSIGNED NOT NULL,
  department_id BIGINT UNSIGNED NULL,
  head_count    INT UNSIGNED    NOT NULL DEFAULT 0,
  notes         VARCHAR(255)    NULL,
  as_of_date    DATE            NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_capacity (cadre_id, department_id, as_of_date),
  KEY idx_capacity_page (page_id),
  CONSTRAINT fk_capacity_page  FOREIGN KEY (page_id)       REFERENCES pages (id)        ON DELETE CASCADE   ON UPDATE CASCADE,
  CONSTRAINT fk_capacity_cadre FOREIGN KEY (cadre_id)      REFERENCES staff_cadres (id) ON DELETE CASCADE   ON UPDATE CASCADE,
  CONSTRAINT fk_capacity_dept  FOREIGN KEY (department_id) REFERENCES departments (id)  ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Career / vacancy postings (HR-relevant enhancement)
CREATE TABLE job_vacancies (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  cadre_id      BIGINT UNSIGNED NULL,
  department_id BIGINT UNSIGNED NULL,
  title         VARCHAR(191)    NOT NULL,
  slug          VARCHAR(191)    NOT NULL,
  summary       TEXT            NULL,
  employment_type ENUM('full_time','part_time','contract','locum','internship','volunteer') NOT NULL DEFAULT 'full_time',
  closing_date  DATE            NULL,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_vacancy_slug (slug),
  KEY idx_vacancy_page (page_id, status),
  CONSTRAINT fk_vacancy_page  FOREIGN KEY (page_id)       REFERENCES pages (id)        ON DELETE CASCADE   ON UPDATE CASCADE,
  CONSTRAINT fk_vacancy_cadre FOREIGN KEY (cadre_id)      REFERENCES staff_cadres (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_vacancy_dept  FOREIGN KEY (department_id) REFERENCES departments (id)  ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `staff_cadres.page_id`, `hr_capacity_stats.page_id`, and `job_vacancies.page_id` reference `pages(id)` for the HR page (`slug = hr-capacity-staff`).
- `hr_capacity_stats.department_id` and `job_vacancies.department_id` reference the shared `departments(id)`, letting capacity be reported and vacancies posted per department.
- The shared `staff` table holds individual employees; `staff_cadres` classifies them by profession and `hr_capacity_stats` aggregates counts (a reporting layer over `staff`/`departments`).
- Page photos live in `media_assets` and attach via the shared `page_media` join table (role `gallery`).
