"""Coalition-proof auctions: the RS's one-round notion on small package auctions (spec specs/2026-10-21-coalition-proof-auctions.md;
notes notes/coalition-proof-auctions.md; predictions predictions/2026-10-21-coalition-proof-auctions.md).

Core library (Part A and the payoff machinery of Part B):

* `Auction`: single-minded bidders on a small item set, integer reports 0..R-1, all report profiles tabulated at once.
  Winner determination maximizes reported welfare; ties go to the allocation with more winners, then to the
  lexicographically lowest bidder-index tuple.  Rules: `vcg`, `surcharge` (minimum-revenue core with respect to reports,
  VCG-nearest in Euclidean distance; exact for <= 2 winners, LP + SLSQP generically), `fp` (first price).
* `group_kernel` (numba): for a proper coalition S and the complement's true values, every deviation d_S of S and the
  complement's response set under R1 (pure Nash equilibria in the closure of the finite best-reply graph from the complement's
  truthful reports) or R2 (joint maximizers of the complement's total payoff); the five variants below.
* `analyze`: instance-level break flags, leader values and the grand ring.
* `twoxl_leader_values`: the 2XL commitment race (notes 8).

Reports are integers; payments of the surcharge rule are multiples of 1/2.  Scale the note's decimal examples by 10.

Variants (index into the kernel's first axis):
  0 R1 / T-strict   strict-improvement graph, NE of the closure closest to truth in L1 (ties: smallest report vector)
  1 R1 / T-weak     any-best-reply graph (lateral moves among best replies allowed), NE of the closure worst for S
  2 R1 / T-weak-literal   strict graph, NE of the closure worst for S
  3 R2 / T-strict   maximizers of the complement's total payoff closest to truth in L1
  4 R2 / T-weak     maximizers worst for S
"""
import os, sys, math, itertools
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abm import njit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOL = 1e-9
VARIANTS = ('R1_strict', 'R1_weak', 'R1_weak_literal', 'R2_strict', 'R2_weak')
NV = 5

# bidder packages as item bitmasks (A = 1, B = 2)
FAMILIES = {
    'AM': (3, 1, 2),          # bidder 1 on AB, bidder 2 on A, bidder 3 on B
    'AMplus': (3, 1, 2, 1),   # plus bidder 4 on A
    'subs': (1, 1, 2, 2),     # substitutes: 1, 2 on A and 3, 4 on B
    'twopk': (3, 3, 1, 2),    # two packages: 1, 2 on AB, 3 on A, 4 on B
}
RULES = ('vcg', 'surcharge', 'fp')


# ------------------------------------------------------------------ the auction tables
class Auction:
    """All report profiles (mixed radix, bidder 0 least significant) with allocation and payments for each rule."""

    def __init__(self, packages, R):
        self.pk = tuple(int(p) for p in packages)
        self.n = n = len(packages)
        self.R = R
        self.M = M = R ** n
        self.base = np.array([R ** i for i in range(n)], np.int64)
        idx = np.arange(M)
        self.B = np.stack([(idx // self.base[i]) % R for i in range(n)], axis=1).astype(np.int64)
        feas = []
        for F in range(1 << n):
            used = 0; ok = True
            for i in range(n):
                if F >> i & 1:
                    if used & self.pk[i]:
                        ok = False; break
                    used |= self.pk[i]
            if ok:
                feas.append(F)
        self.feas = feas
        WF = {F: sum(self.B[:, i] * ((F >> i) & 1) for i in range(n)) for F in feas}
        self.WF = WF
        popc = lambda F: bin(F).count('1')
        tup = lambda F: tuple(i for i in range(n) if F >> i & 1)
        order = sorted(feas, key=lambda F: tup(F))       # lexicographic tuple rank (smaller tuple = better)
        rank = {F: r for r, F in enumerate(order)}
        score = None; best = None
        for F in feas:
            sc = WF[F] * 100000 + popc(F) * 1000 + (999 - rank[F])
            if score is None:
                score = sc.copy(); best = np.full(M, F, np.int64)
            else:
                m = sc > score
                score = np.where(m, sc, score); best = np.where(m, F, best)
        self.alloc = best                                  # winner bitmask per profile
        self.W = np.zeros(M, np.int64)
        for F in feas:
            self.W = np.where(best == F, WF[F], self.W)
        self.Wex = {}
        for S in range(1 << n):                           # max welfare among allocations disjoint from bidder set S
            w = np.zeros(M, np.int64)
            for F in feas:
                if F & S == 0:
                    w = np.maximum(w, WF[F])
            self.Wex[S] = w
        self.win = np.stack([(best >> i) & 1 for i in range(n)], axis=1).astype(np.int8)
        self._pay = {}

    def encode(self, b):
        return int(np.dot(np.asarray(b, np.int64), self.base))

    def payments(self, rule):
        if rule in self._pay:
            return self._pay[rule]
        n, M = self.n, self.M
        if rule == 'fp':
            pay = self.B.astype(np.float64) * self.win
        else:
            pv = np.zeros((M, n))
            for i in range(n):
                pv[:, i] = (self.Wex[1 << i] - (self.W - self.B[:, i])) * self.win[:, i]
            if rule == 'vcg':
                pay = pv
            elif rule == 'surcharge':
                pay = self._surcharge(pv)
            else:
                raise ValueError(rule)
        self._pay[rule] = pay
        return pay

    def tables(self, rule):
        return self.win, self.payments(rule)

    # exact minimum-revenue core payments, VCG-nearest, for <= 2 winners; generic (scipy) otherwise
    def _surcharge(self, pv):
        n, M = self.n, self.M
        Wm = self.alloc
        nw = np.array([bin(F).count('1') for F in range(1 << n)])[Wm]
        cand = {s: np.full(M, -1e18) for s in range(1 << n)}
        for S in range(1, 1 << n):
            cS = np.zeros(M)
            for i in range(n):
                if S >> i & 1:
                    cS = cS + self.B[:, i] * self.win[:, i]
            cS = cS - (self.W - self.Wex[S])
            sub = S & Wm
            for s in range(1 << n):
                m = sub == s
                if m.any():
                    cand[s] = np.where(m, np.maximum(cand[s], cS), cand[s])
        pay = np.zeros((M, n))
        for i in range(n):
            m = (Wm == (1 << i))
            pay[m, i] = np.minimum(np.maximum(cand[1 << i][m], 0.0), self.B[m, i])
        for i in range(n):
            for j in range(i + 1, n):
                w = (1 << i) | (1 << j)
                m = Wm == w
                if not m.any():
                    continue
                ai = cand[1 << i][m]; aj = cand[1 << j][m]; aij = cand[w][m]
                bi = self.B[m, i].astype(float); bj = self.B[m, j].astype(float)
                Rs = np.maximum(ai + aj, aij)
                lo = np.maximum(ai, Rs - bj); hi = np.minimum(bi, Rs - aj)
                mid = pv[m, i] + (Rs - pv[m, i] - pv[m, j]) / 2.0
                pi = np.clip(mid, lo, hi)
                pay[m, i] = pi; pay[m, j] = Rs - pi
        big = np.nonzero(nw >= 3)[0]
        for k in big:                                       # generic path (not used by the four families)
            pay[k] = surcharge_generic(self.B[k], self.pk, self)
        return pay


def surcharge_generic(bids, packages, auc=None):
    """minimum-revenue core payments w.r.t. the reports, VCG-nearest, by LP then SLSQP over all blocking coalitions."""
    from scipy.optimize import linprog, minimize
    n = len(packages)
    auc = auc or Auction(packages, max(bids) + 1)
    k = auc.encode(bids)
    Wm = int(auc.alloc[k]); winners = [i for i in range(n) if Wm >> i & 1]
    if not winners:
        return np.zeros(n)
    b = np.asarray(bids, float)
    pv = np.array([auc.Wex[1 << i][k] - (auc.W[k] - b[i]) if i in winners else 0.0 for i in range(n)])
    rows, rhs = [], []
    for S in range(1, 1 << n):
        sw = [i for i in winners if S >> i & 1]
        if not sw:
            continue
        # sum_{i in S∩W} (b_i - p_i) <= w(N) - w(N\S)  <=>  -sum p >= -(...)  ->  sum p >= sum b - joint
        rows.append([1.0 if i in sw else 0.0 for i in winners])
        rhs.append(sum(b[i] for i in sw) - (auc.W[k] - auc.Wex[S][k]))
    A = np.array(rows); c = np.array(rhs)
    bounds = [(0, b[i]) for i in winners]
    res = linprog(np.ones(len(winners)), A_ub=-A, b_ub=-c, bounds=bounds, method='highs')
    Rstar = res.fun
    x0 = np.array([pv[i] for i in winners])
    cons = [dict(type='ineq', fun=lambda x: A @ x - c), dict(type='eq', fun=lambda x: x.sum() - Rstar)]
    sol = minimize(lambda x: ((x - x0) ** 2).sum(), res.x, constraints=cons, bounds=bounds, method='SLSQP',
                   options=dict(ftol=1e-14, maxiter=500))
    out = np.zeros(n)
    for t, i in enumerate(winners):
        out[i] = sol.x[t]
    return out


# ------------------------------------------------------------------ the notion kernel
@njit(cache=True)
def _pf(win, pay, idx, i, v):
    return v * win[idx, i] - pay[idx, i]


@njit(cache=True)
def _build_tables(win, pay, R, bC, nC, Cl, vals, idxS, P, BL):
    """P[j, lc]: payoff of complement member j at the complement profile lc (S's reports fixed through idxS); BL[j, lc]: the best
    payoff j can reach by changing only its own report from lc."""
    nlc = R ** nC
    pw = np.empty(nC, np.int64)
    for j in range(nC):
        pw[j] = R ** j
    for lc in range(nlc):
        idx = idxS
        for j in range(nC):
            idx += ((lc // pw[j]) % R) * bC[j]
        for j in range(nC):
            P[j, lc] = _pf(win, pay, idx, Cl[j], vals[Cl[j]])
    for j in range(nC):
        for lc in range(nlc):
            if (lc // pw[j]) % R == 0:
                m = -1e300
                for b in range(R):
                    x = P[j, lc + b * pw[j]]
                    if x > m:
                        m = x
                for b in range(R):
                    BL[j, lc + b * pw[j]] = m


@njit(cache=True)
def _r1_closure(P, BL, R, nC, start_lc, weak, queue, visited, stamp, ne_out):
    """pure NE of the complement subgame in the closure of the best-reply graph from `start_lc` (strict-improvement moves, or
    moves to any best reply when `weak`); returns their number."""
    pw = np.empty(nC, np.int64)
    for j in range(nC):
        pw[j] = R ** j
    qh = 0; qt = 0
    queue[qt] = start_lc; qt += 1; visited[start_lc] = stamp
    nne = 0
    while qh < qt:
        lc = queue[qh]; qh += 1
        is_ne = True
        for j in range(nC):
            rj = (lc // pw[j]) % R
            best = BL[j, lc]
            cur = P[j, lc]
            base_lc = lc - rj * pw[j]
            if cur < best - 1e-9:
                is_ne = False
                for b in range(R):
                    if P[j, base_lc + b * pw[j]] >= best - 1e-9:
                        nl = base_lc + b * pw[j]
                        if visited[nl] != stamp:
                            visited[nl] = stamp; queue[qt] = nl; qt += 1
            elif weak:
                for b in range(R):
                    if b != rj and P[j, base_lc + b * pw[j]] >= best - 1e-9:
                        nl = base_lc + b * pw[j]
                        if visited[nl] != stamp:
                            visited[nl] = stamp; queue[qt] = nl; qt += 1
        if is_ne:
            ne_out[nne] = lc; nne += 1
    return nne


@njit(cache=True)
def _r2_set(P, nC, nlc, ne_out):
    best = -1e300; nne = 0
    for lc in range(nlc):
        tot = 0.0
        for j in range(nC):
            tot += P[j, lc]
        if tot > best + 1e-9:
            best = tot; nne = 0; ne_out[nne] = lc; nne += 1
        elif tot >= best - 1e-9:
            ne_out[nne] = lc; nne += 1
    return nne


@njit(cache=True)
def _closest(ne, nne, R, nC, vals, Cl):
    """index of the response closest to the complement's truthful reports in L1 (ties: smallest code)."""
    bestd = 1 << 60; bl = -1
    for t in range(nne):
        lc = ne[t]; d = 0
        for j in range(nC):
            rj = (lc // (R ** j)) % R
            d += abs(rj - vals[Cl[j]])
        if d < bestd or (d == bestd and lc < bl):
            bestd = d; bl = lc
    return bl


@njit(cache=True)
def group_kernel(win, pay, n, R, Rd, G, Sl, Cl, vC, base, gain, arg, lead, unres, nresp):
    """For the coalition Sl (array of bidder indices) and the complement Cl with true values vC (array of length n; entries
    of Sl ignored), loop over every deviation d_S and every true-value vector of S in 1..G.
    gain[k, vs]: max over d_S != v_S of (S's total after the response) - (S's truthful total) under variant k; arg[k, vs]:
    argmax d_S code; lead[k, vs]: max over all d_S of S's total after the response (leader value); unres[k]: number of d_S
    with no response in the closure; nresp[k, 0], nresp[k, 1]: number of (d_S) with a response set larger than one and the
    maximum set size."""
    nS = Sl.shape[0]; nC = Cl.shape[0]
    bS = np.empty(nS, np.int64); bC = np.empty(nC, np.int64)
    for s in range(nS):
        bS[s] = base[Sl[s]]
    for j in range(nC):
        bC[j] = base[Cl[j]]
    nvS = G ** nS; nds = Rd ** nS; nlc = R ** nC
    vals = vC.copy()
    vS = np.empty((nvS, nS), np.int64)
    ttruth = np.empty(nvS)
    idxC_truth = 0
    for j in range(nC):
        idxC_truth += vC[Cl[j]] * bC[j]
    for vs in range(nvS):
        idx = idxC_truth
        for s in range(nS):
            vS[vs, s] = 1 + (vs // (G ** s)) % G
            idx += vS[vs, s] * bS[s]
        t = 0.0
        for s in range(nS):
            t += _pf(win, pay, idx, Sl[s], vS[vs, s])
        ttruth[vs] = t
    lc_truth = 0
    for j in range(nC):
        lc_truth += vC[Cl[j]] * (R ** j)
    queue = np.empty(nlc, np.int64); visited = np.zeros(nlc, np.int64)
    ne_s = np.empty(nlc, np.int64); ne_w = np.empty(nlc, np.int64); ne_2 = np.empty(nlc, np.int64)
    P = np.empty((nC, nlc)); BL = np.empty((nC, nlc))
    mp_w = np.empty(1 << nS); mp_s = np.empty(1 << nS); mp_2 = np.empty(1 << nS)
    stamp = 0
    for k in range(5):
        for vs in range(nvS):
            gain[k, vs] = -1e18; arg[k, vs] = -1; lead[k, vs] = -1e18
        unres[k] = 0
        nresp[k, 0] = 0; nresp[k, 1] = 0
    dd = np.empty(nS, np.int64)
    for ds in range(nds):
        idxS = 0
        for s in range(nS):
            dd[s] = (ds // (Rd ** s)) % Rd
            idxS += dd[s] * bS[s]
        _build_tables(win, pay, R, bC, nC, Cl, vals, idxS, P, BL)
        stamp += 1
        n_s = _r1_closure(P, BL, R, nC, lc_truth, False, queue, visited, stamp, ne_s)
        stamp += 1
        n_w = _r1_closure(P, BL, R, nC, lc_truth, True, queue, visited, stamp, ne_w)
        n_2 = _r2_set(P, nC, nlc, ne_2)
        c_s = _closest(ne_s, n_s, R, nC, vals, Cl) if n_s > 0 else -1
        c_2 = _closest(ne_2, n_2, R, nC, vals, Cl)
        if n_s == 0: unres[0] += 1; unres[2] += 1
        if n_w == 0: unres[1] += 1
        if n_s > 1: nresp[0, 0] += 1
        if n_w > 1: nresp[1, 0] += 1
        if n_2 > 1: nresp[3, 0] += 1
        nresp[0, 1] = max(nresp[0, 1], n_s); nresp[1, 1] = max(nresp[1, 1], n_w); nresp[3, 1] = max(nresp[3, 1], n_2)
        _patterns(win, pay, idxS, ne_w, n_w, R, bC, nC, Sl, nS, mp_w)
        _patterns(win, pay, idxS, ne_s, n_s, R, bC, nC, Sl, nS, mp_s)
        _patterns(win, pay, idxS, ne_2, n_2, R, bC, nC, Sl, nS, mp_2)
        for vs in range(nvS):
            same = True
            for s in range(nS):
                if dd[s] != vS[vs, s]:
                    same = False
            for k in range(5):
                has = False; val = 0.0
                if k == 0 and n_s > 0:
                    has = True; val = _stotal(win, pay, idxS, c_s, R, bC, nC, Sl, vS, vs, nS)
                elif k == 3:
                    has = True; val = _stotal(win, pay, idxS, c_2, R, bC, nC, Sl, vS, vs, nS)
                elif k == 1 and n_w > 0:
                    has = True; val = _worst(mp_w, vS, vs, nS)
                elif k == 2 and n_s > 0:
                    has = True; val = _worst(mp_s, vS, vs, nS)
                elif k == 4:
                    has = True; val = _worst(mp_2, vS, vs, nS)
                if not has:
                    continue
                if val > lead[k, vs]:
                    lead[k, vs] = val
                if not same:
                    g = val - ttruth[vs]
                    if g > gain[k, vs]:
                        gain[k, vs] = g; arg[k, vs] = ds


@njit(cache=True)
def _patterns(win, pay, idxS, ne, nne, R, bC, nC, Sl, nS, mp):
    """mp[pattern]: the largest total payment of S over responses in `ne` at which exactly the S-members in `pattern` win."""
    for q in range(1 << nS):
        mp[q] = -1e18
    for t in range(nne):
        lc = ne[t]
        idx = idxS
        for j in range(nC):
            idx += ((lc // (R ** j)) % R) * bC[j]
        pat = 0; ps = 0.0
        for s in range(nS):
            if win[idx, Sl[s]]:
                pat |= (1 << s)
            ps += pay[idx, Sl[s]]
        if ps > mp[pat]:
            mp[pat] = ps


@njit(cache=True)
def _worst(mp, vS, vs, nS):
    val = 1e18
    for q in range(1 << nS):
        if mp[q] > -1e17:
            x = -mp[q]
            for s in range(nS):
                if (q >> s) & 1:
                    x += vS[vs, s]
            if x < val:
                val = x
    return val


@njit(cache=True)
def _stotal(win, pay, idxS, lc, R, bC, nC, Sl, vS, vs, nS):
    idx = idxS
    for j in range(nC):
        idx += ((lc // (R ** j)) % R) * bC[j]
    t = 0.0
    for s in range(nS):
        t += _pf(win, pay, idx, Sl[s], vS[vs, s])
    return t


def response_set(auc, rule, Sl, vals, dS, kind):
    """Python wrapper: response sets (list of complement report tuples) for a single deviation (for the spite margin)."""
    win, pay = auc.tables(rule)
    n, R = auc.n, auc.R
    Sl = np.array(Sl, np.int64); Cl = np.array([i for i in range(n) if i not in set(Sl.tolist())], np.int64)
    nC = len(Cl); nlc = R ** nC
    bC = np.array([auc.base[i] for i in Cl], np.int64)
    idxS = int(sum(int(dS[s]) * int(auc.base[Sl[s]]) for s in range(len(Sl))))
    vals = np.asarray(vals, np.int64)
    lc_truth = sum(int(vals[Cl[j]]) * R ** j for j in range(nC))
    queue = np.empty(nlc, np.int64); visited = np.zeros(nlc, np.int64); ne = np.empty(nlc, np.int64)
    P = np.empty((nC, nlc)); BL = np.empty((nC, nlc))
    _build_tables(np.ascontiguousarray(win), np.ascontiguousarray(pay), R, bC, nC, Cl, vals, idxS, P, BL)
    if kind == 'r2':
        m = _r2_set(P, nC, nlc, ne)
    else:
        m = _r1_closure(P, BL, R, nC, lc_truth, kind == 'weak', queue, visited, 1, ne)
    return [tuple(int((ne[t] // R ** j) % R) for j in range(nC)) for t in range(m)], Cl.tolist()


# ------------------------------------------------------------------ instances and analysis
def all_instances(n, G):
    idx = np.arange(G ** n)
    return np.stack([1 + (idx // G ** i) % G for i in range(n)], axis=1).astype(np.int64)


def subsets(n):
    """proper nonempty bidder subsets as sorted tuples."""
    out = []
    for m in range(1, (1 << n) - 1):
        out.append(tuple(i for i in range(n) if m >> i & 1))
    return out


def analyze(auc, rule, G, mask=None, Rd=None, verbose=False):
    """For every instance (true values in 1..G) and proper coalition S: gain[k, inst, S], lead[k, inst, S], unresolved flags.
    `mask` (bool over the G**n instances) restricts which v_C groups are evaluated (others are left at -1e18).  `Rd` restricts
    the deviators' reports to 0..Rd-1 (responders use 0..R-1; default Rd = R: one common grid)."""
    n, R = auc.n, auc.R
    Rd = R if Rd is None else Rd
    win, pay = auc.tables(rule)
    win = np.ascontiguousarray(win); pay = np.ascontiguousarray(pay)
    NI = G ** n
    insts = all_instances(n, G)
    SS = subsets(n)
    gain = np.full((NV, NI, len(SS)), -1e18); lead = np.full((NV, NI, len(SS)), -1e18)
    arg = np.full((NV, NI, len(SS)), -1, np.int64)
    unres = np.zeros((NV, NI, len(SS)), np.int64)
    nmulti = np.zeros((NV, len(SS)), np.int64)
    maxset = np.zeros((NV, len(SS)), np.int64)
    pw = [G ** i for i in range(n)]
    for si, S in enumerate(SS):
        C = [i for i in range(n) if i not in S]
        Sl = np.array(S, np.int64); Cl = np.array(C, np.int64)
        # distinct v_C values present
        vCs = {}
        for inst in np.nonzero(mask)[0] if mask is not None else range(NI):
            key = tuple(int(insts[inst, c]) for c in C)
            vCs[key] = True
        for key in vCs:
            vC = np.ones(n, np.int64)
            for c, v in zip(C, key):
                vC[c] = v
            nvS = G ** len(S)
            g = np.empty((NV, nvS)); a = np.empty((NV, nvS), np.int64); l = np.empty((NV, nvS))
            u = np.zeros(NV, np.int64); nr = np.zeros((NV, 2), np.int64)
            group_kernel(win, pay, n, R, Rd, G, Sl, Cl, vC, auc.base, g, a, l, u, nr)
            vCidx = sum((key[t] - 1) * pw[C[t]] for t in range(len(C)))
            for vs in range(nvS):
                inst = vCidx + sum((1 + (vs // G ** s) % G - 1) * pw[S[s]] for s in range(len(S)))
                gain[:, inst, si] = g[:, vs]; lead[:, inst, si] = l[:, vs]; arg[:, inst, si] = a[:, vs]
                unres[:, inst, si] = u
            nmulti[:, si] += nr[:, 0]; maxset[:, si] = np.maximum(maxset[:, si], nr[:, 1])
    return dict(gain=gain, lead=lead, arg=arg, unres=unres, SS=SS, insts=insts, nmulti=nmulti, maxset=maxset, Rd=Rd)


def truth_info(auc, rule, G):
    """per instance: winners at truth (bitmask), revenue, bidder payoffs, true efficient welfare."""
    n = auc.n
    insts = all_instances(n, G)
    idx = insts @ auc.base
    win, pay = auc.tables(rule)
    w = win[idx].astype(np.int64)
    p = pay[idx]
    u = insts * w - p
    return dict(insts=insts, idx=idx, winmask=auc.alloc[idx], revenue=p.sum(1), u=u, welfare=auc.W[idx], pay=p)


def vcg_in_core(auc, G):
    """surcharge == 0 at truthful reports (VCG in the core) per instance, and the surcharge total."""
    n = auc.n
    insts = all_instances(n, G)
    idx = insts @ auc.base
    pv = auc.payments('vcg')[idx]; ps = auc.payments('surcharge')[idx]
    d = (ps - pv)
    return (d.sum(1) < 1e-9), d.sum(1), d


def ring(auc, rule, G, insts=None):
    """the grand bidder coalition's best joint report (the ring of notes 4): max total bidder payoff, ties to the smaller
    total bid; returns per instance the best total, the revenue and true welfare at the optimum, the efficient welfare,
    and the argmax profile."""
    insts = all_instances(auc.n, G) if insts is None else insts
    win, pay = auc.tables(rule)
    return _ring(win, pay, auc.B, auc.W, auc.base, insts)


@njit(cache=True)
def _ring(win, pay, B, W, base, insts):
    NI = insts.shape[0]; M = win.shape[0]; n = win.shape[1]
    best = np.empty(NI); rev = np.empty(NI); wel = np.empty(NI); eff = np.empty(NI); arg = np.empty(NI, np.int64)
    for q in range(NI):
        t_idx = 0
        for i in range(n):
            t_idx += insts[q, i] * base[i]
        eff[q] = W[t_idx]
        bt = -1e18; bs = 1 << 30; ba = -1; br = 0.0; bw = 0.0
        for k in range(M):
            tot = 0.0; r = 0.0; w = 0.0; sb = 0
            for i in range(n):
                x = insts[q, i] * win[k, i]
                w += x
                tot += x - pay[k, i]
                r += pay[k, i]
                sb += B[k, i]
            if tot > bt + 1e-9 or (tot >= bt - 1e-9 and sb < bs):
                bt = tot; bs = sb; ba = k; br = r; bw = w
        best[q] = bt; rev[q] = br; wel[q] = bw; arg[q] = ba
    return best, rev, wel, eff, arg


# ------------------------------------------------------------------ 2XL (notes 8)
def twoxl_leader_values(vh, vl, top, tie='weak'):
    """one toy, two players, no seller; the higher report wins (ties to the high-value player h); the winner pays the
    loser's report to the loser.  Integer reports 0..top.  Returns (v_h, v_l): each player's leader value when it commits to
    a report and the other best-replies; `tie='weak'` resolves the follower's indifference against the leader, 'strict'
    in the leader's favour."""
    def payoffs(rh, rl):
        if rh >= rl:
            return vh - rl, rl
        return rh, vl - rh
    out = []
    for leader in (0, 1):
        best = -1e18
        for r in range(top + 1):
            f = 1 - leader
            vals = []
            for q in range(top + 1):
                pr = (r, q) if leader == 0 else (q, r)
                u = payoffs(*pr)
                vals.append((u[f], u[leader]))
            m = max(x[0] for x in vals)
            resp = [x[1] for x in vals if x[0] >= m - 1e-9]
            lead = min(resp) if tie == 'weak' else max(resp)
            best = max(best, lead)
        out.append(best)
    return tuple(out)


# ------------------------------------------------------------------ the AM closed forms (tests and notes)
def am_vcg_pay(bP, bA, bB):
    """VCG payments for the AM family on integer reports (bidder P on AB, A, B), with the module's tie rule."""
    a = Auction(FAMILIES['AM'], max(bP, bA, bB) + 1)
    k = a.encode((bP, bA, bB))
    return a.payments('vcg')[k], a.win[k]
