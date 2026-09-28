"""Cool check: per-island payoff dispersion vs migration rate (Chicken without
ROLE by default).  Uses islands.run_one; writes runs/cool_check.md/json.

    python3 src/cool_check.py
"""
import argparse, json, os, sys
import numpy as np
from multiprocessing import Pool
from scipy.stats import spearmanr
sys.path.insert(0, os.path.dirname(__file__))
from islands import run_one, _load, ROOT


def main(a):
    jobs = [(a.game, a.norole, 'complete', mN, 'programs', 0, 6400 // N, N, a.w, a.gens, 20)
            for N, grid in ((100, a.mN100), (400, a.mN400)) for mN in grid]
    _load(a.game, a.norole)
    with Pool(a.procs) as pool:
        rows = pool.map(run_one, jobs)
    for r, j in zip(rows, jobs):
        r['N'] = j[7]; r['I'] = j[6]
        for k in [k for k in r if k.startswith('trace') or k in ('trans', 'dom_time', 'final_classes')]:
            r.pop(k)
    json.dump(rows, open(os.path.join(ROOT, 'runs', 'cool_check.json'), 'w'))
    L = ['# Cool check: payoff dispersion per island vs migration rate (%s%s, complete graph, programs seeding, rep 0, %d generations, second half)' % (a.game, ' without ROLE' if a.norole else '', a.gens), '',
         'spread = agent-weighted SD of payoff on an island (0 iff cool); resident range = max - min payoff over classes with >= 5% of the island; load = payoff(smallest mN) - payoff(mN) at the same N; cool = share of island-samples with spread 0.', '',
         '| N | I | mN | spread | resident range | cool | mean payoff | load | P(Swerve,Swerve) | frozen at | within-run corr(spread, payoff) |', '|---|---|---|---|---|---|---|---|---|---|---|']
    for N in (100, 400):
        sub = sorted([r for r in rows if r['N'] == N], key=lambda r: r['mN'])
        base = sub[0]['pay_2nd']
        for r in sub:
            P = np.array(r['spread_pay_pairs'])
            c = np.corrcoef(P[:, 0], P[:, 1])[0, 1] if len(P) > 2 and P[:, 0].std() > 0 else float('nan')
            r['load'] = base - r['pay_2nd']; r['corr'] = c
            L.append('| %d | %d | %g | %.3f | %.3f | %.2f | %.3f | %.3f | %.3f | %s | %.2f |' % (
                N, r['I'], r['mN'], r['spread'], r['resident_range'], r['cool_frac'], r['pay_2nd'], r['load'], r['pcc_2nd'], r['frozen_at'] if r['frozen_at'] >= 0 else '-', c))
        if len(sub) > 2:
            rs = spearmanr([r['spread'] for r in sub], [r['load'] for r in sub]).correlation
            L.append(''); L.append('N = %d: Spearman(spread, load) across mN = %.2f' % (N, rs)); L.append('')
    open(os.path.join(ROOT, 'runs', 'cool_check.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default='chicken_norole')
    ap.add_argument('--norole', action='store_true', default=True)
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--gens', type=int, default=50000)
    ap.add_argument('--mN100', type=float, nargs='+', default=[0.01, 0.03, 0.1, 0.3, 1, 3])
    ap.add_argument('--mN400', type=float, nargs='+', default=[0.01, 0.1, 1])
    ap.add_argument('--procs', type=int, default=9)
    main(ap.parse_args())
