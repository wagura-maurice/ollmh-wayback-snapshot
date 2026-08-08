# OLLMH Font Schema

Complete typography reference extracted from the archived OLLMH website
(Wayback Machine snapshot `20220319205345`).

The archived site ships **no web-font files** — there are no `@font-face`
declarations, no `.woff`/`.ttf`/`.eot`/`.otf`/`.svg` font binaries, no Google
Fonts `<link>` tags, and no `@import` font rules anywhere in the snapshot.
Every typeface is a **system-safe font stack** that relies on fonts already
installed on the visitor's operating system. This document catalogues every
font stack, where it is used, the accompanying type-scale (`font-size`,
`font-weight`, `font-style`, `line-height`), and a ready-to-use WordPress
`theme.json` typography configuration.

---

## Table of contents

1. [Font stacks](#font-stacks)
2. [Type scale (font-size)](#type-scale-font-size)
3. [Font weights](#font-weights)
4. [Font styles](#font-styles)
5. [Line heights](#line-heights)
6. [Inline (HTML) font usage by page](#inline-html-font-usage-by-page)
7. [WordPress theme.json typography](#wordpress-themejson-typography)
8. [WordPress CSS variables](#wordpress-css-variables)
9. [Recommendations for the rebuild](#recommendations-for-the-rebuild)

---

## Font stacks

Six distinct `font-family` stacks appear across the CSS and inline HTML
styles. All are generic, OS-installed families — no web fonts are loaded.

| # | Font stack | Type | Source | Used on |
|---|---|---|---|---|
| 1 | `"Trebuchet MS", Verdana, Arial, sans-serif` | Primary body | `css-bb8fd7…php.css` line 350 (`body`) | Global body text (all pages via template) |
| 2 | `verdana, sans-serif` | Footer | `css-bb8fd7…php.css` line 410 (`#footer .content`) | Footer content area |
| 3 | `Verdana, Geneva, Arial, Helvetica, sans-serif` | Finder | `media/com_finder/css/finder.css` line 62 | Joomla Smart Search autocomplete dropdown |
| 4 | `Verdana, Arial, Helvetica, sans-serif` | Inline body | Inline HTML on 9 pages | Body copy in article sections (wards, philosophy, contacts, admin, etc.) |
| 5 | `Tahoma, Helvetica, Arial, sans-serif` | Inline accent | Inline HTML on `index.html`, `contacts.html` | Headings / labels on home page and contacts |
| 6 | `HelveticaNeue, 'Helvetica Neue', Helvetica, Arial, 'Lucida Grande', sans-serif` | Pasted email | Inline HTML on `hr-capacity-staff.html` | Content pasted from an email client (Yahoo Mail `yiv2952568404` classes) |
| 7 | `"Calibri", "sans-serif"` | Pasted Word | Inline HTML on `index.html` (lines 1342–1488) | Content pasted from Microsoft Word (`mso-*` properties present) |
| 8 | `Arial, sans-serif` | Inline fallback | Inline HTML on `index.html`, `news-events.html`, `philosophy-of-care.html` | Misc inline blocks |
| 9 | `Tahoma, sans-serif` | Inline misc | Inline HTML on `news-events.html` line 291 | Single inline block on news-events page |

### Notes

- **Stack #1** is the canonical site font. It is declared on `body` in the
  main template stylesheet and cascades to every element that does not
  override it.
- **Stacks #4–#9** are all inline `style="font-family: …"` attributes inside
  individual article bodies. They are artefacts of content authors pasting
  from Word / email / other editors. They should **not** be carried into the
  rebuild — the WordPress theme should apply a single, consistent stack.
- **Stack #6** carries Yahoo Mail class names (`yiv2952568404`) and
  `mso-*` properties, confirming it was pasted from an email client.
- **Stack #7** carries `mso-ascii-font-family`, `mso-hansi-font-family`,
  `mso-fareast-font-family`, and `mso-*-theme-font` properties — definitive
  Microsoft Word paste markers.

---

## Type scale (font-size)

### From the main template CSS (`css-bb8fd7…php.css`)

| Size | Unit | Selector / line | Purpose |
|---|---|---|---|
| `0` / `0px` | px | lines 865, 891, 318, 304, 2004, 1777, 172 | Hidden / icon-only elements (text hidden for image-replacement) |
| `10px` | px | line 409 (`#footer .content`) | Footer body text |
| `11px` | px | line 584 | Small text (caption / meta) |
| `12px` | px | lines 351, 754, 1157, 1250 (`!important`), 1765 | Body text, nav sub-text, small UI |
| `13px` | px | `mod_xperttabs/…/common.css` line 37 | Tab labels |
| `14px` | px | line 1761 | Medium text |
| `15px` | px | lines 814, 1201 | Headings / feature text |
| `16px` | px | line 838 | Feature heading |
| `18px` | px | line 374 | Section heading |
| `20px` | px | lines 507, 754 area | Large heading |
| `2em` | em | line 1118 | Icon font size |
| `4em` | em | line 1122 | Icon font size |
| `5em` | em | line 1126 | Icon font size |
| `75%` | % | line 78 | Root reset (Joomla `html { font-size:75% }`) |
| `100%` | % | lines 62, 103 | Reset / normalise |
| `115%` | % | line 580 | Slightly enlarged text |

### From other CSS files

| Size | File | Purpose |
|---|---|---|
| `1px` | `xpertscroller.css` lines 59, 129 | Scroller hidden elements |
| `12px` | `xpertscroller.css` line 33 | Scroller body |
| `15px` | `xpertscroller.css` line 30 | Scroller heading |
| `100%` | `xpertslider.css` line 24 | Slider reset |
| `75%` / `100%` | `systems.css` line 7 | System reset |

### From inline HTML styles

| Size | Pages | Purpose |
|---|---|---|
| `33px !important` | All sub-pages (line 22) | Page `<title>`-style heading in the masthead area |
| `8.5pt` | `index.html` line 2310 | Small footer-style text |
| `9pt` | `news-events.html` line 288 | News listing body |
| `12pt` | `news-events.html` line 291 | News listing heading |
| `1em` | `index.html` line 1786, `philosophy-of-care.html` line 288 | Relative body text |
| `12px` / `15px` | `philosophy-of-care.html` line 291 | Inline body / heading |

---

## Font weights

| Weight | Source | Used on |
|---|---|---|
| `bold` | `css-bb8fd7…php.css` lines 579, 815, 1158, 1202 | Headings, strong labels, nav |
| `bold` | `media/com_finder/css/finder.css` lines 21, 48, 81, 112, 120 | Finder dropdown labels |
| `bold` | `libraries/expose/…/css-212ba4…php.css` (16 occurrences) | Expose framework admin UI labels |
| `bold` | `mod_xperttabs/…/common.css` line 37 | Tab labels |
| `bold` | `mod_maximenuck/…/maximenuck…54.css` line 598 | Menu item hover/active |
| `400` | `mod_maximenuck/…/maximenuck…54.css` line 492 | Menu item normal state |
| `normal` | `css-bb8fd7…php.css` line 376 | Section heading override |
| `normal !important` | `css-bb8fd7…php.css` line 1249 | Forced normal weight |
| `normal` | `mod_maximenuck/…/maximenuck…54.css` lines 323, 381, 631 | Menu item normal states |
| `normal` | `media/com_finder/css/finder.css` line 71 | Finder result item |

---

## Font styles

| Style | Source | Used on |
|---|---|---|
| `normal` | `css-bb8fd7…php.css` line 755 | Icon font normalise |
| `italic` | `libraries/expose/…/css-212ba4…php.css` lines 39, 45 | Expose framework admin UI (italic labels) |

Only two `italic` declarations exist in the entire CSS — both in the Expose
admin framework, not in the public-facing theme.

---

## Line heights

| Line height | Source | Used on |
|---|---|---|
| `0` | `css-bb8fd7…php.css` lines 79, 172, 304, 318, 1777, 2004 | Hidden / image-replacement elements |
| `0` / `normal` | `systems.css` line 7 (6 + 2 occurrences) | System reset |
| `12px` | `css-bb8fd7…php.css` line 756 | Small text |
| `20px` | `css-bb8fd7…php.css` lines 375, 507 | Section headings |
| `22px` | `css-bb8fd7…php.css` line 667 | Nav item |
| `70px` | `css-bb8fd7…php.css` line 812 | Feature block (icon row) |
| `1.7em` | `css-bb8fd7…php.css` line 352 | **Body text** (global, on `body`) |
| `1.8em` | `css-bb8fd7…php.css` line 359 | Lead / intro paragraph |

The global body `line-height` is **1.7em** — a comfortable, readable measure
that should be preserved in the rebuild.

---

## Inline (HTML) font usage by page

| Page | Font stack(s) used inline | Notes |
|---|---|---|
| `index.html` | `Tahoma, Helvetica, Arial, sans-serif`; `Verdana, Arial, Helvetica, sans-serif`; `Arial, sans-serif`; `"Calibri", "sans-serif"` | Calibri from Word paste; Tahoma for masthead headings |
| `wards.html` | `Verdana, Arial, Helvetica, sans-serif` (7×) | Consistent Verdana body |
| `philosophy-of-care.html` | `'Trebuchet MS', Verdana, Arial, sans-serif`; `Verdana, Arial, Helvetica, sans-serif`; `Arial, Helvetica, sans-serif` | Mixed stacks |
| `contacts.html` | `Tahoma, Helvetica, Arial, sans-serif`; `Verdana, Arial, Helvetica, sans-serif` | Two stacks |
| `about-ollmh-location.html` | `'Trebuchet MS', Verdana, Arial, sans-serif`; `Verdana, Arial, Helvetica, sans-serif` | Two stacks |
| `special-medical-services.html` | `Verdana, Arial, Helvetica, sans-serif` (3×) | Consistent Verdana |
| `smi-community.html` | `'Trebuchet MS', Verdana, Arial, sans-serif` | Single stack |
| `news-events.html` | `Arial, sans-serif`; `Tahoma, sans-serif` | Two stacks |
| `hr-capacity-staff.html` | `HelveticaNeue, 'Helvetica Neue', Helvetica, Arial, 'Lucida Grande', sans-serif` (3×) | Pasted from Yahoo Mail |
| `community-support.html` | `Verdana, Arial, Helvetica, sans-serif` (4×) | Consistent Verdana |
| `administration.html` | `Verdana, Arial, Helvetica, sans-serif` (5×) | Consistent Verdana |

---

## WordPress theme.json typography

Ready-to-paste `settings.typography` block for a WordPress block theme. Uses
the site's canonical stack and the extracted type scale.

```json
{
  "settings": {
    "typography": {
      "fluid": true,
      "fontFamilies": [
        {
          "slug": "body",
          "name": "Body (Trebuchet MS stack)",
          "fontFamily": "\"Trebuchet MS\", Verdana, Arial, sans-serif"
        },
        {
          "slug": "footer",
          "name": "Footer (Verdana stack)",
          "fontFamily": "Verdana, Arial, Helvetica, sans-serif"
        },
        {
          "slug": "heading",
          "name": "Heading (Tahoma stack)",
          "fontFamily": "Tahoma, Helvetica, Arial, sans-serif"
        },
        {
          "slug": "system-sans",
          "name": "System Sans",
          "fontFamily": "-apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif"
        }
      ],
      "fontSizes": [
        { "slug": "tiny",    "name": "Tiny",    "size": "10px" },
        { "slug": "small",   "name": "Small",   "size": "12px" },
        { "slug": "normal",  "name": "Normal",  "size": "14px" },
        { "slug": "medium",  "name": "Medium",  "size": "15px" },
        { "slug": "large",   "name": "Large",   "size": "18px" },
        { "slug": "x-large", "name": "X-Large", "size": "20px" },
        { "slug": "xx-large","name": "XX-Large","size": "33px" }
      ],
      "fontStyle": true,
      "fontWeight": true,
      "lineHeight": true,
      "textColumns": false,
      "textDecoration": true,
      "textTransform": true
    },
    "styles": {
      "typography": {
        "fontFamily": "var(--wp--preset--font-family--body)",
        "fontSize": "12px",
        "lineHeight": "1.7"
      },
      "elements": {
        "heading": {
          "typography": {
            "fontFamily": "var(--wp--preset--font-family--heading)",
            "fontWeight": "bold"
          }
        },
        "h1": { "typography": { "fontSize": "33px" } },
        "h2": { "typography": { "fontSize": "20px" } },
        "h3": { "typography": { "fontSize": "18px" } },
        "h4": { "typography": { "fontSize": "16px" } },
        "h5": { "typography": { "fontSize": "15px" } },
        "h6": { "typography": { "fontSize": "14px" } }
      }
    }
  }
}
```

---

## WordPress CSS variables

```css
:root {
  /* Font families */
  --font-body:    "Trebuchet MS", Verdana, Arial, sans-serif;
  --font-footer:  Verdana, Arial, Helvetica, sans-serif;
  --font-heading: Tahoma, Helvetica, Arial, sans-serif;
  --font-finder:  Verdana, Geneva, Arial, Helvetica, sans-serif;

  /* Font sizes */
  --fs-tiny:    10px;
  --fs-small:   11px;
  --fs-body:    12px;
  --fs-tabs:    13px;
  --fs-medium:  14px;
  --fs-large:   15px;
  --fs-xlarge:  16px;
  --fs-h3:      18px;
  --fs-h2:      20px;
  --fs-h1:      33px;

  /* Font weights */
  --fw-normal:  400;
  --fw-bold:    bold;

  /* Line heights */
  --lh-body:    1.7;
  --lh-lead:    1.8;
  --lh-tight:   20px;
  --lh-nav:     22px;
}
```

---

## Recommendations for the rebuild

1. **Drop the pasted-font stacks.** Stacks #6 (HelveticaNeue / Yahoo Mail)
   and #7 (Calibri / Word) are paste artefacts. They should not appear in the
   WordPress theme. When migrating content, strip inline `font-family`
   styles so the theme's stack applies uniformly.

2. **Standardise on two stacks.** Use the **body** stack
   (`"Trebuchet MS", Verdana, Arial, sans-serif`) for all body text and the
   **heading** stack (`Tahoma, Helvetica, Arial, sans-serif`) for headings.
   Add a modern **system-sans** fallback as the first choice for better
   rendering on macOS / iOS / modern Windows, with Trebuchet MS as the
   named fallback:
   ```css
   --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Trebuchet MS", Verdana, Arial, sans-serif;
   ```

3. **Preserve the 1.7 line-height.** The global `line-height: 1.7em` on
   `body` gives the site its readable, airy feel. Keep it as the body
   line-height in `theme.json`.

4. **Preserve the 33px masthead heading.** Every sub-page uses
   `font-size: 33px !important` for its page-title heading. Map this to the
   `h1` block style in `theme.json`.

5. **Consider loading a web font.** The original site loads no web fonts,
   which keeps it fast but means rendering varies by OS. For the rebuild,
   consider loading a single Google Font (e.g. *Open Sans* or *Source Sans
   3*) with `font-display: swap` to get consistent rendering while
   preserving the sans-serif, humanist character of Trebuchet MS. Bundle
   the font locally (no third-party request) for privacy and performance.

6. **Clean up `!important`.** The archive uses `font-size: 12px !important`
   and `font-weight: normal !important` in a few places. Avoid `!important`
   in the WordPress theme — use CSS specificity instead.
