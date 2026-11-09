# 安装与第一次使用

## 1. 安装

把整个仓库目录放进目标 agent 的 skills 目录，保持 `SKILL.md`、`references/`、`assets/`、`scripts/`、`config/`、`agents/` 的相对结构。

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

### 其他支持 Agent Skills 的 agent

放进其 skills 目录即可（目录名 `physics-lab-report`）。没有技能发现机制的 agent，让它读本目录的 `SKILL.md`，按其中链接按需读 `references/`。

已在用本地旧版（例如 `~/.codex/skills/uestc-physics-lab-report`）时，可以直接用仓库内容替换该目录的 `SKILL.md`、`references/`、`scripts/`、`config/`、`agents/`，并保留目录名不动。

安装或更新后重载技能列表或开新会话。

## 2. 确认运行环境

| 能力 | 用途 | 缺失时 |
|---|---|---|
| Microsoft Word 或 LibreOffice（`soffice`） | DOCX 编辑、导出 PDF | 改用 Word 手工导出，并说明未用脚本导出 |
| `python3` + `python-docx` | `scripts/check_docx.py` 查字体与结构 | 脚本退出码 3，改用人工检查并说明 |
| `poppler`（`pdffonts`） | `scripts/check_pdf_fonts.sh` 查 PDF 实际字体 | 退出码 3，改用 PDF 阅读器字体面板核对 |
| Times New Roman、宋体/SimSun | 报告字体 | 缺字体时版面会回退，必须先装字体再导出 |

## 3. 第一次配置（只做一次）

```bash
cd ~/.codex/skills/physics-lab-report
cp config/student_profile.example.yaml config/student_profile.yaml
cp config/naming.example.yaml        config/naming.yaml
cp config/template_fields.example.yaml config/template_fields.yaml
```

填写 `config/student_profile.yaml` 的姓名、学号、邮箱、学院、专业、班级、教师、助教；确认 `config/naming.yaml` 的交付命名；用当次模板核对 `config/template_fields.yaml` 的分值与节标题。

这三个填好的文件已被 `.gitignore` 排除，不会进公开仓库。

## 4. 验证安装

```bash
python3 scripts/check_assets.py                 # 三份模板可打开、节标题与评分框数量正确、相对链接可解析
python3 scripts/lint_writing.py --list-rule     # 打印去 AI 味/去防御性规则 id
python3 scripts/lint_writing.py tests/fixtures/bad-prose.md   # 期望退出码 1
python3 scripts/lint_writing.py tests/fixtures/good-prose.md  # 期望退出码 0
bash scripts/docx_to_pdf.sh \
  "assets/word-templates/01-Template for Prelab work-Physical Experiment 2-2026.docx" \
  /tmp/prelab-check.pdf                          # 能转换出 PDF，且不写进仓库
```

`check_pdf_fonts.sh` 在有 poppler 时再跑：

```bash
bash scripts/check_pdf_fonts.sh /tmp/prelab-check.pdf
```

## 5. 每次写报告

准备三样东西，然后交给 agent：

1. 实验英文全名与当次提交编号（编号只用于封面和文件名）。
2. 报告类型：prelab / 短报告 / 长报告。
3. 本次实测数据，或已扫描数据表并逐值确认。

示例：

```text
使用 physics-lab-report 完成本次报告。

实验全名：The Franck-Hertz Experiment
本学期编号：Lab8，长报告
数据我下面粘贴，你先整理数据表让我确认，确认后再计算、写作、导出 PDF。
```

缺失材料时按 `SKILL.md` 的「缺失材料处理」办，不编造数据和题目。

## 6. 更新

```bash
cd ~/.codex/skills/physics-lab-report
git pull
```

配置文件和本地报告文件夹不受影响；新模板发布时替换 `assets/word-templates/` 并同步核对 `config/template_fields.yaml`。

## 7. 公开仓库边界

仓库只放：三份课程 Word 模板、实验安排图、实验卡片、规则文档与脚本。不放：教材、教师计算文件与数据表、学长报告、原始测量数据、签名照片、填好的个人信息。个人资料留在本地目录或被 gitignore 的路径。