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


def resolve_abl(label, arm):
    if label in (None, 'full'):
        return None
    K = len(arm.S.fs)
    kind, rest = label.split(':', 1)
    m = np.zeros((3, K), bool)
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


def run_job(job, verbose=False):
    arm = UB.get_arm(R.CELLS[job['cell']]['arm'])
    remove = resolve_abl(job.get('abl'), arm)
    core = load_core(job.get('core'))
    spec = dict(cell=job['cell'], m=job.get('m', 1), abl=job.get('abl'), start=job.get('start', 'nat'))
    for k in ('pools', 'raw', 'core', 'rule', 'tag'):
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
