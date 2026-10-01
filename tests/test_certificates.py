"""Reference check for the certificates arm (src/certificates.py): enumerate
actual syntax trees up to n, evaluate every pair without canonical forms, and
compare with the canonical-function evaluator.

- lfp / gfp: synchronous Kleene iteration over tree pairs from all-D / all-C;
  pairs that vary on the terminal cycle get D.  On programs without `not` (monotone, so Kleene from the top/bottom
  gives the greatest/least fixed point) there are no divergent pairs, both
  results are fixed points, and gfp >= lfp.
- tag: certificate equivalence decided by brute-force truth tables over atoms
  identified recursively (an independent implementation of propositional
  equivalence), then EQ(ME) := equiv(opponent, me), EQ(^A) := equiv(opponent, A).
"""
import os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import numpy as np
import certificates as CE
from modal import TM, TT, TL


def trees(n):
    by = {1: [('C',), ('D',)]}
    for s in range(2, n + 1):
        out = [('not', t) for t in by[s - 1]]
        for i in range(1, s - 1):
            for a in by[i]:
                for b in by[s - 1 - i]:
                    out += [('and', a, b), ('or', a, b)]
        if s == 3:
            out += [('atom', 'ME'), ('atom', 'THEM')]
        if s >= 4:
            out += [('atom', a) for a in by[s - 3]]
        by[s] = out
    return [t for s in range(1, n + 1) for t in by[s]]


def ev(t, atom):
    op = t[0]
    if op == 'C': return True
    if op == 'D': return False
    if op == 'not': return not ev(t[1], atom)
    if op == 'and': return ev(t[1], atom) and ev(t[2], atom)
    if op == 'or': return ev(t[1], atom) or ev(t[2], atom)
    return atom(t[1])


def has_not(t):
    return t[0] == 'not' or any(isinstance(c, tuple) and has_not(c) for c in t[1:])


def canon_of(L, t):
    op = t[0]
    if op in ('C', 'D'): return L.op(op)
    if op == 'not': return L.op('not', canon_of(L, t[1]))
    if op in ('and', 'or'): return L.op(op, canon_of(L, t[1]), canon_of(L, t[2]))
    arg = t[1]
    form = TM if arg == 'ME' else (TT if arg == 'THEM' else TL)
    return L.op((0, 0, form), canon_of(L, arg) if form == TL else None)


def ref_fixpoint(T, start):
    idx = {t: i for i, t in enumerate(T)}
    K = len(T)
    def step(v):
        out = np.zeros_like(v)
        for i, p in enumerate(T):
            for j, q in enumerate(T):
                def atom(arg):
                    other = i if arg == 'ME' else (j if arg == 'THEM' else idx[arg])
                    return bool(v[j, other])
                out[i, j] = ev(p, atom)
        return out
    v = np.full((K, K), start, np.int8); seen = {v.tobytes(): 0}; it = 0
    while True:
        it += 1; v = step(v); h = v.tobytes()
        if h in seen:
            per = it - seen[h]; lo = v.copy(); hi = v.copy(); w = v
            for _ in range(per):
                w = step(w); lo = np.minimum(lo, w); hi = np.maximum(hi, w)
            out = lo.copy(); out[lo != hi] = 0
            return out, lo == hi, step
        seen[h] = it


def ref_equiv():
    memo = {}
    def atoms(t, acc):
        if t[0] == 'atom': acc.append(t[1])
        else:
            for c in t[1:]:
                if isinstance(c, tuple): atoms(c, acc)
        return acc
    def atom_eq(a, b):
        if a in ('ME', 'THEM') or b in ('ME', 'THEM'): return a == b
        return equiv(a, b)
    def equiv(s, t):
        key = (s, t)
        if key in memo: return memo[key]
        raw = atoms(s, []) + atoms(t, [])
        raw = [a for a in raw if a != 'THEM']          # EQ(THEM) is a tautology
        reps = []
        for a in raw:
            if not any(atom_eq(a, r) for r in reps): reps.append(a)
        def cls(a): return next(k for k, r in enumerate(reps) if atom_eq(a, r))
        same = True
        for bits in itertools.product((False, True), repeat=len(reps)):
            f = lambda a: True if a == 'THEM' else bits[cls(a)]
            if ev(s, f) != ev(t, f):
                same = False; break
        memo[key] = same
        return same
    return equiv


def test_fixpoint(n=5):
    T = trees(n)
    for variant, start in (('lfp', 0), ('gfp', 1)):
        L = CE.CertLanguage(n, variant)
        V, info = CE.evaluate(L)
        assert len(T) == L.n_programs
        R, conv, step = ref_fixpoint(T, start)
        cs = [canon_of(L, t) for t in T]
        mine = V[np.ix_(cs, cs)]
        assert (mine == R).all(), (variant, int((mine != R).sum()))
    # gfp >= lfp on monotone (not-free) programs
    Lg, Ll = CE.CertLanguage(n, 'gfp'), CE.CertLanguage(n, 'lfp')
    Vg, _ = CE.evaluate(Lg); Vl, _ = CE.evaluate(Ll)
    mono = [t for t in T if not has_not(t)]
    cg = [canon_of(Lg, t) for t in mono]; cl = [canon_of(Ll, t) for t in mono]
    assert (Vg[np.ix_(cg, cg)] >= Vl[np.ix_(cl, cl)]).all()
    # on monotone programs there are no divergent pairs, and both are fixed points
    for L, V, c in ((Lg, Vg, cg), (Ll, Vl, cl)):
        R, conv, step = ref_fixpoint(mono, 1 if L is Lg else 0)
        assert conv.all() and (step(R) == R).all()
    return len(T)


def test_tag(n=5):
    T = trees(n)
    L = CE.CertLanguage(n, 'tag')
    V, _ = CE.evaluate(L)
    equiv = ref_equiv()
    cs = [canon_of(L, t) for t in T]
    # canonical ids agree with reference equivalence
    for i, s in enumerate(T):
        for j, t in enumerate(T):
            assert (cs[i] == cs[j]) == equiv(s, t), (s, t)
    bad = 0
    for i, p in enumerate(T):
        for j, q in enumerate(T):
            def atom(arg):
                if arg == 'THEM': return True
                return equiv(q, p) if arg == 'ME' else equiv(q, arg)
            if ev(p, atom) != bool(V[cs[i], cs[j]]): bad += 1
    assert bad == 0, bad
    return len(T)


def test_tageq(n=5):
    """Tags with the equality axioms: on syntax trees, the signature (value with no atom true,
    the atom groups whose truth alone flips it), with atoms identified by the signature class of
    their argument; behaviour on the exclusive assignment (EQ(ME) takes precedence)."""
    T = trees(n)
    sig_memo = {}
    def atoms(t, acc):
        if t[0] == 'atom': acc.append(t[1])
        else:
            for c in t[1:]:
                if isinstance(c, tuple): atoms(c, acc)
        return acc
    def key(a):
        return ('ME',) if a == 'ME' else ('A', sig(a))
    def sig(t):
        if t in sig_memo: return sig_memo[t]
        groups = sorted({key(a) for a in atoms(t, []) if a != 'THEM'})
        none = ev(t, lambda a: a == 'THEM')
        flips = tuple(g for g in groups if ev(t, lambda a, g=g: a == 'THEM' or key(a) == g) != none)
        sig_memo[t] = (none, flips)
        return sig_memo[t]
    L = CE.CertLanguage(n, 'tageq')
    V, _ = CE.evaluate(L)
    cs = [canon_of(L, t) for t in T]
    cls = CE.tag_classes(L, True)
    bad = 0
    for i, p in enumerate(T):
        none, flips = sig(p)
        for j, q in enumerate(T):
            assert (sig(p) == sig(q)) == (cls[cs[i]] == cls[cs[j]])
            g = ('ME',) if sig(q) == sig(p) else ('A', sig(q))
            if (none ^ (g in flips)) != bool(V[cs[i], cs[j]]): bad += 1
    assert bad == 0, bad
    return len(T)


if __name__ == '__main__':
    print('fixpoint (lfp, gfp): %d programs at n=5, all pairs agree' % test_fixpoint(5))
    print('tag: %d programs at n=5, equivalence and all pairs agree' % test_tag(5))
    print('tageq: %d programs at n=5, signature classes and all pairs agree' % test_tageq(5))
