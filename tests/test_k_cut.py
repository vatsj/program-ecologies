"""K with cut and distribution (src/bounded_k.py option `cut`; src/k_cut.py; notes/k-cut.md §1).  Regression tests;
the soundness proof is notes/k-cut.md §1.5 and the certificate's validity is Theorem E (§1.7).

    python3 -m pytest tests/test_k_cut.py -q
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import numpy as np
import bounded_k as BK
import gl_proofs as G
import k_cut as KC
import k_four as K4
from gl_proofs import FP, FBOT, FTOP, FNOT, FAND, FOR, FIMP, FBOX

FB = 'BOX(THEM(ME))'
INF = BK.INF


def _imp(K, a, b): return K.f((FIMP, a, b))
def _and(K, a, b): return K.f((FAND, a, b))


def _dist_goal(K, a, c, d):
    """[]_a A & []_c (A -> B) -> []_d B with A = P[FB@5, D], B = P[D, D] (notes §1.8)."""
    fb = K.geno(FB, 5); dd = K.geno('D', 0)
    A = K.P(fb, dd); B = K.P(dd, dd)
    return _imp(K, _and(K, K.box(A, a), K.box(_imp(K, A, B), c)), K.box(B, d))


def test_distribution_positive_negative():
    """d* = a + c + 5 exactly (size 6: ->R, &L, Dist over the 3-sequent premise); K never; Dist_1 impossible."""
    for cut in ('c', 'c4'):
        K = KC.KTheoryC(cap=40, cut=cut)
        goals = {(a, c, d): _dist_goal(K, a, c, d) for a in (2, 3, 5) for c in (2, 4) for d in range(a + c + 1, a + c + 8)}
        K.solve(sorted(goals.values()))
        for (a, c, d), g in goals.items():
            if d >= a + c + 5:
                assert K.T.get(g, INF) == 6, (cut, a, c, d, K.T.get(g))
                s, st = KC.check_goal(K, g)
                assert s == 6 and st['dist'] == 1
            else:
                assert K.T.get(g, INF) >= INF, (cut, a, c, d)
        n, bad = K.soundness_check(); assert not bad
    K0 = KC.KTheoryC(cap=40, cut=None)
    goals = [_dist_goal(K0, 2, 3, d) for d in range(5, 30)]
    K0.solve(goals)
    assert all(K0.T.get(g, INF) >= INF for g in goals)


def test_theorem_d0_extension_model():
    """Theorem D0: in the extension model with E = {(P[C,C] -> F, c)} closed under BoxEq/4m only (K + Cut has no
    other box-left rule), []_a P[C,C] and []_c (P[C,C] -> F) are true and []_d F is false, for every d."""
    K = KC.KTheoryC(cap=20, cut='c')
    cc = K.geno('C', 0); A = K.P(cc, cc); AF = _imp(K, A, K.BOT)
    K.solve([A]); assert K.T[A] == 2                    # UnfR, then |- T
    E = {AF}
    def member(Y, e, c=3):
        if K.T.get(Y, INF) <= e: return True            # Std
        return e >= c and Y in E                        # BoxEq images of A -> F: only itself (not a constant)
    for d in range(1, 60):
        assert member(A, 2) and member(AF, 3) and not member(K.BOT, d)


def test_K_derivations_remain_Kc():
    """Every K derivation is a K_c derivation of the same size, and K_c's minimal sizes never exceed K's."""
    import k_at_n8 as KN
    L, vf, hc, hd = KN.tables(6)
    tabs = {}
    for cut in (None, 'c'):
        K = KC.KTheoryC(cap=16, filter_first=True, cut=cut)
        K.prune = KN.make_prune(K, L, hc, hd)
        g = [K.geno(s, 16) for s in L.rep[:60]]
        cont = sorted({K.forms[a][1] for x in g for y in g for a in K.atoms(x, y)})
        K.solve(cont)
        tabs[cut] = (K, cont)
    K0, c0 = tabs[None]; K1, c1 = tabs['c']
    shows0 = {K0.show(a): K0.T.get(a, INF) for a in c0}
    shows1 = {K1.show(a): K1.T.get(a, INF) for a in c1}
    for k, v in shows0.items():
        assert shows1[k] <= v
    # K's extracted derivations pass the K_c checker unchanged
    K0.cut = 'c'
    for a in c0:
        if K0.T.get(a, INF) <= 16:
            K0.cut = None; d = KC.Extract(K0).closed(a); K0.cut = 'c'
            assert KC.Checker(K0).size(d) == K0.T[a]
    K0.cut = None


def test_certificates_named():
    """Corollary P at b = 16, 30: P*, P2, P12b, P*1b certified structural at g = 0 and g = 1 (with 4m in the closure);
    PB2 certified at g = 0, and at g = 1 only without 4m (consistent with the X-arm of 'K with the 4-rule')."""
    import k_at_n8 as KN
    for b in (16, 30):
        for goff in (0, 1):
            for four in (True, False):
                K = KC.KTheoryC(cap=b + goff, filter_first=True, cut='c', goff=goff)
                K.prune = KN.make_prune_trace(K, 60)
                progs = [KC.PSTAR, KC.P2, KC.P12B, KC.PS1B, KC.PB2]
                gs = {s: K.geno(s, b) for s in progs}
                cont = {s: [K.forms[a][1] for a in K.atoms(x, x)] for s, x in gs.items()}
                K.solve(sorted({c for cs in cont.values() for c in cs}))
                cert = KC.Certifier(K, b, four=four)
                for s, x in gs.items():
                    P = K.P(x, x)
                    play = K.play_fn()(x, x)
                    assert not play, (s, b, goff)
                    missing = [c for c in cont[s] if K.T.get(c, INF) > b and cert.gltrue(c)]
                    res = cert.run(missing)
                    if s == KC.PB2 and goff == 1 and four:
                        assert any(res[c] is None for c in missing)
                    else:
                        assert missing and all(res[c] is not None for c in missing), (s, b, goff, four)


def test_n6_table_checker_and_prune():
    """n = 6, b = 16: the K_c table equals K's; every derived content passes the independent checker with its search
    size; every Dist premise and every sequent of every extracted derivation erases to a GL-valid sequent (the prune
    is valid on derivations containing cut); some Lemma C witnesses are replayed."""
    val, meta, K, g = KC.ktable_c(6, 16, 'c', check=True)
    ref = np.load(os.path.join(KC.K4DIR, 'K_g0_n6_b16.npy')) if os.path.exists(os.path.join(KC.K4DIR, 'K_g0_n6_b16.npy')) else KC.ktable_c(6, 16, None)[0]
    assert (val == ref).all()
    assert meta['sound_bad'] == 0 and meta['checker']['size_mismatch'] == 0 and meta['checker']['replayed'] > 0
    assert meta['uncertified_contents'] == 0
    th = G.Theory(); orc = G.Oracle(th); em = {}
    def walk(n):
        S = (frozenset(K4.erase(K, a, th, em) for a in n['L']), frozenset(K4.erase(K, a, th, em) for a in n['R']))
        assert orc.prov(S)
        for k in n['kids']: walk(k)
        for _, _, d in n.get('lemmas', ()): walk(d)
    ex = KC.Extract(K); nd = 0
    for c in sorted(K.T):
        if K.T[c] <= 16 and nd < 150:
            walk(ex.closed(c)); nd += 1
    assert nd > 50
