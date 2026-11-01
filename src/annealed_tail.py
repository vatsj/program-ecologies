"""The annealed mutation tail on the mean-field object of the unequal-basin experiment (spec specs/2026-11-01-annealed-tail-dollar3.md).

The tail-free object is queue 70's (unequal_basin.py: object P, the reflecting m-truncation of the exact I -> infinity jump
chain on settled program triples; many_islands_t_ode.py: arm T).  The tail adds prior arrivals, at rate eps(tau) per island
per migrant event, each to a uniformly random slot with the program drawn from the slot's founding prior p, fixing with
the same Moran kernel as a migrant.  The migration field G(x; q) is linear in the donor law q, so

    dx/dtau = F(x) + eps(tau) G(x; p),         F(x) = G(x; q(x)),

with p the prior over the programs of the state set (programs outside the state set make null events; their mass is the
"restricted mass").  tau = events per island since the tail started (t_s); Anneal: eps(tau) = (Lam/t0)(1 + tau/t0)^-2, so
Lam is the total number of arrivals per island; Const: eps = Lam/T on [0, T] (constant rain).

Systems (duck-typed): DSL (object P of arm L / M, any N through the fixation table) and ArmT (27 L_T^code programs).
Integration: explicit DOP853 on the checkpoint grid to 1e4 events, then backward Euler (geometric steps) with the tail dose of
each step delivered exactly (the step's mean rate is dose/h).  Nothing in the existing modules is edited.
"""
import os, sys, math, time, json, hashlib
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import many_islands as MI
import unequal_basin as UB
import unequal_basin_core as UC

ROOT = MI.ROOT
OUTD = os.path.join(ROOT, 'runs', 'annealed_tail')
ROWS = os.path.join(OUTD, 'rows')
SCR = os.environ.get('AT_SCRATCH', os.path.join(os.path.dirname(UC.SCR), 'at'))
XSD = os.path.join(SCR, 'xstar')
for _d in (OUTD, ROWS, SCR, XSD):
    os.makedirs(_d, exist_ok=True)

DMAX = UB.DMAX
NLEV = UB.NLEV
CLS = UB.CLS


# ====================================================================== schedules
class Sched:
    """tail schedules on the tau clock (events per island since t_s)."""

    def __init__(self, kind, Lam, t0=1.0, T=1e4):
        self.kind, self.Lam, self.t0, self.T = kind, float(Lam), float(t0), float(T)

    def eps(self, tau):
        if self.Lam == 0 or tau < 0:
            return 0.0
        if self.kind == 'anneal':
            return self.Lam / self.t0 / (1.0 + tau / self.t0) ** 2
        if self.kind == 'const':
            return self.Lam / self.T if tau < self.T else 0.0
        raise ValueError(self.kind)

    def cum(self, tau):
        """arrivals per island delivered on [0, tau]"""
        if self.Lam == 0:
            return 0.0
        if self.kind == 'anneal':
            return self.Lam * (1.0 - 1.0 / (1.0 + tau / self.t0))
        return self.Lam * min(tau, self.T) / self.T

    def dose(self, a, b):
        return self.cum(b) - self.cum(a)

    def remaining(self, tau):
        return self.Lam - self.cum(tau)

    def label(self):
        return '%s(Lam=%g,t0=%g)' % (self.kind, self.Lam, self.t0 if self.kind == 'anneal' else self.T)


# ====================================================================== the DSL system
class DSL:
    """object P of a DSL arm: states obj, migration field F, tail field G(x; p), fixation table PF (any N)."""

    def __init__(self, obj, p, PF=None, sym=True, label=''):
        self.obj = obj
        self.p = np.ascontiguousarray(p, np.float64)
        self.PF = UB.PF30 if PF is None else PF
        self.sym = sym
        self.n = obj.n
        self.label = label
        z = np.zeros(obj.n)
        self.lamG = np.zeros(obj.n)
        UB._outflow(z, self.p, obj.ordA, obj.fstA, obj.nfib, obj.lev, obj.pid, self.PF, self.lamG)

    def _flux(self, x, q):
        out = np.zeros(self.n)
        o = self.obj
        UB._rhs(x, q, o.ordA, o.fstA, o.nfib, o.lev, o.pid, self.PF, out, 0)
        return o.sym(out) if self.sym else out

    def F(self, x):
        return self._flux(x, self.obj.marg(x))

    def G(self, x):
        return self._flux(x, self.p)

    def jvpF(self, x, v, q):
        out = np.zeros(self.n)
        o = self.obj
        UB._rhs(v, q, o.ordA, o.fstA, o.nfib, o.lev, o.pid, self.PF, out, 0)
        UB._rhs(x, o.marg(v), o.ordA, o.fstA, o.nfib, o.lev, o.pid, self.PF, out, 0)
        return o.sym(out) if self.sym else out

    def qof(self, x):
        return self.obj.marg(x)

    def lam(self, x):
        o = self.obj
        lam = np.zeros(self.n)
        UB._outflow(x, o.marg(x), o.ordA, o.fstA, o.nfib, o.lev, o.pid, self.PF, lam)
        return lam

    def shares(self, x):
        return self.obj.class_shares(x, True)


# ====================================================================== the arm-T system
@njit(cache=True)
def _outflow_q(q, PF, lam):
    n = PF.shape[1]
    for a0 in range(n):
        for a1 in range(n):
            for a2 in range(n):
                tot = 0.0
                for y in range(n):
                    tot += q[0, y] * PF[0, a0, a1, a2, y] + q[1, y] * PF[1, a0, a1, a2, y] + q[2, y] * PF[2, a0, a1, a2, y]
                lam[(a0 * n + a1) * n + a2] = tot / 3.0


class ArmT:
    def __init__(self, tabs, PF, p27, label=''):
        import many_islands_t_ode as O
        self.O = O
        self.tabs = tabs
        self.PF = PF
        self.NP = O.NP
        self.n = O.NT
        self.p = np.tile(np.asarray(p27, np.float64), (3, 1))
        self.sym = True
        self.label = label
        self.lamG = np.zeros(self.n)
        _outflow_q(self.p, PF, self.lamG)

    def F(self, x):
        return self.O.F_of(x, self.PF, True)

    def G(self, x):
        out = np.zeros_like(x)
        self.O._rhs_bi(x, self.p, self.PF, out)
        return (out + self.O.rot_apply(out, 1) + self.O.rot_apply(out, 2)) / 3.0

    def jvpF(self, x, v, q):
        return self.O.jvp(x, v, self.PF, q, True)

    def qof(self, x):
        return self.O._marg(x, self.NP)

    def lam(self, x):
        return self.O.outflow_rate(x, self.PF)

    def shares(self, x):
        return self.O.class_shares(x, self.tabs, True)


# ====================================================================== integration
def checkpoint_grid(tmax):
    return UB.checkpoint_grid(tmax)


def _record(S, x, tau, sched, extra=None):
    sh, pairs = S.shares(x)
    Fx = S.F(x)
    r = dict(t=float(tau), shares=[float(v) for v in sh], pairs=[float(v) for v in pairs], resid_free=float(np.abs(Fx).sum()),
             minx=float(x.min()), mass=float(x.sum()), rem=float(sched.remaining(tau)))
    e = sched.eps(tau)
    if e > 0:
        r['resid_full'] = float(np.abs(Fx + e * S.G(x)).sum())
    else:
        r['resid_full'] = r['resid_free']
    if extra:
        r.update(extra)
    return r


def _stable(recs, t, sh, thr=1e-4):
    best = None
    for r in recs:
        if abs(r['t'] - t / 10.0) < 0.3 * t / 10.0 and (best is None or abs(r['t'] - t / 10.0) < abs(best['t'] - t / 10.0)):
            best = r
    if best is None:
        return False
    return float(np.abs(np.array(best['shares']) - np.array(sh)).max()) < thr


def stationary(recs, t, r):
    """criterion (a) of queue 70 on the tail-free residual: ||F|| < 1e-9, t >= 1e3, every class share moved < 1e-4 over a decade."""
    return r['resid_free'] < 1e-9 and t >= 1e3 and _stable(recs, t, r['shares'])


def locked(recs, t, r):
    """early classification (scans): a class holds >= 0.99, tail-free residual < 1e-6, t >= 2e4, shares moved < 1e-3 over half a decade."""
    sh = r['shares']
    if t < 2e4 or r['resid_free'] >= 1e-6 or (sh[0] < 0.99 and sh[1] < 0.99):
        return False
    best = None
    for q in recs:
        if abs(q['t'] - t / 3.16) < 0.3 * t / 3.16 and (best is None or abs(q['t'] - t / 3.16) < abs(best['t'] - t / 3.16)):
            best = q
    if best is None:
        return False
    return float(np.abs(np.array(best['shares']) - np.array(sh)).max()) < 1e-3


def be_step(S, x, h, e_h, max_newton=6, gm_tol=1e-9, gm_restart=50, gm_maxiter=30):
    """x' = x + h F(x') + h e_h G(x'), Newton with matrix-free GMRES and a diagonal preconditioner."""
    from scipy.sparse.linalg import LinearOperator, gmres
    xn = x.copy()
    n = x.size
    its = 0
    for it in range(max_newton):
        Fx = S.F(xn)
        R = xn - x - h * Fx
        if e_h != 0.0:
            R = R - h * e_h * S.G(xn)
        rn = float(np.abs(R).sum())
        if rn < 1e-13:
            break
        q = S.qof(xn)
        lam = S.lam(xn) + (e_h * S.lamG if e_h != 0.0 else 0.0)
        Minv = 1.0 / (1.0 + h * lam)
        if e_h != 0.0:
            mv = lambda v: v - h * S.jvpF(xn, v, q) - h * e_h * S.G(v)
        else:
            mv = lambda v: v - h * S.jvpF(xn, v, q)
        A = LinearOperator((n, n), matvec=mv, dtype=np.float64)
        M_ = LinearOperator((n, n), matvec=lambda v: Minv * v, dtype=np.float64)
        try:
            d, info = gmres(A, -R, M=M_, rtol=gm_tol, atol=0.0, restart=gm_restart, maxiter=gm_maxiter)
        except TypeError:
            d, info = gmres(A, -R, M=M_, tol=gm_tol, atol=0.0, restart=gm_restart, maxiter=gm_maxiter)
        its += 1
        xn = xn + d
        if float(np.abs(d).sum()) < 1e-13:
            break
    R = xn - x - h * S.F(xn)
    if e_h != 0.0:
        R = R - h * e_h * S.G(xn)
    return xn, dict(newton=its, resid=float(np.abs(R).sum()))


def classify(sh):
    if sh[1] >= 0.5:
        return 'U'
    if sh[0] >= 0.5:
        return 'F'
    return 'other'


def integrate(S, x0, sched, tau0=0.0, tmax=1e8, explicit_until=1e4, spd=8, early=False, recs=None, keep_at=(), verbose=False,
              stop_stationary=True, wall_limit=None, cb=None, explicit_grid=None):
    """integrate from tau0 to tmax.  Returns (recs, x, status, kept).  status: 'stationary' (criterion (a) on the tail-free residual),
    'early' (locked), 'capped' (tau = tmax), 'wall' (wall_limit s exceeded)."""
    from scipy.integrate import solve_ivp
    t_wall = time.time()
    recs = [] if recs is None else recs
    x = x0.copy()
    kept = {}
    status = 'capped'
    if not recs:
        recs.append(_record(S, x, tau0, sched))
        if cb is not None:
            cb(tau0, x)
    def fun(t, y):
        e = sched.eps(t)
        return S.F(y) + e * S.G(y) if e > 0 else S.F(y)
    t = tau0
    # explicit phase
    if tau0 < explicit_until:
        grid = [g for g in (checkpoint_grid(min(explicit_until, tmax)) if explicit_grid is None else explicit_grid) if g > tau0 and g <= explicit_until]
        if not grid or grid[0] > tau0:
            pass
        tprev = tau0
        for g in grid:
            sol = solve_ivp(fun, (tprev, g), x, method='DOP853', rtol=1e-8, atol=1e-14)
            x = sol.y[:, -1]
            tprev = g
            t = g
            r = _record(S, x, t, sched, dict(nfev=int(sol.nfev)))
            recs.append(r)
            if cb is not None:
                cb(t, x)
            for k in keep_at:
                if abs(k - t) <= 1e-9 * max(1.0, k):
                    kept[k] = x.copy()
            if verbose:
                print('t=%g shares=%s resid=%.2e rem=%.2e' % (t, np.round(r['shares'], 4), r['resid_free'], r['rem']), flush=True)
            if stop_stationary and stationary(recs, t, r):
                return recs, x, 'stationary', kept
            if early and locked(recs, t, r):
                return recs, x, 'early', kept
    # backward-Euler phase on t_k = t_start 10^(k/spd)
    t_start = max(t, 1.0)
    if t_start >= tmax * (1 - 1e-12):
        return recs, x, 'capped', kept
    k = 0
    tcur = t
    while tcur < tmax * (1 - 1e-12):
        k += 1
        # next point on the geometric lattice strictly above tcur
        tn = t_start * 10.0 ** (k / float(spd))
        while tn <= tcur * (1 + 1e-12):
            k += 1
            tn = t_start * 10.0 ** (k / float(spd))
        tn = min(tn, tmax)
        h = tn - tcur
        dose = sched.dose(tcur, tn)
        e_h = dose / h if dose != 0 else 0.0
        hh = h
        xs = x
        tt = tcur
        # sub-steps if Newton fails (halve the step, delivering the dose pro rata)
        todo = h
        while todo > 1e-12 * max(1.0, tn):
            hs = todo
            for attempt in range(16):
                dose_s = sched.dose(tt, tt + hs)
                xn, info = be_step(S, xs, hs, dose_s / hs if dose_s != 0 else 0.0)
                if xn.min() > -1e-10 and info['resid'] < 1e-8:
                    break
                hs *= 0.5
            xs = xn
            tt += hs
            todo -= hs
        x = xs
        tcur = tn
        r = _record(S, x, tcur, sched, dict(newton=info['newton'], be_resid=info['resid'], solver='be'))
        recs.append(r)
        if cb is not None:
            cb(tcur, x)
        for kk in keep_at:
            if abs(kk - tcur) <= 1e-9 * max(1.0, kk):
                kept[kk] = x.copy()
        if verbose:
            print('BE t=%.4g shares=%s resid=%.2e rem=%.2e newton=%d' % (tcur, np.round(r['shares'], 4), r['resid_free'], r['rem'], info['newton']), flush=True)
        if stop_stationary and stationary(recs, tcur, r):
            return recs, x, 'stationary', kept
        if early and locked(recs, tcur, r):
            return recs, x, 'early', kept
        if wall_limit and time.time() - t_wall > wall_limit:
            return recs, x, 'wall', kept
    return recs, x, 'capped', kept


def burst(S, x, dose):
    """deliver `dose` arrivals per island at once: dx/ds = G(x; p) on s in [0, dose] with migration frozen."""
    from scipy.integrate import solve_ivp
    if dose <= 0:
        return x.copy()
    sol = solve_ivp(lambda s, y: S.G(y), (0.0, dose), x, method='DOP853', rtol=1e-9, atol=1e-14)
    return sol.y[:, -1]


def _is_grid(t):
    if t <= 0:
        return t == 0
    e = math.floor(math.log10(t) + 1e-9)
    m = t / 10.0 ** e
    return any(abs(m - g) < 1e-6 for g in (1.0, 2.0, 5.0, 10.0))


def run_cell(S, x0, sched, tmax=1e8, early=False, spd=8, verbose=False, keep_at=(), explicit_until=1e4, wall_limit=None):
    """a full tail run with the spec's censoring protocol.  Returns a dict: status, class, endpoint shares, milestones, records,
    x_end (not json)."""
    t0 = time.time()
    sched0 = sched
    recs, x, status, kept = integrate(S, x0, sched, 0.0, tmax, explicit_until, spd, early, keep_at=keep_at, verbose=verbose, wall_limit=wall_limit)
    tau = recs[-1]['t']
    rem = sched.remaining(tau)
    out = dict(status=status, tau_end=tau, rem_end=float(rem))
    last = recs[-1]
    out['shares_run_end'] = last['shares']
    out['pairs_run_end'] = last['pairs']
    out['resid_free_end'] = last['resid_free']
    free = Sched('anneal', 0.0)
    if status in ('stationary', 'early') and rem < 1e-4:
        out['protocol'] = 'direct'
        out['class'] = classify(last['shares'])
        out['shares'] = last['shares']
        out['pairs'] = last['pairs']
        xe = x
    elif status == 'wall':
        out['protocol'] = 'wall'
        out['class'] = 'unresolved'
        out['shares'] = last['shares']
        out['pairs'] = last['pairs']
        xe = x
    else:
        # censored or tail-pending: (A) tail-free continuation, (B) the remaining dose at once, then tail-free
        out['protocol'] = 'censored' if status == 'capped' else 'burst'
        recsA = list(recs)
        if status in ('stationary', 'early'):
            xA, stA, shA, pairsA = x, status, last['shares'], last['pairs']
        else:
            r2, xA, stA, _ = integrate(S, x, free, tau, tau + 1e8, 0.0, spd, early, recs=[recs[-1]])
            shA, pairsA = r2[-1]['shares'], r2[-1]['pairs']
        xb = burst(S, x, rem)
        r3, xB, stB, _ = integrate(S, xb, free, tau, tau + 1e8, 0.0, spd, early, recs=[_record(S, xb, tau, free)])
        shB, pairsB = r3[-1]['shares'], r3[-1]['pairs']
        cA, cB = classify(shA), classify(shB)
        out['A_tailfree'] = dict(shares=shA, status=stA, cls=cA)
        out['B_burst'] = dict(shares=shB, status=stB, cls=cB, dose=float(rem))
        out['class'] = cA if cA == cB else 'unresolved'
        out['shares'] = shB
        out['pairs'] = pairsB
        out['shares_A'] = shA
        xe = xB
    out['wall'] = time.time() - t0
    # compact records: checkpoint grid + milestones
    ms = {}
    for m in (1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8):
        for r in recs:
            if abs(r['t'] - m) <= 1e-9 * m:
                ms[str(int(m))] = [round(v, 6) for v in r['shares']]
    out['milestones'] = ms
    out['records'] = [dict(t=r['t'], shares=[round(v, 7) for v in r['shares']], rf=float('%.2e' % r['resid_free']), rem=float('%.3e' % r['rem']))
                      for r in recs if _is_grid(r['t'])]
    return out, xe, kept


# ====================================================================== arm-T cells and starts
def armT_system(cell, pm, dose='main', p27=None, tail_dose=None):
    import many_islands_t as MT
    import many_islands_t_common as CT
    T = CT.tabs()
    PF = CT.get_pf(pm)
    p = MT.seed_law(T, tail_dose or dose) if p27 is None else p27
    return ArmT(T, PF, p, label='armT %s %s' % (cell, pm)), T, CT


def armT_start(cell, start, pool=0):
    import many_islands_t_ode as O
    import many_islands_t_common as CT
    T = CT.tabs()
    xs = O.symmetrize(O.hist_to_x(CT.load_pool(cell, pool)))
    if start == 'nat':
        return xs, dict(kind='nat', after=O.class_shares(xs, T).tolist())
    if start.startswith('u:'):
        x0, info = O.tilt(xs, T, 'unequal', float(start[2:]))
        return x0, info
    raise ValueError(start)


# ====================================================================== DSL cells and starts
_SYS = {}


def dsl_base(cellname, corelabel='pilot_L', m=3, remove=None, pools=(0, 1, 2)):
    """(cell, obj, xn) for a DSL cell: the symmetrized post-anneal law of the pools on object P (cached per process)."""
    import unequal_basin_run as R
    import unequal_basin_jobs as J
    key = (cellname, corelabel, m, tuple(pools), None if remove is None else hashlib.md5(remove.tobytes()).hexdigest())
    if key not in _SYS:
        spec = dict(cell=cellname, m=m, start='nat', abl=None)
        core = J.load_core(corelabel) if corelabel else None
        cell, obj, xn, dropped = R.build_obj_start(spec, remove, 'reassign', pools, core)
        _SYS[key] = (cell, obj, xn, dropped)
    return _SYS[key]


def pf_table(N):
    if N is None or int(N) == int(MI.N0):
        return UB.PF30
    return np.array([MI.pfix(d / 30.0, float(N), float(MI.W)) for d in range(-DMAX, DMAX + 1)])


def tail_law(cell, kind='full', renorm=False):
    """the tail's prior (3, KP): the founding prior; ablations remove families (matched-dose: the removed mass becomes null events;
    renorm=True rescales the rest to its original total)."""
    import unequal_basin_run as R
    arm = cell.arm
    p = arm.laws.copy()
    if kind in (None, 'full'):
        return p
    rm = np.zeros((3, UB.KP), bool)
    cons = np.array([x for x in range(UB.KP) if cell.isc[x]])
    names = kind.split('+')
    for nm in names:
        if nm == 'bully':
            rm |= R.family_mask(arm, 'exploiter-fair')
        elif nm == 'victim':
            # constants naming a slot partner at 1/3 (S3 orbit of the (partner, 1/3) constants), every slot
            for s in range(3):
                for x in cons:
                    l = int(arm.S.fs[x][1][0])
                    import dollar3 as D
                    if D.partner_abs(s, l) != D.ALL and l % 3 == 0:
                        rm[s, x] = True
        elif nm == 'cond':
            for s in range(3):
                rm[s, ~cell.isc] = True
        else:
            raise ValueError(nm)
    tot0 = p.sum(axis=1)
    p[rm] = 0.0
    if renorm:
        p *= (tot0 / p.sum(axis=1))[:, None]
    return p


def dsl_start(obj, xn, start):
    import unequal_basin_run as R
    return R.make_start(obj, xn, start)


def row_key(spec):
    s = json.dumps(spec, sort_keys=True, default=str)
    return hashlib.md5(s.encode()).hexdigest()[:12]


def save_row(spec, res, extra=None):
    key = row_key(spec)
    row = dict(spec=spec, key=key)
    row.update({k: v for k, v in res.items() if k != 'x_end'})
    if extra:
        row.update(extra)
    path = os.path.join(ROWS, key + '.json')
    json.dump(row, open(path, 'w'), default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    return row


def load_row(spec):
    path = os.path.join(ROWS, row_key(spec) + '.json')
    if os.path.exists(path):
        return json.load(open(path))
    return None


def blocked(S, x, q, thr=1e-14):
    """flux per event per island of arrivals with donor law q (unit rate) that the reflecting truncation turns into null events,
    and the realized flux of the same arrivals; q = the state's marginals gives the migrants' blocked flux, q = S.p the tail's."""
    o = S.obj
    if o.m >= 3 and o.core is None:
        return 0.0, 0.0
    flat = np.concatenate([o.supp[s] for s in range(3)]).astype(np.int64)
    off = np.zeros(4, np.int64)
    for s in range(3):
        off[s + 1] = off[s] + len(o.supp[s])
    a = o.arm
    Sx = a.S
    PAY2, _ = UC.tables2(o.pfail)
    import dollar3 as D
    out = np.zeros(3)
    UB._blocked(x, q, o.ordA, o.fstA, o.nfib, o.lev, o.pid, o.T, flat, off, np.int64(a.armi), np.ascontiguousarray(Sx.nat),
                np.ascontiguousarray(Sx.atL), np.ascontiguousarray(Sx.atJ), np.ascontiguousarray(Sx.atA), np.ascontiguousarray(Sx.tab),
                np.ascontiguousarray(D.PARTNER), PAY2, S.PF, thr, out)
    lam = np.zeros(o.n)
    UB._outflow(x, q, o.ordA, o.fstA, o.nfib, o.lev, o.pid, S.PF, lam)
    real = float((x * lam).sum())
    return float(out.sum()), real
