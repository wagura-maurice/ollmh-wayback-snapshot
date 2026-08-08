# Patient Information (`/patient-information/`)

> Practical guidance for patients and visitors — admission guidelines,
> what to bring, visiting hours, patient rights, and billing information.
>
> **New page** — does not exist in the archived site. Referenced in the
> footer Support column (see
> [`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md) → Column 3:
> Support).

---

## 1. Page metadata

| Field | Value |
|---|---|
| Slug | `patient-information` |
| `page_type` | `generic` |
| Template | `page-generic.php` |
| Menu location | Footer → Support column |
| SEO title | "Patient Information — OLLMH" |
| Meta description | "Everything you need to know before visiting OLLMH: admission guidelines, what to bring, visiting hours, patient rights, and billing." |

---

## 2. Page sections

### 2.1 Admission guidelines

Information for patients being admitted to the hospital:

- **Pre-admission:** What documents to bring (national ID, NHIF card,
  referral letter if applicable, previous medical records)
- **Registration process:** Where to go (OPD reception), what to expect,
  estimated time
- **Registration fee:** Current fee amount (sourced from
  `registration_fee_kes` setting)
- **Insurance:** Accepted insurance providers (sourced from
  `accepted_insurance_providers` setting) — NHIF, UAP, Jubilee, etc.
- **Emergency admission:** What to do in an emergency (call
  `hospital_emergency_phone`, come directly to emergency department)

### 2.2 What to bring

Checklist for inpatients:

- National ID or birth certificate (for children)
- NHIF card or insurance card
- Referral letter (if referred from another facility)
- Previous medical records and test results
- List of current medications
- Personal items (toiletries, comfortable clothes, phone charger)
- Cash or M-Pesa for any co-payments

### 2.3 Visiting hours

| Ward | Visiting hours | Max visitors per bed |
|---|---|---|
| General wards | 10:00 AM – 12:00 PM, 4:00 PM – 6:00 PM | 2 |
| Maternity ward | 11:00 AM – 1:00 PM, 4:00 PM – 7:00 PM | 2 (spouse + 1) |
| Pediatric ward | 10:00 AM – 8:00 PM (parents only) | 2 |
| ICU / High Dependency | 11:00 AM – 12:00 PM, 4:00 PM – 5:00 PM | 1 |
| Emergency | 24 hours (family only) | 1 |

> Visiting hours are sourced from `visiting_hours_general_wards`,
> `visiting_hours_maternity`, etc. settings so they can be updated without
> editing the page.

### 2.4 Patient rights and responsibilities

**Patient rights:**
- Right to respectful and dignified care
- Right to privacy and confidentiality
- Right to information about diagnosis and treatment
- Right to informed consent before any procedure
- Right to refuse treatment (except in emergencies)
- Right to a second opinion
- Right to access medical records
- Right to complain without fear of retaliation

**Patient responsibilities:**
- Provide accurate and complete information
- Follow the prescribed treatment plan
- Respect hospital staff, other patients, and hospital property
- Keep appointments or notify the hospital in advance of cancellations
- Pay bills promptly or arrange payment plans

### 2.5 Billing and payment

- Accepted payment methods: Cash, M-Pesa, NHIF, private insurance
- Billing office location and hours
- How to request a bill estimate
- How to dispute a bill
- Financial assistance / charity care policy (if available)

### 2.6 Visitor information

- Parking availability
- Cafeteria / canteen hours
- ATM location
- Wi-Fi availability (if any)
- Accommodation for families of critically ill patients

---

## 3. Database

This page uses the `wp_pages` table with `page_type = 'generic'`. No
custom tables are needed — all content is stored as page content in the
WordPress editor.

Settings referenced (from `wp_settings`):
- `registration_fee_kes`
- `accepted_insurance_providers`
- `hospital_emergency_phone`
- `visiting_hours_general_wards`
- `visiting_hours_maternity`
- `visiting_hours_pediatric`
- `visiting_hours_icu`
- `visiting_hours_emergency`

---

## 4. Shortcodes used

| Shortcode | Purpose |
|---|---|
| `[ollmh_hospital_hours]` | Display operating hours in the billing section |

---

## 5. SEO

- JSON-LD schema: `MedicalWebPage` with `about` property set to
  `PatientInformation`
- Internal links to: `/contacts/`, `/out-patient-dept/`, `/wards/`,
  `/clinic-days/`
- Breadcrumb: Home → Patient Information
