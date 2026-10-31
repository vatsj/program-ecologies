"""The mean-field object of the unequal-basin experiment (spec specs/2026-10-31-unequal-basin.md; notes notes/unequal-basin.md).

The exact I -> infinity dynamics of the rare-migration jump chain on settled program triples of the DSL arms L (weak) and M
(modalPA), as in the arm-T ODE (many_islands_t_ode.py), started from the post-anneal law of the pools:

    dx_t/dt = (1/3) sum_s [ q_s(t_s) m_f(l_s(t)) - x_t lam_f(l_s(t)) ],      f = the fibre (s, context of t),
    m_f(l)   = sum_v xlev_f(v) PF[l - v],    lam_f(l) = sum_v qlev_f(v) PF[v - l],

where l_s(t) is the integer payoff (in 1/30 dollar) of slot s in triple t, xlev_f(v) the mass of the fibre's triples
with level v, qlev_f(v) the donor mass of the fibre's programs with level v, and PF[d] the Moran fixation probability
of a migrant with payoff advantage d/30 dollars.  This is the exact kernel in O(states) rather than O(states * C)
because a migrant's payoff takes few distinct values within a fibre.

State space.  The spec's dense lumped field has C^3 states with C the class count per slot; notes 1.5 predicts C ~ 1,300
(the lumping is vacuous), so the object computed is the reflecting m-conditional truncation: triples with at most m
conditional programs; a migration that would give an island m + 1 conditionals is a null event (mass conserved), and
its rate is the reported leak.  m = 0 is the constants-only object (arm T's dose 0), m = 3 would be the full thing
on 3 slots.

Time is migrant events per island.  Importable without side effects.
"""
import os, sys, math, time, itertools
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import dollar3 as D
import many_islands as MI
import many_islands_run as MR
import unequal_basin_core as UC

N0 = MI.N0
W = MI.W
NCLS = 5
CLS = ['F', 'U', 'G', 'W', 'D']
NLEV = 24                    # integer payoff (1/30 dollar) in [-3, 20] -> index l + 3
LOFF = 3
KP = 1305

# ---------------------------------------------------------------- fixation table over integer payoff differences
DMAX = 23
PF30 = np.array([MI.pfix(d / 30.0, float(N0), float(W)) for d in range(-DMAX, DMAX + 1)])      # index d + DMAX


def pf30(d):
    return PF30[d + DMAX]


# ---------------------------------------------------------------- the arm and its programs
_ARMS = {}


def get_arm(name):
    if name not in _ARMS:
        a = MI.Arm(name)
        a.new_cache(22)
        _ARMS[name] = a
    return _ARMS[name]


def program_data(arm):
    """nat (3, K): essential atoms of program x in slot s (0 = constant); isc (K,) constant flag (same in every slot)."""
    nat = np.asarray(arm.S.nat)
    isc = (nat[0] == 0)
    assert (isc == (nat[1] == 0)).all() and (isc == (nat[2] == 0)).all()
    return nat, isc


SIGMAS = list(itertools.permutations(range(3)))


def perm_maps(arm):
    """for each sigma in S3: perm[s][x] = image program index in slot sigma[s] of slot s's program x (every program)."""
    out = []
    for sg in SIGMAS:
        p = MI.permute_support(arm, sg)
        out.append((sg, p))
    return out


def image_triples(arm, trip, pm=None):
    """the six S3 images of every triple (rows (n, 3) of program ids), concatenated sigma-major."""
    pm = pm or perm_maps(arm)
    out = []
    for sg, perm in pm:
        img = np.zeros_like(trip)
        for s in range(3):
            img[:, sg[s]] = perm[s][trip[:, s]]
        out.append(img)
    return np.concatenate(out)


def keys_of(T):
    T = np.asarray(T, np.int64)
    return (T[:, 0] * KP + T[:, 1]) * KP + T[:, 2]


# ---------------------------------------------------------------- state enumeration
def enumerate_states(supp, isc, m, core=None):
    """all triples (a0, a1, a2), a_s in supp[s], with at most m conditionals, as an (n, 3) int16 array sorted by key.
    core (optional, one set of program ids per slot): states with two or more conditionals are admitted only if every
    conditional in them is in core[s] of its slot (a core-restricted m = 2 or 3 object)."""
    cons = [np.array([x for x in supp[s] if isc[x]], np.int64) for s in range(3)]
    cond = [np.array([x for x in supp[s] if not isc[x]], np.int64) for s in range(3)]
    if core is None:
        ccond = cond
    else:
        ccond = [np.array([x for x in supp[s] if (not isc[x]) and x in core[s]], np.int64) for s in range(3)]
    parts = []

    def prod(lists):
        g = np.meshgrid(*lists, indexing='ij')
        return np.stack([a.ravel() for a in g], axis=1)

    if m >= 0:
        parts.append(prod(cons))
    if m >= 1:
        for s in range(3):
            lists = [cons[0], cons[1], cons[2]]
            lists[s] = cond[s]
            parts.append(prod(lists))
    if m >= 2:
        for s, t in ((0, 1), (0, 2), (1, 2)):
            lists = [cons[0], cons[1], cons[2]]
            lists[s] = ccond[s]; lists[t] = ccond[t]
            parts.append(prod(lists))
    if m >= 3:
        parts.append(prod(ccond))
    if m > 3:
        raise ValueError(m)
    T = np.concatenate(parts)
    k = keys_of(T)
    o = np.argsort(k)
    return T[o].astype(np.int16)


@njit(cache=True)
def _codes(armi, nat, atL, atJ, atA, tab, PARTNER, T, out):
    hist = np.empty((2, 3), np.int64)
    val = np.empty(3, np.int64)
    for i in range(T.shape[0]):
        out[i] = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, np.int64(T[i, 0]), np.int64(T[i, 1]), np.int64(T[i, 2]), hist, val)


def codes_of(arm, T):
    S = arm.S
    out = np.empty(len(T), np.int64)
    _codes(np.int64(arm.armi), np.ascontiguousarray(S.nat), np.ascontiguousarray(S.atL), np.ascontiguousarray(S.atJ),
           np.ascontiguousarray(S.atA), np.ascontiguousarray(S.tab), np.ascontiguousarray(D.PARTNER), T, out)
    return out


# ---------------------------------------------------------------- the object
class Obj:
    """States, payoff levels, outcome classes and fibre structure of the m-truncated object over the supports supp[s]."""

    def __init__(self, armname, pfail, supp, m, verbose=False, symmetric=True, core=None):
        self.armname = armname
        self.pfail = float(pfail)
        self.arm = get_arm(armname)
        self.nat, self.isc = program_data(self.arm)
        self.supp = [np.array(sorted(set(int(v) for v in sp)), np.int64) for sp in supp]
        self.m = m
        t0 = time.time()
        self.core = core
        self.T = enumerate_states(self.supp, self.isc, m, core)
        self.n = len(self.T)
        self.key = keys_of(self.T)
        code2 = codes_of(self.arm, self.T)
        self.badmodal = int((code2 < 0).sum())
        assert self.badmodal == 0, 'modal evaluator non-convergence on the support'
        PAY2, VEC2 = UC.tables2(self.pfail)
        self.code2 = code2
        self.code = code2 % 729
        self.mask = code2 // 729
        pay = PAY2[code2]                                          # (n, 3)
        li = np.rint(pay * 30.0).astype(np.int64)
        assert np.abs(pay * 30.0 - li).max() < 1e-9
        assert li.min() >= -LOFF and li.max() <= NLEV - 1 - LOFF, (li.min(), li.max())
        self.lev = np.ascontiguousarray((li + LOFF).T.astype(np.int8))                # (3, n)
        out = VEC2[code2]
        self.out = out
        self.cl = MI.CATMAP[out].astype(np.int8)
        self.pair = MI.VIDX[out]
        self.excl = MI.EXCL[out]
        self.pid = np.ascontiguousarray(self.T.T.astype(np.int64))        # (3, n)
        self.ncond = (~self.isc[self.pid]).sum(axis=0)
        # fibres
        self.ord = []
        self.fst = []
        for s in range(3):
            o1, o2 = MI._others(s)
            k = self.T[:, o1].astype(np.int64) * KP + self.T[:, o2]
            o = np.argsort(k, kind='stable')
            ks = k[o]
            b = np.flatnonzero(np.concatenate([[True], ks[1:] != ks[:-1]]))
            self.ord.append(o.astype(np.int64))
            self.fst.append(np.concatenate([b, [self.n]]).astype(np.int64))
        self.ordA = np.ascontiguousarray(np.stack(self.ord))
        self.nfib = np.array([len(f) - 1 for f in self.fst], np.int64)
        self.fstA = np.zeros((3, self.nfib.max() + 1), np.int64)
        for s in range(3):
            self.fstA[s, :self.nfib[s] + 1] = self.fst[s]
        # S3 action on states
        self.pm = perm_maps(self.arm)
        self.perm_idx = []
        if symmetric:
            for sg, perm in self.pm:
                img = np.zeros((self.n, 3), np.int64)
                for s in range(3):
                    img[:, sg[s]] = perm[s][self.T[:, s]]
                ki = keys_of(img)
                pos = np.searchsorted(self.key, ki)
                pos = np.minimum(pos, self.n - 1)
                assert (self.key[pos] == ki).all(), 'state set not S3-closed'
                self.perm_idx.append(pos.astype(np.int64))
        self.symmetric = symmetric
        self.build_time = time.time() - t0
        if verbose:
            print('Obj %s pfail %g m %d: %d states, %.1f s' % (armname, pfail, m, self.n, self.build_time), flush=True)

    # --- state lookup
    def index_of(self, trip):
        k = keys_of(trip)
        pos = np.searchsorted(self.key, k)
        pos = np.minimum(pos, self.n - 1)
        ok = self.key[pos] == k
        return pos, ok

    def start_from_triples(self, trip):
        """empirical start: counts of the given triples on the allowed states (dropped = mass outside the truncation)."""
        pos, ok = self.index_of(trip)
        x = np.bincount(pos[ok], minlength=self.n).astype(np.float64)
        dropped = float(1.0 - ok.mean())
        return x / x.sum(), dropped

    def marg(self, x):
        q = np.zeros((3, KP))
        for s in range(3):
            q[s] = np.bincount(self.pid[s], weights=x, minlength=KP)
        return q

    def class_shares(self, x, detail=False):
        sh = np.bincount(self.cl, weights=x, minlength=NCLS)
        if not detail:
            return sh
        pr = np.array([x[self.pair == i].sum() for i in range(3)])
        return sh, pr

    def sym(self, F):
        if not self.symmetric:
            return F
        out = F.copy()
        for pi in self.perm_idx[1:]:
            out += F[pi]            # image of state t is pi[t]; the invariant average of F is (1/6) sum_sigma F[pi_sigma[t]]
        return out / 6.0


# ---------------------------------------------------------------- the right-hand side
@njit(cache=True)
def _rhs(x, q, ordA, fstA, nfib, lev, pid, PF, out, blocked):
    """out += G(x; q): the flux of the state x with donor marginals q.  blocked is unused here (the reflecting truncation
    is the state set itself); kept for signature stability."""
    third = 1.0 / 3.0
    xl = np.zeros(NLEV)
    ql = np.zeros(NLEV)
    mm = np.zeros(NLEV)
    lm = np.zeros(NLEV)
    pres = np.zeros(NLEV, np.int64)
    for s in range(3):
        for f in range(nfib[s]):
            a = fstA[s, f]
            b = fstA[s, f + 1]
            for l in range(NLEV):
                xl[l] = 0.0
                ql[l] = 0.0
            for j in range(a, b):
                t = ordA[s, j]
                l = lev[s, t]
                xl[l] += x[t]
                ql[l] += q[s, pid[s, t]]
            npr = 0
            for l in range(NLEV):
                if xl[l] != 0.0 or ql[l] != 0.0:
                    pres[npr] = l
                    npr += 1
            for ii in range(npr):
                l = pres[ii]
                sm = 0.0
                sl = 0.0
                for jj in range(npr):
                    v = pres[jj]
                    sm += xl[v] * PF[l - v + DMAX]
                    sl += ql[v] * PF[v - l + DMAX]
                mm[l] = sm
                lm[l] = sl
            for j in range(a, b):
                t = ordA[s, j]
                l = lev[s, t]
                out[t] += third * (q[s, pid[s, t]] * mm[l] - x[t] * lm[l])


def field(obj, x, sym=True, q=None):
    out = np.zeros(obj.n)
    if q is None:
        q = obj.marg(x)
    _rhs(x, q, obj.ordA, obj.fstA, obj.nfib, obj.lev, obj.pid, PF30, out, 0)
    return obj.sym(out) if sym else out


def jvp(obj, x, v, q=None, sym=True):
    """directional derivative of the (quadratic) field at x along v: G(v; q(x)) + G(x; q(v))."""
    if q is None:
        q = obj.marg(x)
    out = np.zeros(obj.n)
    _rhs(v, q, obj.ordA, obj.fstA, obj.nfib, obj.lev, obj.pid, PF30, out, 0)
    _rhs(x, obj.marg(v), obj.ordA, obj.fstA, obj.nfib, obj.lev, obj.pid, PF30, out, 0)
    return obj.sym(out) if sym else out


@njit(cache=True)
def _outflow(x, q, ordA, fstA, nfib, lev, pid, PF, lam):
    """lam_t = (1/3) sum_s lam_f(l_s(t)): the exit rate of an island in state t (for preconditioning)."""
    third = 1.0 / 3.0
    ql = np.zeros(NLEV)
    for s in range(3):
        for f in range(nfib[s]):
            a = fstA[s, f]
            b = fstA[s, f + 1]
            for l in range(NLEV):
                ql[l] = 0.0
            for j in range(a, b):
                t = ordA[s, j]
                ql[lev[s, t]] += q[s, pid[s, t]]
            for j in range(a, b):
                t = ordA[s, j]
                l = lev[s, t]
                sl = 0.0
                for v in range(NLEV):
                    if ql[v] != 0.0:
                        sl += ql[v] * PF[v - l + DMAX]
                lam[t] += third * sl


def outflow(obj, x):
    lam = np.zeros(obj.n)
    _outflow(x, obj.marg(x), obj.ordA, obj.fstA, obj.nfib, obj.lev, obj.pid, PF30, lam)
    return lam


@njit(cache=True)
def _blocked(x, q, ordA, fstA, nfib, lev, pid, T, supp_flat, supp_off, armi, nat, atL, atJ, atA, tab, PARTNER, PAY2, PF, thr, out):
    """blocked flux of the reflecting truncation: for every fibre (s, context) with mass above thr and every donor y in the
    support of slot s with q_s(y) > 0 that is not a member of the fibre, the flux (1/3) q_s(y) sum_u x_u PF[l_y - l_u]
    that the full object would have, with l_y the payoff level of the would-be triple.  out[s] accumulates it."""
    hist = np.empty((2, 3), np.int64)
    val = np.empty(3, np.int64)
    mark = np.zeros(1305, np.int8)
    xl = np.zeros(NLEV)
    for s in range(3):
        for f in range(nfib[s]):
            a = fstA[s, f]
            b = fstA[s, f + 1]
            tot = 0.0
            for l in range(NLEV):
                xl[l] = 0.0
            for j in range(a, b):
                t = ordA[s, j]
                xl[lev[s, t]] += x[t]
                tot += x[t]
            if tot < thr:
                continue
            for j in range(a, b):
                mark[pid[s, ordA[s, j]]] = 1
            t0 = ordA[s, a]
            c0 = np.int64(T[t0, 0]); c1 = np.int64(T[t0, 1]); c2 = np.int64(T[t0, 2])
            for k in range(supp_off[s], supp_off[s + 1]):
                y = supp_flat[k]
                if mark[y] == 0 and q[s, y] > 0.0:
                    if s == 0:
                        code = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, np.int64(y), c1, c2, hist, val)
                    elif s == 1:
                        code = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, c0, np.int64(y), c2, hist, val)
                    else:
                        code = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, c0, c1, np.int64(y), hist, val)
                    ly = int(np.rint(PAY2[code, s] * 30.0)) + 3
                    acc = 0.0
                    for v in range(NLEV):
                        if xl[v] != 0.0:
                            acc += xl[v] * PF[ly - v + DMAX]
                    out[s] += acc * q[s, y] / 3.0
            for j in range(a, b):
                mark[pid[s, ordA[s, j]]] = 0


def blocked_flux(obj, x, thr=1e-14):
    """(blocked flux per event per island, realized flux per event per island, per-slot blocked fluxes).  Realized = sum_t x_t
    lam_t, the rate at which islands change state under the truncated object."""
    if obj.m >= 3 and obj.core is None:
        return 0.0, float((x * outflow(obj, x)).sum()), [0.0, 0.0, 0.0]
    q = obj.marg(x)
    out = np.zeros(3)
    flat = np.concatenate([obj.supp[s] for s in range(3)]).astype(np.int64)
    off = np.zeros(4, np.int64)
    for s in range(3):
        off[s + 1] = off[s] + len(obj.supp[s])
    a = obj.arm
    S = a.S
    PAY2, _ = UC.tables2(obj.pfail)
    _blocked(x, q, obj.ordA, obj.fstA, obj.nfib, obj.lev, obj.pid, obj.T, flat, off, np.int64(a.armi),
             np.ascontiguousarray(S.nat), np.ascontiguousarray(S.atL), np.ascontiguousarray(S.atJ), np.ascontiguousarray(S.atA),
             np.ascontiguousarray(S.tab), np.ascontiguousarray(D.PARTNER), PAY2, PF30, thr, out)
    real = float((x * outflow(obj, x)).sum())
    return float(out.sum()), real, out.tolist()


# ---------------------------------------------------------------- starts
def tilt(obj, x, kind, target=0.6):
    """rescale outcome-class shares to the target keeping within-class frequencies and the ratios among the other classes:
    'fair' F -> target; 'unequal' U -> target; 'wd' W + D -> target."""
    sh = obj.class_shares(x)
    sel = {'fair': [0], 'unequal': [1], 'wd': [3, 4]}[kind]
    rest = [c for c in range(NCLS) if c not in sel]
    m_t = float(sh[sel].sum())
    m_r = float(sh[rest].sum())
    if m_t <= 0 or m_r <= 0:
        return None, dict(kind=kind, available=False, before=sh.tolist())
    f = np.ones(NCLS)
    for c in sel:
        f[c] = target / m_t
    for c in rest:
        f[c] = (1.0 - target) / m_r
    y = x * f[obj.cl]
    return y, dict(kind=kind, available=True, before=sh.tolist(), after=obj.class_shares(y).tolist())


def tilt_u(obj, x, u):
    return tilt(obj, x, 'unequal', u)


# ---------------------------------------------------------------- integration
def checkpoint_grid(tmax):
    g = [0.0]
    e = 0
    while 10.0 ** e <= tmax * (1 + 1e-12):
        for mlt in (1, 2, 5):
            t = mlt * 10.0 ** e
            if t <= tmax * (1 + 1e-12):
                g.append(t)
        e += 1
    return g


def record(obj, t, x, sym=True, extra=None):
    sh, pairs = obj.class_shares(x, True)
    Fx = field(obj, x, sym)
    r = dict(t=float(t), shares=sh.tolist(), pairs=pairs.tolist(), resid=float(np.abs(Fx).sum()), minx=float(x.min()),
             mass=float(x.sum()))
    if extra:
        r.update(extra)
    return r


def converged(recs, t, sh, resid):
    if resid >= 1e-9 or t < 1e3:
        return False
    best = None
    for r in recs:
        if abs(r['t'] - t / 10.0) < 0.3 * t / 10.0 and (best is None or abs(r['t'] - t / 10.0) < abs(best['t'] - t / 10.0)):
            best = r
    if best is None:
        return False
    return float(np.abs(np.array(best['shares']) - np.array(sh)).max()) < 1e-4


def integrate(obj, x0, tmax, sym=True, rtol=1e-8, atol=1e-14, grid=None, method='DOP853', stop_converged=True, keep_x_at=(),
              verbose=False, recs=None, t_start=0.0):
    from scipy.integrate import solve_ivp
    grid = checkpoint_grid(tmax) if grid is None else list(grid)
    x = x0.copy()
    recs = [] if recs is None else recs
    if not recs:
        recs.append(record(obj, t_start, x, sym))
    kept = {}
    status = 'horizon'
    fun = lambda t, y: field(obj, y, sym)
    for i in range(1, len(grid)):
        t0, t1 = grid[i - 1], grid[i]
        if t1 <= t_start:
            continue
        t0 = max(t0, t_start)
        sol = solve_ivp(fun, (t0, t1), x, method=method, rtol=rtol, atol=atol)
        x = sol.y[:, -1]
        r = record(obj, t1, x, sym, dict(nfev=int(sol.nfev)))
        recs.append(r)
        if t1 in keep_x_at:
            kept[t1] = x.copy()
        if verbose:
            print('t=%g shares=%s resid=%.2e nfev=%d' % (t1, np.round(r['shares'], 4), r['resid'], sol.nfev), flush=True)
        if stop_converged and converged(recs, t1, r['shares'], r['resid']):
            status = 'converged'
            break
    return recs, x, status, kept


def be_step(obj, x, h, sym=True, max_newton=5, gm_tol=1e-9, gm_restart=50, gm_maxiter=30):
    """one backward-Euler step x' = x + h F(x') by Newton with matrix-free GMRES and a diagonal preconditioner."""
    from scipy.sparse.linalg import LinearOperator, gmres
    xn = x.copy()
    n = x.size
    its = 0
    for it in range(max_newton):
        R = xn - x - h * field(obj, xn, sym)
        rn = float(np.abs(R).sum())
        if rn < 1e-13:
            break
        q = obj.marg(xn)
        lam = outflow(obj, xn)
        Minv = 1.0 / (1.0 + h * lam)
        A = LinearOperator((n, n), matvec=lambda v: v - h * jvp(obj, xn, v, q, sym), dtype=np.float64)
        M_ = LinearOperator((n, n), matvec=lambda v: Minv * v, dtype=np.float64)
        try:
            d, info = gmres(A, -R, M=M_, rtol=gm_tol, atol=0.0, restart=gm_restart, maxiter=gm_maxiter)
        except TypeError:
            d, info = gmres(A, -R, M=M_, tol=gm_tol, atol=0.0, restart=gm_restart, maxiter=gm_maxiter)
        its += 1
        xn = xn + d
        if float(np.abs(d).sum()) < 1e-13:
            break
    R = xn - x - h * field(obj, xn, sym)
    return xn, dict(newton=its, resid=float(np.abs(R).sum()))


def integrate_be(obj, x, t0, tmax, sym=True, steps_per_decade=8, recs=None, verbose=False):
    recs = [] if recs is None else recs
    t = t0
    status = 'horizon'
    ratio = 10.0 ** (1.0 / steps_per_decade)
    h = max(t0 * (ratio - 1.0), 1.0)
    while t < tmax * (1 - 1e-12):
        h = min(h, tmax - t)
        for attempt in range(14):
            xn, info = be_step(obj, x, h, sym)
            if xn.min() > -1e-10 and info['resid'] < 1e-8:
                break
            h *= 0.5
        x = xn
        t += h
        r = record(obj, t, x, sym, dict(newton=info['newton'], be_resid=info['resid'], solver='be'))
        recs.append(r)
        if verbose:
            print('BE t=%.4g shares=%s resid=%.2e newton=%d' % (t, np.round(r['shares'], 4), r['resid'], info['newton']), flush=True)
        if converged(recs, t, r['shares'], r['resid']):
            status = 'converged'
            break
        h *= ratio
    return recs, x, status


def run_ode(obj, x0, tmax=1e7, sym=True, explicit_until=1e4, verbose=False, keep_x_at=()):
    """explicit DOP853 to explicit_until events, then backward Euler to tmax; returns (records, x_end, status, kept)."""
    recs, x, status, kept = integrate(obj, x0, min(explicit_until, tmax), sym, verbose=verbose, keep_x_at=keep_x_at)
    if status != 'converged' and tmax > explicit_until:
        recs2 = recs
        recs2, x, status = integrate_be(obj, x, explicit_until, tmax, sym, recs=recs, verbose=verbose)
    return recs, x, status, kept


def classify_endpoint(sh):
    """U-dominated (U >= 0.5), V*-dominated (F >= 0.5), else other."""
    if sh[1] >= 0.5:
        return 'U'
    if sh[0] >= 0.5:
        return 'F'
    return 'other'


# ====================================================================== cells: pools -> symmetrized empirical start
def decode_keys(k):
    k = np.asarray(k, np.int64)
    return np.stack([k // (KP * KP), (k // KP) % KP, k % KP], axis=1)


class Cell:
    """The post-anneal law of a cell: the symmetrized union of its pools' settled islands.

    trip, w: the distinct S3-symmetrized triples and their probabilities (sum 1); supp[s]: the S3-union support of slot s
    plus the nine constants; pool_of: per distinct triple unused.  Built from the pools' npz files (scratch, not committed)."""

    def __init__(self, armname, pfail_found, A, pools=(0, 1, 2), symmetrize=True):
        self.armname = armname
        self.pfail_found = pfail_found
        self.A = A
        self.pools = tuple(pools)
        self.arm = get_arm(armname)
        self.nat, self.isc = program_data(self.arm)
        raw = []
        self.npool = []
        for p in pools:
            tr, info = UC.load_pool2(armname, pfail_found, A, p)
            raw.append(tr)
            self.npool.append(info)
        self.raw = np.concatenate(raw)
        self.n_islands = sum(i['n'] for i in self.npool)
        self.n_settled = len(self.raw)
        self.symmetrized = symmetrize
        img = image_triples(self.arm, self.raw) if symmetrize else self.raw
        k = keys_of(img)
        uk, cnt = np.unique(k, return_counts=True)
        self.trip = decode_keys(uk)
        self.w = cnt / cnt.sum()
        cons = [x for x in range(KP) if self.isc[x]]
        self.supp = []
        for s in range(3):
            sp = set(int(v) for v in np.unique(self.trip[:, s])) | set(cons)
            self.supp.append(sorted(sp))

    def seed_absent_mass(self):
        """seed-law mass of the programs absent from the union supports (per slot)."""
        out = []
        for s in range(3):
            law = self.arm.laws[s]
            m = np.ones(KP, bool)
            m[self.supp[s]] = False
            out.append(float(law[m].sum()))
        return out
