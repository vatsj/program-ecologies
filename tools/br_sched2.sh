#!/bin/bash
# Queue scheduler for queue 76 step 2.  Fills free Daytona slots (max 5 live clients: `daytona_run.py run` or
# `daytona_fetch.py`) from the queue file (one chunk name per line; job list runs/br_jobs/<name>.txt, rows to
# runs/br_rows/<name>), clients detached with setsid so that they survive this script.  Then waits and exits (waking the
# caller) as soon as the live-client count drops below its value after filling, or the queue is empty and a slot is free.
# usage: tools/lpt_sched.sh QUEUEFILE LOGDIR
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
  echo "launched $c"; sleep 15
done
n0=$(count)
echo "live clients $n0, queue $(wc -l < "$Q")"
while true; do
  n=$(count)
  if [ "$n" -lt "$n0" ]; then echo "a client finished (live $n)"; exit 0; fi
  sleep 30
done
