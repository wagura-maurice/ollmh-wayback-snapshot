# Out Patient Department (`/out-patient-dept.html`)

> Describes the hospital's Outpatient Department (OPD), its location, 24-hour operations, equipment, and patient-flow facilities.

## 1. Current State Mapping

- **Page title:** browser title is "Out Patient Dept"; the in-body heading reads **"Out Patient"**.
- **Intro paragraph:** Explains that the OPD is situated at the **main entrance of the hospital**, which facilitates faster attendance of critically ill patients — especially those from accident scenes. Nurses are on hand to receive critically ill patients, who can be wheeled freely to other crucial departments (laboratory, X-ray, etc.) by qualified nurses.
- **Facilities/equipment paragraph:** States the OPD is well equipped with **medical couches, wheelchairs, and stretchers** so patients reach the point of service quickly. Key operational facts stated:
  - The OPD **operates twenty-four hours a day**.
  - The **waiting area can accommodate more than 25 patients**.
  - There are **three consultation rooms** and a **minor theatre** in the OPD.
  - A **TV is installed** in the waiting area for the comfort of clients awaiting a clinician.
- **Images (gallery, no alt text in source):**
  - `outp2.jpg` — Outpatient department scene.
  - `DSCF7421.JPG` — Outpatient department / patient-care photo.
- **Interactive elements:** Only the shared template's Prev/Next article links and the standard header megamenu / footer link columns (About OLLMH, Community Care, Core Values, etc.). No page-specific interactivity.
- **Note:** The archived markup contains injected spam link fragments (Russian anchor text, "megashop24"/"joomla framework" boilerplate) from the compromised Joomla template — these are **not** genuine page content and are excluded from the rebuild.

## 2. Gap Analysis & Feature Enhancements

**Content & information**
- Add explicit **OPD operating details** as structured data: opening hours (currently only "24 hours" in prose), triage process, and typical patient journey (reception → triage → consultation → lab/X-ray → pharmacy).
- List the **services offered at OPD** (consultations, minor procedures/minor theatre, dressings, injections) as discrete items.
- Add **average waiting time / current queue status** and fee/consultation cost guidance.

**Interactivity & integrations**
- **Online appointment / callback booking** for OPD consultations, tied to available consultation rooms and clinicians.
- **Live queue / token number display** and estimated wait time.
- Click-to-call and map/directions widget for the "main entrance" location.

**UX/UI**
- Replace the raw image pair with a captioned, responsive **gallery/lightbox** with meaningful alt text.
- Add an **icon feature grid** for facilities (3 consultation rooms, minor theatre, 25+ waiting capacity, wheelchairs/stretchers, TV).

**Accessibility & SEO**
- Provide descriptive `alt` text for every image (currently empty).
- Add structured metadata (`MedicalClinic` / `Hospital` schema.org) and a concise meta description.
- Ensure headings follow a logical hierarchy (single H1, sectioned H2s).

## 3. Database Schema Design

```sql
-- Facilities/equipment highlights shown on the OPD page (icon feature grid)
CREATE TABLE wp_opd_facilities (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  department_id BIGINT UNSIGNED NULL,
  name          VARCHAR(191)    NOT NULL,          -- e.g. "Minor Theatre"
  description   VARCHAR(512)    NULL,
  quantity      INT UNSIGNED    NULL,              -- e.g. 3 consultation rooms
  icon          VARCHAR(100)    NULL,
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  KEY idx_opd_fac_page (page_id, sort_order),
  CONSTRAINT fk_opd_fac_page FOREIGN KEY (page_id)       REFERENCES wp_pages (id)       ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_opd_fac_dept FOREIGN KEY (department_id) REFERENCES wp_departments (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- OPD operating hours (supports the "24 hours a day" statement, per weekday if needed)
CREATE TABLE wp_opd_operating_hours (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  department_id BIGINT UNSIGNED NOT NULL,
  day_of_week   ENUM('mon','tue','wed','thu','fri','sat','sun','all') NOT NULL DEFAULT 'all',
  is_24_hours   TINYINT(1)      NOT NULL DEFAULT 1,
  opens_at      TIME            NULL,
  closes_at     TIME            NULL,
  notes         VARCHAR(255)    NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_opd_hours (department_id, day_of_week),
  CONSTRAINT fk_opd_hours_dept FOREIGN KEY (department_id) REFERENCES wp_departments (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Consultation rooms / minor theatre resources used for appointment scheduling
CREATE TABLE wp_opd_consultation_rooms (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  department_id BIGINT UNSIGNED NOT NULL,
  room_label    VARCHAR(100)    NOT NULL,          -- e.g. "Consultation Room 1", "Minor Theatre"
  room_type     ENUM('consultation','minor_theatre','triage','other') NOT NULL DEFAULT 'consultation',
  is_active     TINYINT(1)      NOT NULL DEFAULT 1,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_opd_room (department_id, room_label),
  CONSTRAINT fk_opd_room_dept FOREIGN KEY (department_id) REFERENCES wp_departments (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Online OPD appointment requests
CREATE TABLE wp_opd_appointments (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  department_id  BIGINT UNSIGNED NOT NULL,
  room_id        BIGINT UNSIGNED NULL,
  clinician_id   BIGINT UNSIGNED NULL,             -- staff member
  patient_name   VARCHAR(191)    NOT NULL,
  patient_phone  VARCHAR(40)     NOT NULL,
  patient_email  VARCHAR(191)    NULL,
  requested_at   DATETIME        NOT NULL,
  reason         VARCHAR(512)    NULL,
  status         ENUM('pending','confirmed','cancelled','completed','no_show') NOT NULL DEFAULT 'pending',
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_opd_appt_dept (department_id, requested_at),
  KEY idx_opd_appt_status (status),
  CONSTRAINT fk_opd_appt_dept  FOREIGN KEY (department_id) REFERENCES wp_departments (id)          ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_opd_appt_room  FOREIGN KEY (room_id)       REFERENCES wp_opd_consultation_rooms (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_opd_appt_staff FOREIGN KEY (clinician_id)  REFERENCES wp_staff (id)                ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `wp_opd_facilities.page_id`, `wp_opd_appointments` (indirectly via department) and all page-facing rows tie back to the **`wp_pages`** row for the OPD route.
- Every table links to **`wp_departments`** so the OPD's clinical data is anchored to the shared Outpatient department record.
- `wp_opd_appointments.clinician_id` references **`wp_staff`**, reusing the shared clinician directory.
- Facility/room imagery is served through the shared **`wp_media_assets`** + **`wp_page_media`** gallery join (no redefinition needed here).
