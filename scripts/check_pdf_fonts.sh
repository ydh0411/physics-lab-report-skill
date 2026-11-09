#!/bin/bash
# Check the fonts actually embedded in a PDF report (via pdffonts).
#
# Usage: bash scripts/check_pdf_fonts.sh <file.pdf> [-l]
#
# Docx 里写的字体名不等于 PDF 里用的字体：Word 可能把数学字母换成
# Cambria Math，LibreOffice 缺字体时会静默回退成 Liberation/Songti。
# 因此导出 PDF 后必须查实际字体。
#
# 白名单（按 PostScript 名、忽略子集前缀）：
#   - Times New Roman（TimesNewRomanPSMT 等）
#   - SimSun / 宋体（含 NSimSun）
#   - Symbol / OpenSymbol（项目符号）
#   - TeX Gyre 回退（TeXGyreTermes 等）
# Cambria Math（公式字体被 Word 替换）判为错误；LibreOffice 默认替换字体单独提示。
# Base-14 的 Times / Times-Roman（未嵌入的标准 PDF 字体）视为可用但会标注。

set -euo pipefail

usage() {
    cat <<'EOF'
用法: bash scripts/check_pdf_fonts.sh <file.pdf> [-l]

  <file.pdf>  要检查的 PDF（只读，不修改）
  -l          同时打印 pdffonts 的原始表格（逐字体列出 type/encoding/emb）

退出码:
  0  字体全部在白名单内
  1  存在非白名单字体、未嵌入字体，或 PDF 未检测到任何字体
  2  参数用法错误
  3  pdffonts 不可用（未安装 poppler）或 PDF 无法读取/不是 PDF

安装 pdffonts: macOS `brew install poppler`；Debian/Ubuntu `apt install poppler-utils`。
EOF
}

LIST=0
ARGS=()
for arg in "$@"; do
    case "$arg" in
        -l) LIST=1 ;;
        -h|--help) usage; exit 0 ;;
        -*) echo "错误：未知选项 $arg" >&2; usage >&2; exit 2 ;;
        *) ARGS+=("$arg") ;;
    esac
done

if [ "${#ARGS[@]}" -ne 1 ]; then
    usage >&2
    exit 2
fi

PDF="${ARGS[0]}"
if [ ! -f "$PDF" ]; then
    echo "错误：PDF 不存在：$PDF" >&2
    exit 3
fi
if [ ! -r "$PDF" ]; then
    echo "错误：PDF 不可读：$PDF" >&2
    exit 3
fi
if [ "$(head -c 5 "$PDF" 2>/dev/null || true)" != "%PDF-" ]; then
    echo "错误：不是 PDF 文件（缺少 %PDF- 头）：$PDF" >&2
    exit 3
fi
if ! command -v pdffonts >/dev/null 2>&1; then
    echo "错误：找不到 pdffonts，无法核对 PDF 实际字体。" >&2
    echo "安装 poppler（macOS: brew install poppler；Ubuntu: apt install poppler-utils）后重试。" >&2
    exit 3
fi

if ! RAW="$(pdffonts "$PDF" 2>&1)"; then
    echo "错误：pdffonts 无法解析该 PDF：" >&2
    printf '%s\n' "$RAW" >&2
    exit 3
fi

# 去掉子集前缀（如 "BAAAAA+LiberationSerif" -> "LiberationSerif"）。
strip_subset() {
    local name="$1"
    if [[ "$name" =~ ^[A-Z]{6}\+ ]]; then
        name="${name:7}"
    fi
    printf '%s' "$name"
}

# 判定单个字体名；输出 ok / base14 / bad，以及匹配到的白名单类别。
classify_font() {
    local raw="$1"
    local name lower
    name="$(strip_subset "$raw")"
    lower="$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]')"
    case "$name" in
        宋体*) printf 'ok\tSimSun' ; return ;;
    esac
    case "$lower" in
        timesnewroman*|timesnewromanps*|timesnewroman-bold*|timesnewroman-italic*|timesnewromanbold*)
            printf 'ok\tTimes New Roman' ; return ;;
        times|timesroman|times-roman|times-bold|times-italic|times-bolditalic)
            printf 'base14\tTimes' ; return ;;
        simsun*|nsimsun*)
            printf 'ok\tSimSun' ; return ;;
        symbol*)
            printf 'ok\tSymbol' ; return ;;
        opensymbol*)
            printf 'ok\tSymbol（项目符号）' ; return ;;
        cambriamath*|cambria-*)
            printf 'math\tCambria Math' ; return ;;
        texgyre*|tex-gyre*)
            printf 'ok\tTeX Gyre' ; return ;;
        liberation*|carlito*|caladea*|linuxlibertineg*|frankruhlhofshi*)
            printf 'sub\tLibreOffice 替换字体' ; return ;;
        *)
            printf 'bad\t-' ; return ;;
    esac
}

TOTAL=0
BAD=0
BASE14=0
SUB=0
MATHBAD=0
ROWS=""

# pdffonts 表格前两行是表头与分隔线；用 awk 从行尾取 emb 列，
# 用 BSD/GNU awk 都支持的 match()/RSTART 从行首取字体名。
while IFS= read -r line; do
    [ -z "$line" ] && continue
    name="$(printf '%s\n' "$line" | awk '
        {
            if (match($0, / (TrueType|Type 1|Type 3|CID TrueType|CID Type 0C|CID Type 0|Type 0)/)) {
                name = substr($0, 1, RSTART - 1)
            } else {
                name = $1
            }
            sub(/[[:space:]]+$/, "", name)
            print name
        }')"
    emb="$(printf '%s\n' "$line" | awk '{ if (NF >= 5) print $(NF-4); else print "?" }')"
    verdict="$(classify_font "$name")"
    status="${verdict%%$'\t'*}"
    family="${verdict#*$'\t'}"
    TOTAL=$((TOTAL + 1))
    if [ "$status" = "bad" ]; then
        BAD=$((BAD + 1))
        ROWS+="  错误  $(printf '%-34s' "$name") emb=${emb:-?}  非白名单字体（应为 Times New Roman / SimSun / Symbol / TeX Gyre）"$'\n'
    elif [ "$status" = "math" ]; then
        BAD=$((BAD + 1))
        MATHBAD=$((MATHBAD + 1))
        ROWS+="  错误  $(printf '%-34s' "$name") emb=${emb:-?}  公式回退成 Cambria Math，应为 Times New Roman"$'\n'
    elif [ "$status" = "sub" ]; then
        BAD=$((BAD + 1))
        SUB=$((SUB + 1))
        ROWS+="  错误  $(printf '%-34s' "$name") emb=${emb:-?}  LibreOffice 默认把 Times New Roman 等替换成 $family"$'\n'
    elif [ "$status" = "base14" ]; then
        BASE14=$((BASE14 + 1))
        ROWS+="  提示  $(printf '%-34s' "$name") emb=${emb:-?}  PDF Base-14 ${family}，未嵌入（跨机器可能变化）"$'\n'
    elif [ "$emb" != "yes" ]; then
        BAD=$((BAD + 1))
        ROWS+="  错误  $(printf '%-34s' "$name") emb=${emb:-?}  $family 未嵌入，打印/换机可能被替换"$'\n'
    else
        ROWS+="  通过  $(printf '%-34s' "$name") emb=yes  $family"$'\n'
    fi
done < <(printf '%s\n' "$RAW" | tail -n +3)

echo "== check_pdf_fonts.sh =="
echo "PDF：$PDF"
if command -v pdfinfo >/dev/null 2>&1; then
    PAGES="$(pdfinfo "$PDF" 2>/dev/null | awk '/^Pages:/ {print $2}' || true)"
    [ -n "${PAGES:-}" ] && echo "页数：$PAGES"
fi
echo
if [ "$LIST" -eq 1 ]; then
    echo "-- pdffonts 原始输出 --"
    printf '%s\n' "$RAW"
    echo
fi

echo "-- 字体判定（共 $TOTAL 个）--"
if [ "$TOTAL" -eq 0 ]; then
    echo "  （未检测到任何字体：整份 PDF 可能是扫描图片，无法核对字体）"
else
    printf '%s' "$ROWS"
fi

echo
echo "== 结果 =="
if [ "$TOTAL" -eq 0 ]; then
    echo "FAIL：PDF 未检测到任何字体；确认报告正文不是扫描图片替代。"
    exit 1
fi
if [ "$BAD" -gt 0 ]; then
    echo "FAIL：$BAD 个字体不合规（共 $TOTAL 个）。"
    echo "处理：在装有 Times New Roman / SimSun 的机器上重新导出；或用 Word「另存为 PDF」并嵌入字体。"
    if [ "$SUB" -gt 0 ]; then
        echo "其中 $SUB 个来自 LibreOffice 的默认字体替换（Liberation/Carlito/Caladea/Linux Libertine）。"
        echo "LibreOffice 导出的 PDF 不能用于最终提交；用 Word「另存为 PDF」，或只在 Word 中导出。"
    fi
    if [ "$MATHBAD" -gt 0 ]; then
        echo "其中 $MATHBAD 个是公式回退到 Cambria Math：检查 DOCX 里 OMML 是否被 Word 改了 math-font，"
        echo "用 python3 scripts/check_docx.py 复核，并在 Word 中把公式字体设回 Times New Roman。"
    fi
    exit 1
fi
if [ "$BASE14" -gt 0 ]; then
    echo "PASS（$TOTAL 个字体均在白名单；其中 $BASE14 个为未嵌入的 Base-14，建议嵌入）。"
else
    echo "PASS（$TOTAL 个字体均在白名单）。"
fi
exit 0