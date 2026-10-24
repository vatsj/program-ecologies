"""Tests for the pricing-rules experiment: the instrumented ledger on hand-built encounters (notes/pricing-rules.md §1.2),
the equality of its totals with the stored engine, the B ledger (first and repeated checks), the sampled-kernel charge against
the Python ledger, and zero price reproducing each stored lottery draw for draw (L_T games from the tracked stored cells; the
PD from the untracked cache, skipped when absent)."""
import gzip
import json
import os
import sys

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'src'))
import pricing_rules as P
import pricing_rules_lt as L
import pricing_rules_kern as KR
import lt_tape_run as R

_BASE = {}


def base(game):
    if game not in _BASE: _BASE[game] = L.Base(game)
    return _BASE[game]


def led(game, a, b, role=0):
    bs = base(game)
    names = bs.tb.names
    if game == 'rps':
        t = bs.tb.terms[0]; x = t[names[0].index(a)]; y = t[names[0].index(b)]
    elif role == 0:
        x = bs.tb.terms[0][names[0].index(a)]; y = bs.tb.terms[1][names[1].index(b)]
    else:
        x = bs.tb.terms[1][names[1].index(a)]; y = bs.tb.terms[0][names[0].index(b)]
    return bs.eng.ledger(x, y)


def leaf0(rec):
    assert len(rec['leaves']) >= 1
    return rec['leaves'][0]


K = R.K0


def test_instrumented_totals_equal_stored_engine():
    assert base('rps').mismatch == 0
    assert base('insp').mismatch == 0


@pytest.mark.parametrize('a,b,S,ncalls,nto,fa', [
    ('R0', 'P0', 2, 0, 0, 2),
    ('SIM100R', 'R0', 9, 1, 0, 9),                       # a finishing read: 1 + 2 + 1 = 4 steps
    ('SIM100R', 'SIM100R', 111, 1, 1, 9 + K),            # mutual: the root's call times out, 102 steps
    ('SIM20R', 'SIM100R', 31, 1, 1, 9 + K),
    ('SIM100R', 'SIM20R', 38, 2, 1, 16 + K),             # nested: the inner call times out, the outer finishes
    ('SIM20R', 'PB', 31, 1, 1, 9 + K),                   # a partial-cap timeout: the prove charge exceeds the sim's fuel
])
def test_rps_hand_table(a, b, S, ncalls, nto, fa):
    rec = led('rps', a, b)
    w, out, used, calls, reason = leaf0(rec)
    n_to, n_top, steps_top, nc, toplv = P.leaf_stats(used, calls)
    assert used == S
    assert nc == ncalls
    assert n_to == nto
    assert used - steps_top + K * n_top == fa


def test_rps_call_sizes():
    w, out, used, calls, reason = leaf0(led('rps', 'SIM100R', 'R0'))
    assert [c[4] for c in calls] == [4]
    w, out, used, calls, reason = leaf0(led('rps', 'SIM100R', 'SIM100R'))
    assert [c[4] for c in calls] == [102] and calls[0][5] is True and calls[0][6] == 'fuel'
    w, out, used, calls, reason = leaf0(led('rps', 'SIM100R', 'SIM20R'))
    assert [(c[1], c[4], c[5]) for c in calls] == [(-1, 33, False), (0, 22, True)]
    w, out, used, calls, reason = leaf0(led('rps', 'SIM20R', 'PB'))
    assert [(c[4], c[5], c[6]) for c in calls] == [(22, True, 'cap')]       # k + 2 steps: RUN, 3 inside, 17 + 1 charged


def test_uniform_mixer_expected_steps():
    rec = led('rps', 'U', 'R0')
    assert rec['steps'] == 7
    assert sorted(int(l[2]) for l in rec['leaves']) == [5, 8, 8]


@pytest.mark.parametrize('a,b,role,S,callsteps', [
    ('CR3', 'CARR3', 1, 27, 24),
    ('CR3', 'M3', 1, 4, 1),
    ('PR3', 'M3', 1, 43, 40),
    ('SI100n', 'K0', 0, 8, 4),
    ('SI100n', 'SE100k', 0, 106, 102),
])
def test_inspection_hand_table(a, b, role, S, callsteps):
    rec = led('insp', a, b, role=role)
    w, out, used, calls, reason = leaf0(rec)
    assert used == S
    assert [c[4] for c in calls] == [callsteps]
    assert all(l[2] == S for l in rec['leaves'])


def test_b_ledger_repeated_check_and_shared_keys():
    rec = led('insp', 'CR3', 'CARR3', role=1)
    w, out, used, calls, reason = leaf0(rec)
    cache = set()
    assert P.b_charge(used, calls, cache) == 27              # first execution: the whole check is paid
    assert P.b_charge(used, calls, cache) == 3               # repeated: 2 beta steps and the if
    # keys are shared across roles in RPS: after SIM20R vs SIM100R, call 2 of SIM100R vs SIM20R is cached
    w1, o1, u1, c1, r1 = leaf0(led('rps', 'SIM20R', 'SIM100R'))
    w2, o2, u2, c2, r2 = leaf0(led('rps', 'SIM100R', 'SIM20R'))
    cache = set()
    P.b_charge(u1, c1, cache)
    assert P.b_charge(u2, c2, cache) == 38 - 22
    cache2 = set()
    assert P.b_charge(u2, c2, cache2) == 38                 # cold: both calls paid
    assert P.b_charge(u2, c2, cache2) == 5                  # repeat: only the root's own steps


def test_b_charge_numba_equals_python():
    bs = base('rps')
    sd = KR.SampledData(bs, 'B', 1e-3)
    f = sd.f0
    terms = bs.tb.terms[0]
    names = bs.tb.names[0]
    pairs = [('SIM100R', 'SIM20R'), ('SIM20R', 'SIM100R'), ('SIM100R', 'R0'), ('SIM20R', 'PB'), ('SIM100R', 'SIM100R')]
    cache = set()
    paid = np.zeros(sd.nkeys, np.bool_)
    freebuf = np.zeros(256, np.bool_)
    for a, b in pairs * 2:
        i, j = names.index(a), names.index(b)
        rec = bs.eng.ledger(terms[i], terms[j])
        l = f.ps[i, j]                                       # one leaf per pair here
        assert f.pn[i, j] == 1
        w, out, used, calls, reason = rec['leaves'][0]
        py = P.b_charge(used, calls, cache)
        nb = KR._charge(l, 4, 1.0, f.S, f.nto, f.fa, f.ncall, f.top, f.cs, f.cn, f.cpar, f.ckey, f.cown, paid, freebuf)
        assert abs(py - nb) < 1e-9, (a, b, py, nb)


def test_rule_charge_matrices():
    bs = base('rps')
    names = bs.tb.names[0]
    i, j = names.index('SIM100R'), names.index('SIM100R')
    a = bs.arrays
    assert a['S'][i, j] == 111 and a['n_to'][i, j] == 1 and a['fa'][i, j] == 9 + K and a['root_own'][i, j] == 9
    assert bs.charge(a, 'F', 1e-3, K)[i, j] == pytest.approx(0.111)
    assert bs.charge(a, 'A', 0.5, K)[i, j] == pytest.approx(0.5)
    assert bs.charge(a, 'FA', 1e-3, K)[i, j] == pytest.approx(1e-3 * (9 + K))
    assert bs.charge(a, 'Bw', 1e-3, K)[i, j] == pytest.approx(9e-3)
    assert bs.charge(a, 'T', 0.1, K)[i, j] == pytest.approx(0.1)
    u = names.index('U')
    assert a['n_to'][u, :].max() == 0 and a['S'][u, names.index('R0')] == 7


def _stored(name):
    p = os.path.join(ROOT, 'runs', 'lt_tape', name + '.json.gz')
    if not os.path.exists(p): pytest.skip('stored cell absent')
    return json.load(gzip.open(p, 'rt'))


@pytest.mark.parametrize('game,rule,level,stored', [
    ('rps', 'Z', 0.0, 'rps_full_cfree_primary'),
    ('rps', 'F', 1e-3, 'rps_full_c0.001_primary'),
    ('insp', 'Z', 0.0, 'insp_full_cfree_primary'),
    ('insp', 'F', 1e-3, 'insp_full_c0.001_primary'),
])
def test_zero_price_and_F_reproduce_stored_draws(game, rule, level, stored):
    st = _stored(stored)
    bs = base(game)
    tb = bs.view(rule, level)
    label = L.seed_label(rule, level)
    for r in range(2):
        if game == 'rps': full, ex = L.lottery_rps_exact(tb, 'primary', r, 100, 64, label)
        else: full, ex = L.lottery_insp_exact(tb, 'primary', r, 100, 64, label)
        rec = L.make_record(bs, tb, full, 100, ex, R.named_idx(tb), r, 0.0, 'x')
        assert rec['dom2000'] == st['recs'][r]['dom2000']
        assert rec['dom4000'] == st['recs'][r]['dom4000']


def test_sampled_kernel_deterministic_and_charges_apply():
    bs = base('rps')
    sd = KR.SampledData(bs, 'Zs', 0.0)
    tb = bs.view('Zs', 0.0)
    a, _ = KR.lottery_sampled(bs, tb, sd, 'Zs', 0.0, 'primary', 0, 20, 4, 'x')
    b, _ = KR.lottery_sampled(bs, tb, sd, 'Zs', 0.0, 'primary', 0, 20, 4, 'x')
    assert all((a[g] == b[g]).all() for g in a)
    assert all(a[g].sum() == 20 * 4 for g in a)


# ---- the PD (needs the untracked caches runs/provenance/static and runs/detectors/K/static) -------------------------------
def _pd_cache():
    return os.path.exists(os.path.join(ROOT, 'runs', 'detectors', 'K', 'static', 'A.npy'))


def test_pd_model_reproduces_action_table():
    if not _pd_cache(): pytest.skip('PD cache absent')
    import world_k as WK
    import pricing_rules_pd_model as M
    LS = WK.use_world('K')
    st = LS['st']
    PX = M.make_px(LS, 'F', 1e-4)
    utau, BLC, BLD, CHC, CHD, UVt, PRODC, PD, KIND, NAT, DTy, DR, BTy, BA, BL, CST, COSTS, PAR = PX
    O = np.asarray(st['O']); A = st['A']; selfa = np.asarray(st['selfa'])
    rng = np.random.default_rng(3)
    for _ in range(20000):
        u = int(O[rng.integers(len(O))]); v = int(O[rng.integers(len(O))])
        act, S, nto, tos, nc = M.play_ledger(u, v, False, utau, DTy, DR, BTy, BA, BL, BLC, BLD, CHC, CHD, UVt, CST)
        assert act == A[u, v]
        act, S, nto, tos, nc = M.play_ledger(u, u, True, utau, DTy, DR, BTy, BA, BL, BLC, BLD, CHC, CHD, UVt, CST)
        assert act == selfa[u]


def test_pd_zero_price_reproduces_stored_run():
    if not _pd_cache(): pytest.skip('PD cache absent')
    import world_k as WK
    import pricing_rules_pd as PD
    stored = WK.island_job(('wk_Snon_100_64', 0, 'K', 400, False))
    priced = PD.pd_job('wk_Snon_100_64', 0, 'Z', 0.0, 400)
    assert stored['trace'] == priced['trace']
    assert stored['n_types'] == priced['n_types']
    assert stored['final']['cls'] == priced['final']['cls']


def test_pd_charges_have_the_stated_form():
    if not _pd_cache(): pytest.skip('PD cache absent')
    import world_k as WK
    import pricing_rules_pd_model as M
    LS = WK.use_world('K')
    O = np.asarray(LS['st']['O'])
    # a unit with a C list checked against another with a list: F charges c * steps, A charges P per TO, F+A replaces the
    # steps of a TO call by K
    cst = M.CST_DEFAULT
    for rule in ('F', 'A', 'FA', 'B', 'T'):
        PX = M.make_px(LS, rule, 1.0, cst)
        utau, BLC, BLD, CHC, CHD, UVt, PRODC, PD, KIND, NAT, DTy, DR, BTy, BA, BL, CST, COSTS, PAR = PX
        tunit = np.array([int(O[0]), int(O[1])]); tsp = np.array([0, 1]); trule = np.array([0, 0])
        ch = M.charge_pair(0, 1, tunit, tsp, trule, PX)
        act, S, nto, tos, nc = M.play_ledger(int(tunit[0]), int(tunit[1]), False, utau, DTy, DR, BTy, BA, BL, BLC, BLD, CHC, CHD, UVt, CST)
        want = {'F': S, 'A': nto, 'FA': S - tos + M.KPD * nto, 'B': cst[M.C_BASE], 'T': nc}[rule]
        assert ch == pytest.approx(want)
