"""The seed-lottery kernel of the fully realizable social organization game (notes/sog-fully-realizable.md §1.8-§1.11).

The realizable run's kernel (sog_realizable.kern3: islands of three slot populations, Moran births with fitness =
expected payoff against the other slots' residents, migration m = mN/N, exact skipping of inactive units) with:
  * executable triple values composed on the fly from per-subject half rows (a worker's probe values and its
    certification values depend on its co-worker only if it reads the co-worker: then the half row is keyed on the
    co-worker), and boss rows keyed on the probe values the boss reads;
  * S-nonself_3 production at encounters (r = N/3 per Moran event, on uniformly chosen islands; islands whose present
    triples are all production no-ops are 'quiet' and their encounters are skipped exactly);
  * counter-based random numbers (every draw a hash of (seed, counter, index)), so that the kernel can stop on a
    table miss before mutating any state and resume deterministically after the driver fills it.
State lives in arrays owned by the driver (sog_full_run.Run); statistics are computed by the driver from per-check
snapshots of island compositions.

Table layout (worker type x, boss type b, local ids), T = (WSP, WT1, WDEP, PHI, PHD, PH_V, PH_C, WHI, WHD, WH_I, WH_CV,
BRI, BRA, B_ACT, B_IDL, B_CV, V, VPLUS, TOCH):
  WSP[x] spelling, WT1[x] is T1, WDEP[x] reads the co-worker (O-atom or live EQ)
  probe half rows: PHI[x, slot] (independent) or PHD[(x, slot, other)]; PH_V[h, 4], PH_C[h, 4]
  worker half rows: WHI[x, slot, bex] or WHD[(x, slot, bex, other)]; WH_I[h, 2] ([C], [D] ideal), WH_CV[h, 2, 4]
  boss rows: BRI[b, ri], ri the restricted index over BRA[b, 3] (read code positions); B_ACT, B_IDL[3], B_CV[3, 9]
PT = (PBI, PB_N, PB_IDX, PB_OWN, PB_MASK, PB_NEW, B_PLAYOWN, B_CALLM, PWD, PW_N, PW_IDX, PW_OWN, PW_MASK, PW_NEW, WPLAY).
"""
import numpy as np
from numba import njit

ST_B, ST_PHASE, ST_G, ST_R, ST_STEP, ST_ECTR, ST_CI, ST_NEXT, ST_NACT, ST_NQ, ST_STATUS, ST_END = range(12)
MISS_PH, MISS_BROW, MISS_WH, MISS_PB, MISS_PW, MISS_TB, MISS_TW = 1, 2, 3, 4, 5, 6, 7
SH = 21
NCTR = 24
CODE_ID = 6561            # 3**8


@njit(cache=True)
def u01(seed, ctr, k):
    z = np.uint64(seed) * np.uint64(0x9E3779B97F4A7C15) + np.uint64(ctr) * np.uint64(0xBF58476D1CE4E5B9) \
        + np.uint64(k) * np.uint64(0x94D049BB133111EB) + np.uint64(0x632BE59BD9B4E019)
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    z = z ^ (z >> np.uint64(31))
    return float(z >> np.uint64(11)) * (1.0 / 9007199254740992.0)


@njit(cache=True)
def pow3(e):
    v = 1
    for _ in range(e):
        v *= 3
    return v


@njit(cache=True)
def chain(b, x, y, T, oi, oc, miss):
    """Composes the executable encounter.  oi = [code int, boss row, -, bex, wex0..wex3, ri, rel]; oc = [bch0..2,
    wch0..3, pcost0..7].  Returns False on a miss (miss filled: kind, keys)."""
    (WSP, WT1, WCLS, READS_EQ, VTR, VK, VA, VC, VOK, VSTEPS, VUSED, VNU, BKA, MCAP, LIVE_EQ,
     PRD, PR_V, PR_C, WCD, WC_V, WC_CV, NROW, CONSTC, CONSTV,
     BCLS, BRI, BRA, B_ACT, B_IDL, B_CV, V, VPLUS, TOCH) = T
    rel = 1 if WSP[x] == WSP[y] else 0
    cx = WCLS[x]; cy = WCLS[y]; cb = BCLS[b]
    pk = (((cx << SH) | cy) << 1) | rel
    if pk in PRD:
        pr = PRD[pk]
    else:
        if NROW[0] >= NROW[1]:
            miss[0] = 8; return False
        pr = NROW[0]
        ov = np.zeros(4, np.int64)
        ocs = np.zeros((4, 4), np.int64)
        for sp in range(2):
            eval_pair(cx, cy, CONSTV[sp, 0], CONSTV[sp, 1], CONSTV[sp, 2], rel, LIVE_EQ, READS_EQ, VTR, VK, VA, VC,
                      VOK, VSTEPS, VUSED, VNU, BKA, MCAP, ov, ocs)
            for k in range(4):
                idx = (k // 2) * 4 + sp * 2 + (k % 2)
                if ov[k] == 2:
                    PR_V[pr, idx] = 2; PR_C[pr, idx] = V + TOCH
                else:
                    tot = ocs[k, 0] + ocs[k, 1] * CONSTC[sp, 0] + ocs[k, 2] * CONSTC[sp, 1] + ocs[k, 3] * CONSTC[sp, 2]
                    if tot > V + VPLUS:
                        PR_V[pr, idx] = 2; PR_C[pr, idx] = V + TOCH
                    else:
                        PR_V[pr, idx] = ov[k]; PR_C[pr, idx] = tot
        PRD[pk] = pr
        NROW[0] = pr + 1
    code = 0
    for k in range(8):
        code += PR_V[pr, k] * pow3(k)
        oc[7 + k] = PR_C[pr, k]
    code += CODE_ID * (WT1[x] + 2 * WT1[y] + 4 * rel)
    ri = 0
    for q in range(3):
        a = BRA[cb, q]
        if a < 0: break
        if a < 8:
            v = (code // pow3(a)) % 3
        else:
            v = ((code // CODE_ID) >> (a - 8)) & 1
        ri += v * pow3(q)
    r = BRI[cb, ri]
    if r < 0:
        miss[0] = 2; miss[1] = b; miss[2] = ri; miss[3] = code; return False
    bex = 0
    for A in range(3):
        idl = B_IDL[r, A]
        if idl == 2:
            e = 2; ch = V + TOCH
        else:
            tot = B_CV[r, A, 0]
            for k in range(8):
                tot += B_CV[r, A, k + 1] * oc[7 + k]
            if tot > V + VPLUS:
                e = 2; ch = V + TOCH
            else:
                e = idl; ch = tot
        bex += e * pow3(A)
        oc[A] = ch
    wk = pk * 27 + bex
    if wk in WCD:
        w = WCD[wk]
    else:
        if NROW[2] >= NROW[3]:
            miss[0] = 8; return False
        w = NROW[2]
        ov = np.zeros(4, np.int64)
        ocs = np.zeros((4, 4), np.int64)
        eval_pair(cx, cy, bex % 3, (bex // 3) % 3, bex // 9, rel, LIVE_EQ, READS_EQ, VTR, VK, VA, VC, VOK, VSTEPS,
                  VUSED, VNU, BKA, MCAP, ov, ocs)
        for k in range(4):
            WC_V[w, k] = ov[k]
            for q in range(4):
                WC_CV[w, k, q] = ocs[k, q]
        WCD[wk] = w
        NROW[2] = w + 1
    for k in range(4):
        idl = WC_V[w, k]
        if idl == 2:
            e = 2; ch = V + TOCH
        else:
            tot = WC_CV[w, k, 0]
            for A in range(3):
                tot += WC_CV[w, k, A + 1] * oc[A]
            if tot > V + VPLUS:
                e = 2; ch = V + TOCH
            else:
                e = idl; ch = tot
        oi[4 + k] = e
        oc[3 + k] = ch
    oi[0] = code; oi[1] = r; oi[3] = bex; oi[8] = ri; oi[9] = rel
    return True


@njit(cache=True)
def wbits(bex, oS, oW, eq):
    b0 = 1 if (bex % 3) == 1 else 0
    b1 = 1 if ((bex // 3) % 3) == 1 else 0
    b2 = 1 if ((bex // 9) % 3) == 1 else 0
    return b0 | (b1 << 1) | (b2 << 2) | (oS << 3) | (oW << 4) | (eq << 5)


@njit(cache=True)
def jcode(b, x, y, T, WACT, LIVE_EQ, oi, oc, miss):
    if not chain(b, x, y, T, oi, oc, miss):
        return -1
    B_ACT = T[27]
    WCLS = T[2]
    eq = 1 if (oi[9] == 1 and LIVE_EQ == 1) else 0
    bex = oi[3]
    a1 = WACT[WCLS[x], wbits(bex, 1 if oi[7] == 1 else 0, 1 if oi[6] == 1 else 0, eq)]
    a2 = WACT[WCLS[y], wbits(bex, 1 if oi[5] == 1 else 0, 1 if oi[4] == 1 else 0, eq)]
    return 4 * B_ACT[oi[1]] + 2 * a1 + a2


@njit(cache=True)
def jtag(b, x, y, T, WACT, TAG, LIVE_EQ, oi, oc, miss):
    """4 * joint code + 2 * tag(x) + tag(y), or -1 on a miss."""
    j = jcode(b, x, y, T, WACT, LIVE_EQ, oi, oc, miss)
    if j < 0:
        return -1
    WCLS = T[2]
    return 4 * j + 2 * TAG[WCLS[x]] + TAG[WCLS[y]]


@njit(cache=True)
def payq(JQ, PAYF, i, s, pk, pp, pq):
    """Payoff to slot s at positions (pk in slot s; pp, pq in the other slots in slot order) from the cube."""
    if s == 0:
        return PAYF[JQ[i, pk, pp, pq], 0]
    if s == 1:
        return PAYF[JQ[i, pp, pk, pq], 1]
    return PAYF[JQ[i, pp, pq, pk], 2]


@njit(cache=True)
def others(s):
    if s == 0:
        return 1, 2
    if s == 1:
        return 0, 2
    return 0, 1


@njit(cache=True)
def setact(u, a, act, apos, st):
    nact = st[ST_NACT]
    pp = apos[u]
    if a and pp >= nact:
        j = act[nact]; act[nact] = u; act[pp] = j; apos[u] = nact; apos[j] = pp; nact += 1
    elif (not a) and pp < nact:
        nact -= 1; j = act[nact]; act[nact] = u; act[pp] = j; apos[u] = nact; apos[j] = pp
    st[ST_NACT] = nact


@njit(cache=True)
def precheck_multi(i, newt, counts, pres, npres, T, WACT, TAG, LIVE_EQ, oi, oc, miss, scr):
    """Every triple of island i's present types plus the new types newt[s] (-1 none) that contains a new type.  When
    exactly one slot has a new type the cube codes of its slice are left in scr (replace copies them)."""
    nnew = 0
    for s in range(3):
        if newt[s] >= 0: nnew += 1
    for s in range(3):
        if newt[s] < 0: continue
        o1, o2 = others(s)
        n1 = npres[i, o1] + (1 if newt[o1] >= 0 else 0)
        n2 = npres[i, o2] + (1 if newt[o2] >= 0 else 0)
        for t1 in range(n1):
            p = pres[i, o1, t1] if t1 < npres[i, o1] else newt[o1]
            for t2 in range(n2):
                q = pres[i, o2, t2] if t2 < npres[i, o2] else newt[o2]
                if s == 0:
                    b = newt[0]; x = p; y = q
                elif s == 1:
                    b = p; x = newt[1]; y = q
                else:
                    b = p; x = q; y = newt[2]
                c = jtag(b, x, y, T, WACT, TAG, LIVE_EQ, oi, oc, miss)
                if c < 0:
                    return False
                if nnew == 1:
                    scr[t1, t2] = c
    return True


@njit(cache=True)
def fit_full(i, s, k, counts, pres, npres, pos, JQ, PAYF):
    o1, o2 = others(s)
    pk = pos[i, s, k]
    v = 0.0
    for t1 in range(npres[i, o1]):
        p = pres[i, o1, t1]
        for t2 in range(npres[i, o2]):
            q = pres[i, o2, t2]
            v += counts[i, o1, p] * counts[i, o2, q] * payq(JQ, PAYF, i, s, pk, t1, t2)
    return v


@njit(cache=True)
def cube_slice(i, s, pk, k, pres, npres, JQ, T, WACT, TAG, LIVE_EQ, oi, oc, miss):
    """Fill the cube's slice of type k at position pk of slot s against every present position of the other slots."""
    o1, o2 = others(s)
    for t1 in range(npres[i, o1]):
        p = pres[i, o1, t1]
        for t2 in range(npres[i, o2]):
            q = pres[i, o2, t2]
            if s == 0:
                c = jtag(k, p, q, T, WACT, TAG, LIVE_EQ, oi, oc, miss)
                JQ[i, pk, t1, t2] = c
            elif s == 1:
                c = jtag(p, k, q, T, WACT, TAG, LIVE_EQ, oi, oc, miss)
                JQ[i, t1, pk, t2] = c
            else:
                c = jtag(p, q, k, T, WACT, TAG, LIVE_EQ, oi, oc, miss)
                JQ[i, t1, t2, pk] = c


@njit(cache=True)
def replace(i, s, old, new, counts, pres, npres, pos, F, JQ, PAYF, T, WACT, TAG, LIVE_EQ, oi, oc, miss, scr, scr_ok):
    """One individual of type old in slot s of island i becomes type new; the cube and the fitness are updated
    (sog_realizable.kern3's incremental update).  The caller has prechecked every table entry the new type needs."""
    isnew = counts[i, s, new] == 0
    if isnew:
        pn = npres[i, s]
        pres[i, s, pn] = new; pos[i, s, new] = pn; npres[i, s] = pn + 1
        if scr_ok == 1:
            o1, o2 = others(s)
            for t1 in range(npres[i, o1]):
                for t2 in range(npres[i, o2]):
                    if s == 0:
                        JQ[i, pn, t1, t2] = scr[t1, t2]
                    elif s == 1:
                        JQ[i, t1, pn, t2] = scr[t1, t2]
                    else:
                        JQ[i, t1, t2, pn] = scr[t1, t2]
        else:
            cube_slice(i, s, pn, new, pres, npres, JQ, T, WACT, TAG, LIVE_EQ, oi, oc, miss)
    pnew = pos[i, s, new]; pold = pos[i, s, old]
    o1, o2 = others(s)
    for sa in (o1, o2):
        sb = o1 + o2 - sa
        for ta in range(npres[i, sa]):
            k = pres[i, sa, ta]
            v = 0.0
            for tb in range(npres[i, sb]):
                q = pres[i, sb, tb]
                # positions in slot order for the payoff to slot sa: the two others are s and sb
                if s < sb:
                    v += counts[i, sb, q] * (payq(JQ, PAYF, i, sa, ta, pnew, tb) - payq(JQ, PAYF, i, sa, ta, pold, tb))
                else:
                    v += counts[i, sb, q] * (payq(JQ, PAYF, i, sa, ta, tb, pnew) - payq(JQ, PAYF, i, sa, ta, tb, pold))
            F[i, sa, k] += v
    counts[i, s, new] += 1
    counts[i, s, old] -= 1
    if counts[i, s, old] == 0:
        pp = pold
        last_pos = npres[i, s] - 1
        last = pres[i, s, last_pos]
        if pp != last_pos:
            if s == 0:
                JQ[i, pp, :, :] = JQ[i, last_pos, :, :]
            elif s == 1:
                JQ[i, :, pp, :] = JQ[i, :, last_pos, :]
            else:
                JQ[i, :, :, pp] = JQ[i, :, :, last_pos]
        pres[i, s, pp] = last; pos[i, s, last] = pp; pos[i, s, old] = -1; npres[i, s] = last_pos
    if isnew:
        F[i, s, new] = fit_full(i, s, new, counts, pres, npres, pos, JQ, PAYF)


@njit(cache=True)
def parent(F, counts, pres, npres, i, s, N2, w, uu):
    m = -1e300
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        f = F[i, s, k] / N2
        if f > m: m = f
    tot = 0.0
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        tot += counts[i, s, k] * np.exp(w * (F[i, s, k] / N2 - m))
    u = uu * tot; acc = 0.0
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        acc += counts[i, s, k] * np.exp(w * (F[i, s, k] / N2 - m))
        if u <= acc:
            return k
    return pres[i, s, npres[i, s] - 1]


@njit(cache=True)
def pick(counts, pres, npres, i, s, N, uu):
    r = int(uu * N); acc = 0
    for t in range(npres[i, s]):
        k = pres[i, s, t]; acc += counts[i, s, k]
        if r < acc:
            return k
    return pres[i, s, npres[i, s] - 1]


@njit(cache=True)
def prod_boss(b, oi, oc, PT, K, P, VPLUS, PW_, ctr, miss, apply_stats):
    """S-nonself_3 production of boss b at the composed encounter: the new type (b if unchanged), -1 on a miss."""
    (PBI, PB_N, PB_IDX, PB_OWN, PB_MASK, PB_NEW, B_PLAYOWN, B_CALLM, PWD, PW_N, PW_IDX, PW_OWN, PW_MASK, PW_NEW,
     WPLAY, BCLS, BSP, WCLS, WSP, TYPB, TYPW, GATE) = PT
    r = oi[1]; ri = oi[8]
    cb = BCLS[b]
    row = PBI[cb, ri]
    if row < 0:
        miss[0] = 4; miss[1] = b; miss[2] = ri; miss[3] = oi[0]; return -1
    n = PB_N[row]
    if n == 0:
        return b
    play = B_PLAYOWN[r]
    for k in range(8):
        play += B_CALLM[r, k] * oc[7 + k]
    rem = K - play
    pat = 0
    for a in range(n):
        req = PB_OWN[row, a]
        m = PB_MASK[row, a]
        for k in range(8):
            if (m >> k) & 1:
                req += oc[7 + k]
        if apply_stats: ctr[1] += 1
        if rem <= 0:
            if apply_stats: ctr[5] += 1
            continue
        if req - PW_ > P + VPLUS:
            ch = P + VPLUS + PW_
            if ch > rem:
                rem = 0
                if apply_stats: ctr[5] += 1
                continue
            rem -= ch
            if apply_stats:
                ctr[4] += 1; ctr[17] += ch
            continue
        if req > rem:
            rem = 0
            if apply_stats: ctr[5] += 1
            continue
        rem -= req
        if apply_stats: ctr[17] += req
        if PB_IDX[row, a] < 0:
            if apply_stats: ctr[3] += 1
            continue
        pat |= (1 << a)
        if apply_stats: ctr[2] += 1
    nc = PB_NEW[row, pat]
    if nc == cb:
        return b
    key = (BSP[b] << SH) | nc
    if key in TYPB:
        return TYPB[key]
    miss[0] = 6; miss[1] = BSP[b]; miss[2] = nc; return -1


@njit(cache=True)
def prod_worker(x, j, oi, oc, PT, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, apply_stats):
    (PBI, PB_N, PB_IDX, PB_OWN, PB_MASK, PB_NEW, B_PLAYOWN, B_CALLM, PWD, PW_N, PW_IDX, PW_OWN, PW_MASK, PW_NEW,
     WPLAY, BCLS, BSP, WCLS, WSP, TYPB, TYPW, GATE) = PT
    bex = oi[3]
    cx = WCLS[x]
    if j == 1:
        oC = oi[6]; oD = oi[7]; cC = oc[5]; cD = oc[6]
    else:
        oC = oi[4]; oD = oi[5]; cC = oc[3]; cD = oc[4]
    rel = oi[9]
    if rel == 1 and GATE == 1:
        if apply_stats: ctr[11] += 1
        return x
    oex = oC + 3 * oD
    key = ((((cx * 2 + (j - 1)) * 27 + bex) * 9 + oex) * 2 + rel)
    if key in PWD:
        row = PWD[key]
    else:
        miss[0] = 5; miss[1] = x; miss[2] = j; miss[3] = bex; miss[4] = oex; miss[5] = rel; return -1
    n = PW_N[row]
    if n == 0:
        return x
    eq = 1 if (rel == 1 and LIVE_EQ == 1) else 0
    bits = wbits(bex, 1 if oD == 1 else 0, 1 if oC == 1 else 0, eq)
    c0 = oc[0]; c1 = oc[1]; c2 = oc[2]
    play = WPLAY[cx, bits, 0] + WPLAY[cx, bits, 1] * c0 + WPLAY[cx, bits, 2] * c1 + WPLAY[cx, bits, 3] * c2 \
        + WPLAY[cx, bits, 4] * cC + WPLAY[cx, bits, 5] * cD
    rem = K - play
    pat = 0
    for a in range(n):
        req = PW_OWN[row, a]
        mm = PW_MASK[row, a]
        if mm & 1: req += c0
        if mm & 2: req += c1
        if mm & 4: req += c2
        if mm & 8: req += cC
        if mm & 16: req += cD
        if apply_stats: ctr[6] += 1
        if rem <= 0:
            if apply_stats: ctr[10] += 1
            continue
        if req - PW_ > P + VPLUS:
            ch = P + VPLUS + PW_
            if ch > rem:
                rem = 0
                if apply_stats: ctr[10] += 1
                continue
            rem -= ch
            if apply_stats:
                ctr[9] += 1; ctr[18] += ch
            continue
        if req > rem:
            rem = 0
            if apply_stats: ctr[10] += 1
            continue
        rem -= req
        if apply_stats: ctr[18] += req
        if PW_IDX[row, a] < 0:
            if apply_stats: ctr[8] += 1
            continue
        pat |= (1 << a)
        if apply_stats: ctr[7] += 1
    nc = PW_NEW[row, pat]
    if nc == cx:
        return x
    key = (WSP[x] << SH) | nc
    if key in TYPW:
        return TYPW[key]
    miss[0] = 7; miss[1] = WSP[x]; miss[2] = nc; return -1


@njit(cache=True)
def mark_dirty(i, quiet, nqlist, nqpos, st):
    if quiet[i] == 1:
        nq = st[ST_NQ]
        nqlist[nq] = i; nqpos[i] = nq; st[ST_NQ] = nq + 1
    quiet[i] = -1


@njit(cache=True)
def unmark(i, quiet, nqlist, nqpos, st):
    nq = st[ST_NQ]
    pp = nqpos[i]
    last = nqlist[nq - 1]
    nqlist[pp] = last; nqpos[last] = pp
    nqpos[i] = -1
    st[ST_NQ] = nq - 1
    quiet[i] = 1


@njit(cache=True)
def productions(bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc, newt, apply_stats):
    """Composes the encounter and its productions; newt[s] = new type or -1.  False on a miss."""
    if not chain(bb, xx, yy, T, oi, oc, miss):
        return False
    newt[0] = -1; newt[1] = -1; newt[2] = -1
    WCLS = T[2]; BCLS = T[24]
    if BLACK[BCLS[bb]] != 0:
        nb = prod_boss(bb, oi, oc, PT, K, P, VPLUS, PW_, ctr, miss, apply_stats)
        if nb < 0: return False
        if nb != bb: newt[0] = nb
    if WLACK[WCLS[xx]] != 0:
        nx = prod_worker(xx, 1, oi, oc, PT, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, apply_stats)
        if nx < 0: return False
        if nx != xx: newt[1] = nx
    if WLACK[WCLS[yy]] != 0:
        ny = prod_worker(yy, 2, oi, oc, PT, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, apply_stats)
        if ny < 0: return False
        if ny != yy: newt[2] = ny
    return True


@njit(cache=True)
def misskey(miss):
    h = miss[0]
    for q in range(1, 6):
        h = h * 1000003 + miss[q]
    return h


@njit(cache=True)
def quiet_check(i, npres, pres, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc, newt, mbuf, st):
    """1 quiet, 0 not quiet, -1 misses (every miss met is appended to mbuf; st[ST_STATUS] counts them)."""
    nm0 = st[ST_STATUS]
    quiet = 1
    seen = dict()
    seen[-1] = 0
    for ta in range(npres[i, 0]):
        bb = pres[i, 0, ta]
        for tb in range(npres[i, 1]):
            xx = pres[i, 1, tb]
            for tc in range(npres[i, 2]):
                yy = pres[i, 2, tc]
                if BLACK[T[24][bb]] == 0 and WLACK[T[2][xx]] == 0 and WLACK[T[2][yy]] == 0:
                    continue
                if not productions(bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc,
                                   newt, False):
                    hk = misskey(miss)
                    if hk in seen:
                        continue
                    seen[hk] = 1
                    n = st[ST_STATUS]
                    if n < mbuf.shape[0]:
                        for q in range(6): mbuf[n, q] = miss[q]
                        st[ST_STATUS] = n + 1
                    if miss[0] == 8:
                        return -1
                    continue
                if newt[0] >= 0 or newt[1] >= 0 or newt[2] >= 0:
                    quiet = 0
    if st[ST_STATUS] > nm0:
        return -1
    return quiet


@njit(cache=True)
def collect_prod_missing(I, npres, pres, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, mbuf, st):
    """Every missing table entry (boss rows, production rows, new types) met by the productions of the present
    triples of every island; appended to mbuf (st[ST_STATUS] counts).  Returns the count of misses met."""
    oi = np.zeros(10, np.int64)
    oc = np.zeros(15, np.int64)
    miss = np.zeros(8, np.int64)
    newt = np.full(3, -1, np.int64)
    ctr = np.zeros(NCTR, np.int64)
    tot = 0
    seen = dict()
    seen[-1] = 0
    for i in range(I):
        for ta in range(npres[i, 0]):
            bb = pres[i, 0, ta]
            for tb in range(npres[i, 1]):
                xx = pres[i, 1, tb]
                for tc in range(npres[i, 2]):
                    yy = pres[i, 2, tc]
                    if BLACK[T[24][bb]] == 0 and WLACK[T[2][xx]] == 0 and WLACK[T[2][yy]] == 0:
                        continue
                    if not productions(bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc,
                                       newt, False):
                        tot += 1
                        hk = misskey(miss)
                        if hk in seen:
                            continue
                        seen[hk] = 1
                        n = st[ST_STATUS]
                        if n < mbuf.shape[0]:
                            for q in range(6): mbuf[n, q] = miss[q]
                            st[ST_STATUS] = n + 1
                        if miss[0] == 8:
                            return tot
    return tot


@njit(cache=True)
def collect_island(i, newt, npres, pres, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, MODE_S, mbuf, st):
    """Every missing table entry of island i's triples (present types plus newt), compositions and (S) productions,
    deduplicated into mbuf (st[ST_STATUS] counts)."""
    oi = np.zeros(10, np.int64)
    oc = np.zeros(15, np.int64)
    miss = np.zeros(8, np.int64)
    nw = np.full(3, -1, np.int64)
    ctr = np.zeros(NCTR, np.int64)
    seen = dict()
    seen[-1] = 0
    n0 = npres[i, 0] + (1 if newt[0] >= 0 else 0)
    n1 = npres[i, 1] + (1 if newt[1] >= 0 else 0)
    n2 = npres[i, 2] + (1 if newt[2] >= 0 else 0)
    for ta in range(n0):
        bb = pres[i, 0, ta] if ta < npres[i, 0] else newt[0]
        for tb in range(n1):
            xx = pres[i, 1, tb] if tb < npres[i, 1] else newt[1]
            for tc in range(n2):
                yy = pres[i, 2, tc] if tc < npres[i, 2] else newt[2]
                ok = chain(bb, xx, yy, T, oi, oc, miss)
                if ok and MODE_S == 1:
                    ok = productions(bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc,
                                     nw, False)
                if not ok:
                    hk = misskey(miss)
                    if hk in seen:
                        continue
                    seen[hk] = 1
                    n = st[ST_STATUS]
                    if n < mbuf.shape[0]:
                        for q in range(6): mbuf[n, q] = miss[q]
                        st[ST_STATUS] = n + 1
                    if miss[0] == 8:
                        return


@njit(cache=True)
def collect_precheck(i, newt, npres, pres, T, mbuf, st):
    """Every missing composition entry of the triples precheck_multi needs (those containing a new type)."""
    oi = np.zeros(10, np.int64)
    oc = np.zeros(15, np.int64)
    miss = np.zeros(8, np.int64)
    seen = dict()
    seen[-1] = 0
    for s in range(3):
        if newt[s] < 0: continue
        o1, o2 = others(s)
        n1 = npres[i, o1] + (1 if newt[o1] >= 0 else 0)
        n2 = npres[i, o2] + (1 if newt[o2] >= 0 else 0)
        for t1 in range(n1):
            p = pres[i, o1, t1] if t1 < npres[i, o1] else newt[o1]
            for t2 in range(n2):
                q = pres[i, o2, t2] if t2 < npres[i, o2] else newt[o2]
                if s == 0:
                    b = newt[0]; x = p; y = q
                elif s == 1:
                    b = p; x = newt[1]; y = q
                else:
                    b = p; x = q; y = newt[2]
                if not chain(b, x, y, T, oi, oc, miss):
                    hk = misskey(miss)
                    if hk in seen:
                        continue
                    seen[hk] = 1
                    n = st[ST_STATUS]
                    if n < mbuf.shape[0]:
                        for q2 in range(6): mbuf[n, q2] = miss[q2]
                        st[ST_STATUS] = n + 1
                    if miss[0] == 8:
                        return


@njit(cache=True)
def run_kernel(st, seed, I, N, w, m, r_enc, checks, K, P, LIVE_EQ, MODE_S, QMAX, PW_,
               counts, pres, npres, pos, F, act, apos, quiet, nqlist, nqpos,
               T, PT, WACT, TAG, BLACK, WLACK, JQ, PAYF, ctr, miss, snap_t, snap_c, snap_n, maxiter, mbuf):
    """Resumable kernel; returns 0 done, 2 miss (miss filled), 5 iteration budget used (state consistent)."""
    V = T[30]; VPLUS = T[31]
    NU = 3 * I
    UN = NU * N
    nchk = len(checks)
    N2 = float(N) * N
    mm = m if I > 1 else 0.0
    oi = np.zeros(10, np.int64)
    oc = np.zeros(15, np.int64)
    newt = np.full(3, -1, np.int64)
    scr = np.zeros((N + 2, N + 2), np.uint8)
    seed2 = seed + 7919
    it = 0
    while True:
        it += 1
        if it > maxiter:
            return 5
        ph = st[ST_PHASE]
        if ph == 0:
            b = st[ST_B]
            nact = st[ST_NACT]
            pa = (nact + (NU - nact) * mm) / NU
            if pa <= 0.0:
                G = 1 << 60
            elif pa >= 1.0:
                G = 0
            else:
                uu = u01(seed, st[ST_STEP], 0)
                G = int(np.log(1.0 - uu) / np.log(1.0 - pa))
            nextb = checks[st[ST_CI]] * UN
            if b + G >= nextb:
                stretch = nextb - b
                st[ST_END] = 1
            else:
                stretch = G + 1
                st[ST_END] = 0
            st[ST_G] = G
            R = 0
            if MODE_S == 1:
                x = stretch * r_enc
                R = int(x)
                if u01(seed, st[ST_STEP], 1) < x - R:
                    R += 1
            st[ST_R] = R
            st[ST_PHASE] = 1 if MODE_S == 1 else 2
            continue
        if ph == 1:
            k = 0
            while k < st[ST_NQ]:
                i = nqlist[k]
                if quiet[i] == -1:
                    if npres[i, 0] * npres[i, 1] * npres[i, 2] <= QMAX:
                        ctr[14] += 1
                        q = quiet_check(i, npres, pres, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss,
                                        oi, oc, newt, mbuf, st)
                        if q < 0:
                            return 4
                        if q == 1:
                            unmark(i, quiet, nqlist, nqpos, st)
                            continue
                    quiet[i] = 0
                k += 1
            R = st[ST_R]
            brk = False
            while R > 0 and st[ST_NQ] > 0:
                ec = st[ST_ECTR]
                pnq = st[ST_NQ] / I
                if pnq >= 1.0:
                    skip = 0
                else:
                    uu = u01(seed2, ec, 0)
                    skip = int(np.log(1.0 - uu) / np.log(1.0 - pnq))
                if skip >= R:
                    R = 0
                    break
                i = nqlist[min(int(u01(seed2, ec, 1) * st[ST_NQ]), st[ST_NQ] - 1)]
                bb = pick(counts, pres, npres, i, 0, N, u01(seed2, ec, 2))
                xx = pick(counts, pres, npres, i, 1, N, u01(seed2, ec, 3))
                yy = pick(counts, pres, npres, i, 2, N, u01(seed2, ec, 4))
                if not productions(bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc,
                                   newt, False):
                    return 2
                nnew = 0
                for s in range(3):
                    if newt[s] >= 0: nnew += 1
                if nnew > 0:
                    if not precheck_multi(i, newt, counts, pres, npres, T, WACT, TAG, LIVE_EQ, oi, oc, miss, scr):
                        collect_precheck(i, newt, npres, pres, T, mbuf, st)
                        return 4
                ctr[0] += 1
                productions(bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc, newt, True)
                changed = False
                for s in range(3):
                    if newt[s] >= 0:
                        old = bb if s == 0 else (xx if s == 1 else yy)
                        replace(i, s, old, newt[s], counts, pres, npres, pos, F, JQ, PAYF, T, WACT, TAG, LIVE_EQ, oi, oc,
                                miss, scr, 1 if nnew == 1 else 0)
                        if s == 0:
                            ctr[12] += 1
                        else:
                            ctr[13] += 1
                        changed = True
                R -= skip + 1
                st[ST_R] = R
                st[ST_ECTR] = ec + 1
                if changed:
                    for s in range(3):
                        setact(3 * i + s, npres[i, s] > 1, act, apos, st)
                    mark_dirty(i, quiet, nqlist, nqpos, st)
                    brk = True
                    break
            if brk and R > 0:
                continue
            st[ST_R] = 0
            st[ST_PHASE] = 2
            continue
        if st[ST_END] == 1:
            ci = st[ST_CI]
            st[ST_B] = checks[ci] * UN
            for i in range(I):
                for s in range(3):
                    snap_n[ci + 1, i, s] = npres[i, s]
                    for t in range(npres[i, s]):
                        kk = pres[i, s, t]
                        snap_t[ci + 1, i, s, t] = kk
                        snap_c[ci + 1, i, s, t] = counts[i, s, kk]
            st[ST_CI] = ci + 1
            st[ST_PHASE] = 0
            st[ST_STEP] += 1
            if ci + 1 >= nchk:
                return 0
            continue
        stp = st[ST_STEP]
        nact = st[ST_NACT]
        pa = (nact + (NU - nact) * mm) / NU
        if u01(seed, stp, 2) * pa * NU < nact:
            u = act[min(int(u01(seed, stp, 3) * nact), nact - 1)]
            mig = mm > 0.0 and u01(seed, stp, 4) < mm
        else:
            u = act[nact + min(int(u01(seed, stp, 3) * (NU - nact)), NU - nact - 1)]
            mig = True
        i = u // 3; s = u % 3
        src = i
        if mig:
            src = min(int(u01(seed, stp, 5) * (I - 1)), I - 2)
            if src >= i: src += 1
        child = parent(F, counts, pres, npres, src, s, N2, w, u01(seed, stp, 6))
        victim = pick(counts, pres, npres, i, s, N, u01(seed, stp, 7))
        if victim != child:
            if counts[i, s, child] == 0:
                newt[0] = -1; newt[1] = -1; newt[2] = -1
                newt[s] = child
                if not precheck_multi(i, newt, counts, pres, npres, T, WACT, TAG, LIVE_EQ, oi, oc, miss, scr):
                    collect_precheck(i, newt, npres, pres, T, mbuf, st)
                    return 4
                mark_dirty(i, quiet, nqlist, nqpos, st)
            replace(i, s, victim, child, counts, pres, npres, pos, F, JQ, PAYF, T, WACT, TAG, LIVE_EQ, oi, oc, miss,
                    scr, 1)
            if counts[i, s, victim] == 0:
                mark_dirty(i, quiet, nqlist, nqpos, st)
            setact(u, npres[i, s] > 1, act, apos, st)
            if mig: ctr[15] += 1
        ctr[16] += 1
        st[ST_B] = st[ST_B] + st[ST_G] + 1
        st[ST_STEP] = stp + 1
        st[ST_PHASE] = 0


@njit(cache=True)
def collect_missing(I, npres, pres, T, out, cap):
    """Boss-row misses met by the present triples of every island, deduplicated by (boss class, restricted index):
    out[k] = (kind, boss type, ri, code).  Pair rows are computed inline.  A capacity miss stops the pass (returns
    -1)."""
    oi = np.zeros(10, np.int64)
    oc = np.zeros(15, np.int64)
    miss = np.zeros(8, np.int64)
    BCLS = T[24]
    seen = dict()
    seen[-1] = 0
    n = 0
    for i in range(I):
        for ta in range(npres[i, 0]):
            bb = pres[i, 0, ta]
            for tb in range(npres[i, 1]):
                xx = pres[i, 1, tb]
                for tc in range(npres[i, 2]):
                    yy = pres[i, 2, tc]
                    if not chain(bb, xx, yy, T, oi, oc, miss):
                        if miss[0] == 8:
                            return -1
                        key = BCLS[miss[1]] * 64 + miss[2]
                        if key in seen:
                            continue
                        seen[key] = 1
                        if n < cap:
                            for q in range(6): out[n, q] = miss[q]
                        n += 1
    return n


@njit(cache=True)
def init_cube_F(I, counts, pres, npres, pos, F, JQ, PAYF, T, WACT, TAG, LIVE_EQ):
    oi = np.zeros(10, np.int64)
    oc = np.zeros(15, np.int64)
    miss = np.zeros(8, np.int64)
    for i in range(I):
        for t0 in range(npres[i, 0]):
            cube_slice(i, 0, t0, pres[i, 0, t0], pres, npres, JQ, T, WACT, TAG, LIVE_EQ, oi, oc, miss)
        for s in range(3):
            for t in range(npres[i, s]):
                k = pres[i, s, t]
                F[i, s, k] = fit_full(i, s, k, counts, pres, npres, pos, JQ, PAYF)
    return miss[0]


@njit(cache=True)
def comp_dist(types0, counts0, n0, types1, counts1, n1, types2, counts2, n2, T, WACT, TAG, LIVE_EQ, out):
    """out[j, t1, t2] += probability of joint code j with tags for one island composition (one uniform member per
    slot).  Returns False on a miss."""
    oi = np.zeros(10, np.int64)
    oc = np.zeros(15, np.int64)
    miss = np.zeros(8, np.int64)
    s0 = 0.0
    for t in range(n0): s0 += counts0[t]
    s1 = 0.0
    for t in range(n1): s1 += counts1[t]
    s2 = 0.0
    for t in range(n2): s2 += counts2[t]
    for ta in range(n0):
        for tb in range(n1):
            for tc in range(n2):
                j = jcode(types0[ta], types1[tb], types2[tc], T, WACT, LIVE_EQ, oi, oc, miss)
                if j < 0:
                    return False
                out[j, TAG[T[2][types1[tb]]], TAG[T[2][types2[tc]]]] += counts0[ta] * counts1[tb] * counts2[tc] / (s0 * s1 * s2)
    return True


# ----------------------------------------------------------------------------------------------------------------
# the worker-pair evaluator (numba port of AbsEval4 on E-encounters: four certification checks with ExactHost regress
# semantics, the uniform-cost closure and cost vectors (base, multiplicities of the three boss boxes)), driven by the
# validation decision tables built in Python (sog_full.build_vt)
# ----------------------------------------------------------------------------------------------------------------
ABORT = -9


@njit(cache=True)
def pcheck(k, cx, cy, bv, rel, liveEQ, READS_EQ, VTR, VK, VA, VC, VOK, VSTEPS, VUSED, VNU, BK, MCAP,
           mval, mdep, mcost, ctx):
    """ctx = [depth, stack mask, dstack accumulators by depth ...].  Returns 0 F, 1 T, 2 TO (at depth 0 only), or
    ABORT (inside a check)."""
    depth = ctx[0]
    if mval[k] >= 0:
        if depth > 0:
            if mval[k] == 2:
                return ABORT
            if (mdep[k] & ctx[1]) != 0:
                return ABORT
            ctx[2 + depth - 1] |= mdep[k] | (1 << k)
        return mval[k]
    if (ctx[1] & (1 << k)) != 0:
        return ABORT
    ctx[2 + depth] = 0
    ctx[0] = depth + 1
    ctx[1] |= (1 << k)
    cost = np.zeros(4, np.int64)
    todo = np.empty(32, np.int64)
    nt = 0
    done = np.empty(16, np.int64)
    nd = 0
    bk = 0
    kk = k
    first = True
    res = -1
    while True:
        s = kk // 2
        a = kk % 2
        c = cx if s == 0 else cy
        eqb = 1 if (rel == 1 and liveEQ == 1 and READS_EQ[c] == 1) else 0
        node = VTR[c, s, a, eqb]
        ab = False
        while VK[node] == 0:
            at = VA[node]
            if at < 3:
                v = bv[at]
                cost[1 + at] += 1
                if v == 2:
                    ab = True
                    break
            else:
                ok2 = (1 - s) * 2 + (0 if at == 3 else 1)
                v = pcheck(ok2, cx, cy, bv, rel, liveEQ, READS_EQ, VTR, VK, VA, VC, VOK, VSTEPS, VUSED, VNU, BK, MCAP,
                           mval, mdep, mcost, ctx)
                if v < 0 or v == 2:
                    ab = True
                    break
                for q in range(4):
                    cost[q] += mcost[ok2, q]
            node = VC[node, v]
        if ab:
            res = ABORT
            break
        cost[0] += VSTEPS[node]
        nu = VNU[node]
        if first:
            first = False
            if VOK[node] == 0:
                cost[0] += BK[0]                  # F0
                res = 0
                break
            done[0] = k
            nd = 1
            for q in range(nu):
                at = VUSED[node, q]
                todo[nt] = (1 - s) * 2 + (0 if at == 3 else 1)
                nt += 1
        else:
            if VOK[node] == 0:
                bk += BK[7] + BK[8] * nd          # fail, fail_cnt
                cost[0] += BK[2] + bk             # F1
                res = 0
                break
            bk += BK[4] + BK[5] * nd + BK[6] * nu  # ins, ins_cnt, ins_len
            for q in range(nt - 1, -1, -1):
                todo[q + nu] = todo[q]
            for q in range(nu):
                at = VUSED[node, q]
                todo[q] = (1 - s) * 2 + (0 if at == 3 else 1)
            nt += nu
            done[nd] = kk
            nd += 1
        nxt = -1
        capped = False
        while nt > 0:
            y = todo[0]
            for q in range(nt - 1):
                todo[q] = todo[q + 1]
            nt -= 1
            isdone = False
            for q in range(nd):
                if done[q] == y:
                    isdone = True
                    break
            if isdone:
                bk += BK[3]                       # hit
                continue
            if nd >= MCAP:
                bk += BK[9]                       # cap
                capped = True
                break
            nxt = y
            break
        if capped:
            cost[0] += BK[2] + bk
            res = 0
            break
        if nxt < 0:
            cost[0] += BK[1] + bk                 # T0
            res = 1
            break
        kk = nxt
    ctx[0] = depth
    ctx[1] &= ~(1 << k)
    d = ctx[2 + depth]
    if res == ABORT:
        if depth > 0:
            return ABORT
        mval[k] = 2
        mdep[k] = 0
        for q in range(4):
            mcost[k, q] = -1
        return 2
    mval[k] = res
    mdep[k] = d
    for q in range(4):
        mcost[k, q] = cost[q]
    if depth > 0:
        ctx[2 + depth - 1] |= d | (1 << k)
    return res


@njit(cache=True)
def eval_pair(cx, cy, b0, b1, b2, rel, liveEQ, READS_EQ, VTR, VK, VA, VC, VOK, VSTEPS, VUSED, VNU, BK, MCAP,
              out_val, out_cost):
    """The four certification checks of a worker pair (x slot 1 class cx, y slot 2 class cy) beside boss boxes with
    values (b0, b1, b2) (0 F, 1 T, 2 TO): out_val[k] (0, 1, 2), out_cost[k] = (base, mult of the 3 boss boxes) or -1."""
    bv = np.empty(3, np.int64)
    bv[0] = b0; bv[1] = b1; bv[2] = b2
    mval = np.full(4, -1, np.int64)
    mdep = np.zeros(4, np.int64)
    mcost = np.zeros((4, 4), np.int64)
    ctx = np.zeros(12, np.int64)
    for k in range(4):
        pcheck(k, cx, cy, bv, rel, liveEQ, READS_EQ, VTR, VK, VA, VC, VOK, VSTEPS, VUSED, VNU, BK, MCAP,
               mval, mdep, mcost, ctx)
    for k in range(4):
        out_val[k] = mval[k]
        for q in range(4):
            out_cost[k, q] = mcost[k, q]
