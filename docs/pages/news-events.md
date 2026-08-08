# New & Events (`/news-events.html`)

> Despite its "News & Events" title, the archived page is a single promotional article about the OLLMH School of Nursing rather than a dated news feed.

## 1. Current State Mapping

- **Page title:** browser/menu title "New & Events"; in-body `h1.title` reads **"New & Events"**.
- **Actual content:** the page does **not** contain a news list, dates, or event entries. Its `article-body` is one static promotional article about the nursing school:
  - Intro: "OLLMH School Of Nursing prepares and creates informed ability to provide nursing care and leadership within diverse healthcare settings."
  - Images: `news_events/schbus.JPG` (436×291, school bus) and `news_events/schdorm1.JPG` (220×292, dormitory).
  - Paragraph: the School of Nursing is "a major progress and achievement of the hospital, Mwea community and Kenya nation at large"; qualified candidates are increasingly applying at intake season.
  - A highlighted call-to-action text "**(Download Application Form)**" (styled text, not an actual link in this capture).
  - Captions "Nursing Students taking their Theory Lessons" / "A student Taking practical Lesson in Healthcare" above images `news_events/studphoto2.JPG` (305×153) and `news_events/studentprac.JPG` (288×153).
  - A welcome line with two animated GIFs (`graphics-welcome-*.gif`, `graphics-nursing-*.gif`): "Welcome to Our Lady Of Lourdes School Of Nursing."
- **Images have no `alt` text.**
- **Interactive elements:** only the shared template Print/Email actions, a Prev pager link, header megamenu, and footer columns. No dates, categories, pagination, or event calendar.
- **Note:** injected Russian spam anchors (`printer-spb.ru`) appear in the archived markup — template compromise artifacts.

## 2. Gap Analysis & Feature Enhancements

**Content gaps (major)**
- The page is mislabeled: it should be a genuine **News & Events feed** with dated posts, not a single nursing-school advert. Introduce real articles/announcements/events.
- Add publication dates, authors, categories/tags, featured images, and summaries/excerpts.

**UX/UI**
- Chronological, paginated article list with cards (thumbnail, title, date, excerpt) and a single-article detail view.
- An **events calendar** (upcoming vs. past) with date, time, venue, and RSVP.
- Category/tag filtering, search, and an RSS feed (the template already references RSS/Atom).

**Functionality & integrations**
- Email/newsletter subscription for new posts and events.
- Social sharing, related-articles module, and comment moderation (optional).
- Move the nursing-school promo + application CTA to the dedicated nursing pages; link out from relevant news posts.

**Accessibility & SEO**
- `alt` text, `Article`/`Event` schema.org markup, canonical URLs, and per-article meta descriptions.

## 3. Database Schema Design

```sql
-- News/announcement articles
CREATE TABLE news_articles (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,       -- the "News & Events" listing page
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

CREATE TABLE news_categories (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name       VARCHAR(191)    NOT NULL,
  slug       VARCHAR(191)    NOT NULL,
  parent_id  BIGINT UNSIGNED NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_newscat_slug (slug),
  CONSTRAINT fk_newscat_parent FOREIGN KEY (parent_id) REFERENCES news_categories (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE news_tags (
  id   BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(191)    NOT NULL,
  slug VARCHAR(191)    NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_newstag_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE news_article_tags (
  article_id BIGINT UNSIGNED NOT NULL,
  tag_id     BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (article_id, tag_id),
  CONSTRAINT fk_nat_article FOREIGN KEY (article_id) REFERENCES news_articles (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_nat_tag     FOREIGN KEY (tag_id)     REFERENCES news_tags (id)     ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Events (calendar entries)
CREATE TABLE events (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,
  title         VARCHAR(255)    NOT NULL,
  slug          VARCHAR(191)    NOT NULL,
  description   MEDIUMTEXT      NULL,
  starts_at     DATETIME        NOT NULL,
  ends_at       DATETIME        NULL,
  venue         VARCHAR(255)    NULL,
  hero_media_id BIGINT UNSIGNED NULL,
  status        ENUM('draft','published','archived','cancelled') NOT NULL DEFAULT 'draft',
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_event_slug (slug),
  KEY idx_event_start (starts_at),
  CONSTRAINT fk_event_page FOREIGN KEY (page_id)       REFERENCES pages (id)        ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_event_hero FOREIGN KEY (hero_media_id) REFERENCES media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Newsletter subscribers (for post/event notifications)
CREATE TABLE newsletter_subscribers (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  email         VARCHAR(191)    NOT NULL,
  is_confirmed  TINYINT(1)      NOT NULL DEFAULT 0,
  confirmed_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_subscriber_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

> Note: create `news_categories`/`news_tags` before `news_articles`/`news_article_tags` due to FK ordering.

**Relationships**
- `news_articles.page_id` and `events.page_id → pages.id` anchor both feeds to the "News & Events" listing page.
- `news_articles.category_id → news_categories.id` and the `news_article_tags` join give hierarchical + flat taxonomy; `author_id → users.id` reuses the shared CMS **`users`** table.
- All `hero_media_id`/`*_media_id` columns reference the shared **`media_assets`** library.
- `news_categories.parent_id` self-references to allow nested categories.
