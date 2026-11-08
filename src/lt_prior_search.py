"""Targeted search for the rare reader-shaped classes of the length prior (queue 75, step 1b).  The exhaustive enumeration
cannot reach readers in R0 (the shortest is about a dozen nodes) and barely reaches them in R1; this module enumerates, by
size and with exact prior masses, the spellings of a restricted but rich family of reader programs:

  single (let)     app (lam F) READ                 F a decision tree over r = v0
  single (inline)  F[r := READ]                     F with exactly one occurrence of r
  two (let)        app (lam F1') READ1,  F1' = F1 with its CONT leaf replaced by  app (lam F2) READ2   (READ2 of the
                   other slot; reads of one slot only are covered by the single forms)

F are decision trees of depth one (leaves: codes and one junk literal class; tests: eq of r against a code or TO, le / lt
against a code, and the or / and / not combinations of eq tests as nested ifs).  READ is a read of the next or previous
slot: in R0 the written-out reads (capk K1 (run K2 n p) me), (app (run K n p) me) and the prev mirrors, K over the literal
classes of lt_prior that can matter (see CAPS); in R1 the leaves readn / readp.  The program table is composed from the
read's own table (its value r over the 29 x 29 probe profiles and its failed-read count) and the response map of F; the
class is assigned by lt_prior.classify_table, so exact members are recognised by their tables.  Every spelling counted is a
term of the prior, so the masses are LOWER bounds on the class masses (the grammar is not exhaustive); the counts at the
minimal size and the next two are counts of the spellings of this grammar.

    python3 src/lt_prior_search.py R0 OUT.json
"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lt_code as L
import lt_prior as P

TO = ('con', 'TO')
LITM = {rep: m for lab, rep, m in P.LIT_CLASSES}
LITLAB = {rep: lab for lab, rep, m in P.LIT_CLASSES}
CAPS = [95, 191, 383, 767, 1500]          # cap classes that can complete a read of a reader: [64,127] ... >= 1023
SMALLCAPS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 23, 47]


def cls_mass(t, mach):
    """prior mass of a term whose nat literals are literal-class representatives (class mass)."""
    pt = 1.0 / mach.T
    tag = t[0]
    if tag == 'nat':
        return pt * LITM[t[1]]
    if tag == 'v':
        return pt * P.elias(t[1])
    if tag == 'con':
        return pt / 5
    if tag in ('readn', 'readp', 'cont'):
        return pt
    if tag == 'op':
        return pt / 7 * cls_mass(t[2], mach) * cls_mass(t[3], mach)
    m = pt
    for c in t[1:]:
        m *= cls_mass(c, mach)
    return m


# ====================================================================== decision trees over r (v0)
R = ('v', 0)
CODES = [('nat', k) for k in range(9)] + [('nat', 12)]


def tests(small):
    ks = [('nat', k) for k in range(9)] + [TO]
    out = []
    for k in ks:
        out.append(('eq', R, k))
    if not small:
        for k in ks:
            out.append(('eq', k, R))
        for j in range(9):
            for o in ('le', 'lt'):
                out.append(('op', o, R, ('nat', j))); out.append(('op', o, ('nat', j), R))
    eqs = [('eq', R, k) for k in ks]
    for a in eqs:
        out.append(('if', a, ('con', 'F'), ('con', 'T')))
        for b in eqs:
            out.append(('if', a, ('con', 'T'), b))
            out.append(('if', a, b, ('con', 'F')))
    return out


def trees(cont, small, leaves):
    base = [(l, False) for l in leaves]
    if cont:
        base.append((('cont',), True))
    out = list(base)
    for c in tests(small):
        for a in base:
            for b in base:
                out.append((('if', c, a[0], b[0]), a[1] or b[1]))
    return out


def occ(t, pat):
    if t == pat:
        return 1
    if t[0] in ('nat', 'con', 'v', 'cont'):
        return 0
    if t[0] == 'op':
        return occ(t[2], pat) + occ(t[3], pat)
    return sum(occ(c, pat) for c in t[1:])


def subst(t, pat, repl):
    if t == pat:
        return repl
    if t[0] in ('nat', 'con', 'v', 'cont'):
        return t
    if t[0] == 'op':
        return ('op', t[1], subst(t[2], pat, repl), subst(t[3], pat, repl))
    return (t[0],) + tuple(subst(c, pat, repl) for c in t[1:])


def rmap(F):
    """response map of F: entries for r = 0..8, TO, 99 and BOT(11th index handled by the composer): -1 = not a code (forfeit),
    -2 = continue (a cont leaf, marked by the literal 50)."""
    G = subst(F, ('cont',), ('nat', 50))
    out = []
    for val in [('nat', k) for k in range(9)] + [TO, ('nat', 99)]:
        v, st = L.evaluate(('app', ('lam', G), val), 400)
        if v == 50:
            out.append(-2)
        else:
            ok = isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 8
            out.append(int(v) if ok else -1)
    return tuple(out) + (-1,)       # index 11: the read itself was stuck / ran out of fuel: forfeit


def group(cont, small, leaves, mach, need_inline):
    """{(map, size): [mass, count, example]} over the trees (cont: exactly one cont leaf), size = nodes of F (without the
    cont leaf); the inline group takes the trees with one occurrence of r, mass without the r leaf, size - 1 (the r node is
    replaced by READ)."""
    let = {}; inl = {}
    pt = 1.0 / mach.T
    rleaf = pt * P.elias(0)
    for F, hc in trees(cont, small, leaves):
        nc = occ(F, ('cont',))
        if cont and nc != 1:
            continue
        sz = P.node_count(F) - nc
        m = cls_mass(F, mach)
        if nc:
            m /= pt                       # the cont leaf stands for a sub-program counted separately
        mp = rmap(F)
        e = let.setdefault((mp, sz), [0.0, 0, F]); e[0] += m; e[1] += 1
        if need_inline and not cont and occ(F, R) == 1:
            e = inl.setdefault((mp, sz - 1), [0.0, 0, F]); e[0] += m / rleaf; e[1] += 1
    return let, inl


# ====================================================================== READ variants
class Reads:
    def __init__(self, mach):
        self.mach = mach
        self.pr = P.probes()
        self.variants = []
        if mach.name == 'R1':
            self.variants.append(('readn', 'n', ('readn',)))
            self.variants.append(('readp', 'p', ('readp',)))
        else:
            for d in 'np':
                x, y, z = (('v', 1), ('v', 0), ('v', 2)) if d == 'n' else (('v', 0), ('v', 2), ('v', 1))
                for k1 in CAPS + SMALLCAPS[:0]:
                    for k2 in CAPS:
                        self.variants.append(('capk[%s,%s]%s' % (LITLAB[k1], LITLAB[k2], d), d,
                                              ('capk', ('nat', k1), ('run', ('nat', k2), x, y), z)))
                for k in CAPS:
                    self.variants.append(('app[%s]%s' % (LITLAB[k], d), d, ('app', ('run', ('nat', k), x, y), z)))
        self.rc = []; self.nto = []
        n = self.pr.n
        for lab, d, term in self.variants:
            prog = P.frame(P.expand(term))
            rc = np.empty((n, n), np.int64); nto = np.zeros((n, n), np.int64)
            for b in range(n):
                for c in range(n):
                    cd, nt, f, st, raw, _ = P.eval_prog(prog, self.pr.terms[b], self.pr.terms[c])
                    if st > 1100 or (not isinstance(raw, int) and raw != 'TO') or isinstance(raw, bool):
                        rc[b, c] = 11
                    elif raw == 'TO':
                        rc[b, c] = 9
                    elif 0 <= raw <= 8:
                        rc[b, c] = raw
                    else:
                        rc[b, c] = 10
                    nto[b, c] = nt
            self.rc.append(rc); self.nto.append(nto)
            L._compiled.clear()

    def size(self, i):
        return 1 if self.mach.name == 'R1' else P.node_count(self.variants[i][2])

    def mass(self, i, depth):
        if self.mach.name == 'R1':
            return 1.0 / self.mach.T
        return cls_mass(shift(self.variants[i][2], depth), self.mach)


def shift(t, d):
    if t[0] == 'v':
        return ('v', t[1] + d)
    if t[0] in ('nat', 'con'):
        return t
    if t[0] == 'op':
        return ('op', t[1], shift(t[2], d), shift(t[3], d))
    return (t[0],) + tuple(shift(c, d) for c in t[1:])


def tab1(rd, i, mp):
    M = np.array(mp)
    out = M[rd.rc[i]]
    fo = (out < 0)
    return np.where(fo, 8, out).astype(np.int8), np.minimum(rd.nto[i], 100).astype(np.int8), fo.astype(np.int8)


def tab2(rd, i, j, m1, m2):
    M1 = np.array(m1); M2 = np.array(m2)
    o1 = M1[rd.rc[i]]
    cont = (o1 == -2)
    o2 = M2[rd.rc[j]]
    out = np.where(cont, o2, o1)
    nto = rd.nto[i] + cont * rd.nto[j]
    fo = (out < 0)
    return np.where(fo, 8, out).astype(np.int8), np.minimum(nto, 100).astype(np.int8), fo.astype(np.int8)


def search(mach, two_limit=None):
    pr = P.probes()
    rd = Reads(mach)
    pt = 1.0 / mach.T
    res = {}

    def add(key, m, cnt, ex):
        e = res.get(key)
        if e is None:
            res[key] = [m, cnt, ex]
        else:
            e[0] += m; e[1] += cnt

    let, inl = group(False, False, CODES, mach, True)
    nread = len(rd.variants)
    for i in range(nread):
        rs = rd.size(i); rm0 = rd.mass(i, 0)
        for (mp, sz), (mF, cF, F) in let.items():
            fam, exact = P.classify_table(tab1(rd, i, mp), pr)
            add((fam, exact, 2 + sz + rs, 'let'), pt * pt * mF * rm0, cF, ('app', ('lam', F), rd.variants[i][2]))
        for (mp, sz1), (mF, cF, F) in inl.items():
            fam, exact = P.classify_table(tab1(rd, i, mp), pr)
            add((fam, exact, sz1 + rs, 'inline'), mF * rm0, cF, subst(F, R, rd.variants[i][2]))
    # two-stage: leaves of F1 / F2 restricted to the codes the library readers use
    small_leaves = [('nat', k) for k in (1, 4, 8, 0, 3, 5)] + [('nat', 12)]
    let1, _ = group(True, True, small_leaves, mach, False)
    let2, _ = group(False, True, small_leaves, mach, False)
    if mach.name == 'R1':
        two_ids = list(range(nread))
    else:       # two reads of the same cap class (383 or >= 1023) in the written-out capk form
        two_ids = [i for i, v in enumerate(rd.variants) if v[0].startswith('capk[[256,510],[256,510]]') or v[0].startswith('capk[>=1023,>=1023]')]
    for i in two_ids:
        for j in two_ids:
            if rd.variants[i][1] == rd.variants[j][1]:
                continue
            m1r = rd.mass(i, 0); m2r = rd.mass(j, 1)
            for (mp1, sz1), (mF1, c1, F1) in let1.items():
                for (mp2, sz2), (mF2, c2, F2) in let2.items():
                    fam, exact = P.classify_table(tab2(rd, i, j, mp1, mp2), pr)
                    total = 2 + sz1 + 2 + sz2 + rd.size(i) + rd.size(j)
                    ex2 = ('app', ('lam', subst(F1, ('cont',), ('app', ('lam', F2), rd.variants[j][2]))), rd.variants[i][2])
                    add((fam, exact, total, 'two-let'), pt ** 4 * mF1 * mF2 * m1r * m2r, c1 * c2, ex2)
    return res


def pack(res):
    out = {}
    for (fam, exact, size, form), (m, c, ex) in res.items():
        out.setdefault('%s|%s' % (fam, exact), {}).setdefault(str(size), {})[form] = [m, c, P.to_sexpr(ex) if ex else '', ex]
    return out


if __name__ == '__main__':
    mach = P.MACHINES[sys.argv[1]]
    out = sys.argv[2]
    t0 = time.time()
    res = L.run_big(search, mach)
    json.dump(dict(machine=mach.name, wall=time.time() - t0, classes=pack(res)), open(out, 'w'))
    print('done', time.time() - t0)
