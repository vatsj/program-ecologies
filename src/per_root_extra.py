"""Extra job lists for the per-root run (notes §1.0 item 11, predictions addendum): the role-split diagnostics, the
mediation replays and the 20,000-generation extensions, in one pool of <= 3 processes, one job per process.

  python3 src/per_root_extra.py --procs 1
"""
import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import per_root_run as RR

DIAG_REPS = (3, 5, 9, 14, 15, 16, 18)          # the development streams where R2 was fair (predictions addendum)
EXT_REPS = (3, 5, 9, 14, 15)


def jobs():
    jl = []
    for cell in ('R2b_i', 'R2w_i'):
        for r in DIAG_REPS:
            jl.append((cell, r, 10000))
    jl += RR.replay_jobs('R2_i', 5, reps=range(40))
    for r in EXT_REPS:
        jl.append(('R2_i', r, 20000, None, 'R2_i_ext20k'))
        jl.append(('Hfull_i', r, 20000, None, 'Hfull_i_ext20k'))
    out = []
    for j in jl:
        tag = j[4] if len(j) > 4 else j[0]
        if not os.path.exists(os.path.join(RR.OUT, 'cell_' + tag, 'rep_%03d.json' % j[1])):
            out.append(j)
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--procs', type=int, default=1)
    a = ap.parse_args()
    RR.run_pool(jobs(), a.procs)
