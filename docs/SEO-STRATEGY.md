# SEO Strategy — Tools, Seed Data Architecture & Implementation

> This document defines the **complete SEO tool stack**, the **database
> tables that require seed information** for SEO to function correctly, and
> how that seed data integrates with each tool to drive search performance
> for the **Our Lady of Lourdes Mwea Hospital (OLLMH)** WordPress website.
>
> It extends the existing schema (80 tables in the
> [ERD](./ERD.md)) with SEO-specific tables and maps every SEO tool to the
> seed data it consumes.
>
> **Sources:** WordPress.org plugin directory, Google Search Console
> documentation, schema.org MedicalBusiness/Hospital/Physician
> specifications, Sitebulb data modeling guide, Metabase SEO analytics
> reference, and current WordPress technical SEO best practices (2025–2026).

---

## Table of contents

1. [Tool integration — the complete SEO stack](#1-tool-integration--the-complete-seo-stack)
   - [Layer 1: On-page SEO plugin](#layer-1-on-page-seo-plugin)
   - [Layer 2: Google integration](#layer-2-google-integration)
   - [Layer 3: Structured data / schema markup](#layer-3-structured-data--schema-markup)
   - [Layer 4: Redirect & 404 management](#layer-4-redirect--404-management)
   - [Layer 5: Performance & Core Web Vitals](#layer-5-performance--core-web-vitals)
   - [Layer 6: Broken link monitoring](#layer-6-broken-link-monitoring)
   - [Layer 7: Keyword research & rank tracking](#layer-7-keyword-research--rank-tracking)
   - [Layer 8: XML sitemap & robots.txt](#layer-8-xml-sitemap--robotstxt)
   - [Layer 9: Social / Open Graph](#layer-9-social--open-graph)
   - [Layer 10: SEO data warehouse (optional advanced)](#layer-10-seo-data-warehouse-optional-advanced)
   - [Tool stack summary table](#tool-stack-summary-table)
2. [Seed information & data architecture](#2-seed-information--data-architecture)
   - [What "seed information" means in SEO context](#what-seed-information-means-in-seo-context)
   - [Existing tables that need SEO seed data](#existing-tables-that-need-seo-seed-data)
   - [New SEO-specific tables requiring seed data](#new-seo-specific-tables-requiring-seed-data)
   - [Seed data reference table (all tables)](#seed-data-reference-table-all-tables)
3. [Implementation guidance — how seed data drives SEO](#3-implementation-guidance--how-seed-data-drives-seo)
   - [Seed → tool integration map](#seed--tool-integration-map)
   - [Phase 1: Foundation seed data (pre-launch)](#phase-1-foundation-seed-data-pre-launch)
   - [Phase 2: Content seed data (launch)](#phase-2-content-seed-data-launch)
   - [Phase 3: Ongoing SEO operations (post-launch)](#phase-3-ongoing-seo-operations-post-launch)
   - [Schema.org JSON-LD seed templates](#schemaorg-json-ld-seed-templates)
4. [Admin sidebar SEO menu](#4-admin-sidebar-seo-menu)
5. [Recommended plugin versions](#5-recommended-plugin-versions)

---

## 1. Tool integration — the complete SEO stack

Beyond Google Analytics 4 and Rank Math, a comprehensive WordPress SEO
setup requires **10 tool layers**. Each layer addresses a distinct SEO
function. No single plugin covers all layers — the stack is intentionally
modular.

### Layer 1: On-page SEO plugin

**Rank Math** (already selected) or **Yoast SEO** / **SEOPress** / **AIOSEO**.

This is the primary on-page SEO engine. It handles:
- Meta title & meta description templates per content type
- Canonical URL injection
- `robots` meta directives (`index`/`noindex`, `follow`/`nofollow`)
- Focus keyword analysis and content readability scoring
- Breadcrumb generation
- Basic schema markup (Article, Organization, BreadcrumbList)
- XML sitemap generation (see Layer 8)
- Open Graph & Twitter Card tags (see Layer 9)
- 404 monitor (basic — supplemented by Layer 4)
- Internal linking suggestions (Rank Math PRO)

**OLLMH recommendation:** Keep **Rank Math** as the primary SEO plugin. Do
not install a second on-page SEO plugin — running two produces conflicting
canonical tags, duplicate meta output, and double sitemaps.

---

### Layer 2: Google integration

**Site Kit by Google** (free, official Google plugin).

Site Kit is **not** an SEO plugin — it is a **data pipeline** that connects
the WordPress site to Google's measurement products and surfaces their data
inside the WordPress dashboard. It connects to:

| Google product | What it provides | SEO use |
|---|---|---|
| **Google Search Console** | Queries, clicks, impressions, CTR, average position, indexing status, crawl errors, sitemap submission | Primary SEO performance data — which queries drive traffic, which pages are indexed, which have errors |
| **Google Analytics 4** | User behavior, traffic sources, engagement metrics, conversions | Correlates SEO traffic with on-site behavior and conversions (appointment bookings, application submissions) |
| **PageSpeed Insights** | Core Web Vitals (LCP, INP, CLS), performance scores | Technical SEO — page speed signals that affect rankings |
| **AdSense** (optional) | Ad revenue data | Not relevant for OLLMH (non-commercial hospital site) |

**Why Site Kit is critical:** Without Search Console data piped into
WordPress, the SEO plugin operates blind — it can optimize meta tags but
cannot see which keywords actually drive traffic or which pages have
indexing errors. Site Kit bridges this gap.

**OLLMH recommendation:** Install Site Kit alongside Rank Math. Connect
Search Console and GA4 at minimum. PageSpeed Insights is a bonus.

---

### Layer 3: Structured data / schema markup

**Rank Math's built-in schema module** handles basic types (Article,
Organization, BreadcrumbList, LocalBusiness). However, OLLMH is a
**hospital** — it needs **medical-specific schema types** that general SEO
plugins do not generate by default:

| Schema type | Where it applies | Why it matters |
|---|---|---|
| `Hospital` (subtype of `MedicalBusiness` → `LocalBusiness`) | Home page, location page | Enables Google Knowledge Panel, Maps eligibility, rich hospital info in search results |
| `MedicalClinic` | Clinics & OPD pages | Distinguishes clinic services from the main hospital entity |
| `Physician` (subtype of `MedicalBusiness`) | Staff profile pages | Connects doctors to specialties, credentials, hospital affiliation — critical for E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) |
| `MedicalProcedure` | Special medical services pages | Links procedures to conditions and providers in Google's medical knowledge graph |
| `MedicalCondition` | Condition-focused content (if added) | Connects content to Google's medical knowledge graph |
| `Event` | Event pages | Enables event rich snippets (date, location, registration) in search results |
| `FAQPage` | Pages with FAQ sections | Enables FAQ rich results (dropdown Q&A in search) |
| `WebSite` + `SearchAction` | Site-wide | Enables sitelinks search box in Google results |
| `BreadcrumbList` | All pages | Enables breadcrumb display in search results |
| `Organization` + `sameAs` (social profiles) | Site-wide | Connects the hospital entity to its social media profiles in the Knowledge Graph |

**OLLMH recommendation:** Use Rank Math's schema module for basic types
(Article, BreadcrumbList, WebSite, Organization). For medical-specific
types (`Hospital`, `Physician`, `MedicalClinic`, `MedicalProcedure`),
either:
- **Option A (recommended):** Write custom JSON-LD templates in the theme
  that pull seed data from the database tables (see
  [Section 2](#2-seed-information--data-architecture)). This gives full
  control and ensures the markup matches the schema.org spec exactly.
- **Option B:** Install the **Schema Markup for Medical Business** plugin
  (wordpress.org/plugins/schema-markup-for-medical-business/) which
  generates medical-specific JSON-LD and coexists defensively with Rank
  Math.

---

### Layer 4: Redirect & 404 management

**Redirection** (free, wordpress.org/plugins/redirection/).

Rank Math includes a basic 404 monitor and redirect manager, but the
**Redirection** plugin is the industry standard for this function:

- **301/302/307 redirect management** with a full admin UI
- **404 error logging** — tracks every 404 with URL, referrer, IP, timestamp
- **Automatic redirect creation** when a post/page permalink changes
- **Bulk redirect** from CSV
- **Redirect groups** for organization (e.g., "old Joomla URLs", "rebrands")
- **Regex redirects** for pattern-based URL matching
- **HTTP cache header** configuration
- **WP-CLI support** for command-line redirect management (dev only — on
  production, redirects are managed via the WordPress admin UI at Tools →
  Redirection; see [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md)
  → ADR-005)

**Why this is critical for OLLMH:** The site is migrating from a Joomla
archive to WordPress. Every old Joomla URL
(`index.php?option=com_content&view=article&id=123`) must be 301-redirected
to its new WordPress equivalent. Without this, all existing search equity
and inbound links are lost. The Redirection plugin manages this migration
and ongoing URL changes.

**OLLMH recommendation:** Install Redirection. Disable Rank Math's 404
monitor to avoid duplicate logging. Configure log expiry to 30 days.

---

### Layer 5: Performance & Core Web Vitals

**WP Rocket** (premium) or **LiteSpeed Cache** (free, if hosting supports
LiteSpeed) or **W3 Total Cache** (free).

Core Web Vitals are Google ranking factors. The three metrics:

| Metric | What it measures | Good threshold |
|---|---|---|
| **LCP** (Largest Contentful Paint) | Time until the largest visible element renders | < 2.5s |
| **INP** (Interaction to Next Paint) | Responsiveness to user interactions | < 200ms |
| **CLS** (Cumulative Layout Shift) | Visual stability (how much the layout shifts) | < 0.1 |

A caching/performance plugin addresses these by:
- **Page caching** — serves pre-rendered HTML, reducing server response time (improves LCP)
- **CSS/JS minification & deferral** — reduces render-blocking resources (improves LCP, INP)
- **Lazy loading images** — defers offscreen image loading (improves LCP, CLS)
- **Critical CSS generation** — inlines above-the-fold CSS (improves LCP)
- **Database optimization** — cleans post revisions, transients, spam
- **CDN integration** — serves assets from edge locations (improves LCP globally)

**OLLMH recommendation:** Use **WP Rocket** if budget allows (it is the
most reliable and user-friendly). Otherwise, **LiteSpeed Cache** if the
host runs LiteSpeed, or **W3 Total Cache** as a free fallback. Configure
image dimensions on all `<img>` tags (the archived site already has
`width`/`height` attributes — preserve these in the rebuild to prevent
CLS).

---

### Layer 6: Broken link monitoring

**Broken Link Checker** (free, wordpress.org/plugins/broken-link-checker/)
or **WP Broken Link Status Checker**.

Unlike the Redirection plugin (which monitors 404s on *your* site),
Broken Link Checker monitors **outbound links** — links from your content
to external sites that may have gone dead:

- Scans posts, pages, comments, and custom fields for links
- Detects broken links, redirects, and removed pages
- Notifies admins via email or dashboard when a link breaks
- Allows editing/unlinking broken links directly from the plugin UI

**Why this matters for SEO:** Broken outbound links are a negative quality
signal. Google's crawlers follow them and encounter errors, which
degrades the page's perceived quality. For a hospital site that links to
medical resources, partner organizations, and government health portals,
monitoring these links is essential.

**OLLMH recommendation:** Install Broken Link Checker. Configure it to
scan weekly (not daily — daily scans are resource-intensive). Set email
notifications to the Editor role.

---

### Layer 7: Keyword research & rank tracking

Rank Math includes basic keyword tracking in its PRO version. For a
comprehensive setup, integrate with external keyword research tools:

| Tool | Function | Integration with WordPress |
|---|---|---|
| **Google Keyword Planner** (free) | Search volume, competition, CPC estimates | Manual — export keywords, import into Rank Math focus keyword field |
| **Google Search Console** (free, via Site Kit) | Actual queries driving traffic, impressions, CTR, position | Automatic via Site Kit dashboard |
| **Semrush** (paid) | Keyword research, competitor analysis, rank tracking, backlink analysis | Yoast integration (keyword research in editor); Rank Math does not integrate directly |
| **Ahrefs** (paid) | Keyword research, backlink monitoring, site audits, rank tracking | Standalone — no direct WordPress integration; use API for custom dashboards |
| **Wincher** (freemium) | Rank tracking (daily position tracking) | Yoast integration (track keywords in WordPress dashboard) |

**OLLMH recommendation:** For a hospital website with a local/regional
audience, the free tools (Google Keyword Planner + Search Console via
Site Kit) are sufficient for the first 6–12 months. If competitive
analysis becomes necessary, add Semrush or Ahrefs as a standalone tool
(no WordPress integration needed — use their web dashboards). The keyword
data feeds into the `wp_seo_keywords` seed table (see Section 2).

---

### Layer 8: XML sitemap & robots.txt

**Handled by Rank Math** (no additional plugin needed).

Rank Math generates:
- **XML sitemap index** at `/sitemap_index.xml`
- **Child sitemaps** per content type (posts, pages, news, events,
  departments, custom post types)
- **Image sitemaps** (includes images in each page's sitemap entry)
- **News sitemap** (for the News CPT — enables Google News inclusion)
- **Last modification dates** (`lastmod`) on every URL
- **Priority and changefreq** hints (Google largely ignores these but they
  don't hurt)

**robots.txt** is generated by WordPress core (virtual file at
`/robots.txt`). Rank Math can customize it. The recommended configuration:

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /wp-content/plugins/
Disallow: /wp-includes/
Disallow: /?s=*
Disallow: /search/

Sitemap: https://ourladyoflourdesmweahospital.org/sitemap_index.xml
```

**OLLMH recommendation:** Submit the sitemap URL to Google Search Console
via Site Kit. Verify that all `noindex` pages are excluded from the
sitemap (Rank Math handles this automatically). Add the sitemap URL to
robots.txt.

---

### Layer 9: Social / Open Graph

**Handled by Rank Math** (no additional plugin needed).

Rank Math generates:
- **Open Graph tags** (`og:title`, `og:description`, `og:image`,
  `og:url`, `og:type`, `og:site_name`, `og:locale`) — used by Facebook,
  LinkedIn, WhatsApp
- **Twitter Card tags** (`twitter:card`, `twitter:title`,
  `twitter:description`, `twitter:image`) — used by X/Twitter
- **Default social image** — a fallback image used when a page doesn't
  have a specific `og:image`

**Seed data required:** Each page and post needs:
- A social share image (1200×630px recommended) — stored in
  `wp_media_assets` and linked via `wp_seo_meta.og_image_id`
- A social title and description (can fall back to meta title/description
  if not explicitly set)

**OLLMH recommendation:** Create a default social share image (the
hospital logo on a branded background) and set it as the fallback in Rank
Math. For each major page (home, departments, news articles, events),
create a custom 1200×630px social image.

---

### Layer 10: SEO data warehouse (optional advanced)

For data-driven SEO at scale, SEO data can be warehoused in a SQL database
for trend analysis, custom dashboards, and joining SEO performance with
business outcomes. This is an **advanced, optional** layer — not needed
for launch but valuable after 6–12 months of SEO data accumulation.

**Tools:** Metabase (free, open-source analytics), Google Looker Studio
(free), or a custom WordPress admin dashboard plugin.

**Data model** (based on the Metabase SEO analytics reference and the
Iriscale keyword database guide):

| Table | Granularity | Key columns |
|---|---|---|
| `seo_keyword_positions` | One row per keyword per domain per snapshot date | keyword_id, domain, snapshot_date, position, search_volume, url |
| `keyword_metrics` | One row per keyword | keyword_id, keyword_string, volume, difficulty, keyword_group_id |
| `authority_daily` | One row per domain per day | domain, date, authority_score, referring_domains, backlinks |
| `backlink_changes` | One row per gained/lost referring domain per day | domain, date, referring_domain, change_type (gained/lost) |
| `serp_snapshots` | One row per keyword per result per crawl | keyword_id, crawl_date, result_domain, position, serp_feature_type |
| `audit_snapshots` | One row per site audit run | audit_date, health_score, issue_count, critical_count, warning_count |
| `gsc_performance_daily` | One row per query per page per device per country per date | date, query, page_url, device, country, clicks, impressions, ctr, avg_position |
| `keyword_groups` | Reference table for keyword sets | group_id, group_name, brand/nonbrand, topic_cluster |

**OLLMH recommendation:** Skip this layer at launch. After 6–12 months,
if SEO performance data needs deeper analysis than Site Kit's dashboard
provides, export Search Console data via API into a SQL database and build
Metabase dashboards. The `gsc_performance_daily` table is the highest-value
starting point.

---

### Tool stack summary table

| # | Layer | Plugin / tool | Cost | Status |
|---|---|---|---|---|
| 1 | On-page SEO | **Rank Math** | Free (PRO optional) | Already selected |
| 2 | Google integration | **Site Kit by Google** | Free | **Add — critical** |
| 3 | Structured data (medical) | **Custom JSON-LD templates** or Schema Markup for Medical Business | Free | **Add — critical for hospital** |
| 4 | Redirect & 404 | **Redirection** | Free | **Add — critical for Joomla migration** |
| 5 | Performance / CWV | **WP Rocket** or LiteSpeed Cache | Premium / Free | **Add — critical for Core Web Vitals** |
| 6 | Broken link monitor | **Broken Link Checker** | Free | **Add — recommended** |
| 7 | Keyword research | **Google Keyword Planner + Search Console** (via Site Kit) | Free | Already available via Site Kit |
| 8 | XML sitemap & robots.txt | **Rank Math** (built-in) | Free | Already covered |
| 9 | Social / Open Graph | **Rank Math** (built-in) | Free | Already covered |
| 10 | SEO data warehouse | **Metabase** (optional, post-launch) | Free | Optional — defer 6–12 months |

**Net new plugins to install: Site Kit, Redirection, WP Rocket (or
alternative), Broken Link Checker.** That's 4 plugins beyond Rank Math and
Google Analytics.

---

## 2. Seed information & data architecture

### What "seed information" means in SEO context

"Seed information" is the **initial data that must exist in the database
before SEO tools can function correctly**. SEO is not a plugin you install
and forget — it requires structured data about your entity, content, and
target keywords. Without seed data:

- Schema markup outputs empty or generic JSON-LD (no hospital name, no
  address, no phone — Google sees a blank entity)
- Meta titles and descriptions are auto-generated from post titles (often
  truncated, keyword-stuffed, or irrelevant)
- XML sitemaps include the wrong pages (draft pages, admin pages, thin
  content)
- Rank Math's content analysis has no focus keyword to score against
- Search Console has no sitemap to crawl
- Social shares show no image or the wrong image
- Redirect maps have no source→target URL pairs (old Joomla URLs 404)

Seed data is the **fuel** that makes the SEO engine run.

### Existing tables that need SEO seed data

The OLLMH schema already has 80 tables. Several of them need SEO-specific
seed data populated before launch:

#### `wp_pages` — meta title, meta description, canonical, robots directive

The `wp_pages` table already has `meta_title`, `meta_desc`, and `slug`
columns (defined in [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md)).
Every row needs:

| Column | Seed value | Example |
|---|---|---|
| `slug` | URL-friendly slug | `wards`, `clinic-days`, `nursing-school` |
| `meta_title` | 50–60 character SEO title | `"Wards & Inpatient Services \| OLLMH Mwea Hospital"` |
| `meta_desc` | 150–160 character meta description | `"Our Lady of Lourdes Mwea Hospital offers general, maternity, and pediatric wards with 24/7 care. View bed availability and admission information."` |

**Seed count:** ~25 pages (one per navigable page in the site map).

#### `wp_media_assets` — alt text for every image

Every image needs `alt_text` populated. This is both an accessibility
requirement (WCAG) and an SEO signal (Google uses alt text for image
search and to understand image context).

| Column | Seed value | Example |
|---|---|---|
| `alt_text` | Descriptive alternative text | `"OLLMH hospital main building exterior, Mwea, Kenya"` |

**Seed count:** Every image in the media library (estimate: 100–200 images
from the archived site + new images created for the rebuild).

#### `wp_departments` — department name, description, category

Department pages are key landing pages for local search ("hospital
departments in Mwea", "maternity ward Mwea"). Each department row needs:

| Column | Seed value | Example |
|---|---|---|
| `slug` | URL-friendly slug | `maternity`, `pediatrics`, `surgery` |
| `category` | Department category enum | `clinical`, `administrative`, `support` |

The department's `wp_pages` row (linked via `page_id`) needs the
corresponding meta title and description.

**Seed count:** ~15–20 departments.

#### `wp_staff` — staff name, title, department, photo

Staff profile pages are critical for E-E-A-T (Expertise,
Authoritativeness, Trustworthiness). Google's medical content guidelines
emphasize author credentials. Each staff row needs:

| Column | Seed value | Example |
|---|---|---|
| `full_name` | Full name | `"Dr. John Mwangi"` |
| `department_id` | FK to wp_departments | (maternity department) |
| `photo_media_id` | FK to wp_media_assets | (staff portrait) |

The staff member's `Physician` schema markup pulls from these fields.

**Seed count:** ~30–50 staff members.

#### `wp_location_info` — hospital address, GPS, phone, hours

This is the **most critical seed table for local SEO**. The `Hospital`
schema markup and Google Business Profile both pull from this data. If
these fields are empty, Google cannot populate the Knowledge Panel or
Maps listing.

| Column | Seed value | Example |
|---|---|---|
| `name` | Hospital name | `"Our Lady of Lourdes Mwea Hospital"` |
| `street_address` | Physical address | `"Mwea, Kirinyaga County, Kenya"` |
| `latitude` / `longitude` | GPS coordinates | `-0.6703, 37.3552` (approximate) |
| `phone` | Primary phone | `"+254 700 000 000"` |
| `email` | Primary email | `"info@ourladyoflourdesmweahospital.org"` |
| `opening_hours` | Operating hours | `"Mon–Sun, 24 hours"` |
| `website_url` | Website URL | `"https://ourladyoflourdesmweahospital.org"` |

**Seed count:** 1 row (single hospital location).

#### `wp_contact_channels` — social media profiles for `sameAs` schema

The `Organization` schema's `sameAs` property links the hospital to its
social media profiles. This data lives in `wp_contact_channels`:

| Column | Seed value | Example |
|---|---|---|
| `channel_type` | `social` | — |
| `label` | Platform name | `"Facebook"`, `"X"`, `"YouTube"` |
| `value` | Profile URL | `"https://facebook.com/ollmh"` |

**Seed count:** 2–5 social profiles.

#### `wp_news_articles` / `wp_events` — title, excerpt, slug, featured image

News articles and events are the primary content types for ongoing SEO.
Each needs:

| Column | Seed value | Example |
|---|---|---|
| `slug` | URL-friendly slug | `nursing-school-launch-2024` |
| `title` | SEO-optimized title | `"OLLMH Launches Nursing School Programme — 2024 Intake Open"` |
| `excerpt` | 150–160 char summary (used as meta description) | `"Our Lady of Lourdes Mwea Hospital announces the launch of its nursing school programme. Applications for the 2024 intake are now open."` |
| `featured_image_id` | FK to wp_media_assets | (article hero image, 1200×630px for social) |

**Seed count:** Initial 5–10 articles (migrated from the archive); ongoing
articles added by Editors/Authors.

### New SEO-specific tables requiring seed data

The existing 80-table schema does not include dedicated SEO tables. The
following **7 new tables** should be added to support the SEO tool stack.
Each requires seed data at launch.

#### `wp_seo_meta` — per-page SEO metadata (extends `wp_pages`)

Stores SEO fields that are beyond what `wp_pages` already holds. This
table is the bridge between the content management schema and the SEO
plugin (Rank Math stores its data in `wp_postmeta`; this table is a
structured mirror for querying and reporting).

```sql
CREATE TABLE wp_seo_meta (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id         BIGINT UNSIGNED NOT NULL,
  focus_keyword   VARCHAR(191)    NULL,
  secondary_keywords TEXT         NULL,
  canonical_url   VARCHAR(512)    NULL,
  robots_directive ENUM('index,follow','noindex,follow','index,nofollow','noindex,nofollow')
                  NOT NULL DEFAULT 'index,follow',
  og_title        VARCHAR(255)    NULL,
  og_description  VARCHAR(320)    NULL,
  og_image_id     BIGINT UNSIGNED NULL,
  twitter_card_type ENUM('summary','summary_large_image','app','player')
                  NOT NULL DEFAULT 'summary_large_image',
  schema_type     VARCHAR(100)    NULL,
  schema_override JSON            NULL,
  redirect_target VARCHAR(512)    NULL,
  created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_seo_meta_page (page_id),
  KEY idx_seo_meta_keyword (focus_keyword),
  CONSTRAINT fk_seo_meta_page FOREIGN KEY (page_id)
    REFERENCES wp_pages (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_seo_meta_og_image FOREIGN KEY (og_image_id)
    REFERENCES wp_media_assets (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Seed data required:**

| Column | Seed value | Example |
|---|---|---|
| `focus_keyword` | Primary target keyword for the page | `"hospital in Mwea"`, `"nursing school Kenya"`, `"clinic days Mwea"` |
| `secondary_keywords` | Comma-separated secondary keywords | `"Kirinyaga hospital, Catholic hospital Mwea, maternity ward"` |
| `canonical_url` | Canonical URL (usually same as page URL) | `"https://ourladyoflourdesmweahospital.org/wards"` |
| `robots_directive` | Index/follow directive | `"index,follow"` (most pages), `"noindex,follow"` (admin, search, thank-you pages) |
| `og_title` | Social share title | (can mirror meta_title) |
| `og_description` | Social share description | (can mirror meta_desc) |
| `og_image_id` | Social share image (1200×630px) | FK to wp_media_assets |
| `schema_type` | Schema.org type for this page | `"Hospital"`, `"MedicalClinic"`, `"Physician"`, `"Event"`, `"Article"` |
| `redirect_target` | 301 redirect target (for migrated Joomla URLs) | New WordPress URL |

**Seed count:** One row per page (~25 pages at launch).

#### `wp_seo_keywords` — keyword research bank

Stores the target keyword set discovered through keyword research. This is
the "fixed keyword set" that all rank tracking, content optimization, and
trend analysis is measured against.

```sql
CREATE TABLE wp_seo_keywords (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  keyword_string  VARCHAR(255)    NOT NULL,
  search_volume   INT UNSIGNED    NULL,
  difficulty      DECIMAL(4,1)    NULL,
  search_intent   ENUM('informational','navigational','commercial','transactional')
                  NOT NULL DEFAULT 'informational',
  funnel_stage    ENUM('tofu','mofu','bofu') NOT NULL DEFAULT 'tofu',
  brand_nonbrand  ENUM('brand','non-brand') NOT NULL DEFAULT 'non-brand',
  keyword_group_id BIGINT UNSIGNED NULL,
  target_page_id  BIGINT UNSIGNED NULL,
  current_position DECIMAL(5,1)   NULL,
  first_seen_date DATE            NULL,
  last_checked    DATE            NULL,
  status          ENUM('active','paused','archived') NOT NULL DEFAULT 'active',
  created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_seo_keyword (keyword_string),
  KEY idx_seo_keyword_group (keyword_group_id),
  KEY idx_seo_keyword_intent (search_intent),
  CONSTRAINT fk_seo_keyword_page FOREIGN KEY (target_page_id)
    REFERENCES wp_pages (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Seed data required:**

| Column | Seed value | Example |
|---|---|---|
| `keyword_string` | The keyword | `"hospital in Mwea"`, `"Catholic hospital Kenya"`, `"nursing school application"`, `"clinic days schedule"`, `"maternity ward Kirinyaga"` |
| `search_volume` | Monthly search volume (from Keyword Planner) | `320`, `170`, `50` |
| `difficulty` | Keyword difficulty score (0–100, from Semrush/Ahrefs) | `35.2`, `12.8`, `5.0` |
| `search_intent` | Intent classification | `informational` (ward info), `navigational` (brand searches), `transactional` (apply, book) |
| `funnel_stage` | Funnel position | `tofu` (what is OLLMH), `mofu` (departments, services), `bofu` (apply, book appointment) |
| `brand_nonbrand` | Is this a brand search? | `brand` ("OLLMH", "Our Lady of Lourdes Mwea"), `non-brand` ("hospital in Mwea") |
| `target_page_id` | Which page this keyword targets | FK to wp_pages |
| `current_position` | Current ranking position (from Search Console) | `3.5`, `12.0`, `null` (not ranking yet) |

**Seed count:** 30–50 keywords at launch (the initial keyword research
set). Grows over time as new content is planned.

#### `wp_seo_keyword_groups` — keyword clustering

Groups keywords into topical clusters for content planning and silo
architecture.

```sql
CREATE TABLE wp_seo_keyword_groups (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  group_name  VARCHAR(191)    NOT NULL,
  topic_cluster VARCHAR(191)  NULL,
  description TEXT            NULL,
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_seo_keyword_group (group_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Seed data required:**

| Group name | Topic cluster | Keywords in group |
|---|---|---|
| `Hospital core` | Brand | "OLLMH", "Our Lady of Lourdes Mwea Hospital", "Catholic hospital Mwea" |
| `Departments` | Services | "maternity ward Mwea", "pediatrics Kirinyaga", "surgery hospital Kenya" |
| `Nursing school` | Education | "nursing school Kenya", "nursing school application", "medical school Mwea" |
| `Clinics` | Services | "clinic days Mwea", "outpatient department Kirinyaga", "OPD schedule" |
| `Community` | Outreach | "SMI community Kenya", "community health Mwea", "Catholic health outreach" |

**Seed count:** 5–10 keyword groups at launch.

#### `wp_seo_redirects` — 301 redirect map (Joomla → WordPress)

Stores the redirect map for the Joomla-to-WordPress migration. While the
Redirection plugin stores its own redirects in `wp_redirection_items`,
this table is a **structured, queryable record** of the migration mapping
that can be audited, exported, and re-imported.

```sql
CREATE TABLE wp_seo_redirects (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  source_url      VARCHAR(512)    NOT NULL,
  target_url      VARCHAR(512)    NOT NULL,
  redirect_type   SMALLINT UNSIGNED NOT NULL DEFAULT 301,
  status          ENUM('active','disabled') NOT NULL DEFAULT 'active',
  hit_count       INT UNSIGNED    NOT NULL DEFAULT 0,
  last_hit_at     TIMESTAMP       NULL,
  created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_seo_redirect_source (source_url),
  KEY idx_seo_redirect_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Seed data required:**

| source_url (old Joomla URL) | target_url (new WordPress URL) | redirect_type |
|---|---|---|
| `/index.php?option=com_content&view=article&id=1` | `/` | 301 |
| `/index.php?option=com_content&view=article&id=12` | `/about-ollmh-location` | 301 |
| `/index.php?option=com_content&view=article&id=20` | `/wards` | 301 |
| `/index.php?option=com_content&view=article&id=34` | `/clinic-days` | 301 |
| `/index.php?option=com_content&view=article&id=45` | `/nursing-school` | 301 |
| (every archived Joomla URL → its new WordPress equivalent) | | 301 |

**Seed count:** ~25–40 redirects (one per archived Joomla page).

#### `wp_seo_schema_config` — schema.org type configuration per page/CPT

Stores which schema.org type applies to each page or content type, and any
overrides for specific properties. This drives the JSON-LD output.

```sql
CREATE TABLE wp_seo_schema_config (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  page_id         BIGINT UNSIGNED NULL,
  cpt_name        VARCHAR(100)    NULL,
  schema_type     VARCHAR(100)    NOT NULL,
  properties      JSON            NULL,
  is_active       TINYINT(1)      NOT NULL DEFAULT 1,
  created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_seo_schema_page (page_id),
  KEY idx_seo_schema_cpt (cpt_name),
  CONSTRAINT fk_seo_schema_page FOREIGN KEY (page_id)
    REFERENCES wp_pages (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Seed data required:**

| page_id / cpt_name | schema_type | properties (JSON) |
|---|---|---|
| (home page) | `Hospital` | `{"name":"Our Lady of Lourdes Mwea Hospital","medicalSpecialty":"...","areaServed":"Mwea, Kirinyaga County"}` |
| (location page) | `Hospital` | (same as home, with full address/geo) |
| `department` (CPT) | `MedicalClinic` | `{"medicalSpecialty":"[from department category]"}` |
| `staff_member` (CPT) | `Physician` | `{"medicalSpecialty":"[from cadre]","credential":"[from qualification]"}` |
| `special_service` (CPT) | `MedicalProcedure` | `{"procedureType":"[from service name]"}` |
| `news_article` (CPT) | `NewsArticle` | `{"headline":"[from title]","datePublished":"[from published_at]"}` |
| `event` (CPT) | `Event` | `{"startDate":"[from event date]","location":"[from venue]"}` |
| (all pages) | `BreadcrumbList` | (auto-generated from menu hierarchy) |
| (site-wide) | `WebSite` + `SearchAction` | `{"url":"https://ourladyoflourdesmweahospital.org","potentialAction":{"@type":"SearchAction",...}}` |
| (site-wide) | `Organization` | `{"name":"...","url":"...","logo":"...","sameAs":["facebook.com/ollmh",...]}` |

**Seed count:** ~10–15 configuration rows (per CPT + per special page).

#### `wp_seo_gsc_daily` — Google Search Console daily performance (synced)

Stores daily Search Console performance data synced via the Search Console
API (through Site Kit or a custom integration). This is the "measured"
data layer — actual clicks, impressions, CTR, and position by query and
page.

```sql
CREATE TABLE wp_seo_gsc_daily (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  snapshot_date DATE           NOT NULL,
  query        VARCHAR(255)    NOT NULL,
  page_url     VARCHAR(512)    NOT NULL,
  device       ENUM('desktop','mobile','tablet') NOT NULL DEFAULT 'desktop',
  country      VARCHAR(10)     NULL,
  clicks       INT UNSIGNED    NOT NULL DEFAULT 0,
  impressions  INT UNSIGNED    NOT NULL DEFAULT 0,
  ctr           DECIMAL(6,4)   NOT NULL DEFAULT 0,
  avg_position DECIMAL(5,1)    NOT NULL DEFAULT 0,
  created_at   TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_seo_gsc_daily (snapshot_date, query, page_url, device, country),
  KEY idx_seo_gsc_date (snapshot_date),
  KEY idx_seo_gsc_query (query),
  KEY idx_seo_gsc_page (page_url)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Seed data required:** None at launch. This table is **populated by
automated daily sync** from the Search Console API after the site is
indexed. The "seed" is the API connection itself (configured via Site Kit).
Data begins flowing once Google starts crawling the site (typically 1–4
weeks after sitemap submission).

#### `wp_seo_audit_snapshots` — site audit history

Stores snapshots from periodic SEO audits (run via Rank Math's SEO
analysis, or external tools like Ahrefs/Screaming Frog).

```sql
CREATE TABLE wp_seo_audit_snapshots (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  audit_date      DATE            NOT NULL,
  audit_source    VARCHAR(100)    NOT NULL,
  health_score    DECIMAL(5,2)    NULL,
  total_issues    INT UNSIGNED    NOT NULL DEFAULT 0,
  critical_count  INT UNSIGNED    NOT NULL DEFAULT 0,
  warning_count   INT UNSIGNED    NOT NULL DEFAULT 0,
  passed_count    INT UNSIGNED    NOT NULL DEFAULT 0,
  details_json    JSON            NULL,
  created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_seo_audit_date (audit_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Seed data required:** None at launch. The first audit snapshot is
created when the first SEO audit is run (post-launch). The "seed" is
running the initial audit and storing the baseline.

### Seed data reference table (all tables)

| Table | Type | Seed data needed | Seed count | When to seed |
|---|---|---|---|---|
| `wp_pages` | Existing | meta_title, meta_desc, slug per page | ~25 rows | Pre-launch |
| `wp_media_assets` | Existing | alt_text per image | ~100–200 rows | Pre-launch + ongoing |
| `wp_departments` | Existing | slug, category per department | ~15–20 rows | Pre-launch |
| `wp_staff` | Existing | full_name, department_id, photo_media_id | ~30–50 rows | Pre-launch |
| `wp_location_info` | Existing | Full hospital NAP (name, address, phone) + GPS + hours | 1 row | Pre-launch (critical) |
| `wp_contact_channels` | Existing | Social media profile URLs | 2–5 rows | Pre-launch |
| `wp_news_articles` | Existing | slug, title, excerpt, featured_image_id | 5–10 rows | Launch + ongoing |
| `wp_events` | Existing | slug, title, excerpt, featured_image_id | 3–5 rows | Launch + ongoing |
| **`wp_seo_meta`** | **New** | focus_keyword, robots_directive, og_image, schema_type per page | ~25 rows | Pre-launch |
| **`wp_seo_keywords`** | **New** | keyword_string, search_volume, difficulty, intent, target_page | 30–50 rows | Pre-launch (keyword research) |
| **`wp_seo_keyword_groups`** | **New** | group_name, topic_cluster | 5–10 rows | Pre-launch |
| **`wp_seo_redirects`** | **New** | source_url (Joomla) → target_url (WordPress) | 25–40 rows | Pre-launch (migration) |
| **`wp_seo_schema_config`** | **New** | schema_type + properties per page/CPT | 10–15 rows | Pre-launch |
| **`wp_seo_gsc_daily`** | **New** | None — auto-populated by Search Console API sync | 0 at launch | Post-launch (auto-sync) |
| **`wp_seo_audit_snapshots`** | **New** | None — populated by first audit run | 0 at launch | Post-launch (first audit) |

**Total new tables: 7** (bringing the schema from 80 to 87 tables).
**Total seed rows at launch: ~250–350 rows** across existing + new tables.

---

## 3. Implementation guidance — how seed data drives SEO

### Seed → tool integration map

| Seed table | Tool(s) that consume it | How it drives SEO |
|---|---|---|
| `wp_pages.meta_title` / `meta_desc` | Rank Math (reads and outputs `<title>` and `<meta name="description">`) | Controls what appears in Google search results snippet — directly affects CTR |
| `wp_pages.slug` | Rank Math (canonical URL), Redirection (redirect matching), XML sitemap | Determines the URL structure that Google indexes — clean slugs improve ranking signals |
| `wp_media_assets.alt_text` | Rank Math (image SEO), Google Image Search | Enables image search visibility and improves page-level semantic relevance |
| `wp_location_info` | Custom JSON-LD (Hospital schema), Google Business Profile, Site Kit (Search Console geo data) | Populates Google Knowledge Panel, Maps listing, and local search results — the single most important local SEO seed |
| `wp_contact_channels` | Custom JSON-LD (Organization `sameAs` property) | Connects hospital entity to social profiles in Google's Knowledge Graph |
| `wp_departments` | Custom JSON-LD (MedicalClinic schema), Rank Math (per-CPT meta templates) | Enables department-specific rich results and local service queries |
| `wp_staff` | Custom JSON-LD (Physician schema), Rank Math (author meta) | Establishes E-E-A-T — Google sees credentialed medical professionals behind the content |
| `wp_seo_meta.focus_keyword` | Rank Math (content analysis scores against this keyword) | Drives on-page optimization — Rank Math scores content relevance to the target keyword |
| `wp_seo_meta.robots_directive` | Rank Math (outputs `<meta name="robots">`) | Controls which pages Google indexes (e.g., `noindex` on thank-you pages, search results) |
| `wp_seo_meta.og_image_id` | Rank Math (outputs `og:image` and `twitter:image`) | Controls the image shown when links are shared on Facebook, X, WhatsApp — affects social CTR |
| `wp_seo_meta.schema_type` | Custom JSON-LD (selects which schema template to render) | Determines which rich result type Google displays (Hospital, Physician, Event, Article) |
| `wp_seo_keywords` | Rank Math (focus keyword suggestions), Site Kit (Search Console performance matching), Metabase (trend analysis) | The fixed keyword set that all SEO performance is measured against — without it, you cannot track ranking progress |
| `wp_seo_keyword_groups` | Rank Math (content silo suggestions), content planning | Groups keywords into topical clusters — drives internal linking strategy and content silo architecture |
| `wp_seo_redirects` | Redirection plugin (bulk import), Rank Math (redirect monitor) | Preserves SEO equity from old Joomla URLs — without 301 redirects, all old inbound links and search rankings are lost |
| `wp_seo_schema_config` | Custom JSON-LD renderer (theme function) | Controls which schema.org type is output on each page/CPT — drives rich result eligibility |
| `wp_seo_gsc_daily` | Site Kit (dashboard display), Metabase (trend dashboards) | Provides measured SEO performance data — clicks, impressions, CTR, position by query — the ground truth for SEO effectiveness |
| `wp_seo_audit_snapshots` | Rank Math (SEO analysis), custom dashboard | Tracks SEO health over time — detects regressions when plugins update or content changes |

### Phase 1: Foundation seed data (pre-launch)

**Timeline:** Before the site goes live.

1. **Populate `wp_location_info`** with the hospital's full NAP (name,
   address, phone), GPS coordinates, and opening hours. This is the
   highest-priority seed — without it, local SEO cannot function.

2. **Populate `wp_contact_channels`** with all social media profile URLs.
   These feed the `Organization.sameAs` schema property.

3. **Populate `wp_seo_schema_config`** with the site-wide schema types:
   - `Organization` (site-wide, with `sameAs` from `wp_contact_channels`)
   - `WebSite` + `SearchAction` (site-wide, for sitelinks search box)
   - `Hospital` (home page + location page, with data from
     `wp_location_info`)
   - `MedicalClinic` (department CPT)
   - `Physician` (staff CPT)
   - `MedicalProcedure` (special service CPT)
   - `Event` (event CPT)
   - `NewsArticle` (news article CPT)
   - `BreadcrumbList` (all pages, auto-generated)

4. **Populate `wp_seo_redirects`** with the full Joomla → WordPress URL
   mapping. Import these into the Redirection plugin via CSV bulk import.

5. **Configure Rank Math** with:
   - Title templates per CPT (e.g., `%%title%% %%sep%% %%sitename%%`)
   - Meta description templates
   - Default social image (hospital logo on branded background, 1200×630px)
   - Breadcrumbs enabled
   - XML sitemap enabled (excludes `noindex` pages)
   - Schema module enabled
   - 404 monitor **disabled** (use Redirection plugin instead)

6. **Configure robots.txt** (via Rank Math or manually) with the
   recommended rules above.

7. **Install and connect Site Kit** to Google Search Console and GA4.
   Submit the XML sitemap URL in Search Console.

### Phase 2: Content seed data (launch)

**Timeline:** At launch, when content is being created.

1. **Populate `wp_seo_meta`** for every page:
   - Set `focus_keyword` for each page (from the keyword research bank)
   - Set `robots_directive` — `index,follow` for content pages,
     `noindex,follow` for thank-you pages, search results, admin pages
   - Set `og_image_id` for each major page (custom 1200×630px social image)
   - Set `schema_type` to match `wp_seo_schema_config`

2. **Populate `wp_seo_keywords`** with the initial keyword research set:
   - Use Google Keyword Planner to find search volumes for target keywords
   - Classify each keyword by intent (informational, navigational,
     transactional) and funnel stage (TOFU, MOFU, BOFU)
   - Link each keyword to its `target_page_id`
   - Set `current_position` from Search Console data (once available)

3. **Populate `wp_seo_keyword_groups`** with topical clusters:
   - Hospital core (brand keywords)
   - Departments (service keywords)
   - Nursing school (education keywords)
   - Clinics (appointment keywords)
   - Community (outreach keywords)

4. **Populate `wp_media_assets.alt_text`** for every image:
   - Write descriptive alt text (not keyword-stuffed)
   - Include context (e.g., "OLLMH maternity ward, Mwea" not just
     "maternity")

5. **Populate `wp_pages.meta_title` and `meta_desc`** for every page:
   - Meta title: 50–60 characters, include primary keyword + brand
   - Meta description: 150–160 characters, include primary keyword + CTA
   - Example: `"Wards & Inpatient Services | OLLMH Mwea Hospital"` /
     `"Our Lady of Lourdes Mwea Hospital offers general, maternity, and pediatric wards with 24/7 care. View bed availability and admission information."`

### Phase 3: Ongoing SEO operations (post-launch)

**Timeline:** Ongoing, after the site is live and indexed.

1. **Sync `wp_seo_gsc_daily`** daily from the Search Console API:
   - Use Site Kit's data or a custom WP-Cron job that calls the Search
     Console API
   - Store one row per query × page × device × country × date
   - This data powers the SEO dashboard and trend analysis

2. **Run monthly SEO audits** and store results in
   `wp_seo_audit_snapshots`:
   - Use Rank Math's SEO analysis tool
   - Optionally run Screaming Frog or Ahrefs site audit
   - Track health score, issue counts, and specific issues over time
   - Detect regressions (e.g., a plugin update breaks canonical tags)

3. **Update `wp_seo_keywords.current_position`** weekly:
   - Pull position data from Search Console (via `wp_seo_gsc_daily`)
   - Match keyword strings to queries
   - Update `last_checked` date

4. **Monitor `wp_seo_redirects`** for 404 hits:
   - The Redirection plugin logs 404 hits
   - Review weekly — any new 404 from an old Joomla URL means a redirect
     is missing
   - Add missing redirects and update `wp_seo_redirects`

5. **Monitor Broken Link Checker** for outbound link failures:
   - Review weekly
   - Fix or remove broken outbound links

6. **Review Search Console** (via Site Kit) for:
   - New queries driving traffic (add to `wp_seo_keywords`)
   - Pages with high impressions but low CTR (optimize meta title/desc)
   - Pages with indexing errors (fix and resubmit)
   - Core Web Vitals regressions (optimize with WP Rocket)

### Schema.org JSON-LD seed templates

#### Hospital schema (home page / location page)

```json
{
  "@context": "https://schema.org",
  "@type": "Hospital",
  "@id": "https://ourladyoflourdesmweahospital.org/#hospital",
  "name": "Our Lady of Lourdes Mwea Hospital",
  "description": "Faith-based Catholic hospital serving Mwea, Kirinyaga County, Kenya.",
  "url": "https://ourladyoflourdesmweahospital.org",
  "logo": "https://ourladyoflourdesmweahospital.org/wp-content/uploads/ollmh-logo.png",
  "image": "https://ourladyoflourdesmweahospital.org/wp-content/uploads/ollmh-building.jpg",
  "telephone": "+254700000000",
  "email": "info@ourladyoflourdesmweahospital.org",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Mwea",
    "addressLocality": "Mwea",
    "addressRegion": "Kirinyaga County",
    "addressCountry": "KE"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": -0.6703,
    "longitude": 37.3552
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  },
  "medicalSpecialty": ["GeneralPractice","Pediatric","Gynecology","Surgery"],
  "areaServed": {
    "@type": "AdministrativeArea",
    "name": "Mwea, Kirinyaga County, Kenya"
  },
  "parentOrganization": {
    "@type": "Organization",
    "name": "Sisters of Mary Immaculate (SMI)",
    "sameAs": [
      "https://facebook.com/ollmh",
      "https://youtube.com/@ollmh"
    ]
  }
}
```

**Seed sources:** `wp_location_info` (name, address, geo, phone, email,
hours), `wp_contact_channels` (social URLs for `sameAs`).

#### Physician schema (staff profile page)

```json
{
  "@context": "https://schema.org",
  "@type": "Physician",
  "name": "Dr. John Mwangi",
  "medicalSpecialty": "Surgery",
  "credential": "MBChB, MS (Surgery)",
  "hospitalAffiliation": {
    "@type": "Hospital",
    "name": "Our Lady of Lourdes Mwea Hospital",
    "url": "https://ourladyoflourdesmweahospital.org"
  },
  "image": "https://ourladyoflourdesmweahospital.org/wp-content/uploads/staff/dr-mwangi.jpg",
  "url": "https://ourladyoflourdesmweahospital.org/staff/dr-john-mwangi"
}
```

**Seed sources:** `wp_staff` (full_name, qualification/cadre, photo),
`wp_departments` (for medicalSpecialty mapping), `wp_location_info` (for
hospitalAffiliation).

#### Event schema (event page)

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Free Community Health Screening Day",
  "startDate": "2024-09-15T09:00",
  "endDate": "2024-09-15T16:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {
    "@type": "Hospital",
    "name": "Our Lady of Lourdes Mwea Hospital",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Mwea",
      "addressRegion": "Kirinyaga County",
      "addressCountry": "KE"
    }
  },
  "image": "https://ourladyoflourdesmweahospital.org/wp-content/uploads/events/health-screening.jpg",
  "description": "Free health screening for the Mwea community — blood pressure, blood sugar, BMI, and consultations.",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "KES",
    "availability": "https://schema.org/InStock",
    "url": "https://ourladyoflourdesmweahospital.org/events/health-screening-2024"
  }
}
```

**Seed sources:** `wp_events` (name, start/end date, description,
featured image), `wp_location_info` (venue address).

---

## 4. Admin sidebar SEO menu

Add a top-level **SEO** menu to the WordPress admin sidebar (see
[`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md) for the full sidebar structure):

| Submenu | Table(s) | Purpose |
|---|---|---|
| Dashboard | `wp_seo_gsc_daily`, `wp_seo_audit_snapshots` | Overview: current rankings, traffic, health score, recent 404s |
| Keywords | `wp_seo_keywords`, `wp_seo_keyword_groups` | Keyword research bank — add, edit, group, track positions |
| Redirects | `wp_seo_redirects` | Joomla → WordPress redirect map (mirrored in Redirection plugin) |
| Schema Config | `wp_seo_schema_config` | Configure which schema.org type applies to each page/CPT |
| Meta Manager | `wp_seo_meta` | Per-page SEO meta (focus keyword, robots directive, OG image, canonical) |
| Audit History | `wp_seo_audit_snapshots` | Historical SEO audit results with trend charts |
| GSC Data | `wp_seo_gsc_daily` | Search Console daily performance data (query × page × device) |
| Settings | — | Rank Math settings, Site Kit connection, robots.txt, sitemap config |

**Capability:** `manage_seo` (custom capability added to the core
**Editor** and **Administrator** roles via `add_cap()` — no custom roles
are created; see [`USER-ROLES.md`](./USER-ROLES.md)).

---

## 5. Recommended plugin versions

| Plugin | Min version | Notes |
|---|---|---|
| Rank Math | 3.0+ | Free version covers on-page SEO, sitemaps, schema, social. PRO adds keyword tracking, internal linking suggestions. |
| Site Kit by Google | 1.120+ | Free. Connects Search Console, GA4, PageSpeed Insights. |
| Redirection | 5.7+ | Free. 301 redirect manager + 404 monitor. |
| WP Rocket | 3.15+ | Premium (~$59/year). Page caching, CSS/JS optimization, lazy load, CDN. Alternative: LiteSpeed Cache (free, requires LiteSpeed server). |
| Broken Link Checker | 2.0+ | Free. Monitors outbound links. Configure for weekly scans. |
| Schema Markup for Medical Business | 1.1+ | Free (optional). Medical-specific schema if not using custom JSON-LD. |

**Total plugin count for SEO:** 4–6 plugins (Rank Math, Site Kit,
Redirection, WP Rocket, Broken Link Checker, optionally Schema Markup for
Medical Business).

**Performance note:** Each plugin adds PHP overhead. WP Rocket mitigates
this by caching pages — the cached HTML is served without executing PHP
for 95%+ of requests, so the plugin count has minimal impact on
front-end performance.
