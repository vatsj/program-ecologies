"""Tests for the founding-legibility run (notes/founding-legibility.md §1.0): the founding pass respects the gate and
is the kernel's (= the evaluator's) production; the bare-source key's premise; the mark kernel (mode 0 identical to
the parent's kernel; marks only on completed NONE attempts); the withheld surgery; natural reproduction."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import sog_full as F
import sog_full_kern as KN
import sog_full_run as R
import founding_legibility as FL
import founding_legibility_kern as FK

R.load_costc()
SMALL = dict(I=4, N=30)


def small_cfg(name, **kw):
    c = FL.cell_cfg(name)
    c.update(SMALL)
    c.update(kw)
    return c


@pytest.fixture(scope='module')
def l1_small():
    cfg = small_cfg('L1_6')
    ev = FL.evaluator(cfg)
    base = R.Run(ev, dict(cfg, share=False), 3)
    trace = []
    ft, st = FL.founding_pass(base, trace=trace)
    return ev, base, ft, st, trace


def test_founding_pass_respects_gate(l1_small):
    ev, base, ft, st, trace = l1_small
    assert len(trace) > 0
    for s, i, k, m, b, x, y, t0, t1 in trace:
        if s == 0:
            continue
        # a worker founder never meets a copy of its own source
        assert ev.reg[base.wtypes[x]].sp != ev.reg[base.wtypes[y]].sp
    # partners are founders with empty lists (the frozen snapshot)
    for s, i, k, m, b, x, y, t0, t1 in trace:
        for ss, q in ((0, b), (1, x), (2, y)):
            if ss == s:
                continue
            tl = base.btypes if ss == 0 else base.wtypes
            assert all(len(z) == 0 for z in ev.reg[tl[q]].inv)


def test_founding_pass_is_the_evaluators_production(l1_small):
    ev, base, ft, st, trace = l1_small
    rng = np.random.default_rng(0)
    for n in rng.choice(len(trace), size=min(300, len(trace)), replace=False):
        s, i, k, m, b, x, y, t0, t1 = trace[int(n)]
        pids = [base.btypes[b], base.wtypes[x], base.wtypes[y]]
        tl = base.btypes if s == 0 else base.wtypes
        pids[s] = tl[t0]
        res = ev.productions(*pids)[s]
        assert res[1] == tl[t1], (trace[int(n)], res)


def test_founding_lists_enter_the_run(l1_small):
    ev, base, ft, st, trace = l1_small
    base.save_shared()
    cfg = small_cfg('L1_6')
    run = FL.FLRun(ev, cfg, 3, founder_seq=FL.founder_seq(base, ft))
    for i in range(cfg['I']):
        for s in range(3):
            tl = run.btypes if s == 0 else run.wtypes
            got = sorted((ev.reg[tl[int(run.pres[i, s, t])]].sp, ev.reg[tl[int(run.pres[i, s, t])]].inv,
                          int(run.counts[i, s, run.pres[i, s, t]])) for t in range(run.npres[i, s]))
            want = {}
            tlb = base.btypes if s == 0 else base.wtypes
            for kk in range(cfg['N']):
                pr = ev.reg[tlb[int(ft[s, i, kk])]]
                want[(pr.sp, pr.inv)] = want.get((pr.sp, pr.inv), 0) + 1
            assert got == sorted((a, b, c) for (a, b), c in want.items())


def test_isolated_coalition_trace():
    """Notes §1.2: in (D*, T1, T1) no T1 founder has a non-self triple; D* writes <=1/4 only."""
    ev = R.evaluator('eq', 'S')
    co = R.coalition(ev, False)
    cfg = dict(name='iso', arm='eq', mode='S', N=30, I=1, mN=0.0, forced=co, force_n=30, share=False)
    base = R.Run(ev, cfg, 1)
    base.founders = tuple(np.full((1, 30), co[s][0], np.int64) for s in range(3))
    ft, st = FL.founding_pass(base)
    assert st['no_triple_workers'] == 60
    for k in range(30):
        assert ev.reg[base.btypes[int(ft[0, 0, k])]].inv[0] == () and ev.reg[base.btypes[int(ft[0, 0, k])]].inv[1] == ()
        assert len(ev.reg[base.btypes[int(ft[0, 0, k])]].inv[2]) == 1
        for s in (1, 2):
            assert all(len(z) == 0 for z in ev.reg[base.wtypes[int(ft[s, 0, k])]].inv)


@pytest.mark.xfail(strict=True, reason='production reads the partners\' certificates (notes §1.0 item 4): the '
                                       'bare-source key of the amendment is unsafe')
def test_production_reads_sources_only():
    ev = R.evaluator('eq', 'S')
    g = ev.g
    W, B = g.roles['W'], g.roles['B']
    t1 = W['spellings'].index(F.NAMED_W['T1'])
    scab = W['spellings'].index(F.NAMED_W['scab'])
    ds = B['spellings'].index(F.NAMED_B['D*'])
    pre = R.coalition(ev, True)
    d_empty = ev.reg.get('B', ds, F.empty_inv('B'))
    d_cert = ev.reg.get('B', ds, pre[0][1])
    t1e = ev.reg.get('W', t1, F.empty_inv('W'))
    t1d = ev.reg.get('W', t1, ((), pre[1][1][1]))          # T1 holding its [D] script only
    sc = ev.reg.get('W', scab, F.empty_inv('W'))
    # same bare sources (D*, T1, scab), different partner lists: T1's [C] production must not differ
    a = ev.productions(d_empty, t1d, sc)[1]
    b = ev.productions(d_cert, t1d, sc)[1]
    assert [r[:2] for r in a[2]] == [r[:2] for r in b[2]], (a[2], b[2])


def _small_run(cls_kw, rep=2, gens=30, mode=None):
    cfg = small_cfg('N6')
    ev = FL.evaluator(cfg)
    mark = FK.new_mark_state(mode) if mode is not None else None
    run = FL.FLRun(ev, dict(cfg, **cls_kw), rep, mark=mark)
    run.prefill()
    run.run(gens)
    return run


def test_mark_mode0_equals_parent_kernel():
    a = _small_run({}, mode=None)
    b = _small_run({}, mode=0)
    # ctr[14] counts quiet checks including retries after table misses: a function of table history, not dynamics
    keep = [q for q in range(19) if q != 14]
    assert np.array_equal(a.ctr[keep], b.ctr[keep])
    for x, y in zip(a.snap, b.snap):
        assert np.array_equal(x, y)
    MK = b.mark[1]
    assert MK[FK.MK_EXAM] > 0


def test_mark_records_only_completed_none():
    run = _small_run({}, mode=1, gens=30)
    MARK, MK, LOG = run.mark
    assert len(MARK) > 0
    A = run.A
    for key in list(MARK.keys())[:5000]:
        role = key >> 62
        row = (key >> 4) & ((1 << 30) - 1)
        a = key & 15
        idx = (A['PB_IDX'] if role == 0 else A['PW_IDX'])[row, a]
        assert idx < 0
    # the mark-sensitive bound dominates the actual count
    assert MK[FK.MK_SENSB] >= MK[FK.MK_SENS] or MK[FK.MK_SENS] == 0


@pytest.mark.parametrize('at_gen', [0, FL.WITHHOLD_GEN])
def test_withheld_surgery_consistent(at_gen):
    cfg = small_cfg('L1W_3')
    run, info = FL.make_run(cfg, 4)
    run.prefill()
    if at_gen:
        run.run(at_gen)
    before = {}
    ev = run.ev
    for i in range(run.I):
        for s in range(3):
            tl = run.btypes if s == 0 else run.wtypes
            for t in range(run.npres[i, s]):
                k = int(run.pres[i, s, t]); pr = ev.reg[tl[k]]
                before[(i, s, pr.sp)] = before.get((i, s, pr.sp), []) + [pr.inv]
    res = FL.deliver_withheld(run)
    assert res['fitness_err'] < 1e-6
    if at_gen == 0:
        assert res['moved'] > 0          # founders are empty at generation 0
    for i in range(run.I):
        for s in range(3):
            assert run.counts[i, s].sum() == run.N
            tl = run.btypes if s == 0 else run.wtypes
            for t in range(run.npres[i, s]):
                pr = ev.reg[tl[int(run.pres[i, s, t])]]
                # lack rule: some pre-delivery list of this spelling on this island is contained set by set
                assert any(all(set(a) <= set(b) for a, b in zip(old, pr.inv)) for old in before[(i, s, pr.sp)])
    run.run(at_gen + 30)


def test_natural_reproduction_small():
    cfg = small_cfg('N6')
    ev = FL.evaluator(cfg)
    a = R.Run(ev, dict(cfg, share=False), 7); a.prefill(); a.run(30)
    run, info = FL.make_run(cfg, 7)
    run.prefill(); run.run(30)
    for x, y in zip(a.snap, run.snap):
        assert x.shape == y.shape
    # types are numbered by table history; compare spelling/inventory compositions
    for ci in range(int(a.st[KN.ST_CI]) + 1):
        for i in range(cfg['I']):
            for s in range(3):
                ta, ca = R.snap_comp(a, ci, i, s); tb, cb = R.snap_comp(run, ci, i, s)
                tla = a.btypes if s == 0 else a.wtypes; tlb = run.btypes if s == 0 else run.wtypes
                A_ = sorted((ev.reg[tla[int(t)]].sp, ev.reg[tla[int(t)]].inv, int(c)) for t, c in zip(ta, ca))
                B_ = sorted((ev.reg[tlb[int(t)]].sp, ev.reg[tlb[int(t)]].inv, int(c)) for t, c in zip(tb, cb))
                assert A_ == B_
    keep = [q for q in range(19) if q != 14]
    assert np.array_equal(a.ctr[keep], run.ctr[keep])
