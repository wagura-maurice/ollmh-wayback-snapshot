# WordPress User Roles — Default, OLLMH Application & Custom Roles

> This document confirms the **default WordPress user roles** as defined by
> the official WordPress documentation
> ([wordpress.org/documentation/article/roles-and-capabilities](https://wordpress.org/documentation/article/roles-and-capabilities/)),
> explains how each role functions, maps each to the specific operational
> needs of the **Our Lady of Lourdes Mwea Hospital (OLLMH)** website,
> identifies which default roles are actively utilized versus redundant, and
> defines the **custom roles** the OLLMH rebuild requires.
>
> All custom roles and their admin-sidebar capabilities are cross-referenced
> with [`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md).

---

## Table of contents

1. [Confirmation of default WordPress roles](#confirmation-of-default-wordpress-roles)
2. [How each default role functions](#how-each-default-role-functions)
3. [OLLMH website — purpose and content structure](#ollmh-website--purpose-and-content-structure)
4. [Mapping default roles to OLLMH operational needs](#mapping-default-roles-to-ollmh-operational-needs)
5. [Which default roles are utilized vs. redundant](#which-default-roles-are-utilized-vs-redundant)
6. [Custom roles for OLLMH](#custom-roles-for-ollmh)
7. [Full capability matrix (default + custom)](#full-capability-matrix-default--custom)
8. [Role assignment workflow](#role-assignment-workflow)
9. [Registration code reference](#registration-code-reference)

---

## Confirmation of default WordPress roles

WordPress ships with **six** pre-defined roles, not five. The user's list
(Administrator, Editor, Author, Contributor, Subscriber) is correct for a
**single-site installation**. The sixth role — **Super Admin** — exists only
in **Multisite** installations and is omitted from single-site discussions.

| # | Role | Slug | Exists on single-site? | Source |
|---|---|---|---|---|
| 1 | **Super Admin** | — | No (Multisite only) | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#super-admin) |
| 2 | **Administrator** | `administrator` | Yes | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#administrator) |
| 3 | **Editor** | `editor` | Yes | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#editor) |
| 4 | **Author** | `author` | Yes | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#author) |
| 5 | **Contributor** | `contributor` | Yes | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#contributor) |
| 6 | **Subscriber** | `subscriber` | Yes | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#subscriber) |

**Confirmed:** The five roles the user listed — Administrator, Editor,
Author, Contributor, Subscriber — are the five default roles present on a
standard single-site WordPress installation. Super Admin is the sixth,
Multisite-only role.

On a single-site install, the Administrator effectively holds all Super
Admin capabilities (including `update_core`, `install_plugins`,
`edit_themes`, `create_users`, `delete_users`, `unfiltered_html`), so the
distinction is moot for OLLMH, which will be a single-site installation.

---

## How each default role functions

### Super Admin (Multisite only)

- **Slug:** none (assigned at the network level)
- **Capabilities:** Every capability in WordPress, plus the Multisite-only
  network capabilities: `manage_network`, `manage_sites`,
  `manage_network_users`, `manage_network_themes`, `manage_network_plugins`,
  `manage_network_options`, `create_sites`, `delete_sites`,
  `upgrade_network`, `setup_network`.
- **Function:** Can create and delete sites in the network, manage network
  users, manage network-wide plugins and themes, and access every
  admin feature on every site in the network.
- **Relevance to OLLMH:** **None.** OLLMH is a single-site installation.
  This role will not exist.

### Administrator

- **Slug:** `administrator`
- **Capabilities (single-site):** All capabilities. The full list includes:
  `activate_plugins`, `delete_others_pages`, `delete_others_posts`,
  `delete_pages`, `delete_posts`, `delete_private_pages`,
  `delete_private_posts`, `delete_published_pages`,
  `delete_published_posts`, `edit_dashboard`, `edit_others_pages`,
  `edit_others_posts`, `edit_pages`, `edit_posts`, `edit_private_pages`,
  `edit_private_posts`, `edit_published_pages`, `edit_published_posts`,
  `edit_theme_options`, `edit_themes`, `edit_plugins`, `edit_files`,
  `edit_users`, `export`, `import`, `list_users`, `manage_categories`,
  `manage_links`, `manage_options`, `moderate_comments`, `promote_users`,
  `publish_pages`, `publish_posts`, `read_private_pages`,
  `read_private_posts`, `read`, `remove_users`, `switch_themes`,
  `upload_files`, `customize`, `delete_site`, `update_core`,
  `update_plugins`, `update_themes`, `install_plugins`, `install_themes`,
  `delete_themes`, `delete_plugins`, `add_users`, `create_users`,
  `delete_users`, `unfiltered_html`.
- **Function:** Full, unrestricted access to every administration feature
  within a single site. Can install/delete plugins and themes, update
  WordPress core, manage all users, manage all settings, edit all content
  (posts and pages by anyone), moderate comments, and upload files.
- **Hierarchy:** Inherits all capabilities of Editor, Author, Contributor,
  and Subscriber.

### Editor

- **Slug:** `editor`
- **Capabilities:** `delete_others_pages`, `delete_others_posts`,
  `delete_pages`, `delete_posts`, `delete_private_pages`,
  `delete_private_posts`, `delete_published_pages`,
  `delete_published_posts`, `edit_others_pages`, `edit_others_posts`,
  `edit_pages`, `edit_posts`, `edit_private_pages`, `edit_private_posts`,
  `edit_published_pages`, `edit_published_posts`, `manage_categories`,
  `manage_links`, `moderate_comments`, `publish_pages`, `publish_posts`,
  `read`, `read_private_pages`, `read_private_posts`, `unfiltered_html`
  (single-site), `upload_files`.
- **Function:** Can publish and manage posts and pages — including those
  authored by other users. Can moderate comments, manage categories and
  links, and upload files. **Cannot** manage site settings (`manage_options`),
  install/edit plugins or themes, or manage users.
- **Key distinction from Administrator:** No `manage_options`, no
  `edit_theme_options`, no plugin/theme management, no user management.

### Author

- **Slug:** `author`
- **Capabilities:** `delete_posts`, `delete_published_posts`, `edit_posts`,
  `edit_published_posts`, `publish_posts`, `read`, `upload_files`.
- **Function:** Can write, publish, edit, and delete **their own** posts.
  Can upload files (images). **Cannot** edit others' posts, edit pages,
  moderate comments, manage categories, or access site settings.
- **Key distinction from Editor:** No `edit_others_posts`, no `edit_pages`,
  no `moderate_comments`, no `manage_categories`.

### Contributor

- **Slug:** `contributor`
- **Capabilities:** `delete_posts`, `edit_posts`, `read`.
- **Function:** Can write and manage **their own** posts but **cannot
  publish** them. A Contributor's posts remain in "Pending Review" until an
  Editor or Administrator publishes them. **Cannot** upload files (no
  `upload_files` capability), so they cannot add images to their posts.
- **Key distinction from Author:** No `publish_posts`, no
  `edit_published_posts`, no `upload_files`.

### Subscriber

- **Slug:** `subscriber`
- **Capabilities:** `read`.
- **Function:** Can only log in and manage their own profile. **Cannot**
  write posts, edit pages, upload files, moderate comments, or access any
  admin feature beyond their profile page.
- **Typical use:** Sites that require login to read content, or to allow
  users to change their password / email without admin intervention.

---

## OLLMH website — purpose and content structure

The OLLMH website is a **hospital information and services portal** for Our
Lady of Lourdes Mwea Hospital, a Catholic faith-based healthcare facility in
Mwea, Kenya. It is **not a blog** — it is a structured institutional website
with:

| Content domain | Custom tables | Admin section |
|---|---|---|
| News articles | `wp_news_articles`, `wp_news_categories`, `wp_news_tags`, `wp_news_comments`, `wp_news_article_revisions`, `wp_news_article_media`, `wp_news_article_tags` | News |
| Events | `wp_events`, `wp_event_categories`, `wp_event_registrations`, `wp_event_media` | Events |
| Departments | `wp_departments`, `wp_department_showcase`, `wp_department_photos` | Departments |
| Wards & Inpatient | `wp_wards`, `wp_ward_media`, `wp_ward_bed_status`, `wp_inpatient_dept_sections`, `wp_inpatient_admission_enquiries`, `wp_mortuary_services` | Wards & Inpatient |
| Clinics & OPD | `wp_clinics`, `wp_clinic_schedules`, `wp_clinic_schedule_exceptions`, `wp_clinic_bookings`, `wp_opd_facilities`, `wp_opd_operating_hours`, `wp_opd_consultation_rooms`, `wp_opd_appointments` | Clinics & OPD |
| Special Medical Services | `wp_special_medical_services`, `wp_service_specialists`, `wp_service_equipment`, `wp_service_enquiries` | Special Medical Services |
| Staff & HR | `wp_staff`, `wp_staff_cadres`, `wp_hr_capacity_stats`, `wp_job_vacancies` | Staff & HR |
| Nursing School | `wp_nursing_school_profile`, `wp_nursing_programmes`, `wp_nursing_intakes`, `wp_nursing_facilities` | Nursing School |
| Applications | `wp_applicants`, `wp_applications`, `wp_application_documents`, `wp_application_referees`, `wp_application_reviews`, `wp_application_payments`, `wp_application_status_history`, `wp_application_notifications`, `wp_application_form_downloads` | Applications |
| Projects | 12 tables (development, sustainability, upcoming) | Projects |
| Community | 9 tables (community programs, SMI) | Community |
| Gallery | `wp_outlook_albums`, `wp_outlook_gallery_items` | Gallery |
| Home page | `wp_home_slides`, `wp_home_feature_blocks`, `wp_home_in_focus_items`, `wp_home_news_promos` | Home Page |
| Pages | `wp_pages`, `wp_page_media` | Pages |
| Settings | `wp_location_info`, `wp_contact_channels`, `wp_contact_submissions`, `wp_about_facts`, `wp_about_milestones`, `wp_care_statements`, `wp_care_values`, `wp_governance_bodies`, `wp_governance_members` | Settings |
| Platform core | `wp_users`, `wp_media_assets`, `wp_menu_items` | Users, Media, Appearance |

**Total: 80 custom tables** across 16 content domains, managed via 15
Custom Post Types, custom taxonomies, settings pages, and management
screens (see [`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md)).

The site has **multiple staff types** who need different levels of admin
access: hospital administrators, HR managers, nursing school
administrators, admissions officers, receptionists, community program
coordinators, and content editors. The default WordPress roles do not map
cleanly to these operational roles.

---

## Mapping default roles to OLLMH operational needs

### Administrator → Hospital IT Administrator

| Aspect | Detail |
|---|---|
| **OLLMH role** | Hospital IT Administrator / Webmaster |
| **Who** | The IT staff member(s) responsible for the website infrastructure |
| **What they do** | Install/update plugins and themes, manage all users, configure all settings, manage all content, update WordPress core, access all admin features |
| **Default capabilities used** | All — the Administrator role is used as-is, no modifications needed |
| **Custom capabilities added** | All custom capabilities (`manage_applications`, `edit_clinics`, `edit_wards`, `edit_staff`, `edit_nursing`, `edit_projects`, `edit_community`, `edit_home_page`, `edit_special_services`, `edit_departments`, `edit_news_articles`, `edit_events`, `edit_gallery`) — Administrators get every custom capability |
| **Verdict** | **Actively utilized.** Essential. At least one Administrator account is required by WordPress itself (created during installation). |

### Editor → Content Editor / Communications Officer

| Aspect | Detail |
|---|---|
| **OLLMH role** | Content Editor / Communications Officer |
| **Who** | The staff member responsible for publishing news, events, and managing the photo gallery and home page content |
| **What they do** | Write and publish news articles, create events, manage event categories, moderate news comments, manage the photo gallery (albums + items), manage home page content (slides, feature blocks, in-focus items, news promos), edit static pages |
| **Default capabilities used** | `edit_posts`, `edit_others_posts`, `publish_posts`, `edit_pages`, `publish_pages`, `moderate_comments`, `manage_categories`, `upload_files`, `read`, `edit_published_posts`, `edit_published_pages`, `delete_posts`, `delete_others_posts`, `delete_published_posts`, `delete_pages`, `delete_others_pages`, `delete_published_pages` |
| **Custom capabilities added** | `edit_news_articles`, `edit_events`, `edit_gallery`, `edit_home_page`, `edit_departments` (for department showcase editing) |
| **What they CANNOT do** | Manage site settings, install plugins/themes, manage users, access clinical/HR/applications/community/staff sections |
| **Verdict** | **Actively utilized.** The Editor role is the backbone of the content management workflow. It is used as-is from WordPress core, with custom CPT capabilities added via `add_cap()`. |

### Author → Staff Author (limited content contributor)

| Aspect | Detail |
|---|---|
| **OLLMH role** | Staff Author — a staff member who contributes news articles or event posts but should not be able to edit others' content |
| **Who** | A nurse, doctor, or department head who occasionally writes a news article or posts an event but is not a full-time content editor |
| **What they do** | Write and publish their own news articles and events, upload images to accompany their posts |
| **Default capabilities used** | `edit_posts`, `publish_posts`, `edit_published_posts`, `delete_posts`, `delete_published_posts`, `upload_files`, `read` |
| **Custom capabilities added** | `edit_news_articles` (own only — mapped via `edit_published_news_articles` / `edit_others_news_articles` capability split), `edit_events` (own only) |
| **What they CANNOT do** | Edit others' posts, edit pages, moderate comments, manage categories, access any clinical/HR/applications/staff sections |
| **Verdict** | **Actively utilized, but with a narrow scope.** Useful for allowing department heads or clinical staff to contribute news without giving them editorial control over others' content. The capability mapping must ensure Authors get `edit_news_articles` (create own) but **not** `edit_others_news_articles`. |

### Contributor → Guest Writer / External Contributor

| Aspect | Detail |
|---|---|
| **OLLMH role** | Guest writer — an external contributor (e.g., a volunteer, a visiting medical student, a community member) who submits a news article for review but cannot publish it directly |
| **Who** | Non-staff contributors who should not have publishing authority |
| **What they do** | Write news articles (saved as "Pending Review"), which an Editor then reviews and publishes |
| **Default capabilities used** | `edit_posts`, `delete_posts`, `read` |
| **Custom capabilities added** | `edit_news_articles` (create own, pending review only — no `publish_news_articles` capability) |
| **What they CANNOT do** | Publish posts, upload files (no `upload_files` — this is a known limitation; images must be added by the reviewing Editor), edit others' content, access any other admin section |
| **Verdict** | **Marginally utilized.** Useful only if OLLMH plans to accept external article submissions. For a hospital website where content is primarily produced by staff, this role is likely **redundant** in practice. **Recommendation: keep the role registered (it's core) but do not assign it to any user unless external contributors are explicitly onboarded.** |

### Subscriber → Patient / Public User / Newsletter Subscriber

| Aspect | Detail |
|---|---|
| **OLLMH role** | Registered site user — a patient, community member, or newsletter subscriber who has created an account on the website |
| **Who** | Any public user who registers an account (e.g., to book clinic appointments online, to subscribe to the newsletter, to track an application status) |
| **What they do** | Log in, manage their own profile (name, email, password), view their appointment bookings, view their application status, manage their newsletter subscription preferences |
| **Default capabilities used** | `read` (only) |
| **Custom capabilities added** | None from the admin side. On the **front-end**, Subscribers get authenticated access to: their own `wp_clinic_bookings` records, their own `wp_opd_appointments`, their own `wp_applications` / `wp_applicants` profile, their own `wp_newsletter_subscribers` preferences. This is handled via front-end form shortcodes and `is_user_logged_in()` checks, not via admin capabilities. |
| **What they CANNOT do** | Access the WordPress admin dashboard (beyond their profile), write/edit any content, access any admin section |
| **Verdict** | **Actively utilized — but primarily on the front-end, not the admin.** Subscribers never see the admin sidebar. Their "role" is really an authentication identity for front-end interactions (booking appointments, applying to nursing school, managing newsletter preferences). This is the **default role for new user registrations** (set in Settings → General → "New User Default Role"). |

---

## Which default roles are utilized vs. redundant

| Default role | OLLMH utilization | Status | Assignment count (estimated) |
|---|---|---|---|
| **Super Admin** | Not applicable (single-site install) | **N/A — does not exist** | 0 |
| **Administrator** | Hospital IT admin / webmaster | **Actively utilized** | 1–3 |
| **Editor** | Content editor / communications officer | **Actively utilized** | 1–2 |
| **Author** | Staff author (department heads, clinical staff who contribute news) | **Actively utilized (narrow)** | 3–10 |
| **Contributor** | Guest writer / external contributor | **Redundant in practice** — keep registered but do not assign unless external contributors are explicitly onboarded | 0 (typically) |
| **Subscriber** | Patient / public user / newsletter subscriber | **Actively utilized (front-end only)** — default role for new registrations | 100+ (all registered public users) |

### Summary

- **3 default roles are actively utilized in the admin:** Administrator,
  Editor, Author.
- **1 default role is actively utilized but only on the front-end:**
  Subscriber (the default new-user role for patient/public registrations).
- **1 default role is redundant for OLLMH's current needs:** Contributor
  (kept registered but unassigned unless external writers are onboarded).
- **1 default role does not exist:** Super Admin (Multisite only; OLLMH is
  single-site).

### Why the default roles are insufficient

The five default roles are designed for a **blog/magazine workflow** (write
→ review → publish posts). OLLMH is a **hospital operations portal** with
domain-specific admin sections that have nothing to do with blog posts:

- A **receptionist** needs to manage clinic bookings and bed status but
  should not see news, events, or HR sections.
- An **HR manager** needs to manage staff records and job vacancies but
  should not see clinical or applications sections.
- A **nursing school administrator** needs to manage nursing programmes,
  intakes, and applications but should not see ward or clinic management.
- An **admissions officer** needs to manage the application pipeline but
  should not edit news or events.
- A **community coordinator** needs to manage community programs and SMI
  content but should not see clinical or HR sections.

None of these map to Administrator, Editor, Author, Contributor, or
Subscriber. The solution is to create **custom roles** with precisely
scoped capabilities.

---

## Custom roles for OLLMH

Six custom roles are defined, each scoped to a specific operational
function. All custom roles inherit the `read` capability (so users can log
in and see the dashboard) and `upload_files` where file management is part
of their job.

### 1. `hospital_admin` — Hospital Administrator

| Property | Value |
|---|---|
| **Slug** | `hospital_admin` |
| **Display name** | Hospital Administrator |
| **Who** | The hospital administrator or senior IT staff member who oversees the entire website |
| **Base role** | Clone of WordPress `administrator` |
| **Capabilities** | All default Administrator capabilities **plus** all custom capabilities |
| **Custom caps** | `manage_applications`, `edit_clinics`, `edit_wards`, `edit_staff`, `edit_nursing`, `edit_projects`, `edit_community`, `edit_home_page`, `edit_special_services`, `edit_departments`, `edit_news_articles`, `edit_events`, `edit_gallery`, `manage_hospital_info`, `manage_contact_channels`, `manage_about_content`, `manage_governance` |
| **Admin sidebar access** | All 20 top-level menus (full access) |
| **Notes** | This role is functionally identical to the WordPress Administrator. It exists as a **semantic label** so that the hospital's administrative user is clearly distinguished from a generic WordPress "administrator" in the user list. In practice, the default `administrator` role can be used instead — this custom role is optional. |

### 2. `hr_manager` — HR Manager

| Property | Value |
|---|---|
| **Slug** | `hr_manager` |
| **Display name** | HR Manager |
| **Who** | The HR officer who manages staff records, cadres, HR statistics, and job vacancies |
| **Base role** | None (custom) |
| **Capabilities** | `read`, `upload_files`, `edit_staff`, `edit_staff_cadres` (custom taxonomy manage cap), `edit_hr_capacity_stats`, `edit_job_vacancies`, `publish_job_vacancies`, `edit_published_job_vacancies`, `delete_job_vacancies` |
| **Admin sidebar access** | Dashboard, Staff & HR (all submenus), Media Library (upload only), Users (own profile only) |
| **Cannot access** | News, Events, Departments, Wards, Clinics/OPD, Special Services, Nursing School, Applications, Projects, Community, Gallery, Home Page, Pages, Appearance, Plugins, Settings |

### 3. `nursing_admin` — Nursing School Administrator

| Property | Value |
|---|---|
| **Slug** | `nursing_admin` |
| **Display name** | Nursing School Administrator |
| **Who** | The nursing school administrator who manages the school profile, programmes, intakes, facilities, and applications |
| **Base role** | None (custom) |
| **Capabilities** | `read`, `upload_files`, `edit_nursing`, `manage_nursing_profile`, `edit_nursing_programmes`, `publish_nursing_programmes`, `edit_published_nursing_programmes`, `delete_nursing_programmes`, `edit_nursing_intakes`, `edit_nursing_facilities`, `manage_applications`, `edit_applications`, `read_applications`, `edit_application_reviews`, `edit_application_status_history`, `read_application_payments` |
| **Admin sidebar access** | Dashboard, Nursing School (all submenus), Applications (all submenus), Media Library (upload only), Users (own profile only) |
| **Cannot access** | News, Events, Departments, Wards, Clinics/OPD, Special Services, Staff & HR, Projects, Community, Gallery, Home Page, Pages, Appearance, Plugins, Settings |

### 4. `admissions_officer` — Admissions Officer

| Property | Value |
|---|---|
| **Slug** | `admissions_officer` |
| **Display name** | Admissions Officer |
| **Who** | The staff member who processes nursing/medical school applications — reviewing documents, scheduling interviews, updating application status, tracking payments |
| **Base role** | None (custom) |
| **Capabilities** | `read`, `upload_files`, `manage_applications`, `edit_applications`, `read_applications`, `edit_applicants`, `edit_application_documents`, `edit_application_referees`, `edit_application_reviews`, `edit_application_status_history`, `read_application_payments`, `manage_application_notifications`, `read_application_form_downloads` |
| **Admin sidebar access** | Dashboard, Applications (all submenus), Media Library (upload only — for applicant documents), Users (own profile only) |
| **Cannot access** | Everything except Applications and Media |
| **Notes** | This role is more narrowly scoped than `nursing_admin` — it cannot manage nursing school programmes or intakes, only the application pipeline. |

### 5. `receptionist` — Receptionist

| Property | Value |
|---|---|
| **Slug** | `receptionist` |
| **Display name** | Receptionist |
| **Who** | The front-desk receptionist who manages clinic bookings, OPD appointments, and views (but does not configure) ward bed status |
| **Base role** | None (custom) |
| **Capabilities** | `read`, `edit_clinic_bookings`, `edit_opd_appointments`, `read_wards`, `read_ward_bed_status`, `edit_inpatient_admission_enquiries` |
| **Admin sidebar access** | Dashboard, Clinics & OPD (only: Clinic Bookings, OPD Appointments), Wards & Inpatient (only: Bed Status [read-only], Admission Enquiries) |
| **Cannot access** | Clinic Schedules, Schedule Exceptions, OPD Facilities, OPD Operating Hours, Consultation Rooms (these are admin-configured, not receptionist-managed), and all other sections |
| **Notes** | This is the most narrowly scoped role. Receptionists can **create and update** bookings and appointments but cannot **configure** the clinic schedule or OPD facilities — those require `edit_clinics` (held by `hospital_admin` and `editor`). |

### 6. `community_coordinator` — Community Program Coordinator

| Property | Value |
|---|---|
| **Slug** | `community_coordinator` |
| **Display name** | Community Program Coordinator |
| **Who** | The staff member who manages community outreach programs, SMI community content, and processes volunteer/vocation enquiries |
| **Base role** | None (custom) |
| **Capabilities** | `read`, `upload_files`, `edit_community`, `edit_community_programs`, `publish_community_programs`, `edit_published_community_programs`, `delete_community_programs`, `edit_community_outreach_events`, `edit_community_volunteer_signups`, `edit_community_program_media`, `manage_smi_profile`, `edit_smi_facilities`, `edit_smi_community_events`, `publish_smi_community_events`, `edit_published_smi_community_events`, `delete_smi_community_events`, `edit_smi_event_media`, `edit_smi_vocation_enquiries` |
| **Admin sidebar access** | Dashboard, Community (all submenus), Media Library (upload only), Users (own profile only) |
| **Cannot access** | All other sections |

---

## Full capability matrix (default + custom)

### Default WordPress roles — admin sidebar access

| Admin menu | Administrator | Editor | Author | Contributor | Subscriber |
|---|---|---|---|---|---|
| Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ (profile only) |
| News | ✅ | ✅ | ✅ (own) | ✅ (own, pending) | — |
| Events | ✅ | ✅ | ✅ (own) | ✅ (own, pending) | — |
| Departments | ✅ | ✅ | — | — | — |
| Wards & Inpatient | ✅ | — | — | — | — |
| Clinics & OPD | ✅ | — | — | — | — |
| Special Medical Services | ✅ | — | — | — | — |
| Staff & HR | ✅ | — | — | — | — |
| Nursing School | ✅ | — | — | — | — |
| Applications | ✅ | — | — | — | — |
| Projects | ✅ | — | — | — | — |
| Community | ✅ | — | — | — | — |
| Gallery | ✅ | ✅ | — | — | — |
| Home Page | ✅ | ✅ | — | — | — |
| Pages | ✅ | ✅ | — | — | — |
| Appearance | ✅ | — | — | — | — |
| Media Library | ✅ | ✅ | ✅ | — | — |
| Plugins | ✅ | — | — | — | — |
| Users | ✅ | — | — | — | — (own profile) |
| Settings | ✅ | — | — | — | — |

### Custom roles — admin sidebar access

| Admin menu | hospital_admin | hr_manager | nursing_admin | admissions_officer | receptionist | community_coordinator |
|---|---|---|---|---|---|---|
| Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| News | ✅ | — | — | — | — | — |
| Events | ✅ | — | — | — | — | — |
| Departments | ✅ | — | — | — | — | — |
| Wards & Inpatient | ✅ | — | — | — | ✅ (bed status + enquiries only) | — |
| Clinics & OPD | ✅ | — | — | — | ✅ (bookings + appointments only) | — |
| Special Medical Services | ✅ | — | — | — | — | — |
| Staff & HR | ✅ | ✅ | — | — | — | — |
| Nursing School | ✅ | — | ✅ | — | — | — |
| Applications | ✅ | — | ✅ | ✅ | — | — |
| Projects | ✅ | — | — | — | — | — |
| Community | ✅ | — | — | — | — | ✅ |
| Gallery | ✅ | — | — | — | — | — |
| Home Page | ✅ | — | — | — | — | — |
| Pages | ✅ | — | — | — | — | — |
| Appearance | ✅ | — | — | — | — | — |
| Media Library | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| Plugins | ✅ | — | — | — | — | — |
| Users | ✅ | — (own profile) | — (own profile) | — (own profile) | — (own profile) | — (own profile) |
| Settings | ✅ | — | — | — | — | — |

**Legend:** ✅ = full access to that menu's submenus · ✅ (scoped) = limited to specific submenus · ✅ (own) = can edit only own items · — = no access

---

## Role assignment workflow

### Who gets which role?

| OLLMH staff position | WordPress role | Rationale |
|---|---|---|
| Hospital IT Administrator / Webmaster | `administrator` (or `hospital_admin`) | Full access to everything |
| Communications Officer / PR Officer | `editor` | Manages all public-facing content (news, events, gallery, home page, pages) |
| Department Head (occasional news contributor) | `author` | Can write and publish own news articles; cannot edit others' content |
| External guest writer (rare) | `contributor` | Writes articles for review; cannot publish or upload images |
| HR Officer | `hr_manager` | Manages staff records, cadres, HR stats, job vacancies |
| Nursing School Principal / Administrator | `nursing_admin` | Manages nursing school + applications |
| Admissions Clerk | `admissions_officer` | Processes applications only |
| Front-Desk Receptionist | `receptionist` | Manages bookings, appointments, views bed status |
| Community Outreach Coordinator | `community_coordinator` | Manages community programs and SMI content |
| Patient / Public user (registered) | `subscriber` | Front-end only: book appointments, apply, manage newsletter |

### New user default role

Set in **Settings → General → "New User Default Role"** to **`subscriber`**.
This ensures that when a patient or public user registers an account on the
website (e.g., to book an appointment or apply to the nursing school), they
get the minimum-privilege role and cannot access the admin dashboard beyond
their own profile.

### Role escalation policy

- **Role assignments are made by the Administrator only.** No other role
  has `promote_users` or `edit_users` capabilities.
- **Role changes are logged.** Use an audit log plugin (or custom
  `wp_users` meta) to track who changed a user's role and when.
- **Periodic review.** The Administrator should review user role
  assignments quarterly to ensure former staff are deactivated and role
  changes reflect current responsibilities.

---

## Registration code reference

The following PHP code (to be placed in the theme's `functions.php` or a
site-specific plugin) registers the six custom roles and their capabilities.
Capabilities are added on plugin/theme activation to avoid running on every
page load.

```php
<?php
/**
 * Register OLLMH custom user roles.
 * Run on theme/plugin activation.
 */
function ollmh_register_custom_roles() {

    // 1. Hospital Administrator (clone of administrator + all custom caps)
    add_role( 'hospital_admin', 'Hospital Administrator', array(
        'read'                      => true,
        'upload_files'              => true,
        // All default administrator capabilities would be cloned here
        // (see WP's get_role('administrator')->capabilities)
        // Custom capabilities:
        'manage_applications'       => true,
        'edit_clinics'              => true,
        'edit_wards'                => true,
        'edit_staff'                => true,
        'edit_nursing'              => true,
        'edit_projects'             => true,
        'edit_community'            => true,
        'edit_home_page'            => true,
        'edit_special_services'     => true,
        'edit_departments'          => true,
        'edit_news_articles'        => true,
        'edit_events'               => true,
        'edit_gallery'              => true,
        'manage_hospital_info'      => true,
        'manage_contact_channels'   => true,
        'manage_about_content'      => true,
        'manage_governance'         => true,
    ) );

    // 2. HR Manager
    add_role( 'hr_manager', 'HR Manager', array(
        'read'                       => true,
        'upload_files'               => true,
        'edit_staff'                 => true,
        'edit_staff_cadres'          => true,
        'edit_hr_capacity_stats'     => true,
        'edit_job_vacancies'         => true,
        'publish_job_vacancies'      => true,
        'edit_published_job_vacancies' => true,
        'delete_job_vacancies'       => true,
    ) );

    // 3. Nursing School Administrator
    add_role( 'nursing_admin', 'Nursing School Administrator', array(
        'read'                        => true,
        'upload_files'                => true,
        'edit_nursing'                => true,
        'manage_nursing_profile'      => true,
        'edit_nursing_programmes'     => true,
        'publish_nursing_programmes'  => true,
        'edit_published_nursing_programmes' => true,
        'delete_nursing_programmes'   => true,
        'edit_nursing_intakes'        => true,
        'edit_nursing_facilities'     => true,
        'manage_applications'         => true,
        'edit_applications'           => true,
        'read_applications'           => true,
        'edit_application_reviews'    => true,
        'edit_application_status_history' => true,
        'read_application_payments'   => true,
    ) );

    // 4. Admissions Officer
    add_role( 'admissions_officer', 'Admissions Officer', array(
        'read'                            => true,
        'upload_files'                    => true,
        'manage_applications'             => true,
        'edit_applications'               => true,
        'read_applications'               => true,
        'edit_applicants'                 => true,
        'edit_application_documents'      => true,
        'edit_application_referees'       => true,
        'edit_application_reviews'        => true,
        'edit_application_status_history' => true,
        'read_application_payments'       => true,
        'manage_application_notifications'=> true,
        'read_application_form_downloads' => true,
    ) );

    // 5. Receptionist
    add_role( 'receptionist', 'Receptionist', array(
        'read'                          => true,
        'edit_clinic_bookings'          => true,
        'edit_opd_appointments'         => true,
        'read_wards'                    => true,
        'read_ward_bed_status'          => true,
        'edit_inpatient_admission_enquiries' => true,
    ) );

    // 6. Community Program Coordinator
    add_role( 'community_coordinator', 'Community Program Coordinator', array(
        'read'                          => true,
        'upload_files'                  => true,
        'edit_community'                => true,
        'edit_community_programs'       => true,
        'publish_community_programs'    => true,
        'edit_published_community_programs' => true,
        'delete_community_programs'     => true,
        'edit_community_outreach_events'=> true,
        'edit_community_volunteer_signups' => true,
        'edit_community_program_media'  => true,
        'manage_smi_profile'            => true,
        'edit_smi_facilities'           => true,
        'edit_smi_community_events'     => true,
        'publish_smi_community_events'  => true,
        'edit_published_smi_community_events' => true,
        'delete_smi_community_events'   => true,
        'edit_smi_event_media'          => true,
        'edit_smi_vocation_enquiries'   => true,
    ) );
}
// Register on theme activation:
add_action( 'after_switch_theme', 'ollmh_register_custom_roles' );
```

### Adding custom capabilities to default roles

The default Editor and Author roles need custom CPT capabilities added so
they can manage the custom post types (news, events, gallery, etc.):

```php
/**
 * Add custom CPT capabilities to default Editor and Author roles.
 * Run on theme/plugin activation.
 */
function ollmh_add_caps_to_default_roles() {
    $editor = get_role( 'editor' );
    if ( $editor ) {
        $editor->add_cap( 'edit_news_articles' );
        $editor->add_cap( 'edit_others_news_articles' );
        $editor->add_cap( 'publish_news_articles' );
        $editor->add_cap( 'edit_events' );
        $editor->add_cap( 'edit_others_events' );
        $editor->add_cap( 'publish_events' );
        $editor->add_cap( 'edit_gallery' );
        $editor->add_cap( 'edit_home_page' );
        $editor->add_cap( 'edit_departments' );
    }

    $author = get_role( 'author' );
    if ( $author ) {
        $author->add_cap( 'edit_news_articles' );    // own only
        $author->add_cap( 'publish_news_articles' );  // own only
        $author->add_cap( 'edit_events' );            // own only
        $author->add_cap( 'publish_events' );         // own only
    }

    $contributor = get_role( 'contributor' );
    if ( $contributor ) {
        $contributor->add_cap( 'edit_news_articles' ); // own, pending review
    }
}
add_action( 'after_switch_theme', 'ollmh_add_caps_to_default_roles' );
```

### Removing custom roles on theme deactivation

```php
/**
 * Remove custom roles on theme deactivation.
 */
function ollmh_remove_custom_roles() {
    remove_role( 'hospital_admin' );
    remove_role( 'hr_manager' );
    remove_role( 'nursing_admin' );
    remove_role( 'admissions_officer' );
    remove_role( 'receptionist' );
    remove_role( 'community_coordinator' );
}
add_action( 'switch_theme', 'ollmh_remove_custom_roles' );
```

> **Caution:** Removing a role does not delete the users assigned to it.
> Users whose role is removed will be left without a role and unable to log
> in. Before deactivating, reassign all custom-role users to `subscriber`
> or another default role.
