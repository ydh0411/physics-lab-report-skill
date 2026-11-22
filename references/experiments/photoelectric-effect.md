# The Photoelectric Effect

## 中文补注

- 本学期编号：Lab10
- 报告类型：prelab + 短报告（Short lab report）
- 教师特别要求：以当次教师要求为准。

## Aliases

- The Photoelectric Effect
- Photoelectric Effect
- Planck constant by stopping potential
- Archival numbers, not the 2026 lab number: Lab 10 in 2019 data tables; exp11
  in 2019 senior samples; no separate 2018 senior label recorded

## Required Data Tables

- Data Table 7-1: wavelength, frequency, and stopping potential for different
  lights, including 365, 405, 436, 546, and 577 nm rows when used.
- Data Table 7-2: current-voltage characteristics of the photoelectric tube for
  two distances, commonly `d = 30 cm` and `d = 40 cm`.

## Formula And Figure Checklist

- Frequency: `nu = c / lambda` (convert wavelength from nm to m first).
- Linear model using signed stopping potentials `V_s` versus frequency `nu`: `V_s = a + b * nu`, where Einstein's equation gives `V_s = W_0 / (-e) + (-h / e) * nu` (or `|V_s| = (h / e) * nu - W_0 / e` if unsigned magnitudes are used — match the sign convention of the teacher sheet).
- Report sample means, centered sums (`S_xx`, `S_xy`, `S_yy`), slope `b`, intercept `a`, correlation coefficient `r` (or `R^2`), Planck constant `h = -e * b`, work function `W_0`, and relative error of `h`.
- Plot signed stopping potential versus frequency (scatter points plus fitted line, displaying fit equation and `R^2`), and `I-V` curves at both source distances (`30 cm` and `40 cm`) with distinct markers.

## Common Pitfalls

- Mixing wavelength in nm with meters when computing frequency, or dropping `10^14 Hz` scaling when recovering `h` in `J*s`.
- Mixing signed stopping potentials with unsigned magnitudes in the slope sign or work-function intercept.
- Fabricating readings at negative voltage points beyond the instrument's actual range (if the supply does not reach `-2.0 V`, leave blank and note the instrument range limit).
