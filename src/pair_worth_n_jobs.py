"""Job file of queue 73 (notes/pair-worth-n.md 1.6), in priority order (never-cut first, cut order reversed at the end).
    python3 src/pair_worth_n_jobs.py OUTFILE
Line: arm|N|run|delta|lams|mNs|chase."""
import sys


def job(arm, N, r, delta=0.05, lams='0,10', mns='1,0', chase=20):
    return '%s|%d|%d|%s|%s|%s|%d' % (arm, N, r, delta, lams, mns, chase)


def jobs():
    L = []
    add = L.append
    # ---------------- N = 100 (cheap)
    for r in range(60):
        add(job('CF', 100, r))                                   # cell C
    for r in range(20, 60):
        add(job('CG', 100, r))                                   # cell C: extend C+G to 60 runs
    for r in range(20):
        add(job('CFm', 100, r, mns='1'))                         # cell E
        add(job('CBk1', 100, r))
        add(job('CBk4', 100, r))
    # ---------------- N = 200 (cell A, E); Lambda 0 and 10, mN 1 and 0
    for r in range(20, 40):
        for arm in ('C', 'CBs', 'CG', 'CB', 'CF'):
            add(job(arm, 200, r))
    for r in range(20, 40):
        for d in (0.025, 0.15, 0.5):
            add(job('CBs', 200, r, delta=d))
        add(job('CF4', 200, r))
        add(job('CFm', 200, r, mns='1'))
        add(job('CBk1', 200, r))
        add(job('CBk4', 200, r))
    # ---------------- N = 400 (cell B), Lambda = 10; never cut: C, C+B*, C+G delta = 0.05 mN = 1, runs 20-59
    for r in range(20, 40):
        for arm in ('C', 'CBs', 'CG'):
            add(job(arm, 400, r, lams='10', mns='1'))
    for r in range(40, 60):
        for arm in ('C', 'CBs', 'CG'):
            add(job(arm, 400, r, lams='10', mns='1'))
    for r in range(40, 60):                                      # N = 200 extra replication (the last item of the cut order)
        for arm in ('C', 'CBs', 'CG'):
            add(job(arm, 200, r))
    # cut order, last cut first: C+B and C+F at N = 400; dose cells; mN = 0; E at N = 400; (C+F4 at N = 200 only); G; D
    for r in range(20, 40):
        for arm in ('CB', 'CF'):
            add(job(arm, 400, r, lams='10', mns='1'))
    for r in range(20, 40):
        for d in (0.0125, 0.15, 0.5):
            add(job('CBs', 400, r, delta=d, lams='10', mns='1'))
    for r in range(20, 40):
        for arm in ('C', 'CBs', 'CG', 'CF'):
            add(job(arm, 400, r, lams='10', mns='0'))
        add(job('CBs', 400, r, delta=0.0125, lams='10', mns='0'))
    for r in range(20, 40):
        for arm in ('CBk1', 'CBk4'):
            add(job(arm, 400, r, lams='10', mns='1'))
            add(job(arm, 400, r, lams='10', mns='0'))
    for r in range(20, 25):                                      # G: longer chase, 60 N
        for arm in ('CBs', 'CG'):
            add(job(arm, 400, r, lams='10', mns='1', chase=60))
    for r in range(20, 30):                                      # D: N = 800
        for arm in ('C', 'CBs', 'CG'):
            add(job(arm, 800, r, lams='10', mns='1'))
    return L


if __name__ == '__main__':
    L = jobs()
    open(sys.argv[1], 'w').write('\n'.join(L) + '\n')
    print(len(L), 'jobs')
