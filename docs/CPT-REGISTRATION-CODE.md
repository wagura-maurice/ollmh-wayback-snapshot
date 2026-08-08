# CPT Registration Code

> This document contains the actual PHP `register_post_type()` and
> `register_taxonomy()` code for all 14 OLLMH Custom Post Types and 5
> custom taxonomies. This code lives in the `ollmh-core` plugin (see
> [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md)).
>
> **Related:** [`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md) for the admin menu
> mapping, [`USER-ROLES.md`](./USER-ROLES.md) for capability assignments.

---

## 1. Registration class

All CPT and taxonomy registrations are in a single class:
`OLLMH_CPT` (file: `ollmh-core/includes/class-ollmh-cpt.php`).

```php
<?php
if (!defined('ABSPATH')) {
    exit;
}

class OLLMH_CPT {

    public static function init(): void {
        add_action('init', [self::class, 'register_post_types'], 5);
        add_action('init', [self::class, 'register_taxonomies'], 5);
        add_filter('theme_page_templates', [self::class, 'register_page_templates']);
    }

    // ──────────────────────────────────────────────────────────────
    //  CUSTOM POST TYPES
    // ──────────────────────────────────────────────────────────────

    public static function register_post_types(): void {
        self::register_news_article();
        self::register_event();
        self::register_department();
        self::register_ward();
        self::register_clinic();
        self::register_special_service();
        self::register_staff_member();
        self::register_job_vacancy();
        self::register_nursing_programme();
        self::register_development_project();
        self::register_sustainability_project();
        self::register_upcoming_project();
        self::register_community_program();
        self::register_smi_event();
        self::register_outlook_album();
    }

    // ── 1. News Article ───────────────────────────────────────────
    private static function register_news_article(): void {
        register_post_type('news_article', [
            'labels' => [
                'name'               => __('News', 'ollmh-core'),
                'singular_name'      => __('News Article', 'ollmh-core'),
                'add_new'            => __('Add New Article', 'ollmh-core'),
                'add_new_item'       => __('Add New News Article', 'ollmh-core'),
                'edit_item'          => __('Edit News Article', 'ollmh-core'),
                'new_item'           => __('New News Article', 'ollmh-core'),
                'view_item'          => __('View News Article', 'ollmh-core'),
                'search_items'       => __('Search News Articles', 'ollmh-core'),
                'not_found'          => __('No news articles found', 'ollmh-core'),
                'not_found_in_trash' => __('No news articles in trash', 'ollmh-core'),
                'all_items'          => __('All News Articles', 'ollmh-core'),
                'menu_name'          => __('News', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'news', 'with_front' => false],
            'menu_position'       => 5,
            'menu_icon'           => 'dashicons-admin-post',
            'supports'            => ['title', 'editor', 'excerpt', 'thumbnail', 'revisions', 'comments'],
            'capability_type'     => 'news_article',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,  // Enable block editor
        ]);
    }

    // ── 2. Event ──────────────────────────────────────────────────
    private static function register_event(): void {
        register_post_type('event', [
            'labels' => [
                'name'               => __('Events', 'ollmh-core'),
                'singular_name'      => __('Event', 'ollmh-core'),
                'add_new'            => __('Add New Event', 'ollmh-core'),
                'add_new_item'       => __('Add New Event', 'ollmh-core'),
                'edit_item'          => __('Edit Event', 'ollmh-core'),
                'new_item'           => __('New Event', 'ollmh-core'),
                'view_item'          => __('View Event', 'ollmh-core'),
                'search_items'       => __('Search Events', 'ollmh-core'),
                'not_found'          => __('No events found', 'ollmh-core'),
                'not_found_in_trash' => __('No events in trash', 'ollmh-core'),
                'all_items'          => __('All Events', 'ollmh-core'),
                'menu_name'          => __('Events', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'events', 'with_front' => false],
            'menu_position'       => 6,
            'menu_icon'           => 'dashicons-calendar',
            'supports'            => ['title', 'editor', 'excerpt', 'thumbnail'],
            'capability_type'     => 'event',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 3. Department ─────────────────────────────────────────────
    private static function register_department(): void {
        register_post_type('department', [
            'labels' => [
                'name'               => __('Departments', 'ollmh-core'),
                'singular_name'      => __('Department', 'ollmh-core'),
                'add_new'            => __('Add New Department', 'ollmh-core'),
                'add_new_item'       => __('Add New Department', 'ollmh-core'),
                'edit_item'          => __('Edit Department', 'ollmh-core'),
                'new_item'           => __('New Department', 'ollmh-core'),
                'view_item'          => __('View Department', 'ollmh-core'),
                'search_items'       => __('Search Departments', 'ollmh-core'),
                'not_found'          => __('No departments found', 'ollmh-core'),
                'not_found_in_trash' => __('No departments in trash', 'ollmh-core'),
                'all_items'          => __('All Departments', 'ollmh-core'),
                'menu_name'          => __('Departments', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'departments', 'with_front' => false],
            'menu_position'       => 7,
            'menu_icon'           => 'dashicons-building',
            'supports'            => ['title', 'editor', 'excerpt', 'thumbnail'],
            'capability_type'     => 'department',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 4. Ward ───────────────────────────────────────────────────
    private static function register_ward(): void {
        register_post_type('ward', [
            'labels' => [
                'name'               => __('Wards', 'ollmh-core'),
                'singular_name'      => __('Ward', 'ollmh-core'),
                'add_new'            => __('Add New Ward', 'ollmh-core'),
                'add_new_item'       => __('Add New Ward', 'ollmh-core'),
                'edit_item'          => __('Edit Ward', 'ollmh-core'),
                'new_item'           => __('New Ward', 'ollmh-core'),
                'view_item'          => __('View Ward', 'ollmh-core'),
                'search_items'       => __('Search Wards', 'ollmh-core'),
                'not_found'          => __('No wards found', 'ollmh-core'),
                'not_found_in_trash' => __('No wards in trash', 'ollmh-core'),
                'all_items'          => __('All Wards', 'ollmh-core'),
                'menu_name'          => __('Wards', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => false,
            'rewrite'             => ['slug' => 'wards', 'with_front' => false],
            'menu_position'       => 8,
            'menu_icon'           => 'dashicons-bed',
            'supports'            => ['title', 'editor', 'thumbnail'],
            'capability_type'     => 'ward',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 5. Clinic ─────────────────────────────────────────────────
    private static function register_clinic(): void {
        register_post_type('clinic', [
            'labels' => [
                'name'               => __('Clinics', 'ollmh-core'),
                'singular_name'      => __('Clinic', 'ollmh-core'),
                'add_new'            => __('Add New Clinic', 'ollmh-core'),
                'add_new_item'       => __('Add New Clinic', 'ollmh-core'),
                'edit_item'          => __('Edit Clinic', 'ollmh-core'),
                'new_item'           => __('New Clinic', 'ollmh-core'),
                'view_item'          => __('View Clinic', 'ollmh-core'),
                'search_items'       => __('Search Clinics', 'ollmh-core'),
                'not_found'          => __('No clinics found', 'ollmh-core'),
                'not_found_in_trash' => __('No clinics in trash', 'ollmh-core'),
                'all_items'          => __('All Clinics', 'ollmh-core'),
                'menu_name'          => __('Clinics', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => false,
            'rewrite'             => ['slug' => 'clinics', 'with_front' => false],
            'menu_position'       => 9,
            'menu_icon'           => 'dashicons-clock',
            'supports'            => ['title', 'editor', 'excerpt'],
            'capability_type'     => 'clinic',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 6. Special Medical Service ────────────────────────────────
    private static function register_special_service(): void {
        register_post_type('special_service', [
            'labels' => [
                'name'               => __('Special Medical Services', 'ollmh-core'),
                'singular_name'      => __('Special Service', 'ollmh-core'),
                'add_new'            => __('Add New Service', 'ollmh-core'),
                'add_new_item'       => __('Add New Special Service', 'ollmh-core'),
                'edit_item'          => __('Edit Special Service', 'ollmh-core'),
                'new_item'           => __('New Special Service', 'ollmh-core'),
                'view_item'          => __('View Special Service', 'ollmh-core'),
                'search_items'       => __('Search Special Services', 'ollmh-core'),
                'not_found'          => __('No special services found', 'ollmh-core'),
                'not_found_in_trash' => __('No special services in trash', 'ollmh-core'),
                'all_items'          => __('All Special Services', 'ollmh-core'),
                'menu_name'          => __('Special Services', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => false,
            'rewrite'             => ['slug' => 'special-services', 'with_front' => false],
            'menu_position'       => 10,
            'menu_icon'           => 'dashicons-shield-alt',
            'supports'            => ['title', 'editor', 'thumbnail'],
            'capability_type'     => 'special_service',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 7. Staff Member ───────────────────────────────────────────
    private static function register_staff_member(): void {
        register_post_type('staff_member', [
            'labels' => [
                'name'               => __('Staff', 'ollmh-core'),
                'singular_name'      => __('Staff Member', 'ollmh-core'),
                'add_new'            => __('Add New Staff Member', 'ollmh-core'),
                'add_new_item'       => __('Add New Staff Member', 'ollmh-core'),
                'edit_item'          => __('Edit Staff Member', 'ollmh-core'),
                'new_item'           => __('New Staff Member', 'ollmh-core'),
                'view_item'          => __('View Staff Member', 'ollmh-core'),
                'search_items'       => __('Search Staff', 'ollmh-core'),
                'not_found'          => __('No staff members found', 'ollmh-core'),
                'not_found_in_trash' => __('No staff members in trash', 'ollmh-core'),
                'all_items'          => __('All Staff', 'ollmh-core'),
                'menu_name'          => __('Staff & HR', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'staff', 'with_front' => false],
            'menu_position'       => 11,
            'menu_icon'           => 'dashicons-groups',
            'supports'            => ['title', 'editor', 'thumbnail'],
            'capability_type'     => 'staff',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 8. Job Vacancy ────────────────────────────────────────────
    private static function register_job_vacancy(): void {
        register_post_type('job_vacancy', [
            'labels' => [
                'name'               => __('Job Vacancies', 'ollmh-core'),
                'singular_name'      => __('Job Vacancy', 'ollmh-core'),
                'add_new'            => __('Add New Vacancy', 'ollmh-core'),
                'add_new_item'       => __('Add New Job Vacancy', 'ollmh-core'),
                'edit_item'          => __('Edit Job Vacancy', 'ollmh-core'),
                'new_item'           => __('New Job Vacancy', 'ollmh-core'),
                'view_item'          => __('View Job Vacancy', 'ollmh-core'),
                'search_items'       => __('Search Job Vacancies', 'ollmh-core'),
                'not_found'          => __('No job vacancies found', 'ollmh-core'),
                'not_found_in_trash' => __('No job vacancies in trash', 'ollmh-core'),
                'all_items'          => __('All Job Vacancies', 'ollmh-core'),
                'menu_name'          => __('Job Vacancies', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'careers', 'with_front' => false],
            'menu_position'       => 12,
            'menu_icon'           => 'dashicons-businessperson',
            'supports'            => ['title', 'editor', 'excerpt'],
            'capability_type'     => 'job_vacancy',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 9. Nursing Programme ──────────────────────────────────────
    private static function register_nursing_programme(): void {
        register_post_type('nursing_programme', [
            'labels' => [
                'name'               => __('Nursing Programmes', 'ollmh-core'),
                'singular_name'      => __('Nursing Programme', 'ollmh-core'),
                'add_new'            => __('Add New Programme', 'ollmh-core'),
                'add_new_item'       => __('Add New Nursing Programme', 'ollmh-core'),
                'edit_item'          => __('Edit Nursing Programme', 'ollmh-core'),
                'new_item'           => __('New Nursing Programme', 'ollmh-core'),
                'view_item'          => __('View Nursing Programme', 'ollmh-core'),
                'search_items'       => __('Search Nursing Programmes', 'ollmh-core'),
                'not_found'          => __('No nursing programmes found', 'ollmh-core'),
                'not_found_in_trash' => __('No nursing programmes in trash', 'ollmh-core'),
                'all_items'          => __('All Nursing Programmes', 'ollmh-core'),
                'menu_name'          => __('Nursing School', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => false,
            'rewrite'             => ['slug' => 'nursing/programmes', 'with_front' => false],
            'menu_position'       => 13,
            'menu_icon'           => 'dashicons-welcome-learn-more',
            'supports'            => ['title', 'editor', 'excerpt'],
            'capability_type'     => 'nursing_programme',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 10. Development Project ───────────────────────────────────
    private static function register_development_project(): void {
        register_post_type('development_project', [
            'labels' => [
                'name'               => __('Development Projects', 'ollmh-core'),
                'singular_name'      => __('Development Project', 'ollmh-core'),
                'add_new'            => __('Add New Project', 'ollmh-core'),
                'add_new_item'       => __('Add New Development Project', 'ollmh-core'),
                'edit_item'          => __('Edit Development Project', 'ollmh-core'),
                'new_item'           => __('New Development Project', 'ollmh-core'),
                'view_item'          => __('View Development Project', 'ollmh-core'),
                'search_items'       => __('Search Development Projects', 'ollmh-core'),
                'not_found'          => __('No development projects found', 'ollmh-core'),
                'not_found_in_trash' => __('No development projects in trash', 'ollmh-core'),
                'all_items'          => __('All Development Projects', 'ollmh-core'),
                'menu_name'          => __('Development Projects', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'projects/development', 'with_front' => false],
            'menu_position'       => 14,
            'menu_icon'           => 'dashicons-hammer',
            'supports'            => ['title', 'editor', 'excerpt', 'thumbnail'],
            'capability_type'     => 'project',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 11. Sustainability Project ────────────────────────────────
    private static function register_sustainability_project(): void {
        register_post_type('sustainability_project', [
            'labels' => [
                'name'               => __('Sustainability Projects', 'ollmh-core'),
                'singular_name'      => __('Sustainability Project', 'ollmh-core'),
                'add_new'            => __('Add New Project', 'ollmh-core'),
                'add_new_item'       => __('Add New Sustainability Project', 'ollmh-core'),
                'edit_item'          => __('Edit Sustainability Project', 'ollmh-core'),
                'new_item'           => __('New Sustainability Project', 'ollmh-core'),
                'view_item'          => __('View Sustainability Project', 'ollmh-core'),
                'search_items'       => __('Search Sustainability Projects', 'ollmh-core'),
                'not_found'          => __('No sustainability projects found', 'ollmh-core'),
                'not_found_in_trash' => __('No sustainability projects in trash', 'ollmh-core'),
                'all_items'          => __('All Sustainability Projects', 'ollmh-core'),
                'menu_name'          => __('Sustainability Projects', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'projects/sustainability', 'with_front' => false],
            'menu_position'       => 15,
            'menu_icon'           => 'dashicons-palmtree',
            'supports'            => ['title', 'editor', 'excerpt', 'thumbnail'],
            'capability_type'     => 'project',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 12. Upcoming Project ──────────────────────────────────────
    private static function register_upcoming_project(): void {
        register_post_type('upcoming_project', [
            'labels' => [
                'name'               => __('Upcoming Projects', 'ollmh-core'),
                'singular_name'      => __('Upcoming Project', 'ollmh-core'),
                'add_new'            => __('Add New Project', 'ollmh-core'),
                'add_new_item'       => __('Add New Upcoming Project', 'ollmh-core'),
                'edit_item'          => __('Edit Upcoming Project', 'ollmh-core'),
                'new_item'           => __('New Upcoming Project', 'ollmh-core'),
                'view_item'          => __('View Upcoming Project', 'ollmh-core'),
                'search_items'       => __('Search Upcoming Projects', 'ollmh-core'),
                'not_found'          => __('No upcoming projects found', 'ollmh-core'),
                'not_found_in_trash' => __('No upcoming projects in trash', 'ollmh-core'),
                'all_items'          => __('All Upcoming Projects', 'ollmh-core'),
                'menu_name'          => __('Upcoming Projects', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'projects/upcoming', 'with_front' => false],
            'menu_position'       => 16,
            'menu_icon'           => 'dashicons-lightbulb',
            'supports'            => ['title', 'editor', 'excerpt', 'thumbnail'],
            'capability_type'     => 'project',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 13. Community Program ─────────────────────────────────────
    private static function register_community_program(): void {
        register_post_type('community_program', [
            'labels' => [
                'name'               => __('Community Programs', 'ollmh-core'),
                'singular_name'      => __('Community Program', 'ollmh-core'),
                'add_new'            => __('Add New Program', 'ollmh-core'),
                'add_new_item'       => __('Add New Community Program', 'ollmh-core'),
                'edit_item'          => __('Edit Community Program', 'ollmh-core'),
                'new_item'           => __('New Community Program', 'ollmh-core'),
                'view_item'          => __('View Community Program', 'ollmh-core'),
                'search_items'       => __('Search Community Programs', 'ollmh-core'),
                'not_found'          => __('No community programs found', 'ollmh-core'),
                'not_found_in_trash' => __('No community programs in trash', 'ollmh-core'),
                'all_items'          => __('All Community Programs', 'ollmh-core'),
                'menu_name'          => __('Community', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'community/programs', 'with_front' => false],
            'menu_position'       => 17,
            'menu_icon'           => 'dashicons-heart',
            'supports'            => ['title', 'editor', 'excerpt', 'thumbnail'],
            'capability_type'     => 'community_program',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 14. SMI Event ─────────────────────────────────────────────
    private static function register_smi_event(): void {
        register_post_type('smi_event', [
            'labels' => [
                'name'               => __('SMI Events', 'ollmh-core'),
                'singular_name'      => __('SMI Event', 'ollmh-core'),
                'add_new'            => __('Add New SMI Event', 'ollmh-core'),
                'add_new_item'       => __('Add New SMI Event', 'ollmh-core'),
                'edit_item'          => __('Edit SMI Event', 'ollmh-core'),
                'new_item'           => __('New SMI Event', 'ollmh-core'),
                'view_item'          => __('View SMI Event', 'ollmh-core'),
                'search_items'       => __('Search SMI Events', 'ollmh-core'),
                'not_found'          => __('No SMI events found', 'ollmh-core'),
                'not_found_in_trash' => __('No SMI events in trash', 'ollmh-core'),
                'all_items'          => __('All SMI Events', 'ollmh-core'),
                'menu_name'          => __('SMI Events', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'community/smi-events', 'with_front' => false],
            'menu_position'       => 18,
            'menu_icon'           => 'dashicons-calendar-alt',
            'supports'            => ['title', 'editor', 'excerpt', 'thumbnail'],
            'capability_type'     => 'smi_event',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ── 15. Outlook Album (Gallery) ───────────────────────────────
    private static function register_outlook_album(): void {
        register_post_type('outlook_album', [
            'labels' => [
                'name'               => __('Gallery Albums', 'ollmh-core'),
                'singular_name'      => __('Gallery Album', 'ollmh-core'),
                'add_new'            => __('Add New Album', 'ollmh-core'),
                'add_new_item'       => __('Add New Gallery Album', 'ollmh-core'),
                'edit_item'          => __('Edit Gallery Album', 'ollmh-core'),
                'new_item'           => __('New Gallery Album', 'ollmh-core'),
                'view_item'          => __('View Gallery Album', 'ollmh-core'),
                'search_items'       => __('Search Gallery Albums', 'ollmh-core'),
                'not_found'          => __('No gallery albums found', 'ollmh-core'),
                'not_found_in_trash' => __('No gallery albums in trash', 'ollmh-core'),
                'all_items'          => __('All Gallery Albums', 'ollmh-core'),
                'menu_name'          => __('Gallery', 'ollmh-core'),
            ],
            'public'              => true,
            'has_archive'         => true,
            'rewrite'             => ['slug' => 'gallery', 'with_front' => false],
            'menu_position'       => 19,
            'menu_icon'           => 'dashicons-camera',
            'supports'            => ['title', 'editor', 'thumbnail'],
            'capability_type'     => 'gallery',
            'map_meta_cap'        => true,
            'show_in_rest'        => true,
        ]);
    }

    // ──────────────────────────────────────────────────────────────
    //  CUSTOM TAXONOMIES
    // ──────────────────────────────────────────────────────────────

    public static function register_taxonomies(): void {
        self::register_news_category();
        self::register_news_tag();
        self::register_event_category();
        self::register_staff_cadre();
    }

    // ── News Category ─────────────────────────────────────────────
    private static function register_news_category(): void {
        register_taxonomy('news_category', ['news_article'], [
            'labels' => [
                'name'              => __('News Categories', 'ollmh-core'),
                'singular_name'     => __('News Category', 'ollmh-core'),
                'search_items'      => __('Search News Categories', 'ollmh-core'),
                'all_items'         => __('All News Categories', 'ollmh-core'),
                'edit_item'         => __('Edit News Category', 'ollmh-core'),
                'update_item'       => __('Update News Category', 'ollmh-core'),
                'add_new_item'      => __('Add New News Category', 'ollmh-core'),
                'new_item_name'     => __('New News Category Name', 'ollmh-core'),
                'menu_name'         => __('Categories', 'ollmh-core'),
            ],
            'hierarchical'        => true,
            'show_admin_column'   => true,
            'rewrite'             => ['slug' => 'news/category', 'with_front' => false],
            'show_in_rest'        => true,
            'capabilities' => [
                'manage_terms' => 'manage_categories',
                'edit_terms'   => 'manage_categories',
                'delete_terms' => 'manage_categories',
                'assign_terms' => 'edit_posts',
            ],
        ]);
    }

    // ── News Tag ──────────────────────────────────────────────────
    private static function register_news_tag(): void {
        register_taxonomy('news_tag', ['news_article'], [
            'labels' => [
                'name'              => __('News Tags', 'ollmh-core'),
                'singular_name'     => __('News Tag', 'ollmh-core'),
                'search_items'      => __('Search News Tags', 'ollmh-core'),
                'all_items'         => __('All News Tags', 'ollmh-core'),
                'edit_item'         => __('Edit News Tag', 'ollmh-core'),
                'update_item'       => __('Update News Tag', 'ollmh-core'),
                'add_new_item'      => __('Add New News Tag', 'ollmh-core'),
                'new_item_name'     => __('New News Tag Name', 'ollmh-core'),
                'menu_name'         => __('Tags', 'ollmh-core'),
            ],
            'hierarchical'        => false,
            'show_admin_column'   => true,
            'rewrite'             => ['slug' => 'news/tag', 'with_front' => false],
            'show_in_rest'        => true,
            'capabilities' => [
                'manage_terms' => 'manage_categories',
                'edit_terms'   => 'manage_categories',
                'delete_terms' => 'manage_categories',
                'assign_terms' => 'edit_posts',
            ],
        ]);
    }

    // ── Event Category ────────────────────────────────────────────
    private static function register_event_category(): void {
        register_taxonomy('event_category', ['event'], [
            'labels' => [
                'name'              => __('Event Categories', 'ollmh-core'),
                'singular_name'     => __('Event Category', 'ollmh-core'),
                'search_items'      => __('Search Event Categories', 'ollmh-core'),
                'all_items'         => __('All Event Categories', 'ollmh-core'),
                'edit_item'         => __('Edit Event Category', 'ollmh-core'),
                'update_item'       => __('Update Event Category', 'ollmh-core'),
                'add_new_item'      => __('Add New Event Category', 'ollmh-core'),
                'new_item_name'     => __('New Event Category Name', 'ollmh-core'),
                'menu_name'         => __('Categories', 'ollmh-core'),
            ],
            'hierarchical'        => true,
            'show_admin_column'   => true,
            'rewrite'             => ['slug' => 'events/category', 'with_front' => false],
            'show_in_rest'        => true,
            'capabilities' => [
                'manage_terms' => 'manage_categories',
                'edit_terms'   => 'manage_categories',
                'delete_terms' => 'manage_categories',
                'assign_terms' => 'edit_posts',
            ],
        ]);
    }

    // ── Staff Cadre ───────────────────────────────────────────────
    private static function register_staff_cadre(): void {
        register_taxonomy('staff_cadre', ['staff_member'], [
            'labels' => [
                'name'              => __('Staff Cadres', 'ollmh-core'),
                'singular_name'     => __('Staff Cadre', 'ollmh-core'),
                'search_items'      => __('Search Staff Cadres', 'ollmh-core'),
                'all_items'         => __('All Staff Cadres', 'ollmh-core'),
                'edit_item'         => __('Edit Staff Cadre', 'ollmh-core'),
                'update_item'       => __('Update Staff Cadre', 'ollmh-core'),
                'add_new_item'      => __('Add New Staff Cadre', 'ollmh-core'),
                'new_item_name'     => __('New Staff Cadre Name', 'ollmh-core'),
                'menu_name'         => __('Cadres', 'ollmh-core'),
            ],
            'hierarchical'        => false,
            'show_admin_column'   => true,
            'rewrite'             => ['slug' => 'staff/cadre', 'with_front' => false],
            'show_in_rest'        => true,
            'capabilities' => [
                'manage_terms' => 'edit_staff',
                'edit_terms'   => 'edit_staff',
                'delete_terms' => 'edit_staff',
                'assign_terms' => 'edit_staff',
            ],
        ]);
    }

    // ──────────────────────────────────────────────────────────────
    //  PAGE TEMPLATES (registered via theme, not plugin — this is a
    //  reference hook for the theme to filter)
    // ──────────────────────────────────────────────────────────────
    public static function register_page_templates(array $templates): array {
        // The theme registers its own page templates; this method exists
        // for potential plugin-injected templates in the future.
        return $templates;
    }
}
```

---

## 2. CPT summary table

| CPT slug | Singular | Archive slug | Icon | Capabilities |
|---|---|---|---|---|
| `news_article` | News Article | `/news/` | `dashicons-admin-post` | `news_article` |
| `event` | Event | `/events/` | `dashicons-calendar` | `event` |
| `department` | Department | `/departments/` | `dashicons-building` | `department` |
| `ward` | Ward | — | `dashicons-bed` | `ward` |
| `clinic` | Clinic | — | `dashicons-clock` | `clinic` |
| `special_service` | Special Service | — | `dashicons-shield-alt` | `special_service` |
| `staff_member` | Staff Member | `/staff/` | `dashicons-groups` | `staff` |
| `job_vacancy` | Job Vacancy | `/careers/` | `dashicons-businessperson` | `job_vacancy` |
| `nursing_programme` | Nursing Programme | — | `dashicons-welcome-learn-more` | `nursing_programme` |
| `development_project` | Development Project | `/projects/development/` | `dashicons-hammer` | `project` |
| `sustainability_project` | Sustainability Project | `/projects/sustainability/` | `dashicons-palmtree` | `project` |
| `upcoming_project` | Upcoming Project | `/projects/upcoming/` | `dashicons-lightbulb` | `project` |
| `community_program` | Community Program | `/community/programs/` | `dashicons-heart` | `community_program` |
| `smi_event` | SMI Event | `/community/smi-events/` | `dashicons-calendar-alt` | `smi_event` |
| `outlook_album` | Gallery Album | `/gallery/` | `dashicons-camera` | `gallery` |

## 3. Taxonomy summary table

| Taxonomy slug | Attached to | Hierarchical | Rewrite slug |
|---|---|---|---|
| `news_category` | `news_article` | Yes | `/news/category/` |
| `news_tag` | `news_article` | No | `/news/tag/` |
| `event_category` | `event` | Yes | `/events/category/` |
| `staff_cadre` | `staff_member` | No | `/staff/cadre/` |

---

## 4. `map_meta_cap` and capability mapping

Each CPT uses `'capability_type' => '<cpt_slug>'` and
`'map_meta_cap' => true`. This tells WordPress to generate the standard
capability set (`edit_<cpt>`, `edit_others_<cpt>`, `publish_<cpt>`,
`delete_<cpt>`, `delete_others_<cpt>`, `edit_published_<cpt>`,
`delete_published_<cpt>`, `read_private_<cpt>`).

These capabilities are then added to the Editor and Author roles via
`add_cap()` — see [`USER-ROLES.md`](./USER-ROLES.md) → "CPT capability
additions to core roles" for the complete `add_cap()` code.
