"""Tests for the Pangaea run (notes/pangaea.md §1.7).  Tests needing provenance's untracked cached tables skip when
they are absent."""
import gzip
import json
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import pangaea_kern as PK

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAVE_CACHE = os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'sets.npz')) and \
    os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'static', 'meta.pkl'))
needs_cache = pytest.mark.skipif(not HAVE_CACHE, reason='provenance cached tables absent')


def test_dominant_network_constructed():
    # types 0..4: 0,1 mutual (network A, counts 5+5), 2,3 mutual (network B, counts 6+1), 4 a defector (count 50)
    M = np.zeros((5, 5), bool)
    for a, b in [(0, 0), (1, 1), (0, 1), (2, 2), (3, 3), (2, 3)]:
        M[a, b] = M[b, a] = True
    c = np.array([5.0, 5.0, 6.0, 1.0, 50.0])
    K = np.arange(5, dtype=np.int64)
    S = np.array([0, 1, 2, 3], np.int64)
    net = sorted(PK.dominant_network(M, S, c, K).tolist())
    assert net == [0, 1]                       # compatible mass 10 beats 7 although type 2 is the largest cooperator
    # a non-clique neighbourhood: 0 mutual with 1 and 2, but 1 and 2 not mutual -> the larger joins
    M2 = np.zeros((3, 3), bool)
    for a, b in [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2)]:
        M2[a, b] = M2[b, a] = True
    net = PK.dominant_network(M2, np.arange(3, dtype=np.int64), np.array([4.0, 3.0, 2.0]), np.arange(3, dtype=np.int64))
    assert sorted(net.tolist()) == [0, 1]


def test_block_seeds_distinct():
    s = 123456789
    seeds = {PK.block_seed(s, b) for b in range(1, 70)}
    assert len(seeds) == 69 and s not in seeds


@needs_cache
def test_founders_identical_and_nested():
    import pangaea as PG
    import provenance_run as PR
    LS = PR.lot_static('ext')
    for T in PG.TOTALS:
        lst = PG.base_list(T, 3, LS)
        perm = PG.permutation(T, 3)
        ms = None
        for (N, I) in PG.GEOMS[T]:
            a = PG.partition(lst, N, I, perm)
            m = np.sort(a.ravel())
            assert ms is None or np.array_equal(m, ms)
            ms = m
        for (N1, I1), (N2, I2) in zip(PG.GEOMS[T][:-1], PG.GEOMS[T][1:]):
            a1 = PG.partition(lst, N1, I1, perm); a2 = PG.partition(lst, N2, I2, perm)
            k = N2 // N1
            for i in range(I2):
                assert np.array_equal(np.sort(a2[i]), np.sort(a1[i * k:(i + 1) * k].ravel()))
        pl = PG.proportional(lst, T, 3, LS)
        ch = lst != pl
        assert np.isin(lst[ch], LS['Q']).all() and not np.isin(pl, LS['Q']).any()


@needs_cache
def test_kernel_equals_provenance_below_100():
    """For r <= 100 the copied kernel reproduces provenance's segment exactly (same state after 30 generations)."""
    import pangaea as PG
    import provenance as PV
    a = PG.PGRun('pg_L_200_64_r100', 7)
    b = PG.PGRun('pg_L_200_64_r100', 7)
    a.advance(30)
    st, LS = b.LS['st'], b.LS
    g = PV.segment(0, 30, b.seed, b.N, 0.3, b.mN / b.N, b.r, b.slots, b.counts, b.paysum, b.pres, b.npres, b.pos,
                   b.spcount, b.d, b.tunit, b.trule, b.tsp, b.tanc, b.ntv, st['utau'], st['BLC'], st['BLD'],
                   st['SINGLE'], st['APP'], LS['PRODC'], LS['PD'], st['KIND'], st['NAT'], st['CHC'], st['CHD'],
                   st['UVt'], b.A, b.selfa, LS['OSV'], LS['SPO'], LS['capable'], LS['COSTS'], b.ctr, b.steps_rule,
                   b.wn, b.wenc, b.wsp, b.wcode, b.wsid, b.ckey, b.cval, b.ncache, b.plog, b.hist_wait, b.hist_acq,
                   b.hist_steps, b.hist_cens, b.nprod, LS['ident'], LS['spo_unit'], b.tset, b.uns, b.rulecount,
                   b.enc_exp, b.skip, LS['FUT'], b.fcount, b.enc_futile, b.err)
    assert g == 30 and np.array_equal(a.slots, b.slots) and np.array_equal(a.ctr, b.ctr)


@needs_cache
def test_reproduces_stored_scaling_row():
    import pangaea_run as PRN
    import realizable_scaling_run as RSR
    stored = json.load(gzip.open(os.path.join(ROOT, 'runs', 'realizable_scaling', 'lottery_srest.json.gz')))
    s = [x for x in stored if x['cell'] == 'rs_Snon_50_64_m1' and x['rep'] == 1][0]
    r = PRN._validate_job(('rs_Snon_50_64_m1', 1))
    ta = {t[0]: t for t in r['trace']}
    common = [g for g in (t[0] for t in s['trace']) if g in ta and g <= 2000]
    assert len(common) > 30
    for t in s['trace']:
        if t[0] in ta and t[0] <= 2000:
            assert all(abs(x - y) < 1e-9 for x, y in zip(ta[t[0]], t))


@needs_cache
def test_merge_equals_fresh_initialization():
    import pangaea as PG
    import provenance as PV
    R = PG.PGRun('pg_L_100_128_r100_ff200', 2)
    R.advance(20)
    R.merge(99)
    cnt = np.zeros_like(R.counts); np.add.at(cnt[0], R.slots[0], 1)
    ps = np.zeros_like(R.paysum)
    PV.init_paysum(cnt, ps, R.pres, R.npres, R.tunit, R.tsp, R.A, R.selfa)
    assert np.array_equal(cnt, R.counts) and np.allclose(ps, R.paysum)
    assert R.I == 1 and R.N == 12800 and R.rulecount.sum() == 12800
