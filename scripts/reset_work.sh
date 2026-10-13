#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

if [[ -z "$1" ]]; then
  echo "Usage: bash scripts/reset_work.sh <student-id>"
  echo "Resets only the work/ folder for that attempt."
  echo "Evidence and mission files are never changed."
  exit 1
fi

ID="$1"
ATTEMPT="lab-work/lab2-$ID"

if [[ ! -d "$ATTEMPT" ]]; then
  echo "No attempt found at $ATTEMPT"
  echo "Run  bash start.sh  first to create one."
  exit 1
fi

WORK="$ATTEMPT/work"
if [[ ! -d "$WORK" ]]; then
  echo "No work/ folder found inside $ATTEMPT — nothing to reset."
  exit 0
fi


echo ""
echo "This will permanently delete and regenerate:"
echo "  $WORK"
echo ""
echo "Evidence files in evidence/ and mission/ will NOT be changed."
echo ""
read -r -p "Type  yes  to continue, anything else to cancel: " CONFIRM
if [[ "$CONFIRM" != "yes" ]]; then
  echo "Reset cancelled. No files were changed."
  exit 0
fi

python3 setup.py --reset-work "$ID"
echo "Reset complete."
