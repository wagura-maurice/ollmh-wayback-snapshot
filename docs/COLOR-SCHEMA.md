# Color Schema (WordPress Theme)

> This document defines the **complete color palette** extracted from the
> archived OLLMH website snapshot, organized for use in developing a new
> WordPress theme. Every color is listed with its hex code, the CSS source
> file and selector it was extracted from, its role in the design system, and
> a recommended WordPress theme usage.
>
> Colors are grouped into: **Primary**, **Secondary**, **Accent**, **Background**,
> **Text**, **Border/Divider**, and **Inline Content** colors.

---

## Source files analyzed

All colors were extracted from the following CSS and HTML files in the local
snapshot:

| File | Role |
| --- | --- |
| `templates/tx_finnix/css/styles/css-d966e87bd26563e9c2ea496587cbfd40.php.css` | Main template theme styles (style1) — the primary color source |
| `templates/tx_finnix/css/css-bb8fd7a644f50328d257aa61a147f0436f22228bde33e84fa48b98b6de11e47e5f44c95ea87e1dad42d8bc944398778b.php.css` | Template framework/base CSS |
| `templates/tx_finnix/css/xpertscroller.css` | News scroller module |
| `modules/mod_xperttabs/assets/css/style1.css` | Xpert Tabs module |
| `modules/mod_xpertslider/assets/css/xpertslider.css` | Image slider module |
| `modules/mod_maximenuck/themes/custom/css/maximenuck_maximenuck54.css` | Mega-menu navigation module |
| `libraries/expose/interface/css/css-212ba457b58d989b10035c9ea5b91852.php.css` | Expose framework interface |
| `index.html` (inline styles) | Inline content colors in page body |

---

## Primary colors

The primary colors are the dominant brand colors used for the header bar,
footer, menu hover states, and primary buttons. They form the backbone of the
site's visual identity.

| Role | Hex | CSS source | Selector / context | WordPress usage |
| --- | --- | --- | --- | --- |
| **Primary 1 — Deep navy** | `#001A55` | `styles/css-d966...php.css` | `#roof` (top bar background), `#menu .megamenu ul.level-0 > li:hover > a.mega` (menu hover/active background), `#menu ul.level-1 > li.mega > a.mega:hover` (dropdown hover background), `.xslider_wrap .xslider_pag .xslider_pag_ul li` (slider pagination inactive) | Header bar background, menu hover/active states, slider pagination dots |
| **Primary 2 — Dark navy** | `#122348` | `styles/css-d966...php.css` | `#bottom` (footer background), `#footer` (footer section background) | Footer background |
| **Primary 3 — Darkest navy** | `#07112E` | `styles/css-d966...php.css` | `#copyright` (copyright bar background) | Footer bottom bar / copyright strip |
| **Primary 4 — Button blue** | `#0064CD` | `styles/css-d966...php.css` | `.btn.primary` (background-color, border-color) | Primary button background, CTA button |
| **Primary 5 — Button blue light** | `#049CDB` | `styles/css-d966...php.css` | `.btn.primary` (gradient from-color) | Primary button gradient top (gradient: `#049CDB → #0064CD`) |

### Primary gradient

The primary button uses a vertical gradient:

```
linear-gradient(#049CDB, #0064CD)
```

**WordPress CSS variables:**

```css
--color-primary-1: #001A55;   /* deep navy — header bar, menu hover */
--color-primary-2: #122348;   /* dark navy — footer background */
--color-primary-3: #07112E;   /* darkest navy — copyright strip */
--color-primary-4: #0064CD;   /* button blue — primary button */
--color-primary-5: #049CDB;   /* button blue light — gradient top */
--gradient-primary: linear-gradient(#049CDB, #0064CD);
```

---

## Secondary colors

Secondary colors support the primary palette, used for the mega-menu
navigation bar, dropdown backgrounds, and link colors.

| Role | Hex | CSS source | Selector / context | WordPress usage |
| --- | --- | --- | --- | --- |
| **Secondary 1 — Menu blue** | `#0272A7` | `maximenuck_maximenuck54.css` | Menu bar gradient top (`linear-gradient(top, #0272a7 0%, #013953 100%)`) | Navigation bar gradient top |
| **Secondary 2 — Menu dark blue** | `#013953` | `maximenuck_maximenuck54.css` | Menu bar gradient bottom (`linear-gradient(top, #0272a7 0%, #013953 100%)`) | Navigation bar gradient bottom |
| **Secondary 3 — Menu hover blue** | `#015B86` | `maximenuck_maximenuck54.css` | Menu item hover color, dropdown arrow border color | Menu item hover/focus state |
| **Secondary 4 — Menu accent blue** | `#029FEB` | `maximenuck_maximenuck54.css` | Menu item active/hover accent, dropdown arrow active color | Menu active item accent |
| **Secondary 5 — Link blue** | `#3E779D` | `styles/css-d966...php.css` | `a` (global link color) | Body text links |
| **Secondary 6 — Footer title bg** | `#102041` | `styles/css-d966...php.css` | `#bottom .title` (footer column heading background) | Footer column heading background |

### Secondary gradient

The mega-menu navigation bar uses a vertical gradient:

```
linear-gradient(top, #0272A7 0%, #013953 100%)
```

**WordPress CSS variables:**

```css
--color-secondary-1: #0272A7;  /* menu blue — nav bar gradient top */
--color-secondary-2: #013953;  /* menu dark blue — nav bar gradient bottom */
--color-secondary-3: #015B86;  /* menu hover blue */
--color-secondary-4: #029FEB;  /* menu accent blue */
--color-secondary-5: #3E779D;  /* link blue — body text links */
--color-secondary-6: #102041;  /* footer heading background */
--gradient-nav: linear-gradient(to bottom, #0272A7 0%, #013953 100%);
```

---

## Accent colors

Accent colors are the high-visibility "pop" colors used sparingly for
headings on dark backgrounds, active tab states, slider pagination active
dots, and highlights.

| Role | Hex | CSS source | Selector / context | WordPress usage |
| --- | --- | --- | --- | --- |
| **Accent 1 — Gold/yellow** | `#FFDD47` | `styles/css-d966...php.css`, `xpertscroller.css` | `.title, .title a` (section heading text on dark bg), `.xslider_wrap .xslider_pag .xslider_pag_ul li.xslidercurrent` (active slider dot), `.custom .xt-nav ul li a.current` (active tab text), `.basic_h .navi a:hover` / `.active` (scroller nav active) | Section headings on dark backgrounds, active states, highlights |
| **Accent 2 — Gold (variant)** | `#F9DE00` | `styles/css-d966...php.css` | `.title, .title a` (alternate heading color), `#component .col-2 article header h2` (article heading) | Section/article headings (interchangeable with `#FFDD47`) |
| **Accent 3 — Bright yellow** | `#FFEC4F` | `css-bb8fd7...php.css` | `color: #ffec4f` (highlight text), `border-right: 1px solid #ffec4f` (accent border) | Highlight text, accent borders on dark backgrounds |

> `#FFDD47`, `#F9DE00`, and `#FFEC4F` are very close gold/yellow shades used
> interchangeably across different CSS files. For the WordPress theme,
> standardize on **`#FFDD47`** as the canonical accent gold, with `#F9DE00`
> and `#FFEC4F` as documented variants.

**WordPress CSS variables:**

```css
--color-accent-1: #FFDD47;   /* gold — headings on dark, active states */
--color-accent-2: #F9DE00;   /* gold variant — article headings */
--color-accent-3: #FFEC4F;   /* bright yellow — highlight text/borders */
```

---

## Background colors

Background colors are used for the page body, content areas, cards, inputs,
and alternating rows.

| Role | Hex | CSS source | Selector / context | WordPress usage |
| --- | --- | --- | --- | --- |
| **BG 1 — Page background** | `#E7E7E7` | `styles/css-d966...php.css` | `body` (background color behind bg.jpg image) | Page body background |
| **BG 2 — Light gray** | `#F5F5F5` | `css-bb8fd7...php.css`, `xpertscroller.css`, `css-212ba...php.css` | `background: #f5f5f5` (code blocks, well backgrounds, zebra list alternating rows) | Card backgrounds, alternating rows, pre/code blocks |
| **BG 3 — Very light gray** | `#F6F6F6` | `styles/css-d966...php.css` | `#footer` (footer text color — used as text on dark bg, not a background) | Footer text color on dark background |
| **BG 4 — Off-white** | `#F9F9F9` | `style1.css` | Tab content background | Tab panel content background |
| **BG 5 — Lighter gray** | `#F7F7F7` | `style1.css` | Tab content alt background | Tab panel alt background |
| **BG 6 — White** | `#FFFFFF` (`#FFF`) | All CSS files | `background: #fff` (content areas, inputs, cards, slider items) | Content area background, cards, inputs, modals |
| **BG 7 — Dropdown light blue** | `#EDF9FF` | `maximenuck_maximenuck54.css` | Dropdown menu hover background | Menu dropdown hover highlight |
| **BG 8 — Dropdown gray** | `#F4F4F4` | `maximenuck_maximenuck54.css` | Dropdown item background, gradient top (`#F4F4F4 → #EEEEEE`) | Menu dropdown item background |
| **BG 9 — Dropdown gray dark** | `#EEEEEE` | `maximenuck_maximenuck54.css` | Dropdown gradient bottom, border color, arrow color | Menu dropdown gradient bottom, borders |

**WordPress CSS variables:**

```css
--color-bg-page:      #E7E7E7;  /* page body background */
--color-bg-light:     #F5F5F5;  /* card/alt-row background */
--color-bg-footer-text: #F6F6F6; /* footer text on dark bg */
--color-bg-tab:       #F9F9F9;  /* tab content background */
--color-bg-tab-alt:   #F7F7F7;  /* tab content alt background */
--color-bg-white:     #FFFFFF;  /* content area, cards, inputs */
--color-bg-dropdown:  #EDF9FF;  /* dropdown hover highlight */
--color-bg-menu-item: #F4F4F4;  /* dropdown item background */
--color-bg-menu-alt:  #EEEEEE;  /* dropdown gradient bottom */
```

---

## Text colors

Text colors are used for body copy, headings on light backgrounds, menu
labels, and muted/secondary text.

| Role | Hex | CSS source | Selector / context | WordPress usage |
| --- | --- | --- | --- | --- |
| **Text 1 — Body text** | `#324751` | `styles/css-d966...php.css` | `body` (global text color) | Body text — default paragraph color |
| **Text 2 — Dark gray** | `#333333` (`#333`) | `css-bb8fd7...php.css`, `systems.css` | `color: #333` (headings, inputs, article text) | Headings, form input text, article body |
| **Text 3 — Medium gray** | `#444444` (`#444`) | `css-bb8fd7...php.css` | `box-shadow: inset 0 1px 2px #444` (input shadow) | Input field inner shadow |
| **Text 4 — Gray** | `#555555` (`#555`) | `maximenuck_maximenuck54.css`, `index.html` | Menu text color, inline content text | Secondary/muted text |
| **Text 5 — Medium-light gray** | `#666666` | `maximenuck_maximenuck54.css` | Menu description text | Menu item descriptions |
| **Text 6 — Light gray** | `#777777` | `maximenuck_maximenuck54.css` | Menu border color, dropdown border | Muted text, borders |
| **Text 7 — Muted gray** | `#676767` | `index.html` (inline) | `color: #676767` (inline paragraph text — 7 occurrences) | Inline body text variant |
| **Text 8 — Near-black** | `#161616` | `maximenuck_maximenuck54.css` | Menu text color, dropdown arrow color | Menu text on light dropdown |
| **Text 9 — Very dark** | `#222222` (`#222`) | `style1.css` | Tab heading text | Tab heading text |
| **Text 10 — Black** | `#000000` (`#000`) | All CSS files | `color: #000` (scroller item headings, tab nav text) | Scroller item headings, tab nav inactive text |
| **Text 11 — White** | `#FFFFFF` (`#FFF`) | All CSS files | `color: #fff` (text on dark backgrounds — menu hover, copyright, footer) | Text on dark backgrounds (header, footer, buttons) |

**WordPress CSS variables:**

```css
--color-text-body:    #324751;  /* body text — default */
--color-text-heading: #333333;  /* headings on light bg */
--color-text-muted:   #676767;  /* muted/secondary text */
--color-text-light:   #F6F6F6;  /* text on dark backgrounds (footer) */
--color-text-white:   #FFFFFF;  /* text on dark backgrounds (header, buttons) */
--color-text-black:   #000000;  /* scroller headings, tab nav */
```

---

## Border / divider colors

| Role | Hex | CSS source | Selector / context | WordPress usage |
| --- | --- | --- | --- | --- |
| **Border 1 — Light gray** | `#DDDDDD` (`#DDD`) | `css-bb8fd7...php.css`, `xpertscroller.css`, `style1.css`, `finder.css` | `border: 1px solid #ddd` (input borders, card borders, zebra list borders) | Input/card borders, dividers |
| **Border 2 — Very light gray** | `#EFEFEF` | `styles/css-d966...php.css` | `.block` (block border-left color) | Block separators |
| **Border 3 — Light gray alt** | `#EAEAEA` | `style1.css` | Tab content border, tab nav border | Tab panel borders |
| **Border 4 — Light gray alt 2** | `#DCDCDC` | `style1.css` | Tab content alt border | Tab panel alt borders |
| **Border 5 — Medium light gray** | `#C4D3DF` | `css-212ba...php.css` | Interface element border | Framework interface borders |
| **Border 6 — Gray** | `#B7B7B7` | `xpertslider.css` | Slider border color | Image slider borders |
| **Border 7 — Light gray** | `#E5E5E5` | `css-212ba...php.css` | Interface element border | Framework interface borders |
| **Border 8 — Lighter gray** | `#E6E6E6` | `xpertslider.css` | Slider nav background | Slider navigation background |
| **Border 9 — Medium gray** | `#BBBBBB` | `maximenuck_maximenuck54.css` | Dropdown gradient bottom (`#EEEEEE → #BBBBBB`) | Dropdown gradient bottom |

**WordPress CSS variables:**

```css
--color-border-default: #DDDDDD;  /* input/card borders */
--color-border-light:   #EFEFEF;  /* block separators */
--color-border-tab:     #EAEAEA;  /* tab panel borders */
```

---

## Inline content colors

These colors appear in inline `style` attributes within the HTML content of
`index.html`. They are used for specific content elements (call-to-action
text, emphasis, links) and should be preserved as content-level styles in the
WordPress editor.

| Role | Hex | CSS source | Context | WordPress usage |
| --- | --- | --- | --- | --- |
| **Inline 1 — Orange** | `#E46C0A` | `index.html` (inline, 2 occurrences) | `color: #e46c0a` (highlighted call-to-action text) | CTA / highlight text in content |
| **Inline 2 — Dark red** | `#C00000` | `index.html` (inline, 2 occurrences) | `color: #c00000` (emphasized text) | Emphasis / alert text in content |
| **Inline 3 — Blue link** | `#0000CC` | `index.html` (inline, 2 occurrences) | `color: #0000cc` (inline link text) | Inline content links |
| **Inline 4 — Red** | `red` | `index.html` (inline, 1 occurrence) | `color: red` (single inline emphasis) | Inline emphasis (use `#FF0000`) |

**WordPress CSS variables:**

```css
--color-inline-orange: #E46C0A;  /* CTA / highlight text */
--color-inline-red:    #C00000;  /* emphasis / alert text */
--color-inline-link:   #0000CC;  /* inline content links */
```

---

## RGBA / opacity values

These semi-transparent colors are used for shadows, overlays, and hover
effects.

| Value | CSS source | Context | WordPress usage |
| --- | --- | --- | --- |
| `rgba(0, 0, 0, 0.25)` | `styles/css-d966...php.css`, `css-bb8fd7...php.css` | Button text-shadow, box-shadow | Button shadows, overlay shadows |
| `rgba(0, 0, 0, 0.1)` | `styles/css-d966...php.css` | Button border-color rgba variant | Button border |
| `rgba(0, 0, 0, 0.5)` | `css-bb8fd7...php.css`, `xpertslider.css` | Box shadow, slider overlay | Dark overlays |
| `rgba(255, 255, 255, 0.1)` | `css-bb8fd7...php.css` | Button hover highlight | White overlay on hover |
| `rgba(255, 255, 255, 0.5)` | `xpertscroller.css` | Scroller nav text shadow | Light text shadow |
| `rgba(39, 39, 39, 0.5)` | `xpertscroller.css` | Scroller active nav box-shadow | Active nav shadow |
| `rgba(0, 0, 0, 0.2)` | `xpertslider.css` | Slider box-shadow | Slider shadow |

---

## Complete WordPress theme color palette

The following is the consolidated palette ready for use in a WordPress theme
`style.css` or `theme.json`. Colors are organized by role with CSS custom
property names following the `--color-{role}-{variant}` convention.

```css
:root {
  /* === Primary (brand) === */
  --color-primary:           #001A55;  /* deep navy — header bar, menu hover */
  --color-primary-dark:      #07112E;  /* darkest navy — copyright strip */
  --color-primary-footer:    #122348;  /* dark navy — footer background */
  --color-primary-heading:   #102041;  /* footer heading background */
  --color-primary-button:    #0064CD;  /* button blue — primary button */
  --color-primary-button-l:  #049CDB;  /* button blue light — gradient top */
  --gradient-primary-button: linear-gradient(#049CDB, #0064CD);

  /* === Secondary (navigation) === */
  --color-nav-blue:          #0272A7;  /* nav bar gradient top */
  --color-nav-dark-blue:     #013953;  /* nav bar gradient bottom */
  --color-nav-hover:         #015B86;  /* menu item hover */
  --color-nav-accent:        #029FEB;  /* menu active accent */
  --color-link:              #3E779D;  /* body text links */
  --gradient-nav:            linear-gradient(to bottom, #0272A7 0%, #013953 100%);

  /* === Accent (high-visibility) === */
  --color-accent-gold:       #FFDD47;  /* headings on dark, active states */
  --color-accent-gold-alt:   #F9DE00;  /* article headings variant */
  --color-accent-yellow:     #FFEC4F;  /* highlight text/borders */

  /* === Background === */
  --color-bg-page:           #E7E7E7;  /* page body background */
  --color-bg-light:          #F5F5F5;  /* card/alt-row background */
  --color-bg-tab:            #F9F9F9;  /* tab content background */
  --color-bg-tab-alt:        #F7F7F7;  /* tab content alt */
  --color-bg-white:          #FFFFFF;  /* content area, cards, inputs */
  --color-bg-dropdown:       #EDF9FF;  /* dropdown hover highlight */
  --color-bg-menu-item:      #F4F4F4;  /* dropdown item background */
  --color-bg-menu-alt:       #EEEEEE;  /* dropdown gradient bottom */

  /* === Text === */
  --color-text-body:         #324751;  /* body text — default */
  --color-text-heading:      #333333;  /* headings on light bg */
  --color-text-muted:        #676767;  /* muted/secondary text */
  --color-text-footer:       #F6F6F6;  /* text on dark (footer) */
  --color-text-white:        #FFFFFF;  /* text on dark (header, buttons) */
  --color-text-black:        #000000;  /* scroller headings, tab nav */
  --color-text-menu:         #161616;  /* menu text on light dropdown */
  --color-text-menu-desc:    #666666;  /* menu description text */

  /* === Border / divider === */
  --color-border:            #DDDDDD;  /* input/card borders */
  --color-border-light:      #EFEFEF;  /* block separators */
  --color-border-tab:        #EAEAEA;  /* tab panel borders */
  --color-border-slider:     #B7B7B7;  /* slider borders */

  /* === Inline content === */
  --color-inline-orange:     #E46C0A;  /* CTA / highlight text */
  --color-inline-red:        #C00000;  /* emphasis / alert text */
  --color-inline-link:       #0000CC;  /* inline content links */

  /* === Shadows / overlays === */
  --shadow-button:           0 -1px 0 rgba(0, 0, 0, 0.25);
  --shadow-overlay-dark:     rgba(0, 0, 0, 0.25);
  --shadow-overlay-light:    rgba(255, 255, 255, 0.1);
}
```

### WordPress `theme.json` palette

For block themes using `theme.json`, the following palette maps the extracted
colors to WordPress slug/name pairs:

```json
{
  "version": 2,
  "settings": {
    "color": {
      "palette": [
        { "slug": "primary",          "color": "#001A55", "name": "Primary (Deep Navy)" },
        { "slug": "primary-dark",     "color": "#07112E", "name": "Primary Dark (Darkest Navy)" },
        { "slug": "primary-footer",   "color": "#122348", "name": "Footer Navy" },
        { "slug": "primary-heading",  "color": "#102041", "name": "Footer Heading Navy" },
        { "slug": "primary-button",   "color": "#0064CD", "name": "Button Blue" },
        { "slug": "primary-button-l", "color": "#049CDB", "name": "Button Blue Light" },
        { "slug": "nav-blue",         "color": "#0272A7", "name": "Navigation Blue" },
        { "slug": "nav-dark-blue",    "color": "#013953", "name": "Navigation Dark Blue" },
        { "slug": "nav-hover",        "color": "#015B86", "name": "Navigation Hover Blue" },
        { "slug": "nav-accent",       "color": "#029FEB", "name": "Navigation Accent Blue" },
        { "slug": "link",             "color": "#3E779D", "name": "Link Blue" },
        { "slug": "accent-gold",      "color": "#FFDD47", "name": "Accent Gold" },
        { "slug": "accent-gold-alt",  "color": "#F9DE00", "name": "Accent Gold Alt" },
        { "slug": "accent-yellow",    "color": "#FFEC4F", "name": "Accent Yellow" },
        { "slug": "bg-page",          "color": "#E7E7E7", "name": "Page Background" },
        { "slug": "bg-light",         "color": "#F5F5F5", "name": "Light Background" },
        { "slug": "bg-white",         "color": "#FFFFFF", "name": "White" },
        { "slug": "bg-dropdown",      "color": "#EDF9FF", "name": "Dropdown Hover" },
        { "slug": "bg-menu-item",     "color": "#F4F4F4", "name": "Menu Item Background" },
        { "slug": "text-body",        "color": "#324751", "name": "Body Text" },
        { "slug": "text-heading",     "color": "#333333", "name": "Heading Text" },
        { "slug": "text-muted",       "color": "#676767", "name": "Muted Text" },
        { "slug": "text-footer",      "color": "#F6F6F6", "name": "Footer Text" },
        { "slug": "text-white",       "color": "#FFFFFF", "name": "White Text" },
        { "slug": "border",           "color": "#DDDDDD", "name": "Border" },
        { "slug": "border-light",     "color": "#EFEFEF", "name": "Light Border" },
        { "slug": "inline-orange",    "color": "#E46C0A", "name": "Inline Orange" },
        { "slug": "inline-red",       "color": "#C00000", "name": "Inline Red" },
        { "slug": "inline-link",      "color": "#0000CC", "name": "Inline Link" }
      ]
    }
  }
}
```

---

## Color usage map

This table shows which colors are used in which structural areas of the site,
providing a quick reference for theme development.

| Site area | Background | Text | Accent | Border |
| --- | --- | --- | --- | --- |
| **Page body** | `#E7E7E7` | `#324751` | — | — |
| **Top bar (`#roof`)** | `#001A55` | `#FFFFFF` | — | — |
| **Navigation bar** | gradient `#0272A7 → #013953` | `#FFFFFF` / `#161616` | `#029FEB` (active) | `#777777` |
| **Menu hover/active** | `#001A55` | `#FFFFFF` | — | — |
| **Menu dropdown** | `#F4F4F4 → #EEEEEE` | `#161616` / `#666666` | `#015B86` (hover) | `#777777` |
| **Content area** | `#FFFFFF` | `#333333` | `#FFDD47` (headings on dark) | `#DDDDDD` |
| **Section headings (light bg)** | — | `#333333` | — | — |
| **Section headings (dark bg)** | — | `#FFDD47` / `#F9DE00` | — | — |
| **Primary button** | gradient `#049CDB → #0064CD` | `#FFFFFF` | — | `#0064CD` |
| **Footer (`#bottom`)** | `#122348` | `#F6F6F6` | `#FFDD47` (column headings) | — |
| **Footer heading bg** | `#102041` | `#FFDD47` | — | — |
| **Copyright strip** | `#07112E` | `#FFFFFF` | — | — |
| **Links (body)** | — | `#3E779D` | — | — |
| **Links (inline content)** | — | `#0000CC` | — | — |
| **Cards / inputs** | `#FFFFFF` / `#F5F5F5` | `#333333` | — | `#DDDDDD` |
| **Tab nav (inactive)** | — | `#000000` | — | `#EAEAEA` |
| **Tab nav (active)** | — | `#FFDD47` | — | — |
| **Slider pagination (inactive)** | `#001A55` | — | — | — |
| **Slider pagination (active)** | `#FFDD47` | — | — | — |

---

## Color hierarchy summary

The OLLMH color system follows a clear hierarchy:

1. **Navy blues** (`#001A55`, `#122348`, `#07112E`, `#102041`) — the dominant
   brand family, used for the header bar, footer, copyright strip, and menu
   hover states. These convey trust, professionalism, and the Catholic
   institutional identity.
2. **Bright blues** (`#0064CD`, `#049CDB`, `#0272A7`, `#013953`, `#015B86`,
   `#029FEB`) — the interactive family, used for buttons, the navigation bar
   gradient, links, and menu hover/active states. These provide visual energy
   and call attention to clickable elements.
3. **Gold/yellow** (`#FFDD47`, `#F9DE00`, `#FFEC4F`) — the single accent
   family, used sparingly for headings on dark backgrounds, active tab states,
   and slider pagination. This is the "pop" color that creates contrast
   against the navy.
4. **Grays** (`#E7E7E7`, `#F5F5F5`, `#F6F6F6`, `#EFEFEF`, `#DDDDDD`,
   `#EAEAEA`, `#676767`, `#333333`) — the neutral family, used for page
   backgrounds, content areas, borders, and muted text.
5. **Inline content colors** (`#E46C0A`, `#C00000`, `#0000CC`) — used only
   within body content for emphasis, alerts, and inline links; not part of the
   structural design system.
