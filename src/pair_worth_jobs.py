"""Job lists for the pair-worth experiment.  python3 src/pair_worth_jobs.py STAGE OUTFILE
Stages (priority order): main, sec1 (mN already in main; Lambda 1/100, doses, R, transfer), sec2 (N = 200, 400)."""
import sys

RUNS = 20
MN_ALL = '1,0,0.1'


def job(g, arm, r, N=100, delta=0.05, lams='0,10', mns=MN_ALL):
    return '%s|%s|%d|%d|%s|%s|%s' % (g, arm, r, N, delta, lams, mns)


def stage(name):
    L = []
    if name == 'main':
        cells = [('pw13', a) for a in ('CBs', 'C', 'CB', 'CG', 'CA')] + \
                [('pw56', a) for a in ('C', 'CB', 'CBK', 'CB2', 'CG', 'CA')] + \
                [('pw23', 'C'), ('pw23', 'CB'), ('gl6', 'C'), ('gl6', 'CB')] + \
                [('pw13', 'CB0'), ('pw13', 'CBs0'), ('pw56', 'CB0'), ('pw56', 'CBK0')]
        for g, a in cells:
            for r in range(RUNS):
                L.append(job(g, a, r))
    elif name == 'sec1':
        for g, arms in (('pw13', ('C', 'CB', 'CBs')), ('pw56', ('C', 'CB'))):
            for a in arms:
                for r in range(RUNS):
                    L.append(job(g, a, r, lams='1,100'))
        for g, arms in (('pw13', ('CB', 'CBs')), ('pw56', ('CB',))):
            for d in (0.01, 0.15):
                for a in arms:
                    for r in range(RUNS):
                        L.append(job(g, a, r, delta=d))
        for r in range(RUNS):
            L.append(job('pw13', 'CBe', r, mns='1,0'))
        for g in ('pw13', 'pw56'):
            for a in ('R', 'RB'):
                for r in range(RUNS):
                    L.append(job(g, a, r))
        for g in ('pw23t', 'gl24'):
            for a in ('C', 'CB'):
                for r in range(RUNS):
                    L.append(job(g, a, r))
    elif name == 'sec2':
        for a in ('CB', 'CBK'):
            for r in range(RUNS):
                L.append(job('pw56', a, r, N=200, mns='1,0'))
        for N in (200, 400):
            for a in ('C', 'CBs'):
                for r in range(RUNS):
                    L.append(job('pw13', a, r, N=N, mns='1'))
    elif name == 'sec3':
        # engineer's additions: high doses (is the mechanism ever sufficient?), and runs 20-59 of the key cells
        for g, arms in (('pw13', ('CBs', 'CB')), ('pw56', ('CB', 'CBK'))):
            for d in (0.3, 0.5):
                for a in arms:
                    if a == 'CBK' and d > 0.3:
                        continue
                    for r in range(RUNS):
                        L.append(job(g, a, r, delta=d))
        for g, arms in (('pw13', ('C', 'CBs', 'CB')), ('pw56', ('C', 'CB', 'CBK'))):
            for a in arms:
                for r in range(20, 60):
                    L.append(job(g, a, r))
    else:
        raise SystemExit(name)
    return L


if __name__ == '__main__':
    with open(sys.argv[2], 'w') as f:
        f.write('\n'.join(stage(sys.argv[1])) + '\n')
