#!/bin/bash
# Fill free Daytona slots (max 5 live clients) from the queue file; clients are started from this (foreground) call with setsid so that they
# survive the caller.  usage: tools/br_fill.sh QUEUEFILE LOGDIR
Q=$1; LOG=$2
cd "$(dirname "$0")/.."
count() { pgrep -fc "daytona_run.py run|daytona_fetch.py"; }
while [ "$(count)" -lt 5 ] && [ -s "$Q" ]; do
  c=$(head -n 1 "$Q"); sed -i 1d "$Q"
  S1=""; case "$c" in lps*) S1="--step2 runs/bully_resist/step2.json";; esac
  if [ "$c" = "r2" ]; then
    setsid nohup python3 tools/daytona_run.py run --cpus 4 --out runs/lt_prior_br/e_R2 -- bash tools/br_r2.sh > "$LOG/dt_$c.log" 2>&1 < /dev/null &
  else
    setsid nohup python3 tools/daytona_run.py run --cpus 4 --out runs/br_rows/$c -- python3 src/bully_resist_run.py run runs/br_jobs/$c.txt runs/br_rows/$c $S1 > "$LOG/dt_$c.log" 2>&1 < /dev/null &
  fi
  echo "launched $c"; echo "$(date -u +%FT%TZ) launched $c" >> "$LOG/launch.log"; sleep 20
done
echo "live clients $(count), queue $(wc -l < "$Q")"
