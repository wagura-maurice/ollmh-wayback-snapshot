# Migrating & Reconfiguring a WordPress Installation (wardwatch2027 → ollmh)

> **Goal.** Produce an independent, fresh WordPress project for OLLMH by
> **replicating** the existing wardwatch2027 WordPress codebase into a new
> `Ollmh/` folder, **stripping** every wardwatch-specific trace from the copy,
> **re-initialising** its own git history, and **reconfiguring** it (fresh
> database, fresh keys, fresh URL) so the new project is fully independent of
> the source — then implementing the OLLMH build spec from the
> `ollmh-wayback-snapshot` repo's `docs/` folder on top of that baseline.
>
> This is the **remote-VPS workflow** (per `work.txt`): the work runs on a
> remote server with the Devin CLI from `/root/Project/`, using a **git clone**
> of wardwatch2027 as the source (not the local `/var/www/html/wardwatch2027`
> directory). The repo `ollmh-wayback-snapshot` is the **instruction source of
> truth** — its `docs/` folder says exactly what to change in the `Ollmh/`
> replica.
>
> **Related docs:** [`DEPLOYMENT.md`](./DEPLOYMENT.md) (production nginx/vhost),
> [`CRON-JOBS.md`](./CRON-JOBS.md), [`ENVIRONMENT-SETUP.md`](./ENVIRONMENT-SETUP.md),
> [`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md),
> [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md),
> [`CONTENT-MIGRATION.md`](./CONTENT-MIGRATION.md),
> [`ASSET-MIGRATION.md`](./ASSET-MIGRATION.md), [`URL-MAPPING.md`](./URL-MAPPING.md),
> and [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md) (read first —
> ADRs supersede any conflicting guidance).

---

## 0. Environment assumptions

| Item | Value |
|---|---|
| Remote server | VPS, SSH as `root@192.168.1.1` |
| Working root | `/root/Project/` (all three folders live here, not in the web root) |
| Source repo (clone) | `git@github.com:wagura-maurice/wardwatch2027.git` → `/root/Project/wardwatch2027` |
| Replica (new project) | `/root/Project/Ollmh/` (from `cp -r` of the clone) |
| Instruction repo | `git@github.com:wagura-maurice/ollmh-wayback-snapshot.git` → `/root/Project/ollmh-wayback-snapshot` (holds `docs/` + `seeders/`) |
| Devin CLI / model | Run from `/root/Project/` (Claude 4.8) |
| PHP / WP-CLI / Composer | PHP 8.4, WP-CLI, Composer installed on the VPS |
| Web root (final serving) | `/var/www/html/ollmh` (see [`DEPLOYMENT.md`](./DEPLOYMENT.md) — outside `/root/Project`) |
| Source DB (never reused) | MySQL database `wardwatch2027` |
| New DB | MySQL database `ollmh`, dedicated user |

> **What the git clone contains — and what it does NOT.** The wardwatch2027
> repo's `.gitignore` excludes `vendor/`, `wp-content/uploads/`, and the
> third-party plugins (`w3-total-cache`, `seo-by-rank-math`, `redirection`,
> `google-site-kit`, `broken-link-checker`, `wordpress-seo`). A `git clone`
> therefore contains WordPress core, the wardwatch custom plugins, the child
> theme, Composer manifests, and deploy tooling — but **not** the third-party
> plugins or Composer vendor tree. Those are re-obtained in
> [Step 4](#4-step-3--restore-vendor-and-third-party-plugins) via
> `composer install` + `wp plugin install`. This is by design: it is exactly
> the "strip to a fresh baseline" we want.

---

## 1. Preflight checks (on the remote VPS)

```bash
ssh root@192.168.1.1

# Tooling present
wp --version
php -v
composer --version

# Disk headroom (clone + copy ≈ 600 MB; budget >= 2 GB free)
df -h /root

# Working root exists and is empty of the folders we are about to create
mkdir -p /root/Project
ls -la /root/Project

# Confirm SSH access to GitHub (passwordless deploy key / agent)
ssh -T git@github.com || true
```

---

## 2. Step 1 — Clone the wardwatch2027 source and copy it into `Ollmh/`

```bash
cd /root/Project

# 1. Clone the existing project (the source of the replication)
git clone git@github.com:wagura-maurice/wardwatch2027.git /root/Project/wardwatch2027

# 2. Make an exact copy for the new project
cp -r /root/Project/wardwatch2027 /root/Project/Ollmh/

# 3. Verify the copy is complete
du -sh /root/Project/wardwatch2027 /root/Project/Ollmh
ls -la /root/Project/Ollmh
```

The last command should show the WordPress core layout: `wp-admin/`,
`wp-includes/`, `wp-content/`, `wp-config.php`, `index.php`, `wp-load.php`,
etc.

---

## 3. Step 2 — Strip the copy to a fresh baseline

Work **only inside** `/root/Project/Ollmh/`. The clone at
`/root/Project/wardwatch2027` is left untouched as a reference.

### 3.1 Neutralize site-specific runtime data

```bash
cd /root/Project/Ollmh

# Uploaded media (any tracked images/docs; Rank Math also stores images here)
rm -rf wp-content/uploads/*

# W3 Total Cache runtime files & config
rm -rf wp-content/cache wp-content/w3tc-config wp-content/advanced-cache.php

# Upgrade artifacts / any stray logs
rm -rf wp-content/upgrade/* wp-content/backup-db
rm -f  wp-content/debug.log

# Database snapshot directory
rm -rf data
```

### 3.2 Remove wardwatch-specific plugins and setup scripts

```bash
cd /root/Project/Ollmh/wp-content/plugins

rm -rf wardwatch2027-api wardwatch2027-db
rm -f  wardwatch2027-setup.php wardwatch2027-setup-admin.php
rm -rf wordpress-seo   # wardwatch-specific SEO plugin; OLLMH uses Rank Math
```

> The generic third-party plugins (W3TC, Rank Math, Redirection, Google Site
> Kit, Broken Link Checker) are **not in the git clone** anyway — they are
> restored fresh in [Step 4](#4-step-3--restore-vendor-and-third-party-plugins).

### 3.3 Remove the wardwatch child theme

```bash
cd /root/Project/Ollmh/wp-content/themes
rm -rf wardwatch2027-child
```

Keep the default `twenty*` themes (including `twentytwentyfive`, which the
OLLMH child theme extends per ADR-001 / [`THEME-ARCHITECTURE.md`](./THEME-ARCHITECTURE.md)).

### 3.4 Remove / quarantine wardwatch root-level config & deploy tooling

These files all hard-code wardwatch paths, domains, DB names, or Deployer
config. Delete them, or move them aside for reference:

```bash
cd /root/Project/Ollmh
mkdir -p /root/Project/_wardwatch-legacy

for f in deploy.php deployer.txt vhost.config nginx.conf crontab.config \
         ecosystem.config.js wp.sh start-wordpress.bat .local .htaccess .gitignore; do
  [ -e "$f" ] && mv "$f" /root/Project/_wardwatch-legacy/
done

# Dev-only helper scripts
rm -f wp.sh start-wordpress.bat

# Inspect and remove if wardwatch-specific:
ls -la admin 2>/dev/null && rm -rf admin
```

### 3.5 Reset the git history (critical independence step)

The copied `.git` still points at the wardwatch2027 repository. Remove it and
start a clean history for the OLLMH project:

```bash
cd /root/Project/Ollmh

# Remove the source repo history
rm -rf .git

# Start a fresh repository
git init
git add .
git commit -m "Initialize OLLMH project: fresh baseline derived from wardwatch2027 code"

git branch -M main
git remote add origin git@github.com:wagura-maurice/ollmh.git   # (or whichever repo hosts the OLLMH project)
```

> The first commit message documents the provenance: *"new project based on
> the wardwatch2027 code."*

### 3.6 Review the Composer dependencies

```bash
cd /root/Project/Ollmh
cat composer.json
```

- Keep the `composer.json`/`composer.lock` if OLLMH will reuse FPDF or
  PhpSpreadsheet (PDF application forms, Excel exports).
- Otherwise drop them:
  ```bash
  rm -f composer.json composer.lock
  ```

### 3.7 Confirm what the fresh baseline now contains

```bash
find /root/Project/Ollmh -maxdepth 1 -type f -o -maxdepth 1 -type d | sort
ls /root/Project/Ollmh/wp-content/plugins
ls /root/Project/Ollmh/wp-content/themes
```

No `wardwatch` string anywhere in tracked code:

```bash
cd /root/Project/Ollmh
grep -rIl --exclude-dir=wp-admin --exclude-dir=wp-includes --exclude-dir=vendor \
  "wardwatch2027" . 2>/dev/null && echo "FOUND matches — review above" || echo "CLEAN: no wardwatch references in code"
```

---

## 4. Step 3 — Restore vendor and third-party plugins

Because these were git-ignored, restore them after the clone:

```bash
cd /root/Project/Ollmh

# Composer vendor tree (matches composer.json/lock)
composer install --no-dev --optimize-autoloader

# Third-party plugins used by the OLLMH stack (see docs/SEO-STRATEGY.md,
# docs/PERFORMANCE-BUDGET.md, docs/URL-MAPPING.md)
wp plugin install w3-total-cache --activate --allow-root
wp plugin install seo-by-rank-math --activate --allow-root
wp plugin install redirection --allow-root
wp plugin install google-site-kit --allow-root
wp plugin install broken-link-checker --allow-root
```

> If instead the source for the copy is the live `/var/www/html/wardwatch2027`
> directory (not a git clone), these plugins and `vendor/` are already present
> and this step is skipped — but note they ship wardwatch's saved config, which
> is discarded with the old database anyway.

---

## 5. Step 4 — Fresh database (fully independent of the source)

**Critical rule: do not reuse the `wardwatch2027` database.** Reusing it would
carry every wardwatch user, post, option, redirect, and SEO setting into the
OLLMH site and tie the two deployments together. Create a brand-new database
and a dedicated user:

```bash
mysql -e "CREATE DATABASE ollmh CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -e "CREATE USER 'ollmh'@'localhost' IDENTIFIED BY 'CHANGE-ME-strong-passphrase';"
mysql -e "GRANT ALL PRIVILEGES ON ollmh.* TO 'ollmh'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"

# Verify
mysql -e "SHOW DATABASES LIKE 'ollmh';"
```

> `utf8mb4_unicode_ci` matches the collation used throughout
> [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md).

---

## 6. Step 5 — Reconfigure `wp-config.php`

Replace the wardwatch `wp-config.php` with a fresh OLLMH one. Regenerate from
the sample, then re-add the small set of OLLMH-relevant constants:

```bash
cd /root/Project/Ollmh

# Back up the old one (for reference only)
mv wp-config.php /root/Project/_wardwatch-legacy/wp-config.php.wardwatch

# Regenerate with the new DB credentials
wp config create \
  --dbname=ollmh \
  --dbuser=ollmh \
  --dbpass='CHANGE-ME-strong-passphrase' \
  --dbhost=localhost \
  --dbcharset=utf8mb4 \
  --skip-check

# Fresh authentication salts (invalidates all old cookies/sessions)
wp config shuffle-salts

# OLLMH environment + WordPress constants
wp config set WP_ENV local
wp config set WP_DEBUG true --raw
wp config set WP_DEBUG_LOG true --raw
wp config set DISABLE_WP_CRON true --raw
```

The resulting `wp-config.php` should look like this (credentials/salts
placeholder):

```php
<?php
/**
 * OLLMH — Our Lady of Lourdes Mwea Hospital
 * Derived from wardwatch2027 and stripped; fully independent project.
 */

// Detect environment: local (dev) vs production (deployed)
$host = $_SERVER['HTTP_HOST'] ?? $_SERVER['SERVER_NAME'] ?? '';
$is_local = (
    strpos($host, 'localhost') !== false ||
    strpos($host, '127.0.0.1') !== false ||
    strpos($host, '.local') !== false ||
    strpos($host, '.test') !== false ||
    file_exists(__DIR__ . '/.local')
);
$environment = getenv('WP_ENV') ?: ($is_local ? 'local' : 'production');
define('OLLMH_ENVIRONMENT', $environment);

// CLI runs have no HTTP_HOST; provide a safe default for the OLLMH site.
if (PHP_SAPI === 'cli' && empty($_SERVER['HTTP_HOST'])) {
    $_SERVER['HTTP_HOST'] = 'ollmh.local';
}
if (PHP_SAPI === 'cli' && empty($_SERVER['SERVER_NAME'])) {
    $_SERVER['SERVER_NAME'] = 'ollmh.local';
}

/** Database settings */
if ($environment === 'local') {
    define('DB_NAME', 'ollmh');
    define('DB_USER', 'ollmh');
    define('DB_PASSWORD', 'CHANGE-ME-strong-passphrase');
    define('DB_HOST', 'localhost');
} else {
    // Production: fill in on deploy (do not commit real credentials)
    define('DB_NAME', 'ollmh');
    define('DB_USER', 'ollmh');
    define('DB_PASSWORD', getenv('OLLMH_DB_PASSWORD') ?: '');
    define('DB_HOST', 'localhost');
}

define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

/**#@+
 * Authentication unique keys and salts.
 * Generated fresh by: wp config shuffle-salts
 */
define('AUTH_KEY',         'GENERATED');
define('SECURE_AUTH_KEY',  'GENERATED');
define('LOGGED_IN_KEY',    'GENERATED');
define('NONCE_KEY',        'GENERATED');
define('AUTH_SALT',        'GENERATED');
define('SECURE_AUTH_SALT', 'GENERATED');
define('LOGGED_IN_SALT',   'GENERATED');
define('NONCE_SALT',       'GENERATED');
/**#@-*/

$table_prefix = 'wp_';

define('WP_DEBUG',        $environment === 'local');
define('WP_DEBUG_LOG',    $environment === 'local');
define('WP_DEBUG_DISPLAY', $environment === 'local');

/* Custom values */
date_default_timezone_set('Africa/Nairobi');
define('WP_TIMEZONE', 'Africa/Nairobi');

// Use system cron instead of WordPress's poor-man's cron (see CRON-JOBS.md)
define('DISABLE_WP_CRON', true);

/* That's all, stop editing! Happy publishing. */
if (!defined('ABSPATH')) {
    define('ABSPATH', __DIR__ . '/');
}
require_once ABSPATH . 'wp-settings.php';
```

Add the local-dev marker file and a `.gitignore` for the new project:

```bash
cd /root/Project/Ollmh
touch .local   # local environment flag
cat > .gitignore <<'EOF'
wp-config.php
.local
wp-content/uploads/*
wp-content/cache/*
wp-content/w3tc-config/*
wp-content/debug.log
vendor/*
EOF
git add .gitignore && git commit -m "Add OLLMH gitignore and local env marker"
```

> **Never commit `wp-config.php`** (it contains DB credentials and salts).

---

## 7. Step 6 — Fresh WordPress install & base configuration

Because we discarded the wardwatch database, WordPress does **not** see itself
as installed. Run a fresh `wp core install` against the empty `ollmh` database:

```bash
cd /root/Project/Ollmh

wp core install \
  --url="http://ollmh.local" \
  --title="Our Lady of Lourdes Mwea Hospital" \
  --admin_user="ollmh-admin" \
  --admin_password="CHANGE-ME-strong-admin-password" \
  --admin_email="admin@ourladyoflourdesmweahospital.org" \
  --skip-email
```

> **URL note:** use the URL that will serve the site (see
> [`DEPLOYMENT.md`](./DEPLOYMENT.md) for the `/var/www/html/ollmh` web-root
> mapping). Changing the URL later requires `wp option update home`/`siteurl`
> plus `wp search-replace`.

### 7.1 Base options

```bash
cd /root/Project/Ollmh

wp option update blogdescription "Faith-Based Healthcare Serving Mwea, Kirinyaga County"
wp option update timezone_string "Africa/Nairobi"
wp option update date_format "j F Y"
wp option update time_format "g:i A"

# Pretty permalinks (Apache: writes .htaccess; Nginx needs a try_files block)
wp rewrite structure '/%postname%/' --hard
wp rewrite flush --hard
```

### 7.2 Remove default cruft plugins and cache artifacts

```bash
cd /root/Project/Ollmh
wp plugin delete akismet hello
rm -f wp-content/object-cache.php wp-content/advanced-cache.php wp-content/db.php
```

### 7.3 Commit the working baseline

```bash
cd /root/Project/Ollmh
git add -A
git commit -m "Fresh WordPress install: empty OLLMH database, new salts, clean baseline"
```

---

## 8. Step 7 — Implement the OLLMH build spec from `ollmh-wayback-snapshot`

The instruction source of truth is the **pulled** repo, not the local copy:

```bash
cd /root/Project

# Pull the OLLMH project repo so the docs + seeders are available locally on the VPS
git clone git@github.com:wagura-maurice/ollmh-wayback-snapshot.git /root/Project/ollmh-wayback-snapshot
# (or if already cloned: cd /root/Project/ollmh-wayback-snapshot && git pull)

# Confirm the docs are present
ls /root/Project/ollmh-wayback-snapshot/docs
```

> **Devin CLI workflow:** run Devin from `/root/Project/`. All three folders
> (`wardwatch2027`, `Ollmh`, `ollmh-wayback-snapshot`) sit at this level.
> Instruct Devin to read `/root/Project/ollmh-wayback-snapshot/docs/` and
> implement the specs in `/root/Project/Ollmh/`.

### 8.1 Read the docs in order

1. **`ARCHITECTURAL-DECISIONS.md`** — read first; ADRs supersede conflicting
   guidance (child theme on Twenty Twenty-Five, Turnstile, no Tailwind,
   M-Pesa Daraja, WP-CLI dev-only, WordPress-native data layer).
2. **`THEME-ARCHITECTURE.md`** + **`COLOR-SCHEMA.md`** + **`FONT-SCHEMA.md`** —
   build the `ollmh-child` theme in `/root/Project/Ollmh/wp-content/themes/`.
3. **`PLUGIN-ARCHITECTURE.md`** + **`CPT-REGISTRATION-CODE.md`** —
   build `ollmh-core`, `ollmh-forms`, `ollmh-payments`, `ollmh-notifications`
   in `/root/Project/Ollmh/wp-content/plugins/`.
4. **`SETTINGS.md`** + the `seeders/` folder — seed the settings table.
5. **`CONTENT-MIGRATION.md`**, **`ASSET-MIGRATION.md`**, **`URL-MAPPING.md`**,
   **`HEADER-FOOTER-STRUCTURE.md`**, **`pages/`** — import content and wire the
   information architecture.
6. **`DEPLOYMENT.md`**, **`CRON-JOBS.md`**, **`PERFORMANCE-BUDGET.md`**,
   **`SECURITY-HARDENING.md`**, **`BACKUP-RECOVERY.md`** — ship it.

### 8.2 Build / wire the OLLMH theme and plugins

Create the theme and plugin code in `/root/Project/Ollmh/` per the specs
(work directly in the `Ollmh` repo so it is git-tracked):

```bash
mkdir -p /root/Project/Ollmh/wp-content/themes/ollmh-child
mkdir -p /root/Project/Ollmh/wp-content/plugins/ollmh-core \
         /root/Project/Ollmh/wp-content/plugins/ollmh-forms \
         /root/Project/Ollmh/wp-content/plugins/ollmh-payments \
         /root/Project/Ollmh/wp-content/plugins/ollmh-notifications
```

> For development you may symlink from a checkout of the theme/plugin repos,
> but since everything is being built fresh from the docs, the simplest
> approach is to develop **directly** in `/root/Project/Ollmh/wp-content/`.

### 8.3 Activate the plugins (creates the custom tables) then the theme

Per ADR-006 / [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md), the
`ollmh-core` plugin creates the operational custom tables on activation.
Activate core first, then the rest:

```bash
cd /root/Project/Ollmh

wp plugin activate ollmh-core ollmh-forms ollmh-payments ollmh-notifications
wp theme activate ollmh-child
```

Verify the OLLMH tables were created:

```bash
mysql -e "USE ollmh; SHOW TABLES;" | head -30   # expect wp_settings, wp_applications, ... (see docs/ERD.md)
```

### 8.4 Run the seeders

The `ollmh-wayback-snapshot` repo ships seeders under `seeders/`. Seed them
with `wp eval` (repeat for each seeder as it is added):

```bash
cd /root/Project/Ollmh

wp eval '
  require_once "/root/Project/ollmh-wayback-snapshot/seeders/class-seeder-base.php";
  require_once "/root/Project/ollmh-wayback-snapshot/seeders/class-ollmh-settings-seeder.php";
  $result = (new OLLMH_Settings_Seeder())->run();
  var_export($result);
'
```

> The settings seeder only inserts keys that do not yet exist (insert-only
> upsert) — it is safe to re-run. For repeated runs, prefer registering a
> proper WP-CLI command (`wp ollmh seed settings`) in `ollmh-core`.

Verify seeded values:

```bash
mysql -e "USE ollmh; SELECT item, default_value FROM wp_settings WHERE group_name='general';"
```

### 8.5 Import the archived content, assets, and URL mapping

With the baseline live, run the content pipeline (all WP-CLI scripts are
dev-only per ADR-005; details in the referenced docs):

1. **Assets** — migrate ~133 archive images into the media library and
   generate the URL map file (`docs/ASSET-MIGRATION.md`).
2. **Content** — extract/clean/insert pages and CPT content from the archived
   HTML into WordPress (`docs/CONTENT-MIGRATION.md`). The archived HTML lives
   in `web.archive.org/` and `docs/pages/` of the `ollmh-wayback-snapshot`
   repo.
3. **Redirects** — import the old `.html` → new permalink map into the
   Redirection plugin (CSV) or `.htaccess`/nginx rules (`docs/URL-MAPPING.md`).

### 8.6 Server configuration

Once the site code is ready, deploy the working copy to the web root and wire
up the server (full details in [`DEPLOYMENT.md`](./DEPLOYMENT.md)):

```bash
# Example — copy the built project into the web root
sudo rsync -a /root/Project/Ollmh/ /var/www/html/ollmh/
sudo chown -R www-data:www-data /var/www/html/ollmh

# Nginx vhost for the OLLMH site (WordPress permalinks)
sudo nano /etc/nginx/sites-available/ollmh
#   server_name ollmh.local;
#   root /var/www/html/ollmh;
#   location / { try_files $uri $uri/ /index.php?$args; }
sudo ln -s /etc/nginx/sites-available/ollmh /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# System cron (DISABLE_WP_CRON is set) — see docs/CRON-JOBS.md
(crontab -l 2>/dev/null; echo "* * * * * /usr/bin/php8.4 /var/www/html/ollmh/wp-cron.php >/dev/null 2>&1") | crontab -
```

---

## 9. Step 8 — Verification checklist

```bash
cd /root/Project/Ollmh

# Independence from source
mysql -e "SHOW DATABASES;"                                   # ollmh present; wardwatch2027 untouched
mysql -e "USE ollmh; SHOW TABLES;" | grep -c wardwatch || echo "No wardwatch tables in ollmh DB"
git log --oneline                                            # OLLMH's own history, not wardwatch's

# Fresh install state
wp core is-installed && echo "Core installed"
wp option get siteurl home
wp theme list --status=active                                # ollmh-child
wp plugin list --status=active                               # 5 generic + 4 ollmh plugins

# OLLMH data present
mysql -e "USE ollmh; SELECT COUNT(*) AS settings_seeded FROM wp_settings;"
wp eval 'echo home_url();'

# Front-end smoke test (after deployment to the web root)
curl -I http://ollmh.local/                                  # expect 200
curl -s  http://ollmh.local/ | grep -i "Our Lady of Lourdes Mwea Hospital" | head -1
```

---

## 10. Rolling back / starting over

The source clone is untouched, so restarting the whole process is trivial:

```bash
rm -rf /root/Project/Ollmh
mysql -e "DROP DATABASE ollmh; DROP USER 'ollmh'@'localhost';"
# then re-run from Step 1
```

---

## 11. Command quick reference (remote VPS)

| Goal | Command |
|---|---|
| SSH in | `ssh root@192.168.1.1` |
| Clone source | `git clone git@github.com:wagura-maurice/wardwatch2027.git /root/Project/wardwatch2027` |
| Copy into new project | `cp -r /root/Project/wardwatch2027 /root/Project/Ollmh` |
| Reset git | `rm -rf /root/Project/Ollmh/.git && cd /root/Project/Ollmh && git init && git add . && git commit -m "Initialize OLLMH project: fresh baseline derived from wardwatch2027 code"` |
| Pull instruction repo | `git clone git@github.com:wagura-maurice/ollmh-wayback-snapshot.git /root/Project/ollmh-wayback-snapshot` |
| Strip wardwatch code | `rm -rf wp-content/plugins/wardwatch2027-* wp-content/plugins/wardwatch2027-setup*.php wp-content/plugins/wordpress-seo wp-content/themes/wardwatch2027-child wp-content/uploads/* data` |
| Quarantine config | `mv deploy.php vhost.config nginx.conf crontab.config ecosystem.config.js .local .htaccess /root/Project/_wardwatch-legacy/` |
| Restore vendor/plugins | `composer install --no-dev --optimize-autoloader && wp plugin install w3-total-cache seo-by-rank-math redirection google-site-kit broken-link-checker --activate --allow-root` |
| Fresh DB | `mysql -e "CREATE DATABASE ollmh CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE USER 'ollmh'@'localhost' IDENTIFIED BY '...'; GRANT ALL PRIVILEGES ON ollmh.* TO 'ollmh'@'localhost'; FLUSH PRIVILEGES;"` |
| Fresh wp-config | `wp config create --dbname=ollmh --dbuser=ollmh --dbpass='...' --skip-check && wp config shuffle-salts` |
| Fresh install | `wp core install --url="http://ollmh.local" --title="Our Lady of Lourdes Mwea Hospital" --admin_user=ollmh-admin --admin_password='...' --admin_email=admin@ourladyoflourdesmweahospital.org --skip-email` |
| Permalinks | `wp rewrite structure '/%postname%/' --hard && wp rewrite flush --hard` |
| Activate OLLMH code | `wp plugin activate ollmh-core ollmh-forms ollmh-payments ollmh-notifications && wp theme activate ollmh-child` |
| Seed settings | `wp eval 'require_once "/root/Project/ollmh-wayback-snapshot/seeders/class-seeder-base.php"; require_once "/root/Project/ollmh-wayback-snapshot/seeders/class-ollmh-settings-seeder.php"; (new OLLMH_Settings_Seeder())->run();'` |
| Deploy to web root | `sudo rsync -a /root/Project/Ollmh/ /var/www/html/ollmh/` |
| Rollback | `rm -rf /root/Project/Ollmh && mysql -e "DROP DATABASE ollmh; DROP USER 'ollmh'@'localhost';"` |