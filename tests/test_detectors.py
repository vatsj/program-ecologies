"""Tests for legitimate detectors (notes/detectors.md).  The term-level tests run anywhere; the population tests need
the untracked cached tables (runs/provenance/static, runs/detectors/K) and skip without them."""
import os
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import detectors as DT
import lt_code as L
import lt_cert as C

HAVE_L = os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'static', 'A.npy'))
HAVE_K = os.path.exists(os.path.join(ROOT, 'runs', 'detectors', 'K', 'grudge.npz'))


@pytest.fixture(scope='module')
def progs():
    DT.install_library('key')
    cat, names = DT.catalogue()
    prod = C.Producer(host=__import__('carrier_populations').ExactHost())
    det0 = DT.prog(cat, names, DT.DET_SP)
    delta = prod.produce(0, det0, L.PROG_D, 'D', DT.K, DT.V)
    P = DT.prog(cat, names, 'if(CHK(them,me,C),D,C)')
    syn = DT.synonyms(cat, names, 'if(CHK(them,me,C),D,C)')[0]
    return dict(cat=cat, names=names, delta=delta, P=P, Psyn=DT.prog(cat, names, syn), Cb=DT.prog(cat, names, 'C'))


def test_grudge_sound_and_self_fulfilling(progs):
    p = progs
    kP = DT.key_of(p['P'])
    det = DT.prog(p['cat'], p['names'], DT.DET_SP, [('D', DT.keyed(p['delta'], DT.KEY_D)), ('D', DT.keyed(p['delta'], kP))])
    v, n = DT.chk(det, p['P'], 'D')
    assert v == 'T' and DT.play(det, p['P']) == 'D'
    assert DT.host_chk(det, p['P'], 'D') == 'T'
    # keyed to P only: a respelling and CooperateBot see no grudge
    assert DT.chk(det, p['Psyn'], 'D')[0] == 'F' and DT.play(det, p['Psyn']) == 'C'
    assert DT.chk(det, p['Cb'], 'D')[0] == 'F' and DT.play(det, p['Cb']) == 'C'


def test_grudge_inert_for_non_readers_and_negated(progs):
    p = progs
    kP = DT.key_of(p['P'])
    for sp in ('C', 'if(CHK(me,them,D),C,D)'):
        x = DT.prog(p['cat'], p['names'], sp, [('D', DT.keyed(p['delta'], kP))])
        v, n = DT.chk(x, p['P'], 'D')
        assert v == 'F'
        assert DT.host_chk(x, p['P'], 'D') == 'F'


def test_key_rule_is_a_filter(progs):
    p = progs
    assert DT.unkey(DT.keyed(p['delta'], 5)) == p['delta']
    assert DT.has_hyp(DT.keyed(p['delta'], 5))
    assert DT.key_of(p['P']) != DT.key_of(p['Psyn'])


@pytest.mark.skipif(not HAVE_L, reason='needs the cached tables')
def test_eps0_reproduces_stored_scaling_run():
    import json, gzip
    r = DT  # noqa
    sys.path.insert(0, os.path.join(ROOT, 'src'))
    import detectors_run as DR
    path = os.path.join(ROOT, 'runs/realizable_scaling/lottery_main.json.gz')
    if not os.path.exists(path): pytest.skip('no stored rows')
    out = DR._val_job(('scal', 0, 200))
    assert out['compared'] > 0 and not out['bad']


@pytest.mark.skipif(not HAVE_K, reason='needs world K tables')
def test_writes_follow_defections_and_never_own_spelling():
    import provenance as PV
    W = DT.world('K')
    LS = W['LS']
    names = W['names']
    rng = np.random.default_rng(1)
    det = np.nonzero(W['DET'])[0]; pbn = np.nonzero(W['PBN'])[0]
    sp = np.concatenate([rng.choice(det, 60), rng.choice(pbn, 60)]).reshape(1, 120)
    R = DT.DRun('K', sp, np.full(sp.shape, PV.R_SNON, np.int64), LS['Eu'][LS['tau'][sp]], 99, r=100, mN=0.0, gmode=1)
    R.advance(20)
    g = R.glog[:R.nglog[0]]
    assert (g[:, 6] == 2).all()                      # the writer cooperated and the target defected
    assert (g[:, 2] != g[:, 4]).all()                # never against its own spelling
    assert R.gctr[0] == R.nglog[0]
    # lists never exceed the cap
    ks = np.nonzero(R.counts[0])[0]
    assert max(len(R.glist(k)) for k in ks) <= 3
    assert R.check_consistency()                     # free-listed grudge types are never present


@pytest.mark.skipif(not HAVE_K, reason='needs world K tables')
def test_gmode0_has_no_lists_and_sham_plays_base():
    import provenance as PV
    W = DT.world('K')
    LS = W['LS']
    rng = np.random.default_rng(2)
    sp = rng.choice(len(LS['mu']), size=(1, 150), p=LS['mu'])
    for gm in (0, 3):
        R = DT.DRun('K', sp, np.full(sp.shape, PV.R_SNON, np.int64), LS['Eu'][LS['tau'][sp]], 7, r=100, mN=0.0, gmode=gm)
        R.advance(15)
        if gm == 0:
            assert R.ngv[0] == 1                     # only the empty list
        ks = np.nonzero(R.counts[0])[0]
        A, sa = R.A, R.selfa
        for k in ks[:60]:
            for j in ks[:60]:
                u = R.tunit[R.gbase[k]]; v = R.tunit[R.gbase[j]]
                same = u == v and R.tsp[R.gbase[k]] == R.tsp[R.gbase[j]]
                ref = (int(sa[u]), int(sa[u])) if same else (int(A[u, v]), int(A[v, u]))
                assert tuple(int(x) for x in R.acts(k, j)) == ref   # sham lists are ignored in play
