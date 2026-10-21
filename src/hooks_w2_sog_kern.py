"""Hooks, Part W2: copy of hooks_w_sog_kern.py with union contracts (notes/hooks-w2.md §1.4-§1.7).  Additions:
cfg[10] union contracts (0 off, 1 myopic (M), 2 credible response (C)), cfg[11] role key (union fills and the boss's
response keyed on role instead of on lineages), cfg[12] protection of the boss's contract-origin fills against trigger
writes and copies; worker demand fills (action 2 / 3) are always protected the same way.  counters 11 union attempts
blocked, 18 writes blocked by protection.  ustat (int64): 0 union attempts (both workers carry a tag), 1 candidates
evaluated, 2/3 accepted contracts at s = 1/4, 1/2, 4 accepted with a boss response fill, 5 accepted with demand above
the pre-contract wage (raise), 6 accepted with demand at or below it (taming), 7 raises against a constant boss
(boss program without atoms and no behaviour-scope fill), 8 accepted against a constant boss, 9-11 predicted wage
index histogram at acceptance, 12-14 pre-contract wage histogram at acceptance, 15/16 challenges (a held demand fill
selected on path) at s = 1/4, 1/2, 17/18 executions (the worker strikes), 19/20 demand met (realized wage >= s),
21-23 / 24-26 realized wage index histograms under challenge at s = 1/4 / 1/2, 27 candidate (C) responses that
were a fill, 28 unused, 30/31 acceptable candidates (before the uniform draw) at s = 1/4, 1/2.

Part W doc:
Hooks, Part W: the social organization island kernel over types (slot, base, lineage, fills).

Law: sog_lottery.kern's (CC, c = 0.5): a birth event picks an (island, slot) unit uniformly; with probability m the
parent comes from a uniformly chosen other island's same slot; the parent is drawn with weight count * exp(w f), f the
expected payoff against a uniform draw of one member of each other slot on the source island; the victim is uniform
in the unit.  A generation is 3 I N births.  After every birth one encounter is sampled on the birth island (one member
per slot, uniform), in which history-triggered writes (second review, amendment 4), worker copying and boss-worker
contracts change fills (notes/hooks-w.md §1.7, §2.6).  Each island keeps the joint codes of its present triples in a
dense tensor J[i, b, w1, w2]; a new type that is a history variant of the writer's old type copies the old slice.

Type table T = (Ts slot, Tb base, Tl lineage, Tf fills (cap, 4), Tn, Tg hook tags, Tut union tag, Th has active
carried history fills, Tbb (cap, 128) and Trn (cap, 2) the resolution structure without history (see _struct), Rsig
its signature, gcount, meta, freel).  A resolution table for given partner lineages is built from the structure and
the matching history fills in O(fills); its hash (the eval-cache key) needs no table at all.
cfg: 0 recency, 1 grudge writes, 2 thanks writes, 3 contracts, 4 copying, 5 shuffled keys, 6 written fills not
inherited, 7 encounters, 8 initialize, 9 copies keep the copied fill's origin.
counters: 0 encounters, 1 grudge writes, 2 thanks writes, 3 in-place updates, 4 evictions, 5 copies, 6 contract
attempts, 7 contracts, 8 overflow, 9 encounters changed by a fill, 10 writes that changed nothing.
thr[s, q]: per slot s, threat fills: 0 held (fill-encounters), 1 held and active, 2 challenged (selected on path),
3 executed (the threatened act realized).
enc_stats[level, scope, origin]: 0 held, 1 selected on path, 2 executed (outcome differs with the party's fills inert).
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from numba import njit
from hooks_w2_sog import (resolve, rhash, eval_triple, g_action, g_tag, g_scope, g_origin, g_key, RSZ)

NST = 16


@njit(cache=True)
def _tkey(s, base, lin, g):
    return (np.int64((s << 60) | (base << 32) | lin), np.int64(g[0] | (g[1] << 32)), np.int64(g[2] | (g[3] << 32)))


@njit(cache=True)
def _hasactivehist(f, nf, tags, active):
    for j in range(nf):
        if g_scope(f[j]) == 2 and active[2, g_origin(f[j])] and (tags >> g_tag(f[j])) & 1:
            return True
    return False


@njit(cache=True)
def get_type(T, tdict, htags, wtag, active, recency, s, base, lin, f, nf):
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    g = np.zeros(4, np.int64)
    for j in range(nf):
        g[j] = f[j]
    key = _tkey(s, base, lin, g)
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
    Ts[t] = s; Tb[t] = base; Tl[t] = lin; Tn[t] = nf
    for j in range(4):
        Tf[t, j] = g[j]
    tg = htags[0 if s == 0 else 1, base]
    Tg[t] = tg
    Tut[t] = wtag[base] if s > 0 else 0
    Th[t] = _hasactivehist(g, nf, tg, active)
    _struct(g, nf, tg, s, active, recency, Tbb[t], Trn[t])
    Rsig[t] = _sig(Tbb[t], Trn[t], g, nf, recency)
    gcount[t] = 0
    tdict[key] = t
    return t


@njit(cache=True)
def free_type(T, tdict, t):
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    key = _tkey(Ts[t], Tb[t], Tl[t], Tf[t])
    if key in tdict and tdict[key] == t:
        tdict.pop(key)
        freel[meta[1]] = t
        meta[1] += 1


@njit(cache=True)
def _struct(f, nf, tags, slot, active, recency, bb, rn):
    """Resolution structure without history.  bb[b0*16 + b1*2 + t]: specific rule: the most recent applicable
    behaviour fill; recency rule: the most recent applicable non-history fill (-1: none).  rn[t]: specific rule: the
    selected role-or-none fill (role beats none, ties by recency); recency rule: -1."""
    for t in range(2):
        rn[t] = -1
        if recency == 0 and (tags >> t) & 1:
            bestp = -1
            for j in range(nf - 1, -1, -1):
                g = f[j]
                if g_tag(g) != t or not active[g_scope(g), g_origin(g)]:
                    continue
                sc = g_scope(g)
                if sc == 0:
                    pr = 0
                elif sc == 1 and g_key(g) == slot:
                    pr = 1
                else:
                    continue
                if pr > bestp:
                    bestp = pr; rn[t] = j
    for b0 in range(8):
        for b1 in range(8):
            for t in range(2):
                best = -1
                if (tags >> t) & 1:
                    for j in range(nf - 1, -1, -1):
                        g = f[j]
                        if g_tag(g) != t or not active[g_scope(g), g_origin(g)]:
                            continue
                        sc = g_scope(g); k = g_key(g)
                        if sc == 3:
                            if (k // 8 == 0 and k % 8 == b0) or (k // 8 == 1 and k % 8 == b1):
                                best = j
                                break
                        elif recency == 1 and (sc == 0 or (sc == 1 and k == slot)):
                            best = j
                            break
                bb[b0 * 16 + b1 * 2 + t] = best


@njit(cache=True)
def _mix(h, v):
    return (h ^ (v + 7)) * np.int64(1099511628211)


@njit(cache=True)
def _sig(bb, rn, f, nf, recency):
    """Signature of the no-history resolution.  Specific rule (canonical): the table R0 (behaviour fill's action where
    one applies, else the role-or-none fill's) and the mask of entries set by behaviour fills, which with the actions
    of the applicable history fills determine every table.  Recency rule: the index tables and the fills' actions."""
    h = np.int64(-3750763034362895579)
    if recency == 1:
        for i in range(128):
            h = _mix(h, bb[i])
        for j in range(nf):
            h = _mix(h, g_action(f[j]))
        return h
    for i in range(128):
        t = i & 1
        j = bb[i]
        if j >= 0:
            h = _mix(h, 100 + g_action(f[j]))
        else:
            h = _mix(h, g_action(f[rn[t]]) if rn[t] >= 0 else -1)
    return h


@njit(cache=True)
def _hidx(T, active, t, l, tag):
    """Most recent active history fill of type t on a carried tag `tag` keyed on lineage l (-1: none)."""
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    if l < 0 or not Th[t] or not (Tg[t] >> tag) & 1:
        return -1
    for j in range(Tn[t] - 1, -1, -1):
        g = Tf[t, j]
        if g_scope(g) == 2 and g_tag(g) == tag and g_key(g) == l and active[2, g_origin(g)]:
            return j
    return -1


@njit(cache=True)
def rkey(T, active, recency, t, l0, l1):
    """Hash of type t's resolution table with partner lineages (l0, l1).  Specific rule: the signature and, per tag,
    the actions of the applicable history fill for partner 0, partner 1 and both (the more recent); recency rule: the
    signature and the indices of the applicable history fills."""
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    h = Rsig[t]
    if Th[t]:
        for tag in range(2):
            i0 = _hidx(T, active, t, l0, tag); i1 = _hidx(T, active, t, l1, tag)
            if recency == 1:
                h = _mix(h, i0); h = _mix(h, i1)
            else:
                a0 = g_action(Tf[t, i0]) if i0 >= 0 else -1
                a1 = g_action(Tf[t, i1]) if i1 >= 0 else -1
                ib = i0 if i0 > i1 else i1
                ab = g_action(Tf[t, ib]) if ib >= 0 else -1
                h = _mix(h, a0); h = _mix(h, a1); h = _mix(h, ab)
    return h


@njit(cache=True)
def rbuild(T, active, recency, t, l0, l1, R):
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    h0 = np.zeros(2, np.int64); h1 = np.zeros(2, np.int64)
    for tag in range(2):
        h0[tag] = _hidx(T, active, t, l0, tag); h1[tag] = _hidx(T, active, t, l1, tag)
    for ctx in range(4):
        for b0 in range(8):
            for b1 in range(8):
                for tag in range(2):
                    hist = -1
                    if ctx & 1:
                        hist = h0[tag]
                    if (ctx & 2) and h1[tag] > hist:
                        hist = h1[tag]
                    bb = Tbb[t, b0 * 16 + b1 * 2 + tag]
                    if recency == 1:
                        j = bb if bb > hist else hist
                    else:
                        j = bb if bb >= 0 else (hist if hist >= 0 else Trn[t, tag])
                    R[ctx * 128 + b0 * 16 + b1 * 2 + tag] = g_action(Tf[t, j]) if j >= 0 else -1


@njit(cache=True)
def triple_code(T, LA, TT, ev, active, recency, b, x, y, Rb, Rx, Ry, Rall):
    """Full code of the triple (b, x, y) under current fills and lineages, cached by bases and resolution keys."""
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    lb = Tl[b]; lx = Tl[x]; ly = Tl[y]
    hb = rkey(T, active, recency, b, lx, ly); hx = rkey(T, active, recency, x, lb, ly)
    hy = rkey(T, active, recency, y, lb, lx)
    key = (np.int64(Tb[b]), hb, np.int64(Tb[x]), hx, np.int64(Tb[y]), hy)
    if key in ev:
        return ev[key]
    rbuild(T, active, recency, b, lx, ly, Rall[0]); rbuild(T, active, recency, x, lb, ly, Rall[1])
    rbuild(T, active, recency, y, lb, lx, Rall[2])
    nat, atP, atL, tab = LA
    c = eval_triple(nat, atP, atL, tab, TT, Tb[b], Tb[x], Tb[y], Tut[x], Tut[y], Rall)
    ev[key] = c
    return c


@njit(cache=True)
def inert_code(T, LA, TT, ev, active, recency, b, x, y, who, Rall, hz):
    """Code of the triple with party `who` (0, 1, 2) playing its defaults (all its fills inert)."""
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    lb = Tl[b]; lx = Tl[x]; ly = Tl[y]
    hb = hz if who == 0 else rkey(T, active, recency, b, lx, ly)
    hx = hz if who == 1 else rkey(T, active, recency, x, lb, ly)
    hy = hz if who == 2 else rkey(T, active, recency, y, lb, lx)
    key = (np.int64(Tb[b]), hb, np.int64(Tb[x]), hx, np.int64(Tb[y]), hy)
    if key in ev:
        return ev[key]
    if who == 0:
        Rall[0, :] = -1
    else:
        rbuild(T, active, recency, b, lx, ly, Rall[0])
    if who == 1:
        Rall[1, :] = -1
    else:
        rbuild(T, active, recency, x, lb, ly, Rall[1])
    if who == 2:
        Rall[2, :] = -1
    else:
        rbuild(T, active, recency, y, lb, lx, Rall[2])
    nat, atP, atL, tab = LA
    c = eval_triple(nat, atP, atL, tab, TT, Tb[b], Tb[x], Tb[y], Tut[x], Tut[y], Rall)
    ev[key] = c
    return c


@njit(cache=True)
def code_with(LA, TT, ev, bb, hb, tb, bx, hx, tx, ux, by, hy, ty, uy, Rall):
    key = (np.int64(bb), hb, np.int64(bx), hx, np.int64(by), hy)
    if key in ev:
        return ev[key]
    for i in range(RSZ):
        Rall[0, i] = tb[i]; Rall[1, i] = tx[i]; Rall[2, i] = ty[i]
    nat, atP, atL, tab = LA
    c = eval_triple(nat, atP, atL, tab, TT, bb, bx, by, ux, uy, Rall)
    ev[key] = c
    return c


@njit(cache=True)
def _pay_slot(PAY, T, code, x, y, s):
    """Payoff to slot s at joint code (low 6 bits of code), workers x (W1), y (W2)."""
    return PAY[code & 63, T[6][x], T[6][y], s]


@njit(cache=True)
def _slot(pres, npres, i, s, t):
    for q in range(npres[i, s]):
        if pres[i, s, q] == t:
            return q
    return -1


@njit(cache=True)
def _slot_at(cnt, npres, i, s, r):
    acc = 0
    for q in range(npres[i, s]):
        acc += cnt[i, s, q]
        if r < acc:
            return q
    return npres[i, s] - 1


@njit(cache=True)
def _jget(J, i, s, k, p, q):
    """J entry with slot s's slot index k and the other two slots' indices p (lower slot) and q (higher slot)."""
    if s == 0:
        return J[i, k, p, q]
    if s == 1:
        return J[i, p, k, q]
    return J[i, p, q, k]


@njit(cache=True)
def _jset(J, i, s, k, p, q, c):
    if s == 0:
        J[i, k, p, q] = c
    elif s == 1:
        J[i, p, k, q] = c
    else:
        J[i, p, q, k] = c


@njit(cache=True)
def _others(s):
    if s == 0:
        return 1, 2
    if s == 1:
        return 0, 2
    return 0, 1


@njit(cache=True)
def _trip(s, k, p, q):
    """(boss, w1, w2) from slot s's element k and the other slots' elements p, q."""
    if s == 0:
        return k, p, q
    if s == 1:
        return p, k, q
    return p, q, k


@njit(cache=True)
def _fill_slice(T, LA, TT, ev, active, recency, pres, npres, J, i, s, k, nk, Kb, rowb, Rb, Rx, Ry, Rall):
    """J entries of slot s's element k against every present pair of the other two slots.  nk >= 0: a history
    variant with changed lineages Kb[:nk] and its old slice in rowb (indexed by the other slots' indices)."""
    o1, o2 = _others(s)
    Tl = T[2]
    t = pres[i, s, k]
    for p in range(npres[i, o1]):
        tp = pres[i, o1, p]
        for q in range(npres[i, o2]):
            tq = pres[i, o2, q]
            if nk >= 0:
                hit = False
                for r in range(nk):
                    if Kb[r] == Tl[tp] or Kb[r] == Tl[tq]:
                        hit = True
                if not hit and rowb[p, q] >= 0:
                    _jset(J, i, s, k, p, q, rowb[p, q])
                    continue
            b, x, y = _trip(s, t, tp, tq)
            c = triple_code(T, LA, TT, ev, active, recency, b, x, y, Rb, Rx, Ry, Rall)
            _jset(J, i, s, k, p, q, c & 32767)


@njit(cache=True)
def _variant(T, active, a, b, Kb):
    """History variant test (as hooks_w_kern._variant_keys): same slot, base, lineage and no-history resolution."""
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    if Ts[a] != Ts[b] or Tb[a] != Tb[b] or Tl[a] != Tl[b]:
        return -1
    ja = 0; jb = 0
    while True:
        while ja < Tn[a] and g_scope(Tf[a, ja]) == 2:
            ja += 1
        while jb < Tn[b] and g_scope(Tf[b, jb]) == 2:
            jb += 1
        if ja >= Tn[a] or jb >= Tn[b]:
            break
        if Tf[a, ja] != Tf[b, jb]:
            return -1
        ja += 1; jb += 1
    if ja < Tn[a] or jb < Tn[b]:
        return -1
    tg = Tg[a]; nk = 0
    for side in range(2):
        x = a if side == 0 else b
        y = b if side == 0 else a
        for j in range(Tn[x]):
            g = Tf[x, j]
            if g_scope(g) != 2 or not active[2, g_origin(g)] or not (tg >> g_tag(g)) & 1:
                continue
            found = False
            for j2 in range(Tn[y]):
                g2 = Tf[y, j2]
                if g2 == g or (g_scope(g2) == 2 and active[2, g_origin(g2)] and g_tag(g2) == g_tag(g)
                               and g_key(g2) == g_key(g) and g_action(g2) == g_action(g)):
                    found = True
                    break
            if not found:
                k = g_key(g)
                if k == Tl[a]:
                    return -1
                dup = False
                for q in range(nk):
                    if Kb[q] == k:
                        dup = True
                if not dup:
                    if nk >= Kb.shape[0]:
                        return -1
                    Kb[nk] = k; nk += 1
    return nk


@njit(cache=True)
def _fit(PAY, T, pres, cnt, npres, J, i, s, k):
    o1, o2 = _others(s)
    v = 0.0
    for p in range(npres[i, o1]):
        for q in range(npres[i, o2]):
            c = _jget(J, i, s, k, p, q)
            b, x, y = _trip(s, pres[i, s, k], pres[i, o1, p], pres[i, o2, q])
            v += cnt[i, o1, p] * cnt[i, o2, q] * PAY[c & 63, T[6][x], T[6][y], s]
    return v


@njit(cache=True)
def _contrib(PAY, T, pres, cnt, npres, J, F, i, s, k, sign):
    """Add sign * (contribution of slot s's element k, one member) to the fitness sums of the other two slots."""
    o1, o2 = _others(s)
    t = pres[i, s, k]
    for sa in (o1, o2):
        sb = o1 + o2 - sa
        for ka in range(npres[i, sa]):
            ta = pres[i, sa, ka]
            v = 0.0
            for kb in range(npres[i, sb]):
                tb = pres[i, sb, kb]
                # indices in J order
                if s == 0:
                    c = J[i, k, ka, kb] if sa == 1 else J[i, k, kb, ka]
                elif s == 1:
                    c = J[i, ka, k, kb] if sa == 0 else J[i, kb, k, ka]
                else:
                    c = J[i, ka, kb, k] if sa == 0 else J[i, kb, ka, k]
                if s == 0:
                    x = ta if sa == 1 else tb; y = tb if sa == 1 else ta
                elif s == 1:
                    x = t; y = tb if sa == 0 else ta
                else:
                    x = tb if sa == 0 else ta; y = t
                v += cnt[i, sb, kb] * PAY[c & 63, T[6][x], T[6][y], sa]
            F[i, sa, ka] += sign * v


@njit(cache=True)
def _replace(T, tdict, LA, TT, ev, active, recency, PAY, pres, cnt, npres, J, F, i, s, out_t, in_t, Kb, rowb, Rb, Rx, Ry, Rall):
    gcount = T[11]
    o1, o2 = _others(s)
    so = _slot(pres, npres, i, s, out_t)
    # remove one out_t: subtract its contribution
    _contrib(PAY, T, pres, cnt, npres, J, F, i, s, so, -1.0)
    nk = -1
    if _slot(pres, npres, i, s, in_t) < 0:
        nk = _variant(T, active, out_t, in_t, Kb)
        if nk >= 0:
            for p in range(npres[i, o1]):
                for q in range(npres[i, o2]):
                    rowb[p, q] = _jget(J, i, s, so, p, q)
    cnt[i, s, so] -= 1
    gcount[out_t] -= 1
    if cnt[i, s, so] == 0:
        last = npres[i, s] - 1
        if so != last:
            pres[i, s, so] = pres[i, s, last]; cnt[i, s, so] = cnt[i, s, last]; F[i, s, so] = F[i, s, last]
            for p in range(npres[i, o1]):
                for q in range(npres[i, o2]):
                    _jset(J, i, s, so, p, q, _jget(J, i, s, last, p, q))
        npres[i, s] -= 1
    si = _slot(pres, npres, i, s, in_t)
    new = si < 0
    if new:
        if npres[i, s] >= pres.shape[2]:
            return False
        si = npres[i, s]; pres[i, s, si] = in_t; cnt[i, s, si] = 0; npres[i, s] += 1
        _fill_slice(T, LA, TT, ev, active, recency, pres, npres, J, i, s, si, nk, Kb, rowb, Rb, Rx, Ry, Rall)
    cnt[i, s, si] += 1
    gcount[in_t] += 1
    _contrib(PAY, T, pres, cnt, npres, J, F, i, s, si, 1.0)
    if new:
        F[i, s, si] = _fit(PAY, T, pres, cnt, npres, J, i, s, si)
    return True


@njit(cache=True)
def _parent(F, pres, cnt, npres, isl, s, N2, w, wbuf):
    m = -1e300
    for q in range(npres[isl, s]):
        f = F[isl, s, q] / N2
        if f > m: m = f
    tot = 0.0
    for q in range(npres[isl, s]):
        wbuf[q] = cnt[isl, s, q] * np.exp(w * (F[isl, s, q] / N2 - m))
        tot += wbuf[q]
    u = np.random.random() * tot; acc = 0.0
    for q in range(npres[isl, s]):
        acc += wbuf[q]
        if u <= acc:
            return pres[isl, s, q]
    return pres[isl, s, npres[isl, s] - 1]


@njit(cache=True)
def _prot(f, slot, pb):
    """Protected fill: a contract-origin fill that only a later accepted contract may overwrite: a worker's demand
    fill (action 2 or 3), a boss's contract-origin fill when pb = 1."""
    if g_origin(f) != 3:
        return False
    if slot > 0:
        return g_action(f) >= 2
    return pb == 1


@njit(cache=True)
def _evict(out, m, slot, pb):
    """Drop the oldest unprotected fill of out[:m] (the oldest if all are protected); returns the new length."""
    v = 0
    for j in range(m):
        if not _prot(out[j], slot, pb):
            v = j
            break
    for j in range(v, m - 1):
        out[j] = out[j + 1]
    return m - 1


@njit(cache=True)
def _write(T, tdict, htags, wtag, active, recency, x, newf, counters, pb):
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    out = np.zeros(4, np.int64)
    mask = ~np.int64(15 | (3 << 7))
    nkk = (newf - 1) & mask
    hit = -1
    for j in range(Tn[x]):
        if ((Tf[x, j] - 1) & mask) == nkk:
            hit = j
            break
    if hit >= 0 and g_origin(newf) != 3 and _prot(Tf[x, hit], Ts[x], pb):
        counters[18] += 1
        return -1
    m = 0
    for j in range(Tn[x]):
        if j != hit:
            out[m] = Tf[x, j]; m += 1
    if hit < 0 and Tn[x] == 4:
        m = _evict(out, 4, Ts[x], pb)
        counters[4] += 1
    if hit >= 0:
        counters[3] += 1
    out[m] = newf; m += 1
    nt = get_type(T, tdict, htags, wtag, active, recency, Ts[x], Tb[x], Tl[x], out, m)
    if nt < 0:
        counters[8] += 1
        return -1
    if nt == x:
        counters[10] += 1
        return -1
    return nt


@njit(cache=True)
def _pick_tag(tg):
    if tg == 1:
        return 0
    if tg == 2:
        return 1
    return np.random.randint(2)


@njit(cache=True)
def _sel_idx(T, active, recency, t, slot, ctx_l0, ctx_l1, b0, b1, tag):
    """Index of the fill selected at node 0 (all actual) for tag `tag`, partner lineages and classes given."""
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    best = -1; bestp = -1
    for j in range(Tn[t] - 1, -1, -1):
        f = Tf[t, j]
        if g_tag(f) != tag:
            continue
        sc = g_scope(f)
        if not active[sc, g_origin(f)]:
            continue
        k = g_key(f)
        if sc == 0:
            ok = True
        elif sc == 1:
            ok = k == slot
        elif sc == 2:
            ok = k == ctx_l0 or k == ctx_l1
        else:
            ok = (k // 8 == 0 and k % 8 == b0) or (k // 8 == 1 and k % 8 == b1)
        if not ok:
            continue
        if recency == 1:
            return j
        pr = sc if sc < 2 else (2 if sc == 2 else 3)
        if pr > bestp:
            bestp = pr; best = j
    return best


@njit(cache=True)
def _island_stats(PAY, T, SUMT, pres, cnt, npres, J, i, N, out):
    """out[0:7] expected summary categories (union.summary), 7..9 wage paid distribution when someone works,
    10 boss payoff, 11 worker payoff, 12 P(both work), 13 whack rate."""
    for z in range(out.shape[0]):
        out[z] = 0.0
    N3 = float(N) * N * N
    for kb in range(npres[i, 0]):
        for k1 in range(npres[i, 1]):
            for k2 in range(npres[i, 2]):
                p = cnt[i, 0, kb] * cnt[i, 1, k1] * cnt[i, 2, k2] / N3
                c = J[i, kb, k1, k2] & 63
                x = pres[i, 1, k1]; y = pres[i, 2, k2]
                t1 = T[6][x]; t2 = T[6][y]
                out[SUMT[c, t1, t2]] += p
                b = c // 4; a1 = (c // 2) % 2; a2 = c % 2
                if a1 == 0 or a2 == 0:
                    out[7 + b // 3] += p
                if a1 == 0 and a2 == 0:
                    out[12] += p
                hh = b % 3
                if (hh == 0 and (a1 == 1 or a2 == 1)) or (hh == 2 and (t1 == 1 or t2 == 1)):
                    out[13] += p
                out[10] += p * PAY[c, t1, t2, 0]
                out[11] += p * 0.5 * (PAY[c, t1, t2, 1] + PAY[c, t1, t2, 2])


@njit(cache=True)
def _held_s(T, w, scope, key):
    """Highest demand held by worker type w at (scope, key) on a carried tag: 0 none, 1 = action 2 (s = 1/4),
    2 = action 3 (s = 1/2)."""
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    best = 0
    for j in range(Tn[w]):
        f = Tf[w, j]
        a = g_action(f)
        if a >= 2 and g_scope(f) == scope and g_key(f) == key and ((Tg[w] >> g_tag(f)) & 1):
            if a - 1 > best:
                best = a - 1
    return best


@njit(cache=True)
def _demand_fills(T, w, newf, out, slot, pb):
    """out <- w's fills with the demand fill newf written: any held demand fill at the same (scope, key) with a lower
    demand is removed (supersession), then the in-place / FIFO rule.  Returns the new length."""
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    n = 0
    for j in range(Tn[w]):
        f = Tf[w, j]
        if g_action(f) >= 2 and g_scope(f) == g_scope(newf) and g_key(f) == g_key(newf) and g_action(f) < g_action(newf):
            continue
        out[n] = f; n += 1
    return _append(out, n, newf, slot, pb)


@njit(cache=True)
def _boss_fills(T, b, tb, sp, scope, lx, ly, out, pb):
    """out <- the boss's fills with the wage response fill (sp, none) on tag tb written: keyed on the two workers'
    lineages (history scope: one fill per distinct lineage) or on role (scope 1, key 0)."""
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    n = Tn[b]
    for j in range(n):
        out[j] = Tf[b, j]
    act = 3 * sp + 1
    if scope == 1:
        n = _append(out, n, 1 + (act | (tb << 4) | (1 << 5) | (3 << 7) | (0 << 9)), 0, pb)
    else:
        n = _append(out, n, 1 + (act | (tb << 4) | (2 << 5) | (3 << 7) | (lx << 9)), 0, pb)
        if ly != lx:
            n = _append(out, n, 1 + (act | (tb << 4) | (2 << 5) | (3 << 7) | (ly << 9)), 0, pb)
    return n


@njit(cache=True)
def _union(T, tdict, htags, wtag, LA, TT, ev, active, active_c, recency, PAY, cfg, b, x, y, code, counters, ustat,
           Rxc, Ryc, Rbo, Rall, res, pb):
    """One union-contract attempt in the sampled encounter (b, x, y) at current joint code `code`.  res <- the new
    types (boss, W1, W2), -1 where unchanged."""
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    res[0] = -1; res[1] = -1; res[2] = -1
    if Tg[x] == 0 or Tg[y] == 0:
        return
    mode = cfg[10]
    role = cfg[11]
    ustat[0] += 1
    lb = Tl[b]; lx = Tl[x]; ly = Tl[y]
    if role == 1:
        scope = 1; kx = 1; ky = 2
    else:
        scope = 2; kx = lb; ky = lb
    hx = _held_s(T, x, scope, kx); hy = _held_s(T, y, scope, ky)
    t1 = Tut[x]; t2 = Tut[y]
    ux0 = PAY[code, t1, t2, 1]; uy0 = PAY[code, t1, t2, 2]
    pre_w = (code // 4) // 3
    nat = LA[0]
    const_b = nat[0, Tb[b]] == 0
    for j in range(Tn[b]):
        if g_scope(Tf[b, j]) == 3:
            const_b = False
    fx = np.zeros(4, np.int64); fy = np.zeros(4, np.int64); fb = np.zeros(4, np.int64)
    # worker candidate tables, per (s - 1, tag)
    okx = np.zeros((2, 2), np.bool_); oky = np.zeros((2, 2), np.bool_)
    hxh = np.zeros((2, 2), np.int64); hyh = np.zeros((2, 2), np.int64)
    for sv in range(1, 3):
        if hx >= sv and hy >= sv:
            continue
        donex = False; doney = False
        for tg in range(2):
            if (Tg[x] >> tg) & 1:
                if hx >= sv:
                    # x already holds a demand of at least sv at this key: it keeps its fills (one candidate)
                    if not donex:
                        resolve(Tf[x], Tn[x], Tg[x], 1, active_c, recency, lb, ly, Rxc[sv - 1, tg])
                        hxh[sv - 1, tg] = rhash(Rxc[sv - 1, tg]); okx[sv - 1, tg] = True
                        donex = True
                else:
                    nf = _demand_fills(T, x, 1 + ((sv + 1) | (tg << 4) | (scope << 5) | (3 << 7) | (kx << 9)), fx, 1, pb)
                    resolve(fx, nf, Tg[x], 1, active_c, recency, lb, ly, Rxc[sv - 1, tg])
                    hxh[sv - 1, tg] = rhash(Rxc[sv - 1, tg]); okx[sv - 1, tg] = True
            if (Tg[y] >> tg) & 1:
                if hy >= sv:
                    if not doney:
                        resolve(Tf[y], Tn[y], Tg[y], 2, active_c, recency, lb, lx, Ryc[sv - 1, tg])
                        hyh[sv - 1, tg] = rhash(Ryc[sv - 1, tg]); oky[sv - 1, tg] = True
                        doney = True
                else:
                    nf = _demand_fills(T, y, 1 + ((sv + 1) | (tg << 4) | (scope << 5) | (3 << 7) | (ky << 9)), fy, 2, pb)
                    resolve(fy, nf, Tg[y], 2, active_c, recency, lb, lx, Ryc[sv - 1, tg])
                    hyh[sv - 1, tg] = rhash(Ryc[sv - 1, tg]); oky[sv - 1, tg] = True
    # boss option tables: 0 program response; 1 + tb * 3 + sp the wage fill (sp, none) on tag tb (mode C, hooked boss)
    resolve(Tf[b], Tn[b], Tg[b], 0, active_c, recency, lx, ly, Rbo[0])
    hbh = np.zeros(7, np.int64)
    hbh[0] = rhash(Rbo[0])
    okb = np.zeros(7, np.bool_); okb[0] = True
    if mode == 2 and Tg[b] > 0:
        for tb in range(2):
            if not (Tg[b] >> tb) & 1:
                continue
            for sp in range(3):
                nf = _boss_fills(T, b, tb, sp, scope, lx, ly, fb, pb)
                resolve(fb, nf, Tg[b], 0, active_c, recency, lx, ly, Rbo[1 + tb * 3 + sp])
                hbh[1 + tb * 3 + sp] = rhash(Rbo[1 + tb * 3 + sp]); okb[1 + tb * 3 + sp] = True
    acc = np.zeros((16, 6), np.int64); nacc = 0
    for sv in range(1, 3):
        if hx >= sv and hy >= sv:
            continue
        for tx in range(2):
            if not okx[sv - 1, tx]:
                continue
            for ty in range(2):
                if not oky[sv - 1, ty]:
                    continue
                ustat[1] += 1
                best = -1; bestpay = -1e18; bestkey = -1
                cbest = 0
                for o in range(7):
                    if not okb[o]:
                        continue
                    if o > 0 and mode != 2:
                        continue
                    co = code_with(LA, TT, ev, Tb[b], hbh[o], Rbo[o], Tb[x], hxh[sv - 1, tx], Rxc[sv - 1, tx], Tut[x],
                                   Tb[y], hyh[sv - 1, ty], Ryc[sv - 1, ty], Tut[y], Rall) & 63
                    if mode == 1:
                        best = 0; cbest = co
                        break
                    pbo = PAY[co, t1, t2, 0]
                    wo = (co // 4) // 3
                    # preference key among equal boss payoffs: pays the demand (2), lower wage, program response
                    kk = (2 if wo >= sv else 0) * 100 - wo * 10 + (1 if o == 0 else 0)
                    if pbo > bestpay + 1e-9 or (abs(pbo - bestpay) <= 1e-9 and kk > bestkey):
                        bestpay = pbo; bestkey = kk; best = o; cbest = co
                ux = PAY[cbest, t1, t2, 1]; uy = PAY[cbest, t1, t2, 2]
                if ux >= ux0 - 1e-9 and uy >= uy0 - 1e-9 and (ux > ux0 + 1e-9 or uy > uy0 + 1e-9):
                    acc[nacc, 0] = sv; acc[nacc, 1] = tx; acc[nacc, 2] = ty; acc[nacc, 3] = best; acc[nacc, 4] = cbest
                    nacc += 1
                    ustat[29 + sv] += 1
    if nacc == 0:
        return
    k = np.random.randint(nacc)
    sv = acc[k, 0]; tx = acc[k, 1]; ty = acc[k, 2]; bo = acc[k, 3]; cb = acc[k, 4]
    nx = x; ny = y
    if hx < sv:
        nf = _demand_fills(T, x, 1 + ((sv + 1) | (tx << 4) | (scope << 5) | (3 << 7) | (kx << 9)), fx, 1, pb)
        nx = get_type(T, tdict, htags, wtag, active, recency, 1, Tb[x], Tl[x], fx, nf)
    if hy < sv:
        nf = _demand_fills(T, y, 1 + ((sv + 1) | (ty << 4) | (scope << 5) | (3 << 7) | (ky << 9)), fy, 2, pb)
        ny = get_type(T, tdict, htags, wtag, active, recency, 2, Tb[y], Tl[y], fy, nf)
    if nx < 0 or ny < 0:
        counters[8] += 1
        if nx >= 0 and gcount[nx] == 0 and nx != x:
            free_type(T, tdict, nx)
        if ny >= 0 and gcount[ny] == 0 and ny != y:
            free_type(T, tdict, ny)
        return
    nb = -1
    if bo > 0:
        tb = (bo - 1) // 3; sp = (bo - 1) % 3
        nf = _boss_fills(T, b, tb, sp, scope, lx, ly, fb, pb)
        nb = get_type(T, tdict, htags, wtag, active, recency, 0, Tb[b], Tl[b], fb, nf)
        if nb < 0:
            counters[8] += 1
            if gcount[nx] == 0 and nx != x:
                free_type(T, tdict, nx)
            if gcount[ny] == 0 and ny != y:
                free_type(T, tdict, ny)
            return
        ustat[4] += 1
    ustat[1 + sv] += 1
    if sv > pre_w:
        ustat[5] += 1
        if const_b:
            ustat[7] += 1
    else:
        ustat[6] += 1
    if const_b:
        ustat[8] += 1
    ustat[9 + (cb // 4) // 3] += 1
    ustat[12 + pre_w] += 1
    res[0] = nb
    res[1] = nx if nx != x else -1
    res[2] = ny if ny != y else -1



@njit(cache=True)
def kernel(LA, TT, htags, wtag, PAY, SUMT, T, tdict, ev, active, cfg, copy_q, pres, cnt, npres, J, F, N, w, m, gens,
           seed, checks, rec, rec_g, enc_stats, thr, counters, ustat):
    np.random.seed(seed)
    I = pres.shape[0]
    recency = cfg[0]
    active_c = active.copy()
    active_c[2, 3] = True
    active_c[1, 3] = True
    CAP = pres.shape[2]
    pb_ = cfg[12]
    Rxc = np.zeros((2, 2, RSZ), np.int8); Ryc = np.zeros((2, 2, RSZ), np.int8); Rbo = np.zeros((7, RSZ), np.int8)
    ures = np.zeros(3, np.int64)
    Kb = np.zeros(8, np.int64)
    rowb = -np.ones((CAP, CAP), np.int64)
    Rb = np.zeros(RSZ, np.int8); Rx = np.zeros(RSZ, np.int8); Ry = np.zeros(RSZ, np.int8)
    Rall = np.zeros((3, RSZ), np.int8)
    hz = np.int64(-7046029254386353131)            # key of an all-default (inert) resolution table
    wbuf = np.zeros(CAP + 1)
    N2 = float(N) * N
    Ts, Tb, Tl, Tf, Tn, Tg, Tut, Th, Tbb, Trn, Rsig, gcount, meta, freel = T
    if cfg[8] == 1:
        for i in range(I):
            for k in range(npres[i, 0]):
                _fill_slice(T, LA, TT, ev, active, recency, pres, npres, J, i, 0, k, -1, Kb, rowb, Rb, Rx, Ry, Rall)
            for s in range(3):
                for k in range(npres[i, s]):
                    F[i, s, k] = _fit(PAY, T, pres, cnt, npres, J, i, s, k)
    ci = 0
    tmp = np.zeros(NST)
    if ci < checks.shape[0] and checks[ci] == 0:
        for i in range(I):
            _island_stats(PAY, T, SUMT, pres, cnt, npres, J, i, N, rec[ci, i])
        ci += 1
    fa = np.zeros(4, np.int64)
    for g in range(gens):
        for e in range(3 * I * N):
            u = np.random.randint(3 * I)
            i = u // 3; s = u % 3
            src = i
            if m > 0.0 and I > 1 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            child = _parent(F, pres, cnt, npres, src, s, N2, w, wbuf)
            if cfg[6] == 1:
                mm = 0
                for j in range(Tn[child]):
                    if g_origin(Tf[child, j]) != 1:
                        fa[mm] = Tf[child, j]; mm += 1
                if mm < Tn[child]:
                    c2 = get_type(T, tdict, htags, wtag, active, recency, s, Tb[child], Tl[child], fa, mm)
                    if c2 >= 0:
                        child = c2
            r = np.random.randint(N)
            victim = pres[i, s, _slot_at(cnt, npres, i, s, r)]
            if victim != child:
                if not _replace(T, tdict, LA, TT, ev, active, recency, PAY, pres, cnt, npres, J, F, i, s, victim, child,
                                Kb, rowb, Rb, Rx, Ry, Rall):
                    counters[8] += 1
                    return ci
                if gcount[victim] == 0:
                    free_type(T, tdict, victim)
            if cfg[7] == 0:
                continue
            # ---- one sampled encounter on island i
            kb = _slot_at(cnt, npres, i, 0, np.random.randint(N))
            k1 = _slot_at(cnt, npres, i, 1, np.random.randint(N))
            k2 = _slot_at(cnt, npres, i, 2, np.random.randint(N))
            b = pres[i, 0, kb]; x = pres[i, 1, k1]; y = pres[i, 2, k2]
            full = triple_code(T, LA, TT, ev, active, recency, b, x, y, Rb, Rx, Ry, Rall)
            code = full & 63
            counters[0] += 1
            bA = code // 4; a1 = (code // 2) % 2; a2 = code % 2
            sw = bA // 3; hh = bA % 3
            t1 = Tut[x]; t2 = Tut[y]
            wh1 = (hh == 0 and a1 == 1) or (hh == 2 and t1 == 1)
            wh2 = (hh == 0 and a2 == 1) or (hh == 2 and t2 == 1)
            parties = (b, x, y)
            # path statistics: selected fill on path, executed (outcome differs with the party's fills inert)
            anych = False
            for sp in range(3):
                tp = parties[sp]
                inf = (full >> (6 + 3 * sp)) & 7
                for j in range(Tn[tp]):
                    gfill = Tf[tp, j]
                    enc_stats[0, g_scope(gfill), g_origin(gfill)] += 1
                    act = g_action(gfill)
                    thr_ = (act == 1) if sp > 0 else ((act % 3) == 0 or (act % 3) == 2)
                    if thr_:
                        thr[sp, 0] += 1
                        if active[g_scope(gfill), g_origin(gfill)]:
                            thr[sp, 1] += 1
                if (inf & 1) and (inf & 4):
                    tag = (inf >> 1) & 1
                    l0 = Tl[x] if sp == 0 else Tl[b]
                    l1 = Tl[y] if sp == 0 else (Tl[y] if sp == 1 else Tl[x])
                    be0 = (full >> (15 + 6 * sp)) & 7; be1 = (full >> (18 + 6 * sp)) & 7
                    jsel = _sel_idx(T, active, recency, tp, sp, l0, l1, be0, be1, tag)
                    c0 = inert_code(T, LA, TT, ev, active, recency, b, x, y, sp, Rall, hz)
                    exe = (c0 & 63) != code
                    if exe:
                        anych = True
                    if jsel >= 0:
                        gfill = Tf[tp, jsel]
                        enc_stats[1, g_scope(gfill), g_origin(gfill)] += 1
                        if exe:
                            enc_stats[2, g_scope(gfill), g_origin(gfill)] += 1
                        act = g_action(gfill)
                        if sp > 0 and act >= 2:
                            awk = a1 if sp == 1 else a2
                            ustat[13 + act] += 1
                            if awk == 1:
                                ustat[15 + act] += 1
                            if sw >= act - 1:
                                ustat[17 + act] += 1
                            ustat[21 + 3 * (act - 2) + sw] += 1
                        if (sp > 0 and act == 1) or (sp == 0 and ((act % 3) == 0 or (act % 3) == 2)):
                            thr[sp, 2] += 1
                            if sp > 0 or (sp == 0 and (wh1 or wh2)):
                                thr[sp, 3] += 1
            if anych:
                counters[9] += 1
            nb = -1; nx = -1; ny = -1
            uacc = False
            if cfg[10] > 0:
                _union(T, tdict, htags, wtag, LA, TT, ev, active, active_c, recency, PAY, cfg, b, x, y, code, counters,
                       ustat, Rxc, Ryc, Rbo, Rall, ures, pb_)
                if ures[0] >= 0 or ures[1] >= 0 or ures[2] >= 0:
                    nb = ures[0]; nx = ures[1]; ny = ures[2]
                    uacc = True
            # contracts (boss with one worker drawn uniformly)
            if cfg[3] == 1 and not uacc:
                jw = 1 + np.random.randint(2)
                wt = x if jw == 1 else y
                aj = a1 if jw == 1 else a2
                whj = wh1 if jw == 1 else wh2
                coop = aj == 0 and sw >= 1 and not whj
                if Tg[b] > 0 and Tg[wt] > 0 and not coop:
                    counters[6] += 1
                    ub0 = PAY[code, t1, t2, 0]; uw0 = PAY[code, t1, t2, jw]
                    nacc = 0
                    cand = np.zeros((8, 3), np.int64)
                    for tb in range(2):
                        if not (Tg[b] >> tb) & 1:
                            continue
                        for sv in range(1, 3):
                            for tw in range(2):
                                if not (Tg[wt] >> tw) & 1:
                                    continue
                                # hypothetical fills, candidate contract fills active (active_c)
                                fb_ = np.zeros(4, np.int64); fw_ = np.zeros(4, np.int64)
                                nbf = 0
                                for j in range(Tn[b]):
                                    fb_[nbf] = Tf[b, j]; nbf += 1
                                nwf = 0
                                for j in range(Tn[wt]):
                                    fw_[nwf] = Tf[wt, j]; nwf += 1
                                newb = 1 + ((3 * sv + 1) | (tb << 4) | (2 << 5) | (3 << 7) | (Tl[wt] << 9))
                                neww = 1 + (0 | (tw << 4) | (2 << 5) | (3 << 7) | (Tl[b] << 9))
                                nbf = _append(fb_, nbf, newb, 0, pb_)
                                nwf = _append(fw_, nwf, neww, 1 + (jw - 1), pb_)
                                resolve(fb_, nbf, Tg[b], 0, active_c, recency, Tl[x], Tl[y], Rb)
                                if jw == 1:
                                    resolve(fw_, nwf, Tg[x], 1, active_c, recency, Tl[b], Tl[y], Rx)
                                    resolve(Tf[y], Tn[y], Tg[y], 2, active_c, recency, Tl[b], Tl[x], Ry)
                                else:
                                    resolve(Tf[x], Tn[x], Tg[x], 1, active_c, recency, Tl[b], Tl[y], Rx)
                                    resolve(fw_, nwf, Tg[y], 2, active_c, recency, Tl[b], Tl[x], Ry)
                                c = code_with(LA, TT, ev, Tb[b], rhash(Rb), Rb, Tb[x], rhash(Rx), Rx, Tut[x], Tb[y],
                                              rhash(Ry), Ry, Tut[y], Rall) & 63
                                ub = PAY[c, t1, t2, 0]; uw = PAY[c, t1, t2, jw]
                                if ub >= ub0 and uw >= uw0 and (ub > ub0 or uw > uw0):
                                    cand[nacc, 0] = tb; cand[nacc, 1] = sv; cand[nacc, 2] = tw; nacc += 1
                    if nacc > 0:
                        kk = np.random.randint(nacc)
                        tb = cand[kk, 0]; sv = cand[kk, 1]; tw = cand[kk, 2]
                        newb = 1 + ((3 * sv + 1) | (tb << 4) | (2 << 5) | (3 << 7) | (Tl[wt] << 9))
                        neww = 1 + (0 | (tw << 4) | (2 << 5) | (3 << 7) | (Tl[b] << 9))
                        q1 = _write(T, tdict, htags, wtag, active, recency, b, newb, counters, pb_)
                        q2 = _write(T, tdict, htags, wtag, active, recency, wt, neww, counters, pb_)
                        if q1 >= 0 and q2 >= 0:
                            counters[7] += 1
                            nb = q1
                            if jw == 1:
                                nx = q2
                            else:
                                ny = q2
                        else:
                            if q1 >= 0 and gcount[q1] == 0:
                                free_type(T, tdict, q1)
                            if q2 >= 0 and gcount[q2] == 0:
                                free_type(T, tdict, q2)
            # history-triggered writes (amendment 4)
            for sp in range(3):
                if (sp == 0 and nb >= 0) or (sp == 1 and nx >= 0) or (sp == 2 and ny >= 0):
                    continue
                tp = parties[sp]
                if Tg[tp] == 0:
                    continue
                newf = -1; which = 0
                if sp == 0:
                    ns = (1 if a1 == 1 else 0) + (1 if a2 == 1 else 0)
                    nw = (1 if (a1 == 0 and sw >= 1) else 0) + (1 if (a2 == 0 and sw >= 1) else 0)
                    if ns > 0 and cfg[1] == 1:
                        tgt = 1 if (a1 == 1 and (a2 == 0 or np.random.randint(2) == 0)) else 2
                        key = Tl[x] if tgt == 1 else Tl[y]
                        newf = 1 + (0 | (_pick_tag(Tg[tp]) << 4) | (2 << 5) | (1 << 7)); which = 1
                    elif ns == 0 and nw > 0 and cfg[2] == 1:
                        ok1 = a1 == 0 and sw >= 1; ok2 = a2 == 0 and sw >= 1
                        tgt = 1 if (ok1 and (not ok2 or np.random.randint(2) == 0)) else 2
                        key = Tl[x] if tgt == 1 else Tl[y]
                        newf = 1 + (bA | (_pick_tag(Tg[tp]) << 4) | (2 << 5) | (1 << 7)); which = 2
                else:
                    aw = a1 if sp == 1 else a2
                    whk = wh1 if sp == 1 else wh2
                    key = Tl[b]
                    if aw == 0 and (sw == 0 or whk) and cfg[1] == 1:
                        newf = 1 + (1 | (_pick_tag(Tg[tp]) << 4) | (2 << 5) | (1 << 7)); which = 1
                    elif aw == 0 and sw >= 1 and not whk and cfg[2] == 1:
                        newf = 1 + (0 | (_pick_tag(Tg[tp]) << 4) | (2 << 5) | (1 << 7)); which = 2
                if newf < 0:
                    continue
                if cfg[5] == 1:
                    so_ = np.random.randint(3)
                    key = Tl[pres[i, so_, _slot_at(cnt, npres, i, so_, np.random.randint(N))]]
                newf = newf + (key << 9)
                counters[which] += 1
                q = _write(T, tdict, htags, wtag, active, recency, tp, newf, counters, pb_)
                if sp == 0:
                    nb = q
                elif sp == 1:
                    nx = q
                else:
                    ny = q
            # copying between the two workers
            if cfg[4] == 1:
                for sp in range(1, 3):
                    if (sp == 1 and nx >= 0) or (sp == 2 and ny >= 0):
                        continue
                    if np.random.random() >= copy_q:
                        continue
                    me = x if sp == 1 else y
                    ot = y if sp == 1 else x
                    if Tg[me] == 0:
                        continue
                    nc = 0
                    for j in range(Tn[ot]):
                        if (Tg[me] >> g_tag(Tf[ot, j])) & 1:
                            nc += 1
                    if nc == 0:
                        continue
                    rr = np.random.randint(nc); gsel = 0
                    for j in range(Tn[ot]):
                        if (Tg[me] >> g_tag(Tf[ot, j])) & 1:
                            if rr == 0:
                                gsel = Tf[ot, j]
                                break
                            rr -= 1
                    newf = gsel if cfg[9] == 1 else (((gsel - 1) & ~np.int64(3 << 7)) | (2 << 7)) + 1
                    q = _write(T, tdict, htags, wtag, active, recency, me, newf, counters, pb_)
                    if q >= 0:
                        counters[5] += 1
                    if sp == 1:
                        nx = q
                    else:
                        ny = q
            # apply
            for sp in range(3):
                nt = nb if sp == 0 else (nx if sp == 1 else ny)
                if nt < 0:
                    continue
                old = parties[sp]
                if not _replace(T, tdict, LA, TT, ev, active, recency, PAY, pres, cnt, npres, J, F, i, sp, old, nt,
                                Kb, rowb, Rb, Rx, Ry, Rall):
                    counters[8] += 1
                    return ci
            for sp in range(3):
                nt = nb if sp == 0 else (nx if sp == 1 else ny)
                if nt >= 0 and gcount[parties[sp]] == 0:
                    free_type(T, tdict, parties[sp])
        if ci < checks.shape[0] and g + 1 == checks[ci]:
            for i in range(I):
                _island_stats(PAY, T, SUMT, pres, cnt, npres, J, i, N, rec[ci, i])
            rec_g[ci, 0] = meta[0] - meta[1]
            ci += 1
        if len(ev) > 3000000:
            ev.clear()
    return ci


@njit(cache=True)
def _append(f, n, newf, slot, pb):
    """Write newf into f[:n] with the in-place / FIFO rule (FIFO evicts the oldest unprotected fill); returns the new
    length."""
    mask = ~np.int64(15 | (3 << 7))
    nk = (newf - 1) & mask
    hit = -1
    for j in range(n):
        if ((f[j] - 1) & mask) == nk:
            hit = j
            break
    if hit >= 0:
        for j in range(hit, n - 1):
            f[j] = f[j + 1]
        n -= 1
    elif n == 4:
        n = _evict(f, 4, slot, pb)
    f[n] = newf
    return n + 1
