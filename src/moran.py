"""Finite-N Moran simulation: the check on the attractor chain.

Each step: with probability eps a random agent is replaced by a draw from
mu (over mutant classes); otherwise one agent reproduces with probability
proportional to exp(s * fitness) and replaces a random agent.  Fitness is
the mean payoff against the other N-1 agents.  Occupancy is recorded by
support set (which types are present), which is the coarse statistic that
can be compared with the chain's pi without aligning grid positions.
"""
import numpy as np
from collections import defaultdict


def simulate(U, mu, N, eps, steps, s=1.0, seed=0, burn=0.1, init=None):
    rng = np.random.default_rng(seed)
    K = len(mu)
    mu = np.asarray(mu, float); mu = mu / mu.sum()
    if init is None:
        init = rng.choice(K, p=mu)
    counts = np.zeros(K, int)
    counts[init] = N
    occ = defaultdict(float)
    comp = defaultdict(float)
    nburn = int(burn * steps)
    for t in range(steps):
        if rng.random() < eps:
            # mutation: replace a random agent
            victim = rng.choice(K, p=counts / N)
            q = rng.choice(K, p=mu)
            counts[victim] -= 1; counts[q] += 1
        else:
            present = np.nonzero(counts)[0]
            if len(present) > 1:
                sub = U[np.ix_(present, present)]
                c = counts[present]
                # fitness against the other N-1 agents
                fit = (sub @ c - np.diag(sub) * 1.0) / (N - 1)
                w = c * np.exp(s * (fit - fit.max()))
                parent = present[rng.choice(len(present), p=w / w.sum())]
                victim = rng.choice(K, p=counts / N)
                counts[victim] -= 1; counts[parent] += 1
        if t >= nburn:
            key = tuple(np.nonzero(counts)[0].tolist())
            occ[key] += 1
            comp[key] += 0  # placeholder for composition stats
    z = sum(occ.values())
    return {k: v / z for k, v in occ.items()}


def chain_support_occupancy(chain, prov):
    """Aggregate the chain's pi by support (as class-rep indices)."""
    pos = {rep: k for k, (rep, _, _) in enumerate(prov.classes)}
    occ = defaultdict(float)
    for key, w in zip(chain.keys_list, chain.pi):
        ids = chain.states[key][0]
        occ[tuple(sorted(pos[p] for p in ids))] += w
    return occ
