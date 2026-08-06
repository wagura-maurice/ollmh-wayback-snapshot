#!/usr/bin/env python3
"""
Make the wayback snapshot work universally — both on a debug server
served from the repo root AND on GitHub Pages served from a subdirectory
(e.g. https://user.github.io/ollmh-wayback-snapshot/).

The problem: HTML files use <base href="/web.archive.org/web/"> (absolute)
and CSS files use @import/url() with absolute paths like
/web.archive.org/web/20220319205345im_/...  These work when the repo is
served from the server root but break on GitHub Pages where the root is
/ollmh-wayback-snapshot/.

Fix:
  1. HTML: replace <base href="/web.archive.org/web/"> with
     <base href="../../../">  (relative path from the page's directory
     back up to web.archive.org/web/)
  2. CSS: for every url() / @import that starts with /web.archive.org/web/,
     convert it to a relative path computed from the CSS file's own
     location.
  3. HTML: convert full https://web.archive.org/web/... asset URLs
     (im_, cs_, js_, oe_ modifiers) to relative paths when the file
     exists locally, so they load from the local snapshot instead of
     the live Wayback Machine.

Standard library only. Idempotent — safe to run multiple times.
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(ROOT, "web.archive.org", "web")

# Pages live at:  web.archive.org/web/<timestamp>/https:/<site>/<page>.html
# From <site>/ up to web/  =  ../../../
HTML_BASE_OLD = '<base href="/web.archive.org/web/">'
HTML_BASE_NEW = '<base href="../../../">'


def fix_html_files():
    """Replace absolute base href with relative in all HTML pages."""
    pages_dir = os.path.join(
        WEB_DIR, "20220319205345", "https:", "ourladyoflourdesmweahospital.org"
    )
    count = 0
    for name in os.listdir(pages_dir):
        if not name.endswith(".html"):
            continue
        path = os.path.join(pages_dir, name)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if HTML_BASE_OLD in content:
            content = content.replace(HTML_BASE_OLD, HTML_BASE_NEW)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
            print("fixed base href:", name)
    print("  -> %d HTML files updated" % count)


def wayback_url_to_local_path(url):
    """Convert a full https://web.archive.org/web/... URL to its local
    file path.  Returns None if not a wayback asset URL."""
    prefix = "https://web.archive.org/web/"
    if not url.startswith(prefix):
        return None
    rest = url[len(prefix):]
    # Collapse http:// → http:/  and https:// → https:/  to match
    # the on-disk directory layout.
    rest = rest.replace("http://", "http:/").replace("https://", "https:/")
    # Strip query strings (e.g. ?format=feed&type=rss)
    rest = rest.split("?")[0]
    return os.path.join(WEB_DIR, rest)


def fix_html_full_urls():
    """Convert full https://web.archive.org/web/... asset URLs in HTML
    to relative paths when the file exists locally."""
    pages_dir = os.path.join(
        WEB_DIR, "20220319205345", "https:", "ourladyoflourdesmweahospital.org"
    )
    # Asset modifiers that should be localised when the file exists
    asset_modifiers = ("im_", "cs_", "js_", "oe_", "if_", "id_")
    full_url_re = re.compile(
        r'https://web\.archive\.org/web/\d+(?:im_|cs_|js_|oe_|if_|id_)/https?:/+[^"\']+'
    )
    count = 0
    for name in os.listdir(pages_dir):
        if not name.endswith(".html"):
            continue
        path = os.path.join(pages_dir, name)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        original = content

        def replace_full_url(m):
            url = m.group(0)
            local = wayback_url_to_local_path(url)
            if local and os.path.exists(local):
                # Convert to a relative path from web.archive.org/web/
                # (the <base href="../../../"> resolves relative URLs
                # from there)
                rel = os.path.relpath(local, WEB_DIR).replace(os.sep, "/")
                return rel
            return url  # keep full URL — file not local, loads from wayback

        content = full_url_re.sub(replace_full_url, content)

        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            count += 1
            print("fixed full URLs:", name)
    print("  -> %d HTML files updated" % count)


def relpath_to_web(css_path):
    """Return the relative path from a CSS file's directory up to
    web.archive.org/web/  (e.g. '../../../../../../' )."""
    css_dir = os.path.dirname(css_path)
    rel = os.path.relpath(WEB_DIR, css_dir)
    # os.path.relpath returns something like '../../../../../../web'
    # but we want it to end at web/  with a trailing slash for URLs
    rel = rel.replace(os.sep, "/")
    if not rel.endswith("/"):
        rel += "/"
    return rel


def fix_css_file(css_path):
    """Convert absolute /web.archive.org/web/... paths in a CSS file
    to relative paths based on the file's location."""
    with open(css_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    prefix = "/web.archive.org/web/"
    rel_to_web = relpath_to_web(css_path)

    # Match url(...) and @import "..." / @import url(...) patterns
    # that contain the absolute prefix.  We replace the prefix with
    # the relative path back to web/.
    def replace_abs(m):
        full = m.group(0)
        if prefix not in full:
            return full
        # Replace the absolute prefix with the relative path
        return full.replace(prefix, rel_to_web)

    # url(  "..."  )  |  url(  '...'  )  |  url( ... )
    content = re.sub(
        r'url\(\s*["\']?/web\.archive\.org/web/[^)"\']*["\']?\s*\)',
        replace_abs,
        content,
    )
    # @import "..." | @import '...'
    content = re.sub(
        r'@import\s+["\']/web\.archive\.org/web/[^"\']*["\'];?',
        replace_abs,
        content,
    )

    if content != original:
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("fixed css:", os.path.relpath(css_path, ROOT))
        return True
    return False


def fix_css_files():
    """Walk all CSS-like files under web.archive.org/web/ and fix
    absolute paths.  Handles .css files and .php files that contain
    CSS (Joomla generated CSS as .php)."""
    count = 0
    for dirpath, _dirs, files in os.walk(WEB_DIR):
        for name in files:
            if name.endswith(".css") or name.endswith(".php"):
                css_path = os.path.join(dirpath, name)
                if fix_css_file(css_path):
                    count += 1
    print("  -> %d CSS files updated" % count)


if __name__ == "__main__":
    print("Fixing HTML base href tags...")
    fix_html_files()
    print()
    print("Fixing HTML full wayback URLs...")
    fix_html_full_urls()
    print()
    print("Fixing CSS absolute paths...")
    fix_css_files()
    print()
    print("Done.")
