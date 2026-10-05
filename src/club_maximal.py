"""Maximal fixed points of the joint operator F at n = 6..9 (specs/2026-10-04-club.md, measure (i)-(iii)).

F is deflationary (F(K) is a subset of K, predictions S1) but not monotone (runs/club_lattice.json), so the limit
from the full set need not be the greatest fixed point: a program can be removed at step 1 because a non-member
(D, say) is still in K, and never return.  Here: starts from the full set, from the set G of guarded programs
(canonical function implies CLUB(THEM)), and from K* | G; then greedy ascent: for a fixed point S and every
program y outside S, iterate F from S | {y}; a result that strictly contains S replaces S.  Results that are not
comparable with S are recorded (evidence of several maximal fixed points).

    python3 src/club_maximal.py       # writes runs/club_maximal.json
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import club as CL
import club_static as CS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fp_from(c, m):
    traj, cyc = c.iterate(m)
    assert cyc == len(traj) - 1, 'no fixed point reached'
    return traj[-1]


def ascend(c, S, max_rounds=20):
    incomparable = {}
    for rnd in range(max_rounds):
        grew = False
        for y in np.nonzero(c.in_univ)[0]:
            if y in S: continue
            T = fp_from(c, c.mask(set(S) | {int(y)}))
            if T > S:
                S = T; grew = True
            elif not (T <= S):
                incomparable[T] = int(y)
        if not grew:
            break
    return S, incomparable


def main():
    out = []
    for mode in ('full', 'pos'):
        for n in (6, 7, 8, 9):
            t = time.time()
            c = CL.Club(n, mode=mode)
            G = np.array([c.in_univ[x] and CS.guarded(c, x) for x in range(c.K)])
            Kfull = fp_from(c, c.in_univ.copy())
            KG = fp_from(c, G)
            KGu = fp_from(c, G | c.mask(Kfull))
            best = max([Kfull, KG, KGu], key=len)
            Smax, inc = ascend(c, best)
            # is every incomparable fixed point below some other found one, or a genuinely different maximal one?
            inc_max = []
            for T, y in inc.items():
                Tm, _ = ascend(c, T, max_rounds=5)
                if not (Tm <= Smax):
                    inc_max.append((sorted(c.names[x] for x in Tm - Smax), sorted(c.names[x] for x in Smax - Tm), c.names[y]))
            uF, _ = c.F(c.mask(Smax))
            r = dict(mode=mode, n=n, guarded=int(G.sum()), K_full=len(Kfull), K_G=len(KG), K_Gu=len(KGu), K_max=len(Smax),
                     max_is_fixed=bool((uF == c.mask(Smax)).all()),
                     Kfull_subset_of_max=bool(Kfull <= Smax), KG_eq_max=bool(KG == Smax),
                     missed_by_full=sorted(c.names[x] for x in Smax - Kfull),
                     guarded_not_in_max=sorted(c.names[x] for x in np.nonzero(G)[0] if x not in Smax)[:30],
                     n_guarded_not_in_max=int(sum(1 for x in np.nonzero(G)[0] if x not in Smax)),
                     unguarded_in_max=sorted(c.names[x] for x in Smax if not G[x]),
                     n_incomparable=len(inc), other_maximal=inc_max[:10], n_other_maximal=len(inc_max),
                     K_max_members=sorted(c.names[x] for x in Smax), evals=c.n_evals, time_s=time.time() - t)
            out.append(r)
            print('%s n=%d: guarded %d; K(full) %d, K(G) %d, K(G|K*) %d -> ascended max %d (fixed %s); K(full) below max %s; missed by full start %d; guarded not in max %d; unguarded in max %d; incomparable %d, other maximal %d (%.0fs)' % (
                mode, n, G.sum(), len(Kfull), len(KG), len(KGu), len(Smax), r['max_is_fixed'], r['Kfull_subset_of_max'], len(r['missed_by_full']),
                r['n_guarded_not_in_max'], len(r['unguarded_in_max']), len(inc), len(inc_max), time.time() - t), flush=True)
            json.dump(out, open(os.path.join(ROOT, 'runs', 'club_maximal.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
