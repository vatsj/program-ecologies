"""Driver for hooks Part R (notes/hooks-r.md; predictions/2026-10-18-hooks-r.md).

    python3 src/hooks_r_run.py gate                          # term-level gate -> runs/hooks-r-gate.json
    python3 src/hooks_r_run.py validate [--gens 300]         # baseline B against world K's kernel, draw for draw
    python3 src/hooks_r_run.py statics                       # static numbers of grammar H and the seeded fills
    python3 src/hooks_r_run.py audit --cell M --rep 990      # Lemma H against the true hooked carriers
    python3 src/hooks_r_run.py cells --cells M I ... --reps 20 --horizon 10000 [--workers 3] [--rep0 0]
Rows go to runs/hooks_r/rows_<cell>.json.gz (one file per cell; resumable); summaries to runs/hooks-r.json.
"""
import os
for _v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')     # one job per process: no BLAS thread pools
import argparse
import gzip
import json
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'hooks_r')
os.makedirs(OUT, exist_ok=True)
SNAPS = (200, 500, 1000, 2000, 5000, 10000)
NET_AT = (50, 100, 300, 750, 1500, 3000, 4000)


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


# ------------------------------------------------------------------------------------------------ one run
def snapshot(R, full=True, net=True):
    """Checkpoint statistics: the mass-based classifier (hooks_r.HRun.net_stats), counters, and at full snapshots the
    per-island records, fill statistics and founder establishment (the majority spelling's local-lineage share)."""
    cc = R.island_stats()
    out = dict(g=int(R.g), ctr=R.ctr.tolist(), scope_ex=R.scope_ex.tolist(), src_ex=R.src_ex.tolist())
    if not net:
        out.update(pcc=float(np.mean(cc)), n_types=int(len(R.living()[0])), cc=[round(float(x), 4) for x in cc],
                   fills=R.fill_stats())
        return out
    ns = R.net_stats(cc)
    out.update(ns)
    if not full:
        for k in ('open_share', 'target_share', 'own_share', 'maj_sp', 'maj_sp_share', 'maj_hooked'):
            out.pop(k, None)
    if full:
        out['cc'] = [round(float(x), 4) for x in cc]
        if not R.merged:
            loc = []
            for i in range(R.I):
                spi = ns['maj_sp'][i]
                idx = R.tsp[R.slots[i]] == spi
                l = R.lin[i, idx]
                loc.append(round(float(((l - 1) // R.N == i).mean()), 3) if len(l) else None)
            out['local'] = loc
        out['fills'] = R.fill_stats()
        h = __import__('hooks_r')._HOST.get('h')
        if h is not None:
            out['host_n'] = dict(h.n_calls); out['host_t'] = {k: round(v, 2) for k, v in h.t_calls.items()}
    return out


def run_job(job):
    """job = (cell, rep, horizon) -> row."""
    import hooks_r as H
    cell, rep, horizon = job
    sys.setrecursionlimit(1000000)
    t0 = time.time()
    R = H.HRun(cell, rep)
    t_init = time.time() - t0
    c = H.CELLS[cell]
    snaps = {}
    trace = []
    snaps['0'] = snapshot(R, full=True, net=False)
    nxt = [g for g in SNAPS if g <= horizon]
    if horizon not in nxt: nxt.append(horizon)
    step = 10
    last_save = time.time()
    while R.g < horizon:
        if c['ff'] and not R.merged and R.g == H.MERGE_AT:
            R.merge()
        gstep = 10 if R.g < 200 else 50 if R.g < 1000 else 250
        target = min(horizon, R.g + gstep)
        if c['ff'] and not R.merged and R.g < H.MERGE_AT < target: target = H.MERGE_AT
        R.advance(target - R.g)
        if R.g in nxt:
            snaps[str(R.g)] = snapshot(R, full=True)
            s = snaps[str(R.g)]
            trace.append((R.g, round(s['pcc'], 4), int(s['uo']), s.get('n_ident', -1), s.get('n_rival', -1),
                          s.get('n_unheld', -1), s['n_types']))
        elif R.g in NET_AT:
            s = snapshot(R, full=False)
            snaps[str(R.g)] = s
            trace.append((R.g, round(s['pcc'], 4), int(s['uo']), s.get('n_ident', -1), s.get('n_rival', -1),
                          s.get('n_unheld', -1), s['n_types']))
        else:
            cc = R.island_stats()
            trace.append((R.g, round(float(np.mean(cc)), 4), -1, -1, -1, int((cc < 0.5).sum()), -1))
        if time.time() - last_save > 1800:
            R.save(); last_save = time.time()
    n_saved = R.save()
    h = H._HOST.get('h')
    row = dict(cell=cell, rep=rep, horizon=horizon, N=R.N, I=R.I, ff=c['ff'], snaps=snaps, trace=trace,
               final=snaps.get(str(horizon)), t_init=t_init, time_s=time.time() - t0, cache_loaded=R.n_loaded,
               cache_saved=n_saved, n_gc=R.n_gc, kcap=int(R.tsp.shape[0]),
               host_n=dict(h.n_calls) if h else None, host_t=dict(h.t_calls) if h else None)
    return js(row)


def short(r):
    f = r['final']
    if f is None: return '%s rep %d: no final' % (r['cell'], r['rep'])
    return '%s rep %d: uo %s uot %s cls %s pcc %.3f types %d (%.0fs, init %.0fs)' % (
        r['cell'], r['rep'], f['uo'], f['uot'], (f.get('cls') or '').replace('o', '')[:24] or '-', f['pcc'],
        f['n_types'], r['time_s'], r['t_init'])


def rows_path(cell):
    return os.path.join(OUT, 'rows_%s.json.gz' % cell)


def load_rows(cell):
    p = rows_path(cell)
    return json.load(gzip.open(p)) if os.path.exists(p) else []


def save_rows(cell, rows):
    p = rows_path(cell)
    with gzip.open(p + '.tmp', 'wt') as f: json.dump(rows, f)
    os.replace(p + '.tmp', p)


def cmd_cells(a):
    jobs = []
    for cell in a.cells:
        done = {(r['rep'], r['horizon']) for r in load_rows(cell)}
        for rep in range(a.rep0, a.rep0 + a.reps):
            if (rep, a.horizon) not in done:
                jobs.append((cell, rep, a.horizon))
    log('cells %s: %d jobs to run on %d workers (pid %d)' % (a.cells, len(jobs), a.workers, os.getpid()))
    if not jobs: return
    t0 = time.time()
    with Pool(min(3, a.workers), maxtasksperchild=1) as pool:
        for r in pool.imap_unordered(run_job, jobs):
            rows = load_rows(r['cell'])
            rows = [x for x in rows if not (x['rep'] == r['rep'] and x['horizon'] == r['horizon'])] + [r]
            save_rows(r['cell'], rows)
            log('  %s (total %.0fs)' % (short(r), time.time() - t0))


def cmd_one(a):
    r = run_job((a.cell, a.rep, a.horizon))
    log(short(r))
    if a.save:
        rows = load_rows(r['cell'])
        rows = [x for x in rows if not (x['rep'] == r['rep'] and x['horizon'] == r['horizon'])] + [r]
        save_rows(r['cell'], rows)
    else:
        json.dump(r, open(os.path.join(OUT, 'probe_%s_%d.json' % (a.cell, a.rep)), 'w'))


def cmd_gate(a):
    import hooks_r_gate as G
    out = G.gate(log=log)
    json.dump(js({k: v for k, v in out.items() if k != 'rows'}), open(os.path.join(ROOT, 'runs', 'hooks-r-gate.json'),
                                                                     'w'), indent=1)
    with gzip.open(os.path.join(OUT, 'gate_rows.json.gz'), 'wt') as f: json.dump(js(out['rows']), f)


def cmd_validate(a):
    """Grammar P founders, no hooks: the hooked kernel against world K's annealed kernel (draw for draw), and the
    mass-based classifier against world K's type-level classifier on the same trajectory."""
    import hooks_r as H
    import world_k as WK
    H.statics()
    out = []
    for rep in a.reps:
        WK.use_world('K')
        R = WK.IslandRun('wk_Snon_200_64', rep, track=True)
        X = H.HRun('B', rep)
        nd = 0; checks = []
        for g in range(1, a.gens + 1):
            R.advance(1); X.advance(1)
            if not (R.tsp[R.slots] == X.tsp[X.slots]).all(): nd += 1
            if g in (50, 100, 200, 300, 500, 1000, 2000) and g <= a.gens:
                cc = X.island_stats(); ccR = np.asarray(R.island_stats())
                ns = X.net_stats(cc); ct = X.classify(cc)
                checks.append(dict(g=g, pcc_diff=float(np.abs(cc - ccR).max()), mass_uo=ns['uo'],
                                   type_uo=bool(ct['cl']['universal_open']), mass_cls=ns['cls'],
                                   type_cls=''.join({'': 'o', 'identity': 'i', 'rival': 'r', 'unheld': 'u'}[f]
                                                    for f in ct['cl']['fail'])))
        out.append(dict(rep=rep, gens=a.gens, slot_differences=nd, checks=checks))
        log('validate rep %d: %d generations with slot differences; %s' % (rep, nd, checks[-1]))
    json.dump(js(out), open(os.path.join(ROOT, 'runs', 'hooks-r-validate.json'), 'w'), indent=1)


def cmd_audit(a):
    """Lemma H on live runs: kernel plays against the executed true hooked carriers at sampled generations."""
    import hooks_r as H
    import hooks_r_gate as G
    out = []
    for cell in a.cells:
        R = H.HRun(cell, a.rep)
        for g in a.gens:
            if g > R.g: R.advance(g - R.g)
            r = G.audit(R, n_pairs=a.pairs, seed=g, log=log)
            r['cell'] = cell; r['rep'] = a.rep
            out.append(r)
        R.save()
    p = os.path.join(ROOT, 'runs', 'hooks-r-audit.json')
    old = json.load(open(p)) if os.path.exists(p) else []
    json.dump(js(old + out), open(p, 'w'), indent=1)


def cmd_statics(a):
    """Static numbers of grammar H and of the seeded fills over the replicates' founders (notes §2)."""
    import hooks_r as H
    S_ = H.statics()
    gh = S_['gh']
    mu = gh.mu
    out = dict(spellings=int(gh.S), P=int(gh.NP), hooked=int(gh.S - gh.NP))
    out['mass_P'] = float(mu[:gh.NP].sum()); out['mass_1tag'] = float(mu[gh.ntags == 1].sum())
    out['mass_2tag'] = float(mu[gh.ntags == 2].sum())
    reps = []
    for rep in range(a.reps):
        sp, fills = H.founders_H(200, 64, rep)
        n_f = np.zeros(6); n_self = 0; n_keyed = 0; n_keyed_present = 0; n_hooked = 0; n_with = 0
        distinct = len(np.unique(sp))
        for i in range(64):
            present = set(sp[i].tolist())
            for j in range(200):
                fl = fills[i][j]
                if gh.ntags[sp[i, j]]: n_hooked += 1
                if fl: n_with += 1
                for (t, sc, key, act, src) in fl:
                    n_f[sc] += 1
                    if sc == H.SC_SRC and key == H.SELF_KEY: n_self += 1
                    elif sc in (H.SC_SRC, H.SC_HIST):
                        n_keyed += 1
                        if key in present and key != sp[i, j]: n_keyed_present += 1
        reps.append(dict(distinct_spellings=distinct, hooked=n_hooked, with_fills=n_with, fills_by_scope=n_f.tolist(),
                         self_fills=n_self, keyed=n_keyed, keyed_present_on_island=n_keyed_present))
    out['reps'] = reps
    agg = lambda k: float(np.mean([r[k] for r in reps]))
    out['mean'] = {k: agg(k) for k in ('distinct_spellings', 'hooked', 'with_fills', 'self_fills', 'keyed',
                                        'keyed_present_on_island')}
    out['mean']['fills_by_scope'] = np.mean([r['fills_by_scope'] for r in reps], 0).tolist()
    json.dump(js(out), open(os.path.join(ROOT, 'runs', 'hooks-r-static.json'), 'w'), indent=1)
    log(json.dumps(js({k: v for k, v in out.items() if k != 'reps'}), indent=1))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    s = sub.add_parser('cells'); s.add_argument('--cells', nargs='+'); s.add_argument('--reps', type=int, default=20)
    s.add_argument('--rep0', type=int, default=0); s.add_argument('--horizon', type=int, default=2000)
    s.add_argument('--workers', type=int, default=3)
    s = sub.add_parser('one'); s.add_argument('--cell'); s.add_argument('--rep', type=int, default=990)
    s.add_argument('--horizon', type=int, default=200); s.add_argument('--save', action='store_true')
    sub.add_parser('gate')
    s = sub.add_parser('statics'); s.add_argument('--reps', type=int, default=20)
    s = sub.add_parser('audit'); s.add_argument('--cells', nargs='+', default=['M']); s.add_argument('--rep', type=int,
                                                                                                 default=991)
    s.add_argument('--gens', type=int, nargs='+', default=[0, 30, 200]); s.add_argument('--pairs', type=int, default=150)
    s = sub.add_parser('validate'); s.add_argument('--reps', type=int, nargs='+', default=[0, 1])
    s.add_argument('--gens', type=int, default=500)
    a = ap.parse_args()
    {'cells': cmd_cells, 'one': cmd_one, 'gate': cmd_gate, 'statics': cmd_statics, 'audit': cmd_audit,
     'validate': cmd_validate}[a.cmd](a)


if __name__ == '__main__':
    main()
