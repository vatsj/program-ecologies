"""The union game (specs/2026-10-05-union.md): a boss B and two workers W1, W2,
three separate slot populations, fixed roles.

Game.  Each worker works (0) or strikes (1); a working worker produces 1.  The
boss picks a wage s in {0, 1/4, 1/2} paid to each working worker and a whack
policy: whack strikers ('strike', strike targeting), whack nobody ('none'), or
whack by source ('source', source targeting: whack every worker whose program
carries the union tag, working or not).  A whacked worker loses L = 1; the boss
pays c per whack.  Payoffs: a working worker s (- L if whacked), a striker 0
(- L if whacked), the boss sum over working workers of (1 - s), minus c per
whack.  Boss action index b = 3 * si + hi (si wage index, hi whack index).
Joint action code j = 4 b + 2 a1 + a2 (36 codes).

Grammar (one per role; absolute slot labels are filled in per slot):

    A ::= a | if(B, A, A)
    B ::= BOX_L(P) | not B | and B B | or B B          (an atom is 3 nodes)

Every atom is a box of a proposition P about the joint action of the current
encounter, evaluated on the linear GL Kripke chain (modal.py semantics): at world
n, BOX_L(P) holds iff P held at every world m with L <= m < n.  Atoms:
  workers  BOX(s in S)  for the 6 nonempty proper subsets S of the wages,
           BOX(h in H)  for the 6 nonempty proper subsets H of the whack policies,
           BOX(OTHER = work), BOX(OTHER = strike)   (the other worker of the encounter),
           QUORUM = BOX(s < 1/2 -> OTHER = strike)   (spec: "the other worker in this
                    encounter provably strikes whenever s < 1/2"; encounter-level, read
                    from the other worker's source exactly as FairBot reads its opponent);
  boss     BOX(W_j = work), BOX(W_j = strike), j = 1, 2.
Programs are merged into canonical functions (essential atoms, action table) as
in dollar3.py; the prior is the length prior bits = log2 a(|p|) + 2 log2 |p| + 1
per role, the mass of a canonical function the sum over its spellings.

Union tag (what source targeting reads): QUORUM is an essential atom of the
canonical function.  A spelling whose QUORUM clause is dead is the function
without it and carries no tag.
"""
import os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from abm import njit
from dollar3 import Lang as _L3

WAGES = np.array([0.0, 0.25, 0.5])
WNAME = ['0', '1/4', '1/2']
HNAME = ['strike', 'none', 'source']
LOW = (0, 1)                      # wage indices with s < 1/2
NB, NW = 9, 2                     # boss and worker action counts


def bact(si, hi):
    return 3 * si + hi


def bname(b):
    return '(%s,%s)' % (WNAME[b // 3], HNAME[b % 3])


def subset_name(mask, names):
    return '{' + ','.join(names[i] for i in range(3) if (mask >> i) & 1) + '}'


# ---------------------------------------------------------------- propositions
# absolute propositions, truth tables over the 36 joint codes
def _joint():
    for b in range(NB):
        for a1 in range(2):
            for a2 in range(2):
                yield 4 * b + 2 * a1 + a2, b, a1, a2


PROPS = []        # (name, owner, fn(b, a1, a2))
for m in range(1, 7):
    PROPS.append(('s in %s' % subset_name(m, WNAME), None, (lambda m: lambda b, a1, a2: bool((m >> (b // 3)) & 1))(m)))
for m in range(1, 7):
    PROPS.append(('h in %s' % subset_name(m, HNAME), None, (lambda m: lambda b, a1, a2: bool((m >> (b % 3)) & 1))(m)))
PROPS.append(('W1=work', None, lambda b, a1, a2: a1 == 0))
PROPS.append(('W1=strike', None, lambda b, a1, a2: a1 == 1))
PROPS.append(('W2=work', None, lambda b, a1, a2: a2 == 0))
PROPS.append(('W2=strike', None, lambda b, a1, a2: a2 == 1))
PROPS.append(('QUORUM(W1: s<1/2 -> W2=strike)', 1, lambda b, a1, a2: (b // 3) not in LOW or a2 == 1))
PROPS.append(('QUORUM(W2: s<1/2 -> W1=strike)', 2, lambda b, a1, a2: (b // 3) not in LOW or a1 == 1))
NPROP = len(PROPS)
TT = np.zeros((NPROP, 36), np.bool_)
for p, (_, _, fn) in enumerate(PROPS):
    for j, b, a1, a2 in _joint():
        TT[p, j] = fn(b, a1, a2)
P_W = {(1, 0): 12, (1, 1): 13, (2, 0): 14, (2, 1): 15}     # (slot, action) -> prop
P_Q = {1: 16, 2: 17}

# abstract worker atom kinds: 0..5 wage masks 1..6, 6..11 whack masks 1..6, 12 OTHER=work, 13 OTHER=strike, 14 QUORUM
WK_NAMES = (['s in %s' % subset_name(m, WNAME) for m in range(1, 7)] + ['h in %s' % subset_name(m, HNAME) for m in range(1, 7)]
            + ['OTHER=work', 'OTHER=strike', 'QUORUM'])
QK = 14
BK_NAMES = ['W1=work', 'W1=strike', 'W2=work', 'W2=strike']


def worker_prop(slot, k):
    """absolute prop index of abstract worker atom kind k owned by worker `slot` (1 or 2)."""
    other = 3 - slot
    if k < 12:
        return k
    if k == 12:
        return P_W[(other, 0)]
    if k == 13:
        return P_W[(other, 1)]
    return P_Q[slot]


def boss_prop(k):
    return 12 + k


# ---------------------------------------------------------------- language
class RoleLang:
    """Canonical enumeration with a syntactic QUORUM flag.  atoms: abstract
    labels (L, k); nact: action count; qkinds: atom kinds that are QUORUM.
    cntA[s][(f, q)]: number of programs of size s with canonical function f and
    q = 1 iff some QUORUM atom occurs in the spelling."""

    def __init__(self, n, atoms, nact, qkinds=()):
        self.n, self.atoms, self.nact = n, list(atoms), nact
        self.qkinds = set(qkinds)
        self.cntB = [defaultdict(int) for _ in range(n + 1)]
        self.cntA = [defaultdict(int) for _ in range(n + 1)]
        R, E = _L3._reduce, _L3._expand
        for a in self.atoms:
            if n >= 3:
                self.cntB[3][(((a,), (0, 1)), int(a[1] in self.qkinds))] += 1
        for s in range(4, n + 1):
            for (f, q), m in self.cntB[s - 1].items():
                self.cntB[s][(R(f[0], tuple(1 - v for v in f[1])), q)] += m
            for i in range(3, s - 3):
                j = s - 1 - i
                for (fa, qa), ma in self.cntB[i].items():
                    for (fb, qb), mb in self.cntB[j].items():
                        U = sorted(set(fa[0]) | set(fb[0]))
                        ta, tb = E(fa, U), E(fb, U)
                        q = qa | qb
                        self.cntB[s][(R(U, [x & y for x, y in zip(ta, tb)]), q)] += ma * mb
                        self.cntB[s][(R(U, [x | y for x, y in zip(ta, tb)]), q)] += ma * mb
        for l in range(nact):
            self.cntA[1][(((), (l,)), 0)] += 1
        for s in range(2, n + 1):
            for ib in range(3, s - 2):
                for ia in range(1, s - ib - 1):
                    ic = s - 1 - ib - ia
                    if ic < 1:
                        continue
                    for (fb, qb), mb in self.cntB[ib].items():
                        for (fa, qa), ma in self.cntA[ia].items():
                            for (fc, qc), mc in self.cntA[ic].items():
                                U = sorted(set(fb[0]) | set(fa[0]) | set(fc[0]))
                                tb, ta, tc = E(fb, U), E(fa, U), E(fc, U)
                                key = (R(U, [x if c else y for c, x, y in zip(tb, ta, tc)]), qb | qa | qc)
                                self.cntA[s][key] += mb * ma * mc
        self.a = np.array([0] + [sum(self.cntA[s].values()) for s in range(1, n + 1)], float)

    def canon(self, noQ=False):
        """Canonical functions with raw (unnormalized) mass.  noQ: drop every
        spelling that contains QUORUM (the matched no-QUORUM arm: same weight per
        spelling, a(s) from the full grammar)."""
        mu = defaultdict(float); cnt = defaultdict(int); size = {}
        for s in range(1, self.n + 1):
            if self.a[s] == 0:
                continue
            b = np.log2(self.a[s]) + 2 * np.log2(s) + 1
            for (f, q), m in self.cntA[s].items():
                if noQ and q:
                    continue
                mu[f] += m * 2.0 ** (-b); cnt[f] += m; size[f] = min(size.get(f, 99), s)
        fs = sorted(mu, key=lambda f: (size[f], len(f[0]), f))
        return fs, np.array([mu[f] for f in fs]), np.array([cnt[f] for f in fs]), np.array([size[f] for f in fs])


def worker_atoms(levels, quorum=True):
    return [(L, k) for L in levels for k in range(15) if quorum or k != QK]


def boss_atoms(levels):
    return [(L, k) for L in levels for k in range(4)]


# ---------------------------------------------------------------- program arrays
class Programs:
    """Per-slot arrays.  Slot 0 = boss over boss functions fb; slots 1, 2 =
    workers over worker functions fw (the same abstract list; atoms
    instantiated per slot).  atP: absolute prop, atL: level, tab: action table
    over 2^k valuations (bit t = atom t true)."""

    def __init__(self, fb, fw):
        self.fb, self.fw = fb, fw
        K = max(len(fb), len(fw))
        kmax = max(max(len(f[0]) for f in fb), max(len(f[0]) for f in fw))
        assert kmax <= 3
        self.KB, self.KW = len(fb), len(fw)
        self.nat = np.zeros((3, K), np.int64)
        self.atP = np.zeros((3, K, 3), np.int64); self.atL = np.zeros((3, K, 3), np.int64)
        self.tab = np.zeros((3, K, 8), np.int64)
        for x, (atoms, tab) in enumerate(fb):
            self.nat[0, x] = len(atoms)
            for t, (L, k) in enumerate(atoms):
                self.atP[0, x, t] = boss_prop(k); self.atL[0, x, t] = L
            self.tab[0, x, :len(tab)] = tab
        for s in (1, 2):
            for x, (atoms, tab) in enumerate(fw):
                self.nat[s, x] = len(atoms)
                for t, (L, k) in enumerate(atoms):
                    self.atP[s, x, t] = worker_prop(s, k); self.atL[s, x, t] = L
                self.tab[s, x, :len(tab)] = tab
        self.tag = np.array([any(k == QK for (L, k) in f[0]) for f in fw], np.bool_)
        self.index_w = {f: i for i, f in enumerate(fw)}
        self.index_b = {f: i for i, f in enumerate(fb)}

    def arrays(self):
        return self.nat, self.atP, self.atL, self.tab

    def src_w(self, x):
        atoms, tab = self.fw[x]
        an = lambda a: ('BOX%s(%s)' % ('1' if a[0] else '', WK_NAMES[a[1]]))
        act = ['work', 'strike']
        if not atoms:
            return act[tab[0]]
        if len(atoms) == 1:
            return 'if(%s,%s,%s)' % (an(atoms[0]), act[tab[1]], act[tab[0]])
        return 'f[%s]:%s' % (','.join(an(a) for a in atoms), ''.join('WS'[v] for v in tab))

    def src_b(self, x):
        atoms, tab = self.fb[x]
        an = lambda a: ('BOX%s(%s)' % ('1' if a[0] else '', BK_NAMES[a[1]]))
        if not atoms:
            return bname(tab[0])
        if len(atoms) == 1:
            return 'if(%s,%s,%s)' % (an(atoms[0]), bname(tab[1]), bname(tab[0]))
        return 'f[%s]:%s' % (','.join(an(a) for a in atoms), ','.join(bname(v) for v in tab))


# ---------------------------------------------------------------- evaluator
@njit(cache=True)
def encounter(nat, atP, atL, tab, TT, xb, x1, x2, flag):
    """Stable joint action code of the encounter (xb, x1, x2) on the linear GL
    chain.  flag[L, p]: P_p held at every world in [L, n) (True while vacuous).
    Box truth is monotone non-increasing in n, so the play stabilizes."""
    xs = (xb, x1, x2)
    for t in range(flag.shape[1]):
        flag[0, t] = True; flag[1, t] = True
    val = np.zeros(3, np.int64)
    for n in range(64):
        for s in range(3):
            x = xs[s]; idx = 0
            for t in range(nat[s, x]):
                if flag[atL[s, x, t], atP[s, x, t]]:
                    idx |= 1 << t
            val[s] = tab[s, x, idx]
        j = 4 * val[0] + 2 * val[1] + val[2]
        changed = False
        for s in range(3):
            x = xs[s]
            for t in range(nat[s, x]):
                L = atL[s, x, t]; p = atP[s, x, t]
                if n >= L and flag[L, p] and not TT[p, j]:
                    flag[L, p] = False; changed = True
        if not changed and n >= 2:
            return j
    return -1


@njit(cache=True)
def tensor(nat, atP, atL, tab, TT, KB, KW):
    """J[b, x, y]: joint code with boss b, W1 = x, W2 = y."""
    J = np.empty((KB, KW, KW), np.int8)
    flag = np.ones((2, TT.shape[0]), np.bool_)
    for b in range(KB):
        for x in range(KW):
            for y in range(KW):
                J[b, x, y] = encounter(nat, atP, atL, tab, TT, b, x, y, flag)
    return J


def payoff_table(c, Lw=1.0):
    """PAY[j, t1, t2] = (u_B, u_1, u_2) for joint code j and union tags t1, t2."""
    PAY = np.zeros((36, 2, 2, 3))
    for j in range(36):
        b, a1, a2 = j // 4, (j // 2) % 2, j % 2
        s = WAGES[b // 3]; h = b % 3
        for t1 in range(2):
            for t2 in range(2):
                uB = 0.0; u = [0.0, 0.0]
                for w, (a, tg) in enumerate(((a1, t1), (a2, t2))):
                    whacked = (h == 0 and a == 1) or (h == 2 and tg == 1)
                    if a == 0:
                        u[w] += s; uB += 1 - s
                    if whacked:
                        u[w] -= Lw; uB -= c
                PAY[j, t1, t2] = (uB, u[0], u[1])
    return PAY


def joint_name(j):
    b, a1, a2 = j // 4, (j // 2) % 2, j % 2
    return '%s %s %s' % (bname(b), 'WS'[a1], 'WS'[a2])


# ---------------------------------------------------------------- summaries
SUMM = ['fair', 'intermediate', 'zero wage', 'strike', 'scab split', 'repression:strike', 'repression:source']


def summary(j, t1, t2):
    """Disjoint outcome summary of joint code j with tags t1, t2 (realized
    whacking first, by type; then the work pattern; then the wage)."""
    b, a1, a2 = j // 4, (j // 2) % 2, j % 2
    h = b % 3
    if h == 0 and (a1 or a2):
        return 5
    if h == 2 and (t1 or t2):
        return 6
    if a1 and a2:
        return 3
    if a1 or a2:
        return 4
    return 2 - (b // 3)          # wage index 2 -> fair (0), 1 -> intermediate (1), 0 -> zero wage (2)


# ---------------------------------------------------------------- build
def build(nB=6, nW=10, levels=(0,), arm='quorum'):
    """arm: 'quorum' (full worker grammar), 'noquorum' (matched: QUORUM spellings
    removed, same per-spelling weights), 'blind' (workers read only the boss:
    no OTHER and no QUORUM atoms; same per-spelling weights as 'quorum')."""
    LB = RoleLang(nB, boss_atoms(levels), NB)
    fb, mb, cb, sb = LB.canon()
    LW = RoleLang(nW, worker_atoms(levels), NW, qkinds=(QK,))
    fw, mw, cw, sw = LW.canon(noQ=(arm != 'quorum'))
    if arm == 'blind':
        keep = [i for i, f in enumerate(fw) if not any(k >= 12 for (L, k) in f[0])]
        fw, mw, cw, sw = [fw[i] for i in keep], mw[keep], cw[keep], sw[keep]
    P = Programs(fb, fw)
    return dict(LB=LB, LW=LW, P=P, mb=mb, mw=mw, cb=cb, cw=cw, sb=sb, sw=sw)


def named(P):
    """Indices of the named worker programs (abstract functions)."""
    LOWMASK = 0b011           # {0, 1/4} -> wage-mask kind index 2 (masks 1..6 -> kinds 0..5)
    kl = LOWMASK - 1
    out = {}
    out['scab'] = P.index_w.get(((), (0,)))
    out['always strike'] = P.index_w.get(((), (1,)))
    out['militant'] = P.index_w.get((((0, kl),), (0, 1)))
    # union: strike iff BOX(s<1/2) and QUORUM; atoms sorted (0, 1) < (0, 14)
    out['union'] = P.index_w.get((((0, kl), (0, QK)), (0, 0, 0, 1)))
    out["union' (BOX(OTHER=strike))"] = P.index_w.get((((0, kl), (0, 13)), (0, 0, 0, 1)))
    return out


def named_boss(P):
    return {bname(b): P.index_b.get(((), (b,))) for b in range(NB)}


# ---------------------------------------------------------------- behavioural classes
def _keys(arr2d_iter):
    return [a.tobytes() for a in arr2d_iter]


def classes(d, J=None):
    """Behavioural classes (exact lumping): worker x ~ x' iff same tag and
    J[b, x, y] == J[b, x', y] for every boss b and other worker y (by the W1/W2
    symmetry, checked in tests, this covers slot W2); boss b ~ b' iff
    J[b] == J[b'].  Returns class ids, representatives (most massive member),
    class masses (normalized), and the class-level tensor."""
    P = d['P']
    if J is None:
        J = tensor(*P.arrays(), TT, P.KB, P.KW)
    assert (J >= 0).all(), 'unstable encounter'
    kw = {}
    cw = np.empty(P.KW, np.int64)
    for x in range(P.KW):
        key = (bool(P.tag[x]), J[:, x, :].tobytes())
        cw[x] = kw.setdefault(key, len(kw))
    kb = {}
    cb = np.empty(P.KB, np.int64)
    for b in range(P.KB):
        cb[b] = kb.setdefault(J[b].tobytes(), len(kb))
    mw = d['mw'] / d['mw'].sum(); mb = d['mb'] / d['mb'].sum()
    KcW, KcB = len(kw), len(kb)
    massW = np.bincount(cw, weights=mw, minlength=KcW); massB = np.bincount(cb, weights=mb, minlength=KcB)
    repW = np.full(KcW, -1, np.int64); repB = np.full(KcB, -1, np.int64)
    for x in np.argsort(-mw, kind='stable'):
        if repW[cw[x]] < 0: repW[cw[x]] = x
    for b in np.argsort(-mb, kind='stable'):
        if repB[cb[b]] < 0: repB[cb[b]] = b
    Jc = J[repB][:, repW][:, :, repW]
    tagc = P.tag[repW].astype(np.int64)
    return dict(J=J, cw=cw, cb=cb, KcW=KcW, KcB=KcB, massW=massW, massB=massB, repW=repW, repB=repB, Jc=np.ascontiguousarray(Jc), tagc=tagc)
