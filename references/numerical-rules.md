# Numerical Rules

Use this file whenever a report needs uncertainty propagation, significant
figures, linear regression, table values, or final result formatting.

## Authority Order

1. Current teacher data-processing/formula template for the experiment.
2. Current course lecture on uncertainty, graphing, and least-squares fitting.
3. Current lab manual/textbook formula.
4. This reference file.
5. Senior reports, only as examples.

## Default Reporting Rules

- Every number in the final report must trace to raw data, instrument specs,
  teacher templates, or accepted constants.
- Keep extra digits in intermediate calculation; round once at the final result.
- Write final quantitative results as `value ± uncertainty unit` when the
  experiment has a final measured quantity.
- Align the last digit of the value with the last digit of the uncertainty.
- State units in table headings or captions, not only in surrounding prose.
- Do not create a final quantitative result when the experiment is qualitative
  or graph-verification based; use fit quality, deviations, and error sources.

## Type A / Type B Pattern

Use Type A when repeated measurements exist:

```text
mean -> sample standard deviation -> standard uncertainty of the mean
```

Use Type B for instrument or reading limits. If the course template uses a
rectangular distribution, divide the limit by `sqrt(3)`.

Combine independent contributions in quadrature:

```text
sigma = sqrt(sigma_A^2 + sigma_B^2 + ...)
```

For products and quotients, use relative uncertainty propagation. Remember that
quantities raised to powers multiply relative uncertainty by the absolute power
coefficient, e.g. diameter squared contributes `2 sigma_d / d`.

## Regression And Figures

- Use real data arrays only.
- Plot scatter points and the fitted line; do not connect measured points with a
  misleading polyline unless the course explicitly asks for it.
- Label axes with quantity and unit.
- Put the fit equation and fit quality in either the figure caption or text.
- Save generated figures as PDF when possible for vector quality.
- For Malus-law style checks, consider both `I` versus angle and `I` versus
  `cos^2(theta)` when the experiment expects a linear relation.

## Known Course-Specific Defaults

- Chengdu local gravity used in current reports: `g_local = 9.79 m s^{-2}`.
- UESTC Physics Experiments I current postlab sections: Abstract (5),
  Calculations/Results/Comments (15), Conclusions (10), Questions (10).
- Older senior reports may show Abstract worth 10 points; current templates
  override older point values.
- Physics Experiments II historical templates may use short report or long
  report formats; confirm from the current cover/template before writing.
