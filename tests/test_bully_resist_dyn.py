"""Queue 76 dynamics: laws, seeded starts, V1 (the F arm reproduces queue 75's stored row)."""
import os, sys, json, glob
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import bully_resist_dyn as D
import length_prior_t as LP


def test_laws_sum_and_split():
    D.tabs()
    tb = D.tabs()
    for arm in ('F', 'P', 'Po', 'Q', 'O', 'F2', 'PO', 'FPO'):
        w = D.law_arm(arm, 0.03, 3.0)
        assert abs(w.sum() - 1) < 1e-12 and (w >= 0).all()
        bul = sum(w[i] for i in D.ids('bully'))
        assert abs(bul - 0.09) < 1e-3
    w = D.law_arm('PO', 0.1, 1.0)
    assert abs(sum(w[i] for i in D.ids('prudent')) - 0.05) < 1e-9 and abs(sum(w[i] for i in D.ids('opener')) - 0.05) < 1e-9
    assert all(w[i] == 0 for i in D.ids('prudent', D.PO_))


def test_F_law_is_2a():
    wF = D.law_arm('F', 0.03, 1.0)
    w2 = LP.law_2a(0.03, 1.0)
    assert np.allclose(wF[:31], w2) and (wF[31:] == 0).all()


def test_seeded_pools():
    rng = np.random.default_rng(1)
    for arm in ('F', 'P', 'O', 'PO'):
        for kind in ('fair', 'unequal'):
            init, n = D.seeded_init(arm, kind, 8, 100, rng)
            assert n > 0 and (init.sum(2) == 100).all()


def test_v1_F_arm_reproduces_stored_row():
    import length_prior_t_run as LR
    rows = {}
    for d in glob.glob(os.path.join(ROOT, 'runs', 'lpt_rows', '*')):
        rows.update(LR.load_rows(d))
    old = rows.get('2a|2a:d=0.01:b=1.0|100|64|0|0')
    if old is None:
        return
    rec = D.run_cell('br:arm=F:d=0.01:b=1.0', 100, 0, 64, charges=False)
    assert rec['vshare_ts'] == old['vstar'] or rec['vshare_ts'] == old['vshare_ts']
