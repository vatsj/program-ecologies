"""Unit tests for the enforcement evaluator (specs/2026-10-05-enforcement.md).

    python3 tests/test_union_enforcement.py
"""
import os, sys, json
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import union as U
import union_enforcement as E

base = E.make_base()
d, C, Bn, Bf, Wf, mB, mW = base
P = d['P']
TAG = P.tag.astype(np.int64)
nb = U.named_boss(P); nw = U.named(P)
flag = np.ones((2, U.NPROP), np.bool_)


def enc(b, x, y, arm='CC', pool=0, c=0.5, tie='whack'):
    rb, rw = E.ARMS[arm]
    return E.encounter_e(*P.arrays(), U.TT, b, x, y, flag, TAG, rb, rw, pool, c, E.TIES[tie])


def B(s, h):
    return nb[U.bname(U.bact(s, h))]


def test_cc_tensor_equals_union():
    J0 = U.tensor(*P.arrays(), U.TT, P.KB, P.KW)
    for pool in (0, 1):
        J1 = E.tensor_e(*P.arrays(), U.TT, P.KB, P.KW, TAG, 0, 0, pool, 0.5, 0)
        assert (J0 == J1).all()


def test_cc_reproduces_union_static_tables():
    """(CC, no pool) reproduces runs/union/static.json exactly: every named triple's
    play, payoffs and every move's payoff change, and the reduced chains' summaries."""
    ref = json.load(open(os.path.join(ROOT, 'runs', 'union', 'static.json')))
    for c in (0.0, 0.1, 0.5):
        rows = E.reduced_static(base, 'CC', 0, c, 'whack')
        rr = ref['c=%g' % c]
        assert len(rows) == len(rr)
        for a, b in zip(rows, rr):
            assert (a['boss'], a['W1'], a['W2'], a['play'], a['summary']) == (b['boss'], b['W1'], b['W2'], b['play'], b['summary'])
            assert np.allclose(a['pay'], b['pay'])
            assert [(m['slot'], m['mutant'], m['to']) for m in a['moves']] == [(m['slot'], m['mutant'], m['to']) for m in b['moves']]
            assert np.allclose([m['du'] for m in a['moves']], [m['du'] for m in b['moves']], atol=1e-12)
        for prior, key in (('uniform', 'uniform'), ('mu', 'mu')):
            for N in (100, 1000, 10000):
                cell = E.reduced_cell(base, 'CC', 0, c, 'whack', prior, N)
                want = ref['reduced_c=%g' % c]['%s_N%d' % (key, N)]['summary']
                for k, v in want.items():
                    assert abs(cell['summary'][k] - v) <= 1e-9 * max(1.0, abs(v)) + 1e-15, (c, prior, N, k, cell['summary'][k], v)


def test_tie_breaking_workers():
    """Rational workers: indifference resolves to the recommendation."""
    sc, mi, un = nw['scab'], nw['militant'], nw['union']
    act = lambda j: ((j // 2) % 2, j % 2)
    for arm in ('CR', 'RR'):
        # s = 0, no whacking: strike and work both give 0 -> recommendation
        assert act(enc(B(0, 1), mi, mi, arm, 0)) == (1, 1)
        assert act(enc(B(0, 1), sc, sc, arm, 0)) == (0, 0)
        assert act(enc(B(0, 1), un, un, arm, 0)) == (1, 1)
        assert act(enc(B(0, 1), mi, sc, arm, 0)) == (1, 0)
        # s = 1/4: work strictly better -> work even for a committed striker's recommendation
        assert act(enc(B(1, 1), mi, mi, arm, 0)) == (0, 0)
    # CR, committed strike targeting at s = 0: striking gives -L < 0 -> work
    assert act(enc(B(0, 0), mi, mi, 'CR', 0)) == (0, 0)
    # CR, committed source targeting, tagged union at s = 0: whacked either way -> tie -> recommendation (strike)
    assert act(enc(B(0, 2), un, un, 'CR', 0)) == (1, 1)
    # ... and at s = 1/4: work gives 1/4 - 1 > -1 -> work
    assert act(enc(B(1, 2), un, un, 'CR', 0)) == (0, 0)


def test_rational_boss_and_boundary():
    """Rational boss: whack a striker iff (1 - s) - c > 0 with the pool, never without;
    the boundary 1 - s = c is resolved by the declared tie rule."""
    always = P.index_w[((), (1,))]
    h_of = lambda j: (j // 4) % 3
    for si in range(3):
        for hi in range(3):
            b = B(si, hi)
            for c in (0.1, 0.5):
                assert h_of(enc(b, always, always, 'RC', 0, c)) == 1            # no pool: never whack
                g = 1 - 0.25 * si - c
                for tie in ('whack', 'nowhack'):
                    want = 0 if g > 1e-12 else (1 if g < -1e-12 else (0 if tie == 'whack' else 1))
                    assert h_of(enc(b, always, always, 'RC', 1, c, tie)) == want, (si, hi, c, tie)
    # the boundary case itself: s = 1/2, c = 1/2, with the pool
    assert h_of(enc(B(2, 1), always, always, 'RC', 1, 0.5, 'whack')) == 0
    assert h_of(enc(B(2, 1), always, always, 'RC', 1, 0.5, 'nowhack')) == 1
    PAY, REP = E.payoff_table_e(0.5, 1)
    j_wh = 4 * U.bact(2, 0) + 3; j_no = 4 * U.bact(2, 1) + 3
    assert abs(PAY[j_wh, 0, 0, 0] - PAY[j_no, 0, 0, 0]) < 1e-12          # exact indifference
    # a rational boss never whacks a working tagged worker, even under a source-targeting recommendation
    un = nw['union']
    assert h_of(enc(B(2, 2), un, un, 'RC', 1, 0.1)) == 0 and enc(B(2, 2), un, un, 'RC', 1, 0.1) % 4 == 0


def test_pool_payoffs():
    PAY, REP = E.payoff_table_e(0.5, 1)
    j = 4 * U.bact(0, 0) + 2 * 1 + 0          # (0, strike), W1 strikes, W2 works
    assert np.allclose(PAY[j, 0, 0], (1 + (1 - 0.5), -1, 0)) and REP[j, 0, 0] == 1
    PAY0, _ = E.payoff_table_e(0.5, 0)
    assert np.allclose(PAY0, U.payoff_table(0.5))


def test_box_audit():
    """0 violations: every boss function x every named-worker pair, in every arm, pool,
    c and tie rule, plus a random sample of the full language."""
    rng = np.random.default_rng(0)
    named = [nw[k] for k in ('scab', 'militant', 'union', 'always strike')]
    nv = 0; ntot = 0
    for arm, (rb, rw) in E.ARMS.items():
        for pool in (0, 1):
            for c in (0.1, 0.5):
                for tie in ('whack', 'nowhack'):
                    cases = [(b, x, y) for b in range(P.KB) for x in named for y in named]
                    cases += [(int(rng.integers(P.KB)), int(rng.integers(P.KW)), int(rng.integers(P.KW))) for _ in range(150)]
                    for (b, x, y) in cases:
                        j = enc(b, x, y, arm, pool, c, tie)
                        v = E.audit_one(P, b, x, y, j, rb, rw, pool, c, E.TIES[tie])
                        ntot += 1
                        if v:
                            nv += 1
                            print(arm, pool, c, tie, b, x, y, v)
    print('box audit: %d encounters, %d violations' % (ntot, nv))
    assert nv == 0


if __name__ == '__main__':
    for name, f in list(globals().items()):
        if name.startswith('test_'):
            f(); print('ok', name)
