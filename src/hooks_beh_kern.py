"""Behavioural hooks: the eps = 0 island kernel over types (base, fills, lineage) with behavioural keys (notes/hooks-beh.md).

A copy of hooks_w2_kern.py rebuilt on hooks_beh's evaluator.  Differences from hooks_w2_kern (everything else is its law):
  * specs are packed entry words (hooks_beh.spec_of_beh); the match cache `ev` is keyed on the eight words (base, three specs
    for each party) and holds the outcome only (ax | ay << 1);
  * the registry state of "x reads y" (needed by writes) is read through `ev2` (the same eight-word key) and interned in
    `tv` (the truth of every key at the stabilized world), so a conditional key draw is a scan over the keys;
  * write_mode (cfg[11]): 0 lineage (Part W), 1 legacy open (key 8 + p, p = box a), 2 behavioural family (key drawn from the
    prior conditioned on being true of the partner), 3 the a-free family, 4 sham (an unconditioned key matched in size and in
    its applicability count to the conditioned draw);  contract_mode (cfg[12]): 0 lineage, 1 legacy open (key 9), 2 family,
    3 a-free family (one key pair per attempt, independent draws from the prior, action C, on every pair of carried tags);
  * ancestry flags (cfg[14]) in the key field of a behaviour fill (bits 12-13: 0 seeded, 1 thanks, 2 grudge, 3 contract; bit
    14: the fill has been copied at least once) and the origin field as the latest transmission event;
  * ablations: cfg[6] = 2 strips every non-seeded fill at birth, cfg[15] = 1 writes only into empty slots (rejections logged),
    cfg[17:19] a window [lo, hi) of generations (offset cfg[19]) in which fills may be created, cfg[16] the hostile boost factor;
  * cfg[20] = 1 classifies types against the fixed panel (CooperateBot, DefectBot, FairBot, TrustingBot, PrudentBot, the Godel
    predator, a stranger copy), logs class conversions (`conv`), and records per-island class counts and the (class, deciding
    origin, copied) table at the checks.
cfg: 0 recency, 1 grudge writes, 2 thanks writes, 3 contracts, 4 copying, 5 shuffled trigger keys, 6 noinherit (1 strip written,
2 strip every non-seeded fill), 7 encounters on, 8 compute initial matrices, 9 rejection parent sampler, 10 copies keep origin,
11 write_mode, 12 contract_mode, 13 strict history variants, 14 ancestry flags, 15 no eviction, 16 hostile boost, 17/18 write
window, 19 generation offset, 20 class logging.
counters: 0 encounters, 1 grudge writes, 2 thanks writes, 3 in-place updates, 4 evictions, 5 copies, 6 contract attempts,
7 contracts, 8 capacity overflow, 9 encounters whose outcome the fills change, 10 writes that changed nothing, 11 contract
candidates evaluated, 13-16 contract-holder party-encounters and their (C against D) events (open, lineage), 17 behavioural
writes, 18-20 rejected writes / copies / contract writes (no-eviction cells), 21 state-store overflow, 22 writes with no true
key, 23 writes outside the window.
rec_isl[c, i]: 0 P(C,C), 1 mean payoff, 2 lineages, 3 lineage concentration, 4 majority type, 5 majority count, 6 present types.
rec_glob[c]: as hooks_w2_kern (0..63 held fills by (carried, scope, origin, action), 64.. as there; 70-73 behaviour-fill holders).
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from numba import njit, types
from numba.typed import Dict
import hooks_w2 as H
import hooks_beh as HB
from hooks_beh import spec_of_beh, eval_match_beh

NREC_I, NREC_G = 7, 80
NCLS = 8                      # FairBot, PrudentBot, CooperateBot, DefectBot, TrustingBot, predator, other, ambiguous
NORG = 7                      # none, seeded, thanks, grudge, contract, multi, copied-unknown
SCAP = 8192
TCAP = 200_000


def new_tables(KT, cap=TCAP):
    T = (np.zeros(cap, np.int64), np.zeros(cap, np.int64), np.zeros((cap, 4), np.int64), np.zeros(cap, np.int64),
         np.zeros(cap, np.int64), np.zeros(cap, np.int64), np.zeros(cap, np.int64), np.zeros(cap, np.bool_),
         -np.ones(cap, np.int8), np.zeros(cap, np.int64), np.zeros(2, np.int64), np.zeros(cap, np.int64),
         -np.ones(cap, np.int8), np.zeros(cap, np.int8), np.zeros(cap, np.int8))
    tdict = Dict.empty(key_type=types.UniTuple(types.int64, 3), value_type=types.int64)
    ev = Dict.empty(key_type=types.UniTuple(types.int64, 8), value_type=types.int64)
    ev2 = Dict.empty(key_type=types.UniTuple(types.int64, 8), value_type=types.int64)
    sdict = Dict.empty(key_type=types.UniTuple(types.int64, 2), value_type=types.int64)
    tv = np.zeros((SCAP, len(KT.keys)), np.bool_)
    smeta = np.zeros(4, np.int64)
    return T, tdict, ev, ev2, sdict, tv, smeta


# ------------------------------------------------------------------ fill helpers
@njit(cache=True)
def kid_of(f):
    """Key id of a behaviour fill (flags stripped)."""
    return H.f_key(f) & 4095


@njit(cache=True)
def kanc(f):
    return (H.f_key(f) >> 12) & 3


@njit(cache=True)
def kcop(f):
    return (H.f_key(f) >> 14) & 1


@njit(cache=True)
def wfill(f, nf, newf, out, noevict):
    """out <- f with newf written (in-place update when (tag, scope, key) match -- flags and origin ignored for behaviour
    fills; else append, FIFO beyond 4).  Returns (new nf, evicted, in-place, rejected); noevict: a write that would evict is
    rejected (out = f)."""
    sc_new = ((newf - 1) >> 2) & 3
    mask = ~np.int64(1 | (3 << 4)) if sc_new != 3 else ~np.int64(1 | (3 << 4) | (7 << 18))
    nk = (newf - 1) & mask
    hit = -1
    for j in range(nf):
        sc_j = ((f[j] - 1) >> 2) & 3
        if sc_j == sc_new and ((f[j] - 1) & mask) == nk:
            hit = j; break
    if hit < 0 and nf == 4 and noevict == 1:
        for j in range(4):
            out[j] = f[j]
        return nf, 0, 0, 1
    m = 0
    for j in range(nf):
        if j != hit:
            out[m] = f[j]; m += 1
    ev_ = 0
    if hit < 0 and nf == 4:
        for j in range(3):
            out[j] = out[j + 1]
        m = 3; ev_ = 1
    out[m] = newf; m += 1
    for j in range(m, 4):
        out[j] = 0
    return m, ev_, 1 if hit >= 0 else 0, 0


@njit(cache=True)
def _tkey(base, lin, g):
    return (np.int64((base << 32) | lin), np.int64(g[0] | (g[1] << 21) | (g[2] << 42)), np.int64(g[3]))


@njit(cache=True)
def _hashist(f, nf, tags, active):
    for j in range(nf):
        if H.f_scope(f[j]) == 2 and active[2, H.f_origin(f[j])] and (tags >> H.f_tag(f[j])) & 1:
            return True
    return False


@njit(cache=True)
def get_type(T, tdict, b_tags, active, recency, base, lin, f, nf):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    g = np.zeros(4, np.int64)
    for j in range(nf):
        g[j] = f[j]
    key = _tkey(base, lin, g)
    if key in tdict:
        return tdict[key]
    if meta[1] > 0:
        meta[1] -= 1
        t = freel[meta[1]]
    else:
        t = meta[0]
        if t >= Tb.shape[0]:
            return -1
        meta[0] = t + 1
    Tb[t] = base; Tl[t] = lin; Tn[t] = nf
    for j in range(4):
        Tf[t, j] = g[j]
    tg = b_tags[base]
    Tg[t] = tg
    Ts0[t] = spec_of_beh(g, nf, tg, active, recency, -1)
    Tss[t] = spec_of_beh(g, nf, tg, active, recency, lin)
    Th[t] = _hashist(g, nf, tg, active)
    Tgent[t] = -1; gcount[t] = 0; Tcls[t] = -1; Tdec[t] = -1; Tcop[t] = 0
    tdict[key] = t
    return t


@njit(cache=True)
def free_type(T, tdict, t):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    key = _tkey(Tb[t], Tl[t], Tf[t])
    if key in tdict and tdict[key] == t:
        tdict.pop(key)
        freel[meta[1]] = t; meta[1] += 1


@njit(cache=True)
def spec_ctx(T, active, recency, t, l):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    if not Th[t]:
        return Ts0[t]
    if l == Tl[t]:
        return Tss[t]
    return spec_of_beh(Tf[t], Tn[t], Tg[t], active, recency, l)


# ------------------------------------------------------------------ match cache and registry states
@njit(cache=True)
def _ekey(bx, sx0, sx1, sx2, by, sy0, sy1, sy2):
    return (np.int64(bx), np.int64(sx0), np.int64(sx1), np.int64(sx2), np.int64(by), np.int64(sy0), np.int64(sy1), np.int64(sy2))


@njit(cache=True)
def swap_code(c):
    return ((c >> 1) & 1) | ((c & 1) << 1)


@njit(cache=True)
def eval_code(LA, KA, ev, iC, iD, bx, sx0, sx1, sx2, by, sy0, sy1, sy2):
    key = _ekey(bx, sx0, sx1, sx2, by, sy0, sy1, sy2)
    if key in ev:
        return ev[key]
    key2 = _ekey(by, sy0, sy1, sy2, bx, sx0, sx1, sx2)
    if key2 in ev:
        return swap_code(ev[key2])
    p_nat, p_kind, p_lev, p_form, p_arg, p_tt, b_nat, b_kind, b_lev, b_form, b_arg, b_tt = LA
    rs = np.zeros(4, np.int64)
    ax, ay, _, _ = eval_match_beh(p_nat, p_kind, p_lev, p_form, p_arg, p_tt, b_nat, b_kind, b_lev, b_form, b_arg, b_tt,
                                  iC, iD, KA[0], KA[1], KA[2], KA[3], False, bx, sx0, sx1, sx2, by, sy0, sy1, sy2, rs)
    code = np.int64(ax | (ay << 1))
    ev[key] = code
    return code


@njit(cache=True)
def match(T, LA, KA, ev, iC, iD, active, recency, a, b):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    return eval_code(LA, KA, ev, iC, iD, Tb[a], Ts0[a], spec_ctx(T, active, recency, a, Tl[b]), Tss[a],
                     Tb[b], Ts0[b], spec_ctx(T, active, recency, b, Tl[a]), Tss[b])


@njit(cache=True)
def _intern(word, length, tv, sdict, smeta, KA):
    """Id of the registry state reached by the letter word (two levels: the word, then the state's hash, so words that reach
    one state share an id; new states get their key truth vector computed); -1 if the store is full."""
    wkey = (word, (np.int64(1) << 40) | length)
    if wkey in sdict:
        return sdict[wkey]
    B = HB.fold_state(word, length, KA[1], KA[3])
    h1 = np.int64(1469598103934665603); h2 = np.int64(7809847782465536322)
    for j in range(B.shape[0]):
        b = np.int64(1) if B[j] else np.int64(0)
        h1 = h1 * np.int64(1099511628211) + b + 1
        h2 = h2 * np.int64(6364136223846793005) + b * 3 + 7
    key = (h1, h2)
    if key in sdict:
        sdict[wkey] = sdict[key]
        return sdict[key]
    if smeta[0] >= tv.shape[0]:
        smeta[1] += 1
        return -1
    i = smeta[0]
    smeta[0] += 1
    for k in range(tv.shape[1]):
        tv[i, k] = HB.key_true(k, KA[0], B)
    sdict[key] = i
    sdict[wkey] = i
    return i


@njit(cache=True)
def read_state(T, LA, KA, ev2, tv, sdict, smeta, iC, iD, active, recency, a, b):
    """(state id of a reading b, state id of b reading a) at the stabilized world, a and b under their fills and lineages;
    -1 when the store is full."""
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    sx0 = Ts0[a]; sx1 = spec_ctx(T, active, recency, a, Tl[b]); sx2 = Tss[a]
    sy0 = Ts0[b]; sy1 = spec_ctx(T, active, recency, b, Tl[a]); sy2 = Tss[b]
    key = _ekey(Tb[a], sx0, sx1, sx2, Tb[b], sy0, sy1, sy2)
    if key in ev2:
        v = ev2[key]
        return v & 0xFFFFFF, v >> 24
    key2 = _ekey(Tb[b], sy0, sy1, sy2, Tb[a], sx0, sx1, sx2)
    if key2 in ev2:
        v = ev2[key2]
        return v >> 24, v & 0xFFFFFF
    p_nat, p_kind, p_lev, p_form, p_arg, p_tt, b_nat, b_kind, b_lev, b_form, b_arg, b_tt = LA
    rs = np.zeros(4, np.int64)
    ax, ay, _, _ = eval_match_beh(p_nat, p_kind, p_lev, p_form, p_arg, p_tt, b_nat, b_kind, b_lev, b_form, b_arg, b_tt,
                                  iC, iD, KA[0], KA[1], KA[2], KA[3], True, Tb[a], sx0, sx1, sx2, Tb[b], sy0, sy1, sy2, rs)
    if rs[3] > smeta[2]:
        smeta[2] = rs[3]
    if rs[3] > HB.WMAX:
        smeta[3] += 1
    ia = _intern(rs[0], rs[2], tv, sdict, smeta, KA)
    ib = _intern(rs[1], rs[2], tv, sdict, smeta, KA)
    if ia < 0 or ib < 0:
        return -1, -1
    ev2[key] = ia | (ib << 24)
    return ia, ib


# ------------------------------------------------------------------ the panel, classes, deciding fills
@njit(cache=True)
def _sigspec(LA, KA, ev, iC, iD, bx, sp, PANb, PANs):
    sig = 0
    for k in range(6):
        c = eval_code(LA, KA, ev, iC, iD, bx, sp, sp, sp, PANb[k], PANs[k], PANs[k], PANs[k])
        sig |= (c & 1) << k
    c = eval_code(LA, KA, ev, iC, iD, bx, sp, sp, sp, bx, sp, sp, sp)
    sig |= (c & 1) << 6
    return sig


@njit(cache=True)
def _class_of(sig, cref):
    for c in range(6):
        if (sig & 63) == (cref[c] & 63):
            return c if ((sig >> 6) & 1) == ((cref[c] >> 6) & 1) else 7
    return 6


@njit(cache=True)
def _class(T, LA, KA, ev, iC, iD, PANb, PANs, cref, t):
    """Response class of type t against the fixed panel (cached in Tcls): 0 FairBot, 1 PrudentBot, 2 CooperateBot-like,
    3 DefectBot-like, 4 TrustingBot-like, 5 predator-like, 6 other, 7 ambiguous (matches a named class on the six panel
    programs but differs on the stranger copy)."""
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    if Tcls[t] < 0:
        Tcls[t] = _class_of(_sigspec(LA, KA, ev, iC, iD, Tb[t], Ts0[t], PANb, PANs), cref)
    return Tcls[t]


@njit(cache=True)
def _decide_origin(T, LA, KA, ev, iC, iD, PANb, PANs, cref, active, recency, anc_on, t):
    """(origin category, copied flag) of the fill that decides type t's response signature: 0 none (the signature is the
    base's alone), 1 seeded, 2 thanks, 3 grudge, 4 contract, 5 several fills jointly, 6 copied (ancestry not tracked).
    Cached in Tdec / Tcop."""
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    if Tdec[t] >= 0:
        return Tdec[t], Tcop[t]
    sig = _sigspec(LA, KA, ev, iC, iD, Tb[t], Ts0[t], PANb, PANs)
    cat = 0; cop = 0
    if Tn[t] > 0:
        sig0 = _sigspec(LA, KA, ev, iC, iD, Tb[t], np.int64(0), PANb, PANs)
        if sig0 != sig:
            found = -1
            g = np.zeros(4, np.int64)
            for j in range(Tn[t] - 1, -1, -1):
                m = 0
                for q in range(Tn[t]):
                    if q != j:
                        g[m] = Tf[t, q]; m += 1
                for q in range(m, 4):
                    g[q] = 0
                spj = spec_of_beh(g, m, Tg[t], active, recency, -1)
                if _sigspec(LA, KA, ev, iC, iD, Tb[t], spj, PANb, PANs) != sig:
                    found = j
                    break
            if found < 0:
                cat = 5
            else:
                f = Tf[t, found]
                og = H.f_origin(f)
                if H.f_scope(f) == 3 and anc_on == 1:
                    a = kanc(f)
                    cat = 1 if a == 0 else (2 if a == 1 else (3 if a == 2 else 4))
                    cop = kcop(f)
                else:
                    cat = 1 if og == 0 else (4 if og == 3 else (6 if og == 2 else (2 if H.f_action(f) == 1 else 3)))
                    cop = 1 if og == 2 else 0
    Tdec[t] = cat; Tcop[t] = cop
    return cat, cop


# ------------------------------------------------------------------ the island bookkeeping (hooks_w2_kern's)
@njit(cache=True)
def _pay(PAY, c):
    return PAY[c & 1, (c >> 1) & 1]


@njit(cache=True)
def _payT(PAY, c):
    return PAY[(c >> 1) & 1, c & 1]


@njit(cache=True)
def _slot(pres, npres, i, t):
    for s in range(npres[i]):
        if pres[i, s] == t:
            return s
    return -1


@njit(cache=True)
def _slot_at(cnt, npres, i, r):
    acc = 0
    for s in range(npres[i]):
        acc += cnt[i, s]
        if r < acc:
            return s
    return npres[i] - 1


@njit(cache=True)
def _fill_slot(T, LA, KA, ev, iC, iD, active, recency, pres, npres, Cl, i, si):
    t = pres[i, si]
    for x in range(npres[i]):
        c = match(T, LA, KA, ev, iC, iD, active, recency, t, pres[i, x])
        Cl[i, si, x] = c
        Cl[i, x, si] = swap_code(c)


@njit(cache=True)
def _variant_keys(T, active, a, b, K, strict):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    if Tb[a] != Tb[b] or Tl[a] != Tl[b] or Ts0[a] != Ts0[b] or Tss[a] != Tss[b]:
        return -1
    if strict == 1:
        na_ = 0; nb_ = 0
        for j in range(Tn[a]):
            if H.f_scope(Tf[a, j]) != 2:
                na_ += 1
        for j in range(Tn[b]):
            if H.f_scope(Tf[b, j]) != 2:
                nb_ += 1
        if na_ != nb_:
            return -1
        ja = 0; jb = 0
        for q in range(na_):
            while H.f_scope(Tf[a, ja]) == 2:
                ja += 1
            while H.f_scope(Tf[b, jb]) == 2:
                jb += 1
            if Tf[a, ja] != Tf[b, jb]:
                return -1
            ja += 1; jb += 1
    tg = Tg[a]; nk = 0
    for side in range(2):
        x = a if side == 0 else b
        y = b if side == 0 else a
        for j in range(Tn[x]):
            g = Tf[x, j]
            if H.f_scope(g) != 2 or not active[2, H.f_origin(g)] or not (tg >> H.f_tag(g)) & 1:
                continue
            found = False
            for j2 in range(Tn[y]):
                g2 = Tf[y, j2]
                if (H.f_scope(g2) == 2 and active[2, H.f_origin(g2)] and H.f_tag(g2) == H.f_tag(g) and H.f_key(g2) == H.f_key(g)
                        and H.f_action(g2) == H.f_action(g)):
                    found = True
                    break
            if not found:
                k = H.f_key(g)
                if k == Tl[a]:
                    return -1
                dup = False
                for q in range(nk):
                    if K[q] == k:
                        dup = True
                if not dup:
                    K[nk] = k; nk += 1
    return nk


@njit(cache=True)
def _replace(T, tdict, LA, KA, ev, iC, iD, active, recency, PAY, pres, cnt, ps, npres, Cl, vpay, rowb, i, out_t, in_t, strict):
    gcount = T[9]; Tl = T[1]
    so = _slot(pres, npres, i, out_t)
    n0 = npres[i]
    for s in range(n0):
        vpay[s] = _payT(PAY, Cl[i, so, s])
    Kb = np.zeros(8, np.int64)
    nk = -1
    if _slot(pres, npres, i, in_t) < 0:
        nk = _variant_keys(T, active, out_t, in_t, Kb, strict)
        if nk >= 0:
            for x in range(n0):
                rowb[x] = Cl[i, so, x]
    selfc = Cl[i, so, so]
    cnt[i, so] -= 1
    gcount[out_t] -= 1
    moved = -1
    if cnt[i, so] == 0:
        last = n0 - 1
        if so != last:
            pres[i, so] = pres[i, last]; cnt[i, so] = cnt[i, last]; ps[i, so] = ps[i, last]; vpay[so] = vpay[last]
            for x in range(n0):
                Cl[i, so, x] = Cl[i, last, x]
            for x in range(n0):
                Cl[i, x, so] = Cl[i, x, last]
            moved = last
        npres[i] -= 1
    si = _slot(pres, npres, i, in_t)
    new = si < 0
    if new:
        if npres[i] >= pres.shape[1]:
            return False
        si = npres[i]; pres[i, si] = in_t; cnt[i, si] = 0; ps[i, si] = 0.0; npres[i] += 1
        if nk < 0:
            _fill_slot(T, LA, KA, ev, iC, iD, active, recency, pres, npres, Cl, i, si)
        else:
            for x in range(npres[i]):
                t = pres[i, x]
                if x == si or t == out_t:
                    c = selfc
                else:
                    lx = Tl[t]; hit = False
                    for q in range(nk):
                        if Kb[q] == lx:
                            hit = True
                    if hit:
                        c = match(T, LA, KA, ev, iC, iD, active, recency, in_t, t)
                    else:
                        c = rowb[moved] if (moved >= 0 and x == so) else rowb[x]
                Cl[i, si, x] = c
                Cl[i, x, si] = swap_code(c)
    cnt[i, si] += 1
    gcount[in_t] += 1
    for s in range(npres[i]):
        if new and s == si:
            continue
        ps[i, s] += _payT(PAY, Cl[i, si, s]) - vpay[s]
    if new:
        v = 0.0
        for s in range(npres[i]):
            v += cnt[i, s] * _pay(PAY, Cl[i, si, s])
        ps[i, si] = v
    return True


@njit(cache=True)
def _maybe_free(T, tdict, t):
    if T[9][t] == 0:
        free_type(T, tdict, t)


@njit(cache=True)
def _parent(PAY, pres, cnt, ps, npres, Cl, isl, N, w, wbuf):
    m = -1e300
    for s in range(npres[isl]):
        f = (ps[isl, s] - _pay(PAY, Cl[isl, s, s])) / (N - 1)
        if f > m: m = f
    tot = 0.0
    for s in range(npres[isl]):
        f = (ps[isl, s] - _pay(PAY, Cl[isl, s, s])) / (N - 1)
        wbuf[s] = cnt[isl, s] * np.exp(w * (f - m))
        tot += wbuf[s]
    u = np.random.random() * tot; acc = 0.0
    for s in range(npres[isl]):
        acc += wbuf[s]
        if u <= acc:
            return pres[isl, s]
    return pres[isl, npres[isl] - 1]


@njit(cache=True)
def _parent_rej(PAY, pres, cnt, ps, npres, Cl, isl, N, w, fmax):
    while True:
        r = np.random.randint(N)
        s = _slot_at(cnt, npres, isl, r)
        f = (ps[isl, s] - _pay(PAY, Cl[isl, s, s])) / (N - 1)
        if np.random.random() < np.exp(w * (f - fmax)):
            return pres[isl, s]


@njit(cache=True)
def _strip(T, tdict, b_tags, active, recency, t, mode):
    """Offspring keep fills by origin: mode 1 drops written fills (origin 1) as hooks_w2; mode 2 keeps seeded fills only."""
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    g = np.zeros(4, np.int64); m = 0
    for j in range(Tn[t]):
        og = H.f_origin(Tf[t, j])
        drop = (og == 1) if mode == 1 else (og != 0)
        if not drop:
            g[m] = Tf[t, j]; m += 1
    if m == Tn[t]:
        return t
    r = get_type(T, tdict, b_tags, active, recency, Tb[t], Tl[t], g, m)
    return t if r < 0 else r


@njit(cache=True)
def _gentle(T, LA, KA, ev, iC, iD, bD, t):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    if Tgent[t] < 0:
        s = Ts0[t]
        c = eval_code(LA, KA, ev, iC, iD, Tb[t], s, s, s, bD, 0, 0, 0)
        Tgent[t] = c & 1
    return Tgent[t]


# ------------------------------------------------------------------ writes
@njit(cache=True)
def _draw(tvrow, prior, hostile, hk0, hk1, boost):
    """A key id drawn from `prior` restricted to the keys true in tvrow (weights times `boost` for the two hostile keys when
    hostile); -1 if no key is true."""
    tot = 0.0
    for k in range(prior.shape[0]):
        if tvrow[k] and prior[k] > 0:
            w = prior[k] * (boost if (hostile and (k == hk0 or k == hk1)) else 1.0)
            tot += w
    if tot <= 0.0:
        return -1
    u = np.random.random() * tot; acc = 0.0; last = -1
    for k in range(prior.shape[0]):
        if tvrow[k] and prior[k] > 0:
            w = prior[k] * (boost if (hostile and (k == hk0 or k == hk1)) else 1.0)
            acc += w; last = k
            if u <= acc:
                return k
    return last


@njit(cache=True)
def _flagbits(anc_on, anc, cop):
    return ((anc | (cop << 2)) << 12) if anc_on == 1 else 0


@njit(cache=True)
def _trigger(T, tdict, b_tags, LA, KA, ev2, tv, sdict, smeta, iC, iD, D, active, recency, cfg, pres, cnt, npres, N, i, x, y,
             xs, ys, counters, gen, aux):
    """History-triggered write for party x (action xs) against y (action ys): the new type or -1.  aux[0] = 1 if the write
    evicted a fill."""
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    prior_full, prior_noa, sham_off, sham_list, hostile, b_def, b_multi, PANb, PANs, cref = D
    tg = Tg[x]
    aux[0] = 0
    if tg == 0 or xs != 1:
        return -1
    if ys == 0 and cfg[1] == 1:
        act = 0; which = 1
    elif ys == 1 and cfg[2] == 1:
        act = 1; which = 2
    else:
        return -1
    if cfg[18] > 0 and not (cfg[17] <= gen + cfg[19] < cfg[18]):
        counters[23] += 1
        return -1
    t = 0 if tg == 1 else (1 if tg == 2 else np.random.randint(2))
    wm = cfg[11]
    out = np.zeros(4, np.int64)
    anc_on = cfg[14]
    if wm == 0:
        key = Tl[y]
        if cfg[5] == 1:
            key = Tl[pres[i, _slot_at(cnt, npres, i, np.random.randint(N))]]
        newf = 1 + (act | (t << 1) | (2 << 2) | (1 << 4) | (key << 6))
    else:
        ia, ib = read_state(T, LA, KA, ev2, tv, sdict, smeta, iC, iD, active, recency, x, y)
        if ia < 0:
            counters[21] += 1
            return -1
        if wm == 1:
            kk = 9 if tv[ia, 9] else 8
        else:
            prior = prior_noa if wm == 3 else prior_full
            hostile_on = cfg[16] > 1 and act == 0 and b_def[Tb[x], t] == 1
            kk = _draw(tv[ia], prior, hostile_on, hostile[0], hostile[1], float(cfg[16]))
            if kk < 0:
                counters[22] += 1
                return -1
            if wm == 4:
                a0 = sham_off[kk]; a1 = sham_off[kk + 1]
                if a1 > a0:
                    kk = sham_list[a0 + np.random.randint(a1 - a0)]
        newf = 1 + (act | (t << 1) | (3 << 2) | (1 << 4) | ((kk | _flagbits(anc_on, 1 if act == 1 else 2, 0)) << 6))
        counters[17] += 1
    nf, evc, inpl, rej = wfill(Tf[x], Tn[x], newf, out, cfg[15])
    if rej == 1:
        counters[18] += 1
        return -1
    counters[which] += 1; counters[4] += evc; counters[3] += inpl
    aux[0] = evc
    nt = get_type(T, tdict, b_tags, active, recency, Tb[x], Tl[x], out, nf)
    if nt < 0:
        counters[8] += 1
        return -1
    if nt == x:
        counters[10] += 1
        return -1
    return nt


@njit(cache=True)
def _copy(T, tdict, b_tags, active, recency, x, y, counters, keep_origin, anc_on, noevict, aux):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    tg = Tg[x]
    aux[0] = 0
    if tg == 0:
        return -1
    nc = 0
    for j in range(Tn[y]):
        if (tg >> H.f_tag(Tf[y, j])) & 1:
            nc += 1
    if nc == 0:
        return -1
    r = np.random.randint(nc); g = 0
    for j in range(Tn[y]):
        if (tg >> H.f_tag(Tf[y, j])) & 1:
            if r == 0:
                g = Tf[y, j]
                break
            r -= 1
    newf = g if keep_origin == 1 else (((g - 1) & ~np.int64(3 << 4)) | (2 << 4)) + 1
    if anc_on == 1 and H.f_scope(g) == 3:
        newf = ((newf - 1) | (np.int64(1) << 20)) + 1                      # copied flag: key bit 14 = fill bit 20
    out = np.zeros(4, np.int64)
    nf, evc, inpl, rej = wfill(Tf[x], Tn[x], newf, out, noevict)
    if rej == 1:
        counters[19] += 1
        return -1
    counters[4] += evc; counters[3] += inpl
    aux[0] = evc
    nt = get_type(T, tdict, b_tags, active, recency, Tb[x], Tl[x], out, nf)
    if nt < 0:
        counters[8] += 1
        return -1
    if nt == x:
        return -1
    counters[5] += 1
    return nt


@njit(cache=True)
def _cspecs(f, n, g, active_c, recency, lo, lself):
    return (spec_of_beh(f, n, g, active_c, recency, -1), spec_of_beh(f, n, g, active_c, recency, lo),
            spec_of_beh(f, n, g, active_c, recency, lself))


@njit(cache=True)
def _ccode(mode, act, tag, key, anc_on):
    """Contract fill code.  mode 0: lineage technology (history scope, key = partner's lineage, either action); mode 1: the
    legacy open promise (behaviour key 9, action C); modes 2/3: the drawn behavioural key, action C."""
    if mode == 0:
        return 1 + (act | (tag << 1) | (2 << 2) | (3 << 4) | (key << 6))
    if mode == 1:
        return 1 + (1 | (tag << 1) | (3 << 2) | (3 << 4) | ((9 | _flagbits(anc_on, 3, 0)) << 6))
    return 1 + (1 | (tag << 1) | (3 << 2) | (3 << 4) | ((key | _flagbits(anc_on, 3, 0)) << 6))


@njit(cache=True)
def _contract(T, tdict, LA, KA, ev, b_tags, iC, iD, D, active, active_c, recency, PAY, a, b, counters, res, cmode, anc_on,
              noevict, gen, cfg):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    prior_full, prior_noa = D[0], D[1]
    counters[6] += 1
    res[0] = -1; res[1] = -1
    if cfg[18] > 0 and not (cfg[17] <= gen + cfg[19] < cfg[18]):
        counters[23] += 1
        return
    la = Tl[a]; lb = Tl[b]; ga = Tg[a]; gb = Tg[b]
    a0, a1, a2 = _cspecs(Tf[a], Tn[a], ga, active_c, recency, lb, la)
    b0, b1, b2 = _cspecs(Tf[b], Tn[b], gb, active_c, recency, la, lb)
    c0 = eval_code(LA, KA, ev, iC, iD, Tb[a], a0, a1, a2, Tb[b], b0, b1, b2)
    pa0 = PAY[c0 & 1, (c0 >> 1) & 1]; pb0 = PAY[(c0 >> 1) & 1, c0 & 1]
    acc = np.zeros((16, 4), np.int64); nacc = 0
    fa = np.zeros(4, np.int64); fb = np.zeros(4, np.int64)
    ka = 0; kb = 0
    if cmode >= 2:
        prior = prior_noa if cmode == 3 else prior_full
        tvall = np.ones(prior.shape[0], np.bool_)
        ka = _draw(tvall, prior, False, -1, -1, 1.0); kb = _draw(tvall, prior, False, -1, -1, 1.0)
    lo_a = 1 if cmode >= 1 else 0
    for ta in range(2):
        if not (ga >> ta) & 1:
            continue
        for aa in range(lo_a, 2):
            na, e1, i1, r1 = wfill(Tf[a], Tn[a], _ccode(cmode, aa, ta, lb if cmode == 0 else ka, anc_on), fa, noevict)
            if r1 == 1:
                counters[20] += 1
                continue
            sa0, sa1, sa2 = _cspecs(fa, na, ga, active_c, recency, lb, la)
            for tb in range(2):
                if not (gb >> tb) & 1:
                    continue
                for ab in range(lo_a, 2):
                    nb, e2, i2, r2 = wfill(Tf[b], Tn[b], _ccode(cmode, ab, tb, la if cmode == 0 else kb, anc_on), fb, noevict)
                    if r2 == 1:
                        counters[20] += 1
                        continue
                    sb0, sb1, sb2 = _cspecs(fb, nb, gb, active_c, recency, la, lb)
                    counters[11] += 1
                    c = eval_code(LA, KA, ev, iC, iD, Tb[a], sa0, sa1, sa2, Tb[b], sb0, sb1, sb2)
                    pa = PAY[c & 1, (c >> 1) & 1]; pb = PAY[(c >> 1) & 1, c & 1]
                    if pa >= pa0 and pb >= pb0 and (pa > pa0 or pb > pb0):
                        acc[nacc, 0] = ta; acc[nacc, 1] = aa; acc[nacc, 2] = tb; acc[nacc, 3] = ab; nacc += 1
    if nacc == 0:
        return
    k = np.random.randint(nacc)
    ta = acc[k, 0]; aa = acc[k, 1]; tb = acc[k, 2]; ab = acc[k, 3]
    na, e1, i1, r1 = wfill(Tf[a], Tn[a], _ccode(cmode, aa, ta, lb if cmode == 0 else ka, anc_on), fa, noevict)
    nb, e2, i2, r2 = wfill(Tf[b], Tn[b], _ccode(cmode, ab, tb, la if cmode == 0 else kb, anc_on), fb, noevict)
    counters[4] += e1 + e2; counters[3] += i1 + i2
    xa = get_type(T, tdict, b_tags, active, recency, Tb[a], la, fa, na)
    if xa < 0:
        counters[8] += 1
        return
    xb = get_type(T, tdict, b_tags, active, recency, Tb[b], lb, fb, nb)
    if xb < 0:
        counters[8] += 1
        if gcount[xa] == 0 and xa != a:
            free_type(T, tdict, xa)
        return
    counters[7] += 1
    res[0] = xa; res[1] = xb


# ------------------------------------------------------------------ records
@njit(cache=True)
def _record(T, LA, KA, ev, iC, iD, bD, PAY, D, active, recency, cfg, pres, cnt, ps, npres, Cl, N, rec_i, rec_g, rec_c, rec_t):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    PANb, PANs, cref = D[7], D[8], D[9]
    I = pres.shape[0]
    tot = 0.0; gent = 0.0; gh = 0.0; hh = 0.0; nfil = 0.0; ntp = 0
    ho = 0.0; hoc = 0.0; hlc = 0.0; how = 0.0
    for i in range(I):
        n = npres[i]; ntp += n
        cc = 0.0; pay = 0.0
        for s in range(n):
            pay += cnt[i, s] * (ps[i, s] - _pay(PAY, Cl[i, s, s])) / (N - 1)
            for s2 in range(n):
                if (Cl[i, s, s2] & 3) == 3:
                    nn = cnt[i, s] * cnt[i, s2] if s != s2 else cnt[i, s] * (cnt[i, s] - 1)
                    cc += nn
        rec_i[i, 0] = cc / (N * (N - 1.0)); rec_i[i, 1] = pay / N
        lins = np.empty(n, np.int64); lc = np.empty(n, np.int64)
        for s in range(n):
            lins[s] = Tl[pres[i, s]]; lc[s] = cnt[i, s]
        order = np.argsort(lins)
        nl = 0; simp = 0.0; cur = -1; acc = 0
        for q in range(n):
            s = order[q]
            if q == 0 or lins[s] != cur:
                if q > 0:
                    simp += (acc / N) ** 2
                cur = lins[s]; acc = 0; nl += 1
            acc += lc[s]
        simp += (acc / N) ** 2
        rec_i[i, 2] = nl; rec_i[i, 3] = simp
        big = 0
        for s in range(n):
            if cnt[i, s] > cnt[i, big]:
                big = s
        rec_i[i, 4] = pres[i, big]; rec_i[i, 5] = cnt[i, big]; rec_i[i, 6] = n
        for s in range(n):
            a = pres[i, s]; c = cnt[i, s]
            tot += c
            gt = _gentle(T, LA, KA, ev, iC, iD, bD, a)
            hashist = False
            fo = False; foc = False; flc = False; fow = False
            for j in range(Tn[a]):
                g = Tf[a, j]
                carried = (Tg[a] >> H.f_tag(g)) & 1
                if carried == 1 and H.f_scope(g) == 3 and kid_of(g) >= 8:
                    fo = True
                    if H.f_origin(g) == 3: foc = True
                    if H.f_origin(g) == 1: fow = True
                if carried == 1 and H.f_scope(g) == 2 and H.f_origin(g) == 3:
                    flc = True
                rec_g[carried * 32 + H.f_scope(g) * 8 + H.f_origin(g) * 2 + H.f_action(g)] += c
                if H.f_scope(g) == 2:
                    hashist = True
            nfil += c * Tn[a]
            if fo: ho += c
            if foc: hoc += c
            if flc: hlc += c
            if fow: how += c
            if gt == 1:
                gent += c
                if hashist:
                    gh += c
            if hashist:
                hh += c
            if cfg[20] == 1:
                k = _class(T, LA, KA, ev, iC, iD, PANb, PANs, cref, a)
                rec_c[i, k] += c
                cat, cp = _decide_origin(T, LA, KA, ev, iC, iD, PANb, PANs, cref, active, recency, cfg[14], a)
                rec_t[k, cat, cp] += c
    rec_g[64] = gent / tot; rec_g[65] = gh / tot; rec_g[66] = ntp; rec_g[67] = nfil / tot; rec_g[68] = hh / tot
    rec_g[69] = meta[0] - meta[1]
    rec_g[70] = ho / tot; rec_g[71] = hoc / tot; rec_g[72] = hlc / tot; rec_g[73] = how / tot


@njit(cache=True)
def _log_conv(conv, kind, evc, multi, cf, ct):
    conv[kind, evc, multi, cf, ct] += 1


@njit(cache=True)
def kernel(LA, KA, b_tags, iC, iD, bD, T, tdict, ev, ev2, tv, sdict, smeta, D, active, cfg, copy_q, PAY, pres, cnt, ps, npres,
           Cl, N, w, m, gens, seed, checks, rec_isl, rec_glob, rec_cls, rec_tab, enc_stats, counters, conv):
    """Runs gens generations; records at the generations listed in checks (0 = before the first generation).  Returns the number
    of records written (fewer if a capacity overflowed: counters[8] > 0 then)."""
    np.random.seed(seed)
    I = pres.shape[0]
    recency = cfg[0]
    active_c = active.copy()
    active_c[2, 3] = True
    active_c[3, 3] = True
    strict = cfg[13]
    cmode = cfg[12]
    anc_on = cfg[14]
    noevict = cfg[15]
    logc = cfg[20]
    prior_full, prior_noa, sham_off, sham_list, hostile, b_def, b_multi, PANb, PANs, cref = D
    vpay = np.zeros(pres.shape[1] + 1)
    rowb = np.zeros(pres.shape[1] + 1, np.int64)
    wbuf = np.zeros(pres.shape[1] + 1)
    fmax = PAY.max()
    aux = np.zeros(2, np.int64)
    if cfg[8] == 1:
        for i in range(I):
            for s in range(npres[i]):
                _fill_slot(T, LA, KA, ev, iC, iD, active, recency, pres, npres, Cl, i, s)
            for s in range(npres[i]):
                v = 0.0
                for s2 in range(npres[i]):
                    v += cnt[i, s2] * _pay(PAY, Cl[i, s, s2])
                ps[i, s] = v
    ci = 0
    if ci < checks.shape[0] and checks[ci] == 0:
        _record(T, LA, KA, ev, iC, iD, bD, PAY, D, active, recency, cfg, pres, cnt, ps, npres, Cl, N, rec_isl[ci], rec_glob[ci], rec_cls[ci], rec_tab[ci])
        ci += 1
    res = np.zeros(2, np.int64)
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel, Tcls, Tdec, Tcop = T
    for g in range(gens):
        for e in range(I * N):
            i = np.random.randint(I)
            src = i
            if m > 0.0 and I > 1 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            if cfg[9] == 1:
                child = _parent_rej(PAY, pres, cnt, ps, npres, Cl, src, N, w, fmax)
            else:
                child = _parent(PAY, pres, cnt, ps, npres, Cl, src, N, w, wbuf)
            if cfg[6] >= 1:
                child = _strip(T, tdict, b_tags, active, recency, child, cfg[6])
            u = np.random.randint(N); acc = 0; victim = pres[i, 0]
            for s in range(npres[i]):
                acc += cnt[i, s]
                if u < acc:
                    victim = pres[i, s]
                    break
            if victim != child:
                if logc == 1:
                    cv = _class(T, LA, KA, ev, iC, iD, PANb, PANs, cref, victim)
                    cch = _class(T, LA, KA, ev, iC, iD, PANb, PANs, cref, child)
                    _log_conv(conv, 4, 0, b_multi[Tb[child]], cv, cch)
                if not _replace(T, tdict, LA, KA, ev, iC, iD, active, recency, PAY, pres, cnt, ps, npres, Cl, vpay, rowb, i, victim, child, strict):
                    counters[8] += 1
                    return ci
                _maybe_free(T, tdict, victim)
            if cfg[7] == 0:
                continue
            # ---- one sampled encounter on island i
            r1 = np.random.randint(N); r2 = np.random.randint(N - 1)
            if r2 >= r1: r2 += 1
            sa = _slot_at(cnt, npres, i, r1); sb = _slot_at(cnt, npres, i, r2)
            a = pres[i, sa]; b = pres[i, sb]
            code = Cl[i, sa, sb]
            xa = code & 1; xb = (code >> 1) & 1
            counters[0] += 1
            for sd in range(2):
                tq = a if sd == 0 else b
                me = xa if sd == 0 else xb
                ot = xb if sd == 0 else xa
                ho_ = False; hl_ = False
                for j in range(Tn[tq]):
                    gf = Tf[tq, j]
                    enc_stats[0, H.f_scope(gf), H.f_origin(gf)] += 1
                    if H.f_origin(gf) == 3 and ((Tg[tq] >> H.f_tag(gf)) & 1):
                        if H.f_scope(gf) == 3 and kid_of(gf) >= 8:
                            ho_ = True
                        if H.f_scope(gf) == 2:
                            hl_ = True
                if ho_:
                    counters[13] += 1
                    if me == 1 and ot == 0:
                        counters[14] += 1
                if hl_:
                    counters[15] += 1
                    if me == 1 and ot == 0:
                        counters[16] += 1
            exa = False; exb = False
            if Tn[a] > 0:
                c2 = eval_code(LA, KA, ev, iC, iD, Tb[a], 0, 0, 0, Tb[b], Ts0[b], spec_ctx(T, active, recency, b, Tl[a]), Tss[b])
                exa = (c2 & 3) != (code & 3)
            if Tn[b] > 0:
                c2 = eval_code(LA, KA, ev, iC, iD, Tb[a], Ts0[a], spec_ctx(T, active, recency, a, Tl[b]), Tss[a], Tb[b], 0, 0, 0)
                exb = (c2 & 3) != (code & 3)
            if exa or exb:
                counters[9] += 1
            na = -1; nb = -1
            kind_a = -1; kind_b = -1; evc_a = 0; evc_b = 0
            if cfg[3] == 1 and Tg[a] > 0 and Tg[b] > 0 and not (xa == 1 and xb == 1):
                _contract(T, tdict, LA, KA, ev, b_tags, iC, iD, D, active, active_c, recency, PAY, a, b, counters, res, cmode, anc_on, noevict, g, cfg)
                na = res[0]; nb = res[1]
                if na >= 0:
                    kind_a = 3; kind_b = 3
            if na < 0:
                na = _trigger(T, tdict, b_tags, LA, KA, ev2, tv, sdict, smeta, iC, iD, D, active, recency, cfg, pres, cnt, npres, N, i, a, b, xa, xb, counters, g, aux)
                if na >= 0:
                    kind_a = 0 if xb == 1 else 1; evc_a = aux[0]
            if nb < 0:
                nb = _trigger(T, tdict, b_tags, LA, KA, ev2, tv, sdict, smeta, iC, iD, D, active, recency, cfg, pres, cnt, npres, N, i, b, a, xb, xa, counters, g, aux)
                if nb >= 0:
                    kind_b = 0 if xa == 1 else 1; evc_b = aux[0]
            if na < 0 and cfg[4] == 1 and np.random.random() < copy_q:
                na = _copy(T, tdict, b_tags, active, recency, a, b, counters, cfg[10], anc_on, noevict, aux)
                if na >= 0:
                    kind_a = 2; evc_a = aux[0]
            if nb < 0 and cfg[4] == 1 and np.random.random() < copy_q:
                nb = _copy(T, tdict, b_tags, active, recency, b, a, counters, cfg[10], anc_on, noevict, aux)
                if nb >= 0:
                    kind_b = 2; evc_b = aux[0]
            if logc == 1:
                if na >= 0:
                    _log_conv(conv, kind_a, evc_a, b_multi[Tb[a]], _class(T, LA, KA, ev, iC, iD, PANb, PANs, cref, a), _class(T, LA, KA, ev, iC, iD, PANb, PANs, cref, na))
                if nb >= 0:
                    _log_conv(conv, kind_b, evc_b, b_multi[Tb[b]], _class(T, LA, KA, ev, iC, iD, PANb, PANs, cref, b), _class(T, LA, KA, ev, iC, iD, PANb, PANs, cref, nb))
            if na >= 0:
                if not _replace(T, tdict, LA, KA, ev, iC, iD, active, recency, PAY, pres, cnt, ps, npres, Cl, vpay, rowb, i, a, na, strict):
                    counters[8] += 1
                    return ci
            if nb >= 0:
                if not _replace(T, tdict, LA, KA, ev, iC, iD, active, recency, PAY, pres, cnt, ps, npres, Cl, vpay, rowb, i, b, nb, strict):
                    counters[8] += 1
                    return ci
            if na >= 0:
                _maybe_free(T, tdict, a)
            if nb >= 0:
                _maybe_free(T, tdict, b)
        if ci < checks.shape[0] and g + 1 == checks[ci]:
            _record(T, LA, KA, ev, iC, iD, bD, PAY, D, active, recency, cfg, pres, cnt, ps, npres, Cl, N, rec_isl[ci], rec_glob[ci], rec_cls[ci], rec_tab[ci])
            ci += 1
        if len(ev) > 1500000:
            ev.clear()
        if len(ev2) > 2000000:
            ev2.clear()
    return ci
