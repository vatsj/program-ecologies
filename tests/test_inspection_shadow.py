"""Tests for src/inspection_shadow.py: the blocked GTH solver and its censored chain against dense linear algebra, the twin relation of
`N` and `cr(THEM(ME))` against `C` at c = 0 and c = 0.01 (notes/inspection-shadow.md section 1.1), the one-state exit calculations of
section 1.2, the prudent class and the exactness of the boosted prior and its matched control (section 1.4), the exit decomposition on
a toy chain against a brute-force enumeration of moves, the equality of lottery3 with mixed2.lottery2, and the matching of the K-rain
and C-rain controls."""
import os, sys, math
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import mixed2 as M
import inspection_shadow as S

_arms = {}


def arm(a, c):
    if (a, c) not in _arms:
        _arms[(a, c)] = S.get_arm(a, c)
    return _arms[(a, c)]


def random_chain(n, seed=1, dens=0.3):
    rng = np.random.default_rng(seed)
    P = rng.random((n, n)) ** 8
    P[rng.random((n, n)) > dens] = 0
    np.fill_diagonal(P, 0)
    P += 1e-12 * rng.random((n, n))
    np.fill_diagonal(P, 0)
    return P / P.sum(1, keepdims=True)


def test_blocked_gth_matches_dense_and_plain():
    n = 300
    P = random_chain(n)
    A = P.T - np.eye(n); A[-1] = 1
    b = np.zeros(n); b[-1] = 1
    ref = np.linalg.solve(A, b)
    plain = M._gth_inplace(P.copy())
    for blk in (1, 9, 64):
        x, _, _ = S.gth_blocked(P.copy(), np.zeros((n, 1)), m=0, block=blk, chunk=50)
        assert np.abs(x - ref).max() < 1e-12
        assert np.abs(x / plain - 1).max() < 1e-10


def test_snapshot_and_first_passage_against_linear_algebra():
    n, m = 260, 120
    P = random_chain(n, seed=3)
    rew = np.random.default_rng(4).random((n, 2))
    x, B, Rw = S.gth_blocked(P.copy(), rew.copy(), m=m, block=31, chunk=40)
    assert np.abs(B.sum(1) - 1).max() < 1e-12
    Bp, Rp = S.censor_to(P.copy(), rew.copy(), list(range(m)))
    assert np.abs(B - Bp).max() < 1e-12 and np.abs(Rw / Rp - 1).max() < 1e-10
    T = list(range(1, 8))
    mask = np.zeros(m, bool); mask[T] = True
    probs, r0, stay = S.first_passage(B, Rw, 0, mask)
    nt = [i for i in range(n) if i not in T]
    Qn = P[np.ix_(nt, nt)]
    h = np.linalg.solve(np.eye(len(nt)) - Qn, rew[nt])
    pr = np.linalg.solve(np.eye(len(nt)) - Qn, P[np.ix_(nt, T)])
    assert np.abs(r0 - h[0]).max() < 1e-9
    assert np.abs(np.array([probs[t] for t in T]) - pr[0]).max() < 1e-12


def test_twin_relation_and_charged_costs():
    A0 = arm('exact', 0.0); A1 = arm('exact', 0.01)
    for A, c in ((A0, 0.0), (A1, 0.01)):
        nm = S.named(A)
        N_, CRI, C_, K_ = nm['0N'], nm['0CRI'], nm['1C'], nm['1K']
        assert A.CA[CRI, C_] == pytest.approx(1.0) and A.CA[N_, C_] == 0.0              # one level charged to the reader
        assert A.UAg[N_, C_] == 0 and A.UAg[CRI, C_] == 0 and A.UBg[C_, N_] == 0 and A.UBg[C_, CRI] == 0   # same game payoffs against C
        assert A.UAg[N_, K_] == pytest.approx(-4) and A.UAg[CRI, K_] == pytest.approx(-1)            # they differ against K
        assert A.UA[CRI, C_] == pytest.approx(-c) and A.UA[N_, C_] == 0
    nm = S.named(A1)
    assert int((np.abs(A1.UA[:, nm['1C']]) < 1e-9).sum()) == 1                                # at c = 0.01 N is the only zero-cost class against C
    nm = S.named(A0)
    tw = np.nonzero(np.abs(A0.UA[:, nm['1C']]) < 1e-9)[0]
    assert len(tw) == 38 and A0.mass[0][tw].sum() == pytest.approx(0.3105, abs=1e-4)


def test_exit_calculations_of_the_notes():
    A = arm('exact', 0.0)
    nm = S.named(A)
    r = S.reference_exits(A, 10000, nm['0CRI'], nm['1C'])
    assert r['inspector']['neutral'] == pytest.approx(1.546e-5, rel=2e-3) and r['inspector']['strict'] == 0.0
    assert r['inspectee']['strict'] == pytest.approx(7.40e-5, rel=2e-3)
    r = S.reference_exits(A, 10000, nm['0N'], nm['1C'])
    assert r['inspectee']['strict'] == pytest.approx(0.0609, rel=2e-3)
    A1 = arm('exact', 0.01)
    nm1 = S.named(A1)
    r = S.reference_exits(A1, 10000, nm1['0CRI'], nm1['1C'])
    assert r['inspector']['strict'] == pytest.approx(4.60e-4, rel=2e-3)


def test_prudent_class_and_exact_priors():
    A = arm('exact', 0.0)
    S_ = S.prudent_classes(A)
    assert len(S_) == 8 and A.mass[1][S_].sum() == pytest.approx(0.000738, abs=1e-6)
    nm = S.named(A)
    m = A.mass[1]
    mb, fb, ib = S.mass_variant(A, 'boost')
    mc, fc, ic = S.mass_variant(A, 'control')
    assert mb.sum() == pytest.approx(1.0) and mc.sum() == pytest.approx(1.0)
    assert mb[S_].sum() == pytest.approx(10 * m[S_].sum())                                    # x10 exactly
    assert mc[nm['1C']] - m[nm['1C']] == pytest.approx(ib['delta']) and mb[S_].sum() - m[S_].sum() == pytest.approx(ib['delta'])   # the same added mass
    out = np.ones(len(m), bool); out[S_] = False
    out_c = np.ones(len(m), bool); out_c[nm['1C']] = False
    assert np.allclose(fb[out], fb[out][0]) and np.allclose(fc[out_c], fc[out_c][0])           # donors shrink proportionally
    assert np.allclose(fb[S_], 10.0) and np.allclose(fc[nm['1C']], 1 + ic['delta'] / m[nm['1C']])
    # weighted founders reproduce the unweighted draw at factor 1 and the boosted mass in the large
    lang = A.lang
    K1 = A.K[1]
    f_u = M.draw_founders(lang, 1, A.cls_of[1], K1, 8, 100, 99)
    f_1 = S.draw_founders_w(lang, 1, A.cls_of[1], K1, 8, 100, 99, np.ones(K1))
    assert (f_u == f_1).all()
    big = S.draw_founders_w(lang, 1, A.cls_of[1], K1, 400, 1000, 7, fb)
    share = big.sum(0) / big.sum()
    assert share[S_].sum() == pytest.approx(mb[S_].sum(), rel=0.08)
    assert share[nm['1C']] == pytest.approx(mb[nm['1C']], abs=0.004)


def test_sets_nested_and_defined():
    A = arm('exact', 0.0)
    fl = S.class_flags(A)
    s = S.pair_sets(A, fl)
    assert (s['R'] <= s['E']).all() and (s['Rstar'] <= s['R']).all() and (s['Estar'] <= s['E']).all()
    nm = S.named(A)
    assert s['R'][nm['0CRI'], nm['1C']] and s['Rstar'][nm['0CRI'], nm['1C']]
    assert s['E'][nm['0N'], nm['1C']] and not s['R'][nm['0N'], nm['1C']]
    assert not s['E'][nm['0N'], nm['1K']]


def test_exit_decomposition_against_brute_force():
    A = S.get_arm('blind', 0.0)                    # 17 x 17 classes, whole space
    N = 100
    W_ = S.Whole(A, N)
    lpi, _ = W_.solve()
    K0, K1 = A.K
    pi = np.exp(lpi).reshape(K0, K1); pi /= pi.sum()
    fl = S.class_flags(A)
    sets = S.pair_sets(A, fl)
    ex, bal = S.decompose(A, N, pi, sets, fl)
    assert bal['max_rel_residual'] < 1e-9
    for X in ('E', 'Estar'):
        mk = sets[X]
        tot = 0.0
        neutral = 0.0
        for a in range(K0):
            for b in range(K1):
                if not mk[a, b]:
                    continue
                for q in range(K0):
                    if q != a and not mk[q, b]:
                        du = A.UA[q, b] - A.UA[a, b]
                        rate = 0.5 * A.mass[0][q] * math.exp(float(M.lrho(np.array([du]), N)[0]))
                        tot += pi[a, b] * rate
                        neutral += pi[a, b] * rate * (abs(du) <= 1e-9)
                for q in range(K1):
                    if q != b and not mk[a, q]:
                        du = A.UB[q, a] - A.UB[b, a]
                        rate = 0.5 * A.mass[1][q] * math.exp(float(M.lrho(np.array([du]), N)[0]))
                        tot += pi[a, b] * rate
                        neutral += pi[a, b] * rate * (abs(du) <= 1e-9)
        assert ex[X]['flux'] == pytest.approx(tot, rel=1e-9)
        cats = ex[X]['cats']
        assert sum(v['flux'] for v in cats.values()) == pytest.approx(tot, rel=1e-9)
        assert cats['A_neutral_shadow']['flux'] + cats['B_neutral_other']['flux'] == pytest.approx(neutral, rel=1e-9, abs=1e-15)
        assert ex[X]['pi'] == pytest.approx(pi[mk].sum())


def test_lottery3_equals_lottery2_without_rain_and_matches_controls():
    A = arm('exact', 0.0)
    lang = A.lang; K0, K1 = A.K
    f0 = M.draw_founders(lang, 0, A.cls_of[0], K0, 6, 60, 11); f1 = M.draw_founders(lang, 1, A.cls_of[1], K1, 6, 60, 12)
    i0 = np.nonzero(f0.sum(0) > 0)[0]; i1 = np.nonzero(f1.sum(0) > 0)[0]
    UA = np.ascontiguousarray(A.UA[np.ix_(i0, i1)]); UB = np.ascontiguousarray(A.UB[np.ix_(i1, i0)])
    z = np.zeros(0, np.int64)
    cps = np.array([5, 20], np.int64)
    a0, a1 = M.lottery2(UA, UB, np.ascontiguousarray(f0[:, i0]), np.ascontiguousarray(f1[:, i1]), 60, M.W, 0.02, 5, cps)
    b0, b1 = S.lottery3(UA, UB, np.ascontiguousarray(f0[:, i0]), np.ascontiguousarray(f1[:, i1]), 60, M.W, 0.02, 5, cps, 0.0, 1, -1, z, z, z, z)
    assert (a0 == b0).all() and (a1 == b1).all()
    # rain matching: payoff-identical labels K and C, the swapped initial condition gives the label-swapped run bit for bit
    N, I = 40, 5
    UA2 = np.zeros((2, 2)); UB2 = np.zeros((2, 2))
    init0 = np.zeros((I, 2), np.int64); init0[:, 0] = N
    iC = np.zeros((I, 2), np.int64); iC[:, 0] = N          # all class 0
    iK = np.zeros((I, 2), np.int64); iK[:, 1] = N          # all class 1
    cps2 = np.array([10, 30], np.int64)
    r0a, r1a = S.lottery3(UA2, UB2, init0, iC, N, 0.3, 0.05, 123, cps2, 0.05, 1, 1, z, z, z, z)     # rain class 1 into a class-0 population
    r0b, r1b = S.lottery3(UA2, UB2, init0, iK, N, 0.3, 0.05, 123, cps2, 0.05, 1, 0, z, z, z, z)     # rain class 0 into a class-1 population
    assert (r1a[:, :, ::-1] == r1b).all()
    assert r1a[-1][:, 1].sum() > 0                          # the rain does arrive
    # scheduled arrivals: a single arrival at generation 3 puts one class-1 individual in every island at that time
    arr = S.lottery3(UA2, UB2, init0, iC, N, 0.3, 0.0, 5, np.array([3, 4], np.int64), 0.0, 1, -1, np.array([3], np.int64), np.array([1], np.int64),
                     np.array([1], np.int64), np.array([1], np.int64))
    assert (arr[1][0].sum(1) == N).all()
