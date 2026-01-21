#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
DOCS_DIR="${ROOT_DIR}/docs"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "Missing venv at ${VENV_DIR}. Create it first: python3 -m venv .venv" >&2
  exit 1
fi

# Activate venv
source "${VENV_DIR}/bin/activate"

# Ensure dependencies are installed (safe to re-run)
# python3 -m pip install -r "${DOCS_DIR}/requirements.txt"

# Build Chinese and English docs
python3 -m sphinx -b html -D language=zh_CN -c "${DOCS_DIR}" "${DOCS_DIR}/zh" "${DOCS_DIR}/_build/html/zh"
python3 -m sphinx -b html -D language=en -c "${DOCS_DIR}" "${DOCS_DIR}/en" "${DOCS_DIR}/_build/html/en"

echo "Build complete:"
echo "  ${DOCS_DIR}/_build/html/zh"
echo "  ${DOCS_DIR}/_build/html/en"
