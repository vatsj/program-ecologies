"""Queue 81 tests: exact sojourns, the generated kernel against kern_mt, invariants of the regret analysis."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))


def test_sojourn_neutral_establishment():
    import tbr
    for N in (20, 100):
        T, pest = tbr.sojourn(N, 1.0)
        assert abs(pest - 1.0 / (N // 2)) < 1e-12          # neutral gambler's ruin to N/2
        assert T > 0


def test_sojourn_selected_against_matches_geometric_limit():
    import tbr
    T, _ = tbr.sojourn(2000, 0.7)
    assert abs(T - 1.0 / (1.0 - 0.7)) < 0.1                 # P10's reading: T_q -> 1/(1 - r_q)


def test_stage0_exact_process_reduces_to_moran():
    import tbr_stage0 as S
    N = 50
    pu, pd = S.updown_a(N, 0.0, 1.0)
    assert abs(S.bd_fix(pu[:N], pd[:N]) - 1.0 / N) < 1e-12


def test_kern_tbr_draw_for_draw():
    import majority_tail as MT
    import majority_tail_kern as MK
    import tbr_kern as TK
    prep = MT.prepare('T', 'main', 20, 0, I=4)
    H = 400
    snapg = np.array([100, 200, 400], np.int64)
    ag, ai, asl, au, lk = MT.local_arrivals(prep, 100)
    args = (prep['J'], prep['PAY'], prep['VEC'], prep['ISMEM'], prep['TOT'], prep['loc'], 20, MT.W, 1.0 / 20,
            prep['seed'], H, 10, snapg, ag, ai, asl, au, lk, 10000, 10000)
    a = MK.kern_mt(*args)
    b = TK.kern_tbr(*args)
    for x, y in zip(a, b[:12]):
        assert np.array_equal(np.asarray(x), np.asarray(y))


def test_analyze_invariants():
    import majority_tail as MT
    import tbr
    A = tbr.Tri('T')
    I, N = 8, 20
    G = np.zeros((I, 3, A.K), np.int64)
    # two profiles: islands 0-3 hold (14, 10, 1), islands 4-7 hold (14, 4, 1)
    for i in range(I):
        G[i, 0, 14] = N; G[i, 1, 10 if i < 4 else 4] = N; G[i, 2, 1] = N
    founders = G.sum(0)
    tail = [A.seed[s] for s in range(3)]
    w, cases, cache = tbr.analyze(A, G, N, 1.0, founders, tail, comp=True)
    assert w['diverse']
    for c in cases:
        assert c['nE'] >= 1 and c['regT'] >= -1e-12 and c['regA'] >= -1e-12
        assert c['nEc'] == c['nE']                              # monomorphic islands: composition = majority
    # consensus world: every migrant statistic is vacuous
    G2 = G.copy(); G2[:, 1, :] = 0; G2[:, 1, 10] = N
    w2, cases2, _ = tbr.analyze(A, G2, N, 1.0, founders, tail, comp=False)
    assert not w2['diverse']
    assert all(c['vacT'] and c['vacA'] for c in cases2)
