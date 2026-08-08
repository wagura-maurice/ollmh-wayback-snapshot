# OLLMH Website Documentation

Analysis and rebuild blueprint for the archived **Our Lady of Lourdes Mwea
Hospital (OLLMH)** website (Wayback Machine snapshot `20220319205345`).

This documentation maps every page reachable from the site's header/footer
navigation, assesses gaps, and designs a MySQL schema to move the site from a
static archive to a **fully dynamic, database-driven application**.

## Contents

- **[`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md)** —
  formal architectural decision records (ADRs) for the OLLMH rebuild:
  **ADR-001** child theme extending Twenty Twenty-Five (block/FSE),
  **ADR-002** Cloudflare Turnstile with vanilla JavaScript,
  **ADR-003** no Tailwind CSS (pure CSS and native WordPress styling),
  **ADR-004** M-Pesa Daraja G2 API as optional modular integration
  (pending client approval, cPanel feasibility confirmed),
  **ADR-005** WP-CLI available in development only, not production
  (cPanel shared hosting — production-safe alternatives documented for
  every WP-CLI task). **Read this first** — these decisions supersede
  any conflicting guidance in other documentation files.
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
  pages, and management screens, with a capability/role matrix for the 5
  core WordPress roles.
- **[`USER-ROLES.md`](./USER-ROLES.md)** — confirmation of the 6 default
  WordPress user roles (Super Admin, Administrator, Editor, Author,
  Contributor, Subscriber), how each core role functions, and a mapping of
  every OLLMH staff position (IT admin, communications, HR, nursing school
  admin, admissions, receptionist, community coordinator, clinical staff,
  patients) to one of the 5 core single-site roles — **no custom roles are
  created**. Includes a capability matrix, CPT capability additions via
  `add_cap()`, role-assignment workflow, optional granular scoping within
  a core role, and PHP registration code.
- **[`SEO-STRATEGY.md`](./SEO-STRATEGY.md)** — the complete SEO tool stack
  (10 layers: on-page SEO plugin, Google integration via Site Kit,
  medical-specific schema markup, redirect & 404 management, performance &
  Core Web Vitals, broken link monitoring, keyword research, XML sitemaps,
  social/Open Graph, and optional SEO data warehouse), 7 new SEO-specific
  database tables with seed data requirements, a seed-to-tool integration
  map, a 3-phase implementation plan (pre-launch, launch, post-launch),
  JSON-LD seed templates for Hospital/Physician/Event schema, and an admin
  sidebar SEO menu.
- **[`SETTINGS.md`](./SETTINGS.md)** — the complete `wp_settings` catalogue:
  a central key-value configuration table with ~100 settings across 19
  groups (general, homepage, contact, social, clinical, appointments,
  nursing school, applications, auth, security, email, notifications, SEO,
  financial/M-Pesa, community, profiles, cache, analytics, jobs). Includes
  the table schema, column reference, per-group settings tables, admin UI
  rendering rules, front-end API contract, and relationship to existing
  structured tables. The PHP seeder is at
  [`seeders/class-ollmh-settings-seeder.php`](../seeders/class-ollmh-settings-seeder.php).

### Implementation documentation

- **[`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md)** — classic PHP theme
  structure: directory layout, template hierarchy mapping (20 page types →
  WordPress templates), `functions.php` bootstrap, `theme.json` design
  tokens, image sizes, menu locations, widget areas, theme-vs-plugin
  division of labor, and CSS/JS architecture.
- **[`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md)** — 4 custom
  plugins (`ollmh-core`, `ollmh-forms`, `ollmh-payments`, `ollmh-notifications`):
  directory structure, activation/deactivation/uninstall sequences, REST API
  endpoints, M-Pesa STK Push flow, email/SMS queue, and plugin dependency
  order.
- **[`CPT-REGISTRATION-CODE.md`](./CPT-REGISTRATION-CODE.md)** — actual PHP
  `register_post_type()` and `register_taxonomy()` code for all 15 CPTs and
  4 taxonomies, with labels, rewrite slugs, menu icons, capabilities, and
  `map_meta_cap` configuration.
- **[`MIGRATION-PLAN.md`](./MIGRATION-PLAN.md)** — 7-phase plan for
  converting the static Joomla archive to dynamic WordPress: environment
  setup → plugin/theme scaffolding → database/seeders → asset migration →
  content migration → forms/integrations → testing/launch, with entry/exit
  criteria and a dependency graph.
- **[`CONTENT-MIGRATION.md`](./CONTENT-MIGRATION.md)** — how to extract
  content from archived HTML, clean Joomla-specific markup, convert image
  URLs and internal links, and insert into WordPress pages and CPTs.
  Includes a WP-CLI migration script (dev-only — see ADR-005) with HTML
  extraction, cleaning, and URL conversion functions.
- **[`ASSET-MIGRATION.md`](./ASSET-MIGRATION.md)** — how to migrate ~133
  images from the archive into the WordPress media library: filename
  cleaning, alt text assignment, WebP conversion, logo/favicon handling,
  and a WP-CLI migration script (dev-only — see ADR-005) with URL
  mapping file generation.
- **[`ENVIRONMENT-SETUP.md`](./ENVIRONMENT-SETUP.md)** — local development
  environment with Docker Compose (WordPress + MySQL + phpMyAdmin +
  MailHog), first-time setup commands, daily workflow, `wp-config.php`
  settings, database access, and troubleshooting.
- **[`URL-MAPPING.md`](./URL-MAPPING.md)** — complete redirect map from 20
  old Joomla `.html` URLs to new WordPress permalinks, with Redirection
  plugin CSV import, `.htaccess` rules, CPT URL structure, and
  post-launch verification.
- **[`REST-API-SPEC.md`](./REST-API-SPEC.md)** — all custom REST API
  endpoints: contact, appointment booking, multi-step nursing school
  application, document upload, M-Pesa callback, event registration, public
  settings retrieval, and Turnstile verification. Includes authentication,
  rate limiting, and error response format.
- **[`FRONT-END-FORMS.md`](./FRONT-END-FORMS.md)** — specifications for all
  4 front-end forms (contact, appointment, application, event registration):
  field definitions, validation rules, Turnstile integration, AJAX
  submission flow, success/error states, and the multi-step application
  form with progress indicator.
- **[`JAVASCRIPT-INTERACTIVITY.md`](./JAVASCRIPT-INTERACTIVITY.md)** —
  replacement strategy for archived Joomla JS components (XpertSlider →
  Swiper.js, XpertTabs → vanilla JS, XpertScroller → CSS scroll-snap,
  MaximenuCK → CSS hover + JS mobile toggle, EqualHeight → CSS Flexbox),
  with implementation code, HTML structure, and loading strategy.
- **[`RESPONSIVE-DESIGN.md`](./RESPONSIVE-DESIGN.md)** — mobile-first
  responsive strategy: 5 breakpoints (base/640/768/1024/1280px), CSS Grid
  system, sticky header, mobile hamburger menu, responsive images with
  `srcset`, responsive tables, responsive forms, fluid typography with
  `clamp()`, and browser support matrix.
- **[`DEPLOYMENT.md`](./DEPLOYMENT.md)** — production deployment: hosting
  requirements, domain/DNS/SSL configuration, staging→production workflow,
  production `wp-config.php`, Nginx and Apache configurations, file
  permissions, and post-deployment checklist.
- **[`EMAIL-TEMPLATES.md`](./EMAIL-TEMPLATES.md)** — all transactional email
  templates (contact auto-reply, contact admin notification, appointment
  confirmation, appointment reminder, application received, application
  status update, event registration, password reset) and SMS templates,
  with a shared HTML email wrapper and template variable reference.
- **[`CRON-JOBS.md`](./CRON-JOBS.md)** — all 12 scheduled tasks (notification
  queue, appointment reminders, event reminders, transient cleanup, log
  pruning, job pruning, DB optimization, sitemap regeneration, broken link
  check, backups, application expiry, cache clear), with WP-Cron vs system
  cron configuration and PHP registration code.
- **[`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md)** —
  dependency policy (minimize, no jQuery for theme code, no Bootstrap/
  Tailwind, no build step required), CSS dependencies (Swiper, GLightbox),
  JS dependencies, SVG icon system, system font stack, version pinning
  with SRI, and what to explicitly avoid.
- **[`TESTING-PLAN.md`](./TESTING-PLAN.md)** — testing strategy across 5
  phases (unit, integration, UAT, pre-launch, post-launch): database, CPT,
  theme, forms, notifications, admin, cross-browser, mobile, SEO,
  performance, security, accessibility, content verification, and 48-hour
  post-launch monitoring.
- **[`ACCESSIBILITY.md`](./ACCESSIBILITY.md)** — WCAG 2.1 Level AA
  compliance: text alternatives, color contrast (per OLLMH palette),
  keyboard navigation, focus indicators, touch targets, form labels, ARIA
  usage, `prefers-reduced-motion`, WordPress-specific accessibility, and
  testing tools.
- **[`PERFORMANCE-BUDGET.md`](./PERFORMANCE-BUDGET.md)** — Core Web Vitals
  targets (LCP < 2.5s, INP < 200ms, CLS < 0.1), page weight budget (< 700KB
  first view), image optimization (WebP, responsive srcset, lazy loading),
  CSS/JS optimization, caching strategy (WP Rocket, Redis, Cloudflare CDN),
  database optimization, server tuning, and monitoring.
- **[`SECURITY-HARDENING.md`](./SECURITY-HARDENING.md)** — 5-layer security
  strategy (Cloudflare edge, WordPress application, server, data,
  monitoring): WAF, DDoS protection, `wp-config.php` hardening, XML-RPC
  disable, login security, SQL injection/XSS/CSRF prevention, file upload
  security, secret encryption, HTTP security headers, file permissions,
  security plugins, update policy, and incident response.
- **[`BACKUP-RECOVERY.md`](./BACKUP-RECOVERY.md)** — backup strategy (daily
  database, weekly files, server snapshots), 3-2-1 storage rule, recovery
  procedures (full site, database-only, single table, file-only), RTO/RPO
  targets, monthly backup verification, and disaster recovery plan for
  server failure, database corruption, hack, and accidental deletion.
- **[`COOKIE-CONSENT.md`](./COOKIE-CONSENT.md)** — cookie consent strategy
  compliant with Kenya's Data Protection Act 2019: 3 cookie categories
  (essential, analytics, advertising), consent banner with Accept All /
  Reject All / Cookie Settings, per-category toggles, JavaScript
  implementation for conditional script loading, `wp_cookie_consents`
  audit trail table, settings, and Cookie Policy page content outline.
- **[`SHORTCODES.md`](./SHORTCODES.md)** — all 15 custom shortcodes
  (`[ollmh_clinic_schedule]`, `[ollmh_department_list]`, `[ollmh_staff_grid]`,
  `[ollmh_ward_status]`, `[ollmh_contact_form]`, `[ollmh_appointment_form]`,
  `[ollmh_application_form]`, `[ollmh_event_registration]`,
  `[ollmh_newsletter_form]`, `[ollmh_upcoming_events]`, `[ollmh_latest_news]`,
  `[ollmh_social_links]`, `[ollmh_hospital_hours]`, `[ollmh_breadcrumbs]`,
  `[ollmh_gallery]`) with parameters, usage examples, HTML output, and PHP
  registration code.
- **[`pages/`](./pages/)** — one standalone documentation file per page, each
  with: **1. Current State Mapping**, **2. Gap Analysis & Feature
  Enhancements**, **3. Database Schema Design**. The News and Events sections
  are split into individual per-entry pages under [`pages/news/`](./pages/news/)
  and [`pages/events/`](./pages/events/) (see below). New pages created for
  the WordPress build (not in the archive) are documented in
  [`pages/patient-information.md`](./pages/patient-information.md),
  [`pages/faq.md`](./pages/faq.md),
  [`pages/privacy-policy.md`](./pages/privacy-policy.md),
  [`pages/terms-of-service.md`](./pages/terms-of-service.md), and
  [`pages/data-protection.md`](./pages/data-protection.md).

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
| Patient Information | [patient-information.md](./pages/patient-information.md) | 🆕 New page (footer → Support) |
| FAQ | [faq.md](./pages/faq.md) | 🆕 New page (footer → Support) |
| Privacy Policy | [privacy-policy.md](./pages/privacy-policy.md) | 🆕 New page (footer → Legal) |
| Terms of Service | [terms-of-service.md](./pages/terms-of-service.md) | 🆕 New page (footer → Legal) |
| Data Protection | [data-protection.md](./pages/data-protection.md) | 🆕 New page (footer → Legal) |

**Legend:** Real content = archived page has substantive content · ⚠️ =
content present but title/functionality mismatch to address in rebuild · ❌ =
no real content captured; page must be built from scratch · 🆕 = new page
created for the WordPress build (not in the archive).

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
