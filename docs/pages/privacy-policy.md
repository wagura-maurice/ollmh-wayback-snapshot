# Privacy Policy (`/privacy-policy/`)

> How OLLMH collects, uses, and protects personal data of website
> visitors, patients, and newsletter subscribers.
>
> **New page** — does not exist in the archived site. Referenced in the
> footer Legal column and the newsletter consent line (see
> [`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md) → Column 4:
> Legal, Band 2: Newsletter consent).

---

## 1. Page metadata

| Field | Value |
|---|---|
| Slug | `privacy-policy` |
| `page_type` | `generic` |
| Template | `page-generic.php` |
| Menu location | Footer → Legal column, Newsletter consent line, Cookie consent banner |
| SEO title | "Privacy Policy — OLLMH" |
| Meta description | "How Our Lady of Lourdes Mwea Hospital collects, uses, and protects your personal data." |

---

## 2. Page sections

### 2.1 Introduction

- Effective date (auto-updated to the last modified date of the page)
- Who we are (hospital name, address, contact)
- Scope of this policy (website, online forms, newsletter)

### 2.2 Data we collect

| Data type | What | How | Why |
|---|---|---|---|
| Contact form data | Name, email, phone, message | Contact form submission | To respond to enquiries |
| Appointment data | Patient name, email, phone, preferred date/time, reason | Appointment booking form | To schedule and confirm appointments |
| Application data | Full personal info, academic records, documents, payment info | Nursing school application form | To process admissions applications |
| Event registration data | Name, email, phone, number of attendees | Event registration form | To manage event attendance |
| Newsletter data | Email address | Newsletter signup form | To send news and updates |
| Cookie data | Browsing behavior, IP address | Analytics and advertising cookies | To understand site usage (see [`COOKIE-CONSENT.md`](../COOKIE-CONSENT.md)) |
| Server logs | IP address, browser type, pages visited, timestamps | Automatic server logging | Security and troubleshooting |

### 2.3 How we use your data

- To respond to your enquiries and appointment requests
- To process nursing school applications
- To send newsletter emails (only after double opt-in confirmation)
- To improve our website and services
- To comply with legal obligations
- **We do not sell your data to third parties**

### 2.4 Legal basis for processing

Under Kenya's Data Protection Act 2019:
- **Consent:** Newsletter subscription, cookie tracking
- **Contract:** Appointment booking, application processing
- **Legal obligation:** Medical records retention
- **Legitimate interest:** Server logs, security monitoring

### 2.5 Data sharing

We share data only with:
- **Safaricom (M-Pesa):** Payment processing for application fees
- **Cloudflare:** Bot protection (Turnstile) and security
- **Google (Analytics):** Anonymous browsing statistics (if consented)
- **Email/SMS providers:** To send notifications and reminders
- **Regulatory bodies:** When required by law (e.g. nursing council
  accreditation audits)

We **never** sell personal data to any third party.

### 2.6 Data retention

| Data type | Retention period |
|---|---|
| Contact form submissions | 2 years |
| Appointment records | 7 years (medical records law) |
| Application records | 5 years (or as required by nursing council) |
| Event registrations | 1 year after the event |
| Newsletter subscribers | Until unsubscribe + 30 days |
| Cookie consent records | 2 years |
| Server logs | 90 days |

### 2.7 Your rights

Under Kenya's Data Protection Act 2019, you have the right to:
- **Access** your personal data
- **Correct** inaccurate data
- **Delete** your data (right to be forgotten)
- **Object** to processing
- **Withdraw consent** at any time
- **Data portability** (receive your data in a structured format)

To exercise these rights, contact us at `hospital_email` or submit a
data subject request via the contact form.

### 2.8 Security

- All data is transmitted over HTTPS (SSL/TLS encryption)
- Passwords are hashed using bcrypt
- Database access is restricted to authorized personnel
- See [`SECURITY-HARDENING.md`](../SECURITY-HARDENING.md) for full
  security measures

### 2.9 Cookies

This website uses cookies. See our
[Cookie Policy](/cookie-policy/) and [`COOKIE-CONSENT.md`](../COOKIE-CONSENT.md)
for details on what cookies we use and how to manage them.

### 2.10 Changes to this policy

We may update this policy from time to time. The "Last updated" date at
the top of the page reflects the most recent change. Significant changes
will be announced via the website.

### 2.11 Contact

For privacy questions or data subject requests:
- Email: `hospital_email`
- Phone: `hospital_phone`
- Address: `hospital_address`

---

## 3. Database

This page uses the `wp_pages` table with `page_type = 'generic'`. No
custom tables needed.

Settings referenced (from `wp_settings`):
- `hospital_name`, `hospital_email`, `hospital_phone`, `hospital_address`

---

## 4. SEO

- JSON-LD schema: `WebPage` with `about` property referencing privacy
- Internal links to: `/cookie-policy/`, `/data-protection/`, `/contacts/`
- Breadcrumb: Home → Privacy Policy
- `noindex` on this page is **not** set (legal pages should be indexed
  for transparency)
