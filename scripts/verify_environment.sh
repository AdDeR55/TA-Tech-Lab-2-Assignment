#!/usr/bin/env bash
# verify_environment.sh — Check that all required tools are present.
# Run from the repository root.  Exit 0 = all tools found; exit 1 = missing.
set -e
OK=0
MISSING=()

check_tool() {
  if command -v "$1" &>/dev/null; then
    echo "  OK  $1"
  else
    echo "MISS  $1"
    MISSING+=("$1")
    OK=1
  fi
}

echo "=== Environment check ==="
check_tool bash
check_tool python3
check_tool nano
check_tool less
check_tool sort
check_tool uniq
check_tool cut
check_tool diff
check_tool grep
check_tool cat
check_tool head

echo ""
if [[ $OK -eq 0 ]]; then
  echo "All tools found.  The lab environment is ready."
else
  echo "Missing tools: ${MISSING[*]}"
  echo "Install them before running the lab."
fi

# Quick smoke test: generate and check a temp attempt
echo ""
echo "=== Smoke test (temporary attempt) ==="
TMPID="smoke-$$"
python3 setup.py --reset-work "$TMPID" 2>/dev/null || true
echo "$TMPID" | python3 setup.py 2>/dev/null && echo "Setup OK" || echo "Setup FAILED"
TMPDIR="lab-work/lab2-$TMPID"
if [[ -d "$TMPDIR" ]]; then
  pushd "$TMPDIR" > /dev/null
  python3 ../../check.py 2>&1 | tail -3
  popd > /dev/null
  rm -rf "$TMPDIR"
  echo "Smoke test complete — temp attempt removed."
fi

exit $OK
