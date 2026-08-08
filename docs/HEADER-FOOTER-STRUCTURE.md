# Header & Footer Structural Outline (WordPress)

> This document defines the **information architecture, hierarchy, and
> wording** for the header (top navigation) and footer of the OLLMH WordPress
> website. It is a structural specification — not code — describing what each
> section contains and how it is organized.
>
> All database table references in this document follow the WordPress
> `wp_<table_name>` prefix convention, consistent with
> [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md) and the
> [consolidated ERD](./ERD.md).

---

## Header (Top Navigation)

### Design principles

- **Mega-menu dropdowns** for parent items with many sub-pages, revealing
  sub-links in a multi-column panel on hover/focus.
- **Direct-link items** (no dropdown) for single-destination entries.
- **Sticky behaviour**: the header remains visible on scroll for quick
  navigation from anywhere on the page.
- **Mobile**: the full menu collapses into an off-canvas hamburger menu with
  accordion-style expand/collapse for each parent.
- **Accessibility**: every dropdown is keyboard-navigable (Tab / Enter / Esc),
  ARIA labels on parent toggles, and focus indicators on all links.
- **Active state**: the current page's menu item (or its parent) is
  highlighted to orient the visitor.

### Menu data source

All menu items are stored as rows in the `wp_menu_items` table (defined in
[`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md)), with `menu_area =
'header'`. Parent items use `external_url = NULL` and `page_id = NULL` (they
are non-navigating dropdown toggles); leaf items carry `page_id → wp_pages.id`
for internal targets. The `sort_order` column controls the left-to-right
sequence.

---

### Header structure — item by item

#### 1. Home

| Property | Value |
| --- | --- |
| Type | Direct link (no dropdown) |
| Label | **Home** |
| Target | `wp_pages` row with `page_type = 'home'` (the front page) |
| Wording rationale | Universal convention; no ambiguity. |

---

#### 2. About Us

| Property | Value |
| --- | --- |
| Type | Parent (dropdown) |
| Label | **About Us** |
| Target | Non-navigating toggle (`page_id = NULL`) |

**Sub-pages (dropdown items):**

| # | Label | Target page | Notes |
| --- | --- | --- | --- |
| 2.1 | **About OLLMH & Location** | `about-ollmh-location` | Hospital history, milestones, and physical location with map. |
| 2.2 | **Administration & Governance** | `administration` | Board of Management, organizational structure, governance bodies. |
| 2.3 | **Our Philosophy of Care** | `philosophy-of-care` | Mission statement, core values, ministerial goals, and faith foundation. |
| 2.4 | **Our Staff & Capacity** | `hr-capacity-staff` | Staff cadres, HR capacity statistics, current job vacancies. |

**Wording rationale:**
- "About Us" is the standard label for organizational background sections.
- "About OLLMH & Location" combines identity and geography — visitors looking
  for either find both in one place.
- "Administration & Governance" is clearer than the archived "Administration"
  alone; it signals both the people and the structure.
- "Our Philosophy of Care" is preserved from the original — it is already
  well-worded and distinctively OLLMH.
- "Our Staff & Capacity" replaces the awkward "HR-Capacity (Staff)" — it reads
  naturally while covering both the team roster and workforce statistics.

---

#### 3. Services

| Property | Value |
| --- | --- |
| Type | Parent (dropdown) |
| Label | **Services** |
| Target | Non-navigating toggle (`page_id = NULL`) |

**Sub-pages (dropdown items):**

| # | Label | Target page | Notes |
| --- | --- | --- | --- |
| 3.1 | **Inpatient Department** | `in-patient-dept` | Inpatient services, admission process, ward descriptions. |
| 3.2 | **Outpatient Department** | `out-patient-dept` | OPD facilities, operating hours, consultation rooms, appointments. |
| 3.3 | **Wards** | `wards` | Ward listings, bed capacity, mortuary services. |
| 3.4 | **Special Medical Services** | `special-medical-services` | Specialist services, equipment, and consultant directory. |
| 3.5 | **Clinic Days & Schedule** | `clinic-days` | Clinic calendar, booking system, and exceptions/closures. |

**Wording rationale:**
- "Services" is the universal hospital navigation label.
- "Inpatient Department" and "Outpatient Department" fix the abbreviated
  "In patient Dept" / "Out Patient Dept" from the archive — full words are
  clearer and more professional.
- "Wards" is preserved — it is already concise and correct.
- "Special Medical Services" is preserved — it accurately describes specialist
  care.
- "Clinic Days & Schedule" expands the archived "Clinic Days" to signal that
  the page includes both the calendar and the booking workflow.

---

#### 4. Departments

| Property | Value |
| --- | --- |
| Type | Parent (dropdown) |
| Label | **Departments** |
| Target | Non-navigating toggle (`page_id = NULL`) |

**Sub-pages (dropdown items):**

| # | Label | Target page | Notes |
| --- | --- | --- | --- |
| 4.1 | **All Departments** | `ollmh-departments` | Department showcase grid with head of department, cover photo, and description for each. |
| 4.2 | **OLLMH Outlook (Photo Gallery)** | `ollmh-outlook` | Categorized photo albums of the hospital campus, facilities, and events. |

**Wording rationale:**
- "Departments" is split out from the archived "Features" group, which mixed
  departments, a gallery, and a community page under an unclear label.
- "All Departments" replaces the redundant "Ollmh Departments" — the hospital
  name is already in the logo; the word "All" signals a comprehensive listing.
- "OLLMH Outlook (Photo Gallery)" clarifies what "Outlook" means by appending
  the content type in parentheses.

---

#### 5. Projects & Community

| Property | Value |
| --- | --- |
| Type | Parent (dropdown) |
| Label | **Projects & Community** |
| Target | Non-navigating toggle (`page_id = NULL`) |

**Sub-pages (dropdown items):**

| # | Label | Target page | Notes |
| --- | --- | --- | --- |
| 5.1 | **Development Projects** | `development-projects` | Capital projects, strategic plans, progress metrics, and media. |
| 5.2 | **Self-Sustainability Projects** | `self-sustainability-projects` | Income-generating ventures (farm, dairy, etc.) with production records. |
| 5.3 | **Community Support** | `community-support` | Outreach programs, health education, volunteer sign-ups. |
| 5.4 | **S.M.I Community** | `smi-community` | Sisters of Mary Immaculate community profile, facilities, and events. |
| 5.5 | **Upcoming Projects** | `upcoming-projects` | Pipeline projects with phases, pledges, and progress tracking. |

**Wording rationale:**
- "Projects & Community" merges the archived "Projects" parent and the
  "S.M.I Community" item (previously buried under "Features") into one
  logically coherent group — all are forward-looking, community-oriented
  initiatives.
- "Self-Sustainability Projects" fixes the typo "Self Sustinabilbity Projects"
  from the archive.
- "S.M.I Community" is preserved as a proper name (Sisters of Mary Immaculate).
- "Upcoming Projects" is preserved — it is already clear.

---

#### 6. Nursing School

| Property | Value |
| --- | --- |
| Type | Parent (dropdown) |
| Label | **Nursing School** |
| Target | Non-navigating toggle (`page_id = NULL`) |

**Sub-pages (dropdown items):**

| # | Label | Target page | Notes |
| --- | --- | --- | --- |
| 6.1 | **About the Nursing School** | `about-nursing-school` | School profile, programmes, facilities, intake schedule. |
| 6.2 | **Application Form** | `medical-school-application-form` | Online application workflow with status tracking, payments, and document upload. |

**Wording rationale:**
- "Nursing School" replaces the truncated "Nursing Sch-" from the archive.
- "About the Nursing School" is preserved — it is already well-worded.
- "Application Form" replaces the truncated "Medical Sch- Application Form" —
  it is shorter, clearer, and accurately describes the page function.

---

#### 7. News & Events

| Property | Value |
| --- | --- |
| Type | Parent (dropdown) |
| Label | **News & Events** |
| Target | Non-navigating toggle (`page_id = NULL`) |

**Sub-pages (dropdown items):**

| # | Label | Target page | Notes |
| --- | --- | --- | --- |
| 7.1 | **News & Announcements** | `/news/` (listing page) | Chronological feed of all published news articles; each article links to its own standalone page at `/news/<slug>`. |
| 7.2 | **Events Calendar** | `/events/` (listing page) | Calendar of upcoming and past events; each event links to its own standalone page at `/events/<slug>` with RSVP. |

**Wording rationale:**
- "News & Events" fixes the typo "New & Events" from the archive and groups
  the two related content types under one parent.
- "News & Announcements" is more descriptive than "News" alone — it signals
  that the feed includes both news articles and general announcements.
- "Events Calendar" signals that the page is a calendar view (month grid +
  list), not just a text listing.
- This structure reflects the per-entry page architecture documented in
  [`pages/news/`](./pages/news/) and [`pages/events/`](./pages/events/).

---

#### 8. Contact Us

| Property | Value |
| --- | --- |
| Type | Parent (dropdown) |
| Label | **Contact Us** |
| Target | Non-navigating toggle (`page_id = NULL`) |

**Sub-pages (dropdown items):**

| # | Label | Target page | Notes |
| --- | --- | --- | --- |
| 8.1 | **Contact Information** | `contacts` | Phone numbers, email addresses, physical address, map, and contact form. |
| 8.2 | **Webmail Login** | External URL | Link to the hospital's webmail portal for staff. |

**Wording rationale:**
- "Contact Us" replaces the awkward "Contacts/Mails" from the archive — it is
  the standard website convention.
- "Contact Information" is clearer than "Contacts" alone — it tells the
  visitor what to expect (phone, email, address, map, form).
- "Webmail Login" replaces "Mail" — it is explicit about the destination and
  avoids confusion with the contact form.
- The archived "Login" link is dropped from the main menu; staff authentication
  is handled through the Webmail Login and the WordPress admin bar (visible
  only to logged-in CMS users via `wp_users`).

---

### Header visual summary

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [LOGO]  Home  About Us ▾  Services ▾  Departments ▾  Projects &     │
│          Community ▾  Nursing School ▾  News & Events ▾  Contact Us ▾  │
└──────────────────────────────────────────────────────────────────────────┘
```

Dropdown example (About Us):

```
┌──────────────────────────┐
│  About OLLMH & Location  │
│  Administration &        │
│    Governance            │
│  Our Philosophy of Care  │
│  Our Staff & Capacity    │
└──────────────────────────┘
```

---

## Footer

### Design principles

- **Multi-column layout** (4 columns on desktop, stacked on mobile) providing
  quick access to key pages, contact information, and organizational identity.
- **No "Electoral Positions" section** — this section is explicitly excluded.
- **Bottom bar** with copyright notice, legal links, and attribution.
- **Consistency**: footer links point to the same `wp_pages` rows as the header
  menu items, ensuring visitors can reach any page from both locations.
- **Contact-first**: the first column gives visitors immediate access to
  physical address, phone numbers, and email without having to navigate to the
  contacts page.

### Footer data source

Footer links are stored as rows in `wp_menu_items` with `menu_area = 'footer'`.
The contact details (address, phone, email) are stored in the `wp_contact_channels`
table (defined in [`pages/contacts.md`](./pages/contacts.md)) and rendered
directly into the footer template.

---

### Footer structure — column by column

#### Column 1: Contact Information

This column displays the hospital's contact details directly (not as links,
except where noted). It is the leftmost column for immediate visibility.

| # | Type | Content / Label | Details |
| --- | --- | --- | --- |
| 1.1 | **Heading** | **Contact Us** | Column heading. |
| 1.2 | Address | Physical address of the hospital | Rendered as plain text, sourced from `wp_contact_channels` (type = 'address'). Example: "Our Lady of Lourdes Mwea Hospital, Mwea, Kirinyaga County, Kenya." |
| 1.3 | Phone | Primary phone number | Plain text, sourced from `wp_contact_channels` (type = 'phone'). Clickable on mobile (`tel:` link). |
| 1.4 | Phone | Emergency / ambulance number (if separate) | Plain text, sourced from `wp_contact_channels` (type = 'emergency'). |
| 1.5 | Email | General enquiries email | `mailto:` link, sourced from `wp_contact_channels` (type = 'email'). |
| 1.6 | Link | **View on Map** | External link to Google Maps pin for the hospital location. |
| 1.7 | Link | **Send Us a Message** | Internal link to the `contacts` page (contact form). |

**Wording rationale:**
- "Contact Us" as the heading is consistent with the header menu label.
- Displaying the address and phone directly in the footer means a visitor in
  need of urgent contact information does not have to click through to another
  page.
- "View on Map" and "Send Us a Message" are action-oriented labels that tell
  the visitor what happens when they click.

---

#### Column 2: About OLLMH

Quick links to the organizational background pages.

| # | Type | Content / Label | Target page |
| --- | --- | --- | --- |
| 2.1 | **Heading** | **About OLLMH** | — |
| 2.2 | Link | About OLLMH & Location | `about-ollmh-location` |
| 2.3 | Link | Administration & Governance | `administration` |
| 2.4 | Link | Our Philosophy of Care | `philosophy-of-care` |
| 2.5 | Link | Our Staff & Capacity | `hr-capacity-staff` |
| 2.6 | Link | OLLMH Outlook (Photo Gallery) | `ollmh-outlook` |

**Wording rationale:**
- "About OLLMH" as the heading is shorter than "About Us" (already used in the
  header) while still being clear in the footer context.
- The link labels match the header sub-menu labels exactly, so visitors
  recognize the same pages regardless of where they navigate from.
- "OLLMH Outlook (Photo Gallery)" is included here because the gallery is a
  visual showcase that benefits from footer discoverability.

---

#### Column 3: Our Services

Quick links to the clinical service pages.

| # | Type | Content / Label | Target page |
| --- | --- | --- | --- |
| 3.1 | **Heading** | **Our Services** | — |
| 3.2 | Link | Inpatient Department | `in-patient-dept` |
| 3.3 | Link | Outpatient Department | `out-patient-dept` |
| 3.4 | Link | Wards | `wards` |
| 3.5 | Link | Special Medical Services | `special-medical-services` |
| 3.6 | Link | Clinic Days & Schedule | `clinic-days` |
| 3.7 | Link | All Departments | `ollmh-departments` |

**Wording rationale:**
- "Our Services" as the heading is warm and possessive, consistent with a
  hospital's patient-first tone.
- The link labels match the header sub-menu labels exactly.
- "All Departments" is included here because departments are functionally
  related to services — a visitor looking for a specific clinic or ward may
  think to look under "Services" in the footer.

---

#### Column 4: Projects, Community & Nursing School

Quick links to the forward-looking initiatives and the nursing school.

| # | Type | Content / Label | Target page |
| --- | --- | --- | --- |
| 4.1 | **Heading** | **Projects & Community** | — |
| 4.2 | Link | Development Projects | `development-projects` |
| 4.3 | Link | Self-Sustainability Projects | `self-sustainability-projects` |
| 4.4 | Link | Community Support | `community-support` |
| 4.5 | Link | S.M.I Community | `smi-community` |
| 4.6 | Link | Upcoming Projects | `upcoming-projects` |
| 4.7 | **Sub-heading** | **Nursing School** | — |
| 4.8 | Link | About the Nursing School | `about-nursing-school` |
| 4.9 | Link | Application Form | `medical-school-application-form` |

**Wording rationale:**
- "Projects & Community" matches the header parent label for consistency.
- The nursing school links are grouped under a sub-heading within the same
  column to save space (avoiding a 5th column) while keeping them visually
  distinct.
- "Application Form" is included in the footer because prospective students
  may look for it at the bottom of any page, not just under the Nursing School
  menu.

---

### Bottom bar (copyright & legal)

A full-width strip below the four columns.

| # | Position | Content / Label | Details |
| --- | --- | --- | --- |
| B1 | Left | **Copyright notice** | "© 2024 Our Lady of Lourdes Mwea Hospital. All Rights Reserved." (year auto-updated server-side). |
| B2 | Center | **Privacy Policy** | Internal link to a `privacy-policy` page (`wp_pages` row, `page_type = 'generic'`). |
| B3 | Center | **Terms of Service** | Internal link to a `terms-of-service` page (`wp_pages` row, `page_type = 'generic'`). |
| B4 | Right | **News & Events** | Internal link to `/news/` — provides a quick path to fresh content from the footer. |
| B5 | Right | **Webmail Login** | External link to the webmail portal (same as header item 8.2). |

**Wording rationale:**
- The copyright notice uses the full hospital name for formality.
- "Privacy Policy" and "Terms of Service" are standard legal pages required
  for professional websites; they will be created as new `wp_pages` rows during
  the WordPress build.
- "News & Events" and "Webmail Login" in the bottom bar give visitors a
  one-click path to fresh content and staff email from any page.

---

### Footer visual summary

```
┌────────────────────┬────────────────────┬────────────────────┬────────────────────────┐
│  Contact Us        │  About OLLMH       │  Our Services      │  Projects & Community   │
│                    │                    │                    │                        │
│  [address]         │  About OLLMH &     │  Inpatient Dept.   │  Development Projects  │
│  [phone]           │    Location        │  Outpatient Dept.  │  Self-Sustainability   │
│  [emergency]       │  Administration &  │  Wards             │    Projects            │
│  [email]           │    Governance      │  Special Medical   │  Community Support     │
│  View on Map       │  Our Philosophy    │    Services        │  S.M.I Community       │
│  Send Us a Message │    of Care         │  Clinic Days &     │  Upcoming Projects     │
│                    │    Schedule        │                    │                        │
│                    │  Our Staff &       │  All Departments   │  Nursing School        │
│                    │    Capacity        │                    │    About the Nursing   │
│                    │  OLLMH Outlook     │                    │      School            │
│                    │    (Photo Gallery) │                    │    Application Form    │
├────────────────────┴────────────────────┴────────────────────┴────────────────────────┤
│ © 2024 Our Lady of Lourdes Mwea Hospital. All Rights Reserved.  Privacy Policy  Terms  │
│ of Service                              News & Events   Webmail Login                 │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Menu items to database mapping

The following table maps every header and footer menu item to its
`wp_menu_items` row, showing how the information architecture plugs into the
database schema.

| Menu area | Parent label | Item label | `page_id` target | `external_url` |
| --- | --- | --- | --- | --- |
| header | — | Home | `wp_pages.id` (home) | NULL |
| header | About Us | About OLLMH & Location | `wp_pages.id` (about-ollmh-location) | NULL |
| header | About Us | Administration & Governance | `wp_pages.id` (administration) | NULL |
| header | About Us | Our Philosophy of Care | `wp_pages.id` (philosophy-of-care) | NULL |
| header | About Us | Our Staff & Capacity | `wp_pages.id` (hr-capacity-staff) | NULL |
| header | Services | Inpatient Department | `wp_pages.id` (in-patient-dept) | NULL |
| header | Services | Outpatient Department | `wp_pages.id` (out-patient-dept) | NULL |
| header | Services | Wards | `wp_pages.id` (wards) | NULL |
| header | Services | Special Medical Services | `wp_pages.id` (special-medical-services) | NULL |
| header | Services | Clinic Days & Schedule | `wp_pages.id` (clinic-days) | NULL |
| header | Departments | All Departments | `wp_pages.id` (ollmh-departments) | NULL |
| header | Departments | OLLMH Outlook (Photo Gallery) | `wp_pages.id` (ollmh-outlook) | NULL |
| header | Projects & Community | Development Projects | `wp_pages.id` (development-projects) | NULL |
| header | Projects & Community | Self-Sustainability Projects | `wp_pages.id` (self-sustainability-projects) | NULL |
| header | Projects & Community | Community Support | `wp_pages.id` (community-support) | NULL |
| header | Projects & Community | S.M.I Community | `wp_pages.id` (smi-community) | NULL |
| header | Projects & Community | Upcoming Projects | `wp_pages.id` (upcoming-projects) | NULL |
| header | Nursing School | About the Nursing School | `wp_pages.id` (about-nursing-school) | NULL |
| header | Nursing School | Application Form | `wp_pages.id` (medical-school-application-form) | NULL |
| header | News & Events | News & Announcements | `wp_pages.id` (news listing) | NULL |
| header | News & Events | Events Calendar | `wp_pages.id` (events listing) | NULL |
| header | Contact Us | Contact Information | `wp_pages.id` (contacts) | NULL |
| header | Contact Us | Webmail Login | NULL | (external webmail URL) |
| footer | — | Contact Us (column 1) | — | — (contact details rendered from `wp_contact_channels`) |
| footer | — | View on Map | NULL | (Google Maps URL) |
| footer | — | Send Us a Message | `wp_pages.id` (contacts) | NULL |
| footer | About OLLMH (column 2) | About OLLMH & Location | `wp_pages.id` (about-ollmh-location) | NULL |
| footer | About OLLMH | Administration & Governance | `wp_pages.id` (administration) | NULL |
| footer | About OLLMH | Our Philosophy of Care | `wp_pages.id` (philosophy-of-care) | NULL |
| footer | About OLLMH | Our Staff & Capacity | `wp_pages.id` (hr-capacity-staff) | NULL |
| footer | About OLLMH | OLLMH Outlook (Photo Gallery) | `wp_pages.id` (ollmh-outlook) | NULL |
| footer | Our Services (column 3) | Inpatient Department | `wp_pages.id` (in-patient-dept) | NULL |
| footer | Our Services | Outpatient Department | `wp_pages.id` (out-patient-dept) | NULL |
| footer | Our Services | Wards | `wp_pages.id` (wards) | NULL |
| footer | Our Services | Special Medical Services | `wp_pages.id` (special-medical-services) | NULL |
| footer | Our Services | Clinic Days & Schedule | `wp_pages.id` (clinic-days) | NULL |
| footer | Our Services | All Departments | `wp_pages.id` (ollmh-departments) | NULL |
| footer | Projects & Community (col 4) | Development Projects | `wp_pages.id` (development-projects) | NULL |
| footer | Projects & Community | Self-Sustainability Projects | `wp_pages.id` (self-sustainability-projects) | NULL |
| footer | Projects & Community | Community Support | `wp_pages.id` (community-support) | NULL |
| footer | Projects & Community | S.M.I Community | `wp_pages.id` (smi-community) | NULL |
| footer | Projects & Community | Upcoming Projects | `wp_pages.id` (upcoming-projects) | NULL |
| footer | Nursing School (sub-heading) | About the Nursing School | `wp_pages.id` (about-nursing-school) | NULL |
| footer | Nursing School | Application Form | `wp_pages.id` (medical-school-application-form) | NULL |
| footer (bottom bar) | — | Privacy Policy | `wp_pages.id` (privacy-policy) | NULL |
| footer (bottom bar) | — | Terms of Service | `wp_pages.id` (terms-of-service) | NULL |
| footer (bottom bar) | — | News & Events | `wp_pages.id` (news listing) | NULL |
| footer (bottom bar) | — | Webmail Login | NULL | (external webmail URL) |

---

## Changes from the archived navigation

This section summarizes how the new structure improves on the archived
navigation (documented in [`header-footer-links.md`](./header-footer-links.md)).

| Archived issue | Resolution in new structure |
| --- | --- |
| "New & Events" typo; page was a nursing-school advert, not a news feed | Fixed to "News & Events"; split into per-entry pages under `news/` and `events/` with a real feed and calendar. |
| "Nursing Sch-" truncated label | Expanded to "Nursing School". |
| "Medical Sch- Application Form" truncated label | Shortened to "Application Form". |
| "Contacts/Mails" unclear label | Split into "Contact Us" parent with "Contact Information" and "Webmail Login" sub-items. |
| "Features" group mixed departments, a gallery, and a community page | "Departments" (All Departments + Outlook Gallery) and "S.M.I Community" (moved to Projects & Community) are now in logically coherent groups. |
| "Self Sustinabilbity Projects" typo | Fixed to "Self-Sustainability Projects". |
| "In patient Dept" / "Out Patient Dept" abbreviations | Expanded to "Inpatient Department" / "Outpatient Department". |
| "HR-Capacity (Staff)" awkward label | Reworded to "Our Staff & Capacity". |
| "Ollmh Departments" redundant hospital name prefix | Shortened to "All Departments". |
| "Login" link in main menu (unclear destination) | Removed; staff authentication via "Webmail Login" and WordPress admin bar. |
| Footer "Send Your onours" typo and dead link | Replaced with "Send Us a Message" linking to the contact form. |
| Footer "Future Projection" unclear heading | Replaced with "Our Services" column (clearer, service-focused). |
| Footer "Core Values" column with all dead links | Replaced with "Projects, Community & Nursing School" column (real, navigable links). |
| No privacy policy or terms of service links | Added to the bottom bar as standard legal pages. |
| No "Electoral Positions" section | Confirmed: no such section exists in the new structure. |
