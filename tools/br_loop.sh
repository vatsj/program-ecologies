#!/bin/bash
# Foreground loop (<= 9 min): fill free slots from the queue, logging sandbox ids; returns early when the queue is empty.
cd "$(dirname "$0")/.."
end=$(( $(date +%s) + 540 ))
while [ "$(date +%s)" -lt "$end" ]; do
  if [ "$(pgrep -fc 'daytona_run.py run|daytona_fetch.py')" -lt 5 ] && [ -s runs/br_launch/queue.txt ]; then
    tools/br_cycle.sh | grep "="
  fi
  [ -s runs/br_launch/queue.txt ] || { echo "queue empty"; break; }
  sleep 30
done
echo "live: $(pgrep -fc 'daytona_run.py run|daytona_fetch.py'); queue: $(wc -l < runs/br_launch/queue.txt)"
