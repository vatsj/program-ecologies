"""Stationary distribution of a sparse chain with log-rates, by GTH state
reduction in log space (no subtractions, no underflow): rates at large N
span e^-1000 and more, beyond double range, and LU on the generator fails
already at N = 10^3 (checked against dense GTH on the constants chain).

Phase 1 eliminates states in order of increasing in-degree x out-degree
(sparse, Python dicts) until `core` states remain; phase 2 is dense log-GTH
on the core (numba); back-substitution gives log pi for every state.
"""
import heapq, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit

NEG = -np.inf


def _lae(a, b):
    if a == NEG: return b
    if b == NEG: return a
    if a > b: return a + math.log1p(math.exp(b - a))
    return b + math.log1p(math.exp(a - b))


@njit(cache=True)
def _lse_row(x, n):
    m = -np.inf
    for t in range(n):
        if x[t] > m: m = x[t]
    if m == -np.inf:
        return m
    s = 0.0
    for t in range(n):
        s += np.exp(x[t] - m)
    return m + np.log(s)


@njit(cache=True)
def dense_log_gth(A):
    """A[i, j] = log rate i -> j (diagonal ignored). Returns log pi."""
    K = A.shape[0]
    A = A.copy()
    for i in range(K):
        A[i, i] = -np.inf
    for k in range(K - 1, 0, -1):
        s = _lse_row(A[k], k)
        if s == -np.inf:
            s = -1e300
        for i in range(k):
            A[i, k] -= s
        for i in range(k):
            aik = A[i, k]
            if aik == -np.inf:
                continue
            for j in range(k):
                if i == j:
                    continue
                v = aik + A[k, j]
                if v == -np.inf:
                    continue
                a = A[i, j]
                if a == -np.inf:
                    A[i, j] = v
                elif a > v:
                    A[i, j] = a + np.log1p(np.exp(v - a))
                else:
                    A[i, j] = v + np.log1p(np.exp(a - v))
    lp = np.full(K, -np.inf)
    lp[0] = 0.0
    for k in range(1, K):
        m = -np.inf
        for i in range(k):
            v = lp[i] + A[i, k]
            if v > m: m = v
        if m == -np.inf:
            continue
        s = 0.0
        for i in range(k):
            s += np.exp(lp[i] + A[i, k] - m)
        lp[k] = m + np.log(s)
    m = lp.max()
    return lp - (m + np.log(np.exp(lp - m).sum()))


def log_stationary(n, src, dst, lrate, core=2000):
    out = [dict() for _ in range(n)]
    inn = [set() for _ in range(n)]
    for i, j, l in zip(src.tolist(), dst.tolist(), lrate.tolist()):
        if i == j or l == NEG: continue
        d = out[i]
        d[j] = _lae(d.get(j, NEG), l)
        inn[j].add(i)
    alive = np.ones(n, bool)
    heap = [(len(inn[k]) * len(out[k]), k) for k in range(n)]
    heapq.heapify(heap)
    elim = []          # (k, [(i, log A[i,k] - s_k)])
    remaining = n
    while remaining > core and heap:
        c, k = heapq.heappop(heap)
        if not alive[k]: continue
        cur = len(inn[k]) * len(out[k])
        if cur != c:
            heapq.heappush(heap, (cur, k)); continue
        outs = out[k]
        s = NEG
        for j, l in outs.items():
            s = _lae(s, l)
        if s == NEG: s = -1e300
        ins = [(i, out[i][k] - s) for i in inn[k]]
        for i, lik in ins:
            oi = out[i]
            del oi[k]
            for j, lkj in outs.items():
                if j == i: continue
                v = lik + lkj
                if j in oi:
                    oi[j] = _lae(oi[j], v)
                else:
                    oi[j] = v; inn[j].add(i)
        for j in outs:
            inn[j].discard(k)
        for i, _ in ins:
            heapq.heappush(heap, (len(inn[i]) * len(out[i]), i))
        for j in outs:
            heapq.heappush(heap, (len(inn[j]) * len(out[j]), j))
        out[k] = {}; inn[k] = set()
        alive[k] = False; remaining -= 1
        elim.append((k, ins))
    core_ids = np.nonzero(alive)[0]
    pos = {int(k): t for t, k in enumerate(core_ids)}
    A = np.full((len(core_ids), len(core_ids)), NEG)
    for k in core_ids:
        for j, l in out[k].items():
            A[pos[int(k)], pos[j]] = l
    lpc = dense_log_gth(A)
    lp = np.full(n, NEG)
    lp[core_ids] = lpc
    for k, ins in reversed(elim):
        v = NEG
        for i, l in ins:
            v = _lae(v, lp[i] + l)
        lp[k] = v
    m = lp.max()
    return lp - (m + math.log(np.exp(lp - m).sum()))
