# Home (`/index.html`)

> The hospital's landing page: a rotating hero slideshow, an "In Focus" promo strip, tabbed institutional intro content, a scrolling News & Projects feed, and three department showcase columns.

## 1. Current State Mapping

The homepage has an empty `#mainbody`; all real content lives in the template module regions above it. Genuine content, region by region:

### Hero slideshow (`#slideshow`)
An Xpert Slider (`txmod_46`) cycling **12 full-width images** (each with a thumbnail and an empty caption). Slide subjects (from filenames):
1. Prayer Garden (`prayerGarden.jpg`)
2. OLLMH 2019 Graduation (`OLLMH_2019Graduation.jpg`)
3. S.M.I Community 2019 (`SMIcomm2019.jpg`)
4. Diagnostic Unit 2019 (`DiagnosticUnit2019.jpg`)
5. Graduate 2019 (`Graduate2019.JPG`)
6. HIV Test Course (`HivTestCourse.jpg`)
7. 2019 CAFE event (`2019CAFE.jpg`)
8. OLLMH Administration (`OLLMHAdmin.jpg`)
9. Board members 2017 (`Boardmembers17.jpg`)
10. ICU (`ICU_A.jpg`)
11. Inpatient (`Inpatient.jpg`)
12. OLLMH Front Face (`OllmhFrontFace018.jpg`)
Captions are present in markup but empty.

### "In Focus" strip (`#utility`, module title "In Focus")
- **Three promo banner images**, each linked:
  - `DrChir.jpg` → links to **Special Medical Services** page.
  - `nursing_bannerB.jpg` → links to the **nursing application PDF** (`Application form for OLLMMTC updated.pdf`).
  - `Care_Banner.png` → links to the **Wards** page.
- A promotional call-to-action link **"Click to Apply Now!!"** (→ `Application form for OLLMMTC 2021.pdf.pdf`) with the text: *"For A Diploma In School Of; Nursing, Clinical Med & Surgery, Community Health & Dev, Community Health & Hiv-Aids Management, Peri-Operative Theatre Technology, Public Health...."* (markup is heavily MS-Word-pasted).

### Feature region (`#feature`)
**Left column — "Xpert Tabs" (`txmod_27`), 6 tabs**, each with image(s), body text, and a "Read More" button:
1. **About OLLMH** — "Our Lady of Lourdes Mwea Teaching & Referral Hospital is a Catholic institution, ran by the Sisters of Mary Immaculate of Nyeri in Kenya… in collaboration with the Catholic Diocese of Murang'a. It is a registered non-governmental organization (NGO)…" Mentions the **S.M.I Diagnostic Centre** equipped with a **16-slice Sensation CT Scan**. Image `ollmhfrntDescrip2.jpg`.
2. **Hospital Management** — "The board comprises of 14 members, the hospital CEO (Sr. Josephine Ndege) being the secretary to the Board…" Describes the management team of Mary Immaculate Sisters and staff. Image `0llmhBoard.jpg`.
3. **Intl-Attachment Prog** — Hospital is a National & International Attachment/Internship Centre for Doctors and C.Os; offers an exchange programme for doctors from international universities; started 2011 for CO interns. Contact `info@ourladyoflourdesmweahospital.org`. Image `attachmntstud.jpg` (students from Hong Kong University-China).
4. **Philosophy Of Care** — Motto: *"With Compassionate Care, We Treat, Jesus Heals."* **Vision:** "To be the preferred provider of quality health care services." **Mission:** "With compassion, we offer comprehensive and accessible health care services to all for the greater glory of God." Images `banner.gif`, `DSCF7488.JPG`.
5. **Structure & Core** — Core Values intro plus listed values: **Compassion** (treat patients, families, learners with kindness/empathy), **Integrity** (doing the right things at the right time; honesty). Images `DSCF7496.JPG`, `DSCF7494.JPG`.
6. **Name & Origin** — History: hospital is a Catholic church-based institution in the Diocese of Muranga, owned/managed by the Sisters of Mary Immaculate, named after its patron "Our Lady Of Lourdes." Image `history.jpg`.

**Right column — "News & Projects" scroller (XpertScroller)**, 7 items across 2 panes, each with thumbnail, headline, and short intro:
- **16 Slice Sensation CT Scan** — "Opening new CT Scan Facility" (`ctScroll.jpg`).
- **Ollmh Healthcare** (`c4d.jpg`).
- **Ollmh Agricultural Projects** (`ed.jpg`).
- **Hospital & Community Support** (`jiggerspic.JPG`).
- **N.H.I.F** — "We are N.H.I.F Compliant." (`download.jpg`).
- **Ollmh Notice Board** — "1. 22/13/2014 - Staff Tour to….." (`Malysian_plane.jpg`).
- **New & Events** — "OLLMH School Of Nursing prepares and creates informed ability to…" (→ news-events page, `schbus.JPG`).

### Department showcase (`#main-top`), three columns
- **Outpatient Department** — Intro "Ollmh Out patient… facilitates faster and Convenient attendance of critical Situations. Our staff is always ready to handle any patient need at any time." Includes a **(Nursing Application)** PDF link. Sub-section **Paediatric** ("We value our ability to partner with parents in the care of their children… keystone of our philosophy of care" / Children Ward) and **Praying for the Sick** ("Bishop M Wainaina Leading OLLMH staff in praying for the sick, as the world marked the day of the sick"). Images `OutPtest.JPG`, `kidsWard.JPG`, `PrayerFSick.JPG`.
- **Specialised Healthcare** — **The CT Scan Unit**: "Newly Launched CT Scan Unit (S.M.I) Diagnostic Centre (Resident M.O & Hospital C.E.O Sr Josephine Alongside)." **The Eye Unit**: "Patients receive… high quality treatment… friendly and sincere services." **E.N.T**: "Audiology service provides essential assessment and measurement of hearing defects & provision of hearing aids." Images `CtNjOSEPHINE.JPG`, `int-student.jpg`, `Ear.jpg`.
- **Inpatient Department** — "Staff doing routine healthcare to patients admitted…" **Male Ward** ("We are committed to offer Excellent, Affordable & Accessible health care"), **Maternity Ward** ("We respond to the needs of mothers and their babies, in a friendly and professional environment"). Images `medicTime.jpg`, `Inpatient.jpg`, `2019Maternity.jpg`.

### Footer link columns (shared, `#bottom`)
"About" (About OLLMH, Our Organization Structure, Board of Management, Send Your onours), "Future Projection" (Our Staff, Nursing School, …), etc. — these are shared template footer columns, not homepage-specific content.

- **Note:** The archived markup carries injected spam anchors (Russian text, `megashop24`, `printer-spb`) from the compromised Joomla template and vast blocks of MS-Word paste XML; these are **not** real content and are excluded from the rebuild.

## 2. Gap Analysis & Feature Enhancements

**Hero slideshow**
- Add real **captions, titles, and deep-links** per slide (currently all captions are empty), with keyboard-navigable controls, pause-on-hover, and lazy-loaded responsive images.
- Allow admins to schedule slides (publish/unpublish windows) and reorder via CMS.

**Homepage CTAs & conversion**
- Promote clear primary CTAs: **"Apply to Nursing School," "Book an Appointment," "Donate/Support," "Contact Us."** Currently the strongest CTA is a raw PDF link.
- Replace the PDF-only "Apply Now" with an inline **online application** entry point (see application-form page).

**Tabbed intro content**
- Convert the Xpert Tabs to accessible ARIA tabs; store each tab as editable content with its own image and "Read More" target page.
- Fix broken/legacy `index.php?layout=edit` links that point to the old Joomla admin.

**News & Projects**
- Drive the scroller from the real **news/articles** table with dates, categories, and a "View all news" link; add auto-rotation with manual controls.

**Department showcases**
- Pull the three department columns dynamically from `departments`/`services`, each linking to its full page; add icons and consistent captioned galleries.

**Accessibility & SEO**
- Provide descriptive `alt` text for every slide and thumbnail (all currently empty).
- Add a homepage meta title/description, Open Graph tags, `Hospital`/`MedicalOrganization` schema.org markup (name, logo, address, phone, geo), and a single logical H1.
- Remove MS-Word inline styles; use semantic markup and a design system.

**Interactivity & integrations**
- Emergency/contact banner with click-to-call and map.
- Quick links to Clinic Days schedule and NHIF info.
- Optional multilingual (English/Swahili) toggle.

## 3. Database Schema Design

```sql
-- Hero slideshow slides (Xpert Slider replacement)
CREATE TABLE home_slides (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  media_id      BIGINT UNSIGNED NOT NULL,
  headline      VARCHAR(191)    NULL,
  caption       VARCHAR(512)    NULL,
  link_page_id  BIGINT UNSIGNED NULL,      -- internal target page
  link_url      VARCHAR(512)    NULL,       -- external / document target
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  KEY idx_home_slides_page (page_id, sort_order),
  CONSTRAINT fk_slide_page  FOREIGN KEY (page_id)      REFERENCES pages (id)         ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_slide_media FOREIGN KEY (media_id)     REFERENCES media_assets (id)  ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_slide_link  FOREIGN KEY (link_page_id) REFERENCES pages (id)         ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- "In Focus" promo banners
CREATE TABLE home_in_focus_items (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  media_id      BIGINT UNSIGNED NULL,
  title         VARCHAR(191)    NULL,
  body          TEXT            NULL,       -- e.g. the "Click to Apply" programme list
  link_page_id  BIGINT UNSIGNED NULL,
  link_url      VARCHAR(512)    NULL,       -- e.g. application PDF
  cta_label     VARCHAR(100)    NULL,       -- e.g. "Click to Apply Now!!"
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  KEY idx_infocus_page (page_id, sort_order),
  CONSTRAINT fk_infocus_page  FOREIGN KEY (page_id)      REFERENCES pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_infocus_media FOREIGN KEY (media_id)     REFERENCES media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_infocus_link  FOREIGN KEY (link_page_id) REFERENCES pages (id)        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Feature blocks: tabbed intro tabs AND the department-showcase columns
CREATE TABLE home_feature_blocks (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  block_type    ENUM('tab','showcase_column') NOT NULL DEFAULT 'tab',
  title         VARCHAR(191)    NOT NULL,   -- e.g. "About OLLMH", "Outpatient Department"
  body          MEDIUMTEXT      NULL,
  media_id      BIGINT UNSIGNED NULL,       -- lead image
  department_id BIGINT UNSIGNED NULL,       -- link showcase columns to a department
  read_more_page_id BIGINT UNSIGNED NULL,   -- "Read More" target
  read_more_url VARCHAR(512)    NULL,
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  KEY idx_feature_page (page_id, block_type, sort_order),
  CONSTRAINT fk_feature_page  FOREIGN KEY (page_id)           REFERENCES pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_feature_media FOREIGN KEY (media_id)          REFERENCES media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_feature_dept  FOREIGN KEY (department_id)     REFERENCES departments (id)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_feature_rmore FOREIGN KEY (read_more_page_id) REFERENCES pages (id)        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Curated "News & Projects" scroller items shown on the homepage.
-- (Full article bodies live in the news-events schema; this table selects/orders promos.)
CREATE TABLE home_news_promos (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  article_id    BIGINT UNSIGNED NULL,       -- optional FK to news_articles (news-events page)
  media_id      BIGINT UNSIGNED NULL,
  headline      VARCHAR(191)    NOT NULL,
  intro         VARCHAR(512)    NULL,
  link_url      VARCHAR(512)    NULL,
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  KEY idx_news_promo_page (page_id, sort_order),
  CONSTRAINT fk_news_promo_page  FOREIGN KEY (page_id)  REFERENCES pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_news_promo_media FOREIGN KEY (media_id) REFERENCES media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
  -- Optional FK to news_articles(id) is added where the news-events schema is installed:
  -- CONSTRAINT fk_news_promo_article FOREIGN KEY (article_id) REFERENCES news_articles (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- Every homepage table carries `page_id → pages.id` for the `home`-type page, so all regions render from one page record and cascade-delete cleanly.
- `home_slides`, `home_in_focus_items`, `home_feature_blocks`, and `home_news_promos` all reference **`media_assets`** for their imagery instead of hardcoding file paths.
- `home_feature_blocks.department_id → departments.id` links the three showcase columns (Outpatient/Specialised/Inpatient) to the shared department records; `read_more_page_id`/`link_page_id → pages.id` wire internal navigation.
- `home_news_promos.article_id` optionally references the **`news_articles`** table defined on the news-events page, letting the homepage scroller reuse real articles rather than duplicate content.
