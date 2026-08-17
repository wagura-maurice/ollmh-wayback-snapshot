# Deployment

> This document covers production deployment for the OLLMH WordPress site —
> hosting requirements, deployment process, and staging/production workflow.
>
> **Related:** [`ENVIRONMENT-SETUP.md`](./ENVIRONMENT-SETUP.md) for local
> dev, [`SECURITY-HARDENING.md`](./SECURITY-HARDENING.md) for security.

---

## 1. Hosting requirements

### Minimum server specs

| Resource | Minimum | Recommended |
|---|---|---|
| PHP | 8.1 | 8.2+ |
| MySQL | 8.0 | 8.0+ (or MariaDB 10.6+) |
| RAM | 2GB | 4GB+ |
| Storage | 20GB | 50GB+ (for media uploads) |
| Bandwidth | 50GB/month | 100GB+/month |

### Required PHP extensions

- `curl` (M-Pesa API, Turnstile verification)
- `gd` or `imagick` (image processing)
- `mbstring` (multi-byte string handling)
- `xml` (WordPress core)
- `mysqli` (database)
- `zip` (plugin/theme installation)
- `openssl` (encryption for secrets)
- `opcache` (performance)

### Recommended hosting providers (Kenya/Africa context)

| Provider | Type | Notes |
|---|---|---|
| Truehost Cloud | Shared/VPS | Kenya-based, affordable, local support |
| Sasahost | Shared/VPS | Kenya-based, .ke domain registration |
| HostPinnacle | Shared/VPS | Kenya-based, good uptime |
| Cloudways | Managed VPS | DigitalOcean/Linode/AWS Vultr backends, managed WP |
| Cloudflare Pages | Static/Edge | For static assets only (not full WP hosting) |

**Recommendation:** A managed VPS (Cloudways or Truehost VPS) is
preferred for better performance and control. However, **cPanel shared
hosting is confirmed feasible** for all OLLMH functionality including the
optional M-Pesa Daraja G2 API integration (see
[`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md) → ADR-004).
The Daraja G2 API operates over standard HTTPS REST calls and requires
only PHP with cURL — no DNS changes, server migration, or special
infrastructure. A WP-Cron fallback mechanism ensures payment
confirmation is not lost if Daraja callbacks fail under shared hosting
load. Shared hosting is acceptable for the initial launch; upgrade to
VPS if performance or callback reliability becomes an issue.

---

## 2. Domain and DNS

| Record | Type | Value | Purpose |
|---|---|---|---|
| `ourladyoflourdesmweahospital.org` | A | Server IP | Main site |
| `www` | CNAME | `ourladyoflourdesmweahospital.org` | WWW redirect |
| `mail` | A | Mail server IP | Email (if self-hosted) |
| `@` | MX | Mail server | Email routing |

**Cloudflare:** Route DNS through Cloudflare for:
- Free SSL certificate
- DDoS protection
- WAF (Web Application Firewall)
- CDN (content delivery network)
- Turnstile (bot protection — see [`SETTINGS.md`](./SETTINGS.md))

---

## 3. SSL configuration

SSL is **required** — WordPress, M-Pesa API, and Turnstile all require HTTPS.

### Option A: Cloudflare SSL (recommended)

1. Set Cloudflare SSL mode to "Full" (or "Full (strict)" if origin has a cert)
2. Cloudflare provides the edge certificate automatically
3. Install a Let's Encrypt certificate on the origin server for strict mode

### Option B: Let's Encrypt (direct)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-apache

# Obtain certificate
sudo certbot --apache -d ourladyoflourdesmweahospital.org -d www.ourladyoflourdesmweahospital.org

# Auto-renewal is set up by Certbot
```

### WordPress SSL settings

```php
// wp-config.php — force SSL in admin
define('FORCE_SSL_ADMIN', true);
```

---

## 4. Deployment process

> **Architectural constraint:** WP-CLI is available in development only,
> not on production (cPanel shared hosting). See
> [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md) → ADR-005.
> The deployment process below uses WP-CLI in dev/staging and cPanel
> tools (File Manager, phpMyAdmin) + WordPress admin UI on production.

### Staging → Production workflow

```
Local Dev (Docker, WP-CLI) → Staging (staging.ollmh.org, WP-CLI) → Production (cPanel, no WP-CLI)
```

### Step-by-step deployment

#### Phase 1: Prepare in dev/staging (WP-CLI available)

1. **Export database from staging:**
   ```bash
   wp db export staging-export.sql
   ```

2. **Search/replace staging URLs with production URLs:**
   ```bash
   wp search-replace 'staging.ollmh.org' 'ourladyoflourdesmweahospital.org'
   wp db export staging-export-final.sql
   ```

3. **Create a tarball of custom theme and plugins:**
   ```bash
   tar -czf ollmh-deploy.tar.gz \
     wp-content/themes/ollmh-child \
     wp-content/plugins/ollmh-core \
     wp-content/plugins/ollmh-forms \
     wp-content/plugins/ollmh-notifications
   # Note: ollmh-payments is optional — include only if client has approved M-Pesa
   ```

4. **Export content via WordPress admin (Tools → Export):**
   - Export all content (pages, posts, CPTs, media)
   - This produces a WXR XML file as a backup/alternative to DB import

#### Phase 2: Deploy to production (cPanel — no WP-CLI)

5. **Backup current production:**
   - cPanel → phpMyAdmin → select database → Export → save `.sql` file
   - cPanel → File Manager → compress `wp-content/` to `backup-pre-deploy.zip`

6. **Upload theme and plugins via cPanel File Manager:**
   - cPanel → File Manager → `wp-content/themes/`
   - Upload `ollmh-deploy.tar.gz`
   - Extract (cPanel extracts tar.gz and zip files)
   - Move theme to `wp-content/themes/ollmh-child/`
   - Move plugins to `wp-content/plugins/ollmh-*/`
   - Delete the uploaded `.tar.gz` file

   **Alternative:** Upload individual files via FTP (FileZilla) if
   cPanel File Manager has upload size limits.

7. **Import database via phpMyAdmin:**
   - cPanel → phpMyAdmin → select production database
   - Import → choose `staging-export-final.sql` → Go
   - If the database is large (> 50MB), use BigDump or split the SQL file

   **Alternative (no DB import):** If the production database already
   has content and you only need to deploy code changes:
   - Skip DB import
   - Use WordPress admin → Tools → Import → upload WXR XML file from step 4

8. **Search/replace URLs if needed (if DB import was used):**
   - Install "Better Search Replace" plugin via WP admin → Plugins → Add New
   - WP admin → Tools → Better Search Replace
   - Search: `staging.ollmh.org` → Replace: `ourladyoflourdesmweahospital.org`
   - Select all tables → Run dry run first, then live run
   - Uninstall the plugin after use

#### Phase 3: Activate and configure (WordPress admin UI)

9. **Activate theme:**
   - WP admin → Appearance → Themes → Activate "OLLMH Child"

10. **Activate plugins:**
    - WP admin → Plugins → Activate each OLLMH plugin
    - Plugin activation triggers `register_activation_hook()` which
      creates all database tables — identical to `wp plugin activate`

11. **Flush rewrite rules:**
    - WP admin → Settings → Permalinks → scroll to bottom → Save Changes
    - This flushes the rewrite rules cache — identical to `wp rewrite flush`

12. **Clear cache:**
    - WP admin → Performance → General Settings → Empty All Caches (W3 Total Cache)
    - Or: WP admin → Performance → Empty All Caches

13. **Configure settings:**
    - WP admin → OLLMH Settings → enter production values for all settings
    - (Hospital name, contact info, Turnstile keys, SMTP settings, etc.)

#### Phase 4: Post-deployment verification

14. **Verify the site:**
    - Visit the homepage → verify it loads
    - Test all forms (contact, appointment, application)
    - Check redirects (old `.html` URLs → new URLs) via WP admin → Tools → Redirection
    - Verify SSL certificate is valid (browser padlock icon)
    - Check `wp-content/debug.log` for errors
    - Run a speed test (PagePageSpeed Insights)

15. **Monitor for 48 hours:**
    - Check error log via cPanel → Errors or cPanel → Logs
    - Verify forms are submitting correctly
    - Check that cron jobs are running (WP admin → OLLMH Settings → System Status)

---

## 5. Production `wp-config.php`

```php
<?php
// Database
define('DB_NAME', 'ollmh_prod');
define('DB_USER', 'ollmh_user');
define('DB_PASSWORD', 'STRONG_PASSWORD_HERE');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', 'utf8mb4_unicode_ci');
$table_prefix = 'wp_';

// Authentication keys (generate at https://api.wordpress.org/secret-key/1.1/salt/)
define('AUTH_KEY',         '...');
define('SECURE_AUTH_KEY',  '...');
define('LOGGED_IN_KEY',    '...');
define('NONCE_KEY',        '...');
define('AUTH_SALT',        '...');
define('SECURE_AUTH_SALT', '...');
define('LOGGED_IN_SALT',   '...');
define('NONCE_SALT',       '...');

// Debug — OFF in production
define('WP_DEBUG', false);
define('WP_DEBUG_LOG', false);
define('WP_DEBUG_DISPLAY', false);

// Security
define('DISALLOW_FILE_EDIT', true);   // No theme/plugin editor in admin
define('DISALLOW_FILE_MODS', false);   // Allow plugin installation
define('FORCE_SSL_ADMIN', true);       // Force SSL in admin
define('WP_AUTO_UPDATE_CORE', 'minor'); // Auto-update minor WP releases

// Performance
define('WP_MEMORY_LIMIT', '256M');
define('WP_MAX_MEMORY_LIMIT', '512M');
define('WP_POST_REVISIONS', 5);

// Cron — use real cron in production
define('DISABLE_WP_CRON', true);
// Set up system cron: */5 * * * * curl -s https://ollmh.org/wp-cron.php?doing_wp_cron > /dev/null 2>&1

// SSL
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}

// Path
define('ABSPATH', dirname(__FILE__) . '/');

require_once ABSPATH . 'wp-settings.php';
```

---

## 6. Web server configuration

### Nginx (recommended)

```nginx
server {
    listen 80;
    server_name ourladyoflourdesmweahospital.org www.ourladyoflourdesmweahospital.org;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ourladyoflourdesmweahospital.org www.ourladyoflourdesmweahospital.org;

    root /var/www/ollmh;
    index index.php index.html;

    # SSL
    ssl_certificate /etc/letsencrypt/live/ollmh.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ollmh.org/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Gzip
    gzip on;
    gzip_types text/css application/javascript application/json;

    # Browser caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # WordPress
    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    # PHP
    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass unix:/run/php/php8.2-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }

    # Deny sensitive files
    location ~ /\. { deny all; }
    location ~ /(wp-config\.php|readme\.html|license\.txt) { deny all; }
    location ~ /wp-content/uploads/.*\.php$ { deny all; }
}
```

### Apache (alternative)

```apache
<VirtualHost *:80>
    ServerName ourladyoflourdesmweahospital.org
    Redirect permanent / https://ourladyoflourdesmweahospital.org/
</VirtualHost>

<VirtualHost *:443>
    ServerName ourladyoflourdesmweahospital.org
    DocumentRoot /var/www/ollmh

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/ollmh.org/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/ollmh.org/privkey.pem

    <Directory /var/www/ollmh>
        AllowOverride All
        Require all granted
    </Directory>

    # Security headers
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
</VirtualHost>
```

---

## 7. File permissions

```bash
# Set ownership
sudo chown -R www-data:www-data /var/www/ollmh

# Set directory permissions
find /var/www/ollmh -type d -exec chmod 755 {} \;

# Set file permissions
find /var/www/ollmh -type f -exec chmod 644 {} \;

# wp-config.php should be 600 (owner read/write only)
chmod 600 /var/www/ollmh/wp-config.php

# .htaccess should be 644
chmod 644 /var/www/ollmh/.htaccess
```

---

## 8. Post-deployment checklist

- [ ] WordPress loads at `https://ourladyoflourdesmweahospital.org`
- [ ] SSL certificate is valid (no browser warnings)
- [ ] All 20 pages load without 404 errors
- [ ] All 17 old `.html` URLs redirect with 301
- [ ] Contact form submits and email is received
- [ ] Appointment booking form works
- [ ] Application form multi-step works
- [ ] M-Pesa STK Push works in production mode
- [ ] Turnstile captcha validates
- [ ] Admin login works at `/wp-admin/`
- [ ] All CPT admin menus are visible
- [ ] Settings page shows all 19 groups
- [ ] XML sitemap is generated at `/sitemap_index.xml`
- [ ] Google Site Kit is connected
- [ ] Rank Math SEO is configured
- [ ] W3 Total Cache is active
- [ ] Backups are scheduled (see [`BACKUP-RECOVERY.md`](./BACKUP-RECOVERY.md))
- [ ] `debug.log` is empty (no PHP errors)
- [ ] PageSpeed score is 80+ on mobile
