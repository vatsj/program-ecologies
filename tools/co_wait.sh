#!/bin/bash
# Queue 79: exit as soon as fewer than N daytona clients are live, or after MAXMIN minutes (run in the background as a waiter).
# usage: tools/co_wait.sh N [MAXMIN]
N=${1:-5}; MAXM=${2:-110}
end=$(( $(date +%s) + MAXM * 60 ))
while [ "$(pgrep -fc "daytona_run.py run|daytona_fetch.py")" -ge "$N" ] && [ "$(date +%s)" -lt "$end" ]; do sleep 30; done
echo "live clients: $(pgrep -fc "daytona_run.py run|daytona_fetch.py")"
