# Environment Setup

> This document covers local development environment setup for the OLLMH
> WordPress rebuild, including Docker configuration, WordPress install,
> and developer tooling.
>
> **Related:** [`MIGRATION-PLAN.md`](./MIGRATION-PLAN.md) for the overall
> build plan, [`DEPLOYMENT.md`](./DEPLOYMENT.md) for production deployment.

---

## 1. Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Docker | 24.0+ | Container runtime |
| Docker Compose | 2.20+ | Multi-container orchestration |
| Git | 2.40+ | Version control |
| Node.js | 20 LTS | Front-end build tools (optional, for Sass/JS bundling) |
| WP-CLI | 2.9+ | WordPress command-line interface (included in Docker container) — **dev only**, not available on production (see [`ARCHITECTURAL-DECISIONS.md`](./ARCHITECTURAL-DECISIONS.md) → ADR-005) |

**OS:** macOS, Linux, or Windows with WSL2.

---

## 2. Docker setup

### `docker-compose.yml`

Create this file in the project root:

```yaml
version: '3.8'

services:
  database:
    image: mysql:8.0
    container_name: ollmh-db
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: ollmh
      MYSQL_USER: ollmh
      MYSQL_PASSWORD: ollmhpassword
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./docker/mysql/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - ollmh-network

  wordpress:
    image: wordpress:6.4-php8.2-apache
    container_name: ollmh-wp
    restart: unless-stopped
    depends_on:
      - database
    environment:
      WORDPRESS_DB_HOST: database:3306
      WORDPRESS_DB_NAME: ollmh
      WORDPRESS_DB_USER: ollmh
      WORDPRESS_DB_PASSWORD: ollmhpassword
      WORDPRESS_TABLE_PREFIX: wp_
      WORDPRESS_DEBUG: 1
      WORDPRESS_CONFIG_EXTRA: |
        define('WP_DEBUG', true);
        define('WP_DEBUG_LOG', true);
        define('WP_DEBUG_DISPLAY', false);
        define('DISALLOW_FILE_EDIT', true);
    ports:
      - "8080:80"
    volumes:
      - wp_data:/var/www/html
      - ./wp-content/themes/ollmh-child:/var/www/html/wp-content/themes/ollmh-child
      - ./wp-content/plugins/ollmh-core:/var/www/html/wp-content/plugins/ollmh-core
      - ./wp-content/plugins/ollmh-forms:/var/www/html/wp-content/plugins/ollmh-forms
      - ./wp-content/plugins/ollmh-payments:/var/www/html/wp-content/plugins/ollmh-payments
      - ./wp-content/plugins/ollmh-notifications:/var/www/html/wp-content/plugins/ollmh-notifications
      - ./docker/php/uploads.ini:/usr/local/etc/php/conf.d/uploads.ini
    networks:
      - ollmh-network

  phpmyadmin:
    image: phpmyadmin:5.2
    container_name: ollmh-pma
    restart: unless-stopped
    depends_on:
      - database
    environment:
      PMA_HOST: database
      PMA_PORT: 3306
      PMA_USER: root
      PMA_PASSWORD: rootpassword
    ports:
      - "8081:80"
    networks:
      - ollmh-network

  mailhog:
    image: mailhog/mailhog:latest
    container_name: ollmh-mailhog
    restart: unless-stopped
    ports:
      - "8025:8025"  # Web UI
      - "1025:1025"  # SMTP
    networks:
      - ollmh-network

volumes:
  db_data:
  wp_data:

networks:
  ollmh-network:
    driver: bridge
```

### `docker/php/uploads.ini`

```ini
upload_max_filesize = 64M
post_max_size = 64M
max_execution_time = 300
memory_limit = 256M
```

### `docker/mysql/init.sql`

```sql
-- Create database with correct charset
CREATE DATABASE IF NOT EXISTS ollmh CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON ollmh.* TO 'ollmh'@'%';
FLUSH PRIVILEGES;
```

---

## 3. Services overview

| Service | URL | Port | Purpose |
|---|---|---|---|
| WordPress | http://localhost:8080 | 8080 | The main WordPress site |
| phpMyAdmin | http://localhost:8081 | 8081 | Database management GUI |
| MailHog | http://localhost:8025 | 8025 | Email testing (catches all outgoing emails) |
| MySQL | localhost:3306 | 3306 | Direct database access (for CLI tools) |

**MailHog** catches all emails sent by WordPress — no real emails are sent
during local development. Configure WordPress SMTP to use `mailhog:1025`
with no encryption (see [`SETTINGS.md`](./SETTINGS.md) → `email` group).

---

## 4. First-time setup

```bash
# 1. Clone the repository
git clone https://github.com/wagura-maurice/ollmh-wayback-snapshot.git
cd ollmh-wayback-snapshot

# 2. Create the Docker volume directories
mkdir -p docker/php docker/mysql

# 3. Start the containers
docker-compose up -d

# 4. Wait for WordPress to initialize (10–15 seconds)
sleep 15

# 5. Complete WordPress installation via WP-CLI
docker exec ollmh-wp wp core install \
  --url="http://localhost:8080" \
  --title="OLLMH Dev" \
  --admin_user="admin" \
  --admin_password="admin" \
  --admin_email="admin@example.com" \
  --allow-root

# 6. Set permalink structure
docker exec ollmh-wp wp rewrite structure '/%postname%/' --allow-root
docker exec ollmh-wp wp rewrite flush --allow-root

# 7. Activate the theme (block child theme of Twenty Twenty-Five — ADR-001)
docker exec ollmh-wp wp theme activate ollmh-child --allow-root

# 8. Activate plugins (in dependency order)
docker exec ollmh-wp wp plugin activate ollmh-core --allow-root
docker exec ollmh-wp wp plugin activate ollmh-forms --allow-root
docker exec ollmh-wp wp plugin activate ollmh-notifications --allow-root
# ollmh-payments is OPTIONAL (M-Pesa) — activate only if approved (ADR-004):
docker exec ollmh-wp wp plugin activate ollmh-payments --allow-root

# 9. Install third-party plugins
docker exec ollmh-wp wp plugin install rank-math google-site-kit redirection w3-total-cache broken-link-checker --activate --allow-root

# 10. Verify the site loads
curl -s http://localhost:8080 | head -20
```

---

## 5. Daily development workflow

```bash
# Start the environment
docker-compose up -d

# Watch PHP error log
docker exec ollmh-wp tail -f /var/www/html/wp-content/debug.log

# Watch Apache access log
docker exec ollmh-wp tail -f /var/log/apache2/access.log

# Access WP-CLI
docker exec ollmh-wp wp <command> --allow-root

# Access MySQL CLI
docker exec ollmh-db mysql -uollmh -pollmhpassword ollmh

# Run the settings seeder
docker exec ollmh-wp wp eval 'OLLMH_Settings_Seeder::run();' --allow-root

# Run the content migration script
docker exec ollmh-wp wp eval-file scripts/migrate-content.php --allow-root

# Run the asset migration script
docker exec ollmh-wp wp eval-file scripts/migrate-assets.php --allow-root

# Stop the environment (keeps data)
docker-compose down

# Stop and delete all data (fresh start)
docker-compose down -v
```

---

## 6. `wp-config.php` additions

The Docker image auto-generates `wp-config.php`, but if you need to
customize it, mount a custom file or use the `WORDPRESS_CONFIG_EXTRA`
environment variable (already configured in `docker-compose.yml`).

Key settings for development:

```php
// Debug
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);    // Log to wp-content/debug.log
define('WP_DEBUG_DISPLAY', false); // Don't show errors on screen

// Prevent file editing from admin (security best practice)
define('DISALLOW_FILE_EDIT', true);

// Increase memory limit
define('WP_MEMORY_LIMIT', '256M');
define('WP_MAX_MEMORY_LIMIT', '512M');

// Cron (use real cron in production, WP-Cron in dev)
define('DISABLE_WP_CRON', false);

// Revisions
define('WP_POST_REVISIONS', 10);

// Auto-update (disable in dev)
define('WP_AUTO_UPDATE_CORE', false);
```

---

## 7. Local DNS (optional)

Add to your `/etc/hosts` file for a more realistic domain:

```
127.0.0.1  ollmh.test
```

Then update `docker-compose.yml` to use port 80 and add the hostname.

Alternatively, use [Dnsmasq](https://dnsmasq.org/) or
[Laravel Valet](https://laravel.com/docs/valet) for automatic DNS resolution.

---

## 8. Front-end build tools (optional)

If using Sass for CSS or bundling JavaScript:

```bash
# Install Node.js dependencies
cd wp-content/themes/ollmh-child
npm install

# Watch for changes during development
npm run watch

# Build for production
npm run build
```

Example `package.json` for the theme:

```json
{
  "name": "ollmh-child",
  "version": "1.0.0",
  "scripts": {
    "watch": "sass --watch assets/scss:assets/css",
    "build": "sass assets/scss:assets/css --style=compressed && terser assets/js/*.js --compress --mangle --output assets/dist/"
  },
  "devDependencies": {
    "sass": "^1.69.0",
    "terser": "^5.24.0"
  }
}
```

See [`FRONT-END-DEPENDENCIES.md`](./FRONT-END-DEPENDENCIES.md) for the
full front-end tooling strategy.

---

## 9. Database access

### phpMyAdmin
- URL: http://localhost:8081
- Login: `root` / `rootpassword`
- Database: `ollmh`

### MySQL CLI
```bash
docker exec -it ollmh-db mysql -uollmh -pollmhpassword ollmh
```

### Export database
```bash
docker exec ollmh-db mysqldump -uollmh -pollmhpassword ollmh > backup.sql
```

### Import database
```bash
docker exec -i ollmh-db mysql -uollmh -pollmhpassword ollmh < backup.sql
```

---

## 10. Troubleshooting

| Problem | Solution |
|---|---|
| Port 8080 already in use | Change `ports: "8080:80"` to `ports: "8088:80"` in docker-compose.yml |
| WordPress shows "Error establishing database connection" | Wait 15 seconds for MySQL to initialize, then restart: `docker-compose restart wordpress` |
| Permission errors on mounted volumes | Run `docker exec ollmh-wp chown -R www-data:www-data /var/www/html/wp-content/` |
| WP-CLI not found | Use `docker exec ollmh-wp wp <command> --allow-root` |
| Plugin activation fails | Check `wp-content/debug.log` for PHP errors |
| MailHog not catching emails | Set SMTP host to `mailhog:1025` in wp_settings |
