#!/bin/bash
# Queue 78: fill free slots from runs/pa_launch/queue.txt and append the sandbox id of every new launch to runs/pa_launch/launch.log.
cd "$(dirname "$0")/.."
mkdir -p runs/pa_launch; touch runs/pa_launch/launch.log
before=$(grep -c launched runs/pa_launch/launch.log)
tools/pa_fill.sh runs/pa_launch/queue.txt runs/pa_launch
sleep 40
for c in $(grep launched runs/pa_launch/launch.log | tail -n +$((before + 1)) | awk '{print $3}'); do
  sid=$(grep -h sandbox "runs/pa_launch/dt_$c.log" | head -1 | awk '{print $3}')
  echo "$sid = $c" >> runs/pa_launch/launch.log
  echo "$sid = $c"
done
echo "live: $(pgrep -fc 'daytona_run.py run|daytona_fetch.py'); queue: $(wc -l < runs/pa_launch/queue.txt)"
