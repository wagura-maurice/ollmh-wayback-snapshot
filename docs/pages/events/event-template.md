# Event Page Template (`/events/<slug>`)

> This is the **reusable template** for every standalone event page on the
> site. Each event lives at `/events/<slug>` and is a row in the `wp_events`
> table. The calendar/listing page is documented in [`index.md`](./index.md).
>
> No events were captured in the Wayback Machine archive — all event pages will
> be created from scratch. Copy this file as the starting point for documenting
> a new event, then fill in the event-specific sections.

## 1. Current State Mapping

> _Describe the event's source content. Since no events were archived, this
> will typically be "Original content created for the rebuild."_

- **Event title:** _(fill in)_
- **Slug:** _(fill in)_
- **Source:** _(original content / migrated from X)_
- **Date & time:** _(fill in)_
- **Venue:** _(fill in)_
- **Description:** _(summary of the event body)_
- **Images:** _(list with file, dimensions, caption, alt text)_
- **Interactive elements:** _(RSVP/registration, add-to-calendar, comments, etc.)_

## 2. Gap Analysis & Feature Enhancements

**Content gaps**
- _(list content gaps for this event)_

**UX/UI**
- Event hero image, breadcrumb (`Home / Events / <event>`), "Back to Events" link.
- Date/time/venue block prominently displayed.
- Image gallery for multi-image events, with captions and `alt` text.
- RSVP / registration form (if `registration_required`).
- "Add to calendar" (Google/Outlook/.ics) button.
- Related-events module.

**Functionality & integrations**
- Cross-links to related pages (departments, community programs, nursing school).
- Email/SMS notifications to registrants on event updates.
- schema.org `Event` structured data for rich results.

**Accessibility & SEO**
- `alt` text on all images, canonical URL, per-event meta description,
  `Event` JSON-LD with `startDate`/`endDate`/`location`.

## 3. Page-Specific Metadata (Standalone Page)

| Field | Value |
| --- | --- |
| Route | `/events/<slug>` |
| Page type | `news` (row in `wp_events`) |
| Layout | `event-detail` — hero + details + RSVP + gallery |
| Slug | _(fill in)_ |
| Category | _(fill in)_ |
| Start date/time | _(fill in)_ |
| End date/time | _(fill in)_ |
| Venue | _(fill in)_ |
| Capacity | _(fill in or null)_ |
| Registration required | _(yes/no)_ |
| Canonical URL | `https://ollmh.example/events/<slug>` |
| Meta title | _(fill in)_ |
| Meta description | _(fill in)_ |
| schema.org type | `Event` |
| Hero image | _(fill in)_ |
| Sitemap priority | `0.6` |

## 4. Layout Structure (Standalone Page)

```
┌─────────────────────────────────────────────────────┐
│ Breadcrumb: Home / Events / <event title>           │
├─────────────────────────────────────────────────────┤
│ Event hero image                                    │
├──────────────────────────────────┬──────────────────┤
│ Event body                        │ Sidebar          │
│  - Title                          │ - Date & time    │
│  - Category badge                 │ - Venue / map    │
│  - Description                    │ - Add to calendar│
│  - Image gallery (if any)         │ - Related events │
│  - RSVP / registration form       │ - Categories     │
│  - Registrant list (if public)    │ - Newsletter     │
├──────────────────────────────────┴──────────────────┤
│ [← Previous event]        [Back to Events]   [Next →]│
├─────────────────────────────────────────────────────┤
│ Footer (shared)                                     │
└─────────────────────────────────────────────────────┘
```

## 5. Database Schema Design

These tables back **every** standalone event page. They are defined once here
and referenced by all event docs.

```sql
-- Events (one row per standalone event page)
CREATE TABLE wp_events (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id       BIGINT UNSIGNED NOT NULL,       -- the /events/ listing page
  category_id   BIGINT UNSIGNED NULL,
  title         VARCHAR(255)    NOT NULL,
  slug          VARCHAR(191)    NOT NULL,
  description   MEDIUMTEXT      NULL,
  starts_at     DATETIME        NOT NULL,
  ends_at       DATETIME        NULL,
  venue         VARCHAR(255)    NULL,
  capacity      SMALLINT UNSIGNED NULL,                       -- max attendees (null = unlimited)
  registration_required TINYINT(1) NOT NULL DEFAULT 0,
  hero_media_id BIGINT UNSIGNED NULL,
  status        ENUM('draft','published','archived','cancelled') NOT NULL DEFAULT 'draft',
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at    TIMESTAMP       NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_event_slug (slug),
  KEY idx_event_start (status, starts_at),
  CONSTRAINT fk_event_page FOREIGN KEY (page_id)       REFERENCES wp_pages (id)          ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_event_cat  FOREIGN KEY (category_id)   REFERENCES wp_event_categories (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_event_hero FOREIGN KEY (hero_media_id) REFERENCES wp_media_assets (id)   ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Event RSVP / registration with capacity + status tracking
CREATE TABLE wp_event_registrations (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  event_id      BIGINT UNSIGNED NOT NULL,
  attendee_name VARCHAR(191)    NOT NULL,
  attendee_email VARCHAR(191)   NOT NULL,
  attendee_phone VARCHAR(40)    NULL,
  party_size    SMALLINT UNSIGNED NOT NULL DEFAULT 1,
  status        ENUM('registered','waitlisted','cancelled','attended','no_show') NOT NULL DEFAULT 'registered',
  registered_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_event_attendee (event_id, attendee_email),
  KEY idx_event_reg (event_id, status),
  CONSTRAINT fk_ereg_event FOREIGN KEY (event_id) REFERENCES wp_events (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Ordered image gallery attached to an event (beyond the hero image)
CREATE TABLE wp_event_media (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  event_id   BIGINT UNSIGNED NOT NULL,
  media_id   BIGINT UNSIGNED NOT NULL,
  caption    VARCHAR(512)    NULL,
  sort_order INT UNSIGNED    NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_event_media (event_id, media_id),
  KEY idx_event_media (event_id, sort_order),
  CONSTRAINT fk_evmedia_event FOREIGN KEY (event_id) REFERENCES wp_events (id)      ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_evmedia_media FOREIGN KEY (media_id) REFERENCES wp_media_assets (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

> `wp_event_categories` is defined in [`index.md`](./index.md) (listing-level
> taxonomy). `wp_newsletter_subscribers` is shared with the news feed (defined in
> [`../news/index.md`](../news/index.md)).

**Relationships**
- `wp_events.page_id → wp_pages.id` (the `/events/` listing page).
- `wp_events.category_id → wp_event_categories.id` (defined in [`index.md`](./index.md)).
- `wp_events.hero_media_id → wp_media_assets.id` (shared media library).
- `wp_event_registrations.event_id → wp_events.id` records RSVPs, unique per
  attendee email per event, with waitlist/attendance states.
- `wp_event_media.event_id → wp_events.id` and `wp_event_media.media_id → wp_media_assets.id`
  (ordered per-event gallery).
