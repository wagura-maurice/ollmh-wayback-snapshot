# Settings Catalogue — `wp_settings`

> This document is the complete reference for every setting stored in the
> `wp_settings` table. The table is a central key-value store for all
> platform configuration — hospital identity, contact details, clinical
> operations, nursing school, applications, SEO, email/SMTP, M-Pesa,
> security, and reference data (dropdowns for patient registration, staff
> records, and applications).
>
> The table schema is defined in
> [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md). The PHP seeder that
> populates these defaults is at
> [`seeders/class-ollmh-settings-seeder.php`](../seeders/class-ollmh-settings-seeder.php).
>
> **Design principle:** The seeder uses insert-only upsert — it sets
> `current_value = default_value` on first insert and never overwrites a
> `current_value` that an admin has already customised.

---

## Table structure

```sql
CREATE TABLE wp_settings (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  item          VARCHAR(191)    NOT NULL,         -- unique setting key
  default_value LONGTEXT        NULL,             -- factory default
  current_value LONGTEXT        NULL,             -- live value (admin-set)
  description   TEXT            NULL,             -- human-readable explanation
  type          ENUM('string','text','json','boolean','integer','decimal',
                     'url','email','secret','date','datetime','file')
                  NOT NULL DEFAULT 'string',
  group_name    VARCHAR(100)    NOT NULL DEFAULT 'general',
  is_public     TINYINT(1)      NOT NULL DEFAULT 0,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_settings_item (item),
  KEY idx_settings_group (group_name),
  KEY idx_settings_public (is_public)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

| Column | Purpose |
|---|---|
| `item` | Unique setting key (e.g. `hospital_name`, `mpesa_shortcode`). |
| `default_value` | Factory default set by the seeder. Never overwritten by the admin UI. |
| `current_value` | The live value. Set by the admin. If never customised, equals `default_value`. |
| `description` | Human-readable explanation of what the setting controls. |
| `type` | Data type hint for the admin UI rendering. `secret` values are encrypted and never exposed to the front-end. |
| `group_name` | Feature-area grouping for the admin settings page tabs. |
| `is_public` | 1 = safe to expose to the front-end API. 0 = admin-only (SMTP passwords, M-Pesa keys, etc.). |

---

## Settings groups

The seeder populates **16 groups** containing **~100 settings**:

| # | Group | Settings count | Description |
|---|---|---|---|
| 1 | `general` | 10 | Hospital identity, timezone, locale, currency, maintenance mode |
| 2 | `homepage` | 5 | Hero section titles, subtitles, features section |
| 3 | `contact` | 13 | Phone, emergency, ambulance, WhatsApp, address, GPS, emails |
| 4 | `social` | 4 | Facebook, YouTube, X/Twitter, Instagram URLs |
| 5 | `clinical` | 14 | OPD hours, visiting hours, fees, NHIF, insurance, bed capacity |
| 6 | `appointments` | 6 | Booking settings, advance days, slot duration, reminders |
| 7 | `nursing_school` | 7 | School name, application open, fees, intakes, programmes, qualifications |
| 8 | `applications` | 11 | Application form settings, fees, deadlines, document requirements, status flow |
| 9 | `auth` | 9 | 2FA, session, login attempts, password policy, public registration |
| 10 | `security` | 5 | Cloudflare Turnstile keys, captcha toggles per form |
| 11 | `email` | 7 | SMTP host, port, encryption, credentials, from address/name |
| 12 | `notifications` | 7 | Email/SMS toggles, gateway provider, API key, sender ID, reminder toggles |
| 13 | `seo` | 8 | Meta title/description templates, OG image, Twitter handle, GA4, sitemap, robots |
| 14 | `financial` | 11 | M-Pesa environment, credentials, shortcode, passkey, callback URL, invoice/receipt prefixes, payment methods |
| 15 | `community` | 5 | SMI community name/description, outreach toggle, volunteer/vocation enquiry toggles |
| 16 | `profiles` | 10 | Reference data: salutations, genders, languages, marital statuses, education levels, employment statuses, blood types, nationalities, counties, relationships, security questions |
| 17 | `cache` | 3 | Cache enabled, default TTL, clinic schedule TTL |
| 18 | `analytics` | 3 | Analytics enabled, retention, audit log |
| 19 | `jobs` | 4 | Job queue enabled, batch size, max attempts, retention |

---

## Group: `general` — Hospital identity

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `hospital_name` | string | ✅ | `Our Lady of Lourdes Mwea Hospital` | Full display name shown in UI, emails, footer, SEO schema |
| `hospital_short_name` | string | ✅ | `OLLMH` | Abbreviation for breadcrumbs, compact UI, social handles |
| `hospital_tagline` | string | ✅ | `Faith-Based Healthcare Serving Mwea, Kirinyaga County` | Tagline in header, metadata, hero fallback |
| `hospital_description` | text | ✅ | (full description) | Used in footer, SEO meta, homepage hero fallback |
| `hospital_url` | url | ✅ | `null` | Canonical public URL |
| `timezone` | string | ❌ | `Africa/Nairobi` | IANA timezone for all date/time display |
| `default_locale` | string | ❌ | `en_KE` | Locale for i18n formatting |
| `default_currency` | string | ❌ | `KES` | ISO 4217 currency code |
| `maintenance_mode` | boolean | ❌ | `0` | When 1, shows maintenance page to non-admin users |
| `maintenance_message` | text | ✅ | (maintenance message) | Message shown when maintenance_mode is active |

## Group: `homepage` — Hero & features

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `hero_title` | string | ✅ | `Our Lady of Lourdes Mwea Hospital` | Homepage H1 |
| `hero_subtitle` | text | ✅ | (subtitle) | Homepage hero paragraph |
| `features_title` | string | ✅ | `Our Services` | Services section title |
| `features_subtitle` | string | ✅ | (subtitle) | Services section subtitle |
| `news_promo_title` | string | ✅ | `Latest News & Announcements` | News promo section title |

## Group: `contact` — Phone, address, emails

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `hospital_phone` | string | ✅ | `null` | Primary phone (footer, contact page, schema) |
| `hospital_emergency_phone` | string | ✅ | `null` | 24-hour emergency phone |
| `hospital_ambulance_phone` | string | ✅ | `null` | Ambulance dispatch phone |
| `hospital_whatsapp` | string | ✅ | `null` | WhatsApp number (E.164 without +) |
| `hospital_address` | string | ✅ | `Mwea, Kirinyaga County, Kenya` | Physical address |
| `hospital_county` | string | ✅ | `Kirinyaga County` | County (local SEO schema) |
| `hospital_country` | string | ✅ | `Kenya` | Country |
| `hospital_latitude` | string | ✅ | `null` | GPS latitude (Maps embed, schema geo) |
| `hospital_longitude` | string | ✅ | `null` | GPS longitude (Maps embed, schema geo) |
| `hospital_office_hours` | string | ✅ | `24 Hours, 7 Days a Week` | General operating hours |
| `hospital_email` | email | ✅ | `null` | General info email |
| `admin_email` | email | ❌ | `null` | Internal admin email for alerts |
| `nursing_school_email` | email | ✅ | `null` | Nursing school admissions email |
| `hr_email` | email | ✅ | `null` | HR department email |
| `community_email` | email | ✅ | `null` | Community/SMI enquiries email |

## Group: `social` — Social media links

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `social_facebook` | url | ✅ | `null` | Facebook page URL |
| `social_youtube` | url | ✅ | `null` | YouTube channel URL |
| `social_twitter` | url | ✅ | `null` | X (Twitter) profile URL |
| `social_instagram` | url | ✅ | `null` | Instagram profile URL |

## Group: `clinical` — Operations & fees

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `opd_operating_hours` | string | ✅ | `Mon–Fri 8AM–5PM, Sat 8AM–1PM, Sun Closed` | OPD hours |
| `visiting_hours_general` | string | ✅ | `10AM–12PM, 4PM–6PM` | General ward visiting hours |
| `visiting_hours_icu` | string | ✅ | `11AM–12PM, 4PM–5PM` | ICU visiting hours |
| `visiting_hours_maternity` | string | ✅ | `10AM–1PM, 4PM–7PM` | Maternity visiting hours |
| `emergency_services_24h` | boolean | ✅ | `1` | Emergency Dept operates 24h |
| `ambulance_service_available` | boolean | ✅ | `1` | Ambulance services available |
| `lab_operating_hours` | string | ✅ | `Mon–Sat 7AM–8PM, Sun 8AM–2PM` | Lab hours |
| `pharmacy_hours` | string | ✅ | `Mon–Sat 8AM–8PM, Sun 8AM–2PM` | Pharmacy hours |
| `registration_fee_kes` | integer | ✅ | `200` | New OPD patient registration fee (KES) |
| `consultation_fee_general_kes` | integer | ✅ | `500` | General consultation fee (KES) |
| `consultation_fee_specialist_kes` | integer | ✅ | `1500` | Specialist consultation fee (KES) |
| `nhif_accredited` | boolean | ✅ | `1` | NHIF accredited |
| `nhif_code` | string | ✅ | `null` | NHIF facility code |
| `accepted_insurance_providers` | json | ✅ | (9 providers) | JSON object of insurance provider keys to labels |
| `bed_capacity_total` | integer | ✅ | `null` | Total licensed bed capacity |

## Group: `appointments` — Online booking

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `appointment_booking_enabled` | boolean | ✅ | `1` | Master switch for online booking |
| `appointment_advance_days` | integer | ✅ | `14` | Max days in advance to book |
| `appointment_slot_duration_minutes` | integer | ❌ | `30` | Slot duration in minutes |
| `appointment_min_lead_hours` | integer | ✅ | `2` | Min lead time before booking |
| `appointment_cancellation_hours` | integer | ✅ | `4` | Min hours to cancel without penalty |
| `appointment_reminder_hours` | integer | ❌ | `24` | Hours before appointment to send reminder |

## Group: `nursing_school` — School & admissions

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `nursing_school_name` | string | ✅ | `Our Lady of Lourdes Mwea Hospital Nursing School` | School display name |
| `nursing_school_description` | text | ✅ | (description) | School description for page and SEO |
| `nursing_application_open` | boolean | ✅ | `1` | Applications being accepted |
| `nursing_application_fee_kes` | integer | ✅ | `1000` | Application fee (KES) |
| `nursing_intake_months` | json | ✅ | `{"september":"September Intake","january":"January Intake"}` | Intake months |
| `nursing_programmes_offered` | json | ✅ | (4 programmes) | JSON of programme keys to labels |
| `nursing_min_qualification` | string | ✅ | `KCSE Mean Grade C...` | Minimum academic qualification |

## Group: `applications` — Application pipeline

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `application_open` | boolean | ✅ | `1` | Master switch for form acceptance |
| `application_fee_kes` | integer | ✅ | `1000` | Application fee (KES) via M-Pesa |
| `application_deadline` | date | ✅ | `null` | Deadline (YYYY-MM-DD), null = rolling |
| `application_requires_photo` | boolean | ✅ | `1` | Passport photo required |
| `application_requires_transcripts` | boolean | ✅ | `1` | Academic transcripts required |
| `application_requires_id_copy` | boolean | ✅ | `1` | National ID/birth certificate required |
| `application_requires_referees` | boolean | ✅ | `1` | Referees required |
| `application_min_referees` | integer | ✅ | `2` | Minimum referee count |
| `application_review_enabled` | boolean | ❌ | `1` | Review workflow active |
| `application_notification_enabled` | boolean | ❌ | `1` | Email/SMS notifications on status change |
| `application_status_flow` | json | ✅ | (9 statuses) | JSON of status keys to labels |

## Group: `auth` — Authentication & passwords

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `two_factor_auth_enabled` | boolean | ❌ | `0` | Require 2FA for admin/editor |
| `session_lifetime_minutes` | integer | ❌ | `120` | Session expiry in minutes |
| `max_login_attempts` | integer | ❌ | `5` | Max failed logins before lockout |
| `lockout_duration_minutes` | integer | ❌ | `15` | Lockout duration in minutes |
| `password_min_length` | integer | ❌ | `8` | Min password length |
| `password_require_uppercase` | boolean | ❌ | `1` | Require uppercase letter |
| `password_require_number` | boolean | ❌ | `1` | Require numeric digit |
| `public_registration_open` | boolean | ✅ | `1` | Public self-registration enabled |
| `default_user_role` | string | ❌ | `subscriber` | Default role for new registrations |

## Group: `security` — Cloudflare Turnstile

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `turnstile_site_key` | string | ✅ | `null` | Turnstile site key (public) |
| `turnstile_secret_key` | secret | ❌ | `null` | Turnstile secret key (private, encrypted) |
| `captcha_on_contact_form` | boolean | ❌ | `1` | Captcha on contact form |
| `captcha_on_appointment_booking` | boolean | ❌ | `1` | Captcha on appointment booking |
| `captcha_on_application_form` | boolean | ❌ | `1` | Captcha on application form |

## Group: `email` — SMTP

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `smtp_host` | string | ❌ | `null` | SMTP hostname |
| `smtp_port` | integer | ❌ | `587` | SMTP port (587=STARTTLS, 465=SSL) |
| `smtp_encryption` | string | ❌ | `tls` | Encryption: tls, ssl, or blank |
| `smtp_username` | string | ❌ | `null` | SMTP username |
| `smtp_password` | secret | ❌ | `null` | SMTP password (encrypted) |
| `smtp_from_email` | email | ❌ | `null` | From address for outbound emails |
| `smtp_from_name` | string | ❌ | `Our Lady of Lourdes Mwea Hospital` | From display name |

## Group: `notifications` — Email & SMS

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `email_notifications_enabled` | boolean | ❌ | `1` | Master switch for transactional emails |
| `sms_notifications_enabled` | boolean | ❌ | `0` | Master switch for SMS |
| `sms_gateway_provider` | string | ❌ | `africastalking` | Gateway: africastalking, twilio, nexmo, safaricom_sdp |
| `sms_gateway_api_key` | secret | ❌ | `null` | SMS gateway API key (encrypted) |
| `sms_sender_id` | string | ❌ | `OLLMH` | Alphanumeric sender ID (max 11 chars) |
| `appointment_reminder_sms_enabled` | boolean | ❌ | `0` | SMS reminders for appointments |
| `application_status_sms_enabled` | boolean | ❌ | `0` | SMS notifications for application status changes |

## Group: `seo` — Search engine optimization

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `seo_default_meta_title_template` | string | ❌ | `%%title%% %%sep%% %%sitename%%` | Meta title template |
| `seo_default_meta_description_template` | string | ❌ | `%%excerpt%%` | Meta description template |
| `seo_default_og_image_id` | integer | ❌ | `null` | Default OG image media asset ID (1200×630px) |
| `seo_twitter_handle` | string | ✅ | `null` | Twitter/X handle (without @) |
| `seo_google_analytics_id` | string | ❌ | `null` | GA4 measurement ID (G-XXXXXXXXXX) |
| `seo_sitemap_enabled` | boolean | ❌ | `1` | XML sitemap generation enabled |
| `seo_robots_default` | string | ❌ | `index,follow` | Default robots meta directive |
| `seo_breadcrumbs_enabled` | boolean | ❌ | `1` | Breadcrumb generation enabled |

## Group: `financial` — M-Pesa & payments

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `mpesa_environment` | string | ❌ | `sandbox` | Daraja API: sandbox or production |
| `mpesa_consumer_key` | secret | ❌ | `null` | Daraja consumer key (encrypted) |
| `mpesa_consumer_secret` | secret | ❌ | `null` | Daraja consumer secret (encrypted) |
| `mpesa_shortcode` | string | ❌ | `null` | Paybill/till number |
| `mpesa_passkey` | secret | ❌ | `null` | STK Push passkey (encrypted) |
| `mpesa_initiator_username` | string | ❌ | `null` | Initiator username |
| `mpesa_initiator_password` | secret | ❌ | `null` | Initiator password (encrypted) |
| `mpesa_callback_url` | url | ❌ | `null` | STK Push callback URL |
| `invoice_prefix` | string | ❌ | `OLLMH-` | Invoice reference prefix |
| `receipt_prefix` | string | ❌ | `RCP-` | Receipt reference prefix |
| `payment_methods` | json | ✅ | (4 methods) | JSON of payment method keys to labels |

## Group: `community` — SMI & outreach

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `smi_community_name` | string | ✅ | `Sisters of Mary Immaculate (SMI) Community` | SMI section display name |
| `smi_description` | text | ✅ | (description) | SMI description for page and SEO |
| `community_outreach_enabled` | boolean | ✅ | `1` | Community outreach section active |
| `volunteer_registration_open` | boolean | ✅ | `1` | Volunteer registration open |
| `vocation_enquiries_open` | boolean | ✅ | `1` | Vocation enquiries accepted |

## Group: `profiles` — Reference data (dropdowns)

These JSON objects populate dropdowns in patient registration, staff
records, and application forms. Each key is the stored value; the value is
the display label.

| Item | Type | Public | Entries | Description |
|---|---|---|---|---|
| `profile_salutations` | json | ✅ | 18 | Salutation dropdown (Mr, Mrs, Dr, Sr, Fr, etc.) |
| `profile_genders` | json | ✅ | 4 | Gender dropdown |
| `profile_languages` | json | ✅ | 19 | Languages spoken (Swahili, English, Kikuyu, etc.) |
| `profile_marital_statuses` | json | ✅ | 8 | Marital status dropdown |
| `profile_education_levels` | json | ✅ | 16 | Education level (aligned with Kenyan education system) |
| `profile_employment_statuses` | json | ✅ | 14 | Employment status |
| `profile_blood_types` | json | ✅ | 9 | ABO/Rh blood types |
| `profile_nationalities` | json | ✅ | 18 | Nationalities (focus on East African + international) |
| `profile_counties` | json | ✅ | 47 | All 47 Kenyan counties |
| `profile_relationships` | json | ✅ | 12 | Next-of-kin relationship types |
| `profile_security_questions` | json | ✅ | 8 | Security questions for password recovery |

## Group: `cache` — Application caching

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `cache_enabled` | boolean | ❌ | `1` | Application cache active |
| `cache_default_ttl_seconds` | integer | ❌ | `3600` | Default cache TTL (1 hour) |
| `cache_clinic_schedule_ttl_seconds` | integer | ❌ | `86400` | Clinic schedule cache TTL (24 hours) |

## Group: `analytics` — Tracking & audit

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `analytics_enabled` | boolean | ❌ | `1` | Analytics tracking active |
| `analytics_retention_days` | integer | ❌ | `365` | Raw analytics retention period |
| `audit_log_enabled` | boolean | ❌ | `1` | Audit trail active for compliance logging |

## Group: `jobs` — Background queue

| Item | Type | Public | Default | Description |
|---|---|---|---|---|
| `job_queue_enabled` | boolean | ❌ | `1` | Background job processor active |
| `job_queue_batch_size` | integer | ❌ | `20` | Jobs per cron cycle |
| `job_max_attempts` | integer | ❌ | `3` | Max retries before dead-letter |
| `job_retention_days` | integer | ❌ | `30` | Days to retain job records |

---

## Admin settings page

The Settings top-level menu in the WordPress admin sidebar (see
[`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md)) renders each `group_name` as a
tab. Within each tab, settings are rendered based on their `type`:

| `type` value | Admin UI rendering |
|---|---|
| `string` | Single-line text input |
| `text` | Textarea (multi-line) |
| `json` | JSON editor (syntax-highlighted textarea or visual editor) |
| `boolean` | Toggle switch (0/1) |
| `integer` | Number input (step=1) |
| `decimal` | Number input (step=0.01) |
| `url` | URL input with validation |
| `email` | Email input with validation |
| `secret` | Password field (value masked, stored encrypted) |
| `date` | Date picker (YYYY-MM-DD) |
| `datetime` | Datetime picker (YYYY-MM-DD HH:MM:SS) |
| `file` | File upload (stores media asset ID) |

**Capability:** `manage_options` (Administrator only). The SEO sub-tab
additionally requires `manage_seo` (granted to Editor via `add_cap()`; see
[`USER-ROLES.md`](./USER-ROLES.md)).

---

## Front-end settings API

The front-end can read public settings via a REST API endpoint or a
WordPress AJAX handler. The endpoint returns only rows where
`is_public = 1` and excludes any `type = 'secret'` values entirely:

```
GET /wp-json/ollmh/v1/settings
→ Returns: { hospital_name, hospital_short_name, hospital_tagline, ... }
→ Does NOT return: smtp_password, mpesa_consumer_key, turnstile_secret_key, etc.
```

This allows the front-end to render hospital name, contact info, social
links, operating hours, fees, and reference data without exposing
credentials.

---

## Relationship to existing tables

`wp_settings` is a **general-purpose configuration store** that
complements (not replaces) the existing domain-specific tables:

| Existing table | What `wp_settings` adds |
|---|---|
| `wp_location_info` | `wp_settings` stores the hospital name, tagline, URL, timezone, and other identity fields that are not in `wp_location_info`. The two tables can be merged in a future refactor, or `wp_location_info` can remain the structured address/geo table while `wp_settings` holds the broader identity config. |
| `wp_contact_channels` | `wp_settings` stores social media URLs and department emails as key-value pairs. `wp_contact_channels` stores them as structured rows (type, label, value, icon). Both can coexist — `wp_settings` is for quick config, `wp_contact_channels` is for the sortable admin list UI. |
| `wp_about_facts` | `wp_settings` does not store about facts — those remain in `wp_about_facts` as structured rows. |

**Recommendation:** Use `wp_settings` for scalar configuration values
(strings, booleans, integers, JSON blobs) and keep the existing structured
tables for multi-row content (contact channels, about facts, milestones,
etc.). The admin settings page reads from `wp_settings`; the admin
management screens read from the structured tables.
