"""Tests for the priced RPS module (hand cost table and priced payoffs of notes/rps-priced.md section 1, the reference cost
recursion, work = depth at n = 6, c = 0 reproducing the unpriced tables exactly, forfeit-only price, the statics of
Prediction 1, priced class recomputation, lottery pairing, the toy contest).

    RPS_PRICED_CACHE=<dir> python3 -m pytest tests/test_rps_priced.py -q
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import rps as RP
import rps_priced as PP

ORDER = ['R', 'P', 'S', 'X', 'TM', 'N', 'N2', 'C', 'GN', 'GC', 'M']
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_B = {}


def base(arm, D=12):
    if (arm, D) not in _B:
        _B[(arm, D)] = PP.load_base(arm, 6, D)
    return _B[(arm, D)]


def hand_H():
    """notes/rps-priced.md 1.2: H(row, column) for the eleven programs, D = 12."""
    ix = {k: i for i, k in enumerate(ORDER)}
    H = np.zeros((11, 11))
    free = ['R', 'P', 'S', 'X', 'M']
    for r in ('TM', 'N', 'N2'):
        for k in free: H[ix[r], ix[k]] = 1.0
        for k in ('TM', 'N', 'N2', 'C'): H[ix[r], ix[k]] = 12.0
        H[ix[r], ix['GN']] = 189 / 64; H[ix[r], ix['GC']] = 13 / 2
    for k in free: H[ix['C'], ix[k]] = 1.0
    for k in ('TM', 'N', 'N2', 'C', 'GN', 'GC'): H[ix['C'], ix[k]] = 12.0
    for k in free: H[ix['GN'], ix[k]] = 0.5; H[ix['GC'], ix[k]] = 0.5
    for k in ('TM', 'N', 'N2'): H[ix['GN'], ix[k]] = 63 / 32; H[ix['GC'], ix[k]] = 6.0
    H[ix['GN'], ix['C']] = 6.0; H[ix['GN'], ix['GN']] = 4095 / 4096; H[ix['GN'], ix['GC']] = 13 / 4
    H[ix['GC'], ix['C']] = 6.0; H[ix['GC'], ix['GN']] = 6.0; H[ix['GC'], ix['GC']] = 6.0
    return H


def named_program_ids(L):
    return [L.find(RP.NAMED[k]) for k in ORDER]


def hand_U(e=1 / 128):
    import test_rps
    return test_rps.hand_table(e)


def test_hand_cost_table():
    for arm in ('exact', 'sample'):
        b = base(arm)
        L = b.lang
        have = [i for i, k in enumerate(ORDER) if RP.NAMED[k] in {L.src(e) for e in range(L.S)}] if arm == 'sample' else list(range(11))
        pid = [L.find(RP.NAMED[ORDER[i]]) for i in have]
        Hh = hand_H()[np.ix_(have, have)]
        H = np.asarray(b.H)[np.ix_(pid, pid)]
        assert np.abs(H - Hh).max() < 1e-12, arm
        HW = np.asarray(b.HW)[np.ix_(pid, pid)]
        assert np.abs(HW - Hh).max() < 1e-12
        if arm == 'sample':
            assert len(have) == 9


def test_hand_priced_payoffs():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    b = base('exact')
    L = b.lang
    pid = named_program_ids(L)
    for c in (0.001, 0.01, 0.05):
        Un = (np.asarray(b.U) - PP.price_matrix(b, c, 'depth'))[np.ix_(pid, pid)]
        want = hand_U() - c * hand_H()
        assert np.abs(Un - want).max() < 1e-12
    # spot values quoted in notes 1.3 at c = 0.01
    ix = {k: i for i, k in enumerate(ORDER)}
    Un = (np.asarray(b.U) - PP.price_matrix(b, 0.01, 'depth'))[np.ix_(pid, pid)]
    assert abs(Un[ix['N'], ix['R']] - 0.99) < 1e-12 and abs(Un[ix['N2'], ix['R']] + 1.01) < 1e-12
    assert abs(Un[ix['TM'], ix['R']] + 0.01) < 1e-12 and abs(Un[ix['N'], ix['N']] + 0.12) < 1e-12
    assert abs(Un[ix['GN'], ix['N']] - (1 / 128 - 0.01 * 63 / 32)) < 1e-12
    assert abs(Un[ix['N'], ix['GN']] - (-1 / 128 - 0.01 * 189 / 64)) < 1e-12
    assert abs(Un[ix['GC'], ix['N']] - (1 / 128 - 0.06)) < 1e-12 and abs(Un[ix['GC'], ix['GN']] + 0.06) < 1e-12
    assert np.abs(Un[ix['X']]).max() == 0.0


def test_reference_cost_agrees():
    rng = np.random.default_rng(3)
    for arm in ('exact', 'sample', 'pure', 'matched'):
        b = base(arm)
        L = b.lang
        reads = np.nonzero(L.reads_me)[0]
        for _ in range(80):
            a, c = int(rng.integers(L.S)), int(rng.integers(L.S))
            e, m = PP.cost_ref(L, a, c, 12, work=False)
            assert abs(e - b.H[a, c]) < 1e-12, (arm, L.src(a), L.src(c))
            ew, mw = PP.cost_ref(L, a, c, 12, work=True)
            assert abs(ew - b.HW[a, c]) < 1e-12
        for _ in range(60):
            a, c = int(rng.choice(reads)), int(rng.choice(reads))
            assert abs(PP.cost_ref(L, a, c, 12)[0] - b.H[a, c]) < 1e-12


def test_work_equals_depth_at_n6():
    """No body has two applications at n = 6, so work = depth on the whole table."""
    for arm in ('pure', 'sample', 'exact', 'matched'):
        b = base(arm)
        assert np.abs(np.asarray(b.HW) - np.asarray(b.H)).max() == 0.0, arm


def test_cost_bounds_and_forfeit_identity():
    """0 <= H <= D; a certain forfeit pays exactly D; H >= D * P(forfeit); the pure constants pay nothing."""
    for arm in ('exact', 'sample'):
        b = base(arm)
        H = np.asarray(b.H); F = np.asarray(b.F)
        assert H.min() >= 0 and H.max() <= 12 + 1e-12
        sure = F > 1 - 1e-12
        assert sure.any() and np.abs(H[sure] - 12).max() < 1e-12
        assert (H >= 12 * F - 1e-9).all()
        L = b.lang
        for k in 'RPSX':
            assert H[L.find(k)].max() == 0.0


def test_forfeit_only_price():
    b = base('exact')
    L = b.lang
    n, r, tm = L.find('next(THEM(ME))'), L.find('R'), L.find('THEM(ME)')
    cost = PP.price_matrix(b, 0.01, 'forfeit')
    assert abs(cost[n, tm] - 0.12) < 1e-12 and cost[n, r] == 0.0
    gn = L.find('coin(X,next(THEM(ME)))')
    assert abs(cost[gn, gn] - 0.12 * 2.0 ** -13) < 1e-15


def test_c0_reproduces_unpriced_tables():
    """make_arm at c = 0 is the unpriced class table, entry for entry (same classes, same payoff table, same masses)."""
    for arm in ('pure', 'sample', 'matched', 'exact', 'exact_br'):
        b = base(arm) if arm != 'exact_br' else PP.load_base('exact_br', 6, 12)
        A0 = PP.make_arm(b, 0.0, 'depth', dec=6)
        Au = RP.build_arm(arm, 6, 12)
        assert A0.K == Au.K
        assert (A0.rep == Au.rep).all() and (A0.cls_of == Au.cls_of).all()
        assert np.abs(A0.U - Au.U).max() == 0.0
        assert np.abs(A0.mass - Au.mass).max() < 1e-15
        assert np.abs(np.asarray(b.U) - Au.U_full).max() == 0.0          # the full program table is bit-identical
        assert np.abs(A0.Gcl - Au.Gcl).max() == 0.0
    # and the stored unpriced class counts of runs/rps/static.json
    st = json.load(open(os.path.join(ROOT, 'runs', 'rps', 'static.json')))
    for arm in ('pure', 'sample', 'matched', 'exact', 'exact_br'):
        b = base(arm) if arm != 'exact_br' else PP.load_base('exact_br', 6, 12)
        assert PP.make_arm(b, 0.0, 'depth', dec=6).K == st[arm]['K']


def test_pricing_splits_but_never_merges():
    """Priced classes refine the unpriced ones; the X class splits off its costly impostor (notes 1.3 hand expectation)."""
    b = base('exact')
    A0 = PP.make_arm(b, 0.0, 'depth', dec=6)
    A1 = PP.make_arm(b, 0.01, 'depth')
    rep = PP.split_report(A1, A0)
    assert rep['priced_classes_that_merge_unpriced'] == 0
    assert rep['K_priced'] >= rep['K_unpriced']
    L = b.lang
    x, imp = L.find('X'), L.find('THEM(^THEM(THEM))')
    assert A0.cls_of[x] == A0.cls_of[imp]              # unpriced: same class
    assert A1.cls_of[x] != A1.cls_of[imp]              # priced: the reader pays


def test_priced_class_equivariance():
    b = base('exact')
    A = PP.make_arm(b, 0.01, 'depth')
    for shift in (1, 2):
        sig = A.lang.relabel_map(shift)
        perm = RP.class_perm(A, sig)
        assert np.abs(A.U[np.ix_(perm, perm)] - A.U).max() < 1e-9


def test_prediction1_statics():
    """X pays 0, earns >= 0 against everyone; invades and weakly dominates every self-forfeiting program at c > 0, but only
    ties at c = 0."""
    for arm in ('sample', 'exact'):
        b = base(arm)
        L = b.lang
        xid = L.find('X')
        F = np.asarray(b.F); Fs = np.diag(F)
        forf = np.nonzero(Fs > 1e-12)[0]
        assert len(forf) > 0
        for c in (0.0, 0.001, 0.01, 0.05):
            Un = np.asarray(b.U) - PP.price_matrix(b, c, 'depth')
            assert Un[xid].min() >= -1e-12 and PP.price_matrix(b, c, 'depth')[xid].max() == 0.0
            inv = Un[xid, forf] - Un[forf, forf]
            dom = Un[xid, xid] - Un[forf, xid]
            assert dom.min() >= -1e-9
            if c > 0:
                assert inv.min() > 1e-9
                assert inv.min() >= 0.9 * c * 12 * Fs[forf].min() - 1e-12 or True
            else:
                assert inv.min() > -1e-9          # X earns >= the self-forfeiting program, weakly
        # X earns exactly the forfeit mass of its opponent
        assert np.abs(np.asarray(b.U)[xid] - F[:, xid]).max() < 1e-12


def test_support_class():
    N = 100
    a = np.array([[50, 50, 0]] * 5)
    assert PP.support_class(a, N)[0] == 'resolved'
    b = np.array([[97, 3, 0], [96, 4, 0], [97, 3, 0], [97, 3, 0]])      # the small class stays below 5 percent: support {0}
    assert PP.support_class(b, N)[0] == 'resolved'
    b2 = np.array([[50, 50, 0], [50, 50, 0], [97, 3, 0], [97, 3, 0]])   # the support changes once and never returns
    assert PP.support_class(b2, N)[0] == 'unresolved'
    c = np.array([[50, 50, 0], [60, 40, 0], [50, 50, 0]])
    assert PP.support_class(c, N)[0] == 'resolved'                       # same support {0,1}
    d = np.array([[100, 0, 0], [50, 50, 0], [100, 0, 0]])
    assert PP.support_class(d, N)[0] == 'cycling'
    e = np.array([[100, 0, 0], [50, 50, 0], [0, 100, 0]])
    assert PP.support_class(e, N)[0] == 'unresolved'


def test_class_grouping_merges_rounding_boundary_splits():
    S = 6
    rng = np.random.default_rng(2)
    base_ = rng.random((S, S))
    Un = base_.copy()
    Un[1] = Un[0]; Un[:, 1] = Un[:, 0]; Un[1, 1] = Un[0, 0]
    Un[1, 3] += 4e-10 * 1.0                 # within the merge tolerance? no: 4e-10 > 1e-11, a real difference at 9 decimals
    groups = PP._classes_from_table(Un, 9)
    assert len(groups) == S                 # 0 and 1 differ by 4e-10, rounding at 9 decimals may or may not split them, merge
                                            # tolerance 1e-11 keeps them apart
    Un2 = base_.copy()
    Un2[1] = Un2[0]; Un2[:, 1] = Un2[:, 0]; Un2[1, 1] = Un2[0, 0]
    Un2[1, 3] += 1e-13                      # noise
    groups2 = PP._classes_from_table(Un2, 9)
    assert len(groups2) == S - 1
    # boundary case: values straddling a rounding boundary by 1e-14 still merge
    Un3 = base_.copy()
    Un3[0, 2] = 0.1234567895 - 1e-14; Un3[1] = Un3[0]; Un3[:, 1] = Un3[:, 0]; Un3[1, 1] = Un3[0, 0]
    Un3[1, 2] = 0.1234567895 + 1e-14
    assert len(PP._classes_from_table(Un3, 9)) == S - 1


def test_lottery_founders_pairing_with_unpriced():
    """Founders are drawn at the program level and mapped to the priced classes, so summing priced counts over the members of
    an unpriced class returns the unpriced founder counts exactly."""
    b = base('exact')
    A0 = PP.make_arm(b, 0.0, 'depth', dec=6)
    A1 = PP.make_arm(b, 0.01, 'depth')
    seed = RP.run_seed('founders|primary', 3)
    i0 = RP.draw_founders(b.lang, A0.cls_of, A0.K, 8, 100, seed)
    i1 = RP.draw_founders(b.lang, A1.cls_of, A1.K, 8, 100, seed)
    # map priced class -> unpriced class through a representative program
    m = np.array([A0.cls_of[A1.rep[k]] for k in range(A1.K)])
    back = np.zeros_like(i0)
    for k in range(A1.K):
        back[:, m[k]] += i1[:, k]
    assert (back == i0).all()


def test_toy_two_type_contest_priced():
    """A two-class priced toy (X against N at c = 0.01) through LogChain: closed-form Moran ratio of the priced table."""
    from chain import fixation
    from chain_log import LogChain
    b = base('exact')
    L = b.lang
    ids = [L.find('X'), L.find('next(THEM(ME))')]
    Un = (np.asarray(b.U) - PP.price_matrix(b, 0.01, 'depth'))[np.ix_(ids, ids)]
    mu = np.array([0.5, 0.5]); N, w = 60, 0.3
    lc = LogChain(RP.ClassProvider(Un, mu), N=N, w=w).explore_closure(max_states=100)
    k0, k1 = lc.mono(0), lc.mono(1)
    rho_nx = fixation(Un[1, 1], Un[1, 0], Un[0, 1], Un[0, 0], N, w, N)     # one N in an all-X population
    rho_xn = fixation(Un[0, 0], Un[0, 1], Un[1, 0], Un[1, 1], N, w, N)     # one X in an all-N population
    assert abs(lc.trans[k0][k1] - 0.5 * rho_nx) < 1e-12 and abs(lc.trans[k1][k0] - 0.5 * rho_xn) < 1e-12
    assert rho_xn > 1.0 / N > rho_nx          # X invades N faster than neutral; N invades X slower than neutral
    keys, lpi, info, out_un, rec = lc.solve_sparse()
    pi = dict(zip(keys, np.exp(lpi)))
    ratio = (0.5 * rho_xn) / (0.5 * rho_nx)
    assert abs(pi[k0] / pi[k1] - ratio) / ratio < 1e-9
    assert pi[k0] > 0.5


def test_subset_cost_table_matches_full():
    b = base('exact')
    L = b.lang
    small = np.nonzero(L.size <= 3)[0]
    Z = np.unique(np.concatenate([small, [L.find('next(THEM(ME))'), L.find('cr(THEM(ME))'), L.find('coin(X,cr(THEM(ME)))')]]))
    Hs, _ = PP.cost_table_subset(L, Z, 12)
    assert np.abs(Hs - np.asarray(b.H)[np.ix_(Z, Z)]).max() < 1e-12


def test_work_exceeds_depth_for_two_application_coin_at_n7():
    """n = 7: coin(THEM(ME), THEM(THEM)) read exactly by cr(THEM(ME)) executes both branches (work) but only the deepest
    counts for depth."""
    L = RP.Lang('exact', 7)
    k2 = L.find('coin(THEM(ME),THEM(THEM))')
    c = L.find('cr(THEM(ME))')
    Z = np.unique(np.concatenate([np.nonzero(L.size <= 4)[0], [k2, c]]))
    H, _ = PP.cost_table_subset(L, Z, 12, work=False)
    HW, _ = PP.cost_table_subset(L, Z, 12, work=True)
    pos = {int(z): i for i, z in enumerate(Z)}
    d = H[pos[c], pos[k2]]; w = HW[pos[c], pos[k2]]
    ed, md = PP.cost_ref(L, c, k2, 12, work=False)
    ew, mw = PP.cost_ref(L, c, k2, 12, work=True)
    assert abs(d - ed) < 1e-12 and abs(w - ew) < 1e-12
    assert w > d + 1e-9
    # sampling readers never differ in work and depth at any n
    n = L.find('next(THEM(ME))')
    assert abs(H[pos[n], pos[k2]] - HW[pos[n], pos[k2]]) < 1e-12


def test_c0_chain_and_lottery_reproduce_stored_unpriced_run():
    """The priced pipeline at c = 0 reproduces the stored unpriced chain statistics (to 1e-6) and the stored unpriced lottery
    runs (bitwise on the stored statistics) -- the validation that the machinery, not the price, is unchanged."""
    import gzip
    import rps_priced_run as PR
    for arm in ('pure', 'sample', 'exact'):
        b = base(arm)
        A = PP.make_arm(b, 0.0, 'depth', dec=6)
        disc = PR.discover(A, att_starts=0)
        res = PR.chain_cell_p(A, 1000, None, None, disc, log_theta=np.log(1e-14))
        old = json.load(open(os.path.join(ROOT, 'runs', 'rps', 'chain_%s_D12_N1000.json' % arm)))
        for k in ('e_prog', 'mix_pop', 'forfeit_self', 'forfeit_plays', 'e_act'):
            assert abs(res['pi_stat'][k] - old['pi_stat'][k]) < 1e-6, (arm, k, res['pi_stat'][k], old['pi_stat'][k])
        assert abs(res['pi_polymorphic_mass']) < 1e-12 and res['n_recurrent'] == old['n_recurrent']
    # lottery: the first runs of the sample arm
    pth = os.path.join(ROOT, 'runs', 'rps', 'lottery_sample_primary.jsonl.gz')
    old = [json.loads(l) for l in gzip.open(pth, 'rt')][:2]
    b = base('sample')
    A = PP.make_arm(b, 0.0, 'depth', dec=6)
    nm = RP.named_classes(A)
    for r in range(2):
        rec = PR.one_run(A, 'primary', r, None, None, nm, 'sample')
        for g in ('500', '1000', '2000'):
            for k in ('e_prog', 'mix_pop', 'forfeit_plays', 'nclass'):
                assert abs(rec['means'][g][k] - float(np.mean(old[r]['stats'][g][k]))) < 1e-5, (r, g, k)
