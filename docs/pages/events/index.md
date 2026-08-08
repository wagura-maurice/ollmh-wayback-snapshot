# Events Listing & Calendar (`/events/`)

> This is the **events index/calendar page** — a chronological listing of all
> published events (upcoming and past). Each event in the listing links to its
> own **standalone event page** documented in the sibling files in this folder.
>
> This page supersedes the old unified `news-events.html` page. News articles
> now live in [`../news/`](../news/).

## 1. Current State Mapping

- **Original archived page:** `/news-events.html` (titled "New & Events").
- **Actual archived content:** the page contained **no events at all** — no
  dates, no calendar, no venue information. It was a single static promotional
  article about the nursing school (now migrated to
  [`../news/nursing-school-promo.md`](../news/nursing-school-promo.md)).
- **Interactive elements (archived):** only the shared template Print/Email
  actions, a Prev pager link, header megamenu, and footer columns. No event
  calendar, RSVP, or date-based navigation.
- **Note:** injected Russian spam anchors (`printer-spb.ru`) appeared in the
  archived markup — template compromise artifacts.

## 2. Gap Analysis & Feature Enhancements

**Content gaps (major)**
- The page had **zero events**. The rebuild must introduce a genuine events
  calendar with dated entries — hospital open days, community outreach drives,
  nursing school intake openings, fundraising galas, medical camps, etc.
- Each event needs a title, date/time, venue, description, hero image, and
  optional RSVP/registration.

**UX/UI**
- Calendar grid view (month) + list view (upcoming/past), toggleable.
- Event cards (thumbnail, title, date, venue, excerpt) linking to standalone
  event pages (`/events/<slug>`).
- Filter by category (e.g. "Community", "Education", "Fundraising") and by
  upcoming/past.
- "Add to calendar" (Google/Outlook/.ics) export on each card.

**Functionality & integrations**
- RSVP / registration on event pages (see [`event-template.md`](./event-template.md)).
- Email/SMS notifications to registrants when event details change.
- Newsletter subscription for event announcements (shares
  `wp_newsletter_subscribers` with the news feed).

**Accessibility & SEO**
- `alt` text on all thumbnails, `Event` schema.org markup on the listing,
  canonical URL, and a meta description.

## 3. Page-Specific Metadata (Standalone Page)

| Field | Value |
| --- | --- |
| Route | `/events/` |
| Page type (in `wp_pages` table) | `news` (events share the news page-type family) |
| Layout | `events-calendar` — calendar grid + list + sidebar |
| Canonical URL | `https://ollmh.example/events/` |
| Meta title | "Events & Calendar — OLLMH" |
| Meta description | "Upcoming and past events at Our Lady of Lourdes Mwea Hospital: open days, community outreach, medical camps, and more." |
| schema.org type | `CollectionPage` + `ItemList` of `Event` |
| iCal feed | `/events/calendar.ics` |
| Sitemap priority | `0.8` |
| Cache strategy | Full-page cache, purged on event publish/cancel |

## 4. Layout Structure (Standalone Page)

```
┌─────────────────────────────────────────────────────┐
│ Hero / page header (title + intro)                  │
├──────────────────────────────────┬──────────────────┤
│ [ Month grid ]  [ List view ]    │ Sidebar          │
│  toggle                          │ - Categories     │
│                                  │ - Upcoming       │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐    │ - Past events    │
│  │evnt│ │evnt│ │evnt│ │evnt│    │ - Newsletter     │
│  └────┘ └────┘ └────┘ └────┘    │ - Subscribe to   │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐    │   calendar (.ics)│
│  │evnt│ │evnt│ │evnt│ │evnt│    │                  │
│  └────┘ └────┘ └────┘ └────┘    │                  │
│  [ ← Prev month ]  March 2026  [ Next month → ]    │
├──────────────────────────────────┴──────────────────┤
│ Footer (shared)                                     │
└─────────────────────────────────────────────────────┘
```

Each event card renders: thumbnail (`hero_media_id`), category badge, title,
date/time, venue, excerpt, and a "View event" link to `/events/<slug>`.

## 5. Database Schema Design

The listing page itself is a row in the shared `wp_pages` table. The events that
populate the calendar live in the `wp_events` table (defined in
[`event-template.md`](./event-template.md)).

```sql
-- Event categories (hierarchical taxonomy, parallel to news_categories)
CREATE TABLE wp_event_categories (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name       VARCHAR(191)    NOT NULL,
  slug       VARCHAR(191)    NOT NULL,
  parent_id  BIGINT UNSIGNED NULL,
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_eventcat_slug (slug),
  CONSTRAINT fk_eventcat_parent FOREIGN KEY (parent_id) REFERENCES wp_event_categories (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

> `wp_events`, `wp_event_registrations`, and `wp_event_media` are defined in
> [`event-template.md`](./event-template.md) because they belong to each
> **individual event page**, not the listing. `wp_newsletter_subscribers` is
> shared with the news feed (defined in [`../news/index.md`](../news/index.md)).

**Relationships**
- The listing page is a `wp_pages` row; every `wp_events.page_id → wp_pages.id` points
  back to it.
- `wp_event_categories.parent_id` self-references for nested categories.
- `wp_newsletter_subscribers` (defined in the news index) is reused for event
  announcements.

## 6. Events in This Directory

| Event | Doc | Status |
| --- | --- | --- |
| (Template for new events) | [event-template.md](./event-template.md) | Reusable template |

> No events were captured in the archive. All event pages will be created from
> scratch using the template.
