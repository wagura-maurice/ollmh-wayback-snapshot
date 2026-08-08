# Contacts (`/contacts.html`)

> Provides the hospital's contact channels — email and several phone numbers — and invites visitors to call, email, or visit.

## 1. Current State Mapping

**Page title:** "Contacts" (from `<h1 class="title">`).

**Page actions:** Joomla "Print" and "Email" icons (boilerplate).

**Textual content (faithful summary):**

- **Invitation line:** "Feel free to Contact us and even to visit us. Someone is waiting for your Call."
- **Email:** Rendered via Joomla's spam-protection cloak — displayed as *"This email address is being protected from spambots. You need JavaScript enabled to view it."* The JavaScript decodes to **info@ourladyoflourdesmweahospital.org**.
- **Phone numbers (labelled "Pnone No" — sic; rendered without spacing in the source):**
  - **+254737801707**
  - **+2540722260748**
  - **+2540202032382**
- **Closing line:** "We check our mails frequently, feel free to email us and [we] will give feedback as quickly as we receive it."

**Images (2 inline photos, empty `alt`):**
- A miscellaneous department photo (`hospitalUnits/MiscDept/DSCF7360.JPG`).
- An outpatient photo (`images/ollmh/outp2.jpg`).

**Interactive elements:** None functional — despite being the "Contacts" page there is **no contact form, no clickable `tel:`/`mailto:` links, and no embedded map**. The email is obfuscated behind JavaScript.

## 2. Gap Analysis & Feature Enhancements

**Content Gaps**
- No **physical/postal address** on the contacts page itself (the address appears only on the Location page), no P.O. Box, and no **opening/visiting hours**.
- No department- or role-specific contacts (e.g. appointments, billing, emergency line).
- No social media links or emergency/ambulance number.

**UX/UI**
- Add a proper **contact form** (name, email, phone, subject, message) with validation and spam protection (honeypot/CAPTCHA).
- Make phone numbers clickable (`tel:`) and email `mailto:`; group them with labels (main line, mobile, landline).
- Embed a **map** with directions, and show opening hours prominently.

**Functionality**
- Store form submissions in the database with status tracking and email notifications to `info@`.
- Route enquiries to the right department; auto-acknowledge submitters.
- List multiple contact points (departments) sourced from shared `departments`/`staff`.

**Trust/Accessibility**
- Fix the "Pnone No" typo; normalise/verify the phone numbers (`+254 202 032382` etc.).
- Add `alt`/captions to images; ensure form fields have proper labels and ARIA.
- `ContactPoint` structured data and reCAPTCHA for spam resilience.

## 3. Database Schema Design

```sql
-- Contact channels shown on the contacts page (emails, phones, hours, social)
CREATE TABLE contact_channels (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  department_id BIGINT UNSIGNED NULL,             -- optional department-specific channel
  channel_type  ENUM('phone','mobile','email','fax','whatsapp','postal','social','hours') NOT NULL,
  label         VARCHAR(191)    NULL,             -- "Main line", "Appointments"
  value         VARCHAR(255)    NOT NULL,         -- "+254737801707", "info@..."
  is_primary    TINYINT(1)      NOT NULL DEFAULT 0,
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  is_active     TINYINT(1)      NOT NULL DEFAULT 1,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_contact_channel_page (page_id, sort_order),
  CONSTRAINT fk_contact_channel_page FOREIGN KEY (page_id)       REFERENCES pages (id)       ON DELETE CASCADE   ON UPDATE CASCADE,
  CONSTRAINT fk_contact_channel_dept FOREIGN KEY (department_id) REFERENCES departments (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Submissions from the enhanced contact form
CREATE TABLE contact_submissions (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  department_id BIGINT UNSIGNED NULL,             -- routed-to department
  sender_name   VARCHAR(191)    NOT NULL,
  sender_email  VARCHAR(191)    NOT NULL,
  sender_phone  VARCHAR(40)     NULL,
  subject       VARCHAR(255)    NULL,
  message       TEXT            NOT NULL,
  status        ENUM('new','read','replied','spam','archived') NOT NULL DEFAULT 'new',
  handled_by    BIGINT UNSIGNED NULL,             -- staff/user who responded
  ip_address    VARBINARY(16)   NULL,
  user_agent    VARCHAR(255)    NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_submission_page_status (page_id, status),
  CONSTRAINT fk_submission_page    FOREIGN KEY (page_id)       REFERENCES pages (id)       ON DELETE CASCADE   ON UPDATE CASCADE,
  CONSTRAINT fk_submission_dept    FOREIGN KEY (department_id) REFERENCES departments (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_submission_handler FOREIGN KEY (handled_by)    REFERENCES users (id)       ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Relationships**
- `contact_channels.page_id` and `contact_submissions.page_id` reference `pages(id)` for the contacts page (`slug = contacts`).
- Both tables optionally reference `departments(id)` so channels/enquiries can be scoped or routed to a specific department.
- `contact_submissions.handled_by` references the shared `users(id)` (CMS editors/admins) for enquiry follow-up.
- Contact-page images live in `media_assets` and attach through the shared `page_media` join table (role `inline`/`gallery`).
