"""Decomposition of the refusal bit's frequency change (added after the R1 cells; no prediction is scored on it).

For every island and 50-generation window: the change of the island's mean bit frequency, the window's contract
events on the island (guarded offers refused / guarded offers that went through / unguarded installations), and the
island's state (on a V* member at the window start or not).  Sums of the change by category show where the
metapopulation's rise comes from.  Also: the change by the island's own bit frequency relative to the run mean
(immigrant rescue predicts gains on low-bit islands that are moving, none lost on high-bit islands that are stuck).
    python3 src/dominance_contracts_refusal.py CELL [CELL ...]  -> runs/dominance_contracts/refusal_<CELL>.json
"""
import json, os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_sets as SS
import dominance_contracts_run as DR


def decompose(cell, nruns=40):
    T = DR.tables(); V = np.array(sorted(SS.symmetric_set(T.R, 6)))
    nout = len(T.R)
    tot = defaultdict(lambda: [0.0, 0])
    bylevel = defaultdict(lambda: [0.0, 0])
    for r in range(nruns):
        f = os.path.join(DR.OUT, cell, 'r%d.npz' % r)
        if not os.path.exists(f):
            continue
        z = np.load(f)
        rf = z['rfreq'].astype(float)          # every 50 generations
        cls = z['cls']; cev = z['cev']
        nw = rf.shape[0] - 1
        I = rf.shape[1]
        ev = defaultdict(set)
        for row in cev:
            g, i, st, guard = int(row[0]), int(row[1]), int(row[3]), row[10] > 0
            w = g // 50
            if guard and st == 1: ev[(i, w)].add('refused')
            elif guard and st == 2: ev[(i, w)].add('guarded-through')
            elif st == 2: ev[(i, w)].add('unguarded-install')
        for w in range(nw):
            g0 = w * 50
            rbar = rf[w].mean()
            for i in range(I):
                d = rf[w + 1, i].mean() - rf[w, i].mean()
                mem = (cls[g0, i] in V) or cls[g0, i] == nout
                e = ev.get((i, w), set())
                key = ('member' if mem else 'non-member') + '|' + (
                    'guarded-through' if 'guarded-through' in e else ('refused' if 'refused' in e else
                                                                     ('unguarded-install' if 'unguarded-install' in e else 'none')))
                tot[key][0] += d; tot[key][1] += 1
                lvl = 'below' if rf[w, i].mean() < rbar else 'above'
                bylevel[lvl + '|' + ('member' if mem else 'non-member')][0] += d
                bylevel[lvl + '|' + ('member' if mem else 'non-member')][1] += 1
    nr = sum(1 for r in range(nruns) if os.path.exists(os.path.join(DR.OUT, cell, 'r%d.npz' % r)))
    out = dict(cell=cell, runs=nr,
               by_event={k: dict(sum_per_run_per_island=v[0] / nr / 64, windows=v[1], mean=v[0] / max(v[1], 1)) for k, v in sorted(tot.items())},
               by_level={k: dict(sum_per_run_per_island=v[0] / nr / 64, windows=v[1], mean=v[0] / max(v[1], 1)) for k, v in sorted(bylevel.items())})
    json.dump(out, open(os.path.join(DR.OUT, 'refusal_%s.json' % cell), 'w'), indent=1)
    return out


if __name__ == '__main__':
    for c in sys.argv[1:]:
        o = decompose(c)
        print(c)
        for k, v in o['by_event'].items():
            print('  %-35s sum %.4f  windows %d  mean %.5f' % (k, v['sum_per_run_per_island'], v['windows'], v['mean']))
        for k, v in o['by_level'].items():
            print('  %-35s sum %.4f  windows %d  mean %.5f' % (k, v['sum_per_run_per_island'], v['windows'], v['mean']))
