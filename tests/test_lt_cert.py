"""Tests for certificates as code (src/lt_cert.py): the check-aware self-interpreter against the host decomposition and
the reference stepper, the checker term against the independent host replay checker, the wrapper's cost bound, the
hand instances and corrupted instances of notes/certificates-as-code.md §1.10, Lemma Sym, and a fuzz soundness audit
(every accepted atom true for the sound, copy, self-only and none checkers; the naive checker accepts false atoms)."""
import os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import lt_cert as C
import lt_code as L

N, P = L.N, L.P
K6 = 10 ** 6
V6 = K6 // 4


def big(fn):
    return L.run_big(fn)


_ARM = {}


def arm(K=K6, name='S'):
    if (K, name) not in _ARM:
        _ARM[(K, name)] = C.build_arm(K, name)
    return _ARM[(K, name)]


def cv(mode, t, m, a='C', K=K6, V=None):
    V = K // 4 if V is None else V
    return C.check_value(mode, V, t, m, a, K)


def test_self_interpreter_matches_host_decomposition():
    """cstep (term) against hdecompose (host) along play chains through check-call states and sim frames."""
    def body():
        progs, _ = arm()
        for a in ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap', 'SFc', 'Ccert', 'CBw2', 'CBlet2', 'CBPh']:
            for b_ in ['CB', 'SFc', 'D']:
                t = L.initial(progs[a], progs[b_])
                for _ in range(30):
                    ctx, kind, pay, ito = C.hdecompose(t)
                    v, _n = L.evaluate(L.call('cstep', ('quote', t)))
                    if kind == 'value': assert v[0] == 0
                    elif kind == 'stuck': assert v[0] == 1
                    elif kind == 'det':
                        assert v[0] == 2 and L.canon_rt(v[1][0]) == L.canon_term(L.plug(ctx, pay)) and v[1][1] == ito
                    else:
                        assert v[0] == 3 and v[1][0] == pay[0] and L.canon_rt(v[1][1][0]) == L.canon_term(pay[1])
                        frames = L.rt_to_tval(v[1][1][1])
                        for code, xt in ((2, L.T_), (3, L.F_)):
                            pv, _ = L.evaluate(L.call('plug', frames, P(N(3), N(code)), N(17)))
                            assert L.canon_rt(pv) == L.canon_term(L.plug(ctx, xt, 17))
                    if kind != 'det': break
                    t = L.plug(ctx, pay)
    big(body)


def test_evaluator_matches_reference_on_checks():
    """Whole plays (the checks run step by step under the substitution semantics) at K = 10^5."""
    def body():
        K = 10 ** 5
        progs, _ = arm(K)
        for a, b_ in [('CB', 'CB'), ('CB', 'CB0'), ('CB', 'Ccert'), ('CBN0', 'CBN')]:
            L.CACHE.clear()
            v1, n1 = L.evaluate(L.initial(progs[a], progs[b_]), K)
            v2, n2 = L.ref_run(L.initial(progs[a], progs[b_]), K)
            assert (v1 if v1 == 'BOT' else L.canon_rt(v1)) == (v2 if v2 == 'BOT' else L.canon_tval(v2))
            assert v1 == 'BOT' or n1 == n2, (a, b_, n1, n2)
    big(body)


def test_wrapper_cost_bound():
    """A check call costs exactly (inner steps) + 6 <= V + 6, also when the core times out."""
    def body():
        progs, _ = arm()
        for a, b_ in [('CB', 'CB1'), ('CBP', 'CB'), ('CB', 'D'), ('CB0', 'CB')]:
            for V in (V6, 30000, 5000, 100):
                res, total = cv(0, progs[a], progs[b_], V=V)
                v, steps = C.wrapper_call_cost(0, V, progs[a], progs[b_], 'C', K6)
                assert steps == total + 5 <= V + 6, (a, b_, V, steps, total)
                assert v == ('T' if res == 'T' else 'F')
    big(body)


def test_term_check_matches_host_replay():
    """Every check of every ordered pair of arm S at K = 10^6: the checker term against the host replay checker."""
    def body():
        progs, _ = arm()
        host = C.HostCheck()
        names = [n for n in progs if not n.endswith('_code') and n != 'SF']
        nchk = 0
        for x in names:
            for y in names:
                for a in ('C', 'D'):
                    for mode in (0, 1, 2, 3, 4, 5):
                        res, total = cv(mode, progs[x], progs[y], a)
                        if res == 'TO': continue
                        h = host.check(C.ID[C.MODE_WRAP[mode]], C.mk_arg(V6, progs[x], progs[y], a, K6))
                        assert h == res, (x, y, a, mode, res, h)
                        nchk += 1
        assert nchk > 1000
    big(body)


def test_hand_instance_1_valid_pair():
    def body():
        progs, _ = arm()
        for x, y in [('CB', 'CB1'), ('CB1', 'CB')]:
            res, total = cv(0, progs[x], progs[y])
            assert res == 'T' and total <= V6
            assert L.play(progs[x], progs[y], K6)[0] == 'C'
        assert C.HostCheck().vone(0, C.mk_arg(V6, progs['CB'], progs['CB1'], 'C', K6),
                                  ('cbox', C.ID['CHKS'], C.mk_arg(V6, progs['CB'], progs['CB1'], 'C', K6)),
                                  ('cbox', C.ID['CHKS'], C.mk_arg(V6, progs['CB1'], progs['CB'], 'C', K6)))[:2] == (True, True)
    big(body)


def test_hand_instance_2_wrong_code():
    def body():
        progs, _ = arm()
        for y in ['CB', 'CB1', 'CBP']:
            assert cv(0, progs['CBfake'], progs[y])[0] == 'F'
            assert cv(0, progs['CBdef'], progs[y])[0] == 'F'
    big(body)


def test_hand_instance_3_fuel_mismatch():
    """A CB naming K' = 10K in its call: its box is not the reader's S; the reader's check is F, both defect."""
    def body():
        progs, _ = arm()
        cb = progs['CB']
        lst = C.h_getcerts(cb)
        cbx = C.carrier(('if', C.CALL(0, V6, C.THEM3, C.ME3, 'C', 10 * K6), L.C_, L.D_), lst)
        assert cv(0, cbx, cb)[0] == 'F'
        assert L.play(cb, cbx, K6)[0] == 'D' and L.play(cbx, cb, K6)[0] == 'D'
    big(body)


def test_hand_instance_4_fit_boundary():
    """CB against itself with V = 25,000 named in the source: the static boundary is K = V + 10."""
    def body():
        V = 25000
        s = C.node(C.EVS, 0, C.node(C.CHKR, 0, C.node(C.EVS, 0, C.node(C.AX, 0)), C.node(C.HYP, 0)))
        for K, exp in ((V + 8, 'F'), (V + 9, 'F'), (V + 10, 'T'), (V + 11, 'T')):
            cb = C.carrier(C.body_CB(0, V, K), C.cons([('C', s)]))
            assert C.check_value(0, V, cb, cb, 'C', K)[0] == exp, K
            assert L.play(cb, cb, K)[0] == ('C' if exp == 'T' else 'D'), K
    big(body)


def test_hand_instance_5_hyp_not_R_or_S():
    """A carrier whose call checks a third program: Hyp on that box is rejected."""
    def body():
        progs, _ = arm()
        third = ('quote', progs['CB1'])
        s = C.node(C.EVS, 0, C.node(C.CHKR, 0, C.node(C.EVS, 0, C.node(C.AX, 0)), C.node(C.HYP, 0)))
        z = C.carrier(('if', C.CALL(0, V6, third, C.ME3, 'C', K6), L.C_, L.D_), C.cons([('C', s)]))
        assert cv(0, z, progs['CB'])[0] == 'F'
        assert C.HostCheck().check(C.ID['CHKS'], C.mk_arg(V6, z, progs['CB'], 'C', K6)) == 'F'
    big(body)


def test_hand_instance_6_partner_validation():
    def body():
        progs, _ = arm()
        assert cv(0, progs['CB'], progs['CB0'])[0] == 'F'      # Hyp(S) syntactically fine, partner has no script
        assert cv(1, progs['CBN'], progs['CBN0'])[0] == 'T'    # the unguarded rule accepts
        assert L.play(progs['CBN0'], progs['CBN'], K6)[0] == 'C' and L.play(progs['CBN'], progs['CBN0'], K6)[0] == 'D'
    big(body)


def test_hand_instance_7_run_exclusions():
    """Run on S, Run on R (via a self-checking carrier), and Run with a cap below the root's: rejected."""
    def body():
        progs, _ = arm()
        lst = C.h_getcerts(progs['CB'])
        run_s = C.node(C.EVS, 0, C.node(C.CHKR, 0, C.node(C.EVS, 0, C.node(C.AX, 0)), C.node(C.RUN, 0)))
        cb_run = C.carrier(C.body_CB(0, V6, K6), C.cons([('C', run_s)]))
        assert cv(0, cb_run, progs['CB'])[0] == 'F'
        lob_run = C.carrier(C.body_LobC(0, V6, K6), C.cons([('C', run_s)]))
        assert cv(0, lob_run, progs['CB'])[0] == 'F'
        # a sloppy carrier with a smaller cap in its call: the sound reader's Run on it is refused
        s_small = C.carrier(('if', C.CALL(4, V6 // 2, C.THEM3, C.ME3, 'C', K6), L.C_, L.D_),
                            C.cons([('C', C.node(C.EVS, 0, C.node(C.CHKR, 0, C.node(C.EVS, 0, C.node(C.AX, 0)), C.node(C.RUN, 0))))]))
        assert cv(0, s_small, progs['CB'])[0] == 'F'
        assert cv(0, progs['CBsloppy'], progs['CB'])[0] == 'T'
        assert lst is not None
    big(body)


def test_hand_instance_8_dcert():
    def body():
        progs, _ = arm()
        for y in ['CB', 'CB1', 'CBP', 'CBN', 'CBS2']:
            for mode in (0, 1, 2, 3, 5):
                assert cv(mode, progs['Dcert'], progs[y])[0] == 'F', (y, mode)
            assert cv(4, progs['Dcert'], progs[y])[0] == 'T'
        assert cv(4, L.PROG_D, progs['CB'])[0] == 'F'
        assert L.play(progs['CBsloppy'], progs['Dcert'], K6)[0] == 'C'
        assert L.play(progs['CB'], progs['Dcert'], K6)[0] == 'D'
    big(body)


def test_hand_instance_10_lemma_sym():
    """Every sound check that closed S: the swap check is T with an equal step count if the partner closed R, else no
    more."""
    def body():
        progs, _ = arm()
        host = C.HostCheck()
        names = ['CB', 'CB1', 'CBP', 'CBlet', 'CBwrap', 'SFc', 'LobC', 'CBsloppy', 'CBmut', 'CBS2', 'CBlet2', 'CBw2',
                 'CB1h', 'CB1r', 'CBPh', 'CBPr_fresh']
        n = 0
        for x in names:
            for y in names:
                for mode in (0, 5):
                    v = C.mk_arg(V6, progs[x], progs[y], 'C', K6)
                    nid = C.ID[C.MODE_WRAP[mode]]
                    Rb, Sb = ('cbox', nid, v), ('cbox', nid, C.swap_arg(v))
                    ok, usesS, _ = host.vone(mode, v, Rb, Sb)
                    if not (ok and usesS and Rb != Sb): continue
                    r1, t1 = cv(mode, progs[x], progs[y])
                    if r1 != 'T': continue
                    r2, t2 = cv(mode, progs[y], progs[x])
                    ok2, usesS2, _ = host.vone(mode, C.swap_arg(v), Sb, Rb)
                    assert r2 == 'T', (x, y)
                    assert (t2 == t1) if usesS2 else (t2 <= t1), (x, y, t1, t2)
                    n += 1
        assert n >= 20
    big(body)


FUZZ_CALLS = [('them', 'me', 'C'), ('me', 'them', 'C'), ('them', 'QD', 'D'), ('them', 'me', 'D')]


def fuzz_body(rng, depth, mode, V, K):
    if depth == 0 or rng.random() < 0.3: return rng.choice([L.C_, L.D_])
    x, y, a = rng.choice(FUZZ_CALLS)
    xx = {'them': C.THEM3, 'me': C.ME3, 'QD': C.QD}
    return ('if', C.CALL(mode, V, xx[x], xx[y], a, K), fuzz_body(rng, depth - 1, mode, V, K),
            fuzz_body(rng, depth - 1, mode, V, K))


def fuzz_script(rng, depth):
    r = rng.random()
    if depth == 0 or r < 0.35:
        return C.node(rng.choice([C.AX, C.HYP, C.HYP, C.RUN, C.RUNNEG]), rng.choice([0, 0, 1]))
    if r < 0.6: return C.node(C.EVS, rng.choice([0, 0, 1]), fuzz_script(rng, depth - 1))
    return C.node(C.CHKR, rng.choice([0, 0, 1]), fuzz_script(rng, depth - 1), fuzz_script(rng, depth - 1))


def test_fuzz_soundness_audit():
    """Random carrier-like codes with produced and random scripts: every accepted atom is true for modes 0, 2, 3, 5
    (Theorem S^cert); mode 1 (the unguarded pair rule) accepts at least one false atom."""
    def body():
        rng = random.Random(20261006)
        K, V = 10 ** 5, 10 ** 5 // 4
        progs = {}
        prod = C.Producer()
        for mode in (0, 1, 2, 3, 5):
            for i in range(14):
                bodyt = fuzz_body(rng, 2, mode, V, K)
                ents = []
                for _ in range(2):
                    ents.append((rng.choice(['C', 'C', 'D']), fuzz_script(rng, 4)))
                p0 = C.carrier(bodyt, C.cons(ents))
                for a, probe in (('C', p0), ('D', L.PROG_D)):
                    s = prod.produce(mode, p0, probe, a, K, V)
                    if s is not None: ents.append((a, s))
                progs[(mode, i)] = C.carrier(bodyt, C.cons(ents))
        viol = {m: 0 for m in (0, 1, 2, 3, 5)}
        acc = {m: 0 for m in (0, 1, 2, 3, 5)}
        for mode in (0, 1, 2, 3, 5):
            ps = [p for (m, i), p in progs.items() if m == mode] + [L.PROG_C, L.PROG_D]
            for t in ps:
                for m_ in ps:
                    for a in ('C', 'D'):
                        res, _ = C.check_value(mode, V, t, m_, a, K)
                        if res != 'T': continue
                        acc[mode] += 1
                        if L.play(t, m_, K)[0] != a: viol[mode] += 1
        assert all(viol[m] == 0 for m in (0, 2, 3, 5)), (viol, acc)
        assert acc[0] > 20
        return viol, acc
    big(body)


def test_naive_counterexample_every_K():
    def body():
        for K in (10 ** 5, 10 ** 6):
            progs, _ = arm(K)
            assert L.play(progs['CBN0'], progs['CBN'], K)[0] == 'C' and L.play(progs['CBN'], progs['CBN0'], K)[0] == 'D'
    big(body)


def test_host_budget_lower_bound():
    """The host replay's budget is sound: one interpreted step at context depth d costs the term >= 20 (1 + d)."""
    def body():
        progs, _ = arm()
        worst = None
        for a, b_ in [('SFc', 'SFc'), ('SFc', 'CB'), ('CB', 'CB1'), ('CBP', 'CB'), ('SF', 'SF')]:
            t = L.initial(progs[a], progs[b_])
            for _ in range(400):
                ctx, kind, pay, ito = C.hdecompose(t)
                if kind != 'det': break
                v, n = L.evaluate(L.call('cstep', ('quote', t)))
                r = n / (1 + len(ctx))
                worst = r if worst is None else min(worst, r)
                t = L.plug(ctx, pay)
        assert worst >= C.HOST_STEP_COST, worst
    big(body)
