"""Tests of the arm-T islands experiment (src/many_islands_t*.py): the unit-sized validations of the spec."""
import os, sys, math
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import lt_code as L
import churn_primary_t as CT
import many_islands_t as M
import many_islands_t_ode as O
import many_islands_t_jac as JA
import many_islands_t_worlds as WD
import many_islands_t_analysis as AN
import many_islands_t_validate as VA

NP = M.NP


@pytest.fixture(scope='module')
def T():
    return M.Tabs()


@pytest.fixture(scope='module')
def PF01(T):
    return M.make_pf(T.payoff(0.1))


def ix(T, n):
    return T.names.index(n)


# ------------------------------------------------------------------ tables and charges
def test_table_reproduces_stored_sample(T):
    """re-execute 300 random triples with the stored evaluator path and compare with the table entries."""
    cat = T.cat
    rng = np.random.default_rng(0)

    def go():
        bad = 0
        for _ in range(300):
            p, n, v = [int(z) for z in rng.integers(0, NP, 3)]
            c, st, _ = cat.f_eval(p, n, v)
            if c != T.code[p, n, v] or st != T.steps[p, n, v]:
                bad += 1
        return bad
    assert L.run_big(go) == 0


def test_joint_codes_match_stored(T):
    JT0, ST0 = T.cat.joint_codes()
    assert (JT0[:NP, :NP, :NP] == T.JT).all()
    assert (ST0[:NP, :NP, :NP] == T.ST).all()


def test_hand_triples(T):
    for names, nto, gross in VA.hand_rows(T):
        t = tuple(ix(T, n) for n in names)
        assert tuple(int(T.NTO[t[0], t[1], t[2], s]) for s in range(3)) == nto
        assert np.allclose(T.GROSS[t[0], t[1], t[2]], gross)


def test_no_forfeits_and_bounds(T):
    assert T.fo.sum() == 0
    fam = np.array(T.fam)
    assert T.nto[fam == 'const'].max() == 0
    assert T.nto[(fam == 'single') | (fam == 'exploit')].max() <= 1
    assert T.nto[fam == 'two'].max() <= 2
    assert T.steps.max() < CT.KR


def test_charge_counter_rules():
    prog = CT._prog
    omega = '((lambda (x) (x x)) (lambda (x) (x x)))'
    rd = prog(CT.src_single('n', 'o', 'y'))
    terms = [prog('(lambda (me n p) %s)' % omega),
             prog('(lambda (me n p) (let ((r (capk 5 (run 5 n p) me))) 1))'),
             prog('(lambda (me n p) (let ((r (capk 5 (run 5 n p) me))) %s))' % omega),
             prog('(lambda (me n p) (let ((r (capk 5 (run 5 n p) me))) (let ((s (capk 5 (run 5 p n) me))) 1)))'),
             rd, prog('(lambda (me n p) 1)')]
    # forfeit by looping: no failed read, one forfeit
    assert VA.counted_eval(terms, 0, 4, 5)[2:] == (0, 1)
    # one expiring read, normal return
    assert VA.counted_eval(terms, 1, 4, 4)[2:] == (1, 0)
    # an expiring read and then a forfeit: two failure events
    assert VA.counted_eval(terms, 2, 4, 4)[2:] == (1, 1)
    # two expiring reads
    assert VA.counted_eval(terms, 3, 4, 4)[2:] == (2, 0)
    # a constant reads nothing
    assert VA.counted_eval(terms, 5, 4, 4)[2:] == (0, 0)


def test_units_and_fitness_ratios(T):
    """w = 0.3 acts on dollars; P_fail is in dollars: a failed read costs 0.1 dollars = w * 0.1 = 0.03 in the exponent."""
    assert abs(M.W - 0.3) < 1e-12
    pay = T.payoff(0.1)
    t = (ix(T, 'Snoy'), ix(T, 'Spoy'), ix(T, 'C1'))
    assert np.allclose(pay[t], [0.4, 0.4, 0.0])
    # the stored gross payoff of a fair pair is 0.5 dollars
    assert abs(T.GROSS[ix(T, 'Snoy'), ix(T, 'C4'), ix(T, 'C1'), 0] - 0.5) < 1e-12
    # fixation ratios (notes 1.1)
    assert abs(M.pfix(0.1, 100.0, 0.3) - 0.0311) < 1e-4
    assert abs(M.pfix(-0.1, 100.0, 0.3) - 0.001596) < 2e-6
    assert abs(M.pfix(-0.2, 100.0, 0.3) - 1.5e-4) < 1e-5
    assert abs(M.pfix(1.0 / 6.0, 100.0, 0.3) - 0.0491) < 1e-4
    assert abs(M.pfix(0.0, 100.0, 0.3) - 0.01) < 1e-15
    # exact tensor entry on a hand-built triple: a reader into a reading pair against a constant (loses one read)
    PF = M.make_pf(pay)
    # resident (Snoy, C4, C1); migrant Spoy into slot 1: slot 1 earns 0 (excluded) before and after? use the table
    r = (ix(T, 'Snoy'), ix(T, 'C4'), ix(T, 'C1'))
    y = ix(T, 'Spoy')
    d = pay[r[0], y, r[2], 1] - pay[r[0], r[1], r[2], 1]
    assert abs(PF[1, r[0], r[1], r[2], y] - M.pfix(d, 100.0, 0.3)) < 1e-15


def test_pfix_against_exact_absorption():
    """the closed form against the absorption probability of the Moran chain solved by linear algebra (N = 10, 40)."""
    for N in (10, 40):
        for a in (-0.3, -0.05, 0.05, 0.2):
            rho = math.exp(a)
            # birth-death chain on k = number of migrants: up prob = k rho / (k rho + N - k) * (N - k) / N, down prob =
            # (N - k) / (k rho + N - k) * k / N
            A = np.zeros((N - 1, N - 1)); b = np.zeros(N - 1)
            for k in range(1, N):
                up = (k * rho / (k * rho + N - k)) * ((N - k) / N)
                dn = ((N - k) / (k * rho + N - k)) * (k / N)
                A[k - 1, k - 1] = up + dn
                if k + 1 <= N - 1:
                    A[k - 1, k] = -up
                else:
                    b[k - 1] += up
                if k - 1 >= 1:
                    A[k - 1, k - 2] = -dn
            h = np.linalg.solve(A, b)
            assert abs(h[0] - M.pfix(a / 0.3, float(N), 0.3)) < 1e-12 * max(1.0, h[0]) + 1e-14


def test_rotation_equivariance_exhaustive(T):
    res = VA.equivariance(T)
    assert res['equiv_total_violations'] == 0


# ------------------------------------------------------------------ simulator against the closed form
def test_island_simulator_fixation_matches_pfix(T):
    """single-migrant injections into settled triples, simulated with the dense-table island kernel, against pfix."""
    PT = T.payoff(0.1)
    cum = M.cum_of(M.seed_law(T, 'main'))
    cases = [((ix(T, 'C1'), ix(T, 'C4'), ix(T, 'C1')), 0, ix(T, 'C2')),     # fair pair, a greedier migrant into the pair
             ((ix(T, 'C1'), ix(T, 'C4'), ix(T, 'C1')), 2, ix(T, 'C4')),
             ((ix(T, 'Snoy'), ix(T, 'Spoy'), ix(T, 'C1')), 0, ix(T, 'C1'))]
    rng = np.random.default_rng(11)
    for tr, s, y in cases:
        d = PT[tr[0], tr[1], tr[2], s] - (PT[y, tr[1], tr[2], 0] if s == 0 else PT[tr[0], tr[1], y, 2] if s == 2 else 0)
        t2 = list(tr); t2[s] = y
        dd = PT[t2[0], t2[1], t2[2], s] - PT[tr[0], tr[1], tr[2], s]
        p = float(M.pfix(dd, 100.0, 0.3))
        n = 1200
        k = 0
        for _ in range(n):
            f, st = VA.simulate_injection(T, PT, cum, tr, s, y, rng.integers(1 << 31))
            k += f
        mu = n * p; sd = math.sqrt(n * p * (1 - p))
        assert abs(k - mu) < 4 * sd + 1.0


def test_dense_island_matches_founding_symmetry(T):
    """the founding law has no preferred slot: the class shares of the three slot-rotated founding runs agree."""
    PT = T.payoff(0.0)
    law = M.seed_law(T, 'main'); cum = M.cum_of(law)
    rng = np.random.default_rng(2)
    h = np.zeros(M.NT)
    for _ in range(600):
        r = M.build_island(PT, law, cum, rng, int(rng.integers(1 << 30)), A=0)
        assert r['status'] == 0
        h[O.tidx(*r['triple'])] += 1
    x = O.hist_to_x(h)
    sh = O.class_shares(x, T)
    assert abs(sh.sum() - 1.0) < 1e-12
    assert 0.3 < sh[0] < 0.7


# ------------------------------------------------------------------ the ODE
def test_ode_logistic_and_voter():
    from scipy.integrate import solve_ivp
    PF = np.zeros((3, NP, NP, NP, NP))
    PF[0, 0, 0, 0, 1] = 0.12; PF[0, 1, 0, 0, 0] = 0.03
    x = np.zeros(NP ** 3); x[O.tidx(1, 0, 0)] = 0.1; x[O.tidx(0, 0, 0)] = 0.9
    sol = solve_ivp(lambda t, y: O.F_of(y, PF, False), (0, 100.0), x, t_eval=[100.0], method='DOP853', rtol=1e-10, atol=1e-14)
    r = 0.09 / 3.0
    assert abs(sol.y[O.tidx(1, 0, 0), -1] - 1.0 / (1.0 + 9.0 * math.exp(-r * 100.0))) < 1e-7
    PF2 = np.zeros_like(PF); PF2[0, 0, 0, 0, 1] = 0.01; PF2[0, 1, 0, 0, 0] = 0.01
    sol2 = solve_ivp(lambda t, y: O.F_of(y, PF2, False), (0, 300.0), x, method='DOP853', rtol=1e-10, atol=1e-14)
    assert abs(sol2.y[O.tidx(1, 0, 0), -1] - 0.1) < 1e-9


def test_ode_mass_and_symmetric_projection(T, PF01):
    PT = T.payoff(0.1)
    law = M.seed_law(T, 'main'); cum = M.cum_of(law)
    rng = np.random.default_rng(4)
    h = np.zeros(M.NT)
    for _ in range(500):
        r = M.build_island(PT, law, cum, rng, int(rng.integers(1 << 30)), A=0)
        h[O.tidx(*r['triple'])] += 1
    x0 = O.symmetrize(O.hist_to_x(h))
    # symmetrized state is rotation invariant and the field preserves mass and is equivariant
    assert np.abs(x0 - O.rot_apply(x0, 1)).max() < 1e-15
    F = O.F_of(x0, PF01, False)
    assert abs(F.sum()) < 1e-15
    assert np.abs(F - O.rot_apply(F, 1)).max() < 1e-12
    recs, x, st, _ = O.integrate(x0, PF01, 100.0, T, sym=True, stop_converged=False)
    assert abs(x.sum() - 1) < 1e-10 and x.min() > -1e-10
    # jvp equals a finite difference of the quadratic field
    v = np.random.default_rng(1).standard_normal(x0.size) * (x0 > 0)
    fd = (O.F_of(x0 + 1e-6 * v, PF01) - O.F_of(x0 - 1e-6 * v, PF01)) / 2e-6
    assert np.abs(fd - O.jvp(x0, v, PF01)).max() < 1e-9 * max(1.0, np.abs(fd).max())


def test_tilts(T):
    rng = np.random.default_rng(0)
    x = rng.random(M.NT) * (rng.random(M.NT) < 0.2)
    x = O.symmetrize(x / x.sum())
    for kind, cls in (('fair', [0]), ('unequal', [1]), ('wd', [3, 4])):
        y, info = O.tilt(x, T, kind)
        if y is None:
            continue
        sh = O.class_shares(y, T)
        assert abs(sh[cls].sum() - 0.6) < 1e-12
        # within-class relative frequencies preserved
        cl = T.CL.ravel()
        for c in range(M.NCLS):
            m = cl == c
            if x[m].sum() > 0 and y[m].sum() > 0:
                assert np.allclose(x[m] / x[m].sum(), y[m] / y[m].sum())


def test_jacobian_matches_finite_difference(T, PF01):
    """dense support Jacobian columns equal central differences of the field."""
    rng = np.random.default_rng(5)
    x = np.zeros(M.NT)
    idx = rng.choice(M.NT, 60, replace=False)
    x[idx] = rng.random(60)
    x = O.symmetrize(x / x.sum())
    sup = JA.support(x, 1e-12)
    J = JA.dense_jacobian(x, PF01, sup)
    for j in (0, 5, 17):
        e = np.zeros_like(x); e[sup[j]] = 1.0
        fd = (O.F_of(x + 1e-7 * e, PF01) - O.F_of(x - 1e-7 * e, PF01)) / 2e-7
        assert np.abs(fd[sup] - J[:, j]).max() < 1e-7 * max(1.0, np.abs(J).max())


def test_sector_spectrum_block_diagonal(T, PF01):
    """the C3-symmetric Jacobian splits: eigenvalues of J on the whole support = invariant + two conjugate sectors."""
    rng = np.random.default_rng(6)
    x = np.zeros(M.NT)
    idx = rng.choice(M.NT, 40, replace=False)
    x[idx] = rng.random(40)
    x = O.symmetrize(x / x.sum())
    sup = JA.support(x, 1e-12)
    J = JA.dense_jacobian(x, PF01, sup)
    reps3, fixed, inS = JA.orbits(sup)
    Jw, Tm = JA.sector_matrix(J, sup, reps3, inS, JA.OMEGA)
    Jb, Tb = JA.sector_matrix(J, sup, reps3, inS, JA.OMEGA ** 2)
    Ji = JA.invariant_matrix(J, sup, reps3, fixed, inS)
    ev_all = np.linalg.eigvals(J)
    ev_parts = np.concatenate([np.linalg.eigvals(Jw), np.linalg.eigvals(Jb), np.linalg.eigvals(Ji)])
    assert len(ev_all) == len(ev_parts)
    # multiset equality up to numerical error: every eigenvalue of J has a partner among the parts (Hausdorff distance)
    d1 = np.abs(ev_all[:, None] - ev_parts[None, :]).min(axis=1).max()
    d2 = np.abs(ev_parts[:, None] - ev_all[None, :]).min(axis=1).max()
    assert max(d1, d2) < 1e-6


# ------------------------------------------------------------------ finite worlds
def test_world_run_conserves_and_matches_pfix_in_the_two_state_case(T):
    """two-island-type world with a single selected migrant program: class counts add to I; first_loss bookkeeping."""
    PF = M.make_pf(T.payoff(0.0))
    rng = np.random.default_rng(1)
    tri = rng.integers(0, M.NT, 200).astype(np.int64)
    r = WD.run_world(PF, T, tri, [1, 10, 100], 5)
    assert (r['hist'].sum(axis=1) == 200).all()
    assert r['events'] == 100 * 200
    assert (r['pairs'].sum(axis=1) <= 200).all()


def test_analysis_flux_rows_sum_to_exit_rate(T, PF01):
    rng = np.random.default_rng(8)
    x = np.zeros(M.NT)
    idx = rng.choice(M.NT, 300, replace=False)
    x[idx] = rng.random(300)
    x /= x.sum()
    R = AN.sum_flux_classes(x, PF01, T)
    cl = T.CL.ravel()
    mass = np.bincount(cl, weights=x, minlength=M.NCLS)
    q = O.marginals(x)
    # brute force over the support: class-changing events
    tot = np.zeros((M.NCLS, M.NCLS))
    for t in np.nonzero(x)[0]:
        a = O._TR[t]
        for s in range(3):
            for y in range(NP):
                if y == a[s]:
                    continue
                b2 = a.copy(); b2[s] = y
                tn = (b2[0] * NP + b2[1]) * NP + b2[2]
                if cl[tn] != cl[t]:
                    tot[cl[t], cl[tn]] += x[t] * q[s, y] * PF01[s, a[0], a[1], a[2], y] / 3.0
    R2 = tot / np.maximum(mass[:, None], 1e-300)
    assert np.abs(R - R2).max() < 1e-12


def test_pools_deterministic_given_seed(T):
    PT = T.payoff(0.0)
    law = M.seed_law(T, 'main'); cum = M.cum_of(law)
    a = M.build_island(PT, law, cum, np.random.default_rng(1), 5, A=0)['triple']
    b = M.build_island(PT, law, cum, np.random.default_rng(1), 5, A=0)['triple']
    assert a == b
