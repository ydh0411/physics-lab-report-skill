# Franck-Hertz Experiment

## 中文补注

- 本学期编号：Lab8
- 报告类型：prelab + 长报告（Long lab report）；本学期两个长报告之一
- 教师特别要求：以当次教师要求为准。

## Aliases

- The Franck-Hertz Experiment
- Frank-Hertz Experiment
- First excitation potential of argon atom
- Archival numbers, not the 2026 lab number: Lab 8 in 2019 data tables; exp09
  in 2019 senior samples; lab10 in 2018 senior samples

## Required Data Tables

- Data Table 3-1: manual-mode current grid for accelerating voltage.
- Data Table 3-2: computer-mode current grid.
- Data Table 3-3: additional computer-mode grid when required.
- Record the peak positions `V1`, `V2`, `V3` from each curve before computing
  the first excitation potential.

## Formula Checklist

- Record the accelerating voltage coordinates of the six crests from the chosen trace; when two adjacent `1 V` readings tie at a flat crest, take their midpoint.
- Cumulative-difference method (teacher formula): compute `sum_{i=1}^{3} (V_{i+3} - V_i)` or the teacher-specified pairing, and divide by the exact denominator in `Calculations for Lab-8.docx` (e.g., `15` for six crests paired with cumulative differences) to obtain the first excitation potential `U0` and excitation energy `Delta E = e U0`.
- Distinguish the physical roles of `V1` (filament heating / thermionic emission), `V2` (extraction), `V3` (retarding barrier), and `V4` (accelerating voltage).
- Compare `U0` with the course accepted value for argon (`13.1 V`) and compute relative error.
- For postlab photon-wavelength question, use `lambda = hc / Delta E` and note that vacuum-ultraviolet lines require an evacuated optical path and VUV spectrometer.

## Common Pitfalls

- Choosing peaks by eye without showing the multi-trace `I-V` graph (plot manual and computer traces with distinct markers and label crests 1–6).
- Mixing up `V1`, `V2`, `V3` effects with changes in the intrinsic excitation potential `U0` (the voltages shift peak amplitude/width, not the atomic energy gap).
- Confusing excitation potential (V) with excitation energy (eV or J) in prelab definitions.
- Misreading trailing units on raw computer exports (e.g., `s` instead of `nA`): verify unit and document the correction in delivery notes.
