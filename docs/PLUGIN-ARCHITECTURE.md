# Plugin Architecture

> This document defines the WordPress plugin architecture for the OLLMH
> rebuild — which custom functionality lives in plugins (survives theme
> switches) vs. the theme (presentation only).
>
> **Related:** [`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md) for the
> theme side, [`CPT-REGISTRATION-CODE.md`](./CPT-REGISTRATION-CODE.md) for
> the actual registration PHP, [`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md) for
> the admin menu structure.

---

## 1. Plugin inventory

Three **core** custom plugins handle OLLMH-specific functionality, plus
one **optional** plugin for M-Pesa payments:

| Plugin | Slug | Status | Purpose | Tables managed |
|---|---|---|---|---|
| **OLLMH Core** | `ollmh-core` | Core (required) | CPT/taxonomy registration, settings UI, capability management, cron jobs, database table creation | All 81 tables (creation), `wp_settings` (admin UI) |
| **OLLMH Forms** | `ollmh-forms` | Core (required) | Front-end form handlers (contact, appointment, application, event registration) via REST API | `wp_contact_submissions`, `wp_clinic_bookings`, `wp_opd_appointments`, `wp_applications`, `wp_applicants`, `wp_application_*`, `wp_event_registrations` |
| **OLLMH Notifications** | `ollmh-notifications` | Core (required) | Transactional email + SMS sending (appointment reminders, application status updates, contact auto-replies) | None (reads from settings, sends via SMTP/SMS gateway) |
| **OLLMH Payments** | `ollmh-payments` | **Optional** (pending client approval) | M-Pesa Daraja G2 API integration (STK Push) for application fees | `wp_application_payments` |

> **Architectural decision:** The M-Pesa payment integration is an
> optional, modular feature — see
> [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md) → ADR-004
> for the full context, rationale, and cPanel feasibility analysis.
> The `ollmh-payments` plugin can be activated or deactivated
> independently. When inactive, the application form operates without
> online payment (applicants pay offline).

**Plus 6 third-party plugins** (see [`SEO-STRATEGY.md`](./SEO-STRATEGY.md)):
Rank Math, Site Kit by Google, Redirection, WP Rocket, Broken Link Checker,
and optionally Schema Markup for Medical Business.

---

## 2. `ollmh-core` — Core plugin

### Directory structure

```
ollmh-core/
├── ollmh-core.php              # Main plugin file (header, activation/deactivation hooks)
├── includes/
│   ├── class-ollmh-activator.php    # Activation: create tables, seed settings, add caps
│   ├── class-ollmh-deactivator.php  # Deactivation: remove caps (keeps tables and data)
│   ├── class-ollmh-uninstaller.php  # Uninstall: drop tables, remove options (multisite-safe)
│   ├── class-ollmh-cpt.php          # register_post_type() and register_taxonomy() calls
│   ├── class-ollmh-settings.php     # wp_settings admin page (tabbed, grouped by group_name)
│   ├── class-ollmh-capabilities.php # add_cap() to core roles (Editor, Author, Contributor)
│   ├── class-ollmh-cron.php         # wp_schedule_event() registrations
│   ├── class-ollmh-meta-boxes.php   # Custom meta boxes for CPTs (ward bed status, clinic schedule, etc.)
│   ├── class-ollmh-admin-columns.php # Custom admin list table columns for CPTs
│   ├── class-ollmh-shortcodes.php   # Shortcodes for front-end embedding ([ollmh_clinic_schedule], etc.)
│   └── class-ollmh-helpers.php      # Shared utility functions (get_setting(), render_inbox(), etc.)
├── seeders/
│   ├── class-seeder-base.php            # Abstract base class (already created)
│   ├── class-ollmh-settings-seeder.php  # Settings seeder (already created)
│   ├── class-ollmh-departments-seeder.php  # Departments seed
│   ├── class-ollmh-staff-seeder.php        # Staff seed
│   ├── class-ollmh-pages-seeder.php        # Pages seed
│   └── class-ollmh-menu-seeder.php         # Menu items seed
├── assets/
│   ├── css/admin.css           # Admin page styling
│   └── js/admin.js             # Admin page JS (settings tabs, meta box interactions)
├── languages/                  # .pot file for i18n
└── uninstall.php              # WordPress uninstall hook entry point
```

### Activation sequence

On plugin activation (`register_activation_hook`):

1. **Create all 81 database tables** via `dbDelta()` — SQL from
   [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md) and per-page docs.
2. **Run the settings seeder** — populates `wp_settings` with ~100 defaults
   (see [`seeders/class-ollmh-settings-seeder.php`](../seeders/class-ollmh-settings-seeder.php)).
3. **Run content seeders** — populates `wp_departments`, `wp_staff`,
   `wp_pages`, `wp_menu_items` with seed data from the archived site.
4. **Add CPT capabilities to core roles** — `add_cap()` calls for Editor,
   Author, Contributor (see [`USER-ROLES.md`](./USER-ROLES.md) for the full
   capability list).
5. **Register cron jobs** — `wp_schedule_event()` for daily/weekly tasks
   (see [`CRON-JOBS.md`](./CRON-JOBS.md)).
6. **Set default options** — `update_option('ollmh_core_version', '1.0.0')`,
   set default permalink structure if not already set.
7. **Flush rewrite rules** — `flush_rewrite_rules()` so CPT URLs work.

### Deactivation sequence

On plugin deactivation (`register_deactivation_hook`):

1. **Remove CPT capabilities from core roles** — `remove_cap()` calls.
2. **Clear cron schedules** — `wp_clear_scheduled_hook()`.
3. **Flush rewrite rules**.
4. **Do NOT drop tables** — data is preserved in case of reactivation.

### Uninstall sequence

On plugin uninstall (`uninstall.php`):

1. **Drop all 81 custom tables** — `DROP TABLE IF EXISTS`.
2. **Remove all options** — `delete_option('ollmh_*')`.
3. **Remove all transients** — `delete_transient('ollmh_*')`.
4. **Remove CPT capabilities from core roles**.

> **Warning:** Uninstall is irreversible. Only run when permanently removing
> the plugin. Deactivation preserves data; uninstall destroys it.

---

## 3. `ollmh-forms` — Form handlers

### Directory structure

```
ollmh-forms/
├── ollmh-forms.php
├── includes/
│   ├── class-ollmh-rest-routes.php     # register_rest_route() for all form endpoints
│   ├── class-ollmh-contact-form.php    # Contact form handler
│   ├── class-ollmh-appointment-form.php # Appointment booking handler
│   ├── class-ollmh-application-form.php # Nursing school application handler (multi-step)
│   ├── class-ollmh-event-registration.php # Event registration handler
│   ├── class-ollmh-validation.php      # Shared validation utilities
│   └── class-ollmh-turnstile.php       # Cloudflare Turnstile verification
├── assets/
│   ├── css/forms.css
│   └── js/forms.js                     # AJAX submission, multi-step navigation, validation
└── templates/
    ├── contact-form.php                # Contact form HTML
    ├── appointment-form.php            # Appointment booking form HTML
    ├── application-form-step-1.php     # Application: personal info
    ├── application-form-step-2.php     # Application: academic info
    ├── application-form-step-3.php     # Application: documents upload
    ├── application-form-step-4.php     # Application: review & submit
    └── event-registration-form.php     # Event registration form HTML
```

### REST API endpoints

See [`REST-API-SPEC.md`](./REST-API-SPEC.md) for the full API specification.

| Endpoint | Method | Purpose |
|---|---|---|
| `/ollmh/v1/contact` | POST | Submit contact form |
| `/ollmh/v1/appointments` | POST | Book an OPD/clinic appointment |
| `/ollmh/v1/applications` | POST | Submit nursing school application (multi-step) |
| `/ollmh/v1/applications/upload` | POST | Upload application document |
| `/ollmh/v1/events/register` | POST | Register for an event |
| `/ollmh/v1/turnstile/verify` | POST | Verify Turnstile token (server-side) |

### Turnstile integration

All public-facing forms are protected by Cloudflare Turnstile (see
[`SETTINGS.md`](./SETTINGS.md) → `security` group). The flow:

1. Front-end renders Turnstile widget (site key from `wp_settings`)
2. User completes challenge → token generated
3. Form submits via AJAX with token
4. Server verifies token via Turnstile API (`siteverify` endpoint)
5. If verification fails → return 400 with error message
6. If verification passes → process form data

---

## 4. `ollmh-payments` — M-Pesa integration (OPTIONAL)

> **Status:** Optional — pending client approval.
> See [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md) →
> ADR-004 for the full decision record, cPanel feasibility analysis,
> and implementation conditions.

### Overview

The `ollmh-payments` plugin is a **modular, optional** plugin that
integrates the M-Pesa Daraja (G2) API to facilitate STK Push (Lipa Na
M-Pesa Online) payments for nursing school application fees. It is
**not part of the core WordPress functionality** — the site operates
fully without it. When activated, it adds online payment capability to
the application form.

**Technical feasibility on cPanel shared hosting has been confirmed.**
The Daraja G2 API operates over standard HTTPS REST calls and requires
only PHP with cURL — no DNS changes, server migration, or special
infrastructure. Development will proceed once the client design is
finalized and approval is granted.

### Directory structure

```
ollmh-payments/
├── ollmh-payments.php
├── includes/
│   ├── class-ollmh-mpesa.php           # Daraja G2 API client (STK Push, transaction query)
│   ├── class-ollmh-payment-handler.php  # Payment processing logic
│   ├── class-ollmh-payment-callback.php # Callback URL handler (Daraja webhook)
│   ├── class-ollmh-mpesa-auth.php       # OAuth token management (caches access token)
│   └── class-ollmh-payment-query.php    # Query transaction status (cron fallback)
├── assets/
│   ├── css/payment.css                 # Payment UI styling (pure CSS, no framework)
│   └── js/payment.js                   # STK Push status polling (vanilla JS, no jQuery)
└── logs/
    └── .gitkeep                         # M-Pesa transaction logs (gitignored)
```

### Payment flow (STK Push — Lipa Na M-Pesa Online)

1. User submits application form → application saved with status `submitted`
2. System triggers STK Push to user's phone (M-Pesa prompt)
3. User enters M-Pesa PIN → payment confirmed or cancelled
4. Daraja G2 API sends callback to `/ollmh/v1/payments/callback`
5. Callback handler updates `wp_application_payments` with transaction status
6. If successful → application status updated to `screening`, notification sent
7. If failed → application remains `submitted`, user can retry payment

**Fallback:** If the Daraja callback is not received within 5 minutes,
a WP-Cron job polls the Daraja `QueryTransactionStatus` API to check
the transaction status — ensuring payment confirmation is not lost
even if the callback fails (a known issue on shared hosting under load).

See [`SETTINGS.md`](./SETTINGS.md) → `financial` group for all M-Pesa
configuration keys (conditional: only used when this plugin is active).

---

## 5. `ollmh-notifications` — Email & SMS

### Directory structure

```
ollmh-notifications/
├── ollmh-notifications.php
├── includes/
│   ├── class-ollmh-mailer.php           # SMTP email sending (phpmailer override)
│   ├── class-ollmh-sms.php              # SMS gateway client (Africa's Talking, Twilio)
│   ├── class-ollmh-notification-queue.php # Queue management (wp_cron batch processing)
│   └── class-ollmh-notification-logger.php # Log all sent notifications
├── templates/
│   ├── email/
│   │   ├── base.php                     # HTML email wrapper (header + footer)
│   │   ├── appointment-confirmation.php
│   │   ├── appointment-reminder.php
│   │   ├── application-received.php
│   │   ├── application-status-update.php
│   │   ├── contact-auto-reply.php
│   │   ├── password-reset.php
│   │   └── event-registration-confirmation.php
│   └── sms/
│       ├── appointment-reminder.txt
│       ├── application-status-update.txt
│       └── event-reminder.txt
└── logs/
    └── .gitkeep
```

See [`EMAIL-TEMPLATES.md`](./EMAIL-TEMPLATES.md) for the full template
specifications and [`SETTINGS.md`](./SETTINGS.md) → `notifications` and
`email` groups for configuration.

---

## 6. Plugin dependency order

```
ollmh-core (required, must be active first)
    ├── ollmh-forms (depends on core for CPTs, settings, Turnstile config)
    ├── ollmh-payments (depends on core for settings, forms for payment trigger)
    └── ollmh-notifications (depends on core for settings, forms for trigger events)
```

`ollmh-core` checks on activation that it is the first OLLMH plugin
activated. The other plugins check on activation that `ollmh-core` is
active — if not, they display an admin notice and refuse to activate.

---

## 7. Plugin header format

Each plugin's main PHP file uses the standard WordPress plugin header:

```php
<?php
/**
 * Plugin Name: OLLMH Core
 * Plugin URI: https://ourladyoflourdesmweahospital.org
 * Description: Core functionality for Our Lady of Lourdes Mwea Hospital — CPT registration, settings, capabilities, cron jobs, database tables.
 * Version: 1.0.0
 * Author: OLLMH IT
 * License: GPL-2.0-or-later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: ollmh-core
 * Domain Path: /languages
 * Requires at least: 6.2
 * Requires PHP: 8.0
 */

if (!defined('ABSPATH')) {
    exit;
}

define('OLLMH_CORE_VERSION', '1.0.0');
define('OLLMH_CORE_PATH', plugin_dir_path(__FILE__));
define('OLLMH_CORE_URL', plugin_dir_url(__FILE__));

// Load includes
require_once OLLMH_CORE_PATH . 'includes/class-ollmh-activator.php';
require_once OLLMH_CORE_PATH . 'includes/class-ollmh-cpt.php';
require_once OLLMH_CORE_PATH . 'includes/class-ollmh-settings.php';
require_once OLLMH_CORE_PATH . 'includes/class-ollmh-capabilities.php';
require_once OLLMH_CORE_PATH . 'includes/class-ollmh-cron.php';
// ... etc.

register_activation_hook(__FILE__, ['OLLMH_Activator', 'activate']);
register_deactivation_hook(__FILE__, ['OLLMH_Deactivator', 'deactivate']);

OLLMH_CPT::init();
OLLMH_Settings::init();
OLLMH_Capabilities::init();
OLLMH_Cron::init();
```

---

## 8. PHP version requirement

All OLLMH plugins require **PHP 8.0+** (uses typed properties, named
arguments, match expressions, nullsafe operator). WordPress 6.2+ minimum.
