#!/usr/bin/env python3
"""
Download Wayback Machine pages and all their assets (CSS, JS, images)
for the OLLMH hospital website snapshot.

Usage:
    python3 download_assets.py

Run this script from the project root directory.
It creates a temp_files/ folder with all downloaded content.

If the script fails partway through, just run it again - it skips
files that are already downloaded.
"""

import os
import re
import time
import sys
import urllib.request
import urllib.error
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
# (local_filename, wayback_url)

PAGES = [
    # ── About Us ──
    ("about-ollmh-location.html",
     "https://web.archive.org/web/20220402223358/http://ourladyoflourdesmweahospital.org/index.php/typography/typography-3"),
    ("administration.html",
     "https://web.archive.org/web/20220424015154/http://ourladyoflourdesmweahospital.org/index.php/typography/typography-5"),
    ("philosophy-of-care.html",
     "https://web.archive.org/web/20220128210254/http://ourladyoflourdesmweahospital.org/index.php/typography/philosophy-of-care"),
    ("hr-capacity-staff.html",
     "https://web.archive.org/web/20220424130955/http://ourladyoflourdesmweahospital.org/index.php/typography/philosophy-of-care-2"),

    # ── Projects ──
    ("development-projects.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-2"),
    ("self-sustainability-projects.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-4"),
    ("community-support.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-6"),
    ("upcoming-projects.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-2/typography-7"),

    # ── Services ──
    ("in-patient-dept.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-2"),
    ("out-patient-dept.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/2011-08-26-17-32-08"),
    ("wards.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework"),
    ("special-medical-services.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-3"),
    ("clinic-days.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-17-08-00-23/expose-framework-4"),

    # ── Features ──
    ("ollmh-outlook.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-5/typography-3"),
    ("ollmh-departments.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-5/typography-4"),
    ("smi-community.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/typography-5/typography-5"),

    # ── Contacts / Mails ──
    ("contacts.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-26-17-44-34/typography-6"),
    ("news-events.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/2011-08-26-17-44-34/expose-framework-4"),

    # ── Nursing School ──
    ("about-nursing-school.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/good"),
    ("medical-school-application-form.html",
     "https://web.archive.org/web/20220319205345/http://ourladyoflourdesmweahospital.org/index.php/nursing-sch/nursing-application-form"),
]

# ── Helpers ──────────────────────────────────────────────────────────────────


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
                # Detect 429 body that slipped through
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
                print(f"  HTTP {e.code} – not found, skipping")
                return False
            else:
                print(f"  HTTP {e.code}: {e.reason}")
                return False
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    return False


def url_to_local_path(url):
    """Map a web.archive.org URL to a path under temp_files/."""
    for scheme in ("https://", "http://"):
        prefix = scheme + "web.archive.org/"
        if url.startswith(prefix):
            rest = url[len(prefix):]            # e.g. web/2022…cs_/http:/…
            return os.path.join(TEMP_DIR, "web.archive.org", rest)
    return None


def is_asset_url(url):
    """True if *url* points to a Wayback asset (CSS / JS / image)."""
    # Asset URLs contain a 14-digit timestamp followed by cs_, js_, im_, or if_
    return bool(re.search(r"/web/\d{14}(cs_|js_|im_|if_)/", url))


def extract_asset_urls(html_text):
    """Return a set of absolute asset URLs found in *html_text*."""
    decoded = html_module.unescape(html_text)
    raw_urls = set()

    # href="…"  (CSS, favicon, etc.)
    for m in re.finditer(r'<link[^>]+href="([^"]+)"', decoded, re.I):
        raw_urls.add(m.group(1))

    # src="…"  (scripts, images)
    for m in re.finditer(r'<(?:script|img|iframe|embed)[^>]+src="([^"]+)"',
                         decoded, re.I):
        raw_urls.add(m.group(1))

    # url(…)  in inline styles
    for m in re.finditer(r'url\(([^)]+)\)', decoded):
        u = m.group(1).strip().strip('"').strip("'")
        u = html_module.unescape(u)
        raw_urls.add(u)

    # Resolve and filter
    result = set()
    for u in raw_urls:
        if not u or u.startswith(("javascript:", "mailto:", "#", "data:")):
            continue
        if "web-static.archive.org" in u:          # Wayback toolbar – skip
            continue

        # Relative ../../../  →  https://web.archive.org/web/…
        if u.startswith("../../../"):
            u = "https://web.archive.org/web/" + u.lstrip("./")

        # Relative ../../  or  ../  (less common)
        elif u.startswith("../") and "2022" in u:
            # Resolve by stripping ../ prefixes and appending to web/ root
            stripped = u.lstrip("./")
            if stripped.startswith("2022"):
                u = "https://web.archive.org/web/" + stripped

        if not u.startswith(("https://web.archive.org/web/",
                             "http://web.archive.org/web/")):
            continue

        # Only keep asset URLs (css/js/im modifiers)
        if not is_asset_url(u):
            continue

        result.add(u)

    return result


def extract_css_urls(css_text):
    """Return asset URLs found in url(…) references inside CSS text."""
    decoded = html_module.unescape(css_text)
    urls = set()
    for m in re.finditer(r'url\(([^)]+)\)', decoded):
        u = m.group(1).strip().strip('"').strip("'")
        u = html_module.unescape(u)
        if u.startswith(("https://web.archive.org/web/",
                         "http://web.archive.org/web/")):
            urls.add(u)
    return urls


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    os.makedirs(PAGES_DIR, exist_ok=True)

    print("=" * 64)
    print("  OLLMH Wayback Snapshot – Downloader")
    print("=" * 64)
    print(f"  Pages to download : {len(PAGES)}")
    print(f"  Output folder     : {TEMP_DIR}/")
    print(f"  Delay between req : {DELAY}s")
    print(f"  Retry on 429      : {MAX_RETRIES}x / {RETRY_DELAY}s")
    print("=" * 64)

    # ── Phase 1: Download HTML pages ──────────────────────────────────────
    print("\n▶ PHASE 1: Downloading HTML pages\n")
    ok_pages = []
    for i, (fname, url) in enumerate(PAGES, 1):
        print(f"[{i}/{len(PAGES)}] {fname}")
        dest = os.path.join(PAGES_DIR, fname)
        if download_url(url, dest):
            size = os.path.getsize(dest)
            print(f"  ✓ {size:,} bytes")
            ok_pages.append((fname, dest, url))
        else:
            print("  ✗ FAILED")
        time.sleep(DELAY)

    print(f"\n  Pages: {len(ok_pages)}/{len(PAGES)} downloaded")

    # ── Phase 2: Extract & download assets from HTML ─────────────────────
    print("\n▶ PHASE 2: Extracting & downloading page assets\n")
    asset_urls = set()
    for fname, fpath, _ in ok_pages:
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        found = extract_asset_urls(content)
        asset_urls.update(found)
        print(f"  {fname}: {len(found)} asset URLs")

    # Remove URLs we already have on disk
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
            found = extract_css_urls(css)
            css_image_urls.update(found)
            if found:
                print(f"  {fn}: {len(found)} url() refs")

    # Filter already-downloaded
    new_css_urls = []
    for u in sorted(css_image_urls):
        lp = url_to_local_path(u)
        if lp and not (os.path.exists(lp) and os.path.getsize(lp) > 1024):
            new_css_urls.append(u)

    print(f"\n  CSS-referenced images : {len(css_image_urls)} total, "
          f"{len(new_css_urls)} new\n")

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
