"""Agent-based check for the three-player dollar at finite eps*N (approach
rates, not pi).

Three populations of N programs (payoff-class representatives), one per slot.
An event picks a slot uniformly; a parent in that slot reproduces with
probability proportional to count * exp(w * mean payoff), the mean taken over
random encounters with one member of each other population (no self-play,
fixed roles); with probability eps the offspring is a fresh draw from the
slot's prior over classes; a uniformly random member of the slot dies.  A
generation is 3N events (N births per slot on average).  Every `every`
generations the encounter-level outcome distribution is recorded, with the
dominant coalition label: the outcome of the triple of majority classes when
every slot has a class above 1/2 of its population, else 'mixed'.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dollar3 as D
from abm import njit

TMAX = 160


@njit(cache=True)
def _fill(arm, nat, atL, atJ, atA, tab, PARTNER, reps, tid, W, s, t):
    """W[i0, i1, i2] = packed outcome for active indices; fill the slice of
    slot s at index t against every active index of the other slots."""
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64); u = np.empty(3, np.int64)
    for a in range(TMAX):
        if (s != 0 and tid[0, a] < 0) or (s == 0 and a != t):
            continue
        for b in range(TMAX):
            if (s != 1 and tid[1, b] < 0) or (s == 1 and b != t):
                continue
            for c in range(TMAX):
                if (s != 2 and tid[2, c] < 0) or (s == 2 and c != t):
                    continue
                typ = D.enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, reps[0, tid[0, a]], reps[1, tid[1, b]], reps[2, tid[2, c]], hist, val, u)
                W[a, b, c] = typ * 125 + u[0] * 25 + u[1] * 5 + u[2]


@njit(cache=True)
def _add(arm, nat, atL, atJ, atA, tab, PARTNER, reps, tid, cnt, W, s, cl):
    for t in range(TMAX):
        if tid[s, t] == cl:
            cnt[s, t] += 1
            return t
    for t in range(TMAX):
        if tid[s, t] < 0:
            tid[s, t] = cl; cnt[s, t] = 1
            _fill(arm, nat, atL, atJ, atA, tab, PARTNER, reps, tid, W, s, t)
            return t
    return -1


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
def run(arm, nat, atL, atJ, atA, tab, PARTNER, reps, cdfs, init, N, w, eps, gens, every, seed):
    """init[s, k]: initial class of member k of slot s.  Returns per record:
    outcome-type probabilities (5), mean payoffs (3), dominant classes (3, -1 if
    none) and dominant outcome packed (-1 if none)."""
    np.random.seed(seed)
    tid = -np.ones((3, TMAX), np.int64); cnt = np.zeros((3, TMAX), np.int64)
    W = np.zeros((TMAX, TMAX, TMAX), np.int64)
    member = np.empty((3, N), np.int64)       # active index of each member
    for s in range(3):
        for k in range(N):
            member[s, k] = _add(arm, nat, atL, atJ, atA, tab, PARTNER, reps, tid, cnt, W, s, init[s, k])
    nrec = gens // every
    rec_typ = np.zeros((nrec, 5)); rec_pay = np.zeros((nrec, 3)); rec_dom = -np.ones((nrec, 3), np.int64); rec_out = -np.ones(nrec, np.int64)
    fit = np.zeros(TMAX); act = np.empty(TMAX, np.int64)
    ri = 0
    for g in range(gens):
        for ev in range(3 * N):
            s = np.random.randint(3)
            o1 = 1 if s == 0 else 0
            o2 = 2 if s != 2 else 1
            # payoffs of active types in slot s
            na = 0
            for t in range(TMAX):
                if tid[s, t] >= 0:
                    act[na] = t; na += 1
            tot = 0.0
            for ii in range(na):
                t = act[ii]; acc = 0.0
                for b in range(TMAX):
                    if tid[o1, b] < 0: continue
                    xb = cnt[o1, b]
                    for c in range(TMAX):
                        if tid[o2, c] < 0: continue
                        if s == 0:
                            code = W[t, b, c]
                        elif s == 1:
                            code = W[b, t, c]
                        else:
                            code = W[b, c, t]
                        uu = code % 125
                        us = (uu // 25) if s == 0 else ((uu // 5) % 5 if s == 1 else uu % 5)
                        acc += xb * cnt[o2, c] * us
                pay = acc / (N * N) / 6.0
                fit[ii] = cnt[s, t] * np.exp(w * pay)
                tot += fit[ii]
            r = np.random.random() * tot
            par = act[na - 1]
            for ii in range(na):
                r -= fit[ii]
                if r <= 0:
                    par = act[ii]; break
            if np.random.random() < eps:
                cl = _sample_cdf(cdfs[s], np.random.random())
            else:
                cl = tid[s, par]
            k = np.random.randint(N)
            old = member[s, k]
            cnt[s, old] -= 1
            if cnt[s, old] == 0:
                tid[s, old] = -1
            member[s, k] = _add(arm, nat, atL, atJ, atA, tab, PARTNER, reps, tid, cnt, W, s, cl)
        if (g + 1) % every == 0 and ri < nrec:
            for a in range(TMAX):
                if tid[0, a] < 0: continue
                for b in range(TMAX):
                    if tid[1, b] < 0: continue
                    for c in range(TMAX):
                        if tid[2, c] < 0: continue
                        p = cnt[0, a] * cnt[1, b] * cnt[2, c] / (N * N * N)
                        code = W[a, b, c]
                        uu = code % 125
                        rec_typ[ri, code // 125] += p
                        rec_pay[ri, 0] += p * (uu // 25) / 6.0; rec_pay[ri, 1] += p * ((uu // 5) % 5) / 6.0; rec_pay[ri, 2] += p * (uu % 5) / 6.0
            dom = np.empty(3, np.int64); ok = True
            for s in range(3):
                dom[s] = -1
                for t in range(TMAX):
                    if tid[s, t] >= 0 and 2 * cnt[s, t] > N:
                        dom[s] = t
                if dom[s] < 0:
                    ok = False
                rec_dom[ri, s] = tid[s, dom[s]] if dom[s] >= 0 else -1
            if ok:
                rec_out[ri] = W[dom[0], dom[1], dom[2]]
            ri += 1
    return rec_typ, rec_pay, rec_dom, rec_out


# ---------------------------------------------------------------- driver
def cell(job):
    """job = (arm, start, seed, N, eps, gens, every, w)."""
    import json
    from dollar3_run import build_chain
    arm, start, seed, N, eps, gens, every, w = job
    ch, S = build_chain(arm, N, w, 1e-9, 10)
    m = ch.mass.copy()
    cdfs = np.cumsum(m, axis=1); cdfs /= cdfs[:, -1:]
    rng = np.random.default_rng(seed)
    if start == 'uniform':
        init = rng.integers(0, ch.Kc, size=(3, N))
    else:
        init = np.array([[ch.const_class[s][D.local_of(s, D.ALL, 0)]] * N for s in range(3)])
    t = time.time()
    typ, pay, dom, out = run(ch.ia, *ch.A, ch.reps, cdfs, init.astype(np.int64), N, w, eps, gens, every, seed)
    res = dict(arm=arm, start=start, seed=seed, N=N, eps=eps, gens=gens, every=every, w=w, time_s=time.time() - t)
    # dominant coalition label per record
    lab = []
    for o in out:
        if o < 0:
            lab.append('mixed'); continue
        t_ = o // 125; uu = o % 125; u = (uu // 25, (uu // 5) % 5, uu % 5)
        if t_ == 4: lab.append('X')
        elif t_ == 0: lab.append('G')
        else:
            sl = [i + 1 for i in range(3) if u[i] > 0]; lab.append('P%d%d' % tuple(sl))
    res['labels'] = lab
    res['typ'] = typ.tolist(); res['pay'] = pay.tolist()
    res['dom_src'] = [[S.src(s, ch.reps[s, d[s]]) if d[s] >= 0 else None for s in range(3)] for d in dom[::max(1, len(dom) // 200)]]
    return res
