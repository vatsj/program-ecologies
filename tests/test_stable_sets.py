"""Tests for stable sets on islands (notes/stable-sets-on-islands.md §1.14)."""
import os
import sys
import itertools

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import stable_sets as SS
import dollar3 as D

G = SS.dollar3_game()
X = G.R
IDX = {x: k for k, x in enumerate(X)}
M = SS.dom_M(X, 6)


def dom(a, b):
    return bool(M[IDX[a], IDX[b]])


def test_realizable_outcomes():
    assert len(X) == 20
    three_pos = [x for x in X if min(x) > 0]
    assert three_pos == [(2, 2, 2)]                       # no discriminatory element except the degenerate (2,2,2)


def test_relation_M_hand_cases():
    assert dom((0, 3, 3), (4, 2, 0))                      # via {2,3}
    assert dom((4, 0, 2), (3, 3, 0))                      # M4: a member is dominated by an outsider
    assert not dom((3, 0, 3), (3, 3, 0))                  # members do not dominate each other (strict)
    assert not dom((3, 3, 0), (3, 0, 3))
    assert dom((3, 3, 0), (2, 2, 2))
    assert not dom((2, 2, 2), (4, 2, 0))                  # M1: (2,2,2) dominates only (0,0,0)
    assert [SS.label(X[v]) for v in np.nonzero(M[IDX[(2, 2, 2)]])[0]] == ['X']
    assert not M[IDX[(0, 0, 0)]].any()
    assert all(M[:, v].any() for v in range(len(X)))     # M2: the core is empty


def test_relation_C_equals_M_on_R_and_lemma_I():
    C, by = SS.dom_C(G.nact, G.pay, X)
    assert (C == M).all()                                 # C1
    assert not by[1].any()                                # singletons dominate nothing


def test_symmetric_set_unique_stable_on_R():
    V = SS.symmetric_set(X, 6)
    assert SS.is_stable(M, V)
    ks, ok = SS.kernels(M)
    assert ok and ks == [V]
    assert set(SS.brute_kernels(M)) == {V}


def test_discriminatory_lines_fail_on_grids():
    for g in (6, 8):
        Xg = SS.grid(g, True); Mg = SS.dom_M(Xg, g)
        for k in range(3):
            for c in range(1, g):
                line = [j for j, x in enumerate(Xg) if x[k] == c]
                assert not SS.is_stable(Mg, line)          # Lemma G
        ks, ok = SS.kernels(Mg)
        assert ok and ks == [SS.symmetric_set(Xg, g)]


def test_kernel_enumerator_against_brute_force():
    rng = np.random.default_rng(7)
    for trial in range(40):
        n = int(rng.integers(4, 12))
        Dm = rng.random((n, n)) < rng.uniform(0.1, 0.5)
        np.fill_diagonal(Dm, False)
        ks, ok = SS.kernels(Dm)
        assert ok and sorted(map(sorted, ks)) == sorted(map(sorted, SS.brute_kernels(Dm)))


def test_chicken_C_stable_sets():
    pay = SS.chicken_game(); Xc = [(-10, -10), (2, -1), (-1, 2), (0, 0)]
    Cc, _ = SS.dom_C((2, 2), pay, Xc, players=2)
    ks, _ = SS.kernels(Cc)
    assert sorted(map(sorted, ks)) == [[1], [2]]


def _island(T, J, comps, N=20):
    """one island from per-slot {local class: count}."""
    K = J.shape[0]
    init = np.zeros((1, 3, K), np.int64)
    for s in range(3):
        for k, c in comps[s].items():
            init[0, s, k] = c
    return init


def _const_universe():
    U = [np.arange(9) for _ in range(3)]                  # the nine constants are canonical functions 0..8
    S, mu = SS.arm_data('weak')
    ci = SS.const_index(S.fs)
    assert sorted(ci) == list(range(9)) and [ci[l] for l in range(9)] == list(range(9))
    return U


def test_classifier_on_constructed_islands():
    T = SS.Tables(G); U = _const_universe(); J = SS.joint_for('weak', U)
    lo = D.local_of; nout = len(T.R)
    dist = np.zeros(nout)
    # fair pair {1,2}, slot 3 anything: class P12:3|3
    init = _island(T, J, [{lo(0, 1, 1): 20}, {lo(1, 0, 1): 20}, {lo(2, D.ALL, 0): 10, lo(2, 0, 2): 10}])
    pres = np.zeros((1, 3, 9), np.int64); npres = np.zeros((1, 3), np.int64)
    for s in range(3):
        ks = np.nonzero(init[0, s])[0]; pres[0, s, :len(ks)] = ks; npres[0, s] = len(ks)
    c, e = SS._classify(J, T.VEC, T.ISMEM, T.TOT, init, pres, npres, 0, 20, dist, nout)
    assert T.labels[c] == 'P12:3|3' and abs(e - 1.0) < 1e-12
    # slot 1 split 50/50 between the two fair pairs: member-mixed
    init = _island(T, J, [{lo(0, 1, 1): 10, lo(0, 2, 1): 10}, {lo(1, 0, 1): 20}, {lo(2, 0, 1): 20}])
    for s in range(3):
        ks = np.nonzero(init[0, s])[0]; pres[0, s, :] = 0; pres[0, s, :len(ks)] = ks; npres[0, s] = len(ks)
    c, e = SS._classify(J, T.VEC, T.ISMEM, T.TOT, init, pres, npres, 0, 20, dist, nout)
    assert c == nout
    # unequal / fair mixture: other-mixed
    init = _island(T, J, [{lo(0, 1, 2): 10, lo(0, 1, 1): 10}, {lo(1, 0, 0): 20}, {lo(2, 0, 1): 20}])
    for s in range(3):
        ks = np.nonzero(init[0, s])[0]; pres[0, s, :] = 0; pres[0, s, :len(ks)] = ks; npres[0, s] = len(ks)
    c, e = SS._classify(J, T.VEC, T.ISMEM, T.TOT, init, pres, npres, 0, 20, dist, nout)
    assert c == nout + 1
    # 96% of encounters on P12:4|2: still P12:4|2 at tolerance 0.95
    init = _island(T, J, [{lo(0, 1, 2): 24, lo(0, 2, 2): 1}, {lo(1, 0, 0): 25}, {lo(2, D.ALL, 2): 25}])
    for s in range(3):
        ks = np.nonzero(init[0, s])[0]; pres[0, s, :] = 0; pres[0, s, :len(ks)] = ks; npres[0, s] = len(ks)
    c, e = SS._classify(J, T.VEC, T.ISMEM, T.TOT, init, pres, npres, 0, 25, dist, nout)
    assert T.labels[c] == 'P12:4|2'


def test_seed_laws():
    S, mu = SS.arm_data('weak')
    L = SS.seed_law('L', 0)
    assert abs(L[:9].sum() - 0.9759759759759757) < 1e-12 and np.allclose(L[:9], L[0])
    K = SS.seed_law('K', 1)
    assert abs(K[:9].sum() - 1) < 1e-12 and np.allclose(K[:9], 1 / 9)
    A0 = SS.seed_law('A', 0); A2 = SS.seed_law('A', 2)
    assert np.allclose(A0, L)
    low = [x for x in range(9) if S.fs[x][1][0] % 3 == 0]
    assert len(low) == 3
    assert abs(A2[low].sum() / A2[:9].sum() - 2 / 3) < 1e-12      # the (., 1/3) constants: 1/3 -> 2/3 of constant mass
    cat = np.random.default_rng(0).choice(len(mu), 160, replace=False)
    Ul = SS.seed_law('U', 0, cat=cat)
    assert (Ul > 0).sum() == 160 and np.allclose(Ul[cat], 1 / 160)
    # multinomial draws have the law's mean
    init = SS.draw_seeds(np.random.default_rng(1), 400, 100, [L, L, A2])
    f = init.sum(0) / (400 * 100)
    assert abs(f[0, :9].sum() - L[:9].sum()) < 0.005 and abs(f[2, low].sum() - A2[low].sum()) < 0.01
    # forced residence targets
    assert SS.target_constants('fair') == [D.local_of(0, 1, 1), D.local_of(1, 0, 1), None]


def test_flip_logger_on_constructed_flip():
    """slot 1 split 60/40 between naming 2 and naming 3 at 1/2, both partners offering 1/2 to slot 1: a
    neutral drift flip to P13:3|3 (pure drift through member-mixed states, no outsider)."""
    T = SS.Tables(G); U = _const_universe(); J = SS.joint_for('weak', U)
    lo = D.local_of; nout = len(T.R)
    N = 30
    hits = 0
    for seed in range(400):
        init = np.zeros((2, 3, 9), np.int64)
        init[0, 0, lo(0, 1, 1)] = 18; init[0, 0, lo(0, 2, 1)] = 12
        init[0, 1, lo(1, 0, 1)] = N; init[0, 2, lo(2, 0, 1)] = N
        init[1] = init[0]
        out = SS.kern(J, T.PAY, T.VEC, T.ISMEM, T.TOT, init, N, SS.W, 0.0, seed, 400, 1, np.array([400], np.int64), 10000)
        st, stop, counts, cls, eff, dist, ev, nev, nmig = out
        seq = cls[:, 0]
        hr = SS.held_runs(seq, nout, minlen=1)
        assert seq[0] == nout                                   # 60/40: member-mixed at the start
        assert set(np.unique(seq)) <= {nout, IDX[(3, 3, 0)], IDX[(3, 0, 3)]}   # never an outsider
        if counts[0, 0, lo(0, 2, 1)] == N:
            assert T.labels[seq[stop]] == 'P13:3|3'
            rows = [e for e in ev if e[1] == 0 and e[2] == 0 and e[4] == lo(0, 2, 1) and e[0] > 0]
            assert rows and all(abs(e[7]) < 1e-12 for e in rows)        # neutral crossing logged
            tr, nch = SS.trigger([e for e in ev if e[1] == 0], 0, stop, False)
            assert tr == 'pure drift' and nch == 1
            hits += 1
        if hits >= 3:
            break
    assert hits >= 3


def test_trigger_taxonomy_on_synthetic_events():
    # (gen, island, slot, old, new, intro, t10, dpay)
    prep = [(10, 0, 2, 1, 5, 4, 6, 0.0), (40, 0, 0, 2, 7, 30, 35, 1 / 6)]
    assert SS.trigger(prep, 0, 50, False)[0] == 'drift-prepared'
    coinc = [(10, 0, 2, 1, 5, 4, 6, 0.0), (12, 0, 0, 2, 7, 5, 8, 1 / 6)]
    assert SS.trigger(coinc, 0, 50, False)[0] == 'two-slot coincidence'
    single = [(10, 0, 0, 2, 7, 4, 6, 1 / 6)]
    assert SS.trigger(single, 0, 50, True)[0] == 'conditional'
    assert SS.trigger(single, 0, 50, False)[0] == 'single-slot strict'
    assert SS.trigger([], 0, 50, False)[0] == 'no-dominant-change'
