"""Static part of specs/2026-10-04-club.md, in the order the spec fixes:
  1. fixed-point enumeration of the joint operator F at n = 6, 7 (full set, empty set, 20 random sets), the union
     check, empirical monotonicity, and the 'pos' control;
  2. the sanity check: K empty in the base language at n <= 9;
  3. composition of K at n = 6..9 (programs, canons, behavioural classes, mu, members, within-K graph), collateral,
     the drift-closure check (neutral entrants into all-club-FairBot, suckerable members), cutoff dependence.

    python3 src/club_static.py            # writes runs/club_static.json
"""
import json, os, sys, time
from collections import deque
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import club as CL
from club import KCLUB

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FB = 'BOX(THEM(ME))'
CFB = 'and(BOX(THEM(ME)),CLUB(THEM))'
CT = 'CLUB(THEM)'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
PSTAR = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'
S_PAY = -2.0
SEED = 20261004


# ------------------------------------------------------------------ 1. fixed points
def enumerate_fixed_points(n, mode='full', n_random=20, rng=None):
    rng = rng or np.random.default_rng(SEED + n)
    c = CL.Club(n, mode=mode)
    U = c.in_univ
    starts = [('full set', U.copy()), ('empty set', np.zeros(c.K, bool))]
    for i in range(n_random):
        starts.append(('random %d' % (i + 1), U & (rng.random(c.K) < 0.5)))
    # extra (labelled): random subsets of the limit from the full set, to probe the lattice below it
    res = []; fps = {}
    for lab, K0 in starts:
        traj, cyc = c.iterate(K0)
        last = traj[-1]
        is_fp = cyc is not None and cyc == len(traj) - 1
        res.append(dict(start=lab, size0=int(K0.sum()), steps=len(traj) - 1, cycle=bool(cyc is not None and cyc < len(traj) - 1),
                        fixed=is_fp, size=len(last)))
        if is_fp:
            fps.setdefault(last, []).append(lab)
    Kstar = res[0]
    kstar = [k for k, labs in fps.items() if 'full set' in labs][0]
    extra = []
    for i in range(20):
        sub = c.mask([x for x in kstar if rng.random() < 0.5])
        traj, cyc = c.iterate(sub)
        last = traj[-1]
        extra.append(len(last))
        fps.setdefault(last, []).append('sub-K* %d' % (i + 1))
    fp_list = sorted(fps.items(), key=lambda kv: -len(kv[0]))
    # maximality and union
    union = frozenset().union(*[k for k, _ in fp_list])
    uF, _ = c.F(c.mask(union))
    union_fixed = frozenset(np.nonzero(uF)[0].tolist()) == union
    all_below = all(k <= kstar for k, _ in fp_list)
    maximal = [k for k, _ in fp_list if not any(k < k2 for k2, _ in fp_list)]
    # monotonicity on random nested pairs
    mono_viol = 0; pairs = 50
    for i in range(pairs):
        A = U & (rng.random(c.K) < rng.random())
        B = A | (U & (rng.random(c.K) < rng.random()))
        FA, _ = c.F(A); FB_, _ = c.F(B)
        if (FA & ~FB_).any(): mono_viol += 1
    # also nested pairs inside K* (where the club lives)
    mono_viol_in = 0
    for i in range(pairs):
        A = c.mask([x for x in kstar if rng.random() < 0.5])
        B = A | c.mask([x for x in kstar if rng.random() < 0.5])
        FA, _ = c.F(A); FB_, _ = c.F(B)
        if (FA & ~FB_).any(): mono_viol_in += 1
    return dict(n=n, mode=mode, universe=int(U.sum()), starts=res,
                n_fixed_points=len(fp_list),
                fixed_points=[dict(size=len(k), reached_from=labs[:6], n_starts=len(labs),
                                   members=sorted(c.names[x] for x in k)[:12] if len(k) <= 12 else None) for k, labs in fp_list],
                kstar_size=len(kstar), kstar=sorted(c.names[x] for x in kstar),
                any_cycle=any(r['cycle'] for r in res), union_size=len(union), union_is_fixed=bool(union_fixed),
                all_fixed_points_below_kstar=bool(all_below), n_maximal=len(maximal),
                monotonicity_violations=mono_viol, monotonicity_pairs=pairs,
                monotonicity_violations_inside_kstar=mono_viol_in, sub_kstar_sizes=extra, evals=c.n_evals)


# ------------------------------------------------------------------ helpers on a solved K
def solve_kstar(n, mode='full', club=True):
    c = CL.Club(n, club=club, mode=mode)
    traj, cyc = c.iterate(c.in_univ.copy())
    K = c.mask(traj[-1])
    F, val = c.F(K)
    assert (F == K).all()
    return c, K, len(traj) - 1


def guarded(c, x):
    """x's canonical function implies CLUB(THEM) (CLUB is a top-level conjunct guard)."""
    atoms, tt, k = c.L.funcs[x]
    j = [i for i, a in enumerate(atoms) if c.L.atoms[a][0] == KCLUB]
    if not j: return False
    j = j[0]
    return all(not ((tt >> i) & 1) or ((i >> j) & 1) for i in range(1 << k))


def components(nodes, adj):
    comp = {}; out = []
    for s in nodes:
        if s in comp: continue
        comp[s] = len(out); mem = [s]; dq = deque([s])
        while dq:
            a = dq.popleft()
            for b in adj[a]:
                if b not in comp:
                    comp[b] = len(out); mem.append(b); dq.append(b)
        out.append(mem)
    return out


def composition(c, K):
    prov, val = c.provider(K)
    names = prov.names; U = prov.Ufull; P = prov.PCC
    mu = np.array([cl[2] for cl in prov.classes]); nC = len(names)
    inK = prov.inK
    assert (prov.inK == prov.inK_any).all(), 'a behavioural class mixes members and non-members'
    selfc = np.array([P[i, i] == 1 for i in range(nC)])
    S = np.nonzero(selfc)[0]
    Kc = [int(i) for i in np.nonzero(inK)[0]]
    suck = {int(i): bool(np.isclose(U[i], S_PAY).any()) for i in S}
    suckers = {int(i): [names[y] for y in np.nonzero(np.isclose(U[i], S_PAY))[0]][:3] for i in S}
    get = lambda s: names.index(s) if s in names else None
    iFB, iC, iD, iCFB, iCT, iPB, iPS = (get(s) for s in (FB, 'C', 'D', CFB, CT, PB, PSTAR))
    # within-K mutual-cooperation graph over behavioural classes
    adj = {a: [b for b in Kc if b != a and P[a, b] == 1] for a in Kc}
    comps = components(Kc, adj)
    comps.sort(key=lambda m: -mu[m].sum())
    # mutual-cooperation graph over all self-cooperators, FairBot's component (ALLC excluded from the weights)
    adjS = {int(a): [int(b) for b in S if b != a and P[a, b] == 1] for a in S}
    compsS = components([int(s) for s in S], adjS)
    cFBcomp = [m for m in compsS if iFB in m][0]
    KFB = [y for y in cFBcomp if y != iC]
    muKFB = mu[KFB].sum()
    univ = {a: float(mu[[y for y in KFB if P[a, y] == 1]].sum() / muKFB) for a in Kc}
    # drift-closure checks
    neutral_into_cfb = []
    if iCFB is not None:
        a = iCFB; uaa = U[a, a]
        for y in range(nC):
            if y != a and max(abs(U[y, a] - uaa), abs(U[a, y] - uaa), abs(U[y, y] - uaa)) < 1e-12:
                neutral_into_cfb.append(names[y])
    neutral_outside = [s for s in neutral_into_cfb if not inK[names.index(s)]]
    out_unsuck = [int(i) for i in S if not inK[i] and not suck[int(i)]]
    out_suck = [int(i) for i in S if not inK[i] and suck[int(i)]]
    canon_members = [x for x in np.nonzero(K)[0]]
    progs = float(sum(c.L.count_canon[x] for x in canon_members))
    rows = []
    for i in sorted(Kc, key=lambda i: -mu[i]):
        cm = prov.canon_members[i]
        rows.append(dict(name=names[i], mu=float(mu[i]), canons=len(cm), programs=float(prov.sizes[i]),
                         guarded=all(guarded(c, x) for x in cm), any_guarded=any(guarded(c, x) for x in cm),
                         suckerable=suck[i], suckered_by=suckers[i], coop_D=bool(P[i, iD] == 1),
                         coops_with_CT=bool(iCT is not None and P[i, iCT] == 1), mutual_CT=bool(iCT is not None and P[i, iCT] == 1 and P[iCT, i] == 1),
                         n_mates=len(adj[i]), universality=univ[i]))
    pstar_block = [int(q) for q in S if iPS is not None and P[q, iPS] == 1 and P[q, iFB] != 1]
    return dict(prov=prov, val=val, out=dict(
        classes=nC, self_coop=int(len(S)), mu_self_coop=float(mu[S].sum()),
        K_canons=len(canon_members), K_programs=progs, K_classes=len(Kc), K_mu=float(mu[Kc].sum()),
        K_share_selfcoop=len(Kc) / max(len(S), 1), K_mu_share_selfcoop=float(mu[Kc].sum() / mu[S].sum()),
        members=rows,
        within_K_components=[dict(size=len(m), mu=float(mu[m].sum()), members=[names[q] for q in sorted(m, key=lambda q: -mu[q])][:8],
                                  clique=bool(all(P[a, b] == 1 for a in m for b in m))) for m in comps],
        within_K_n_components=len(comps), within_K_all_singletons=bool(all(len(m) == 1 for m in comps)),
        within_K_largest=len(comps[0]) if comps else 0,
        n_suckerable_members=sum(1 for i in Kc if suck[i]), mu_suckerable_members=float(sum(mu[i] for i in Kc if suck[i])),
        n_unguarded_members=sum(1 for r in rows if not r['any_guarded']),
        collateral_unsuck_out=float(mu[out_unsuck].sum()), n_unsuck_out=len(out_unsuck),
        collateral_unsuck_out_top=[(names[q], float(mu[q])) for q in sorted(out_unsuck, key=lambda q: -mu[q])[:8]],
        collateral_suck_out=float(mu[out_suck].sum()), n_suck_out=len(out_suck),
        collateral_suck_out_top=[(names[q], float(mu[q])) for q in sorted(out_suck, key=lambda q: -mu[q])[:6]],
        collateral_ratio=float(mu[out_unsuck].sum() / mu[Kc].sum()) if Kc else float('nan'),
        universality_max=max(univ.values()) if univ else float('nan'),
        KFB_size=len(KFB) + 1, KFB_mu=float(muKFB), n_components_all=len(compsS),
        neutral_into_cfb=neutral_into_cfb, neutral_into_cfb_outside_K=neutral_outside,
        mu_FB=float(mu[iFB]), mu_CT=float(mu[iCT]) if iCT is not None else None, mu_CFB=float(mu[iCFB]) if iCFB is not None else None,
        FB_unsuckerable=bool(not suck[iFB]), PB_in=bool(iPB is not None),
        pstar_block_classes=len(pstar_block), pstar_block_mu=float(mu[pstar_block].sum()),
        cfb_same_class_as_CT=bool(iCFB is None or iCT is None)))


def cutoff(cs):
    """cs: {n: (club, Kmask)}.  Track canons by source string."""
    out = []
    ns = sorted(cs)
    for n0, n1 in zip(ns[:-1], ns[1:]):
        c0, K0 = cs[n0]; c1, K1 = cs[n1]
        idx1 = {s: i for i, s in enumerate(c1.names) if c1.in_univ[i]}
        val1 = c1.play(K1)
        mem0 = [c0.names[x] for x in np.nonzero(K0)[0]]
        missing = [s for s in mem0 if s not in idx1]
        dropped = []
        for s in mem0:
            if s not in idx1: continue
            x = idx1[s]
            if K1[x]: continue
            why = []
            if val1[x, x] != 1: why.append('no longer self-cooperates')
            outs = [y for y in np.nonzero((val1[x] == 1) & c1.in_univ & ~K1)[0] if y != x]
            outs.sort(key=lambda y: (len(c1.names[y]), c1.names[y]))
            new = [c1.names[y] for y in outs if c1.names[y] not in set(c0.names)]
            dropped.append(dict(name=s, guarded=guarded(c1, x), why=why, coops_with=[c1.names[y] for y in outs[:3]], new_partners=new[:3]))
        new_members = [c1.names[x] for x in np.nonzero(K1)[0] if c1.names[x] not in set(mem0)]
        out.append(dict(n=n0, n1=n1, members=len(mem0), dropped=len(dropped), drop_share=len(dropped) / max(len(mem0), 1),
                        missing=missing, dropped_rows=dropped[:20], n_new=len(new_members), new_examples=sorted(new_members, key=len)[:8]))
    return out


def main():
    t0 = time.time(); R = dict()
    # 1. fixed points
    R['fixed_points'] = []
    for mode in ('full', 'pos'):
        for n in (6, 7):
            r = enumerate_fixed_points(n, mode)
            R['fixed_points'].append(r)
            print('[fp] %s n=%d: universe %d, %d fixed points, K* %d, cycles %s, union %d fixed %s, all below K* %s, maximal %d, mono viol %d/%d (inside K* %d/%d)' % (
                mode, n, r['universe'], r['n_fixed_points'], r['kstar_size'], r['any_cycle'], r['union_size'], r['union_is_fixed'],
                r['all_fixed_points_below_kstar'], r['n_maximal'], r['monotonicity_violations'], r['monotonicity_pairs'],
                r['monotonicity_violations_inside_kstar'], r['monotonicity_pairs']), flush=True)
    # 2. sanity: base language
    R['sanity'] = []
    for n in (6, 7, 8, 9):
        c, K, steps = solve_kstar(n, club=False)
        R['sanity'].append(dict(n=n, K=int(K.sum()), members=[c.names[x] for x in np.nonzero(K)[0]][:10], steps=steps))
        print('[sanity] base n=%d: |K| = %d (%d steps)' % (n, K.sum(), steps), flush=True)
    # 3. composition, collateral, drift-closure, cutoff
    R['composition'] = []; cs = {}
    for mode in ('full', 'pos'):
        for n in (6, 7, 8, 9):
            t = time.time()
            c, K, steps = solve_kstar(n, mode=mode)
            comp = composition(c, K)
            o = comp['out']; o.update(n=n, mode=mode, steps=steps)
            R['composition'].append(o)
            if mode == 'full': cs[n] = (c, K)
            print('[comp] %s n=%d: K %d canons / %d classes / %.0f programs, mu %.4g (CT %.4g), share of self-coop %.3f; within-K comps %d (largest %d); suckerable members %d; neutral into cFB outside K %d; collateral unsuck out %.4g (x%.1f), suck out %.4g; univ max %.3g (%.1fs)' % (
                mode, n, o['K_canons'], o['K_classes'], o['K_programs'], o['K_mu'], o['mu_CT'] or 0, o['K_share_selfcoop'], o['within_K_n_components'],
                o['within_K_largest'], o['n_suckerable_members'], len(o['neutral_into_cfb_outside_K']), o['collateral_unsuck_out'], o['collateral_ratio'],
                o['collateral_suck_out'], o['universality_max'], time.time() - t), flush=True)
    R['cutoff'] = cutoff(cs)
    for r in R['cutoff']:
        print('[cutoff] %d -> %d: %d members, %d dropped (%.2f), %d missing, %d new' % (r['n'], r['n1'], r['members'], r['dropped'], r['drop_share'], len(r['missing']), r['n_new']), flush=True)
    R['time_s'] = time.time() - t0
    json.dump(R, open(os.path.join(ROOT, 'runs', 'club_static.json'), 'w'), indent=1, default=str)


# ------------------------------------------------------------------ at the maximal fixed point (runs/club_maximal.json)
def main_kmax():
    """Composition, collateral, drift-closure check and cutoff dependence at K_max, the greatest fixed point found by
    src/club_maximal.py (the limit from the full set is not the greatest at n >= 8, since F is not monotone)."""
    KM = {(r['n'], r['mode']): r['K_max_members'] for r in json.load(open(os.path.join(ROOT, 'runs', 'club_maximal.json')))}
    R = dict(composition=[]); cs = {}
    for mode in ('full', 'pos'):
        for n in (6, 7, 8, 9):
            if (n, mode) not in KM: continue
            c = CL.Club(n, mode=mode)
            K = c.mask([c.names.index(s) for s in KM[(n, mode)]])
            F, _ = c.F(K); assert (F == K).all()
            o = composition(c, K)['out']; o.update(n=n, mode=mode)
            R['composition'].append(o)
            if mode == 'full': cs[n] = (c, K)
            print('[comp K_max] %s n=%d: K %d canons / %d classes / %.0f programs, mu %.4g (CT %.4g), share of self-coop %.3f; within-K comps %d (largest %d, singletons %s); suckerable members %d (mu %.3g); neutral into cFB outside K %d; collateral unsuck out %.4g (x%.2f), suck out %.4g; univ max %.3g' % (
                mode, n, o['K_canons'], o['K_classes'], o['K_programs'], o['K_mu'], o['mu_CT'] or 0, o['K_share_selfcoop'], o['within_K_n_components'],
                o['within_K_largest'], o['within_K_all_singletons'], o['n_suckerable_members'], o['mu_suckerable_members'], len(o['neutral_into_cfb_outside_K']),
                o['collateral_unsuck_out'], o['collateral_ratio'], o['collateral_suck_out'], o['universality_max']), flush=True)
    R['cutoff'] = cutoff(cs)
    for r in R['cutoff']:
        print('[cutoff K_max] %d -> %d: %d members, %d dropped (%.2f), %d missing, %d new: %s' % (r['n'], r['n1'], r['members'], r['dropped'], r['drop_share'], len(r['missing']), r['n_new'], r['new_examples']), flush=True)
    json.dump(R, open(os.path.join(ROOT, 'runs', 'club_static_kmax.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    if '--kmax' in sys.argv:
        main_kmax()
    else:
        main()
