#!/bin/sh
# usage: watch.sh LOG INTERVAL STOPFILE  -- prints a progress line every INTERVAL seconds; exits on error or STOPFILE
f=$1; iv=$2; stop=$3
while true; do
  n=$(grep -c " rep " "$f")
  echo "$(date +%H:%M) $(basename $f) rows $n; $(tail -1 "$f" | cut -c1-90)"
  if grep -q "Traceback\|Error" "$f"; then grep -m3 "Traceback\|Error" "$f"; exit 1; fi
  [ -e "$stop" ] && exit 0
  sleep "$iv"
done
