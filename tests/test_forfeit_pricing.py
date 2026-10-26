"""Tests for forfeit pricing (notes/forfeit-pricing.md section 1): the charge rule on hand-built plays, the exact simulators on hand-built
opponents and at their exact fuel boundaries, the one-play payoffs of SIMX and SIM against the notes' hand table, the forfeit payoff
tables under A, A_f and A_m, the clone and the founders, A_f without forfeits reproducing A draw for draw, a stored confirmation cell
reproduced through the new pipeline, the fresh-index guard, and (when the world-K caches exist) the PD recorder."""
import gzip
import json
import os
import sys

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'src'))
import lt_tape as T
import lt_tape_games as G
import lt_tape_run as R
import rps as RP
import forfeit_pricing as FP
import forfeit_pricing_run as FR
from lt_tape import con, nat, L2, IF, EQ, ME, THEM

_BASE = {}


def base(game):
    if game not in _BASE: _BASE[game] = FP.BaseX(game)
    return _BASE[game]


_ENG = {}


def engines(K=10000):
    if K not in _ENG:
        prover = T.TProver(3, limit=3 * max(K, 20000))
        _ENG[K] = (T.Engine(prover, K=K, r=3, m=3), FP.LedgerEngineX(prover, K, 3, 3))
    return _ENG[K]


OMEGA = FP.OMEGA
LOOP = L2(OMEGA)                                    # forfeits against anything
R0 = L2(con('R'))


def sim_capped(k, default):
    return L2(G.let(('run', nat(k), THEM, ME), G.beat_case(('v', 0), con(default))))


def events(x, y, K=10000):
    _, le = engines(K)
    ex = FP.x_expectations(le.ledger(x, y))
    return ex


def u_net(x, y, rule, P, K=10000):
    """One-play expected net payoff of x against y (RPS), stored forfeit convention (A, A_f) or the security replacement (A_m)."""
    e, le = engines(K)
    dx = e.dist(x, y)['dist']; dy = e.dist(y, x)['dist']
    u = FR.rps_u4('m' if rule == 'Am' else 'stored')
    idx = {'R': 0, 'P': 1, 'S': 2}
    g = 0.0
    for a, wa in dx.items():
        for b, wb in dy.items():
            g += float(wa) * float(wb) * u[idx.get(a, 3), idx.get(b, 3)]
    ex = FP.x_expectations(le.ledger(x, y))
    return g - P * (ex['ev_A'] if rule == 'A' else ex['ev_Af'])


# ---------------------------------------------------------------------------------------------------------------- the charge rule (notes 1.0)
def test_leaf_events():
    sim = (0, -1, FP.RUN_, 0, 22, True, 'cap')
    unc = (0, -1, FP.RUNX_, 0, 9990, True, 'cap')
    fin = (0, -1, FP.RUNX_, 0, 4, False, 'value')
    assert FP.leaf_events((), 'value') == (0, 0, 0, 0, 0)                    # neither
    assert FP.leaf_events((), 'K') == (0, 0, 1, 0, 1)                        # a forfeit alone: free under A, one charge under A_f
    assert FP.leaf_events((sim,), 'value') == (1, 0, 0, 1, 1)                # a timed-out read alone
    assert FP.leaf_events((sim,), 'K') == (1, 0, 1, 1, 2)                    # both: two distinct failures
    assert FP.leaf_events((unc,), 'K') == (0, 1, 1, 0, 1)                    # an uncapped read that exhausts the root: one charge, not two
    assert FP.leaf_events((fin,), 'value') == (0, 0, 0, 0, 0)


def test_hand_built_plays_charges():
    ex = events(R0, R0)
    assert ex['ev_A'] == 0 and ex['ev_Af'] == 0 and ex['forf'] == 0                                    # neither
    ex = events(LOOP, R0)
    assert ex['forf'] == 1 and ex['ev_A'] == 0 and ex['ev_Af'] == 1                                    # a forfeit
    ex = events(sim_capped(20, 'R'), LOOP)
    assert ex['n_to'] == 1 and ex['forf'] == 0 and ex['ev_A'] == 1 and ex['ev_Af'] == 1                # a timed-out read
    both = L2(G.let(('run', nat(20), THEM, ME), OMEGA))
    ex = events(both, LOOP)
    assert ex['n_to'] == 1 and ex['forf'] == 1 and ex['ev_A'] == 1 and ex['ev_Af'] == 2                # both: two failures
    simx = FP.simx_rps(10000)
    ex = events(simx, LOOP)
    assert ex['forf'] == 1 and ex['n_uto'] == 1 and ex['ev_A'] == 0 and ex['ev_Af'] == 1             # one charge for an uncapped read that exhausts
    ex = events(simx, R0)
    assert ex['forf'] == 0 and ex['n_uto'] == 0 and ex['unc_fin'] == 1 and ex['ev_Af'] == 0           # a finishing exact read
    ex = events(simx, sim_capped(100, 'R'))                                                           # nested: the opponent's cap-100 read times out
    assert ex['n_to'] == 1 and ex['forf'] == 0 and ex['ev_A'] == 1 and ex['ev_Af'] == 1
    ex = events(sim_capped(100, 'R'), sim_capped(20, 'R'))                                            # notes row 6: a nested timed-out call is the root's
    assert ex['n_to'] == 1 and ex['ev_Af'] == 1


def test_ledger_reproduces_engine_exactly_on_hand_pairs():
    e, le = engines()
    simx = FP.simx_rps(10000)
    for x, y in ((simx, R0), (R0, simx), (simx, LOOP), (simx, sim_capped(100, 'P')), (sim_capped(100, 'P'), simx), (LOOP, R0)):
        d = e.dist(x, y); l = le.ledger(x, y)
        assert d['dist'] == l['dist'] and d['steps'] == l['steps'] and d['fuel'] == l['fuel']


# ---------------------------------------------------------------------------------------------------------------- exact simulators
def test_simx_hand_cases_and_steps():
    e, _ = engines()
    simx = FP.simx_rps(10000)
    d = e.dist(simx, R0)
    assert dict(d['dist']) == {'P': 1} and d['steps'] == 9                                            # notes 1.3: 9 steps against a constant
    for nm, act in (('R', 'P'), ('P', 'S'), ('S', 'R')):
        assert dict(e.dist(simx, L2(con(nm)))['dist']) == {act: 1}
    u = L2(IF(EQ(T.TP(0), nat(0)), con('R'), IF(EQ(T.TP(0), nat(1)), con('P'), con('S'))))
    d = e.dist(simx, u)
    assert all(abs(float(d['dist'][a]) - 1 / 3) < 1e-12 for a in 'RPS')                              # one sample of an independent tape: uniform
    assert float(e.dist(simx, LOOP)['fuel']) == 1 and e.dist(simx, LOOP)['steps'] == 10000          # a reader that never finishes: forfeit by running out


def burn(n, act):
    """An opponent whose play takes exactly n steps inside the frame beyond the two root beta steps, then plays act."""
    body = con(act)
    for _ in range(n): body = ('app', ('lam', ('v', 0)), body)
    return L2(body)


@pytest.mark.parametrize('act,resp_steps', [('R', 2), ('P', 4), ('S', 6)])
def test_reservation_exact_boundary_rps(act, resp_steps):
    K = 120
    eng = T.Engine(T.TProver(3, limit=3 * 20000), K=K, r=3, m=3)
    simx = FP.simx_rps(K)
    nmax = K - FP.RESP_RPS - 2                       # the frame has k = K - 11 steps, 2 of them the opponent's own beta
    d = eng.dist(simx, burn(nmax, act))
    assert d['fuel'] == 0 and sum(d['dist'].values()) == 1 and 'BOT' not in d['dist']
    assert d['steps'] == 2 + 1 + (2 + nmax) + 1 + 1 + resp_steps          # the response always fits
    if act == 'S': assert d['steps'] == K                                    # the worst response uses exactly the fuel
    d = eng.dist(simx, burn(nmax + 1, act))          # one step over: the read closes on TO and the program forfeits
    assert d['fuel'] == 1 and dict(d['dist']) == {'BOT': 1}


@pytest.mark.parametrize('maker,acts', [(FP.simx_insp_I, ('C', 'K')), (FP.simx_insp_E, ('I', 'N'))])
def test_reservation_exact_boundary_inspection(maker, acts):
    K = 120
    eng = T.Engine(T.TProver(3, limit=3 * 20000), K=K, r=2, m=3)
    x = maker(K)
    nmax = K - FP.RESP_INSP - 2
    for act in acts:
        d = eng.dist(x, burn(nmax, act))
        assert d['fuel'] == 0 and 'BOT' not in d['dist'] and d['steps'] <= K
        d = eng.dist(x, burn(nmax + 1, act))
        assert d['fuel'] == 1
    # the worst response (4 ladder steps) lands exactly on the fuel
    worst = acts[0] if maker is FP.simx_insp_I else acts[1]
    assert eng.dist(x, burn(nmax, worst))['steps'] == K


def test_exact_read_shares_fuel_with_enclosing_frames():
    # SIMX against SIMX: a regress without a base, forfeit for every budget (notes 1.3, nearby budgets)
    for K in (200, 300, 1000):
        eng = T.Engine(T.TProver(3, limit=3 * 20000), K=K, r=3, m=3)
        x = FP.simx_rps(K)
        d = eng.dist(x, x)
        assert dict(d['dist']) == {'BOT': 1} and d['fuel'] == 1
    # against a capped simulator it finishes for every K (the opponent's cap closes first)
    for K in (200, 300, 1000, 10000):
        eng = T.Engine(T.TProver(3, limit=3 * 20000), K=K, r=3, m=3)
        d = eng.dist(FP.simx_rps(K), sim_capped(20, 'R'))
        assert dict(d['dist']) == {'P': 1}


def test_clone_is_identical_where_it_should_be():
    assert FP.capped_clone_rps(100) == G.catalogue_rps(10000, 3)[0][[t.name for t in G.catalogue_rps(10000, 3)[0]].index('SIM100u')].build('tape')
    ins, ee = G.catalogue_insp(10000, 3)
    assert FP.capped_clone_I(100) == [t for t in ins if t.name == 'SI100n'][0].build('tape')
    assert FP.capped_clone_E(100) == [t for t in ee if t.name == 'SE100k'][0].build('tape')
    # the clone is a different spelling, so only the hash-keyed programmes (H*, HE*, HI*) see a different quote: everywhere else the play
    # law, the capped timeouts and the forfeits are identical (notes 1.2: "behaviourally identical" up to the hash programmes)
    b = base('rps')
    names = b.tb.names[0]; nb = b.n_base[0]
    ic, it = names.index('SIM100u'), names.index('SIM100u~')
    for j in range(nb):
        same = np.allclose(b.tb.Gt[ic, j], b.tb.Gt[it, j]) and np.allclose(b.tb.Gt[j, ic], b.tb.Gt[j, it])
        assert same == (not names[j].startswith('H')), names[j]
        for k in ('n_to', 'forf'):
            assert np.isclose(b.arrays[k][ic, j], b.arrays[k][it, j]) and np.isclose(b.arrays[k][j, ic], b.arrays[k][j, it]), (k, names[j])
    bi = base('insp')
    n0, n1 = bi.n_base
    for role, cp, xn, sn in FP.TWINS['insp']:
        names = bi.tb.names[role]; ic, it = names.index(cp), names.index(sn)
        opp = bi.tb.names[1 - role]
        for j in range(bi.n_base[1 - role]):
            if role == 0:
                same = np.allclose(bi.tb.G0[ic, j], bi.tb.G0[it, j]) and np.allclose(bi.tb.G1[j, ic], bi.tb.G1[j, it])
                a_ = bi.arr0; ar1 = bi.arr1
                nt = np.isclose(a_['n_to'][ic, j], a_['n_to'][it, j]) and np.isclose(ar1['n_to'][j, ic], ar1['n_to'][j, it])
            else:
                same = np.allclose(bi.tb.G1[ic, j], bi.tb.G1[it, j]) and np.allclose(bi.tb.G0[j, ic], bi.tb.G0[j, it])
                a_ = bi.arr1; ar1 = bi.arr0
                nt = np.isclose(a_['n_to'][ic, j], a_['n_to'][it, j]) and np.isclose(ar1['n_to'][j, ic], ar1['n_to'][j, it])
            assert same == (not opp[j].startswith('H')), (cp, opp[j])
            assert nt, (cp, opp[j])


# ---------------------------------------------------------------------------------------------------------------- hand table of notes 1.3
HAND = [  # opponent class -> (g, k, k_opp)
    ('R0', 1, 0, 0), ('P0', 1, 0, 0), ('S0', 1, 0, 0), ('U', 0, 0, 0), ('B_RP', 1 / 3, 0, 0), ('B_SR', 1 / 3, 0, 0), ('CB_PS', 1 / 3, 0, 0),
    ('H0', 1, 0, 0), ('H1', 1, 0, 0), ('H2', 1, 0, 0), ('SIM20R', 1, 1, 1), ('SIM100P', 1, 1, 1), ('SIM100S', 1, 1, 1),
    ('SIM20u', 0, 1, 1), ('SIM100u', 0, 1, 1), ('PRR', 0, 0, 0), ('CRR', 0, 0, 0),
]


@pytest.mark.parametrize('P', (0.03, 0.1, 0.3, 1.0, 10.0))
def test_simx_against_the_catalogue_hand_table(P):
    b = base('rps')
    names = b.tb.names[0]
    ix = {n: i for i, n in enumerate(names)}
    s = ix['SIMX']
    Ug = FR.rps_game_payoffs(b.tb.Gt, 'stored')
    for (opp, g, k, kopp) in HAND:
        j = ix[opp]
        assert abs(Ug[s, j] - g) < 1e-9, (opp, Ug[s, j])
        assert abs(b.arrays['n_to'][s, j] - k) < 1e-9 and abs(b.arrays['n_to'][j, s] - kopp) < 1e-9, opp
        assert b.arrays['forf'][s, j] == 0 and b.arrays['forf'][j, s] == 0
        net = Ug[s, j] - P * b.arrays['ev_Af'][s, j]
        assert abs(net - (g - P * k)) < 1e-9
        assert abs(Ug[j, s] - (-g)) < 1e-9                                                    # zero-sum: the opponent's gross is -g
    # SIMX against SIMX: both forfeit; A: (0, 0), A_f: (-P, -P), A_m: (-P, -P); the single charge
    assert b.arrays['forf'][s, s] == 1 and b.arrays['ev_A'][s, s] == 0 and b.arrays['ev_Af'][s, s] == 1
    assert Ug[s, s] == 0 and FR.rps_game_payoffs(b.tb.Gt, 'm')[s, s] == 0
    # SIM100R against SIM100R: both time out, play R, tie: -P each, no forfeit
    r = ix['SIM100R']
    assert Ug[r, r] == 0 and b.arrays['ev_A'][r, r] == 1 and b.arrays['ev_Af'][r, r] == 1


def test_simx_against_prover_is_mutual_forfeit():
    b = base('rps')
    ix = {n: i for i, n in enumerate(b.tb.names[0])}
    s, pb = ix['SIMX'], ix['PB']
    assert b.arrays['forf'][s, pb] == 1 and b.arrays['forf'][pb, s] == 1          # the prover's search exceeds the fuel; SIMX's read dies with it


def test_merged_columns_unchanged_by_the_extension():
    import pricing_rules_lt as PL
    mb = PL.Base('rps')
    b = base('rps')
    n = b.n_base[0]
    assert np.allclose(b.tb.Gt[:n, :n], mb.tb.Gt) and np.allclose(b.arrays['n_to'][:n, :n], mb.arrays['n_to'])
    assert np.allclose(b.arrays['forf'][:n, :n], mb.arrays['fuel']) and np.allclose(b.arrays['S'][:n, :n], mb.arrays['S'])
    mi = PL.Base('insp')
    bi = base('insp')
    n0, n1 = bi.n_base[0], bi.n_base[1]
    assert np.allclose(bi.arr0['n_to'][:n0, :n1], mi.arr0['n_to']) and np.allclose(bi.arr1['n_to'][:n1, :n0], mi.arr1['n_to'])
    assert bi.arr0['forf'][:n0, :n1].max() == 0 and bi.arr1['forf'][:n1, :n0].max() == 0     # no forfeits in the merged inspection catalogue


# ---------------------------------------------------------------------------------------------------------------- forfeit payoff tables
def test_rps_forfeit_tables_entry_by_entry():
    # x forfeits (index 0), y plays R (index 1) with certainty
    Gt = np.zeros((2, 2, 4)); Gt[0, 1, 3] = 1; Gt[1, 0, 0] = 1
    st = FR.rps_game_payoffs(Gt, 'stored'); m = FR.rps_game_payoffs(Gt, 'm')
    assert st[0, 1] == -1 and st[1, 0] == 1                                       # A, A_f: the game's own forfeit outcome
    assert m[0, 1] == 0 and m[1, 0] == 0                                           # A_m: the referee's uniform draw has expectation 0 against any pure action
    for a in range(3):                                                             # independence of the fallback from the opponent's action
        G3 = np.zeros((2, 2, 4)); G3[0, 1, 3] = 1; G3[1, 0, a] = 1
        assert FR.rps_game_payoffs(G3, 'm')[0, 1] == 0 and FR.rps_game_payoffs(G3, 'm')[1, 0] == 0
    both = np.zeros((2, 2, 4)); both[0, 1, 3] = 1; both[1, 0, 3] = 1
    assert FR.rps_game_payoffs(both, 'stored')[0, 1] == 0 and FR.rps_game_payoffs(both, 'm')[0, 1] == 0
    # the charge: P once per forfeit under A_f and A_m, none under A (leaf rule)
    assert FP.leaf_events((), 'K')[3] == 0 and FP.leaf_events((), 'K')[4] == 1


def test_inspection_forfeit_tables_entry_by_entry():
    V0, V1 = FR.insp_V('stored'); W0, W1 = FR.insp_V('m')
    # rows x in (I, N, F), columns y in (C, K, F)
    assert (V0[2, 0], V1[2, 0]) == (-1, 0) and (V0[2, 1], V1[2, 1]) == (-4, 1)           # inspector forfeits: stored
    assert (V0[0, 2], V1[0, 2]) == (-1, -3) and (V0[1, 2], V1[1, 2]) == (0, 0)           # inspectee forfeits: stored
    assert (V0[2, 2], V1[2, 2]) == (-4, -3)                                              # both forfeit: stored
    assert (W0[2, 0], W1[2, 0]) == (-1, 0) and (W0[2, 1], W1[2, 1]) == (-1, -3)          # A_m: the inspector plays I
    assert (W0[0, 2], W1[0, 2]) == (-1, 0) and (W0[1, 2], W1[1, 2]) == (0, 0)            # A_m: the inspectee plays C
    assert (W0[2, 2], W1[2, 2]) == (-1, 0)                                               # both: (I, C)
    assert np.allclose(V0[:2, :2], W0[:2, :2]) and np.allclose(V1[:2, :2], W1[:2, :2])  # completed plays unchanged
    # security: I is the pure maximin of the inspector, C of the inspectee
    P0, P1 = G.INSP.P0, G.INSP.P1
    assert P0.min(1).argmax() == 0 and P1.min(0).argmax() == 0


def test_u_net_one_play_payoffs():
    simx = FP.simx_rps(10000)
    for P in (0.03, 0.1, 1.0, 10.0):
        assert abs(u_net(simx, simx, 'A', P) - 0.0) < 1e-12
        assert abs(u_net(simx, simx, 'Af', P) + P) < 1e-12 and abs(u_net(simx, simx, 'Am', P) + P) < 1e-12
        s1 = sim_capped(100, 'R')
        assert abs(u_net(s1, s1, 'Af', P) + P) < 1e-12                                # SIM against SIM: a tie minus P
        assert abs(u_net(simx, s1, 'Af', P) - (1 - P)) < 1e-12                        # notes: +1 - P
        assert abs(u_net(s1, simx, 'Af', P) - (-1 - P)) < 1e-12
    # a unilateral forfeit (LOOP) against a constant: A: -1, A_f: -1 - P, A_m: -P
    assert abs(u_net(LOOP, R0, 'A', 0.1) + 1) < 1e-12 and abs(u_net(LOOP, R0, 'Af', 0.1) + 1.1) < 1e-12 and abs(u_net(LOOP, R0, 'Am', 0.1) + 0.1) < 1e-12


# ---------------------------------------------------------------------------------------------------------------- statistics
def test_e_comp_undefined_when_no_completed_plays():
    import types
    names = ['a', 'b']
    NUM = np.array([[0.0, 0.0], [0.0, 0.0]]); DEN = np.array([[1.0, 0.0], [0.0, 0.0]])
    tb = types.SimpleNamespace(NUM=NUM, DEN=DEN, keep=[np.array([True, True])])
    counts = np.array([[0, 100], [100, 0], [50, 50]])
    ec = FR.e_comp_islands(tb, counts, 100)
    assert np.isnan(ec[0]) and not np.isnan(ec[1])                                  # island 0: only program b, which never completes: undefined, not zero


# ---------------------------------------------------------------------------------------------------------------- founders and the validation
def test_founders_paired_and_split():
    b = base('rps')
    from collections import Counter
    f0 = FR.founders_arm(b, 'rps', 'primary', 300, 100, 64, 'none')[0]
    fx = FR.founders_arm(b, 'rps', 'primary', 300, 100, 64, 'X')[0]
    fs = FR.founders_arm(b, 'rps', 'primary', 300, 100, 64, 'sham')[0]
    names = b.tb.names[0]
    c, x, s = names.index('SIM100u'), names.index('SIMX'), names.index('SIM100u~')
    assert (f0.sum(1) == 100).all() and (fx.sum(1) == 100).all()
    # no other template changes; the counterpart's founders are split between it and the twin
    keep = [i for i in range(len(names)) if i not in (c, x, s)]
    assert (f0[:, keep] == fx[:, keep]).all() and (f0[:, keep] == fs[:, keep]).all()
    assert (fx[:, c] + fx[:, x] == f0[:, c]).all() and (fs[:, c] + fs[:, s] == f0[:, c]).all()
    assert (fx[:, s] == 0).all() and (fs[:, x] == 0).all() and (f0[:, [x, s]] == 0).all()
    # the same split in X and sham (same coin)
    assert (fx[:, x] == fs[:, s]).all()
    # the merged founders of the same run are the base part
    import pricing_rules_lt as PL
    mb = PL.Base('rps')
    assert (mb.tb.founders('primary', 300, 100, 64)[0] == f0[:, :b.n_base[0]]).all()


def _same_records(a, b, keys=('e_gross', 'e_prog', 'forfeit', 'mix', 'net_payoff')):
    for ra, rb in zip(a['recs'], b['recs']):
        assert ra['ext']['dom'] == rb['ext']['dom']
        for k in keys: assert ra['stats']['2000'][k] == rb['stats']['2000'][k], k


def test_af_without_forfeits_reproduces_A_draw_for_draw_rps():
    b = base('rps')
    ref = FR.lt_cell(b, 'A', 'none', 0.1, runs=[300, 301], no_write=True, quiet=True)
    # the A_f charge with its forfeit term zeroed, under A's dynamics label, is A's table: the same cell draw for draw
    af0 = FR.lt_cell(b, 'Af', 'none', 0.1, runs=[300, 301], no_write=True, quiet=True, label='A@0.1', no_forfeit=True)
    _same_records(ref, af0)
    tbA = FR.make_view(b, 'A', 0.1, 'none'); tbF = FR.make_view(b, 'Af', 0.1, 'none', no_forfeit=True)
    assert (tbA.U == tbF.U).all()
    # and without the zeroing the two differ exactly by P times the forfeit probability
    tbF2 = FR.make_view(b, 'Af', 0.1, 'none')
    assert np.allclose(tbA.U - tbF2.U, 0.1 * b.arrays['forf'])


def test_af_equals_A_draw_for_draw_inspection_without_forfeits():
    bi = base('insp')
    ref = FR.lt_cell(bi, 'A', 'none', 0.1, runs=[300], no_write=True, quiet=True)
    af = FR.lt_cell(bi, 'Af', 'none', 0.1, runs=[300], no_write=True, quiet=True, label='A@0.1')
    for k in ('n_eff_net', 'n_eff_gross', 'n_u0', 'n_u1'):
        assert ref['recs'][0]['stats']['2000'][k] == af['recs'][0]['stats']['2000'][k], k
    assert ref['recs'][0]['ext']['dom'] == af['recs'][0]['ext']['dom']
    am = FR.lt_cell(bi, 'Am', 'none', 0.1, runs=[300], no_write=True, quiet=True, label='A@0.1')       # the same tables again (no forfeit in the merged catalogue)
    assert ref['recs'][0]['ext']['dom'] == am['recs'][0]['ext']['dom']


def test_stored_confirmation_cell_reproduced_through_the_new_pipeline():
    p = os.path.join(ROOT, 'runs', 'failure_pricing_confirm', 'rps_A_0.1_primary.json.gz')
    if not os.path.exists(p): pytest.skip('stored cell absent')
    st = json.load(gzip.open(p, 'rt'))
    b = base('rps')
    res = FR.lt_cell(b, 'A', 'none', 0.1, runs=[100, 101], no_write=True, quiet=True)
    for a, ref in zip(res['recs'], st['recs'][:2]):
        assert a['ext']['dom']['2000'] == ref['ext']['dom']['2000'] and a['ext']['dom']['4000'] == ref['ext']['dom']['4000']
        for k in ('e_gross', 'e_prog', 'forfeit', 'mix', 'net_payoff', 'homo'):
            assert a['stats']['2000'][k] == ref['stats']['2000'][k], k


def test_X_arm_with_no_exact_simulators_present_equals_no_X():
    # an X arm whose founders contain no SIMX (never split) behaves as the no-X cell: here the tables of the merged part are the same
    b = base('rps')
    tb0 = FR.make_view(b, 'Af', 0.3, 'none'); tbx = FR.make_view(b, 'Af', 0.3, 'X')
    n = b.n_base[0]
    assert (tb0.U[:n, :n] == tbx.U[:n, :n]).all()


# ---------------------------------------------------------------------------------------------------------------- freshness
def test_fresh_indices_disjoint_and_seeds_new():
    assert set(FP.FRESH_LT).isdisjoint(FP.STORED_LT) and set(FP.FRESH_PD).isdisjoint(FP.STORED_PD)
    assert FP.FRESH_LT == list(range(300, 340)) and FP.FRESH_PD == list(range(300, 340))
    import provenance_run as PR
    ks = lambda rep: PR.kernel_seed(100, 64, rep)
    assert {ks(r) for r in FP.FRESH_PD}.isdisjoint({ks(r) for r in FP.STORED_PD})
    stored_labels = ['0', 'A@0.01', 'A@0.03', 'A@0.1', 'A@0.2', 'A@0.3', 'A@0.5', 'A@1', 'A@10', 'F@0.001', 'FA@1e-05', 'B@0.001', 'T@0.1', 'T@1']

    def seeds(game, runs, labels):
        out = set()
        for r in runs:
            for ro in (0, 1): out.add(RP.run_seed('founders|primary|%d' % ro, r))
            for lab in labels: out.add(RP.run_seed('dynamics|primary|%s|full|%s|10000|False' % (game, lab), r))
        return out
    fresh_labels = ['A@%g%s' % (lv, sfx) for lv in FP.LEVELS for sfx in ('', '+X', '+S')] + \
                   ['%s@%g%s' % (r, lv, sfx) for r in ('Af', 'Am') for lv in FP.LEVELS for sfx in ('', '+X', '+S')]
    for game in ('rps', 'insp'):
        assert seeds(game, FP.FRESH_LT, fresh_labels).isdisjoint(seeds(game, FP.STORED_LT, stored_labels + fresh_labels))


# ---------------------------------------------------------------------------------------------------------------- PD
def _pd_cache():
    return os.path.exists(os.path.join(ROOT, 'runs', 'detectors', 'K', 'static', 'A.npy'))


def test_pd_recorder_is_read_only_and_shows_no_forfeit(tmp_path):
    if not _pd_cache(): pytest.skip('PD cache absent')
    import forfeit_pricing_pd as FD
    import failure_pricing_confirm as F
    recs = FD.pd_cell_af(0.1, reps=[300], out_dir=str(tmp_path), horizon=60, quiet=True)
    ref = F.pd_cell('A', 0.1, reps=[300], out_dir=str(tmp_path), horizon=60, name='ref', quiet=True)
    a, r = recs[0], ref[0]
    assert a['ffe']['forfeit_weight'] == 0 and a['ffe']['max_steps'] <= FD.KPD
    for k in ('last_gen', 'frozen_at', 'n_types'):
        assert a[k] == r[k], k
    assert a['final']['pcc'] == r['final']['pcc'] and a['ledger'] == r['ledger']
