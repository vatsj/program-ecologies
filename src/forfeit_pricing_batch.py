"""Batch driver for the forfeit-pricing run: one process per job, at most W at a time, jobs in priority order (the spec's cut order read
backwards: A with X at 1, A_m in inspection and A_f at 0.03 are last), skipping jobs whose output exists.  Exits when the batch is done;
prints STALL and exits if no log file has changed for 2 hours.  No multiprocessing.Pool.

    python3 src/forfeit_pricing_batch.py run [workers]
    python3 src/forfeit_pricing_batch.py hashes pre|post
"""
import gzip
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'forfeit_pricing')
PY = sys.executable
FRR = os.path.join(HERE, 'forfeit_pricing_run.py')
FPD = os.path.join(HERE, 'forfeit_pricing_pd.py')


def specs(game):
    """Cell specs of a game in priority order (cut order last)."""
    s = []
    hi = [0.1, 0.3, 1.0, 10.0]
    s += ['Af@%g' % l for l in hi] + ['A@%g' % l for l in (0.1, 0.3, 1.0, 10.0)]
    s += ['Af+X@%g' % l for l in hi]
    s += ['Am@%g' % l for l in hi] if game == 'rps' else ['Am@0.1']
    s += ['Am+X@%g' % l for l in hi] if game == 'rps' else []
    s += ['Af+S@0.1', 'A+X@0.1', 'Af+S@1', 'Af@0.03', 'Af+X@0.03', 'A@0.03']
    if game == 'rps': s += ['Am@0.03', 'Am+X@0.03']
    s += ['A+X@1']
    if game == 'insp': s += ['Am@1', 'Am+X@0.1', 'Am+X@1']
    # de-duplicate keeping order
    out = []
    for x in s:
        if x not in out: out.append(x)
    return out


def spec_file(game, s):
    sys.path.insert(0, HERE)
    import forfeit_pricing_run as FR
    rule, arm, level = FR.parse_spec(s)
    return os.path.join(OUT, FR.spec_name(game, rule, arm, level) + '.json.gz')


def done_pd(path, n=40):
    if not os.path.exists(path): return False
    try:
        return len(json.load(gzip.open(path, 'rt'))['recs']) >= n
    except Exception:
        return False


def jobs():
    j = []
    for game in ('rps', 'insp'):
        sp = specs(game)
        j.append(('lt_%s' % game, [PY, FRR, 'lt', game] + sp, [spec_file(game, s) for s in sp], False))
    j.append(('static', [PY, os.path.join(HERE, 'forfeit_pricing_static.py')], [os.path.join(OUT, 'static_K.json')], False))
    for lv in (0.1, 1.0):
        j.append(('pd_%g' % lv, [PY, FPD, repr(lv)], [os.path.join(OUT, 'pd_Af_%g.json.gz' % lv)], True))
    return j


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
        code = F.code_hashes()
        for f in ('forfeit_pricing.py', 'forfeit_pricing_run.py', 'forfeit_pricing_pd.py', 'forfeit_pricing_batch.py'):
            code['src/' + f] = F._sha(os.path.join(HERE, f))
        d[sys.argv[2]] = dict(time=time.strftime('%Y-%m-%d %H:%M:%S'), caches=F.cache_hashes(), code=code)
        json.dump(d, open(path, 'w'), indent=1)
        print(json.dumps(d[sys.argv[2]], indent=1)[:1500])
        return 0
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    os.makedirs(OUT, exist_ok=True)
    todo = [j for j in jobs() if not finished(j)]
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
