"""Driver for removing rival networks (notes/removing-rivals.md).

    python3 src/removing_rivals_run.py ckpt [--workers 3]        # Part 0: reconstruct stored N >= 200 S-rule runs to 2,000
    python3 src/removing_rivals_run.py branch [--workers 3]      # B1: matched eps = 0 and rain branches from checkpoints
    python3 src/removing_rivals_run.py lottery --cells ... --out NAME   # A, B2, B3, baselines
    python3 src/removing_rivals_run.py inject                    # injection assays (amendment 4)
    python3 src/removing_rivals_run.py triples                   # forced-island triples (amendment 2)
Rows go to runs/removing_rivals/*.json (summaries); checkpoints to runs/removing_rivals/ckpt_*.npz (not committed).
"""
import argparse
import gzip
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import provenance_run as PR
import realizable_scaling as RS
import realizable_scaling_run as RSR
import removing_rivals as RR

ROOT = RR.ROOT
OUT = RR.OUT
os.makedirs(OUT, exist_ok=True)
STEP = 5
LOSS_MIN = 25
PAYM = PV.PAYM


def log(*a):
    print(*a, flush=True)


def stored_rows(files=('lottery_main', 'lottery_srest')):
    rows = []
    for f in files:
        rows += json.load(gzip.open(os.path.join(ROOT, 'runs', 'realizable_scaling', f + '.json.gz')))
    return rows


def ckpt_path(cell, rep):
    return os.path.join(OUT, 'ckpt_%s_%d.npz' % (cell, rep))


def upay(p, x, S):
    """Payoff of unit p against unit x (distinct quotes; p == x is twin play)."""
    A = S['A']
    return float(PAYM[A[p, x], A[x, p]])


def uself(x, S):
    a = S['sa'][x]
    return float(PAYM[a, a])


# ------------------------------------------------------------------------------------------------ tracking
class Tracker:
    """Per-island status every STEP generations: code (0 unheld, 1 target, 2 rival), majority quote, the predator
    share relative to the rival episode's first holder; lineage colonizations; snapshots."""

    def __init__(self, R, snaps, rival0=None):
        self.R = R
        self.S = RR.static(R.LS)
        self.snaps = sorted(snaps)
        self.tl = [[] for _ in range(R.I)]           # per island: [g, code, unit, sp, predhalf]
        self.ep_x = [None] * R.I                     # rival episode's first holder unit
        self.ep_flag = {}
        self.pcache = {}
        self.colon = {}                              # (lid, island) -> first g
        self.snap_out = {}
        self.uot_first = -1
        self.rival0 = rival0

    def _pflags(self, x, Tun):
        key = (x, tuple(Tun))
        if key not in self.ep_flag:
            self.ep_flag[key] = RR.predflag_units(x, Tun, self.R.LS)
        return self.ep_flag[key]

    def step(self, full=False):
        R, S = self.R, self.S
        cc = R.island_stats()
        h = RR.holders(R, cc) if (full or R.g % 50 == 0) else self._light(cc)
        Tun = RR.target_run_units(h, S)
        ps = np.zeros(R.I)
        for i in range(R.I):
            code = 0 if not h['held'][i] else (1 if h['ontgt'][i] else 2)
            k = int(h['maj'][i]); u = int(R.tunit[k]); sp = int(R.tsp[k])
            if code == 2 and self.ep_x[i] is None:
                self.ep_x[i] = u
            if code == 1:
                self.ep_x[i] = None
            if self.ep_x[i] is not None:
                f = self._pflags(self.ep_x[i], Tun)
                ks = R.pres[i, :R.npres[i]]
                ps[i] = float((R.counts[i, ks] * f[R.tunit[ks]]).sum()) / R.N
            ph = int(ps[i] >= 0.5)
            last = self.tl[i][-1] if self.tl[i] else None
            if last is None or last[1] != code or last[2] != u or last[3] != sp or last[4] != ph:
                self.tl[i].append([R.g, code, u, sp, ph])
        if R.track:
            lid, cnt = RR.lineage_majorities(R)
            for i in np.nonzero(cnt * 2 >= R.N)[0].tolist():
                key = (int(lid[i]), i)
                if key not in self.colon: self.colon[key] = R.g
        if 'uot' in h:
            if h['uot'] and self.uot_first < 0: self.uot_first = R.g
        if R.g in self.snaps:
            self.snap_out[R.g] = self.snapshot(cc, h)
        return h

    def _light(self, cc):
        R, S = self.R, self.S
        maj = R.maj_k.copy()
        hu = R.tunit[maj]
        selfc = np.where(R.tsp[maj] >= 0, S['sa'][hu] == 1, False)   # majority quote's same-quote self-play
        held = selfc & (cc >= 0.5)
        ontgt = held & S['T'][hu]
        return dict(maj=maj, hu=hu, held=held, ontgt=ontgt, tgt_units=sorted(set(int(u) for u in hu[ontgt].tolist())))

    def snapshot(self, cc, h):
        R, S = self.R, self.S
        if 'uot' not in h: h = RR.holders(R, cc)
        lab, mass, self.pcache = RR.classify_rivals(R, h, R.LS, self.pcache)
        from collections import Counter
        c = Counter(lab)
        return dict(g=R.g, uot=h['uot'], uo=h['uo'], split=h['split'], target=int(h['ontgt'].sum()),
                    held=int(h['held'].sum()), identity=c.get('identity', 0), exploitable=c.get('exploitable', 0),
                    closed_open=c.get('closed-open', 0), closed_nonopen=c.get('closed-nonopen', 0),
                    unheld=c.get('unheld', 0), pcc=float(cc.mean()), eff=int((cc >= 0.95).sum()),
                    labels=lab, holder_sp=[int(R.tsp[k]) for k in h['maj']],
                    holder_unit=[int(R.tunit[k]) for k in h['maj']], pred_mass=[round(m, 6) for m in mass],
                    n_types=int(R.ntv[0]))


def status_at(tl, g):
    """The island's status entry in force at generation g (the last checkpoint at or before g)."""
    cur = None
    for e in tl:
        if e[0] <= g: cur = e
        else: break
    return cur


def losses(tl, g_end):
    """Target -> non-target episodes: (start, length, new code, unit, sp), lasting >= LOSS_MIN (losses) or not
    (transient contamination)."""
    out_l, out_t = [], []
    for n, e in enumerate(tl):
        if n == 0 or e[1] == 1 or tl[n - 1][1] != 1: continue
        # e: first non-target checkpoint after target
        end = g_end
        for e2 in tl[n + 1:]:
            if e2[1] == 1:
                end = e2[0]; break
        rec = (e[0], end - e[0] + STEP, e[1], e[2], e[3])
        (out_l if end - e[0] + STEP > LOSS_MIN else out_t).append(rec)
    return out_l, out_t


def path_of(tl, g0, x0):
    """Resolution and path of a rival island whose episode starts at g0 with holder unit x0 (notes §1.6)."""
    seq = [e for e in tl if e[0] >= g0]
    pred = False
    inter = []
    for n, e in enumerate(seq):
        if e[4]: pred = True
        if e[1] == 1:
            # resolution if target for >= LOSS_MIN generations
            end = None
            for e2 in seq[n + 1:]:
                if e2[1] != 1:
                    end = e2[0]; break
            if end is None or end - e[0] >= LOSS_MIN:
                path = 'predator' if pred else ('direct' if not inter else 'other')
                return dict(resolved=True, g=e[0], path=path, inter=inter[:6])
        elif e[2] != x0 and e[1] != 1:
            inter.append((e[0], e[1], e[2], e[3], e[4]))
    last = seq[-1] if seq else None
    elsewhere = bool(last is not None and last[1] == 2 and last[2] != x0)
    return dict(resolved=False, elsewhere=elsewhere, pred_seen=pred, inter=inter[:6])


def arrivals_summary(R, tr, horizon_end):
    """Selected / neutral / deleterious classification of every rain arrival (notes §1.9) and colonization
    outcomes by class and by the island's status at arrival (vectorized)."""
    S = RR.static(R.LS)
    n = int(R.nfr[0])
    if n == 0: return dict(n=0)
    fr = R.fr[:n]; frf = R.frf[:n]
    g = fr[:, 0]; isl = fr[:, 1]; s = fr[:, 2]; mk = fr[:, 3]; lid = fr[:, 4]
    x = R.tunit[mk]; sx = R.tsp[mk]
    tau = R.LS['tau']
    same = s == sx
    key = np.where(same, -(s + 1) * 20000 - x, tau[s] * 20000 + x)
    uk, inv = np.unique(key, return_inverse=True)
    first = np.zeros(len(uk), np.int64)
    first[inv[::-1]] = np.arange(n)[::-1]
    ph = np.zeros(len(uk), np.int64); cl = np.zeros(len(uk), np.int64)     # 0 selected 1 neutral 2 deleterious
    for j, q in enumerate(first.tolist()):
        p = RR.phenotype(int(S['spE'][s[q]]), int(s[q]), int(x[q]), int(sx[q]), R.LS)
        dlt = upay(p, int(x[q]), S) - uself(int(x[q]), S)
        ph[j] = p; cl[j] = 0 if dlt > 1e-9 else (1 if dlt > -1e-9 else 2)
    acl = cl[inv]; aph = ph[inv]
    stc = np.full(n, -1, np.int64)
    for i in range(R.I):
        m = isl == i
        if not m.any() or not tr.tl[i]: continue
        G = np.array([e[0] for e in tr.tl[i]]); C = np.array([e[1] for e in tr.tl[i]])
        idx = np.searchsorted(G, g[m], side='right') - 1
        stc[m] = np.where(idx >= 0, C[np.maximum(idx, 0)], -1)
    pos = {int(l): q for q, l in enumerate(lid.tolist())}
    colf = np.zeros(n, bool)
    events = []
    names = ('selected', 'neutral', 'deleterious')
    for (l, i), gc in tr.colon.items():
        q = pos.get(l)
        if q is None or int(isl[q]) != i: continue
        colf[q] = True
        events.append(dict(lid=int(l), island=int(i), g_arr=int(g[q]), g_col=int(gc), cls=names[acl[q]],
                           status_at_arrival=int(stc[q]), spelling=R.LS['names'][int(s[q])], phen=int(aph[q]),
                           x=int(x[q]), maj_share=float(frf[q, 0]), empty_unit_adv=float(frf[q, 1] - frf[q, 2]),
                           on_target_after=bool(S['T'][aph[q]])))
    cls_cnt = {}
    for c in range(3):
        for st in (-1, 0, 1, 2):
            m = (acl == c) & (stc == st)
            if m.any():
                cls_cnt['%s|%d' % (names[c], st)] = [int(m.sum()), int((m & colf).sum())]
    mig = sum(1 for (l, i) in tr.colon if pos.get(l) is None or int(isl[pos[l]]) != i)
    return dict(n=n, by_class=cls_cnt, colonizations=events, migrated_colonizations=mig,
                overflow=bool(n >= RR.FCAP))


# ------------------------------------------------------------------------------------------------ Part 0 checkpoints
def stored_trace_fields(R, cc):
    sn = R.snapshot(cc)
    det = RSR.holders_detail(R, cc)
    return (R.g, sn['pcc'], sn['islands90'], sn['held'], sn['identity_islands'], sn['open_islands'],
            sn['spo_islands'], sn['n_types'], int(det['cl']['universal_open']), int((cc >= 0.95).sum()))


def compare_trace(mine, stored):
    tb = {t[0]: t for t in stored}
    bad = 0; n = 0
    for t in mine:
        if t[0] in tb:
            n += 1
            if any(abs(a - b) > 1e-9 for a, b in zip(t, tb[t[0]])): bad += 1
    return n, bad


def ckpt_job(job):
    cell, rep, stored_trace, stored_final_sp = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    R = RR.RRRun(cell, rep, epsN=0.0)
    mine = []
    while R.g < 2000:
        R.advance(10)
        if R.g % 50 == 0:
            cc = R.island_stats()
            mine.append(stored_trace_fields(R, cc))
    n, bad = compare_trace(mine, [t for t in stored_trace if t[0] <= 2000])
    cc = R.island_stats()
    h = RR.holders(R, cc)
    S = RR.static(R.LS)
    lab, mass, cache = RR.classify_rivals(R, h, R.LS)
    det = RSR.holders_detail(R, cc)
    st_lab = det['cl']['fail']
    Tun = RR.target_run_units(h, S)
    preds = {}
    for (x, sx, xr, tt), pt in cache.items():
        preds['%d|%d' % (x, sx)] = dict(pt, holder=R.LS['names'][sx], unit=x)
    saved = False
    if not h['uot']:
        np.savez_compressed(ckpt_path(cell, rep), **R.save_state())
        saved = True
    return dict(cell=cell, rep=rep, N=R.N, I=R.I, mN=R.mN, trace_compared=n, trace_bad=bad,
                uot=h['uot'], uo=h['uo'], split=h['split'], labels=lab, pred_mass=mass, stored_labels=st_lab,
                holder_sp=[int(R.tsp[k]) for k in h['maj']], holder_unit=[int(R.tunit[k]) for k in h['maj']],
                held=h['held'].astype(int).tolist(), ontgt=h['ontgt'].astype(int).tolist(),
                same_as_stored_final=bool([int(R.tsp[k]) for k in h['maj']] == stored_final_sp),
                tgt_units=Tun, preds=preds, saved=saved, n_types=int(R.ntv[0]), time_s=time.time() - t0)


def run_pool(fn, jobs, path, workers, key=lambda r: (r['cell'], r['rep']), jkey=lambda j: (j[0], j[1]), tag=''):
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {key(r) for r in rows}
    jobs = [j for j in jobs if jkey(j) not in done]
    log('%s jobs %d (pid %d), already done %d' % (tag, len(jobs), os.getpid(), len(done)))
    if not jobs: return rows
    t0 = time.time()
    with Pool(min(3, workers)) as pool:
        for r in pool.imap_unordered(fn, jobs):
            rows.append(r)
            tmp = path + '.tmp'
            json.dump(rows, open(tmp, 'w')); os.replace(tmp, path)
            log('%s %s: %s (%.0fs, total %.0fs)' % (tag, key(r), r.get('msg', ''), r['time_s'], time.time() - t0))
    return rows


def cmd_ckpt(a):
    rows = [r for r in stored_rows() if r['N'] >= 200 and r['rule'] in ('Snon', 'prop', 'abl')]
    jobs = [(r['cell'], r['rep'], [tuple(t) for t in r['trace']], r['final_isl']['holder_sp']) for r in rows]
    jobs.sort(key=lambda j: -(RS.CELL_INFO[j[0]]['N'] ** 2 * RS.CELL_INFO[j[0]]['I']))
    out = run_pool(ckpt_job, jobs, os.path.join(OUT, 'ckpt_rows.json'), a.workers, tag='ckpt')
    log('done', len(out))


# ------------------------------------------------------------------------------------------------ B1 branches
def branch_one(cell, rep, state, epsN, gens, rival0, stored_trace=None):
    t0 = time.time()
    R = RR.RRRun(cell, rep, epsN=epsN)
    R.load_state(state)
    g0 = R.g
    snaps = [g0 + 2000, g0 + 5000, g0 + gens] + ([10000] if g0 + gens > 10000 > g0 else [])
    tr = Tracker(R, snaps)
    tr.step(full=True)
    val = []
    stb = {t[0]: t for t in stored_trace} if stored_trace is not None else {}
    while R.g < g0 + gens:
        R.advance(STEP)
        tr.step()
        if epsN == 0 and R.g % 500 == 0 and R.g in stb:
            mine = stored_trace_fields(R, R.island_stats())
            val.append(int(any(abs(x - y) > 1e-9 for x, y in zip(mine, stb[R.g]))))
    cc = R.island_stats()
    h = RR.holders(R, cc)
    isl = []
    for i, (lab, x0) in rival0.items():
        p = path_of(tr.tl[i], g0, x0)
        p.update(island=i, label=lab, x0=x0, final_code=tr.tl[i][-1][1], final_unit=tr.tl[i][-1][2],
                 final_sp=tr.tl[i][-1][3])
        isl.append(p)
    L, Tt = [], []
    for i in range(R.I):
        l, t = losses(tr.tl[i], R.g)
        L += [(i,) + tuple(z) for z in l]; Tt += [(i,) + tuple(z) for z in t]
    arr = arrivals_summary(R, tr, R.g) if R.track else dict(n=0)
    return dict(epsN=epsN, g0=g0, g_end=R.g, snaps={str(k): v for k, v in tr.snap_out.items()}, islands=isl,
                losses=L, transient=Tt[:200], n_transient=len(Tt), uot_first=tr.uot_first,
                rain_founders=int(R.rcount.sum()), arrivals=arr, n_types=int(R.ntv[0]),
                validate=dict(n=len(val), bad=int(sum(val))), time_s=time.time() - t0)


def branch_job(job):
    cell, rep, rates, gens, rival0, stored_trace = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    z = np.load(ckpt_path(cell, rep))
    state = {k: z[k] for k in z.files}
    out = []
    for e in rates:
        out.append(branch_one(cell, rep, state, e, gens, rival0, stored_trace if e == 0 else None))
    return dict(cell=cell, rep=rep, branches=out, time_s=time.time() - t0,
                msg=' '.join('%g:uot%s/res%d' % (b['epsN'], b['snaps'][str(b['g_end'])]['uot'],
                                                  sum(1 for x in b['islands'] if x['resolved'])) for b in out))


def cmd_branch(a):
    ck = json.load(open(os.path.join(OUT, 'ckpt_rows.json')))
    st = {(r['cell'], r['rep']): r for r in stored_rows()}
    jobs = []
    for r in ck:
        if not r['saved']: continue
        if a.cells and r['cell'] not in a.cells: continue
        rival0 = {i: (lab, r['holder_unit'][i]) for i, lab in enumerate(r['labels']) if lab not in ('', 'unheld')}
        jobs.append((r['cell'], r['rep'], tuple(a.rates), a.gens, rival0,
                     [tuple(t) for t in st[(r['cell'], r['rep'])]['trace']]))
    jobs.sort(key=lambda j: -(RS.CELL_INFO[j[0]]['N'] ** 2 * RS.CELL_INFO[j[0]]['I']))
    run_pool(branch_job, jobs, os.path.join(OUT, 'branch_%s.json' % a.out), a.workers, tag='branch')


# ------------------------------------------------------------------------------------------------ lottery cells
def lottery_job(job):
    cell, rep, gens = job[:3]
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    R = RR.RRRun(cell, rep)
    snaps = [500, 1000, 2000, 5000, 10000]
    snaps = [s for s in snaps if s <= gens]
    tr = Tracker(R, snaps)
    while R.g < gens:
        R.advance(STEP)
        tr.step()
        if R.epsN == 0 and R.g >= 2000 and R.g % 500 == 0 and R.frozen():
            # exact at eps = 0: a single global type whose own encounters change nothing
            cc = R.island_stats(); h = RR.holders(R, cc)
            snap = tr.snapshot(cc, h)
            for s in snaps:
                if s > R.g: tr.snap_out[s] = dict(snap, g=s, frozen_from=R.g)
            break
    L, Tt = [], []
    for i in range(R.I):
        l, t = losses(tr.tl[i], R.g)
        L += [(i,) + tuple(z) for z in l]; Tt += [(i,) + tuple(z) for z in t]
    # rival episodes and their resolution (B2/B3 and A: every rival episode starting at or after 500)
    eps_res = []
    for i in range(R.I):
        tl = tr.tl[i]
        for n, e in enumerate(tl):
            if e[1] == 2 and (n == 0 or tl[n - 1][1] != 2) and e[0] >= 500:
                p = path_of(tl, e[0], e[2]); p.update(island=i, g0=e[0], x0=e[2])
                eps_res.append(p)
    arr = arrivals_summary(R, tr, R.g) if R.track else dict(n=0)
    s2 = tr.snap_out.get(2000, {}); s10 = tr.snap_out.get(gens, {})
    return dict(cell=cell, rep=rep, N=R.N, I=R.I, epsN=R.epsN, gens=gens, last_gen=R.g,
                snaps={str(k): v for k, v in tr.snap_out.items()}, losses=L, transient=Tt[:200], n_transient=len(Tt),
                rival_episodes=eps_res[:400], uot_first=tr.uot_first, rain_founders=int(R.rcount.sum()),
                arrivals=arr, n_types=int(R.ntv[0]), time_s=time.time() - t0,
                msg='uot2k %s uot10k %s tgt %s id %s expl %s cl %s' % (s2.get('uot'), s10.get('uot'), s10.get('target'),
                                                                      s10.get('identity'), s10.get('exploitable'),
                                                                      s10.get('closed_open')))


def cmd_lottery(a):
    jobs = []
    for c in a.cells:
        jobs += [(c, rep, a.gens) for rep in range(a.rep0, a.rep0 + a.runs)]
    jobs.sort(key=lambda j: -(RS.CELL_INFO[j[0]]['N'] ** 2 * RS.CELL_INFO[j[0]]['I'] * (1 + RR.CELL_EPSN.get(j[0], 0))))
    run_pool(lottery_job, jobs, os.path.join(OUT, 'lottery_%s.json' % a.out), a.workers, tag='lottery')


# ------------------------------------------------------------------------------------------------ assays
def matched_nonpred(s, pt, x, sx, LS):
    """The non-predator spelling closest in prior mass to s whose phenotype against X self-cooperates or
    cooperates with X (notes §1.3)."""
    S = RR.static(LS)
    mu = LS['mu']
    order = np.argsort(np.abs(mu - mu[s]))
    for c in order.tolist():
        if pt['is_pred'][c] or c == s: continue
        p = int(pt['phen'][c])
        if S['sa'][p] == 1 or S['A'][p, x] == 1:
            return c
    return None


def inject_job(job):
    cell, rep, island, sp, kind, k, gens = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    z = np.load(ckpt_path(cell, rep))
    R = RR.RRRun(cell, rep, epsN=0.0, track=True)
    R.load_state({kk: z[kk] for kk in z.files})
    R.seed = int((R.seed + 104729 * (k + 1) + (7919 if kind == 'nonpred' else 0)) % (2 ** 62))
    rng = np.random.default_rng([R.N, R.I, rep, island, k, 99])
    cc = R.island_stats()
    xk = int(R.maj_k[island]); x = int(R.tunit[xk])
    js = np.nonzero(R.tunit[R.slots[island]] == x)[0]
    j = int(rng.choice(js))
    R.lin[:] = 0; R.nlin[0] = 0
    R.inject(island, j, sp)
    lid = int(R.nlin[0])
    g0 = R.g
    tr = Tracker(R, [g0 + gens])
    tr.step(full=True)
    while R.g < g0 + gens:
        R.advance(STEP)
        tr.step()
    col = [g for (l, i), g in tr.colon.items() if l == lid and i == island]
    other = sorted(i for (l, i) in tr.colon if l == lid and i != island)
    p = path_of(tr.tl[island], g0, x)
    return dict(cell=cell, rep=rep, island=island, sp=sp, spelling=R.LS['names'][sp], kind=kind, k=k, x=x,
                colonized=bool(col), g_col=(col[0] - g0) if col else None, spread_to=len(other), path=p,
                final_code=tr.tl[island][-1][1], time_s=time.time() - t0, msg='%s col %s res %s' % (kind, bool(col), p['resolved']))


def cmd_inject(a):
    ck = json.load(open(os.path.join(OUT, 'ckpt_rows.json')))
    cand = []
    for r in ck:
        if not r['saved']: continue
        for i, lab in enumerate(r['labels']):
            if lab == 'exploitable':
                cand.append((r['pred_mass'][i], r['cell'], r['rep'], i, r))
    cand.sort(key=lambda z: -z[0])
    chosen, per_cell = [], {}
    for m, cell, rep, i, r in cand:
        if per_cell.get(cell, 0) >= 2: continue
        if any((c[0], c[1]) == (cell, rep) for c in chosen): continue
        chosen.append((cell, rep, i, r)); per_cell[cell] = per_cell.get(cell, 0) + 1
        if len(chosen) >= a.n: break
    LS = PR.lot_static()
    jobs = []
    meta = []
    for cell, rep, i, r in chosen:
        x = r['holder_unit'][i]; sx = r['holder_sp'][i]
        xr = PV.R_SNON
        pt = RR.predator_table(x, sx, xr, r['tgt_units'], LS)
        s = int(np.argmax(LS['mu'] * pt['is_pred']))
        c = matched_nonpred(s, pt, x, sx, LS)
        meta.append(dict(cell=cell, rep=rep, island=i, x=x, holder=LS['names'][sx], pred=LS['names'][s],
                         pred_mu=float(LS['mu'][s]), nonpred=LS['names'][c] if c is not None else None,
                         nonpred_mu=float(LS['mu'][c]) if c is not None else None, mass=pt['mass']))
        for k in range(a.reps):
            jobs.append((cell, rep, i, s, 'pred', k, a.gens))
            if c is not None: jobs.append((cell, rep, i, c, 'nonpred', k, a.gens))
    json.dump(meta, open(os.path.join(OUT, 'inject_meta.json'), 'w'), indent=1)
    run_pool(inject_job, jobs, os.path.join(OUT, 'inject_rows.json'), a.workers,
             key=lambda r: (r['cell'], r['rep'], r['kind'], r['k']), jkey=lambda j: (j[0], j[1], j[4], j[5]), tag='inject')


def triple_job(job):
    name, rep, x, sx, xr, z_, sz, zr, ps, gens, N, I = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    S = RR.static(PR.lot_static())
    sp = np.zeros((I, N), np.int64); rule = np.zeros((I, N), np.int64); unit = np.zeros((I, N), np.int64)
    for i in range(I):
        if i < I // 2: sp[i] = sx; rule[i] = xr; unit[i] = x
        else: sp[i] = sz; rule[i] = zr; unit[i] = z_
    sp[0, 0] = ps; rule[0, 0] = PV.R_SNON; unit[0, 0] = S['spE'][ps]
    RR.FORCED[name] = (sp, rule, unit)
    RR.register(name, N, I, 'forced')
    R = RR.RRRun(name, rep, epsN=0.0, track=True)
    R.lin[0, 0] = 1; R.nlin[0] = 1
    tr = Tracker(R, [gens])
    tr.step(full=True)
    while R.g < gens:
        R.advance(STEP)
        tr.step()
    xi = list(range(I // 2))
    fin = [tr.tl[i][-1] for i in range(I)]
    col = sorted(i for (l, i) in tr.colon if l == 1)
    res = [path_of(tr.tl[i], 0, x) for i in xi]
    return dict(name=name, rep=rep, x=x, z=z_, ps=ps, colonized=col, x_to_target=sum(1 for r in res if r['resolved']),
                paths=[r.get('path') for r in res], z_lost=sum(1 for i in range(I // 2, I) if fin[i][1] != 1),
                time_s=time.time() - t0, msg='col %s x->T %d' % (col, sum(1 for r in res if r['resolved'])))


def cmd_triples(a):
    ck = json.load(open(os.path.join(OUT, 'ckpt_rows.json')))
    LS = PR.lot_static()
    best = {}
    for r in ck:
        if not r['saved']: continue
        for i, lab in enumerate(r['labels']):
            if lab != 'exploitable': continue
            key = (r['holder_unit'][i], r['holder_sp'][i])
            if key not in best or r['pred_mass'][i] > best[key][0]:
                best[key] = (r['pred_mass'][i], r)
    top = sorted(best.items(), key=lambda kv: -kv[1][0])[:a.n]
    jobs, meta = [], []
    for n, ((x, sx), (m, r)) in enumerate(top):
        from collections import Counter
        zc = Counter((u, s) for u, s, t in zip(r['holder_unit'], r['holder_sp'], r['ontgt']) if t)
        (z_, sz), _ = zc.most_common(1)[0]
        pt = RR.predator_table(x, sx, PV.R_SNON, r['tgt_units'], LS)
        ps = int(np.argmax(LS['mu'] * pt['is_pred']))
        c = matched_nonpred(ps, pt, x, sx, LS)
        meta.append(dict(n=n, x=x, holder=LS['names'][sx], z=z_, z_holder=LS['names'][sz], pred=LS['names'][ps],
                         nonpred=LS['names'][c] if c is not None else None, mass=m, cell=r['cell'], rep=r['rep']))
        for k in range(a.reps):
            jobs.append(('rr_tri%d_p' % n, 7000 + k, x, sx, PV.R_SNON, z_, sz, PV.R_SNON, ps, a.gens, 200, 8))
            if c is not None and k < a.reps // 2:
                jobs.append(('rr_tri%d_n' % n, 7000 + k, x, sx, PV.R_SNON, z_, sz, PV.R_SNON, c, a.gens, 200, 8))
    json.dump(meta, open(os.path.join(OUT, 'triples_meta.json'), 'w'), indent=1)
    run_pool(triple_job, jobs, os.path.join(OUT, 'triples_rows.json'), a.workers,
             key=lambda r: (r['name'], r['rep']), jkey=lambda j: (j[0], j[1]), tag='triples')


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('ckpt'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('branch'); s.add_argument('--workers', type=int, default=3)
    s.add_argument('--rates', nargs='+', type=float, default=[0.0, 0.01, 0.1, 1.0])
    s.add_argument('--gens', type=int, default=10000); s.add_argument('--out', default='main')
    s.add_argument('--cells', nargs='*', default=None)
    s = sub.add_parser('lottery'); s.add_argument('--cells', nargs='+'); s.add_argument('--runs', type=int, default=20)
    s.add_argument('--rep0', type=int, default=0); s.add_argument('--gens', type=int, default=10000)
    s.add_argument('--workers', type=int, default=3); s.add_argument('--out', default='main')
    s = sub.add_parser('inject'); s.add_argument('--workers', type=int, default=3); s.add_argument('--n', type=int, default=6)
    s.add_argument('--reps', type=int, default=20); s.add_argument('--gens', type=int, default=2000)
    s = sub.add_parser('triples'); s.add_argument('--workers', type=int, default=3); s.add_argument('--n', type=int, default=3)
    s.add_argument('--reps', type=int, default=50); s.add_argument('--gens', type=int, default=2000)
    a = ap.parse_args()
    {'ckpt': cmd_ckpt, 'branch': cmd_branch, 'lottery': cmd_lottery, 'inject': cmd_inject,
     'triples': cmd_triples}[a.cmd](a)


if __name__ == '__main__':
    main()
