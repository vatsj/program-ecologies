"""Batch driver for the failure-pricing confirmation: one process per job, at most W at a time, jobs in priority order (the
spec's cut order read backwards), skipping jobs whose output exists.  Exits when the batch is done; prints STALL and exits if no
log file has changed for 2 hours.  No multiprocessing.Pool.

    python3 src/failure_pricing_confirm_batch.py run [workers]
    python3 src/failure_pricing_confirm_batch.py hashes pre|post
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'failure_pricing_confirm')
PY = sys.executable
FPC = os.path.join(HERE, 'failure_pricing_confirm.py')


def lt_jobs():
    """(name, command, output files) for the L_T games.  Levels as strings: 'Z@0' zero price, else the A level."""
    jobs = []
    for game, extra in (('rps', '0.2'), ('insp', '0.5')):
        lv = ['Z@0', '0.1', '1', '10', '0.3', '0.03', extra]
        outs = [os.path.join(OUT, '%s_%s_%g_primary.json.gz' % (game, 'Z' if s.startswith('Z') else 'A', float(s.split('@')[-1]))) for s in lv]
        jobs.append(('lt_%s_100_64' % game, [PY, FPC, 'lt', game, '100_64'] + lv, outs))
    for game in ('rps', 'insp'):
        lv = ['Z@0', '0.1']
        outs = [os.path.join(OUT, '%s_%s_%g_size.json.gz' % (game, 'Z' if s.startswith('Z') else 'A', float(s.split('@')[-1]))) for s in lv]
        jobs.append(('lt_%s_400_16' % game, [PY, FPC, 'lt', game, '400_16'] + lv, outs))
    return jobs


def pd_jobs():
    jobs = []
    for lv in (0.1, 0.0, 1.0, 10.0, 0.3, 0.03):                  # cut order: PD 0.03 and 0.3 last
        rule = 'Z' if lv == 0.0 else 'A'
        jobs.append(('pd_%g' % lv, [PY, FPC, 'pd', repr(lv)], [os.path.join(OUT, 'pd_%s_%g.json.gz' % (rule, lv))], True))
    return jobs


def batch():
    j = []
    lts = lt_jobs(); pds = pd_jobs()
    j.append(lts[0] + (False,)); j.append(lts[1] + (False,))
    j.append(pds[0]); j.append(pds[1]); j.append(pds[2]); j.append(pds[3])
    j.append(lts[2] + (False,)); j.append(lts[3] + (False,))
    j.append(pds[4]); j.append(pds[5])
    return j


def done_pd(path, n=40):
    if not os.path.exists(path): return False
    import gzip
    try:
        d = json.load(gzip.open(path, 'rt'))
        return len(d['recs']) >= n
    except Exception:
        return False


def finished(job):
    name, cmd, outs, ispd = job
    if ispd: return done_pd(outs[0])
    return all(os.path.exists(o) for o in outs)


def main():
    if sys.argv[1] == 'hashes':
        sys.path.insert(0, HERE)
        import failure_pricing_confirm as F
        os.makedirs(OUT, exist_ok=True)
        path = os.path.join(OUT, 'provenance_hashes.json')
        d = json.load(open(path)) if os.path.exists(path) else {}
        d[sys.argv[2]] = dict(time=time.strftime('%Y-%m-%d %H:%M:%S'), caches=F.cache_hashes(), code=F.code_hashes())
        json.dump(d, open(path, 'w'), indent=1)
        print(json.dumps(d[sys.argv[2]], indent=1)[:2000])
        return 0
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    os.makedirs(OUT, exist_ok=True)
    todo = [j for j in batch() if not finished(j)]
    print('%d jobs, %d workers (pid %d): %s' % (len(todo), workers, os.getpid(), [j[0] for j in todo]), flush=True)
    running = []
    tries = {}
    last = time.time()
    while todo or running:
        while todo and len(running) < workers:
            job = todo.pop(0)
            logp = os.path.join(OUT, 'log_%s.txt' % job[0])
            f = open(logp, 'a')
            p = subprocess.Popen(job[1], stdout=f, stderr=subprocess.STDOUT, cwd=ROOT)
            running.append((job, p, f, logp, time.time()))
            print('start', job[0], 'pid', p.pid, flush=True); last = time.time()
        time.sleep(20)
        for item in list(running):
            job, p, f, logp, t0 = item
            if p.poll() is not None:
                f.close(); running.remove(item)
                print('done', job[0], 'rc', p.returncode, 'wall %.0fs' % (time.time() - t0), flush=True); last = time.time()
                if (p.returncode != 0 or not finished(job)) and tries.get(job[0], 0) < 3:
                    tries[job[0]] = tries.get(job[0], 0) + 1
                    todo.insert(0, job)
                    print('retry', job[0], 'attempt', tries[job[0]], flush=True)
        newest = max([os.path.getmtime(it[3]) for it in running] + [last]) if running else last
        if running and time.time() - newest > 7200:
            print('STALL', flush=True)
            for it in running: it[1].kill()
            return 2
    print('batch finished', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
