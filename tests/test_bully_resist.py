"""Queue 76: P, Q, O behave as specified (src/bully_resist.py); V2 (the T+ block is unchanged)."""
import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import bully_resist as BR
import bully_resist_validate as V
import tplus as TP

CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'runs', '_cache')


@pytest.fixture(scope='module')
def tb():
    return BR.TabsBR(cache_dir=CACHE)


def test_count_and_names(tb):
    assert tb.K == 51 and tb.names[:31] == [x[0] for x in TP.library_plus()]
    assert tb.names[31:39] == ['Pnoy', 'Pnon', 'Pnzy', 'Pnzn', 'Ppoy', 'Ppon', 'Ppzy', 'Ppzn']


def test_v2_block(tb):
    tp = TP.TabsPlus(cache_dir=CACHE)
    assert (tb.code[:31, :31, :31] == tp.code).all() and (tb.steps[:31, :31, :31] == tp.steps).all()


def test_prudent_refuses_bullies_accepts_half_constants(tb):
    ix = tb.names.index
    for nm in ('Pnzy', 'Pnzn', 'Ppzy', 'Ppzn', 'Pnon'):
        me = ix(nm); dirn = nm[1]; go = 1 if dirn == 'n' else 4
        for b in ('Bn', 'Bp'):
            for k in range(29):
                nx, pv = (ix(b), k) if dirn == 'n' else (k, ix(b))
                assert tb.code[me, nx, pv] != go
        for k in range(29):
            c = 'C4' if dirn == 'n' else 'C1'
            nx, pv = (ix(c), k) if dirn == 'n' else (k, ix(c))
            assert tb.code[me, nx, pv] == go


def test_lenient_probe_accepts_untested(tb):
    ix = tb.names.index
    me = ix('Qnzy')
    assert any(tb.code[me, ix('Bp'), k] == 1 for k in range(29))
    assert all(tb.code[ix('Pnzy'), ix('Bp'), k] != 1 for k in range(29))


def test_opener_offers_half_to_third_holder(tb):
    ix = tb.names.index
    for nm in BR.NAMES_O:
        me = ix(nm)
        assert tb.code[me, ix('C2'), ix('C3')] == 4          # next names prev at 2/3, prev names next at 1/3
    for nm in ('Onfy', 'Opfn', 'Opfy', 'Onfn'):
        assert tb.code[ix(nm), ix('C0'), ix('C5')] == 1      # next C0 names prev at 1/3, prev C5 names next at 2/3


def test_reference_agrees(tb):
    ix = tb.names.index
    for nm in ('Pnzn', 'Ppoy', 'Qpzy'):
        me = ix(nm)
        for j in range(29):
            for k in range(0, 29, 3):
                r = V.ref_prudent(tb, me, j, k, nm[1], nm[2], nm[3], nm[0] == 'Q')
                if r is not None and not tb.fo[me, j, k]:
                    assert r == tb.code[me, j, k]
    for nm in ('Onfy', 'Opzn'):
        me = ix(nm)
        for j in range(29):
            for k in range(0, 29, 3):
                r = V.ref_opener(tb, me, j, k, nm[1], nm[2], nm[3])
                if r is not None and not tb.fo[me, j, k]:
                    assert r == tb.code[me, j, k]
