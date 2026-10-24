"""Sampled-encounter island lotteries with per-island read ledgers (rule B, cold cache) and the matched bridges (F, A, F+A,
zero price through the same sampled kernel), for RPS and the inspection game.

Each generation every individual plays `nenc` encounters as the row player against uniformly drawn members of its opponent
population on its island; a leaf of the decision tree is drawn for each side from the exact leaf weights of the instrumented
engine (so actions, steps, read calls and time-outs are jointly sampled); the individual's fitness is the mean of
(game payoff - the rule's charge) over its encounters; then 2 I N (inspection) or I N (RPS) replacement events with parent
probability proportional to exp(w * fitness) on the source island (migration probability m from a uniform other island),
victim uniform.  Under rule B the charge of a leaf is computed against the island's ledger of keys: the root's own steps plus
the own steps of every read call that is neither cached nor under a cached call; the executed calls' keys are inserted.  The
ledger belongs to the island and migrates with nobody.  warm=1 starts with every key cached.
"""
import os
import sys

import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pricing_rules as P
import lt_tape_games as G
import rps as RP
import mixed2 as M2

NENC = 10
CPS_S = np.array([500, 1000, 1500, 2000], np.int64)        # sampled cells stop at 2,000
RC = {'Z': 0, 'Zs': 0, 'F': 1, 'Fs': 1, 'A': 2, 'As': 2, 'FA': 3, 'FAs': 3, 'B': 4, 'T': 5}


class Flat:
    """The leaves of a matrix of pairs (x plays y) in flat arrays."""

    def __init__(self, base, xs, ys, outmap, K):
        nx, ny = len(xs), len(ys)
        self.ps = np.zeros((nx, ny), np.int64); self.pn = np.zeros((nx, ny), np.int64)
        cum = []; out = []; S = []; nto = []; fa = []; ncall = []; cs = []; cn = []; top = []
        cpar = []; ckey = []; cstep = []; cown = []
        maxc = 1
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                rec = base.eng.ledger(x, y)
                self.ps[i, j] = len(cum)
                acc = 0.0
                for (w, o, used, calls, reason) in rec['leaves']:
                    acc += float(w)
                    cum.append(acc); out.append(outmap.get(o, outmap['BOT']))
                    n_to, n_top, steps_top, nc, toplv = P.leaf_stats(used, calls)
                    S.append(used); nto.append(n_to); fa.append(used - steps_top + K * n_top); ncall.append(nc)
                    top.append(toplv)
                    cs.append(len(cpar)); cn.append(len(calls)); maxc = max(maxc, len(calls))
                    idx = {c[0]: q for q, c in enumerate(calls)}
                    kids = {}
                    for c in calls: kids.setdefault(c[1], 0)
                    ch = {}
                    for c in calls: ch[c[1]] = ch.get(c[1], 0) + c[4]
                    for c in calls:
                        cpar.append(idx.get(c[1], -1)); ckey.append(c[3]); cstep.append(c[4])
                        cown.append(c[4] - ch.get(c[0], 0))
                self.pn[i, j] = len(cum) - self.ps[i, j]
                cum[-1] = 1.0
        self.cum = np.array(cum); self.out = np.array(out, np.int64); self.S = np.array(S, float)
        self.nto = np.array(nto, float); self.fa = np.array(fa, float); self.ncall = np.array(ncall, float)
        self.top = np.array(top, float)
        self.cs = np.array(cs, np.int64); self.cn = np.array(cn, np.int64)
        self.cpar = np.array(cpar if cpar else [0], np.int64); self.ckey = np.array(ckey if ckey else [0], np.int64)
        self.cstep = np.array(cstep if cstep else [0.0], float); self.cown = np.array(cown if cown else [0.0], float)
        self.maxc = maxc


class SampledData:
    def __init__(self, base, rule, level):
        self.game = base.game
        K = base.K
        if base.game == 'rps':
            terms = base.tb.terms[0]
            self.f0 = Flat(base, terms, terms, {'R': 0, 'P': 1, 'S': 2, 'BOT': 3}, K)
            u = np.zeros((4, 4))
            for a, na in enumerate('RPS'):
                for b, nb in enumerate('RPS'):
                    u[a, b] = G.RPS.u(na, nb)
            for a in range(3): u[a, 3] = 1.0; u[3, a] = -1.0
            self.u = u
        else:
            t0, t1 = base.tb.terms
            self.f0 = Flat(base, t0, t1, {'I': 0, 'N': 1, 'BOT': 2}, K)        # inspector a plays inspectee b
            self.f1 = Flat(base, t1, t0, {'C': 0, 'K': 1, 'BOT': 2}, K)        # inspectee b plays inspector a
            self.V0, self.V1 = G.insp_payoff_tensors()
        self.nkeys = max(1, len(base.eng.key_list))
        self.maxc = self.f0.maxc if base.game == 'rps' else max(self.f0.maxc, self.f1.maxc)


@njit(cache=True)
def _pick(cum, ps, pn, a, b):
    s = ps[a, b]; n = pn[a, b]
    u = np.random.random()
    for t in range(n):
        if cum[s + t] > u or t == n - 1:
            return s + t
    return s + n - 1


@njit(cache=True)
def _charge(l, rc, lev, S, nto, fa, ncall, top, cs, cn, cpar, ckey, cown, paid_row, freebuf):
    if rc == 0: return 0.0
    if rc == 1: return lev * S[l]
    if rc == 2: return lev * nto[l]
    if rc == 3: return lev * fa[l]
    if rc == 5: return lev * ncall[l]
    # B: the island ledger
    charge = S[l] - top[l]
    c0 = cs[l]
    for q in range(cn[l]):
        c = c0 + q
        p = cpar[c]
        if p >= 0 and freebuf[p]:
            freebuf[q] = True
            continue
        k = ckey[c]
        if paid_row[k]:
            freebuf[q] = True
            continue
        freebuf[q] = False
        charge += cown[c]
        paid_row[k] = True
    return lev * charge


@njit(cache=True)
def _reject(fit_row, mxref, w, N):
    """Parent index with probability proportional to exp(w * fit): rejection sampling against the reference mxref (an upper
    bound of the row, so the acceptance probability exp(w (f - mxref)) <= 1); exact."""
    for t in range(2000):
        j = np.random.randint(N)
        if np.random.random() < np.exp(w * (fit_row[j] - mxref)):
            return j
    tot = 0.0
    for j in range(N): tot += np.exp(w * (fit_row[j] - mxref))
    u = np.random.random() * tot
    acc = 0.0
    for j in range(N):
        acc += np.exp(w * (fit_row[j] - mxref))
        if u <= acc: return j
    return N - 1


@njit(cache=True)
def _cpick(cum, u, n):
    lo = 0; hi = n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if cum[mid] > u: hi = mid
        else: lo = mid + 1
    return lo


@njit(cache=True)
def lottery_rps_sampled(cum, ps, pn, out, S, nto, fa, ncall, top, cs, cn, cpar, ckey, cown, u, rc, lev, warm, nkeys, init,
                        N, w, m, seed, cps, nenc):
    np.random.seed(seed)
    I, n = init.shape
    cls = np.zeros((I, N), np.int64)
    for i in range(I):
        k = 0
        for a in range(n):
            for t in range(init[i, a]):
                cls[i, k] = a; k += 1
    fit = np.zeros((I, N))
    paid = np.zeros((I, nkeys), np.bool_)
    if warm == 1:
        for i in range(I):
            for k in range(nkeys): paid[i, k] = True
    freebuf = np.zeros(256, np.bool_)
    outc = np.zeros((len(cps), I, n), np.int64)
    cumw = np.zeros(N)
    mxi = np.zeros(I)
    ci = 0
    gens = cps[len(cps) - 1]
    for g in range(gens):
        for i in range(I):
            for j in range(N):
                a = cls[i, j]
                s = 0.0
                for e in range(nenc):
                    o = np.random.randint(N - 1)
                    if o >= j: o += 1
                    b = cls[i, o]
                    l1 = _pick(cum, ps, pn, a, b)
                    l2 = _pick(cum, ps, pn, b, a)
                    s += u[out[l1], out[l2]] - _charge(l1, rc, lev, S, nto, fa, ncall, top, cs, cn, cpar, ckey, cown, paid[i], freebuf)
                fit[i, j] = s / nenc
        for i in range(I):
            mx = -1e300
            for j in range(N):
                if fit[i, j] > mx: mx = fit[i, j]
            mxi[i] = mx
        for e in range(I * N):
            i = np.random.randint(I)
            src = i
            if m > 0.0 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            par = _reject(fit[src], mxi[src], w, N)
            vic = np.random.randint(N)
            cls[i, vic] = cls[src, par]; fit[i, vic] = fit[src, par]
            if fit[src, par] > mxi[i]: mxi[i] = fit[src, par]
        gg = g + 1
        while ci < len(cps) and gg == cps[ci]:
            for i in range(I):
                for j in range(N):
                    outc[ci, i, cls[i, j]] += 1
            ci += 1
    return outc


@njit(cache=True)
def lottery_insp_sampled_p(cum0, ps0, pn0, out0, S0, nto0, fa0, ncall0, top0, cs0, cn0, cpar0, ckey0, cown0,
                           cum1, ps1, pn1, out1, S1, nto1, fa1, ncall1, top1, cs1, cn1, cpar1, ckey1, cown1,
                           V0, V1, rc, lev, warm, nkeys, init0, init1, N, w, m, seed, cps, nenc):
    np.random.seed(seed)
    I, n0 = init0.shape
    n1 = init1.shape[1]
    cl0 = np.zeros((I, N), np.int64); cl1 = np.zeros((I, N), np.int64)
    for i in range(I):
        k = 0
        for a in range(n0):
            for t in range(init0[i, a]):
                cl0[i, k] = a; k += 1
        k = 0
        for b in range(n1):
            for t in range(init1[i, b]):
                cl1[i, k] = b; k += 1
    fit0 = np.zeros((I, N)); fit1 = np.zeros((I, N))
    paid = np.zeros((I, nkeys), np.bool_)
    if warm == 1:
        for i in range(I):
            for k in range(nkeys): paid[i, k] = True
    freebuf = np.zeros(256, np.bool_)
    o0 = np.zeros((len(cps), I, n0), np.int64); o1 = np.zeros((len(cps), I, n1), np.int64)
    mx0 = np.zeros(I); mx1 = np.zeros(I)
    ci = 0
    gens = cps[len(cps) - 1]
    for g in range(gens):
        for i in range(I):
            for j in range(N):
                a = cl0[i, j]
                s = 0.0
                for e in range(nenc):
                    o = np.random.randint(N)
                    b = cl1[i, o]
                    l0 = _pick(cum0, ps0, pn0, a, b)
                    l1 = _pick(cum1, ps1, pn1, b, a)
                    s += V0[out0[l0], out1[l1]] - _charge(l0, rc, lev, S0, nto0, fa0, ncall0, top0, cs0, cn0, cpar0, ckey0, cown0, paid[i], freebuf)
                fit0[i, j] = s / nenc
            for j in range(N):
                b = cl1[i, j]
                s = 0.0
                for e in range(nenc):
                    o = np.random.randint(N)
                    a = cl0[i, o]
                    l0 = _pick(cum0, ps0, pn0, a, b)
                    l1 = _pick(cum1, ps1, pn1, b, a)
                    s += V1[out0[l0], out1[l1]] - _charge(l1, rc, lev, S1, nto1, fa1, ncall1, top1, cs1, cn1, cpar1, ckey1, cown1, paid[i], freebuf)
                fit1[i, j] = s / nenc
        for i in range(I):
            mx = -1e300
            for j in range(N):
                if fit0[i, j] > mx: mx = fit0[i, j]
            mx0[i] = mx
            mx = -1e300
            for j in range(N):
                if fit1[i, j] > mx: mx = fit1[i, j]
            mx1[i] = mx
        for e in range(2 * I * N):
            i = np.random.randint(I); p = np.random.randint(2)
            src = i
            if m > 0.0 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            if p == 0:
                par = _reject(fit0[src], mx0[src], w, N)
                vic = np.random.randint(N)
                cl0[i, vic] = cl0[src, par]; fit0[i, vic] = fit0[src, par]
                if fit0[src, par] > mx0[i]: mx0[i] = fit0[src, par]
            else:
                par = _reject(fit1[src], mx1[src], w, N)
                vic = np.random.randint(N)
                cl1[i, vic] = cl1[src, par]; fit1[i, vic] = fit1[src, par]
                if fit1[src, par] > mx1[i]: mx1[i] = fit1[src, par]
        gg = g + 1
        while ci < len(cps) and gg == cps[ci]:
            for i in range(I):
                for j in range(N):
                    o0[ci, i, cl0[i, j]] += 1; o1[ci, i, cl1[i, j]] += 1
            ci += 1
    return o0, o1


def lottery_sampled(base, tb, sd, rule, level, cell, run, N, I, label, mN=1.0, warm=0):
    import lt_tape_run as R
    rc = RC[rule]
    seed_d = RP.run_seed('sampled|%s|%s|%s|%s|%d' % (cell, tb.game, tb.arm, label, tb.K), run)
    nk = sd.nkeys
    if base.game == 'rps':
        init, = tb.founders(cell, run, N, I)
        idx = np.nonzero(init.sum(0) > 0)[0]
        # the flat arrays are indexed by the full catalogue: use all classes, init padded
        f = sd.f0
        out = lottery_rps_sampled(f.cum, f.ps, f.pn, f.out, f.S, f.nto, f.fa, f.ncall, f.top, f.cs, f.cn, f.cpar, f.ckey, f.cown,
                                  sd.u, rc, float(level), warm, nk, np.ascontiguousarray(init), N, RP.W, mN / N, seed_d, CPS_S, NENC)
        full = {int(g): out[ci].copy() for ci, g in enumerate(CPS_S)}
        return full, {}
    init0, init1 = tb.founders(cell, run, N, I)
    f0, f1 = sd.f0, sd.f1
    o0, o1 = lottery_insp_sampled_p(f0.cum, f0.ps, f0.pn, f0.out, f0.S, f0.nto, f0.fa, f0.ncall, f0.top, f0.cs, f0.cn, f0.cpar, f0.ckey, f0.cown,
                                    f1.cum, f1.ps, f1.pn, f1.out, f1.S, f1.nto, f1.fa, f1.ncall, f1.top, f1.cs, f1.cn, f1.cpar, f1.ckey, f1.cown,
                                    sd.V0, sd.V1, rc, float(level), warm, nk, np.ascontiguousarray(init0), np.ascontiguousarray(init1),
                                    N, M2.W, mN / N, seed_d, CPS_S, NENC)
    full = {int(g): (o0[ci].copy(), o1[ci].copy()) for ci, g in enumerate(CPS_S)}
    return full, {}
