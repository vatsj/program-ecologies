"""Tests for the identity-and-tags experiment (notes/identity-tags.md §1.12)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.setrecursionlimit(1000000)
import lt_code as L
import lt_cert as C
import carrier_populations as CP
import identity_tags as IT

K = 10 ** 6
V = K // 4
_CACHE = {}


def cat(n):
    if n not in _CACHE:
        _CACHE[n] = IT.Catalogue(n, K)
    return _CACHE[n]


def tables(n):
    key = ('tab', n)
    if key not in _CACHE:
        _CACHE[key] = IT.serial_tables(cat(n))
    return _CACHE[key]


def test_counts():
    assert CP.count_by_hand(7, 23) == {1: 2, 2: 0, 3: 0, 4: 92, 5: 92, 6: 4324, 7: 21252}
    G = IT.enumerate_grammar(7, IT.atom_alphabet())
    assert {n: len(v) for n, v in G.items()} == CP.count_by_hand(7, 23)
    a = CP.count_by_hand(7, 23)
    n_sp = sum(a[n] * (1 + 2 * (n <= 6) + (n <= 5)) for n in a)
    assert n_sp == 34968
    Z = sum(a[n] * 2.0 ** -n * (1 + 2 * 0.5 * (n <= 6) + 0.25 * (n <= 5)) for n in a)
    assert abs(Z - 322.8125) < 1e-9
    c = cat(5)
    assert c.nsp == 186 + 2 * 94 + 2


def test_eq_and_tags():
    c = cat(6)
    for M in IT.MSETS:
        prog = c.term(c.spelling_of(IT.CB_X, M))
        for t in (1, 2):
            v, _ = L.evaluate(IT.tag_term(t, ('quote', prog)))
            assert v == ('T' if M & (1 << (t - 1)) else 'F'), (M, t, v)
    for p in (L.PROG_C, L.PROG_D):
        for t in (1, 2):
            assert L.evaluate(IT.tag_term(t, ('quote', p)))[0] == 'F'
    # eq: EQ cooperates only in self-play; EQ against EQ' (same run tree) defects
    eq = c.term(c.spelling_of(IT.EQ_X, 0)); eq2 = c.term(c.spelling_of(IT.EQ2_X, 0)); eqm = c.term(c.spelling_of(IT.EQ_X, 1))
    assert L.play(eq, eq, K)[0] == 'C'
    assert L.play(eq, eq2, K)[0] == 'D' and L.play(eq2, eq, K)[0] == 'D'
    assert L.play(eq, eqm, K)[0] == 'D' and L.play(eqm, eqm, K)[0] == 'C'
    # a marker changes no play of a tag-free program
    cb, cbm = c.term(c.spelling_of(IT.CB_X, 0)), c.term(c.spelling_of(IT.CB_X, 3))
    for y in (('C',), ('D',), IT.CB_X):
        for M in (0, 1):
            yy = c.term(c.spelling_of(y, M))
            assert L.play(cb, yy, K)[0] == L.play(cbm, yy, K)[0]


def test_named_hand_table():
    prod = C.Producer(host=CP.ExactHost())
    probes, cb, comp = IT.build_probes(prod, K, V)
    progs = {}
    for nm in IT.NAMED_ORDER:
        x, M = IT.NAMED[nm]
        mk = lambda c_, x=x, M=M: comp.program(x, M, c_)
        lst, _ = C.produce_list(prod, 0, mk, probes, K, V)
        progs[nm] = mk(lst)
    assert L.canon_term(progs['CB']) == L.canon_term(cb)
    assert L.canon_term(progs['XC']) == L.canon_term(dict(probes)['XC'])
    for x in IT.NAMED_ORDER:
        row = ''
        for y in IT.NAMED_ORDER:
            L.CACHE.clear()
            row += L.play(progs[x], progs[y], K)[0]
        assert row == IT.HAND[x], (x, row, IT.HAND[x])


def test_composition_lemma_R_small():
    """Composed table = whole plays: every spelling pair at n <= 4, and a sample at n <= 5 (marked pairs, twins, self)."""
    for n, sample in ((4, None), (5, 1500)):
        c = cat(n)
        A, s = tables(n)
        rng = np.random.default_rng(n)
        if sample is None:
            pairs = [(x, y) for x in range(c.nsp) for y in range(c.nsp)]
        else:
            pairs = [tuple(int(v) for v in rng.integers(0, c.nsp, 2)) for _ in range(sample)]
            for u in range(c.NU):
                if len(c.members[u]) >= 2: pairs.append(tuple(c.members[u][:2]))
        for x, y in pairs:
            L.CACHE.clear()
            r = L.play(c.term(x), c.term(y), K)[0]
            ux, uy = c.sp_unit[x], c.sp_unit[y]
            pred = s[ux] if x == y else A[ux, uy]
            assert (r == 'C') == bool(pred), (n, c.name(x), c.name(y), r, pred)


def test_lumping_identity_aware():
    c = cat(5)
    A, s = tables(5)
    lp = IT.lump(c, A, s, c.spelling_weights())
    cos = IT.class_of_spelling(lp['classes'], c.nsp)
    eqd = c.sx_dt[c.sx_index[IT.EQ_X]]
    eqs = np.nonzero(c.sp_dt == eqd)[0]
    assert len(eqs) >= 4
    assert len({int(cos[k]) for k in eqs}) == len(eqs)                     # each eq-clique spelling its own class
    assert all(len(lp['classes'][int(cos[k])]['spellings']) == 1 for k in eqs)
    cbc = [int(cos[c.spelling_of(IT.CB_X, M)]) for M in (0, 1, 2)]
    assert len(set(cbc)) == 3                                                # marked and unmarked CB separate
    # the spelling-level criterion on every merged pair of a sample of classes
    for cl in lp['classes'][:60]:
        ks = cl['spellings']
        if len(ks) < 2: continue
        x, y = ks[0], ks[1]
        ux, uy = c.sp_unit[x], c.sp_unit[y]
        zs = np.array([z for z in range(c.nsp) if z not in (x, y)])        # spelling level: z distinct from x, y
        uz = c.sp_unit[zs]
        assert np.array_equal(A[ux, uz], A[uy, uz]) and np.array_equal(A[uz, ux], A[uz, uy])
        assert s[ux] == s[uy] == A[ux, uy] == A[uy, ux]


def test_families_named():
    names = IT.NAMED_ORDER
    A = np.array([[1 if IT.HAND[x][j] == 'C' else 0 for j in range(len(names))] for x in names], np.int8)
    U, _ = CP.pay_matrix(A)
    est = [i for i, x in enumerate(names) if A[i, i] == 1 and A[i, names.index('D')] == 0]
    cl, complete, comps = IT.maximal_cliques(A, np.array(est))
    got = sorted(sorted(names[i] for i in q) for q in cl)
    want = sorted([sorted(['CB', 'MC^1', 'OF^1']), sorted(['MC^1', 'TC1^1', 'AF^1', 'OF^1']), sorted(['XC', "XC'"]),
                   ['EQ'], ["EQ'"], ['TwinD']])
    assert got == want
    q1 = {names.index(x) for x in ['CB', 'MC^1', 'OF^1']}
    q2 = {names.index(x) for x in ['MC^1', 'TC1^1', 'AF^1', 'OF^1']}
    assert {names[i] for i in q1 & q2} == {'MC^1', 'OF^1'}
    assert names.index('D^1') in IT.strict_invaders(U, names.index('OF^1'))
    assert len(IT.strict_invaders(U, names.index('MC^1'))) == 0
    assert names.index('AF^1') not in q1


def test_tilt_law():
    import identity_tags_run as R
    w = np.full(20, 1 / 20)
    t = R.Static._tilt(w, [3, 4], [0.1, 0.05])
    assert abs(t.sum() - 1) < 1e-12 and abs(t[3] - 0.1) < 1e-12 and abs(t[4] - 0.05) < 1e-12
    rest = np.delete(t, [3, 4])
    assert np.allclose(rest, rest[0]) and abs(rest.sum() - 0.85) < 1e-12
