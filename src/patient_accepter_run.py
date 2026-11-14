"""Driver for step 2 of queue 78 (spec specs/2026-11-14-patient-accepters.md); a copy of queue 76's bully_resist_run.py with this queue's
stages (nothing existing is edited).

    python3 src/patient_accepter_run.py jobs OUT.txt STAGE [STAGE ...] [--step2 runs/patient_accepter/step1_law.json] [--part i/k]
    python3 src/patient_accepter_run.py run JOBFILE OUTDIR [--step2 ..] [--shard I --of K]      # DAYTONA_CPUS workers
    python3 src/patient_accepter_run.py rows OUTDIR

A job is `series|spec|N|I|r|long`; one cell (Lambda = 100, mN = 1).  Workers claim jobs by lock files and append one JSON row per
finished job to OUTDIR/rows_<pid>.jsonl, so a stopped run resumes.  Stages: main (arms FR, FOR, FC, R, FRs; gamma = 1; beta 1, 3; the five
delta; N = 100, 200, 400; I = 64), gam (FR, FOR, FC at gamma 0.3 and 3, N = 200), i256 (FR at N = 200, I = 256), b0 (FR at beta = 0, N = 200),
seed (seeded starts, N = 200, delta = 0.03, beta = 3, arms F, FR, FOR, FC, R, to 240N), v1 (F arm against queue 75's stored rows), lps
(length-prior-shaped, needs --step2), long (continuations from --long LISTFILE).  The F control of the grid is queue 75's stored rows.
"""
import argparse, glob, json, os, sys, time, hashlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DELTAS = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3]
BETAS = [1.0, 3.0]
NS = [100, 200, 400]
RUNS = 20
COSTW = {100: 1.0, 200: 3.4, 400: 12.0}
SEEDW = 1.5


def fmt(x):
    return repr(float(x))


def jid(series, spec, N, I, r, long=False):
    return '%s|%s|%d|%d|%d|%d' % (series, spec, N, I, r, int(long))


def cost(job):
    s = job.split('|')
    N, I = int(s[2]), int(s[3])
    return COSTW[N] * (I / 64.0) * (2.0 if s[5] == '1' else 1.0) * (SEEDW if 'seed=' in s[1] else 1.0)


def pa(arm, d, b, g=None, extra=''):
    return 'pa:arm=%s:d=%s:b=%s%s%s' % (arm, fmt(d), fmt(b), (':g=%s' % fmt(g)) if g is not None else '', extra)


MAIN_ARMS = ('FR', 'FOR', 'FC', 'R', 'FRs')
GAMMA_ARMS = ('FR', 'FOR', 'FC')


def make_jobs(stages, step2=None, longlist=None):
    jobs = []
    for st in stages:
        if st == 'main':
            for arm in MAIN_ARMS:
                for N in NS:
                    for b in BETAS:
                        for d in DELTAS:
                            for r in range(RUNS):
                                jobs.append(jid('main', pa(arm, d, b, 1.0 if arm in GAMMA_ARMS else None), N, 64, r))
        elif st == 'gam':
            for arm in GAMMA_ARMS:
                for g in (0.3, 3.0):
                    for b in BETAS:
                        for d in DELTAS:
                            for r in range(RUNS):
                                jobs.append(jid('gam', pa(arm, d, b, g), 200, 64, r))
        elif st == 'i256':
            for b in BETAS:
                for d in DELTAS:
                    for r in range(RUNS):
                        jobs.append(jid('i256', pa('FR', d, b, 1.0), 200, 256, r))
        elif st == 'b0':
            for d in DELTAS:
                for r in range(RUNS):
                    jobs.append(jid('b0', pa('FR', d, 0.0, 1.0), 200, 64, r))
        elif st == 'seed':
            for arm in ('F', 'FR', 'FOR', 'FC', 'R'):
                for kind in ('unequal', 'fair'):
                    for r in range(RUNS):
                        jobs.append(jid('seed', pa(arm, 0.03, 3.0, 1.0 if arm in GAMMA_ARMS else None, ':seed=%s' % kind), 200, 64, r, True))
        elif st == 'v1':
            for N in (100, 200):
                for b in BETAS:
                    for d in (1e-2, 1e-1):
                        for r in range(5):
                            jobs.append(jid('v1', pa('F', d, b), N, 64, r))
        elif st == 'lps':
            from patient_accepter_dyn import law_lp
            for mach in step2['machines']:
                for alloc in ('const', 'junk'):
                    for N in (200, 400):
                        for d in [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4]:
                            try:
                                law_lp(step2, mach, alloc, d)
                            except AssertionError:
                                continue
                            for r in range(RUNS):
                                jobs.append(jid('lps', 'lp:%s:%s:d=%s' % (mach, alloc, fmt(d)), N, 64, r))
        elif st == 'long':
            for j in longlist:
                s = j.split('|')
                jobs.append(jid(s[0], s[1], int(s[2]), int(s[3]), int(s[4]), True))
        else:
            raise ValueError(st)
    jobs.sort(key=lambda j: -cost(j))
    return jobs


def load_rows(outdir):
    rows = {}
    for f in glob.glob(os.path.join(outdir, 'rows_*.jsonl')):
        for line in open(f):
            line = line.strip()
            if line:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                rows[r['id']] = r
    return rows


def worker(jobfile, outdir, step2_path, shard, of):
    import patient_accepter_dyn as D
    jobs = [l.strip() for l in open(jobfile) if l.strip()][shard::of]
    step2 = json.load(open(step2_path)) if step2_path and step2_path != '-' else None
    cache = os.environ.get('MT_CACHE', os.path.join(ROOT, 'runs', '_cache'))
    done = load_rows(outdir)
    outf = os.path.join(outdir, 'rows_%d.jsonl' % os.getpid())
    for j in jobs:
        if j in done:
            continue
        lock = os.path.join(outdir, 'lock_' + hashlib.md5(j.encode()).hexdigest())
        try:
            os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        except FileExistsError:
            continue
        t0 = time.time()
        try:
            row = D.run_job(j, step2, cache)
            row['job_wall'] = round(time.time() - t0, 1)
            with open(outf, 'a') as f:
                f.write(json.dumps(row) + '\n')
            print('done', j, row['job_wall'], flush=True)
        except Exception as e:
            import traceback
            print('FAIL', j, repr(e), flush=True); traceback.print_exc()
            try:
                os.remove(lock)
            except OSError:
                pass


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    a = sp.add_parser('jobs'); a.add_argument('out'); a.add_argument('stages', nargs='+')
    a.add_argument('--step2'); a.add_argument('--long'); a.add_argument('--part', default=None)
    b = sp.add_parser('run'); b.add_argument('jobfile'); b.add_argument('outdir'); b.add_argument('--step2')
    b.add_argument('--shard', type=int, default=0); b.add_argument('--of', type=int, default=1); b.add_argument('--workers', type=int)
    c = sp.add_parser('rows'); c.add_argument('outdir')
    d = sp.add_parser('worker'); d.add_argument('jobfile'); d.add_argument('outdir'); d.add_argument('step2'); d.add_argument('shard', type=int); d.add_argument('of', type=int)
    ns = ap.parse_args()
    if ns.cmd == 'jobs':
        step2 = json.load(open(ns.step2)) if ns.step2 else None
        longlist = [l.strip() for l in open(ns.long) if l.strip()] if ns.long else None
        jobs = make_jobs(ns.stages, step2, longlist)
        if ns.part:
            i, k = [int(x) for x in ns.part.split('/')]
            jobs = jobs[i::k]
        open(ns.out, 'w').write('\n'.join(jobs) + '\n')
        print(len(jobs), 'jobs, cost units %.0f' % sum(cost(j) for j in jobs))
    elif ns.cmd == 'rows':
        print(len(load_rows(ns.outdir)))
    elif ns.cmd == 'worker':
        worker(ns.jobfile, ns.outdir, ns.step2, ns.shard, ns.of)
    else:
        os.makedirs(ns.outdir, exist_ok=True)
        nw = ns.workers or int(os.environ.get('DAYTONA_CPUS', os.cpu_count() or 1))
        import patient_accepter_dyn as D
        cache = os.environ.get('MT_CACHE', os.path.join(ROOT, 'runs', '_cache'))
        D.tabs(cache)
        D.run_cell('pa:arm=FR:d=0.03:b=0.0:seed=unequal', 100, 0, 8, cache_dir=cache)          # warm up (numba compilation cached on disk)
        procs = []
        for w in range(nw):
            procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), 'worker', ns.jobfile, ns.outdir,
                                           ns.step2 or '-', str(ns.shard), str(ns.of)]))
        for p in procs:
            p.wait()
        sys.exit(1 if any(p.returncode for p in procs) else 0)


if __name__ == '__main__':
    main()
