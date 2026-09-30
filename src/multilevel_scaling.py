"""Threshold w_g* (mean P(C,C) crosses 1/2) of payoff-weighted emigration, as a
function of island size N and island count I.  Per-island rates fixed:
eps N and mN per island per generation.

    python3 src/multilevel_scaling.py
Writes runs/multilevel_scaling.md/json.
"""
import argparse, json, os, sys
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from islands import run_one, _load, ROOT


def threshold(wgs, p):
    for k in range(len(wgs) - 1):
        if p[k] < 0.5 <= p[k + 1]:
            a, b = np.log(wgs[k]), np.log(wgs[k + 1])
            return float(np.exp(a + (0.5 - p[k]) / (p[k + 1] - p[k]) * (b - a)))
    return float('inf') if p[-1] < 0.5 else float(wgs[0]) if p[0] >= 0.5 else float('nan')


def main(a):
    sizes = [(64, N) for N in a.Ns] + [(I, 100) for I in a.Is if I != 64]
    jobs = [('pd', False, 'complete', a.mN, 'alld', r, I, N, a.w, a.gens, 20, a.epsN, wg)
            for (I, N) in sizes for wg in a.wg for r in range(a.reps)]
    jobs.sort(key=lambda j: -j[6] * j[7])            # big cells first
    _load('pd', False)
    rows = []
    with Pool(a.procs) as pool:
        for r in pool.imap_unordered(run_one, jobs):
            t = np.array(r.pop('trace_cc')); h = len(t) // 2
            r['pcc_1st'] = float(t[:h].mean())
            for k in ('trace_pay', 'trace_R', 'trace_C', 'trans', 'final_classes', 'spread_pay_pairs', 'dom_time', 'isl_cc_hist', 'isl_dwl_hist'):
                r.pop(k, None)
            rows.append(r)
            print('done', r['wg'], r['rep'], '%.3f' % r['pcc_2nd'], flush=True)
    json.dump(rows, open(os.path.join(ROOT, 'runs', 'multilevel_scaling.json'), 'w'), indent=1)
    report(rows, a)


def report(rows, a):
    L = ['# Multilevel threshold vs island size and count (PD, complete graph, eps N = %g and mN = %g per island per generation, start all-D, %d generations; finite eps N)' % (a.epsN, a.mN, a.gens), '',
         'Cells: mean second-half P(C,C) over %d replicates (first-half mean in parentheses). w_g* = where the mean crosses 1/2 (log-linear interpolation).' % a.reps, '',
         '| I | N | ' + ' | '.join('w_g=%g' % g for g in a.wg) + ' | w_g* |', '|' + '---|' * (len(a.wg) + 3)]
    cells = sorted({(r['I'], r['N']) for r in rows}, key=lambda c: (c[0] != 64, c[1], c[0]))
    for (I, N) in cells:
        p2 = [np.mean([r['pcc_2nd'] for r in rows if (r['I'], r['N'], r['wg']) == (I, N, g)]) for g in a.wg]
        p1 = [np.mean([r['pcc_1st'] for r in rows if (r['I'], r['N'], r['wg']) == (I, N, g)]) for g in a.wg]
        L.append('| %d | %d | %s | %.1f |' % (I, N, ' | '.join('%.3f (%.3f)' % (x, y) for x, y in zip(p2, p1)), threshold(a.wg, p2)))
    open(os.path.join(ROOT, 'runs', 'multilevel_scaling.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--Ns', type=int, nargs='+', default=[50, 100, 200])
    ap.add_argument('--Is', type=int, nargs='+', default=[16, 64, 256])
    ap.add_argument('--wg', type=float, nargs='+', default=[3, 6, 10, 15, 25])
    ap.add_argument('--reps', type=int, default=3)
    ap.add_argument('--mN', type=float, default=1.0)
    ap.add_argument('--epsN', type=float, default=0.1)
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--gens', type=int, default=200000)
    ap.add_argument('--procs', type=int, default=9)
    main(ap.parse_args())
