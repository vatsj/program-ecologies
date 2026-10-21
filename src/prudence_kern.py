"""The post-merge arrival kernel for the prudence run (notes/prudence.md §1.1, §1.3).

`segment_pru` is the Pangaea island kernel (`src/pangaea_kern.py::segment`, itself provenance's) with the annealed run's
fresh-founder arrivals (`src/annealed_kern.py::segment_ann`) added at the birth step, and three changes:

1. a per-generation arrival probability epsg[g] per Moran event (0 beyond the array); with epsg = 0 and track = 0 the
   function is the Pangaea kernel draw for draw (the copier no-change cache of the Pangaea kernel is dropped: it is
   used only in the C-donor cells);
2. paired arrival spellings: the n-th arrival on island i draws its spelling from the counter stream
   ru(fseed, i 2^24 + n, 6), mapped through the cumulative prior cumL (which may be a depleted prior: removed spellings
   have flat increments and are never selected);
3. lineage tracking by rejection sampling: the newborn's parent individual is drawn uniformly from the individuals of
   the chosen type by redrawing an index from a separate counter stream (lseed) until it hits the type, so a birth
   costs about N / (count of the chosen type) draws and not O(N) (the annealed kernel's scan costs O(N) per birth, too
   slow at N = 12,800); the arrival log has six columns: generation, island, spelling, the victim's type, lineage id and
   the island's majority type at arrival.  No draw of the dynamics is consumed by the lineage bookkeeping.
"""
import os
import sys

import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV

QBLOCK = 100


@njit(cache=True)
def block_seed(seed, blk):
    """Seed of encounter block blk >= 1 (an independent counter stream)."""
    z = PV.mix64(np.uint64(seed) ^ (np.uint64(blk) * np.uint64(0xD1B54A32D192ED03) + np.uint64(0x632BE59BD9B4E019)))
    return int(z >> np.uint64(2))


@njit(cache=True)
def segment_pru(g0, gens, seed, N, w, m, r, slots, counts, paysum, pres, npres, pos, spcount, d, tunit, trule, tsp, tanc,
            ntv, utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, A, selfa, OSV, SPO, capable, COSTS,
            ctr, steps_rule, wn, wenc, wsp, wcode, wsid, ckey, cval, ncache, plog, hist_wait, hist_acq, hist_steps,
            hist_cens, nprod, identu, spou, tset, uns, rulecount, enc_exp, skip, FUT, fcount, enc_futile, err,
            epsg, fseed, lseed, cumL, spE, rain_rule, track, lin, nlin, fr, frf, nfr, rcount):
    """See the module docstring."""
    I = slots.shape[0]
    KCAP = tunit.shape[0]
    fs = np.empty(N)
    ex = np.empty(N)
    stv = np.zeros(1)
    tot_ind = float(I * N)
    nblk = (r + QBLOCK - 1) // QBLOCK
    bseeds = np.empty(max(nblk, 1), np.int64)
    bseeds[0] = seed
    for b in range(1, nblk):
        bseeds[b] = block_seed(seed, b)
    neg = epsg.shape[0]
    for g in range(g0, g0 + gens):
        eps = epsg[g] if g < neg else 0.0
        for e in range(I * N):
            ev = g * I * N + e
            for rr in range(PV.NRULE):
                if rulecount[rr] > 0:
                    enc_exp[rr] += 2.0 * r * rulecount[rr] / tot_ind
                if fcount[rr] > 0:
                    enc_futile[rr] += 2.0 * r * fcount[rr] / tot_ind
            for q in range(r):
                sq = bseeds[q // QBLOCK]
                b0 = 8 + 5 * (q % QBLOCK)
                i = PV.ri(sq, ev, b0, I)
                if skip and uns[i] == 0:
                    continue
                f = PV.ri(sq, ev, b0 + 1, N)
                p = PV.ri(sq, ev, b0 + 2, N - 1)
                if p >= f: p += 1
                kf = slots[i, f]; kp = slots[i, p]
                if skip and PV.is_settled(kf, tunit, trule, tset, BLC, BLD, PD, utau, FUT) and \
                        PV.is_settled(kp, tunit, trule, tset, BLC, BLD, PD, utau, FUT):
                    continue
                rel = PV.relation(kf, kp, tunit, tsp)
                shf = -1; shp = -1
                if trule[kf] == PV.R_SDEL:
                    s1 = PV.ri(sq, ev, b0 + 3, N - 1)
                    if s1 >= f: s1 += 1
                    shf = tsp[slots[i, s1]]
                if trule[kp] == PV.R_SDEL:
                    s2 = PV.ri(sq, ev, b0 + 4, N - 1)
                    if s2 >= p: s2 += 1
                    shp = tsp[slots[i, s2]]
                if plog[i, f, 0] >= 0 and plog[i, f, 4] < 0:
                    plog[i, f, 4] = 1 if (spcount[i, tsp[kf]] - 1) >= 0.9 * (N - 1) else 0
                if plog[i, p, 0] >= 0 and plog[i, p, 4] < 0:
                    plog[i, p, 4] = 1 if (spcount[i, tsp[kp]] - 1) >= 0.9 * (N - 1) else 0
                nf = PV.side(i, f, kf, kp, rel, shf, d, tunit, trule, tsp, tanc, ntv, KCAP, utau, BLC, BLD, SINGLE,
                             APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, OSV, SPO, COSTS, ctr, steps_rule, wn, wenc,
                             wsp, wcode, wsid, ckey, cval, ncache, plog, stv, err)
                if err[0] != 0: return g
                np_ = PV.side(i, p, kp, kf, rel, shp, d, tunit, trule, tsp, tanc, ntv, KCAP, utau, BLC, BLD, SINGLE,
                              APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, OSV, SPO, COSTS, ctr, steps_rule, wn, wenc,
                              wsp, wcode, wsid, ckey, cval, ncache, plog, stv, err)
                if err[0] != 0: return g
                if nf != kf:
                    slots[i, f] = nf; ctr[trule[kf], PV.C_CHANGE] += 1
                    if BLC[tunit[nf], 0] >= 0 and BLC[tunit[kf], 0] < 0:
                        PV.plog_close(i, f, kf, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq,
                                      hist_steps, hist_cens, nprod, 0)
                    if identu[tunit[nf]] and not identu[tunit[kf]]: ctr[trule[kf], PV.C_IDENT_ENTRY] += 1
                    if spou[tunit[nf]] and not spou[tunit[kf]]: ctr[trule[kf], PV.C_SPOU_ENTRY] += 1
                    uns[i] += (0 if PV.is_settled(nf, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1) - \
                        (0 if PV.is_settled(kf, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1)
                    fcount[trule[kf]] += (1 if tset[nf] == 2 else 0) - (1 if tset[kf] == 2 else 0)
                    PV._change(i, kf, nf, counts, paysum, pres, npres, pos, tunit, tsp, A, selfa)
                if np_ != kp:
                    slots[i, p] = np_; ctr[trule[kp], PV.C_CHANGE] += 1
                    if BLC[tunit[np_], 0] >= 0 and BLC[tunit[kp], 0] < 0:
                        PV.plog_close(i, p, kp, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq,
                                      hist_steps, hist_cens, nprod, 0)
                    if identu[tunit[np_]] and not identu[tunit[kp]]: ctr[trule[kp], PV.C_IDENT_ENTRY] += 1
                    if spou[tunit[np_]] and not spou[tunit[kp]]: ctr[trule[kp], PV.C_SPOU_ENTRY] += 1
                    uns[i] += (0 if PV.is_settled(np_, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1) - \
                        (0 if PV.is_settled(kp, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1)
                    fcount[trule[kp]] += (1 if tset[np_] == 2 else 0) - (1 if tset[kp] == 2 else 0)
                    PV._change(i, kp, np_, counts, paysum, pres, npres, pos, tunit, tsp, A, selfa)
            # birth-death (provenance's), event-indexed draws 0-4 of the run seed
            i = PV.ri(seed, ev, 0, I)
            src = i
            if m > 0.0 and I > 1 and PV.ru(seed, ev, 1) < m:
                src = PV.ri(seed, ev, 2, I - 1)
                if src >= i: src += 1
            nps = npres[src]
            mx = -1e300
            for tt in range(nps):
                kk = pres[src, tt]
                fv = (paysum[src, kk] - PV.pay(kk, kk, tunit, tsp, A, selfa)) / (N - 1)
                fs[tt] = fv
                if fv > mx: mx = fv
            tot = 0.0
            for tt in range(nps):
                ex[tt] = np.exp(w * (fs[tt] - mx))
                tot += counts[src, pres[src, tt]] * ex[tt]
            uu = PV.ru(seed, ev, 3) * tot
            acc = 0.0
            child = pres[src, nps - 1]
            for tt in range(nps):
                kk = pres[src, tt]
                acc += counts[src, kk] * ex[tt]
                if uu <= acc:
                    child = kk
                    break
            vs = PV.ri(seed, ev, 4, N)
            kv = slots[i, vs]
            if eps > 0.0 and PV.ru(seed, ev, 5) < eps:
                # a fresh founder from the (possibly depleted) prior: the n-th arrival on island i draws u6 from the
                # counter stream of fseed (paired across schedules and worlds); empty lists, rule rain_rule
                nL = cumL.shape[0]
                u6 = PV.ru(fseed, i * 16777216 + rcount[i], 6) * cumL[nL - 1]
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
                child, nt2 = PV.make_type(d, tunit, trule, tsp, tanc, nt, spE[s], rain_rule, s, 0)
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
                            fnew += counts[i, kk] * PV.pay(child, kk, tunit, tsp, A, selfa)
                            fm += counts[i, kk] * (paysum[i, kk] - PV.pay(kk, kk, tunit, tsp, A, selfa)) / (N - 1)
                        fnew = (fnew - PV.pay(child, kv, tunit, tsp, A, selfa)) / (N - 1)
                        fr[q, 0] = g; fr[q, 1] = i; fr[q, 2] = s; fr[q, 3] = kv; fr[q, 4] = lid; fr[q, 5] = best
                        frf[q, 0] = bn / N; frf[q, 1] = fnew; frf[q, 2] = fm / N
                        nfr[0] = q + 1
                    lin[i, vs] = lid
            elif track:
                # the newborn inherits the lineage of a uniformly chosen parent individual of the chosen type on the
                # source island: rejection sampling over individual indices (expected N / counts[child] tries) from a
                # separate counter stream (these draws feed no dynamics), with a scan fallback
                mc = counts[src, child]
                par = -1
                for t in range(200):
                    j2 = PV.ri(lseed, ev, t, N)
                    if slots[src, j2] == child:
                        par = j2
                        break
                if par < 0:
                    pick = PV.ri(lseed, ev, 201, mc)
                    c = 0
                    for jj in range(N):
                        if slots[src, jj] == child:
                            if c == pick:
                                par = jj
                                break
                            c += 1
                lin[i, vs] = lin[src, par]
            ctr[trule[child], PV.C_BIRTH] += 1
            PV.plog_close(i, vs, kv, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq, hist_steps,
                          hist_cens, nprod, 1)
            wn[i, vs] = 0; wenc[i, vs] = 0; ncache[i, vs] = 0
            PV.plog_open(i, vs, child, tunit, trule, BLC, plog)
            spcount[i, tsp[kv]] -= 1
            spcount[i, tsp[child]] += 1
            rulecount[trule[kv]] -= 1
            rulecount[trule[child]] += 1
            if kv == child: continue
            uns[i] += (0 if PV.is_settled(child, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1) - \
                (0 if PV.is_settled(kv, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1)
            fcount[trule[child]] += 1 if tset[child] == 2 else 0
            fcount[trule[kv]] -= 1 if tset[kv] == 2 else 0
            slots[i, vs] = child
            PV._change(i, kv, child, counts, paysum, pres, npres, pos, tunit, tsp, A, selfa)
    return g0 + gens
