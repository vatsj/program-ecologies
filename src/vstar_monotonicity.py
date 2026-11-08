"""x-improvement monotonicity of the stable set in majority division (sixths grid): give (1/2, 1/2, 0) a bonus b
(in ticks) for its two members and list every stable set (exhaustive kernels). Theory tab section 1, 2026-11-08.
Result: b = 1/2 tick -> no stable set; b >= 1 -> (1/2,1/2,0) stays, partners become unequal."""
import sys, itertools, numpy as np
sys.path.insert(0, 'src')
import stable_sets as SS
g = 6
X = SS.grid(g)                       # all splits with sum <= 6 (sixths)
A = np.array(X, float); n = len(X)
idx = {tuple(x): k for k, x in enumerate(X)}
x0 = idx[(3, 3, 0)]
V0 = frozenset(idx[v] for v in [(3,3,0),(3,0,3),(0,3,3)])
COAL = [(0,1),(0,2),(1,2),(0,1,2)]
def dom(U):
    D = np.zeros((n, n), bool)
    for S in COAL:
        eff = A[:, list(S)].sum(1) <= g
        better = np.ones((n, n), bool)
        for i in S: better &= U[:, None, i] > U[None, :, i]
        D |= better & eff[:, None]
    return D
lab = lambda V: sorted(tuple(int(v) for v in X[k]) for k in V)
for b in [0, 0.5, 1, 2, 3]:
    U = A.copy(); U[x0, 0] += b; U[x0, 1] += b
    D = dom(U)
    ks, complete = SS.kernels(D)
    with_x0 = [V for V in ks if x0 in V]
    print(f"bonus {b} ticks: {len(ks)} stable sets (complete={complete}); V* stable: {SS.is_stable(D, V0)}; "
          f"containing (3,3,0): {len(with_x0)}")
    for V in ks[:6]: print("   ", lab(V))
