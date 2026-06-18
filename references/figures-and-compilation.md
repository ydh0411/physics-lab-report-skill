# Figures And Compilation

Use this file when generating figures, adding scanned data sheets, compiling
with XeLaTeX, or preparing final PDFs for submission.

## Golden Template Rule

The committed files below are golden templates:

- `templates/prelab_template.tex`
- `templates/postlab_template.tex`

Do not rewrite, reformat, or simplify their settings unless the user explicitly
asks for template maintenance. They encode hard-won cover insertion, overlay,
watermark, score-box, font, and spacing behavior. Generate report copies from
them, but leave the originals unchanged.

## File Layout For A Report

Keep all compile-time files in one report folder:

```text
report-folder/
├── report.tex
├── official-cover.pdf
├── scanned-data.pdf
├── figures/
│   ├── fit-plot.pdf
│   └── apparatus-photo.jpg
└── scripts/
    └── make_plot.py
```

LaTeX files should use relative paths only. Avoid absolute paths from the user's
Desktop or Downloads folders.

## Figures

- Generate plots from real data with Python/matplotlib or another reproducible
  script.
- Save vector plots as `.pdf` when possible.
- Use short ASCII filenames for generated figures: `malus-fit.pdf`,
  `lissajous-ratio-1.png`, `photoelectric-fit.pdf`.
- If a figure comes from a scan/photo, only crop, rotate, deskew, or trim for
  readability. Do not redraw waveforms, change values, or add missing markings.
- If a required figure is missing, leave a placeholder note in the draft and ask
  for the source image; do not invent the figure.

## Compilation

Use XeLaTeX for the committed UESTC templates:

```bash
bash scripts/build_report.sh report.tex "final-name.pdf"
```

The script compiles twice, cleans common auxiliary files, and optionally renames
the PDF. If it fails, inspect the `.log` before changing content.

## Static Checks Before Delivery

- Cover PDF path exists and matches `\CoverPDF`.
- Data sheet path exists and matches `\DataPDF` when appendix scans are included.
- Every `\includegraphics` target exists.
- No generated report references a private absolute path.
- No fabricated data, formulas, postlab questions, or signatures appear.
- Final PDF filename follows `config/naming.yaml` when available.
