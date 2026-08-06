#!/usr/bin/env python3
"""
Download a single Wayback Machine asset into the local snapshot tree.

Default target:
  https://web.archive.org/web/20190212014712cs_/http://ourladyoflourdesmweahospital.org/modules/mod_xperttabs/assets/css/common.css

Saved to:
  web.archive.org/web/20190212014712cs_/http:/ourladyoflourdesmweahospital.org/modules/mod_xperttabs/assets/css/common.css

Usage:
  python3 download_xperttabs_css.py            # downloads the default URL
  python3 download_xperttabs_css.py <URL>      # downloads any wayback asset URL

Standard library only. Skips files already present and >1 KB.
"""

import os
import sys
import time
import urllib.request
import urllib.error

DEFAULT_URL = (
    "https://web.archive.org/web/20190212014712cs_/"
    "http://ourladyoflourdesmweahospital.org/"
    "modules/mod_xperttabs/assets/css/common.css"
)

WAYBACK_PREFIX = "https://web.archive.org/web/"


def url_to_local_path(url, root="."):
    """Convert a wayback asset URL to its local snapshot path."""
    if not url.startswith(WAYBACK_PREFIX):
        raise ValueError("URL must start with " + WAYBACK_PREFIX)
    # Strip the wayback prefix, leaving e.g.
    #   20190212014712cs_/http://ourlady.../common.css
    rest = url[len(WAYBACK_PREFIX):]
    # Collapse the double slash after http:/ or https:/ to match the
    # existing on-disk layout (http:/ourlady... not http://ourlady...).
    rest = rest.replace("http://", "http:/").replace("https://", "https:/")
    return os.path.join(root, "web.archive.org", "web", rest)


def download(url, root="."):
    dest = url_to_local_path(url, root)
    if os.path.exists(dest) and os.path.getsize(dest) > 1024:
        print("skip (exists):", dest)
        return

    os.makedirs(os.path.dirname(dest), exist_ok=True)

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(1, 6):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            with open(dest, "wb") as f:
                f.write(data)
            print("ok (%d bytes): %s" % (len(data), dest))
            return
        except urllib.error.HTTPError as e:
            print("attempt %d: HTTP %d for %s" % (attempt, e.code, url))
            if e.code == 429:
                print("  rate limited, waiting 60s...")
                time.sleep(60)
            else:
                time.sleep(5)
        except urllib.error.URLError as e:
            print("attempt %d: %s for %s" % (attempt, e.reason, url))
            time.sleep(5)

    print("FAILED after 5 attempts:", url)


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    download(url)
