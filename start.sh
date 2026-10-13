#!/usr/bin/env bash
# start.sh -- Campus IT Service Desk Handover Lab
# Run from the repository root: bash start.sh
set -e
cd "$(dirname "$0")"

# Detect Python 3 (Windows Git Bash uses "python"; Linux/Codespace uses "python3")
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo "Error: python3 (or python) is not in PATH." >&2
    exit 1
fi

$PY setup.py "$@"
