#!/usr/bin/env python3
"""check_docx.py — UESTC 大物实验 Word 报告的字体与排版自检。

用法:
    python3 scripts/check_docx.py <file.docx> [--strict] [--json]
    python3 scripts/check_docx.py --help

检查项:
    - 字体统计与白名单：拉丁用 Times New Roman，中文用 SimSun / 宋体，符号用 Symbol
    - 字号分布：正文是否出现 < 9pt 的异常小字
    - 原生公式 OMML 数量（公式应是可编辑 OMML，不是图片）
    - 模板节标题是否齐全、顺序是否与模板一致
    - 教师评分框数量（prelab 1 / short 4 / long 9）
    - A4 纸张、页边距、分节数、不同首页页眉
    - 页码域 PAGE 与页眉文字
    - 封面字段（Lab Title / Name / UESTC ID / Instructor / TA / Date / Score）
    - 文档内嵌图片数量

退出码:
    0  通过（无 error；--strict 下也无 warn）
    1  发现 error（或 --strict 下有 warn）
    2  参数用法错误
    3  运行环境或输入不可用（缺 python-docx、文件不存在/不是 docx）

只读输入文件：本脚本不修改 .docx，也不写仓库。
"""

import argparse
import json
import re
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

try:
    import docx  # noqa: F401  (python-docx)
    from docx import Document
    from lxml import etree
except ImportError as exc:  # pragma: no cover - 环境分支
    print(
        "错误：缺少 python-docx（或 lxml）。安装后重试：\n"
        "    python3 -m pip install python-docx\n"
        f"原始错误：{exc}",
        file=sys.stderr,
    )
    sys.exit(3)

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"

# 字体白名单。拉丁：Times New Roman；中文：SimSun / 宋体；符号：Symbol。
LATIN_OK = {"Times New Roman"}
CJK_OK = {"SimSun", "宋体", "NSimSun"}
SYMBOL_OK = {"Symbol"}
KNOWN_WARN_FONTS = {
    "Cambria Math": "Word 常把数学字母换成 Cambria Math，导出 PDF 后必须用 check_pdf_fonts.sh 复核实际字体",
    "Meiryo": "模板残留日文字体，确认不是正文所用",
}

EXPECTED_SCORE_BOXES = {"prelab": 1, "short": 4, "long": 9}
TYPE_LABEL = {"prelab": "Prelab 预习报告", "short": "Short lab report 短报告", "long": "Long lab report 长报告"}

# 节标题：在「加粗的短段落」里按模板措辞匹配，允许 Appendix A/B 等字母编号。
# 正则需要容忍教师/往届报告对标题的小改动（如 "Appendix A Calculations"）。
EXPECTED_TITLES = {
    "prelab": [
        ("Answers to Questions", r"^answers to .*questions\b"),
    ],
    "short": [
        ("Abstract", r"^abstract\b"),
        ("Calculations and Results", r"^calculations and results\b"),
        ("Conclusions", r"^conclusions\b"),
        ("Answers to Postlab Questions", r"^answers to .*questions\b"),
        ("Appendix (Scanned data sheets)", r"^appendix\b.*(scanned data sheets|data sheets)"),
    ],
    "long": [
        ("Abstract", r"^abstract\b"),
        ("Introduction", r"^introduction\b"),
        ("Experimental Procedure", r"^experimental procedure\b"),
        ("Results", r"^results\b"),
        ("Discussion", r"^discussion\b"),
        ("Conclusions", r"^conclusions\b"),
        ("References", r"^references\b"),
        ("Answers to Questions", r"^answers to .*questions\b"),
        ("Appendix (Calculations)", r"^appendix\b.*calculations\b"),
        ("Appendix (Scanned data sheets)", r"^appendix\b.*(scanned data sheets|data sheets)"),
    ],
}

COVER_LABELS = [
    "Lab Title:",
    "Name (in Chinese):",
    "UESTC ID:",
    "Instructor:",
    "Teaching Assistant:",
    "Date:",
    "Score:",
]


def normalize(text: str) -> str:
    """折叠所有空白（含全角空格），用于标题/字段比对。"""
    text = unicodedata.normalize("NFKC", text or "")
    return re.sub(r"\s+", " ", text).strip()


class Report:
    def __init__(self):
        self.findings = []
        self.stats = {}

    def add(self, level, code, message):
        self.findings.append({"level": level, "code": code, "message": message})

    def error(self, code, message):
        self.add("error", code, message)

    def warn(self, code, message):
        self.add("warn", code, message)

    def info(self, code, message):
        self.add("info", code, message)

    def count(self, level):
        return sum(1 for f in self.findings if f["level"] == level)


def short_part_name(part_name: str) -> str:
    base = part_name.rsplit("/", 1)[-1]
    if base == "document.xml":
        return "正文"
    if base.startswith("header"):
        return "页眉"
    if base.startswith("footer"):
        return "页脚"
    return base


def collect_xml_stats(zf):
    """遍历正文/页眉/页脚 XML，统计字体、字号、OMML、图片、域。"""
    parts = ["word/document.xml"] + sorted(
        n for n in zf.namelist() if re.fullmatch(r"word/(header|footer)\d*\.xml", n)
    )
    font_runs = Counter()
    font_chars = Counter()
    font_where = defaultdict(set)
    sizes = Counter()
    small_text_runs = []
    omml = 0
    drawings = 0
    page_field = False
    instr_texts = []

    for part in parts:
        try:
            data = zf.read(part)
        except KeyError:
            continue
        root = etree.fromstring(data)
        where = short_part_name(part)
        for run in root.iter(W + "r", M + "r"):
            rpr = run.find(W + "rPr")
            text = "".join(run.itertext())
            text = text.strip()
            if rpr is None:
                continue
            rfonts = rpr.find(W + "rFonts")
            if rfonts is not None:
                names = {
                    rfonts.get(W + attr)
                    for attr in ("ascii", "hAnsi", "eastAsia", "cs")
                    if rfonts.get(W + attr)
                }
                for name in names:
                    font_runs[name] += 1
                    font_where[name].add(where)
                    if text:
                        font_chars[name] += len(text)
            sz = rpr.find(W + "sz")
            if sz is not None and text:
                try:
                    pt = int(sz.get(W + "val")) / 2.0
                except (TypeError, ValueError):
                    continue
                sizes[pt] += 1
                if pt < 9:
                    small_text_runs.append((where, pt, text[:24]))
        doc_part = part == "word/document.xml"
        if doc_part:
            omml += sum(1 for _ in root.iter(M + "oMath"))
            drawings += len(root.findall(".//" + W + "drawing"))
        else:
            drawings += len(root.findall(".//" + W + "drawing"))
        if where == "页脚":
            for el in root.iter(W + "instrText"):
                if el.text:
                    instr_texts.append(el.text)
                    if re.search(r"\bPAGE\b", el.text):
                        page_field = True
            for el in root.iter(W + "fldSimple"):
                instr = el.get(W + "instr") or ""
                instr_texts.append(instr)
                if re.search(r"\bPAGE\b", instr):
                    page_field = True

    return {
        "font_runs": font_runs,
        "font_chars": font_chars,
        "font_where": font_where,
        "sizes": sizes,
        "small_text_runs": small_text_runs,
        "omml": omml,
        "drawings": drawings,
        "page_field": page_field,
        "instr_texts": instr_texts,
    }


def classify_font(name):
    """返回 (等级, 说明)。等级: ok / warn / error。"""
    if name in LATIN_OK:
        return "ok", "拉丁白名单"
    if name in CJK_OK:
        return "ok", "中文白名单"
    if name in SYMBOL_OK:
        return "ok", "符号白名单"
    if name in KNOWN_WARN_FONTS:
        return "warn", KNOWN_WARN_FONTS[name]
    return "error", "不在白名单（应为 Times New Roman / SimSun / 宋体 / Symbol）"


def detect_report_type(filename, body_text):
    low = filename.lower()
    if "prelab" in low:
        return "prelab", "按文件名"
    if "short" in low:
        return "short", "按文件名"
    if "long" in low:
        return "long", "按文件名"
    text = body_text.lower()
    if "prelab report" in text:
        return "prelab", "按封面标题"
    if "introduction" in text and "discussion" in text:
        return "long", "按节标题"
    if "calculations and results" in text:
        return "short", "按节标题"
    return None, "无法判定"


def paragraph_infos(document):
    """返回非空段落的文本与「是否含加粗文字」。"""
    infos = []
    for par in document.paragraphs:
        text = normalize(par.text)
        if not text:
            continue
        bold = any(bool(run.bold) for run in par.runs if (run.text or "").strip())
        infos.append({"text": text, "bold": bold})
    return infos


def heading_candidates(infos):
    """把 'Appendix' + '(Calculations, …)' 这类两行标题合并成一个候选串。"""
    candidates = []
    for i, info in enumerate(infos):
        merged = info["text"]
        is_bold = info["bold"]
        if i + 1 < len(infos) and infos[i + 1]["text"].startswith(("(", "（")):
            merged = f"{merged} {infos[i + 1]['text']}"
            is_bold = is_bold or infos[i + 1]["bold"]
        candidates.append({"text": merged, "bold": is_bold})
    return candidates


def check_titles(report, infos, report_type):
    if not report_type:
        if infos:
            report.warn("TITLE-TYPE", "无法从文件名或标题判断报告类型，跳过节标题核对")
        return
    candidates = heading_candidates(infos)
    headings = [c for c in candidates if c["bold"]]
    if not headings:
        report.warn(
            "TITLE-BOLD",
            "没有检测到加粗的节标题段落；按全部短段落匹配（若模板标题本就不加粗，可忽略）",
        )
        headings = [c for c in candidates if len(c["text"]) <= 100]
    expected = EXPECTED_TITLES[report_type]
    positions = []
    found = 0
    for label, pattern in expected:
        regex = re.compile(pattern, re.IGNORECASE)
        idx = next((i for i, c in enumerate(headings) if regex.match(c["text"])), None)
        if idx is None:
            report.error("TITLE-MISSING", f"缺少模板节标题：{label}")
        else:
            found += 1
            positions.append((label, idx))
    report.stats["titles"] = {
        "found": found,
        "expected": len(expected),
        "headings": [c["text"] for c in headings],
        "positions": positions,
    }
    if found == len(expected):
        report.info("TITLE-OK", f"节标题 {found}/{len(expected)} 齐全")
        order = [idx for _, idx in positions]
        if order != sorted(order):
            report.warn("TITLE-ORDER", "节标题顺序与模板不一致：" + " → ".join(l for l, _ in positions))


def find_cover_table(document):
    for table in document.tables:
        try:
            label = normalize(table.rows[0].cells[0].text)
        except (IndexError, AttributeError):
            continue
        if label.startswith("Lab Title"):
            return table
    return None


def check_cover(report, document, has_prose):
    table = find_cover_table(document)
    if table is None:
        report.warn("COVER-MISSING", "未找到封面字段表（Lab Title / Name …）；确认没有删掉教师封面")
        return
    labels, values = [], {}
    try:
        for row in table.rows:
            cells = row.cells
            if len(cells) < 2:
                continue
            label = normalize(cells[0].text)
            labels.append(label)
            values[label] = normalize(cells[1].text)
    except (IndexError, AttributeError):
        report.warn("COVER-READ", "封面字段表结构异常，未能逐行读取")
        return
    report.stats["cover"] = {"labels": labels, "values": values}
    missing = [lab for lab in COVER_LABELS if lab not in labels]
    if missing:
        report.warn("COVER-LABEL", "封面字段被改动或删除：" + "、".join(missing))
    score = values.get("Score:", "")
    if score:
        report.warn("COVER-SCORE", f"Score 字段已填「{score}」，评分应由教师填写")
    if has_prose:
        empty = [
            lab
            for lab in COVER_LABELS
            if lab != "Score:" and not values.get(lab, "")
        ]
        if empty:
            report.warn("COVER-EMPTY", "封面字段为空：" + "、".join(empty))
        else:
            report.info("COVER-OK", "封面字段已填写")
    else:
        report.info("COVER-BLANK", "封面为空白模板（尚未填写，正常）")


def check_page_setup(report, document, xml_stats):
    sections = document.sections
    report.stats["sections"] = len(sections)
    if len(sections) != 2:
        report.warn("SECTION-COUNT", f"分节数为 {len(sections)}，2026 模板为封面 + 正文两节；确认没有合并或拆节")
    for i, section in enumerate(sections):
        try:
            width = section.page_width.inches
            height = section.page_height.inches
            top, bottom = section.top_margin.inches, section.bottom_margin.inches
            left, right = section.left_margin.inches, section.right_margin.inches
        except (AttributeError, TypeError):
            report.warn("MARGIN-READ", f"第 {i} 节页面属性无法读取")
            continue
        a4 = abs(width - 8.27) <= 0.02 and abs(height - 11.69) <= 0.02
        margin_ok = (
            abs(top - 1.0) <= 0.02
            and abs(bottom - 1.0) <= 0.02
            and abs(left - 1.25) <= 0.02
            and abs(right - 1.25) <= 0.02
        )
        if not a4:
            report.warn("PAGE-A4", f"第 {i} 节纸张不是 A4：{width:.2f}×{height:.2f} in")
        if not margin_ok:
            report.warn(
                "MARGIN",
                f"第 {i} 节页边距异常：上 {top:.2f} / 下 {bottom:.2f} / 左 {left:.2f} / 右 {right:.2f} in"
                "（模板：上下 1.0、左右 1.25）",
            )
    if len(sections) and not getattr(sections[0], "different_first_page_header_footer", False):
        report.warn("TITLEPG", "首页未设置为「不同首页页眉页脚」：封面页眉页脚可能被正文样式覆盖")
    if xml_stats["page_field"]:
        report.info("PAGE-FIELD", "页码域 PAGE 存在（页脚）")
    else:
        report.error("PAGE-FIELD", "页脚未找到页码域 PAGE：页码会从模板继承失败")


def check_header(report, document, report_type, xml_stats):
    """检查页眉文字是否与模板一致（prelab/long 有 UESTC Student Number 字段）。"""
    header_texts = []
    for section in document.sections:
        for part in (section.header, section.first_page_header, section.even_page_header):
            try:
                text = normalize(" ".join(p.text for p in part.paragraphs))
            except (AttributeError, TypeError):
                continue
            if text:
                header_texts.append(text)
    joined = " ".join(header_texts)
    if report_type in ("prelab", "long"):
        if "UESTC Student Number" not in joined:
            report.warn("HEADER-TEXT", "页眉缺少「UESTC Student Number: …」字段，与模板不一致")
        else:
            report.info("HEADER-OK", "页眉字段与模板一致")
    elif report_type == "short" and joined:
        report.warn("HEADER-TEXT", f"short report 模板页眉无文字字段，当前页眉有文字：{joined[:60]}")


def check_score_boxes(report, document, report_type):
    count = 0
    for table in document.tables:
        try:
            first = normalize(table.rows[0].cells[0].text)
            rows = len(table.rows)
        except (IndexError, AttributeError):
            continue
        if first == "Score" and rows == 2:
            count += 1
    report.stats["score_boxes"] = count
    expected = EXPECTED_SCORE_BOXES.get(report_type)
    if expected is None:
        report.info("SCORE-BOXES", f"评分框 {count} 个（报告类型未知，未与模板比对）")
        return
    if count == expected:
        report.info("SCORE-BOXES", f"评分框 {count} 个（与模板一致）")
    elif count < expected:
        report.error("SCORE-BOXES", f"评分框 {count} 个，模板应有 {expected} 个：可能删掉了教师评分区")
    else:
        report.warn("SCORE-BOXES", f"评分框 {count} 个，多于模板的 {expected} 个：确认是否有误插入的评分表")


def check_fonts(report, xml_stats):
    font_runs = xml_stats["font_runs"]
    font_chars = xml_stats["font_chars"]
    stats = []
    for name, runs in font_runs.most_common():
        level, note = classify_font(name)
        stats.append(
            {
                "font": name,
                "runs": runs,
                "chars": font_chars.get(name, 0),
                "where": sorted(xml_stats["font_where"][name]),
                "level": level,
                "note": note,
            }
        )
    report.stats["fonts"] = stats
    for item in stats:
        if item["level"] == "error":
            report.error(
                "FONT",
                f"非白名单字体 {item['font']}：{item['runs']} 处（{'/'.join(item['where'])}），{item['note']}",
            )
        elif item["level"] == "warn":
            report.warn(
                "FONT",
                f"需复核字体 {item['font']}：{item['runs']} 处（{'/'.join(item['where'])}），{item['note']}",
            )
    if not font_runs:
        report.warn("FONT-EMPTY", "文档中未发现显式字体设置：全部使用样式默认字体，需查 PDF 实际字体")


def check_sizes(report, xml_stats):
    sizes = xml_stats["sizes"]
    report.stats["sizes"] = {str(k): v for k, v in sorted(sizes.items())}
    if not sizes:
        return
    dominant = max(sizes, key=sizes.get)
    report.info("SIZE", f"正文字号以 {dominant:g}pt 为主；分布：" + "、".join(f"{pt:g}pt×{n}" for pt, n in sorted(sizes.items())))
    small = xml_stats["small_text_runs"]
    if small:
        sample = "；".join(f"{w} {pt:g}pt「{t}」" for w, pt, t in small[:3])
        report.warn("SIZE-SMALL", f"{len(small)} 处正文小于 9pt：{sample}")


def check_omml(report, xml_stats, has_prose):
    omml = xml_stats["omml"]
    report.stats["omml"] = omml
    if has_prose and omml == 0:
        report.warn(
            "OMML-0",
            "成稿未检测到原生公式 OMML：确认本次确实无公式；有公式时不要用图片或纯文本代替",
        )
    elif omml:
        report.info("OMML", f"原生 OMML 公式 {omml} 个")
    else:
        report.info("OMML", "模板无公式（空白模板，正常）")


def check_images(report, xml_stats):
    drawings = xml_stats["drawings"]
    report.stats["drawings"] = drawings
    if drawings == 0:
        report.warn("IMAGE", "文档内没有内嵌图片：模板应有 logo / 水印；若被删除需补回")
    else:
        report.info("IMAGE", f"内嵌图片 {drawings} 处（模板 logo / 水印照常保留）")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="check_docx.py",
        description="检查 UESTC 大物实验 Word 报告的字体、公式、节标题、评分框、页边距等设置。",
        epilog=(
            "退出码：0 通过；1 有 error（--strict 下 warn 也算失败）；2 用法错误；"
            "3 运行环境或输入不可用（缺 python-docx、文件缺失/不是 docx）。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("file", help="待检查的 .docx 文件")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式：warn 也视为失败（用于提交前最终检查）",
    )
    parser.add_argument("--json", action="store_true", help="输出机器可读的 JSON")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)  # 用法错误时 argparse 以 2 退出
    path = Path(args.file)
    if not path.exists():
        print(f"错误：文件不存在：{path}", file=sys.stderr)
        return 3
    if path.suffix.lower() != ".docx":
        print(f"错误：{path} 不是 .docx 文件（本脚本只查 Word 文档）", file=sys.stderr)
        return 3
    try:
        document = Document(str(path))
        zf = zipfile.ZipFile(str(path))
    except Exception as exc:  # 损坏或非 docx
        print(f"错误：无法打开 {path}：{exc}", file=sys.stderr)
        return 3

    report = Report()
    infos = paragraph_infos(document)
    paragraphs = [info["text"] for info in infos]
    body_text = " ".join(paragraphs)
    has_prose = any(len(p) > 100 for p in paragraphs)
    report.stats["paragraphs"] = len(paragraphs)
    report.stats["body_text_chars"] = len(body_text)
    report.stats["has_prose"] = has_prose
    report.stats["tables"] = len(document.tables)

    report_type, how = detect_report_type(path.name, body_text)
    report.stats["report_type"] = report_type
    report.stats["type_detect"] = how

    try:
        xml_stats = collect_xml_stats(zf)
    finally:
        zf.close()

    check_fonts(report, xml_stats)
    check_sizes(report, xml_stats)
    check_omml(report, xml_stats, has_prose)
    check_titles(report, infos, report_type)
    check_score_boxes(report, document, report_type)
    check_page_setup(report, document, xml_stats)
    check_header(report, document, report_type, xml_stats)
    check_cover(report, document, has_prose)
    check_images(report, xml_stats)

    errors, warns, infos = report.count("error"), report.count("warn"), report.count("info")
    passed = errors == 0 and (warns == 0 if args.strict else True)

    if args.json:
        payload = {
            "file": str(path),
            "report_type": report_type,
            "type_detect": how,
            "strict": args.strict,
            "passed": passed,
            "findings": report.findings,
            "stats": report.stats,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if passed else 1

    print("== check_docx.py ==")
    print(f"文件：{path}")
    print(f"类型：{TYPE_LABEL.get(report_type, '未知') if report_type else '未知'}（{how}）")
    print(
        f"分节 {len(document.sections)}　段落 {report.stats['paragraphs']}　"
        f"表格 {report.stats['tables']}　内嵌图 {report.stats['drawings']}　"
        f"OMML {report.stats['omml']}"
    )
    if has_prose:
        print(f"正文：约 {report.stats['body_text_chars']} 字符")
    else:
        print("正文：空白模板（没有 >100 字符的正文段落）")

    print("\n-- 字体 --")
    if report.stats["fonts"]:
        for item in report.stats["fonts"]:
            mark = {"ok": "OK", "warn": "复核", "error": "错误"}[item["level"]]
            where = "/".join(item["where"])
            print(
                f"  {item['font']:<22} {mark:<4} {item['runs']:>4} 处 / {item['chars']:>6} 字符　[{where}]"
            )
    else:
        print("  （无显式字体设置）")

    print("\n-- 字号（有文字的 run）--")
    if report.stats["sizes"]:
        print(
            "  "
            + "、".join(f"{pt}pt×{n}" for pt, n in sorted(
                ((float(k), v) for k, v in report.stats["sizes"].items()), key=lambda x: x[0]
            ))
        )
    else:
        print("  （无）")

    print("\n-- 页面 --")
    for i, section in enumerate(document.sections):
        try:
            print(
                f"  第 {i} 节：{section.page_width.inches:.2f}×{section.page_height.inches:.2f} in，"
                f"边距 上 {section.top_margin.inches:.2f} / 下 {section.bottom_margin.inches:.2f} / "
                f"左 {section.left_margin.inches:.2f} / 右 {section.right_margin.inches:.2f} in"
            )
        except (AttributeError, TypeError):
            print(f"  第 {i} 节：页面属性无法读取")

    print("\n-- 结构 --")
    title_stats = report.stats.get("titles")
    if title_stats:
        print(f"  节标题：{title_stats['found']}/{title_stats['expected']}")
    print(f"  评分框：{report.stats.get('score_boxes')} 个")
    print(f"  页码域 PAGE：{'有' if xml_stats['page_field'] else '无'}")

    print("\n-- 发现 --")
    if not report.findings:
        print("  （无）")
    for finding in report.findings:
        tag = {"error": "ERROR", "warn": "WARN", "info": "INFO"}[finding["level"]]
        print(f"  [{tag}] {finding['code']}: {finding['message']}")

    print("\n== 结果 ==")
    if passed:
        print(f"PASS（error 0 / warn {warns} / info {infos}）")
    else:
        print(f"FAIL（error {errors} / warn {warns} / info {infos}）")
        if args.strict and errors == 0 and warns:
            print("--strict：warn 视为失败；按上面的条目逐项确认或修正。")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())