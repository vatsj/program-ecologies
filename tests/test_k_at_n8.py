"""Analytic cut and DAG measures (src/gl_proofs.py; specs/2026-10-05-k-at-n8.md), and the GL-erasure prune of K
(src/bounded_k.py, src/k_at_n8.py).

    python3 -m pytest tests/test_k_at_n8.py -q
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import numpy as np
import gl_proofs as G

FB = 'BOX(THEM(ME))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'


def _self(xs, cut):
    th = G.Theory(); x = th.prog(xs); orc = G.Oracle(th)
    R = G.roots_for(th, x, x)
    cuts = G.cut_closure(th, [s for _, s in R]) if cut else None
    ms = G.MinSearch(th, orc, cuts=cuts)
    S = R[0][1]
    r = ms.minimize(S)
    return r, ms.dag_sizes(S)


def test_cut_anchors():
    r, d = _self(FB, False); assert r['c'] == (4, 1) and d == dict(tree=4, exact=4, subsumption=4)
    r, d = _self(FB, True); assert r['c'] == (4, 1) and d == dict(tree=4, exact=4, subsumption=4)
    r, d = _self(PB, False); assert r['c'] == (24, 5) and d['exact'] == 24 and d['subsumption'] == 15
    r, d = _self(PB, True); assert r['certified'] and r['c'] == (18, 3) and d['exact'] == 18


def test_dag_measures_hand_tree():
    a = (frozenset(), frozenset([1])); b = (frozenset([2]), frozenset([1]))      # b is a weakening of a
    leaf = lambda s: (s, 'Ax', [])
    t = ((frozenset(), frozenset([9])), 'X', [(b, 'Y', [leaf((frozenset([5]), frozenset([5])))]),
                                            (a, 'Y', [leaf((frozenset([5]), frozenset([5])))])])
    d = G.dag_measures(t)
    assert d['tree'] == 5 and d['exact'] == 4          # the two identical leaves are shared
    assert d['subsumption'] == 3                       # b is a free reference to a (a certified first)


def test_cut_matches_knuth_and_provability_n6_sample():
    """With analytic cut, iterative deepening = Knuth on the normal-form graph with cut; cut never changes
    provability (cut is admissible in GL) and never lengthens a minimal derivation."""
    L, val, hc, hd = G.box_tables(6)
    K = len(L.rep)
    rng = np.random.default_rng(7)
    checked = 0
    for c, d in rng.integers(K, size=(25, 2)):
        th = G.Theory(); x = th.prog(L.rep[c]); y = th.prog(L.rep[d]); orc = G.Oracle(th)
        R = G.roots_for(th, x, y)
        cuts = G.cut_closure(th, [s for _, s in R])
        ms1 = G.MinSearch(th, orc, cuts=cuts); ms0 = G.MinSearch(th, orc)
        g = G.Graph(th, [s for _, s in R], oracle=orc, nf=True, cuts=cuts, cap=300000, time_cap=60)
        for nm, S in R:
            r1 = ms1.minimize(S); r0 = ms0.minimize(S)
            assert (r1 is None) == (r0 is None) == (not orc.prov(S))
            if r1 is None: continue
            assert r1['certified'] and r1['c'][0] <= r0['c'][0]
            if g.complete:
                assert g.result(S) == r1['c']; checked += 1
    assert checked > 0


def test_prune_reproduces_n6_tables():
    import k_at_n8 as KN
    for b in (4, 16):
        v0, m0, _, _ = KN.ktable(6, b, prune=False, filter_first=False)
        v1, m1, _, _ = KN.ktable(6, b, prune=True, filter_first=True)
        assert (v0 == v1).all() and m1['sound_bad'] == 0
