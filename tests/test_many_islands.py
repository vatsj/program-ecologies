"""Tests for src/many_islands.py (spec specs/2026-10-25-many-islands.md; notes notes/many-islands.md section 1).

 - the Moran fixation formula against an exact absorption solve;
 - the island kernel reproduces `stable_sets.kern` (I = 1, m = 0) draw for draw, and settles / caps as specified;
 - the one-migrant event: simulated fixation frequencies against the closed form (neutral and selected);
 - S3 equivariance: prior, readers' law, evaluator, payoffs and the one-event kernel (notes 1.4);
 - the class-level ODE on a hand-built 3-state kernel with a known solution; mass conservation and nonnegativity;
 - the pool chain against the exact expectation; the founding shares reproduce the stored L, mN = 0 cell.
"""
import os, sys, itertools, math
import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'src'))
import many_islands as MI
import stable_sets as SS
import dollar3 as D

_ARM = {}


def arm(name='L'):
    if name not in _ARM:
        _ARM[name] = MI.Arm(name)
    return _ARM[name]


def const(a, s, partner, d):
    """program index of the constant (partner, demand d in 0, 1, 2) of slot s in arm L's catalogue."""
    ci = SS.const_index(arm('L').S.fs)
    return ci[D.local_of(s, partner, d)]


def counts_of(tr, K, N=100):
    c = np.zeros((3, K), np.int64)
    for s in range(3):
        c[s, tr[s]] = N
    return c


def run(a, init, seed, H=4000, arr=None, mono=True, L=32):
    arr = np.empty(0) if arr is None else arr
    return MI.island_run(a.ctx(), a.lc(L), MI.PAY, init, 100, MI.W, seed, H, arr, a.cum, mono)


# ---------------------------------------------------------------------------------------------- Moran formula
def moran_exact(dpay, N, w):
    """absorption probability at N from state 1 of the birth-death chain with parent ~ count * exp(w pay), victim uniform."""
    rho = math.exp(w * dpay)
    P = np.zeros((N + 1, N + 1))
    for i in range(1, N):
        up = (i * rho / (i * rho + N - i)) * ((N - i) / N)
        dn = ((N - i) / (i * rho + N - i)) * (i / N)
        P[i, i + 1] = up; P[i, i - 1] = dn; P[i, i] = 1 - up - dn
    # solve h = P h with h(0) = 0, h(N) = 1
    A = np.eye(N - 1) - P[1:N, 1:N]
    b = P[1:N, N]
    h = np.linalg.solve(A, b)
    return h[0]


@pytest.mark.parametrize('dpay', [0.0, 1 / 6, 2 / 6, 3 / 6, -1 / 6, -2 / 6, 4 / 6])
def test_pfix_matches_absorption_solve(dpay):
    for N in (10, 40, 100):
        ex = moran_exact(dpay, N, MI.W)
        assert MI.pfix_py(dpay, N) == pytest.approx(ex, rel=1e-6, abs=1e-14)


def test_pfix_values_of_notes():
    # notes 1.2 table (sixths)
    tab = {-3: 3e-8, -2: 5e-6, -1: 3.5e-4, 0: 0.01, 1: 0.049, 2: 0.095, 3: 0.139, 4: 0.181}
    for d6, v in tab.items():
        got = MI.pfix_py(d6 / 6)
        assert got == pytest.approx(v, rel=0.7 if d6 < 0 else 0.03), (d6, got, v)


# ---------------------------------------------------------------------------------------------- the island kernel
def kern_final(a, init, seed, H):
    loc, U = SS.compress(init[None])
    J = SS.joint_for('weak', U)
    T = MI.T
    out = SS.kern(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, 100, MI.W, 0.0, seed, H, H + 10, np.zeros(0, np.int64), 1000)
    counts = out[2][0]                               # (3, Kmax) local
    full = np.zeros(init.shape, np.int64)
    for s in range(3):
        full[s, U[s]] = counts[s, :len(U[s])]
    return full


def test_kernel_draw_for_draw_founders():
    a = arm('L')
    rng = np.random.default_rng(3)
    for k in range(5):
        init = np.stack([rng.multinomial(100, a.laws[s]) for s in range(3)]).astype(np.int64)
        H = 2500
        st, g, counts, narr = run(a, init, 100 + k, H=H)
        assert st == 0
        ref = kern_final(a, init, 100 + k, H)
        assert (counts == ref).all(), k


def test_kernel_draw_for_draw_one_migrant():
    a = arm('L')
    rng = np.random.default_rng(5)
    K = a.K
    wasteful = (const(a, 0, 1, 0), const(a, 1, 0, 0), const(a, 2, 0, 1))
    cases = [(wasteful, 0, const(a, 0, 1, 1)), (wasteful, 0, const(a, 0, 1, 2)), (wasteful, 1, const(a, 1, 0, 2)),
             (wasteful, 2, const(a, 2, 1, 1))]
    for n, (tr, s, x) in enumerate(cases):
        init = counts_of(tr, K)
        init[s, tr[s]] -= 1; init[s, x] += 1
        for seed in (11, 12, 13):
            st, g, counts, narr = run(a, init, seed * 7 + n, H=1500)
            ref = kern_final(a, init, seed * 7 + n, 1500)
            assert (counts == ref).all(), (n, seed)


def test_settlement_neutral_slot_drifts_to_monomorphism():
    a = arm('L'); K = a.K
    # fair pair {0,1}; excluded slot 2 split between two constants that both leave the play unchanged
    t0 = (const(a, 0, 1, 1), const(a, 1, 0, 1), const(a, 2, 0, 2))
    x = const(a, 2, 1, 0)
    init = counts_of(t0, K)
    init[2, t0[2]] = 50; init[2, x] = 50
    fixed = 0; n = 120
    for seed in range(n):
        st, g, counts, narr = run(a, init, seed)
        assert st == 0
        tr = MI.triple_of(counts)
        assert tr is not None and tr[:2] == t0[:2]
        fixed += tr[2] == x
    assert abs(fixed - n / 2) < 4 * math.sqrt(n / 4)


def test_selected_type_fixes_and_cap_is_reported():
    a = arm('L'); K = a.K
    t0 = (const(a, 0, 1, 1), const(a, 1, 0, 1), const(a, 2, 0, 2))
    worse = const(a, 0, 1, 0)                         # demands 1/3: pair still forms, payoff 2 < 3
    init = counts_of(t0, K)
    init[0, t0[0]] = 50; init[0, worse] = 50
    for seed in range(20):
        st, g, counts, narr = run(a, init, seed)
        assert st == 0 and MI.triple_of(counts)[0] == t0[0]
    st, g, counts, narr = run(a, init, 1, H=1)       # cap: not settled, reported as such
    assert st == 1 and MI.triple_of(counts) is None


def test_arrivals_are_delivered_and_island_settles():
    a = arm('L'); K = a.K
    t0 = (const(a, 0, 1, 1), const(a, 1, 0, 1), const(a, 2, 0, 2))
    init = counts_of(t0, K)
    arr = np.array([5.0, 30.0, 400.0])
    st, g, counts, narr = run(a, init, 3, H=3000, arr=arr, L=32)
    assert st == 0 and narr == 3 and MI.triple_of(counts) is not None
    # the schedule has a finite last arrival
    rng = np.random.default_rng(0)
    t = MI.arrival_times(rng, 150)
    assert t.min() >= 200.0 and np.isfinite(t.max()) and 100 < len(t) < 200


# ---------------------------------------------------------------------------------------------- the event, simulated vs closed form
def simulated_fix(a, tr, s, x, n, seed0):
    K = a.K
    fixed = 0
    for k in range(n):
        init = counts_of(tr, K)
        init[s, tr[s]] -= 1; init[s, x] += 1
        st, g, counts, narr = run(a, init, seed0 + k, H=6000)
        assert st == 0
        fixed += MI.triple_of(counts)[s] == x
    return fixed


def test_event_formula_selected():
    a = arm('L')
    tr = (const(a, 0, 1, 0), const(a, 1, 0, 0), const(a, 2, 0, 1))     # wasteful (2, 2, 0)
    x = const(a, 0, 1, 1)                                               # slot 0 asks 1/2: payoff 3 vs 2, +1 sixth
    p, new = MI.event_prob(a, tr, 0, x)
    assert p == pytest.approx(MI.pfix_py(1 / 6)) and new[0] == x
    n = 1500
    f = simulated_fix(a, tr, 0, x, n, 1000)
    assert abs(f - n * p) < 4.5 * math.sqrt(n * p * (1 - p))


def test_event_formula_neutral_and_deleterious():
    a = arm('L')
    tr = (const(a, 0, 1, 1), const(a, 1, 0, 1), const(a, 2, 0, 2))     # fair {0,1}
    x = const(a, 2, 1, 0)                                               # excluded slot: payoff 0 either way
    p, _ = MI.event_prob(a, tr, 2, x)
    assert p == pytest.approx(0.01)
    n = 2500
    f = simulated_fix(a, tr, 2, x, n, 5000)
    assert abs(f - n * p) < 4.5 * math.sqrt(n * p * (1 - p))
    bad = const(a, 0, 1, 2)                                             # asks 2/3 of a 1/2 partner: disagreement
    p2, _ = MI.event_prob(a, tr, 0, bad)
    assert p2 < 1e-6
    assert simulated_fix(a, tr, 0, bad, 300, 9000) == 0


# ---------------------------------------------------------------------------------------------- S3 equivariance
SIGMAS = [s for s in itertools.permutations(range(3))]


@pytest.mark.parametrize('name', ['L', 'R'])
def test_prior_and_laws_invariant_under_S3(name):
    a = arm(name)
    for sigma in SIGMAS:
        perm = MI.permute_support(a, sigma)
        for s in range(3):
            ts = sigma[s]
            sup = a.laws[s] > 0
            img = perm[s][sup]
            assert (img >= 0).all()
            assert np.allclose(a.laws[ts][img], a.laws[s][sup]), (name, sigma, s)


@pytest.mark.parametrize('name', ['L', 'M', 'R'])
def test_evaluator_and_payoffs_equivariant(name):
    a = arm(name)
    rng = np.random.default_rng(11)
    ctx = a.ctx()
    for _ in range(300):
        tr = tuple(int(rng.choice(a.K, p=a.laws[s])) for s in range(3))
        c = int(MI.jl(ctx, *map(np.int64, tr)))
        assert c >= 0
        for sigma in SIGMAS:
            perm = MI.permute_support(a, sigma)
            tr2 = [0, 0, 0]
            for s in range(3):
                tr2[sigma[s]] = int(perm[s][tr[s]])
            c2 = int(MI.jl(ctx, *map(np.int64, tr2)))
            for s in range(3):
                assert MI.PAY[c2, sigma[s]] == pytest.approx(MI.PAY[c, s]), (name, tr, sigma)
            assert MI.CATMAP[MI.VEC[c2]] == MI.CATMAP[MI.VEC[c]]


@pytest.mark.parametrize('name', ['L', 'R'])
def test_one_event_kernel_equivariant(name):
    a = arm(name)
    rng = np.random.default_rng(13)
    for _ in range(200):
        tr = tuple(int(rng.choice(a.K, p=a.laws[s])) for s in range(3))
        s = int(rng.integers(3)); x = int(rng.choice(a.K, p=a.laws[s]))
        p, new = MI.event_prob(a, tr, s, x)
        for sigma in SIGMAS:
            perm = MI.permute_support(a, sigma)
            tr2 = [0, 0, 0]
            for t in range(3):
                tr2[sigma[t]] = int(perm[t][tr[t]])
            p2, new2 = MI.event_prob(a, tuple(tr2), sigma[s], int(perm[s][x]))
            assert p2 == pytest.approx(p, rel=1e-9, abs=1e-15)


def test_reader_catalogue_reflection_symmetric():
    a = arm('R')
    K0 = a.cat.K0
    assert a.K == K0 + 12
    laws = a.laws
    # reader mass about 9% per slot (notes 1.4)
    for s in range(3):
        idx = [a.cat.idx[(s, k)] for k in ('Sj', 'Sk', 'Zj', 'Zk', 'R2jf', 'R2jz', 'R2kf', 'R2kz')]
        m = laws[s][idx].sum()
        assert 0.09 <= m < 0.095, m
    # the swap of the owner's two others is a symmetry of each slot's law
    for s in range(3):
        j, k = D.others(s)
        sigma = [0, 1, 2]; sigma[j], sigma[k] = k, j
        sigma = tuple(sigma)
        perm = MI.permute_support(a, sigma)
        sup = laws[s] > 0
        assert np.allclose(laws[s][perm[s][sup]], laws[s][sup])


# ---------------------------------------------------------------------------------------------- the class-level ODE
def test_ode_logistic_known_solution():
    NC = 3
    K = np.zeros((NC, NC, NC))
    for a_ in range(NC):
        for b_ in range(NC):
            K[a_, b_, a_] = 1.0
    p = 0.3
    K[0, 1, 0] = 1 - p; K[0, 1, 1] = p                   # class 0 hit by a class-1 donor becomes 1 with prob p
    x0 = np.array([0.9, 0.1, 0.0])
    ts, X_ = MI.ode_integrate(K, x0, 50.0, n_out=20)
    for t, x in zip(ts, X_):
        y = 0.1 * math.exp(p * t) / (0.9 + 0.1 * math.exp(p * t))
        assert x[1] == pytest.approx(y, abs=1e-6)
        assert x[2] == pytest.approx(0.0, abs=1e-9)
        assert x.sum() == pytest.approx(1.0, abs=1e-9)


def test_ode_mass_conserved_and_nonnegative():
    rng = np.random.default_rng(2)
    NC = 6
    K = rng.random((NC, NC, NC)) ** 3
    K /= K.sum(axis=2, keepdims=True)
    x0 = rng.dirichlet(np.ones(NC))
    ts, X_ = MI.ode_integrate(K, x0, 200.0, n_out=30)
    assert np.allclose(X_.sum(axis=1), 1.0, atol=1e-8)
    assert (X_ > -1e-9).all()
    assert abs(MI.ode_rates(K, x0).sum()) < 1e-12


# ---------------------------------------------------------------------------------------------- pool chain vs exact expectation
def test_chain_fixation_rate_matches_exact_expectation():
    a = arm('L')
    rng = np.random.default_rng(21)
    isl = [MI.build_island(a, rng, 700 + k, 0) for k in range(120)]
    pool = np.array([r['triple'] for r in isl if r['triple'] is not None], np.int64)
    I = len(pool)
    ctx = a.ctx()
    # exact expected fixations per event
    rec = np.repeat(np.arange(I), I - 1); don = np.concatenate([[j for j in range(I) if j != i] for i in range(I)])
    out = np.zeros((MI.NOUT, MI.NOUT, MI.NOUT)); npair = np.zeros((MI.NOUT, MI.NOUT)); outslot = np.zeros((MI.NOUT, 3, 2))
    MI.exact_rates(ctx, MI.PAY, MI.VEC, pool, rec.astype(np.int64), don.astype(np.int64), 100, MI.W, out, npair, outslot)
    exp_fix = outslot[:, :, 0].sum() / (3.0 * len(rec))            # per event, summed over slots / 3 and pairs
    E = 40000
    cps = np.array([E], np.int64)
    hist = np.zeros((1, MI.NOUT), np.int64); Kc = np.zeros((1, 1, 1, 1), np.int64); dr = np.zeros((1, MI.NOUT, 3), np.int64)
    fl = np.zeros(3, np.int64)
    p2 = pool.copy()
    MI.chain_run(ctx, MI.PAY, MI.VEC, MI.EXCL, p2, I, E, cps, 5, 100, MI.W, hist, False, Kc, dr, fl, np.array(MI.V, np.int64))
    changed = (p2 != pool).any(axis=1).sum()
    # every fixation changes one program; the pool changes slowly so the initial rate is a fair expectation
    assert hist.sum() == I
    assert changed > 0.3 * E * exp_fix and changed < 1.7 * E * exp_fix, (changed, E * exp_fix)


# ---------------------------------------------------------------------------------------------- founding reproduces the stored cell
def test_founding_reproduces_stored_L_mN0_cell():
    """stored: fair 0.281 [0.263, 0.300] of islands at generation 2,000 (L, mN = 0, 40 runs of 64 islands)."""
    a = arm('L')
    rng = np.random.default_rng(99)
    n = 700
    nf = 0
    for k in range(n):
        init = np.stack([rng.multinomial(100, a.laws[s]) for s in range(3)]).astype(np.int64)
        st, g, counts, narr = MI.island_run(a.ctx(), a.lc(32), MI.PAY, init, 100, MI.W, 4000 + k, 2000, np.empty(0), a.cum, True)
        c, e = MI.classify_counts(a, counts)
        nf += (c < MI.NOUT and MI.CATMAP[c] == 0)
    f = nf / n
    se = math.sqrt(0.281 * 0.719 / n)
    assert abs(f - 0.281) < 3.5 * se + 0.01, f
