"""The epsilon -> 0 chain, as a DIAGNOSTIC for the private-tape experiment (spec: the first item of the cut order).

Inspection: the whole state space of pairs of monomorphic role classes (22 x 24), exact two-population chain
(mixed2.TwoPopChain.solve_full; mutation to a role with probability 1/2, to a class by the prior, Moran fixation under constant
selection with fitness exp(w * net payoff)).  RPS: the chain over MONOMORPHIC states only (a symmetric zero-sum game with a price can
have polymorphic stable states, which this chain does not see; labelled in the report).
    python3 src/lt_tape_chain.py <game> <arm> <c> <N>
Writes runs/lt_tape/chain_<game>_<arm>_<c>_N<N>.json.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault('NUMBA_NUM_THREADS', '1')
import lt_tape_games as G
import lt_tape_run as RUN
import mixed2 as M2
import chain_log as CL

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'runs', 'lt_tape')


class _A:
    pass


def chain_insp(tb, N):
    A = _A()
    A.K = (len(tb.names[0]), len(tb.names[1]))
    A.UA, A.UB = tb.UA, tb.UB
    A.mass = [G.prior_masses(tb.sizes[ro]) for ro in range(2)]
    ch = M2.TwoPopChain(A, N)
    lpi = ch.solve_full()
    pi = np.exp(lpi - lpi.max()); pi /= pi.sum()
    P = pi.reshape(A.K)
    out = dict(N=N, game='insp', arm=tb.arm, c=tb.c)
    out['u0g'] = float((P * tb.UAg).sum()); out['u1g'] = float((P * tb.UBg.T).sum())
    out['efficient'] = float(P[(tb.UAg >= -0.05) & (tb.UBg.T >= -0.05)].sum())
    d0 = 1 - tb.G0[:, :, 2]; d1 = 1 - tb.G1[:, :, 2].T
    pI = np.divide(tb.G0[:, :, 0], d0, out=np.full(d0.shape, np.nan), where=d0 > 1e-12)
    qK = np.divide(tb.G1[:, :, 1].T, d1, out=np.full(d1.shape, np.nan), where=d1 > 1e-12)
    out['p_insp'] = float(np.nansum(P * np.nan_to_num(pI, nan=0.5)))
    out['q_cheat'] = float(np.nansum(P * np.nan_to_num(qK, nan=0.5)))
    pn = np.nan_to_num(pI, nan=0.5); qn = np.nan_to_num(qK, nan=0.5)
    out['commit_comply'] = float(P[(pn > 0.25 + 5e-3) & (qn < 0.1)].sum())
    fam0 = tb.fam[0]; fam1 = tb.fam[1]
    out['pi_role0'] = {f: float(P.sum(1)[fam0 == f].sum()) for f in G.FAMILIES}
    out['pi_role1'] = {f: float(P.sum(0)[fam1 == f].sum()) for f in G.FAMILIES}
    out['pi_names0'] = {n: float(v) for n, v in zip(tb.names[0], P.sum(1)) if v > 0.01}
    out['pi_names1'] = {n: float(v) for n, v in zip(tb.names[1], P.sum(0)) if v > 0.01}
    out['top_states'] = [(tb.names[0][i // A.K[1]], tb.names[1][i % A.K[1]], float(pi[i])) for i in np.argsort(-pi)[:8]]
    out['steps0'] = float((P * tb.S0).sum()); out['steps1'] = float((P * tb.S1.T).sum())
    return out


def chain_rps(tb, N):
    n = len(tb.names[0])
    mu = G.prior_masses(tb.sizes[0])
    LA = np.full((n, n), -np.inf)
    for i in range(n):
        du = tb.U[:, i] - tb.U[i, i]
        lr = M2.lrho(du, N, M2.W)
        for j in range(n):
            if j != i and mu[j] > 0:
                LA[i, j] = math.log(mu[j]) + lr[j]
    lpi, info = CL.stationary_log(LA, np.log(np.maximum(mu, 1e-300)))
    pi = np.exp(lpi - lpi.max()); pi /= pi.sum()
    U = tb.U
    out = dict(N=N, game='rps', arm=tb.arm, c=tb.c, info=info)
    out['pi_names'] = {nm: float(v) for nm, v in zip(tb.names[0], pi) if v > 0.01}
    out['pi_fam'] = {f: float(pi[tb.fam[0] == f].sum()) for f in G.FAMILIES}
    out['pi_U'] = float(pi[tb.names[0].index('U')])
    ex = tb.keep[0]
    out['e_indiv'] = float(sum(pi[i] * np.where(ex, tb.U[:, i], -1e9).max() for i in range(n)))
    Dself = tb.Gt[np.arange(n), np.arange(n)]
    out['forfeit_self'] = float((pi * Dself[:, 3]).sum())
    tv = 0.5 * np.abs(tb.Gt - RUN.UNI4).sum(-1)
    out['mix_self'] = float((pi * (0.5 * np.abs(Dself - RUN.UNI4).sum(-1) <= 0.05)).sum())
    out['top_states'] = [(tb.names[0][i], float(pi[i])) for i in np.argsort(-pi)[:8]]
    out['prior_U'] = float(mu[tb.names[0].index('U')])
    return out


if __name__ == '__main__':
    game, arm, cs, N = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    c = RUN.C0 if cs == 'c0' else float(cs)
    tb = RUN.Tables(game, arm, RUN.K0, c)
    res = chain_insp(tb, N) if game == 'insp' else chain_rps(tb, N)
    os.makedirs(OUT, exist_ok=True)
    name = 'chain_%s_%s_%s_N%d.json' % (game, arm, 'cprice' if cs == 'c0' else 'cfree', N)
    with open(os.path.join(OUT, name), 'w') as f:
        json.dump(res, f, indent=1)
    print(name, {k: v for k, v in res.items() if k in ('u0g', 'u1g', 'efficient', 'p_insp', 'q_cheat', 'pi_U', 'e_indiv')})
