#!/bin/bash
# Queue 80: keep the Daytona slots filled from runs/sco_launch/queue.txt until it is empty.
cd "$(dirname "$0")/.."
while [ -s runs/sco_launch/queue.txt ]; do
  while [ "$(pgrep -fc 'daytona_run.py run|daytona_fetch.py')" -ge "${SCO_SLOTS:-5}" ]; do sleep 60; done
  bash tools/sco_fill.sh
done
echo "queue empty; live clients $(pgrep -fc 'daytona_run.py run|daytona_fetch.py')"
