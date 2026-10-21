"""Tests for src/core_auction.py: instance cores and Vickrey-nearest points by hand, best-offer resolution with random revenue ties,
PRU expected-payoff best replies (including the tie case near value), the evaluator's two-pass order, the statics, the island kernel."""
import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import core_auction as C


# ---------------------------------------------------------------- instance cores and Vickrey-nearest points, by hand
def test_core_bounds_threshold():
    # (P, A, B) = (20, 15, 15): w(N) = 30; u_P <= 0, u_A, u_B <= 10, u_A + u_B <= 10, so the bidders get at most 10 and the revenue is at least 20
    cin = C.core_inequalities((20, 15, 15))
    assert cin[(0,)] == 0 and cin[(1,)] == 10 and cin[(2,)] == 10 and cin[(1, 2)] == 10
    assert C.min_revenue((20, 15, 15)) == pytest.approx(20)
    assert C.core_revenue_range((20, 15, 15)) == (pytest.approx(20), 30)


def test_core_bounds_asymmetric():
    # (20, 16, 12): w(N) = 28; u_A <= 8, u_B <= 8, u_A + u_B <= 8: min revenue 20
    cin = C.core_inequalities((20, 16, 12))
    assert cin[(1,)] == 8 and cin[(2,)] == 8 and cin[(1, 2)] == 8 and cin[(0,)] == 0
    assert C.min_revenue((20, 16, 12)) == pytest.approx(20)


def test_core_bounds_collusion():
    # (20, 5, 5): P wins, w(N) = 20; u_P <= 20 - 10 = 10, the items' u <= 0: P pays at least 10
    cin = C.core_inequalities((20, 5, 5))
    assert cin[(0,)] == 10 and cin[(1,)] == 0 and cin[(2,)] == 0
    assert C.min_revenue((20, 5, 5)) == pytest.approx(10)


def test_vickrey_nearest_points():
    assert C.vcg_payments((20, 15, 15)) == {'A': 5.0, 'B': 5.0}
    assert C.vickrey_nearest((20, 15, 15)) == {'A': 10.0, 'B': 10.0}
    assert C.vcg_payments((20, 16, 12)) == {'A': 8.0, 'B': 4.0}
    assert C.vickrey_nearest((20, 16, 12)) == {'A': 12.0, 'B': 8.0}
    assert C.vickrey_nearest((20, 5, 5)) == {'P': 10.0}


def test_in_core_vectors():
    v = (20, 15, 15)
    assert C.in_core(v, (0, 5, 5), 20)                 # payments 10 + 10: Vickrey-nearest
    assert C.in_core(v, (0, 10, 0), 20)                # A pays 5, B pays 15: the edge
    assert not C.in_core(v, (0, 6, 5), 19)             # revenue 19 below the minimum (accounting does not close: 6 + 5 + 19 = 30 but u_A + u_B > 10)
    assert not C.in_core(v, (0, 10, 10), 10)           # payments 5 + 5 (VCG): bidders get 20 > 10
    assert C.in_core(v, (0, 0, 0), 30)                 # all surplus to the seller is in the core
    assert not C.in_core(v, (0, 0, 0), 20)             # u + revenue < w(N): not efficient
    assert not C.in_core(v, (5, 0, 0), 15)             # P wins at 15: inefficient
    assert C.in_core((20, 5, 5), (10, 0, 0), 10)       # collusion: P pays 10
    assert not C.in_core((20, 5, 5), (15, 0, 0), 5)    # P pays 5: the losers can profitably outbid


def test_edge_baseline_asymmetric_by_hand():
    # splits (pA, pB) with pA + pB in {20, 21}, pA >= 8, pB >= 4, pA <= 16, pB <= 12: 9 + 8 = 17 points; within one tick of (12, 8): 5
    b = C.edge_baseline('asymmetric', 'no-overbid')
    assert b['n_edge'] == 17 and b['n_near'] == 5
    assert b['baseline'] == pytest.approx(5 / 17)
    b2 = C.edge_baseline('asymmetric', 'unrestricted')
    assert b2['n_edge'] == 17            # an overbid cannot be in the core, so the unrestricted edge is the same


# ---------------------------------------------------------------- best-offer resolution and the random revenue tie
def test_outcome_plain_win():
    # P bids 12 against A + B = 10: P wins, pays 12, u_P = 8; inefficient in the threshold instance
    o = C.outcome(12, 5, 5, 20, 15, 15)
    assert o[0] == pytest.approx(8) and o[1] == 0 and o[3] == pytest.approx(12) and o[4] == 0
    assert o[7] == 1.0
    # A + B = 20 beats P at 19: both items win and pay their bids; efficient, in the core
    o = C.outcome(19, 10, 10, 20, 15, 15)
    assert o[1] == pytest.approx(5) and o[2] == pytest.approx(5) and o[3] == pytest.approx(20) and o[4] == 1.0 and o[6] == 1.0


def test_outcome_revenue_tie_is_a_fair_lottery():
    o = C.outcome(20, 10, 10, 20, 15, 15)             # P at 20 ties the pair's 20
    assert o[3] == pytest.approx(20)
    assert o[0] == pytest.approx(0)                   # P wins half the time at zero surplus
    assert o[1] == pytest.approx(2.5) and o[2] == pytest.approx(2.5)
    assert o[4] == pytest.approx(0.5) and o[7] == pytest.approx(0.5) and o[8] == pytest.approx(0.5)
    o = C.outcome(10, 10, 0, 20, 15, 15)              # B bids zero: {P} and {A} tie at 10
    assert o[7] == pytest.approx(0.5) and o[8] == pytest.approx(0.5) and o[9] == 0
    assert o[0] == pytest.approx(5) and o[1] == pytest.approx(2.5)


def test_outcome_zero_bids_and_no_sale():
    o = C.outcome(0, 0, 0, 20, 15, 15)
    assert o[3] == 0 and o[4] == 0 and o[5] == 1.0 and o[7] == 0 and o[8] == 0
    o = C.outcome(0, 7, 0, 20, 15, 15)                # A alone wins at 7 (zero is no bid)
    assert o[1] == pytest.approx(8) and o[3] == pytest.approx(7) and o[8] == 1.0


def test_outcome_overbid_loses_money():
    o = C.outcome(0, 20, 5, 20, 15, 15)              # A overbids to 20 > value 15 and wins with B: u_A = -5, not IR
    assert o[1] == pytest.approx(-5) and o[5] == 0


# ---------------------------------------------------------------- PRU best replies
def test_pru_best_reply_tie_beats_outbidding_near_value():
    # P (value 20) against A + B = 19: tying at 19 gives half of (20 - 19); bidding 20 wins at zero surplus
    assert C.best_reply(0, 0, 10, 9, 20, 15, 15, 20, 7) == 19
    # against 18: tying at 18 gives 0.5 * 2 = 1, outbidding at 19 gives 1; ties in expected payoff go to the lower bid
    assert C.best_reply(0, 0, 10, 8, 20, 15, 15, 20, 7) == 18
    # against 17: outbidding at 18 gives 2 > tying at 17 giving 1.5
    assert C.best_reply(0, 0, 10, 7, 20, 15, 15, 20, 7) == 18
    # against 20: the best expected payoff is not strictly positive: the default
    assert C.best_reply(0, 0, 10, 10, 20, 15, 15, 20, 7) == 7
    # against 25: the same
    assert C.best_reply(0, 0, 15, 10, 20, 15, 15, 20, 7) == 7


def test_pru_zero_bid_handling():
    # A with P and B both at 0: bidding 1 wins alone at u = 14; bidding 0 is no bid
    assert C.best_reply(1, 0, 0, 0, 20, 15, 15, 15, 9) == 1
    # P bids 12 and B bids 0: A needs more than 12 alone; 13 gives u = 2, which beats a tie at 12 (0.5 * 3 = 1.5)
    assert C.best_reply(1, 12, 0, 0, 20, 15, 15, 15, 9) == 13
    # no bid is profitable above the value: with B at 30 and P at 20, A needs only 1 (total 31)
    assert C.best_reply(1, 20, 0, 30, 20, 15, 15, 40, 9) == 1


def test_pru_wins_exactly_when_the_other_side_underbids():
    # loser A against a firm B at 10 and P at 20: A needs 11 (total 21 > 20), u = 4; the tie at 10 gives 0.5 * 5 = 2.5
    assert C.best_reply(1, 20, 0, 10, 20, 15, 15, 15, 3) == 11
    # B at 4 and P at 25 (overbidding in the unrestricted space): A would need 22 > its value: the default
    assert C.best_reply(1, 25, 0, 4, 20, 15, 15, 15, 3) == 3


# ---------------------------------------------------------------- the evaluator's two passes
def test_evaluator_two_pass_hand_case():
    # threshold, P = PRU(0), A = PRU(0), B = constant 10, no-overbid caps (20, 15, 15).
    # order P, A, B:  pass 1: P 11 (against B alone at 10: u = 9), A 2 (total 12 > 11);  pass 2: P 13, A 4  -> bids (13, 4, 10), cycling
    kP, kA, kB = C.NC + 0, C.NC + 0, 10
    bP, bA, bB, cyc = C.resolve(kP, kA, kB, 20, 15, 15, 20, 15, 15, 0, 1, 2)
    assert (bP, bA, bB, cyc) == (13, 4, 10, 1)
    # order B, A, P:  pass 1: A 1 (P at its default 0), P 12;  pass 2: A 3, P 14 -> (14, 3, 10), cycling: the order moves the result
    bP, bA, bB, cyc = C.resolve(kP, kA, kB, 20, 15, 15, 20, 15, 15, 2, 1, 0)
    assert (bP, bA, bB, cyc) == (14, 3, 10, 1)


def test_evaluator_resolved_profile_and_constants_only():
    # a constant profile is returned unchanged and never cycles
    assert C.resolve(5, 9, 12, 20, 15, 15, 20, 15, 15, 0, 1, 2) == (5, 9, 12, 0)
    # PRU for P against constants A = B = 10: total 20, no strictly positive reply: its default
    assert C.resolve(C.NC + 7, 10, 10, 20, 15, 15, 20, 15, 15, 0, 1, 2) == (7, 10, 10, 0)
    # against A + B = 15 PRU outbids at 16 (u = 4) rather than tying at 15 (2.5)
    assert C.resolve(C.NC + 7, 8, 7, 20, 15, 15, 20, 15, 15, 0, 1, 2) == (16, 8, 7, 0)


# ---------------------------------------------------------------- statics
def test_nash_membership_by_hand():
    idx, U, X, caps = C.pure_nash('threshold', 'no-overbid')
    S = {tuple(int(x) for x in r) for r in idx}
    assert (19, 10, 10) in S             # the pair pays 20; A deviating to 9 ties P at 19 for 0.5 * 6 = 3 < 5
    assert (20, 10, 10) not in S         # P at 20 ties the pair: A gets half of 5 = 2.5 and prefers to bid 11 and win for 4
    assert (5, 10, 10) not in S          # a lower bid by A wins more cheaply against P at 5
    assert (10, 8, 8) not in S           # P outbids (revenue 16 < 19)
    # hand argument: in the no-overbid space the caps force bA + bB <= bP + 1 <= 21 at an efficient equilibrium, and P cannot profit iff bA + bB >= 20
    for r in S:
        if X[C.XEFF, r[0], r[1], r[2]] > 1 - 1e-9:
            assert 20 - 1e-9 <= X[C.XREV, r[0], r[1], r[2]] <= 21 + 1e-9


def test_nash_unrestricted_by_hand():
    idx, U, X, caps = C.pure_nash('threshold', 'unrestricted')
    S = {tuple(int(x) for x in r) for r in idx}
    assert (27, 14, 14) in S             # revenue 28 inside the core; A at 13 would only tie P at 27 for 0.5 * 2 = 1 = its present payoff
    assert (30, 15, 15) not in S         # P at the item total ties for -5 in expectation and prefers to lose
    assert (29, 15, 14) not in S         # A at 14 ties P for 0.5 > 0
    assert (20, 11, 10) in S             # revenue 21; P at its value 20 loses and cannot gain by tying at 21 (-0.5)
    rev = {round(float(X[C.XREV, r[0], r[1], r[2]])) for r in S if X[C.XEFF, r[0], r[1], r[2]] > 1 - 1e-9}
    assert min(rev) == 20 and max(rev) <= 30


# ---------------------------------------------------------------- the island kernel
def _run(inst, space, m_pru, kind, gens, seed, A=3.0, m=0.0, I=8, N=40):
    with_pru = m_pru > 0
    U, X = C.build_tensor(inst, space, with_pru)
    pr = C.prior(inst, space, m_pru)
    rng = np.random.default_rng(seed)
    init = C.seed_counts(pr, I, N, rng)
    sched = C.eps_schedule(kind, N, A=A, gens=gens)
    smp = C.sample_times(gens)
    out = C.sim(U, X, init, N, 0.3, m, gens, seed, sched, C.cdf_of(pr), smp, C.min_revenue(C.INSTANCES[inst]))
    return U, X, init, out, smp


def test_kernel_incremental_payoffs_and_stats_consistent():
    for kind, m in (('zero', 0.0), ('rain', 0.0), ('zero', 0.05)):
        U, X, init, (counts, samp, fe, stop, pay), smp = _run('threshold', 'no-overbid', 0.2, kind, 150, 3, m=m)
        N = 40
        assert (counts.sum(axis=2) == N).all()
        for i in range(counts.shape[0]):
            for r in range(3):
                for k in np.nonzero(counts[i, r])[0]:
                    assert pay[i, r, k] == pytest.approx(C._payoff_of(U, counts, i, r, k), abs=1e-6)
            mean = [(counts[i, r] * pay[i, r]).sum() / N ** 3 for r in range(3)]
            assert samp[-1, i, 0] == pytest.approx(mean[0], abs=1e-6)
            assert samp[-1, i, 1] == pytest.approx(mean[1], abs=1e-6)
            assert samp[-1, i, 2] == pytest.approx(mean[2], abs=1e-6)


def test_kernel_no_mutation_no_new_programs_and_fixation():
    U, X, init, (counts, samp, fe, stop, pay), smp = _run('threshold', 'unrestricted', 0.0, 'zero', 3000, 4)
    assert ((counts > 0) <= (init.sum(axis=0, keepdims=True) > 0)).all()
    assert stop < 3000                   # all islands fixed before the horizon at N = 40


def test_schedule_annealed_total_and_onset():
    N = 100
    s = C.eps_schedule('ann', N, A=3.0, gens=5000)
    assert (s[:200] == 0).all()
    total = s.sum() * N
    assert total == pytest.approx(3.0 * (5000 - 200) / (5000 - 200 + N / 2.0), rel=1e-6)
    r = C.eps_schedule('rain', N, gens=100, epsN=0.05)
    assert r[0] * N == pytest.approx(0.05)


def test_prior_masses():
    p = C.prior('threshold', 'no-overbid', 0.2)
    assert p.shape == (3, 82)
    assert p[0, :21].sum() == pytest.approx(0.8) and p[0, C.NC:C.NC + 21].sum() == pytest.approx(0.2)
    assert p[1, :16].sum() == pytest.approx(0.8)
    assert p[1, 16:C.NC].sum() == 0
    q = C.prior('threshold', 'unrestricted', 0.0)
    assert q.shape == (3, 41) and q[0].sum() == pytest.approx(1)
