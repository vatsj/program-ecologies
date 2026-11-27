"""Leader-value core from the influence function "S forces a sink of the followers' game" (finite pure games).
Checks: two players, core nonempty iff some outcome meets both leader values; three players, Scarf balancedness
implies a nonempty core.  notes/2026-11-27-forces-existence.md."""
import itertools, random, json, sys
import networkx as nx

def sinks(n, nact, u, S, aS):
    F = [i for i in range(n) if i not in S]
    profs = list(itertools.product(range(nact), repeat=len(F)))
    def full(b):
        x = [None] * n
        for i, a in zip(S, aS): x[i] = a
        for i, a in zip(F, b): x[i] = a
        return tuple(x)
    G = nx.DiGraph(); G.add_nodes_from(profs)
    for b in profs:
        ub = u[full(b)]
        for c in profs:
            if c == b: continue
            T = [k for k in range(len(F)) if b[k] != c[k]]
            uc = u[full(c)]
            if all(uc[F[k]] > ub[F[k]] for k in T): G.add_edge(b, c)
    C = nx.condensation(G)
    out = [frozenset(full(b) for b in C.nodes[k]['members']) for k in C.nodes if C.out_degree(k) == 0]
    sne = [b for b in profs if G.out_degree(b) == 0]
    return out, len(sne)

def analyse(n, nact, u):
    X = list(itertools.product(range(nact), repeat=n))
    forced = {}; no_sne = 0; commits = 0
    for r in range(1, n):
        for S in itertools.combinations(range(n), r):
            lst = []
            for aS in itertools.product(range(nact), repeat=r):
                K, ns = sinks(n, nact, u, S, aS); commits += 1; no_sne += (ns == 0)
                for B in K: lst.append(tuple(min(u[b][i] for b in B) for i in S))
            forced[S] = lst
    N = tuple(range(n))
    def dominated(x):
        if any(all(u[y][i] > u[x][i] for i in N) for y in X): return True
        return any(all(g[k] > u[x][S[k]] for k in range(len(S))) for S, L in forced.items() for g in L)
    core = [x for x in X if not dominated(x)]
    # minimal balanced collections
    if n == 2: cols = [[(0,), (1,)]]
    else: cols = [[(0,), (1,), (2,)], [(0,), (1, 2)], [(1,), (0, 2)], [(2,), (0, 1)], [(0, 1), (0, 2), (1, 2)]]
    balanced = True
    for col in cols:
        for choice in itertools.product(*[forced[S] for S in col]):
            z = [min(g[S.index(i)] for S, g in zip(col, choice) if i in S) for i in N]
            if not any(all(u[x][i] >= z[i] for i in N) for x in X): balanced = False; break
        if not balanced: break
    return len(core) > 0, balanced, no_sne, commits

if __name__ == '__main__':
    random.seed(20261127); res = {}
    for n, nact, trials in ((2, 3, 20000), (3, 2, 20000), (3, 3, 2000)):
        X = list(itertools.product(range(nact), repeat=n)); c = dict(ne=0, bal=0, bal_empty=0, ne_unbal=0, nosne=0, commits=0, games_nosne=0)
        for _ in range(trials):
            u = {x: tuple(random.random() for _ in range(n)) for x in X}
            ne, bal, ns, cm = analyse(n, nact, u)
            c['ne'] += ne; c['bal'] += bal; c['bal_empty'] += (bal and not ne); c['ne_unbal'] += (ne and not bal)
            c['nosne'] += ns; c['commits'] += cm; c['games_nosne'] += (ns > 0)
        c['trials'] = trials; res[f'n{n}_a{nact}'] = c; print(n, nact, c, flush=True)
    json.dump(res, open('runs/lvc-forces.json', 'w'), indent=1)
