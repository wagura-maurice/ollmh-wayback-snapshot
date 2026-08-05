# How to Recover the Wayback Machine Snapshot Locally

This guide shows you how to download the March 19, 2022 Wayback Machine
snapshot of `https://ourladyoflourdesmweahospital.org/` on your own PC.

The snapshot timestamp is: **20220319205345**

---

## Option A: Download Just the Homepage (Quickest)

This grabs only the homepage HTML file. No dependencies required beyond
`curl`, which is pre-installed on macOS and Linux (and on Windows 10+).

### macOS / Linux

```bash
mkdir -p ollmh_snapshot
curl -L -o ollmh_snapshot/index.html \
  "https://web.archive.org/web/20220319205345id_/https://ourladyoflourdesmweahospital.org/"
```

### Windows (PowerShell)

```powershell
New-Item -ItemType Directory -Force -Path ollmh_snapshot
Invoke-WebRequest -Uri "https://web.archive.org/web/20220319205345id_/https://ourladyoflourdesmweahospital.org/" -OutFile ollmh_snapshot\index.html
```

> The `id_` in the URL tells the Wayback Machine to serve the **raw original
> HTML** with no rewriting or toolbar injected.

The file will be saved to `ollmh_snapshot/index.html`.

---

## Option B: Download the Full Site Snapshot (Recommended)

This downloads the entire website as it appeared at that timestamp — all
pages, images, CSS, JS, etc. — and recreates the directory structure.

### Step 1: Install Ruby (if you don't have it)

You need **Ruby >= 1.9.2**. Check whether it's already installed:

```bash
ruby --version
```

If you see a version number (e.g. `ruby 3.2.1`), skip to Step 2.
If you get `command not found`, install Ruby for your platform:

#### macOS

Ruby comes pre-installed on macOS, but the system version may be old.
The recommended approach is via **Homebrew**:

```bash
# Install Homebrew if you don't have it (https://brew.sh)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Ruby
brew install ruby

# Add Homebrew Ruby to your PATH (run once, then restart your terminal)
echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
ruby --version
```

> On Intel Macs, the path is `/usr/local/opt/ruby/bin` instead of
> `/opt/homebrew/opt/ruby/bin`.

#### Linux (Debian / Ubuntu)

```bash
sudo apt update
sudo apt install ruby-full

# Verify
ruby --version
```

#### Linux (Fedora / RHEL)

```bash
sudo dnf install ruby

# Verify
ruby --version
```

#### Windows

1. Go to https://rubyinstaller.org/
2. Download the latest **RubyInstaller** (with Devkit) `.exe`.
3. Run the installer and accept the defaults (including "Add Ruby
   executables to your PATH").
4. Open a new Command Prompt or PowerShell window and verify:

```powershell
ruby --version
```

### Step 2: Install the Wayback Machine Downloader gem

The downloader is distributed as a Ruby **gem** (Ruby's package format).
Install it with:

#### macOS / Linux

```bash
gem install wayback_machine_downloader
```

If you get a permission error (e.g. `You don't have write permissions
for the ... directory`), use `sudo`:

```bash
sudo gem install wayback_machine_downloader
```

> **Recommended (avoids `sudo`):** configure a user-local gem directory
> so you don't need `sudo` for future gem installs:
> ```bash
> echo '# Ruby gem user setup' >> ~/.bashrc
> echo 'export GEM_HOME="$HOME/.gem"' >> ~/.bashrc
> echo 'export PATH="$HOME/.gem/bin:$PATH"' >> ~/.bashrc
> source ~/.bashrc
> gem install wayback_machine_downloader
> ```
> (On macOS with Zsh, use `~/.zshrc` instead of `~/.bashrc`.)

#### Windows (PowerShell or Command Prompt)

```powershell
gem install wayback_machine_downloader
```

> On Windows you typically don't need `sudo` / elevated permissions.

#### Verify the installation

```bash
wayback_machine_downloader --help
```

You should see the usage/help text. If you get `command not found`, make
sure Ruby's gem bin directory is on your `PATH` (see the platform-specific
notes above).

### Step 3: Run the download

```bash
wayback_machine_downloader https://ourladyoflourdesmweahospital.org/ \
  --from 20220319205345 \
  --to 20220319205345 \
  --directory ollmh_snapshot
```

### What each flag does

| Flag | Meaning |
|---|---|
| `https://ourladyoflourdesmweahospital.org/` | The base URL of the site to recover. |
| `--from 20220319205345` | Only fetch file versions on or after this timestamp. |
| `--to 20220319205345` | Only fetch file versions on or before this timestamp. |
| `--directory ollmh_snapshot` | Save recovered files into `ollmh_snapshot/`. |

Using the same value for `--from` and `--to` locks the download to that
exact snapshot.

### Optional: Speed it up

Add concurrency to download multiple files at once:

```bash
wayback_machine_downloader https://ourladyoflourdesmweahospital.org/ \
  --from 20220319205345 \
  --to 20220319205345 \
  --directory ollmh_snapshot \
  --concurrency 20
```

### Optional: Just the homepage via the downloader

```bash
wayback_machine_downloader https://ourladyoflourdesmweahospital.org/ \
  --from 20220319205345 \
  --to 20220319205345 \
  --exact-url \
  --directory ollmh_snapshot
```

---

## Option C: Download via Docker (No Ruby Needed)

If you have Docker installed, you can skip the Ruby installation entirely.

### Full site

```bash
mkdir -p ollmh_snapshot
docker run --rm -it -v "$PWD/ollmh_snapshot:/websites/ourladyoflourdesmweahospital.org" \
  hartator/wayback-machine-downloader \
  https://ourladyoflourdesmweahospital.org/ \
  --from 20220319205345 \
  --to 20220319205345
```

> On **Windows PowerShell**, replace `$PWD` with `${PWD}`.

The files will be saved into `ollmh_snapshot/`.

---

## Verifying the Download

After the download completes:

```bash
ls -la ollmh_snapshot/
```

You should see the site's files (e.g., `index.html`, image folders, CSS,
etc.). Open `ollmh_snapshot/index.html` in your browser to view the
recovered homepage.

---

## Troubleshooting

### `429 Too Many Requests`

The Wayback Machine is rate-limiting your IP. Wait 15–60 minutes and retry.
This is more common on shared/cloud IPs than on residential connections.

### Permission errors during `gem install`

Add `sudo`:

```bash
sudo gem install wayback_machine_downloader
```

### Docker volume mounts on Windows

Make sure Docker Desktop has file sharing enabled for the drive you're
working on (Settings > Resources > File Sharing).

---

## Reference

- Tool: [wayback-machine-downloader](https://github.com/hartator/wayback-machine-downloader)
- Snapshot URL: https://web.archive.org/web/20220319205345/https://ourladyoflourdesmweahospital.org/
- Timestamp: `20220319205345` (March 19, 2022, 20:53:45 UTC)
