"""Mixed-budget populations under K: do budget soft cliques become bridge-less rivals when budgets vary?
Spec specs/2026-10-05-mixed-budgets.md (reviewed, reviews/2026-10-05-mixed-budgets-gpt-6.1-sol.md);
predictions predictions/2026-10-05-mixed-budgets.md.

Finite-horizon incidence at n = 8 (N = 200, I = 64, horizon 1e5), not large-population universality.

    python3 src/mixed_budgets.py cross            # missing cross-budget blocks (4, 8), (8, 16) (src/k_at_n8._cross8)
"""
import argparse, gzip, json, math, os, sys, time, zlib
from collections import Counter, defaultdict, deque
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
KDIR = os.path.join(RUNS, 'k-at-n8')
B = (4, 8, 16)
W = 0.3
PDP = np.array([[-1.0, 1.0], [-2.0, 0.0]])       # pay[a][b], level order (D, C)
FB, FB1 = 'BOX(THEM(ME))', 'BOX1(THEM(ME))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
CORE = [FB, FB1, 'BOX(THEM(THEM))', 'BOX1(THEM(THEM))', 'BOX(THEM(^C))', 'BOX1(THEM(^C))', PB]
PRIORS = {'uniform': (1 / 3, 1 / 3, 1 / 3), 'cheap': (0.6, 0.3, 0.1), 'above': (0.0, 0.5, 0.5),
          'h4': (1.0, 0.0, 0.0), 'h8': (0.0, 1.0, 0.0), 'h16': (0.0, 0.0, 1.0)}
PRLAB = {'uniform': 'uniform', 'cheap': 'cheap-heavy', 'above': 'above-threshold', 'h4': 'homogeneous b = 4',
         'h8': 'homogeneous b = 8', 'h16': 'homogeneous b = 16'}
NSEED = 200
STATIC = os.path.join(RUNS, 'mixed-budgets-static.json')


def cmd_cross(a):
    import k_at_n8 as K8
    jobs = []
    for i in range(len(B)):
        for k in range(i + 1, len(B)):
            bx, by = B[i], B[k]
            if not (os.path.exists(os.path.join(KDIR, 'kcross_n8_%d_%d.npy' % (bx, by))) and
                    os.path.exists(os.path.join(KDIR, 'kcross_n8_%d_%d.npy' % (by, bx)))):
                jobs.append((bx, by))
    print('cross jobs', jobs, flush=True)
    meta = {}
    mp = os.path.join(KDIR, 'kcross_meta_mixed.json')
    if os.path.exists(mp):
        meta = json.load(open(mp))
    with Pool(max(1, min(a.procs, len(jobs) or 1))) as pool:
        for bx, by, nchk, nbad, dt in pool.imap_unordered(K8._cross8, jobs):
            meta['%d_%d' % (bx, by)] = dict(sound_checked=nchk, sound_bad=nbad, t=dt)
            json.dump(meta, open(mp, 'w'), indent=1)
            print('(%d, %d) sound bad %d / %d, %.0fs' % (bx, by, nbad, nchk, dt), flush=True)


# ------------------------------------------------------------------ the budgeted catalogue
_CAT = {}


def catalogue(Bs=B):
    """Genotypes (source, budget): C and D unbudgeted (budget 0), every other canonical source of L_8 at each budget
    in Bs; plays from the K tables (same budget) and the cross-budget blocks (k_at_n8.catalogue_val8).  Behavioural
    classes: genotypes with identical directed rows and columns (prior-independent; masses per prior)."""
    Bs = tuple(Bs)
    if Bs in _CAT:
        return _CAT[Bs]
    import k_at_n8 as K8
    val, base, gb, L = K8.catalogue_val8(list(Bs))
    G = len(base)
    srcname = [L.rep[c] for c in base]
    gname = [s if b == 0 else '%s@%d' % (s, b) for s, b in zip(srcname, gb)]
    sig = defaultdict(list)
    for g in range(G):
        sig[(val[g].tobytes(), val[:, g].tobytes())].append(g)
    raw_src = L.mu_canon                       # raw shell masses of canonical sources

    def gm(g):
        return raw_src[base[g]] * (1.0 if gb[g] == 0 else 1.0 / len(Bs))
    groups = list(sig.values())
    groups.sort(key=lambda mem: (-sum(gm(g) for g in mem), min(mem)))
    reps = [min(mem, key=lambda g: (L.bits_canon[base[g]], gb[g], base[g])) for mem in groups]
    idx = np.array(reps, np.int64)
    V = np.ascontiguousarray(val[np.ix_(idx, idx)]).astype(np.uint8)
    K = len(reps)
    cls_of = np.full(G, -1, np.int64)
    for j, mem in enumerate(groups):
        cls_of[np.array(mem)] = j
    names = [gname[r] for r in reps]
    selfc = np.diagonal(V).astype(bool).copy()
    gidx = {x: i for i, x in enumerate(gname)}
    iC = int(cls_of[gidx['C']]); iD = int(cls_of[gidx['D']])
    allc_row = V.all(1).astype(bool)
    allc_k = np.zeros(K, bool); allc_k[iC] = True
    vD = V[:, iD].astype(bool)
    bidx = np.array([0 if b == 0 else 1 + list(Bs).index(b) for b in gb], np.int64)   # 0 = unbudgeted
    d = dict(Bs=Bs, G=G, val=val, base=base, gb=gb, bidx=bidx, gname=gname, srcname=srcname, raw_src=raw_src,
             V=V, K=K, names=names, members=groups, reps=idx, cls_of=cls_of, gidx=gidx, iC=iC, iD=iD, selfc=selfc,
             allc_row=allc_row, coop_s=selfc & ~allc_row, est_s=selfc & ~vD & ~allc_row,
             coop=selfc & ~allc_k, est=selfc & ~vD & ~allc_k, L=L)
    _CAT[Bs] = d
    return d


def gmass(d, prior, raw=False):
    """Genotype masses under a budget prior (a tuple over d['Bs']); cut-normalized unless raw."""
    pr = np.array([1.0] + list(prior))
    m = d['raw_src'][d['base']] * pr[d['bidx']]
    return m if raw else m / m.sum()


def cmass(d, prior, raw=False):
    m = np.zeros(d['K']); np.add.at(m, d['cls_of'], gmass(d, prior, raw))
    return m


def gcls(d, name):
    return int(d['cls_of'][d['gidx'][name]])


def budgets_of(d, k, prior=None):
    """Budget split of class k's members (by uniform mass, or by the prior's mass); 0 = unbudgeted."""
    gm = gmass(d, prior if prior is not None else (1.0,) * len(d['Bs']), raw=True)
    out = Counter()
    for g in d['members'][k]:
        out[int(d['gb'][g])] += gm[g]
    t = sum(out.values())
    return {str(b): round(v / t, 4) for b, v in sorted(out.items())} if t > 0 else {}


def same_source_pair(d, x, y):
    sx = {int(d['base'][g]) for g in d['members'][x] if d['gb'][g] > 0}
    sy = {int(d['base'][g]) for g in d['members'][y] if d['gb'][g] > 0}
    return sorted(d['L'].rep[c] for c in sx & sy)


def bfs_dist(adj, s):
    dist = -np.ones(adj.shape[0], np.int64); dist[s] = 0; dq = deque([s])
    while dq:
        u = dq.popleft()
        for v in np.nonzero(adj[u] & (dist < 0))[0]:
            dist[v] = dist[u] + 1; dq.append(v)
    return dist


def components(adj):
    n = adj.shape[0]; comp = -np.ones(n, np.int64); c = 0
    for s in range(n):
        if comp[s] >= 0: continue
        comp[s] = c; st = [s]
        while st:
            u = st.pop()
            for v in np.nonzero(adj[u] & (comp < 0))[0]:
                comp[v] = c; st.append(v)
        c += 1
    return comp, c


def coseed(mx, my, N=NSEED):
    """P(both classes present on one island of N iid draws)."""
    return float(1 - (1 - mx) ** N - (1 - my) ** N + (1 - mx - my) ** N)


def pair_row(d, x, y, mu, raw, pos, MC, est, dist=None, comp=None):
    coop = d['coop_s']
    br_s = coop & MC[x] & MC[y]; br_s[[x, y]] = False
    br = br_s & pos
    return dict(x=int(x), y=int(y), a=d['names'][x], b=d['names'][y], mu_x=float(mu[x]), mu_y=float(mu[y]),
                pair_mu=float(mu[x] * mu[y]), pair_raw=float(raw[x] * raw[y]), coseed=coseed(mu[x], mu[y]),
                n_bridges=int(br.sum()), bridge_mu=float(mu[br].sum()), n_bridges_struct=int(br_s.sum()),
                n_bridges_est=int((br & est).sum()),
                bridges_top=[(d['names'][k], float(mu[k])) for k in sorted(np.nonzero(br)[0], key=lambda k: -mu[k])[:3]],
                path=dist, same_comp=comp, budget_copies=same_source_pair(d, x, y),
                members_x=len(d['members'][x]), members_y=len(d['members'][y]))


def screen(d, prior, top=40):
    """Incompatible pairs of budgeted establishers (classes of positive mass under the prior), with exhaustive
    pairwise-bridge enumeration (bridges: cooperative classes of positive mass under the prior; structural: any
    cooperative class of the catalogue), mediator paths (length <= 3 in the establisher mutual-cooperation graph of the
    prior's support), components, budget copies of one source."""
    V = d['V'].astype(bool)
    mu = cmass(d, prior); raw = cmass(d, prior, raw=True)
    pos = mu > 0
    est = d['est_s']
    MC = V & V.T
    MD = ~V & ~V.T
    E = np.nonzero(est & pos)[0]
    adjE = MC[np.ix_(E, E)].copy(); np.fill_diagonal(adjE, False)
    comp, nc = components(adjE)
    pairs = []
    for a in range(len(E)):
        x = E[a]
        da = bfs_dist(adjE, a)
        for b in range(a + 1, len(E)):
            y = E[b]
            if MD[x, y]:
                r = pair_row(d, x, y, mu, raw, pos, MC, est, int(da[b]) if da[b] >= 0 else None, bool(comp[a] == comp[b]))
                r['budgets_x'] = budgets_of(d, x, prior); r['budgets_y'] = budgets_of(d, y, prior)
                pairs.append(r)
    pairs.sort(key=lambda r: -r['pair_mu'])

    def agg(sel):
        rs = [r for r in pairs if sel(r)]
        return dict(n=len(rs), mu=float(sum(r['pair_mu'] for r in rs)), raw=float(sum(r['pair_raw'] for r in rs)),
                    coseed=float(sum(r['coseed'] for r in rs)),
                    coseed_max=float(max([r['coseed'] for r in rs], default=0.0)))
    out = dict(prior=list(prior), K_pos=int(pos.sum()), est_n=int(len(E)), est_mu=float(mu[E].sum()),
               est_raw=float(raw[E].sum()), components=int(nc),
               comp_sizes=[int(s) for _, s in Counter(comp.tolist()).most_common(8)],
               comp_mu=sorted([float(mu[E[comp == c]].sum()) for c in range(nc)], reverse=True)[:8],
               incompatible=agg(lambda r: True),
               bridged=agg(lambda r: r['n_bridges'] > 0),
               direct_bridgeless=agg(lambda r: r['n_bridges'] == 0),
               direct_bridgeless_struct=agg(lambda r: r['n_bridges_struct'] == 0),
               no_path3=agg(lambda r: r['path'] is None or r['path'] > 3),
               disconnected=agg(lambda r: not r['same_comp']),
               budget_copy=agg(lambda r: bool(r['budget_copies'])),
               budget_copy_bridgeless=agg(lambda r: bool(r['budget_copies']) and r['n_bridges'] == 0),
               b14_bridgeless=agg(lambda r: r['n_bridges'] == 0 and has_b1_4([r['a'], r['b']])),
               core_bridgeless=agg(lambda r: r['n_bridges'] == 0 and any(x.rsplit('@', 1)[0] in (FB, FB1) for x in (r['a'], r['b']))),
               path_hist=dict(Counter(str(r['path']) for r in pairs)),
               n_pairs=len(pairs))
    out['pairs_top'] = pairs[:top]
    out['pairs_bridgeless'] = [r for r in pairs if r['n_bridges'] == 0][:top]
    out['pairs_bridged'] = [r for r in pairs if r['n_bridges'] > 0][:top]
    # core programs: do their budget copies share a component?
    core = {}
    posE = {int(x): i for i, x in enumerate(E)}
    bs = [str(b) for b in d['Bs']]
    for s in CORE:
        row = {}
        for b in d['Bs']:
            k = gcls(d, '%s@%d' % (s, b))
            row[str(b)] = dict(cls=d['names'][k], est=bool(est[k]), selfc=bool(d['selfc'][k]), present=bool(pos[k]),
                               comp=int(comp[posE[k]]) if k in posE else None)
        cps = {b: row[b]['comp'] for b in bs}
        row['share'] = {'%s-%s' % (u, v): bool(cps[u] is not None and cps[u] == cps[v]) for i, u in enumerate(bs) for v in bs[i + 1:]}
        core[s] = row
    out['core'] = core
    return out


def a16_rivals(d, prior):
    """Secondary statistic: rivals of A16 = {FairBot@16, BOX1(THEM(ME))@16} (establishers of positive mass mutually
    defecting with either member), with direct bridges (cooperative classes of positive mass mutually cooperating with
    both members and the rival)."""
    V = d['V'].astype(bool); mu = cmass(d, prior); pos = mu > 0
    a0, a1 = gcls(d, FB + '@16'), gcls(d, FB1 + '@16')
    MC = V & V.T; MD = ~V & ~V.T
    riv = d['est_s'] & pos & (MD[a0] | MD[a1])
    rows = []
    for r in np.nonzero(riv)[0]:
        br = d['coop_s'] & pos & MC[a0] & MC[a1] & MC[r]; br[[a0, a1, r]] = False
        rows.append(dict(name=d['names'][r], mu=float(mu[r]), full=bool(MD[a0, r] and MD[a1, r]), n_bridges=int(br.sum()),
                         bridge_mu=float(mu[br].sum()), budgets=budgets_of(d, r, prior)))
    rows.sort(key=lambda x: -x['mu'])
    tot = sum(x['mu'] for x in rows); bl = sum(x['mu'] for x in rows if x['n_bridges'] == 0)
    return dict(n=len(rows), mu=tot, bridgeless_mu=bl, bridgeless_share=bl / tot if tot else None, rows=rows[:20],
                A16_mutual=bool(MC[a0, a1]))


def lumping_check(d, priors, seed=7):
    """(i) identical directed rows and columns within each class (exhaustive); (ii) masses preserved per prior;
    (iii) seed law: genotype-level draws lumped versus class-level draws (first moments); (iv) establisher,
    incompatibility and bridge tests at genotype level agree with the class tests on every genotype pair."""
    val = d['val'].astype(bool); G = d['G']
    bad = 0
    for k, mem in enumerate(d['members']):
        r0 = d['reps'][k]
        for g in mem:
            if not (np.array_equal(val[g], val[r0]) and np.array_equal(val[:, g], val[:, r0])):
                bad += 1
    out = dict(members_bad=bad, n_genotypes=G, n_classes=d['K'], mass_err={}, seed_z={})
    rng = np.random.default_rng(seed)
    for p, pr in priors.items():
        gm = gmass(d, pr); agg = np.zeros(d['K']); np.add.at(agg, d['cls_of'], gm)
        out['mass_err'][p] = float(np.abs(agg - cmass(d, pr)).max())
        a = np.zeros(d['K']); b = np.zeros(d['K'])
        for _ in range(500):
            x = rng.multinomial(NSEED, gm); y = np.zeros(d['K']); np.add.at(y, d['cls_of'], x); a += y
            b += rng.multinomial(NSEED, agg)
        out['seed_z'][p] = float(np.max(np.abs(a - b) / np.sqrt(np.maximum(a + b, 1))))
    selfc = np.diagonal(val).copy(); allc = val.all(1)
    iDg = d['gidx']['D']
    coop = selfc & ~allc; est = coop & ~val[:, iDg]
    co = d['cls_of']
    mism = Counter()
    mism['est'] = int((est != d['est_s'][co]).sum())
    MCg = val & val.T; MDg = ~val & ~val.T
    Vc = d['V'].astype(bool)
    MDc = ~Vc & ~Vc.T; MCc = Vc & Vc.T
    E = np.nonzero(est)[0]
    npair = 0
    for i, x in enumerate(E):
        for y in E[i + 1:]:
            if MDg[x, y] != MDc[co[x], co[y]]:
                mism['incompatible'] += 1
            if MDg[x, y]:
                npair += 1
                brg = coop & MCg[x] & MCg[y] & ~np.isin(co, [co[x], co[y]])
                brc = d['coop_s'] & MCc[co[x]] & MCc[co[y]]; brc[[co[x], co[y]]] = False
                if not np.array_equal(np.unique(co[brg]), np.nonzero(brc)[0]):
                    mism['bridge'] += 1
    out['genotype_incompatible_pairs'] = npair
    out['mismatches'] = {k: int(v) for k, v in mism.items()}
    out['ok'] = bool(bad == 0 and max(out['mass_err'].values()) < 1e-12 and sum(mism.values()) == 0)
    return out


def named_checks(d):
    """The budget-grid facts on the catalogue (row plays first): FairBot, BOX1(THEM(ME)), PrudentBot."""
    out = {}
    V = d['V']
    for s1, s2 in ((FB, FB), (FB1, FB1), (FB, FB1), (PB, PB), (PB, FB), ('BOX(THEM(THEM))', FB1), ('BOX1(THEM(THEM))', FB1)):
        for bx in d['Bs']:
            for by in d['Bs']:
                x = gcls(d, '%s@%d' % (s1, bx)); y = gcls(d, '%s@%d' % (s2, by))
                out['%s@%d vs %s@%d' % (s1, bx, s2, by)] = '%s%s' % ('DC'[V[x, y]], 'DC'[V[y, x]])
    return out


def static_main(a):
    t0 = time.time()
    Bs = tuple(a.budgets)
    d = catalogue(Bs)
    print('catalogue %s: %d genotypes, %d classes (%.0fs)' % (Bs, d['G'], d['K'], time.time() - t0), flush=True)
    res = dict(Bs=list(Bs), G=d['G'], K=d['K'])
    meta = {}
    for b in Bs:
        m = json.load(open(os.path.join(KDIR, 'kmeta_n8_b%d.json' % b)))
        meta['%d' % b] = dict(sound_checked=m['sound_checked'], sound_bad=m['sound_bad'])
    mp = os.path.join(KDIR, 'kcross_meta_mixed.json')
    meta.update(json.load(open(mp)) if os.path.exists(mp) else {})
    meta.setdefault('4_16', dict(sound_checked=37893, sound_bad=0, note='K at n = 8, catalogue8.log'))
    res['soundness'] = meta
    pri = dict(PRIORS) if len(Bs) == 3 else {'uniform': tuple(1 / len(Bs) for _ in Bs)}
    res['lumping'] = lumping_check(d, pri)
    print('lumping', res['lumping'], flush=True)
    res['named'] = named_checks(d)
    res['classes'] = {}
    for p, pr in pri.items():
        mu = cmass(d, pr); pos = mu > 0; gm = gmass(d, pr)
        E = np.nonzero(d['est_s'] & pos)[0]
        res['classes'][p] = dict(K_pos=int(pos.sum()), est_n=int(len(E)), est_mu=float(mu[E].sum()),
                                 est_raw=float(cmass(d, pr, raw=True)[E].sum()),
                                 est_budget_mu={str(b): float(sum(gm[g] for k in E for g in d['members'][k] if d['gb'][g] == b)) for b in Bs},
                                 top=[(d['names'][k], float(mu[k]), bool(d['est_s'][k]), budgets_of(d, k, pr)) for k in np.argsort(-mu)[:25]])
    res['screen'] = {}; res['a16'] = {}
    for p, pr in pri.items():
        s = screen(d, pr)
        res['screen'][p] = s
        if 16 in Bs:
            res['a16'][p] = a16_rivals(d, pr)
        print('[%s] est %d (mu %.4f), comps %d %s; incompatible %d mu %.3g; bridged %d; direct-bridge-less %d mu %.3g '
              '(coseed sum %.3g); no path<=3 %d mu %.3g; disconnected %d; budget copies %d (bridge-less %d)' % (
                  p, s['est_n'], s['est_mu'], s['components'], s['comp_sizes'], s['incompatible']['n'], s['incompatible']['mu'],
                  s['bridged']['n'], s['direct_bridgeless']['n'], s['direct_bridgeless']['mu'], s['direct_bridgeless']['coseed'],
                  s['no_path3']['n'], s['no_path3']['mu'], s['disconnected']['n'], s['budget_copy']['n'],
                  s['budget_copy_bridgeless']['n']), flush=True)
    res['t'] = time.time() - t0
    path = STATIC if len(Bs) == 3 else os.path.join(RUNS, 'mixed-budgets', 'static-%s.json' % '-'.join(map(str, Bs)))
    json.dump(res, open(path, 'w'), indent=1, default=str)
    print('saved', path, '%.0fs' % (time.time() - t0))


# ------------------------------------------------------------------ kernel (copy of rival_islands._kern, see _kern_mb)
from numba import njit
import almost_all_seeds as AS
from rival_islands import _repay, _setact, _isactive, LUMPMAX


@njit(cache=True)
def _kern_mb(U, PCC, coopmask, tag, init, comp0, N, w, m, seed, checks, lump, iD, r1, r2, preest):
    """rival_islands._kern (single-migrant, kprop = 1) plus the expected budget composition of every (island, class)
    (comp[i, k, :], the exact conditional expectation given the lumped path: genotypes are exchangeable within a
    static class and within a dynamic lump) and a snapshot of holders and their composition at the first check
    after every island is established.  Same law as _kern; the stream differs only by the removed kprop branch
    (never taken at kprop = 1)."""
    np.random.seed(seed)
    I, K = init.shape
    counts = init.copy(); loc = init.copy()
    comp = comp0.copy(); NBm = comp0.shape[2]
    snap_gen = -1; snap_hold = -np.ones(I, np.int64); snap_cert = np.zeros(I, np.int64); snap_comp = np.zeros((I, NBm))
    bigs = np.zeros(I, np.int64); certs = np.zeros(I, np.int64)
    locsum = np.zeros(I, np.int64)
    paysum = np.zeros((I, K))
    pres = np.zeros((I, K), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, K), np.int64)
    glob = np.zeros(K, np.int64)
    for i in range(I):
        for k in range(K):
            if counts[i, k] > 0:
                pres[i, npres[i]] = k; pos[i, k] = npres[i]; npres[i] += 1
                glob[k] += counts[i, k]; locsum[i] += counts[i, k]
        _repay(i, counts, paysum, U, pres, npres)
    gtag = np.zeros(4, np.int64)
    for k in range(K): gtag[tag[k]] += glob[k]
    t_ext = -np.ones(4)
    for t in range(4):
        if gtag[t] == 0: t_ext[t] = 0.0
    parent = np.arange(K)
    est = np.zeros(I, np.int64)
    # per-island records
    t_est = -np.ones(I, np.int64); e_arr = np.zeros(I, np.int64); e_arrC = np.zeros(I, np.int64); e_arrD = np.zeros(I, np.int64)
    e_imm = -np.ones(I); e_hold = -np.ones(I, np.int64); e_hloc = -np.ones(I)
    t90 = -np.ones(I, np.int64); a90 = np.zeros(I, np.int64); imm90 = -np.ones(I); h90 = -np.ones(I, np.int64); hl90 = -np.ones(I)
    arr = np.zeros(I, np.int64); arrC = np.zeros(I, np.int64); arrD = np.zeros(I, np.int64); arr_all = np.zeros(I, np.int64)
    strong = np.zeros(I, np.int64)
    nloss = 0; loss_log = np.zeros((2000, 4), np.int64)       # gen, island, holder before (last strong check), holder after
    lasthold = -np.ones(I, np.int64)
    nchk = len(checks)
    trace = np.zeros((nchk, 14))
    # strong-holder transitions (class with >= 0.9 of an island; additions for island_path, no effect on dynamics)
    shold = -np.ones(I, np.int64); ntr = 0; tr_log = np.zeros((50000, 4), np.int64)   # gen, island, old cls, new cls
    mig_ct = np.zeros((4, 5), np.int64)        # migrant individuals by (child tag, recipient strong-holder tag; 4 = none)
    prem = np.zeros(K, np.int64); pvic = np.zeros(K, np.int64); pch = np.zeros(K, np.int64)
    first_sep = -1; sep_a = -1; sep_b = -1; nsepchk = 0
    held_zero = -np.ones(4, np.int64)
    act = np.arange(I); apos = np.arange(I); nact = 0
    for i in range(I):
        if preest[i] == 1:
            est[i] = 1; t_est[i] = 0
            h = pres[i, 0]
            e_hold[i] = h; e_hloc[i] = 1.0; e_imm[i] = 0.0; t90[i] = 0; h90[i] = h; hl90[i] = 1.0; imm90[i] = 0.0
        if _isactive(i, npres, est, locsum, N):
            nact = _setact(i, True, act, apos, nact)
        for t in range(npres[i]):
            if 10 * counts[i, pres[i, t]] >= 9 * N: shold[i] = pres[i, t]
    IN = I * N
    total = checks[nchk - 1] * IN
    mm = m if I > 1 else 0.0
    b = 0
    ci = 0
    nextchk = checks[0] * IN
    status = 0; stop_gen = checks[nchk - 1]
    lastP = -1
    while True:
        pa = (nact + (I - nact) * mm) / I
        if pa <= 0.0:
            G = total + 1
        elif pa >= 1.0:
            G = 0
        else:
            uu = np.random.random()
            G = int(np.log(1.0 - uu) / np.log(1.0 - pa))
        if b + G >= nextchk:
            b = nextchk
            g = checks[ci]
            # ---------------- check
            ncert = 0; cc_tot = 0.0
            held = np.zeros(4, np.int64); heldc = np.zeros(4, np.int64)
            hl = np.zeros(I, np.int64); nh = 0
            for i in range(I):
                co = 0; allco = True; big = pres[i, 0]
                for t in range(npres[i]):
                    k = pres[i, t]
                    if coopmask[k]: co += counts[i, k]
                    else: allco = False
                    if counts[i, k] > counts[i, big]: big = k
                lo = 1e300; hi = -1e300
                for t in range(npres[i]):
                    a = pres[i, t]
                    for t2 in range(npres[i]):
                        q = pres[i, t2]
                        if U[a, q] < lo: lo = U[a, q]
                        if U[a, q] > hi: hi = U[a, q]
                fz = hi - lo < 1e-12
                cert = fz and allco
                held[tag[big]] += 1
                bigs[i] = big; certs[i] = 1 if cert else 0
                if cert:
                    ncert += 1; heldc[tag[big]] += 1
                    new = True
                    for u in range(nh):
                        if hl[u] == big: new = False; break
                    if new:
                        hl[nh] = big; nh += 1
                cc, pay = AS._island_cc(counts, PCC, U, pres, npres, paysum, i, N)
                cc_tot += cc
                if t90[i] < 0 and 10 * co >= 9 * N:
                    hb = -1
                    for t in range(npres[i]):
                        k = pres[i, t]
                        if coopmask[k] and (hb < 0 or counts[i, k] > counts[i, hb]): hb = k
                    t90[i] = g; a90[i] = arr[i]; imm90[i] = 1.0 - locsum[i] / N; h90[i] = hb; hl90[i] = loc[i, hb] / counts[i, hb]
                if cert and est[i] == 0:
                    est[i] = 1; t_est[i] = g; e_arr[i] = arr[i]; e_arrC[i] = arrC[i]; e_arrD[i] = arrD[i]
                    e_imm[i] = 1.0 - locsum[i] / N; e_hold[i] = big; e_hloc[i] = loc[i, big] / counts[i, big]
                    nact = _setact(i, _isactive(i, npres, est, locsum, N), act, apos, nact)
                if strong[i] == 1 and 2 * co < N:
                    if nloss < 2000:
                        loss_log[nloss, 0] = g; loss_log[nloss, 1] = i; loss_log[nloss, 2] = lasthold[i]; loss_log[nloss, 3] = big
                    nloss += 1
                if 10 * co >= 9 * N:
                    strong[i] = 1; lasthold[i] = big
                elif 2 * co < N:
                    strong[i] = 0
            if snap_gen < 0:
                ne = 0
                for i in range(I): ne += est[i]
                if ne == I:
                    snap_gen = g
                    for i in range(I):
                        snap_hold[i] = bigs[i]; snap_cert[i] = 1 if 10 * counts[i, bigs[i]] >= 9 * N else 0
                        for z_ in range(NBm): snap_comp[i, z_] = comp[i, bigs[i], z_]
            sepf = 0
            for u in range(nh):
                for v in range(u + 1, nh):
                    a = hl[u]; q = hl[v]
                    if U[a, q] < -0.5 and U[q, a] < -0.5 and U[a, q] > -1.5 and U[q, a] > -1.5:
                        sepf = 1
                        if first_sep < 0:
                            first_sep = g; sep_a = a; sep_b = q
            nsepchk += sepf
            for t in range(1, 4):
                if held[t] == 0 and held_zero[t] < 0: held_zero[t] = g
            nP = 0
            for k in range(K):
                if glob[k] > 0: nP += 1
            trace[ci, 0] = g; trace[ci, 1] = gtag[1]; trace[ci, 2] = gtag[2]; trace[ci, 3] = held[1]; trace[ci, 4] = held[2]
            trace[ci, 5] = heldc[1]; trace[ci, 6] = heldc[2]; trace[ci, 7] = ncert; trace[ci, 8] = sepf; trace[ci, 9] = cc_tot / I
            trace[ci, 10] = nact; trace[ci, 11] = nP; trace[ci, 12] = held[3]; trace[ci, 13] = heldc[3]
            for i in range(I):
                for t in range(npres[i]):
                    k = pres[i, t]
                    if 10 * counts[i, k] >= 9 * N and shold[i] != k:
                        if ntr < 50000:
                            tr_log[ntr, 0] = g; tr_log[ntr, 1] = i; tr_log[ntr, 2] = shold[i]; tr_log[ntr, 3] = k
                        ntr += 1
                        shold[i] = k
            ci += 1
            # ---------------- stopping
            if mm > 0.0:
                Pl = np.zeros(nP, np.int64); z = 0
                for k in range(K):
                    if glob[k] > 0:
                        Pl[z] = k; z += 1
                lo = 1e300; hi = -1e300
                for x in range(nP):
                    a = Pl[x]
                    for y in range(nP):
                        q = Pl[y]
                        if U[a, q] < lo: lo = U[a, q]
                        if U[a, q] > hi: hi = U[a, q]
                    if hi - lo >= 1e-12: break
                if hi - lo < 1e-12:
                    status = 1; stop_gen = g; break
            else:
                allf = True
                for i in range(I):
                    lo = 1e300; hi = -1e300
                    for t in range(npres[i]):
                        a = pres[i, t]
                        for t2 in range(npres[i]):
                            q = pres[i, t2]
                            if U[a, q] < lo: lo = U[a, q]
                            if U[a, q] > hi: hi = U[a, q]
                    if hi - lo >= 1e-12:
                        allf = False; break
                if allf:
                    status = 5; stop_gen = g; break
            if ci >= nchk:
                break
            nextchk = checks[ci] * IN
            # ---------------- lumping
            if lump and nP <= LUMPMAX and nP != lastP:
                P = np.zeros(nP, np.int64); h = np.zeros(nP); z = 0
                for k in range(K):
                    if glob[k] > 0:
                        P[z] = k; z += 1
                for z in range(nP):
                    a = P[z]; v = 0.0
                    for z2 in range(nP):
                        q = P[z2]
                        v += U[a, q] * r1[q] + U[q, a] * r2[q]
                    h[z] = v + 1000.0 * tag[a] + 10000.0 * coopmask[a]
                order = np.argsort(h)
                for x in range(nP):
                    a = P[order[x]]
                    if glob[a] == 0: continue
                    y = x + 1
                    while y < nP and abs(h[order[y]] - h[order[x]]) < 1e-9:
                        q = P[order[y]]
                        y += 1
                        if glob[q] == 0: continue
                        if tag[a] != tag[q] or coopmask[a] != coopmask[q]: continue
                        same = True
                        for z in range(nP):
                            c = P[z]
                            if glob[c] == 0: continue
                            if U[a, c] != U[q, c] or U[c, a] != U[c, q]:
                                same = False; break
                        if not same: continue
                        # merge q into a
                        parent[q] = a
                        for i in range(I):
                            if counts[i, q] == 0: continue
                            if counts[i, a] == 0:
                                pres[i, npres[i]] = a; pos[i, a] = npres[i]; npres[i] += 1
                            ca = counts[i, a]; cq = counts[i, q]
                            for z_ in range(NBm): comp[i, a, z_] = (ca * comp[i, a, z_] + cq * comp[i, q, z_]) / (ca + cq)
                            counts[i, a] += counts[i, q]; loc[i, a] += loc[i, q]; counts[i, q] = 0; loc[i, q] = 0
                            p = pos[i, q]; last = pres[i, npres[i] - 1]
                            pres[i, p] = last; pos[i, last] = p; pos[i, q] = -1; npres[i] -= 1
                            _repay(i, counts, paysum, U, pres, npres)
                            if lasthold[i] == q: lasthold[i] = a
                            if shold[i] == q: shold[i] = a
                            nact = _setact(i, _isactive(i, npres, est, locsum, N), act, apos, nact)
                        glob[a] += glob[q]; glob[q] = 0
                nP2 = 0
                for k in range(K):
                    if glob[k] > 0: nP2 += 1
                lastP = nP2
            continue
        # ---------------- one possibly-effective birth
        b = b + G + 1
        if np.random.random() * pa * I < nact:
            i = act[np.random.randint(nact)]
            mig = mm > 0.0 and np.random.random() < mm
        else:
            i = act[nact + np.random.randint(I - nact)]
            mig = True
        src = i
        if mig:
            src = np.random.randint(I - 1)
            if src >= i: src += 1
        child = AS._sample_parent(counts, paysum, U, pres, npres, src, N, w)
        if src != i:
            cb = counts[i, child]
            for z_ in range(NBm): comp[i, child, z_] = (cb * comp[i, child, z_] + comp[src, child, z_]) / (cb + 1)
        u = np.random.randint(N); acc = 0; victim = pres[i, 0]
        for t in range(npres[i]):
            k = pres[i, t]; acc += counts[i, k]
            if u < acc:
                victim = k; break
        if mig:
            arr_all[i] += 1
            mig_ct[tag[child], 4 if shold[i] < 0 else tag[shold[i]]] += 1
        if est[i] == 0:
            if mig:
                cl = 0
                arr[i] += 1
                if coopmask[child]: arrC[i] += 1
                if child == iD: arrD[i] += 1
            else:
                cl = 1 if np.random.random() * counts[i, child] < loc[i, child] else 0
            vl = 1 if np.random.random() * counts[i, victim] < loc[i, victim] else 0
            loc[i, victim] -= vl; loc[i, child] += cl; locsum[i] += cl - vl
        if victim != child:
            counts[i, victim] -= 1; glob[victim] -= 1
            gtag[tag[victim]] -= 1
            if gtag[tag[victim]] == 0 and t_ext[tag[victim]] < 0:
                t_ext[tag[victim]] = b / IN
            if counts[i, victim] == 0:
                p = pos[i, victim]; last = pres[i, npres[i] - 1]
                pres[i, p] = last; pos[i, last] = p; pos[i, victim] = -1; npres[i] -= 1
            new = counts[i, child] == 0
            if new:
                pres[i, npres[i]] = child; pos[i, child] = npres[i]; npres[i] += 1
            counts[i, child] += 1; glob[child] += 1; gtag[tag[child]] += 1
            for t in range(npres[i]):
                j = pres[i, t]
                if new and j == child:
                    continue
                paysum[i, j] += U[j, child] - U[j, victim]
            if new:
                v = 0.0
                for t in range(npres[i]):
                    k = pres[i, t]
                    v += counts[i, k] * U[child, k]
                paysum[i, child] = v
        nact = _setact(i, _isactive(i, npres, est, locsum, N), act, apos, nact)
    if status == 0:
        allf = True
        for i in range(I):
            lo = 1e300; hi = -1e300
            for t in range(npres[i]):
                a = pres[i, t]
                for t2 in range(npres[i]):
                    q = pres[i, t2]
                    if U[a, q] < lo: lo = U[a, q]
                    if U[a, q] > hi: hi = U[a, q]
            if hi - lo >= 1e-12:
                allf = False
        status = 3 if allf else 4
    isl_cc = np.zeros(I); isl_pay = np.zeros(I)
    for i in range(I):
        isl_cc[i], isl_pay[i] = AS._island_cc(counts, PCC, U, pres, npres, paysum, i, N)
    return (status, stop_gen, counts, isl_cc, isl_pay, trace[:ci], t_ext, held_zero, parent,
            t_est, e_arr, e_arrC, e_arrD, e_imm, e_hold, e_hloc, t90, a90, imm90, h90, hl90, arr_all,
            loss_log[:min(nloss, 2000)], nloss, first_sep, sep_a, sep_b, nsepchk, tr_log[:min(ntr, 50000)], ntr, mig_ct, comp, snap_gen, snap_hold, snap_cert, snap_comp)


# ------------------------------------------------------------------ lottery
# Kernel: rival_islands._kern (exact skipping, exact lumping, ancestry labels, strong-holder log), copied as _kern_mb
# with the expected budget composition of every (island, class) carried along (no effect on the law).  PD, w = 0.3,
# eps = 0, complete island graph, generation = I*N births, horizon 1e5.  Seeds: iid canonical sources of L_8 from the
# length prior (one stream per (N, I, rep), shared by every budget prior), then a budget per non-constant individual
# by inverse CDF of one uniform per individual (shared by every prior: a monotone coupling), lumped by the
# catalogue's classes.  Forced founders replace one uniformly chosen seed individual on each forced island.
SALT = 20261009
GENS = 100000
CALIB = os.path.join(RUNS, 'mixed-budgets-calib.json')
COMMON_MN = 1.091
NB = 4                                           # budget slots: 0 = unbudgeted (C, D), 1..3 = B


def kern():
    return _kern_mb


def seed_streams(N, I, rep, cell):
    rs = [SALT, N, I, rep]                        # sources
    rb = [SALT + 1, N, I, rep]                    # budget uniforms
    rf = [SALT + 2, N, I, rep]                    # founder placement / bridge redraws
    return rs, rb, rf


def kstream(exp, prior, N, I, mN, rep, cell):
    return (1000003 * rep + 7919 * zlib.crc32(exp.encode()) + 104729 * zlib.crc32(prior.encode()) + 13 * N + 17 * I
            + int(round(mN * 1000)) + 31 * zlib.crc32(str(cell).encode()) + SALT) % (2 ** 31 - 1)


def build_seed(d, prior, N, I, rep, cell=None):
    """Genotype counts per island (I x G).  cell: None (iid), or dict(founders=[(island set, genotype)],
    remove=[class indices] (redrawn from the renormalized law))."""
    L = d['L']
    mu_s = L.mu_canon / L.mu_canon.sum()
    rs, rb, rf = seed_streams(N, I, rep, cell)
    rng = np.random.default_rng(rs); rngb = np.random.default_rng(rb); rngf = np.random.default_rng(rf)
    nB = len(d['Bs'])
    cdf = np.cumsum(np.array(PRIORS[prior] if isinstance(prior, str) else prior, float))
    # genotype index of (source c, budget slot j): constants by gidx, others by name
    gi = np.full((len(L.rep), nB), -1, np.int64)
    for g in range(d['G']):
        if d['gb'][g] == 0:
            gi[d['base'][g], :] = g
        else:
            gi[d['base'][g], d['bidx'][g] - 1] = g
    out = np.zeros((I, d['G']), np.int64)
    for i in range(I):
        x = rng.multinomial(N, mu_s)
        for c in np.nonzero(x)[0]:
            u = rngb.random(x[c])
            j = np.minimum(np.searchsorted(cdf, u, side='right'), nB - 1)
            np.add.at(out[i], gi[c, j], 1)
    if cell:
        rem = cell.get('remove')
        if rem is not None and len(rem):
            bad = np.isin(d['cls_of'], rem)
            gm = gmass(d, PRIORS[prior] if isinstance(prior, str) else prior)
            gm2 = np.where(bad, 0.0, gm); gm2 = gm2 / gm2.sum()
            for i in range(I):
                nb = int(out[i, bad].sum())
                if nb:
                    out[i, bad] = 0
                    out[i] += rngf.multinomial(nb, gm2)
        for isl, g in cell.get('founders', []):
            for i in isl:
                u = rngf.integers(N)
                c = int(np.searchsorted(np.cumsum(out[i]), u, side='right'))
                out[i, c] -= 1; out[i, g] += 1
    return out


def lump_seed(d, gcounts):
    """Class counts (I x K) and the budget composition comp0 (I x K x NB) of each class on each island."""
    I = gcounts.shape[0]; K = d['K']
    init = np.zeros((I, K), np.int64); bc = np.zeros((I, K, NB))
    for i in range(I):
        nz = np.nonzero(gcounts[i])[0]
        np.add.at(init[i], d['cls_of'][nz], gcounts[i, nz])
        np.add.at(bc[i], (d['cls_of'][nz], d['bidx'][nz]), gcounts[i, nz])
    comp0 = bc / np.maximum(init, 1)[:, :, None]
    return init, comp0


def pair_tags(d, sup, X, Y):
    """Network tags (rival_islands.tags_for): 1 = cooperative, mutually cooperating with X not Y; 2 = with Y not X;
    3 = with both (bridge); 0 = other."""
    V = d['V']; t = np.zeros(len(sup), np.int64)
    if X is None:
        return t
    vX = V[sup, X].astype(bool) & V[X, sup].astype(bool)
    vY = V[sup, Y].astype(bool) & V[Y, sup].astype(bool)
    sc = d['coop'][sup]
    t[sc & vX & ~vY] = 1; t[sc & vY & ~vX] = 2; t[sc & vX & vY] = 3
    return t


def sep_intervals(trace):
    g = trace[:, 0]; f = trace[:, 8] > 0.5
    if not f.any():
        return dict(ever=False, n_episodes=0, first=-1, last_sep=-1, resolved_at=-1, sep_at_end=False, sep_checks=0)
    on = np.nonzero(f)[0]
    last = int(on[-1]); sep_end = bool(f[-1])
    return dict(ever=True, n_episodes=int(1 + np.sum(np.diff(on) > 1)), first=int(g[on[0]]), last_sep=int(g[last]),
                resolved_at=-1 if sep_end else int(g[last + 1]), sep_at_end=sep_end, sep_checks=int(f.sum()))


def comp_dist(holders, certs, coop, comp_rows):
    """Island-weighted budget distribution (slots 1..3) of cooperative certified holders: one vote per island, the vote
    being the holder's expected budget composition on that island."""
    v = []
    for h, c, row in zip(holders, certs, comp_rows):
        if h >= 0 and c and coop[h]:
            r = np.asarray(row[1:], float)
            if r.sum() > 0:
                v.append(r / r.sum())
    if not v:
        return None, 0
    return [float(x) for x in np.mean(v, 0)], len(v)


_SCR = {}


def pair_static(d, prior, x, y):
    """Static type of an incompatible pair of global classes under the prior (bridges of positive mass, structural
    bridges, path length, component, budget copies)."""
    key = (prior, min(x, y), max(x, y))
    if key in _SCR:
        return _SCR[key]
    if prior not in _SCR:
        V = d['V'].astype(bool); mu = cmass(d, PRIORS[prior]); pos = mu > 0
        E = np.nonzero(d['est_s'] & pos)[0]
        adjE = (V & V.T)[np.ix_(E, E)].copy(); np.fill_diagonal(adjE, False)
        comp, _ = components(adjE)
        _SCR[prior] = dict(V=V, mu=mu, raw=cmass(d, PRIORS[prior], raw=True), pos=pos, E=E, adjE=adjE, comp=comp,
                           posE={int(k): i for i, k in enumerate(E)})
    S = _SCR[prior]
    MC = S['V'] & S['V'].T
    path = None; same = None
    if x in S['posE'] and y in S['posE']:
        dd = bfs_dist(S['adjE'], S['posE'][x]); v = dd[S['posE'][y]]
        path = int(v) if v >= 0 else None; same = bool(S['comp'][S['posE'][x]] == S['comp'][S['posE'][y]])
    r = pair_row(d, x, y, S['mu'], S['raw'], S['pos'], MC, d['est_s'], path, same)
    r['budgets_x'] = budgets_of(d, x, PRIORS[prior]); r['budgets_y'] = budgets_of(d, y, PRIORS[prior])
    _SCR[key] = r
    return r


def job(j):
    """j = (exp, prior, N, I, mN, rep, gens, cell) with cell None | 'bl' | 'br' | 'brabs' | 'dctl' (forced cells:
    the pairs are fixed in FORCED, chosen from the static screening)."""
    exp, prior, N, I, mN, rep, gens, cell = j
    d = catalogue(B); nm = d['names']
    FORCED['I'] = I
    cfg = forced_cfg(d, cell) if cell else None
    gcounts = build_seed(d, prior, N, I, rep, cfg)
    init, comp0 = lump_seed(d, gcounts)
    X = Y = None
    if cfg and cfg.get('X') is not None:
        X, Y = cfg['X'], cfg['Y']
    t0 = time.time()
    sup = sorted(set(np.nonzero(init.sum(0) > 0)[0].tolist()) | ({X, Y} if X is not None else set()))
    ext = np.array(sup, np.int64)
    Vs = d['V'][np.ix_(ext, ext)].astype(np.int64)
    U = np.ascontiguousarray(PDP[Vs, Vs.T]); PCC = np.ascontiguousarray((Vs * Vs.T).astype(float))
    coop = d['coop'][ext].copy()
    tag = pair_tags(d, ext, X, Y) if (cell in ('bl', 'br', 'brabs')) else np.zeros(len(ext), np.int64)
    li = np.ascontiguousarray(init[:, ext]); c0 = np.ascontiguousarray(comp0[:, ext, :])
    K = len(ext)
    ss = kstream(exp, prior, N, I, mN, rep, cell)
    rr = np.random.default_rng(ss); r1 = rr.random(K); r2 = rr.random(K)
    iDl = int(np.nonzero(ext == d['iD'])[0][0]) if (ext == d['iD']).any() else -1
    import rival_islands as R_
    o = kern()(U, PCC, coop, tag, li, c0, N, W, mN / N, ss, R_.checks_schedule(gens), True, iDl, r1, r2,
               np.zeros(I, np.int64))
    (st, sg, counts, isl_cc, isl_pay, trace, t_ext, held_zero, parent, t_est, e_arr, e_arrC, e_arrD, e_imm, e_hold, e_hloc,
     t90, a90, imm90, h90, hl90, arr_all, loss_log, nloss, first_sep, sep_a, sep_b, nsepchk, tr_log, ntr, mig_ct,
     comp, snap_gen, snap_hold, snap_cert, snap_comp) = o
    root = np.arange(K)
    for x in range(K):
        r_ = x
        while parent[r_] != r_: r_ = parent[r_]
        root[x] = r_
    G_ = lambda x: nm[int(ext[x])] if x >= 0 else None
    glob = counts.sum(0)
    hold = np.array([R_.holder(counts[i]) for i in range(I)])
    estd = t_est >= 0
    x = glob / glob.sum(); pr = np.nonzero(x)[0]
    cf = float(x[pr] @ PCC[np.ix_(pr, pr)] @ x[pr])
    cert_end = isl_cc >= 0.95
    r = dict(exp=exp, prior=prior, N=N, I=I, mN=mN, rep=rep, gens=gens, cell=cell,
             status=R_.STATUS[int(st)], stop_gen=int(sg), pcc=float(isl_cc.mean()), pcc_min=float(isl_cc.min()),
             pcc_cert=float(isl_cc[cert_end].mean()) if cert_end.any() else float('nan'),
             cf_cross_pcc=cf, isl_eff=int(cert_end.sum()), n_est=int(estd.sum()), n_support=int(K),
             n_classes_end=int((glob > 0).sum()))
    r['t_est'] = [int(v) for v in t_est]
    r['final_trace'] = [float(v) for v in trace[-1]]
    w5 = np.nonzero(trace[:, 0] == 100000)[0]
    r['trace_1e5'] = [float(v) for v in trace[w5[0]]] if len(w5) else None
    # holders and composition at the two checkpoints
    r['snap_gen'] = int(snap_gen)
    sd, sn = comp_dist(snap_hold, snap_cert, coop, snap_comp) if snap_gen >= 0 else (None, 0)
    strong_end = np.array([10 * counts[i, hold[i]] >= 9 * N for i in range(I)])
    ed, en = comp_dist(hold, strong_end, coop, [comp[i, hold[i]] for i in range(I)])
    r['comp_snap'] = sd; r['comp_snap_n'] = sn; r['comp_end'] = ed; r['comp_end_n'] = en
    r['holders_end'] = dict(Counter(G_(h) for h in hold).most_common(8))
    r['holders_end_budget'] = dict(Counter('%s' % budgets_of(d, int(ext[h])) for h in hold if coop[h]).most_common(4))
    hc = sorted({int(h) for i, h in enumerate(hold) if cert_end[i] and coop[h]})
    sep_end = [(a, b) for ai, a in enumerate(hc) for b in hc[ai + 1:] if U[a, b] == -1 and U[b, a] == -1]
    r['first_sep'] = int(first_sep); r['n_sep_end'] = len(sep_end)
    r['sep'] = sep_intervals(trace)
    if first_sep >= 0 or sep_end:
        Sx = [('first', int(root[sep_a]), int(root[sep_b]))] if first_sep >= 0 else []
        Sx += [('end', a, b) for a, b in sep_end[:4]]
        Vx = d['V'][np.ix_(ext, ext)].astype(bool)
        out = []
        for kind, a, b in Sx:
            ga, gb_ = int(ext[a]), int(ext[b])
            c = dict(when=kind, a=G_(a), b=G_(b))
            ps = pair_static(d, prior, ga, gb_)
            c.update(n_bridges_prior=ps['n_bridges'], n_bridges_struct=ps['n_bridges_struct'], path=ps['path'],
                     same_comp=ps['same_comp'], budget_copies=ps['budget_copies'], budgets_a=ps['budgets_x'],
                     budgets_b=ps['budgets_y'], pair_mu=ps['pair_mu'])
            mcab = Vx[:, a] & Vx[a, :] & Vx[:, b] & Vx[b, :] & coop
            mcab[[a, b]] = False
            brl = np.nonzero(mcab)[0]
            br_set = set(brl.tolist())
            med = 0; t_med = -1
            for g_, i_, a_, b_ in tr_log:
                if a_ >= 0 and b_ in br_set and root[a_] in (a, b):
                    med += 1
                    if t_med < 0: t_med = int(g_)
            c.update(n_bridge_classes_seeded=int(len(brl)), bridge_seed=int(li[:, brl].sum()) if len(brl) else 0,
                     bridge_seed_islands=int((li[:, brl].sum(1) > 0).sum()) if len(brl) else 0,
                     bridge_alive_end=bool(glob[brl].sum() > 0) if len(brl) else False,
                     bridge_held_end=int(np.isin(hold, brl).sum()) if len(brl) else 0,
                     mediations=med, t_first_med=t_med,
                     held_a=int((root[hold] == a).sum()), held_b=int((root[hold] == b).sum()))
            out.append(c)
        r['seps'] = out
    if cell in ('bl', 'br', 'brabs', 'dctl'):
        r['forced'] = [cfg['xname'], cfg['yname']]
        held = {t: trace[:, 3 + (t - 1)] for t in (1, 2)}
        heldc = {t: trace[:, 5 + (t - 1)] for t in (1, 2)}
        g = trace[:, 0]
        htag = tag[hold]
        r['founders'] = int(sum(len(isl) for isl, _ in cfg['founders']))
        if cell != 'dctl':
            ev = np.nonzero((heldc[1] >= 1) & (heldc[2] >= 1))[0]
            r['ever_sep_tag'] = bool(len(ev) > 0); r['t_sep_tag'] = int(g[ev[0]]) if len(ev) else -1
            e1 = np.nonzero(heldc[1] >= 1)[0]; e2 = np.nonzero(heldc[2] >= 1)[0]
            r['x_est'] = bool(len(e1) > 0); r['y_est'] = bool(len(e2) > 0)
            loss_t = -1; loss_net = 0
            if len(ev):
                after = np.arange(ev[0], len(g))
                z1 = after[held[1][after] == 0]; z2 = after[held[2][after] == 0]
                c1 = int(g[z1[0]]) if len(z1) else -1; c2 = int(g[z2[0]]) if len(z2) else -1
                cands = [(c_, k_) for c_, k_ in ((c1, 1), (c2, 2)) if c_ >= 0]
                if cands:
                    loss_t, loss_net = min(cands)
            r['loss_t'] = loss_t; r['loss_net'] = loss_net
            import island_path as IP
            tend = loss_t if loss_t >= 0 else float(sg)
            r['expo'] = IP.integ(trace, 3, 4, tend) if len(ev) else 0.0
            r['expo_start'] = int(g[ev[0]]) if len(ev) else -1
            r['sep_end_tag'] = bool(((htag == 1) & cert_end).any() and ((htag == 2) & cert_end).any())
            r['held_end'] = {str(t): int((htag == t).sum()) for t in range(4)}
            b3 = tag == 3
            r['bridge_classes'] = int(b3.sum())
            r['bridge_seed_islands'] = int((li[:, b3].sum(1) > 0).sum()); r['bridge_seed_copies'] = int(li[:, b3].sum())
            inv = Counter(); med_t = []
            for g_, i_, a_, b_ in tr_log:
                if a_ < 0: continue
                ta, tb = int(tag[a_]), int(tag[b_])
                if ta != tb:
                    inv['%d>%d' % (ta, tb)] += 1
                    if ta in (1, 2) and tb == 3: med_t.append(int(g_))
            r['inv'] = dict(inv); r['n_med'] = len(med_t); r['t_med'] = med_t[0] if med_t else -1
            lim = loss_t if loss_t >= 0 else int(sg)
            r['med_before_end'] = bool(any(t <= lim for t in med_t))
            r['bridge_alive_end'] = bool(glob[b3].sum() > 0)
            r['bridge_alive_sep'] = bool(r['bridge_alive_end'])
            r['t_ext'] = [float(v) for v in t_ext]
        # founders' classes alive / cooperative establishment by the forced classes
        fx = [int(np.nonzero(ext == cfg['X'])[0][0])] if cfg.get('X') is not None else []
        r['n_loc_est'] = int((estd & (e_hloc >= 0.5)).sum())
    r['time_s'] = time.time() - t0
    return r


# forced cells: the pairs are chosen from the static screening (predictions addendum) and set here
FORCED = {}


def forced_cfg(d, cell):
    I = FORCED['I']
    half = (list(range(I // 2)), list(range(I // 2, I)))
    if cell == 'dctl':
        g = d['gidx']['D']
        return dict(X=None, Y=None, founders=[(half[0], g), (half[1], g)], xname='D', yname='D')
    key = 'bl' if cell == 'bl' else 'br'
    gx, gy = d['gidx'][FORCED[key][0]], d['gidx'][FORCED[key][1]]
    X, Y = int(d['cls_of'][gx]), int(d['cls_of'][gy])
    cfg = dict(X=X, Y=Y, founders=[(half[0], gx), (half[1], gy)], xname=FORCED[key][0], yname=FORCED[key][1])
    if cell == 'brabs':
        V = d['V'].astype(bool); MC = V & V.T
        br = d['coop_s'] & MC[X] & MC[Y]; br[[X, Y]] = False
        cfg['remove'] = np.nonzero(br)[0]
    return cfg


def rows_path(exp):
    return os.path.join(RUNS, 'mixed-budgets', 'rows-%s.json.gz' % exp)


def load(exp):
    p = rows_path(exp)
    return json.load(gzip.open(p, 'rt')) if os.path.exists(p) else []


def save(exp, rows):
    def conv(o):
        if isinstance(o, np.integer): return int(o)
        if isinstance(o, np.floating): return float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, np.bool_): return bool(o)
        raise TypeError(type(o))
    tmp = rows_path(exp) + '.tmp'
    with gzip.open(tmp, 'wt') as f:
        json.dump(rows, f, default=conv)
    os.replace(tmp, rows_path(exp))


def ckey(r):
    return (r['exp'], r['prior'], r['N'], r['I'], r['mN'], r['gens'], r['cell'])


def warm():
    catalogue(B)
    load_forced()
    job(('time', 'cheap', 20, 4, 1.0, 0, 50, None))


def load_forced():
    p = os.path.join(RUNS, 'mixed-budgets', 'forced.json')
    if os.path.exists(p):
        FORCED.update(json.load(open(p)))
    FORCED.setdefault('I', 64)


def boundary():
    return dict(json.load(open(CALIB))['mN_boundary'])


def cells(exp, a):
    """(exp, prior, N, I, mN, reps, gens, cell)."""
    out = []
    if exp == 'cal':
        for p in ('cheap', 'above', 'uniform', 'h4', 'h8', 'h16'):
            out.append(('cal', p, 200, 16, 0.0, 120, GENS, None))
    elif exp == 'hom':
        for p in ('h16', 'h8', 'h4'):
            out.append(('hom', p, 200, 64, COMMON_MN, a.reps, GENS, None))
    elif exp == 'nat':
        for p in a.priors:
            out.append(('nat', p, 200, 64, COMMON_MN, a.reps, GENS, None))
    elif exp == 'natcal':
        Bd = boundary()
        for p in a.priors:
            out.append(('natcal', p, 200, 64, Bd[p], a.reps, GENS, None))
    elif exp == 'forced':
        for c in a.cells:
            out.append(('forced', a.priors[0], 200, 64, COMMON_MN, a.reps, GENS, None if c == 'iid' else c))
    elif exp == 'scale':
        for I, gens in ((64, 300000), (256, 100000), (256, 300000)):
            out.append(('scale', a.priors[0], 200, I, COMMON_MN, a.reps, gens, a.cells[0]))
    return out


def run_main(a):
    load_forced()
    rows = load(a.exp)
    done = Counter(ckey(r) for r in rows)
    jobs = []
    for c in cells(a.exp, a):
        e, p, N, I, mN, reps, gens, cell = c
        key = (e, p, N, I, mN, gens, cell)
        if a.exp == 'scale':
            FORCED['I'] = I
        for rep in range(done[key], reps):
            jobs.append((e, p, N, I, mN, rep, gens, cell))
    jobs.sort(key=lambda j: (j[5], j[1], str(j[7])))
    print('%s: %d jobs' % (a.exp, len(jobs)), flush=True)
    t0 = time.time()
    with Pool(a.procs, initializer=warm) as pool:
        for r in pool.imap_unordered(job_scaled, jobs):
            rows.append(r)
            print('%s %s %s mN=%g I=%d rep %d: %s gen %d pcc %.3f sep_end %d first_sep %d tag %s (%.1fs; %.0fs total)' % (
                r['exp'], r['prior'], r['cell'], r['mN'], r['I'], r['rep'], r['status'], r['stop_gen'], r['pcc'],
                r['n_sep_end'], r['first_sep'], r.get('sep_end_tag'), r['time_s'], time.time() - t0), flush=True)
            if len(rows) % 25 == 0:
                save(a.exp, rows)
    save(a.exp, rows)


def job_scaled(j):
    FORCED['I'] = j[3]
    return job(j)


def calib_main(a):
    rows = load('cal')
    out = dict(T_nuc={}, dist={}, p={}, mN_boundary={}, n_nuc={}, x=0.3, N=200, I=16, runs={})
    for p in PRIORS:
        rs = [r for r in rows if r['prior'] == p]
        if not rs: continue
        ts = np.array([t for r in rs for t in r['t_est'] if t >= 0], float)
        nis = sum(r['I'] for r in rs)
        T = float(np.median(ts))
        out['runs'][p] = len(rs)
        out['T_nuc'][p] = T; out['n_nuc'][p] = [int(len(ts)), int(nis)]; out['p'][p] = float(len(ts) / nis)
        out['dist'][p] = {str(q): float(np.percentile(ts, q)) for q in (25, 50, 75)}
        out['mN_boundary'][p] = round(0.3 * 200 / T, 3)
        rng = np.random.default_rng(1)
        per = [np.array([t for t in r['t_est'] if t >= 0]) for r in rs]
        bs = []
        for _ in range(2000):
            idx = rng.integers(0, len(per), len(per))
            v = np.concatenate([per[i] for i in idx])
            if len(v): bs.append(np.median(v))
        out['dist'][p]['median_ci'] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
    json.dump(out, open(CALIB, 'w'), indent=1)
    print(json.dumps(out, indent=1))


def timing_main(a):
    load_forced()
    for p in ('cheap', 'above', 'h4', 'h16'):
        t = time.time()
        r = job(('time', p, 200, 64, COMMON_MN, a.rep, GENS, None))
        print(p, r['status'], r['stop_gen'], '%.1fs' % (time.time() - t), round(r['pcc'], 3), 'sep_end', r['n_sep_end'],
              'first', r['first_sep'], 'snap', r['snap_gen'], r['comp_snap'], r['comp_end'], r['holders_end'], flush=True)


# ------------------------------------------------------------------ report
OUT_MD = os.path.join(RUNS, 'mixed-budgets.md')
OUT_JS = os.path.join(RUNS, 'mixed-budgets.json')
MARKS = (100, 1000, 10000, 100000, 300000)


def cp(k, n, a=0.05):
    """Exact (Clopper-Pearson) two-sided interval."""
    from scipy.stats import beta
    if n == 0: return (float('nan'), float('nan'))
    lo = 0.0 if k == 0 else float(beta.ppf(a / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - a / 2, k + 1, n - k))
    return lo, hi


def cps(k, n, d=3):
    if n == 0: return '–'
    lo, hi = cp(k, n)
    return ('%d/%d = %.' + str(d) + 'f [%.' + str(d) + 'f, %.' + str(d) + 'f]') % (k, n, k / n, lo, hi)


def fe(x, dg=2):
    if x is None or (isinstance(x, float) and math.isnan(x)): return '–'
    if x == 0: return '0'
    return ('%.' + str(dg - 1) + 'e') % x if (abs(x) < 1e-2 or abs(x) >= 1e4) else ('%.' + str(dg + 1) + 'g') % x


def km(times, events, marks=MARKS):
    t = np.asarray(times, float); e = np.asarray(events, bool)
    o = np.argsort(t, kind='stable'); t = t[o]; e = e[o]
    S = 1.0; at = len(t); res = []
    for ti, ei in zip(t, e):
        if ei: S *= (at - 1) / at
        at -= 1; res.append((ti, S))
    out = {}
    for mk in marks:
        s = 1.0
        for ti, Si in res:
            if ti <= mk: s = Si
            else: break
        out[mk] = s
    return out


def poisson_upper(k, expo):
    from scipy.stats import chi2
    if expo <= 0: return float('nan')
    return float(chi2.ppf(0.975, 2 * k + 2) / 2 / expo)


BUD = np.array([4.0, 8.0, 16.0])


def tv(p, q):
    return 0.5 * float(np.abs(np.asarray(p) - np.asarray(q)).sum())


def comp_stats(rs, prior):
    pr = np.array(PRIORS[prior], float)
    both = [r for r in rs if r['comp_snap'] is not None and r['comp_end'] is not None]
    out = dict(n_both=len(both), n=len(rs))
    if not both:
        return out
    S = np.array([r['comp_snap'] for r in both]); E = np.array([r['comp_end'] for r in both])
    tS = np.array([tv(s, pr) for s in S]); tE = np.array([tv(e_, pr) for e_ in E])
    dT = tE - tS; dB = E @ BUD - S @ BUD
    rng = np.random.default_rng(5); bs = []; bb = []
    for _ in range(2000):
        ix = rng.integers(0, len(both), len(both))
        bs.append(dT[ix].mean()); bb.append(dB[ix].mean())
    out.update(snap=[float(x) for x in S.mean(0)], end=[float(x) for x in E.mean(0)], tv_snap=float(tS.mean()),
               tv_end=float(tE.mean()), dtv=float(dT.mean()), dtv_ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
               dbud=float(dB.mean()), dbud_ci=[float(np.percentile(bb, 2.5)), float(np.percentile(bb, 97.5))],
               tv_pooled_snap=tv(S.mean(0), pr), tv_pooled_end=tv(E.mean(0), pr),
               snap_gen_median=float(np.median([r['snap_gen'] for r in both])),
               bud_snap=float((S @ BUD).mean()), bud_end=float((E @ BUD).mean()))
    # the same, restricted to unseparated runs (the main network alone)
    un = [r for r in both if r['n_sep_end'] == 0]
    if un:
        S2 = np.array([r['comp_snap'] for r in un]); E2 = np.array([r['comp_end'] for r in un])
        out['unsep'] = dict(n=len(un), bud_snap=float((S2 @ BUD).mean()), bud_end=float((E2 @ BUD).mean()),
                            dtv=float(np.mean([tv(e_, pr) - tv(s, pr) for s, e_ in zip(S2, E2)])))
    return out


def has_b1_4(names):
    return any(x is not None and x.startswith(FB1 + '@4') for x in names)


def nat_stats(rs):
    n = len(rs); prior = rs[0]['prior']
    st = dict(n=n, prior=prior, mN=rs[0]['mN'], status=dict(Counter(r['status'] for r in rs)))
    st['ever'] = sum(r['first_sep'] >= 0 for r in rs)
    st['end'] = sum(r['n_sep_end'] > 0 for r in rs)
    st['end_ci'] = list(cp(st['end'], n)); st['ever_ci'] = list(cp(st['ever'], n))
    ends = [r for r in rs if r['n_sep_end'] > 0]
    pairs_end = Counter(); kinds = Counter()
    for r in ends:
        e_ = [s for s in r.get('seps', []) if s['when'] == 'end']
        if not e_: continue
        s = e_[0]
        pairs_end['%s | %s' % tuple(sorted((s['a'], s['b'])))] += 1
        kinds['bridge-less (prior)' if s['n_bridges_prior'] == 0 else 'bridged (prior)'] += 1
        kinds['struct bridge-less' if s['n_bridges_struct'] == 0 else 'struct bridged'] += 1
        kinds['budget copies' if s['budget_copies'] else 'distinct sources'] += 1
        kinds['BOX1@4 member' if has_b1_4([s['a'], s['b']]) else 'no BOX1@4'] += 1
        kinds['disconnected (no path<=3)' if (s['path'] is None or s['path'] > 3) else 'path<=3'] += 1
        if s['n_bridges_prior'] > 0:
            kinds['bridged: bridge seeded' if s['bridge_seed'] > 0 else 'bridged: bridge not seeded'] += 1
            kinds['bridged: bridge alive at end' if s['bridge_alive_end'] else 'bridged: bridge dead/absent at end'] += 1
    st['pairs_end'] = dict(pairs_end.most_common(12)); st['kinds_end'] = dict(kinds)
    ev = [r for r in rs if r['sep']['ever']]
    dur = [(r['sep']['resolved_at'] - r['sep']['first']) if not r['sep']['sep_at_end'] else (r['stop_gen'] - r['sep']['first']) for r in ev]
    evt = [not r['sep']['sep_at_end'] for r in ev]
    st['resolved'] = int(sum(evt)); st['censored'] = int(len(evt) - sum(evt))
    st['expo'] = float(sum(dur)); st['hazard'] = st['resolved'] / st['expo'] if st['expo'] else float('nan')
    st['hazard_upper'] = poisson_upper(st['resolved'], st['expo'])
    st['km'] = {str(k): v for k, v in km(dur, evt).items()} if ev else {}
    fate = Counter()
    for r in ev:
        f = [s for s in r.get('seps', []) if s['when'] == 'first']
        if not f: continue
        s = f[0]
        key = ('bridge-less' if s['n_bridges_prior'] == 0 else ('bridged, ' + ('seeded' if s['bridge_seed'] else 'not seeded')
               + (', alive' if s['bridge_alive_end'] else ', dead'))) + (', separated at end' if r['sep']['sep_at_end'] else ', resolved')
        fate[key] += 1
    st['fate_first'] = dict(fate)
    pc = [r['pcc_cert'] for r in rs if not math.isnan(r['pcc_cert'])]
    st['pcc_cert'] = float(np.mean(pc)) if pc else float('nan'); st['pcc_cert_min'] = float(np.min(pc)) if pc else float('nan')
    st['runlevel'] = float(np.mean([r['isl_eff'] / r['I'] for r in rs]))
    st['alld'] = sum(r['isl_eff'] == 0 for r in rs)
    st['cf_sep'] = float(np.mean([r['cf_cross_pcc'] for r in ends])) if ends else float('nan')
    st['cf_all'] = float(np.mean([r['cf_cross_pcc'] for r in rs]))
    st['hours'] = sum(r['time_s'] for r in rs) / 3600
    st['comp'] = comp_stats(rs, prior)
    st['b14_end'] = sum(1 for r in ends if any(has_b1_4([s['a'], s['b']]) for s in r.get('seps', []) if s['when'] == 'end'))
    return st


def paired(a, b, key):
    A = {r['rep']: r for r in a}; Bm = {r['rep']: r for r in b}
    common = sorted(set(A) & set(Bm))
    x = [(key(A[k]), key(Bm[k])) for k in common]
    return dict(n=len(common), both=sum(1 for p, q in x if p and q), a_only=sum(1 for p, q in x if p and not q),
                b_only=sum(1 for p, q in x if q and not p))


def forced_stats(rs):
    n = len(rs)
    st = dict(n=n, cell=rs[0]['cell'], prior=rs[0]['prior'], I=rs[0]['I'], gens=rs[0]['gens'], forced=rs[0].get('forced'))
    st['end'] = sum(r['n_sep_end'] > 0 for r in rs)
    st['pcc_cert'] = float(np.nanmean([r['pcc_cert'] for r in rs]))
    st['runlevel'] = float(np.mean([r['isl_eff'] / r['I'] for r in rs]))
    st['hours'] = sum(r['time_s'] for r in rs) / 3600
    st['n_loc_est'] = float(np.mean([r.get('n_loc_est', 0) for r in rs]))
    if rs[0]['cell'] in ('bl', 'br', 'brabs'):
        both = [r for r in rs if r['ever_sep_tag']]
        st['x_est'] = sum(r['x_est'] for r in rs); st['y_est'] = sum(r['y_est'] for r in rs)
        st['both_est'] = len(both)
        st['sep_tag_end'] = sum(r['sep_end_tag'] for r in rs)
        st['sep_tag_end_given_both'] = sum(r['sep_end_tag'] for r in both)
        st['losses'] = sum(r['loss_t'] >= 0 for r in both)
        st['expo'] = float(sum(r['expo'] for r in both))
        st['hazard'] = st['losses'] / st['expo'] if st['expo'] else float('nan')
        st['hazard_upper'] = poisson_upper(st['losses'], st['expo'])
        st['med_before'] = sum(r['med_before_end'] for r in both)
        st['bridge_classes'] = float(np.mean([r['bridge_classes'] for r in rs]))
        st['bridge_seed_islands'] = float(np.mean([r['bridge_seed_islands'] for r in rs]))
        st['bridge_alive_end'] = sum(r['bridge_alive_end'] for r in rs)
        st['sep_bridge_alive'] = sum(r['sep_end_tag'] for r in rs if r['bridge_alive_end'])
        st['sep_bridge_dead'] = sum(r['sep_end_tag'] for r in rs if not r['bridge_alive_end'])
        st['n_bridge_alive'] = sum(1 for r in rs if r['bridge_alive_end'])
        st['inv'] = dict(sum((Counter(r['inv']) for r in rs), Counter()))
        st['held_end'] = {k: float(np.mean([r['held_end'][k] for r in rs])) for k in ('0', '1', '2', '3')}
        st['cf_sep'] = float(np.mean([r['cf_cross_pcc'] for r in rs if r['sep_end_tag']])) if st['sep_tag_end'] else float('nan')
    return st


def report_main(a):
    S = json.load(open(STATIC))
    cal = json.load(open(CALIB)) if os.path.exists(CALIB) else None
    out = dict(static_summary={}, cells={})
    md = ['# Mixed-budget populations under K: do budget soft cliques become bridge-less rivals when budgets vary? '
          '(`src/mixed_budgets.py`)', '',
          'Spec `specs/2026-10-05-mixed-budgets.md` (reviewed by gpt-6.1-sol); predictions '
          '`predictions/2026-10-05-mixed-budgets.md`. Modal language L_8 under the sound bounded calculus K; genotypes '
          '(source, budget) with budget in B = {4, 8, 16} (C and D unbudgeted); plays from the K tables and the cross-budget '
          'blocks (`runs/k-at-n8/`, guard at the reader\'s own budget). PD, w = 0.3, ε = 0, complete island graph, '
          'N = 200, I = 64, horizon 10⁵, generation = I·N births. Seeds: iid canonical sources from the length prior, a '
          'budget per non-constant individual by inverse CDF of one shared uniform (so every prior sees the same sources '
          'and monotonically coupled budgets: paired seeds across priors), lumped by the catalogue\'s behavioural classes. '
          '**Finite-horizon incidence at n = 8; not large-population universality or permanent isolation.** Intervals are '
          'exact (Clopper–Pearson) with runs as the units; hazards are events per exposure with a 97.5% Poisson upper '
          'bound; resolution times are right-censored (Kaplan–Meier).', '']
    md += a_static_md(S, out)
    if cal:
        md += ['## 3. Calibration (m = 0, N = 200, I = 16, 120 runs per prior)', '',
               '| prior | T_nuc (median [95% bootstrap]) | quartiles | per-island nucleation p | boundary mN = 0.3·N/T_nuc |',
               '|---|---|---|---|---|']
        for p in ('cheap', 'above', 'uniform', 'h4', 'h8', 'h16'):
            if p not in cal['T_nuc']: continue
            dd = cal['dist'][p]
            md.append('| %s | %.0f [%.0f, %.0f] | %.0f / %.0f / %.0f | %.3f (%d / %d) | %.3f |' % (
                PRLAB[p], cal['T_nuc'][p], dd['median_ci'][0], dd['median_ci'][1], dd['25'], dd['50'], dd['75'],
                cal['p'][p], cal['n_nuc'][p][0], cal['n_nuc'][p][1], cal['mN_boundary'][p]))
        md += ['', 'Checks are every 5 generations, so T_nuc is resolved to 5.', '']
        out['calib'] = cal
    md += lottery_md(cal, out)
    open(OUT_MD, 'w').write('\n'.join(md) + '\n')
    json.dump(out, open(OUT_JS, 'w'), indent=1, default=str)
    print('wrote', OUT_MD, OUT_JS)


def pr_fmt(p):
    return '(%s)' % ', '.join('%.2g' % x for x in PRIORS[p])


def a_static_md(S, out):
    md = ['## 1. The budgeted catalogue', '']
    so = S['soundness']
    md.append('**Catalogue.** %d genotypes (C, D and 608 non-constant sources at each of b = 4, 8, 16), %d behavioural '
              'classes (identical directed rows and columns). Soundness checks of the K closures behind each block: %s.' % (
                  S['G'], S['K'], '; '.join('%s: %d bad of %d' % (k.replace('_', '×'), v['sound_bad'], v['sound_checked'])
                                            for k, v in sorted(so.items()))))
    lc = S['lumping']
    md.append('')
    md.append('**Lumping validity.** Member rows/columns identical in every class (%d violations); masses preserved under '
              'every prior (max error %s); genotype-level seed draws lumped versus class-level draws agree in first moments '
              '(max |z| %.1f over priors, 500 islands each); establisher, incompatibility and pairwise-bridge tests at '
              'genotype level against the class tests on all %d incompatible genotype pairs: mismatches %s.' % (
                  lc['members_bad'], fe(max(lc['mass_err'].values())), max(lc['seed_z'].values()),
                  lc['genotype_incompatible_pairs'], lc['mismatches'] or '0'))
    md.append('')
    md += ['**The budget grid on the catalogue** (row program\'s play, column program\'s play; C = cooperates):', '',
           '| pair | 4 vs 4 | 4 vs 8 | 4 vs 16 | 8 vs 4 | 8 vs 8 | 8 vs 16 | 16 vs 4 | 16 vs 8 | 16 vs 16 |', '|---|' + '---|' * 9]
    seen = []
    for k in S['named']:
        s1, s2 = k.split(' vs ')
        key = (s1.rsplit('@', 1)[0], s2.rsplit('@', 1)[0])
        if key not in seen: seen.append(key)
    for s1, s2 in seen:
        row = ['`%s` vs `%s`' % (s1, s2)]
        for bx in (4, 8, 16):
            for by in (4, 8, 16):
                row.append(S['named']['%s@%d vs %s@%d' % (s1, bx, s2, by)])
        md.append('| ' + ' | '.join(row) + ' |')
    md.append('')
    md += ['**Induced class tables** (classes of positive mass; establisher = self-cooperates, defects on D, not all-C):', '',
           '| prior (b = 4, 8, 16) | classes | establishers | establisher μ (cut) [raw] | establisher μ by budget 4 / 8 / 16 |',
           '|---|---|---|---|---|']
    for p in ('cheap', 'uniform', 'above', 'h4', 'h8', 'h16'):
        c = S['classes'][p]
        md.append('| %s %s | %d | %d | %.4f [%.4f] | %s |' % (PRLAB[p], pr_fmt(p), c['K_pos'], c['est_n'], c['est_mu'], c['est_raw'],
                                                            ' / '.join('%.4f' % c['est_budget_mu'][str(b)] for b in B)))
    md.append('')
    md += ['## 2. Static screening: incompatible pairs of budgeted establishers', '',
           'Unit: an incompatible pair = two establisher classes of positive mass that mutually defect. Pairwise bridge = '
           'a cooperative class of positive mass under the prior mutually cooperating with both (exhaustive); structural '
           'bridge = any cooperative class of the catalogue; mediator path = shortest path in the establisher '
           'mutual-cooperation graph of the prior\'s support. Pair mass = product of the two class masses (cut); '
           'co-seeding = P(both on one island of N = 200), summed over pairs.', '',
           '| prior | establishers | components (sizes) | incompatible: n, mass [raw] | bridged: n, mass | **direct-bridge-less**: n, mass [raw], co-seed sum (max) | structurally bridge-less: n, mass | no path ≤ 3: n, mass | disconnected: n, mass | budget copies of one source: n (bridge-less n) |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for p in ('cheap', 'uniform', 'above', 'h4', 'h8', 'h16'):
        s = S['screen'][p]
        g = lambda k: s[k]
        md.append('| %s | %d | %d (%s) | %d, %s [%s] | %d, %s | **%d, %s** [%s], %.3g (%.3g) | %d, %s | %d, %s | %d, %s | %d (%d) |' % (
            PRLAB[p], s['est_n'], s['components'], ', '.join(map(str, s['comp_sizes'][:5])),
            g('incompatible')['n'], fe(g('incompatible')['mu']), fe(g('incompatible')['raw']),
            g('bridged')['n'], fe(g('bridged')['mu']),
            g('direct_bridgeless')['n'], fe(g('direct_bridgeless')['mu']), fe(g('direct_bridgeless')['raw']),
            g('direct_bridgeless')['coseed'], g('direct_bridgeless')['coseed_max'],
            g('direct_bridgeless_struct')['n'], fe(g('direct_bridgeless_struct')['mu']),
            g('no_path3')['n'], fe(g('no_path3')['mu']), g('disconnected')['n'], fe(g('disconnected')['mu']),
            g('budget_copy')['n'], g('budget_copy_bridgeless')['n']))
    ch, ab = S['screen']['cheap']['direct_bridgeless']['mu'], S['screen']['above']['direct_bridgeless']['mu']
    out['static_summary']['bl_ratio_cheap_above'] = ch / ab if ab else float('inf')
    md.append('')
    md.append('Direct-bridge-less pair mass, cheap-heavy / above-threshold: %s.' % (
        ('%.3g' % (ch / ab)) if ab else ('∞ (above-threshold has none; cheap-heavy %s)' % fe(ch))))
    # share of bridge-less mass involving BOX1@4
    for p in ('cheap', 'uniform'):
        s = S['screen'][p]
        allbl = s['pairs_bridgeless']
        b4 = sum(r['pair_mu'] for r in allbl if has_b1_4([r['a'], r['b']]))
        out['static_summary']['b14_share_' + p] = b4 / s['direct_bridgeless']['mu'] if s['direct_bridgeless']['mu'] else None
        md.append('Under %s, pairs with `BOX1(THEM(ME))`@4\'s class as a member carry %.3f of the direct-bridge-less mass '
                  '(over the %d heaviest bridge-less pairs listed).' % (PRLAB[p], out['static_summary']['b14_share_' + p] or 0, len(allbl)))
    md.append('')
    md += ['**Core programs: do their budget copies share an establisher component?** (component index per budget; "—" = not an establisher at that budget)', '',
           '| program | prior | b = 4 | b = 8 | b = 16 | 4–8 | 4–16 | 8–16 |', '|---|---|---|---|---|---|---|---|']
    for p in ('cheap', 'uniform', 'above'):
        for prog, row in S['screen'][p]['core'].items():
            cells_ = [('—' if row[str(b)]['comp'] is None else str(row[str(b)]['comp'])) for b in B]
            sh = row['share']
            md.append('| `%s` | %s | %s | %s | %s | %s |' % (prog, PRLAB[p], ' | '.join(cells_), 'yes' if sh['4-8'] else 'no',
                                                         'yes' if sh['4-16'] else 'no', 'yes' if sh['8-16'] else 'no'))
    md.append('')
    for p in ('cheap', 'above', 'uniform'):
        s = S['screen'][p]
        md += ['**Incompatible-pair list, %s** (heaviest direct-bridge-less pairs, then heaviest bridged pairs; budgets in class names; path = mediator path length, – = none):' % PRLAB[p], '',
               '| pair | pair mass | co-seed | bridges (n, mass, heaviest) | structural bridges | path | same component | budget copies of |', '|---|---|---|---|---|---|---|---|']
        for r in s['pairs_bridgeless'][:15] + s['pairs_bridged'][:10]:
            md.append('| `%s` × `%s` | %s | %.3g | %d, %s, %s | %d | %s | %s | %s |' % (
                r['a'], r['b'], fe(r['pair_mu']), r['coseed'], r['n_bridges'], fe(r['bridge_mu']),
                ('`%s`' % r['bridges_top'][0][0]) if r['bridges_top'] else '–', r['n_bridges_struct'],
                r['path'] if r['path'] is not None else '–', 'yes' if r['same_comp'] else 'no',
                ', '.join('`%s`' % x for x in r['budget_copies']) or '–'))
        md.append('')
    md += ['**Secondary: rivals of A₁₆ = {FairBot@16, `BOX1(THEM(ME))`@16}** (establishers of positive mass mutually defecting with either member):', '',
           '| prior | rivals | rival mass | direct-bridge-less mass (share) | heaviest rivals |', '|---|---|---|---|---|']
    for p in ('cheap', 'uniform', 'above'):
        r = S['a16'][p]
        md.append('| %s | %d | %s | %s (%s) | %s |' % (PRLAB[p], r['n'], fe(r['mu']), fe(r['bridgeless_mu']),
                                                    fe(r['bridgeless_share']), ', '.join('`%s` (%s, %d bridges)' % (x['name'], fe(x['mu']), x['n_bridges']) for x in r['rows'][:4])))
    md.append('')
    out['static'] = {p: {k: v for k, v in S['screen'][p].items() if k not in ('pairs_top',)} for p in S['screen']}
    out['static_a16'] = S['a16']
    return md


def lottery_md(cal, out):
    md = []
    groups = defaultdict(list)
    for exp in ('hom', 'nat', 'natcal', 'forced', 'scale'):
        for r in load(exp):
            groups[(exp, r['prior'], r['I'], r['mN'], r['gens'], r['cell'])].append(r)
    T = cal['T_nuc'] if cal else {}

    def xval(p, mN):
        return mN * T[p] / 200 if p in T else float('nan')
    # natural cells
    nat_keys = [k for k in groups if k[0] in ('hom', 'nat', 'natcal')]
    order = {'hom': 0, 'nat': 1, 'natcal': 2}
    pord = {'h4': 0, 'h8': 1, 'h16': 2, 'cheap': 3, 'uniform': 4, 'above': 5}
    nat_keys.sort(key=lambda k: (order[k[0]], pord.get(k[1], 9)))
    if nat_keys:
        md += ['## 4. Natural runs (N = 200, I = 64, horizon 10⁵): homogeneous controls, common mN, calibrated mN', '',
               '| cell | prior | mN | x = mN·T_nuc/N | runs | ever separated [95%] | **separated at the horizon** [95%] | with `BOX1(THEM(ME))`@4 | bridge-less (prior) / structural | budget copies | island P(C,C), certified (min) | run-level efficient | all-D runs | cf cross P(C,C): separated / all | worker-hours |',
               '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
        out['cells']['natural'] = {}
        for k in nat_keys:
            rs = sorted(groups[k], key=lambda r: r['rep'])
            st = nat_stats(rs)
            out['cells']['natural']['%s|%s|%g' % (k[0], k[1], k[3])] = st
            kd = st['kinds_end']
            md.append('| %s | %s | %.3f | %.3f | %d | %s | **%s** | %d | %d / %d | %d | %.4f (%.3f) | %.3f | %d | %s / %.3f | %.2f |' % (
                {'hom': 'homogeneous', 'nat': 'common mN', 'natcal': 'calibrated'}[k[0]], PRLAB[k[1]], k[3], xval(k[1], k[3]),
                st['n'], cps(st['ever'], st['n']), cps(st['end'], st['n']), st['b14_end'],
                kd.get('bridge-less (prior)', 0), kd.get('struct bridge-less', 0), kd.get('budget copies', 0),
                st['pcc_cert'], st['pcc_cert_min'], st['runlevel'], st['alld'], fe(st['cf_sep']), st['cf_all'], st['hours']))
        md.append('')
        # paired comparisons
        def get(e, p):
            for k in nat_keys:
                if k[0] == e and k[1] == p: return groups[k]
            return []
        pc = []
        for e1, p1, e2, p2 in (('nat', 'cheap', 'nat', 'above'), ('nat', 'cheap', 'nat', 'uniform'), ('nat', 'uniform', 'nat', 'above'),
                               ('nat', 'cheap', 'natcal', 'cheap'), ('hom', 'h4', 'nat', 'cheap')):
            A_, B_ = get(e1, p1), get(e2, p2)
            if A_ and B_:
                pr_ = paired(A_, B_, lambda r: r['n_sep_end'] > 0)
                pc.append('%s %s vs %s %s: %d common reps, both %d, first only %d, second only %d' % (
                    e1, PRLAB[p1], e2, PRLAB[p2], pr_['n'], pr_['both'], pr_['a_only'], pr_['b_only']))
                out.setdefault('paired', []).append(dict(a=[e1, p1], b=[e2, p2], **pr_))
        if pc:
            md += ['**Paired horizon separation** (same source seeds and budget uniforms): ' + '; '.join(pc) + '.', '']
        md += ['**Separated pairs at the horizon** (first listed pair of each separated run) and per-separation tracking:', '',
               '| cell | prior | heaviest separated pairs (runs) | first-separation fate | resolved / censored | resolution hazard per separated-run-generation [upper] | KM P(still separated) at 10² / 10³ / 10⁴ / 10⁵ after first separation |',
               '|---|---|---|---|---|---|---|']
        for k in nat_keys:
            st = out['cells']['natural']['%s|%s|%g' % (k[0], k[1], k[3])]
            if st['ever'] == 0:
                continue
            md.append('| %s | %s | %s | %s | %d / %d | %s [%s] | %s |' % (
                k[0], PRLAB[k[1]], '; '.join('`%s` %d' % (p_, c) for p_, c in list(st['pairs_end'].items())[:4]) or '–',
                ', '.join('%s %d' % (a_, b_) for a_, b_ in st['fate_first'].items()), st['resolved'], st['censored'],
                fe(st['hazard']), fe(st['hazard_upper']),
                ' / '.join('%.2f' % st['km'].get(str(m), float('nan')) for m in (100, 1000, 10000, 100000))))
        md.append('')
        md += ['**Budget composition of cooperative holders** (island-weighted, one vote per holding island, each vote the '
               'holder\'s expected budget composition on that island; first checkpoint = first check after every island '
               'is established, horizon = 10⁵ or the stop of a frozen run; TV against the prior over {4, 8, 16}; mean over '
               'runs with both checkpoints, bootstrap 95%):', '',
               '| cell | prior | runs with both | first checkpoint (median gen) | composition 4 / 8 / 16 at first | at horizon | TV first → horizon | ΔTV [95%] | mean budget first → horizon | Δ budget [95%] | unseparated runs: mean budget first → horizon |',
               '|---|---|---|---|---|---|---|---|---|---|---|']
        for k in nat_keys:
            st = out['cells']['natural']['%s|%s|%g' % (k[0], k[1], k[3])]
            c = st['comp']
            if not c.get('n_both'):
                continue
            u = c.get('unsep', {})
            md.append('| %s | %s | %d | %.0f | %s | %s | %.3f → %.3f | %+.3f [%+.3f, %+.3f] | %.2f → %.2f | %+.2f [%+.2f, %+.2f] | %s |' % (
                k[0], PRLAB[k[1]], c['n_both'], c['snap_gen_median'], ' / '.join('%.3f' % x for x in c['snap']),
                ' / '.join('%.3f' % x for x in c['end']), c['tv_snap'], c['tv_end'], c['dtv'], c['dtv_ci'][0], c['dtv_ci'][1],
                c['bud_snap'], c['bud_end'], c['dbud'], c['dbud_ci'][0], c['dbud_ci'][1],
                ('%.2f → %.2f (%d)' % (u['bud_snap'], u['bud_end'], u['n'])) if u else '–'))
        md.append('')
    fk = sorted([k for k in groups if k[0] in ('forced', 'scale')], key=lambda k: (k[0], str(k[5]), k[2], k[4]))
    if fk:
        md += ['## 5. Forced cells (cheap-heavy background, common mN; founders on disjoint island halves)', '',
               '| cell | I | horizon | forced pair | runs | X / Y network established | both established | **separated at the horizon (tags)** [95%] | given both | losses / exposure (minority-island-generations), hazard [upper] | mediation-before-loss (given both) | bridge classes in support, seed islands | separated with bridge alive / dead | island P(C,C) cert | run-level efficient | cf cross (separated) | worker-hours |',
               '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
        out['cells']['forced'] = {}
        for k in fk:
            rs = groups[k]
            st = forced_stats(rs)
            out['cells']['forced']['%s|%s|%d|%d' % (k[0], k[5], k[2], k[4])] = st
            lab = {'bl': 'bridge-less pair', 'br': 'bridged pair, bridges present', 'brabs': 'bridged pair, bridges removed',
                   'dctl': 'inert-defector control', None: 'iid control'}[k[5]]
            if k[5] in ('bl', 'br', 'brabs'):
                md.append('| %s | %d | %d | `%s` × `%s` | %d | %d / %d | %d | **%s** | %s | %d / %s, %s [%s] | %s | %.1f, %.1f | %d of %d / %d of %d | %.4f | %.3f | %s | %.2f |' % (
                    lab, k[2], k[4], st['forced'][0], st['forced'][1], st['n'], st['x_est'], st['y_est'], st['both_est'],
                    cps(st['sep_tag_end'], st['n'], 2), cps(st['sep_tag_end_given_both'], st['both_est'], 2),
                    st['losses'], fe(st['expo']), fe(st['hazard']), fe(st['hazard_upper']),
                    cps(st['med_before'], st['both_est'], 2), st['bridge_classes'], st['bridge_seed_islands'],
                    st['sep_bridge_alive'], st['n_bridge_alive'], st['sep_bridge_dead'], st['n'] - st['n_bridge_alive'],
                    st['pcc_cert'], st['runlevel'], fe(st['cf_sep']), st['hours']))
            else:
                md.append('| %s | %d | %d | %s | %d | – | – | %s (any incompatible holders) | – | – | – | – | – | %.4f | %.3f | – | %.2f |' % (
                    lab, k[2], k[4], 'D on both halves' if k[5] == 'dctl' else 'none', st['n'], cps(st['end'], st['n'], 2),
                    st['pcc_cert'], st['runlevel'], st['hours']))
        md.append('')
        md.append('Local establishments per run (q-style nucleation count, islands whose holder at establishment was ≥ ½ local): ' + '; '.join(
            '%s %s %.1f' % (k[0], k[5], out['cells']['forced']['%s|%s|%d|%d' % (k[0], k[5], k[2], k[4])]['n_loc_est']) for k in fk) + '.')
        md.append('')
    return md


def kcheck_main(a):
    """_kern_mb against rival_islands._kern (kprop = 1) on the same inputs: identical trajectories (counts, traces,
    establishment times, separation records); composition rows sum to 1 on present classes; a class whose members
    all carry one budget keeps that budget exactly."""
    import rival_islands as R_
    Bs = tuple(a.budgets)
    d = catalogue(Bs)
    out = []
    for rep in range(a.reps):
        for N, I, mN, gens in ((60, 8, 1.0, 3000), (200, 16, 1.091, 2000)):
            gc = build_seed(d, tuple(1 / len(Bs) for _ in Bs), N, I, rep)
            init, comp0 = lump_seed(d, gc)
            ext = np.nonzero(init.sum(0) > 0)[0]
            Vs = d['V'][np.ix_(ext, ext)].astype(np.int64)
            U = np.ascontiguousarray(PDP[Vs, Vs.T]); PCC = np.ascontiguousarray((Vs * Vs.T).astype(float))
            coop = d['coop'][ext].copy(); tag = np.zeros(len(ext), np.int64)
            li = np.ascontiguousarray(init[:, ext]); c0 = np.ascontiguousarray(comp0[:, ext, :])
            K = len(ext); rr = np.random.default_rng(rep); r1 = rr.random(K); r2 = rr.random(K)
            iDl = int(np.nonzero(ext == d['iD'])[0][0]) if (ext == d['iD']).any() else -1
            ch = R_.checks_schedule(gens)
            o1 = R_._kern(U, PCC, coop, tag, li, N, W, mN / N, 1000 + rep, ch, True, iDl, r1, r2, np.zeros(I, np.int64), 1)
            o2 = _kern_mb(U, PCC, coop, tag, li, c0, N, W, mN / N, 1000 + rep, ch, True, iDl, r1, r2, np.zeros(I, np.int64))
            same = all(np.array_equal(np.asarray(x), np.asarray(y)) for x, y in zip(o1, o2[:len(o1)]))
            counts, comp = o2[2], o2[-5]
            pres = counts > 0
            rowsum = comp.sum(2)[pres]
            pure = np.array([len(set(d['bidx'][g] for g in d['members'][int(k)])) == 1 for k in ext])
            purity = []
            for k in np.nonzero(pure)[0]:
                bslot = d['bidx'][d['members'][int(ext[k])][0]]
                for i in range(I):
                    if counts[i, k] > 0 and o2[8][k] == k:      # not merged into another class
                        purity.append(abs(comp[i, k, bslot] - 1.0))
            out.append(dict(rep=rep, N=N, I=I, identical=bool(same), rowsum_err=float(np.abs(rowsum - 1).max()) if len(rowsum) else 0.0,
                            purity_err=float(max(purity)) if purity else 0.0, status=int(o2[0]), stop=int(o2[1]),
                            snap_gen=int(o2[-4]), merged=int((o2[8] != np.arange(K)).sum())))
            print(out[-1], flush=True)
    json.dump(out, open(os.path.join(RUNS, 'mixed-budgets', 'kcheck.json'), 'w'), indent=1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--budgets', type=int, nargs='+', default=list(B))
    ap.add_argument('--exp', default='nat')
    ap.add_argument('--priors', nargs='+', default=['cheap', 'above'])
    ap.add_argument('--cells', nargs='+', default=['bl'])
    ap.add_argument('--reps', type=int, default=3000)
    ap.add_argument('--rep', type=int, default=0)
    a = ap.parse_args()
    {'cross': cmd_cross, 'static': static_main, 'run': run_main, 'calib': calib_main, 'timing': timing_main,
     'kcheck': kcheck_main, 'report': report_main}[a.what](a)
