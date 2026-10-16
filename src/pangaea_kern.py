"""The Pangaea run's island kernel (notes/pangaea.md §1.3): provenance's `segment`, copied, with two changes that do
not alter any trajectory provenance can produce.

1. Production encounters q >= 100 of a Moran event draw from a separate counter stream per block of 100 encounters
   (seed_b = mix of the run seed and the block index), so that r > 100 encounters per event never reuse the draws of
   the next event (provenance hashes (event, draw) as event*512 + draw; encounter q uses draws 8 + 5q .. 12 + 5q, which
   pass 511 at q = 101).  For r <= 100 the draws are provenance's, bit for bit.
2. The birth step stores exp(w (f - max)) per present type instead of computing it twice; the values and the order of
   summation are unchanged, so the chosen parent is identical.

Everything else (encounter procedure, settled skip, payoff bookkeeping, logs) is provenance's own functions.
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
def segment(g0, gens, seed, N, w, m, r, slots, counts, paysum, pres, npres, pos, spcount, d, tunit, trule, tsp, tanc,
            ntv, utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, A, selfa, OSV, SPO, capable, COSTS,
            ctr, steps_rule, wn, wenc, wsp, wcode, wsid, ckey, cval, ncache, plog, hist_wait, hist_acq, hist_steps,
            hist_cens, nprod, identu, spou, tset, uns, rulecount, enc_exp, skip, FUT, fcount, enc_futile, err):
    """Provenance's segment (same signature) with overlap-free encounter draws above r = 100."""
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
    for g in range(g0, g0 + gens):
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


@njit(cache=True)
def mutual_matrix(K, tunit, tsp, A, selfa):
    """M[a, b]: types K[a] and K[b] cooperate with each other (a == b: self-play)."""
    n = len(K)
    M = np.zeros((n, n), np.bool_)
    for a in range(n):
        for b in range(a, n):
            v = PV.cc_pair(K[a], K[b], tunit, tsp, A, selfa) > 0.5
            M[a, b] = v
            M[b, a] = v
    return M


@njit(cache=True)
def dominant_network(M, S, c, K):
    """Among cooperators S (indices into M), the one with the largest compatible mass (ties: larger count, lower type
    id), then a greedy clique over its mutual partners in decreasing count (ties: lower type id).  Returns the clique's
    indices into M."""
    n = len(S)
    best = -1
    bm = -1.0
    for a in range(n):
        s = 0.0
        for b in range(n):
            if M[S[a], S[b]]: s += c[S[b]]
        if best < 0 or s > bm or (s == bm and (c[S[a]] > c[S[best]] or (c[S[a]] == c[S[best]] and K[S[a]] < K[S[best]]))):
            best = a; bm = s
    cand = np.empty(n, np.int64)
    nc = 0
    for b in range(n):
        if b != best and M[S[best], S[b]]:
            cand[nc] = b; nc += 1
    # sort candidates by (-count, type id): insertion sort on a small key array
    keys = np.empty(nc)
    for z in range(nc):
        keys[z] = -c[S[cand[z]]] * 1e9 + K[S[cand[z]]] * 1e-6
    order = np.argsort(keys, kind='mergesort')
    net = np.empty(n, np.int64)
    nn = 0
    net[nn] = S[best]; nn += 1
    for z in range(nc):
        a = S[cand[order[z]]]
        ok = True
        for y in range(nn):
            if not M[a, net[y]]:
                ok = False
                break
        if ok:
            net[nn] = a; nn += 1
    return net[:nn]
