"""Tests for Part B of the coalition-proof auctions run (src/auction_islands.py): the payoff tensor's resolution order, the audit, the
tremble control, and the three-population kernel."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import auction_islands as B


def test_resolution_order_items_first_then_p():
    for rule in B.RULES:
        for inst in B.INSTANCES:
            c = B.Ctx(rule, inst)
            for pa in B.ITEM:
                for pb in B.ITEM:
                    items = {c.bids(pa, pb, pp)[1:] for pp in B.PROG_P}
                    assert len(items) == 1, (rule, inst, pa, pb)        # P's program never changes the items' bids
            # POL's bid is a function of the items' intended bids only
            for pa in B.ITEM:
                for pb in B.ITEM:
                    bP, bA, bB = c.bids(pa, pb, 'POL')
                    assert bP == c.p_bid('POL', bA, bB)


def test_pair_conditioning():
    c = B.Ctx('vcg', 'collusion')
    assert c.pair == (20, 20)
    assert c.bids('PAIR', 'PAIR', 'T')[1:] == (20, 20)
    assert c.bids('PAIR', 'T', 'T')[1:] == (5, 5)          # PAIR with a non-PAIR partner is truthful
    assert c.bids('PAIR', 'PAIRU', 'T')[1:] == (5, 20)     # PAIRU is not PAIR's partner class: PAIRU overbids alone
    assert c.bids('PAIRU', 'T', 'T')[1:] == (20, 5)
    assert c.bids(('C', 17), 'PAIR', 'T')[1:] == (17, 5)   # a constant is not a PAIR


def test_pol_truthful_against_truthful_items_and_spite_against_pairs():
    c = B.Ctx('vcg', 'collusion')
    assert c.bids('T', 'T', 'POL')[0] == 20                # truthful against truthful items
    assert c.bids('SH', 'SH', 'POL')[0] == 20              # SH is truthful under VCG
    assert c.bids('PAIR', 'PAIR', 'POL')[0] == 40          # the highest losing bid: the pair's prices become 20
    u = c.payoffs(c.bids('PAIR', 'PAIR', 'POL'))
    assert u == (0.0, -15.0, -15.0)
    assert c.payoffs(c.bids('PAIR', 'PAIR', 'T')) == (0.0, 5.0, 5.0)


def test_pair_report_individually_rational():
    for rule in B.RULES:
        for inst in B.INSTANCES:
            c = B.Ctx(rule, inst)
            u = c.payoffs((c.v[0],) + c.pair)
            if c.pair != (c.v[1], c.v[2]):
                assert u[1] > c.u0[1] and u[2] > c.u0[2]
    # under the surcharge the pair has no joint gain (total payments are pinned by P's report): PAIR plays truthfully
    assert B.Ctx('surcharge', 'collusion').pair == (5, 5)
    assert B.Ctx('surcharge', 'threshold').pair == (15, 15)


def test_audit_replaces_reading_programs():
    for rule in B.RULES:
        for inst in B.INSTANCES:
            U, rec, c = B.tensor(rule, inst, False)
            Ua, reca, _ = B.tensor(rule, inst, True)
            iT, iPAIR, iPAIRU, iSH = (B.ITEM.index(x) for x in ('T', 'PAIR', 'PAIRU', 'SH'))
            pT, pPOL = B.PROG_P.index('T'), B.PROG_P.index('POL')
            assert np.allclose(Ua[:, iPAIR, :, :], Ua[:, iT, :, :])
            assert np.allclose(Ua[:, :, iPAIR, :], Ua[:, :, iT, :])
            assert np.allclose(Ua[:, :, :, pPOL], Ua[:, :, :, pT])
            assert np.allclose(Ua[:, iPAIRU, iPAIRU, pT], U[:, iPAIRU, iPAIRU, pT])   # PAIRU unchanged


def test_tremble_control_prediction_12():
    t = B.tremble('vcg', 'collusion')
    assert t['intended_pair'] == [20, 20]
    assert t['no_tremble']['POL']['uP'] == 0.0 and t['no_tremble']['T']['uP'] == 0.0
    assert t['tremble']['POL']['E_uP'] < t['tremble']['T']['E_uP']
    assert abs(t['tremble']['POL']['E_uP'] - (-0.45)) < 1e-9 and abs(t['tremble']['T']['E_uP'] - 0.025) < 1e-9


def test_vcg_collusion_nash_contains_pair_and_truth():
    U, rec, c = B.tensor('vcg', 'collusion', False)
    ne = set(B.pure_nash(U))
    assert ('PAIR', 'PAIR', 'T') in ne and ('T', 'T', 'T') in ne and ('T', 'T', 'POL') in ne
    assert ('PAIR', 'PAIR', 'POL') not in ne               # the pair is deterred when the police read it
    assert B.pure_nash(U, True) == []                      # everything is neutral somewhere: no strict equilibrium


def test_kernel_conserves_and_absorbs():
    U, rec, c = B.tensor('vcg', 'collusion', False)
    rng = np.random.default_rng(3)
    init = B.seed_counts(B.prior('U'), 8, 40, rng)
    cnt, fg, fx, pf, te, sg = B.sim3(U, init, 40, 0.3, 0.0, 2000, 11, 5, 1, 2, 3, 1)
    assert (cnt.sum(2) == 40).all()
    assert (fx >= 0).all()
    assert ((cnt > 0).sum(2) == 1).all()                   # every role monomorphic
    # a strictly dominant program takes over: make item program 1 strictly better in every context
    U2 = np.zeros_like(U)
    U2[0, 1, :, :] = 1.0; U2[1, :, 1, :] = 1.0
    init = np.zeros((4, 3, B.K), np.int64)
    init[:, 0, 0] = 30; init[:, 0, 1] = 10; init[:, 1, 0] = 30; init[:, 1, 1] = 10; init[:, 2, 0] = 40
    cnt, fg, fx, pf, te, sg = B.sim3(U2, init, 40, 0.3, 0.0, 2000, 12, 5, 1, 2, 3, 1)
    assert (cnt[:, 0, 1] == 40).sum() >= 3 and (cnt[:, 1, 1] == 40).sum() >= 3


def test_encounter_stats_monomorphic_pair():
    c = B.Ctx('vcg', 'collusion')
    cnt = np.zeros((3, B.K), np.int64)
    cnt[0, 2] = 100; cnt[1, 2] = 100; cnt[2, 0] = 100        # (PAIR, PAIR, T)
    st = B.encounter_stats(c, cnt, False)
    assert st['joint'] == 1.0 and st['items_dev'] == 1.0 and st['eff'] == 0.0
    assert B.classify_island(st, cnt, False)['cls'] == 'pair'
    cnt[2, 0] = 0; cnt[2, 1] = 100                           # (PAIR, PAIR, POL): the pair is still played, and policed
    st = B.encounter_stats(c, cnt, False)
    k = B.classify_island(st, cnt, False)
    assert k['cls'] == 'pair' and k['policed']
