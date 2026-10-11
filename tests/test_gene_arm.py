"""Tests for the gene arm (src/gene_arm.py, src/gene_arm_run.py; notes/gene-arm.md §1)."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import gene_arm as GA
import gene_arm_run as R
import union as U

G = R.sog()
TCC = R.tables('CC'); TRR = R.tables('RR')
w = lambda base, genes=(): G.find_w(base, genes)
bb = lambda s, h, p, genes=(): G.find_b((s, h, p), genes)
SC, ST, T0, MI, UN = w((0, 0)), w((3, 0)), w((1, 0)), w((2, 0)), w((0, 1))


def play(T, b, x, y):
    return U.joint_name(int(T['J'][b, x, y]))


def test_grammar_counts():
    assert (len(GA.W_BASES), len(GA.B_BASES), len(GA.C_BASES)) == (8, 27, 4)
    assert (GA.NWG, GA.NBG, GA.NCG) == (16, 48, 4)
    assert (G.KW, G.KB) == (136, 1323)
    G2 = GA.SOG(2)
    assert (G2.KW, G2.KB) == (2056, 62235)
    assert GA.Chicken(2).K == 68 and GA.Chicken(1).K == 20


def test_gene_evaluation_hand_cases():
    assert play(TCC, bb(0, 1, 0), SC, SC) == '(0,none) W W'
    assert play(TCC, bb(0, 1, 0), ST, ST) == '(0,none) S S'
    assert play(TCC, bb(2, 1, 0), MI, MI) == '(1/2,none) W W'
    assert play(TCC, bb(2, 1, 0), UN, UN) == '(1/2,none) W W'
    assert play(TCC, bb(1, 1, 0), T0, T0) == '(1/4,none) W W'
    assert play(TCC, bb(0, 1, 2), MI, MI) == '(1/2,none) W W'          # D* pays the militants fair
    assert play(TRR, bb(0, 1, 2), MI, MI) == '(1/4,none) W W'          # under RR the 1/4 probe is false
    cut = bb(2, 1, 0, (GA.bgene(2, 1),))                               # (BOX(W1=work) -> wage 1/4)
    assert play(TCC, cut, MI, MI) == '(1/2,none) W W'
    assert play(TRR, cut, MI, MI) == '(1/4,none) W W'
    # quorum gene on a scab is the union pair's play
    qw = w((0, 0), (GA.wgene(7, 1),))
    assert play(TCC, bb(1, 1, 0), qw, qw) == '(1/4,none) S S'
    # Z_D0: W1 adds (BOX(s=0) -> strike); D0 pays 1/2 and W1 works
    t0g = w((0, 0), (GA.wgene(0, 1),))
    assert play(TCC, bb(0, 1, 1), t0g, SC) == '(1/2,none) W W'
    # world 0: the first gene is operative
    tr = GA.trace_g(G, TCC['FV'], cut, MI, MI, 'CC', 4)
    assert tr[0]['ops'][0] == 0


def test_flag_evaluator_matches_history_trace():
    rng = np.random.default_rng(3)
    for rule, T in (('CC', TCC), ('RR', TRR)):
        for _ in range(300):
            b, x, y = int(rng.integers(G.KB)), int(rng.integers(G.KW)), int(rng.integers(G.KW))
            tr = GA.trace_g(G, T['FV'], b, x, y, rule, 12)
            assert tr[-1]['imp'] == int(T['J'][b, x, y])
            assert tr[-2]['imp'] == tr[-1]['imp']


def test_filter_named_genes():
    F = R.the_filter()
    assert not F['boss'][GA.bgene(0, 3)]['admitted']            # whack
    assert not F['worker'][GA.wgene(7, 1)]['admitted']          # quorum
    assert not F['boss'][GA.bgene(4, 2)]['admitted']            # probe concession
    assert F['boss'][GA.bgene(0, 4)]['admitted']                # de-escalation
    assert F['worker'][GA.wgene(3, 0)]['admitted']              # threat accommodation
    for t in range(8):
        assert F['worker'][GA.wgene(t, 0)]['admitted']          # every work gene
    C = GA.Chicken(2); Fc = C.filter()
    assert not Fc[0]['admitted']                               # firm (BOX(THEM=St) -> St)
    assert Fc[2]['admitted'] and Fc[1]['admitted']              # bridge, yield


def test_filter_slot_mirror():
    """the worker filter tested in slot W2 gives the same verdicts (strike genes fail, work genes pass)."""
    J = TCC['J']; O = TCC['OPS']
    for g in range(GA.NWG):
        tr, ov = g // 2, g % 2
        car = [x for x in range(G.KW) if G.wprog[x][1] == (g,)]
        fails = 0; fired = 0
        for x in car:
            sub = J[:, :, x].astype(np.int64); o2 = O[:, :, x].astype(np.int64) // 9 - 1
            fires = o2 == 0
            a1 = (sub // 2) % 2; a2 = sub % 2
            T1 = np.broadcast_to(G.tag[None, :], sub.shape); T2 = np.full(sub.shape, G.tag[x])
            own = GA.PAY[sub, T1, T2, 2]; alt = GA.PAY[4 * (sub // 4) + 2 * a1 + (1 - a2), T1, T2, 2]
            fired += fires.sum(); fails += (fires & (own < alt - 1e-12)).sum()
        assert (fails == 0) == R.the_filter()['worker'][g]['admitted']


def test_encoding_invariance_pairs():
    qw = w((0, 0), (GA.wgene(7, 1),))
    for T in (TCC, TRR):
        assert (T['J'][:, qw, :] == T['J'][:, UN, :]).all() and (T['J'][:, :, qw] == T['J'][:, :, UN]).all()
    assert G.tag[qw] == G.tag[UN] == 1
    pi = bb(0, 1, 0, (GA.bgene(4, 2),))
    assert (TCC['J'][pi] == TCC['J'][bb(0, 1, 1)]).all()
    w1 = bb(0, 1, 0, (GA.bgene(0, 3),))
    assert (TCC['J'][w1] != TCC['J'][bb(0, 0, 0)]).any()


def test_gene_stability_hand_states():
    NP = R.named_progs()
    res = {}
    for a in ('G-all', 'G-cred', 'G-cred-whole', 'G-recip'):
        A = R.arm(a); T = R.tables(A['rule'])
        res[a] = {k: GA.gene_stable(G, T, A, *NP[k])[0] for k in NP}
    for a in res:
        assert res[a]['Z'] and res[a]['Z_w'] and res[a]['I']
    # S: stable in the CC arms; under RR the rational striker works at a positive wage, so the boss's
    # (BOX(W1=work) -> wage 1/4) is a strict improvement (notes §1.14: a hand-table error corrected by code)
    assert res['G-all']['S'] and res['G-cred']['S'] and res['G-recip']['S'] and not res['G-cred-whole']['S']
    assert res['G-all']['F'] and res['G-cred']['F'] and not res['G-cred-whole']['F']
    assert res['G-all']['F_u'] and not res['G-cred-whole']['F_u']
    assert not res['G-all']['Z_D0'] and res['G-cred']['Z_D0'] and not res['G-cred-whole']['Z_D0']
    # S: gene-stable, Nash and Pareto-dominated (the proof device's counterexample)
    j = int(TCC['J'][NP['S']]); u = GA.PAY[j, 0, 0]
    assert GA.is_nash(j, 0, 0) and GA.pareto_dominated(u)


def test_sg_proposal_hand_state():
    A = R.arm('G-all')
    P = GA.sg_proposals(G, TCC, A, *R.named_progs()['Z_D0'])
    strict = [p for p in P['W1'] if p['kind'] == 'strict']
    assert any(p['gene'] == GA.wgene_name(GA.wgene(0, 1)) for p in strict)
    assert all(p['kind'] != 'strict' for p in P['B'])            # the boss is at its maximum
    # the boss's conservative choice keeps the wage at 0 (fixed order: wage overrides first)
    assert all(p['gene'].endswith('wage 0)') for p in P['B'])


def test_coalition_rate_neutral_pair():
    N = 20
    f = lambda k: (0.0, 0.0)
    rho2 = R.two_slot_fixation(f, f, N)
    assert abs(rho2 - 1.0 / N ** 2) < 1e-9


def test_gchain_matches_uchain_prior_kernel():
    from union_chain import UChain
    G_, A, T, L, Un, QSc, mB, mW = R.build_cell('base-CC', 'prior', 'uniform')
    ch = GA.GChain(L, Un, QSc, 0, 1000.0)
    seeds, _ = R.seeds_for(ch, G_, A, L, Un)
    ch.explore_hybrid(seeds)
    C = dict(Jc=L['Jc'], tagc=L['tagc'], KcB=L['KcB'], KcW=L['KcW'], massB=L['massB'], massW=L['massW'])
    uc = UChain(C, GA.C_WHACK, 1000.0, verbose=False)
    uc.explore_hybrid(seeds)
    assert np.array_equal(uc.codes, ch.codes)
    assert np.abs(uc.pi - ch.pi).max() < 1e-10


def test_local_kernel_lumping():
    """refined units: every program of a unit has the same local mutants' units (cap 1: depends on the base only)."""
    G_, A, T, L, Un, QSc, mB, mW = R.build_cell('G-all', 'SG', 'length')
    for k, x in enumerate(A['wsel'][:60]):
        u = Un['uw'][k]
        for g in range(GA.NWG):
            m = G.add_gene_w(int(x), g)
            assert Un['posW'].get(m, -1) == Un['LOCW'][u, g]
