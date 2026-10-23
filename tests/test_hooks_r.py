"""Tests for hooks Part R (notes/hooks-r.md).  Tests marked `cache` need the untracked world-K tables
(runs/detectors/K/static/ and friends) and skip without them."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
sys.setrecursionlimit(1000000)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAVE_CACHE = os.path.exists(os.path.join(ROOT, 'runs', 'detectors', 'K', 'static', 'A.npy'))
cache = pytest.mark.skipif(not HAVE_CACHE, reason='needs the untracked world-K tables')


def test_grammar_counts_and_equal_node_cost():
    import hooks_r as H
    A = H.enumerate_H(5)
    n = sum(1 for k in A for x in A[k] if H.hook_leaves(x) and H.canonical(x))
    assert n == 2 + 256 + 256          # n = 1, 4, 5 hooked spellings (scratch count (i))
    # one node per hook leaf whatever its tag or default
    for x in (('H', 1, 'C'), ('H', 2, 'D')):
        assert H.nodes_H(x) == 1
    y = ('if', ('A', (0, 'them', 'me', 'C')), ('H', 1, 'C'), ('D',))
    assert H.nodes_H(y) == 4
    assert H.resolve(y, {1: None}) == ('if', ('A', (0, 'them', 'me', 'C')), ('C',), ('D',))
    assert H.resolve(y, {1: 'D'}) == ('if', ('A', (0, 'them', 'me', 'C')), ('D',), ('D',))


def test_conflict_rule_and_keys():
    import hooks_r as H
    fl = [(1, H.SC_NONE, 0, 0, 0), (1, H.SC_SRC, 7, 1, 0), (1, H.SC_ROOT, H.RK_D, 0, 0)]
    # source beats none against spelling 7
    assert H.winner(fl, 1, H.KIND_P, 7, 0, 3) == 1
    # against another spelling, none applies (root key 'other' absent)
    assert H.winner(fl, 1, H.KIND_P, 8, 0, 3) == 0
    # at the ⌜D⌝ root the root fill beats none
    assert H.winner(fl, 1, H.KIND_D, -1, 0, 3) == 2
    # recency only: the latest applicable fill wins
    assert H.winner(fl, 1, H.KIND_D, -1, 0, 3, recency=True) == 2
    assert H.winner(fl[:2], 1, H.KIND_P, 7, 0, 3, recency=True) == 1
    # behaviour never holds at the self root (the self guard); SELF holds at same-spelling roots
    assert not H.key_holds(H.SC_BEH, 1, H.KIND_S, 3, 1, 3)
    assert H.key_holds(H.SC_BEH, 1, H.KIND_P, 4, 1, 3)
    assert H.key_holds(H.SC_SRC, H.SELF_KEY, H.KIND_P, 3, 0, 3)
    assert not H.key_holds(H.SC_SRC, H.SELF_KEY, H.KIND_P, 4, 0, 3)
    # inert fills are never applied
    inert = np.zeros((4, 6), bool); inert[:, H.SC_SRC] = True
    assert H.winner(fl, 1, H.KIND_P, 7, 0, 3, inert=inert) == 0


def test_kernel_fill_write_rule():
    import hooks_r_kern as HK
    st = HK.KState()
    st.fdict = HK.new_dicts()['fdict']
    st.FN = np.zeros(100, np.int64); st.FP = np.zeros((100, 4), np.int64); st.nfl = np.zeros(1, np.int64)
    st.LFREE = np.zeros(100, np.int64); st.LST = np.zeros(1, np.int64); st.tmp = np.zeros(8, np.int64)
    ctr = np.zeros(HK.NCT, np.int64); st.ctr = ctr
    FN, FP = st.FN, st.FP
    f = HK.fl_of(st, 0, np.zeros(8, np.int64))
    for key in range(5):                                   # FIFO beyond 4
        f = HK.fl_add(st, f, 1, 3, key, 1, 1)
    assert FN[f] == 4 and [HK.fkey(FP[f, i]) for i in range(4)] == [1, 2, 3, 4]
    assert ctr[HK.CT_EVICT] == 1
    g = HK.fl_add(st, f, 1, 3, 2, 1, 1)                    # same action: a no-op
    assert g == f
    h = HK.fl_add(st, f, 1, 3, 2, 0, 1)                    # action flips: in place, moved to the end
    assert FN[h] == 4 and HK.fkey(FP[h, 3]) == 2 and HK.fact(FP[h, 3]) == 0 and ctr[HK.CT_EVICT] == 1
    s = HK.fl_add(st, h, 1, 3, -2, 1, 0)                   # SELF key packs and unpacks
    assert HK.fkey(FP[s, 3]) == -2


def test_term_gene_site_semantics():
    """The term's CHKH, the host replay and the actual play agree on the primitive (source, conflict, root, SELF)."""
    import hooks_r as H
    import lt_cert as C
    import lt_code as L
    import detectors as DT
    H.install_hook_library()
    y = H.hooked_carrier(('H', 1, 'C'), (), (), [])
    yk = L.canon_term(DT.bare(y))

    def x_with(fills):
        return H.hooked_carrier(('H', 1, 'D'), (), (), [(a, H.fill_script(t, sc, kd)) for (t, sc, kd, a) in fills])
    h = H.HostH()
    x = x_with([(1, H.SC_SRC, yk, 'C')])
    assert h.hook_check(x, y, 'C', 1) == 'T' and C.play(x, y, H.K)[0] == 'C'
    assert C.play(x, L.PROG_D, H.K)[0] == 'D'
    x2 = x_with([(1, H.SC_SRC, yk, 'C'), (1, H.SC_NONE, 0, 'D')])
    assert C.play(x2, y, H.K)[0] == 'C'                 # source beats a later none
    x3 = x_with([(1, H.SC_ROOT, H.RK_OTHER, 'C')])
    assert C.play(x3, y, H.K)[0] == 'C' and C.play(x3, x3, H.K)[0] == 'D'
    x4 = x_with([(1, H.SC_SRC, H.SELF_TOK, 'C')])
    x4b = x_with([(1, H.SC_SRC, H.SELF_TOK, 'C'), (1, H.SC_NONE, 0, 'D')])
    assert C.play(x4, x4b, H.K)[0] == 'C' and C.play(x4, y, H.K)[0] == 'D'


@cache
def test_gate_go():
    import hooks_r_gate as G
    out = G.gate(log=lambda *a: None)
    assert out['g2']['disagreements'] == 0
    assert out['g3']['false_atoms'] == 0 and out['g3']['accepted'] > 0
    assert out['g1']['differences'] == 0
    assert out['g3_recheck']['before_vs_FB'] == 'T' and out['g3_recheck']['after_vs_FB'] == 'F'
    assert out['go']


@cache
def test_baseline_reproduces_world_k_kernel():
    """Grammar P founders without hooks: the hooked kernel equals world K's annealed kernel draw for draw."""
    import hooks_r as H
    import world_k as WK
    H.statics()
    WK.use_world('K')
    R = WK.IslandRun('wk_Snon_200_64', 0, track=True)
    X = H.HRun('B', 0)
    for _ in range(15):
        R.advance(1); X.advance(1)
        assert (R.tsp[R.slots] == X.tsp[X.slots]).all()
    assert np.abs(np.asarray(R.island_stats()) - X.island_stats()).max() == 0.0
