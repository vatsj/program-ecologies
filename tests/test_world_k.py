"""Tests for the world-K reruns (notes/world-k.md).  The term-level mechanism checks (spec amendment 2.5) run anywhere;
the population tests need the untracked cached tables (runs/provenance/static, runs/detectors/K) and skip without
them."""
import gzip
import json
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
HAVE_K = os.path.exists(os.path.join(ROOT, 'runs', 'detectors', 'K', 'static', 'A.npy'))
TWIND = 'if(or(CHK(me,me,D),CHK(me,them,D)),D,C)'


@pytest.fixture(scope='module')
def keyed():
    """The TwinD reader's D-step script δ (produced against ⌜D⌝), keyed to ⌜D⌝ as world K reads it."""
    DT.install_library('key')
    cat, names = DT.catalogue()
    prod = C.Producer(host=__import__('carrier_populations').ExactHost())
    x0 = DT.prog(cat, names, TWIND)
    delta = prod.produce(0, x0, L.PROG_D, 'D', DT.K, DT.V)
    syn = DT.synonyms(cat, names, TWIND)[0]
    kd = DT.keyed(delta, DT.KEY_D)
    return dict(cat=cat, names=names, delta=delta, kd=kd, syn=syn,
                x=DT.prog(cat, names, TWIND, [('D', kd)]), x_unkeyed=DT.prog(cat, names, TWIND, [('D', delta)]),
                Dpop=DT.prog(cat, names, 'D'), Cb=DT.prog(cat, names, 'C'),
                P=DT.prog(cat, names, 'if(CHK(them,me,C),D,C)'))


def test_population_defectbot_is_not_the_literal_key(keyed):
    """§1.1: a population DefectBot's bare source is the grammar body, not ⌜D⌝."""
    assert DT.has_hyp(keyed['delta'])
    assert DT.key_of(keyed['Dpop']) != DT.KEY_D
    assert DT.key_of(L.PROG_D) == DT.KEY_D


def test_keyed_certificate_accepted_only_against_its_production_partner(keyed):
    k = keyed
    assert DT.chk(k['x'], L.PROG_D, 'D')[0] == 'T'                  # its production partner ⌜D⌝
    for m in (k['Dpop'], k['Cb'], k['P']):                          # different quotes
        assert DT.chk(k['x'], m, 'D')[0] == 'F'
    assert DT.chk(k['x'], k['x'], 'D')[0] == 'F'                     # self-play root
    # the play: the keyed TwinD reader cooperates with the population DefectBot (it is a sucker in K)
    assert DT.play(k['x'], k['Dpop']) == 'C' and DT.play(k['x'], k['Cb']) == 'C'
    # in L the same script, unkeyed, validates against the population DefectBot and the reader defects
    assert DT.chk(k['x_unkeyed'], k['Dpop'], 'D')[0] == 'T' and DT.play(k['x_unkeyed'], k['Dpop']) == 'D'


def test_keyed_certificate_after_copying_and_after_removal(keyed):
    k = keyed
    y = DT.prog(k['cat'], k['names'], k['syn'], [('D', k['kd'])])   # a copy on a synonym spelling (same run tree)
    assert DT.chk(y, L.PROG_D, 'D')[0] == 'T'
    assert DT.chk(y, k['Dpop'], 'D')[0] == 'F' and DT.chk(y, k['x'], 'D')[0] == 'F'
    z = DT.prog(k['cat'], k['names'], TWIND)                        # the entry removed (no list cap exists in K0)
    assert DT.chk(z, L.PROG_D, 'D')[0] == 'F'


@pytest.mark.skipif(not (HAVE_L and HAVE_K), reason='needs the cached tables')
def test_no_identity_unit_under_s_nonself_in_k():
    import world_k as WK
    for w, n_expected in (('L', 8), ('K', 0)):
        s = np.load(WK.sets_path(w))
        LS = WK.world_ls(w)
        import provenance as PV
        idn = PV.identity_units(set(np.nonzero(s['reach_nonself'])[0].tolist()), LS['st']['A'], LS['st']['selfa'])
        assert len(idn) == n_expected


@pytest.mark.skipif(not (HAVE_L and HAVE_K), reason='needs the cached tables')
def test_world_switch_and_paired_founders():
    import world_k as WK
    import provenance_run as PR
    LSL = WK.use_world('L'); fl = PR.founders('wk_prop_200_64', 3, LSL)
    LSK = WK.use_world('K'); fk = PR.founders('wk_prop_200_64', 3, LSK)
    assert len(LSL['meta']['units']) == 17394 and len(LSK['meta']['units']) == 17375
    assert (fl[0] == fk[0]).all() and (fl[1] == fk[1]).all()
    assert (LSK['Q'] == LSL['Q']).all() and len(LSK['Q_K']) == 0
    assert not np.isin(fl[0], LSL['Q']).any()


@pytest.mark.skipif(not (HAVE_L and HAVE_K), reason='needs the cached tables')
def test_reproduces_stored_runs_and_tracking_is_inert():
    import world_k as WK
    r = WK.island_job(('wk_Snon_200_64', 0, 'L', 200, True))
    st = [x for x in json.load(gzip.open(os.path.join(ROOT, 'runs/realizable_scaling/lottery_main.json.gz')))
          if x['cell'] == 'rs_Snon_200_64_cal' and x['rep'] == 0][0]
    ref = {t[0]: t for t in st['trace']}
    common = [t for t in r['trace'] if t[0] in ref]
    assert common and all(abs(ref[t[0]][1] - t[1]) < 1e-4 and ref[t[0]][7] == t[7] for t in common)
    rk = WK.island_job(('wk_Snon_200_64', 0, 'K', 200, True))
    d = [x for x in json.load(gzip.open(os.path.join(ROOT, 'runs/detectors/cells_C_slim.json.gz')))
         if x['cell'] == 'Cis_K0_e0' and x['rep'] == 0][0]
    ser = {int(x[0]): x[3] for x in d['series']}
    assert all(abs(ser[t[0]] - t[1]) < 1e-4 for t in rk['trace'] if t[0] in ser)
    ra = WK.island_job(('wk_Snon_100_64', 1, 'K', 100, True))
    rb = WK.island_job(('wk_Snon_100_64', 1, 'K', 100, False))
    assert ra['trace'] == rb['trace']
