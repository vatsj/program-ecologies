"""Driver for the majority-division experiment (spec specs/2026-11-07-majority-current-object.md).

    python3 src/majority_tail_run.py jobs OUT.txt [--stage S ...]   # write the job list
    python3 src/majority_tail_run.py shard JOBFILE I K OUTDIR       # run jobs I, I+K, I+2K, ... with DAYTONA_CPUS workers
    python3 src/majority_tail_run.py one JOB OUTDIR                  # run one job in this process

A job is  arm:variant:N:r  (all cells of the (arm, variant) at that N and founders r; one universe and joint table, one
founder draw, every (Lambda, mN) cell).  Rows go to OUTDIR/<job>.jsonl.gz, one JSON object per cell.
"""
import argparse, gzip, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RUNS = {100: 40, 200: 40, 400: 20}
LONG_RUNS = 10


def cells_of(arm, variant):
    """(Lambda, mN) cells of the job family."""
    if variant == 'main':
        return [(lam, mN) for lam in (0, 10, 100) for mN in (0, 0.1, 1)]
    if variant == 'D1':
        return [(100, 0.1), (100, 1)]
    if variant in ('D2', 'D3') or variant.startswith('D4'):
        return [(100, 1)]
    if variant == 'T0':
        return [(0, 1), (100, 1)]
    raise ValueError(variant)


def make_jobs(stages):
    jobs = []
    def add(arm, variant, Ns, runs=None):
        for N in Ns:
            nr = (runs or RUNS)[N] if not isinstance(runs, int) else runs
            for r in range(nr):
                jobs.append('%s:%s:%d:%d' % (arm, variant, N, r))
    for st in stages:
        if st == 'main':
            add('M', 'main', (100, 200, 400)); add('T', 'main', (100, 200, 400))
        elif st == 'L':
            add('L', 'main', (100, 200))
        elif st == 'D':
            for v in ('D1', 'D2', 'D3'):
                add('M', v, (100, 200))
            for d in range(3):
                add('M', 'D4:%d' % d, (100, 200), runs=20)
        elif st == 'T0':
            add('T', 'T0', (100, 200, 400))
        else:
            raise ValueError(st)
    return jobs


def run_job(job, outdir, cache_dir=None):
    import majority_tail as MT
    arm, variant, N, r = job.split(':', 3)[0], None, None, None
    parts = job.split(':')
    arm = parts[0]
    if parts[1] == 'D4':
        variant = 'D4:' + parts[2]; N = int(parts[3]); r = int(parts[4])
    else:
        variant = parts[1]; N = int(parts[2]); r = int(parts[3])
    path = os.path.join(outdir, job.replace(':', '_') + '.jsonl.gz')
    if os.path.exists(path):
        return path
    t0 = time.time()
    prep = MT.prepare(arm, variant, N, r, cache_dir=cache_dir)
    t_prep = time.time() - t0
    geo = prep['geo']
    names, fam = MT.family_table(arm)
    rows = []
    for lam, mN in cells_of(arm, variant):
        long = (variant == 'main' and lam == 100 and mN == 1 and r < LONG_RUNS)
        H = geo['Hlong'] if long else geo['H']
        snaps = list(geo['snaps']) + ([240 * N] if long else [])
        t1 = time.time()
        res = MT.run_kernel(prep, lam, mN, H, snaps)
        rec = MT.summarize(prep, res, lam, mN, fam, long=long)
        rec['wall'] = round(time.time() - t1, 1); rec['prep_wall'] = round(t_prep, 1)
        rec['fam_names'] = names
        rows.append(rec)
    tmp = path + '.tmp'
    with gzip.open(tmp, 'wt') as f:
        for rec in rows:
            f.write(json.dumps(rec) + '\n')
    os.replace(tmp, path)
    return path


def worker(jobs, outdir, cache_dir):
    """jobs are claimed through lock files in outdir, so several workers can share one list."""
    for j in jobs:
        lock = os.path.join(outdir, j.replace(':', '_') + '.lock')
        try:
            os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        except FileExistsError:
            continue
        try:
            run_job(j, outdir, cache_dir)
            print('done', j, flush=True)
        except Exception as e:                    # keep the shard going; the failure is listed at the end
            import traceback
            print('FAIL', j, repr(e), flush=True); traceback.print_exc()


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    a = sp.add_parser('jobs'); a.add_argument('out'); a.add_argument('--stage', action='append')
    b = sp.add_parser('shard'); b.add_argument('jobfile'); b.add_argument('i', type=int); b.add_argument('k', type=int); b.add_argument('outdir')
    c = sp.add_parser('one'); c.add_argument('job'); c.add_argument('outdir')
    ns = ap.parse_args()
    cache = os.environ.get('MT_CACHE', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'runs', '_cache'))
    os.makedirs(cache, exist_ok=True)
    if ns.cmd == 'jobs':
        jobs = make_jobs(ns.stage or ['main', 'L', 'D', 'T0'])
        jobs.sort(key=lambda j: -int(j.split(':')[3] if j.split(':')[1] == 'D4' else j.split(':')[2]))     # dearest (largest N) first
        open(ns.out, 'w').write('\n'.join(jobs) + '\n')
        print(len(jobs), 'jobs')
    elif ns.cmd == 'one':
        os.makedirs(ns.outdir, exist_ok=True)
        print(run_job(ns.job, ns.outdir, cache))
    else:
        os.makedirs(ns.outdir, exist_ok=True)
        jobs = [l.strip() for l in open(ns.jobfile) if l.strip()][ns.i::ns.k]
        ncpu = int(os.environ.get('DAYTONA_CPUS', os.cpu_count() or 1))
        # one subprocess per worker, each taking every ncpu-th job of this shard
        procs = []
        fn = os.path.join(ns.outdir, '_shard%d.txt' % ns.i)
        open(fn, 'w').write('\n'.join(jobs) + '\n')
        for w in range(ncpu):
            procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), 'worker', fn, '0', '1', ns.outdir]))
        for p in procs:
            p.wait()
        fails = [p.returncode for p in procs if p.returncode]
        sys.exit(1 if fails else 0)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'worker':
        jobs = [l.strip() for l in open(sys.argv[2]) if l.strip()]
        worker(jobs, sys.argv[5], os.environ.get('MT_CACHE', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'runs', '_cache')))
    else:
        main()
