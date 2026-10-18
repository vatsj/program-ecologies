"""Hooks, Part W: the social organization (union) game with hooks (notes/hooks-w.md §1.2-§1.10, §2.6).

The union game's grammar, payoff table and GL semantics (src/union.py; CC, c = 0.5, L = 1; boss n = 6, workers
n = 10, level 0) with hook leaves HOOK(t, a0) (t in {0, 1}, a0 a role action) as one-node leaves.  A match is
evaluated on the closure of slot substitutions (27 nodes: each slot actual, its role's C constant or its D
constant); behaviour keys (partner position, beta) read the partner's favourable play in E[h := C], E[h := D] and
E, by boxes.  Fills resolve with the conflict rule of hooks_w (behaviour > history > role > none, ties by recency).
The island kernel is sog_lottery's law (three slot populations per island, parent proportional to count *
exp(w f), f the expected payoff against a uniform draw of the other two slots, migration per slot) over types
(role, base, lineage, fills), with one sampled encounter (one member per slot) after every birth event on that
island.  Imports src/union.py unchanged.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
from numba import njit, types
from numba.typed import Dict
import union as U

NACT = np.array([9, 2, 2], np.int64)          # actions per slot
CACT = np.array([U.bact(2, 1), 0, 0], np.int64)   # the role's C constant: (1/2, none), work
DACT = np.array([U.bact(0, 1), 1, 1], np.int64)   # the role's D constant: (0, none), strike
NONE, ROLE, HIST, BEH = 0, 1, 2, 3
SEEDED, WRITTEN, COPIED, CONTRACT = 0, 1, 2, 3
SCOPES = ('none', 'role', 'history', 'behaviour')
ORIGINS = ('seeded', 'written', 'copied', 'contract')
POISSON = np.array([np.exp(-1) / f for f in (1, 1, 2, 6, 24)]); POISSON /= POISSON.sum()
RSZ = 512                                      # resolution table: ctx(4) x beta0(8) x beta1(8) x tag(2)


# ------------------------------------------------------------------ language
class SogLang:
    """Canonical boss and worker functions of the union grammar, with hook leaves (hooks=True) or without.
    Leaf l < nact is action l; l >= nact is HOOK(t, a0) with h = l - nact, t = h // nact, a0 = h % nact."""

    def __init__(self, hooks=True, nB=6, nW=10):
        k = 3 if hooks else 1
        LB = U.RoleLang(nB, U.boss_atoms((0,)), 9 * k)
        fb, mb, cb, sb = LB.canon()
        LW = U.RoleLang(nW, U.worker_atoms((0,)), 2 * k, qkinds=(U.QK,))
        fw, mw, cw, sw = LW.canon()
        self.LB, self.LW = LB, LW
        self.fb, self.fw = fb, fw
        self.muB = mb / mb.sum(); self.muW = mw / mw.sum()
        P = U.Programs(fb, fw)
        self.P = P
        self.nat, self.atP, self.atL, self.tab = P.arrays()
        self.wtag = P.tag.astype(np.int64)
        K = self.nat.shape[1]
        self.htags = np.zeros((2, K), np.int64)     # hook tags carried, role 0 boss / 1 worker
        for x, (atoms, tab) in enumerate(fb):
            for l in tab:
                if l >= 9:
                    self.htags[0, x] |= 1 << ((l - 9) // 9)
        for x, (atoms, tab) in enumerate(fw):
            for l in tab:
                if l >= 2:
                    self.htags[1, x] |= 1 << ((l - 2) // 2)
        self.KB, self.KW = len(fb), len(fw)

    def src(self, role, x):
        f = (self.fb if role == 0 else self.fw)[x]
        nact = 9 if role == 0 else 2
        def leaf(l):
            if l < nact:
                return U.bname(l) if role == 0 else ['work', 'strike'][l]
            h = l - nact
            return 'HOOK(%d,%s)' % (h // nact, U.bname(h % nact) if role == 0 else ['work', 'strike'][h % nact])
        atoms, tab = f
        if not atoms:
            return leaf(tab[0])
        nm = U.BK_NAMES if role == 0 else U.WK_NAMES
        an = ['BOX(%s)' % nm[a[1]] for a in atoms]
        if len(atoms) == 1:
            return 'if(%s,%s,%s)' % (an[0], leaf(tab[1]), leaf(tab[0]))
        return 'f[%s]:%s' % (','.join(an), ','.join(leaf(v) for v in tab))

    def arrays(self):
        return self.nat, self.atP, self.atL, self.tab


def fcode(action, tag, scope, origin, key):
    return 1 + (action | (tag << 4) | (scope << 5) | (origin << 7) | (key << 9))


@njit(cache=True)
def g_action(f): return (f - 1) & 15
@njit(cache=True)
def g_tag(f): return ((f - 1) >> 4) & 1
@njit(cache=True)
def g_scope(f): return ((f - 1) >> 5) & 3
@njit(cache=True)
def g_origin(f): return ((f - 1) >> 7) & 3
@njit(cache=True)
def g_key(f): return (f - 1) >> 9


def is_threat(slot, action):
    """A threat fill: a worker's strike, a boss's whack policy (strike or source targeting)."""
    return action == 1 if slot > 0 else (action % 3) in (0, 2)


# ------------------------------------------------------------------ resolution tables
@njit(cache=True)
def resolve(fills, nf, tags, slot, active, recency, l0, l1, R):
    """R[ctx*128 + b0*16 + b1*2 + t] <- the action of the fill selected for tag t (or -1), for a holder in `slot` whose
    partners (in the fixed order: boss -> W1, W2; worker -> boss, other worker) have lineages l0, l1 (-1 = none) and
    are actual in the node iff the ctx bits are set."""
    for ctx in range(4):
        la = l0 if (ctx & 1) else -1
        lb = l1 if (ctx & 2) else -1
        for b0 in range(8):
            for b1 in range(8):
                for t in range(2):
                    best = -1; bestp = -1
                    if (tags >> t) & 1:
                        for j in range(nf - 1, -1, -1):
                            f = fills[j]
                            if g_tag(f) != t:
                                continue
                            sc = g_scope(f)
                            if not active[sc, g_origin(f)]:
                                continue
                            k = g_key(f)
                            if sc == 0:
                                ok = True
                            elif sc == 1:
                                ok = k == slot
                            elif sc == 2:
                                ok = (la >= 0 and k == la) or (lb >= 0 and k == lb)
                            else:
                                ok = (k // 8 == 0 and k % 8 == b0) or (k // 8 == 1 and k % 8 == b1)
                            if not ok:
                                continue
                            if recency == 1:
                                best = j; break
                            pr = sc if sc < 2 else (2 if sc == 2 else 3)
                            if pr > bestp:
                                bestp = pr; best = j
                    R[ctx * 128 + b0 * 16 + b1 * 2 + t] = g_action(fills[best]) if best >= 0 else -1


@njit(cache=True)
def rhash(R):
    h = np.int64(-3750763034362895579)
    for i in range(R.shape[0]):
        h = (h ^ (R[i] + 2)) * np.int64(1099511628211)
    return h


# ------------------------------------------------------------------ the evaluator (27-node substitution closure)
@njit(cache=True)
def _fav(q, h, j, t1, t2):
    """Is slot q's play favourable to slot h at joint code j (worker tags t1, t2)?"""
    b = j // 4; a1 = (j // 2) % 2; a2 = j % 2
    if q > 0:
        return (a1 if q == 1 else a2) == 0
    s_i = b // 3; hh = b % 3
    aj = a1 if h == 1 else a2
    tj = t1 if h == 1 else t2
    wh = (hh == 0 and aj == 1) or (hh == 2 and tj == 1)
    if wh:
        return False
    return aj == 1 or s_i >= 1


@njit(cache=True)
def _hooked(tab, s, x, nleaf):
    """Does program x of slot s have a hook leaf in its table?"""
    nact = 9 if s == 0 else 2
    for i in range(nleaf):
        if tab[s, x, i] >= nact:
            return True
    return False


@njit(cache=True)
def eval_triple(nat, atP, atL, tab, TT, x0, x1, x2, tg1, tg2, R):
    """Joint code at the actual node (bits 0-5); per slot s, bits 6 + 3 s: hook leaf reached on path, its tag, a fill
    applied; per slot s, bits 15 + 6 s: the classes (beta0, beta1) of its two partners at the actual node.
    R: (3, RSZ) resolution tables of the three actual programs.  Only the nodes reachable from the actual encounter
    through hooked holders' substitutions are evaluated (the others are never read)."""
    NP = TT.shape[0]
    xs = (x0, x1, x2)
    hk = np.zeros(3, np.bool_)
    for s in range(3):
        hk[s] = _hooked(tab, s, xs[s], 1 << nat[s, xs[s]])
    need = np.zeros(27, np.bool_)
    need[0] = True
    order = np.zeros(27, np.int64); nn = 1
    q = 0
    while q < nn:
        e = order[q]; q += 1
        for s in range(3):
            ms = 9 if s == 0 else (3 if s == 1 else 1)
            sg = (e // ms) % 3
            if sg == 0 and hk[s]:
                for d in (1, 2):
                    e2 = e + d * ms
                    if not need[e2]:
                        need[e2] = True; order[nn] = e2; nn += 1
    fl = np.ones((27, 2, NP), np.bool_)
    ff = np.ones((27, 3, 3), np.bool_)
    jn = np.zeros(27, np.int64)
    act = np.zeros(3, np.int64)
    info = 0
    for n in range(80):
        for qq in range(nn):
            e = order[qq]
            sg0 = e // 9; sg1 = (e // 3) % 3; sg2 = e % 3
            for s in range(3):
                sg = sg0 if s == 0 else (sg1 if s == 1 else sg2)
                if sg == 1:
                    act[s] = 7 if s == 0 else 0
                    continue
                if sg == 2:
                    act[s] = 1
                    continue
                x = xs[s]
                idx = 0
                for t in range(nat[s, x]):
                    if fl[e, atL[s, x, t], atP[s, x, t]]:
                        idx |= 1 << t
                leaf = tab[s, x, idx]
                nact = 9 if s == 0 else 2
                if leaf < nact:
                    act[s] = leaf
                    if e == 0:
                        info &= ~(7 << (6 + 3 * s))
                    continue
                hh = leaf - nact; tg = hh // nact; a0 = hh % nact
                p0 = 1 if s == 0 else 0
                p1 = 2 if s == 0 else (2 if s == 1 else 1)
                ms = 9 if s == 0 else (3 if s == 1 else 1)
                e1 = e + ms
                e2 = e + 2 * ms
                b0 = (1 if ff[e1, s, p0] else 0) | ((1 if ff[e2, s, p0] else 0) << 1) | ((1 if ff[e, s, p0] else 0) << 2)
                b1 = (1 if ff[e1, s, p1] else 0) | ((1 if ff[e2, s, p1] else 0) << 1) | ((1 if ff[e, s, p1] else 0) << 2)
                sp0 = sg0 if p0 == 0 else (sg1 if p0 == 1 else sg2)
                sp1 = sg0 if p1 == 0 else (sg1 if p1 == 1 else sg2)
                ctx = (1 if sp0 == 0 else 0) | ((1 if sp1 == 0 else 0) << 1)
                r = R[s, ctx * 128 + b0 * 16 + b1 * 2 + tg]
                act[s] = r if r >= 0 else a0
                if e == 0:
                    info &= ~(7 << (6 + 3 * s))
                    info |= (1 | (tg << 1) | ((1 if r >= 0 else 0) << 2)) << (6 + 3 * s)
            jn[e] = 4 * act[0] + 2 * act[1] + act[2]
        changed = False
        for qq in range(nn):
            e = order[qq]
            j = jn[e]
            for L in range(2):
                if n < L:
                    continue
                for p in range(NP):
                    if fl[e, L, p] and not TT[p, j]:
                        fl[e, L, p] = False; changed = True
            sg1 = (e // 3) % 3; sg2 = e % 3
            t1 = tg1 if sg1 == 0 else 0
            t2 = tg2 if sg2 == 0 else 0
            for h in range(3):
                for q2 in range(3):
                    if q2 == h:
                        continue
                    if ff[e, h, q2] and not _fav(q2, h, j, t1, t2):
                        ff[e, h, q2] = False; changed = True
        if not changed and n >= 2:
            out = np.int64(jn[0] | info)
            for s in range(3):
                if not hk[s]:
                    continue
                ms = 9 if s == 0 else (3 if s == 1 else 1)
                p0 = 1 if s == 0 else 0
                p1 = 2 if s == 0 else (2 if s == 1 else 1)
                b0 = (1 if ff[ms, s, p0] else 0) | ((1 if ff[2 * ms, s, p0] else 0) << 1) | ((1 if ff[0, s, p0] else 0) << 2)
                b1 = (1 if ff[ms, s, p1] else 0) | ((1 if ff[2 * ms, s, p1] else 0) << 1) | ((1 if ff[0, s, p1] else 0) << 2)
                out |= np.int64(b0 | (b1 << 3)) << (15 + 6 * s)
            return out
    return -1
