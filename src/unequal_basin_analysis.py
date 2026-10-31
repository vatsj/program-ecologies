"""Static analyses at an endpoint of the unequal-basin object: roles, program-by-role association, rescue moves, the
U -> V* flux decomposition, the Jacobian (spec Questions 2-4).  Works on an Obj and a state x (from the endpoint npz)."""
import os, sys, json, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import dollar3 as D
import many_islands as MI
import unequal_basin as UB

ROLE = ['high', 'low', 'excl', 'n/a']


def roles(obj):
    """role[s, t] of slot s in state t: 0 high demander, 1 low demander (unequal pair), 2 excluded slot, 3 not an unequal pair
    (fair, grand, wasteful, disagreement states).  Fair pairs get 0/0 'pair' tagged 4/4 and 2 excluded in rolesF."""
    n = obj.n
    r = np.full((3, n), 3, np.int8)
    U = obj.cl == 1
    ex = obj.excl
    for s in range(3):
        r[s, U & (ex == s)] = 2
    for s in range(3):
        pair_s = U & (ex != s)
        other = np.zeros(n, np.int64)
        # the other pair member: the slot that is neither s nor the excluded
        o = 3 - s - np.where(ex >= 0, ex, 0)
        lev_s = obj.lev[s].astype(np.int64)
        lev_o = np.take_along_axis(obj.lev.astype(np.int64), np.clip(o, 0, 2)[None, :], axis=0)[0]
        hi = pair_s & (lev_s > lev_o)
        lo = pair_s & (lev_s < lev_o)
        r[s, hi] = 0
        r[s, lo] = 1
    return r


def program_role_assoc(obj, x, slot=0):
    """for slot `slot`: mass of each program in each role over the U states (and in F states and elsewhere):
    dict program -> [high, low, excl, in_F, other].  By S3 symmetry of a symmetric x the choice of slot is immaterial up to the
    program relabelling."""
    r = roles(obj)
    out = np.zeros((UB.KP, 5))
    for k in range(3):
        sel = r[slot] == k
        out[:, k] = np.bincount(obj.pid[slot], weights=x * sel, minlength=UB.KP)
    out[:, 3] = np.bincount(obj.pid[slot], weights=x * (obj.cl == 0), minlength=UB.KP)
    out[:, 4] = np.bincount(obj.pid[slot], weights=x * ((obj.cl != 0) & (r[slot] == 3)), minlength=UB.KP)
    return out


def top_classes(obj, x, slot=0, mass_min=1e-3, top=20):
    q = obj.marg(x)[slot]
    assoc = program_role_assoc(obj, x, slot)
    idx = [int(i) for i in np.argsort(-q) if q[i] >= mass_min][:top]
    rows = []
    for i in idx:
        rows.append(dict(prog=i, src=obj.arm.name_of(slot, i), conditional=bool(not obj.isc[i]), mass=float(q[i]),
                         high=float(assoc[i, 0]), low=float(assoc[i, 1]), excl=float(assoc[i, 2]), in_F=float(assoc[i, 3]),
                         other=float(assoc[i, 4])))
    return rows, int((q >= mass_min).sum())


@njit(cache=True)
def _flux_by(x, q, ordA, fstA, nfib, lev, pid, cl, role, PF, src_mask, dst_mask, out):
    """out[s_role, y] += (1/3) x_t q_s(y) PF over states t with cl in src (mask) moving to the fibre member (y, ctx) with
    cl in dst (mask): the flux of migrant program y into recipient role r.  Roles are those of the source state."""
    third = 1.0 / 3.0
    for s in range(3):
        for f in range(nfib[s]):
            a = fstA[s, f]
            b = fstA[s, f + 1]
            for ja in range(a, b):
                t = ordA[s, ja]
                if not src_mask[cl[t]] or x[t] == 0.0:
                    continue
                lt = lev[s, t]
                r = role[s, t]
                for jb in range(a, b):
                    u = ordA[s, jb]
                    if u == t or not dst_mask[cl[u]]:
                        continue
                    y = pid[s, u]
                    out[r, y] += third * x[t] * q[s, y] * PF[lev[s, u] - lt + UB.DMAX]


def flux_decomposition(obj, x, src=(1,), dst=(0,)):
    """flux per event per island from classes src to classes dst by (recipient role in the source state, migrant program).
    Returns a (4, KP) array (roles high, low, excl, n/a)."""
    q = obj.marg(x)
    r = roles(obj)
    sm = np.zeros(5, np.bool_); dm = np.zeros(5, np.bool_)
    for c in src: sm[c] = True
    for c in dst: dm[c] = True
    out = np.zeros((4, UB.KP))
    _flux_by(x, q, obj.ordA, obj.fstA, obj.nfib, obj.lev, obj.pid, obj.cl.astype(np.int64), r.astype(np.int64), UB.PF30, sm, dm, out)
    return out


def class_flux_matrix(obj, x):
    """5 x 5 matrix of class-to-class flux per event per island (all migrant programs)."""
    M = np.zeros((5, 5))
    for a in range(5):
        for b in range(5):
            if a == b:
                continue
            M[a, b] = flux_decomposition(obj, x, (a,), (b,)).sum()
    return M


def dominant_triples(obj, x, cls=1, top=6, slot_excl=None):
    sel = np.nonzero(obj.cl == cls)[0]
    o = sel[np.argsort(-x[sel])][:top]
    return o


def moves_from(obj, x, t, q=None):
    """every single-migrant move out of the state index t: (slot, migrant program, payoff change in 1/30, new class, P_fix, flux
    (1/3) x_t q_s(y) P_fix) over the migrants y with q_s(y) > 0 that give an allowed state."""
    if q is None:
        q = obj.marg(x)
    rows = []
    T = obj.T[t].astype(np.int64)
    for s in range(3):
        for y in obj.supp[s]:
            if y == T[s] or q[s, y] <= 0:
                continue
            T2 = T.copy(); T2[s] = y
            p, ok = obj.index_of(T2[None, :])
            if not ok[0]:
                continue
            p = int(p[0])
            d = int(obj.lev[s, p]) - int(obj.lev[s, t])
            pf = float(UB.PF30[d + UB.DMAX])
            rows.append(dict(slot=s, prog=int(y), dl=d, new_cl=int(obj.cl[p]), pfix=pf, q=float(q[s, y]), flux=float(x[t] * q[s, y] * pf / 3.0)))
    return rows
