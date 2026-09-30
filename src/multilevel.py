"""Island-level selection on emigration with mutation (PD by default).

    python3 src/multilevel.py --wg 0 1 3 10 --reps 5

Writes runs/multilevel_<game>.md/json.  Exits from THEM(^C) islands are split
into faker (u(q,R) > u(R,R)), shadow (on-path identical to R) and other.
"""
import argparse, json, os, sys
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from islands import run_one, _load, ROOT


def main(a):
    jobs = [(a.game, False, 'complete', a.mN, 'alld', r, a.I, a.N, a.w, a.gens, 20, a.epsN, wg) for wg in a.wg for r in range(a.reps)]
    game, U, PCC, names, sizes, mu = _load(a.game, False)
    with Pool(a.procs) as pool:
        rows = pool.map(run_one, jobs)
    iR = names.index('THEM(^%s)' % game.actions[-1]); uRR = U[iR, iR]
    def kind(q):
        if max(abs(U[q, iR] - uRR), abs(U[iR, q] - uRR), abs(U[q, q] - uRR)) < 1e-9: return 'shadow'
        return 'faker' if U[q, iR] > uRR + 1e-9 else 'other'
    for r in rows:
        t = np.array(r.pop('trace_cc')); h = len(t) // 2
        r['pcc_1st'] = float(t[:h].mean())
        ex = dict(faker=0, shadow=0, other=0)
        for x, y, n in r['trans']:
            if x == names[iR]: ex[kind(names.index(y))] += n
        r['exits'] = ex
        tot = sum(r['dom_time'].values()) or 1
        r['dom_share'] = {k: v / tot for k, v in sorted(r['dom_time'].items(), key=lambda kv: -kv[1])[:4]}
        for k in ('trace_pay', 'trace_R', 'trace_C', 'trans', 'final_classes', 'spread_pay_pairs'):
            r.pop(k, None)
    json.dump(rows, open(os.path.join(ROOT, 'runs', 'multilevel_%s.json' % a.game), 'w'), indent=1)
    L = ['# Island-level selection on emigration: %s, %d islands of %d, complete graph, mN = %g, eps N = %g per island, w = %g, start all-D, %d generations (finite eps N: approach rate, not the eps->0 object)' % (
        a.game, a.I, a.N, a.mN, a.epsN, a.w, a.gens), '',
         '| w_g | P(C,C) 2nd half mean ± sd | P(C,C) 1st half mean | payoff | exits from THEM(^C) islands: faker / shadow / other (pooled) | dominant classes, 2nd half (rep 0) |',
         '|---|---|---|---|---|---|']
    for wg in a.wg:
        s = [r for r in rows if r['wg'] == wg]
        p2 = np.array([r['pcc_2nd'] for r in s]); p1 = np.array([r['pcc_1st'] for r in s])
        ex = {k: sum(r['exits'][k] for r in s) for k in ('faker', 'shadow', 'other')}
        L.append('| %g | %.3f ± %.3f | %.3f | %.3f | %d / %d / %d | %s |' % (wg, p2.mean(), p2.std(), p1.mean(), np.mean([r['pay_2nd'] for r in s]),
                 ex['faker'], ex['shadow'], ex['other'], ', '.join('`%s` %.2f' % kv for kv in s[0]['dom_share'].items())))
    L += ['', 'Per replicate second-half P(C,C): ' + '; '.join('w_g=%g: %s' % (wg, ', '.join('%.2f' % r['pcc_2nd'] for r in rows if r['wg'] == wg)) for wg in a.wg)]
    open(os.path.join(ROOT, 'runs', 'multilevel_%s.md' % a.game), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default='pd')
    ap.add_argument('--wg', type=float, nargs='+', default=[0, 1, 3, 10])
    ap.add_argument('--reps', type=int, default=5)
    ap.add_argument('--I', type=int, default=64)
    ap.add_argument('--N', type=int, default=100)
    ap.add_argument('--mN', type=float, default=1.0)
    ap.add_argument('--epsN', type=float, default=0.1)
    ap.add_argument('--w', type=float, default=0.3)
    ap.add_argument('--gens', type=int, default=500000)
    ap.add_argument('--procs', type=int, default=9)
    main(ap.parse_args())
