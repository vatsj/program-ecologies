"""Job queue for the zero-tolerance experiment: runs the jobs of a job file as separate processes (one job per process, no pool), at most 2 at a
time (other subagents' processes are alive), one whole-space chain at a time, gated by estimated peak memory against available memory.  Jobs
whose output file already exists are skipped (restart-safe).  Exits when the queue is empty and the last job has finished, and exits with
"STALL" if no state change has been logged for 2 hours; every state change is appended to the log.

    python3 src/zero_tolerance_batch.py JOBFILE LOG

JOBFILE lines:   priority | est_gb | output_file_name | arguments of zero_tolerance_run.py      (lower priority number first)
"""
import os, sys, time, subprocess
import psutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.environ.get('ZERO_TOLERANCE_OUT', os.path.join(ROOT, 'runs', 'zero_tolerance'))
SAFETY_GB = 1.8
CAP = int(os.environ.get('ZT_CAP', '2'))
STALL_S = 7200


def main():
    jobfile, logfile = sys.argv[1], sys.argv[2]
    jobs = []
    for line in open(jobfile):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        pr, gb, outn, args = [x.strip() for x in line.split('|')]
        jobs.append(dict(pr=float(pr), gb=float(gb), out=outn, args=args.split()))
    jobs.sort(key=lambda j: j['pr'])
    log = open(logfile, 'a')
    last_change = [time.time()]

    def say(msg):
        log.write('%s %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)); log.flush()
        last_change[0] = time.time()

    running = []
    pending = [j for j in jobs if not os.path.exists(os.path.join(OUT, j['out']))]
    say('queue: %d jobs, %d pending (%d already done)' % (len(jobs), len(pending), len(jobs) - len(pending)))
    while pending or running:
        for r in list(running):
            rc = r['proc'].poll()
            if rc is not None:
                say('finished rc=%d %s (%.0fs)' % (rc, ' '.join(r['job']['args']), time.time() - r['t0']))
                running.remove(r)
        newest = max([last_change[0]] + [os.path.getmtime(r['log']) for r in running if os.path.exists(r['log'])])
        if time.time() - newest > STALL_S:
            say('STALL: no state change for %d s; running: %s' % (STALL_S, [' '.join(r['job']['args']) for r in running]))
            print('STALL')
            sys.exit(2)
        if pending and len(running) < CAP:
            avail = psutil.virtual_memory().available / 1e9
            reserved = 0.0
            for r in running:       # memory the running jobs still have to take (estimate minus current RSS)
                try:
                    cur = psutil.Process(r['proc'].pid).memory_info().rss / 1e9
                except Exception:
                    cur = 0.0
                reserved += max(0.0, r['job']['gb'] - cur)
            heavy_running = sum(1 for r in running if r['job']['gb'] > 2.0)
            for j in pending:
                if j['gb'] > 2.0 and heavy_running >= 1:
                    continue                      # one whole-space chain at a time
                if j['gb'] + reserved + SAFETY_GB <= avail:
                    lpath = os.path.join(os.path.dirname(logfile), 'job_' + j['out'].replace('/', '_') + '.log')
                    lf = open(lpath, 'w')
                    proc = subprocess.Popen([sys.executable, os.path.join(HERE, 'zero_tolerance_run.py')] + j['args'], stdout=lf, stderr=subprocess.STDOUT, cwd=ROOT)
                    running.append(dict(proc=proc, job=j, t0=time.time(), log=lpath))
                    pending.remove(j)
                    say('started pid %d (est %.1f GB, avail %.1f GB, cap %d) %s' % (proc.pid, j['gb'], avail, CAP, ' '.join(j['args'])))
                    break
        time.sleep(15)
    say('batch complete')
    print('batch complete')


if __name__ == '__main__':
    main()
