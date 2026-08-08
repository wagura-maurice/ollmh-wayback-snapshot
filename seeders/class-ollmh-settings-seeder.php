<?php
if (!defined('ABSPATH')) {
    exit;
}

require_once __DIR__ . '/class-seeder-base.php';

/**
 * Settings Seeder — Our Lady of Lourdes Mwea Hospital (OLLMH)
 *
 * Populates wp_settings with the hospital's default configuration.
 * Groups map to the OLLMH feature areas defined in docs/SETTINGS.md.
 *
 * Only inserts when a key does not yet exist; never overwrites a live
 * current_value that an admin has already customised.
 *
 * IMPORTANT: This seeder is intentionally EXCLUDED from default bulk
 * execution because it is static reference data and must only run once
 * at activation (or on explicit admin request).
 *
 * To run manually:
 *   $seeder = new OLLMH_Settings_Seeder();
 *   $seeder->run();
 *
 * @package OLLMH\Seeders
 */
class OLLMH_Settings_Seeder extends OLLMH_Seeder_Base {

    protected function get_table_name(): string {
        return 'settings';
    }

    protected function fetch_from_source(): array {
        return ['success' => true, 'data' => []];
    }

    /**
     * All hospital settings, grouped by feature area.
     *
     * @return array<int, array{item: string, default_value: ?string, type: string, group_name: string, is_public: int, description: string}>
     */
    private function get_settings(): array {
        return [

            // ── General ──────────────────────────────────────────────────────
            [
                'item'          => 'hospital_name',
                'default_value' => 'Our Lady of Lourdes Mwea Hospital',
                'type'          => 'string',
                'group_name'    => 'general',
                'is_public'     => 1,
                'description'   => 'Full display name of the hospital shown in UI, emails, footer, and SEO schema.',
            ],
            [
                'item'          => 'hospital_short_name',
                'default_value' => 'OLLMH',
                'type'          => 'string',
                'group_name'    => 'general',
                'is_public'     => 1,
                'description'   => 'Short name/abbreviation used in breadcrumbs, compact UI elements, and social handles.',
            ],
            [
                'item'          => 'hospital_tagline',
                'default_value' => 'Faith-Based Healthcare Serving Mwea, Kirinyaga County',
                'type'          => 'string',
                'group_name'    => 'general',
                'is_public'     => 1,
                'description'   => 'Short tagline displayed in the site header, metadata, and hero subtitle fallback.',
            ],
            [
                'item'          => 'hospital_description',
                'default_value' => 'Our Lady of Lourdes Mwea Hospital is a Catholic faith-based healthcare facility operated by the Sisters of Mary Immaculate (SMI), serving the community of Mwea, Kirinyaga County, Kenya. The hospital offers outpatient services, inpatient wards, maternity care, paediatrics, surgery, a nursing school, and community health outreach programs.',
                'type'          => 'text',
                'group_name'    => 'general',
                'is_public'     => 1,
                'description'   => 'Hospital description used in footer about text, SEO meta description, and homepage hero subtitle fallback.',
            ],
            [
                'item'          => 'hospital_url',
                'default_value' => null,
                'type'          => 'url',
                'group_name'    => 'general',
                'is_public'     => 1,
                'description'   => 'Canonical public URL of the hospital website (e.g. https://ourladyoflourdesmweahospital.org).',
            ],
            [
                'item'          => 'timezone',
                'default_value' => 'Africa/Nairobi',
                'type'          => 'string',
                'group_name'    => 'general',
                'is_public'     => 0,
                'description'   => 'Default timezone for all date/time display and scheduling (IANA timezone identifier).',
            ],
            [
                'item'          => 'default_locale',
                'default_value' => 'en_KE',
                'type'          => 'string',
                'group_name'    => 'general',
                'is_public'     => 0,
                'description'   => 'Default locale code for i18n formatting (dates, numbers, currency).',
            ],
            [
                'item'          => 'default_currency',
                'default_value' => 'KES',
                'type'          => 'string',
                'group_name'    => 'general',
                'is_public'     => 0,
                'description'   => 'ISO 4217 currency code used across financial tables and display.',
            ],
            [
                'item'          => 'maintenance_mode',
                'default_value' => '0',
                'type'          => 'boolean',
                'group_name'    => 'general',
                'is_public'     => 0,
                'description'   => 'When 1, the website shows a maintenance page to non-admin users.',
            ],
            [
                'item'          => 'maintenance_message',
                'default_value' => 'We are currently performing scheduled maintenance on the OLLMH website. Please check back shortly. For emergencies, call our 24-hour line.',
                'type'          => 'text',
                'group_name'    => 'general',
                'is_public'     => 1,
                'description'   => 'Message displayed to visitors when maintenance_mode is active.',
            ],

            // ── Homepage ─────────────────────────────────────────────────────
            [
                'item'          => 'hero_title',
                'default_value' => 'Our Lady of Lourdes Mwea Hospital',
                'type'          => 'string',
                'group_name'    => 'homepage',
                'is_public'     => 1,
                'description'   => 'Hero section H1 title on the homepage.',
            ],
            [
                'item'          => 'hero_subtitle',
                'default_value' => 'A Catholic faith-based hospital serving Mwea, Kirinyaga County with compassionate, quality healthcare for all.',
                'type'          => 'text',
                'group_name'    => 'homepage',
                'is_public'     => 1,
                'description'   => 'Hero section subtitle paragraph on the homepage.',
            ],
            [
                'item'          => 'features_title',
                'default_value' => 'Our Services',
                'type'          => 'string',
                'group_name'    => 'homepage',
                'is_public'     => 1,
                'description'   => 'Title for the services/features section on the homepage.',
            ],
            [
                'item'          => 'features_subtitle',
                'default_value' => 'Comprehensive healthcare services for the Mwea community',
                'type'          => 'string',
                'group_name'    => 'homepage',
                'is_public'     => 1,
                'description'   => 'Subtitle for the services/features section on the homepage.',
            ],
            [
                'item'          => 'news_promo_title',
                'default_value' => 'Latest News & Announcements',
                'type'          => 'string',
                'group_name'    => 'homepage',
                'is_public'     => 1,
                'description'   => 'Title for the news promo section on the homepage.',
            ],

            // ── Contact ──────────────────────────────────────────────────────
            [
                'item'          => 'hospital_phone',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   => 'Primary hospital phone number displayed across the site (footer, contact page, schema markup).',
            ],
            [
                'item'          => 'hospital_emergency_phone',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   => '24-hour emergency phone number for the Emergency Department.',
            ],
            [
                'item'          => 'hospital_ambulance_phone',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   => 'Ambulance dispatch phone number.',
            ],
            [
                'item'          => 'hospital_whatsapp',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   => 'WhatsApp contact number in E.164 format without + (used for wa.me links).',
            ],
            [
                'item'          => 'hospital_address',
                'default_value' => 'Mwea, Kirinyaga County, Kenya',
                'type'          => 'string',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   => 'Physical address shown on contact page, footer, and Hospital schema markup.',
            ],
            [
                'item'          => 'hospital_county',
                'default_value' => 'Kirinyaga County',
                'type'          => 'string',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   => 'County where the hospital is located (used in local SEO schema).',
            ],
            [
                'item'          => 'hospital_country',
                'default_value' => 'Kenya',
                'type'          => 'string',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   => 'Country where the hospital is located.',
            ],
            [
                'item'          => 'hospital_latitude',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   => 'GPS latitude coordinate for Google Maps embed and Hospital schema geo property.',
            ],
            [
                'item'          => 'hospital_longitude',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   => 'GPS longitude coordinate for Google Maps embed and Hospital schema geo property.',
            ],
            [
                'item'          => 'hospital_office_hours',
                'default_value' => '24 Hours, 7 Days a Week',
                'type'          => 'string',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   => 'General operating hours string displayed on contact page and footer.',
            ],
            [
                'item'          => 'hospital_email',
                'default_value' => null,
                'type'          => 'email',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   'General information email displayed on contact page and footer.',
            ],
            [
                'item'          => 'admin_email',
                'default_value' => null,
                'type'          => 'email',
                'group_name'    => 'contact',
                'is_public'     => 0,
                'description'   => 'Internal admin email for system alerts, contact form submissions, and error notifications.',
            ],
            [
                'item'          => 'nursing_school_email',
                'default_value' => null,
                'type'          => 'email',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   'Nursing school admissions enquiry email.',
            ],
            [
                'item'          => 'hr_email',
                'default_value' => null,
                'type'          => 'email',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   'HR department email for job applications and staff enquiries.',
            ],
            [
                'item'          => 'community_email',
                'default_value' => null,
                'type'          => 'email',
                'group_name'    => 'contact',
                'is_public'     => 1,
                'description'   'Community outreach and SMI enquiries email.',
            ],

            // ── Social Media ─────────────────────────────────────────────────
            [
                'item'          => 'social_facebook',
                'default_value' => null,
                'type'          => 'url',
                'group_name'    => 'social',
                'is_public'     => 1,
                'description'   => 'Facebook page URL for the hospital.',
            ],
            [
                'item'          => 'social_youtube',
                'default_value' => null,
                'type'          => 'url',
                'group_name'    => 'social',
                'is_public'     => 1,
                'description'   => 'YouTube channel URL for the hospital.',
            ],
            [
                'item'          => 'social_twitter',
                'default_value' => null,
                'type'          => 'url',
                'group_name'    => 'social',
                'is_public'     => 1,
                'description'   => 'X (Twitter) profile URL for the hospital.',
            ],
            [
                'item'          => 'social_instagram',
                'default_value' => null,
                'type'          => 'url',
                'group_name'    => 'social',
                'is_public'     => 1,
                'description'   => 'Instagram profile URL for the hospital.',
            ],

            // ── Clinical / Operations ────────────────────────────────────────
            [
                'item'          => 'opd_operating_hours',
                'default_value' => 'Monday – Friday: 8:00 AM – 5:00 PM, Saturday: 8:00 AM – 1:00 PM, Sunday: Closed',
                'type'          => 'string',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'Outpatient Department (OPD) operating hours displayed on the OPD page.',
            ],
            [
                'item'          => 'visiting_hours_general',
                'default_value' => '10:00 AM – 12:00 PM, 4:00 PM – 6:00 PM',
                'type'          => 'string',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'General ward visiting hours.',
            ],
            [
                'item'          => 'visiting_hours_icu',
                'default_value' => '11:00 AM – 12:00 PM, 4:00 PM – 5:00 PM',
                'type'          => 'string',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'ICU visiting hours (restricted).',
            ],
            [
                'item'          => 'visiting_hours_maternity',
                'default_value' => '10:00 AM – 1:00 PM, 4:00 PM – 7:00 PM',
                'type'          => 'string',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'Maternity ward visiting hours.',
            ],
            [
                'item'          => 'emergency_services_24h',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'Whether the Emergency Department operates 24 hours a day.',
            ],
            [
                'item'          => 'ambulance_service_available',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'Whether ambulance services are available.',
            ],
            [
                'item'          => 'lab_operating_hours',
                'default_value' => 'Monday – Saturday: 7:00 AM – 8:00 PM, Sunday: 8:00 AM – 2:00 PM',
                'type'          => 'string',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'Laboratory operating hours.',
            ],
            [
                'item'          => 'pharmacy_hours',
                'default_value' => 'Monday – Saturday: 8:00 AM – 8:00 PM, Sunday: 8:00 AM – 2:00 PM',
                'type'          => 'string',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'Pharmacy operating hours.',
            ],
            [
                'item'          => 'registration_fee_kes',
                'default_value' => '200',
                'type'          => 'integer',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'Patient registration fee in KES for new OPD patients.',
            ],
            [
                'item'          => 'consultation_fee_general_kes',
                'default_value' => '500',
                'type'          => 'integer',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'General consultation fee in KES.',
            ],
            [
                'item'          => 'consultation_fee_specialist_kes',
                'default_value' => '1500',
                'type'          => 'integer',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'Specialist consultation fee in KES.',
            ],
            [
                'item'          => 'nhif_accredited',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'Whether the hospital is NHIF (National Hospital Insurance Fund) accredited.',
            ],
            [
                'item'          => 'nhif_code',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'NHIF facility code.',
            ],
            [
                'item'          => 'accepted_insurance_providers',
                'default_value' => json_encode([
                    'nhif'      => 'NHIF (National Hospital Insurance Fund)',
                    'shif'      => 'SHIF (Social Health Insurance Fund)',
                    'aar'       => 'AAR Healthcare',
                    'uap'       => 'UAP Old Mutual',
                    'jubilee'   => 'Jubilee Health Insurance',
                    'minet'     => 'Minet (Public Service)',
                    'cipa'      => 'CIC Insurance',
                    'apa'       => 'APA Insurance',
                    'heritage'  => 'Heritage Insurance',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'JSON object of accepted insurance provider keys to display labels.',
            ],
            [
                'item'          => 'bed_capacity_total',
                'default_value' => null,
                'type'          => 'integer',
                'group_name'    => 'clinical',
                'is_public'     => 1,
                'description'   => 'Total licensed bed capacity of the hospital.',
            ],

            // ── Appointment Booking ──────────────────────────────────────────
            [
                'item'          => 'appointment_booking_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'appointments',
                'is_public'     => 1,
                'description'   => 'Master switch enabling online appointment booking for OPD and clinics.',
            ],
            [
                'item'          => 'appointment_advance_days',
                'default_value' => '14',
                'type'          => 'integer',
                'group_name'    => 'appointments',
                'is_public'     => 1,
                'description'   => 'Maximum number of days in advance an appointment can be booked.',
            ],
            [
                'item'          => 'appointment_slot_duration_minutes',
                'default_value' => '30',
                'type'          => 'integer',
                'group_name'    => 'appointments',
                'is_public'     => 0,
                'description'   => 'Duration in minutes of each appointment slot.',
            ],
            [
                'item'          => 'appointment_min_lead_hours',
                'default_value' => '2',
                'type'          => 'integer',
                'group_name'    => 'appointments',
                'is_public'     => 1,
                'description'   => 'Minimum lead time in hours before an appointment can be booked online.',
            ],
            [
                'item'          => 'appointment_cancellation_hours',
                'default_value' => '4',
                'type'          => 'integer',
                'group_name'    => 'appointments',
                'is_public'     => 1,
                'description'   => 'Minimum hours before an appointment that a patient can cancel without penalty.',
            ],
            [
                'item'          => 'appointment_reminder_hours',
                'default_value' => '24',
                'type'          => 'integer',
                'group_name'    => 'appointments',
                'is_public'     => 0,
                'description'   => 'Hours before an appointment to send a reminder notification (email/SMS).',
            ],

            // ── Nursing School ───────────────────────────────────────────────
            [
                'item'          => 'nursing_school_name',
                'default_value' => 'Our Lady of Lourdes Mwea Hospital Nursing School',
                'type'          => 'string',
                'group_name'    => 'nursing_school',
                'is_public'     => 1,
                'description'   => 'Display name of the nursing school.',
            ],
            [
                'item'          => 'nursing_school_description',
                'default_value' => 'The OLLMH Nursing School offers comprehensive nursing training programmes accredited by the Nursing Council of Kenya, preparing students for careers in healthcare with a strong foundation in compassionate, faith-based patient care.',
                'type'          => 'text',
                'group_name'    => 'nursing_school',
                'is_public'     => 1,
                'description'   => 'Nursing school description used on the school page and SEO meta.',
            ],
            [
                'item'          => 'nursing_application_open',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'nursing_school',
                'is_public'     => 1,
                'description'   => 'Whether nursing school applications are currently being accepted.',
            ],
            [
                'item'          => 'nursing_application_fee_kes',
                'default_value' => '1000',
                'type'          => 'integer',
                'group_name'    => 'nursing_school',
                'is_public'     => 1,
                'description'   'Non-refundable application fee in KES for nursing school applications.',
            ],
            [
                'item'          => 'nursing_intake_months',
                'default_value' => json_encode([
                    'september' => 'September Intake',
                    'january'   => 'January Intake',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'nursing_school',
                'is_public'     => 1,
                'description'   => 'JSON object of intake month keys to display labels.',
            ],
            [
                'item'          => 'nursing_programmes_offered',
                'default_value' => json_encode([
                    'krn'       => 'Kenya Registered Nurse (KRN)',
                    'krchn'     => 'Kenya Registered Community Health Nurse (KRCHN)',
                    'krn_mid'   => 'Kenya Registered Nurse & Midwife (KRN/M)',
                    'enrolled_nurse' => 'Enrolled Nurse (Certificate)',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'nursing_school',
                'is_public'     => 1,
                'description'   => 'JSON object of programme keys to display labels for the nursing programmes offered.',
            ],
            [
                'item'          => 'nursing_min_qualification',
                'default_value' => 'KCSE Mean Grade C (Minimum C in English, Biology, Chemistry, and Mathematics)',
                'type'          => 'string',
                'group_name'    => 'nursing_school',
                'is_public'     => 1,
                'description'   => 'Minimum academic qualification required for nursing school admission.',
            ],

            // ── Applications ─────────────────────────────────────────────────
            [
                'item'          => 'application_open',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'applications',
                'is_public'     => 1,
                'description'   => 'Master switch for whether the online application form is accepting submissions.',
            ],
            [
                'item'          => 'application_fee_kes',
                'default_value' => '1000',
                'type'          => 'integer',
                'group_name'    => 'applications',
                'is_public'     => 1,
                'description'   'Application processing fee in KES payable via M-Pesa.',
            ],
            [
                'item'          => 'application_deadline',
                'default_value' => null,
                'type'          => 'date',
                'group_name'    => 'applications',
                'is_public'     => 1,
                'description'   'Application submission deadline (YYYY-MM-DD). Null means rolling admissions.',
            ],
            [
                'item'          => 'application_requires_photo',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'applications',
                'is_public'     => 1,
                'description'   => 'Whether applicants must upload a passport-size photo.',
            ],
            [
                'item'          => 'application_requires_transcripts',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'applications',
                'is_public'     => 1,
                'description'   => 'Whether applicants must upload academic transcripts/certificates.',
            ],
            [
                'item'          => 'application_requires_id_copy',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'applications',
                'is_public'     => 1,
                'description'   => 'Whether applicants must upload a copy of their national ID or birth certificate.',
            ],
            [
                'item'          => 'application_requires_referees',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'applications',
                'is_public'     => 1,
                'description'   'Whether applicants must provide referee contacts.',
            ],
            [
                'item'          => 'application_min_referees',
                'default_value' => '2',
                'type'          => 'integer',
                'group_name'    => 'applications',
                'is_public'     => 1,
                'description'   => 'Minimum number of referees required per application.',
            ],
            [
                'item'          => 'application_review_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'applications',
                'is_public'     => 0,
                'description'   => 'Whether the application review workflow (screening, interview, decision) is active.',
            ],
            [
                'item'          => 'application_notification_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'applications',
                'is_public'     => 0,
                'description'   => 'Whether applicants receive email/SMS notifications at each status change.',
            ],
            [
                'item'          => 'application_status_flow',
                'default_value' => json_encode([
                    'submitted'   => 'Submitted',
                    'screening'   => 'Under Screening',
                    'interview'   => 'Interview Scheduled',
                    'interviewed' => 'Interviewed',
                    'offered'     => 'Admission Offered',
                    'accepted'    => 'Admission Accepted',
                    'rejected'    => 'Application Rejected',
                    'waitlisted'  => 'Waitlisted',
                    'deferred'    => 'Deferred to Next Intake',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'applications',
                'is_public'     => 1,
                'description'   => 'JSON object of application status keys to display labels. Keys match the wp_application_status_history.status ENUM values.',
            ],

            // ── Authentication & Security ────────────────────────────────────
            [
                'item'          => 'two_factor_auth_enabled',
                'default_value' => '0',
                'type'          => 'boolean',
                'group_name'    => 'auth',
                'is_public'     => 0,
                'description'   => 'Require two-factor authentication for admin and editor accounts.',
            ],
            [
                'item'          => 'session_lifetime_minutes',
                'default_value' => '120',
                'type'          => 'integer',
                'group_name'    => 'auth',
                'is_public'     => 0,
                'description'   => 'Idle session expiry in minutes before a user is logged out.',
            ],
            [
                'item'          => 'max_login_attempts',
                'default_value' => '5',
                'type'          => 'integer',
                'group_name'    => 'auth',
                'is_public'     => 0,
                'description'   => 'Maximum failed login attempts before temporary lockout.',
            ],
            [
                'item'          => 'lockout_duration_minutes',
                'default_value' => '15',
                'type'          => 'integer',
                'group_name'    => 'auth',
                'is_public'     => 0,
                'description'   => 'Duration in minutes an account remains locked after exceeding max_login_attempts.',
            ],
            [
                'item'          => 'password_min_length',
                'default_value' => '8',
                'type'          => 'integer',
                'group_name'    => 'auth',
                'is_public'     => 0,
                'description'   => 'Minimum number of characters required for user passwords.',
            ],
            [
                'item'          => 'password_require_uppercase',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'auth',
                'is_public'     => 0,
                'description'   => 'Require at least one uppercase letter in passwords.',
            ],
            [
                'item'          => 'password_require_number',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'auth',
                'is_public'     => 0,
                'description'   => 'Require at least one numeric digit in passwords.',
            ],
            [
                'item'          => 'public_registration_open',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'auth',
                'is_public'     => 1,
                'description'   => 'Whether public users (patients, community members) can self-register for an account.',
            ],
            [
                'item'          => 'default_user_role',
                'default_value' => 'subscriber',
                'type'          => 'string',
                'group_name'    => 'auth',
                'is_public'     => 0,
                'description'   => 'Default WordPress role assigned to new public user registrations. Must be one of the 5 core roles: subscriber, contributor, author, editor, administrator.',
            ],

            // ── Cloudflare Turnstile (Bot Protection) ────────────────────────
            [
                'item'          => 'turnstile_site_key',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'security',
                'is_public'     => 1,
                'description'   => 'Cloudflare Turnstile site key (public). Obtain from https://dash.cloudflare.com/ → Turnstile → Add Site.',
            ],
            [
                'item'          => 'turnstile_secret_key',
                'default_value' => null,
                'type'          => 'secret',
                'group_name'    => 'security',
                'is_public'     => 0,
                'description'   => 'Cloudflare Turnstile secret key (private). Never expose this value publicly.',
            ],
            [
                'item'          => 'captcha_on_contact_form',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'security',
                'is_public'     => 0,
                'description'   => 'Whether Turnstile captcha is required on the contact form.',
            ],
            [
                'item'          => 'captcha_on_appointment_booking',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'security',
                'is_public'     => 0,
                'description'   => 'Whether Turnstile captcha is required on the appointment booking form.',
            ],
            [
                'item'          => 'captcha_on_application_form',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'security',
                'is_public'     => 0,
                'description'   => 'Whether Turnstile captcha is required on the nursing school application form.',
            ],

            // ── SMTP / Email ─────────────────────────────────────────────────
            [
                'item'          => 'smtp_host',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'email',
                'is_public'     => 0,
                'description'   => 'SMTP server hostname for outbound transactional emails.',
            ],
            [
                'item'          => 'smtp_port',
                'default_value' => '587',
                'type'          => 'integer',
                'group_name'    => 'email',
                'is_public'     => 0,
                'description'   => 'SMTP port. Common values: 587 (STARTTLS), 465 (SSL), 2525 (Mailtrap sandbox).',
            ],
            [
                'item'          => 'smtp_encryption',
                'default_value' => 'tls',
                'type'          => 'string',
                'group_name'    => 'email',
                'is_public'     => 0,
                'description'   => 'SMTP encryption protocol: "tls" (STARTTLS) or "ssl". Leave blank for none.',
            ],
            [
                'item'          => 'smtp_username',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'email',
                'is_public'     => 0,
                'description'   => 'SMTP authentication username.',
            ],
            [
                'item'          => 'smtp_password',
                'default_value' => null,
                'type'          => 'secret',
                'group_name'    => 'email',
                'is_public'     => 0,
                'description'   => 'SMTP authentication password (stored encrypted).',
            ],
            [
                'item'          => 'smtp_from_email',
                'default_value' => null,
                'type'          => 'email',
                'group_name'    => 'email',
                'is_public'     => 0,
                'description'   => 'From address used on all outbound platform emails.',
            ],
            [
                'item'          => 'smtp_from_name',
                'default_value' => 'Our Lady of Lourdes Mwea Hospital',
                'type'          => 'string',
                'group_name'    => 'email',
                'is_public'     => 0,
                'description'   => 'From display name used on all outbound platform emails.',
            ],

            // ── Notifications ────────────────────────────────────────────────
            [
                'item'          => 'email_notifications_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'notifications',
                'is_public'     => 0,
                'description'   => 'Master switch for transactional email notifications (appointment confirmations, application status updates, contact form auto-replies).',
            ],
            [
                'item'          => 'sms_notifications_enabled',
                'default_value' => '0',
                'type'          => 'boolean',
                'group_name'    => 'notifications',
                'is_public'     => 0,
                'description'   => 'Whether SMS notifications are active (requires SMS gateway configuration).',
            ],
            [
                'item'          => 'sms_gateway_provider',
                'default_value' => 'africastalking',
                'type'          => 'string',
                'group_name'    => 'notifications',
                'is_public'     => 0,
                'description'   => 'SMS gateway provider: africastalking | twilio | nexmo | safaricom_sdp.',
            ],
            [
                'item'          => 'sms_gateway_api_key',
                'default_value' => null,
                'type'          => 'secret',
                'group_name'    => 'notifications',
                'is_public'     => 0,
                'description'   => 'API key for the configured SMS gateway provider.',
            ],
            [
                'item'          => 'sms_sender_id',
                'default_value' => 'OLLMH',
                'type'          => 'string',
                'group_name'    => 'notifications',
                'is_public'     => 0,
                'description'   => 'Alphanumeric sender ID for outbound SMS messages (max 11 chars).',
            ],
            [
                'item'          => 'appointment_reminder_sms_enabled',
                'default_value' => '0',
                'type'          => 'boolean',
                'group_name'    => 'notifications',
                'is_public'     => 0,
                'description'   => 'Whether SMS reminders are sent before appointments (requires sms_notifications_enabled).',
            ],
            [
                'item'          => 'application_status_sms_enabled',
                'default_value' => '0',
                'type'          => 'boolean',
                'group_name'    => 'notifications',
                'is_public'     => 0,
                'description'   => 'Whether SMS notifications are sent for application status changes.',
            ],

            // ── SEO ──────────────────────────────────────────────────────────
            [
                'item'          => 'seo_default_meta_title_template',
                'default_value' => '%%title%% %%sep%% %%sitename%%',
                'type'          => 'string',
                'group_name'    => 'seo',
                'is_public'     => 0,
                'description'   => 'Default meta title template for pages without a custom meta title. Variables: %%title%%, %%sep%%, %%sitename%%, %%page%%.',
            ],
            [
                'item'          => 'seo_default_meta_description_template',
                'default_value' => '%%excerpt%%',
                'type'          => 'string',
                'group_name'    => 'seo',
                'is_public'     => 0,
                'description'   => 'Default meta description template. Variables: %%excerpt%%, %%title%%, %%sitename%%.',
            ],
            [
                'item'          => 'seo_default_og_image_id',
                'default_value' => null,
                'type'          => 'integer',
                'group_name'    => 'seo',
                'is_public'     => 0,
                'description'   => 'Media asset ID of the default Open Graph image (1200×630px) used when a page does not have a custom og:image.',
            ],
            [
                'item'          => 'seo_twitter_handle',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'seo',
                'is_public'     => 1,
                'description'   => 'Twitter/X handle for the hospital (without @) used in twitter:card meta tags.',
            ],
            [
                'item'          => 'seo_google_analytics_id',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'seo',
                'is_public'     => 0,
                'description'   => 'Google Analytics 4 measurement ID (e.g. G-XXXXXXXXXX).',
            ],
            [
                'item'          => 'seo_sitemap_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'seo',
                'is_public'     => 0,
                'description'   => 'Whether XML sitemap generation is enabled.',
            ],
            [
                'item'          => 'seo_robots_default',
                'default_value' => 'index,follow',
                'type'          => 'string',
                'group_name'    => 'seo',
                'is_public'     => 0,
                'description'   => 'Default robots meta directive for pages without a custom directive: index,follow | noindex,follow | index,nofollow | noindex,nofollow.',
            ],
            [
                'item'          => 'seo_breadcrumbs_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'seo',
                'is_public'     => 0,
                'description'   => 'Whether breadcrumb generation is enabled (affects BreadcrumbList schema and on-page breadcrumbs).',
            ],

            // ── Financial / M-Pesa ───────────────────────────────────────────
            [
                'item'          => 'mpesa_environment',
                'default_value' => 'sandbox',
                'type'          => 'string',
                'group_name'    => 'financial',
                'is_public'     => 0,
                'description'   => 'Safaricom Daraja API environment: sandbox or production.',
            ],
            [
                'item'          => 'mpesa_consumer_key',
                'default_value' => null,
                'type'          => 'secret',
                'group_name'    => 'financial',
                'is_public'     => 0,
                'description'   => 'Safaricom Daraja API consumer key for M-Pesa STK Push integration.',
            ],
            [
                'item'          => 'mpesa_consumer_secret',
                'default_value' => null,
                'type'          => 'secret',
                'group_name'    => 'financial',
                'is_public'     => 0,
                'description'   => 'Safaricom Daraja API consumer secret for M-Pesa STK Push integration.',
            ],
            [
                'item'          => 'mpesa_shortcode',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'financial',
                'is_public'     => 0,
                'description'   => 'M-Pesa paybill or till number for application fee payments.',
            ],
            [
                'item'          => 'mpesa_passkey',
                'default_value' => null,
                'type'          => 'secret',
                'group_name'    => 'financial',
                'is_public'     => 0,
                'description'   => 'M-Pesa STK Push passkey for authentication.',
            ],
            [
                'item'          => 'mpesa_initiator_username',
                'default_value' => null,
                'type'          => 'string',
                'group_name'    => 'financial',
                'is_public'     => 0,
                'description'   => 'M-Pesa initiator username for B2C/C2B operations.',
            ],
            [
                'item'          => 'mpesa_initiator_password',
                'default_value' => null,
                'type'          => 'secret',
                'group_name'    => 'financial',
                'is_public'     => 0,
                'description'   => 'M-Pesa initiator password (stored encrypted).',
            ],
            [
                'item'          => 'mpesa_callback_url',
                'default_value' => null,
                'type'          => 'url',
                'group_name'    => 'financial',
                'is_public'     => 0,
                'description'   => 'Callback URL for M-Pesa STK Push payment confirmation.',
            ],
            [
                'item'          => 'invoice_prefix',
                'default_value' => 'OLLMH-',
                'type'          => 'string',
                'group_name'    => 'financial',
                'is_public'     => 0,
                'description'   => 'Prefix prepended to auto-generated invoice reference numbers.',
            ],
            [
                'item'          => 'receipt_prefix',
                'default_value' => 'RCP-',
                'type'          => 'string',
                'group_name'    => 'financial',
                'is_public'     => 0,
                'description'   => 'Prefix prepended to auto-generated receipt reference numbers.',
            ],
            [
                'item'          => 'payment_methods',
                'default_value' => json_encode([
                    'mpesa_stk'   => 'M-Pesa STK Push',
                    'mpesa_paybill' => 'M-Pesa Paybill (Manual)',
                    'cash'        => 'Cash (At Hospital)',
                    'bank_transfer' => 'Bank Transfer',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'financial',
                'is_public'     => 1,
                'description'   => 'JSON object of accepted payment method keys to display labels.',
            ],

            // ── Community / SMI ──────────────────────────────────────────────
            [
                'item'          => 'smi_community_name',
                'default_value' => 'Sisters of Mary Immaculate (SMI) Community',
                'type'          => 'string',
                'group_name'    => 'community',
                'is_public'     => 1,
                'description'   => 'Display name of the SMI community section.',
            ],
            [
                'item'          => 'smi_description',
                'default_value' => 'The Sisters of Mary Immaculate (SMI) community at Our Lady of Lourdes Mwea Hospital runs health outreach programs, community health education, and vocational discernment activities serving the Mwea community and beyond.',
                'type'          => 'text',
                'group_name'    => 'community',
                'is_public'     => 1,
                'description'   => 'SMI community description used on the community page and SEO meta.',
            ],
            [
                'item'          => 'community_outreach_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'community',
                'is_public'     => 1,
                'description'   => 'Whether the community outreach programs section is active.',
            ],
            [
                'item'          => 'volunteer_registration_open',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'community',
                'is_public'     => 1,
                'description'   => 'Whether volunteer registration is currently open.',
            ],
            [
                'item'          => 'vocation_enquiries_open',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'community',
                'is_public'     => 1,
                'description'   => 'Whether vocation/religious discernment enquiries are being accepted.',
            ],

            // ── Profile Reference Values ─────────────────────────────────────
            [
                'item'          => 'profile_salutations',
                'default_value' => json_encode([
                    'Mr'      => 'Mister',
                    'Mrs'     => 'Missus',
                    'Ms'      => 'Miss',
                    'Dr'      => 'Doctor',
                    'Prof'    => 'Professor',
                    'Sr'      => 'Sister',
                    'Fr'      => 'Father',
                    'Rev'     => 'Reverend',
                    'Bro'     => 'Brother',
                    'Bp'      => 'Bishop',
                    'Arch'    => 'Archbishop',
                    'Hon'     => 'Honourable',
                    'Eng'     => 'Engineer',
                    'Pst'     => 'Pastor',
                    'Sheikh'  => 'Sheikh',
                    'Imam'    => 'Imam',
                    'Chief'   => 'Chief',
                    'Elder'   => 'Elder',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of salutation keys to display labels used to populate salutation dropdowns for patient registration, staff records, and applications.',
            ],
            [
                'item'          => 'profile_genders',
                'default_value' => json_encode([
                    'male'   => 'Male',
                    'female' => 'Female',
                    'other'  => 'Other',
                    'prefer_not_to_say' => 'Prefer not to say',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of gender keys to display labels used in patient registration and staff records.',
            ],
            [
                'item'          => 'profile_languages',
                'default_value' => json_encode([
                    // ── National / Official ──
                    'swahili'   => 'Swahili (Kiswahili)',
                    'english'   => 'English',
                    // ── Central Kenya (relevant to Mwea) ──
                    'kikuyu'    => 'Kikuyu (Gikuyu)',
                    'embu'      => 'Embu (Kiembu)',
                    'mbeere'    => 'Mbeere (Kimbeere)',
                    'meru'      => 'Meru (Kimeru)',
                    'kamba'     => 'Kamba (Kikamba)',
                    // ── Other major Kenyan languages ──
                    'luo'       => 'Luo (Dholuo)',
                    'kisii'     => 'Kisii (Ekegusii)',
                    'kalenjin'  => 'Kalenjin',
                    'maasai'    => 'Maasai (Maa)',
                    'luhya'     => 'Luhya (Oluluhya)',
                    'somali'    => 'Somali',
                    'borana'    => 'Borana (Afaan Borana)',
                    // ── Kenyan Sign Language ──
                    'ksl'       => 'Kenyan Sign Language (KSL)',
                    // ── International ──
                    'arabic'    => 'Arabic',
                    'french'    => 'French',
                    'german'    => 'German',
                    'hindi'     => 'Hindi',
                    'chinese'   => 'Chinese (Mandarin)',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of language keys to display labels. Used in patient registration to record languages spoken.',
            ],
            [
                'item'          => 'profile_marital_statuses',
                'default_value' => json_encode([
                    'single'            => 'Single',
                    'married'           => 'Married',
                    'married_polygamous' => 'Married (Polygamous)',
                    'divorced'          => 'Divorced',
                    'widowed'           => 'Widowed',
                    'separated'         => 'Separated',
                    'cohabiting'        => 'Cohabiting',
                    'prefer_not_to_say' => 'Prefer not to say',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of marital status keys to display labels used in patient registration.',
            ],
            [
                'item'          => 'profile_education_levels',
                'default_value' => json_encode([
                    'none'                => 'No Formal Education',
                    'pre_primary'         => 'Pre-Primary (Nursery)',
                    'primary'             => 'Primary School (KCPE)',
                    'secondary'           => 'Secondary School (KCSE)',
                    'artisan'             => 'Artisan / Craft Certificate',
                    'certificate'         => 'Certificate (Post-Secondary)',
                    'diploma'             => 'Diploma',
                    'higher_diploma'      => 'Higher National Diploma',
                    'bachelors'           => 'Bachelor\'s Degree',
                    'postgraduate_dip'    => 'Postgraduate Diploma',
                    'masters'             => 'Master\'s Degree',
                    'phd'                 => 'Doctorate (PhD)',
                    'medical'             => 'Medical Degree (MBChB, BDS, PharmD)',
                    'nursing'             => 'Nursing Qualification (KRN, KRCHN)',
                    'theology'            => 'Theological / Religious Studies',
                    'other'               => 'Other',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of education level keys to display labels. Used in patient registration, staff records, and applications.',
            ],
            [
                'item'          => 'profile_employment_statuses',
                'default_value' => json_encode([
                    'employed_full_time'  => 'Employed (Full Time)',
                    'employed_part_time'  => 'Employed (Part Time)',
                    'self_employed'       => 'Self Employed',
                    'business_owner'      => 'Business Owner',
                    'unemployed'          => 'Unemployed',
                    'student'             => 'Student',
                    'retired'             => 'Retired',
                    'homemaker'           => 'Homemaker',
                    'farmer'              => 'Farmer',
                    'casual'              => 'Casual / Day Worker',
                    'civil_servant'       => 'Civil Servant',
                    'healthcare_worker'   => 'Healthcare Worker',
                    'clergy'              => 'Clergy / Religious Leader',
                    'prefer_not_to_say'   => 'Prefer not to say',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of employment status keys to display labels used in patient registration.',
            ],
            [
                'item'          => 'profile_blood_types',
                'default_value' => json_encode([
                    'A+'      => 'A Positive (A+)',
                    'A-'      => 'A Negative (A-)',
                    'B+'      => 'B Positive (B+)',
                    'B-'      => 'B Negative (B-)',
                    'AB+'     => 'AB Positive (AB+)',
                    'AB-'     => 'AB Negative (AB-)',
                    'O+'      => 'O Positive (O+)',
                    'O-'      => 'O Negative (O-)',
                    'unknown' => 'Unknown / Not Tested',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of ABO/Rh blood type keys to display labels used in patient registration.',
            ],
            [
                'item'          => 'profile_nationalities',
                'default_value' => json_encode([
                    // ── East Africa ──
                    'Kenyan'        => 'Kenyan',
                    'Ugandan'       => 'Ugandan',
                    'Tanzanian'     => 'Tanzanian',
                    'Rwandan'       => 'Rwandan',
                    'South_Sudanese'=> 'South Sudanese',
                    'Ethiopian'     => 'Ethiopian',
                    'Somali'        => 'Somali',
                    'Sudanese'      => 'Sudanese',
                    // ── Other African ──
                    'Nigerian'      => 'Nigerian',
                    'Congolese'     => 'Congolese (DRC)',
                    'Cameroonian'   => 'Cameroonian',
                    'Zambian'       => 'Zambian',
                    'Malawian'      => 'Malawian',
                    // ── International ──
                    'Indian'        => 'Indian',
                    'British'       => 'British',
                    'American'      => 'American',
                    'Chinese'       => 'Chinese',
                    'Other'         => 'Other',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of nationality keys to display labels used in patient registration and applications.',
            ],
            [
                'item'          => 'profile_counties',
                'default_value' => json_encode([
                    // ── Kenya's 47 counties (alphabetical) ──
                    'baringo'      => 'Baringo',
                    'bomet'        => 'Bomet',
                    'bungoma'      => 'Bungoma',
                    'busia'        => 'Busia',
                    'elgeyo_marakwet' => 'Elgeyo-Marakwet',
                    'embu'         => 'Embu',
                    'garissa'      => 'Garissa',
                    'homa_bay'     => 'Homa Bay',
                    'isiolo'       => 'Isiolo',
                    'kajiado'      => 'Kajiado',
                    'kakamega'     => 'Kakamega',
                    'kericho'      => 'Kericho',
                    'kiambu'       => 'Kiambu',
                    'kilifi'       => 'Kilifi',
                    'kirinyaga'    => 'Kirinyaga',
                    'kisii'        => 'Kisii',
                    'kisumu'       => 'Kisumu',
                    'kitui'        => 'Kitui',
                    'kwale'        => 'Kwale',
                    'laikipia'     => 'Laikipia',
                    'lamu'         => 'Lamu',
                    'machakos'     => 'Machakos',
                    'makueni'      => 'Makueni',
                    'mandera'      => 'Mandera',
                    'marsabit'     => 'Marsabit',
                    'meru'         => 'Meru',
                    'migori'       => 'Migori',
                    'marsabit'     => 'Marsabit',
                    'mombasa'      => 'Mombasa',
                    'muranga'      => 'Murang\'a',
                    'nairobi'      => 'Nairobi',
                    'nakuru'       => 'Nakuru',
                    'nandi'        => 'Nandi',
                    'narok'        => 'Narok',
                    'nyamira'      => 'Nyamira',
                    'nyandarua'    => 'Nyandarua',
                    'nyeri'        => 'Nyeri',
                    'samburu'      => 'Samburu',
                    'siaya'        => 'Siaya',
                    'taita_taveta' => 'Taita-Taveta',
                    'tana_river'   => 'Tana River',
                    'tharaka_nithi'=> 'Tharaka-Nithi',
                    'trans_nzoia'  => 'Trans Nzoia',
                    'turkana'      => 'Turkana',
                    'uasin_gishu'  => 'Uasin Gishu',
                    'vihiga'       => 'Vihiga',
                    'wajir'        => 'Wajir',
                    'west_pokot'   => 'West Pokot',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of Kenya\'s 47 county keys to display labels. Used in patient registration to record county of residence.',
            ],
            [
                'item'          => 'profile_relationships',
                'default_value' => json_encode([
                    'spouse'        => 'Spouse / Partner',
                    'parent'        => 'Parent',
                    'child'         => 'Child',
                    'sibling'       => 'Sibling',
                    'grandparent'   => 'Grandparent',
                    'grandchild'    => 'Grandchild',
                    'aunt_uncle'    => 'Aunt / Uncle',
                    'niece_nephew'  => 'Niece / Nephew',
                    'cousin'        => 'Cousin',
                    'guardian'      => 'Legal Guardian',
                    'friend'        => 'Friend',
                    'other'         => 'Other',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of next-of-kin relationship keys to display labels used in patient registration.',
            ],
            [
                'item'          => 'profile_security_questions',
                'default_value' => json_encode([
                    'first_pet'         => 'What was the name of your first pet?',
                    'first_school'      => 'What was the name of your primary school?',
                    'mothers_maiden'    => 'What is your mother\'s maiden name?',
                    'birth_city'        => 'In what town or city were you born?',
                    'oldest_sibling'    => 'What is the name of your oldest sibling?',
                    'favourite_teacher' => 'What was the name of your favourite teacher?',
                    'childhood_nickname'=> 'What was your childhood nickname?',
                    'hometown'          => 'What is the name of your hometown?',
                ], JSON_UNESCAPED_UNICODE),
                'type'          => 'json',
                'group_name'    => 'profiles',
                'is_public'     => 1,
                'description'   => 'JSON object of security question keys to display labels for password recovery.',
            ],

            // ── Cache ────────────────────────────────────────────────────────
            [
                'item'          => 'cache_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'cache',
                'is_public'     => 0,
                'description'   => 'Whether the application-level cache layer is active.',
            ],
            [
                'item'          => 'cache_default_ttl_seconds',
                'default_value' => '3600',
                'type'          => 'integer',
                'group_name'    => 'cache',
                'is_public'     => 0,
                'description'   => 'Default time-to-live in seconds for cached entries.',
            ],
            [
                'item'          => 'cache_clinic_schedule_ttl_seconds',
                'default_value' => '86400',
                'type'          => 'integer',
                'group_name'    => 'cache',
                'is_public'     => 0,
                'description'   => 'TTL in seconds for cached clinic schedules and OPD operating hours.',
            ],

            // ── Analytics ────────────────────────────────────────────────────
            [
                'item'          => 'analytics_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'analytics',
                'is_public'     => 0,
                'description'   => 'Whether platform analytics tracking and aggregation is active.',
            ],
            [
                'item'          => 'analytics_retention_days',
                'default_value' => '365',
                'type'          => 'integer',
                'group_name'    => 'analytics',
                'is_public'     => 0,
                'description'   => 'Number of days to retain raw analytics records before archiving.',
            ],
            [
                'item'          => 'audit_log_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'analytics',
                'is_public'     => 0,
                'description'   => 'Whether the audit trail is active for compliance logging (user logins, content changes, settings changes).',
            ],

            // ── Jobs / Queue ─────────────────────────────────────────────────
            [
                'item'          => 'job_queue_enabled',
                'default_value' => '1',
                'type'          => 'boolean',
                'group_name'    => 'jobs',
                'is_public'     => 0,
                'description'   => 'Whether the background job queue processor is active (for email sending, SMS, notifications).',
            ],
            [
                'item'          => 'job_queue_batch_size',
                'default_value' => '20',
                'type'          => 'integer',
                'group_name'    => 'jobs',
                'is_public'     => 0,
                'description'   => 'Number of jobs processed per cron execution cycle.',
            ],
            [
                'item'          => 'job_max_attempts',
                'default_value' => '3',
                'type'          => 'integer',
                'group_name'    => 'jobs',
                'is_public'     => 0,
                'description'   => 'Maximum retry attempts for a failed background job before it is marked as dead.',
            ],
            [
                'item'          => 'job_retention_days',
                'default_value' => '30',
                'type'          => 'integer',
                'group_name'    => 'jobs',
                'is_public'     => 0,
                'description'   => 'Number of days to retain completed and failed job records before pruning.',
            ],
        ];
    }

    /**
     * Insert-only upsert: sets current_value = default_value on first insert,
     * never overwrites a current_value that has already been customised.
     *
     * @return array{success: bool, inserted: int, updated: int, skipped?: bool, error?: string}
     */
    public function run(): array {
        global $wpdb;
        $table = $this->get_table();

        // Skip if the target table doesn't exist yet (e.g. fresh install, tables still being created)
        if (!$this->table_exists()) {
            return [
                'success'  => true,
                'inserted' => 0,
                'updated'  => 0,
                'skipped'  => true,
                'error'    => "Table {$table} does not exist yet — skipping seeder.",
            ];
        }

        $now      = current_time('mysql', true);
        $inserted = 0;
        $updated  = 0;

        foreach ($this->get_settings() as $setting) {
            $existing = $wpdb->get_var($wpdb->prepare(
                "SELECT id FROM {$table} WHERE item = %s",
                $setting['item']
            ));

            if ($existing) {
                // Capture the old default_value before we overwrite it.
                $old_default = $wpdb->get_var($wpdb->prepare(
                    "SELECT default_value FROM {$table} WHERE id = %d",
                    $existing
                ));

                // Refresh default_value on existing rows.
                $wpdb->update(
                    $table,
                    [
                        'default_value' => $setting['default_value'],
                        'description'   => $setting['description'],
                        'type'          => $setting['type'],
                        'group_name'    => $setting['group_name'],
                        'is_public'     => $setting['is_public'],
                        'updated_at'    => $now,
                    ],
                    ['id' => $existing]
                );

                // If current_value was never customised (empty, null, or
                // still equal to the old default), sync it to the new default.
                $current_val = $wpdb->get_var($wpdb->prepare(
                    "SELECT current_value FROM {$table} WHERE id = %d",
                    $existing
                ));
                if ($current_val === '' || $current_val === null || $current_val === $old_default) {
                    $wpdb->update(
                        $table,
                        ['current_value' => $setting['default_value'], 'updated_at' => $now],
                        ['id' => $existing]
                    );
                }
                $updated++;
            } else {
                $default = $setting['default_value'];
                $wpdb->insert(
                    $table,
                    [
                        'item'          => $setting['item'],
                        'default_value' => $default,
                        'current_value' => $default,
                        'description'   => $setting['description'],
                        'type'          => $setting['type'],
                        'group_name'    => $setting['group_name'],
                        'is_public'     => $setting['is_public'],
                        'created_at'    => $now,
                        'updated_at'    => $now,
                    ],
                    [
                        '%s',
                        is_null($default) ? null : '%s',
                        is_null($default) ? null : '%s',
                        '%s',
                        '%s',
                        '%s',
                        '%d',
                        '%s',
                        '%s',
                    ]
                );
                $inserted++;
            }
        }

        return [
            'success'  => true,
            'inserted' => $inserted,
            'updated'  => $updated,
        ];
    }
}
