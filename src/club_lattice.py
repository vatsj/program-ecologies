"""Exhaustive check of the fixed points of F below K* (specs/2026-10-04-club.md, measure (i), extended):
is every subset of K* a fixed point?  Also empirical monotonicity of F at n = 8 (extra diagnostic).

    python3 src/club_lattice.py        # writes runs/club_lattice.json
"""
import json, os, sys, time
from itertools import combinations
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import club_static as CS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    out = []
    for mode in ('full', 'pos'):
        for n in (6, 7, 8):
            t = time.time()
            c, K, steps = CS.solve_kstar(n, mode=mode)
            ks = [int(x) for x in np.nonzero(K)[0]]
            fixed = 0; notfixed = []
            for r in range(len(ks) + 1):
                for S in combinations(ks, r):
                    m = c.mask(S); F, _ = c.F(m)
                    if (F == m).all(): fixed += 1
                    else: notfixed.append(([c.names[x] for x in S], [c.names[x] for x in np.nonzero(m & ~F)[0]]))
            rng = np.random.default_rng(CS.SEED + 100 + n)
            viol = 0; pairs = 200; U = c.in_univ
            for i in range(pairs):
                A = U & (rng.random(c.K) < rng.random()); B = A | (U & (rng.random(c.K) < rng.random()))
                FA, _ = c.F(A); FB_, _ = c.F(B)
                if (FA & ~FB_).any(): viol += 1
            r = dict(mode=mode, n=n, kstar=len(ks), subsets=2 ** len(ks), fixed=fixed, not_fixed=notfixed[:10],
                     mono_pairs=pairs, mono_violations=viol, time_s=time.time() - t)
            out.append(r)
            print('%s n=%d: |K*| %d, %d of %d subsets are fixed points; monotonicity violations %d/%d (%.0fs)' % (
                mode, n, len(ks), fixed, 2 ** len(ks), viol, pairs, time.time() - t), flush=True)
            for nf in notfixed[:5]: print('   not fixed:', nf)
    json.dump(out, open(os.path.join(ROOT, 'runs', 'club_lattice.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
