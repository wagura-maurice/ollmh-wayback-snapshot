# News Article: OLLMH School of Nursing Launch (`/news/nursing-school-launch`)

> This is a **standalone article page** for the single piece of news content
> that existed in the archived `/news-events.html` page — a promotional article
> about the OLLMH School of Nursing. In the new architecture each news item
> gets its own page at `/news/<slug>`; this is the first such page, migrated
> from the old unified page.
>
> The feed/listing page is documented in [`index.md`](./index.md). The reusable
> template for future articles is in
> [`article-template.md`](./article-template.md).

## 1. Current State Mapping

> This content was originally part of the unified `/news-events.html` page. It
> is reproduced here in full so this article page is self-contained.

- **Source page:** `/news-events.html` (archived, titled "New & Events").
- **Article title (proposed):** "OLLMH School of Nursing — A Major Milestone"
  (the archived page had no article-level title; the body was the nursing-school
  promo).
- **Actual archived content:** the `article-body` was one static promotional
  article about the nursing school:
  - **Intro:** "OLLMH School Of Nursing prepares and creates informed ability to
    provide nursing care and leadership within diverse healthcare settings."
  - **Images:**
    - `news_events/schbus.JPG` (436×291, school bus) — caption: none in archive.
    - `news_events/schdorm1.JPG` (220×292, dormitory) — caption: none in archive.
    - `news_events/studphoto2.JPG` (305×153) — caption: "Nursing Students taking
      their Theory Lessons".
    - `news_events/studentprac.JPG` (288×153) — caption: "A student Taking
      practical Lesson in Healthcare".
  - **Body paragraph:** the School of Nursing is "a major progress and
    achievement of the hospital, Mwea community and Kenya nation at large";
    qualified candidates are increasingly applying at intake season.
  - **Call-to-action:** a highlighted "**(Download Application Form)**" text
    (styled text, not an actual link in this capture).
  - **Welcome line** with two animated GIFs (`graphics-welcome-*.gif`,
    `graphics-nursing-*.gif`): "Welcome to Our Lady Of Lourdes School Of Nursing."
- **Images have no `alt` text.**
- **Interactive elements (archived):** only the shared template Print/Email
  actions, a Prev pager link, header megamenu, and footer columns. No dates,
  categories, or article-specific navigation.
- **Note:** injected Russian spam anchors (`printer-spb.ru`) appeared in the
  archived markup — template compromise artifacts.

## 2. Gap Analysis & Feature Enhancements

**Content gaps**
- Give the article a real **headline**, **publication date**, **author**, and
  **category** (e.g. "Education" / "School of Nursing").
- Write a proper **excerpt** for the feed card.
- Replace the animated GIF welcome line with a static hero image or remove it.
- Rewrite the body as a proper news article (lead paragraph, body, quote,
  closing) rather than a raw promo blurb.
- Move the "Download Application Form" CTA to a real button linking to the
  [application form page](../medical-school-application-form.md).

**UX/UI**
- Article hero image (the school bus or dormitory photo), breadcrumb
  (`Home / News / OLLMH School of Nursing Launch`), and a "Back to News" link.
- Image gallery for the four archived photos with proper captions and `alt`
  text.
- Related-articles module and social-sharing buttons.
- Comments section (moderated).

**Functionality & integrations**
- Link to the [About the Nursing School](../about-nursing-school.md) page and
  the [application form](../medical-school-application-form.md) as in-article
  CTAs.
- schema.org `NewsArticle` structured data for Google News / rich results.

**Accessibility & SEO**
- `alt` text on all images, canonical URL (`/news/nursing-school-launch`),
  per-article meta description, and `NewsArticle` JSON-LD.

## 3. Page-Specific Metadata (Standalone Page)

| Field | Value |
| --- | --- |
| Route | `/news/nursing-school-launch` |
| Page type | `news` (row in `wp_news_articles`, not a standalone `wp_pages` row) |
| Layout | `news-article` — hero + body + gallery + sidebar |
| Slug | `nursing-school-launch` |
| Category | Education / School of Nursing |
| Proposed publish date | (backfill from archive date: 2022-03-19) |
| Author | OLLMH Communications (placeholder) |
| Canonical URL | `https://ollmh.example/news/nursing-school-launch` |
| Meta title | "OLLMH School of Nursing — A Major Milestone" |
| Meta description | "Our Lady of Lourdes Mwea Hospital launches its School of Nursing, training the next generation of healthcare leaders." |
| schema.org type | `NewsArticle` |
| Hero image | `news_events/schbus.JPG` (school bus) |
| Featured | Yes (first/seed article) |
| Sitemap priority | `0.6` |

## 4. Layout Structure (Standalone Page)

```
┌─────────────────────────────────────────────────────┐
│ Breadcrumb: Home / News / OLLMH School of Nursing…  │
├─────────────────────────────────────────────────────┤
│ Article hero image (schbus.JPG)                     │
├──────────────────────────────────┬──────────────────┤
│ Article body                      │ Sidebar          │
│  - Headline                       │ - Author card    │
│  - Meta (date, author, category)  │ - Related posts  │
│  - Lead paragraph                 │ - Categories     │
│  - Body paragraphs                │ - Tags           │
│  - Image gallery (4 photos)       │ - Newsletter     │
│  - CTA: Apply now →               │ - Social share   │
│  - Comments section               │                  │
├──────────────────────────────────┴──────────────────┤
│ [← Previous article]        [Back to News]   [Next →]│
├─────────────────────────────────────────────────────┤
│ Footer (shared)                                     │
└─────────────────────────────────────────────────────┘
```

## 5. Image Gallery (Archived Assets)

| # | File | Dimensions | Caption (archived) | Proposed `alt` text |
| --- | --- | --- | --- | --- |
| 1 | `news_events/schbus.JPG` | 436×291 | — | "School bus for the OLLMH School of Nursing" |
| 2 | `news_events/schdorm1.JPG` | 220×292 | — | "Dormitory at the OLLMH School of Nursing" |
| 3 | `news_events/studphoto2.JPG` | 305×153 | Nursing Students taking their Theory Lessons | "Nursing students during a theory lesson" |
| 4 | `news_events/studentprac.JPG` | 288×153 | A student Taking practical Lesson in Healthcare | "A nursing student during a practical lesson" |

These map to `wp_news_article_media` rows (ordered gallery) referencing the shared
`wp_media_assets` library.

## 6. Database Schema Design

This article is a **row in `wp_news_articles`** (defined in
[`article-template.md`](./article-template.md)). No article-specific tables are
needed beyond what the template defines. The article's relationships are:

```sql
-- Example row for this article (illustrative, not a CREATE TABLE)
-- news_articles:
--   slug           = 'nursing-school-launch'
--   title          = 'OLLMH School of Nursing — A Major Milestone'
--   category_id    = (Education category)
--   author_id      = (OLLMH Communications user)
--   hero_media_id  = (schbus.JPG media asset)
--   is_featured    = 1
--   status         = 'published'
--   published_at   = '2022-03-19 20:53:45'  (backfilled from archive date)

-- news_article_media (ordered gallery, 4 rows):
--   sort_order 0: schbus.JPG    "School bus for the OLLMH School of Nursing"
--   sort_order 1: schdorm1.JPG  "Dormitory at the OLLMH School of Nursing"
--   sort_order 2: studphoto2.JPG "Nursing students during a theory lesson"
--   sort_order 3: studentprac.JPG "A nursing student during a practical lesson"
```

**Relationships**
- `wp_news_articles.page_id → wp_pages.id` (the `/news/` listing page).
- `wp_news_articles.category_id → wp_news_categories.id` (defined in
  [`index.md`](./index.md)).
- `wp_news_articles.author_id → wp_users.id` (shared CMS users).
- `wp_news_articles.hero_media_id → wp_media_assets.id` (shared media library).
- `wp_news_article_media.article_id → wp_news_articles.id` (the 4-image gallery).
- `wp_news_article_media.media_id → wp_media_assets.id` (shared media library).

See [`article-template.md`](./article-template.md) for the full `CREATE TABLE`
statements for `wp_news_articles`, `wp_news_article_media`, `wp_news_article_revisions`,
`wp_news_article_tags`, and `wp_news_comments`.
