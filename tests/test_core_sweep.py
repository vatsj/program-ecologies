"""Tests for the leader-value core sweep (notes/core-existence-sweep.md)."""
import os
import sys
import itertools
import warnings

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import core_sweep as CS

warnings.filterwarnings('ignore')


def tu(G, mode='ind', sel='pess'):
    n = G.n
    v = {S: G.leader(S, mode, sel)['v'] for S in CS.proper(n)}
    v[CS.full(n)] = G.vN()['v']
    return v, CS.tu_core(v, n)


# ---------------------------------------------------------------- the catalogue (notes/leader-value-core.md)
def test_catalogue_reproduced():
    r = CS.catalogue_report()
    for sel in ('pess', 'opt'):
        assert r['PD'][sel]['ntu_core'] == [['C', 'C']]
        assert r['PD'][sel]['v']['[0]'] == -1 and r['PD'][sel]['v']['[1]'] == -1
        for g in ('chicken', 'hd3', 'hd6', 'dollar5', 'dollar3'):
            assert r[g][sel]['ntu_core'] == [] and r[g][sel]['tu']['verdict'] == 'empty'
        assert r['chicken'][sel]['v']['[0]'] == 2 and abs(r['dollar5'][sel]['v']['[0]'] - 5 / 6) < 1e-12
    assert r['SOG']['opt']['ntu_core'] == [['0', 'work']]                       # ties for the leader
    assert r['SOG']['pess']['ntu_core'] == [['0', 'work'], ['1/4', 'work']]      # ties against the leader
    assert r['SOG']['pess']['v']['[0]'] == 0.75 and r['SOG']['opt']['v']['[0]'] == 1.0
    assert r['SOG']['pess']['v']['[1]'] == 0.0
    # majority division: pairs are decisive; under pess no coalition gains from moving first (S11)
    assert all(abs(x) < 1e-12 for x in r['dollar3']['pess']['fma'].values())
    assert r['dollar3']['pess']['v']['[0, 1]'] == 1.0 and r['dollar3']['pess']['v']['[0]'] == 0.0
    assert abs(r['dollar3']['opt']['v']['[0]'] - 2 / 3) < 1e-12


def test_dollar3_payoff_matches_repo_rule():
    try:
        import dollar3 as D
    except Exception:
        return
    for prof in itertools.product(range(9), repeat=3):
        u, _ = D.outcome(D.PARTNER, *prof)
        assert tuple(x / 6 for x in u) == CS.dollar3_payoff(prof)


# ---------------------------------------------------------------- balancedness on known cases
def test_balancedness_known_cases():
    # three-player majority game: empty, certified by the three pairs at weight 1/2
    v = {S: (1.0 if CS.popcount(S) >= 2 else 0.0) for S in range(1, 8)}
    t = CS.tu_core(v, 3)
    assert t['verdict'] == 'empty' and t['collection_balanced_exact']
    assert abs(t['gap'] - 0.5) < 1e-9
    assert sorted(len(c[0]) for c in t['collection']) == [2, 2, 2]
    assert all(c[1] == '1/2' for c in t['collection'])
    # glove game L = {0}, R = {1, 2}: core = everything to the scarce side
    v = {1: 0, 2: 0, 4: 0, 3: 1, 5: 1, 6: 0, 7: 1}
    t = CS.tu_core(v, 3)
    assert t['verdict'] == 'tight' and abs(t['alloc'][0] - 1) < 1e-9
    # convex (supermodular) game v(S) = |S|^2: nonempty with slack
    v = {S: CS.popcount(S) ** 2 for S in range(1, 16)}
    assert CS.tu_core(v, 4)['verdict'] == 'nonempty'
    # superadditivity failure as in chicken
    v = {1: 2.0, 2: 2.0, 3: 1.0}
    t = CS.tu_core(v, 2)
    assert t['verdict'] == 'empty' and abs(t['gap'] - 3.0) < 1e-9


# ---------------------------------------------------------------- symmetric Cournot (notes §2)
def test_symmetric_cournot_closed_form():
    for n in (2, 3, 4, 5):
        G = CS.Cournot([0.0] * n)
        v, t = tu(G)
        for S in CS.proper(n):
            k = CS.popcount(S)
            assert abs(v[S] - 1 / (4 * (n - k + 1))) < 1e-12
            assert abs(G.sim(S) - 1 / (n - k + 2) ** 2) < 1e-12
        assert abs(v[CS.full(n)] - 0.25) < 1e-12
        assert t['verdict'] == 'tight'
        assert np.allclose(t['alloc'], 1 / (4 * n))
        ntu = G.ntu_core()
        assert ntu['verdict'] == 'tight' and abs(ntu['Q'] - 0.5) < 1e-6 and np.allclose(ntu['z'], 1 / (4 * n), atol=1e-8)


def test_symmetric_cournot_panel():
    for n in (3, 4):
        G = CS.Cournot([0.0] * n)
        v, t = tu(G, 'coord')
        assert all(abs(v[S] - 1 / 8) < 1e-12 for S in CS.proper(n))
        assert t['verdict'] == 'empty'
    v, t = tu(CS.Cournot([0.0, 0.0]), 'coord')
    assert t['verdict'] == 'tight'


def test_cournot_ray_onset_and_n2_ntu():
    # one cost deviation: emptiness on (h*, 1/(2n-1)) by the singleton partition (notes §3.1)
    for n in (3, 4):
        hs = 2 * n / ((n + 1) ** 2 * (n - 1) + 1)
        hi = 1 / (2 * n - 1)
        G = CS.Cournot([0.0] * (n - 1) + [hs - 0.005])
        assert tu(G)[1]['verdict'] == 'nonempty'
        G = CS.Cournot([0.0] * (n - 1) + [0.5 * (hs + hi)])
        r, v, L = CS.evaluate(G)
        assert r['tu']['verdict'] == 'empty' and CS.violating_singletons(r, n)
    for d in (0.05, 0.2, 0.45):
        assert CS.Cournot([0.0, d]).ntu_core()['verdict'] == 'empty'
        assert tu(CS.Cournot([0.0, d]))[1]['verdict'] == 'nonempty'
    assert CS.Cournot([0.0, 0.6]).ntu_core()['verdict'] in ('tight', 'nonempty')


def test_cournot_leader_vs_bruteforce():
    rng = np.random.default_rng(3)
    for _ in range(5):
        c = np.r_[0.0, np.sort(rng.uniform(0, 0.5, 2))]
        G = CS.Cournot(c)
        for S in CS.proper(3):
            Sm = CS.members(S, 3)
            Cm = [i for i in range(3) if not S >> i & 1]
            best = -np.inf
            for QS in np.linspace(0, 1, 2001):
                # followers' Cournot equilibrium by best-response iteration
                q = np.zeros(3)
                for _ in range(400):
                    for j in Cm:
                        q[j] = max(0.0, (1 - QS - (q[Cm].sum() - q[j]) - c[j]) / 2)
                p = 1 - QS - q[Cm].sum()
                best = max(best, QS * (p - c[Sm].min()))
            assert abs(G.leader(S)['v'] - best) < 2e-4


# ---------------------------------------------------------------- other closed forms
def test_bertrand_symmetric_closed_form():
    for g in (0.2, 0.5, 0.8):
        G = CS.bertrand_game([0.0, 0.0], g)
        v, t = tu(G)
        assert abs(v[1] - (1 + g / 2) ** 2 / (4 * (1 - g ** 2 / 2))) < 1e-12
        assert abs(v[3] - 1 / (2 * (1 - g))) < 1e-12
        assert abs(G.sim(1) - 1 / (2 - g) ** 2) < 1e-12
        assert t['verdict'] == 'nonempty'


def test_public_goods_n2_log_threshold():
    th_star = 1 / (2 * (1 - np.log(2)))
    assert tu(CS.PublicGoods([th_star - 0.01] * 2, 'log'))[1]['verdict'] == 'nonempty'
    assert tu(CS.PublicGoods([th_star + 0.01] * 2, 'log'))[1]['verdict'] == 'empty'
    assert tu(CS.PublicGoods([1.3, 1.3], 'sqrt'))[1]['verdict'] == 'tight'
    v, t = tu(CS.PublicGoods([2.0, 2.0], 'log'))
    assert abs(v[1] - 2 * np.log(2)) < 1e-12 and abs(v[3] - (4 * np.log(4) - 3)) < 1e-12


def test_hombertrand_grid_limit():
    """The closed form (suprema) against a discrete price grid with ties split equally."""
    c = [0.0, 0.2]
    G = CS.HomBertrand(c)
    prices = np.round(np.arange(0, 1.0001, 0.01), 4)
    def pay(p):
        pr = [prices[p[0]], prices[p[1]]]
        lo = min(pr)
        win = [i for i in range(2) if pr[i] == lo]
        return tuple((pr[i] - c[i]) * (1 - lo) / len(win) if i in win else 0.0 for i in range(2))
    F = CS.FiniteGame('hb', [list(prices)] * 2, pay)
    for S in (1, 2):
        assert abs(F.leader(S, 'ind', 'pess')['v'] - G.leader(S)['v']) < 0.011


def test_lemma_sma_lq_symmetric():
    """Symmetric LQ: follower dominance at every coalition and an equal split in the core (notes §3.4)."""
    for sigma in (0.0, 0.5, -1.0):
        G = CS.lq_game([1.0, 1.0, 1.0], 0.15, sigma)
        r, v, L = CS.evaluate(G)
        if sigma >= 0:
            assert r['all_dominance']
        assert r['tu']['verdict'] in ('nonempty', 'tight')
        assert CS.symmetric_equal_split_ok(v, 3) >= -1e-12


def test_exchange_equilibrium_in_core():
    rng = np.random.default_rng(7)
    for util, rr in (('cd', None), ('ces', -1.0), ('ces', 0.5)):
        a = rng.dirichlet(np.ones(2), 3)
        w = rng.uniform(0.1, 1, (3, 2))
        E = CS.Exchange(a, w, util, rr)
        p, X = E.equilibrium()
        assert np.allclose(X.sum(axis=0), w.sum(axis=0), atol=1e-9)
        assert np.allclose(X @ p, w @ p, atol=1e-9)
        z = np.array([E.u(i, X[i]) for i in range(3)])
        assert max(E.block_margin(S, z) for S in CS.proper(3)) <= 1e-7
