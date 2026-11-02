"""Static numbers of the pair-worth games (spec design 1; notes/pair-worth.md).  Run: python3 src/pair_worth_static.py

For each game and grid: outcome set, core proper, strict / weak undominated sets and the decomposition (core proper, ring
= undominated efficient outside the core, undominated wasteful), stable sets (kernels of the dominance digraph, MILP)
under strict and weak dominance, and the length-prior mass of the named families under R's grammar."""
import json, os, sys, math, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix, vstack

OUTP = os.path.join(PW.ROOT, 'runs', 'pair_worth')


def dom_matrix(G, R, weak):
    A = np.array(R, np.int64); n = len(R)
    M = np.zeros((n, n), bool)
    for S, cap in G.coalitions():
        S = list(S)
        eff = A[:, S].sum(1) <= cap
        if weak:
            ge = np.ones((n, n), bool); gt = np.zeros((n, n), bool)
            for i in S:
                ge &= A[:, None, i] >= A[None, :, i]; gt |= A[:, None, i] > A[None, :, i]
            M |= ge & gt & eff[:, None]
        else:
            b = np.ones((n, n), bool)
            for i in S:
                b &= A[:, None, i] > A[None, :, i]
            M |= b & eff[:, None]
    return M


def kernels(M, maxn=6, timeout=60):
    """stable sets (kernels) of the digraph M[x, y] = x dominates y via MILP; up to maxn."""
    n = M.shape[0]
    xi, yj = np.nonzero(M)
    na = len(xi)
    rows = []
    # independence: x_i + x_j <= 1 for every arc
    A1 = lil_matrix((na, n))
    for k in range(na):
        A1[k, xi[k]] = 1; A1[k, yj[k]] = 1
    # external stability: x_j + sum_{i dom j} x_i >= 1
    A2 = lil_matrix((n, n))
    for j in range(n):
        A2[j, j] = 1
    for k in range(na):
        A2[yj[k], xi[k]] = 1
    cons = [LinearConstraint(csr_matrix(A1), -np.inf, 1), LinearConstraint(csr_matrix(A2), 1, np.inf)]
    found = []
    for _ in range(maxn):
        r = milp(np.zeros(n), constraints=cons, integrality=np.ones(n), bounds=Bounds(0, 1),
                 options=dict(time_limit=timeout))
        if r.status != 0:
            break
        S = [i for i in range(n) if r.x[i] > 0.5]
        found.append(S)
        cut = np.where(np.isin(np.arange(n), S), 1.0, -1.0)
        cons.append(LinearConstraint(csr_matrix(cut[None, :]), -np.inf, len(S) - 1))
    return found


def decomp(G, R, idx, und_set):
    """decomposition of a set of vector indices: core proper / ring / undominated-wasteful / other."""
    out = dict(core=0, ring=0, eff_other=0, wasteful=0, null=0)
    cl, und = G.classify_vectors()
    for i in idx:
        y = R[i]
        c = cl[y]
        if c == 0: out['null'] += 1
        elif c == 1: out['core'] += 1
        elif c == 2: out['ring'] += 1
        elif c == 3: out['eff_other'] += 1
        else: out['wasteful'] += 1
    return out


def static_game(name, stable=True):
    G = PW.get_game(name)
    R = G.vectors()
    n = len(R)
    res = dict(game=name, Gd=G.Gd, nact=G.nact, n_outcomes_ids=G.nout, n_vectors=n)
    core = [i for i, y in enumerate(R) if G.in_core(y)]
    res['core_proper'] = len(core)
    res['core_points'] = [list(R[i]) for i in core]
    res['n_efficient'] = sum(1 for y in R if sum(y) == G.Gd)
    for rel in ('strict', 'weak'):
        M = dom_matrix(G, R, rel == 'weak')
        und = [i for i in range(n) if not M[:, i].any()]
        d = decomp(G, R, und, None)
        ext = bool(all(M[und][:, j].any() for j in range(n) if j not in set(und)))
        res[rel] = dict(undominated=len(und), decomposition=d, und_equals_core=(set(und) == set(core)),
                        und_externally_stable=ext,
                        und_points=[list(R[i]) for i in und][:80])
        if stable and n <= 500:
            t0 = time.time()
            ks = kernels(M, maxn=6)
            res[rel]['stable_sets_found'] = len(ks)
            res[rel]['stable_sets_capped_at_6'] = len(ks) == 6
            res[rel]['stable_sets'] = [dict(size=len(S), decomposition=decomp(G, R, S, None),
                                            points=[list(R[i]) for i in S][:40]) for S in ks[:3]]
            res[rel]['stable_wall'] = round(time.time() - t0, 1)
    return res


# ---------------------------------------------------------------- length-prior mass under R's grammar
def prior_mass(G, kind, nsig, menu_label):
    """mass of one spelling of the family member under R's length prior (level-0 atoms: 2 * nact atoms), unnormalised
    (sum over sizes 1/(2 s^2) normalised by the sizes present at n <= 6), relative to a single constant."""
    import dollar3 as D
    n_atoms = 2 * G.nact
    lines = {'B0': 3, 'K0': 5, 'A0': None}[kind] if kind != 'A0' else None
    # sizes: decision list of ell lines with two-atom first grand line
    def size(lines2, lines1):
        s = 1                               # default constant
        s += lines2 * (1 + 7 + 1)           # if(and(b,b), x, rest): 1 + 7 + 1
        s += lines1 * (1 + 3 + 1)
        return s
    if kind == 'B0':
        sz = size(1, 2)
    elif kind == 'K0':
        sz = size(1, 4)
    elif kind == 'A0':
        w = G.v[0][1]
        sz = size(1, 2 * (w + 1))
    else:
        raise ValueError(kind)
    aS = D.raw_counts(sz, n_atoms)[sz]
    logmass = -(math.log2(aS) + 2 * math.log2(sz) + 1)
    norm_n6 = 0.5 + 1 / (2 * 36.0)
    return dict(kind=kind, size=sz, a_size=float(aS), log10_one_spelling=logmass * math.log10(2),
                log10_rel_to_total_n6=(logmass - math.log2(norm_n6)) * math.log10(2))


def main():
    os.makedirs(OUTP, exist_ok=True)
    out = {}
    for name in ('pw13', 'pw23', 'gl6', 'pw56', 'pw23t', 'gl24'):
        t0 = time.time()
        r = static_game(name, stable=name not in ('pw23t', 'gl24'))
        out[name] = r
        print(name, 'vectors', r['n_vectors'], 'core', r['core_proper'], 'strict und', r['strict']['undominated'],
              r['strict']['decomposition'], 'weak und', r['weak']['undominated'], r['weak']['decomposition'],
              'wall %.0fs' % (time.time() - t0), flush=True)
        for rel in ('strict', 'weak'):
            if 'stable_sets_found' in r[rel]:
                print('   ', rel, 'stable sets', r[rel]['stable_sets_found'], 'capped' if r[rel]['stable_sets_capped_at_6'] else '',
                      [(s['size'], s['decomposition']) for s in r[rel]['stable_sets']], flush=True)
    masses = {}
    for name in ('pw13', 'pw56'):
        G = PW.get_game(name)
        masses[name] = {k: prior_mass(G, k, 0, '') for k in ('B0', 'K0', 'A0')}
        print(name, 'prior mass (log10 of one spelling):', {k: (v['size'], round(v['log10_one_spelling'], 1)) for k, v in masses[name].items()})
    out['prior_mass_R'] = masses
    out['prior_mass_note'] = ('level-1 atoms (B, K, A as run) are outside R\'s modalPA grammar (mass 0 under R); '
                              'B0/K0/A0 are the level-0 spellings; sizes in DSL nodes')
    with open(os.path.join(OUTP, 'static.json'), 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
