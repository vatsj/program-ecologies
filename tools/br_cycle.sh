#!/bin/bash
# Fill free slots from the queue and append the sandbox id of every new launch to runs/br_launch/launch.log.
cd "$(dirname "$0")/.."
before=$(grep -c launched runs/br_launch/launch.log)
tools/br_fill.sh runs/br_launch/queue.txt runs/br_launch
sleep 20
for c in $(grep launched runs/br_launch/launch.log | tail -n +$((before + 1)) | awk '{print $3}'); do
  sid=$(grep -h sandbox "runs/br_launch/dt_$c.log" | head -1 | awk '{print $3}')
  echo "$sid = $c" >> runs/br_launch/launch.log
  echo "$sid = $c"
done
echo "live: $(pgrep -fc 'daytona_run.py run|daytona_fetch.py'); queue: $(wc -l < runs/br_launch/queue.txt)"
