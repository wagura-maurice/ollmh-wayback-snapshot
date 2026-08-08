# URL Mapping

> This document maps all old Joomla URLs to their new WordPress
> equivalents and defines the 301 redirect strategy.
>
> **Related:** [`MIGRATION-PLAN.md`](./MIGRATION-PLAN.md) for the overall
> plan, [`SEO-STRATEGY.md`](./SEO-STRATEGY.md) for SEO implications.

---

## 1. Old URL pattern

The archived Joomla site used **SEF (Search Engine Friendly) URLs** with
`.html` extensions:

```
http://ourladyoflourdesmweahospital.org/{page-name}.html
```

No query-string URLs (`index.php?option=com_content&...`) were used in
public-facing navigation. This simplifies redirect mapping — each old URL
maps 1:1 to a new WordPress permalink.

---

## 2. Complete redirect map

### Standard pages (17 redirects)

| Old Joomla URL | New WordPress URL | Redirect type |
|---|---|---|
| `/index.html` | `/` | 301 |
| `/about-ollmh-location.html` | `/about-ollmh-location/` | 301 |
| `/administration.html` | `/administration/` | 301 |
| `/philosophy-of-care.html` | `/philosophy-of-care/` | 301 |
| `/hr-capacity-staff.html` | `/hr-capacity-staff/` | 301 |
| `/development-projects.html` | `/development-projects/` | 301 |
| `/self-sustainability-projects.html` | `/self-sustainability-projects/` | 301 |
| `/community-support.html` | `/community-support/` | 301 |
| `/upcoming-projects.html` | `/upcoming-projects/` | 301 |
| `/in-patient-dept.html` | `/in-patient-dept/` | 301 |
| `/out-patient-dept.html` | `/out-patient-dept/` | 301 |
| `/wards.html` | `/wards/` | 301 |
| `/special-medical-services.html` | `/special-medical-services/` | 301 |
| `/clinic-days.html` | `/clinic-days/` | 301 |
| `/ollmh-outlook.html` | `/ollmh-outlook/` | 301 |
| `/ollmh-departments.html` | `/ollmh-departments/` | 301 |
| `/smi-community.html` | `/smi-community/` | 301 |
| `/contacts.html` | `/contacts/` | 301 |
| `/news-events.html` | `/news-events/` | 301 |
| `/medical-school-application-form.html` | `/medical-school-application-form/` | 301 |
| `/about-nursing-school.html` | `/about-nursing-school/` | 301 |

### Joomla system URLs (return 404, no redirect)

| Old URL | Action |
|---|---|
| `/administrator/*` | Return 404 (Joomla admin, never public) |
| `/index.php/component/finder/search` | Return 404 (Joomla search, replaced by WordPress search) |
| `/index.php?format=feed&type=rss` | Redirect to `/feed/` (WordPress RSS) |
| `/index.php?format=feed&type=atom` | Redirect to `/feed/atom/` (WordPress Atom) |

### External links to remove

| Old URL | Action |
|---|---|
| `https://shared65.accountservergroup.com:2096/webmail/` | Remove link (replace with contact form or mailto:) |

### Image URLs (handled by asset migration)

Old image URLs (`/images/...`) are not redirected — they are replaced
in-content during content migration (see [`ASSET-MIGRATION.md`](./ASSET-MIGRATION.md)).
The old `/images/` directory does not exist on the new server.

---

## 3. Redirect implementation

### Method: Redirection plugin (recommended)

Install the [Redirection](https://wordpress.org/plugins/redirection/)
plugin and configure each redirect via the admin UI or import a CSV.

**Import file format** (`redirects.csv`):

```csv
source,target,regex,code,match
/index.html,/,0,301,url
/about-ollmh-location.html,/about-ollmh-location/,0,301,url
/administration.html,/administration/,0,301,url
/philosophy-of-care.html,/philosophy-of-care/,0,301,url
/hr-capacity-staff.html,/hr-capacity-staff/,0,301,url
/development-projects.html,/development-projects/,0,301,url
/self-sustainability-projects.html,/self-sustainability-projects/,0,301,url
/community-support.html,/community-support/,0,301,url
/upcoming-projects.html,/upcoming-projects/,0,301,url
/in-patient-dept.html,/in-patient-dept/,0,301,url
/out-patient-dept.html,/out-patient-dept/,0,301,url
/wards.html,/wards/,0,301,url
/special-medical-services.html,/special-medical-services/,0,301,url
/clinic-days.html,/clinic-days/,0,301,url
/ollmh-outlook.html,/ollmh-outlook/,0,301,url
/ollmh-departments.html,/ollmh-departments/,0,301,url
/smi-community.html,/smi-community/,0,301,url
/contacts.html,/contacts/,0,301,url
/news-events.html,/news-events/,0,301,url
/medical-school-application-form.html,/medical-school-application-form/,0,301,url
/about-nursing-school.html,/about-nursing-school/,0,301,url
```

### Alternative: `.htaccess` (Apache only)

If not using the Redirection plugin, add to `.htaccess`:

```apache
<IfModule mod_rewrite.c>
RewriteEngine On

# OLLMH Joomla → WordPress redirects
RewriteRule ^index\.html$ / [R=301,L]
RewriteRule ^about-ollmh-location\.html$ /about-ollmh-location/ [R=301,L]
RewriteRule ^administration\.html$ /administration/ [R=301,L]
RewriteRule ^philosophy-of-care\.html$ /philosophy-of-care/ [R=301,L]
RewriteRule ^hr-capacity-staff\.html$ /hr-capacity-staff/ [R=301,L]
RewriteRule ^development-projects\.html$ /development-projects/ [R=301,L]
RewriteRule ^self-sustainability-projects\.html$ /self-sustainability-projects/ [R=301,L]
RewriteRule ^community-support\.html$ /community-support/ [R=301,L]
RewriteRule ^upcoming-projects\.html$ /upcoming-projects/ [R=301,L]
RewriteRule ^in-patient-dept\.html$ /in-patient-dept/ [R=301,L]
RewriteRule ^out-patient-dept\.html$ /out-patient-dept/ [R=301,L]
RewriteRule ^wards\.html$ /wards/ [R=301,L]
RewriteRule ^special-medical-services\.html$ /special-medical-services/ [R=301,L]
RewriteRule ^clinic-days\.html$ /clinic-days/ [R=301,L]
RewriteRule ^ollmh-outlook\.html$ /ollmh-outlook/ [R=301,L]
RewriteRule ^ollmh-departments\.html$ /ollmh-departments/ [R=301,L]
RewriteRule ^smi-community\.html$ /smi-community/ [R=301,L]
RewriteRule ^contacts\.html$ /contacts/ [R=301,L]
RewriteRule ^news-events\.html$ /news-events/ [R=301,L]
RewriteRule ^medical-school-application-form\.html$ /medical-school-application-form/ [R=301,L]
RewriteRule ^about-nursing-school\.html$ /about-nursing-school/ [R=301,L]

# Joomla RSS → WordPress feed
RewriteRule ^index\.php\?format=feed&type=rss$ /feed/ [R=301,L]
RewriteRule ^index\.php\?format=feed&type=atom$ /feed/atom/ [R=301,L]
</IfModule>
```

---

## 4. Permalink structure

Set WordPress permalinks to `/%postname%/` (Post Name):

```
Settings → Permalinks → Custom Structure: /%postname%/
```

This produces clean URLs like:
- `/about-ollmh-location/` (page)
- `/news/nursing-school-promo/` (news_article CPT)
- `/events/annual-health-fair-2024/` (event CPT)
- `/departments/outpatient/` (department CPT)

---

## 5. CPT URL structure

| CPT | Archive URL | Single URL |
|---|---|---|
| `news_article` | `/news/` | `/news/{slug}/` |
| `event` | `/events/` | `/events/{slug}/` |
| `department` | `/departments/` | `/departments/{slug}/` |
| `staff_member` | `/staff/` | `/staff/{slug}/` |
| `job_vacancy` | `/careers/` | `/careers/{slug}/` |
| `development_project` | `/projects/development/` | `/projects/development/{slug}/` |
| `sustainability_project` | `/projects/sustainability/` | `/projects/sustainability/{slug}/` |
| `upcoming_project` | `/projects/upcoming/` | `/projects/upcoming/{slug}/` |
| `community_program` | `/community/programs/` | `/community/programs/{slug}/` |
| `smi_event` | `/community/smi-events/` | `/community/smi-events/{slug}/` |
| `outlook_album` | `/gallery/` | `/gallery/{slug}/` |

---

## 6. Post-launch redirect verification

After deploying redirects, verify each one:

1. Use the Redirection plugin's built-in checker (Tools → Redirection → Logs)
2. Run a bulk HTTP status check:
   ```bash
   for url in about-ollmh-location administration philosophy-of-care; do
     status=$(curl -s -o /dev/null -w "%{http_code}" "https://ourladyoflourdesmweahospital.org/${url}.html")
     echo "${url}.html → ${status}"
   done
   ```
3. All should return `301`
4. Check Google Search Console for crawl errors after 1–2 weeks
5. Monitor for any 404s from old URLs not in the redirect map
