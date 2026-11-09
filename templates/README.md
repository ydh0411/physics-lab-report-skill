# LaTeX 遗留模板

这两个文件是早期方案留下的 LaTeX 模板，当前课程（2026 Physical Experiment II）不使用，报告以 `assets/word-templates/` 的 Word 模板为准。

- `prelab_template.tex`：预习报告，`\includepdf` 插入官方封面 PDF，绝对坐标叠加页眉/日期，水印与评分框沿用封面 PDF。
- `postlab_template.tex`：正式报告，含分值区、数据表、附录扫描页。

## 什么时候用

1. 课程或教师明确要求提交 LaTeX/PDF 生成的报告（例如 Physics Experiments I 的旧流程）。
2. 用户明确要求保留原有 `.tex` 工程。

其他情况不要用 LaTeX 重做 Word 报告，也不要用 LaTeX 版本覆盖现有 DOCX。

## 使用方式

模板是金标准，不要为了「整理」重写其中的字体、坐标、水印、评分框设定。复制到报告工作目录后填写内容，用 XeLaTeX 编译：

```bash
bash scripts/build_report.sh report.tex "final_submission_name.pdf"
```

脚本连续编译两遍、在临时目录清理辅助文件、拒绝覆盖已有 PDF；确认要覆盖时显式使用 `--force`。没有本地 TeX 环境时把工程上传 Overleaf，编译器选 XeLaTeX。

模板依赖 `templates/` 中写死的封面 PDF 文件名（`01-Template for Prelab work-2026.pdf`、`02-Template for lab report-2026.pdf`），需要自备对应封面；这些 PDF 不随仓库分发。

CI 的 `scripts/smoke_test.sh` 会用占位 PDF 编译两个模板，验证它们仍然可用。