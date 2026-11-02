"""The pair-worth-a game on islands (spec specs/2026-11-01-pair-worth.md; notes notes/pair-worth.md).

Games (three slots, any pair worth v, the grand coalition worth Gd ticks):
  pw13, pw23, pw56   pair worth a = 1/3 (sixths), 2/3 (sixths), 5/6 (twelfths)
  gl6                glove monopolist, slot 0 = R: v(R, L) = Gd, v(L1, L2) = 0 (sixths)
  pw23t, gl24        the same on 24ths (transfer cells)
Actions of a slot: l = (Gd + 1) * pi + d, pi in {0, 1} the slot's two others in increasing order, 2 = ALL, d = 0..Gd.

Programs are decision lists over box atoms BOX_L(THEM_j = a) evaluated on the encounter's linear GL Kripke chain
(dollar3.eval_modal semantics).  Named families: bids B (grand if both others provably bid; else Löbian pair handshakes
at the exclusion split; else the fallback constant c), blockers K (pair handshakes first), accept-pair bids A, grand
constants G; B0/A0/K0 are the as-written level-0 variants (notes 1.3: their handshake lines never hold).

Importable without side effects.
"""
import os, sys, zlib
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import itertools
import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ALL = 3
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAIRS = ((0, 1), (0, 2), (1, 2))
MAXL = 64           # longest decision list (A for R at 24ths: 2 * 25 + 1)
VAC, BRK = -2, -1


def others(s):
    return [t for t in range(3) if t != s]


# ====================================================================== games
class Game:
    def __init__(self, name, Gd, v, glove=False):
        self.name, self.Gd, self.v, self.glove = name, Gd, v, glove     # v[i][j] symmetric, ticks
        self.nact = 3 * (Gd + 1)
        self.PARTNER = np.array([[self.partner(s, l) for l in range(self.nact)] for s in range(3)], np.int64)
        self.DEM = np.array([l % (Gd + 1) for l in range(self.nact)], np.int64)
        self._build_outcomes()

    # action helpers
    def act(self, s, partner, d):
        pi = 2 if partner == ALL else others(s).index(partner)
        return (self.Gd + 1) * pi + d

    def partner(self, s, l):
        pi = l // (self.Gd + 1)
        return others(s)[pi] if pi < 2 else ALL

    def aname(self, s, l):
        p = self.partner(s, l)
        return '(%s,%d)' % ('ALL' if p == ALL else str(p), l % (self.Gd + 1))

    def outcome_of(self, a):
        """(kind, pair index or -1, payoff vector in ticks) for the action triple a; kind 0 null, 1 grand, 2 pair."""
        Gd = self.Gd
        ps = [self.PARTNER[s, a[s]] for s in range(3)]
        ds = [int(self.DEM[a[s]]) for s in range(3)]
        if ps[0] == ALL and ps[1] == ALL and ps[2] == ALL:
            if sum(ds) <= Gd:
                return (1, -1, tuple(ds))
            return (0, -1, (0, 0, 0))
        for s in range(3):
            t = ps[s]
            if t != ALL and t > s and ps[t] == s:
                if ds[s] + ds[t] <= self.v[s][t]:
                    u = [0, 0, 0]
                    u[s] = ds[s]; u[t] = ds[t]
                    if u == [0, 0, 0]:
                        return (0, -1, (0, 0, 0))
                    return (2, PAIRS.index((s, t)), tuple(u))
                return (0, -1, (0, 0, 0))
        return (0, -1, (0, 0, 0))

    def _build_outcomes(self):
        n = self.nact
        ids = {(0, -1, (0, 0, 0)): 0}
        lst = [(0, -1, (0, 0, 0))]
        OUT = np.zeros((n, n, n), np.int16)
        for a in itertools.product(range(n), repeat=3):
            o = self.outcome_of(a)
            k = ids.get(o)
            if k is None:
                k = len(lst); ids[o] = k; lst.append(o)
            OUT[a] = k
        self.OUT = OUT
        self.outs = lst
        self.oid = ids
        self.nout = len(lst)
        self.KIND = np.array([o[0] for o in lst], np.int64)
        self.VEC = np.array([o[2] for o in lst], np.int64)             # (nout, 3) ticks
        self.PAY = self.VEC.astype(float) / self.Gd                    # dollars
        self.TOT = self.PAY.sum(1)

    # ------------------------------------------------------------ static classification by payoff vector
    def vectors(self):
        return sorted({o[2] for o in self.outs})

    def coalitions(self):
        return [((0, 1), self.v[0][1]), ((0, 2), self.v[0][2]), ((1, 2), self.v[1][2]), ((0, 1, 2), self.Gd)]

    def dominates(self, x, y, weak=False):
        for S, cap in self.coalitions():
            if sum(x[i] for i in S) > cap:
                continue
            if weak:
                if all(x[i] >= y[i] for i in S) and any(x[i] > y[i] for i in S):
                    return True
            elif all(x[i] > y[i] for i in S):
                return True
        return False

    def in_core(self, y):
        return sum(y) == self.Gd and all(sum(y[i] for i in S) >= cap for S, cap in self.coalitions()[:3])

    def classify_vectors(self):
        """class of each distinct payoff vector: 0 null, 1 core proper, 2 ring (strictly undominated efficient, not
        core), 3 efficient dominated, 4 undominated wasteful, 5 dominated wasteful."""
        R = self.vectors()
        und = {y for y in R if not any(self.dominates(x, y) for x in R)}
        cl = {}
        for y in R:
            if sum(y) == 0:
                cl[y] = 0
            elif self.in_core(y):
                cl[y] = 1
            elif sum(y) == self.Gd:
                cl[y] = 2 if y in und else 3
            else:
                cl[y] = 4 if y in und else 5
        return cl, und

    def class_tables(self):
        """CLA[o]: vector class (6); CLB[o]: kind class (0 null, 1 grand efficient, 2 grand wasteful, 3 pair)."""
        cl, und = self.classify_vectors()
        CLA = np.array([cl[tuple(int(t) for t in self.VEC[o])] for o in range(self.nout)], np.int64)
        CLB = np.zeros(self.nout, np.int64)
        for o, (kind, pi, vec) in enumerate(self.outs):
            if kind == 1:
                CLB[o] = 1 if sum(vec) == self.Gd else 2
            elif kind == 2:
                CLB[o] = 3
        return CLA, CLB


CLASS_A = ['null', 'core', 'ring', 'eff-dominated', 'und-wasteful', 'dom-wasteful']
CLASS_B = ['null', 'grand-eff', 'grand-wasteful', 'pair']

_GAMES = {}


def get_game(name):
    if name in _GAMES:
        return _GAMES[name]
    if name == 'pw13':
        g = Game(name, 6, [[0, 2, 2], [2, 0, 2], [2, 2, 0]])
    elif name == 'pw23':
        g = Game(name, 6, [[0, 4, 4], [4, 0, 4], [4, 4, 0]])
    elif name == 'pw56':
        g = Game(name, 12, [[0, 10, 10], [10, 0, 10], [10, 10, 0]])
    elif name == 'gl6':
        g = Game(name, 6, [[0, 6, 6], [6, 0, 0], [6, 0, 0]], glove=True)
    elif name == 'pw23t':
        g = Game(name, 24, [[0, 16, 16], [16, 0, 16], [16, 16, 0]])
    elif name == 'gl24':
        g = Game(name, 24, [[0, 24, 24], [24, 0, 0], [24, 0, 0]], glove=True)
    elif name == 'pw1':                              # a = 1 on sixths (V1: dollar3's game when restricted)
        g = Game(name, 6, [[0, 6, 6], [6, 0, 6], [6, 6, 0]])
    else:
        raise ValueError(name)
    _GAMES[name] = g
    return g


# ====================================================================== the named programs
def pi_split(G, i, j, sigma):
    """exclusion split (pi_i, pi_j) of the pair {i, j} given the grand split sigma (ticks)."""
    w = G.v[i][j]
    if w == 0:
        return 0, 0
    if G.glove:
        den = sigma[i] + sigma[j]
        if den == 0:                         # outside the bid sets (R's share >= 1/2): equal split
            return w // 2 + (w % 2 if sigma[i] >= sigma[j] else 0), w // 2 + (w % 2 if sigma[i] < sigma[j] else 0)
        pi_, pj = (w * sigma[i]) // den, (w * sigma[j]) // den
        rem = w - pi_ - pj
        if sigma[i] >= sigma[j]:
            pi_ += rem
        else:
            pj += rem
        return pi_, pj
    a = w // 2
    odd = w % 2
    if sigma[i] > sigma[j]:
        return a + odd, a
    return a, a + odd


def _grand_line(G, i, sigma):
    j, k = others(i)
    return ([(j, G.act(j, ALL, sigma[j]), 0, 1), (k, G.act(k, ALL, sigma[k]), 0, 1)], G.act(i, ALL, sigma[i]))


def _pair_lines(G, i, sigma, lvl, prio=None):
    out = []
    for p in (prio if prio is not None else others(i)):
        pii, pip = pi_split(G, i, p, sigma)
        out.append(([(p, G.act(p, i, pip), lvl, 1)], G.act(i, p, pii)))
    return out


def program(G, kind, s, sigma, c, prio=None):
    """(lines, default) of slot s's program of the named family.  kind: 'B', 'K', 'A', 'G' (level 1 pair lines) or
    'B0', 'K0', 'A0' (level 0 throughout).  sigma: grand split in ticks (3-tuple); c: fallback action.  prio: the order
    in which the two other slots' handshakes are tried (default: increasing slot index, the spec's j < k)."""
    lvl = 0 if kind.endswith('0') else 1
    base = kind[0]
    if base == 'G':
        return ([], G.act(s, ALL, sigma[s]))
    if base == 'B':
        return ([_grand_line(G, s, sigma)] + _pair_lines(G, s, sigma, lvl, prio), c)
    if base == 'K':
        return (_pair_lines(G, s, sigma, lvl, prio) + [_grand_line(G, s, sigma)] + _pair_lines(G, s, sigma, lvl, prio), c)
    if base == 'A':
        lines = [_grand_line(G, s, sigma)]
        for p in (prio if prio is not None else others(s)):
            w = G.v[s][p]
            for d in range(w + 1):
                lines.append(([(p, G.act(p, s, d), lvl, 1)], G.act(s, p, w - d)))
        return (lines, c)
    raise ValueError(kind)


def const_program(c):
    return ([], c)


def splits(Gd, ok=lambda s: True):
    return [s for s in itertools.product(range(Gd + 1), repeat=3) if sum(s) == Gd and ok(s)]


# ====================================================================== arms (menus)
class Family:
    def __init__(self, kind, sigmas, dose):
        self.kind, self.sigmas, self.dose = kind, sigmas, dose
        self.code = {'B': 1, 'K': 2, 'A': 3, 'G': 4, 'B0': 1, 'K0': 2, 'A0': 3}[kind]


class Menu:
    """The seed law of a slot: constants uniform with probability 1 - sum(dose); family f with probability dose_f,
    uniform over its members (sigma, c) (G: sigma).  Member ids per slot: constants 0..nact-1, then the families in
    order."""

    def __init__(self, G, families):
        self.G, self.fams = G, families
        n = G.nact
        self.off = []; self.size = []
        o = n
        for f in families:
            sz = len(f.sigmas) * (1 if f.kind == 'G' else n)
            self.off.append(o); self.size.append(sz); o += sz
        self.total = o
        self.cum = np.cumsum([f.dose for f in families]) if families else np.zeros(0)

    def decode(self, m):
        """member id -> (family index or -1, sigma index, c)."""
        n = self.G.nact
        if m < n:
            return -1, -1, m
        for fi, f in enumerate(self.fams):
            if m < self.off[fi] + self.size[fi]:
                r = m - self.off[fi]
                if f.kind == 'G':
                    return fi, r, -1
                return fi, r // n, r % n
        raise ValueError(m)

    def prog(self, s, m):
        fi, si, c = self.decode(m)
        if fi < 0:
            return const_program(c)
        f = self.fams[fi]
        return program(self.G, f.kind, s, f.sigmas[si], c)

    def famcode(self, m):
        fi, _, _ = self.decode(m)
        return 0 if fi < 0 else self.fams[fi].code

    def draw(self, u1, u2, u3):
        """vectorised member ids from common random numbers: u1 uniform in [0,1) (constant), u2 (family), u3 (member)."""
        n = self.G.nact
        m = np.minimum((u1 * n).astype(np.int64), n - 1)
        lo = 0.0
        for fi, f in enumerate(self.fams):
            hi = self.cum[fi]
            sel = (u2 >= lo) & (u2 < hi)
            mem = np.minimum((u3 * self.size[fi]).astype(np.int64), self.size[fi] - 1)
            m = np.where(sel, self.off[fi] + mem, m)
            lo = hi
        return m


GAMES_MENU = {}


def bid_sigmas(gname, menu):
    """bid sigma sets (ticks). menu: 'core' (G1/3 core points), 'all' (all grand splits), 'eq' (equal split)."""
    G = get_game(gname)
    Gd = G.Gd
    if menu == 'eq':
        return [(Gd // 3,) * 3]
    if menu == 'all':
        return splits(Gd)
    if menu == 'core':
        return [s for s in splits(Gd) if G.in_core(s)]
    if menu == 'mid':       # G2/3: every share >= 1/6;  glove: R's share >= 1/2
        if G.glove:
            return splits(Gd, lambda s: 2 * s[0] >= Gd)
        return splits(Gd, lambda s: min(s) >= 1)
    raise ValueError(menu)


def arm_menu(gname, arm, delta=0.05):
    """arm names: C, CB (the game's standard bid set), CBs (all splits), CBe (equal split only), CB2 (delta 0.10),
    CG, CA, CBK, CB0, CBK0, R / RB are handled separately."""
    G = get_game(gname)
    std = {'pw13': 'core', 'pw23': 'mid', 'gl6': 'mid', 'pw56': 'eq', 'pw23t': 'mid', 'gl24': 'mid'}[gname]

    def sc(menu):
        S = bid_sigmas(gname, menu)
        if G.Gd == 24:      # transfer cells: the sixths splits scaled
            raise ValueError
        return S

    def std_set():
        if gname in ('pw23t', 'gl24'):
            base = bid_sigmas('pw23' if gname == 'pw23t' else 'gl6', 'mid')
            return [tuple(4 * t for t in s) for s in base]
        return bid_sigmas(gname, std)

    if arm == 'C':
        fams = []
    elif arm == 'CB':
        fams = [Family('B', std_set(), delta)]
    elif arm == 'CBs':
        fams = [Family('B', bid_sigmas(gname, 'all'), delta)]
    elif arm == 'CBe':
        fams = [Family('B', bid_sigmas(gname, 'eq'), delta)]
    elif arm == 'CB2':
        fams = [Family('B', std_set(), 2 * delta)]
    elif arm == 'CG':
        S = bid_sigmas(gname, 'all') if gname == 'pw13' else std_set()
        fams = [Family('G', S, delta)]
    elif arm == 'CA':
        fams = [Family('A', std_set(), delta)]
    elif arm == 'CBK':
        fams = [Family('B', std_set(), delta), Family('K', std_set(), delta)]
    elif arm == 'CB0':
        fams = [Family('B0', std_set(), delta)]
    elif arm == 'CBs0':
        fams = [Family('B0', bid_sigmas(gname, 'all'), delta)]
    elif arm == 'CBK0':
        fams = [Family('B0', std_set(), delta), Family('K0', std_set(), delta)]
    else:
        raise ValueError(arm)
    return Menu(G, fams)


# ====================================================================== evaluator (numba)
@njit(cache=True)
def eval_dl(LN, ATP, ATA, ATL, ATS, OA, DF, x0, x1, x2, hist, val):
    """Stable actions of the encounter (x0, x1, x2) on the linear GL chain (dollar3.eval_modal semantics, decision
    lists).  Returns True on success; val holds the three actions."""
    for L in range(2):
        for s in range(3):
            hist[L, s] = VAC
    for n in range(64):
        for s in range(3):
            x = x0 if s == 0 else (x1 if s == 1 else x2)
            out = DF[s, x]
            for ln in range(LN[s, x]):
                ok = True
                for t in range(2):
                    p = ATP[s, x, ln, t]
                    if p < 0:
                        continue
                    h = hist[ATL[s, x, ln, t], p]
                    holds = (h == VAC) or (h == ATA[s, x, ln, t])
                    if ATS[s, x, ln, t] == 0:
                        holds = not holds
                    if not holds:
                        ok = False
                        break
                if ok:
                    out = OA[s, x, ln]
                    break
            val[s] = out
        changed = False
        for L in range(2):
            if n < L:
                continue
            for s in range(3):
                h = hist[L, s]
                if h == VAC:
                    hist[L, s] = val[s]; changed = True
                elif h >= 0 and h != val[s]:
                    hist[L, s] = BRK; changed = True
        if not changed and n >= 2:
            return True
    return False


@njit(cache=True)
def joint_table(LN, ATP, ATA, ATL, ATS, OA, DF, OUT, K0, K1, K2, Kmax):
    J = np.zeros((Kmax, Kmax, Kmax), np.int16)
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64)
    bad = 0
    for a in range(K0):
        for b in range(K1):
            for c in range(K2):
                if eval_dl(LN, ATP, ATA, ATL, ATS, OA, DF, a, b, c, hist, val):
                    J[a, b, c] = OUT[val[0], val[1], val[2]]
                else:
                    bad += 1
    return J, bad


@njit(cache=True)
def play_triple(LN, ATP, ATA, ATL, ATS, OA, DF, a, b, c):
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64)
    ok = eval_dl(LN, ATP, ATA, ATL, ATS, OA, DF, a, b, c, hist, val)
    return ok, val[0], val[1], val[2]


class ProgTable:
    """Padded arrays of the decision lists of a universe: U[s] = member ids of slot s."""

    def __init__(self, menu, U):
        self.menu, self.U = menu, U
        self.K = [len(u) for u in U]
        Kmax = max(self.K)
        self.Kmax = Kmax
        self.LN = np.zeros((3, Kmax), np.int64)
        self.ATP = -np.ones((3, Kmax, MAXL, 2), np.int64)
        self.ATA = np.zeros((3, Kmax, MAXL, 2), np.int64)
        self.ATL = np.zeros((3, Kmax, MAXL, 2), np.int64)
        self.ATS = np.ones((3, Kmax, MAXL, 2), np.int64)
        self.OA = np.zeros((3, Kmax, MAXL), np.int64)
        self.DF = np.zeros((3, Kmax), np.int64)
        self.FAM = np.zeros((3, Kmax), np.int64)
        for s in range(3):
            for x in range(Kmax):
                m = int(U[s][x]) if x < self.K[s] else int(U[s][0])
                lines, df = menu.prog(s, m)
                self.set(s, x, lines, df)
                self.FAM[s, x] = menu.famcode(m) if x < self.K[s] else 0

    def set(self, s, x, lines, df):
        assert len(lines) <= MAXL
        self.LN[s, x] = len(lines); self.DF[s, x] = df
        for ln, (atoms, out) in enumerate(lines):
            self.OA[s, x, ln] = out
            for t, (p, a, L, sg) in enumerate(atoms):
                self.ATP[s, x, ln, t] = p; self.ATA[s, x, ln, t] = a; self.ATL[s, x, ln, t] = L; self.ATS[s, x, ln, t] = sg

    def arrs(self):
        return self.LN, self.ATP, self.ATA, self.ATL, self.ATS, self.OA, self.DF

    def joint(self, G):
        J, bad = joint_table(*self.arrs(), G.OUT, self.K[0], self.K[1], self.K[2], self.Kmax)
        assert bad == 0, 'chain did not stabilise on %d triples' % bad
        return J

    def play(self, a, b, c):
        ok, v0, v1, v2 = play_triple(*self.arrs(), a, b, c)
        assert ok
        return int(v0), int(v1), int(v2)


def table_from_programs(G, progs):
    """a ProgTable for an explicit list of (lines, default) per slot (V4/V5 hand-built triples): progs[s] = list."""
    class M:
        pass
    m = M()
    cache = {}

    def prog(s, x):
        return progs[s][x]
    m.prog = prog
    m.famcode = lambda x: 0
    K = max(len(p) for p in progs)
    t = ProgTable.__new__(ProgTable)
    t.menu = m; t.K = [len(p) for p in progs]; t.Kmax = K
    t.LN = np.zeros((3, K), np.int64); t.ATP = -np.ones((3, K, MAXL, 2), np.int64)
    t.ATA = np.zeros((3, K, MAXL, 2), np.int64); t.ATL = np.zeros((3, K, MAXL, 2), np.int64)
    t.ATS = np.ones((3, K, MAXL, 2), np.int64); t.OA = np.zeros((3, K, MAXL), np.int64)
    t.DF = np.zeros((3, K), np.int64); t.FAM = np.zeros((3, K), np.int64)
    for s in range(3):
        for x in range(K):
            lines, df = progs[s][x] if x < len(progs[s]) else progs[s][0]
            t.set(s, x, lines, df)
    return t


# ====================================================================== founders, tail schedule, universe
def seed_int(*parts):
    return zlib.crc32(('pair-worth|' + '|'.join(str(p) for p in parts)).encode()) & 0x7fffffff


def draw_founders(menu, base, r, I, N):
    """member ids (I, 3, N) with common random numbers across arms that share (base, r)."""
    rng = np.random.default_rng(seed_int('F', base, r))
    u1 = rng.random((I, 3, N)); u2 = rng.random((I, 3, N)); u3 = rng.random((I, 3, N))
    return menu.draw(u1, u2, u3)


def tail_schedule(menu, base, r, I, N, Lmax, g0, t0, gend, lams):
    """arrivals for the largest Lambda (Lmax), thinned for each Lambda in lams.  Returns dict lam -> arrays
    (g, island, slot, victim uniform, member id) sorted by g; arrivals nest across lams."""
    rng = np.random.default_rng(seed_int('T', base, r))
    gs = np.arange(g0, gend)
    mean = Lmax * (1.0 / (1.0 + (gs - g0) / t0) - 1.0 / (1.0 + (gs + 1 - g0) / t0))
    cnt = rng.poisson(mean[:, None], size=(len(gs), I))
    gi, ii = np.nonzero(cnt)
    rep = cnt[gi, ii]
    ag = np.repeat(gs[gi], rep); ai = np.repeat(ii, rep)
    n = len(ag)
    asl = rng.integers(0, 3, n); au = rng.random(n); thin = rng.random(n)
    u1 = rng.random(n); u2 = rng.random(n); u3 = rng.random(n)
    am = menu.draw(u1, u2, u3)
    out = {}
    for lam in lams:
        keep = thin < lam / Lmax
        out[lam] = (ag[keep].astype(np.int64), ai[keep].astype(np.int64), asl[keep].astype(np.int64), au[keep], am[keep])
    return out


def build_universe(menu, founders, sched_max):
    """per-slot sorted unique member ids among founders and the largest schedule; local founder counts."""
    I, _, N = founders.shape
    U = []
    for s in range(3):
        ids = set(np.unique(founders[:, s, :]).tolist())
        if sched_max is not None:
            ag, ai, asl, au, am = sched_max
            ids |= set(np.unique(am[asl == s]).tolist())
        U.append(np.array(sorted(ids), np.int64))
    Kmax = max(len(u) for u in U)
    loc = np.zeros((I, 3, Kmax), np.int64)
    for s in range(3):
        idx = np.searchsorted(U[s], founders[:, s, :])
        for i in range(I):
            loc[i, s, :] += np.bincount(idx[i], minlength=Kmax)[:Kmax]
    return U, loc


def local_arrivals(U, sched):
    ag, ai, asl, au, am = sched
    ak = np.zeros(len(am), np.int64)
    for s in range(3):
        sel = asl == s
        ak[sel] = np.searchsorted(U[s], am[sel])
    return ag, ai, asl, au, ak
