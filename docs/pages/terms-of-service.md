# Terms of Service (`/terms-of-service/`)

> Terms governing use of the OLLMH website and online services
> (appointments, applications, newsletter).
>
> **New page** — does not exist in the archived site. Referenced in the
> footer Legal column and the newsletter consent line (see
> [`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md) → Column 4:
> Legal, Band 2: Newsletter consent).

---

## 1. Page metadata

| Field | Value |
|---|---|
| Slug | `terms-of-service` |
| `page_type` | `generic` |
| Template | `page-generic.php` |
| Menu location | Footer → Legal column, Newsletter consent line |
| SEO title | "Terms of Service — OLLMH" |
| Meta description | "Terms governing the use of the OLLMH website and online services." |

---

## 2. Page sections

### 2.1 Acceptance of terms

By accessing and using this website, you agree to be bound by these
Terms of Service. If you do not agree, please do not use the website.

### 2.2 Use of the website

- The website is provided for informational purposes and to facilitate
  communication with the hospital (appointments, applications, enquiries)
- You must provide accurate and truthful information in all forms
- You must not use the website for any unlawful purpose
- You must not attempt to disrupt or compromise the website's security
- Automated access (scraping, bots) is prohibited except for search
  engine indexing

### 2.3 Appointments

- Appointment requests submitted via the website are **requests**, not
  confirmed bookings
- Confirmation is sent via email and SMS after the hospital reviews
  availability
- Appointments are subject to the hospital's scheduling policies
- Cancellations should be made at least
  `appointment_cancellation_hours` hours in advance

### 2.4 Nursing school applications

- The application form must be completed truthfully and accurately
- Providing false information may result in disqualification
- The application fee (`nursing_application_fee_kes`) is non-refundable
- Submission of an application does not guarantee admission
- The hospital reserves the right to reject any application without
  providing a reason

### 2.5 Payments

- Application fees are processed via M-Pesa (Safaricom Daraja API)
- Payments are confirmed via callback from Safaricom
- The hospital is not responsible for M-Pesa transaction failures caused
  by Safaricom network issues
- Refunds (if applicable) are processed within 14 working days

### 2.6 Newsletter

- By subscribing to the newsletter, you consent to receiving periodic
  emails from OLLMH
- You can unsubscribe at any time via the link in any newsletter email
- See our [Privacy Policy](/privacy-policy/) for how we handle your email
  address

### 2.7 Intellectual property

- All website content (text, images, logos) is the property of OLLMH
  unless otherwise stated
- You may not reproduce, distribute, or modify content without prior
  written permission
- Hospital name, logo, and crest are trademarks of OLLMH

### 2.8 Medical disclaimer

- Information on this website is for general informational purposes only
  and is **not** a substitute for professional medical advice
- Always seek the advice of a qualified healthcare provider with any
  health questions
- Do not disregard professional medical advice because of something you
  read on this website
- In a medical emergency, call `hospital_emergency_phone` or visit the
  emergency department immediately

### 2.9 Limitation of liability

- The hospital is not liable for any damages arising from the use of
  this website
- The hospital is not liable for the accuracy of information submitted by
  third parties
- The hospital is not liable for temporary unavailability of the website
  due to maintenance or technical issues

### 2.10 Third-party links

- The website may contain links to third-party websites (Google Maps,
  social media, M-Pesa)
- The hospital is not responsible for the content or privacy practices of
  third-party websites

### 2.11 Changes to terms

- The hospital may update these terms at any time
- The "Last updated" date reflects the most recent change
- Continued use of the website after changes constitutes acceptance of
  the new terms

### 2.12 Governing law

- These terms are governed by the laws of the Republic of Kenya
- Disputes are subject to the jurisdiction of Kenyan courts

### 2.13 Contact

For questions about these terms:
- Email: `hospital_email`
- Phone: `hospital_phone`

---

## 3. Database

This page uses the `wp_pages` table with `page_type = 'generic'`. No
custom tables needed.

Settings referenced (from `wp_settings`):
- `hospital_email`, `hospital_phone`, `hospital_emergency_phone`
- `nursing_application_fee_kes`
- `appointment_cancellation_hours`

---

## 4. SEO

- JSON-LD schema: `WebPage`
- Internal links to: `/privacy-policy/`, `/data-protection/`, `/contacts/`,
  `/medical-school-application-form/`
- Breadcrumb: Home → Terms of Service
