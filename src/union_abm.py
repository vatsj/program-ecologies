"""Finite-eps agent-based runs and island runs for the union game (approach
rates, not pi).

Each island holds three populations of N programs (behavioural-class
representatives), one per slot (boss, W1, W2).  A birth event picks an island i
and a slot s uniformly.  With probability m = mN / N the parent comes from
another island j (complete graph), drawn with weight exp(w_g[s] * mean payoff
of slot s on island j) (w_g = 0: uniform), as in src/islands.py / multilevel.py;
otherwise from island i.  Within the source island the parent is drawn with
probability proportional to count * exp(w * mean payoff), the mean taken over
encounters with one member of each other slot population of that island.  With
probability eps the offspring is a fresh draw from the slot's prior over classes.
A uniformly random member of slot s on island i dies.  A generation is 3 N
births per island.  I = 1 is the single-island agent-based run.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import union as U
from abm import njit

TMAX = 16


@njit(cache=True)
def slot_pay(Jc, tagc, PAY, tid, cnt, i, s, t, N):
    """Mean payoff of class t in slot s on island i against the island's other
    two slot populations (one member of each per encounter)."""
    o1 = 1 if s == 0 else 0
    o2 = 2 if s != 2 else 1
    acc = 0.0
    for a in range(TMAX):
        if cnt[i, o1, a] == 0: continue
        ca = tid[i, o1, a]
        for b in range(TMAX):
            if cnt[i, o2, b] == 0: continue
            cb = tid[i, o2, b]
            if s == 0:
                xb, x1, x2 = t, ca, cb
            elif s == 1:
                xb, x1, x2 = ca, t, cb
            else:
                xb, x1, x2 = ca, cb, t
            j = Jc[xb, x1, x2]
            acc += cnt[i, o1, a] * cnt[i, o2, b] * PAY[j, tagc[x1], tagc[x2], s]
    return acc / (N * N)


@njit(cache=True)
def _sample_cdf(cdf, r):
    lo = 0; hi = cdf.shape[0] - 1
    while lo < hi:
        m = (lo + hi) // 2
        if cdf[m] < r:
            lo = m + 1
        else:
            hi = m
    return lo


@njit(cache=True)
def _parent(Jc, tagc, PAY, tid, cnt, i, s, N, w, fit):
    mx = -1e300
    for t in range(TMAX):
        if cnt[i, s, t] > 0:
            fit[t] = slot_pay(Jc, tagc, PAY, tid, cnt, i, s, tid[i, s, t], N)
            if fit[t] > mx: mx = fit[t]
    tot = 0.0
    for t in range(TMAX):
        if cnt[i, s, t] > 0:
            fit[t] = cnt[i, s, t] * np.exp(w * (fit[t] - mx)); tot += fit[t]
        else:
            fit[t] = 0.0
    r = np.random.random() * tot
    last = -1
    for t in range(TMAX):
        if fit[t] > 0:
            last = t
            r -= fit[t]
            if r <= 0:
                return tid[i, s, t]
    return tid[i, s, last]


@njit(cache=True)
def _add(tid, cnt, i, s, cl):
    free = -1
    for t in range(TMAX):
        if cnt[i, s, t] > 0 and tid[i, s, t] == cl:
            cnt[i, s, t] += 1
            return True
        if free < 0 and cnt[i, s, t] == 0:
            free = t
    if free < 0:
        return False
    tid[i, s, free] = cl; cnt[i, s, free] = 1
    return True


@njit(cache=True)
def _island_mean(Jc, tagc, PAY, tid, cnt, i, s, N):
    acc = 0.0
    for t in range(TMAX):
        if cnt[i, s, t] > 0:
            acc += cnt[i, s, t] * slot_pay(Jc, tagc, PAY, tid, cnt, i, s, tid[i, s, t], N)
    return acc / N


@njit(cache=True)
def run(Jc, tagc, PAY, SUMM, WAGE, WHK, cdfs, init, I, N, w, eps, mN, wg, gens, every, seed):
    """init[i, s]: initial class of every member of slot s on island i.
    SUMM[j, t1, t2]: summary code (0..6); WAGE[j], WHK[j]: wage and whack index.
    Records every `every` generations, per island: encounter-level summary
    distribution (7), wage x whack-policy distribution (9), mean payoffs (3),
    dominant classes (3; -1 if no class holds > 1/2 of its slot)."""
    np.random.seed(seed)
    tid = np.zeros((I, 3, TMAX), np.int64); cnt = np.zeros((I, 3, TMAX), np.int64)
    for i in range(I):
        for s in range(3):
            tid[i, s, 0] = init[i, s]; cnt[i, s, 0] = N
    nrec = gens // every
    r_sum = np.zeros((nrec, I, 7)); r_sw = np.zeros((nrec, I, 9)); r_pay = np.zeros((nrec, I, 3))
    r_dom = -np.ones((nrec, I, 3), np.int64)
    fit = np.zeros(TMAX); gw = np.zeros(I)
    m = mN / N
    overflow = 0
    ri = 0
    for g in range(gens):
        for ev in range(3 * N * I):
            i = np.random.randint(I); s = np.random.randint(3)
            src = i
            if I > 1 and np.random.random() < m:
                if wg[s] == 0.0:
                    src = np.random.randint(I - 1)
                    if src >= i: src += 1
                else:
                    mx = -1e300
                    for j in range(I):
                        if j == i:
                            gw[j] = -1e300; continue
                        gw[j] = _island_mean(Jc, tagc, PAY, tid, cnt, j, s, N)
                        if gw[j] > mx: mx = gw[j]
                    tot = 0.0
                    for j in range(I):
                        if j == i:
                            gw[j] = 0.0
                        else:
                            gw[j] = np.exp(wg[s] * (gw[j] - mx)); tot += gw[j]
                    r = np.random.random() * tot; src = -1
                    for j in range(I):
                        if gw[j] > 0:
                            src = j
                            r -= gw[j]
                            if r <= 0:
                                break
            child = _parent(Jc, tagc, PAY, tid, cnt, src, s, N, w, fit)
            if eps > 0.0 and np.random.random() < eps:
                child = _sample_cdf(cdfs[s], np.random.random())
            # victim uniform on island i, slot s
            k = np.random.randint(N); acc = 0; vt = -1
            for t in range(TMAX):
                acc += cnt[i, s, t]
                if k < acc:
                    vt = t; break
            if tid[i, s, vt] == child:
                continue
            if not _add(tid, cnt, i, s, child):
                overflow += 1
                continue
            cnt[i, s, vt] -= 1
        if (g + 1) % every == 0 and ri < nrec:
            for i in range(I):
                for a in range(TMAX):
                    if cnt[i, 0, a] == 0: continue
                    for b in range(TMAX):
                        if cnt[i, 1, b] == 0: continue
                        for c in range(TMAX):
                            if cnt[i, 2, c] == 0: continue
                            p = cnt[i, 0, a] * cnt[i, 1, b] * cnt[i, 2, c] / (N * N * N)
                            x1 = tid[i, 1, b]; x2 = tid[i, 2, c]
                            j = Jc[tid[i, 0, a], x1, x2]
                            t1 = tagc[x1]; t2 = tagc[x2]
                            r_sum[ri, i, SUMM[j, t1, t2]] += p
                            r_sw[ri, i, 3 * WAGE[j] + WHK[j]] += p
                            for s in range(3):
                                r_pay[ri, i, s] += p * PAY[j, t1, t2, s]
                for s in range(3):
                    for t in range(TMAX):
                        if 2 * cnt[i, s, t] > N:
                            r_dom[ri, i, s] = tid[i, s, t]
            ri += 1
    return r_sum, r_sw, r_pay, r_dom, overflow


def tables():
    SUMM = np.zeros((36, 2, 2), np.int64)
    for j in range(36):
        for t1 in range(2):
            for t2 in range(2):
                SUMM[j, t1, t2] = U.summary(j, t1, t2)
    WAGE = np.array([(j // 4) // 3 for j in range(36)], np.int64)
    WHK = np.array([(j // 4) % 3 for j in range(36)], np.int64)
    return SUMM, WAGE, WHK
