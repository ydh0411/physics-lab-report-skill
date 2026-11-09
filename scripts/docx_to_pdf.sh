#!/bin/bash
# Convert a Word .docx lab report to PDF with LibreOffice (headless).
#
# Usage: bash scripts/docx_to_pdf.sh <in.docx> [out.pdf] [--force]
#
# The input .docx is read-only (never modified). LibreOffice runs with a
# throw-away user profile so it cannot touch the user's LibreOffice settings.
# The output is written only after a successful conversion; an existing PDF is
# preserved unless --force is given.
#
# 注意：LibreOffice 默认把 Microsoft 核心字体替换成度量兼容字体
# （Times New Roman -> Liberation Serif、Calibri -> Carlito、Cambria -> Caladea），
# 在本机实测导出的 PDF 里没有真正的 Times New Roman。因此本脚本适合做版式预览，
# 最终提交的 PDF 要用 Word「另存为 PDF」导出，再用 check_pdf_fonts.sh 核对。

set -euo pipefail

usage() {
    cat <<'EOF'
用法: bash scripts/docx_to_pdf.sh <in.docx> [out.pdf] [--force]

  <in.docx>   输入 Word 文件（只读，不修改）
  [out.pdf]   输出 PDF；省略时写到与输入同目录、同名的 .pdf
  --force     目标 PDF 已存在时允许覆盖（默认拒绝，防止误盖终稿）

退出码:
  0  转换成功
  1  LibreOffice 转换失败（或没有生成 PDF）
  2  参数用法错误（缺参数、输入不是 .docx、输出不是 .pdf、目录不存在）
  3  找不到 soffice（未安装 LibreOffice）
  4  目标 PDF 已存在且未给 --force

注意: LibreOffice 会把 Times New Roman 等替换成 Liberation/Carlito，
      导出的 PDF 只适合看版式；最终提交用 Word「另存为 PDF」。

下一步: bash scripts/check_pdf_fonts.sh <out.pdf>
EOF
}

FORCE=0
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --force) FORCE=1 ;;
        -h|--help) usage; exit 0 ;;
        -*) echo "错误：未知选项 $arg" >&2; usage >&2; exit 2 ;;
        *) ARGS+=("$arg") ;;
    esac
done

if [ "${#ARGS[@]}" -lt 1 ] || [ "${#ARGS[@]}" -gt 2 ]; then
    usage >&2
    exit 2
fi

INPUT="${ARGS[0]}"
if [ ! -f "$INPUT" ]; then
    echo "错误：输入文件不存在：$INPUT" >&2
    exit 2
fi
case "$INPUT" in
    *.docx|*.DOCX) ;;
    *) echo "错误：输入必须是 .docx 文件：$INPUT" >&2; exit 2 ;;
esac

if [ "${#ARGS[@]}" -eq 2 ]; then
    OUTPUT="${ARGS[1]}"
else
    OUTPUT="${INPUT%.*}.pdf"
fi
case "$OUTPUT" in
    *.pdf|*.PDF) ;;
    *) echo "错误：输出文件名必须以 .pdf 结尾：$OUTPUT" >&2; exit 2 ;;
esac
OUT_DIR="$(dirname "$OUTPUT")"
if [ ! -d "$OUT_DIR" ]; then
    echo "错误：输出目录不存在：$OUT_DIR" >&2
    exit 2
fi
if [ -e "$OUTPUT" ] && [ "$FORCE" -ne 1 ]; then
    echo "错误：目标 PDF 已存在：$OUTPUT"
    echo "确认可以覆盖后再加 --force（例如需要重导出终稿时）。"
    exit 4
fi

SOFFICE=""
if command -v soffice >/dev/null 2>&1; then
    SOFFICE="$(command -v soffice)"
elif [ -x "/Applications/LibreOffice.app/Contents/MacOS/soffice" ]; then
    SOFFICE="/Applications/LibreOffice.app/Contents/MacOS/soffice"
else
    echo "错误：找不到 soffice，无法导出 PDF。" >&2
    echo "请安装 LibreOffice（macOS: brew install --cask libreoffice）。" >&2
    exit 3
fi

WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/docx-to-pdf.XXXXXX")"
OUT_TMP="$WORK_DIR/out"
PROFILE_DIR="$WORK_DIR/profile"
mkdir -p "$OUT_TMP" "$PROFILE_DIR"
cleanup() {
    rm -rf "$WORK_DIR"
}
trap cleanup EXIT INT TERM

echo "==> 转换: $INPUT"
echo "    输出: $OUTPUT"
echo "    LibreOffice: ${SOFFICE}（临时 profile，不动用户配置）"

if ! "$SOFFICE" --headless --norestore --invisible --nodefault --nolockcheck \
    "-env:UserInstallation=file://$PROFILE_DIR" \
    --convert-to pdf:writer_pdf_Export \
    --outdir "$OUT_TMP" "$INPUT" >"$WORK_DIR/soffice.log" 2>&1; then
    echo "错误：LibreOffice 转换失败。日志末尾：" >&2
    tail -n 20 "$WORK_DIR/soffice.log" >&2 || true
    exit 1
fi

shopt -s nullglob
PDFS=("$OUT_TMP"/*.pdf)
shopt -u nullglob
if [ "${#PDFS[@]}" -eq 0 ]; then
    echo "错误：LibreOffice 没有生成 PDF。日志末尾：" >&2
    tail -n 20 "$WORK_DIR/soffice.log" >&2 || true
    exit 1
fi
if [ "${#PDFS[@]}" -gt 1 ]; then
    echo "错误：一次转换生成了多个 PDF，无法确定输出：" >&2
    printf '  %s\n' "${PDFS[@]}" >&2
    exit 1
fi
if [ ! -s "${PDFS[0]}" ]; then
    echo "错误：生成的 PDF 为空：${PDFS[0]}" >&2
    exit 1
fi

if [ -e "$OUTPUT" ]; then
    mv -f "${PDFS[0]}" "$OUTPUT"
else
    mv "${PDFS[0]}" "$OUTPUT"
fi

SIZE="$(du -h "$OUTPUT" | awk '{print $1}')"
PAGES=""
if command -v pdfinfo >/dev/null 2>&1; then
    PAGES="$(pdfinfo "$OUTPUT" 2>/dev/null | awk '/^Pages:/ {print $2}')"
fi
echo "==> 完成: ${OUTPUT}（${SIZE}${PAGES:+, ${PAGES} 页}）"
echo "==> 下一步检查字体: bash scripts/check_pdf_fonts.sh \"$OUTPUT\""