"""Tests of src/hooks_beh.py (behavioural hooks, spec specs/2026-10-21-behavioural-hooks.md): the key family and its guardedness,
the registry programs against direct Kripke semantics, the generalized evaluator against the stored solver on the legacy
keys, and the named members' table (the launch gate)."""
import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import hooks_beh as HB
import hooks_w2 as H


@pytest.fixture(scope='module')
def B():
    return HB.Beh()


# ------------------------------------------------------------------ key family
def test_family_counts_and_bounds(B):
    F = B.KT.fam_full
    assert list(F.a[2:]) == [3, 9, 36, 174, 855, 4437]              # spellings of size s (modalized, depth <= 2)
    assert len(F.classes) == 600 and len(F.constants) == 2
    for v in F.classes:
        assert HB.modalized(v['form']) and HB.fdepth(v['form']) <= 2 and HB.fsize(v['form']) <= 7
        assert HB.fsize(v['form']) == v['size']
    assert abs(sum(v['weight'] for v in F.classes) - 1) < 1e-12
    G = B.KT.fam_noa
    assert len(G.classes) == 199
    for v in G.classes:
        assert 'a' not in HB.fname(v['form'])


def test_guardedness_every_atom_under_a_box():
    assert HB.modalized(('box', 'a')) and HB.modalized(('and', ('box', 'a'), ('not', ('box', 'c'))))
    assert not HB.modalized('a') and not HB.modalized(('or', 'a', ('box', 'c')))
    assert HB.modalized(('box', ('or', 'a', 'c')))


def test_class_weights_by_shortest_member(B):
    F = B.KT.fam_full
    w = {v['name']: v['weight'] for v in F.classes}
    z = sum(2.0 ** (-v['bits']) for v in F.classes)
    assert abs(w['[]a'] - 2.0 ** (-(np.log2(3) + 2 * np.log2(2) + 1)) / z) < 1e-12
    assert w['[]a'] > w['~[]a']


def test_no_constant_keys(B):
    for v in B.KT.fam_full.classes:
        assert v['tt'].min() != v['tt'].max()
    tautology = ('or', ('box', 'a'), ('not', ('box', 'a')))
    tt = B.KT.fam_full.ps.tt(tautology, ('a', 'c', 'd'))
    assert tt.min() == tt.max() == 1
    assert HB.fname(tautology) not in {v['name'] for v in B.KT.fam_full.classes}


def test_quotient_is_by_truth_on_all_words():
    """Two keys in one class agree on every word up to length 6 (checked directly, no truth-table machinery)."""
    F = HB.Family(HB.ATOMS, L=5)
    rng = np.random.default_rng(0)
    box = lambda f: ('box', f)
    pairs = [(('not', box('a')), ('not', box('a'))), (box(('and', 'a', 'c')), ('and', box('a'), box('c'))),
             (box(('or', 'a', ('not', 'a'))), None)]
    for f, g in pairs[:2]:
        for _ in range(300):
            w = list(rng.integers(0, 8, size=rng.integers(1, 7)))
            assert HB.eval_word(f, w) == HB.eval_word(g, w)
    # both spellings land in one class
    names = {v['name'] for v in F.classes}
    assert ('[](a & c)' in names) != ('([]a & []c)' in names)


def test_truth_tables_match_direct_semantics(B):
    ps = B.KT.ps
    rng = np.random.default_rng(1)
    ks = rng.choice(len(B.KT.keys), size=40, replace=False)
    for k in ks:
        form = B.KT.keys[k]['form']
        tt = ps.tt(form, HB.ATOMS)
        for _ in range(20):
            n = int(rng.integers(1, ps.L + 1))
            w = [int(x) for x in rng.integers(0, 8, size=n)]
            idx = ps.offs[n - 1] + int(sum(c * 8 ** (n - 1 - i) for i, c in enumerate(w)))
            assert tt[idx] == HB.eval_word(form, w)


def test_registry_programs_match_direct_semantics(B):
    """The postfix key programs advanced through the registry reproduce the direct Kripke value at every world."""
    KT = B.KT
    rng = np.random.default_rng(2)
    stack = np.zeros(32, np.int64)
    for k in rng.choice(len(KT.keys), size=60, replace=False):
        for _ in range(10):
            word = [int(x) for x in rng.integers(0, 8, size=int(rng.integers(1, 7)))]
            Bst = np.ones(KT.R, np.bool_)
            for m in range(len(word)):
                # value of key k at world m (atoms under boxes: only the past matters)
                v = HB.key_true(int(k), KT.key_prog, Bst)
                assert int(v) == HB.eval_word(KT.keys[int(k)]['form'], word[:m] + [0]), (KT.keys[int(k)]['name'], word, m)
                bv = np.array([HB._run_prog(KT.reg_prog[j], KT.reg_prog.shape[1], word[m], Bst, stack) == 1 for j in range(KT.R)])
                Bst = Bst & bv


def test_key_requirements_cover_programs(B):
    KT = B.KT
    for k in KT.keys:
        refs = {t - HB.T_REG for t in k['prog'] if t >= HB.T_REG}
        req = {int(x) for x in KT.key_req[k['id']] if x >= 0}
        assert refs <= req
        for j in req:
            assert {t - HB.T_REG for t in KT.reg_prog[j] if t >= HB.T_REG} <= req


# ------------------------------------------------------------------ the evaluator against the stored solver (legacy keys)
def _random_fills(rng, tags, NI=50):
    nf = int(rng.integers(0, 5))
    fills = []
    for _ in range(nf):
        t = int(rng.integers(2))
        sc = int(rng.integers(4))
        key = 0 if sc in (0, 1) else (int(rng.integers(NI)) if sc == 2 else int(rng.integers(10)))
        fills.append(H.fcode(int(rng.integers(2)), t, sc, int(rng.integers(4)), key))
    return fills


def test_evaluator_reproduces_stored_solver_on_legacy_keys(B):
    L = B.Lx
    rng = np.random.default_rng(3)
    hooked = [i for i in range(len(L.base)) if L.b_tags[i] > 0]
    active = np.ones((4, 4), np.bool_)
    rs = np.zeros((2, B.R), np.bool_)
    for trial in range(400):
        bx = int(rng.choice(hooked if rng.random() < 0.8 else len(L.base)))
        by = int(rng.choice(hooked if rng.random() < 0.8 else len(L.base)))
        recency = int(rng.integers(2))
        lx = int(rng.integers(50)); ly = int(rng.integers(50))
        fx = _random_fills(rng, L.b_tags[bx]); fy = _random_fills(rng, L.b_tags[by])
        gx = np.zeros(4, np.int64); gx[:len(fx)] = fx; gy = np.zeros(4, np.int64); gy[:len(fy)] = fy
        old = H.eval_match(*L.arrays()[:12], L.iC, L.iD, bx, H.spec_of(gx, len(fx), int(L.b_tags[bx]), active, recency, -1),
                           H.spec_of(gx, len(fx), int(L.b_tags[bx]), active, recency, ly),
                           H.spec_of(gx, len(fx), int(L.b_tags[bx]), active, recency, lx), by,
                           H.spec_of(gy, len(fy), int(L.b_tags[by]), active, recency, -1),
                           H.spec_of(gy, len(fy), int(L.b_tags[by]), active, recency, lx),
                           H.spec_of(gy, len(fy), int(L.b_tags[by]), active, recency, ly))
        sp = lambda g, n, b, c: int(HB.spec_of_beh(g, n, int(L.b_tags[b]), active, recency, c))
        new = HB.eval_match_beh(*L.arrays()[:12], L.iC, L.iD, *B.KT.arrays()[:2], B.KT.arrays()[2], False, bx,
                                sp(gx, len(fx), bx, -1), sp(gx, len(fx), bx, ly), sp(gx, len(fx), bx, lx), by,
                                sp(gy, len(fy), by, -1), sp(gy, len(fy), by, lx), sp(gy, len(fy), by, ly), rs)
        assert (old[0], old[1]) == (new[0], new[1]), (trial, old, new)


# ------------------------------------------------------------------ the named members (launch gate)
box = lambda f: ('box', f)
REF = {'FairBot': ('D', [(box('a'), 1)]), 'TrustingBot': ('C', [(box(('not', 'a')), 0)]),
       'PrudentBot': ('D', [(('and', box('a'), box(('not', 'd'))), 1)]), 'GodelPredator': ('C', [(box('a'), 0)]),
       'CooperateBot': ('C', []), 'DefectBot': ('D', [])}


def test_named_table_solver_equals_independent_reference(B):
    N = HB.named_programs(B)
    for x in N:
        for y in N:
            ax, ay, _ = B.play(*N[x], *N[y])
            rx, ry = HB.ref_match(REF[x], REF[y])
            assert rx[-6:] == [rx[-1]] * 6 and ry[-6:] == [ry[-1]] * 6
            assert (ax, ay) == (rx[-1], ry[-1]), (x, y)


def test_named_table_by_hand(B):
    """The entries the RE derived by hand agree with the solver, except PrudentBot against FairBot (see the gate)."""
    N = HB.named_programs(B)
    out = lambda x, y: ''.join('CD'[1 - v] for v in B.play(*N[x], *N[y])[:2])
    assert out('FairBot', 'TrustingBot') == 'DC'
    assert out('GodelPredator', 'GodelPredator') == 'CC'
    assert out('FairBot', 'GodelPredator') == 'DC'
    assert out('PrudentBot', 'CooperateBot') == 'DC'
    assert out('PrudentBot', 'TrustingBot') == 'DC'
    assert out('FairBot', 'FairBot') == 'CC'
    assert out('FairBot', 'DefectBot') == 'DD'


def test_launch_gate_disagreement_prudentbot_fairbot(B):
    """THE GATE.  The spec's hand derivation says PrudentBot (key box a and box not d, level PA) cooperates with FairBot.  The
    solver and the independent reference both say mutual defection: FairBot cooperates with DefectBot at world 0 (vacuous
    box), so d = (C, D, D, ...) for FairBot and box not d fails from world 1.  Recorded as a test so the discrepancy is
    pinned; it passes while the gate fails."""
    N = HB.named_programs(B)
    assert B.play(*N['PrudentBot'], *N['FairBot'])[:2] == (0, 0)
    assert B.play(*N['PrudentBot'], *N['PrudentBot'])[:2] == (0, 0)
    rx, ry = HB.ref_match(REF['PrudentBot'], REF['FairBot'], 8)
    assert ''.join('CD'[1 - v] for v in rx) == 'CDDDDDDD' and ''.join('CD'[1 - v] for v in ry) == 'CCDDDDDD'


def test_level_one_reading_agrees_with_the_hand_derivation():
    """With the d-clause one level up (box1, ignoring world 0) PrudentBot cooperates with FairBot and with itself."""
    pb1 = ('D', [(('and', box('a'), ('box1', ('not', 'd'))), 1)])
    fb = REF['FairBot']
    rx, ry = HB.ref_match(pb1, fb)
    assert rx[-1] == 1 and ry[-1] == 1
    rx, ry = HB.ref_match(pb1, pb1)
    assert rx[-1] == 1 and ry[-1] == 1
    rx, ry = HB.ref_match(pb1, REF['CooperateBot'])
    assert rx[-1] == 0 and ry[-1] == 1


def test_no_one_fill_prudent_program_in_the_level_pa_family(B):
    """Over every family key (and the legacy open keys) and both defaults, no program HOOK(0, d) + (key -> action) is D against
    CooperateBot and DefectBot and C against FairBot and against a copy of itself."""
    N = HB.named_programs(B)
    for base, act in ((B.base('HOOK(0,D)'), 1), (B.base('HOOK(0,C)'), 0)):
        for k in B.KT.keys:
            if k['family'] == 'legacy' and k['id'] < 8:
                continue
            sp = B.spec([H.fcode(act, 0, H.BEH, H.SEEDED, k['id'])], 1)
            s = ''.join('CD'[1 - B.play(base, sp, *N[q])[0]] for q in ('CooperateBot', 'DefectBot', 'FairBot'))
            s += 'CD'[1 - B.play(base, sp, base, sp)[0]]
            assert s != 'DDCC', k['name']
