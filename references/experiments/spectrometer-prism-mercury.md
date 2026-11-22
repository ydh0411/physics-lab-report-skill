# Spectrometer Prism And Mercury Lines

## 中文补注

- 本学期编号：Lab7
- 报告类型：prelab + 短报告（Short lab report）
- 教师特别要求：以当次教师要求为准。

## Aliases

- Measurement of the Apex Angle of a Prism and the Wavelengths of Mercury Lights Using a Spectrometer
- To use a spectrometer to measure the apex angle of a prism and the wavelengths of mercury lights
- Spectrometer
- Prism apex angle
- Mercury spectrum
- Archival numbers, not the 2026 lab number: Lab 7 in 2019 data tables; exp12
  in 2019 senior samples; lab09 in 2018 senior samples

## Required Data Tables

- Data Table 2-1: apex angle readings for left and right telescope positions,
  two verniers, multiple trials, and averaged angles.
- Data Table 2-2: mercury spectral-line readings for diffraction orders `k=-1`
  and `k=+1`, including yellow doublet and green lines, with vernier readings
  and averages.

## Formula Checklist

- Opposite-vernier averaging for each position (`theta = (theta_1 + theta_2) / 2`) to cancel dial eccentricity error, and apex angle `A = |theta_L - theta_R| / 2`.
- Type A uncertainty from repeated trials and Type B uncertainty from instrument error limit (`1' / sqrt(3)` for rectangular distribution when specified), propagated independently across left and right telescope positions.
- Calibrate grating spacing `d` from the `546.07 nm` mercury green line (`d sin(phi_G) = |k| lambda_G`), then compute yellow-doublet wavelengths (`lambda_Y1`, `lambda_Y2`) and compare against `577.0 nm` and `579.0 nm`.
- Convert degrees/minutes carefully (`1 deg = 60'`) before averaging or propagating uncertainty.

## Common Pitfalls

- Averaging raw degree-minute strings without converting arcminutes (`60'` wrap-around near `360 deg`).
- Swapping left/right or `k=-1`/`k=+1` readings.
- Collapsing the yellow doublet (`577.0 nm` / `579.0 nm`) into one line when the data table separates it.
- Omitting the appendix section heading (`Appendix` + `Scanned data sheets` / `Original completed data sheet`) in short reports.
