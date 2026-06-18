<p align="center">
  <img src="https://img.shields.io/badge/LaTeX-XeLaTeX-008080?style=for-the-badge&logo=latex" alt="XeLaTeX">
  <img src="https://img.shields.io/badge/UESTC-Glasgow%20College-005bac?style=for-the-badge" alt="UESTC Glasgow College">
  <img src="https://img.shields.io/badge/Codex%20%7C%20Claude%20Code-Skill-5b5fc7?style=for-the-badge" alt="Codex and Claude Code Skill">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">大学物理实验报告 Skill</h1>

<p align="center">
  面向电子科技大学格拉斯哥学院的大物实验报告工作流。<br>
  用现成的 prelab/postlab LaTeX 模板，结合真实数据、公式表格和课程要求，生成可提交的 PDF。
</p>

---

## 目录

- [这个仓库解决什么问题](#这个仓库解决什么问题)
- [现在包含什么](#现在包含什么)
- [已整理的实验参考](#已整理的实验参考)
- [安装](#安装)
- [第一次使用](#第一次使用)
- [每次写报告](#每次写报告)
- [数据怎么处理](#数据怎么处理)
- [学长报告怎么用](#学长报告怎么用)
- [编译 PDF](#编译-pdf)
- [仓库结构](#仓库结构)
- [重要约定](#重要约定)

## 这个仓库解决什么问题

大物实验报告最麻烦的地方通常不是写几段话，而是这些细节：

- 封面 PDF 要按学校模板插入，不能在 LaTeX 里重画。
- 预习报告有固定的页眉、计分框、水印和绝对坐标叠加层。
- 正式报告要有分值框、数据表、不确定度、课后题和原始数据附录。
- lab 编号每年会变，实验标题才是可靠线索。
- 手写数据容易被 OCR 读错，尤其是小数点、单位、角度和表格行。
- 学长报告有参考价值，但不能覆盖当前老师的模板和公式要求。

这个 skill 的思路很简单：保留已经整理好的 LaTeX 模板，把课程经验整理成可查的静态 reference。它不是向量数据库，也不会“训练”模型。以后生成报告时，agent 先按实验标题找到对应参考，再使用你提供的真实数据和当前模板完成报告。

## 现在包含什么

| 模块 | 内容 |
|---|---|
| `templates/` | 已整理好的 `prelab_template.tex` 和 `postlab_template.tex`，这是本仓库的核心，不随便改 |
| `scripts/` | `build_report.sh`，本地 XeLaTeX 两遍编译并重命名 PDF |
| `config/` | 学生信息、命名规则、模板字段的示例配置 |
| `references/` | 材料查找、数值规则、编译交付、课程流程、实验索引 |
| `references/experiments/` | Physics Experiments I/II 的实验知识卡片 |
| `agents/openai.yaml` | Codex UI 里显示 skill 名称和默认提示词 |

## 已整理的实验参考

### Physics Experiments I

| 当前提交标签 | 实验标题 |
|---|---|
| lab1 | Measurement of Resistance by Ammeter-Voltmeter Method |
| lab2 | The Oscilloscope |
| lab3 | Newton's Rings |
| lab4 | Young's Modulus of Wire by Elongating |
| lab5 | Polarized Light |

### Physics Experiments II

这些来自历史资料和“三人行”文件夹的整理。不同年份编号会变，所以这里只把编号当线索。

| 历史标签 | 实验标题 |
|---|---|
| Lab 6 / exp08 | Michelson Interferometer: laser wavelength and air refractive index |
| Lab 7 / exp12 | Spectrometer: prism apex angle and mercury spectral lines |
| Lab 8 / exp09 | Franck-Hertz Experiment |
| Lab 9 / exp10 | Millikan Oil Drop Experiment |
| Lab 10 / exp11 | The Photoelectric Effect |
| Lab 11 / exp13 | The Potentiometer |

旧年份里还出现过 Wheatstone Bridge、Ultrasonic Speed 等实验。它们已经在索引里标为历史补充材料；如果你们当年也做，再按当前模板补成正式卡片。

## 安装

### Codex

```bash
mkdir -p ~/.codex/skills
git clone --depth=1 https://github.com/ydh0411/physics-lab-report-skill.git \
  ~/.codex/skills/physics-lab-report
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone --depth=1 https://github.com/ydh0411/physics-lab-report-skill.git \
  ~/.claude/skills/physics-lab-report
```

安装后重启 Codex 或 Claude Code。更新时进入 skill 目录执行：

```bash
git pull
```

## 第一次使用

第一次设置只做一遍，之后每次报告就不用反复输入个人信息。

1. 把官方 prelab/postlab 封面 PDF 放到报告工作目录。
2. 复制 `config/student_profile.example.yaml` 为 `config/student_profile.yaml`，填姓名、学号、邮箱、学院、专业、班级、老师和 TA。
3. 复制 `config/naming.example.yaml` 为 `config/naming.yaml`，按老师要求写 PDF 文件名格式。
4. 复制 `config/template_fields.example.yaml` 为 `config/template_fields.yaml`，记录封面字段。
5. 确认课程版本和本学期模板。

个人配置、教材 PDF、老师 PPT、扫描数据表都不要提交到公开仓库。放在本地工作目录或 `private_assets/` 里即可。

## 每次写报告

推荐流程大概是这样：

| 步骤 | 要做什么 | 目的 |
|---:|---|---|
| 1 | 确认实验标题 | 用标题匹配 reference，避免 lab 编号变动 |
| 2 | 选择 prelab / postlab | 使用对应的金标准 LaTeX 模板 |
| 3 | 输入或确认原始数据 | 先确认数据，再计算和写结论 |
| 4 | 读取实验参考和当前模板 | 对齐公式、表格、分值和老师要求 |
| 5 | 生成 TeX、图表和附录 | 保留可追溯的报告工程 |
| 6 | 用 XeLaTeX 编译 | 本地生成可提交 PDF |
| 7 | 按命名规则输出 | 得到符合提交要求的文件名 |

推荐你这样给 agent 信息：

```text
使用 physics-lab-report 生成正式报告。

实验标题：Polarized Light
提交标签：lab5
日期：2026.5.12

我会手动输入原始数据。请先整理数据表让我确认，
确认后再计算、写报告并编译 PDF。
```

更简短也可以：

```text
帮我生成 Young's Modulus 的 postlab。lab 编号是 lab4，数据我下面给你。
```

关键是给完整实验标题。`lab4` 这种标签只用于封面和文件名，不用来判断实验内容。

## 数据怎么处理

手动输入数据优先。OCR 或图片识别只能作为草稿。

如果你上传扫描件，agent 应该先把数据整理成表格给你确认。你确认之前，它不应该继续算不确定度，也不应该写最终结论。这个规则有点麻烦，但能避开最常见的坑：小数点看错、单位漏掉、角度行错位。

## 学长报告怎么用

学长报告只做三件事：

- 看完整度，比如摘要、计算、结论和课后题是不是都覆盖了。
- 看表达习惯，比如误差分析该写到什么程度。
- 看旧年份有哪些实验和表格形式。

它们不能当作当前答案来源。当前模板、老师给的公式表格、你的原始数据永远排在前面。我们要做的是在参考它们的基础上写得更可靠，而不是复刻旧报告。

资料优先级可以简单记成：

| 优先级 | 材料 |
|---:|---|
| 1 | 当前官方模板、封面、老师要求 |
| 2 | 你的原始数据和已签字扫描件 |
| 3 | 本仓库的实验 reference |
| 4 | 教材、实验书、老师 PPT |
| 5 | 学长报告和旧年份样例 |

## 编译 PDF

本地有 XeLaTeX 时，直接用脚本：

```bash
bash scripts/build_report.sh report.tex "大物实验I-通微-学号-姓名-lab5-post.pdf"
```

脚本会：

1. 检查 `xelatex` 是否存在。
2. 编译两遍。
3. 清理常见辅助文件。
4. 按你给的名字重命名 PDF。

没有本地 LaTeX 环境也没关系。把报告工程上传到 Overleaf，编译器选 XeLaTeX。

## 仓库结构

```text
physics-lab-report-skill/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── config/
│   ├── naming.example.yaml
│   ├── student_profile.example.yaml
│   └── template_fields.example.yaml
├── references/
│   ├── course-workflow.md
│   ├── experiment-index.md
│   ├── figures-and-compilation.md
│   ├── material-discovery.md
│   ├── numerical-rules.md
│   └── experiments/
├── scripts/
│   └── build_report.sh
└── templates/
    ├── prelab_template.tex
    └── postlab_template.tex
```

## 重要约定

- `templates/prelab_template.tex` 和 `templates/postlab_template.tex` 是金标准模板。除非明确要维护模板，否则不要改它们的设定。
- 封面用 `\includepdf` 插入，不在 LaTeX 里重画。
- 生成报告时复制模板到工作文件，再填内容。
- 所有数字必须能追溯到原始数据、仪器规格、公式表格或教材常数。
- 缺数据就生成空表，不生成最终报告。
- 缺题目就留占位或问用户，不编题。
- 教师签名不自动放置。正确做法是手填数据表、签字、扫描，再放进附录。

## 这个 skill 不做什么

- 不替你伪造实验数据。
- 不把教材、老师 PPT、学长报告原文塞进公开仓库。
- 不把旧报告里的结论当成当前结论。
- 不保证所有年份的 lab 编号一致。
- 不在没有编译的情况下声称 PDF 已经通过。

## 适配别的学校

可以借这个结构，但不要直接套模板。你至少要换：

- 官方封面 PDF
- prelab 页眉和计分框坐标
- postlab 分区名称和分值
- 水印文字
- PDF 命名规则
- 实验索引和公式表格

## License

MIT
