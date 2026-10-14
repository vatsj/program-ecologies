"""Tests for dominance contracts and refusal on islands (notes/dominance-contracts.md §1.10)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import stable_sets as SS
import stable_sets_run as SR
import dollar3 as D
import dominance_contracts as DC

G = SS.dollar3_game()
X = G.R
IDX = {x: k for k, x in enumerate(X)}
V = SS.symmetric_set(X, 6)
T = SS.Tables(G)
S_, MU = SS.arm_data('weak')
CI = SS.const_index(S_.fs)
U9 = [np.array(sorted(CI[l] for l in range(9)), np.int64) for _ in range(3)]
POS = {x: j for j, x in enumerate(U9[0])}
lo = D.local_of


def homogeneous(profiles, N):
    I = len(profiles)
    init = np.zeros((I, 3, 9), np.int64)
    for i, a in enumerate(profiles):
        for s in range(3):
            init[i, s, POS[CI[a[s]]]] = N
    return init


def fair12(k3):
    return (lo(0, 1, 1), lo(1, 0, 1), k3)


def test_contract_universe_and_proposal_rule():
    assert len(DC.CONTRACTS) == 27
    assert sum(1 for (S, a, b) in DC.CONTRACTS if a + b > 6) == 9      # three per pair
    props = lambda y: sorted(SS.label(DC.contract_x(k)) for k in range(27) if DC.proposed(k, y))
    assert props((3, 3, 0)) == ['P13:4|2', 'P23:4|2']          # a member is left only for unequal pairs
    assert props((4, 2, 0)) == ['P23:3|2', 'P23:3|3', 'P23:4|2']
    assert len(props((3, 2, 0))) == 4 and len(props((2, 2, 0))) == 7
    assert len(props((2, 2, 2))) == 3 and len(props((0, 0, 0))) == 18
    # every recurrent outsider has exactly one proposed contract into V*
    for y in X:
        cat = SS.category(y, 6)
        if cat in ('unequal',) or (cat == 'wasteful' and max(y) == 3):
            assert sum(1 for k in range(27) if DC.proposed(k, y) and IDX[DC.contract_x(k)] in V) == 1


def test_generator_and_anchor():
    M = SS.dom_M(X, 6)
    pu = DC.stationary(DC.uniform_successor(X, M))
    assert abs(pu[list(V)].sum() - 4 / 17) < 1e-9                # the spec's 0.235
    Q, nprop, mult = DC.generator(X)
    assert mult.max() == 1
    pg = DC.stationary(Q)
    assert abs(pg[list(V)].sum() - 1 / 3) < 1e-9
    Qa = Q.copy()
    for v in V:
        Qa[v] = 0; Qa[v, v] = 1
    ht = DC.hitting_times(Qa, V)
    assert abs(ht[IDX[(4, 2, 0)]] - 27) < 1e-9 and abs(ht[IDX[(3, 2, 0)]] - 27) < 1e-9


def test_nu0_reproduces_stable_sets_kernel():
    for (mN, law, H, I, N, sd) in [(0, 'L', 300, 8, 30, 1), (1, 'L', 200, 6, 30, 2)]:
        p = dict(law=law, mN=mN, arm='weak', I=I, N=N, name='val')
        loc, U, J, conds, I_, N_ = SR.build_run(p, sd)
        seed = 1000 + sd; hrec = np.array([H], np.int64)
        a = SS.kern(J, T.PAY, T.VEC, T.ISMEM, T.TOT, loc, N, SS.W, mN / N, seed, H, 10, hrec, 100000)
        b = DC.run_kernel(DC.Setup(loc, U), T, N, mN, seed, H, hrec, nu=0.0)
        K = loc.shape[2]
        assert a[0] == b[0] and a[1] == b[1] and a[8] == b[8]
        assert (a[2] == b[2][:, :, :K]).all() and (a[3] == b[3]).all()


def test_atomic_contract_jumps_exactly_to_x():
    N = 20
    profs = [fair12(k3) for k3 in range(9)] + [(lo(0, 1, 2), lo(1, 0, 0), k3) for k3 in range(9)]
    st = DC.Setup(homogeneous(profs, N), U9)
    out = DC.run_kernel(st, T, N, 0, 7, 60, np.array([60], np.int64), nu=1.0)
    cls, cev = out[3], out[9]
    n = 0
    for row in cev:
        g, i, kap, status = int(row[0]), int(row[1]), int(row[2]), int(row[3])
        if status == 2 and g + 1 < cls.shape[0]:
            assert cls[g + 1, i] == T.ridx[DC.contract_x(kap)]
            # proposal held at the pre-event state
            y = X[int(cls[g, i])]
            assert DC.proposed(kap, y)
            n += 1
    assert n > 20


def test_refusal_guard_public_makes_members_absorbing():
    N = 20
    profs = [fair12(k3) for k3 in range(9)] * 2
    st = DC.Setup(homogeneous(profs, N), U9, fr=1.0, rng=np.random.default_rng(1))
    out = DC.run_kernel(st, T, N, 0, 11, 300, np.array([300], np.int64), nu=1.0, consent=DC.CONSENT['public'])
    cls, cev = out[3], out[9]
    assert np.isin(cls, list(V)).all()                    # never leaves the member it starts on
    assert (cev[:, 3] == 1).all() and (cev[:, 10] == 1).all() and len(cev) > 50
    # without the bit the same islands leave
    st0 = DC.Setup(homogeneous(profs, N), U9)
    out0 = DC.run_kernel(st0, T, N, 0, 11, 300, np.array([300], np.int64), nu=1.0)
    assert not np.isin(out0[3][-1], list(V)).all()


def test_private_refusers_keep_their_demand_and_genes_are_inherited():
    N = 40
    profs = [fair12(lo(2, 0, 0))] * 150                   # the excluded slot already offers slot 1 a third
    st = DC.Setup(homogeneous(profs, N), U9, fr=0.5, rng=np.random.default_rng(3))
    out = DC.run_kernel(st, T, N, 0, 5, 2, np.array([2], np.int64), nu=1.0, consent=DC.CONSENT['private'])
    tcount, cev = out[2], out[9]
    guarded = [row for row in cev if int(row[3]) == 2 and row[10] > 0 and int(row[0]) == 1]
    assert len(guarded) >= 1
    for row in guarded:
        if True:
            i = int(row[1]); kap = int(row[2]); Sx = DC.CONTRACTS[kap][0]
            for z, s in enumerate(Sx):
                assert row[13 + z] == row[17 + z] and row[11 + z] + row[13 + z] == N   # refusers kept, the rest installed
                assert all(st.TR[s, t] == 0 for t in range(st.ntypes[s]) if st.TO[s, t] >= 0 and tcount[i, s, t] > 0)
    # inheritance under beta < 1: installed overrides are copied by births and keep their refusal bit
    st2 = DC.Setup(homogeneous([fair12(lo(2, 0, 0))] * 6, N), U9, fr=0.5, rng=np.random.default_rng(4))
    out2 = DC.run_kernel(st2, T, N, 0, 9, 200, np.array([200], np.int64), nu=0.05, beta=0.5)
    tc2 = out2[2]
    grew = 0
    for row in out2[9]:
        if int(row[3]) == 2:
            i = int(row[1]); s = DC.CONTRACTS[int(row[2])][0][0]
            ov = sum(tc2[i, s, t] for t in range(st2.ntypes[s]) if st2.TO[s, t] >= 0)
            grew += ov > row[11]
    assert grew >= 1
    assert set(st2.TR[0, :st2.ntypes[0]]) <= {0, 1}


def test_menu_G_only_shrinks_without_migration():
    p = dict(mN=0, nu=0.1, menu='G', H=300, seedbase='L0', I=8, N=30)
    import dominance_contracts_run as DR
    st, I, N = DR.build(p, 0)
    out = DC.run_kernel(st, T, N, 0, 3, 300, np.array([300], np.int64), nu=0.1, menu_g=True)
    menus = out[13]
    for j in range(1, menus.shape[0]):
        assert ((menus[j] & ~menus[j - 1]) == 0).all()
    assert menus[0].any()
