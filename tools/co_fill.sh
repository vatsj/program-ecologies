#!/bin/bash
# Queue 79: fill free Daytona slots (max 5 live clients) from runs/co_launch/queue.txt; clients detached with setsid so that they survive
# the caller; every launch is logged in runs/co_launch/launch.log and the sandbox id is appended once it is known.
# usage: tools/co_fill.sh
cd "$(dirname "$0")/.."
Q=runs/co_launch/queue.txt; LOG=runs/co_launch
mkdir -p $LOG; touch $LOG/launch.log
count() { pgrep -fc "daytona_run.py run|daytona_fetch.py"; }
new=""
while [ "$(count)" -lt 5 ] && [ -s "$Q" ]; do
  c=$(head -n 1 "$Q"); sed -i 1d "$Q"
  setsid nohup python3 tools/daytona_run.py run --cpus 4 --out runs/co_rows/$c -- python3 src/certified_offers_run.py run runs/co_jobs/$c.txt runs/co_rows/$c > "$LOG/dt_$c.log" 2>&1 < /dev/null &
  echo "$(date -u +%FT%TZ) launched $c" >> "$LOG/launch.log"; echo "launched $c"; new="$new $c"; sleep 20
done
if [ -n "$new" ]; then
  sleep 40
  for c in $new; do
    sid=$(grep -h sandbox "$LOG/dt_$c.log" | head -1 | awk '{print $3}')
    echo "$sid = $c" >> "$LOG/launch.log"; echo "$sid = $c"
  done
fi
echo "live clients $(count), queue $(wc -l < "$Q")"
