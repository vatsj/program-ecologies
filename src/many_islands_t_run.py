"""Driver for the arm-T islands-to-infinity experiment (notes/many-islands-t.md).

    python3 src/many_islands_t_run.py jobs OUT [--stage S ...]     write a job list
    python3 src/many_islands_t_run.py one JOB                      run one job in this process, print a digest
    python3 src/many_islands_t_run.py worker JOBFILE               claim and run the jobs of the file one at a time
    python3 src/many_islands_t_run.py batch JOBFILE --workers K    start K worker processes, wait, stall watchdog

Jobs (fields separated by ':'; a cell is dose|P_fail|A):
    P:<cell>:<pool>                       one founding pool (16,384 islands)
    O:<cell>:<pm>:<start>:<pool>[:raw]    the mean-field ODE from the pool law (start nat, fair, uneq, wd) under the
                                          migration charge pm (P_fail); raw = unsymmetrized
    J:<cell>:<pm>:<pool>                  Jacobian analysis at the symmetric limit and controlled perturbations
    W:<cell>:<I>                          finite worlds (20) at I islands
    X:<cell>:<pm>                         analyses of the kernel (rates, charges) at the post-anneal law and the limit
    V:<name>                              validations

One job per process; no multiprocessing.Pool.  Per-job records go to $MIT_SCRATCH/out/<job>.json (outside the repository);
many_islands_t_report.py aggregates them into runs/many-islands-t.{md,json} and runs/many_islands_t/.
"""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import argparse, json, subprocess, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import many_islands_t as M
import many_islands_t_ode as O

from many_islands_t_common import (SCR, OUT, POOLS, XSTAR, NPOOL, NISL, DOSEID, parse_cell, cname, job_name, result_path, tabs,
                                   get_pf, pool_path, load_pool, xstar_path)
STARTS = ('nat', 'fair', 'uneq', 'wd')
WORLD_I = (64, 256, 1024, 4096)
NWORLDS = 20
CPS = (1, 3, 10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000)


# ---------------------------------------------------------------- cells
def cells_main():
    cs = []
    for dose in M.DOSES:
        for P in ('0', '0.1'):
            cs.append('%s|%s|0' % (dose, P))
    cs.append('main|0.03|0')
    cs.append('main|0|150')
    cs.append('main|0.1|150')
    return cs


def cells_ablation():
    return ['%s|%s|0' % (d, P) for d in ('ab-So', 'ab-D', 'ab-X') for P in ('0', '0.1')]


# ---------------------------------------------------------------- jobs
def run_pool(cell, pool, n=NISL):
    t0 = time.time()
    T = tabs()
    dose, P, A = parse_cell(cell)
    PT = T.payoff(P)
    law = M.seed_law(T, dose)
    cum = M.cum_of(law)
    rng = np.random.default_rng([17, DOSEID[dose], A, pool, 20261029])
    hist = np.zeros(M.NT, np.int64)
    n_capped = n_late = n_mixed = n_drift = 0
    gens = []
    for i in range(n):
        seed = int(rng.integers(1 << 31))
        r = M.build_island(PT, law, cum, rng, seed, A=A)
        gens.append(r['gen'])
        if r['status'] == 0:
            hist[O.tidx(*r['triple'])] += 1
            continue
        n_capped += 1
        counts = r['counts']
        status, g, counts2, _ = M.island_run_t(PT, counts.copy(), M.N0, M.W, (seed + 1) % (2 ** 31), 5000, np.zeros(0), cum, True)
        if status == 0:
            tr = M.triple_of(counts2)
            hist[O.tidx(*tr)] += 1
            n_late += 1
        else:
            f1 = counts / M.N0; f2 = counts2 / M.N0
            lost = ((counts > 0) & (counts2 == 0)).any()
            if (np.abs(f1 - f2).max() < 0.1) and not lost:
                n_mixed += 1
            else:
                n_drift += 1
    os.makedirs(POOLS, exist_ok=True)
    np.savez(pool_path(cell, pool), hist=hist.astype(np.int32))
    x = O.hist_to_x(hist)
    sh, pairs = O.class_shares(x, T, True)
    return dict(cell=cell, pool=pool, n=n, settled=int(hist.sum()), capped=n_capped, late=n_late, mixed=n_mixed, drifting=n_drift,
                support=int((hist > 0).sum()), shares=sh.tolist(), pairs=pairs.tolist(),
                readers=O.reader_marginals(x, T).tolist(), mean_gen=float(np.mean(gens)), max_gen=int(max(gens)),
                wall=round(time.time() - t0, 1))


def start_law(cell, pool, start, raw=False):
    T = tabs()
    x = O.hist_to_x(load_pool(cell, pool))
    if raw:
        return x, None
    xs = O.symmetrize(x)
    if start == 'nat':
        return xs, dict(kind='nat')
    kind = {'fair': 'fair', 'uneq': 'unequal', 'wd': 'wd'}[start]
    y, info = O.tilt(xs, T, kind)
    return y, info


def run_ode(cell, pm, start, pool, raw=False):
    t0 = time.time()
    T = tabs()
    PF = get_pf(pm)
    x0, info = start_law(cell, pool, start, raw)
    if x0 is None:
        return dict(cell=cell, pm=pm, start=start, pool=pool, raw=raw, available=False, tilt=info)
    sym = not raw
    recs, x, st, _ = O.integrate(x0, PF, 1e5, T, sym=sym, stop_converged=sym)
    status = st
    if status != 'converged':
        tmax = 1e7 if sym else 1e6
        recs, x, status = O.integrate_be(x, 1e5, PF, T, tmax, sym=sym, steps_per_decade=8, recs=recs)
    out = dict(cell=cell, pm=pm, start=start, pool=pool, raw=raw, available=True, tilt=info, status=status, recs=recs,
               final_shares=recs[-1]['shares'], final_pairs=recs[-1]['pairs'], final_readers=recs[-1]['readers'],
               t_end=recs[-1]['t'], resid_end=recs[-1]['resid'], nonsym_end=float(np.abs(x - O.symmetrize(x)).sum()),
               min_x=min(r['minx'] for r in recs), mass_dev=max(abs(r['mass'] - 1.0) for r in recs))
    if start == 'nat' and pool == 0 and not raw:
        # tolerance check: tighter explicit tolerance to 1e4 and finer BE steps from 1e4
        recs_a, xa, sta, kept = O.integrate(x0, PF, 1e4, T, sym=True, rtol=1e-10, atol=1e-16, stop_converged=False)
        recs_b, xb, stb = O.integrate_be(xa, 1e4, PF, T, recs[-1]['t'] if recs[-1]['t'] >= 1e4 else 1e4, sym=True, steps_per_decade=16,
                                         recs=list(recs_a))
        ref = {r['t']: r for r in recs}
        d4 = float(np.abs(np.array(recs_a[-1]['shares']) - np.array(ref[1e4]['shares'])).max())
        dend = float(np.abs(np.array(recs_b[-1]['shares']) - np.array(recs[-1]['shares'])).max())
        out['tolcheck'] = dict(rtol_ref=1e-8, rtol_tight=1e-10, max_share_diff_at_1e4=d4, max_share_diff_end=dend,
                               be_steps_ref=8, be_steps_fine=16, t_end=recs_b[-1]['t'])
    os.makedirs(XSTAR, exist_ok=True)
    np.save(xstar_path(cell, pm, start, pool, raw), x)
    out['wall'] = round(time.time() - t0, 1)
    return out


def run_world_job(cell, I, start='raw'):
    import many_islands_t_worlds as WD
    T = tabs()
    dose, P, A = parse_cell(cell)
    PF = get_pf(P)
    hist = sum(load_pool(cell, p) for p in range(NPOOL))
    if start != 'raw':
        # worlds founded from the tilted symmetrized pooled law (the same tilt as the ODE start)
        kind = {'fair': 'fair', 'uneq': 'unequal', 'wd': 'wd'}[start]
        y, info = O.tilt(O.symmetrize(O.hist_to_x(hist)), T, kind)
        hist = y
    cps = np.array(CPS, np.int64)
    rows = []
    t0 = time.time()
    for w in range(NWORLDS):
        rng = np.random.default_rng([31, DOSEID[dose], int(round(P * 1000)), A, I, w])
        tri = WD.sample_world(hist, I, rng)
        r = WD.run_world(PF, T, tri, cps, int(rng.integers(1 << 31)))
        rows.append(dict(w=w, hist=r['hist'].tolist(), pairs=r['pairs'].tolist(), first_loss=r['first_loss'].tolist(),
                         events=r['events']))
    return dict(cell=cell, I=I, cps=list(CPS), worlds=rows, wall=round(time.time() - t0, 1))


def run_worldx_job(cell, I, Tmax, nworlds=None):
    """long finite worlds: checkpoints 1, 3, 10, ... up to Tmax events per island."""
    import many_islands_t_worlds as WD
    T = tabs()
    dose, P, A = parse_cell(cell)
    PF = get_pf(P)
    hist = sum(load_pool(cell, p) for p in range(NPOOL))
    cps = []
    e = 0
    while 10 ** e <= Tmax:
        for m in (1, 3):
            if m * 10 ** e <= Tmax:
                cps.append(m * 10 ** e)
        e += 1
    cps = np.array(sorted(set(cps)), np.int64)
    rows = []
    t0 = time.time()
    for w in range(nworlds or NWORLDS):
        rng = np.random.default_rng([37, DOSEID[dose], int(round(P * 1000)), A, I, w])
        tri = WD.sample_world(hist, I, rng)
        r = WD.run_world(PF, T, tri, cps, int(rng.integers(1 << 31)))
        rows.append(dict(w=w, hist=r['hist'].tolist(), pairs=r['pairs'].tolist(), first_loss=r['first_loss'].tolist(), events=r['events']))
    return dict(cell=cell, I=I, cps=cps.tolist(), worlds=rows, wall=round(time.time() - t0, 1))


def run_job(j):
    parts = j.split(':')
    if parts[0] == 'P':
        return dict(job=j, **run_pool(parts[1], int(parts[2])))
    if parts[0] == 'O':
        raw = len(parts) > 5 and parts[5] == 'raw'
        return dict(job=j, **run_ode(parts[1], float(parts[2]), parts[3], int(parts[4]), raw))
    if parts[0] == 'W':
        return dict(job=j, **run_world_job(parts[1], int(parts[2]), parts[3] if len(parts) > 3 else 'raw'))
    if parts[0] == 'WX':
        return dict(job=j, **run_worldx_job(parts[1], int(parts[2]), int(float(parts[3])), int(parts[4]) if len(parts) > 4 else None))
    if parts[0] == 'J':
        import many_islands_t_jobs as JB
        return dict(job=j, **JB.run_jac(parts[1], float(parts[2]), int(parts[3])))
    if parts[0] == 'X':
        import many_islands_t_jobs as JB
        return dict(job=j, **JB.run_analysis(parts[1], float(parts[2])))
    if parts[0] == 'V':
        import many_islands_t_validate as VA
        return dict(job=j, **VA.run(parts[1]))
    raise ValueError(j)


def _default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, tuple)):
        return list(o)
    if isinstance(o, complex):
        return [o.real, o.imag]
    raise TypeError(type(o))


def worker(jobfile):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, '_claims'), exist_ok=True)
    jobs = [l.strip() for l in open(jobfile) if l.strip() and not l.startswith('#')]
    for j in jobs:
        if os.path.exists(result_path(j)):
            continue
        claim = os.path.join(OUT, '_claims', job_name(j))
        try:
            fd = os.open(claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode()); os.close(fd)
        except FileExistsError:
            continue
        t0 = time.time()
        try:
            rec = run_job(j)
        except Exception as e:
            print('FAIL', j, repr(e), flush=True)
            import traceback; traceback.print_exc()
            continue
        tmp = result_path(j) + '.tmp'
        json.dump(rec, open(tmp, 'w'), default=_default)
        os.replace(tmp, result_path(j))
        print('done', j, 'wall %.0f' % (time.time() - t0), flush=True)


def batch(jobfile, workers, stall_hours=2.0, log=None):
    here = os.path.abspath(__file__)
    procs = []
    os.makedirs(OUT, exist_ok=True)
    logf = open(log or os.path.join(OUT, 'batch.log'), 'a')
    for k in range(workers):
        procs.append(subprocess.Popen([sys.executable, here, 'worker', jobfile], stdout=logf, stderr=subprocess.STDOUT))
    last = time.time(); lastsize = -1
    while True:
        time.sleep(30)
        if all(p.poll() is not None for p in procs):
            print('BATCH DONE', flush=True)
            return 0
        sz = os.path.getsize(logf.name)
        if sz != lastsize:
            lastsize = sz; last = time.time()
        elif time.time() - last > stall_hours * 3600:
            print('STALL: log unchanged for %.1f h; killing workers %s' % (stall_hours, [p.pid for p in procs]), flush=True)
            for p in procs:
                if p.poll() is None:
                    p.kill()
            return 2


# ---------------------------------------------------------------- stages
def stage_valid():
    return ['V:tables', 'V:charge', 'V:ode']


def stage_valid2():
    return ['V:kernel', 'V:founding', 'V:arch', 'V:dslcmp']


def stage_pools():
    return ['P:%s:%d' % (c, p) for c in cells_main() for p in range(NPOOL)]


def stage_ode():
    js = []
    for c in cells_main():
        dose, P, A = parse_cell(c)
        for pool in range(NPOOL):
            for st in STARTS:
                js.append('O:%s:%s:%s:%d' % (c, P, st, pool))
            js.append('O:%s:%s:nat:%d:raw' % (c, P, pool))
    return js


def stage_cross():
    js = []
    for pf, pm in (('0', 0.1), ('0.1', 0.0)):
        c = 'main|%s|0' % pf
        for pool in range(NPOOL):
            js.append('O:%s:%s:nat:%d' % (c, pm, pool))
            js.append('O:%s:%s:uneq:%d' % (c, pm, pool))
    return js


def stage_jac():
    return ['J:%s:%s:%d' % (c, parse_cell(c)[1], 0) for c in cells_main()]


def stage_x():
    return ['X:%s:%s' % (c, parse_cell(c)[1]) for c in cells_main()]


def stage_worlds():
    cs = ['main|0.1|0', 'main|0|0', '0|0|0']
    js = ['W:%s:%d' % (c, I) for I in WORLD_I for c in cs]
    js += ['W:%s:%d:uneq' % (c, I) for I in (1024, 4096) for c in cs]
    return js


def stage_worldsx():
    cs = ['main|0.1|0', 'main|0|0', '0|0|0']
    return ['WX:%s:%d:%d' % (c, I, T) for (I, T) in ((64, 10 ** 7), (256, 3 * 10 ** 6), (1024, 10 ** 6)) for c in cs]


def stage_worlds_big():
    return ['WX:0|0|0:16384:100000:10', 'WX:main|0.1|0:16384:100000:10', 'WX:0|0|0:65536:30000:6']


def stage_abl_pools():
    return ['P:%s:%d' % (c, p) for c in cells_ablation() for p in range(NPOOL)]


def stage_abl_ode():
    js = []
    for c in cells_ablation():
        P = parse_cell(c)[1]
        for pool in range(NPOOL):
            js.append('O:%s:%s:nat:%d' % (c, P, pool))
    return js


STAGES = {'valid': stage_valid, 'valid2': stage_valid2, 'pools': stage_pools, 'ode': stage_ode, 'cross': stage_cross, 'jac': stage_jac,
          'x': stage_x, 'worlds': stage_worlds, 'worldsx': stage_worldsx, 'worlds_big': stage_worlds_big, 'abl_pools': stage_abl_pools, 'abl_ode': stage_abl_ode}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('a', nargs='*')
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--stage', nargs='*', default=list(STAGES))
    a = ap.parse_args()
    if a.cmd == 'one':
        rec = run_job(a.a[0])
        print(json.dumps(rec, default=_default)[:3000])
    elif a.cmd == 'worker':
        worker(a.a[0])
    elif a.cmd == 'batch':
        sys.exit(batch(a.a[0], a.workers))
    elif a.cmd == 'jobs':
        lines = []
        for st in a.stage:
            lines += STAGES[st]()
        open(a.a[0], 'w').write('\n'.join(lines) + '\n')
        print(len(lines), 'jobs')


if __name__ == '__main__':
    main()
