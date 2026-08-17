# Cron Jobs & Scheduled Tasks

> This document defines all scheduled tasks for the OLLMH WordPress site.
>
> **Related:** [`SETTINGS.md`](./SETTINGS.md) → `jobs` group,
> [`EMAIL-TEMPLATES.md`](./EMAIL-TEMPLATES.md) for notification templates.

---

## 1. WP-Cron vs system cron

### Development (local Docker)

Use WP-Cron (default WordPress behavior). WP-Cron runs on every page load
if a scheduled task is due.

```php
// wp-config.php — default (WP-Cron enabled)
define('DISABLE_WP_CRON', false);
```

### Production

Use **system cron** for reliability (WP-Cron depends on site traffic,
which may be low for a hospital website). Set up a system cron job to
trigger WP-Cron every 5 minutes:

```bash
# Add to crontab (crontab -e)
*/5 * * * * curl -s https://ourladyoflourdesmweahospital.org/wp-cron.php?doing_wp_cron > /dev/null 2>&1
```

```php
// wp-config.php — disable WP-Cron (system cron handles it)
define('DISABLE_WP_CRON', true);
```

---

## 2. Scheduled tasks

| Task | Hook name | Schedule | Plugin | Purpose |
|---|---|---|---|---|
| Process notification queue | `ollmh_process_notifications` | Every 5 min | `ollmh-notifications` | Send queued emails/SMS |
| Send appointment reminders | `ollmh_send_appointment_reminders` | Hourly | `ollmh-notifications` | Check for appointments due in `appointment_reminder_hours` |
| Send event reminders | `ollmh_send_event_reminders` | Hourly | `ollmh-notifications` | Check for events happening in 24 hours |
| Clean expired transients | `ollmh_clean_transients` | Daily | `ollmh-core` | Remove expired cache entries |
| Prune old logs | `ollmh_prune_logs` | Daily | `ollmh-core` | Delete notification/audit logs older than `analytics_retention_days` |
| Prune completed jobs | `ollmh_prune_jobs` | Daily | `ollmh-core` | Delete completed/failed jobs older than `job_retention_days` |
| Database optimization | `ollmh_optimize_db` | Weekly | `ollmh-core` | Run `OPTIMIZE TABLE` on all custom tables |
| Sitemap regeneration | `ollmh_regenerate_sitemap` | Daily | Rank Math | Regenerate XML sitemap |
| Check for broken links | `ollmh_check_broken_links` | Weekly | Broken Link Checker | Scan all content for broken links |
| Backup database | `ollmh_backup_db` | Daily | Backup plugin | Database backup (see [`BACKUP-RECOVERY.md`](./BACKUP-RECOVERY.md)) |
| Backup files | `ollmh_backup_files` | Weekly | Backup plugin | File backup |
| Update application statuses | `ollmh_auto_expire_applications` | Daily | `ollmh-core` | Mark applications as expired if past deadline |
| Clear cache | `ollmh_clear_cache` | Daily (3 AM) | W3 Total Cache | Clear page cache for fresh content |

---

## 3. Registration code

```php
<?php
// ollmh-core/includes/class-ollmh-cron.php

if (!defined('ABSPATH')) {
    exit;
}

class OLLMH_Cron {

    public static function init(): void {
        // Register custom cron schedules
        add_filter('cron_schedules', [self::class, 'add_schedules']);

        // Schedule events on activation
        add_action('ollmh_activate', [self::class, 'schedule_events']);

        // Clear on deactivation
        add_action('ollmh_deactivate', [self::class, 'clear_events']);

        // Hook task callbacks
        add_action('ollmh_process_notifications', [self::class, 'process_notifications']);
        add_action('ollmh_send_appointment_reminders', [self::class, 'send_appointment_reminders']);
        add_action('ollmh_send_event_reminders', [self::class, 'send_event_reminders']);
        add_action('ollmh_clean_transients', [self::class, 'clean_transients']);
        add_action('ollmh_prune_logs', [self::class, 'prune_logs']);
        add_action('ollmh_prune_jobs', [self::class, 'prune_jobs']);
        add_action('ollmh_optimize_db', [self::class, 'optimize_db']);
        add_action('ollmh_auto_expire_applications', [self::class, 'auto_expire_applications']);
    }

    public static function add_schedules(array $schedules): array {
        $schedules['every_5_minutes'] = [
            'interval' => 300,
            'display'  => __('Every 5 Minutes', 'ollmh-core'),
        ];
        return $schedules;
    }

    public static function schedule_events(): void {
        if (!wp_next_scheduled('ollmh_process_notifications')) {
            wp_schedule_event(time(), 'every_5_minutes', 'ollmh_process_notifications');
        }
        if (!wp_next_scheduled('ollmh_send_appointment_reminders')) {
            wp_schedule_event(time(), 'hourly', 'ollmh_send_appointment_reminders');
        }
        if (!wp_next_scheduled('ollmh_send_event_reminders')) {
            wp_schedule_event(time(), 'hourly', 'ollmh_send_event_reminders');
        }
        if (!wp_next_scheduled('ollmh_clean_transients')) {
            wp_schedule_event(time(), 'daily', 'ollmh_clean_transients');
        }
        if (!wp_next_scheduled('ollmh_prune_logs')) {
            wp_schedule_event(time(), 'daily', 'ollmh_prune_logs');
        }
        if (!wp_next_scheduled('ollmh_prune_jobs')) {
            wp_schedule_event(time(), 'daily', 'ollmh_prune_jobs');
        }
        if (!wp_next_scheduled('ollmh_optimize_db')) {
            wp_schedule_event(time(), 'weekly', 'ollmh_optimize_db');
        }
        if (!wp_next_scheduled('ollmh_auto_expire_applications')) {
            wp_schedule_event(time(), 'daily', 'ollmh_auto_expire_applications');
        }
    }

    public static function clear_events(): void {
        wp_clear_scheduled_hook('ollmh_process_notifications');
        wp_clear_scheduled_hook('ollmh_send_appointment_reminders');
        wp_clear_scheduled_hook('ollmh_send_event_reminders');
        wp_clear_scheduled_hook('ollmh_clean_transients');
        wp_clear_scheduled_hook('ollmh_prune_logs');
        wp_clear_scheduled_hook('ollmh_prune_jobs');
        wp_clear_scheduled_hook('ollmh_optimize_db');
        wp_clear_scheduled_hook('ollmh_auto_expire_applications');
    }

    // ── Task implementations ──────────────────────────────────────

    public static function process_notifications(): void {
        OLLMH_Notification_Queue::process_batch(
            (int) OLLMH_Helpers::get_setting('job_queue_batch_size', 20)
        );
    }

    public static function send_appointment_reminders(): void {
        global $wpdb;
        $reminder_hours = (int) OLLMH_Helpers::get_setting('appointment_reminder_hours', 24);
        $reminder_time = date('Y-m-d H:i:s', time() + $reminder_hours * 3600);

        $appointments = $wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$wpdb->prefix}opd_appointments
             WHERE appointment_date BETWEEN %s AND %s
             AND status = 'confirmed'
             AND reminder_sent = 0",
            date('Y-m-d H:i:s'),
            $reminder_time
        ));

        foreach ($appointments as $appointment) {
            OLLMH_Mailer::send('appointment-reminder', $appointment);
            $wpdb->update(
                "{$wpdb->prefix}opd_appointments",
                ['reminder_sent' => 1],
                ['id' => $appointment->id]
            );
        }
    }

    public static function send_event_reminders(): void {
        // Similar to appointment reminders — check for events in 24 hours
        // Send reminder to all registered attendees
    }

    public static function clean_transients(): void {
        global $wpdb;
        $wpdb->query(
            "DELETE FROM {$wpdb->prefix}options
             WHERE option_name LIKE '\_transient\_ollmh\_%'
             AND option_value NOT LIKE 'a:%'"
        );
    }

    public static function prune_logs(): void {
        global $wpdb;
        $retention_days = (int) OLLMH_Helpers::get_setting('analytics_retention_days', 365);
        $cutoff = date('Y-m-d H:i:s', time() - $retention_days * 86400);

        $wpdb->query($wpdb->prepare(
            "DELETE FROM {$wpdb->prefix}notification_logs WHERE created_at < %s",
            $cutoff
        ));
        $wpdb->query($wpdb->prepare(
            "DELETE FROM {$wpdb->prefix}audit_logs WHERE created_at < %s",
            $cutoff
        ));
    }

    public static function prune_jobs(): void {
        global $wpdb;
        $retention_days = (int) OLLMH_Helpers::get_setting('job_retention_days', 30);
        $cutoff = date('Y-m-d H:i:s', time() - $retention_days * 86400);

        $wpdb->query($wpdb->prepare(
            "DELETE FROM {$wpdb->prefix}job_queue WHERE completed_at < %s",
            $cutoff
        ));
    }

    public static function optimize_db(): void {
        global $wpdb;
        $tables = $wpdb->get_col("SHOW TABLES LIKE '{$wpdb->prefix}%'");
        foreach ($tables as $table) {
            $wpdb->query("OPTIMIZE TABLE {$table}");
        }
    }

    public static function auto_expire_applications(): void {
        global $wpdb;
        $deadline = OLLMH_Helpers::get_setting('application_deadline');
        if (!$deadline) {
            return; // Rolling admissions — no expiry
        }
        $wpdb->query($wpdb->prepare(
            "UPDATE {$wpdb->prefix}applications
             SET status = 'expired'
             WHERE status = 'submitted' AND created_at < %s",
            $deadline
        ));
    }
}
```

---

## 4. Monitoring cron health

Install [WP Crontrol](https://wordpress.org/plugins/wp-control/) plugin
to monitor cron jobs via the admin UI:

- View all scheduled events
- See when each event last ran
- Manually run events
- Edit or delete events

**Alert:** If any cron job hasn't run in 24 hours, check:
1. Is system cron configured? (`crontab -l`)
2. Is `wp-cron.php` accessible? (`curl -s https://ollmh.org/wp-cron.php`)
3. Are there PHP errors in `debug.log`?
4. Is `DISABLE_WP_CRON` set correctly?
