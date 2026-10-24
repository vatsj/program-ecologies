"""Tests for src/zero_tolerance.py: the payoffs of zt, cr_s, zt_s, sr_k and the unconditional inspector against constants, light cheaters, the
stored bounded-read exploiters and mutual readers (hand table, notes/zero-tolerance.md section 1); the kernel-based rows against an independent
scalar evaluator (tests/zt_reference.py); the stored-operator self-tests (the machinery reproduces the stored `cr(THEM(ME))` and `RI` rows); the
q thresholds of sr_k; behavioural classes; the matched prior; the replaced-founder coupling; the resident-specific exit categories."""
import os, sys, math
import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'src'))
sys.path.insert(0, HERE)
import mixed2 as M
import inspection_shadow as S
import zero_tolerance as Z
import zt_reference as R
from zt_reference import C0, C1, X, ME, coin, cr, zt, crs, zts, sr, srs, ife, up

SPEC = {'zt': zt(ME), 'crs': crs(ME), 'zts': zts(ME), 'sr1': sr(1, ME), 'sr4': sr(4, ME), 'sr16': sr(16, ME),
        'sr1s': srs(1, ME), 'sr4s': srs(4, ME), 'sr16s': srs(16, ME), 'cr': cr(ME)}


def light(q):
    return {1 / 16: coin(C0, coin(C0, coin(C0, X))), 1 / 8: coin(C0, coin(C0, X)), 3 / 16: coin(C0, coin(C0, coin(C1, X))), 1 / 4: coin(C0, X)}[q]


def pay(P, Q):
    r = R.payoffs(P, Q)
    return r['u0'], r['u1']


# ---------------------------------------------------------------------------------------------- hand table (closed forms)
def test_constants_closed_forms():
    for name in ('zt', 'crs', 'zts', 'cr', 'sr1', 'sr4', 'sr16', 'sr1s', 'sr4s', 'sr16s'):
        assert pay(SPEC[name], C0) == pytest.approx((0, 0)), name                    # compliant inspectee: never inspected
        assert pay(SPEC[name], C1) == pytest.approx((-1, -3)), name                  # constant cheater: inspected
    assert pay(C0, C0) == (-1, 0) and pay(C1, C0) == (0, 0)                           # I and N against C
    assert pay(C0, C1) == (-1, -3) and pay(C1, C1) == (-4, 1)


def test_light_cheaters_closed_forms():
    for q in (1 / 16, 1 / 8, 3 / 16):
        # exact reader: tolerates q < 1/4; zero tolerance inspects; unconditional inspector inspects
        assert pay(cr(ME), light(q)) == pytest.approx((-4 * q, q))
        for name in ('zt', 'zts'):
            assert pay(SPEC[name], light(q)) == pytest.approx((-1, -3 * q))
        assert pay(C0, light(q)) == pytest.approx((-1, -3 * q))
        assert pay(C1, light(q)) == pytest.approx((-4 * q, q))
        # sampling: p_k = 1 - (1 - q)^k
        for k, name in ((1, 'sr1'), (4, 'sr4'), (16, 'sr16')):
            p = 1 - (1 - q) ** k
            assert pay(SPEC[name], light(q)) == pytest.approx((-p - 4 * (1 - p) * q, q * (1 - 4 * p)))
            assert pay(SPEC[name + 's'], light(q)) == pytest.approx(pay(SPEC[name], light(q)))      # no timeouts against a non-reader
    # at exactly q = 1/4 the exact reader mixes 1/2 : 1/2; sr_1 inspects with probability 1/4
    assert pay(cr(ME), light(1 / 4)) == pytest.approx((-1, -0.25))
    assert pay(sr(1, ME), light(1 / 4)) == pytest.approx((-1, 0))
    # X (q = 1/2)
    assert pay(sr(1, ME), X) == pytest.approx((-1.5, -0.5)) and pay(sr(4, ME), X) == pytest.approx((-1.0625, -1.375))


def test_sr_thresholds():
    for k, th in ((1, 0.25), (4, 0.0694), (16, 0.0178)):
        qs = 1 - 0.75 ** (1.0 / k)
        assert qs == pytest.approx(th, abs=5e-5)
        # a cheater with q just below the threshold gains, just above loses
        assert 1 - (1 - qs * 0.99) ** k < 0.25 + 1e-9 and (qs * 0.99) * (1 - 4 * (1 - (1 - qs * 0.99) ** k)) > 0
        assert (qs * 1.01) * (1 - 4 * (1 - (1 - qs * 1.01) ** k)) < 0
    # grammar mixers (n = 8): q = 1/16 is the smallest; it gains against sr_1, sr_4 and loses against sr_16
    u1 = {name: pay(SPEC[name], light(1 / 16))[1] for name in ('sr1', 'sr4', 'sr16')}
    assert u1['sr1'] > 0 and u1['sr4'] > 0 and u1['sr16'] < 0


def test_costs():
    r = R.payoffs(SPEC['sr16'], C0)
    assert r['e0'] == pytest.approx(16.0) and R.payoffs(SPEC['sr4'], C0)['e0'] == pytest.approx(4.0)
    assert R.payoffs(SPEC['sr16'], C1)['e0'] == pytest.approx(1.0)                 # stops at the first cheating draw
    assert R.payoffs(SPEC['sr4'], X)['e0'] == pytest.approx(1.875) and R.payoffs(SPEC['sr16'], X)['e0'] == pytest.approx(2.0, abs=1e-3)
    for name in ('zt', 'crs', 'zts', 'cr'):
        assert R.payoffs(SPEC[name], C0)['e0'] == pytest.approx(1.0)
    assert R.payoffs(C0, C0)['e0'] == 0.0


def test_exploiter_phase():
    ex = cr(coin(C1, ME))
    # D = 12: the stored exploiter beats cr and zt and loses to the suspicious variants
    assert pay(cr(ME), ex)[1] == pytest.approx(0.9918, abs=1e-3) and pay(zt(ME), ex)[1] == pytest.approx(0.9918, abs=1e-3)
    assert pay(crs(ME), ex) == pytest.approx((-1, -3)) and pay(zts(ME), ex) == pytest.approx((-1, -3))
    assert pay(sr(16, ME), ex)[1] < 0 < pay(sr(4, ME), ex)[1]
    ex2 = cr(coin(C1, coin(X, ME)))
    assert pay(sr(16, ME), ex2)[1] == pytest.approx(0.791, abs=2e-3)               # sr_16 is not immune
    old = R.D
    try:
        R.D = 11
        assert pay(crs(ME), ex)[1] == pytest.approx(1.0, abs=1e-6) and pay(cr(ME), ex)[1] == pytest.approx(0.0, abs=2e-3)
        R.D = 13
        assert pay(crs(ME), ex)[1] == pytest.approx(0.0, abs=1e-6)
    finally:
        R.D = old


def test_mutual_readers_forfeit_under_cr_not_under_suspicious():
    mr = cr(ME)                                                        # the mutual-reading inspectee
    r = R.payoffs(cr(ME), mr)
    assert r['f0'] == pytest.approx(1.0) and r['f1'] == pytest.approx(1.0) and (r['u0'], r['u1']) == pytest.approx((-4, -3))
    r = R.payoffs(zt(ME), mr)
    assert r['f0'] == pytest.approx(1.0)
    r = R.payoffs(crs(ME), mr)
    assert r['f0'] == 0.0 and r['f1'] == 0.0 and (r['u0'], r['u1']) == pytest.approx((-1, -3))


# ---------------------------------------------------------------------------------------------- the kernel-based rows
@pytest.fixture(scope='module')
def lang_ev():
    return Z.base_eval(12, keep=True)


def to_ast(lang, e):
    o = lang.op[e]
    if o == M.OP_C0: return C0
    if o == M.OP_C1: return C1
    if o == M.OP_X: return X
    if o == M.OP_COIN: return coin(to_ast(lang, lang.A[e]), to_ast(lang, lang.B[e]))
    if o == M.OP_CR: return cr(to_ast(lang, lang.A[e]))
    if o == M.OP_IF: return ife(to_ast(lang, lang.C[e]), to_ast(lang, lang.A[e]), to_ast(lang, lang.B[e]))
    if o == M.OP_APP: return ME if lang.K[e] == M.APP_ME else up(to_ast(lang, lang.B[e]))
    raise ValueError(o)


def test_machinery_reproduces_stored_operators(lang_ev):
    lang, ev = lang_ev
    pcri = M.prog_of(lang, 0, ('cr', M.APPME)); pri = M.prog_of(lang, 0, ('if', M.APPME, 'c1', 'c0'))
    for name, p in (('cr', pcri), ('sr1', pri)):
        r = Z.added_rows(name, 12)
        for k in ('U0', 'E0', 'F0'):
            assert np.abs(r[k] - ev[k][p]).max() == 0.0, (name, k)
        for k in ('U1', 'E1', 'F1'):
            assert np.abs(r[k] - ev[k][:, p]).max() == 0.0, (name, k)
        assert np.abs(r['G0'] - ev['G0'][p]).max() == 0.0 and np.abs(r['G1'] - ev['G1'][:, p]).max() == 0.0
        assert np.abs(r['prevG0'] - ev['prevG0'][p]).max() == 0.0 and np.abs(r['prevG1'] - ev['prevG1'][:, p]).max() == 0.0


def test_rows_equal_the_scalar_evaluator(lang_ev):
    lang, ev = lang_ev
    asts = [to_ast(lang, e) for e in lang.progs[1]]
    idx = np.random.default_rng(5).choice(len(asts), 150, replace=False)
    for name in ('zt', 'crs', 'zts', 'sr1', 'sr4', 'sr16', 'sr1s', 'sr4s', 'sr16s'):
        r = Z.added_rows(name, 12)
        for j in idx:
            q = R.payoffs(SPEC[name], asts[j])
            for a, b in ((q['u0'], r['U0'][j]), (q['u1'], r['U1'][j]), (q['f0'], r['F0'][j]), (q['f1'], r['F1'][j]), (q['e0'], r['E0'][j]), (q['e1'], r['E1'][j])):
                assert abs(a - b) <= 1e-9 * max(1.0, abs(a)), (name, j)


# ---------------------------------------------------------------------------------------------- classes and priors
_arm = {}


def arm(tag, c=0.0):
    if (tag, c) not in _arm:
        _arm[(tag, c)] = Z.get_arm_zt(tag, c)
    return _arm[(tag, c)]


def test_validation_arm_is_the_stored_table():
    A, B = arm('v0'), M.get_arm('insp', 'exact', 8, 0.0)
    assert A.K == B.K and np.abs(A.UA - B.UA).max() == 0 and np.abs(A.UB - B.UB).max() == 0 and np.abs(A.mass[0] - B.mass[0]).max() == 0
    assert np.abs(A.CA - B.CA).max() == 0 and np.abs(A.G0 - B.G0).max() == 0


def test_behavioural_classes_of_the_added_programs():
    base = arm('v0')
    nm = S.named(base)
    A = arm('sr1')
    assert A.K == base.K                                                            # sr_1 is the stored sampled responder: no new class
    assert A.zt['added'][0]['cls'] == S.named(A)['0RI'] and not A.zt['added'][0]['new_class']      # the class of the stored RI (its representative is now the smaller sr1 spelling)
    assert A.zt['added'][0]['cls_rep'] == 'sr1(THEM(ME))' and A.zt['added'][0]['n_members'] == 12
    for tag in ('zt', 'sus', 'ztsus', 'sr4', 'sr16'):
        B = arm(tag)
        assert B.K[0] == base.K[0] + 1 and B.K[1] == base.K[1]                       # a new inspector class, no inspectee class splits at c = 0
        assert B.zt['added'][0]['new_class'] and B.zt['added'][0]['n_members'] == 1
    assert arm('sr4', 0.01).K[1] > arm('v0', 0.01).K[1]                              # at c = 0.01 the k-fold read splits inspectee classes


def test_matched_prior():
    base = arm('v0')
    nm = S.named(base)
    m = base.mass[0][nm['0CRI']]
    for tag in ('zt', 'sus', 'ztsus', 'sr4', 'sr16'):
        A = arm(tag)
        assert A.zt['m'] == pytest.approx(m)
        a = A.zt['added'][0]['cls']
        assert A.mass[0][a] == pytest.approx(m)                                      # the whole added mass on the one added program
        assert A.mass[0].sum() == pytest.approx(1.0) and A.mass[1].sum() == pytest.approx(1.0)
        nmA = S.named(A)
        for key in ('0N', '0I', '0CRI'):
            assert A.mass[0][nmA[key]] == pytest.approx(base.mass[0][nm[key]] * (1 - m))      # other inspector classes shrink proportionally
        assert np.allclose(A.mass[1], base.mass[1])                                  # the inspectee prior is untouched
    C = arm('ctl'); nmC = S.named(C)
    assert C.mass[0][nmC['0CRI']] == pytest.approx(base.mass[0][nm['0CRI']] * (1 - m) + m)
    assert C.mass[0][nmC['0N']] == pytest.approx(base.mass[0][nm['0N']] * (1 - m))
    U = arm('unc'); nmU = S.named(U)
    assert U.mass[0][nmU['0I']] == pytest.approx(base.mass[0][nm['0I']] * (1 - m) + m)
    # sr1 adds its mass to the class of RI
    R1 = arm('sr1'); nm1 = S.named(R1)
    assert R1.mass[0][nm1['0RI']] == pytest.approx(base.mass[0][nm['0RI']] * (1 - m) + m)


def test_fixed_reference_embedding_conserves_mass():
    c, z = arm('ctl'), arm('zt')
    pi = np.random.default_rng(0).random(c.K); pi /= pi.sum()
    out, kept = Z._embed(pi, c.names, z.names)
    assert kept == pytest.approx(1.0) and out.shape == tuple(z.K) and out.sum() == pytest.approx(1.0)
    assert out[z.zt['added'][0]['cls']].sum() == 0.0


# ---------------------------------------------------------------------------------------------- strict invaders and exits
def test_strict_invaders_of_the_resident():
    for tag, a_lab in (('v0', 'CRI'), ('zt', 'zt'), ('sus', 'crs'), ('ztsus', 'zts')):
        A = arm(tag); nm = S.named(A)
        a = nm['0CRI'] if a_lab == 'CRI' else A.zt['added'][0]['cls']
        C_ = nm['1C']
        inv = np.nonzero(A.UB[:, a] - A.UB[C_, a] > 1e-9)[0]
        nonread = [b for b in inv if not A.reader[1][b]]
        read = [b for b in inv if A.reader[1][b]]
        if a_lab == 'CRI':
            assert A.mass[1][nonread].sum() == pytest.approx(0.002916, abs=1e-6) and A.mass[1][read].sum() == pytest.approx(0.000177, abs=1e-6)
        elif a_lab == 'zt':
            assert len(nonread) == 0 and A.mass[1][read].sum() == pytest.approx(0.000141, abs=1e-6)          # no light cheater invades zero tolerance
        elif a_lab == 'crs':
            assert A.mass[1][nonread].sum() == pytest.approx(0.002916, abs=1e-6) and len(read) == 0             # light cheaters yes, the exploiters no
        else:
            assert len(inv) == 0                                                                                  # neither
    A = arm('sr16'); a = A.zt['added'][0]['cls']; C_ = S.named(A)['1C']
    inv = np.nonzero(A.UB[:, a] - A.UB[C_, a] > 1e-9)[0]
    assert all(A.reader[1][b] for b in inv)                                                                       # no non-reading invader of sr_16


def test_resident_exit_categories_partition_and_match_reference():
    A = arm('zt'); nm = S.named(A); fl = S.class_flags(A)
    N = 10000
    for lab, a, b in (('(CRI,C)', nm['0CRI'], nm['1C']), ('(N,C)', nm['0N'], nm['1C']), ('(zt,C)', A.zt['added'][0]['cls'], nm['1C'])):
        r = Z.resident_exits(A, N, a, b, fl)
        assert sum(r['cats'].values()) == pytest.approx(r['total'])
        ref = S.reference_exits(A, N, a, b)
        assert r['total'] == pytest.approx(ref['total'], rel=1e-9)
    r = Z.resident_exits(A, N, nm['0CRI'], nm['1C'], fl)
    assert r['cats']['A_neutral_shadow'] == pytest.approx(1.546e-5, rel=0.02)         # the stored shadow drift (the added mass changes it by 0.14%)
    z = Z.resident_exits(A, N, A.zt['added'][0]['cls'], nm['1C'], fl)
    assert z['cats']['D_strict_nonreader'] == 0.0 and z['cats']['E_strict_reader'] > 0


# ---------------------------------------------------------------------------------------------- the coupled founders
def test_founder_coupling():
    base = arm('v0'); lang0 = Z.base_lang(12)
    I, N = 8, 100
    seed0 = M.run_seed('found|primary|3|0', 0); seed1 = M.run_seed('found|primary|3|1', 0)
    f0, f1, nrep = Z.founders_coupled(base, lang0, I, N, seed0, seed1)
    assert nrep == 0 and (f0 == M.draw_founders(lang0, 0, base.cls_of[0], base.K[0], I, N, seed0)).all()      # the validation arm is the stored draw
    assert (f1 == M.draw_founders(lang0, 1, base.cls_of[1], base.K[1], I, N, seed1)).all()
    A = arm('zt')
    g0, g1, nrep = Z.founders_coupled(A, lang0, 400, 100, seed0, seed1)
    assert abs(nrep / (400 * 100) - A.zt['m']) < 4 * math.sqrt(A.zt['m'] / (400 * 100))
    assert g0[:, A.zt['added'][0]['cls']].sum() == nrep                                                          # every replaced slot is the added program
    h0, _, nrep2 = Z.founders_coupled(arm('sus'), lang0, 400, 100, seed0, seed1)
    assert nrep2 == nrep                                                                                           # arms share the replaced slots
    # outside the replaced slots the founders are the stored draw
    cl = base.cls_of[0][Z.slot_programs(lang0, 0, 400, 100, seed0)].reshape(400, 100)
    assert (cl.sum() > 0)
