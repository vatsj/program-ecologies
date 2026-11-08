"""Driver for series 2a / 2b of queue 75 (spec specs/2026-11-08-length-prior-t.md).

    python3 src/length_prior_t_run.py jobs OUT.txt STAGE [STAGE ...] [--step1 runs/lt-prior.json]
    python3 src/length_prior_t_run.py run JOBFILE OUTDIR [--shard I --of K]       # DAYTONA_CPUS (or --workers) workers
    python3 src/length_prior_t_run.py rows OUTDIR                                  # count rows

A job is `series|spec|N|I|r|long`; one cell (Lambda = 100, mN = 1).  Workers claim jobs by lock files and append one JSON
row per finished job to OUTDIR/rows_<pid>.jsonl, so a stopped run resumes (rows already present are skipped).  Specs: see
length_prior_t.parse_law (`2a:d=..:b=..[:s1][:fm=..][:tm=..]`, `2a:df=..:dt=..:b=..` for independent founder and tail doses,
`2b:<machine>:d=..`).  Stages: 2a, slice1, matched, indep (independent founder / tail copies at c = 64), 2b (needs --step1),
slice2 (needs --delta2 from the 2a result: the delta just above delta*(200, 64, 0)), long (needs --long LISTFILE).
"""
import argparse, glob, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DELTAS = [2e-1, 1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4]
BETAS = [0.0, 0.3, 1.0, 3.0]
NS = [100, 200, 400]
IS = [64, 256]
RUNS = 20
MATCH_PAIRS = [(100, 64), (200, 64), (400, 64), (100, 256), (200, 256)]
COSTW = {100: 1.0, 200: 3.4, 400: 12.0}


def fmt(x):
    return repr(float(x))


def jid(series, spec, N, I, r, long=False):
    return '%s|%s|%d|%d|%d|%d' % (series, spec, N, I, r, int(long))


def cost(job):
    s = job.split('|')
    N, I = int(s[2]), int(s[3])
    return COSTW[N] * (I / 64.0) * (2.0 if s[5] == '1' else 1.0)


def make_jobs(stages, step1=None, delta2=None, longlist=None):
    jobs = []
    for st in stages:
        if st == '2a':
            for N in NS:
                for I in IS:
                    for b in BETAS:
                        for d in DELTAS:
                            for r in range(RUNS):
                                jobs.append(jid('2a', '2a:d=%s:b=%s' % (fmt(d), fmt(b)), N, I, r))
        elif st == 'slice1':
            for d in DELTAS:
                for r in range(RUNS):
                    jobs.append(jid('slice1', '2a:d=%s:b=0.0:s1' % fmt(d), 200, 64, r))
        elif st == 'matched':
            for c in (64, 640):
                for (N, I) in MATCH_PAIRS:
                    d = c / (I * N)
                    for r in range(RUNS):
                        jobs.append(jid('matched', '2a:d=%s:b=0.0' % fmt(d), N, I, r))
        elif st == 'indep':
            for (N, I) in MATCH_PAIRS:
                df = 64.0 / (I * N)            # founder copies I*N*df = 64
                dt = 64.0 / (I * 100.0)        # tail copies I*Lambda*dt = 64 (Lambda = 100)
                for (a, b_) in ((df, 0.0), (0.0, dt), (df, dt)):
                    for r in range(RUNS):
                        jobs.append(jid('indep', '2a:df=%s:dt=%s:b=0.0' % (fmt(a), fmt(b_)), N, I, r))
        elif st == 'slice2':
            for (kind, a, b_) in (('fo', 1.0, 0.0), ('to', 0.0, 1.0)):
                for r in range(RUNS):
                    jobs.append(jid('slice2', '2a:df=%s:dt=%s:b=0.0' % (fmt(delta2 * a), fmt(delta2 * b_)), 200, 64, r))
        elif st == '2b':
            for mach in step1['machines']:
                m = step1[mach]
                rd = m['single'] + m['two']
                for N in (200, 400):
                    for d in DELTAS:
                        rest = 1.0 - d * (1.0 + (m['bully'] + m['exploit']) / rd) - m['junk_f'] - m['junk_r']
                        if rest <= 0:
                            continue        # the measured junk and bully mass leave no room for readers at this delta
                        for r in range(RUNS):
                            jobs.append(jid('2b', '2b:%s:d=%s' % (mach, fmt(d)), N, 64, r))
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


KEEP = ('vshare_ts', 'cons_modal', 'cons_majo', 'cons_modal_240', 'trans', 'tail', 'nmig', 'status', 'stop', 'wall')


def run_job(job, step1, cache_dir):
    import length_prior_t as LP
    series, spec, N, I, r, long = job.split('|')
    N, I, r, long = int(N), int(I), int(r), bool(int(long))
    wf, wt = LP.parse_law(spec, step1)
    rec = LP.run_cell(wf, wt, N, r, I, long=long, cache_dir=cache_dir)
    out = dict(id=job, series=series, spec=spec, N=N, I=I, r=r, long=long)
    for k in KEEP:
        if k in rec:
            out[k] = rec[k]
    sn = rec['snap'][str(120 * N)]
    out['snap120'] = dict(cls_modal=sn['cls_modal'], pair_modal=sn['pair_modal'], npairs_modal=sn['npairs_modal'],
                          cls_majo=sn['cls_majo'], hold=sn['hold'], fair_enc=sn['fair_enc'], surplus=sn['surplus'])
    out['vstar'] = rec['vshare_ts'][120]
    return out


def worker(jobfile, outdir, step1_path, shard, of):
    jobs = [l.strip() for l in open(jobfile) if l.strip()][shard::of]
    step1 = json.load(open(step1_path)) if step1_path else None
    cache = os.environ.get('MT_CACHE', os.path.join(ROOT, 'runs', '_cache'))
    done = load_rows(outdir)
    outf = os.path.join(outdir, 'rows_%d.jsonl' % os.getpid())
    for j in jobs:
        if j in done:
            continue
        import hashlib
        lock = os.path.join(outdir, 'lock_' + hashlib.md5(j.encode()).hexdigest())
        try:
            os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        except FileExistsError:
            continue
        t0 = time.time()
        try:
            row = run_job(j, step1, cache)
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
    a.add_argument('--step1'); a.add_argument('--delta2', type=float); a.add_argument('--long')
    a.add_argument('--max-cost', type=float, default=None); a.add_argument('--part', default=None)
    b = sp.add_parser('run'); b.add_argument('jobfile'); b.add_argument('outdir'); b.add_argument('--step1')
    b.add_argument('--shard', type=int, default=0); b.add_argument('--of', type=int, default=1); b.add_argument('--workers', type=int)
    c = sp.add_parser('rows'); c.add_argument('outdir')
    d = sp.add_parser('worker'); d.add_argument('jobfile'); d.add_argument('outdir'); d.add_argument('step1'); d.add_argument('shard', type=int); d.add_argument('of', type=int)
    ns = ap.parse_args()
    if ns.cmd == 'jobs':
        step1 = json.load(open(ns.step1)) if ns.step1 else None
        longlist = [l.strip() for l in open(ns.long) if l.strip()] if ns.long else None
        jobs = make_jobs(ns.stages, step1, ns.delta2, longlist)
        if ns.part:                                  # i/k : every k-th job from i of the cost-sorted list
            i, k = [int(x) for x in ns.part.split('/')]
            jobs = jobs[i::k]
        open(ns.out, 'w').write('\n'.join(jobs) + '\n')
        print(len(jobs), 'jobs, cost units %.0f' % sum(cost(j) for j in jobs))
    elif ns.cmd == 'rows':
        print(len(load_rows(ns.outdir)))
    elif ns.cmd == 'worker':
        worker(ns.jobfile, ns.outdir, ns.step1 if ns.step1 != '-' else None, ns.shard, ns.of)
    else:
        os.makedirs(ns.outdir, exist_ok=True)
        nw = ns.workers or int(os.environ.get('DAYTONA_CPUS', os.cpu_count() or 1))
        # warm up (table build, numba compilation cached on disk) with one small cell before the pool starts
        import length_prior_t as LP
        cache = os.environ.get('MT_CACHE', os.path.join(ROOT, 'runs', '_cache'))
        wf, wt = LP.parse_law('2a:d=0.03:b=0.0')
        LP.tabs(cache)
        LP.run_cell(wf, wt, 100, 0, 8, cache_dir=cache)
        procs = []
        for w in range(nw):
            procs.append(subprocess.Popen([sys.executable, os.path.abspath(__file__), 'worker', ns.jobfile, ns.outdir,
                                           ns.step1 or '-', str(ns.shard), str(ns.of)]))
        for p in procs:
            p.wait()
        sys.exit(1 if any(p.returncode for p in procs) else 0)


if __name__ == '__main__':
    main()
