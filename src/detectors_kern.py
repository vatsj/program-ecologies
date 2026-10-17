"""The grudge kernel (notes/detectors.md §1.4): the annealed kernel (src/annealed_kern.py, itself provenance's `segment`
with rain; unchanged there) over *grudge types*.

A grudge type k is a base type kb = gbase[k] (provenance's (unit, rule, spelling, ancestry), created by provenance's
`side` and `make_type`) and a grudge list gid = gg[k] (interned: GS[gid, :GN[gid]] spelling ids, oldest first).
Individuals hold grudge types; counts, payoff sums and births are over grudge types.  The play of a pair is the base
table's unless a grudge bit is live (b_xy: y's spelling in x's list), in which case the exact pair tables AG1 (one bit)
/ AG2 (both bits) give both actions (host-computed with explicit keyed lists, src/detectors.py).

gmode: 0 no grudge rule (lists stay empty; the kernel is the annealed kernel draw for draw), 1 vertical, 2 vertical
and horizontal, 3 sham (written and inherited, ignored in play), 4 prewritten (no writing; the bits are the oracle
table PW: a writer holds a grudge against every unit that would exploit it).
"""
import os
import sys

import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(__file__))
import provenance as PV
from provenance import (ri, ru, side, plog_close, plog_open, is_settled, make_type, NRULE, C_CHANGE, C_IDENT_ENTRY,
                        C_SPOU_ENTRY, C_BIRTH, R_SDEL)

PAYM = PV.PAYM
G_OFF, G_VERT, G_HORIZ, G_SHAM, G_PRE = 0, 1, 2, 3, 4
GCAP_MAX = 4
# grudge counters
NGC = 16
(GC_WRITE, GC_EVICT, GC_ADOPT, GC_LIVE_ENC, GC_SUCKER_ENC, GC_ENC, GC_WRITE_SELFSKIP, GC_NOWRITER, GC_WFAIL,
 GC_SKIP_ISL, GC_RECOMP, GC_DIRTY, GC_BOOT, GC_PRED_MARKED, GC_PRED_UNMARKED, GC_SPARE) = range(NGC)


# ------------------------------------------------------------------------------------------------ grudge lists
@njit(cache=True)
def gkey(GS, GN, gid):
    h = np.uint64(1469598103934665603)
    for q in range(GN[gid]):
        h = (h ^ np.uint64(GS[gid, q] + 1)) * np.uint64(1099511628211)
    h = (h ^ np.uint64(GN[gid] + 7)) * np.uint64(1099511628211)
    return np.int64(h >> np.uint64(2))


@njit(cache=True)
def gintern(gdict, GS, GN, ngv, tmp, n):
    """The gid of the list tmp[:n] (interned).  ngv[0]: lists so far."""
    h = np.uint64(1469598103934665603)
    for q in range(n):
        h = (h ^ np.uint64(tmp[q] + 1)) * np.uint64(1099511628211)
    h = (h ^ np.uint64(n + 7)) * np.uint64(1099511628211)
    key = np.int64(h >> np.uint64(2))
    while key in gdict:
        g = gdict[key]
        same = GN[g] == n
        if same:
            for q in range(n):
                if GS[g, q] != tmp[q]:
                    same = False
                    break
        if same: return g
        key += 1
    g = ngv[0]
    if g >= GS.shape[0]:
        return -1
    for q in range(n): GS[g, q] = tmp[q]
    GN[g] = n
    gdict[key] = g
    ngv[0] = g + 1
    return g


@njit(cache=True)
def gholds(GS, GN, gid, s):
    for q in range(GN[gid]):
        if GS[gid, q] == s: return True
    return False


@njit(cache=True)
def gmake(gdict2, gbase, gg, ngt, kb, gid, freel, nfree):
    """The grudge type (kb, gid): an existing id, a recycled id (free list) or a new one; -1 if full."""
    code = kb * 1048576 + gid
    if code in gdict2:
        return gdict2[code]
    if nfree[0] > 0:
        k = freel[nfree[0] - 1]
        nfree[0] -= 1
    else:
        k = ngt[0]
        if k >= gbase.shape[0]:
            return -1
        ngt[0] = k + 1
    gbase[k] = kb; gg[k] = gid
    gdict2[code] = k
    return k


@njit(cache=True)
def gfree(k, gdict2, gbase, gg, freel, nfree):
    code = gbase[k] * 1048576 + gg[k]
    if code in gdict2 and gdict2[code] == k:
        gdict2.pop(code)
        freel[nfree[0]] = k
        nfree[0] += 1


@njit(cache=True)
def gdrop(k, gcount, gdict2, gbase, gg, freel, nfree):
    """Free a type made during an encounter and not placed."""
    if k >= 0 and gcount[k] == 0:
        gfree(k, gdict2, gbase, gg, freel, nfree)


# ------------------------------------------------------------------------------------------------ plays
@njit(cache=True)
def acts(k, j, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode):
    """(x's action against y, y's against x) for grudge types k, j (1 C, 0 D)."""
    kb = gbase[k]; jb = gbase[j]
    u = tunit[kb]; v = tunit[jb]
    sk = tsp[kb]; sj = tsp[jb]
    if u == v and sk == sj:
        a = np.int64(selfa[u])
        return a, a
    bkj = False; bjk = False
    if gmode == G_VERT or gmode == G_HORIZ:
        bkj = gholds(GS, GN, gg[k], sj)
        bjk = gholds(GS, GN, gg[j], sk)
    elif gmode == G_PRE:
        if widx[u] >= 0: bkj = PW[widx[u], v] == 1
        if widx[v] >= 0: bjk = PW[widx[v], u] == 1
    if bkj and widx[u] < 0: bkj = False
    if bjk and widx[v] < 0: bjk = False
    if bkj and bjk:
        c = AG2[widx[u], widx[v]]
        if c >= 0: return np.int64(c & 1), np.int64((c >> 1) & 1)
    elif bkj:
        c = AG1[widx[u], v]
        if c >= 0: return np.int64(c & 1), np.int64((c >> 1) & 1)
    elif bjk:
        c = AG1[widx[v], u]
        if c >= 0: return np.int64((c >> 1) & 1), np.int64(c & 1)
    return np.int64(A[u, v]), np.int64(A[v, u])


@njit(cache=True)
def gpay(k, j, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode):
    a, b = acts(k, j, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode)
    return PAYM[a, b]


@njit(cache=True)
def gcc(k, j, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode):
    a, b = acts(k, j, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode)
    return 1.0 if (a == 1 and b == 1) else 0.0


@njit(cache=True)
def gchange(i, a, b, counts, paysum, pres, npres, pos, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW,
            gmode, gdirty, gcount, gdict2, freel, nfree):
    gcount[a] -= 1
    gcount[b] += 1
    counts[i, a] -= 1
    if counts[i, a] == 0:
        p = pos[i, a]; last = pres[i, npres[i] - 1]
        pres[i, p] = last; pos[i, last] = p; pos[i, a] = -1; npres[i] -= 1
        gdirty[i] = 1
    new = counts[i, b] == 0
    if new:
        pres[i, npres[i]] = b; pos[i, b] = npres[i]; npres[i] += 1
        gdirty[i] = 1
    counts[i, b] += 1
    for tt in range(npres[i]):
        j = pres[i, tt]
        if new and j == b: continue
        paysum[i, j] += gpay(j, b, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode) - \
            gpay(j, a, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode)
    if new:
        vv = 0.0
        for tt in range(npres[i]):
            kk = pres[i, tt]
            vv += counts[i, kk] * gpay(b, kk, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode)
        paysum[i, b] = vv
    if gcount[a] == 0:
        gfree(a, gdict2, gbase, gg, freel, nfree)


@njit(cache=True)
def ginit_paysum(counts, paysum, pres, npres, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode):
    I = counts.shape[0]
    for i in range(I):
        for tt in range(npres[i]):
            j = pres[i, tt]
            vv = 0.0
            for t2 in range(npres[i]):
                kk = pres[i, t2]
                vv += counts[i, kk] * gpay(j, kk, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode)
            paysum[i, j] = vv


# ------------------------------------------------------------------------------------------------ grudge acts
@njit(cache=True)
def can_write(x, y, ax, ay, gbase, gg, GS, GN, tunit, tsp, widx, Wt):
    """x (after its production) may write a grudge against y's spelling: x cooperated (ax), y defected (ay)."""
    if ax != 1 or ay != 0: return False
    xb = gbase[x]; yb = gbase[y]
    if tsp[xb] == tsp[yb]: return False
    iw = widx[tunit[xb]]
    if iw < 0: return False
    if gholds(GS, GN, gg[x], tsp[yb]): return False
    return Wt[iw, tunit[yb]] == 1


@njit(cache=True)
def can_adopt(x, y, gbase, gg, GS, GN, tunit, tsp, widx, Wt, wdel, spE):
    """Horizontal: x adopts a key of y's list (same δ skeleton, valid for x at root (x, ⌜k⌝))."""
    xb = gbase[x]; yb = gbase[y]
    ix = widx[tunit[xb]]; iy = widx[tunit[yb]]
    if ix < 0 or iy < 0 or wdel[ix] != wdel[iy]: return False
    sx = tsp[xb]
    for q in range(GN[gg[y]]):
        s = GS[gg[y], q]
        if s == sx or gholds(GS, GN, gg[x], s): continue
        if Wt[ix, spE[s]] == 1: return True
    return False


@njit(cache=True)
def gappend(gid, s, GS, GN, gdict, ngv, tmp, gcap, gctr):
    n = GN[gid]
    m = 0
    start = 0
    if n >= gcap:
        start = n - gcap + 1
        gctr[GC_EVICT] += n - gcap + 1
    for q in range(start, n):
        tmp[m] = GS[gid, q]; m += 1
    tmp[m] = s; m += 1
    return gintern(gdict, GS, GN, ngv, tmp, m)


@njit(cache=True)
def gstep(x, y, ax, ay, gmode, gcap, gbase, gg, GS, GN, gdict, ngv, tmp, tunit, tsp, widx, Wt, wdel, spE, gctr, glog,
          nglog, g, i, natu, xpre):
    """x's grudge list after the encounter (x already produced): returns the new gid."""
    gid = gg[x]
    if gmode == G_OFF or gmode == G_PRE: return gid
    xb = gbase[x]; yb = gbase[y]
    if can_write(x, y, ax, ay, gbase, gg, GS, GN, tunit, tsp, widx, Wt):
        gid = gappend(gid, tsp[yb], GS, GN, gdict, ngv, tmp, gcap, gctr)
        if gid < 0: return -1
        gctr[GC_WRITE] += 1
        if natu[xpre] == 0: gctr[GC_BOOT] += 1
        q = nglog[0]
        if q < glog.shape[0]:
            glog[q, 0] = g; glog[q, 1] = i; glog[q, 2] = tsp[xb]; glog[q, 3] = tunit[xb]; glog[q, 4] = tsp[yb]
            glog[q, 5] = tunit[yb]; glog[q, 6] = ax * 2 + ay; glog[q, 7] = natu[xpre]
            nglog[0] = q + 1
    if gmode == G_HORIZ:
        ix = widx[tunit[xb]]; iy = widx[tunit[yb]]
        if ix >= 0 and iy >= 0 and wdel[ix] == wdel[iy]:
            sx = tsp[xb]
            for q in range(GN[gg[y]]):
                s = GS[gg[y], q]
                if s == sx or gholds(GS, GN, gid, s): continue
                if Wt[ix, spE[s]] == 1:
                    gid = gappend(gid, s, GS, GN, gdict, ngv, tmp, gcap, gctr)
                    if gid < 0: return -1
                    gctr[GC_ADOPT] += 1
    return gid


@njit(cache=True)
def pair_live(x, y, gmode, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, Wt, wdel, spE):
    """An encounter between settled base types can still change a grudge list."""
    if gmode == G_OFF or gmode == G_PRE: return False
    ax, ay = acts(x, y, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode)
    if can_write(x, y, ax, ay, gbase, gg, GS, GN, tunit, tsp, widx, Wt): return True
    if can_write(y, x, ay, ax, gbase, gg, GS, GN, tunit, tsp, widx, Wt): return True
    if gmode == G_HORIZ:
        if can_adopt(x, y, gbase, gg, GS, GN, tunit, tsp, widx, Wt, wdel, spE): return True
        if can_adopt(y, x, gbase, gg, GS, GN, tunit, tsp, widx, Wt, wdel, spE): return True
    return False


@njit(cache=True)
def island_live(i, pres, npres, gmode, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, Wt, wdel, spE):
    if gmode == G_OFF or gmode == G_PRE: return False
    for t1 in range(npres[i]):
        x = pres[i, t1]
        if widx[tunit[gbase[x]]] < 0: continue
        for t2 in range(npres[i]):
            y = pres[i, t2]
            if pair_live(x, y, gmode, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, Wt, wdel, spE):
                return True
    return False


# ------------------------------------------------------------------------------------------------ the segment
@njit(cache=True)
def segment_g(g0, gens, seed, N, w, m, r, slots, counts, paysum, pres, npres, pos, spcount, d, tunit, trule, tsp,
              tanc, ntv, utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, A, selfa, OSV, SPO,
              capable, COSTS, ctr, steps_rule, wn, wenc, wsp, wcode, wsid, ckey, cval, ncache, plog, hist_wait,
              hist_acq, hist_steps, hist_cens, nprod, identu, spou, tset, uns, rulecount, enc_exp, skip, FUT, fcount,
              enc_futile, err, epsg, pairmode, fseed, cumL, spE, rain_rule, rcount, arr, narr,
              gbase, gg, gdict2, ngt, GS, GN, gdict, ngv, widx, AG1, AG2, PW, Wt, wdel, natu, sucker, gmode, gcap,
              gctr, glog, nglog, gdirty, glive, isl_sucker_gen, gcount, freel, nfree):
    """Generations g0 .. g0 + gens - 1.  Slots, counts, pres and paysum are over grudge types; `side` runs on base
    types.  Island skip: no unsettled base type (uns) and no live grudge pair (glive, recomputed when the island's
    composition changed)."""
    I = slots.shape[0]
    KCAP = tunit.shape[0]
    fs = np.empty(N)
    stv = np.zeros(1)
    tmp = np.zeros(GCAP_MAX + 2, np.int64)
    tot_ind = float(I * N)
    neg = epsg.shape[0]
    for g in range(g0, g0 + gens):
        eps = epsg[g] if g < neg else 0.0
        for i in range(I):
            # a live flag may be stale-1 (safe: nothing is skipped); refresh dirty islands once per generation
            if skip and gdirty[i] == 1 and glive[i] == 1:
                glive[i] = 1 if island_live(i, pres, npres, gmode, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1,
                                            AG2, PW, Wt, wdel, spE) else 0
                gdirty[i] = 0
                gctr[GC_RECOMP] += 1
            ns = 0
            for tt in range(npres[i]):
                kk = pres[i, tt]
                if sucker[tunit[gbase[kk]]] == 1: ns += counts[i, kk]
            if ns > 0: isl_sucker_gen[0] += 1.0
            isl_sucker_gen[1] += ns / N
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
                    if gdirty[i] == 1 and glive[i] == 0:
                        glive[i] = 1 if island_live(i, pres, npres, gmode, gbase, gg, GS, GN, tunit, tsp, A, selfa,
                                                    widx, AG1, AG2, PW, Wt, wdel, spE) else 0
                        gdirty[i] = 0
                        gctr[GC_RECOMP] += 1
                    if glive[i] == 0:
                        continue
                f = ri(seed, ev, b0 + 1, N)
                p = ri(seed, ev, b0 + 2, N - 1)
                if p >= f: p += 1
                kf = slots[i, f]; kp = slots[i, p]
                bf = gbase[kf]; bp = gbase[kp]
                if skip and is_settled(bf, tunit, trule, tset, BLC, BLD, PD, utau, FUT) and \
                        is_settled(bp, tunit, trule, tset, BLC, BLD, PD, utau, FUT):
                    if not pair_live(kf, kp, gmode, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, Wt,
                                     wdel, spE):
                        continue
                gctr[GC_ENC] += 1
                af, ap = acts(kf, kp, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode)
                if sucker[tunit[bf]] == 1 or sucker[tunit[bp]] == 1: gctr[GC_SUCKER_ENC] += 1
                if gmode != G_OFF:
                    if gholds(GS, GN, gg[kf], tsp[bp]) or gholds(GS, GN, gg[kp], tsp[bf]): gctr[GC_LIVE_ENC] += 1
                rel = PV.relation(bf, bp, tunit, tsp)
                shf = -1; shp = -1
                if trule[bf] == R_SDEL:
                    s1 = ri(seed, ev, b0 + 3, N - 1)
                    if s1 >= f: s1 += 1
                    shf = tsp[gbase[slots[i, s1]]]
                if trule[bp] == R_SDEL:
                    s2 = ri(seed, ev, b0 + 4, N - 1)
                    if s2 >= p: s2 += 1
                    shp = tsp[gbase[slots[i, s2]]]
                if plog[i, f, 0] >= 0 and plog[i, f, 4] < 0:
                    plog[i, f, 4] = 1 if (spcount[i, tsp[bf]] - 1) >= 0.9 * (N - 1) else 0
                if plog[i, p, 0] >= 0 and plog[i, p, 4] < 0:
                    plog[i, p, 4] = 1 if (spcount[i, tsp[bp]] - 1) >= 0.9 * (N - 1) else 0
                nbf = side(i, f, bf, bp, rel, shf, d, tunit, trule, tsp, tanc, ntv, KCAP, utau, BLC, BLD, SINGLE, APP,
                           PRODC, PD, KIND, NAT, CHC, CHD, UVt, OSV, SPO, COSTS, ctr, steps_rule, wn, wenc, wsp, wcode,
                           wsid, ckey, cval, ncache, plog, stv, err)
                if err[0] != 0: return g
                nbp = side(i, p, bp, bf, rel, shp, d, tunit, trule, tsp, tanc, ntv, KCAP, utau, BLC, BLD, SINGLE, APP,
                           PRODC, PD, KIND, NAT, CHC, CHD, UVt, OSV, SPO, COSTS, ctr, steps_rule, wn, wenc, wsp, wcode,
                           wsid, ckey, cval, ncache, plog, stv, err)
                if err[0] != 0: return g
                # grudge lists after production (the would-be self: the produced unit, pre-encounter partner)
                nf = kf; np_ = kp
                if nbf != bf:
                    nf = gmake(gdict2, gbase, gg, ngt, nbf, gg[kf], freel, nfree)
                if nbp != bp:
                    np_ = gmake(gdict2, gbase, gg, ngt, nbp, gg[kp], freel, nfree)
                if nf < 0 or np_ < 0:
                    err[0] = 31
                    return g
                if gmode == G_VERT or gmode == G_HORIZ or gmode == G_SHAM:
                    gf = gstep(nf, kp, af, ap, gmode, gcap, gbase, gg, GS, GN, gdict, ngv, tmp, tunit, tsp, widx, Wt,
                               wdel, spE, gctr, glog, nglog, g, i, natu, tunit[bf])
                    gp = gstep(np_, kf, ap, af, gmode, gcap, gbase, gg, GS, GN, gdict, ngv, tmp, tunit, tsp, widx, Wt,
                               wdel, spE, gctr, glog, nglog, g, i, natu, tunit[bp])
                    if gf < 0 or gp < 0:
                        err[0] = 32
                        return g
                    nf0 = nf; np0 = np_
                    if gf != gg[nf]:
                        nf = gmake(gdict2, gbase, gg, ngt, gbase[nf0], gf, freel, nfree)
                    if gp != gg[np_]:
                        np_ = gmake(gdict2, gbase, gg, ngt, gbase[np0], gp, freel, nfree)
                    if nf < 0 or np_ < 0:
                        err[0] = 31
                        return g
                    if nf0 != nf and nf0 != np_ and nf0 != kf and nf0 != kp:
                        gdrop(nf0, gcount, gdict2, gbase, gg, freel, nfree)
                    if np0 != np_ and np0 != nf and np0 != kf and np0 != kp and np0 != nf0:
                        gdrop(np0, gcount, gdict2, gbase, gg, freel, nfree)
                    if nf < 0 or np_ < 0:
                        err[0] = 31
                        return g
                nbf = gbase[nf]; nbp = gbase[np_]
                if nf != kf:
                    slots[i, f] = nf
                    if nbf != bf:
                        ctr[trule[bf], C_CHANGE] += 1
                        if BLC[tunit[nbf], 0] >= 0 and BLC[tunit[bf], 0] < 0:
                            plog_close(i, f, bf, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq,
                                       hist_steps, hist_cens, nprod, 0)
                        if identu[tunit[nbf]] and not identu[tunit[bf]]: ctr[trule[bf], C_IDENT_ENTRY] += 1
                        if spou[tunit[nbf]] and not spou[tunit[bf]]: ctr[trule[bf], C_SPOU_ENTRY] += 1
                        uns[i] += (0 if is_settled(nbf, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1) - \
                            (0 if is_settled(bf, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1)
                        fcount[trule[bf]] += (1 if tset[nbf] == 2 else 0) - (1 if tset[bf] == 2 else 0)
                    gchange(i, kf, nf, counts, paysum, pres, npres, pos, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx,
                            AG1, AG2, PW, gmode, gdirty, gcount, gdict2, freel, nfree)
                if np_ != kp:
                    slots[i, p] = np_
                    if nbp != bp:
                        ctr[trule[bp], C_CHANGE] += 1
                        if BLC[tunit[nbp], 0] >= 0 and BLC[tunit[bp], 0] < 0:
                            plog_close(i, p, bp, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq,
                                       hist_steps, hist_cens, nprod, 0)
                        if identu[tunit[nbp]] and not identu[tunit[bp]]: ctr[trule[bp], C_IDENT_ENTRY] += 1
                        if spou[tunit[nbp]] and not spou[tunit[bp]]: ctr[trule[bp], C_SPOU_ENTRY] += 1
                        uns[i] += (0 if is_settled(nbp, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1) - \
                            (0 if is_settled(bp, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1)
                        fcount[trule[bp]] += (1 if tset[nbp] == 2 else 0) - (1 if tset[bp] == 2 else 0)
                    gchange(i, kp, np_, counts, paysum, pres, npres, pos, gbase, gg, GS, GN, tunit, tsp, A, selfa,
                            widx, AG1, AG2, PW, gmode, gdirty, gcount, gdict2, freel, nfree)
            # birth-death, event-indexed draws 0-4 (provenance's)
            i = ri(seed, ev, 0, I)
            src = i
            if m > 0.0 and I > 1 and ru(seed, ev, 1) < m:
                src = ri(seed, ev, 2, I - 1)
                if src >= i: src += 1
            nps = npres[src]
            mx = -1e300
            for tt in range(nps):
                kk = pres[src, tt]
                fv = (paysum[src, kk] - gpay(kk, kk, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW,
                                             gmode)) / (N - 1)
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
                # a fresh founder from L (draw 6, or the island's paired stream), empty lists, no grudges
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
                cb, nt2 = make_type(d, tunit, trule, tsp, tanc, nt, spE[s], rain_rule, s, 0)
                ntv[0] = nt2
                child = gmake(gdict2, gbase, gg, ngt, cb, 0, freel, nfree)
                if child < 0:
                    err[0] = 31
                    return g
                rcount[i] += 1
                qa = narr[0]
                if qa < arr.shape[0]:
                    arr[qa, 0] = g; arr[qa, 1] = i; arr[qa, 2] = s
                    narr[0] = qa + 1
            cbb = gbase[child]; kvb = gbase[kv]
            ctr[trule[cbb], C_BIRTH] += 1
            plog_close(i, vs, kvb, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq, hist_steps, hist_cens,
                       nprod, 1)
            wn[i, vs] = 0; wenc[i, vs] = 0; ncache[i, vs] = 0
            plog_open(i, vs, cbb, tunit, trule, BLC, plog)
            spcount[i, tsp[kvb]] -= 1
            spcount[i, tsp[cbb]] += 1
            rulecount[trule[kvb]] -= 1
            rulecount[trule[cbb]] += 1
            if kv == child: continue
            uns[i] += (0 if is_settled(cbb, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1) - \
                (0 if is_settled(kvb, tunit, trule, tset, BLC, BLD, PD, utau, FUT) else 1)
            fcount[trule[cbb]] += 1 if tset[cbb] == 2 else 0
            fcount[trule[kvb]] -= 1 if tset[kvb] == 2 else 0
            slots[i, vs] = child
            gchange(i, kv, child, counts, paysum, pres, npres, pos, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1,
                    AG2, PW, gmode, gdirty, gcount, gdict2, freel, nfree)
    return g0 + gens


@njit(cache=True)
def gisland_stats(counts, pres, npres, N, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode, maj_k,
                  maj_n):
    """Per island: P(C,C) over ordered pairs of distinct individuals; the majority quote (a representative grudge type
    and the quote's count; a quote is (unit, spelling), grudge lists aside)."""
    I = counts.shape[0]
    cc = np.zeros(I)
    for i in range(I):
        tot = 0.0
        best = -1; bn = -1
        for t1 in range(npres[i]):
            a = pres[i, t1]
            ab = gbase[a]
            qn = 0
            first = True
            for t2 in range(npres[i]):
                b = pres[i, t2]
                bb = gbase[b]
                if tunit[bb] == tunit[ab] and tsp[bb] == tsp[ab]:
                    if t2 < t1: first = False
                    qn += counts[i, b]
            if first and qn > bn:
                bn = qn; best = a
            for t2 in range(npres[i]):
                b = pres[i, t2]
                nn = counts[i, a] * counts[i, b] if a != b else counts[i, a] * (counts[i, a] - 1)
                tot += nn * gcc(a, b, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode)
        cc[i] = tot / (N * (N - 1))
        maj_k[i] = best; maj_n[i] = bn
    return cc


@njit(cache=True)
def gacts_matrix(i, pres, npres, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode):
    """M[a, b] = action of the a-th present type against the b-th (diagonal: self-play of the type's quote)."""
    n = npres[i]
    M = np.zeros((n, n), np.int8)
    for a in range(n):
        for b in range(a, n):
            x, y = acts(pres[i, a], pres[i, b], gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode)
            M[a, b] = x
            M[b, a] = y
    return M


@njit(cache=True)
def gfitness(i, counts, paysum, pres, npres, N, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode,
             out):
    """Per present type on island i: the kernel's fitness (mean payoff against the others)."""
    for tt in range(npres[i]):
        kk = pres[i, tt]
        out[tt] = (paysum[i, kk] - gpay(kk, kk, gbase, gg, GS, GN, tunit, tsp, A, selfa, widx, AG1, AG2, PW, gmode)) / (N - 1)
