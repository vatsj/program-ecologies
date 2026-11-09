#!/bin/bash
# Exit as soon as fewer than N daytona clients are live (run with run_in_background; timeout 7200000).  usage: tools/br_wait.sh N
N=${1:-5}
while [ "$(pgrep -fc "daytona_run.py run|daytona_fetch.py")" -ge "$N" ]; do sleep 30; done
echo "live clients below $N"
