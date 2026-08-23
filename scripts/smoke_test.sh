#!/bin/bash
# Compile both golden templates with disposable placeholder PDFs.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"

if ! command -v xelatex >/dev/null 2>&1; then
    echo "SKIP: xelatex is not installed"
    exit 0
fi

TEST_DIR="$(mktemp -d "${TMPDIR:-/tmp}/physics-lab-smoke.XXXXXX")"
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT INT TERM

cp "$ROOT_DIR/templates/prelab_template.tex" "$TEST_DIR/prelab.tex"
cp "$ROOT_DIR/templates/postlab_template.tex" "$TEST_DIR/postlab.tex"

printf '%s\n' \
    '\documentclass[a4paper]{article}' \
    '\pagestyle{empty}' \
    '\begin{document}' \
    '\null' \
    '\end{document}' > "$TEST_DIR/placeholder.tex"

xelatex -interaction=nonstopmode -halt-on-error -output-directory="$TEST_DIR" \
    "$TEST_DIR/placeholder.tex" >/dev/null
cp "$TEST_DIR/placeholder.pdf" "$TEST_DIR/01-Template for Prelab work-2026.pdf"
cp "$TEST_DIR/placeholder.pdf" "$TEST_DIR/02-Template for lab report-2026.pdf"
cp "$TEST_DIR/placeholder.pdf" "$TEST_DIR/scanned-data.pdf"

bash "$ROOT_DIR/scripts/build_report.sh" "$TEST_DIR/prelab.tex" "prelab-smoke.pdf"
bash "$ROOT_DIR/scripts/build_report.sh" "$TEST_DIR/postlab.tex" "postlab-smoke.pdf"

test -s "$TEST_DIR/prelab-smoke.pdf"
test -s "$TEST_DIR/postlab-smoke.pdf"
test ! -e "$TEST_DIR/prelab.aux"
test ! -e "$TEST_DIR/prelab.log"
test ! -e "$TEST_DIR/postlab.aux"
test ! -e "$TEST_DIR/postlab.log"

BEFORE_CKSUM="$(cksum "$TEST_DIR/prelab-smoke.pdf")"
if bash "$ROOT_DIR/scripts/build_report.sh" "$TEST_DIR/prelab.tex" "prelab-smoke.pdf"; then
    echo "FAIL: build_report.sh overwrote an existing PDF without --force"
    exit 1
fi
AFTER_CKSUM="$(cksum "$TEST_DIR/prelab-smoke.pdf")"
test "$BEFORE_CKSUM" = "$AFTER_CKSUM"

bash "$ROOT_DIR/scripts/build_report.sh" --force "$TEST_DIR/prelab.tex" "prelab-smoke.pdf"
test -s "$TEST_DIR/prelab-smoke.pdf"

echo "PASS: both templates compile and overwrite protection works"
