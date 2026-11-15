#!/bin/bash
# Queue 79: keep the Daytona slots filled from runs/co_launch/queue.txt until it is empty (run in the background; re-arm if stopped).
cd "$(dirname "$0")/.."
while [ -s runs/co_launch/queue.txt ]; do
  bash tools/co_wait.sh 5 600 > /dev/null
  bash tools/co_fill.sh
done
echo "queue empty; live clients $(pgrep -fc 'daytona_run.py run|daytona_fetch.py')"
