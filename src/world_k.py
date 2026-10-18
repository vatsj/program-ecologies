"""Identity-dependent results under world K (spec specs/2026-10-18-world-k-reruns.md, notes notes/world-k.md).

Imports the provenance, scaling, Pangaea, removing-rivals, annealed and detectors machinery unchanged and adds:
  - a world switch: provenance's run constructor, the removing-rivals statics, the Pangaea statics and the scaling
    run's static check read world w's tables (L: runs/provenance; K: runs/detectors/K).  In K the static set's 'Q'
    (empty: no identity unit is reachable under S-nonself) is replaced by L's Q, so every K run tracks the *former*
    TwinD family and the proportional control redraws the same founder slots in both worlds; K's own (empty) set is
    kept as 'Q_K';
  - cells for the scaling path, the provenance rule and the paired rain cell, with the scaling founders (identical
    spellings in both worlds; units are the world's E units) and provenance's kernel seed;
  - the island run object: the annealed kernel (provenance's draws for r <= 100) at r = 100, eps = 0 except in the
    rain cell, with lineage tracking from the seed (every founder its own lineage id), which consumes only the
    otherwise unused draw 7 and so leaves every trajectory unchanged;
  - per-island statistics: outcome classes, establishment times, holder changes with migrant ancestry, rival classes,
    gentle readers' exposure and the S-self production budget.
Pangaea cells run through the Pangaea run's own job (src/pangaea_run.py) under the world switch.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import provenance_run as PR
import realizable_scaling as RS
import realizable_scaling_run as RSR
import pangaea as PG
import pangaea_run as PGR
import removing_rivals as RR
import annealed as AN
import detectors as DT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'world_k')
R_FIXED = 100
SNAPS = (200, 500, 1000, 2000, 5000, 10000)
EXPO_AT = (200, 2000, 10000)
SELF_AT = (0, 10, 50, 200, 2000)
CLS_CODE = {'': 'o', 'identity': 'i', 'rival': 'r', 'unheld': 'u'}

# ------------------------------------------------------------------------------------------------ worlds
_LS_ORIG = PR.lot_static
_WLS = {}
WORLD = {'w': None}


def world_ls(w):
    """World w's static set (cached).  K: detectors' tables with L's Q as 'Q' (the former TwinD family)."""
    if w in _WLS: return _WLS[w]
    saved = PR.lot_static
    PR.lot_static = _LS_ORIG
    try:
        LSL = _LS_ORIG('ext')
        if w == 'L':
            LS = LSL
        else:
            LSK = DT.lot_static_K()
            LS = dict(LSK)
            LS['Q_K'] = LSK['Q']
            LS['Q'] = LSL['Q']
            LS['world'] = 'K'
    finally:
        PR.lot_static = saved
    _WLS[w] = LS
    return LS


def sets_path(w):
    return os.path.join(PR.OUT if w == 'L' else DT.KDIR, 'sets.npz')


def use_world(w):
    """Point every module cache at world w (call at the start of every job; workers may alternate worlds)."""
    LS = world_ls(w)
    PR.lot_static = lambda which='ext', _LS=LS: _LS
    RR._SC.clear(); RR._PH.clear()
    PG._X.clear()
    RSR._EXTRA.clear()
    RSR._EXTRA['reach_nonself'] = np.asarray(np.load(sets_path(w))['reach_nonself'])
    WORLD['w'] = w
    return LS


# ------------------------------------------------------------------------------------------------ cells
CELLS = {}                  # name -> dict(N, I, rule, prior, rain_K, tag)
RULE_SPEC = {'Snon': 'S-nonself', 'Sself': 'S-self', 'prop': 'S-nonself'}


def cell_name(tag, N, I):
    return 'wk_%s_%d_%d' % (tag, N, I)


def register(tag, N, I, rain_K=0):
    """tag: Snon | Sself | prop | rain (S-nonself with the annealed schedule at exposure rain_K)."""
    name = cell_name(tag, N, I)
    rule = 'Snon' if tag == 'rain' else tag
    prior = 'prop' if tag == 'prop' else 'L'
    PR.CELLS[name] = (N, I, RULE_SPEC[rule], prior, 'ext')
    RS.CELL_MN[name] = RS.mN_cal(N)
    CELLS[name] = dict(N=N, I=I, tag=tag, rule=rule, prior=prior, rain_K=rain_K)
    return name


GEOMS_A = [(100, 64), (200, 64), (400, 64), (100, 128), (200, 128), (100, 256)]
CELLS_A = [register(t, N, I) for (N, I) in GEOMS_A for t in ('Snon', 'prop')]
CELLS_B = [register('Sself', N, I) for (N, I) in [(100, 64), (200, 64)]]
CELL_RAIN = register('rain', 200, 64, rain_K=3)

# Pangaea cells (the Pangaea run's own names; the r = N/2 control registered here where it was not a stored cell)
PG_CONT = ['pg_L_200_64_r100', 'pg_L_800_16_r100', 'pg_L_3200_4_r100', 'pg_L_12800_1_r100']
PG_FF = ['pg_L_100_128_r100_ff200']
PG_PANG = ['pg_L_3200_1_r100', 'pg_L_6400_1_r100']
PG_NAT = [PG.register('L', 800, 16, 'n'), PG.register('L', 3200, 4, 'n'), PG.register('L', 6400, 1, 'n')]

_PREV_FOUNDERS = PR.founders


def founders_wk(cell, rep, LS):
    """The scaling founders (stream [N, I, rep, SALT]; the proportional control's stream 6 over LS['Q'], which is L's Q
    in both worlds), rule per cell, units = the world's E units."""
    if cell not in CELLS:
        return _PREV_FOUNDERS(cell, rep, LS)
    c = CELLS[cell]
    N, I = c['N'], c['I']
    sp = RS._base_sp(N, I, rep, LS)
    if c['prior'] == 'prop':
        sp = RS.replace_Q_proportional(sp, N, I, rep, LS)
    rule = np.full((I, N), PV.RULE_OF[RULE_SPEC[c['rule']]], np.int64)
    unit = LS['Eu'][LS['tau'][sp]]
    return sp, rule, unit


PR.founders = founders_wk


# ------------------------------------------------------------------------------------------------ the island run
class IslandRun(AN.AnnRun):
    """The annealed run object at r = 100 with lineage tracking from the seed: founder (i, j) has lineage id
    i*N + j + 1; rain arrivals get ids above I*N."""

    def __init__(self, cell, rep, track=True):
        c = CELLS[cell]
        sched = AN.schedule('ann', c['N'], c['rain_K']) if c['rain_K'] else np.zeros(1)
        super().__init__(cell, rep, sched=sched, pairmode=1, r=R_FIXED, track=track)
        if track:
            I, N = self.I, self.N
            self.lin[:] = (np.arange(I)[:, None] * N + np.arange(N)[None, :] + 1).astype(np.int64)
            self.nlin[0] = I * N


# ------------------------------------------------------------------------------------------------ static sets
_ST = {}


def static_sets():
    """World-independent spelling sets: own-D readers (eff trees), the former TwinD family Q (L's), the minted
    C-identity class (spellings of the trees of K's universe identity units)."""
    if _ST: return _ST
    LSL = world_ls('L'); LSK = world_ls('K')
    cat = LSL['cat']
    eff = set(DT.eff_trees(cat))
    tau = LSL['tau']
    effsp = np.array([int(tau[s]) in eff for s in range(len(tau))])
    unitsK = LSK['meta']['units']
    mint_trees = sorted(set(int(unitsK[u][0]) for u in np.nonzero(LSK['ident'])[0].tolist()))
    mint = np.isin(tau, mint_trees)
    Q = np.zeros(len(tau), bool); Q[LSL['Q']] = True
    _ST.update(effsp=effsp, Q=Q, mint=mint, mint_trees=mint_trees, eff_trees=sorted(eff))
    return _ST


# ------------------------------------------------------------------------------------------------ statistics
def island_classes(det):
    """Per island: o (in the open main network), i (identity), r (non-identity rival), u (unheld)."""
    return ''.join(CLS_CODE[f] for f in det['cl']['fail'])


def local_share(R, i, k):
    """Share of island i's individuals of type k whose founder lineage started on island i (lineage ids <= I*N);
    rain-descended individuals counted apart."""
    idx = R.slots[i] == k
    l = R.lin[i, idx]
    if len(l) == 0: return None, None
    IN = R.I * R.N
    seeded = l[l <= IN]
    rain = float((l > IN).mean())
    if len(seeded) == 0: return 0.0, rain
    orig = (seeded - 1) // R.N
    return float((orig == i).sum()) / len(l), rain


def exposure(R, effsp):
    """Own-D reader individuals' expected encounter outcomes against their island (uniform pairing): fractions
    [mutual C, exploited (C vs D), exploiting (D vs C), mutual D] and the number of such individuals."""
    A = np.asarray(R.A); sa = np.asarray(R.selfa)
    tot = np.zeros(4); n_ind = 0
    for i in range(R.I):
        ks = R.pres[i, :R.npres[i]]
        s = R.tsp[ks]
        m = effsp[s]
        if not m.any(): continue
        c = R.counts[i, ks].astype(float)
        u = R.tunit[ks]
        a = A[np.ix_(u, u)].astype(float)
        same = (u[:, None] == u[None, :]) & (s[:, None] == s[None, :])
        a = np.where(same, sa[u][:, None].astype(float) * np.ones_like(a), a)
        for x in np.nonzero(m)[0].tolist():
            w = c.copy(); w[x] -= 1.0
            if w.sum() <= 0: continue
            ax = a[x]; ay = a[:, x]
            f = np.array([(w * ax * ay).sum(), (w * ax * (1 - ay)).sum(), (w * (1 - ax) * ay).sum(),
                          (w * (1 - ax) * (1 - ay)).sum()]) / w.sum()
            tot += f * c[x]
            n_ind += int(c[x])
    return (tot / n_ind).tolist() if n_ind else None, n_ind


def self_budget(R):
    """S-self producers lacking a C entry: their number and the expected share of their production attempts at a
    self root (the island frequency of their own quote among the other N - 1)."""
    st = R.LS['st']
    BLC = np.asarray(st['BLC'])
    num = 0.0; n = 0
    for i in range(R.I):
        ks = R.pres[i, :R.npres[i]]
        if not len(ks): continue
        u = R.tunit[ks]; s = R.tsp[ks]; r_ = R.trule[ks]; c = R.counts[i, ks]
        qkey = u * 100000 + s
        uq, inv = np.unique(qkey, return_inverse=True)
        qc = np.bincount(inv, weights=c)
        lack = (r_ == PV.R_SSELF) & (BLC[u, 0] < 0)
        for x in np.nonzero(lack)[0].tolist():
            num += c[x] * (qc[inv[x]] - 1) / (R.N - 1)
            n += int(c[x])
    return dict(lacking=n, self_share=(num / n) if n else None)


def rival_labels(R, cc, cache):
    """Removing-rivals' holders (universal-on-target) and rival classes of held non-target islands."""
    h = RR.holders(R, cc)
    lab, mass, _ = RR.classify_rivals(R, h, R.LS, cache)
    cnt = {}
    for l in lab:
        cnt[l] = cnt.get(l, 0) + 1
    return dict(uot=bool(h['uot']), uo=bool(h['uo']), labels=lab, counts=cnt,
                ontgt=int(h['ontgt'].sum()), ident=int(h['ident'].sum()))


def holder_info(R, cc, det, LS, ST):
    maj = R.maj_k
    out = []
    for i in range(R.I):
        k = int(maj[i])
        out.append((int(R.tsp[k]), int(R.tunit[k])))
    return out


# ------------------------------------------------------------------------------------------------ jobs
_RCACHE = {}                # world -> removing-rivals predator-table cache (per process)


def island_job(job):
    """One island run (scaling, provenance or rain cell) in world w to `horizon` generations."""
    import time
    cell, rep, w, horizon = job[:4]
    track = bool(job[4]) if len(job) > 4 else True
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    LS = use_world(w)
    ST = static_sets()
    c = CELLS[cell]
    R = IslandRun(cell, rep, track=track)
    I, N = R.I, R.N
    sp0 = R.sp0
    seeded = dict(Q=np.isin(sp0, np.nonzero(ST['Q'])[0]).sum(1).tolist(),
                  mint=np.isin(sp0, np.nonzero(ST['mint'])[0]).sum(1).tolist(),
                  effsp=int(ST['effsp'][sp0].sum()))
    est = -np.ones(I, np.int64)
    prev_cls = None
    prev_h = [None] * I
    changes = []                  # (g, island, spelling, unit, class, local share, rain share)
    cls_tr = []                   # (g, class string) at every checkpoint
    trace = []                    # (g, pcc, held, identity islands, uo, islands >= 0.95, Q share, n_types)
    snaps = {}
    expo = {}
    selfb = {}
    rcache = _RCACHE.setdefault(w, {})
    uo_first = -1; uo_last_change = -1; prev_uo = None
    frozen_at = -1
    if c['rule'] == 'Sself':
        selfb['0'] = self_budget(R)
    g = 0
    Qmask = ST['Q']
    while g < horizon:
        R.advance(10 if g < 1000 else 50)
        g = R.g
        cc = R.island_stats()
        new = (cc >= 0.9) & (est < 0)
        est[new] = g
        det = RSR.holders_detail(R, cc)
        cl = island_classes(det)
        uo = bool(det['cl']['universal_open'])
        if uo and uo_first < 0: uo_first = g
        if prev_uo is not None and uo != prev_uo: uo_last_change = g
        prev_uo = uo
        hol = holder_info(R, cc, det, LS, ST)
        for i in range(I):
            key = (hol[i][0], cl[i])
            if key != prev_h[i]:
                ls, rs_ = local_share(R, i, int(R.maj_k[i])) if track else (None, None)
                changes.append((g, i, hol[i][0], hol[i][1], cl[i], ls, rs_))
                prev_h[i] = key
        if cl != prev_cls:
            cls_tr.append((g, cl)); prev_cls = cl
        gsp = R.spcount.sum(0)
        qsh = float(gsp[Qmask].sum()) / (I * N)
        held = det['held']
        idn = sum(1 for i in range(I) if held[i] and det['ident'][det['hol'][i]])
        trace.append((g, round(float(cc.mean()), 5), int(held.sum()), int(idn), int(uo), int((cc >= 0.95).sum()),
                      round(qsh, 6), int(R.ntv[0])))
        if g in EXPO_AT:
            expo[str(g)] = exposure(R, ST['effsp'])
        if c['rule'] == 'Sself' and g in SELF_AT:
            selfb[str(g)] = self_budget(R)
        if g in SNAPS:
            sn = RSR.slim(R.snapshot(cc))
            sn['isl'] = RSR.island_record(R, cc, det)
            sn['cls'] = cl
            sn['holders'] = [h[0] for h in hol]
            sn['local'] = [local_share(R, i, int(R.maj_k[i]))[0] for i in range(I)] if track else None
            if N >= 200 and g in (2000, 10000):
                sn['rr'] = rival_labels(R, cc, rcache)
            snaps[str(g)] = sn
        if g >= 50 and (not c['rain_K'] or g >= AN.HORIZON) and R.frozen():
            frozen_at = g          # under rain the stop waits for the schedule's end (arrivals continue)
            break
    R.final_logs()
    cc = R.island_stats()
    det = RSR.holders_detail(R, cc)
    fin = RSR.slim(R.snapshot(cc))
    fin['isl'] = RSR.island_record(R, cc, det)
    fin['cls'] = island_classes(det)
    fin['holders'] = [h[0] for h in holder_info(R, cc, det, LS, ST)]
    fin['rr'] = rival_labels(R, cc, rcache) if N >= 200 else None
    stat = RSR.static_check_run(R, cc, det)
    if frozen_at >= 0:
        for gs in SNAPS:
            if gs > frozen_at and gs <= horizon and str(gs) not in snaps:
                snaps[str(gs)] = dict(fin, g=gs, frozen_from=frozen_at)
    return dict(cell=cell, rep=rep, world=w, N=N, I=I, tag=c['tag'], rule=c['rule'], prior=c['prior'],
                rain_K=c['rain_K'], r=R.r, mN=R.mN, horizon=horizon, last_gen=R.g, frozen_at=frozen_at, track=track,
                seeded=seeded, establish=est.tolist(), changes=changes, cls_tr=cls_tr, trace=trace, snaps=snaps,
                final=fin, static=dict(label=stat['label'], per=stat['per'][:300],
                                       n_living_types=stat['n_living_types']),
                uo_first=uo_first, uo_last_change=uo_last_change, expo=expo, selfb=selfb,
                arrivals=int(R.rcount.sum()), ctr=R.ctr.tolist(), enc_exp=R.enc_exp.tolist(),
                steps_rule=R.steps_rule.tolist(), n_types=int(R.ntv[0]), time_s=time.time() - t0)


def pg_job(job):
    """One Pangaea-run job (continuum, fission-fusion, Pangaea, r = N/2 control) in world w."""
    cell, rep, w, gens, ext = job[:5]
    use_world(w)
    r = PGR.lottery_job((cell, rep, gens, ext))
    r['world'] = w
    return r
