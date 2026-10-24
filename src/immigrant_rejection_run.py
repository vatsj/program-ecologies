"""Driver for the immigrant-rejection experiment (notes/immigrant-rejection.md).

    python3 src/immigrant_rejection_run.py jobs OUT [--stage S ...] [--runs R]   # write a job list (ARM mN run)
    python3 src/immigrant_rejection_run.py one ARM MN RUN                         # run one job in this process
    python3 src/immigrant_rejection_run.py worker JOBFILE                         # claim and run the jobs of the file
    python3 src/immigrant_rejection_run.py batch JOBFILE --workers K              # K worker processes + STALL watchdog

One job at a time per process; no multiprocessing.Pool.  Per-run records go to $IR_SCRATCH/<arm>-m<mN>/r<k>.json
(outside the repository); `immigrant_rejection_report.py` aggregates them into runs/immigrant-rejection.{md,json}.
"""
import argparse, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SCR = os.environ.get('IR_SCRATCH', '/private/tmp/claude-501/-Users-jstav-code-program-ecologies/'
                     'eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/ir/runs')
MNS = (0.01, 0.1, 1.0)
RUNS = 40
# priority order (cut candidates last): the gV / baseline comparison, the strict veto, the freezes, then g0 and gKRw
STAGES = {
    '1': ['B', 'gV'],
    '2': ['gVs'],
    '3': ['FI', 'FP', 'FX', 'FXP', 'FPL'],
    '4': ['gKRw', 'g0'],
}


def mlab(m):
    return '%g' % m


def cell(arm, m):
    return '%s-m%s' % (arm, mlab(m))


def result_path(arm, m, r):
    return os.path.join(SCR, cell(arm, m), 'r%d.json' % r)


def run_one(arm, m, r):
    import immigrant_rejection as IR
    return IR.run_arm(arm, m, r)


def worker(jobfile):
    os.makedirs(os.path.join(SCR, '_claims'), exist_ok=True)
    jobs = [l.split() for l in open(jobfile) if l.strip() and not l.startswith('#')]
    for arm, m, r in jobs:
        m = float(m); r = int(r)
        if os.path.exists(result_path(arm, m, r)):
            continue
        claim = os.path.join(SCR, '_claims', '%s__%d' % (cell(arm, m), r))
        try:
            fd = os.open(claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode()); os.close(fd)
        except FileExistsError:
            continue
        try:
            rec = run_one(arm, m, r)
        except Exception as e:
            print('FAIL', arm, m, r, repr(e), flush=True)
            import traceback; traceback.print_exc()
            continue
        os.makedirs(os.path.dirname(result_path(arm, m, r)), exist_ok=True)
        tmp = result_path(arm, m, r) + '.tmp'
        json.dump(rec, open(tmp, 'w'))
        os.replace(tmp, result_path(arm, m, r))
        print('done', cell(arm, m), r, 'wall %.0f rss %.2fGB' % (rec['wall'], rec['rss_gb']), flush=True)


def batch(jobfile, workers, stall_hours=2.0):
    here = os.path.abspath(__file__)
    procs = []
    os.makedirs(SCR, exist_ok=True)
    logf = open(os.path.join(SCR, 'batch.log'), 'a')
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
    ap.add_argument('--stage', action='append', default=[])
    ap.add_argument('--runs', type=int, default=RUNS)
    a = ap.parse_args()
    if a.cmd == 'one':
        rec = run_one(a.a[0], float(a.a[1]), int(a.a[2]))
        print(json.dumps(rec)[:3000])
    elif a.cmd == 'worker':
        worker(a.a[0])
    elif a.cmd == 'batch':
        sys.exit(batch(a.a[0], a.workers))
    elif a.cmd == 'jobs':
        stages = a.stage or sorted(STAGES)
        lines = []
        for st in stages:
            for arm in STAGES[st]:
                for m in MNS:
                    for r in range(a.runs):
                        lines.append('%s %g %d' % (arm, m, r))
        open(a.a[0], 'w').write('\n'.join(lines) + '\n')
        print(len(lines), 'jobs')


if __name__ == '__main__':
    main()
