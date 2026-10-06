"""Regression tests for the two failure modes of the lazy linear-domain chain where deep polymorphisms exist
(specs/2026-10-05-solver-audit.md, item 5):

 (i)  underflow: a hand-built class table with one deep hawk-dove polymorphism G whose exits underflow in double
      precision at N = 10^4; the published linear solve is wrong, the log-domain solve matches mpmath (50 digits);
 (ii) missed-state exploration: a deep polymorphism reachable only through a sub-threshold flow (a hawk of prior
      mass 1e-12 entering an accommodating shadow); the lazy exploration (eager_poly=False, theta = 1e-7) never
      expands it, the class-table enumeration finds it, and the seeded log-domain chain puts pi on it.

    python3 -m pytest tests/test_solver_deep.py -q
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from chain import Chain
from chain_log import LogChain, linear_stationary, gth_mp, stationary_log
from dollar_partitions import ClassProvider
from solver_audit import enumerate_candidates

N = 10000
W = 0.3


def _key_of(ch, ids):
    for k, (i, x, kind) in ch.states.items():
        if tuple(sorted(i)) == tuple(sorted(ids)):
            return k
    return None


def test_underflow_deep_polymorphism():
    # 0 E (a fair convention), 1 H (hawk), 2 D (dove); G = H 2/3 + D 1/3 is a deep hawk-dove polymorphism
    U = np.array([[0.5, -2.0, -2.0],
                  [0.2, 0.0, 1.0],
                  [0.2, 0.25, 0.5]])
    mu = np.array([0.5, 0.25, 0.25])
    cands, _ = enumerate_candidates(U, mu)
    deep = [c for c in cands if c['deep'] and c['size'] == 2]
    assert len(deep) == 1 and sorted(deep[0]['ids']) == [1, 2]
    # published lazy linear chain (the dollar config): its stationary answer
    ch = LogChain(ClassProvider(U, mu), N=N, w=W, theta=1e-7).explore()
    keys, pi_lin, nc, nt, ae = linear_stationary(ch.trans, ch.seed_weight, ch.states)
    kG = _key_of(ch, (1, 2))
    assert kG in keys
    # some edge out of G underflowed to exactly 0 in the linear weights
    assert ch.underflow > 0
    _, LA, lpi, info, _ = ch.solve(keys)
    lmp = gth_mp(LA, 50)
    fin = np.isfinite(lmp)
    assert np.allclose(lpi[fin], lmp[fin], atol=1e-9, rtol=0)
    iG = keys.index(kG)
    assert np.exp(lmp[iG]) > 0.999                      # truth: the deep polymorphism holds pi
    assert abs(pi_lin[iG] - np.exp(lmp[iG])) > 0.1      # the linear solve is wrong (0.5)


def test_missed_deep_state_exploration():
    # 0 E (fair convention), 1 D (accommodating shadow of E), 2 H (hawk, prior mass 1e-12)
    U = np.array([[0.5, 0.5, 0.1],
                  [0.5, 0.5, 0.25],
                  [0.2, 1.0, 0.0]])
    mu = np.array([0.5, 0.5 - 1e-12, 1e-12])
    lazy = Chain(ClassProvider(U, mu), N=N, w=W, theta=1e-7, eager_poly=False).explore()
    assert _key_of(lazy, (1, 2)) is None or _key_of(lazy, (1, 2)) not in lazy.trans   # never expanded
    cands, _ = enumerate_candidates(U, mu)
    deep = [c for c in cands if c['deep'] and c['size'] > 1]
    assert len(deep) == 1 and sorted(deep[0]['ids']) == [1, 2]
    lc = LogChain(ClassProvider(U, mu), N=N, w=W).explore_log(extra_states=[(deep[0]['ids'], deep[0]['x'])])
    keys, LA, lpi, info, _ = lc.solve()
    kG = _key_of(lc, (1, 2))
    lmp = gth_mp(LA, 50)
    fin = np.isfinite(lmp)
    assert np.allclose(lpi[fin], lmp[fin], atol=1e-9, rtol=0)
    assert np.exp(lpi[keys.index(kG)]) > 0.99
    # the lazy chain puts no mass on it at all
    assert sum(p for k, p in zip(lazy.keys_list, lazy.pi) if len(lazy.states[k][0]) > 1) == 0.0


def test_log_gth_matches_mpmath_random():
    rng = np.random.default_rng(7)
    n = 9
    LA = rng.normal(-200, 400, (n, n))
    np.fill_diagonal(LA, -np.inf)
    LA[rng.random((n, n)) < 0.25] = -np.inf
    for i in range(n):              # keep it irreducible: a cycle
        LA[i, (i + 1) % n] = max(LA[i, (i + 1) % n], -900.0)
    lpi, info = stationary_log(LA)
    lmp = gth_mp(LA, 60)
    assert info['n_closed'] == 1
    assert np.allclose(lpi, lmp, atol=1e-9, rtol=0)
