---
name: physics-lab-report
description: Use when generating, auditing, revising, or compiling UESTC Glasgow College Physics Experiments I/II lab reports, prelab预习报告, postlab实验报告, short/long lab reports, XeLaTeX templates, data tables, uncertainty calculations, scanned-data appendices, or 大物实验报告.
---

# UESTC Physics Lab Report

## Overview

Generate and audit UESTC Glasgow College physics experiment reports with the
existing XeLaTeX templates. Use this skill for prelabs, postlabs, short reports,
long reports, report audits, data-table setup, uncertainty calculation, and
PDF-first delivery.

This is a static, auditable skill knowledge base. It is not a RAG service, vector
database, or automatic textbook ingestion system. Load only the reference files
needed for the current experiment and keep private course materials outside the
public repository.

## Golden Template Rule

The files below are hard-won golden templates:

- `templates/prelab_template.tex`
- `templates/postlab_template.tex`

Do not rewrite, reformat, simplify, or "clean up" their settings unless the user
explicitly asks for template maintenance. They encode the official cover
insertion, absolute prelab overlays, score boxes, watermark wording, fonts,
spacing, and appendix behavior.

When producing a report, copy or adapt from these templates into a working
report file. Leave the committed templates unchanged.

## Core Principles

1. Use the full experiment title as the primary key. Lab numbers change by year.
2. Use current official templates and teacher materials before old examples.
3. Use real data only. Never invent raw data, questions, signatures, or formulas.
4. Prefer manual raw-data input. OCR or visual extraction is only a draft until
   the user confirms every value.
5. Treat senior reports as style and completeness references only. The goal is
   to produce a better, more current, more traceable report than the references.
6. Return the final PDF as the main deliverable when local XeLaTeX is available.
7. Keep generated plots, scans, and scripts inside the report folder with
   relative paths.

## Reference Routing

Read these files only when they apply:

| Need | Read |
|---|---|
| First-time setup, update mode, audit mode | `references/course-workflow.md` |
| Finding local templates, scans, reports, PPTs, and senior examples | `references/material-discovery.md` |
| Significant figures, uncertainty, regression, units | `references/numerical-rules.md` |
| Figures, scanned appendix, XeLaTeX/PDF workflow | `references/figures-and-compilation.md` |
| Experiment title lookup | `references/experiment-index.md` |
| Physics Experiments II lookup | `references/experiments/physics-experiments-ii-index.md` |
| Specific experiment formulas/tables | Matching `references/experiments/*.md` |

## Work Modes

### First-Time Setup

Use once per semester or course version:

1. Save official prelab and postlab cover PDFs.
2. Copy `config/student_profile.example.yaml` to `config/student_profile.yaml`.
3. Copy `config/naming.example.yaml` to `config/naming.yaml`.
4. Copy `config/template_fields.example.yaml` to `config/template_fields.yaml`.
5. Confirm stable fields: name, student ID, email, college, major, class,
   instructor, and teaching assistant.
6. Confirm PDF naming rules and course version.

Private filled config files and private assets are gitignored.

### Regular Generation

For each report, collect:

1. Report type: prelab, postlab, short report, or long report.
2. Full experiment title.
3. Lab number/submission label for cover and filename only.
4. Date fields.
5. Manually entered raw data, or a scan transcription confirmed by the user.
6. Teacher formula/data-processing sheet when it differs from the reference.
7. Completed scanned data sheet for appendix when required.

Then:

1. Select the experiment reference by title/alias.
2. Prepare or confirm the data table before calculations.
3. Generate the report `.tex` from the golden template.
4. Compile with XeLaTeX.
5. Rename the PDF using `config/naming.yaml` when available.

### Update Mode

Use when stable material changes:

- cover template PDFs
- student profile
- instructor or TA
- output naming rule
- course/textbook version
- teacher formula template
- experiment reference card

Do not edit golden templates unless the update is specifically about template
maintenance.

### Audit Mode

Use this to check a finished report or this skill:

1. Identify report type, submission label, and actual title.
2. Read the current official template first.
3. Read the matching experiment reference and current teacher materials.
4. Check raw-data traceability, formulas, units, significant figures, final
   result, questions, cover, watermark, and appendix scans.
5. Compile in a clean temporary folder when possible.
6. Report current-template mismatches before style suggestions.

## Report Types At A Glance

| | Prelab | Postlab |
|---|---|---|
| Cover PDF | `01-Template for Prelab work-2026*.pdf` | `02-Template for lab report-2026*.pdf` |
| Cover insertion | `\includepdf` | `\includepdf` |
| Page style | `empty` | `fancy`, centered page numbers |
| Watermark | `Physics Lab 2026` | `Physics Labs 2026` |
| Main sections | `Answers to Questions (20 points)` | Abstract, Calculations/Results/Comments, Conclusions, Questions |
| Data appendix | Usually not needed | attach completed scanned data sheet when required |
| Identity | overlay on answer pages | usually contained in filled cover PDF |

Physics Experiments II may use prelab, short lab report, or long lab report
formats. Always inspect the current cover/template before assuming section
names or point values.

## Title-Based Experiment Mapping

Known Physics Experiments I current mapping:

| Submission label | Actual experiment |
|---|---|
| lab1 | Measurement of Resistance by Ammeter-Voltmeter Method |
| lab2 | The Oscilloscope |
| lab3 | Newton's Rings |
| lab4 | Young's Modulus of Wire by Elongating |
| lab5 | Polarized Light |

Physics Experiments II historical labels conflict across years. Use
`references/experiments/physics-experiments-ii-index.md` and ask the user to
confirm the full title when labels disagree.

## Data Handling

Manual input is the default. If the user uploads scans:

1. Try direct text extraction when the PDF is text-based.
2. Render scanned pages for visual inspection when extraction is empty.
3. Transcribe conservatively.
4. Show the table to the user for confirmation.
5. Do not calculate until the user confirms unclear values.

If raw data is missing, generate only a skeleton report or blank data-entry
table. Do not generate a final report.

## Formula Sources

Use formulas in this order:

1. Current teacher formula/data-processing sheet.
2. Matching experiment reference card.
3. Current lab manual/textbook.
4. Senior reports as examples only.

If a teacher-specific formula sheet is missing, use the reference card only when
it covers the experiment and warn that current teacher details may differ.

## LaTeX Patterns To Preserve

Cover insertion:

```latex
\usepackage{pdfpages}
\includepdf[pages=1,pagecommand={\thispagestyle{empty}}]{\CoverPDF}
\setcounter{page}{1}
```

Postlab section headings:

```latex
\labsection{Calculations, Results, and Comments}{(Calculations, data tables and figures; 15 points)}
```

Data table pattern:

```latex
\datatable{DATA TABLE X-X}{(Purpose: ...)}
\begin{table}[H]
\centering
\small
\renewcommand{\arraystretch}{1.15}
\setlength{\tabcolsep}{3pt}
{\tablefont
\begin{tabular}{|...|}
\hline
... real data only ...
\hline
\end{tabular}
}
\caption*{Unit: ... $\Delta_{\mathrm{instr.}}=...$, $\Delta_{\mathrm{read}}=...$}
\end{table}
```

Scanned appendix:

```latex
\clearpage
\appendixhead
\begin{figure}[H]
\centering
\includegraphics[page=1,width=0.90\textwidth]{\DataPDF}
\caption*{Scanned data sheet page 1}
\end{figure}
```

## Compilation

Use XeLaTeX:

```bash
bash scripts/build_report.sh file.tex "final_submission_name.pdf"
```

The script compiles twice, cleans auxiliary files, and optionally renames the
PDF. If XeLaTeX is unavailable, produce an Overleaf-ready project and say that
local compilation was not run.

## When Materials Are Missing

| Missing material | Behavior |
|---|---|
| Cover template PDF | Generate `.tex` draft only and ask for the official cover |
| Raw data | Generate skeleton or data-entry table only |
| Formula template | Use reference card if available and warn about teacher-specific gaps |
| Questions | Leave placeholders or ask user; do not invent questions |
| Unclear scan | Draft transcription with caveats and ask for confirmation |
| Teacher signature | Attach completed signed scan; do not auto-place signatures |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using lab number as the experiment key | Match by full title and aliases |
| Editing golden templates casually | Copy into a report file; leave templates untouched |
| Copying senior-report formulas blindly | Check current teacher template first |
| Relying on OCR for handwritten numbers | Ask the user to confirm every value |
| Fabricating missing data/questions | Stop and request the missing material |
| Compiling with pdfLaTeX | Use XeLaTeX |
| Referencing Desktop paths in LaTeX | Use relative paths inside the report folder |
| Forgetting scanned-data appendix | Attach completed data sheet when required |
| Treating old point values as current | Current cover/template wins |

## Finish Checklist

Before saying a report is ready:

- [ ] Full experiment title identified.
- [ ] Current template/cover rules checked.
- [ ] Matching experiment reference loaded.
- [ ] Raw data confirmed by the user or manually provided.
- [ ] Every reported number traces to a source.
- [ ] Units and significant figures checked.
- [ ] Uncertainty or regression handled according to current materials.
- [ ] Golden templates were not modified.
- [ ] Figures and scans use relative paths.
- [ ] XeLaTeX compilation was run, or an Overleaf-ready fallback was clearly stated.
- [ ] Final PDF name follows `config/naming.yaml` when available.
