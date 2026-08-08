# Our Philosophy Of Care (`/philosophy-of-care.html`)

> States the hospital's guiding motto, vision, mission, and the beliefs that underpin its patient- and family-centred, faith-based approach to care.

## 1. Current State Mapping

**Page title:** "Our Philosophy Of Care" (from `<h1 class="title">`).

**Page actions:** Joomla "Print" and "Email" icons (boilerplate).

**Textual content (faithful summary):**

- **Motto (centred H1):** *"In Compassionate care we treat; Jesus Heals".*
- **VISION (H4):** To be the leading providers of **quality health and spiritual care** in the **Mt. Kenya Region, Kirinyaga County**, at a place called **Mwea**.
- **MISSION (H4):** The **Sisters of Mary Immaculate** and staff of OLLMH are committed to offering **excellent, affordable, accessible and acceptable health care** to patients and the wider community — including **curative, preventive, promotive, rehabilitative and spiritual** services.
- **Beliefs paragraph 1:** OLLMH respects each family's **values, needs, cultures, resources and strengths**, striving for the highest quality of care by blending **patient care, education and research**; these beliefs are the foundation of its care and partnership with society.
- **Beliefs paragraph 2:** The hospital promotes **healthcare competence through love, knowledge and skills**, believing competence is enhanced by maximizing abilities in **selfless devotion to serve mankind**.

**Images (2 inline photos, empty `alt`):**
- A banner graphic (`images/banner.gif`).
- The Children's Ward (`hospitalUnits/ChildrenWard/kidsWard.JPG`).

**Interactive elements:** None beyond Print/Email actions. No lists, tables, or forms — content is motto + vision + mission + belief statements.

## 2. Gap Analysis & Feature Enhancements

**Content Gaps**
- The care values (curative, preventive, promotive, rehabilitative, spiritual) are buried in prose — they would benefit from being **discrete, explainable value items**.
- No **core values list** (e.g. compassion, integrity, dignity) beyond the mission sentence.
- Vision/mission are static; no patient charter, service standards, or complaints/feedback commitment.

**UX/UI**
- Present the motto as a **hero statement**, with Vision and Mission as distinct visually separated cards.
- Turn the five service dimensions into an **icon grid** with short descriptions.
- Replace the decorative banner GIF and add a captioned, accessible ward image.

**Functionality**
- A **patient feedback / testimonial** module tied to the philosophy ("did we live up to our values?").
- Downloadable **Patient Charter / Code of Conduct** PDF.

**Trust/Accessibility**
- Multiple `<h1>` elements exist (page title + motto) — enforce a single H1 for accessibility/SEO; demote the motto to styled H2.
- Add `alt`/captions; ensure adequate colour contrast on the coloured value text.
- `MedicalOrganization` schema with `slogan` and `knowsAbout` for SEO.

## 3. Database Schema Design

```sql
-- Vision / mission / motto statements for the philosophy page
CREATE TABLE care_statements (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id        BIGINT UNSIGNED NOT NULL,
  statement_type ENUM('motto','vision','mission','belief','other') NOT NULL,
  heading        VARCHAR(191)    NULL,          -- "VISION", "MISSION"
  body           TEXT            NOT NULL,
  sort_order     INT UNSIGNED    NOT NULL DEFAULT 0,
  status         ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at   DATETIME        NULL,
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at     TIMESTAMP       NULL,
  PRIMARY KEY (id),
  KEY idx_care_statements_page (page_id, statement_type, sort_order),
  CONSTRAINT fk_care_statements_page FOREIGN KEY (page_id)
    REFERENCES pages (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Individual care values / service dimensions (curative, preventive, spiritual, ...)
CREATE TABLE care_values (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id     BIGINT UNSIGNED NOT NULL,
  name        VARCHAR(191)    NOT NULL,          -- "Curative", "Spiritual care"
  description TEXT            NULL,
  icon        VARCHAR(100)    NULL,
  sort_order  INT UNSIGNED    NOT NULL DEFAULT 0,
  is_active   TINYINT(1)      NOT NULL DEFAULT 1,
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_care_value_name (page_id, name),
  KEY idx_care_values_page (page_id, sort_order),
  CONSTRAINT fk_care_values_page FOREIGN KEY (page_id)
    REFERENCES pages (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- Both `care_statements.page_id` and `care_values.page_id` reference `pages(id)` for the philosophy page (`slug = philosophy-of-care`).
- Images (banner, Children's Ward) live in `media_assets` and attach through the shared `page_media` join table (role `inline`/`banner`).
- `care_statements` typically holds one motto/vision/mission each, while `care_values` enumerates the five service dimensions as a reusable, sortable list.
