"""K with the 4-rule (src/bounded_k.py option `four`; notes/k-four.md §1) and the frozen classifier
(src/k_four.py).  Regression tests: the soundness proof is notes/k-four.md §1.4.

    python3 -m pytest tests/test_k_four.py -q
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import numpy as np
import bounded_k as BK
import k_four as K4
from gl_proofs import FP, FBOT, FTOP, FNOT, FAND, FOR, FIMP, FBOX

FB = 'BOX(THEM(ME))'
PB = 'and(BOX(THEM(ME)),BOXD1(THEM(^D)))'
G1 = 'not(BOX(THEM(ME)))'


def _imp(K, a, b): return K.f((FIMP, a, b))


def test_nested_box_case_table():
    """|- []_a A -> []_c []_d A for A = P[FB@5, FB@5]: the literal rule fires iff d == a and c >= a + 1, 4m iff
    d >= a and c >= a + 1; whatever the search derives is true (closure checker)."""
    for four in ('lit', 'mono'):
        K = K4.KTheoryG(cap=8, four=four)
        x = K.geno(FB, 5); P = K.P(x, x)
        goals = {}
        for a in range(1, 5):
            for c in range(1, 7):
                for d in range(1, 7):
                    goals[(a, c, d)] = _imp(K, K.box(P, a), K.box(K.box(P, d), c))
        K.solve(sorted(goals.values()))
        for (a, c, d), f in goals.items():
            fires = (d == a and c >= a + 1) if four == 'lit' else (d >= a and c >= a + 1)
            if fires:
                assert K.T.get(f, BK.INF) == 2, (four, a, c, d)      # ->R then the 4-rule leaf
        n, bad = K4.closure_check(K)
        assert not bad


def test_cross_budget_boundaries_unfolding():
    """4m (ii)-(iv) at their boundaries: [](P[D,y], a) |- [](([](F, d)), c) needs d >= a, c >= a + 1."""
    K = K4.KTheoryG(cap=12, four='mono')
    d0 = K.geno('D', 0); y = K.geno(FB, 4)
    PD = K.P(d0, y)                          # phi(PD) = F
    for a in (2, 3, 4):
        for d in (a - 1, a, a + 1):
            for c in (a, a + 1, a + 2):
                f = _imp(K, K.box(PD, a), K.box(K.box(K.BOT, d), c))
                K.solve([f])
                ok = K.T.get(f, BK.INF) <= 12
                if d >= a and c >= a + 1:
                    assert ok, (a, c, d)
    n, bad = K4.closure_check(K)
    assert not bad
    # without the rule, K cannot derive the same sequent at any boundary (no rule acts under a box)
    K0 = K4.KTheoryG(cap=12, four=None)
    d0 = K0.geno('D', 0); y = K0.geno(FB, 4)
    f = _imp(K0, K0.box(K0.P(d0, y), 3), K0.box(K0.box(K0.BOT, 3), 4))
    K0.solve([f])
    assert K0.T.get(f, BK.INF) > 12


def test_generated_formulas_sound():
    """Random formulas outside the catalogue (budgets 2-8, box depth <= 3) under K+4m: every derived closed formula
    is true in the model (closure checker), and K+4m derives everything K derives."""
    rng = np.random.default_rng(20261005)
    progs = [FB, PB, G1, 'C', 'D']
    for trial in range(3):
        K = K4.KTheoryG(cap=10, four='mono'); K0 = K4.KTheoryG(cap=10, four=None)

        def gen(KK, depth, r):
            u = r.random()
            if depth == 0 or u < 0.3:
                x = KK.geno(progs[r.integers(len(progs))], int(r.integers(2, 9)))
                y = KK.geno(progs[r.integers(len(progs))], int(r.integers(2, 9)))
                return KK.P(x, y)
            if u < 0.55:
                return KK.box(gen(KK, depth - 1, r), int(r.integers(2, 9)))
            if u < 0.7:
                return KK.neg(gen(KK, depth - 1, r))
            k = (FAND, FOR, FIMP)[int(r.integers(3))]
            return KK.f((k, gen(KK, depth - 1, r), gen(KK, depth - 1, r)))
        fs, fs0 = [], []
        for i in range(30):
            seed = int(rng.integers(1 << 30))
            fs.append(gen(K, 3, np.random.default_rng(seed))); fs0.append(gen(K0, 3, np.random.default_rng(seed)))
        K.solve(fs); K0.solve(fs0)
        for f, f0 in zip(fs, fs0):
            if K0.T.get(f0, BK.INF) <= 10:
                assert K.T.get(f, BK.INF) <= K0.T[f0]
        n, bad = K4.closure_check(K)
        assert not bad, [K.show(b) for b in bad]


def test_literal_rule_vacuous_on_family():
    """Lemma V: on DSL programs the literal rule never fires, so K+4 = K on a named family with level-2 guards."""
    import k_at_n8 as KN
    fam = [FB, PB, K4.PB2, K4.PSTAR, K4.P2, 'BOX1(THEM(ME))', G1, 'C', 'D']
    for b in (6, 12):
        out = []
        for four in (None, 'lit'):
            K = K4.KTheoryG(cap=b, filter_first=True, four=four)
            K.prune = KN.make_prune_trace(K, 60)
            g = [K.geno(s, b) for s in fam]
            cont = {K.forms[a][1] for x in g for y in g for a in K.atoms(x, y)}
            K.solve(sorted(cont))
            play = K.play_fn()
            out.append(np.array([[play(x, y) for y in g] for x in g]))
        assert (out[0] == out[1]).all()


def test_classifier_anchors():
    C = K4.Classifier()
    r = C.classify_play(G1, 'BOX1(THEM(THEM))')
    assert r['play'] == 0 and r['flagG'] and r['certified']
    r = C.classify_play(FB, FB)
    assert r['play'] == 1 and not r['flag'] and r['size'] == 4
