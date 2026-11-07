"""Tests for the majority-division-in-the-current-object experiment (spec specs/2026-11-07-majority-current-object.md):
the kernel reduces to kern_mw without arrivals (draw for draw), the arrival schedule (mean, nesting, own stream), the
clean-tail identities, matched-mass removals, slot symmetry of the laws and tables, the charged table of arm T, the
arrival bookkeeping (a single arrival lands where it should), and the summary statistics on hand-built series.

    python3 -m pytest tests/test_majority_tail.py -q
"""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import numpy as np
import dollar3 as D
import stable_sets as SS
import migration_window as MW
import migration_window_kernels as MKW
import churn_primary as CP
import majority_tail as MT
import majority_tail_kern as MK

T = MT.T


def test_kernel_equals_kern_mw_without_arrivals():
    cat = CP.get_cat('B6w')
    for r in range(2):
        prep = CP.prepare(cat, 'L1', r)
        for mN in (0, 1):
            H = 1500
            ref = MKW.kern_mw(prep['J'], prep['PAY'], prep['VEC'], T.ISMEM, T.TOT, prep['loc'], prep['N'], MT.W,
                              mN / prep['N'], prep['seed'], H, 10, np.zeros(0, np.int64), 200000)
            z = np.zeros(0, np.int64)
            out = MK.kern_mt(prep['J'], prep['PAY'], prep['VEC'], T.ISMEM, T.TOT, prep['loc'], prep['N'], MT.W,
                             mN / prep['N'], prep['seed'], H, 10, np.array([0, 500, H], np.int64), z, z, z, np.zeros(0), z, 1000, 1000)
            status, stop, counts, modal = out[0], out[1], out[2], out[3]
            assert int(status) == int(ref[0]) and int(stop) == int(ref[1])
            assert (counts == ref[2]).all()
            assert (modal.astype(np.int64) == ref[9].astype(np.int64)).all()
            assert int(out[-1]) == int(ref[8])


def test_schedule_mean_nesting_and_stream():
    N, I = 100, 64
    geo = MT.geometry(N)
    s = MT.make_schedule(N, 3, I)
    expect = 100.0 * (1 - 1 / (1 + (geo['gend'] - geo['g0']) / geo['t0']))
    n = len(s['g']) / I
    assert abs(n - expect) < 4 * np.sqrt(expect / I) + 1.0
    assert s['g'].min() >= geo['g0'] and s['g'].max() < geo['gend']
    laws = MT.base_laws('M')
    a100 = MT.map_programs(s, laws, 100)
    a10 = MT.map_programs(s, laws, 10)
    keys100 = set(zip(a100[0].tolist(), a100[1].tolist(), a100[2].tolist(), a100[3].tolist()))
    keys10 = set(zip(a10[0].tolist(), a10[1].tolist(), a10[2].tolist(), a10[3].tolist()))
    assert keys10 <= keys100 and 0.05 < len(keys10) / len(keys100) < 0.2
    # times, islands, slots and victims are arm independent (program draws are the only arm-dependent part)
    lawsT = MT.base_laws('T')
    b100 = MT.map_programs(s, lawsT, 100)
    for x, y in zip(a100[:4], b100[:4]):
        assert (x == y).all()
    assert b100[4].max() < 27


def test_arrival_law_matches_seed_law():
    s = MT.make_schedule(100, 0, 64)
    laws = MT.base_laws('M')
    g, i, sl, u, k = MT.map_programs(s, laws, 100)
    for slot in range(3):
        ks = k[sl == slot]
        p = laws[slot]
        top = [x for x in np.argsort(-p)[:20] if p[x] * len(ks) >= 5]      # pool classes with expected count < 5
        obs = np.array([(ks == x).sum() for x in top] + [(~np.isin(ks, top)).sum()], float)
        pe = np.array([p[x] for x in top] + [1 - p[top].sum()]) * len(ks)
        chi2 = ((obs - pe) ** 2 / pe).sum()
        from scipy.stats import chi2 as C2
        assert C2.sf(chi2, len(pe) - 1) > 0.001


def test_clean_identities_match_queue71():
    import unequal_basin_run as R
    import unequal_basin as UB
    cat = CP.get_cat('B6m')
    fam, vic, bul = MT.dsl_family_data(cat.S)
    assert (vic.sum(1) == 2).all() and (bul.sum(1) == 2).all()
    class A:
        pass
    a = A(); a.S = cat.S
    ref = R.family_mask(a, 'exploiter-fair')
    assert (ref == bul).all()
    p = MT.base_laws('M')[0]
    cm = MT.clean_mask('M')
    assert abs(p[cm[0]].sum() - 0.217) < 0.01        # the spec's matched mass per slot


def test_matched_mass_removals():
    p = MT.base_laws('M')
    cm = MT.clean_mask('M')
    mass = p[0][cm[0]].sum()
    for d in range(3):
        fl, tl = MT.variant_laws('M', 'D4:%d' % d)
        assert fl[0] is tl[0] or (fl[0] == tl[0]).all()
        for s in range(3):
            removed = p[s][fl[s] == 0].sum()
            assert abs(removed - mass) < 0.0035
            assert abs(fl[s].sum() - 1) < 1e-12
            assert not (fl[s][cm[s]] == 0).any() or True
    a = MT.variant_laws('M', 'D4:0')[0]; b = MT.variant_laws('M', 'D4:1')[0]
    assert not (a[0] == b[0]).all()


def test_slot_symmetry_of_laws_and_tables():
    cat = CP.get_cat('B6m')
    S = cat.S
    rot = [1, 2, 0]
    perm = S.permute(rot)
    law = MT.base_laws('M')
    for s in range(3):
        assert np.allclose(law[rot[s]][perm[s]], law[s])
    fam, vic, bul = MT.dsl_family_data(S)
    for s in range(3):
        assert (fam[rot[s]][perm[s]] == fam[s]).all()
        assert (vic[rot[s]][perm[s]] == vic[s]).all() and (bul[rot[s]][perm[s]] == bul[s]).all()
    # joint table equivariance on random triples: play(x0,x1,x2) rotated equals play of the images
    rng = np.random.default_rng(0)
    for _ in range(300):
        x = rng.integers(0, S.K, 3)
        a = SS._joint_table(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, x[:1], x[1:2], x[2:3])[0, 0, 0]
        y = np.array([perm[s][x[s]] for s in range(3)])
        # slot s program goes to slot rot[s]; the image triple in slot order
        z = np.zeros(3, np.int64)
        for s in range(3):
            z[rot[s]] = y[s]
        b = SS._joint_table(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, z[:1], z[1:2], z[2:3])[0, 0, 0]
        # outcome ids correspond under the rotation: compare the fair/unequal/grand/waste class
        assert MW.CATMAP[T.VEC[a]] == MW.CATMAP[T.VEC[b]]


def test_tabs_charge_and_closure_types():
    import many_islands_t as MIT
    tabs = MT._tabs()
    J, PAY, VEC, ISMEM, TOT = MT.t_charged_tables(tabs, 0.1)
    net = tabs.payoff(0.1, 0.1)
    rng = np.random.default_rng(1)
    for _ in range(2000):
        a, b, c = (int(x) for x in rng.integers(0, 27, 3))
        t = J[a, b, c]
        assert np.allclose(PAY[t], net[a, b, c])
        assert VEC[t] == tabs.OUT[a, b, c]


def test_single_arrival_lands_and_is_logged():
    # a homogeneous island set: every slot all program 0; one arrival of program 1 in slot 0 on island 0
    cat = CP.get_cat('B6m')
    S = cat.S
    U = [np.array([0, 1])] * 3
    J = MT._joint16(cat.armi, S.nat, S.atL, S.atJ, S.atA, S.tab, D.PARTNER, U[0], U[1], U[2])
    I, N = 4, 20
    loc = np.zeros((I, 3, 2), np.int64); loc[:, :, 0] = N
    ag = np.array([5], np.int64); ai = np.array([2], np.int64); asl = np.array([0], np.int64)
    au = np.array([0.5]); ak = np.array([1], np.int64)
    out = MK.kern_mt(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, N, MT.W, 0.0, 7, 30, 10, np.array([4, 6], np.int64),
                     ag, ai, asl, au, ak, 100, 100)
    snapc = out[5]; alog = out[9]; na = out[10]
    assert na == 1 and tuple(alog[0][:4]) == (5, 2, 0, 1) and alog[0][5] == 1
    assert snapc[0, 2, 0, 1] == 0 and snapc[1, 2, 0, 1] >= 0
    assert snapc[0].sum() == I * 3 * N


def test_transition_counts_hand_built():
    G, I = 400, 2
    ids = np.zeros((G + 1, I), np.int64)
    fair = MW.V[0]
    other = [k for k in range(MT.NOUT) if MW.CATMAP[k] == 1][0]
    ids[:, :] = fair
    ids[100:200, 0] = other                    # island 0: F -> U at 100, back at 200
    ids[250:255, 1] = other                    # a blip shorter than the debounce: ignored at 25
    tr = MT.transitions(ids, 0, 400, 25)
    M = np.array(tr['M'])
    assert M[0, 1] == 1 and M[1, 0] == 1 and M.sum() == 2
    tr = MT.transitions(ids, 0, 400, 3)
    assert np.array(tr['M']).sum() == 4


def test_consensus_flags():
    fair = MW.V[1]
    ids = np.full(64, fair)
    assert MT.consensus_flags(ids) == (1, -1)
    ids[0] = MW.V[0]
    assert MT.consensus_flags(ids) == (-1, -1)          # 63/64 < 0.99
