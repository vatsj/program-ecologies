"""Tests for the fully realizable social organization run (notes/sog-fully-realizable.md §1).  Whole encounters are
run by the term (the K3' library, the programs compiled with their inventories) and compared with the evaluator and the
kernel.  Codes: boss action = 3 * wage index + whack index (pay(1/2, none) = 7, pay(0, none) = 1); 'C' work, 'D' strike."""
import os
import random
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.setrecursionlimit(1000000)

import sog_full as F
import sog_full_run as R
import sog_full_kern as KN

R.load_costc()


def ev_(arm, mode):
    return R.evaluator(arm, mode)


def pid(ev, role, name, inv='full'):
    return R.named_pid(ev, role, name, inv)


def play_ev(ev, b, x, y):
    tr = ev.triple(b, x, y)
    return (tr['boss'], tr['a1'], tr['a2'])


def play_term(ev, b, x, y):
    return R.term_encounter(ev, b, x, y, produce=False)['play']


# notes §1.3.1, column H (full H lists)
HAND_H = [
    (('D*', 'T1', 'T1'), (7, 'C', 'C')),
    (('D*', 'T1', 'scab'), (7, 'C', 'C')),
    (('pay(1/2,none)', 'U_eq', 'U_eq'), (7, 'C', 'C')),
    (('pay(1/2,none)', 'U_eq', 'scab'), (7, 'C', 'C')),
    (('pay(0,none)', 'U_eq', 'U_eq'), (1, 'D', 'D')),
    (('pay(0,none)', 'U_eq', 'scab'), (1, 'C', 'C')),
    (('D*', 'U_eq', 'U_eq'), (7, 'C', 'C')),
    (('D*', 'U_eq', 'scab'), (1, 'C', 'C')),
    (('B_eq', 'T1', 'T1'), (7, 'C', 'C')),
    (('B_eq', 'T1p', 'T1p'), (1, 'D', 'D')),
    (('B_eq', 'T1', 'scab'), (7, 'C', 'C')),
    (('B_eq', 'scab', 'T1'), (1, 'C', 'D')),
    (('B_id', 'U_eq', 'U_eq'), (7, 'C', 'C')),
    (('B_id', 'U_eq', 'scab'), (1, 'C', 'C')),
    (('pay(1/2,none)', 'XM', 'XM'), (7, 'C', 'C')),
    (('pay(1/2,none)', 'XM', 'scab'), (7, 'D', 'C')),
    (('WF', 'T1', 'T1'), (1, 'D', 'D')),
]


@pytest.mark.parametrize('names,want', HAND_H)
def test_hand_plays_H_by_whole_runs(names, want):
    """The named triples' plays under H: the evaluator equals the whole run by the term, and both equal the hand
    table (the eq atoms in both roles: EQ, N1, EQW)."""
    ev = ev_('eq', 'H')
    b, x, y = pid(ev, 'B', names[0]), pid(ev, 'W', names[1]), pid(ev, 'W', names[2])
    assert play_ev(ev, b, x, y) == want
    assert play_term(ev, b, x, y) == want


def test_sham_matches_eq_on_distinct_sources_and_reads_false_on_copies():
    """The sham literal has the eq atom's node count and step count on distinct sources (same grammar 'id'); on
    copies it reads false: U_eq beside a copy works under pay(0) in the sham arm, strikes in the eq arm."""
    eq, sh = ev_('eq', 'H'), ev_('sham', 'H')
    assert eq.g.gram == sh.g.gram == 'id'
    for names in (('pay(0,none)', 'U_eq', 'scab'), ('D*', 'U_eq', 'T1'), ('B_eq', 'T1p', 'XM'), ('B_id', 'XM', 'T1')):
        te = R.term_encounter(eq, pid(eq, 'B', names[0]), pid(eq, 'W', names[1]), pid(eq, 'W', names[2]), False)
        ts = R.term_encounter(sh, pid(sh, 'B', names[0]), pid(sh, 'W', names[1]), pid(sh, 'W', names[2]), False)
        assert te['play'] == ts['play']
        assert te['steps'] == ts['steps']
    # where the identity atom reads true the arms differ (B_eq pays the named source only in the eq arm)
    assert play_term(eq, pid(eq, 'B', 'B_eq'), pid(eq, 'W', 'T1'), pid(eq, 'W', 'XM'))[0] == 7
    assert play_term(sh, pid(sh, 'B', 'B_eq'), pid(sh, 'W', 'T1'), pid(sh, 'W', 'XM'))[0] == 1
    b, u = pid(sh, 'B', 'pay(0,none)'), pid(sh, 'W', 'U_eq')
    assert play_term(sh, b, u, u) == (1, 'C', 'C') == play_ev(sh, b, u, u)
    b, u = pid(eq, 'B', 'pay(0,none)'), pid(eq, 'W', 'U_eq')
    assert play_term(eq, b, u, u) == (1, 'D', 'D')


def test_eq_relation_is_spelling_equality():
    """EQ (srcof equality of quotes) is true iff the two workers have one spelling, on random pairs of spellings and
    inventories, by the term: the worker if(EQ, strike, work) under pay(1/2)."""
    ev = ev_('eq', 'H')
    g = ev.g
    W = g.roles['W']
    x = F._if(F.EQa, F._L('S'), F._L('W'))
    sp = W['spellings'].index(x)
    probe = ev.reg.get('W', sp, F.full_inv(g, 'W', int(W['tau'][sp])))
    b = pid(ev, 'B', 'pay(1/2,none)')
    rng = random.Random(3)
    for _ in range(6):
        sp2 = rng.randrange(len(W['spellings']))
        y = ev.reg.get('W', sp2, F.full_inv(g, 'W', int(W['tau'][sp2])))
        a1 = play_term(ev, b, probe, y)[1]
        assert a1 == ('D' if sp2 == sp else 'C')
    assert play_term(ev, b, probe, ev.reg.get('W', sp, F.empty_inv('W')))[1] == 'D'


def test_gate_on_named_triples():
    """S-nonself_3: workers are refused beside an exact copy, bosses never; beside a non-copy T1 writes its strike
    certificate; the evaluator's productions equal the term's PROD3 runs."""
    ev = ev_('eq', 'S')
    E = F.empty_inv
    d, t1, scab = pid(ev, 'B', 'D*', E('B')), pid(ev, 'W', 'T1', E('W')), pid(ev, 'W', 'scab', E('W'))
    out = ev.productions(d, t1, t1)
    assert out[1][2] == [('refused',)] and out[2][2] == [('refused',)]
    assert out[0][2] and out[0][2][0] != ('refused',)
    out = ev.productions(d, t1, scab)
    nt1 = ev.reg[out[1][1]]
    assert nt1.inv[F.FAM['W'].index(F.A_STRIKE)] != ()
    te = R.term_encounter(ev, d, t1, scab, produce=True)
    for (p, np_, rec), trec in zip(out, te['prods']):
        for k, r in enumerate(rec):
            if r[0] == 'refused':
                assert trec[0][0] == 'refused'; continue
            assert r[1] == trec[k][1]
            if r[1] == 'found':
                assert ev.reg[np_].inv[r[0]] == (trec[k][2],)


def test_greenbeard_strike_certificate_is_not_producible():
    """Claim N3 (notes §1.3.2): U_eq's strike script exists only on its EQ-true path, so PROD3 finds none at a
    non-self root; the EQ-true path has one (it is H-listed)."""
    t = F.dt(F.NAMED_W['U_eq'])
    for boxv in ('T', 'F'):
        sc_f, _ = F.sym_prod3(t, 'W', F.A_STRIKE, lambda n: False, lambda a: boxv)
        assert sc_f is None
    sc_t, _ = F.sym_prod3(t, 'W', F.A_STRIKE, lambda n: True, lambda a: 'F')
    assert sc_t is not None
    _, per = F.h_list(t, 'W')
    assert per[F.A_STRIKE]


def test_lumping_twins_and_inventories():
    """Row classes: T1 and its respelling T1' are distinct classes (the is-T1 bit) and B_eq separates them; a
    respelling of U_eq shares U_eq's class; identical sources with different inventories are distinct classes; every
    case's evaluator play equals the whole run."""
    ev = ev_('eq', 'H')
    g = ev.g
    W = g.roles['W']
    t1, t1p = pid(ev, 'W', 'T1'), pid(ev, 'W', 'T1p')
    assert ev.canon(t1) != ev.canon(t1p)
    beq = pid(ev, 'B', 'B_eq')
    assert play_ev(ev, beq, t1, t1) != play_ev(ev, beq, t1p, t1p)
    u = pid(ev, 'W', 'U_eq')
    tk = W['tau'][W['spellings'].index(F.NAMED_W['U_eq'])]
    twins = [s for s in range(len(W['spellings'])) if W['tau'][s] == tk and W['spellings'][s] != F.NAMED_W['U_eq']]
    assert twins
    u2 = ev.reg.get('W', twins[0], F.full_inv(g, 'W', int(tk)))
    assert ev.canon(u2) == ev.canon(u)
    p0 = pid(ev, 'B', 'pay(0,none)')
    for (x, y) in ((u, u2), (u2, u2), (u, u)):
        assert play_ev(ev, p0, x, y) == play_term(ev, p0, x, y)
    assert play_ev(ev, p0, u, u2) == (1, 'C', 'C') and play_ev(ev, p0, u2, u2) == (1, 'D', 'D')
    full = ev.reg[t1].inv
    sd = F.FAM['W'].index(F.A_STRIKE)
    only_d = tuple(full[i] if i == sd else () for i in range(len(full)))
    t1d = ev.reg.get('W', ev.reg[t1].sp, only_d)
    assert ev.canon(t1d) != ev.canon(t1)
    for b in ('D*', 'pay(1/2,none)', 'B_eq'):
        bp = pid(ev, 'B', b)
        for (x, y) in ((t1d, t1), (t1, t1d), (t1d, t1d)):
            assert play_ev(ev, bp, x, y) == play_term(ev, bp, x, y)


def test_cost_model_on_replayed_encounters():
    """The cost model on a sample: whole encounters by the term (plays, step counts, PROD3 outcomes) equal the
    evaluator's composition (notes §1.9 (3)-(4); the full validation is runs/sog-full-validate.json)."""
    res, bad = R.validate_replays(n=16, seed=77)
    assert res['encounters'] == 16
    assert res['play_match'] == 16, bad[:3]
    # play step counts: class-level canonical own-step tables (notes §1.13) are approximate (median 0.07%, 90th
    # percentile 6% on 400 replays); plays and production outcomes must match exactly
    for b in bad:
        if b['kind'] == 'play':
            for p, t in zip(b['psteps'], b['tsteps']):
                assert abs(p - t) <= max(8, 0.15 * t), b
    assert res.get('attempt_match', 0) == res.get('attempts', 0), [b for b in bad if b['kind'] == 'prod'][:3]


@pytest.mark.parametrize('arm,mode', [('eq', 'S'), ('eq', 'H'), ('sham', 'S')])
def test_kernel_tables_equal_evaluator(arm, mode):
    """The kernel's composed encounter (pair rows, boss rows, worker rows, productions) equals the evaluator on
    every present triple of a small run (no support reduction: the kernel is the executable semantics)."""
    ev = ev_(arm, mode)
    run = R.Run(ev, dict(name='t', arm=arm, mode=mode, N=8, I=2, mN=1.0, share=False), 4)
    run.prefill()
    T, PT = run.T(), run.PT()
    A = run.A
    oi = np.zeros(10, np.int64); oc = np.zeros(15, np.int64); miss = np.zeros(8, np.int64)
    newt = np.zeros(3, np.int64); ctr = np.zeros(KN.NCTR, np.int64)
    live_eq = 1 if 'EQ' in ev.live else 0
    n = 0
    for i in range(run.I):
        for ta in range(run.npres[i, 0]):
            for tb in range(run.npres[i, 1]):
                for tc in range(run.npres[i, 2]):
                    bb, xx, yy = run.pres[i, 0, ta], run.pres[i, 1, tb], run.pres[i, 2, tc]
                    j = KN.jcode(bb, xx, yy, T, A['WACT'], live_eq, oi, oc, miss)
                    assert j >= 0
                    b, x, y = run.btypes[bb], run.wtypes[xx], run.wtypes[yy]
                    tr = ev.triple(b, x, y)
                    assert A['B_ACT'][oi[1]] == tr['boss']
                    assert j == 4 * tr['boss'] + 2 * (tr['a1'] == 'D') + (tr['a2'] == 'D')
                    if mode == 'S':
                        for _ in range(50):          # fill production rows on demand, as the kernel does
                            T, PT = run.T(), run.PT()
                            ok = KN.productions(bb, xx, yy, T, PT, A['BLACK'], A['WLACK'], live_eq, ev.K, ev.P,
                                                F.VPLUS, F.PROD_W, ctr, miss, oi, oc, newt, False)
                            if ok: break
                            if miss[0] == 8: run.grow_pairs()
                            else: run.fill_miss(miss.copy())
                        assert ok
                        out = ev.productions(b, x, y, tr)
                        for s, (p, np_, rec) in enumerate(out):
                            tl = run.btypes if s == 0 else run.wtypes
                            got = tl[newt[s]] if newt[s] >= 0 else p
                            assert ev.canon(got) == ev.canon(np_) and ev.reg[got].sp == ev.reg[np_].sp
                    n += 1
    assert n > 0
