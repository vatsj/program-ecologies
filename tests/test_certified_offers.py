"""Queue 79: certified offers (catalogue, check map, soundness on hand triples, laws, the Fc* table, the seeded triples)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'runs', '_cache')
import certified_offers as CO
import certified_offers_dyn as D
import patient_accepter as PA
import migration_window as MW


def test_catalogue_extends_queue78():
    cat = CO.CatalogueCO()
    assert cat.K == 87 and cat.names[:59] == PA.CataloguePA().names
    assert sum(1 for m in cat.meta if m['cert'] is not None) == 28


def test_check_map_machines_agree_and_forgers_rejected():
    cat = CO.CatalogueCO(extra=CO.forgers())
    for i, t in enumerate(cat.terms):
        hs = CO.host_skel(t)
        if cat.fam[i] == 'forger':
            assert hs is None
        for w in (0, 1):
            want = 'F' if hs is None else ('T' if hs[w] == 1 else 'F')
            assert CO.check_value('C0', t, w)[0] == want
            assert CO.check_value('C1', t, w)[0] == want
    CO.set_machine('C1')


def test_first59_unchanged_and_pointing_pairs():
    tb = CO.TabsCO(cache_dir=CACHE, machine='C1')
    old = PA.TabsPA(cache_dir=CACHE)
    for a in ('code', 'steps', 'nto', 'fo', 'JT'):
        assert (getattr(tb, a)[:59, :59, :59] == getattr(old, a)).all()
    i = tb.cat.idx
    OUT = tb.VEC[tb.JT]
    # the bully's island with Rcn as victim and Ocp in e: the fair pair (v, e), no timed-out read
    t = (i['Bn'], i['Rcn'], i['Ocp'])
    assert MW.CATMAP[OUT[t]] == 0 and MW.X[OUT[t]][1] == 3 and MW.X[OUT[t]][2] == 3 and tb.NTO[t].sum() == 0
    # beside a simulating reader Rcn is the 1/3 constant, legibly
    t = (i['Bn'], i['Rcn'], i['Snzn']); t3 = (i['Bn'], i['C3'], i['Snzn'])
    assert OUT[t] == OUT[t3] and tb.NTO[t][0] == 0 and tb.NTO[t][1] == 0
    # (Fc)^3 all-next is a cycle, a mixed orientation is a fair pair
    t = (i['FcSnzn'],) * 3
    assert MW.CATMAP[OUT[t]] != 0
    assert MW.CATMAP[OUT[(i['FcSnzn'], i['FcSnzn'], i['FcSpzn'])]] == 0


def test_laws():
    for arm in D.ARMS:
        for ph in (0.0, 0.5, 1.0):
            w = D.law_arm(arm, 0.03, 3.0, ph)
            assert abs(w.sum() - 1) < 1e-12 and (w >= 0).all()
    tb = D.tabs(CACHE)
    # the matched pair FcOcRc / FcOcC3 differ only in Rc vs the 1/3 constants (same donor mass)
    a = D.law_arm('FcOcRc', 0.03, 3.0); b = D.law_arm('FcOcC3', 0.03, 3.0)
    rc = D.ids('c_acc'); c13 = [D.idx('C3'), D.idx('C0')]
    diff = [k for k in range(tb.K) if abs(a[k] - b[k]) > 1e-15]
    assert set(diff) == set(rc + c13)
    assert abs(sum(a[k] for k in rc) - (sum(b[k] for k in c13) - sum(a[k] for k in c13))) < 1e-12
    # queue 78's F law on the first 59 entries (zeros after)
    import patient_accepter_dyn as PD
    w78 = PD.law_arm('F', 0.03, 3.0); w79 = D.law_arm('F', 0.03, 3.0)
    assert np.allclose(w78, w79[:59]) and (w79[59:] == 0).all()
    # phi splits the bully mass
    w = D.law_arm('Fc', 0.03, 3.0, 1.0)
    assert sum(w[k] for k in D.ids('bully')) == 0 and sum(w[k] for k in D.ids('c_bully')) > 0


def test_cyclefix_changes_only_carrier_cycles():
    tb = D.tabs(CACHE)
    J, PAY, VEC, _, _ = D.tables(0.1)
    J2, PAY2, VEC2, n = D._cyclefix(tb, J, PAY, VEC)
    assert n > 0
    ch = np.argwhere(J2 != J)
    assert len(ch) == n
    car = np.array([tb.cat.meta[k]['cert'] is not None for k in range(tb.K)])
    for a, b, c in ch[:200]:
        assert car[a] and car[b] and car[c]
        o = VEC2[J2[a, b, c]]
        assert MW.CATMAP[o] == 0 and MW.X[o][0] == 3 and MW.X[o][1] == 3


def test_seeded_triples():
    tb = D.tabs(CACHE)
    OUT = tb.VEC[tb.JT]
    for kind, cl in (('unequal', 1), ('unequalBc', 1), ('fair', 0), ('fairC', 0)):
        for t in D.seed_triples(kind):
            assert MW.CATMAP[OUT[t]] == cl
