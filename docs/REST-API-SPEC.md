# REST API Specification

> This document defines all custom REST API endpoints for the OLLMH
> WordPress site — front-end form submissions, settings retrieval, and
> payment callbacks.
>
> **Related:** [`FRONT-END-FORMS.md`](./FRONT-END-FORMS.md) for form field
> specs, [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md) for plugin
> structure.

---

## 1. API base URL

```
Production:  https://ourladyoflourdesmweahospital.org/wp-json/ollmh/v1
Local dev:   http://localhost:8080/wp-json/ollmh/v1
```

All endpoints are registered under the `ollmh/v1` namespace.

---

## 2. Authentication

| Endpoint type | Auth method |
|---|---|
| Public form submissions (contact, appointment, application, event) | None (Turnstile token required) |
| Settings retrieval (public) | None (returns only `is_public=1` settings) |
| Settings update (admin) | WordPress nonce + `manage_options` capability |
| Payment callback (M-Pesa) | IP whitelist + shared secret |
| Admin data endpoints | WordPress nonce + capability check |

**Turnstile verification:** All public form submissions must include a
`turnstile_token` field. The server verifies this token via Cloudflare's
`siteverify` endpoint before processing the form data.

---

## 3. Endpoints

### 3.1 Contact form

```
POST /ollmh/v1/contact
```

**Request body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+254712345678",
  "subject": "General enquiry",
  "department": "opd",
  "message": "I would like to know the visiting hours for the maternity ward.",
  "turnstile_token": "0.xxxxx"
}
```

**Validation:**
- `name`: required, string, max 100
- `email`: required, valid email, max 191
- `phone`: optional, string, max 20
- `subject`: required, string, max 200
- `department`: optional, must be a valid department slug
- `message`: required, string, max 5000
- `turnstile_token`: required if `captcha_on_contact_form` setting is `1`

**Response (200):**
```json
{
  "success": true,
  "message": "Your message has been sent. We will respond within 48 hours.",
  "submission_id": 123
}
```

**Response (400):**
```json
{
  "success": false,
  "errors": {
    "email": "Please enter a valid email address.",
    "turnstile_token": "Bot verification failed. Please try again."
  }
}
```

**Side effects:**
- Insert into `wp_contact_submissions`
- Send email notification to `admin_email` setting
- Send auto-reply email to the submitter
- Log to notification queue

---

### 3.2 Appointment booking

```
POST /ollmh/v1/appointments
```

**Request body:**
```json
{
  "patient_name": "Jane Doe",
  "patient_email": "jane@example.com",
  "patient_phone": "+254712345678",
  "appointment_type": "opd",
  "department_id": 5,
  "clinic_id": null,
  "preferred_date": "2024-03-15",
  "preferred_time": "10:00",
  "reason": "General consultation",
  "is_new_patient": true,
  "turnstile_token": "0.xxxxx"
}
```

**Validation:**
- `patient_name`: required, string, max 100
- `patient_email`: required, valid email
- `patient_phone`: required, string, max 20
- `appointment_type`: required, enum: `opd`, `clinic`
- `department_id`: required if `appointment_type` is `opd`, must be a valid department
- `clinic_id`: required if `appointment_type` is `clinic`, must be a valid clinic
- `preferred_date`: required, valid date (YYYY-MM-DD), must be within `appointment_advance_days` setting
- `preferred_time`: required, valid time (HH:MM)
- `reason`: optional, string, max 1000
- `is_new_patient`: required, boolean
- `turnstile_token`: required if `captcha_on_appointment_booking` setting is `1`

**Response (200):**
```json
{
  "success": true,
  "message": "Your appointment request has been received. We will confirm via email and SMS.",
  "appointment_id": 456,
  "reference_number": "OLLMH-APT-20240315-001"
}
```

**Side effects:**
- Insert into `wp_opd_appointments` or `wp_clinic_bookings`
- Generate reference number (`OLLMH-APT-YYYYMMDD-NNN`)
- Send confirmation email to patient
- Send notification to relevant department/clinic
- Schedule reminder (cron job, `appointment_reminder_hours` before appointment)

---

### 3.3 Nursing school application (multi-step)

#### Step 1: Personal information

```
POST /ollmh/v1/applications
```

**Request body:**
```json
{
  "step": 1,
  "salutation": "Mr",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+254712345678",
  "date_of_birth": "2000-05-15",
  "gender": "male",
  "nationality": "Kenyan",
  "county": "kirinyaga",
  "address": "P.O. Box 123, Mwea",
  "id_number": "12345678",
  "programme": "krchn",
  "intake": "september",
  "turnstile_token": "0.xxxxx"
}
```

**Response (200):**
```json
{
  "success": true,
  "application_id": 789,
  "next_step": 2
}
```

#### Step 2: Academic information

```
POST /ollmh/v1/applications
```

**Request body:**
```json
{
  "step": 2,
  "application_id": 789,
  "kcse_year": "2019",
  "kcse_mean_grade": "B",
  "kcse_english": "B",
  "kcse_biology": "B+",
  "kcse_chemistry": "B",
  "kcse_mathematics": "C+",
  "previous_school": "Mwea Secondary School",
  "other_qualifications": "First Aid Certificate",
  "turnstile_token": "0.xxxxx"
}
```

#### Step 3: Document upload

```
POST /ollmh/v1/applications/upload
Content-Type: multipart/form-data
```

**Request body:**
```
application_id: 789
document_type: photo | transcript | id_copy | application_form
file: <binary>
turnstile_token: 0.xxxxx
```

**Validation:**
- `file`: required, max 5MB, allowed types: jpg, jpeg, png, pdf
- `document_type`: required, enum: `photo`, `transcript`, `id_copy`, `application_form`
- Each document type can only be uploaded once per application

**Response (200):**
```json
{
  "success": true,
  "document_id": 101,
  "file_url": "https://...wp-content/uploads/2024/01/applicant-photo-789.jpg"
}
```

#### Step 4: Review and submit

```
POST /ollmh/v1/applications
```

> **Payment fields are optional.** `payment_method` and `mpesa_phone` apply
> only when the `ollmh-payments` plugin is active and M-Pesa is approved
> (ADR-004). When the plugin is inactive, omit them — the application is
> finalised without online payment and the `payment` object is absent from the
> response.

**Request body (with optional payment — `ollmh-payments` active):**
```json
{
  "step": 4,
  "application_id": 789,
  "confirm": true,
  "payment_method": "mpesa_stk",
  "mpesa_phone": "+254712345678",
  "turnstile_token": "0.xxxxx"
}
```

**Request body (no online payment — `ollmh-payments` inactive):**
```json
{
  "step": 4,
  "application_id": 789,
  "confirm": true,
  "turnstile_token": "0.xxxxx"
}
```

**Response (200):**
```json
{
  "success": true,
  "application_id": 789,
  "status": "submitted",
  "payment": {
    "status": "pending",
    "checkout_request_id": "ws_CO_123456789",
    "message": "Please enter your M-Pesa PIN on your phone to complete the payment."
  }
}
```

> When `ollmh-payments` is inactive, the `payment` object is omitted and
> `status` is `submitted` immediately.

**Side effects:**
- Update application status to `submitted`
- **If `ollmh-payments` is active:** trigger M-Pesa STK Push to `mpesa_phone`
- Send confirmation email to applicant
- Send notification to `nursing_school_email`

---

### 3.4 M-Pesa payment callback

```
POST /ollmh/v1/payments/callback
```

This endpoint is called by Safaricom's Daraja API after an STK Push
transaction completes. It is **not** called by the front-end.

**Request body (from Safaricom):**
```json
{
  "Body": {
    "stkCallback": {
      "MerchantRequestID": "29115-34620561-1",
      "CheckoutRequestID": "ws_CO_191220191020363925",
      "ResultCode": 0,
      "ResultDesc": "The service request is processed successfully.",
      "CallbackMetadata": {
        "Item": [
          {"Name": "Amount", "Value": 1000},
          {"Name": "MpesaReceiptNumber", "Value": "NLJ7RT61SV"},
          {"Name": "PhoneNumber", "Value": "254712345678"}
        ]
      }
    }
  }
}
```

**Processing:**
- If `ResultCode` is `0`: payment successful → update `wp_application_payments`, update application status to `screening`, send notification
- If `ResultCode` is not `0`: payment failed → update `wp_application_payments` with failure reason, notify applicant

**Response (200):**
```json
{
  "ResultCode": 0,
  "ResultDesc": "Success"
}
```

---

### 3.5 Event registration

```
POST /ollmh/v1/events/register
```

**Request body:**
```json
{
  "event_id": 42,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+254712345678",
  "number_of_attendees": 2,
  "turnstile_token": "0.xxxxx"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "You are registered for this event.",
  "registration_id": 555
}
```

---

### 3.6 Public settings retrieval

```
GET /ollmh/v1/settings
GET /ollmh/v1/settings?group=contact
GET /ollmh/v1/settings?group=clinical
```

Returns all public settings (`is_public = 1`, excludes `type = 'secret'`).
Optionally filter by group.

**Response (200):**
```json
{
  "hospital_name": "Our Lady of Lourdes Mwea Hospital",
  "hospital_short_name": "OLLMH",
  "hospital_phone": "+254700123456",
  "hospital_email": "info@ollmh.org",
  "hospital_address": "Mwea, Kirinyaga County, Kenya",
  "social_facebook": "https://facebook.com/ollmh",
  "opd_operating_hours": "Monday – Friday: 8:00 AM – 5:00 PM...",
  "registration_fee_kes": "200",
  "accepted_insurance_providers": {"nhif": "NHIF...", ...}
}
```

---

### 3.7 Turnstile verification (server-side)

```
POST /ollmh/v1/turnstile/verify
```

Called internally by other endpoints to verify the Turnstile token. Not
called directly by the front-end (the front-end includes the token in
form submissions, and each endpoint calls this internally).

**Request body:**
```json
{
  "token": "0.xxxxx"
}
```

**Internal logic:**
1. POST to `https://challenges.cloudflare.com/turnstile/v0/siteverify`
2. With `secret` = `turnstile_secret_key` setting and `response` = token
3. If `success` is `true` → return success
4. If `success` is `false` → return error with error codes

---

### 3.8 Newsletter subscription

```
POST /ollmh/v1/newsletter/subscribe
```

Handles the footer newsletter signup form (Band 2 — see
[`HEADER-FOOTER-STRUCTURE.md`](./HEADER-FOOTER-STRUCTURE.md) → Band 2).
Implements a **double opt-in** flow for compliance with Kenya's Data
Protection Act 2019 (see [`COOKIE-CONSENT.md`](./COOKIE-CONSENT.md)).

**Request body:**
```json
{
  "email": "john@example.com",
  "consent": true,
  "turnstile_token": "0.xxxxx"
}
```

**Validation:**
- `email`: required, valid email, max 191, not already subscribed
- `consent`: required, must be `true` (the checkbox on the form must be checked)
- `turnstile_token`: required if `captcha_on_newsletter_signup` setting is `1`

**Response (200):**
```json
{
  "success": true,
  "message": "Thank you for subscribing! Please check your email to confirm your subscription.",
  "subscriber_id": 321
}
```

**Response (400) — already subscribed:**
```json
{
  "success": false,
  "code": "already_subscribed",
  "message": "This email address is already subscribed to our newsletter."
}
```

**Response (400) — consent missing:**
```json
{
  "success": false,
  "errors": {
    "consent": "You must agree to the Privacy Policy and Terms of Service to subscribe."
  }
}
```

**Side effects:**
1. Insert into `wp_newsletter_subscribers` with `status = 'pending'` and a
   random `confirmation_token` (32-char hex)
2. Send a **confirmation email** to the subscriber with a confirmation link:
   `{site_url}/newsletter/confirm/?token={confirmation_token}`
3. Store the consent timestamp and IP address for audit trail
4. Do **not** add to active mailing list until confirmation link is clicked

**Confirmation flow:**
```
GET /newsletter/confirm/?token={confirmation_token}
```

When the user clicks the confirmation link:
1. Look up the subscriber by `confirmation_token`
2. If found and `status = 'pending'`:
   - Update `status` to `subscribed`
   - Set `confirmed_at` timestamp
   - Send "Welcome to OLLMH newsletter" email
   - Show a "Subscription confirmed" success page
3. If token is invalid or already confirmed:
   - Show an error or "already subscribed" message

**Unsubscribe flow:**
```
GET /newsletter/unsubscribe/?token={subscriber_token}
```

Every newsletter email includes an unsubscribe link with the subscriber's
unique token. When clicked:
1. Look up the subscriber by token
2. Update `status` to `unsubscribed`
3. Show an "You have been unsubscribed" confirmation page
4. Optionally ask for unsubscribe reason (optional feedback, not required)

**Admin notification:**
On successful confirmation, the admin is not notified (to avoid noise).
The admin can view all subscribers via the Newsletter admin screen (see
[`ADMIN-SIDEBAR.md`](./ADMIN-SIDEBAR.md)).

---

### 3.9 Cookie consent preference

```
POST /ollmh/v1/cookie-consent
```

Stores the user's cookie consent preference (see
[`COOKIE-CONSENT.md`](./COOKIE-CONSENT.md) for the full cookie consent
strategy). This endpoint is called by the cookie consent banner JS when
the user makes a choice.

**Request body:**
```json
{
  "preference": "all",
  "categories": ["essential", "analytics", "advertising"]
}
```

**Validation:**
- `preference`: required, enum: `all`, `essential_only`, `custom`
- `categories`: required if `preference` is `custom`, array of strings from
  enum: `essential`, `analytics`, `advertising`
- `essential` is always included (cannot be disabled)

**Response (200):**
```json
{
  "success": true,
  "preference": "all",
  "categories": ["essential", "analytics", "advertising"]
}
```

**Side effects:**
1. Store the preference in a cookie (`ollmh_cookie_consent`) for 365 days
2. Store the preference in `wp_cookie_consents` table (for audit trail)
   with IP address, timestamp, and preference
3. Return the preference so the JS can enable/disable scripts accordingly

**No Turnstile required** — this is a simple preference storage endpoint,
not a form submission that could be abused by bots.

---

## 4. Rate limiting

All public endpoints are rate-limited to prevent abuse:

| Endpoint | Rate limit |
|---|---|
| `POST /contact` | 5 requests per IP per 10 minutes |
| `POST /appointments` | 3 requests per IP per 10 minutes |
| `POST /applications` | 2 requests per IP per 10 minutes |
| `POST /applications/upload` | 10 requests per application per hour |
| `POST /events/register` | 5 requests per IP per 10 minutes |
| `POST /newsletter/subscribe` | 3 requests per IP per 10 minutes |
| `POST /cookie-consent` | 10 requests per IP per hour |
| `GET /settings` | 60 requests per IP per minute |

Rate limiting is implemented via WordPress transients (stores request
counts per IP with TTL).

---

## 5. Error response format

All error responses follow this structure:

```json
{
  "success": false,
  "code": "validation_error",
  "message": "Please correct the errors below.",
  "errors": {
    "field_name": "Human-readable error message."
  }
}
```

| HTTP status | Code | Meaning |
|---|---|---|
| 400 | `validation_error` | Field validation failed |
| 400 | `turnstile_failed` | Bot verification failed |
| 429 | `rate_limited` | Too many requests |
| 403 | `forbidden` | Missing capability or invalid nonce |
| 404 | `not_found` | Resource not found |
| 500 | `server_error` | Internal server error |
