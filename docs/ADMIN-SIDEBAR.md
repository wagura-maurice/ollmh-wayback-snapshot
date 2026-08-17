# WordPress Admin Sidebar Menu Structure

> This document defines the **complete admin sidebar menu** for the OLLMH
> WordPress rebuild. Every top-level menu item and submenu is mapped to the
> custom database tables (from the [ERD](./ERD.md)) and WordPress core
> functionality it manages.
>
> Per [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md) → **ADR-006**
> (Approved), the data layer is **WordPress-native**: content entities are
> Custom Post Types and taxonomies (which surface as native admin menus),
> while only the ~26 operational tables in ADR-006 have bespoke management
> screens. The older "**81 custom tables**" framing below is superseded by
> ADR-006's classification — read the entities here as CPTs / taxonomies /
> post meta / retained custom tables accordingly. The structure groups these
> into logical admin sections using WordPress Custom Post Types (CPTs), custom
> taxonomy registrations, settings pages, and management screens. The goal is a
> sidebar that is comprehensive yet scannable — no more than **18 top-level
> items** — with related entities grouped under a single parent menu.

---

## Table of contents

1. [Sidebar overview (visual map)](#sidebar-overview-visual-map)
2. [Menu items — detailed reference](#menu-items--detailed-reference)
3. [Capability/role matrix](#capabilityrole-matrix)
4. [CPT registration summary](#cpt-registration-summary)
5. [Settings page tabs](#settings-page-tabs)

---

## Sidebar overview (visual map)

```
┌─────────────────────────────────────────────────────────────┐
│  OLLMH Admin                                                │
├─────────────────────────────────────────────────────────────┤
│  📊 Dashboard                                               │
│  📰 News                                                    │
│      ├── All Articles                                       │
│      ├── Add New Article                                    │
│      ├── Categories                                         │
│      ├── Tags                                               │
│      ├── Comments                                           │
│      └── Newsletter Subscribers                             │
│  📅 Events                                                  │
│      ├── All Events                                         │
│      ├── Add New Event                                      │
│      ├── Event Categories                                   │
│      └── Registrations                                      │
│  🏥 Departments                                             │
│      ├── All Departments                                    │
│      ├── Department Showcase                                │
│      └── Department Photos                                  │
│  🛏️ Wards & Inpatient                                       │
│      ├── Wards                                              │
│      ├── Ward Media                                         │
│      ├── Bed Status                                         │
│      ├── Inpatient Sections                                 │
│      ├── Admission Enquiries                                │
│      └── Mortuary Services                                  │
│  🩺 Clinics & OPD                                           │
│      ├── Clinics                                            │
│      ├── Clinic Schedules                                   │
│      ├── Schedule Exceptions                                │
│      ├── Clinic Bookings                                    │
│      ├── OPD Facilities                                     │
│      ├── OPD Operating Hours                                │
│      ├── Consultation Rooms                                 │
│      └── OPD Appointments                                   │
│  🔬 Special Medical Services                                │
│      ├── Services                                           │
│      ├── Specialists                                        │
│      ├── Equipment                                          │
│      └── Service Enquiries                                  │
│  👥 Staff & HR                                              │
│      ├── Staff Members                                      │
│      ├── Staff Cadres                                       │
│      ├── HR Capacity Stats                                  │
│      └── Job Vacancies                                      │
│  🎓 Nursing School                                          │
│      ├── School Profile                                     │
│      ├── Programmes                                         │
│      ├── Intakes                                            │
│      └── Facilities                                         │
│  📋 Applications                                            │
│      ├── All Applications                                   │
│      ├── Applicants                                         │
│      ├── Application Documents                              │
│      ├── Referees                                           │
│      ├── Reviews                                            │
│      ├── Payments                                           │
│      ├── Status History                                     │
│      ├── Notifications                                      │
│      └── Form Downloads                                     │
│  🏗️ Projects                                               │
│      ├── Development Projects                               │
│      ├── Strategic Plans                                    │
│      ├── Project Media                                      │
│      ├── Project Metrics                                    │
│      ├── Plan Links                                         │
│      ├── Sustainability Projects                            │
│      ├── Production Records                                 │
│      ├── Sustainability Media                               │
│      ├── Upcoming Projects                                  │
│      ├── Project Phases                                     │
│      ├── Upcoming Project Media                             │
│      └── Pledges                                            │
│  🤝 Community                                               │
│      ├── Community Programs                                 │
│      ├── Outreach Events                                    │
│      ├── Volunteer Signups                                  │
│      ├── Program Media                                      │
│      ├── SMI Community Profile                              │
│      ├── SMI Facilities                                     │
│      ├── SMI Community Events                               │
│      ├── SMI Event Media                                    │
│      └── Vocation Enquiries                                 │
│  📸 Gallery (Outlook)                                       │
│      ├── Albums                                             │
│      └── Gallery Items                                      │
│  🏠 Home Page                                               │
│      ├── Slides                                             │
│      ├── Feature Blocks                                     │
│      ├── In Focus Items                                     │
│      └── News Promos                                        │
│  📄 Pages                                                   │
│  🎨 Appearance                                              │
│      ├── Themes                                             │
│      ├── Customize                                          │
│      ├── Menus                                              │
│      ├── Header                                             │
│      ├── Footer                                             │
│      ├── Color Scheme                                       │
│      └── Font Schema                                        │
│  📁 Media Library                                           │
│  🧩 Plugins                                                 │
│  👤 Users                                                   │
│  ⚙️ Settings                                                │
│      ├── General                                            │
│      ├── Hospital Info                                      │
│      ├── Contact Channels                                   │
│      ├── About Facts                                        │
│      ├── Milestones                                         │
│      ├── Care Statements                                    │
│      ├── Care Values                                        │
│      ├── Governance Bodies                                  │
│      └── Governance Members                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Menu items — detailed reference

### 1. Dashboard *(WordPress core)*

| Submenu | Purpose |
|---|---|
| Home | At-a-glance widgets: pending applications, today's clinic bookings, bed status summary, recent enquiries, recent news articles |
| Updates | WordPress core/plugin/theme updates |

**Custom widgets to register:**
- Pending Applications count → links to Applications
- Today's Clinic Bookings → links to Clinics & OPD → Clinic Bookings
- Bed Status Summary (occupied vs. available) → links to Wards → Bed Status
- Recent Enquiries (service + admission + vocation) → links to respective sections
- Recent News Articles → links to News

---

### 2. News *(CPT: `news_article`)*

Manages all news content and newsletter subscribers.

| Submenu | Table(s) | Type |
|---|---|---|
| All Articles | `wp_news_articles`, `wp_news_article_revisions` | CPT list |
| Add New Article | `wp_news_articles` | CPT editor |
| Categories | `wp_news_categories` | Custom taxonomy |
| Tags | `wp_news_tags`, `wp_news_article_tags` | Custom taxonomy |
| Comments | `wp_news_comments` | Management list |
| Newsletter Subscribers | `wp_newsletter_subscribers` | Management list |

**Capability:** `edit_news_articles` (editors + admins)

---

### 3. Events *(CPT: `event`)*

Manages all events and registrations.

| Submenu | Table(s) | Type |
|---|---|---|
| All Events | `wp_events` | CPT list |
| Add New Event | `wp_events` | CPT editor |
| Event Categories | `wp_event_categories` | Custom taxonomy |
| Registrations | `wp_event_registrations` | Management list |
| Event Media | `wp_event_media` | Media assignment |

**Capability:** `edit_events` (editors + admins)

---

### 4. Departments *(CPT: `department`)*

Manages hospital departments, their showcase, and photos.

| Submenu | Table(s) | Type |
|---|---|---|
| All Departments | `wp_departments` | CPT list |
| Add New Department | `wp_departments` | CPT editor |
| Department Showcase | `wp_department_showcase` | Meta box on CPT editor |
| Department Photos | `wp_department_photos` | Media assignment |

**Capability:** `edit_departments` (editors + admins)

---

### 5. Wards & Inpatient *(CPT: `ward` + management screens)*

Groups all inpatient-related tables under one parent menu.

| Submenu | Table(s) | Type |
|---|---|---|
| Wards | `wp_wards` | CPT list + editor |
| Ward Media | `wp_ward_media` | Media assignment |
| Bed Status | `wp_ward_bed_status` | Management list (real-time bed availability grid) |
| Inpatient Sections | `wp_inpatient_dept_sections` | Management list |
| Admission Enquiries | `wp_inpatient_admission_enquiries` | Inbox-style list |
| Mortuary Services | `wp_mortuary_services` | Management list |

**Capability:** `edit_wards` (nurses/admins for bed status; admins for mortuary)

---

### 6. Clinics & OPD *(CPT: `clinic` + management screens)*

Groups outpatient and clinic scheduling under one parent menu.

| Submenu | Table(s) | Type |
|---|---|---|
| Clinics | `wp_clinics` | CPT list + editor |
| Clinic Schedules | `wp_clinic_schedules` | Management list (recurring weekly schedule) |
| Schedule Exceptions | `wp_clinic_schedule_exceptions` | Management list (holidays, closures) |
| Clinic Bookings | `wp_clinic_bookings` | Inbox-style list (patient appointments) |
| OPD Facilities | `wp_opd_facilities` | Management list |
| OPD Operating Hours | `wp_opd_operating_hours` | Management list |
| Consultation Rooms | `wp_opd_consultation_rooms` | Management list |
| OPD Appointments | `wp_opd_appointments` | Inbox-style list |

**Capability:** `edit_clinics` (receptionists for bookings/appointments; admins for schedules)

---

### 7. Special Medical Services *(CPT: `special_service`)*

Manages specialized medical services, specialists, equipment, and enquiries.

| Submenu | Table(s) | Type |
|---|---|---|
| Services | `wp_special_medical_services` | CPT list + editor |
| Specialists | `wp_service_specialists` | Management list (links to `wp_staff`) |
| Equipment | `wp_service_equipment` | Management list |
| Service Enquiries | `wp_service_enquiries` | Inbox-style list |

**Capability:** `edit_special_services` (admins)

---

### 8. Staff & HR *(CPT: `staff_member`)*

Manages staff records, cadres, HR statistics, and job vacancies.

| Submenu | Table(s) | Type |
|---|---|---|
| Staff Members | `wp_staff` | CPT list + editor (links to `wp_departments`, `wp_media_assets`) |
| Staff Cadres | `wp_staff_cadres` | Custom taxonomy |
| HR Capacity Stats | `wp_hr_capacity_stats` | Management list (headcount by cadre/dept) |
| Job Vacancies | `wp_job_vacancies` | CPT list + editor (public-facing job board) |

**Capability:** `edit_staff` (HR role; admins)

---

### 9. Nursing School *(CPT: `nursing_programme` + settings)*

Manages the nursing school profile, programmes, intakes, and facilities.

| Submenu | Table(s) | Type |
|---|---|---|
| School Profile | `wp_nursing_school_profile` | Single-record settings page |
| Programmes | `wp_nursing_programmes` | CPT list + editor |
| Intakes | `wp_nursing_intakes` | Management list (admission cycles) |
| Facilities | `wp_nursing_facilities` | Management list |

**Capability:** `edit_nursing` (nursing admin role; admins)

---

### 10. Applications *(management screens)*

Manages the entire medical/nursing school application pipeline. This is the
most complex admin section — 9 tables covering the full application
lifecycle.

| Submenu | Table(s) | Type |
|---|---|---|
| All Applications | `wp_applications` | Master list (filterable by status) |
| Applicants | `wp_applicants` | Management list (personal data) |
| Application Documents | `wp_application_documents` | File management list |
| Referees | `wp_application_referees` | Management list |
| Reviews | `wp_application_reviews` | Review/approval workflow list |
| Payments | `wp_application_payments` | Payment tracking list |
| Status History | `wp_application_status_history` | Audit log per application |
| Notifications | `wp_application_notifications` | Email/notification log |
| Form Downloads | `wp_application_form_downloads` | Download tracking list |

**Capability:** `manage_applications` (admissions role; admins)

**Dashboard widget:** Pending applications count + urgent review alerts.

---

### 11. Projects *(CPT group: 3 post types)*

Groups all three project types (Development, Sustainability, Upcoming)
under one parent menu to avoid sidebar bloat.

| Submenu | Table(s) | Type |
|---|---|---|
| Development Projects | `wp_development_projects` | CPT list + editor |
| Strategic Plans | `wp_development_strategic_plans` | Management list |
| Project Media | `wp_development_project_media` | Media assignment |
| Project Metrics | `wp_development_project_metrics` | Management list (KPIs) |
| Plan Links | `wp_development_project_plan_links` | Link management |
| Sustainability Projects | `wp_sustainability_projects` | CPT list + editor |
| Production Records | `wp_sustainability_production_records` | Management list |
| Sustainability Media | `wp_sustainability_project_media` | Media assignment |
| Upcoming Projects | `wp_upcoming_projects` | CPT list + editor |
| Project Phases | `wp_upcoming_project_phases` | Management list |
| Upcoming Project Media | `wp_upcoming_project_media` | Media assignment |
| Pledges | `wp_upcoming_project_pledges` | Management list (donations/pledges) |

**Capability:** `edit_projects` (project managers; admins)

---

### 12. Community *(CPT group)*

Groups community support programs and SMI (Sisters of Mary Immaculate)
community content under one parent menu.

| Submenu | Table(s) | Type |
|---|---|---|
| Community Programs | `wp_community_programs` | CPT list + editor |
| Outreach Events | `wp_community_outreach_events` | Management list |
| Volunteer Signups | `wp_community_volunteer_signups` | Inbox-style list |
| Program Media | `wp_community_program_media` | Media assignment |
| SMI Community Profile | `wp_smi_community_profile` | Single-record settings page |
| SMI Facilities | `wp_smi_facilities` | Management list |
| SMI Community Events | `wp_smi_community_events` | CPT list + editor |
| SMI Event Media | `wp_smi_event_media` | Media assignment |
| Vocation Enquiries | `wp_smi_vocation_enquiries` | Inbox-style list |

**Capability:** `edit_community` (community coordinators; admins)

---

### 13. Gallery (Outlook) *(CPT: `outlook_album`)*

Manages the photo gallery (the "OLLMH Outlook" page).

| Submenu | Table(s) | Type |
|---|---|---|
| Albums | `wp_outlook_albums` | CPT list + editor |
| Gallery Items | `wp_outlook_gallery_items` | Media management list |

**Capability:** `edit_gallery` (editors + admins)

---

### 14. Home Page *(management screens)*

Manages the dynamic content blocks on the home page. No CPT — these are
structured management screens with custom meta boxes.

| Submenu | Table(s) | Type |
|---|---|---|
| Slides | `wp_home_slides` | Slider management (image, caption, link, order) |
| Feature Blocks | `wp_home_feature_blocks` | Tabbed feature blocks management |
| In Focus Items | `wp_home_in_focus_items` | "In Focus" sidebar items management |
| News Promos | `wp_home_news_promos` | News scroller/promo items management |

**Capability:** `edit_home_page` (editors + admins)

---

### 15. Pages *(WordPress core)*

| Submenu | Table(s) | Type |
|---|---|---|
| All Pages | `wp_pages` | Core page list |
| Add New Page | `wp_pages` | Core page editor |

Manages static content pages (Location, Philosophy of Care, Contacts,
Administration, etc.). Each page's body content is stored in `wp_pages`;
page-specific tables (e.g. `wp_location_info`, `wp_care_statements`) are
managed via meta boxes on the page editor or via the Settings page (see
below).

**Capability:** `edit_pages` (editors + admins)

---

### 16. Appearance *(WordPress core + theme customizer)*

| Submenu | Purpose |
|---|---|
| Themes | WordPress core theme management |
| Customize | WordPress Customizer (live preview) |
| Menus | Menu builder — manages `wp_menu_items` (header nav, footer columns) |
| Header | Header layout settings (brand block, CTA button, sticky behavior) |
| Footer | Footer layout settings (5-band structure, newsletter, link columns) |
| Color Scheme | Color palette editor — manages CSS variables from [`COLOR-SCHEMA.md`](./COLOR-SCHEMA.md) |
| Font Schema | Typography editor — manages font stacks/sizes from [`FONT-SCHEMA.md`](./FONT-SCHEMA.md) |

**Capability:** `edit_theme_options` (admins)

---

### 17. Media Library *(WordPress core)*

| Submenu | Table(s) | Type |
|---|---|---|
| Library | `wp_media_assets`, `wp_page_media` | Core media grid/list |
| Add New | `wp_media_assets` | Upload screen |

All images, documents, and files across the site. `wp_page_media` maps
media to pages with roles (hero, gallery, inline, etc.).

**Capability:** `upload_files` (authors + editors + admins)

---

### 18. Plugins *(WordPress core)*

Standard WordPress plugin management. Not mapped to custom tables.

---

### 19. Users *(WordPress core)*

| Submenu | Table(s) | Type |
|---|---|---|
| All Users | `wp_users` | Core user list |
| Add New User | `wp_users` | Core user editor |
| Your Profile | `wp_users` | Current user profile |

**Roles:** Only the five core WordPress roles are used — Administrator,
Editor, Author, Contributor, Subscriber. No custom roles are created. See
[`USER-ROLES.md`](./USER-ROLES.md) for the full role-to-position mapping
and [capability matrix](#capabilityrole-matrix) below.

**Capability:** `list_users` (admins); `read` (own profile for all)

---

### 20. Settings *(WordPress core + custom settings pages)*

| Submenu | Table(s) | Type |
|---|---|---|
| General | WordPress core | Site title, tagline, URL, timezone |
| Platform Config | `wp_settings` | Tabbed settings page — 19 groups: general, homepage, contact, social, clinical, appointments, nursing_school, applications, auth, security, email, notifications, seo, financial, community, profiles, cache, analytics, jobs (see [`SETTINGS.md`](./SETTINGS.md)) |
| Hospital Info | `wp_location_info` | Single-record settings: address, GPS, phone, email, map embed |
| Contact Channels | `wp_contact_channels` | Management list: phone, email, social media, emergency contacts |
| Contact Submissions | `wp_contact_submissions` | Inbox-style list: form submissions from the Contacts page |
| About Facts | `wp_about_facts` | Management list: quick facts about the hospital |
| Milestones | `wp_about_milestones` | Management list: historical milestones/timeline |
| Care Statements | `wp_care_statements` | Management list: philosophy of care statements |
| Care Values | `wp_care_values` | Management list: core care values |
| Governance Bodies | `wp_governance_bodies` | Management list: board/council structures |
| Governance Members | `wp_governance_members` | Management list: individual governance members |
| Reading | WordPress core | Front page display, posts per page |
| Permalinks | WordPress core | URL structure |

**Capability:** `manage_options` (admins). The SEO sub-tab within Platform
Config additionally requires `manage_seo` (granted to Editor via
`add_cap()`; see [`USER-ROLES.md`](./USER-ROLES.md)).

---

## Capability/role matrix

Only the five core WordPress roles are used — no custom roles. See
[`USER-ROLES.md`](./USER-ROLES.md) for the full position-to-role mapping.

| Role | Dashboard | News | Events | Departments | Wards | Clinics/OPD | Special Services | Staff/HR | Nursing School | Applications | Projects | Community | Gallery | Home Page | Pages | Appearance | Media | Users | Settings | SEO |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Administrator** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Editor** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | — | — | ✅ |
| **Author** | ✅ | ✅ (own) | ✅ (own) | — | ✅ (own bookings/enquiries) | ✅ (own bookings/appts) | — | — | — | ✅ (own assigned) | — | ✅ (own signups) | — | — | — | — | ✅ | — | — | — |
| **Contributor** | ✅ | ✅ (own, pending) | ✅ (own, pending) | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| **Subscriber** | ✅ (profile) | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — (own profile) | — | — |

**Legend:** ✅ = full access to that menu's submenus · ✅ (own) = can edit only
own items · ✅ (own, pending) = can create own items but cannot publish ·
✅ (profile) = dashboard access limited to profile page · — = no access

### How operational positions map to this matrix

| OLLMH position | Core role | What they actually do in the admin |
|---|---|---|
| Hospital IT Administrator / Webmaster | **Administrator** | Everything — plugins, themes, users, settings, all content |
| Communications Officer / PR Officer | **Editor** | News, events, gallery, home page, pages, SEO |
| HR Officer / HR Manager | **Editor** | Staff & HR (focused use of Editor's full CPT access) |
| Nursing School Principal / Administrator | **Editor** | Nursing School + Applications |
| Admissions Officer (senior) | **Editor** | Applications pipeline |
| Community Outreach Coordinator | **Editor** | Community programs + SMI content |
| Projects Manager | **Editor** | All three project types |
| Department Head (news contributor) | **Author** | Own news articles and events only |
| Front-Desk Receptionist | **Author** | Own clinic bookings, OPD appointments, admission enquiries |
| Admissions Clerk (junior) | **Author** | Own application records only |
| Clinical Staff (nurses, doctors) | **Author** | Own news contributions |
| Volunteer Coordinator | **Author** | Own volunteer signup records |
| External guest writer (rare) | **Contributor** | Submits news articles for review (no publish, no upload) |
| Patient / Public user (registered) | **Subscriber** | Front-end only — no admin access beyond profile |

---

## CPT registration summary

| CPT slug | Menu parent | Taxonomies | Supports | Icon |
|---|---|---|---|---|
| `news_article` | News | `news_category`, `news_tag` | title, editor, excerpt, thumbnail, revisions, comments | `dashicons-admin-post` |
| `event` | Events | `event_category` | title, editor, excerpt, thumbnail | `dashicons-calendar` |
| `department` | Departments | — | title, editor, excerpt, thumbnail | `dashicons-building` |
| `ward` | Wards & Inpatient | — | title, editor, thumbnail | `dashicons-bed` |
| `clinic` | Clinics & OPD | — | title, editor, excerpt | `dashicons-clock` |
| `special_service` | Special Medical Services | — | title, editor, thumbnail | `dashicons-shield-alt` |
| `staff_member` | Staff & HR | `staff_cadre` | title, editor, thumbnail | `dashicons-groups` |
| `job_vacancy` | Staff & HR | — | title, editor, excerpt | `dashicons-businessperson` |
| `nursing_programme` | Nursing School | — | title, editor, excerpt | `dashicons-welcome-learn-more` |
| `development_project` | Projects | — | title, editor, excerpt, thumbnail | `dashicons-hammer` |
| `sustainability_project` | Projects | — | title, editor, excerpt, thumbnail | `dashicons-palmtree` |
| `upcoming_project` | Projects | — | title, editor, excerpt, thumbnail | `dashicons-lightbulb` |
| `community_program` | Community | — | title, editor, excerpt, thumbnail | `dashicons-heart` |
| `smi_event` | Community | — | title, editor, excerpt, thumbnail | `dashicons-calendar-alt` |
| `outlook_album` | Gallery | — | title, editor, thumbnail | `dashicons-camera` |

---

## Settings page tabs

The **Settings** top-level menu has two kinds of submenus:

### WordPress core settings (standard)
- **General** — site title, tagline, URL, timezone, language
- **Reading** — front page display, posts per page
- **Permalinks** — URL structure
- **Media** — image sizes

### Custom hospital settings (plugin-registered)
These are single-record or short-list management screens for tables that
don't warrant their own CPT but need an admin UI:

| Settings submenu | Table(s) | UI type |
|---|---|---|
| Hospital Info | `wp_location_info` | Single-record form (address, GPS coordinates, phone, email, map embed code) |
| Contact Channels | `wp_contact_channels` | Sortable list (type: phone/email/social/emergency, label, value, icon) |
| Contact Submissions | `wp_contact_submissions` | Inbox table (name, email, subject, message, date, status: new/read/replied) |
| About Facts | `wp_about_facts` | Sortable list (label, value, icon) |
| Milestones | `wp_about_milestones` | Sortable list (year, title, description, image) |
| Care Statements | `wp_care_statements` | Sortable list (heading, body, icon) |
| Care Values | `wp_care_values` | Sortable list (title, description, icon) |
| Governance Bodies | `wp_governance_bodies` | List (name, type: board/council/committee, description) |
| Governance Members | `wp_governance_members` | List (name, body_id FK, role/title, photo, bio) |

---

## Design principles

1. **Group by domain, not by table.** The 81 tables are grouped into 12
   domain-specific top-level menus (News, Events, Departments, Wards &
   Inpatient, Clinics & OPD, Special Medical Services, Staff & HR, Nursing
   School, Applications, Projects, Community, Gallery) plus Home Page
   management. This keeps the sidebar to **20 top-level items** (12 custom +
   8 WordPress core) rather than 80.

2. **CPT for repeatable content, settings for single-record.** Entities that
   have multiple instances (articles, events, departments, wards, staff)
   are registered as CPTs with full list/edit screens. Single-record
   configuration (hospital location, nursing school profile, SMI community
   profile) lives under Settings or as a single-record settings page.

3. **Inbox pattern for submissions.** All public-facing form submissions
   (contact submissions, clinic bookings, OPD appointments, admission
   enquiries, service enquiries, vocation enquiries, volunteer signups,
   pledges) use an inbox-style list with status tracking (new/read/replied)
   so staff can triage them.

4. **Role-based scoping.** Each menu item is gated by a capability mapped
   to one of the five core WordPress roles (no custom roles). Authors see
   only their own bookings and articles; Editors see all content menus;
   Subscribers see only their profile. This prevents sidebar overload for
   non-admin users. See [`USER-ROLES.md`](./USER-ROLES.md).

5. **Dashboard widgets for triage.** The dashboard surfaces actionable
   counts (pending applications, today's bookings, new enquiries) so staff
   don't have to hunt through menus to find what needs attention.

6. **Appearance submenus for theme config.** Header layout, footer layout,
   color scheme, and font schema are managed under Appearance, keeping all
   visual/branding configuration in one place — consistent with WordPress
   conventions.
