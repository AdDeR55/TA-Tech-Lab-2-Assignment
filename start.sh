#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo "Error: python3 (or python) is not in PATH." >&2
    exit 1
fi

$PY setup.py "$@"
