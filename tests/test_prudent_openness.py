"""Tests for the prudent-openness experiment (notes/prudent-openness.md §1.13).

The hand plays use a small catalogue (whole runs, no cached table); the seed laws, families and the kernel use the
identity run's cached class table (runs/identity_tags/static_n7.npz, lists_n7.pkl) and are skipped without it.
"""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.setrecursionlimit(1000000)
import lt_code as L
import lt_cert as C
import carrier_populations as CP
import identity_tags as IT
import prudent_openness as PO

K = 10 ** 6
V = K // 4
HAVE_TABLE = os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'runs', 'identity_tags', 'static_n7.npz'))
_C = {}


def po():
    if 'po' not in _C:
        _C['po'] = PO.PO()
    return _C['po']


def test_cbp_hand_plays_by_whole_runs():
    """notes §1.2: CBP against CB, EQ, XC, C and D (and the table among them), by whole plays."""
    prod = C.Producer(host=CP.ExactHost())
    probes, cb, comp = IT.build_probes(prod, K, V)
    xs = {'Cc': ('C',), 'D': ('D',), 'CB': IT.CB_X, 'EQ': IT.EQ_X, 'XC': IT.XC_X, 'CBP': PO.CBP_X}
    progs = {}
    for n, x in xs.items():
        mk = lambda c_, x=x: comp.program(x, 0, c_)
        lst, _ = C.produce_list(prod, 0, mk, probes, K, V)
        progs[n] = mk(lst)
    assert L.canon_term(progs['CB']) == L.canon_term(cb)
    hand = {'Cc': 'CCCCCC', 'D': 'DDDDDD', 'CB': 'CDCDDC', 'EQ': 'DDDCDD', 'XC': 'DDDDCD', 'CBP': 'DDCDDC'}
    order = ['Cc', 'D', 'CB', 'EQ', 'XC', 'CBP']
    for r in order:
        row = ''
        for c in order:
            L.CACHE.clear()
            row += L.play(progs[r], progs[c], K)[0]
        assert row == hand[r], (r, row)
    # the certificate facts behind it (ideal checker)
    chk = CP.Checker('ideal', V, K)
    assert chk(0, progs['CB'], L.PROG_C, 'D')[0] == 'T'          # CB certifies defection against the certificate-less C
    assert chk(0, progs['Cc'], L.PROG_C, 'D')[0] == 'F'          # Cc cannot
    assert chk(0, progs['CBP'], cb, 'D')[0] == 'F'               # no D script of CBP against the named CB
    assert chk(0, progs['XC'], progs['CBP'], 'C')[0] == 'F'


@pytest.mark.skipif(not HAVE_TABLE, reason='cached class table not present')
def test_families_and_paths():
    p = po()
    assert len(p.FP) == 147 and abs(p.muL[p.FP].sum() - 0.015513) < 1e-5
    assert p.cb in p.FP and p.cbp in p.FP
    assert len(p.core) == 38 and len(p.nice) == 109
    assert set(p.FX.tolist()) == set(np.nonzero(p.lab == 'exclusive')[0].tolist())
    assert p.xb in p.FX and p.mut[p.xb, p.cbp] and p.mut[p.xb, p.xc] and not p.mut[p.xb, p.cb]
    assert not (set(p.ident.tolist()) & set(p.FP.tolist()))
    pa = p.paths()
    assert pa['n_direct'] == 72 and pa['direct_FX_members'] == [p.xb] and pa['cbp_xc_bridges'] == [p.xb]


@pytest.mark.skipif(not HAVE_TABLE, reason='cached class table not present')
def test_seed_laws():
    p = po()
    st = p.st
    M = p.M
    for cell, blk, mass, zero in [('P1', 'FP', M, []), ('P1p', 'core', M, ['nice']), ('P2n', 'nice', M, ['core']),
                                  ('P3', 'FP', M, ['identity']), ('P4p', 'core', M, ['nice'])]:
        pr = p.class_prior(cell)
        assert abs(pr.sum() - 1) < 1e-12
        assert abs(pr[p.groups[blk]].sum() - mass) < 1e-12, cell
        for z in zero:
            assert pr[p.groups[z]].sum() == 0
        # inside the block, relative L weights are kept
        b = p.groups[blk]
        r = pr[b] / p.muL[b]
        assert r.max() / r.min() - 1 < 1e-9
        # outside the block and removed sets: proportional to L
        out = np.ones(p.nc, bool); out[b] = False
        for z in zero: out[p.groups[z]] = False
        if cell in ('P4p',): out[p.allc] = False
        out &= pr > 0
        r = pr[out] / p.muL[out]
        assert r.max() / r.min() - 1 < 1e-9
    assert p.class_prior('P4')[p.allc].sum() == 0
    # P2 is the identity run's T1c, exactly
    assert np.abs(st.mass(p.cell_weights('P2')) - st.class_prior('T1c')).max() < 1e-15
    # the scan: identity mass m, F_P held at exactly M on the second curve, the rest renormalized
    for i, m in enumerate(PO.SCAN_M):
        m = p.m_L if m is None else m
        a = p.class_prior('scanA_%d' % i); b = p.class_prior('scanB_%d' % i)
        assert abs(a[p.ident].sum() - m) < 1e-12 and abs(b[p.ident].sum() - m) < 1e-12
        assert abs(b[p.FP].sum() - M) < 1e-12
        rest = np.ones(p.nc, bool); rest[p.ident] = False
        ra = a[rest] / p.muL[rest]
        assert ra.max() / ra.min() - 1 < 1e-9
        rest[p.FP] = False
        rb = b[rest] / p.muL[rest]
        assert rb.max() / rb.min() - 1 < 1e-9
    assert np.abs(st.mass(p.cell_weights('scanA_6')) - st.class_prior('L')).max() < 1e-15
    assert np.abs(st.mass(p.cell_weights('scanA_0')) - st.class_prior('noclique')).max() < 1e-15
    # empirical draws
    rng = np.random.default_rng(1)
    d = rng.multinomial(200000, p.class_prior('P1p'))
    assert abs(d[p.core].sum() / 200000 - M) < 5 * np.sqrt(M / 200000)


def test_stage_logger_constructed():
    """Four islands, one family, checkpoints (500, 1000): seeded establishment, extinction, spread, persistence."""
    c0 = [3, 2, 0, 1]
    zg = [-1, 40, -1, 700]           # island 1's lineage vanished at gen 40; island 3's at 700, after it held at 300
    fh = [100, 600, 800, 300]        # island 1 held later by migrants (spread); island 2 never seeded (spread)
    held = np.array([[True, False, False, True],      # at 500
                     [True, True, True, False]])      # at 1000
    s = PO.stage_stats(c0, zg, fh, held, ckpts=(500, 1000))
    assert s['n0'] == 6 and s['occupied'] == 3
    assert s['est_times'] == [100, 300]
    assert s[500] == dict(seeded_est=2, extinct=1, held=2, persist=2, spread=0)
    assert s[1000] == dict(seeded_est=2, extinct=1, held=3, persist=1, spread=2)


def test_crossing_and_bootstrap():
    ms = [0, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 9e-3, 2e-2]
    f = [0.8, 0.75, 0.7, 0.6, 0.4, 0.2, 0.1, 0.0]
    m, fl = PO.crossing(ms, f)
    assert fl == 'ok' and abs(m - np.exp(np.log(1e-3) + 0.5 * (np.log(2e-3) - np.log(1e-3)))) < 1e-15
    assert PO.crossing(ms, [0.4] * 8)[1] == 'below'
    assert PO.crossing(ms, [0.9] * 8)[1] == 'above'
    assert abs(PO.crossing(ms, [1.0, 0.0] + [0.0] * 6)[0] - 1e-4) < 1e-15        # linear on [0, 2e-4]
    # bootstrap: a step curve built from paired replicates; the interval contains the point estimate
    rng = np.random.default_rng(0)
    X = np.array([rng.random(40) < q for q in f], float)
    m0, fl, lo, hi, s = PO.bootstrap_crossing(ms, X, B=300, seed=1)
    assert lo <= m0 <= hi
    fit = PO.fit_exp(np.array(ms[:4]), np.exp(-6400 * np.array(ms[:4]) * 0.05) * 0.8, prefactor=True)
    assert abs(fit['q'] - 0.05) < 1e-3 and abs(fit['f0'] - 0.8) < 1e-3


@pytest.mark.skipif(not HAVE_TABLE, reason='cached class table not present')
def test_kernel_reproduces_identity_run_L0():
    """The kernel with the identity run's streams reproduces its L replicate 0 at 2,000 and 10,000."""
    import json
    import prudent_openness_run as PR
    ref = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'runs', 'identity_tags', 'lottery_main.json')))
    q = [r for r in ref if r['cell'] == 'L' and r['rep'] == 0][0]
    r = PR.lottery_job(('L', 0, 10000))
    assert r['ck']['2000']['outcome'] == q['h2000']['outcome']
    assert abs(r['ck']['2000']['cross_pcc'] - q['h2000']['cross_pcc']) < 1e-12
    assert abs(r['ck']['10000']['cross_pcc'] - q['end']['cross_pcc']) < 1e-12
    assert all(r['consistency'].values())
