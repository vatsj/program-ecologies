"""Tests for the private tape in the realizable language (src/lt_tape*.py; notes/lt-tape.md section 1 is the hand table)."""
import os
import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import lt_tape as T
import lt_tape_games as G
import lt_tape_audit as A
from lt_tape import con, nat, L2, TP, EQ, IF, PL, THEM, ME

K = 10000
F = Fraction


def insp_env(K=K):
    ins, ee = G.catalogue_insp(K)
    terms, _ = G.arm_terms('insp', [ins, ee], 'full')
    names = [[t.name for t in ins], [t.name for t in ee]]
    prover = T.TProver(2, limit=3 * K)
    eng = T.Engine(prover, K=K, r=2, m=3)
    d0 = {n: x for n, x in zip(names[0], terms[0])}
    d1 = {n: x for n, x in zip(names[1], terms[1])}
    return eng, d0, d1


def rps_env(K=K):
    (tp,) = G.catalogue_rps(K)
    terms, _ = G.arm_terms('rps', [tp], 'full')
    prover = T.TProver(3, limit=3 * K)
    eng = T.Engine(prover, K=K, r=3, m=3)
    return eng, {t.name: x for t, x in zip(tp, terms[0])}


# ----------------------------------------------------------------------------------------------- hand table, section 1.2
HAND_LEAVES = {          # j -> {prefix: (action, depth)}
    1: {(0, 0, 0): 'I', (0, 0, 1): 'N', (0, 1): 'N', (1,): 'N'},
    2: {(0, 0): 'I', (0, 1): 'N', (1,): 'N'},
    3: {(0, 0): 'I', (0, 1, 0): 'I', (0, 1, 1): 'N', (1,): 'N'},
    4: {(0,): 'I', (1,): 'N'},
    5: {(0,): 'I', (1, 0, 0): 'I', (1, 0, 1): 'N', (1, 1): 'N'},
    6: {(0,): 'I', (1, 0): 'I', (1, 1): 'N'},
    7: {(0,): 'I', (1, 0): 'I', (1, 1, 0): 'I', (1, 1, 1): 'N'},
}
HAND_ESTEPS = {1: F(29, 4), 2: F(13, 2), 3: F(29, 4), 4: F(5), 5: F(29, 4), 6: F(13, 2), 7: F(29, 4)}
HAND_MIXER_SIZE = {1: 21, 2: 15, 3: 21, 4: 9, 5: 21, 6: 15, 7: 21}
HAND_CERTS = {1: 15, 2: 13, 3: 21, 4: 11, 5: 19, 6: 17, 7: 25}
HAND_CARR_SIZE = {1: 38, 2: 30, 3: 44, 4: 22, 6: 34}


def test_hand_table_mixers():
    eng, d0, d1 = insp_env()
    for j in range(1, 8):
        x = d0['M%d' % j]
        assert T.size(x) == HAND_MIXER_SIZE[j]
        d = eng.dist(x, d1['C0'])
        assert d['dist'] == {'I': F(j, 8), 'N': F(8 - j, 8)}
        assert d['steps'] == HAND_ESTEPS[j]
        # leaf list and depths from the exact tree
        leaves = {}
        def emit(w, o, used, rt, reason): leaves[len(leaves)] = (w, o, used)
        eng.explore(T.initial(x, d1['C0']), T.EMPTY_STORE, 0, (0,) * 5, F(1), emit)
        want = sorted((F(1, 2 ** len(p)), a, 2 + 3 * len(p)) for p, a in HAND_LEAVES[j].items())
        assert sorted(leaves.values()) == want
        # the inspectee mixer is the same tree with K at the cheat leaves
        y = d1['Mc%d' % j]
        dy = eng.dist(y, d0['I0'])
        assert dy['dist'] == {'K': F(j, 8), 'C': F(8 - j, 8)} and dy['steps'] == HAND_ESTEPS[j]


def test_cert_sizes_and_carriers():
    eng, d0, d1 = insp_env()
    for j in (1, 2, 3, 4, 6):
        x = d0['CARR%d' % j]
        assert T.size(x) == HAND_CARR_SIZE[j]
        certs = x[1][1][2]
        assert T.size(certs) == HAND_CERTS[j]
        stamp, ents = T.parse_cert(x)
        assert stamp == K and ents[0][0] == 'I'
    st, ents = T.parse_cert(d0['CARR3'])
    assert ents == [('I', [[0, 0], [0, 1, 0]])]
    assert T.parse_cert(d0['M3']) is None
    # a carrier plays exactly its mixer, one beta-step later
    for j in (1, 2, 3, 4, 6):
        dm = eng.dist(d0['M%d' % j], d1['C0']); dc = eng.dist(d0['CARR%d' % j], d1['C0'])
        assert dm['dist'] == dc['dist'] and dc['steps'] == dm['steps'] + 1


def test_RI_search_against_constant_is_8_and_12_steps():
    eng, d0, d1 = insp_env()
    d = eng.dist(d0['RI'], d1['C0'])
    assert d['dist'] == {'N': F(1)} and d['steps'] == 12
    assert d['route']['search'] == 8 and d['route']['plain'] == 4
    th = eng.th
    q = eng.prover.query(th.plays(d1['C0'], d0['RI'], 'C'), 8)
    assert q['W'] == 8 and q['found'] and q['size'] == 3
    # the refutation against K0 is dearer (prediction S3)
    q2 = eng.prover.query(th.plays(d1['K0'], d0['RI'], 'C'), 8)
    assert q2['complete'] and not q2['found'] and q2['W'] > 8


def test_route_totals():
    eng, d0, d1 = insp_env()
    PR_plain = {1: 43, 2: 28, 3: 43, 4: 16, 5: 43, 6: 28, 7: 43}
    for j, want in PR_plain.items():
        assert eng.dist(d1['PR3'], d0['M%d' % j])['steps'] == want
    PR_carr = {1: 47, 2: 31, 3: 47, 4: 18, 6: 31}
    CR_carr = {1: 17, 2: 14, 3: 27, 4: 11, 6: 21}
    for j in PR_carr:
        assert eng.dist(d1['PR3'], d0['CARR%d' % j])['steps'] == PR_carr[j]
        assert eng.dist(d1['CR3'], d0['CARR%d' % j])['steps'] == CR_carr[j]
        assert CR_carr[j] < PR_carr[j]                                   # S2
        assert eng.dist(d1['CR3'], d0['M%d' % j])['steps'] == 4
    assert eng.dist(d1['CR3'], d0['M3'])['dist'] == {'K': F(1)}          # blind to an uncertified mixer
    assert eng.dist(d1['PR3'], d0['I0'])['steps'] == 7 and eng.dist(d1['CR3'], d0['I0'])['steps'] == 4
    # SE against a constant: 8 steps
    assert eng.dist(d1['SE100k'], d0['I0'])['steps'] == 8
    # routes recorded
    d = eng.dist(d1['CR3'], d0['CARR3'])
    assert d['route']['check'] == 24 and d['route']['plain'] == 3
    d = eng.dist(d1['PR3'], d0['M3'])
    assert d['route']['enum'] == 40


def test_compliance_thresholds():
    eng, d0, d1 = insp_env()
    for j in range(1, 8):
        for k in (2, 3, 4):
            comply = eng.dist(d1['PR%d' % k], d0['M%d' % j])['dist']
            assert comply == ({'C': F(1)} if j >= k else {'K': F(1)})
    for j in (1, 2, 3, 4, 6):
        for k in (2, 3, 4):
            comply = eng.dist(d1['CR%d' % k], d0['CARR%d' % j])['dist']
            assert comply == ({'C': F(1)} if j >= k else {'K': F(1)})
    # PR3 is the exact best responder: it complies exactly when 4p - 1 > 0 on the grid (p >= 3/8) or is indifferent (p = 1/4)
    for j in range(1, 8):
        p = F(j, 8)
        gain = 1 - 4 * p                                                 # payoff of cheating
        assert (gain <= 0) == (j >= 2)


def test_payoff_formulas_inspection():
    eng, d0, d1 = insp_env()
    ps = {'I0': F(1), 'N0': F(0), **{'M%d' % j: F(j, 8) for j in range(1, 8)}}
    qs = {'C0': F(0), 'K0': F(1), **{'Mc%d' % j: F(j, 8) for j in range(1, 8)}}
    n0 = list(ps); n1 = list(qs)
    terms0 = [d0[n] for n in n0]; terms1 = [d1[n] for n in n1]
    G0, G1, S0, S1, RT0, RT1, FU0, FU1 = G.insp_tables(terms0, terms1, eng)
    UAg, UBg, UA, UB = G.insp_payoffs(G0, G1, S0, S1, 0.0)
    for a, na in enumerate(n0):
        for b, nb in enumerate(n1):
            p, q = float(ps[na]), float(qs[nb])
            assert abs(UAg[a, b] - (-p - 4 * (1 - p) * q)) < 1e-12
            assert abs(UBg[b, a] - q * (1 - 4 * p)) < 1e-12
    # the hand table of section 1.3
    ia = {n: i for i, n in enumerate(n0)}; ib = {n: i for i, n in enumerate(n1)}
    assert abs(UAg[ia['M3'], ib['Mc1']] - (-11 / 16)) < 1e-12 and abs(UBg[ib['Mc1'], ia['M3']] - (-1 / 16)) < 1e-12
    assert abs(UAg[ia['M4'], ib['Mc1']] - (-3 / 4)) < 1e-12


# ----------------------------------------------------------------------------------------------- tape semantics
def test_repeated_reads_and_privacy():
    eng, d0, d1 = insp_env()
    same = L2(IF(EQ(TP(0), TP(0)), con('C'), con('K')))
    assert eng.dist(same, d0['I0'])['dist'] == {'C': F(1)}
    # a sim draws its own fresh tape: the real digit and the sim's action are independent
    mc4 = d1['Mc4']
    prog = L2(IF(EQ(TP(0), nat(0)), IF(EQ(('run', nat(60), THEM, ME), con('K')), con('C'), con('K')),
                 IF(EQ(('run', nat(60), THEM, ME), con('K')), con('K'), con('C'))))
    d = eng.dist(prog, mc4)       # if the sim's digit equalled the real digit this would be {'C': 1}
    assert d['dist'] == {'C': F(1, 2), 'K': F(1, 2)}
    # two sims are independent of each other as well: P(equal) = 1/2
    two = L2(IF(EQ(('run', nat(60), THEM, ME), ('run', nat(60), THEM, ME)), con('C'), con('K')))
    assert eng.dist(two, mc4)['dist'] == {'C': F(1, 2), 'K': F(1, 2)}


def test_padded_space_reference_matches_branching_engine():
    eng, d0, d1 = insp_env(3000)
    cases = A.adaptive_cases()
    for nx in ('repeat', 'repeat_branch', 'branch_sim', 'indep', 'same_both', 'diff'):
        for y in (d1['C0'], d1['Mc4'], d1['K0']):
            ref = eng.dist_padded(cases[nx], y, ninv=2)
            d = eng.dist(cases[nx], y)
            assert ref['dist'] == d['dist'] and ref['steps'] == d['steps'], nx


def test_hash_and_simulators_rps():
    eng, r = rps_env()
    # SIM100 beats the explicitly terminating hash fixtures exactly, earns 0 against U, and the bias against B
    for h in ('H0', 'H1', 'H2'):
        for s in ('SIM100R', 'SIM100P', 'SIM100S'):
            dx = eng.dist(r[s], r[h]); dy = eng.dist(r[h], r[s])
            ug = float(sum(dx['dist'].get(a, 0) * dy['dist'].get(b, 0) * G.RPS.u(a, b) for a in 'RPS' for b in 'RPS'))
            assert abs(ug - 1.0) < 1e-12, (s, h, ug)
    for s in ('SIM100R', 'SIM100u'):
        du = eng.dist(r[s], r['U'])
        assert all(du['dist'].get(a, 0) == F(1, 3) for a in 'RPS')
    eng2, r2 = rps_env()
    tabs = G.rps_tables([r['SIM100R'], r['B_RP'], r['U'], r['PRR'], r['CRR'], r['CB_RP'], r['P0']], eng2)
    Ug, _ = G.rps_payoffs(tabs[0], tabs[1], 0.0)
    assert abs(Ug[0, 1] - 1 / 3) < 1e-12                  # SIM100 against the biased mixer: the bias, half the best response
    assert abs(Ug[6, 1] - 2 / 3) < 1e-12                  # the best response P0
    assert abs(Ug[3, 1] - 2 / 3) < 1e-12 and abs(Ug[3, 2]) < 1e-12     # PRR (enumeration) reads the bias, not U
    assert abs(Ug[4, 5] - 2 / 3) < 1e-12 and abs(Ug[4, 1]) < 1e-12     # CRR (check) reads the carrier, not the plain mixer
    assert abs(Ug[2]).max() < 1e-12 and abs(Ug[0, 2]) < 1e-12        # U earns 0 against everything (SIM100 included)


def test_pseudo_random_arm_is_predictable_and_junk_carriers_rejected():
    (tp,) = G.catalogue_rps(K)
    terms, _ = G.arm_terms('rps', [tp], 'prand')
    names = [t.name for t in tp]
    prover = T.TProver(3, limit=3 * K); eng = T.Engine(prover, K=K, r=3, m=3)
    u = terms[0][names.index('U')]; sim = terms[0][names.index('SIM100R')]; crr = terms[0][names.index('CRR')]
    cb = terms[0][names.index('CB_RP')]
    # U in the pseudo-random arm is a deterministic function of the opponent's source: the simulator predicts it exactly
    du = eng.dist(u, sim); ds = eng.dist(sim, u)
    assert len(du['dist']) == 1 and len(ds['dist']) == 1
    ug = sum(ds['dist'].get(a, 0) * du['dist'].get(b, 0) * G.RPS.u(a, b) for a in 'RPS' for b in 'RPS')
    assert ug == 1
    # the hash carrier's replay reads the opponent: its certificate is rejected, so CRR does not read it
    ok, charge, why = eng.check_cert(cb, 'R', 12)
    assert not ok


def test_nested_enumeration_returns_false_for_one_step():
    eng, r = rps_env()
    d = eng.dist(r['PRR'], r['PRR'])
    # the inner enumeration cannot enumerate: both fall back to uniform play and tie
    assert all(abs(float(d['dist'].get(a, 0)) - 1 / 3) < 1e-12 for a in 'RPS')


# ----------------------------------------------------------------------------------------------- price
def test_price_calibration():
    import lt_tape_run as RUN
    assert abs(RUN.C0 * RUN.K0 - 0.12) < 1e-15
    # a program that exhausts the fuel pays c * K = 0.12 (the loop: fix-point recursion)
    eng, d0, d1 = insp_env(500)
    # PB-like exhaustion: RIM against SE20 needs 8687 steps > 500 -> forfeit at K = 500
    d = eng.dist(d0['RIM'], d1['SE20k'])
    assert d['fuel'] == 1 and d['steps'] == 500


# ----------------------------------------------------------------------------------------------- K_T tape rules
def test_tape_rules_derive_for_all_tapes_only():
    eng, d0, d1 = insp_env()
    th = eng.th; P = eng.prover
    mc4 = d1['Mc4']; c0 = d1['C0']; ri = d0['RI']
    same = L2(IF(EQ(TP(0), nat(0)), con('C'), con('C')))
    diff = L2(IF(EQ(TP(0), nat(0)), con('C'), con('K')))
    qs = P.query(th.plays(same, ri, 'C'), 12)
    assert qs['found'] and qs['size'] == 9           # TapeR + two eq/if branches: size 9, beyond the responsive inspector's budget 8
    assert not P.query(th.plays(same, ri, 'C'), 8)['found']
    assert not P.query(th.plays(diff, ri, 'C'), 12)['found'] and not P.query(th.plays(diff, ri, 'K'), 12)['found']
    assert P.query(th.plays(c0, ri, 'C'), 12)['found']
    # the responsive inspector inspects a mixer: no for-all proof, so it plays I
    assert eng.dist(ri, mc4)['dist'] == {'I': F(1)}
    # and, with budget 8, also against `same` (its for-all proof has size 9); with budget 12 it plays N
    assert eng.dist(ri, same)['dist'] == {'I': F(1)}
    ri12 = L2(IF(('prove', nat(12), PL(THEM, ME, 'C')), con('N'), con('I')))
    assert eng.dist(ri12, same)['dist'] == {'N': F(1)}


def test_soundness_adaptive_and_certificates():
    out = A.run_all(K=3000, budgets=(8,))
    ad = out['adaptive']
    assert ad['false'] == 0 and ad['padded_ok'] == ad['padded_ref'] and ad['skipped'] == 0
    assert all(out['certs_honest_accepted'].values())
    assert all(out['certs_overclaim_rejected'].values())
    assert all(out['attacks_rejected'].values()), [k for k, v in out['attacks_rejected'].items() if not v]
