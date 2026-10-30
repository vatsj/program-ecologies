"""Finite worlds of the rare-migration jump chain on triples (I islands, exact one-migrant kernel PF), arm T.

One event: recipient island uniform, donor island uniform among the others, slot uniform; the migrant (the donor's
program in that slot) fixes with the exact Moran probability PF.  Time = events per island.
"""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import many_islands_t as M

NP = M.NP


@njit(cache=True)
def world_run(PF, tri, cps, seed, CLv, PAIRv, hist, pairs, first_loss, ncls):
    """tri (I,) int64 triple index per island (mutated).  cps: sorted checkpoints in events per island.  hist[len(cps),
    ncls] class counts and pairs[len(cps), 3] fair-pair counts at each checkpoint; first_loss[3]: event index (total
    events) at which a fair pair's count first hits zero after having been positive (-1 never; 0 if absent at the
    start).  Returns the total events done."""
    np.random.seed(seed)
    I = tri.shape[0]
    n = NP
    cnt = np.zeros(ncls, np.int64)
    pc = np.zeros(3, np.int64)
    for i in range(I):
        cnt[CLv[tri[i]]] += 1
        if PAIRv[tri[i]] >= 0:
            pc[PAIRv[tri[i]]] += 1
    for q in range(3):
        first_loss[q] = -1
        if pc[q] == 0:
            first_loss[q] = 0
    e = 0
    for ci in range(cps.shape[0]):
        tgt = cps[ci] * I
        while e < tgt:
            i = np.random.randint(I)
            j = np.random.randint(I - 1)
            if j >= i:
                j += 1
            s = np.random.randint(3)
            tj = tri[j]
            ti = tri[i]
            e += 1
            if s == 0:
                x = tj // (n * n)
                r = ti // (n * n)
                if x == r:
                    continue
                pf = PF[0, ti // (n * n), (ti // n) % n, ti % n, x]
                tn = x * n * n + ti % (n * n)
            elif s == 1:
                x = (tj // n) % n
                r = (ti // n) % n
                if x == r:
                    continue
                pf = PF[1, ti // (n * n), (ti // n) % n, ti % n, x]
                tn = (ti // (n * n)) * n * n + x * n + ti % n
            else:
                x = tj % n
                r = ti % n
                if x == r:
                    continue
                pf = PF[2, ti // (n * n), (ti // n) % n, ti % n, x]
                tn = (ti // n) * n + x
            if np.random.random() < pf:
                tri[i] = tn
                oc = CLv[ti]; nc = CLv[tn]
                if oc != nc:
                    cnt[oc] -= 1; cnt[nc] += 1
                op = PAIRv[ti]; np_ = PAIRv[tn]
                if op != np_:
                    if op >= 0:
                        pc[op] -= 1
                        if pc[op] == 0 and first_loss[op] < 0:
                            first_loss[op] = e
                    if np_ >= 0:
                        pc[np_] += 1
        for z in range(ncls):
            hist[ci, z] = cnt[z]
        for q in range(3):
            pairs[ci, q] = pc[q]
    return e


def run_world(PF, tabs, tri0, cps, seed):
    """run one world from the initial triple indices tri0 (copied); returns dict of numpy arrays."""
    tri = np.array(tri0, np.int64)
    cps = np.asarray(cps, np.int64)
    hist = np.zeros((len(cps), M.NCLS), np.int64)
    pairs = np.zeros((len(cps), 3), np.int64)
    fl = np.zeros(3, np.int64)
    e = world_run(PF, tri, cps, int(seed) % (2 ** 31), tabs.CL.ravel().astype(np.int64), tabs.PAIR.ravel().astype(np.int64),
                  hist, pairs, fl, M.NCLS)
    return dict(hist=hist, pairs=pairs, first_loss=fl, events=int(e), final=tri)


def sample_world(hist_counts, I, rng):
    """I islands drawn iid from the pooled settled-triple histogram."""
    p = np.asarray(hist_counts, np.float64)
    p = p / p.sum()
    return rng.choice(len(p), size=I, p=p).astype(np.int64)
