"""Farsighted stability with profile-level moves and projection stabilizers (RS, 2026-11-08), majority division on sixths.

Acceptable profiles: every action profile realizing an outcome in A.  A stabilizer sigma maps each profile to an
outcome in A, the identity on acceptable profiles.  Moves: a coalition S changes only its own actions (others held).
  (I) no acceptable profile a has a move a -> b by S with every member strictly preferring sigma(b) to a's outcome;
  (C) every other profile b has a move b -> c by S with sigma(c) = sigma(b) and every member strictly preferring
      sigma(b) to b's outcome, the chain ending in an acceptable profile (well-founded layering).
sigma is searched by greedy layering over every order of A's members, so "none" means none found that way.
Bonus b (ticks) on (3, 3, 0) for players 1 and 2 tests x-improvement monotonicity at the profile level."""
import itertools, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_sets as SS
import farsighted_stabilization as F

COALS = SS.COALS


def setup(bonus, g=6):
    game = SS.ext_game(g)
    X = game.R; idx = {x: k for k, x in enumerate(X)}
    nact = game.nact
    prof = list(itertools.product(*[range(k) for k in nact]))
    pidx = {a: i for i, a in enumerate(prof)}
    out = np.array([idx[game.outcome(a)] for a in prof])
    U = np.array(X, float); x0 = idx[(3, 3, 0)]
    U[x0, 0] += bonus; U[x0, 1] += bonus
    P = {S: np.all(U[:, None, list(S)] > U[None, :, list(S)], axis=2) for S in COALS}  # P[S][v, y]
    groups = {}
    for S in COALS:
        T = [p for p in range(3) if p not in S]
        gmap = {}
        for i, a in enumerate(prof):
            gmap.setdefault(tuple(a[p] for p in T), []).append(i)
        groups[S] = [np.array(v) for v in gmap.values()]
    return X, out, P, groups, x0


def consistent(A, X, out, P, groups):
    A = list(A); n = len(out)
    acc = np.isin(out, A)
    allow = np.ones((n, len(A)), bool)
    for S in COALS:
        for gi in groups[S]:
            ga = gi[acc[gi]]
            if len(ga) == 0:
                continue
            # value v forbidden on the whole group if v >_S u(a) for some acceptable a in the group
            bad = np.array([P[S][v, out[ga]].any() for v in A])
            if bad.any():
                allow[np.ix_(gi, np.nonzero(bad)[0])] = False
    Ak = {v: j for j, v in enumerate(A)}
    for i in np.nonzero(acc)[0]:
        if not allow[i, Ak[out[i]]]:
            return False
    for order in itertools.permutations(range(len(A))):
        sig = np.full(n, -1); sig[acc] = [Ak[o] for o in out[acc]]
        for j in order:
            v = A[j]; grown = True
            while grown:
                grown = False
                for S in COALS:
                    for gi in groups[S]:
                        if not (sig[gi] == j).any():
                            continue
                        cand = gi[(sig[gi] == -1) & allow[gi, j] & P[S][v, out[gi]]]
                        if len(cand):
                            sig[cand] = j; grown = True
        if (sig >= 0).all():
            return True
    return False


if __name__ == '__main__':
    for b in [0.0, 0.5, 1.0]:
        X, out, P, groups = setup(b)[:4]
        x0 = X.index((3, 3, 0))
        Xo, Eo, Uo, Po, _ = F.setup(b)
        conf = np.zeros((len(X), len(X)), bool)
        for S in COALS: conf |= Eo[S] & Po[S].T
        cands = []
        def rec(start, cur):
            cands.append(list(cur))
            if len(cur) == 4: return
            for a in range(start, len(X)):
                if a == x0 or conf[a, a] or any(conf[x, a] or conf[a, x] for x in cur): continue
                rec(a + 1, cur + [a])
        if not conf[x0, x0]: rec(0, [x0])
        ok = [A for A in cands if consistent(A, X, out, P, groups)]
        vstar = [X.index(v) for v in [(3, 3, 0), (3, 0, 3), (0, 3, 3)]]
        print(f"bonus {b}: {len(cands)} candidate sets containing (3,3,0) (|A|<=4); consistent: {len(ok)}",
              [[X[k] for k in A] for A in ok[:4]],
              "| V* consistent:" , consistent(vstar, X, out, P, groups) if b == 0 else "-", flush=True)
