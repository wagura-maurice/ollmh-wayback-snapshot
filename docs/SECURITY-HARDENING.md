# Security Hardening

> This document defines the security hardening strategy for the OLLMH
> WordPress site — beyond the Turnstile bot protection covered in
> [`SETTINGS.md`](./SETTINGS.md).
>
> **Related:** [`DEPLOYMENT.md`](./DEPLOYMENT.md) for server config,
> [`SETTINGS.md`](./SETTINGS.md) → `security` and `auth` groups.

---

## 1. Security layers

| Layer | Tool/Config | Purpose |
|---|---|---|
| Edge | Cloudflare (DNS, WAF, DDoS, SSL) | Block attacks before they reach the server |
| Application | WordPress core + plugins + theme | Secure code, authentication, authorization |
| Server | Nginx/Apache + PHP-FPM + MySQL | File permissions, security headers, PHP config |
| Data | Database + backups | Encryption, backup verification |
| Monitoring | Security plugin + logs | Detect and respond to threats |

---

## 2. Cloudflare configuration

### 2.1 SSL/TLS

- SSL mode: **Full (strict)** — requires a valid cert on the origin server
- Always Use HTTPS: **On** — redirects all HTTP to HTTPS
- Minimum TLS Version: **1.2** — disable TLS 1.0/1.1
- Automatic HTTPS Rewrites: **On** — fixes mixed content

### 2.2 WAF (Web Application Firewall)

- Enable Cloudflare WAF (free plan includes basic rules)
- Enable managed rules: WordPress, OWASP
- Block known bad IPs automatically
- Security level: **Medium** (challenge suspicious visitors)

### 2.3 DDoS protection

- Enable DDoS protection (included in free plan)
- Enable "I'm Under Attack" mode only during active attacks
- Rate limiting: Configure rules for `/wp-login.php` and form endpoints

### 2.4 Bot protection

- Cloudflare Turnstile on all public forms (see [`SETTINGS.md`](./SETTINGS.md) → `security` group)
- Bot Fight Mode: **On** (free plan) — challenges known bots

### 2.5 Page rules

| Pattern | Setting | Purpose |
|---|---|---|
| `*ollmh.org/wp-admin/*` | Security Level: High | Extra protection for admin |
| `*ollmh.org/wp-login.php` | Security Level: High | Extra protection for login |
| `*ollmh.org/wp-content/uploads/*` | Cache Level: Cache Everything | Cache media files |

---

## 3. WordPress core security

### 3.1 `wp-config.php` hardening

```php
// Disable file editor in admin
define('DISALLOW_FILE_EDIT', true);

// Force SSL in admin
define('FORCE_SSL_ADMIN', true);

// Limit revisions (reduces database exposure)
define('WP_POST_REVISIONS', 5);

// Auto-update core
define('WP_AUTO_UPDATE_CORE', 'minor');

// Disable unnecessary features
define('EMPTY_TRASH_DAYS', 7);  // Auto-empty trash after 7 days
```

### 3.2 Remove WordPress version

```php
// functions.php
remove_action('wp_head', 'wp_generator');
remove_action('wp_head', 'wlwmanifest_link');
remove_action('wp_head', 'rsd_link');
```

### 3.3 Disable XML-RPC

```php
// functions.php — disable XML-RPC
add_filter('xmlrpc_enabled', '__return_false');
add_filter('wp_xmlrpc_server_class', '__return_false');
```

```nginx
# Nginx — block xmlrpc.php
location = /xmlrpc.php { deny all; }
```

### 3.4 Disable REST API for non-authenticated users (optional)

If the REST API is only used for form submissions (which use custom
endpoints), disable the default WP REST API for non-authenticated users:

```php
// Only if you don't need the default REST API
add_filter('rest_authentication_errors', function($result) {
    if (!is_user_logged_in() && !strpos($_SERVER['REQUEST_URI'], '/ollmh/v1/')) {
        return new WP_Error('rest_forbidden', 'REST API restricted.', ['status' => 403]);
    }
    return $result;
});
```

> **Note:** This is optional. The custom `ollmh/v1` endpoints need to be
> accessible without authentication (they use Turnstile instead).

### 3.5 Login security

- **Strong passwords:** Enforce via WordPress default (minimum strength indicator)
- **2FA:** Enable if `two_factor_auth_enabled` setting is `1` (use [Two Factor](https://wordpress.org/plugins/two-factor/) plugin)
- **Login attempts:** Limit to `max_login_attempts` setting (default: 5) with `lockout_duration_minutes` lockout (default: 15 min)
- **Hide login URL:** Optionally change `/wp-admin/` to a custom path (use [WPS Hide Login](https://wordpress.org/plugins/wps-hide-login/))
- **Disable login hints:** Remove "Invalid username" / "Invalid password" messages:
  ```php
  add_filter('login_errors', function() {
      return 'Invalid login credentials.';
  });
  ```

---

## 4. Code security

### 4.1 SQL injection prevention

All database queries use `$wpdb->prepare()` with parameterized queries:

```php
// ✅ Correct
$wpdb->get_var($wpdb->prepare(
    "SELECT id FROM {$table} WHERE item = %s",
    $item
));

// ❌ Wrong (SQL injection vulnerable)
$wpdb->get_var("SELECT id FROM {$table} WHERE item = '{$item}'");
```

### 4.2 XSS prevention

All output is escaped:

```php
// ✅ Correct
echo esc_html($user_input);
echo esc_attr($attribute_value);
echo esc_url($url);
echo wp_kses_post($html_content);

// ❌ Wrong (XSS vulnerable)
echo $user_input;
```

### 4.3 CSRF prevention

All forms include a WordPress nonce:

```php
// Generate nonce
wp_nonce_field('ollmh_contact_form', 'ollmh_nonce');

// Verify nonce on submission
if (!wp_verify_nonce($_POST['ollmh_nonce'], 'ollmh_contact_form')) {
    wp_die('Security check failed.');
}
```

For REST API endpoints, use the `X-WP-Nonce` header:

```php
// JS: include nonce in fetch headers
headers: {
  'X-WP-Nonce': ollmhConfig.nonce,
  'Content-Type': 'application/json',
}

// PHP: verify in REST API callback
if (!wp_verify_nonce($request->get_header('x-wp-nonce'), 'wp_rest')) {
    return new WP_Error('forbidden', 'Invalid nonce.', ['status' => 403]);
}
```

### 4.4 File upload security

- Validate file type via `wp_check_filetype_and_ext()` (not just extension)
- Validate MIME type via `finfo_file()` (checks actual file content)
- Limit file size (2MB for photos, 5MB for documents)
- Store uploads in `wp-content/uploads/` (never in theme/plugin directories)
- Disable PHP execution in uploads directory:
  ```nginx
  # Nginx
  location ~ /wp-content/uploads/.*\.php$ { deny all; }
  ```
  ```apache
  # Apache — wp-content/uploads/.htaccess
  <Files *.php>
    Deny from all
  </Files>
  ```

### 4.5 Secret storage

All secrets (SMTP password, M-Pesa keys, Turnstile secret) are stored in
`wp_settings` with `type = 'secret'`. The admin UI masks these values
and they are never returned by the public settings API.

For additional encryption at rest, use `openssl_encrypt()` with a key
stored in `wp-config.php`:

```php
// wp-config.php
define('OLLMH_ENCRYPTION_KEY', '32-byte-random-key-here...');

// Encryption helper
function ollmh_encrypt(string $value): string {
    $key = base64_decode(OLLMH_ENCRYPTION_KEY);
    $iv = openssl_random_pseudo_bytes(16);
    $encrypted = openssl_encrypt($value, 'aes-256-cbc', $key, 0, $iv);
    return base64_encode($iv . $encrypted);
}

function ollmh_decrypt(string $value): string {
    $key = base64_decode(OLLMH_ENCRYPTION_KEY);
    $data = base64_decode($value);
    $iv = substr($data, 0, 16);
    $encrypted = substr($data, 16);
    return openssl_decrypt($encrypted, 'aes-256-cbc', $key, 0, $iv);
}
```

---

## 5. HTTP security headers

### Nginx

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://challenges.cloudflare.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://challenges.cloudflare.com;" always;
```

### Apache

```apache
<IfModule mod_headers.c>
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
</IfModule>
```

### Header meanings

| Header | Purpose |
|---|---|
| `X-Frame-Options: SAMEORIGIN` | Prevent clickjacking (site can't be embedded in iframes on other domains) |
| `X-Content-Type-Options: nosniff` | Prevent MIME type sniffing |
| `Strict-Transport-Security` | Force HTTPS for 1 year (HSTS) |
| `Referrer-Policy` | Control what referrer info is sent |
| `Content-Security-Policy` | Control what resources can be loaded |
| `Permissions-Policy` | Disable unnecessary browser APIs (geolocation, microphone, camera) |

---

## 6. File permissions

```bash
# WordPress core files
find /var/www/ollmh -type d -exec chmod 755 {} \;
find /var/www/ollmh -type f -exec chmod 644 {} \;

# wp-config.php — owner only
chmod 600 /var/www/ollmh/wp-config.php

# .htaccess — readable
chmod 644 /var/www/ollmh/.htaccess

# wp-content — writable by web server
chown -R www-data:www-data /var/www/ollmh/wp-content/
```

---

## 7. Security plugins

| Plugin | Purpose | Cost |
|---|---|---|
| [Wordfence](https://www.wordfence.com/) | Firewall, malware scanner, login security | Free (Premium available) |
| [Solid Security](https://solidwp.com/security/) (formerly iThemes Security) | WordPress hardening, file change detection | Free (Pro available) |

**Recommendation:** Install **Wordfence** (free) for:
- Web application firewall
- Malware scanner (daily scan)
- Login attempt limiting
- Two-factor authentication (premium)

---

## 8. Update policy

| Component | Update frequency | Auto-update? |
|---|---|---|
| WordPress core (minor) | As released | Yes (`WP_AUTO_UPDATE_CORE: minor`) |
| WordPress core (major) | Test on staging first | No (manual) |
| Plugins | As released | No (test on staging first) |
| Theme | As released | No (test on staging first) |
| PHP | When hosting provider supports | No (coordinate with hosting) |
| MySQL | When hosting provider supports | No (coordinate with hosting) |

**Process:**
1. Test update on staging
2. If staging is stable → deploy to production
3. Check `debug.log` for errors after update
4. Run testing checklist (see [`TESTING-PLAN.md`](./TESTING-PLAN.md))

---

## 9. Monitoring and incident response

### Monitoring

- **Wordfence alerts:** Email on blocked login attempts, malware detection, file changes
- **Cloudflare alerts:** Email on DDoS attacks, WAF rule triggers
- **Server monitoring:** CPU/memory/disk alerts (use Uptime Robot or server monitoring tool)
- `debug.log` monitoring: Check daily for PHP errors

### Incident response

1. **If site is hacked:**
   - Take site offline (maintenance mode)
   - Restore from most recent backup
   - Scan all files with Wordfence
   - Change all passwords (admin, database, FTP, hosting)
   - Identify and patch the vulnerability
   - Bring site back online

2. **If DDoS attack:**
   - Enable Cloudflare "I'm Under Attack" mode
   - Monitor server resources
   - Wait for attack to subside
   - Disable "I'm Under Attack" mode

3. **If data breach:**
   - Notify hospital administration immediately
   - Assess what data was exposed (patient data, application data, payment data)
   - Notify affected individuals if required by law
   - Patch the vulnerability
   - Document the incident
