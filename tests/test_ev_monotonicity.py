"""Tests of src/ev_monotonicity.py: the payoff modifications and the kernel they induce."""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import many_islands_t as M
import ev_monotonicity as E


@pytest.fixture(scope='module')
def T():
    return M.Tabs()


def test_identity(T):
    assert np.array_equal(E.modified_payoff(T, 0.1), T.payoff(0.1))


def test_penalty_touches_only_positive_nonfair(T):
    d = T.GROSS - (E.modified_payoff(T, 0.0, c=0.1))
    cl = np.broadcast_to(T.CL[..., None], d.shape)
    pos = T.GROSS > 1e-12
    assert np.allclose(d[(cl == 0) | (cl == 4)], 0)           # fair pairs and disagreement unchanged
    m = np.isin(cl, (1, 2, 3))
    assert np.allclose(d[m & pos], 0.1) and np.allclose(d[m & ~pos], 0)


def test_bonus_only_f0_slots_01(T):
    d = E.modified_payoff(T, 0.0, b=1 / 6) - T.GROSS
    f0 = T.PAIR == 0
    assert np.allclose(d[f0][:, :2], 1 / 6) and np.allclose(d[f0][:, 2], 0)
    assert np.allclose(d[~f0], 0)
    assert np.allclose(T.GROSS[f0][:, :2], 0.5)               # F0 = (1/2, 1/2, 0)


def test_penalty_rotation_equivariant(T):
    P = E.modified_payoff(T, 0.1, c=0.1)
    n = M.NP
    # rotation R (a0, a1, a2) = (a2, a0, a1); slot s payoff of t equals slot s+1 payoff of R t
    PR = np.transpose(P, (2, 0, 1, 3))                        # PR[a2, a0, a1, s]  <- P[a0, a1, a2, s]
    # P[R t][s+1] == P[t][s]
    Q = np.empty_like(P)
    for a0 in range(0, n, 5):
        for a1 in range(0, n, 5):
            for a2 in range(0, n, 5):
                for s in range(3):
                    assert abs(P[a2, a0, a1, (s + 1) % 3] - P[a0, a1, a2, s]) < 1e-12


def test_bonus_breaks_symmetry_only_in_f0(T):
    P0 = E.modified_payoff(T, 0.1)
    P1 = E.modified_payoff(T, 0.1, b=1 / 12)
    assert (np.abs(P1 - P0).sum(axis=-1) > 0).sum() == (T.PAIR == 0).sum()
