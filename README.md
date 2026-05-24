# Physics Lab Report — Claude Code Skill

Generate UESTC Physics Experiments I/II lab reports (大物实验报告) using XeLaTeX and LaTeX. Includes both **prelab** (预习报告) and **postlab** (实验报告) templates with cover-page insertion, score-box sectioning, data-table formatting, uncertainty propagation, and scanned-data appendix.

## Preview

| Prelab | Postlab |
|--------|---------|
| Cover PDF → Overlay with student info + score box → Enumerated answers | Cover PDF → Abstract → Calculations & Data Tables → Conclusions → Postlab Q&A → Appendix with scanned data sheets |
| "Physics Lab 2026" watermark | "Physics Labs 2026" watermark |

## Prerequisites

- **XeLaTeX** (not pdfLaTeX) — required for `fontspec` / Times New Roman / Calibri support
- LaTeX packages: `pdfpages`, `fontspec`, `newtxmath`, `amsmath`, `tikz`, `eso-pic`, `fancyhdr`, `enumitem`, `setspace`, `booktabs`, `caption`
- Python 3 with `pypdf` and `matplotlib` (optional, for data extraction and figure generation)
- The official UESTC cover template PDFs (`01-Template for Prelab work-2026*.pdf` and `02-Template for lab report-2026*.pdf`)

### macOS Font Notes

The templates use **Arial** as a fallback for Calibri. Install optional fonts for exact matching:

```bash
# If you have Microsoft Office installed, Calibri is already available.
# Otherwise, Arial (bundled with macOS) works fine.
```

Windows users with Microsoft Office will have Calibri natively — no changes needed.

## Installation

```bash
# Clone into your Claude Code skills directory
mkdir -p ~/.claude/skills
git clone https://github.com/YOUR_USERNAME/physics-lab-report.git ~/.claude/skills/physics-lab-report
```

Or copy the `SKILL.md` and `templates/` folder into any directory scanned by Claude Code.

## Quick Start

### 1. Create a Prelab Report

```bash
cp ~/.claude/skills/physics-lab-report/templates/prelab_template.tex ./labN_pre.tex
```

Edit `labN_pre.tex`:
- Fill in your `\StudentNumber`, `\StudentEmail`, `\ReportDate`
- Set `\CoverPDF` to your cover template filename
- Write your answers inside `\PrelabAnswerBody`

```bash
xelatex -interaction=nonstopmode labN_pre.tex
xelatex -interaction=nonstopmode labN_pre.tex
```

### 2. Create a Postlab Report

```bash
cp ~/.claude/skills/physics-lab-report/templates/postlab_template.tex ./labN_post.tex
```

Edit `labN_post.tex`:
- Fill in your info
- Set `\CoverPDF` and `\DataPDF` filenames
- Fill all four sections (Abstract, Calculations, Conclusions, Questions)
- Insert your scanned data sheet as `\DataPDF`

```bash
xelatex -interaction=nonstopmode labN_post.tex
xelatex -interaction=nonstopmode labN_post.tex
```

### 3. Or Just Ask Claude

With the skill installed, you can say:

> "Generate the prelab for lab 5 (Polarized Light), here is my data sheet PDF"

Claude will read the skill, use the templates, and produce the `.tex` file for you.

## File Structure

```
physics-lab-report/
├── SKILL.md                          # Skill reference (loaded by Claude Code)
├── README.md                         # This file
├── LICENSE                           # MIT
└── templates/
    ├── prelab_template.tex           # Prelab LaTeX template
    └── postlab_template.tex          # Postlab LaTeX template
```

## Key Features

- **Real data only** — every value must trace to a scanned data sheet or instrument specification
- **Cover page via `\includepdf`** — never drawn in LaTeX, always inserted from the official template PDF
- **Score boxes on every section** — matches the instructor's grading rubric format
- **Uncertainty propagation** — Type A + Type B with rectangular distribution, combined into final result
- **Scanned data sheet appendix** — the original handwritten data must appear at the end
- **Two font strategies** — clean all-Times New Roman, or Calibri tables to match the Word template exactly
- **Standard and compact spacing** — choose based on report length

## Adapting for Your School

This skill was built from UESTC Physics Experiments I templates, but the patterns apply broadly:

1. **Different cover PDF**: Change `\CoverPDF` to your school's template
2. **Different header info**: Edit the `\PrelabPageForeground` overlay coordinates
3. **Different section names/personas**: Edit `\labsection` calls in the postlab template
4. **Different watermark text**: Search for "Physics Lab" in the templates and replace

The core infrastructure (score boxes, data tables, uncertainty propagation, watermark, appendix) is reusable across any physics lab course that uses LaTeX.

## FAQ

**Q: Why XeLaTeX instead of pdfLaTeX?**
A: The templates use `fontspec` for Times New Roman/Calibri font matching. pdfLaTeX cannot load system fonts this way. The `iftex` package provides a fallback warning if you accidentally use pdfLaTeX.

**Q: Calibri renders as Arial on my Mac. Is that OK?**
A: Yes. The templates default to Arial as a Calibri substitute on macOS. The visual difference is negligible. If you have Calibri installed (e.g., via Microsoft Office), it will use Calibri automatically.

**Q: The prelab overlay looks misaligned. How do I fix it?**
A: Don't change `\setlength{\unitlength}{1pt}` or the geometry settings. If you modified the cover PDF template, the overlay coordinates in `\PrelabPageForeground` may need adjustment — each coordinate is in absolute points from the lower-left corner.

**Q: Can I use Overleaf?**
A: Yes, but you must switch the compiler to XeLaTeX (Menu → Compiler → XeLaTeX). Upload the cover template PDFs alongside your `.tex` file.

## License

MIT — see [LICENSE](LICENSE).

## Credits

Created by [岳东翰 (Yue Donghan)](https://github.com/YOUR_USERNAME) based on 5 labs of UESTC Physics Experiments I (2026 Spring), with iterative refinements across prelab and postlab reports. Templates capture patterns evolved over a full semester of submissions.
