# Data Protection (`/data-protection/`)

> Data protection statement compliant with Kenya's Data Protection Act
> 2019 — how OLLMH processes, stores, and safeguards personal data.
>
> **New page** — does not exist in the archived site. Referenced in the
> footer Legal column (see
> [`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md) → Column 4:
> Legal).

---

## 1. Page metadata

| Field | Value |
|---|---|
| Slug | `data-protection` |
| `page_type` | `generic` |
| Template | `page-generic.php` |
| Menu location | Footer → Legal column |
| SEO title | "Data Protection — OLLMH" |
| Meta description | "How OLLMH complies with Kenya's Data Protection Act 2019 for the collection, processing, and storage of personal data." |

---

## 2. Page sections

### 2.1 Data controller

- **Data controller:** Our Lady of Lourdes Mwea Hospital
- **Address:** `hospital_address`
- **Contact:** `hospital_email`, `hospital_phone`
- **Data Protection Officer:** To be designated (contact via
  `hospital_email`)

### 2.2 Compliance statement

OLLMH is committed to complying with the Kenya Data Protection Act 2019
(DPA) and the Data Protection (General) Regulations 2021. This statement
explains how we collect, process, store, and protect personal data.

### 2.3 Categories of personal data

| Category | Data elements | Source |
|---|---|---|
| Identification data | Name, national ID number, date of birth, gender, nationality | Contact form, appointment form, application form |
| Contact data | Email, phone number, postal address | Contact form, appointment form, application form |
| Medical data | Reason for appointment, medical history | Appointment form, inpatient records |
| Academic data | KCSE results, school name, qualifications | Application form |
| Financial data | M-Pesa transaction ID, payment amount | Application payment |
| Technical data | IP address, browser type, cookies | Server logs, analytics |
| Special category data | Health information (reason for visit) | Appointment and medical records |

### 2.4 Purposes of processing

| Purpose | Legal basis | Data categories |
|---|---|---|
| Responding to enquiries | Consent | Contact data |
| Scheduling appointments | Contract | Identification, contact, medical |
| Processing applications | Contract | Identification, contact, academic, financial |
| Sending newsletters | Consent (double opt-in) | Contact data |
| Website analytics | Consent | Technical data |
| Security monitoring | Legitimate interest | Technical data |
| Regulatory compliance | Legal obligation | All categories as required |

### 2.5 Data subject rights

Under the DPA, data subjects have the right to:

1. **Right to be informed** — this statement and our
   [Privacy Policy](/privacy-policy/) fulfill this right
2. **Right of access** — request a copy of your personal data
3. **Right to rectification** — correct inaccurate data
4. **Right to erasure** — request deletion of your data (subject to
   legal retention requirements)
5. **Right to object** — object to processing based on legitimate
   interest
6. **Right to restrict processing** — request that we limit how we use
   your data
7. **Right to data portability** — receive your data in a structured,
   machine-readable format
8. **Right to withdraw consent** — withdraw consent for processing
   based on consent (newsletter, cookies)

**How to exercise your rights:**
- Submit a request via email to `hospital_email`
- Include "Data Subject Request" in the subject line
- Provide identification (national ID number) to verify your identity
- We will respond within 7 working days

### 2.6 Data security measures

| Measure | Implementation |
|---|---|
| Encryption in transit | HTTPS (TLS 1.2+) for all traffic |
| Encryption at rest | Database secrets encrypted with AES-256 |
| Access control | Role-based access, strong passwords, 2FA for admins |
| Firewall | Cloudflare WAF |
| Bot protection | Cloudflare Turnstile on all forms |
| SQL injection prevention | Parameterized queries (`$wpdb->prepare()`) |
| XSS prevention | Output escaping (`esc_html`, `esc_attr`, `esc_url`) |
| CSRF prevention | WordPress nonces on all forms |
| Audit logging | `wp_audit_logs` table tracks all admin actions |
| Regular security scans | Wordfence daily malware scan |

See [`SECURITY-HARDENING.md`](../SECURITY-HARDENING.md) for full details.

### 2.7 Data retention

| Data type | Retention period | Justification |
|---|---|---|
| Contact form submissions | 2 years | Customer service |
| Appointment records | 7 years | Medical records law |
| Application records | 5 years | Nursing council requirement |
| Payment records | 7 years | Tax and audit requirements |
| Newsletter subscribers | Until unsubscribe + 30 days | Consent withdrawal |
| Cookie consent records | 2 years | DPA audit requirement |
| Server logs | 90 days | Security monitoring |
| Audit logs | 1 year | Security and compliance |

After the retention period, data is automatically deleted by scheduled
cron jobs (see [`CRON-JOBS.md`](../CRON-JOBS.md) → `ollmh_prune_logs`).

### 2.8 Data sharing with third parties

| Recipient | Purpose | Data shared |
|---|---|---|
| Safaricom (M-Pesa) | Payment processing | Phone number, amount |
| Cloudflare | Security, bot protection | IP address, Turnstile token |
| Google Analytics | Website analytics (if consented) | Anonymous browsing data |
| SMS gateway provider | Appointment reminders, status updates | Phone number, message content |
| Email service (SMTP) | Sending notifications and newsletters | Email address, message content |
| Nursing Council of Kenya | Accreditation audits | Aggregate application data |

We **do not** sell, rent, or trade personal data with any third party.

### 2.9 International transfers

Personal data is stored on servers located in Kenya (or the EU if using
Cloudflare's EU data centers). If data is transferred outside Kenya, we
ensure adequate protection measures are in place as required by the DPA.

### 2.10 Data breach procedure

In the event of a personal data breach:
1. The hospital will contain the breach immediately
2. The Data Protection Officer will assess the severity and scope
3. The Office of the Data Protection Commissioner (ODPC) will be notified
   within 72 hours (as required by the DPA)
4. Affected data subjects will be notified if there is a high risk to
   their rights and freedoms
5. A breach report will be documented and retained

### 2.11 Complaints

If you believe we have not handled your personal data in accordance with
the DPA, you have the right to complain to:

**Office of the Data Protection Commissioner (ODPC)**
- Website: https://www.odpc.go.ke
- Email: complaints@odpc.go.ke
- Phone: +254 703 642 000

You also have the right to complain directly to OLLMH first — we will
investigate and respond within 14 working days.

---

## 3. Database

This page uses the `wp_pages` table with `page_type = 'generic'`. No
custom tables needed.

Settings referenced (from `wp_settings`):
- `hospital_name`, `hospital_email`, `hospital_phone`, `hospital_address`

Related tables:
- `wp_cookie_consents` — stores cookie consent audit trail
- `wp_audit_logs` — tracks admin actions for compliance
- `wp_notification_logs` — tracks all emails/SMS sent

---

## 4. SEO

- JSON-LD schema: `WebPage`
- Internal links to: `/privacy-policy/`, `/cookie-policy/`, `/contacts/`
- Breadcrumb: Home → Data Protection
