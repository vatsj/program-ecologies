"""Annealed re-injection kernel (notes/annealed.md §1.3): a copy of removing-rivals' rain kernel
(src/removing_rivals_kern.py, itself provenance's `segment` with rain and lineages; both unchanged there) with
  - a time-dependent rate: the per-Moran-event fresh-founder probability of generation g is epsg[g] (0 beyond the
    array), instead of one eps per segment;
  - paired founder streams (pairmode = 1): the n-th fresh founder on island i takes its spelling from the
    counter-based draw ru(fseed, i * 2^24 + n, 6), so schedules that differ only in timing see the same founders in the
    same order on each island; pairmode = 0 keeps removing-rivals' event-indexed draw ru(seed, ev, 6) (validation).
The production rate r is a parameter of the kernel already (this run fixes r = 100).  With epsg all zero and track = 0
the function is removing-rivals' and the scaling kernel draw for draw.
"""
import os
import sys

import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
from provenance import (ri, ru, side, plog_close, plog_open, is_settled, _change, pay, make_type, relation, NRULE, C_CHANGE,
                        C_IDENT_ENTRY, C_SPOU_ENTRY, C_BIRTH, R_SDEL)

@njit(cache=True)
def segment_ann(g0, gens, seed, N, w, m, r, slots, counts, paysum, pres, npres, pos, spcount, d, tunit, trule, tsp, tanc,
            ntv, utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, A, selfa, OSV, SPO, capable, COSTS,
            ctr, steps_rule, wn, wenc, wsp, wcode, wsid, ckey, cval, ncache, plog, hist_wait, hist_acq, hist_steps,
            hist_cens, nprod, identu, spou, tset, uns, rulecount, enc_exp, skip, FUT, fcount, enc_futile, err,
                 epsg, pairmode, fseed, cumL, spE, rain_rule, track, lin, nlin, fr, frf, nfr, rcount):
    """(Rain and lineages: see the module docstring.)  Generations g0 .. g0 + gens - 1 (I*N Moran events each, r encounters per event).  An encounter on an island
    whose residents are all *settled* (H, or holding a C and a D entry under a lack rule) changes nothing and is
    skipped (its draws are event-indexed, so skipping consumes nothing); enc_exp accumulates the expected
    side-encounters per rule (the per-match denominator)."""
    I = slots.shape[0]
    KCAP = tunit.shape[0]
    fs = np.empty(N)
    stv = np.zeros(1)
    tot_ind = float(I * N)
    neg = epsg.shape[0]
    for g in range(g0, g0 + gens):
        eps = epsg[g] if g < neg else 0.0
        for e in range(I * N):
            ev = g * I * N + e
            for rr in range(NRULE):
                if rulecount[rr] > 0:
                    enc_exp[rr] += 2.0 * r * rulecount[rr] / tot_ind
                if fcount[rr] > 0:
                    enc_futile[rr] += 2.0 * r * fcount[rr] / tot_ind
            for q in range(r):
                b0 = 8 + 5 * q
                i = ri(seed, ev, b0, I)
                if skip and uns[i] == 0:
                    continue
                f = ri(seed, ev, b0 + 1, N)
                p = ri(seed, ev, b0 + 2, N - 1)
                if p >= f: p += 1
                kf = slots[i, f]; kp = slots[i, p]
                if skip and is_settled(kf, tunit, trule, tset, BLC, BLD, PD, utau, FUT) and \
                        is_settled(kp, tunit, trule, tset, BLC, BLD, PD, utau, FUT):
                    continue
                rel = relation(kf, kp, tunit, tsp)
                shf = -1; shp = -1
                if trule[kf] == R_SDEL:
                    s1 = ri(seed, ev, b0 + 3, N - 1)
                    if s1 >= f: s1 += 1
                    shf = tsp[slots[i, s1]]
                if trule[kp] == R_SDEL:
                    s2 = ri(seed, ev, b0 + 4, N - 1)
                    if s2 >= p: s2 += 1
                    shp = tsp[slots[i, s2]]
                # first encounter of a producer: near-monoclonal in its spelling?
                if plog[i, f, 0] >= 0 and plog[i, f, 4] < 0:
                    plog[i, f, 4] = 1 if (spcount[i, tsp[kf]] - 1) >= 0.9 * (N - 1) else 0
                if plog[i, p, 0] >= 0 and plog[i, p, 4] < 0:
                    plog[i, p, 4] = 1 if (spcount[i, tsp[kp]] - 1) >= 0.9 * (N - 1) else 0
                nf = side(i, f, kf, kp, rel, shf, d, tunit, trule, tsp, tanc, ntv, KCAP, utau, BLC, BLD, SINGLE, APP,
                          PRODC, PD, KIND, NAT, CHC, CHD, UVt, OSV, SPO, COSTS, ctr, steps_rule, wn, wenc, wsp, wcode,
                          wsid, ckey, cval, ncache, plog, stv, err)
                if err[0] != 0: return g
                np_ = side(i, p, kp, kf, rel, shp, d, tunit, trule, tsp, tanc, ntv, KCAP, utau, BLC, BLD, SINGLE, APP,
                           PRODC, PD, KIND, NAT, CHC, CHD, UVt, OSV, SPO, COSTS, ctr, steps_rule, wn, wenc, wsp, wcode,
                           wsid, ckey, cval, ncache, plog, stv, err)
                if err[0] != 0: return g
                if nf != kf:
                    slots[i, f] = nf; ctr[trule[kf], C_CHANGE] += 1
                    if BLC[tunit[nf], 0] >= 0 and BLC[tunit[kf], 0] < 0:
                        plog_close(i, f, kf, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq, hist_steps,
                                   hist_cens, nprod, 0)
                    if identu[tunit[nf]] and not identu[tunit[kf]]: ctr[trule[kf], C_IDENT_ENTRY] += 1
                    if spou[tunit[nf]] and not spou[tunit[kf]]: ctr[trule[kf], C_SPOU_ENTRY] += 1
                    uns[i] += (0 if is_settled(nf, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1) - \
                        (0 if is_settled(kf, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1)
                    fcount[trule[kf]] += (1 if tset[nf] == 2 else 0) - (1 if tset[kf] == 2 else 0)
                    _change(i, kf, nf, counts, paysum, pres, npres, pos, tunit, tsp, A, selfa)
                if np_ != kp:
                    slots[i, p] = np_; ctr[trule[kp], C_CHANGE] += 1
                    if BLC[tunit[np_], 0] >= 0 and BLC[tunit[kp], 0] < 0:
                        plog_close(i, p, kp, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq, hist_steps,
                                   hist_cens, nprod, 0)
                    if identu[tunit[np_]] and not identu[tunit[kp]]: ctr[trule[kp], C_IDENT_ENTRY] += 1
                    if spou[tunit[np_]] and not spou[tunit[kp]]: ctr[trule[kp], C_SPOU_ENTRY] += 1
                    uns[i] += (0 if is_settled(np_, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1) - \
                        (0 if is_settled(kp, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1)
                    fcount[trule[kp]] += (1 if tset[np_] == 2 else 0) - (1 if tset[kp] == 2 else 0)
                    _change(i, kp, np_, counts, paysum, pres, npres, pos, tunit, tsp, A, selfa)
            # birth-death (milestone 2's), event-indexed draws 0-4
            i = ri(seed, ev, 0, I)
            src = i
            if m > 0.0 and I > 1 and ru(seed, ev, 1) < m:
                src = ri(seed, ev, 2, I - 1)
                if src >= i: src += 1
            nps = npres[src]
            mx = -1e300
            for tt in range(nps):
                kk = pres[src, tt]
                fv = (paysum[src, kk] - pay(kk, kk, tunit, tsp, A, selfa)) / (N - 1)
                fs[tt] = fv
                if fv > mx: mx = fv
            tot = 0.0
            for tt in range(nps):
                tot += counts[src, pres[src, tt]] * np.exp(w * (fs[tt] - mx))
            uu = ru(seed, ev, 3) * tot
            acc = 0.0
            child = pres[src, nps - 1]
            for tt in range(nps):
                kk = pres[src, tt]
                acc += counts[src, kk] * np.exp(w * (fs[tt] - mx))
                if uu <= acc:
                    child = kk
                    break
            vs = ri(seed, ev, 4, N)
            kv = slots[i, vs]
            if eps > 0.0 and ru(seed, ev, 5) < eps:
                # a fresh founder from L (draw 6), empty lists
                nL = cumL.shape[0]
                if pairmode == 1:
                    u6 = ru(fseed, i * 16777216 + rcount[i], 6) * cumL[nL - 1]
                else:
                    u6 = ru(seed, ev, 6) * cumL[nL - 1]
                lo = 0; hi = nL - 1
                while lo < hi:
                    mid = (lo + hi) // 2
                    if cumL[mid] > u6: hi = mid
                    else: lo = mid + 1
                s = lo
                nt = ntv[0]
                if nt >= KCAP - 2:
                    err[0] = 2
                    return g
                child, nt2 = make_type(d, tunit, trule, tsp, tanc, nt, spE[s], rain_rule, s, 0)
                ntv[0] = nt2
                rcount[i] += 1
                if track:
                    nlin[0] += 1
                    lid = nlin[0]
                    if nfr[0] < fr.shape[0]:
                        q = nfr[0]
                        best = -1; bn = -1
                        fnew = 0.0; fm = 0.0
                        for tt in range(npres[i]):
                            kk = pres[i, tt]
                            if counts[i, kk] > bn:
                                bn = counts[i, kk]; best = kk
                            fnew += counts[i, kk] * pay(child, kk, tunit, tsp, A, selfa)
                            fm += counts[i, kk] * (paysum[i, kk] - pay(kk, kk, tunit, tsp, A, selfa)) / (N - 1)
                        fnew = (fnew - pay(child, kv, tunit, tsp, A, selfa)) / (N - 1)
                        fr[q, 0] = g; fr[q, 1] = i; fr[q, 2] = s; fr[q, 3] = best; fr[q, 4] = lid
                        frf[q, 0] = bn / N; frf[q, 1] = fnew; frf[q, 2] = fm / N
                        nfr[0] = q + 1
                    lin[i, vs] = lid
            elif track:
                # the newborn's lineage: a parent individual of the chosen type on the source island (draw 7)
                mc = counts[src, child]
                pick = ri(seed, ev, 7, mc)
                c = 0
                for jj in range(N):
                    if slots[src, jj] == child:
                        if c == pick:
                            lin[i, vs] = lin[src, jj]
                            break
                        c += 1
            ctr[trule[child], C_BIRTH] += 1
            # the victim's mutable state ends with it
            plog_close(i, vs, kv, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq, hist_steps, hist_cens,
                       nprod, 1)
            wn[i, vs] = 0; wenc[i, vs] = 0; ncache[i, vs] = 0
            plog_open(i, vs, child, tunit, trule, BLC, plog)
            spcount[i, tsp[kv]] -= 1
            spcount[i, tsp[child]] += 1
            rulecount[trule[kv]] -= 1
            rulecount[trule[child]] += 1
            if kv == child: continue
            uns[i] += (0 if is_settled(child, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1) - \
                (0 if is_settled(kv, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1)
            fcount[trule[child]] += 1 if tset[child] == 2 else 0
            fcount[trule[kv]] -= 1 if tset[kv] == 2 else 0
            slots[i, vs] = child
            _change(i, kv, child, counts, paysum, pres, npres, pos, tunit, tsp, A, selfa)
    return g0 + gens


