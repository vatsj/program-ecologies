#!/bin/bash
# Queue 80: fill free Daytona slots (max ${SCO_SLOTS:-5} live clients) from runs/sco_launch/queue.txt; clients detached with setsid;
# every launch is logged in runs/sco_launch/launch.log with its sandbox id.
# usage: tools/sco_fill.sh
cd "$(dirname "$0")/.."
Q=runs/sco_launch/queue.txt; LOG=runs/sco_launch; MAX=${SCO_SLOTS:-5}
mkdir -p $LOG; touch $LOG/launch.log
count() { pgrep -fc "daytona_run.py run|daytona_fetch.py"; }
new=""
while [ "$(count)" -lt "$MAX" ] && [ -s "$Q" ]; do
  c=$(head -n 1 "$Q"); sed -i 1d "$Q"
  setsid nohup python3 tools/daytona_run.py run --cpus 4 --out runs/sco_rows/$c -- python3 src/script_offers_run.py run runs/sco_jobs/$c.txt runs/sco_rows/$c > "$LOG/dt_$c.log" 2>&1 < /dev/null &
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
