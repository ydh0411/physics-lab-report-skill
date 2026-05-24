# 大学物理实验 LaTeX 报告 Skill

基于**电子科技大学格拉斯哥学院（UESTC Glasgow College）**大学物理实验 I/II 课程，面向 `Claude Code`、`Codex` 及同类智能编程代理的 skill 仓库，用于根据实验数据和课程要求生成、审计和修订符合规范的 LaTeX 实验报告（预习报告 + 正式报告）。

仓库提供两套 LaTeX 模板：预习报告模板（封面叠加层 + 计分框 + 预习题答案）和正式报告模板（摘要、计算与数据表格、结论、课后题、原始数据附录）。同时提供一套审计流程，用于对照学校模板、实验书、原始数据扫描件和学长参考报告，检查报告或 skill 规则是否可靠。

GitHub 仓库地址：

`https://github.com/ydh0411/physics-lab-report-skill`

## 功能概览

- 预习报告模板：`\includepdf` 插入封面 → 绝对坐标叠加层（学号/邮箱/日期/计分框）→ 预习题答案枚举
- 正式报告模板：封面 → 摘要（5分）→ 计算与数据表格（15分）→ 结论（10分）→ 课后题（10分）→ 扫描原始数据附录
- 报告审计流程：学校 PDF/DOCX 模板 → 实验书/数据表 → 学生 PDF/TeX → 原始扫描数据 → 学长参考 → 可复现编译
- `\labsection` 宏自动为每节生成左侧计分框
- `\datatable` 宏统一数据表标题格式
- "Physics Lab(s) 2026" 对角水印
- 标准间距和紧凑间距两套参数，按报告篇幅切换
- 两种字体策略：全 Times New Roman 简洁风格，或 Calibri 表格风格
- 使用 XeLaTeX 编译，macOS 可用 Arial 替代 Calibri

## 安装方式

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone --depth=1 https://github.com/ydh0411/physics-lab-report-skill.git \
  ~/.claude/skills/physics-lab-report
```

### Codex

```bash
mkdir -p ~/.codex/skills
git clone --depth=1 https://github.com/ydh0411/physics-lab-report-skill.git \
  ~/.codex/skills/physics-lab-report
```

安装后重启代理使其重新发现新 skill。已安装的可进入对应目录执行 `git pull` 更新。

## 使用方式

安装 skill 后，将封面模板 PDF、实验数据扫描件和 `.tex` 模板放在同一工作目录，然后直接对话即可：

- "帮我生成 lab5 偏振光的预习报告"
- "根据这份数据扫描件生成正式实验报告"
- "完整检查我的报告、学长报告、学校模板、实验书和数据，看 skill 有没有问题"
- "先整理数据表让我确认，再继续写报告"
- "用紧凑间距模板，表格字体用 Calibri"

也可以显式调用：

```text
使用 physics-lab-report-skill 生成 LaTeX 实验报告
```

## 用户需要额外提供什么

skill 仓库提供 LaTeX 模板，用户需要在当前工作目录额外放入：

- 学校下发的封面模板 PDF（`01-Template for Prelab work-2026*.pdf` / `02-Template for lab report-2026*.pdf`）
- 实验原始数据扫描件（手写数据表照片或 PDF）
- 学校给的实验数据表/公式模板（如 DOCX/PDF）
- 如有实验指导书、教师补充 PPT 或学长参考报告，一并放入

## 推荐工作流

1. 在一个工作文件夹中放入封面模板、数据扫描件和相关资料
2. 让代理使用本 skill，先识别并展示 `data.tex`，确认数据无误
3. 确认后让代理生成完整 `.tex` 文件
4. 用 XeLaTeX 编译两遍：`xelatex -interaction=nonstopmode file.tex`
5. 或直接上传到 Overleaf（切换编译器为 XeLaTeX）

## 审计工作流

当目标是检查报告或检查本 skill 是否写对时，按下面顺序读材料：

1. 先确认提交文件名中的 `labN` 和实际实验编号/实验题目，二者不一定一致
2. 读取当前学校 PDF/DOCX 模板，确认封面字段、分区标题、分值和附录要求
3. 读取实验书或学校给的数据表/公式模板，确认必填数据、公式和问题
4. 读取学生已完成的 PDF 和 TeX 源文件，检查结构、公式、单位、有效数字、图表、附录和水印
5. 读取原始扫描数据，逐项核对报告里的数值来源
6. 读取学长报告作为风格和完整度参考，但旧模板分值不能覆盖当前模板
7. 在干净临时目录中复制封面、数据 PDF、图像和签名等依赖，重新编译验证可复现性

## 输出结果通常包含什么

- `report.tex` — 主报告文件
- `data.tex` — 整理后的实验数据表（如适用）
- `figures/` — matplotlib 生成的矢量图（如适用）
- 编译产物 `report.pdf`（本地有 XeLaTeX 工具链时）

## 仓库结构

```text
physics-lab-report-skill/
├── SKILL.md                    # Skill 定义文件
├── README.md                   # 本文件
├── LICENSE                     # MIT
├── .gitignore
└── templates/
    ├── prelab_template.tex     # 预习报告模板
    └── postlab_template.tex    # 正式报告模板
```

## 设计原则

- 所有数值必须来自原始数据扫描件或仪器规格，绝不编造
- 封面通过 `\includepdf` 插入学校模板 PDF，不在 LaTeX 中重绘
- 每节带计分框，与教师评分表格式一致
- 定量测量型实验应包含合适的不确定度传递；验证型或图像拟合型实验至少要说明仪器分辨率、读数误差、拟合/偏差和主要误差源
- 数据识别保守，不能擅自编造、修正或补全模糊数据
- 扫描 PDF 如无法直接抽取文本，应先渲染页面，再 OCR 或人工读图核对
- 封面日期可用 `/` 格式，叠加层日期用 `.` 格式
- 预习报告水印为 "Physics Lab 2026"（单数），正式报告为 "Physics Labs 2026"（复数）

## 适配其他学校

模板基于 UESTC 大学物理实验 I 构建，核心结构通用：

1. 修改 `\CoverPDF` 为你的封面模板文件名
2. 编辑 `\PrelabPageForeground` 中的叠加坐标和文字
3. 修改 `\labsection` 调用中的分区名称和分值
4. 替换模板中的水印文字

计分框、数据表格、不确定度传递、附录结构适用于任何使用 LaTeX 的物理实验课程。

## 常见问题

**为什么必须用 XeLaTeX？** 模板用 `fontspec` 加载 Times New Roman / Calibri 系统字体，pdfLaTeX 不支持。

**Mac 上 Calibri 显示为 Arial？** 视觉差异很小，如有 Office 则自动使用 Calibri。

**预习报告叠加层错位？** 不要改 `\setlength{\unitlength}{1pt}` 和 geometry。如果换了封面模板，需微调 `\PrelabPageForeground` 中的叠加坐标。

**能用 Overleaf 吗？** 可以，编译器切换为 XeLaTeX，封面模板 PDF 一并上传。

## 更新

```bash
cd ~/.claude/skills/physics-lab-report
git pull origin main
```

## License

MIT — 详见 [LICENSE](LICENSE)。
