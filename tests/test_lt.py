"""Tests for the realizable language L_T and the calculus K_T (src/lt.py, src/lt_check.py)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import lt
from lt import *
import lt_check as LC


def test_frozen_terms():
    C, D, T, F = ('con', 'C'), ('con', 'D'), ('con', 'T'), ('con', 'F')
    ME, THEM = ('v', 1), ('v', 0)
    PLm = ('mk', 'plays', THEM, ME, C)
    assert FB(5) == ('lam', ('lam', ('if', ('prove', ('nat', 5), PLm), C, D)))
    assert G(5) == ('lam', ('lam', ('if', ('prove', ('nat', 5), PLm), D, C)))
    con = ('mk', 'not', ('mk', 'box', ('nat', 5), ('mk', 'bot')))
    assert FB1(5) == ('lam', ('lam', ('if', ('prove', ('nat', 5), ('mk', 'imp', con, PLm)), C, D)))
    assert PB(5)[1][1][2][1] == ('prove', ('nat', 5), ('mk', 'imp', con, ('mk', 'plays', THEM, ('quote', PROG_D), D)))
    assert SF(7) == ('lam', ('lam', ('if', ('eq', ('run', ('nat', 7), THEM, ME), C), C, D)))
    assert VRENAME(5) == FB(5)
    assert VWRAP(5)[1][1][2][1][1] == FB(5)


def run_value(t, K=10 ** 5):
    n = 0
    while n < K:
        r = step(t)
        if r[0] == 'value': return r[1], n
        if r[0] == 'stuck': return 'stuck', n
        assert r[0] == 'det'
        t = r[1]; n += 1
    return None, n


def test_evaluator_basics():
    # identity, if, pairs, quotes as nested pairs
    assert run_value(('app', ('lam', ('v', 0)), ('nat', 3))) == (('nat', 3), 1)
    assert run_value(('if', ('eq', ('nat', 1), ('nat', 1)), ('con', 'C'), ('con', 'D')))[0] == ('con', 'C')
    q = ('quote', ('lam', ('v', 0)))
    assert run_value(('fst', q))[0] == ('nat', 1)
    assert run_value(('snd', q))[0] == ('quote', ('v', 0))
    assert run_value(('eq', q, ('pair', ('nat', 1), ('pair', ('nat', 0), ('nat', 0)))))[0] == ('con', 'T')
    # fix: a divergent loop never reaches a value
    loop = ('app', ('fix', ('lam', ('app', ('v', 1), ('v', 0)))), ('nat', 0))
    assert run_value(loop, K=500)[0] is None
    # fix: count down to zero via a nat-equality test on a successor-free countdown (pairs as unary numbers)
    # f x = if eq(x, 0) then C else f (snd x), x = pair(1, pair(1, 0))
    body = ('lam', ('if', ('eq', ('v', 0), ('nat', 0)), ('con', 'C'), ('app', ('v', 1), ('snd', ('v', 0)))))
    prog = ('app', ('fix', body), ('pair', ('nat', 1), ('pair', ('nat', 1), ('nat', 0))))
    assert run_value(prog)[0] == ('con', 'C')


def test_independent_evaluator_agrees():
    cat = catalogue(8); register_names(cat)
    pr = Prover()
    for x in cat:
        for y in cat:
            tr = []
            run_play(pr, cat[x], cat[y], 10 ** 4, trace=tr)
            n, bad = LC.check_trace(tr)
            assert bad == 0 and n == len(tr) - 1


def test_sim_timeout_and_simulation_fairbot():
    cat = catalogue(8, k=20); pr = Prover()
    r = run_play(pr, cat['SF'], cat['SF'], 10 ** 4)
    assert r['play'] == 'D' and r['reason'] == 'value'
    assert run_play(pr, cat['SF'], cat['C'], 10 ** 4)['play'] == 'C'
    assert run_play(pr, cat['SF'], cat['D'], 10 ** 4)['play'] == 'D'


def test_fairbot_copy_threshold_and_witness():
    for b, want in [(6, False), (7, False), (8, True), (12, True)]:
        cat = catalogue(b); register_names(cat)
        pr = Prover(); th = pr.th
        A = th.plays(cat['FB'], cat['FB'], 'C')
        r = pr.query(A, b)
        assert r['found'] == want
        if want:
            assert r['size'] == 8
            w = pr.witness(A, b)
            assert wlambda(w) == 1 and wsize(w) == 8
            assert LC.replay(LC.convert(th, w)) == 8
        assert run_play(pr, cat['FB'], cat['FB'], 10 ** 4)['play'] == ('C' if want else 'D')


def test_fairbot_distinct_budgets_min_rule():
    for x, y, want in [(8, 16, False), (11, 16, False), (12, 16, True), (12, 12, True), (16, 32, True)]:
        pr = Prover()
        px, py = FB(x), FB(y)
        a = run_play(pr, px, py, 10 ** 5)['play']; b = run_play(pr, py, px, 10 ** 5)['play']
        assert a == b == ('C' if want or x == y else 'D'), (x, y, a, b)


def test_goedel_suckered_and_sloppy_exploited():
    cat = catalogue(10); pr = Prover()
    assert run_play(pr, cat['FB'], cat['G'], 10 ** 5)['play'] == 'D'
    assert run_play(pr, cat['G'], cat['FB'], 10 ** 5)['play'] == 'C'
    assert run_play(pr, cat['G'], cat['SC'], 10 ** 5)['play'] == 'D'
    assert run_play(pr, cat['SC'], cat['G'], 10 ** 5)['play'] == 'C'


def test_soundness_and_brute_agree_small():
    cat = catalogue(8); register_names(cat)
    pr = Prover(); th = pr.th
    for x in ['FB', 'C', 'SC', 'G', 'D']:
        for y in ['FB', 'C', 'SC', 'G', 'D']:
            A = th.plays(cat[y], cat[x], 'C')
            r = pr.query(A, 8)
            br = LC.Brute(root=LC.ideep(th, A, {}))
            assert br.minsize(8) == r['size']
    nbox, nseq, bad = soundness_check(pr)
    assert nbox > 0 and bad == []


def test_jlob_disabled_control():
    cat = catalogue(12); pr = Prover(jlob=False)
    assert run_play(pr, cat['FB'], cat['FB'], 10 ** 4)['play'] == 'D'
    assert run_play(pr, cat['FB'], cat['C'], 10 ** 4)['play'] == 'C'
