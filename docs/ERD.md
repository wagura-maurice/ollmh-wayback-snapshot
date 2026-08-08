# Consolidated Entity-Relationship Diagram (ERD)

This document is the **single-source ERD** for the entire OLLMH dynamic website
schema. It covers all **80 tables** (7 shared/platform + 73 page-specific) and
their **116 foreign-key relationships**, grouped into logical clusters.

For table definitions and column-level details, see:
- [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md) — the 7 shared tables.
- [`pages/`](./pages/) — one file per page with its own `CREATE TABLE` statements.

> **How to read this document:** Mermaid `erDiagram` blocks render inline on
> GitHub. Each cluster diagram shows only the tables in that cluster plus the
> shared tables they reference (shown in a lighter style). The final
> "Cross-cluster" diagram shows how the clusters connect through shared tables.

---

## Cluster 1 — Platform core (shared tables)

Defined in [`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md). Every other
cluster foreign-keys into these.

```mermaid
erDiagram
    pages ||--o{ page_media : "has"
    media_assets ||--o{ page_media : "appears on"
    media_assets }o--o| users : "uploaded_by"
    pages }o--o| media_assets : "hero_media"
    menu_items }o--o| menu_items : "parent"
    menu_items }o--o| pages : "links to"
    departments }o--o| pages : "described by"
    staff }o--o| departments : "belongs to"
    staff }o--o| media_assets : "photo"

    pages {
        BIGINT id PK
        VARCHAR slug
        VARCHAR title
        ENUM page_type
        BIGINT hero_media_id FK
        ENUM status
    }
    media_assets {
        BIGINT id PK
        VARCHAR file_path
        ENUM media_type
        BIGINT uploaded_by FK
    }
    page_media {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT media_id FK
        ENUM role
    }
    users {
        BIGINT id PK
        VARCHAR email
        ENUM role
    }
    menu_items {
        BIGINT id PK
        ENUM menu_area
        BIGINT parent_id FK
        BIGINT page_id FK
    }
    departments {
        BIGINT id PK
        VARCHAR slug
        ENUM category
        BIGINT page_id FK
    }
    staff {
        BIGINT id PK
        VARCHAR full_name
        BIGINT department_id FK
        BIGINT photo_media_id FK
    }
```

---

## Cluster 2 — Home page

Defined in [`pages/index.md`](./pages/index.md).

```mermaid
erDiagram
    pages ||--o{ home_slides : "page_id"
    media_assets ||--o{ home_slides : "media_id"
    pages ||--o{ home_slides : "link_page_id"
    pages ||--o{ home_in_focus_items : "page_id"
    media_assets ||--o{ home_in_focus_items : "media_id"
    pages ||--o{ home_in_focus_items : "link_page_id"
    pages ||--o{ home_feature_blocks : "page_id"
    media_assets ||--o{ home_feature_blocks : "media_id"
    departments ||--o{ home_feature_blocks : "department_id"
    pages ||--o{ home_feature_blocks : "read_more_page_id"
    pages ||--o{ home_news_promos : "page_id"
    media_assets ||--o{ home_news_promos : "media_id"
    news_articles ||--o{ home_news_promos : "article_id"

    home_slides {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT media_id FK
        BIGINT link_page_id FK
    }
    home_in_focus_items {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT media_id FK
        BIGINT link_page_id FK
    }
    home_feature_blocks {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT media_id FK
        BIGINT department_id FK
        BIGINT read_more_page_id FK
    }
    home_news_promos {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT media_id FK
        BIGINT article_id FK
    }
```

---

## Cluster 3 — News (feed + articles)

Defined in [`pages/news/index.md`](./pages/news/index.md) (feed/taxonomy) and
[`pages/news/article-template.md`](./pages/news/article-template.md) (articles).

```mermaid
erDiagram
    pages ||--o{ news_articles : "page_id"
    news_categories ||--o{ news_articles : "category_id"
    news_categories }o--o| news_categories : "parent"
    users ||--o{ news_articles : "author_id"
    media_assets ||--o{ news_articles : "hero_media_id"
    news_articles ||--o{ news_article_tags : "article_id"
    news_tags ||--o{ news_article_tags : "tag_id"
    news_articles ||--o{ news_article_media : "article_id"
    media_assets ||--o{ news_article_media : "media_id"
    news_articles ||--o{ news_article_revisions : "article_id"
    users ||--o{ news_article_revisions : "editor_id"
    news_articles ||--o{ news_comments : "article_id"
    news_comments }o--o| news_comments : "parent"

    news_articles {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT category_id FK
        BIGINT author_id FK
        BIGINT hero_media_id FK
        VARCHAR slug
        ENUM status
    }
    news_categories {
        BIGINT id PK
        VARCHAR slug
        BIGINT parent_id FK
    }
    news_tags {
        BIGINT id PK
        VARCHAR slug
    }
    news_article_tags {
        BIGINT article_id PK,FK
        BIGINT tag_id PK,FK
    }
    news_article_media {
        BIGINT id PK
        BIGINT article_id FK
        BIGINT media_id FK
    }
    news_article_revisions {
        BIGINT id PK
        BIGINT article_id FK
        BIGINT editor_id FK
    }
    news_comments {
        BIGINT id PK
        BIGINT article_id FK
        BIGINT parent_id FK
    }
    newsletter_subscribers {
        BIGINT id PK
        VARCHAR email
    }
```

---

## Cluster 4 — Events (calendar + event pages)

Defined in [`pages/events/index.md`](./pages/events/index.md) (calendar/taxonomy)
and [`pages/events/event-template.md`](./pages/events/event-template.md)
(individual events).

```mermaid
erDiagram
    pages ||--o{ events : "page_id"
    event_categories ||--o{ events : "category_id"
    event_categories }o--o| event_categories : "parent"
    media_assets ||--o{ events : "hero_media_id"
    events ||--o{ event_registrations : "event_id"
    events ||--o{ event_media : "event_id"
    media_assets ||--o{ event_media : "media_id"

    events {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT category_id FK
        BIGINT hero_media_id FK
        VARCHAR slug
        DATETIME starts_at
        ENUM status
    }
    event_categories {
        BIGINT id PK
        VARCHAR slug
        BIGINT parent_id FK
    }
    event_registrations {
        BIGINT id PK
        BIGINT event_id FK
        VARCHAR attendee_email
        ENUM status
    }
    event_media {
        BIGINT id PK
        BIGINT event_id FK
        BIGINT media_id FK
    }
```

---

## Cluster 5 — Nursing school & application workflow

Defined in [`pages/about-nursing-school.md`](./pages/about-nursing-school.md)
and [`pages/medical-school-application-form.md`](./pages/medical-school-application-form.md).

```mermaid
erDiagram
    pages ||--|| nursing_school_profile : "page_id"
    media_assets ||--o{ nursing_school_profile : "hero_media_id"
    nursing_school_profile ||--o{ nursing_programmes : "school_profile_id"
    nursing_school_profile ||--o{ nursing_facilities : "school_profile_id"
    media_assets ||--o{ nursing_facilities : "media_id"
    nursing_programmes ||--o{ nursing_intakes : "programme_id"

    pages ||--o{ applications : "page_id"
    applicants ||--o{ applications : "applicant_id"
    nursing_programmes ||--o{ applications : "programme_id"
    nursing_intakes ||--o{ applications : "intake_id"
    users ||--o{ applications : "reviewed_by"
    applications ||--o{ application_documents : "application_id"
    media_assets ||--o{ application_documents : "media_id"
    pages ||--o{ application_form_downloads : "page_id"
    media_assets ||--o{ application_form_downloads : "media_id"
    applications ||--o{ application_status_history : "application_id"
    users ||--o{ application_status_history : "changed_by"
    applications ||--o{ application_referees : "application_id"
    applications ||--o{ application_reviews : "application_id"
    users ||--o{ application_reviews : "reviewer_id"
    applications ||--o{ application_payments : "application_id"
    applications ||--o{ application_notifications : "application_id"

    nursing_school_profile {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT hero_media_id FK
    }
    nursing_programmes {
        BIGINT id PK
        BIGINT school_profile_id FK
        VARCHAR slug
    }
    nursing_facilities {
        BIGINT id PK
        BIGINT school_profile_id FK
        BIGINT media_id FK
    }
    nursing_intakes {
        BIGINT id PK
        BIGINT programme_id FK
    }
    applicants {
        BIGINT id PK
        VARCHAR email
    }
    applications {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT applicant_id FK
        BIGINT programme_id FK
        BIGINT intake_id FK
        BIGINT reviewed_by FK
        ENUM status
    }
    application_documents {
        BIGINT id PK
        BIGINT application_id FK
        BIGINT media_id FK
    }
    application_form_downloads {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT media_id FK
    }
    application_status_history {
        BIGINT id PK
        BIGINT application_id FK
        BIGINT changed_by FK
    }
    application_referees {
        BIGINT id PK
        BIGINT application_id FK
    }
    application_reviews {
        BIGINT id PK
        BIGINT application_id FK
        BIGINT reviewer_id FK
    }
    application_payments {
        BIGINT id PK
        BIGINT application_id FK
    }
    application_notifications {
        BIGINT id PK
        BIGINT application_id FK
    }
```

---

## Cluster 6 — Departments, wards & clinical services

Defined in [`pages/ollmh-departments.md`](./pages/ollmh-departments.md),
[`pages/wards.md`](./pages/wards.md),
[`pages/out-patient-dept.md`](./pages/out-patient-dept.md),
[`pages/in-patient-dept.md`](./pages/in-patient-dept.md),
[`pages/special-medical-services.md`](./pages/special-medical-services.md),
and [`pages/clinic-days.md`](./pages/clinic-days.md).

```mermaid
erDiagram
    pages ||--o{ department_showcase : "page_id"
    departments ||--o{ department_showcase : "department_id"
    staff ||--o{ department_showcase : "head_staff_id"
    media_assets ||--o{ department_showcase : "cover_media_id"
    departments ||--o{ department_photos : "department_id"
    media_assets ||--o{ department_photos : "media_id"

    pages ||--o{ wards : "page_id"
    departments ||--o{ wards : "department_id"
    staff ||--o{ wards : "in_charge_id"
    wards ||--o{ ward_media : "ward_id"
    media_assets ||--o{ ward_media : "media_id"
    pages ||--o{ mortuary_services : "page_id"
    wards ||--o{ mortuary_services : "ward_id"
    wards ||--o{ ward_bed_status : "ward_id"
    users ||--o{ ward_bed_status : "recorded_by"

    pages ||--o{ opd_facilities : "page_id"
    departments ||--o{ opd_facilities : "department_id"
    departments ||--o{ opd_operating_hours : "department_id"
    departments ||--o{ opd_consultation_rooms : "department_id"
    departments ||--o{ opd_appointments : "department_id"
    opd_consultation_rooms ||--o{ opd_appointments : "room_id"
    staff ||--o{ opd_appointments : "clinician_id"

    pages ||--o{ inpatient_dept_sections : "page_id"
    departments ||--o{ inpatient_dept_sections : "department_id"
    media_assets ||--o{ inpatient_dept_sections : "hero_media_id"
    departments ||--o{ inpatient_admission_enquiries : "department_id"

    pages ||--o{ special_medical_services : "page_id"
    departments ||--o{ special_medical_services : "department_id"
    media_assets ||--o{ special_medical_services : "hero_media_id"
    special_medical_services ||--o{ service_specialists : "service_id"
    staff ||--o{ service_specialists : "staff_id"
    special_medical_services ||--o{ service_equipment : "service_id"
    pages ||--o{ service_equipment : "page_id"
    media_assets ||--o{ service_equipment : "media_id"
    special_medical_services ||--o{ service_enquiries : "service_id"

    pages ||--o{ clinics : "page_id"
    departments ||--o{ clinics : "department_id"
    clinics ||--o{ clinic_schedules : "clinic_id"
    staff ||--o{ clinic_schedules : "clinician_id"
    clinic_schedules ||--o{ clinic_schedule_exceptions : "schedule_id"
    clinic_schedules ||--o{ clinic_bookings : "schedule_id"

    department_showcase {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
        BIGINT head_staff_id FK
        BIGINT cover_media_id FK
    }
    department_photos {
        BIGINT id PK
        BIGINT department_id FK
        BIGINT media_id FK
    }
    wards {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
        BIGINT in_charge_id FK
    }
    ward_media {
        BIGINT id PK
        BIGINT ward_id FK
        BIGINT media_id FK
    }
    mortuary_services {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT ward_id FK
    }
    ward_bed_status {
        BIGINT id PK
        BIGINT ward_id FK
        BIGINT recorded_by FK
    }
    opd_facilities {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
    }
    opd_operating_hours {
        BIGINT id PK
        BIGINT department_id FK
    }
    opd_consultation_rooms {
        BIGINT id PK
        BIGINT department_id FK
    }
    opd_appointments {
        BIGINT id PK
        BIGINT department_id FK
        BIGINT room_id FK
        BIGINT clinician_id FK
    }
    inpatient_dept_sections {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
        BIGINT hero_media_id FK
    }
    inpatient_admission_enquiries {
        BIGINT id PK
        BIGINT department_id FK
    }
    special_medical_services {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
        BIGINT hero_media_id FK
    }
    service_specialists {
        BIGINT id PK
        BIGINT service_id FK
        BIGINT staff_id FK
    }
    service_equipment {
        BIGINT id PK
        BIGINT service_id FK
        BIGINT page_id FK
        BIGINT media_id FK
    }
    service_enquiries {
        BIGINT id PK
        BIGINT service_id FK
    }
    clinics {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
    }
    clinic_schedules {
        BIGINT id PK
        BIGINT clinic_id FK
        BIGINT clinician_id FK
    }
    clinic_schedule_exceptions {
        BIGINT id PK
        BIGINT schedule_id FK
    }
    clinic_bookings {
        BIGINT id PK
        BIGINT schedule_id FK
    }
```

---

## Cluster 7 — Projects, community & sustainability

Defined in [`pages/development-projects.md`](./pages/development-projects.md),
[`pages/upcoming-projects.md`](./pages/upcoming-projects.md),
[`pages/self-sustainability-projects.md`](./pages/self-sustainability-projects.md),
[`pages/community-support.md`](./pages/community-support.md), and
[`pages/smi-community.md`](./pages/smi-community.md).

```mermaid
erDiagram
    pages ||--o{ development_projects : "page_id"
    departments ||--o{ development_projects : "department_id"
    media_assets ||--o{ development_projects : "cover_media_id"
    pages ||--o{ development_strategic_plans : "page_id"
    media_assets ||--o{ development_strategic_plans : "document_media_id"
    development_projects ||--o{ development_project_plan_links : "project_id"
    development_strategic_plans ||--o{ development_project_plan_links : "plan_id"
    development_projects ||--o{ development_project_media : "project_id"
    media_assets ||--o{ development_project_media : "media_id"
    development_projects ||--o{ development_project_metrics : "project_id"

    pages ||--o{ upcoming_projects : "page_id"
    departments ||--o{ upcoming_projects : "department_id"
    pages ||--o{ upcoming_projects : "related_page_id"
    media_assets ||--o{ upcoming_projects : "cover_media_id"
    upcoming_projects ||--o{ upcoming_project_phases : "project_id"
    upcoming_projects ||--o{ upcoming_project_media : "project_id"
    media_assets ||--o{ upcoming_project_media : "media_id"
    upcoming_projects ||--o{ upcoming_project_pledges : "project_id"

    pages ||--o{ sustainability_projects : "page_id"
    media_assets ||--o{ sustainability_projects : "cover_media_id"
    sustainability_projects ||--o{ sustainability_production_records : "project_id"
    sustainability_projects ||--o{ sustainability_project_media : "project_id"
    media_assets ||--o{ sustainability_project_media : "media_id"

    pages ||--o{ community_programs : "page_id"
    departments ||--o{ community_programs : "department_id"
    media_assets ||--o{ community_programs : "cover_media_id"
    community_programs ||--o{ community_outreach_events : "program_id"
    community_programs ||--o{ community_volunteer_signups : "program_id"
    community_programs ||--o{ community_program_media : "program_id"
    media_assets ||--o{ community_program_media : "media_id"

    pages ||--o{ smi_community_profile : "page_id"
    media_assets ||--o{ smi_community_profile : "cover_media_id"
    pages ||--o{ smi_facilities : "page_id"
    media_assets ||--o{ smi_facilities : "cover_media_id"
    pages ||--o{ smi_community_events : "page_id"
    media_assets ||--o{ smi_community_events : "cover_media_id"
    pages ||--o{ smi_vocation_enquiries : "page_id"
    smi_community_events ||--o{ smi_event_media : "event_id"
    media_assets ||--o{ smi_event_media : "media_id"

    development_projects {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
        BIGINT cover_media_id FK
    }
    development_strategic_plans {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT document_media_id FK
    }
    development_project_plan_links {
        BIGINT id PK
        BIGINT project_id FK
        BIGINT plan_id FK
    }
    development_project_media {
        BIGINT id PK
        BIGINT project_id FK
        BIGINT media_id FK
    }
    development_project_metrics {
        BIGINT id PK
        BIGINT project_id FK
    }
    upcoming_projects {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
        BIGINT related_page_id FK
        BIGINT cover_media_id FK
    }
    upcoming_project_phases {
        BIGINT id PK
        BIGINT project_id FK
    }
    upcoming_project_media {
        BIGINT id PK
        BIGINT project_id FK
        BIGINT media_id FK
    }
    upcoming_project_pledges {
        BIGINT id PK
        BIGINT project_id FK
    }
    sustainability_projects {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT cover_media_id FK
    }
    sustainability_production_records {
        BIGINT id PK
        BIGINT project_id FK
    }
    sustainability_project_media {
        BIGINT id PK
        BIGINT project_id FK
        BIGINT media_id FK
    }
    community_programs {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
        BIGINT cover_media_id FK
    }
    community_outreach_events {
        BIGINT id PK
        BIGINT program_id FK
    }
    community_volunteer_signups {
        BIGINT id PK
        BIGINT program_id FK
    }
    community_program_media {
        BIGINT id PK
        BIGINT program_id FK
        BIGINT media_id FK
    }
    smi_community_profile {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT cover_media_id FK
    }
    smi_facilities {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT cover_media_id FK
    }
    smi_community_events {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT cover_media_id FK
    }
    smi_vocation_enquiries {
        BIGINT id PK
        BIGINT page_id FK
    }
    smi_event_media {
        BIGINT id PK
        BIGINT event_id FK
        BIGINT media_id FK
    }
```

---

## Cluster 8 — About, administration & philosophy

Defined in [`pages/about-ollmh-location.md`](./pages/about-ollmh-location.md),
[`pages/administration.md`](./pages/administration.md),
[`pages/philosophy-of-care.md`](./pages/philosophy-of-care.md),
[`pages/hr-capacity-staff.md`](./pages/hr-capacity-staff.md),
[`pages/ollmh-outlook.md`](./pages/ollmh-outlook.md), and
[`pages/contacts.md`](./pages/contacts.md).

```mermaid
erDiagram
    pages ||--o{ about_facts : "page_id"
    pages ||--o{ about_milestones : "page_id"
    media_assets ||--o{ about_milestones : "media_id"
    pages ||--o{ location_info : "page_id"

    pages ||--o{ governance_bodies : "page_id"
    governance_bodies ||--o{ governance_members : "body_id"
    staff ||--o{ governance_members : "staff_id"
    media_assets ||--o{ governance_members : "photo_media_id"

    pages ||--o{ care_statements : "page_id"
    pages ||--o{ care_values : "page_id"

    pages ||--o{ staff_cadres : "page_id"
    pages ||--o{ hr_capacity_stats : "page_id"
    staff_cadres ||--o{ hr_capacity_stats : "cadre_id"
    departments ||--o{ hr_capacity_stats : "department_id"
    pages ||--o{ job_vacancies : "page_id"
    staff_cadres ||--o{ job_vacancies : "cadre_id"
    departments ||--o{ job_vacancies : "department_id"

    pages ||--o{ outlook_albums : "page_id"
    media_assets ||--o{ outlook_albums : "cover_media_id"
    pages ||--o{ outlook_gallery_items : "page_id"
    outlook_albums ||--o{ outlook_gallery_items : "album_id"
    media_assets ||--o{ outlook_gallery_items : "media_id"

    pages ||--o{ contact_channels : "page_id"
    departments ||--o{ contact_channels : "department_id"
    pages ||--o{ contact_submissions : "page_id"
    departments ||--o{ contact_submissions : "department_id"
    users ||--o{ contact_submissions : "handled_by"

    about_facts {
        BIGINT id PK
        BIGINT page_id FK
    }
    about_milestones {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT media_id FK
    }
    location_info {
        BIGINT id PK
        BIGINT page_id FK
    }
    governance_bodies {
        BIGINT id PK
        BIGINT page_id FK
    }
    governance_members {
        BIGINT id PK
        BIGINT body_id FK
        BIGINT staff_id FK
        BIGINT photo_media_id FK
    }
    care_statements {
        BIGINT id PK
        BIGINT page_id FK
    }
    care_values {
        BIGINT id PK
        BIGINT page_id FK
    }
    staff_cadres {
        BIGINT id PK
        BIGINT page_id FK
    }
    hr_capacity_stats {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT cadre_id FK
        BIGINT department_id FK
    }
    job_vacancies {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT cadre_id FK
        BIGINT department_id FK
    }
    outlook_albums {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT cover_media_id FK
    }
    outlook_gallery_items {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT album_id FK
        BIGINT media_id FK
    }
    contact_channels {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
    }
    contact_submissions {
        BIGINT id PK
        BIGINT page_id FK
        BIGINT department_id FK
        BIGINT handled_by FK
    }
```

---

## Cross-cluster overview

This simplified diagram shows how the 8 clusters connect through the shared
`pages`, `media_assets`, `users`, `departments`, and `staff` hub tables. Page
and media detail tables are omitted for clarity — only the "root" table of
each cluster is shown to illustrate the hub-and-spoke topology.

```mermaid
erDiagram
    pages ||--o{ news_articles : "Cluster 3 News"
    pages ||--o{ events : "Cluster 4 Events"
    pages ||--|| nursing_school_profile : "Cluster 5 Nursing"
    pages ||--o{ applications : "Cluster 5 Applications"
    pages ||--o{ wards : "Cluster 6 Wards"
    pages ||--o{ clinics : "Cluster 6 Clinics"
    pages ||--o{ development_projects : "Cluster 7 Projects"
    pages ||--o{ community_programs : "Cluster 7 Community"
    pages ||--o{ about_facts : "Cluster 8 About"
    pages ||--o{ governance_bodies : "Cluster 8 Admin"
    pages ||--o{ contact_channels : "Cluster 8 Contacts"
    pages ||--o{ home_slides : "Cluster 2 Home"

    media_assets }o--o{ news_articles : "hero"
    media_assets }o--o{ events : "hero"
    media_assets }o--o{ nursing_school_profile : "hero"
    media_assets }o--o{ wards : "via ward_media"
    media_assets }o--o{ development_projects : "cover"

    users }o--o{ news_articles : "author"
    users }o--o{ applications : "reviewed_by"
    users }o--o{ contact_submissions : "handled_by"

    departments }o--o{ wards : "department"
    departments }o--o{ clinics : "department"
    departments }o--o{ development_projects : "department"
    departments }o--o{ community_programs : "department"

    staff }o--o{ wards : "in_charge"
    staff }o--o{ governance_members : "member"
    staff }o--o{ opd_appointments : "clinician"

    news_articles ||--o{ home_news_promos : "featured on home"
    nursing_programmes ||--o{ applications : "applied to"
    nursing_intakes ||--o{ applications : "intake"
```

---

## Table inventory

### Shared / platform (7 tables)

| Table | File | FKs |
| --- | --- | --- |
| `pages` | `SCHEMA_CONVENTIONS.md` | `hero_media_id → media_assets` |
| `media_assets` | `SCHEMA_CONVENTIONS.md` | `uploaded_by → users` |
| `page_media` | `SCHEMA_CONVENTIONS.md` | `page_id → pages`, `media_id → media_assets` |
| `users` | `SCHEMA_CONVENTIONS.md` | — |
| `menu_items` | `SCHEMA_CONVENTIONS.md` | `parent_id → menu_items`, `page_id → pages` |
| `departments` | `SCHEMA_CONVENTIONS.md` | `page_id → pages` |
| `staff` | `SCHEMA_CONVENTIONS.md` | `department_id → departments`, `photo_media_id → media_assets` |

### Page-specific (73 tables)

| Cluster | Table | File | FKs |
| --- | --- | --- | --- |
| Home | `home_slides` | `index.md` | `page_id`, `media_id`, `link_page_id` |
| Home | `home_in_focus_items` | `index.md` | `page_id`, `media_id`, `link_page_id` |
| Home | `home_feature_blocks` | `index.md` | `page_id`, `media_id`, `department_id`, `read_more_page_id` |
| Home | `home_news_promos` | `index.md` | `page_id`, `media_id`, `article_id → news_articles` |
| News | `news_articles` | `news/article-template.md` | `page_id`, `category_id`, `author_id`, `hero_media_id` |
| News | `news_categories` | `news/index.md` | `parent_id` (self) |
| News | `news_tags` | `news/index.md` | — |
| News | `news_article_tags` | `news/article-template.md` | `article_id`, `tag_id` |
| News | `news_article_media` | `news/article-template.md` | `article_id`, `media_id` |
| News | `news_article_revisions` | `news/article-template.md` | `article_id`, `editor_id → users` |
| News | `news_comments` | `news/article-template.md` | `article_id`, `parent_id` (self) |
| News | `newsletter_subscribers` | `news/index.md` | — |
| Events | `events` | `events/event-template.md` | `page_id`, `category_id`, `hero_media_id` |
| Events | `event_categories` | `events/index.md` | `parent_id` (self) |
| Events | `event_registrations` | `events/event-template.md` | `event_id` |
| Events | `event_media` | `events/event-template.md` | `event_id`, `media_id` |
| Nursing | `nursing_school_profile` | `about-nursing-school.md` | `page_id`, `hero_media_id` |
| Nursing | `nursing_programmes` | `about-nursing-school.md` | `school_profile_id` |
| Nursing | `nursing_facilities` | `about-nursing-school.md` | `school_profile_id`, `media_id` |
| Nursing | `nursing_intakes` | `about-nursing-school.md` | `programme_id` |
| Applications | `applicants` | `medical-school-application-form.md` | — |
| Applications | `applications` | `medical-school-application-form.md` | `page_id`, `applicant_id`, `programme_id`, `intake_id`, `reviewed_by` |
| Applications | `application_documents` | `medical-school-application-form.md` | `application_id`, `media_id` |
| Applications | `application_form_downloads` | `medical-school-application-form.md` | `page_id`, `media_id` |
| Applications | `application_status_history` | `medical-school-application-form.md` | `application_id`, `changed_by` |
| Applications | `application_referees` | `medical-school-application-form.md` | `application_id` |
| Applications | `application_reviews` | `medical-school-application-form.md` | `application_id`, `reviewer_id` |
| Applications | `application_payments` | `medical-school-application-form.md` | `application_id` |
| Applications | `application_notifications` | `medical-school-application-form.md` | `application_id` |
| Depts/Wards | `department_showcase` | `ollmh-departments.md` | `page_id`, `department_id`, `head_staff_id`, `cover_media_id` |
| Depts/Wards | `department_photos` | `ollmh-departments.md` | `department_id`, `media_id` |
| Depts/Wards | `wards` | `wards.md` | `page_id`, `department_id`, `in_charge_id` |
| Depts/Wards | `ward_media` | `wards.md` | `ward_id`, `media_id` |
| Depts/Wards | `mortuary_services` | `wards.md` | `page_id`, `ward_id` |
| Depts/Wards | `ward_bed_status` | `wards.md` | `ward_id`, `recorded_by` |
| Depts/Wards | `opd_facilities` | `out-patient-dept.md` | `page_id`, `department_id` |
| Depts/Wards | `opd_operating_hours` | `out-patient-dept.md` | `department_id` |
| Depts/Wards | `opd_consultation_rooms` | `out-patient-dept.md` | `department_id` |
| Depts/Wards | `opd_appointments` | `out-patient-dept.md` | `department_id`, `room_id`, `clinician_id` |
| Depts/Wards | `inpatient_dept_sections` | `in-patient-dept.md` | `page_id`, `department_id`, `hero_media_id` |
| Depts/Wards | `inpatient_admission_enquiries` | `in-patient-dept.md` | `department_id` |
| Depts/Wards | `special_medical_services` | `special-medical-services.md` | `page_id`, `department_id`, `hero_media_id` |
| Depts/Wards | `service_specialists` | `special-medical-services.md` | `service_id`, `staff_id` |
| Depts/Wards | `service_equipment` | `special-medical-services.md` | `service_id`, `page_id`, `media_id` |
| Depts/Wards | `service_enquiries` | `special-medical-services.md` | `service_id` |
| Depts/Wards | `clinics` | `clinic-days.md` | `page_id`, `department_id` |
| Depts/Wards | `clinic_schedules` | `clinic-days.md` | `clinic_id`, `clinician_id` |
| Depts/Wards | `clinic_schedule_exceptions` | `clinic-days.md` | `schedule_id` |
| Depts/Wards | `clinic_bookings` | `clinic-days.md` | `schedule_id` |
| Projects | `development_projects` | `development-projects.md` | `page_id`, `department_id`, `cover_media_id` |
| Projects | `development_strategic_plans` | `development-projects.md` | `page_id`, `document_media_id` |
| Projects | `development_project_plan_links` | `development-projects.md` | `project_id`, `plan_id` |
| Projects | `development_project_media` | `development-projects.md` | `project_id`, `media_id` |
| Projects | `development_project_metrics` | `development-projects.md` | `project_id` |
| Projects | `upcoming_projects` | `upcoming-projects.md` | `page_id`, `department_id`, `related_page_id`, `cover_media_id` |
| Projects | `upcoming_project_phases` | `upcoming-projects.md` | `project_id` |
| Projects | `upcoming_project_media` | `upcoming-projects.md` | `project_id`, `media_id` |
| Projects | `upcoming_project_pledges` | `upcoming-projects.md` | `project_id` |
| Projects | `sustainability_projects` | `self-sustainability-projects.md` | `page_id`, `cover_media_id` |
| Projects | `sustainability_production_records` | `self-sustainability-projects.md` | `project_id` |
| Projects | `sustainability_project_media` | `self-sustainability-projects.md` | `project_id`, `media_id` |
| Projects | `community_programs` | `community-support.md` | `page_id`, `department_id`, `cover_media_id` |
| Projects | `community_outreach_events` | `community-support.md` | `program_id` |
| Projects | `community_volunteer_signups` | `community-support.md` | `program_id` |
| Projects | `community_program_media` | `community-support.md` | `program_id`, `media_id` |
| Projects | `smi_community_profile` | `smi-community.md` | `page_id`, `cover_media_id` |
| Projects | `smi_facilities` | `smi-community.md` | `page_id`, `cover_media_id` |
| Projects | `smi_community_events` | `smi-community.md` | `page_id`, `cover_media_id` |
| Projects | `smi_vocation_enquiries` | `smi-community.md` | `page_id` |
| Projects | `smi_event_media` | `smi-community.md` | `event_id`, `media_id` |
| About/Admin | `about_facts` | `about-ollmh-location.md` | `page_id` |
| About/Admin | `about_milestones` | `about-ollmh-location.md` | `page_id`, `media_id` |
| About/Admin | `location_info` | `about-ollmh-location.md` | `page_id` |
| About/Admin | `governance_bodies` | `administration.md` | `page_id` |
| About/Admin | `governance_members` | `administration.md` | `body_id`, `staff_id`, `photo_media_id` |
| About/Admin | `care_statements` | `philosophy-of-care.md` | `page_id` |
| About/Admin | `care_values` | `philosophy-of-care.md` | `page_id` |
| About/Admin | `staff_cadres` | `hr-capacity-staff.md` | `page_id` |
| About/Admin | `hr_capacity_stats` | `hr-capacity-staff.md` | `page_id`, `cadre_id`, `department_id` |
| About/Admin | `job_vacancies` | `hr-capacity-staff.md` | `page_id`, `cadre_id`, `department_id` |
| About/Admin | `outlook_albums` | `ollmh-outlook.md` | `page_id`, `cover_media_id` |
| About/Admin | `outlook_gallery_items` | `ollmh-outlook.md` | `page_id`, `album_id`, `media_id` |
| About/Admin | `contact_channels` | `contacts.md` | `page_id`, `department_id` |
| About/Admin | `contact_submissions` | `contacts.md` | `page_id`, `department_id`, `handled_by` |

**Totals:** 7 shared + 73 page-specific = **80 tables** · **116 foreign keys**.
