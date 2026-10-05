"""The closed club (specs/2026-10-04-club.md): the modal arm plus one atom CLUB(THEM),
true iff the opponent's program is in the club K.  CLUB is a *global semantic oracle*
over the finite universe L_n, not a proof procedure: this arm is an oracle benchmark.

Grammar: the modal arm's (boxes BOX/BOXD at PA and PA + Con), plus

    A ::= ... | CLUB(THEM)          (3 nodes, like BOX(THEM(ME)))

CLUB(THEM) may occur anywhere an atom may, including under `not` and inside a box
argument THEM(^A) (there it is evaluated by A about A's opponent).  The control
grammar 'pos' admits a program only if every CLUB occurrence is under an even number
of `not`s and outside every box argument (syntactic polarity, tracked in the DP).

The joint operator.  For a candidate set K of program IDs, P_K is the play table with
CLUB(y) := [y in K] (CLUB atoms are world-independent; boxes resolve by the GL
Kripke chain as in modal.py).  F(K) = {x : x plays C against itself under P_K, and
under P_K x plays C against no program outside K}.  A club is a fixed point K = F(K).

Program IDs.  Membership is solved over canonical boolean functions of atoms (the
finest unit the DP keeps): two programs with the same canonical function over the same
atoms play identically against everything for every K (the CLUB atom reads only the
opponent's ID, and the usual induction on worlds goes through), so this is the
syntactic level of the arm.  Behavioural classes are formed only after K is solved.
"""
import os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
import modal as M
from modal import TM, TT, TL, KC, KD, ModalLanguage, ModalProvider, PD

KCLUB = 2                     # atom kind: club membership of the opponent
FCLUB = 3                     # form slot for the CLUB atom (no application)
P_NONE, P_POS, P_NEG, P_MIX = 0, 1, 2, 3      # polarity of CLUB occurrences


def _pol_not(p):
    return {P_POS: P_NEG, P_NEG: P_POS}.get(p, p)


def _pol_join(a, b):
    if a == P_NONE: return b
    if b == P_NONE: return a
    return a if a == b else P_MIX


class ClubLanguage(ModalLanguage):
    def __init__(self, n, kinds=((0, 0), (1, 0), (0, 1), (1, 1)), club=True, mode='full'):
        """club: include the CLUB atom.  mode: 'full' or 'pos' (CLUB only positively, top level)."""
        self.club = club; self.mode = mode
        super().__init__(n, kinds)

    def op(self, name, a=None, b=None):
        if name == 'club':
            key = ('club', None, None)
            if key in self._memo: return self._memo[key]
            at = (KCLUB, 0, FCLUB, -1)
            aid = self.atom_id.get(at)
            if aid is None:
                aid = len(self.atoms); self.atom_id[at] = aid; self.atoms.append(at)
            c = self._canon((aid,), 2)
            self._memo[key] = c
            return c
        return super().op(name, a, b)

    def _enumerate(self):
        n = self.n
        pos = self.mode == 'pos'
        cnt = [defaultdict(int) for _ in range(n + 1)]      # size -> (canon, polarity) -> count
        for name in ('C', 'D'):
            c = self.op(name); cnt[1][(c, P_NONE)] += 1; self._note(c, 1, name)
        for s in range(2, n + 1):
            for (c, p), m in list(cnt[s - 1].items()):
                c2 = self.op('not', c); cnt[s][(c2, _pol_not(p))] += m; self._note(c2, s, 'not(%s)' % self.rep[c])
            for i in range(1, s - 1):
                for (ca, pa), ma in cnt[i].items():
                    for (cb, pb), mb in cnt[s - 1 - i].items():
                        pj = _pol_join(pa, pb)
                        if pos and pj == P_MIX: continue
                        for nm in ('and', 'or'):
                            c2 = self.op(nm, ca, cb); cnt[s][(c2, pj)] += ma * mb
                            self._note(c2, s, '%s(%s,%s)' % (nm, self.rep[ca], self.rep[cb]))
            for kind, level in self.kinds:
                if s == 3:
                    for form in (TM, TT):
                        c2 = self.op((kind, level, form)); cnt[s][(c2, P_NONE)] += 1; self._note(c2, s, self._src_box(kind, level, form, -1))
                if s >= 4:
                    for (ca, pa), ma in cnt[s - 3].items():
                        if pos and pa != P_NONE: continue        # no CLUB inside box arguments
                        c2 = self.op((kind, level, TL), ca); cnt[s][(c2, P_NONE if pa == P_NONE else P_MIX)] += ma
                        self._note(c2, s, self._src_box(kind, level, TL, ca))
            if self.club and s == 3:
                c2 = self.op('club'); cnt[s][(c2, P_POS)] += 1; self._note(c2, s, 'CLUB(THEM)')
        if pos:   # keep only programs with no CLUB or CLUB positive at top level
            cnt = [defaultdict(int, {k: v for k, v in d.items() if k[1] in (P_NONE, P_POS)}) for d in cnt]
        # collapse polarity
        cc = [defaultdict(int) for _ in range(n + 1)]
        for s in range(1, n + 1):
            for (c, p), m in cnt[s].items():
                cc[s][c] += m
        self.a = np.array([0] + [sum(cc[s].values()) for s in range(1, n + 1)], float)
        K = len(self.funcs)
        mu = np.zeros(K); bits_min = np.full(K, np.inf)
        for s in range(1, n + 1):
            if self.a[s] == 0: continue
            b = np.log2(self.a[s]) + 2 * np.log2(s) + 1
            for c, m in cc[s].items():
                mu[c] += m * 2.0 ** (-b); bits_min[c] = min(bits_min[c], b)
        self.cnt_by_size = cc
        self.count_canon = np.zeros(K)
        for s in range(1, n + 1):
            for c, m in cc[s].items():
                self.count_canon[c] += m
        self.present = np.array([self.count_canon[c] > 0 for c in range(K)])
        # canons that exist only as box arguments of valid programs (pos mode can create
        # canons whose programs are all filtered out) are kept as IDs with zero mass; they
        # are not in the universe and are removed by `universe()`
        self.mu_canon = mu; self.bits_canon = bits_min
        self.n_programs = int(self.a.sum())
        # source strings must refer to a present program: recompute reps for present canons
        # (rep is the shortest source found; in 'pos' mode the shortest may be filtered out)
        if pos:
            self._fix_reps_pos()

    def _fix_reps_pos(self):
        # Re-run a source search restricted to valid programs: shortest valid source per canon.
        n = self.n
        best = {}
        srcs = [defaultdict(dict) for _ in range(n + 1)]   # size -> (canon, pol) -> src (one per key)
        for name in ('C', 'D'):
            srcs[1][(self.op(name), P_NONE)] = name
        for s in range(2, n + 1):
            for (c, p), src in list(srcs[s - 1].items()):
                k = (self.op('not', c), _pol_not(p))
                srcs[s].setdefault(k, 'not(%s)' % src)
            for i in range(1, s - 1):
                for (ca, pa), sa in srcs[i].items():
                    for (cb, pb), sb in srcs[s - 1 - i].items():
                        pj = _pol_join(pa, pb)
                        if pj == P_MIX: continue
                        for nm in ('and', 'or'):
                            srcs[s].setdefault((self.op(nm, ca, cb), pj), '%s(%s,%s)' % (nm, sa, sb))
            for kind, level in self.kinds:
                if s == 3:
                    for form in (TM, TT):
                        srcs[s].setdefault((self.op((kind, level, form)), P_NONE), self._src_box(kind, level, form, -1))
                if s >= 4:
                    for (ca, pa), sa in srcs[s - 3].items():
                        if pa != P_NONE: continue
                        inner = 'THEM(^%s)' % sa
                        nm = '%s%s(%s)' % ('BOX' if kind == KC else 'BOXD', '1' if level else '', inner)
                        srcs[s].setdefault((self.op((kind, level, TL), ca), P_NONE), nm)
            if s == 3 and self.club:
                srcs[s].setdefault((self.op('club'), P_POS), 'CLUB(THEM)')
        for s in range(1, n + 1):
            for (c, p), src in srcs[s].items():
                if p in (P_NONE, P_POS) and c not in best:
                    best[c] = src
        for c, src in best.items():
            self.rep[c] = src

    def arrays(self):
        K = len(self.funcs)
        nat = np.zeros(K, np.int64); ak = np.zeros((K, 4), np.int64); af = np.zeros((K, 4), np.int64); al = np.zeros((K, 4), np.int64)
        aa = np.zeros((K, 4), np.int64); tt = np.zeros(K, np.int64)
        for c, (atoms, t, k) in enumerate(self.funcs):
            assert k <= 4
            nat[c] = k; tt[c] = t
            for j, aid in enumerate(atoms):
                kind, level, form, arg = self.atoms[aid]
                ak[c, j] = kind; al[c, j] = level; af[c, j] = form; aa[c, j] = arg
        return nat, ak, al, af, aa, tt

    def has_club(self, c, _memo=None):
        """Does canon c mention CLUB (top level or inside a box argument)?"""
        if _memo is None: _memo = {}
        if c in _memo: return _memo[c]
        _memo[c] = False
        r = False
        for aid in self.funcs[c][0]:
            kind, level, form, arg = self.atoms[aid]
            if kind == KCLUB or (form == TL and self.has_club(arg, _memo)):
                r = True; break
        _memo[c] = r
        return r


@njit(cache=True)
def _evaluate_club(nat, ak, al, af, aa, tt, inK, max_worlds):
    """modal._evaluate with the CLUB atom: value inK[y] for x against y, every world."""
    K = nat.shape[0]
    hc = np.ones((2, K, K), np.bool_)
    hd = np.ones((2, K, K), np.bool_)
    val = np.zeros((K, K), np.int8)
    for n in range(max_worlds):
        for x in range(K):
            for y in range(K):
                idx = 0
                for j in range(nat[x]):
                    kd = ak[x, j]
                    if kd == 2:
                        b = inK[y]
                    else:
                        f = af[x, j]
                        if f == 0:
                            p, q = y, x
                        elif f == 1:
                            p, q = y, y
                        else:
                            p, q = y, aa[x, j]
                        L = al[x, j]
                        b = hc[L, p, q] if kd == 0 else hd[L, p, q]
                    if b: idx |= 1 << j
                val[x, y] = (tt[x] >> idx) & 1
        changed = False
        for L in range(2):
            if n < L:
                continue
            for x in range(K):
                for y in range(K):
                    c = val[x, y] == 1
                    if hc[L, x, y] and not c:
                        hc[L, x, y] = False; changed = True
                    if hd[L, x, y] and c:
                        hd[L, x, y] = False; changed = True
        if not changed and n >= 2:
            return val, n
    return val, -1


class Club:
    """A language with its arrays and the joint operator F over canon IDs.
    The universe is the set of canons with a program in L_n (count > 0)."""
    def __init__(self, n, club=True, mode='full', kinds=((0, 0), (1, 0), (0, 1), (1, 1))):
        self.L = ClubLanguage(n, kinds, club=club, mode=mode)
        self.arr = self.L.arrays()
        self.K = len(self.L.funcs)
        self.univ = np.nonzero(self.L.present)[0]          # canons in L_n
        self.in_univ = self.L.present.copy()
        self.names = list(self.L.rep)
        self.n_evals = 0

    def play(self, inK):
        """P_K over all canon IDs (helper canons outside the universe included as opponents of
        box arguments only)."""
        val, worlds = _evaluate_club(*self.arr, np.asarray(inK, np.bool_), 400)
        self.n_evals += 1
        if worlds < 0:
            raise RuntimeError('club evaluation did not stabilize')
        return val

    def F(self, inK, val=None):
        if val is None: val = self.play(inK)
        U = self.in_univ
        sc = np.diag(val) == 1
        outside = U & ~np.asarray(inK, bool)
        coop_out = (val[:, outside] == 1).any(axis=1)
        return U & sc & ~coop_out, val

    def iterate(self, inK0, max_iter=200):
        """K_{t+1} = F(K_t) from K_0 until a repeat.  Returns (trajectory of frozensets, cycle start)."""
        seen = {}; traj = []
        K = np.asarray(inK0, bool) & self.in_univ
        for t in range(max_iter):
            key = frozenset(np.nonzero(K)[0].tolist())
            if key in seen:
                return traj, seen[key]
            seen[key] = t; traj.append(key)
            K, _ = self.F(K)
        return traj, None

    def mask(self, S):
        m = np.zeros(self.K, bool); m[list(S)] = True; return m

    def provider(self, inK):
        """Payoff table under P_K restricted to the universe; behavioural classes formed after K."""
        val = self.play(inK)
        u = self.univ
        v = val[np.ix_(u, u)]
        U, PCC = M.pd_payoffs(v, PD)
        prov = ModalProvider(U.astype(float), PCC, self.L.mu_canon[u], [self.names[c] for c in u], self.L.bits_canon[u])
        # map class -> canon IDs (global)
        prov.canon_members = [[int(u[i]) for i in mem] for mem in prov.members]
        prov.sizes = np.array([self.L.count_canon[cm].sum() for cm in prov.canon_members])
        prov.inK = np.array([all(inK[c] for c in cm) for cm in prov.canon_members])
        prov.inK_any = np.array([any(inK[c] for c in cm) for cm in prov.canon_members])
        return prov, val
