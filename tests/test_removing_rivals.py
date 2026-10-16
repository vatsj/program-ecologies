"""Tests for removing rival networks (notes/removing-rivals.md §1.7).  The cached tables are untracked; tests that need
them skip without them."""
import gzip
import json
import os
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
HAVE = os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'static')) and \
    os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'OSV.npy'))
need = pytest.mark.skipif(not HAVE, reason='cached tables absent')


@need
def test_eps0_kernel_draw_for_draw_and_tracking_inert():
    import realizable_scaling as RS
    import removing_rivals as RR
    a = RS.RSRun('rs_Snon_200_64_cal', 2); a.advance(150)
    b = RR.RRRun('rs_Snon_200_64_cal', 2, epsN=0.0, track=False); b.advance(150)
    c = RR.RRRun('rs_Snon_200_64_cal', 2, epsN=0.0, track=True); c.advance(150)
    for z in (b, c):
        assert (a.slots == z.slots).all() and (a.pres == z.pres).all() and a.ntv[0] == z.ntv[0]
        nt = a.ntv[0]
        assert (a.tunit[:nt] == z.tunit[:nt]).all()
    assert (c.lin == 0).all()


@need
def test_stored_trace_reproduced_and_restore_exact():
    import removing_rivals as RR
    import removing_rivals_run as RRR
    rows = json.load(gzip.open(os.path.join(ROOT, 'runs', 'realizable_scaling', 'lottery_main.json.gz')))
    r = [x for x in rows if x['cell'] == 'rs_Snon_200_64_cal' and x['rep'] == 1][0]
    R = RR.RRRun('rs_Snon_200_64_cal', 1, epsN=0.0)
    mine = []
    while R.g < 300:
        R.advance(10)
        if R.g % 50 == 0: mine.append(RRR.stored_trace_fields(R, R.island_stats()))
    n, bad = RRR.compare_trace(mine, [tuple(t) for t in r['trace'] if t[0] <= 300])
    assert n >= 5 and bad == 0
    st = R.save_state()
    Q = RR.RRRun('rs_Snon_200_64_cal', 1, epsN=0.0); Q.load_state(st)
    R.advance(100); Q.advance(100)
    assert (R.slots == Q.slots).all() and (R.pres == Q.pres).all()
    for i in range(R.I):
        ks = R.pres[i, :R.npres[i]]
        assert np.array_equal(R.paysum[i, ks], Q.paysum[i, ks])


@need
def test_sponsored_founder_and_empty_control():
    import provenance as PV
    import provenance_run as PR
    import removing_rivals as RR
    LS = PR.lot_static()
    S = RR.static(LS)
    units = LS['meta']['units']
    assert S['uPB'] == 123 and units[123] == (123, (9,), (3,))
    sp_s, ru_s, un_s = RR.founders_rr('rr_spon_200_64', 4, LS)
    sp_e, ru_e, un_e = RR.founders_rr('rr_pbe_200_64', 4, LS)
    sp_b, ru_b, un_b = RR._base(200, 64, 4, LS)
    a, _, _ = PR.founders.__wrapped__('rs_Snon_200_64_cal', 4, LS) if hasattr(PR.founders, '__wrapped__') else \
        RR._PREV_FOUNDERS('rs_Snon_200_64_cal', 4, LS)
    assert np.array_equal(a, sp_b)                                  # the base is S-nonself's founders
    diff = (sp_s != sp_b) | (ru_s != ru_b) | (un_s != un_b)
    assert diff.sum(1).max() <= 1                                   # one founder per island changed
    pos = RR.donor_positions(200, 64, 4)
    for i in range(64):
        j = pos[i]
        assert sp_s[i, j] == S['kPB'] and ru_s[i, j] == PV.R_H and un_s[i, j] == 123
        assert sp_e[i, j] == S['kPB'] and ru_e[i, j] == PV.R_SNON and un_e[i, j] == S['ePB']
    assert ((sp_s != sp_e) | (ru_s != ru_e) | (un_s != un_e)).sum() == 64
    # C-donor's donors sit at the same positions
    _, ru_c, _ = RR._PREV_FOUNDERS('rs_Cdon_200_64_cal', 4, LS)
    for i in range(64):
        assert ru_c[i, pos[i]] == PV.R_H


@need
def test_rain_rate_and_prior():
    import provenance_run as PR
    import removing_rivals as RR
    LS = PR.lot_static()
    R = RR.RRRun('rs_Snon_200_64_cal', 990, epsN=20.0, track=True)
    R.advance(40)
    n = int(R.nfr[0])
    rate = R.rcount.sum() / (R.I * 40)
    assert abs(rate - 20.0) < 4 * np.sqrt(20.0 / (R.I * 40)) + 0.2
    sp = R.fr[:n, 2]
    mu = LS['mu']
    top = np.argsort(-mu)[:15]
    obs = np.array([(sp == s).sum() for s in top]); exp = mu[top] * n
    chi2 = ((obs - exp) ** 2 / exp).sum()
    assert chi2 < 45                                               # 15 cells, p ~ 1e-4 threshold
    # lineage ids: every fresh founder a new id
    assert R.nlin[0] == n


@need
def test_predator_classifier_on_RE_example():
    import provenance as PV
    import provenance_run as PR
    import removing_rivals as RR
    LS = PR.lot_static()
    x = 9430; sx = LS['names'].index('if(or(CHK(me,^C,C),CHK(them,^D,D)),D,C)')
    pt = RR.predator_table(x, sx, PV.R_SNON, [123, 147, 2133, 2144], LS)
    assert pt['cert_coop_defect'] == 2870 and pt['cert_pred'] == 2222       # the RE's static counts
    assert pt['mass'] > 0 and 'D' not in pt['constants']
    # an identity holder is closed
    ident = np.nonzero(np.asarray(LS['ident']))[0]
    u = int(ident[0]); su = int(np.nonzero(LS['tau'] == LS['st']['utau'][u])[0][0])
    pt2 = RR.predator_table(u, su, PV.R_SNON, [123], LS)
    assert pt2['mass'] == 0
