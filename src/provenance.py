"""Provenance: who writes the first certificate, and against whom (notes/provenance.md §1).

Milestone 5's certificate-gene ecology (src/lt_genes*.py, tables reused) with the production mode replaced by a
*provenance rule*, a property of the program kept as metadata (not in the quote):

    H, S-self, C, S-nonself, S-2, S-3, S-3 strict, S-gate+cache, S-self-delayed, CS-nonself.

Quotes are (code, certificate list): two individuals are the same quote iff same spelling and same unit; the rules'
"source" test reads the spelling only.  Every random number of the dynamics is a counter-based function of
(replicate seed, Moran event, draw index), so paired cells consume identical draws at identical events.

Parts: (1) rules and the counter RNG; (2) the island kernel (numba); (3) static helpers (own-side validity, the
self-play-only table, the S-nonself closure, the ablation sets); (4) term-level rule procedures (tests, single pairs).
"""
import os
import sys

import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(__file__))
import lt_genes_kern as KN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'provenance')

# ---------------------------------------------------------------------------------------------------------------- 1
R_H, R_SSELF, R_C, R_SNON, R_SK2, R_SK3, R_SK3S, R_SGATE, R_SDEL, R_CSNON = range(10)
NRULE = 10
RULE_NAMES = ['H', 'S-self', 'C', 'S-nonself', 'S-2', 'S-3', 'S-3 strict', 'S-gate+cache', 'S-self-delayed',
              'CS-nonself']
RULE_OF = {n: i for i, n in enumerate(RULE_NAMES)}
MODE_OF = np.array([0, 1, 2, 1, 1, 1, 1, 1, 1, 3], np.int64)       # H S C CS
PRODUCING = np.array([0, 1, 0, 1, 1, 1, 1, 1, 1, 1], np.bool_)      # rules with an S step
LMAX = KN.LMAX
UV_C_SELF, UV_D_SELF, UV_C_C, UV_D_C, UV_C_D, UV_D_D = range(6)
PAYM = KN.PAYM
WINDOW_DEADLINE = 50
CACHE_CAP = 64

# counters (per rule)
NCTR = 40
(C_ENC, C_CATT, C_COK, C_CTO, C_CNONE, C_DATT, C_DOK, C_DTO, C_AC, C_ACOK, C_SPO_PROD, C_SPO_COPY, C_SKIPSELF,
 C_WIN_K, C_WIN_DL, C_WIN_SAFE, C_WIN_FALLBACK, C_WIN_STRICTCLR, C_WIN_EMPTYCLR, C_CAND, C_GATE, C_GATE_T, C_HIT,
 C_MISS, C_STORE, C_OVERFLOW, C_HIT_TO, C_HIT_REJ, C_INVAL, C_BIRTH, C_CHANGE, C_DELAY_SKIP, C_GATE_TO,
 C_GATE_APPEND, C_SPO_GATE, C_SAFE_SPO, C_FALL_SPO, C_NONSELF_SPO, C_IDENT_ENTRY, C_SPOU_ENTRY) = range(40)
# histogram bins over encounters: [0,1,2,3,5,10,20,50,100,200,500,1000,2000,5000,inf)
EBINS = np.array([0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10 ** 12], np.int64)
NEB = len(EBINS) - 1
NSB = 60                                   # steps histogram: 0.1-decade bins from 10^2 to 10^8


@njit(cache=True)
def mix64(z):
    z = z ^ (z >> np.uint64(30))
    z = z * np.uint64(0xBF58476D1CE4E5B9)
    z = z ^ (z >> np.uint64(27))
    z = z * np.uint64(0x94D049BB133111EB)
    z = z ^ (z >> np.uint64(31))
    return z


@njit(cache=True)
def ru(seed, ev, j):
    """Uniform in [0, 1) from (seed, event, draw)."""
    z = mix64(np.uint64(seed) * np.uint64(0x9E3779B97F4A7C15) + np.uint64(1442695040888963407))
    z = mix64(z ^ (np.uint64(ev) * np.uint64(512) + np.uint64(j)))
    return float(z >> np.uint64(11)) * (1.0 / 9007199254740992.0)


@njit(cache=True)
def ri(seed, ev, j, n):
    k = int(ru(seed, ev, j) * n)
    return k if k < n else n - 1


@njit(cache=True)
def ebin(x):
    for b in range(NEB):
        if x < EBINS[b + 1]:
            return b
    return NEB - 1


@njit(cache=True)
def sbin(x):
    if x <= 100.0: return 0
    b = int((np.log10(x) - 2.0) * 10.0)
    if b < 0: return 0
    if b >= NSB: return NSB - 1
    return b


# ---------------------------------------------------------------------------------------------------------------- 2
@njit(cache=True)
def type_code(unit, rule, sp, anc):
    return ((unit * 16 + rule) * 16384 + (sp + 1)) * 4096 + anc


@njit(cache=True)
def make_type(d, tunit, trule, tsp, tanc, nt, unit, rule, sp, anc):
    code = type_code(unit, rule, sp, anc)
    if code in d:
        return d[code], nt
    k = nt
    d[code] = k
    tunit[k] = unit; trule[k] = rule; tsp[k] = sp; tanc[k] = anc
    return k, nt + 1


@njit(cache=True)
def relation(k, j, tunit, tsp):
    """0 distinct units, 1 twin (same unit, other spelling), 2 same quote (same spelling and same unit)."""
    if tunit[k] != tunit[j]: return 0
    if tsp[k] == tsp[j]: return 2
    return 1


@njit(cache=True)
def pay(k, j, tunit, tsp, A, selfa):
    u = tunit[k]; v = tunit[j]
    if u == v and tsp[k] == tsp[j]:
        a = selfa[u]
        return PAYM[a, a]
    return PAYM[A[u, v], A[v, u]]


@njit(cache=True)
def cc_pair(k, j, tunit, tsp, A, selfa):
    u = tunit[k]; v = tunit[j]
    if u == v and tsp[k] == tsp[j]:
        return 1.0 if selfa[u] == 1 else 0.0
    return 1.0 if (A[u, v] == 1 and A[v, u] == 1) else 0.0


@njit(cache=True)
def d_step(u, anc, PD, BLD, ctr, steps, COSTS, err):
    """The D production of every producing rule (milestone 5): while the list has no D entry, PROD(x, ⌜D⌝, D)."""
    if BLD[u, 0] >= 0:
        return u, anc
    ctr[C_DATT] += 1
    u2 = PD[u]
    if u2 == -2:
        err[0] = 21
        return u, anc
    if u2 == -3:
        ctr[C_DTO] += 1
        steps[0] += COSTS[5]
        return u, anc
    steps[0] += COSTS[4]
    if u2 != u:
        ctr[C_DOK] += 1
        anc = anc | (1 << LMAX)
        return u2, anc
    return u, anc


@njit(cache=True)
def c_code(u, v, rel, utau, KIND, NAT, CHD, UVt, BLC, BLD):
    return KN.sig_code(u, v, rel, utau, KIND, NAT, CHD, UVt, BLC, BLD)


@njit(cache=True)
def c_produce(u, v, rel, utau, KIND, NAT, CHD, UVt, BLC, BLD, PRODC, ctr, steps, COSTS, err):
    """The tactic's C script against v (signature lookup).  Returns (sid >= 0 | -1 none | -3 cap timeout, code)."""
    t = utau[u]
    code = c_code(u, v, rel, utau, KIND, NAT, CHD, UVt, BLC, BLD)
    sid = PRODC[t, code]
    ctr[C_CATT] += 1
    if sid == -2:
        err[0] = 22
        return -1, code
    if sid == -3:
        ctr[C_CTO] += 1
        steps[0] += COSTS[5]
        return -3, code
    steps[0] += COSTS[3]
    if sid < 0:
        ctr[C_CNONE] += 1
    return sid, code


@njit(cache=True)
def c_append(u, sid, anc, APP, BLC, err):
    pos = KN.blen(BLC, u)
    u2 = APP[u, sid]
    if u2 < 0:
        err[0] = 23
        return u, anc
    return u2, anc | (1 << pos)


@njit(cache=True)
def copy_step(u, sp, v, spv, rel, anc, ancv, utau, BLC, BLD, SINGLE, APP, CHC, UVt, SPO, ctr, steps, COSTS, err):
    """Milestone 5's copy-and-check (lack rule, would-be-self check), exact at a would-be self equal to the donor's
    quote (a self-play check)."""
    if rel == 2:
        return u, anc
    t = utau[u]
    for blk in range(2):
        BL = BLC if blk == 0 else BLD
        off = 0 if blk == 0 else LMAX
        if BL[u, 0] >= 0:
            continue
        for kk in range(LMAX):
            s = BL[v, kk]
            if s < 0: break
            if KN.holds(BL, u, s): continue
            ctr[C_AC] += 1
            steps[0] += COSTS[0]
            if SINGLE[t, s] < 0:
                continue
            xs = APP[u, s]
            if xs < 0:
                err[0] = 24
                return u, anc
            if blk == 0:
                if xs == v and sp == spv:
                    acv = UVt[xs, UV_C_SELF]
                else:
                    acv = CHC[xs, v]
            else:
                acv = UVt[xs, UV_D_D]
            if acv < 0:
                err[0] = 25
                return u, anc
            if acv == 1:
                pos = KN.blen(BL, u)
                bit = (ancv >> (off + kk)) & 1
                anc = anc | (bit << (off + pos))
                if blk == 0 and SPO[t, s]:
                    ctr[C_SPO_COPY] += 1
                u = xs
                ctr[C_ACOK] += 1
                break
    return u, anc


@njit(cache=True)
def window_close(i, a, t, rule, wn, wsid, wcode, OSV, ctr):
    """Selection at window closing.  Returns the kept sid or -1 (cleared)."""
    n = wn[i, a]
    best = -1
    first = -1
    for c in range(n):
        s = wsid[i, a, c]
        if s < 0: continue
        sc = 0
        for m in range(n):
            if OSV[t, s, wcode[i, a, m]] == 1:
                sc += 1
        if sc >= 1 and first < 0:
            first = s                                   # the earliest admissible candidate (validity >= 1)
        if sc >= 2:
            best = s
            break
    if best >= 0:
        ctr[C_WIN_SAFE] += 1
        return best, 1
    if first < 0:
        ctr[C_WIN_EMPTYCLR] += 1
        return -1, 0
    if rule == R_SK3S:
        ctr[C_WIN_STRICTCLR] += 1
        return -1, 0
    ctr[C_WIN_FALLBACK] += 1
    return first, 2


@njit(cache=True)
def side(i, a, k, j, rel, shadow_sp, d, tunit, trule, tsp, tanc, ntv, KCAP, utau, BLC, BLD, SINGLE, APP, PRODC, PD,
         KIND, NAT, CHC, CHD, UVt, OSV, SPO, COSTS, ctr, steps_rule, wn, wenc, wsp, wcode, wsid, ckey, cval, ncache,
         plog, st, err):
    """The type individual (i, a) of type k becomes after an encounter with an individual of type j (rel: their
    relation; shadow_sp: the spelling of S-self-delayed's shadow draw).  Mutable per-individual state (window, cache,
    producer log) is updated in place.  Returns the new type."""
    rule = trule[k]
    if rule == R_H:
        return k
    u = tunit[k]; anc = tanc[k]; sp = tsp[k]
    v = tunit[j]; spv = tsp[j]
    t = utau[u]
    u0 = u; anc0 = anc
    cr = ctr[rule]
    st[0] = 0.0
    lacking = BLC[u, 0] < 0
    if lacking and plog[i, a, 0] >= 0:
        plog[i, a, 1] += 1                                   # encounters while lacking
    if rule == R_C or rule == R_CSNON:
        u, anc = copy_step(u, sp, v, spv, rel, anc, tanc[j], utau, BLC, BLD, SINGLE, APP, CHC, UVt, SPO, cr, st,
                           COSTS, err)
        if err[0] != 0: return k
    if rule != R_C:
        # relation after a copy (the partner's quote is the pre-encounter one)
        rel2 = rel
        if u != u0:
            rel2 = 0 if u != v else (2 if sp == spv else 1)
        if rule == R_SGATE:
            # the gate with the negative cache (notes §1.2)
            key = (v * 16384 + (spv + 1)) * 2 + (1 if rel2 == 2 else 0)
            nc = ncache[i, a]
            hit = -1
            for e in range(nc):
                if ckey[i, a, e] == key:
                    hit = e
                    break
            st[0] += 1.0 + (hit + 1 if hit >= 0 else nc)
            cr[C_GATE] += 1
            if hit >= 0:
                cr[C_HIT] += 1
                if cval[i, a, hit] == 2: cr[C_HIT_TO] += 1
                else: cr[C_HIT_REJ] += 1
            else:
                cr[C_MISS] += 1
                hasc = BLC[u, 0] >= 0
                if hasc:
                    g = UVt[u, UV_C_SELF] if rel2 == 2 else CHC[u, v]
                    if g < 0:
                        err[0] = 26
                        return k
                    st[0] += COSTS[1]
                else:
                    g = 0
                    st[0] += COSTS[2]
                if g == 1:
                    cr[C_GATE_T] += 1
                else:
                    if g == 2: cr[C_GATE_TO] += 1
                    if plog[i, a, 0] >= 0 and plog[i, a, 2] < 0:
                        plog[i, a, 2] = plog[i, a, 1] - 1
                    sid, code = c_produce(u, v, rel2, utau, KIND, NAT, CHD, UVt, BLC, BLD, PRODC, cr, st, COSTS, err)
                    if err[0] != 0: return k
                    if sid >= 0 and not KN.holds(BLC, u, sid):
                        if SPO[t, sid]: cr[C_SPO_PROD] += 1; cr[C_SPO_GATE] += 1
                        u, anc = c_append(u, sid, anc, APP, BLC, err)
                        if err[0] != 0: return k
                        cr[C_COK] += 1; cr[C_GATE_APPEND] += 1
                    else:
                        val = 2 if (g == 2 or sid == -3) else 1
                        if nc < CACHE_CAP:
                            ckey[i, a, nc] = key; cval[i, a, nc] = val; ncache[i, a] = nc + 1
                            st[0] += 3.0
                            cr[C_STORE] += 1
                        else:
                            cr[C_OVERFLOW] += 1
        elif BLC[u, 0] < 0:
            if rule == R_SSELF or rule == R_CSNON or rule == R_SNON or rule == R_SDEL:
                go = True
                if rule == R_SNON or rule == R_CSNON:
                    go = spv != sp
                elif rule == R_SDEL:
                    go = shadow_sp != sp
                if not go:
                    if rule == R_SDEL: cr[C_DELAY_SKIP] += 1
                    else: cr[C_SKIPSELF] += 1
                else:
                    if plog[i, a, 0] >= 0 and plog[i, a, 2] < 0:
                        plog[i, a, 2] = plog[i, a, 1] - 1        # the wait: encounters before the first attempt
                    sid, code = c_produce(u, v, rel2, utau, KIND, NAT, CHD, UVt, BLC, BLD, PRODC, cr, st, COSTS, err)
                    if err[0] != 0: return k
                    if sid >= 0:
                        if SPO[t, sid]:
                            cr[C_SPO_PROD] += 1
                            if rule == R_SNON or rule == R_CSNON: cr[C_NONSELF_SPO] += 1
                        u, anc = c_append(u, sid, anc, APP, BLC, err)
                        if err[0] != 0: return k
                        cr[C_COK] += 1
            else:
                # S-k windows
                kk = 2 if rule == R_SK2 else 3
                wenc[i, a] += 1
                n = wn[i, a]
                seen = False
                for m in range(n):
                    if wsp[i, a, m] == spv:
                        seen = True
                        break
                if not seen:
                    if plog[i, a, 0] >= 0 and plog[i, a, 2] < 0:
                        plog[i, a, 2] = plog[i, a, 1] - 1
                    sid, code = c_produce(u, v, rel2, utau, KIND, NAT, CHD, UVt, BLC, BLD, PRODC, cr, st, COSTS, err)
                    if err[0] != 0: return k
                    wsp[i, a, n] = spv; wcode[i, a, n] = code; wsid[i, a, n] = sid if sid >= 0 else -1
                    if sid >= 0: cr[C_CAND] += 1
                    st[0] += 2.0                                  # the partner's quote stored
                    n += 1
                    wn[i, a] = n
                if n >= kk or wenc[i, a] >= WINDOW_DEADLINE:
                    if n >= kk: cr[C_WIN_K] += 1
                    else: cr[C_WIN_DL] += 1
                    ncand = 0
                    for m in range(n):
                        if wsid[i, a, m] >= 0: ncand += 1
                    st[0] += COSTS[0] * ncand * (n - 1)          # own-side validations of candidates
                    keep, how = window_close(i, a, t, rule, wn, wsid, wcode, OSV, cr)
                    wn[i, a] = 0; wenc[i, a] = 0
                    if keep >= 0:
                        if SPO[t, keep]:
                            cr[C_SPO_PROD] += 1
                            if how == 1: cr[C_SAFE_SPO] += 1
                            else: cr[C_FALL_SPO] += 1
                        u, anc = c_append(u, keep, anc, APP, BLC, err)
                        if err[0] != 0: return k
                        cr[C_COK] += 1
        u, anc = d_step(u, anc, PD, BLD, cr, st, COSTS, err)
        if err[0] != 0: return k
    cr[C_ENC] += 1
    steps_rule[rule] += st[0]
    if plog[i, a, 0] >= 0:
        plog[i, a, 3] += int(st[0])                                # steps while lacking
    if u == u0 and anc == anc0:
        return k
    if u != u0 and rule == R_SGATE:
        ncache[i, a] = 0                                           # invalidation on any change of one's own list
        cr[C_INVAL] += 1
    nt = ntv[0]
    if nt >= KCAP - 2:
        err[0] = 2
        return k
    kk2, nt2 = make_type(d, tunit, trule, tsp, tanc, nt, u, rule, sp, anc)
    ntv[0] = nt2
    return kk2


@njit(cache=True)
def plog_close(i, a, k, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq, hist_steps, hist_cens, nprod,
               how):
    """Close a producer's log: how 0 acquired, 1 censored by death, 2 censored by the horizon."""
    if plog[i, a, 0] < 0: return
    rule = trule[k]
    cap = 1 if capable[utau[tunit[k]]] else 0
    mono = plog[i, a, 4]
    w = plog[i, a, 2]
    if how == 0:
        hist_acq[rule, cap, ebin(plog[i, a, 1])] += 1
        hist_steps[rule, sbin(float(plog[i, a, 3]))] += 1
        nprod[rule, cap, 0] += 1
    else:
        hist_cens[rule, cap, how - 1, ebin(plog[i, a, 1])] += 1
        nprod[rule, cap, how] += 1
    if w >= 0:
        hist_wait[rule, cap, 0, ebin(w)] += 1
        if mono == 1: hist_wait[rule, cap, 1, ebin(w)] += 1
    else:
        # never attempted: the wait is at least the encounters seen
        hist_wait[rule, cap, 2, ebin(plog[i, a, 1])] += 1
        if mono == 1: hist_wait[rule, cap, 3, ebin(plog[i, a, 1])] += 1
    if mono == 1: nprod[rule, cap, 3] += 1
    plog[i, a, 0] = -1


@njit(cache=True)
def plog_open(i, a, k, tunit, trule, BLC, plog):
    rule = trule[k]
    if PRODUCING[rule] and BLC[tunit[k], 0] < 0:
        plog[i, a, 0] = 1; plog[i, a, 1] = 0; plog[i, a, 2] = -1; plog[i, a, 3] = 0; plog[i, a, 4] = -1
    else:
        plog[i, a, 0] = -1


@njit(cache=True)
def _change(i, a, b, counts, paysum, pres, npres, pos, tunit, tsp, A, selfa):
    counts[i, a] -= 1
    if counts[i, a] == 0:
        p = pos[i, a]; last = pres[i, npres[i] - 1]
        pres[i, p] = last; pos[i, last] = p; pos[i, a] = -1; npres[i] -= 1
    new = counts[i, b] == 0
    if new:
        pres[i, npres[i]] = b; pos[i, b] = npres[i]; npres[i] += 1
    counts[i, b] += 1
    for tt in range(npres[i]):
        j = pres[i, tt]
        if new and j == b: continue
        paysum[i, j] += pay(j, b, tunit, tsp, A, selfa) - pay(j, a, tunit, tsp, A, selfa)
    if new:
        vv = 0.0
        for tt in range(npres[i]):
            kk = pres[i, tt]
            vv += counts[i, kk] * pay(b, kk, tunit, tsp, A, selfa)
        paysum[i, b] = vv


@njit(cache=True)
def init_paysum(counts, paysum, pres, npres, tunit, tsp, A, selfa):
    I = counts.shape[0]
    for i in range(I):
        for tt in range(npres[i]):
            j = pres[i, tt]
            vv = 0.0
            for t2 in range(npres[i]):
                kk = pres[i, t2]
                vv += counts[i, kk] * pay(j, kk, tunit, tsp, A, selfa)
            paysum[i, j] = vv


@njit(cache=True)
def is_settled(k, tunit, trule, tset, BLC, BLD):
    """A type none of whose encounters can change it: H, or a lack rule holding a C and a D entry."""
    s = tset[k]
    if s >= 0:
        return s == 1
    rule = trule[k]; u = tunit[k]
    v = 1 if (rule == R_H or (rule != R_SGATE and BLC[u, 0] >= 0 and BLD[u, 0] >= 0)) else 0
    tset[k] = v
    return v == 1


@njit(cache=True)
def init_uns(slots, tunit, trule, tset, BLC, BLD, uns, rulecount):
    I, N = slots.shape
    for i in range(I):
        uns[i] = 0
        for j in range(N):
            k = slots[i, j]
            if not is_settled(k, tunit, trule, tset, BLC, BLD):
                uns[i] += 1
            rulecount[trule[k]] += 1


@njit(cache=True)
def segment(g0, gens, seed, N, w, m, r, slots, counts, paysum, pres, npres, pos, spcount, d, tunit, trule, tsp, tanc,
            ntv, utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, A, selfa, OSV, SPO, capable, COSTS,
            ctr, steps_rule, wn, wenc, wsp, wcode, wsid, ckey, cval, ncache, plog, hist_wait, hist_acq, hist_steps,
            hist_cens, nprod, identu, spou, tset, uns, rulecount, enc_exp, skip, err):
    """Generations g0 .. g0 + gens - 1 (I*N Moran events each, r encounters per event).  An encounter on an island
    whose residents are all *settled* (H, or holding a C and a D entry under a lack rule) changes nothing and is
    skipped (its draws are event-indexed, so skipping consumes nothing); enc_exp accumulates the expected
    side-encounters per rule (the per-match denominator)."""
    I = slots.shape[0]
    KCAP = tunit.shape[0]
    fs = np.empty(N)
    stv = np.zeros(1)
    tot_ind = float(I * N)
    for g in range(g0, g0 + gens):
        for e in range(I * N):
            ev = g * I * N + e
            for rr in range(NRULE):
                if rulecount[rr] > 0:
                    enc_exp[rr] += 2.0 * r * rulecount[rr] / tot_ind
            for q in range(r):
                b0 = 8 + 5 * q
                i = ri(seed, ev, b0, I)
                if skip and uns[i] == 0:
                    continue
                f = ri(seed, ev, b0 + 1, N)
                p = ri(seed, ev, b0 + 2, N - 1)
                if p >= f: p += 1
                kf = slots[i, f]; kp = slots[i, p]
                if skip and is_settled(kf, tunit, trule, tset, BLC, BLD) and \
                        is_settled(kp, tunit, trule, tset, BLC, BLD):
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
                    uns[i] += (0 if is_settled(nf, tunit, trule, tset, BLC, BLD) else 1) - \
                        (0 if is_settled(kf, tunit, trule, tset, BLC, BLD) else 1)
                    _change(i, kf, nf, counts, paysum, pres, npres, pos, tunit, tsp, A, selfa)
                if np_ != kp:
                    slots[i, p] = np_; ctr[trule[kp], C_CHANGE] += 1
                    if BLC[tunit[np_], 0] >= 0 and BLC[tunit[kp], 0] < 0:
                        plog_close(i, p, kp, tunit, trule, utau, BLC, capable, plog, hist_wait, hist_acq, hist_steps,
                                   hist_cens, nprod, 0)
                    if identu[tunit[np_]] and not identu[tunit[kp]]: ctr[trule[kp], C_IDENT_ENTRY] += 1
                    if spou[tunit[np_]] and not spou[tunit[kp]]: ctr[trule[kp], C_SPOU_ENTRY] += 1
                    uns[i] += (0 if is_settled(np_, tunit, trule, tset, BLC, BLD) else 1) - \
                        (0 if is_settled(kp, tunit, trule, tset, BLC, BLD) else 1)
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
            uns[i] += (0 if is_settled(child, tunit, trule, tset, BLC, BLD) else 1) - \
                (0 if is_settled(kv, tunit, trule, tset, BLC, BLD) else 1)
            slots[i, vs] = child
            _change(i, kv, child, counts, paysum, pres, npres, pos, tunit, tsp, A, selfa)
    return g0 + gens


@njit(cache=True)
def island_stats(counts, pres, npres, N, tunit, tsp, A, selfa, maj_k, maj_n):
    """Per island: P(C,C) over ordered pairs of distinct individuals; the majority quote (a representative type and
    the quote's count)."""
    I = counts.shape[0]
    cc = np.zeros(I)
    for i in range(I):
        tot = 0.0
        best = -1; bn = -1
        for t1 in range(npres[i]):
            a = pres[i, t1]
            # the quote's count: types with the same (unit, spelling)
            qn = 0
            first = True
            for t2 in range(npres[i]):
                b = pres[i, t2]
                if tunit[b] == tunit[a] and tsp[b] == tsp[a]:
                    if t2 < t1: first = False
                    qn += counts[i, b]
            if first and qn > bn:
                bn = qn; best = a
            for t2 in range(npres[i]):
                b = pres[i, t2]
                nn = counts[i, a] * counts[i, b] if a != b else counts[i, a] * (counts[i, a] - 1)
                tot += nn * cc_pair(a, b, tunit, tsp, A, selfa)
        cc[i] = tot / (N * (N - 1))
        maj_k[i] = best; maj_n[i] = bn
    return cc


@njit(cache=True)
def e3_status(counts, pres, npres, glob_types, nglob, tunit, tsp, A, selfa):
    """Milestone 2's E3 per island (1 success, 0 fail, -1 indeterminate)."""
    I = counts.shape[0]
    out = np.zeros(I, np.int64)
    inZ = np.zeros(nglob, np.bool_)
    queue = np.empty(nglob, np.int64)
    gidx = -np.ones(tunit.shape[0], np.int64)
    for tt in range(nglob): gidx[glob_types[tt]] = tt
    for i in range(I):
        for tt in range(nglob): inZ[tt] = False
        qn = 0; qh = 0
        for tt in range(npres[i]):
            gi = gidx[pres[i, tt]]
            inZ[gi] = True; queue[qn] = gi; qn += 1
        while qh < qn:
            z = glob_types[queue[qh]]; qh += 1
            uzz = pay(z, z, tunit, tsp, A, selfa)
            for qq in range(nglob):
                if inZ[qq]: continue
                x = glob_types[qq]
                if pay(x, z, tunit, tsp, A, selfa) >= uzz - 1e-9:
                    inZ[qq] = True; queue[qn] = qq; qn += 1
        ns = 0
        for tt in range(qn):
            kk = glob_types[queue[tt]]
            if cc_pair(kk, kk, tunit, tsp, A, selfa) > 0.5: ns += 1
        out[i] = 1 if ns == qn else (0 if ns == 0 else -1)
    return out


@njit(cache=True)
def cross_pcc(counts, pres, npres, N, tunit, tsp, A, selfa):
    I = counts.shape[0]
    num = 0.0
    for a in range(I):
        for b in range(I):
            if a == b: continue
            for t1 in range(npres[a]):
                x = pres[a, t1]
                for t2 in range(npres[b]):
                    y = pres[b, t2]
                    num += counts[a, x] * counts[b, y] * cc_pair(x, y, tunit, tsp, A, selfa)
    return num / (N * N * I * (I - 1))


# ---------------------------------------------------------------------------------------------------------------- 3
def own_side_valid(chk, x_term, y_term, V, K):
    """OSV: the C derivation of x's list closes at the root (x, y) with the S hypothesis accepted (no partner
    validation); Run/RunNeg boxes take their real values (IdealCheck)."""
    import lt_cert as C
    v = C.mk_arg(V, x_term, y_term, 'C', K)
    n = C.ID['CHKS']
    Rb = ('cbox', n, v); Sb = ('cbox', n, C.swap_arg(v))
    ok, usesS, _ = chk.vone(0, v, Rb, Sb)
    return bool(ok), bool(usesS)


def spo_table(OSV):
    """SPO[t, s]: valid at some self-root code (>= 25) and at no distinct-quote code (< 25)."""
    selfv = (OSV[:, :, 25:] == 1).any(2)
    nonv = (OSV[:, :, :25] == 1).any(2)
    known = (OSV[:, :, :] >= 0).any(2)
    return selfv & ~nonv & known


@njit(cache=True)
def nonself_closure(Eunits, O, utau, KIND, NAT, CHD, UVt, BLC, BLD, PRODC, PD, APP, reach):
    """Units reachable from the empty units under S-nonself (non-self codes only; the D step at every encounter),
    against every unit of O as partner (rel 0, or 1 for the same unit).  reach: bool over units (in/out)."""
    n = reach.shape[0]
    stack = np.empty(n, np.int64)
    sn = 0
    for e in Eunits:
        if not reach[e]:
            reach[e] = True; stack[sn] = e; sn += 1
    while sn > 0:
        sn -= 1
        u = stack[sn]
        t = utau[u]
        outs = np.empty(len(O) + 1, np.int64)
        no = 0
        outs[no] = u; no += 1
        if BLC[u, 0] < 0:
            for v in O:
                rel = 1 if v == u else 0
                code = KN.sig_code(u, v, rel, utau, KIND, NAT, CHD, UVt, BLC, BLD)
                sid = PRODC[t, code]
                if sid >= 0:
                    u2 = APP[u, sid]
                    if u2 >= 0:
                        outs[no] = u2; no += 1
        for z in range(no):
            u2 = outs[z]
            if BLD[u2, 0] < 0:
                u3 = PD[u2]
                if u3 >= 0 and u3 != u2 and not reach[u3]:
                    reach[u3] = True; stack[sn] = u3; sn += 1
            if not reach[u2]:
                reach[u2] = True; stack[sn] = u2; sn += 1
    return reach


def identity_units(units_set, A, selfa):
    """Identity units of a set: self-cooperating, mutually cooperating with no other unit of the set, twin play D."""
    S = np.array(sorted(units_set), np.int64)
    sub = A[np.ix_(S, S)]
    mutual = (sub == 1) & (sub.T == 1)
    np.fill_diagonal(mutual, False)
    ok = (np.asarray(selfa)[S] == 1) & (~mutual.any(1)) & (np.asarray(A)[S, S] == 0)
    return S[ok]


# ---------------------------------------------------------------------------------------------------------------- 4
class TermState:
    """Mutable per-individual state of a rule at the term level (S-k window, gate cache)."""

    def __init__(self):
        self.window = []          # [(partner body, partner term, script or None, x term at the time)]
        self.wenc = 0
        self.cache = {}           # key -> 'rejected' | 'timeout'
        self.log = []


def term_side(x, y, rule, st, K, V, Pcap, shadow_nonself=None, chk=None):
    """One side's post-play procedure at the term level.  x, y: lt_genes.Prog with mode None (no marker: the quote
    is code + list).  Source = body (structural equality); same quote = equal terms.  Returns (new Prog, events)."""
    import lt_genes as G
    import lt_code as L
    import carrier_populations as CP
    ev = []
    cseq, dseq, anc = list(x.cseq), list(x.dseq), list(x.anc)
    cur = x
    if rule in ('C', 'CS-nonself'):
        cur, acct = G.produce_side(x, y, 'C', K, V, Pcap, K, True, None, rule='lack', ac='full')
        cur = G.Prog(cur.name, cur.body, None, cur.cseq, cur.dseq, cur.anc, cur.tags)
        ev += [('copy',) + tuple(e) for e in acct.events]
        cseq, dseq, anc = list(cur.cseq), list(cur.dseq), list(cur.anc)
    if rule in ('H', 'C'):
        return cur, ev
    same_source = (x.body == y.body)
    yt = y.term()

    def produce(target_prog):
        s, n, oc = G.produce_term(target_prog.term(), yt, 'C', V, K, Pcap, K)
        ev.append(('prodC', oc, n))
        return s

    if rule == 'S-gate+cache':
        key = (y.term(), tuple(cur.cseq), tuple(cur.dseq))
        if key in st.cache:
            ev.append(('hit', st.cache[key]))
        else:
            if cseq:
                g, n = G.check_term(cur.term(), yt, 'C', V, K, K)
                ev.append(('gate', g, n))
            else:
                g = 'F'
            if g != 'T':
                s, n, oc = G.produce_term(cur.term(), yt, 'C', V, K, Pcap, K)
                ev.append(('prodC', oc, n))
                if s is not None and s not in cseq:
                    cseq.append(s); anc.insert(len(cseq) - 1, 'search')
                    st.cache = {}
                    ev.append(('invalidate',))
                else:
                    st.cache[key] = 'timeout' if (g is None or g == 'TO' or oc in ('capTO', 'fuelTO')) else 'rejected'
            cur = G.Prog(cur.name, cur.body, None, cseq, dseq, anc, cur.tags)
    elif not cseq:
        if rule in ('S-self', 'S-nonself', 'S-self-delayed', 'CS-nonself'):
            go = True
            if rule in ('S-nonself', 'CS-nonself'): go = not same_source
            if rule == 'S-self-delayed': go = bool(shadow_nonself)
            if go:
                s = produce(cur)
                if s is not None:
                    cseq.append(s); anc.insert(len(cseq) - 1, 'search')
            else:
                ev.append(('skip',))
        else:
            kk = 2 if rule == 'S-2' else 3
            st.wenc += 1
            if all(w[0] != y.body for w in st.window):
                s = produce(cur)
                st.window.append((y.body, yt, s, cur))
            if len(st.window) >= kk or st.wenc >= WINDOW_DEADLINE:
                chk = chk or CP.IdealCheck()
                keep = None
                first = None
                scores = []
                for c, (_, _, s, xc) in enumerate(st.window):
                    if s is None:
                        scores.append(None); continue
                    sc = 0
                    for (_, pt, _, xm) in st.window:
                        # the root as it was at that encounter: x then (with s appended) against that partner; a
                        # partner that was x's own quote gives the self-play root of the would-be self
                        xm2 = G.Prog(xm.name, xm.body, None, (s,), xm.dseq)
                        selfroot = (pt == xm.term())
                        ok, _ = own_side_valid(chk, xm2.term(), xm2.term() if selfroot else pt, V, K)
                        sc += int(ok)
                    scores.append(sc)
                    if sc >= 1 and first is None:
                        first = s
                    if sc >= 2 and keep is None:
                        keep = s
                ev.append(('window', [None if s is None else 1 for (_, _, s, _) in st.window], scores))
                if keep is None and first is not None and rule != 'S-3 strict':
                    keep = first
                    ev.append(('fallback',))
                st.window = []; st.wenc = 0
                if keep is not None:
                    cseq.append(keep); anc.insert(len(cseq) - 1, 'search')
        cur = G.Prog(cur.name, cur.body, None, cseq, dseq, anc, cur.tags)
    if not dseq:
        s, n, oc = G.produce_term(cur.term(), L.PROG_D, 'D', V, K, Pcap, K)
        ev.append(('prodD', oc, n))
        if s is not None:
            dseq.append(s); anc.append('search')
        cur = G.Prog(cur.name, cur.body, None, cseq, dseq, anc, cur.tags)
    return cur, ev


def term_encounter(x, y, rx, ry, sx, sy, K, V, Pcap, self_play=False, shadow=(None, None), chk=None):
    """Play at fuel K, then each side's rule procedure against the other's pre-encounter quote."""
    import lt_code as L
    ax, _ = L.play(x.term(), y.term(), K)
    ay = ax if self_play else L.play(y.term(), x.term(), K)[0]
    nx, ex = term_side(x, y, rx, sx, K, V, Pcap, shadow[0], chk)
    if self_play:
        ny, ey = nx, ex
    else:
        ny, ey = term_side(y, x, ry, sy, K, V, Pcap, shadow[1], chk)
    return dict(ax=('D' if ax == 'BOT' else ax), ay=('D' if ay == 'BOT' else ay), nx=nx, ny=ny, ex=ex, ey=ey)
