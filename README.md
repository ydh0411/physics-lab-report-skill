<p align="center">
  <img src="https://img.shields.io/badge/LaTeX-XeLaTeX-008080?style=for-the-badge&logo=latex" alt="XeLaTeX">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
  <img src="https://img.shields.io/badge/UESTC-Glasgow%20College-005bac?style=for-the-badge" alt="UESTC">
  <img src="https://img.shields.io/badge/Platform-Claude%20Code%20%7C%20Codex-blueviolet?style=for-the-badge" alt="Platform">
</p>

<h1 align="center">Physics Lab Report Skill</h1>
<h3 align="center">大学物理实验 LaTeX 报告生成器</h3>

<p align="center">
  <b>电子科技大学格拉斯哥学院</b> · UESTC Physics Experiments I & II<br>
  对话式生成预习报告 & 正式报告 · 支持 Claude Code / Codex / 兼容代理
</p>

---

## 目录

- [学生使用流程](#学生使用流程)
- [功能概览](#功能概览)
- [安装](#安装)
- [使用示例](#使用示例)
- [审计工作流](#审计工作流)
- [仓库结构](#仓库结构)
- [设计原则](#设计原则)
- [适配其他学校](#适配其他学校)
- [FAQ](#faq)

---

## 学生使用流程

> **一句话：** 首次设置填一次信息 → 每次报告输入实验标题和数据 → 生成 PDF 直接提交。

### 首次设置

*每学期只做一次。*

| 步骤 | 操作 |
|:---:|---|
| 1 | 放入封面模板 PDF（`01-Template for Prelab work-2026*.pdf` / `02-Template for lab report-2026*.pdf`） |
| 2 | 复制 `config/student_profile.example.yaml` → `student_profile.yaml`，填写个人信息 |
| 3 | 复制 `config/naming.example.yaml` → `naming.yaml`，设置 PDF 提交命名格式 |
| 4 | 确认课程/教材版本 |

### 每次报告

| 步骤 | 操作 | 必需 |
|:---:|------|:---:|
| 1 | 选择 **prelab**（预习）或 **postlab**（正式） | 是 |
| 2 | 输入完整实验标题（如 Polarization of Light / 偏振光） | 是 |
| 3 | 输入 lab 编号（仅用于封面和文件名） | 是 |
| 4 | 手动输入实验原始数据 | 推荐 |
| 5 | 上传教师特殊公式/数据处理模板 | 视情况 |
| 6 | 上传已完成签名的扫描数据表 | 视情况 |
| 7 | 生成最终 PDF | — |

> Skill 自动加载已保存的模板、个人信息和命名规则。**数据输入优先手动**，OCR 仅作备选。

### 更新配置

模板更换、个人信息变动、命名规则调整、课程版本更新时，修改对应 config 文件或重新上传模板即可。

---

## 功能概览

<table>
<tr>
<td width="50%">

#### 预习报告
`\includepdf` 插入封面 → 绝对坐标叠加层（学号/邮箱/日期/计分框）→ 预习题答案枚举

#### 正式报告
封面 → 摘要(5分) → 计算与数据表格(15分) → 结论(10分) → 课后题(10分) → 原始数据附录

</td>
<td width="50%">

#### 一键编译
`build_report.sh`：检查 XeLaTeX → 编译两遍 → 清理辅助文件 → 重命名输出 PDF

#### 自动计分框
`\labsection{标题}{分值}` 自动为每节生成左侧评分框，与教师评分表一致

</td>
</tr>
<tr>
<td>

#### 数据表格
`\datatable{标题}{说明}` 统一格式，支持 `\small` ~ `\scriptsize` 多级缩放

</td>
<td>

#### 对角水印
"Physics Lab 2026"（预报告，单数） / "Physics Labs 2026"（正式报告，复数）

</td>
</tr>
<tr>
<td>

#### 间距 & 字体
标准/紧凑两套间距参数 · Times New Roman / Calibri 两种字体策略 · macOS 自动降级 Arial

</td>
<td>

#### 不确定度 & 误差
Type-A/Type-B 不确定度传递，仪器分辨率、读数误差、主要误差源分析

</td>
</tr>
</table>

---

## 安装

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

安装后重启代理。更新：`cd ~/.claude/skills/physics-lab-report && git pull`

---

## 使用示例

直接对话即可，无需显式调用。典型 prompt：

| 场景 | 对话 |
|------|------|
| 预习报告 | "帮我生成 lab5 偏振光的预习报告" |
| 正式报告 | "根据这份数据扫描件生成正式实验报告" |
| 分步确认 | "先整理数据表让我确认，再继续写报告" |
| 自定义样式 | "用紧凑间距模板，表格字体用 Calibri" |
| 完整审计 | "完整审计我的报告，对照学校模板、实验书和原始数据" |

编译 PDF：

```bash
scripts/build_report.sh report.tex "大物实验I-格院-2024XXXXXXXX-张三-lab5-post.pdf"
```

> 也可上传到 Overleaf，编译器切换为 XeLaTeX。

---

## 审计工作流

> 目标：检查报告或 skill 规则是否与课程材料一致。

| 步骤 | 内容 |
|:---:|---|
| 1 | 确认 `labN` 与实际实验编号/标题的对应关系（二者不一定一致，标题为主键） |
| 2 | 阅读学校 PDF/DOCX 模板，确认封面字段、分区标题、分值 |
| 3 | 阅读实验书/数据表模板，确认公式、表格和习题 |
| 4 | 阅读学生 PDF 与 TeX 源文件，检查结构、公式、单位、有效数字 |
| 5 | 逐项核对报告数值与原始扫描数据 |
| 6 | 学长报告仅作风格参考，旧模板分值不覆盖当前要求 |
| 7 | 干净目录中复制依赖重新编译，验证可复现性 |

---

## 仓库结构

```
physics-lab-report-skill/
├── SKILL.md                           # Skill 定义（编译、模板、字体、审计规则）
├── README.md
├── LICENSE                            # MIT
├── .gitignore
├── config/
│   ├── student_profile.example.yaml   # 学生信息模板
│   └── naming.example.yaml            # PDF 命名规则模板
├── scripts/
│   └── build_report.sh                # PDF 一键编译脚本
├── references/
│   └── experiments/                   # 实验知识库扩展点（按标题索引）
└── templates/
    ├── prelab_template.tex            # 预习报告 LaTeX 模板
    └── postlab_template.tex           # 正式报告 LaTeX 模板
```

---

## 设计原则

| 原则 | 说明 |
|------|------|
| 数据溯源 | 所有数值来自原始扫描数据或仪器规格，绝不编造 |
| 缺材料降级 | 缺模板 → 仅生成草稿；缺数据 → 不生成报告；缺题目 → 留占位符（详见 SKILL.md） |
| 签名处理 | 学生手填数据表 → 教师签字 → 扫描 → skill 附加到附录，不自动放置签名 |
| 公式灵活 | 课本公式 > 教师模板 > 复用已保存模板，三种来源自动适配 |
| 封面插入 | `\includepdf` 插入学校 PDF 模板，不在 LaTeX 中重绘 |
| 手动优先 | 数据输入优先手动，OCR 仅为备选，计算前所有值需用户确认 |

---

## 适配其他学校

核心结构通用，修改以下内容即可：

| 修改项 | 位置 |
|--------|------|
| 封面模板文件名 | `\CoverPDF` |
| 叠加层坐标与文字 | `\PrelabPageForeground` |
| 分区名称与分值 | `\labsection` 调用处 |
| 水印文字 | 模板末尾 |

---

## FAQ

<details open>
<summary><b>为什么必须用 XeLaTeX？</b></summary>

模板使用 `fontspec` 加载系统字体（Times New Roman / Calibri），pdfLaTeX 不支持。
</details>

<details>
<summary><b>Mac 上 Calibri 显示为 Arial？</b></summary>

视觉差异极小。安装了 Office 的 Mac 会自动使用 Calibri。
</details>

<details>
<summary><b>预习报告叠加层错位？</b></summary>

不要修改 `\setlength{\unitlength}{1pt}` 和 geometry。更换封面模板后，微调 `\PrelabPageForeground` 坐标即可。
</details>

<details>
<summary><b>能用 Overleaf 吗？</b></summary>

可以，编译器切换为 XeLaTeX，封面模板 PDF 一并上传。
</details>

---

<p align="center">
  <sub>MIT License · <a href="https://github.com/ydh0411/physics-lab-report-skill">GitHub</a> · Made for UESTC Glasgow College</sub>
</p>
