"""The exact mean-field equation of the rare-migration jump chain on triples (islands -> infinity first), for the arm-T
kernel of many_islands_t.  State: x over the 27^3 triples (flattened [a0, a1, a2]); time: migrant events per island.

dx_c/dt = sum_s (1/3) sum_{a, y: a with slot s := y = c, a != c} x_a q_s(y) PF[s, a, y] - x_c sum_s (1/3) sum_y q_s(y) PF[s, c, y],
q_s the slot-s marginal of x (the donors), PF the closed-form Moran fixation tensor.

Contents: symmetry (cyclic rotations), outcome-class shares and tilts, the right-hand side and its directional
derivative (F is quadratic), explicit adaptive and backward-Euler integrators, the Jacobian on the rotation sectors.
"""
import os, sys, math
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import many_islands_t as M

NP = M.NP
NT = M.NT
NCLS = M.NCLS

# ====================================================================== state vectors and symmetry
_TR = np.array([(a0, a1, a2) for a0 in range(NP) for a1 in range(NP) for a2 in range(NP)], np.int64)
ROT1 = (_TR[:, 2] * NP + _TR[:, 0]) * NP + _TR[:, 1]       # index of R t, with R (a0, a1, a2) = (a2, a0, a1)
ROT2 = ROT1[ROT1]
ISFIX = (ROT1 == np.arange(NT))                             # the triples (a, a, a)


def tidx(a0, a1, a2):
    return (a0 * NP + a1) * NP + a2


def hist_to_x(hist):
    x = np.asarray(hist, np.float64).ravel()
    return x / x.sum()


def rot_apply(x, k):
    """(R^k x)[R^k t] = x[t]."""
    y = np.empty_like(x)
    y[ROT1 if k == 1 else ROT2] = x
    return y


def symmetrize(x):
    """average over the three cyclic rotations of the slots."""
    return (x + rot_apply(x, 1) + rot_apply(x, 2)) / 3.0


def class_shares(x, tabs, detail=False):
    """shares of F (all fair pairs), U, G, W, D; detail also returns the three fair pairs separately."""
    out = np.bincount(tabs.CL.ravel(), weights=x, minlength=NCLS)
    if not detail:
        return out
    pr = tabs.PAIR.ravel()
    pairs = np.array([x[pr == i].sum() for i in range(3)])
    return out, pairs


def marginals(x):
    X = x.reshape(NP, NP, NP)
    return np.stack([X.sum(axis=(1, 2)), X.sum(axis=(0, 2)), X.sum(axis=(0, 1))])


def reader_marginals(x, tabs):
    return (marginals(x) * tabs.is_reader[None, :]).sum(axis=1)


def tilt(x, tabs, kind, target=0.6):
    """rescale the outcome-class shares of x to the target, keeping within-class frequencies and the ratios among the
    other classes: 'fair' F -> target; 'unequal' U -> target; 'wd' W + D -> target (their ratio kept).  Returns (x', info);
    x' is None when the tilted classes (or all the others) have no mass."""
    sh = class_shares(x, tabs)
    cl = tabs.CL.ravel()
    sel = {'fair': [0], 'unequal': [1], 'wd': [3, 4]}[kind]
    rest = [c for c in range(NCLS) if c not in sel]
    m_t = float(sh[sel].sum()); m_r = float(sh[rest].sum())
    if m_t <= 0 or m_r <= 0:
        return None, dict(kind=kind, available=False, before=sh.tolist())
    f = np.ones(NCLS)
    for c in sel:
        f[c] = target / m_t
    for c in rest:
        f[c] = (1.0 - target) / m_r
    y = x * f[cl]
    return y, dict(kind=kind, available=True, before=sh.tolist(), after=class_shares(y, tabs).tolist())


# ====================================================================== the right-hand side
@njit(cache=True)
def _rhs_bi(Z, q, PF, out):
    """out += flux with recipient mass Z (n^3) and donor marginals q (3, n)."""
    n = q.shape[1]
    third = 1.0 / 3.0
    for a0 in range(n):
        for a1 in range(n):
            for a2 in range(n):
                t = (a0 * n + a1) * n + a2
                z = Z[t]
                if z == 0.0:
                    continue
                tot = 0.0
                for y in range(n):
                    f = z * q[0, y] * PF[0, a0, a1, a2, y] * third
                    out[(y * n + a1) * n + a2] += f
                    tot += f
                    f = z * q[1, y] * PF[1, a0, a1, a2, y] * third
                    out[(a0 * n + y) * n + a2] += f
                    tot += f
                    f = z * q[2, y] * PF[2, a0, a1, a2, y] * third
                    out[(a0 * n + a1) * n + y] += f
                    tot += f
                out[t] -= tot


@njit(cache=True)
def _marg(x, n):
    q = np.zeros((3, n))
    for a0 in range(n):
        for a1 in range(n):
            for a2 in range(n):
                v = x[(a0 * n + a1) * n + a2]
                q[0, a0] += v; q[1, a1] += v; q[2, a2] += v
    return q


def F_of(x, PF, sym=False):
    out = np.zeros_like(x)
    _rhs_bi(x, _marg(x, NP), PF, out)
    if sym:
        out = (out + rot_apply(out, 1) + rot_apply(out, 2)) / 3.0
    return out


def jvp(x, v, PF, q=None, sym=False):
    """directional derivative of F at x along v (F is quadratic: dF = G(v; q(x)) + G(x; q(v)))."""
    if q is None:
        q = _marg(x, NP)
    out = np.zeros_like(x)
    _rhs_bi(v, q, PF, out)
    _rhs_bi(x, _marg(v, NP), PF, out)
    if sym:
        out = (out + rot_apply(out, 1) + rot_apply(out, 2)) / 3.0
    return out


@njit(cache=True)
def outflow_rate(x, PF):
    """lambda_t = (1/3) sum_s sum_y q_s(y) PF[s, t, y] for every triple: the exit rate of an island in state t."""
    n = PF.shape[1]
    q = _marg(x, n)
    lam = np.zeros(n * n * n)
    for a0 in range(n):
        for a1 in range(n):
            for a2 in range(n):
                tot = 0.0
                for y in range(n):
                    tot += q[0, y] * PF[0, a0, a1, a2, y] + q[1, y] * PF[1, a0, a1, a2, y] + q[2, y] * PF[2, a0, a1, a2, y]
                lam[(a0 * n + a1) * n + a2] = tot / 3.0
    return lam


# ====================================================================== integrators
def checkpoint_grid(tmax):
    g = [0.0]
    e = 0
    while 10.0 ** e <= tmax * (1 + 1e-12):
        for m in (1, 2, 5):
            t = m * 10.0 ** e
            if t <= tmax * (1 + 1e-12):
                g.append(t)
        e += 1
    return g


def _record(t, x, PF, tabs, sym, extra=None):
    sh, pairs = class_shares(x, tabs, True)
    Fx = F_of(x, PF, sym)
    r = dict(t=float(t), shares=sh.tolist(), pairs=pairs.tolist(), readers=reader_marginals(x, tabs).tolist(),
             resid=float(np.abs(Fx).sum()), minx=float(x.min()), mass=float(x.sum()))
    if extra:
        r.update(extra)
    return r


def _converged(recs, t, sh, resid):
    """criterion (a): ||dx/dt||_1 < 1e-9 and every class share changed by < 1e-4 over the last decade of events."""
    if resid >= 1e-9 or t < 1e3:
        return False
    best = None
    for r in recs:
        if abs(r['t'] - t / 10.0) < 0.3 * t / 10.0 and (best is None or abs(r['t'] - t / 10.0) < abs(best['t'] - t / 10.0)):
            best = r
    if best is None:
        return False
    return float(np.abs(np.array(best['shares']) - np.array(sh)).max()) < 1e-4


def integrate(x0, PF, tmax, tabs, sym=True, rtol=1e-8, atol=1e-14, grid=None, method='DOP853', stop_converged=True,
              keep_x_at=(), verbose=False):
    """explicit adaptive integration from x0 to tmax events per island, recording at checkpoints.  sym=True projects the
    vector field on the rotation-invariant subspace at every evaluation.  Returns (records, x_end, status, kept)."""
    from scipy.integrate import solve_ivp
    grid = checkpoint_grid(tmax) if grid is None else list(grid)
    x = x0.copy()
    recs = [_record(0.0, x, PF, tabs, sym)]
    kept = {}
    status = 'horizon'
    fun = lambda t, y: F_of(y, PF, sym)
    for i in range(1, len(grid)):
        t0, t1 = grid[i - 1], grid[i]
        sol = solve_ivp(fun, (t0, t1), x, method=method, rtol=rtol, atol=atol)
        x = sol.y[:, -1]
        r = _record(t1, x, PF, tabs, sym, dict(nfev=int(sol.nfev)))
        recs.append(r)
        if t1 in keep_x_at:
            kept[t1] = x.copy()
        if verbose:
            print('t=%g shares=%s resid=%.2e nfev=%d' % (t1, np.round(r['shares'], 4), r['resid'], sol.nfev), flush=True)
        if stop_converged and _converged(recs, t1, r['shares'], r['resid']):
            status = 'converged'
            break
    return recs, x, status, kept


def be_step(x, h, PF, sym=True, max_newton=5, gm_tol=1e-9, gm_restart=50, gm_maxiter=30):
    """one backward-Euler step x' = x + h F(x') by Newton with matrix-free GMRES and a diagonal preconditioner."""
    from scipy.sparse.linalg import LinearOperator, gmres
    xn = x.copy()
    n = x.size
    its = 0
    gits = 0
    for it in range(max_newton):
        R = xn - x - h * F_of(xn, PF, sym)
        rn = float(np.abs(R).sum())
        if rn < 1e-13:
            break
        q = _marg(xn, NP)
        lam = outflow_rate(xn, PF)
        Minv = 1.0 / (1.0 + h * lam)
        A = LinearOperator((n, n), matvec=lambda v: v - h * jvp(xn, v, PF, q, sym), dtype=np.float64)
        M_ = LinearOperator((n, n), matvec=lambda v: Minv * v, dtype=np.float64)
        try:
            d, info = gmres(A, -R, M=M_, rtol=gm_tol, atol=0.0, restart=gm_restart, maxiter=gm_maxiter)
        except TypeError:
            d, info = gmres(A, -R, M=M_, tol=gm_tol, atol=0.0, restart=gm_restart, maxiter=gm_maxiter)
        its += 1
        xn = xn + d
        if float(np.abs(d).sum()) < 1e-13:
            break
    R = xn - x - h * F_of(xn, PF, sym)
    return xn, dict(newton=its, resid=float(np.abs(R).sum()))


def integrate_be(x, t0, PF, tabs, tmax, sym=True, steps_per_decade=8, recs=None, verbose=False):
    """backward-Euler continuation from t0 to tmax (geometric steps); returns (records, x, status)."""
    recs = [] if recs is None else recs
    t = t0
    status = 'horizon'
    ratio = 10.0 ** (1.0 / steps_per_decade)
    h = max(t0 * (ratio - 1.0), 1.0)
    while t < tmax * (1 - 1e-12):
        h = min(h, tmax - t)
        for attempt in range(14):
            xn, info = be_step(x, h, PF, sym)
            if xn.min() > -1e-10 and info['resid'] < 1e-9:
                break
            h *= 0.5                      # the implicit equation is quadratic: a large step can land on a spurious root
        x = xn
        t += h
        r = _record(t, x, PF, tabs, sym, dict(newton=info['newton'], be_resid=info['resid'], solver='be'))
        recs.append(r)
        if verbose:
            print('BE t=%.4g shares=%s resid=%.2e newton=%d' % (t, np.round(r['shares'], 4), r['resid'], info['newton']), flush=True)
        if _converged(recs, t, r['shares'], r['resid']):
            status = 'converged'
            break
        h *= ratio
    return recs, x, status
