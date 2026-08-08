# WordPress User Roles — Core Roles & OLLMH Mapping

> This document confirms the **default WordPress user roles** as defined by
> the official WordPress documentation
> ([wordpress.org/documentation/article/roles-and-capabilities](https://wordpress.org/documentation/article/roles-and-capabilities/)),
> explains how each role functions, and maps every OLLMH staff position to
> one of the **five core WordPress roles** — Administrator, Editor, Author,
> Contributor, Subscriber. **No custom roles are created.** All operational
> needs (HR, nursing school, admissions, reception, community coordination)
> are handled by assigning the appropriate core role and adding CPT
> capabilities to that role via `add_cap()`.
>
> Admin-sidebar capabilities are cross-referenced with
> [`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md).

---

## Table of contents

1. [Confirmation of default WordPress roles](#confirmation-of-default-wordpress-roles)
2. [How each core role functions](#how-each-core-role-functions)
3. [OLLMH website — purpose and content structure](#ollmh-website--purpose-and-content-structure)
4. [Mapping OLLMH staff positions to core roles](#mapping-ollmh-staff-positions-to-core-roles)
5. [Which core roles are utilized vs. redundant](#which-core-roles-are-utilized-vs-redundant)
6. [Capability matrix (core roles × admin menus)](#capability-matrix-core-roles--admin-menus)
7. [CPT capability additions to core roles](#cpt-capability-additions-to-core-roles)
8. [Role assignment workflow](#role-assignment-workflow)
9. [Granular scoping within a core role (optional)](#granular-scoping-within-a-core-role-optional)
10. [Registration code reference](#registration-code-reference)

---

## Confirmation of default WordPress roles

WordPress ships with **six** pre-defined roles. Five exist on a standard
single-site installation; the sixth — **Super Admin** — exists only in
Multisite installations.

| # | Role | Slug | Exists on single-site? | Source |
|---|---|---|---|---|
| 1 | **Super Admin** | — | No (Multisite only) | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#super-admin) |
| 2 | **Administrator** | `administrator` | Yes | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#administrator) |
| 3 | **Editor** | `editor` | Yes | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#editor) |
| 4 | **Author** | `author` | Yes | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#author) |
| 5 | **Contributor** | `contributor` | Yes | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#contributor) |
| 6 | **Subscriber** | `subscriber` | Yes | [wordpress.org](https://wordpress.org/documentation/article/roles-and-capabilities/#subscriber) |

**Confirmed:** Administrator, Editor, Author, Contributor, and Subscriber
are the five default roles present on a standard single-site WordPress
installation. OLLMH will be a single-site installation, so Super Admin
does not apply.

On a single-site install, the Administrator holds all capabilities
(including `update_core`, `install_plugins`, `edit_themes`,
`create_users`, `delete_users`, `unfiltered_html`).

**OLLMH uses only these five core roles. No custom roles are created.**

---

## How each core role functions

### Administrator

- **Slug:** `administrator`
- **Capabilities (single-site):** All capabilities, including:
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
  links, and upload files. **Cannot** manage site settings
  (`manage_options`), install/edit plugins or themes, or manage users.
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
with 80 custom tables across 16 content domains, managed via 15 Custom Post
Types, custom taxonomies, settings pages, and management screens (see
[`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md)).

The site has multiple staff types who need different levels of admin access.
Rather than creating custom roles, **every staff position is mapped to one
of the five core WordPress roles**. The differentiation between staff types
is achieved by:

1. **Assigning the appropriate core role** (Editor vs. Author vs.
   Subscriber) based on whether the person needs to manage others' content
   (Editor) or only their own (Author) or no content at all (Subscriber).
2. **Adding CPT capabilities to the core roles** via `add_cap()` so that
   Editors and Authors can manage the custom post types (news, events,
   departments, staff, etc.) — this is standard WordPress practice when
   registering CPTs, not a custom role.
3. **Optionally using a capability manager plugin** (see
   [Granular scoping](#granular-scoping-within-a-core-role-optional)) to
   remove specific CPT capabilities from individual users within a role —
   the user is still an Editor, but with certain menus hidden.

---

## Mapping OLLMH staff positions to core roles

### Administrator → Hospital IT Administrator / Webmaster

| Aspect | Detail |
|---|---|
| **OLLMH position(s)** | Hospital IT Administrator, Webmaster |
| **Who** | The IT staff member(s) responsible for the website infrastructure |
| **What they do** | Install/update plugins and themes, manage all users, configure all settings, manage all content, update WordPress core, access all admin features |
| **Core capabilities used** | All — the Administrator role is used as-is, no modifications needed |
| **CPT capabilities** | All CPT capabilities are automatically available to Administrators (WordPress grants all capabilities to the Administrator role by default) |
| **Estimated count** | 1–3 users |
| **Verdict** | **Actively utilized.** Essential. At least one Administrator account is required by WordPress itself (created during installation). |

### Editor → Communications, HR, Nursing Admin, Community Coordinator

The Editor role is the **workhorse** for OLLMH. Every staff member who needs
to manage content across a domain — not just their own posts — gets the
Editor role. The Editor's core capabilities (`edit_others_posts`,
`edit_pages`, `publish_posts`, `moderate_comments`, `manage_categories`,
`upload_files`) are exactly what these positions need.

| OLLMH position | What they manage as Editor |
|---|---|
| **Communications Officer / PR Officer** | News articles, events, gallery (albums + items), home page content (slides, feature blocks, in-focus items, news promos), static pages |
| **HR Officer / HR Manager** | Staff records, staff cadres, HR capacity stats, job vacancies |
| **Nursing School Principal / Administrator** | Nursing school profile, programmes, intakes, facilities, applications |
| **Admissions Officer (senior)** | Applications pipeline (applicants, documents, referees, reviews, payments, status history, notifications) |
| **Community Outreach Coordinator** | Community programs, outreach events, volunteer signups, SMI community profile, SMI facilities, SMI events, vocation enquiries |
| **Projects Manager** | Development projects, sustainability projects, upcoming projects, project media/metrics/phases/pledges |

**What all Editors can do:** Create, edit, publish, and delete any CPT
content (news, events, departments, staff, wards, clinics, applications,
projects, community programs, gallery items, home page blocks). Moderate
comments. Manage categories and tags. Upload files. Edit static pages.

**What Editors cannot do:** Install/manage plugins and themes, manage
users, manage site settings (hospital info, contact channels, governance),
access the Appearance or Plugins or Settings menus.

**Estimated count:** 4–8 users.

**Verdict:** **Actively utilized.** The Editor role is the backbone of the
content management workflow. CPT capabilities are added to the Editor role
via `add_cap()` (see [Registration code](#registration-code-reference)).

### Author → Department Heads, Receptionists, Admissions Clerks, Junior Staff

The Author role is for staff who create and manage **their own** records but
should not edit other people's content. This is the right role for anyone
who enters data (bookings, appointments, applications, news contributions)
but is not responsible for editorial oversight.

| OLLMH position | What they manage as Author |
|---|---|
| **Department Head (occasional news contributor)** | Writes and publishes their own news articles and events; cannot edit others' articles |
| **Front-Desk Receptionist** | Creates and manages clinic bookings and OPD appointments (their own entries); views ward bed status |
| **Admissions Clerk (junior)** | Creates and manages application records they are assigned to; cannot edit others' applications |
| **Clinical Staff (nurses, doctors)** | May contribute news articles about their department; cannot edit others' content |
| **Volunteer Coordinator** | Manages volunteer signup records they create; cannot edit others' |

**What Authors can do:** Create, publish, edit, and delete their own posts
and CPT entries. Upload files (images).

**What Authors cannot do:** Edit others' posts or pages, moderate comments,
manage categories, access site settings, manage users, install plugins.

**Estimated count:** 5–15 users.

**Verdict:** **Actively utilized.** The Author role gives individual
contributors the ability to create content without editorial control over
others. CPT capabilities for "own only" are added via `add_cap()` (the
`edit_others_*` capabilities are NOT granted to Authors).

### Contributor → Guest Writer / External Contributor

| Aspect | Detail |
|---|---|
| **OLLMH position** | Guest writer — an external contributor (e.g., a volunteer, a visiting medical student, a community member) who submits a news article for review but cannot publish it directly |
| **What they do** | Write news articles (saved as "Pending Review"), which an Editor then reviews and publishes |
| **Core capabilities used** | `edit_posts`, `delete_posts`, `read` |
| **What they cannot do** | Publish posts, upload files (no `upload_files` — images must be added by the reviewing Editor), edit others' content, access any other admin section |
| **Estimated count** | 0 (typically) |
| **Verdict** | **Redundant in practice.** Useful only if OLLMH plans to accept external article submissions. For a hospital website where content is primarily produced by staff, this role is likely unassigned. **Recommendation: keep the role registered (it is a core WordPress role and cannot be removed) but do not assign any user to it unless external contributors are explicitly onboarded.** |

### Subscriber → Patient / Public User / Newsletter Subscriber

| Aspect | Detail |
|---|---|
| **OLLMH position** | Registered site user — a patient, community member, or newsletter subscriber who has created an account on the website |
| **Who** | Any public user who registers an account (e.g., to book clinic appointments online, to subscribe to the newsletter, to track an application status) |
| **What they do** | Log in, manage their own profile (name, email, password), view their appointment bookings, view their application status, manage their newsletter subscription preferences |
| **Core capabilities used** | `read` (only) |
| **What they cannot do** | Access the WordPress admin dashboard (beyond their profile), write/edit any content, access any admin section |
| **Front-end access** | On the **front-end**, Subscribers get authenticated access to: their own `wp_clinic_bookings` records, their own `wp_opd_appointments`, their own `wp_applications` / `wp_applicants` profile, their own `wp_newsletter_subscribers` preferences. This is handled via front-end form shortcodes and `is_user_logged_in()` checks, not via admin capabilities. |
| **Estimated count** | 100+ (all registered public users) |
| **Verdict** | **Actively utilized — but primarily on the front-end, not the admin.** Subscribers never see the admin sidebar. This is the **default role for new user registrations** (set in Settings → General → "New User Default Role"). |

---

## Which core roles are utilized vs. redundant

| Core role | OLLMH utilization | Status | Estimated count |
|---|---|---|---|
| **Super Admin** | Not applicable (single-site install) | **N/A — does not exist** | 0 |
| **Administrator** | Hospital IT admin / webmaster | **Actively utilized** | 1–3 |
| **Editor** | Communications, HR, nursing admin, admissions (senior), community coordinator, projects manager | **Actively utilized** | 4–8 |
| **Author** | Department heads, receptionists, admissions clerks, clinical staff, volunteer coordinators | **Actively utilized** | 5–15 |
| **Contributor** | Guest writer / external contributor | **Redundant in practice** — keep registered but unassigned unless external contributors are onboarded | 0 (typically) |
| **Subscriber** | Patient / public user / newsletter subscriber | **Actively utilized (front-end only)** — default role for new registrations | 100+ |

### Summary

- **4 core roles are actively utilized:** Administrator, Editor, Author,
  Subscriber.
- **1 core role is redundant for OLLMH's current needs:** Contributor (kept
  registered but unassigned unless external writers are onboarded).
- **1 core role does not exist:** Super Admin (Multisite only; OLLMH is
  single-site).
- **0 custom roles are created.** All OLLMH staff positions fit within the
  five core WordPress roles.

---

## Capability matrix (core roles × admin menus)

| Admin menu | Administrator | Editor | Author | Contributor | Subscriber |
|---|---|---|---|---|---|
| Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ (profile only) |
| News | ✅ | ✅ | ✅ (own) | ✅ (own, pending) | — |
| Events | ✅ | ✅ | ✅ (own) | ✅ (own, pending) | — |
| Departments | ✅ | ✅ | — | — | — |
| Wards & Inpatient | ✅ | ✅ | ✅ (own bookings/enquiries) | — | — |
| Clinics & OPD | ✅ | ✅ | ✅ (own bookings/appointments) | — | — |
| Special Medical Services | ✅ | ✅ | — | — | — |
| Staff & HR | ✅ | ✅ | — | — | — |
| Nursing School | ✅ | ✅ | — | — | — |
| Applications | ✅ | ✅ | ✅ (own assigned) | — | — |
| Projects | ✅ | ✅ | — | — | — |
| Community | ✅ | ✅ | ✅ (own volunteer signups) | — | — |
| Gallery | ✅ | ✅ | — | — | — |
| Home Page | ✅ | ✅ | — | — | — |
| Pages | ✅ | ✅ | — | — | — |
| Appearance | ✅ | — | — | — | — |
| Media Library | ✅ | ✅ | ✅ | — | — |
| Plugins | ✅ | — | — | — | — |
| Users | ✅ | — | — | — | — (own profile) |
| Settings | ✅ | — | — | — | — |
| SEO | ✅ | ✅ | — | — | — |

**Legend:** ✅ = full access to that menu's submenus · ✅ (own) = can edit
only own items · ✅ (own, pending) = can create own items but cannot publish
· — = no access

### How the matrix works in practice

- An **Editor** who is the HR Officer sees all admin menus their role
  grants (News, Events, Departments, Wards, Clinics, Staff & HR, Nursing
  School, Applications, Projects, Community, Gallery, Home Page, Pages,
  Media, SEO). In practice, the HR Officer focuses on the Staff & HR menu.
  If the hospital wants to **hide menus the HR Officer doesn't need**, see
  [Granular scoping](#granular-scoping-within-a-core-role-optional) below.

- An **Author** who is a Receptionist sees Dashboard, News (own), Events
  (own), Wards & Inpatient (own bookings/enquiries), Clinics & OPD (own
  bookings/appointments), Community (own volunteer signups), Applications
  (own assigned), and Media Library. They cannot edit others' content.

---

## CPT capability additions to core roles

When Custom Post Types are registered, WordPress creates corresponding
capabilities (e.g., `edit_news_articles`, `edit_others_news_articles`,
`publish_news_articles`). These capabilities must be added to the Editor
and Author roles so they can manage the CPTs. **This is standard WordPress
practice — it does not create custom roles.** The capabilities are added to
existing core roles via `add_cap()`.

### Editor gets full CPT access (edit own + edit others' + publish + delete)

| CPT | Capabilities added to Editor |
|---|---|
| News articles | `edit_news_articles`, `edit_others_news_articles`, `publish_news_articles`, `delete_news_articles`, `delete_others_news_articles` |
| Events | `edit_events`, `edit_others_events`, `publish_events`, `delete_events`, `delete_others_events` |
| Departments | `edit_departments`, `edit_others_departments`, `publish_departments`, `delete_departments` |
| Wards | `edit_wards`, `edit_others_wards`, `publish_wards`, `delete_wards` |
| Clinics | `edit_clinics`, `edit_others_clinics`, `publish_clinics`, `delete_clinics` |
| Special services | `edit_special_services`, `edit_others_special_services`, `publish_special_services` |
| Staff | `edit_staff`, `edit_others_staff`, `publish_staff`, `delete_staff` |
| Job vacancies | `edit_job_vacancies`, `edit_others_job_vacancies`, `publish_job_vacancies` |
| Nursing programmes | `edit_nursing_programmes`, `edit_others_nursing_programmes`, `publish_nursing_programmes` |
| Applications | `edit_applications`, `edit_others_applications`, `publish_applications` |
| Projects (all 3) | `edit_projects`, `edit_others_projects`, `publish_projects` |
| Community programs | `edit_community_programs`, `edit_others_community_programs`, `publish_community_programs` |
| SMI events | `edit_smi_events`, `edit_others_smi_events`, `publish_smi_events` |
| Gallery albums | `edit_gallery`, `edit_others_gallery`, `publish_gallery` |
| Home page blocks | `edit_home_page` |
| SEO | `manage_seo` |

### Author gets own-only CPT access (edit own + publish own + delete own — no edit_others)

| CPT | Capabilities added to Author |
|---|---|
| News articles | `edit_news_articles`, `publish_news_articles`, `delete_news_articles` (NOT `edit_others_news_articles`) |
| Events | `edit_events`, `publish_events`, `delete_events` (NOT `edit_others_events`) |
| Clinic bookings | `edit_clinic_bookings`, `publish_clinic_bookings` |
| OPD appointments | `edit_opd_appointments`, `publish_opd_appointments` |
| Applications | `edit_applications`, `publish_applications` (NOT `edit_others_applications`) |
| Community volunteer signups | `edit_community_volunteer_signups` |
| Inpatient admission enquiries | `edit_inpatient_admission_enquiries` |

### Contributor gets create-only (no publish, no upload)

| CPT | Capabilities added to Contributor |
|---|---|
| News articles | `edit_news_articles` (creates drafts/pending only — no `publish_news_articles`) |

### Subscriber gets no CPT capabilities

Subscribers interact with the site entirely on the **front-end** (booking
appointments, applying to nursing school, managing newsletter preferences).
No admin CPT capabilities are added to the Subscriber role.

---

## Role assignment workflow

### Who gets which core role?

| OLLMH staff position | Core WordPress role | Rationale |
|---|---|---|
| Hospital IT Administrator / Webmaster | **Administrator** | Full access to everything — plugins, themes, users, settings, all content |
| Communications Officer / PR Officer | **Editor** | Manages all public-facing content (news, events, gallery, home page, pages) |
| HR Officer / HR Manager | **Editor** | Manages staff records, cadres, HR stats, job vacancies — needs `edit_others` for staff CPT |
| Nursing School Principal / Administrator | **Editor** | Manages nursing school + applications — needs `edit_others` for programmes and applications |
| Admissions Officer (senior) | **Editor** | Manages the full application pipeline — needs `edit_others` for applications |
| Community Outreach Coordinator | **Editor** | Manages community programs and SMI content — needs `edit_others` for programs and events |
| Projects Manager | **Editor** | Manages all three project types — needs `edit_others` for project CPTs |
| Department Head (occasional news contributor) | **Author** | Writes and publishes own news articles; cannot edit others' content |
| Front-Desk Receptionist | **Author** | Creates and manages own clinic bookings and OPD appointments; cannot edit others' |
| Admissions Clerk (junior) | **Author** | Creates and manages own application records; cannot edit others' applications |
| Clinical Staff (nurses, doctors) | **Author** | May contribute news articles about their department; cannot edit others' content |
| Volunteer Coordinator | **Author** | Manages own volunteer signup records; cannot edit others' |
| External guest writer (rare) | **Contributor** | Writes articles for review; cannot publish or upload images |
| Patient / Public user (registered) | **Subscriber** | Front-end only: book appointments, apply, manage newsletter |

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

## Granular scoping within a core role (optional)

In some cases, the hospital may want an Editor to see only certain admin
menus — for example, the HR Officer should see Staff & HR but not News or
Events. There are two approaches, **both of which keep the user as an
Editor** (no custom role is created):

### Approach 1: Capability manager plugin (recommended)

Install a capability management plugin such as **Members** (by MemberPress,
free, wordpress.org/plugins/members/) or **User Role Editor** (free,
wordpress.org/plugins/user-role-editor/). These plugins let the
Administrator:

- Remove specific capabilities from individual users (not the whole role)
- The user remains an Editor in the database, but certain menus are hidden
  because they lack the specific capability for that CPT

**Example:** The HR Officer is an Editor. The Administrator uses the
Members plugin to remove `edit_news_articles`, `edit_events`,
`edit_wards`, `edit_clinics`, etc. from this specific user. The HR Officer
now sees only Dashboard, Staff & HR, Media Library, and SEO — but their
role is still "Editor" in the user list.

### Approach 2: Admin menu visibility plugin (simpler, less granular)

Install a plugin like **Admin Menu Editor** (wordpress.org/plugins/admin-menu-editor/)
or **Hide Admin Menu** to hide specific admin menus per user or per role.
This is purely visual — it hides the menu item but does not remove the
underlying capability. A savvy user could still access the hidden page via
direct URL. For a hospital internal site where staff are trusted, this is
usually sufficient.

### Which approach to use?

| Need | Approach |
|---|---|
| Hide menus visually (trusted internal staff) | Admin Menu Editor (Approach 2) |
| Enforce capability restrictions (security-relevant) | Members plugin (Approach 1) |
| No scoping needed — all Editors see everything | Neither — default Editor access |

**OLLMH recommendation:** Start with no scoping (all Editors see all
menus). If staff report confusion from seeing too many menus, add Admin
Menu Editor (Approach 2) to hide irrelevant menus per user. Only escalate
to the Members plugin (Approach 1) if there is a security or compliance
requirement to enforce capability restrictions.

---

## Registration code reference

The following PHP code (to be placed in the theme's `functions.php` or a
site-specific plugin) adds CPT capabilities to the core Editor, Author, and
Contributor roles. **No custom roles are registered.** No `add_role()`
calls are made. Only `add_cap()` is used to extend existing core roles.

```php
<?php
/**
 * Add CPT capabilities to core WordPress roles.
 * No custom roles are created — only core roles are used.
 * Run on theme/plugin activation.
 */
function ollmh_add_cpt_caps_to_core_roles() {

    // ── Editor: full CPT access (edit own + edit others' + publish + delete) ──
    $editor = get_role( 'editor' );
    if ( $editor ) {
        // News
        $editor->add_cap( 'edit_news_articles' );
        $editor->add_cap( 'edit_others_news_articles' );
        $editor->add_cap( 'publish_news_articles' );
        $editor->add_cap( 'delete_news_articles' );
        $editor->add_cap( 'delete_others_news_articles' );

        // Events
        $editor->add_cap( 'edit_events' );
        $editor->add_cap( 'edit_others_events' );
        $editor->add_cap( 'publish_events' );
        $editor->add_cap( 'delete_events' );
        $editor->add_cap( 'delete_others_events' );

        // Departments
        $editor->add_cap( 'edit_departments' );
        $editor->add_cap( 'edit_others_departments' );
        $editor->add_cap( 'publish_departments' );
        $editor->add_cap( 'delete_departments' );

        // Wards
        $editor->add_cap( 'edit_wards' );
        $editor->add_cap( 'edit_others_wards' );
        $editor->add_cap( 'publish_wards' );
        $editor->add_cap( 'delete_wards' );

        // Clinics
        $editor->add_cap( 'edit_clinics' );
        $editor->add_cap( 'edit_others_clinics' );
        $editor->add_cap( 'publish_clinics' );
        $editor->add_cap( 'delete_clinics' );

        // Special Medical Services
        $editor->add_cap( 'edit_special_services' );
        $editor->add_cap( 'edit_others_special_services' );
        $editor->add_cap( 'publish_special_services' );

        // Staff
        $editor->add_cap( 'edit_staff' );
        $editor->add_cap( 'edit_others_staff' );
        $editor->add_cap( 'publish_staff' );
        $editor->add_cap( 'delete_staff' );

        // Job Vacancies
        $editor->add_cap( 'edit_job_vacancies' );
        $editor->add_cap( 'edit_others_job_vacancies' );
        $editor->add_cap( 'publish_job_vacancies' );

        // Nursing Programmes
        $editor->add_cap( 'edit_nursing_programmes' );
        $editor->add_cap( 'edit_others_nursing_programmes' );
        $editor->add_cap( 'publish_nursing_programmes' );

        // Applications
        $editor->add_cap( 'edit_applications' );
        $editor->add_cap( 'edit_others_applications' );
        $editor->add_cap( 'publish_applications' );

        // Projects (development, sustainability, upcoming)
        $editor->add_cap( 'edit_projects' );
        $editor->add_cap( 'edit_others_projects' );
        $editor->add_cap( 'publish_projects' );

        // Community Programs
        $editor->add_cap( 'edit_community_programs' );
        $editor->add_cap( 'edit_others_community_programs' );
        $editor->add_cap( 'publish_community_programs' );

        // SMI Events
        $editor->add_cap( 'edit_smi_events' );
        $editor->add_cap( 'edit_others_smi_events' );
        $editor->add_cap( 'publish_smi_events' );

        // Gallery
        $editor->add_cap( 'edit_gallery' );
        $editor->add_cap( 'edit_others_gallery' );
        $editor->add_cap( 'publish_gallery' );

        // Home Page
        $editor->add_cap( 'edit_home_page' );

        // SEO
        $editor->add_cap( 'manage_seo' );
    }

    // ── Author: own-only CPT access (edit own + publish own — NO edit_others) ──
    $author = get_role( 'author' );
    if ( $author ) {
        // News (own only)
        $author->add_cap( 'edit_news_articles' );
        $author->add_cap( 'publish_news_articles' );
        $author->add_cap( 'delete_news_articles' );
        // NOTE: edit_others_news_articles is NOT added — Authors can only
        // edit their own news articles.

        // Events (own only)
        $author->add_cap( 'edit_events' );
        $author->add_cap( 'publish_events' );
        $author->add_cap( 'delete_events' );

        // Clinic bookings (own only — for receptionists)
        $author->add_cap( 'edit_clinic_bookings' );
        $author->add_cap( 'publish_clinic_bookings' );

        // OPD appointments (own only — for receptionists)
        $author->add_cap( 'edit_opd_appointments' );
        $author->add_cap( 'publish_opd_appointments' );

        // Applications (own only — for admissions clerks)
        $author->add_cap( 'edit_applications' );
        $author->add_cap( 'publish_applications' );

        // Community volunteer signups (own only)
        $author->add_cap( 'edit_community_volunteer_signups' );

        // Inpatient admission enquiries (own only)
        $author->add_cap( 'edit_inpatient_admission_enquiries' );
    }

    // ── Contributor: create-only (no publish, no upload) ──
    $contributor = get_role( 'contributor' );
    if ( $contributor ) {
        // News (create drafts/pending only — no publish capability)
        $contributor->add_cap( 'edit_news_articles' );
        // NOTE: publish_news_articles is NOT added — Contributor posts
        // remain "Pending Review" until an Editor publishes them.
    }

    // ── Subscriber: no CPT capabilities (front-end only) ──
    // No add_cap() calls for Subscriber — they interact with the site
    // entirely via front-end forms (booking, applications, newsletter).
}
add_action( 'after_switch_theme', 'ollmh_add_cpt_caps_to_core_roles' );
```

### Cleanup on theme deactivation

```php
/**
 * Remove CPT capabilities from core roles on theme deactivation.
 * No custom roles to remove — only caps are cleaned up.
 */
function ollmh_remove_cpt_caps_from_core_roles() {
    $editor = get_role( 'editor' );
    $author = get_role( 'author' );
    $contributor = get_role( 'contributor' );

    $editor_caps = array(
        'edit_news_articles', 'edit_others_news_articles', 'publish_news_articles',
        'delete_news_articles', 'delete_others_news_articles',
        'edit_events', 'edit_others_events', 'publish_events',
        'delete_events', 'delete_others_events',
        'edit_departments', 'edit_others_departments', 'publish_departments', 'delete_departments',
        'edit_wards', 'edit_others_wards', 'publish_wards', 'delete_wards',
        'edit_clinics', 'edit_others_clinics', 'publish_clinics', 'delete_clinics',
        'edit_special_services', 'edit_others_special_services', 'publish_special_services',
        'edit_staff', 'edit_others_staff', 'publish_staff', 'delete_staff',
        'edit_job_vacancies', 'edit_others_job_vacancies', 'publish_job_vacancies',
        'edit_nursing_programmes', 'edit_others_nursing_programmes', 'publish_nursing_programmes',
        'edit_applications', 'edit_others_applications', 'publish_applications',
        'edit_projects', 'edit_others_projects', 'publish_projects',
        'edit_community_programs', 'edit_others_community_programs', 'publish_community_programs',
        'edit_smi_events', 'edit_others_smi_events', 'publish_smi_events',
        'edit_gallery', 'edit_others_gallery', 'publish_gallery',
        'edit_home_page', 'manage_seo',
    );

    $author_caps = array(
        'edit_news_articles', 'publish_news_articles', 'delete_news_articles',
        'edit_events', 'publish_events', 'delete_events',
        'edit_clinic_bookings', 'publish_clinic_bookings',
        'edit_opd_appointments', 'publish_opd_appointments',
        'edit_applications', 'publish_applications',
        'edit_community_volunteer_signups',
        'edit_inpatient_admission_enquiries',
    );

    $contributor_caps = array( 'edit_news_articles' );

    foreach ( $editor_caps as $cap ) {
        if ( $editor ) $editor->remove_cap( $cap );
    }
    foreach ( $author_caps as $cap ) {
        if ( $author ) $author->remove_cap( $cap );
    }
    foreach ( $contributor_caps as $cap ) {
        if ( $contributor ) $contributor->remove_cap( $cap );
    }
}
add_action( 'switch_theme', 'ollmh_remove_cpt_caps_from_core_roles' );
```

> **Note:** Unlike the previous version of this document, there are **no
> `add_role()` calls** and **no `remove_role()` calls**. Only the five core
> WordPress roles are used. CPT capabilities are added to and removed from
> existing core roles via `add_cap()` / `remove_cap()`.
