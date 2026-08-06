#!/usr/bin/env python3
"""Download the 6 malformed-URL images (now corrected) and probe CDX for the 2 real 404s."""

import os
import time
import urllib.request
import urllib.error
import urllib.parse
import json

CANONICAL_TS = "20220319205345"
SITE = "ourladyoflourdesmweahospital.org"
DEST_BASE = os.path.join("web.archive.org", "web", f"{CANONICAL_TS}im_", "http:", SITE)
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# 6 entries that were malformed in download_missing_images.py (truncated at spaces / HTML entity not decoded).
# Stored DECODED here; quoted for URL and disk path in download_image() so on-disk naming matches
# the existing convention (e.g. "Faith%20giving...JPG").
CORRECTED = [
    "images/ollmh/CommunityProject/A TEAM OF LOCAL ADMINISTRATION CHIEFS AND SUB CHIEFS OF MWEA DURING ONE OF THE RESOURCE MOBILIZAT.JPG",
    "images/ollmh/CommunityProject/COMMUNITY HEALTH VOLUNTEERS.JPG",
    "images/ollmh/CommunityProject/ORPHANS AND VENERABLE CHILDREN DURING ONE OF THE TRAININGS HELD IN 2010.JPG",
    "images/ollmh/hospitalUnits/InPatient/DSCF7526 (2).JPG",
    "images/ollmh/hospitalUnits/Mwea MH.jpg",
    "templates/tx_finnix/images/style1/logo.png",
]

# 2 real images that 404'd at CANONICAL_TS — probe CDX for any snapshot
CDX_PROBES = [
    "images/ollmh/Aministration/DSC00488.JPG",
    "images/ollmh/hospitalUnits/OutPatient/DSCF7421.JPG",
]


def fetch(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def download_image(path):
    # Quote spaces/unsafe chars for both the URL and the on-disk path so naming
    # matches the existing convention (e.g. "Faith%20giving...JPG"). Parens kept literal.
    qpath = urllib.parse.quote(path, safe="/%()")
    url = f"https://web.archive.org/web/{CANONICAL_TS}im_/http://{SITE}/{qpath}"
    filepath = os.path.join(DEST_BASE, qpath)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
        print(f"  SKIP (exists): {os.path.basename(qpath)}")
        return True
    for attempt in range(1, 6):
        try:
            data = fetch(url)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(data)
            print(f"  OK {len(data)} bytes")
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
            print(f"  err: {e}")
            if attempt < 5:
                time.sleep(3 * attempt)
    return False


def _cdx_query(url):
    """Hit one CDX URL with retries on 429/503. Returns parsed rows or None on permanent failure."""
    for attempt in range(1, 6):
        try:
            data = fetch(url, timeout=60)
            rows = json.loads(data)
            return [tuple(r) for r in rows[1:]] if len(rows) > 1 else []
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                wait = 60 * attempt
                print(f"  CDX {e.code} – retry {attempt}/5 in {wait}s …")
                time.sleep(wait)
            else:
                print(f"  CDX HTTP {e.code}")
                return None
        except Exception as e:
            print(f"  CDX err: {e}")
            if attempt < 5:
                time.sleep(5 * attempt)
    return None


def cdx_lookup(original_path):
    """Find any 200 snapshot of the original URL. Falls back to an unfiltered query
    (any statuscode) so the caller can tell 'never captured' from 'captured but not 200'."""
    q = urllib.parse.urlencode({
        "url": f"{SITE}/{original_path}",
        "output": "json",
        "fl": "timestamp,statuscode,length",
        "limit": "50",
        "filter": "statuscode:200",
    })
    rows = _cdx_query(f"https://web.archive.org/cdx/search/cdx?{q}")
    if rows is None:
        return None
    if rows:
        return rows
    # no 200 snapshot — confirm whether it was captured at all (any status)
    print("  no 200 snapshot; checking for any capture …")
    q2 = urllib.parse.urlencode({
        "url": f"{SITE}/{original_path}",
        "output": "json",
        "fl": "timestamp,statuscode,length",
        "limit": "50",
    })
    any_rows = _cdx_query(f"https://web.archive.org/cdx/search/cdx?{q2}")
    if any_rows:
        statuses = sorted({r[1] for r in any_rows})
        print(f"  found {len(any_rows)} capture(s) with status codes: {statuses} (none 200)")
    else:
        print("  no capture of any kind found in CDX")
    return []


def main():
    print("=" * 64)
    print("  Fix remaining images (corrected URLs + CDX probes)")
    print("=" * 64)

    ok = fail = 0
    print("\n--- Corrected URLs ---")
    for p in CORRECTED:
        print(f"[corr] {os.path.basename(p)}")
        if download_image(p):
            ok += 1
        else:
            fail += 1
        time.sleep(3)

    print("\n--- CDX probes for real 404s ---")
    for p in CDX_PROBES:
        print(f"[cdx] {p}")
        snaps = cdx_lookup(p)
        if snaps is None:
            fail += 1
            continue
        if not snaps:
            print("  no 200 snapshot found in CDX")
            fail += 1
            continue
        # prefer the canonical timestamp if present, else the closest
        chosen = None
        for ts, sc, length in snaps:
            if ts == CANONICAL_TS:
                chosen = (ts, sc, length)
                break
        if not chosen:
            # closest to canonical (string compare works for YYYYMMDDhhmmss)
            chosen = min(snaps, key=lambda s: abs(int(s[0]) - int(CANONICAL_TS)))
        ts, sc, length = chosen
        print(f"  found snapshot {ts} (status {sc}, {length} bytes)")
        qpath = urllib.parse.quote(p, safe="/%()")
        url = f"https://web.archive.org/web/{ts}im_/http://{SITE}/{qpath}"
        filepath = os.path.join(DEST_BASE, qpath)
        for attempt in range(1, 6):
            try:
                data = fetch(url)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(data)
                print(f"  OK {len(data)} bytes (from {ts})")
                ok += 1
                break
            except urllib.error.HTTPError as e:
                print(f"  HTTP {e.code}")
                fail += 1
                break
            except Exception as e:
                print(f"  err: {e}")
                if attempt < 5:
                    time.sleep(3 * attempt)
                else:
                    fail += 1
        time.sleep(3)

    print(f"\n  Done: {ok} downloaded, {fail} failed")


if __name__ == "__main__":
    main()
