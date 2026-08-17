# Email Templates

> This document specifies all transactional email and SMS templates for
> the OLLMH WordPress site.
>
> **Related:** [`SETTINGS.md`](./SETTINGS.md) → `email` and `notifications`
> groups, [`PLUGIN-ARCHITECTURE.md`](./PLUGIN-ARCHITECTURE.md) →
> `ollmh-notifications` plugin.

---

## 1. Email configuration

All emails are sent via SMTP (configured in `wp_settings` → `email` group).
In local development, MailHog catches all emails (see
[`ENVIRONMENT-SETUP.md`](./ENVIRONMENT-SETUP.md)).

**From address:** `smtp_from_email` setting
**From name:** `smtp_from_name` setting
**Format:** HTML (with plain-text fallback)

---

## 2. Base email template

All emails use a shared HTML wrapper:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{email_subject}}</title>
</head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);">

          <!-- Header -->
          <tr>
            <td style="background:#0046a8;padding:20px 30px;text-align:center;">
              <img src="{{logo_url}}" alt="OLLMH" height="48" style="display:inline-block;">
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:30px;color:#1a1a1a;font-size:16px;line-height:1.6;">
              {{email_body}}
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f5f5f5;padding:20px 30px;border-top:1px solid #e0e0e0;font-size:14px;color:#666;text-align:center;">
              <p style="margin:0 0 10px;">
                <strong>Our Lady of Lourdes Mwea Hospital</strong><br>
                Mwea, Kirinyaga County, Kenya<br>
                {{hospital_phone}} | {{hospital_email}}
              </p>
              <p style="margin:0;font-size:12px;color:#999;">
                &copy; {{year}} OLLMH. All rights reserved.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```

**Template variables:**

| Variable | Source | Example |
|---|---|---|
| `{{email_subject}}` | Per template | "Appointment Confirmation" |
| `{{email_body}}` | Per template | HTML content |
| `{{logo_url}}` | Theme logo URL | `https://ollmh.org/wp-content/themes/ollmh-child/assets/images/logo.png` |
| `{{hospital_phone}}` | `hospital_phone` setting | `+254700123456` |
| `{{hospital_email}}` | `hospital_email` setting | `info@ollmh.org` |
| `{{year}}` | Current year | `2024` |

---

## 3. Email templates

### 3.1 Contact form — auto-reply to sender

**Trigger:** Contact form submitted successfully
**Recipient:** The form submitter
**Subject:** `Thank you for contacting OLLMH`

```html
<h2>Thank you for your message, {{name}}!</h2>

<p>We have received your enquiry and will respond within 48 hours.</p>

<p><strong>Your message:</strong></p>
<blockquote style="border-left:3px solid #0046a8;padding-left:15px;color:#666;">
  {{message}}
</blockquote>

<p>If you need urgent medical attention, please call our 24-hour emergency line: <strong>{{emergency_phone}}</strong></p>

<p>Best regards,<br>The OLLMH Team</p>
```

### 3.2 Contact form — notification to admin

**Trigger:** Contact form submitted successfully
**Recipient:** `admin_email` setting
**Subject:** `New contact form submission: {{subject}}`

```html
<h2>New Contact Form Submission</h2>

<table style="width:100%;font-size:16px;">
  <tr><td style="padding:8px 0;font-weight:bold;width:120px;">Name:</td><td>{{name}}</td></tr>
  <tr><td style="padding:8px 0;font-weight:bold;">Email:</td><td>{{email}}</td></tr>
  <tr><td style="padding:8px 0;font-weight:bold;">Phone:</td><td>{{phone}}</td></tr>
  <tr><td style="padding:8px 0;font-weight:bold;">Subject:</td><td>{{subject}}</td></tr>
  <tr><td style="padding:8px 0;font-weight:bold;">Department:</td><td>{{department}}</td></tr>
</table>

<p><strong>Message:</strong></p>
<blockquote style="border-left:3px solid #0046a8;padding-left:15px;color:#666;">
  {{message}}
</blockquote>

<p><a href="{{admin_url}}/admin.php?page=ollmh-contact-submissions&view={{submission_id}}" style="display:inline-block;padding:10px 20px;background:#0046a8;color:#fff;text-decoration:none;border-radius:4px;">View in Admin</a></p>
```

### 3.3 Appointment confirmation

**Trigger:** Appointment booked successfully
**Recipient:** The patient
**Subject:** `Appointment Confirmation — {{reference_number}}`

```html
<h2>Appointment Confirmed</h2>

<p>Dear {{patient_name}},</p>

<p>Your appointment has been booked. Here are the details:</p>

<table style="width:100%;font-size:16px;border:1px solid #e0e0e0;border-radius:4px;">
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Reference</td><td style="padding:12px;">{{reference_number}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Type</td><td style="padding:12px;">{{appointment_type}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Department</td><td style="padding:12px;">{{department_name}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Date</td><td style="padding:12px;">{{appointment_date}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Time</td><td style="padding:12px;">{{appointment_time}}</td></tr>
</table>

<p><strong>Please arrive 15 minutes before your appointment time.</strong></p>

<p>Bring the following documents:</p>
<ul>
  <li>National ID or birth certificate</li>
  <li>NHIF card (if applicable)</li>
  <li>Previous medical records (if any)</li>
</ul>

<p>If you need to cancel or reschedule, please call us at <strong>{{hospital_phone}}</strong> at least {{cancellation_hours}} hours before your appointment.</p>

<p>We look forward to serving you.</p>

<p>Best regards,<br>The OLLMH Team</p>
```

### 3.4 Appointment reminder

**Trigger:** Cron job, `appointment_reminder_hours` before appointment (default: 24 hours)
**Recipient:** The patient
**Subject:** `Reminder: Your appointment tomorrow at {{appointment_time}}`

```html
<h2>Appointment Reminder</h2>

<p>Dear {{patient_name}},</p>

<p>This is a reminder for your appointment at Our Lady of Lourdes Mwea Hospital:</p>

<table style="width:100%;font-size:16px;border:1px solid #e0e0e0;border-radius:4px;">
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Reference</td><td style="padding:12px;">{{reference_number}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Date</td><td style="padding:12px;">{{appointment_date}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Time</td><td style="padding:12px;">{{appointment_time}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Department</td><td style="padding:12px;">{{department_name}}</td></tr>
</table>

<p><strong>Please arrive 15 minutes before your appointment time.</strong></p>

<p>If you need to cancel, please call <strong>{{hospital_phone}}</strong>.</p>
```

### 3.5 Application received

**Trigger:** Nursing school application submitted successfully
**Recipient:** The applicant
**Subject:** `Application Received — {{application_reference}}`

```html
<h2>Application Received</h2>

<p>Dear {{first_name}} {{last_name}},</p>

<p>Thank you for applying to the Our Lady of Lourdes Mwea Hospital Nursing School. Your application has been received successfully.</p>

<table style="width:100%;font-size:16px;border:1px solid #e0e0e0;border-radius:4px;">
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Application Reference</td><td style="padding:12px;">{{application_reference}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Programme</td><td style="padding:12px;">{{programme_name}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Intake</td><td style="padding:12px;">{{intake_name}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Application Fee</td><td style="padding:12px;">KES {{application_fee}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Payment Status</td><td style="padding:12px;color:{{payment_status_color}};">{{payment_status}}</td></tr>
</table>

<p><strong>What happens next?</strong></p>
<ol>
  <li>Your application will be reviewed by our admissions team (1–2 weeks)</li>
  <li>If you meet the minimum qualifications, you will be invited for an interview</li>
  <li>You will receive notifications at each stage of the process</li>
</ol>

<p>You can check your application status at any time: <a href="{{site_url}}/application-status/?ref={{application_reference}}">Check Status</a></p>

<p>If you have questions, please contact us at <strong>{{nursing_school_email}}</strong></p>
```

### 3.6 Application status update

**Trigger:** Application status changes in admin
**Recipient:** The applicant
**Subject:** `Application Update: {{status_label}}`

```html
<h2>Application Status Update</h2>

<p>Dear {{first_name}},</p>

<p>The status of your nursing school application has been updated:</p>

<table style="width:100%;font-size:16px;border:1px solid #e0e0e0;border-radius:4px;">
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Reference</td><td style="padding:12px;">{{application_reference}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">New Status</td><td style="padding:12px;font-weight:bold;color:{{status_color}};">{{status_label}}</td></tr>
</table>

{{status_specific_message}}

<p>Check your full application status: <a href="{{site_url}}/application-status/?ref={{application_reference}}">View Application</a></p>

<p>If you have questions, please contact us at <strong>{{nursing_school_email}}</strong></p>
```

**Status-specific messages:**

| Status | Message |
|---|---|
| `screening` | "Your application is now under review by our admissions team. We will contact you within 1–2 weeks." |
| `interview` | "You have been selected for an interview! Please check your email for the interview date, time, and location." |
| `offered` | "Congratulations! You have been offered admission to the OLLMH Nursing School. Please confirm your acceptance within 14 days." |
| `accepted` | "Welcome to OLLMH Nursing School! We will send you joining instructions shortly." |
| `rejected` | "We regret to inform you that your application was not successful this time. You may reapply for the next intake." |
| `waitlisted` | "You have been placed on the waitlist. We will contact you if a position becomes available." |
| `deferred` | "Your application has been deferred to the next intake. You do not need to reapply." |

### 3.7 Event registration confirmation

**Trigger:** Event registration submitted
**Recipient:** The registrant
**Subject:** `Registered: {{event_title}}`

```html
<h2>Event Registration Confirmed</h2>

<p>Dear {{name}},</p>

<p>You are registered for the following event:</p>

<table style="width:100%;font-size:16px;border:1px solid #e0e0e0;border-radius:4px;">
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Event</td><td style="padding:12px;">{{event_title}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Date</td><td style="padding:12px;">{{event_date}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Time</td><td style="padding:12px;">{{event_time}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Location</td><td style="padding:12px;">{{event_location}}</td></tr>
  <tr><td style="padding:12px;font-weight:bold;background:#f5f5f5;">Attendees</td><td style="padding:12px;">{{number_of_attendees}}</td></tr>
</table>

<p>We look forward to seeing you there!</p>
```

### 3.8 Password reset

**Trigger:** User requests password reset
**Recipient:** The user
**Subject:** `Password Reset — OLLMH`

```html
<h2>Password Reset Request</h2>

<p>Someone has requested a password reset for your OLLMH account.</p>

<p>If this was you, click the link below to reset your password:</p>

<p><a href="{{reset_link}}" style="display:inline-block;padding:12px 24px;background:#0046a8;color:#fff;text-decoration:none;border-radius:4px;">Reset Password</a></p>

<p>This link will expire in 24 hours.</p>

<p>If you did not request a password reset, please ignore this email. Your password will not be changed.</p>
```

---

## 4. SMS templates

SMS messages are limited to 160 characters. All SMS templates are plain text.

### 4.1 Appointment reminder (SMS)

```
OLLMH: Reminder for your appointment on {{date}} at {{time}}. Dept: {{department}}. Ref: {{reference}}. Call {{phone}} to reschedule.
```

### 4.2 Application status update (SMS)

```
OLLMH: Your nursing school application ({{reference}}) status is now: {{status_label}}. Check your email for details.
```

### 4.3 Event reminder (SMS)

```
OLLMH: Reminder for {{event_title}} on {{date}} at {{time}}, {{location}}. We look forward to seeing you!
```

---

## 5. Notification queue

All notifications (email and SMS) are queued in a database table and
processed by a cron job (see [`CRON-JOBS.md`](./CRON-JOBS.md)). This
prevents slow SMTP/SMS API calls from blocking the user's form submission.

**Queue flow:**
1. Form submission triggers → notification added to queue
2. Cron job runs every 5 minutes → processes queued notifications
3. Each notification is sent via SMTP (email) or SMS gateway
4. Success/failure is logged in `wp_notification_logs`
5. Failed notifications are retried up to `job_max_attempts` times

---

## 6. Email template variables

All templates support these global variables:

| Variable | Description |
|---|---|
| `{{site_url}}` | WordPress site URL |
| `{{site_name}}` | Hospital name (`hospital_name` setting) |
| `{{hospital_phone}}` | Primary phone (`hospital_phone` setting) |
| `{{hospital_email}}` | Primary email (`hospital_email` setting) |
| `{{emergency_phone}}` | Emergency phone (`hospital_emergency_phone` setting) |
| `{{nursing_school_email}}` | Nursing school email (`nursing_school_email` setting) |
| `{{admin_url}}` | WordPress admin URL |
| `{{logo_url}}` | Theme logo URL |
| `{{year}}` | Current year |

Form-specific variables are listed in each template above.
