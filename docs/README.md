# OLLMH Website Documentation

Analysis and rebuild blueprint for the archived **Our Lady of Lourdes Mwea
Hospital (OLLMH)** website (Wayback Machine snapshot `20220319205345`).

This documentation maps every page reachable from the site's header/footer
navigation, assesses gaps, and designs a MySQL schema to move the site from a
static archive to a **fully dynamic, database-driven application**.

## Contents

- **[`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md)** — shared, platform-wide
  tables (`wp_pages`, `wp_media_assets`, `wp_page_media`, `wp_users`, `wp_menu_items`,
  `wp_departments`, `wp_staff`) and conventions that every per-page schema references
  via foreign keys. **Read this first** — page files define only their own
  tables and FK into these.
- **[`ERD.md`](./ERD.md)** — consolidated entity-relationship diagram covering
  all **80 tables** and **116 foreign keys** across the platform, grouped into
  8 logical clusters with Mermaid `erDiagram` blocks that render inline on
  GitHub.
- **[`header-footer-links.md`](./header-footer-links.md)** — the extracted
  inventory of every hyperlink in the header navigation and footer.
- **[`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md)** — the
  WordPress header (top navigation) and footer information architecture:
  menu hierarchy, sub-pages, labels, footer columns, and the mapping of every
  item to `wp_menu_items` rows.
- **[`COLOR-SCHEMA.md`](./COLOR-SCHEMA.md)** — the complete color palette
  extracted from the archived site's CSS, organized into primary, secondary,
  accent, background, text, border, and inline content colors with hex codes,
  CSS source selectors, WordPress CSS variables, and a `theme.json` palette.
- **[`FONT-SCHEMA.md`](./FONT-SCHEMA.md)** — the complete typography
  reference extracted from the archived site's CSS and inline HTML styles:
  every `font-family` stack, type scale (`font-size`), weights, styles, line
  heights, per-page inline usage, WordPress CSS variables, and a
  `theme.json` typography configuration.
- **[`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md)** — the complete WordPress
  admin sidebar menu structure: 20 top-level items (12 custom + 8 core)
  mapping all 80 database tables into CPTs, custom taxonomies, settings
  pages, and management screens, with a capability/role matrix for 8 custom
  user roles.
- **[`USER-ROLES.md`](./USER-ROLES.md)** — confirmation and explanation of
  the 6 default WordPress user roles (Super Admin, Administrator, Editor,
  Author, Contributor, Subscriber), their mapping to OLLMH operational
  needs, a redundancy analysis (which defaults are utilized vs. redundant),
  and full definitions of 6 custom roles (hospital_admin, hr_manager,
  nursing_admin, admissions_officer, receptionist, community_coordinator)
  with capabilities, admin-sidebar access, a combined capability matrix,
  role-assignment workflow, and PHP registration code.
- **[`SEO-STRATEGY.md`](./SEO-STRATEGY.md)** — the complete SEO tool stack
  (10 layers: on-page SEO plugin, Google integration via Site Kit,
  medical-specific schema markup, redirect & 404 management, performance &
  Core Web Vitals, broken link monitoring, keyword research, XML sitemaps,
  social/Open Graph, and optional SEO data warehouse), 7 new SEO-specific
  database tables with seed data requirements, a seed-to-tool integration
  map, a 3-phase implementation plan (pre-launch, launch, post-launch),
  JSON-LD seed templates for Hospital/Physician/Event schema, and an admin
  sidebar SEO menu.
- **[`pages/`](./pages/)** — one standalone documentation file per page, each
  with: **1. Current State Mapping**, **2. Gap Analysis & Feature
  Enhancements**, **3. Database Schema Design**. The News and Events sections
  are split into individual per-entry pages under [`pages/news/`](./pages/news/)
  and [`pages/events/`](./pages/events/) (see below).

## Page index

The **Content status** column flags how faithful the archived page is to its
title — a key input for the rebuild.

| Page | Doc | Content status |
| --- | --- | --- |
| Home | [index.md](./pages/index.md) | Real content (slideshow, In Focus, tabs, news scroller, dept columns) |
| Location | [about-ollmh-location.md](./pages/about-ollmh-location.md) | Real content |
| Admin menu (Administration) | [administration.md](./pages/administration.md) | Real content |
| Our Philosophy Of Care | [philosophy-of-care.md](./pages/philosophy-of-care.md) | Real content |
| HR-Capacity (Staff) | [hr-capacity-wp_staff.md](./pages/hr-capacity-wp_staff.md) | Real content |
| Hospital Development | [development-projects.md](./pages/development-projects.md) | Real content |
| Self Sustainability Projects | [self-sustainability-projects.md](./pages/self-sustainability-projects.md) | Real content |
| Community Support | [community-support.md](./pages/community-support.md) | Real content |
| Upcoming Projects | [upcoming-projects.md](./pages/upcoming-projects.md) | Real content (text only) |
| Out Patient Department | [out-patient-dept.md](./pages/out-patient-dept.md) | Real content |
| Wards | [wp_wards.md](./pages/wp_wards.md) | Real content |
| Ollmh Outlook | [ollmh-outlook.md](./pages/ollmh-outlook.md) | Real content (photo gallery) |
| Ollmh Departments | [ollmh-wp_departments.md](./pages/ollmh-wp_departments.md) | Real content (photo grid) |
| S.M.I Community | [smi-community.md](./pages/smi-community.md) | Real content |
| Contacts | [contacts.md](./pages/contacts.md) | ⚠️ No form/map; email JS-cloaked |
| Special Medical Services | [special-medical-services.md](./pages/special-medical-services.md) | ⚠️ Mislabeled — in-body heading is "Inpatient Department (Nursing Application)" |
| News (listing) | [news/index.md](./pages/news/index.md) | ⚠️ Mislabeled — a nursing-school advert, not a news feed |
| News article: Nursing School Launch | [news/nursing-school-promo.md](./pages/news/nursing-school-promo.md) | Migrated from archive (standalone article page) |
| News article template | [news/article-template.md](./pages/news/article-template.md) | Reusable template for all article pages |
| Events (calendar) | [events/index.md](./pages/events/index.md) | ❌ No events in archive; built from scratch |
| Event page template | [events/event-template.md](./pages/events/event-template.md) | Reusable template for all event pages |
| ~~New & Events~~ (split) | [news-wp_events.md](./pages/news-wp_events.md) | Redirect note — content moved to `news/` and `events/` |
| Medical School Application Form | [medical-school-application-form.md](./pages/medical-school-application-form.md) | ⚠️ Not a form — only a PDF download link |
| About The Nursing School | [about-nursing-school.md](./pages/about-nursing-school.md) | ❌ Placeholder stub (not archived) |
| Clinic Days | [clinic-days.md](./pages/clinic-days.md) | ❌ Placeholder stub (not archived) |
| In Patient Dept | [in-patient-dept.md](./pages/in-patient-dept.md) | ❌ Placeholder stub (not archived) |

**Legend:** Real content = archived page has substantive content · ⚠️ =
content present but title/functionality mismatch to address in rebuild · ❌ =
no real content captured; page must be built from scratch.

## How the schema fits together

Every page-specific table foreign-keys into `pages(id)` and, where relevant,
into other shared tables (`wp_media_assets`, `wp_departments`, `wp_staff`, `wp_users`).
Cross-page integrations are noted in the individual files — for example the
[application form](./pages/medical-school-application-form.md) links applicants
to nursing programmes defined in
[About The Nursing School](./pages/about-nursing-school.md), and both the
[contacts](./pages/contacts.md) and department pages route through the shared
`wp_departments` catalogue. See each file's **Relationships** subsection for
details.

For the full visual map of all 80 tables and 116 foreign keys, see the
**[consolidated ERD](./ERD.md)**, which groups the schema into 8 logical
clusters (Platform core, Home, News, Events, Nursing & Applications,
Departments/Wards/Clinical, Projects/Community, About/Admin) with Mermaid
diagrams that render inline on GitHub.
