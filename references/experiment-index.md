# 实验索引

实验英文全名是主键。编号（Lab6、exp12、lab08）只用于封面字段和文件名，不用于判断是哪个实验。

## 匹配规则

1. 先用实验英文全名匹配卡片与教师材料；全名不完全一致时用 `Aliases` 里的正式全称、常见简称。
2. 全名与编号冲突时以全名为准，并告诉用户编号标签不一致。
3. 编号每年、每位教师都可能变；同一实验在不同年份有多个历史编号，只作检索线索。
4. 卡片匹配不到时不要硬套：说明缺卡片，按当次教师模板与公式文件工作，必要时新增卡片。
5. 匹配到卡片后仍要读当次模板与 `Calculations for Lab-*.docx`；卡片给的是清单，不是当年公式。

## Physics Experiments I（历史，5 项）

历史实验，编号来自 Physical Experiment I 的提交标签。2026 秋季的 Physical Experiment II 不使用这些标签。

| 提交标签 | 实验全名 | 报告类型 | 卡片 |
| --- | --- | --- | --- |
| lab1 | Measurement of Resistance by Ammeter-Voltmeter Method | 历史参考：prelab + postlab | [`experiments/measurement-of-resistance-by-ammeter-voltmeter-method.md`](experiments/measurement-of-resistance-by-ammeter-voltmeter-method.md) |
| lab2 | The Oscilloscope | 历史参考：prelab + postlab | [`experiments/the-oscilloscope.md`](experiments/the-oscilloscope.md) |
| lab3 | Newton's Rings | 历史参考：prelab + postlab | [`experiments/newtons-rings.md`](experiments/newtons-rings.md) |
| lab4 | Young's Modulus of Wire by Elongating | 历史参考：prelab + postlab | [`experiments/youngs-modulus-of-wire-by-elongating.md`](experiments/youngs-modulus-of-wire-by-elongating.md) |
| lab5 | Polarized Light | 历史参考：prelab + postlab | [`experiments/polarized-light.md`](experiments/polarized-light.md) |

旧资料里还有 Hall Effect 等其他 Physical Experiment I 实验。课程要求出现时再补结构化卡片，不要凭旧目录凑。

## Physics Experiments II（2026 秋，6 项）

每个实验都写 prelab；正式报告按「报告类型」列选模板。本学期的两个长报告是 Michelson 与 Franck-Hertz，其余为短报告。

| 本学期编号 | 实验全名 | 报告类型 | 学长编号 | 卡片 |
| --- | --- | --- | --- | --- |
| Lab6 | Measuring Laser Wavelength and Index of Refraction of Air by Michelson Interferometer | prelab + **Long** | exp08 | [`experiments/michelson-interferometer.md`](experiments/michelson-interferometer.md) |
| Lab7 | Measurement of the Apex Angle of a Prism and the Wavelengths of Mercury Lights Using a Spectrometer | prelab + Short | exp12 | [`experiments/spectrometer-prism-mercury.md`](experiments/spectrometer-prism-mercury.md) |
| Lab8 | The Franck-Hertz Experiment | prelab + **Long** | exp09 | [`experiments/franck-hertz.md`](experiments/franck-hertz.md) |
| Lab9 | The Millikan Oil Drop Experiment | prelab + Short | exp10 | [`experiments/millikan-oil-drop.md`](experiments/millikan-oil-drop.md) |
| Lab10 | The Photoelectric Effect | prelab + Short | exp11 | [`experiments/photoelectric-effect.md`](experiments/photoelectric-effect.md) |
| Lab11 | The Potentiometer | prelab + Short | exp13 | [`experiments/potentiometer.md`](experiments/potentiometer.md) |

- 前半段顺序：Lab6 → Lab7 → Lab9 → Lab8；之后按学号单双号与安排表，见 `assets/course-schedule-2026.png`。
- Lab9（2026-10-24）教师要求：5 组油滴，每组 3 次电压和时间读数；数据表与附录保留 5 组、删掉 6–10 组空白行，平均元电荷取 5 组均值。仅该次适用，其他实验以当次教师要求为准。
- 学长编号来自历史学长报告文件名里的 `expNN`，不能当成本学期编号。
- 2019 数据表编号即教师公式文件夹里 `Calculations for Lab 6` … `Calculations for Lab-11` 的后缀数字。

## 历史编号对照

同一实验在 2019 数据表、2019 学长报告、2018 学长报告里的编号各不相同。2026 编号与 2019 数据表编号恰好一致，但 2019 学长报告的 `expNN` 与 2018 学长报告的 `labNN` 都错位，不能互推。

| 实验全名 | 2019 数据表编号 | 2019 学长 expNN | 2018 学长 labNN | 2026 本学期编号 |
| --- | --- | --- | --- | --- |
| Measuring Laser Wavelength and Index of Refraction of Air by Michelson Interferometer | Lab 6 | exp08 | lab08 | Lab6 |
| Measurement of the Apex Angle of a Prism and the Wavelengths of Mercury Lights Using a Spectrometer | Lab 7 | exp12 | lab09 | Lab7 |
| The Franck-Hertz Experiment | Lab 8 | exp09 | lab10 | Lab8 |
| The Millikan Oil Drop Experiment | Lab 9 | exp10 | lab11 | Lab9 |
| The Photoelectric Effect | Lab 10 | exp11 | 无记录 | Lab10 |
| The Potentiometer | Lab 11 | exp13 | lab15 | Lab11 |

读法举例：卡片或旧文件里出现 `lab08`，在 2018 学长报告里指 Michelson，而 2026 的 Lab8 是 Franck-Hertz。遇到这种编号先按全名确认，再决定用哪份材料。

## 旧资料中的其他实验

只在旧学长文件夹里出现、本学期安排表没有的实验。当前课程材料确认前只当历史补充，不据此生成报告。

| 实验 | 历史来源 | 处理 |
| --- | --- | --- |
| The Wheatstone Bridge and the Prototype of Electric Balance | 2018 / 2017 学长报告 | 历史补充；本学期出现时再建卡片 |
| Measuring the Ultrasonic Speed | 2018 / 2017 学长报告 | 历史补充；本学期出现时再建卡片 |
| Experimental Examination - Potentiometer | 2019 学长报告 | 历史补充；与 Lab11 Potentiometer 卡片部分重叠，考核形式不同，不混用结论 |
| Hall Effect | Physical Experiment I 旧资料 | 历史补充；属 Physics I，不属本学期安排 |

## 模板与分值

同一实验在不同年份可能套不同模板，分值也不同：旧报告的 Abstract 有 3 分和 10 分两种。节标题、字数与分值一律读当次模板，不按旧报告推断。教师签名出现在数据表上；附已完成扫描件，不生成签名。