"""Job layer of the annealed-tail experiment: one JSON job per line, lock-file workers (at most 3 processes).

    python3 src/annealed_tail_jobs.py worker JOBFILE WID

Job fields:
  kind     'dsl' | 'armT' | 'late0' (store the tail-free M state at tau = 1e6 and the endpoint, with the donor marginals)
  cell     DSL: 'M0' | 'L0';  armT: 'main|0.1|0' ...
  start    'nat' | 'u:<u>' | 'late'  (late: the stored tail-free state at tau = t_s = 1e6, the tail clock restarted)
  sched    {kind: 'anneal'|'const', Lam, t0 | T}
  tail     'full' | 'bully' | 'victim' | 'bully+victim' | 'cond'   (matched-dose removals from the tail law; founding unchanged)
  renorm   rescale the remaining tail law to its original mass (secondary versions)
  N        fixation table for migration and tail (default 100)
  early    allow early classification (scans / bisection)
  obj      'P' (default) | 'm1core' | 'm1full'   (object variants of cell 6b)
  tag      free label (part of the row key)
"""
import os, sys, json, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import annealed_tail as A
import unequal_basin as UB

_CACHE = {}


def get_dsl(job):
    cell_name = job['cell']
    objv = job.get('obj', 'P')
    N = job.get('N', 100)
    tail = job.get('tail', 'full')
    renorm = bool(job.get('renorm', False))
    key = ('dsl', cell_name, objv, N, tail, renorm)
    if key not in _CACHE:
        if objv == 'P':
            cell, obj, xn, dropped = A.dsl_base(cell_name, 'pilot_L', 3)
        elif objv == 'm1full':
            cell, obj, xn, dropped = A.dsl_base(cell_name, None, 1)
        elif objv == 'm1core':
            cell, obj, xn, dropped = A.dsl_m1core(cell_name)
        else:
            raise ValueError(objv)
        p = A.tail_law(cell, tail, renorm)
        S = A.DSL(obj, p, A.pf_table(N), label='%s %s N=%s tail=%s' % (cell_name, objv, N, tail))
        _CACHE[key] = (cell, obj, xn, S, dropped)
    return _CACHE[key]


def late_state(cell_name, N=100):
    path = os.path.join(A.XSD, 'late_%s_N%d.npz' % (cell_name, N))
    for _ in range(120):
        if os.path.exists(path):
            time.sleep(2)
            break
        time.sleep(30)
    z = np.load(path)
    return z['x'], z['x_end']


def run_job(job, verbose=False):
    if job['kind'] == 'bisect':
        return run_bisect(job)
    sc = job['sched']
    sched = A.Sched(sc['kind'], sc['Lam'], sc.get('t0', 1.0), sc.get('T', 1e4))
    t_wall = time.time()
    if job['kind'] == 'late0':
        cell, obj, xn, S, dropped = get_dsl(dict(job, tail='full'))
        x0, _ = A.dsl_start(obj, xn, 'nat')
        free = A.Sched('anneal', 0.0)
        res, xe, kept = A.run_cell(S, x0, free, tmax=1e8, keep_at=(1e6,), early=False)
        # keep_at is honoured by integrate; run_cell returns kept states only through the third value
        x_late = kept.get(1e6)
        if x_late is None:
            x_late = xe          # the tail-free object had already converged before tau = 1e6: its endpoint is the state at t_s
        np.savez_compressed(os.path.join(A.XSD, 'late_%s_N%d.npz' % (job['cell'], job.get('N', 100))), x=x_late, x_end=xe)
        q = obj.marg(x_late)
        extra = dict(donor_const=[[float(q[s][x]) for x in range(9)] for s in range(3)],
                     shares_late=[float(v) for v in obj.class_shares(x_late)])
        return A.save_row(job, res, extra)
    if job['kind'] == 'dsl':
        cell, obj, xn, S, dropped = get_dsl(job)
        if job['start'] == 'late':
            x0, _ = late_state(job['cell'], job.get('N', 100))
            sinfo = dict(kind='late')
        else:
            x0, sinfo = A.dsl_start(obj, xn, job['start'])
        if x0 is None:
            return A.save_row(job, dict(status='unavailable'))
        res, xe, kept = A.run_cell(S, x0, sched, tmax=job.get('tmax', 1e8), early=bool(job.get('early', False)),
                                   spd=job.get('spd', 8), verbose=verbose, explicit_until=job.get('explicit_until', 4e4), rtol=job.get('rtol', 1e-8))
        row = A.save_row(job, res, dict(states=obj.n, dropped_mass=dropped, start_info=sinfo))
        if job.get('keep_x'):
            np.savez_compressed(os.path.join(A.XSD, A.row_key(job) + '.npz'), x=xe)
        return row
    if job['kind'] == 'bisect':
        return run_bisect(job)
    if job['kind'] == 'tailonly':
        # the tail alone (no migration): dx/ds = G(x; p) at unit rate to s = tmax; the stationary law the tail itself imposes
        cell, obj, xn, S, dropped = get_dsl(job)
        x0, sinfo = A.dsl_start(obj, xn, job['start'])

        class TailOnly(A.DSL):
            def F(self, x):
                return np.zeros_like(x)
        S2 = TailOnly(obj, S.p, S.PF)
        sch = A.Sched('const', float(job.get('tmax', 1e3)), T=float(job.get('tmax', 1e3)))
        recs, x, st, _ = A.integrate(S2, x0, sch, 0.0, float(job.get('tmax', 1e3)), float(job.get('tmax', 1e3)), stop_stationary=False)
        res = dict(status=st, shares=recs[-1]['shares'], pairs=recs[-1]['pairs'], tau_end=recs[-1]['t'], protocol='tailonly',
                   records=[dict(t=r['t'], shares=r['shares']) for r in recs], resid_G=float(np.abs(S2.G(x)).sum()), **{'class': 'U' if recs[-1]['shares'][1] >= 0.5 else ('F' if recs[-1]['shares'][0] >= 0.5 else 'other')})
        return A.save_row(job, res, dict(start_info=sinfo))
    if job['kind'] == 'asym':
        # S3-asymmetric perturbation of a saved tail-free endpoint (the Lam = 0 row of `source`, run with keep_x), integrated without projection
        cell, obj, xn, S, dropped = get_dsl(dict(job, tail='full'))
        S2 = A.DSL(obj, S.p, S.PF, sym=False, label='asym')
        xe = np.load(os.path.join(A.XSD, A.row_key(job['source']) + '.npz'))['x']
        d = float(job['delta'])
        f = np.ones(obj.n)
        f[obj.pair == 0] += d
        f[obj.pair == 1] -= d
        x0 = xe * f
        x0 = x0 / x0.sum()
        res, xe2, kept = A.run_cell(S2, x0, A.Sched('anneal', 0.0), tmax=float(job.get('tmax', 1e6)), explicit_until=job.get('explicit_until', 4e4))
        res['pairs_end'] = res.get('pairs')
        return A.save_row(job, res, dict(delta=d))
    if job['kind'] == 'attr':
        import annealed_tail_attr as AT
        cell, obj, xn, S, dropped = get_dsl(job)
        x0, sinfo = A.dsl_start(obj, xn, job['start']) if job['start'] != 'late' else (late_state(job['cell'], job.get('N', 100))[0], None)
        res = AT.run_attr(S, cell, x0, sched, tmax=job.get('tmax', 1e5))
        return A.save_row(job, res, dict(states=obj.n))
    if job['kind'] == 'armT':
        cn, pm, ad = job['cell'].split('|')
        S, T, CT = A.armT_system(job['cell'], float(pm), tail_dose=job.get('tail_dose'))
        if job.get('N') and int(job['N']) != 100:
            raise NotImplementedError
        x0, sinfo = A.armT_start(job['cell'], job['start'])
        if x0 is None:
            return A.save_row(job, dict(status='unavailable'))
        res, xe, kept = A.run_cell(S, x0, sched, tmax=job.get('tmax', 1e8), early=bool(job.get('early', False)),
                                   spd=job.get('spd', 8), verbose=verbose, explicit_until=job.get('explicit_until', 1e4))
        return A.save_row(job, res, dict(start_info=sinfo))
    raise ValueError(job['kind'])


def vstar_of(row):
    sh = row.get('shares')
    return None if sh is None else float(sh[0])


def with_lam(base, lam):
    j = json.loads(json.dumps(base))
    j['sched']['Lam'] = float(lam)
    return j


def run_one(base, lam):
    j = with_lam(base, lam)
    r = A.load_row(j)
    if r is None:
        r = run_job(j)
    return r


def run_bisect(job):
    """Lam*: the first Lam on the grid whose endpoint crosses V* = 0.5 (mode 'rescue': V* >= 0.5 from a start below; mode 'harm': V* < 0.5
    from a start above), bisected in log Lam to a factor `ratio`.  base: a dsl/armT job template; lams: the grid (rows computed if
    absent).  In 'rescue' mode the search extends below the grid (down to 1e-3) when the first grid value already flips."""
    base = job['base']
    ratio = float(job.get('ratio', 1.25))
    mode = job.get('mode', 'rescue')
    lams = sorted(job['lams'])
    flips = (lambda v: v is not None and v >= 0.5) if mode == 'rescue' else (lambda v: v is not None and v < 0.5)
    vs = {}
    for lam in lams:
        vs[lam] = vstar_of(run_one(base, lam))
    first = next((i for i, l in enumerate(lams) if flips(vs[l])), None)
    out = dict(series=base, mode=mode, grid={str(l): vs[l] for l in lams}, ratio=ratio)
    if first is None:
        out.update(lam_star=None, note='none on the grid')
        return A.save_row(job, out)
    hi = lams[first]
    if first == 0:
        lo = None
        cand = hi
        while cand > 1.1e-3:
            cand = cand / 3.1623
            v = vstar_of(run_one(base, cand))
            vs[cand] = v
            if not flips(v):
                lo = cand
                break
            hi = cand
        if lo is None:
            out.update(lam_star=hi, bracket=[0.0, hi], note='flips at the lowest value tested', grid2={str(k): v for k, v in vs.items()})
            return A.save_row(job, out)
    else:
        lo = lams[first - 1]
    evals = {}
    while hi / lo > ratio * (1 + 1e-12):
        mid = (lo * hi) ** 0.5
        v = vstar_of(run_one(base, mid))
        evals[str(mid)] = v
        if flips(v):
            hi = mid
        else:
            lo = mid
    out.update(lam_star=hi, bracket=[lo, hi], evals=evals, grid2={str(k): v for k, v in vs.items()})
    return A.save_row(job, out)


def worker(jobfile, wid):
    jobs = [json.loads(l) for l in open(jobfile) if l.strip()]
    lockd = os.path.join(A.SCR, 'locks')
    os.makedirs(lockd, exist_ok=True)
    for i, job in enumerate(jobs):
        if A.load_row(job) is not None:
            continue
        lock = os.path.join(lockd, '%s_%d' % (os.path.basename(jobfile), i))
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
        except FileExistsError:
            continue
        t0 = time.time()
        try:
            r = run_job(job)
            print('worker %d job %d done %.0fs %s -> %s %s' % (wid, i, time.time() - t0, json.dumps(job, sort_keys=True), r.get('class'), r.get('status')), flush=True)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print('worker %d job %d FAILED %s' % (wid, i, e), flush=True)
            try:
                os.remove(lock)
            except OSError:
                pass


if __name__ == '__main__':
    if sys.argv[1] == 'worker':
        worker(sys.argv[2], int(sys.argv[3]))
