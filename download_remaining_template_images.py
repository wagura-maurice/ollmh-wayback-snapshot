#!/usr/bin/env python3
"""Download the 4 template images that got 429'd from the VPS.

Run locally: python3 download_remaining_template_images.py
"""

import os
import time
import urllib.request
import urllib.error

CANONICAL_TS = "20220319205345"
SITE = "ourladyoflourdesmweahospital.org"
DEST_BASE = os.path.join("web.archive.org", "web", f"{CANONICAL_TS}im_", "http:", SITE)
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

REMAINING = [
    "modules/mod_maximenuck/themes/custom/images/transparent.gif",
    "templates/images/style1/tab_nav_bg.png",
    "templates/tx_finnix/img/navigator.png",
    "templates/tx_finnix/img/vert_large.png",
]


def download(url, filepath):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
        print(f"  SKIP (exists): {os.path.basename(filepath)}")
        return True
    for attempt in range(1, 6):
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
                wait = 60 * attempt
                print(f"  429 – retry {attempt}/5 in {wait}s …")
                time.sleep(wait)
            elif e.code in (404, 410):
                print(f"  HTTP {e.code} – not found")
                return False
            else:
                print(f"  HTTP {e.code}: {e.reason}")
                return False
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < 5:
                time.sleep(3 * attempt)
    return False


def main():
    print("Downloading 4 remaining template images…\n")
    ok = fail = 0
    for path in REMAINING:
        url = f"https://web.archive.org/web/{CANONICAL_TS}im_/http://{SITE}/{path}"
        filepath = os.path.join(DEST_BASE, path)
        print(f"  {os.path.basename(path)}")
        if download(url, filepath):
            ok += 1
        else:
            fail += 1
        time.sleep(3)
    print(f"\nDone: {ok} downloaded, {fail} failed")


if __name__ == "__main__":
    main()
