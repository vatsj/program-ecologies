"""Tests of the unequal-basin machinery (src/unequal_basin*.py).  Fast; the long validations are in
src/unequal_basin_validate.py and recorded in runs/unequal_basin/validate-*.json."""
import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import many_islands as MI
import stable_sets as SS
import unequal_basin as UB
import unequal_basin_core as UC
import unequal_basin_validate as UV


def small_support(arm, seed=1, n=10):
    return UV.tiny_support(arm, np.random.default_rng(seed), n)


def test_pf30_table_matches_pfix():
    for d in range(-UB.DMAX, UB.DMAX + 1):
        assert abs(UB.PF30[d + UB.DMAX] - MI.pfix(d / 30.0, 100.0, 0.3)) < 1e-15


def test_extended_code_low_part_and_mask():
    arm = UB.get_arm('L')
    arm_old = MI.Arm('L')
    arm_old.new_cache(20)               # separate cache: the stored joint code and the extended one must not share a table
    rng = np.random.default_rng(3)
    n_div = 0
    for _ in range(3000):
        tr = rng.integers(0, UB.KP, 3)
        c2 = UC.joint2(arm, *tr)
        c = int(MI.jl(arm_old.ctx(), *map(np.int64, tr)))
        assert c2 % 729 == c
        n_div += c2 // 729 != 0
    # mutual reading between two conditionals diverges (mask with the two readers' bits)
    fs = arm.S.fs
    ids = [x for x, f in enumerate(fs) if len(f[0]) == 1]
    found = False
    for x in ids[:600]:
        for y in ids[:600:5]:
            c2 = UC.joint2(arm, x, y, 0)
            if c2 // 729 == 3:
                found = True
                break
        if found:
            break
    assert found, 'no mutual-reading divergent pair found among conditionals'


def test_charge_in_payoff_table():
    PAY2, VEC2 = UC.tables2(0.1)
    for m in range(8):
        for s in range(3):
            assert np.allclose(PAY2[m * 729:(m + 1) * 729, s], MI.PAY[:, s] - 0.1 * ((m >> s) & 1))


def test_island_run2_matches_stored_kernel_at_pfail_zero():
    arm_a = MI.Arm('L'); arm_a.new_cache(20)
    arm_b = MI.Arm('L'); arm_b.new_cache(20)
    PAY2, _ = UC.tables2(0.0)
    for i in range(6):
        rf = np.random.default_rng(UC.crc('mi-found|LM|0|%d' % i))
        init = np.stack([rf.multinomial(100, arm_a.laws[s]) for s in range(3)]).astype(np.int64)
        r1 = MI.island_run(arm_a.ctx(), arm_a.lc(32), MI.PAY, init, 100, MI.W, 11 + i, 20002, np.empty(0), arm_a.cum, True)
        r2 = UC.island_run2(arm_b.ctx(), arm_b.lc(32), PAY2, init, 100, MI.W, 11 + i, 20002, np.empty(0), arm_b.cum, True)
        assert r1[0] == r2[0] and r1[1] == r2[1] and (r1[2] == r2[2]).all()


@pytest.mark.parametrize('armname,pfail', [('L', 0.1), ('M', 0.0)])
def test_field_matches_definition_and_conserves_mass(armname, pfail):
    arm = UB.get_arm(armname)
    supp = small_support(arm)
    obj = UB.Obj(armname, pfail, supp, 2)
    rng = np.random.default_rng(4)
    x = rng.random(obj.n) ** 3
    x /= x.sum()
    F = UB.field(obj, x, sym=False)
    assert abs(F.sum()) < 1e-15
    q = obj.marg(x)
    for ti in rng.integers(0, obj.n, 60):
        t = obj.T[ti].astype(np.int64)
        tot = 0.0
        for s in range(3):
            for y in obj.supp[s]:
                if y != t[s]:
                    t2 = t.copy(); t2[s] = y
                    p2, ok = obj.index_of(t2[None, :])
                    if ok[0]:
                        tot -= x[ti] * q[s, y] * UB.PF30[obj.lev[s, p2[0]] - obj.lev[s, ti] + UB.DMAX] / 3.0
            y = t[s]
            for u in obj.supp[s]:
                if u != y:
                    t2 = t.copy(); t2[s] = u
                    p2, ok = obj.index_of(t2[None, :])
                    if ok[0]:
                        tot += x[p2[0]] * q[s, y] * UB.PF30[obj.lev[s, ti] - obj.lev[s, p2[0]] + UB.DMAX] / 3.0
        assert abs(tot - F[ti]) < 1e-14


def test_jvp_is_the_derivative():
    arm = UB.get_arm('L')
    obj = UB.Obj('L', 0.1, small_support(arm, 5, 8), 1)
    rng = np.random.default_rng(6)
    x = rng.random(obj.n); x /= x.sum()
    v = rng.standard_normal(obj.n) * 1e-3
    h = 1e-6
    fd = (UB.field(obj, x + h * v, sym=False) - UB.field(obj, x - h * v, sym=False)) / (2 * h)
    assert np.abs(fd - UB.jvp(obj, x, v, sym=False)).max() < 1e-9


def test_symmetry_of_table_and_field():
    arm = UB.get_arm('L')
    obj = UB.Obj('L', 0.1, small_support(arm, 7, 12), 2)
    for i, (sg, perm) in enumerate(obj.pm):
        pi = obj.perm_idx[i]
        for s in range(3):
            assert (obj.lev[sg[s], pi] == obj.lev[s]).all()
        assert (obj.cl[pi] == obj.cl).all()
    rng = np.random.default_rng(8)
    x = obj.sym(rng.random(obj.n)); x /= x.sum()
    F = UB.field(obj, x, sym=False)
    assert np.abs(F - obj.sym(F)).max() < 1e-14


def test_lumping_is_exact_on_merging_support():
    res = UV.v2()
    for k, v in res.items():
        assert v['passed'], (k, v)
    assert res['L-all-action']['classes'][0] < res['L-all-action']['programs'][0]


def test_constants_table_equals_arm_t():
    try:
        import many_islands_t_common as CT
        T = CT.tabs()
    except Exception as e:                      # arm-T cache not present in this checkout
        pytest.skip('arm-T tables unavailable: %s' % e)
    arm = UB.get_arm('L')
    ci = SS.const_index(arm.S.fs)
    def dsl_local(s, v):
        if s == 1:
            pi, d = v // 3, v % 3
            return 3 * (1 - pi) + d if pi < 2 else v
        return v
    mp = np.array([[ci[dsl_local(s, v)] for v in range(9)] for s in range(3)])
    obj = UB.Obj('L', 0.0, [mp[s].tolist() for s in range(3)], 0)
    PT = T.payoff(0.0)
    for a in range(9):
        for b in range(9):
            for c in range(9):
                pos, ok = obj.index_of(np.array([[mp[0][a], mp[1][b], mp[2][c]]]))
                assert np.allclose((obj.lev[:, pos[0]] - 3) / 30.0, PT[a, b, c])


def test_tilt_keeps_within_class_frequencies():
    arm = UB.get_arm('L')
    obj = UB.Obj('L', 0.0, small_support(arm, 9, 10), 1)
    rng = np.random.default_rng(10)
    x = rng.random(obj.n); x /= x.sum()
    y, info = UB.tilt(obj, x, 'unequal', 0.6)
    assert info['available']
    sh = obj.class_shares(y)
    assert abs(sh[1] - 0.6) < 1e-12 and abs(sh.sum() - 1) < 1e-12
    sel = obj.cl == 1
    assert np.allclose(y[sel] / y[sel].sum(), x[sel] / x[sel].sum())
