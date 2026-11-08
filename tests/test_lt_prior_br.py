"""Queue 76 step 2: R2's probe tag against the explicit implementation (V3-type equivalence), V4 (member bodies classify as their own
family), opener templates, R2's size masses."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import pytest
import lt_code as L
import lt_prior as P
import lt_prior_search as S
import churn_primary_t as CT
import bully_resist as BR
import lt_prior_br as B


def test_probe_tag_expansion_is_the_explicit_read():
    for dirn, src in (('n', BR.PROBEN), ('p', BR.PROBEP)):
        term = P.frame(P.expand(('probn' if dirn == 'n' else 'probp', ('nat', 3 if dirn == 'n' else 0))))
        expl = CT._prog('(lambda (me n p) %s)' % src)
        assert term == expl
    assert P.expand(('probn', ('v', 0))) == ('fst', ('nat', 0))
    assert P.expand(('probn', ('nat', 12))) == ('fst', ('nat', 0))


def test_probe_tag_table_equals_explicit_table():
    pr = B.extend_probes()
    for dirn, tag, code in (('n', 'probn', 3), ('p', 'probp', 0)):
        rc_tag, nto_tag = B.read_table(pr, (tag, ('nat', code)))
        explicit = ('capk', ('nat', 400), ('run', ('nat', 400), ('v', 1), B.const_quote(code)), ('v', 2)) if dirn == 'n' else \
            ('capk', ('nat', 400), ('run', ('nat', 400), ('v', 0), ('v', 2)), B.const_quote(code))
        rc_e, nto_e = B.read_table(pr, explicit)
        assert (rc_tag == rc_e).all() and (nto_tag == nto_e).all()
        for b in range(0, 29, 3):
            for c in range(0, 29, 3):
                a = P.eval_prog(P.frame(P.expand((tag, ('nat', code)))), pr.terms[b], pr.terms[c])
                e = P.eval_prog(P.frame(explicit), pr.terms[b], pr.terms[c])
                assert a[:4] == e[:4]


def test_r2_size_masses_and_arity():
    R2 = P.MACHINES['R2']
    assert R2.T == 22 and abs(R2.mean_arity - 26 / 22) < 1e-12
    q = R2.extinction()
    assert 0 < q < 1 and abs(R2.gf(q) - q) < 1e-12
    sm = R2.size_masses(60)
    assert sum(sm) <= q + 1e-12


def test_prudent_member_bodies_classify_as_themselves():
    pr = B.extend_probes()
    R2 = P.MACHINES['R2']
    for name in BR.NAMES_P + BR.NAMES_Q:
        dirn, fb, to = name[1], name[2], name[3]
        rd = ('readn',) if dirn == 'n' else ('readp',)
        pbt = ('probn', ('nat', 3)) if dirn == 'n' else ('probp', ('nat', 0))
        go = 1 if dirn == 'n' else 4; other = 4 if dirn == 'n' else 1; ex = 2 if dirn == 'n' else 5
        f = {'o': other, 'z': 8}[fb]
        acc4 = 4 if dirn == 'n' else 1
        cond1 = ('eq', ('v', 0), ('nat', acc4)) if to == 'n' else ('if', ('eq', ('v', 0), ('nat', acc4)), ('con', 'T'), ('eq', ('v', 0), ('con', 'TO')))
        bad = ('eq', ('v', 0), ('nat', ex)) if name[0] == 'Q' else ('if', ('eq', ('v', 0), ('nat', ex)), ('con', 'T'), ('eq', ('v', 0), ('con', 'TO')))
        inner = ('app', ('lam', ('if', bad, ('nat', f), ('nat', go))), pbt)
        body = ('app', ('lam', ('if', cond1, inner, ('nat', f))), rd)
        fam, exact, _ = L.run_big(P.classify_body, body, R2, pr)
        twins = [m for ids_ in pr.sig2member.values() if name in [pr.members[i] for i in ids_] for m in [pr.members[i] for i in ids_]]
        assert exact in twins, (name, exact, twins)       # Q with timeouts rejected is table-equal to P (Qnzn = Pnzn): classified by the first member


def test_opener_template_classifies_for_every_member_r2():
    R2 = P.MACHINES['R2']
    for name in BR.NAMES_O:
        r = L.run_big(B.opener_search, R2, name, (383, 1500), 3)
        assert r['count'] > 0 and r['mass'] > 0 and r['shortest'][0] >= 30, (name, r['count'])


def test_bully_and_fair_reader_unchanged_by_extended_members():
    pr = B.extend_probes()
    R1 = P.MACHINES['R1']
    fam, exact, _ = L.run_big(P.classify_body, ('if', ('eq', ('readn',), ('nat', 4)), ('nat', 1), ('nat', 4)), R1, pr)
    assert exact == 'Snon'
    fam, exact, _ = L.run_big(P.classify_body, ('if', ('eq', ('readn',), ('nat', 3)), ('nat', 2), ('nat', 4)), R1, pr)
    assert exact == 'Bn'
