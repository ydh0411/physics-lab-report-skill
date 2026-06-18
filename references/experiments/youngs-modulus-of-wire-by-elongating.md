# Young's Modulus of Wire by Elongating

## Aliases

- Young's Modulus of Wire by Elongating
- Measurement of the Young's Modulus
- Youngs Modulus
- 杨氏模量
- Lab 4 current label, Experiment 4 historical label

## Use This Card When

The report measures Young's modulus of a metal wire using an optical lever,
telescope scale, loading/unloading readings, and wire diameter measurements.

## Required Data Tables

- Data Table 4-1: instrument parameters. Include diameter zero reading, nine
  diameter readings, corrected diameters, `L`, `D`, optical lever arm `b`,
  instrument errors, and evaluating errors.
- Data Table 4-2: telescope scale readings during loading and unloading for
  total masses, plus averaged `n_i` values.

## Formula Checklist

- Mean diameter from corrected diameter readings.
- Loading interval displacement:
  `Delta n = [(n7-n3)+(n6-n2)+(n5-n1)+(n4-n0)] / 4`.
- Use absolute value of `Delta n` in the modulus formula.
- `E = 8 F L D / (pi d^2 b |Delta n|)`, with `F = mg`.
- Relative uncertainty propagation:
  `sigma_E / E` includes `sigma_L/L`, `sigma_D/D`, `2 sigma_d/d`,
  `sigma_b/b`, and `sigma_Delta n/Delta n`.

## Report Pattern

- Use the compact postlab spacing when the uncertainty section and appendix are
  long.
- Show a full worked example for mean diameter, scale displacement, Young's
  modulus, and uncertainty.
- Discuss wire diameter as a dominant uncertainty source because it appears as
  `d^2`.

## Common Pitfalls

- Losing the sign convention for `Delta n`; report the magnitude for `E`.
- Mixing millimetres and metres without stating conversion.
- Omitting loading/unloading averaging.
- Underestimating diameter uncertainty.
