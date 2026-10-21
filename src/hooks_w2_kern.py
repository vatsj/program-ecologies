"""Hooks, Part W2: copy of hooks_w_kern.py with open keys (notes/hooks-w2.md).  Additions: cfg[11] open history writes
(grudge/thanks keyed on the partner's predicate p = bit 2 of the class it read), cfg[12] open contracts (the pair of open
promises, action C, key p = 1), cfg[13] strict history-variant test (a variant must have identical non-history fills);
counters 11 candidates evaluated, 13 party-encounters of holders of an open contract-origin fill, 14 their (C against D)
events, 15 / 16 the same for lineage contract-origin fills, 17 open writes.  rec_glob 70-73: share of individuals holding
at least one open fill (carried tag), one open contract-origin fill, one lineage contract-origin fill, one open written
fill.

Part W doc:
Hooks, Part W: the eps = 0 island kernel over types (base, fills, lineage) for the hooked modal PD.

The law is almost_all_seeds._run's (parent proportional to count * exp(w f), f the exact mean payoff against the
island's other residents under current fills; migration with probability m from a uniform other island; uniform
victim) with classes replaced by types, plus one sampled encounter on the birth island after every birth event
(cfg[7] = 1), in which contracts, history-triggered writes and copies change fills (notes/hooks-w.md §1.7, §1.9).
Each island keeps the match codes among its present types in a dense slot matrix Cl, so fitness bookkeeping costs
array operations; a new type entering an island costs one match per present slot (cached by spec key in ev).
With cfg[7] = 0 and one type per class the random stream and the arithmetic are the stored kernel's.

cfg: 0 recency-only conflict rule, 1 grudge writes, 2 thanks writes, 3 contracts, 4 copying, 5 shuffled trigger keys,
6 written fills not inherited, 7 encounters on, 8 compute initial matrices and paysums, 9 rejection parent sampler
(used for the merged fission-fusion population; the same law as the stored sampler), 10 copies keep the copied
fill's origin (provenance-preserving copying, the strict source ablations; 0 = a copy has origin 'copied').
counters: 0 encounters, 1 grudge writes, 2 thanks writes, 3 in-place updates, 4 evictions, 5 copies, 6 contract
attempts, 7 contracts, 8 type-capacity or slot-capacity overflow, 9 encounters whose outcome a selected fill changed,
10 writes that changed nothing.
enc_stats[level, scope, origin]: levels 0 held, 1 applicable, 2 selected, 3 executed.
rec_isl[c, i]: 0 P(C,C), 1 mean payoff, 2 lineages, 3 lineage concentration (sum of squared lineage shares),
4 majority type, 5 majority count, 6 present types.
rec_glob[c]: 0..63 held fills by (carried, scope, origin, action) = carried*32 + scope*8 + origin*2 + action,
64 gentle share, 65 gentle-holder share, 66 present types, 67 fills per program, 68 history-fill holders,
69 live type ids.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from numba import njit
from hooks_w2 import (spec_of, eval_code, match, swap_code, write_fill, select_idx, get_type, free_type, spec_ctx,
                      f_action, f_tag, f_scope, f_origin, f_key, beh_ok)

NREC_I, NREC_G = 7, 80


@njit(cache=True)
def _pay(PAY, c):
    return PAY[c & 1, (c >> 1) & 1]


@njit(cache=True)
def _payT(PAY, c):
    """Payoff of the column player of code c (Cl is antisymmetric: Cl[y, x] = swap(Cl[x, y]), so a column entry is
    read from a row)."""
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
def _fill_slot(T, LA, ev, iC, iD, active, recency, pres, npres, Cl, i, si):
    t = pres[i, si]
    for x in range(npres[i]):
        c = match(T, LA, ev, iC, iD, active, recency, t, pres[i, x])
        Cl[i, si, x] = c
        Cl[i, x, si] = swap_code(c)


@njit(cache=True)
def _variant_keys(T, active, a, b, K, strict):
    """If types a and b differ only in active history fills keyed on lineages other than their own (same base,
    lineage, spec without lineage and spec against their own lineage), write those lineages into K and return their
    number; else -1.  Then a and b play identically against every type whose lineage is not in K."""
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    if Tb[a] != Tb[b] or Tl[a] != Tl[b] or Ts0[a] != Ts0[b] or Tss[a] != Tss[b]:
        return -1
    if strict == 1:
        na_ = 0; nb_ = 0
        for j in range(Tn[a]):
            if f_scope(Tf[a, j]) != 2:
                na_ += 1
        for j in range(Tn[b]):
            if f_scope(Tf[b, j]) != 2:
                nb_ += 1
        if na_ != nb_:
            return -1
        ja = 0; jb = 0
        for q in range(na_):
            while f_scope(Tf[a, ja]) == 2:
                ja += 1
            while f_scope(Tf[b, jb]) == 2:
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
            if f_scope(g) != 2 or not active[2, f_origin(g)] or not (tg >> f_tag(g)) & 1:
                continue
            found = False
            for j2 in range(Tn[y]):
                g2 = Tf[y, j2]
                if (f_scope(g2) == 2 and active[2, f_origin(g2)] and f_tag(g2) == f_tag(g) and f_key(g2) == f_key(g)
                        and f_action(g2) == f_action(g)):
                    found = True
                    break
            if not found:
                k = f_key(g)
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
def _replace(T, tdict, LA, ev, iC, iD, active, recency, PAY, pres, cnt, ps, npres, Cl, vpay, rowb, i, out_t, in_t, strict):
    """One individual of type out_t on island i becomes in_t (mirrors almost_all_seeds._run's arithmetic).  A new
    type that is a history variant of out_t copies out_t's match row except against the lineages whose fills changed."""
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
            _fill_slot(T, LA, ev, iC, iD, active, recency, pres, npres, Cl, i, si)
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
                        c = match(T, LA, ev, iC, iD, active, recency, in_t, t)
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
    """The stored sampler (same arithmetic; each slot's weight computed once and reused in the cumulative pass)."""
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
    """Exact rejection sampler for large populations: propose a resident uniformly, accept with probability
    exp(w (f - fmax)), fmax an upper bound on f (the largest payoff entry).  Same law as _parent."""
    while True:
        r = np.random.randint(N)
        s = _slot_at(cnt, npres, isl, r)
        f = (ps[isl, s] - _pay(PAY, Cl[isl, s, s])) / (N - 1)
        if np.random.random() < np.exp(w * (f - fmax)):
            return pres[isl, s]


@njit(cache=True)
def _strip(T, tdict, b_tags, active, recency, t):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    g = np.zeros(4, np.int64); m = 0
    for j in range(Tn[t]):
        if f_origin(Tf[t, j]) != 1:
            g[m] = Tf[t, j]; m += 1
    if m == Tn[t]:
        return t
    r = get_type(T, tdict, b_tags, active, recency, Tb[t], Tl[t], g, m)
    return t if r < 0 else r


@njit(cache=True)
def _gentle(T, LA, ev, iC, iD, bD, t):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    if Tgent[t] < 0:
        s = Ts0[t]
        c = eval_code(LA, ev, iC, iD, Tb[t], s, s, s, bD, 0, 0, 0)
        Tgent[t] = c & 1
    return Tgent[t]


@njit(cache=True)
def _party_stats(T, active, recency, x, ctx, beta, executed, enc_stats):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    tg = Tg[x]
    sel0 = select_idx(Tf[x], Tn[x], tg, active, recency, ctx, beta, 0, True)
    sel1 = select_idx(Tf[x], Tn[x], tg, active, recency, ctx, beta, 1, True)
    for j in range(Tn[x]):
        g = Tf[x, j]; sc = f_scope(g); og = f_origin(g)
        enc_stats[0, sc, og] += 1
        if (tg >> f_tag(g)) & 1:
            ok = (sc <= 1) or (sc == 2 and ctx >= 0 and f_key(g) == ctx) or (sc == 3 and beh_ok(f_key(g), beta))
            if ok:
                enc_stats[1, sc, og] += 1
        if j == sel0 or j == sel1:
            enc_stats[2, sc, og] += 1
            if executed:
                enc_stats[3, sc, og] += 1
    return sel0 >= 0 or sel1 >= 0


@njit(cache=True)
def _trigger(T, tdict, b_tags, active, recency, cfg, pres, cnt, npres, N, i, x, y, xs, ys, counters, pred):
    """History-triggered write for party x (action xs) against partner y (action ys); the new type or -1.  With
    cfg[11] = 1 (open writes) the fill is keyed on the predicate pred (x's read of y: does y provably cooperate with
    x) in the behaviour scope, key 8 + pred; otherwise on y's lineage in the history scope (Part W)."""
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    tg = Tg[x]
    if tg == 0 or xs != 1:
        return -1
    if ys == 0 and cfg[1] == 1:
        act = 0; which = 1
    elif ys == 1 and cfg[2] == 1:
        act = 1; which = 2
    else:
        return -1
    t = 0 if tg == 1 else (1 if tg == 2 else np.random.randint(2))
    key = Tl[y]
    if cfg[5] == 1:
        key = Tl[pres[i, _slot_at(cnt, npres, i, np.random.randint(N))]]
    out = np.zeros(4, np.int64)
    if cfg[11] == 1:
        nf, evc, inpl = write_fill(Tf[x], Tn[x], 1 + (act | (t << 1) | (3 << 2) | (1 << 4) | ((8 + pred) << 6)), out)
        counters[17] += 1
    else:
        nf, evc, inpl = write_fill(Tf[x], Tn[x], 1 + (act | (t << 1) | (2 << 2) | (1 << 4) | (key << 6)), out)
    counters[which] += 1; counters[4] += evc; counters[3] += inpl
    nt = get_type(T, tdict, b_tags, active, recency, Tb[x], Tl[x], out, nf)
    if nt < 0:
        counters[8] += 1
        return -1
    if nt == x:
        counters[10] += 1
        return -1
    return nt


@njit(cache=True)
def _copy(T, tdict, b_tags, active, recency, x, y, counters, keep_origin):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    tg = Tg[x]
    if tg == 0:
        return -1
    nc = 0
    for j in range(Tn[y]):
        if (tg >> f_tag(Tf[y, j])) & 1:
            nc += 1
    if nc == 0:
        return -1
    r = np.random.randint(nc); g = 0
    for j in range(Tn[y]):
        if (tg >> f_tag(Tf[y, j])) & 1:
            if r == 0:
                g = Tf[y, j]
                break
            r -= 1
    newf = g if keep_origin == 1 else (((g - 1) & ~np.int64(3 << 4)) | (2 << 4)) + 1
    out = np.zeros(4, np.int64)
    nf, evc, inpl = write_fill(Tf[x], Tn[x], newf, out)
    counters[4] += evc; counters[3] += inpl
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
    return (spec_of(f, n, g, active_c, recency, -1), spec_of(f, n, g, active_c, recency, lo),
            spec_of(f, n, g, active_c, recency, lself))


@njit(cache=True)
def _ccode(open_c, act, tag, key):
    """Contract fill code: lineage technology (history scope, key = the partner's lineage, either action) or open
    technology (behaviour scope, key 9 = partner provably cooperates with me, action C)."""
    if open_c == 1:
        return 1 + (1 | (tag << 1) | (3 << 2) | (3 << 4) | (9 << 6))
    return 1 + (act | (tag << 1) | (2 << 2) | (3 << 4) | (key << 6))


@njit(cache=True)
def _contract(T, tdict, LA, ev, b_tags, iC, iD, active, active_c, recency, PAY, a, b, counters, res, open_c):
    """Pair contract between a and b: candidates (ta, aa, tb, ab); accepted iff, judged under active_c (candidate
    contract fills active), both parties weakly gain and one strictly; one accepted candidate drawn uniformly.
    open_c = 1: the pair of open promises (action C, key p = 1) on the parties' tags; evaluated jointly by the
    evaluator with both fills in force."""
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    counters[6] += 1
    la = Tl[a]; lb = Tl[b]; ga = Tg[a]; gb = Tg[b]
    a0, a1, a2 = _cspecs(Tf[a], Tn[a], ga, active_c, recency, lb, la)
    b0, b1, b2 = _cspecs(Tf[b], Tn[b], gb, active_c, recency, la, lb)
    c0 = eval_code(LA, ev, iC, iD, Tb[a], a0, a1, a2, Tb[b], b0, b1, b2)
    pa0 = PAY[c0 & 1, (c0 >> 1) & 1]; pb0 = PAY[(c0 >> 1) & 1, c0 & 1]
    acc = np.zeros((16, 4), np.int64); nacc = 0
    fa = np.zeros(4, np.int64); fb = np.zeros(4, np.int64)
    lo_a = 1 if open_c == 1 else 0
    for ta in range(2):
        if not (ga >> ta) & 1:
            continue
        for aa in range(lo_a, 2):
            na, e1, i1 = write_fill(Tf[a], Tn[a], _ccode(open_c, aa, ta, lb), fa)
            sa0, sa1, sa2 = _cspecs(fa, na, ga, active_c, recency, lb, la)
            for tb in range(2):
                if not (gb >> tb) & 1:
                    continue
                for ab in range(lo_a, 2):
                    nb, e2, i2 = write_fill(Tf[b], Tn[b], _ccode(open_c, ab, tb, la), fb)
                    sb0, sb1, sb2 = _cspecs(fb, nb, gb, active_c, recency, la, lb)
                    counters[11] += 1
                    c = eval_code(LA, ev, iC, iD, Tb[a], sa0, sa1, sa2, Tb[b], sb0, sb1, sb2)
                    pa = PAY[c & 1, (c >> 1) & 1]; pb = PAY[(c >> 1) & 1, c & 1]
                    if pa >= pa0 and pb >= pb0 and (pa > pa0 or pb > pb0):
                        acc[nacc, 0] = ta; acc[nacc, 1] = aa; acc[nacc, 2] = tb; acc[nacc, 3] = ab; nacc += 1
    res[0] = -1; res[1] = -1
    if nacc == 0:
        return
    k = np.random.randint(nacc)
    ta = acc[k, 0]; aa = acc[k, 1]; tb = acc[k, 2]; ab = acc[k, 3]
    na, e1, i1 = write_fill(Tf[a], Tn[a], _ccode(open_c, aa, ta, lb), fa)
    nb, e2, i2 = write_fill(Tf[b], Tn[b], _ccode(open_c, ab, tb, la), fb)
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


@njit(cache=True)
def _record(T, LA, ev, iC, iD, bD, PAY, pres, cnt, ps, npres, Cl, N, rec_i, rec_g):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
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
            gt = _gentle(T, LA, ev, iC, iD, bD, a)
            hashist = False
            fo = False; foc = False; flc = False; fow = False
            for j in range(Tn[a]):
                g = Tf[a, j]
                carried = (Tg[a] >> f_tag(g)) & 1
                if carried == 1 and f_scope(g) == 3 and f_key(g) >= 8:
                    fo = True
                    if f_origin(g) == 3: foc = True
                    if f_origin(g) == 1: fow = True
                if carried == 1 and f_scope(g) == 2 and f_origin(g) == 3:
                    flc = True
                rec_g[carried * 32 + f_scope(g) * 8 + f_origin(g) * 2 + f_action(g)] += c
                if f_scope(g) == 2:
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
    rec_g[64] = gent / tot; rec_g[65] = gh / tot; rec_g[66] = ntp; rec_g[67] = nfil / tot; rec_g[68] = hh / tot
    rec_g[69] = meta[0] - meta[1]
    rec_g[70] = ho / tot; rec_g[71] = hoc / tot; rec_g[72] = hlc / tot; rec_g[73] = how / tot


@njit(cache=True)
def kernel(LA, b_tags, iC, iD, bD, T, tdict, ev, active, cfg, copy_q, PAY, pres, cnt, ps, npres, Cl, N, w, m, gens,
           seed, checks, rec_isl, rec_glob, enc_stats, counters):
    """Runs gens generations; records at the generations listed in checks (0 = before the first generation).
    Returns the number of records written (fewer if a capacity overflowed: counters[8] > 0 then)."""
    np.random.seed(seed)
    I = pres.shape[0]
    recency = cfg[0]
    active_c = active.copy()
    active_c[2, 3] = True
    active_c[3, 3] = True
    strict = cfg[13]
    open_c = cfg[12]
    vpay = np.zeros(pres.shape[1] + 1)
    rowb = np.zeros(pres.shape[1] + 1, np.int64)
    wbuf = np.zeros(pres.shape[1] + 1)
    fmax = PAY.max()
    if cfg[8] == 1:
        for i in range(I):
            for s in range(npres[i]):
                _fill_slot(T, LA, ev, iC, iD, active, recency, pres, npres, Cl, i, s)
            for s in range(npres[i]):
                v = 0.0
                for s2 in range(npres[i]):
                    v += cnt[i, s2] * _pay(PAY, Cl[i, s, s2])
                ps[i, s] = v
    ci = 0
    if ci < checks.shape[0] and checks[ci] == 0:
        _record(T, LA, ev, iC, iD, bD, PAY, pres, cnt, ps, npres, Cl, N, rec_isl[ci], rec_glob[ci])
        ci += 1
    res = np.zeros(2, np.int64)
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
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
            if cfg[6] == 1:
                child = _strip(T, tdict, b_tags, active, recency, child)
            u = np.random.randint(N); acc = 0; victim = pres[i, 0]
            for s in range(npres[i]):
                acc += cnt[i, s]
                if u < acc:
                    victim = pres[i, s]
                    break
            if victim != child:
                if not _replace(T, tdict, LA, ev, iC, iD, active, recency, PAY, pres, cnt, ps, npres, Cl, vpay, rowb, i, victim, child, strict):
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
            xa = code & 1; xb = (code >> 1) & 1; ba = (code >> 2) & 7; bb = (code >> 5) & 7
            counters[0] += 1
            for sd in range(2):
                tq = a if sd == 0 else b
                me = xa if sd == 0 else xb
                ot = xb if sd == 0 else xa
                ho_ = False; hl_ = False
                for j in range(Tn[tq]):
                    gf = Tf[tq, j]
                    if f_origin(gf) == 3 and ((Tg[tq] >> f_tag(gf)) & 1):
                        if f_scope(gf) == 3 and f_key(gf) >= 8:
                            ho_ = True
                        if f_scope(gf) == 2:
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
                c2 = eval_code(LA, ev, iC, iD, Tb[a], 0, 0, 0, Tb[b], Ts0[b], spec_ctx(T, active, recency, b, Tl[a]), Tss[b])
                exa = (c2 & 3) != (code & 3)
            if Tn[b] > 0:
                c2 = eval_code(LA, ev, iC, iD, Tb[a], Ts0[a], spec_ctx(T, active, recency, a, Tl[b]), Tss[a], Tb[b], 0, 0, 0)
                exb = (c2 & 3) != (code & 3)
            s1 = _party_stats(T, active, recency, a, Tl[b], ba, exa, enc_stats)
            s2 = _party_stats(T, active, recency, b, Tl[a], bb, exb, enc_stats)
            if (exa and s1) or (exb and s2):
                counters[9] += 1
            na = -1; nb = -1
            if cfg[3] == 1 and Tg[a] > 0 and Tg[b] > 0 and not (xa == 1 and xb == 1):
                _contract(T, tdict, LA, ev, b_tags, iC, iD, active, active_c, recency, PAY, a, b, counters, res, open_c)
                na = res[0]; nb = res[1]
            if na < 0:
                na = _trigger(T, tdict, b_tags, active, recency, cfg, pres, cnt, npres, N, i, a, b, xa, xb, counters, (ba >> 2) & 1)
            if nb < 0:
                nb = _trigger(T, tdict, b_tags, active, recency, cfg, pres, cnt, npres, N, i, b, a, xb, xa, counters, (bb >> 2) & 1)
            if na < 0 and cfg[4] == 1 and np.random.random() < copy_q:
                na = _copy(T, tdict, b_tags, active, recency, a, b, counters, cfg[10])
            if nb < 0 and cfg[4] == 1 and np.random.random() < copy_q:
                nb = _copy(T, tdict, b_tags, active, recency, b, a, counters, cfg[10])
            if na >= 0:
                if not _replace(T, tdict, LA, ev, iC, iD, active, recency, PAY, pres, cnt, ps, npres, Cl, vpay, rowb, i, a, na, strict):
                    counters[8] += 1
                    return ci
            if nb >= 0:
                if not _replace(T, tdict, LA, ev, iC, iD, active, recency, PAY, pres, cnt, ps, npres, Cl, vpay, rowb, i, b, nb, strict):
                    counters[8] += 1
                    return ci
            if na >= 0:
                _maybe_free(T, tdict, a)
            if nb >= 0:
                _maybe_free(T, tdict, b)
        if ci < checks.shape[0] and g + 1 == checks[ci]:
            _record(T, LA, ev, iC, iD, bD, PAY, pres, cnt, ps, npres, Cl, N, rec_isl[ci], rec_glob[ci])
            ci += 1
        if len(ev) > 4000000:
            ev.clear()
    return ci
