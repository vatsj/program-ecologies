"""Certificates-only arm (predictions/2026-10-01-certificates.md).

Each program publishes a certificate and observes only its opponent's
certificate.  Certificates are honest by construction: the certificate *is* the
rule, a propositional formula over certificate atoms, and the program's action
against an opponent is the value of that formula.  There is no simulation of
source and no provability operator.

Grammar (k = 2, no X, no ROLE), node for node the grammar of the matched control
(W0 / M0, src/matched_control.py), so the length prior mu is identical:

    A    ::= C | D | not A | and A A | or A A | ATOM(App)
    App  ::= THEM(ME) | THEM(THEM) | THEM(^A)          (the atom node is the application)

Node costs: C, D 1; not 1 + |A|; and/or 1 + |A| + |B|; ATOM(THEM(ME)) and
ATOM(THEM(THEM)) 3; ATOM(THEM(^A)) 3 + |A|.  Bits as in the weak arm:
log2 a(|p|) + 2 log2 |p| + 1, a(s) = number of programs of size s.

Variants (only the meaning of an atom differs):

  tag   EQ(ME): the opponent's certificate is equivalent to mine; EQ(^A): it is
        equivalent to A; EQ(THEM) is a tautology (= C).  Equivalence is
        propositional equivalence over canonical atoms (the canonical-function
        id), i.e. the certificate logic's own equivalence.  "I cooperate with
        holders of K."
  lfp   IMP(THEM(Q)): "the opponent's certificate implies it plays C against Q",
        where implication is inductive: the least fixed point of the joint
        system v[x, y] = f_x(atoms read off v), reached by Kleene iteration
        from all-D.  Self-referential loops with no grounding resolve to D.
  gfp   the same atoms, coinductive: Kleene iteration from all-C, the greatest
        fixed point on monotone parts.  Positive loops resolve to C.  This is a
        selection rule among fixed points (re-opens REJECTED "Black-magic fixed
        points").
  lob   the same grammar read as provability in PA (modal.py with the PA box
        only, = M0 of the matched control): unique fixed points.  Reference arm.

In lfp and gfp a pair whose iteration does not settle (a genuine cycle, from
negated self-reference) gets D, the minimax action, as divergent pairs do in the
weak arm.  Two programs with the same canonical function have identical rows and
columns at every iteration (induction on iterations), so the canonical
enumeration of modal.py is exact here too.
"""
import os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import modal as M
from modal import TM, TT, TL, ModalProvider, PD, pd_payoffs
from abm import njit

VARIANTS = ('tag', 'tageq', 'lfp', 'gfp', 'lob', 'lob1')


class CertLanguage(M.ModalLanguage):
    """modal.ModalLanguage with one atom kind; for 'tag' the TT form is the
    tautology EQ(THEM) and folds to C (it still counts as a 3-node program)."""
    def __init__(self, n, variant):
        assert variant in VARIANTS
        self.variant = variant
        self.is_tag = variant in ('tag', 'tageq')
        super().__init__(n, kinds=((0, 1),) if variant == 'lob1' else ((0, 0),))

    def op(self, name, a=None, b=None):
        if self.is_tag and isinstance(name, tuple) and name[2] == TT:
            return super().op('C')
        return super().op(name, a, b)

    def _src_box(self, kind, level, form, arg):
        if self.is_tag:
            return {TM: 'EQ(ME)', TT: 'EQ(THEM)'}.get(form) or 'EQ(^%s)' % self.rep[arg]
        if self.variant in ('lob', 'lob1'):
            return super()._src_box(kind, level, form, arg)
        inner = {TM: 'THEM(ME)', TT: 'THEM(THEM)'}.get(form) or 'THEM(^%s)' % self.rep[arg]
        return 'IMP(%s)' % inner


@njit(cache=True)
def _kleene_step(nat, af, aa, tt, v, out):
    K = nat.shape[0]
    for x in range(K):
        for y in range(K):
            idx = 0
            for j in range(nat[x]):
                f = af[x, j]
                if f == 0:
                    b = v[y, x]
                elif f == 1:
                    b = v[y, y]
                else:
                    b = v[y, aa[x, j]]
                if b: idx |= 1 << j
            out[x, y] = (tt[x] >> idx) & 1


def evaluate_fixpoint(lang, start, max_iter=2000):
    """Synchronous Kleene iteration from all-`start` (0 = D, 1 = C).  Returns
    (val, iterations to settle or enter the cycle, period, number of divergent
    pairs).  Pairs that vary on the terminal cycle get D."""
    nat, ak, al, af, aa, tt = lang.arrays()
    K = len(nat)
    v = np.full((K, K), start, np.int8)
    seen = {v.tobytes(): 0}
    nxt = np.empty_like(v)
    for it in range(1, max_iter + 1):
        _kleene_step(nat, af, aa, tt, v, nxt)
        v, nxt = nxt, v
        h = v.tobytes()
        if h in seen:
            period = it - seen[h]
            if period == 1:
                lang._divergent = np.zeros(v.shape, bool)
                return v.copy(), it, 1, 0
            lo = v.copy(); hi = v.copy(); w = v.copy(); w2 = np.empty_like(w)
            for _ in range(period):
                _kleene_step(nat, af, aa, tt, w, w2); w, w2 = w2, w
                lo = np.minimum(lo, w); hi = np.maximum(hi, w)
            div = lo != hi
            out = lo.copy(); out[div] = 0
            lang._divergent = div
            return out, it, period, int(div.sum())
        seen[h] = it
    raise RuntimeError('Kleene iteration did not cycle within %d steps' % max_iter)


def tag_classes(lang, axioms, want_sigs=False):
    """Certificate-equivalence class of each canonical function.  Without
    axioms: the canonical id (propositional equivalence over independent atoms).
    With the equality axioms (tageq): the atoms of one certificate are
    equalities of the opponent's certificate to distinct certificates, so at
    most one is true; two certificates are equivalent iff they agree when no
    atom is true and when exactly one atom (up to equivalence of its argument)
    is true: the signature is (value with no atom true, the atoms whose truth
    alone flips it).  Computed bottom-up: an atom's argument is an earlier canonical id."""
    nat, ak, al, af, aa, tt = lang.arrays()
    K = len(nat)
    if not axioms:
        return np.arange(K)
    cls = np.zeros(K, np.int64); ids = {}
    for c in range(K):
        keys = [('ME',) if af[c, j] == TM else ('A', int(cls[aa[c, j]])) for j in range(nat[c])]
        groups = sorted(set(keys))
        none = int(tt[c]) & 1
        true_on = []
        for g in groups:
            idx = 0
            for j in range(nat[c]):
                if keys[j] == g: idx |= 1 << j
            if ((int(tt[c]) >> idx) & 1) != none: true_on.append(g)     # groups where the value flips
        sig = (none, tuple(true_on))
        cls[c] = ids.setdefault(sig, len(ids))
    if want_sigs:
        sigs = {k: v for v, k in ids.items()}
        return cls, [sigs[int(cls[c])] for c in range(K)]
    return cls


def evaluate_tag(lang, axioms=False):
    nat, ak, al, af, aa, tt = lang.arrays()
    K = len(nat)
    val = np.zeros((K, K), np.int8)
    if axioms:
        # behaviour read off the signature on the exclusive assignment: if the opponent's certificate is
        # equivalent to mine only EQ(ME) is true (it takes precedence when a named literal is also
        # equivalent to me, which the axioms exclude), else only the atom naming its class, if any
        cls, sigs = tag_classes(lang, True, want_sigs=True)
        for x in range(K):
            none, flips = sigs[x]; fl = set(flips)
            for y in range(K):
                g = ('ME',) if cls[y] == cls[x] else ('A', int(cls[y]))
                val[x, y] = none ^ (1 if g in fl else 0)
        return val
    cls = tag_classes(lang, False)
    for x in range(K):
        idx = np.zeros(K, np.int64)
        for j in range(nat[x]):
            f = af[x, j]
            assert f in (TM, TL)
            b = (cls == cls[x]) if f == TM else (cls == cls[aa[x, j]])
            idx |= b.astype(np.int64) << j
        val[x] = (int(tt[x]) >> idx) & 1
    return val


def evaluate(lang):
    """val[x, y] = 1 iff canonical program x plays C against y.  info: dict."""
    if lang.is_tag:
        return evaluate_tag(lang, lang.variant == 'tageq'), dict(iters=0, period=1, divergent=0)
    if lang.variant in ('lob', 'lob1'):
        val, worlds = M.evaluate(lang)
        return val, dict(iters=worlds, period=1, divergent=0)
    val, it, per, div = evaluate_fixpoint(lang, 0 if lang.variant == 'lfp' else 1)
    return val, dict(iters=it, period=per, divergent=div, inconsistent=fallback_inconsistent(lang, val))


def fallback_inconsistent(lang, val):
    """Settled (non-divergent) pairs whose value is not reproduced by one more
    Kleene step from the final matrix: the D fallback on divergent pairs can
    break the equations of settled pairs that read them.  (count, mu x mu weight)"""
    nat, ak, al, af, aa, tt = lang.arrays()
    out = np.empty_like(val)
    _kleene_step(nat, af, aa, tt, val, out)
    bad = (out != val) & ~lang._divergent
    return int(bad.sum()), float(lang.mu_canon @ bad @ lang.mu_canon)


def build(n, variant, pay=PD):
    L = CertLanguage(n, variant)
    val, info = evaluate(L)
    U, PCC = pd_payoffs(val, pay)
    prov = ModalProvider(U.astype(float), PCC, L.mu_canon, L.rep, L.bits_canon)
    prov.sizes = np.array([L.count_canon[m].sum() for m in prov.members])
    return L, val, info, prov


# ------------------------------------------------------------------ analysis helpers
def class_val(prov, val):
    """Class-level action matrix: cv[i, j] = 1 iff class i plays C against class j."""
    reps = [m[0] for m in prov.members]
    return val[np.ix_(reps, reps)]


def fb_name(variant):
    return {'tag': 'EQ(ME)', 'tageq': 'EQ(ME)', 'lob': 'BOX(THEM(ME))', 'lob1': 'BOX1(THEM(ME))'}.get(variant, 'IMP(THEM(ME))')


def class_of(prov, L, src):
    c = L.rep.index(src)
    for i, m in enumerate(prov.members):
        if c in m:
            return i
    return None


def coop_components(cv, nodes):
    """Connected components of the mutual-cooperation graph on `nodes`
    (edge i-j iff i and j cooperate with each other)."""
    nodes = list(nodes); comp = {}
    for s in nodes:
        if s in comp: continue
        comp[s] = s; stack = [s]
        while stack:
            a = stack.pop()
            for b in nodes:
                if b not in comp and cv[a, b] and cv[b, a]:
                    comp[b] = s; stack.append(b)
    groups = defaultdict(list)
    for a in nodes: groups[comp[a]].append(a)
    return list(groups.values())
