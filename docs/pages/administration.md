# Admin menu (`/administration.html`)

> Describes the hospital's governance structure — the 14-member management Board and the day-to-day hospital management team.

## 1. Current State Mapping

**Page title:** "Admin menu" (from `<h1 class="title">`).

**Page actions:** Joomla "Print" and "Email" icons (boilerplate).

**Textual content (faithful summary):**

- **Heading:** "MANAGEMENT" (bold lead-in).
- **Board paragraph:** OLLMH has a **management Board** which is the *governing and policy-formulating body* of the hospital. The board comprises **14 members**, with the **hospital CEO acting as secretary** to the Board within the hospital management team.
- **Management team paragraph:** A **hospital management team** is responsible for the day-to-day management of the institution, comprising: **Administrator, Matron, ART Project Coordinator, Chief Accountant, MOH (Medical Officer of Health), and Deputy Nursing Officer In-Charge.**

**Images (5 inline photos, all with empty `alt`):**
- Row 1: Sr. Josephine portrait (`Aministration/SrJosephine.jpg`), the OLLMH administration block (`0llmhadminblock.jpg`), and the OLLMH Board (`0llmhBoard.jpg`).
- Row 2: A "project action" photo (`images/project_action.jpg`) and the nursing administration block (`nusingadminBlock.jpg`).

**Interactive elements:** None beyond Print/Email actions. No tables, lists, forms, or org chart — the roles are listed only within prose.

## 2. Gap Analysis & Feature Enhancements

**Content Gaps**
- Named leaders are almost entirely missing — only "Sr. Josephine" appears (as an uncaptioned photo). No profiles, titles, tenure, or contact points for the CEO, Administrator, Matron, etc.
- The **14 board members** are referenced but not listed.
- Roles (ART Project Coordinator, MOH, etc.) are named in prose but not defined for lay readers.

**UX/UI**
- Replace prose role lists with a **leadership grid** (photo, name, title, short bio) and a clear **organisational chart** distinguishing the Board (governance) from the Management Team (operations).
- Add captions/`alt` text so photos of the admin block, board, and Sr. Josephine are identifiable.

**Functionality**
- Pull leadership from the shared `staff` table so the same records power department pages and the HR page.
- Add "message the office" / secretariat contact for governance enquiries.

**Trust/Accessibility**
- `Person`/`Organization` structured data for leadership; accessible headshot alt text.
- Publish board mandate, meeting cadence, and (optionally) annual report links to strengthen NGO transparency.

## 3. Database Schema Design

```sql
-- Governance bodies (the Board and the Management Team)
CREATE TABLE governance_bodies (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id     BIGINT UNSIGNED NOT NULL,
  name        VARCHAR(191)    NOT NULL,               -- "Management Board", "Hospital Management Team"
  slug        VARCHAR(191)    NOT NULL,
  body_type   ENUM('board','management_team','committee') NOT NULL DEFAULT 'board',
  member_count SMALLINT UNSIGNED NULL,                -- e.g. 14
  mandate     TEXT            NULL,                    -- "governing and policy formulating body"
  sort_order  INT UNSIGNED    NOT NULL DEFAULT 0,
  status      ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at  TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_gov_body_slug (slug),
  KEY idx_gov_body_page (page_id, sort_order),
  CONSTRAINT fk_gov_body_page FOREIGN KEY (page_id)
    REFERENCES pages (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Membership of a governance body, linking to shared staff records
CREATE TABLE governance_members (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  body_id      BIGINT UNSIGNED NOT NULL,
  staff_id     BIGINT UNSIGNED NULL,                  -- optional link to staff record
  member_name  VARCHAR(191)    NOT NULL,              -- fallback / external member
  position     VARCHAR(191)    NULL,                  -- "Secretary (CEO)", "Administrator", "Matron"
  is_secretary TINYINT(1)      NOT NULL DEFAULT 0,
  photo_media_id BIGINT UNSIGNED NULL,
  sort_order   INT UNSIGNED    NOT NULL DEFAULT 0,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_gov_member_body (body_id, sort_order),
  CONSTRAINT fk_gov_member_body  FOREIGN KEY (body_id)        REFERENCES governance_bodies (id) ON DELETE CASCADE   ON UPDATE CASCADE,
  CONSTRAINT fk_gov_member_staff FOREIGN KEY (staff_id)       REFERENCES staff (id)             ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_gov_member_photo FOREIGN KEY (photo_media_id) REFERENCES media_assets (id)      ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `governance_bodies.page_id` references `pages(id)` for the "Admin menu" page (`slug = administration`).
- `governance_members.body_id` references `governance_bodies(id)`; each member optionally links to a shared `staff(id)` record (management roles like Administrator, Matron, CEO) so profiles are reused across pages.
- `governance_members.photo_media_id` references `media_assets(id)`; the admin-block/board photos on the page are attached through the shared `page_media` join table (role `gallery`).
