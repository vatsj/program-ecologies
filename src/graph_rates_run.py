"""Exp 2 of predictions/2026-10-01-priced-arm.md: entry and price-ladder rates
on the torus and hypercube vs the well-mixed reference, priced modal arm n = 8.

    python3 src/graph_rates_run.py
Writes runs/graph_rates.md/json.
"""
import json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
from graph_rates import torus, hypercube, _invade, well_mixed, ROOT

W = 0.3
CS = (0.0, 1e-2, 1e-1)
GRAPHS = [('torus', 16), ('torus', 32), ('torus', 64), ('hypercube', 6), ('hypercube', 8), ('hypercube', 10)]
PAIRS = [('entry FB|D', 'BOX(THEM(ME))', 'D'), ('entry PB|D', 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))', 'D'),
         ('ladder C|FB', 'C', 'BOX(THEM(ME))'), ('ladder FB|PB', 'BOX(THEM(ME))', 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))')]


def _job(j):
    c, kind, size, label, mut, res, trials, cap = j
    nb = torus(size) if kind == 'torus' else hypercube(size)
    N = nb.shape[0]
    t = time.time()
    if label == 'neutral':                    # measured neutral baseline on this graph
        U = np.zeros((2, 2)); s, f, u = _invade(U, nb, W, 0, 1, trials, cap, 2000 + size)
        dec = s + f; lo, hi = wilson(s, dec)
        return dict(c=c, graph=kind, size=size, N=N, pair=label, succ=s, fail=f, undec=u, trials=trials, rho=s / dec if dec else float('nan'), lo=lo, hi=hi, wm=2.0 / N, time_s=time.time() - t)
    L, val, worlds, prov = M.build_priced(8, c)
    U = np.ascontiguousarray(prov.Ufull); names = prov.names
    s = f = u = 0; tot = 0; batch = 0
    while (s < 20 and tot < 100 * trials) or tot == 0:         # adaptive: >= 20 successes or 1e5 trials
        s1, f1, u1 = _invade(U, nb, W, names.index(res), names.index(mut), trials, cap, 1000 + size + 7919 * batch)
        s += s1; f += f1; u += u1; tot += trials; batch += 1
    trials = tot
    dec = s + f                                   # undecided trials are excluded from the denominator
    lo, hi = wilson(s, dec)
    return dict(c=c, graph=kind, size=size, N=N, pair=label, succ=s, fail=f, undec=u, trials=trials,
                rho=s / dec if dec else float('nan'), lo=lo, hi=hi, wm=well_mixed(U, names.index(res), names.index(mut), N, W), time_s=time.time() - t)


def wilson(k, n, z=1.96):
    if n == 0: return 0.0, 1.0
    p = k / n; d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d; half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, centre - half), min(1.0, centre + half)


def main(trials=1000):
    J = []
    for c in CS:
        for kind, size in GRAPHS:
            N = size * size if kind == 'torus' else 1 << size
            for label, mut, res in PAIRS:
                if label.startswith('ladder') and N > 1024:
                    continue
                J.append((c, kind, size, label, mut, res, trials, 2000 if N >= 1024 else 500))
    for kind, size in GRAPHS:
        N = size * size if kind == 'torus' else 1 << size
        if N <= 1024:
            J.append((0.0, kind, size, 'neutral', None, None, 4 * trials, 2000 if N >= 1024 else 500))
    J.sort(key=lambda j: -(j[2] ** 2 if j[1] == 'torus' else 1 << j[2]))
    rows = []
    with Pool(9) as pool:
        for r in pool.imap_unordered(_job, J):
            rows.append(r)
            print('c=%g %s %d (N=%d) %s: rho %.4f (succ %d fail %d undec %d) well-mixed %.2e (%.0fs)' % (
                r['c'], r['graph'], r['size'], r['N'], r['pair'], r['rho'], r['succ'], r['fail'], r['undec'], r['wm'], r['time_s']), flush=True)
            json.dump(rows, open(os.path.join(ROOT, 'runs', 'graph_rates.json'), 'w'), indent=1)
    rows.sort(key=lambda r: (r['pair'], r['c'], r['graph'], r['N']))
    L = ['# Exp 2: per-mutant rates on graphs, priced modal arm n = 8, w = 0.3 (rho = P(mutant reaches half); well-mixed = Moran fixation to N/2)', '',
         '| pair | c | graph | N | rho (graph) [95% Wilson] | succ / fail / undecided (trials) | rho (well-mixed, same N) | 2/N |', '|---|---|---|---|---|---|---|---|']
    for r in rows:
        L.append('| %s | %g | %s %d | %d | %.4f [%.4f, %.4f] | %d / %d / %d (%d) | %.2e | %.2e |' % (r['pair'], r['c'], r['graph'], r['size'], r['N'], r['rho'], r['lo'], r['hi'], r['succ'], r['fail'], r['undec'], r['trials'], r['wm'], 2.0 / r['N']))
    open(os.path.join(ROOT, 'runs', 'graph_rates.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
