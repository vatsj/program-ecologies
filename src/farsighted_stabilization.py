"""Farsighted stability through a consistent stabilization (RS, 2026-11-08), majority division on sixths.

An acceptable set A with a stabilization sigma: X -> A (sigma(a) = a on A) is consistent when
  (I) no x in A has a coalition S that can move x -> y (game effectiveness: S changes only its own actions)
      with every member strictly preferring sigma(y) to x;
  (C) every y outside A has a coalition S that can move y -> z with sigma(z) = sigma(y), every member of S strictly
      preferring sigma(y) to y, and the chain ending in A (well-founded).
Optimistic acceptable set = union of A over consistent pairs; pessimistic = intersection.  The search covers every
A of size <= KMAX that is internally consistent with sigma = id on A; sigma is found by an order-greedy layering
over A's members (all orders tried), so "not consistent" means "no sigma found by that procedure".
Bonus b (ticks) on x0 = (3, 3, 0) for players 1 and 2 tests x-improvement monotonicity."""
import itertools, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_sets as SS

COALS = SS.COALS


def setup(bonus, g=6):
    game = SS.ext_game(g)
    X = game.R
    E = SS.eff_game(game, X)
    U = np.array(X, float)
    x0 = X.index((3, 3, 0))
    U[x0, 0] += bonus; U[x0, 1] += bonus
    # P[S][v, y] = every member of S strictly prefers v to y
    P = {S: np.all(U[:, None, list(S)] > U[None, :, list(S)], axis=2) for S in COALS}
    return X, E, U, P, x0


def consistent(A, X, E, P):
    n = len(X); A = list(A); Aset = set(A)
    # Allow(y): values v in A such that no x in A, S with x ->_S y has v >_S x
    allow = []
    for y in range(n):
        ok = []
        for v in A:
            bad = any(E[S][x, y] and P[S][v, x] for x in A for S in COALS)
            if not bad:
                ok.append(v)
        allow.append(ok)
    for a in A:
        if a not in allow[a]:
            return False
    rest = [y for y in range(n) if y not in Aset]
    for order in itertools.permutations(A):
        sigma = {a: a for a in A}
        left = set(rest)
        for v in order:
            grown = True
            while grown:
                grown = False
                for y in list(left):
                    if v not in allow[y]:
                        continue
                    for S in COALS:
                        if not P[S][v, y]:
                            continue
                        if any(E[S][y, z] and sigma.get(z) == v for z in range(n) if z != y):
                            sigma[y] = v; left.discard(y); grown = True
                            break
        if not left:
            return True
    return False


def search(bonus, kmax=4):
    X, E, U, P, x0 = setup(bonus)
    n = len(X)
    # internal conflict with sigma = id: a blocks x if some S moves x -> a and prefers a
    conf = np.zeros((n, n), bool)
    for S in COALS:
        conf |= E[S] & P[S].T          # conf[x, a]: S moves x -> a, prefers a to x
    sols = []
    def rec(start, cur):
        if cur and consistent(cur, X, E, P):
            sols.append(tuple(cur))
        if len(cur) == kmax:
            return
        for a in range(start, n):
            if any(conf[x, a] or conf[a, x] for x in cur) or conf[a, a]:
                continue
            rec(a + 1, cur + [a])
    rec(0, [])
    return X, x0, sols


if __name__ == '__main__':
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    for b in [0, 0.5, 1, 2, 3]:
        X, x0, sols = search(b, kmax)
        lab = lambda A: [X[k] for k in A]
        union = sorted({X[k] for A in sols for k in A}, key=SS._okey)
        inter = sorted(set.intersection(*[{X[k] for k in A} for A in sols]), key=SS._okey) if sols else []
        print(f"bonus {b}: {len(sols)} consistent sets (|A| <= {kmax}); (3,3,0) acceptable (optimistic): "
              f"{(3,3,0) in union}; pessimistic: {(3,3,0) in inter}")
        for A in sols[:8]:
            print("   ", lab(A))
        if len(sols) > 8: print("    ...")
