"""Cost probes for notes §2 (discarded; replicate 990 for founder cells, a 2,000-generation branch for B1)."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import removing_rivals_run as RRR

if __name__ == '__main__':
    what = sys.argv[1]
    t0 = time.time()
    if what == 'branch':
        cell, rep = sys.argv[2], int(sys.argv[3])
        ck = [r for r in json.load(open(os.path.join(RRR.OUT, 'ckpt_rows.json'))) if r['cell'] == cell and r['rep'] == rep][0]
        rival0 = {i: (lab, ck['holder_unit'][i]) for i, lab in enumerate(ck['labels']) if lab not in ('', 'unheld')}
        out = RRR.branch_job((cell, rep, (0.0, 0.01, 0.1, 1.0), 2000, rival0, None))
        res = {b['epsN']: b['time_s'] for b in out['branches']}
    else:
        out = RRR.lottery_job((sys.argv[2], 990, int(sys.argv[3])))
        res = dict(time=out['time_s'], last=out['last_gen'])
    print(what, sys.argv[2:], res, 'wall %.0f' % (time.time() - t0), flush=True)
    p = os.path.join(RRR.OUT, 'probes.json')
    old = json.load(open(p)) if os.path.exists(p) else []
    old.append(dict(what=what, args=sys.argv[2:], res={str(k): v for k, v in res.items()}))
    json.dump(old, open(p, 'w'), indent=1)
