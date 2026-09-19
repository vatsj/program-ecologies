"""Finite-N Moran simulation: the check on the attractor chain.

Each step: with probability eps a random agent is replaced by a draw from
mu (over mutant classes); otherwise one agent reproduces with probability
proportional to exp(w * payoff) (the same map as the chain's fixation
probabilities) and replaces a random agent.  Payoff is the mean
against the other N-1 agents.  Occupancy is recorded by support set and by
majority type.
"""
import numpy as np
from collections import defaultdict


def simulate(U, mu, N, eps, steps, w=1.0, seed=0, burn=0.1, init=None):
    rng = np.random.default_rng(seed)
    K = len(mu)
    mu = np.asarray(mu, float); mu = mu / mu.sum()
    if init is None:
        init = rng.choice(K, p=mu)
    counts = np.zeros(K, int)
    counts[init] = N
    occ = defaultdict(float)
    maj = defaultdict(float)
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
                f = np.exp(w * (fit - fit.max()))
                wt = c * f
                parent = present[rng.choice(len(present), p=wt / wt.sum())]
                victim = rng.choice(K, p=counts / N)
                counts[victim] -= 1; counts[parent] += 1
        if t >= nburn:
            key = tuple(np.nonzero(counts)[0].tolist())
            occ[key] += 1
            maj[int(np.argmax(counts))] += 1
    z = sum(occ.values())
    return {k: v / z for k, v in occ.items()}, {k: v / z for k, v in maj.items()}


def chain_occupancy(chain, prov):
    """The chain's pi by support and by majority type (class-rep indices)."""
    pos = {rep: k for k, (rep, _, _) in enumerate(prov.classes)}
    occ = defaultdict(float); maj = defaultdict(float)
    for key, w in zip(chain.keys_list, chain.pi):
        ids, x, kind = chain.states[key]
        occ[tuple(sorted(pos[p] for p in ids))] += w
        maj[pos[ids[int(np.argmax(x))]]] += w
    return occ, maj
