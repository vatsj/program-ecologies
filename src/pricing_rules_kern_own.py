"""GENERATED from pricing_rules_kern.py by a text transformation (notes/pricing-rules.md section 2): the sampled-encounter
lotteries of rule B with a `mode`: 0 = the island ledger (draw for draw with pricing_rules_kern for the same seed: no extra random
numbers), 1 = B-own, a per-program memo (a bit-row per individual, empty for founders, copied to offspring, carried by migrants),
and counters of payments (insertions) and of memo / ledger sizes at the checkpoints.  Do not edit by hand."""
import os
import sys

import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pricing_rules_kern import _pick, _reject, _cpick


@njit(cache=True)
def _charge_c(l, rc, lev, S, nto, fa, ncall, top, cs, cn, cpar, ckey, cown, paid_row, freebuf, cnt):
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
        cnt[0] += 1
    return lev * charge


@njit(cache=True)
def lottery_rps_own(cum, ps, pn, out, S, nto, fa, ncall, top, cs, cn, cpar, ckey, cown, u, rc, lev, warm, nkeys, init,
                        N, w, m, seed, cps, nenc, mode):
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
    memo = np.zeros((I, N, nkeys), np.bool_) if mode == 1 else np.zeros((1, 1, 1), np.bool_)
    cnt = np.zeros(1, np.int64)
    msz = np.zeros((len(cps), 2))
    if warm == 1:
        for i in range(I):
            for k in range(nkeys): paid[i, k] = True
            if mode == 1:
                for j in range(N):
                    for k in range(nkeys): memo[i, j, k] = True
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
                    s += u[out[l1], out[l2]] - _charge_c(l1, rc, lev, S, nto, fa, ncall, top, cs, cn, cpar, ckey, cown, memo[i, j] if mode == 1 else paid[i], freebuf, cnt)
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
            if mode == 1:
                for k in range(nkeys): memo[i, vic, k] = memo[src, par, k]
            if fit[src, par] > mxi[i]: mxi[i] = fit[src, par]
        gg = g + 1
        while ci < len(cps) and gg == cps[ci]:
            for i in range(I):
                for j in range(N):
                    outc[ci, i, cls[i, j]] += 1
            tot = 0.0; mxs = 0.0
            if mode == 1:
                for i in range(I):
                    for j in range(N):
                        s = 0.0
                        for k in range(nkeys):
                            if memo[i, j, k]: s += 1.0
                        tot += s
                        if s > mxs: mxs = s
                msz[ci, 0] = tot / (I * N)
            else:
                for i in range(I):
                    s = 0.0
                    for k in range(nkeys):
                        if paid[i, k]: s += 1.0
                    tot += s
                    if s > mxs: mxs = s
                msz[ci, 0] = tot / I
            msz[ci, 1] = mxs
            ci += 1
    return outc, msz, cnt


@njit(cache=True)
def lottery_insp_own(cum0, ps0, pn0, out0, S0, nto0, fa0, ncall0, top0, cs0, cn0, cpar0, ckey0, cown0,
                           cum1, ps1, pn1, out1, S1, nto1, fa1, ncall1, top1, cs1, cn1, cpar1, ckey1, cown1,
                           V0, V1, rc, lev, warm, nkeys, init0, init1, N, w, m, seed, cps, nenc, mode):
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
    memo0 = np.zeros((I, N, nkeys), np.bool_) if mode == 1 else np.zeros((1, 1, 1), np.bool_)
    memo1 = np.zeros((I, N, nkeys), np.bool_) if mode == 1 else np.zeros((1, 1, 1), np.bool_)
    cnt = np.zeros(1, np.int64)
    msz = np.zeros((len(cps), 2))
    if warm == 1:
        for i in range(I):
            for k in range(nkeys): paid[i, k] = True
            if mode == 1:
                for j in range(N):
                    for k in range(nkeys):
                        memo0[i, j, k] = True; memo1[i, j, k] = True
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
                    s += V0[out0[l0], out1[l1]] - _charge_c(l0, rc, lev, S0, nto0, fa0, ncall0, top0, cs0, cn0, cpar0, ckey0, cown0, memo0[i, j] if mode == 1 else paid[i], freebuf, cnt)
                fit0[i, j] = s / nenc
            for j in range(N):
                b = cl1[i, j]
                s = 0.0
                for e in range(nenc):
                    o = np.random.randint(N)
                    a = cl0[i, o]
                    l0 = _pick(cum0, ps0, pn0, a, b)
                    l1 = _pick(cum1, ps1, pn1, b, a)
                    s += V1[out0[l0], out1[l1]] - _charge_c(l1, rc, lev, S1, nto1, fa1, ncall1, top1, cs1, cn1, cpar1, ckey1, cown1, memo1[i, j] if mode == 1 else paid[i], freebuf, cnt)
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
                if mode == 1:
                    for k in range(nkeys): memo0[i, vic, k] = memo0[src, par, k]
                if fit0[src, par] > mx0[i]: mx0[i] = fit0[src, par]
            else:
                par = _reject(fit1[src], mx1[src], w, N)
                vic = np.random.randint(N)
                cl1[i, vic] = cl1[src, par]; fit1[i, vic] = fit1[src, par]
                if mode == 1:
                    for k in range(nkeys): memo1[i, vic, k] = memo1[src, par, k]
                if fit1[src, par] > mx1[i]: mx1[i] = fit1[src, par]
        gg = g + 1
        while ci < len(cps) and gg == cps[ci]:
            for i in range(I):
                for j in range(N):
                    o0[ci, i, cl0[i, j]] += 1; o1[ci, i, cl1[i, j]] += 1
            tot = 0.0; mxs = 0.0
            if mode == 1:
                for i in range(I):
                    for j in range(N):
                        s = 0.0; s2 = 0.0
                        for k in range(nkeys):
                            if memo0[i, j, k]: s += 1.0
                            if memo1[i, j, k]: s2 += 1.0
                        tot += s + s2
                        if s > mxs: mxs = s
                        if s2 > mxs: mxs = s2
                msz[ci, 0] = tot / (2 * I * N)
            else:
                for i in range(I):
                    s = 0.0
                    for k in range(nkeys):
                        if paid[i, k]: s += 1.0
                    tot += s
                    if s > mxs: mxs = s
                msz[ci, 0] = tot / I
            msz[ci, 1] = mxs
            ci += 1
    return o0, o1, msz, cnt


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


def lottery_own(base, tb, sd, rule, level, cell, run, N, I, label, mN=1.0, warm=0):
    """Dispatcher: rule 'Bo' = B-own (mode 1), 'Bl' = the island ledger through this kernel (mode 0, logged).  Returns
    (full counts by checkpoint, extra statistics)."""
    import rps as RP
    import mixed2 as M2
    import pricing_rules_kern as KR
    mode = 1 if rule == 'Bo' else 0
    seed_d = RP.run_seed('sampled|%s|%s|%s|%s|%d' % (cell, tb.game, tb.arm, label, tb.K), run)
    nk = sd.nkeys
    if base.game == 'rps':
        init, = tb.founders(cell, run, N, I)
        f = sd.f0
        out, msz, cnt = lottery_rps_own(f.cum, f.ps, f.pn, f.out, f.S, f.nto, f.fa, f.ncall, f.top, f.cs, f.cn, f.cpar, f.ckey, f.cown,
                                        sd.u, 4, float(level), warm, nk, np.ascontiguousarray(init), N, RP.W, mN / N, seed_d,
                                        KR.CPS_S, KR.NENC, mode)
        full = {int(g): out[ci].copy() for ci, g in enumerate(KR.CPS_S)}
        n_ind = I * N
    else:
        init0, init1 = tb.founders(cell, run, N, I)
        f0, f1 = sd.f0, sd.f1
        o0, o1, msz, cnt = lottery_insp_own(f0.cum, f0.ps, f0.pn, f0.out, f0.S, f0.nto, f0.fa, f0.ncall, f0.top, f0.cs, f0.cn, f0.cpar, f0.ckey, f0.cown,
                                            f1.cum, f1.ps, f1.pn, f1.out, f1.S, f1.nto, f1.fa, f1.ncall, f1.top, f1.cs, f1.cn, f1.cpar, f1.ckey, f1.cown,
                                            sd.V0, sd.V1, 4, float(level), warm, nk, np.ascontiguousarray(init0), np.ascontiguousarray(init1),
                                            N, M2.W, mN / N, seed_d, KR.CPS_S, KR.NENC, mode)
        full = {int(g): (o0[ci].copy(), o1[ci].copy()) for ci, g in enumerate(KR.CPS_S)}
        n_ind = 2 * I * N
    ex = dict(memo_mean=float(msz[-1, 0]), memo_max=float(msz[-1, 1]), payments=int(cnt[0]), payments_per_ind=float(cnt[0]) / n_ind,
              cert_invalidations=0, nkeys=int(nk))
    return full, ex
