"""Tests for hooks, Part W2 (src/hooks_w2*.py): open keys in the PD (notes/hooks-w2.md §1.1) and union contracts in the
union game (§1.4, §1.5).  Checks: the open predicate and its fills, the hand equivalences (an open promise on
HOOK(t, D) is FairBot), soundness of open fills, the open contract acceptance on hand cases, the strict variant test,
and the reproduction of Part W's stored rows with the open flags off."""
import os, sys, json, gzip
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import hooks_w2 as H
import hooks_w2_kern as K

ROOT = os.path.join(os.path.dirname(__file__), '..')
ALL = np.ones((4, 4), np.bool_)
NONE_ACTIVE = np.zeros((4, 4), np.bool_)
OPEN0, OPEN1 = 8, 9


@pytest.fixture(scope='module')
def hk():
    return H.Lang(6, hooks=True)


def spec(fills, tags, active=ALL, recency=0, ctx=-1):
    f = np.zeros(4, np.int64); f[:len(fills)] = fills
    return H.spec_of(f, len(fills), tags, active, recency, ctx)


def play(L, bx, sx, by, sy):
    a, b, _, _ = H.eval_match(*L.arrays(), L.iC, L.iD, bx, sx, sx, sx, by, sy, sy, sy)
    return a, b


def base(L, name):
    return L.names.index(name)


def promise(t=0):
    """The open promise: cooperate with any partner that provably cooperates with me."""
    return H.fcode(1, t, H.BEH, H.WRITTEN, OPEN1)


# ------------------------------------------------------------------ the open predicate
def test_beh_ok_keys():
    for beta in range(8):
        assert H.beh_ok(beta, beta) and not H.beh_ok((beta + 1) % 8, beta)       # keys 0-7: the class itself
        assert H.beh_ok(OPEN1, beta) == bool(beta & 4)                           # key 9: bit 2 set
        assert H.beh_ok(OPEN0, beta) == (not (beta & 4))                         # key 8: bit 2 clear


def test_open_promise_is_fairbot(hk):
    hD = base(hk, 'HOOK(0,D)')
    sp = spec([promise()], 1)
    assert sp != 0
    # an open promise on HOOK(0, D) cooperates iff the partner provably cooperates with it
    assert play(hk, hD, sp, hk.bD, 0) == (0, 0)          # DefectBot: never provably cooperates
    assert play(hk, hD, sp, hk.bC, 0) == (1, 1)          # ALLC: provably cooperates
    assert play(hk, hD, sp, hk.FB, 0) == (1, 1)          # FairBot: Loeb
    assert play(hk, hD, sp, hD, 0) == (0, 0)             # the unfilled hook defects
    assert play(hk, hD, sp, hD, sp) == (1, 1)            # two promises cooperate by Loeb
    # identical behaviour to the plain FairBot against every plain program
    for i in range(len(hk.base)):
        assert play(hk, hD, sp, i, 0)[0] == play(hk, hk.FB, 0, i, 0)[0] or hk.b_tags[i] > 0


def test_open_promise_on_allc_hook_is_allc(hk):
    hC = base(hk, 'HOOK(0,C)')
    sp = spec([promise()], 1)
    assert play(hk, hC, sp, hk.bD, 0) == (1, 0)           # the idle fill leaves HOOK(0, C) an ALLC sucker


def test_open_grudge_on_allc_hook_is_fairbot(hk):
    hC = base(hk, 'HOOK(0,C)')
    sp = spec([H.fcode(0, 0, H.BEH, H.WRITTEN, OPEN0)], 1)     # defect against partners who do not provably cooperate
    assert play(hk, hC, sp, hk.bD, 0) == (0, 0)
    assert play(hk, hC, sp, hk.bC, 0) == (1, 1)
    assert play(hk, hC, sp, hk.FB, 0) == (1, 1)
    hD = base(hk, 'HOOK(0,D)')
    sp2 = spec([H.fcode(0, 0, H.BEH, H.WRITTEN, OPEN0)], 1)
    assert play(hk, hD, sp2, hk.bC, 0) == (0, 1)           # H_D with that grudge stays DefectBot (exploits ALLC)


def test_open_fills_ignore_lineage(hk):
    fl = [promise()]
    f = np.zeros(4, np.int64); f[0] = fl[0]
    specs = {H.spec_of(f, 1, 1, ALL, 0, c) for c in (-1, 0, 7, 12345)}
    assert len(specs) == 1


def test_open_fills_sound_against_provers(hk):
    """No fill, open or otherwise, lets a program exploit a sound prover (Lemma 0 still holds)."""
    rng = np.random.default_rng(7)
    cands = [i for i in range(len(hk.base)) if hk.b_tags[i] > 0]
    BOX1 = hk.bidx[hk.L.op((0, 1, 0))] if False else None
    provers = [hk.FB]
    for _ in range(4000):
        x = int(rng.choice(cands))
        tg = int(hk.b_tags[x])
        fl = []
        for _ in range(int(rng.integers(1, 5))):
            t = [0, 1][int(rng.integers(2))]
            if not (tg >> t) & 1:
                continue
            sc = int(rng.choice([0, 1, 2, 3, 3, 3]))
            key = {0: 0, 1: 0, 2: int(rng.integers(50)), 3: int(rng.choice([OPEN0, OPEN1, int(rng.integers(8))]))}[sc]
            fl.append(H.fcode(int(rng.integers(2)), t, sc, H.WRITTEN, key))
        if not fl:
            continue
        f = np.zeros(4, np.int64); f[:len(fl)] = fl
        ctx = int(rng.integers(50))
        s0 = H.spec_of(f, len(fl), tg, ALL, 0, -1); s1 = H.spec_of(f, len(fl), tg, ALL, 0, ctx)
        for p in provers:
            a, b, _, _ = H.eval_match(*hk.arrays(), hk.iC, hk.iD, x, s0, s1, s0, p, 0, 0, 0)
            assert not (a == 0 and b == 1)


# ------------------------------------------------------------------ contracts, writes, variants
def _types(hk, names):
    T, tdict, ev = H.new_tables(1000)
    ids = []
    for k, nm in enumerate(names):
        ids.append(H.get_type(T, tdict, hk.b_tags, ALL, 0, base(hk, nm), k, np.zeros(4, np.int64), 0))
    return T, tdict, ev, ids


def _attempt(hk, names, open_c):
    T, tdict, ev, ids = _types(hk, names)
    res = np.zeros(2, np.int64); ctr = np.zeros(24, np.int64)
    K._contract(T, tdict, hk.arrays(), ev, hk.b_tags, hk.iC, hk.iD, ALL, ALL, 0, H.PDPAY, ids[0], ids[1], ctr, res, open_c)
    return T, ids, res, ctr


def test_open_contract_two_defaulting_hooks(hk):
    T, ids, res, ctr = _attempt(hk, ['HOOK(0,D)', 'HOOK(0,D)'], 1)
    assert res[0] >= 0 and res[1] >= 0                        # (D, D) -> (C, C): accepted
    for t in res:
        d = [H.f_scope(int(T[2][t, j])) for j in range(int(T[3][t]))]
        keys = [H.f_key(int(T[2][t, j])) for j in range(int(T[3][t]))]
        assert d == [H.BEH] and keys == [OPEN1] and H.f_action(int(T[2][t, 0])) == 1
    assert ctr[11] == 1 and ctr[7] == 1


def test_open_contract_rejects_exploiter_vs_sucker(hk):
    T, ids, res, ctr = _attempt(hk, ['HOOK(0,D)', 'HOOK(0,C)'], 1)
    assert res[0] == -1 and res[1] == -1                      # the defector would lose 1: Pareto fails


def test_lineage_contract_unchanged(hk):
    T, ids, res, ctr = _attempt(hk, ['HOOK(0,D)', 'HOOK(0,D)'], 0)
    assert res[0] >= 0 and res[1] >= 0
    t = res[0]
    assert H.f_scope(int(T[2][t, 0])) == H.HIST and H.f_key(int(T[2][t, 0])) == 1       # keyed on the partner's lineage


def test_strict_variant_test(hk):
    T, tdict, ev, ids = _types(hk, ['HOOK(0,D)'])
    a = ids[0]
    f1 = np.zeros(4, np.int64); f1[0] = promise()
    f2 = np.zeros(4, np.int64); f2[0] = promise(); f2[1] = H.fcode(0, 0, H.HIST, H.WRITTEN, 9)
    b = H.get_type(T, tdict, hk.b_tags, ALL, 0, base(hk, 'HOOK(0,D)'), 0, f1, 1)
    c = H.get_type(T, tdict, hk.b_tags, ALL, 0, base(hk, 'HOOK(0,D)'), 0, f2, 2)
    Kb = np.zeros(8, np.int64)
    assert K._variant_keys(T, ALL, b, c, Kb, 1) >= 0          # differ only in a history fill
    f3 = np.zeros(4, np.int64); f3[0] = H.fcode(1, 0, H.ROLE, H.SEEDED, 0)
    d = H.get_type(T, tdict, hk.b_tags, ALL, 0, base(hk, 'HOOK(0,D)'), 0, f3, 1)
    assert K._variant_keys(T, ALL, b, d, Kb, 1) == -1         # differ in a non-history fill


def test_reproduces_part_w_stored_rows_with_flags_off():
    """With the open flags off, a short run of this module's `maximal` cell reproduces Part W's stored rows at the
    stored generations (island P(C,C) per island, types, held fills)."""
    import hooks_w2_run as R
    stored = {r['rep']: r for r in json.load(gzip.open(os.path.join(ROOT, 'runs', 'hooks_w', 'maximal.json.gz')))}
    row = R.run_one('maximal', 0, gens=25)
    by_gen = {t['gen']: t for t in stored[0]['ts']}
    assert [t['gen'] for t in row['ts']] == [0, 10, 25]
    for t in row['ts']:
        assert t['isl_pcc'] == by_gen[t['gen']]['isl_pcc']
        assert t['types'] == by_gen[t['gen']]['types']
        assert t['held'] == by_gen[t['gen']]['held']


# ================================================================== the union game (notes §1.4, §1.5)
import union as U
import hooks_w2_sog as S
import hooks_w2_sog_kern as SK
import hooks_w2_sog_run as SR


@pytest.fixture(scope='module')
def sg():
    return S.SogLang(hooks=True)


def _slot_types(sg, boss_prog, wa, wb, boss_fills=(), wa_fills=(), wb_fills=()):
    T, tdict, ev = SR.new_tables(2000)
    ids = []
    for s_, (prog, lin, fl) in enumerate(((boss_prog, 100, boss_fills), (wa, 101, wa_fills), (wb, 102, wb_fills))):
        f = np.zeros(4, np.int64); f[:len(fl)] = fl
        ids.append(SK.get_type(T, tdict, sg.htags, sg.wtag, ALL, 0, s_, prog, lin, f, len(fl)))
    return T, tdict, ev, ids


def _code(sg, T, ev, ids):
    RS = S.RSZ
    return int(SK.triple_code(T, sg.arrays(), U.TT, ev, ALL, 0, ids[0], ids[1], ids[2], np.zeros(RS, np.int8),
                              np.zeros(RS, np.int8), np.zeros(RS, np.int8), np.zeros((3, RS), np.int8)) & 63)


def _attempt_union(sg, T, tdict, ev, ids, mode, role=0, pb=0):
    RS = S.RSZ
    PAY, SUMT = SR.tables()
    cfg = np.zeros(13, np.int64); cfg[10] = mode; cfg[11] = role; cfg[12] = pb
    ctr = np.zeros(24, np.int64); ust = np.zeros(40, np.int64); res = np.zeros(3, np.int64)
    code = _code(sg, T, ev, ids)
    np.random.seed(1)
    SK._union(T, tdict, sg.htags, sg.wtag, sg.arrays(), U.TT, ev, ALL, ALL, 0, PAY, cfg, ids[0], ids[1], ids[2], code,
              ctr, ust, np.zeros((2, 2, RS), np.int8), np.zeros((2, 2, RS), np.int8), np.zeros((7, RS), np.int8),
              np.zeros((3, RS), np.int8), res, pb)
    return code, res, ust


def _expect(mode, w_cur, hooked, strikers, s):
    """Notes §1.5's table (constant boss, no whack): is the demand s (1 = 1/4, 2 = 1/2) acceptable?"""
    some = strikers >= 1
    if mode == 1 or not hooked:
        if w_cur == 0:
            return False
        if s <= w_cur:
            return some
        return False
    # (C), hooked boss: the boss's best reply is the wage s (cut to the demand, or raise to it)
    if s > w_cur:
        return True
    if s == w_cur:
        return some
    return strikers == 2                          # a cut to s < w_cur: only if both workers currently strike


@pytest.mark.parametrize('mode', [1, 2])
@pytest.mark.parametrize('hooked', [False, True])
@pytest.mark.parametrize('w_cur', [0, 1, 2])
@pytest.mark.parametrize('strikers', [0, 1, 2])
def test_union_acceptance_matches_hand_table(sg, mode, hooked, w_cur, strikers):
    act = U.bact(w_cur, 1)
    boss = sg.P.index_b[((), ((9 + act) if hooked else act,))]
    hw = sg.P.index_w[((), (2,))]; hs = sg.P.index_w[((), (3,))]
    wa = hs if strikers >= 1 else hw
    wb = hs if strikers == 2 else hw
    T, tdict, ev, ids = _slot_types(sg, boss, wa, wb)
    code, res, ust = _attempt_union(sg, T, tdict, ev, ids, mode)
    assert (code // 4) == act
    for s in (1, 2):
        assert bool(ust[29 + s] > 0) == _expect(mode, w_cur, hooked, strikers, s), (mode, hooked, w_cur, strikers, s)


def test_credible_response_boss_adopts_the_demand(sg):
    """(C), hooked boss paying 0 against scabs (work at 0): a demand is accepted and the boss adopts the wage as fills
    keyed on the two workers' lineages; under (M) nothing is accepted."""
    boss = sg.P.index_b[((), (9 + U.bact(0, 1),))]
    hw = sg.P.index_w[((), (2,))]
    T, tdict, ev, ids = _slot_types(sg, boss, hw, hw)
    code, res, ust = _attempt_union(sg, T, tdict, ev, ids, 2)
    assert res[1] >= 0 and res[2] >= 0
    assert ust[4] == 1                                        # the boss adopted a response fill
    nb = res[0]
    Tf, Tn = T[3], T[4]
    acts = sorted({S.g_action(int(Tf[nb, j])) for j in range(int(Tn[nb]))})
    assert len(acts) == 1 and acts[0] in (U.bact(1, 1), U.bact(2, 1))
    keys = sorted(S.g_key(int(Tf[nb, j])) for j in range(int(Tn[nb])))
    assert keys == [101, 102]
    c2 = _code(sg, T, ev, [res[0], res[1], res[2]])
    assert c2 // 4 == acts[0] and (c2 % 4) == 0               # both work at the adopted wage
    code, res, ust = _attempt_union(sg, T, tdict, ev, ids, 1)
    assert res[1] == -1 and ust[2] + ust[3] == 0


def test_role_keyed_union_applies_against_any_boss(sg):
    boss = sg.P.index_b[((), (9 + U.bact(0, 1),))]
    hw = sg.P.index_w[((), (2,))]
    T, tdict, ev, ids = _slot_types(sg, boss, hw, hw)
    code, res, ust = _attempt_union(sg, T, tdict, ev, ids, 2, role=1)
    assert res[1] >= 0
    for t in (res[1], res[2]):
        assert S.g_scope(int(T[3][t, 0])) == S.ROLE and S.g_action(int(T[3][t, 0])) in (2, 3)
    assert S.g_scope(int(T[3][res[0], 0])) == S.ROLE
    # the response and demand are role-wide: a boss of another lineage with the same adopted fill pays too
    boss2 = SK.get_type(T, tdict, sg.htags, sg.wtag, ALL, 0, 0, boss, 999, T[3][res[0]].copy(), int(T[4][res[0]]))
    c = _code(sg, T, ev, [boss2, res[1], res[2]])
    assert c % 4 == 0                                         # both work


def test_demand_fill_semantics_on_the_evaluator(sg):
    """work iff the boss provably pays at least s: constant bosses (table of notes §1.5)."""
    hw = sg.P.index_w[((), (2,))]
    for s, act in ((1, 2), (2, 3)):                           # fill action 2 = demand 1/4, 3 = demand 1/2
        f = S.fcode(act, 0, S.HIST, S.CONTRACT, 100)
        for w in range(3):
            boss = sg.P.index_b[((), (U.bact(w, 1),))]
            T, tdict, ev, ids = _slot_types(sg, boss, hw, hw, wa_fills=[f], wb_fills=[f])
            c = _code(sg, T, ev, ids)
            works = (w >= s)
            assert (c % 4 == 0) == works and (c % 4 == 3) == (not works), (s, w, c)


def test_responsive_boss_hand_cases(sg):
    """notes §1.5: R1 'pay 1/2 iff provably W1 works' meets demanding workers at (work, 1/2); R2 'pay 1/2 iff provably
    W1 strikes' at (strike, 0): the demand backfires."""
    hw = sg.P.index_w[((), (2,))]
    f = S.fcode(3, 0, S.HIST, S.CONTRACT, 100)               # demand 1/2
    r1 = sg.P.index_b[(((0, 0),), (U.bact(0, 1), U.bact(2, 1)))]
    r2 = sg.P.index_b[(((0, 1),), (U.bact(0, 1), U.bact(2, 1)))]
    T, tdict, ev, ids = _slot_types(sg, r1, hw, hw, wa_fills=[f], wb_fills=[f])
    assert _code(sg, T, ev, ids) == 4 * U.bact(2, 1) + 0
    T, tdict, ev, ids = _slot_types(sg, r2, hw, hw, wa_fills=[f], wb_fills=[f])
    assert _code(sg, T, ev, ids) == 4 * U.bact(0, 1) + 3


def test_protected_fills_resist_trigger_writes(sg):
    hw = sg.P.index_w[((), (2,))]
    T, tdict, ev, ids = _slot_types(sg, 0, hw, hw)
    ctr = np.zeros(24, np.int64)
    dem = S.fcode(3, 0, S.HIST, S.CONTRACT, 100)
    thanks = S.fcode(0, 0, S.HIST, S.WRITTEN, 100)
    f = np.zeros(4, np.int64); f[0] = dem
    w2 = SK.get_type(T, tdict, sg.htags, sg.wtag, ALL, 0, 1, hw, 101, f, 1)
    assert SK._write(T, tdict, sg.htags, sg.wtag, ALL, 0, w2, thanks, ctr, 0) == -1 and ctr[18] == 1   # blocked
    dem2 = S.fcode(2, 0, S.HIST, S.CONTRACT, 100)                # a contract-origin write supersedes it in place
    assert SK._write(T, tdict, sg.htags, sg.wtag, ALL, 0, w2, dem2, ctr, 0) >= 0
    hb = sg.P.index_b[((), (9 + U.bact(0, 1),))]                 # the boss's contract fill: protected only if pb = 1
    bf = np.zeros(4, np.int64); bf[0] = S.fcode(U.bact(2, 1), 0, S.HIST, S.CONTRACT, 101)
    b2 = SK.get_type(T, tdict, sg.htags, sg.wtag, ALL, 0, 0, hb, 100, bf, 1)
    gr = S.fcode(U.bact(0, 0), 0, S.HIST, S.WRITTEN, 101)
    assert SK._write(T, tdict, sg.htags, sg.wtag, ALL, 0, b2, gr, ctr, 1) == -1
    assert SK._write(T, tdict, sg.htags, sg.wtag, ALL, 0, b2, gr, ctr, 0) >= 0


def test_sog_reproduces_part_w_stored_rows_with_union_off():
    """A short `maximal` run through this module reproduces Part W's stored records at generations 10 and 25."""
    stored = SR._stored_rows('maximal')
    row = SR.run_one('maximal', 0, gens=25)
    by_gen = {t['gen']: t for t in stored[0]['ts']}
    for t in row['ts']:
        assert t['labels'] == by_gen[t['gen']]['labels'] and t['wage'] == by_gen[t['gen']]['wage']


def test_union_never_downgrades_a_held_demand(sg):
    """A worker already holding a demand of at least s at the key keeps it: the candidate writes only the other worker."""
    boss = sg.P.index_b[((), (9 + U.bact(0, 1),))]
    hw = sg.P.index_w[((), (2,))]
    dem = S.fcode(3, 0, S.HIST, S.CONTRACT, 100)
    T, tdict, ev, ids = _slot_types(sg, boss, hw, hw, wa_fills=[dem])
    code, res, ust = _attempt_union(sg, T, tdict, ev, ids, 2)
    assert code % 4 == 2 and code // 4 == U.bact(0, 1)        # x strikes against the zero wage, y works at 0
    assert res[1] == -1 and res[2] >= 0                       # x keeps its demand; y writes
    assert S.g_action(int(T[3][res[2], 0])) in (2, 3)
    assert ust[4] == 1
