"""Driver for step 2 of queue 79 (spec specs/2026-11-15-certified-offers.md); queue 78's patient_accepter_run.py with this queue's stages
(nothing existing is edited).

    python3 src/certified_offers_run.py jobs OUT.txt STAGE [STAGE ...] [--part i/k]
    python3 src/certified_offers_run.py run JOBFILE OUTDIR                 # DAYTONA_CPUS workers
    python3 src/certified_offers_run.py rows OUTDIR

A job is `series|spec|N|I|r|long`.  Workers claim jobs by lock files and append one JSON row per finished job to OUTDIR/rows_<pid>.jsonl.
Stages (I = 64, phi = 1/2 unless stated; 20 runs; beta in {0, 1, 3}; the five delta):
  main   Fc, FcOc, FcOcRc, FcRc, mix at N = 100, 200, 400
  rcs    FcOcRcs at N = 200
  phi    phi in {0, 1} at N = 200, beta in {1, 3} (beta = 0 has no bullies), arms Fc, FcOc, FcOcRc, FcRc, FcOcRcs, mix
  ctl    FcOcC3 (beta 0, 1, 3) and Fcs (Fc*, beta 0, 3) at N = 200
  i256   FcOcRc at N = 200, I = 256
  pc     PcOcRc at N = 200
  seed   seeded starts (N = 200, delta = 0.03, beta = 3, to 240N): kinds unequal, unequalBc (phi 1/2 and 1), fair, fairC; arms Fc, FcOcRc,
         FcRc, FcOcRcs; and FR for the two new kinds (unequalBc, fairC; FR's tail has simulating bullies only)
  v1     F and FR cells to compare with queue 75's and queue 78's stored rows
"""
import argparse, glob, json, os, sys, time, hashlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DELTAS = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3]
BETAS = [0.0, 1.0, 3.0]
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


def co(arm, d, b, ph=0.5, extra=''):
    return 'co:arm=%s:d=%s:b=%s:ph=%s%s' % (arm, fmt(d), fmt(b), fmt(ph), extra)


MAIN_ARMS = ('Fc', 'FcOc', 'FcOcRc', 'FcRc', 'mix')
PHI_ARMS = ('Fc', 'FcOc', 'FcOcRc', 'FcRc', 'FcOcRcs', 'mix')
SEED_ARMS = ('Fc', 'FcOcRc', 'FcRc', 'FcOcRcs')


def make_jobs(stages):
    jobs = []
    for st in stages:
        if st == 'main':
            for arm in MAIN_ARMS:
                for N in NS:
                    for b in BETAS:
                        for d in DELTAS:
                            for r in range(RUNS):
                                jobs.append(jid('main', co(arm, d, b), N, 64, r))
        elif st == 'rcs':
            for b in BETAS:
                for d in DELTAS:
                    for r in range(RUNS):
                        jobs.append(jid('rcs', co('FcOcRcs', d, b), 200, 64, r))
        elif st == 'phi':
            for arm in PHI_ARMS:
                for ph in (0.0, 1.0):
                    for b in (1.0, 3.0):
                        for d in DELTAS:
                            for r in range(RUNS):
                                jobs.append(jid('phi', co(arm, d, b, ph), 200, 64, r))
        elif st == 'ctl':
            for arm, bs in (('FcOcC3', BETAS), ('Fcs', (0.0, 3.0))):
                for b in bs:
                    for d in DELTAS:
                        for r in range(RUNS):
                            jobs.append(jid('ctl', co(arm, d, b), 200, 64, r))
        elif st == 'i256':
            for b in BETAS:
                for d in DELTAS:
                    for r in range(RUNS):
                        jobs.append(jid('i256', co('FcOcRc', d, b), 200, 256, r))
        elif st == 'pc':
            for b in BETAS:
                for d in DELTAS:
                    for r in range(RUNS):
                        jobs.append(jid('pc', co('PcOcRc', d, b), 200, 64, r))
        elif st == 'seed':
            for arm in SEED_ARMS:
                for kind, ph in (('unequal', 0.5), ('unequalBc', 0.5), ('unequalBc', 1.0), ('fair', 0.5), ('fairC', 0.5)):
                    for r in range(RUNS):
                        jobs.append(jid('seed', co(arm, 0.03, 3.0, ph, ':seed=%s' % kind), 200, 64, r, True))
            for kind in ('unequalBc', 'fairC'):
                for r in range(RUNS):
                    jobs.append(jid('seed', co('FR', 0.03, 3.0, 0.0, ':seed=%s' % kind), 200, 64, r, True))
        elif st == 'v1':
            for arm in ('F', 'FR'):
                for (N, b, d) in ((200, 1.0, 0.01), (200, 1.0, 0.1), (200, 3.0, 0.01), (200, 3.0, 0.1), (100, 3.0, 0.1)):
                    for r in range(2):
                        jobs.append(jid('v1', co(arm, d, b, 0.0), N, 64, r))
        elif st == 'pilot':
            for N in (100, 200):
                jobs.append(jid('pilot', co('FcOcRc', 0.03, 3.0), N, 64, 95))
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


def worker(jobfile, outdir, shard, of):
    import certified_offers_dyn as D
    jobs = [l.strip() for l in open(jobfile) if l.strip()][shard::of]
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
            row = D.run_job(j, cache)
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
    a = sp.add_parser('jobs'); a.add_argument('out'); a.add_argument('stages', nargs='+'); a.add_argument('--part', default=None)
    b = sp.add_parser('run'); b.add_argument('jobfile'); b.add_argument('outdir'); b.add_argument('--workers', type=int)
    c = sp.add_parser('rows'); c.add_argument('outdir')
    d = sp.add_parser('worker'); d.add_argument('jobfile'); d.add_argument('outdir'); d.add_argument('shard', type=int); d.add_argument('of', type=int)
    ns = ap.parse_args()
    if ns.cmd == 'jobs':
        jobs = make_jobs(ns.stages)
        if ns.part:
            i, k = [int(x) for x in ns.part.split('/')]
            jobs = jobs[i::k]
        open(ns.out, 'w').write('\n'.join(jobs) + '\n')
        print(len(jobs), 'jobs, cost units %.0f' % sum(cost(j) for j in jobs))
    elif ns.cmd == 'rows':
        print(len(load_rows(ns.outdir)))
    elif ns.cmd == 'worker':
        worker(ns.jobfile, ns.outdir, ns.shard, ns.of)
    else:
        os.makedirs(ns.outdir, exist_ok=True)
        nw = ns.workers or int(os.environ.get('DAYTONA_CPUS', os.cpu_count() or 1))
        import certified_offers_dyn as D
        cache = os.environ.get('MT_CACHE', os.path.join(ROOT, 'runs', '_cache'))
        D.tabs(cache)
        D.run_cell(co('FcOcRc', 0.03, 0.0, 0.5, ':seed=unequal'), 100, 0, 8, cache_dir=cache, pace=True)   # warm up (numba cache)
        procs = []
        for w in range(nw):
            procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), 'worker', ns.jobfile, ns.outdir, '0', '1']))
        for p in procs:
            p.wait()
        sys.exit(1 if any(p.returncode for p in procs) else 0)


if __name__ == '__main__':
    main()
