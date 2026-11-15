"""Queue 80 tests: the script checker (S0 against the host reference), the forgers, the S1 machine's interruption rule, and pairing."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import lt_code as L
import tplus as TP
import script_offers as S
import script_offers_cat as SC


def _cat():
    return SC.Cat('S', forg=True)


def test_checker_matches_host_and_expected_holdings():
    cat = _cat()
    for i in range(cat.Kc, cat.K):        # forgers: S0 = host, acceptances within the allowed (true) statements
        acc = ''
        for c in range(1, 6):
            v, _ = S.core_s0(cat.terms[i], c)
            assert (v == 'T') == S.host_check(cat.terms[i], c), (cat.names[i], c)
            if v == 'T':
                acc += str(c)
        assert set(acc) <= set(cat.meta[i]['expected']), (cat.names[i], acc)
    for i in range(SC.NBASE, cat.Kc, 7):  # a sample of carriers
        m = cat.meta[i]
        exp = set()
        if m['fn']:
            exp |= {2} | ({1} if m['R'] == 0 else set())
        if m['fp']:
            exp |= {4} | ({3} if m['R'] == 0 else set())
        if m['nx']:
            exp.add(5)
        got = {c for c in range(1, 6) if S.core_s0(cat.terms[i], c)[0] == 'T'}
        assert got == exp, (cat.names[i], got, exp)


def test_s1_interruption_equals_s0():
    cat = _cat()
    tab = SC.s1_table([cat.terms[cat.idx[n]] for n in ('Ocn.canon', 'Pc+Spoy.guard', 'XvacBc')])
    SC.install_s1(tab)
    for n in ('Ocn.canon', 'Pc+Spoy.guard', 'XvacBc'):
        t = cat.terms[cat.idx[n]]
        for c in (1, 5):
            cost = tab[(L.canon_term(t), c)][1]
            for fuel in (cost, cost + 1):
                term = ('app', ('lib', S.ID_CCORE), ('pair', ('quote', t), ('nat', c)))
                r = []
                for m in ('S0', 'S1'):
                    S.set_machine(m)
                    v, st = L.run_big(L.evaluate, term, fuel)
                    r.append((v, st))
                assert r[0] == r[1], (n, c, fuel, r)
    S.set_machine('S0')


def test_cross_spelling_pair():
    TP.install_counter(); S.set_regress(True); S.set_machine('S0')
    cat = _cat()
    a, b, c = cat.terms[cat.idx['FcSnoy.rord']], cat.terms[cat.idx['Fc+Spoy.noelig']], cat.terms[cat.idx['C8']]
    ca = L.run_big(TP.f_eval, a, b, c, S.KRP)        # a's next is b: a names next at 1/2
    cb = L.run_big(TP.f_eval, b, c, a, S.KRP)        # b's prev is a: b names prev at 1/2
    assert ca[0] == 1 and cb[0] == 4 and ca[2] == 0 and cb[2] == 0


def test_prudent_excludes_bully_and_unplussed():
    TP.install_counter(); S.set_regress(True); S.set_machine('S0')
    cat = _cat()
    p, c8 = cat.terms[cat.idx['Pc+Snoy.canon']], cat.terms[cat.idx['C8']]
    # certified eligibility (the certificate check, not the outcome: fallbacks can still pair, e.g. Pc+'s firm reader with Oc's
    # 1/2 constant): Pc+ requires S_nx of the partner; Oc / Bc see no offer from Pc+ (its requirement is not within h = {})
    for other, elig in (('Bcp.inl', False), ('Ocp.canon', False), ('Oc+p.canon', True), ('Pc+Spoy.rord', True)):
        o = cat.terms[cat.idx[other]]
        h_o = cat.meta[cat.idx[other]]['H']
        sees = S.core_s0(p, 2 if True else 1)[0] == 'T' if h_o == 1 else S.core_s0(p, 1)[0] == 'T'
        req = S.core_s0(o, 5)[0] == 'T'
        assert (sees and req) == elig, (other, sees, req)
        if elig:
            cp = L.run_big(TP.f_eval, p, o, c8, S.KRP)
            co = L.run_big(TP.f_eval, o, c8, p, S.KRP)
            assert cp[0] == 1 and co[0] == 4 and cp[2] == 0 and co[2] == 0
