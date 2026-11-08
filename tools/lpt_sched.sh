#!/bin/bash
# Queue scheduler for queue 75 step 2: keeps up to 5 Daytona clients running, launching the next chunk from the queue file
# (one `chunk-name` per line, a job list runs/lpt_jobs/<name>.txt, rows to runs/lpt_rows/<name>) whenever a slot is free.
# Exits (so that the caller is woken) when the queue file is empty AND fewer than 5 clients run, or when the stop file exists.
# usage: tools/lpt_sched.sh QUEUEFILE LOGDIR
Q=$1; LOG=$2
cd "$(dirname "$0")/.."
while true; do
  n=$(pgrep -fc "daytona_run.py run")
  if [ -f "$Q.stop" ]; then echo "stop file"; exit 0; fi
  if [ "$n" -lt 5 ] && [ -s "$Q" ]; then
    c=$(head -n 1 "$Q"); sed -i 1d "$Q"
    nohup python3 tools/daytona_run.py run --cpus 4 --out runs/lpt_rows/$c -- python3 src/length_prior_t_run.py run runs/lpt_jobs/$c.txt runs/lpt_rows/$c > "$LOG/dt_$c.log" 2>&1 &
    echo "launched $c"; sleep 20; continue
  fi
  if [ ! -s "$Q" ] && [ "$n" -lt 5 ]; then echo "queue empty, free slot"; exit 0; fi
  sleep 30
done
