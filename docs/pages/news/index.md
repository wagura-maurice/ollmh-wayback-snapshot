# News Listing & Feed (`/news/`)

> This is the **news index/listing page** — the chronological feed of all
> published news articles. Each article in the feed links to its own
> **standalone article page** documented in the sibling files in this folder.
>
> This page supersedes the old unified `news-events.html` page. Events now live
> in [`../events/`](../events/).

## 1. Current State Mapping

- **Original archived page:** `/news-events.html` (titled "New & Events").
- **Actual archived content:** the page did **not** contain a news list, dates,
  or event entries. Its `article-body` was one static promotional article about
  the nursing school (see [`nursing-school-promo.md`](./nursing-school-promo.md)
  for the full mapping of that single article).
- **Images on the archived page:** `news_events/schbus.JPG` (436×291, school
  bus), `news_events/schdorm1.JPG` (220×292, dormitory),
  `news_events/studphoto2.JPG` (305×153), `news_events/studentprac.JPG`
  (288×153). None had `alt` text.
- **Interactive elements (archived):** only the shared template Print/Email
  actions, a Prev pager link, header megamenu, and footer columns. No dates,
  categories, pagination, or event calendar.
- **Note:** injected Russian spam anchors (`printer-spb.ru`) appeared in the
  archived markup — template compromise artifacts.

## 2. Gap Analysis & Feature Enhancements

**Content gaps (major)**
- The page was mislabeled: it should be a genuine **news feed** with dated
  posts, not a single nursing-school advert. The nursing-school promo has been
  moved to its own article page
  ([`nursing-school-promo.md`](./nursing-school-promo.md)).
- Add publication dates, authors, categories/tags, featured images, and
  summaries/excerpts for every article in the feed.

**UX/UI**
- Chronological, paginated article list with cards (thumbnail, title, date,
  excerpt). Each card links to the article's standalone page
  (`/news/<slug>`).
- Category/tag filtering, search, and an RSS feed (the template already
  references RSS/Atom).
- Featured/sticky article slot at the top of the feed.
- Sidebar with recent posts, categories, and newsletter signup.

**Functionality & integrations**
- Email/newsletter subscription for new posts (see `wp_newsletter_subscribers`
  table below).
- Social sharing on each card, related-articles module on article pages.
- Comment moderation on article pages (see
  [`article-template.md`](./article-template.md)).

**Accessibility & SEO**
- `alt` text on all thumbnails, `Blog`/`ItemList` schema.org markup on the
  feed, canonical URL for the listing, and a meta description summarizing the
  feed.

## 3. Page-Specific Metadata (Standalone Page)

| Field | Value |
| --- | --- |
| Route | `/news/` |
| Page type (in `wp_pages` table) | `news` |
| Layout | `news-feed` — card grid + sidebar |
| Canonical URL | `https://ollmh.example/news/` |
| Meta title | "News & Announcements — OLLMH" |
| Meta description | "Latest news, announcements, and updates from Our Lady of Lourdes Mwea Hospital." |
| schema.org type | `CollectionPage` + `ItemList` |
| RSS/Atom feed | `/news/feed.xml` |
| Sitemap priority | `0.8` |
| Cache strategy | Full-page cache, purged on article publish/unpublish |

## 4. Layout Structure (Standalone Page)

```
┌─────────────────────────────────────────────────────┐
│ Hero / page header (title + intro)                  │
├──────────────────────────────────┬──────────────────┤
│ Article card grid (paginated)    │ Sidebar          │
│  ┌──────┐ ┌──────┐ ┌──────┐     │ - Categories     │
│  │ card │ │ card │ │ card │     │ - Tags           │
│  └──────┘ └──────┘ └──────┘     │ - Recent posts   │
│  ┌──────┐ ┌──────┐ ┌──────┐     │ - Newsletter     │
│  │ card │ │ card │ │ card │     │ - Search         │
│  └──────┘ └──────┘ └──────┘     │                  │
│  [ ← Prev ]   1 2 3   [ Next → ]│                  │
├──────────────────────────────────┴──────────────────┤
│ Footer (shared)                                     │
└─────────────────────────────────────────────────────┘
```

Each card renders: thumbnail (`hero_media_id`), category badge, title, excerpt,
author + date, and a "Read more" link to `/news/<slug>`.

## 5. Database Schema Design

The listing page itself is a row in the shared `wp_pages` table
(`page_type = 'news'`). The articles that populate the feed live in
`wp_news_articles` (defined in
[`article-template.md`](./article-template.md)). The tables below are
**feed-level** concerns: taxonomy, newsletter subscribers, and the join that
links articles to the listing page.

```sql
-- News categories (hierarchical taxonomy)
CREATE TABLE wp_news_categories (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name       VARCHAR(191)    NOT NULL,
  slug       VARCHAR(191)    NOT NULL,
  parent_id  BIGINT UNSIGNED NULL,
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_newscat_slug (slug),
  CONSTRAINT fk_newscat_parent FOREIGN KEY (parent_id) REFERENCES wp_news_categories (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Flat tag set
CREATE TABLE wp_news_tags (
  id   BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(191)    NOT NULL,
  slug VARCHAR(191)    NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_newstag_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Newsletter subscribers (for post notifications)
CREATE TABLE wp_newsletter_subscribers (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  email         VARCHAR(191)    NOT NULL,
  is_confirmed  TINYINT(1)      NOT NULL DEFAULT 0,
  confirmed_at  DATETIME        NULL,
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_subscriber_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

> `wp_news_articles`, `wp_news_article_tags`, `wp_news_article_media`,
> `wp_news_article_revisions`, and `wp_news_comments` are defined in
> [`article-template.md`](./article-template.md) because they belong to each
> **individual article page**, not the listing.

**Relationships**
- The listing page is a `wp_pages` row (`page_type = 'news'`); every
  `wp_news_articles.page_id → wp_pages.id` points back to it.
- `wp_news_categories.parent_id` self-references for nested categories.
- `wp_newsletter_subscribers` is standalone (no FK) — used by the notification
  pipeline to alert subscribers when a new article is published.

## 6. Articles in This Directory

| Article | Doc | Status |
| --- | --- | --- |
| OLLMH School of Nursing Launch (archived promo) | [nursing-school-promo.md](./nursing-school-promo.md) | Migrated from archive |
| (Template for new articles) | [article-template.md](./article-template.md) | Reusable template |
