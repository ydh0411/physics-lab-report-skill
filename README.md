<p align="center">
  <img src="https://img.shields.io/badge/Word-DOCX-2B579A?style=for-the-badge&logo=microsoftword" alt="Word DOCX">
  <img src="https://img.shields.io/badge/UESTC-Glasgow%20College-005bac?style=for-the-badge" alt="UESTC Glasgow College">
  <img src="https://img.shields.io/badge/Codex%20%7C%20Claude%20Code-Skill-5b5fc7?style=for-the-badge" alt="Codex and Claude Code Skill">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">大学物理实验报告 Skill</h1>

<p align="center">
  电子科技大学格拉斯哥学院大物实验报告的个人工作流。<br>
  用当次教师的 Word 模板，结合真实数据、教师公式表格和课程要求，产出可提交、可复核的 DOCX + PDF。
</p>

---

## 目录

- [这个仓库解决什么问题](#这个仓库解决什么问题)
- [现在包含什么](#现在包含什么)
- [三类报告](#三类报告)
- [工作流：七个阶段](#工作流七个阶段)
- [写作要求：去 AI 味与去防御性](#写作要求去-ai-味与去防御性)
- [已整理的实验参考](#已整理的实验参考)
- [安装](#安装)
- [第一次使用](#第一次使用)
- [每次写报告](#每次写报告)
- [数据怎么处理](#数据怎么处理)
- [学长报告怎么用](#学长报告怎么用)
- [字体、公式与 PDF 检查](#字体公式与-pdf-检查)
- [LaTeX 遗留路径](#latex-遗留路径)
- [仓库结构](#仓库结构)
- [重要约定](#重要约定)
- [这个 skill 不做什么](#这个-skill-不做什么)
- [适配别的学校](#适配别的学校)
- [License 与素材归属](#license-与素材归属)

## 这个仓库解决什么问题

大物实验报告费时间的地方通常不是写几段话，而是这些细节：

- **老师换模板**：封面要填在表格里、每节配一个评分框、页眉有学号/邮箱/日期栏、正文分节、水印和校徽嵌在模板里。这些是原生 Word 要素，重画就露馅。
- **英文报告里的字体陷阱**：正文要 Times New Roman，中文姓名要宋体；公式必须是原生 OMML。Word 常把数学字母悄悄换成 Cambria Math，LibreOffice 缺字体时回退 Liberation——写在样式里的字体名不等于 PDF 里真的用了。
- **编号每年变**：`lab7`、`exp12`、`Lab7` 在不同年份指不同的实验，实验英文全名才是可靠主键。
- **手写数据容易读错**：小数点、单位、角度、行错位，OCR 只配当草稿，必须人工确认后再计算。
- **学长报告只能参考**：能看题目覆盖、计算展开和版面密度，不能拿它的数据、错误公式或旧分值当答案。
- **模型爱写 AI 味和防御性句子**：`plays a crucial role`、`It is important to note`、`To ensure rigor`、`might potentially suggest` 这类句子不进报告。本仓库把这条要求变成流程关卡，并给了可执行的 lint。

这个 skill 是静态的、可审计的知识库：不训练模型、不做向量检索。agent 按实验全名找到对应卡片和规则，用你提供的真实数据和当次模板完成报告。

## 现在包含什么

| 模块 | 内容 |
|---|---|
| `assets/word-templates/` | 2026 三份教师 Word 模板（预习 / 短报告 / 长报告），是当前主路径 |
| `assets/course-schedule-2026.png` | 本学期实验编号、全名与顺序 |
| `references/` | 课程地图、写作规则、计算与排版检查、全流程、实验索引、11 张实验卡片 |
| `scripts/` | 文风 lint、DOCX 结构/字体检查、DOCX→PDF、PDF 字体检查、素材与链接校验；另有 LaTeX 遗留编译脚本 |
| `config/` | 个人信息、交付命名、模板字段映射的示例配置（填好的版本被 gitignore） |
| `tests/fixtures/` | 文风 lint 的正反例句，CI 用它验证规则有效 |
| `templates/` | 早期 LaTeX 模板，历史保留，当前课程不用 |
| `agents/openai.yaml` | Codex 中的显示名与默认提示词 |

## 三类报告

2026 三份模板的核验快照；当次模板改版时以实际文件为准。

| | Prelab | Short postlab | Long lab report |
|---|---|---|---|
| 封面 | 表格字段 + 评分框 | 同左 | 同左 |
| 正文节 | Answers to Questions (20) | Abstract (10)、Calculations and Results (15)、Conclusions (5)、Answers to Postlab Questions (10)、数据扫描附录 | Abstract (3)、Introduction (3)、Experimental Procedure (3)、Results (2)、Discussion (5)、Conclusions (2)、References (1)、Answers to Questions (6)、Appendix Calculations (15)、数据扫描附录 |
| 字数 | 按题作答 | 摘要约 100 词、结论约 100 词 | 摘要约 100 词、讨论 >150 词、结论约 50 词 |
| 引用 | 不加 References、不放文内编号 | 同左 | 保留真实、核验过的 References |

章节标题、分值和字数要求来自模板原文，不要凭印象写，也不要给 prelab 拼通用论文式的背景、讨论和结论。

## 工作流：七个阶段

每阶段有硬门槛，未过不进下一阶段。细节见 [`references/course-workflow.md`](references/course-workflow.md)。

1. **确认任务**：新建 / 重算 / 修订 / 纯格式修改 / 只读提交检查。范围不同，产物不同。
2. **定位实验**：用实验英文全名匹配卡片与当次教师材料，编号只用于封面和文件名。
3. **确认数据**：整理成表格给用户确认；OCR 结果逐值确认前不算数。
4. **计算**：按教师文件的公式结构、符号、顺序做四步链（公式 → 带单位代入 → 结果 → 不确定度/误差/拟合）。
5. **写各节**：按模板骨架逐节填写，不增不减章节。
6. **写作关卡**：内容通读 → 表达通读（去 AI 味、去防御性）→ `python3 scripts/lint_writing.py <docx>` 清零。
7. **排版与导出**：`check_docx.py` → `docx_to_pdf.sh` → `check_pdf_fonts.sh` → 逐页看 PDF。

## 写作要求：去 AI 味与去防御性

这不是可选润色，而是第 6 阶段的关卡。完整清单、规则 id 和 before→after 例句见 [`references/writing-policy.md`](references/writing-policy.md)。

**删掉的典型句子**（中英对照的判据在写作规则里）：

| 类别 | 反例 | 处理 |
|---|---|---|
| AI-1 浮夸形容词 | `plays a crucial role in modern physics` | 直接说该量在实验里干什么 |
| AI-4 聊天腔/第三人称 | `In this report, we will discuss...` / `This study investigates...` | 从第一句物理内容开始 |
| AI-2 机械三段式 | 先讲意义 → 再讲步骤 → 再讲意义 | 按模板节次和物理因果组织 |
| AI-9 破折号打断 | `The drift — caused by heating — shifted...` | 改用逗号、括号或从句 |
| AI-10 空洞 `-ing` 尾巴 | `serves as ..., highlighting its importance` | 改回 `is/has` 并删空洞拔高 |
| DEF-1 模板声明 | `We use the provided template and tables` | 删；模板使用不是报告内容 |
| DEF-2 章节旁白 | `Data are processed using Sec. 3.9.6 of the textbook` | 删；直接给出处理过程和结果 |
| DEF-3 重复限定 | `might potentially suggest that` | 收成一层：`suggests that` |
| DEF-4 自我辩护 | `To ensure rigor and avoid misunderstanding` | 删；说明具体做法即可 |
| DEF-5 有效数字教学 | 解释末位对齐为什么保留两位 | 删；正确取位直接体现在式子里 |

**保留的内容**：影响结论的真实假设（只说一次）、证实不足时的 `may` / `suggests`、异常数据和不理想结果、题目要求的定义与推导。

**两轮通读**：内容通读（每问是否答到、段落职责、方程与结果衔接、详略符合模板）和表达通读（过程旁白、过度解释、重复限定、聊天腔）。两轮改同一份成稿，不另出一份语言评审报告。

lint 命令：

```bash
python3 scripts/lint_writing.py 报告.docx              # 默认命中即失败（--max 0）
python3 scripts/lint_writing.py 报告.docx --max 2      # 允许 2 处未处理
python3 scripts/lint_writing.py --list-rule            # 打印规则 id 与说明
```

lint 只查词句模式，不判断物理正确性和是否答到题；内容通读不能省。

## 已整理的实验参考

### Physics Experiments I（历史）

| 提交标签 | 实验标题 | 卡片 |
|---|---|---|
| lab1 | Measurement of Resistance by Ammeter-Voltmeter Method | [`experiments/measurement-of-resistance-by-ammeter-voltmeter-method.md`](references/experiments/measurement-of-resistance-by-ammeter-voltmeter-method.md) |
| lab2 | The Oscilloscope | [`experiments/the-oscilloscope.md`](references/experiments/the-oscilloscope.md) |
| lab3 | Newton's Rings | [`experiments/newtons-rings.md`](references/experiments/newtons-rings.md) |
| lab4 | Young's Modulus of Wire by Elongating | [`experiments/youngs-modulus-of-wire-by-elongating.md`](references/experiments/youngs-modulus-of-wire-by-elongating.md) |
| lab5 | Polarized Light | [`experiments/polarized-light.md`](references/experiments/polarized-light.md) |

### Physics Experiments II（2026 学期）

| 本学期编号 | 实验标题 | 报告类型 | 学长编号 | 卡片 |
|---|---|---|---|---|
| Lab6 | Measuring Laser Wavelength and Index of Refraction of Air by Michelson Interferometer | Long | exp08 | [`experiments/michelson-interferometer.md`](references/experiments/michelson-interferometer.md) |
| Lab7 | Measurement of the Apex Angle of a Prism and the Wavelengths of Mercury Lights Using a Spectrometer | Short | exp12 | [`experiments/spectrometer-prism-mercury.md`](references/experiments/spectrometer-prism-mercury.md) |
| Lab8 | The Franck-Hertz Experiment | Long | exp09 | [`experiments/franck-hertz.md`](references/experiments/franck-hertz.md) |
| Lab9 | The Millikan Oil Drop Experiment | Short | exp10 | [`experiments/millikan-oil-drop.md`](references/experiments/millikan-oil-drop.md) |
| Lab10 | The Photoelectric Effect | Short | exp11 | [`experiments/photoelectric-effect.md`](references/experiments/photoelectric-effect.md) |
| Lab11 | The Potentiometer | Short | exp13 | [`experiments/potentiometer.md`](references/experiments/potentiometer.md) |

本学期安排表见 [`assets/course-schedule-2026.png`](assets/course-schedule-2026.png)，编号与题目的完整对照见 [`references/experiment-index.md`](references/experiment-index.md)。编号每年会变，历史编号只作线索。

## 安装

```bash
mkdir -p ~/.codex/skills
git clone --depth=1 https://github.com/ydh0411/physics-lab-report-skill.git \
  ~/.codex/skills/physics-lab-report
```

Claude Code 换成 `~/.claude/skills/physics-lab-report`。完整步骤、运行环境依赖和验证命令见 [`INSTALL.md`](INSTALL.md)。

## 第一次使用

1. 复制 `config/*.example.yaml` 为同目录的 `*.yaml`，填写个人信息、命名规则、模板字段。
2. 用当次模板核对 `config/template_fields.yaml` 的节标题与分值（模板换版时必做）。
3. 确认系统装有 Times New Roman 与宋体；需要脚本检查时再准备 `python-docx`、LibreOffice、`pdffonts`。
4. 跑一遍 `INSTALL.md` 的验证命令，确认模板可打开、lint 的正反例退出码正确。

## 每次写报告

| 步骤 | 做什么 |
|---:|---|
| 1 | 给实验英文全名、当次编号、报告类型、本次数据 |
| 2 | agent 先整理数据表，用户确认后才计算 |
| 3 | 按教师公式表格做计算链，补全平均值等派生栏 |
| 4 | 按模板骨架写各节 |
| 5 | 过写作关卡：两轮通读 + lint 清零 |
| 6 | 检查字体/结构，导出 PDF 并逐页看版式 |
| 7 | 按命名规则交付 DOCX + PDF |

示例：

```text
使用 physics-lab-report 完成本次报告。

实验全名：The Millikan Oil Drop Experiment
本学期编号：Lab9，短报告
教师要求：测 5 组油滴，每组 3 次电压和时间读数
数据我下面粘贴，先整理成表让我确认，确认后再计算和写。
```

## 数据怎么处理

- **手输优先**。扫描件、照片、OCR 都只是草稿。
- 让 agent 先把数据整理成表格给你确认；确认前不计算、不写结论。
- 原始记录不因偏离理论值而调整。有依据的录入或计算错误可以改，保留原记录，并说明改了哪几项、依据是什么。
- 无法唯一确定的读数不猜改，直接问。
- 缺数据时只出空表或骨架，不填示例值、不写结论。

## 学长报告怎么用

只做三件事：看题目覆盖是否完整、看计算展开和误差分析写到什么程度、看旧年份的表格形式。

优先级：

| 优先级 | 材料 |
|---:|---|
| 1 | 当次教师模板、封面、教师通知 |
| 2 | 你的原始数据与已确认记录 |
| 3 | 本仓库实验卡片与教师公式表格 |
| 4 | 教材、实验书、教师 PPT |
| 5 | 学长报告与旧年份样例 |

学长报告不能覆盖当次模板和公式要求，也不能按旧编号直接套用。

## 字体、公式与 PDF 检查

- 英文正文、表格、页眉页脚、公式中的拉丁字母与数字：**Times New Roman**，通常 12 pt。
- 中文封面信息：**宋体 / SimSun**。缺汉字的字体里硬写中文会显示为方块或替换字形。
- 公式用原生可编辑 OMML；变量斜体，数值、单位、函数、描述性下标正体。不要把公式做成图片来掩盖字体问题。
- 版式保留模板原生的边框、logo、水印、评分框、分节、页眉页脚与页码域；正文连续分页，避免每项计算单独一页。

导出后必须查实际字体，不能只看 DOCX 样式 XML：

```bash
python3 scripts/check_docx.py 报告.docx            # 字体统计、非 TNR/宋体命中、OMML 数、节标题、评分框数
bash scripts/docx_to_pdf.sh 报告.docx 报告.pdf     # LibreOffice 导出，拒绝覆盖除非 --force
bash scripts/check_pdf_fonts.sh 报告.pdf          # PDF 里真正用到的字体
```

Word 可能把数学字母替换成 Cambria Math；LibreOffice 在字体缺失时回退 Liberation。两条都要看，最后逐页看 PDF：封面信息、边框、水印、评分框、断页、公式符号、签名位置、页码、异常空白。

## LaTeX 遗留路径

`templates/prelab_template.tex`、`templates/postlab_template.tex` 和 `scripts/build_report.sh` 是早期 LaTeX 方案，当前课程不用。仅当课程或教师明确要求 LaTeX 时使用，说明见 [`templates/README.md`](templates/README.md)。不要用 LaTeX 版本覆盖现有 Word 报告。

## 仓库结构

```text
physics-lab-report-skill/
├── SKILL.md                     # 主规范（agent 入口）
├── README.md
├── INSTALL.md
├── agents/openai.yaml
├── assets/
│   ├── ASSETS.md                # 素材来源与使用边界
│   ├── course-schedule-2026.png
│   └── word-templates/          # 2026 三份教师 Word 模板
├── config/                      # 个人信息、命名、模板字段示例
├── references/
│   ├── course-profile.md        # 课程地图、模板结构、编号映射、交付
│   ├── writing-policy.md        # 去 AI 味 + 去防御性 + 语言规则
│   ├── calculation-layout-qa.md # 计算链、表格、字体、公式、版式、PDF 检查
│   ├── course-workflow.md       # 七阶段流程与四种任务模式
│   ├── experiment-index.md      # 实验索引（全名优先）
│   └── experiments/             # 11 张实验卡片
├── scripts/
│   ├── lint_writing.py          # 文风 lint（去 AI 味/去防御性规则）
│   ├── check_docx.py            # DOCX 字体与结构检查
│   ├── docx_to_pdf.sh           # LibreOffice 导出
│   ├── check_pdf_fonts.sh       # PDF 实际字体检查
│   ├── check_assets.py          # 素材可打开 + 相对链接校验
│   ├── build_report.sh          # LaTeX 遗留编译
│   └── smoke_test.sh            # LaTeX 模板冒烟测试
├── templates/                   # LaTeX 遗留模板
└── tests/fixtures/             # 文风 lint 正反例句
```

## 重要约定

- 三份 Word 模板是当前金标准：复制出来填内容，不重画封面、不删评分框、不改水印与页眉页脚。
- 实验全名是主键；编号只用于封面和文件名。
- 所有数字必须能追溯到原始数据、仪器规格、教师公式表格或教材常数。
- 缺数据出空表，缺题目留占位或问用户，缺签名不代签。
- 字体和 PDF 检查要做，做了才说做了；没渲染、没核实数据时明确说明。
- 个人信息、教材、教师计算文件、学长报告、原始数据、签名留在本地，不进公开仓库。

## 这个 skill 不做什么

- 不伪造实验数据、题目、公式或签名。
- 不把教材、教师计算文件、学长报告塞进公开仓库。
- 不把旧报告结论当成当前结论，不按旧编号套用。
- 不用「看起来没问题」代替 PDF 逐页检查。
- 不把 lint 通过当成物理和内容正确。

## 适配别的学校

结构可以借，内容必须换。至少替换：

- `assets/word-templates/` 的模板与 `assets/course-schedule-*.png`
- `config/template_fields.yaml` 的封面字段、节标题、分值
- `references/course-profile.md` 的课程映射与资料角色
- `references/experiments/` 的实验卡片与教师公式表格位置
- `config/naming.yaml` 的交付命名
- `references/writing-policy.md` 中与本课程冲突的表达偏好

## License 与素材归属

代码与文档采用 [MIT](LICENSE)。`assets/word-templates/` 与 `assets/course-schedule-2026.png` 是课程材料，仅本人学习使用，不随 MIT 许可对外再分发；来源与边界见 [`assets/ASSETS.md`](assets/ASSETS.md)。课程方要求撤下时，删掉对应文件即可，不影响其余内容。