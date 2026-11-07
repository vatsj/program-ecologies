"""Majority division in the current object: seed lottery with the annealed tail, finite N, finite I, migration
(spec specs/2026-11-07-majority-current-object.md; notes notes/majority-current-object.md).

Arms: M (n <= 6 DSL, modalPA free sound box), L (same DSL, weak evaluator), T (27-program L_T^code library at the A_f
charge, P_fail = 0.1).  Variants: main, D1 (clean tail), D2 (clean founders and tail), D3 (clean founders, full tail),
D4:<d> (matched-mass random removals), T0 (constants only, arm T).

Pieces: arm descriptions and seed laws, the arm-independent tail schedule (the arrival process has its own random
stream), the per-run universe and joint table, the kernel wrapper (majority_tail_kern.kern_mt), the per-cell summary.
Importable without side effects; drivers are in majority_tail_run.py.
"""
import os, sys, time, zlib, math
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from numba import njit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dollar3 as D
import stable_sets as SS
import churn_primary as CP
import migration_window as MW
import majority_tail_kern as MK

W = SS.W
T = MW.T
V = np.array(MW.V)
ISFAIR = CP.ISFAIR
NOUT = MW.NOUT
CATMAP = MW.CATMAP
CLS = ['F', 'U', 'G', 'W', 'D']
PAIROF = -np.ones(NOUT, np.int64)
for _i, _v in enumerate(MW.V):
    PAIROF[_v] = _i                     # fair pair index 0..2 of an outcome id (-1 if not fair)
I_DEFAULT = 64
LAMS = (0, 10, 100)
MNS = (0, 0.1, 1)
PFAIL = 0.1
DEBOUNCE = 25


# ====================================================================== arms and laws
ARMS = {
    'M': dict(kind='dsl', cat='B6m', base='L1'),
    'L': dict(kind='dsl', cat='B6w', base='L1'),
    'T': dict(kind='t', cat='T-main', base='CP-T-main'),
}
_CACHE = {}


def geometry(N):
    g0 = 2 * N; t0 = N / 2.0; gend = 100 * N
    return dict(g0=g0, t0=t0, gend=gend, H=gend + 20 * N, Hlong=240 * N,
                snaps=(2 * N, 10 * N, 30 * N, 100 * N, 120 * N))


def _tabs(cache_dir=None):
    if 'tabs' not in _CACHE:
        import many_islands_t as MT
        _CACHE['tabs'] = MT.Tabs(cache_dir=cache_dir)
    return _CACHE['tabs']


def get_cat(arm, cache_dir=None):
    return CP.get_cat(ARMS[arm]['cat'], cache_dir)


# ---- the clean-tail identities of queue 71 (annealed_tail.tail_law, unequal_basin_run.family_mask), copied
def _features(S):
    feats = [[None] * len(S.fs) for _ in range(3)]
    for s in range(3):
        for x, f in enumerate(S.fs):
            atoms, tab = f
            if len(atoms) == 0:
                continue
            (L, jr, al) = atoms[0]
            j = D.others(s)[jr]
            pa = D.partner_abs(j, al)
            tgt = 'all' if pa == D.ALL else ('self' if pa == s else 'third')
            bt = D.partner_abs(s, tab[1]); bf = D.partner_abs(s, tab[0])
            feats[s][x] = dict(j=j, atom_tgt=tgt, atom_d=al % 3, t_tgt=('all' if bt == D.ALL else ('j' if bt == j else 'k')),
                               t_d=tab[1] % 3, f_tgt=('all' if bf == D.ALL else ('j' if bf == j else 'k')), f_d=tab[0] % 3)
    return feats


def dsl_family_data(S):
    """per slot and class: family code (FAMS_DSL), the victim mask (pair-naming constants at 1/3) and the bully mask."""
    key = ('fam', id(S))
    if key in _CACHE:
        return _CACHE[key]
    feats = _features(S)
    K = len(S.fs)
    fam = np.zeros((3, K), np.int64); vic = np.zeros((3, K), bool); bul = np.zeros((3, K), bool)
    for s in range(3):
        for x in range(K):
            atoms, tab = S.fs[x]
            if len(atoms) == 0:
                l = int(tab[0])
                if D.partner_abs(s, l) == D.ALL:
                    fam[s, x] = 3
                else:
                    fam[s, x] = l % 3
                    vic[s, x] = (l % 3 == 0)
                continue
            f = feats[s][x]
            if (f['atom_tgt'] == 'self' and f['atom_d'] == 0 and f['t_tgt'] == 'j' and f['t_d'] == 2
                    and f['f_tgt'] == 'k' and f['f_d'] == 1):
                fam[s, x] = 4; bul[s, x] = True
            elif f['atom_tgt'] == 'self' and f['atom_d'] == 0 and f['t_tgt'] == 'j' and f['t_d'] == 2:
                fam[s, x] = 5
            elif f['atom_tgt'] == 'self' and f['atom_d'] == 2 and f['t_tgt'] == 'j' and f['t_d'] == 0:
                fam[s, x] = 6
            elif f['atom_tgt'] == 'self' and f['atom_d'] == 1 and f['t_tgt'] == 'j' and f['t_d'] == 1:
                fam[s, x] = 7
            else:
                fam[s, x] = 8
    _CACHE[key] = (fam, vic, bul)
    return _CACHE[key]


FAMS_DSL = ['c_third', 'c_half', 'c_two3', 'c_grand', 'bully', 'exploiter', 'yielder', 'fair_reader', 'other_cond']
FAMS_T = ['c_third', 'c_half', 'c_two3', 'c_grand', 'single', 'two', 'exploit']


def family_table(arm):
    """(names, fam) with fam (3, Kglobal) integer family codes of every program of the arm's catalogue."""
    if ARMS[arm]['kind'] == 'dsl':
        cat = get_cat(arm)
        fam, _, _ = dsl_family_data(cat.S)
        return FAMS_DSL, fam
    tabs = _tabs()
    f = np.zeros(27, np.int64)
    for p in range(27):
        fm = tabs.fam[p]
        if fm == 'const':
            a = int(tabs.names[p][1:])
            f[p] = 3 if a // 3 == 2 else a % 3
        else:
            f[p] = {'single': 4, 'two': 5, 'exploit': 6}[fm]
    return FAMS_T, np.tile(f, (3, 1))


def base_laws(arm, cache_dir=None):
    """the arm's seed law per slot over its catalogue (length 1,305 for the DSL, 31 incl. four stubs for T)."""
    cat = get_cat(arm, cache_dir)
    return [CP.cat_law(cat, s) for s in range(3)]


def clean_mask(arm):
    cat = get_cat(arm)
    _, vic, bul = dsl_family_data(cat.S)
    return vic | bul


def renorm(p):
    return p / p.sum()


def variant_laws(arm, variant, cache_dir=None):
    """(founding laws, tail laws), each a list of three vectors.  The founding law of D2/D3 and the tail law of D1/D2
    have the clean mask removed and renormalized; D4:<d> removes random classes of the same total prior mass."""
    base = base_laws(arm, cache_dir)
    if variant in ('main',):
        return base, base
    if variant == 'T0':
        assert arm == 'T'
        tabs = _tabs(cache_dir)
        import many_islands_t as MT
        w = np.zeros(len(base[0]))
        w[:27] = MT.seed_law(tabs, '0')
        return [w.copy() for _ in range(3)], [w.copy() for _ in range(3)]
    assert ARMS[arm]['kind'] == 'dsl', variant
    if variant.startswith('D4'):
        d = int(variant.split(':')[1])
        cm = clean_mask(arm)
        out = []
        for s in range(3):
            p = base[s]
            target = float(p[cm[s]].sum())
            rng = np.random.default_rng(zlib.crc32(('majtail|D4|%d|%d' % (d, s)).encode()))
            cand = np.nonzero(~cm[s] & (p > 0))[0]
            best = None
            for _try in range(5000):              # random order, a class that would overshoot is skipped; first draw within 0.003
                order = rng.permutation(cand)
                q = p.copy(); acc = 0.0
                for x in order:
                    if acc + p[x] <= target + 0.003:
                        q[x] = 0.0; acc += p[x]
                        if abs(target - acc) < 0.003:
                            break
                if best is None or abs(target - acc) < best[0]:
                    best = (abs(target - acc), q)
                if best[0] < 0.003:
                    break
            q = best[1]
            out.append(renorm(q))
        return out, out
    cm = clean_mask(arm)
    clean = [renorm(np.where(cm[s], 0.0, base[s])) for s in range(3)]
    if variant == 'D1':
        return base, clean
    if variant == 'D2':
        return clean, clean
    if variant == 'D3':
        return clean, base
    raise ValueError(variant)


# ====================================================================== founders, schedule, universe
def founders(laws, base, r, I, N):
    """init counts (I, 3, K) from the stored-baseline generator (CP.founders), with laws given."""
    rng = np.random.default_rng(SS_run_seed(base, r))
    return SS.draw_seeds(rng, I, N, laws), SS_run_seed(base, r) % (2 ** 31)


def SS_run_seed(base, r):
    import stable_sets_run as SR
    return SR.run_seed(base, r)


def _seed_int(*parts):
    return zlib.crc32(('majority-tail|' + '|'.join(str(p) for p in parts)).encode()) & 0x7fffffff


def tail_mean(N, g0, t0, gend, Lam):
    gs = np.arange(g0, gend)
    return gs, Lam * (1.0 / (1.0 + (gs - g0) / t0) - 1.0 / (1.0 + (gs + 1 - g0) / t0))


def make_schedule(N, r, I, Lmax=100.0):
    """Arrival schedule for Lmax, arm-independent (its own stream seeded by (N, r)): arrays g, island, slot, victim
    uniform, thinning uniform, program uniform.  Lam < Lmax thins (nested)."""
    geo = geometry(N)
    rng = np.random.default_rng(_seed_int('T', N, r))
    gs, mean = tail_mean(N, geo['g0'], geo['t0'], geo['gend'], Lmax)
    cnt = rng.poisson(mean[:, None], size=(len(gs), I))
    gi, ii = np.nonzero(cnt)
    rep = cnt[gi, ii]
    ag = np.repeat(gs[gi], rep).astype(np.int64); ai = np.repeat(ii, rep).astype(np.int64)
    n = len(ag)
    asl = rng.integers(0, 3, n).astype(np.int64); au = rng.random(n); thin = rng.random(n); up = rng.random(n)
    return dict(g=ag, i=ai, s=asl, u=au, thin=thin, up=up, Lmax=Lmax)


def map_programs(sched, tail_laws, lam):
    """arrivals of the schedule thinned to lam, with programs drawn from each arrival's slot tail law by inverse CDF."""
    keep = sched['thin'] < lam / sched['Lmax']
    g = sched['g'][keep]; i = sched['i'][keep]; s = sched['s'][keep]; u = sched['u'][keep]; up = sched['up'][keep]
    k = np.zeros(len(g), np.int64)
    for sl in range(3):
        cdf = np.cumsum(tail_laws[sl] / tail_laws[sl].sum())
        sel = s == sl
        k[sel] = np.minimum(np.searchsorted(cdf, up[sel], side='right'), len(cdf) - 1)
    return g, i, s, u, k


@njit(cache=True)
def _joint16(armi, nat, atL, atJ, atA, tab, PARTNER, U0, U1, U2):
    K0, K1, K2 = U0.shape[0], U1.shape[0], U2.shape[0]
    J = np.empty((K0, K1, K2), np.int16)
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64); u = np.empty(3, np.int64)
    for a in range(K0):
        for b in range(K1):
            for c in range(K2):
                D.enc_into(armi, nat, atL, atJ, atA, tab, PARTNER, U0[a], U1[b], U2[c], hist, val, u)
                J[a, b, c] = val[0] * 81 + val[1] * 9 + val[2]
    return J


def build_universe(arm, init, sched_tail):
    """per-slot sorted universe of catalogue ids (founders and the scheduled arrivals), local founder counts."""
    I = init.shape[0]
    kind = ARMS[arm]['kind']
    if kind == 't':
        init = init[:, :, :27]
        U = [np.arange(27, dtype=np.int64) for _ in range(3)]
        return U, init.astype(np.int64)
    ag, ai, asl, au, ak = sched_tail if sched_tail is not None else (None,) * 5
    U = []
    for s in range(3):
        ids = set(np.nonzero(init[:, s, :].sum(0))[0].tolist())
        if ak is not None:
            ids |= set(np.unique(ak[asl == s]).tolist())
        U.append(np.array(sorted(ids), np.int64))
    Kmax = max(len(u) for u in U)
    loc = np.zeros((I, 3, Kmax), np.int64)
    for s in range(3):
        loc[:, s, :len(U[s])] = init[:, s, U[s]]
    return U, loc


def build_tables(arm, U, cache_dir=None):
    """J (local joint table), PAY, VEC, ISMEM, TOT for the universe U."""
    if ARMS[arm]['kind'] == 'dsl':
        cat = get_cat(arm, cache_dir)
        Kmax = max(len(u) for u in U)
        Up = [np.concatenate([u, np.full(Kmax - len(u), u[0])]).astype(np.int64) for u in U]
        S = cat.S
        J = _joint16(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, Up[0], Up[1], Up[2])
        return J, T.PAY, T.VEC, T.ISMEM, T.TOT
    tabs = _tabs(cache_dir)
    return t_charged_tables(tabs, PFAIL)


def t_charged_tables(tabs, pfail):
    """arm T under A_f: J holds type ids of (outcome code, the three net payoffs); PAY[type] the net payoffs; VEC[type]
    the outcome id.  Programs with equal outcome and payoffs against a given pair play identically (closure)."""
    net = tabs.payoff(pfail, pfail)                  # (27,27,27,3) dollars
    code = tabs.JT                                   # (27,27,27) joint code
    key = np.concatenate([code[..., None].astype(np.float64), np.round(net, 12)], axis=-1).reshape(-1, 4)
    uk, inv = np.unique(key, axis=0, return_inverse=True)
    PAY = uk[:, 1:4].copy()
    VEC = T.VEC[uk[:, 0].astype(np.int64)]
    J = inv.reshape(27, 27, 27).astype(np.int32)
    return J, PAY, VEC.astype(np.int64), T.ISMEM, T.TOT


# ====================================================================== one run
def prepare(arm, variant, N, r, I=I_DEFAULT, Lmax=100.0, cache_dir=None):
    fl, tl = variant_laws(arm, variant, cache_dir)
    base = ARMS[arm]['base']
    init, seed = founders(fl, base, r, I, N)
    sched = make_schedule(N, r, I, Lmax)
    st = map_programs(sched, tl, Lmax)
    U, loc = build_universe(arm, init, st)
    J, PAY, VEC, ISMEM, TOT = build_tables(arm, U, cache_dir)
    return dict(arm=arm, variant=variant, N=N, r=r, I=I, init=init, seed=seed, sched=sched, tail_laws=tl, U=U, loc=loc,
                J=J, PAY=PAY, VEC=VEC, ISMEM=ISMEM, TOT=TOT, geo=geometry(N))


def local_arrivals(prep, lam):
    if lam <= 0:
        z = np.zeros(0, np.int64)
        return z, z, z, np.zeros(0), z
    ag, ai, asl, au, ak = map_programs(prep['sched'], prep['tail_laws'], lam)
    lk = np.zeros(len(ak), np.int64)
    for s in range(3):
        sel = asl == s
        lk[sel] = np.searchsorted(prep['U'][s], ak[sel])
        assert (prep['U'][s][lk[sel]] == ak[sel]).all()
    return ag, ai, asl, au, lk


def run_kernel(prep, lam, mN, H, snapg, xcap=400000, acap=40000):
    ag, ai, asl, au, lk = local_arrivals(prep, lam)
    N = prep['N']
    out = MK.kern_mt(prep['J'], prep['PAY'], prep['VEC'], prep['ISMEM'], prep['TOT'], prep['loc'], N, W, mN / N,
                     prep['seed'], H, 10, np.asarray(snapg, np.int64), ag, ai, asl, au, lk, xcap, acap)
    keys = ('status', 'stop', 'counts', 'modal', 'majo', 'snapc', 'snapd', 'xlog', 'nx', 'alog', 'na', 'nmig')
    res = dict(zip(keys, out))
    res['arr'] = (ag, ai, asl, au, lk)
    return res


# ====================================================================== statistics
def flips_series(series, L):
    return CP.flips(series, L)


def class_of(ids):
    return CATMAP[ids]


def transitions(series_ids, lo, hi, L):
    """debounced island-level transitions of the modal outcome in generations [lo, hi]: 5x5 class counts, fair-to-fair
    pair flips, exposure (island-generations).  The debounce is applied to the whole series (the state at lo is the
    value just before the window)."""
    cls = CATMAP[series_ids].astype(np.int64)
    Gp, I = cls.shape
    fc = CP.flips(cls, L)
    fi = CP.flips(series_ids.astype(np.int64), L)
    M = np.zeros((5, 5), np.int64)
    for ch in fc:
        for g, a, b in ch:
            if lo <= g <= hi:
                M[a, b] += 1
    ff = 0; fn = 0
    for ch in fi:
        for g, a, b in ch:
            if lo <= g <= hi and ISFAIR[a] and ISFAIR[b]:
                ff += 1
    # occupancy of each class (island-generations) for rates
    occ = np.array([(cls[lo:hi + 1] == c).sum() for c in range(5)], np.int64)
    return dict(M=M.tolist(), ff=int(ff), occ=occ.tolist(), expo=int(I * (hi - lo + 1)), L=int(L))


def snap_stats(snapc, snapd, modal, majo, si, g, fam, U):
    """measurements at snapshot si (generation g)."""
    I = modal.shape[1]
    m = modal[g].astype(np.int64); mj = majo[g].astype(np.int64)
    out = {}
    for nm, ids in (('modal', m), ('majo', mj)):
        cl = CATMAP[ids]
        out['cls_' + nm] = [int((cl == c).sum()) for c in range(5)]
        pr = PAIROF[ids]
        out['pair_' + nm] = [int((pr == p).sum()) for p in range(3)]
        out['npairs_' + nm] = int(len({int(p) for p in pr if p >= 0}))
    d = snapd[si]                                   # (I, nout)
    out['fair_enc'] = float(d[:, ISFAIR].sum(1).mean())
    out['fair_enc_pair'] = [float(d[:, MW.V[p]].mean()) for p in range(3)]
    out['surplus'] = float((d * T.TOT[None, :]).sum(1).mean())
    out['enc_cls'] = [float(d[:, CATMAP == c].sum(1).mean()) for c in range(5)]
    srt = np.sort(d, axis=1)
    out['ties'] = int(((srt[:, -1] - srt[:, -2]) < 1e-12).sum())
    out['fair_enc_isl'] = [round(float(x), 4) for x in d[:, ISFAIR].sum(1)]
    # who holds: dominant program per slot on F and U islands (by the majority triple's islands)
    hold = {}
    cm = CATMAP[mj]
    c = snapc[si]                                   # (I, 3, K)
    for label, code in (('F', 0), ('U', 1)):
        cnt = {}
        for i in np.nonzero(cm == code)[0]:
            for s in range(3):
                k = int(np.argmax(c[i, s]))
                f = int(fam[s, U[s][k]])
                cnt[f] = cnt.get(f, 0) + 1
        hold[label] = cnt
    out['hold'] = hold
    return out


def consensus_flags(modal_ids, thr=0.99):
    """(fair consensus pair or -1, unequal consensus outcome or -1) of an array of island modal outcome ids."""
    n = len(modal_ids)
    vals, cnt = np.unique(modal_ids, return_counts=True)
    j = int(np.argmax(cnt)); top = int(vals[j])
    if cnt[j] >= thr * n:
        cl = int(CATMAP[top])
        if cl == 0:
            return int(PAIROF[top]), -1
        if cl == 1:
            return -1, top
    return -1, -1


def tail_accounting(prep, res, lam, fam, N):
    """arrivals delivered, by family and by early/late; establishment (a presence episode begun by the arrival crosses
    N/2 of its slot) and the island's class one 5N later.  Returns a compact dict."""
    geo = prep['geo']
    alog = res['alog']; na = int(res['na'])
    xlog = res['xlog']
    U = prep['U']
    nf = fam.max() + 1
    # index established episodes: (island, slot, local program, intro generation) -> crossing generation
    est = {}
    for row in xlog:
        g, i, s, k, arrf, intro = (int(x) for x in row)
        if arrf == 1:
            est[(i, s, k, intro)] = g
    modal = res['modal']; cl = CATMAP[modal.astype(np.int64)]
    out = dict(sched=int(len(res['arr'][0])), logged=na, early=np.zeros((nf, 4), np.int64).tolist(),
               late=np.zeros((nf, 4), np.int64).tolist())
    early = np.zeros((nf, 4), np.int64); late = np.zeros((nf, 4), np.int64)   # delivered, applied (victim differs), established, established and class changed
    Hh = modal.shape[0] - 1
    for t in range(min(na, len(alog))):
        g, i, s, k, vk, ap = (int(x) for x in alog[t])
        f = int(fam[s, U[s][k]])
        tgt = early if g <= 15 * N else late
        tgt[f, 0] += 1
        if ap == 1 and vk != k:
            key = (i, s, k, g)
            tgt[f, 1] += 1
            if key in est:
                tgt[f, 2] += 1
                g5 = min(g + 5 * N, Hh)
                if cl[g5, i] != cl[min(g, Hh), i]:
                    tgt[f, 3] += 1
    out['early'] = early.tolist(); out['late'] = late.tolist()
    return out


def summarize(prep, res, lam, mN, fam, long=False):
    N = prep['N']; geo = prep['geo']
    H = geo['Hlong'] if long else geo['H']
    snaps = list(geo['snaps']) + ([240 * N] if long else [])
    modal = res['modal']; majo = res['majo']
    I = prep['I']
    rec = dict(arm=prep['arm'], variant=prep['variant'], N=N, run=prep['r'], lam=lam, mN=mN, status=int(res['status']),
               stop=int(res['stop']), nmig=int(res['nmig']), n_arr=int(len(res['arr'][0])), n_logged=int(res['na']),
               xlog_n=int(res['nx']), K=[len(u) for u in prep['U']], long=bool(long))
    sn = {}
    for si, g in enumerate(snaps):
        sn[str(g)] = snap_stats(res['snapc'], res['snapd'], modal, majo, si, g, fam, prep['U'])
    rec['snap'] = sn
    g120 = 120 * N
    fp, up = consensus_flags(modal[g120].astype(np.int64))
    rec['cons_modal'] = dict(fair_pair=fp, unequal=up)
    fp, up = consensus_flags(majo[g120].astype(np.int64))
    rec['cons_majo'] = dict(fair_pair=fp, unequal=up)
    if long:
        fp, up = consensus_flags(modal[240 * N].astype(np.int64))
        rec['cons_modal_240'] = dict(fair_pair=fp, unequal=up)
    # V* share time series every N generations (modal and majo)
    tg = np.arange(0, H + 1, N)
    rec['vshare_ts'] = [round(float(ISFAIR[modal[g]].mean()), 4) for g in tg]
    # transitions
    tr = {}
    for L, tag in ((DEBOUNCE, 'd25'), (max(1, int(round(0.25 * N))), 'dq')):
        tr['tail|' + tag] = transitions(modal, geo['g0'], geo['gend'], L)
        tr['chase|' + tag] = transitions(modal, geo['gend'], 120 * N, L)
        if long:
            tr['chase2|' + tag] = transitions(modal, 120 * N, 240 * N, L)
    rec['trans'] = tr
    rec['tail'] = tail_accounting(prep, res, lam, fam, N) if lam > 0 else None
    return rec
