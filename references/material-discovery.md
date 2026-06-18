# Material Discovery

Use this file when the working folder contains many reports, templates, scans,
teacher files, or senior examples. This skill is not a vector database or RAG
service. It uses static, auditable reference files plus user-provided local
materials selected at runtime.

## Source Priority

| Priority | Source | How to Use |
|---|---|---|
| 1 | Current official cover/template PDFs | Control cover fields, section names, point values, and required appendix style |
| 2 | Current teacher formula sheet, data table, PPT, or DOCX | Control this year's formulas, data fields, and special requirements |
| 3 | `references/experiments/*.md` | Provide experiment aliases, required tables, formulas, and error-analysis checklist |
| 4 | Student's scanned completed data sheet | Authoritative source for raw data after user confirmation |
| 5 | Student's existing `.tex` report | Reuse style and macros only after checking against current requirements |
| 6 | Senior/reference reports | Style and completeness examples only; never override current templates |
| 7 | Textbook or lab manual PDF | Use for theory and formulas, but avoid committing copyrighted source material |

## Local Folder Patterns

The user's local collection may include:

- `大物实验报告/` - current student's generated PDFs, `.tex`, scans, plots, and data-entry files.
- `大物实验三人行/17级.../公式表格/` - historical prelab/postlab templates and data tables.
- `大物实验三人行/18级.../Physics Experiments I/` - Physics Experiments I reports, PPTs, and manual.
- `大物实验三人行/18级.../Physics Experiments II/` - Physics Experiments II reports, schedules, lecture PDFs, templates, and PPTs.
- `private_assets/` - optional local-only textbook/PPT/source files; keep gitignored.

## Discovery Steps

1. Identify the report type and full experiment title first.
2. Search for current-year templates and teacher materials before senior reports.
3. Match by experiment title and aliases, not just lab number.
4. If multiple materials disagree, prefer newer and more specific course files.
5. If the scanned data is unclear, stop at a draft transcription and ask for confirmation.
6. Keep original filenames in notes, but use short ASCII names for generated figures and scripts.

## Copyright Boundary

Do not commit full textbooks, teacher PPTs, senior reports, or a student's private
data sheets into the public repository unless there is explicit permission.
Public references should contain structured summaries: titles, aliases, required
table fields, formula names, calculation steps, and common mistakes.
