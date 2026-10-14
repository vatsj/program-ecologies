"""Stable sets on islands (spec specs/2026-10-13-stable-sets-on-islands.md, reviewed by gpt-6.1-sol and
gemini-4-argon; notes notes/stable-sets-on-islands.md; predictions predictions/2026-10-13-stable-sets-on-islands.md).

Static part: outcome sets (the dollar3 game's realizable vectors R, the classical grids G6/G8, the extended
constants games' realizable sets), the dominance relations M (strict majority) and C (commitment with credible
best-reply response, "every best reply"), indirect dominance (Harsanyi/Chwe) and Chwe's largest consistent set, and
an exhaustive kernel (stable set) enumerator.

Dynamic part: the eps = 0 island lottery with three slot populations per island (the birth-death process of
src/sog_lottery.py, mirrored draw for draw so that it can be checked against sog_lottery.kern), with per-generation
island classification by play and a dominance-change log for flip triggers; seed laws; the per-run analysis.
"""
import itertools, math, os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numba import njit
import dollar3 as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'stable_sets')
W = 0.3
PAIRS = ((0, 1), (0, 2), (1, 2))


# ====================================================================== games (action level)
class Game:
    """A three-player normal form with finite action sets.  pay[a0, a1, a2] = payoff vector in grid units (ints);
    g = the grid (6 or 8); names = action names per slot."""

    def __init__(self, nact, pay, g, names=None):
        self.nact = nact; self.pay = pay; self.g = g; self.names = names
        self.R = sorted({tuple(int(v) for v in pay[a]) for a in itertools.product(*[range(n) for n in nact])},
                        key=_okey)

    def outcome(self, a):
        return tuple(int(v) for v in self.pay[tuple(a)])


def _okey(x):
    """canonical order: disagreement, grand outcomes, then pair outcomes by pair and split (largest first)."""
    z = sum(1 for v in x if v == 0)
    pair = tuple(i for i in range(len(x)) if x[i] > 0)
    return (0 if z == len(x) else (1 if z == 0 else 2), pair, tuple(-v for v in x))


def dollar3_game():
    n = 9
    pay = np.zeros((n, n, n, 3), np.int64)
    for a in itertools.product(range(n), repeat=3):
        u, t = D.outcome(D.PARTNER, *a)
        pay[a] = u
    names = [[D.act_name(s, l) for l in range(9)] for s in range(3)]
    return Game((n, n, n), pay, 6, names)


def ext_actions(g):
    """extended constants game on the 1/g grid: actions (partner index pi in {0, 1, ALL=2}, demand d in 1..g-1),
    local index l = pi*(g-1) + (d-1); pi = 0, 1 are the slot's two others in increasing order."""
    return [(pi, d) for pi in range(3) for d in range(1, g)]


def ext_game(g):
    acts = ext_actions(g); n = len(acts)
    pay = np.zeros((n, n, n, 3), np.int64)
    for a in itertools.product(range(n), repeat=3):
        pay[a] = ext_outcome(g, acts, a)
    names = [['(%s,%d/%d)' % ('ALL' if pi == 2 else str(D.others(s)[pi] + 1), d, g) for (pi, d) in acts] for s in range(3)]
    return Game((n, n, n), pay, g, names)


def ext_outcome(g, acts, a):
    ps = []; ds = []
    for s in range(3):
        pi, d = acts[a[s]]
        ps.append(3 if pi == 2 else D.others(s)[pi]); ds.append(d)
    u = [0, 0, 0]
    if ps[0] == 3 and ps[1] == 3 and ps[2] == 3:
        if sum(ds) <= g:
            return ds
        return u
    for s in range(3):
        t = ps[s]
        if t != 3 and t > s and ps[t] == s:
            if ds[s] + ds[t] <= g:
                u[s] = ds[s]; u[t] = ds[t]
            return u
    return u


def chicken_game():
    """two-player chicken (St = 0, Sw = 1), payoffs (-10, 2, -1, 0) as games/chicken.yaml."""
    P = np.array([[-10, 2], [-1, 0]])
    pay = np.zeros((2, 2, 2), np.int64)
    for a in range(2):
        for b in range(2):
            pay[a, b] = (P[a, b], P[b, a])
    return pay


# ====================================================================== relations
def grid(g, efficient=False):
    X = [(a, b, c) for a in range(g + 1) for b in range(g + 1) for c in range(g + 1)
         if (a + b + c == g if efficient else a + b + c <= g)]
    return sorted(X, key=_okey)


def dom_M(X, g):
    """M[x, y] = x strictly majority-dominates y (some winning coalition |S| >= 2, effective sum <= g, all of S
    strictly better)."""
    A = np.array(X); n = len(X)
    M = np.zeros((n, n), bool)
    for S in PAIRS + ((0, 1, 2),):
        eff = A[:, list(S)].sum(1) <= g
        better = np.ones((n, n), bool)
        for i in S:
            better &= A[:, None, i] > A[None, :, i]
        M |= better & eff[:, None]
    return M


def dom_C(nact, pay, X, players=3):
    """C[x, y]: some coalition S commits to a_S; the complement responds with its pure Nash equilibria (individual
    best replies) given a_S; x is one of the resulting outcomes and every resulting outcome gives every member of S
    strictly more than y.  `pay` indexed by full action profiles -> payoff vector.  Returns (C, by_size) where
    by_size[k] is the relation restricted to coalitions of size k."""
    idx = {tuple(int(v) for v in x): k for k, x in enumerate(X)}
    A = np.array(X); n = len(X)
    out = {k: np.zeros((n, n), bool) for k in range(1, players + 1)}
    allp = list(range(players))
    for k in range(1, players + 1):
        for S in itertools.combinations(allp, k):
            T = [p for p in allp if p not in S]
            for aS in itertools.product(*[range(nact[p]) for p in S]):
                resp = []
                if not T:
                    resp = [()]
                else:
                    for aT in itertools.product(*[range(nact[p]) for p in T]):
                        prof = [0] * players
                        for p, v in zip(S, aS): prof[p] = v
                        for p, v in zip(T, aT): prof[p] = v
                        ok = True
                        for j, p in enumerate(T):
                            cur = pay[tuple(prof)][p]
                            for alt in range(nact[p]):
                                if alt == prof[p]: continue
                                q = list(prof); q[p] = alt
                                if pay[tuple(q)][p] > cur:
                                    ok = False; break
                            if not ok: break
                        if ok:
                            resp.append(aT)
                if not resp:
                    continue
                outs = []
                for aT in resp:
                    prof = [0] * players
                    for p, v in zip(S, aS): prof[p] = v
                    for p, v in zip(T, aT): prof[p] = v
                    outs.append(tuple(int(v) for v in pay[tuple(prof)]))
                mins = np.array([min(o[i] for o in outs) for i in S])
                ys = np.all(A[:, list(S)] < mins[None, :], axis=1)
                for o in set(outs):
                    if o in idx:
                        out[k][idx[o]] |= ys
    C = np.zeros((n, n), bool)
    for k in out:
        C |= out[k]
    return C, out


COALS = tuple(S for k in (1, 2, 3) for S in itertools.combinations(range(3), k))


def eff_tu(X, g):
    """TU (Harsanyi/Chwe) effectiveness: E[S][z, w] iff sum_{i in S} w_i <= v(S) (v = g for |S| >= 2, 0 for
    singletons), w != z.  Others' payoffs are unrestricted (the classical, permissive convention)."""
    A = np.array(X); n = len(X)
    E = {}
    for S in COALS:
        v = g if len(S) >= 2 else 0
        ok = A[:, list(S)].sum(1) <= v
        m = np.repeat(ok[None, :], n, 0)
        np.fill_diagonal(m, False)
        E[S] = m
    return E


def eff_game(game, X):
    """game effectiveness: E[S][z, w] iff some action profile realizing z and some realizing w differ only in S's
    coordinates (S changes its own actions, the others' actions fixed), w != z."""
    idx = {x: k for k, x in enumerate(X)}
    n = len(X); nact = game.nact
    E = {S: np.zeros((n, n), bool) for S in COALS}
    prof = list(itertools.product(*[range(k) for k in nact]))
    outc = {a: idx[game.outcome(a)] for a in prof}
    for S in COALS:
        T = [p for p in range(3) if p not in S]
        groups = {}
        for a in prof:
            groups.setdefault(tuple(a[p] for p in T), set()).add(outc[a])
        for grp in groups.values():
            gl = list(grp)
            for z in gl:
                for w in gl:
                    if z != w:
                        E[S][z, w] = True
    return E


def indirect(X, E):
    """indirect dominance F[x, y] = x >> y: a chain of >= 1 moves from y ending at x, each move by an effective
    coalition whose every member strictly prefers x to the state it leaves (Harsanyi 1974, Chwe 1994)."""
    A = np.array(X); n = len(X)
    F = np.zeros((n, n), bool)
    for x in range(n):
        P = A[x][None, :] > A
        prefS = {S: np.all(P[:, list(S)], axis=1) for S in COALS}
        R = np.zeros(n, bool); R[x] = True
        changed = True
        while changed:
            changed = False
            for S in COALS:
                cand = prefS[S] & ~R
                if not cand.any():
                    continue
                hit = cand & E[S][:, R].any(1)
                if hit.any():
                    R |= hit; changed = True
        R[x] = False
        F[x] = R
    return F


def lcs(X, E, F):
    """Chwe's largest consistent set: iterate Z <- {x in Z: for every S and every z != x that S can move to from x,
    some w in Z with w = z or w >> z such that not every i in S strictly prefers w to x}."""
    A = np.array(X); n = len(X)
    Z = np.ones(n, bool)
    eye = np.eye(n, dtype=bool)
    while True:
        newZ = Z.copy()
        for x in np.nonzero(Z)[0]:
            ok = True
            for S in COALS:
                notpref = ~np.all(A[:, list(S)] > A[x, list(S)][None, :], axis=1)
                for z in np.nonzero(E[S][x])[0]:
                    if not (Z & (F[:, z] | eye[z]) & notpref).any():
                        ok = False; break
                if not ok: break
            if not ok:
                newZ[x] = False
        if (newZ == Z).all():
            return Z
        Z = newZ


# ====================================================================== kernels (stable sets)
def kernels(Dm, cap=200000):
    """All kernels of the digraph Dm[x, y] (x dominates y): independent and absorbing.  Backtracking over an
    unabsorbed vertex's candidate set (itself and its undecided dominators), each kernel produced once.
    Returns (list of frozensets, complete flag)."""
    n = Dm.shape[0]
    out_nb = [0] * n; in_nb = [0] * n
    for x in range(n):
        for y in range(n):
            if Dm[x, y] and x != y:
                out_nb[x] |= 1 << y; in_nb[y] |= 1 << x
    selfloop = [bool(Dm[x, x]) for x in range(n)]
    full = (1 << n) - 1
    res = []
    state = dict(stop=False)

    def absorbed_mask(IN):
        m = IN
        x = IN
        while x:
            b = x & -x; v = b.bit_length() - 1; x ^= b
            m |= out_nb[v]
        return m

    def rec(IN, OUT):
        if state['stop']:
            return
        absb = absorbed_mask(IN)
        rest = full & ~absb
        if rest == 0:
            res.append(IN);
            if len(res) >= cap:
                state['stop'] = True
            return
        # pick the unabsorbed vertex with the fewest candidates
        best = None; bc = None
        x = rest
        while x:
            b = x & -x; v = b.bit_length() - 1; x ^= b
            cand = (in_nb[v] | (1 << v)) & ~OUT
            if selfloop[v]:
                cand &= ~(1 << v)
            c = bin(cand).count('1')
            if best is None or c < bc:
                best, bc = (v, cand), c
                if c == 0:
                    return
        v, cand = best
        excl = 0
        x = cand
        while x:
            b = x & -x; u = b.bit_length() - 1; x ^= b
            conf = out_nb[u] | in_nb[u]
            if conf & IN:
                excl |= b; continue
            rec(IN | b, OUT | excl | conf)
            excl |= b

    rec(0, 0)
    sets = [frozenset(v for v in range(n) if (m >> v) & 1) for m in res]
    return sets, not state['stop']


def is_stable(Dm, V):
    V = sorted(V); n = Dm.shape[0]
    Vm = np.zeros(n, bool); Vm[V] = True
    if Dm[np.ix_(Vm, Vm)].any():
        return False
    outside = ~Vm
    return bool(Dm[np.ix_(Vm, outside)].any(0).all()) if outside.any() else True


def brute_kernels(Dm):
    n = Dm.shape[0]; out = []
    for m in range(1 << n):
        V = [v for v in range(n) if (m >> v) & 1]
        if is_stable(Dm, V):
            out.append(frozenset(V))
    return out


# ====================================================================== outcome labels
def label(x):
    z = [i for i in range(3) if x[i] == 0]
    if len(z) == 3: return 'X'
    if not z: return 'G(%d,%d,%d)' % x
    p = [i for i in range(3) if x[i] > 0]
    if len(p) == 1: return 'S%d:%d' % (p[0] + 1, x[p[0]])
    return 'P%d%d:%d|%d' % (p[0] + 1, p[1] + 1, x[p[0]], x[p[1]])


def category(x, g):
    z = sum(1 for v in x if v == 0)
    if z == 3: return 'disagreement'
    if z == 0:
        if sum(x) < g: return 'grand-wasteful'
        return 'grand-equal' if len(set(x)) == 1 else 'grand-unequal'
    if z == 2: return 'single'
    a, b = [v for v in x if v > 0]
    if a + b < g: return 'wasteful'
    return 'fair' if a == b else 'unequal'


def symmetric_set(X, g):
    return frozenset(k for k, x in enumerate(X) if category(x, g) == 'fair')


def discriminatory_counts(X, g, V):
    """for each (k, c > 0): the number of points of V on D_k(c) with all coordinates positive."""
    out = {}
    for k in range(3):
        for c in range(1, g):
            m = sum(1 for v in V if X[v][k] == c and sum(X[v]) == g and min(X[v]) > 0)
            if m:
                out[(k, c)] = m
    return out


# ====================================================================== program tables for the lottery
_ARMS = {}


def arm_data(arm):
    """arm in {'weak', 'modalPA'}: (Slots, mu, fs).  Both arms share the canonical functions and the prior."""
    if arm not in _ARMS:
        L, S, mu, cnt, size = D.build(arm, 6)
        _ARMS[arm] = (S, mu)
    return _ARMS[arm]


@njit(cache=True)
def _joint_table(armi, nat, atL, atJ, atA, tab, PARTNER, U0, U1, U2):
    K0, K1, K2 = U0.shape[0], U1.shape[0], U2.shape[0]
    J = np.empty((K0, K1, K2), np.int32)
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64); u = np.empty(3, np.int64)
    for a in range(K0):
        for b in range(K1):
            for c in range(K2):
                D.enc_into(armi, nat, atL, atJ, atA, tab, PARTNER, U0[a], U1[b], U2[c], hist, val, u)
                J[a, b, c] = val[0] * 81 + val[1] * 9 + val[2]
    return J


class Tables:
    """Joint-code payoff tables of a game on its realizable outcome list R: PAY[code, s] (dollar units), VEC[code]
    (outcome id), ISMEM[o] (fair pair), TOT[o] (total payoff, dollar units)."""

    def __init__(self, game):
        self.game = game
        n = game.nact[0]
        self.n = n
        self.R = game.R
        self.ridx = {x: k for k, x in enumerate(self.R)}
        codes = n ** 3
        self.PAY = np.zeros((codes, 3)); self.VEC = np.zeros(codes, np.int64)
        for a in itertools.product(range(n), repeat=3):
            c = a[0] * n * n + a[1] * n + a[2]
            x = game.outcome(a)
            self.PAY[c] = np.array(x) / game.g
            self.VEC[c] = self.ridx[x]
        g = game.g
        self.cat = [category(x, g) for x in self.R]
        self.ISMEM = np.array([c == 'fair' for c in self.cat], np.bool_)
        self.TOT = np.array([sum(x) / g for x in self.R])
        self.labels = [label(x) for x in self.R]


# ====================================================================== the island kernel
@njit(cache=True)
def _code(J, s, k, p, q):
    if s == 0:
        return J[k, p, q]
    if s == 1:
        return J[p, k, q]
    return J[p, q, k]


@njit(cache=True)
def _others(s):
    if s == 0:
        return 1, 2
    if s == 1:
        return 0, 2
    return 0, 1


@njit(cache=True)
def _fit_full(J, PAY, counts, pres, npres, i, s, k):
    o1, o2 = _others(s)
    v = 0.0
    for t1 in range(npres[i, o1]):
        p = pres[i, o1, t1]
        for t2 in range(npres[i, o2]):
            q = pres[i, o2, t2]
            v += counts[i, o1, p] * counts[i, o2, q] * PAY[_code(J, s, k, p, q), s]
    return v


@njit(cache=True)
def _parent(F, counts, pres, npres, i, s, N2, w):
    m = -1e300
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        f = F[i, s, k] / N2
        if f > m: m = f
    tot = 0.0
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        tot += counts[i, s, k] * np.exp(w * (F[i, s, k] / N2 - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        acc += counts[i, s, k] * np.exp(w * (F[i, s, k] / N2 - m))
        if u <= acc:
            return k
    return pres[i, s, npres[i, s] - 1]


@njit(cache=True)
def _closed(J, cls0, n0, cls1, n1, cls2, n2):
    """play identity: in every slot, all listed classes give the same joint code against every combination of the
    other slots' listed classes."""
    for tb in range(n1):
        x = cls1[tb]
        for tc in range(n2):
            y = cls2[tc]
            k0 = J[cls0[0], x, y]
            for ta in range(1, n0):
                if J[cls0[ta], x, y] != k0:
                    return False
    for ta in range(n0):
        b = cls0[ta]
        for tc in range(n2):
            y = cls2[tc]
            k0 = J[b, cls1[0], y]
            for tb in range(1, n1):
                if J[b, cls1[tb], y] != k0:
                    return False
        for tb in range(n1):
            x = cls1[tb]
            k0 = J[b, x, cls2[0]]
            for tc in range(1, n2):
                if J[b, x, cls2[tc]] != k0:
                    return False
    return True


@njit(cache=True)
def _setact(u, a, act, apos, nact):
    p = apos[u]
    if a and p >= nact:
        j = act[nact]; act[nact] = u; act[p] = j; apos[u] = nact; apos[j] = p; nact += 1
    elif (not a) and p < nact:
        nact -= 1; j = act[nact]; act[nact] = u; act[p] = j; apos[u] = nact; apos[j] = p
    return nact


@njit(cache=True)
def _classify(J, VEC, ISMEM, TOT, counts, pres, npres, i, N, dist, nout):
    for z in range(nout):
        dist[z] = 0.0
    N3 = float(N) * N * N
    for ta in range(npres[i, 0]):
        a = pres[i, 0, ta]
        for tb in range(npres[i, 1]):
            b = pres[i, 1, tb]
            for tc in range(npres[i, 2]):
                c = pres[i, 2, tc]
                dist[VEC[J[a, b, c]]] += counts[i, 0, a] * counts[i, 1, b] * counts[i, 2, c] / N3
    mx = -1.0; arg = 0; mem = 0.0; eff = 0.0
    for z in range(nout):
        if dist[z] > mx:
            mx = dist[z]; arg = z
        if ISMEM[z]:
            mem += dist[z]
        eff += dist[z] * TOT[z]
    if mx >= 0.95:
        return arg, eff
    if mem >= 0.95:
        return nout, eff
    return nout + 1, eff


@njit(cache=True)
def kern(J, PAY, VEC, ISMEM, TOT, init, N, w, m, seed, H, close_every, hrec, evcap):
    """eps = 0 island lottery, three slot populations per island; the birth-death law and the random-draw order of
    sog_lottery.kern with a check every generation.  Returns status (1 globally closed, 5 every island locally
    closed at m = 0, 4 censored at H), the stop generation, final counts, the per-generation island classes
    cls[g, i] (outcome id, nout = member-mixed, nout + 1 = other-mixed), efficiency and outcome distributions at the
    generations in hrec, the dominance-change event log (gen, island, slot, old, new, intro, t10, dpay), the number
    of events (> evcap = overflow) and the number of migrant births."""
    np.random.seed(seed)
    I = init.shape[0]; K = init.shape[2]
    nout = ISMEM.shape[0]
    counts = init.copy()
    pres = np.zeros((I, 3, K), np.int64); npres = np.zeros((I, 3), np.int64); pos = -np.ones((I, 3, K), np.int64)
    glob = np.zeros((3, K), np.int64)
    F = np.zeros((I, 3, K))
    intro = np.full((I, 3, K), -2, np.int64)
    t10 = np.full((I, 3, K), -1, np.int64)
    for i in range(I):
        for s in range(3):
            for k in range(K):
                if counts[i, s, k] > 0:
                    pres[i, s, npres[i, s]] = k; pos[i, s, k] = npres[i, s]; npres[i, s] += 1
                    glob[s, k] += counts[i, s, k]
                    intro[i, s, k] = -1
                    if counts[i, s, k] * 10 >= N:
                        t10[i, s, k] = 0
    for i in range(I):
        for s in range(3):
            for t in range(npres[i, s]):
                k = pres[i, s, t]
                F[i, s, k] = _fit_full(J, PAY, counts, pres, npres, i, s, k)
    NU = 3 * I
    act = np.arange(NU); apos = np.arange(NU); nact = 0
    for u in range(NU):
        if npres[u // 3, u % 3] > 1:
            nact = _setact(u, True, act, apos, nact)
    cls = np.zeros((H + 1, I), np.int16)
    nh = hrec.shape[0]
    effrec = np.zeros((nh, I)); distrec = np.zeros((nh, I, nout))
    dist = np.zeros(nout)
    dom = -np.ones((I, 3), np.int64)
    ev = np.zeros((evcap, 8))
    nev = 0
    N2 = float(N) * N
    UN = NU * N
    mm = m if I > 1 else 0.0
    for i in range(I):
        c, e = _classify(J, VEC, ISMEM, TOT, counts, pres, npres, i, N, dist, nout)
        cls[0, i] = c
        for s in range(3):
            for t in range(npres[i, s]):
                k = pres[i, s, t]
                if 2 * counts[i, s, k] > N:
                    dom[i, s] = k
            if dom[i, s] >= 0 and nev < evcap:
                ev[nev, 0] = 0; ev[nev, 1] = i; ev[nev, 2] = s; ev[nev, 3] = -1; ev[nev, 4] = dom[i, s]
                ev[nev, 5] = -1; ev[nev, 6] = 0; ev[nev, 7] = np.nan
                nev += 1
    b = 0
    g = 0
    hi = 0
    nextchk = UN
    status = 4; stop_gen = H
    nmig = 0
    total = H * UN
    cls0 = np.zeros(K, np.int64); cls1 = np.zeros(K, np.int64); cls2 = np.zeros(K, np.int64)
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
                c, e = _classify(J, VEC, ISMEM, TOT, counts, pres, npres, i, N, dist, nout)
                cls[g, i] = c
                if hi < nh and hrec[hi] == g:
                    effrec[hi, i] = e
                    for z in range(nout):
                        distrec[hi, i, z] = dist[z]
                for s in range(3):
                    nd = -1
                    for t in range(npres[i, s]):
                        k = pres[i, s, t]
                        if t10[i, s, k] < 0 and counts[i, s, k] * 10 >= N:
                            t10[i, s, k] = g
                        if 2 * counts[i, s, k] > N:
                            nd = k
                    if nd >= 0 and nd != dom[i, s]:
                        # a change of the slot's (last) majority class; dom keeps the last majority class
                        if nev < evcap:
                            ev[nev, 0] = g; ev[nev, 1] = i; ev[nev, 2] = s; ev[nev, 3] = dom[i, s]; ev[nev, 4] = nd
                            ev[nev, 5] = intro[i, s, nd]; ev[nev, 6] = t10[i, s, nd]
                            if dom[i, s] >= 0:
                                ev[nev, 7] = (_fit_full(J, PAY, counts, pres, npres, i, s, nd) - _fit_full(J, PAY, counts, pres, npres, i, s, dom[i, s])) / N2
                            else:
                                ev[nev, 7] = np.nan
                        nev += 1
                        dom[i, s] = nd
            if hi < nh and hrec[hi] == g:
                hi += 1
            done = False
            if g % close_every == 0 or g == H:
                if mm > 0.0:
                    n0 = 0; n1 = 0; n2 = 0
                    for k in range(K):
                        if glob[0, k] > 0:
                            cls0[n0] = k; n0 += 1
                        if glob[1, k] > 0:
                            cls1[n1] = k; n1 += 1
                        if glob[2, k] > 0:
                            cls2[n2] = k; n2 += 1
                    if _closed(J, cls0, n0, cls1, n1, cls2, n2):
                        status = 1; stop_gen = g; done = True
                else:
                    allc = True
                    for i in range(I):
                        if not _closed(J, pres[i, 0], npres[i, 0], pres[i, 1], npres[i, 1], pres[i, 2], npres[i, 2]):
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
        child = _parent(F, counts, pres, npres, src, s, N2, w)
        r = np.random.randint(N); acc = 0; victim = pres[i, s, 0]
        for t in range(npres[i, s]):
            k = pres[i, s, t]; acc += counts[i, s, k]
            if r < acc:
                victim = k; break
        if victim == child:
            continue
        counts[i, s, victim] -= 1; glob[s, victim] -= 1
        if counts[i, s, victim] == 0:
            p = pos[i, s, victim]; last = pres[i, s, npres[i, s] - 1]
            pres[i, s, p] = last; pos[i, s, last] = p; pos[i, s, victim] = -1; npres[i, s] -= 1
            intro[i, s, victim] = -2; t10[i, s, victim] = -1
        new = counts[i, s, child] == 0
        if new:
            pres[i, s, npres[i, s]] = child; pos[i, s, child] = npres[i, s]; npres[i, s] += 1
            intro[i, s, child] = g + 1
        counts[i, s, child] += 1; glob[s, child] += 1
        o1, o2 = _others(s)
        for sa in (o1, o2):
            sb = o1 + o2 - sa
            for ta in range(npres[i, sa]):
                k = pres[i, sa, ta]
                v = 0.0
                for tb in range(npres[i, sb]):
                    q = pres[i, sb, tb]
                    if s < sb:
                        v += counts[i, sb, q] * (PAY[_code(J, sa, k, child, q), sa] - PAY[_code(J, sa, k, victim, q), sa])
                    else:
                        v += counts[i, sb, q] * (PAY[_code(J, sa, k, q, child), sa] - PAY[_code(J, sa, k, q, victim), sa])
                F[i, sa, k] += v
        if new:
            F[i, s, child] = _fit_full(J, PAY, counts, pres, npres, i, s, child)
        nact = _setact(u, npres[i, s] > 1, act, apos, nact)
    for gg in range(stop_gen + 1, H + 1):
        for i in range(I):
            cls[gg, i] = cls[stop_gen, i]
    for z in range(hi, nh):
        if hrec[z] > stop_gen:
            for i in range(I):
                c, e = _classify(J, VEC, ISMEM, TOT, counts, pres, npres, i, N, dist, nout)
                effrec[z, i] = e
                for zz in range(nout):
                    distrec[z, i, zz] = dist[zz]
    return status, stop_gen, counts, cls, effrec, distrec, ev[:min(nev, evcap)], nev, nmig


# ====================================================================== seed laws
def const_index(fs):
    return {f[1][0]: x for x, f in enumerate(fs) if not f[0]}


def seed_law(law, slot, rng=None, cat=None):
    """probability vector over the 1,305 canonical functions (weak / modalPA grammar) for a slot."""
    S, mu = arm_data('weak')
    fs = S.fs
    p = mu.copy()
    if law in ('L', 'M'):
        return p / p.sum()
    if law == 'K':
        q = np.zeros_like(p)
        for l, x in const_index(fs).items():
            q[x] = 1.0
        return q / q.sum()
    if law == 'A':
        if slot == 2:
            for x, f in enumerate(fs):
                if all(l % 3 == 0 for l in f[1]):
                    p[x] *= 4.0
        return p / p.sum()
    if law == 'U':
        q = np.zeros_like(p); q[cat] = 1.0
        return q / q.sum()
    raise ValueError(law)


def target_constants(target):
    """local actions per slot (None = excluded slot, drawn from the prior)."""
    lo = D.local_of
    if target == 'fair':
        return [lo(0, 1, 1), lo(1, 0, 1), None]
    if target == 'unequal':
        return [lo(0, 1, 2), lo(1, 0, 0), None]
    if target == 'wasteful':
        return [lo(0, 1, 0), lo(1, 0, 0), None]
    if target == 'grand':
        return [lo(s, D.ALL, 0) for s in range(3)]
    raise ValueError(target)


def draw_seeds(rng, I, N, laws):
    """laws[s] probability vectors; returns init (I, 3, Kfs) counts over canonical functions."""
    K = len(laws[0])
    out = np.zeros((I, 3, K), np.int64)
    for i in range(I):
        for s in range(3):
            out[i, s] = rng.multinomial(N, laws[s])
    return out


def compress(init):
    """map canonical-function counts to per-slot universes: returns (init_local (I, 3, Kmax), U list per slot)."""
    I = init.shape[0]
    U = [np.nonzero(init[:, s, :].sum(0))[0] for s in range(3)]
    Kmax = max(len(u) for u in U)
    loc = np.zeros((I, 3, Kmax), np.int64)
    for s in range(3):
        loc[:, s, :len(U[s])] = init[:, s, U[s]]
    return loc, U


def joint_for(arm, U):
    S, mu = arm_data(arm)
    armi = D.ARM[arm]
    Kmax = max(len(u) for u in U)
    Up = [np.concatenate([u, np.full(Kmax - len(u), u[0])]).astype(np.int64) for u in U]
    return _joint_table(armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, Up[0], Up[1], Up[2])


def ext_joint(g, U):
    n = 3 * (g - 1)
    Kmax = max(len(u) for u in U)
    Up = [np.concatenate([u, np.full(Kmax - len(u), u[0])]).astype(np.int64) for u in U]
    return (Up[0][:, None, None] * n * n + Up[1][None, :, None] * n + Up[2][None, None, :]).astype(np.int32)


# ====================================================================== analysis helpers
HELD = 25


def held_runs(seq, nout, minlen=HELD):
    """list of (class, start, end) maximal runs of a non-mixed class lasting >= minlen generations."""
    out = []
    t = 0; T = len(seq)
    while t < T:
        c = seq[t]; u = t
        while u + 1 < T and seq[u + 1] == c:
            u += 1
        if c < nout and u - t + 1 >= minlen:
            out.append((int(c), t, u))
        t = u + 1
    return out


def segments(seq, a, b):
    """segments (class, length) of seq[a:b]."""
    out = []
    t = a
    while t < b:
        c = seq[t]; u = t
        while u + 1 < b and seq[u + 1] == c:
            u += 1
        out.append((int(c), u - t + 1))
        t = u + 1
    return out


def trigger(events_i, tA, tB, conds_at, tol=1e-9):
    """classify a flip from the dominance-change events on its island in (tA, tB] (rows: gen, island, slot, old,
    new, intro, t10, dpay) and whether a conditional program is a dominant class at either end (conds_at)."""
    rows = [e for e in events_i if tA < e[0] <= tB and e[4] >= 0]
    if not rows:
        return 'no-dominant-change', 0
    slots = sorted({int(e[2]) for e in rows})
    kinds = []
    rows = [e for e in rows if not np.isnan(e[7])] or rows
    for e in rows:
        d = e[7]
        if np.isnan(d): kinds.append('n/a')
        elif d > tol: kinds.append('strict')
        elif d < -tol: kinds.append('deleterious')
        else: kinds.append('neutral')
    conc = False
    for x in range(len(rows)):
        for y in range(x + 1, len(rows)):
            if rows[x][2] != rows[y][2] and rows[y][6] >= 0 and rows[y][6] <= rows[x][0]:
                conc = True
    if len(slots) == 1 and conds_at:
        return 'conditional', len(slots)
    if len(slots) >= 2 and conc:
        return 'two-slot coincidence', len(slots)
    if all(k == 'neutral' for k in kinds):
        return 'pure drift', len(slots)
    if len(slots) >= 2 and kinds[0] == 'neutral' and 'strict' in kinds[1:]:
        return 'drift-prepared', len(slots)
    if len(slots) == 1 and kinds[-1] == 'strict':
        return 'single-slot strict', 1
    return 'other', len(slots)
