"""Three-player majority divide-the-dollar with separate slot populations
(specs/2026-10-04-three-player-dollar.md).

Game.  Slots 0, 1, 2 (the spec's 1, 2, 3).  An action of slot s is (partner,
demand): partner one of the other two slots or ALL, demand 1/3, 1/2, 2/3
(stored in sixths: 2, 3, 4).  Local action index l = 3*pi + d, where pi = 0, 1
are slot s's two others in increasing order, pi = 2 is ALL, d = 0, 1, 2 is the
demand.  A pair forms if two slots name each other with demands summing to at
most 1; a grand coalition if all name ALL with demands summing to at most 1
(only thirds); otherwise everyone gets 0.

Grammar (one per slot, absolute slot labels; every slot's language is the
image of slot 0's under a slot permutation):

    A ::= a                          9 constants, 1 node
        | if(B, A, A)                1 + |B| + |A| + |A|
    B ::= BOX_L(THEM_j = a)          3 nodes (box node with level L and action a
                                     folded in, as BOX/BOXD/BOX1 in modal.py;
                                     THEM_j; ME), j an other slot, a one of
                                     slot j's 9 actions
        | not B | and B B | or B B   1 + ...

The atom speaks about the current encounter only (spec: modal atoms are
BOX(THEM_j = a) in the current encounter).  Two arms share this grammar and
this prior, as in the E1 matched control:
  modal  BOX_L is provability in PA (L = 0) or PA + Con(PA) (L = 1), on the
         linear GL Kripke chain over the encounter (modal.py semantics);
  weak   the atom is evaluated by simulating slot j in the current encounter
         (budget iteration from bottom, evaluate.py semantics); a slot whose
         value stays bottom is divergent and plays the minimax disagreement
         action (ALL, 2/3).  Only PA-level atoms (simulation has no levels).

Prior: bits = log2 a(|p|) + 2 log2 |p| + 1 (a(s) = programs of size s), as in
every other arm; programs are merged into canonical functions (essential
atoms, action table), and mu of a canonical function is the sum over its
spellings of size <= n.
"""
import os, sys, itertools
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from abm import njit

ALL = 3
DEM = np.array([2, 3, 4], np.int64)          # demands in sixths
DNAME = ['1/3', '1/2', '2/3']
NULL_LOCAL = 8                                # (ALL, 2/3): minimax disagreement action
OUT_NAMES = ['grand', 'fair pair', 'unfair pair', 'wasteful pair', 'disagreement']


def others(s):
    return [t for t in range(3) if t != s]


def partner_abs(s, l):
    pi = l // 3
    return others(s)[pi] if pi < 2 else ALL


def local_of(s, partner, d):
    pi = 2 if partner == ALL else others(s).index(partner)
    return 3 * pi + d


def act_name(s, l):
    p = partner_abs(s, l)
    return '(%s,%s)' % ('ALL' if p == ALL else str(p + 1), DNAME[l % 3])


# ---------------------------------------------------------------- outcome
PARTNER = np.array([[partner_abs(s, l) for l in range(9)] for s in range(3)], np.int64)


@njit(cache=True)
def outcome(PARTNER, a0, a1, a2):
    """Payoffs in sixths and outcome type for local actions (a0, a1, a2).
    type 0 grand, 1 fair pair, 2 unfair pair, 3 wasteful pair, 4 disagreement."""
    a = (a0, a1, a2)
    u = np.zeros(3, np.int64)
    p0, p1, p2 = PARTNER[0, a0], PARTNER[1, a1], PARTNER[2, a2]
    ps = (p0, p1, p2)
    d0, d1, d2 = 2 + a0 % 3, 2 + a1 % 3, 2 + a2 % 3
    ds = (d0, d1, d2)
    if p0 == ALL and p1 == ALL and p2 == ALL:
        if d0 + d1 + d2 <= 6:
            u[0], u[1], u[2] = d0, d1, d2
            return u, 0
        return u, 4
    for s in range(3):
        t = ps[s]
        if t != ALL and t > s and ps[t] == s:
            if ds[s] + ds[t] <= 6:
                u[s] = ds[s]; u[t] = ds[t]
                if ds[s] + ds[t] < 6:
                    return u, 3
                if ds[s] == ds[t]:
                    return u, 1
                return u, 2
            return u, 4
    return u, 4


# ---------------------------------------------------------------- language
class Lang:
    """Canonical enumeration (abstract labels), counts per size, prior, and
    per-slot absolute program arrays.

    An abstract atom is (L, jr, al): jr = 0/1 indexes the owner's two others in
    increasing order; al is the local action index of that other slot.  A
    canonical function is (atoms tuple sorted, table tuple of local actions
    of the owner over 2^k atom valuations, bit t = atom t true)."""

    def __init__(self, n, levels=(0, 1), canon_upto=None):
        self.n, self.levels = n, tuple(levels)
        self.atoms = [(L, jr, al) for L in self.levels for jr in (0, 1) for al in range(9)]
        canon_upto = n if canon_upto is None else canon_upto
        self.cntB = [defaultdict(int) for _ in range(canon_upto + 1)]
        self.cntA = [defaultdict(int) for _ in range(canon_upto + 1)]
        self._enumerate(canon_upto)
        self.a = np.array([0] + [sum(self.cntA[s].values()) for s in range(1, canon_upto + 1)], float)

    # canonical reduction ------------------------------------------------
    @staticmethod
    def _reduce(atoms, tab):
        atoms = list(atoms); tab = list(tab)
        j = 0
        while j < len(atoms):
            k = len(atoms)
            ess = any(tab[i] != tab[i | (1 << j)] for i in range(1 << k) if not (i >> j) & 1)
            if ess:
                j += 1; continue
            nt = []
            for i in range(1 << (k - 1)):
                lo = i & ((1 << j) - 1); hi = (i >> j) << (j + 1)
                nt.append(tab[lo | hi])
            atoms.pop(j); tab = nt
        # sort atoms for a canonical key
        if len(atoms) > 1:
            order = sorted(range(len(atoms)), key=lambda t: atoms[t])
            k = len(atoms)
            nt = [None] * (1 << k)
            for i in range(1 << k):
                ni = 0
                for newpos, old in enumerate(order):
                    if (i >> old) & 1: ni |= 1 << newpos
                nt[ni] = tab[i]
            atoms = [atoms[t] for t in order]; tab = nt
        return (tuple(atoms), tuple(tab))

    @staticmethod
    def _expand(f, union):
        atoms, tab = f
        pos = [union.index(a) for a in atoms]
        out = []
        for i in range(1 << len(union)):
            sub = 0
            for t, p in enumerate(pos):
                if (i >> p) & 1: sub |= 1 << t
            out.append(tab[sub])
        return out

    def _enumerate(self, n):
        for a in self.atoms:
            if n >= 3:
                self.cntB[3][((a,), (0, 1))] += 1
        for s in range(4, n + 1):
            for f, m in self.cntB[s - 1].items():
                g = self._reduce(f[0], tuple(1 - v for v in f[1])); self.cntB[s][g] += m
            for i in range(3, s - 3):
                j = s - 1 - i
                for fa, ma in self.cntB[i].items():
                    for fb, mb in self.cntB[j].items():
                        U = sorted(set(fa[0]) | set(fb[0]))
                        ta, tb = self._expand(fa, U), self._expand(fb, U)
                        self.cntB[s][self._reduce(U, [x & y for x, y in zip(ta, tb)])] += ma * mb
                        self.cntB[s][self._reduce(U, [x | y for x, y in zip(ta, tb)])] += ma * mb
        for l in range(9):
            self.cntA[1][((), (l,))] += 1
        for s in range(2, n + 1):
            for ib in range(3, s - 2):
                for ia in range(1, s - ib - 1):
                    ic = s - 1 - ib - ia
                    if ic < 1: continue
                    for fb, mb in self.cntB[ib].items():
                        for fa, ma in self.cntA[ia].items():
                            for fc, mc in self.cntA[ic].items():
                                U = sorted(set(fb[0]) | set(fa[0]) | set(fc[0]))
                                tb, ta, tc = self._expand(fb, U), self._expand(fa, U), self._expand(fc, U)
                                self.cntA[s][self._reduce(U, [x if c else y for c, x, y in zip(tb, ta, tc)])] += mb * ma * mc

    # prior over canonical functions at size <= n ---------------------------
    def canon(self, n=None):
        n = self.n if n is None else n
        mu = defaultdict(float); cnt = defaultdict(int); size = {}
        for s in range(1, n + 1):
            if self.a[s] == 0: continue
            b = np.log2(self.a[s]) + 2 * np.log2(s) + 1
            for f, m in self.cntA[s].items():
                mu[f] += m * 2.0 ** (-b); cnt[f] += m; size[f] = min(size.get(f, 99), s)
        fs = sorted(mu, key=lambda f: (size[f], len(f[0]), f))
        return fs, np.array([mu[f] for f in fs]), np.array([cnt[f] for f in fs]), np.array([size[f] for f in fs])


def raw_counts(n, n_atoms):
    """a(s): number of programs of size s (no canonical reduction)."""
    aB = defaultdict(int); aA = defaultdict(int)
    aB[3] = n_atoms; aA[1] = 9
    for s in range(4, n + 1):
        aB[s] = aB[s - 1] + 2 * sum(aB[i] * aB[s - 1 - i] for i in range(3, s - 3))
    for s in range(2, n + 1):
        aA[s] = sum(aB[ib] * aA[ia] * aA[s - 1 - ib - ia] for ib in range(3, s - 2) for ia in range(1, s - ib - 1) if s - 1 - ib - ia >= 1)
    return [aA[s] for s in range(n + 1)]


class Slots:
    """Absolute per-slot arrays of the canonical functions fs (abstract)."""
    KMAX = 4

    def __init__(self, fs):
        self.fs = fs
        K = len(fs); self.K = K
        kmax = max(len(f[0]) for f in fs)
        assert kmax <= 2
        self.nat = np.zeros((3, K), np.int64)
        self.atL = np.zeros((3, K, 2), np.int64); self.atJ = np.zeros((3, K, 2), np.int64); self.atA = np.zeros((3, K, 2), np.int64)
        self.tab = np.zeros((3, K, 4), np.int64)
        self.index = [dict() for _ in range(3)]
        for s in range(3):
            for x, f in enumerate(fs):
                atoms, tab = f
                self.nat[s, x] = len(atoms)
                for t, (L, jr, al) in enumerate(atoms):
                    self.atL[s, x, t] = L; self.atJ[s, x, t] = others(s)[jr]; self.atA[s, x, t] = al
                for v, l in enumerate(tab):
                    self.tab[s, x, v] = l
                self.index[s][f] = x

    def src(self, s, x):
        atoms, tab = self.fs[x]
        if not atoms:
            return act_name(s, tab[0])
        if len(atoms) == 1:
            L, jr, al = atoms[0]; j = others(s)[jr]
            return 'if(BOX%s(%d=%s),%s,%s)' % ('1' if L else '', j + 1, act_name(j, al), act_name(s, tab[1]), act_name(s, tab[0]))
        return 'f%s:%s' % ([(L, others(s)[jr] + 1, act_name(others(s)[jr], al)) for L, jr, al in atoms], [act_name(s, l) for l in tab])

    def permute(self, sigma):
        """perm[s][x] = index in slot sigma[s] of the image of slot s's program x."""
        out = []
        for s in range(3):
            ts = sigma[s]
            m = np.empty(self.K, np.int64)
            for x, f in enumerate(self.fs):
                atoms, tab = f
                img_atoms = []
                for (L, jr, al) in atoms:
                    j = others(s)[jr]; tj = sigma[j]
                    p = partner_abs(j, al); tp = ALL if p == ALL else sigma[p]
                    img_atoms.append((L, others(ts).index(tj), local_of(tj, tp, al % 3)))
                img_tab = []
                for l in tab:
                    p = partner_abs(s, l); tp = ALL if p == ALL else sigma[p]
                    img_tab.append(local_of(ts, tp, l % 3))
                g = Lang._reduce(img_atoms, img_tab)
                m[x] = self.index[ts][g]
            out.append(m)
        return out


# ---------------------------------------------------------------- evaluators
VAC, BROKEN = -2, -1


@njit(cache=True)
def eval_modal(nat, atL, atJ, atA, tab, x0, x1, x2):
    """Stable actions of the encounter (x0, x1, x2) on the linear GL chain.
    hist[L, s]: VAC (no world in [L, n) yet), the action slot s played at every
    world in [L, n), or BROKEN."""
    xs = (x0, x1, x2)
    hist = np.full((2, 3), VAC, np.int64)
    val = np.zeros(3, np.int64)
    for n in range(64):
        for s in range(3):
            x = xs[s]; idx = 0
            for t in range(nat[s, x]):
                h = hist[atL[s, x, t], atJ[s, x, t]]
                if h == VAC or h == atA[s, x, t]:
                    idx |= 1 << t
            val[s] = tab[s, x, idx]
        changed = False
        for L in range(2):
            if n < L:
                continue
            for s in range(3):
                h = hist[L, s]
                if h == VAC:
                    hist[L, s] = val[s]; changed = True
                elif h >= 0 and h != val[s]:
                    hist[L, s] = BROKEN; changed = True
        if not changed and n >= 2:
            return val
    return -np.ones(3, np.int64)


@njit(cache=True)
def eval_weak(nat, atL, atJ, atA, tab, x0, x1, x2):
    """Least fixed point by budget iteration: an atom reading a bottom value is
    bottom; a slot still bottom at the fixed point diverges and plays
    NULL_LOCAL.  Left-to-right short-circuit for two atoms (atom 0 first)."""
    xs = (x0, x1, x2)
    val = -np.ones(3, np.int64)
    new = np.empty(3, np.int64)
    for it in range(16):
        for s in range(3):
            x = xs[s]; k = nat[s, x]
            if k == 0:
                new[s] = tab[s, x, 0]; continue
            idx = 0; bot = False
            for t in range(k):
                v = val[atJ[s, x, t]]
                if v < 0:
                    bot = True; break
                if v == atA[s, x, t]:
                    idx |= 1 << t
            new[s] = -1 if bot else tab[s, x, idx]
        same = True
        for s in range(3):
            if new[s] != val[s]:
                same = False
            val[s] = new[s]
        if same:
            break
    for s in range(3):
        if val[s] < 0:
            val[s] = 8
    return val


@njit(cache=True)
def encounter(arm, nat, atL, atJ, atA, tab, PARTNER, x0, x1, x2):
    if arm == 0:
        v = eval_modal(nat, atL, atJ, atA, tab, x0, x1, x2)
    else:
        v = eval_weak(nat, atL, atJ, atA, tab, x0, x1, x2)
    u, typ = outcome(PARTNER, v[0], v[1], v[2])
    return u, typ, v


@njit(cache=True)
def _modal_into(nat, atL, atJ, atA, tab, x0, x1, x2, hist, val):
    for L in range(2):
        for s in range(3):
            hist[L, s] = VAC
    for n in range(64):
        for s in range(3):
            x = x0 if s == 0 else (x1 if s == 1 else x2)
            idx = 0
            for t in range(nat[s, x]):
                h = hist[atL[s, x, t], atJ[s, x, t]]
                if h == VAC or h == atA[s, x, t]:
                    idx |= 1 << t
            val[s] = tab[s, x, idx]
        changed = False
        for L in range(2):
            if n < L:
                continue
            for s in range(3):
                h = hist[L, s]
                if h == VAC:
                    hist[L, s] = val[s]; changed = True
                elif h >= 0 and h != val[s]:
                    hist[L, s] = BROKEN; changed = True
        if not changed and n >= 2:
            return
    val[0] = -9


@njit(cache=True)
def _weak_into(nat, atL, atJ, atA, tab, x0, x1, x2, hist, val):
    for s in range(3):
        val[s] = -1
    for it in range(16):
        same = True
        for s in range(3):
            x = x0 if s == 0 else (x1 if s == 1 else x2)
            k = nat[s, x]
            if k == 0:
                nv = tab[s, x, 0]
            else:
                idx = 0; bot = False
                for t in range(k):
                    v = val[atJ[s, x, t]] if it > 0 else -1
                    if v < 0:
                        bot = True; break
                    if v == atA[s, x, t]:
                        idx |= 1 << t
                nv = -1 if bot else tab[s, x, idx]
            hist[0, s] = nv
        for s in range(3):
            if hist[0, s] != val[s]:
                same = False
            val[s] = hist[0, s]
        if same and it > 0:
            break
    for s in range(3):
        if val[s] < 0:
            val[s] = 8


@njit(cache=True)
def _outcome_into(PARTNER, val, u):
    a0, a1, a2 = val[0], val[1], val[2]
    u[0] = 0; u[1] = 0; u[2] = 0
    p0, p1, p2 = PARTNER[0, a0], PARTNER[1, a1], PARTNER[2, a2]
    d0, d1, d2 = 2 + a0 % 3, 2 + a1 % 3, 2 + a2 % 3
    if p0 == ALL and p1 == ALL and p2 == ALL:
        if d0 + d1 + d2 <= 6:
            u[0] = d0; u[1] = d1; u[2] = d2
            return 0
        return 4
    for s in range(3):
        ps = p0 if s == 0 else (p1 if s == 1 else p2)
        if ps == ALL or ps <= s:
            continue
        t = ps
        pt = p0 if t == 0 else (p1 if t == 1 else p2)
        if pt != s:
            continue
        ds = d0 if s == 0 else (d1 if s == 1 else d2)
        dt = d0 if t == 0 else (d1 if t == 1 else d2)
        if ds + dt <= 6:
            u[s] = ds; u[t] = dt
            if ds + dt < 6:
                return 3
            if ds == dt:
                return 1
            return 2
        return 4
    return 4


@njit(cache=True)
def enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, x0, x1, x2, hist, val, u):
    if arm == 0:
        _modal_into(nat, atL, atJ, atA, tab, x0, x1, x2, hist, val)
    else:
        _weak_into(nat, atL, atJ, atA, tab, x0, x1, x2, hist, val)
    return _outcome_into(PARTNER, val, u)


@njit(cache=True)
def slot_row(arm, nat, atL, atJ, atA, tab, PARTNER, s, y0, y1, y2):
    """For every program q of slot s placed into (y0, y1, y2): payoffs (3, in
    sixths) and outcome type."""
    K = nat.shape[1]
    U = np.empty((K, 3), np.int64); T = np.empty(K, np.int64)
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64); u = np.empty(3, np.int64)
    for q in range(K):
        if s == 0:
            typ = enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, q, y1, y2, hist, val, u)
        elif s == 1:
            typ = enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, y0, q, y2, hist, val, u)
        else:
            typ = enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, y0, y1, q, hist, val, u)
        U[q, 0] = u[0]; U[q, 1] = u[1]; U[q, 2] = u[2]; T[q] = typ
    return U, T


@njit(cache=True)
def class_hash(arm, nat, atL, atJ, atA, tab, PARTNER, s, lo, hi):
    """Signatures of slot-s programs lo..hi-1 over every opponent pair: columns
    0-1 hash the joint action vector, columns 2-3 the payoff triple (in
    sixths).  Payoff-equivalence is the chain's lumping relation (twopop.py
    merges by payoff rows and columns likewise)."""
    K = nat.shape[1]
    H = np.zeros((hi - lo, 4), np.uint64)
    M1 = np.uint64(0x9E3779B97F4A7C15); M2 = np.uint64(0xC2B2AE3D27D4EB4F)
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64); u = np.empty(3, np.int64)
    for qi in range(hi - lo):
        q = lo + qi
        h1 = np.uint64(1469598103934665603); h2 = np.uint64(7)
        g1 = np.uint64(1469598103934665603); g2 = np.uint64(7)
        for a in range(K):
            for b in range(K):
                if s == 0:
                    enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, q, a, b, hist, val, u)
                elif s == 1:
                    enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, a, q, b, hist, val, u)
                else:
                    enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, a, b, q, hist, val, u)
                code = np.uint64(val[0] * 81 + val[1] * 9 + val[2] + 1)
                h1 = (h1 ^ code) * M1
                h2 = (h2 + code * np.uint64(a * K + b + 1)) * M2
                pc = np.uint64(u[0] * 25 + u[1] * 5 + u[2] + 1)
                g1 = (g1 ^ pc) * M1
                g2 = (g2 + pc * np.uint64(a * K + b + 1)) * M2
        H[qi, 0] = h1; H[qi, 1] = h2; H[qi, 2] = g1; H[qi, 3] = g2
    return H


def build(arm, n, levels=None):
    """arm 'modal' (PA and PA + Con(PA) boxes), 'modalPA' (PA box only: the
    grammar of the weak arm, as M0 in the E1 matched control) or 'weak'."""
    if levels is None:
        levels = (0, 1) if arm == 'modal' else (0,)
    L = Lang(n, levels)
    fs, mu, cnt, size = L.canon()
    S = Slots(fs)
    return L, S, mu / mu.sum(), cnt, size


def arrays(S):
    return S.nat, S.atL, S.atJ, S.atA, S.tab, PARTNER


ARM = {'modal': 0, 'modalPA': 0, 'weak': 1}
