"""Driver for cliques on a Pangaea (notes/pangaea.md, predictions/2026-10-16-pangaea.md).

    python3 src/pangaea_run.py validate [--reps 3]          # draw-for-draw against stored scaling rows (§1.7)
    python3 src/pangaea_run.py kernelcheck                    # overlap-free draws, founder identities, merge
    python3 src/pangaea_run.py determ                         # deterministic family dynamics (H, certificates saturated)
    python3 src/pangaea_run.py smoke --cells ... --gens 200   # cost probes on a discarded replicate (990)
    python3 src/pangaea_run.py lottery --cells ... --out NAME [--ext 1]
Rows go to runs/pangaea/*.json (summaries); nothing large.
"""
import argparse
import gzip
import hashlib
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
import pangaea as PG
import pangaea_kern as PK

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'pangaea')
os.makedirs(OUT, exist_ok=True)
SNAPS = (200, 500, 1000, 2000, 5000, 10000)
EXT_NONE, EXT_ALL, EXT_IF_NOT_UO, EXT_IF_UNRESOLVED = 0, 1, 2, 3


def log(*a):
    print(*a, flush=True)


def r4(x):
    return None if x is None else round(float(x), 5)


# ------------------------------------------------------------------------------------------------ one run
def founder_meta(R):
    LS = R.LS
    sp0 = R.sp0
    X = PG.statics(LS)
    flat = np.sort(sp0.ravel())
    h = hashlib.sha1(flat.tobytes()).hexdigest()[:16]
    q = np.isin(sp0, X['Q_sp'])
    qsp = {LS['names'][int(s)]: int(n) for s, n in zip(*np.unique(sp0[q], return_counts=True))}
    return dict(founder_hash=h, seeded_Q=int(q.sum()), Q_isl=q.sum(1).tolist() if R.I > 1 else [int(q.sum())],
                Q_spellings=qsp, seeded_R=int(np.isin(sp0, X['R_sp']).sum()),
                donors=int((R.rule0 == PV.R_H).sum()) if (R.rule0 == PV.R_C).any() else 0,
                cls0=[int(n) for n in np.bincount(X['cls'][sp0.ravel()], minlength=len(PG.CLASSES))])


def track_ids(R):
    """Spellings whose extinction is logged: R (prudent core), Q (clique identities), BR (bridges); only those seeded."""
    X = PG.statics(R.LS)
    seeded = set(np.unique(R.sp0).tolist())
    out = {}
    for tag, arr in (('R', X['R_sp']), ('Q', X['Q_sp']), ('BR', X['BR_sp'])):
        out[tag] = np.array([s for s in arr.tolist() if s in seeded], np.int64)
    return out


def island_part(R, cc):
    det = RSR.holders_detail(R, cc)
    cl = det['cl']
    ident_isl = sum(1 for i in range(R.I) if det['held'][i] and det['ident'][det['hol'][i]])
    return det, dict(uo=bool(cl['universal_open']), cause=cl['cause'], held=int(det['held'].sum()),
                     ident_isl=int(ident_isl), isl95=int((cc >= 0.95).sum()),
                     rival_isl=int(sum(1 for f in cl['fail'] if f == 'rival')),
                     unheld_isl=int(sum(1 for f in cl['fail'] if f == 'unheld')))


def lottery_job(job):
    cell, rep, gens, ext = job[:4]
    tmax = job[4] if len(job) > 4 else 0
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    info = PG.PG[cell]
    R = PG.PGRun(cell, rep)
    LS = R.LS
    meta = founder_meta(R)
    ids = track_ids(R)
    ext_max = {tag: np.zeros(len(a), np.int64) for tag, a in ids.items()}
    ext_gen = {tag: -np.ones(len(a), np.int64) for tag, a in ids.items()}
    merge_at = info['merge_at']
    trace, snaps = [], {}
    estab = -1; first_univ = -1; first_uo = -1; last_uo_change = -1; prev_uo = None
    first_resolved = -1; first_lost = -1
    max_ident = 0.0; max_Q = 0.0; max_AP = 0.0; max_Q_sp = 0
    estab_dec = None
    ctr_at = {}
    horizon = gens if ext != EXT_ALL else 10000
    frozen_at = -1; ext_cut = -1
    merged_gen = -1
    g = 0
    while g < horizon:
        R.advance(10)
        g = R.g
        if merge_at and g == merge_at:
            R.merge(PG.kernel_seed_pg(R.N * R.I, 1, rep) ^ 0x5DEECE66D)
            merged_gen = g
        cc = R.island_stats()
        if estab < 0 and (cc >= 0.9).any():
            estab = g
        chk = g <= 500 or g % 50 == 0 or g in SNAPS or estab == g
        if not chk: continue
        snap = g in SNAPS
        dec = PG.decompose(R, cc, closure=(snap or g % 500 == 0))
        gsp = R.spcount.sum(0)
        for tag, arr in ids.items():
            if len(arr) == 0: continue
            v = gsp[arr]
            ext_max[tag] = np.maximum(ext_max[tag], v)
            newz = (v == 0) & (ext_gen[tag] < 0)
            ext_gen[tag][newz] = g
        if len(ids['Q']): max_Q_sp = max(max_Q_sp, int(gsp[ids['Q']].max()))
        max_ident = max(max_ident, dec['ident']); max_Q = max(max_Q, dec['Q']); max_AP = max(max_AP, dec['APnet'])
        if R.I > 1:
            det, ip = island_part(R, cc)
            uo = ip['uo']
        else:
            det, ip = None, {}
            uo = dec['universal_open']
        if dec['universal'] and first_univ < 0 and R.I == 1: first_univ = g
        if uo and first_uo < 0: first_uo = g
        if prev_uo is not None and uo != prev_uo: last_uo_change = g
        prev_uo = uo
        if 'status' in dec:
            if dec['status'] == 'resolved' and first_resolved < 0 and R.I == 1: first_resolved = g
            if dec['status'] == 'lost' and first_lost < 0: first_lost = g
        if estab == g: estab_dec = dict(dec)
        if g in (50, 100, 200, 500, 2000, 10000):
            ctr_at[g] = R.ctr[:, [PV.C_ENC, PV.C_CATT, PV.C_COK, PV.C_DATT, PV.C_DOK, PV.C_AC, PV.C_ACOK]].sum(0).tolist()
        tr = dict(g=g, pcc=r4(dec['pcc']), M=r4(dec['M']), open=dec['h_open'], target=r4(dec['target']),
                  ident=r4(dec['ident']), Q=r4(dec['Q']), AP=r4(dec['APnet']), sucker=r4(dec['sucker']),
                  coop=r4(dec['coop']), cert=r4(dec['cert']), ccap=r4(dec['cert_of_capable']),
                  Mcert=r4(dec['M_of_cert']), unc=r4(dec['uncert_coop']), nt=dec['n_types'], uo=bool(uo))
        if g <= 500: tr['cls'] = [r4(x) for x in dec['cls']]
        if 'status' in dec: tr['status'] = dec['status']
        tr.update(ip)
        trace.append(tr)
        if snap:
            s = dict(dec)
            s['uo'] = bool(uo)
            s.update(ip)
            if R.I > 1:
                s['isl'] = RSR.island_record(R, cc, det)
            snaps[g] = s
        if g == gens and ext in (EXT_IF_NOT_UO, EXT_IF_UNRESOLVED):
            if ext == EXT_IF_NOT_UO and not uo: horizon = 10000
            if ext == EXT_IF_UNRESOLVED and dec.get('status') == 'unresolved': horizon = 10000
        if tmax > 0 and g > gens and time.time() - t0 > tmax:
            ext_cut = g
            break
        if g >= 50 and R.frozen():
            frozen_at = g
            for gs in SNAPS:
                if g < gs <= horizon and gs not in snaps:
                    base = snaps.get(g)
                    if base is None:
                        base = dict(dec); base.update(ip); base['uo'] = bool(uo)
                        if R.I > 1: base['isl'] = RSR.island_record(R, cc, det)
                    snaps[gs] = dict(base, g=gs, frozen_from=g)
            break
    R.final_logs()
    cc = R.island_stats()
    fin = PG.decompose(R, cc, closure=True)
    stat = None
    if R.I > 1:
        det, ip = island_part(R, cc)
        fin.update(ip); fin['uo'] = ip['uo']
        fin['isl'] = RSR.island_record(R, cc, det)
        stat = RSR.static_check_run(R, cc, det)
    else:
        fin['uo'] = fin['universal_open']
    exts = {tag: dict(names=[LS['names'][int(s)] for s in ids[tag]], max=ext_max[tag].tolist(),
                      extinct=ext_gen[tag].tolist()) for tag in ids if tag != 'BR'}
    br = ids['BR']
    exts['BR_summary'] = dict(n_seeded=int(len(br)), n_extinct=int((ext_gen['BR'] >= 0).sum()),
                              extinct_by_200=int(((ext_gen['BR'] >= 0) & (ext_gen['BR'] <= 200)).sum()))
    return dict(cell=cell, rep=rep, T=info['T'], N=info['N'], I=info['I'], prior=info['prior'], r=info['r'],
                rarm=info['rarm'], mN=info['mN'], merge_at=merge_at, merged_gen=merged_gen,
                gens=gens, ext=ext, horizon=horizon, last_gen=R.g, frozen_at=frozen_at, ext_cut=ext_cut,
                establish_gen=estab, first_univ=first_univ, first_uo=first_uo, last_uo_change=last_uo_change,
                first_resolved=first_resolved, first_lost=first_lost, max_ident=max_ident, max_Q=max_Q,
                max_AP=max_AP, max_Q_spelling=max_Q_sp, estab_dec=estab_dec, meta=meta, ext_log=exts,
                trace=trace, snaps={str(k): v for k, v in snaps.items()}, final=fin, static=stat,
                ctr_at={str(k): v for k, v in ctr_at.items()}, ctr=R.ctr.tolist(), enc_exp=R.enc_exp.tolist(),
                steps_rule=R.steps_rule.tolist(), n_types=int(R.ntv[0]), time_s=time.time() - t0)


def run_pool(fn, jobs, path, workers, tag):
    rows = json.load(gzip.open(path)) if os.path.exists(path) else []
    done = {(r['cell'], r['rep']) for r in rows}
    jobs = [j for j in jobs if (j[0], j[1]) not in done]
    log('%s jobs %d (pid %d), already done %d' % (tag, len(jobs), os.getpid(), len(done)))
    if not jobs: return rows
    t0 = time.time()
    with Pool(min(3, workers), maxtasksperchild=4) as pool:
        for r in pool.imap_unordered(fn, jobs):
            rows.append(r)
            tmp = path + '.tmp'
            with gzip.open(tmp, 'wt') as f: json.dump(rows, f)
            os.replace(tmp, path)
            f = r['final']
            log('%s rep %d: estab %d pcc %.3f M %.3f open %s uo %s target %.3f ident %.4f maxQ %.4f AP %.3f status %s last %d (%.0fs, total %.0fs)' % (
                r['cell'], r['rep'], r['establish_gen'], f['pcc'], f['M'], f['h_open'], f['uo'], f['target'],
                f['ident'], r['max_Q'], r['max_AP'], f.get('status'), r['last_gen'], r['time_s'], time.time() - t0))
    return rows


def cmd_lottery(a):
    cells = []
    for c in a.cells:
        cells += PG.ALL[c] if c in PG.ALL else [c]
    jobs = []
    for c in cells:
        for rep in range(a.rep0, a.rep0 + a.runs):
            jobs.append((c, rep, a.gens, a.ext, a.tmax))
    # largest expected cost first: Pangaea-like cells, then large N
    jobs.sort(key=lambda j: (-(PG.PG[j[0]]['N'] if not PG.PG[j[0]]['merge_at'] else 12800), j[1]))
    run_pool(lottery_job, jobs, os.path.join(OUT, 'lottery_%s.json.gz' % a.out), a.workers, 'lottery')


# ------------------------------------------------------------------------------------------------ validation
class LegacyRun(PG.PGRun):
    """The stored scaling run's conventions (r = N/2, provenance's seed) on the new kernel."""

    def __init__(self, cell, rep):
        super().__init__(cell, rep, legacy=True)


def _validate_job(job):
    RS.RSRun = LegacyRun            # the scaling run's lottery job, with the kernel swapped (per worker process)
    cell, rep = job
    return RSR.lottery_job((cell, rep, 2000, 1e-9, True))


def cmd_validate(a):
    stored = []
    for f in ('lottery_main', 'lottery_srest'):
        stored += json.load(gzip.open(os.path.join(ROOT, 'runs', 'realizable_scaling', f + '.json.gz')))
    cells = ['rs_Snon_200_64_cal', 'rs_Snon_100_64_cal', 'rs_prop_200_64_cal', 'rs_Snon_50_64_m1']
    jobs = [(c, rep) for c in cells for rep in range(a.reps)]
    t0 = time.time()
    with Pool(min(3, a.workers)) as pool:
        rows = pool.map(_validate_job, jobs)
    out = []
    for r in rows:
        s = [x for x in stored if x['cell'] == r['cell'] and x['rep'] == r['rep']][0]
        ta = {t[0]: t for t in r['trace'] if t[0] <= 2000}
        tb = {t[0]: t for t in s['trace'] if t[0] <= 2000}
        common = sorted(set(ta) & set(tb))
        bad = [g for g in common if any(abs(x - y) > 1e-9 for x, y in zip(ta[g], tb[g]))]
        sb = []
        for k in ('universal_open', 'held', 'identity_islands', 'open_islands', 'outcome', 'pcc'):
            if r['snaps']['2000'][k] != s['snaps']['2000'][k]: sb.append(k)
        out.append(dict(cell=r['cell'], rep=r['rep'], n_common=len(common), n_bad=len(bad), first_bad=bad[:3],
                        snap_bad=sb, estab=(r['establish_gen'], s['establish_gen'])))
    nbad = sum(1 for o in out if o['n_bad'] or o['snap_bad'] or o['estab'][0] != o['estab'][1])
    rep = dict(n_rows=len(out), n_bad=nbad, trace_points=sum(o['n_common'] for o in out), rows=out,
               time_s=time.time() - t0)
    json.dump(rep, open(os.path.join(ROOT, 'runs', 'pangaea-validate.json'), 'w'), indent=1)
    log(json.dumps({k: v for k, v in rep.items() if k != 'rows'}))


def cmd_kernelcheck(a):
    """Notes §1.7 items 2, 3, 5."""
    LS = PR.lot_static('ext')
    out = {}
    # 2. draw keys: encounter draws of q >= 100 against every draw of the same and next event under the base seed
    seed = PG.kernel_seed_pg(800, 16, 0)
    ev = 12345
    base = set()
    for e in (ev, ev + 1):
        for j in range(512):
            base.add(PV.ru(seed, e, j))
    hi = set()
    for q in range(100, 400):
        sq = PK.block_seed(seed, q // 100)
        for o in range(5):
            hi.add(PV.ru(sq, ev, 8 + 5 * (q % 100) + o))
    old = [PV.ru(seed, ev, 8 + 5 * q + o) for q in range(100, 200) for o in range(3)]
    out['draws'] = dict(n_high=len(hi), collisions_with_base=len(hi & base),
                        legacy_overlap_with_next_event=sum(1 for x in old if x in set(PV.ru(seed, ev + 1, j) for j in range(512))))
    # 3. founders
    fc = {}
    for T in PG.TOTALS:
        for rep in (0, 1):
            hs = set(); qs = set()
            for (N, I) in PG.GEOMS[T]:
                R = PG.PGRun(PG.cell_name('L', N, I), rep)
                m = founder_meta(R)
                hs.add(m['founder_hash']); qs.add(m['seeded_Q'])
                if (N, I) != PG.GEOMS[T][-1]:
                    # nesting: each island of this geometry is a union of islands of the previous (smaller N) one
                    pass
            fc['%d_%d' % (T, rep)] = dict(hashes=len(hs), seeded_Q=sorted(qs))
            perm = PG.permutation(T, rep)
            lst = PG.base_list(T, rep, LS)
            nest = True
            for (N1, I1), (N2, I2) in zip(PG.GEOMS[T][:-1], PG.GEOMS[T][1:]):
                a1 = PG.partition(lst, N1, I1, perm); a2 = PG.partition(lst, N2, I2, perm)
                k = N2 // N1
                nest &= all(np.array_equal(np.sort(a2[i]), np.sort(a1[i * k:(i + 1) * k].ravel())) for i in range(I2))
            fc['%d_%d' % (T, rep)]['nested'] = bool(nest)
            pl = PG.proportional(lst, T, rep, LS)
            ch = lst != pl
            fc['%d_%d' % (T, rep)]['prop_changed_only_Q'] = bool(np.isin(lst[ch], LS['Q']).all() and
                                                                  not np.isin(pl, LS['Q']).any())
    for c in ('pg_Cdon_12800_1_r100', 'pg_Cdon13_12800_1_r100', 'pg_Cdon6_6400_1_r100'):
        R = PG.PGRun(c, 0)
        fc[c + '_donors'] = int((R.rule0 == PV.R_H).sum())
    out['founders'] = fc
    # 5. merge = fresh initialization from the merged slots
    R = PG.PGRun(PG.cell_name('L', 100, 128, merge_at=200), 0)
    R.advance(30)
    R.merge(777)
    paysum0 = R.paysum.copy(); counts0 = R.counts.copy(); uns0 = R.uns.copy()
    from numba.typed import Dict
    slots = R.slots.copy()
    cnt = np.zeros_like(counts0); np.add.at(cnt[0], slots[0], 1)
    ps = np.zeros_like(paysum0)
    PV.init_paysum(cnt, ps, R.pres, R.npres, R.tunit, R.tsp, R.A, R.selfa)
    out['merge'] = dict(counts_equal=bool(np.array_equal(cnt, counts0)), paysum_equal=bool(np.allclose(ps, paysum0)),
                        uns=int(uns0[0]), npres=int(R.npres[0]), N=R.N, I=R.I)
    R.advance(10)
    out['merge']['advance_ok'] = True
    json.dump(out, open(os.path.join(ROOT, 'runs', 'pangaea-kernelcheck.json'), 'w'), indent=1)
    log(json.dumps(out, indent=1))


def cmd_determ(a):
    LS = PR.lot_static('ext')
    res = {}
    for prior in ('L', 'prop'):
        t0 = time.time()
        d = PG.determ(LS, prior=prior, gens=a.gens, dt=a.dt)
        d['time_s'] = time.time() - t0
        res[prior] = d
        tr = d['traj']
        for x in tr:
            if x['g'] in (0, 10, 20, 50, 100, 150, 200, 300, 500, 1000, 2000):
                log(prior, int(x['g']), 'pcc %.3f target %.3f open %.3f AP %.3f ident %.5f' % (
                    x['pcc'], x['target'], x['open'], x['APnet'], x['ident']),
                    ' '.join('%s %.3f' % (n, v) for n, v in zip(PG.CLASSES, x['cls'])))
        log(prior, 'top', d['final_top'][:5])
    json.dump(res, open(os.path.join(ROOT, 'runs', 'pangaea-determ.json'), 'w'), indent=1)


def cmd_smoke(a):
    out = {}
    path = os.path.join(OUT, 'smoke.json')
    old = json.load(open(path)) if os.path.exists(path) else {}
    for c in a.cells:
        t0 = time.time()
        R = PG.PGRun(c, 990)
        tt = []
        for k in range(a.gens // 10):
            t1 = time.time(); R.advance(10); tt.append(round(time.time() - t1, 2))
        cc = R.island_stats()
        t2 = time.time()
        dec = PG.decompose(R, cc, closure=True)
        out[c] = dict(gens=a.gens, time_s=time.time() - t0, per10=tt, n_types=int(R.ntv[0]),
                      npres=int(R.npres.max()), decompose_s=time.time() - t2, M=dec['M'], pcc=dec['pcc'])
        log(c, '%.1fs' % (time.time() - t0), 'npres', int(R.npres.max()), ' '.join('%.1f' % x for x in tt[-10:]))
    old.update(out)
    json.dump(old, open(path, 'w'), indent=1)


def cmd_cachecheck(a):
    """The copier no-change cache is exact: C-donor runs with and without it agree state for state."""
    out = []
    for cell, gens in (('pg_Cdon_6400_1_r100', a.gens), ('pg_Cdon6_6400_1_r100', a.gens)):
        for rep in (990, 991):
            A_ = PG.PGRun(cell, rep); B_ = PG.PGRun(cell, rep)
            B_.use_nochg = False
            assert A_.use_nochg
            t0 = time.time(); A_.advance(gens); ta = time.time() - t0
            t0 = time.time(); B_.advance(gens); tb = time.time() - t0
            same = bool(np.array_equal(A_.slots, B_.slots) and np.array_equal(A_.counts, B_.counts) and
                        np.array_equal(A_.ctr[:, PV.C_BIRTH], B_.ctr[:, PV.C_BIRTH]) and
                        np.array_equal(A_.ctr[:, PV.C_ACOK], B_.ctr[:, PV.C_ACOK]) and int(A_.ntv[0]) == int(B_.ntv[0]))
            out.append(dict(cell=cell, rep=rep, gens=gens, identical=same, t_cache=ta, t_plain=tb,
                            skipped_sides=int(A_.nskip[0]), cache_size=len(A_.nochg)))
            log(out[-1])
    json.dump(out, open(os.path.join(ROOT, 'runs', 'pangaea-cachecheck.json'), 'w'), indent=1)
    if not all(o['identical'] for o in out):
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('lottery'); s.add_argument('--cells', nargs='+'); s.add_argument('--runs', type=int, default=20)
    s.add_argument('--rep0', type=int, default=0); s.add_argument('--gens', type=int, default=2000)
    s.add_argument('--ext', type=int, default=EXT_ALL); s.add_argument('--tmax', type=float, default=0)
    s.add_argument('--workers', type=int, default=3); s.add_argument('--out', default='main')
    s = sub.add_parser('validate'); s.add_argument('--reps', type=int, default=3); s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('kernelcheck')
    s = sub.add_parser('determ'); s.add_argument('--gens', type=int, default=2000); s.add_argument('--dt', type=float, default=0.1)
    s = sub.add_parser('smoke'); s.add_argument('--cells', nargs='+'); s.add_argument('--gens', type=int, default=200)
    s = sub.add_parser('cachecheck'); s.add_argument('--gens', type=int, default=80)
    a = ap.parse_args()
    {'lottery': cmd_lottery, 'validate': cmd_validate, 'kernelcheck': cmd_kernelcheck, 'determ': cmd_determ,
     'smoke': cmd_smoke, 'cachecheck': cmd_cachecheck}[a.cmd](a)


if __name__ == '__main__':
    main()
