"""Phase 0/1 checks: hand cases against the reference evaluator, and exact
agreement between the batched evaluator and the reference at n <= 4."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from dsl import Language
from game import Game
from evaluate import Tape, close_pairs, pair_keys, unkey, square
from reference import Reference

PD = os.path.join(os.path.dirname(__file__), '..', 'games', 'pd.yaml')


def test_hand_cases():
    L = Language('weak', 4)
    R = Reference(L)
    v = lambda a, b: R.value(L.parse(a), L.parse(b), 0, 60)
    assert v('C', 'C') == (1, 0, 0)
    assert v('D', 'D') == (0, 1, 0)
    assert v('X', 'X') == (0.5, 0.5, 0)
    c, d, f = v('or(X,THEM(ME))', 'or(X,THEM(ME))')
    assert abs(c - 1) < 1e-12 and f < 1e-12
    assert v('THEM(ME)', 'THEM(ME)') == (0, 0, 1)                  # divergent
    assert v('THEM(ME)', 'not(THEM(ME))') == (0, 0, 1)             # match vs swap
    assert v('or(THEM(ME),X)', 'or(THEM(ME),X)') == (0, 0, 1)      # no short-circuit grounding
    c, d, f = v('and(X,THEM(ME))', 'and(X,THEM(ME))')
    assert abs(d - 1) < 1e-12
    assert v('or(and(X,X),THEM(ME))', 'D')[0] == 0.25


def test_batched_matches_reference():
    g = Game.load(PD)
    for arm, role in [('strong', False), ('weak', False), ('source', False), ('source', True)]:
        L = Language(arm, 4, role=role)
        ids = L.ids()
        keys = close_pairs(L, pair_keys(L, ids, ids, role), role)
        tape = Tape(L, keys, role)
        R = Reference(L, role=role)
        i, j, r = unkey(L.count, keys)
        for b in range(0, 8):
            Vc, Vf, bud, d = tape.iterate(tol=-1, bmax=b)
            assert bud == b
            ref = np.array([R.value(int(a), int(bb), int(rr), b) for a, bb, rr in zip(i, j, r)])
            assert np.abs(ref[:, 0] - Vc).max() == 0.0
            assert np.abs(ref[:, 2] - Vf).max() == 0.0


def test_square_converges():
    g = Game.load(PD)
    L = Language('strong', 5)
    res = square(L, g)
    assert res.delta < 1e-10
    fb = L.parse('or(X,THEM(ME))')
    assert abs(res.V[res.index(fb, fb)] - 1) < 1e-9
    assert res.div[res.index(L.parse('THEM(ME)'), L.parse('THEM(ME)'))]
