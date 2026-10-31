"""Job layer of the unequal-basin experiment: labels -> ablation masks and cores, lock-file workers.

    python3 src/unequal_basin_jobs.py worker JOBFILE WID      # JOBFILE: one JSON job per line
Job fields: kind 'run'|'scan', cell, m, start, abl, rule, core, pools, raw, tag.
abl labels: 'fam:A+B' (syntactic families, S3-closed), 'orb:s.x,s.x' (explicit slot.program pairs, S3 orbits removed).
"""
import os, sys, json, time, hashlib
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import unequal_basin as UB
import unequal_basin_core as UC
import unequal_basin_run as R


def resolve_abl(label, arm, cell=None):
    if label in (None, 'full'):
        return None
    K = len(arm.S.fs)
    kind, rest = label.split(':', 1)
    m = np.zeros((3, K), bool)
    if kind == 'rand':
        # rand:SEED:MASS[:EXCLUDE_FAMILY]: conditional programs (slot-0 frame, S3 orbits) drawn at random until the mean over
        # slots of the removed start-law donor mass reaches MASS
        parts = rest.split(':')
        seed, mass = int(parts[0]), float(parts[1])
        rng = np.random.default_rng(seed)
        q0 = np.zeros((3, K))
        for s in range(3):
            q0[s] = np.bincount(cell.trip[:, s], weights=cell.w, minlength=K)
        cond = np.array([x for x in range(K) if not cell.isc[x]])
        excl = R.family_mask(arm, parts[2]) if len(parts) > 2 else np.zeros((3, K), bool)
        order = rng.permutation(cond)
        tot = 0.0
        for x in order:
            if excl[0, x]:
                continue
            m[0, x] = True
            om = R.orbit_mask(arm, m)
            tot = float(np.mean([q0[s][om[s]].sum() for s in range(3)]))
            if tot >= mass:
                break
        return R.orbit_mask(arm, m)
    if kind == 'fam':
        for nm in rest.split('+'):
            m |= R.family_mask(arm, nm)
    elif kind == 'orb':
        for tok in rest.split(','):
            s, x = tok.split('.')
            m[int(s), int(x)] = True
    else:
        raise ValueError(label)
    return R.orbit_mask(arm, m)


def load_core(label):
    if not label:
        return None
    z = np.load(os.path.join(R.ABLD, 'core_%s.npz' % label))
    return [set(int(v) for v in z['c%d' % s]) for s in range(3)]


def save_core(label, core):
    np.savez(os.path.join(R.ABLD, 'core_%s.npz' % label), **{'c%d' % s: np.array(sorted(core[s]), np.int64) for s in range(3)})


def auto_core(job, remove, base='pilot_L', qmin=1e-7, cap=100):
    """core for an ablated object: the base core minus the removed programs, plus the conditional donors (q >= qmin) at the endpoints
    of the m = 1 runs of the ablated object from the natural start and the U tilt 0.9 (everything that can carry anything in the
    ablated world), S3-closed.  Cached by label."""
    import hashlib
    lab = 'auto_%s_%s_%s' % (job['cell'], hashlib.md5(json.dumps([job.get('abl'), job.get('rule'), job.get('keep'), job.get('pools')], default=str).encode()).hexdigest()[:8], base)
    path = os.path.join(R.ABLD, 'core_%s.npz' % lab)
    if os.path.exists(path):
        return lab
    arm = UB.get_arm(R.CELLS[job['cell']]['arm'])
    core = load_core(base)
    if remove is not None:
        core = [set(v for v in core[s] if not remove[s][v]) for s in range(3)]
    cand = {}
    for st in ('nat', 'u:0.9'):
        spec = dict(cell=job['cell'], m=1, abl=job.get('abl'), start=st)
        for k in ('pools', 'rule', 'tag', 'keep'):
            if job.get(k) is not None:
                spec[k] = job[k]
        spec['autocore'] = True
        c, obj, xn, dropped = R.build_obj_start(spec, remove, job.get('rule', 'reassign'))
        x0, _ = R.make_start(obj, xn, st)
        if x0 is None:
            continue
        recs, xe, status, kept = UB.run_ode(obj, x0, 1e5, sym=True, early=True)
        q = obj.marg(xe)
        for y in np.nonzero(q[0] >= qmin)[0]:
            if not obj.isc[y]:
                cand[int(y)] = max(cand.get(int(y), 0.0), float(q[0, y]))
    import unequal_basin_cores as C
    for y, qq in sorted(cand.items(), key=lambda kv: -kv[1]):
        trial = [set(c) for c in core]
        trial[0].add(y)
        trial = C.close(arm, trial)
        if len(trial[0]) > cap:
            break
        core = trial
    core = C.close(arm, core)
    save_core(lab, core)
    return lab


def run_job(job, verbose=False):
    arm = UB.get_arm(R.CELLS[job['cell']]['arm'])
    remove = resolve_abl(job.get('abl'), arm, R.cell_of(job['cell'], tuple(job.get('pools') or (0, 1, 2)), not job.get('raw', False)))
    if job.get('core') == 'auto':
        job = dict(job, core=auto_core(job, remove))
    core = load_core(job.get('core'))
    spec = dict(cell=job['cell'], m=job.get('m', 1), abl=job.get('abl'), start=job.get('start', 'nat'))
    for k in ('pools', 'raw', 'core', 'rule', 'tag', 'keep'):
        if job.get(k) is not None:
            spec[k] = job[k]
    rule = job.get('rule', 'reassign')
    if job['kind'] == 'run':
        return R.run_one(spec, remove, rule, core, verbose=verbose)
    return R.scan_ustar(spec, remove, rule, core, verbose=verbose)


def worker(jobfile, wid):
    jobs = [json.loads(l) for l in open(jobfile) if l.strip()]
    lockd = os.path.join(UC.SCR, 'locks')
    os.makedirs(lockd, exist_ok=True)
    for i, job in enumerate(jobs):
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
            if job['kind'] == 'scan':
                out = os.path.join(R.ROWS, 'scan_%s.json' % hashlib.md5(json.dumps(job, sort_keys=True).encode()).hexdigest()[:10])
                json.dump(dict(job=job, result=r), open(out, 'w'), default=str)
            print('worker %d job %d done %.0fs %s' % (wid, i, time.time() - t0, json.dumps(job)), flush=True)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print('worker %d job %d FAILED %s' % (wid, i, e), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'worker':
        worker(sys.argv[2], int(sys.argv[3]))
