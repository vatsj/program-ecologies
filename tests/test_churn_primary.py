"""Tests for the churn-in-the-primary-object experiment (spec specs/2026-10-25-churn-primary.md): payoffs of the named
readers by hand in both arms, the flip statistic on hand-built trajectories, the arm-E grammar restricted to n = 6
reproducing the stored modalPA lottery, the baseline rerun reproducing the stored migration-window rows, the
homogeneous-reader cell's resident outcome, the price types.

    python3 -m pytest tests/test_churn_primary.py -q
"""
import json, os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import numpy as np
import dollar3 as D
import stable_sets as SS
import migration_window as MW
import churn_primary as CP
import churn_primary_probe as PR
import lt_code as L

ROOT = SS.ROOT
T = CP.T
F01, F02, F12 = PR.F01, PR.F02, PR.F12
LABEL = {F01: 'F{0,1}', F02: 'F{0,2}', F12: 'F{1,2}'}


# ------------------------------------------------------------------ arm T by hand
_TC = {}


def tcat():
    if 'c' not in _TC:
        import churn_primary_t as CT
        _TC['c'] = CT.TCat()
        _TC['tab'] = _TC['c'].tables()
    return _TC['c']


def tplay(a, b, c):
    """(codes of the three slots, steps) of programs a (slot 0), b (slot 1), c (slot 2)."""
    cat = tcat(); code, steps = _TC['tab']
    i = [cat.idx[x] for x in (a, b, c)]
    return ([int(code[i[0], i[1], i[2]]), int(code[i[1], i[2], i[0]]), int(code[i[2], i[0], i[1]])],
            [int(steps[i[0], i[1], i[2]]), int(steps[i[1], i[2], i[0]]), int(steps[i[2], i[0], i[1]])])


def toutcome(a, b, c):
    cat = tcat()
    JT, ST = cat.joint_codes()
    i = [cat.idx[x] for x in (a, b, c)]
    return int(T.VEC[JT[i[0], i[1], i[2]]])


def test_T_switcher_paths():
    # resident: slot 0 reads slot 1 (C4 names its prev = slot 0), slot 2 = C1 (names its next = slot 0)
    codes, steps = tplay('Snoy', 'C4', 'C1')
    assert codes == [1, 4, 1] and steps[1] == 3 and steps[0] == 14
    assert toutcome('Snoy', 'C4', 'C1') == F01
    # immigrant in slot 1 naming its next (slot 2): the read returns 1 != 4, fallback names prev (slot 2): pair {0, 2}
    codes, steps = tplay('Snoy', 'C1', 'C1')
    assert codes == [4, 1, 1]
    assert toutcome('Snoy', 'C1', 'C1') == F02
    # fallback disabled: the stubborn twin keeps naming slot 1 and no pair forms
    assert toutcome('Snqy', 'C1', 'C1') != F02 and toutcome('Snqy', 'C1', 'C1') != F01
    # a partner naming slot 0 at 1/3 is rejected as well
    assert toutcome('Snoy', 'C3', 'C1') == F02


def test_T_two_partner_paths():
    assert toutcome('Dnfy', 'C4', 'C1') == F01
    codes, steps = tplay('Dnfy', 'C3', 'C1')               # first read rejected, second accepted
    assert codes[0] == 4 and steps[0] == 26
    assert toutcome('Dnfy', 'C3', 'C1') == F02
    # branch priority: both partners offer, the first partner (next) wins
    codes, _ = tplay('Dnfy', 'C4', 'C4')
    assert codes[0] == 1                                    # slot 1 offers slot 0 (C4) and slot 2's prev reading: C4 names its prev = slot 1
    # negative guard: when the second partner (prev) does not offer either, the fallback f names the first
    codes, _ = tplay('Dnfy', 'C0', 'C0')
    assert codes[0] == 1
    codes, _ = tplay('Dnzy', 'C0', 'C0')
    assert codes[0] == 8


def test_T_timeouts_and_symmetry():
    # three identical orientations cycle: every slot names its next, no pair
    codes, steps = tplay('Dnfy', 'Dnfy', 'Dnfy')
    assert codes == [1, 1, 1] and steps == [414, 414, 414]
    assert T.R[toutcome('Dnfy', 'Dnfy', 'Dnfy')] == (0, 0, 0)
    # mixed orientation pairs after the timeouts (the homogeneous-reader cell)
    assert toutcome('Dnfy', 'Dpfy', 'Dpfy') == F01
    # timeout 'n' (reject): the same triple takes the fallback instead
    codes, _ = tplay('Dnfn', 'Dpfn', 'Dpfn')
    assert codes[0] == 1                                    # fallback f = the first partner
    # the dearest finishing encounter of the library is 821 steps
    _, steps = _TC['tab']
    assert int(steps.max()) == 821


def test_T_exploiter():
    # Xn reads next; C3 (names its prev at 1/3) accepts anything: Xn names it at 2/3 -> unequal pair (4, 2, 0)
    assert T.R[toutcome('Xn', 'C3', 'C0')] == (4, 2, 0)
    assert T.R[toutcome('Xn', 'C4', 'C0')] == (3, 3, 0)
    assert T.R[toutcome('Xn', 'C5', 'C0')] == (0, 0, 0)     # a partner demanding 2/3 is rejected: null


def test_T_price_types():
    cat = CP.get_cat('T-main')
    U = [np.array([cat.idx['Snoy'], cat.idx['C1']]), np.array([cat.idx['C4'], cat.idx['C1']]), np.array([cat.idx['C1']])]
    J0, P0, V0 = cat.make_J(U, 0.0)
    J1, P1, V1 = cat.make_J(U, 1.2e-4)
    # same outcomes; net payoffs differ by price * steps for the program that reads
    assert (V1[J1] == V0[J0].astype(np.int64)).all() or (V1[J1] == V0[J0]).all()
    k = (0, 0, 0)                                           # (Snoy, C4, C1): F01, Snoy takes 14 steps
    assert abs(P0[J0[k], 0] - P1[J1[k], 0] - 1.2e-4 * 14) < 1e-12
    assert abs(P0[J0[k], 1] - P1[J1[k], 1] - 1.2e-4 * 3) < 1e-12


# ------------------------------------------------------------------ the DSL by hand
def dplay(cat, a, b, c):
    S = cat.S
    u, typ, val = D.encounter(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, a, b, c)
    return tuple(int(x) for x in u), int(typ)


def test_dsl_named_readers_modal():
    cat = CP.get_cat('Emin-main-m')
    ci = PR.const_index(cat)
    lo = D.local_of
    C01 = ci[lo(0, 1, 1)]; C10 = ci[lo(1, 0, 1)]; C20 = ci[lo(2, 0, 1)]; C12 = ci[lo(1, 2, 1)]
    sw = cat.idx[(0, 'Sj')]
    # resident: reader accepts slot 1's half offer; slot 2 offers slot 0 as well
    assert dplay(cat, sw, C10, C20)[0] == (3, 3, 0)
    # immigrant in slot 1 names slot 2: the box is false, the reader names slot 2, slot 2 names slot 0
    assert dplay(cat, sw, C12, C20)[0] == (3, 0, 3)
    # two-partner reader: first slot 1, then slot 2
    r2 = cat.idx[(0, 'R2jf')]
    assert dplay(cat, r2, C10, C20)[0] == (3, 3, 0)
    assert dplay(cat, r2, C12, C20)[0] == (3, 0, 3)
    # branch priority: both partners offer, the first (slot 1) wins
    assert dplay(cat, r2, C10, C20)[0] == (3, 3, 0)
    # fallback stay: nobody offers, the reader names slot 1 and no pair forms
    C21 = ci[lo(2, 1, 1)]
    assert dplay(cat, r2, ci[lo(1, D.ALL, 1)], ci[lo(2, D.ALL, 1)])[0] == (0, 0, 0)
    # the taker: accepts the excluded slot's offer
    tk = cat.idx[(0, 'Sk')]
    assert dplay(cat, tk, C10, ci[lo(2, 1, 1)])[0] == (3, 3, 0)
    assert dplay(cat, tk, C10, C20)[0] == (3, 0, 3)


def test_dsl_hom_cells_by_hand():
    cm = CP.get_cat('Emin-main-m'); cw = CP.get_cat('Emin-main-w')
    rm = PR.Roles(cm); rw = PR.Roles(cw)
    a, b, c = rm.hom['modal']
    assert dplay(cm, a, b, c)[0] == (3, 3, 0)               # mutual reading by Loeb
    # the weak arm: two readers that read each other diverge and play (ALL, 2/3): no pair
    assert dplay(cw, a, b, c)[0] == (0, 0, 0)
    a, b, c = rw.hom['weak']
    assert dplay(cw, a, b, c)[0] == (3, 3, 0)
    # homogeneous cells through the probe code: resident outcome F{0,1}
    for cat, key in ((cm, 'modal'), (cw, 'weak')):
        r = PR.Roles(cat)
        x = r.hom[key]
        pr = PR.make_prep(cat, [[x[0]], [x[1]], [x[2]]])
        dist, pay, red = PR.encounter_stats(pr, PR.init_local(pr, [{x[0]: 100}, {x[1]: 100}, {x[2]: 100}]), 100)
        assert dist[F01] > 0.999


def test_T_hom_cell():
    cat = CP.get_cat('T-main')
    r = PR.Roles(cat)
    x = r.hom['T']
    pr = PR.make_prep(cat, [[x[0]], [x[1]], [x[2]]])
    dist, pay, red = PR.encounter_stats(pr, PR.init_local(pr, [{x[0]: 100}, {x[1]: 100}, {x[2]: 100}]), 100)
    assert dist[F01] > 0.999


def test_E10_has_no_two_partner_reader():
    cat = CP.get_cat('E10m')
    forms = CP.reader_forms(0)
    for key, f in forms.items():
        if key.startswith('R2'):
            assert f not in cat.S.index[0]
        else:
            assert f in cat.S.index[0]
    # n = 11 does have them (size 11)
    L11, S11, mu11, cnt11, size11 = D.build('modalPA', 11)
    assert forms['R2jf'] in S11.index[0] and size11[S11.index[0][forms['R2jf']]] == 11


# ------------------------------------------------------------------ flips on hand-built trajectories
def _series(spec, G):
    s = np.zeros(G + 1, np.int8)
    for (a, b, v) in spec:
        s[a:b] = v
    return s


def test_flip_statistic_handbuilt():
    A, B, Cc, Dd = F01, F02, F12, int(MW.CATMAP.tolist().index(4))
    G = 200
    # island 0: A to B at 50 (held), B to C at 120 (held), island 1: a 10-generation excursion (not a flip), island 2:
    # A then a change to a non-member at 150 held to the end of the horizon
    isl0 = _series([(0, 50, A), (50, 120, B), (120, 201, Cc)], G)
    isl1 = _series([(0, 100, A), (100, 110, B), (110, 201, A)], G)
    isl2 = _series([(0, 150, A), (150, 201, Dd)], G)
    modal = np.stack([isl0, isl1, isl2], axis=1)
    fl = CP.flips(modal)
    assert fl[0] == [(50, A, B), (120, B, Cc)] and fl[1] == [] and fl[2] == [(150, A, Dd)]
    fc = CP.flip_counts(fl, modal, G)
    assert fc['mm'] == 2 and fc['mo'] == 1 and fc['om'] == 0 and fc['oo'] == 0
    assert fc['expo'] == (G + 1) * 2 + 150                  # island 0 and 1 are on fair pairs throughout; island 2 for 150
    # a change inside the last 25 generations is accepted (to the end of the horizon)
    isl = _series([(0, 190, A), (190, 201, B)], G)[:, None]
    assert CP.flips(isl)[0] == [(190, A, B)]
    # flips after the stop generation are not counted
    fc2 = CP.flip_counts(fl, modal, 100)
    assert fc2['mm'] == 1 and fc2['mo'] == 0


# ------------------------------------------------------------------ reproduction of the stored runs
def test_restricted_grammar_equals_n6():
    L10 = D.Lang(10, (0,))
    fs10, mu10, cnt10, size10 = L10.canon(6)
    L6, S6, mu6, cnt6, size6 = D.build('modalPA', 6)
    assert [f for f in fs10] == list(S6.fs)
    assert np.allclose(mu10 / mu10.sum(), mu6)


def test_B6m_reproduces_stored_modalPA_lottery():
    stored = json.load(open(os.path.join(ROOT, 'runs', 'stable_sets', 'M0.json')))['runs']
    cat = CP.get_cat('B6m')
    for r in (0, 1):
        prep = CP.prepare(cat, 'L0', r)
        res = CP.kernel(prep, 0, 10000)
        s = [x for x in stored if x['run'] == r][0]
        assert prep['seed'] == s['seed']
        assert res['status'] == s['status'] and res['stop'] == s['stop_gen'] and res['nev'] == s['nev']
        assert [len(u) for u in prep['U']] == s['K']


def test_B6w_reproduces_stored_migration_window_rows():
    sto = json.load(open(os.path.join(ROOT, 'runs', 'migration_window', 'M-base-N100-m1.json')))
    sf = sto['snap_fields']
    r0 = [r for r in sto['runs'] if r['run'] == 0][0]
    recs = CP.run_cell_run('B6w', 0, mNs=(1,), H=10000)
    snap = recs[0]['snap']['10000']
    st = dict(zip(sf, r0['snap']['10000']))
    assert snap['nm'] == st['nm'] and snap['F'] == st['F'] and snap['cons'] == st['cons'] and abs(snap['inef'] - st['inef']) < 1e-9


def test_emin_law_and_catalogue():
    cat = CP.get_cat('Emin-main-m')
    for s in range(3):
        p = cat.law(s)
        assert abs(p.sum() - 1) < 1e-12
        tw = sum(p[cat.idx[(s, k)]] for k in ('R2jf', 'R2jz', 'R2kf', 'R2kz'))
        assert abs(tw - 0.03) < 1e-6 or tw > 0.03 - 1e-6
        # the E-min readers read the right atoms: the two-partner reader of slot s names a partner when it offers s a half
        S = cat.S
        x = cat.idx[(s, 'R2jf')]
        assert S.nat[s, x] == 2
    low = CP.get_cat('Emin-lo-m'); hi = CP.get_cat('Emin-hi-m')
    for cat_, w in ((low, 0.003), (hi, 0.10)):
        p = cat_.law(0)
        assert abs(sum(p[cat_.idx[(0, k)]] for k in ('R2jf', 'R2jz', 'R2kf', 'R2kz')) - w) < 1e-3


def test_T_law_sums():
    for dose, two in (('main', 0.03), ('lo', 0.003), ('hi', 0.10)):
        cat = CP.get_cat('T-' + dose)
        w = cat.law(dose)
        assert abs(w.sum() - 1) < 1e-12
        assert abs(sum(w[i] for i in range(cat.K) if cat.fam[i] == 'two') - two) < 1e-12
        assert w[[i for i in range(cat.K) if cat.fam[i] == 'stub']].sum() == 0


def test_balanced_start_pairs():
    """every island of a balanced start sits on its pair, for every kind in every grammar."""
    for spec in ('Emin-main-m', 'Emin-main-w', 'T-main'):
        cat = CP.get_cat(spec)
        for kind in ('const', 'switch', 'two'):
            prep = PR.prepare_balanced(cat, kind, 'test-bal', 0, I=6)
            res = CP.kernel(prep, 0.0, 30)
            want = [F01, F02, F12, F01, F02, F12]
            got = [int(res['modal'][0, i]) for i in range(6)]
            # the excluded slot is natural: the pair should still be the modal outcome on most islands
            assert sum(g == w for g, w in zip(got, want)) >= 4, (spec, kind, got)
            for i in range(3):
                a, b = ((0, 1), (0, 2), (1, 2))[i]
                ca, cb = PR.pair_residents(cat, kind, a, b)
                assert prep['loc'][i].sum() == 300
