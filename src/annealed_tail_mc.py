"""Pool Monte Carlo of the jump chain with an annealed prior tail (V3 of the annealed-tail spec).  A copy of
unequal_basin_mc.chain_run2 with prior arrivals added: after each migrant event, Poisson(eps(t)) tail arrivals, each to a uniform
island and slot, the program drawn from the slot's founding prior, fixing with the same exact Moran probability."""
import os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import many_islands as MI
import unequal_basin_core as UC

DMAX = 23


@njit(cache=True)
def chain_tail(C, PAY2, VEC2, pool, code, oc, e0, events, seed, PF30, cum, Lam, t0, tail_on):
    """advance the pool by `events` migrant events starting at event count e0 (time t = e / I); state in pool/code/oc."""
    np.random.seed(seed)
    I = pool.shape[0]
    K = cum.shape[1]
    e = 0
    n_tail = 0
    n_tail_fix = 0
    while e < events:
        i = np.random.randint(I)
        j = np.random.randint(I - 1)
        if j >= i:
            j += 1
        s = np.random.randint(3)
        x = pool[j, s]
        e += 1
        if x != pool[i, s]:
            if s == 0:
                cx = UC.jl2(C, x, pool[i, 1], pool[i, 2])
            elif s == 1:
                cx = UC.jl2(C, pool[i, 0], x, pool[i, 2])
            else:
                cx = UC.jl2(C, pool[i, 0], pool[i, 1], x)
            d = int(np.rint(30.0 * (PAY2[cx, s] - PAY2[code[i], s])))
            pf = PF30[d + DMAX]
            if pf > 1e-12 and np.random.random() < pf:
                pool[i, s] = x
                code[i] = cx
                oc[i] = VEC2[cx]
        if tail_on:
            t = (e0 + e) / I
            eps = Lam / t0 / (1.0 + t / t0) ** 2
            k = np.random.poisson(eps)
            for _ in range(k):
                i = np.random.randint(I)
                s = np.random.randint(3)
                u = np.random.random()
                lo = 0
                hi = K - 1
                while lo < hi:
                    mid = (lo + hi) // 2
                    if cum[s, mid] < u:
                        lo = mid + 1
                    else:
                        hi = mid
                y = lo
                n_tail += 1
                if y == pool[i, s]:
                    continue
                if s == 0:
                    cx = UC.jl2(C, y, pool[i, 1], pool[i, 2])
                elif s == 1:
                    cx = UC.jl2(C, pool[i, 0], y, pool[i, 2])
                else:
                    cx = UC.jl2(C, pool[i, 0], pool[i, 1], y)
                d = int(np.rint(30.0 * (PAY2[cx, s] - PAY2[code[i], s])))
                pf = PF30[d + DMAX]
                if pf > 1e-12 and np.random.random() < pf:
                    pool[i, s] = y
                    code[i] = cx
                    oc[i] = VEC2[cx]
                    n_tail_fix += 1
    return n_tail, n_tail_fix


def run_mc_tail(armname, pfail, triples, cps, seed, Lam, t0, quiet=True, PF30=None):
    arm = MI.Arm(armname)
    arm.new_cache(26)
    PAY2, VEC2 = UC.tables2(pfail)
    if PF30 is None:
        PF30 = np.array([MI.pfix(d / 30.0, float(MI.N0), float(MI.W)) for d in range(-DMAX, DMAX + 1)])
    pool = np.ascontiguousarray(triples.copy())
    I = len(pool)
    C = arm.ctx()
    code = np.zeros(I, np.int64)
    oc = np.zeros(I, np.int64)
    for i in range(I):
        code[i] = UC.jl2(C, pool[i, 0], pool[i, 1], pool[i, 2])
        oc[i] = VEC2[code[i]]
    cum = np.ascontiguousarray(arm.cum)
    hist = np.zeros((len(cps), MI.NOUT), np.int64)
    prev = 0
    rs = seed
    tot_tail = tot_fix = 0
    for k, c in enumerate(cps):
        todo = int(c) * I - prev
        while todo > 0:
            piece = min(5_000_000, todo)
            arm.maybe_flush(0.5)
            C = arm.ctx()
            rs = (rs * 1103515245 + 12345) % (2 ** 31)
            nt, nf = chain_tail(C, PAY2, VEC2, pool, code, oc, prev, piece, rs, PF30, cum, float(Lam), float(t0), Lam > 0)
            tot_tail += nt
            tot_fix += nf
            prev += piece
            todo -= piece
        h = np.zeros(MI.NOUT, np.int64)
        for i in range(I):
            h[oc[i]] += 1
        hist[k] = h
    return hist, dict(n_tail=int(tot_tail), n_tail_fix=int(tot_fix))
