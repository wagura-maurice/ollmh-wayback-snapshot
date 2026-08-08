# Clinic Days (`/clinic-days.html`)

> Intended weekly outpatient clinic schedule page; the archived snapshot has no real content, so the schedule must be rebuilt as structured, filterable data.

## 1. Current State Mapping

- **Page title:** "Clinic Days".
- **Archive status:** This route was **not captured** in the Wayback Machine. The snapshot file is a **placeholder stub** whose entire body is:
  - An `<h1>` heading: **"Clinic Days"**.
  - A single paragraph: *"This page was not available in the Wayback Machine archive. Content will be added soon."*
  - A **"← Back to Home"** link.
- **No** genuine archived content exists — in particular, **no weekly schedule table was recovered**. Based on the page name and hospital context, this page was intended to publish a **weekly clinic timetable** (which specialist/outpatient clinics run on which days/times), typically structured as a table with columns such as *Clinic / Day / Time / Location / Clinician*.

## 2. Gap Analysis & Feature Enhancements

**Foundational content (everything is missing)**
- Build the core **weekly clinic schedule**: named clinics (e.g. antenatal, immunization, HIV/CCC, dental, eye, diabetic/hypertension) mapped to day(s), start/end times, room/location, and responsible clinician.
- Add per-clinic **descriptions** and any preparation/eligibility notes.

**Interactivity & integrations**
- **Filter/search** the timetable by clinic, day of week, or department.
- **"Today's clinics"** view and calendar (month/week) view with `.ics` export / Google Calendar add.
- **Appointment booking** linked to each clinic session.
- **Notifications/reminders** and holiday/closure overrides.

**UX/UI, accessibility & SEO**
- Responsive, accessible table (proper `<th>` scopes, caption) that reflows to cards on mobile.
- Structured `Schedule`/`MedicalClinic` data and a descriptive meta description.
- Replace the placeholder with published, indexed content.

## 3. Database Schema Design

```sql
-- A named clinic offered by the hospital (e.g. Antenatal, Immunization, CCC)
CREATE TABLE clinics (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  department_id BIGINT UNSIGNED NULL,
  name          VARCHAR(191)    NOT NULL,
  slug          VARCHAR(191)    NOT NULL,
  description   TEXT            NULL,
  location      VARCHAR(191)    NULL,               -- room / block
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at  DATETIME        NULL,
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_clinics_slug (slug),
  KEY idx_clinics_page (page_id, sort_order),
  CONSTRAINT fk_clinics_page FOREIGN KEY (page_id)       REFERENCES pages (id)       ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_clinics_dept FOREIGN KEY (department_id) REFERENCES departments (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- The weekly schedule: one row per clinic session (the timetable table)
CREATE TABLE clinic_schedules (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  clinic_id     BIGINT UNSIGNED NOT NULL,
  clinician_id  BIGINT UNSIGNED NULL,               -- staff member running the session
  day_of_week   ENUM('mon','tue','wed','thu','fri','sat','sun') NOT NULL,
  start_time    TIME            NOT NULL,
  end_time      TIME            NULL,
  location      VARCHAR(191)    NULL,               -- overrides clinic.location if set
  frequency     ENUM('weekly','biweekly','monthly') NOT NULL DEFAULT 'weekly',
  capacity      INT UNSIGNED    NULL,
  notes         VARCHAR(512)    NULL,
  is_active     TINYINT(1)      NOT NULL DEFAULT 1,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_sched_day (day_of_week, start_time),
  KEY idx_sched_clinic (clinic_id),
  CONSTRAINT fk_sched_clinic FOREIGN KEY (clinic_id)    REFERENCES clinics (id) ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_sched_staff  FOREIGN KEY (clinician_id) REFERENCES staff (id)   ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- One-off overrides: closures, holidays, or rescheduled sessions
CREATE TABLE clinic_schedule_exceptions (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  schedule_id  BIGINT UNSIGNED NOT NULL,
  exception_date DATE          NOT NULL,
  is_cancelled TINYINT(1)      NOT NULL DEFAULT 1,
  new_start_time TIME          NULL,
  new_end_time   TIME          NULL,
  reason       VARCHAR(255)    NULL,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_sched_exception (schedule_id, exception_date),
  CONSTRAINT fk_exc_sched FOREIGN KEY (schedule_id) REFERENCES clinic_schedules (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Booking requests for a specific clinic session
CREATE TABLE clinic_bookings (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  schedule_id   BIGINT UNSIGNED NOT NULL,
  booking_date  DATE            NOT NULL,
  patient_name  VARCHAR(191)    NOT NULL,
  phone         VARCHAR(40)     NOT NULL,
  email         VARCHAR(191)    NULL,
  status        ENUM('pending','confirmed','cancelled','attended','no_show') NOT NULL DEFAULT 'pending',
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_booking_sched (schedule_id, booking_date),
  KEY idx_booking_status (status),
  CONSTRAINT fk_booking_sched FOREIGN KEY (schedule_id) REFERENCES clinic_schedules (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `clinics.page_id` binds the schedule to the shared **`pages`** row for `/clinic-days.html`.
- `clinics.department_id` links each clinic to the shared **`departments`** table (e.g. outpatient/clinical), and `clinic_schedules.clinician_id` references the shared **`staff`** directory for the clinician running each session.
- `clinic_schedules` provides the row-per-session data that renders the weekly timetable table; `clinic_schedule_exceptions` and `clinic_bookings` extend it for closures and appointment booking.
- Any clinic imagery would use the shared **`media_assets`** library via the platform `page_media` join (not redefined here).
