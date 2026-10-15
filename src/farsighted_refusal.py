"""Farsighted refusal (spec specs/2026-10-14-farsighted-refusal.md, reviewed by gpt-6.1-sol and gemini-4-argon; notes
notes/farsighted-refusal.md; predictions predictions/2026-10-14-farsighted-refusal.md).

Imports the dominance-contracts and stable-sets machinery and edits neither.

Static part: the contract process on the 20 realizable outcomes R of dollar3 (27 pair contracts, a uniform draw per
contract event, dominance required for proposal, consent by both members of S, discount delta per event); the
Konishi-Ray (KR) fixed points A(kappa, y) = 1 iff W_j(x) > W_j(y) for both members j, enumerated exhaustively by a
branch and bound with MDP bounds and verified in exact rational arithmetic; the frozen default-selection rule; per
fixed point its recurrent classes, absorption probabilities, stationary V* mass, hitting times and consent margins;
the guard tables g0, gV, g1, g1-x, gKR(delta).

Dynamic part: `fkern`, a copy of dominance_contracts.dkern restricted to menu F, beta = 1 and public consent, with a
heritable guard index in the genotype (program k, override o, guard g).  Static guards consent from a table
(y = the island's modal outcome, kappa, member position); a gKR-read guard solves the 20-state system under the
island's current guard composition (treating gKR and gKR-read copies as the default gKR table) and consents iff its
own value rises.  Draws of the consenting individuals are made iff some guard type present in either S slot would
refuse (so universal g0 reproduces D1 and universal gV reproduces R2 draw for draw).
"""
import itertools, os, sys
from fractions import Fraction
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numba import njit
import stable_sets as SS
import dominance_contracts as DC

ROOT = SS.ROOT
NCON = DC.NCON
GAME = SS.dollar3_game()
X = list(GAME.R)                                   # 20 outcomes, sixths
NX = len(X)
RIDX = {x: k for k, x in enumerate(X)}
UPAY = np.array(X, float)                          # (20, 3) sixths
V = sorted(SS.symmetric_set(X, 6))                 # [3, 9, 15]
LAB = [SS.label(x) for x in X]
CAT = [SS.category(x, 6) for x in X]
CS_, CD_, CACT_ = DC.contract_arrays()
CX = np.array([RIDX.get(DC.contract_x(k), 0) for k in range(NCON)], np.int64)   # contract -> outcome (0 if infeasible)
FEAS = np.array([CD_[k].sum() <= 6 for k in range(NCON)], np.bool_)
PROPM = np.zeros((NX, NCON), np.bool_)
for _y in range(NX):
    for _k in range(NCON):
        PROPM[_y, _k] = DC.proposed(_k, X[_y])
PROP = [(y, k) for y in range(NX) for k in range(NCON) if PROPM[y, k]]          # canonical order
NP = len(PROP)
PY = np.array([p[0] for p in PROP], np.int64)
PK = np.array([p[1] for p in PROP], np.int64)
PXX = CX[PK]
PM0 = CS_[PK, 0].copy(); PM1 = CS_[PK, 1].copy()


def _priority():
    rank = {'fair': 0, 'unequal': 1, 'wasteful': 2}
    def key(j):
        y = PY[j]; c = CAT[y]
        r = rank.get(c, 3)
        if c == 'wasteful' and sorted(X[y]) == [0, 2, 2]:
            r = 3
        return (r, j)
    return sorted(range(NP), key=key)


PRIO = _priority()


# ====================================================================== S3 symmetry
def perms():
    out = []
    for pi in itertools.permutations(range(3)):
        ymap = np.zeros(NX, np.int64)
        for y, x in enumerate(X):
            z = [0, 0, 0]
            for i in range(3):
                z[pi[i]] = x[i]
            ymap[y] = RIDX[tuple(z)]
        kmap = np.zeros(NCON, np.int64)
        for k, (S, d0, d1) in enumerate(DC.CONTRACTS):
            a, b = pi[S[0]], pi[S[1]]
            da, db = d0, d1
            if a > b:
                a, b = b, a; da, db = db, da
            kmap[k] = DC.CONTRACTS.index(((a, b), da, db))
        pidx = {p: j for j, p in enumerate(PROP)}
        pmap = np.array([pidx[(int(ymap[y]), int(kmap[k]))] for (y, k) in PROP], np.int64)
        out.append((pi, ymap, kmap, pmap))
    return out


PERMS = perms()


def canon(A):
    """canonical representative of the S3 orbit of a proposed-pair table A (tuple of 0/1)."""
    best = None
    for pi, ymap, kmap, pmap in PERMS:
        B = [0] * NP
        for j in range(NP):
            B[pmap[j]] = A[j]
        B = tuple(B)
        if best is None or B < best:
            best = B
    return best


# ====================================================================== values (float)
@njit(cache=True)
def gsolve(M, B):
    """Gaussian elimination with partial pivoting (no BLAS threads): solves M X = B for B of shape (n, m)."""
    n = M.shape[0]; m = B.shape[1]
    A = M.copy(); Xs = B.copy()
    for k in range(n):
        p = k; mx = abs(A[k, k])
        for i in range(k + 1, n):
            if abs(A[i, k]) > mx:
                mx = abs(A[i, k]); p = i
        if p != k:
            for j in range(n):
                t = A[k, j]; A[k, j] = A[p, j]; A[p, j] = t
            for j in range(m):
                t = Xs[k, j]; Xs[k, j] = Xs[p, j]; Xs[p, j] = t
        piv = A[k, k]
        for i in range(k + 1, n):
            f = A[i, k] / piv
            if f != 0.0:
                for j in range(k, n):
                    A[i, j] -= f * A[k, j]
                for j in range(m):
                    Xs[i, j] -= f * Xs[k, j]
    for k in range(n - 1, -1, -1):
        for j in range(m):
            v = Xs[k, j]
            for i in range(k + 1, n):
                v -= A[k, i] * Xs[i, j]
            Xs[k, j] = v / A[k, k]
    return Xs


@njit(cache=True)
def _cmat(acc, delta, PY, PXX, n):
    M = np.zeros((n, n))
    for y in range(n):
        M[y, y] = 1.0 - delta
    for j in range(acc.shape[0]):
        a = acc[j]
        if a != 0.0:
            M[PY[j], PY[j]] += delta * a / 27.0
            M[PY[j], PXX[j]] -= delta * a / 27.0
    return M


def chain_matrix(acc, delta):
    """M with M W = (1 - delta) U for an acceptance vector acc over PROP (floats in [0, 1])."""
    return _cmat(np.asarray(acc, np.float64), float(delta), PY, PXX, NX)


def values(acc, delta):
    return gsolve(chain_matrix(acc, delta), (1 - delta) * UPAY)


@njit(cache=True)
def nb_bounds(fixed, delta, PY, PXX, UPAY):
    """lo, hi (n x 3): min / max of W_i(y) over all completions of the free entries of `fixed` (-1 free), by policy
    iteration per player and sense (exact linear solves)."""
    n = UPAY.shape[0]; P = fixed.shape[0]
    lo = np.zeros((n, 3)); hi = np.zeros((n, 3))
    base = np.zeros(P)
    for j in range(P):
        if fixed[j] == 1:
            base[j] = 1.0
    rhs = np.zeros((n, 1))
    for i in range(3):
        for y in range(n):
            rhs[y, 0] = (1.0 - delta) * UPAY[y, i]
        for sense in (1.0, -1.0):
            pol = base.copy()
            W = np.zeros(n)
            for it in range(500):
                Wm = gsolve(_cmat(pol, delta, PY, PXX, n), rhs)
                for y in range(n):
                    W[y] = Wm[y, 0]
                changed = False
                for j in range(P):
                    if fixed[j] >= 0:
                        continue
                    gain = sense * (W[PXX[j]] - W[PY[j]])
                    if gain > 1e-13 and pol[j] == 0.0:
                        pol[j] = 1.0; changed = True
                    elif gain < -1e-13 and pol[j] == 1.0:
                        pol[j] = 0.0; changed = True
                if not changed:
                    break
            for y in range(n):
                if sense > 0:
                    hi[y, i] = W[y]
                else:
                    lo[y, i] = W[y]
    return lo, hi


def best_response(W, strict=True):
    d0 = W[PXX, PM0] - W[PY, PM0]
    d1 = W[PXX, PM1] - W[PY, PM1]
    if strict:
        return ((d0 > 0) & (d1 > 0)).astype(np.int8)
    return d0, d1


def margins(W):
    d0 = W[PXX, PM0] - W[PY, PM0]
    d1 = W[PXX, PM1] - W[PY, PM1]
    return np.minimum(np.abs(d0), np.abs(d1)), d0, d1


# ====================================================================== exact values
def dfrac(delta):
    return Fraction(str(delta)).limit_denominator(10 ** 6)


def int_system(acc, delta):
    """integer system [27(q-p) + p m(y)] W(y) - p sum_acc W(x) = 27 (q - p) u(y) for 0/1 acceptance; returns
    (diag list, off dict-of-lists (y -> [(x, mag)]), rhs (20 x 3))."""
    d = dfrac(delta); p, q = d.numerator, d.denominator
    m = [0] * NX
    off = [dict() for _ in range(NX)]
    for j in range(NP):
        if acc[j]:
            y, x = int(PY[j]), int(PXX[j])
            m[y] += 1
            off[y][x] = off[y].get(x, 0) + p
    diag = [27 * (q - p) + p * m[y] for y in range(NX)]
    rhs = [[27 * (q - p) * X[y][i] for i in range(3)] for y in range(NX)]
    return diag, off, rhs


def bareiss_solve(Mat, rhs):
    """fraction-free Gauss-Jordan (Bareiss) on an integer matrix (list of lists) with integer right-hand sides (list
    of lists): returns (det, numerators) with W = numerators / det exactly.  Every division is exact."""
    n = len(Mat)
    A = [list(Mat[i]) + list(rhs[i]) for i in range(n)]
    ncol = len(A[0])
    prev = 1
    for k in range(n):
        piv = A[k][k]
        assert piv != 0
        rk = A[k]
        for i in range(n):
            if i == k:
                continue
            row = A[i]; aik = row[k]
            for j in range(ncol):
                if j == k:
                    continue
                v = piv * row[j] - aik * rk[j]
                assert v % prev == 0
                row[j] = v // prev
            row[k] = 0
        prev = piv
    det = A[n - 1][n - 1]
    assert all(A[i][i] == det for i in range(n))
    return det, [[A[i][n + c] for c in range(len(rhs[0]))] for i in range(n)]


def int_matrix(acc, delta):
    diag, off, rhs = int_system(acc, delta)
    Mat = [[0] * NX for _ in range(NX)]
    for y in range(NX):
        Mat[y][y] = diag[y]
        for x, v in off[y].items():
            if x != y:
                Mat[y][x] -= v
    return Mat, rhs


def exact_values(acc, delta):
    """exact W (20 x 3) as Fractions for a 0/1 acceptance vector."""
    diag, off, rhs = int_system(acc, delta)
    Mat = [[0] * NX for _ in range(NX)]
    for y in range(NX):
        Mat[y][y] = diag[y]
        for x, v in off[y].items():
            if x == y:
                continue
            Mat[y][x] -= v
    # Fraction Gaussian elimination (independent of the Bareiss routine)
    n = NX
    A = [[Fraction(v) for v in Mat[i]] + [Fraction(v) for v in rhs[i]] for i in range(n)]
    for k in range(n):
        piv = A[k][k]
        for j in range(k, n + 3):
            A[k][j] /= piv
        for i in range(n):
            if i != k and A[i][k] != 0:
                f = A[i][k]
                for j in range(k, n + 3):
                    A[i][j] -= f * A[k][j]
    return [[A[i][n + c] for c in range(3)] for i in range(n)]


def exact_check(acc, delta):
    """'strict' if acc is a fixed point under the strict rule, 'weak' if only with ties, else None; plus the exact
    minimum margin (Fraction) and the number of exact ties."""
    W = exact_values(acc, delta)
    strict = True; weak = True; ties = 0; mmin = None
    for j in range(NP):
        y, x, a, b = int(PY[j]), int(PXX[j]), int(PM0[j]), int(PM1[j])
        d0 = W[x][a] - W[y][a]; d1 = W[x][b] - W[y][b]
        for d in (d0, d1):
            ad = abs(d)
            mmin = ad if mmin is None or ad < mmin else mmin
            if d == 0:
                ties += 1
        br = 1 if (d0 > 0 and d1 > 0) else 0
        if br != acc[j]:
            strict = False
        if acc[j] == 1 and not (d0 >= 0 and d1 >= 0):
            weak = False
        if acc[j] == 0 and not (d0 <= 0 or d1 <= 0):
            weak = False
    return ('strict' if strict else ('weak' if weak else None)), mmin, ties


# ====================================================================== branch and bound
CORE = [y for y in range(NX) if CAT[y] in ('fair', 'unequal') or (CAT[y] == 'wasteful' and sorted(X[y]) != [0, 2, 2])]
LEVEL2 = [y for y in range(NX) if y not in CORE and X[y] != (0, 0, 0)]       # (2,2)-type pairs and (2,2,2)
LEVEL3 = [RIDX[(0, 0, 0)]]
ACTIVE_CORE = np.array([PY[j] in CORE for j in range(NP)])


def exact_check_subset(acc, delta, mask):
    """exact_check restricted to the proposed pairs in mask (values of the states involved must not depend on entries
    outside the mask)."""
    W = exact_values(acc, delta)
    strict = True; weak = True; ties = 0; mmin = None
    for j in range(NP):
        if not mask[j]:
            continue
        y, x, a, b = int(PY[j]), int(PXX[j]), int(PM0[j]), int(PM1[j])
        d0 = W[x][a] - W[y][a]; d1 = W[x][b] - W[y][b]
        for d in (d0, d1):
            ad = abs(d)
            mmin = ad if mmin is None or ad < mmin else mmin
            if d == 0:
                ties += 1
        br = 1 if (d0 > 0 and d1 > 0) else 0
        if br != acc[j]:
            strict = False
        if acc[j] == 1 and not (d0 >= 0 and d1 >= 0):
            weak = False
        if acc[j] == 0 and not (d0 <= 0 or d1 <= 0):
            weak = False
    return ('strict' if strict else ('weak' if weak else None)), mmin, ties, W


class BnB:
    """branch and bound over the proposed pairs in `active` (others fixed at 0 and ignored: their states must not feed
    the active states' values, which holds for the core, notes §1.9)."""

    def __init__(self, delta, tau=1e-9, maxnodes=5_000_000, active=None):
        self.delta = delta; self.tau = tau; self.maxnodes = maxnodes
        self.active = np.ones(NP, bool) if active is None else np.asarray(active, bool)
        self.nodes = 0; self.leaves = 0; self.solutions = []; self.weak = []; self.rejected_leaves = 0
        self.solves = 0
        self.complete = True

    def bounds(self, fixed):
        self.solves += 1
        return nb_bounds(fixed.astype(np.int64), float(self.delta), PY, PXX, UPAY)

    def run(self):
        fixed = np.where(self.active, -1, 0).astype(np.int8)
        self._rec(fixed)
        return self

    def _rec(self, fixed):
        self.nodes += 1
        if self.nodes > self.maxnodes:
            self.complete = False
            return
        tau = self.tau; act = self.active
        while True:
            lo, hi = self.bounds(fixed)
            dmax0 = hi[PXX, PM0] - lo[PY, PM0]; dmin0 = lo[PXX, PM0] - hi[PY, PM0]
            dmax1 = hi[PXX, PM1] - lo[PY, PM1]; dmin1 = lo[PXX, PM1] - hi[PY, PM1]
            one = act & (fixed == 1); zero = act & (fixed == 0); free = fixed < 0
            if np.any(one & ((dmax0 < -tau) | (dmax1 < -tau))):
                return
            if np.any(zero & (dmin0 > tau) & (dmin1 > tau)):
                return
            f1 = free & (dmin0 > tau) & (dmin1 > tau)
            f0 = free & ((dmax0 < -tau) | (dmax1 < -tau))
            if not (f1.any() or f0.any()):
                break
            fixed = fixed.copy()
            fixed[f1] = 1; fixed[f0] = 0
        free = fixed < 0
        if not free.any():
            self.leaves += 1
            acc = tuple(int(v) for v in fixed)
            st, mmin, ties, W = exact_check_subset(acc, self.delta, act)
            if st == 'strict':
                self.solutions.append((acc, mmin, ties))
            elif st == 'weak':
                self.weak.append((acc, mmin, ties))
            else:
                self.rejected_leaves += 1
            return
        j = next(j for j in PRIO if fixed[j] < 0)
        for v in (1, 0):
            f2 = fixed.copy(); f2[j] = v
            self._rec(f2)


def _status(fixed, delta, act, tau=1e-9):
    lo, hi = nb_bounds(fixed.astype(np.int64), float(delta), PY, PXX, UPAY)
    dmax0 = hi[PXX, PM0] - lo[PY, PM0]; dmin0 = lo[PXX, PM0] - hi[PY, PM0]
    dmax1 = hi[PXX, PM1] - lo[PY, PM1]; dmin1 = lo[PXX, PM1] - hi[PY, PM1]
    one = act & (fixed == 1); zero = act & (fixed == 0); free = fixed < 0
    if np.any(one & ((dmax0 < -tau) | (dmax1 < -tau))):
        return None
    if np.any(zero & (dmin0 > tau) & (dmin1 > tau)):
        return None
    return free & (dmin0 > tau) & (dmin1 > tau), free & ((dmax0 < -tau) | (dmax1 < -tau))


def _propagate(fixed, delta, act):
    while True:
        r = _status(fixed, delta, act)
        if r is None:
            return None
        f1, f0 = r
        if not (f1.any() or f0.any()):
            return fixed
        fixed = fixed.copy(); fixed[f1] = 1; fixed[f0] = 0


class CoreSearch:
    """the certified search used for the core (notes §1.9): the BnB of §1.4 with failed-literal probing (a free entry
    whose 1-branch or 0-branch dies under propagation is forced to the other value) and fail-first branching (the
    free entry whose weaker branch fixes the most entries).  Pruning is conservative (tau), leaves are checked
    exactly, so the list is complete when the search terminates within its node cap."""

    def __init__(self, delta, active=None, maxnodes=2_000_000, log=None):
        self.delta = delta; self.act = ACTIVE_CORE if active is None else np.asarray(active, bool)
        self.maxnodes = maxnodes; self.nodes = 0; self.complete = True
        self.solutions = []; self.weak = []; self.rejected = 0; self.log = log

    def run(self, fixed=None):
        if fixed is None:
            fixed = np.where(self.act, -1, 0).astype(np.int8)
        self._rec(fixed)
        return self

    def _rec(self, fixed):
        self.nodes += 1
        if self.log and self.nodes % 5000 == 0:
            self.log('nodes %d free %d solutions %d' % (self.nodes, int((fixed < 0).sum()), len(self.solutions)))
        if self.nodes > self.maxnodes:
            self.complete = False
            return
        d = self.delta; act = self.act
        fixed = _propagate(fixed, d, act)
        if fixed is None:
            return
        while True:
            free = np.nonzero(fixed < 0)[0]
            if len(free) == 0:
                acc = tuple(int(v) for v in fixed)
                st, mmin, ties, W = exact_check_subset(acc, d, act)
                if st == 'strict':
                    self.solutions.append((acc, mmin, ties))
                elif st == 'weak':
                    self.weak.append((acc, mmin, ties))
                else:
                    self.rejected += 1
                return
            best = None; forced = False
            for j in free:
                r = {}
                for v in (1, 0):
                    f2 = fixed.copy(); f2[j] = v
                    r[v] = _propagate(f2, d, act)
                if r[1] is None and r[0] is None:
                    return
                if r[1] is None or r[0] is None:
                    fixed = r[0] if r[1] is None else r[1]
                    forced = True
                    break
                sc = min(int((r[1] >= 0).sum()), int((r[0] >= 0).sum()))
                if best is None or sc > best[0]:
                    best = (sc, j, r)
            if not forced:
                break
        sc, j, r = best
        for v in (1, 0):
            self._rec(r[v])


def subgroup_fixed_points(delta, group):
    """exhaustive enumeration of the core fixed points invariant under a subgroup of S3 (list of indices into PERMS):
    every invariant core table is evaluated (float screen with tolerance, exact check of the survivors)."""
    act = np.nonzero(ACTIVE_CORE)[0]
    orb = {}
    for j in act:
        key = min(int(PERMS[g][3][j]) for g in group)
        orb.setdefault(key, set()).update(int(PERMS[g][3][j]) for g in group)
    orbs = [sorted(v) for v in orb.values()]
    n = len(orbs)
    out = []; weak = []
    for m in range(2 ** n):
        A = np.zeros(NP, np.int8)
        for b in range(n):
            if (m >> b) & 1:
                A[orbs[b]] = 1
        W = values(A, delta)
        d0 = W[PXX, PM0] - W[PY, PM0]; d1 = W[PXX, PM1] - W[PY, PM1]
        acc_ok = (d0 > -1e-9) & (d1 > -1e-9); ref_ok = (d0 < 1e-9) | (d1 < 1e-9)
        ok = np.where(A[act] == 1, acc_ok[act], ref_ok[act]).all()
        if ok:
            acc = tuple(int(v) for v in A)
            st, mmin, ties, Wx = exact_check_subset(acc, delta, ACTIVE_CORE)
            if st == 'strict':
                out.append((acc, mmin, ties))
            elif st == 'weak':
                weak.append((acc, mmin, ties))
    return dict(n_orbits=n, solutions=out, weak=weak)


def local_solutions(y, Wex, delta, weak=False):
    """all subsets S of the proposed contracts at a state y that nothing else depends on, such that S is the set of
    contracts both members strictly prefer given W(y; S) (exact, Wex = exact values of the successor states)."""
    d = dfrac(delta)
    js = [j for j in range(NP) if PY[j] == y]
    n = len(js)
    # float filter over all subsets, then exact verification
    Wf = np.array([[float(v) for v in Wex[int(PXX[j])]] for j in js])          # (n, 3)
    df = float(d)
    bits = ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.float64)
    m = bits.sum(1)
    Wy = ((1 - df) * np.array(X[y], float)[None, :] + df / 27 * bits @ Wf) / ((1 - df) + df * m / 27)[:, None]
    ok = np.ones(2 ** n, bool)
    tau = 1e-9
    for a, j in enumerate(js):
        s0, s1 = int(PM0[j]), int(PM1[j])
        g0 = Wf[a, s0] - Wy[:, s0]; g1 = Wf[a, s1] - Wy[:, s1]
        inS = bits[:, a] > 0
        # possibly consistent (keeps exact ties for the exact check)
        ok &= np.where(inS, (g0 > -tau) & (g1 > -tau), (g0 < tau) | (g1 < tau))
    out = []
    for idx in np.nonzero(ok)[0]:
        S = [int(bits[idx, a]) for a in range(n)]
        mm = sum(S)
        Wy_ex = [((1 - d) * X[y][i] + d / 27 * sum(Wex[int(PXX[js[a]])][i] for a in range(n) if S[a]))
                 / ((1 - d) + d * mm / 27) for i in range(3)]
        strict = True; wk = True
        for a, j in enumerate(js):
            s0, s1 = int(PM0[j]), int(PM1[j])
            x = int(PXX[j])
            e0 = Wex[x][s0] - Wy_ex[s0]; e1 = Wex[x][s1] - Wy_ex[s1]
            br = 1 if (e0 > 0 and e1 > 0) else 0
            if br != S[a]: strict = False
            if S[a] == 1 and not (e0 >= 0 and e1 >= 0): wk = False
            if S[a] == 0 and not (e0 <= 0 or e1 <= 0): wk = False
        if strict:
            out.append((js, S, 'strict', Wy_ex))
        elif wk and weak:
            out.append((js, S, 'weak', Wy_ex))
    return out


def enumerate_fixed_points(delta, maxnodes=2_000_000, weak=True, log=None):
    """all pure KR fixed points (strict rule), plus weak ones (ties), by the decomposition core -> level 2 -> (0,0,0):
    nothing enters (0,0,0) or (2,2,2), (2,2)-type pairs are entered only from (0,0,0), so the core's values do not
    depend on the other states' decisions.  Every returned table is verified exactly on all 90 pairs."""
    b = CoreSearch(delta, maxnodes=maxnodes, log=log).run()
    strict_out = []; weak_out = []
    cores = [(acc, 'strict') for acc, _, _ in b.solutions] + ([(acc, 'weak') for acc, _, _ in b.weak] if weak else [])
    for acc, kind in cores:
        Wc = exact_values(acc, delta)
        # level 2: each state independently, given the core
        l2 = []
        for y in LEVEL2:
            l2.append(local_solutions(y, Wc, delta, weak=weak))
        for combo in itertools.product(*l2):
            A = list(acc)
            W2 = [list(r) for r in Wc]
            for (js, S, k2, Wy) in combo:
                for a, j in enumerate(js):
                    A[j] = S[a]
                W2[int(PY[js[0]])] = Wy
            for (js, S, k3, Wy) in local_solutions(LEVEL3[0], W2, delta, weak=weak):
                A3 = list(A)
                for a, j in enumerate(js):
                    A3[j] = S[a]
                A3 = tuple(A3)
                st, mmin, ties = exact_check(A3, delta)
                if st == 'strict':
                    strict_out.append((A3, mmin, ties))
                elif st == 'weak':
                    weak_out.append((A3, mmin, ties))
    return dict(solutions=strict_out, weak=weak_out, core_nodes=b.nodes,
                core_solutions=len(b.solutions), core_weak=len(b.weak), complete=b.complete,
                core_rejected=b.rejected)


# ====================================================================== default selection (frozen rule, notes §1.4)
def default_policy(delta, maxit=10000):
    myopic = np.ones(NP, np.int8)
    A = myopic.copy(); seen = {A.tobytes(): 0}
    path = [A.copy()]
    for t in range(1, maxit + 1):
        B = best_response(values(A, delta))
        if np.array_equal(B, A):
            return dict(A=A, rule='simultaneous', iterations=t - 1, path_len=len(path))
        A = B
        key = A.tobytes()
        if key in seen:
            break
        seen[key] = t; path.append(A.copy())
    cyc = dict(cycle_at=t)
    A = myopic.copy(); flips = 0
    while flips < maxit:
        B = best_response(values(A, delta))
        diff = np.nonzero(B != A)[0]
        if len(diff) == 0:
            return dict(A=A, rule='asynchronous', flips=flips, simultaneous=cyc)
        A = A.copy(); A[diff[0]] = B[diff[0]]; flips += 1
    return dict(A=None, rule='hamming', simultaneous=cyc, flips=flips)


# ====================================================================== analysis of a fixed point
def event_chain(acc):
    Q = np.zeros((NX, NX))
    for j in range(NP):
        if acc[j]:
            Q[PY[j], PXX[j]] += 1.0 / NCON
    Q[np.arange(NX), np.arange(NX)] += 1.0 - Q.sum(1)
    return Q


def recurrent_classes(Q):
    R = (Q > 0).astype(int)
    reach = R.copy() | np.eye(NX, dtype=int)
    for k in range(NX):
        reach = reach | (reach[:, [k]] & reach[[k], :])
    classes = []
    seen = set()
    for y in range(NX):
        if y in seen:
            continue
        cl = [z for z in range(NX) if reach[y, z] and reach[z, y]]
        closed = all(reach[y, z] == 0 or reach[z, y] for z in range(NX))
        if closed:
            classes.append(sorted(cl))
        seen.update(cl)
    return classes


def stationary_in(Q, cl):
    if len(cl) == 1:
        return np.array([1.0])
    P = Q[np.ix_(cl, cl)]
    w, v = np.linalg.eig(P.T)
    k = int(np.argmin(np.abs(w - 1)))
    p = np.real(v[:, k]); return p / p.sum()


def absorption(Q, classes):
    rec = sorted(z for c in classes for z in c)
    T = [z for z in range(NX) if z not in rec]
    out = np.zeros((NX, len(classes)))
    for ci, c in enumerate(classes):
        for z in c:
            out[z, ci] = 1.0
    if T:
        A = np.eye(len(T)) - Q[np.ix_(T, T)]
        B = np.zeros((len(T), len(classes)))
        for ci, c in enumerate(classes):
            B[:, ci] = Q[np.ix_(T, c)].sum(1)
        H = np.linalg.solve(A, B)
        for a, z in enumerate(T):
            out[z] = H[a]
    return out


def hitting(Q, target, tmax=20000):
    """survival curves P(T > t) of the hitting time (events) of `target` from every outcome; mean, median, q90."""
    T = [z for z in range(NX) if z not in target]
    res = {}
    if not T:
        return {LAB[z]: dict(mean=0.0, median=0, q90=0) for z in range(NX)}
    QT = Q[np.ix_(T, T)]
    A = np.eye(len(T)) - QT
    try:
        mean = np.linalg.solve(A, np.ones(len(T)))
    except np.linalg.LinAlgError:
        mean = np.full(len(T), np.inf)
    s = np.ones(len(T)); med = [None] * len(T); q90 = [None] * len(T)
    for t in range(1, tmax + 1):
        s = QT @ s
        for a in range(len(T)):
            if med[a] is None and s[a] <= 0.5: med[a] = t
            if q90[a] is None and s[a] <= 0.1: q90[a] = t
        if all(m is not None for m in q90):
            break
    for a, z in enumerate(T):
        res[LAB[z]] = dict(mean=float(mean[a]) if np.isfinite(mean[a]) and 0 <= mean[a] < 1e9 else None,
                           median=med[a], q90=q90[a])
    for z in target:
        res[LAB[z]] = dict(mean=0.0, median=0, q90=0)
    return res


def seeded_distribution():
    """outcome distribution of the baseline L, mN = 0 islands at closure (stored stable-sets runs, horizon 2,000,
    classified islands only)."""
    import json
    d = json.load(open(os.path.join(ROOT, 'runs', 'stable_sets', 'L0.json')))
    cnt = np.zeros(NX)
    lab2 = {l: k for k, l in enumerate(LAB)}
    for r in d['runs']:
        for l, v in r['horizons']['2000']['labels'].items():
            if l in lab2:
                cnt[lab2[l]] += v
    return cnt / cnt.sum()


def describe(acc, delta, seeded):
    acc = np.asarray(acc, np.int8)
    Q = event_chain(acc)
    classes = recurrent_classes(Q)
    ab = absorption(Q, classes)
    absorbing = sorted(z for c in classes for z in c)
    stat_V = 0.0
    from_seed = seeded @ ab
    cls_info = []
    for ci, c in enumerate(classes):
        st = stationary_in(Q, c)
        vm = float(sum(st[a] for a, z in enumerate(c) if z in V))
        stat_V += from_seed[ci] * vm
        cls_info.append(dict(outcomes=[LAB[z] for z in c], cats=sorted({CAT[z] for z in c}), V_mass=vm,
                             p_from_seed=float(from_seed[ci])))
    W = values(acc, delta)
    mg, d0, d1 = margins(W)
    hitA = hitting(Q, absorbing)
    hitV = hitting(Q, V) if all(z in absorbing or True for z in V) else None
    # can V be hit from everywhere?
    abV = absorption(Q, classes)
    accepted_member_exits = int(sum(acc[j] for j in range(NP) if PY[j] in V and PXX[j] not in V))
    return dict(absorbing=[LAB[z] for z in absorbing], absorbing_is_V=(absorbing == V), classes=cls_info,
                n_accept=int(acc.sum()), accepted_member_exits=accepted_member_exits,
                absorb_from={LAB[y]: [round(float(v), 6) for v in ab[y]] for y in range(NX)},
                stationary_V_from_seed=float(stat_V),
                min_margin=float(mg.min()),
                W={LAB[y]: [round(float(v), 6) for v in W[y]] for y in range(NX)},
                hit_absorbing=hitA, hit_V=hitV if set(V) <= set(absorbing) else hitting(Q, V))


# ====================================================================== guard tables
def table_g0():
    return np.ones((NX, NCON, 2), np.bool_)


def table_gV():
    T = np.ones((NX, NCON, 2), np.bool_)
    for y in range(NX):
        for k in range(NCON):
            if y in V and not (CD_[k, 0] == 3 and CD_[k, 1] == 3):
                T[y, k, :] = False
    return T


def exposed(x, i):
    """some feasible contract on the pair not containing i is proposed (dominates) at outcome x."""
    for k in range(NCON):
        S = DC.CONTRACTS[k][0]
        if i in S or not FEAS[k]:
            continue
        if DC.proposed(k, x):
            return True
    return False


def table_g1(variant='y'):
    T = np.ones((NX, NCON, 2), np.bool_)
    for y in range(NX):
        for k in range(NCON):
            x = DC.contract_x(k)
            for z in range(2):
                i = int(CS_[k, z])
                ex = exposed(x, i)
                if variant == 'y':
                    T[y, k, z] = not (ex and 0 < X[y][i])
                else:
                    T[y, k, z] = not (ex and 0 < x[i])
    return T


def table_from_W(W):
    """member-level consent table a_i(y, kappa) = [W_i(x) > W_i(y)] for every y, kappa, member position."""
    T = np.zeros((NX, NCON, 2), np.bool_)
    for y in range(NX):
        for k in range(NCON):
            x = CX[k]
            for z in range(2):
                i = int(CS_[k, z])
                T[y, k, z] = W[x, i] > W[y, i]
    return T


def freezing_set(T):
    """outcomes at which every proposed contract is refused (by some member) under the table T."""
    out = []
    for y in range(NX):
        ks = [k for k in range(NCON) if PROPM[y, k]]
        if all(not (T[y, k, 0] and T[y, k, 1]) for k in ks):
            out.append(LAB[y])
    return out


# ====================================================================== the kernel
@njit(cache=True)
def _ftypeid(s, k, o, g, NG, Kmax, TK, TO, TG, TPC, TMAP, ntypes):
    key = (k * 10 + (o + 1)) * NG + g
    t = TMAP[s, key]
    if t >= 0:
        return t
    t = ntypes[s]
    if t >= TK.shape[1]:
        return -1
    TMAP[s, key] = t
    TK[s, t] = k; TO[s, t] = o; TG[s, t] = g
    TPC[s, t] = k if o < 0 else Kmax + o
    ntypes[s] = t + 1
    return t


@njit(cache=True)
def _gcounts(tcount, tpres, tnpres, TG, i, NG, out):
    for s in range(3):
        for g in range(NG):
            out[s, g] = 0
        for t in range(tnpres[i, s]):
            tt = tpres[i, s, t]
            out[s, TG[s, tt]] += tcount[i, s, tt]


@njit(cache=True)
def reader_values(gc, N, GKIND, GTAB, KRTAB, PROPM, CS, CX, UPAY, delta, player):
    """W_player (20) of the contract process whose consent probabilities are the slot compositions gc (3 x NG): readers
    and gKR copies consent by KRTAB, static guards by their own table."""
    NXl = UPAY.shape[0]; NCl = CS.shape[0]; NG = gc.shape[1]
    M = np.zeros((NXl, NXl))
    for y in range(NXl):
        M[y, y] = 1.0 - delta
    for y in range(NXl):
        for k in range(NCl):
            if not PROPM[y, k]:
                continue
            a = 1.0
            for z in range(2):
                s = CS[k, z]
                p = 0.0
                for g in range(NG):
                    if gc[s, g] == 0:
                        continue
                    if GKIND[g] == 0:
                        c = GTAB[g, y, k, z]
                    else:
                        c = KRTAB[y, k, z]
                    if c:
                        p += gc[s, g]
                a *= p / N
            if a > 0.0:
                x = CX[k]
                M[y, y] += delta * a / NCl
                M[y, x] -= delta * a / NCl
    rhs = np.zeros((NXl, 1))
    for y in range(NXl):
        rhs[y, 0] = (1.0 - delta) * UPAY[y, player]
    return gsolve(M, rhs)[:, 0]


@njit(cache=True)
def _consent(g, y, k, z, GKIND, GTAB, rdec):
    if GKIND[g] == 0:
        return GTAB[g, y, k, z]
    return rdec[z]


@njit(cache=True)
def fkern(J, PAY, VEC, ISMEM, TOT, tcount0, TK, TO, TG, TPC, TMAP, ntypes, Kmax, NG, N, w, m, seed, H,
          close_every, hrec, nu, CS, CD, CACT, CX, GKIND, GTAB, KRTAB, PROPM, UPAY, rdelta, stop_closed, rec_every,
          evcap, cevcap):
    """eps = 0 island lottery with genotypes (k, o, g) and contract events (menu F, beta = 1, public consent by guard).
    Births, migration, classification and closure exactly as dominance_contracts.dkern."""
    np.random.seed(seed)
    I = tcount0.shape[0]; Tcap = tcount0.shape[2]; PCn = J.shape[0]
    nout = ISMEM.shape[0]
    tcount = tcount0.copy()
    tpres = np.zeros((I, 3, Tcap), np.int64); tnpres = np.zeros((I, 3), np.int64); tpos = -np.ones((I, 3, Tcap), np.int64)
    pcount = np.zeros((I, 3, PCn), np.int64); ppres = np.zeros((I, 3, PCn), np.int64)
    pnpres = np.zeros((I, 3), np.int64); ppos = -np.ones((I, 3, PCn), np.int64)
    glob = np.zeros((3, PCn), np.int64)
    Fp = np.zeros((I, 3, PCn))
    introg = np.full((I, 3, PCn), -2, np.int64); introc = np.zeros((I, 3, PCn), np.int64)
    for i in range(I):
        for s in range(3):
            for t in range(Tcap):
                if tcount[i, s, t] > 0:
                    tpres[i, s, tnpres[i, s]] = t; tpos[i, s, t] = tnpres[i, s]; tnpres[i, s] += 1
                    pcount[i, s, TPC[s, t]] += tcount[i, s, t]
            for pc in range(PCn):
                if pcount[i, s, pc] > 0:
                    ppres[i, s, pnpres[i, s]] = pc; ppos[i, s, pc] = pnpres[i, s]; pnpres[i, s] += 1
                    glob[s, pc] += pcount[i, s, pc]
                    introg[i, s, pc] = -1; introc[i, s, pc] = 0
    for i in range(I):
        for s in range(3):
            for t in range(pnpres[i, s]):
                pc = ppres[i, s, t]
                Fp[i, s, pc] = SS._fit_full(J, PAY, pcount, ppres, pnpres, i, s, pc)
    NU = 3 * I
    act = np.arange(NU); apos = np.arange(NU); nact = 0
    for u in range(NU):
        if tnpres[u // 3, u % 3] > 1:
            nact = SS._setact(u, True, act, apos, nact)
    cls = np.zeros((H + 1, I), np.int16)
    nh = hrec.shape[0]
    effrec = np.zeros((nh, I)); distrec = np.zeros((nh, I, nout))
    dist = np.zeros(nout)
    dom = -np.ones((I, 3), np.int64)
    ev = np.zeros((evcap, 8)); nev = 0
    cev = np.zeros((cevcap, 16)); ncev = 0
    cnt = np.zeros((I, 8), np.int64)      # draws, null, -, consulted, refused, installed, infeasible, overflow
    refby = np.zeros((I, NG), np.int64)   # refusals by the drawn individual's guard
    nrec = H // rec_every + 1
    gfreq = np.zeros((nrec, I, 3, NG), np.float32)
    gc = np.zeros((3, NG), np.int64)
    rdec = np.zeros(2, np.bool_)
    nsolve = 0
    N2 = float(N) * N
    UN = NU * N
    mm = m if I > 1 else 0.0
    overflow = False
    hasreader = False
    for g_ in range(NG):
        if GKIND[g_] == 1:
            hasreader = True
    for i in range(I):
        c, e = SS._classify(J, VEC, ISMEM, TOT, pcount, ppres, pnpres, i, N, dist, nout)
        cls[0, i] = c
        for s in range(3):
            for t in range(pnpres[i, s]):
                pc = ppres[i, s, t]
                if 2 * pcount[i, s, pc] > N:
                    dom[i, s] = pc
            if dom[i, s] >= 0 and nev < evcap:
                ev[nev, 0] = 0; ev[nev, 1] = i; ev[nev, 2] = s; ev[nev, 3] = -1; ev[nev, 4] = dom[i, s]
                ev[nev, 5] = -1; ev[nev, 6] = 0; ev[nev, 7] = np.nan
                nev += 1
    for i in range(I):
        _gcounts(tcount, tpres, tnpres, TG, i, NG, gc)
        for s in range(3):
            for g_ in range(NG):
                gfreq[0, i, s, g_] = gc[s, g_] / N
    b = 0
    g = 0
    hi = 0
    nextchk = UN
    status = 4; stop_gen = H
    nmig = 0
    total = H * UN
    cls0 = np.zeros(PCn, np.int64); cls1 = np.zeros(PCn, np.int64); cls2 = np.zeros(PCn, np.int64)
    mvt = np.zeros(Tcap, np.int64); mvn = np.zeros(Tcap, np.int64); tmpc = np.zeros(Tcap, np.int64)
    while True:
        pa = (nact + (NU - nact) * mm) / NU
        if pa <= 0.0:
            G = total + 1
        elif pa >= 1.0:
            G = 0
        else:
            uu = np.random.random()
            G = int(np.log(1.0 - uu) / np.log(1.0 - pa))
        if b + G >= nextchk:
            b = nextchk
            g += 1
            for i in range(I):
                c, e = SS._classify(J, VEC, ISMEM, TOT, pcount, ppres, pnpres, i, N, dist, nout)
                cls[g, i] = c
                if hi < nh and hrec[hi] == g:
                    effrec[hi, i] = e
                    for z in range(nout):
                        distrec[hi, i, z] = dist[z]
                for s in range(3):
                    nd = -1
                    for t in range(pnpres[i, s]):
                        pc = ppres[i, s, t]
                        if 2 * pcount[i, s, pc] > N:
                            nd = pc
                    if nd >= 0 and nd != dom[i, s]:
                        if nev < evcap:
                            ev[nev, 0] = g; ev[nev, 1] = i; ev[nev, 2] = s; ev[nev, 3] = dom[i, s]; ev[nev, 4] = nd
                            ev[nev, 5] = introg[i, s, nd]; ev[nev, 6] = introc[i, s, nd]
                            if dom[i, s] >= 0:
                                ev[nev, 7] = (SS._fit_full(J, PAY, pcount, ppres, pnpres, i, s, nd)
                                              - SS._fit_full(J, PAY, pcount, ppres, pnpres, i, s, dom[i, s])) / N2
                            else:
                                ev[nev, 7] = np.nan
                        nev += 1
                        dom[i, s] = nd
            if hi < nh and hrec[hi] == g:
                hi += 1
            if g % rec_every == 0:
                rr_ = g // rec_every
                for i in range(I):
                    _gcounts(tcount, tpres, tnpres, TG, i, NG, gc)
                    for s in range(3):
                        for g_ in range(NG):
                            gfreq[rr_, i, s, g_] = gc[s, g_] / N
            # contract events
            if nu > 0.0 and g < H:
                for i in range(I):
                    if np.random.random() >= nu:
                        continue
                    cnt[i, 0] += 1
                    kap = np.random.randint(CS.shape[0])
                    s0 = CS[kap, 0]; s1 = CS[kap, 1]; d0 = CD[kap, 0]; d1 = CD[kap, 1]
                    if d0 + d1 > 6:
                        cnt[i, 6] += 1; cnt[i, 1] += 1
                        continue
                    y0 = DC._slot_mean(Fp, pcount, ppres, pnpres, i, s0, N, N2)
                    y1 = DC._slot_mean(Fp, pcount, ppres, pnpres, i, s1, N, N2)
                    if not (d0 / 6.0 > y0 + 1e-9 and d1 / 6.0 > y1 + 1e-9):
                        cnt[i, 1] += 1
                        continue
                    cc_, e_ = SS._classify(J, VEC, ISMEM, TOT, pcount, ppres, pnpres, i, N, dist, nout)
                    modal = 0; mx = -1.0
                    for z in range(nout):
                        if dist[z] > mx:
                            mx = dist[z]; modal = z
                    _gcounts(tcount, tpres, tnpres, TG, i, NG, gc)
                    # reader decisions for the two member slots (if a reader is present in that slot)
                    rdec[0] = False; rdec[1] = False
                    if hasreader:
                        for z in range(2):
                            sz = s0 if z == 0 else s1
                            pres = False
                            for g_ in range(NG):
                                if GKIND[g_] == 1 and gc[sz, g_] > 0:
                                    pres = True
                            if pres:
                                Wr = reader_values(gc, N, GKIND, GTAB, KRTAB, PROPM, CS, CX, UPAY, rdelta, sz)
                                nsolve += 1
                                rdec[z] = Wr[CX[kap]] > Wr[modal]
                    need = False
                    for z in range(2):
                        sz = s0 if z == 0 else s1
                        for g_ in range(NG):
                            if gc[sz, g_] > 0 and not _consent(g_, modal, kap, z, GKIND, GTAB, rdec):
                                need = True
                    refused = False
                    gd0 = -1; gd1 = -1; c0 = 1; c1 = 1
                    if need:
                        cnt[i, 3] += 1
                        for z in range(2):
                            sz = s0 if z == 0 else s1
                            r_ = np.random.randint(N); acc = 0; tv = tpres[i, sz, 0]
                            for t in range(tnpres[i, sz]):
                                tt = tpres[i, sz, t]; acc += tcount[i, sz, tt]
                                if r_ < acc:
                                    tv = tt; break
                            gz = TG[sz, tv]
                            cz = _consent(gz, modal, kap, z, GKIND, GTAB, rdec)
                            if z == 0:
                                gd0 = gz; c0 = 1 if cz else 0
                            else:
                                gd1 = gz; c1 = 1 if cz else 0
                            if not cz:
                                refused = True
                                refby[i, gz] += 1
                    row = ncev
                    if ncev < cevcap:
                        cev[row, 0] = g; cev[row, 1] = i; cev[row, 2] = kap; cev[row, 4] = cc_; cev[row, 5] = modal
                        cev[row, 6] = y0; cev[row, 7] = y1; cev[row, 8] = gd0; cev[row, 9] = gd1
                        cev[row, 10] = 1.0 if need else 0.0; cev[row, 11] = c0; cev[row, 12] = c1
                    ncev += 1
                    if refused:
                        cnt[i, 4] += 1
                        if row < cevcap:
                            cev[row, 3] = 1
                        continue
                    for z in range(2):
                        sz = s0 if z == 0 else s1
                        az = CACT[kap, z]
                        nm = 0
                        for t in range(tnpres[i, sz]):
                            tt = tpres[i, sz, t]
                            mvt[nm] = tt; mvn[nm] = tcount[i, sz, tt]; nm += 1
                        for q in range(nm):
                            if mvn[q] == 0:
                                continue
                            tt = mvt[q]
                            nt = _ftypeid(sz, TK[sz, tt], az, TG[sz, tt], NG, Kmax, TK, TO, TG, TPC, TMAP, ntypes)
                            if nt < 0:
                                overflow = True
                                break
                            if nt == tt:
                                continue
                            DC._tsub(i, sz, tt, mvn[q], tcount, tpres, tnpres, tpos)
                            DC._tadd(i, sz, nt, mvn[q], tcount, tpres, tnpres, tpos)
                            pco = TPC[sz, tt]; pcn = TPC[sz, nt]
                            if pco != pcn:
                                DC._psub(i, sz, pco, mvn[q], pcount, ppres, pnpres, ppos, glob, introg)
                                DC._padd(i, sz, pcn, mvn[q], pcount, ppres, pnpres, ppos, glob, introg, introc, g, 2)
                        nact = SS._setact(3 * i + sz, tnpres[i, sz] > 1, act, apos, nact)
                    if overflow:
                        cnt[i, 7] += 1
                        break
                    for s in range(3):
                        for t in range(pnpres[i, s]):
                            pc = ppres[i, s, t]
                            Fp[i, s, pc] = SS._fit_full(J, PAY, pcount, ppres, pnpres, i, s, pc)
                    cnt[i, 5] += 1
                    if row < cevcap:
                        cev[row, 3] = 2
                if overflow:
                    status = 9; stop_gen = g
                    break
            done = False
            if stop_closed and (g % close_every == 0 or g == H):
                if mm > 0.0:
                    n0 = 0; n1 = 0; n2 = 0
                    for k in range(PCn):
                        if glob[0, k] > 0:
                            cls0[n0] = k; n0 += 1
                        if glob[1, k] > 0:
                            cls1[n1] = k; n1 += 1
                        if glob[2, k] > 0:
                            cls2[n2] = k; n2 += 1
                    if SS._closed(J, cls0, n0, cls1, n1, cls2, n2):
                        status = 1; stop_gen = g; done = True
                else:
                    allc = True
                    for i in range(I):
                        if not SS._closed(J, ppres[i, 0], pnpres[i, 0], ppres[i, 1], pnpres[i, 1], ppres[i, 2], pnpres[i, 2]):
                            allc = False; break
                    if allc:
                        status = 5; stop_gen = g; done = True
            if done or g >= H:
                break
            nextchk = (g + 1) * UN
            continue
        b = b + G + 1
        if np.random.random() * pa * NU < nact:
            u = act[np.random.randint(nact)]
            mig = mm > 0.0 and np.random.random() < mm
        else:
            u = act[nact + np.random.randint(NU - nact)]
            mig = True
        i = u // 3; s = u % 3
        src = i
        if mig:
            src = np.random.randint(I - 1)
            if src >= i: src += 1
            nmig += 1
        mx = -1e300
        for t in range(tnpres[src, s]):
            tt = tpres[src, s, t]
            f = Fp[src, s, TPC[s, tt]] / N2
            if f > mx: mx = f
        tot = 0.0
        for t in range(tnpres[src, s]):
            tt = tpres[src, s, t]
            tot += tcount[src, s, tt] * np.exp(w * (Fp[src, s, TPC[s, tt]] / N2 - mx))
        uu = np.random.random() * tot; acc2 = 0.0
        child = tpres[src, s, tnpres[src, s] - 1]
        for t in range(tnpres[src, s]):
            tt = tpres[src, s, t]
            acc2 += tcount[src, s, tt] * np.exp(w * (Fp[src, s, TPC[s, tt]] / N2 - mx))
            if uu <= acc2:
                child = tt; break
        r = np.random.randint(N); acc = 0; victim = tpres[i, s, 0]
        for t in range(tnpres[i, s]):
            tt = tpres[i, s, t]; acc += tcount[i, s, tt]
            if r < acc:
                victim = tt; break
        if victim == child:
            continue
        DC._tsub(i, s, victim, 1, tcount, tpres, tnpres, tpos)
        DC._tadd(i, s, child, 1, tcount, tpres, tnpres, tpos)
        pv = TPC[s, victim]; pcc = TPC[s, child]
        if pv != pcc:
            DC._psub(i, s, pv, 1, pcount, ppres, pnpres, ppos, glob, introg)
            new = pcount[i, s, pcc] == 0
            DC._padd(i, s, pcc, 1, pcount, ppres, pnpres, ppos, glob, introg, introc, g + 1, 1 if mig else 0)
            o1, o2 = SS._others(s)
            for sa in (o1, o2):
                sb = o1 + o2 - sa
                for ta in range(pnpres[i, sa]):
                    k = ppres[i, sa, ta]
                    v = 0.0
                    for tb in range(pnpres[i, sb]):
                        q = ppres[i, sb, tb]
                        if s < sb:
                            v += pcount[i, sb, q] * (PAY[SS._code(J, sa, k, pcc, q), sa] - PAY[SS._code(J, sa, k, pv, q), sa])
                        else:
                            v += pcount[i, sb, q] * (PAY[SS._code(J, sa, k, q, pcc), sa] - PAY[SS._code(J, sa, k, q, pv), sa])
                    Fp[i, sa, k] += v
            if new:
                Fp[i, s, pcc] = SS._fit_full(J, PAY, pcount, ppres, pnpres, i, s, pcc)
        nact = SS._setact(u, tnpres[i, s] > 1, act, apos, nact)
    for gg in range(stop_gen + 1, H + 1):
        for i in range(I):
            cls[gg, i] = cls[stop_gen, i]
    for z in range(hi, nh):
        if hrec[z] > stop_gen:
            for i in range(I):
                c, e = SS._classify(J, VEC, ISMEM, TOT, pcount, ppres, pnpres, i, N, dist, nout)
                effrec[z, i] = e
                for zz in range(nout):
                    distrec[z, i, zz] = dist[zz]
    return (status, stop_gen, tcount, cls, effrec, distrec, ev[:min(nev, evcap)], nev, nmig, cev[:min(ncev, cevcap)],
            ncev, cnt, gfreq, refby, nsolve, pcount)


# ====================================================================== run setup
class Setup:
    """per-run tables for fkern: the extended play-class universe of dominance_contracts.Setup, the genotype tables
    (k, o, g) and the initial counts.  Guard assignment mimics dominance_contracts.Setup's bit draws: guard index 0 is
    the base; `assign` is None (everyone guard 0), ('bit', f, g1) (each founder individual carries guard g1 with
    probability f, else 0; for f = 1 no number is drawn, as DC.Setup), or ('mix', [g...], [p...]) (one uniform number
    per individual)."""

    def __init__(self, init, U, NG, assign=None, rng=None, arm='weak'):
        S, mu = SS.arm_data(arm)
        I = init.shape[0]
        self.U = U; self.NG = NG
        Kmax = max(len(u) for u in U)
        self.Kmax = Kmax
        ci = SS.const_index(S.fs)
        Up = []
        for s in range(3):
            u = np.concatenate([U[s], np.full(Kmax - len(U[s]), U[s][0])]).astype(np.int64)
            Up.append(np.concatenate([u, np.array([ci[l] for l in range(9)], np.int64)]))
        self.Uext = Up
        self.J = SS.joint_for(arm, Up)
        Tcap = Kmax * 10 * NG
        self.TK = np.zeros((3, Tcap), np.int64); self.TO = -np.ones((3, Tcap), np.int64)
        self.TG = np.zeros((3, Tcap), np.int64)
        self.TPC = np.zeros((3, Tcap), np.int64)
        self.TMAP = -np.ones((3, Kmax * 10 * NG), np.int64)
        self.ntypes = np.zeros(3, np.int64)
        for s in range(3):
            for k in range(Kmax):
                t = self.tid(s, k, -1, 0)
                assert t == k
        tc = np.zeros((I, 3, Tcap), np.int64)
        tc[:, :, :init.shape[2]] = init[:, :, :Kmax]
        if assign is not None:
            new = np.zeros_like(tc)
            for i in range(I):
                for s in range(3):
                    for k in np.nonzero(tc[i, s, :Kmax])[0]:
                        n = int(tc[i, s, k])
                        if assign[0] == 'bit':
                            f, g1 = assign[1], assign[2]
                            gs = np.where(rng.random(n) < f, g1, 0) if f < 1.0 else np.full(n, g1)
                        else:
                            gl, ps = assign[1], np.cumsum(assign[2])
                            u_ = rng.random(n)
                            gs = np.array([gl[int(np.searchsorted(ps, v, side='right'))] for v in u_])
                        for g_ in gs:
                            t = self.tid(s, k, -1, int(g_))
                            new[i, s, t] += 1
            tc = new
        self.tc0 = tc
        self.Tcap = Tcap

    def tid(self, s, k, o, g):
        key = (k * 10 + (o + 1)) * self.NG + g
        t = self.TMAP[s, key]
        if t >= 0:
            return int(t)
        t = int(self.ntypes[s])
        self.TMAP[s, key] = t
        self.TK[s, t] = k; self.TO[s, t] = o; self.TG[s, t] = g
        self.TPC[s, t] = k if o < 0 else self.Kmax + o
        self.ntypes[s] = t + 1
        return t


def run_fkern(setup, T, N, mN, seed, H, hrec, guards, nu=0.1, stop_closed=None, close_every=10, rec_every=10,
              evcap=2000000, cevcap=600000):
    """guards: dict with GKIND (NG,), GTAB (NG, 20, 27, 2), KRTAB (20, 27, 2), rdelta."""
    if stop_closed is None:
        stop_closed = (nu == 0.0)
    return fkern(setup.J, T.PAY, T.VEC, T.ISMEM, T.TOT, setup.tc0, setup.TK, setup.TO, setup.TG, setup.TPC,
                 setup.TMAP, setup.ntypes, setup.Kmax, setup.NG, N, SS.W, mN / N, seed, H, close_every,
                 np.asarray(hrec, np.int64), float(nu), CS_, CD_, CACT_, CX, guards['GKIND'], guards['GTAB'],
                 guards['KRTAB'], PROPM, UPAY, float(guards['rdelta']), bool(stop_closed), rec_every, evcap, cevcap)
