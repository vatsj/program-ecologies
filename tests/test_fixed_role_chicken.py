"""Tests for fixed-role chicken and hawk-dove (notes/fixed-role-chicken.md §1.10)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import fixed_role_chicken as F


def test_three_tables():
    assert F.GAMES['chicken'].tolist() == [[-10, 2], [-1, 0]]
    assert F.GAMES['hd3'].tolist() == [[-0.5, 2], [0, 1]]          # V = 2, C = 3: (V - C)/2, V, 0, V/2
    assert F.GAMES['hd6'].tolist() == [[-2, 2], [0, 1]]
    for g in F.GAME_NAMES:
        t = F.tsrp(g)
        assert t['T'] > t['R'] and t['S'] > t['P']                    # anti-coordination
    assert F.benchmark('chicken') == 1 and F.benchmark('hd3') == 2 and F.benchmark('hd6') == 2
    assert abs(F.fstar('chicken') - 0.75) < 1e-12 and abs(F.fstar('hd3') - 0.2) < 1e-12 and abs(F.fstar('hd6') - 0.5) < 1e-12
    assert abs(F.xstar('chicken') - 2 / 11) < 1e-12 and abs(F.xstar('hd3') - 2 / 3) < 1e-12 and abs(F.xstar('hd6') - 1 / 3) < 1e-12
    # the chicken table is the repo's games/chicken.yaml
    import yaml
    cfg = yaml.safe_load(open(os.path.join(F.ROOT, 'games', 'chicken.yaml')))
    p = cfg['payoffs']
    assert [[p['Straight']['Straight'], p['Straight']['Swerve']], [p['Swerve']['Straight'], p['Swerve']['Swerve']]] == F.GAMES['chicken'].tolist()


def test_catalogues():
    expect = dict(weak=(46, 1852), modal=(51, 1020), W0=(12, 666), M0=(8, 666), const=(2, 2))
    for arm, (K, n) in expect.items():
        d = F.catalogue(arm)
        assert d['K'] == K and d['n_programs'] == n, (arm, d['K'], d['n_programs'])
        assert abs(d['mu'].sum() - 1) < 1e-12
        assert d['S'][d['iSt']].max() < 1e-12 and d['S'][d['iSw']].min() > 1 - 1e-12      # the constants
        # classes are distinct by play
        R = np.round(d['S'], 9)
        assert len({(R[k].tobytes(), R[:, k].tobytes()) for k in range(K)}) == K
    mb = {arm: F.catalogue(arm)['mu'][F.catalogue(arm)['tags'] == 'bridge'].sum() for arm in ('weak', 'modal', 'W0', 'M0')}
    assert abs(mb['weak'] - 0.00185) < 5e-5 and abs(mb['modal'] - 0.0310) < 5e-4
    assert abs(mb['W0'] - 0.00396) < 5e-5 and abs(mb['M0'] - 0.00396) < 5e-5
    # payoff classes coincide with play classes in every game
    for arm in ('weak', 'modal', 'W0', 'M0'):
        d = F.catalogue(arm)
        for g in F.GAME_NAMES:
            U = np.round(F.payoff(d['S'], g), 9)
            assert len({(U[k].tobytes(), U[:, k].tobytes()) for k in range(d['K'])}) == d['K']


def test_conventions_strict_in_action_space():
    for g in F.GAME_NAMES:
        d = F.catalogue('const')
        U = F.payoff(d['S'], g)
        St, Sw = d['iSt'], d['iSw']
        assert U[St, Sw] > U[Sw, Sw] + 1e-9          # winner's deviation loses
        assert U[Sw, St] > U[St, St] + 1e-9          # loser's deviation loses
        assert not (U[Sw, Sw] >= U[St, Sw])          # mutual swerve is not an equilibrium
        assert not (U[St, St] >= U[Sw, St])          # crash is not an equilibrium


def test_hand_bridge_tables():
    d = F.catalogue('weak')
    i = {n: k for k, n in enumerate(d['names'])}
    S = d['S']
    b1, b2, b4, b5 = i['not(THEM(ME))'], i['not(THEM(THEM))'], i['not(THEM(^Swerve))'], i['not(THEM(^Straight))']
    assert S[b1, b1] == 1 and S[b2, b2] == 1 and S[b1, b2] == 1 and S[b2, b1] == 1      # regress -> minimax Swerve
    assert S[b4, b1] == 1 and S[b1, b4] == 0                                             # (B1 | B4) is role-1-wins
    assert S[b5, b5] == 0                                                                # not(THEM(^Straight)) crashes with itself
    assert S[b5, b4] == 0 and S[b4, b5] == 1
    for b in (b1, b2, b4, b5):
        assert S[b, d['iSt']] == 1 and S[b, d['iSw']] == 0
    # modal: BOXD bridges crash with themselves, not(BOX) bridges swerve with themselves
    m = F.catalogue('modal')
    j = {n: k for k, n in enumerate(m['names'])}
    assert m['S'][j['BOXD(THEM(ME))'], j['BOXD(THEM(ME))']] == 0
    assert m['S'][j['not(BOX(THEM(ME)))'], j['not(BOX(THEM(ME)))']] == 1


def test_matched_pair_differs_only_on_matcher_bridge_cells():
    dw, dm = F.catalogue('W0'), F.catalogue('M0')
    Sw = dw['S'][np.ix_(dw['prog_cls'], dw['prog_cls'])]
    Sm = dm['S'][np.ix_(dw['prog_cls_M0'], dw['prog_cls_M0'])]
    diff = np.abs(Sw - Sm) > 1e-9
    assert diff.sum() == 2000
    # every differing cell is between two self-referential readers (never a constant): the weak regress resolves to
    # the minimax Swerve where the modal box resolves by Loeb (notes 1.10 corrects the 1.5 hand claim)
    cw = dw['prog_cls']
    for a, b in zip(*np.nonzero(diff)):
        assert cw[a] not in (dw['iSt'], dw['iSw']) and cw[b] not in (dw['iSt'], dw['iSw'])
        assert 'THEM' in dw['names'][cw[a]] and 'THEM' in dw['names'][cw[b]]


def test_classifier_on_constructed_islands():
    d = F.catalogue('weak')
    i = {n: k for k, n in enumerate(d['names'])}
    Jp = F.joint(d['S'])

    def isl(x, y):
        X = np.zeros(d['K']); Y = np.zeros(d['K'])
        for k, v in x.items(): X[i[k]] = v
        for k, v in y.items(): Y[i[k]] = v
        return F.classify(np.einsum('a,b,abk->k', X, Y, Jp))
    # a polymorphic island implementing a perfect one-sided norm counts as the norm
    assert isl({'Straight': 0.6, 'and(THEM(ME),Straight)': 0.1, 'not(THEM(ME))': 0.3}, {'Swerve': 1.0}) == F.R1
    assert isl({'Straight': 1.0}, {'Swerve': 0.5, 'or(THEM(ME),Swerve)': 0.3, 'not(THEM(THEM))': 0.2}) == F.R1
    # bridges in both seats are not a convention: they swerve with each other
    assert isl({'Straight': 0.6, 'not(THEM(ME))': 0.4}, {'Swerve': 0.5, 'not(THEM(THEM))': 0.5}) == F.MIXED
    assert isl({'Swerve': 1.0}, {'Straight': 1.0}) == F.R2
    # two monomorphic readers that crash count as crash
    assert isl({'not(THEM(^Straight))': 1.0}, {'not(THEM(^Straight))': 1.0}) == F.CRASH
    assert isl({'not(THEM(ME))': 1.0}, {'not(THEM(ME))': 1.0}) == F.DOVE
    assert isl({'X': 1.0}, {'X': 1.0}) == F.MIXED
    # two distinct readers can anti-coordinate
    assert isl({'not(THEM(^Straight))': 1.0}, {'not(THEM(^Swerve))': 1.0}) == F.R1
    # tolerance 0.95
    assert isl({'Straight': 0.96, 'Swerve': 0.04}, {'Swerve': 1.0}) == F.R1
    assert isl({'Straight': 0.94, 'Swerve': 0.06}, {'Swerve': 1.0}) == F.MIXED


def test_lottery_seed_law():
    d = F.catalogue('weak')
    rng = np.random.default_rng(1)
    c = F.seed_counts(d['mu'], 2000, 100, rng)
    assert c.shape == (2000, 2, d['K'])
    assert (c.sum(2) == 100).all()
    f = c.sum((0, 1)) / c.sum()
    assert np.abs(f - d['mu']).max() < 0.005
    assert not (c[:, 0] == c[:, 1]).all()                         # roles drawn independently
    # paired seeds: one program draw, two semantics
    dw, dm = F.catalogue('W0'), F.catalogue('M0')
    a, b = F.paired_seed_counts(dw, dm, 8, 100, np.random.default_rng(2))
    assert (a.sum(2) == 100).all() and (b.sum(2) == 100).all()
    # forced founders: matched founder mass
    fi = F.forced_counts(d, 64, 100, 0.1, np.random.default_rng(3), bridges=True)
    fr = F.forced_counts(d, 64, 100, 0.1, np.random.default_rng(3), bridges=False)
    assert (fi.sum(2) == 100).all() and (fr.sum(2) == 100).all()
    br = d['tags'] == 'bridge'
    assert (fi[:, :, br].sum(2) == 10).all() and (fr[:, :, br].sum(2) == 0).all()
    assert (fr[:32, 0, d['iSt']] == 100).all() and (fr[32:, 0, d['iSw']] == 100).all()


def test_role_swap_mirror():
    d = F.catalogue('weak')
    U = np.ascontiguousarray(F.payoff(d['S'], 'chicken'))
    init = F.seed_counts(d['mu'], 6, 30, np.random.default_rng(5))
    s0, n0, g0 = F.sim_two_pop(U, U, init, 30, F.W, 1 / 30, 60, 10, 99, 0, 0)
    s1, n1, g1 = F.sim_two_pop(U, U, init[:, ::-1, :].copy(), 30, F.W, 1 / 30, 60, 10, 99, 1, 0)
    assert (s0 == s1[:, :, ::-1, :]).all()


def test_chain_symmetry_and_solver():
    for arm in ('W0', 'M0', 'const'):
        d = F.catalogue(arm)
        U = F.payoff(d['S'], 'hd3')
        for N in (100, 10000):
            ch = F.two_pop_chain(U, d['mu'], N)
            lp = F.two_pop_chain_logcheck(U, d['mu'], N)
            assert 0.5 * np.abs(np.exp(lp) - np.exp(ch['lpi'])).sum() < 1e-9
            pi = np.exp(ch['lpi'])
            assert np.abs(pi - pi.T).max() < 1e-9                  # role-exchange symmetry: pi(a|b) = pi(b|a)


def test_e3():
    d = F.catalogue('weak')
    K = d['K']; U = F.payoff(d['S'], 'chicken'); lp = F.classify(F.joint(d['S']))
    St, Sw = d['iSt'], d['iSw']
    b1 = d['names'].index('not(THEM(ME))')
    c0 = np.zeros(K, np.int64); c1 = np.zeros(K, np.int64)
    c0[St] = 100; c1[Sw] = 100
    own0, own1 = c0 > 0, c1 > 0
    assert F.e3_island(c0, c1, own0, own1, U, U, lp, K) == F.R1
    pool0 = own0.copy(); pool0[b1] = True
    pool1 = own1.copy(); pool1[St] = True
    # a bridge can join the winner seat, then the opposite convention's Straight joins the loser seat: crash pairs
    assert F.e3_island(c0, c1, pool0, pool1, U, U, lp, K) == -1
    # without the bridge the opposite convention's Straight cannot join
    assert F.e3_island(c0, c1, own0, pool1, U, U, lp, K) == F.R1


def test_static_closure():
    for g in F.GAME_NAMES:
        s = F.static('const', g)
        assert s['n_closed'] == 2 and sorted(map(tuple, s['closed_with_convention'])) == [('R1',), ('R2',)]
        for arm in ('weak', 'modal', 'W0', 'M0'):
            s = F.static(arm, g)
            assert len(s['closed_with_convention']) == 1
            assert 'R1' in s['closed_with_convention'][0] and 'R2' in s['closed_with_convention'][0]
            p = s['escape_path']
            assert [e['edge'] for e in p[1:]] == ['neutral', 'strict']
