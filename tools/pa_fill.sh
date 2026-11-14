#!/bin/bash
# Queue 78: fill free Daytona slots (max 5 live clients) from the queue file; clients detached with setsid so that they survive the caller.
# usage: tools/pa_fill.sh QUEUEFILE LOGDIR
Q=$1; LOG=$2
cd "$(dirname "$0")/.."
count() { pgrep -fc "daytona_run.py run|daytona_fetch.py"; }
while [ "$(count)" -lt 5 ] && [ -s "$Q" ]; do
  c=$(head -n 1 "$Q"); sed -i 1d "$Q"
  S2=""; case "$c" in lps*) S2="--step2 runs/patient_accepter/step1_law.json";; esac
  if [ "${c:0:2}" = "mc" ]; then
    setsid nohup python3 tools/daytona_run.py run --cpus 4 --out runs/patient_accepter/$c -- bash tools/pa_mc.sh $c > "$LOG/dt_$c.log" 2>&1 < /dev/null &
  else
    setsid nohup python3 tools/daytona_run.py run --cpus 4 --out runs/pa_rows/$c -- python3 src/patient_accepter_run.py run runs/pa_jobs/$c.txt runs/pa_rows/$c $S2 > "$LOG/dt_$c.log" 2>&1 < /dev/null &
  fi
  echo "$(date -u +%FT%TZ) launched $c" >> "$LOG/launch.log"; echo "launched $c"; sleep 20
done
echo "live clients $(count), queue $(wc -l < "$Q")"
