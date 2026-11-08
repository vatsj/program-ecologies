"""Step 2 of queue 76 (spec specs/2026-11-08-bully-resistance.md): the length-prior mass of the prudent reader P and the opener O.

Machines R0 and R1 are queue 75's (lt_prior.py).  R2 = R1 + two probe tags probn, probp (arity 1, one child that must be a literal code
0..8 -- anything else is stuck): probn(c) = (capk 400 (run 400 n <the constant program of code c>) me), the read of next with the third slot (p)
replaced by the quoted constant program lam me. lam n. lam p. c; probp(c) = (capk 400 (run 400 p me) <that constant>).  The expansion is the
written-out read of bully_resist.py (PROBEN, PROBEP) with the same caps, so the probe tag is only an abbreviation (checked in
tests/test_lt_prior_br.py against the explicit implementation on the full probe table: arguments, nested caps, root fuel, actions, charges).

This module patches lt_prior / lt_prior_enum / lt_prior_search at import (R2 registered, probe expansion, extended members), it edits no file.

  python3 src/lt_prior_br.py search R0|R1|R2 OUT.json      lower bounds and shortest spellings of P / Q / O (and, for R2, the T+ classes)
  python3 src/lt_prior_br.py enum R2 5 SHARD K OUT.json    exhaustive enumeration (V3 accounting)
  python3 src/lt_prior_br.py mc R2 N SEED OUT.json S0      Monte Carlo from the prior
  python3 src/lt_prior_br.py v4 OUT.json                   V4: member bodies classified by the step-2 classifier return their own class

Grammar.  P: two nested lets, F1 (a depth-one decision tree over the cooperation read r with one continuation leaf) whose continuation is
let q = PROBE in F2 (a depth-one tree over q), reads of the same direction, caps in the classes 383 and >= 1023 (R0, R1) -- the grammar of
lt_prior_search.py with the probe as the second read.  O: let a = READn, let b = READp (either order), G = if C1 4 (if C2 1 D) with the
pattern tests spelled as nested ifs, every order of conjuncts and of eq arguments, D the two-partner rule spelled over (a, b).  Every
spelling counted is a term of the prior, so the masses are lower bounds on the class masses.
"""
import os, sys, json, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lt_code as L
import lt_prior as P
import lt_prior_enum as E
import lt_prior_search as S
import bully_resist as BR

# ====================================================================== the machine R2 and its expansion
P.ARITY['probn'] = 1
P.ARITY['probp'] = 1
R2 = P.Machine('R2', L.TAGS + ['readn', 'readp', 'probn', 'probp'])
P.MACHINES['R2'] = R2
P.ENUM_TAGS['R2'] = [t for t in R2.tags if t not in P.EXCLUDED_ENUM]
P._FORBID = tuple(P._FORBID) + ('probn', 'probp')


def const_quote(c):
    return ('quote', ('lam', ('lam', ('lam', ('nat', int(c))))))


_orig_expand = P.expand
_orig_expand_q = P.expand_q


def expand(t, d=0):
    tag = t[0]
    if tag in ('probn', 'probp'):
        c = t[1]
        if c[0] != 'nat' or not (0 <= c[1] <= 8):
            return ('fst', ('nat', 0))                        # not a literal code: stuck
        Q = const_quote(c[1])
        if tag == 'probn':
            return ('capk', ('nat', 400), ('run', ('nat', 400), ('v', d + 1), Q), ('v', d + 2))
        return ('capk', ('nat', 400), ('run', ('nat', 400), ('v', d), ('v', d + 2)), Q)
    return _orig_expand(t, d)


def expand_q(t, d):
    if t[0] in ('probn', 'probp'):
        return expand(t, d)
    return _orig_expand_q(t, d)


P.expand = expand
P.expand_q = expand_q

# the R1 fast paths of classify_body also serve R2 (a body without a probe tag)
_orig_classify_body = P.classify_body


def classify_body(body, mach, pr=None, taint=True):
    if mach.name == 'R2':
        pr = pr or P.probes()
        if P.static_junk(body):
            return 'junk_f', '', 0
        acc = {}
        P._scan(body, 0, acc)
        if (acc.get('n') or acc.get('p')) and not acc.get('bad'):
            tab = P.fast_table_r1(body, acc, pr)
            fam, exact = P.classify_table(tab, pr)
            return fam, exact, 1
        if (acc.get('n') or acc.get('p')) and acc.get('badref') and not acc.get('badtag'):
            tab = P.hybrid_table_r1(body, acc, pr)
            fam, exact = P.classify_table(tab, pr)
            return fam, exact, pr.n * pr.n
        term = P.expand(body)
        prog = P.frame(term)
        c0 = pr.terms[0]
        cd, nt, f, st, raw, hit = P.eval_prog(prog, c0, c0, taint=True)
        if not (hit[0] or hit[1]):
            fam, _ = P._const_cls(cd, nt, f)
            return fam, '', 1
        tab, ne = pr.table_adaptive(prog, hit)
        fam, exact = P.classify_table(tab, pr)
        return fam, exact, 1 + ne
    return _orig_classify_body(body, mach, pr, taint)


P.classify_body = classify_body

_orig_gen = E.Enumerator.gen


def _gen(self, size, d):
    yield from _orig_gen(self, size, d)
    if size >= 2:
        for tg in ('probn', 'probp'):
            if tg in self.tags:
                for t, m in self.get(size - 1, d):
                    yield (tg, t), self.pt * m


E.Enumerator.gen = _gen


def extend_probes():
    """members = the 55 programs of the extended catalogue (T+, P, Q, O, F2)."""
    pr = P.probes()
    if getattr(pr, '_br', False):
        return pr
    cat = BR.CatalogueBR()
    pr.members = cat.names; pr.mterm = cat.terms; pr.mfam = cat.fam
    pr.sig2member = {}
    for i, term in enumerate(cat.terms):
        pr.sig2member.setdefault(pr.signature(pr.table(term)), []).append(i)
    pr._br = True
    return pr


FAMOF = {n: f for n, f, _ in BR.library_br()}


def member_group(name):
    f = FAMOF[name]
    if f == 'prudent':
        return 'prudent_z' if name[2] == 'z' else 'prudent_o'
    return {'prudent_a': 'prudent_a', 'opener': 'opener', 'single2': 'f2', 'single': 'single', 'two': 'two', 'bully': 'bully',
            'exploit': 'exploit', 'const': 'const', 'junk_f': 'junk_f', 'junk_r': 'junk_r'}[f]


# ====================================================================== reads and probes of a machine
class ReadsBR(S.Reads):
    """S.Reads with R2 treated as R1 (readn / readp)."""

    def __init__(self, mach):
        self.mach = mach
        self.pr = P.probes()
        self.variants = []
        if mach.name in ('R1', 'R2'):
            self.variants.append(('readn', 'n', ('readn',)))
            self.variants.append(('readp', 'p', ('readp',)))
        else:
            for d in 'np':
                x, y, z = (('v', 1), ('v', 0), ('v', 2)) if d == 'n' else (('v', 0), ('v', 2), ('v', 1))
                for k1 in S.CAPS:
                    for k2 in S.CAPS:
                        self.variants.append(('capk[%s,%s]%s' % (S.LITLAB[k1], S.LITLAB[k2], d), d,
                                              ('capk', ('nat', k1), ('run', ('nat', k2), x, y), z)))
                for k in S.CAPS:
                    self.variants.append(('app[%s]%s' % (S.LITLAB[k], d), d, ('app', ('run', ('nat', k), x, y), z)))
        self._tables()

    def _tables(self):
        self.rc = []; self.nto = []
        n = self.pr.n
        for lab, d, term in self.variants:
            rc, nto = read_table(self.pr, term)
            self.rc.append(rc); self.nto.append(nto)
            L._compiled.clear()

    def size(self, i):
        return 1 if self.mach.name in ('R1', 'R2') else P.node_count(self.variants[i][2])

    def mass(self, i, depth):
        if self.mach.name in ('R1', 'R2'):
            return 1.0 / self.mach.T
        return S.cls_mass(S.shift(self.variants[i][2], depth), self.mach)


def read_table(pr, term):
    """(value code table, failed-read count table) of a read term over the 29 x 29 probe profiles: codes 0..8, 9 = TO, 10 = other
    value, 11 = stuck or over 1100 steps."""
    n = pr.n
    prog = P.frame(P.expand(term))
    rc = np.empty((n, n), np.int64); nto = np.zeros((n, n), np.int64)
    for b in range(n):
        for c in range(n):
            cd, nt, f, st, raw, _ = P.eval_prog(prog, pr.terms[b], pr.terms[c])
            if st > 1100 or (not isinstance(raw, int) and raw != 'TO') or isinstance(raw, bool):
                rc[b, c] = 11
            elif raw == 'TO':
                rc[b, c] = 9
            elif 0 <= raw <= 8:
                rc[b, c] = raw
            else:
                rc[b, c] = 10
            nto[b, c] = nt
    return rc, nto


def probe_term(mach, dirn, code, k1=383, k2=383, app=False):
    """a probe read of direction dirn with the constant of code `code`, in the machine's syntax."""
    if mach.name == 'R2':
        return ('probn' if dirn == 'n' else 'probp', ('nat', code))
    Q = const_quote(code)
    if dirn == 'n':
        run = ('run', ('nat', k2), ('v', 1), Q)
        return ('app', run, ('v', 2)) if app else ('capk', ('nat', k1), run, ('v', 2))
    run = ('run', ('nat', k2), ('v', 0), ('v', 2))
    return ('app', run, Q) if app else ('capk', ('nat', k1), run, Q)


class Probes2:
    """probe read variants (label, direction, term, rc, nto, size, mass-at-depth-1 function) for the prudent search."""

    def __init__(self, mach, caps=(383, 1500)):
        self.pr = P.probes()
        self.mach = mach
        self.items = []
        for d, code in (('n', 3), ('p', 0)):
            if mach.name == 'R2':
                self.add('probe' + d, d, probe_term(mach, d, code))
            else:
                for k1 in caps:
                    for k2 in caps:
                        self.add('probe_capk[%d,%d]%s' % (k1, k2, d), d, probe_term(mach, d, code, k1, k2))
                for k in caps:
                    self.add('probe_app[%d]%s' % (k, d), d, probe_term(mach, d, code, k, k, True))

    def add(self, lab, d, term):
        rc, nto = read_table(self.pr, term)
        L._compiled.clear()
        self.items.append(dict(label=lab, d=d, term=term, rc=rc, nto=nto, size=P.node_count(term)))

    def mass(self, it, depth):
        return S.cls_mass(S.shift(it['term'], depth), self.mach)


def cap_ok(v):
    """the cap classes used for the first read of the prudent search (R0 written-out reads): equal classes 383 / >= 1023."""
    return v[0].startswith('capk[[256,510],[256,510]]') or v[0].startswith('capk[>=1023,>=1023]') or v[0] in ('readn', 'readp')


# ====================================================================== the prudent search
def group_inline_cont(mach, leaves):
    """F1 trees with one continuation leaf and exactly one occurrence of r, for the inline spelling F1[r := READ] (the r leaf and the cont
    leaf are not counted: the first is replaced by the read, the second by the second stage): {(map, size): [mass, count, F]}."""
    out = {}
    pt = 1.0 / mach.T
    rleaf = pt * P.elias(0)
    for F, hc in S.trees(True, True, leaves):
        nc = S.occ(F, ('cont',))
        if nc != 1 or S.occ(F, S.R) != 1:
            continue
        sz = P.node_count(F) - nc - 1
        m = S.cls_mass(F, mach) / pt / rleaf
        mp = S.rmap(F)
        e = out.setdefault((mp, sz), [0.0, 0, F]); e[0] += m; e[1] += 1
    return out


def search_prudent(mach, log=True):
    pr = extend_probes()
    rd = ReadsBR(mach)
    pb = Probes2(mach)
    pt = 1.0 / mach.T
    small_leaves = [('nat', k) for k in (1, 4, 8, 0, 3, 5)] + [('nat', 12)]
    let1, _ = S.group(True, True, small_leaves, mach, False)
    let2, _ = S.group(False, True, small_leaves, mach, False)
    inl1 = group_inline_cont(mach, small_leaves)
    _, inl2 = S.group(False, True, small_leaves, mach, True)
    L1 = {}; L2 = {}; I1 = {}; I2 = {}
    for (mp, sz), (m, c, F) in let1.items():
        L1.setdefault(mp, []).append((sz, m, c, F))
    for (mp, sz), (m, c, F) in let2.items():
        L2.setdefault(mp, []).append((sz, m, c, F))
    for (mp, sz), (m, c, F) in inl1.items():
        I1.setdefault(mp, []).append((sz, m, c, F))
    for (mp, sz), (m, c, F) in inl2.items():
        I2.setdefault(mp, []).append((sz, m, c, F))
    res = {}
    t0 = time.time()
    ncls = 0

    def add(g, exact, total, m, cnt, ex, form):
        key = (g, exact, total, form)
        e = res.get(key)
        if e is None:
            res[key] = [m, cnt, ex]
        else:
            e[0] += m; e[1] += cnt
    for i, v in enumerate(rd.variants):
        if not cap_ok(v):
            continue
        for it in pb.items:
            if it['d'] != v[1]:
                continue
            for form, A, B, m1r, m2r, fac in (('let', L1, L2, rd.mass(i, 0), pb.mass(it, 1), pt ** 4), ('inline', I1, I2, rd.mass(i, 0), pb.mass(it, 0), 1.0)):
                for mp1, l1 in A.items():
                    M1 = np.array(mp1)
                    o1 = M1[rd.rc[i]]
                    cont = (o1 == -2)
                    if not cont.any():
                        continue
                    for mp2, l2 in B.items():
                        M2 = np.array(mp2)
                        o2 = M2[it['rc']]
                        out = np.where(cont, o2, o1)
                        nto = rd.nto[i] + cont * it['nto']
                        fo = (out < 0)
                        tab = (np.where(fo, 8, out).astype(np.int8), np.minimum(nto, 100).astype(np.int8), fo.astype(np.int8))
                        fam, exact = P.classify_table(tab, pr)
                        ncls += 1
                        if not exact:
                            continue
                        g = member_group(exact)
                        for (s1, mF1, c1, F1) in l1:
                            for (s2, mF2, c2, F2) in l2:
                                if form == 'let':
                                    total = 2 + s1 + 2 + s2 + rd.size(i) + it['size']
                                    ex = ('app', ('lam', S.subst(F1, ('cont',), ('app', ('lam', F2), it['term']))), v[2])
                                else:
                                    total = s1 + s2 + rd.size(i) + it['size']
                                    ex = S.subst(S.subst(F1, S.R, v[2]), ('cont',), S.subst(F2, S.R, it['term']))
                                add(g, exact, total, fac * mF1 * mF2 * m1r * m2r, c1 * c2, ex, form)
            L._compiled.clear()
        if log:
            print('prudent', mach.name, v[0], 'classified', ncls, 'elapsed %.0f' % (time.time() - t0), flush=True)
    return res


# ====================================================================== the opener templates
def _eq(var, k, flip):
    return ('eq', k, var) if flip else ('eq', var, k)


def _and(x, y):
    return ('if', x, y, ('con', 'F'))


TOK = ('con', 'TO')


def _acc(var, k, to, order, flip1, flip2):
    """acceptance of a read value: (eq var k), or with the timeout accepted: (if (eq var k) T (eq var TO)) / the other order."""
    a = _eq(var, ('nat', k), flip1)
    if to == 'n':
        return a
    b = _eq(var, TOK, flip2)
    return ('if', a, ('con', 'T'), b) if order == 0 else ('if', b, ('con', 'T'), a)


def opener_bodies(first, fb, to, read_a, read_b, let_order):
    """all spellings of the opener O<first><fb><to> in the template grammar, as (body, extra) with the reads inserted.  read_a / read_b are
    functions depth -> term (the read of next / the read of prev at binder depth `depth`)."""
    g1 = 1 if first == 'n' else 4
    g2 = 4 if first == 'n' else 1
    f = {'f': g1, 'z': 8}[fb]
    out = []
    # variables: let_order 'ab': a outer (v1), b inner (v0); 'ba': b outer (v1), a inner (v0)
    va, vb = (('v', 1), ('v', 0)) if let_order == 'ab' else (('v', 0), ('v', 1))
    for flips in itertools.product((0, 1), repeat=4):
        for conj1, conj2, pat_order in itertools.product((0, 1), repeat=3):
            t_a2 = _eq(va, ('nat', 2), flips[0]); t_b3 = _eq(vb, ('nat', 3), flips[1])
            t_b5 = _eq(vb, ('nat', 5), flips[2]); t_a0 = _eq(va, ('nat', 0), flips[3])
            c1 = _and(t_a2, t_b3) if conj1 == 0 else _and(t_b3, t_a2)
            c2 = _and(t_b5, t_a0) if conj2 == 0 else _and(t_a0, t_b5)
            for dflips in itertools.product((0, 1), repeat=2 if to == 'n' else 4):
                for dord in ((0,) if to == 'n' else itertools.product((0, 1), repeat=2)):
                    if to == 'n':
                        accs = [_acc(va, 4, 'n', 0, dflips[0], 0), _acc(vb, 1, 'n', 0, dflips[1], 0)]
                    else:
                        accs = [_acc(va, 4, 'y', dord[0], dflips[0], dflips[1]), _acc(vb, 1, 'y', dord[1], dflips[2], dflips[3])]
                    if first == 'n':
                        D = ('if', accs[0], ('nat', g1), ('if', accs[1], ('nat', g2), ('nat', f)))
                    else:
                        D = ('if', accs[1], ('nat', g1), ('if', accs[0], ('nat', g2), ('nat', f)))
                    G = ('if', c1, ('nat', 4), ('if', c2, ('nat', 1), D)) if pat_order == 0 else ('if', c2, ('nat', 1), ('if', c1, ('nat', 4), D))
                    out.append(G)
    return out


def opener_search(mach, name, caps=(383, 1500), sample_check=12, pr=None):
    """lower bound (sum of the masses of the spellings whose canonical representative classifies as `name`), shortest spelling."""
    pr = pr or extend_probes()
    first, fb, to = name[1], name[2], name[3]
    pt = 1.0 / mach.T
    if mach.name in ('R1', 'R2'):
        read_opts = [(('readn',), ('readp',), 'R')]
    else:
        read_opts = []
        for k in caps:
            read_opts.append((('capk', ('nat', k), ('run', ('nat', k), ('v', 1), ('v', 0)), ('v', 2)),
                              ('capk', ('nat', k), ('run', ('nat', k), ('v', 0), ('v', 2)), ('v', 1)), 'C%d' % k))
    total = 0.0; ncount = 0; best = None; ok_classes = []
    for ra, rb, lab in read_opts:
        for lo in ('ab', 'ba'):
            Gs = opener_bodies(first, fb, to, None, None, lo)
            # the reads at their depths: a = READn, b = READp; outer read at depth 0, inner at depth 1 (the read terms refer to me / n / p
            # by absolute index, so they are shifted by the depth)
            if lo == 'ab':
                body = lambda G: ('app', ('lam', ('app', ('lam', G), S.shift(rb, 1))), ra)
            else:
                body = lambda G: ('app', ('lam', ('app', ('lam', G), S.shift(ra, 1))), rb)
            # canonical check of the class: classify the first spelling of this (read option, let order)
            term0 = body(Gs[0])
            fam, exact, _ = P.classify_body(term0, mach, pr)
            L._compiled.clear()
            if exact != name:
                continue
            ok_classes.append((lab, lo, fam, exact))
            # spot check: random other spellings classify the same
            rng = np.random.default_rng(len(Gs))
            for j in rng.choice(len(Gs), size=min(sample_check, len(Gs)), replace=False):
                fam_j, exact_j, _ = P.classify_body(body(Gs[int(j)]), mach, pr)
                assert exact_j == name, (name, lab, lo, int(j), exact_j)
            L._compiled.clear()
            for G in Gs:
                t = body(G)
                m = S.cls_mass(t, mach)
                total += m; ncount += 1
                sz = P.node_count(t)
                if best is None or sz < best[0]:
                    best = (sz, P.to_sexpr(t))
    return dict(mass=total, count=ncount, shortest=best, classes=ok_classes)


# ====================================================================== member bodies (V4) and the report of a machine
def member_body(name, mach):
    """a canonical spelling of the member's body in the machine's syntax: P and Q via the grammar's own two-let form, O via the template,
    the T+ readers by their plain forms (read through a let)."""
    raise NotImplementedError


def search_machine(mach_name, out):
    mach = P.MACHINES[mach_name]
    t0 = time.time()
    pr = extend_probes()
    res = {'machine': mach_name, 'n_tags': mach.T}
    prud = L.run_big(search_prudent, mach)
    classes = {}
    for (g, exact, size, form), (m, c, ex) in prud.items():
        classes.setdefault(g + '|' + exact, {}).setdefault(str(size), {})[form] = [m, c, P.to_sexpr(ex)]
    res['prudent'] = classes
    op = {}
    for name in BR.NAMES_O:
        op[name] = L.run_big(opener_search, mach, name)
    res['opener'] = op
    if mach_name == 'R2':
        S.Reads = ReadsBR
        base = L.run_big(S.search, mach)
        res['t_plus'] = S.pack(base)
    res['wall'] = time.time() - t0
    json.dump(res, open(out, 'w'), default=str)
    return res


def main():
    cmd = sys.argv[1]
    if cmd == 'search':
        search_machine(sys.argv[2], sys.argv[3])
    elif cmd in ('enum', 'mc'):
        extend_probes()
        sys.argv = [sys.argv[0]] + sys.argv[1:]
        E.main()
    else:
        raise SystemExit(cmd)


if __name__ == '__main__':
    main()
