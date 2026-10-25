"""Driver for the churn-in-the-primary-object experiment (notes/churn-primary.md).

    python3 src/churn_primary_run.py jobs OUT [--stage S ...]    # write the job list (stages in priority order)
    python3 src/churn_primary_run.py one JOB                     # run one job in this process and print a digest
    python3 src/churn_primary_run.py worker JOBFILE              # claim and run jobs of the file one at a time
    python3 src/churn_primary_run.py batch JOBFILE --workers K   # start K worker processes, wait, STALL watchdog

A job is  L:<spec>:<run>[:c0]  (one run of a lottery cell at every mN) or  P:<name>  (one probe configuration).
One job per process at a time; no multiprocessing.Pool.  Per-job records go to $CP_SCRATCH/<job>.json (outside the
repository); churn_primary_report.py aggregates them into runs/churn-primary.{md,json} and runs/churn_primary/.
"""
import argparse, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SCR = os.environ.get('CP_SCRATCH', '/private/tmp/claude-501/-Users-jstav-code-program-ecologies/'
                     'eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/churn/out')
CACHE = os.environ.get('CP_CACHE', '/private/tmp/claude-501/-Users-jstav-code-program-ecologies/'
                       'eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/churn/cache')
RUNS = 40
H = 10000

LOTTERY = ['B6w', 'B6m', 'E10m', 'E10w'] + ['Emin-%s-%s' % (d, e) for d in ('main', 'hi', 'lo') for e in ('m', 'w')] + \
          ['T-main', 'T-lo', 'T-hi']
C0_CELLS = ['T-main', 'T-hi']


# ---------------------------------------------------------------- probe configurations
def probe_defs():
    P = {}
    gram = {'dm': 'Emin-main-m', 'dw': 'Emin-main-w', 't': 'T-main'}
    for g, spec in gram.items():
        kinds = ['const', 'switch', 'two'] + (['taker'] if g != 't' else [])
        for kind in kinds:
            for st in ('a', 'b'):
                if kind == 'taker' and st == 'b':
                    continue
                P['P-%s-%s-%s-single' % (g, kind, st)] = dict(spec=spec, kind=kind, stratum=st, reps=200)
                if kind != 'const':
                    for ctl in ('sham', 'namepres', 'twin'):
                        if st == 'a' or ctl == 'sham':
                            P['P-%s-%s-%s-%s' % (g, kind, st, ctl)] = dict(spec=spec, kind=kind, stratum=st, control=ctl, reps=100)
        for Nn in (50, 200):
            P['P-%s-switch-a-N%d' % (g, Nn)] = dict(spec=spec, kind='switch', stratum='a', N=Nn, reps=100)
        P['P-%s-switch-a-frac' % g] = dict(spec=spec, kind='switch', stratum='a', mode='frac', frac=0.05, reps=100)
    for g, key in (('dm', 'modal'), ('dw', 'weak'), ('t', 'T')):
        P['H-%s' % g] = dict(spec=gram[g], hom=key, fracs=[0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], reps=100)
    return P


PROBES = probe_defs()


def job_name(j):
    return j.replace(':', '__')


def result_path(j):
    return os.path.join(SCR, job_name(j) + '.json')


def run_job(j):
    import churn_primary as CP
    parts = j.split(':')
    if parts[0] == 'L':
        spec, r = parts[1], int(parts[2])
        price = 1.2e-4 if len(parts) > 3 and parts[3] == 'c0' else 0.0
        recs = CP.run_cell_run(spec, r, H=H, price=price, cache_dir=CACHE)
        return dict(job=j, recs=recs)
    if parts[0] == 'B':
        import churn_primary_probe as PR
        recs = PR.run_balanced(parts[1], parts[2], int(parts[3]), mNs=(0.01, 0.1, 1), H=H, cache_dir=CACHE)
        return dict(job=j, recs=recs)
    if parts[0] == 'P':
        import churn_primary_probe as PR
        name = parts[1]
        d = dict(PROBES[name])
        spec = d.pop('spec')
        cat = CP.get_cat(spec, cache_dir=CACHE)
        t0 = time.time()
        if 'hom' in d:
            key = d.pop('hom')
            outs = PR.hom_cell(cat, key, N=100, fracs=tuple(d['fracs']), reps=d['reps'])
            out = dict(job=j, name=name, hom={str(f): _ser(o) for f, o in outs.items()})
        else:
            cfg = PR.probe_config(cat, d.pop('kind'), d.pop('stratum'), seed_base='P|' + name, **d)
            out = dict(job=j, name=name, cfg=_ser(cfg) if cfg is not None else None)
        out['wall'] = round(time.time() - t0, 1)
        return out
    raise ValueError(j)


def _ser(cfg):
    if cfg is None:
        return None
    c = dict(cfg)
    c['rows'] = {'%d:%d' % k: v for k, v in cfg['rows'].items()}
    return c


def worker(jobfile):
    os.makedirs(SCR, exist_ok=True)
    os.makedirs(os.path.join(SCR, '_claims'), exist_ok=True)
    jobs = [l.strip() for l in open(jobfile) if l.strip() and not l.startswith('#')]
    for j in jobs:
        if os.path.exists(result_path(j)):
            continue
        claim = os.path.join(SCR, '_claims', job_name(j))
        try:
            fd = os.open(claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode()); os.close(fd)
        except FileExistsError:
            continue
        t0 = time.time()
        try:
            rec = run_job(j)
        except Exception as e:
            print('FAIL', j, repr(e), flush=True)
            import traceback; traceback.print_exc()
            continue
        tmp = result_path(j) + '.tmp'
        json.dump(rec, open(tmp, 'w'), default=_default)
        os.replace(tmp, result_path(j))
        print('done', j, 'wall %.0f' % (time.time() - t0), flush=True)


def _default(o):
    import numpy as np
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, tuple)):
        return list(o)
    raise TypeError(type(o))


def batch(jobfile, workers, stall_hours=2.0, log=None):
    here = os.path.abspath(__file__)
    procs = []
    os.makedirs(SCR, exist_ok=True)
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


STAGES = {
    # stage 1: the matched baseline, the arm-E cells and the gate
    '1': lambda: ['L:%s:%d' % (s, r) for s in ('B6w', 'B6m', 'E10m', 'E10w') for r in range(RUNS)],
    # stage 2: E-min and T at c = 0
    '2': lambda: ['L:%s:%d' % (s, r) for s in LOTTERY[4:] for r in range(RUNS)],
    # stage 3: the probe and the homogeneous-reader cell
    '3': lambda: ['P:%s' % n for n in PROBES],
    # stage 4: the balanced start with resident readers (an extension, registered in the predictions' addendum)
    '4': lambda: ['B:%s:%s:%d' % (sp, k, r) for sp, kinds in (('B6w', ('const',)), ('B6m', ('const',)),
                                                              ('Emin-main-m', ('const', 'switch', 'two')),
                                                              ('Emin-main-w', ('const', 'switch', 'two')),
                                                              ('T-main', ('const', 'switch', 'two'))) for k in kinds
                  for r in range(20)],
    # stage 5: the c0 sensitivity (cut candidate)
    '5': lambda: ['L:%s:%d:c0' % (s, r) for s in C0_CELLS for r in range(RUNS)],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('a', nargs='*')
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--stage', nargs='*', default=sorted(STAGES))
    a = ap.parse_args()
    if a.cmd == 'one':
        rec = run_job(a.a[0])
        print(json.dumps(rec, default=_default)[:3000])
    elif a.cmd == 'worker':
        worker(a.a[0])
    elif a.cmd == 'batch':
        sys.exit(batch(a.a[0], a.workers))
    elif a.cmd == 'jobs':
        lines = []
        for st in a.stage:
            lines += STAGES[st]()
        open(a.a[0], 'w').write('\n'.join(lines) + '\n')
        print(len(lines), 'jobs')


if __name__ == '__main__':
    main()
