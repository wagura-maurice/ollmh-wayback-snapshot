# Special Medical Services (`/special-medical-services.html`)

> Presents the hospital's inpatient / nursing care philosophy and its commitment to advanced medical instruments for comprehensive, fast treatment.

## 1. Current State Mapping

- **Page title:** browser title is "Special Medical Services". Note a **content discrepancy in the archive**: the in-body heading actually reads **"Inpatient Department (Nursing Application)"** — the archived Special Medical Services route was populated with inpatient/nursing content.
- **Mission/values paragraph:** States the hospital offers **"Excellent, Affordable, Accessible health care to our patients and community at large."** It attributes their motivation to **the love of Christ to the needy**, accomplished through **commitment, devotion, talents and measure of grace, with minimal supervision** — a faith-based, values-driven statement.
- **Clinical care caption:** **"Doctors carrying out routine check-ups to patients."**
- **Equipment/investment paragraph:** States that to achieve **the most comprehensive and fast treatment results**, a large portion of resources goes into **purchasing the most advanced medical instruments and systems**.
- **Images (gallery, no alt text in source):**
  - `Inpatient.jpg` — inpatient/clinical scene.
  - `DSCF7526.JPG` — clinical care / doctors with patients.
  - `InpatientB.jpg` — inpatient ward scene.
  - `InpatientA.jpg` — inpatient ward scene.
- **Interactive elements:** Shared template Prev/Next links and header/footer navigation only; no page-specific interactivity.
- **Note:** The archived source contains injected Joomla-template spam fragments (Russian anchor text / "megashop24"), which are not genuine content and are excluded.

## 2. Gap Analysis & Feature Enhancements

**Content clarity**
- Resolve the title/content mismatch: the rebuilt page should present a clear catalogue of **specialised/special medical services** (e.g. diagnostics, theatre, specialist clinics) rather than generic inpatient prose.
- Enumerate each **special service** as its own item with description, availability, and the responsible department/specialist.
- Surface the **advanced instruments/systems** as a concrete equipment list with purpose.

**Interactivity & integrations**
- **Service enquiry / referral request** form per special service.
- **Specialist availability** lookup and appointment linkage.
- Cross-links to related departments (Inpatient, Diagnostics, Theatre).

**UX/UI**
- Convert prose + loose images into a **service card grid** with captioned galleries and alt text.
- Add a values/mission highlight block reflecting the faith-based ethos.

**Accessibility & SEO**
- Alt text for all images; single coherent H1 matching the page's real subject.
- `MedicalProcedure`/`MedicalClinic` structured data and a targeted meta description.

## 3. Database Schema Design

```sql
-- Catalogue of special medical services featured on the page
CREATE TABLE wp_special_medical_services (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  department_id  BIGINT UNSIGNED NULL,
  name           VARCHAR(191)    NOT NULL,
  slug           VARCHAR(191)    NOT NULL,
  summary        VARCHAR(512)    NULL,
  description    TEXT            NULL,
  availability   VARCHAR(255)    NULL,              -- e.g. "24 hours", "By appointment"
  is_referral_only TINYINT(1)    NOT NULL DEFAULT 0,
  hero_media_id  BIGINT UNSIGNED NULL,
  sort_order     INT UNSIGNED    NOT NULL DEFAULT 0,
  status         ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at   DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at     TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_sms_slug (slug),
  KEY idx_sms_page (page_id, sort_order),
  CONSTRAINT fk_sms_page  FOREIGN KEY (page_id)       REFERENCES wp_pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_sms_dept  FOREIGN KEY (department_id) REFERENCES wp_departments (id)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_sms_media FOREIGN KEY (hero_media_id) REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Specialists (staff) linked to each special service
CREATE TABLE wp_service_specialists (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  service_id  BIGINT UNSIGNED NOT NULL,
  staff_id    BIGINT UNSIGNED NOT NULL,
  role_label  VARCHAR(191)    NULL,                 -- e.g. "Lead Specialist"
  sort_order  INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_service_specialist (service_id, staff_id),
  CONSTRAINT fk_ss_service FOREIGN KEY (service_id) REFERENCES wp_special_medical_services (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_ss_staff   FOREIGN KEY (staff_id)   REFERENCES wp_staff (id)                    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Advanced medical instruments / systems highlighted on the page
CREATE TABLE wp_service_equipment (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  service_id   BIGINT UNSIGNED NULL,
  page_id      BIGINT UNSIGNED NOT NULL,
  name         VARCHAR(191)    NOT NULL,
  purpose      VARCHAR(512)    NULL,
  media_id     BIGINT UNSIGNED NULL,
  sort_order   INT UNSIGNED    NOT NULL DEFAULT 0,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_equip_page (page_id, sort_order),
  CONSTRAINT fk_equip_service FOREIGN KEY (service_id) REFERENCES wp_special_medical_services (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_equip_page    FOREIGN KEY (page_id)    REFERENCES wp_pages (id)                    ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_equip_media   FOREIGN KEY (media_id)   REFERENCES wp_media_assets (id)             ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Enquiry / referral requests for a special service
CREATE TABLE wp_service_enquiries (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  service_id    BIGINT UNSIGNED NOT NULL,
  full_name     VARCHAR(191)    NOT NULL,
  phone         VARCHAR(40)     NOT NULL,
  email         VARCHAR(191)    NULL,
  message       TEXT            NULL,
  status        ENUM('new','in_progress','resolved','closed') NOT NULL DEFAULT 'new',
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_enq_service (service_id, status),
  CONSTRAINT fk_enq_service FOREIGN KEY (service_id) REFERENCES wp_special_medical_services (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `wp_special_medical_services.page_id` and `wp_service_equipment.page_id` bind the content to the shared **`wp_pages`** row for `/special-medical-services.html`.
- `wp_special_medical_services.department_id` links each service to the shared **`wp_departments`** table; `wp_service_specialists.staff_id` maps services to clinicians in the shared **`wp_staff`** table.
- Service hero images and equipment photos reference the shared **`wp_media_assets`** library (also exposed via the platform `wp_page_media` gallery).
- `wp_service_enquiries` captures front-end referral/enquiry submissions and connects to a service, feeding the CMS handled by shared **`wp_users`**.
