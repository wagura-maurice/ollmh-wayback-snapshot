# FAQ (`/faq/`)

> Frequently asked questions about OLLMH services, billing, appointments,
> and the nursing school — to reduce repetitive phone enquiries.
>
> **New page** — does not exist in the archived site. Referenced in the
> footer Support column (see
> [`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md) → Column 3:
> Support).

---

## 1. Page metadata

| Field | Value |
|---|---|
| Slug | `faq` |
| `page_type` | `generic` |
| Template | `page-faq.php` (accordion layout) |
| Menu location | Footer → Support column |
| SEO title | "Frequently Asked Questions — OLLMH" |
| Meta description | "Answers to common questions about OLLMH services, appointments, billing, insurance, and the nursing school." |

---

## 2. Page layout

The FAQ page uses an **accordion layout** — questions are collapsed by
default, clicking a question expands the answer. This keeps the page
compact and scannable.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Frequently Asked Questions                                                  │
│                                                                              │
│  Can't find what you're looking for? [Contact Us →]                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ▸ Appointments & OPD                                                        │
│    ▸ How do I book an appointment?                                           │
│    ▸ Do I need to register before seeing a doctor?                           │
│    ▸ What are the OPD operating hours?                                       │
│    ▸ Can I walk in without an appointment?                                   │
│                                                                              │
│  ▸ Billing & Insurance                                                       │
│    ▸ What insurance providers do you accept?                                 │
│    ▸ How much is the registration fee?                                       │
│    ▸ Can I pay via M-Pesa?                                                   │
│    ▸ How do I get a bill estimate?                                           │
│                                                                              │
│  ▸ Inpatient & Wards                                                         │
│    ▸ What are the visiting hours?                                            │
│    ▸ What should I bring for admission?                                      │
│    ▸ Can family members stay overnight?                                      │
│                                                                              │
│  ▸ Nursing School                                                            │
│    ▸ What programmes are offered?                                            │
│    ▸ How do I apply?                                                         │
│    ▸ What is the application fee?                                            │
│    ▸ When are the intake periods?                                            │
│    ▸ What are the minimum KCSE requirements?                                 │
│                                                                              │
│  ▸ General                                                                   │
│    ▸ Where is the hospital located?                                          │
│    ▸ Is there an emergency line?                                             │
│    ▸ Do you offer ambulance services?                                        │
│    ▸ Can I access my medical records?                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. FAQ categories and questions

### 3.1 Appointments & OPD

| Question | Answer summary |
|---|---|
| How do I book an appointment? | Use the online appointment form on the Outpatient Department page, or call `hospital_phone`. You'll receive a confirmation email and SMS with your reference number. |
| Do I need to register before seeing a doctor? | Yes. First-time patients register at OPD reception. The registration fee is KES `registration_fee_kes`. Bring your national ID and NHIF card (if applicable). |
| What are the OPD operating hours? | `opd_operating_hours` setting (typically Mon–Sat, 7am–8pm). Emergency services are available 24 hours. |
| Can I walk in without an appointment? | Yes, walk-ins are accepted, but patients with appointments are seen first. Expect longer wait times for walk-ins. |

### 3.2 Billing & Insurance

| Question | Answer summary |
|---|---|
| What insurance providers do you accept? | We accept: `accepted_insurance_providers` (NHIF, UAP, Jubilee, AAR, etc.). Bring your insurance card at registration. |
| How much is the registration fee? | KES `registration_fee_kes` for new patients. Returning patients within the same year pay a reduced fee. |
| Can I pay via M-Pesa? | Yes. Our M-Pesa Paybill is `mpesa_paybill`. Use your patient number as the account number. |
| How do I get a bill estimate? | Visit the billing office during operating hours, or call `hospital_phone` and ask for the billing department. |

### 3.3 Inpatient & Wards

| Question | Answer summary |
|---|---|
| What are the visiting hours? | See our [Patient Information](/patient-information/) page for detailed visiting hours by ward. |
| What should I bring for admission? | National ID, NHIF/insurance card, referral letter, previous records, medications list, personal toiletries. See [Patient Information](/patient-information/). |
| Can family members stay overnight? | Only in critical cases (ICU, pediatric). Accommodation is not provided for general ward visitors. |

### 3.4 Nursing School

| Question | Answer summary |
|---|---|
| What programmes are offered? | `nursing_programmes_offered` (e.g. KRCHN, Enrolled Nurse). See [About the Nursing School](/about-nursing-school/). |
| How do I apply? | Complete the online application form at [/medical-school-application-form/](/medical-school-application-form/). The form has 4 steps: personal info, academic info, document upload, and payment. |
| What is the application fee? | KES `nursing_application_fee_kes`, payable via M-Pesa during the application process. |
| When are the intake periods? | `nursing_intake_months` (typically January and September). Check the nursing school page for exact dates. |
| What are the minimum KCSE requirements? | Mean grade C (plain), with C in English, Biology, Chemistry, and Mathematics. See [About the Nursing School](/about-nursing-school/) for full requirements. |

### 3.5 General

| Question | Answer summary |
|---|---|
| Where is the hospital located? | `hospital_address`. See [About OLLMH & Location](/about-ollmh-location/) for directions and a map. |
| Is there an emergency line? | Yes, call `hospital_emergency_phone`. Emergency services are available 24 hours, 7 days a week. |
| Do you offer ambulance services? | `ambulance_service_available` setting. If yes, call `hospital_emergency_phone` to request an ambulance. |
| Can I access my medical records? | Yes. Submit a records request at the medical records department. Bring your national ID. Processing takes 2–3 working days. |

> Answers that reference settings (e.g. `registration_fee_kes`) are
> dynamically populated from `wp_settings` so they stay current without
> editing the page.

---

## 4. Database

This page uses the `wp_pages` table with `page_type = 'generic'`. No
custom tables needed.

Settings referenced (from `wp_settings`):
- `hospital_phone`, `hospital_emergency_phone`, `hospital_address`
- `registration_fee_kes`, `accepted_insurance_providers`, `mpesa_paybill`
- `opd_operating_hours`, `ambulance_service_available`
- `nursing_programmes_offered`, `nursing_application_fee_kes`,
  `nursing_intake_months`

---

## 5. Implementation notes

- The accordion is implemented with vanilla JS (no jQuery UI needed) —
  see [`JAVASCRIPT-INTERACTIVITY.md`](./JAVASCRIPT-INTERACTIVITY.md)
- Each FAQ item uses `<details>` / `<summary>` HTML elements for
  accessibility (works without JS, keyboard-navigable, screen-reader
  friendly):
  ```html
  <details class="faq-item">
    <summary class="faq-question">How do I book an appointment?</summary>
    <div class="faq-answer">
      <p>Use the online appointment form...</p>
    </div>
  </details>
  ```
- CSS enhances the native `<details>` styling with the OLLMH color palette
- The "Contact Us →" link at the top directs users to `/contacts/` if
  their question isn't answered

---

## 6. SEO

- JSON-LD schema: `FAQPage` with `mainEntity` array of `Question` /
  `Answer` pairs — this enables rich snippets in Google search results
- Internal links to: `/out-patient-dept/`, `/patient-information/`,
  `/about-nursing-school/`, `/medical-school-application-form/`,
  `/about-ollmh-location/`, `/contacts/`
- Breadcrumb: Home → FAQ
