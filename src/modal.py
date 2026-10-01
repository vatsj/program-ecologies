"""Modal (Löbian) arm: programs condition on what is *provable* about the
opponent's play (THEORY §9.2).  An instrument, not a theory commitment: a free
provability operator idealizes proof search at zero cost (upper bound).

Grammar (k = 2, no X, no ROLE; deterministic):

    A ::= C | D | not A | and A A | or A A | BOX(App) | BOXD(App) | BOX1(App) | BOXD1(App)
    App ::= THEM(ME) | THEM(THEM) | THEM(^A)

BOX(THEM(P)) is true (C) iff it is provable (in PA) that the opponent plays C against P;
BOXD(THEM(P)) iff it is provable that it plays D against P.  BOX1/BOXD1 are the same
with provability in PA + Con(PA), which PrudentBot's second clause needs: PA cannot
prove that FairBot defects against DefectBot (that needs Con(PA)), so with PA alone
PrudentBot defects on FairBot and on itself (LaVictoire et al. 2014 use PA+1 there).  The box is the
application node itself, so BOX(THEM(ME)) (FairBot) costs 3 nodes, as THEM(ME)
does in the weak arm; BOX(THEM(^A)) costs 3 + |A|.  PrudentBot
and(BOX(THEM(ME)), BOXD1(THEM(^D))) costs 8.

Semantics: provability logic GL on the linear Kripke chain.  At world n,
BOX(s) holds iff s holds at every world m < n (so every box holds at world 0),
and BOX1(s) iff s holds at every world m with 1 <= m < n (Con(PA) fails only at world 0),
and the pair values at world n follow from the boxes.  Box truth is monotone
non-increasing in n, so the values stabilize; the stable value is the outcome
(LaVictoire et al. 2014, modal agents).  Every self-reference is guarded by a
box, so fixed points are unique (de Jongh-Sambin): no selection rule is hidden.

Programs reduce exactly to boolean functions of their box atoms, and two
programs with the same reduced function over the same (canonical) atoms play
identically against everything (induction on worlds).  Enumeration is a DP over
(size, canonical function) counts, so the prior (bits = log2 a(|p|) + 2 log2
|p| + 1, as in the weak arm) is exact without materializing programs.
"""
import os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit

TM, TT, TL = 0, 1, 2          # THEM(ME), THEM(THEM), THEM(^A)
KC, KD = 0, 1                 # box kinds: provably C, provably D
LEVELS = (0, 1)               # proof systems PA, PA + Con(PA)


class ModalLanguage:
    def __init__(self, n, kinds=((0, 0), (1, 0), (0, 1), (1, 1))):
        """kinds: allowed boxes as (kind, level); (0, 0) alone = BOX only, the grammar
        isomorphic to the weak arm without X and ROLE."""
        self.n = n
        self.kinds = tuple(kinds)
        self.atoms = []           # atom id -> (kind, form, arg canon or -1)
        self.atom_id = {}
        self.funcs = []           # canon id -> (atoms tuple, tt, k)
        self.func_id = {}
        self.rep = []             # canon id -> shortest source
        self.rep_size = []
        self._memo = {}
        self._enumerate()

    # ---- canonical boolean functions over box atoms ---------------------
    def _canon(self, atoms, tt):
        """Reduce to essential atoms; return canon id."""
        atoms = list(atoms); k = len(atoms)
        j = 0
        while j < len(atoms):
            k = len(atoms)
            dep = False
            for i in range(1 << k):
                if not (i >> j) & 1:
                    if ((tt >> i) & 1) != ((tt >> (i | (1 << j))) & 1):
                        dep = True; break
            if dep:
                j += 1; continue
            # drop atom j
            ntt = 0; idx = 0
            for i in range(1 << k):
                if not (i >> j) & 1:
                    lo = i & ((1 << j) - 1); hi = (i >> (j + 1)) << j
                    if (tt >> i) & 1:
                        ntt |= 1 << (lo | hi)
            atoms.pop(j); tt = ntt
        key = (tuple(atoms), tt)
        c = self.func_id.get(key)
        if c is None:
            c = len(self.funcs); self.func_id[key] = c
            self.funcs.append((tuple(atoms), tt, len(atoms)))
            self.rep.append(None); self.rep_size.append(None)
        return c

    def _expand(self, canon, union):
        atoms, tt, k = self.funcs[canon]
        pos = [union.index(a) for a in atoms]
        out = 0
        for i in range(1 << len(union)):
            sub = 0
            for t, p in enumerate(pos):
                if (i >> p) & 1: sub |= 1 << t
            if (tt >> sub) & 1: out |= 1 << i
        return out

    def op(self, name, a=None, b=None):
        key = (name, a, b)
        if key in self._memo: return self._memo[key]
        if name == 'C': c = self._canon((), 1)
        elif name == 'D': c = self._canon((), 0)
        elif name == 'not':
            atoms, tt, k = self.funcs[a]
            c = self._canon(atoms, (~tt) & ((1 << (1 << k)) - 1))
        elif name in ('and', 'or'):
            union = sorted(set(self.funcs[a][0]) | set(self.funcs[b][0]))
            ta, tb = self._expand(a, union), self._expand(b, union)
            c = self._canon(union, (ta & tb) if name == 'and' else (ta | tb))
        else:     # box: name = (kind, level, form), a = arg canon for TL
            kind, level, form = name
            at = (kind, level, form, a if form == TL else -1)
            aid = self.atom_id.get(at)
            if aid is None:
                aid = len(self.atoms); self.atom_id[at] = aid; self.atoms.append(at)
            c = self._canon((aid,), 2)       # tt: value = atom
        self._memo[key] = c
        return c

    def _src_box(self, kind, level, form, arg):
        inner = {TM: 'THEM(ME)', TT: 'THEM(THEM)'}.get(form) or 'THEM(^%s)' % self.rep[arg]
        return '%s%s(%s)' % ('BOX' if kind == KC else 'BOXD', '1' if level else '', inner)

    def _note(self, c, s, src):
        if self.rep_size[c] is None or s < self.rep_size[c]:
            self.rep_size[c] = s; self.rep[c] = src

    def _enumerate(self):
        n = self.n
        cnt = [defaultdict(int) for _ in range(n + 1)]     # size -> canon -> count
        for name in ('C', 'D'):
            c = self.op(name); cnt[1][c] += 1; self._note(c, 1, name)
        for s in range(2, n + 1):
            for c, m in list(cnt[s - 1].items()):
                c2 = self.op('not', c); cnt[s][c2] += m; self._note(c2, s, 'not(%s)' % self.rep[c])
            for i in range(1, s - 1):
                for ca, ma in cnt[i].items():
                    for cb, mb in cnt[s - 1 - i].items():
                        for nm in ('and', 'or'):
                            c2 = self.op(nm, ca, cb); cnt[s][c2] += ma * mb
                            self._note(c2, s, '%s(%s,%s)' % (nm, self.rep[ca], self.rep[cb]))
            for kind, level in self.kinds:
              if True:
                if s == 3:
                    for form in (TM, TT):
                        c2 = self.op((kind, level, form)); cnt[s][c2] += 1; self._note(c2, s, self._src_box(kind, level, form, -1))
                if s >= 4:
                    for ca, ma in cnt[s - 3].items():
                        c2 = self.op((kind, level, TL), ca); cnt[s][c2] += ma; self._note(c2, s, self._src_box(kind, level, TL, ca))
        self.a = np.array([0] + [sum(cnt[s].values()) for s in range(1, n + 1)], float)
        K = len(self.funcs)
        mu = np.zeros(K); bits_min = np.full(K, np.inf)
        for s in range(1, n + 1):
            b = np.log2(self.a[s]) + 2 * np.log2(s) + 1
            for c, m in cnt[s].items():
                mu[c] += m * 2.0 ** (-b); bits_min[c] = min(bits_min[c], b)
        self.mu_canon = mu; self.bits_canon = bits_min
        self.count_canon = np.zeros(K)
        for s in range(1, n + 1):
            for c, m in cnt[s].items():
                self.count_canon[c] += m
        self.n_programs = int(self.a.sum())

    # ---- arrays for the evaluator ----------------------------------------
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


@njit(cache=True)
def _evaluate(nat, ak, al, af, aa, tt, max_worlds):
    """val[x, y] = 1 if x plays C against y, at the stable world.
    hc[L, x, y]: val = C at every world m with L <= m < n (likewise hd for D)."""
    K = nat.shape[0]
    hc = np.ones((2, K, K), np.bool_)
    hd = np.ones((2, K, K), np.bool_)
    val = np.zeros((K, K), np.int8)
    for n in range(max_worlds):
        for x in range(K):
            for y in range(K):
                idx = 0
                for j in range(nat[x]):
                    f = af[x, j]
                    if f == 0:
                        p, q = y, x
                    elif f == 1:
                        p, q = y, y
                    else:
                        p, q = y, aa[x, j]
                    L = al[x, j]
                    b = hc[L, p, q] if ak[x, j] == 0 else hd[L, p, q]
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


def evaluate(lang, max_worlds=200):
    val, n = _evaluate(*lang.arrays(), max_worlds)
    if n < 0:
        raise RuntimeError('modal evaluation did not stabilize')
    return val, n


def pd_payoffs(val, pay):
    """pay[a][b] with level order (D=0, C=1)."""
    a = val.astype(int); b = val.T.astype(int)
    P = np.asarray(pay)
    return P[a, b], (a * b).astype(float)


class ModalProvider:
    """Chain provider over behavioural classes (merged by payoff row and column)."""
    def __init__(self, U, PCC, mu, names, bits):
        R = np.round(U, 9)
        sig = defaultdict(list)
        for c in range(U.shape[0]):
            sig[(R[c].tobytes(), R[:, c].tobytes())].append(c)
        reps = []
        for mem in sig.values():
            rep = min(mem, key=lambda c: (bits[c], c))
            reps.append((rep, mem, float(mu[mem].sum())))
        reps.sort(key=lambda t: -t[2])
        z = sum(t[2] for t in reps)
        self.classes = [(i, [i], t[2] / z) for i, t in enumerate(reps)]
        idx = [t[0] for t in reps]
        self.Ufull = U[np.ix_(idx, idx)]; self.PCC = PCC[np.ix_(idx, idx)]
        self.names = [names[c] for c in idx]; self.bits = np.array([bits[c] for c in idx])
        self.members = [t[1] for t in reps]
        self.sizes = None
        self.ids = np.arange(len(idx))

    def prepare(self, support): pass
    def U(self, ids, sup=None): return self.Ufull[np.ix_(list(ids), list(ids))]
    def mutant_classes(self, support): return self.classes
    def blocks_for(self, support):
        si = np.array(list(support), int); R = self.ids
        return self.Ufull[np.ix_(R, si)], self.Ufull[np.ix_(si, R)], self.Ufull[R, R], self.Ufull[np.ix_(si, si)]


class ClassLang:
    """The minimal language interface the chain's reporting uses."""
    def __init__(self, prov):
        self.names = prov.names; self.bits = prov.bits
        self.mu = np.array([c[2] for c in prov.classes])
    def src(self, i): return self.names[int(i)]


PD = [[-1, 1], [-2, 0]]       # pay[a][b], level order (D, C): D/D -1, D/C 1, C/D -2, C/C 0


def build(n, pay=PD, kinds=((0, 0), (1, 0), (0, 1), (1, 1))):
    L = ModalLanguage(n, kinds)
    val, worlds = evaluate(L)
    U, PCC = pd_payoffs(val, pay)
    prov = ModalProvider(U, PCC, L.mu_canon, L.rep, L.bits_canon)
    prov.sizes = np.array([L.count_canon[m].sum() for m in prov.members])
    return L, val, worlds, prov
