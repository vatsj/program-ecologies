"""Job plan of the annealed-tail experiment: builds the job files (one JSON per line) and the bisection driver.

    python3 src/annealed_tail_plan.py write NAME      # writes $AT/jobs/NAME.txt
    python3 src/annealed_tail_plan.py bisect NAME     # job-file of bisection series (each line a 'bisect' series; run with the worker)

Series key: dict(kind, cell, start, tail, renorm, N, obj, t0 or schedule kind).  A series' grid rows are the jobs of mk().
"""
import os, sys, json
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import annealed_tail as A

LAMS = [0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0]
T0S = [1.0, 100.0, 10000.0]
JOBS = os.path.join(A.SCR, 'jobs')
os.makedirs(JOBS, exist_ok=True)


def mk(kind, cell, start, Lam, t0=100.0, sk='anneal', **kw):
    sched = dict(kind=sk, Lam=float(Lam))
    if sk == 'anneal':
        sched['t0'] = float(t0)
    else:
        sched['T'] = float(t0)
    j = dict(kind=kind, cell=cell, start=start, sched=sched)
    j.update(kw)
    return j


def write(name, jobs):
    p = os.path.join(JOBS, name + '.txt')
    with open(p, 'w') as f:
        for j in jobs:
            f.write(json.dumps(j, sort_keys=False) + '\n')
    return p


def plan_main():
    jobs = []
    # priority: M natural, L natural, M u=0.6, L u=0.6; t0 = 1, 100, then 1e4
    for t0 in (100.0, 1.0):
        for Lam in LAMS:
            jobs.append(mk('dsl', 'M0', 'nat', Lam, t0))
    for t0 in (100.0, 1.0):
        for cell, start in (('L0', 'nat'), ('M0', 'u:0.6'), ('L0', 'u:0.6')):
            for Lam in LAMS:
                jobs.append(mk('dsl', cell, start, Lam, t0))
    for cell, start in (('M0', 'nat'), ('L0', 'nat'), ('M0', 'u:0.6'), ('L0', 'u:0.6')):
        for Lam in LAMS:
            jobs.append(mk('dsl', cell, start, Lam, 1e4))
    return jobs


def plan_armT():
    jobs = []
    for cell in ('main|0.1|0', 'main|0|0'):
        for start in ('nat', 'u:0.8'):
            for t0 in T0S:
                for Lam in LAMS:
                    jobs.append(mk('armT', cell, start, Lam, t0))
    return jobs


def plan_late():
    jobs = []
    for t0 in (1.0, 100.0, 10000.0):
        for Lam in [0.01, 0.03] + LAMS:
            jobs.append(mk('dsl', 'M0', 'late', Lam, t0))
    return jobs


def plan_rain():
    return [mk('dsl', 'M0', 'nat', Lam, 1e4, sk='const') for Lam in LAMS]


PLANS = dict(main=plan_main, armT=plan_armT, late=plan_late, rain=plan_rain)

if __name__ == '__main__':
    cmd, name = sys.argv[1], sys.argv[2]
    if cmd == 'write':
        print(write(name, PLANS[name]()))
