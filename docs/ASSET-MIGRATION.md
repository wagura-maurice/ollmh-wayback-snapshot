# Asset Migration

> This document details how to migrate all images, PDFs, and documents
> from the archived Joomla site into the WordPress media library.
>
> **Related:** [`MIGRATION-PLAN.md`](./MIGRATION-PLAN.md) for the overall
> plan, [`CONTENT-MIGRATION.md`](./CONTENT-MIGRATION.md) for content.

---

## 1. Asset inventory

Based on the audit of the archived site:

| Type | Count | Location | Status |
|---|---|---|---|
| JPG/JPEG | ~93 (30 lowercase + 63 uppercase) | `images/`, `images/ollmh/` | Need migration |
| PNG | ~30 | `images/`, `templates/tx_finnix/images/` | Need migration (content images only) |
| GIF | ~9 | `images/`, `images/ollmh/` | Need migration (convert to PNG/WebP) |
| ICO | 1 | `templates/tx_finnix/favicon.ico` | Replace with modern favicon |
| PDF | 0 archived (3 referenced) | Not in archive | Source from hospital |
| Video/Audio | 0 | — | None to migrate |

**Total: ~133 image files to migrate.**

### Directory structure in archive

```
images/
├── DrChir.jpg, history.jpg, banner.gif, ...     # Root-level images
└── ollmh/
    ├── Aministration/          (6 files)         # Administration photos
    ├── CommunityProject/       (7 files)         # Community project photos
    ├── News_projects/          (2 files)         # News project photos
    ├── Nursing_sch/            (2 files)         # Nursing school photos
    ├── S.M.IMwea/              (5 files)         # SMI community photos
    ├── Sustainability_Projects/(7 files)         # Sustainability project photos
    ├── animated/               (3 files)         # Animated GIFs
    ├── attachment/             (1 file)          # Attachment
    ├── developmentsnachievments/(3 files)        # Development photos
    ├── hospitalUnits/          (22 files)        # Hospital unit photos (ICU, wards, etc.)
    ├── misc_Select/            (6 files)         # Miscellaneous
    ├── news_events/            (5 files)         # News event photos
    ├── Inpatient.jpg, outp2.jpg                   # Department photos
    └── slideshow/              (N files)         # Homepage slideshow images
```

### Naming issues found

- **Mixed case extensions:** `.jpg` and `.JPG` — standardize to lowercase
- **URL-encoded filenames:** `A%20TEAM%20OF%20LOCAL%20ADMINISTRATION...JPG` — decode and rename
- **Camera-generated names:** `DSC07763.JPG`, `DSCF7488.JPG` — rename to descriptive names
- **Spaces in filenames:** `FAITH KARIUKI IN MATERNITY WARD...gif` — replace with hyphens
- **Empty alt text:** Most images have `alt=""` — need manual alt text

### Referenced-but-missing PDFs

These PDFs are linked in the HTML but were not captured by the Wayback Machine:
1. `Application form for OLLMMTC updated.pdf`
2. `Application form for OLLMMTC 2021.pdf.pdf`
3. `Nursing_school_Application.pdf`

**Action:** Source these from the hospital administration. If unavailable, create new application form PDFs.

---

## 2. Migration script

> **Dev-only:** This script runs via WP-CLI in the development
> environment only. WP-CLI is not available on production (cPanel shared
> hosting) — see [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md)
> → ADR-005. After running the migration in dev, media assets are deployed
> to production by uploading the `wp-content/uploads/` directory via
> cPanel File Manager (or FTP), and importing the database via phpMyAdmin.

Create a PHP script at `scripts/migrate-assets.php` that runs via WP-CLI:

```php
<?php
/**
 * Asset Migration Script — OLLMH
 * Run via: wp eval-file scripts/migrate-assets.php
 *
 * Scans the archived images directory, cleans filenames, uploads each
 * image to the WordPress media library, and records the old→new URL
 * mapping for the content migration script.
 */

$archive_images_dir = dirname(__DIR__) . '/web.archive.org/web/20220319205345im_/http:/ourladyoflourdesmweahospital.org/images/';
$mapping_file = dirname(__DIR__) . '/scripts/asset-url-mapping.json';

// Collect all image files
$images = [];
$iterator = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($archive_images_dir, RecursiveDirectoryIterator::SKIP_DOTS)
);
foreach ($iterator as $file) {
    $ext = strtolower($file->getExtension());
    if (in_array($ext, ['jpg', 'jpeg', 'png', 'gif'])) {
        $images[] = $file->getPathname();
    }
}

WP_CLI::log("Found " . count($images) . " images to migrate.");

$mapping = [];
$migrated = 0;
$skipped = 0;

foreach ($images as $image_path) {
    // Clean the filename
    $original_name = basename($image_path);
    $clean_name = clean_filename($original_name);

    // Check if already migrated (by clean name in postmeta)
    $existing = find_attachment_by_filename($clean_name);
    if ($existing) {
        WP_CLI::log("  Skipping (already exists): {$clean_name}");
        $mapping[$original_name] = wp_get_attachment_url($existing->ID);
        $skipped++;
        continue;
    }

    // Copy to temp directory with clean name
    $temp_dir = sys_get_temp_dir() . '/ollmh-migration/';
    if (!is_dir($temp_dir)) {
        mkdir($temp_dir, 0755, true);
    }
    $temp_path = $temp_dir . $clean_name;
    copy($image_path, $temp_path);

    // Import into WordPress media library
    require_once ABSPATH . 'wp-admin/includes/image.php';
    require_once ABSPATH . 'wp-admin/includes/file.php';
    require_once ABSPATH . 'wp-admin/includes/media.php';

    $attachment_id = media_handle_sideload(
        ['name' => $clean_name, 'tmp_name' => $temp_path],
        0,  // No parent post
        '', // No description
        ['post_title' => generate_title_from_filename($clean_name)]
    );

    if (is_wp_error($attachment_id)) {
        WP_CLI::warning("  Failed to migrate: {$original_name} — " . $attachment_id->get_error_message());
        continue;
    }

    // Generate alt text placeholder (to be filled manually)
    update_post_meta($attachment_id, '_wp_attachment_image_alt', '');

    // Record mapping
    $mapping[$original_name] = wp_get_attachment_url($attachment_id);
    WP_CLI::log("  Migrated: {$original_name} → {$clean_name} (ID: {$attachment_id})");
    $migrated++;
}

// Save mapping for content migration script
file_put_contents($mapping_file, json_encode($mapping, JSON_PRETTY_PRINT));

WP_CLI::success("Asset migration complete. Migrated: {$migrated}, Skipped: {$skipped}");
WP_CLI::log("URL mapping saved to: {$mapping_file}");

// ── Helper functions ────────────────────────────────────────────

function clean_filename(string $filename): string {
    // URL-decode
    $name = urldecode($filename);
    // Lowercase extension
    $info = pathinfo($name);
    $ext = strtolower($info['extension']);
    // Replace spaces with hyphens
    $base = preg_replace('/\s+/', '-', $info['filename']);
    // Remove special characters
    $base = preg_replace('/[^a-zA-Z0-9\-_]/', '', $base);
    // Collapse multiple hyphens
    $base = preg_replace('/-+/', '-', $base);
    // Lowercase
    $base = strtolower($base);
    // Limit length
    if (strlen($base) > 60) {
        $base = substr($base, 0, 60);
    }
    return $base . '.' . $ext;
}

function generate_title_from_filename(string $filename): string {
    $base = pathinfo($filename, PATHINFO_FILENAME);
    return ucwords(str_replace(['-', '_'], ' ', $base));
}

function find_attachment_by_filename(string $filename): ?WP_Post {
    global $wpdb;
    $id = $wpdb->get_var($wpdb->prepare(
        "SELECT post_id FROM {$wpdb->prefix}postmeta
         WHERE meta_key = '_wp_attached_file'
         AND meta_value LIKE %s LIMIT 1",
        '%' . $filename
    ));
    return $id ? get_post($id) : null;
}
```

---

## 3. Post-migration tasks

### Alt text assignment

All migrated images have empty alt text. Assign alt text by:

1. **Bulk assignment for obvious images:** Staff photos → "Portrait of [Name]",
   department photos → "[Department Name] at OLLMH"
2. **Context-based assignment:** For images embedded in pages, read the
   surrounding text to infer what the image shows
3. **Manual review:** Go through the Media Library and add descriptive alt
   text to each image

### Image optimization

After migration, optimize all images:

1. Install **ShortPixel** or **Imagify** plugin (or use W3 Total Cache's lazy load + a free image optimizer like **Converter for Media** for WebP conversion)
2. Bulk-optimize all images in the media library
3. Convert to **WebP** format (smaller file size, supported by all modern browsers)
4. Generate responsive `srcset` sizes (WordPress does this automatically for
   images inserted via the editor, but verify)

### Logo and favicon

| Asset | Source | Action |
|---|---|---|
| Logo | `templates/tx_finnix/images/style1/logo.png` (222×96px) | Re-export at 2x resolution (444×192px) for retina displays. Upload as the theme logo. |
| Favicon | `templates/tx_finnix/favicon.ico` | Generate modern favicon set (16×16, 32×32, 180×180 apple-touch-icon, 192×192, 512×512) using a favicon generator. Upload to theme root. |
| Apple touch icon | `templates/tx_finnix/images/apple_touch_icon.png` | Replace with 180×180px version |

### Template/system images

These images are part of the Joomla template, not content. They are **not
migrated** to the media library — the WordPress theme will use its own
CSS-based equivalents:

- `templates/tx_finnix/images/style1/bg.jpg` → CSS background or remove
- `templates/tx_finnix/images/style1/social_icons.png` → SVG icons (see [`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md))
- `templates/tx_finnix/images/style1/menu_hover_arrow.png` → CSS arrow
- `templates/tx_finnix/images/typography/*` → CSS (no images needed)

---

## 4. GIF handling

9 GIF files were found in the archive. Some are animated graphics (e.g.,
`graphics-nursing-315195.gif`, `graphics-welcome-731955.gif`). For each:

| GIF type | Action |
|---|---|
| Animated GIF (decorative) | Convert to MP4/WebM for smaller file size, or replace with CSS animation |
| Static GIF (photo) | Convert to PNG or WebP |
| Animated GIF (content) | Keep as GIF if the animation is meaningful, otherwise convert |

---

## 5. URL mapping file

The migration script generates `scripts/asset-url-mapping.json` — a JSON
file mapping old filenames to new WordPress media URLs. This file is used
by the content migration script (see [`CONTENT-MIGRATION.md`](./CONTENT-MIGRATION.md))
to replace image `src` attributes in the HTML content.

Example mapping:
```json
{
  "DrChir.jpg": "https://newsite.com/wp-content/uploads/2024/01/drchir.jpg",
  "ICU.JPG": "https://newsite.com/wp-content/uploads/2024/01/icu.jpg",
  "A%20TEAM%20OF%20LOCAL%20ADMINISTRATION...JPG": "https://newsite.com/wp-content/uploads/2024/01/a-team-of-local-administration.jpg"
}
```
