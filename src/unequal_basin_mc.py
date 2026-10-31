"""Pool Monte Carlo of the jump chain over the extended joint code (divergence-aware), for the matched Monte Carlo of V3 and
the crossed-charge checks.  A copy of many_islands.chain_run with jl2 / PAY2 / VEC2 and the exact 1/30-dollar fixation table.
Nothing existing is edited."""
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
def chain_run2(C, PAY2, VEC2, pool, events_total, seed, PF30, hist_out, isc, mmax):
    """I = len(pool) islands (one component); `events_total` events (recipient uniform, donor uniform among the others, slot
    uniform; the migrant fixes with the exact Moran probability).  hist_out[NOUT] is overwritten with the outcome counts at
    the end.  mmax < 3: the reflecting truncation of the ODE object (a migration that would give the island more than
    mmax conditional programs is a null event); mmax >= 3: the full dynamics."""
    np.random.seed(seed)
    I = pool.shape[0]
    code = np.zeros(I, np.int64)
    oc = np.zeros(I, np.int64)
    for i in range(I):
        code[i] = UC.jl2(C, pool[i, 0], pool[i, 1], pool[i, 2])
        oc[i] = VEC2[code[i]]
    e = 0
    while e < events_total:
        i = np.random.randint(I)
        j = np.random.randint(I - 1)
        if j >= i:
            j += 1
        s = np.random.randint(3)
        x = pool[j, s]
        e += 1
        if x == pool[i, s]:
            continue
        if mmax < 3:
            nc = 0
            for r in range(3):
                v = x if r == s else pool[i, r]
                if not isc[v]:
                    nc += 1
            if nc > mmax:
                continue
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
    for z in range(hist_out.shape[0]):
        hist_out[z] = 0
    for i in range(I):
        hist_out[oc[i]] += 1
    return e


def run_mc(armname, pfail, triples, cps, seed, quiet=True, mmax=3):
    """run the chain on `triples` (I, 3) to each checkpoint (events per island, ascending); returns hist (ncp, NOUT) and wall."""
    arm = MI.Arm(armname)
    arm.new_cache(26)
    PAY2, VEC2 = UC.tables2(pfail)
    PF30 = np.array([MI.pfix(d / 30.0, float(MI.N0), float(MI.W)) for d in range(-DMAX, DMAX + 1)])
    pool = np.ascontiguousarray(triples.copy())
    isc = np.ascontiguousarray(np.asarray(arm.S.nat)[0] == 0)
    I = len(pool)
    hist = np.zeros((len(cps), MI.NOUT), np.int64)
    prev = 0
    t0 = time.time()
    rs = seed
    for k, c in enumerate(cps):
        todo = int(c) * I - prev
        while todo > 0:
            piece = min(20_000_000, todo)
            arm.maybe_flush(0.5)
            h = np.zeros(MI.NOUT, np.int64)
            rs = (rs * 1103515245 + 12345) % (2 ** 31)
            chain_run2(arm.ctx(), PAY2, VEC2, pool, piece, rs, PF30, h, isc, np.int64(mmax))
            prev += piece
            todo -= piece
        hist[k] = h
        if not quiet:
            print('  checkpoint %s: %.0f s' % (c, time.time() - t0), flush=True)
    return hist, time.time() - t0
