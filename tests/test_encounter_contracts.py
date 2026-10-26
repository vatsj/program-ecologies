"""Tests for src/encounter_contracts.py: the two-stage evaluation on hand-built triples, genesis by hand (fair, unequal, wasteful,
disagreement islands, a mismatched migrant), BR against R, NR, hooks, replays, bundle copying, and the nu = 0 reproduction of
`many_islands.island_run` draw for draw."""
import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import encounter_contracts as EC
import many_islands as MI
import stable_sets as SS
import dollar3 as D

lo = D.local_of


@pytest.fixture(scope='module')
def arm():
    return EC.CArm()


@pytest.fixture(scope='module')
def ci(arm):
    return SS.const_index(arm.S.fs)


def const(ci, s, partner, d):
    return ci[lo(s, partner, d)]


def reader(arm, s, atom_slot, atom_act, a_true, a_false):
    """if (slot atom_slot plays local action atom_act) then a_true else a_false, a program of slot s (actions are local
    indices of slot s; atom_act is the local action index of slot atom_slot)."""
    jr = D.others(s).index(atom_slot)
    f = (((0, jr, atom_act),), (a_false, a_true))
    return arm.S.index[s][f]


def island(arm, R, trip):
    c = np.zeros((3, arm.K), np.int64)
    for s in range(3):
        c[s, trip[s]] = 100
    return R.init_island(c)


def tid(isl, s, prog=None):
    ST = isl.ST
    for i in range(ST[7][s]):
        t = ST[6][s, i]
        if prog is None or ST[1][s, t] == prog:
            return int(t)
    raise KeyError


def carrier(isl, s, has=True):
    ST = isl.ST
    for i in range(ST[7][s]):
        t = int(ST[6][s, i])
        if (ST[2][s, t] > 0) == has:
            return t
    raise KeyError


def pay6(code):
    return tuple(int(x) for x in EC.PAY6[code])


def test_nu0_reproduces_island_run(arm):
    """with nu = 0 and no exogenous events the engine reproduces the stored island kernel draw for draw"""
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    marm = MI.Arm('L'); marm.new_cache(22)
    rng = np.random.default_rng(7)
    for trial in range(4):
        init = np.stack([rng.multinomial(100, arm.laws[s]) for s in range(3)]).astype(np.int64)
        seed = 4000 + trial
        st0, g0, c0, _ = MI.island_run(marm.ctx(), marm.lc(32), MI.PAY, init, 100, MI.W, seed, 20002, np.empty(0), marm.cum, True)
        isl = R.init_island(init)
        st, g = R.run(isl, 20002, seed, 0.0)
        assert (st, g) == (st0, g0)
        assert np.array_equal(isl.counts_by_program(arm.K), c0)


def test_nu0_reproduces_island_run_with_arrivals(arm):
    """annealed arrivals are consumed in the stored order too"""
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    marm = MI.Arm('L'); marm.new_cache(22)
    rng = np.random.default_rng(11)
    for trial in range(3):
        init = np.stack([rng.multinomial(100, arm.laws[s]) for s in range(3)]).astype(np.int64)
        arr = MI.arrival_times(rng, 20)
        seed = 5000 + trial
        H = int(arr[-1]) + 5002
        st0, g0, c0, na0 = MI.island_run(marm.ctx(), marm.lc(64), MI.PAY, init, 100, MI.W, seed, H, arr, marm.cum, True)
        isl = R.init_island(init)
        X = [R.xrow(t, 0) for t in arr]
        st, g = R.run(isl, H, seed, 0.0, xrows=X)
        assert (st, g) == (st0, g0)
        assert np.array_equal(isl.counts_by_program(arm.K), c0)


def test_two_stage_contract_fires_and_does_not(arm, ci):
    """fair island of constants; the contract (key = the fair profile, slot 0 plays (2,2/3), slot 2 plays (0,1/3)) fires only
    when both carriers meet; a lone carrier meets disagreement; a non-carrier slot 0 keeps the pair {0,1}"""
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    trip = [const(ci, 0, 1, 1), const(ci, 1, 0, 1), const(ci, 2, 0, 1)]
    isl = island(arm, R, trip)
    t = [tid(isl, s) for s in range(3)]
    p, c2 = EC.encounter(R, isl, t)
    assert p == c2 and pay6(c2) == (3, 3, 0)
    ok, p, fills, pb, _ = EC.propose_check(R, isl, t, 0b101, {0: lo(0, 2, 2), 2: lo(2, 0, 0)})
    assert ok                                              # accepted even against a constant responder (slot 1's loss untested)
    EC.install_python(R, isl, t, 0b101, {0: lo(0, 2, 2), 2: lo(2, 0, 0)}, p)
    types = isl.types()
    assert sorted(c for _, c, _ in types[0]) == [1, 99] and sorted(c for _, c, _ in types[2]) == [1, 99]
    c0, c1_, c2_ = carrier(isl, 0), carrier(isl, 1, False), carrier(isl, 2)
    n0, n2 = carrier(isl, 0, False), carrier(isl, 2, False)
    p1, code = EC.encounter(R, isl, [c0, c1_, c2_]); assert p1 == p and pay6(code) == (4, 0, 2)
    p1, code = EC.encounter(R, isl, [c0, c1_, n2]); assert pay6(code) == (0, 0, 0)
    p1, code = EC.encounter(R, isl, [n0, c1_, c2_]); assert pay6(code) == (3, 3, 0)
    p1, code = EC.encounter(R, isl, [n0, c1_, n2]); assert pay6(code) == (3, 3, 0)


def test_key_mismatch_plays_program(arm, ci):
    """a carrier whose key is not the encounter's stage-1 profile plays its program"""
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    trip = [const(ci, 0, 1, 1), const(ci, 1, 0, 1), const(ci, 2, 0, 1)]
    isl = island(arm, R, trip)
    t = [tid(isl, s) for s in range(3)]
    p, c2 = EC.encounter(R, isl, t)
    EC.install_python(R, isl, t, 0b001, {0: lo(0, 2, 2)}, p + 1 if p < 728 else p - 1)
    car = carrier(isl, 0)
    p1, code = EC.encounter(R, isl, [car, t[1], t[2]])
    assert code == c2


def test_responder_reacts(arm, ci):
    """an accommodator in slot 1 ('if slot 0 plays (1,2/3) then (0,1/3) else (0,1/2)') answers slot 0's fill; R accepts the
    proposal S={0}: (1,2/3), NR rejects it (the responder holds its stage-1 action: 4 + 3 > 6), BR rejects it (with two
    uncommitted responders the pure equilibria of the remaining game include slots 1 and 2 pairing with each other, which leaves
    slot 0 with nothing: the robust-acceptance rule is stricter than R here)"""
    acc = reader(arm, 1, 0, lo(0, 1, 2), lo(1, 0, 0), lo(1, 0, 1))
    trip = [const(ci, 0, 1, 1), acc, const(ci, 2, 0, 1)]
    for mode, expect in ((EC.ACC_R, True), (EC.ACC_NR, False), (EC.ACC_BR, False)):
        R = EC.Runner(arm, EC.make_P(nu=0.0, acc=mode))
        isl = island(arm, R, trip)
        t = [tid(isl, s) for s in range(3)]
        ok, p, fills, pb, _ = EC.propose_check(R, isl, t, 0b001, {0: lo(0, 1, 2)})
        assert ok == expect, mode
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    isl = island(arm, R, trip)
    t = [tid(isl, s) for s in range(3)]
    ok, p, fills, pb, _ = EC.propose_check(R, isl, t, 0b001, {0: lo(0, 1, 2)})
    EC.install_python(R, isl, t, 0b001, {0: lo(0, 1, 2)}, p)
    car = carrier(isl, 0)
    _, code = EC.encounter(R, isl, [car, t[1], t[2]])
    assert pay6(code) == (4, 2, 0)


def test_br_differs_from_r_on_stubborn_responder(arm, ci):
    """a stubborn constant (0,1/2) in slot 1 and a committed slot 2 (it carries an entry for the key, so only slot 1 is an
    uncommitted responder): R rejects S={0}:(1,2/3); BR accepts (slot 1's unique best reply is (0,1/3)) yet the installed contract
    earns slot 0 nothing against the stubborn constant"""
    trip = [const(ci, 0, 1, 1), const(ci, 1, 0, 1), const(ci, 2, 0, 1)]
    res = {}
    for mode in (EC.ACC_R, EC.ACC_BR):
        R = EC.Runner(arm, EC.make_P(nu=0.0, acc=mode))
        isl = island(arm, R, trip)
        t = [tid(isl, s) for s in range(3)]
        p, _ = EC.encounter(R, isl, t)
        EC.install_python(R, isl, t, 0b100, {2: lo(2, 0, 1)}, p)          # slot 2 committed to its own action
        t[2] = carrier(isl, 2)
        ok, p, fills, pb, _ = EC.propose_check(R, isl, t, 0b001, {0: lo(0, 1, 2)})
        res[mode] = ok
    assert res[EC.ACC_R] is False and res[EC.ACC_BR] is True
    R = EC.Runner(arm, EC.make_P(nu=0.0, acc=EC.ACC_BR))
    isl = island(arm, R, trip)
    t = [tid(isl, s) for s in range(3)]
    p, _ = EC.encounter(R, isl, t)
    EC.install_python(R, isl, t, 0b100, {2: lo(2, 0, 1)}, p)
    t[2] = carrier(isl, 2)
    EC.install_python(R, isl, t, 0b001, {0: lo(0, 1, 2)}, p)
    car = carrier(isl, 0)
    _, code = EC.encounter(R, isl, [car, t[1], t[2]])
    assert pay6(code)[0] == 0                                # the BR-accepted contract delivers 0 with a program responder


def test_br_exec_plays_best_reply(arm, ci):
    """in the execution-consistent BR cell the uncommitted responder plays the best reply (here with slot 2 committed)"""
    trip = [const(ci, 0, 1, 1), const(ci, 1, 0, 1), const(ci, 2, 0, 1)]
    R = EC.Runner(arm, EC.make_P(nu=0.0, acc=EC.ACC_BR, exe=EC.EXE_BR))
    isl = island(arm, R, trip)
    t = [tid(isl, s) for s in range(3)]
    p, _ = EC.encounter(R, isl, t)
    EC.install_python(R, isl, t, 0b100, {2: lo(2, 0, 1)}, p)
    t[2] = carrier(isl, 2)
    ok, p, fills, pb, _ = EC.propose_check(R, isl, t, 0b001, {0: lo(0, 1, 2)})
    assert ok
    EC.install_python(R, isl, t, 0b001, {0: lo(0, 1, 2)}, p)
    car = carrier(isl, 0)
    _, code = EC.encounter(R, isl, [car, t[1], t[2]])
    assert pay6(code) == (4, 2, 0)


def test_genesis_fair_island_two_accepted_proposals(arm, ci):
    """notes 1.2: on a fair island of constants exactly two proposals of |S| = 2 are accepted, none of |S| = 1 or 3; the
    exhaustive oracle gives 2/560 per genesis draw"""
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    trip = [const(ci, 0, 1, 1), const(ci, 1, 0, 1), const(ci, 2, 0, 1)]
    isl = island(arm, R, trip)
    out = EC.acceptance_profile(R, isl)
    assert out[3] == 0 and out[5] == 0 and out[4] == 2
    assert abs(out[:3].sum() - 2 / 560) < 1e-12


def test_genesis_unequal_island(arm, ci):
    """notes 1.3: unequal island (4,2,0): S = {1,2} proposing (2,1/2),(1,1/2) is accepted against a constant dictator; S = {1}
    alone is rejected against a constant excluded slot and accepted against a reader that answers"""
    trip = [const(ci, 0, 1, 2), const(ci, 1, 0, 0), const(ci, 2, 0, 1)]
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    isl = island(arm, R, trip)
    t = [tid(isl, s) for s in range(3)]
    _, c = EC.encounter(R, isl, t)
    assert pay6(c) == (4, 2, 0)
    ok, *_ = EC.propose_check(R, isl, t, 0b110, {1: lo(1, 2, 1), 2: lo(2, 1, 1)}); assert ok
    ok, *_ = EC.propose_check(R, isl, t, 0b010, {1: lo(1, 2, 1)}); assert not ok
    rd = reader(arm, 2, 1, lo(1, 2, 1), lo(2, 1, 1), lo(2, 0, 1))
    isl2 = island(arm, R, [trip[0], trip[1], rd])
    t2 = [tid(isl2, s) for s in range(3)]
    ok, *_ = EC.propose_check(R, isl2, t2, 0b010, {1: lo(1, 2, 1)}); assert ok


def test_genesis_wasteful_and_disagreement(arm, ci):
    """notes 1.4: wasteful (2,2,0): S = {0} proposing (1,1/2) or (1,2/3) is accepted alone; disagreement: S = {0} proposing (1,1/3)"""
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    isl = island(arm, R, [const(ci, 0, 1, 0), const(ci, 1, 0, 0), const(ci, 2, 0, 0)])
    t = [tid(isl, s) for s in range(3)]
    _, c = EC.encounter(R, isl, t); assert pay6(c) == (2, 2, 0)
    assert EC.propose_check(R, isl, t, 0b001, {0: lo(0, 1, 1)})[0]
    assert EC.propose_check(R, isl, t, 0b001, {0: lo(0, 1, 2)})[0]
    isl = island(arm, R, [const(ci, 0, 1, 2), const(ci, 1, 0, 2), const(ci, 2, 1, 1)])
    t = [tid(isl, s) for s in range(3)]
    _, c = EC.encounter(R, isl, t); assert pay6(c) == (0, 0, 0)
    assert EC.propose_check(R, isl, t, 0b001, {0: lo(0, 1, 0)})[0]
    assert not EC.propose_check(R, isl, t, 0b001, {0: lo(0, 1, 1)})[0]


def test_genesis_mismatched_migrant(arm, ci):
    """notes 1.4: a migrant constant (2,1/2) in slot 1 of the fair island makes every one of its encounters a disagreement; S = {1}
    proposing (0,1/2) is accepted (0 -> 3) and the repaired migrant plays the resident's action"""
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    trip = [const(ci, 0, 1, 1), const(ci, 1, 0, 1), const(ci, 2, 0, 1)]
    isl = island(arm, R, trip)
    mig = const(ci, 1, 2, 1)
    tm = [EC.inject(R, isl, 1, mig)]
    t = [tid(isl, 0), tm[0], tid(isl, 2)]
    _, c = EC.encounter(R, isl, t); assert pay6(c) == (0, 0, 0)
    ok, p, fills, pb, _ = EC.propose_check(R, isl, t, 0b010, {1: lo(1, 0, 1)})
    assert ok
    EC.install_python(R, isl, t, 0b010, {1: lo(1, 0, 1)}, p)
    car = carrier(isl, 1)
    _, c = EC.encounter(R, isl, [t[0], car, t[2]]); assert pay6(c) == (3, 3, 0)


def test_replay_matches_prediction_grand_and_replacement(arm, ci):
    """an accepted genesis replayed after installation reproduces the predicted outcome (here a grand-coalition proposal on a
    disagreement island) and a second installation with the same key replaces the carrier's entry"""
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    isl = island(arm, R, [const(ci, 0, 1, 2), const(ci, 1, 0, 2), const(ci, 2, 1, 1)])
    t = [tid(isl, s) for s in range(3)]
    na = {0: lo(0, 3, 0), 1: lo(1, 3, 0), 2: lo(2, 3, 0)}
    ok, p, fills, pb, _ = EC.propose_check(R, isl, t, 0b111, na)
    assert ok                                              # (2,2,2) beats (0,0,0) for everyone
    EC.install_python(R, isl, t, 0b111, na, p)
    cars = [carrier(isl, s) for s in range(3)]
    _, code = EC.encounter(R, isl, cars)
    assert pay6(code) == (2, 2, 2)
    ok2, p2, fills2, pb2, _ = EC.propose_check(R, isl, cars, 0b001, {0: lo(0, 3, 1)})
    assert p2 == p and (fills2 >= 0).all()                  # the carriers' fills are committed in the genesis encounter
    EC.install_python(R, isl, cars, 0b001, {0: lo(0, 3, 1)}, p)
    for e in [e for (_, c, e) in isl.types()[0] if e]:
        assert len([k for k, f, b in e if k == p]) <= 1    # at most one entry per key


def test_hook_blocking(arm):
    """arm H: a program that reaches no hook cannot sign; the hooked grammar has hooked and unhooked constants as different programs"""
    harm = EC.CArm(hooked=True)
    assert harm.K > arm.K
    hooked = [x for x in range(harm.K) if harm.hk[0, x].max() >= 0 and not harm.S.fs[x][0]]
    plain = [x for x in range(harm.K) if harm.hk[0, x].max() < 0 and not harm.S.fs[x][0]]
    assert len(hooked) == 18 and len(plain) == 9
    ci_ = {harm.S.fs[x][1][0]: x for x in plain}
    trip = [ci_[lo(0, 1, 1)], ci_[lo(1, 0, 1)], ci_[lo(2, 0, 1)]]
    R = EC.Runner(harm, EC.make_P(nu=0.0, hook=EC.HOOK_H))
    c = np.zeros((3, harm.K), np.int64)
    for s in range(3): c[s, trip[s]] = 100
    isl = R.init_island(c)
    out = EC.acceptance_profile(R, isl)
    assert out[:6].sum() == 0
    R2 = EC.Runner(harm, EC.make_P(nu=0.0, hook=EC.HOOK_TOP))
    isl2 = R2.init_island(c)
    out2 = EC.acceptance_profile(R2, isl2)
    assert abs(out2[:3].sum() - 2 / 560) < 1e-12
    c = np.zeros((3, harm.K), np.int64)
    for s, a in enumerate((lo(0, 1, 1), lo(1, 0, 1), lo(2, 0, 1))):
        c[s, [x for x in hooked if harm.S.fs[x][1][0] % 9 == a][0]] = 100
    isl3 = R.init_island(c)
    out3 = EC.acceptance_profile(R, isl3)
    assert abs(out3[:3].sum() - 2 / 560) < 1e-12


def test_arm_C_copy_draws_existing_bundle(arm, ci):
    """a copied proposal is an actual surviving bundle offered in an encounter whose stage-1 profile equals its key"""
    R = EC.Runner(arm, EC.make_P(nu=0.0, copy=1.0))
    trip = [const(ci, 0, 1, 1), const(ci, 1, 0, 1), const(ci, 2, 0, 1)]
    isl = island(arm, R, trip)
    t = [tid(isl, s) for s in range(3)]
    na = {0: lo(0, 2, 2), 2: lo(2, 0, 0)}
    ok, p, fills, pb, _ = EC.propose_check(R, isl, t, 0b101, na)
    EC.install_python(R, isl, t, 0b101, na, p)
    newa = np.zeros(3, np.int64); ts = np.zeros(3, np.int64); stat = np.zeros(EC.ST_LEN, np.int64)
    np.random.seed(1)
    smask, okc = EC.pick_copy(R.A, R.arm.c1, isl.ST, 100, newa, ts, stat)
    assert okc and smask == 0b101 and newa[0] == lo(0, 2, 2) and newa[2] == lo(2, 0, 0)
    isl0 = island(arm, R, trip)
    stat = np.zeros(EC.ST_LEN, np.int64)
    smask, okc = EC.pick_copy(R.A, R.arm.c1, isl0.ST, 100, newa, ts, stat)
    assert not okc and stat[EC.ST_UNMATCHED] == 1


def test_arm_S_installs_every_proposal(arm, ci):
    """with the filter off every genesis attempt installs on its signers"""
    R = EC.Runner(arm, EC.make_P(nu=2.0, filt=0))
    trip = [const(ci, 0, 1, 1), const(ci, 1, 0, 1), const(ci, 2, 0, 1)]
    isl = island(arm, R, trip)
    R.run(isl, 20, 9, 0.0)
    s = R.stat
    assert s[EC.ST_ATT_S:EC.ST_ATT_S + 3].sum() == s[EC.ST_ACC_S:EC.ST_ACC_S + 3].sum() > 0


def test_cap_eviction(arm, ci):
    """the entry list is capped; the oldest entry is evicted first"""
    R = EC.Runner(arm, EC.make_P(nu=0.0, cap=2))
    trip = [const(ci, 0, 1, 1), const(ci, 1, 0, 1), const(ci, 2, 0, 1)]
    isl = island(arm, R, trip)
    t = [tid(isl, s) for s in range(3)]
    for key in (10, 11, 12):
        EC.install_python(R, isl, t, 0b001, {0: 3}, key)
        t[0] = carrier(isl, 0)                             # the (single) carrier receives the next entry
    ents = [e for (_, c, e) in isl.types()[0] if e]
    assert len(ents) == 1 and [k for k, f, b in ents[0]] == [11, 12]


def check_invariants(R, isl):
    ST = isl.ST
    cnt, tprog, tn, tkey, tfil, tbun, pres, npres, pos, ser, F, mi, mf = ST
    A = R.A; arm = R.arm
    for s in range(3):
        assert cnt[s].sum() == 100
        live = {int(pres[s, i]) for i in range(npres[s])}
        assert len(live) == npres[s]
        for t in range(EC.TM):
            if t in live:
                assert cnt[s, t] > 0 and tprog[s, t] >= 0 and pos[s, t] >= 0 and pres[s, pos[s, t]] == t
            else:
                assert cnt[s, t] == 0 and tprog[s, t] < 0 and pos[s, t] < 0
        # entry lists respect the cap and have distinct keys
        for t in live:
            ks = [int(tkey[s, t, e]) for e in range(tn[s, t])]
            assert len(ks) == len(set(ks)) <= int(R.P[EC.P_CAP])
    # direct evaluation agrees with the cache, F agrees with a full recomputation
    arm.clear_c2()
    for i0 in range(npres[0]):
        for i1 in range(npres[1]):
            for i2 in range(npres[2]):
                t0, t1, t2 = int(pres[0, i0]), int(pres[1, i1]), int(pres[2, i2])
                a = EC.tcode(A, arm.c1, arm.c2, ST, R.P, t0, t1, t2)
                b = EC.enc2_compute(A, arm.c1, ST, R.P, t0, t1, t2)
                assert a == b
    if mi[EC.MI_NEUTRAL] == 0:
        for s in range(3):
            for i in range(npres[s]):
                k = int(pres[s, i])
                assert abs(F[s, k] - EC.fit_type(A, arm.c1, arm.c2, ST, R.P, s, k)) < 1e-6 * 1e4
    else:
        # neutral: every present triple gives the same payoff vector
        vals = set()
        for i0 in range(npres[0]):
            for i1 in range(npres[1]):
                for i2 in range(npres[2]):
                    c = EC.tcode(A, arm.c1, arm.c2, ST, R.P, int(pres[0, i0]), int(pres[1, i1]), int(pres[2, i2]))
                    vals.add(pay6(c))
        assert len(vals) == 1


@pytest.mark.parametrize('kw', [dict(), dict(acc=EC.ACC_NR), dict(acc=EC.ACC_BR), dict(acc=EC.ACC_BR, exe=EC.EXE_BR),
                                dict(bcast=9), dict(filt=0), dict(copy=0.5), dict(cap=2)])
def test_invariants_random_runs(arm, kw):
    """population and table invariants, cache = direct evaluation, F = full recomputation, along random runs with genesis from
    polymorphic founders"""
    R = EC.Runner(arm, EC.make_P(nu=2.0, **kw))
    rng = np.random.default_rng(3)
    for trial in range(3):
        init = np.stack([rng.multinomial(100, arm.laws[s]) for s in range(3)]).astype(np.int64)
        isl = R.init_island(init)
        t = 0.0
        for rnd in range(4):
            R.run(isl, 500, 100 * trial + rnd, t); t += 500
            check_invariants(R, isl)


def test_invariants_hooked_arm():
    harm = EC.CArm(hooked=True)
    for hook in (EC.HOOK_H, EC.HOOK_TOP):
        R = EC.Runner(harm, EC.make_P(nu=2.0, hook=hook))
        rng = np.random.default_rng(5)
        init = np.stack([rng.multinomial(100, harm.laws[s]) for s in range(3)]).astype(np.int64)
        isl = R.init_island(init)
        R.run(isl, 800, 17, 0.0)
        check_invariants(R, isl)
        assert R.stat[EC.ST_ATT_S:EC.ST_ATT_S + 3].sum() > 0


def test_two_responders_nested_substitution(arm, ci):
    """S = {0} with two responders that read: slot 1 answers slot 0's fill, slot 2 answers slot 1's answer (the substitution
    reaches nested simulation depth)"""
    acc1 = reader(arm, 1, 0, lo(0, 1, 2), lo(1, 0, 0), lo(1, 0, 1))          # if slot 0 plays (1,2/3) then (0,1/3) else (0,1/2)
    rd2 = reader(arm, 2, 1, lo(1, 0, 0), lo(2, 1, 2), lo(2, 0, 1))           # if slot 1 plays (0,1/3) then (1,2/3) else (0,1/2)
    trip = [const(ci, 0, 1, 1), acc1, rd2]
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    isl = island(arm, R, trip)
    t = [tid(isl, s) for s in range(3)]
    p, c2 = EC.encounter(R, isl, t)
    assert (c2 // 81, (c2 // 9) % 9, c2 % 9) == (lo(0, 1, 1), lo(1, 0, 1), lo(2, 0, 1))      # stage 1: fair pair, slot 2 offers 0
    ok, p, fills, pb, _ = EC.propose_check(R, isl, t, 0b001, {0: lo(0, 1, 2)})
    EC.install_python(R, isl, t, 0b001, {0: lo(0, 1, 2)}, p)
    car = carrier(isl, 0)
    _, code = EC.encounter(R, isl, [car, t[1], t[2]])
    # slot 0 plays (1,2/3); slot 1 answers (0,1/3); slot 2 reads slot 1's answer and plays (1,2/3) (not (0,1/2))
    assert (code // 81, (code // 9) % 9, code % 9) == (lo(0, 1, 2), lo(1, 0, 0), lo(2, 1, 2))
    assert ok


def test_acceptance_monte_carlo_matches_oracle(arm, ci):
    """the genesis draws (uniform individuals, coalition, profile) accept with the oracle's probability on a hand-built island"""
    R = EC.Runner(arm, EC.make_P(nu=0.0))
    acc = reader(arm, 1, 0, lo(0, 1, 2), lo(1, 0, 0), lo(1, 0, 1))
    for trip in ([const(ci, 0, 1, 1), const(ci, 1, 0, 1), const(ci, 2, 0, 1)],
                 [const(ci, 0, 1, 0), const(ci, 1, 0, 0), const(ci, 2, 0, 0)],
                 [const(ci, 0, 1, 1), acc, const(ci, 2, 0, 1)]):
        isl = island(arm, R, trip)
        out = EC.acceptance_profile(R, isl)
        pexp = out[:3].sum()
        n = 40000
        hits = 0
        act = np.arange(3); apos = np.arange(3)
        np.random.seed(5)
        stat0 = np.zeros(EC.ST_LEN, np.int64)
        for i in range(n):
            ST = tuple(a.copy() for a in isl.ST)
            R.arm.clear_c2()
            EC.genesis_attempt(R.A, R.arm.c1, R.arm.c2, ST, R.P, act.copy(), apos.copy(), 0, 100, stat0, isl.trk.copy(), 0.0, False)
        acc_n = int(stat0[EC.ST_ACC_S:EC.ST_ACC_S + 3].sum())
        # binomial interval, 4 sigma
        sd = (pexp * (1 - pexp) / n) ** 0.5
        assert abs(acc_n / n - pexp) < 4 * sd + 1e-9, (acc_n / n, pexp)
