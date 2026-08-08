# Content Migration

> This document details how to extract content from the archived Joomla
> HTML pages and insert it into the WordPress database — pages, CPTs, and
> custom tables.
>
> **Related:** [`MIGRATION-PLAN.md`](./MIGRATION-PLAN.md) for the overall
> plan, [`ASSET-MIGRATION.md`](./ASSET-MIGRATION.md) for image handling,
> [`URL-MAPPING.md`](./URL-MAPPING.md) for URL redirects.

---

## 1. Source archive structure

The archived site is at `web.archive.org/web/20220319205345im_/http:/ourladyoflourdesmweahospital.org/`.

**20 HTML pages** (17 fully archived, 3 placeholder):

| # | Archived file | WP slug | WP type | Status |
|---|---|---|---|---|
| 1 | `index.html` | `/` (home) | Page (front-page.php) | ✅ Full |
| 2 | `about-ollmh-location.html` | `/about-ollmh-location` | Page | ✅ Full |
| 3 | `administration.html` | `/administration` | Page | ✅ Full |
| 4 | `philosophy-of-care.html` | `/philosophy-of-care` | Page | ✅ Full |
| 5 | `hr-capacity-staff.html` | `/hr-capacity-staff` | Page | ✅ Full |
| 6 | `development-projects.html` | `/development-projects` | Page → CPT archive | ✅ Full |
| 7 | `self-sustainability-projects.html` | `/self-sustainability-projects` | Page → CPT archive | ✅ Full |
| 8 | `community-support.html` | `/community-support` | Page → CPT archive | ✅ Full |
| 9 | `upcoming-projects.html` | `/upcoming-projects` | Page → CPT archive | ✅ Full |
| 10 | `in-patient-dept.html` | `/in-patient-dept` | Page | ❌ Placeholder |
| 11 | `out-patient-dept.html` | `/out-patient-dept` | Page | ✅ Full |
| 12 | `wards.html` | `/wards` | Page | ✅ Full |
| 13 | `special-medical-services.html` | `/special-medical-services` | Page | ✅ Full |
| 14 | `clinic-days.html` | `/clinic-days` | Page | ❌ Placeholder |
| 15 | `ollmh-outlook.html` | `/ollmh-outlook` | Page → CPT archive | ✅ Full |
| 16 | `ollmh-departments.html` | `/ollmh-departments` | Page → CPT archive | ✅ Full |
| 17 | `smi-community.html` | `/smi-community` | Page → CPT archive | ✅ Full |
| 18 | `contacts.html` | `/contacts` | Page | ✅ Full |
| 19 | `news-events.html` | `/news-events` | Page → CPT archive | ✅ Full |
| 20 | `medical-school-application-form.html` | `/medical-school-application-form` | Page | ✅ Full |
| — | `about-nursing-school.html` | `/about-nursing-school` | Page | ❌ Placeholder |

---

## 2. Content extraction strategy

Each archived HTML page has this structure (Joomla TX Finnix template):

```html
<html>
<head>...</head>
<body>
  <div id="roof">...</div>          <!-- top bar (search, social) -->
  <div id="header">...</div>        <!-- logo + main menu -->
  <div id="main">                    <!-- main content area -->
    <div id="mainbody">              <!-- content column -->
      <!-- PAGE-SPECIFIC CONTENT HERE -->
    </div>
    <div id="sidebar-a">...</div>   <!-- sidebar -->
    <div id="sidebar-b">...</div>   <!-- sidebar -->
  </div>
  <div id="footer">...</div>         <!-- footer -->
</body>
</html>
```

**Extraction target:** The content inside `<div id="mainbody">` (or the
equivalent component container). Everything else (header, footer, sidebars,
menu) is template chrome that the WordPress theme will render from
`header.php` and `footer.php`.

---

## 3. HTML cleaning rules

After extracting the raw HTML from `#mainbody`, apply these cleaning rules
before inserting into WordPress:

### Remove
- `border="0"` attributes on `<img>` tags (deprecated)
- `align="left"`, `align="right"` attributes (use CSS classes instead)
- `hspace="..."`, `vspace="..."` attributes (deprecated)
- `<font>` tags (deprecated — use CSS)
- Inline `style="..."` attributes (move to theme CSS)
- Joomla-specific CSS classes: `item-page`, `item-fulltext`, `readmore`, `article-info`, `article-info-term`
- Joomla admin links (`administrator/index.php?option=...`)
- Joomla search form (`mod-finder-searchform`)
- Wayback Machine injected elements (`#wm-ipp`, `.wayback_*`)

### Convert
- `<table>` layouts → CSS grid/flexbox
- `<img src="20220319205345im_/http:/ourladyoflourdesmweahospital.org/images/...">` → `<img src="https://newsite.com/wp-content/uploads/...">` (WordPress media URL)
- Internal links `about-ollmh-location.html` → `/about-ollmh-location/` (WordPress permalink)
- `<h1>` inside content → `<h2>` (the page title is the `<h1>`)
- `<p>&nbsp;</p>` empty paragraphs → remove
- `<br><br><br>` multiple breaks → single `<p>` paragraph break

### Preserve
- Text content (obviously)
- Heading hierarchy (`<h2>` through `<h6>`)
- Lists (`<ul>`, `<ol>`)
- Tables with actual tabular data (ward bed status, clinic schedules)
- Image references (after URL conversion)
- Internal links (after URL conversion)

---

## 4. Migration script

Create a PHP script at `scripts/migrate-content.php` that runs via WP-CLI:

```php
<?php
/**
 * Content Migration Script — OLLMH
 * Run via: wp eval-file scripts/migrate-content.php
 *
 * Extracts content from archived HTML files and inserts into WordPress.
 */

// Configuration
$archive_base = dirname(__DIR__) . '/web.archive.org/web/20220319205345im_/http:/ourladyoflourdesmweahospital.org/';

// Page mapping: archived_file => [wp_slug, wp_type, page_template]
$page_map = [
    'index.html'                        => ['/', 'page', 'front-page.php'],
    'about-ollmh-location.html'         => ['about-ollmh-location', 'page', 'page-about.php'],
    'administration.html'               => ['administration', 'page', 'page-administration.php'],
    'philosophy-of-care.html'           => ['philosophy-of-care', 'page', 'page-philosophy.php'],
    'hr-capacity-staff.html'            => ['hr-capacity-staff', 'page', 'page-hr-capacity.php'],
    'development-projects.html'         => ['development-projects', 'page', 'page-projects.php'],
    'self-sustainability-projects.html' => ['self-sustainability-projects', 'page', 'page-projects.php'],
    'community-support.html'            => ['community-support', 'page', 'page-community.php'],
    'upcoming-projects.html'            => ['upcoming-projects', 'page', 'page-projects.php'],
    'out-patient-dept.html'             => ['out-patient-dept', 'page', 'page-opd.php'],
    'wards.html'                        => ['wards', 'page', 'page-wards.php'],
    'special-medical-services.html'     => ['special-medical-services', 'page', 'page-special-services.php'],
    'ollmh-outlook.html'                => ['ollmh-outlook', 'page', 'page-gallery.php'],
    'ollmh-departments.html'            => ['ollmh-departments', 'page', 'page-departments.php'],
    'smi-community.html'                => ['smi-community', 'page', 'page-community.php'],
    'contacts.html'                     => ['contacts', 'page', 'page-contacts.php'],
    'news-events.html'                  => ['news-events', 'page', 'page-news-events.php'],
    'medical-school-application-form.html' => ['medical-school-application-form', 'page', 'page-application-form.php'],
];

foreach ($page_map as $file => [$slug, $type, $template]) {
    $html_file = $archive_base . $file;
    if (!file_exists($html_file)) {
        WP_CLI::warning("File not found: {$file} — skipping");
        continue;
    }

    $raw_html = file_get_contents($html_file);
    $content = extract_mainbody($raw_html);
    $content = clean_html($content);
    $content = convert_image_urls($content);
    $content = convert_internal_links($content);
    $title = extract_page_title($raw_html);

    // Check if page already exists
    $existing = get_page_by_path($slug);
    if ($existing) {
        WP_CLI::log("Updating existing page: {$slug}");
        wp_update_post([
            'ID'           => $existing->ID,
            'post_content' => $content,
            'post_title'   => $title,
        ]);
    } else {
        WP_CLI::log("Creating new page: {$slug}");
        $post_id = wp_insert_post([
            'post_title'   => $title,
            'post_name'    => $slug,
            'post_content' => $content,
            'post_status'  => 'publish',
            'post_type'    => 'page',
        ]);
        if ($template !== 'front-page.php') {
            update_post_meta($post_id, '_wp_page_template', $template);
        }
    }
}

WP_CLI::success('Content migration complete.');

// ── Helper functions ────────────────────────────────────────────

function extract_mainbody(string $html): string {
    // Extract content from #mainbody or equivalent Joomla container
    if (preg_match('/<div id="mainbody"[^>]*>(.*?)<\/div>\s*<!--\s*end mainbody/s', $html, $m)) {
        return $m[1];
    }
    // Fallback: extract .item-page or .blog
    if (preg_match('/<div class="item-page[^"]*"[^>]*>(.*?)<\/div>\s*<!-- end/s', $html, $m)) {
        return $m[1];
    }
    // Final fallback: extract #component
    if (preg_match('/<div id="component"[^>]*>(.*?)<\/div>\s*<!--\s*end component/s', $html, $m)) {
        return $m[1];
    }
    return '';
}

function clean_html(string $html): string {
    // Remove deprecated attributes
    $html = preg_replace('/\s+border="0"/i', '', $html);
    $html = preg_replace('/\s+align="(left|right|center)"/i', '', $html);
    $html = preg_replace('/\s+hspace="\d+"/i', '', $html);
    $html = preg_replace('/\s+vspace="\d+"/i', '', $html);
    // Remove inline styles
    $html = preg_replace('/\s+style="[^"]*"/i', '', $html);
    // Remove <font> tags (keep content)
    $html = preg_replace('/<\/?font[^>]*>/i', '', $html);
    // Remove Joomla-specific classes
    $html = preg_replace('/\s+class="(item-page|item-fulltext|readmore|article-info[^"]*)"/i', '', $html);
    // Remove empty paragraphs
    $html = preg_replace('/<p>\s*(&nbsp;)?\s*<\/p>/i', '', $html);
    // Collapse multiple <br> into paragraph breaks
    $html = preg_replace('/(<br\s*\/?>\s*){2,}/i', '</p><p>', $html);
    // Remove Wayback Machine elements
    $html = preg_replace('/<!--\s*BEGIN WAYBACK TOOLBAR.*?END WAYBACK TOOLBAR-->/is', '', $html);
    return trim($html);
}

function convert_image_urls(string $html): string {
    // Convert Wayback Machine image URLs to WordPress media URLs
    // Pattern: 20220319205345im_/http:/ourladyoflourdesmweahospital.org/images/...
    $html = preg_replace_callback(
        '/src="[^"]*?\/images\/([^"]+)"/i',
        function ($m) {
            $filename = basename($m[1]);
            // Look up attachment by filename
            $attachment = page_by_attachment_filename($filename);
            if ($attachment) {
                return 'src="' . wp_get_attachment_url($attachment->ID) . '"';
            }
            return $m[0]; // Keep original if not found
        },
        $html
    );
    return $html;
}

function convert_internal_links(string $html): string {
    // Convert .html internal links to WordPress permalinks
    $html = preg_replace_callback(
        '/href="([^"]*?)\/([a-z0-9-]+)\.html"/i',
        function ($m) {
            $slug = $m[2];
            $page = get_page_by_path($slug);
            if ($page) {
                return 'href="' . get_permalink($page->ID) . '"';
            }
            return $m[0];
        },
        $html
    );
    return $html;
}

function extract_page_title(string $html): string {
    if (preg_match('/<title>(.*?)<\/title>/i', $html, $m)) {
        // Remove site name suffix if present
        $title = $m[1];
        $title = preg_replace('/\s*[-|]\s*.*$/', '', $title);
        return trim($title);
    }
    return '';
}

function page_by_attachment_filename(string $filename): ?WP_Post {
    global $wpdb;
    $attachment = $wpdb->get_var($wpdb->prepare(
        "SELECT post_id FROM {$wpdb->prefix}postmeta
         WHERE meta_key = '_wp_attached_file'
         AND meta_value LIKE %s
         LIMIT 1",
        '%' . $filename
    ));
    if ($attachment) {
        return get_post($attachment);
    }
    return null;
}
```

---

## 5. CPT-specific migration

After pages are migrated, extract structured content into CPTs:

### News articles → `news_article` CPT

The `news-events.html` page contains a listing of news items. Each news
item links to a full article page (or contains the full text inline).

For each news item:
- **Title:** From the `<h2>` or `<h3>` in the news listing
- **Content:** From the linked article page or the inline content
- **Excerpt:** First paragraph or the summary text from the listing
- **Date:** From the article's publication date (Joomla `article-info`)
- **Category:** From the Joomla category (map to `news_category` taxonomy)
- **Featured image:** From the article's lead image

### Departments → `department` CPT

From `ollmh-departments.html`:
- Each department is a section with a heading, description, and image
- Extract each as a separate `department` post
- Set the department category (clinical, administrative, support) via the `department_category` field in `wp_departments`

### Staff → `staff_member` CPT

From `hr-capacity-staff.html` and `administration.html`:
- Each staff member has a name, title/role, photo, and bio
- Extract each as a separate `staff_member` post
- Link to their department via `department_id` in `wp_staff`
- Set their cadre via the `staff_cadre` taxonomy

### Projects → `development_project` / `sustainability_project` / `upcoming_project` CPTs

From the respective project pages:
- Each project has a title, description, image(s), and status
- Extract each as a separate CPT post of the appropriate type

### Gallery → `outlook_album` CPT

From `ollmh-outlook.html`:
- Each gallery section becomes an album
- Images within each section are attached to the album post

---

## 6. Content that needs manual creation

The 3 placeholder pages have no archived content:

| Page | Source for content |
|---|---|
| `/in-patient-dept` | Extract from the homepage "Inpatient Department" tab content + ward information from `wards.html` |
| `/clinic-days` | Source clinic schedule data from the hospital administration (no archived content exists) |
| `/about-nursing-school` | Source from the hospital administration or the nursing school application form page |

---

## 7. Post-migration verification

After running the migration script:

1. Visit each page on the front-end and verify content renders correctly
2. Check that all images display (no broken images)
3. Check that all internal links work (no 404s)
4. Verify heading hierarchy is correct (one `<h1>` per page, then `<h2>` subheadings)
5. Run a broken link checker scan
6. Compare each migrated page side-by-side with the archived version to ensure no content was lost
7. Check mobile rendering of each page
