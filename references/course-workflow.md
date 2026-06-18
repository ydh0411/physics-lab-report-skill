# Course Workflow

Use this file for the semester-level workflow: first-time setup, regular report
generation, updates, and audits.

## First-Time Setup

1. Save official prelab and postlab cover PDFs locally.
2. Copy `config/student_profile.example.yaml` to `config/student_profile.yaml`.
3. Copy `config/naming.example.yaml` to `config/naming.yaml`.
4. Copy `config/template_fields.example.yaml` to `config/template_fields.yaml`.
5. Confirm the course version, teacher, TA, and official PDF naming rule.
6. Keep private templates, textbooks, and teacher materials in `private_assets/`
   or the report working folder, not in the public repo.

## Regular Generation

Required inputs:

- Report type: prelab, postlab, short report, or long report.
- Full experiment title.
- Lab number or submission label for cover and filename only.
- Experiment date and/or submission date.
- Manually entered raw data, or a scanned data draft confirmed by the user.
- Teacher formula/data-processing template when it differs from the reference.
- Completed scanned data sheet when the appendix requires it.

Process:

1. Select the experiment reference by title/alias.
2. Load current config and official templates.
3. Prepare data-entry table if raw data is missing.
4. Confirm all extracted or manually typed data before calculation.
5. Generate a report copy from the golden template.
6. Compile with XeLaTeX and return the PDF as the primary deliverable.

## Update Mode

Use update mode when stable information changes:

- New official cover template.
- New instructor, TA, class, or email.
- New naming rule.
- New course version.
- New teacher formula sheet.
- New experiment reference card.

Update config or references; do not edit the golden LaTeX templates unless the
change is explicitly about template maintenance.

## Audit Mode

Use audit mode to check a finished report:

1. Identify report type, submission label, and actual experiment title.
2. Read current official template first.
3. Read the experiment reference and current teacher materials.
4. Cross-check raw data, formulas, units, significant figures, and appendix scans.
5. Recompile in a clean folder when possible.
6. Report issues by severity: data/fabrication risk, formula mismatch, template
   mismatch, compile failure, then style or formatting concerns.
