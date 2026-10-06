#!/bin/zsh
# Runs the bridge-less rivals lottery cells in the spec's priority order on 3 workers.
cd "$(dirname "$0")/.."
for e in iid dense nobridge sparse; do
  python3 src/bridgeless_rivals.py run --exp $e --ref --procs 3 > runs/log_bridgeless_$e.txt 2>&1 || echo "FAILED $e" >> runs/log_bridgeless_status.txt
  echo "done $e $(date)" >> runs/log_bridgeless_status.txt
done
for e in nat scale; do
  python3 src/bridgeless_rivals.py run --exp $e --procs 3 > runs/log_bridgeless_$e.txt 2>&1 || echo "FAILED $e" >> runs/log_bridgeless_status.txt
  echo "done $e $(date)" >> runs/log_bridgeless_status.txt
done
