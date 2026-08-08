# OLLMH Website Documentation

Analysis and rebuild blueprint for the archived **Our Lady of Lourdes Mwea
Hospital (OLLMH)** website (Wayback Machine snapshot `20220319205345`).

This documentation maps every page reachable from the site's header/footer
navigation, assesses gaps, and designs a MySQL schema to move the site from a
static archive to a **fully dynamic, database-driven application**.

## Contents

- **[`SCHEMA_CONVENTIONS.md`](./SCHEMA_CONVENTIONS.md)** — shared, platform-wide
  tables (`pages`, `media_assets`, `page_media`, `users`, `menu_items`,
  `departments`, `staff`) and conventions that every per-page schema references
  via foreign keys. **Read this first** — page files define only their own
  tables and FK into these.
- **[`header-footer-links.md`](./header-footer-links.md)** — the extracted
  inventory of every hyperlink in the header navigation and footer.
- **[`pages/`](./pages/)** — one standalone documentation file per page, each
  with: **1. Current State Mapping**, **2. Gap Analysis & Feature
  Enhancements**, **3. Database Schema Design**.

## Page index

The **Content status** column flags how faithful the archived page is to its
title — a key input for the rebuild.

| Page | Doc | Content status |
| --- | --- | --- |
| Home | [index.md](./pages/index.md) | Real content (slideshow, In Focus, tabs, news scroller, dept columns) |
| Location | [about-ollmh-location.md](./pages/about-ollmh-location.md) | Real content |
| Admin menu (Administration) | [administration.md](./pages/administration.md) | Real content |
| Our Philosophy Of Care | [philosophy-of-care.md](./pages/philosophy-of-care.md) | Real content |
| HR-Capacity (Staff) | [hr-capacity-staff.md](./pages/hr-capacity-staff.md) | Real content |
| Hospital Development | [development-projects.md](./pages/development-projects.md) | Real content |
| Self Sustainability Projects | [self-sustainability-projects.md](./pages/self-sustainability-projects.md) | Real content |
| Community Support | [community-support.md](./pages/community-support.md) | Real content |
| Upcoming Projects | [upcoming-projects.md](./pages/upcoming-projects.md) | Real content (text only) |
| Out Patient Department | [out-patient-dept.md](./pages/out-patient-dept.md) | Real content |
| Wards | [wards.md](./pages/wards.md) | Real content |
| Ollmh Outlook | [ollmh-outlook.md](./pages/ollmh-outlook.md) | Real content (photo gallery) |
| Ollmh Departments | [ollmh-departments.md](./pages/ollmh-departments.md) | Real content (photo grid) |
| S.M.I Community | [smi-community.md](./pages/smi-community.md) | Real content |
| Contacts | [contacts.md](./pages/contacts.md) | ⚠️ No form/map; email JS-cloaked |
| Special Medical Services | [special-medical-services.md](./pages/special-medical-services.md) | ⚠️ Mislabeled — in-body heading is "Inpatient Department (Nursing Application)" |
| New & Events | [news-events.md](./pages/news-events.md) | ⚠️ Mislabeled — a nursing-school advert, not a news feed |
| Medical School Application Form | [medical-school-application-form.md](./pages/medical-school-application-form.md) | ⚠️ Not a form — only a PDF download link |
| About The Nursing School | [about-nursing-school.md](./pages/about-nursing-school.md) | ❌ Placeholder stub (not archived) |
| Clinic Days | [clinic-days.md](./pages/clinic-days.md) | ❌ Placeholder stub (not archived) |
| In Patient Dept | [in-patient-dept.md](./pages/in-patient-dept.md) | ❌ Placeholder stub (not archived) |

**Legend:** Real content = archived page has substantive content · ⚠️ =
content present but title/functionality mismatch to address in rebuild · ❌ =
no real content captured; page must be built from scratch.

## How the schema fits together

Every page-specific table foreign-keys into `pages(id)` and, where relevant,
into other shared tables (`media_assets`, `departments`, `staff`, `users`).
Cross-page integrations are noted in the individual files — for example the
[application form](./pages/medical-school-application-form.md) links applicants
to nursing programmes defined in
[About The Nursing School](./pages/about-nursing-school.md), and both the
[contacts](./pages/contacts.md) and department pages route through the shared
`departments` catalogue. See each file's **Relationships** subsection for
details.
