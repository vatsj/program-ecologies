"""Tests for the core stage-2 module (certified threats TX(t), followers F(delta), the acyclic two-order resolution, the statics, the island kernel).

    python3 -m pytest tests/test_core_stage2.py -q
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import core_auction as C
import core_stage2 as S
import core_stage2_run as R


# ------------------------------------------------------------------ the policy checker
def test_checker_admits_true_claims():
    for t in (1, 2, 7, 20, 40):
        assert S.check_policy(S.tx_source(t), ('policy', t)) == t
        assert S.certified_threat_of_tx(t) == t


def test_checker_rejects_false_claims():
    src = S.tx_source(20)
    assert S.check_policy(src, ('policy', 19)) is None                    # wrong threat
    assert S.check_policy(src, ('policy', 21)) is None
    assert S.check_policy(src, ('constant', 20)) is None                  # not a policy claim
    assert S.check_policy(src, 'policy') is None
    # a program that bids T (not T + 1) while claiming the policy
    bad = ('if', ('le', ('add', ('T',), ('int', 1)), ('int', 20)), ('T',), ('int', 20))
    assert S.check_policy(bad, ('policy', 20)) is None
    # the constant 20 claims the policy of TX(20): it differs at small T
    assert S.check_policy(('int', 20), ('policy', 20)) is None
    # a program that bids T + 1 for every T (no cap) does not satisfy any threat claim
    assert S.check_policy(('add', ('T',), ('int', 1)), ('policy', 20)) is None
    # a program that agrees with the policy except at one total
    sneaky = ('if', ('le', ('T',), ('int', 79)), tx_branch(20), ('int', 0))
    assert S.check_policy(sneaky, ('policy', 20)) is None


def tx_branch(t):
    return S.tx_source(t)


def test_policy_values():
    assert [S.policy_bid(20, T) for T in (0, 5, 18, 19, 20, 21, 30)] == [1, 6, 19, 20, 20, 20, 20]
    assert S.eval_src(S.tx_source(20), 18) == 19 and S.eval_src(S.tx_source(20), 19) == 20


# ------------------------------------------------------------------ follower bids by hand
def test_follower_bids_by_hand():
    # TX(20): R = 21, deltas 0.1..0.9, value 15 (an item): floor(d R / 10 + 1/2)
    assert [S.follower_bid_py(d, 21, 15) for d in range(1, 10)] == [2, 4, 6, 8, 11, 13, 15, 15, 15]
    assert [S.follower_bid_py(d, 21, 100) for d in range(1, 10)] == [2, 4, 6, 8, 11, 13, 15, 17, 19]
    # half rounds up: R = 15, d = 1 -> 1.5 -> 2 ; d = 3 -> 4.5 -> 5 ; d = 5 -> 7.5 -> 8
    assert [S.follower_bid_py(d, 15, 100) for d in (1, 3, 5)] == [2, 5, 8]
    # raised to at least 1: R = 1 (constant 0) at d = 1 -> 0.1 -> 0 -> 1
    assert S.follower_bid_py(1, 1, 15) == 1
    # capped at its value
    assert S.follower_bid_py(9, 41, 8) == 8
    # numba agrees
    for R_ in (1, 2, 7, 15, 21, 41):
        for d in range(1, 10):
            for val in (3, 8, 15, 40):
                assert S.f_bid(d, R_, val) == S.follower_bid_py(d, R_, val)


def test_follower_reads_constant_and_certificate():
    v = C.INSTANCES['threshold']
    # P is the constant 12: R = 13, delta 0.5 bids floor(6.5 + .5) = 7
    (bP, bA, bB), _ = S.py_resolve(12, S.F0 + 4, S.F0 + 4, v)
    assert (bP, bA, bB) == (12, 7, 7)
    # P is TX(12): the follower reads the certified threat 12, the same R = 13
    (bP, bA, bB), _ = S.py_resolve(S.TX0 + 11, S.F0 + 4, S.F0 + 4, v)
    assert (bA, bB) == (7, 7) and bP == 12            # T = 14 > 12: TX bids its threat 12


def test_tx_resolution_by_hand():
    v = C.INSTANCES['threshold']
    tx20 = S.TX0 + 19
    # (0.3, 0.7): bids 6 and 15, T = 21: TX bids its threat 20, the items win at revenue 21
    (bP, bA, bB), _ = S.py_resolve(tx20, S.F0 + 2, S.F0 + 6, v)
    assert (bA, bB, bP) == (6, 15, 20)
    o = C.outcome(bP, bA, bB, *v)
    assert abs(o[3] - 21) < 1e-9 and abs(o[4] - 1) < 1e-9
    # (0.1, 0.9): bids 2 and 15, T = 17: TX bids 18 and wins (inefficient)
    (bP, bA, bB), _ = S.py_resolve(tx20, S.F0, S.F0 + 8, v)
    assert (bA, bB, bP) == (2, 15, 18)
    o = C.outcome(bP, bA, bB, *v)
    assert abs(o[7] - 1) < 1e-9 and abs(o[4]) < 1e-9
    # exact tie at T = 20: constants 10 + 10 against TX(20): both sides bid 20, revenue lottery 50/50
    (bP, bA, bB), _ = S.py_resolve(tx20, 10, 10, v)
    assert (bP, bA, bB) == (20, 10, 10)
    o = C.outcome(bP, bA, bB, *v)
    assert abs(o[7] - 0.5) < 1e-9


# ------------------------------------------------------------------ order freedom
def test_order_free_numba_vs_python_sample():
    rng = np.random.default_rng(3)
    for inst in R.INSTS:
        v = C.INSTANCES[inst]
        U0, X0, B0 = S.build_tensor2(inst, 0)
        U1, X1, B1 = S.build_tensor2(inst, 1)
        assert (B0 == B1).all() and (U0 == U1).all() and (X0 == X1).all()
        for _ in range(3000):
            kP = int(rng.integers(0, S.K)); kA = int(rng.integers(0, S.F0 + S.NF)); kB = int(rng.integers(0, S.F0 + S.NF))
            a, da = S.py_resolve(kP, kA, kB, v, 'items_first')
            b, db = S.py_resolve(kP, kA, kB, v, 'p_first')
            assert a == b == tuple(int(x) for x in B0[:, kP, kA, kB])
            assert da <= 3 and db <= 3                        # the call graph is acyclic: bounded depth


def test_followers_do_not_read_each_other_or_p_output():
    """changing the partner item program (a follower or a constant) never changes a follower's bid; changing P's bids through a different TX with the
    same certified threat never changes it either."""
    v = C.INSTANCES['threshold']
    for kA in range(S.F0, S.F0 + S.NF):
        base = S.py_resolve(S.TX0 + 14, kA, 3, v)[0][1]
        for kB in list(range(0, 16)) + list(range(S.F0, S.F0 + S.NF)):
            assert S.py_resolve(S.TX0 + 14, kA, kB, v)[0][1] == base


# ------------------------------------------------------------------ statics
def test_prediction1_statics():
    for inst in R.INSTS:
        v = C.INSTANCES[inst]; mr = C.min_revenue(v)
        U, X, B = S.build_tensor2(inst, 0)
        vP = v[0]
        for dA in range(1, 10):
            dB = 10 - dA
            kP = S.TX0 + vP - 1
            bP, bA, bB = (int(x) for x in B[:, kP, S.F0 + dA - 1, S.F0 + dB - 1])
            if X[C.XEFF, kP, S.F0 + dA - 1, S.F0 + dB - 1] > 1 - 1e-9:
                assert X[C.XREV, kP, S.F0 + dA - 1, S.F0 + dB - 1] <= mr + 2 + 1e-9


def test_threshold_complementary_revenues_by_hand():
    U, X, B = S.build_tensor2('threshold', 0)
    kP = S.TX0 + 19
    revs = []
    for dA in range(1, 10):
        kA = S.F0 + dA - 1; kB = S.F0 + (10 - dA) - 1
        if X[C.XEFF, kP, kA, kB] > 0.99:
            revs.append(float(X[C.XREV, kP, kA, kB]))
    assert sorted(revs) == [21, 21, 21, 21, 22]


def test_skew_static_map_hand_values():
    U, X, B = S.build_tensor2('skew', 0)
    kP = S.TX0 + 13                                           # TX(14), R = 15
    bids = {dA: int(B[1, kP, S.F0 + dA - 1, S.F0]) for dA in range(1, 10)}
    assert bids == {1: 2, 2: 3, 3: 5, 4: 6, 5: 8, 6: 9, 7: 11, 8: 12, 9: 14}
    bB = {dB: int(B[2, kP, S.F0, S.F0 + dB - 1]) for dB in range(1, 10)}
    assert bB == {1: 2, 2: 3, 3: 5, 4: 6, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8}
    n_out = sum(1 for dA in range(1, 10) for dB in range(1, 10) if X[C.XPRUWIN, kP, S.F0 + dA - 1, S.F0 + dB - 1] < 1e-9)
    # items win outright or tie: count the T >= 14 pairs; T >= 15 are the 35 outright
    out = sum(1 for dA in range(1, 10) for dB in range(1, 10) if B[1, kP, S.F0 + dA - 1, S.F0 + dB - 1] + B[2, kP, S.F0 + dA - 1, S.F0 + dB - 1] >= 15)
    assert out == 35


def test_reference_splits_skew():
    refs = R.reference_splits('skew')
    assert refs['vn'] == (10.0, 4.0) and refs['es'] == (11.0, 3.0) and refs['ep'] == (7.0, 7.0)


# ------------------------------------------------------------------ priors, arrivals, kernel
def test_prior_masses():
    pr = S.prior2('threshold', 'no-overbid', 0.5)
    assert np.allclose(pr.sum(axis=1), 1.0)
    assert abs(pr[0, S.TX0:].sum() - 0.5) < 1e-12 and pr[0, 21:S.TX0].sum() == 0
    assert abs(pr[1, S.F0:S.F0 + S.NF].sum() - 0.5) < 1e-12 and pr[1, 16:S.F0].sum() == 0
    pc = S.prior2('threshold', 'unrestricted', 0.5, ptype='matched', itype='const')
    assert np.allclose(pc.sum(axis=1), 1.0) and pc[0, S.TX0:].sum() == 0 and pc[1, S.F0:].sum() == 0
    # matched constants: the mass of the constants c = t is doubled relative to uniform: 0.5/41 + 0.5/40 at c >= 1
    assert abs(pc[0, 5] - (0.5 / 41 + 0.5 / 40)) < 1e-12
    # threat means: no-overbid threshold, constants 0..20 mean 10, TX 1..20 mean 10.5
    assert abs(S.prior_mean_threat(S.prior2('threshold', 'no-overbid', 0.5)) - 10.25) < 1e-9


def test_rain_priors():
    pr = S.prior2('threshold', 'no-overbid', 0.5)
    q = S.rain_prior(pr, 'fol_only')
    assert np.allclose(q[0], pr[0]) and q[1, :S.NC].sum() == 0 and abs(q[1, S.F0:S.F0 + S.NF].sum() - 1) < 1e-12
    q = S.rain_prior(pr, 'safe')
    assert q[1, S.F0:S.F0 + 4].sum() == 0 and abs(q[1, S.F0 + 4:S.F0 + S.NF].sum() - 1) < 1e-12


def test_arrivals_pairing_and_filter():
    N, I, gens = 20, 4, 200
    sched = np.full(gens, 0.05 / N * 10)
    pr = S.prior2('threshold', 'no-overbid', 0.5)
    cdf_full = C.cdf_of(pr)
    cdf_fol = C.cdf_of(S.rain_prior(pr, 'fol_only'))
    a = S.make_arrivals(sched, N, I, cdf_full, 123)
    b = S.make_arrivals(sched, N, I, cdf_fol, 123)
    for x, y in zip((a[0], a[1], a[2], a[3], a[5]), (b[0], b[1], b[2], b[3], b[5])):
        assert (x == y).all()                                  # same times, islands, roles, victim uniforms
    ch = b[4][b[3] > 0]
    assert ((ch >= S.F0) & (ch < S.F0 + S.NF)).all()          # item arrivals are followers only
    assert (a[4][a[3] == 0] == b[4][b[3] == 0]).all()         # P arrivals identical
    p_only = S.make_arrivals(sched, N, I, cdf_full, 123, roles=(0,))
    assert (p_only[3] == 0).all() and len(p_only[1]) == int((a[3] == 0).sum())
    assert p_only[0][-2] == len(p_only[1])
    # per-generation pointers consistent after filtering
    for g in range(gens):
        assert (p_only[1][p_only[0][g]:p_only[0][g + 1]] >= 0).all()
    # number of arrivals is about 3 I N eps
    assert abs(len(a[1]) - 3 * I * N * sched[0] * gens) < 6 * np.sqrt(3 * I * N * sched[0] * gens)


def test_kernel_conservation_incremental_payoffs_and_pairing():
    cell = dict(R.CELLS['p_threshold_no-overbid_rain_m50'])
    cell['N'] = 20; cell['I'] = 4; cell['gens'] = 300
    U, X, B = S.build_tensor2('threshold', 0)
    pr = S.prior2('threshold', 'no-overbid', 0.5)
    rng = np.random.default_rng(5)
    init = C.seed_counts(pr, cell['I'], cell['N'], rng)
    sched = np.full(cell['gens'], 0.3 / cell['N'])
    arr = S.make_arrivals(sched, cell['N'], cell['I'], C.cdf_of(pr), 9)
    smp = C.sample_times(cell['gens'])
    out = S.sim2(U, X, init, cell['N'], C.W, 0.02, cell['gens'], 11, *arr, smp, 17.0, 1)
    counts, samp, samp2, hist, fe, stop, pay, fi, fa, ft, rr, rm = out
    assert (counts.sum(axis=2) == cell['N']).all()
    for i in range(cell['I']):
        for r in range(3):
            for k in range(S.K):
                if counts[i, r, k] > 0:
                    assert abs(pay[i, r, k] - C._payoff_of(U, counts, i, r, k)) < 1e-6
    assert (hist.sum(axis=3) == cell['N']).all()
    assert rr[-1].sum() > 0 and rm[-1].sum() > 0                  # arrivals and migration both replaced programs
    # the final sampled statistic row equals a recomputation of the stats on the final counts
    row = np.zeros(C.NS)
    C._stats(U, X, counts, 0, cell['N'], row)
    assert np.allclose(row, samp[-1, 0])


def test_frozen_islands_stop_and_tested_flags():
    N, I, gens = 20, 4, 400
    U, X, B = S.build_tensor2('threshold', 0)
    # P fixed on TX(20), A and B fixed on the constants 5 and 5: T = 10, TX bids 11 and wins: tested
    init = np.zeros((I, 3, S.K), np.int64)
    init[:, 0, S.TX0 + 19] = N; init[:, 1, 5] = N; init[:, 2, 5] = N
    arr = S.make_arrivals(np.zeros(gens), N, I, C.cdf_of(S.prior2('threshold', 'no-overbid', 0.5)), 1)
    smp = C.sample_times(gens)
    out = S.sim2(U, X, init, N, C.W, 0.0, gens, 3, *arr, smp, 17.0, 1)
    counts, samp, samp2, hist, fe, stop, pay, fi, fa, ft, rr, rm = out
    assert stop == 0 and (counts == init).all()
    assert (ft[:, S.TX0 + 19] == 0).all()                            # tested at generation 0
    assert (fa == 0).all() and (fi == 0).all()
    assert abs(samp[-1, 0, 7] - 1.0) < 1e-9                          # TX wins every encounter
    # TX shadow: items at 12 and 12 (T = 24 > 20): TX never wins, never tested
    init2 = np.zeros((I, 3, S.K), np.int64)
    init2[:, 0, S.TX0 + 19] = N; init2[:, 1, 12] = N; init2[:, 2, 12] = N
    out = S.sim2(U, X, init2, N, C.W, 0.0, gens, 3, *arr, smp, 17.0, 1)
    assert (out[9][:, S.TX0 + 19] == -1).all() and abs(out[1][-1, 0, 7]) < 1e-12


def test_txwin_statistic_and_dtx():
    """the TX-minus-matched-constant payoff of a state with TX(20) against constants 5, 5: TX bids 11, the constant 20 bids 20."""
    N = 10
    U, X, B = S.build_tensor2('threshold', 0)
    counts = np.zeros((1, 3, S.K), np.int64)
    counts[0, 0, S.TX0 + 19] = N; counts[0, 1, 5] = N; counts[0, 2, 5] = N
    row2 = np.zeros(S.NS2)
    S._stats2(U, X, counts, 0, N, row2)
    # TX(20) vs 5,5: bid 11, wins, payoff 20 - 11 = 9; constant 20: payoff 0
    assert abs(row2[S.S2_DTX] - 9.0) < 1e-9 and abs(row2[S.S2_THREAT] - 20.0) < 1e-9
