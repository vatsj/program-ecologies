"""Timing probe: python3 tools/beh_probe.py CELL N I GENS [key=value ...]  (overrides cell fields, e.g. log=0)."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import hooks_beh_run as R

cell = sys.argv[1]
N, I, G = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
c = dict(R.CELLS[cell]); c.update(N=N, I=I, gens=G)
for kv in sys.argv[5:]:
    k, v = kv.split('=')
    c[k] = int(v)
R.CELLS['probe'] = c
R.setup()
t = time.time()
row = R.run_one('probe', 1000)
print(cell, N, I, G, c, 'wall %.1f' % (time.time() - t), 'run wall', row['wall'], 'types', row['ntypes'], 'states', row['states'], 'ev', row['ev_size'], 'ev2', row['ev2_size'],
      'eff', row['eff_islands'], 'counters', row['counters'][:24], flush=True)
