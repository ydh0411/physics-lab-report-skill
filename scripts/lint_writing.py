#!/usr/bin/env python3
"""Lint the prose of a physics lab report for AI-style filler and defensive wording.

Rules follow `references/writing-policy.md`:

    AI-1 .. AI-8  去 AI 味（浮夸词、机械三段式、同义词轮换、聊天腔开场、无信息承诺、
                  列举堆砌、排比/粗体滥用、每段过渡语）
    DEF-1 .. DEF-6 去防御性语言（模板/流程声明、教材章节旁白、重复限定堆叠、
                  自我辩护与免责、有效数字与不确定度教学式解释、假想反驳）
    OK-1 .. OK-3  允许保留（一层准确限定、真实假设、异常与偏差解释），只列不报。

Usage
    python3 scripts/lint_writing.py <file.md|file.docx|file.txt> [--json] [--max N]
    python3 scripts/lint_writing.py --list-rule

Exit codes
    0  no hit, or hit count <= --max (default 0)
    1  hit count > --max
    2  usage error (no file given, unknown option, non-integer --max, multiple files)
    3  file unreadable, unsupported extension, or not a valid .docx package

Behaviour notes
    * .md / .txt are read as UTF-8 (UTF-8 BOM tolerated). A GB18030 fallback is
      tried, then the file is reported as unreadable (exit 3).
    * .md fenced code blocks (``` / ~~~) and inline code spans (`...`) are masked
      before scanning, so policy documents can embed bad examples safely.
    * .docx is read with python-docx when available. If python-docx is missing or
      fails to import, the script falls back to the standard library: it unzips
      `word/document.xml` and rebuilds one paragraph per `<w:p>` from `<w:t>`.
      Either path gives the same paragraph/line scan, so .docx lint works without
      any third-party package; exit code 3 is reserved for a file that cannot be
      opened as a valid docx (zip) package.
    * A hit is a prompt to review a sentence, not an automatic deletion order.
"""

from __future__ import annotations

import json
import os
import re
import sys
import zipfile

# --------------------------------------------------------------------------- #
# Rule table. Ids match references/writing-policy.md one-to-one.
# "checkable" False means the rule documents allowed content and never reports.
# --------------------------------------------------------------------------- #

RULES = [
    {
        "id": "AI-1",
        "name": "浮夸形容词与空泛意义",
        "kind": "AI",
        "checkable": True,
        "patterns": [
            r"\b(crucial|crucially|vital|paramount|indispensable|pivotal|groundbreaking|"
            r"cutting[- ]edge|state[- ]of[- ]the[- ]art|seamless(ly)?|holistic|"
            r"comprehensive(ly)?|remarkabl[ey]|robust(ly|ness)?|leverage[sd]?|"
            r"delve[sd]? into|shed[s]? light on|pave[sd]? the way|holds? promise|"
            r"testament to|underscore[sd]?)\b",
            r"\bplays? (an? )?(crucial|vital|key|central|pivotal|significant|important) role\b",
            r"\bof (great|considerable|paramount) (significance|importance)\b",
            r"\b(extremely|highly|very|incredibly|remarkably) (important|accurate|precise|useful|reliable|sensitive)\b",
        ],
        "advice": "改成具体物理事实或量值；形容词不能替代证据。",
        "bad": "The micrometer plays a crucial role in this robust and comprehensive setup.",
        "good": "The micrometer reads the mirror displacement in steps of 0.01 mm.",
    },
    {
        "id": "AI-2",
        "name": "机械三段式与套话",
        "kind": "AI",
        "checkable": True,
        "patterns": [
            r"\b(first of all|last but not least|all in all|in a word|to sum up|in summary|"
            r"as a matter of fact|needless to say|goes without saying)\b",
            r"\b(it is (worth|important|necessary) (noting|to note|mentioning) that|"
            r"it should be (noted|mentioned) that)\b",
            r"^\s*(in conclusion|to conclude|in summary)\s*[,:]",
            r"\bthe (whole|entire) (process|experiment) can be (divided|summari[sz]ed) into\b",
        ],
        "advice": "删掉开场套话，直接写结论或现象；结论段不靠“总之/综上所述”撑结构。",
        "bad": "First of all, it is worth noting that the fringes moved. All in all, the result is good.",
        "good": "The fringes moved by 240 counts over 0.126 mm of mirror travel.",
    },
    {
        "id": "AI-3",
        "name": "同义词轮换（同段落多个近义词指同一对象）",
        "kind": "AI",
        "checkable": True,
        "patterns": [],
        "advice": "同一物理量、同一器材只用同一个词；不要为“变化”换近义词。",
        "bad": "The apparatus was levelled, the instrument was calibrated, and the equipment was checked.",
        "good": "The interferometer was levelled and calibrated before the first reading.",
    },
    {
        "id": "AI-4",
        "name": "聊天腔开场与第一人称预告",
        "kind": "AI",
        "checkable": True,
        "patterns": [
            r"\b(in this (report|paper|experiment|lab report|section),? (we|i) (will|shall|are going to|aim|attempt))\b",
            r"\b(this (report|paper) (will|aims to|is going to|sets out to))\b",
            r"\bwe will (now )?(explore|examine|delve|take a look|look at|walk through)\b",
            r"\b(let us|let's) (now )?(consider|examine|take|start|begin|look)\b",
            r"\b(as we all know|as is well known|as (you|we) (may |might )?know)\b",
            r"\bin the (following|next) (section|part),? (we|this report)\b",
        ],
        "advice": "直接从测量对象和结果写起，删掉“本报告将……”“让我们……”式预告。",
        "bad": "In this report, we will explore how the Michelson interferometer works.",
        "good": "The wavelength of the He-Ne laser was measured with a Michelson interferometer.",
    },
    {
        "id": "AI-5",
        "name": "无信息承诺",
        "kind": "AI",
        "checkable": True,
        "patterns": [
            r"\bwill be (discussed|described|presented|analy[sz]ed|explained|illustrated|"
            r"shown|covered) (in (further |more )?detail|in detail|below|later)\b",
            r"\bis (discussed|described|presented|analy[sz]ed) (in (further )?detail|in detail|below|later)\b",
            r"\bwe will see (that|how)\b",
            r"\bas (will be|is) (shown|discussed) (below|later)\b",
            r"\bthe (details|remainder) (of which )?(are|is) (given|presented|left) (below|later)\b",
            r"\bsubsequent sections? (will|describe)\b",
            r"\bmore (detail|details) (will|can be found) (be )?(given|found)\b",
        ],
        "advice": "承诺要展示的内容不该占正文；直接给出该内容本身，删掉“下文将详细讨论”。",
        "bad": "The alignment procedure will be discussed in detail in the following section.",
        "good": "The mirrors were aligned until the central fringe closed to a single spot.",
    },
    {
        "id": "AI-6",
        "name": "列举堆砌代替论证",
        "kind": "AI",
        "checkable": True,
        "patterns": [
            r"\bthere are (three|four|five|several|multiple|many) (main )?"
            r"(reasons|aspects|factors|points|steps|features|advantages|reasons why)\b",
        ],
        "advice": "列举前先给因果或证据；顺序步骤（Experimental Procedure）属于允许例外。",
        "bad": "There are three main aspects: first the alignment, second the counting, third the fitting.",
        "good": "Fringe counts were taken at five mirror positions and fitted against the order number.",
    },
    {
        "id": "AI-7",
        "name": "排比、粗体与感叹号滥用",
        "kind": "AI",
        "checkable": True,
        "patterns": [
            r"\bnot only\b[^.]{0,90}\bbut also\b",
            r"[!！]",
        ],
        "advice": "报告正文不用感叹号、不堆粗体、不造对仗排比；强调靠数据和对比。",
        "bad": "**Crucial** point: the fringe **count** is **critical** to the **result**!",
        "good": "A miscount of one fringe shifts the wavelength by 0.6 nm.",
    },
    {
        "id": "AI-8",
        "name": "每段必加过渡语",
        "kind": "AI",
        "checkable": True,
        "patterns": [],
        "advice": "段落之间靠物理因果衔接；删掉 Moreover/Furthermore/Additionally 式填充过渡。",
        "bad": "Moreover, the fringes were sharp. Furthermore, the count was stable. Additionally, the fit was good.",
        "good": "The fringes were sharp and the count stayed stable, so the fit residuals stayed below 2 counts.",
    },
    {
        "id": "DEF-1",
        "name": "模板与流程使用声明",
        "kind": "DEF",
        "checkable": True,
        "patterns": [
            r"\b(the )?(provided|given|supplied|official) (word )?(template|format)\b",
            r"\b(provided|given) (data )?(tables?|sheets?|forms?)\b",
            r"\b(we|i) (use|used|follow|followed|adopt|adopted|stick to) the "
            r"(provided|given|official|required|prescribed) (template|format|tables?|structure|layout)\b",
            r"\b(according to|following|as required by|per) the (provided |official |required )?"
            r"(template|format|score ?box)\b",
            r"\bthe (report|document) follows the (template|required|prescribed|official)\b",
        ],
        "advice": "模板是否被使用由成稿版式自己证明；正文不写“按模板/按给定表格”。",
        "bad": "We use the provided template and the provided data tables in this report.",
        "good": "",
    },
    {
        "id": "DEF-2",
        "name": "教材章节与处理流程旁白",
        "kind": "DEF",
        "checkable": True,
        "patterns": [
            r"\b(processed|calculated|computed|analy[sz]ed|derived|treated|obtained|handled) "
            r"(using|with|by|according to|following)[^.]{0,40}\b(sec\.?|section|chapter)\s*\.?\s*\d",
            r"\b(according to|as described in|as given in|per|from)\s+(sec\.?|section|chapter)\s*\.?\s*\d",
            r"\btextbook'?s? (sec\.?|section|chapter)\b",
            r"\b(the )?(lab )?manual'?s? (sec\.?|section|chapter)\b",
            r"\b(using|following) the (procedure|method|treatment) (in|of) the (textbook|manual|handout)\b",
        ],
        "advice": "教材章节号留在内部笔记；正文给公式、代入和结果，不写“按第 3.9.6 节处理”。",
        "bad": "Data are processed using Sec. 3.9.6 of the textbook.",
        "good": "Fringe order N was converted to mirror displacement with d = N·λ/2.",
    },
    {
        "id": "DEF-3",
        "name": "重复限定堆叠",
        "kind": "DEF",
        "checkable": True,
        "patterns": [
            r"\b(might|may|could|would|can)\s+(potentially|possibly|perhaps|conceivably|arguably|tentatively)\b",
            r"\b(potentially|possibly|perhaps|conceivably|arguably)\s+(might|may|could)\b",
            r"\b(seems?|appears?|tends?) to (suggest|indicate|imply)\b",
            r"\bwould appear to\b",
            r"\bit is (possible|conceivable) that[^.]{0,60}\b(may|might|could)\b",
            r"\b(somewhat|rather|relatively|fairly) (possibly|likely|uncertain)\b",
        ],
        "advice": "保留一层限定（may / suggests / could indicate）；叠两三层就把结论写没了。",
        "bad": "The residual offset might potentially suggest that the plate was slightly tilted.",
        "good": "The residual 0.4° offset suggests the plate was slightly tilted.",
    },
    {
        "id": "DEF-4",
        "name": "自我辩护与免责声明",
        "kind": "DEF",
        "checkable": True,
        "patterns": [
            r"\bto (ensure|maintain|guarantee|preserve) (rigor|rigour|accuracy|correctness|reliability|consistency|clarity)\b",
            r"\bto (avoid|prevent|eliminate|rule out) (any )?(misunderstanding|confusion|ambiguity|misinterpretation)\b",
            r"\bfor the sake of (rigor|rigour|completeness|clarity|accuracy|precision)\b",
            r"\bfor (completeness|clarity|rigor|rigour)\b",
            r"\bit (must|should) be (emphasi[sz]ed|stressed|pointed out) that\b",
            r"\bwe (must|should) (emphasi[sz]e|stress|point out)\b",
            r"\bnot to be confused with\b",
            r"\bit goes without saying that\b",
        ],
        "advice": "删掉“为保证严谨/避免误解”这类自我辩护；只要证据和限定准确即可。",
        "bad": "To ensure rigor and avoid misunderstanding, we emphasize that all data were checked twice.",
        "good": "",
    },
    {
        "id": "DEF-5",
        "name": "有效数字与不确定度规则的教学式解释",
        "kind": "DEF",
        "checkable": True,
        "patterns": [
            r"\b(rules?|conventions?) (of|for) significant figures\b",
            r"\b(round(ed|ing)?|quot(e|ed|ing)|keep|keeping|retain(ed|ing)?|express(ed|ing)?|"
            r"report(ed|ing)?) [^.]{0,45}\bsignificant figures?\b",
            r"\bsignificant figures? (is|are|were) (used|kept|retained|applied|required|adopted)\b",
            r"\bby convention,? [^.]{0,70}\b(uncertainty|significant figures?)\b",
            r"\b(coverage factor|standard uncertainty is (defined|calculated) as|"
            r"the last (significant )?digit (is|was) (aligned|kept|adjusted))\b",
            r"\bthe (rules?|definition) of (standard )?uncertainty\b",
        ],
        "advice": "取位直接体现在数值里：写 x = 0.126 ± 0.002 mm，不解释为什么保留一位有效数字。",
        "bad": "According to the rules of significant figures, the uncertainty is kept to one significant figure.",
        "good": "d = 0.126 ± 0.002 mm.",
    },
    {
        "id": "DEF-6",
        "name": "假想反驳与自我设问",
        "kind": "DEF",
        "checkable": True,
        "patterns": [
            r"\b(some|many|one|others|critics|readers) (may|might|could|will) "
            r"(argue|say|object|think|wonder|claim|point out)\b",
            r"\bit (could|might|may) be (objected|argued|countered|suggested) (that)?\b",
            r"\bone (might|could) (argue|object|think|wonder)\b",
            r"\bwhile (some|it) (might|may) (seem|think|argue)\b",
            r"\bit (may|might) seem (counterintuitive|surprising|strange|odd) (that)?\b",
            r"\bcontrary to (a )?(common|popular) (belief|misconception)\b",
            r"\bsome (would|might) (disagree|object)\b",
        ],
        "advice": "报告里没有对手要反驳；删掉“有人可能会说”。",
        "bad": "Some may argue that the fringe count was subjective, but our data are reliable.",
        "good": "Fringe counts from two observers differed by at most one count in ten.",
    },
    {
        "id": "OK-1",
        "name": "一层准确限定（允许）",
        "kind": "OK",
        "checkable": False,
        "patterns": [],
        "advice": "may / suggests / could indicate 这类单层限定保留，不按 DEF-3 删除。",
        "bad": "",
        "good": "The 3% excess may come from the plate thickness tolerance.",
    },
    {
        "id": "OK-2",
        "name": "真实假设（允许）",
        "kind": "OK",
        "checkable": False,
        "patterns": [],
        "advice": "影响结论的假设写一次，放在用到它的那一步（如忽略浮力）。",
        "bad": "",
        "good": "The buoyancy correction was neglected because it changes the result by 0.02%.",
    },
    {
        "id": "OK-3",
        "name": "异常数据与偏差解释（允许）",
        "kind": "OK",
        "checkable": False,
        "patterns": [],
        "advice": "异常值、失败尝试、系统偏差照实写并给机制，不得删掉或改得贴近参考值。",
        "bad": "",
        "good": "The third run drifted by 1.8% and was excluded; the drift followed the room warm-up.",
    },
]

RULE_BY_ID = {rule["id"]: rule for rule in RULES}

# Synonyms that should not rotate within one paragraph (rule AI-3).
SYNONYM_FAMILIES = {
    "仪器": ("apparatus", "device", "instrument", "equipment", "rig"),
    "计算": ("calculate", "compute", "evaluate", "derive"),
    "显示": ("show", "demonstrate", "display", "reveal", "illustrate", "indicate"),
    "方法": ("method", "approach", "procedure", "technique"),
}
SYNONYM_THRESHOLD = 3

# Transition adverbs that should not open two sentences of one paragraph (AI-8).
TRANSITION_OPENERS = (
    "moreover", "furthermore", "additionally", "in addition", "besides",
    "what is more", "similarly", "equally important", "on top of that",
)
TRANSITION_THRESHOLD = 2

# Ordinal markers for enumerations inside one paragraph (AI-6).
ORDINALS = {
    "first": 1, "firstly": 1, "second": 2, "secondly": 2, "third": 3,
    "thirdly": 3, "fourth": 4, "fourthly": 4, "fifth": 5, "fifthly": 5,
}
ORDINAL_RE = re.compile(r"\b(" + "|".join(ORDINALS) + r")\b", re.IGNORECASE)
NUMERIC_ORDINAL_RE = re.compile(r"(?:^|(?<=[.;:]\s))[(]?\d[).]\s", re.MULTILINE)

# Paragraphs under these headings may legitimately enumerate steps (Long report).
PROCEDURE_HEADING_RE = re.compile(r"procedure|steps?|操作|步骤", re.IGNORECASE)

MAX_SENTENCE_DISPLAY = 120


def split_sentences(paragraph_text):
    """Split one paragraph into sentences.

    A period is only treated as a sentence end when the next character starts a
    new sentence; decimals ("3.9.6"), abbreviations ("Sec. 3.9.6") and inline
    references ("Eq. 3") therefore stay inside one sentence.
    """
    text = paragraph_text.strip()
    sentences = []
    start = 0
    for match in re.finditer(r"(?<=[.!?])(\s+)", text):
        following = text[match.end():match.end() + 1]
        if following and (following.isdigit() or following.islower()):
            continue
        sentences.append(text[start:match.start()].strip())
        start = match.end()
    tail = text[start:].strip()
    if tail:
        sentences.append(tail)
    return [sentence for sentence in sentences if sentence]


def longest_increasing_run(values):
    """Length of the longest strictly increasing subsequence (small lists only)."""
    best = []
    for pos, value in enumerate(values):
        run = [value]
        last = value
        for later in values[pos + 1:]:
            if later > last:
                run.append(later)
                last = later
        if len(run) > len(best):
            best = run
    return len(best)


def check_ai3_synonym_rotation(paragraph_text):
    """Report paragraphs that rotate synonyms for one and the same object."""
    lowered = paragraph_text.lower()
    for family_name, words in SYNONYM_FAMILIES.items():
        present = [word for word in words if re.search(r"\b" + re.escape(word) + r"s?\b", lowered)]
        if len(present) >= SYNONYM_THRESHOLD:
            snippet = paragraph_text.strip()
            return [
                "同一段落用 %d 个近义词指代同一%s：%s"
                % (len(present), family_name, "、".join(present)),
                snippet,
            ]
    return None


def check_ai6_enumeration(paragraph_text):
    """Report enumeration-heavy paragraphs: ordinal chains or numeric 1) 2) 3)."""
    matches = [(m.start(), ORDINALS[m.group(1).lower()]) for m in ORDINAL_RE.finditer(paragraph_text)]
    numeric = NUMERIC_ORDINAL_RE.findall(paragraph_text)
    chain = longest_increasing_run([rank for _, rank in matches])
    if chain >= 3 or len(numeric) >= 3:
        return paragraph_text.strip()
    return None


def check_ai7_style(paragraph_text):
    """Report bold/emoji abuse and exclamation marks at paragraph level."""
    hits = []
    bold_spans = re.findall(r"\*\*[^*\n]+\*\*", paragraph_text)
    if len(bold_spans) >= 3:
        hits.append(("粗体强调 %d 处" % len(bold_spans), bold_spans[0]))
    emoji_re = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2705\u274C]")
    found = emoji_re.findall(paragraph_text)
    if found:
        hits.append(("正文出现 emoji %s" % "".join(found[:3]), "".join(found[:3])))
    parallel = re.findall(r"\bnot only\b[^.]{0,90}\bbut also\b", paragraph_text, re.IGNORECASE)
    if parallel:
        hits.append(("排比句式 not only ... but also", parallel[0]))
    return hits


def check_ai8_transitions(paragraph_text):
    """Report paragraphs whose sentences keep opening with filler transitions."""
    sentences = split_sentences(paragraph_text)
    openers = []
    matched_sentences = []
    for sentence in sentences:
        lowered = sentence.lower()
        for opener in TRANSITION_OPENERS:
            if lowered.startswith(opener):
                openers.append(opener)
                matched_sentences.append(sentence)
                break
    if len(openers) >= TRANSITION_THRESHOLD:
        return openers, " ".join(matched_sentences)
    return None


def mask_markdown(text):
    """Blank out fenced code blocks and inline code spans, keeping offsets/新行."""
    masked_lines = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            masked_lines.append("".join("\n" if ch == "\n" else " " for ch in line))
            continue
        if in_fence:
            masked_lines.append("".join("\n" if ch == "\n" else " " for ch in line))
        else:
            masked_lines.append(line)
    masked = "".join(masked_lines)
    return re.sub(r"`[^`\n]*`", lambda m: " " * len(m.group(0)), masked)


def build_paragraphs(lines, markdown):
    """Yield (first_line_no, heading, [line_no, text]) and skip heading lines."""
    buffer = []
    heading = ""

    def flush():
        if buffer:
            yielded = (buffer[0][0], heading, list(buffer))
            buffer.clear()
            return yielded
        return None

    paragraphs = []
    for lineno, raw in enumerate(lines, start=1):
        text = raw.rstrip("\n")
        if not text.strip():
            pending = flush()
            if pending:
                paragraphs.append(pending)
            continue
        if markdown and re.match(r"^\s{0,3}#{1,6}\s", text):
            pending = flush()
            if pending:
                paragraphs.append(pending)
            heading = re.sub(r"^\s{0,3}#{1,6}\s*", "", text).strip()
            continue
        buffer.append((lineno, text))
    pending = flush()
    if pending:
        paragraphs.append(pending)
    return paragraphs, heading


def read_text_file(path):
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            with open(path, "r", encoding=encoding) as handle:
                return handle.read()
        except UnicodeDecodeError:
            continue
        except OSError as error:
            raise LintError("无法读取文件 %s：%s" % (path, error))
    raise LintError("无法按 UTF-8 或 GB18030 解码 %s（可能是二进制文件）" % path)


def read_docx_with_python_docx(path):
    import docx  # noqa: WPS433 - optional dependency, guarded by caller

    document = docx.Document(path)
    lines = []
    for paragraph in document.paragraphs:
        style_name = (paragraph.style.name if paragraph.style is not None else "") or ""
        prefix = "# " if style_name.lower().startswith("heading") else ""
        lines.append(prefix + paragraph.text)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    lines.append(paragraph.text)
    return "\n\n".join(line for line in lines if line.strip())


def read_docx_with_stdlib(path):
    """Fallback: rebuild paragraph text straight from word/document.xml."""
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml").decode("utf-8", "ignore")
    except (zipfile.BadZipFile, KeyError, OSError) as error:
        raise LintError("无法读取 .docx（不是有效的 docx/zip 包）：%s" % error)

    xml = xml.replace("</w:p>", "\n</w:p>")
    xml = re.sub(r"<w:tab\s*/>", "\t", xml)
    xml = re.sub(r"<w:br\s*/>", "\n", xml)
    text = re.sub(r"<[^>]+>", "", xml)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&apos;", "'")
    paragraphs = [line.strip() for line in text.splitlines()]
    return "\n\n".join(paragraph for paragraph in paragraphs if paragraph)


class LintError(Exception):
    """Raised when the input file cannot be read or parsed."""


def load_lines(path):
    suffix = os.path.splitext(path)[1].lower()
    if suffix == ".docx":
        try:
            text = read_docx_with_python_docx(path)
        except ImportError:
            text = read_docx_with_stdlib(path)
        except LintError:
            raise
        except Exception:
            text = read_docx_with_stdlib(path)
        return text.splitlines(), True
    if suffix in (".md", ".markdown"):
        return mask_markdown(read_text_file(path)).splitlines(), True
    if suffix in (".txt", ""):
        return read_text_file(path).splitlines(), False
    raise LintError(
        "不支持的文件类型 %s（支持 .md / .docx / .txt）" % (suffix or "无扩展名")
    )


def scan(text_lines, markdown):
    hits = []

    def add(rule_id, lineno, sentence, note=""):
        rule = RULE_BY_ID[rule_id]
        display = " ".join(sentence.split())
        if len(display) > MAX_SENTENCE_DISPLAY:
            display = display[: MAX_SENTENCE_DISPLAY - 1] + "…"
        hits.append(
            {
                "rule": rule_id,
                "rule_name": rule["name"],
                "kind": rule["kind"],
                "line": lineno,
                "sentence": display,
                "note": note,
                "advice": rule["advice"],
            }
        )

    paragraphs, _ = build_paragraphs(text_lines, markdown)
    for first_line, heading, block in paragraphs:
        paragraph_text = " ".join(text for _, text in block)
        is_procedure = bool(PROCEDURE_HEADING_RE.search(heading or ""))

        # Sentence-level rules.
        for lineno, text in block:
            for sentence in split_sentences(text):
                for rule in RULES:
                    if not rule["checkable"] or not rule["patterns"]:
                        continue
                    for pattern in rule["patterns"]:
                        match = re.search(pattern, sentence, re.IGNORECASE)
                        if match:
                            add(rule["id"], lineno, sentence, "命中 %r" % match.group(0))
                            break

        # Paragraph-level rules.
        synonym = check_ai3_synonym_rotation(paragraph_text)
        if synonym:
            add("AI-3", first_line, synonym[1], synonym[0])

        if not is_procedure:
            enumeration = check_ai6_enumeration(paragraph_text)
            if enumeration:
                add("AI-6", first_line, enumeration, "同段落出现 3 个及以上顺序列举")

        for note, sentence in check_ai7_style(paragraph_text):
            add("AI-7", first_line, sentence, note)

        transition = check_ai8_transitions(paragraph_text)
        if transition:
            add(
                "AI-8",
                first_line,
                transition[1],
                "同段落 %d 句以后置过渡词开头：%s"
                % (len(transition[0]), "、".join(transition[0])),
            )

    # De-duplicate identical (rule, line, sentence) records.
    unique = {}
    for hit in hits:
        key = (hit["rule"], hit["line"], hit["sentence"])
        unique.setdefault(key, hit)
    ordered = sorted(unique.values(), key=lambda item: (item["line"], item["rule"]))
    return ordered


def print_rule_table():
    print("规则 id  类型  规则名                           判定要点")
    print("-" * 96)
    for rule in RULES:
        kind = "禁用" if rule["checkable"] else "允许"
        sample = rule["bad"] or rule["good"] or ""
        print("%-8s %-5s %-32s %s" % (rule["id"], kind, rule["name"], sample[:46]))
    print()
    print("允许类规则（OK-1..OK-3）只用于自查，不产生命中，也不影响退出码。")


def main(argv):
    args = list(argv[1:])
    json_output = False
    max_hits = 0
    paths = []

    index = 0
    while index < len(args):
        token = args[index]
        if token in ("--help", "-h"):
            print(__doc__)
            return 0
        if token == "--list-rule":
            print_rule_table()
            return 0
        if token == "--json":
            json_output = True
        elif token == "--max":
            index += 1
            if index >= len(args):
                print("用法错误：--max 需要整数参数", file=sys.stderr)
                return 2
            try:
                max_hits = int(args[index])
            except ValueError:
                print("用法错误：--max 需要整数，收到 %r" % args[index], file=sys.stderr)
                return 2
            if max_hits < 0:
                print("用法错误：--max 不能为负数", file=sys.stderr)
                return 2
        elif token.startswith("--"):
            print("用法错误：未知选项 %s（见 --help）" % token, file=sys.stderr)
            return 2
        else:
            paths.append(token)
        index += 1

    if len(paths) != 1:
        print("用法：python3 scripts/lint_writing.py <file.md|file.docx|file.txt> "
              "[--json] [--max N] [--list-rule]", file=sys.stderr)
        return 2

    path = paths[0]
    if not os.path.exists(path):
        print("错误：文件不存在 %s" % path, file=sys.stderr)
        return 3
    if not os.path.isfile(path):
        print("错误：不是普通文件 %s" % path, file=sys.stderr)
        return 3

    try:
        text_lines, markdown = load_lines(path)
    except LintError as error:
        print("错误：%s" % error, file=sys.stderr)
        return 3

    hits = scan(text_lines, markdown)
    passed = len(hits) <= max_hits
    counts = {}
    for hit in hits:
        counts[hit["rule"]] = counts.get(hit["rule"], 0) + 1

    if json_output:
        payload = {
            "file": path,
            "max": max_hits,
            "hit_count": len(hits),
            "passed": passed,
            "counts_by_rule": counts,
            "hits": hits,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for hit in hits:
            print("%s:%d  [%s] %s" % (path, hit["line"], hit["rule"], hit["rule_name"]))
            print("    句子：%s" % hit["sentence"])
            if hit["note"]:
                print("    命中：%s" % hit["note"])
            print("    建议：%s" % hit["advice"])
        summary = "共 %d 处命中（阈值 %d）：%s" % (
            len(hits), max_hits, "通过" if passed else "未通过")
        if counts:
            summary += "；按规则：" + "，".join(
                "%s×%d" % (rule_id, counts[rule_id]) for rule_id in sorted(counts))
        print(summary)

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))