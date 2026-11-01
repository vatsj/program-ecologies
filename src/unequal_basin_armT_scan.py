"""RE follow-up check to queue 70: arm T main-dose unequal tilt scan (predictions/2026-11-01-arm-t-tilt-scan.md).

    python3 src/unequal_basin_armT_scan.py CELL PM U OUT.json     e.g. "main|0.1|0" 0.1 0.8 out.json
Needs the arm-T founding pools in MIT_SCRATCH (src/many_islands_t_run.py P jobs)."""
import os, sys, json
for v in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS","VECLIB_MAXIMUM_THREADS","NUMBA_NUM_THREADS"): os.environ[v]="1"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import many_islands_t_ode as O
from many_islands_t_common import tabs, get_pf, load_pool
cell, pm, u = sys.argv[1], sys.argv[2], float(sys.argv[3])
T = tabs(); PF = get_pf(pm)
xs = O.symmetrize(O.hist_to_x(load_pool(cell, 0)))
x0, info = O.tilt(xs, T, 'unequal', target=u)
recs, x, st, _ = O.integrate(x0, PF, 1e5, T, sym=True, stop_converged=True)
if st != 'converged':
    recs, x, st = O.integrate_be(x, 1e5, PF, T, 1e7, sym=True, steps_per_decade=8, recs=recs)
out = dict(cell=cell, pm=pm, u=u, status=st, t_end=recs[-1]['t'], final_shares=recs[-1]['shares'],
           traj={str(r['t']): r['shares'] for r in recs if r['t'] in (0, 1e2, 1e3, 1e4, 1e5)}, before=info['before'])
json.dump(out, open(sys.argv[4], 'w'), default=float)
