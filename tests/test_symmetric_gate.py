"""Unit tests for the access rules of the symmetric gate (src/symmetric_gate.py).

Reciprocal and nested queries under each rule: a non-carrier's box about a carrier, a non-carrier's box about a
carrier's play toward a third party or toward a carrier (contract-level) and toward the reader itself (the carrier's
own box about the reader, evaluated under the carrier's access), literal targets, constants, the carrier block.
"""
import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import contracts as CT
import symmetric_gate as SG

RUNS = os.path.join(os.path.dirname(__file__), '..', 'runs')


@pytest.fixture(scope='module')
def T():
    C = SG.setup()
    out = {}
    for b, bl in ((0, '0'), (CT.INF, 'inf')):
        for rule in SG.RULES:
            if bl == 'inf' and rule.startswith('q'):
                continue
            val, info, aux = SG.evaluate(C, b, rule)
            out[(bl, rule)] = (val, aux, SG.audit(C, val, aux))
    return C, out


def ty(C, name, carrier):
    p = C.names.index(name)
    return int(C.cs_type[p]) if carrier else p


def test_asym_reproduces_published_tables(T):
    C, out = T
    assert (out[('0', 'asym')][0] == np.load(os.path.join(RUNS, 'contracts_types_b0.npz'))['val_0']).all()
    assert (out[('inf', 'asym')][0] == np.load(os.path.join(RUNS, 'contracts_types.npz'))['val_inf']).all()


def test_audit_sound_every_rule(T):
    C, out = T
    for k, (val, aux, a) in out.items():
        assert a['contract_violations'] == 0 and a['source_violations'] == 0, k
        assert a['carrier_pairs_off_table'] == 0 and a['recompute_mismatch'] == 0, k


def test_carrier_block_rule_independent(T):
    C, out = T
    car = C.tcon >= 0
    for bl in ('0', 'inf'):
        ref = out[(bl, 'asym')][0]
        for rule in SG.RULES:
            if (bl, rule) in out:
                assert (out[(bl, rule)][0][np.ix_(car, car)] == ref[np.ix_(car, car)]).all()
    # b = 0: also the carrier rows against non-carriers and the non-carrier block
    ref = out[('0', 'asym')][0]
    for rule in SG.RULES:
        v = out[('0', rule)][0]
        assert (v[car] == ref[car]).all()
        assert (v[np.ix_(~car, ~car)] == ref[np.ix_(~car, ~car)]).all()


def test_reciprocal_fairbot(T):
    """FairBot non-carrier vs FairBot carrier: the non-carrier's atom targets itself (no contract), so it is a source
    read; the carrier's box about it is the carrier's own execution under its access."""
    C, out = T
    fn, fc = ty(C, CT.FB, False), ty(C, CT.FB, True)
    for rule in SG.RULES:
        v = out[('0', rule)][0]
        assert v[fn, fc] == 0 and v[fc, fn] == 0          # b = 0: mutually illegible
        assert v[fc, fc] == 1
    for rule in ('asym', 'sym'):
        v = out[('inf', rule)][0]
        assert v[fn, fc] == 1 and v[fc, fn] == 1          # b = inf: Löbian cooperation across the access boundary


@pytest.mark.parametrize('name', ['BOX(THEM(THEM))', 'BOX(THEM(^C))', 'BOXD1(THEM(^D))'])
def test_fringe_nested(T, name):
    """A non-carrier's box about a carrier's play (toward itself or a literal carrier): contract read under asym,
    masked under sym at b = 0; the carrier defects on the reader under both rules."""
    C, out = T
    t, fc = ty(C, name, False), ty(C, CT.FB, True)
    a = out[('0', 'asym')][0]; s = out[('0', 'sym')][0]
    assert a[t, fc] == 1 and s[t, fc] == 0
    assert a[fc, t] == 0 and s[fc, t] == 0


def test_constants_legible_under_every_rule(T):
    C, out = T
    t = ty(C, 'BOX(THEM(THEM))', False)
    dc, cc = ty(C, 'D', True), ty(C, 'C', True)
    for rule in SG.RULES:
        v = out[('0', rule)][0]
        assert v[t, dc] == 0 and v[t, cc] == 1


def test_quenched_rows(T):
    """Under q, a non-carrier whose source reads contracts plays its asym row; any other plays its sym row."""
    C, out = T
    a = out[('0', 'asym')][0]; s = out[('0', 'sym')][0]
    r25 = SG.reads_assignment(C.K, 0.25); r50 = SG.reads_assignment(C.K, 0.5)
    assert (r25 <= r50).all()
    for rule, r in (('q0.25', r25), ('q0.5', r50)):
        v = out[('0', rule)][0]
        for p in range(C.K):
            assert (v[p] == (a[p] if r[p] else s[p])).all()
        rc = SG.rc_for(C, rule)
        assert (rc[C.tcon >= 0] == 1).all()
