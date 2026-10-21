"""Rediscovering the core: first-price package auctions on islands, the losing bid as a threat
(spec specs/2026-10-21-core-rediscovery.md; notes notes/core-rediscovery.md; predictions predictions/2026-10-21-core-rediscovery.md).

Roles (one population per role per island): P (the package bidder, on AB), A (on item A), B (on item B); role indices 0, 1, 2.
Values (vP, vA, vB) are complete information.  Bids are integers on 0..40.

Seller (best offer, first price): the allocation among {P}, {A, B}, {A}, {B} with the highest reported revenue; revenue ties
are broken uniformly at random; winners pay their bids.  A bid of 0 is "no bid" (it cannot win; all-zero means no sale).
Payoffs and every statistic are expectations over the seller's tie lottery.

Programs: constant c (index c, 0..40) and PRU(c) (index 41 + c, the responder with default c).
  PRU(c) in role r reads the other roles' programs (here the same as seeing their bids) and plays the bid maximizing its
  expected payoff against the others' current bids over the bid set of the space (0..40 unrestricted; 0..value no-overbid),
  ties toward the lower bid; it plays that bid when its expected payoff is strictly positive and otherwise its default c.
Evaluator: constants resolve first; PRU programs then best-reply in the role order `order` (default P, A, B) to the bids resolved
  so far (unresolved responders at their defaults); a second pass follows; if it changes nothing the profile is resolved,
  otherwise the triple is recorded as cycling and the second-pass bids are used.

The island dynamics (`sim`): the repo's fixed-role seed lottery as in `auction_islands.sim3` (three populations per island, a
birth-death process with fitness exp(w * expected payoff), uniform victim, 3NI events per generation, expectation over
independent draws from the two other roles' island populations), extended to 82 programs per role with incremental payoffs on
present programs only, a re-injection schedule (a founder drawn from the prior replaces a uniformly chosen program with
per-event probability eps_g), per-role migration, and sampled per-island statistics.
"""
import os, sys, math, json, ast
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abm import njit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'core_auction')
R = 41                       # bids 0..40
NC = 41                      # constants
W = 0.3
TOL = 1e-9
INSTANCES = {'threshold': (20, 15, 15), 'asymmetric': (20, 16, 12), 'collusion': (20, 5, 5)}
ROLES = ('P', 'A', 'B')
# statistics channels of the tensor X (float32); U holds the three payoffs (float64)
XREV, XEFF, XIR, XCORE, XPRUWIN, XCYC, XBP, XBA, XBB = range(9)
NX = 9
# per-island statistic vector (sampled)
NS = 18   # uP uA uB rev eff ir core pruwin cyc | bid max (P A B) | bid median (P A B) | PRU share (P A B)
SI_U, SI_REV, SI_EFF, SI_IR, SI_CORE, SI_PRUWIN, SI_CYC, SI_BMAX, SI_BMED, SI_PRU = 0, 3, 4, 5, 6, 7, 8, 9, 12, 15


# ------------------------------------------------------------------ instance facts (pure python, by hand in the tests)
def wstar(v):
    vP, vA, vB = v
    return max(vP, vA + vB)


def w_without(v, S):
    """max welfare among the seller and the bidders not in S (S a set of roles 0/1/2)."""
    vP, vA, vB = v
    inP, inA, inB = 0 in S, 1 in S, 2 in S
    best = 0
    if not inP:
        best = max(best, vP)
    if not inA and not inB:
        best = max(best, vA + vB)
    if not inA:
        best = max(best, vA)
    if not inB:
        best = max(best, vB)
    return best


def core_inequalities(v):
    """the true-value core: {S: bound on the sum of the bidders' payoffs in S} for every nonempty S, plus the total."""
    ws = wstar(v)
    out = {}
    for mask in range(1, 8):
        S = {i for i in range(3) if mask >> i & 1}
        out[tuple(sorted(S))] = ws - w_without(v, S)
    return out


def in_core(v, u, rev, tol=1e-6):
    """is the outcome (bidder payoffs u = (uP, uA, uB), seller revenue rev) in the true-value core: efficient, individually
    rational (bidders and seller), and no set of bidders gets more than its joint marginal contribution."""
    ws = wstar(v)
    if sum(u) + rev < ws - tol:
        return False
    if rev < -tol or any(x < -tol for x in u):
        return False
    for S, bound in core_inequalities(v).items():
        if sum(u[i] for i in S) > bound + tol:
            return False
    return True


def core_violations(v, u, rev, tol=1e-6):
    """the true-value core inequalities violated by the outcome (labels), including efficiency and individual rationality."""
    ws = wstar(v)
    out = []
    if sum(u) + rev < ws - tol:
        out.append('inefficient')
    if rev < -tol:
        out.append('seller_IR')
    for i in range(3):
        if u[i] < -tol:
            out.append('IR_' + ROLES[i])
    for S, bound in core_inequalities(v).items():
        if sum(u[i] for i in S) > bound + tol:
            out.append('S=' + ''.join(ROLES[i] for i in S))
    return out


def max_bidder_total(v):
    """the largest total bidders' payoff over the true-value core (a small LP over the bidders' payoffs, bounds from `core_inequalities`)."""
    from scipy.optimize import linprog
    cin = core_inequalities(v)
    A = []; b = []
    for S, bound in cin.items():
        A.append([1.0 if i in S else 0.0 for i in range(3)]); b.append(bound)
    res = linprog([-1.0, -1.0, -1.0], A_ub=A, b_ub=b, bounds=[(0, None)] * 3, method='highs')
    return float(-res.fun)


def min_revenue(v):
    """minimum seller revenue over the true-value core: w(N) minus the largest total bidders' payoff the core allows."""
    return wstar(v) - max_bidder_total(v)


def core_revenue_range(v):
    ws = wstar(v)
    return min_revenue(v), ws


def vcg_payments(v):
    """VCG payments of the efficient allocation in the AM family with truthful reports (P, A, B)."""
    vP, vA, vB = v
    if vP >= vA + vB:                          # P wins (ties to P is irrelevant for the prices)
        return {'P': float(vA + vB)}
    return {'A': float(max(vP, vB) - vB), 'B': float(max(vP, vA) - vA)}


def vickrey_nearest(v):
    """the Vickrey-nearest point of the minimum-revenue core: the point of the minimum-revenue core nearest (Euclid) to the VCG payments.
    Two item winners: the payments are on the line pA + pB = min revenue, clamped by the core's bounds uA <= bA, uB <= bB."""
    vP, vA, vB = v
    if vP >= vA + vB:
        return {'P': float(min_revenue(v))}
    cin = core_inequalities(v)
    T = float(min_revenue(v))
    vc = vcg_payments(v)
    pa0, pb0 = vc['A'], vc['B']
    # nearest point on pA + pB = T to (pa0, pb0)
    d = (T - pa0 - pb0) / 2.0
    pa, pb = pa0 + d, pb0 + d
    # lower bounds on the payments: uA = vA - pA <= cin[(1,)], uB <= cin[(2,)]
    lo_a = vA - cin[(1,)]
    lo_b = vB - cin[(2,)]
    if pa < lo_a:
        pa, pb = lo_a, T - lo_a
    if pb < lo_b:
        pb, pa = lo_b, T - lo_b
    return {'A': float(pa), 'B': float(pb)}


def bidder_optimal_edge(v, space='no-overbid'):
    """integer split points of the bidder-optimal edge of the core: item bids (pA, pB) with revenue within one tick of the minimum, in the
    core when played as winners' bids, in the space's bid set.  Returns a list of (pA, pB)."""
    vP, vA, vB = v
    mr = min_revenue(v)
    cap = {'no-overbid': (vA, vB), 'unrestricted': (R - 1, R - 1)}[space]
    out = []
    for pa in range(1, cap[0] + 1):
        for pb in range(1, cap[1] + 1):
            rev = pa + pb
            if rev > mr + 1 + TOL or rev < mr - TOL:
                continue
            if in_core(v, (0, vA - pa, vB - pb), rev):
                out.append((pa, pb))
    return out


# ------------------------------------------------------------------ the seller (numba)
@njit(cache=True)
def _core_flag(vP, vA, vB, uP, uA, uB, rev, welfare, ws, tol):
    if welfare < ws - tol:
        return 0.0
    if rev < -tol or uP < -tol or uA < -tol or uB < -tol:
        return 0.0
    # S sets: bound = ws - w(N \ S)
    b = ws - max(vA + vB, vA, vB)                 # S = {P}: remaining A, B (and the seller)
    if uP > b + tol:
        return 0.0
    b = ws - max(vP, vB)                          # S = {A}
    if uA > b + tol:
        return 0.0
    b = ws - max(vP, vA)                          # S = {B}
    if uB > b + tol:
        return 0.0
    b = ws - vB                                   # S = {P, A}: remaining B
    if uP + uA > b + tol:
        return 0.0
    b = ws - vA                                   # S = {P, B}
    if uP + uB > b + tol:
        return 0.0
    b = ws - vP                                   # S = {A, B}
    if uA + uB > b + tol:
        return 0.0
    if uP + uA + uB > ws + tol:                   # S = all
        return 0.0
    return 1.0


@njit(cache=True)
def outcome(bP, bA, bB, vP, vA, vB):
    """expectations over the seller's tie lottery: uP, uA, uB, revenue, efficient, IR, in-core, P(P wins), P(A wins), P(B wins)."""
    ws = max(vP, vA + vB)
    revs = np.zeros(4)
    if bP >= 1:
        revs[0] = bP
    if bA >= 1 and bB >= 1:
        revs[1] = bA + bB
    if bA >= 1:
        revs[2] = bA
    if bB >= 1:
        revs[3] = bB
    M = 0.0
    for j in range(4):
        if revs[j] > M:
            M = revs[j]
    out = np.zeros(10)
    if M <= 0.0:
        out[5] = 1.0                                  # no sale: individually rational, not efficient
        return out
    n = 0
    for j in range(4):
        if revs[j] == M:
            n += 1
    for j in range(4):
        if revs[j] != M:
            continue
        wp = 1 if j == 0 else 0
        wa = 1 if (j == 1 or j == 2) else 0
        wb = 1 if (j == 1 or j == 3) else 0
        uP = (vP - bP) * wp
        uA = (vA - bA) * wa
        uB = (vB - bB) * wb
        welfare = vP * wp + vA * wa + vB * wb
        ir = 1.0 if (uP >= -TOL and uA >= -TOL and uB >= -TOL) else 0.0
        eff = 1.0 if welfare >= ws - TOL else 0.0
        core = _core_flag(vP, vA, vB, uP, uA, uB, M, welfare, ws, 1e-6)
        q = 1.0 / n
        out[0] += q * uP; out[1] += q * uA; out[2] += q * uB; out[3] += q * M
        out[4] += q * eff; out[5] += q * ir; out[6] += q * core
        out[7] += q * wp; out[8] += q * wa; out[9] += q * wb
    return out


@njit(cache=True)
def _exp_payoff(r, bP, bA, bB, vP, vA, vB):
    o = outcome(bP, bA, bB, vP, vA, vB)
    return o[r]


@njit(cache=True)
def best_reply(r, bP, bA, bB, vP, vA, vB, cap, default):
    """PRU's bid in role r against the others' bids (bP, bA, bB with the entry for r ignored): the expected-payoff maximizer on 0..cap,
    ties toward the lower bid; the default if the best expected payoff is not strictly positive."""
    best = 0.0; bx = default
    for x in range(0, cap + 1):
        if r == 0:
            u = _exp_payoff(0, x, bA, bB, vP, vA, vB)
        elif r == 1:
            u = _exp_payoff(1, bP, x, bB, vP, vA, vB)
        else:
            u = _exp_payoff(2, bP, bA, x, vP, vA, vB)
        if u > best + 1e-9:
            best = u; bx = x
    return bx


@njit(cache=True)
def resolve(kP, kA, kB, vP, vA, vB, capP, capA, capB, o0, o1, o2):
    """program triple -> resolved bids (bP, bA, bB) and the cycling flag.  Program k < NC is the constant k; k >= NC is PRU(k - NC).
    (o0, o1, o2) is the best-reply order of the roles (a permutation of 0, 1, 2)."""
    b = np.zeros(3, np.int64)
    ks = (kP, kA, kB)
    caps = (capP, capA, capB)
    pru = np.zeros(3, np.bool_)
    for r in range(3):
        if ks[r] >= NC:
            pru[r] = True; b[r] = ks[r] - NC
        else:
            b[r] = ks[r]
    order = (o0, o1, o2)
    # pass 1
    for t in range(3):
        r = order[t]
        if pru[r]:
            b[r] = best_reply(r, b[0], b[1], b[2], vP, vA, vB, caps[r], ks[r] - NC)
    b1 = b.copy()
    for t in range(3):
        r = order[t]
        if pru[r]:
            b[r] = best_reply(r, b[0], b[1], b[2], vP, vA, vB, caps[r], ks[r] - NC)
    cyc = 0
    for r in range(3):
        if b[r] != b1[r]:
            cyc = 1
    return b[0], b[1], b[2], cyc


@njit(cache=True)
def _build(K, vP, vA, vB, capP, capA, capB, o0, o1, o2, U, X):
    for kP in range(K):
        for kA in range(K):
            for kB in range(K):
                bP, bA, bB, cyc = resolve(kP, kA, kB, vP, vA, vB, capP, capA, capB, o0, o1, o2)
                o = outcome(bP, bA, bB, vP, vA, vB)
                U[0, kP, kA, kB] = o[0]; U[1, kP, kA, kB] = o[1]; U[2, kP, kA, kB] = o[2]
                X[XREV, kP, kA, kB] = o[3]; X[XEFF, kP, kA, kB] = o[4]; X[XIR, kP, kA, kB] = o[5]; X[XCORE, kP, kA, kB] = o[6]
                pw = 0.0
                if kP >= NC: pw += o[7]
                if kA >= NC: pw += o[8]
                if kB >= NC: pw += o[9]
                X[XPRUWIN, kP, kA, kB] = pw
                X[XCYC, kP, kA, kB] = cyc
                X[XBP, kP, kA, kB] = bP; X[XBA, kP, kA, kB] = bA; X[XBB, kP, kA, kB] = bB


def build_tensor(inst, space, with_pru, order=(0, 1, 2)):
    """payoff tensor U (3, K, K, K) float64 and statistics tensor X (9, K, K, K) float32, indexed [role, kP, kA, kB]."""
    v = INSTANCES[inst]
    K = 2 * NC if with_pru else NC
    caps = (R - 1,) * 3 if space == 'unrestricted' else tuple(v)
    U = np.zeros((3, K, K, K)); X = np.zeros((NX, K, K, K), np.float32)
    _build(K, v[0], v[1], v[2], caps[0], caps[1], caps[2], order[0], order[1], order[2], U, X)
    return U, X


# ------------------------------------------------------------------ statics
def constant_game(inst, space):
    """payoff arrays of the constant-bid game, bid sets per role (a prefix 0..cap), and the seller's statistics, as (3, nP, nA, nB) arrays."""
    v = INSTANCES[inst]
    caps = (R - 1,) * 3 if space == 'unrestricted' else tuple(v)
    U, X = build_tensor_const(inst)
    sl = (slice(0, caps[0] + 1), slice(0, caps[1] + 1), slice(0, caps[2] + 1))
    return U[(slice(None),) + sl], X[(slice(None),) + sl], caps


_CONST = {}


def build_tensor_const(inst):
    if inst not in _CONST:
        _CONST[inst] = build_tensor(inst, 'unrestricted', False)
    return _CONST[inst]


def pure_nash(inst, space):
    """all pure Nash equilibria of the constant-bid game: every role's bid maximizes its own expected payoff against the others' bids."""
    U, X, caps = constant_game(inst, space)
    ok = np.ones(U.shape[1:], bool)
    for r in range(3):
        best = U[r].max(axis=r, keepdims=True)
        ok &= U[r] >= best - 1e-9
    idx = np.argwhere(ok)
    return idx, U, X, caps


def nash_report(inst, space):
    v = INSTANCES[inst]
    idx, U, X, caps = pure_nash(inst, space)
    mr = min_revenue(v); ws = wstar(v)
    rows = []
    for (bP, bA, bB) in idx:
        u = (U[0, bP, bA, bB], U[1, bP, bA, bB], U[2, bP, bA, bB])
        rows.append(dict(bids=(int(bP), int(bA), int(bB)), u=tuple(float(x) for x in u), rev=float(X[XREV, bP, bA, bB]), eff=float(X[XEFF, bP, bA, bB]),
                         core=float(X[XCORE, bP, bA, bB]), mean_core=bool(in_core(v, u, float(X[XREV, bP, bA, bB])))))
    return dict(inst=inst, space=space, v=v, min_revenue=mr, wstar=ws, n=len(rows), rows=rows)


def summarize_nash(rep):
    rows = rep['rows']; mr = rep['min_revenue']; ws = rep['wstar']
    eff = [r for r in rows if r['eff'] > 1 - 1e-9]
    hist = {}
    for r in eff:
        hist[int(round(r['rev']))] = hist.get(int(round(r['rev'])), 0) + 1
    out = dict(inst=rep['inst'], space=rep['space'], n_nash=rep['n'], n_efficient=len(eff), n_in_core_certain=sum(r['core'] > 1 - 1e-9 for r in rows),
               n_in_core_mean=sum(r['mean_core'] for r in rows), min_revenue=mr, wstar=ws,
               revenue_min=min((r['rev'] for r in eff), default=None), revenue_max=max((r['rev'] for r in eff), default=None),
               revenue_hist_efficient=dict(sorted(hist.items())),
               n_efficient_below_core=sum(r['rev'] < mr - 1e-9 for r in eff), n_efficient_above_min_plus2=sum(r['rev'] > mr + 2 + 1e-9 for r in eff),
               n_efficient_not_core=sum(not r['mean_core'] for r in eff),
               n_inefficient=len(rows) - len(eff))
    return out


def edge_baseline(inst, space):
    """the split statistic's chance baseline: among integer split points of the bidder-optimal edge (revenue within one tick of the minimum, in
    the core), the share within one tick per winner of the Vickrey-nearest point."""
    v = INSTANCES[inst]
    vn = vickrey_nearest(v)
    if 'A' not in vn:
        return dict(n_edge=0, n_near=0, baseline=None, vn=vn)
    edge = bidder_optimal_edge(v, space)
    near = [(pa, pb) for (pa, pb) in edge if abs(pa - vn['A']) <= 1 + TOL and abs(pb - vn['B']) <= 1 + TOL]
    return dict(n_edge=len(edge), n_near=len(near), baseline=len(near) / len(edge) if edge else None, vn=vn, edge=edge)


# ------------------------------------------------------------------ priors and founders
def allowed(inst, space):
    v = INSTANCES[inst]
    return (R - 1,) * 3 if space == 'unrestricted' else tuple(v)


def prior(inst, space, m_pru=0.0):
    """per-role prior over the K programs: uniform over the allowed constants (mass 1 - m) and PRU(c) with default uniform over the same set (mass m)."""
    caps = allowed(inst, space)
    K = 2 * NC if m_pru > 0 else NC
    p = np.zeros((3, K))
    for r in range(3):
        n = caps[r] + 1
        p[r, :n] = (1 - m_pru) / n
        if m_pru > 0:
            p[r, NC:NC + n] = m_pru / n
    return p


def seed_counts(pr, I, N, rng):
    K = pr.shape[1]
    out = np.zeros((I, 3, K), np.int64)
    for i in range(I):
        for r in range(3):
            out[i, r] = rng.multinomial(N, pr[r])
    return out


def _load_annealed_schedule():
    """the repo's annealed re-injection schedule, loaded from src/annealed.py without executing its module body (its imports need run data
    that a fresh worktree lacks): the functions `eps_n_annealed`, `delivered` and the constants ONSET, HORIZON are taken from the source."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'annealed.py')
    tree = ast.parse(open(path).read())
    keep = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ('eps_n_annealed', 'delivered'):
            keep.append(node)
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ('ONSET', 'HORIZON') for t in node.targets):
            keep.append(node)
    ns = {'np': np}
    exec(compile(ast.Module(body=keep, type_ignores=[]), path, 'exec'), ns)
    return ns


_ANN = None


def eps_schedule(kind, N, A=0.0, gens=5000, epsN=0.05):
    """per-event mutation probability eps_g for g < len: 'zero'; 'ann' the repo's annealed tail (A founders per role per island, t0 = N/2,
    onset ONSET); 'rain' constant epsN founders per role per island per generation."""
    global _ANN
    if kind == 'zero':
        return np.zeros(1)
    if kind == 'ann':
        if _ANN is None:
            _ANN = _load_annealed_schedule()
        en = _ANN['eps_n_annealed'](N, A, _ANN['ONSET'], gens)
        return (en / N).astype(np.float64)
    if kind == 'rain':
        return np.full(gens, epsN / N)
    raise ValueError(kind)


# ------------------------------------------------------------------ island statistics (numba)
@njit(cache=True)
def _stats(U, X, counts, i, N, row):
    """the sampled statistic vector of island i into `row` (NS floats): the encounter-weighted means over the present program triples."""
    K = counts.shape[2]
    row[:] = 0.0
    bsum = np.zeros((3, K))
    for a in range(K):
        ca = counts[i, 0, a]
        if ca == 0:
            continue
        for b in range(K):
            cb = counts[i, 1, b]
            if cb == 0:
                continue
            for c in range(K):
                cc = counts[i, 2, c]
                if cc == 0:
                    continue
                p = ca * cb * cc / (N * N * N * 1.0)
                row[0] += p * U[0, a, b, c]; row[1] += p * U[1, a, b, c]; row[2] += p * U[2, a, b, c]
                row[3] += p * X[XREV, a, b, c]; row[4] += p * X[XEFF, a, b, c]; row[5] += p * X[XIR, a, b, c]
                row[6] += p * X[XCORE, a, b, c]; row[7] += p * X[XPRUWIN, a, b, c]; row[8] += p * X[XCYC, a, b, c]
                bsum[0, a] += (cb * cc / (N * N * 1.0)) * X[XBP, a, b, c]
                bsum[1, b] += (ca * cc / (N * N * 1.0)) * X[XBA, a, b, c]
                bsum[2, c] += (ca * cb / (N * N * 1.0)) * X[XBB, a, b, c]
    for r in range(3):
        mx = -1.0
        tot = 0
        npr = 0
        pru = 0.0
        for k in range(K):
            if counts[i, r, k] > 0:
                if bsum[r, k] > mx:
                    mx = bsum[r, k]
                npr += 1
                if k >= NC:
                    pru += counts[i, r, k]
        row[9 + r] = mx
        row[15 + r] = pru / N
        # weighted median of the present programs' mean bids
        vals = np.zeros(npr); wts = np.zeros(npr)
        t = 0
        for k in range(K):
            if counts[i, r, k] > 0:
                vals[t] = bsum[r, k]; wts[t] = counts[i, r, k]; t += 1
        o = np.argsort(vals)
        acc = 0.0
        med = vals[o[npr - 1]]
        for t in range(npr):
            acc += wts[o[t]]
            if acc >= N / 2.0:
                med = vals[o[t]]
                break
        row[12 + r] = med


# ------------------------------------------------------------------ the dynamics (numba)
@njit(cache=True)
def _tri(r, kr, s, ks, t, kt):
    kp = kr if r == 0 else (ks if s == 0 else kt)
    ka = kr if r == 1 else (ks if s == 1 else kt)
    kb = kr if r == 2 else (ks if s == 2 else kt)
    return kp, ka, kb


@njit(cache=True)
def _payoff_of(U, counts, i, r, k):
    """unnormalized expected payoff sum_{x,y} c_x c_y U_r of program k in role r on island i."""
    K = counts.shape[2]
    s = (r + 1) % 3; t = (r + 2) % 3
    tot = 0.0
    for x in range(K):
        cx = counts[i, s, x]
        if cx == 0:
            continue
        for y in range(K):
            cy = counts[i, t, y]
            if cy == 0:
                continue
            kp, ka, kb = _tri(r, k, s, x, t, y)
            tot += cx * cy * U[r, kp, ka, kb]
    return tot


@njit(cache=True)
def _fit(counts, pay, i, r, pres, npres, N, w):
    m = -1e300
    for t in range(npres[i, r]):
        k = pres[i, r, t]
        f = pay[i, r, k] / (N * N)
        if f > m:
            m = f
    tot = 0.0
    for t in range(npres[i, r]):
        k = pres[i, r, t]
        tot += counts[i, r, k] * np.exp(w * (pay[i, r, k] / (N * N) - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[i, r]):
        k = pres[i, r, t]
        acc += counts[i, r, k] * np.exp(w * (pay[i, r, k] / (N * N) - m))
        if u <= acc:
            return k
    return pres[i, r, npres[i, r] - 1]


@njit(cache=True)
def sim(U, X, init, N, w, m, gens, seed, sched, cdf, samples, minrev):
    """Three populations per island.  `sched[g]` is the per-event founder probability at generation g (0 beyond its length); a founder is drawn
    from `cdf[r]` (the role's prior) and replaces a uniformly chosen program.  m > 0: per-role migration, the child's source island uniform
    among the others, the child drawn in the source by the role's own fitness.  Returns the final counts, the sampled statistics
    (len(samples), I, NS), the first sampled generation at which an island was eroded (revenue < minrev - 1; -1: never) the stop generation and the incrementally maintained unnormalized payoffs (a test compares them with a recomputation)."""
    np.random.seed(seed)
    I = init.shape[0]; K = init.shape[2]
    counts = init.copy()
    pay = np.zeros((I, 3, K))
    pres = np.zeros((I, 3, K), np.int64); npres = np.zeros((I, 3), np.int64); pos = -np.ones((I, 3, K), np.int64)
    for i in range(I):
        for r in range(3):
            for k in range(K):
                if counts[i, r, k] > 0:
                    pres[i, r, npres[i, r]] = k; pos[i, r, k] = npres[i, r]; npres[i, r] += 1
        for r in range(3):
            for k in range(K):
                if counts[i, r, k] > 0:
                    pay[i, r, k] = _payoff_of(U, counts, i, r, k)
    ns = samples.shape[0]
    samp = np.zeros((ns, I, NS))
    first_erode = -np.ones(I, np.int64)
    row = np.zeros(NS)
    nsched = sched.shape[0]
    si = 0
    stop_g = gens
    for g in range(gens + 1):
        # sampling at the generation boundary
        while si < ns and samples[si] <= g:
            for i in range(I):
                _stats(U, X, counts, i, N, row)
                samp[si, i, :] = row
                if first_erode[i] < 0 and row[3] < minrev - 1.0 - 1e-9:
                    first_erode[i] = samples[si]
            si += 1
        if g == gens:
            break
        eps = sched[g] if g < nsched else 0.0
        if eps == 0.0 and m == 0.0:
            allfix = True
            for i in range(I):
                if npres[i, 0] > 1 or npres[i, 1] > 1 or npres[i, 2] > 1:
                    allfix = False; break
            if allfix and g >= nsched:
                stop_g = g
                break
        for e in range(3 * I * N):
            i = np.random.randint(I)
            r = np.random.randint(3)
            mut = False
            if eps > 0.0 and np.random.random() < eps:
                mut = True
            if (not mut) and m == 0.0 and npres[i, r] == 1:
                continue
            if mut:
                u0 = np.random.random(); child = K - 1
                for k in range(K):
                    if u0 <= cdf[r, k]:
                        child = k; break
            else:
                src = i
                if m > 0.0 and np.random.random() < m:
                    src = np.random.randint(I - 1)
                    if src >= i:
                        src += 1
                child = _fit(counts, pay, src, r, pres, npres, N, w)
            u1 = np.random.randint(N); acc = 0; victim = pres[i, r, 0]
            for t in range(npres[i, r]):
                k = pres[i, r, t]; acc += counts[i, r, k]
                if u1 < acc:
                    victim = k; break
            if victim == child:
                continue
            # payoffs of the other roles' present programs change by the swap victim -> child
            s1 = (r + 1) % 3; s2 = (r + 2) % 3
            for dd in range(2):
                s = s1 if dd == 0 else s2
                t3 = s2 if dd == 0 else s1
                for q in range(npres[i, s]):
                    k = pres[i, s, q]
                    d = 0.0
                    for z in range(npres[i, t3]):
                        y = pres[i, t3, z]
                        kp, ka, kb = _tri(r, child, s, k, t3, y)
                        kp2, ka2, kb2 = _tri(r, victim, s, k, t3, y)
                        d += counts[i, t3, y] * (U[s, kp, ka, kb] - U[s, kp2, ka2, kb2])
                    pay[i, s, k] += d
            counts[i, r, victim] -= 1
            if counts[i, r, victim] == 0:
                q = pos[i, r, victim]; last = pres[i, r, npres[i, r] - 1]
                pres[i, r, q] = last; pos[i, r, last] = q; pos[i, r, victim] = -1; npres[i, r] -= 1
            newp = False
            if counts[i, r, child] == 0:
                pres[i, r, npres[i, r]] = child; pos[i, r, child] = npres[i, r]; npres[i, r] += 1
                newp = True
            counts[i, r, child] += 1
            if newp:
                pay[i, r, child] = _payoff_of(U, counts, i, r, child)
    # a run stopped early (all islands fixed, no further arrivals): the remaining samples repeat the final state
    if stop_g < gens:
        while si < ns:
            for i in range(I):
                _stats(U, X, counts, i, N, row)
                samp[si, i, :] = row
            si += 1
    return counts, samp, first_erode, stop_g, pay


# ------------------------------------------------------------------ sample times and run helpers
def sample_times(gens):
    base = [0, 1, 2, 5, 10, 20, 30, 50, 75, 100, 150, 200, 250, 300, 400, 500, 750, 1000, 1500, 2000]
    t = [x for x in base if x < gens]
    x = 2500
    step = 500 if gens <= 5000 else 1000
    while x < gens:
        t.append(x); x += step
    t.append(gens)
    return np.array(sorted(set(t)), np.int64)


def cdf_of(pr):
    c = np.cumsum(pr, axis=1)
    c[c >= c[:, -1:] - 1e-12] = 1.0
    return c


def island_core_mean(inst, row):
    """the core flag of an island from its mean payoff vector and mean revenue (statistics row)."""
    v = INSTANCES[inst]
    return in_core(v, (row[0], row[1], row[2]), row[3])


def island_table(inst, samp_final, counts_final, N):
    """per-island end-state columns from the final statistic rows (I, NS) and counts."""
    v = INSTANCES[inst]
    mr = min_revenue(v)
    vn = vickrey_nearest(v)
    I = samp_final.shape[0]
    rows = []
    for i in range(I):
        s = samp_final[i]
        core = island_core_mean(inst, s)
        row = dict(uP=s[0], uA=s[1], uB=s[2], rev=s[3], eff=s[4], ir=s[5], core_enc=s[6], pruwin=s[7], cyc=s[8],
                   bmaxP=s[9], bmaxA=s[10], bmaxB=s[11], bmedP=s[12], bmedA=s[13], bmedB=s[14], pruP=s[15], pruA=s[16], pruB=s[17],
                   eroded=bool(s[3] < mr - 1 - 1e-9), core=bool(core), edge=bool(core and s[3] <= mr + 1 + 1e-6))
        if 'A' in vn:
            row['at_vn'] = bool(row['edge'] and abs(s[1] - (v[1] - vn['A'])) <= 1 + 1e-6 and abs(s[2] - (v[2] - vn['B'])) <= 1 + 1e-6)
        else:
            row['at_vn'] = bool(row['edge'])
        rows.append(row)
    return rows
