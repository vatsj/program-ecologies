"""Tests for the prover as code (src/lt_code.py): evaluator against the reference stepper, the self-interpreter against
the reference stepper, the term search against the host oracle and the brute-force prover, witness replay, the
checker term, and the corrupted side conditions of notes/prover-as-code.md §1.9."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import lt_code as L

N, P = L.N, L.P


def big(fn):
    return L.run_big(fn)


def same_value(v_rt, v_term):
    if v_rt == 'BOT' or v_term == 'BOT': return v_rt == v_term
    return L.canon_rt(v_rt) == L.canon_tval(v_term)


SMALL = [
    ('op', 'add', N(2), N(3)),
    ('op', 'sub', N(2), N(3)),
    ('op', 'div', N(2), N(0)),
    ('if', ('op', 'lt', N(1), N(2)), L.C_, L.D_),
    ('fst', ('quote', ('lam', ('v', 0)))),
    ('snd', ('quote', ('app', ('v', 0), ('nat', 3)))),
    ('eq', ('quote', ('nat', 3)), P(N(4), N(3))),
    ('eq', ('quote', ('lam', ('v', 0))), P(N(1), ('quote', ('v', 0)))),
    ('capk', N(3), ('lam', ('op', 'add', ('v', 0), N(1))), N(5)),
    ('capk', N(1), ('lam', ('op', 'add', ('v', 0), N(1))), N(5)),
    ('capk', N(0), ('lam', ('v', 0)), N(5)),
    ('capk', N(5), ('lam', ('fst', ('v', 0))), N(5)),
    ('sim', 4, ('sim', 2, ('op', 'add', ('op', 'add', N(1), N(1)), N(1)))),
    ('sim', 2, ('sim', 4, ('op', 'add', ('op', 'add', N(1), N(1)), N(1)))),
    ('run', N(10), ('quote', L.PROG_C), ('quote', L.PROG_D)),
    ('app', ('fix', ('lam', ('if', ('eq', ('v', 0), N(0)), L.C_, ('app', ('v', 1), ('op', 'sub', ('v', 0), N(1)))))), N(4)),
    ('libsrc', N(3)),
    L.call('min', N(7), N(4)),
]


def test_evaluator_matches_reference_small():
    for t in SMALL:
        for K in (0, 1, 2, 3, 5, 8, 100):
            v1, n1 = L.evaluate(t, K)
            v2, n2 = L.ref_run(t, K)
            assert same_value(v1, v2) and (n1 == n2 or v1 == 'BOT'), (t, K, v1, n1, v2, n2)


def test_evaluator_matches_reference_plays():
    """Plays run step by step under the reference stepper (the whole library executed by substitution)."""
    def body():
        cat = L.catalogue(10 ** 4, 3, k=40)
        for a, b_ in [('FB', 'C'), ('FB', 'D'), ('SF', 'SF'), ('SF', 'C'), ('C', 'SF'), ('G', 'D'), ('SC', 'D')]:
            for K in (3, 50, 400, 3000):
                L.CACHE.clear()
                v1, n1 = L.evaluate(L.initial(cat[a], cat[b_]), K)
                v2, n2 = L.ref_run(L.initial(cat[a], cat[b_]), K)
                assert same_value(v1, v2), (a, b_, K, v1, v2)
                assert v1 == 'BOT' or n1 == n2, (a, b_, K, n1, n2)
    big(body)


def test_self_interpreter_matches_reference():
    def body():
        cat = L.catalogue(10 ** 6, 8, k=500)
        for a in ['FB', 'SF', 'PB', 'Vwrap', 'Vlet', 'FB2', 'P*']:
            for b_ in ['FB', 'SF', 'C', 'D']:
                t = L.initial(cat[a], cat[b_])
                for _ in range(40):
                    r = L.step(t)
                    v, _n = L.evaluate(L.call('step', ('quote', t)))
                    if r[0] == 'value': assert v[0] == 0
                    elif r[0] == 'stuck': assert v[0] == 1
                    elif r[0] == 'det':
                        assert v[0] == 2 and L.canon_rt(v[1][0]) == L.canon_term(r[1]) and v[1][1] == r[2]
                    else:
                        assert v[0] == 3 and v[1][0] == r[1] and L.canon_rt(v[1][1][0]) == L.canon_term(r[2])
                        frames = L.rt_to_tval(v[1][1][1])
                        for code, xt in ((2, L.T_), (3, L.F_)):
                            pv, _ = L.evaluate(L.call('plug', frames, P(N(3), N(code)), N(17)))
                            assert L.canon_rt(pv) == L.canon_term(L.plug(r[3], xt, 17))
                    if r[0] != 'det': break
                    t = r[1]
    big(body)


def _queries(K, b, names):
    cat = L.catalogue(K, b)
    for x in names:
        for y in names:
            L.play(cat[x], cat[y], K)
    return cat


def test_term_search_matches_host_and_replays():
    def body():
        L.CACHE.clear()
        cat = _queries(10 ** 6, 12, ['C', 'D', 'FB', 'PB', 'SF', 'SC', 'G'])
        nfin = 0
        for key, (res, total) in list(L.CACHE.items()):
            n, U, (c, (psi, _u)) = key
            mode = L.CORE_LIBS[n]
            if res not in ('T', 'F'): continue
            nfin += 1
            h = L.host_query(mode, c, psi, U)
            r, w, wi, _ = L.core_witness(mode, c, psi, U)
            assert h['found'] == (res == 'T') and r == res
            assert wi == (h['work'], h['inst'])
            if res == 'T':
                wt = L.witness_from_rt(w)
                assert L.replay(wt, mode, c, U, L.rt_to_formula(psi), True) == h['size']
                assert wt == h['search'].witness()
                v, _ = L.term_check(mode, c, psi, U, w)
                assert v == 'T'
        assert nfin >= 10
    big(body)


def test_brute_force_agrees_small_b():
    def body():
        K = 10 ** 6
        for b in (5, 6, 7, 8):
            cat = L.catalogue(K, b)
            U = K // 4
            for x, y in [('FB', 'FB'), ('FB', 'C'), ('FB', 'D'), ('G', 'G'), ('SC', 'SC'), ('FB', 'SC'), ('FB2', 'FB2')]:
                mode = 1 if x == 'SC' else 0
                psi = L.PLAYS(('quote', cat[y]), ('quote', cat[x]), L.C_, K)
                psi_rt = L.tval_to_rt(psi)
                h = L.host_query(mode, b, psi_rt, U)
                br = L.Brute(mode, b, L.rt_to_formula(psi_rt), U).minsize()
                assert h['size'] == br, (b, x, y, h['size'], br)
    big(body)


def test_fairbot_threshold_and_witness():
    """Notes §1.7: b*(FB) = 7; the derivation is JLob^self over EvR, EvR, SrchR(EvR, Ax; Ax)."""
    def body():
        K = 10 ** 6; U = K // 4
        for b, exp in ((6, False), (7, True), (8, True)):
            cat = L.catalogue(K, b)
            psi = L.tval_to_rt(L.PLAYS(('quote', cat['FB']), ('quote', cat['FB']), L.C_, K))
            r, w, wi, steps = L.core_witness(0, b, psi, U)
            assert (r == 'T') == exp
            if exp:
                wt = L.witness_from_rt(w)
                rules = []

                def walk(nd):
                    rules.append(nd['rule'])
                    for p in nd['prem']: walk(p)
                walk(wt)
                assert rules == ['jlob', 'EvR', 'EvR', 'SrchR', 'EvR', 'ax', 'ax'] and wt['size'] == 7
            assert L.play(cat['FB'], cat['FB'], K)[0] == ('C' if exp else 'D')
    big(body)


def _fb_witness(K=10 ** 6, b=8):
    U = K // 4
    cat = L.catalogue(K, b)
    psi = L.tval_to_rt(L.PLAYS(('quote', cat['FB']), ('quote', cat['FB']), L.C_, K))
    r, w, wi, steps = L.core_witness(0, b, psi, U)
    return cat, psi, U, L.witness_from_rt(w)


def _corrupt(wt, fn):
    import copy
    w2 = copy.deepcopy(wt)
    fn(w2)
    return w2


def _rejected(mode, b, psi, U, wt):
    root = L.rt_to_formula(psi)
    try:
        L.replay(wt, mode, b, U, root, True)
        host = False
    except L.ReplayError:
        host = True
    v, _ = L.term_check(mode, b, psi, U, L.witness_to_rt(wt))
    return host, v != 'T'


def test_corrupted_side_conditions_rejected():
    """Notes §1.9 instances 2-7: each corrupted derivation is rejected by the replay checker and the checker term."""
    def body():
        K, b = 10 ** 6, 8
        cat, psi, U, wt = _fb_witness(K, b)
        root = L.rt_to_formula(psi)
        H = ('box', 0, b, U, root)
        assert _rejected(0, b, psi, U, wt) == (False, False)          # the valid one is accepted

        def set_hyp(newH):
            def f(w):
                p = w['prem'][0]                                      # JLob premise H |- root

                def sub(nd):
                    nd['L'] = [newH if x == H else x for x in nd['L']]
                    for q in nd['prem']: sub(q)
                sub(p)
            return f
        cases = {
            '2 budget b-1': set_hyp(('box', 0, b - 1, U, root)),
            '3 cap U-1': set_hyp(('box', 0, b, U - 1, root)),
        }

        def member(w):   # JLob with a non-root member: premise H' |- A1, H' the box of A1
            A1 = w['prem'][0]['prem'][0]['R'][0]
            w['prem'][0]['L'] = [('box', 0, b, U, A1)]
            w['prem'][0]['R'] = [A1]
            w['prem'][0] = w['prem'][0]['prem'][0]
            w['prem'][0]['L'] = [('box', 0, b, U, A1)]
        cases['4 member'] = member

        def through_search(w):   # JLob concluding the after-state of the search call (not downstream)
            import copy
            prem = copy.deepcopy(w['prem'][0])
            srch = w['prem'][0]['prem'][0]['prem'][0]
            p1 = srch['prem'][0]
            x = p1['R'][0]
            p1.update({'rule': 'jlob', 'x': x, 'prem': [prem]})
        cases['5 conclusion through a search call'] = through_search

        def run_root(w):         # close P2's owed root box by Run instead of Ax
            srch = w['prem'][0]['prem'][0]['prem'][0]
            p2 = srch['prem'][1]
            bx = [x for x in p2['R'] if x[0] == 'box'][0]
            p2.update({'rule': 'run', 'x': bx, 'prem': []})
        cases['7 Run on the root call'] = run_root
        for name, fn in cases.items():
            w2 = _corrupt(wt, fn)
            host_rej, term_rej = _rejected(0, b, psi, U, w2)
            assert host_rej and term_rej, name

        # 6: SrchR fit corrupted.  Y returns its search's bit directly; SFX_k simulates Y with sim fuel k = 100, far
        # below U + 7, and plays C iff the simulation returns T.  The actual simulation times out (the search costs
        # more than 100 steps), so SFX defects.  A search that skips the fit test (the host with h_asucc's fit
        # skipped) certifies "SFX cooperates" through the minimal-residual reading sim(0, T) -> T; the sound
        # checkers must reject it.
        Y = L.L2(L.SRCH(0, b, L.PLAYS(('quote', L.PROG_C), ('quote', L.PROG_C), L.C_, K), U))
        SFX = L.L2(('if', ('eq', ('run', N(100), ('quote', Y), L.ME), L.T_), L.C_, L.D_))
        fb = cat['FB']
        b6 = 16
        psi6 = L.tval_to_rt(L.PLAYS(('quote', SFX), ('quote', fb), L.C_, K))
        orig = L.h_asucc
        try:
            L.h_asucc = lambda phi, mode: orig(phi, 1 if mode == 0 else mode)
            s = L.HostSearch(0, b6, L.rt_to_formula(psi6), U)
            found, size = s.search()
            w6 = s.witness() if found else None
        finally:
            L.h_asucc = orig
        assert found
        host_rej, term_rej = _rejected(0, b6, psi6, U, w6)
        assert host_rej and term_rej
        assert L.play(SFX, fb, K)[0] == 'D'        # the certified claim is false
        sound = L.HostSearch(0, b6, L.rt_to_formula(psi6), U)
        assert sound.search()[0] is False
    big(body)


def test_regress_jump_matches_reference():
    """The regress lemma fast-forward gives the reference result and step count (SF against itself)."""
    for k in (10, 37, 60):
        for K in (50, 200, 10 ** 4):
            sf = L.SF(k)
            v1, n1 = L.evaluate(L.initial(sf, sf), K)
            v2, n2 = L.ref_run(L.initial(sf, sf), K)
            assert same_value(v1, v2) and (v1 == 'BOT' or n1 == n2), (k, K, v1, n1, v2, n2)
