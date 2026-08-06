# OLLMH Wayback Snapshot – Local Download Instructions

## What this does

`download_assets.py` downloads every Wayback Machine page listed in the
navigation menu (About Us, Projects, Services, Features, Contacts, Nursing
School) along with all their CSS, JavaScript, and image assets.

Everything is saved into a `temp_files/` folder at the project root:

```
temp_files/
├── pages/                          ← HTML pages (20 pages)
│   ├── about-ollmh-location.html
│   ├── administration.html
│   ├── philosophy-of-care.html
│   ├── hr-capacity-staff.html
│   ├── development-projects.html
│   ├── ... (etc)
│   └── medical-school-application-form.html
│
└── web.archive.org/web/            ← CSS / JS / image assets
    ├── 20220319205345cs_/http:/ourladyoflourdesmweahospital.org/...
    ├── 20220319205345im_/http:/ourladyoflourdesmweahospital.org/...
    ├── 20220319205345js_/http:/ourladyoflourdesmweahospital.org/...
    ├── 20220402223358cs_/http:/ourladyoflourdesmweahospital.org/...
    └── ... (various timestamps)
```

## Prerequisites

- **Python 3.6+** (comes pre-installed on macOS/Linux; on Windows use
  `python` instead of `python3`)
- **git** (to clone/push)
- An internet connection

No third-party Python packages are needed — the script uses only the
standard library.

## Steps

### 1. Clone the repo to your PC

```bash
git clone git@github.com:wagura-maurice/ollmh-wayback-snapshot.git
cd ollmh-wayback-snapshot
```

Or via HTTPS:

```bash
git clone https://github.com/wagura-maurice/ollmh-wayback-snapshot.git
cd ollmh-wayback-snapshot
```

### 2. Run the download script

```bash
python3 download_assets.py
```

On Windows:

```
python download_assets.py
```

#### What to expect

- The script downloads **20 HTML pages** first, one at a time with a
  3-second delay between each.
- It then extracts all CSS/JS/image URLs from those pages and downloads
  them (Phase 2).
- Finally it parses the downloaded CSS files for `url()` image references
  and downloads those too (Phase 3).
- If the Wayback Machine returns **429 Too Many Requests**, the script
  automatically waits 60 seconds and retries up to 5 times.
- If the script crashes or you stop it, just run it again — it skips
  files that are already downloaded.

#### Expected runtime

With no rate-limiting: ~10 minutes.
With rate-limiting: could take 30–60 minutes (the script handles this
automatically).

### 3. Verify the download

Check that the pages and assets were downloaded:

```bash
# Should list 20 .html files
ls temp_files/pages/

# Should show cs_, im_, js_ directories
ls temp_files/web.archive.org/web/

# Count total files downloaded
find temp_files/ -type f | wc -l
```

You should see at least 80–100 files total.

### 4. Commit and push back to GitHub

```bash
git add temp_files/
git add download_assets.py
git commit -m "add downloaded wayback pages and assets"
git push origin main
```

### 5. Let me know

Once you've pushed, tell me and I'll:

1. Pull the changes.
2. Process each downloaded HTML page (remove Wayback rewrite scripts,
   fix asset paths, add the `<base>` tag, fix logo/Home links).
3. Move the pages and assets into the correct location in the project.
4. Update all navigation links in `index.html` to point to the local
   pages.
5. Verify everything loads correctly.

## Troubleshooting

**"429 Too Many Requests" keeps appearing**

The Wayback Machine is rate-limiting your IP. The script retries
automatically, but if it keeps failing after several retries:
- Wait 10–15 minutes and run the script again.
- The script skips already-downloaded files, so you won't lose progress.

**"python3: command not found"**

You're probably on Windows. Use `python` instead:

```
python download_assets.py
```

**Script fails partway through**

Just run it again. It skips files that already exist (>1 KB on disk).

**Some pages show 0 bytes or are very small**

This means the download failed for that page. Run the script again —
it will retry failed downloads (since they're either missing or too
small to skip).

**Port 9099 / local server**

This is unrelated to the download script. The local server on port 9099
is only needed for viewing the site, not for downloading assets.
