#!/usr/bin/env bash
# Run each test file in its own pytest process.
#
# Several modules (src/sog_full.py, src/sog_realizable.py, ...) extend the shared
# realizable-language library and wrapper tables at import time, so a single
# pytest process collects them in an order-dependent global state: run together,
# test_detectors fails collection with KeyError 'CHK3' and coverage_components,
# per_root, sog_full and founding_legibility raise IndexErrors. Each passes alone
# (checked 2026-11-04). Per-file processes are the supported way to run the suite.
#
# Usage: tools/run_tests.sh [-j JOBS] [test files...]   (default: all, JOBS=3)
set -u
cd "$(dirname "$0")/.."
JOBS=3
if [ "${1:-}" = "-j" ]; then JOBS=$2; shift 2; fi
FILES=("$@")
[ ${#FILES[@]} -eq 0 ] && FILES=(tests/test_*.py)
LOG=$(mktemp -d)
printf '%s\n' "${FILES[@]}" | xargs -P "$JOBS" -I{} sh -c \
  'out="$1/$(basename "$2").log"; python3 -m pytest -q -p no:cacheprovider "$2" >"$out" 2>&1; echo "$? $2" >>"$1/status"' _ "$LOG" {}
fail=0
while read -r code f; do
  if [ "$code" != 0 ] && [ "$code" != 5 ]; then
    fail=1; echo "FAIL $f"; tail -n 5 "$LOG/$(basename "$f").log"
  fi
done < "$LOG/status"
echo "$(wc -l < "$LOG/status") files; logs in $LOG"
exit $fail
