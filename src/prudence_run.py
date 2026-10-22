"""Driver for the prudence run (notes/prudence.md, predictions/2026-10-21-prudence-world-k.md).

    python3 src/prudence_run.py statics                      # sets, fixed-list premium, schedule checks (runs/prudence-static.json)
    python3 src/prudence_run.py validate [--reps 3]          # A0 reproduces the stored fission-fusion cells (both worlds)
    python3 src/prudence_run.py probe --jobs L:A156:990:3000 K:A0:990:500   # cost / sanity probes on a discarded replicate
    python3 src/prudence_run.py cells [--arms ...] [--worlds ...] [--reps 20] [--rep0 0] [--workers 3] --out NAME
Rows go to runs/prudence/*.json.gz (not committed if large); summaries to runs/prudence.json.
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
import pangaea as PG
import world_k as WK
import prudence as P

OUT = P.OUT
os.makedirs(OUT, exist_ok=True)
ROOT = P.ROOT
TRACE_KEYS = ('g', 'nt', 'pcc', 'coopsh', 'imm', 'T', 'prud', 'ung', 'pb', 'off', 'suck_c', 'suck_u', 'ident', 'AP', 'Q',
              'i_T', 'i_prud', 'i_ung', 'i_pb', 'i_off', 'i_suck_c', 'i_suck_u', 'edge_enc', 'edge_enc_c', 'sel_adv',
              'top_lin', 'top_lin_sh', 'plur_s', 'plur_sh')
RES_GROUPS = ('off', 'suck_c', 'suck_u', 'ident', 'Q', 'prud', 'T')


def log(*a):
    print(*a, flush=True)


def js(x):
    if isinstance(x, dict): return {str(k): js(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [js(v) for v in x]
    if isinstance(x, np.integer): return int(x)
    if isinstance(x, np.floating): return None if not np.isfinite(x) else float(x)
    if isinstance(x, float): return None if not np.isfinite(x) else x
    if isinstance(x, np.bool_): return bool(x)
    if isinstance(x, np.ndarray): return js(x.tolist())
    return x


def r5(x):
    return None if x is None else round(float(x), 5)


def gstep(g):
    return 10 if g < 800 else 20


def stored_ff_rows():
    import gzip as gz
    rows = json.load(gz.open(os.path.join(ROOT, 'runs/world_k/cells_C.json.gz')))
    return {(r['world'], r['rep']): r for r in rows if r['cell'] == P.FF_CELL}


# ------------------------------------------------------------------------------------------------ one run
def pru_job(job):
    w, arm, rep = job[:3]
    gmax = int(job[3]) if len(job) > 3 and job[3] else P.G_END
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    LS = WK.use_world(w)
    S = P.sets(LS)
    R = P.PruRun(rep, arm)
    A_exp, depl = P.ARMS[arm]
    pre = []
    # phase 1: the islands, exactly the stored loop's decompositions every 10 generations
    while R.g < P.MERGE:
        R.advance(10)
        cc = R.island_stats()
        dec = PG.decompose(R, cc, closure=False)
        pre.append(dict(g=int(R.g), pcc=r5(dec['pcc']), M=r5(dec['M']), target=r5(dec['target']), nt=int(dec['n_types'])))
    R.do_merge()
    comp = dict(light=P.light_stats(R, S, LS), heavy=P.heavy_stats(R, S, LS, R.g))
    comp['light'].pop('plur', None)
    trace = []
    snaps = {}
    res_tail = {k: 0.0 for k in RES_GROUPS}
    res_chase = {k: 0.0 for k in RES_GROUPS}
    colon = {}
    prev = None
    frozen_at = -1
    first = P.light_stats(R, S, LS)
    prev = first
    while R.g < gmax:
        R.advance(gstep(R.g))
        g = R.g
        ls = P.light_stats(R, S, LS)
        trace.append({k: ls[k] for k in TRACE_KEYS})
        dg = g - prev['g']
        for k in RES_GROUPS:
            v = 0.5 * (ls[k] + prev[k]) * dg
            if g <= P.G_TAILEND: res_tail[k] += v
            else: res_chase[k] += v
        if ls['top_lin_sh'] >= 0.5 and ls['top_lin'] not in colon:
            colon[ls['top_lin']] = (g, ls['top_lin_sh'])
        t = g - P.MERGE
        if t in P.SNAP_T:
            h = P.heavy_stats(R, S, LS, g)
            h['light'] = ls
            snaps[str(t)] = h
        prev = ls
        if g >= P.MERGE + 50 and (A_exp == 0 or g >= P.G_TAILEND) and R.frozen():
            frozen_at = g
            h = P.heavy_stats(R, S, LS, g)
            h['light'] = ls
            for gend, kk in ((P.G_TAILEND, res_tail), (P.G_END, res_chase)):
                pass
            # exact carry-forward of the residences and of the later snapshots
            for k in RES_GROUPS:
                if g < P.G_TAILEND:
                    res_tail[k] += ls[k] * (P.G_TAILEND - g)
                    res_chase[k] += ls[k] * (P.G_END - P.G_TAILEND)
                else:
                    res_chase[k] += ls[k] * (P.G_END - g)
            for tt in P.SNAP_T:
                if P.MERGE + tt > g and str(tt) not in snaps:
                    snaps[str(tt)] = dict(h, g=P.MERGE + tt, frozen_from=g)
            break
    arr = P.arrival_summary(R, S, LS)
    # colonizations: arrival lineages that reached half of the population
    col = []
    n = int(R.nfr[0])
    for lid, (g, sh) in colon.items():
        q = np.nonzero(R.fr[:n, 4] == lid)[0]
        if len(q) == 0: continue
        q = int(q[0])
        s = int(R.fr[q, 2])
        col.append(dict(lid=int(lid), first_g=int(g), share=r5(sh), arrival_g=int(R.fr[q, 0]), spelling=LS['names'][s],
                        rel_pay=r5(R.frf[q, 1] - R.frf[q, 2]), selected=bool(R.frf[q, 1] - R.frf[q, 2] > 1e-12),
                        suckerE=bool(S['arr_suckerE'][s]), T_H=bool(S['arr_T_H'][s]), prud_H=bool(S['arr_prud_H'][s]),
                        Q=bool(S['Qsp'][s])))
    row = dict(world=w, arm=arm, rep=rep, A=A_exp, depleted=depl, last_gen=int(R.g), frozen_at=frozen_at,
               n_types=int(R.ntv[0]), time_s=time.time() - t0, pre=pre, comp=comp, trace=trace, snaps=snaps,
               res_tail=res_tail, res_chase=res_chase, arrivals=arr, colonizations=col, gmax=gmax)
    return js(row)


# ------------------------------------------------------------------------------------------------ pools
def rkey(r):
    return (r['world'], r['arm'], r['rep'])


def run_pool(jobs, path, workers):
    rows = json.load(gzip.open(path)) if os.path.exists(path) else []
    done = {rkey(r) for r in rows}
    todo = [j for j in jobs if (j[0], j[1], j[2]) not in done]
    log('%s: %d jobs, %d done, %d to run on %d workers (pid %d)' % (os.path.basename(path), len(jobs), len(done),
                                                                    len(todo), workers, os.getpid()))
    if not todo: return rows
    t0 = time.time(); last = time.time()
    with Pool(min(3, workers), maxtasksperchild=2) as pool:
        for r in pool.imap_unordered(pru_job, todo):
            rows.append(r)
            s = r['snaps'].get('10000', {})
            log('  %s %s rep %d: tail-end uo %s pcc %s T %s prud %s last %d frozen %s arrivals %s (%.0fs; total %.0fs)' % (
                r['world'], r['arm'], r['rep'], s.get('universal_open'), s.get('pcc'),
                (s.get('light') or {}).get('T'), (s.get('light') or {}).get('prud'), r['last_gen'], r['frozen_at'],
                r['arrivals'].get('n'), r['time_s'], time.time() - t0))
            if time.time() - last > 60:
                with gzip.open(path + '.tmp', 'wt') as f: json.dump(rows, f)
                os.replace(path + '.tmp', path); last = time.time()
    with gzip.open(path + '.tmp', 'wt') as f: json.dump(rows, f)
    os.replace(path + '.tmp', path)
    return rows


def cost_key(j):
    return (-P.ARMS[j[1]][0], j[1], j[0], j[2])        # arm by cost, then world, then replicate (a worker mostly keeps one world's tables)


def cmd_cells(a):
    jobs = [(w, arm, rep) for arm in a.arms for w in a.worlds for rep in range(a.rep0, a.rep0 + a.reps)]
    jobs.sort(key=cost_key)
    run_pool(jobs, os.path.join(OUT, 'cells_%s.json.gz' % a.out), a.workers)


def cmd_probe(a):
    out = {}
    for spec in a.jobs:
        w, arm, rep, gm = spec.split(':')
        t0 = time.time()
        r = pru_job((w, arm, int(rep), int(gm)))
        out[spec] = dict(time_s=time.time() - t0, last_gen=r['last_gen'], arrivals=r['arrivals'].get('n'),
                         n_types=r['n_types'], frozen_at=r['frozen_at'])
        log(spec, json.dumps(out[spec]))
        if a.keep:
            with gzip.open(os.path.join(OUT, 'probe_%s_%s_%s.json.gz' % (w, arm, rep)), 'wt') as f: json.dump(r, f)
    p = os.path.join(OUT, 'probe.json')
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(out)
    json.dump(old, open(p, 'w'), indent=1)


# ------------------------------------------------------------------------------------------------ validation
def _val_job(job):
    """A0 against the stored fission-fusion row: the stored loop's decompositions at the stored checkpoints."""
    w, rep = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    LS = WK.use_world(w)
    S = P.sets(LS)
    st = stored_ff_rows()[(w, rep)]
    ref = {t['g']: t for t in st['trace']}
    R = P.PruRun(rep, 'A0')
    n = 0; bad = []
    g = 0
    last = st['last_gen']
    while g < last:
        R.advance(10)
        g = R.g
        if g == P.MERGE: R.do_merge()
        if g > last: break
        chk = g <= 500 or g % 50 == 0
        if not chk: continue
        cc = R.island_stats()
        dec = PG.decompose(R, cc, closure=False)
        if g in ref:
            s = ref[g]
            n += 1
            mine = dict(pcc=r5(dec['pcc']), M=r5(dec['M']), target=r5(dec['target']), nt=int(dec['n_types']))
            theirs = dict(pcc=s['pcc'], M=s['M'], target=s['target'], nt=s['nt'])
            if mine != theirs:
                bad.append((g, mine, theirs))
        if g >= 50 and R.frozen():
            break
    return dict(world=w, rep=rep, compared=n, bad=bad[:5], nbad=len(bad), last_gen=int(R.g), stored_last=last,
                frozen_mine=bool(R.frozen()), frozen_stored=st['frozen_at'], time_s=time.time() - t0)


def cmd_validate(a):
    jobs = [(w, rep) for rep in range(a.reps) for w in P.WORLDS]
    res = []
    with Pool(min(3, a.workers), maxtasksperchild=1) as pool:
        for r in pool.imap_unordered(_val_job, jobs):
            log('validate', json.dumps(r))
            res.append(r)
    json.dump(res, open(os.path.join(ROOT, 'runs', 'prudence-validate.json'), 'w'), indent=1)
    log('validation: %d of %d reproduce exactly' % (sum(1 for r in res if r['nbad'] == 0), len(res)))


# ------------------------------------------------------------------------------------------------ statics
def cmd_statics(a):
    out = {}
    for w in P.WORLDS:
        LS = WK.use_world(w)
        S = P.sets(LS)
        mu = LS['mu']
        d = dict(T_units=int(S['T'].sum()), SD_n=int(S['SD'].sum()), SD_mass=float(mu[S['SD']].sum()),
                 suckerE_mass=float(mu[S['arr_suckerE']].sum()), Q_mass=float(mu[S['Qsp']].sum()),
                 T_H_mass=float(mu[S['arr_T_H']].sum()), prud_H_mass=float(mu[S['arr_prud_H']].sum()),
                 pbtree_mass=float(mu[S['arr_pbtree']].sum()), CBo_mass=float(mu[S['arr_CBo']].sum()),
                 premium=P.static_premium(LS))
        out[w] = d
        out[w + '_SD'] = np.nonzero(S['SD'])[0]
    out['SD_equal'] = bool((out.pop('L_SD') == out.pop('K_SD')).all())
    lamA = {str(A): dict(total=float(P.lam(A).sum()), frac_by_1000=float(P.lam(A)[:1000].sum() / P.lam(A).sum()),
                         first=float(P.lam(A)[0]), last=float(P.lam(A)[-1])) for A in (52, 156)}
    out['schedule'] = lamA
    json.dump(js(out), open(os.path.join(ROOT, 'runs', 'prudence-static.json'), 'w'), indent=1)
    log(json.dumps(js(out), indent=1))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('statics')
    p = sub.add_parser('validate'); p.add_argument('--reps', type=int, default=3); p.add_argument('--workers', type=int, default=3)
    p = sub.add_parser('probe'); p.add_argument('--jobs', nargs='+', required=True); p.add_argument('--keep', action='store_true')
    p = sub.add_parser('cells')
    p.add_argument('--arms', nargs='+', default=list(P.ARMS)); p.add_argument('--worlds', nargs='+', default=list(P.WORLDS))
    p.add_argument('--reps', type=int, default=20); p.add_argument('--rep0', type=int, default=0)
    p.add_argument('--workers', type=int, default=3); p.add_argument('--out', required=True)
    a = ap.parse_args()
    {'statics': cmd_statics, 'validate': cmd_validate, 'probe': cmd_probe, 'cells': cmd_cells}[a.cmd](a)


if __name__ == '__main__':
    main()
