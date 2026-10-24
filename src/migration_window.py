"""A migration window for stable sets on islands (notes/migration-window.md).

Runs the stable-sets lottery (baseline), U-gKR(0.99) and gV on archipelagos made of one or several independent
components (complete migration inside a component, none between), with per-generation records of every island's modal
outcome, and computes the target statistics.  Kernels come from migration_window_kernels.py (generated copies of
stable_sets.kern and farsighted_refusal.fkern with extra records; draw-for-draw identical to the originals).

Importable without side effects; the drivers are in migration_window_run.py.
"""
import json, os, sys, time, zlib, resource
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stable_sets as SS
import stable_sets_run as SR
import dollar3 as D
import dominance_contracts as DC
import dominance_contracts_run as DR
import farsighted_refusal as F
import farsighted_refusal_run as FR
import migration_window_kernels as MK

ROOT = SS.ROOT
OUT = os.path.join(ROOT, 'runs', 'migration_window')
HELD = 25
SNAPS = (0, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000)
GRID = 50
NU = 0.1

T = DR.tables()
X = T.R
NOUT = len(X)
V = sorted(SS.symmetric_set(X, 6))                 # outcome ids of the three fair pairs
CATLAB = ['F', 'U', 'G', 'W', 'D']                 # fair, unequal, grand, wasteful, disagreement


def _cat(k):
    c = T.cat[k]
    if c == 'fair': return 0
    if c == 'unequal': return 1
    if c.startswith('grand'): return 2 if sum(X[k]) == 6 else 3
    if c == 'wasteful': return 3
    return 4


CATMAP = np.array([_cat(k) for k in range(NOUT)], np.int8)
OLAB = []
for _k in range(NOUT):
    _c = int(CATMAP[_k])
    OLAB.append(('F%d' % V.index(_k)) if _c == 0 else CATLAB[_c])
MEMIDX = {v: i for i, v in enumerate(V)}


# ---------------------------------------------------------------- the reference formula (unit-tested)
def p_all_three(C):
    """P(all three fair pairs present) if each of C components independently settles on a uniform fair pair."""
    return 1 - 3 * (2 / 3) ** C + 3 * (1 / 3) ** C


# ---------------------------------------------------------------- founders
def founders(base, r, Itot, N):
    rng = np.random.default_rng(SR.run_seed(base, r))
    laws = [SS.seed_law('L', s) for s in range(3)]
    return SS.draw_seeds(rng, Itot, N, laws), rng


def control_founders(kind, base, r, I, N):
    """kind 'bal': every island on one fair pair, the three in equal numbers (I a multiple of 3), no waste;
    'waste': a quarter of the islands (I a multiple of 12) on a wasteful pair (both name each other at 1/3), the rest
    on the fair pairs in equal numbers.  The excluded slot of an island is drawn from the length prior (as in the
    stable-sets forced-entry cells); the two pair slots are the constant programs, so the island's outcome is exactly
    the seeded one."""
    init, rng = founders(base + '|' + kind, r, I, N)
    S, mu = SS.arm_data('weak')
    ci = SS.const_index(S.fs)
    lo = D.local_of
    pairs = ((0, 1), (0, 2), (1, 2))
    k = 0
    for i in range(I):
        if kind == 'bal':
            p = i % 3; dem = 1
        else:
            if i % 4 == 3:
                p = (i // 4) % 3; dem = 0            # wasteful (2, 2)
            else:
                p = k % 3; k += 1; dem = 1
        a, b = pairs[p]
        for (s, o) in ((a, b), (b, a)):
            init[i, s] = 0; init[i, s, ci[lo(s, o, dem)]] = N
    return init


# ---------------------------------------------------------------- one component
def run_comp(guard, init_sub, N, mN, seed, H):
    """returns dict(cls, modal, effm, fairm, status, stop, nmig, nev, cnt)."""
    loc, U = SS.compress(init_sub)
    hrec = np.zeros(0, np.int64)
    if guard == 'base':
        J = SS.joint_for('weak', U)
        out = MK.kern_mw(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, N, SS.W, mN / N, seed, H, 10, hrec, 1000)
        status, stop, counts, cls, eff, dist, ev, nev, nmig, modal, effm, fairm = out
        return dict(cls=cls, modal=modal, effm=effm, fairm=fairm, status=int(status), stop=int(stop), nmig=int(nmig),
                    nev=int(nev), cnt=None)
    names = {'gKR': ['g0', 'gKR0.99'], 'gV': ['g0', 'gV']}[guard]
    st = F.Setup(loc, U, len(names), assign=('bit', 1.0, 1), rng=None)
    ga = FR.guard_arrays(names)
    out = run_fkern_mw(st, N, mN, seed, H, hrec, ga)
    return out


def run_fkern_mw(setup, N, mN, seed, H, hrec, guards, nu=NU, rec_every=50):
    CS, CD, CACT = F.CS_, F.CD_, F.CACT_
    res, modal, effm, fairm = MK.fkern_mw(setup.J, T.PAY, T.VEC, T.ISMEM, T.TOT, setup.tc0, setup.TK, setup.TO, setup.TG,
                                          setup.TPC, setup.TMAP, setup.ntypes, setup.Kmax, setup.NG, N, SS.W, mN / N,
                                          seed, H, 10, np.asarray(hrec, np.int64), float(nu), CS, CD, CACT, F.CX,
                                          guards['GKIND'], guards['GTAB'], guards['KRTAB'], F.PROPM, F.UPAY,
                                          float(guards['rdelta']), False, rec_every, 1000, 1000)
    status, stop, tcount, cls, eff, dist, ev, nev, nmig, cev, ncev, cnt, gfreq, refby, nsolve, pcount = res
    return dict(cls=cls, modal=modal, effm=effm, fairm=fairm, status=int(status), stop=int(stop), nmig=int(nmig),
                nev=int(nev), cnt=[int(v) for v in cnt.sum(0)], ncev=int(ncev),
                gfreq=gfreq[::max(1, 500 // rec_every)].mean(axis=(1, 2)).astype(np.float32))


# ---------------------------------------------------------------- one archipelago
def comp_seed(base, r, c, size, single):
    if single:
        return SR.run_seed(base, r) % (2 ** 31)
    return SR.run_seed('%s|comp%d|size%d' % (base, c, size), r) % (2 ** 31)


def run_archipelago(spec, r):
    """spec: dict(guard, N, mN, H, base, sizes (list of component sizes), start in {'lottery', 'bal', 'waste'}).
    Returns (arrays dict, per-component slices, totals)."""
    N = spec['N']; H = spec['H']; sizes = spec['sizes']; Itot = sum(sizes)
    if spec.get('start', 'lottery') == 'lottery':
        init, _ = founders(spec['base'], r, Itot, N)
    else:
        init = control_founders(spec['start'], spec['base'], r, Itot, N)
    parts = []; slices = []; a = 0
    single = len(sizes) == 1
    for c, sz in enumerate(sizes):
        seed = comp_seed(spec['base'], r, c, sz, single)
        o = run_comp(spec['guard'], init[a:a + sz], N, spec['mN'], seed, H)
        parts.append(o); slices.append((a, a + sz)); a += sz
    arr = {k: np.concatenate([p[k] for p in parts], axis=1) for k in ('cls', 'modal', 'effm', 'fairm')}
    meta = dict(status=[p['status'] for p in parts], stop=[p['stop'] for p in parts], nmig=sum(p['nmig'] for p in parts),
                nev=sum(p['nev'] for p in parts))
    if parts[0].get('cnt') is not None:
        meta['cnt'] = [sum(p['cnt'][j] for p in parts) for j in range(len(parts[0]['cnt']))]
        meta['gfreq'] = np.mean([p['gfreq'] for p in parts], axis=0)[:, 1].round(4).tolist()
    return arr, slices, meta


# ---------------------------------------------------------------- statistics
def first_window(arr, L=HELD, start=0):
    """first g >= start with arr[g:g+L] all True (window inside the horizon), else -1."""
    n = len(arr)
    if n - start < L:
        return -1
    c = np.concatenate([[0], np.cumsum(arr.astype(np.int64))])
    win = c[L:] - c[:-L]                      # win[g] = sum arr[g:g+L]
    idx = np.nonzero(win[start:] == L)[0]
    return int(idx[0] + start) if len(idx) else -1


def episodes(ind):
    """maximal True runs of a boolean series: list of (start, length)."""
    x = np.concatenate([[0], ind.astype(np.int8), [0]])
    d = np.diff(x)
    st = np.nonzero(d == 1)[0]; en = np.nonzero(d == -1)[0]
    return [(int(a), int(b - a)) for a, b in zip(st, en)]


def target_series(modal, effm, fairm, cat=None):
    """per-generation target indicators for the islands in the given columns (all arrays (G+1, I))."""
    if cat is None:
        cat = CATMAP[modal]
    I = modal.shape[1]
    nf = (cat == 0).sum(1)
    nm = np.zeros(modal.shape[0], np.int64)
    for v in V:
        nm += (modal == v).any(1)
    waste = ((cat == 3) | (cat == 4)).sum(1)
    ts = (waste == 0) & (nm == 3)
    tv = (nf == I) & (nm == 3)
    hps = (effm.min(1) >= 0.95) & (nm == 3)
    hpv = (fairm.min(1) >= 0.95) & (nm == 3)
    return dict(ts=ts, tv=tv, hps=hps, hpv=hpv, nm=nm, waste=waste, nf=nf, cat=cat)


def analyse(arr, slices, meta, H, collect_grid=False):
    modal = arr['modal']; effm = arr['effm']; fairm = arr['fairm']; cls = arr['cls']
    G1, I = modal.shape
    cat = CATMAP[modal]
    ser = target_series(modal, effm, fairm, cat)
    ts, tv, hps, hpv, nm, waste, nf = (ser[k] for k in ('ts', 'tv', 'hps', 'hpv', 'nm', 'waste', 'nf'))
    nu_ = (cat == 1).sum(1); ng_ = (cat == 2).sum(1); nw_ = (cat == 3).sum(1); nd_ = (cat == 4).sum(1)
    inef = 1.0 - effm.mean(1)
    rec = dict(I=int(I))
    # snapshots
    snaps = {}
    Vset = np.array(V)
    for g in SNAPS:
        if g > H:
            continue
        mg = modal[g]
        snaps[str(g)] = dict(ts=int(ts[g]), tv=int(tv[g]), hps=int(hps[g]), hpv=int(hpv[g]), nm=int(nm[g]),
                             F=int(nf[g]), U=int(nu_[g]), G=int(ng_[g]), W=int(nw_[g]), D=int(nd_[g]),
                             inef=round(float(inef[g]), 5), cons=int((mg == mg[0]).all()),
                             occ=round(float(np.isin(cls[g], Vset).mean()), 4),
                             pres=[int((mg == v).any()) for v in V])
        if g in (2000, 10000, 20000):
            u_, c_ = np.unique(mg, return_counts=True)
            snaps[str(g)]['labels'] = {T.labels[int(k)]: int(c) for k, c in zip(u_, c_)}
    rec['snap'] = snaps
    # passage times
    wf = waste == 0
    t_clear = first_window(wf)
    cov3 = nm == 3
    g_est = int(np.argmax(cov3)) if cov3.any() else -1
    t_lost = first_window(~cov3, start=g_est) if g_est >= 0 else -1
    last_waste = int(np.nonzero(waste > 0)[0][-1]) if (waste > 0).any() else -1
    rec.update(t_clear=t_clear, g_est=g_est, t_lost=t_lost, last_waste=last_waste,
               waste0=int(waste[0]), nm0=int(nm[0]))
    # target episodes
    for name, s in (('ts', ts), ('tv', tv), ('hps', hps), ('hpv', hpv)):
        eps = episodes(s)
        L = [l for _, l in eps]
        rec['ep_' + name] = dict(first=int(eps[0][0]) if eps else -1, n=len(eps), n25=int(sum(1 for l in L if l >= HELD)),
                                 cum=int(sum(L)), longest=int(max(L)) if L else 0,
                                 first25=next((int(a) for a, l in eps if l >= HELD), -1),
                                 final=int(bool(s[-1])))
    rec['mean_inef'] = round(float(inef.mean()), 5)
    rec['cum_ineff_mass_gens'] = round(float(inef.sum()), 2)
    # components
    comps = []
    for (a, b) in slices:
        m = modal[:, a:b]
        same = (m == m[:, :1]).all(1)
        c = dict(size=b - a, cons_first=first_window(same))
        for g in (0, 100, 1000, 10000, 20000):
            if g > H:
                continue
            mg = m[g]
            c['pres%d' % g] = int(sum(1 for v in V if (mg == v).any()))
            c['out%d' % g] = int(mg[0]) if (mg == mg[0]).all() else -1
            c['eff%d' % g] = int(((CATMAP[mg] <= 2)).all())
        comps.append(c)
    rec['comps'] = comps
    # transitions on the 50-generation grid (modal outcome class), colonization = destination present elsewhere
    gm = modal[::GRID]
    trans = {}
    comp_of = np.zeros(I, np.int64)
    for ci_, (a, b) in enumerate(slices):
        comp_of[a:b] = ci_
    for t in range(1, gm.shape[0]):
        prev = gm[t - 1]; cur = gm[t]
        ch = np.nonzero(prev != cur)[0]
        for i in ch:
            a, b = slices[comp_of[i]]
            col = bool((prev[a:b] == cur[i]).any())
            key = '%s>%s:%s' % (OLAB[prev[i]], OLAB[cur[i]], 'col' if col else 'loc')
            trans[key] = trans.get(key, 0) + 1
    rec['trans'] = trans
    rec['status'] = meta['status']; rec['stop'] = meta['stop']; rec['nmig'] = meta['nmig']; rec['nev'] = meta['nev']
    for k in ('cnt', 'gfreq'):
        if k in meta:
            rec[k] = meta[k]
    out = {}
    if collect_grid:
        out['grid'] = gm.astype(np.int8)
    return rec, out


def run_job(spec, r, prefixes=None):
    """one run of a cell; returns the record (analysis of the whole archipelago, plus the prefix archipelagos
    C = 1, 2, 4, 8 of 16-island components when `prefixes` is a list of C values)."""
    t0 = time.time()
    arr, slices, meta = run_archipelago(spec, r)
    wall1 = time.time() - t0
    H = spec['H']
    if prefixes:
        rec = {}
        for C in prefixes:
            a, b = slices[0][0], slices[C - 1][1]
            sub = {k: v[:, a:b] for k, v in arr.items()}
            mc = dict(meta); mc['status'] = meta['status'][:C]; mc['stop'] = meta['stop'][:C]
            rc, _ = analyse(sub, slices[:C], mc, H)
            rec['C%d' % C] = rc
        rec['meta'] = dict(nmig=meta['nmig'])
    else:
        rec, _ = analyse(arr, slices, meta, H)
    rec.update(run=r, wall=time.time() - t0, wall_kernel=wall1, rss_mb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6)
    return rec
