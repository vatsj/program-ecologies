"""Tests for the immigrant-rejection experiment (notes/immigrant-rejection.md).  Run: python3 -m pytest tests/test_immigrant_rejection.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import immigrant_rejection as IR
import migration_window as MW
import migration_window_kernels as MK
import immigrant_rejection_kernels as IK
import stable_sets as SS
import farsighted_refusal as F

T = IR.T


def _setup(names, assign, I=6, N=30, base='L1', r=0):
    init, _ = MW.founders(base, r, I, N)
    loc, U = SS.compress(init)
    st = F.Setup(loc, U, len(names), assign=assign, rng=None)
    return st, I, N


def _args(st, N, mN, seed, H, nu, ga):
    return (st.J, T.PAY, T.VEC, T.ISMEM, T.TOT, st.tc0, st.TK, st.TO, st.TG, st.TPC, st.TMAP, st.ntypes, st.Kmax, st.NG, N,
            SS.W, mN / N, seed, H, 10, np.zeros(0, np.int64), nu, IR.CS, IR.CD, IR.CACT, F.CX, ga['GKIND'], ga['GTAB'],
            ga['KRTAB'], F.PROPM, F.UPAY, float(ga['rdelta']), nu == 0.0, 50, 1000, 20000)


def test_identity_with_fkern_mw():
    """with fr = 0 the generated kernel reproduces fkern_mw draw for draw (gV and g0 contract cells, mN = 1)."""
    for names, assign in ((['g0', 'gV'], ('bit', 1.0, 1)), (['g0'], None)):
        st, I, N = _setup(names, assign)
        ga = IR.guard_arrays_ir(names)
        a = _args(st, N, 1.0, 12345, 400, 0.1, ga)
        res0, m0, e0, f0 = MK.fkern_mw(*a)
        res1, m1, e1, f1, fate, tdesc = IK.fkern_ir(*a, np.array([0, 0, 0, 1], np.int64), IR.EXCL, IR.PARTNER)
        assert np.array_equal(res0[3], res1[3])          # cls
        assert np.array_equal(m0, m1) and np.allclose(e0, e1) and np.allclose(f0, f1)
        assert np.array_equal(res0[2], res1[2])          # final type counts
        assert res0[8] == res1[8] and res0[10] == res1[10]   # migrants, contract events
        assert np.array_equal(res0[11], res1[11])        # contract counters


def test_identity_with_kern_mw_baseline():
    """nu = 0, guard g0 only: the classes of every island and generation are those of kern_mw (the stored baseline)."""
    for mN in (0.0, 1.0):
        init, _ = MW.founders('L1', 1, 6, 30)
        loc, U = SS.compress(init)
        J = SS.joint_for('weak', U)
        out = MK.kern_mw(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, 30, SS.W, mN / 30, 777, 500, 10, np.zeros(0, np.int64), 1000)
        st = F.Setup(loc, U, 1, assign=None, rng=None)
        ga = IR.guard_arrays_ir(['g0'])
        res1, m1, e1, f1, fate, tdesc = IK.fkern_ir(*_args(st, 30, mN, 777, 500, 0.0, ga), np.array([0, 0, 0, 1], np.int64),
                                                    IR.EXCL, IR.PARTNER)
        assert int(out[0]) == int(res1[0]) and int(out[1]) == int(res1[1])
        assert np.array_equal(out[3], res1[3])
        assert np.array_equal(out[9], m1)
        assert int(out[8]) == int(res1[8])


def test_fair33_and_excl_tables():
    assert IR.FAIR33.sum() == 3
    assert len(IR.V) == 3
    assert sorted(int(IR.EXCL[z]) for z in IR.V) == [0, 1, 2]
    # the strict veto refuses everything at a fair pair; gV exempts exactly the (3, 3) contracts there
    Ts = IR.table_gVs(); Tv = F.table_gV()
    for y in IR.V:
        assert not Ts[y].any()
        for k in range(F.NCON):
            assert bool(Tv[y, k, 0] and Tv[y, k, 1]) == bool(IR.FAIR33[k])
    assert np.array_equal(Ts[[y for y in range(F.NX) if y not in IR.V]], Tv[[y for y in range(F.NX) if y not in IR.V]])


def test_weak_consent_contains_strict():
    import farsighted_refusal_run as FR
    Tk, d, W, acc = FR.kr_table('0.99')
    Tw = IR.table_gKRw()
    assert (Tw | ~Tk).all()                    # strict acceptance implies weak acceptance


def _tiny_J():
    """two constant classes per slot: slot 0: 0 -> (name slot 1, 1/2), 1 -> (name slot 2, 1/2); slot 1: 0 -> (name 0), 1 -> (name 2);
    slot 2: 0 -> (name 0), 1 -> (name 1); local action 1 = (first other, 1/2), 4 = (second other, 1/2)."""
    a = [[1, 4], [1, 4], [1, 4]]
    J = np.zeros((2, 2, 2), np.int32)
    for x in range(2):
        for y in range(2):
            for z in range(2):
                J[x, y, z] = a[0][x] * 81 + a[1][y] * 9 + a[2][z]
    return J


def test_veto_by_hand():
    J = _tiny_J()
    z = [z for z in IR.V if IR.EXCL[z] == 2][0]           # pair (0, 1), slot 2 excluded
    ismem = T.ISMEM
    lastmod = np.array([z], np.int64); modcls = np.zeros((1, 3), np.int64)
    V = IK._veto
    P = IR.PARTNER
    # pivot (slot 0) partner choice 1 -> 2
    assert V(np.array([0, 1, 0, 1]), False, 0, 0, 0, 1, lastmod, modcls, IR.EXCL, ismem, J, P)
    assert V(np.array([0, 2, 0, 1]), False, 0, 0, 0, 1, lastmod, modcls, IR.EXCL, ismem, J, P)       # local births only: local
    assert not V(np.array([0, 2, 0, 1]), True, 0, 0, 0, 1, lastmod, modcls, IR.EXCL, ismem, J, P)    # migrant passes
    assert V(np.array([0, 3, 0, 1]), True, 0, 0, 0, 1, lastmod, modcls, IR.EXCL, ismem, J, P)        # migrant only
    # excluded slot offers 0 -> 1
    assert V(np.array([1, 0, 0, 1]), False, 0, 2, 0, 1, lastmod, modcls, IR.EXCL, ismem, J, P)
    assert not V(np.array([0, 1, 0, 1]), False, 0, 2, 0, 1, lastmod, modcls, IR.EXCL, ismem, J, P)   # FP does not freeze it
    # fiat on immigrants: any slot, migrant births only
    assert V(np.array([0, 0, 1, 1]), True, 0, 2, 0, 1, lastmod, modcls, IR.EXCL, ismem, J, P)
    assert not V(np.array([0, 0, 1, 1]), False, 0, 2, 0, 1, lastmod, modcls, IR.EXCL, ismem, J, P)
    # same class, or a non-member island: never vetoed
    assert not V(np.array([1, 1, 1, 1]), True, 0, 0, 1, 1, lastmod, modcls, IR.EXCL, ismem, J, P)
    nm = [k for k in range(len(ismem)) if not ismem[k]][0]
    assert not V(np.array([1, 1, 1, 1]), True, 0, 0, 0, 1, np.array([nm], np.int64), modcls, IR.EXCL, ismem, J, P)


def test_flips_by_hand():
    G = 400
    modal = np.zeros((G, 3), np.int8)
    a, b = IR.V[0], IR.V[1]
    modal[:, 0] = a; modal[100:, 0] = b                       # one clean flip at 100
    modal[:, 1] = a; modal[50:60, 1] = b                      # a flicker of 10 generations: not a flip
    modal[:, 2] = a; modal[380:, 2] = b                       # a flip inside the last 25 generations: accepted (to the end)
    fl = IR.flips(modal)
    assert fl[0] == [(100, a, b)] and fl[1] == [] and fl[2] == [(380, a, b)]
    fs = IR.flip_summary(fl, np.array([[99, 0]]), G)          # an install on island 0 at generation 99 mediates the flip at 100
    assert fs['mm'] == 2 and fs['mm_med'] == 1


def test_candidates_by_hand():
    s = 0
    # slots 1 and 2 both name slot 0 at 1/2 (3 sixths): a tie for a program that demands 1/2
    act_b = (0, 3); act_c = (0, 3)
    base = (1, 3)
    assert IR.is_tie(0, base, act_b, act_c)[0]
    assert not IR.is_tie(0, base, act_b, (1, 3))[0]
    assert not IR.is_tie(0, (1, 4), (0, 3), (0, 3))[0]        # 4 + 3 > 6: the offers are not completions at demand 2/3
    # LOYAL-1
    assert IR.loyal_choice(s, base, act_b, act_c, [2], 1) == (2, 3)
    assert IR.loyal_choice(s, base, act_b, act_c, [1, 2], 1) == (2, 3)          # last encounter only
    assert IR.loyal_choice(s, base, act_b, act_c, [], 1) == base                # empty memory: base
    assert IR.loyal_choice(s, base, act_b, act_c, [None], 1) == base            # excluded last time: base
    assert IR.loyal_choice(s, base, (0, 3), (2, 3), [2], 1) == base             # not a tie: base is untouched
    # LOYAL-5: strict majority of the last five
    assert IR.loyal_choice(s, (1, 3), act_b, act_c, [2, 2, 1, 2, 1], 5) == (2, 3)   # 3 of 5
    assert IR.loyal_choice(s, (2, 3), act_b, act_c, [1, 1, 2, None, 2], 5) == (2, 3)      # 2-2-1: no strict majority, the base choice stands
    assert IR.loyal_choice(s, base, act_b, act_c, [1, 2, None, 1, 2], 5) == base     # 2-2-1: no majority
    assert IR.loyal_choice(s, base, act_b, act_c, [2, 2, 2, 2, 2, 1], 5) == (2, 3)   # only the last five count: 4 of 5
    # SQ-direct
    assert IR.sq_choice(0, (2, 3), act_b, act_c, (0, 1)) == (1, 3)                  # island on (0, 1): keep 1
    assert IR.sq_choice(0, (2, 3), act_b, act_c, (1, 2)) == (2, 3)                  # slot 0 not in the pair: base
    # SQ-valued: symmetric values give an exact tie at eps = 0 (fall back to base), a strict choice at eps > 0
    W = {1: 7.0, 2: 7.0}
    assert IR.sq_valued_choice(0, (2, 3), act_b, act_c, W, 1, 0.0) == (2, 3)         # no override: base action
    assert IR.sq_valued_choice(0, (2, 3), act_b, act_c, W, 1, 0.05) == (1, 3)        # incumbent partner 1 wins
    assert IR.sq_valued_choice(0, (1, 3), act_b, act_c, W, 2, 0.05) == (2, 3)
    assert IR.sq_valued_choice(0, (1, 3), act_b, act_c, {1: 7.0, 2: 7.02}, 1, 0.05) == (1, 3)  # cost larger than the gap
    assert IR.sq_valued_choice(0, (1, 3), act_b, act_c, {1: 7.0, 2: 7.2}, 1, 0.05) == (2, 3)   # gap larger than the cost
    # CONF
    assert IR.conf_update(0, (2, 3), (0, 1)) == (1, 3)
    assert IR.conf_update(0, (2, 3), (1, 2)) == (2, 3)                                # excluded in the sample: keep
    assert IR.conf_update(0, (2, 3), None) == (2, 3)                                  # sample not a fair pair: keep


def test_run_arm_smoke_and_invariants():
    """a short run of each kind: flips, installs, fates are consistent."""
    r = IR.run_arm('gV', 1.0, 0, H=300, I=16)
    assert r['flips']['mm'] >= r['flips']['mm_med']
    assert r['inst']['inst_mem_other'] == 0           # a contract installed at a fair pair is always a (3, 3) contract under gV
    assert np.array(r['fate']).min() >= 0 and np.array(r['alive']).min() >= 0
    b = IR.run_arm('B', 1.0, 0, H=300, I=16)
    assert b['flips']['mm_med'] == 0 and sum(b['inst'].values()) == 0
    fi = IR.run_arm('FI', 1.0, 0, H=300, I=16)
    assert fi['flips']['mm'] == 0
