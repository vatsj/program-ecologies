"""Tests for the failure-pricing confirmation: the new scores on hand-built rows (notes/failure-pricing-confirm.md section 1.2),
the fresh-index guard and the hand-derived seeds (1.5), the depth tables on the hand cases (1.1), and one stored cell of each
game reproduced draw for draw (the PD from the untracked cache, skipped when absent)."""
import gzip
import json
import os
import sys
import types

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'src'))
import failure_pricing_confirm as F

_CTX = {}


def ctx(game):
    if game not in _CTX: _CTX[game] = F.LTContext(game)
    return _CTX[game]


# ---------------------------------------------------------------------------------------------------------------- statuses
def test_statuses_and_classification():
    assert F.status_le((0.05, 0.02, 0.09), 0.10) == 'met'
    assert F.status_le((0.10, 0.08, 0.10), 0.10) == 'met'                # float tolerance: 0.10 is not above 0.10
    assert F.status_le((0.15, 0.12, 0.2), 0.10) == 'failed'
    assert F.status_le((0.1, 0.05, 0.2), 0.10) == 'undetermined'
    assert F.status_ge((0.85, 0.709, 0.929), 0.70) == 'met'
    assert F.status_ge((0.75, 0.598, 0.858), 0.70) == 'undetermined'
    assert F.status_ge((0.4, 0.3, 0.6), 0.70) == 'failed'
    assert F.worst('met', 'undetermined', 'failed') == 'failed'
    assert F.worst('met', 'met') == 'met'
    assert F.classify(['met', 'met', 'met']) == 'confirmed'
    assert F.classify(['met', 'undetermined', 'met']) == 'unresolved'
    assert F.classify(['met', 'undetermined', 'failed']) == 'refuted'


def test_wilson_hand_values():
    # notes 1.2b: 34 of 40 is the smallest count that meets the 0.70 line
    assert F.wilson(34, 40)[1] >= 0.70 and F.wilson(33, 40)[1] < 0.70
    p, lo, hi = F.wilson(34, 40)
    assert abs(lo - 0.709) < 0.001 and abs(hi - 0.929) < 0.001
    assert abs(F.wilson(33, 40)[1] - 0.680) < 0.001


# ---------------------------------------------------------------------------------------------------------------- RPS by mixing
def test_rps_by_mixing_hand_examples():
    # PRR islands: e_gross 0, forfeits 0 -> met
    st, a, b = F.rps_by_mixing([0.0] * 40, [0.0] * 40)
    assert st == 'met'
    # stored A at 1 (notes 1.2a(iv)): e_gross ~0.515 and forfeits ~0.418 -> failed although the net target is met
    rng = np.random.default_rng(1)
    eg = 0.515 + 0.15 * rng.standard_normal(40); fo = 0.418 + 0.15 * rng.standard_normal(40)
    assert F.rps_by_mixing(eg, fo)[0] == 'failed'
    # low e_gross but forfeits above 0.05 -> failed by the forfeit clause only
    st, a, b = F.rps_by_mixing([0.01] * 40, [0.30 + 0.02 * rng.standard_normal(40)][0])
    assert a == 'met' and b == 'failed' and st == 'failed'
    # e_gross interval straddling the line, forfeits 0 -> undetermined
    st, a, b = F.rps_by_mixing(np.r_[np.full(20, 0.0), np.full(20, 0.25)], np.zeros(40))
    assert st == 'undetermined'


# ---------------------------------------------------------------------------------------------------------------- PD scores
def rec(uo, frozen_at, last_gen, ulc, charge):
    return dict(final=dict(universal_open=uo), frozen_at=frozen_at, last_gen=last_gen, uo_last_change=ulc,
                ledger=[1.0, 0.0, 0.0, charge, 9900.0])


def test_pd_persistence_and_charge_cap():
    # notes 1.2b examples
    late = F.pd_flags(rec(True, -1, 10000, 9800, 0.0))
    assert late['A'] and not late['B'] and late['late'] and late['censored']
    froz = F.pd_flags(rec(True, 4200, 4200, 4150, 0.0))
    assert froz['A'] and froz['B'] and froz['C'] and not froz['censored']
    never = F.pd_flags(rec(True, -1, 10000, -1, 0.0))                      # indicator never changed
    assert never['B'] and never['C']
    old = F.pd_flags(rec(True, -1, 10000, 9500, 0.0))                      # exactly 500 generations
    assert old['B']
    notuo = F.pd_flags(rec(False, 3000, 3000, 2000, 0.0))
    assert not notuo['A'] and not notuo['B'] and not notuo['C']
    # charge cap 0.3 (= 0.1 of the range 3): F 1e-2 stored 91.8 fails (C) although universal-open; B 1e-2 (0.04) passes
    f = F.pd_flags(rec(True, 5000, 5000, 100, 91.77))
    assert f['B'] and not f['C']
    f = F.pd_flags(rec(True, 5000, 5000, 100, 0.04))
    assert f['C']
    f = F.pd_flags(rec(True, 5000, 5000, 100, 0.3))                       # at the cap counts
    assert f['C']
    f = F.pd_flags(rec(True, 5000, 5000, 100, 0.3001))
    assert not f['C']


def test_pd_counts_and_status():
    recs = [rec(True, 100, 100, 50, 0.0)] * 34 + [rec(False, 100, 100, 50, 0.0)] * 6
    c = F.pd_counts(recs)
    assert (c['A'], c['B'], c['C']) == (34, 34, 34) and c['sC'] == 'met'
    recs = [rec(True, 100, 100, 50, 0.0)] * 33 + [rec(False, 100, 100, 50, 0.0)] * 7
    assert F.pd_counts(recs)['sC'] == 'undetermined'
    assert F.RANGE['pd'] == 3.0 and abs(0.1 * F.RANGE['pd'] - F.TH['pd_charge']) < 1e-12
    assert abs(0.01 * F.RANGE['pd'] - F.TH['pd_charge_tight']) < 1e-12


def test_pd_payoff_range_is_three():
    import lt_genes_kern as KN
    P = np.asarray(KN.PAYM)
    assert P.max() - P.min() == 3.0
    assert P[0, 1] == 1.0 and P[1, 0] == -2.0 and P[0, 0] == -1.0 and P[1, 1] == 0.0


def test_trace_stats_weights():
    # scramble = checkpoints with g <= 200, interval weighted; hand: two intervals of 10 with charges 0.2 and 0.0
    tr = [(10, 10, 5.0, 0.0, 1.0, 0.2), (20, 10, 5.0, 0.0, 0.0, 0.0), (300, 280, 5.0, 0.0, 0.0, 0.0)]
    s = F.trace_stats(tr)
    assert abs(s['scr_charge'] - 0.1) < 1e-12
    assert abs(s['cum_charge'] - 0.2 * 10 / 300) < 1e-12


# ---------------------------------------------------------------------------------------------------------------- inspection net
def test_insp_net_efficiency_hand_example():
    # two islands, one program per role; gross payoffs (0, 0) and (-0.04, 0); charges 0.1 and 0.003
    tb = types.SimpleNamespace(UAg=np.array([[-0.04]]), UBg=np.array([[0.0]]), UA=np.array([[-0.04 - 0.003]]), UB=np.array([[0.0 - 0.1]]))
    c0 = np.array([[100]]); c1 = np.array([[100]])
    m = F.insp_island_means(tb, c0, c1, 100)
    assert m['eff_gross'][0] == 1.0 and m['eff_net'][0] == 0.0           # inspectee pays 0.1 > 0.05 allowance
    tb = types.SimpleNamespace(UAg=np.array([[-0.048]]), UBg=np.array([[0.0]]), UA=np.array([[-0.051]]), UB=np.array([[0.0]]))
    m = F.insp_island_means(tb, c0, c1, 100)
    assert m['eff_gross'][0] == 1.0 and m['eff_net'][0] == 0.0           # a borderline inspector pushed across the line
    tb = types.SimpleNamespace(UAg=np.array([[-0.05]]), UBg=np.array([[0.0]]), UA=np.array([[-0.05]]), UB=np.array([[0.0]]))
    assert F.insp_island_means(tb, c0, c1, 100)['eff_net'][0] == 1.0     # exactly -0.05 counts (float tolerance)
    # affordable timeouts per play for gross (0, 0): 0.05 / P
    for P, tp in ((0.1, 0.5), (0.3, 1 / 6), (1.0, 0.05), (10.0, 0.005)):
        assert abs(0.05 / P - tp) < 1e-9


# ---------------------------------------------------------------------------------------------------------------- freshness
def test_fresh_indices_disjoint_and_seed_values():
    import provenance_run as PR
    import rps as RP
    # PD: the kernel seed is increasing in rep; hand values of notes 1.5
    ks = lambda rep: PR.kernel_seed(100, 64, rep)
    assert PR.SALT == 20261012
    assert ks(0) == 21268176 and ks(39) == 39 * 1000003 + 21268176 == 60268293
    assert ks(200) == 221268776 and ks(239) == 260268893
    assert set(F.FRESH_PD).isdisjoint(F.STORED_PD) and set(F.FRESH_LT).isdisjoint(F.STORED_LT['primary']) and set(F.FRESH_LT).isdisjoint(F.STORED_LT['size'])
    assert {ks(r) for r in F.FRESH_PD}.isdisjoint({ks(r) for r in F.STORED_PD})
    # L_T: founder and dynamics seeds of every stored (cell, role / label, run) against every fresh one
    def seeds(game, cell, runs, labels):
        out = set()
        for r in runs:
            for ro in (0, 1):
                out.add(RP.run_seed('founders|%s|%d' % (cell, ro), r))
            for lab in labels:
                out.add(RP.run_seed('dynamics|%s|%s|full|%s|10000|False' % (cell, game, lab), r))
        return out
    stored_labels = ['0', '0.0001', '0.001', '1e-05', '0.01', 'A@0.01', 'A@0.1', 'A@1', 'A@10', 'FA@1e-05', 'B@0.001', 'T@0.1', 'T@1']
    fresh_labels = ['0', 'A@0.03', 'A@0.1', 'A@0.3', 'A@1', 'A@10', 'A@0.2', 'A@0.5']
    import pricing_rules_lt as PL
    for game in ('rps', 'insp'):
        tb = ctx(game).base.view('A', 0.1)
        for cell in ('primary', 'size'):
            assert PL.dyn_seed(tb, cell, 123, 'A@0.1') == RP.run_seed('dynamics|%s|%s|full|%s|10000|False' % (cell, game, 'A@0.1'), 123)
            st = seeds(game, cell, STORED_ALL[cell], stored_labels)
            fr = seeds(game, cell, F.FRESH_LT, fresh_labels)
            # the same label at different runs never collides, and a fresh run's founder seeds are new
            assert fr.isdisjoint({RP.run_seed('founders|%s|%d' % (cell, ro), r) for r in STORED_ALL[cell] for ro in (0, 1)})
            assert fr.isdisjoint(st)


STORED_ALL = {'primary': list(range(0, 80)), 'size': list(range(0, 20))}


def test_dyn_seed_label_matches_merged_code():
    import pricing_rules_lt as PL
    assert PL.seed_label('Z', 0.0) == '0' and PL.seed_label('A', 0.1) == 'A@0.1' and PL.seed_label('A', 0.03) == 'A@0.03'


# ---------------------------------------------------------------------------------------------------------------- depth tables
def test_depth_tables_hand_cases():
    for game in ('rps',):
        c = ctx(game)
        names = c.base.tb.names[0]
        ix = {n: i for i, n in enumerate(names)}
        d = c.depth[0]
        # row 4: mutual SIM100R: one topmost timed-out call, issued by x itself
        i = ix['SIM100R']
        assert d['top'][i, i] == 1 and d['nested'][i, i] == 0 and d['opp'][i, i] == 0
        # row 5: SIM20R vs SIM100R: x's own call times out
        assert d['top'][ix['SIM20R'], ix['SIM100R']] == 1 and d['opp'][ix['SIM20R'], ix['SIM100R']] == 0
        # row 6: SIM100R vs SIM20R: the timed-out call is inside the finishing call and issued from the opponent's code
        a, b = ix['SIM100R'], ix['SIM20R']
        assert d['top'][a, b] == 1 and d['nested'][a, b] == 0 and d['opp'][a, b] == 1
        # a finishing read and a constant: nothing
        assert d['tot'][ix['SIM100R'], ix['R0']] == 0
        # totals equal the merged n_to table
        assert np.allclose(d['tot'], c.base.arrays['n_to']) and np.allclose(d['top'] + d['nested'], d['tot'])


# ---------------------------------------------------------------------------------------------------------------- stored cells, draw for draw
def _stored(name):
    p = os.path.join(ROOT, 'runs', 'pricing_rules', name + '.json.gz')
    if not os.path.exists(p): pytest.skip('stored cell absent')
    return json.load(gzip.open(p, 'rt'))


@pytest.mark.parametrize('game,rule,level', [('rps', 'A', 0.1), ('rps', 'Z', 0.0), ('insp', 'A', 0.1), ('insp', 'Z', 0.0)])
def test_lt_stored_cells_reproduced(game, rule, level):
    st = _stored('%s_%s_%g_primary' % (game, rule, level))
    res = F.lt_cell(ctx(game), rule, level, 'primary', runs=[0, 1], out_dir='/tmp/_fpc_none', quiet=True, no_write=True)
    for a, b in zip(res['recs'], st['recs'][:2]):
        assert a['dom2000'] == b['dom2000'] and a['dom4000'] == b['dom4000']
        for k in b['stats']['2000']:
            assert a['stats']['2000'][k] == b['stats']['2000'][k], k
    if game == 'insp':
        # the per-island efficiency flags reproduce the stored mean, and net is contained in gross
        ext = res['recs'][0]['ext']
        assert abs(np.mean(ext['isl_eff_gross']) - st['recs'][0]['stats']['2000']['isl_efficient']) < 1e-9
        assert all(n <= g for n, g in zip(ext['isl_eff_net'], ext['isl_eff_gross']))
        assert abs(np.mean(ext['isl_u0g']) - st['recs'][0]['stats']['2000']['u0g']) < 1e-4


def _pd_cache():
    return os.path.exists(os.path.join(ROOT, 'runs', 'detectors', 'K', 'static', 'A.npy'))


def test_pd_stored_cell_reproduced_draw_for_draw(tmp_path):
    if not _pd_cache(): pytest.skip('PD cache absent')
    st = _stored('pd_A_0.1_wk_Snon_100_64')
    ref = [r for r in st['recs'] if r['rep'] == 0][0]
    recs = F.pd_cell('A', 0.1, reps=[0], out_dir=str(tmp_path), name='t', quiet=True)
    a = json.loads(json.dumps(recs[0]))
    for k in ('last_gen', 'frozen_at', 'uo_first', 'uo_last_change', 'n_types'):
        assert a[k] == ref[k], k
    assert a['final']['universal_open'] == ref['final']['universal_open'] and a['final']['pcc'] == ref['final']['pcc']
    assert a['ledger'] == ref['ledger'] and a['trace'] == ref['trace'] and a['cls'] == ref['cls']
    assert a['ltrace_stats']['scr_charge'] >= 0 and a['ltrace_stats']['cum_charge'] >= 0
