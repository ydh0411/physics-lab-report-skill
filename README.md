# Physics Lab Report — Claude Code Skill

使用 XeLaTeX 生成大学物理实验报告（预习报告 + 实验报告）。包含封面插入、计分框分区、数据表格格式化、不确定度传递、原始数据附录等完整模板。

## 效果概览

| 预习报告 | 实验报告 |
|---------|---------|
| 封面 PDF → 叠加层（学号/邮箱/日期/计分框）→ 预习题答案 | 封面 PDF → 摘要 → 计算与数据表格 → 结论 → 课后题 → 附录（扫描数据） |
| "Physics Lab 2026" 水印（单数） | "Physics Labs 2026" 水印（复数） |

## 环境要求

- **XeLaTeX**（不能用 pdfLaTeX）—— 模板使用 `fontspec` 加载 Times New Roman / Calibri 系统字体
- LaTeX 宏包：`pdfpages`、`fontspec`、`newtxmath`、`amsmath`、`tikz`、`eso-pic`、`fancyhdr`、`enumitem`、`setspace`、`booktabs`、`caption`
- Python 3 + `pypdf` + `matplotlib`（可选，用于数据提取和图表生成）
- 学校提供的封面模板 PDF（如 UESTC 的 `01-Template for Prelab work-2026*.pdf` 和 `02-Template for lab report-2026*.pdf`）

### macOS 字体说明

macOS 不自带 Calibri，模板默认用 **Arial** 替代，视觉差异很小。Windows 用户安装 Microsoft Office 后自带 Calibri，无需额外配置。

## 安装

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/你的用户名/physics-lab-report.git ~/.claude/skills/physics-lab-report
```

克隆完成后重启 Claude Code 即可自动加载。也可以直接放到项目目录的 `.claude/skills/` 下。

### Codex

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/你的用户名/physics-lab-report.git ~/.agents/skills/physics-lab-report
```

克隆完成后重启 Codex 即可自动加载。

### 手动安装

直接将 `SKILL.md` 和 `templates/` 文件夹拷贝到你的 skills 目录即可，无需 git clone。

## 快速上手

### 1. 生成预习报告

```bash
cp ~/.claude/skills/physics-lab-report/templates/prelab_template.tex ./labN_pre.tex
```

编辑 `labN_pre.tex`：
- 填写 `\StudentNumber`、`\StudentEmail`、`\ReportDate`
- 设置 `\CoverPDF` 为封面模板文件名
- 在 `\PrelabAnswerBody` 里写入预习题答案

```bash
xelatex -interaction=nonstopmode labN_pre.tex
xelatex -interaction=nonstopmode labN_pre.tex   # 两遍编译
```

### 2. 生成实验报告

```bash
cp ~/.claude/skills/physics-lab-report/templates/postlab_template.tex ./labN_post.tex
```

编辑 `labN_post.tex`：
- 填写个人信息
- 设置 `\CoverPDF` 和 `\DataPDF`（原始数据扫描件）
- 填写四个部分：摘要、计算与结果、结论、课后题答案
- 附录自动引用 `\DataPDF`

```bash
xelatex -interaction=nonstopmode labN_post.tex
xelatex -interaction=nonstopmode labN_post.tex
```

### 3. 直接让 Claude 帮你写

安装 skill 后，直接对话即可：

> "帮我生成 lab5 偏振光的预习报告，数据表 PDF 在这里"

Claude 会自动加载 skill、使用模板、生成 `.tex` 文件。

## 文件结构

```
physics-lab-report/
├── SKILL.md                          # Skill 定义（Claude Code 加载此文件）
├── README.md                         # 本文件
├── LICENSE                           # MIT
└── templates/
    ├── prelab_template.tex           # 预习报告 LaTeX 模板
    └── postlab_template.tex          # 实验报告 LaTeX 模板
```

## 核心特性

- **真实数据** —— 所有数值必须来自原始数据扫描件或仪器规格，绝不编造
- **封面用 `\includepdf` 插入** —— 不在 LaTeX 里重绘封面，直接插入学校提供的模板 PDF
- **每节带计分框** —— 与教师评分表的格式一致
- **不确定度传递** —— A 类（统计）+ B 类（仪器+读数，矩形分布除以 √3），合并给出最终结果
- **原始数据附录** —— 手写数据扫描件放在报告末尾
- **两种字体策略** —— 全 Times New Roman 简洁风格，或 Calibri 表格匹配 Word 模板
- **标准/紧凑两套间距** —— 根据报告篇幅选择

## 适配其他学校

模板基于 UESTC 大学物理实验 I 构建，但核心模式通用：

1. **换封面**：修改 `\CoverPDF` 为你学校的模板文件名
2. **换头部信息**：编辑 `\PrelabPageForeground` 里的叠加坐标和文字
3. **换分区名称/分值**：修改 postlab 模板中的 `\labsection` 调用
4. **换水印文字**：在模板中搜索 `Physics Lab` 替换

计分框、数据表格、不确定度传递、水印、附录这些基础结构适用于任何使用 LaTeX 的物理实验课程。

## 常见问题

**Q: 为什么必须用 XeLaTeX？**
A: 模板用 `fontspec` 加载 Times New Roman / Calibri 系统字体，pdfLaTeX 不支持。`iftex` 宏包会在用错编译器时给出警告。

**Q: Mac 上 Calibri 显示为 Arial，有问题吗？**
A: 没问题。视觉差异很小。如果你装了 Microsoft Office，模板会自动使用 Calibri。

**Q: 预习报告叠加层位置不对怎么办？**
A: 不要改 `\setlength{\unitlength}{1pt}` 和 geometry 设置。如果换了封面模板 PDF，需要微调 `\PrelabPageForeground` 里的叠加坐标（单位是 pt，原点在左下角）。

**Q: 能用 Overleaf 吗？**
A: 可以，但需要把编译器切换为 XeLaTeX（Menu → Compiler → XeLaTeX），并把封面模板 PDF 一起上传。

## 许可证

MIT — 详见 [LICENSE](LICENSE)。
