---
name: physics-lab-report
description: Use when generating UESTC Physics Experiments I/II lab reports (prelab预习报告 or postlab实验报告) with LaTeX. Covers cover-page insertion via includepdf, score-box sectioning, data-table formatting, uncertainty propagation, scanned-data appendix, and the prelab overlay technique. Also use when the user says 大物实验报告, 物理实验报告, or asks to create a physics lab report.
---

# UESTC Physics Lab Report Generator

## Overview

Generate prelab (预习报告) and postlab (实验报告) for UESTC Physics Experiments I/II using XeLaTeX. Two distinct templates share core infrastructure: cover page via `\includepdf`, score boxes on every section, diagonal watermark, and real-data tables. The templates are designed for any UESTC student — fill in your personal info via `\newcommand` variables.

## Report Types at a Glance

| | Prelab | Postlab |
|---|---|---|
| Cover PDF | `01-Template for Prelab work-2026*.pdf` | `02-Template for lab report-2026*.pdf` |
| Cover title | "Prelab Report" | "Lab Report" |
| Page style | `empty` | `fancy`, centered page numbers |
| Watermark | "Physics Lab 2026" (singular) | "Physics Labs 2026" (plural) |
| Sections | One: "Answers to Questions (20 points)" with overlay score box | Four: Abstract (5), Calculations/Results/Comments (15), Conclusions (10), Questions (10) |
| Multi-page | Repeat background + foreground per page; continue `enumi` counter | Natural text flow |
| Answer format | `(\arabic*)` enumeration, no left margin | `\item \textbf{Title}` with full paragraphs |
| Header on page 2+ | Absolute-position overlay with student info + score box | None (info is on cover only) |

## Compilation

**Must use XeLaTeX** (not pdfLaTeX). Two passes required. Work in a single directory containing all `.tex`, cover PDFs, data PDFs, and figure PDFs.

```bash
xelatex -interaction=nonstopmode file.tex
xelatex -interaction=nonstopmode file.tex
```

## Personal Info Variables

Both templates use these `\newcommand` variables at the top — change them for each student:

```latex
\newcommand{\StudentNumber}{2025190907024}
\newcommand{\StudentEmail}{2025190907024@std.uestc.edu.cn}
\newcommand{\ReportDate}{2026.X.X}        % dots format for overlay
\newcommand{\CoverPDF}{01-Template for Prelab work-2026.pdf}
\newcommand{\DataPDF}{scanned-data.pdf}
```

The cover page date (filled in the template PDF itself) may use `/` format (e.g., `2026/5/12`). The overlay date on prelab page 2 uses `.` format (e.g., `2026.5.12`). These can differ by a day (submission date vs. writing date).

## Core Principles

### 1. Real Data Only

All numbers must trace to scanned data sheets, instrument specs, or textbook values. Extract data from PDFs with Python/pypdf. When data is unclear, transcribe manually — never fabricate.

### 2. Cover via includepdf

```latex
\usepackage{pdfpages}
\includepdf[pages=1,pagecommand={\thispagestyle{empty}}]{\CoverPDF}
\setcounter{page}{1}
```

Never draw the cover in LaTeX.

### 3. Score Boxes

Postlab: `\labsection{Title}{(points)}` renders a left score box + heading.
Prelab: score box drawn in foreground overlay with `\rule` primitives.

### 4. Data Table Format

```latex
\datatable{DATA TABLE X-X}{(Purpose: ...)}
\begin{table}[H]
\centering
\small  % or \footnotesize or \scriptsize
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

### 5. Uncertainty Propagation

Every postlab must show: Type A (from repeated measurements), Type B (instrument + reading error, rectangular distribution: divide by √3), combined propagation, final result as `\boxed{value ± uncertainty unit}`.

### 6. Appendix with Scanned Originals

```latex
\clearpage
\appendixhead
\begin{figure}[H]
\centering
\includegraphics[page=1,width=0.90\textwidth]{\DataPDF}
\caption*{Scanned data sheet page 1}
\end{figure}
```

Multi-page: repeat `figure[H]` per page. Some reports annotate with `Scanned data sheet: filename.pdf`.

## Font Strategies

Two approaches evolved across reports. Both require XeLaTeX.

### Strategy A: All Times New Roman (clean, uniform)

Used in lab5 (polarized light) postlab. Best for most reports.

```latex
\usepackage{fontspec}
\setmainfont{Times New Roman}
\setsansfont{Times New Roman}
\setmonofont{Courier New}
\usepackage{newtxmath}
\newfontfamily\tablefont{Times New Roman}
\newfontfamily\titlefont{Times New Roman}
\newfontfamily\watermarkfont{Times New Roman}
```

### Strategy B: Calibri tables (matches instructor template exactly)

Used in lab4 (Young's modulus) postlab. Tables match the original Word template font. On macOS, fall back to Arial since Calibri may not be installed.

```latex
\IfFontExistsTF{Calibri}{\newfontfamily\tablefont{Calibri}}{\newfontfamily\tablefont{Arial}}
\IfFontExistsTF{Calibri Light}{\newfontfamily\watermarkfont{Calibri Light}}{\newfontfamily\watermarkfont{Arial}}
```

### Prelab Fonts

```latex
\newfontfamily\calibrifont{Arial}      % Calibri fallback for macOS
\newfontfamily\calibrilight{Arial}
```

For prelab header info, font size evolved from `\fontsize{10pt}{10pt}` to `\fontsize{8.5pt}{8.5pt}` for better fit.

## Spacing Settings

| Setting | Standard (lab1, lab5) | Compact (lab4, long reports) |
|---|---|---|
| `\setstretch` | 1.04 | 1.02 |
| `\parskip` | 1pt | 0.5pt |
| Display skips | 5pt/4pt (above/below) | 4pt/3pt |
| `\captionsetup{skip}` | 4pt | 2pt |
| `\labsection` vspace before | 0.5em | 0.35em |
| `\labsection` vspace after | 0.55em | 0.4em |
| Extra float spacing | — | `\textfloatsep=6pt`, `\floatsep=5pt`, `\intextsep=5pt` |

Standard geometry for all reports:
```latex
\usepackage[a4paper,top=1in,bottom=1in,left=1.25in,right=1.25in,headsep=10pt]{geometry}
\setlength{\parindent}{2em}
```

## Prelab Template

See `templates/prelab_template.tex`. Page structure:

1. **Page 1**: Cover PDF inserted via `\includepdf`
2. **Page 2+**: Background watermark + foreground overlay (student info, score box, section title, page number)

### Two Structural Approaches

**Approach A: `\PrelabAnswerBody` command** — All answers in one `\newcommand`. Best for 1-2 page prelabs. Used in lab1, lab2, lab3, lab5.

**Approach B: `{prelabanswers}` environment** — Answers in a reusable environment with overlays split into `\PrelabPageBackground`, `\PrelabPageForeground{page#}`, `\PrelabTitleForeground`. Multi-page via `\clearpage` + `\setcounter{enumi}{N}`. Used in lab4.

### Prelab Header Evolution

Header line on page 2 evolved across 5 labs:

1. **lab1**: cramped, `edu,cn` typo: `UESTCStudentNumber:2025190907024Email:...edu,cn Date:2026.3.15`
2. **lab2-4**: cramped, fixed: `UESTCStudentNumber:2025190907024Email:...edu.cnDate:2026.X.X`
3. **lab5** (recommended): spaces added for readability: `UESTCStudentNumber: 2025190907024 Email: ...@std.uestc.edu.cn Date:2026.5.12`

The current template uses the clean lab5 spacing.

### Overlay Coordinates (absolute, unit = 1pt)

| Element | Position |
|---|---|
| "UESTCStudentNumber:" label | (75.864, 785.568) |
| Student number value | (~190, 785.568) |
| "Email:" label | (~270, 785.568) |
| Email value | (~302, 784.0) |
| "Date:" label | (~450, 785.568) |
| Separator rule | (74.34, 783.585), width 441.766pt |
| Score box | (99.984, 756.46) to (135.86, 724.18) |
| Section title "Answers to Questions" | (149.8, 723.0) |
| "(20 points)" | (~305, 723.45) |
| Footer page number | (294.4, 60.2) |
| First answer page vspace | 2.15cm |
| Continuation page vspace | 0.45cm |

## Postlab Template

See `templates/postlab_template.tex`. Four mandatory sections in fixed order:

### Section 1: Abstract (5 points, ~100 words)

Concise summary: what was measured, method, key results with final values and uncertainties. Bold key physics terms with `\textbf{}`.

### Section 2: Calculations, Results, and Comments (15 points)

The section title is usually `Calculations, Results, and Comments` but lab3 used the shorter `Calculations and Results`. Either is acceptable.

Structure pattern (varies by lab):

**Pattern A** (lab2, lab3): Data tables first → then calculations
**Pattern B** (lab4, lab5): Sample calculations first → then data tables → then comments/error analysis

Sample calculations should:
- Box key formulas with `\boxed{}`
- Show one complete worked example per formula
- Include substitution of real measured values
- State the final propagated uncertainty

Data tables:
- Start with `\small`, drop to `\footnotesize` or `\scriptsize` for wide tables
- Reduce `\tabcolsep` (to 2-3pt) before resorting to smaller font
- Wide tables (9+ columns) need `\scriptsize` + minimal `\tabcolsep`

Figures (when applicable):
- Generate from real data with Python/matplotlib, export PDF for vector quality
- Width: 0.88-1.03 `\textwidth`
- Caption should describe both what is plotted and the key finding

Error analysis:
- List sources with `\textbf{bold labels}`
- Discuss which source dominates (e.g., wire diameter appears as d², doubles its relative error)
- Mention: reading error, instrument calibration, alignment, environmental factors

### Section 3: Conclusions (10 points, ~100 words)

State what was verified/measured, restate final results with uncertainties, note main error sources. Use `\textbf{}` for key findings. In lab4 and lab5, conclusions are structured with bold sub-headings.

### Section 4: Answers to Postlab Questions (10 points)

```latex
\begin{enumerate}[leftmargin=2em,itemsep=0.25em,topsep=0.15em]
\item \textbf{Question title here}
% Full paragraph answer with equations, reasoning, and experimental references
\end{enumerate}
```

Lab5 established the best pattern: bold question summary as first sentence, then full explanation with equations, then connection to experimental observations. Earlier labs (lab1) had shorter 1-line answers.

### Appendix

Multi-page data sheets: one `figure[H]` per page. Some reports include a small signature/joke image at the bottom right: `\vfill\hfill\includegraphics[width=2.8cm]{signature.jpg}` (optional, personal preference).

## Data Extraction Scripts

Python with pypdf for bulk data extraction from textbook/data-sheet PDFs:

```python
from pypdf import PdfReader
reader = PdfReader("data.pdf")
for i, page in enumerate(reader.pages):
    text = page.extract_text()
```

Scripts live alongside the working directory.

## Figure Generation

```python
import matplotlib.pyplot as plt
# Use consistent styling: fontsize 12-14, grid, labeled axes
plt.rcParams.update({'font.size': 12})
# plot from real data arrays
plt.savefig("fig_name.pdf", bbox_inches="tight")
```

Only lab5-post included generated figures. Earlier labs used placeholder boxes or no figures.

## File Naming Convention

```
Source:  ExperimentName_Prelab_岳东翰.tex  /  ExperimentName_Postlab_岳东翰.tex
Output:  大物实验I-通微-2025190907024-岳东翰-labN-pre.pdf
         大物实验I-通微-2025190907024-岳东翰-labN-post.pdf
```

Adapt school/name/ID for each student.

## Common Mistakes

| Mistake | Fix |
|---|---|
| pdfLaTeX instead of XeLaTeX | XeLaTeX required for fontspec/Calibri/Times New Roman |
| Missing watermark on postlab | `\AddToShipoutPictureBG` after `\includepdf`, before first section |
| Single XeLaTeX pass | Two passes for cross-refs and page numbers |
| Fabricating data | Every value must be on a scanned data sheet or instrument spec |
| Wrong cover PDF filename | Match `\CoverPDF` exactly to file in working directory |
| Table exceeds margin | Reduce `\tabcolsep`, use smaller font, or rotate: `\scriptsize` + `\tabcolsep=2pt` |
| Prelab overlay misalignment | Don't change `\setlength{\unitlength}{1pt}` or geometry |
| Missing `\setcounter{page}{1}` after cover | Page numbering starts from cover |
| Prelab header `edu,cn` typo | Always check: it's `edu.cn` with a period |
| Cover date vs. overlay date mismatch | Cover uses `/`, overlay uses `.` — both fine, small differences OK |
| Forgetting `\tablefont` wrapper | Table text renders in wrong font without it |
