# Wards (`/wards.html`)

> Overview of the hospital's inpatient wards (Maternity, Male, Children), plus the Morgue and Hearse services, describing their setup and equipment.

## 1. Current State Mapping

- **Page title:** "Wards".
- **Intro / General Wards' Design:** States the wards are all equipped with **special beds that enhance comfort and quick recovery**, and that the OLLMH ward setup is convenient for daily operations and makes it easier for medical personnel to do their work.
- **Maternity Ward:** Introduced with photo captions describing **medical personnel and mothers celebrating their newborns** and a **nurse giving routine immunization**.
  - Images: `hospMatron.JPG` (hospital matron/personnel), `FAITH KARIUKI IN MATERNITY WARD GIVING ROUTINE IMMUNIZATION copy.gif` (nurse giving routine immunization).
- **Male Ward:** Caption text: **"Doctors attending Patients at Our Lady Of Lourdes Mwea Hospital (OLLMH)."**
  - Images: `Inpatient.jpg`, `DSC09662.JPG`.
- **Children Ward:** Narrative committing to the best care for the child; emphasizes that the parent is the child's **primary caregiver and source of safety/support**, a role that should not change due to illness/injury, and highlights **partnership with parents/family** as the keystone of their philosophy of care.
  - Image: `DSCF7526 (2).JPG`.
- **Morgue:** Located within the hospital; has **refrigerated chambers with capacity for twenty bodies**; staffed by qualified personnel offering excellent service. The morgue serves **bodies from outside at an affordable rate**, and offers **postmortem (on request)** and **Hearse services**.
  - Images: `Morgue1.JPG`, `Morgue2.JPG`.
- **Hearse:** Notes the hospital **recently acquired a new hearse**, and that **Bishop Maria Wainaina blessed it** just before the launch of the S.M.I Diagnostic Center.
  - Images: `NewHrseFrnt.JPG`, `HearsNBishp.JPG` (bishop blessing the hearse), `NewHsSide.JPG`.
- **Interactive elements:** Only the shared template Prev/Next links and header/footer navigation. No page-specific interactivity. Images have no alt text in the source.
- **Note:** As with sibling pages, the archived HTML carries injected Joomla-template spam fragments (Russian anchor text / "megashop24") that are not real content and are ignored.

## 2. Gap Analysis & Feature Enhancements

**Content & structure**
- Split each ward into a structured **ward profile** (name, description, bed count, gender/age scope, visiting hours, contact) rather than free prose.
- Add **bed capacity and live bed-availability** per ward.
- Add **visiting hours** and admission/discharge guidance.
- Add a dedicated **Morgue & Hearse services** section with pricing tiers, postmortem-on-request info, and a contact/booking channel.

**Interactivity & integrations**
- **Real-time bed availability** indicator per ward (occupied/available).
- **Visitor information / visiting-hour reminders** and directions to each ward.
- **Hearse/mortuary service enquiry form** with response tracking.

**UX/UI**
- Convert the mixed inline images into per-ward **captioned galleries** with alt text and lightbox.
- Feature cards per ward with icons (Maternity, Male, Children, Morgue).

**Accessibility & SEO**
- Descriptive `alt` text for all ward/morgue/hearse images.
- Structured `Hospital`/`MedicalWard` schema and unique meta description.
- Rename cryptic image filenames to descriptive slugs on migration.

## 3. Database Schema Design

```sql
-- Individual wards displayed on the page
CREATE TABLE wards (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  department_id  BIGINT UNSIGNED NULL,
  name           VARCHAR(191)    NOT NULL,          -- Maternity, Male, Children
  slug           VARCHAR(191)    NOT NULL,
  ward_type      ENUM('maternity','male','female','children','general','morgue','other') NOT NULL DEFAULT 'general',
  description    TEXT            NULL,
  bed_count      INT UNSIGNED    NULL,
  available_beds INT UNSIGNED    NULL,
  visiting_hours VARCHAR(255)    NULL,
  in_charge_id   BIGINT UNSIGNED NULL,              -- staff member (ward matron/nurse in charge)
  sort_order     INT UNSIGNED    NOT NULL DEFAULT 0,
  status         ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at   DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at     TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_wards_slug (slug),
  KEY idx_wards_page (page_id, sort_order),
  CONSTRAINT fk_wards_page  FOREIGN KEY (page_id)       REFERENCES pages (id)       ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_wards_dept  FOREIGN KEY (department_id) REFERENCES departments (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_wards_staff FOREIGN KEY (in_charge_id)  REFERENCES staff (id)       ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Per-ward image gallery (captions like "Nurse giving routine immunization")
CREATE TABLE ward_media (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  ward_id    BIGINT UNSIGNED NOT NULL,
  media_id   BIGINT UNSIGNED NOT NULL,
  caption    VARCHAR(512)    NULL,
  sort_order INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_ward_media (ward_id, media_id),
  CONSTRAINT fk_wm_ward  FOREIGN KEY (ward_id)  REFERENCES wards (id)        ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_wm_media FOREIGN KEY (media_id) REFERENCES media_assets (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Morgue & hearse (mortuary) services offered
CREATE TABLE mortuary_services (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  ward_id       BIGINT UNSIGNED NULL,               -- links to the "Morgue" ward row
  name          VARCHAR(191)    NOT NULL,           -- e.g. "Postmortem", "Hearse Service"
  service_type  ENUM('storage','postmortem','hearse','other') NOT NULL DEFAULT 'other',
  description   VARCHAR(512)    NULL,
  on_request    TINYINT(1)      NOT NULL DEFAULT 0,
  fee_amount    DECIMAL(10,2)   NULL,
  currency      CHAR(3)         NOT NULL DEFAULT 'KES',
  chamber_capacity INT UNSIGNED NULL,               -- e.g. 20 bodies
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  KEY idx_mort_page (page_id),
  CONSTRAINT fk_mort_page FOREIGN KEY (page_id) REFERENCES pages (id) ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_mort_ward FOREIGN KEY (ward_id) REFERENCES wards (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Snapshots of bed availability per ward (for the live availability widget)
CREATE TABLE ward_bed_status (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  ward_id        BIGINT UNSIGNED NOT NULL,
  total_beds     INT UNSIGNED    NOT NULL,
  occupied_beds  INT UNSIGNED    NOT NULL DEFAULT 0,
  recorded_at    DATETIME        NOT NULL,
  recorded_by    BIGINT UNSIGNED NULL,              -- users.id
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_bed_ward_time (ward_id, recorded_at),
  CONSTRAINT fk_bed_ward FOREIGN KEY (ward_id)     REFERENCES wards (id) ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_bed_user FOREIGN KEY (recorded_by) REFERENCES users (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `wards.page_id` and `mortuary_services.page_id` anchor all content to the shared **`pages`** row for `/wards.html`.
- `wards.department_id` links each ward to the shared **`departments`** table (inpatient category); `wards.in_charge_id` links to **`staff`** (ward matron/nurse in charge).
- `ward_media.media_id` uses the shared **`media_assets`** library for per-ward galleries, complementing the platform `page_media` join.
- `mortuary_services.ward_id` connects the Morgue/Hearse offerings back to the Morgue ward row; `ward_bed_status.recorded_by` references shared **`users`** (staff CMS accounts).
