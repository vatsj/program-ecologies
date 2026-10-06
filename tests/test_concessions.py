"""Unit tests for the concessions evaluator (specs/2026-10-06-concessions.md).

    python3 tests/test_concessions.py
"""
import os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import union as U
import union_enforcement as E
import concessions as K

W = K.worker_lang(); P = W['P']
TAG = P.tag.astype(np.int64)
RNG = np.random.default_rng(3)
NW = K.named_workers()


def _pairs(n=400):
    xs = list(NW.values())
    PX = [x for x in xs for y in xs] + list(RNG.integers(0, P.KW, n))
    PY = [y for x in xs for y in xs] + list(RNG.integers(0, P.KW, n))
    return np.array(PX, np.int64), np.array(PY, np.int64)


def test_probe_free_equals_union_evaluators():
    """For probe-free bosses the new evaluator equals union.encounter (CC) and union_enforcement.encounter_e (RR)."""
    d = U.build()
    PU = d['P']
    BA = K.BossArrays(PU.fb)
    PX, PY = _pairs()
    flag = np.ones((2, U.NPROP), np.bool_)
    for enf, pool, c in (('CC', 0, 0.5), ('RR', 0, 0.5), ('RR', 1, 0.1), ('CC', 1, 0.1)):
        rb, rw = K.ENF[enf]
        CF = K.cf_for(enf, pool, c)
        J = K.pairs_c(*BA.arrays(), P.nat, P.atP, P.atL, P.tab, U.TT, 0, PU.KB, PX, PY, CF['FV'], TAG, rb, rw, pool, c, 0)
        for b in range(PU.KB):
            for p in range(len(PX)):
                ref = E.encounter_e(*PU.arrays(), U.TT, b, PX[p], PY[p], flag, TAG, rb, rw, pool, c, 0)
                assert J[b, p] == ref, (enf, pool, b, PX[p], PY[p], J[b, p], ref)


def _named_lang():
    nb = K.named_bosses('P01')
    fams = K.dstar_family()
    fl = list(nb.values()) + list(fams.values())
    # every one- and two-probe function over a few atoms, for coverage
    for k in range(4, 12):
        for L in (0, 1):
            a = (L, k)
            fl.append(K.bfn([a], lambda tv, a=a: U.bact(2, 1) if tv[a] else U.bact(0, 0)))
    return K.BossArrays(fl)


def test_box_audit_and_lemma0():
    """Independent history-based trace: the stable play equals the flag evaluator's; box atoms are monotone;
    Lemma 0 at the stable world for base boxes and probes (a true probe's proposition holds in the quoted
    encounter's stable executed play)."""
    BA = _named_lang()
    PX, PY = _pairs(200)
    for enf, pool, c in (('CC', 0, 0.5), ('RR', 0, 0.5)):
        rb, rw = K.ENF[enf]
        CF = K.cf_for(enf, pool, c)
        J = K.pairs_c(*BA.arrays(), P.nat, P.atP, P.atL, P.tab, U.TT, 0, len(BA.nat), PX, PY, CF['FV'], TAG, rb, rw, pool, c, 0)
        for b in range(len(BA.nat)):
            for p in range(0, len(PX), 3):
                x, y = PX[p], PY[p]
                tr = K.trace_c(BA, P, CF['FV'], b, x, y, rb, rw, pool, c, 0, K=12)
                js = [w['imp'] for w in tr]
                assert js[-1] == J[b, p] and js[-2] == js[-1], (b, x, y, js, J[b, p])
                for t in range(BA.nat[b]):
                    seq = [w['boss_atoms'][t] for w in tr]
                    assert not any((not seq[m]) and seq[m + 1] for m in range(len(seq) - 1))
                    k = int(BA.atK[b, t])
                    if seq[-1]:
                        if k < 4:
                            assert U.TT[12 + k, js[-1]]
                        else:
                            pk = k - 4; q, i, a = pk // 4, (pk // 2) % 2, pk % 2
                            assert CF['EXS'][x, y, q, i] == a


def test_slot_symmetry():
    """J[b, x, y] = swap(J[sigma b, y, x]) with sigma exchanging W1 and W2 in the boss's atoms."""
    BA = _named_lang()
    swapk = lambda k: (k ^ 2) if k < 4 else 4 + (((k - 4) ^ 2))
    fl2 = []
    for (atoms, tab) in BA.fb:
        m = {a: (a[0], swapk(a[1])) for a in atoms}
        fl2.append(K.bfn([m[a] for a in atoms], lambda tv, atoms=atoms, tab=tab, m=m: tab[sum(1 << t for t, a in enumerate(atoms) if tv[m[a]])]))
    BA2 = K.BossArrays(fl2)
    PX, PY = _pairs(200)
    CF = K.cf_for('CC', 0, 0.5)
    J1 = K.pairs_c(*BA.arrays(), P.nat, P.atP, P.atL, P.tab, U.TT, 0, len(BA.nat), PX, PY, CF['FV'], TAG, 0, 0, 0, 0.5, 0)
    J2 = K.pairs_c(*BA2.arrays(), P.nat, P.atP, P.atL, P.tab, U.TT, 0, len(BA2.nat), PY, PX, CF['FV'], TAG, 0, 0, 0, 0.5, 0)
    sw = lambda j: 4 * (j // 4) + 2 * (j % 2) + (j // 2) % 2
    for b in range(len(BA.nat)):
        for p in range(len(PX)):
            assert J1[b, p] == sw(int(J2[b, p]))


def test_named_plays():
    """The spec's hand analysis, by the evaluator (CC): D0 pays 1/2 to T0 and T1 pairs; D0q pays T0 1/4 (work)
    and is struck by T1; D* pays T0 1/4 and T1 1/2."""
    nb = K.named_bosses('P01')
    names = list(nb)
    BA = K.BossArrays([nb[k] for k in names])
    CF = K.cf_for('CC', 0, 0.5)
    t0 = NW['T0 (strike iff s = 0)']; t1 = NW['T1 = militant (strike iff s <= 1/4)']
    J = K.tensor_c(*BA.arrays(), P.nat, P.atP, P.atL, P.tab, U.TT, np.arange(len(names)), np.array([t0, t1]),
                   np.array([t0, t1]), CF['FV'], TAG, 0, 0, 0, 0.5, 0)
    g = lambda pre: [i for i, n in enumerate(names) if n.startswith(pre)][0]
    assert U.joint_name(int(J[g('D0 ='), 0, 0])) == '(1/2,none) W W'
    assert U.joint_name(int(J[g('D0 ='), 1, 1])) == '(1/2,none) W W'
    assert U.joint_name(int(J[g('D0q'), 0, 0])) == '(1/4,none) W W'
    assert U.joint_name(int(J[g('D0q'), 1, 1])) == '(1/4,none) S S'
    assert U.joint_name(int(J[g('D* ='), 0, 0])) == '(1/4,none) W W'
    assert U.joint_name(int(J[g('D* ='), 1, 1])) == '(1/2,none) W W'


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn(); print(name, 'ok', flush=True)
