"""Diagnostic: rerun the torus 128, c = 0.01, all-D, seed 3 agent-based run (the one whose FB-net
sea lost its ALLC load) and print the final composition by class.  Same kernel, same seed.

    python3 src/rival_seed3.py
"""
import os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import rival_run as R
from rival_kernels import _abm

prov, nw, reps = R.setup(0.01)
U = np.ascontiguousarray(prov.Ufull); A = np.ascontiguousarray(prov.ACT)
lab = np.array([R.LABS.index(l) for l in nw['lab']], np.int64)
mu = nw['mu'].copy(); cdf = np.cumsum(mu) / mu.sum()
nb = R.graph('torus', 128); N = nb.shape[0]
init = np.full(N, reps['D-type'], np.int64)
rec, grid = _abm(U, A, lab, len(R.LABS), cdf, nb, R.W, 1e-3, 200000, 100, init, 3, reps['FB-net'], reps['P*-net'], reps['exploitable'])
cnt = collections.Counter(grid.tolist())
iC, iD = reps['exploitable'], reps['D-type']
for k, v in cnt.most_common(8):
    print('%-45s %-11s share %.3f  vs ALLC: %s  ALLC vs it: %s  vs D: %s  vs FB: %s' % (
        prov.names[k], nw['lab'][k], v / N, 'C' if A[k, iC] else 'D', 'C' if A[iC, k] else 'D', 'C' if A[k, iD] else 'D',
        'C' if A[k, reps['FB-net']] else 'D'))
