"""Tests for the farsighted-refusal experiment (spec specs/2026-10-14-farsighted-refusal.md, required tests):
the g1 freezing set; the KR fixed-point equations at the reported solutions; gKR-read = gKR on monomorphic islands;
g0 reproduces D1 (and gV reproduces R2) draw for draw.

    python3 -m pytest tests/test_farsighted_refusal.py -q
"""
import json, os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import numpy as np
import stable_sets as SS
import stable_sets_run as SR
import dominance_contracts as DC
import farsighted_refusal as F
import farsighted_refusal_run as R


def _small(sd, mN, law='L', I=8, N=30):
    p = dict(law=law, mN=mN, arm='weak', I=I, N=N, name='val')
    loc, U, J, conds, I_, N_ = SR.build_run(p, sd)
    return loc, U, I, N


def _same(a, b):
    return (a[0] == b[0] and a[1] == b[1] and (a[3] == b[3]).all() and a[8] == b[8]
            and (a[11][:, [0, 1, 4, 5, 6]] == b[11][:, [0, 1, 4, 5, 6]]).all())


def test_g1_freezing_set():
    fs = F.freezing_set(F.table_g1('y'))
    assert set(fs) == set(F.LAB) - {'X'}
    assert set(F.freezing_set(F.table_g1('x'))) == set(F.LAB)
    # exposure: every member of a fair or wasteful pair is exposed; of an unequal pair only the 4-member
    for y, x in enumerate(F.X):
        if F.CAT[y] in ('fair', 'wasteful'):
            assert all(F.exposed(x, i) for i in range(3) if x[i] > 0)
        if F.CAT[y] == 'unequal':
            for i in range(3):
                if x[i] == 4: assert F.exposed(x, i)
                if x[i] == 2: assert not F.exposed(x, i)


def test_proposal_counts():
    n = {F.LAB[y]: int(F.PROPM[y].sum()) for y in range(F.NX)}
    assert F.NP == 90
    assert n['P12:3|3'] == 2 and n['P12:4|2'] == 3 and n['P12:3|2'] == 4 and n['P12:2|2'] == 7
    assert n['G(2,2,2)'] == 3 and n['X'] == 18


def test_exact_solvers_agree():
    rng = np.random.default_rng(0)
    for d in (0.9, 0.99):
        acc = tuple(int(v) for v in rng.integers(0, 2, F.NP))
        Wex = F.exact_values(acc, d)
        Mat, rhs = F.int_matrix(acc, d)
        det, nums = F.bareiss_solve(Mat, rhs)
        from fractions import Fraction
        assert all(Fraction(nums[i][c], det) == Wex[i][c] for i in range(F.NX) for c in range(3))
        Wf = F.values(np.array(acc), d)
        assert np.abs(Wf - np.array([[float(v) for v in r] for r in Wex])).max() < 1e-10


def test_kr_fixed_points_hold():
    S = json.load(open(R.STATIC))
    for dk, ent in S['deltas'].items():
        d = float(dk)
        for o in ent['orbits']:
            for acc in o['members']:
                st, mmin, ties = F.exact_check(tuple(acc), d)
                assert st == 'strict', (dk, st)
        st, _, _ = F.exact_check(tuple(ent['default']['acc']), d)
        assert st == 'strict'
        # the default is one of the listed fixed points when the list is complete
        if ent['complete']:
            assert ent['default']['in_list']


def test_reader_equals_kr_on_monomorphic_islands():
    # unit: the plug-in reader's values under an all-gKR composition are the default fixed point's
    names = ['g0', 'gKR0.99', 'read0.99']
    ga = R.guard_arrays(names)
    T, d, W, acc = R.kr_table('0.99')
    N = 100
    for gc in (np.array([[0, 100, 0]] * 3), np.array([[0, 0, 100]] * 3), np.array([[0, 40, 60], [0, 100, 0], [0, 7, 93]])):
        for s in range(3):
            Wr = F.reader_values(gc.astype(np.int64), N, ga['GKIND'], ga['GTAB'], ga['KRTAB'], F.PROPM, F.CS_, F.CX,
                                 F.UPAY, d, s)
            assert np.abs(Wr - W[:, s]).max() < 1e-9
            for y in range(F.NX):
                for k in range(F.NCON):
                    for z in range(2):
                        if F.CS_[k, z] == s and F.FEAS[k]:
                            assert (Wr[F.CX[k]] > Wr[y]) == T[y, k, z]
    # kernel: universal gKR-read reproduces universal gKR draw for draw
    Tt = R.DR.tables()
    for sd, mN in ((1, 0), (2, 1)):
        loc, U, I, N = _small(sd, mN)
        outs = []
        for nm in (['g0', 'gKR0.99'], ['g0', 'read0.99']):
            st = F.Setup(loc, U, 2, assign=('bit', 1.0, 1), rng=None)
            outs.append(F.run_fkern(st, Tt, N, mN, 500 + sd, 300, np.array([300], np.int64), R.guard_arrays(nm), nu=0.1))
        assert _same(outs[0], outs[1])
        assert (outs[0][11][:, 3] == outs[1][11][:, 3]).all()


def test_g0_reproduces_D1_and_gV_reproduces_R2():
    Tt = R.DR.tables()
    for sd, mN in ((1, 0), (2, 1), (3, 1)):
        loc, U, I, N = _small(sd, mN)
        seed = 900 + sd; hrec = np.array([300], np.int64)
        a = DC.run_kernel(DC.Setup(loc, U), Tt, N, mN, seed, 300, hrec, nu=0.1)
        b = F.run_fkern(F.Setup(loc, U, 1), Tt, N, mN, seed, 300, hrec, R.guard_arrays(['g0']), nu=0.1)
        assert _same(a, b)
        a = DC.run_kernel(DC.Setup(loc, U, fr=1.0, rng=np.random.default_rng(0)), Tt, N, mN, seed, 300, hrec, nu=0.1,
                          consent=DC.CONSENT['public'])
        b = F.run_fkern(F.Setup(loc, U, 2, assign=('bit', 1.0, 1)), Tt, N, mN, seed, 300, hrec,
                        R.guard_arrays(['g0', 'gV']), nu=0.1)
        assert _same(a, b)
        assert (a[11][:, 3] == b[11][:, 3]).all()        # guard firings = consultations


def test_forced_island_jump_is_the_table():
    """a homogeneous constant island moves only by contracts the table accepts (one event per island per check)."""
    T, d, W, acc = R.kr_table('0.99')
    Q = F.event_chain(acc)
    for y in range(F.NX):
        for x in range(F.NX):
            if x != y and Q[y, x] > 0:
                assert any(F.PY[j] == y and F.PXX[j] == x and acc[j] for j in range(F.NP))
