# Cookie Consent & Data Protection

> This document defines the cookie consent strategy for the OLLMH
> WordPress site, ensuring compliance with Kenya's Data Protection Act
> 2019 and international best practice (GDPR-style consent).
>
> **Related:** [`SECURITY-HARDENING.md`](./SECURITY-HARDENING.md) for
> security, [`REST-API-SPEC.md`](./REST-API-SPEC.md) → 3.9 Cookie consent
> endpoint, [`SETTINGS.md`](./SETTINGS.md) → `security` group.

---

## 1. Legal context

### Kenya Data Protection Act 2019

The Kenya Data Protection Act 2019 (DPA) requires that websites:
1. Obtain **informed consent** before collecting personal data
2. Provide **clear information** about what data is collected and why
3. Allow users to **withdraw consent** at any time
4. Maintain a **record of consent** (audit trail)

The OLLMH website collects personal data via:
- Contact form (name, email, phone, message)
- Appointment booking (patient name, email, phone, medical reason)
- Nursing school application (full personal and academic data)
- Event registration (name, email, phone)
- Newsletter subscription (email)
- Analytics cookies (anonymous browsing data)
- Advertising cookies (if Google AdSense is used)

### International visitors

The site may receive visitors from the EU (subject to GDPR) and other
regions with cookie consent requirements. The cookie consent banner is
shown to **all visitors** regardless of location, for simplicity and
universal compliance.

---

## 2. Cookie categories

| Category | Purpose | Can be disabled? | Cookies |
|---|---|---|---|
| **Essential** | Site functionality, security, form submission | No | `ollmh_cookie_consent`, `wordpress_logged_in_*`, `wp-settings-*`, Cloudflare `__cfduid`, Turnstile `cf_clearance` |
| **Analytics** | Understanding how visitors use the site | Yes | Google Analytics `_ga`, `_gid`, `_gat`, Site Kit `__utmz` |
| **Advertising** | Serving relevant ads (if Google AdSense is enabled) | Yes | Google AdSense `IDE`, `NID`, `test_cookie` |

**Essential cookies are always set** — they are required for the site to
function (login, security, form CSRF tokens). The user cannot disable
these.

---

## 3. Cookie consent banner

### When it appears

The banner appears on **first visit** to any page. It is a fixed-position
bar at the bottom of the screen (below the footer on long pages, or
overlaying content on short pages).

### Banner layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  We use cookies to enhance your browsing experience, serve personalized ads, │
│  and analyze our traffic. By clicking "Accept All", you consent to our use   │
│  of cookies. You can customize your preferences or withdraw consent at any    │
│  time. Read our Privacy Policy.                                              │
│                                                                              │
│  [ Reject All ]  [ Cookie Settings ]  [ Accept All ]                         │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Banner behavior

| Action | Result |
|---|---|
| **Accept All** | All cookie categories enabled, banner dismissed, preference stored for 365 days |
| **Reject All** | Only essential cookies enabled, banner dismissed, preference stored for 365 days |
| **Cookie Settings** | Opens a modal with per-category toggles (see below) |
| **Click "Privacy Policy" link** | Navigates to `/privacy-policy/` |

The banner does **not** reappear for 365 days after the user makes a
choice (stored in `ollmh_cookie_consent` cookie).

---

## 4. Cookie settings modal

When the user clicks "Cookie Settings", a modal opens with per-category
toggles:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Cookie Preferences                                                    [×]  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  We use cookies to enhance your browsing experience, serve personalized     │
│  ads, and analyze our traffic. You can customize your preferences or         │
│  withdraw consent at any time. Read our Privacy Policy.                      │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Essential Cookies                                              [ON]     │ │
│  │ Required for the website to function correctly. These cannot be        │ │
│  │ disabled.                                                              │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Analytics Cookies                                            [ON/OFF]  │ │
│  │ Help us understand how visitors interact with our website by           │ │
│  │ collecting and reporting information anonymously.                      │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Advertising Cookies                                          [ON/OFF]  │ │
│  │ Used by Google AdSense and other third-party ad partners to serve      │ │
│  │ ads that are relevant to your interests. You may opt out of            │ │
│  │ personalized advertising by visiting Google Ads Settings or            │ │
│  │ aboutads.info/choices.                                                 │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  [ Save Preferences ]                                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Modal behavior

- **Essential cookies** toggle is disabled (always ON, greyed out)
- **Analytics** and **Advertising** toggles are interactive
- User toggles each category, then clicks "Save Preferences"
- Preference is stored via `POST /ollmh/v1/cookie-consent` (see
  [`REST-API-SPEC.md`](./REST-API-SPEC.md) → 3.9)
- Modal closes, banner dismisses, and scripts load/unload based on preference

---

## 5. JavaScript implementation

### Script loading strategy

All non-essential scripts (analytics, advertising) are **blocked by
default**. They are only loaded after the user grants consent.

```javascript
// assets/js/cookie-consent.js

(function() {
  const consentCookie = getCookie('ollmh_cookie_consent');
  let consent = consentCookie ? JSON.parse(consentCookie) : null;

  // If no consent record, show the banner
  if (!consent) {
    showBanner();
  } else {
    applyConsent(consent);
  }

  function showBanner() {
    document.getElementById('cookie-banner').style.display = 'block';
  }

  function hideBanner() {
    document.getElementById('cookie-banner').style.display = 'none';
  }

  function acceptAll() {
    const preference = {
      preference: 'all',
      categories: ['essential', 'analytics', 'advertising'],
      timestamp: Date.now(),
    };
    saveConsent(preference);
  }

  function rejectAll() {
    const preference = {
      preference: 'essential_only',
      categories: ['essential'],
      timestamp: Date.now(),
    };
    saveConsent(preference);
  }

  function saveConsent(preference) {
    // Store in cookie (365 days)
    setCookie('ollmh_cookie_consent', JSON.stringify(preference), 365);

    // Send to server for audit trail
    fetch(ollmhConfig.restUrl + '/cookie-consent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-WP-Nonce': ollmhConfig.nonce,
      },
      body: JSON.stringify(preference),
    });

    applyConsent(preference);
    hideBanner();
  }

  function applyConsent(preference) {
    const categories = preference.categories || ['essential'];

    // Analytics
    if (categories.includes('analytics')) {
      loadAnalytics();
    } else {
      unloadAnalytics();
    }

    // Advertising
    if (categories.includes('advertising')) {
      loadAdvertising();
    } else {
      unloadAdvertising();
    }
  }

  function loadAnalytics() {
    // Load Google Analytics / Site Kit
    if (!window.gaLoaded) {
      const script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + ollmhConfig.gaId;
      document.head.appendChild(script);

      window.dataLayer = window.dataLayer || [];
      function gtag() { dataLayer.push(arguments); }
      gtag('js', new Date());
      gtag('config', ollmhConfig.gaId, { anonymize_ip: true });
      window.gaLoaded = true;
    }
  }

  function unloadAnalytics() {
    // Delete GA cookies
    document.cookie = '_ga=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = '_gid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = '_gat=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.gaLoaded = false;
  }

  function loadAdvertising() {
    // Load Google AdSense if enabled
    if (ollmhConfig.adsenseId && !window.adsLoaded) {
      const script = document.createElement('script');
      script.async = true;
      script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ollmhConfig.adsenseId;
      document.head.appendChild(script);
      window.adsLoaded = true;
    }
  }

  function unloadAdvertising() {
    // AdSense cookies removal
    document.cookie = 'IDE=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = 'NID=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.adsLoaded = false;
  }

  // Expose for banner buttons
  window.ollmhCookieConsent = {
    acceptAll,
    rejectAll,
    saveCustom: saveConsent,
  };
})();
```

### WordPress integration

The cookie consent script is loaded in the footer on **all pages**:

```php
wp_enqueue_script(
  'ollmh-cookie-consent',
  OLLMH_THEME_URI . '/assets/js/cookie-consent.js',
  [],
  OLLMH_THEME_VERSION,
  true
);
wp_localize_script('ollmh-cookie-consent', 'ollmhConfig', [
  'restUrl'    => esc_url_raw(rest_url('ollmh/v1')),
  'nonce'      => wp_create_nonce('wp_rest'),
  'gaId'       => OLLMH_Helpers::get_setting('google_analytics_id'),
  'adsenseId'  => OLLMH_Helpers::get_setting('google_adsense_id'),
]);
```

The banner HTML is rendered in `footer.php` before the closing `</body>`:

```php
<div id="cookie-banner" style="display:none;">
  <!-- Banner content with Reject All / Cookie Settings / Accept All buttons -->
</div>

<div id="cookie-modal" style="display:none;">
  <!-- Modal content with per-category toggles -->
</div>
```

---

## 6. Database table: `wp_cookie_consents`

Stores a record of each user's consent preference for audit trail (required
by Kenya DPA 2019).

| Column | Type | Description |
|---|---|---|
| `id` | BIGINT UNSIGNED AUTO_INCREMENT | Primary key |
| `ip_address` | VARCHAR(45) | Visitor IP address (IPv4 or IPv6) |
| `user_agent` | VARCHAR(255) | Browser user agent |
| `preference` | VARCHAR(20) | `all`, `essential_only`, or `custom` |
| `categories` | JSON | Array of enabled categories |
| `created_at` | DATETIME | When consent was given |
| `expires_at` | DATETIME | When the consent cookie expires (365 days) |

**Retention:** Consent records are retained for **2 years** (per Kenya DPA
guidance), then automatically deleted by the `ollmh_prune_logs` cron job
(see [`CRON-JOBS.md`](./CRON-JOBS.md)).

---

## 7. Settings

The following settings in `wp_settings` → `security` group control cookie
consent behavior (see [`SETTINGS.md`](./SETTINGS.md)):

| Setting key | Type | Default | Description |
|---|---|---|---|
| `cookie_consent_enabled` | boolean | `1` | Master toggle for cookie consent banner |
| `cookie_consent_retention_days` | integer | `365` | Days before consent cookie expires |
| `google_analytics_id` | string | `''` | Google Analytics 4 measurement ID (e.g. `G-XXXXXXXXXX`) |
| `google_adsense_id` | string | `''` | Google AdSense publisher ID (e.g. `ca-pub-XXXXXXXXXXXXXXXX`) |

If `cookie_consent_enabled` is `0`, the banner is not shown and all cookies
are set without consent (not recommended for production).

---

## 8. Cookie policy page

A dedicated Cookie Policy page (`/cookie-policy/`) should be created with
the following content sections:

1. **What are cookies** — brief explanation
2. **Types of cookies we use** — table of all cookies with name, purpose,
   duration, and category
3. **Essential cookies** — list with descriptions
4. **Analytics cookies** — list with descriptions, link to Google Analytics
   privacy policy
5. **Advertising cookies** — list with descriptions, links to Google Ads
   Settings and aboutads.info/choices
6. **How to manage cookies** — instructions for browser-level cookie
   controls (Chrome, Firefox, Safari, Edge)
7. **Changes to this policy** — when the policy was last updated

This page is linked from the cookie consent banner ("Read our Privacy
Policy") and should also be accessible from the footer Legal column (see
[`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md) → Column 4:
Legal).

**Add to footer Legal column:**
- Privacy Policy
- Terms of Service
- Data Protection
- Cookie Policy ← new

---

## 9. Compliance checklist

- [ ] Cookie consent banner appears on first visit
- [ ] Banner has "Accept All", "Reject All", and "Cookie Settings" buttons
- [ ] Essential cookies cannot be disabled
- [ ] Analytics and advertising cookies are blocked until consent is given
- [ ] Consent is stored for 365 days
- [ ] Consent record is stored in `wp_cookie_consents` for audit trail
- [ ] User can change preferences at any time (via Cookie Settings button
      in footer or by clearing cookies)
- [ ] Cookie Policy page exists at `/cookie-policy/`
- [ ] Privacy Policy page mentions cookies and links to Cookie Policy
- [ ] Google Analytics uses `anonymize_ip: true` (IP anonymization)
- [ ] Newsletter signup uses double opt-in (see [`REST-API-SPEC.md`](./REST-API-SPEC.md) → 3.8)
- [ ] All forms include a consent checkbox linking to Privacy Policy
