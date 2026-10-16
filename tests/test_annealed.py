"""Tests for annealed mutation (notes/annealed.md §1.7).  The kernel tests need the untracked cached tables
(runs/provenance/static, runs/lt_genes/static, ...) and skip without them."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAVE = os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'static')) and \
    os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'OSV.npy'))
need = pytest.mark.skipif(not HAVE, reason='cached tables absent')


def _sched_only():
    """The schedule functions without loading the tables."""
    import importlib.util
    src = open(os.path.join(ROOT, 'src', 'annealed.py')).read()
    ns = {'__file__': os.path.join(ROOT, 'src', 'annealed.py')}
    head = src[:src.index('# ------------------------------------------------------------------------------------------------ cells')]
    head = head.replace('import provenance as PV', '').replace('import provenance_run as PR', '') \
        .replace('import realizable_scaling as RS', '').replace('import removing_rivals as RR', '') \
        .replace('import annealed_kern as AK', '').replace("ROOT = RR.ROOT", "ROOT = '.'")
    exec(head, ns)
    return ns


def test_schedule_integrates():
    ns = _sched_only()
    A = ns['arrivals_A'](3)
    assert abs(A - 156.195) < 0.01
    for N in (200, 400, 800, 1600):
        en = ns['eps_n_annealed'](N, A)
        assert en[:200].sum() == 0.0 and en[200] > 0
        T, t0 = 9800, N / 2
        assert abs(en.sum() - A * T / (T + t0)) < 1e-9
        assert abs(en.sum() - ns['delivered'](N, A)) < 1e-9
        ec = ns['eps_n_constant'](N, A)
        assert abs(ec.sum() - en.sum()) < 1e-9 and ec[:200].sum() == 0 and np.ptp(ec[200:]) < 1e-15
        assert abs(en[200] - A / (t0 + 1)) < 1e-9          # the integral of a (1 + x/t0)^-2 over the first generation
    # delivered fraction >= 0.9 at N = 1,600
    assert ns['delivered'](1600, A) / A > 0.92


def _state(R):
    nt = int(R.ntv[0])
    return (R.slots.copy(), R.npres.copy(), R.tunit[:nt].copy(), R.trule[:nt].copy(), R.tsp[:nt].copy(), nt)


def _eq(a, b):
    return all(np.array_equal(x, y) if isinstance(x, np.ndarray) else x == y for x, y in zip(a, b))


@need
def test_eps0_equals_scaling_and_rain_kernels():
    import annealed as AN
    import realizable_scaling as RS
    import removing_rivals as RR
    for cell, N in (('an_iiiS_200', 200), ('an_iiiS_400', 400)):
        a = AN.AnnRun(cell, 3)
        b = RS.RSRun(cell, 3); b.r = 100
        c = RR.RRRun(cell, 3, epsN=0.0); c.r = 100
        for R in (a, b, c):
            R.advance(150)
        assert a.r == 100
        assert _eq(_state(a), _state(b)) and _eq(_state(a), _state(c))


@need
def test_event_indexed_mode_equals_removing_rivals_rain():
    import annealed as AN
    import removing_rivals as RR
    cell = 'an_i_200'
    a = AN.AnnRun(cell, 1, sched=np.full(1000, 0.1 / 200), pairmode=0, track=True, fcap=100000)
    b = RR.RRRun(cell, 1, epsN=0.1, track=True); b.r = 100
    for R in (a, b):
        R.advance(250)
    assert _eq(_state(a), _state(b))
    n = int(a.nfr[0])
    assert n == int(b.nfr[0]) and n > 50
    assert np.array_equal(a.fr[:n], b.fr[:n]) and np.allclose(a.frf[:n], b.frf[:n])
    assert np.array_equal(a.lin, b.lin)


@need
def test_paired_founder_streams():
    import annealed as AN
    a = AN.AnnRun('an_i_200', 2)          # annealed
    b = AN.AnnRun('an_iv_200', 2)         # constant rain, same total
    for R in (a, b):
        R.advance(1200)
    for i in range(a.I):
        sa = a.fr[:int(a.nfr[0])]; sb = b.fr[:int(b.nfr[0])]
        xa = sa[sa[:, 1] == i, 2]; xb = sb[sb[:, 1] == i, 2]
        m = min(len(xa), len(xb))
        assert m > 5 and np.array_equal(xa[:m], xb[:m])
    # before the onset nothing arrives and the two runs are identical
    c = AN.AnnRun('an_i_200', 2); d = AN.AnnRun('an_iv_200', 2)
    c.advance(200); d.advance(200)
    assert int(c.rcount.sum()) == 0 and _eq(_state(c), _state(d))


@need
def test_founders():
    import annealed as AN
    import removing_rivals as RR
    import provenance as PV
    for cls, (x, xs) in AN.FORCED_X.items():
        R = AN.AnnRun('anF_%s_400_K3' % cls, 0)
        u = R.tunit[R.slots]
        assert (u[0] == x).all() and (u[1:] == 3).all()
        assert R.LS['names'][int(R.tsp[R.slots[0, 0]])] == xs
        assert (R.trule[R.slots] == PV.R_SNON).all()
    S = RR.static()
    a = AN.AnnRun('an_ii_200', 4); b = AN.AnnRun('an_i_200', 4)
    diff = a.tsp[a.slots] != b.tsp[b.slots]
    assert diff.sum(1).max() <= 1
    pos = RR.donor_positions(200, 8, 4)
    for i in range(8):
        k = a.slots[i, pos[i]]
        assert a.tunit[k] == S['uPB'] and a.trule[k] == PV.R_H
