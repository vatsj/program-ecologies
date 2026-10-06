"""The guard margin as a heritable trait (src/guard_trait.py).  Fast regression tests of the mixed-guard semantics,
the high-budget certificate rule and the kernels.

    python3 -m pytest tests/test_guard_trait.py -q
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import numpy as np
import guard_trait as GT
from gl_proofs import FBOX, FIMP, FNOT

PSTAR = 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'


def test_semantics_collapse_and_guard_budget():
    K = GT.KTheoryM(cap=40, glong=24)
    fb0 = K.geno('BOX(THEM(ME))', 16, 0); fb1 = K.geno('BOX(THEM(ME))', 16, 1)
    assert fb0 == fb1                                       # guard-free: one program
    r0 = K.geno('BOX1(THEM(ME))', 16, 0); r1 = K.geno('BOX1(THEM(ME))', 16, 1)
    assert r0 != r1 and K.gg[r1] == 1
    q0 = K.geno('BOX(THEM(^BOX1(THEM(ME))))', 16, 0); q1 = K.geno('BOX(THEM(^BOX1(THEM(ME))))', 16, 1)
    assert q0 != q1                                         # guarded quote: the quoter's guard matters
    # the g = L reader's level-1 atom reads ~[]_40 F; the g = 0 reader's ~[]_16 F
    for g, want in ((r0, 16), (r1, 40)):
        (a,) = K.atoms(g, fb0)
        c = K.forms[a][1]; t = K.forms[c]
        assert t[0] == FIMP
        neg = K.forms[t[1]]; bx = K.forms[neg[1]]
        assert bx[0] == FBOX and bx[2] == want
    # quoted argument inherits the quoter's guard
    (a,) = K.atoms(q1, fb0)
    P = K.forms[K.forms[a][1]]
    assert K.gg[P[2]] == 1


def test_high_budget_rule_pstar():
    """P*'s self-play content is certified structural at g = 0 (Corollary P) and not at g = L, where the
    high-budget rule finds GL |- (P & []P) -> F (Dist+ can reach []_{2b+8} F)."""
    import k_at_n8 as KN
    for g, certified in ((0, True), (1, False)):
        K = GT.KTheoryM(cap=40, glong=24, filter_first=True)
        K.prune = KN.make_prune_trace(K, 60)
        x = K.geno(PSTAR, 16, g)
        cs = [K.forms[a][1] for a in K.atoms(x, x)]
        K.solve(cs)
        cert = GT.CertifierM(K, 16)
        res = cert.run([c for c in cs if K.T.get(c, GT.INF) > 16 and K.prune(c)])
        lvl1 = [c for c in res if K.forms[c][0] == FIMP]
        assert lvl1
        assert all((res[c] is not None) == certified for c in lvl1), (g, res)


def test_sham_joint_allocation_is_prior():
    import k_at_n8 as KN
    L = KN.tables(6)[0]
    nr = len(L.rep)
    rng = np.random.default_rng(1)
    v0 = (rng.random((nr, nr)) < 0.3).astype(np.int8)
    iD = L.rep.index('D'); iC = L.rep.index('C')
    v0[iD, :] = 0; v0[iC, :] = 1
    cat = [(c, g) for g in (0, 1) for c in range(nr)]
    idx = np.array([c for c, g in cat])
    C = GT.Cat(v0[np.ix_(idx, idx)], cat, L, (0.7, 0.3))
    assert C.twins()[nr:].all()
    r = GT.run_chain(C, 'joint', 200, lazy=False, rates=False)
    assert abs(r['allocation_twins'] - 0.3) < 1e-9
    blocks, blk = GT.lump(C, 'separate')
    assert all(len({C.lab[i] for i in b}) == 1 for b in blocks)
