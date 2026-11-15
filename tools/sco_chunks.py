#!/usr/bin/env python3
"""Queue 80: split the step-2 jobs into Daytona chunks (one world per chunk; balanced by cost) and write runs/sco_launch/queue.txt in
priority order (the spec's cut order last: N = 100 and 400 cells).

    python3 tools/sco_chunks.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import script_offers_run as R

GROUPS = [('k', ['K', 'K2'], 3), ('core', ['U', 'A1', 'A2'], 4), ('rest', ['A3', 'A4', 'A5', 'seed'], 3), ('nscale', ['A1n', 'A2n'], 5)]

if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(os.path.join(root, 'runs', 'sco_jobs'), exist_ok=True)
    os.makedirs(os.path.join(root, 'runs', 'sco_launch'), exist_ok=True)
    names = []
    tot = 0
    for tag, stages, k in GROUPS:
        jobs = R.make_jobs(stages)
        bins = [[] for _ in range(k)]; load = [0.0] * k
        for j in jobs:                       # longest first, greedy balance
            i = load.index(min(load)); bins[i].append(j); load[i] += R.cost(j)
        for i, b in enumerate(bins):
            nm = '%s_%dof%d' % (tag, i, k)
            open(os.path.join(root, 'runs', 'sco_jobs', nm + '.txt'), 'w').write('\n'.join(b) + '\n')
            names.append(nm); tot += load[i]
            print(nm, len(b), 'jobs, cost units %.0f' % load[i])
    open(os.path.join(root, 'runs', 'sco_launch', 'queue.txt'), 'w').write('\n'.join(names) + '\n')
    print('total cost units %.0f' % tot)
