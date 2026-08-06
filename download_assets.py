#!/usr/bin/env python3
"""
Download Wayback Machine pages and all their assets (CSS, JS, images)
for the OLLMH hospital website snapshot.

Usage:
    python3 download_assets.py

Run this script from the project root directory.
It creates a temp_files/ folder with all downloaded content.

If the script fails partway through, just run it again - it skips
files that are already downloaded (>1 KB on disk).

FIXES in v2:
  - Asset extraction now handles ORIGINAL site URLs (not just
    Wayback-rewritten ones).  The Wayback Machine uses wombat.js
    for client-side URL rewriting, so downloaded HTML contains
    original URLs like /templates/tx_finnix/css/systems.css.
    These are now converted to Wayback Machine asset URLs.
  - Failed page downloads now try alternative URLs (id_ modifier,
    fallback timestamps).
  - CSS url() references are resolved relative to the CSS file's
    original URL, not just matched as absolute Wayback URLs.
"""

import os
import re
import time
import sys
import urllib.request
import urllib.error
import urllib.parse
import html as html_module

# ── Configuration ────────────────────────────────────────────────────────────

TEMP_DIR = "temp_files"
PAGES_DIR = os.path.join(TEMP_DIR, "pages")
DELAY = 3            # seconds between normal requests
MAX_RETRIES = 5      # retries on 429 rate-limit
RETRY_DELAY = 60     # seconds to wait after a 429
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# ── Pages to download ────────────────────────────────────────────────────────
# (local_filename, [list of URLs to try in order])

PAGES = [
    # ── About Us ──
    ("about-ollmh-location.html", [
        "https://web.archive.org/web/20220402223358/http://ourladyoflourdesmweahospital.org/index.php/typography/typography-3",
        "https://web.archive.org/web/20220402223358id_/http://ourladyoflourdesmweahospital.org/index.php/typography/typography-3",
    ]),
    ("administration.html", [
        "https://web.archive.org/web/20220424015154/http://ourladyoflourdesmweahospital.org/index.php/typography/typography-5",
        "https://web.archive.org/web/20220424015154id_/http://ourladyoflourdesmweahospital.org/index.php/typography/typography-5",
    ]),
    ("philosophy-of-care.html", [
        "https://web.archive.org/web/20220128210254/http://ourladyoflourdesmweahospital.org/index.php/typography/philosophy-of-care",
        "https://web.archive.org/web/20220128210254id_/http://ourladyoflourdesmweahospital.org/index.php/typography/philosophy-of-care",
    ]),
    ("hr-capacity-staff.html", [
        "https://web.archive.org/web/20220424130955/http://ourladyoflourdesmweahospital.org/index.php/typography/philosophy-of-care-2",
        "https://web.archive.org/web/20220424130955id_/http://ourladyoflourdesmweahospital.org/index.php/typography/philosophy-of-care-2",
    ]),

    # ── Projects ──
    ("development-projects.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-2",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-2",
    ]),
    ("self-sustainability-projects.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-4",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-4",
    ]),
    ("community-support.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-6",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-6",
    ]),
    ("upcoming-projects.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-7",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-7",
    ]),

    # ── Services ──
    ("in-patient-dept.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-2",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-2",
        "https://web.archive.org/web/20220319205345if_/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-2",
    ]),
    ("out-patient-dept.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/2011-08-26-17-32-08",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/2011-08-26-17-32-08",
    ]),
    ("wards.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework",
    ]),
    ("special-medical-services.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-3",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-3",
    ]),
    ("clinic-days.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-4",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-4",
        "https://web.archive.org/web/20220319205345if_/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-4",
    ]),

    # ── Features ──
    ("ollmh-outlook.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-5/typography-3",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/typography-5/typography-3",
    ]),
    ("ollmh-departments.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-5/typography-4",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/typography-5/typography-4",
    ]),
    ("smi-community.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-5/typography-5",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/typography-5/typography-5",
    ]),

    # ── Contacts / Mails ──
    ("contacts.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-26-17-44-34/typography-6",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/2011-08-26-17-44-34/typography-6",
    ]),
    ("news-events.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-26-17-44-34/expose-framework-4",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/2011-08-26-17-44-34/expose-framework-4",
    ]),

    # ── Nursing School ──
    ("about-nursing-school.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/good",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/good",
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/good",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/good",
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/nursing-sch",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/nursing-sch",
    ]),
    ("medical-school-application-form.html", [
        "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/nursing-sch/nursing-application-form",
        "https://web.archive.org/web/20220319205345id_/http://ourladyoflourdesmweahospital.org/index.php/nursing-sch/nursing-application-form",
    ]),
]

# ── URL parsing helpers ──────────────────────────────────────────────────────


def parse_wayback_url(url):
    """Extract (timestamp, modifier, original_url) from a Wayback Machine URL.

    Returns (None, None, None) if the URL is not a Wayback URL.
    """
    m = re.match(
        r'https?://web\.archive\.org/web/(\d{14})(\w{0,4}_?)/(?:https?://)?(.+)',
        url
    )
    if not m:
        return None, None, None
    timestamp = m.group(1)
    modifier = m.group(2)  # e.g. "cs", "js", "im", "id", "if", or ""
    original = m.group(3)
    # Reconstruct the original URL with protocol
    if url.startswith("https://web.archive.org"):
        # Check if original had http:// or https://
        if "/https://" in url:
            original = "https://" + original
        else:
            original = "http://" + original
    return timestamp, modifier, original


def get_asset_modifier(url_path):
    """Determine the Wayback asset modifier (cs_, js_, im_) from a URL path."""
    # Strip query string and fragment
    path = url_path.split("?")[0].split("#")[0].lower()
    if path.endswith(".css") or path.endswith(".less"):
        return "cs_"
    elif path.endswith(".js") or path.endswith(".mjs"):
        return "js_"
    elif any(path.endswith(ext) for ext in [
        ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
        ".bmp", ".webp", ".cur", ".eot", ".ttf", ".woff",
        ".woff2", ".otf",
    ]):
        return "im_"
    # Unknown extension — default to im_ for images, but return None
    # so we don't try to download non-asset URLs
    return None


def build_wayback_asset_url(original_url, timestamp, modifier):
    """Build a Wayback Machine asset URL from an original site URL."""
    # Ensure original_url has a protocol
    if not original_url.startswith(("http://", "https://")):
        original_url = "http://" + original_url
    return f"https://web.archive.org/web/{timestamp}{modifier}/{original_url}"


def url_to_local_path(url):
    """Map a web.archive.org URL to a local path under temp_files/."""
    for scheme in ("https://", "http://"):
        prefix = scheme + "web.archive.org/"
        if url.startswith(prefix):
            rest = url[len(prefix):]
            # File systems treat // as /, so http:// becomes http:/
            # This matches the existing directory structure
            rest = rest.replace("https://", "https:/").replace("http://", "http:/")
            return os.path.join(TEMP_DIR, "web.archive.org", rest)
    return None


def is_wayback_asset_url(url):
    """True if *url* is already a Wayback asset URL (has cs_/js_/im_ modifier)."""
    return bool(re.search(r"/web/\d{14}(cs_|js_|im_|if_)/", url))


# ── Download function ────────────────────────────────────────────────────────


def download_url(url, filepath):
    """Download *url* to *filepath*.  Returns True on success.

    Skips files that already exist and are larger than 1 KB.
    Retries on HTTP 429 (rate-limit)."""
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1024:
        print(f"  SKIP (exists): {os.path.basename(filepath)}")
        return True

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": USER_AGENT,
                "Accept": "*/*",
            })
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
                if len(data) < 500 and b"429" in data:
                    raise urllib.error.HTTPError(
                        url, 429, "Too Many Requests", {}, None)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(data)
                return True
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = RETRY_DELAY * attempt
                print(f"  429 rate-limited – retry {attempt}/{MAX_RETRIES} "
                      f"in {wait}s …")
                time.sleep(wait)
            elif e.code in (404, 410):
                print(f"  HTTP {e.code} – not found")
                return False
            else:
                print(f"  HTTP {e.code}: {e.reason}")
                return False
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    return False


def download_page(fname, urls, dest_dir):
    """Try multiple URLs to download a page.  Returns (filepath, url_used) or None."""
    dest = os.path.join(dest_dir, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 1024:
        print(f"  SKIP (exists): {fname} ({os.path.getsize(dest):,} bytes)")
        return dest, None  # Already downloaded, URL not needed

    for url in urls:
        print(f"  Trying: {url.split('/')[-1]}")
        if download_url(url, dest):
            size = os.path.getsize(dest)
            print(f"  ✓ {size:,} bytes")
            return dest, url
        print(f"  Failed, trying next URL…")
        time.sleep(DELAY)
    return None


# ── Asset extraction from HTML ───────────────────────────────────────────────


def extract_asset_urls(html_text, page_wayback_url):
    """Extract all asset URLs from HTML text.

    Handles both Wayback-rewritten URLs and original site URLs.
    For original URLs, converts them to Wayback Machine asset URLs
    using the timestamp from *page_wayback_url*.
    """
    decoded = html_module.unescape(html_text)
    raw_urls = set()

    # href="…" or href='…' in <link> tags (CSS, favicon, etc.)
    for m in re.finditer(
        r'<link[^>]+href=["\']([^"\']+)["\']', decoded, re.I | re.DOTALL
    ):
        raw_urls.add(("link", m.group(1)))

    # src="…" or src='…' in <script>, <img>, <iframe>, <embed> tags
    for m in re.finditer(
        r'<(?:script|img|iframe|embed)[^>]+src=["\']([^"\']+)["\']',
        decoded, re.I | re.DOTALL
    ):
        raw_urls.add(("src", m.group(1)))

    # url(…) in inline styles (handles &quot; encoding too)
    for m in re.finditer(r'url\(([^)]+)\)', decoded):
        u = m.group(1).strip().strip('"').strip("'")
        u = html_module.unescape(u)
        raw_urls.add(("url", u))

    # Get timestamp and original site URL from the page's Wayback URL
    timestamp, _, original_page_url = parse_wayback_url(page_wayback_url)
    if not timestamp:
        # Try to use a default timestamp
        timestamp = "20220319205345"
    if not original_page_url:
        original_page_url = "http://ourladyoflourdesmweahospital.org/"

    # Parse the original page URL for resolving relative URLs
    parsed_page = urllib.parse.urlparse(original_page_url)
    site_root = f"{parsed_page.scheme}://{parsed_page.netloc}"

    result = set()

    for source_type, raw_url in raw_urls:
        u = raw_url.strip()

        if not u or u.startswith(("javascript:", "mailto:", "#", "data:",
                                   "tel:", "void(")):
            continue
        if "web-static.archive.org" in u:
            continue  # Wayback toolbar assets — skip

        # ── Case 1: Already a Wayback asset URL ──
        if is_wayback_asset_url(u):
            result.add(u)
            continue

        # ── Case 2: Wayback URL but not an asset URL (e.g., link to another page) ──
        if "web.archive.org/web/" in u:
            # Check if it has a cs_/js_/im_ modifier
            if re.search(r"/web/\d{14}(cs_|js_|im_)/", u):
                result.add(u)
            continue

        # ── Case 3: Relative ../../../TIMESTAMP{cs_,js_,im_}/ URL ──
        if u.startswith("../../../") and re.search(r'\d{14}(cs_|js_|im_)/', u):
            u = "https://web.archive.org/web/" + u.lstrip("./")
            result.add(u)
            continue

        # ── Case 4: Original site URL — convert to Wayback asset URL ──
        # Determine the asset modifier from the file extension
        # First, resolve the URL to get the full path
        if u.startswith(("http://", "https://")):
            # Absolute URL to the original site
            if "ourladyoflourdesmweahospital.org" not in u:
                continue  # External URL — skip
            full_url = u
        elif u.startswith("//"):
            # Protocol-relative URL
            full_url = parsed_page.scheme + ":" + u
            if "ourladyoflourdesmweahospital.org" not in full_url:
                continue
        elif u.startswith("/"):
            # Root-relative URL — prepend site root
            full_url = site_root + u
        else:
            # Relative URL — resolve against page URL
            full_url = urllib.parse.urljoin(original_page_url, u)

        # Determine asset type from the URL path
        parsed = urllib.parse.urlparse(full_url)
        modifier = get_asset_modifier(parsed.path)
        if not modifier:
            # Not a recognizable asset type — skip
            continue

        # Build Wayback Machine asset URL
        wayback_url = build_wayback_asset_url(full_url, timestamp, modifier)
        result.add(wayback_url)

    return result


# ── Asset extraction from CSS ────────────────────────────────────────────────


def extract_css_urls(css_text, css_original_url, timestamp):
    """Extract image URLs from CSS url() references.

    Handles both Wayback-rewritten URLs and original URLs.
    Resolves relative URLs against *css_original_url*.
    """
    decoded = html_module.unescape(css_text)
    urls = set()

    for m in re.finditer(r'url\(([^)]+)\)', decoded):
        u = m.group(1).strip().strip('"').strip("'")
        u = html_module.unescape(u)

        if not u or u.startswith(("data:", "#", "javascript:")):
            continue

        # Already a Wayback asset URL
        if is_wayback_asset_url(u):
            urls.add(u)
            continue

        # Already a Wayback URL (but not asset — try to use as-is)
        if "web.archive.org/web/" in u:
            if re.search(r"/web/\d{14}(cs_|js_|im_)/", u):
                urls.add(u)
            continue

        # Relative ../../../TIMESTAMP{cs_,js_,im_}/ URL
        if u.startswith("../../../") and re.search(r'\d{14}(cs_|js_|im_)/', u):
            u = "https://web.archive.org/web/" + u.lstrip("./")
            urls.add(u)
            continue

        # Original URL — resolve and convert
        if u.startswith(("http://", "https://")):
            if "ourladyoflourdesmweahospital.org" not in u:
                continue
            full_url = u
        elif u.startswith("//"):
            full_url = "https:" + u
            if "ourladyoflourdesmweahospital.org" not in full_url:
                continue
        elif u.startswith("/"):
            # Root-relative
            parsed = urllib.parse.urlparse(css_original_url)
            full_url = f"{parsed.scheme}://{parsed.netloc}" + u
        else:
            # Relative to CSS file
            full_url = urllib.parse.urljoin(css_original_url, u)

        parsed = urllib.parse.urlparse(full_url)
        modifier = get_asset_modifier(parsed.path)
        if not modifier:
            continue

        wayback_url = build_wayback_asset_url(full_url, timestamp, modifier)
        urls.add(wayback_url)

    return urls


# ── Map local CSS file path back to its original URL ─────────────────────────


def local_path_to_original_url(local_path):
    """Given a local CSS file path, reconstruct its original site URL."""
    # Path format: temp_files/web.archive.org/web/TIMESTAMPcs_/http:/site.com/...
    # We need: http://site.com/...
    parts = local_path.replace("\\", "/").split("/")
    # Find the timestamp+modifier part (e.g., 20220319205345cs_)
    for i, part in enumerate(parts):
        if re.match(r'\d{14}(cs_|js_|im_|if_|id_)?$', part):
            # Everything after this is the original URL
            after = "/".join(parts[i + 1:])
            # The first segment is http:/ or https:/ — convert to ://
            if after.startswith("http:/"):
                after = "http://" + after[6:]
            elif after.startswith("https:/"):
                after = "https://" + after[7:]
            return after
    return None


def local_path_to_timestamp(local_path):
    """Extract the 14-digit timestamp from a local asset path."""
    parts = local_path.replace("\\", "/").split("/")
    for part in parts:
        m = re.match(r'(\d{14})', part)
        if m:
            return m.group(1)
    return "20220319205345"


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    os.makedirs(PAGES_DIR, exist_ok=True)

    print("=" * 64)
    print("  OLLMH Wayback Snapshot – Downloader v2")
    print("=" * 64)
    print(f"  Pages to download : {len(PAGES)}")
    print(f"  Output folder     : {TEMP_DIR}/")
    print(f"  Delay between req : {DELAY}s")
    print(f"  Retry on 429      : {MAX_RETRIES}x / {RETRY_DELAY}s")
    print("=" * 64)

    # ── Phase 1: Download HTML pages ──────────────────────────────────────
    print("\n▶ PHASE 1: Downloading HTML pages\n")
    ok_pages = []  # (fname, filepath, url_used_or_first_url)
    for i, (fname, urls) in enumerate(PAGES, 1):
        print(f"[{i}/{len(PAGES)}] {fname}")
        result = download_page(fname, urls, PAGES_DIR)
        if result:
            filepath, url_used = result
            ok_pages.append((fname, filepath, url_used or urls[0]))
        else:
            print("  ✗ ALL URLs FAILED")
        time.sleep(DELAY)

    print(f"\n  Pages: {len(ok_pages)}/{len(PAGES)} downloaded")

    # ── Phase 2: Extract & download assets from HTML ─────────────────────
    print("\n▶ PHASE 2: Extracting & downloading page assets\n")
    asset_urls = set()
    for fname, fpath, page_url in ok_pages:
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        found = extract_asset_urls(content, page_url)
        asset_urls.update(found)
        print(f"  {fname}: {len(found)} asset URLs")
        if found:
            for u in list(found)[:3]:
                print(f"    → {u.split('/')[-1]}")
            if len(found) > 3:
                print(f"    … and {len(found) - 3} more")

    # Filter out already-downloaded
    to_download = []
    for u in sorted(asset_urls):
        lp = url_to_local_path(u)
        if lp and not (os.path.exists(lp) and os.path.getsize(lp) > 1024):
            to_download.append(u)

    print(f"\n  Total unique assets : {len(asset_urls)}")
    print(f"  Already downloaded  : {len(asset_urls) - len(to_download)}")
    print(f"  To download         : {len(to_download)}\n")

    assets_ok = 0
    assets_fail = 0
    for i, u in enumerate(to_download, 1):
        lp = url_to_local_path(u)
        print(f"[{i}/{len(to_download)}] {os.path.basename(lp)}")
        if download_url(u, lp):
            assets_ok += 1
        else:
            assets_fail += 1
        time.sleep(DELAY)

    # ── Phase 3: Parse CSS files for url() images ────────────────────────
    print("\n▶ PHASE 3: Parsing CSS files for url() references\n")
    css_image_urls = set()
    assets_root = os.path.join(TEMP_DIR, "web.archive.org", "web")

    css_count = 0
    for root, _, files in os.walk(assets_root):
        for fn in files:
            if not fn.endswith(".css"):
                continue
            fpath = os.path.join(root, fn)
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    css = f.read()
            except Exception:
                continue

            # Reconstruct the original URL and timestamp for this CSS file
            orig_url = local_path_to_original_url(fpath)
            ts = local_path_to_timestamp(fpath)
            if not orig_url:
                continue

            found = extract_css_urls(css, orig_url, ts)
            css_image_urls.update(found)
            css_count += 1
            if found:
                print(f"  {fn}: {len(found)} url() refs")

    print(f"\n  Parsed {css_count} CSS files")
    print(f"  CSS-referenced images : {len(css_image_urls)} total")

    # Filter already-downloaded
    new_css_urls = []
    for u in sorted(css_image_urls):
        lp = url_to_local_path(u)
        if lp and not (os.path.exists(lp) and os.path.getsize(lp) > 1024):
            new_css_urls.append(u)

    print(f"  Already downloaded    : {len(css_image_urls) - len(new_css_urls)}")
    print(f"  To download           : {len(new_css_urls)}\n")

    for i, u in enumerate(new_css_urls, 1):
        lp = url_to_local_path(u)
        print(f"[{i}/{len(new_css_urls)}] {os.path.basename(lp)}")
        if download_url(u, lp):
            assets_ok += 1
        else:
            assets_fail += 1
        time.sleep(DELAY)

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 64)
    print("  DOWNLOAD COMPLETE")
    print("=" * 64)
    print(f"  HTML pages   : {len(ok_pages)}/{len(PAGES)}")
    print(f"  Assets (OK)  : {assets_ok}")
    print(f"  Assets (fail): {assets_fail}")
    print()
    print("  Files saved to:")
    print(f"    {PAGES_DIR}/")
    print(f"    {TEMP_DIR}/web.archive.org/web/")
    print()
    print("  Next steps:")
    print("    1.  git add temp_files/")
    print("    2.  git commit -m 'add downloaded wayback pages and assets'")
    print("    3.  git push origin main")
    print("=" * 64)

    return 0 if len(ok_pages) == len(PAGES) else 1


if __name__ == "__main__":
    sys.exit(main())
