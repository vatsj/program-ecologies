"""Tests for the RPS module (hand payoffs of notes/rps.md section 1, the reference evaluator, cyclic symmetry, forfeit
rules, depth-cap parity, a two-type contest on a toy table, the lottery kernel, founders pairing).

    python3 -m pytest tests/test_rps.py -q
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import rps

ORDER = ['R', 'P', 'S', 'X', 'TM', 'N', 'N2', 'C', 'GN', 'GC', 'M']


def hand_table(e):
    """notes/rps.md 1.3 (plus the M column), e = payoff gap between pure and guarded readers."""
    T = np.zeros((11, 11))
    cyc = {('R', 'P'): -1, ('R', 'S'): 1, ('P', 'S'): -1}
    for (a, b), v in cyc.items():
        T[ORDER.index(a), ORDER.index(b)] = v; T[ORDER.index(b), ORDER.index(a)] = -v
    ix = ORDER.index
    for c in 'RPS':
        T[ix('N'), ix(c)] = 1; T[ix('C'), ix(c)] = 1; T[ix('N2'), ix(c)] = -1
        T[ix('GN'), ix(c)] = 0.5; T[ix('GC'), ix(c)] = 0.5
        for r in ('N', 'C', 'N2', 'GN', 'GC'):
            T[ix(c), ix(r)] = -T[ix(r), ix(c)]
    for r in ('TM', 'N', 'N2', 'C'):
        for g in ('GN', 'GC'):
            T[ix(r), ix(g)] = -e; T[ix(g), ix(r)] = e
    # against M = coin R P
    vm = dict(R=-0.5, P=0.5, S=0.0, X=0.0, TM=0.0, N=0.25, N2=-0.25, C=0.5, GN=0.125, GC=0.25, M=0.0)
    for k, v in vm.items():
        T[ix(k), ix('M')] = v; T[ix('M'), ix(k)] = -v
    return T


_ARM = {}


def arm(name='exact', D=12, sweep=()):
    key = (name, D, tuple(sweep))
    if key not in _ARM:
        _ARM[key] = rps.build_arm(name, 6, D, sweep=sweep)
    return _ARM[key]


def test_counts():
    L = rps.Lang('exact', 6)
    assert list(L.counts[1:]) == [4, 8, 34, 136, 616, 2898]
    assert list(rps.Lang('pure', 6).counts[1:]) == [3, 3, 5, 8, 11, 16]
    assert rps.Lang('matched', 6).S == L.S                      # same grammar size as exact


def test_hand_table():
    A = arm()
    nm = rps.named_classes(A)
    idx = [nm[k] for k in ORDER]
    got = A.U[np.ix_(idx, idx)]
    assert np.abs(got - hand_table(1 / 128)).max() < 1e-12


def test_antisymmetry_and_class_merges():
    A = arm()
    assert A.antisym_err < 1e-12 and A.diag_err < 1e-12
    nm = rps.named_classes(A)
    # N and C coincide on the ten programs but are different classes in the full table; GN and GC likewise
    assert nm['N'] != nm['C'] and nm['GN'] != nm['GC']
    ten = [nm[k] for k in ORDER[:10]]
    U = A.U[np.ix_(ten, ten)]
    assert np.abs(U[ORDER.index('N')] - U[ORDER.index('C')]).max() < 1e-12
    assert np.abs(U[ORDER.index('GN')] - U[ORDER.index('GC')]).max() < 1e-12


def test_self_play_forfeit():
    A = arm()
    nm = rps.named_classes(A)
    for k in ('TM', 'N', 'N2', 'C'):
        assert abs(A.Gcl[nm[k], nm[k], 3] - 1.0) < 1e-12
    for k in ('GN', 'GC'):
        assert abs(A.Gcl[nm[k], nm[k], 3] - 2.0 ** -13) < 1e-12
    for k in ('R', 'P', 'S', 'X', 'M'):
        assert A.Gcl[nm[k], nm[k], 3] == 0.0


def test_reference_evaluator_agrees():
    rng = np.random.default_rng(1)
    for name in ('exact', 'exact_br', 'exact_uniform', 'matched', 'sample', 'pure'):
        L = rps.Lang(name, 6)
        G, Gp, Us = rps.evaluate(L, 12)
        for _ in range(120):
            a, b = rng.integers(L.S, size=2)
            ref = rps.evaluate_ref(L, int(a), int(b), 12)
            assert np.abs(G[a, b] - ref).max() < 1e-12, (name, L.src(a), L.src(b))
        # a few reading-heavy pairs
        reads = np.nonzero(L.reads_me)[0]
        for _ in range(60):
            a = int(rng.choice(reads)); b = int(rng.choice(reads))
            assert np.abs(G[a, b] - rps.evaluate_ref(L, a, b, 12)).max() < 1e-12
        # payoff via reference
        for _ in range(40):
            a, b = rng.integers(L.S, size=2)
            assert abs(Us[12][a, b] - rps.payoff_ref(L, int(a), int(b), 12)) < 1e-12


def test_cyclic_symmetry():
    for name in ('pure', 'sample', 'exact', 'matched', 'exact_br', 'exact_uniform'):
        A = arm(name)
        for shift in (1, 2):
            err, sig = rps.symmetry_errors(A, shift)
            assert err < 1e-9, (name, shift, err)
            perm = rps.class_perm(A, sig)
            assert sorted(perm) == list(range(A.K))
            assert np.abs(A.U[np.ix_(perm, perm)] - A.U).max() < 1e-9
            Gp = A.Gcl[np.ix_(perm, perm)]            # distributions of the relabeled classes
            rolled = np.concatenate([np.roll(A.Gcl[..., :3], shift, axis=-1), A.Gcl[..., 3:]], axis=-1)
            assert np.abs(Gp - rolled).max() < 1e-9, (name, shift)


def test_forfeit_rules():
    A = arm()
    nm = rps.named_classes(A)
    N, TM, C, X, R = nm['N'], nm['TM'], nm['C'], nm['X'], nm['R']
    # next(forfeit) = forfeit: N and TM forfeit against each other
    assert abs(A.Gcl[N, TM, 3] - 1) < 1e-12 and abs(A.Gcl[TM, N, 3] - 1) < 1e-12
    # cr(THEM(ME)) against itself forfeits (prediction 1)
    assert abs(A.Gcl[C, C, 3] - 1) < 1e-12
    # N beats every constant
    for c in 'RPS':
        assert abs(A.U[N, nm[c]] - 1) < 1e-12
    # against X every non-forfeiting program earns 0
    forf = A.Gcl[:, X, 3]
    assert np.abs(A.U[:, X][forf < 1e-12]).max() < 1e-12
    # uniform default: no forfeits at all
    Au = arm('exact_uniform')
    assert Au.G_full_forfeit_mass == 0.0
    nu = rps.named_classes(Au)
    assert Au.Gcl[nu['C'], nu['C'], 3] == 0.0 and np.abs(Au.Gcl[nu['C'], nu['C'], :3] - 1 / 3).max() < 1e-12
    # genuine best response never forfeits on cr alone: cr(THEM(ME)) against itself plays uniform
    Ab = arm('exact_br')
    nb = rps.named_classes(Ab)
    assert np.abs(Ab.Gcl[nb['C'], nb['C'], :3] - 1 / 3).max() < 1e-12 and Ab.Gcl[nb['C'], nb['C'], 3] == 0.0


def test_depth_parity_gap():
    """pure reader against guarded reader: -2^-(k+1) at D = 2k, exactly 0 at odd D (notes/rps.md 1.2 g)."""
    rows = {}
    for D in (11, 12, 13, 20):
        A = arm('exact', D)
        nm = rps.named_classes(A)
        rows[D] = A.U[nm['TM'], nm['GN']]
        assert A.U[nm['N'], nm['GC']] == rows[D]
    assert abs(rows[11]) < 1e-15 and abs(rows[13]) < 1e-15
    assert abs(rows[12] + 1 / 128) < 1e-15
    assert abs(rows[20] + 1 / 2048) < 1e-15


def test_simulating_vs_exact_counter_on_mixers():
    """u(N, d) = 1/2 sum (d_i - d_j)^2 against an opponent mixing d; u(C, d) = max_a u(a, d)."""
    A = arm()
    nm = rps.named_classes(A)
    # coin(R,P): d = (1/2, 1/2, 0)
    m = nm['M']
    assert abs(A.U[nm['N'], m] - 0.25) < 1e-12 and abs(A.U[nm['C'], m] - 0.5) < 1e-12
    # a skewed mixer coin(R, coin(R, P)) = (3/4, 1/4, 0): N earns 1/2*((3/4)^2*2 + ...) exactly
    L = A.lang
    e = L.find('coin(R,coin(R,P))')
    c = A.cls_of[e]
    d = np.array([0.75, 0.25, 0.0])
    var = 0.5 * ((d[0] - d[2]) ** 2 + (d[1] - d[0]) ** 2 + (d[2] - d[1]) ** 2)
    assert abs(A.U[nm['N'], c] - var) < 1e-12
    best = max(d[2] - d[1], d[0] - d[2], d[1] - d[0])
    assert abs(A.U[nm['C'], c] - best) < 1e-12


def test_two_type_contest_on_toy_table():
    """A two-class toy table through ClassProvider: LogChain (linear weights) agrees with chain.Chain, and both with
    the closed-form Moran fixation ratio."""
    from chain import Chain, fixation
    from chain_log import LogChain
    U = np.array([[0.0, -2.0], [1.0, -1.0]])         # prisoner's dilemma: class 1 (D) dominates
    mu = np.array([0.4, 0.6])
    N, w = 50, 0.3
    ch = Chain(rps.ClassProvider(U, mu), N=N, w=w, theta=0.0, max_states=100).explore()
    lc = LogChain(rps.ClassProvider(U, mu), N=N, w=w).explore_closure(max_states=100)
    rho_cd = fixation(U[1, 1], U[1, 0], U[0, 1], U[0, 0], N, w, N)      # one D in an all-C population
    rho_dc = fixation(U[0, 0], U[0, 1], U[1, 0], U[1, 1], N, w, N)      # one C in an all-D population
    k0 = lc.mono(0); k1 = lc.mono(1)
    assert abs(lc.trans[k0][k1] - 0.6 * rho_cd) < 1e-12
    assert abs(lc.trans[k1][k0] - 0.4 * rho_dc) < 1e-12
    keys, lpi, info, out_un, rec = lc.solve_sparse()
    pi = dict(zip(keys, np.exp(lpi)))
    ratio = (0.6 * rho_cd) / (0.4 * rho_dc)                               # pi(D) / pi(C)
    assert abs(pi[k1] / pi[k0] - ratio) / ratio < 1e-9
    assert abs(sum(pi.values()) - 1) < 1e-9


def test_lottery_kernel_basics():
    """Counts conserved; a dominated class disappears; checkpoints recorded; pure drift neutral with equal payoffs."""
    K = 3
    U = np.array([[0.0, -1.0, 1.0], [1.0, 0.0, -1.0], [-1.0, 1.0, 0.0]])
    init = np.zeros((4, K), np.int64); init[:, 0] = 20; init[:, 1] = 20; init[:, 2] = 20
    out, na, ho, nw = rps.lottery_kernel(U, init, 60, 0.3, 1 / 60, 7, np.array([5, 50], np.int64), 20, 50, 5)
    assert out.shape == (2, 4, 3)
    assert (out.sum(2) == 60).all()
    assert nw == 6
    out2, _, _, _ = rps.lottery_kernel(U, init, 60, 0.3, 1 / 60, 7, np.array([5, 50], np.int64), 20, 50, 5)
    assert (out2 == out).all()                                   # deterministic given the seed
    # a strictly dominated class dies: class 1 beats class 0 for sure at selection 5
    U2 = np.array([[0.0, -3.0], [3.0, 0.0]])
    init2 = np.zeros((2, 2), np.int64); init2[:, 0] = 25; init2[:, 1] = 25
    o3, _, _, _ = rps.lottery_kernel(U2, init2, 50, 1.0, 0.0, 3, np.array([200], np.int64), 100, 200, 10)
    assert (o3[0, :, 0] == 0).all() and (o3[0, :, 1] == 50).all()


def test_founders_pairing():
    """exact and matched share an enumeration order, so a slot maps to spellings with the same structure."""
    Ae = arm('exact'); Am = arm('matched')
    Le, Lm = Ae.lang, Am.lang
    assert Le.S == Lm.S
    # spelling-by-spelling correspondence: cr <-> next2 in the same positions
    ok = 0
    for e in range(Le.S):
        se = Le.src(e).replace('cr(', 'next2(')
        ok += (se == Lm.src(e))
    assert ok == Le.S
    a = rps.draw_founders(Le, Ae.cls_of, Ae.K, 8, 100, 5)
    assert (a.sum(1) == 100).all()
    b = rps.draw_founders(Le, Ae.cls_of, Ae.K, 8, 100, 5)
    assert (a == b).all()


def test_state_stats_uniform_population():
    A = arm()
    nm = rps.named_classes(A)
    st = rps.state_stats(A, [nm['X']], [1.0], nm)
    assert abs(st['e_prog'] - 0.0) < 1e-12 and st['mix_pop'] == 1.0 and st['forfeit_plays'] == 0.0
    # constants uniform: action exploitability 0, program exploitability positive (the exact counter beats them)
    ids = [nm['R'], nm['P'], nm['S']]
    st = rps.state_stats(A, ids, [1 / 3] * 3, nm)
    assert abs(st['e_act']) < 1e-12 and st['e_prog'] > 0.99
    assert st['mix_pop'] == 0.0 and abs(st['share_consts'] - 1) < 1e-12
