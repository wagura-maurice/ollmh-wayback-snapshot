# Front-End Forms

> This document specifies all front-end forms on the OLLMH website —
> fields, validation, error handling, Turnstile integration, and
> success/error states.
>
> **Related:** [`REST-API-SPEC.md`](./REST-API-SPEC.md) for the API
> endpoints, [`SETTINGS.md`](./SETTINGS.md) for form-related settings.

---

## 1. Forms overview

| Form | Page | Endpoint | Turnstile | Payment |
|---|---|---|---|---|
| Contact form | `/contacts/` | `POST /ollmh/v1/contact` | Yes (if `captcha_on_contact_form=1`) | No |
| Appointment booking | `/out-patient-dept/` or modal | `POST /ollmh/v1/appointments` | Yes (if `captcha_on_appointment_booking=1`) | No |
| Nursing school application | `/medical-school-application-form/` | `POST /ollmh/v1/applications` (multi-step) | Yes (if `captcha_on_application_form=1`) | Yes (M-Pesa) |
| Event registration | Event single page | `POST /ollmh/v1/events/register` | Yes | No |

---

## 2. Form behavior

All forms use **AJAX submission** (no page reload). The flow:

1. User fills form → clicks submit
2. JS validates fields client-side
3. JS submits via `fetch()` to REST API endpoint
4. Server validates → returns success or error JSON
5. On success: show success message, reset form, optionally redirect
6. On error: show field-level error messages inline
7. During submission: disable submit button, show loading spinner

**No form uses traditional HTTP POST with page reload.** This provides a
better UX and allows Turnstile token to be included without page reload.

---

## 3. Contact form

### Fields

| Field | Type | Required | Validation | Notes |
|---|---|---|---|---|
| Name | text | Yes | min 2, max 100 | |
| Email | email | Yes | valid email, max 191 | |
| Phone | tel | No | max 20 | |
| Subject | select | Yes | enum | Options: General, Appointments, Billing, Nursing School, HR, Other |
| Department | select | No | valid department slug | Populated from `department` CPT |
| Message | textarea | Yes | min 10, max 5000 | |
| Turnstile | hidden | Yes (if enabled) | valid token | Rendered as Turnstile widget |

### HTML structure

```html
<form id="ollmh-contact-form" class="ollmh-form" novalidate>
  <div class="form-field">
    <label for="contact-name">Name <span class="required">*</span></label>
    <input type="text" id="contact-name" name="name" required maxlength="100">
    <span class="field-error" data-error-for="name"></span>
  </div>

  <div class="form-field">
    <label for="contact-email">Email <span class="required">*</span></label>
    <input type="email" id="contact-email" name="email" required maxlength="191">
    <span class="field-error" data-error-for="email"></span>
  </div>

  <div class="form-field">
    <label for="contact-phone">Phone</label>
    <input type="tel" id="contact-phone" name="phone" maxlength="20">
    <span class="field-error" data-error-for="phone"></span>
  </div>

  <div class="form-field">
    <label for="contact-subject">Subject <span class="required">*</span></label>
    <select id="contact-subject" name="subject" required>
      <option value="">Select a subject...</option>
      <option value="general">General Enquiry</option>
      <option value="appointments">Appointments</option>
      <option value="billing">Billing</option>
      <option value="nursing_school">Nursing School</option>
      <option value="hr">HR / Jobs</option>
      <option value="other">Other</option>
    </select>
    <span class="field-error" data-error-for="subject"></span>
  </div>

  <div class="form-field">
    <label for="contact-department">Department</label>
    <select id="contact-department" name="department">
      <option value="">Select a department...</option>
      <!-- Populated dynamically from department CPT -->
    </select>
    <span class="field-error" data-error-for="department"></span>
  </div>

  <div class="form-field">
    <label for="contact-message">Message <span class="required">*</span></label>
    <textarea id="contact-message" name="message" required maxlength="5000" rows="5"></textarea>
    <span class="field-error" data-error-for="message"></span>
  </div>

  <div class="form-field turnstile-container">
    <!-- Cloudflare Turnstile widget renders here -->
  </div>

  <div class="form-actions">
    <button type="submit" class="btn btn-primary">
      <span class="btn-text">Send Message</span>
      <span class="btn-spinner" hidden><i class="icon-spinner"></i></span>
    </button>
  </div>

  <div class="form-success" hidden>
    <i class="icon-check"></i>
    <p>Your message has been sent. We will respond within 48 hours.</p>
  </div>
</form>
```

---

## 4. Appointment booking form

### Fields

| Field | Type | Required | Validation | Notes |
|---|---|---|---|---|
| Patient name | text | Yes | min 2, max 100 | |
| Email | email | Yes | valid email | |
| Phone | tel | Yes | max 20, Kenya phone format | |
| Appointment type | radio | Yes | `opd` or `clinic` | |
| Department | select | Yes (if OPD) | valid department | Populated from CPT |
| Clinic | select | Yes (if clinic) | valid clinic | Populated from CPT |
| Preferred date | date | Yes | valid date, within advance_days | Min = today + min_lead_hours |
| Preferred time | time | Yes | valid time | |
| Reason | textarea | No | max 1000 | |
| New patient | checkbox | Yes | boolean | |
| Turnstile | hidden | Yes (if enabled) | valid token | |

### Date/time constraints

- **Min date:** `today + appointment_min_lead_hours` (default: 2 hours)
- **Max date:** `today + appointment_advance_days` (default: 14 days)
- **Disabled days:** Sundays (configurable in future)
- **Time slots:** `appointment_slot_duration_minutes` intervals (default: 30 min)

---

## 5. Nursing school application form (multi-step)

This is the most complex form — 4 steps with progress indicator.

### Step 1: Personal Information

| Field | Type | Required | Validation |
|---|---|---|---|
| Salutation | select | Yes | From `profile_salutations` setting |
| First name | text | Yes | min 2, max 50 |
| Last name | text | Yes | min 2, max 50 |
| Email | email | Yes | valid email |
| Phone | tel | Yes | Kenya phone format |
| Date of birth | date | Yes | min 1900-01-01, max today |
| Gender | select | Yes | From `profile_genders` setting |
| Nationality | select | Yes | From `profile_nationalities` setting |
| County | select | Yes | From `profile_counties` setting |
| Address | textarea | Yes | max 500 |
| ID number | text | Yes | max 20 |
| Programme | select | Yes | From `nursing_programmes_offered` setting |
| Intake | select | Yes | From `nursing_intake_months` setting |

### Step 2: Academic Information

| Field | Type | Required | Validation |
|---|---|---|---|
| KCSE year | select | Yes | 1980–current year |
| KCSE mean grade | select | Yes | A, A-, B+, B, B-, C+, C, C-, D+, D, D-, E |
| KCSE English grade | select | Yes | Same scale |
| KCSE Biology grade | select | Yes | Same scale |
| KCSE Chemistry grade | select | Yes | Same scale |
| KCSE Mathematics grade | select | Yes | Same scale |
| Previous school | text | Yes | max 200 |
| Other qualifications | textarea | No | max 1000 |

### Step 3: Document Upload

| Document | Required | Max size | Allowed types |
|---|---|---|---|
| Passport-size photo | Yes (if `application_requires_photo=1`) | 2MB | jpg, jpeg, png |
| Academic transcripts/certificates | Yes (if `application_requires_transcripts=1`) | 5MB | pdf, jpg, png |
| National ID or birth certificate | Yes (if `application_requires_id_copy=1`) | 5MB | pdf, jpg, png |
| Application form (downloaded PDF) | Yes (if required) | 5MB | pdf |

Each document is uploaded individually via `POST /ollmh/v1/applications/upload`
with a progress bar.

### Step 4: Review and Submit

- Display all entered information for review
- Show uploaded document thumbnails
- Display application fee amount (`nursing_application_fee_kes` setting)
- M-Pesa phone number input
- Confirm checkbox ("I confirm the information is correct")
- Submit button triggers M-Pesa STK Push

### Progress indicator

```html
<div class="application-progress">
  <div class="step active" data-step="1">
    <span class="step-number">1</span>
    <span class="step-label">Personal Info</span>
  </div>
  <div class="step" data-step="2">
    <span class="step-number">2</span>
    <span class="step-label">Academic Info</span>
  </div>
  <div class="step" data-step="3">
    <span class="step-number">3</span>
    <span class="step-label">Documents</span>
  </div>
  <div class="step" data-step="4">
    <span class="step-number">4</span>
    <span class="step-label">Review & Pay</span>
  </div>
</div>
```

---

## 6. Event registration form

### Fields

| Field | Type | Required | Validation |
|---|---|---|---|
| Name | text | Yes | min 2, max 100 |
| Email | email | Yes | valid email |
| Phone | tel | Yes | max 20 |
| Number of attendees | number | Yes | min 1, max 10 |
| Turnstile | hidden | Yes | valid token |

---

## 7. Turnstile integration

All forms include a Cloudflare Turnstile widget. The widget renders inside
a `<div class="turnstile-container">` element.

### Front-end rendering

```html
<!-- In <head> or before form -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

<!-- Inside the form -->
<div class="cf-turnstile" data-sitekey="SITE_KEY" data-theme="light"></div>
```

The `data-sitekey` is populated from the `turnstile_site_key` setting
(retrieved via the public settings API).

### Token handling

When the form is submitted, the Turnstile widget injects a hidden input
named `cf-turnstile-response` containing the token. The JS form handler
reads this value and includes it as `turnstile_token` in the API request.

```javascript
const turnstileToken = form.querySelector('[name="cf-turnstile-response"]')?.value;
if (!turnstileToken) {
  showError('turnstile', 'Please complete the bot verification.');
  return;
}
// Include in fetch body
body.turnstile_token = turnstileToken;
```

### Reset after submission

After a successful or failed submission, reset the Turnstile widget so the
user can submit again:

```javascript
turnstile.reset(form.querySelector('.cf-turnstile'));
```

---

## 8. Client-side validation

Validation runs on three events:
1. **On blur:** Validate individual field when user leaves it
2. **On submit:** Validate all fields before AJAX submission
3. **Server-side:** Server validates again (never trust client-side)

### Validation rules

```javascript
const validationRules = {
  email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
  phone: (value) => /^\+?[\d\s\-()]{10,20}$/.test(value),
  required: (value) => value.trim().length > 0,
  minLength: (value, min) => value.trim().length >= min,
  maxLength: (value, max) => value.trim().length <= max,
  date: (value) => !isNaN(Date.parse(value)),
  futureDate: (value) => new Date(value) > new Date(),
};
```

### Error display

Errors are displayed inline below each field:

```html
<div class="form-field has-error">
  <label for="email">Email *</label>
  <input type="email" id="email" name="email" value="invalid">
  <span class="field-error" role="alert">Please enter a valid email address.</span>
</div>
```

The `has-error` class adds a red border to the input. The `field-error`
span is announced by screen readers via `role="alert"`.

---

## 9. Success and error states

### Success state

```html
<div class="form-success" role="status">
  <i class="icon-check-circle" aria-hidden="true"></i>
  <h3>Thank you!</h3>
  <p>Your message has been sent. We will respond within 48 hours.</p>
  <button type="button" class="btn btn-secondary" onclick="resetForm()">Send another message</button>
</div>
```

### Error state (general)

```html
<div class="form-error" role="alert">
  <i class="icon-exclamation-circle" aria-hidden="true"></i>
  <p>There was a problem submitting your form. Please check the errors above and try again.</p>
</div>
```

### Error state (rate limited)

```html
<div class="form-error" role="alert">
  <i class="icon-clock" aria-hidden="true"></i>
  <p>You've submitted too many requests. Please wait 10 minutes before trying again.</p>
</div>
```
