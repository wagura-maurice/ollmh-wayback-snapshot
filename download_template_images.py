#!/usr/bin/env python3
"""Download missing template images referenced in CSS files.

These are background images, icons, arrows, etc. that were never downloaded
during the initial asset fetch. Run locally (VPS IP is rate-limited):

    python3 download_template_images.py

If you get 429 Too Many Requests errors, just wait 10-15 minutes
and run again — it skips files that already exist.
"""

import os
import time
import urllib.request
import urllib.error
import urllib.parse

CANONICAL_TS = "20220319205345"
SITE = "ourladyoflourdesmweahospital.org"
DEST_BASE = os.path.join("web.archive.org", "web", f"{CANONICAL_TS}im_", "http:", SITE)
DELAY = 3
MAX_RETRIES = 5
RETRY_DELAY = 60
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Template images referenced in CSS that are missing from disk
MISSING_TEMPLATE_IMAGES = [
    "libraries/expose/interface/images/expose_logo_dark.png",
    "libraries/expose/interface/images/expose_logo_light.png",
    "libraries/expose/interface/images/typography.png",
    "media/system/images/pdf_button.png",
    "modules/mod_maximenuck/themes/custom/images/transparent.gif",
    "modules/mod_xpertslider/assets/images/blank.gif",
    "modules/mod_xpertslider/assets/images/xslider-loader.gif",
    "modules/mod_xpertslider/assets/images/xslider_skins.png",
    "templates/images/style1/tab_nav_bg.png",
    "templates/system/images/selector-arrow.png",
    "templates/tx_finnix/images/glyphicons-halflings.png",
    "templates/tx_finnix/images/menu_l.png",
    "templates/tx_finnix/images/menu_r.png",
    "templates/tx_finnix/images/menu_r_rtl.png",
    "templates/tx_finnix/images/rss2_icon.png",
    "templates/tx_finnix/images/scroller_arrow.png",
    "templates/tx_finnix/images/social-icons/facebook.png",
    "templates/tx_finnix/images/social-icons/rss.png",
    "templates/tx_finnix/images/social-icons/twitter.png",
    "templates/tx_finnix/images/style1/bg.jpg",
    "templates/tx_finnix/images/style1/bottom_sep.png",
    "templates/tx_finnix/images/style1/bottom_shadow.jpg",
    "templates/tx_finnix/images/style1/header_bg.png",
    "templates/tx_finnix/images/style1/header_bg_rtl.png",
    "templates/tx_finnix/images/style1/menu_hover_arrow.png",
    "templates/tx_finnix/images/style1/social_icons.png",
    "templates/tx_finnix/images/style1/tab_nav_bg.png",
    "templates/tx_finnix/images/style1/tab_nav_bg_rtl.png",
    "templates/tx_finnix/images/submenu_bg.png",
    "templates/tx_finnix/images/themexpert.png",
    "templates/tx_finnix/images/totop.png",
    "templates/tx_finnix/images/typography/arrow.png",
    "templates/tx_finnix/images/typography/list_check.png",
    "templates/tx_finnix/img/navigator.png",
    "templates/tx_finnix/img/vert_large.png",
]


def download(url, filepath):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
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
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(data)
                return True
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = RETRY_DELAY * attempt
                print(f"  429 rate-limited – retry {attempt}/{MAX_RETRIES} in {wait}s …")
                time.sleep(wait)
            elif e.code in (404, 410):
                print(f"  HTTP {e.code} – not found: {url}")
                return False
            else:
                print(f"  HTTP {e.code}: {e.reason}")
                return False
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(DELAY * attempt)
    return False


def main():
    print("=" * 64)
    print("  Download Missing Template Images from Wayback Machine")
    print("=" * 64)
    print(f"  Images to download: {len(MISSING_TEMPLATE_IMAGES)}")
    print(f"  Output folder: {DEST_BASE}/")
    print("=" * 64 + "\n")

    ok = 0
    fail = 0
    for i, path in enumerate(MISSING_TEMPLATE_IMAGES, 1):
        url = f"https://web.archive.org/web/{CANONICAL_TS}im_/http://{SITE}/{path}"
        filepath = os.path.join(DEST_BASE, path)
        print(f"[{i}/{len(MISSING_TEMPLATE_IMAGES)}] {os.path.basename(path)}")
        if download(url, filepath):
            ok += 1
        else:
            fail += 1
        time.sleep(DELAY)

    print(f"\n  Done: {ok} downloaded, {fail} failed")


if __name__ == "__main__":
    main()
