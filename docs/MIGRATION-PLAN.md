# Migration Plan

> This document is the step-by-step plan for converting the static archived
> OLLMH website (Joomla 3.x, TX Finnix template, March 2022 Wayback
> snapshot) into a dynamic WordPress website.
>
> **Related:** [`CONTENT-MIGRATION.md`](./CONTENT-MIGRATION.md) for content
> extraction details, [`ASSET-MIGRATION.md`](./ASSET-MIGRATION.md) for
> image/PDF handling, [`URL-MAPPING.md`](./URL-MAPPING.md) for redirects.

---

## Overview

The migration has 7 phases, each with clear entry/exit criteria. Phases
1–3 are setup, 4–6 are content migration, and 7 is launch.

| Phase | Name | Duration estimate | Depends on |
|---|---|---|---|
| 1 | Environment setup | — | — |
| 2 | Plugin + theme scaffolding | — | Phase 1 |
| 3 | Database tables + seeders | — | Phase 2 |
| 4 | Asset migration | — | Phase 1 |
| 5 | Content migration | — | Phases 3, 4 |
| 6 | Front-end forms + integrations | — | Phases 2, 3 |
| 7 | Testing + launch | — | Phases 5, 6 |

---

## Phase 1: Environment setup

**Goal:** A working local WordPress development environment.

**Steps:**
1. Install Docker and Docker Compose (see [`ENVIRONMENT-SETUP.md`](./ENVIRONMENT-SETUP.md))
2. Clone the project repository
3. Run `docker-compose up -d` to start WordPress + MySQL + phpMyAdmin
4. Complete the WordPress installation wizard
5. Configure `wp-config.php` with proper salts and debug settings
6. Install the 6 third-party plugins (Rank Math, Site Kit, Redirection, WP Rocket, Broken Link Checker, Schema Markup)
7. Verify the site loads at `http://localhost:8080`

**Exit criteria:** WordPress loads locally, database is accessible, plugins installed.

---

## Phase 2: Plugin + theme scaffolding

**Goal:** Custom plugins and theme are active with empty but functional structure.

**Steps:**
1. Create the `ollmh-theme` directory in `wp-content/themes/` (see [`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md))
2. Create `style.css`, `functions.php`, `theme.json`, `header.php`, `footer.php`, `index.php`
3. Activate the theme
4. Create the 4 custom plugins in `wp-content/plugins/` (see [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md)):
   - `ollmh-core` — activate first
   - `ollmh-forms` — activate after core
   - `ollmh-payments` — activate after core
   - `ollmh-notifications` — activate after core
5. Verify all 4 plugins activate without errors
6. Register CPTs and taxonomies (see [`CPT-REGISTRATION-CODE.md`](./CPT-REGISTRATION-CODE.md))
7. Flush rewrite rules
8. Verify CPT admin menus appear in the sidebar

**Exit criteria:** Theme is active, all 4 plugins are active, CPT admin menus visible.

---

## Phase 3: Database tables + seeders

**Goal:** All 81 custom tables exist and are seeded with initial data.

**Steps:**
1. Write the `OLLMH_Activator` class with all `CREATE TABLE` statements (SQL from [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md) + per-page docs)
2. Run plugin activation to create tables via `dbDelta()`
3. Verify all 81 tables exist (check via phpMyAdmin or `wp db` CLI)
4. Run the settings seeder (`OLLMH_Settings_Seeder`) — populates `wp_settings` with ~100 defaults
5. Write and run content seeders:
   - `OLLMH_Departments_Seeder` — seed departments from archived site
   - `OLLMH_Staff_Seeder` — seed staff from archived site
   - `OLLMH_Pages_Seeder` — create WordPress pages with correct slugs and page templates
   - `OLLMH_Menu_Seeder` — seed `wp_menu_items` and create WordPress nav menus
6. Verify seed data in the admin (departments, staff, pages, menus all visible)
7. Configure hospital settings via the Platform Config admin page (phone, email, address, GPS, social links — see [`SETTINGS.md`](./SETTINGS.md))

**Exit criteria:** 81 tables exist, settings seeded, pages created with correct slugs, menus populated.

---

## Phase 4: Asset migration

**Goal:** All images from the archived site are in the WordPress media library.

**Steps:**
1. Run the asset migration script (see [`ASSET-MIGRATION.md`](./ASSET-MIGRATION.md))
2. The script scans `web.archive.org/.../images/` for all image files (~133 images)
3. Each image is:
   - Renamed to a clean, descriptive filename (remove URL encoding, spaces, mixed case)
   - Uploaded to WordPress via `media_handle_sideload()` → enters `wp_media_assets`
   - Given alt text (manually or AI-assisted — most archived images have empty alt)
4. Verify all images appear in the WordPress Media Library
5. Manually upload the 3 referenced-but-missing PDFs (application forms) if available from the hospital
6. Set the default Open Graph image (`seo_default_og_image_id` setting)

**Exit criteria:** All archived images are in the WordPress media library with clean filenames and alt text.

---

## Phase 5: Content migration

**Goal:** All page content from the archived site is in WordPress, structured into CPTs and custom tables.

**Steps:**
1. Run the content migration script (see [`CONTENT-MIGRATION.md`](./CONTENT-MIGRATION.md))
2. For each of the 17 fully-archived pages:
   - Extract the main content area from the HTML (strip Joomla template chrome)
   - Clean the HTML (remove inline styles, deprecated attributes, Joomla-specific classes)
   - Insert into the appropriate WordPress page or CPT
   - Replace image references with WordPress media library URLs
   - Replace internal links with new WordPress URLs
3. For the 3 placeholder pages (in-patient-dept, clinic-days, about-nursing-school):
   - Create content from the homepage department showcase sections
   - Source missing content from the hospital administration
4. Migrate news articles into `news_article` CPT (from the news-events page and any linked articles)
5. Migrate events into `event` CPT
6. Migrate departments into `department` CPT (from the departments page)
7. Migrate staff into `staff_member` CPT (from the HR capacity page)
8. Migrate projects into `development_project`, `sustainability_project`, `upcoming_project` CPTs
9. Migrate community programs into `community_program` CPT
10. Migrate gallery images into `outlook_album` CPT
11. Verify all content renders correctly on the front-end

**Exit criteria:** All 20 pages have content, all CPTs are populated, front-end pages render with correct content.

---

## Phase 6: Front-end forms + integrations

**Goal:** All interactive forms and third-party integrations are functional.

**Steps:**
1. Build the contact form (see [`FRONT-END-FORMS.md`](./FRONT-END-FORMS.md))
   - Front-end form with Turnstile captcha
   - REST API endpoint (`/ollmh/v1/contact`)
   - Email notification to `admin_email` setting
   - Auto-reply to sender
   - Save to `wp_contact_submissions`
2. Build the appointment booking form
   - Clinic/department dropdown
   - Date/time picker (respecting `appointment_advance_days` and `appointment_min_lead_hours` settings)
   - Turnstile captcha
   - REST API endpoint (`/ollmh/v1/appointments`)
   - Email confirmation to patient
   - Save to `wp_opd_appointments` or `wp_clinic_bookings`
3. Build the nursing school application form (multi-step)
   - Step 1: Personal information
   - Step 2: Academic information
   - Step 3: Document upload (photo, transcripts, ID copy)
   - Step 4: Review and submit + M-Pesa payment
   - REST API endpoints (`/ollmh/v1/applications`, `/ollmh/v1/applications/upload`)
   - Save to `wp_applicants` + `wp_applications` + `wp_application_documents`
   - M-Pesa STK Push for application fee
   - Email confirmation to applicant
   - Notification to `nursing_school_email`
4. Build the event registration form
   - REST API endpoint (`/ollmh/v1/events/register`)
   - Save to `wp_event_registrations`
   - Email confirmation
5. Configure SMTP (see [`SETTINGS.md`](./SETTINGS.md) → `email` group)
6. Configure M-Pesa (see [`SETTINGS.md`](./SETTINGS.md) → `financial` group)
   - Start with sandbox environment
   - Test STK Push flow end-to-end
   - Switch to production when ready
7. Configure Cloudflare Turnstile (see [`SETTINGS.md`](./SETTINGS.md) → `security` group)
8. Configure SMS gateway (if SMS notifications enabled)
9. Set up cron jobs (see [`CRON-JOBS.md`](./CRON-JOBS.md))
10. Set up email templates (see [`EMAIL-TEMPLATES.md`](./EMAIL-TEMPLATES.md))

**Exit criteria:** All forms submit successfully, emails send, M-Pesa works in sandbox, Turnstile validates, cron jobs scheduled.

---

## Phase 7: Testing + launch

**Goal:** Site is tested, deployed, and live.

**Steps:**
1. Run the full testing checklist (see [`TESTING-PLAN.md`](./TESTING-PLAN.md))
2. Set up redirects (see [`URL-MAPPING.md`](./URL-MAPPING.md))
   - Configure 17 `.html` → WordPress URL redirects in the Redirection plugin
   - Test each redirect returns 301
3. Configure SEO (see [`SEO-STRATEGY.md`](./SEO-STRATEGY.md))
   - Set up Rank Math (meta titles, descriptions, schema)
   - Connect Google Site Kit (Search Console, Analytics, AdSense)
   - Generate XML sitemap
   - Submit sitemap to Google Search Console
4. Performance optimization (see [`PERFORMANCE-BUDGET.md`](./PERFORMANCE-BUDGET.md))
   - Configure WP Rocket (caching, minification, lazy loading)
   - Optimize images (convert to WebP)
   - Test Core Web Vitals
5. Security hardening (see [`SECURITY-HARDENING.md`](./SECURITY-HARDENING.md))
   - Set up SSL
   - Configure file permissions
   - Install security plugin (Wordfence or Solid Security)
   - Set up Cloudflare (DNS, WAF, DDoS protection)
6. Accessibility audit (see [`ACCESSIBILITY.md`](./ACCESSIBILITY.md))
7. Set up backup system (see [`BACKUP-RECOVERY.md`](./BACKUP-RECOVERY.md))
8. Deploy to production (see [`DEPLOYMENT.md`](./DEPLOYMENT.md))
9. Configure production DNS and SSL
10. Switch M-Pesa from sandbox to production
11. Post-launch monitoring (24–48 hours of active monitoring)

**Exit criteria:** Site is live at the production domain, all redirects work, SEO tools connected, backups running, monitoring active.

---

## Migration order dependency graph

```
Phase 1 (Environment)
    ├── Phase 4 (Assets) — can run in parallel with Phase 2
    └── Phase 2 (Plugins + Theme)
            └── Phase 3 (Database + Seeders)
                    ├── Phase 5 (Content) — needs assets + tables
                    └── Phase 6 (Forms) — needs tables + plugins
                            └── Phase 7 (Testing + Launch) — needs everything
```

**Parallelization opportunity:** Phase 4 (asset migration) can run
concurrently with Phase 2 (plugin/theme scaffolding) since it only needs
the WordPress install from Phase 1.
