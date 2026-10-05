"""GLS+Def prover (src/gl_proofs.py): anchors and the audit against the evaluator's box-fact tables.

    python3 -m pytest tests/test_gl_proofs.py -q
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import numpy as np
import gl_proofs as G

FB = 'BOX(THEM(ME))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'


def _pair(xs, ys):
    th = G.Theory(); x = th.prog(xs); y = th.prog(ys)
    o, g = G.prove_pair(th, x, y, oracle=G.Oracle(th))
    return {k: (o[k]['c'] if o[k] else None) for k in ('C0', 'D0', 'C1', 'D1')}


def test_anchors():
    assert _pair('C', 'D')['C0'] == (2, 0)
    assert _pair('D', 'C')['D0'] == (2, 0)
    r = _pair(FB, FB)
    assert r['C0'] == (4, 1) and r['D0'] is None
    r = _pair(FB, 'D')                      # FairBot's defection on D needs Con(PA)
    assert r['C0'] is None and r['D0'] is None and r['D1'] is not None
    r = _pair(PB, PB)
    assert r['C0'] == (24, 5)
    r = _pair('and(BOX1(THEM(ME)),not(BOX(THEM(ME))))', 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))')   # P*: true, not PA-provable
    assert r['C0'] is None and r['D0'] is None and r['C1'] is not None


def test_oracle_matches_full_graph_n6():
    L, val, hc, hd = G.box_tables(6)
    th = G.Theory(); pid = [th.prog(s) for s in L.rep]; orc = G.Oracle(th)
    rng = np.random.default_rng(1)
    K = len(L.rep)
    for _ in range(300):
        c, d = rng.integers(K, size=2)
        o1, _ = G.prove_pair(th, pid[c], pid[d], oracle=orc)
        o2, _ = G.prove_pair(th, pid[c], pid[d])
        assert o2['complete']
        for k in ('C0', 'D0', 'C1', 'D1'):
            assert (o1[k] and o1[k]['c']) == (o2[k] and o2[k]['c'])


def test_audit_n6_every_pair():
    """hc[0] <=> |- P, hd[0] <=> P |- , hc[1] <=> |- ~[]F -> P, hd[1] <=> |- ~[]F -> ~P, on all 4,356 pairs."""
    L, val, hc, hd = G.box_tables(6)
    th = G.Theory(); pid = [th.prog(s) for s in L.rep]; orc = G.Oracle(th)
    K = len(L.rep)
    neither0 = 0
    for c in range(K):
        for d in range(K):
            o, bad = G.audit_pair(th, pid, c, d, val, hc, hd, oracle=orc)
            assert bad == [], (L.rep[c], L.rep[d], bad)
            neither0 += (o['C0'] is None and o['D0'] is None)
    assert neither0 > 0          # the trichotomy is non-empty at level 0


def test_soundness_truth_vs_proofs_n6():
    """A provable C (D) is a true C (D) at the stable world."""
    L, val, hc, hd = G.box_tables(6)
    assert not (hc[0] & (val == 0)).any() and not (hd[0] & (val == 1)).any()


def test_iterative_deepening_matches_knuth_n6():
    """MinSearch (iterative deepening with lower bounds, normal form, oracle pruning) gives the same certified
    (size, Loeb) as Knuth's algorithm on the all-orders graph, on every n = 6 root."""
    L, val, hc, hd = G.box_tables(6)
    th = G.Theory(); pid = [th.prog(s) for s in L.rep]; orc = G.Oracle(th); ms = G.MinSearch(th, orc)
    K = len(L.rep)
    for c in range(K):
        for d in range(K):
            o, _ = G.prove_pair(th, pid[c], pid[d])
            assert o['complete']
            for nm, S in G.roots_for(th, pid[c], pid[d]):
                r = ms.minimize(S)
                assert (r and r['c']) == (o[nm] and o[nm]['c'])
                assert r is None or (r['certified'] and ms.stats(S)['size'] == r['c'][0])
