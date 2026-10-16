"""Tests for the realizable-scaling run (notes/realizable-scaling.md §1.8).  The tests that need provenance's
untracked cached tables skip when they are absent."""
import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import realizable_scaling as RS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAVE_CACHE = os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'sets.npz')) and \
    os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'static', 'meta.pkl'))
needs_cache = pytest.mark.skipif(not HAVE_CACHE, reason='provenance cached tables absent')


def test_calibrated_mN_and_horizons():
    assert RS.mN_cal(100) == 1.0
    assert abs(RS.mN_cal(200) - 1.6245) < 1e-3 and abs(RS.mN_cal(400) - 2.6390) < 1e-3
    assert abs(RS.mN_cal(50) - 0.6156) < 1e-3
    assert [RS.t_ext(*g) for g in [(100, 64), (200, 64), (400, 64), (100, 128), (200, 128), (100, 256)]] == \
        [10000, 12311, 15157, 20000, 24623, 40000]
    # every main cell is S-nonself calibrated or a panel cell
    for c, inf in RS.CELL_INFO.items():
        if inf['main']:
            assert inf['arm'] == 'cal'
            assert inf['rule'] == 'Snon' or inf['rule'] == 'prop' or inf['rule'].startswith('cross')
    # N = 100 is registered once, as 'cal' with mN = 1
    assert not any(inf['N'] == 100 and inf['arm'] == 'm1' for inf in RS.CELL_INFO.values())
    assert len(RS.ALL['A']) == 42 and len(RS.ALL['B']) == 9 and len(RS.ALL['C']) == 12 and len(RS.ALL['D']) == 4


def test_rho_neutral_and_against_simulation():
    for N in (20, 50, 100):
        assert abs(RS.rho_fix(N, 0, 0, 0, 0) - 1.0 / N) < 1e-12
    # the TwinD coordination barrier (notes §1.6): rho = 1.85e-5 at N = 100
    assert abs(RS.rho_fix(100, 0, -1, -1, 0) / 1.8517e-5 - 1) < 1e-3
    # direct simulation of the birth-death step at N = 12, an advantageous type
    N, a, b, c, d = 12, 0.0, -1.0, -2.0, -1.0
    rng = np.random.default_rng(3)
    fix = 0
    T = 20000
    for _ in range(T):
        j = 1
        while 0 < j < N:
            fz = ((j - 1) * a + (N - j) * b) / (N - 1); fx = (j * c + (N - j - 1) * d) / (N - 1)
            pz = j * math.exp(RS.W * fz) / (j * math.exp(RS.W * fz) + (N - j) * math.exp(RS.W * fx))
            born_z = rng.random() < pz
            dies_z = rng.random() < j / N
            j += int(born_z) - int(dies_z)
        fix += j == N
    p = RS.rho_fix(N, a, b, c, d)
    assert abs(fix / T - p) < 4 * math.sqrt(p * (1 - p) / T)


def _arch(spec):
    """Constructed archipelago over named holder types: CB (open), CB2 (open, mutual with CB), TW (identity), P (a
    non-open non-identity self-cooperator), D (defector, never held)."""
    names = ['CB', 'CB2', 'TW', 'P', 'D']
    ix = {n: i for i, n in enumerate(names)}
    mutual = np.zeros((5, 5), bool)
    for x, y in [('CB', 'CB'), ('CB2', 'CB2'), ('CB', 'CB2'), ('TW', 'TW'), ('P', 'P')]:
        mutual[ix[x], ix[y]] = mutual[ix[y], ix[x]] = True
    openv = np.array([1, 1, 0, 0, 0], bool)
    ident = np.array([0, 0, 1, 0, 0], bool)
    hol = [ix[s] for s in spec]
    held = [s != 'D' for s in spec]
    return hol, held, mutual, openv, ident


def test_classifier_constructed():
    r = RS.classify(*_arch(['CB'] * 6))
    assert r['universal_open'] and r['cause'] is None
    r = RS.classify(*_arch(['CB', 'CB2', 'CB', 'CB2']))
    assert r['universal_open']
    r = RS.classify(*_arch(['CB'] * 5 + ['TW']))
    assert not r['universal_open'] and r['cause'] == 'identity' and r['fail'] == [''] * 5 + ['identity']
    r = RS.classify(*_arch(['CB'] * 5 + ['P']))
    assert r['cause'] == 'rival' and r['fail'][-1] == 'rival'
    r = RS.classify(*_arch(['CB'] * 5 + ['D']))
    assert r['cause'] == 'inefficient' and r['fail'][-1] == 'unheld'
    r = RS.classify(*_arch(['CB', 'P', 'TW', 'D']))
    assert r['cause'] == 'identity' and r['fail'] == ['', 'rival', 'identity', 'unheld']
    r = RS.classify(*_arch(['TW'] * 4))           # universal but not open
    assert not r['universal_open'] and r['main'] == [] and r['cause'] == 'identity'
    r = RS.classify(*_arch(['D'] * 3))
    assert r['cause'] == 'inefficient'


def test_static_check_constructed():
    fail = ['', '', 'rival', 'identity']
    # one target-compatible living type, mutual with the rival island's holder (a bridge), not with the clique
    lab, per = RS.static_check(fail, [0, 0, 3, 2], 100, 1.0, [True], [[False, False, True, False]],
                               [[0, 0, 0.01, 1.85e-5]], [[0, 0, 0.5, 0.5]], [False] * 4)
    kinds = {p['island']: p['kind'] for p in per}
    assert kinds[2] == 'bridged' and kinds[3] == 'coordination'      # 1/(0.5 * 1.85e-5) ~ 1.1e5 < 1e6
    assert lab == 'coordination'
    lab, per = RS.static_check(fail, [0, 0, 3, 2], 200, 1.6, [True], [[False, False, True, False]],
                               [[0, 0, 0.005, 7.2e-9]], [[0, 0, 0.5, 0.5]], [False] * 4)
    assert lab == 'absorbing' and {p['island']: p['kind'] for p in per}[3] == 'absorbing'
    lab, per = RS.static_check(['', 'rival'], [0, 3], 200, 1.0, [True], [[False, False]], [[0, 1e-12]],
                               [[0, 0.9]], [False, True])
    assert lab == 'reachable-bridge'
    lab, per = RS.static_check(['', ''], [0, 0], 100, 1.0, [], [], [], [], [False, False])
    assert lab == 'universal' and per == []


@needs_cache
def test_founders_panel_and_controls():
    import provenance_run as PR
    LS = PR.lot_static('ext')
    Q = set(LS['Q'].tolist())
    for (N, I) in [(100, 64), (200, 128)]:
        for rep in (0, 7):
            base = RS._base_sp(N, I, rep, LS)
            prop, _, _ = RS.founders_rs(RS.cell_name('prop', N, I, 'cal'), rep, LS)
            nq = int(np.isin(base, list(Q)).sum())
            assert int(np.isin(prop, list(Q)).sum()) == 0
            assert int((prop != base).sum()) == nq                  # only Q founders redrawn
            for c in (4, 8, 16):
                name = RS.cell_name('cross%d' % c, N, I, 'cal')
                if name not in RS.CELL_INFO: continue
                sp, rule, unit = RS.founders_rs(name, rep, LS)
                assert int(np.isin(sp, list(Q)).sum()) == c
                assert int(((sp != prop) & ~np.isin(sp, list(Q))).sum()) == 0
    # S-nonself and the ablation are provenance's founders
    sp1, _, _ = RS.founders_rs(RS.cell_name('Snon', 100, 64, 'cal'), 3, LS)
    assert (sp1 == RS._base_sp(100, 64, 3, LS)).all()
    # dense donors: ceil(N/100) H founders per island
    sp, rule, unit = RS.founders_rs(RS.cell_name('Cdense', 400, 64, 'cal'), 0, LS)
    import provenance as PV
    assert ((rule == PV.R_H).sum(1) == 4).all()


@needs_cache
def test_placement_uniform():
    import provenance_run as PR
    LS = PR.lot_static('ext')
    Qs = list(LS['Q'].tolist())
    N, I = 100, 64
    hist = np.zeros(I)
    for rep in range(300):
        sp = RS.place_Q(np.zeros((I, N), np.int64) - 1, 16, N, I, rep, LS)
        hist += np.isin(sp, Qs).sum(1)
    exp = 300 * 16 / I
    chi2 = float(((hist - exp) ** 2 / exp).sum())
    assert chi2 < 120          # 63 degrees of freedom; p < 1e-5 above ~120


@needs_cache
def test_reproduces_stored_provenance_run():
    import gzip, json
    import realizable_scaling_run as RR
    stored = json.load(gzip.open(os.path.join(ROOT, 'runs', 'provenance', 'lottery_main.json.gz')))
    s = [r for r in stored if r['cell'] == 'Snon' and r['rep'] == 1][0]
    r = RR.lottery_job((RS.cell_name('Snon', 100, 64, 'cal'), 1, 2000, 0))
    c = RR.compare_stored(r, s)
    assert c['n_common'] > 10 and c['n_trace_bad'] == 0 and not c['snap_bad'] and not c['estab_bad']
    assert r['classifier_mismatch'] == 0
