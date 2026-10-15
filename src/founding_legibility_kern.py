"""The mark (L2) kernel for the founding-legibility run (notes/founding-legibility.md §1.0 item 4).

The parent's kernel `sog_full_kern` is not edited.  This module reads its source, replaces three functions
(`prod_boss`, `prod_worker`, `productions`) and one line of `run_kernel` (the encounter clock), writes the result to a
cache file outside the repository, and imports it.  Everything else is the parent's code byte for byte.

PT carries three extra items: MARK (a numba Dict int64 -> int64: a cached NONE, keyed on the producer's type, its
production row (the encounter values PROD3 reads) and the attempt; the value is the unit step at which it was first
recorded), MK (an int64 control/counter array, layout below) and LOG (a stride sample of executed encounters).

MK layout:
  0 mode: 0 = S-nonself_3 (no skip; marks are recorded and the counters below are kept), 1 = the mark (L2)
  1 the current unit step (set by run_kernel before each executed encounter)
  2 executed-encounter counter (apply_stats calls of productions), 3 log stride, 4 log rows filled
  5 attempts skipped by the mark, 6 steps those attempts would have charged
  7 mark-sensitive productions (successes with the recorded marks differ from no skip)
  8 mark-sensitive bound (successes with every completed NONE skipped differ from no skip; Lemma M)
  9 marks recorded, 10 executed productions examined
  11, 12 scratch: production steps of the current encounter without / with the mark
LOG row: (unit step, play steps of the three participants, production steps without the mark, with the mark).
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
MK_MODE, MK_TIME, MK_ENC, MK_STRIDE, MK_LOGN, MK_SKIP, MK_SKIPSTEPS, MK_SENS, MK_SENSB, MK_REC, MK_EXAM, \
    MK_P0, MK_P1 = range(13)

_NEW_PROD = r'''
@njit(cache=True)
def _att(n, reqs, idxs, rem, P, VPLUS, PW_, skip, ctr, ia, i_st, i_cap, i_none, i_found, i_steps, apply_stats, MK):
    """The parent's attempt loop for one participant with attempts in `skip` not made.  Returns (pattern, charged
    steps, mask of attempts that ran to completion and returned NONE)."""
    pat = 0
    charged = 0
    nonemask = 0
    for a in range(n):
        req = reqs[a]
        if (skip >> a) & 1:
            if apply_stats:
                MK[5] += 1; MK[6] += req
            continue
        if apply_stats: ctr[ia] += 1
        if rem <= 0:
            if apply_stats: ctr[i_st] += 1
            continue
        if req - PW_ > P + VPLUS:
            ch = P + VPLUS + PW_
            if ch > rem:
                rem = 0
                if apply_stats: ctr[i_st] += 1
                continue
            rem -= ch
            charged += ch
            if apply_stats:
                ctr[i_cap] += 1; ctr[i_steps] += ch
            continue
        if req > rem:
            rem = 0
            if apply_stats: ctr[i_st] += 1
            continue
        rem -= req
        charged += req
        if apply_stats: ctr[i_steps] += req
        if idxs[a] < 0:
            nonemask |= (1 << a)
            if apply_stats: ctr[i_none] += 1
            continue
        pat |= (1 << a)
        if apply_stats: ctr[i_found] += 1
    return pat, charged, nonemask


@njit(cache=True)
def _choose(t, role, row, n, reqs, idxs, rem, P, VPLUS, PW_, ctr, ia, i_st, i_cap, i_none, i_found, i_steps,
            apply_stats, MARK, MK):
    """Pattern of successes under the cell's semantics; with apply_stats, the parent's counters for the chosen
    semantics, the mark's counters, and new marks recorded (completed NONE attempts)."""
    base = (role << 62) | (t << 34) | (row << 4)
    marked = 0
    allnone = 0
    for a in range(n):
        if (base | a) in MARK:
            marked |= (1 << a)
        if idxs[a] < 0:
            allnone |= (1 << a)
    dummy = np.zeros(1, np.int64)
    pat0, ch0, nm0 = _att(n, reqs, idxs, rem, P, VPLUS, PW_, 0, dummy, 0, 0, 0, 0, 0, 0, False, MK)
    patm, chm, nmm = _att(n, reqs, idxs, rem, P, VPLUS, PW_, marked, dummy, 0, 0, 0, 0, 0, 0, False, MK)
    pata, cha, nma = _att(n, reqs, idxs, rem, P, VPLUS, PW_, allnone, dummy, 0, 0, 0, 0, 0, 0, False, MK)
    mode = MK[0]
    skip = marked if mode == 1 else 0
    if apply_stats:
        pat, ch, nm = _att(n, reqs, idxs, rem, P, VPLUS, PW_, skip, ctr, ia, i_st, i_cap, i_none, i_found, i_steps,
                           True, MK)
        MK[10] += 1
        if patm != pat0: MK[7] += 1
        if pata != pat0: MK[8] += 1
        MK[11] += ch0
        MK[12] += chm
        for a in range(n):
            if (nm >> a) & 1:
                k = base | a
                if k not in MARK:
                    MARK[k] = MK[1]
                    MK[9] += 1
        return pat
    return patm if mode == 1 else pat0


@njit(cache=True)
def prod_boss(b, oi, oc, PT, K, P, VPLUS, PW_, ctr, miss, apply_stats):
    """S-nonself_3 production of boss b at the composed encounter, with the mark (founding_legibility_kern)."""
    (PBI, PB_N, PB_IDX, PB_OWN, PB_MASK, PB_NEW, B_PLAYOWN, B_CALLM, PWD, PW_N, PW_IDX, PW_OWN, PW_MASK, PW_NEW,
     WPLAY, BCLS, BSP, WCLS, WSP, TYPB, TYPW, GATE, MARK, MK, LOG) = PT
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
    reqs = np.zeros(n, np.int64)
    idxs = np.zeros(n, np.int64)
    for a in range(n):
        req = PB_OWN[row, a]
        m = PB_MASK[row, a]
        for k in range(8):
            if (m >> k) & 1:
                req += oc[7 + k]
        reqs[a] = req
        idxs[a] = PB_IDX[row, a]
    pat = _choose(b, 0, row, n, reqs, idxs, rem, P, VPLUS, PW_, ctr, 1, 5, 4, 3, 2, 17, apply_stats, MARK, MK)
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
     WPLAY, BCLS, BSP, WCLS, WSP, TYPB, TYPW, GATE, MARK, MK, LOG) = PT
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
    reqs = np.zeros(n, np.int64)
    idxs = np.zeros(n, np.int64)
    for a in range(n):
        req = PW_OWN[row, a]
        mm = PW_MASK[row, a]
        if mm & 1: req += c0
        if mm & 2: req += c1
        if mm & 4: req += c2
        if mm & 8: req += cC
        if mm & 16: req += cD
        reqs[a] = req
        idxs[a] = PW_IDX[row, a]
    pat = _choose(x, 1, row, n, reqs, idxs, rem, P, VPLUS, PW_, ctr, 6, 10, 9, 8, 7, 18, apply_stats, MARK, MK)
    nc = PW_NEW[row, pat]
    if nc == cx:
        return x
    key = (WSP[x] << SH) | nc
    if key in TYPW:
        return TYPW[key]
    miss[0] = 7; miss[1] = WSP[x]; miss[2] = nc; return -1


@njit(cache=True)
def play3(bb, xx, yy, oi, oc, T, PT, LIVE_EQ):
    """Play steps of the three participants of the composed encounter (the parent's play cost model)."""
    (PBI, PB_N, PB_IDX, PB_OWN, PB_MASK, PB_NEW, B_PLAYOWN, B_CALLM, PWD, PW_N, PW_IDX, PW_OWN, PW_MASK, PW_NEW,
     WPLAY, BCLS, BSP, WCLS, WSP, TYPB, TYPW, GATE, MARK, MK, LOG) = PT
    r = oi[1]
    play = B_PLAYOWN[r]
    for k in range(8):
        play += B_CALLM[r, k] * oc[7 + k]
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
        play += WPLAY[cx, bits, 0] + WPLAY[cx, bits, 1] * oc[0] + WPLAY[cx, bits, 2] * oc[1] \
            + WPLAY[cx, bits, 3] * oc[2] + WPLAY[cx, bits, 4] * cC + WPLAY[cx, bits, 5] * cD
    return play


@njit(cache=True)
def productions(bb, xx, yy, T, PT, BLACK, WLACK, LIVE_EQ, K, P, VPLUS, PW_, ctr, miss, oi, oc, newt, apply_stats):
    """Composes the encounter and its productions; newt[s] = new type or -1.  False on a miss."""
    if not chain(bb, xx, yy, T, oi, oc, miss):
        return False
    newt[0] = -1; newt[1] = -1; newt[2] = -1
    WCLS = T[2]; BCLS = T[24]
    MK = PT[23]
    if apply_stats:
        MK[11] = 0; MK[12] = 0
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
        MK[2] += 1
        LOG = PT[24]
        if MK[3] > 0 and MK[2] % MK[3] == 0 and MK[4] < LOG.shape[0]:
            q = MK[4]
            LOG[q, 0] = MK[1]
            LOG[q, 1] = play3(bb, xx, yy, oi, oc, T, PT, LIVE_EQ)
            LOG[q, 2] = MK[11]
            LOG[q, 3] = MK[12]
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
    # remove the three replaced functions (each from its decorator to the next decorator)
    for name in ('prod_boss', 'prod_worker', 'productions'):
        pat = re.compile(r'@njit\(cache=True\)\ndef %s\(.*?(?=\n@njit\(cache=True\)\n)' % name, re.S)
        src, n = pat.subn('', src)
        assert n == 1, name
    # insert the new ones before mark_dirty (after wbits, chain and the helpers they use)
    anchor = '@njit(cache=True)\ndef mark_dirty('
    assert src.count(anchor) == 1
    src = src.replace(anchor, _NEW_PROD.lstrip('\n') + '\n' + anchor)
    assert src.count(_CLOCK_OLD) == 1
    src = src.replace(_CLOCK_OLD, _CLOCK_NEW)
    header = '# GENERATED by src/founding_legibility_kern.py from src/sog_full_kern.py; do not edit.\n'
    return header + src


def _load():
    d = os.path.join(tempfile.gettempdir(), 'program_ecologies_flk')
    os.makedirs(d, exist_ok=True)
    f = os.path.join(d, 'flk_kern_gen.py')
    src = generated_source()
    if not os.path.exists(f) or open(f).read() != src:
        tmp = f + '.%d.tmp' % os.getpid()
        with open(tmp, 'w') as fh:
            fh.write(src)
        os.replace(tmp, f)
    spec = importlib.util.spec_from_file_location('flk_kern_gen', f)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['flk_kern_gen'] = mod
    spec.loader.exec_module(mod)
    return mod


K2 = _load()


def new_mark_state(mode, stride=200, logcap=20000):
    from numba import types
    from numba.typed import Dict
    MARK = Dict.empty(key_type=types.int64, value_type=types.int64)
    MK = np.zeros(MK_N, np.int64)
    MK[MK_MODE] = mode
    MK[MK_STRIDE] = stride
    LOG = np.zeros((logcap, 4), np.int64)
    return MARK, MK, LOG
