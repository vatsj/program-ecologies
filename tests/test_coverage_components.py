"""Tests for the coverage-components run (notes/coverage-components.md §1.0): the static partition, the masks, the
lack rule under grants, and draw-for-draw equivalence of the empty and full masks (mark on and off) and of the minus
cells' two modes (Lemma P)."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import sog_full as F
import sog_full_run as R
import founding_legibility as FL
import founding_legibility_kern as FK
import coverage_components as CC

R.load_costc()
G = R.grammar('id')
SMALL = dict(I=4, N=30)
GENS = 60


def support_trees(role, reps=range(3)):
    """Run trees of the founders of the given replicates at (100, 64)."""
    r = G.roles[role]
    cum = np.cumsum(G.mass(role))
    out = set()
    for rep in reps:
        rng = np.random.default_rng([rep, 100, 64, 20261013])
        uB = rng.random((64, 100)); u1 = rng.random((64, 100)); u2 = rng.random((64, 100))
        us = (uB,) if role == 'B' else (u1, u2)
        for u in us:
            sps = np.minimum(np.searchsorted(cum, u * cum[-1]), len(cum) - 1).ravel()
            out |= set(int(r['tau'][s]) for s in sps)
    return sorted(out)


# ---------------------------------------------------------------- the static partition
@pytest.mark.parametrize('role', ['W', 'B'])
def test_partition(role):
    trees = list(range(len(G.roles['W']['members']))) if role == 'W' else support_trees('B')
    for tk in trees:
        c = CC.classify(G, role, tk)
        _, per = G.hlist(role, tk)
        for A in F.FAM[role]:
            rows = c[A]
            assert [r['i'] for r in rows] == list(range(len(per[A])))
            labs = [r['label'] for r in rows]
            assert all(l in CC.LABELS for l in labs)
            assert labs.count('canon') <= 1
            S3 = {r['i'] for r in rows if r['S3']}
            comps = {r['i'] for r in rows if r['label'] in CC.COMPS}
            canon = {r['i'] for r in rows if r['label'] == 'canon'}
            assert canon <= S3
            assert canon | comps == set(range(len(rows))) and not (canon & comps)
            assert S3 | comps == set(range(len(rows)))          # the amendment's test
            if role == 'B':
                assert not any(l == 'd' for l in labs)
                assert all(r['live'] is False for r in rows if r['label'] == 'c')
        if role == 'W':
            pinv = R.producible_inv(G, tk)
            for si, A in enumerate(F.FAM['W']):
                assert set(pinv[si]) == {r['i'] for r in c[A] if r['S3']}


def _labs(role, name):
    x = (F.NAMED_W if role == 'W' else F.NAMED_B)[name]
    sp = G.roles[role]['spellings'].index(x)
    return CC.labels_of(G, role, int(G.roles[role]['tau'][sp]))


def test_named():
    assert _labs('W', 'T1') == (('a',), ('canon',))
    assert _labs('W', 'R') == (('canon',), ('a',))
    assert _labs('W', 'U') == (('b', 'canon'), ('canon',))
    assert _labs('W', 'U_eq') == (('d', 'canon'), ('d',))
    assert _labs('W', 'XM') == (('d',), ('b', 'canon'))
    assert _labs('B', 'D*') == (('a', 'a'), ('a',), ('b', 'canon'))
    assert _labs('B', 'B_eq') == (('a',), ('a',), ('canon',))


# ---------------------------------------------------------------- masks
def test_masks():
    for role in ('W', 'B'):
        trees = support_trees(role, reps=[0])[:400]
        for tk in trees:
            labs = CC.labels_of(G, role, tk)
            full = F.full_inv(G, role, tk)
            for X in CC.COMPS:
                for kind in ('plus', 'minus', 'randplus', 'randminus'):
                    m = CC.Mask('t', kind, X, seed=7).bind(G)
                    Gs, Xs = m.sets(role, tk)
                    for si, ls in enumerate(labs):
                        comp = {i for i, l in enumerate(ls) if l == X}
                        allx = set(range(len(ls)))
                        if kind == 'plus':
                            assert Gs[si] == comp and not Xs[si]
                        elif kind == 'minus':
                            assert Gs[si] == allx - comp and Xs[si] == comp
                        else:
                            d = Gs[si] if kind == 'randplus' else Xs[si]
                            assert not (d & comp)
                            assert all(ls[i] != 'canon' for i in d)
                            if kind == 'randminus':
                                assert Gs[si] == allx - d
            assert CC.Mask('f', 'full').bind(G).grant_inv(role, tk) == full
            assert CC.Mask('e', 'empty').bind(G).grant_inv(role, tk) == F.empty_inv(role)


def test_pairs():
    m = CC.mask_for('plus_ab').bind(G)
    for tk in support_trees('B', reps=[0])[:200]:
        labs = CC.labels_of(G, 'B', tk)
        Gs, _ = m.sets('B', tk)
        for si, ls in enumerate(labs):
            assert Gs[si] == {i for i, l in enumerate(ls) if l in ('a', 'b')}


# ---------------------------------------------------------------- the lack rule under grants
def _named_pid(ev, role, name, inv):
    x = (F.NAMED_W if role == 'W' else F.NAMED_B)[name]
    sp = G.roles[role]['spellings'].index(x)
    return ev.reg.get(role, sp, inv)


def _dstar_code(p14, p0):
    code = ['F'] * 8
    code[F.PROBE_ATOMS.index(F.P1_14S[1])] = 'T' if p14 else 'F'
    code[F.PROBE_ATOMS.index(F.P1_0S[1])] = 'T' if p0 else 'F'
    return tuple(code) + (False, False, False)


def test_lack_rule_plus_and_minus():
    evp = CC.MaskEvaluator(G, 'eq', 'S', CC.KI, CC.mask_for('plus_a'))
    x = F.NAMED_B['D*']; sp = G.roles['B']['spellings'].index(x); tk = int(G.roles['B']['tau'][sp])
    b = evp.reg.get('B', sp, evp.mask.grant_inv('B', tk))
    assert evp.lacking(evp.reg[b]) == [True, True, True]          # the grant never suppresses production
    att = evp.prod_boss(b, _dstar_code(True, False))                 # the 1/2 path: >=1/4, =1/2 granted, <=1/4 none
    idx = {si: i for si, i, _, _ in att}
    assert idx[0] is None and idx[1] is None and idx[2] is None
    att0 = evp.prod_boss(b, _dstar_code(False, False))               # the default path: <=1/4 canon is found
    idx0 = {si: i for si, i, _, _ in att0}
    assert idx0[2] is not None and idx0[0] is None
    # minus (b): the 1/4-path <=1/4 script is barred
    evm = CC.MaskEvaluator(G, 'eq', 'S', CC.KI, CC.mask_for('minus_b'))
    bm = evm.reg.get('B', sp, F.empty_inv('B'))
    att = evm.prod_boss(bm, _dstar_code(False, True))
    idx = {si: i for si, i, _, _ in att}
    assert idx[2] is None
    k = [v for kk, v in evm.kinds.items() if kk[0] == 'B']
    assert any('barred' in v for v in k)
    # union semantics in produce
    w = _named_pid(evp, 'W', 'T1', ((0,), ()))
    nw, rec = evp.produce(w, [(1, 0, 10, ())], [0] * 5, 0)
    assert evp.reg[nw].inv == ((0,), (0,))


# ---------------------------------------------------------------- draw-for-draw equivalence
def comp_seq(run):
    st, sc, sn = run.snap
    tl = (run.btypes, run.wtypes, run.wtypes)
    out = []
    for ci in range(int(run.st[KN_ST_CI()]) + 1):
        row = []
        for i in range(run.I):
            for s in range(3):
                n = int(sn[ci, i, s])
                row.append(tuple(sorted(((run.ev.reg[tl[s][int(st[ci, i, s, t])]].sp,
                                          run.ev.reg[tl[s][int(st[ci, i, s, t])]].inv), int(sc[ci, i, s, t]))
                                        for t in range(n))))
        out.append(tuple(row))
    return out


def KN_ST_CI():
    import sog_full_kern as KN
    return KN.ST_CI


def small_cfg(mode, name='t'):
    return dict(name=name, arm='eq', mode=mode, N=SMALL['N'], I=SMALL['I'], mN=1.0, K=CC.KI)


@pytest.fixture(scope='module')
def ref_runs():
    out = {}
    evS = R.evaluator_k('eq', 'S', CC.KI)
    evH = R.evaluator_k('eq', 'H', CC.KI)
    for rep in (0, 1):
        r = R.Run(evS, small_cfg('S'), rep); r.prefill(); r.run(GENS)
        out[('S', rep)] = r
        r = FL.FLRun(evS, small_cfg('S'), rep, mark=FK.new_mark_state(1)); r.prefill(); r.run(GENS)
        out[('Smark', rep)] = r
        r = R.Run(evH, small_cfg('H'), rep); r.prefill(); r.run(GENS)
        out[('H', rep)] = r
    return out


def _mrun(cell, rep, mode, mark):
    m = CC.mask_for(cell)
    ev = CC.evaluator(m, mode, CC.KI)
    mk = FK.new_mark_state(1) if mark else None
    r = CC.MaskRun(ev, small_cfg(mode, cell), rep, mark=mk)
    r.prefill(); r.run(GENS)
    return r


@pytest.mark.parametrize('rep', [0, 1])
def test_empty_mask_is_S3(ref_runs, rep):
    a = _mrun('S3', rep, 'S', False)
    b = ref_runs[('S', rep)]
    assert b.ctr[2] > 0 and b.ctr[7] > 0                           # production happened in the reference
    assert comp_seq(a) == comp_seq(b)
    assert [v for k, v in enumerate(a.ctr) if k != 14] == [v for k, v in enumerate(b.ctr) if k != 14]
    a = _mrun('S3', rep, 'S', True)
    b = ref_runs[('Smark', rep)]
    assert comp_seq(a) == comp_seq(b)
    assert [v for k, v in enumerate(a.ctr) if k != 14] == [v for k, v in enumerate(b.ctr) if k != 14]
    assert list(a.mark[1]) == list(b.mark[1])


@pytest.mark.parametrize('rep', [0, 1])
def test_full_mask_is_H(ref_runs, rep):
    ref = comp_seq(ref_runs[('H', rep)])
    assert comp_seq(_mrun('Hfull', rep, 'H', False)) == ref
    for mark in (False, True):
        a = _mrun('Hfull', rep, 'S', mark)
        assert comp_seq(a) == ref
        assert a.ctr[2] == 0 and a.ctr[7] == 0                     # no production ever found a new script


@pytest.mark.parametrize('cell', ['minus_b', 'minus_a', 'rminus_b'])
def test_lemma_P(cell):
    a = _mrun(cell, 0, 'H', False)
    b = _mrun(cell, 0, 'S', True)
    assert comp_seq(a) == comp_seq(b)
    assert b.ctr[2] == 0 and b.ctr[7] == 0


def test_plus_cell_runs_and_only_adds():
    """A plus cell: every individual holds its grant at all times (lists only grow), production adds non-granted
    scripts only."""
    r = _mrun('plus_b', 0, 'S', True)
    ev = r.ev
    st, sc, sn = r.snap
    for ci in range(int(r.st[KN_ST_CI()]) + 1):
        for i in range(r.I):
            for s in range(3):
                tl = r.btypes if s == 0 else r.wtypes
                for t in range(int(sn[ci, i, s])):
                    pr = ev.reg[tl[int(st[ci, i, s, t])]]
                    Gs, _ = ev.mask.sets(pr.role, pr.tk)
                    for si, idxs in enumerate(pr.inv):
                        assert Gs[si] <= set(idxs)
                        assert len(set(idxs) - Gs[si]) <= 1


def test_control_q():
    """The hard-coded inclusion probabilities of the complement controls equal their definition (founders 0-19)."""
    import coverage_components_run as CR
    q = CR.control_q(G)
    for role in ('W', 'B'):
        for X in CC.COMPS:
            assert abs(q[role][X]['q'] - CC.CONTROL_Q[role][X]) < 1e-5
