"""The production kernel of the per-root run (notes/per-root.md §1.0 items 3-8).

The parent's kernel `sog_full_kern` is not edited.  This module reads its source, replaces three functions
(`prod_boss`, `prod_worker`, `productions`) and one line of `run_kernel` (the encounter clock, as
`founding_legibility_kern` did), writes the result to a cache file outside the repository, and imports it.  Everything
else is the parent's code byte for byte.

A participant's production at an encounter, for every rule (notes §1.0 item 4):
  (i)   validation: for every set with a non-empty list (per-root rules only), the program's own root validation in the
        residual fuel, capped at V (a timeout or a nested timeout makes the set lacking); fuel exhausted -> nothing is
        attempted;
  (ii)  the mark (key: role, spelling, set, root; never the program's own list) skips lacking sets with a recorded NONE;
  (iii) production attempts for the remaining lacking sets in family order (the parent's charging, cap P);
  (iv)  the new class is QX_NEW[row, code], code = sum_a s_a 3^a with s_a = 0 nothing, 1 used (CLOCK bits only),
        2 produced; filled lazily by the driver (miss kind 9).

PT = the parent's 22 items + (MARK, MK, LOG, PC, SC, RV,
      QB_VAL, QB_VOWN, QB_VMASK, QB_IDX, QB_ALT, QB_OWN, QB_MASK, QB_NEW,
      QW_VAL, QW_VOWN, QW_VMASK, QW_IDX, QW_ALT, QW_OWN, QW_MASK, QW_NEW).
RV = [per-root (0/1), use bits (0/1), TO_CHARGE].
MK (as founding_legibility_kern): 0 mode (1 = skip marked), 1 clock, 2 executed encounters, 3 log stride, 4 log rows,
  5 skipped attempts, 6 their steps, 7 mark-sensitive productions, 8 Lemma-M bound, 9 marks recorded, 10 examined.
PC (per role, offset 0 boss / 32 worker): 0 valid, 1 invalid, 2 validation cap timeout, 3 validation fuel stop,
  4 attempts, 5 found, 6 none, 7 cap timeout, 8 fuel timeout, 9 marked skips, 10 their steps, 11 validation steps,
  12 production steps, 13 found with an alternative, 14 class changes, 15 participants examined.
LOG row: unit step, play b/x/y, validation b/x/y, production b/x/y.
"""
import os
import re
import sys
import tempfile
import importlib.util

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

MK_N = 16
PC_N = 64
SC_N = 16
LOG_W = 10
MISS_NEW = 9

_NEW_PROD = r'''
@njit(cache=True)
def _att2(n, lack, reqs, idxs, rem, P, VPLUS, PW_, skip, ctr, ia, i_st, i_cap, i_none, i_found, i_steps, PC, off,
          apply_stats, MK):
    """The parent's attempt loop over the lacking sets (bit a of `lack`), attempts in `skip` not made.  Returns
    (pattern of successes, charged steps, mask of attempts completed with NONE)."""
    pat = 0
    charged = 0
    nonemask = 0
    for a in range(n):
        if not ((lack >> a) & 1):
            continue
        req = reqs[a]
        if (skip >> a) & 1:
            if apply_stats:
                MK[5] += 1; MK[6] += req; PC[off + 9] += 1; PC[off + 10] += req
            continue
        if apply_stats:
            ctr[ia] += 1; PC[off + 4] += 1
        if rem <= 0:
            if apply_stats:
                ctr[i_st] += 1; PC[off + 8] += 1
            continue
        if req - PW_ > P + VPLUS:
            ch = P + VPLUS + PW_
            if ch > rem:
                rem = 0
                if apply_stats:
                    ctr[i_st] += 1; PC[off + 8] += 1
                continue
            rem -= ch
            charged += ch
            if apply_stats:
                ctr[i_cap] += 1; ctr[i_steps] += ch; PC[off + 7] += 1; PC[off + 12] += ch
            continue
        if req > rem:
            rem = 0
            if apply_stats:
                ctr[i_st] += 1; PC[off + 8] += 1
            continue
        rem -= req
        charged += req
        if apply_stats:
            ctr[i_steps] += req; PC[off + 12] += req
        if idxs[a] < 0:
            nonemask |= (1 << a)
            if apply_stats:
                ctr[i_none] += 1; PC[off + 6] += 1
            continue
        pat |= (1 << a)
        if apply_stats:
            ctr[i_found] += 1; PC[off + 5] += 1
    return pat, charged, nonemask


@njit(cache=True)
def _part(n, vals, vreq, areq, idxs, alts, rem, V, P, VPLUS, PW_, TOCH, perroot, usebits, mkbase, MARK, MK, PC, off,
          ctr, ia, i_st, i_cap, i_none, i_found, i_steps, apply_stats):
    """One participant: validation, the mark, attempts.  Returns (code, validation steps charged, production steps
    charged)."""
    states = np.zeros(3, np.int64)
    lack = 0
    vch = 0
    stopped = False
    for a in range(n):
        v = vals[a]
        if v < 0:
            lack |= (1 << a)
            continue
        if perroot == 0:
            continue
        if rem <= 0:
            stopped = True
            if apply_stats: PC[off + 3] += 1
            break
        req = vreq[a]
        if req > V + VPLUS:
            ch = V + TOCH
            if ch > rem:
                rem = 0
                stopped = True
                if apply_stats: PC[off + 3] += 1
                break
            rem -= ch
            vch += ch
            lack |= (1 << a)
            if apply_stats: PC[off + 2] += 1
            continue
        if req > rem:
            rem = 0
            stopped = True
            if apply_stats: PC[off + 3] += 1
            break
        rem -= req
        vch += req
        if v == 1:
            if usebits == 1:
                states[a] = 1
            if apply_stats: PC[off + 0] += 1
        else:
            lack |= (1 << a)
            if apply_stats: PC[off + 1] += 1
    if apply_stats:
        PC[off + 11] += vch; PC[off + 15] += 1
    if stopped:
        lack = 0
    marked = 0
    allnone = 0
    for a in range(n):
        if (lack >> a) & 1:
            if (mkbase | a) in MARK:
                marked |= (1 << a)
            if idxs[a] < 0:
                allnone |= (1 << a)
    dummy = np.zeros(1, np.int64)
    dpc = np.zeros(PC.shape[0], np.int64)
    mode = MK[0]
    skip = marked if mode == 1 else 0
    if apply_stats:
        pat0, ch0, nm0 = _att2(n, lack, areq, idxs, rem, P, VPLUS, PW_, 0, dummy, 0, 0, 0, 0, 0, 0, dpc, 0, False, MK)
        patm, chm, nmm = _att2(n, lack, areq, idxs, rem, P, VPLUS, PW_, marked, dummy, 0, 0, 0, 0, 0, 0, dpc, 0, False,
                               MK)
        pata, cha, nma = _att2(n, lack, areq, idxs, rem, P, VPLUS, PW_, allnone, dummy, 0, 0, 0, 0, 0, 0, dpc, 0,
                               False, MK)
        pat, pch, nm = _att2(n, lack, areq, idxs, rem, P, VPLUS, PW_, skip, ctr, ia, i_st, i_cap, i_none, i_found,
                             i_steps, PC, off, True, MK)
        MK[10] += 1
        if patm != pat0: MK[7] += 1
        if pata != pat0: MK[8] += 1
        MK[11] += ch0
        MK[12] += chm
        for a in range(n):
            if (nm >> a) & 1:
                k = mkbase | a
                if k not in MARK:
                    MARK[k] = MK[1]
                    MK[9] += 1
            if (pat >> a) & 1 and alts[a] >= 0:
                PC[off + 13] += 1
    else:
        pat, pch, nm = _att2(n, lack, areq, idxs, rem, P, VPLUS, PW_, skip, dummy, 0, 0, 0, 0, 0, 0, dpc, 0, False, MK)
    code = 0
    p3 = 1
    for a in range(n):
        s = 2 if (pat >> a) & 1 else states[a]
        code += s * p3
        p3 *= 3
    return code, vch, pch


@njit(cache=True)
def prod_boss(b, oi, oc, PT, K, P, VPLUS, PW_, ctr, miss, apply_stats):
    """Per-root production of boss b at the composed encounter: the new type (b if unchanged), -1 on a miss."""
    (PBI, PB_N, PB_IDX, PB_OWN, PB_MASK, PB_NEW, B_PLAYOWN, B_CALLM, PWD, PW_N, PW_IDX, PW_OWN, PW_MASK, PW_NEW,
     WPLAY, BCLS, BSP, WCLS, WSP, TYPB, TYPW, GATE, MARK, MK, LOG, PC, SC, RV,
     QB_VAL, QB_VOWN, QB_VMASK, QB_IDX, QB_ALT, QB_OWN, QB_MASK, QB_NEW,
     QW_VAL, QW_VOWN, QW_VMASK, QW_IDX, QW_ALT, QW_OWN, QW_MASK, QW_NEW) = PT
    r = oi[1]; ri = oi[8]
    cb = BCLS[b]
    row = PBI[cb, ri]
    if row < 0:
        miss[0] = 4; miss[1] = b; miss[2] = ri; miss[3] = oi[0]; return -1
    play = B_PLAYOWN[r]
    for k in range(8):
        play += B_CALLM[r, k] * oc[7 + k]
    rem = K - play
    vals = np.zeros(3, np.int64); vreq = np.zeros(3, np.int64); areq = np.zeros(3, np.int64)
    idxs = np.zeros(3, np.int64); alts = np.zeros(3, np.int64)
    for a in range(3):
        vals[a] = QB_VAL[row, a]
        v = QB_VOWN[row, a]
        m = QB_VMASK[row, a]
        for k in range(8):
            if (m >> k) & 1:
                v += oc[7 + k]
        vreq[a] = v
        req = QB_OWN[row, a]
        m = QB_MASK[row, a]
        for k in range(8):
            if (m >> k) & 1:
                req += oc[7 + k]
        areq[a] = req
        idxs[a] = QB_IDX[row, a]
        alts[a] = QB_ALT[row, a]
    V = K // 4
    mkbase = (np.int64(1) << 62) | (BSP[b] << 30) | (ri << 4)
    code, vch, pch = _part(3, vals, vreq, areq, idxs, alts, rem, V, P, VPLUS, PW_, RV[2], RV[0], RV[1], mkbase, MARK,
                           MK, PC, 0, ctr, 1, 5, 4, 3, 2, 17, apply_stats)
    if apply_stats:
        SC[0] = play; SC[3] = vch; SC[6] = pch
    if code == 0:
        return b
    nc = QB_NEW[row, code]
    if nc < 0:
        miss[0] = 9; miss[1] = 0; miss[2] = row; miss[3] = code; return -1
    if nc == cb:
        return b
    if apply_stats: PC[14] += 1
    key = (BSP[b] << SH) | nc
    if key in TYPB:
        return TYPB[key]
    miss[0] = 6; miss[1] = BSP[b]; miss[2] = nc; return -1


@njit(cache=True)
def prod_worker(x, j, oi, oc, PT, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, apply_stats):
    (PBI, PB_N, PB_IDX, PB_OWN, PB_MASK, PB_NEW, B_PLAYOWN, B_CALLM, PWD, PW_N, PW_IDX, PW_OWN, PW_MASK, PW_NEW,
     WPLAY, BCLS, BSP, WCLS, WSP, TYPB, TYPW, GATE, MARK, MK, LOG, PC, SC, RV,
     QB_VAL, QB_VOWN, QB_VMASK, QB_IDX, QB_ALT, QB_OWN, QB_MASK, QB_NEW,
     QW_VAL, QW_VOWN, QW_VMASK, QW_IDX, QW_ALT, QW_OWN, QW_MASK, QW_NEW) = PT
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
    rcode = ((((j - 1) * 27 + bex) * 9 + oex) * 2 + rel)
    key = cx * 972 + rcode
    if key in PWD:
        row = PWD[key]
    else:
        miss[0] = 5; miss[1] = x; miss[2] = j; miss[3] = bex; miss[4] = oex; miss[5] = rel; return -1
    eq = 1 if (rel == 1 and LIVE_EQ == 1) else 0
    bits = wbits(bex, 1 if oD == 1 else 0, 1 if oC == 1 else 0, eq)
    c0 = oc[0]; c1 = oc[1]; c2 = oc[2]
    play = WPLAY[cx, bits, 0] + WPLAY[cx, bits, 1] * c0 + WPLAY[cx, bits, 2] * c1 + WPLAY[cx, bits, 3] * c2 \
        + WPLAY[cx, bits, 4] * cC + WPLAY[cx, bits, 5] * cD
    rem = K - play
    vals = np.zeros(2, np.int64); vreq = np.zeros(2, np.int64); areq = np.zeros(2, np.int64)
    idxs = np.zeros(2, np.int64); alts = np.zeros(2, np.int64)
    for a in range(2):
        vals[a] = QW_VAL[row, a]
        v = QW_VOWN[row, a]
        mm = QW_VMASK[row, a]
        if mm & 1: v += c0
        if mm & 2: v += c1
        if mm & 4: v += c2
        if mm & 8: v += cC
        if mm & 16: v += cD
        vreq[a] = v
        req = QW_OWN[row, a]
        mm = QW_MASK[row, a]
        if mm & 1: req += c0
        if mm & 2: req += c1
        if mm & 4: req += c2
        if mm & 8: req += cC
        if mm & 16: req += cD
        areq[a] = req
        idxs[a] = QW_IDX[row, a]
        alts[a] = QW_ALT[row, a]
    V = K // 4
    mkbase = (np.int64(1) << 62) | (np.int64(1) << 61) | (WSP[x] << 30) | (rcode << 4)
    code, vch, pch = _part(2, vals, vreq, areq, idxs, alts, rem, V, P, VPLUS, PW_, RV[2], RV[0], RV[1], mkbase, MARK,
                           MK, PC, 32, ctr, 6, 10, 9, 8, 7, 18, apply_stats)
    if apply_stats:
        SC[j] = play; SC[3 + j] = vch; SC[6 + j] = pch
    if code == 0:
        return x
    nc = QW_NEW[row, code]
    if nc < 0:
        miss[0] = 9; miss[1] = 1; miss[2] = row; miss[3] = code; return -1
    if nc == cx:
        return x
    if apply_stats: PC[32 + 14] += 1
    key = (WSP[x] << SH) | nc
    if key in TYPW:
        return TYPW[key]
    miss[0] = 7; miss[1] = WSP[x]; miss[2] = nc; return -1


@njit(cache=True)
def play_part(bb, xx, yy, oi, oc, T, PT, LIVE_EQ, SC):
    """Play steps of the three participants of the composed encounter into SC[0..2] (the parent's play model)."""
    (PBI, PB_N, PB_IDX, PB_OWN, PB_MASK, PB_NEW, B_PLAYOWN, B_CALLM, PWD, PW_N, PW_IDX, PW_OWN, PW_MASK, PW_NEW,
     WPLAY, BCLS, BSP, WCLS, WSP, TYPB, TYPW, GATE, MARK, MK, LOG, PC, SC_, RV,
     QB_VAL, QB_VOWN, QB_VMASK, QB_IDX, QB_ALT, QB_OWN, QB_MASK, QB_NEW,
     QW_VAL, QW_VOWN, QW_VMASK, QW_IDX, QW_ALT, QW_OWN, QW_MASK, QW_NEW) = PT
    r = oi[1]
    play = B_PLAYOWN[r]
    for k in range(8):
        play += B_CALLM[r, k] * oc[7 + k]
    SC[0] = play
    bex = oi[3]
    eq = 1 if (oi[9] == 1 and LIVE_EQ == 1) else 0
    for j in (1, 2):
        x = xx if j == 1 else yy
        cx = WCLS[x]
        if j == 1:
            oC = oi[6]; oD = oi[7]; cC = oc[5]; cD = oc[6]
        else:
            oC = oi[4]; oD = oi[5]; cC = oc[3]; cD = oc[4]
        bits = wbits(bex, 1 if oD == 1 else 0, 1 if oC == 1 else 0, eq)
        SC[j] = WPLAY[cx, bits, 0] + WPLAY[cx, bits, 1] * oc[0] + WPLAY[cx, bits, 2] * oc[1] \
            + WPLAY[cx, bits, 3] * oc[2] + WPLAY[cx, bits, 4] * cC + WPLAY[cx, bits, 5] * cD


@njit(cache=True)
def productions(bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc, newt, apply_stats):
    """Composes the encounter and its productions; newt[s] = new type or -1.  False on a miss."""
    if not chain(bb, xx, yy, T, oi, oc, miss):
        return False
    newt[0] = -1; newt[1] = -1; newt[2] = -1
    WCLS = T[2]; BCLS = T[24]
    SC = PT[26]
    if apply_stats:
        for q in range(SC.shape[0]):
            SC[q] = 0
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
    if apply_stats:
        MK = PT[23]
        MK[2] += 1
        LOG = PT[24]
        if MK[3] > 0 and MK[2] % MK[3] == 0 and MK[4] < LOG.shape[0]:
            play_part(bb, xx, yy, oi, oc, T, PT, LIVE_EQ, SC)
            q = MK[4]
            LOG[q, 0] = MK[1]
            for z in range(9):
                LOG[q, 1 + z] = SC[z]
            MK[4] = q + 1
    return True

'''

_CLOCK_OLD = ("                ctr[0] += 1\n"
              "                productions(bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc, newt, True)\n")
_CLOCK_NEW = ("                ctr[0] += 1\n"
              "                PT[23][1] = st[ST_B]\n"
              "                productions(bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc, newt, True)\n")


def generated_source():
    src = open(os.path.join(HERE, 'sog_full_kern.py')).read()
    for name in ('prod_boss', 'prod_worker', 'productions'):
        pat = re.compile(r'@njit\(cache=True\)\ndef %s\(.*?(?=\n@njit\(cache=True\)\n)' % name, re.S)
        src, n = pat.subn('', src)
        assert n == 1, name
    anchor = '@njit(cache=True)\ndef mark_dirty('
    assert src.count(anchor) == 1
    src = src.replace(anchor, _NEW_PROD.lstrip('\n') + '\n' + anchor)
    assert src.count(_CLOCK_OLD) == 1
    src = src.replace(_CLOCK_OLD, _CLOCK_NEW)
    header = '# GENERATED by src/per_root_kern.py from src/sog_full_kern.py; do not edit.\n'
    return header + src


def _load():
    d = os.path.join(tempfile.gettempdir(), 'program_ecologies_prk')
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, 'prk_kern_gen.py')
    src = generated_source()
    if not os.path.exists(f) or open(f).read() != src:
        tmp = f + '.%d.tmp' % os.getpid()
        with open(tmp, 'w') as fh:
            fh.write(src)
        os.replace(tmp, f)
    spec = importlib.util.spec_from_file_location('prk_kern_gen', f)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['prk_kern_gen'] = mod
    spec.loader.exec_module(mod)
    return mod


K3 = _load()


def new_state(mode=1, stride=200, logcap=20000):
    """(MARK, MK, LOG, PC, SC): the mark table, its controls/counters, the cost log, per-role counters, scratch."""
    from numba import types
    from numba.typed import Dict
    MARK = Dict.empty(key_type=types.int64, value_type=types.int64)
    MK = np.zeros(MK_N, np.int64)
    MK[0] = mode
    MK[3] = stride
    LOG = np.zeros((logcap, LOG_W), np.int64)
    PC = np.zeros(PC_N, np.int64)
    SC = np.zeros(SC_N, np.int64)
    return MARK, MK, LOG, PC, SC
