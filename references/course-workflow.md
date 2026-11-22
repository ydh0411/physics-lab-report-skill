# 全流程与任务模式

本文件是操作流程：四种任务模式、七阶段流程、各阶段验收、缺失材料处理。规则的详细内容在各自文件里，本文件只负责顺序与门槛。

- 写作与表达要求：[references/writing-policy.md](writing-policy.md)
- 计算、字体、排版与 PDF 检查：[references/calculation-layout-qa.md](calculation-layout-qa.md)
- 课程资料、模板结构与实验映射：[references/course-profile.md](course-profile.md)
- 按实验全名选卡片：[references/experiment-index.md](experiment-index.md)

## 1. 四种任务模式

先判任务类型，范围不同，产物不同。

| 模式 | 何时用 | 输入 | 产出 |
|---|---|---|---|
| A 首次设置 | 新学期、换电脑、换模板 | 三份当次模板、个人信息、命名规则 | 填好的 `config/*.yaml`、套用当次模板的报告副本 |
| B 新建或重算 | 新报告；或数据/公式有变要重算 | 实验全名、报告类型、当次数据、教师公式表格 | 可编辑 DOCX + 对应 PDF |
| C 修订或纯格式 | 已有报告改内容 / 只改字体排版 | 现有报告、改动要求（内容或格式） | 更新后的 DOCX + PDF，内容与改动范围一致 |
| D 只读检查 | 「能不能提交」 | 现有报告，必要时当次模板 | 问题清单与位置，不改稿 |

典型误判：把「只改字体」当成「重写重算」会悄悄换掉数据；把「只读检查」当成「顺手改稿」会让用户失去对照版本。

## 2. 七阶段流程

### 阶段 ①：确认任务

- 判模式（A/B/C/D）。
- 确认报告类型：prelab / 短报告 / 长报告。
- 确认交付：DOCX、PDF，或只出问题清单。
- C 模式先记录改动前的正文、数据、公式、图片、日期、签名；D 模式明确「不改稿」。

验收：能一句话说清「改什么、不改什么、交付什么」。

### 阶段 ②：定位实验与材料

- 用**实验英文全名**匹配实验卡片与教师材料；编号只用于封面和文件名。
- 读当次模板（第 4.1 节快照仅作核对，实际以文件为准）与教师公式表格。
- 编号与全名冲突时以全名为准，并在交付时说明。
- 需要时看对应学长报告，只用于核对题目覆盖、计算展开组织与版面密度。

验收：说得出用的是哪份模板、哪份公式表格、哪张卡片；数据版本已确认。

### 阶段 ③：确认数据

- 让用户以表格形式提供或确认本次实测数据。
- 扫描件、照片、OCR 结果先转写成表，逐值请用户确认；小数点、单位、角度、行错位是常见错处。
- 未确认前不计算、不写结论。

验收：用户确认过数据表（或明确「先留空」）。

### 阶段 ④：计算与表格

- 按教师文件的公式结构、符号、计算顺序做「公式 → 带单位代入 → 结果 → 不确定度/误差/拟合」四步链。
- 表格保留列、表头单位与合并关系；按当次要求调整组数；补全可计算的派生栏。
- 细节与判定见 [references/calculation-layout-qa.md](calculation-layout-qa.md)。

验收：每个结果都能从原始记录一路追到结果表；简化过程保留、全部要求的结果都在。

### 阶段 ⑤：写各节

- Prelab 按题号逐题作答，不复述题目，不写「本报告将回答」。
- 短报告：Abstract（约 100 词）、Calculations and Results、Conclusions（约 100 词）、Answers to Postlab Questions、数据扫描附录。
- 长报告：Abstract、Introduction、Experimental Procedure、Results、Discussion（>150 词）、Conclusions（约 50 词）、References、Answers to Questions、Appendix（Calculations）、数据扫描附录。
- 不增不减章节；不因为「简洁」删必答题；不给 prelab 拼通用论文式背景与结论。
- Prelab 与短报告不加 References、不放文内引用编号；长报告保留真实、核验过的 References。

验收：模板每节都有实质内容，字数符合模板要求。

### 阶段 ⑥：写作关卡（不可跳过）

按顺序做完三件事，缺一件不算过：

1. **内容通读**：每问是否答到；每段职责是否单一（方法/结果/讨论/结论）；论述链「为什么做→公式（先意后式）→代入→结果→比较」是否完整；详略与时态是否符合模板；原始表、计算链、图表、摘要、结论及问答引用数值是否全篇一致。
2. **表达通读**：按 [references/writing-policy.md](writing-policy.md) 逐类删改——去 AI 味（`AI-1`～`AI-10`）与去防御性语言（`DEF-1`～`DEF-6`）；保留允许项（`OK-1`～`OK-3`），已清晰的句子原样保留。
3. **机器复核**：

```bash
python3 scripts/lint_writing.py 报告.docx            # 默认 --max 0，命中即退出 1
python3 scripts/lint_writing.py 报告.docx --json     # 结构化结果
python3 scripts/lint_writing.py --list-rule          # 规则 id 与判定要点
```

命中规则 id 时按 writing-policy 对应小节逐条改；确认要保留的句子（如 `OK-1` 的一层限定、`OK-2` 的真实假设）明确说明理由，不为了清零而删掉物理内容。

验收：内容通读与表达通读都做过；lint 无未处理命中；数据与结论在两轮中未被改动。

### 阶段 ⑦：排版、导出与核对

1. `python3 scripts/check_docx.py 报告.docx`：字体统计、非 TNR/宋体 run、OMML 公式数、节标题、评分框数、页边距。
2. Word「另存为 PDF」（嵌入字体）。LibreOffice 导出只用于看版式：它会把 Times New Roman 替换成 Liberation Serif，不能作为提交版。
3. `bash scripts/check_pdf_fonts.sh 报告.pdf`：PDF 实际字体；报 Liberation/Carlito 说明用了 LibreOffice，报 Cambria Math 说明公式字体被替换。
4. 逐页看 PDF：封面与正文信息、边框、水印、评分框、断页、公式符号、签名位置、页码、异常空白。
5. 按 `config/naming.example.yaml` 的规则命名 DOCX 与 PDF，两者同基名。

验收：结构检查无异常项、字体检查通过、PDF 每页都看过；没做成的项目明确说明。

## 3. 缺失材料处理

| 缺什么 | 怎么做 |
|---|---|
| 当次教师模板 | 用 `assets/word-templates/` 内置 2026 三份起草，并说明用的是哪份；请用户提供当次版本 |
| 原始数据 | 只出空表或骨架，不填示例值、不写结论、不在摘要里声称一致性 |
| 教师公式表格 | 用实验卡片并提示「教师公式可能不同」；不自创处理流程 |
| 题目 | 留占位或问用户，不编题 |
| 扫描不清 | 给草稿转写并逐值请用户确认 |
| 教师签名 | 仅在用户明确授权时沿用已有签名图，置于数据附录右下角；prelab 不自动加签名 |
| 参考报告（学长） | 只用本仓库卡片与教材；不假装核对过学长报告 |

## 4. 更新模式（A 的一种）

稳定信息变化时更新配置与参考资料，不动报告正文：

- 模板换版：替换 `assets/word-templates/`，同步核对 `config/template_fields.yaml` 的节标题、分值、字数；旧报告的修改要基于新模板重新迁移。
- 换教师/助教、换班级：改 `config/student_profile.yaml`。
- 命名规则变化：改 `config/naming.yaml`，已交付文件不追改文件名。
- 新实验或编号变化：更新 `references/experiment-index.md` 与对应卡片，不按旧编号推内容。
- 教师公式表格变化：以新文件为准，旧卡片只作参考并注明可能过期。

## 5. 审计模式（D 的一种）

只检查、不改稿，按严重程度排序报告：

1. **数据与伪造风险**：无法追溯到原始记录的数值、补造的读数、被改到接近理论值的记录。
2. **公式与计算**：公式结构、符号、代入、单位、取位、结果一致性错误。
3. **模板不符**：缺节、分值区被改、封面/页眉字段缺失、字数不达要求。
4. **导出与字体**：字体回退、公式变图片、PDF 未嵌入、断页与空白页。
5. **表达与风格**：AI 味与防御性语言、术语不一致、过程旁白（按规则 id 给位置）。

每条给出位置（节/表/图/页）与依据；不把「风格建议」写成「必须修改」，也不在只读任务里动文件。

## 6. LaTeX 遗留路径

`templates/prelab_template.tex`、`templates/postlab_template.tex` 与 `scripts/build_report.sh` 是早期 LaTeX 方案，当前课程（2026 Physical Experiment II）用 Word 模板，不使用这条路径。

仅当课程或用户明确要求 LaTeX 时：

```bash
bash scripts/build_report.sh report.tex "final_submission_name.pdf"          # 拒绝覆盖已有 PDF
bash scripts/build_report.sh --force report.tex "final_submission_name.pdf"  # 确认后可覆盖
```

脚本连续编译两遍、在临时目录清理辅助文件、不污染报告目录；封面 PDF 需自备（不随仓库分发）。说明见 [templates/README.md](../templates/README.md)。不要用 LaTeX 版本覆盖现有 Word 报告。