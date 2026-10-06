"""Tests for the carrier-population milestone (notes/carrier-populations.md §1.10)."""
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import lt_code as L
import lt_cert as C
import carrier_populations as CP

K = 10 ** 6
V = K // 4
_CACHE = {}


def cat(n, arm='P'):
    k = (n, arm)
    if k not in _CACHE:
        _CACHE[k] = CP.Catalogue(n, arm, K)
    return _CACHE[k]


def S(p, q, a, e=0): return ('A', (e, p, q, a))


NAMED = {
    'Cc': ('C',), 'Dc': ('D',),
    'CB': ('if', S('them', 'me', 'C'), ('C',), ('D',)),
    'CB1': ('if', S('them', 'me', 'C'), ('if', S('me', 'them', 'C'), ('C',), ('D',)), ('D',)),
    'CBP': ('if', S('them', 'me', 'C'), ('if', S('them', 'D', 'D'), ('C',), ('D',)), ('D',)),
    'LobC': ('if', S('me', 'them', 'C'), ('C',), ('D',)),
    'CBdef': ('if', S('them', 'me', 'C'), ('D',), ('C',)),
}
HAND = {   # notes §1.7: row's action against column
    'Cc': 'CCCCCCC', 'Dc': 'DDDDDDD', 'CB': 'CDCCCCD', 'CB1': 'CDCCCCD', 'CBP': 'DDCCCDD', 'LobC': 'CCCCCCC', 'CBdef': 'DCCCCDC'}
ORDER = ['Cc', 'Dc', 'CB', 'CB1', 'CBP', 'LobC', 'CBdef']


def named_terms(c):
    idx = {x: i for i, x in enumerate(c.sexprs)}
    out = {}
    for nm, x in NAMED.items():
        i = idx[x]
        k = [k for k, s in enumerate(c.spell) if s['i'] == i and s['choice'] != 'none'][0]
        out[nm] = (k, c.term(k))
    return out


def test_counts():
    assert CP.count_by_hand(7, 16) == {1: 2, 2: 0, 3: 0, 4: 64, 5: 64, 6: 2112, 7: 10304}
    assert CP.count_by_hand(7, 32) == {1: 2, 2: 0, 3: 0, 4: 128, 5: 128, 6: 8320, 7: 41088}
    G = CP.enumerate_grammar(7, (0,))
    assert {n: len(v) for n, v in G.items()} == CP.count_by_hand(7, 16)
    tot = np.cumsum([len(G[n]) for n in range(1, 8)])
    assert (tot[4], tot[5], tot[6]) == (130, 2242, 12546)
    GE = CP.enumerate_grammar(6, (0, 5))
    assert sum(len(v) for v in GE.values()) == 8578
    assert all(CP.nodes(x) == n for n, xs in G.items() for x in xs)


def test_production_matches_milestone4():
    progs, info = C.build_arm(K, 'S')
    c = cat(7)
    nt = named_terms(c)
    for nm, m4 in (('CB', 'CB'), ('CB1', 'CB1'), ('CBP', 'CBP'), ('LobC', 'LobC'), ('Cc', 'Ccert')):
        assert C.h_getcerts(nt[nm][1]) == C.h_getcerts(progs[m4]), nm
    # the catalogue's CB spelling is milestone 4's CB term exactly
    assert L.canon_term(nt['CB'][1]) == L.canon_term(progs['CB'])


def test_named_plays_hand_table():
    c = cat(7)
    nt = named_terms(c)
    for x in ORDER:
        row = ''
        for y in ORDER:
            L.CACHE.clear()
            row += L.play(nt[x][1], nt[y][1], K)[0]
        assert row == HAND[x], (x, row, HAND[x])


def _tau_tables(c):
    from carrier_populations_run import compose
    import carrier_populations_run as R
    T = c.T
    reps = {t: (c.rep(t, 0), c.rep(t, 1)) for t in range(T)}
    out = {}
    for kind in ('ideal', 'exec'):
        chk = CP.Checker(kind, c.V, c.K)
        keys = R.unit_keys(c.tau_atoms)
        UV = {k: dict(val=np.zeros(T, np.int8)) for k in keys}
        for u in range(T):
            tm = c.term(reps[u][0])
            for (k, md, a) in keys:
                m = tm if k == 'self' else (L.PROG_C if k == 'C' else L.PROG_D)
                UV[(k, md, a)]['val'][u] = 1 if chk(md, tm, m, a)[0] == 'T' else 0
        Sx, Rx = CP.needed_pairs(c.tau_atoms, T)
        need = CP.pair_matrix_entries(Sx, Rx, T, c.has_entry)
        CH = {k: np.zeros((T, T), np.int8) for k in set(list(Sx) + list(Rx))}
        for (md, a), ent in need.items():
            for (t, m) in ent:
                tt, mm = (c.term(reps[t][0]), c.term(reps[t][1])) if t == m else (c.term(reps[t][0]), c.term(reps[m][0]))
                CH[(md, a)][t, m] = 1 if chk(md, tt, mm, a)[0] == 'T' else 0
        out[kind] = compose(c.tau_dt, dict(CH=CH, UV=UV))
    return out


def test_composition_and_lemmaT_n5():
    """Every pair of n <= 5 spellings: the whole actual play equals the tau-composed table; ideal equals exec."""
    c = cat(5)
    tabs = _tau_tables(c)
    A_id, s_id = tabs['ideal']
    A_ex, s_ex = tabs['exec']
    assert (A_id == A_ex).all() and (s_id == s_ex).all()
    n = len(c.spell)
    Asp = CP.spelling_matrix(c, A_ex, s_ex, list(range(n)))
    bad = 0
    for x in range(n):
        for y in range(n):
            L.CACHE.clear()
            r = L.play(c.term(x), c.term(y), K)[0]
            bad += (r == 'C') != bool(Asp[x, y])
    assert bad == 0


def test_lemmaT_sample_n6():
    """Same-tau spellings are interchangeable (direct plays, no table): rows, columns, self and cross-twin."""
    c = cat(6)
    rng = random.Random(7)
    multi = [t for t in range(c.T) if len(c.members[t]) >= 2]
    n = len(c.spell)
    for _ in range(40):
        t = rng.choice(multi)
        x, x2 = rng.sample(c.members[t], 2)
        z = rng.randrange(n)
        if z in (x, x2): continue
        P = lambda p, q: (L.CACHE.clear(), L.play(c.term(p), c.term(q), K)[0])[1]
        assert P(x, z) == P(x2, z) and P(z, x) == P(z, x2)
        assert P(x, x) == P(x2, x2) and P(x, x2) == P(x2, x)


def test_empty_selection_is_F():
    c = cat(6)
    rng = random.Random(3)
    for _ in range(60):
        k = rng.randrange(len(c.spell)); m = rng.randrange(len(c.spell))
        t = c.tau[k]
        for a in ('C', 'D'):
            if not c.has_entry(t, a):
                assert C.check_value(0, V, c.term(k), c.term(m), a, K)[0] == 'F'


def test_lemmaG_n5():
    from carrier_populations import pay_matrix
    c = cat(5)
    A, s = _tau_tables(c)['exec']
    Ad = A.copy(); Ad[np.arange(c.T), np.arange(c.T)] = s
    U, PCC = pay_matrix(Ad)
    for t in range(c.T):
        est = Ad[t, t] == 1 and Ad[t, c.tau[[k for k, sp in enumerate(c.spell) if c.sexprs[sp['i']] == ('D',)][0]]] == 0
        if est and CP.s_guarded(c.tau_dt[t]):
            assert (U[:, t] <= U[t, t] + 1e-12).all()


def test_bor_bridge():
    """notes §1.7: Bor cooperates with CB on entry 0 and on entry 5, with itself, and defects on D (E production)."""
    prod = C.Producer(host=CP.ExactHost())
    probes = {md: CP.make_probes(prod, md, K, V) for md in (0, 5)}
    def mk(x):
        body = CP.body_term(x, V, K)
        return CP.program(x, CP.produce_multi(prod, [0, 5], lambda cc: C.carrier(body, cc), probes, K, V), V, K)
    bor = mk(('if', ('or', S('them', 'me', 'C', 0), S('them', 'me', 'C', 5)), ('C',), ('D',)))
    cb0 = mk(NAMED['CB'])
    cb5 = mk(('if', S('them', 'me', 'C', 5), ('C',), ('D',)))
    d = mk(('D',))
    def pl(p, q):
        L.CACHE.clear(); return L.play(p, q, K)[0] + L.play(q, p, K)[0]
    assert pl(bor, cb0) == 'CC'
    assert pl(bor, cb5) == 'CC'
    assert pl(bor, bor) == 'CC'
    assert pl(bor, d) == 'DD'
    assert pl(cb0, cb5) == 'DD'
