"""Tests for provenance (notes/provenance.md §1.11).  Term-level tests run whole encounters of the term; the tests that
need the run's untracked static cache (runs/provenance/) skip without it."""
import json
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.setrecursionlimit(1000000)

import lt_cert as C
import lt_code as L
import provenance as PV
import provenance_run as PR

K, V, PC = PR.K, PR.V, PR.PCAP
OUT = PR.OUT
HAVE_STATIC = os.path.exists(os.path.join(OUT, 'static', 'A.npy')) and os.path.exists(os.path.join(OUT, 'sets.npz'))
IOTA = 'EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Ax] · Hyp]'
SIG_CB1 = 'EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp]'
SIG_CB = 'EvR*; ChkR[EvR*; Ax · Hyp]'


def P(name):
    return PR.named_prog(name, None)


def side(x, y, rule, st=None, shadow=None, Pcap=PC):
    st = st or PV.TermState()
    nx, ev = PV.term_side(x, y, rule, st, K, V, Pcap, shadow_nonself=shadow)
    return nx, ev, st


def cs(p):
    return [C.show_script(s) for s in p.cseq]


# ------------------------------------------------------------------ identity bookkeeping and the streams
def test_identity_bookkeeping_rules_do_not_split_quotes():
    from numba.typed import Dict
    from numba import types
    d = Dict.empty(key_type=types.int64, value_type=types.int64)
    tu, tr, ts, ta = (np.zeros(8, np.int64) for _ in range(4))
    k0, n = PV.make_type(d, tu, tr, ts, ta, 0, 5, PV.R_SSELF, 3, 0)
    k1, n = PV.make_type(d, tu, tr, ts, ta, n, 5, PV.R_SNON, 3, 0)          # same unit and spelling, other rule
    k2, n = PV.make_type(d, tu, tr, ts, ta, n, 5, PV.R_SSELF, 4, 0)         # same unit, other spelling: a twin
    k3, n = PV.make_type(d, tu, tr, ts, ta, n, 6, PV.R_SSELF, 3, 0)         # same spelling, other list
    assert k0 != k1                                                          # distinct types (rule is metadata)
    assert PV.relation(k0, k1, tu, ts) == 2                                  # ... but one quote
    assert PV.relation(k0, k2, tu, ts) == 1
    assert PV.relation(k0, k3, tu, ts) == 0
    A = np.zeros((8, 8), np.int8); selfa = np.ones(8, np.int8)
    assert PV.pay(k0, k1, tu, ts, A, selfa) == 0.0                           # self-play payoff (C, C)
    assert PV.pay(k0, k2, tu, ts, A, selfa) == -1.0                          # twin play from A (D, D)


def test_counter_rng_is_event_indexed():
    a = [PV.ru(123, ev, j) for ev in range(50) for j in range(10)]
    b = [PV.ru(123, ev, j) for ev in range(50) for j in range(10)]
    assert a == b
    assert len(set(a)) == len(a)
    assert all(0.0 <= x < 1.0 for x in a)
    # a draw does not depend on which other draws were made
    assert PV.ru(123, 7, 3) == PV.ru(123, 7, 3)
    assert PV.ru(123, 7, 3) != PV.ru(124, 7, 3)
    assert abs(np.mean([PV.ru(5, ev, 0) for ev in range(20000)]) - 0.5) < 0.01


# ------------------------------------------------------------------ S-k selection and tie-break (kernel)
def _window(cands, codes, osv_valid, rule):
    T, ns = 1, 4
    OSV = np.zeros((T, ns, 64), np.int8)
    for s, cset in osv_valid.items():
        for c in cset: OSV[0, s, c] = 1
    wn = np.array([[len(codes)]], np.int64)
    wsid = np.full((1, 1, 3), -1, np.int64); wcode = np.zeros((1, 1, 3), np.int64)
    for m, (s, c) in enumerate(zip(cands, codes)):
        wsid[0, 0, m] = s; wcode[0, 0, m] = c
    ctr = np.zeros(PV.NCTR, np.int64)
    return PV.window_close(0, 0, 0, rule, wn, wsid, wcode, OSV, ctr)


def test_window_safeguard_tiebreak_strict_and_inadmissible():
    # candidate 0 (written at the self root, code 37) valid only there; candidate 1 valid at both: safeguard keeps 1
    assert _window([0, 1], [37, 13], {0: {37}, 1: {37, 13}}, PV.R_SK2) == (1, 1)
    # one admissible candidate valid against one partner only: the fallback keeps it, the strict rule clears
    assert _window([0, -1, -1], [37, 3, 5], {0: {37}}, PV.R_SK3) == (0, 2)
    assert _window([0, -1, -1], [37, 3, 5], {0: {37}}, PV.R_SK3S) == (-1, 0)
    # two candidates each valid against one partner: the tie-break keeps the earliest
    assert _window([2, 3], [1, 2], {2: {1}, 3: {2}}, PV.R_SK2) == (2, 2)
    # zero validity is inadmissible: nothing kept
    assert _window([2], [1], {}, PV.R_SK3) == (-1, 0)
    # among several safeguard-meeting candidates the earliest
    assert _window([2, 3, 1], [1, 2, 3], {2: {1, 2}, 3: {1, 2, 3}, 1: {3}}, PV.R_SK3) == (2, 1)


# ------------------------------------------------------------------ the rules by whole runs of the term (notes §1.4)
def test_self_root_scripts_and_snonself_refusal():
    cb1 = P('CB1')
    nx, ev, _ = side(cb1, cb1, 'S-self')
    assert cs(nx) == [IOTA]                                   # the identity script at the self root
    nx, ev, _ = side(cb1, cb1, 'S-nonself')
    assert cs(nx) == [] and len(nx.dseq) == 1                 # no C production against one's own source; D produced
    nx, ev, _ = side(cb1, P('CB'), 'S-nonself')
    assert cs(nx) == [SIG_CB1]                                # the general script against a distinct source
    mm = P('MM')
    nx, _, _ = side(mm, mm, 'S-self')
    assert cs(nx) == [IOTA]
    nx, _, _ = side(mm, P('CB'), 'S-nonself')
    assert cs(nx) == []                                       # MM has no script at any distinct root
    cb = P('CB')
    for y in (cb, P('CB1'), P('C'), P('D')):
        nx, _, _ = side(cb, y, 'S-self')
        assert cs(nx) == [SIG_CB]                             # CB writes σCB against every partner


def test_twin_spelling_is_another_source():
    cb1, twin = P('CB1'), PR.named_prog(PR.TWIN['CB1'], None)
    assert cb1.body != twin.body
    nx, _, _ = side(cb1, twin, 'S-nonself')
    assert cs(nx) == [SIG_CB1]                                # a respelling is a distinct source and a distinct quote


def test_self_delayed_produces_against_the_actual_partner():
    cb1 = P('CB1')
    nx, ev, _ = side(cb1, cb1, 'S-self-delayed', shadow=True)
    assert cs(nx) == [IOTA]                                   # shadow non-self: produce, against oneself if present
    nx, ev, _ = side(cb1, cb1, 'S-self-delayed', shadow=False)
    assert cs(nx) == [] and ('skip',) in ev


def test_coverage_rule_windows():
    cb1, cb, mm, d = P('CB1'), P('CB'), P('MM'), P('D')
    st = PV.TermState()
    x, ev, _ = side(cb1, cb1, 'S-2', st)                      # window: ι from the copy
    assert cs(x) == []
    x, ev, _ = side(x, cb, 'S-2', st)                         # second source: σCB1 validates at both roots
    assert cs(x) == [SIG_CB1]
    w = [e for e in ev if e[0] == 'window'][0]
    assert w[2] == [1, 2]                                      # scores: ι 1 (self only), σCB1 2
    st = PV.TermState()
    x, _, _ = side(mm, mm, 'S-2', st)
    x, ev, _ = side(x, cb, 'S-2', st)
    assert cs(x) == [IOTA] and ('fallback',) in ev            # MM's only candidate is ι: the fallback keeps it
    st = PV.TermState()
    x, _, _ = side(mm, mm, 'S-3 strict', st)
    x, _, _ = side(x, cb, 'S-3 strict', st)
    x, ev, _ = side(x, d, 'S-3 strict', st)
    assert cs(x) == [] and not st.window                      # the strict safeguard refuses it and clears


def test_cache_contract():
    cb, d = P('CB'), P('D')
    st = PV.TermState()
    x, ev, _ = side(cb, d, 'S-gate+cache', st)
    assert cs(x) == [SIG_CB] and ('invalidate',) in ev and st.cache == {}
    x, ev, _ = side(x, d, 'S-gate+cache', st)                 # gate F (D certifies nothing), production repeats σCB
    assert [v for v in st.cache.values()] == ['rejected']
    x2, ev2, _ = side(x, d, 'S-gate+cache', st)
    assert ev2[0] == ('hit', 'rejected')                      # a hit: neither gate nor production runs
    assert not any(e[0] in ('gate', 'prodC') for e in ev2)
    # the cache key reads one's own list: a changed list misses
    x3 = PR.G.Prog(x.name, x.body, None, x.cseq, ())          # the same C entry, the D entry gone
    x3, ev3, _ = side(x3, d, 'S-gate+cache', st)
    assert ev3[0][0] == 'gate'
    # rejection vs timeout: a production cap below the tactic's cost stores a timeout
    st2 = PV.TermState()
    y, ev, _ = side(P('CB1'), cb, 'S-gate+cache', st2, Pcap=200)
    assert list(st2.cache.values()) == ['timeout']


# ------------------------------------------------------------------ static audits (need the untracked cache)
@pytest.mark.skipif(not HAVE_STATIC, reason='needs runs/provenance static cache')
def test_snonself_never_writes_a_self_play_only_script():
    rep = json.load(open(os.path.join(OUT, 'sets.json')))
    assert rep['spo_written_at_nonself_codes'] == 0
    LS = PR.lot_static('ext')
    P_ = LS['PRODC']; SPO = LS['SPO']
    for t in range(P_.shape[0]):
        for c in range(25):
            s = P_[t, c]
            if s >= 0:
                assert not SPO[t, s]


@pytest.mark.skipif(not HAVE_STATIC, reason='needs runs/provenance static cache')
def test_ablation_masses_and_pairing():
    LS = PR.lot_static('ext')
    mu, Q, R = LS['mu'], LS['Q'], LS['R']
    for rep in range(6):
        sp_a, _, _ = PR.founders('ablation', rep, LS)
        sp_n, _, _ = PR.founders('Snon', rep, LS)
        inq = np.isin(sp_n, Q)
        assert not np.isin(sp_a, Q).any()                    # no clique founder
        assert (sp_a[~inq] == sp_n[~inq]).all()              # every other founder identical (paired)
        assert np.isin(sp_a[inq], R).all()                   # replaced by a receiving spelling
    # the ablated prior: μ'(Q) = 0, μ'(R) = μ(R) + μ(Q), the rest unchanged
    mQ, mR = mu[Q].sum(), mu[R].sum()
    mu2 = mu.copy(); mu2[Q] = 0; mu2[R] = mu[R] * (1 + mQ / mR)
    assert abs(mu2.sum() - 1) < 1e-12 and abs(mu2[R].sum() - (mR + mQ)) < 1e-12
