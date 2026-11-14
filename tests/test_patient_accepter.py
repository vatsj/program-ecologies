"""Queue 78: the patient accepter R (catalogue, gates), the laws, the seeded triples, the logging kernel and V1."""
import os, sys, glob
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'runs', '_cache')
import patient_accepter as PA
import patient_accepter_dyn as D
import migration_window as MW


def test_catalogue_extends_queue76():
    import bully_resist as BR
    cat = PA.CataloguePA()
    assert cat.K == 59 and cat.names[:55] == BR.CatalogueBR().names and cat.names[55:] == ['Rnn', 'Rny', 'Rpn', 'Rpy']


def test_v2_block_unchanged():
    import bully_resist as BR
    tb = PA.TabsPA(cache_dir=CACHE); ob = BR.TabsBR(cache_dir=CACHE)
    for a in ('code', 'steps', 'nto', 'fo', 'JT'):
        assert (getattr(tb, a)[:55, :55, :55] == getattr(ob, a)).all()


def test_R_on_the_unequal_island():
    tb = PA.TabsPA(cache_dir=CACHE)
    i = tb.cat.idx
    OUT = tb.VEC[tb.JT]
    # (Bn, C3, C8) is unequal, bully on 2/3; Rnn in the victim's slot plays exactly C3 (read of C8 completes, no charge)
    t = (i['Bn'], i['C3'], i['C8']); tR = (i['Bn'], i['Rnn'], i['C8'])
    assert MW.CATMAP[OUT[t]] == 1 and OUT[t] == OUT[tR]
    assert tb.NTO[tR][1] == 0 and tb.FO[tR][1] == 0
    # with C4 (names its prev = the victim at 1/2) in the excluded slot, Rnn pairs with it: fair
    tO = (i['Bn'], i['Rnn'], i['C4'])
    assert MW.CATMAP[OUT[tO]] == 0 and MW.X[OUT[tO]][1] == 3 and MW.X[OUT[tO]][2] == 3
    # with a firm reader in the excluded slot R's read times out and the n variant does not switch
    tF = (i['Bn'], i['Rnn'], i['Spzn'])
    assert tb.NTO[tF][1] >= 1 and tb.code[i['Rnn'], i['Spzn'], i['Bn']] == 3


def test_laws():
    for arm in D.ARMS:
        for g in (0.3, 1.0, 3.0):
            w = D.law_arm(arm, 0.03, 3.0, g)
            assert abs(w.sum() - 1) < 1e-12 and (w >= 0).all()
            assert abs(sum(w[j] for j in D.ids('bully')) - 0.09) < 1e-9
    wR = D.law_arm('FR', 0.03, 3.0, 1.0); wC = D.law_arm('FC', 0.03, 3.0, 1.0)
    Rm = [D.idx('Rnn'), D.idx('Rpn')]; C = [D.idx('C3'), D.idx('C0')]
    assert abs(sum(wR[j] for j in Rm) - 0.03) < 1e-12
    # F+R and F+C1/3 differ only in the substituted family
    d = wR - wC
    nz = set(np.nonzero(np.abs(d) > 1e-15)[0].tolist())
    assert nz == set(Rm + C)
    assert abs(sum(wC[j] for j in C) - sum(wR[j] for j in C) - 0.03) < 1e-12
    # F is queue 75's law 2a
    import length_prior_t as LP
    assert np.allclose(D.law_arm('F', 0.03, 1.0)[:31], LP.law_2a(0.03, 1.0))


def test_seeded_triples():
    init = D.seeded_init('unequal', 6, 100)
    tb = D.tabs(); OUT = tb.VEC[tb.JT]
    for i in range(6):
        t = tuple(int(np.argmax(init[i, s])) for s in range(3))
        assert MW.CATMAP[OUT[t]] == 1 and sorted(MW.X[OUT[t]]) == [0, 2, 4]
    init = D.seeded_init('fair', 6, 100)
    for i in range(6):
        t = tuple(int(np.argmax(init[i, s])) for s in range(3))
        assert MW.CATMAP[OUT[t]] == 0


def test_logging_kernel_matches_kern_mt():
    import majority_tail as MT
    pr = D.parse('pa:arm=FR:d=0.03:b=3.0:seed=unequal')
    prep = D.prepare(pr['wf'], pr['wt'], 60, 3, 6, init=D.seeded_init('unequal', 6, 60))
    geo = prep['geo']
    a = MT.run_kernel(prep, 100, 1.0, geo['H'], list(geo['snaps']))
    b = D.run_kernel_pa(prep, 100, 1.0, geo['H'], list(geo['snaps']), 10000)
    for k in ('counts', 'modal', 'majo', 'snapc', 'xlog', 'alog'):
        assert np.array_equal(a[k], b[k])
    assert a['nmig'] == b['nmig']


def test_v1_F_arm_reproduces_stored_row():
    import length_prior_t_run as LR
    rows = {}
    for d in glob.glob(os.path.join(ROOT, 'runs', 'lpt_rows', '*')):
        rows.update(LR.load_rows(d))
    old = rows.get('2a|2a:d=0.01:b=1.0|100|64|0|0')
    if old is None:
        return
    rec = D.run_cell('pa:arm=F:d=0.01:b=1.0', 100, 0, 64, charges=False)
    assert rec['vshare_ts'] == old['vshare_ts']
