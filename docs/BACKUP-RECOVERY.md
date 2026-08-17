# Backup & Recovery

> This document defines the backup strategy, recovery procedures, and
> retention policy for the OLLMH WordPress site.
>
> **Related:** [`DEPLOYMENT.md`](./DEPLOYMENT.md) for server setup,
> [`CRON-JOBS.md`](./CRON-JOBS.md) for scheduled backup tasks.

---

## 1. What to back up

| Component | Contents | Frequency | Retention |
|---|---|---|---|
| Database | All WordPress core tables (CPT content, users, terms) + the ~26 retained custom tables (ADR-006) | Daily | 30 days |
| Media uploads | `wp-content/uploads/` (all uploaded images, PDFs) | Weekly | 90 days |
| Theme + plugins | `wp-content/themes/ollmh-child/` + `wp-content/plugins/ollmh-*/` | On change | 90 days |
| `wp-config.php` | Database credentials, salts, settings | On change | Indefinite (version controlled) |
| Nginx/Apache config | Server configuration files | On change | Indefinite |

---

## 2. Backup strategy

### 2.1 Plugin-based backups (recommended)

Install [UpdraftPlus](https://updraftplus.com/) (free) or
[BackWPup](https://wordpress.org/plugins/backwpup/) (free):

**UpdraftPlus configuration:**
- Schedule: Daily database, weekly files
- Storage: Cloud (Google Drive, Dropbox, or AWS S3) — **not** on the same server
- Retention: Keep 30 database backups, 12 file backups
- Encryption: Enable for database backups (AES-256)
- Email on completion: Send to `admin_email` setting

### 2.2 Server-level backups (additional layer)

If using a VPS, configure server-level snapshots via the hosting provider:
- DigitalOcean: Weekly automated snapshots ($0.05/GB/month)
- Linode: Weekly automated backups ($2/month)
- AWS: EBS snapshots (configured via AWS CLI or console)
- Truehost/Sasahost: Check if backups are included in the plan

### 2.3 Manual backups (before changes)

Before any major change (plugin update, theme update, database migration):

```bash
# Database backup
wp db export backup-$(date +%Y%m%d-%H%M%S).sql

# Files backup
tar -czf backup-files-$(date +%Y%m%d-%H%M%S).tar.gz \
  wp-content/themes/ollmh-child \
  wp-content/plugins/ollmh-* \
  wp-content/uploads/
```

---

## 3. Backup schedule

| Backup type | Frequency | Time | Storage | Retention |
|---|---|---|---|---|
| Database (automated) | Daily | 2:00 AM | Cloud (Google Drive) | 30 days |
| Files (automated) | Weekly | Sunday 3:00 AM | Cloud (Google Drive) | 90 days |
| Server snapshot | Weekly | Sunday 4:00 AM | Hosting provider | 4 weeks |
| Manual (pre-deploy) | On demand | Before changes | Local + cloud | Indefinite |

---

## 4. Recovery procedures

### 4.1 Full site recovery (from UpdraftPlus)

1. Log in to WordPress admin (if accessible)
2. Go to Settings → UpdraftPlus Backups → Restore
3. Select the backup date to restore from
4. Choose what to restore: Database, Files, Both
5. Click "Restore"
6. Wait for restoration to complete (5–30 minutes depending on size)
7. Verify the site is functional

### 4.2 Full site recovery (if WordPress admin is inaccessible)

1. Download the backup files from cloud storage (Google Drive)
2. Upload to the server:
   ```bash
   scp backup-*.sql user@server:/tmp/
   scp backup-files-*.tar.gz user@server:/tmp/
   ```
3. Restore files:
   ```bash
   cd /var/www/ollmh
   tar -xzf /tmp/backup-files-*.tar.gz -C wp-content/
   ```
4. Restore database:
   ```bash
   wp db import /tmp/backup-*.sql
   ```
5. Update URLs if domain changed:
   ```bash
   wp search-replace 'old-domain.com' 'new-domain.com'
   ```
6. Flush rewrite rules:
   ```bash
   wp rewrite flush
   wp cache flush
   ```

### 4.3 Database-only recovery

```bash
# Stop web server to prevent writes during recovery
sudo systemctl stop nginx

# Restore database
wp db import /tmp/backup-database.sql

# Start web server
sudo systemctl start nginx

# Flush cache
wp cache flush
```

### 4.4 Single table recovery

If only one table is corrupted (e.g., `wp_settings`):

```bash
# Export the specific table from backup
wp db export --tables=wp_settings backup-settings.sql

# Drop the corrupted table
wp db query "DROP TABLE wp_settings;"

# Import from backup
wp db import backup-settings.sql
```

### 4.5 File-only recovery (theme or plugin)

```bash
# Restore theme
rm -rf /var/www/ollmh/wp-content/themes/ollmh-child
tar -xzf /tmp/backup-files-*.tar.gz -C /var/www/ollmh/wp-content/ wp-content/themes/ollmh-child

# Or restore a single plugin
rm -rf /var/www/ollmh/wp-content/plugins/ollmh-core
tar -xzf /tmp/backup-files-*.tar.gz -C /var/www/ollmh/wp-content/ wp-content/plugins/ollmh-core
```

---

## 5. Recovery Time Objective (RTO) and Recovery Point Objective (RPO)

| Metric | Target | Notes |
|---|---|---|
| **RTO** (how fast to recover) | < 4 hours | From backup to fully operational |
| **RPO** (max data loss) | < 24 hours | Daily backups = max 1 day of lost data |

For critical patient-facing features (appointments, applications), the RPO
could be reduced to < 1 hour by increasing backup frequency to hourly for
the relevant tables only.

---

## 6. Backup verification

Backups are useless if they can't be restored. Verify monthly:

1. **Monthly restore test:**
   - Download the most recent backup
   - Restore to a test environment (local Docker or staging)
   - Verify the site loads
   - Verify all forms work
   - Verify admin login works
   - Document the test result

2. **Backup integrity check:**
   - Check backup file sizes are reasonable (not 0 KB)
   - Check backup timestamps are recent
   - Check cloud storage has the expected number of backups
   - Verify backup encryption (if enabled)

---

## 7. Emergency contacts

| Role | Responsibility | Contact |
|---|---|---|
| Hospital IT Administrator | First responder, restores from backup | (set in `admin_email` setting) |
| Hosting provider support | Server-level recovery | (hosting provider's support number) |
| Cloudflare account admin | DNS/SSL/WAF recovery | (Cloudflare dashboard access) |
| Domain registrar | Domain renewal/recovery | (registrar's support) |
| Developer/agency | Code-level fixes | (developer's contact) |

Keep this information in a secure, offline location (not only on the
server that might need recovery).

---

## 8. Disaster recovery plan

### Scenario: Server failure (complete loss)

1. Provision a new server (same specs as original)
2. Install Docker, Nginx, PHP, MySQL
3. Deploy WordPress from version control (Git repository)
4. Restore database from cloud backup
5. Restore media uploads from cloud backup
6. Update DNS to point to new server IP
7. Verify SSL certificate is active (Cloudflare or Let's Encrypt)
8. Run full testing checklist (see [`TESTING-PLAN.md`](./TESTING-PLAN.md))

**Estimated time:** 4–8 hours (depending on server provisioning speed and backup size)

### Scenario: Database corruption

1. Take site offline (maintenance mode)
2. Restore database from most recent backup
3. Verify data integrity
4. Bring site back online
5. Check for any data loss (compare with backup)

**Estimated time:** 1–2 hours

### Scenario: Hacked site

1. Take site offline immediately
2. Restore from most recent clean backup (before the hack)
3. Change all passwords (WordPress admin, database, FTP, hosting, Cloudflare)
4. Scan all files with Wordfence
5. Identify and patch the vulnerability
6. Bring site back online
7. Monitor for re-infection

**Estimated time:** 4–12 hours (depending on severity)

### Scenario: Accidental content deletion

1. Identify what was deleted (page, post, media, settings)
2. Restore from most recent backup (single table or full database)
3. Verify restored content is correct

**Estimated time:** 30 minutes – 2 hours

---

## 9. Backup storage locations

**Never store backups only on the same server as the website.** If the
server fails, the backups are lost too.

| Location | Purpose | Encryption |
|---|---|---|
| Cloud storage (Google Drive) | Primary off-site backup | Yes (UpdraftPlus encryption) |
| Server (local copy) | Quick restore access | No (server is already secured) |
| Developer's machine | Emergency copy | Manual |
| Hosting provider snapshots | Server-level recovery | Provider-managed |

**3-2-1 rule:** Keep 3 copies of data, on 2 different media, with 1 copy off-site.
