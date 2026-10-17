"""Driver for annealed mutation (notes/annealed.md).

    python3 src/annealed_run.py cells --cells NAME ... --out NAME [--runs 20] [--workers 3]   # natural and Part F cells
    python3 src/annealed_run.py neutral --N 200 --reps 3000 --sp C --out NAME [--workers 3]  # neutral single arrivals
    python3 src/annealed_run.py predator --N 200 --cls AP --reps 100 --out NAME              # predator single arrivals
    python3 src/annealed_run.py validate                                                      # §1.7 checks
    python3 src/annealed_run.py probe                                                         # cost probes
Rows go to runs/annealed/*.json (summaries per run).
"""
import argparse
import gzip
import json
import os
import sys
import time
from collections import Counter
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
import provenance_run as PR
import realizable_scaling as RS
import realizable_scaling_run as RSR
import removing_rivals as RR
import removing_rivals_run as RRR
import annealed as AN

OUT = AN.OUT
os.makedirs(OUT, exist_ok=True)
STEP = RRR.STEP
LOSS_MIN = RRR.LOSS_MIN
SNAPS = (200, 1000, 2000, 5000, 10000, 12000)


def log(*a):
    print(*a, flush=True)


class FateTracker(RRR.Tracker):
    """Removing-rivals' tracker plus the fate of every colonizing lineage (max share, last share, fixation)."""

    def __init__(self, R, snaps):
        super().__init__(R, snaps)
        self.fate = {}                                # (lid, island) -> [max share, last share, g_fix]

    def step(self, full=False):
        h = super().step(full)
        R = self.R
        for key in self.colon:
            if key not in self.fate: self.fate[key] = [0.0, 0.0, -1]
        for (l, i), f in self.fate.items():
            sh = float(np.count_nonzero(R.lin[i] == l)) / R.N
            if sh > f[0]: f[0] = sh
            if sh >= 1.0 and f[2] < 0: f[2] = R.g
            f[1] = sh
        return h


def episodes(tl, g_end):
    """Non-target episodes after a target spell on one island: list of (start, end, codes/units seen)."""
    out = []
    n = 0
    while n < len(tl):
        e = tl[n]
        if n > 0 and e[1] != 1 and tl[n - 1][1] == 1:
            start = e[0]; seen = []
            m = n
            while m < len(tl) and tl[m][1] != 1:
                nxt = tl[m + 1][0] if m + 1 < len(tl) else g_end + STEP
                seen.append((tl[m][0], nxt, tl[m][1], tl[m][2]))
                m += 1
            end = tl[m][0] if m < len(tl) else g_end + STEP
            out.append((start, end, seen))
            n = m
        else:
            n += 1
    return out


def identity_takeovers(tl, g_end, ident):
    """Target episodes followed, before the island is target again, by an identity holder for >= LOSS_MIN
    generations (notes §1.6).  Returns list of dict(start, end, permanent)."""
    out = []
    for start, end, seen in episodes(tl, g_end):
        idt = sum(b - a for a, b, c, u in seen if c == 2 and ident[u])
        if idt >= LOSS_MIN:
            last = seen[-1]
            out.append(dict(start=int(start), end=int(end), ident_gens=int(idt),
                            permanent=bool(end > g_end and last[2] == 2 and ident[last[3]])))
    return out


def secondary_takeovers(tl, g_end, colon_events, ident):
    """Shadow-on-target drift colonizations whose island later leaves target status for >= LOSS_MIN generations."""
    out = []
    eps_ = episodes(tl, g_end)
    for c in colon_events:
        if c['cls'] == 'selected' or c['status_at_arrival'] != 1: continue
        for start, end, seen in eps_:
            if start >= c['g_col'] and end - start >= LOSS_MIN:
                last = seen[-1]
                kind = 'identity' if any(cc == 2 and ident[u] for a, b, cc, u in seen) else (
                    'rival' if any(cc == 2 for a, b, cc, u in seen) else 'unheld')
                out.append(dict(lid=c['lid'], island=c['island'], g_col=c['g_col'], start=int(start), end=int(end),
                                kind=kind, spelling=c['spelling']))
                break
    return out


def cures_at_onset(R, tr, labels0, units0, colon_events, g_end):
    """Rival islands at the onset snapshot: resolution and path (removing-rivals §1.6), and how a cure came about:
    'direct' (a rain lineage that arrived on this island with a predator phenotype against the onset holder colonized
    it before resolution), 'migrant' (a predator step without such a lineage: the predator came by migration), or
    'no-predator' (resolution without a predator step)."""
    S = RR.static(R.LS)
    Tun = sorted(set(int(u) for u, l in zip(units0, labels0) if l == '') | {S['uPB']})
    out = []
    for i, lab in enumerate(labels0):
        if lab in ('', 'unheld'): continue
        x0 = int(units0[i])
        p = RRR.path_of(tr.tl[i], AN.ONSET, x0)
        p.update(island=i, label=lab, x0=x0)
        if p['resolved']:
            pf = RR.predflag_units(x0, Tun, R.LS)
            direct = [c for c in colon_events if c['island'] == i and c['g_col'] <= p['g'] and bool(pf[c['phen']])]
            p['via'] = 'direct' if direct else ('migrant' if p['path'] == 'predator' else 'no-predator')
        out.append(p)
    return out


def cell_job(job):
    cell, rep, gens = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    R = AN.AnnRun(cell, rep)
    info = AN.CELL[cell]
    tr = FateTracker(R, [s for s in SNAPS if s <= gens])
    frozen_from = None
    while R.g < gens:
        R.advance(STEP)
        tr.step()
        if not R.track and R.g >= 2000 and R.g % 500 == 0 and R.frozen():
            cc = R.island_stats(); h = RR.holders(R, cc)
            snap = tr.snapshot(cc, h)
            for s in tr.snaps:
                if s > R.g: tr.snap_out[s] = dict(snap, g=s, frozen_from=R.g)
            frozen_from = R.g
            break
    S = RR.static(R.LS)
    ident = S['ident']
    g_end = R.g
    arr = RRR.arrivals_summary(R, tr, g_end) if R.track else dict(n=0)
    events = arr.get('colonizations') or []
    for c in events:
        f = tr.fate.get((c['lid'], c['island']))
        if f is not None:
            c.update(max_share=f[0], last_share=f[1], g_fix=f[2],
                     fate='fixed' if f[2] >= 0 and f[1] >= 1.0 else ('lost' if f[1] == 0.0 else
                                                                     ('held' if f[1] >= 0.5 else 'minority')),
                     island_code_end=int(tr.tl[c['island']][-1][1]), island_unit_end=int(tr.tl[c['island']][-1][2]))
    mig = []
    lidpos = {}
    for q in range(int(R.nfr[0])):
        lidpos[int(R.fr[q, 4])] = (int(R.fr[q, 1]), int(R.fr[q, 0]))
    for (l, i), gc in tr.colon.items():
        a = lidpos.get(l)
        if a is not None and a[0] != i:
            mig.append(dict(lid=int(l), island=int(i), g_col=int(gc), from_island=a[0], g_arr=a[1]))
    idt, sec = [], []
    for i in range(R.I):
        for z in identity_takeovers(tr.tl[i], g_end, ident):
            z['island'] = i; idt.append(z)
    sec = []
    for i in range(R.I):
        sec += secondary_takeovers(tr.tl[i], g_end, [c for c in events if c['island'] == i], ident)
    s0 = tr.snap_out.get(AN.ONSET, {})
    cures = cures_at_onset(R, tr, s0.get('labels', []), s0.get('holder_unit', []), events, g_end) if s0 else []
    L, Tt = [], []
    for i in range(R.I):
        l, t = RRR.losses(tr.tl[i], g_end)
        L += [(i,) + tuple(z) for z in l]; Tt += [(i,) + tuple(z) for z in t]
    sl = tr.snap_out.get(gens, {})
    return dict(cell=cell, rep=rep, N=R.N, I=R.I, arm=info['arm'], K=info['K'], sched=info['sched'], cls=info['cls'],
                r=R.r, mN=R.mN, gens=gens, last_gen=g_end, frozen_from=frozen_from,
                arrivals_total=int(R.rcount.sum()), arrivals_per_island=R.rcount.tolist(),
                arrivals_by_10k=int(sum(1 for q in range(int(R.nfr[0])) if R.fr[q, 0] < AN.HORIZON)),
                snaps={str(k): v for k, v in tr.snap_out.items()}, colonizations=events, migrant_colonizations=mig,
                by_class=arr.get('by_class', {}), identity_takeovers=idt, secondary=sec, cures=cures, losses=L,
                n_transient=len(Tt), tl=[[list(map(int, e)) for e in t] for t in tr.tl] if R.N * R.I <= 3200 else None,
                n_types=int(R.ntv[0]), time_s=time.time() - t0,
                msg='uot %s id %s tgt %s drift %d sel %d arr %d' % (
                    sl.get('uot'), sl.get('identity'), sl.get('target'),
                    sum(1 for c in events if c['cls'] != 'selected'), sum(1 for c in events if c['cls'] == 'selected'),
                    int(R.rcount.sum())))


def run_pool(fn, jobs, path, workers, key=lambda r: (r['cell'], r['rep']), jkey=lambda j: (j[0], j[1]), tag=''):
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {key(r) for r in rows}
    jobs = [j for j in jobs if jkey(j) not in done]
    log('%s jobs %d (pid %d), already done %d' % (tag, len(jobs), os.getpid(), len(done)))
    if not jobs: return rows
    t0 = time.time()
    with Pool(min(3, workers), maxtasksperchild=4) as pool:
        for r in pool.imap_unordered(fn, jobs):
            rows.append(r)
            tmp = path + '.tmp'
            json.dump(rows, open(tmp, 'w')); os.replace(tmp, path)
            log('%s %s: %s (%.0fs, total %.0fs)' % (tag, key(r), r.get('msg', ''), r['time_s'], time.time() - t0))
    return rows


def cmd_cells(a):
    jobs = []
    for c in a.cells:
        jobs += [(c, rep, a.gens) for rep in range(a.rep0, a.rep0 + a.runs)]
    jobs.sort(key=lambda j: -(AN.CELL[j[0]]['N'] * (2 if AN.CELL[j[0]]['K'] else 1)))
    run_pool(cell_job, jobs, os.path.join(OUT, 'cells_%s.json' % a.out), a.workers, tag='cells')


# ------------------------------------------------------------------------------------------------ assays
def neutral_job(job):
    N, sp, k0, k1 = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    name = 'anA_FB_%d' % N
    if name not in AN.CELL:
        LS = PR.lot_static()
        sfb = LS['names'].index(AN.FB_SP)
        RR.FORCED[name] = (np.full((1, N), sfb, np.int64), np.full((1, N), PV.R_SNON, np.int64),
                           np.full((1, N), int(LS['Hu'][LS['tau'][sfb]]), np.int64))
        AN._reg(name, N, 1, 'forced', 'zero', 0, 'assay')
    R = AN.AnnRun(name, 0, track=True, fcap=2)
    s0 = R.save_state()
    s_idx = R.LS['names'].index(sp)
    out = []
    for k in range(k0, k1):
        R.load_state(s0)
        R.seed = int(PR.kernel_seed(N, 1, 50000 + k))
        R.lin[:] = 0; R.nlin[0] = 0
        j = int(np.random.default_rng([N, k, 77]).integers(N))
        R.inject(0, j, s_idx)
        lid = int(R.nlin[0])
        col5 = -1; colany = -1; gfix = -1; glost = -1; mx = 1
        while R.g < 6 * N:
            R.advance(1)
            c = int(np.count_nonzero(R.lin[0] == lid))
            mx = max(mx, c)
            if c * 2 >= N and colany < 0: colany = R.g
            if c * 2 >= N and col5 < 0 and R.g % STEP == 0: col5 = R.g
            if c == 0: glost = R.g; break
            if c == N: gfix = R.g; break
        out.append((k, col5, colany, gfix, glost, mx, R.g))
    return dict(N=N, sp=sp, k0=k0, k1=k1, rows=out, time_s=time.time() - t0, msg='%d reps' % (k1 - k0))


def cmd_neutral(a):
    jobs = [(a.N, a.sp, k, min(k + a.chunk, a.reps)) for k in range(0, a.reps, a.chunk)]
    run_pool(neutral_job, jobs, os.path.join(OUT, 'assay_%s.json' % a.out), a.workers,
             key=lambda r: (r['N'], r['sp'], r['k0']), jkey=lambda j: (j[0], j[1], j[2]), tag='neutral')


def predator_job(job):
    N, cls, k0, k1, cap = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    name = AN.reg_forced(cls, N, K=0, sched='zero', tag='_assay')
    LS = PR.lot_static()
    S = RR.static(LS)
    s_pred, pt = AN.top_predator(cls, LS)
    R = AN.AnnRun(name, 0, track=True, fcap=2)
    s0 = R.save_state()
    x = AN.FORCED_X[cls][0]
    out = []
    for k in range(k0, k1):
        R.load_state(s0)
        R.seed = int(PR.kernel_seed(N, R.I, (60000 if cls == 'AP' else 70000) + k))
        R.lin[:] = 0; R.nlin[0] = 0
        j = int(np.random.default_rng([N, k, 78]).integers(N))
        R.inject(0, j, s_pred)
        lid = int(R.nlin[0])
        g_est = -1; g_done = -1; tgt_run = 0; g_lost = -1; mx = 1; g_xback = -1
        while R.g < cap:
            R.advance(STEP)
            c0 = int(np.count_nonzero(R.lin[0] == lid))
            call = int(np.count_nonzero(R.lin == lid))
            mx = max(mx, c0)
            if c0 * 2 >= N and g_est < 0: g_est = R.g
            cc = R.island_stats()
            k_ = int(R.maj_k[0]); u = int(R.tunit[k_])
            held = S['sa'][u] == 1 and cc[0] >= 0.5
            if held and S['T'][u]:
                tgt_run += 1
                if tgt_run * STEP > LOSS_MIN: g_done = R.g; break
            else:
                tgt_run = 0
            if call == 0 and g_lost < 0:
                g_lost = R.g
                if u == x: g_xback = R.g; break
        out.append((k, g_est, g_done, g_lost, mx, R.g))
    return dict(N=N, cls=cls, pred=LS['names'][s_pred], pred_mu=float(LS['mu'][s_pred]), k0=k0, k1=k1, rows=out,
                time_s=time.time() - t0, msg='%d reps' % (k1 - k0))


def cmd_predator(a):
    jobs = [(a.N, a.cls, k, min(k + a.chunk, a.reps), a.cap) for k in range(0, a.reps, a.chunk)]
    run_pool(predator_job, jobs, os.path.join(OUT, 'assay_%s.json' % a.out), a.workers,
             key=lambda r: (r['N'], r['cls'], r['k0']), jkey=lambda j: (j[0], j[1], j[2]), tag='predator')


# ------------------------------------------------------------------------------------------------ validation
def cmd_validate(a):
    """§1.7: (1) eps = 0 against the scaling kernel and stored traces at N = 200; (3) the event-indexed constant rate
    against a stored removing-rivals B2 run to 2,000 with its colonization classes.  (2) and (4) are tests."""
    res = {}
    t0 = time.time()
    # (1a) stored scaling runs at N = 200 (r = 100 is native there), S-nonself calibrated (200, 64), reps 0-3, to 2,000
    stored = {(r['cell'], r['rep']): r for r in RRR.stored_rows()}
    bad_tot = 0; n_tot = 0
    for rep in range(a.nrep):
        cell = 'rs_Snon_200_64_cal'
        R = AN.AnnRun(cell, rep, sched=np.zeros(1), r=100)
        assert R.r == RS.RSRun(cell, rep).r == 100
        mine = []
        while R.g < 2000:
            R.advance(10)
            if R.g % 50 == 0:
                mine.append(RRR.stored_trace_fields(R, R.island_stats()))
        n, bad = RRR.compare_trace(mine, [t for t in stored[(cell, rep)]['trace'] if t[0] <= 2000])
        n_tot += n; bad_tot += bad
        log('stored', cell, rep, n, bad)
    res['stored_N200'] = dict(runs=a.nrep, points=n_tot, bad=bad_tot)
    # (3) removing-rivals B2 rain run rr_rain01_200_64 rep 0 to 2,000, event-indexed draws
    rowsB = json.load(gzip.open(os.path.join(RR.ROOT, 'runs', 'removing_rivals', 'lottery_B.json.gz')))
    tgt = [r for r in rowsB if r['cell'] == 'rr_rain01_200_64' and r['rep'] in range(a.nb2)]
    agree = []
    for r in tgt:
        rep = r['rep']
        sch = np.full(10000, 0.1 / 200.0)
        R = AN.AnnRun('rr_rain01_200_64', rep, sched=sch, pairmode=0, r=100, track=True, fcap=RR.FCAP)
        tr = RRR.Tracker(R, [500, 1000, 2000])
        while R.g < 2000:
            R.advance(STEP)
            tr.step()
        arr = RRR.arrivals_summary(R, tr, R.g)
        mine = {(c['lid'], c['island']): (c['g_arr'], c['g_col'], c['cls'], c['status_at_arrival'], c['spelling'])
                for c in arr.get('colonizations') or []}
        theirs = {(c['lid'], c['island']): (c['g_arr'], c['g_col'], c['cls'], c['status_at_arrival'], c['spelling'])
                  for c in (r['arrivals'].get('colonizations') or []) if c['g_col'] <= 2000}
        same_snap = all(r['snaps'][str(g)][k] == tr.snap_out[g][k] for g in (500, 1000, 2000)
                        for k in ('uot', 'target', 'identity', 'exploitable', 'closed_open', 'holder_sp'))
        # stored colonization events were classified at the stored run's end; compare those with g_col <= 2,000
        agree.append(dict(rep=rep, mine=len(mine), theirs=len(theirs), same=sum(1 for k in theirs if mine.get(k) == theirs[k]),
                          missing=sorted(set(theirs) - set(mine))[:5], extra=sorted(set(mine) - set(theirs))[:5],
                          snaps_equal=bool(same_snap), rain=int(R.rcount.sum())))
        log('B2', agree[-1])
    res['b2_reproduction'] = agree
    res['time_s'] = time.time() - t0
    json.dump(res, open(os.path.join(RR.ROOT, 'runs', 'annealed-validate.json'), 'w'), indent=1)
    log(json.dumps(res)[:2000])


def cmd_probe(a):
    out = {}
    for cell in a.cells:
        t0 = time.time()
        R = AN.AnnRun(cell, 0)
        tr = FateTracker(R, [200, 1000, 2000])
        while R.g < a.gens:
            R.advance(STEP); tr.step()
        out[cell] = dict(gens=a.gens, time_s=time.time() - t0, arrivals=int(R.rcount.sum()), n_types=int(R.ntv[0]))
        log(cell, out[cell])
    p = os.path.join(OUT, 'probes.json')
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(out)
    json.dump(old, open(p, 'w'), indent=1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('cells'); s.add_argument('--cells', nargs='+'); s.add_argument('--runs', type=int, default=20)
    s.add_argument('--rep0', type=int, default=0); s.add_argument('--gens', type=int, default=AN.END)
    s.add_argument('--workers', type=int, default=3); s.add_argument('--out', default='main')
    s = sub.add_parser('neutral'); s.add_argument('--N', type=int); s.add_argument('--sp', default='C')
    s.add_argument('--reps', type=int, default=3000); s.add_argument('--chunk', type=int, default=250)
    s.add_argument('--workers', type=int, default=3); s.add_argument('--out', default='neutral')
    s = sub.add_parser('predator'); s.add_argument('--N', type=int); s.add_argument('--cls', default='AP')
    s.add_argument('--reps', type=int, default=100); s.add_argument('--chunk', type=int, default=10)
    s.add_argument('--cap', type=int, default=3000)
    s.add_argument('--workers', type=int, default=3); s.add_argument('--out', default='predator')
    s = sub.add_parser('validate'); s.add_argument('--nrep', type=int, default=4); s.add_argument('--nb2', type=int, default=2)
    s = sub.add_parser('probe'); s.add_argument('--cells', nargs='+'); s.add_argument('--gens', type=int, default=2000)
    a = ap.parse_args()
    {'cells': cmd_cells, 'neutral': cmd_neutral, 'predator': cmd_predator, 'validate': cmd_validate,
     'probe': cmd_probe}[a.cmd](a)


if __name__ == '__main__':
    main()
