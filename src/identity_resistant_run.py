"""Driver for the identity-resistant target (notes/identity-resistant.md).

    python3 src/identity_resistant_run.py exec [--workers 3]            # executed check of the partition (§1.2)
    python3 src/identity_resistant_run.py static                        # partition, guard, masses, occupancy, M1 relations
    python3 src/identity_resistant_run.py validate                      # §1.9 reproduction checks
    python3 src/identity_resistant_run.py assay --N 200 --reps 1000     # M1 forced TwinD challenges (and C baselines)
    python3 src/identity_resistant_run.py cells --cells NAME ... --out NAME [--runs 20] [--workers 3]
    python3 src/identity_resistant_run.py probe --cells NAME ... --gens 2000
Rows go to runs/identity_resistant/*.json.gz (summaries per run).
"""
import argparse
import gzip
import json
import os
import sys
import time
from collections import Counter, defaultdict
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
import annealed_run as AR
import pangaea as PG
import identity_resistant as IRM

ROOT = IRM.ROOT
OUT = IRM.OUT
os.makedirs(OUT, exist_ok=True)
STEP = RRR.STEP
LOSS_MIN = RRR.LOSS_MIN


def log(*a):
    print(*a, flush=True)


def r5(x):
    return None if x is None else round(float(x), 5)


# ------------------------------------------------------------------------------------------------ executed check
_EX = {}


def _exec_init():
    sys.setrecursionlimit(1000000)
    PR._vainit()
    _EX['U'] = PR._VA['U']
    _EX['U'].cat = PR.lot_static()['cat']


def _exec_job(items):
    import lt_code as L
    U = _EX['U']
    out = []
    for t, q, wt, wq in items:
        if len(L.CACHE) > 200000: L.CACHE.clear()
        x = PR.unit_prog_nm(U, t, wt); y = PR.unit_prog_nm(U, q, wq)
        if x is None or y is None:
            out.append((t, q, wt, wq, None, None)); continue
        ax, _ = L.play(x.term(), y.term(), PR.K)
        ay, _ = L.play(y.term(), x.term(), PR.K)
        out.append((t, q, wt, wq, 'D' if ax == 'BOT' else ax, 'D' if ay == 'BOT' else ay))
    return out


def cmd_exec(a):
    """Every (target unit, challenge unit) pair, both directions, on spellings 0 and 1 of each run tree."""
    t0 = time.time()
    LS = PR.lot_static()
    P = IRM.partition(LS, use_exec=False)
    A = RR.static(LS)['A']
    cat = LS['cat']; units = LS['meta']['units']
    items = []
    for t in P['Tu'].tolist():
        nt = len(cat.members[units[t][0]])
        for q in P['chal'].tolist():
            nq = len(cat.members[units[q][0]])
            for wt in range(min(2, nt)):
                for wq in range(min(2, nq)):
                    items.append((int(t), int(q), wt, wq))
    chunks = [items[i:i + 200] for i in range(0, len(items), 200)]
    res = []
    with Pool(min(3, a.workers), initializer=_exec_init) as pool:
        for r in pool.imap_unordered(_exec_job, chunks):
            res += r
    dis = []
    exploit = defaultdict(bool)
    for t, q, wt, wq, ax, ay in res:
        if ax is None: continue
        at, aq = int(A[t, q]), int(A[q, t])
        et, eq = int(ax == 'C'), int(ay == 'C')
        if (at, aq) != (et, eq): dis.append(dict(t=t, q=q, wt=wt, wq=wq, table=[at, aq], exec=[et, eq]))
        if et == 1 and eq == 0: exploit[t] = True
    ex_exec = {str(int(t)): bool(exploit[int(t)]) for t in P['Tu'].tolist()}
    changed = [int(t) for t, e0 in zip(P['Tu'].tolist(), P['ex_ideal'].tolist()) if bool(e0) != ex_exec[str(int(t))]]
    out = dict(pairs=len(res), plays=2 * len(res), fuel=PR.K, disagreements=dis[:50], n_disagreements=len(dis),
               exploitable_exec=ex_exec, n_exploitable_exec=sum(ex_exec.values()),
               n_exploitable_ideal=int(P['ex_ideal'].sum()), class_changes=changed, time_s=time.time() - t0)
    json.dump(out, open(IRM.EXEC_PATH, 'w'), indent=1)
    log(json.dumps({k: v for k, v in out.items() if k not in ('exploitable_exec',)})[:3000])


# ------------------------------------------------------------------------------------------------ static
def cmd_static(a):
    LS = PR.lot_static()
    S = RR.static(LS)
    P = IRM.partition(LS)
    A, sa, T = S['A'], S['sa'], S['T']
    names, tau, mu = LS['names'], LS['tau'], LS['mu']
    cat = LS['cat']; units = LS['meta']['units']; utau = np.asarray(LS['st']['utau'])
    O = np.asarray(LS['st']['O'])
    rows = []
    for u, e in zip(P['Tu'].tolist(), P['ex'].tolist()):
        t = int(utau[u]); sps = cat.members[t]
        g = [IRM.guarded(names[k]) for k in sps]
        gx = [IRM.guarded(names[k], True) for k in sps]
        n_any = int(((A[u, O] == 1) & (A[O, u] == 0)).sum())
        rows.append(dict(unit=int(u), tree=t, exploitable=bool(e), guarded=all(g), guard_tree_const=all(g) == any(g),
                         guarded_excl=all(gx), name=names[sps[0]], mass=float(mu[sps].sum()), n_exploiters_any=n_any))
    res = [r for r in rows if not r['exploitable']]; exr = [r for r in rows if r['exploitable']]
    out = dict(n_target=len(rows), n_exploitable=len(exr), n_resistant=len(res),
               challenge=[int(q) for q in P['chal']], masses=P['mass'],
               resistant_guarded=sum(r['guarded'] for r in res), exploitable_guarded=sum(r['guarded'] for r in exr),
               guard_tree_constant=all(r['guard_tree_const'] for r in rows),
               resistant_unguarded=[r['name'] for r in res if not r['guarded']],
               guarded_universally_unexploitable=sum(1 for r in res if r['guarded'] and r['n_exploiters_any'] == 0),
               unguarded_res_universally_unexploitable=sum(1 for r in res if not r['guarded'] and r['n_exploiters_any'] == 0),
               rows=rows)
    # priors: masses of classes and the marginal check of the piece tables
    pri = {}
    for p in IRM.PRIORS:
        m = IRM.prior_mass(p, LS)
        d = {}
        for base in ('np', 'kern'):
            tm = IRM.table_mass(p, base, LS)
            d['maxdiff_%s' % base] = float(np.abs(tm - m).max())
            d['pieces_%s' % base] = int(len(IRM.piece_table(p, base, LS)[0]))
        pri[p] = dict(total=float(m.sum()), E=float(m[P['sp_E']].sum()), Res=float(m[P['sp_Res']].sum()),
                      Q=float(m[P['sp_Q']].sum()), UC=float(m[P['sp_UC'] & ~P['sp_E'] & ~P['sp_Res']].sum()),
                      FB=float(m[tau == tau[names.index('if(CHK(them,me,C),C,D)')]].sum()), **d)
    out['priors'] = pri
    # M1 static relations: the TwinD founder's phenotype against each assay holder
    out['m1_holders'] = m1_static(LS)
    p = os.path.join(ROOT, 'runs', 'identity-resistant-static.json')
    json.dump(out, open(p, 'w'), indent=1)
    log(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1)[:6000])


def m1_holders(LS):
    """(label, class, unit, spelling) of the M1 holders: the exploitable / resistant choices of notes §1.8."""
    S = RR.static(LS)
    names = LS['names']
    P = IRM.partition(LS)
    ck = json.load(gzip.open(os.path.join(ROOT, 'runs', 'removing_rivals', 'ckpt_rows.json.gz')))
    occ = Counter()
    for r in ck:
        for u, sp, o in zip(r['holder_unit'], r['holder_sp'], r['ontgt']):
            if o and P['exu'][u]: occ[(u, sp)] += 1
    (xu, xs) = [k for k, n in occ.most_common() if k[0] not in (31, 87)][0]     # most-held other exploitable unit
    H = [('ex_31', 'ex', 31, names.index('if(CHK(them,^D,D),C,D)')),
         ('ex_87', 'ex', 87, names.index('if(CHK(them,me,C),C,if(CHK(them,them,C),C,D))')),
         ('ex_top', 'ex', int(xu), int(xs)),
         ('res_FB', 'res', 3, names.index('if(CHK(them,me,C),C,D)')),
         ('res_PB', 'res', int(S['uPB']), int(S['kPB'])),
         ('res_183', 'res', 183, names.index('if(or(CHK(them,me,C),CHK(me,^D,C)),C,D)'))]
    return H


def m1_static(LS):
    S = RR.static(LS)
    A = S['A']
    P = IRM.partition(LS)
    out = []
    for lab, cls, x, sx in m1_holders(LS):
        assert IRM.unit_class(x, P) == cls, (lab, x)
        per = []
        for q in LS['Q'].tolist():
            p = RR.phen_cached(int(q), x, sx, LS)
            d = RRR.upay(p, x, S) - RRR.uself(x, S)
            per.append(dict(q=LS['names'][q], phen=int(p), cls='selected' if d > 1e-9 else ('neutral' if d > -1e-9 else 'deleterious'),
                            x_coop=int(A[x, p]), p_coop=int(A[p, x]), p_ident=bool(LS['ident'][p])))
        pc = RR.phen_cached(LS['names'].index('C'), x, sx, LS)
        dc = RRR.upay(pc, x, S) - RRR.uself(x, S)
        out.append(dict(label=lab, cls=cls, unit=x, spelling=LS['names'][sx], guarded=IRM.guarded(LS['names'][sx]),
                        Q=per, Q_classes=sorted(set(z['cls'] for z in per)),
                        C_phen=int(pc), C_cls='selected' if dc > 1e-9 else ('neutral' if dc > -1e-9 else 'deleterious')))
    return out


# ------------------------------------------------------------------------------------------------ Part I: fission-fusion
def merged_shares(R, P):
    nt = int(R.ntv[0])
    gc = R.counts[:, :nt].sum(0).astype(float)
    tot = gc.sum()
    u = R.tunit[:nt]
    S = RR.static(R.LS)
    return dict(T=float(gc[S['T'][u]].sum() / tot), res=float(gc[P['resu'][u]].sum() / tot),
                ex=float(gc[P['exu'][u]].sum() / tot))


def island_block(R, LS, P, cache):
    cc = R.island_stats()
    h = RR.holders(R, cc)
    lab, mass, cache = RR.classify_rivals(R, h, LS, cache)
    hu = [int(R.tunit[k]) for k in h['maj']]
    res, ex = IRM.island_targets(hu, lab, P)
    c = Counter(lab)
    snap = dict(g=R.g, uot=bool(h['uot']), uo=bool(h['uo']), target=int(h['ontgt'].sum()), held=int(h['held'].sum()),
                identity=c.get('identity', 0), exploitable=c.get('exploitable', 0), closed_open=c.get('closed-open', 0),
                closed_nonopen=c.get('closed-nonopen', 0), unheld=c.get('unheld', 0), tgt_res=res, tgt_ex=ex,
                pcc=float(cc.mean()), eff=int((cc >= 0.95).sum()), holder_unit=hu, labels=lab)
    snap['uot70'] = IRM.uot70(snap, P)
    snap['est'] = IRM.establishment(R.sp0, hu, lab, LS, P)
    return snap, cache


def ff_job(job):
    cell, rep = job[:2]
    gens = job[2] if len(job) > 2 else IRM.IR[cell]['horizon']
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    info = IRM.IR[cell]
    R = PG.PGRun(cell, rep)
    LS = R.LS
    P = IRM.partition(LS)
    seeded = {k: int(v) for k, v in Counter(IRM.sp_class(int(s), P) for s in R.sp0.ravel()).items()}
    pre = None
    cache = {}
    trace = []
    max_ident_after = 0.0; ident_zero = -1; frozen_at = -1
    while R.g < gens:
        R.advance(10)
        g = R.g
        if g == info['merge_at']:
            pre, cache = island_block(R, LS, P, cache)
            R.merge(PG.kernel_seed_pg(R.N * R.I, 1, rep) ^ 0x5DEECE66D)
        if g % 50 and g not in (info['merge_at'],): continue
        cc = R.island_stats()
        dec = PG.decompose(R, cc)
        ms = merged_shares(R, P)
        if R.I == 1:
            max_ident_after = max(max_ident_after, dec['ident'])
            if dec['ident'] == 0 and ident_zero < 0: ident_zero = g
        trace.append([g, r5(dec['pcc']), r5(dec['M']), r5(dec['target']), r5(dec['ident']), r5(ms['res']),
                      r5(ms['ex']), int(dec['h_open'])])
        if R.I == 1 and g >= 250 and R.frozen():
            frozen_at = g
            break
    cc = R.island_stats()
    fin = PG.decompose(R, cc, closure=True)
    ms = merged_shares(R, P)
    univ = bool(fin['M'] >= 0.95)
    fin_out = dict(pcc=fin['pcc'], M=fin['M'], h_sp=fin['h_sp'], h_open=fin['h_open'], universal=univ,
                   uo=bool(fin['universal_open']), target_dec=fin['target'], ident=fin['ident'], Q=fin['Q'],
                   T_share=ms['T'], res_share=ms['res'], ex_share=ms['ex'], status=fin.get('status'),
                   uot235=bool(univ and ms['T'] >= 0.95), uot70=bool(univ and ms['res'] >= 0.95),
                   lost=bool(fin.get('status') == 'lost' or fin['coop'] == 0))
    return dict(cell=cell, rep=rep, part='I', prior=info['prior'], spon=info['spon'], gens=gens, last_gen=R.g,
                frozen_at=frozen_at, seeded=seeded, pre=pre, final=fin_out, max_ident_after=max_ident_after,
                ident_zero=ident_zero, trace=trace, n_types=int(R.ntv[0]), time_s=time.time() - t0,
                msg='pre id %s tgt %s/%s | uo %s uot %s uot70 %s T %.3f ex %.4f id %.4f' % (
                    pre['identity'] if pre else None, pre['tgt_res'] if pre else None, pre['tgt_ex'] if pre else None,
                    fin_out['uo'], fin_out['uot235'], fin_out['uot70'], ms['T'], ms['ex'], fin['ident']))


# ------------------------------------------------------------------------------------------------ Part II: islands
def isl_job(job):
    cell, rep = job[:2]
    gens = job[2] if len(job) > 2 else IRM.IR[cell]['horizon']
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    info = IRM.IR[cell]
    R = RR.RRRun(cell, rep)
    LS = R.LS
    P = IRM.partition(LS)
    seeded = {k: int(v) for k, v in Counter(IRM.sp_class(int(s), P) for s in R.sp0.ravel()).items()}
    snaps = [s for s in (200, 500, 1000, 2000, 5000, 10000) if s <= gens]
    tr = RRR.Tracker(R, snaps)
    trace = []
    frozen_from = None
    while R.g < gens:
        R.advance(STEP)
        tr.step()
        if R.g % 50 == 0 and R.g <= 2000:
            trace.append(RRR.stored_trace_fields(R, R.island_stats()))
        if R.g >= 2000 and R.g % 500 == 0 and R.frozen():
            cc = R.island_stats(); h = RR.holders(R, cc)
            snap = tr.snapshot(cc, h)
            for s in snaps:
                if s > R.g: tr.snap_out[s] = dict(snap, g=s, frozen_from=R.g)
            frozen_from = R.g
            break
    out = {}
    for g, s in tr.snap_out.items():
        res, ex = IRM.island_targets(s['holder_unit'], s['labels'], P)
        s = dict(s, tgt_res=res, tgt_ex=ex, uot70=IRM.uot70(s, P))
        if g in (200, 2000):
            s['est'] = IRM.establishment(R.sp0, s['holder_unit'], s['labels'], LS, P)
        out[str(g)] = s
    L_, Tt = [], []
    for i in range(R.I):
        l, t = RRR.losses(tr.tl[i], R.g)
        L_ += [(i,) + tuple(z) for z in l]; Tt += [(i,) + tuple(z) for z in t]
    idt = []
    for i in range(R.I):
        for z in AR.identity_takeovers(tr.tl[i], R.g, RR.static(LS)['ident']):
            z['island'] = i; idt.append(z)
    sl = out.get(str(gens), {})
    return dict(cell=cell, rep=rep, part='II', prior=info['prior'], spon=info['spon'], gens=gens, last_gen=R.g,
                frozen_from=frozen_from, seeded=seeded, snaps=out, losses=L_, n_transient=len(Tt),
                identity_takeovers=idt, trace=trace, n_types=int(R.ntv[0]), time_s=time.time() - t0,
                msg='uot2k %s uot %s uot70 %s tgt %s/%s id %s co %s unheld %s' % (
                    out.get('2000', {}).get('uot'), sl.get('uot'), sl.get('uot70'), sl.get('tgt_res'), sl.get('tgt_ex'),
                    sl.get('identity'), sl.get('closed_open'), sl.get('unheld')))


# ------------------------------------------------------------------------------------------------ Part III: rain
def tgt_island_gens(tl, g_end, P):
    """Target island-generations by holder class (res / ex) from an island timeline."""
    out = {'res': 0, 'ex': 0}
    for n, e in enumerate(tl):
        if e[1] != 1: continue
        nxt = tl[n + 1][0] if n + 1 < len(tl) else g_end
        k = IRM.unit_class(int(e[2]), P)
        if k: out[k] += nxt - e[0]
    return out


def holder_before(tl, g):
    """The last target entry of the timeline strictly before generation g."""
    last = None
    for e in tl:
        if e[0] >= g: break
        if e[1] == 1: last = e
    return last


def rain_job(job):
    cell, rep = job[:2]
    gens = job[2] if len(job) > 2 else AN.END
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    info = IRM.IR[cell]
    R = IRM.IRAnnRun(cell, rep)
    LS = R.LS
    S = RR.static(LS)
    P = IRM.partition(LS)
    A = S['A']; ident = S['ident']
    seeded = {k: int(v) for k, v in Counter(IRM.sp_class(int(s), P) for s in R.sp0.ravel()).items()}
    tr = AR.FateTracker(R, [s for s in AR.SNAPS if s <= gens])
    while R.g < gens:
        R.advance(STEP)
        tr.step()
    g_end = R.g
    arr = RRR.arrivals_summary(R, tr, g_end) if R.track else dict(n=0)
    events = arr.get('colonizations') or []
    for c in events:
        f = tr.fate.get((c['lid'], c['island']))
        if f is not None:
            c.update(max_share=f[0], last_share=f[1], g_fix=f[2])
    n = int(R.nfr[0])
    fr = R.fr[:n]
    # exposure by class
    expo = Counter(IRM.sp_class(int(s), P) for s in fr[:, 2].tolist())
    # identity arrivals: status of the island and drift class against its majority
    qarr = []
    qset = set(LS['Q'].tolist())
    for q in range(n):
        s = int(fr[q, 2])
        if s not in qset: continue
        g, i, mk = int(fr[q, 0]), int(fr[q, 1]), int(fr[q, 3])
        x = int(R.tunit[mk]); sx = int(R.tsp[mk])
        p = RR.phen_cached(s, x, sx, LS)
        d = RRR.upay(p, x, S) - RRR.uself(x, S)
        st = RRR.status_at(tr.tl[i], g)
        code = st[1] if st else -1
        qarr.append(dict(g=g, island=i, lid=int(fr[q, 4]), x=x, x_cls=IRM.unit_class(x, P) if code == 1 else '',
                         status=int(code), cls='selected' if d > 1e-9 else ('neutral' if d > -1e-9 else 'deleterious'),
                         phen_ident=bool(ident[p])))
    # identity takeovers of target islands and their attribution
    idt = []
    qnames = set(LS['names'][q] for q in qset)
    for i in range(R.I):
        for z in AR.identity_takeovers(tr.tl[i], g_end, ident):
            z['island'] = i
            hb = holder_before(tr.tl[i], z['start'])
            z['holder_before'] = int(hb[2]) if hb else -1
            z['holder_cls'] = IRM.unit_class(int(hb[2]), P) if hb else ''
            col = [c for c in events if c['island'] == i and c['spelling'] in qnames and
                   z['start'] - 200 <= c['g_col'] <= z['end']]
            if col:
                z['attr'] = 'prey' if any(c['cls'] == 'selected' for c in col) else 'arrival-drift'
            else:
                z['attr'] = 'migrant'
            idt.append(z)
    # target island-generations by holder class
    tig = Counter()
    for i in range(R.I):
        for k, v in tgt_island_gens(tr.tl[i], g_end, P).items(): tig[k] += v
    # drift colonizations of target islands split by holder class and colonizer phenotype
    dsplit = Counter()
    dH = P['dH']
    for c in events:
        if c['cls'] == 'selected' or c['status_at_arrival'] != 1: continue
        hc = IRM.unit_class(int(c['x']), P) or 'nt'
        p = int(c['phen'])
        pc = 'UC' if (A[p, dH] == 1 and S['sa'][p] == 1) else ('E' if P['exu'][p] else ('Res' if P['resu'][p] else 'other'))
        dsplit['%s>%s' % (hc, pc)] += 1
    # snapshots with uot70 and occupancy
    snaps = {}
    for g, s in tr.snap_out.items():
        res, ex = IRM.island_targets(s['holder_unit'], s['labels'], P)
        snaps[str(g)] = dict(s, tgt_res=res, tgt_ex=ex, uot70=IRM.uot70(s, P))
    sec = []
    for i in range(R.I):
        sec += AR.secondary_takeovers(tr.tl[i], g_end, [c for c in events if c['island'] == i], ident)
    sl = snaps.get(str(gens), {})
    return dict(cell=cell, rep=rep, part='III', prior=info['prior'], sched=info['sched'], N=R.N, I=R.I, gens=gens,
                last_gen=g_end, seeded=seeded, arrivals_total=int(R.rcount.sum()), exposure=dict(expo),
                identity_arrivals=qarr, colonizations=events, by_class=arr.get('by_class', {}),
                identity_takeovers=idt, secondary=sec, tgt_island_gens=dict(tig), drift_split=dict(dsplit),
                snaps=snaps, n_types=int(R.ntv[0]), time_s=time.time() - t0,
                msg='uot %s uot70 %s id %s tgt %s/%s drift %d qarr %d idt %s' % (
                    sl.get('uot'), sl.get('uot70'), sl.get('identity'), sl.get('tgt_res'), sl.get('tgt_ex'),
                    sum(1 for c in events if c['cls'] != 'selected'), len(qarr),
                    ','.join(z['attr'] for z in idt) or '-'))


# ------------------------------------------------------------------------------------------------ pool
def any_job(job):
    part = IRM.IR[job[0]]['part']
    return {'I': ff_job, 'II': isl_job, 'III': rain_job}[part](job)


def run_pool(fn, jobs, path, workers, key=lambda r: (r['cell'], r['rep']), jkey=lambda j: (j[0], j[1]), tag=''):
    rows = json.load(gzip.open(path)) if os.path.exists(path) else []
    done = {key(r) for r in rows}
    jobs = [j for j in jobs if jkey(j) not in done]
    log('%s jobs %d (pid %d), already done %d' % (tag, len(jobs), os.getpid(), len(done)))
    if not jobs: return rows
    t0 = time.time()
    with Pool(min(3, workers), maxtasksperchild=4) as pool:
        for r in pool.imap_unordered(fn, jobs):
            rows.append(r)
            tmp = path + '.tmp'
            with gzip.open(tmp, 'wt') as f: json.dump(rows, f)
            os.replace(tmp, path)
            log('%s %s: %s (%.0fs, total %.0fs)' % (tag, key(r), r.get('msg', ''), r['time_s'], time.time() - t0))
    return rows


def cmd_cells(a):
    jobs = []
    for c in a.cells:
        jobs += [(c, rep) for rep in range(a.rep0, a.rep0 + a.runs)]
    cost = lambda j: {'I': 1, 'II': 2, 'III': 3}[IRM.IR[j[0]]['part']] * IRM.IR[j[0]]['N']
    jobs.sort(key=lambda j: (-cost(j), j[1]))
    run_pool(any_job, jobs, os.path.join(OUT, 'cells_%s.json.gz' % a.out), a.workers, tag='cells')


# ------------------------------------------------------------------------------------------------ M1 assays
def assay_job(job):
    """One island of N, every individual the holder (unit, spelling, S-nonself); inject one fresh founder of spelling
    `inj` per replicate; until loss, takeover (the lineage holds >= 0.5 of the island for >= LOSS_MIN generations at
    5-generation checkpoints), fixation, or the cap."""
    lab, x, sx, inj, N, k0, k1, cap = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    name = 'irA_%s_%d' % (lab, N)
    if name not in AN.CELL:
        RR.FORCED[name] = (np.full((1, N), sx, np.int64), np.full((1, N), PV.R_SNON, np.int64),
                           np.full((1, N), x, np.int64))
        AN._reg(name, N, 1, 'forced', 'zero', 0, 'assay')
    R = AN.AnnRun(name, 0, track=True, fcap=2)
    s0 = R.save_state()
    LS = R.LS
    s_idx = LS['names'].index(inj)
    salt = 80000 + 20000 * (IRM.q_reps(LS).index(inj) if inj != 'C' else 4)
    out = []
    for k in range(k0, k1):
        R.load_state(s0)
        R.seed = int(PR.kernel_seed(N, 1, salt + k))
        R.lin[:] = 0; R.nlin[0] = 0
        j = int(np.random.default_rng([N, k, 79]).integers(N))
        R.inject(0, j, s_idx)
        lid = int(R.nlin[0])
        g_est = -1; g_take = -1; g_fix = -1; g_lost = -1; mx = 1; run = 0
        while R.g < cap:
            R.advance(1)
            c = int(np.count_nonzero(R.lin[0] == lid))
            mx = max(mx, c)
            if c * 2 >= N and g_est < 0: g_est = R.g
            if R.g % STEP == 0:
                run = run + 1 if c * 2 >= N else 0
                if run * STEP > LOSS_MIN and g_take < 0: g_take = R.g
            if c == 0: g_lost = R.g; break
            if c == N: g_fix = R.g; break
        out.append((k, g_est, g_take, g_fix, g_lost, mx, R.g))
    return dict(lab=lab, x=x, inj=inj, N=N, k0=k0, k1=k1, rows=out, time_s=time.time() - t0, msg='%d reps' % (k1 - k0))


def cmd_assay(a):
    LS = PR.lot_static()
    H = m1_holders(LS)
    jobs = []
    for lab, cls, x, sx in H:
        if a.only and lab not in a.only: continue
        for inj in (IRM.q_reps(LS) + (['C'] if a.C and a.N == 200 else [])):
            reps = a.reps if inj != 'C' else a.creps
            for k in range(0, reps, a.chunk):
                jobs.append((lab, x, sx, inj, a.N, k, min(k + a.chunk, reps), a.cap))
    run_pool(assay_job, jobs, os.path.join(OUT, 'assay_%s.json.gz' % a.out), a.workers,
             key=lambda r: (r['lab'], r['inj'], r['N'], r['k0']), jkey=lambda j: (j[0], j[3], j[4], j[5]), tag='assay')


# ------------------------------------------------------------------------------------------------ validation (§1.9)
def cmd_validate(a):
    t0 = time.time()
    res = {}
    LS = PR.lot_static()
    # 3a. Part I-L-unsponsored against the stored Pangaea fission-fusion rows (decomposition fields at common g)
    F = {r['rep']: r for r in json.load(gzip.open(os.path.join(ROOT, 'runs', 'pangaea', 'lottery_F.json.gz')))
         if r['cell'] == IRM.STORED_I}
    ff = []
    for rep in range(a.nrep):
        r = ff_job((IRM.reg_ff('L', False), rep, 2200))
        st = {t['g']: t for t in F[rep]['trace']}
        n = bad = 0
        for t in r['trace']:
            s = st.get(t[0])
            if s is None: continue
            n += 1
            if any(abs((x or 0) - (s[k] or 0)) > 1e-4 for x, k in zip((t[1], t[2], t[3], t[4]), ('pcc', 'M', 'target', 'ident'))):
                bad += 1
        ff.append(dict(rep=rep, points=n, bad=bad, last_gen=r['last_gen'], stored_last=F[rep]['last_gen']))
        log('ff', ff[-1])
    res['ff'] = ff
    # 3b. Part II-L against the stored scaling traces to 2,000 and removing-rivals' sponsored snapshots
    stored = {(r['cell'], r['rep']): r for r in RRR.stored_rows()}
    isl = []
    for rep in range(a.nrep):
        r = isl_job((IRM.reg_isl('L', False), rep, 2000))
        n, bad = RRR.compare_trace([tuple(t) for t in r['trace']],
                                   [t for t in stored[('rs_Snon_200_64_cal', rep)]['trace'] if t[0] <= 2000])
        isl.append(dict(rep=rep, points=n, bad=bad))
        log('isl', isl[-1])
    Asp = {r['rep']: r for r in json.load(gzip.open(os.path.join(ROOT, 'runs', 'removing_rivals', 'lottery_A.json.gz')))
           if r['cell'] == 'rr_spon_200_64'}
    for rep in range(min(2, a.nrep)):
        r = isl_job((IRM.reg_isl('L', True), rep, 2000))
        same = {k: r['snaps']['2000'][k] == Asp[rep]['snaps']['2000'][k]
                for k in ('uot', 'target', 'identity', 'exploitable', 'closed_open', 'holder_sp')}
        isl.append(dict(rep=rep, sponsored=True, same=same))
        log('isl spon', isl[-1])
    res['isl'] = isl
    # 3c. Part III-L against stored annealed an_i_800 rows to 2,000
    M = {(r['cell'], r['rep']): r for r in json.load(gzip.open(os.path.join(ROOT, 'runs', 'annealed', 'cells_main.json.gz')))}
    rn = []
    for rep in range(min(2, a.nrep)):
        r = rain_job((IRM.reg_rain('L', 'ann', 800), rep, 2000))
        s = M[('an_i_800', rep)]
        same = {k: r['snaps']['2000'][k] == s['snaps']['2000'][k]
                for k in ('uot', 'target', 'identity', 'exploitable', 'closed_open', 'holder_sp', 'holder_unit')}
        mine = sorted((c['lid'], c['island'], c['g_arr'], c['g_col'], c['cls']) for c in r['colonizations'] if c['g_col'] <= 2000)
        theirs = sorted((c['lid'], c['island'], c['g_arr'], c['g_col'], c['cls']) for c in s['colonizations'] if c['g_col'] <= 2000)
        rn.append(dict(rep=rep, same=same, colon_mine=len(mine), colon_stored=len(theirs), colon_equal=mine == theirs))
        log('rain', rn[-1])
    res['rain'] = rn
    res['time_s'] = time.time() - t0
    json.dump(res, open(os.path.join(ROOT, 'runs', 'identity-resistant-validate.json'), 'w'), indent=1)
    log(json.dumps(res)[:3000])


def cmd_probe(a):
    out = {}
    for cell in a.cells:
        t0 = time.time()
        r = any_job((cell, 990, a.gens))
        out[cell] = dict(gens=a.gens, time_s=time.time() - t0, msg=r['msg'])
        log(cell, out[cell])
    p = os.path.join(OUT, 'probes.json')
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(out)
    json.dump(old, open(p, 'w'), indent=1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('exec'); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('static')
    s = sub.add_parser('validate'); s.add_argument('--nrep', type=int, default=3)
    s = sub.add_parser('assay'); s.add_argument('--N', type=int, default=200); s.add_argument('--reps', type=int, default=1000)
    s.add_argument('--creps', type=int, default=1000); s.add_argument('--C', type=int, default=1)
    s.add_argument('--chunk', type=int, default=100); s.add_argument('--cap', type=int, default=3000)
    s.add_argument('--only', nargs='*'); s.add_argument('--workers', type=int, default=3); s.add_argument('--out', default='m1')
    s = sub.add_parser('cells'); s.add_argument('--cells', nargs='+'); s.add_argument('--runs', type=int, default=20)
    s.add_argument('--rep0', type=int, default=0); s.add_argument('--workers', type=int, default=3)
    s.add_argument('--out', default='main')
    s = sub.add_parser('probe'); s.add_argument('--cells', nargs='+'); s.add_argument('--gens', type=int, default=2000)
    a = ap.parse_args()
    {'exec': cmd_exec, 'static': cmd_static, 'validate': cmd_validate, 'assay': cmd_assay, 'cells': cmd_cells,
     'probe': cmd_probe}[a.cmd](a)


if __name__ == '__main__':
    main()
