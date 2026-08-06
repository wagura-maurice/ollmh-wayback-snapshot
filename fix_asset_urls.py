#!/usr/bin/env python3
"""Fix asset URLs in CSS and HTML files so they resolve correctly under the
<base href="...web.archive.org/web/"> tag.

Two problems:
1. CSS files contain absolute https://web.archive.org/web/TIMESTAMP{mod}/http://SITE/...
   URLs with various timestamps → rewrite to relative CANONICAL_TS{mod}/http:/SITE/...
2. HTML files have root-relative paths (/libraries/..., /templates/..., /modules/...)
   inside IE conditional comments → rewrite to CANONICAL_TS{mod}/http:/SITE/...
"""

import os
import re
import glob

CANONICAL_TS = "20220319205345"
SITE = "ourladyoflourdesmweahospital.org"
WEB_ROOT = os.path.join("web.archive.org", "web")

# ── 1. Fix absolute Wayback URLs in CSS files ─────────────────────────────────

# Match: https://web.archive.org/web/TIMESTAMP{mod}/http://SITE/PATH
# Also match http:// variant
ABS_URL_RE = re.compile(
    r"https?://web\.archive\.org/web/\d{14}(cs_|js_|im_|if_)/http://"
    + re.escape(SITE)
    + r"/([^\)\"'\s]+)",
    re.IGNORECASE,
)


def rewrite_css_url(m):
    mod = m.group(1)
    path = m.group(2)
    if mod == "if_":
        mod = "im_"
    return f"{CANONICAL_TS}{mod}/http:/{SITE}/{path}"


def fix_css_files():
    print("▶ Fixing absolute Wayback URLs in CSS files\n")
    css_dirs = [
        os.path.join(WEB_ROOT, f"{CANONICAL_TS}cs_"),
    ]
    total = 0
    for css_dir in css_dirs:
        for fp in glob.glob(os.path.join(css_dir, "**", "*.css"), recursive=True):
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                txt = f.read()
            new, n = ABS_URL_RE.subn(rewrite_css_url, txt)
            if n:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new)
                total += n
                print(f"  {os.path.relpath(fp)}: {n} URLs rewritten")
        # Also fix .php files (some CSS is in .php files)
        for fp in glob.glob(os.path.join(css_dir, "**", "*.php"), recursive=True):
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                txt = f.read()
            new, n = ABS_URL_RE.subn(rewrite_css_url, txt)
            if n:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(new)
                total += n
                print(f"  {os.path.relpath(fp)}: {n} URLs rewritten")
    print(f"\n  Total CSS URLs rewritten: {total}\n")


# ── 2. Fix root-relative asset paths in HTML files ─────────────────────────────

# Match: href="/path" or src="/path" where path starts with a known asset dir
ROOT_REL_RE = re.compile(
    r'(href|src)="(/(?:libraries|templates|modules|media|components|plugins|cache|images)/[^"]+)"',
    re.IGNORECASE,
)


def rewrite_root_rel(m):
    attr = m.group(1)
    path = m.group(2).lstrip("/")
    # Determine modifier from extension
    if path.endswith(".css"):
        mod = "cs_"
    elif path.endswith(".js"):
        mod = "js_"
    elif path.endswith((".png", ".jpg", ".jpeg", ".gif", ".ico", ".bmp", ".svg")):
        mod = "im_"
    else:
        # Default to cs_ for unknown types (most common in templates)
        mod = "cs_"
    return f'{attr}="{CANONICAL_TS}{mod}/http:/{SITE}/{path}"'


def fix_html_files():
    print("▶ Fixing root-relative asset paths in HTML files\n")
    pages_dir = os.path.join(
        WEB_ROOT, CANONICAL_TS, "https:", SITE
    )
    total = 0
    for fp in sorted(glob.glob(os.path.join(pages_dir, "*.html"))):
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
        new, n = ROOT_REL_RE.subn(rewrite_root_rel, txt)
        if n:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new)
            total += n
            print(f"  {os.path.basename(fp)}: {n} paths rewritten")
    print(f"\n  Total HTML root-relative paths rewritten: {total}\n")


if __name__ == "__main__":
    print("=" * 64)
    print("  Fix Asset URLs (CSS + HTML)")
    print("=" * 64 + "\n")
    fix_css_files()
    fix_html_files()
    print("=" * 64)
    print("  DONE")
    print("=" * 64)
