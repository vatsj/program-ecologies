"""Driver for step 2 of queue 80 (spec specs/2026-11-16-script-checked-offers.md); queue 79's certified_offers_run.py with this queue's
stages.

    python3 src/script_offers_run.py jobs OUT.txt STAGE [STAGE ...] [--part i/k]
    python3 src/script_offers_run.py run JOBFILE OUTDIR          # DAYTONA_CPUS workers; writes OUTDIR/tables_md5.json first
    python3 src/script_offers_run.py rows OUTDIR

A job is `series|spec|N|I|r|long`; one JSON row per finished job in OUTDIR/rows_<pid>.jsonl.  Stages (I = 64, 20 runs, the five delta,
N = 200 unless stated; beta = 0 has no bullies, so phi is run once there):
  U    UF, UFR (phi 0), beta 0, 1, 3
  K    K, phi 0 and 1/2
  K2   K2, phi 0 and 1/2
  A1   A1, phi 0 and 1/2;  A1n: N = 100 and 400 at beta 3, phi 0 and 1/2
  A2   A2, likewise;       A2n
  A3   A3, phi 1/2 and 1
  A4   A4, phi 1/2 and 1 at beta 1, 3; phi 0 at beta 3
  A5   A5, phi 1/2, beta 3
  seed A2, all-unequal simulating-bully start, delta 0.03, beta 3, phi 1/2, to 240N
  v1   UF0, UFR0 (old fuel) on queue 79's V1 cells
"""
import argparse, glob, json, os, sys, time, hashlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DELTAS = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3]
RUNS = 20
COSTW = {100: 0.3, 200: 1.0, 400: 4.4}


def fmt(x):
    return repr(float(x))


def jid(series, spec, N, I, r, long=False):
    return '%s|%s|%d|%d|%d|%d' % (series, spec, N, I, r, int(long))


def sco(arm, d, b, ph=0.5, extra=''):
    return 'sco:arm=%s:d=%s:b=%s:ph=%s%s' % (arm, fmt(d), fmt(b), fmt(ph), extra)


def cost(job):
    s = job.split('|')
    return COSTW[int(s[2])] * (2.0 if s[5] == '1' else 1.0)


def cells(arm, phis_by_beta, N=200, series=None):
    out = []
    for b, phis in phis_by_beta:
        for ph in phis:
            for d in DELTAS:
                for r in range(RUNS):
                    out.append(jid(series or arm, sco(arm, d, b, ph), N, 64, r))
    return out


PH01 = [(0.0, [0.5]), (1.0, [0.0, 0.5]), (3.0, [0.0, 0.5])]


def make_jobs(stages):
    jobs = []
    for st in stages:
        if st == 'U':
            for arm in ('UF', 'UFR'):
                jobs += cells(arm, [(0.0, [0.0]), (1.0, [0.0]), (3.0, [0.0])])
        elif st in ('K', 'K2', 'A1', 'A2'):
            jobs += cells(st, PH01)
        elif st in ('A1n', 'A2n'):
            for N in (100, 400):
                jobs += cells(st[:2], [(3.0, [0.0, 0.5])], N=N, series=st)
        elif st == 'A3':
            jobs += cells('A3', [(0.0, [0.5]), (1.0, [0.5, 1.0]), (3.0, [0.5, 1.0])])
        elif st == 'A4':
            jobs += cells('A4', [(0.0, [0.5]), (1.0, [0.5, 1.0]), (3.0, [0.0, 0.5, 1.0])])
        elif st == 'A5':
            jobs += cells('A5', [(3.0, [0.5])])
        elif st == 'seed':
            for r in range(RUNS):
                jobs.append(jid('seed', sco('A2', 0.03, 3.0, 0.5, ':seed=unequal'), 200, 64, r, True))
        elif st == 'v1':
            for arm in ('UF0', 'UFR0'):
                for (N, b, d) in ((200, 1.0, 0.01), (200, 1.0, 0.1), (200, 3.0, 0.01), (200, 3.0, 0.1), (100, 3.0, 0.1)):
                    for r in range(2):
                        jobs.append(jid('v1', sco(arm, d, b, 0.0), N, 64, r))
        elif st == 'pilot':
            jobs.append(jid('pilot', sco('A2', 0.03, 3.0), 200, 64, 95))
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


def worker(jobfile, outdir):
    import script_offers_dyn as D
    jobs = [l.strip() for l in open(jobfile) if l.strip()]
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
            row = D.run_job(j)
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


def tables_md5(worlds):
    import numpy as np
    import script_offers_dyn as D
    out = {}
    for w in worlds:
        tb = D.tabs(w)
        h = hashlib.md5()
        for a in (tb.code, tb.nto, tb.fo):
            h.update(np.ascontiguousarray(a).tobytes())
        out[w] = h.hexdigest()
    return out


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    a = sp.add_parser('jobs'); a.add_argument('out'); a.add_argument('stages', nargs='+'); a.add_argument('--part', default=None)
    b = sp.add_parser('run'); b.add_argument('jobfile'); b.add_argument('outdir'); b.add_argument('--workers', type=int)
    c = sp.add_parser('rows'); c.add_argument('outdir')
    d = sp.add_parser('worker'); d.add_argument('jobfile'); d.add_argument('outdir')
    m = sp.add_parser('md5'); m.add_argument('worlds', nargs='+')
    ns = ap.parse_args()
    if ns.cmd == 'jobs':
        jobs = make_jobs(ns.stages)
        if ns.part:
            i, k = [int(x) for x in ns.part.split('/')]
            jobs = jobs[i::k]
        os.makedirs(os.path.dirname(os.path.abspath(ns.out)), exist_ok=True)
        open(ns.out, 'w').write('\n'.join(jobs) + '\n')
        print(len(jobs), 'jobs, cost units %.0f' % sum(cost(j) for j in jobs))
    elif ns.cmd == 'rows':
        print(len(load_rows(ns.outdir)))
    elif ns.cmd == 'md5':
        print(json.dumps(tables_md5(ns.worlds)))
    elif ns.cmd == 'worker':
        worker(ns.jobfile, ns.outdir)
    else:
        os.makedirs(ns.outdir, exist_ok=True)
        nw = ns.workers or int(os.environ.get('DAYTONA_CPUS', os.cpu_count() or 1))
        jobs = [l.strip() for l in open(ns.jobfile) if l.strip()]
        import script_offers_dyn as D
        worlds = sorted({D.world_of(D.parse(j.split('|')[1])['arm']) if False else D.world_of(j.split('|')[1].split('arm=')[1].split(':')[0])
                         for j in jobs})
        t0 = time.time()
        md = tables_md5(worlds)
        json.dump(dict(md5=md, build_wall=round(time.time() - t0)), open(os.path.join(ns.outdir, 'tables_md5.json'), 'w'))
        procs = [subprocess.Popen([sys.executable, os.path.abspath(__file__), 'worker', ns.jobfile, ns.outdir]) for _ in range(nw)]
        for p in procs:
            p.wait()
        sys.exit(1 if any(p.returncode for p in procs) else 0)


if __name__ == '__main__':
    main()
