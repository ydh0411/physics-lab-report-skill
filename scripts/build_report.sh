#!/bin/bash
# Build a physics lab report PDF from a .tex source file.
# Usage: ./build_report.sh [--force] file.tex ["output_filename.pdf"]

set -euo pipefail

FORCE=0
if [ "${1:-}" = "--force" ]; then
    FORCE=1
    shift
fi

TEX_FILE="${1:-}"
OUTPUT_NAME="${2:-}"

if [ -z "$TEX_FILE" ] || [ "$#" -gt 2 ]; then
    echo "Usage: build_report.sh [--force] <file.tex> [output_filename.pdf]"
    echo "  file.tex           — LaTeX source file (required)"
    echo "  output_filename.pdf — final PDF name (optional, defaults to <file>.pdf)"
    echo "  --force             — overwrite an existing output PDF"
    exit 1
fi

if [ ! -f "$TEX_FILE" ]; then
    echo "Error: $TEX_FILE not found"
    exit 1
fi

# Check XeLaTeX availability
if ! command -v xelatex &> /dev/null; then
    echo "Error: xelatex not found. Install TeX distribution (e.g., MacTeX on macOS)."
    exit 1
fi

TEX_NAME="$(basename "$TEX_FILE")"
BASENAME="$(basename "$TEX_FILE" .tex)"
WORK_DIR="$(cd "$(dirname "$TEX_FILE")" && pwd -P)"

if [ -z "$OUTPUT_NAME" ]; then
    OUTPUT_PATH="${WORK_DIR}/${BASENAME}.pdf"
elif [ "${OUTPUT_NAME#/}" != "$OUTPUT_NAME" ]; then
    OUTPUT_PATH="$OUTPUT_NAME"
else
    OUTPUT_PATH="${WORK_DIR}/${OUTPUT_NAME}"
fi

case "$OUTPUT_PATH" in
    *.pdf) ;;
    *)
        echo "Error: output filename must end with .pdf"
        exit 1
        ;;
esac

if [ ! -d "$(dirname "$OUTPUT_PATH")" ]; then
    echo "Error: output directory does not exist: $(dirname "$OUTPUT_PATH")"
    exit 1
fi

if [ -e "$OUTPUT_PATH" ] && [ "$FORCE" -ne 1 ]; then
    echo "Error: output already exists: $OUTPUT_PATH"
    echo "Use --force only after confirming that it is safe to overwrite."
    exit 1
fi

BUILD_DIR="$(mktemp -d "${TMPDIR:-/tmp}/physics-lab-report.XXXXXX")"
cleanup() {
    rm -rf "$BUILD_DIR"
}
trap cleanup EXIT INT TERM

echo "==> Compiling $TEX_FILE with XeLaTeX (pass 1/2)..."
cd "$WORK_DIR"
if ! xelatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" "$TEX_NAME" > /dev/null; then
    echo "Error: XeLaTeX failed on pass 1. Last log lines:" >&2
    tail -n 40 "${BUILD_DIR}/${BASENAME}.log" >&2 || true
    exit 1
fi

echo "==> Compiling with XeLaTeX (pass 2/2)..."
if ! xelatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" "$TEX_NAME" > /dev/null; then
    echo "Error: XeLaTeX failed on pass 2. Last log lines:" >&2
    tail -n 40 "${BUILD_DIR}/${BASENAME}.log" >&2 || true
    exit 1
fi

# Check if PDF was produced
if [ ! -f "${BUILD_DIR}/${BASENAME}.pdf" ]; then
    echo "Error: ${BASENAME}.pdf was not generated."
    exit 1
fi

echo "==> Writing $OUTPUT_PATH..."
mv "${BUILD_DIR}/${BASENAME}.pdf" "$OUTPUT_PATH"
echo "==> Done: $OUTPUT_PATH"
