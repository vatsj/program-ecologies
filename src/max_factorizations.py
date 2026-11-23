"""Maximal symmetric factorizations of the PD in the provability arm (notes/2026-11-23-maximal-factorizations.md)."""
import sys, os, json
import numpy as np, networkx as nx
sys.path.insert(0, os.path.dirname(__file__))
import provability as P
from case3_static import GAMES

def run(n, kinds):
    L = P.ModalLanguage(n, kinds); val, _ = P.evaluate(L)
    v = val.astype(int); K = v.shape[0]
    mu = np.asarray(L.mu_canon, float); mu /= mu.sum()
    g = GAMES['PD']; u = np.zeros((2, 2))
    for (x, y), (p, q) in g.items(): u[x, y] = p
    U = u[v, v.T]                              # U[i, j]: i's payoff against j
    best = U.max(axis=0)                       # best any program earns against resident j
    nash = (U >= best[None, :] - 1e-12)        # i is a best reply to j
    cell = nash & nash.T                       # Nash both ways
    eff = (v == 1) & (v.T == 1)                # CC is the only efficient outcome not blocked by the pair
    ok = cell & eff
    nodes = [i for i in range(K) if ok[i, i]]
    G = nx.Graph(); G.add_nodes_from(nodes)
    for a in nodes:
        for b in nodes:
            if a < b and ok[a, b]: G.add_edge(a, b)
    cl = sorted(nx.find_cliques(G), key=lambda c: -mu[c].sum())
    nashonly = [i for i in range(K) if cell[i, i] and not ok[i, i]]
    tot = mu[sorted(set().union(*cl))].sum() if cl else 0
    name = lambda i: L.rep[i]
    out = {'n': n, 'K': K, 'members_any': len(nodes), 'mass_any': float(tot), 'n_maximal': len(cl),
           'top': [{'size': len(c), 'mass': float(mu[c].sum()),
                    'members': [name(i) for i in sorted(c, key=lambda i: -mu[i])[:8]]} for c in cl[:6]],
           'sizes': [len(c) for c in cl[:30]],
           'unexploited_CC_self': len(nodes)}
    if len(cl) > 1:
        core = set(cl[0]).intersection(*map(set, cl))
        out['in_all'] = [name(i) for i in sorted(core, key=lambda i: -mu[i])[:8]]
        out['pair_disjoint_from_top'] = sum(1 for c in cl[1:] if not set(c) & set(cl[0]))
        out['only_outside_top'] = [[name(i) for i in sorted(set(c) - set(cl[0]), key=lambda i: -mu[i])[:5]] for c in cl[1:5]]
    return out

if __name__ == '__main__':
    import case3_static as C
    import inspect
    src = inspect.getsource(C)
    res = []
    for n in (5, 6, 7, 8, 9):
        res.append(run(n, ((0, 0), (1, 0), (0, 1), (1, 1))))
        print(json.dumps(res[-1], indent=1, ensure_ascii=False))
    json.dump(res, open('runs/max-factorizations.json', 'w'), indent=1, ensure_ascii=False)
