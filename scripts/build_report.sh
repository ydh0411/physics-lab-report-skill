#!/bin/bash
# Build a physics lab report PDF from a .tex source file.
# Usage: ./build_report.sh file.tex ["output_filename.pdf"]

set -euo pipefail

TEX_FILE="${1:-}"
OUTPUT_NAME="${2:-}"

if [ -z "$TEX_FILE" ]; then
    echo "Usage: build_report.sh <file.tex> [output_filename.pdf]"
    echo "  file.tex           — LaTeX source file (required)"
    echo "  output_filename.pdf — final PDF name (optional, defaults to <file>.pdf)"
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

BASENAME="$(basename "$TEX_FILE" .tex)"
WORK_DIR="$(dirname "$TEX_FILE")"

echo "==> Compiling $TEX_FILE with XeLaTeX (pass 1/2)..."
cd "$WORK_DIR"
xelatex -interaction=nonstopmode "$(basename "$TEX_FILE")" > /dev/null

echo "==> Compiling with XeLaTeX (pass 2/2)..."
xelatex -interaction=nonstopmode "$(basename "$TEX_FILE")" > /dev/null

# Check if PDF was produced
if [ ! -f "${BASENAME}.pdf" ]; then
    echo "Error: ${BASENAME}.pdf was not generated. Check .log file for errors."
    exit 1
fi

# Clean auxiliary files
echo "==> Cleaning auxiliary files..."
rm -f "${BASENAME}.aux" "${BASENAME}.log" "${BASENAME}.out" \
      "${BASENAME}.toc" "${BASENAME}.synctex.gz" \
      "${BASENAME}.fdb_latexmk" "${BASENAME}.fls"

# Rename if output name specified
if [ -n "$OUTPUT_NAME" ]; then
    echo "==> Renaming to $OUTPUT_NAME..."
    mv "${BASENAME}.pdf" "$OUTPUT_NAME"
    echo "==> Done: $OUTPUT_NAME"
else
    echo "==> Done: ${BASENAME}.pdf"
fi
