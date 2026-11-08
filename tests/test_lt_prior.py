"""Tests for the length prior over L_T syntax (queue 75 step 1: src/lt_prior.py, lt_prior_enum.py, lt_prior_search.py).
V3 (mass formula, mass bookkeeping of the exhaustive part), V4 (classification of the library by the probe set), the
read macro, the taint rule and the adaptive probe table, and the composition of the targeted search against evaluation."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import pytest
import lt_code as L
import lt_prior as P
import lt_prior_enum as E
import lt_prior_search as S
import churn_primary_t as CT


def test_elias_and_literal_classes():
    assert abs(sum(P.elias(n) for n in range((1 << 14) - 1)) - (1 - 2.0 ** -14)) < 1e-9
    assert abs(sum(m for _, _, m in P.LIT_CLASSES) - 1.0) < 1e-12
    assert abs(P.elias_range(1, 1) - 0.5) < 1e-15 and abs(P.elias_range(2, 3) - 0.25) < 1e-15


def test_criticality_and_finite_mass():
    assert abs(P.R0.mean_arity - 24 / 18) < 1e-12
    q0, q1 = P.R0.extinction(), P.R1.extinction()
    assert abs(q0 - (-7 + math.sqrt(97)) / 6) < 1e-9        # 3q^2 + 7q - 4 = 0
    assert abs(q1 - 2 / 3) < 1e-9                           # 3q^2 + 7q - 6 = 0
    for m, q in ((P.R0, q0), (P.R1, q1)):
        sm = m.size_masses(120)
        assert abs(sum(sm) - q) < 5e-3 * q and sum(sm) <= q + 1e-12


def _bodies():
    pr = P.probes()
    return [(n, t[1][1][1]) for n, t in zip(pr.members[:27], pr.mterm[:27])]


def test_v3_mass_formula_library():
    for n, body in _bodies():
        for m in (P.R0, P.R1):
            a = P.term_mass(body, m); b = P.mass_formula(body, m)
            assert abs(a - b) <= 1e-12 * b, n
    # a constant is a single node
    assert P.node_count(_bodies()[3][1]) == 1


def test_v3_enumerated_mass_adds_up():
    for mn in ('R0', 'R1'):
        mach = P.MACHINES[mn]
        sm = mach.size_masses(4, tags=P.ENUM_TAGS[mn])
        en = E.Enumerator(mach)
        for s in range(1, 4):
            tot = sum(m for _, m in en.get(s, 0))
            assert abs(tot - sm[s]) < 1e-12, (mn, s, tot, sm[s])


def test_v4_library_classification():
    pr = P.probes()
    fam = {'const': 'const', 'single': 'single_fair', 'two': 'two_fair', 'exploit': 'exploit', 'bully': 'bully',
           'junk_f': 'junk_f', 'junk_r': 'junk_r'}
    for i, (n, f) in enumerate(zip(pr.members, pr.mfam)):
        lab, exact = P.classify_table(pr.table(pr.mterm[i]), pr)
        assert exact == n and lab.startswith(fam[f]), (n, lab, exact)


def test_read_macro_matches_library_reader():
    # R1 inline reader `if (eq readn 4) 1 4` has exactly the table of the library reader Snon
    pr = P.probes()
    body = ('if', ('eq', ('readn',), ('nat', 4)), ('nat', 1), ('nat', 4))
    lab, exact, _ = P.classify_body(body, P.R1, pr)
    assert (lab, exact) == ('single_fair:n', 'Snon')
    body = ('if', ('eq', ('readp',), ('nat', 1)), ('nat', 4), ('nat', 1))
    lab, exact, _ = P.classify_body(body, P.R1, pr)
    assert (lab, exact) == ('single_fair:p', 'Spon')
    # the Trojan bully in R1: if (eq readn 3) 2 4
    lab, exact, _ = P.classify_body(('if', ('eq', ('readn',), ('nat', 3)), ('nat', 2), ('nat', 4)), P.R1, pr)
    assert (lab, exact) == ('bully:n', 'Bn')


def test_taint_and_adaptive_table():
    pr = P.probes()
    c0 = pr.terms[0]
    r = P.eval_prog(pr.mterm[3], c0, c0, taint=True)            # constant: partners untouched
    assert r[5] == (False, False)
    r = P.eval_prog(pr.mterm[pr.members.index('Snon')], c0, c0, taint=True)   # reader: runs next
    assert r[5][0]
    for nm in ('Snon', 'Dnfy', 'Spzy', 'Xp'):
        prog = pr.mterm[pr.members.index(nm)]
        r = P.eval_prog(prog, c0, c0, taint=True)
        a, ne = pr.table_adaptive(prog, r[5])
        assert pr.signature(a) == pr.signature(pr.table(prog)), nm
    # a source inspector is tainted: fst n is the tag of the partner's term (lam = 1), a constant output
    body = ('fst', ('v', 1))
    lab, exact, _ = P.classify_body(body, P.R0, pr)
    assert lab == 'const:1'


def test_static_junk_is_junk():
    pr = P.probes()
    c0 = pr.terms[0]
    for body in [('app', ('nat', 3), ('nat', 4)), ('if', ('nat', 1), ('nat', 2), ('nat', 3)), ('con', 'C'),
                 ('fst', ('nat', 0)), ('op', 'add', ('con', 'T'), ('nat', 1)), ('op', 'le', ('nat', 1), ('nat', 2))]:
        assert P.static_junk(body)
        cd, nt, f, _, _, _ = P.eval_prog(P.frame(P.expand(body)), c0, c0)
        assert f == 1


def test_search_composition_matches_evaluation():
    pr = P.probes()
    rd = S.Reads(P.R1)
    # let r = readn in if (eq r 4) 1 4  composed vs evaluated
    F = ('if', ('eq', S.R, ('nat', 4)), ('nat', 1), ('nat', 4))
    mp = S.rmap(F)
    tab = S.tab1(rd, 0, mp)
    body = ('app', ('lam', F), ('readn',))
    real = pr.table(P.frame(P.expand(body)))
    assert pr.signature(tab) == pr.signature(real)
    # two-stage: reader Dnfy-like (accept 4 or TO on next -> 1; else read prev, accept 1 or TO -> 4, else 1)
    acc = lambda k: ('if', ('eq', S.R, ('nat', k)), ('con', 'T'), ('eq', S.R, S.TO))
    F1 = ('if', acc(4), ('nat', 1), ('cont',))
    F2 = ('if', acc(1), ('nat', 4), ('nat', 1))
    m1, m2 = S.rmap(F1), S.rmap(F2)
    t2 = S.tab2(rd, 0, 1, m1, m2)
    body = ('app', ('lam', ('if', acc(4), ('nat', 1), ('app', ('lam', F2), ('readp',)))), ('readn',))
    real = pr.table(P.frame(P.expand(body)))
    assert pr.signature(t2) == pr.signature(real)
    lab, exact = P.classify_table(t2, pr)
    assert exact == 'Dnfy'


def test_sampler_literals_and_scope():
    sm = E.Sampler(P.R0, 3)
    # Elias sampler: P(0) = 1/2, P(1) = P(2) = 1/8
    xs = [sm.elias() for _ in range(40000)]
    assert abs(xs.count(0) / 40000 - 0.5) < 0.01 and abs(xs.count(1) / 40000 - 0.125) < 0.01
    assert E.scope_fix(('v', 5)) == ('oos',) and E.scope_fix(('lam', ('v', 3))) == ('lam', ('v', 3))


def test_adaptive_table_random():
    """the taint rule (a run that never inspects a partner's source is the same for every partner) against the full
    probe tables, on random tainted programs of both machines (and with R1's read macro)."""
    pr = P.probes()
    c0 = pr.terms[0]
    for mn, seed in (('R0', 11), ('R1', 12)):
        mach = P.MACHINES[mn]
        sm = E.Sampler(mach, seed)
        got = tries = 0
        while got < 12 and tries < 100000:
            tries += 1
            t, sz = sm.draw()
            if t is None:
                continue
            body = E.scope_fix(t)
            if P.static_junk(body):
                continue
            prog = P.frame(P.expand(body))
            r = P.eval_prog(prog, c0, c0, taint=True)
            if not (r[5][0] or r[5][1]):
                continue
            got += 1
            a, _ = pr.table_adaptive(prog, r[5])
            assert pr.signature(a) == pr.signature(pr.table(prog)), P.to_sexpr(body)
        assert got == 12


def test_r1_fast_and_hybrid_tables():
    """R1 read macro: bodies whose only partner contact is through the read leaves are evaluated once per read outcome
    (fast_table_r1), those that also refer to n / p per profile with the reads replaced by their outcomes
    (hybrid_table_r1); both equal the real 29 x 29 table."""
    pr = P.probes()
    cases = [('if', ('eq', ('readn',), ('nat', 4)), ('nat', 1), ('nat', 4)),
             ('add', ('readp',), ('nat', 2)) if False else ('op', 'add', ('readp',), ('nat', 2)),
             ('app', ('lam', ('v', 0)), ('readn',)),
             ('op', 'add', ('readp',), ('fst', ('v', 1))),
             ('if', ('eq', ('readn',), ('v', 0)), ('nat', 1), ('nat', 4))]
    for body in cases:
        acc = {}
        P._scan(body, 0, acc)
        real = pr.table(P.frame(P.expand(body)))
        if not acc.get('bad'):
            tab = P.fast_table_r1(body, acc, pr)
        else:
            assert acc.get('badref') and not acc.get('badtag')
            tab = P.hybrid_table_r1(body, acc, pr)
        assert pr.signature(tab) == pr.signature(real), P.to_sexpr(body)
