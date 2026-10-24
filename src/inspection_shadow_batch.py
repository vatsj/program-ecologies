"""Job queue for the inspection-shadow experiment: runs the jobs of a job file as separate processes (one job per process, no pool), at
most 3 at a time (2 while the exploration audit's processes are alive), gated by estimated peak memory against available memory.
Jobs whose output file already exists are skipped (restart-safe).  Exits when the queue is empty and the last job has finished;
every state change is appended to the log.

    python3 src/inspection_shadow_batch.py JOBFILE LOG

JOBFILE lines:   priority | est_gb | output_file_name | arguments of inspection_shadow_run.py      (lower priority number first)
"""
import os, sys, time, subprocess
import psutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.environ.get('INSPECTION_SHADOW_OUT', os.path.join(ROOT, 'runs', 'inspection_shadow'))
SAFETY_GB = 1.8


def audit_alive():
    for p in psutil.process_iter(['cmdline']):
        try:
            cl = ' '.join(p.info['cmdline'] or [])
        except Exception:
            continue
        if 'exploration_audit_run' in cl:
            return True
    return False


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

    def say(msg):
        log.write('%s %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)); log.flush()

    running = []
    pending = [j for j in jobs if not os.path.exists(os.path.join(OUT, j['out']))]
    say('queue: %d jobs, %d pending (%d already done)' % (len(jobs), len(pending), len(jobs) - len(pending)))
    while pending or running:
        for r in list(running):
            rc = r['proc'].poll()
            if rc is not None:
                say('finished rc=%d %s (%.0fs)' % (rc, ' '.join(r['job']['args']), time.time() - r['t0']))
                running.remove(r)
        cap = 2 if audit_alive() else 3
        if pending and len(running) < cap:
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
                    lf = open(os.path.join(os.path.dirname(logfile), 'job_' + j['out'].replace('/', '_') + '.log'), 'w')
                    proc = subprocess.Popen([sys.executable, os.path.join(HERE, 'inspection_shadow_run.py')] + j['args'], stdout=lf, stderr=subprocess.STDOUT, cwd=ROOT)
                    running.append(dict(proc=proc, job=j, t0=time.time()))
                    pending.remove(j)
                    say('started pid %d (est %.1f GB, avail %.1f GB, cap %d) %s' % (proc.pid, j['gb'], avail, cap, ' '.join(j['args'])))
                    break
        time.sleep(15)
    say('batch complete')


if __name__ == '__main__':
    main()
