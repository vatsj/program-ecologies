#!/bin/bash
# Reattach fetch clients to running sandboxes: tools/br_reattach.sh SANDBOX_ID:OUTDIR ...  (OUTDIR repo-relative)
cd "$(dirname "$0")/.."
for pair in "$@"; do
  sid=${pair%%:*}
  out=${pair##*:}
  name=$(basename "$out")
  setsid nohup python3 tools/daytona_fetch.py "$sid" "$out" --poll 60 > "runs/br_launch/fetch_$name.log" 2>&1 < /dev/null &
  echo "reattached $sid -> $out"
done
