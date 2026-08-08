# Header & Footer Structural Outline (WordPress)

> This document defines the **information architecture, hierarchy, and
> wording** for the header (top navigation) and footer of the OLLMH WordPress
> website. It is a structural specification — not code — describing what each
> section contains, how it is organized, and where each element is placed.
>
> All database table references follow the WordPress `wp_<table_name>` prefix
> convention, consistent with [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md)
> and the [consolidated ERD](./ERD.md).

---

## Header (Top Navigation)

### Layout arrangement

The header is a single horizontal bar divided into three zones, left to right:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  [LOGO + TAGLINE]    [NAV MENU ITEMS . . .]              [CTA BUTTON]       │
│  (left zone)         (center zone)                       (right zone)       │
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **Left zone — Brand block**: the hospital logo (icon mark) paired with the
   site name and a one-line tagline beneath it. The entire brand block is
   clickable and navigates to the home page.
2. **Center zone — Navigation menu**: a horizontal row of top-level menu items.
   Items with sub-pages reveal a dropdown panel on hover/focus; items without
   sub-pages are direct links.
3. **Right zone — Call-to-action button**: a single, visually distinct button
   (filled background, contrasting colour) that stands apart from the plain
   text links in the navigation row.

On mobile (≤ 768px) the center and right zones collapse into an off-canvas
hamburger panel; the brand block remains visible in the bar.

### Design principles

- **Sticky behaviour**: the header remains pinned to the top of the viewport on
  scroll, so navigation is always reachable.
- **Dropdown panels**: parent items show a vertical dropdown of sub-page links
  on hover (desktop) or tap-expand (mobile accordion). The dropdown is a simple
  single-column list — not a mega-menu — keeping the hierarchy shallow and
  scannable.
- **CTA button separation**: the call-to-action is visually separated from the
  nav links (different shape, colour, and padding) so it reads as an action,
  not a navigation destination.
- **Active state**: the current page's menu item (or its parent) is
  highlighted (e.g. bold or underline) to orient the visitor.
- **Accessibility**: keyboard-navigable (Tab / Enter / Esc), ARIA labels on
  dropdown toggles, focus indicators on all links, and `aria-current="page"`
  on the active item.

### Brand block

| Element | Content | Placement |
| --- | --- | --- |
| Logo icon | Hospital crest / cross mark | Left of the text |
| Site name | **OLLMH** | Bold, primary colour |
| Tagline | **Our Lady of Lourdes Mwea Hospital** | Smaller, muted text beneath the site name |

**Wording rationale:**
- "OLLMH" as the short brand name is punchy and recognizable; the full name
  as a tagline provides context for first-time visitors without taking up a
  second line in the logo area.

### Menu data source

All menu items are stored as rows in the `wp_menu_items` table (defined in
[`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md)), with `menu_area =
'header'`. Parent items use `external_url = NULL` and `page_id = NULL` (they
are non-navigating dropdown toggles); leaf items carry `page_id → wp_pages.id`
for internal targets. The `sort_order` column controls the left-to-right
sequence. The CTA button is a `wp_menu_items` row with a CSS class flag
(e.g. `menu-item-cta`) that the theme renders as a button.

---

### Header structure — item by item

#### 1. Home

| Property | Value |
| --- | --- |
| Type | Direct link (no dropdown) |
| Label | **Home** |
| Target | `wp_pages` row with `page_type = 'home'` |
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

#### 7. News

| Property | Value |
| --- | --- |
| Type | Direct link (no dropdown) |
| Label | **News** |
| Target | `/news/` (listing page, `wp_pages` row with `page_type = 'news'`) |
| Wording rationale | "News" is a standalone top-level item — each article has its own page at `/news/<slug>` (see [`pages/news/`](./pages/news/)). Keeping it as a direct link (not a dropdown) mirrors the flat-nav pattern: the user lands on the feed, then drills into individual articles. |

---

#### 8. Events

| Property | Value |
| --- | --- |
| Type | Direct link (no dropdown) |
| Label | **Events** |
| Target | `/events/` (listing page, `wp_pages` row with `page_type = 'news'`) |
| Wording rationale | "Events" is a standalone top-level item — each event has its own page at `/events/<slug>` (see [`pages/events/`](./pages/events/)). Separating News and Events into distinct top-level items (rather than grouping them under a "News & Events" parent) gives each content type its own discoverable entry point in the navigation bar. |

---

#### 9. Contact Us

| Property | Value |
| --- | --- |
| Type | Direct link (no dropdown) |
| Label | **Contact Us** |
| Target | `contacts` page (`wp_pages` row) |
| Wording rationale | "Contact Us" replaces the awkward "Contacts/Mails" from the archive — it is the standard website convention. It is a direct link (not a dropdown) because the contacts page is a single destination; the webmail login is moved to the footer. |

---

#### 10. Apply Now (CTA button)

| Property | Value |
| --- | --- |
| Type | CTA button (visually distinct, filled background) |
| Label | **Apply Now** |
| Target | `medical-school-application-form` page (`wp_pages` row) |
| Placement | Rightmost element in the header bar, separated from the nav links |
| Wording rationale | "Apply Now" is an action-oriented label that creates urgency and directs prospective nursing-school students straight to the application workflow. It mirrors the pattern of placing a single high-conversion CTA at the end of the navigation bar, visually separated from the informational links. |

---

### Header visual summary

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  [crest] OLLMH        Home  About Us ▾  Services ▾  Departments ▾       │
│  Our Lady of Lourdes  Projects & Community ▾  Nursing School ▾  News     │
│  Mwea Hospital        Events  Contact Us              [  Apply Now  ]    │
└──────────────────────────────────────────────────────────────────────────────┘
```

Dropdown example (About Us):

```
  About Us ▾
  ┌──────────────────────────┐
  │  About OLLMH & Location  │
  │  Administration &        │
  │    Governance            │
  │  Our Philosophy of Care  │
  │  Our Staff & Capacity    │
  └──────────────────────────┘
```

Mobile (off-canvas):

```
  ┌──────────────────────────────────┐
  │  [crest] OLLMH         [ ☰ ]    │
  ├──────────────────────────────────┤
  │  (hamburger panel slides in)     │
  │  Home                             │
  │  About Us ▸                       │
  │  Services ▸                       │
  │  Departments ▸                    │
  │  Projects & Community ▸           │
  │  Nursing School ▸                 │
  │  News                             │
  │  Events                           │
  │  Contact Us                       │
  │  ┌──────────────────────────┐    │
  │  │      Apply Now           │    │
  │  └──────────────────────────┘    │
  └──────────────────────────────────┘
```

---

## Footer

### Layout arrangement

The footer is a multi-section block at the bottom of every page, arranged
top-to-bottom in four horizontal bands:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  BAND 1: Brand section (logo + tagline + description paragraph)             │
├──────────────────────────────────────────────────────────────────────────────┤
│  BAND 2: Newsletter signup (heading + email input + subscribe button)       │
├────────────────┬──────────────────┬──────────────────┬──────────────────────┤
│  BAND 3: Link columns (4 columns side by side)                             │
│  Quick Links    │  Our Services    │  Support         │  Contact             │
├────────────────┴──────────────────┴──────────────────┴──────────────────────┤
│  BAND 4: Legal links row (Privacy Policy · Terms of Service · Data          │
│          Protection)                                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│  BAND 5: Bottom bar (copyright · accreditation badge · builder credit)     │
└──────────────────────────────────────────────────────────────────────────────┘
```

1. **Band 1 — Brand section**: the hospital logo, site name, tagline, and a
   short descriptive paragraph. This is the full-width top band of the footer.
2. **Band 2 — Newsletter signup**: a heading ("Stay Updated"), a one-line
   description, an email input field, and a subscribe button — all on one row.
   Below the form, a small privacy/terms consent line.
3. **Band 3 — Link columns**: four columns of links, side by side on desktop
   and stacked on mobile. Each column has a heading and a vertical list of
   links.
4. **Band 4 — Legal links**: a centered horizontal row of legal page links.
5. **Band 5 — Bottom bar**: copyright notice on the left, accreditation badge
   in the center, and builder credit on the right.

On mobile (≤ 768px) all bands stack vertically; the four link columns become
accordion sections.

### Design principles

- **No "Electoral Positions" section** — this section type is explicitly
  excluded; it is not relevant to a hospital website.
- **Brand-first**: the footer opens with the hospital's identity (logo +
  description), reinforcing the brand after the page content ends.
- **Newsletter prominence**: the signup form gets its own band (Band 2)
  immediately below the brand section, making it prominent without competing
  with the link columns.
- **Column balance**: each of the four link columns serves a distinct purpose
  — navigation, services, support, and contact — so no column is overloaded.
- **Legal separation**: legal links are in their own band (Band 4), distinct
  from the navigational link columns, so they are easy to find without being
  confused with site content.
- **Bottom bar attribution**: the bottom bar carries the copyright,
  accreditation, and credit in a single full-width strip.

### Footer data source

Footer link columns are stored as rows in `wp_menu_items` with
`menu_area = 'footer'`. The contact details (address, phone, email, hours)
are stored in the `wp_contact_channels` table (defined in
[`pages/contacts.md`](./pages/contacts.md)) and rendered directly into the
Contact column. Newsletter subscribers are stored in the
`wp_newsletter_subscribers` table (defined in
[`pages/news/index.md`](./pages/news/index.md)).

---

### Footer structure — band by band

#### Band 1: Brand section

Full-width, centered or left-aligned.

| # | Element | Content | Placement |
| --- | --- | --- | --- |
| 1.1 | Logo | Hospital crest / cross mark (same as header) | Left of text |
| 1.2 | Site name | **OLLMH** | Bold, primary colour |
| 1.3 | Tagline | **Our Lady of Lourdes Mwea Hospital** | Beneath site name, muted |
| 1.4 | Description | "Compassionate, faith-based healthcare serving the Mwea community and beyond. Offering inpatient and outpatient services, specialist clinics, a nursing school, and community outreach programs." | Full paragraph beneath the logo block |

**Wording rationale:**
- The description summarizes the hospital's mission and scope in one sentence,
  giving footer visitors an immediate understanding of what OLLMH is and does.

---

#### Band 2: Newsletter signup

Full-width, centered.

| # | Element | Content | Placement |
| --- | --- | --- | --- |
| 2.1 | Heading | **Stay Updated** | Above the form |
| 2.2 | Description | "Get the latest news, announcements, and event updates from OLLMH." | Beneath the heading |
| 2.3 | Email input | Placeholder: "Enter your email address" | Left of the button |
| 2.4 | Subscribe button | **Subscribe** | Right of the input, filled button style |
| 2.5 | Consent line | "By subscribing you agree to our Privacy Policy and Terms of Service." | Beneath the form, small text with links |

**Wording rationale:**
- "Stay Updated" is a clear, action-adjacent heading that tells the visitor
  what they gain by subscribing.
- The description specifies what they will receive (news, announcements,
  events) — setting expectations.
- "Subscribe" on the button is the standard label for email list signup.
- The consent line with linked legal pages mirrors professional compliance
  practice.

---

#### Band 3: Link columns

Four columns, side by side on desktop.

##### Column 1: Quick Links

Mirrors the main navigation, giving footer visitors a quick path to any
top-level section.

| # | Type | Content / Label | Target page |
| --- | --- | --- | --- |
| 1.1 | **Heading** | **Quick Links** | — |
| 1.2 | Link | Home | `wp_pages.id` (home) |
| 1.3 | Link | About Us | `wp_pages.id` (about-ollmh-location) |
| 1.4 | Link | Services | `wp_pages.id` (out-patient-dept) |
| 1.5 | Link | Departments | `wp_pages.id` (ollmh-departments) |
| 1.6 | Link | Projects & Community | `wp_pages.id` (community-support) |
| 1.7 | Link | Nursing School | `wp_pages.id` (about-nursing-school) |
| 1.8 | Link | News | `/news/` (listing page) |
| 1.9 | Link | Events | `/events/` (listing page) |
| 1.10 | Link | Contact Us | `wp_pages.id` (contacts) |
| 1.11 | Link | Apply Now | `wp_pages.id` (medical-school-application-form) |

**Wording rationale:**
- "Quick Links" is a standard footer column heading that signals these are
  shortcuts to the main site sections.
- The labels match the header menu labels exactly, so visitors recognize the
  same pages regardless of where they navigate from.
- "Apply Now" is included here as well as in the header CTA, because footer
  visitors may decide to apply after reading a page's content.

---

##### Column 2: Our Services

Links to the clinical service pages and departments.

| # | Type | Content / Label | Target page |
| --- | --- | --- | --- |
| 2.1 | **Heading** | **Our Services** | — |
| 2.2 | Link | Inpatient Department | `in-patient-dept` |
| 2.3 | Link | Outpatient Department | `out-patient-dept` |
| 2.4 | Link | Wards | `wards` |
| 2.5 | Link | Special Medical Services | `special-medical-services` |
| 2.6 | Link | Clinic Days & Schedule | `clinic-days` |
| 2.7 | Link | All Departments | `ollmh-departments` |
| 2.8 | Link | OLLMH Outlook (Photo Gallery) | `ollmh-outlook` |

**Wording rationale:**
- "Our Services" as the heading is warm and possessive, consistent with a
  hospital's patient-first tone.
- The link labels match the header sub-menu labels exactly.
- "All Departments" and "OLLMH Outlook (Photo Gallery)" are included here
  because they are functionally related to services — a visitor looking for a
  specific clinic or ward may think to look under "Services" in the footer.

---

##### Column 3: Support

Links to visitor/patient support resources.

| # | Type | Content / Label | Target page | Notes |
| --- | --- | --- | --- | --- |
| 3.1 | **Heading** | **Support** | — | |
| 3.2 | Link | **Patient Information** | `patient-information` | New page: admission guidelines, what to bring, visiting hours, patient rights. `wp_pages` row, `page_type = 'generic'`. |
| 3.3 | Link | **FAQ** | `faq` | New page: frequently asked questions about services, billing, appointments. `wp_pages` row, `page_type = 'generic'`. |
| 3.4 | Link | **Clinic Days & Schedule** | `clinic-days` | Quick access to the clinic calendar from the support column. |
| 3.5 | Link | **Send Us a Message** | `contacts` | Internal link to the contact form page. |
| 3.6 | Link | **Webmail Login** | External URL | External link to the hospital's webmail portal for staff. |

**Wording rationale:**
- "Support" is a concise heading that signals help resources for visitors and
  patients.
- "Patient Information" is a standard hospital website section covering
  practical guidance for patients and visitors.
- "FAQ" is universally understood and reduces repetitive phone enquiries.
- "Clinic Days & Schedule" is cross-listed here because patients looking for
  support often need to know when a clinic is open.
- "Send Us a Message" is an action-oriented label for the contact form.
- "Webmail Login" gives staff a footer-level shortcut to their email.

---

##### Column 4: Contact

Displays the hospital's contact details directly (not as links, except where
noted). This is the rightmost column for immediate visibility.

| # | Type | Content / Label | Details |
| --- | --- | --- | --- |
| 4.1 | **Heading** | **Contact** | Column heading. |
| 4.2 | Email | General enquiries email | `mailto:` link, sourced from `wp_contact_channels` (type = 'email'). |
| 4.3 | Email | Appointments / bookings email (if separate) | `mailto:` link, sourced from `wp_contact_channels` (type = 'email'). |
| 4.4 | Phone | Primary phone number | `tel:` link, sourced from `wp_contact_channels` (type = 'phone'). |
| 4.5 | Phone | Emergency / ambulance number (if separate) | `tel:` link, sourced from `wp_contact_channels` (type = 'emergency'). |
| 4.6 | Address | Physical address | Multi-line plain text, sourced from `wp_contact_channels` (type = 'address'). Example: "Our Lady of Lourdes Mwea Hospital\nMwea, Kirinyaga County\nKenya" |
| 4.7 | Map link | "View on Map" | External link to Google Maps pin for the hospital location. Opens in a new tab. Rendered as a small text link beneath the address. |
| 4.8 | Hours | Operating hours | Multi-line plain text. Example: "Outpatient: Mon–Sat, 7am–8pm\nEmergency: 24 hours\nClinics: By appointment" |
| 4.9 | Social icons | Facebook · YouTube · X (Twitter) | Row of social media icon links, sourced from `wp_settings` (`social_facebook`, `social_youtube`, `social_twitter` settings). Each icon is an inline SVG (see [`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md) → Icons) that links to the hospital's social profile, opening in a new tab with `rel="noopener noreferrer"`. Rendered beneath the hours. |

**Wording rationale:**
- "Contact" as the heading is short and direct.
- Displaying emails, phones, address, and hours directly in the footer means a
  visitor in need of urgent contact information does not have to click through
  to another page.
- The `tel:` and `mailto:` links are clickable on mobile devices for immediate
  action.
- Operating hours are included because patients frequently need to know when
  services are available — this is one of the most sought-after pieces of
  information on a hospital website.
- The "View on Map" link gives visitors a one-click path to directions,
  especially useful on mobile devices where the Google Maps app can open
  directly.
- Social media icons (Facebook, YouTube, X) are included in the Contact column
  so visitors can connect with the hospital on their preferred platform. The
  icons use inline SVGs (no icon font library — see
  [`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md)) and open in a
  new tab with `rel="noopener noreferrer"` for security. The profile URLs are
  sourced from `wp_settings` (`social_facebook`, `social_youtube`,
  `social_twitter`), so they can be updated from the admin without code
  changes.

---

#### Band 4: Legal links

A centered horizontal row of legal page links, visually separated from the
link columns above.

| # | Content / Label | Target page |
| --- | --- | --- |
| 4.1 | **Privacy Policy** | `privacy-policy` (`wp_pages` row, `page_type = 'generic'`) |
| 4.2 | **Terms of Service** | `terms-of-service` (`wp_pages` row, `page_type = 'generic'`) |
| 4.3 | **Data Protection** | `data-protection` (`wp_pages` row, `page_type = 'generic'`) |

**Wording rationale:**
- "Privacy Policy", "Terms of Service", and "Data Protection" are standard
  legal pages required for professional websites, especially those that
  collect patient information and newsletter subscriptions.
- Placing them in their own band (rather than inside a link column) separates
  legal notices from navigational content, following professional web design
  conventions.
- These pages will be created as new `wp_pages` rows during the WordPress
  build.

---

#### Band 5: Bottom bar

A full-width strip at the very bottom of the footer.

| # | Position | Content / Label | Details |
| --- | --- | --- | --- |
| 5.1 | Left | **Copyright notice** | "Copyright © 2024 Our Lady of Lourdes Mwea Hospital. All rights reserved." (year auto-updated server-side). |
| 5.2 | Center | **Accreditation badge** | Text badge indicating accreditation, e.g. "Nursing Council of Kenya Accredited" or "KMPDC Accredited". Rendered as a small pill/badge element. |
| 5.3 | Right | **Builder credit** | "Built with ♥ by [Builder Name]" — a small, muted credit link. |

**Wording rationale:**
- The copyright notice uses the full hospital name for formality.
- The accreditation badge in the center reinforces the hospital's credentials
  — a trust signal for patients and prospective students.
- The builder credit on the right is a standard web design convention.

---

### Footer visual summary

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  [crest]  OLLMH                                                              │
│           Our Lady of Lourdes Mwea Hospital                                   │
│                                                                              │
│  Compassionate, faith-based healthcare serving the Mwea community and        │
│  beyond. Offering inpatient and outpatient services, specialist clinics,     │
│  a nursing school, and community outreach programs.                          │
├──────────────────────────────────────────────────────────────────────────────┤
│  Stay Updated                                                                │
│  Get the latest news, announcements, and event updates from OLLMH.           │
│  [ Enter your email address          ] [ Subscribe ]                         │
│  By subscribing you agree to our Privacy Policy and Terms of Service.        │
├──────────────────┬──────────────────┬──────────────────┬────────────────────┤
│  Quick Links     │  Our Services    │  Support         │  Contact           │
│                  │                  │                  │                    │
│  Home            │  Inpatient Dept. │  Patient         │  [email]           │
│  About Us        │  Outpatient Dept.│    Information   │  [email]           │
│  Services        │  Wards           │  FAQ             │  [phone]           │
│  Departments     │  Special Medical │  Clinic Days &   │  [phone]           │
│  Projects &      │    Services      │    Schedule      │  [address          │
│    Community     │  Clinic Days &   │  Send Us a       │   line 1           │
│  Nursing School  │    Schedule      │    Message       │   line 2           │
│  News            │  All Departments │  Webmail Login   │   line 3]          │
│  Events          │  OLLMH Outlook   │                  │  View on Map →     │
│  Contact Us      │    (Photo Gallery)│                  │  [hours            │
│  Apply Now       │                  │                  │   line 1           │
│                  │                  │                  │   line 2]          │
│                  │                  │                  │  [f] [▶] [𝕏]       │
├──────────────────┴──────────────────┴──────────────────┴────────────────────┤
│              Privacy Policy  ·  Terms of Service  ·  Data Protection         │
├──────────────────────────────────────────────────────────────────────────────┤
│ Copyright © 2024 OLLMH.   [NCK Accredited]              Built by [Name]     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Menu items to database mapping

The following table maps every header and footer menu item to its
`wp_menu_items` row, showing how the information architecture plugs into the
database schema.

### Header menu items

| Menu area | Parent label | Item label | `page_id` target | `external_url` | Notes |
| --- | --- | --- | --- | --- | --- |
| header | — | Home | `wp_pages.id` (home) | NULL | Direct link |
| header | About Us | About OLLMH & Location | `wp_pages.id` (about-ollmh-location) | NULL | Dropdown child |
| header | About Us | Administration & Governance | `wp_pages.id` (administration) | NULL | Dropdown child |
| header | About Us | Our Philosophy of Care | `wp_pages.id` (philosophy-of-care) | NULL | Dropdown child |
| header | About Us | Our Staff & Capacity | `wp_pages.id` (hr-capacity-staff) | NULL | Dropdown child |
| header | Services | Inpatient Department | `wp_pages.id` (in-patient-dept) | NULL | Dropdown child |
| header | Services | Outpatient Department | `wp_pages.id` (out-patient-dept) | NULL | Dropdown child |
| header | Services | Wards | `wp_pages.id` (wards) | NULL | Dropdown child |
| header | Services | Special Medical Services | `wp_pages.id` (special-medical-services) | NULL | Dropdown child |
| header | Services | Clinic Days & Schedule | `wp_pages.id` (clinic-days) | NULL | Dropdown child |
| header | Departments | All Departments | `wp_pages.id` (ollmh-departments) | NULL | Dropdown child |
| header | Departments | OLLMH Outlook (Photo Gallery) | `wp_pages.id` (ollmh-outlook) | NULL | Dropdown child |
| header | Projects & Community | Development Projects | `wp_pages.id` (development-projects) | NULL | Dropdown child |
| header | Projects & Community | Self-Sustainability Projects | `wp_pages.id` (self-sustainability-projects) | NULL | Dropdown child |
| header | Projects & Community | Community Support | `wp_pages.id` (community-support) | NULL | Dropdown child |
| header | Projects & Community | S.M.I Community | `wp_pages.id` (smi-community) | NULL | Dropdown child |
| header | Projects & Community | Upcoming Projects | `wp_pages.id` (upcoming-projects) | NULL | Dropdown child |
| header | Nursing School | About the Nursing School | `wp_pages.id` (about-nursing-school) | NULL | Dropdown child |
| header | Nursing School | Application Form | `wp_pages.id` (medical-school-application-form) | NULL | Dropdown child |
| header | — | News | `wp_pages.id` (news listing) | NULL | Direct link |
| header | — | Events | `wp_pages.id` (events listing) | NULL | Direct link |
| header | — | Contact Us | `wp_pages.id` (contacts) | NULL | Direct link |
| header | — | Apply Now | `wp_pages.id` (medical-school-application-form) | NULL | CTA button (CSS class `menu-item-cta`) |

### Footer menu items

| Menu area | Column / band | Item label | `page_id` target | `external_url` | Notes |
| --- | --- | --- | --- | --- | --- |
| footer | Quick Links | Home | `wp_pages.id` (home) | NULL | |
| footer | Quick Links | About Us | `wp_pages.id` (about-ollmh-location) | NULL | |
| footer | Quick Links | Services | `wp_pages.id` (out-patient-dept) | NULL | |
| footer | Quick Links | Departments | `wp_pages.id` (ollmh-departments) | NULL | |
| footer | Quick Links | Projects & Community | `wp_pages.id` (community-support) | NULL | |
| footer | Quick Links | Nursing School | `wp_pages.id` (about-nursing-school) | NULL | |
| footer | Quick Links | News | `wp_pages.id` (news listing) | NULL | |
| footer | Quick Links | Events | `wp_pages.id` (events listing) | NULL | |
| footer | Quick Links | Contact Us | `wp_pages.id` (contacts) | NULL | |
| footer | Quick Links | Apply Now | `wp_pages.id` (medical-school-application-form) | NULL | |
| footer | Our Services | Inpatient Department | `wp_pages.id` (in-patient-dept) | NULL | |
| footer | Our Services | Outpatient Department | `wp_pages.id` (out-patient-dept) | NULL | |
| footer | Our Services | Wards | `wp_pages.id` (wards) | NULL | |
| footer | Our Services | Special Medical Services | `wp_pages.id` (special-medical-services) | NULL | |
| footer | Our Services | Clinic Days & Schedule | `wp_pages.id` (clinic-days) | NULL | |
| footer | Our Services | All Departments | `wp_pages.id` (ollmh-departments) | NULL | |
| footer | Our Services | OLLMH Outlook (Photo Gallery) | `wp_pages.id` (ollmh-outlook) | NULL | |
| footer | Support | Patient Information | `wp_pages.id` (patient-information) | NULL | New page |
| footer | Support | FAQ | `wp_pages.id` (faq) | NULL | New page |
| footer | Support | Clinic Days & Schedule | `wp_pages.id` (clinic-days) | NULL | |
| footer | Support | Send Us a Message | `wp_pages.id` (contacts) | NULL | |
| footer | Support | Webmail Login | NULL | (external webmail URL) | |
| footer | Contact | (emails, phones, address, hours) | — | — | Rendered from `wp_contact_channels`, not `wp_menu_items` |
| footer | Legal band | Privacy Policy | `wp_pages.id` (privacy-policy) | NULL | New page |
| footer | Legal band | Terms of Service | `wp_pages.id` (terms-of-service) | NULL | New page |
| footer | Legal band | Data Protection | `wp_pages.id` (data-protection) | NULL | New page |

### New pages to create

The following pages do not exist in the current documentation and must be
created as new `wp_pages` rows during the WordPress build:

| Page | Slug | `page_type` | Referenced in |
| --- | --- | --- | --- |
| Patient Information | `patient-information` | `generic` | Footer → Support column |
| FAQ | `faq` | `generic` | Footer → Support column |
| Privacy Policy | `privacy-policy` | `generic` | Footer → Legal band, Newsletter consent |
| Terms of Service | `terms-of-service` | `generic` | Footer → Legal band, Newsletter consent |
| Data Protection | `data-protection` | `generic` | Footer → Legal band |

---

## Changes from the previous header/footer structure

This section summarizes what changed from the prior version of this document
(commit `901d64e`), which used a different layout pattern.

| Prior structure | New structure | Rationale |
| --- | --- | --- |
| Header had no brand tagline; logo was just a placeholder | Header brand block now includes site name + full hospital name as tagline | Reinforces brand identity; first-time visitors immediately see the full hospital name. |
| Header had 8 top-level items, with "News & Events" as a combined parent dropdown | Header now has 10 items: News and Events are separate top-level direct links | Separating News and Events gives each content type its own discoverable entry point; they are direct links (not dropdowns) because the listing pages are the drill-down starting points. |
| Header had no CTA button; "Contact Us" was a dropdown with Webmail Login | Header now ends with a distinct "Apply Now" CTA button; Contact Us is a direct link; Webmail Login moved to footer | A single high-conversion CTA at the end of the nav bar is a proven pattern; Contact Us as a direct link is simpler; webmail is a staff utility that belongs in the footer, not the main nav. |
| Footer had 4 columns (Contact, About OLLMH, Our Services, Projects & Community) + bottom bar | Footer now has 5 bands: Brand section, Newsletter signup, 4 link columns (Quick Links, Our Services, Support, Contact), Legal links band, Bottom bar | The brand section + newsletter band give the footer a richer, more professional structure; the 4 columns are reorganized for better balance. |
| Footer had no newsletter signup | Footer now has a dedicated newsletter signup band (Band 2) with email input, subscribe button, and consent line | Newsletter signup is a key engagement tool; giving it its own band makes it prominent without cluttering the link columns. |
| Footer had no legal links band | Footer now has a dedicated legal links band (Band 4) with Privacy Policy, Terms of Service, and Data Protection | Separating legal notices from navigational content follows professional web design conventions; Data Protection is added for compliance. |
| Footer had no brand description | Footer now opens with a brand description paragraph | Reinforces the hospital's mission and scope for visitors who scroll to the bottom. |
| Footer bottom bar had Privacy Policy, Terms, News & Events, Webmail Login | Footer bottom bar now has copyright, accreditation badge, and builder credit only | Legal links moved to their own band; News/Events/Webmail are in the link columns; the bottom bar is now purely attribution. |
| Footer had no accreditation badge | Footer bottom bar now includes an accreditation badge (e.g. "NCK Accredited") | Trust signal for patients and prospective students. |
| Footer Contact column had "View on Map" and "Send Us a Message" links | Footer Contact column now displays emails, phones, address, and hours directly | Visitors get complete contact information without clicking; "Send Us a Message" moved to the Support column. |
| Footer had no Support column | Footer now has a Support column with Patient Information, FAQ, Clinic Days, Contact form, Webmail Login | Gives patients and visitors a dedicated help-resources section, a standard pattern for service-oriented websites. |
| No "Electoral Positions" section | Confirmed: no such section exists | This section type is not relevant to a hospital website. |

---

## Changes from the archived navigation

This section summarizes how the new structure improves on the archived
navigation (documented in [`header-footer-links.md`](./header-footer-links.md)).

| Archived issue | Resolution in new structure |
| --- | --- |
| "New & Events" typo; page was a nursing-school advert, not a news feed | Fixed to separate "News" and "Events" top-level items; each has its own listing page and per-entry standalone pages under `news/` and `events/`. |
| "Nursing Sch-" truncated label | Expanded to "Nursing School". |
| "Medical Sch- Application Form" truncated label | Shortened to "Application Form" (dropdown) and "Apply Now" (CTA button). |
| "Contacts/Mails" unclear label | Replaced with "Contact Us" as a direct link; webmail moved to footer Support column. |
| "Features" group mixed departments, a gallery, and a community page | "Departments" (All Departments + Outlook Gallery) and "S.M.I Community" (moved to Projects & Community) are now in logically coherent groups. |
| "Self Sustinabilbity Projects" typo | Fixed to "Self-Sustainability Projects". |
| "In patient Dept" / "Out Patient Dept" abbreviations | Expanded to "Inpatient Department" / "Outpatient Department". |
| "HR-Capacity (Staff)" awkward label | Reworded to "Our Staff & Capacity". |
| "Ollmh Departments" redundant hospital name prefix | Shortened to "All Departments". |
| "Login" link in main menu (unclear destination) | Removed; staff authentication via "Webmail Login" in footer and WordPress admin bar. |
| Footer "Send Your onours" typo and dead link | Replaced with "Send Us a Message" in the Support column. |
| Footer "Future Projection" unclear heading | Replaced with "Our Services" column (clearer, service-focused). |
| Footer "Core Values" column with all dead links | Replaced with "Support" column (real, navigable links to Patient Information, FAQ, etc.). |
| No privacy policy or terms of service links | Added as a dedicated Legal band with Privacy Policy, Terms of Service, and Data Protection. |
| No newsletter signup | Added as a dedicated band (Band 2) with email input, subscribe button, and consent line. |
| No brand description in footer | Added a description paragraph in the brand section (Band 1). |
| No accreditation badge | Added to the bottom bar as a trust signal. |
| No "Electoral Positions" section | Confirmed: no such section exists in the new structure. |
