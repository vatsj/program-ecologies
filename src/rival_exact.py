"""Exact check of the death-birth kernel on small graphs (hypercube d = 3, torus 3 x 3).

For a 2x2 block U (0 = resident, 1 = mutant), solves the absorbing-chain equations over all
2^N configurations for h(x) = P(mutant count reaches N/2 before 0 | x), with the update of
src/rival_kernels.py: a uniformly random site s dies; its neighbours compete with weight
exp(w * mean payoff over their own neighbours), evaluated *before* s is replaced (s still
holds its old type).  Compares h averaged over single-mutant placements with the Monte
Carlo kernel _invade_fix.  Single-threaded.

    python3 src/rival_exact.py
"""
import os
for v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[v] = '1'
import sys, time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
sys.path.insert(0, os.path.dirname(__file__))
from graph_rates import torus, hypercube
from rival_kernels import _invade_fix
from graph_rates_run import wilson

W = 0.3


def exact_half(U, nb, w=W):
    N, deg = nb.shape
    S = 1 << N
    xs = np.arange(S)
    g = ((xs[:, None] >> np.arange(N)[None, :]) & 1).astype(np.int64)        # S x N
    k = g.sum(1)
    pay = np.zeros((S, N))
    for v in range(N):
        for u in nb[v]:
            pay[:, v] += U[g[:, v], g[:, u]]
    pay /= deg
    absorb = (k == 0) | (2 * k >= N)
    rows, cols, vals = [], [], []
    stay = np.ones(S)
    for s in range(N):
        e = np.exp(w * (pay[:, nb[s]] - pay[:, nb[s]].max(1, keepdims=True)))
        pm = (e * g[:, nb[s]]).sum(1) / e.sum(1)
        up = (g[:, s] == 0) & ~absorb                      # resident site s -> mutant w.p. pm
        dn = (g[:, s] == 1) & ~absorb
        rows.append(xs[up]); cols.append(xs[up] | (1 << s)); vals.append(pm[up] / N)
        rows.append(xs[dn]); cols.append(xs[dn] & ~(1 << s)); vals.append((1 - pm[dn]) / N)
        stay[up] -= pm[up] / N; stay[dn] -= (1 - pm[dn]) / N
    P = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(S, S))
    # transient equations: h = P h + stay*h  =>  (I - P - diag(stay)) h = 0 on transient, h = b on absorbing
    b = np.where(absorb & (k > 0), 1.0, 0.0)
    A = sp.identity(S, format='csr') - P - sp.diags(np.where(absorb, 0.0, stay))
    if S <= 4096:
        h = spla.spsolve(A.tocsc(), b)
    else:
        h, info = spla.bicgstab(A, b, tol=1e-12, maxiter=20000)
        assert info == 0, info
    return float(np.mean([h[1 << v] for v in range(N)]))


def main():
    blocks = {'FB|D': (0.0, -1.0, -1.0, -1.0), 'P*|FB c=0.1': (0.0, -1.6, -1.2, 0.0), 'FB|P* c=0.1': (0.0, -1.2, -1.6, 0.0),
              'D|ALLC': (-1.0, 1.0, -2.0, 0.0), 'shadow|P* c=0.1': (0.0, -0.2, -0.4, 0.0)}
    for gname, nb in (('hypercube 3', hypercube(3)), ('torus 3', torus(3))):
        for name, (qq, qr, rq, rr) in blocks.items():
            U2 = np.array([[rr, rq], [qr, qq]])
            t = time.time(); ex = exact_half(U2, nb)
            h, l, u, *_ = _invade_fix(U2, nb, W, 1000000, 1000, 0, 0, 11)
            lo, hi = wilson(h, h + l)
            print('%s %-16s exact %.5f  MC %.5f [%.5f, %.5f]  %s (%.0fs)' % (gname, name, ex, h / (h + l), lo, hi,
                  'ok' if lo <= ex <= hi else 'MISMATCH', time.time() - t), flush=True)


if __name__ == '__main__':
    main()
