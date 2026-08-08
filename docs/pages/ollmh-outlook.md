# Ollmh Outlook (`/ollmh-outlook.html`)

> A "Features" photo showcase giving a visual outlook of the hospital — its frontage, administration, care services, and Christian-based character.

## 1. Current State Mapping

- **Page title:** browser title "Ollmh Outlook"; in-body `h1.title` reads **"Ollmh Outlook"** (part of the "Features" menu group).
- **Structure:** a single `article-body` composed of caption paragraphs interleaved with rows of images — effectively a captioned photo gallery. No long-form prose.
- **Row 1 captions:** "OLLMH Front Face" · "Hosp Administrator" · "Ollmh Direction to Departments" with three images:
  - `GA_PRGlobalFutures503.jpg` (336×189) — front face.
  - `ollmh/Aministration/DSC00488.JPG` (224×190) — hospital administrator.
  - `ollmh/hospitalUnits/Mwea MH.jpg` (255×191) — directions to departments.
- **Row 2 captions:** "Health Care Services" · "OLLMH Resting Shade" · "Ollmh as Christian Based Organisation" with three images:
  - `ollmh/hospitalUnits/maternity/DSCF7519.JPG` (194×160) — health care services.
  - `ollmh/hospitalUnits/more_photos/DSC00460.JPG` (266×161) — resting shade.
  - `history.jpg` (276×155) — Christian-based organisation.
- **Images have no `alt` text** in the source; captions are plain paragraphs positioned above the image rows.
- **Interactive elements:** only the shared template Print/Email actions, Prev/Next article pager, header megamenu, and footer columns. No page-specific interactivity.
- **Note:** injected Russian spam anchors (`printer-spb.ru`) appear in the archived markup; these are template compromise artifacts, not real content.

## 2. Gap Analysis & Feature Enhancements

**Content & structure**
- Give each photo a proper **title + descriptive caption** (currently captions are loose paragraphs decoupled from the images) and meaningful `alt` text.
- Add short introductory copy explaining what "OLLMH Outlook" is (an at-a-glance visual tour), rather than an unlabelled image grid.
- Group photos into named albums (Frontage, Administration, Care Services, Environment/Grounds, Mission & Faith).

**UX/UI**
- Replace fixed-pixel `<img>` rows with a responsive **masonry gallery + lightbox** (zoom, next/prev, captions).
- Add thumbnails with lazy loading and consistent aspect ratios.

**Accessibility & SEO**
- Descriptive `alt` text and figure/figcaption semantics for each image.
- Page meta description and `ImageGallery`/`Photograph` schema.org markup.

**Interactivity & integrations**
- Optional 360°/virtual tour or embedded map of the campus.
- Social share buttons and download-image option where appropriate.

## 3. Database Schema Design

```sql
-- Captioned gallery items for the "Ollmh Outlook" visual showcase
CREATE TABLE wp_outlook_gallery_items (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  album_id      BIGINT UNSIGNED NULL,
  media_id      BIGINT UNSIGNED NOT NULL,
  caption       VARCHAR(255)    NULL,       -- e.g. "OLLMH Front Face"
  description   TEXT            NULL,
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  KEY idx_outlook_page (page_id, sort_order),
  CONSTRAINT fk_outlook_page  FOREIGN KEY (page_id)  REFERENCES wp_pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_outlook_album FOREIGN KEY (album_id) REFERENCES wp_outlook_albums (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_outlook_media FOREIGN KEY (media_id) REFERENCES wp_media_assets (id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Optional grouping of gallery items into named albums
CREATE TABLE wp_outlook_albums (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  name          VARCHAR(191)    NOT NULL,   -- e.g. "Frontage", "Administration"
  slug          VARCHAR(191)    NOT NULL,
  description   TEXT            NULL,
  cover_media_id BIGINT UNSIGNED NULL,
  sort_order    INT UNSIGNED    NOT NULL DEFAULT 0,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'published',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_outlook_album_slug (slug),
  KEY idx_outlook_album_page (page_id, sort_order),
  CONSTRAINT fk_outlook_album_page  FOREIGN KEY (page_id)       REFERENCES wp_pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_outlook_album_cover FOREIGN KEY (cover_media_id) REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

> Note: create `wp_outlook_albums` before `wp_outlook_gallery_items` (or add the FK afterwards) since the item table references it.

**Relationships**
- Both tables carry `page_id → wp_pages.id` so the gallery belongs to the "Ollmh Outlook" feature page and cascade-deletes with it.
- `wp_outlook_gallery_items.media_id` and `wp_outlook_albums.cover_media_id` reference the shared **`wp_media_assets`** library, so imagery is centrally managed (with alt text, dimensions, captions) rather than hardcoded.
- `wp_outlook_gallery_items.album_id → wp_outlook_albums.id` provides optional album grouping while keeping a flat, orderable gallery by default.
