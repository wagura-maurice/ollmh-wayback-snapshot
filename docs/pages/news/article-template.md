# News Article Template (`/news/<slug>`)

> This is the **reusable template** for every standalone news article page on
> the site. Each article lives at `/news/<slug>` and is a row in the
> `news_articles` table. The feed/listing page is documented in
> [`index.md`](./index.md); the one migrated article from the archive is in
> [`nursing-school-promo.md`](./nursing-school-promo.md).
>
> Copy this file as the starting point for documenting a new article, then fill
> in the article-specific sections.

## 1. Current State Mapping

> _Describe the article's source content. For new (non-archived) articles, note
> that this is original content created for the rebuild._

- **Article title:** _(fill in)_
- **Slug:** _(fill in)_
- **Source:** _(archived page / original content / migrated from X)_
- **Body content:** _(summary of the article body)_
- **Images:** _(list with file, dimensions, caption, alt text)_
- **Interactive elements:** _(comments, social share, related articles, etc.)_

## 2. Gap Analysis & Feature Enhancements

**Content gaps**
- _(list content gaps for this article)_

**UX/UI**
- Article hero image, breadcrumb (`Home / News / <article>`), "Back to News" link.
- Image gallery for multi-image articles, with captions and `alt` text.
- Related-articles module and social-sharing buttons.
- Comments section (moderated).

**Functionality & integrations**
- Cross-links to related pages (departments, nursing school, application form).
- schema.org `NewsArticle` structured data.

**Accessibility & SEO**
- `alt` text on all images, canonical URL, per-article meta description,
  `NewsArticle` JSON-LD.

## 3. Page-Specific Metadata (Standalone Page)

| Field | Value |
| --- | --- |
| Route | `/news/<slug>` |
| Page type | `news` (row in `news_articles`) |
| Layout | `news-article` — hero + body + gallery + sidebar |
| Slug | _(fill in)_ |
| Category | _(fill in)_ |
| Publish date | _(fill in)_ |
| Author | _(fill in)_ |
| Canonical URL | `https://ollmh.example/news/<slug>` |
| Meta title | _(fill in)_ |
| Meta description | _(fill in)_ |
| schema.org type | `NewsArticle` |
| Hero image | _(fill in)_ |
| Featured | _(yes/no)_ |
| Sitemap priority | `0.6` |

## 4. Layout Structure (Standalone Page)

```
┌─────────────────────────────────────────────────────┐
│ Breadcrumb: Home / News / <article title>           │
├─────────────────────────────────────────────────────┤
│ Article hero image                                  │
├──────────────────────────────────┬──────────────────┤
│ Article body                      │ Sidebar          │
│  - Headline                       │ - Author card    │
│  - Meta (date, author, category)  │ - Related posts  │
│  - Lead paragraph                 │ - Categories     │
│  - Body paragraphs                │ - Tags           │
│  - Image gallery (if any)         │ - Newsletter     │
│  - CTA (if any)                   │ - Social share   │
│  - Comments section               │                  │
├──────────────────────────────────┴──────────────────┤
│ [← Previous article]        [Back to News]   [Next →]│
├─────────────────────────────────────────────────────┤
│ Footer (shared)                                     │
└─────────────────────────────────────────────────────┘
```

## 5. Database Schema Design

These tables back **every** standalone article page. They are defined once
here and referenced by all article docs.

```sql
-- News/announcement articles (one row per standalone article page)
CREATE TABLE news_articles (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,       -- the /news/ listing page
  category_id   BIGINT UNSIGNED NULL,
  author_id     BIGINT UNSIGNED NULL,           -- CMS user
  title         VARCHAR(255)    NOT NULL,
  slug          VARCHAR(191)    NOT NULL,
  excerpt       VARCHAR(512)    NULL,
  body          MEDIUMTEXT      NULL,
  hero_media_id BIGINT UNSIGNED NULL,
  is_featured   TINYINT(1)      NOT NULL DEFAULT 0,
  status        ENUM('draft','published','archived') NOT NULL DEFAULT 'draft',
  published_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_news_slug (slug),
  KEY idx_news_pub (status, published_at),
  CONSTRAINT fk_news_page   FOREIGN KEY (page_id)       REFERENCES pages (id)          ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_news_cat    FOREIGN KEY (category_id)   REFERENCES news_categories (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_news_author FOREIGN KEY (author_id)     REFERENCES users (id)          ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_news_hero   FOREIGN KEY (hero_media_id) REFERENCES media_assets (id)   ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Article ↔ tag join (many-to-many)
CREATE TABLE news_article_tags (
  article_id BIGINT UNSIGNED NOT NULL,
  tag_id     BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (article_id, tag_id),
  CONSTRAINT fk_nat_article FOREIGN KEY (article_id) REFERENCES news_articles (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_nat_tag     FOREIGN KEY (tag_id)     REFERENCES news_tags (id)     ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Ordered image gallery attached to an article (beyond the hero image)
CREATE TABLE news_article_media (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  article_id BIGINT UNSIGNED NOT NULL,
  media_id   BIGINT UNSIGNED NOT NULL,
  caption    VARCHAR(512)    NULL,
  sort_order INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_news_media (article_id, media_id),
  KEY idx_news_media (article_id, sort_order),
  CONSTRAINT fk_nam_article FOREIGN KEY (article_id) REFERENCES news_articles (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_nam_media   FOREIGN KEY (media_id)   REFERENCES media_assets (id)  ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Revision history for auditing article edits
CREATE TABLE news_article_revisions (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  article_id  BIGINT UNSIGNED NOT NULL,
  editor_id   BIGINT UNSIGNED NULL,       -- CMS user who made the edit
  title       VARCHAR(255)    NOT NULL,
  body        MEDIUMTEXT      NULL,
  change_note VARCHAR(255)    NULL,
  revised_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_news_rev (article_id, revised_at),
  CONSTRAINT fk_nrev_article FOREIGN KEY (article_id) REFERENCES news_articles (id) ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_nrev_editor  FOREIGN KEY (editor_id)  REFERENCES users (id)         ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Moderated reader comments (self-referencing for threads)
CREATE TABLE news_comments (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  article_id   BIGINT UNSIGNED NOT NULL,
  parent_id    BIGINT UNSIGNED NULL,
  author_name  VARCHAR(191)    NOT NULL,
  author_email VARCHAR(191)    NULL,
  body         TEXT            NOT NULL,
  status       ENUM('pending','approved','spam','rejected') NOT NULL DEFAULT 'pending',
  ip_address   VARBINARY(16)   NULL,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_ncomment_article (article_id, status),
  CONSTRAINT fk_ncomment_article FOREIGN KEY (article_id) REFERENCES news_articles (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_ncomment_parent  FOREIGN KEY (parent_id)  REFERENCES news_comments (id)  ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

> `news_categories` and `news_tags` are defined in [`index.md`](./index.md)
> (feed-level taxonomy). Create them before `news_articles` /
> `news_article_tags` due to FK ordering.

**Relationships**
- `news_articles.page_id → pages.id` (the `/news/` listing page).
- `news_articles.category_id → news_categories.id` (defined in
  [`index.md`](./index.md)).
- `news_articles.author_id → users.id` (shared CMS users).
- `news_articles.hero_media_id → media_assets.id` (shared media library).
- `news_article_tags.article_id → news_articles.id` and
  `news_article_tags.tag_id → news_tags.id` (many-to-many tagging).
- `news_article_media.article_id → news_articles.id` and
  `news_article_media.media_id → media_assets.id` (ordered per-article gallery).
- `news_article_revisions.article_id → news_articles.id` (with
  `editor_id → users.id`) provides an audit trail.
- `news_comments.article_id → news_articles.id` and
  `news_comments.parent_id → news_comments.id` (threaded comments).
