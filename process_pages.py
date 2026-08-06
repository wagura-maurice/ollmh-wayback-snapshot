#!/usr/bin/env python3
"""
Process downloaded Wayback Machine HTML pages into self-contained local pages.

This script:
  1. Consolidates all CSS/JS/image assets under the canonical timestamp
     20220319205345 in web.archive.org/web/.
  2. Processes each downloaded page in temp_files/pages/:
     - Strips Wayback rewrite scripts (bundle-playback, wombat, ruffle, etc.)
     - Removes the <base href="https://web.archive.org/..."> tag
     - Inserts the base-tag <script> (same as index.html) so relative asset
       URLs resolve against web.archive.org/web/
     - Rewrites all asset URLs to use 20220319205345{cs_,js_,im_}/http:/...
     - Rewrites navigation links to point to local .html pages
     - Fixes the logo and Home links to point to index.html
  3. Saves processed pages alongside index.html.
  4. Updates index.html navigation links to point to local pages.
  5. Creates placeholder stubs for the 3 pages that failed to download.
  6. Generates download_missing_images.py for the user to run locally.

Usage:
    python3 process_pages.py
"""

import os
import re
import glob
import shutil
import html as html_module

# ── Paths ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
WEB_ROOT = os.path.join(PROJECT_ROOT, "web.archive.org", "web")
CANONICAL_TS = "20220319205345"
SITE = "ourladyoflourdesmweahospital.org"

# Prefix for nav links (relative to the <base href="...web.archive.org/web/"> tag).
# With the base tag, href="PAGE_LINK_PREFIX/about-ollmh-location.html" resolves to:
#   .../web.archive.org/web/20220319205345/https:/ourladyoflourdesmweahospital.org/about-ollmh-location.html
PAGE_LINK_PREFIX = f"{CANONICAL_TS}/https:/{SITE}"

# Where processed pages go (alongside index.html)
PAGES_DEST = os.path.join(
    WEB_ROOT, CANONICAL_TS, "https:", SITE
)

# Where downloaded raw pages live
RAW_PAGES = os.path.join(PROJECT_ROOT, "temp_files", "pages")

# Asset directories under WEB_ROOT for the canonical timestamp
CS_DIR = os.path.join(WEB_ROOT, f"{CANONICAL_TS}cs_", "http:", SITE)
JS_DIR = os.path.join(WEB_ROOT, f"{CANONICAL_TS}js_", "http:", SITE)
IM_DIR = os.path.join(WEB_ROOT, f"{CANONICAL_TS}im_", "http:", SITE)

# temp_files asset root
TEMP_WEB = os.path.join(PROJECT_ROOT, "temp_files", "web.archive.org", "web")

# ── Navigation: original site path → local filename ──────────────────────────

NAV_MAP = {
    "/index.php/typography/typography-3": "about-ollmh-location.html",
    "/index.php/typography/typography-5": "administration.html",
    "/index.php/typography/philosophy-of-care": "philosophy-of-care.html",
    "/index.php/typography/philosophy-of-care-2": "hr-capacity-staff.html",
    "/index.php/typography-2/typography-2": "development-projects.html",
    "/index.php/typography-2/typography-4": "self-sustainability-projects.html",
    "/index.php/typography-2/typography-6": "community-support.html",
    "/index.php/typography-2/typography-7": "upcoming-projects.html",
    "/index.php/2011-08-17-08-00-23/expose-framework-2": "in-patient-dept.html",
    "/index.php/2011-08-17-08-00-23/2011-08-26-17-32-08": "out-patient-dept.html",
    "/index.php/2011-08-17-08-00-23/expose-framework": "wards.html",
    "/index.php/2011-08-17-08-00-23/expose-framework-3": "special-medical-services.html",
    "/index.php/2011-08-17-08-00-23/expose-framework-4": "clinic-days.html",
    "/index.php/typography-5/typography-3": "ollmh-outlook.html",
    "/index.php/typography-5/typography-4": "ollmh-departments.html",
    "/index.php/typography-5/typography-5": "smi-community.html",
    "/index.php/2011-08-26-17-44-34/typography-6": "contacts.html",
    "/index.php/2011-08-26-17-44-34/expose-framework-4": "news-events.html",
    "/good": "about-nursing-school.html",
    "/index.php/nursing-sch/nursing-application-form": "medical-school-application-form.html",
}

# Pages that failed to download and need stubs
STUB_PAGES = {
    "in-patient-dept.html": "In Patient Dept",
    "clinic-days.html": "Clinic Days",
    "about-nursing-school.html": "About The Nursing School",
}

# The base-tag script (identical to index.html) — inserted at top of <head>
BASE_TAG_SCRIPT = """<script>
      (function () {
        var p = window.location.pathname;
        var m = "web.archive.org/web/";
        var i = p.indexOf(m);
        if (i !== -1) {
          var b = document.createElement("base");
          b.href = p.substring(0, i + m.length);
          document.head.insertBefore(b, document.head.firstChild);
        }
      })();
    </script>
    <!-- End Wayback Rewrite JS Include -->"""


# ── Phase A: Consolidate assets ──────────────────────────────────────────────


def consolidate_assets():
    """Copy assets from temp_files into the canonical timestamp dirs."""
    print("▶ PHASE A: Consolidating assets to canonical timestamp\n")

    copied = 0

    # Walk temp_files asset dirs and copy unique files to canonical location
    for root, dirs, files in os.walk(TEMP_WEB):
        for fn in files:
            src = os.path.join(root, fn)
            # Determine the relative path after http:/SITE/
            rel = None
            for mod_dir in ("cs_", "js_", "im_"):
                marker = f"{mod_dir}http:{os.sep}{SITE}{os.sep}"
                idx = src.find(marker.replace("/", os.sep))
                # Also try with the dir structure
                parts = src.split(os.sep)
                for i, part in enumerate(parts):
                    if re.match(rf"\d{{14}}{mod_dir}$", part):
                        # Check that next is http: then SITE
                        if (
                            i + 2 < len(parts)
                            and parts[i + 1] == "http:"
                            and parts[i + 2] == SITE
                        ):
                            rel = os.path.join(*parts[i + 3 :])
                            mod = mod_dir
                            break
                if rel:
                    break
            if not rel:
                continue

            if mod == "cs_":
                dest_dir = CS_DIR
            elif mod == "js_":
                dest_dir = JS_DIR
            else:
                dest_dir = IM_DIR

            dest = os.path.join(dest_dir, rel)
            if not os.path.exists(dest):
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(src, dest)
                copied += 1
                print(f"  copied: {mod} {rel}")

    # Fix systems.css — it's under https:/ instead of http:/ in the main dir
    wrong_systems = os.path.join(
        WEB_ROOT, f"{CANONICAL_TS}cs_",
        "https:", SITE, "templates", "tx_finnix", "css", "systems.css"
    )
    correct_systems = os.path.join(CS_DIR, "templates", "tx_finnix", "css", "systems.css")
    if os.path.exists(wrong_systems) and not os.path.exists(correct_systems):
        os.makedirs(os.path.dirname(correct_systems), exist_ok=True)
        shutil.copy2(wrong_systems, correct_systems)
        copied += 1
        print(f"  fixed: systems.css moved to correct path")

    # Copy .php.css → .php so pages that reference .php (without .css) work
    php_css_files = [
        "libraries/expose/interface/css/css-212ba457b58d989b10035c9ea5b91852.php.css",
        "templates/tx_finnix/css/css-bb8fd7a644f50328d257aa61a147f0436f22228bde33e84fa48b98b6de11e47e5f44c95ea87e1dad42d8bc944398778b.php.css",
        "templates/tx_finnix/css/styles/css-d966e87bd26563e9c2ea496587cbfd40.php.css",
    ]
    for pf in php_css_files:
        src = os.path.join(CS_DIR, pf)
        dest = os.path.join(CS_DIR, pf[:-4])  # strip .css
        if os.path.exists(src) and not os.path.exists(dest):
            shutil.copy2(src, dest)
            copied += 1
            print(f"  copied: {pf} → {pf[:-4]}")

    print(f"\n  Total files copied/fixed: {copied}\n")


# ── Phase B: Process pages ───────────────────────────────────────────────────


# Regex to match Wayback asset URLs: /web/TIMESTAMP{cs_,js_,im_}/http://SITE/...
ASSET_URL_RE = re.compile(
    r'/web/(\d{14})(cs_|js_|im_|if_)/http://ourladyoflourdesmweahospital\.org/([^"\'<> )]+)',
    re.IGNORECASE,
)

# Regex to match Wayback page URLs (no modifier): /web/TIMESTAMP/http://SITE/index.php/...
PAGE_URL_RE = re.compile(
    r'/web/\d{14}/http://ourladyoflourdesmweahospital\.org(/index\.php/[^"\'<> #]*)',
    re.IGNORECASE,
)

# Also match full https://web.archive.org/web/.../http://SITE/index.php/...
FULL_PAGE_URL_RE = re.compile(
    r'https://web\.archive\.org/web/\d{14}/http://ourladyoflourdesmweahospital\.org(/index\.php/[^"\'<> #]*)',
    re.IGNORECASE,
)

# Match /good path
GOOD_URL_RE = re.compile(
    r'(?:https://web\.archive\.org/web/\d{14}|)/web/\d{14}?(?:/http://ourladyoflourdesmweahospital\.org)?(/good)',
    re.IGNORECASE,
)

# Wayback rewrite block: from first <script ...archive.org...> to <!-- End Wayback Rewrite -->
WAYBACK_BLOCK_RE = re.compile(
    r'<script[^>]*src="https://web-static\.archive\.org[^"]*"[^>]*></script>\s*'
    r'<script[^>]*src="https://web-static\.archive\.org[^"]*"[^>]*></script>\s*'
    r'(?:<script[^>]*>.*?</script>\s*)*'
    r'<link[^>]*href="https://web-static\.archive\.org[^"]*"[^>]*/?\s*>\s*'
    r'<link[^>]*href="https://web-static\.archive\.org[^"]*"[^>]*/?\s*>\s*'
    r'<!--\s*End Wayback Rewrite JS Include\s*-->',
    re.DOTALL | re.IGNORECASE,
)

# Fallback: also catch the __wm.init wombat script block
WM_INIT_RE = re.compile(
    r'<script type="text/javascript">\s*__wm\.init.*?__wm\.wombat\(.*?\);\s*</script>',
    re.DOTALL | re.IGNORECASE,
)

# <base href="https://web.archive.org/...">
BASE_HREF_RE = re.compile(
    r'<base\s+href="https://web\.archive\.org/web/[^"]*"\s*/?>',
    re.IGNORECASE,
)


def rewrite_asset_url(match):
    """Rewrite /web/TIMESTAMP{mod}/http://SITE/path → CANONICAL_TS{mod}/http:/SITE/path"""
    ts, mod, path = match.group(1), match.group(2), match.group(3)
    # Normalize: if_ modifier → im_ (iframe content treated as image/html)
    if mod == "if_":
        mod = "im_"
    # Fix .php → .php.css for known generated CSS files
    if mod == "cs_" and path.endswith(".php"):
        path = path + ".css"
    return f"{CANONICAL_TS}{mod}/http:/{SITE}/{path}"


def rewrite_nav_links(html_text):
    """Replace Wayback page URLs in nav with PAGE_LINK_PREFIX-prefixed local filenames."""
    changes = 0

    def _prefixed(filename):
        return f"{PAGE_LINK_PREFIX}/{filename}"

    # Handle full https://web.archive.org/web/TS/http://SITE/index.php/PATH
    def full_repl(m):
        nonlocal changes
        path = m.group(1)
        if path in NAV_MAP:
            changes += 1
            return _prefixed(NAV_MAP[path])
        return m.group(0)

    html_text = FULL_PAGE_URL_RE.sub(full_repl, html_text)

    # Handle /web/TS/http://SITE/index.php/PATH
    def page_repl(m):
        nonlocal changes
        path = m.group(1)
        if path in NAV_MAP:
            changes += 1
            return _prefixed(NAV_MAP[path])
        return m.group(0)

    html_text = PAGE_URL_RE.sub(page_repl, html_text)

    # Handle /good path → about-nursing-school.html
    def good_repl(m):
        nonlocal changes
        changes += 1
        return _prefixed("about-nursing-school.html")

    # Match /web/TS/http://SITE/good (with or without index.php prefix)
    good_re = re.compile(
        r'/web/\d{14}/http://ourladyoflourdesmweahospital\.org/good',
        re.IGNORECASE,
    )
    html_text = good_re.sub(good_repl, html_text)

    # Also full URL for /good
    good_full_re = re.compile(
        r'https://web\.archive\.org/web/\d{14}/http://ourladyoflourdesmweahospital\.org/good',
        re.IGNORECASE,
    )
    html_text = good_full_re.sub(good_repl, html_text)

    # Fix Home link: /web/TS/http://SITE/index.php → prefixed index.html
    home_re = re.compile(
        r'/web/\d{14}/http://ourladyoflourdesmweahospital\.org/index\.php(?=["\'])',
        re.IGNORECASE,
    )
    html_text, n_home = home_re.subn(_prefixed("index.html"), html_text)
    changes += n_home

    # Fix logo link: /web/TS/http://SITE/ → prefixed index.html
    logo_re = re.compile(
        r'href="/web/\d{14}/http://ourladyoflourdesmweahospital\.org/"',
        re.IGNORECASE,
    )
    html_text, n_logo = logo_re.subn(f'href="{_prefixed("index.html")}"', html_text)
    changes += n_logo

    return html_text, changes


def process_page(filename):
    """Process a single downloaded HTML page."""
    src = os.path.join(RAW_PAGES, filename)
    with open(src, "r", encoding="utf-8", errors="replace") as f:
        html_text = f.read()

    original_len = len(html_text)

    # 1. Strip Wayback rewrite block
    html_text, n1 = WAYBACK_BLOCK_RE.subn("", html_text)
    # Also strip any remaining __wm.init blocks
    html_text, n2 = WM_INIT_RE.subn("", html_text)

    # 2. Remove <base href="https://web.archive.org/...">
    html_text, n3 = BASE_HREF_RE.subn("", html_text)

    # 3. Insert base-tag script at the very beginning of <head>
    html_text = re.sub(
        r"(<head[^>]*>)",
        r"\1\n    " + BASE_TAG_SCRIPT,
        html_text,
        count=1,
        flags=re.IGNORECASE,
    )

    # 4. Rewrite asset URLs to canonical timestamp
    html_text, n_assets = ASSET_URL_RE.subn(rewrite_asset_url, html_text)

    # 5. Rewrite nav links
    html_text, n_nav = rewrite_nav_links(html_text)

    # 6. Fix remaining /web/TS/http://SITE/ references in inline styles
    # (e.g., background: url('/web/TSim_/http://SITE/...'))
    style_asset_re = re.compile(
        r"['\"]?/web/\d{14}(cs_|js_|im_)/http://ourladyoflourdesmweahospital\.org/([^'\"]+)['\"]?",
        re.IGNORECASE,
    )

    def style_repl(m):
        mod, path = m.group(1), m.group(2)
        if mod == "if_":
            mod = "im_"
        if mod == "cs_" and path.endswith(".php"):
            path = path + ".css"
        return f"{CANONICAL_TS}{mod}/http:/{SITE}/{path}"

    html_text = style_asset_re.sub(style_repl, html_text)

    # 7. Final pass: prefix any remaining bare href="<page>.html" links
    #    (catches relative links in the raw HTML that weren't Wayback URLs)
    known_pages = set(NAV_MAP.values()) | {"index.html"}
    bare_href_re = re.compile(
        r'href="(' + "|".join(re.escape(p) for p in known_pages) + r')"'
    )
    html_text, n_bare = bare_href_re.subn(
        lambda m: f'href="{PAGE_LINK_PREFIX}/{m.group(1)}"', html_text
    )

    # 8. Strip LESS compiler error messages leaked into the page markup
    #    (e.g. "LESS ERROR : load error: failed to find C:\xampp\...")
    html_text, n_less = re.subn(r"LESS ERROR : load error: failed to find [^\n<]*", "", html_text)

    # Save
    dest = os.path.join(PAGES_DEST, filename)
    os.makedirs(PAGES_DEST, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html_text)

    print(
        f"  {filename}: "
        f"stripped wayback={n1 + n2}, base_removed={n3}, "
        f"assets_rewritten={n_assets}, nav_fixed={n_nav}, "
        f"size {original_len}→{len(html_text)}"
    )
    return dest


# ── Phase C: Create stub pages for failed downloads ──────────────────────────


def create_stub(filename, title):
    """Create a minimal stub page matching the site template."""
    stub = f"""<!DOCTYPE html>
<html lang="en-gb" dir="ltr" class="no-js">
    <head>
    <script>
      (function () {{
        var p = window.location.pathname;
        var m = "web.archive.org/web/";
        var i = p.indexOf(m);
        if (i !== -1) {{
          var b = document.createElement("base");
          b.href = p.substring(0, i + m.length);
          document.head.insertBefore(b, document.head.firstChild);
        }}
      }})();
    </script>
    <!-- End Wayback Rewrite JS Include -->

    <link rel="stylesheet" href="{CANONICAL_TS}cs_/http:/{SITE}/templates/tx_finnix/css/systems.css" type="text/css"/>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{title}</title>
    <link href="{CANONICAL_TS}im_/http:/{SITE}/templates/tx_finnix/favicon.ico" rel="shortcut icon" type="image/vnd.microsoft.icon"/>
    <link rel="stylesheet" href="{CANONICAL_TS}cs_/http:/{SITE}/libraries/expose/interface/css/css-212ba457b58d989b10035c9ea5b91852.php.css" type="text/css" media="screen"/>
    <link rel="stylesheet" href="{CANONICAL_TS}cs_/http:/{SITE}/templates/tx_finnix/css/css-bb8fd7a644f50328d257aa61a147f0436f22228bde33e84fa48b98b6de11e47e5f44c95ea87e1dad42d8bc944398778b.php.css" type="text/css" media="screen"/>
    <link rel="stylesheet" href="{CANONICAL_TS}cs_/http:/{SITE}/templates/tx_finnix/css/styles/css-d966e87bd26563e9c2ea496587cbfd40.php.css" type="text/css" media="screen"/>
    <link rel="stylesheet" href="{CANONICAL_TS}cs_/http:/{SITE}/modules/mod_maximenuck/themes/custom/css/maximenuck_maximenuck54.css" type="text/css"/>
    <link rel="stylesheet" href="{CANONICAL_TS}cs_/http:/{SITE}/modules/mod_maximenuck/templatelayers/gantry-navigation.css" type="text/css"/>
    <link rel="stylesheet" href="{CANONICAL_TS}cs_/http:/{SITE}/modules/mod_maximenuck/assets/maximenuresponsiveck.css" type="text/css"/>
    <script src="{CANONICAL_TS}js_/http:/{SITE}/media/jui/js/jquery.min.js" type="text/javascript"></script>
    <script src="{CANONICAL_TS}js_/http:/{SITE}/media/jui/js/jquery-noconflict.js" type="text/javascript"></script>
    <script src="{CANONICAL_TS}js_/http:/{SITE}/media/jui/js/jquery-migrate.min.js" type="text/javascript"></script>
    <script src="{CANONICAL_TS}js_/http:/{SITE}/libraries/expose/interface/js/equalheight.js" type="text/javascript"></script>
    <script src="{CANONICAL_TS}js_/http:/{SITE}/libraries/expose/interface/js/breakpoints.js" type="text/javascript"></script>
    <script src="{CANONICAL_TS}js_/http:/{SITE}/templates/tx_finnix/js/template.js" type="text/javascript"></script>
    </head>

    <body class="style1 align-ltr page-id-0 com-content-article">
        <div class="container">
            <section id="top" class="row">
                <div class="grid9 column first ex-odd top-1"><div class="block widget widget-logo no-title clearfix "><div class="content"><p id="logo" class="brand image" style="">
                    <a class="auto-size" style="background: url('{CANONICAL_TS}im_/http:/{SITE}/templates/tx_finnix/images/style1/logo.png') no-repeat; background-size: contain; width: 222px; height:96px;" href="{PAGE_LINK_PREFIX}/index.html">Our Lady of Lourdes Mwea Hospital</a>
                </p></div></div></div>
            </section>

            <nav id="menu" class="hidden-phone">
                <div class="megamenu clearfix" id="megamenu">
                    <div class="maximenuckh ltr" id="maximenuck54" style="z-index: 10">
                        <div class="maxiroundedleft"></div>
                        <div class="maxiroundedcenter">
                            <ul class="maximenuck">
                                <li class="maximenuck item101 first level1" style="z-index: 12000"><a class="maximenuck" href="{PAGE_LINK_PREFIX}/index.html"><span class="titreck">Home</span></a></li>
                            </ul>
                        </div>
                        <div class="maxiroundedright"></div>
                        <div style="clear: both"></div>
                    </div>
                </div>
            </nav>

            <section id="mainBody" class="row">
                <div class="grid12 column first last">
                    <div class="block">
                        <h1>{title}</h1>
                        <p>This page was not available in the Wayback Machine archive. Content will be added soon.</p>
                        <p><a href="{PAGE_LINK_PREFIX}/index.html">&larr; Back to Home</a></p>
                    </div>
                </div>
            </section>
        </div>
    </body>
</html>
"""
    dest = os.path.join(PAGES_DEST, filename)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(stub)
    print(f"  {filename}: stub created ({title})")


# ── Phase D: Update index.html nav links ─────────────────────────────────────


def update_index_nav():
    """Update navigation links in index.html to point to local pages."""
    print("\n▶ PHASE D: Updating index.html navigation links\n")

    index_path = os.path.join(PAGES_DEST, "index.html")
    with open(index_path, "r", encoding="utf-8", errors="replace") as f:
        html_text = f.read()

    original = html_text
    changes = 0

    def _prefixed(filename):
        return f"{PAGE_LINK_PREFIX}/{filename}"

    # Replace full wayback page URLs in nav
    def full_repl(m):
        nonlocal changes
        path = m.group(1)
        if path in NAV_MAP:
            changes += 1
            return _prefixed(NAV_MAP[path])
        return m.group(0)

    html_text = FULL_PAGE_URL_RE.sub(full_repl, html_text)

    # Replace /web/TS/http://SITE/index.php/PATH in case any remain
    def page_repl(m):
        nonlocal changes
        path = m.group(1)
        if path in NAV_MAP:
            changes += 1
            return _prefixed(NAV_MAP[path])
        return m.group(0)

    html_text = PAGE_URL_RE.sub(page_repl, html_text)

    # Handle /good
    good_full_re = re.compile(
        r'https://web\.archive\.org/web/\d{14}/http://ourladyoflourdesmweahospital\.org/good',
        re.IGNORECASE,
    )

    def good_full_repl(m):
        nonlocal changes
        changes += 1
        return _prefixed("about-nursing-school.html")

    html_text = good_full_re.sub(good_full_repl, html_text)

    # Final pass: prefix any remaining bare href="<page>.html" links
    known_pages = set(NAV_MAP.values()) | {"index.html"}
    bare_href_re = re.compile(
        r'href="(' + "|".join(re.escape(p) for p in known_pages) + r')"'
    )
    html_text, n_bare = bare_href_re.subn(
        lambda m: f'href="{_prefixed(m.group(1))}"', html_text
    )
    changes += n_bare

    if html_text != original:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_text)
        print(f"  index.html: {changes} nav links updated")
    else:
        print("  index.html: no changes needed")


# ── Phase E: Fix asset URLs in CSS and HTML ───────────────────────────────────


# Match absolute Wayback URLs in CSS: https://web.archive.org/web/TS{mod}/http://SITE/...
CSS_ABS_URL_RE = re.compile(
    r"https?://web\.archive\.org/web/\d{14}(cs_|js_|im_|if_)/http://"
    + re.escape(SITE) + r"/([^\)\"'\s]+)",
    re.IGNORECASE,
)

# Match root-relative asset paths in HTML: href="/libraries/..." etc.
ROOT_REL_ASSET_RE = re.compile(
    r'(href|src)="(/(?:libraries|templates|modules|media|components|plugins|cache|images)/[^"]+)"',
    re.IGNORECASE,
)


def _css_url_replacer(m):
    mod = m.group(1)
    path = m.group(2)
    if mod == "if_":
        mod = "im_"
    return f"{CANONICAL_TS}{mod}/http:/{SITE}/{path}"


def _root_rel_replacer(m):
    attr = m.group(1)
    path = m.group(2).lstrip("/")
    if path.endswith(".css"):
        mod = "cs_"
    elif path.endswith(".js"):
        mod = "js_"
    elif path.endswith((".png", ".jpg", ".jpeg", ".gif", ".ico", ".bmp", ".svg")):
        mod = "im_"
    else:
        mod = "cs_"
    return f'{attr}="{CANONICAL_TS}{mod}/http:/{SITE}/{path}"'


def fix_asset_urls():
    """Rewrite absolute Wayback URLs in CSS files to relative canonical paths,
    and fix root-relative asset paths in HTML files."""
    print("\n▶ PHASE E: Fixing asset URLs in CSS and HTML\n")

    # 1. Fix CSS files
    css_total = 0
    for fp in glob.glob(os.path.join(CS_DIR, "**", "*.css"), recursive=True):
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
        new, n = CSS_ABS_URL_RE.subn(_css_url_replacer, txt)
        if n:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new)
            css_total += n
            print(f"  CSS {os.path.relpath(fp)}: {n} URLs rewritten")
    # Also .php files (some CSS stored as .php)
    for fp in glob.glob(os.path.join(CS_DIR, "**", "*.php"), recursive=True):
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
        new, n = CSS_ABS_URL_RE.subn(_css_url_replacer, txt)
        if n:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new)
            css_total += n
            print(f"  CSS {os.path.relpath(fp)}: {n} URLs rewritten")
    print(f"  CSS total: {css_total} URLs rewritten")

    # 2. Fix HTML root-relative asset paths
    html_total = 0
    for fp in sorted(glob.glob(os.path.join(PAGES_DEST, "*.html"))):
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
        new, n = ROOT_REL_ASSET_RE.subn(_root_rel_replacer, txt)
        if n:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new)
            html_total += n
            print(f"  HTML {os.path.basename(fp)}: {n} paths rewritten")
    print(f"  HTML total: {html_total} paths rewritten")


# ── Phase F: Generate missing-images download script ─────────────────────────


def generate_missing_images_script():
    """Scan processed pages for image URLs and check which are missing locally."""
    print("\n▶ PHASE E: Generating missing-images download script\n")

    # Collect all image paths referenced by processed pages
    img_re = re.compile(
        rf'{CANONICAL_TS}im_/http:/ourladyoflourdesmweahospital\.org/([^"\'<> )]+)',
        re.IGNORECASE,
    )
    needed = set()
    for fn in os.listdir(PAGES_DEST):
        if not fn.endswith(".html"):
            continue
        with open(os.path.join(PAGES_DEST, fn), "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        for m in img_re.finditer(text):
            needed.add(m.group(1))

    # Check which are missing
    missing = []
    for path in sorted(needed):
        local = os.path.join(IM_DIR, path)
        if not os.path.exists(local):
            missing.append(path)

    print(f"  Total images referenced: {len(needed)}")
    print(f"  Already present:         {len(needed) - len(missing)}")
    print(f"  Missing:                 {len(missing)}\n")

    if not missing:
        print("  All images present — no download needed.")
        return

    # Generate the script
    script_path = os.path.join(PROJECT_ROOT, "download_missing_images.py")
    script = f'''#!/usr/bin/env python3
"""
Download missing images from the Wayback Machine.

Generated by process_pages.py. Run from the project root:

    python3 download_missing_images.py

If you get 429 Too Many Requests errors, just wait 10-15 minutes
and run again — it skips files that already exist.
"""

import os
import time
import urllib.request
import urllib.error

CANONICAL_TS = "{CANONICAL_TS}"
SITE = "{SITE}"
DEST_BASE = os.path.join("web.archive.org", "web", f"{{CANONICAL_TS}}im_", "http:", SITE)
DELAY = 3
MAX_RETRIES = 5
RETRY_DELAY = 60
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

MISSING_IMAGES = [
'''

    for path in missing:
        script += f'    {path!r},\n'

    script += f''']

def download(url, filepath):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
        print(f"  SKIP (exists): {{os.path.basename(filepath)}}")
        return True
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={{
                "User-Agent": USER_AGENT,
                "Accept": "*/*",
            }})
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(data)
                return True
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = RETRY_DELAY * attempt
                print(f"  429 rate-limited – retry {{attempt}}/{{MAX_RETRIES}} in {{wait}}s …")
                time.sleep(wait)
            elif e.code in (404, 410):
                print(f"  HTTP {{e.code}} – not found: {{url}}")
                return False
            else:
                print(f"  HTTP {{e.code}}: {{e.reason}}")
                return False
        except Exception as e:
            print(f"  Error: {{e}}")
            if attempt < MAX_RETRIES:
                time.sleep(DELAY * attempt)
    return False


def main():
    print("=" * 64)
    print("  Download Missing Images from Wayback Machine")
    print("=" * 64)
    print(f"  Images to download: {{len(MISSING_IMAGES)}}")
    print(f"  Output folder: {{DEST_BASE}}/")
    print("=" * 64 + "\\n")

    ok = 0
    fail = 0
    for i, path in enumerate(MISSING_IMAGES, 1):
        url = f"https://web.archive.org/web/{{CANONICAL_TS}}im_/http://{{SITE}}/{{path}}"
        filepath = os.path.join(DEST_BASE, path)
        print(f"[{{i}}/{{len(MISSING_IMAGES)}}] {{os.path.basename(path)}}")
        if download(url, filepath):
            ok += 1
        else:
            fail += 1
        time.sleep(DELAY)

    print(f"\\n  Done: {{ok}} downloaded, {{fail}} failed")


if __name__ == "__main__":
    main()
'''
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)
    os.chmod(script_path, 0o755)
    print(f"  Generated: {script_path}")
    print(f"  Run it locally: python3 download_missing_images.py")


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    print("=" * 64)
    print("  OLLMH Wayback Snapshot – Page Processor")
    print("=" * 64 + "\n")

    # Phase A: consolidate assets
    consolidate_assets()

    # Phase B: process downloaded pages
    print("▶ PHASE B: Processing downloaded pages\n")
    processed = 0
    for fn in sorted(os.listdir(RAW_PAGES)):
        if fn.endswith(".html"):
            process_page(fn)
            processed += 1
    print(f"\n  Processed {processed} pages\n")

    # Phase C: create stubs for failed pages
    print("▶ PHASE C: Creating stub pages for failed downloads\n")
    for fn, title in STUB_PAGES.items():
        create_stub(fn, title)
    print()

    # Phase D: update index.html nav
    update_index_nav()

    # Phase E: fix asset URLs in CSS and HTML
    fix_asset_urls()

    # Phase F: generate missing images script
    generate_missing_images_script()

    print("\n" + "=" * 64)
    print("  PROCESSING COMPLETE")
    print("=" * 64)
    print(f"  Pages processed : {processed}")
    print(f"  Stubs created   : {len(STUB_PAGES)}")
    print(f"  Output folder   : {PAGES_DEST}")
    print("=" * 64)


if __name__ == "__main__":
    main()
