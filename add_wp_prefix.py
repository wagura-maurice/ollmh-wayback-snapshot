#!/usr/bin/env python3
"""
Add wp_ prefix to all database table names across all documentation files.
Context-aware: only replaces table names in SQL, backtick, Mermaid, and
table.column notation contexts — never in plain English prose.
"""
import re
import os
import glob

# All 80 table names
TABLES = [
    # Shared (7)
    "pages", "media_assets", "page_media", "users", "menu_items", "departments", "staff",
    # Home (4)
    "home_slides", "home_in_focus_items", "home_feature_blocks", "home_news_promos",
    # News (8)
    "news_articles", "news_categories", "news_tags", "news_article_tags",
    "news_article_media", "news_article_revisions", "news_comments",
    "newsletter_subscribers",
    # Events (4)
    "events", "event_categories", "event_registrations", "event_media",
    # Nursing (4)
    "nursing_school_profile", "nursing_programmes", "nursing_facilities", "nursing_intakes",
    # Applications (9)
    "applicants", "applications", "application_documents", "application_form_downloads",
    "application_status_history", "application_referees", "application_reviews",
    "application_payments", "application_notifications",
    # Departments/Wards/Clinical (20)
    "department_showcase", "department_photos", "wards", "ward_media", "mortuary_services",
    "ward_bed_status", "opd_facilities", "opd_operating_hours", "opd_consultation_rooms",
    "opd_appointments", "inpatient_dept_sections", "inpatient_admission_enquiries",
    "special_medical_services", "service_specialists", "service_equipment", "service_enquiries",
    "clinics", "clinic_schedules", "clinic_schedule_exceptions", "clinic_bookings",
    # Projects/Community (21)
    "development_projects", "development_strategic_plans", "development_project_plan_links",
    "development_project_media", "development_project_metrics",
    "upcoming_projects", "upcoming_project_phases", "upcoming_project_media", "upcoming_project_pledges",
    "sustainability_projects", "sustainability_production_records", "sustainability_project_media",
    "community_programs", "community_outreach_events", "community_volunteer_signups", "community_program_media",
    "smi_community_profile", "smi_facilities", "smi_community_events", "smi_vocation_enquiries", "smi_event_media",
    # About/Admin (14)
    "about_facts", "about_milestones", "location_info",
    "governance_bodies", "governance_members",
    "care_statements", "care_values",
    "staff_cadres", "hr_capacity_stats", "job_vacancies",
    "outlook_albums", "outlook_gallery_items",
    "contact_channels", "contact_submissions",
]

# Sort by length, longest first — prevents partial-match issues
TABLES.sort(key=len, reverse=True)

def prefix_file(text):
    for table in TABLES:
        wp = f"wp_{table}"
        esc = re.escape(table)

        # 1. CREATE TABLE <name>
        text = re.sub(rf'CREATE TABLE {esc}\b', f'CREATE TABLE {wp}', text)

        # 2. REFERENCES <name>
        text = re.sub(rf'REFERENCES {esc}\b', f'REFERENCES {wp}', text)

        # 3. `<name>` (exact backtick-quoted)
        text = text.replace(f'`{table}`', f'`{wp}`')

        # 4. `<name>.` (backtick + table + dot, for `table.column` starts)
        text = text.replace(f'`{table}.`', f'`{wp}.`')

        # 5. → <name> (arrow notation in prose/backticks — handles both
        #    `→ <name>` and `→ <name>.<col>`)
        text = re.sub(rf'→ {esc}\b', f'→ {wp}', text)

        # 6. <name>.<column> in prose (table.column notation)
        #    Positive lookbehind: only match when preceded by whitespace, backtick,
        #    or start of string — prevents false positives in URL paths like
        #    `/wards.html` or `hr-capacity-staff.html`
        text = re.sub(rf'(?<=[\s`^]){esc}\.(\w)', f'{wp}.\\1', text)

        # 7. Mermaid entity block: <name> {  (on its own line, indented)
        text = re.sub(rf'(\n\s*){esc}(\s+\{{)', rf'\1{wp}\2', text)

        # 8. Mermaid left side: <name> ||--
        text = re.sub(rf'(\n\s*){esc}(\s+\|\|--)', rf'\1{wp}\2', text)

        # 9. Mermaid left side: <name> }o--
        text = re.sub(rf'(\n\s*){esc}(\s+\}}o--)', rf'\1{wp}\2', text)

        # 10. Mermaid right side: --o{ <name> (space or colon after)
        text = re.sub(rf'(--o\{{\s+){esc}(\s)', f'\\1{wp}\\2', text)

        # 11. Mermaid right side: --|| <name> (space or colon after)
        text = re.sub(rf'(--\|\|\s+){esc}(\s)', f'\\1{wp}\\2', text)

        # 12. Mermaid right side: --o| <name> (space or colon after)
        text = re.sub(rf'(--o\|\s+){esc}(\s)', f'\\1{wp}\\2', text)

        # 13. Markdown table cell: | <name> |  (standalone cell)
        text = re.sub(rf'\| {esc} \|', f'| {wp} |', text)

        # 14. Markdown table cell: | <name> `  (cell starting with table name + space + backtick for file ref)
        text = re.sub(rf'\| {esc}(\s+`)', f'| {wp}\\1', text)

    return text


def main():
    docs_dir = "/root/Projects/ollmh-wayback-snapshot/docs"
    files = []
    files.extend(glob.glob(os.path.join(docs_dir, "*.md")))
    files.extend(glob.glob(os.path.join(docs_dir, "pages", "*.md")))
    files.extend(glob.glob(os.path.join(docs_dir, "pages", "news", "*.md")))
    files.extend(glob.glob(os.path.join(docs_dir, "pages", "events", "*.md")))

    total_changes = 0
    for filepath in sorted(files):
        with open(filepath, 'r') as f:
            original = f.read()
        modified = prefix_file(original)
        if modified != original:
            with open(filepath, 'w') as f:
                f.write(modified)
            # Count rough changes
            changes = sum(1 for a, b in zip(original.split('\n'), modified.split('\n')) if a != b)
            total_changes += changes
            print(f"  Modified: {os.path.relpath(filepath, docs_dir)} ({changes} lines changed)")
        else:
            print(f"  Unchanged: {os.path.relpath(filepath, docs_dir)}")

    print(f"\nTotal: {total_changes} lines changed across {len(files)} files")


if __name__ == '__main__':
    main()
