"""Stable sets of the PD program game (deviation without response), provability catalogue.
notes/2026-11-23-maximal-factorizations.md, addendum of 2026-11-25."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import provability as P

def run(n):
    L = P.ModalLanguage(n, ((0, 0), (1, 0), (0, 1), (1, 1))); val, _ = P.evaluate(L)
    v = val.astype(int); K = v.shape[0]
    u = np.array([[-1, 1], [-2, 0]])
    U1 = u[v, v.T].astype(float); U2 = U1.T.copy()       # profile (i, j): U1[i,j], U2[i,j]
    out = v * 2 + v.T                                     # 3 CC, 2 CD(i C, j D), 1 DC, 0 DD
    # state: 1 in V, -1 out, 0 undecided.  x is dominated by member y if
    #  y = (i', j) with U1 greater, or (i, j') with U2 greater, or any (i', j') with both greater.
    S = np.zeros((K, K), int)
    def dom_by(mask):
        # best member payoff reachable by player 1 in column j, by player 2 in row i
        m1 = np.where(mask, U1, -9).max(axis=0)[None, :] > U1 + 1e-12
        m2 = np.where(mask, U2, -9).max(axis=1)[:, None] > U2 + 1e-12
        pts = {(a, b) for a, b in zip(U1[mask], U2[mask])}
        g = np.zeros((K, K), bool)
        for a, b in pts: g |= (a > U1 + 1e-12) & (b > U2 + 1e-12)
        return m1 | m2 | g
    full = np.ones((K, K), bool)
    rounds = 0
    while True:
        rounds += 1
        cand = S >= 0                                     # could still be in V
        newin = (S == 0) & ~dom_by(cand)                  # dominated by nothing that may be in V
        S[newin] = 1
        newout = (S == 0) & dom_by(S == 1)
        S[newout] = -1
        if not newin.any() and not newout.any(): break
    V = S == 1; und = S == 0
    core = ~dom_by(full)
    mu = np.asarray(L.mu_canon, float); mu /= mu.sum(); W = np.outer(mu, mu)
    names = {3: 'CC', 2: 'CD', 1: 'DC', 0: 'DD'}
    res = {'n': n, 'K': K, 'rounds': rounds, 'undecided': int(und.sum()),
           'core_profiles': int(core.sum()), 'V_profiles': int(V.sum()),
           'V_by_outcome': {names[o]: int((V & (out == o)).sum()) for o in names},
           'V_mass_by_outcome': {names[o]: float(W[V & (out == o)].sum()) for o in names},
           'internal_ok': bool(not (dom_by(V) & V).any()),
           'external_ok': bool((dom_by(V) | V).all()) if not und.any() else None}
    ex = np.argwhere(V & (out == 1))[:3]
    res['example_exploit_members'] = [[L.rep[i], L.rep[j]] for i, j in ex]
    return res

if __name__ == '__main__':
    r = [run(n) for n in (5, 6, 7, 8)]
    for x in r: print(json.dumps(x, ensure_ascii=False))
    json.dump(r, open('runs/stable-set-pd.json', 'w'), indent=1, ensure_ascii=False)
