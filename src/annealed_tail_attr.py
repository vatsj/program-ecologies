"""Flux attribution of the tail (spec cell 5): class-changing flux, by source class, destination class, arriving family, the
arrival slot's role in the source state, and the source category (is the excluded slot of a U source holding an offering constant).

For a fibre (slot s, context) with members t, the Moran flux from member a to member b != a is
    x_a (1/3) q_s(y_b) PF[l_b - l_a],
so grouping the sources by (level, class, role, category) gives all fluxes of the fibre in O(members x groups).  The same kernel is
applied with q = p (the tail's arrivals, unit rate) and with q = the state's marginals (migrants).

Families of the arriving program y in slot s: 0..8 the nine constants (index = the constant's id; its meaning in slot s is
`const_table`), 9 exploiter-fair (Trojan bully), 10 exploiter, 11 yielder, 12 fair-reader, 13 other conditional.
Roles of slot s in the source state: 0 no pair, 1 member of a fair or wasteful pair, 2 high member of an unequal pair, 3 low member,
4 the excluded slot of a pair outcome.  Category: 1 for a U source whose excluded slot holds a constant naming the low member at
demand <= 1/2 (an offering constant), 2 for the other U sources, 0 for non-U sources.
"""
import os, sys, json
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import dollar3 as D
import unequal_basin as UB
import unequal_basin_run as R
import annealed_tail as A

NFAM = 14
NROLE = 5
NCAT = 3
NKEY = 5 * NROLE * NCAT
SHAPE = (5, 5, NFAM, NROLE, NCAT)
FAMNAMES = ['c%d' % i for i in range(9)] + ['bully', 'exploiter', 'yielder', 'fair-reader', 'other-cond']


def attr_arrays(cell, obj):
    arm = cell.arm
    isc = cell.isc
    K = UB.KP
    fam = np.full((3, K), 13, np.int64)
    for s in range(3):
        for x in range(K):
            if isc[x]:
                fam[s, x] = x
    for nm, code in (('exploiter-fair', 9), ('exploiter', 10), ('yielder', 11), ('fair-reader', 12)):
        m = R.family_mask(arm, nm)
        for s in range(3):
            fam[s, m[s]] = code
    n = obj.n
    role = np.zeros((3, n), np.int8)
    cat = np.zeros(n, np.int8)
    lev = obj.lev.astype(np.int64)
    excl = obj.excl
    cl = obj.cl
    # constant local actions
    cact = np.full(K, -1, np.int64)
    for x in range(K):
        if isc[x]:
            cact[x] = int(arm.S.fs[x][1][0])
    for s in range(3):
        ex = excl == s
        role[s, ex] = 4
        has = (excl >= 0) & ~ex
        role[s, has & ((cl == 0) | (cl == 3))] = 1
        # unequal: compare with the other pair member

    # high / low members of U states
    Uidx = np.nonzero((cl == 1) & (excl >= 0))[0]
    if len(Uidx):
        e = excl[Uidx]
        pay = lev[:, Uidx]                       # (3, m)
        pr = np.where(np.arange(3)[:, None] == e[None, :], -99, pay)
        hi = np.argmax(pr, axis=0)
        pr2 = np.where(np.arange(3)[:, None] == e[None, :], 99, pay)
        lo = np.argmin(pr2, axis=0)
        role[hi, Uidx] = 2
        role[lo, Uidx] = 3
        # category: excluded slot's program is a constant naming the low member at demand <= 1/2
        pid = obj.pid
        for k, t in enumerate(Uidx):
            ee = int(e[k])
            y = int(pid[ee, t])
            c = 2
            if isc[y]:
                l = cact[y]
                if D.partner_abs(ee, l) == int(lo[k]) and (l % 3) <= 1:
                    c = 1
            cat[t] = c
    return dict(fam=fam, role=role, cat=cat)


@njit(cache=True)
def _attr(x, q, ordA, fstA, nfib, lev, pid, cl, fam, role, cat, PF, out):
    third = 1.0 / 3.0
    xk = np.zeros(NLEV_ * NKEY)
    mark = np.zeros(NLEV_ * NKEY, np.int8)
    present = np.zeros(NLEV_ * NKEY, np.int64)
    for s in range(3):
        for f in range(nfib[s]):
            a = fstA[s, f]
            b = fstA[s, f + 1]
            if b - a < 2:
                continue
            npres = 0
            for j in range(a, b):
                t = ordA[s, j]
                if x[t] == 0.0:
                    continue
                key = (np.int64(cl[t]) * 5 + np.int64(role[s, t])) * 3 + np.int64(cat[t])
                idx = np.int64(lev[s, t]) * NKEY + key
                if mark[idx] == 0:
                    mark[idx] = 1
                    present[npres] = idx
                    npres += 1
                xk[idx] += x[t]
            if npres > 0:
                for j in range(a, b):
                    t = ordA[s, j]
                    qb = q[s, pid[s, t]]
                    if qb == 0.0:
                        continue
                    lb = np.int64(lev[s, t])
                    cb = np.int64(cl[t])
                    fb = np.int64(fam[s, pid[s, t]])
                    for k in range(npres):
                        idx = present[k]
                        v = idx // NKEY
                        key = idx % NKEY
                        ca = key // 15
                        if ca == cb:
                            continue
                        r = (key // 3) % 5
                        sc = key % 3
                        out[ca, cb, fb, r, sc] += xk[idx] * PF[lb - v + DMAX_] * qb * third
            for k in range(npres):
                idx = present[k]
                xk[idx] = 0.0
                mark[idx] = 0


NLEV_ = UB.NLEV
DMAX_ = UB.DMAX


def flux_tensor(S, arrs, x, q):
    out = np.zeros(SHAPE)
    o = S.obj
    _attr(x, q, o.ordA, o.fstA, o.nfib, o.lev, o.pid, o.cl, arrs['fam'], arrs['role'], arrs['cat'], S.PF, out)
    return out


def fine_grid(lo_exp=-2.0, hi_exp=4.0, per_decade=12):
    k0, k1 = int(round(lo_exp * per_decade)), int(round(hi_exp * per_decade))
    return [10.0 ** (k / float(per_decade)) for k in range(k0, k1 + 1)]


def run_attr(S, cell, x0, sched, tmax=1e5, snaps=(1e2, 1e3, 1e4, 1e5), spd=16):
    """integrate with a flux callback; returns dict(tail=snapshots of the integrated direct tail flux, mig=the same for migrants)."""
    arrs = attr_arrays(cell, S.obj)
    st = dict(prev_t=None, prev_ft=None, prev_fm=None, acc_t=np.zeros(SHAPE), acc_m=np.zeros(SHAPE))
    snapshots = {}
    pending = sorted(snaps)

    def cb(tau, x):
        e = sched.eps(tau)
        ft = flux_tensor(S, arrs, x, S.p) * e if e > 0 else np.zeros(SHAPE)
        fm = flux_tensor(S, arrs, x, S.obj.marg(x))
        if st['prev_t'] is not None:
            dt = tau - st['prev_t']
            st['acc_t'] += 0.5 * (st['prev_ft'] + ft) * dt
            st['acc_m'] += 0.5 * (st['prev_fm'] + fm) * dt
        st['prev_t'], st['prev_ft'], st['prev_fm'] = tau, ft, fm
        while pending and tau >= pending[0] * (1 - 1e-9):
            snapshots[pending[0]] = (st['acc_t'].copy(), st['acc_m'].copy())
            pending.pop(0)

    recs, x, status, _ = A.integrate(S, x0, sched, 0.0, tmax, 1e4, spd, False, cb=cb, explicit_grid=[0.0] + fine_grid(), stop_stationary=False)
    out = dict(status=status, shares_end=recs[-1]['shares'], snaps={})
    for s, (t, m) in snapshots.items():
        out['snaps'][str(int(s))] = dict(tail=_sparse(t), mig=_sparse(m))
    out['famnames'] = FAMNAMES
    out['shape'] = SHAPE
    return out


def _sparse(T, thr=1e-13):
    idx = np.argwhere(np.abs(T) > thr)
    return [[int(v) for v in i] + [float('%.6e' % T[tuple(i)])] for i in idx]
