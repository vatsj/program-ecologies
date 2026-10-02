"""Static map for predictions/2026-10-02-drift-closure.md: universality against drift-closure in the free
modal arm (PD, deterministic programs).

For each self-cooperating behavioural class x of L_n:
  - its component K(x) in the mutual-cooperation graph G over self-cooperating classes.  In the eps->0 chain
    with PD payoffs, the mutants that are neutral at every frequency in the x world are exactly the
    self-cooperating y with (C, C) against x, so K(x) is x's neutral closure (Proposition 1 of the brief);
  - whether x is suckerable: some class y of L_n with x(y) = C and y(x) = D (a strict invader of all-x);
  - drift distance d(x): shortest path in G from x to a suckerable class (0 if x is suckerable, inf if none);
  - universality: the mu-weighted share of FairBot's component (ALLC excluded) that x mutually cooperates with;
  - closed components: no suckerable member.

    python3 src/moat_static.py 6 8 9 10 11     (writes runs/drift_closure_static.json and .md)
"""
import json, os, sys, time
from collections import deque
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import modal as M

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FB = 'BOX(THEM(ME))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
S_PAY, R_PAY = -2.0, 0.0        # sucker payoff and mutual cooperation in modal.PD


def components(adj_rows):
    n = len(adj_rows); comp = -np.ones(n, int); out = []
    for s in range(n):
        if comp[s] >= 0: continue
        comp[s] = len(out); mem = [s]; dq = deque([s])
        while dq:
            a = dq.popleft()
            for b in adj_rows[a]:
                if comp[b] < 0:
                    comp[b] = len(out); mem.append(b); dq.append(b)
        out.append(mem)
    return comp, out


def static_map(n, prov=None):
    if prov is None:
        L, val, worlds, prov = M.build(n)
    U = prov.Ufull; P = prov.PCC; names = prov.names
    mu = np.array([c[2] for c in prov.classes])
    K = len(names)
    selfc = np.array([P[i, i] == 1 for i in range(K)])
    S = np.nonzero(selfc)[0]
    pos = {int(s): j for j, s in enumerate(S)}
    PS = P[np.ix_(S, S)] == 1
    adj = [[int(j) for j in np.nonzero(PS[i])[0] if j != i] for i in range(len(S))]
    comp, comps = components(adj)
    # suckerable: x plays C against y while y plays D against x  <=>  U[x, y] == S
    suck = np.isclose(U[S], S_PAY).any(axis=1)
    fakers = {int(S[i]): [int(y) for y in np.nonzero(np.isclose(U[S[i]], S_PAY))[0]] for i in range(len(S))}
    faker_mu = np.array([mu[fakers[int(s)]].sum() for s in S])
    # drift distance: multi-source BFS from suckerable classes
    d = np.full(len(S), np.inf); dq = deque()
    for i in np.nonzero(suck)[0]:
        d[i] = 0; dq.append(i)
    while dq:
        a = dq.popleft()
        for b in adj[a]:
            if d[b] == np.inf:
                d[b] = d[a] + 1; dq.append(b)
    iFB = names.index(FB); iC = names.index('C'); iD = names.index('D')
    cFB = comp[pos[iFB]]
    KFB = [int(S[j]) for j in comps[cFB] if S[j] != iC]
    muKFB = mu[KFB].sum()
    univ = np.array([mu[[y for y in KFB if P[s, y] == 1]].sum() / muKFB for s in S])
    enters_D = np.array([U[s, iD] == U[iD, iD] for s in S])     # x defects on D: neutral at one copy in all-D
    comp_rows = []
    for c, mem in enumerate(comps):
        cls = [int(S[j]) for j in mem]
        closed = not suck[mem].any()
        comp_rows.append(dict(id=c, size=len(cls), mu=float(mu[cls].sum()), closed=bool(closed), has_FB=bool(c == cFB),
                              has_ALLC=bool(iC in cls), n_suckerable=int(suck[mem].sum()),
                              mu_suckerable=float(mu[[S[j] for j in mem if suck[j]]].sum()),
                              n_enter_D=int(enters_D[mem].sum()), mu_enter_D=float(mu[[S[j] for j in mem if enters_D[j]]].sum()),
                              max_d=float(d[mem].max()) if not closed else float('inf'),
                              top=[(names[k], float(mu[k])) for k in sorted(cls, key=lambda k: -mu[k])[:6]]))
    comp_rows.sort(key=lambda r: -r['mu'])
    cls_rows = []
    for j, s in enumerate(S):
        s = int(s)
        cls_rows.append(dict(name=names[s], mu=float(mu[s]), comp=int(comp[j]), in_KFB=bool(comp[j] == cFB),
                             suckerable=bool(suck[j]), faker_mu=float(faker_mu[j]), n_fakers=len(fakers[s]),
                             top_fakers=[names[y] for y in sorted(fakers[s], key=lambda y: -mu[y])[:3]],
                             d=float(d[j]), universality=float(univ[j]), enters_D=bool(enters_D[j]),
                             coop_ALLC=bool(P[s, iC] == 1), coop_FB=bool(P[s, iFB] == 1)))
    cls_rows.sort(key=lambda r: -r['mu'])
    closed = [r for r in comp_rows if r['closed']]
    out = dict(n=n, classes=K, self_coop=int(len(S)), mu_self_coop=float(mu[S].sum()), n_components=len(comps),
               KFB_size=len(KFB) + 1, KFB_mu=float(muKFB), KFB_mu_with_ALLC=float(muKFB + mu[iC]),
               n_closed=len(closed), mu_closed=float(sum(r['mu'] for r in closed)),
               closed_enter_D=sum(1 for r in closed if r['n_enter_D'] > 0),
               max_univ_closed=float(max([univ[j] for j in range(len(S)) if not suck[comps[comp[j]]].any()], default=0.0)),
               components=comp_rows, classes_rows=cls_rows)
    # the trade-off, checked directly: every class with universality > 0 lies in K(FB), and K(FB) is not closed
    out['check_univ_implies_KFB'] = bool(all(r['in_KFB'] for r in cls_rows if r['universality'] > 0))
    out['check_KFB_not_closed'] = bool(any(suck[comps[cFB]]))
    # frontier: unsuckerable self-cooperators; leak = mu of suckerable mutual cooperators (one neutral step from a
    # strict exit); leak_nonD = the part not suckerable by D; tolerant = mu of mates that cooperate with ALLC
    Dsuck = {int(s): U[s, iD] == S_PAY for s in S}
    front = []
    for j, s in enumerate(S):
        if suck[j]: continue
        s = int(s)
        mates = [int(S[k]) for k in adj[j]]
        lk = [y for y in mates if suck[pos[y]]]
        front.append(dict(name=names[s], mu=float(mu[s]), universality=float(univ[j]), leak=float(mu[lk].sum()),
                          leak_nonD=float(mu[[y for y in lk if not Dsuck[y]]].sum()),
                          tolerant=float(mu[[y for y in mates if P[y, iC] == 1]].sum()),
                          coop_FB=bool(P[s, iFB] == 1), coop_ALLC=bool(P[s, iC] == 1),
                          top_leaks=[names[y] for y in sorted(lk, key=lambda y: -mu[y])[:2]]))
    front.sort(key=lambda r: r['leak'])
    out['frontier'] = front
    return out


def closure(prov, tol=1e-12):
    """Generalized closure under any payoff matrix (free arm, fringe, prices).  Edge x -> y of the
    sub-exponential transition graph H (monomorphic states, N -> infinity at fixed payoffs): in all-x, a single y
    has gap1 = u(y,x) - u(x,x) > 0, or gap1 = 0 and slope = (u(y,y) - u(y,x)) - (u(x,y) - u(x,x)) >= 0.  Every
    other single-mutant transition out of all-x has probability exp(-Theta(N)).  A self-cooperating class x is
    *closed* iff no H-path from x reaches a class that does not cooperate with itself.  Polymorphic rest points
    are not represented (an edge to y stands for 'y enters and is not exponentially suppressed')."""
    U = prov.Ufull; P = prov.PCC; names = prov.names
    mu = np.array([c[2] for c in prov.classes]); K = len(names)
    d = np.diag(U)
    gap1 = U - d[None, :]                        # gap1[y, x] = u(y, x) - u(x, x)
    slope = (d[:, None] - U) - (U.T - d[None, :])  # [y, x]: (u(y,y) - u(y,x)) - (u(x,y) - u(x,x))
    H = (gap1 > tol) | ((np.abs(gap1) <= tol) & (slope >= -tol))
    np.fill_diagonal(H, False)                    # H[y, x]: x -> y
    bad = np.array([P[i, i] != 1 for i in range(K)])
    # reverse BFS from bad classes: x reaches bad iff some y with H[y, x] reaches bad
    reach = bad.copy(); dq = deque(np.nonzero(bad)[0].tolist())
    Ht = H                                        # predecessors of y: x with H[y, x]
    while dq:
        y = dq.popleft()
        for x in np.nonzero(Ht[y] & ~reach)[0]:
            reach[x] = True; dq.append(x)
    iFB = names.index(FB)
    closed = [i for i in range(K) if not bad[i] and not reach[i]]
    rows = [dict(name=names[i], mu=float(mu[i]), coop_FB=bool(P[i, iFB] == 1), n_out=int(H[:, i].sum()),
                 out=[names[y] for y in np.nonzero(H[:, i])[0]][:4]) for i in sorted(closed, key=lambda i: -mu[i])]
    return dict(n_closed=len(closed), mu_closed=float(mu[closed].sum()),
                mu_closed_univ=float(sum(r['mu'] for r in rows if r['coop_FB'])),
                FB_closed=bool(iFB in closed), closed=rows)


def size_of(L, c, memo=None):
    """Size of the canonical function's representative if enumerated, else None."""
    return L.rep_size[c] if c < len(L.rep_size) else None


PRUDENCE = [
    # (label, size, builder(L) -> canonical id).  Orders: 0 tolerates everything that cooperates with it;
    # 1 punishes D-cooperators; 2 punishes ALLC-cooperators; 1+2 punishes both.
    ('FairBot (order 0)', 3, lambda L, o, b: b(0, 0, M.TM)),
    ('PrudentBot (order 1: defect on D-cooperators)', 8, lambda L, o, b: o('and', b(0, 0, M.TM), b(1, 1, M.TL, o('D')))),
    ('P2 = and(BOX1(TM),not(BOX(^C))) (order 2: defect on ALLC-cooperators)', 9,
     lambda L, o, b: o('and', b(0, 1, M.TM), o('not', b(0, 0, M.TL, o('C'))))),
    ('P* = and(BOX1(TM),not(BOX(TM)))', 8, lambda L, o, b: o('and', b(0, 1, M.TM), o('not', b(0, 0, M.TM)))),
    ('P12 = and(P2, BOXD1(^D)) (orders 1 and 2)', 14,
     lambda L, o, b: o('and', o('and', b(0, 1, M.TM), o('not', b(0, 0, M.TL, o('C')))), b(1, 1, M.TL, o('D')))),
    ('P*1 = and(P*, BOXD1(^D))', 13,
     lambda L, o, b: o('and', o('and', b(0, 1, M.TM), o('not', b(0, 0, M.TM))), b(1, 1, M.TL, o('D')))),
    ('PB_BTT = and(PB, not(BOX(^BOX(TT)))) (order 1 plus: defect on cooperators of the self-prover)', 15,
     lambda L, o, b: o('and', o('and', b(0, 0, M.TM), b(1, 1, M.TL, o('D'))), o('not', b(0, 0, M.TL, b(0, 0, M.TT))))),
]
PRUDENCE2 = [   # needs lmax = 2: the D-check one level up
    ('PB2 = and(BOX(TM), BOXD2(^D))', 8, lambda L, o, b: o('and', b(0, 0, M.TM), b(1, 2, M.TL, o('D')))),
    ('P12b = and(P2, BOXD2(^D)) (orders 1 and 2, PA+2)', 14,
     lambda L, o, b: o('and', o('and', b(0, 1, M.TM), o('not', b(0, 0, M.TL, o('C')))), b(1, 2, M.TL, o('D')))),
    ('P*1b = and(P*, BOXD2(^D)) (PA+2)', 13,
     lambda L, o, b: o('and', o('and', b(0, 1, M.TM), o('not', b(0, 0, M.TM))), b(1, 2, M.TL, o('D')))),
    ('PB_BTTb = and(PB, not(BOX1(^BOX(TT)))) (PA+2 not needed?)', 15,
     lambda L, o, b: o('and', o('and', b(0, 0, M.TM), b(1, 1, M.TL, o('D'))), o('not', b(0, 1, M.TL, b(0, 0, M.TT))))),
    ('P2D2 = and(BOX2(TM), not(BOX1(^C)), BOXD2(^D))', 14,
     lambda L, o, b: o('and', o('and', b(0, 2, M.TM), o('not', b(0, 1, M.TL, o('C')))), b(1, 2, M.TL, o('D')))),
]


def candidates(n, cands=PRUDENCE, lmax=1):
    """Static properties of candidate programs (possibly longer than n) against L_n: they are added to the
    evaluator with prior mass 0, so they act as probes of L_n, not as members of it.  lmax > 1 uses the
    grammar with boxes up to PA + Con^lmax (src/modal_lv.py)."""
    import modal_lv as LV
    kinds = tuple((k, l) for l in range(lmax + 1) for k in (M.KC, M.KD))
    L = LV.ModalLanguageLv(n, kinds)
    o = L.op; b = lambda k, l, f, a=None: o((k, l, f), a)
    ids = [(lab, sz, f(L, o, b)) for lab, sz, f in cands]
    val, worlds = LV._evaluate_lv(*L.arrays(), lmax + 1, 300)
    U, PCC = M.pd_payoffs(val, M.PD)
    K0 = len(L.mu_canon); K = len(L.funcs)
    mu = np.zeros(K); mu[:K0] = L.mu_canon / L.mu_canon.sum()
    enumerated = np.zeros(K, bool); enumerated[:K0] = L.count_canon > 0
    E = np.nonzero(enumerated)[0]
    selfc = np.array([PCC[i, i] == 1 for i in range(K)])
    suck = np.array([(np.isclose(U[i, E], S_PAY)).any() for i in range(K)])
    iC, iD = L.op('C'), L.op('D'); iFB = L.op((0, 0, M.TM))
    SE = [i for i in E if selfc[i]]
    KFB = [j for j in SE if j != iC]
    rows = []
    for lab, sz, c in ids:
        if not selfc[c]:
            rows.append(dict(label=lab, size=sz, self_coop=False)); continue
        mates = [j for j in SE if j != c and PCC[c, j] == 1]
        leak = [j for j in mates if suck[j]]
        allc_mates = [j for j in mates if PCC[j, iC] == 1]
        rows.append(dict(label=lab, size=sz, self_coop=True, suckerable=bool(suck[c]),
                         fakers=[L.rep[j] for j in E if U[c, j] == S_PAY][:3],
                         universality=float(mu[[j for j in KFB if PCC[c, j] == 1]].sum() / mu[KFB].sum()),
                         leak=float(mu[leak].sum()), allc_tolerant_mates=float(mu[allc_mates].sum()),
                         coop_FB=bool(PCC[c, iFB] == 1), coop_ALLC=bool(PCC[c, iC] == 1), coop_D=bool(val[c, iD] == 1),
                         top_leaks=[L.rep[j] for j in sorted(leak, key=lambda j: -mu[j])[:3]],
                         coop_with=[lab2 for lab2, _, c2 in ids if c2 != c and PCC[c, c2] == 1]))
    return rows


def fmt(o):
    L = ['## n = %d' % o['n'], '',
         '- behavioural classes %d; self-cooperating %d (μ %.4f); components of G %d' % (o['classes'], o['self_coop'], o['mu_self_coop'], o['n_components']),
         '- FairBot component: %d classes, μ %.4f without ALLC (%.4f with)' % (o['KFB_size'], o['KFB_mu'], o['KFB_mu_with_ALLC']),
         '- closed components: %d, μ %.3g; closed components with a member that enters all-D neutrally: %d; max universality over closed classes %.3g' % (
             o['n_closed'], o['mu_closed'], o['closed_enter_D'], o['max_univ_closed']),
         '- checks: universality > 0 ⇒ in K(FB): %s; K(FB) has a suckerable member: %s' % (o['check_univ_implies_KFB'], o['check_KFB_not_closed']), '',
         '| component | size | μ | closed | has FB | has ALLC | suckerable members (μ) | enter all-D (μ) | max d | top members |', '|---|---|---|---|---|---|---|---|---|---|']
    for r in o['components'][:15]:
        L.append('| %d | %d | %.3g | %s | %s | %s | %d (%.3g) | %d (%.3g) | %s | %s |' % (
            r['id'], r['size'], r['mu'], r['closed'], r['has_FB'], r['has_ALLC'], r['n_suckerable'], r['mu_suckerable'],
            r['n_enter_D'], r['mu_enter_D'], r['max_d'], '; '.join('`%s` %.2g' % t for t in r['top'][:3])))
    L += ['', '| class (top 25 by μ among self-cooperators) | μ | in K(FB) | suckerable | faker μ | d | universality | enters D | top fakers |', '|---|---|---|---|---|---|---|---|---|']
    for r in o['classes_rows'][:25]:
        L.append('| `%s` | %.3g | %s | %s | %.2g | %s | %.3f | %s | %s |' % (
            r['name'], r['mu'], r['in_KFB'], r['suckerable'], r['faker_mu'], r['d'], r['universality'], r['enters_D'],
            ', '.join('`%s`' % f for f in r['top_fakers'][:2])))
    return '\n'.join(L) + '\n'


def fmt_frontier(o):
    L = ['', '**Frontier (n = %d): unsuckerable self-cooperating classes, by leak**' % o['n'], '',
         '| class | μ | universality | leak | leak not via D | ALLC-tolerant mates | coop FB | coop ALLC | top leaks |', '|---|---|---|---|---|---|---|---|---|']
    for r in o['frontier'][:16]:
        L.append('| `%s` | %.2e | %.3f | %.2e | %.2e | %.2e | %s | %s | %s |' % (r['name'], r['mu'], r['universality'], r['leak'], r['leak_nonD'],
                 r['tolerant'], r['coop_FB'], r['coop_ALLC'], ', '.join('`%s`' % t for t in r['top_leaks'])))
    return '\n'.join(L) + '\n'


def fmt_cands(n, lmax, rows):
    L = ['', '**Prudence ladder against L_%d (boxes up to PA + Con^%d; candidates at prior mass 0)**' % (n, lmax), '',
         '| candidate | size | self-cooperates | suckerable | universality | leak | ALLC-tolerant mates | coop FB | top leaks |', '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        if not r['self_coop']:
            L.append('| %s | %d | no | | | | | | |' % (r['label'], r['size'])); continue
        L.append('| %s | %d | yes | %s | %.3f | %.2e | %.2e | %s | %s |' % (r['label'], r['size'], r['suckerable'], r['universality'], r['leak'],
                 r['allc_tolerant_mates'], r['coop_FB'], ', '.join('`%s`' % t for t in r['top_leaks'][:2])))
    return '\n'.join(L) + '\n'


def main():
    ns = [int(a) for a in sys.argv[1:]] or [6, 8, 9, 10, 11]
    res = []; md = ['# Drift-closure static map (free modal arm, PD)', '',
                    'Written by src/moat_static.py for predictions/2026-10-02-drift-closure.md. Leak masses are prior masses of classes '
                    '(normalized over L_n); a world\'s neutral exit rate to them is leak / N per mutation event.', '']
    for n in ns:
        t = time.time(); o = static_map(n)
        L, val, worlds, prov = M.build(n)
        o['closure_free'] = closure(prov)
        o['time_s'] = time.time() - t; res.append(o)
        md.append(fmt(o)); md.append(fmt_frontier(o))
        print('n=%d done (%.0fs)' % (n, o['time_s']), flush=True)
    cands = {}
    for n, lmax in ((9, 1), (10, 1), (8, 2), (9, 2)):
        rows = candidates(n, PRUDENCE + (PRUDENCE2 if lmax > 1 else []), lmax)
        cands['%d/%d' % (n, lmax)] = rows; md.append(fmt_cands(n, lmax, rows))
    json.dump(dict(maps=res, candidates=cands), open(os.path.join(ROOT, 'runs', 'drift_closure_static.json'), 'w'), indent=1, default=str)
    open(os.path.join(ROOT, 'runs', 'drift_closure_static.md'), 'w').write('\n'.join(md))


if __name__ == '__main__':
    main()
