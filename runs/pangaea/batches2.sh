#!/bin/zsh
# Replaces the tail of batches.sh (stopped after its batch A started): wait for batch A's pool (pid 79195), validate
# the copier no-change cache and rerun the tests, then the remaining batches in the original order.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-adf253ba407add1ea
P=src/pangaea_run.py
while ps -p 79195 > /dev/null; do sleep 30; done
python3 $P cachecheck > runs/pangaea/cachecheck.log 2>&1 || exit 8
python3 -m pytest -q tests/test_pangaea.py > runs/pangaea/pytest.log 2>&1 || exit 9
python3 $P lottery --cells G --ext 0 --out G > runs/pangaea/lottery_G.log 2>&1 || exit 7
python3 $P lottery --cells F pg_prop_12800_1_r100 pg_prop_6400_1_r100 --ext 1 --out F > runs/pangaea/lottery_F.log 2>&1 || exit 2
python3 $P lottery --cells pg_prop_100_128_r100 pg_prop_200_64_r100 pg_prop_800_16_r100 pg_prop_3200_4_r100 B2 --ext 2 --out B > runs/pangaea/lottery_B.log 2>&1 || exit 3
python3 $P lottery --cells E --ext 0 --out E > runs/pangaea/lottery_E.log 2>&1 || exit 4
python3 $P lottery --cells D --ext 0 --out D > runs/pangaea/lottery_D.log 2>&1 || exit 5
python3 $P lottery --cells D2 --ext 0 --out D2 > runs/pangaea/lottery_D2.log 2>&1 || exit 6
echo done > runs/pangaea/batches.done
