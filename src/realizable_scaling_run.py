"""Driver for the realizable lottery along paths in (N, I, mN) (notes/realizable-scaling.md).

    python3 src/realizable_scaling_run.py calib [--runs 20]           # T_nuc at m = 0 (notes §1.2)
    python3 src/realizable_scaling_run.py validate                      # draw-for-draw against stored provenance rows
    python3 src/realizable_scaling_run.py smoke --cells ... --gens 100  # cost probes (discarded)
    python3 src/realizable_scaling_run.py lottery --cells ... --runs 20 --out NAME
Rows go to runs/realizable_scaling/*.json (summaries; nothing large).
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'realizable_scaling')
os.makedirs(OUT, exist_ok=True)
SNAPS0 = (500, 1000, 2000, 5000, 10000)


def log(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------------------------------------ per-island detail
_EXTRA = {}


def extra_static(LS):
    """Arrays the classifier needs beyond provenance's lot_static: the S-nonself prior closure."""
    if 'reach_nonself' not in _EXTRA:
        sets = np.load(os.path.join(PR.OUT, 'sets.npz'))
        _EXTRA['reach_nonself'] = np.asarray(sets['reach_nonself'])
    return _EXTRA


def holders_detail(R, cc):
    """Per island: holder type, held, and the classifier's verdict (notes §1.6)."""
    LS = R.LS
    I = R.I
    maj = R.maj_k.copy()
    H = sorted(set(int(k) for k in maj.tolist()))
    hix = {k: n for n, k in enumerate(H)}
    nh = len(H)
    mutual = np.zeros((nh, nh), bool)
    for a in range(nh):
        for b in range(a, nh):
            v = PV.cc_pair(H[a], H[b], R.tunit, R.tsp, R.A, R.selfa) > 0.5
            mutual[a, b] = mutual[b, a] = v
    units = R.tunit[H]
    openv = np.asarray(LS['openu'])[units]
    ident = np.asarray(LS['ident'])[units]
    selfc = np.array([mutual[n, n] for n in range(nh)])
    hol = [hix[int(k)] for k in maj.tolist()]
    held = np.array([selfc[hol[i]] and cc[i] >= 0.5 for i in range(I)])
    cl = RS.classify(hol, held, mutual, openv, ident)
    return dict(H=H, hol=hol, held=held, mutual=mutual, openv=openv, ident=ident, selfc=selfc, cl=cl)


def static_check_run(R, cc, det):
    """The static absorbing check on the final support (notes §1.6)."""
    LS, st = R.LS, R.LS['st']
    I, N = R.I, R.N
    cl = det['cl']
    if cl['universal_open']:
        return dict(label='universal', per=[], n_living_types=0)
    nt = int(R.ntv[0])
    cnt = R.counts[:, :nt]
    glob = cnt.sum(0)
    living = np.nonzero(glob)[0]
    H = det['H']
    main = [H[n] for n in cl['main']]
    A, selfa = R.A, R.selfa
    openu = np.asarray(LS['openu'])
    cp = lambda x, y: PV.cc_pair(int(x), int(y), R.tunit, R.tsp, A, selfa) > 0.5
    fail_isl = [i for i, f in enumerate(cl['fail']) if f != '']
    X = {i: H[det['hol'][i]] for i in fail_isl}
    Z_ok, Z_mx, Z_rho, Z_sh = [], [], [], []
    Zs = []
    for z in living.tolist():
        if not cp(z, z) or not openu[R.tunit[z]]: continue
        if not all(cp(z, h) for h in main): continue
        Zs.append(z)
    for z in Zs:
        mx, rh, sh = [], [], []
        for i in range(I):
            if i not in X:
                mx.append(False); rh.append(0.0); sh.append(0.0); continue
            x = X[i]
            mx.append(cp(z, x))
            a = PV.pay(z, z, R.tunit, R.tsp, A, selfa); b = PV.pay(z, x, R.tunit, R.tsp, A, selfa)
            c = PV.pay(x, z, R.tunit, R.tsp, A, selfa); d = PV.pay(x, x, R.tunit, R.tsp, A, selfa)
            rh.append(RS.rho_fix(N, a, b, c, d))
            sh.append(float(glob[z] - cnt[i, z]) / (N * (I - 1)) if I > 1 else 0.0)
        Z_ok.append(True); Z_mx.append(mx); Z_rho.append(rh); Z_sh.append(sh)
    # reachable (gene acquisition from the living units against living partners) and dead prior bridges, unit-level
    lu = np.array(sorted(set(R.tunit[living].tolist())), np.int64)
    reach = np.zeros(len(openu), np.bool_)
    PV.nonself_closure(lu, lu, np.asarray(st['utau']), np.asarray(st['KIND']), np.asarray(st['NAT']),
                       np.asarray(st['CHD']), np.asarray(st['UVt']), np.asarray(st['BLC']), np.asarray(st['BLD']),
                       LS['PRODC'], LS['PD'], np.asarray(st['APP']), reach)
    reach[lu] = False
    prior = extra_static(LS)['reach_nonself'].copy()
    prior[lu] = False
    main_u = [int(R.tunit[h]) for h in main]
    Aa = np.asarray(A); sa = np.asarray(selfa)

    def unit_bridges(cand, xu):
        c = np.nonzero(cand)[0]
        if len(c) == 0: return 0
        ok = (sa[c] == 1) & openu[c]
        for hu in main_u + [xu]:
            ok &= (Aa[c, hu] == 1) & (Aa[hu, c] == 1)
        return int(ok.sum())
    rb, dead = [], []
    for i in range(I):
        if i in X:
            xu = int(R.tunit[X[i]])
            rb.append(unit_bridges(reach, xu) > 0); dead.append(unit_bridges(prior, xu))
        else:
            rb.append(False); dead.append(0)
    label, per = RS.static_check(cl['fail'], det['hol'], N, R.mN, Z_ok, Z_mx, Z_rho, Z_sh, rb)
    for p in per:
        p['dead_prior_bridges'] = dead[p['island']]
        p['holder_spelling'] = LS['names'][int(R.tsp[X[p['island']]])]
        p['t_res'] = None if p['t_res'] == float('inf') else p['t_res']
    return dict(label=label, per=per, n_living_types=int(len(living)), n_target_compatible=len(Zs),
                n_reachable_units=int(reach.sum()))


# ------------------------------------------------------------------------------------------------ one run
def lottery_job(job):
    cell, rep, gens = job[:3]
    tmax = job[3] if len(job) > 3 else 0
    noext = bool(job[4]) if len(job) > 4 else False      # drop-order step 1 (notes §2): no extension off the main cells
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    info = RS.CELL_INFO[cell]
    R = RS.RSRun(cell, rep)
    LS = R.LS
    I, N = R.I, R.N
    Tm = info['T_ext'] if info['main'] else 10000
    snaps_at = sorted(set(SNAPS0) | {Tm})
    every = 10
    trace = []
    snaps, isl = {}, {}
    estab = -1
    e3_gen, e3_out = -1, None
    ever90 = np.zeros(I, bool)
    ident_ever = np.zeros(I, bool)
    ident_first = -np.ones(I, np.int64)
    uo_first = -1
    uo_last_change = -1
    uo_prev = False
    horizon = Tm if info['main'] else gens
    frozen_at = -1
    ext_cut = -1
    nmismatch = 0
    sp0 = R.sp0
    q_isl = np.isin(sp0, LS['Q']).sum(1)
    identu = np.asarray(LS['ident'])
    g = 0
    while g < horizon:
        R.advance(every)
        g = R.g
        cc = R.island_stats()
        if estab < 0 and (cc >= 0.9).any(): estab = g
        ever90 |= cc >= 0.9
        hu = R.tunit[R.maj_k]
        selfc = np.array([PV.cc_pair(int(k), int(k), R.tunit, R.tsp, R.A, R.selfa) > 0.5 for k in R.maj_k])
        idn = identu[hu] & selfc & (cc >= 0.5)
        newi = idn & ~ident_ever
        ident_first[newi] = g
        ident_ever |= idn
        if e3_gen < 0 and (g <= gens or g in snaps_at or g % 500 == 0):
            s3 = R.e3()
            if s3 is not None and (s3 >= 0).all():
                e3_gen = g; e3_out = 'success' if (s3 == 1).all() else 'fail'
        if g in snaps_at or estab == g or g % 50 == 0:
            sn = R.snapshot(cc)
            det = holders_detail(R, cc)
            uo = det['cl']['universal_open']
            if uo != sn['universal_open']: nmismatch += 1
            if uo and uo_first < 0: uo_first = g
            if uo != uo_prev: uo_last_change = g
            uo_prev = uo
            trace.append((g, sn['pcc'], sn['islands90'], sn['held'], sn['identity_islands'], sn['open_islands'],
                          sn['spo_islands'], sn['n_types'], int(uo), int((cc >= 0.95).sum())))
            if g in snaps_at:
                snaps[g] = slim(sn)
                isl[g] = island_record(R, cc, det)
        if g == gens and not info['main'] and not noext:
            sn = snaps.get(gens)
            if sn is not None and (not sn['universal_open'] or e3_out is None) and e3_out != 'fail':
                horizon = 10000
        if tmax > 0 and g > gens and time.time() - t0 > tmax:
            ext_cut = g
            break
        if g >= 50 and R.frozen():
            frozen_at = g
            sn = slim(R.snapshot(R.island_stats()))
            cc = R.island_stats()
            det = holders_detail(R, cc)
            rec = island_record(R, cc, det)
            for gs in snaps_at:
                if g < gs <= horizon and gs not in snaps:
                    snaps[gs] = dict(sn, g=gs, frozen_from=g); isl[gs] = rec
            break
    R.final_logs()
    cc = R.island_stats()
    fin = slim(R.snapshot(cc))
    det = holders_detail(R, cc)
    if det['cl']['universal_open'] != fin['universal_open']: nmismatch += 1
    fin_isl = island_record(R, cc, det)
    stat = static_check_run(R, cc, det)
    persist = float((ever90 & (cc >= 0.9)).sum() / ever90.sum()) if ever90.any() else None
    # clustering (amendment 4)
    ident_fin = np.array([f == 'identity' for f in det['cl']['fail']]) | \
        np.array([bool(det['ident'][det['hol'][i]]) and det['held'][i] for i in range(I)])
    clus = dict(q_isl=q_isl.tolist(), seeded=int(q_isl.sum()), occupied=int((q_isl > 0).sum()),
                multi=int((q_isl >= 2).sum()), ident_ever=ident_ever.astype(int).tolist(),
                ident_first=ident_first.tolist(), ident_final=ident_fin.astype(int).tolist(),
                ident_final_seeded_sp=int(sum(1 for i in range(I) if ident_fin[i] and int(R.tsp[R.maj_k[i]]) in set(LS['Q'].tolist()))))
    return dict(cell=cell, rep=rep, N=N, I=I, mN=R.mN, rule=info['rule'], arm=info['arm'], main=info['main'], noext=noext,
                T_ext=Tm, gens=gens, horizon=horizon, last_gen=R.g, frozen_at=frozen_at, ext_cut=ext_cut,
                establish_gen=estab, E3_gen=e3_gen, E3=e3_out if e3_out else 'censored', ever90=int(ever90.sum()),
                persistence=persist, trace=trace, snaps={str(k): v for k, v in snaps.items()},
                isl={str(k): v for k, v in isl.items()}, final=fin, final_isl=fin_isl, static=stat,
                uo_first=uo_first, uo_last_change=uo_last_change, classifier_mismatch=nmismatch,
                clus=clus, seeded_Q=int(q_isl.sum()), ctr=R.ctr.tolist(), steps_rule=R.steps_rule.tolist(),
                enc_exp=R.enc_exp.tolist(), enc_futile=R.enc_futile.tolist(), n_types=int(R.ntv[0]),
                time_s=time.time() - t0)


KEEP = ('g', 'pcc', 'islands90', 'held', 'outcome', 'universal_open', 'open_islands', 'identity_islands',
        'spo_islands', 'cross_pcc', 'n_quotes', 'n_spellings', 'n_types', 'holders', 'rule_all', 'rule_coop', 'inst',
        'group_ind')


def slim(sn):
    return {k: sn[k] for k in KEEP if k in sn}


def island_record(R, cc, det):
    LS = R.LS
    cl = det['cl']
    return dict(cc=[round(float(x), 4) for x in cc], held=det['held'].astype(int).tolist(), fail=cl['fail'],
                holder_sp=[int(R.tsp[k]) for k in R.maj_k], cause=cl['cause'], universal_open=cl['universal_open'],
                eff=int((cc >= 0.95).sum()))


# ------------------------------------------------------------------------------------------------ calibration
def calib_job(job):
    cell, rep, gens = job
    t0 = time.time()
    R = RS.RSRun(cell, rep)
    I = R.I
    t_est = -np.ones(I, np.int64)
    first = -1
    g = 0
    while g < gens:
        R.advance(5)
        g = R.g
        cc = R.island_stats()
        new = (cc >= 0.9) & (t_est < 0)
        t_est[new] = g
        if first < 0 and new.any(): first = g
    return dict(cell=cell, rep=rep, N=R.N, I=I, rule=RS.CELL_INFO[cell]['rule'], t_est=t_est.tolist(), first=first,
                n_nuc=int((t_est >= 0).sum()), time_s=time.time() - t0)


def run_pool(fn, jobs, path, workers, tag):
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['cell'], r['rep']) for r in rows}
    jobs = [j for j in jobs if (j[0], j[1]) not in done]
    log('%s jobs %d (pid %d), already done %d' % (tag, len(jobs), os.getpid(), len(done)))
    t0 = time.time()
    if not jobs: return rows
    with Pool(min(3, workers)) as pool:
        for r in pool.imap_unordered(fn, jobs):
            rows.append(r)
            tmp = path + '.tmp'
            json.dump(rows, open(tmp, 'w')); os.replace(tmp, path)
            if fn is lottery_job:
                f = r['final']
                log('%s rep %d: estab %d E3 %s pcc %.3f held %d uo %s cause %s static %s ident %d seededQ %d last %d (%.0fs, total %.0fs)' % (
                    r['cell'], r['rep'], r['establish_gen'], r['E3'], f['pcc'], f['held'], f['universal_open'],
                    r['final_isl']['cause'], r['static']['label'], f['identity_islands'], r['seeded_Q'], r['last_gen'],
                    r['time_s'], time.time() - t0))
            else:
                log('%s rep %d: nuc %d first %d (%.0fs, total %.0fs)' % (r['cell'], r['rep'], r['n_nuc'], r['first'],
                                                                      r['time_s'], time.time() - t0))
    return rows


def cmd_calib(a):
    cells = [c for c in RS.CALIB if (a.cells is None or c in a.cells)]
    jobs = [(c, rep, a.gens) for rep in range(500, 500 + a.runs) for c in cells]
    jobs.sort(key=lambda j: -RS.CELL_INFO[j[0]]['N'])
    run_pool(calib_job, jobs, os.path.join(OUT, 'calib_rows.json'), a.workers, 'calib')


def cmd_lottery(a):
    cells = []
    for c in a.cells:
        cells += RS.ALL[c] if c in RS.ALL else [c]
    jobs = []
    for c in cells:
        N, I = RS.CELL_INFO[c]['N'], RS.CELL_INFO[c]['I']
        nr = a.runs if a.runs else (40 if (N, I) == (100, 64) else 20)
        jobs += [(c, rep, a.gens, a.tmax, a.noext) for rep in range(a.rep0, a.rep0 + nr)]
    # largest first (better packing)
    jobs.sort(key=lambda j: -(RS.CELL_INFO[j[0]]['N'] ** 2 * RS.CELL_INFO[j[0]]['I'] * (5 if 'Cd' in j[0] else 1)))
    run_pool(lottery_job, jobs, os.path.join(OUT, 'lottery_%s.json' % a.out), a.workers, 'lottery')


def cmd_smoke(a):
    out = {}
    for c in a.cells:
        t0 = time.time()
        R = RS.RSRun(c, 990)
        tt = []
        for k in range(a.gens // 10):
            t1 = time.time(); R.advance(10); tt.append(time.time() - t1)
        out[c] = dict(gens=a.gens, time_s=time.time() - t0, per10=tt, n_types=int(R.ntv[0]))
        log(c, '%.1fs' % (time.time() - t0), ' '.join('%.1f' % x for x in tt))
    path = os.path.join(OUT, 'smoke.json')
    old = json.load(open(path)) if os.path.exists(path) else {}
    old.update(out)
    json.dump(old, open(path, 'w'), indent=1)


def stored_rows():
    rows = []
    for f in ('lottery_main', 'lottery_size', 'lottery_size2'):
        p = os.path.join(PR.OUT, f + '.json.gz')
        rows += json.load(gzip.open(p))
    return rows


STORED_OF = {('Snon', 100, 64, 'cal'): 'Snon', ('abl', 100, 64, 'cal'): 'ablation', ('Cdon', 100, 64, 'cal'): 'Cdonor',
             ('Snon', 200, 64, 'm1'): 'Snon_N200', ('abl', 200, 64, 'm1'): 'ablation_N200',
             ('Cdon', 200, 64, 'm1'): 'Cdonor_N200', ('Snon', 100, 128, 'cal'): 'Snon_I128',
             ('abl', 100, 128, 'cal'): 'ablation_I128', ('Cdon', 100, 128, 'cal'): 'Cdonor_I128'}


def compare_stored(r, s):
    """Trace entries at common generations (g, pcc, islands90, held, identity, open, spo, n_types) and the common
    snapshots' key fields."""
    ta = {t[0]: t[:8] for t in r['trace']}
    tb = {t[0]: tuple(t) for t in s['trace']}
    common = sorted(set(ta) & set(tb))
    bad = [g for g in common if any(abs(x - y) > 1e-9 for x, y in zip(ta[g], tb[g]))]
    sb = []
    for g in ('2000', '10000'):
        if g in r['snaps'] and g in s['snaps']:
            for k in ('universal_open', 'held', 'identity_islands', 'open_islands', 'outcome'):
                if r['snaps'][g][k] != s['snaps'][g][k]: sb.append((g, k))
            if abs(r['snaps'][g]['pcc'] - s['snaps'][g]['pcc']) > 1e-9: sb.append((g, 'pcc'))
    eb = (r['establish_gen'] != s['establish_gen'])
    return dict(n_common=len(common), last_common=common[-1] if common else None, trace_bad=bad[:5],
                n_trace_bad=len(bad), snap_bad=sb, estab_bad=bool(eb))


def cmd_validate(a):
    """Draw-for-draw reproduction of stored provenance rows (notes §1.8 item 2)."""
    stored = stored_rows()
    jobs = []
    for (rule, N, I, arm), sc in STORED_OF.items():
        if rule not in a.rules: continue
        if (N, I) not in [tuple(x) for x in a.geoms]: continue
        name = RS.cell_name(rule, N, I, arm)
        for rep in range(a.reps):
            jobs.append((name, rep, 2000, 0))
    path = os.path.join(OUT, 'validate_rows.json')
    rows = run_pool(lottery_job, jobs, path, a.workers, 'validate')
    rev = {RS.cell_name(*k): v for k, v in STORED_OF.items()}
    out = []
    for r in rows:
        sc = rev[r['cell']]
        s = [x for x in stored if x['cell'] == sc and x['rep'] == r['rep']]
        if not s: continue
        c = compare_stored(r, s[0])
        c.update(cell=r['cell'], rep=r['rep'], classifier_mismatch=r['classifier_mismatch'],
                 stored_last=s[0]['last_gen'], new_last=r['last_gen'])
        out.append(c)
    n_bad = sum(1 for c in out if c['n_trace_bad'] or c['snap_bad'] or c['estab_bad'])
    rep = dict(n_compared=len(out), n_bad=n_bad, n_classifier_mismatch=sum(c['classifier_mismatch'] for c in out),
               trace_points=sum(c['n_common'] for c in out), rows=out)
    json.dump(rep, open(os.path.join(ROOT, 'runs', 'realizable-scaling-validate.json'), 'w'), indent=1)
    log(json.dumps({k: v for k, v in rep.items() if k != 'rows'}))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('calib'); s.add_argument('--runs', type=int, default=20); s.add_argument('--gens', type=int, default=400)
    s.add_argument('--workers', type=int, default=3); s.add_argument('--cells', nargs='*', default=None)
    s = sub.add_parser('lottery'); s.add_argument('--cells', nargs='+'); s.add_argument('--runs', type=int, default=0)
    s.add_argument('--rep0', type=int, default=0); s.add_argument('--gens', type=int, default=2000)
    s.add_argument('--tmax', type=float, default=0); s.add_argument('--workers', type=int, default=3)
    s.add_argument('--out', default='main'); s.add_argument('--noext', action='store_true')
    s = sub.add_parser('smoke'); s.add_argument('--cells', nargs='+'); s.add_argument('--gens', type=int, default=100)
    s = sub.add_parser('validate'); s.add_argument('--workers', type=int, default=3); s.add_argument('--reps', type=int, default=6)
    s.add_argument('--rules', nargs='+', default=['Snon', 'abl', 'Cdon'])
    s.add_argument('--geoms', nargs='+', type=lambda z: tuple(int(x) for x in z.split(',')), default=[(100, 64), (200, 64)])
    a = ap.parse_args()
    {'calib': cmd_calib, 'lottery': cmd_lottery, 'smoke': cmd_smoke, 'validate': cmd_validate}[a.cmd](a)


if __name__ == '__main__':
    main()
