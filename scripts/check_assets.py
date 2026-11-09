#!/usr/bin/env python3
"""校验仓库素材与文档链接。

检查项：
1. `assets/word-templates/` 三份 2026 Word 模板存在，且能用 python-docx 打开；
   节标题包含模板快照中的关键短语，评分框数量与快照一致。
2. `assets/course-schedule-2026.png` 存在且非空。
3. 仓库内 Markdown 的相对链接（含图片）都能解析到真实文件。
4. 文本文件中不出现本机绝对路径 `/Users/` 或个人隐私残留。

用法：
    python3 scripts/check_assets.py            # 全量检查
    python3 scripts/check_assets.py --no-docx  # 跳过 DOCX 深检（缺 python-docx 时自动跳过）

退出码：0 = 通过；1 = 有失败项；3 = 缺 python-docx 且未指定 --no-docx（其余检查仍执行）。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WORD_TEMPLATES = {
    "prelab": {
        "path": "assets/word-templates/01-Template for Prelab work-Physical Experiment 2-2026.docx",
        "headings": ["Answers to Questions (20 points)"],
        "score_boxes": 1,
    },
    "short_report": {
        "path": "assets/word-templates/02-Template for short lab report-Physical Experiment 2-2026.docx",
        "headings": [
            "Abstract (About 100 words, 10 points)",
            "Calculations and Results",
            "Conclusions (About 100 words, 5 points)",
            "Answers to Postlab Questions (10 points)",
        ],
        "score_boxes": 4,
    },
    "long_report": {
        "path": "assets/word-templates/03-Template for long lab report-Physical Experiment 2-2026.docx",
        "headings": [
            "Abstract (About 100 words, 3 points)",
            "Introduction (3 points)",
            "Experimental Procedure",
            "Results (Data tables and figures, 2 points)",
            "Discussion (More than 150 words, 5 points)",
            "Conclusions (About 50 words, 2 points)",
            "References (1 points)",
            "Answers to Questions (6 points)",
            "Appendix",
        ],
        "score_boxes": 9,
    },
}

SCHEDULE = "assets/course-schedule-2026.png"

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".sh", ".txt"}
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", "build", "out", "cache"}
FORBIDDEN_TEXT = ["/Users/", "/home/", "C:\\Users\\"]

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.S)


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.notes: list[str] = []

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


def iter_files(suffixes: set[str]):
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts[:-1]):
            continue
        if path.suffix.lower() in suffixes:
            yield path


def check_word_templates(report: Report, deep: bool) -> None:
    try:
        from docx import Document  # noqa: PLC0415
    except ImportError:
        report.fail("缺少 python-docx，无法检查 DOCX 模板结构（pip install python-docx）")
        return

    for name, spec in WORD_TEMPLATES.items():
        path = ROOT / spec["path"]
        if not path.is_file():
            report.fail(f"[{name}] 模板不存在：{spec['path']}")
            continue
        try:
            document = Document(path)
        except Exception as exc:  # noqa: BLE001
            report.fail(f"[{name}] 无法打开：{exc}")
            continue

        texts = [p.text.strip() for p in document.paragraphs]
        all_text = "\n".join(texts)
        for heading in spec["headings"]:
            if heading not in all_text:
                report.fail(f"[{name}] 缺少节标题：{heading}")

        score_boxes = sum(
            1
            for table in document.tables
            if table.rows and table.rows[0].cells and "Score" in table.rows[0].cells[0].text
        )
        if score_boxes != spec["score_boxes"]:
            report.fail(
                f"[{name}] 评分框数量 {score_boxes}，快照为 {spec['score_boxes']}"
            )

        report.note(f"[{name}] OK：{len(document.paragraphs)} 段、{score_boxes} 个评分框")


def check_schedule(report: Report) -> None:
    path = ROOT / SCHEDULE
    if not path.is_file() or path.stat().st_size == 0:
        report.fail(f"缺失或为空：{SCHEDULE}")


def check_links(report: Report) -> None:
    for path in iter_files({".md"}):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            report.fail(f"无法按 UTF-8 读取：{path.relative_to(ROOT)}")
            continue
        text = FENCE_RE.sub("", text)
        for target in LINK_RE.findall(text):
            target = target.strip().strip("<>").split(" ")[0]
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                report.fail(f"{path.relative_to(ROOT)} 链接指向仓库外：{target}")
                continue
            if not resolved.exists():
                report.fail(f"{path.relative_to(ROOT)} 链接失效：{target}")


def check_private_paths(report: Report) -> None:
    for path in iter_files(TEXT_SUFFIXES):
        rel = path.relative_to(ROOT)
        if rel.as_posix() == "scripts/check_assets.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for marker in FORBIDDEN_TEXT:
            if marker in text:
                report.fail(f"{rel} 含本机绝对路径残留：{marker}")


def main() -> int:
    parser = argparse.ArgumentParser(description="校验素材、模板结构与 Markdown 相对链接")
    parser.add_argument("--no-docx", action="store_true", help="跳过 DOCX 深度检查")
    args = parser.parse_args()

    report = Report()
    try:
        import docx  # noqa: F401, PLC0415
        have_docx = True
    except ImportError:
        have_docx = False

    if args.no_docx or have_docx:
        if not args.no_docx:
            check_word_templates(report, deep=True)
        else:
            report.note("已按 --no-docx 跳过模板结构检查")
    else:
        report.note("缺少 python-docx：跳过模板结构检查（pip install python-docx 后可启用）")

    check_schedule(report)
    check_links(report)
    check_private_paths(report)

    for line in report.notes:
        print(f"note: {line}")
    if report.failures:
        print("\nFAIL:")
        for line in report.failures:
            print(f"  - {line}")
        return 1

    print("\nPASS: 素材、模板结构与相对链接检查通过")
    if not have_docx and not args.no_docx:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())