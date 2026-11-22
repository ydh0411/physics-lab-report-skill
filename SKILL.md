---
name: physics-lab-report
description: Use when preparing, revising, auditing, formatting, or compiling UESTC Glasgow College physics experiment reports (Physical Experiment I/II) — prelab 预习报告, short postlab 短报告, long lab report 长报告, 大物实验报告, 数据处理, Word/DOCX or legacy LaTeX templates, OMML equations, scanned-data appendices, font/PDF checks, or removing AI/defensive prose.
---

# UESTC 大物实验报告

交付符合当次教师 Word 模板的英文报告：题目答完整、计算可复核、语言自然不防御、Word 可编辑、PDF 排版与字体经过实际检查。

本 skill 是本人课程规范，不是通用物理论文写作流程。默认选择来自已完成报告和本学期课程要求；当次教师通知、模板与用户新要求优先于本文件。

适用：Physical Experiment I/II 的预习报告、短报告、长报告，以及既有报告的修订、纯格式调整、只读提交检查。不适用：其他学校课程、科研论文、与实验报告无关的写作。需要适配别的学校时按 `README.md` 的「适配别的学校」逐项替换。

## 动笔前的三份材料

1. **当次教师模板**：默认用 `assets/word-templates/` 内置的 2026 三份；用户提供更新版本时以用户版本为准。
2. **当次教师公式与数据表格**：本地课程文件夹里按实验全名匹配的 `Calculations for Lab-*.docx`、`Data tables.docx`。这是公式结构和表格列关系的来源。
3. **本次实测数据**：用户最新提供或确认的记录。扫描件只作草稿，逐值确认后才计算。

缺任何一份时，按「缺失材料处理」执行，不编造。

## 按任务读取

只读当前决策需要的文件。

| 需要 | 读 |
|---|---|
| 第一次接手、定位课程资料、模板结构、编号与报告类型映射 | [课程与文件地图](references/course-profile.md) |
| 七阶段流程、四种任务模式、各阶段验收与写作关卡 | [全流程](references/course-workflow.md) |
| 写作与表达：去 AI 味、去防御性语言、字数、两轮通读、自查清单 | [写作规则](references/writing-policy.md) |
| 计算链、表格、字体、原生公式、版式、PDF 检查 | [计算、排版与检查](references/calculation-layout-qa.md) |
| 按实验全名选卡片、编号冲突 | [实验索引](references/experiment-index.md) |
| 某实验的表格、公式清单与常见错误 | 匹配的 `references/experiments/*.md` |
| 安装、换电脑、第一次配置 | [`INSTALL.md`](INSTALL.md) |

## 三类报告

| 类型 | 内容骨架 | 分值 | 引用 |
|---|---|---|---|
| Prelab | 封面；Answers to Questions，按题号逐题回答、必要推导与计算 | 20 | 不加 References，不放文内编号 |
| Short postlab | Abstract（约 100 词）；Calculations and Results；Conclusions（约 100 词）；Answers to Postlab Questions；原始数据扫描附录 | 10 / 15 / 5 / 10 | 不加 References，不放文内编号 |
| Long lab report | Abstract（约 100 词）；Introduction；Experimental Procedure；Results；Discussion（>150 词）；Conclusions（约 50 词）；References；Answers to Questions；Appendix（Calculations）；数据扫描附录 | 3 / 3 / 3 / 2 / 5 / 2 / 1 / 6 / 15 | 保留真实、核验过的 References |

章节标题、字数与分值以当次模板实际内容为准；上表是 2026 三份模板的核验快照。不要用「简洁」删掉必答题、必要计算或长报告必需章节，也不要给 prelab 拼接通用论文式背景、讨论和结论。

## 七阶段流程

每阶段有硬门槛，未过不进下一阶段。细节与四种任务模式的差异见 [全流程](references/course-workflow.md)。

1. **确认任务**：新建 / 重算 / 修订 / 纯格式 / 只读检查。范围不同，产物不同。
2. **定位实验**：用实验英文全名匹配卡片与教师材料；编号只用于封面和文件名。
3. **确认数据**：整理成表格给用户确认；OCR 结果未确认前不算数。
4. **计算**：按教师文件的公式结构、符号、计算顺序做四步链（公式 → 带单位代入 → 结果 → 不确定度/误差/拟合）。
5. **写各节**：按模板骨架填写，不增不减章节。
6. **写作关卡**：内容通读 → 表达通读（去 AI 味、去防御性）→ `python3 scripts/lint_writing.py <docx>` 清零。三件事都做完才算过。
7. **排版与导出**：`python3 scripts/check_docx.py` → `bash scripts/docx_to_pdf.sh` → `bash scripts/check_pdf_fonts.sh` → 逐页看 PDF。

## 写作门槛（摘要）

规则全文、可判定清单与英文 before→after 例句见 [写作规则](references/writing-policy.md)。这里只列不可让步的部分。

- **直接讲物理**：测量对象、处理方法、结果、单位、解释。不写「本报告将…」式开场，不写模板/表格/教材章节来源声明。
- **去 AI 味**：删浮夸形容词、空泛意义、机械三段式、同义词轮换、无信息承诺、为对称而排比、每段强行过渡、破折号（`—`）打断、句末空洞 `-ing` 拔高。
- **去防御性**：删假想反驳、重复限定堆叠（`might potentially suggest`）、自我辩护与免责（`To ensure rigor`、`avoid misunderstanding`）、第三人称论文旁白、有效数字与不确定度规则的教学式解释。
- **保留真实边界**：影响结论的假设（如忽略浮力）在相关位置说明一次；确有不确定时用一层 `may` / `suggests`；异常数据、量程限制和不理想结果照实写。
- **克制润色与完整链路**：已清楚自然的句子原样保留，不为换词而改；必要推导、计算链、跨章节数字一致性和解释不可省略。
- **连续性自行判定**：lint 只查词句模式，不判物理正确性、时态与跨节数值对账；内容通读与表达通读不可省。

## 计算与排版硬规则（摘要）

- 每项计算四步：公式 → 带单位数值代入 → 结果数值与单位 → 不确定度/相对误差/拟合的公式、输入与结果。中间保留保护位，最终按课程规则取位并末位对齐。
- 表格保留教师文件的列、表头单位与合并关系；按当次要求删多余空白组（如 Lab9 只测 5 组）；正文与附录补全能由已有记录算出的平均值等派生栏。
- 英文正文、表格、页眉页脚、公式中的拉丁字母与数字：Times New Roman；中文封面信息：宋体/SimSun；变量斜体、数值单位函数正体；公式用原生可编辑 OMML，不做成图片。
- 保留模板原生边框、logo、水印、评分框、分节、页眉页脚、页码域；不要重画封面；正文连续分页，避免每项计算单独一页。
- Docx 里写了字体名不等于 PDF 用了该字体：Word 可能把数学字母换成 Cambria Math，LibreOffice 缺字体时回退 Liberation。必须查 PDF 实际字体并逐页看版式。

详细做法见 [计算、排版与检查](references/calculation-layout-qa.md)。

## 缺失材料处理

| 缺什么 | 怎么做 |
|---|---|
| 当次模板 | 用内置 2026 模板起草，并明确说明用的是哪份；请用户提供当次版本 |
| 原始数据 | 只出空表或骨架，不填示例值、不写结论 |
| 公式表格 | 用实验卡片并提示「教师公式可能不同」；不要自创处理流程 |
| 题目 | 留占位或问用户，不编题 |
| 扫描不清 | 给草稿转写并逐值请用户确认 |
| 教师签名 | 仅在用户明确授权时沿用已有签名图；prelab 不自动加签名 |

## 任务边界

- 「能不能提交」默认只检查不改稿；改稿需明确要求。
- 「只改字体/格式」不动正文、数据、公式表达式、图片、日期、签名。先记录再改，改后比对。
- 不因偏离理论值调整原始记录；有依据的录入或计算错误可改，并把改动和依据告诉用户。
- 学长报告只用于核对题目覆盖、结构、计算展开和版面密度；不复制数据、不沿用错误公式、不按旧编号套用。
- 旧制作脚本和旧预览稿可能含过期数据，不作为数据真源；不重建覆盖用户当前报告。
- 不删除或改写用户现有报告、原始记录、模板和参考资料。

## 完成标准

- 逐题核对：每问都有回答，且对应本次教材/教师问题。
- 数值核对：原始记录 → 差值/平均值 → 公式代入 → 结果表 → 摘要与结论，各处一致。
- 表达核对：两轮通读完成；`scripts/lint_writing.py` 无命中或命中已逐条处理并说明。
- 版式核对：`check_docx.py` 无异常；PDF 逐页看过；`check_pdf_fonts.sh` 字体合规。
- 明确说明尚未完成的项目（未渲染、未核实数据、缺签名等），不用「应该没问题」代替检查。
- 交付可编辑 DOCX 与对应 PDF，命名见 [课程与文件地图](references/course-profile.md) 与 `config/naming.example.yaml`。

## 本地配置

个人信息、命名规则、模板字段映射复制 `config/*.example.yaml` 为同目录下的 `.yaml` 后填写；填写后的文件被 `.gitignore` 排除，不进公开仓库。

## 遗留 LaTeX 路径

`templates/prelab_template.tex`、`templates/postlab_template.tex` 与 `scripts/build_report.sh` 是历史 LaTeX 方案，当前课程不用。仅当课程或用户明确要求 LaTeX 时使用，说明见 [`templates/README.md`](templates/README.md)。不要用 LaTeX 模板改写或覆盖现有 Word 报告。