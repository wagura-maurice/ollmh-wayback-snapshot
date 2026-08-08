# New & Events (`/news-events.html`) — SPLIT

> **This page has been split.** The old unified `/news-events.html` page
> treated News and Events as a single page. The new site architecture gives
> each news item and each event its own standalone page.
>
> The content and schemas that were previously in this file have been moved to:
>
> - **News feed (listing):** [`./news/index.md`](./news/index.md)
> - **News article pages (one per article):**
>   - [`./news/nursing-school-promo.md`](./news/nursing-school-promo.md) — the
>     one archived article (nursing-school promo), migrated as a standalone
>     article page.
>   - [`./news/article-template.md`](./news/article-template.md) — reusable
>     template for all future article pages, with the full `wp_news_articles`,
>     `wp_news_article_tags`, `wp_news_article_media`, `wp_news_article_revisions`, and
>     `wp_news_comments` schema.
> - **Events calendar (listing):** [`./events/index.md`](./events/index.md)
> - **Event pages (one per event):**
>   - [`./events/event-template.md`](./events/event-template.md) — reusable
>     template for all event pages, with the full `wp_events`,
>     `wp_event_registrations`, and `wp_event_media` schema.
>
> The shared `wp_news_categories`, `wp_news_tags`, and `wp_newsletter_subscribers`
> tables are now defined in [`./news/index.md`](./news/index.md), and
> `wp_event_categories` in [`./events/index.md`](./events/index.md).
>
> See [`../ERD.md`](../ERD.md) for the consolidated entity-relationship diagram
> covering all tables.
