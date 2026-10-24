"""Driver for the migration-window experiment (notes/migration-window.md).

    python3 src/migration_window_run.py jobs [--set NAME ...]       # write the job list for the named job sets
    python3 src/migration_window_run.py one CELL RUN                # run one job in this process, print its record
    python3 src/migration_window_run.py worker JOBFILE              # claim and run jobs of the file one at a time
    python3 src/migration_window_run.py batch JOBFILE --workers K   # start K worker processes, wait, STALL watchdog

One job per process at a time; no multiprocessing.Pool.  Per-run records go to $MW_SCRATCH/<cell>/r<k>.json (outside the
repository); `migration_window_report.py` aggregates them into runs/migration-window.{md,json} and runs/migration_window/.
"""
import argparse, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SCR = os.environ.get('MW_SCRATCH', '/private/tmp/claude-501/-Users-jstav-code-program-ecologies/'
                     'eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/mw')
MNS = (0, 0.003, 0.01, 0.03, 0.1, 0.3, 1)
H = 20000


def mlab(m):
    return ('%g' % m)


def _base(N):
    return 'L1' if N == 100 else 'L1-N%d' % N


CELLS = {}


def _add(name, **kw):
    kw.setdefault('H', H)
    CELLS[name] = kw


def build_cells():
    for g in ('base', 'gKR', 'gV'):
        for N, runs in ((100, 40), (200, 20)):
            for m in MNS:
                _add('M-%s-N%d-m%s' % (g, N, mlab(m)), guard=g, N=N, mN=m, base=_base(N), sizes=[64], runs=runs,
                     kind='M')
    # components: 16-island components, nested prefixes C = 1, 2, 4, 8
    for g in ('base', 'gKR'):
        for N, runs in ((100, 40), (200, 20)):
            for m in (0.1, 1):
                _add('C16-%s-N%d-m%s' % (g, N, mlab(m)), guard=g, N=N, mN=m, base=_base(N), sizes=[16] * 8,
                     runs=runs, kind='C', prefixes=[1, 2, 4, 8])
    # size panel: C = 4 components of 4 or 64 islands (16 is the C = 4 row of the 16-island panel)
    for g in ('base', 'gKR'):
        for sz in (4, 64):
            for m in (0.1, 1):
                _add('Z%d-%s-N100-m%s' % (sz, g, mlab(m)), guard=g, N=100, mN=m, base='L1', sizes=[sz] * 4,
                     runs=40 if sz == 4 else 20, kind='Z')
    # re-verification of the stored cells (H = 10,000, the stored horizon): the same founders and seeds
    for g in ('base', 'gKR', 'gV'):
        _add('VER-%s-N100-m1' % g, guard=g, N=100, mN=1, base='L1', sizes=[64], runs=40, kind='V', H=10000)
    # controls (I = 60 islands, one component)
    for st in ('bal', 'waste'):
        for m in (0.01, 0.1, 1):
            _add('K%s-base-N100-m%s' % (st, mlab(m)), guard='base', N=100, mN=m, base='L1', sizes=[60], runs=20,
                 kind='K', start=st)
        for g in ('gKR', 'gV'):
            for m in (0.1, 1):
                _add('K%s-%s-N100-m%s' % (st, g, mlab(m)), guard=g, N=100, mN=m, base='L1', sizes=[60], runs=20,
                     kind='K', start=st)


build_cells()


def run_one(cell, r):
    import migration_window as MW
    p = CELLS[cell]
    rec = MW.run_job(p, r, prefixes=p.get('prefixes'))
    rec.update(cell=cell)
    return rec


def result_path(cell, r):
    return os.path.join(SCR, cell, 'r%d.json' % r)


def worker(jobfile):
    os.makedirs(os.path.join(SCR, '_claims'), exist_ok=True)
    jobs = [l.split() for l in open(jobfile) if l.strip() and not l.startswith('#')]
    for cell, r in jobs:
        r = int(r)
        if os.path.exists(result_path(cell, r)):
            continue
        claim = os.path.join(SCR, '_claims', '%s__%d' % (cell, r))
        try:
            fd = os.open(claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode()); os.close(fd)
        except FileExistsError:
            continue
        try:
            rec = run_one(cell, r)
        except Exception as e:                                   # leave the claim so a rerun can see it, report
            print('FAIL', cell, r, repr(e), flush=True)
            import traceback; traceback.print_exc()
            continue
        os.makedirs(os.path.dirname(result_path(cell, r)), exist_ok=True)
        tmp = result_path(cell, r) + '.tmp'
        json.dump(rec, open(tmp, 'w'))
        os.replace(tmp, result_path(cell, r))
        print('done', cell, r, 'wall %.0f rss %.2fGB' % (rec['wall'], rec['rss_mb'] / 1e3), flush=True)


def batch(jobfile, workers, stall_hours=2.0, log=None):
    here = os.path.abspath(__file__)
    procs = []
    logf = open(log or os.path.join(SCR, 'batch.log'), 'a')
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('a', nargs='*')
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--prefix', default='')
    ap.add_argument('--runs', type=int, default=0)
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    if a.cmd == 'one':
        rec = run_one(a.a[0], int(a.a[1]))
        print(json.dumps(rec)[:3000])
    elif a.cmd == 'worker':
        worker(a.a[0])
    elif a.cmd == 'batch':
        sys.exit(batch(a.a[0], a.workers))
    elif a.cmd == 'jobs':
        names = [n for n in CELLS if n.startswith(a.prefix)]
        lines = []
        for n in names:
            nr = a.runs or CELLS[n]['runs']
            for r in range(nr):
                lines.append('%s %d' % (n, r))
        open(a.out, 'w').write('\n'.join(lines) + '\n')
        print(len(lines), 'jobs')
    elif a.cmd == 'list':
        for n, p in CELLS.items():
            print(n, p['runs'])


if __name__ == '__main__':
    main()
