<?php
/**
 * OLLMH Seeder Base Class
 *
 * Base class for all OLLMH database seeders. Provides the common interface
 * for insert-only upsert seeding: never overwrites a current_value that an
 * admin has already customised.
 *
 * @package OLLMH\Seeders
 */

if (!defined('ABSPATH')) {
    exit;
}

/**
 * Abstract base class for seeders.
 */
abstract class OLLMH_Seeder_Base {

    /**
     * The table name (without wp_ prefix).
     *
     * @return string
     */
    abstract protected function get_table_name(): string;

    /**
     * Fetch source data from an external system (if applicable).
     * Override in subclasses that sync from an external API.
     *
     * @return array{success: bool, data: array}
     */
    protected function fetch_from_source(): array {
        return ['success' => true, 'data' => []];
    }

    /**
     * Run the seeder. Implemented by each subclass.
     *
     * @return array{success: bool, inserted: int, updated: int, skipped?: bool, error?: string}
     */
    abstract public function run(): array;

    /**
     * Check if the target table exists in the database.
     *
     * @return bool
     */
    protected function table_exists(): bool {
        global $wpdb;
        $table = $wpdb->prefix . $this->get_table_name();
        $result = $wpdb->get_var($wpdb->prepare("SHOW TABLES LIKE %s", $table));
        return (bool) $result;
    }

    /**
     * Get the fully-qualified table name.
     *
     * @return string
     */
    protected function get_table(): string {
        global $wpdb;
        return $wpdb->prefix . $this->get_table_name();
    }
}
