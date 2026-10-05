"""Unit tests for the union game (specs/2026-10-05-union.md).

    python3 tests/test_union.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import union as U
import union_abm as A
from union_chain import log_rho

d = U.build()
P = d['P']
nm = U.named(P)
nb = U.named_boss(P)
flag = np.ones((2, U.NPROP), np.bool_)


def enc(b, x, y):
    return U.encounter(*P.arrays(), U.TT, b, x, y, flag)


def act(j):
    return (j // 2) % 2, j % 2


def test_quorum_semantics():
    un, sc, mi, up = nm['union'], nm['scab'], nm['militant'], nm["union' (BOX(OTHER=strike))"]
    for si in range(3):
        for hi in range(3):
            b = nb[U.bname(U.bact(si, hi))]
            low = si < 2
            # two union programs resolve QUORUM mutually by Lob: both strike iff s < 1/2
            assert act(enc(b, un, un)) == ((1, 1) if low else (0, 0))
            # QUORUM is unprovable against a scab: the union works at any wage
            assert act(enc(b, un, sc)) == (0, 0) and act(enc(b, sc, un)) == (0, 0)
            # a militant provably strikes whenever s < 1/2, so the union joins it
            assert act(enc(b, un, mi)) == ((1, 1) if low else (0, 0))
            assert act(enc(b, mi, sc)) == ((1, 0) if low else (0, 0))
            # union' (BOX(OTHER = strike) in place of QUORUM) plays like the union
            assert act(enc(b, up, up)) == act(enc(b, un, un))
    assert P.tag[un] and not P.tag[up] and not P.tag[mi] and not P.tag[sc]


def test_union_equals_union_prime_everywhere():
    J = U.tensor(*P.arrays(), U.TT, P.KB, P.KW)
    un, up = nm['union'], nm["union' (BOX(OTHER=strike))"]
    assert (J[:, un, :] == J[:, up, :]).all() and (J[:, :, un] == J[:, :, up]).all()


def test_worker_symmetry():
    """J[b, y, x] = swap(J[sigma b, x, y]), sigma relabels W1 <-> W2 in the boss's atoms."""
    J = U.tensor(*P.arrays(), U.TT, P.KB, P.KW)
    SW = np.array([(j // 4) * 4 + (j % 2) * 2 + (j // 2) % 2 for j in range(36)], np.int8)
    perm = {0: 2, 1: 3, 2: 0, 3: 1}
    from dollar3 import Lang
    sig = np.empty(P.KB, np.int64)
    for b, (atoms, tab) in enumerate(P.fb):
        g = Lang._reduce([(L, perm[k]) for (L, k) in atoms], list(tab))
        sig[b] = P.index_b[g]
    assert (J.transpose(0, 2, 1) == SW[J[sig]]).all()


def test_frequency_independence_every_count(N=20):
    """A slot-s mutant's mean payoff, computed by the agent-based kernel in a
    population with k mutants (k = 1 .. N-1) and the other slots monomorphic,
    equals the pairwise payoff the chain uses, for every k; and so does the
    resident's.  Checked for every named triple, every named mutant and c."""
    C = U.classes(d)
    cw, cb = C['cw'], C['cb']
    W = [cw[nm[k]] for k in ('scab', 'militant', 'union', "union' (BOX(OTHER=strike))")]
    B = [cb[nb[U.bname(b)]] for b in range(U.NB)]
    for c in (0.0, 0.1, 0.5):
        PAY = U.payoff_table(c)
        for b in B:
            for x in W:
                for y in W:
                    res = [b, x, y]
                    r = PAY[C['Jc'][b, x, y], C['tagc'][x], C['tagc'][y]]
                    for s in range(3):
                        for q in (B if s == 0 else W):
                            if q == res[s]: continue
                            t = list(res); t[s] = q
                            u = PAY[C['Jc'][t[0], t[1], t[2]], C['tagc'][t[1]], C['tagc'][t[2]]]
                            tid = np.zeros((1, 3, A.TMAX), np.int64); cnt = np.zeros((1, 3, A.TMAX), np.int64)
                            for s2 in range(3):
                                tid[0, s2, 0] = res[s2]; cnt[0, s2, 0] = N
                            tid[0, s, 1] = q
                            for k in range(1, N):
                                cnt[0, s, 0] = N - k; cnt[0, s, 1] = k
                                um = A.slot_pay(C['Jc'], C['tagc'], PAY, tid, cnt, 0, s, q, N)
                                ur = A.slot_pay(C['Jc'], C['tagc'], PAY, tid, cnt, 0, s, res[s], N)
                                assert abs(um - u[s]) < 1e-12 and abs(ur - r[s]) < 1e-12


def test_log_rho():
    assert abs(np.exp(log_rho(0.0, 100.0)) - 0.01) < 1e-15
    r = np.exp(0.3 * 0.5)
    assert abs(np.exp(log_rho(0.15, 100.0)) - (1 - 1 / r) / (1 - r ** -100)) < 1e-12


if __name__ == '__main__':
    for k, v in list(globals().items()):
        if k.startswith('test_'):
            v(); print(k, 'ok')
