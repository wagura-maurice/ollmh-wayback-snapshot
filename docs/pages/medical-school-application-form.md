# Medical School Application Form (`/medical-school-application-form.html`)

> Titled an "application form", the archived page is not an interactive form at all — it only offers a downloadable PDF application document.

## 1. Current State Mapping

- **Page title:** browser title "Medical School Application Form"; in-body `h1.title` reads **"Medical School Application Form"** (part of the "Nursing Sch-" menu group).
- **Actual content:** the `article-body` contains **no form fields**. It has a single call-to-action link:
  - An animated nursing GIF (`animated/graphics-nursing-315195.gif`, 63×63) plus emphasized text *"Click to Download Application Form. Now!!"*.
  - The link targets a PDF: **`Application form for OLLMMTC updated.pdf`** (OLLMMTC = OLL Medical/Nursing Training College).
- The only actual `<form>` in the page markup is the shared site **search box** (`mod-finder-searchform`) — not an application form.
- **Interactive elements:** shared template Print/Email actions, header megamenu, footer columns. No inputs, validation, file upload, or submission handling.
- **Note:** injected foreign-language spam anchors (`megashop24.org`, `artvision.kiev.ua`) appear in the archived markup — template compromise artifacts.

## 2. Gap Analysis & Feature Enhancements

**Content & functionality gaps (major)**
- Replace the download-only PDF with a real **online application form** so prospective students can apply digitally (with the PDF kept as an optional alternative).
- Capture applicant details: personal info, contact, prior education/grades (e.g. KCSE mean grade and subject grades), programme/intake choice, and supporting document uploads (certificates, ID, passport photo).
- Add server-side + client-side **validation**, required-field enforcement, and a confirmation/receipt email with a reference number.

**UX/UI**
- Multi-step wizard with progress indicator and save-and-resume.
- Inline field help, file-type/size hints, and a review step before submission.
- Clear intake deadlines and eligibility summary above the form.

**Workflow & integrations**
- Admin review dashboard: statuses (submitted → under review → shortlisted → admitted/rejected), notes, and bulk export.
- Payment integration for application fees (e.g. M-Pesa) and automated status-update emails/SMS.
- Anti-spam (CAPTCHA/Turnstile) and audit logging.

**Accessibility & SEO**
- Proper labels, `aria` attributes, keyboard navigation, and error summaries; meta description and structured data.

## 3. Database Schema Design

```sql
-- Applicant identity (can reuse across multiple applications/intakes)
CREATE TABLE wp_applicants (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  first_name    VARCHAR(100)    NOT NULL,
  last_name     VARCHAR(100)    NOT NULL,
  gender        ENUM('male','female','other','prefer_not') NULL,
  date_of_birth DATE            NULL,
  national_id   VARCHAR(40)     NULL,
  email         VARCHAR(191)    NOT NULL,
  phone         VARCHAR(40)     NULL,
  county        VARCHAR(100)    NULL,
  postal_address VARCHAR(255)   NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_applicant_email (email),
  KEY idx_applicant_name (last_name, first_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- A submitted application tied to the page and (ideally) a programme/intake
CREATE TABLE wp_applications (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  applicant_id  BIGINT UNSIGNED NOT NULL,
  programme_id  BIGINT UNSIGNED NULL,   -- -> wp_nursing_programmes.id (see about-nursing-school.md)
  intake_id     BIGINT UNSIGNED NULL,   -- -> wp_nursing_intakes.id
  reference_no  VARCHAR(40)     NOT NULL,
  kcse_mean_grade VARCHAR(4)    NULL,
  prior_school  VARCHAR(191)    NULL,
  status        ENUM('submitted','under_review','shortlisted','admitted','rejected','withdrawn') NOT NULL DEFAULT 'submitted',
  reviewed_by   BIGINT UNSIGNED NULL,   -- CMS user
  review_notes  TEXT            NULL,
  submitted_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_application_ref (reference_no),
  KEY idx_application_status (status),
  CONSTRAINT fk_app_page      FOREIGN KEY (page_id)      REFERENCES wp_pages (id)              ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_app_applicant FOREIGN KEY (applicant_id) REFERENCES wp_applicants (id)         ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_app_programme FOREIGN KEY (programme_id) REFERENCES wp_nursing_programmes (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_app_intake    FOREIGN KEY (intake_id)    REFERENCES wp_nursing_intakes (id)    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_app_reviewer  FOREIGN KEY (reviewed_by)  REFERENCES wp_users (id)              ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Uploaded supporting documents (certificates, ID, photo) per application
CREATE TABLE wp_application_documents (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  application_id BIGINT UNSIGNED NOT NULL,
  media_id       BIGINT UNSIGNED NOT NULL,
  doc_type       ENUM('kcse_certificate','national_id','passport_photo','transcript','other') NOT NULL DEFAULT 'other',
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_appdoc_app (application_id),
  CONSTRAINT fk_appdoc_app   FOREIGN KEY (application_id) REFERENCES wp_applications (id)  ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_appdoc_media FOREIGN KEY (media_id)       REFERENCES wp_media_assets (id)  ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Downloadable PDF form(s) still offered as an alternative
CREATE TABLE wp_application_form_downloads (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id      BIGINT UNSIGNED NOT NULL,
  media_id     BIGINT UNSIGNED NOT NULL,   -- the PDF in media_assets
  label        VARCHAR(191)    NOT NULL,   -- e.g. "OLLMMTC Application Form (PDF)"
  is_current   TINYINT(1)      NOT NULL DEFAULT 1,
  download_count BIGINT UNSIGNED NOT NULL DEFAULT 0,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_formdl_page (page_id),
  CONSTRAINT fk_formdl_page  FOREIGN KEY (page_id)  REFERENCES wp_pages (id)        ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_formdl_media FOREIGN KEY (media_id) REFERENCES wp_media_assets (id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Extended tables (workflow, payments, review, notifications)

These turn the form into a full admissions pipeline: an auditable status
trail, referees, structured reviewer scoring, application-fee payments
(e.g. M-Pesa), and an outbound notification log.

```sql
-- Audit trail of every status transition on an application
CREATE TABLE wp_application_status_history (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  application_id BIGINT UNSIGNED NOT NULL,
  from_status    ENUM('submitted','under_review','shortlisted','admitted','rejected','withdrawn') NULL,
  to_status      ENUM('submitted','under_review','shortlisted','admitted','rejected','withdrawn') NOT NULL,
  changed_by     BIGINT UNSIGNED NULL,   -- CMS user; NULL = system/applicant
  note           VARCHAR(512)    NULL,
  changed_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_ash_app (application_id, changed_at),
  CONSTRAINT fk_ash_app  FOREIGN KEY (application_id) REFERENCES wp_applications (id) ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_ash_user FOREIGN KEY (changed_by)     REFERENCES wp_users (id)        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Referees / character references supplied with an application
CREATE TABLE wp_application_referees (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  application_id BIGINT UNSIGNED NOT NULL,
  full_name      VARCHAR(191)    NOT NULL,
  relationship   VARCHAR(100)    NULL,
  email          VARCHAR(191)    NULL,
  phone          VARCHAR(40)     NULL,
  PRIMARY KEY (id),
  KEY idx_referee_app (application_id),
  CONSTRAINT fk_referee_app FOREIGN KEY (application_id) REFERENCES wp_applications (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Structured reviewer scoring (many reviewers per application)
CREATE TABLE wp_application_reviews (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  application_id BIGINT UNSIGNED NOT NULL,
  reviewer_id    BIGINT UNSIGNED NOT NULL,   -- CMS user
  score          DECIMAL(5,2)    NULL,
  recommendation ENUM('admit','waitlist','reject','undecided') NOT NULL DEFAULT 'undecided',
  comments       TEXT            NULL,
  reviewed_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_review_app_reviewer (application_id, reviewer_id),
  CONSTRAINT fk_review_app  FOREIGN KEY (application_id) REFERENCES wp_applications (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_review_user FOREIGN KEY (reviewer_id)    REFERENCES wp_users (id)        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Application-fee payments (e.g. M-Pesa / card / bank)
CREATE TABLE wp_application_payments (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  application_id BIGINT UNSIGNED NOT NULL,
  amount         DECIMAL(12,2)   NOT NULL,
  currency       CHAR(3)         NOT NULL DEFAULT 'KES',
  method         ENUM('mpesa','card','bank_transfer','cash','waiver') NOT NULL,
  provider_ref   VARCHAR(100)    NULL,        -- gateway / M-Pesa transaction id
  status         ENUM('pending','paid','failed','refunded') NOT NULL DEFAULT 'pending',
  paid_at        DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_payment_ref (provider_ref),
  KEY idx_payment_app (application_id, status),
  CONSTRAINT fk_payment_app FOREIGN KEY (application_id) REFERENCES wp_applications (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Outbound notifications (email/SMS) sent to applicants
CREATE TABLE wp_application_notifications (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  application_id BIGINT UNSIGNED NOT NULL,
  channel        ENUM('email','sms') NOT NULL,
  template_key   VARCHAR(100)    NOT NULL,    -- e.g. "submission_received"
  recipient      VARCHAR(191)    NOT NULL,
  status         ENUM('queued','sent','failed') NOT NULL DEFAULT 'queued',
  sent_at        DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_notif_app (application_id, status),
  CONSTRAINT fk_notif_app FOREIGN KEY (application_id) REFERENCES wp_applications (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `wp_applications.page_id → wp_pages.id` ties every submission to this page; `applicant_id → wp_applicants.id` separates reusable identity from a specific application.
- `programme_id → wp_nursing_programmes.id` and `intake_id → wp_nursing_intakes.id` integrate with the School of Nursing schema in [`about-nursing-school.md`](./about-nursing-school.md).
- `reviewed_by → wp_users.id` reuses the shared CMS **`wp_users`** table for the admin review workflow.
- `wp_application_documents.media_id` and `wp_application_form_downloads.media_id` reference the shared **`wp_media_assets`** library (uploaded docs and the downloadable PDF alike), so files are centrally stored and access-controlled.
- `wp_application_status_history`, `wp_application_referees`, `wp_application_reviews`, `wp_application_payments`, and `wp_application_notifications` all hang off `wp_applications.id` (cascade delete), giving a complete, auditable admissions pipeline.
- `wp_application_status_history.changed_by` and `wp_application_reviews.reviewer_id` reference the shared **`wp_users`** table; `wp_application_reviews` is unique per (application, reviewer) so each panelist scores once.
