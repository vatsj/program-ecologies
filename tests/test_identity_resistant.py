"""Tests for the identity-resistant target (notes/identity-resistant.md).  All but the guard parser need the untracked
cached tables (runs/lt_genes/static, runs/provenance/static) and skip without them."""
import gzip
import json
import os
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
HAVE = os.path.exists(os.path.join(ROOT, 'runs', 'provenance', 'static')) and \
    os.path.exists(os.path.join(ROOT, 'runs', 'lt_genes', 'static'))
need = pytest.mark.skipif(not HAVE, reason='needs the untracked cached tables')


def test_guard_parser():
    import importlib
    if not HAVE:
        pytest.skip('module import needs the cached tables')
    IRM = importlib.import_module('identity_resistant')
    assert IRM.guarded('if(CHK(them,me,C),C,D)')
    assert IRM.guarded('if(CHK(them,me,C),if(CHK(them,^D,D),C,D),D)')
    assert IRM.guarded('if(and(CHK(them,^D,D),CHK(them,me,C)),C,D)')
    assert not IRM.guarded('if(CHK(them,^D,D),C,D)')
    assert not IRM.guarded('if(CHK(them,me,C),C,if(CHK(them,them,C),C,D))')
    assert not IRM.guarded('if(or(CHK(them,me,C),CHK(them,them,D)),C,D)')
    assert not IRM.guarded('C') and IRM.guarded('D')


@need
def test_partition_on_examples():
    import provenance_run as PR
    import removing_rivals as RR
    import identity_resistant as IRM
    LS = PR.lot_static(); S = RR.static(LS)
    P = IRM.partition(LS)
    assert len(P['Tu']) == 235 and int(P['ex_ideal'].sum()) == 165
    assert len(P['chal']) == 21
    names = LS['names']
    for nm in ('if(CHK(them,^D,D),C,D)', 'if(CHK(them,me,C),C,if(CHK(them,them,C),C,D))'):
        u = int(LS['Hu'][LS['tau'][names.index(nm)]])
        assert P['exu'][u], nm
    assert P['resu'][3] and P['resu'][S['uPB']]
    # no guarded unit is exploitable (soundness)
    utau = np.asarray(LS['st']['utau'])
    for u, e in zip(P['Tu'].tolist(), P['ex'].tolist()):
        if e:
            assert not IRM.guarded(names[LS['cat'].members[utau[u]][0]])


@need
def test_priors_preserve_totals_and_coupling():
    import provenance_run as PR
    import identity_resistant as IRM
    LS = PR.lot_static()
    P = IRM.partition(LS)
    mu = LS['mu']
    for p in IRM.PRIORS:
        m = IRM.prior_mass(p, LS)
        assert abs(m.sum() - mu.sum()) < 1e-12
        assert abs(m[P['sp_Q']].sum() - mu[P['sp_Q']].sum()) < 1e-15
        for base in ('np', 'kern'):
            assert np.abs(IRM.table_mass(p, base, LS) - m).max() < 1e-12
    assert IRM.prior_mass('Rm', LS)[P['sp_E']].sum() == 0
    assert abs(IRM.prior_mass('Rm', LS)[P['sp_Res']].sum() - (P['mass']['E'] + P['mass']['Res'])) < 1e-12
    u = np.random.default_rng(5).random(200000)
    sL = IRM.quantile(u, 'L')
    for p in ('Rm', 'Rp'):
        sp = IRM.quantile(u, p)
        diff = sL != sp
        assert (P['sp_E'][sL] == diff).all()          # a slot changes iff its L draw is exploitable-target
        assert not P['sp_E'][sp].any()


@need
def test_L_coupling_reproduces_stored_founders():
    import provenance_run as PR
    import pangaea as PG
    import identity_resistant as IRM
    import annealed as AN
    LS = PR.lot_static()
    for rep in (0, 3):
        a = PG.base_list(12800, rep, LS)
        b = IRM.quantile(np.random.default_rng([12800, rep, PG.SALT_PG]).random(12800), 'L')
        assert np.array_equal(a, b)
    # scaling / annealed founders: the stored natural cell against the L rain cell, and the sponsored island cell
    for stored, mine, rep in (('an_i_800', IRM.reg_rain('L', 'ann', 800), 1), ('rr_spon_200_64', IRM.reg_isl('L', True), 2),
                              ('rs_Snon_200_64_cal', IRM.reg_isl('L', False), 0)):
        x = PR.founders(stored, rep, LS); y = PR.founders(mine, rep, LS)
        for u, v in zip(x, y):
            assert np.array_equal(u, v), stored
    sp, rule, unit = PR.founders(IRM.reg_ff('L', False), 4, LS)
    sp2, rule2, unit2 = PR.founders(PG.cell_name('L', 100, 128, merge_at=200), 4, LS)
    assert np.array_equal(sp, sp2) and np.array_equal(rule, rule2) and np.array_equal(unit, unit2)


@need
def test_kernel_copy_equals_annealed():
    import annealed as AN
    import identity_resistant as IRM
    name = IRM.reg_rain('L', 'ann', 200)
    a = AN.AnnRun(name, 0); b = IRM.IRAnnRun(name, 0)
    sched = np.full(400, 1.0 / 200)
    a.epsg = sched.copy(); b.epsg = sched.copy()
    a.advance(150); b.advance(150)
    assert np.array_equal(a.slots, b.slots) and int(a.ntv[0]) == int(b.ntv[0])
    assert np.array_equal(a.fr[:a.nfr[0]], b.fr[:b.nfr[0]]) and int(a.nfr[0]) > 50


@need
def test_rm_rain_differs_only_on_E_draws():
    import identity_resistant as IRM
    LS = IRM.PR.lot_static()
    P = IRM.partition(LS)
    nL = IRM.reg_rain('L', 'ann', 200); nR = IRM.reg_rain('Rm', 'ann', 200)
    a = IRM.IRAnnRun(nL, 0); b = IRM.IRAnnRun(nR, 0)
    sched = np.full(400, 1.0 / 200)
    a.epsg = sched.copy(); b.epsg = sched.copy()
    a.advance(3); b.advance(3)
    # the first few arrivals per island: same times; spellings equal unless the L draw was exploitable-target
    fa = a.fr[:a.nfr[0]]; fb = b.fr[:b.nfr[0]]
    k = min(len(fa), len(fb), 20)
    assert k > 5
    for x, y in zip(fa[:k], fb[:k]):
        if x[0] != y[0] or x[1] != y[1]: break       # states diverged
        assert x[2] == y[2] or P['sp_E'][x[2]]
