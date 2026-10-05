"""Compatibility among co-seeded establishers: the seed lottery's second condition.
Spec specs/2026-10-05-compatibility.md; predictions predictions/2026-10-05-compatibility.md.

Modal arm, PD, w = 0.3, eps = 0.  Class data from src/spoiler_conditioned.py (`cdata`: the modal language evaluated once
at n = 12, classes merged within L_n by identical row and column, cached in cache/spoiler-n{6,9,12}.npz).

    python3 src/compatibility.py check       # cached class data equals modal.build at n = 6, 9
    python3 src/compatibility.py static      # parts 1-3 -> runs/compatibility-static.json
    python3 src/compatibility.py reanalyze   # part 4 -> runs/compatibility-reanalysis.json
    python3 src/compatibility.py lottery     # part 5a -> runs/compatibility-lottery.json.gz
    python3 src/compatibility.py pairs       # part 5b -> runs/compatibility-pairs.json
    python3 src/compatibility.py report      # runs/compatibility.md and runs/compatibility.json
"""
import argparse, gzip, itertools, json, math, os, sys, time
from collections import Counter, defaultdict
import numpy as np
from numba import njit
sys.path.insert(0, os.path.dirname(__file__))
import spoiler_conditioned as SC

ROOT = SC.ROOT
RUNS = SC.RUNS
NS = (6, 9, 12)
NS_N = (100, 400)
NSIM = 100000
CONSEQ = 0.01
MU_HEAVY = 1e-4
STATIC = os.path.join(RUNS, 'compatibility-static.json')
REAN = os.path.join(RUNS, 'compatibility-reanalysis.json')
LOTT = os.path.join(RUNS, 'compatibility-lottery.json.gz')
PAIRS = os.path.join(RUNS, 'compatibility-pairs.json')
NAMED = ['BOX(THEM(ME))', 'BOX1(THEM(ME))', 'BOX(THEM(THEM))', 'BOX1(THEM(THEM))', 'BOX(THEM(^C))', 'BOX1(THEM(^C))',
         'and(BOX(THEM(ME)),BOXD1(THEM(^D)))']
OBSERVED = ('not(BOXD(THEM(THEM)))', 'BOX1(THEM(^BOX1(THEM(^D))))')     # the unresolved island, seeds-in-n n = 9 (400, 4) mN = 0 rep 94


def coseed(mx, my, N):
    """Exact P(x and y both present) in a multinomial seed of N draws."""
    return 1.0 - (1.0 - mx) ** N - (1.0 - my) ** N + (1.0 - mx - my) ** N


def ptype(V, x, y):
    a, b = int(V[x, y]), int(V[y, x])
    if a and b: return 'CC'
    if not a and not b: return 'DD'
    return 'exploit'


@njit(cache=True)
def _any_pair(draws, inset, loc, B):
    """Per island (row of draws): 1 if two distinct present classes in the set (inset[c]) have B[loc[a], loc[b]] true."""
    S, N = draws.shape
    out = np.zeros(S, np.bool_)
    buf = np.zeros(N, np.int64)
    for s in range(S):
        m = 0
        for t in range(N):
            c = draws[s, t]
            if inset[c]:
                dup = False
                for u in range(m):
                    if buf[u] == c:
                        dup = True; break
                if not dup:
                    buf[m] = c; m += 1
        hit = False
        for u in range(m):
            for v in range(u + 1, m):
                if B[loc[buf[u]], loc[buf[v]]]:
                    hit = True; break
            if hit: break
        out[s] = hit
    return out


def sim_any(mu, members, B, N, seed, nsim=NSIM, chunk=10000):
    """Simulated P(some pair of distinct present classes among `members` has B true), nsim seeds of N iid draws."""
    K = len(mu)
    inset = np.zeros(K, np.bool_); inset[members] = True
    loc = -np.ones(K, np.int64); loc[members] = np.arange(len(members))
    cum = np.cumsum(mu); cum[-1] = 1.0
    rng = np.random.default_rng(seed)
    hits = 0
    for c0 in range(0, nsim, chunk):
        m = min(chunk, nsim - c0)
        draws = np.searchsorted(cum, rng.random((m, N)), side='right').astype(np.int64)
        hits += int(_any_pair(draws, inset, loc, np.ascontiguousarray(B)).sum())
    return hits / nsim


def exact_any(muH, B, N):
    """Exact P(some pair of distinct present classes in H has B true), H small: inclusion-exclusion over present sets."""
    h = len(muH)
    MH = float(sum(muH))
    # f[T] = P(present & H subset of T) = (1 - mu(H) + mu(T))^N
    f = np.zeros(1 << h)
    for T in range(1 << h):
        mt = sum(muH[i] for i in range(h) if T >> i & 1)
        f[T] = (1.0 - MH + mt) ** N
    # g[S] = P(present & H == S) by Moebius inversion (subset-sum transform)
    g = f.copy()
    for i in range(h):
        bit = 1 << i
        for S in range(1 << h):
            if S & bit:
                g[S] -= g[S ^ bit]
    p_ok = 0.0
    for S in range(1 << h):
        idx = [i for i in range(h) if S >> i & 1]
        if all(not B[a, b] for a, b in itertools.combinations(idx, 2)):
            p_ok += g[S]
    return 1.0 - p_ok


def components(M):
    from scipy.sparse.csgraph import connected_components
    from scipy.sparse import csr_matrix
    nc, lab = connected_components(csr_matrix(M.astype(np.int8)), directed=False)
    return nc, lab


# ------------------------------------------------------------------ check
def check_main(a):
    import seeds_in_n as SN
    for n in (6, 9):
        d = SN.data(n); c = SC.cdata(n)
        perm = [c['names'].index(x) for x in d['names']]
        Vb = c['V'][np.ix_(perm, perm)]
        print('n=%d: classes %d vs %d, max |dmu| %.2e, U equal %s' % (
            n, len(d['names']), c['K'], np.abs(d['mu'] - c['mu'][perm]).max(), np.array_equal(SC.PDP[Vb, Vb.T], d['U'])), flush=True)
    print('n=12: %d classes' % SC.cdata(12)['K'])


# ------------------------------------------------------------------ static (parts 1-3)
def static_n(n):
    t0 = time.time()
    d = SC.cdata(n); V = d['V']; mu = d['mu']; nm = d['names']; K = d['K']
    E = np.nonzero(d['est'])[0]
    mE = mu[E]; mest = float(mE.sum())
    Ve = V[np.ix_(E, E)].astype(bool)
    MC = Ve & Ve.T; DD = ~Ve & ~Ve.T; EX = Ve ^ Ve.T
    np.fill_diagonal(MC, True); np.fill_diagonal(DD, False); np.fill_diagonal(EX, False)
    w = np.outer(mE, mE)
    den = mest ** 2
    off = 1.0 - np.eye(len(E), dtype=bool)
    r = dict(n=n, classes=K, n_est=int(len(E)), mu_est=mest,
             kappa=float(w[MC].sum() / den), dd_rate=float(w[DD].sum() / den), ex_rate=float(w[EX].sum() / den),
             kappa_distinct=float(w[MC & off.astype(bool)].sum() / (den - float((mE ** 2).sum()))),
             same_class_share=float((mE ** 2).sum() / den))
    # exploiter / exploited split of exploitation
    # components of the mutual-cooperation graph (no self-loops)
    Mg = MC & off.astype(bool)
    nc, lab = components(Mg)
    comp = []
    for c in range(nc):
        idx = np.nonzero(lab == c)[0]
        mc = float(mE[idx].sum())
        sub = Mg[np.ix_(idx, idx)]
        miss = ~sub & ~np.eye(len(idx), dtype=bool)
        mm = float((np.outer(mE[idx], mE[idx])[miss]).sum() / 2)
        comp.append(dict(size=int(len(idx)), mass=mc, share_of_est=mc / mest, missing_edge_mass=mm,
                         missing_frac=mm / (mc ** 2 / 2) if mc > 0 else 0.0,
                         heaviest=[(nm[E[i]], float(mE[i])) for i in idx[np.argsort(-mE[idx])][:6]]))
    comp.sort(key=lambda c: -c['mass'])
    r['n_components'] = nc
    r['components'] = comp[:12]
    r['singleton_components_mass'] = float(sum(c['mass'] for c in comp if c['size'] == 1))
    loc = {int(e): i for i, e in enumerate(E)}
    # heavy set
    heavy = [int(e) for e in E if mu[e] >= MU_HEAVY]
    for x in NAMED:
        if x in nm and nm.index(x) not in heavy and d['est'][nm.index(x)]:
            heavy.append(nm.index(x))
    heavy.sort(key=lambda e: -mu[e])
    cmass = np.bincount(lab, weights=mE, minlength=nc)
    rank = np.empty(nc, np.int64); rank[np.argsort(-cmass, kind='stable')] = np.arange(nc)
    r['heavy'] = [dict(name=nm[e], mu=float(mu[e]), comp_rank=int(rank[lab[loc[e]]]),
                       vs_D=int(V[e, d['iD']]), vs_ALLC=int(V[e, d['iC']])) for e in heavy]
    r['heavy_matrix'] = [[ptype(V, x, y) if x != y else 'self' for y in heavy] for x in heavy]
    r['heavy_play'] = [[int(V[x, y]) for y in heavy] for x in heavy]        # row cooperates with column
    for x in NAMED:
        if x not in nm or not d['est'][nm.index(x)]:
            r.setdefault('named_missing', []).append(x)
    # incompatible pairs (distinct establisher classes)
    inc = DD | EX
    iu = np.argwhere(np.triu(inc, 1))
    pm = mE[iu[:, 0]] * mE[iu[:, 1]]
    r['dd_pair_mass'] = float((np.triu(DD, 1) * w).sum()); r['ex_pair_mass'] = float((np.triu(EX, 1) * w).sum())
    r['dd_pair_frac'] = 2 * r['dd_pair_mass'] / den; r['ex_pair_frac'] = 2 * r['ex_pair_mass'] / den
    pairs = []
    for (i, j), m_ in zip(iu, pm):
        x, y = int(E[i]), int(E[j])
        p400 = coseed(mu[x], mu[y], 400)
        if p400 >= 1e-3:
            t = ptype(V, x, y)
            if t == 'exploit' and V[x, y] == 1:      # order: exploiter first
                x, y = y, x
            pairs.append(dict(x=nm[x], y=nm[y], type=t, mu_x=float(mu[x]), mu_y=float(mu[y]), pair_mass=float(m_),
                              co100=coseed(mu[x], mu[y], 100), co400=p400, same_component=bool(lab[loc[x]] == lab[loc[y]]),
                              x_vs_D=int(V[x, d['iD']]), y_vs_D=int(V[y, d['iD']]), x_vs_C=int(V[x, d['iC']]), y_vs_C=int(V[y, d['iC']])))
    pairs.sort(key=lambda p: -p['co400'])
    r['incompatible_pairs'] = pairs
    r['n_incompatible_pairs'] = int(len(iu)); r['n_dd_pairs'] = int(np.triu(DD, 1).sum()); r['n_ex_pairs'] = int(np.triu(EX, 1).sum())
    r['consequential'] = [p for p in pairs if p['co400'] >= CONSEQ]
    # co-seeding of any incompatible pair: simulated over all establishers, exact and simulated over the heavy set
    hl = np.array([loc[e] for e in heavy])
    Bh = inc[np.ix_(hl, hl)]
    r['coseed_any'] = {}
    for N in NS_N:
        s_all = sim_any(mu, E, inc, N, [n, N, 1])
        s_dd = sim_any(mu, E, DD, N, [n, N, 1])            # same seeds (same RNG seed)
        s_h = sim_any(mu, np.array(heavy), Bh, N, [n, N, 1])
        e_h = exact_any([float(mu[e]) for e in heavy], Bh, N) if len(heavy) <= 16 else None
        s_est = sim_any(mu, E, np.ones_like(inc), N, [n, N, 1])     # two or more distinct establisher classes
        r['coseed_any'][str(N)] = dict(sim_all=s_all, sim_dd=s_dd, sim_heavy=s_h, exact_heavy=e_h, sim_two_est=s_est)
    del Ve, MC, DD, EX, w, inc
    # anti-coordinators over all classes
    diag0 = np.diagonal(V) == 0
    cand = np.nonzero(diag0 & (V.sum(1) > 0))[0]
    Vc = V[np.ix_(cand, cand)].astype(bool)
    A = Vc & Vc.T
    np.fill_diagonal(A, False)
    ia = np.argwhere(np.triu(A, 1))
    ac = []
    mx_, my_ = mu[cand[ia[:, 0]]], mu[cand[ia[:, 1]]]
    tot_mass = float((mx_ * my_).sum())
    p400s = coseed(mx_, my_, 400)
    obs = [nm.index(o) for o in OBSERVED if o in nm]
    for k_ in np.nonzero((p400s >= 1e-4) | (np.isin(cand[ia[:, 0]], obs) & np.isin(cand[ia[:, 1]], obs)))[0]:
        i, j = ia[k_]
        x, y = int(cand[i]), int(cand[j])
        m_ = float(mu[x] * mu[y]); p400 = float(p400s[k_])
        if True:
            ac.append(dict(x=nm[x], y=nm[y], mu_x=float(mu[x]), mu_y=float(mu[y]), pair_mass=m_, co100=coseed(mu[x], mu[y], 100),
                           co400=p400, x_vs_D=int(V[x, d['iD']]), y_vs_D=int(V[y, d['iD']]), x_vs_C=int(V[x, d['iC']]),
                           y_vs_C=int(V[y, d['iC']]), x_self=int(V[x, x]), y_self=int(V[y, y])))
    ac.sort(key=lambda p: -p['co400'])
    bothD = (V[cand[ia[:, 0]], d['iD']] == 0) & (V[cand[ia[:, 1]], d['iD']] == 0)
    r['anti'] = dict(n_pairs=int(len(ia)), pair_mass=tot_mass * 2, pair_mass_frac_of_mu2=tot_mass * 2, n_classes=int(len(np.unique(ia))) if len(ia) else 0,
                     class_mass=float(mu[cand[np.unique(ia)]].sum()) if len(ia) else 0.0,
                     n_pairs_both_defect_D=int(bothD.sum()), pairs=ac[:40],
                     observed=[p for p in ac if (p['x'], p['y']) in (OBSERVED, OBSERVED[::-1])])
    r['anti']['coseed_any'] = {}
    if len(ia):
        Ab = np.zeros_like(A); Ab2 = np.zeros_like(A)
        Ab[ia[bothD, 0], ia[bothD, 1]] = True; Ab[ia[bothD, 1], ia[bothD, 0]] = True
        Ab2[ia[~bothD, 0], ia[~bothD, 1]] = True; Ab2[ia[~bothD, 1], ia[~bothD, 0]] = True
        for N in NS_N:
            r['anti']['coseed_any'][str(N)] = dict(all=sim_any(mu, cand, A, N, [n, N, 2]), both_defect_D=sim_any(mu, cand, Ab, N, [n, N, 2]),
                                                   other=sim_any(mu, cand, Ab2, N, [n, N, 2]))
    del Vc, A
    r['time_s'] = time.time() - t0
    return r


def static_main(a):
    out = json.load(open(STATIC)) if os.path.exists(STATIC) else {}
    for n in (a.n or NS):
        r = static_n(n)
        out[str(n)] = r
        json.dump(out, open(STATIC, 'w'), indent=1)
        print('n=%d: %d est, mu_est %.4f, kappa %.4f (distinct %.4f), DD %.4f, exploit %.4f; %d components; %d incompatible pairs '
              '(%d DD, %d exploit), %d consequential; co-seed any N=100 %.3f N=400 %.3f; anti pairs %d, co-seed any(400) %s; %.0fs' % (
                  n, r['n_est'], r['mu_est'], r['kappa'], r['kappa_distinct'], r['dd_rate'], r['ex_rate'], r['n_components'],
                  r['n_incompatible_pairs'], r['n_dd_pairs'], r['n_ex_pairs'], len(r['consequential']),
                  r['coseed_any']['100']['sim_all'], r['coseed_any']['400']['sim_all'], r['anti']['n_pairs'],
                  r['anti']['coseed_any'].get('400'), r['time_s']), flush=True)
        if n == 12:
            SC._C.pop(12, None)


# ------------------------------------------------------------------ re-analysis (part 4)
CERT = ('certified-frozen', 'certified-separated', 'local-frozen')
_VN = {}


def vdata(n):
    """names -> index and the 0/1 play matrix at cutoff n (cdata for 6, 9, 12; modal.build via seeds_in_n otherwise)."""
    if n in _VN:
        return _VN[n]
    if n in NS:
        d = SC.cdata(n); V = d['V']; nm = d['names']; est = d['est']; selfc = d['selfc']
    else:
        import seeds_in_n as SN
        d = SN.data(n); U = d['U']; nm = d['names']
        V = ((U == 0) | (U == -2)).astype(np.uint8)          # row cooperates: R = 0 or S = -2
        iD = nm.index('D')
        selfc = np.diagonal(V).astype(bool); allc = V.all(1).astype(bool)
        est = selfc & (V[:, iD] == 0) & ~allc
    _VN[n] = dict(V=V, idx={x: i for i, x in enumerate(nm)}, est=est, selfc=selfc, names=nm)
    return _VN[n]


def island_rec(n, comp, cert, pcc_known=None, code=None):
    """One island: comp = {name: count} (or None), cert flag, P(C,C) if known, outcome code if known."""
    v = vdata(n)
    rec = dict(cert=cert)
    if comp is not None:
        ids = [v['idx'][x] for x in comp]
        cnt = np.array([comp[x] for x in comp], float); Nn = cnt.sum()
        Vs = v['V'][np.ix_(ids, ids)].astype(float)
        pair = np.outer(cnt, cnt) - np.diag(cnt)            # ordered pairs of distinct individuals
        cc = float((pair * Vs * Vs.T).sum() / (Nn * (Nn - 1)))
        dd = float((pair * (1 - Vs) * (1 - Vs.T)).sum() / (Nn * (Nn - 1)))
        E = [i for i in ids if v['est'][i]]
        rec.update(pcc=cc, pareto=dd == 0.0, n_est=len(E), support=len(ids))
        if len(E) >= 2:
            sub = v['V'][np.ix_(E, E)]
            rec['est_compatible'] = bool((sub & sub.T).all())
            rec['est_support'] = sorted(((x, int(comp[x])) for x in comp if v['est'][v['idx'][x]]), key=lambda t: -t[1])
        rec['coop'] = cert and all(v['selfc'][i] for i in ids) and not all(v['V'][i].all() for i in ids)
    else:
        rec.update(pcc=pcc_known, pareto=None, n_est=None, support=None)
        rec['coop'] = None
    if code is not None:
        rec['code'] = code
    return rec


def frozen(n, comp):
    v = vdata(n); ids = [v['idx'][x] for x in comp]
    Vs = v['V'][np.ix_(ids, ids)].astype(np.int64)
    U = SC.PDP[Vs, Vs.T]
    return bool(U.max() - U.min() < 1e-12)


def separated_detail():
    rows = json.load(open(os.path.join(RUNS, 'seeds-in-n.json')))['rows']
    out = []
    for r in rows:
        if r['status'] != 'certified-separated':
            continue
        v = vdata(r['n']); cl = list(r['final'])
        ids = [v['idx'][x] for x in cl]
        out.append(dict(n=r['n'], N=r['N'], I=r['I'], rep=r['rep'], final=r['final'],
                        est=[bool(v['est'][i]) for i in ids],
                        pairs=[(cl[a_], cl[b_], ptype(v['V'], ids[a_], ids[b_])) for a_ in range(len(ids)) for b_ in range(a_ + 1, len(ids))],
                        islands_out=Counter(r['isl_out'])))
    return out


def forced_unresolved():
    """Regenerate the unresolved forced spoiler islands (deterministic frc_job init) for their terminal support."""
    frc = json.load(gzip.open(os.path.join(RUNS, 'spoiler-conditioned-rows-frc.json.gz'), 'rt'))
    todo = [(r['n'], r['N'], r['pair'], r['rep'], r['salt'], k) for r in frc for k, rec in r['out'].items() if not rec[0]]
    del frc
    out = []
    for n, N, pi, rep, salt, key in todo:
        d = SC.cdata(n); mu = d['mu']; nm = d['names']
        P = SC.forced_pairs(n)[pi]; t, q = P['t'], P['q']
        rng = np.random.default_rng([n, N, pi, rep, salt])
        bg = rng.multinomial(N, mu).astype(np.int64)
        slots = np.repeat(np.arange(d['K']), bg); perm = rng.permutation(N)
        ss = 1000003 * rep + 7 * N + 13 * n + 101 * pi + salt % 100000
        tr = key.rstrip('0123456789'); k = int(key[len(tr):])
        first = slots[perm[:k]]; second = slots[perm[10:10 + k]]
        init = bg.copy()
        if tr in ('a', 'b', 'c', 'cD'):
            np.subtract.at(init, first, 1); init[t] += k
        if tr in ('b', 'c', 'cD'):
            np.subtract.at(init, second, 1); init[{'b': q, 'c': t, 'cD': d['iD']}[tr]] += k
        if tr == 'd':
            np.subtract.at(init, first, 1); init[q] += k
        cat = np.full(d['K'], 5, np.int64)
        res = SC.simulate(d, init, N, ss, cat, keep_log=False)
        fin = res['final']; ids = list(fin)
        out.append(dict(n=n, N=N, pair=pi, rep=rep, key=key, status=res['status'], pcc=res['pcc'],
                        final={nm[c]: v for c, v in fin.items()}, est=[bool(d['est'][c]) for c in ids],
                        self=[int(d['V'][c, c]) for c in ids], vsD=[int(d['V'][c, d['iD']]) for c in ids],
                        pairs=[(nm[a_], nm[b_], ptype(d['V'], a_, b_)) for i_, a_ in enumerate(ids) for b_ in ids[i_ + 1:]],
                        ext=sorted(((nm[c], t_) for c, t_ in res['ext'].items() if c in set(np.nonzero(init)[0]) and init[c] > 0), key=lambda z: z[1])[-6:]))
        print('forced unresolved', out[-1]['n'], out[-1]['pair'], out[-1]['rep'], key, out[-1]['status'], out[-1]['final'], out[-1]['pairs'], flush=True)
    return out


def reanalyze_main(a):
    out = {}
    recs = defaultdict(list)
    # seeds-in-n (n = 6..9)
    rows = json.load(open(os.path.join(RUNS, 'seeds-in-n.json')))['rows']
    for r in rows:
        cert = r['status'] in CERT
        src = 'seeds-in-n mN=%g' % r['mN']
        if r['isl_final'] is not None:
            for i, comp in enumerate(r['isl_final']):
                c_i, st_i = cert, r['status']
                if r['mN'] == 0:          # independent islands: the certification rule applied per island
                    c_i = frozen(r['n'], comp); st_i = 'local-frozen' if c_i else 'unresolved'
                recs[(src, r['n'])].append(dict(island_rec(r['n'], comp, c_i), status=st_i, run=(r['N'], r['I'], r['rep'], i)))
        else:
            # I = 64, 256: per-island compositions not stored; outcome codes e/d/o; global support for the establisher count
            g = island_rec(r['n'], r['final'], cert)
            for c in r['isl_out']:
                recs[(src + ' (I>16, global support)', r['n'])].append(dict(cert=cert, pcc=None, code=c, pareto=None, status=r['status'],
                                                                              n_est=None, coop=None))
            recs[(src + ' (I>16, run level)', r['n'])].append(dict(g, status=r['status'], run=(r['N'], r['I'], r['rep'])))
    # seeds-tail (n = 12)
    for r in json.load(open(os.path.join(RUNS, 'seeds-tail-rows.json'))):
        cert = r['status'] in CERT
        for comp in r['isl_final']:
            recs[('seeds-tail mN=%g' % r['mN'], 12)].append(dict(island_rec(12, comp, cert), status=r['status'], run=(r['N'], r['I'], r['rep'])))
    # spoiler-conditioned natural islands (n = 6, 9, 12; complete support: final_support <= 6 everywhere)
    nat = json.load(gzip.open(os.path.join(RUNS, 'spoiler-conditioned-rows-nat.json.gz'), 'rt'))
    for r in nat:
        assert r['final_support'] == len(r['final_top'])
        comp = {x: c for x, c in r['final_top']}
        rr = island_rec(r['n'], comp, r['status'] in CERT)
        assert abs(rr['pcc'] - r['pcc']) < 1e-9, (rr['pcc'], r['pcc'])
        recs[('spoiler natural', r['n'])].append(dict(rr, status=r['status'], N=r['N'], ext=r['ext']))
    # spoiler-conditioned forced islands: resolved flag, P(C,C), cooperative fixation (no support stored)
    frc = json.load(gzip.open(os.path.join(RUNS, 'spoiler-conditioned-rows-frc.json.gz'), 'rt'))
    for r in frc:
        for k, rec in r['out'].items():
            recs[('spoiler forced', r['n'])].append(dict(cert=bool(rec[0]), pcc=rec[7], coop=bool(rec[0]) and bool(rec[3]), pareto=None,
                                                          n_est=None, status='local-frozen' if rec[0] else 'unresolved'))
    del nat, frc
    for (src, n), L in sorted(recs.items()):
        st = Counter(x['status'] for x in L)
        C = [x for x in L if x['cert']]
        pk = [x for x in C if x.get('pcc') is not None]
        res = dict(source=src, n=n, islands=len(L), status=dict(st), certified=len(C), excluded=len(L) - len(C), horizon=100000)
        if pk:
            res['pcc_below_095'] = sum(x['pcc'] < 0.95 for x in pk); res['pcc_known'] = len(pk)
            res['pcc_strictly_between'] = sum(0.0 < x['pcc'] < 1.0 for x in pk)
        cod = [x for x in C if x.get('code')]
        if cod:
            res['codes'] = dict(Counter(x['code'] for x in cod))
        pa = [x for x in C if x.get('pareto') is not None]
        if pa:
            res['pareto_inefficient'] = sum(not x['pareto'] for x in pa); res['pareto_known'] = len(pa)
            res['pareto_ineff_but_pcc_ge_095'] = sum((not x['pareto']) and x['pcc'] >= 0.95 for x in pa)
        co = [x for x in C if x.get('coop')]
        res['frozen_coop'] = len(co); res['frozen_coop_pcc_below_095'] = sum(x['pcc'] is not None and x['pcc'] < 0.95 for x in co)
        me = [x for x in C if (x.get('n_est') or 0) >= 2]
        res['multi_est'] = len(me)
        res['multi_est_compatible'] = sum(x['est_compatible'] for x in me)
        res['multi_est_incompatible'] = sum(not x['est_compatible'] for x in me)
        res['multi_est_pcc_ge_095'] = sum(x['pcc'] is not None and x['pcc'] >= 0.95 for x in me)
        ex = [x for x in L if not x['cert']]
        res['uncertified'] = [dict(status=x['status'], run=x.get('run'), pcc=x.get('pcc'), n_est=x.get('n_est'),
                                   est_support=x.get('est_support'), est_compatible=x.get('est_compatible')) for x in ex][:20]
        res['multi_est_examples'] = Counter(tuple(t[0] for t in x['est_support']) for x in me).most_common(8)
        out['%s | n=%d' % (src, n)] = res
        print('%-45s n=%2d islands %6d certified %6d excl %3d | P(C,C)<.95 %s / %s (strictly between %s) | Pareto-ineff %s / %s | frozen coop %d (below .95: %d) | multi-est %d (compat %d, incompat %d, P(C,C)>=.95 %d)' % (
            src, n, len(L), len(C), len(L) - len(C), res.get('pcc_below_095'), res.get('pcc_known'), res.get('pcc_strictly_between'),
            res.get('pareto_inefficient'), res.get('pareto_known'), res['frozen_coop'], res['frozen_coop_pcc_below_095'], len(me),
            res['multi_est_compatible'], res['multi_est_incompatible'], res['multi_est_pcc_ge_095']), flush=True)
    out['separated_runs'] = separated_detail()
    for x in out['separated_runs']: print('separated', x)
    out['forced_unresolved'] = forced_unresolved()
    json.dump(out, open(REAN, 'w'), indent=1)


# ------------------------------------------------------------------ conditioned lottery and pair competitions (part 5)
NL = 12
NLOT = 400
SALT_COND, SALT_DD, SALT_UNC, SALT_PAIR = 20261051, 20261052, 20261053, 20261054
GENS_PAIR = 20000      # pair competitions: administrative horizon (anti-coordinator polymorphisms never freeze)
PRUDENT = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
PSTAR = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'


def pair_sets():
    """The consequential incompatible establisher pairs at n = 12 (predeclared), the added mutually-defecting pairs, and
    the anti-coordinator pairs (12 heaviest by co-seeding at N = 400, the heaviest that both defect on D, the observed)."""
    S = json.load(open(STATIC))[str(NL)]
    d = SC.cdata(NL); nm = d['names']; ix = {x: i for i, x in enumerate(nm)}
    cons = [(p['x'], p['y'], 'conseq-' + p['type']) for p in S['consequential']]
    dd = [p for p in S['incompatible_pairs'] if p['type'] == 'DD']
    added = [(dd[0]['x'], dd[0]['y'], 'added-DD heaviest'), ('BOX1(THEM(ME))', PRUDENT, 'added-DD PrudentBot'),
             ('BOX(THEM(^C))', PRUDENT, 'added-DD PrudentBot'), ('BOX1(THEM(ME))', PSTAR, 'added-DD P* (separated runs)')]
    anti = [(p['x'], p['y'], 'anti (co400 %.3f)' % p['co400']) for p in S['anti']['pairs'] if p['co400'] >= CONSEQ][:12]
    bothD = [p for p in S['anti']['pairs'] if p['x_vs_D'] == 0 and p['y_vs_D'] == 0]
    anti.append((bothD[0]['x'], bothD[0]['y'], 'anti heaviest both-defect-D'))
    anti.append((OBSERVED[0], OBSERVED[1], 'anti observed (seeds-in-n n=9)'))
    out = []
    for x, y, lab in cons + added + anti:
        a_, b_ = ix[x], ix[y]
        out.append(dict(x=x, y=y, label=lab, type=ptype(d['V'], a_, b_), xi=a_, yi=b_,
                        self=(int(d['V'][a_, a_]), int(d['V'][b_, b_])), est=(bool(d['est'][a_]), bool(d['est'][b_])),
                        vsD=(int(d['V'][a_, d['iD']]), int(d['V'][b_, d['iD']]))))
    return out


def _fate(fin, x, y):
    a_, b_ = x in fin, y in fin
    return 'both' if a_ and b_ else 'x' if a_ else 'y' if b_ else 'neither'


def lottery_job(j):
    kind, rep = j
    d = SC.cdata(NL); mu = d['mu']; nm = d['names']; V = d['V']; est = d['est']
    S = json.load(open(STATIC))[str(NL)]
    ix = {x: i for i, x in enumerate(nm)}
    cons = [(ix[p['x']], ix[p['y']]) for p in S['consequential']]
    salt = {'cond': SALT_COND, 'dd': SALT_DD, 'unc': SALT_UNC}[kind]
    rng = np.random.default_rng([NL, 400, rep, salt])
    tries = 0
    while True:
        tries += 1
        init = rng.multinomial(400, mu).astype(np.int64)
        sup = np.nonzero(init)[0]
        E = sup[est[sup]]
        Ve = V[np.ix_(E, E)]
        DDm = (Ve == 0) & (Ve.T == 0); EXm = Ve != Ve.T
        ddp = [(int(E[a_]), int(E[b_])) for a_, b_ in np.argwhere(np.triu(DDm, 1))]
        exp_ = [(int(E[a_]), int(E[b_])) for a_, b_ in np.argwhere(np.triu(EXm, 1))]
        cp = [(x, y) for x, y in cons if init[x] > 0 and init[y] > 0]
        if kind == 'unc' or (kind == 'cond' and cp) or (kind == 'dd' and ddp):
            break
    ss = 1000003 * rep + 7 * 400 + 13 * NL + salt % 100000
    cat = np.full(d['K'], 5, np.int64)
    t0 = time.time()
    r = SC.simulate(d, init, 400, ss, cat, keep_log=False)
    fin = r['final']
    order = lambda x, y: (x, y) if V[x, y] == 0 or V[y, x] == 1 else (y, x)     # exploiter first
    def fates(pairs):
        out = []
        for x, y in pairs:
            x, y = order(x, y)
            out.append((nm[x], nm[y], int(init[x]), int(init[y]), _fate(fin, x, y), r['ext'].get(x, -1.0), r['ext'].get(y, -1.0)))
        return out
    fin_est = [c for c in fin if est[c]]
    inc_fin = [(nm[a_], nm[b_], ptype(V, a_, b_)) for i_, a_ in enumerate(fin_est) for b_ in fin_est[i_ + 1:] if ptype(V, a_, b_) != 'CC']
    return dict(kind=kind, rep=rep, tries=tries, status=r['status'], resolved=r['resolved'], stop_gen=r['stop_gen'], pcc=r['pcc'],
                coop_fix=r['coop_fix'], efficient=r['efficient'], final={nm[c]: v for c, v in fin.items()},
                n_est_seed=int(len(E)), n_est_final=len(fin_est), inc_final=inc_fin,
                cons=fates(cp), dd=fates(ddp), n_exploit_pairs=len(exp_),
                est_seed_mass=int(init[E].sum()), time_s=time.time() - t0)


def pair_job(j):
    pi, mode, nx, ny, rep = j
    P = pair_sets()[pi] if not hasattr(pair_job, 'P') else pair_job.P[pi]
    d = SC.cdata(NL); mu = d['mu']
    rng = np.random.default_rng([NL, pi, nx, ny, rep, SALT_PAIR, 0 if mode == 'pair' else 1])
    init = np.zeros(d['K'], np.int64)
    if mode == 'bg':
        init += rng.multinomial(400 - nx - ny, mu)
    init[P['xi']] += nx; init[P['yi']] += ny
    assert init.sum() == 400
    ss = 1000003 * rep + 101 * pi + 7 * nx + 3 * ny + (0 if mode == 'pair' else 55555) + SALT_PAIR % 100000
    cat = np.full(d['K'], 5, np.int64)
    t0 = time.time()
    r = SC.simulate(d, init, 400, ss, cat, gens=GENS_PAIR, keep_log=False)
    fin = r['final']
    return dict(pair=pi, mode=mode, nx=nx, ny=ny, rep=rep, status=r['status'], stop_gen=r['stop_gen'], pcc=r['pcc'],
                fate=_fate(fin, P['xi'], P['yi']), fx=int(fin.get(P['xi'], 0)), fy=int(fin.get(P['yi'], 0)),
                final_n=len(fin), final_top=sorted(((d['names'][c], v) for c, v in fin.items()), key=lambda t: -t[1])[:4],
                ext_x=r['ext'].get(P['xi'], -1.0), ext_y=r['ext'].get(P['yi'], -1.0), time_s=time.time() - t0)


def _warm5():
    SC.kernel(); SC.cdata(NL)
    pair_job.P = pair_sets()


def lottery_main(a):
    from multiprocessing import Pool
    jobs = [(k, rep) for k in ('cond', 'dd', 'unc') for rep in range(NLOT)]
    if a.time:
        _warm5(); t0 = time.time()
        rs = [lottery_job((k, rep)) for k in ('cond', 'dd', 'unc') for rep in range(1000, 1004)]
        print('timing (separate reps): %.2fs per island; max %.2f' % ((time.time() - t0) / len(rs), max(r['time_s'] for r in rs)))
        return
    rows = []; t0 = time.time()
    with Pool(a.procs, initializer=_warm5) as pool:
        for i, r in enumerate(pool.imap_unordered(lottery_job, jobs, chunksize=4)):
            rows.append(r)
            if (i + 1) % 100 == 0:
                print('%d / %d, %.0fs' % (i + 1, len(jobs), time.time() - t0), flush=True)
            if time.time() - t0 > 2 * 3600:
                print('ADMINISTRATIVE CENSORING at %d / %d' % (i + 1, len(jobs)), flush=True)
                pool.terminate(); break
    rows.sort(key=lambda r: (r['kind'], r['rep']))
    with gzip.open(LOTT, 'wt') as f:
        json.dump(rows, f)
    print('done %d islands, %.0fs' % (len(rows), time.time() - t0))


def pairs_main(a):
    from multiprocessing import Pool
    P = pair_sets()
    for i, p in enumerate(P):
        print(i, p['label'], p['x'], '|', p['y'], p['type'], 'self', p['self'], 'est', p['est'], 'vsD', p['vsD'], flush=True)
    jobs = []
    for pi in range(len(P)):
        for mode, starts in (('pair', ((200, 200), (300, 100), (100, 300))), ('bg', ((100, 100), (150, 50), (50, 150)))):
            for nx, ny in starts:
                for rep in range(100):
                    jobs.append((pi, mode, nx, ny, rep))
    if a.time:
        _warm5(); t0 = time.time()
        sel = [(pi, m, nx, ny, 1000) for pi in (0, 10, len(P) - 2, len(P) - 1) for m, nx, ny in (('pair', 200, 200), ('bg', 100, 100))]
        for j in sel:
            r = pair_job(j); print(j, r['status'], r['fate'], r['stop_gen'], '%.2fs' % r['time_s'], flush=True)
        return
    rows = []; t0 = time.time()
    with Pool(a.procs, initializer=_warm5) as pool:
        for i, r in enumerate(pool.imap_unordered(pair_job, jobs, chunksize=10)):
            rows.append(r)
            if (i + 1) % 1000 == 0:
                print('%d / %d, %.0fs' % (i + 1, len(jobs), time.time() - t0), flush=True)
            if time.time() - t0 > 2 * 3600:
                print('ADMINISTRATIVE CENSORING at %d / %d' % (i + 1, len(jobs)), flush=True)
                pool.terminate(); break
    rows.sort(key=lambda r: (r['pair'], r['mode'], r['nx'], r['rep']))
    json.dump(dict(pairs=[{k: v for k, v in p.items()} for p in P], rows=rows), open(PAIRS, 'w'))
    print('done %d runs, %.0fs' % (len(rows), time.time() - t0))


# ------------------------------------------------------------------ path, natural-row split and report
PATH = os.path.join(RUNS, 'compatibility-path.json')
NPATH = (100, 400, 1600, 6400, 25600)


def path_main(a):
    """Co-seeding of some incompatible establisher pair along N at n = 12 (exact on the heavy set; simulated over all
    establishers with 2e4 seeds at N > 400), and the natural-row split of efficiency by incompatibility."""
    S = json.load(open(STATIC))
    out = dict(coseed={}, natural={})
    for n in NS:
        d = SC.cdata(n); V = d['V']; mu = d['mu']; nm = d['names']
        E = np.nonzero(d['est'])[0]
        Ve = V[np.ix_(E, E)].astype(bool); inc = ~(Ve & Ve.T); np.fill_diagonal(inc, False)
        heavy = [nm.index(h['name']) for h in S[str(n)]['heavy']]
        loc = {int(e): i for i, e in enumerate(E)}
        hl = np.array([loc[e] for e in heavy]); Bh = inc[np.ix_(hl, hl)]
        cons = S[str(n)]['consequential']
        cc = sorted({nm.index(p['x']) for p in cons} | {nm.index(p['y']) for p in cons})
        cl = {c: i for i, c in enumerate(cc)}
        Bc = np.zeros((len(cc), len(cc)), bool)
        for p in cons:
            Bc[cl[nm.index(p['x'])], cl[nm.index(p['y'])]] = Bc[cl[nm.index(p['y'])], cl[nm.index(p['x'])]] = True
        rows = {}
        for N in NPATH:
            r = dict(exact_heavy=exact_any([float(mu[e]) for e in heavy], Bh, N),
                     exact_conseq=exact_any([float(mu[c]) for c in cc], Bc, N))
            if n == 12 and N <= 6400:
                r['sim_all'] = sim_any(mu, E, inc, N, [n, N, 3], nsim=20000 if N > 400 else NSIM)
            rows[str(N)] = r
            print('n=%d N=%d %s' % (n, N, r), flush=True)
        out['coseed'][str(n)] = rows
        del Ve, inc
        if n == 12: SC._C.pop(12, None)
    nat = json.load(gzip.open(os.path.join(RUNS, 'spoiler-conditioned-rows-nat.json.gz'), 'rt'))
    for n in NS:
        d = SC.cdata(n); V = d['V']; ix = {x: i for i, x in enumerate(d['names'])}
        for N in NS_N:
            g = defaultdict(lambda: [0, 0, 0])
            for r in nat:
                if r['n'] != n or r['N'] != N: continue
                E = [ix[x] for x in r['est']]
                prs = [(a_, b_) for i_, a_ in enumerate(E) for b_ in E[i_ + 1:]]
                if not E: key = 'no establisher'
                elif any(not V[a_, b_] and not V[b_, a_] for a_, b_ in prs): key = 'incompatible (some DD)'
                elif any(not (V[a_, b_] and V[b_, a_]) for a_, b_ in prs): key = 'incompatible (exploitation only)'
                elif len(E) > 1: key = 'compatible, 2+ establishers'
                else: key = 'one establisher'
                fe = [ix[x] for x, c in r['final_top'] if d['est'][ix[x]]]
                g[key][0] += 1; g[key][1] += int(r['efficient'])
                g[key][2] += int(any(not (V[a_, b_] and V[b_, a_]) for i_, a_ in enumerate(fe) for b_ in fe[i_ + 1:]))
            out['natural']['%d,%d' % (n, N)] = {k: dict(islands=v[0], efficient=v[1], incompatible_terminal=v[2]) for k, v in g.items()}
        if n == 12: SC._C.pop(12, None)
    json.dump(out, open(PATH, 'w'), indent=1)


def wilson_upper(k, n, z=1.96):
    if n == 0: return 1.0
    p = k / n; den = 1 + z * z / n
    return (p + z * z / (2 * n) + z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / den


def pair_summary():
    D = json.load(open(PAIRS)); P = D['pairs']
    res = []
    for pi, p in enumerate(P):
        rr = [r for r in D['rows'] if r['pair'] == pi]
        cell = {}
        for mode, starts in (('pair', ((200, 200), (300, 100), (100, 300))), ('bg', ((100, 100), (150, 50), (50, 150)))):
            for nx, ny in starts:
                L = [r for r in rr if r['mode'] == mode and r['nx'] == nx and r['ny'] == ny]
                f = Counter(r['fate'] for r in L)
                cell['%s %d:%d' % (mode, nx, ny)] = dict(runs=len(L), x=f['x'], y=f['y'], both=f['both'], neither=f['neither'],
                                                         unresolved=sum(r['status'] == 'unresolved' for r in L),
                                                         median_stop=float(np.median([r['stop_gen'] for r in L])) if L else None)
        tv = {}
        for a_, b_ in (('pair 200:200', 'bg 100:100'), ('pair 300:100', 'bg 150:50'), ('pair 100:300', 'bg 50:150')):
            A, B = cell[a_], cell[b_]
            if A['runs'] and B['runs']:
                tv[a_.split()[1]] = 0.5 * sum(abs(A[k] / A['runs'] - B[k] / B['runs']) for k in ('x', 'y', 'both', 'neither'))
        sk = [cell['pair 300:100'], cell['pair 100:300']]
        larger = (sk[0]['x'] + sk[1]['y']); smaller = (sk[0]['y'] + sk[1]['x']); nsk = sk[0]['runs'] + sk[1]['runs']
        res.append(dict(pair=pi, x=p['x'], y=p['y'], label=p['label'], type=p['type'], self=p['self'], vsD=p['vsD'], cells=cell, tv=tv,
                        larger_wins_3to1=larger / nsk if nsk else None, smaller_wins_3to1=smaller / nsk if nsk else None,
                        poly_pair=sum(cell[k]['both'] for k in cell if k.startswith('pair')) / max(1, sum(cell[k]['runs'] for k in cell if k.startswith('pair'))),
                        poly_bg=sum(cell[k]['both'] for k in cell if k.startswith('bg')) / max(1, sum(cell[k]['runs'] for k in cell if k.startswith('bg')))))
    return res


def lottery_summary():
    R = json.load(gzip.open(LOTT, 'rt'))
    out = {}
    for k in ('cond', 'dd', 'unc'):
        L = [r for r in R if r['kind'] == k]
        tries = sum(r['tries'] for r in L)
        cf = Counter(); dd = Counter(); byp = defaultdict(Counter)
        for r in L:
            for x in r['cons']:
                cf[x[4]] += 1; byp['%s | %s' % (x[0], x[1])][x[4]] += 1
            for x in r['dd']:
                dd[x[4]] += 1
        out[k] = dict(islands=len(L), draws=tries, accept=len(L) / tries, status=dict(Counter(r['status'] for r in L)),
                      efficient=sum(r['efficient'] for r in L), coop_fix=sum(r['coop_fix'] for r in L),
                      incompatible_terminal=sum(bool(r['inc_final']) for r in L),
                      islands_with_conseq=sum(bool(r['cons']) for r in L), conseq_fates=dict(cf),
                      islands_with_dd=sum(bool(r['dd']) for r in L), dd_fates=dict(dd),
                      islands_poly_conseq=sum(any(x[4] == 'both' for x in r['cons']) for r in L),
                      islands_poly_dd=sum(any(x[4] == 'both' for x in r['dd']) for r in L),
                      by_pair={p: dict(c) for p, c in sorted(byp.items(), key=lambda t: -sum(t[1].values()))},
                      unresolved=[(r['final'], r['pcc']) for r in L if not r['resolved']])
    return out


VERDICTS = '''
## Deviations from the predeclared design

- Pair competitions: the cap of 12 binds for anti-coordinators (many pairs co-seed at >= 0.01); it was applied per
  category (all 10 consequential establisher pairs; the 12 heaviest anti-coordinator pairs, plus the heaviest pair that
  both defect on D and the observed pair). No consequential pair is mutually defecting, so four mutually-defecting
  establisher pairs were added (the heaviest; PrudentBot with `BOX1(THEM(ME))` and with `BOX(THEM(^C))`; `BOX1(THEM(ME))`
  with P*, the pair of the two certified-separated runs). A second conditioned sample (400 islands conditioned on a
  mutually-defecting establisher pair) was added for prediction 4's polymorphism clause.
- Pair-competition horizon 2e4 generations (administrative; anti-coordinator polymorphisms never freeze and cost 5.7 s
  per run at 1e5). The lottery keeps 1e5.
- The 2x2 game inside every pair of one type is identical (exploitation, mutual defection, anti-coordination), so
  pair-only runs differ between pairs of a type only by random numbers.

## Unresolved incompatibility risk

- Co-seeding factor (n = 12, any incompatible establisher pair): 0.063 (N = 100), 0.26 (400), 0.70 (1600), 0.99 (6400).
  It tends to 1 along any N -> infinity path.
- Resolution-failure factor: of 3,814 single islands that co-seeded an incompatible establisher pair (2,918 natural
  spoiler islands at n = 6, 9, 12 and N = 100, 400; 896 lottery islands at n = 12, N = 400), none ended uncertified and
  none ended with an incompatible establisher pair in the terminal support: 0 / 3,814, rule-of-three 95% bound 7.9e-4.
  Efficiency is not lower when an incompatible pair is co-seeded (n = 12, N = 400: 0.204 exploitation-only, 0.269 with a
  DD pair, 0.180 compatible with 2+ establishers; conditioned lottery 84 / 400 against 68 / 400 unconditioned).
- Two-class argument: for two self-cooperating classes the diagonal is R = 0, so a stable interior rest point would need
  both off-diagonal payoffs above 0, i.e. both T, which is impossible. Establisher pairs are neutral (CC), bistable (DD)
  or dominated (exploitation); only self-defecting classes (anti-coordinators) can hold a stable two-class polymorphism.
- Bound: unresolved incompatibility risk per island <= P(co-seed) x 7.9e-4 <= 7.9e-4 at N <= 400, n <= 12. The
  resolution factor is measured only at N <= 400; uniformity in N rests on the two-class argument, not data.
- The only uncertified islands in all rows are anti-coordinator polymorphisms (no establisher present, P(C,C) ~ 0.5):
  1 / 4,800 seeds-in-n mN = 0 islands, 0 / 24,000 natural spoiler islands, 0 / 1,200 lottery islands, 8 / 525,000 forced
  spoiler islands.
- Metapopulation: mutually-defecting establishers can be held on different islands (2 / 100 runs at n = 9, (100, 256),
  `BOX1(THEM(ME))` against the P* family); every island is efficient, so this is a rival network across islands, not on
  one.

## Verdicts

1. **Held on its falsifier; the network clause holds only as written.** kappa = 0.977 / 0.958 / 0.951 (>= 0.9 at every
   n, falling with n). All establishers form one component at every n (vacuous, as the review said). Pairwise, the heavy
   set minus PrudentBot is *not* a compatible network: the two near-universal suckers `not(BOXD(THEM(^C)))`,
   `not(BOXD1(THEM(^C)))` (mu >= 1e-4) are exploited by every prover. PrudentBot (mu ~ 3e-6) mutually defects with both
   probe-readers as predicted, but also with `BOX1(THEM(ME))`, and it exploits `BOX1(THEM(THEM))`.
2. **Held.** DD pair mass / mu_est^2 = 0 / 0.0010 / 0.0017 (< 0.05). P(an island of N = 400 co-seeds an incompatible
   establisher pair) = 0.119 / 0.219 / 0.260 (in 0.1-0.4), rising with N (0.026-0.063 at N = 100; 0.70 at N = 1600 and
   0.99 at N = 6400, n = 12).
3. **Held, structurally.** In the PD, the certification rule (all present classes pairwise payoff-identical) forces an
   island to be all-CC or all-DD (T != S), so a certified island has P(C,C) in {0, 1}, P(C,C) < 0.95 coincides with
   Pareto-inefficiency, no certified cooperative island is below 0.95 and every certified island with 2+ establishers
   is mutually cooperating (0 incompatible out of 1,920 such islands with stored per-island support). The two
   certified-separated runs hold mutually-defecting establishers on different islands, each island efficient.
4. **Failed** (falsifier not triggered). Held: mutually-defecting establisher pairs are bistable (the larger class wins
   100% at 3:1 pair-only; 0 / 400 DD-conditioned islands polymorphic in a DD pair); anti-coordinators are polymorphic in
   100% of pair-only runs. Failed: anti-coordinator co-seeding at N = 400 is 0.89 / 0.92 / 0.93 for any pair and 0.024 /
   0.056 / 0.073 for pairs that both defect on D (the predicted bound was 0.02); the background changes the pair-only
   outcome by TV 0.19-0.34 for DD pairs at 1:1, up to 0.15 for exploitation pairs, and 0.6-1.0 for anti-coordinators
   (predicted < 0.2). Exploitation pairs, the only consequential ones, are a third pattern: the exploiter wins at every
   ratio.
'''


def report_main(a):
    S = json.load(open(STATIC)); RA = json.load(open(REAN)); PA = json.load(open(PATH))
    LS = lottery_summary(); PS = pair_summary()
    md = ['# Compatibility among co-seeded establishers (2026-10-05)', '',
          'Spec `specs/2026-10-05-compatibility.md`; predictions `predictions/2026-10-05-compatibility.md`; code `src/compatibility.py`.',
          'Modal arm, PD, w = 0.3, eps = 0. Class data: `spoiler_conditioned.cdata` (checked equal to modal.build at n = 6, 9).', '']
    md += ['## 1. Compatibility index', '',
           '| n | classes | establishers | mu_est | kappa | kappa (x != y) | mutual-defection rate | exploitation rate | components | DD pair mass / mu_est^2 |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for n in NS:
        r = S[str(n)]
        md.append('| %d | %d | %d | %.4f | %.4f | %.4f | %.4f | %.4f | %d | %.4f |' % (n, r['classes'], r['n_est'], r['mu_est'], r['kappa'], r['kappa_distinct'],
                                                                              r['dd_rate'], r['ex_rate'], r['n_components'], r['dd_pair_frac']))
    md += ['', 'Denominator: two iid draws from mu that are both establishers (mu_est^2); same-class draws count as mutual cooperation.',
           'Missing-edge mass within the single component, as a fraction of mu(C)^2/2: ' +
           ', '.join('n = %d: %.4f' % (n, S[str(n)]['components'][0]['missing_frac']) for n in NS), '']
    for n in NS:
        r = S[str(n)]
        md += ['### Heavy-set pairwise matrix, n = %d (row vs column; CC mutual cooperation, DD mutual defection, exploit one-sided)' % n, '']
        names = [h['name'] for h in r['heavy']]
        md.append('| | mu | ' + ' | '.join('%d' % (i + 1) for i in range(len(names))) + ' |')
        md.append('|---|---|' + '---|' * len(names))
        for i, (h, row) in enumerate(zip(r['heavy'], r['heavy_matrix'])):
            md.append('| %d `%s` | %.5f | ' % (i + 1, h['name'], h['mu']) + ' | '.join(row) + ' |')
        md.append('')
    md += ['## 2. Incompatible pairs and co-seeding', '',
           '| n | incompatible pairs (DD / exploit) | consequential (co-seed >= 0.01 at N = 400) | P(any incompatible) N = 100 | N = 400 | P(any DD) N = 400 | heavy set exact N = 400 | P(2+ establisher classes) N = 400 |',
           '|---|---|---|---|---|---|---|---|']
    for n in NS:
        r = S[str(n)]; c = r['coseed_any']
        md.append('| %d | %d (%d / %d) | %d | %.4f | %.4f | %.4f | %.4f | %.4f |' % (n, r['n_incompatible_pairs'], r['n_dd_pairs'], r['n_ex_pairs'], len(r['consequential']),
                                                                          c['100']['sim_all'], c['400']['sim_all'], c['400']['sim_dd'], c['400']['exact_heavy'], c['400']['sim_two_est']))
    md += ['', 'Consequential pairs (exploiter | exploited), n = 12:', '', '| exploiter | exploited | type | co-seed N = 100 | N = 400 |', '|---|---|---|---|---|']
    for p in S['12']['consequential']:
        md.append('| `%s` | `%s` | %s | %.4f | %.4f |' % (p['x'], p['y'], p['type'], p['co100'], p['co400']))
    md += ['', 'Heaviest mutually-defecting pairs, n = 12: ' + '; '.join('`%s` / `%s` %.4f' % (p['x'], p['y'], p['co400']) for p in [q for q in S['12']['incompatible_pairs'] if q['type'] == 'DD'][:6]), '']
    md += ['Along N (exact over the consequential classes and the heavy set; simulated over all establishers at n = 12):', '',
           '| n | N | exact, consequential pairs | exact, heavy set | simulated, all establishers |', '|---|---|---|---|---|']
    for n in NS:
        for N in NPATH:
            r = PA['coseed'][str(n)][str(N)]
            md.append('| %d | %d | %.4f | %.4f | %s |' % (n, N, r['exact_conseq'], r['exact_heavy'], '%.4f' % r['sim_all'] if 'sim_all' in r else ''))
    md += ['', '## 3. Anti-coordinators', '',
           '| n | pairs | classes involved | class mass | pair mass / mu^2 | pairs both defecting on D | P(any co-seeded) N = 400 | both defect on D | N = 100 both defect on D |',
           '|---|---|---|---|---|---|---|---|---|']
    for n in NS:
        r = S[str(n)]['anti']; c = r['coseed_any']
        md.append('| %d | %d | %d | %.4f | %.2e | %d | %.4f | %.4f | %.4f |' % (n, r['n_pairs'], r['n_classes'], r['class_mass'], r['pair_mass'], r['n_pairs_both_defect_D'],
                                                                     c['400']['all'], c['400']['both_defect_D'], c['100']['both_defect_D']))
    md += ['', 'Heaviest anti-coordinator pairs at n = 12: ' + '; '.join('`%s` / `%s` %.3f (one cooperates with D: %s)' % (p['x'], p['y'], p['co400'], bool(p['x_vs_D'] or p['y_vs_D'])) for p in S['12']['anti']['pairs'][:4]),
           'Observed pair (seeds-in-n n = 9, unresolved): ' + '; '.join('n = %d co-seed(400) %.4f' % (n, S[str(n)]['anti']['observed'][0]['co400']) for n in (9, 12) if S[str(n)]['anti']['observed']), '']
    md += ['## 4. Re-analysis of existing rows (certification rule alone; horizon 1e5 generations)', '',
           '| source | n | islands | certified | excluded | P(C,C) < 0.95 | Pareto-inefficient | strictly 0 < P(C,C) < 1 | frozen cooperative | of which P(C,C) < 0.95 | 2+ establishers | compatible | incompatible |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for k, r in RA.items():
        if not isinstance(r, dict) or 'source' not in r: continue
        md.append('| %s | %d | %d | %d | %d | %s | %s | %s | %d | %d | %d | %d | %d |' % (r['source'], r['n'], r['islands'], r['certified'], r['excluded'],
                  r.get('pcc_below_095', '-'), r.get('pareto_inefficient', '-'), r.get('pcc_strictly_between', '-'), r['frozen_coop'], r['frozen_coop_pcc_below_095'],
                  r['multi_est'], r['multi_est_compatible'], r['multi_est_incompatible']))
    md += ['', 'Uncertified islands and their terminal support:', '']
    for x in RA['forced_unresolved']:
        md.append('- forced spoiler n = %d pair %d rep %d %s: %s, P(C,C) %.3f, pair types %s, self-play %s, vs D %s' % (x['n'], x['pair'], x['rep'], x['key'], x['final'], x['pcc'], [t[2] for t in x['pairs']], x['self'], x['vsD']))
    md.append('- seeds-in-n n = 9 (400, 4) mN = 0 rep 94 island 2: {not(BOXD(THEM(THEM))): 211, BOX1(THEM(^BOX1(THEM(^D)))): 189} (anti-coordinators)')
    md += ['', 'Certified-separated runs (incompatible establishers held on different islands):', '']
    for x in RA['separated_runs']:
        md.append('- n = %d (%d, %d) rep %d: %s; pair types %s; island outcomes %s' % (x['n'], x['N'], x['I'], x['rep'], x['final'], [t[2] for t in x['pairs']], x['islands_out']))
    md += ['', 'Natural spoiler islands split by the seed (efficiency = P(C,C) >= 0.95):', '', '| n | N | seed | islands | efficient | share | incompatible terminal |', '|---|---|---|---|---|---|---|']
    for key, g in PA['natural'].items():
        n, N = key.split(',')
        for k in ('no establisher', 'one establisher', 'compatible, 2+ establishers', 'incompatible (exploitation only)', 'incompatible (some DD)'):
            if k in g:
                md.append('| %s | %s | %s | %d | %d | %.3f | %d |' % (n, N, k, g[k]['islands'], g[k]['efficient'], g[k]['efficient'] / g[k]['islands'], g[k]['incompatible_terminal']))
    md += ['', '## 5a. Conditioned lottery (n = 12, N = 400, single islands, horizon 1e5)', '',
           '| sample | islands | draws | acceptance | certified | efficient | islands with an incompatible terminal pair | consequential-pair fates (x / y / both / neither) | DD-pair fates (x / y / both / neither) | islands polymorphic in a DD pair |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for k, lab in (('cond', 'conditioned on a consequential pair'), ('dd', 'conditioned on a DD establisher pair (added)'), ('unc', 'unconditioned')):
        r = LS[k]; cf = r['conseq_fates']; df = r['dd_fates']
        md.append('| %s | %d | %d | %.4f | %d | %d | %d | %d / %d / %d / %d | %d / %d / %d / %d | %d |' % (lab, r['islands'], r['draws'], r['accept'], r['status'].get('local-frozen', 0), r['efficient'],
                  r['incompatible_terminal'], cf.get('x', 0), cf.get('y', 0), cf.get('both', 0), cf.get('neither', 0), df.get('x', 0), df.get('y', 0), df.get('both', 0), df.get('neither', 0), r['islands_poly_dd']))
    md += ['', 'Achieved counts by consequential pair (conditioned sample): ' + '; '.join('%s %d' % (p, sum(c.values())) for p, c in LS['cond']['by_pair'].items()), '']
    md += ['## 5b. Pair competitions (n = 12, N = 400, 100 runs per start, horizon %d generations)' % GENS_PAIR, '',
           '| # | x | y | type | self | vs D | pair 200:200 | 300:100 | 100:300 | bg 100:100 | 150:50 | 50:150 | larger wins at 3:1 | TV (1:1 / 3:1 / 1:3) |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    fmt = lambda c: '%d/%d/%d/%d' % (c['x'], c['y'], c['both'], c['neither'])
    for r in PS:
        c = r['cells']
        md.append('| %d | `%s` | `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %.2f | %s |' % (r['pair'], r['x'], r['y'], r['type'], r['self'], r['vsD'],
                  fmt(c['pair 200:200']), fmt(c['pair 300:100']), fmt(c['pair 100:300']), fmt(c['bg 100:100']), fmt(c['bg 150:50']), fmt(c['bg 50:150']),
                  r['larger_wins_3to1'], ' / '.join('%.2f' % r['tv'][k] for k in ('200:200', '300:100', '100:300'))))
    md += ['', 'Cells are x only / y only / both / neither. For exploitation pairs x is the exploiter.', '']
    md += VERDICTS.strip('\n').split('\n') + ['']
    open(os.path.join(RUNS, 'compatibility.md'), 'w').write('\n'.join(md) + '\n')
    js = dict(static={n: dict({k: v for k, v in S[n].items() if k != 'incompatible_pairs'}, incompatible_pairs_top=S[n]['incompatible_pairs'][:40]) for n in S},
              reanalysis=RA, path=PA, lottery=LS, pairs=PS)
    json.dump(js, open(os.path.join(RUNS, 'compatibility.json'), 'w'), indent=1)
    print('\n'.join(md))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['check', 'static', 'reanalyze', 'lottery', 'pairs', 'path', 'report'])
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--n', type=int, nargs='*', default=None)
    ap.add_argument('--time', action='store_true')
    a = ap.parse_args()
    {'check': check_main, 'static': static_main, 'reanalyze': reanalyze_main, 'lottery': lottery_main, 'pairs': pairs_main, 'path': path_main, 'report': report_main}[a.what](a)
