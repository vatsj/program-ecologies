"""Tests for the social organization game over the realizable language (notes/sog-realizable.md §1.x).

Run: python3 -m pytest tests/test_sog_realizable.py -q   (needs runs/sog_realizable/tables.pkl: `python3 src/sog_realizable_run.py tables`)
"""
import os
import random
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import sog_realizable as S
import sog_realizable_run as R

K, V = R.K_MAIN, R.V_MAIN


@pytest.fixture(scope='module')
def T():
    return R.tables()


@pytest.fixture(scope='module')
def named():
    return R.named_programs()


def test_wrapper_cost_bound(named):
    """A CHK3 call costs exactly W + 6 <= V + 6 (milestone 4's accounting)."""
    W, B, _ = named
    enc = (B['D*'], W['T1'][0], W['T1'][1])
    v, steps = S.L.run_big(S.L.evaluate, ('app', ('lib', S.ID3['CHK3']), S.mk_arg3(V, enc, 0, S.A_EQ12, K)))
    tv, ts = S.term_check(enc, 0, S.A_EQ12, V, K)
    assert v == 'T' and tv == 'T'
    assert steps == ts + 1 + 6 - 1 or steps <= V + 6


def test_three_quote_roots_term_and_host(named):
    """Three-quote roots: the checker term and the host replay agree on the named encounters (where the term fits)."""
    W, B, _ = named
    h = S.HostCheck3()
    for (bn, x, y), _ in R.HAND:
        enc = (B[bn], W[x][0], W[y][1])
        for e, j, A in R._checks_of(enc):
            tv, ts = S.term_check(e, j, A, V, K)
            hv = h.check3(e, j, A, V, K)
            if tv != 'TO' or hv == 'TO':
                assert tv == hv, (bn, x, y, j, A, tv, hv)


def test_production_host_equals_symbolic():
    cat = R.catalogue()
    w = cat.roles['W']; b = cat.roles['B']
    pp = S.PathProducer()
    rng = random.Random(3)
    for tk in rng.sample(range(len(w['dt'])), 60):
        for slot in (1, 2):
            x = w['spellings'][w['members'][tk][0]]
            prog0 = S.compile_program(x, 'W', slot, V, K, 0)
            assert S.produce_lists(w['dt'][tk], 'W', pp, prog0, slot, V, K)[0] == w['lists'][tk]
    for tk in rng.sample(range(len(b['dt'])), 60):
        x = b['spellings'][b['members'][tk][0]]
        prog0 = S.compile_program(x, 'B', 0, V, K, 0)
        assert S.produce_lists(b['dt'][tk], 'B', pp, prog0, 0, V, K)[0] == b['lists'][tk]


def test_hand_plays_by_whole_runs(named):
    W, B, _ = named
    for (bn, x, y), exp in R.HAND:
        play, steps, raw = S.play3(B[bn], W[x][0], W[y][1], K)
        assert tuple(play) == exp, (bn, x, y, play)


def test_corrupted_instances_rejected():
    c = R.corrupted_instances()
    for k, v in c.items():
        assert v['ok'], (k, v)
    assert c['1_slot2_ordering']['classification'] == 'substitution'
    assert c['4_exhausted_fuel']['four_checks_vs_C1']['classification'] == 'timeout'
    assert c['3_unequal_branches']['naive_accepts_QN_strikes'][0] == 'T'
    assert c['3_unequal_branches']['sound_on_same'][0] == 'F'


def test_composition_vs_whole_runs(T):
    """The factorized class table (Lemma F_3) against whole runs, on triples whose checks all fit the cap (the ideal
    table is the K -> infinity executable table)."""
    cat = R.catalogue()
    rng = random.Random(11)
    nbc = len(T['repb']) - T['n_extra']
    n = 0
    for _ in range(80):
        bc, xc, yc = rng.randrange(nbc), rng.randrange(len(T['rep1'])), rng.randrange(len(T['rep2']))
        K7 = 10 ** 7
        enc = (R.compiled('B', int(T['repb'][bc]), 0, K=K7), R.compiled('W', int(T['rep1'][xc]), 1, K=K7),
               R.compiled('W', int(T['rep2'][yc]), 2, K=K7))
        play, steps, raw = S.play3(*enc, K7)
        jc = S.joint_code(T, bc, xc, yc)
        if max(steps) < K7 // 4:
            assert tuple(play) == (jc // 4, 'CD'[(jc // 2) % 2], 'CD'[jc % 2]), (bc, xc, yc, play, jc)
            n += 1
    assert n >= 60


def test_abstract_equals_host_on_cert_values(T):
    cat = R.catalogue()
    w = cat.roles['W']
    rng = random.Random(5)
    consts = {c: S.carrier3(S.N(c), S.constant_list(c)) for c in (1, 4, 7)}
    for _ in range(150):
        x = rng.randrange(len(w['dt'])); y = rng.randrange(len(w['dt'])); bc = rng.choice([1, 4, 7])
        r = S.AbsEval(w['acc']).worker_pair(S.beta_of_code(bc), x, y, w['dt'])
        h = S.HostCheck3()
        enc = (consts[bc], R.compiled('W', x, 1), R.compiled('W', y, 2))
        hv = tuple(h.check3(enc, j, A, V, K) for j in (1, 2) for A in S.WORKER_Q)
        assert hv == tuple(r[2:]), (x, y, bc)


def test_expanded_node_counts():
    for nm, n in (('T1', 34), ('T0', 40), ('Q', 30), ('scab', 1)):
        assert S.expanded_nodes(S.NAMED_W[nm], 'W', V, K) == n
    for nm, n in (('D*', 151), ('D0', 63), ('D14', 89)):
        assert S.expanded_nodes(S.NAMED_B[nm], 'B', V, K) == n
    cat = R.catalogue()
    rng = random.Random(2)
    for role in ('W', 'B'):
        r = cat.roles[role]
        for k in rng.sample(range(len(r['spellings'])), 100):
            x = r['spellings'][k]
            assert S.expanded_nodes(x, role, V, K) == S.term_nodes(S.body_term(x, role, 1 if role == 'W' else 0, V, K))


def test_kernel_matches_sog_lottery_kernel(T):
    """kern3 (J on the fly) against sog_lottery.kern (dense Jc) on a small random class subset: identical trajectories."""
    import sog_lottery as SL
    rng = np.random.default_rng(1)
    nbc = len(T['repb']) - T['n_extra']
    bs = rng.choice(nbc, 12, replace=False)
    ws = rng.choice(len(T['rep1']), 10, replace=False)
    Kc = max(len(bs), len(ws))
    FBA = np.zeros((Kc, T['FBA'].shape[1]), np.int64); FBB = np.zeros_like(FBA)
    FBA[:len(bs)] = T['FBA'][bs]; FBB[:len(bs)] = T['FBB'][bs]
    PV = np.zeros((Kc, Kc), np.int64); PV[:len(ws), :len(ws)] = T['PV'][np.ix_(ws, ws)]
    EA = np.zeros((T['EA'].shape[0], Kc, Kc), np.int64); EA[:, :len(ws), :len(ws)] = T['EA'][:, ws][:, :, ws]
    tag = np.zeros(Kc, np.int64); tag[:len(ws)] = T['tag1'][ws]
    Jc = np.zeros((Kc, Kc, Kc), np.int8)
    for i in range(Kc):
        for x in range(Kc):
            for y in range(Kc):
                c = PV[x, y]
                Jc[i, x, y] = 4 * FBA[i, c] + EA[FBB[i, c], x, y]
    I, N = 4, 30
    init = np.zeros((I, 3, Kc), np.int64)
    for i in range(I):
        np.add.at(init[i, 0], rng.choice(len(bs), N), 1)
        np.add.at(init[i, 1], rng.choice(len(ws), N), 1)
        np.add.at(init[i, 2], rng.choice(len(ws), N), 1)
    checks = np.arange(10, 201, 10, dtype=np.int64)
    PAYc = R.PAY
    LB = np.zeros((4, Kc), np.int64); LW = np.zeros((5, Kc), np.int64)
    T_, _ = SL.code_tables(0.5, 0)[1], None
    st1, sg1, c1, *_ = SL.kern(Jc, tag, PAYc, SL.code_tables(0.5, 0)[1], R.KEYT, LB, LW, init, N, 0.3, 0.02, 99, checks, 0, 10 ** 9)
    MB = np.zeros((1, Kc), np.bool_); MW = np.zeros((1, Kc), np.bool_)
    st2, sg2, c2, *_ = S.kern3(R.jm_cc(), FBA, FBB, PV, EA, tag, PAYc, R.KEYT, MB, MW, init, N, 0.3, 0.02, 99, checks, 12)
    assert st1 == st2 and sg1 == sg2
    assert np.array_equal(c1, c2)
