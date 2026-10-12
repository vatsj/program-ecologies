"""The ε = 0 island lottery with per-individual certificate inventories (notes/certificates-as-genes.md §1.8).

State per individual: a type (unit, mode, spelling for split run trees else -1, ancestry bits); per island the N
slots hold type indices.  Per Moran event: r encounters (a uniform island, a uniform focal, a uniform other partner;
both run their mode's procedure against the other's pre-encounter quote), then milestone 2's birth-death step (parent
from the source island by exp(w * mean payoff against the source's other residents), uniform victim, the child
inherits the parent's type).  Transitions are computed from the static unit tables (lt_genes_pop.finalize).
"""
import numpy as np
from numba import njit, types
from numba.typed import Dict

MODE_H, MODE_S, MODE_C, MODE_CS = 0, 1, 2, 3
LMAX = 6
# UVt columns
UV_C_SELF, UV_D_SELF, UV_C_C, UV_D_C, UV_C_D, UV_D_D = 0, 1, 2, 3, 4, 5
PAYM = np.array([[-1.0, 1.0], [-2.0, 0.0]])      # [my action][their action], D = 0, C = 1
# counters
NCTR = 24
(C_ENC, C_GATE, C_GATE_T, C_PRODC, C_PRODC_OK, C_PRODD, C_PRODD_OK, C_AC, C_AC_OK, C_AC_SCREEN0,
 C_TRANSFER_FAIL, C_BIRTH, C_CHANGE, C_STEPS, C_TRANSFER_UNK, C_PROD_TO) = range(16)


@njit(cache=True)
def type_code(unit, mode, sp, anc):
    return ((unit * 4 + mode) * 16384 + (sp + 1)) * 4096 + anc


@njit(cache=True)
def has_c(BLC, u):
    return BLC[u, 0] >= 0


@njit(cache=True)
def has_d(BLD, u):
    return BLD[u, 0] >= 0


@njit(cache=True)
def uvv(UVt, BLC, BLD, u, col):
    a_is_c = (col % 2) == 0
    if a_is_c:
        if BLC[u, 0] < 0: return 0
    else:
        if BLD[u, 0] < 0: return 0
    return 1 if UVt[u, col] == 1 else 0


@njit(cache=True)
def blen(BL, u):
    n = 0
    for k in range(BL.shape[1]):
        if BL[u, k] < 0: break
        n += 1
    return n


@njit(cache=True)
def holds(BL, u, s):
    for k in range(BL.shape[1]):
        if BL[u, k] < 0: return False
        if BL[u, k] == s: return True
    return False


@njit(cache=True)
def uvr(UVt, BLC, BLD, u, col):
    """Raw unit value (0 F, 1 T, 2 TO), 0 without an entry of the column's outcome."""
    if (col % 2) == 0:
        if BLC[u, 0] < 0: return 0
    else:
        if BLD[u, 0] < 0: return 0
    v = UVt[u, col]
    return v if v >= 0 else 0


@njit(cache=True)
def v3(x):
    if x == 1: return 1
    if x == 2: return 4
    return 0


@njit(cache=True)
def sig_code(u, v, rel, utau, KIND, NAT, CHD, UVt, BLC, BLD):
    """lt_genes_pop.Tables.sig_codes_C for one opponent (rel 0 distinct, 1 twin, 2 same quote)."""
    t = utau[u]
    code = 25 if rel == 2 else 0
    for i in range(NAT[t]):
        k = KIND[t, i, 0]; ai = KIND[t, i, 1]; qi = KIND[t, i, 2]
        c = 0
        if rel == 2 and k <= 3:
            if ai == 0: c = 2
            else: c = v3(uvr(UVt, BLC, BLD, u, UV_D_SELF))
        elif rel == 2 and k == 4:
            c = v3(uvr(UVt, BLC, BLD, u, (2 if qi == 0 else 4) + ai))
        elif k == 0:
            if ai == 0: c = 3
            else: c = v3(CHD[v, u]) if BLD[v, 0] >= 0 else 0
        elif k == 1:
            if ai == 0: c = 2
            else: c = v3(CHD[u, v]) if BLD[u, 0] >= 0 else 0
        elif k == 2:
            c = v3(uvr(UVt, BLC, BLD, v, ai))
        elif k == 3:
            c = v3(uvr(UVt, BLC, BLD, u, ai))
        elif k == 4:
            c = v3(uvr(UVt, BLC, BLD, v, (2 if qi == 0 else 4) + ai))
        else:
            c = v3(uvr(UVt, BLC, BLD, u, (2 if qi == 0 else 4) + ai))
        code += c * (5 if i == 0 else 1)
    return code


@njit(cache=True)
def trans_C(u, v, rel, anc, ancv, utau, BLC, BLD, SINGLE, APP, CHC, UVt, ctr, cost, COSTS):
    """Copy-and-check (notes §1.3): every donor entry not held, in the donor's order, one adoption per outcome.
    Returns (u', anc')."""
    if rel == 2:
        return u, anc
    t = utau[u]
    for blk in range(2):
        BL = BLC if blk == 0 else BLD
        off = 0 if blk == 0 else LMAX
        if BL[u, 0] >= 0:
            continue                               # rule 'lack': this outcome already has an entry
        for k in range(LMAX):
            s = BL[v, k]
            if s < 0: break
            if holds(BL, u, s): continue
            ctr[C_AC] += 1
            cost[0] += COSTS[0]                    # adoption check (median term cost) + surgery
            xs = SINGLE[t, s]
            if xs < 0:
                ctr[C_AC_SCREEN0] += 1
                continue
            if blk == 0:
                acv = CHC[xs, v]
            else:
                acv = UVt[xs, UV_D_D]
            if acv == 1:
                pos = blen(BL, u)
                u2 = APP[u, s]
                bit = (ancv >> (off + k)) & 1
                anc = anc | (bit << (off + pos))
                if blk == 0:
                    # Lemma A in the population: is the adopted object certified against the donor?
                    tv = CHC[v, v] if u2 == v else CHC[u2, v]
                    if tv < 0:
                        ctr[C_TRANSFER_UNK] += 1
                    elif tv != 1:
                        ctr[C_TRANSFER_FAIL] += 1
                u = u2
                ctr[C_AC_OK] += 1
                break
    return u, anc


@njit(cache=True)
def trans_S(u, v, rel, anc, utau, BLC, BLD, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, ctr, cost, COSTS):
    """Search (notes §1.3): gate = own C check against the partner; if not T, produce a C script; then a D script
    if the list has no D entry."""
    t = utau[u]
    ctr[C_GATE] += 1
    g = 1 if BLC[u, 0] >= 0 else 0               # rule 'lack': produce a C script only while the list has none
    if g == 1:
        ctr[C_GATE_T] += 1
    else:
        code = sig_code(u, v, rel, utau, KIND, NAT, CHD, UVt, BLC, BLD)
        sid = PRODC[t, code]
        if sid == -2:
            return -1, anc
        ctr[C_PRODC] += 1
        if sid == -3:                              # the executable producer exceeds its cap P: nothing adopted
            ctr[C_PROD_TO] += 1
            cost[0] += COSTS[5]
            sid = -1
        else:
            cost[0] += COSTS[3]
        if sid >= 0 and not holds(BLC, u, sid):
            pos = blen(BLC, u)
            u = APP[u, sid]
            anc = anc | (1 << pos)
            ctr[C_PRODC_OK] += 1
    if BLD[u, 0] < 0:
        ctr[C_PRODD] += 1
        cost[0] += COSTS[4]
        u2 = PD[u]
        if u2 == -2:
            return -1, anc
        if u2 == -3:
            ctr[C_PROD_TO] += 1
            cost[0] += COSTS[5] - COSTS[4]
            u2 = u
        if u2 != u:
            anc = anc | (1 << LMAX)
            ctr[C_PRODD_OK] += 1
            u = u2
    return u, anc


@njit(cache=True)
def make_type(d, tunit, tmode, tsp, tanc, nt, unit, mode, sp, anc):
    code = type_code(unit, mode, sp, anc)
    if code in d:
        return d[code], nt
    k = nt
    d[code] = k
    tunit[k] = unit; tmode[k] = mode; tsp[k] = sp; tanc[k] = anc
    return k, nt + 1


@njit(cache=True)
def pay(k, j, tunit, tmode, tsp, A, selfa):
    """Payoff of type k against an individual of type j (identity: same quote iff same unit, mode and spelling,
    spellings tracked for split run trees; otherwise distinct quotes)."""
    u = tunit[k]; v = tunit[j]
    if u == v and tsp[k] >= 0 and tsp[k] == tsp[j] and tmode[k] == tmode[j]:
        a = selfa[u]
        return PAYM[a, a]
    return PAYM[A[u, v], A[v, u]]


@njit(cache=True)
def cc_pair(k, j, tunit, tmode, tsp, A, selfa):
    u = tunit[k]; v = tunit[j]
    if u == v and tsp[k] >= 0 and tsp[k] == tsp[j] and tmode[k] == tmode[j]:
        return 1.0 if selfa[u] == 1 else 0.0
    return 1.0 if (A[u, v] == 1 and A[v, u] == 1) else 0.0


@njit(cache=True)
def relation(k, j, tunit, tmode, tsp):
    if tunit[k] != tunit[j]: return 0
    if tsp[k] >= 0 and tsp[k] == tsp[j] and tmode[k] == tmode[j]: return 2
    return 1


@njit(cache=True)
def transition(k, j, rel, d, tunit, tmode, tsp, tanc, ntv, utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT,
               CHC, CHD, UVt, publish, ctr, cost, COSTS):
    """The type k becomes after meeting j.  Returns (new type, error flag); ntv[0] is the type count."""
    mode = tmode[k]
    if mode == MODE_H:
        return k, 0
    u = tunit[k]; anc = tanc[k]
    u0 = u
    if mode == MODE_C or mode == MODE_CS:
        if publish:
            u, anc = trans_C(u, tunit[j], rel, anc, tanc[j], utau, BLC, BLD, SINGLE, APP, CHC, UVt, ctr, cost, COSTS)
    if mode == MODE_S or mode == MODE_CS:
        rel2 = rel
        if u != u0 and rel2 != 2:
            rel2 = 1 if u == tunit[j] else 0
        u, anc = trans_S(u, tunit[j], rel2, anc, utau, BLC, BLD, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, ctr, cost, COSTS)
        if u < 0:
            return k, 1
    if u == u0 and anc == tanc[k]:
        return k, 0
    nt = ntv[0]
    if nt >= tunit.shape[0]:
        return k, 2
    kk, nt2 = make_type(d, tunit, tmode, tsp, tanc, nt, u, mode, tsp[k], anc)
    ntv[0] = nt2
    return kk, 0


@njit(cache=True)
def pair_cost(k, j, tunit, tmode, tsp, tanc, utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt,
              publish, COSTS, dctr):
    """Modelled production steps of type k in one encounter with type j (no type is created)."""
    mode = tmode[k]
    if mode == MODE_H:
        return 0.0
    cost = np.zeros(1)
    rel = relation(k, j, tunit, tmode, tsp)
    u = tunit[k]; anc = tanc[k]; u0 = u
    if (mode == MODE_C or mode == MODE_CS) and publish:
        u, anc = trans_C(u, tunit[j], rel, anc, tanc[j], utau, BLC, BLD, SINGLE, APP, CHC, UVt, dctr, cost, COSTS)
    if mode == MODE_S or mode == MODE_CS:
        rel2 = rel
        if u != u0 and rel2 != 2:
            rel2 = 1 if u == tunit[j] else 0
        trans_S(u, tunit[j], rel2, anc, utau, BLC, BLD, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, dctr, cost, COSTS)
    return cost[0]


@njit(cache=True)
def _change(i, a, b, counts, paysum, pcs, pres, npres, pos, tunit, tmode, tsp, tanc, A, selfa, price,
            utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, publish, COSTS, dctr):
    """One individual on island i changes type a -> b (birth-death or adoption).  pcs[i, k] = sum over the
    island's individuals j of pair_cost(k, j) (maintained only when price > 0)."""
    counts[i, a] -= 1
    if counts[i, a] == 0:
        p = pos[i, a]; last = pres[i, npres[i] - 1]
        pres[i, p] = last; pos[i, last] = p; pos[i, a] = -1; npres[i] -= 1
    new = counts[i, b] == 0
    if new:
        pres[i, npres[i]] = b; pos[i, b] = npres[i]; npres[i] += 1
    counts[i, b] += 1
    for t in range(npres[i]):
        j = pres[i, t]
        if new and j == b: continue
        paysum[i, j] += pay(j, b, tunit, tmode, tsp, A, selfa) - pay(j, a, tunit, tmode, tsp, A, selfa)
        if price > 0.0 and tmode[j] != MODE_H:
            pcs[i, j] += (pair_cost(j, b, tunit, tmode, tsp, tanc, utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT,
                                    CHC, CHD, UVt, publish, COSTS, dctr)
                          - pair_cost(j, a, tunit, tmode, tsp, tanc, utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND,
                                      NAT, CHC, CHD, UVt, publish, COSTS, dctr))
    if new:
        v = 0.0; c = 0.0
        for t in range(npres[i]):
            k = pres[i, t]
            v += counts[i, k] * pay(b, k, tunit, tmode, tsp, A, selfa)
            if price > 0.0 and tmode[b] != MODE_H:
                c += counts[i, k] * pair_cost(b, k, tunit, tmode, tsp, tanc, utau, BLC, BLD, SINGLE, APP, PRODC, PD,
                                              KIND, NAT, CHC, CHD, UVt, publish, COSTS, dctr)
        paysum[i, b] = v
        pcs[i, b] = c


@njit(cache=True)
def _sample_parent(counts, paysum, pcs, pres, npres, src, N, w, tunit, tmode, tsp, tanc, A, selfa, price, Kfuel,
                   utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, publish, COSTS, dctr):
    nps = npres[src]
    fs = np.empty(nps)
    m = -1e300
    for t in range(nps):
        k = pres[src, t]
        f = (paysum[src, k] - pay(k, k, tunit, tmode, tsp, A, selfa)) / (N - 1)
        if price > 0.0 and tmode[k] != MODE_H:
            cs = (pcs[src, k] - pair_cost(k, k, tunit, tmode, tsp, tanc, utau, BLC, BLD, SINGLE, APP, PRODC, PD,
                                          KIND, NAT, CHC, CHD, UVt, publish, COSTS, dctr)) / (N - 1)
            f -= price * cs / Kfuel
        fs[t] = f
        if f > m: m = f
    tot = 0.0
    for t in range(nps):
        tot += counts[src, pres[src, t]] * np.exp(w * (fs[t] - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(nps):
        k = pres[src, t]
        acc += counts[src, k] * np.exp(w * (fs[t] - m))
        if u <= acc:
            return k
    return pres[src, nps - 1]


@njit(cache=True)
def seed_rng(seed):
    np.random.seed(seed)


@njit(cache=True)
def segment(gens, N, w, m, r, publish, inherit, price, Kfuel,
            slots, counts, paysum, pcs, pres, npres, pos, d, tunit, tmode, tsp, tanc, ntv, FU,
            utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, A, selfa, COSTS,
            ctr, steps_mode, err):
    """Run `gens` generations (I*N events each).  ctr[mode, :] counters; steps_mode[mode] modelled production
    steps; FU[mode, τ]: the founding unit of a mode (inheritance disabled)."""
    I = slots.shape[0]
    dctr = np.zeros(NCTR, np.int64)
    cost = np.zeros(1)
    for g in range(gens):
        for e in range(I * N):
            for q in range(r):
                i = np.random.randint(I)
                f = np.random.randint(N)
                p = np.random.randint(N - 1)
                if p >= f: p += 1
                kf = slots[i, f]; kp = slots[i, p]
                rel = relation(kf, kp, tunit, tmode, tsp)
                mf = tmode[kf]; mp = tmode[kp]
                cost[0] = 0.0
                nf, ef = transition(kf, kp, rel, d, tunit, tmode, tsp, tanc, ntv, utau, BLC, BLD, SINGLE, APP,
                                    PRODC, PD, KIND, NAT, CHC, CHD, UVt, publish, ctr[mf], cost, COSTS)
                steps_mode[mf] += cost[0]
                ctr[mf, C_ENC] += 1
                cost[0] = 0.0
                np_, ep = transition(kp, kf, rel, d, tunit, tmode, tsp, tanc, ntv, utau, BLC, BLD, SINGLE, APP,
                                     PRODC, PD, KIND, NAT, CHC, CHD, UVt, publish, ctr[mp], cost, COSTS)
                steps_mode[mp] += cost[0]
                ctr[mp, C_ENC] += 1
                if ef != 0 or ep != 0:
                    err[0] = 10 * ef + ep
                    return g
                if nf != kf:
                    slots[i, f] = nf; ctr[mf, C_CHANGE] += 1
                    _change(i, kf, nf, counts, paysum, pcs, pres, npres, pos, tunit, tmode, tsp, tanc, A, selfa, price,
                            utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, publish, COSTS, dctr)
                if np_ != kp:
                    slots[i, p] = np_; ctr[mp, C_CHANGE] += 1
                    _change(i, kp, np_, counts, paysum, pcs, pres, npres, pos, tunit, tmode, tsp, tanc, A, selfa, price,
                            utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, publish, COSTS, dctr)
            i = np.random.randint(I)
            src = i
            if m > 0.0 and I > 1 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            child = _sample_parent(counts, paysum, pcs, pres, npres, src, N, w, tunit, tmode, tsp, tanc, A, selfa,
                                   price, Kfuel, utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt,
                                   publish, COSTS, dctr)
            if not inherit:
                u0 = FU[tmode[child], utau[tunit[child]]]
                if u0 != tunit[child] or tanc[child] != 0:
                    if ntv[0] >= tunit.shape[0]:
                        err[0] = 3
                        return g
                    child, ntv[0] = make_type(d, tunit, tmode, tsp, tanc, ntv[0], u0, tmode[child], tsp[child], 0)
            vs = np.random.randint(N)
            kv = slots[i, vs]
            ctr[tmode[child], C_BIRTH] += 1
            if kv == child: continue
            slots[i, vs] = child
            _change(i, kv, child, counts, paysum, pcs, pres, npres, pos, tunit, tmode, tsp, tanc, A, selfa, price,
                    utau, BLC, BLD, SINGLE, APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, publish, COSTS, dctr)
    return gens


@njit(cache=True)
def island_stats(counts, pres, npres, N, tunit, tmode, tsp, A, selfa):
    """Per island: P(C,C) among ordered pairs of distinct individuals, majority type, its count."""
    I = counts.shape[0]
    cc = np.zeros(I); maj = np.zeros(I, np.int64); majn = np.zeros(I, np.int64)
    for i in range(I):
        tot = 0.0
        best = -1; bn = -1
        for t in range(npres[i]):
            a = pres[i, t]
            if counts[i, a] > bn:
                bn = counts[i, a]; best = a
            for t2 in range(npres[i]):
                b = pres[i, t2]
                nn = counts[i, a] * counts[i, b] if a != b else counts[i, a] * (counts[i, a] - 1)
                tot += nn * cc_pair(a, b, tunit, tmode, tsp, A, selfa)
        cc[i] = tot / (N * (N - 1))
        maj[i] = best; majn[i] = bn
    return cc, maj, majn


@njit(cache=True)
def e3_status(counts, pres, npres, glob_types, nglob, tunit, tmode, tsp, A, selfa):
    """Milestone 2's E3: per island, Z = closure of the residents under 'a type present anywhere joins if
    pay(q, z) >= pay(z, z) for some z in Z'; 1 if every type in Z self-cooperates, 0 if none, -1 otherwise.
    Returns per-island status."""
    I = counts.shape[0]
    out = np.zeros(I, np.int64)
    inZ = np.zeros(nglob, np.bool_)
    queue = np.empty(nglob, np.int64)
    gidx = -np.ones(tunit.shape[0], np.int64)
    for t in range(nglob): gidx[glob_types[t]] = t
    for i in range(I):
        for t in range(nglob): inZ[t] = False
        qn = 0; qh = 0
        for t in range(npres[i]):
            gi = gidx[pres[i, t]]
            inZ[gi] = True; queue[qn] = gi; qn += 1
        while qh < qn:
            z = glob_types[queue[qh]]; qh += 1
            uzz = pay(z, z, tunit, tmode, tsp, A, selfa)
            for q in range(nglob):
                if inZ[q]: continue
                qq = glob_types[q]
                if pay(qq, z, tunit, tmode, tsp, A, selfa) >= uzz - 1e-9:
                    inZ[q] = True; queue[qn] = q; qn += 1
        ns = 0
        for t in range(qn):
            k = glob_types[queue[t]]
            if cc_pair(k, k, tunit, tmode, tsp, A, selfa) > 0.5: ns += 1
        out[i] = 1 if ns == qn else (0 if ns == 0 else -1)
    return out


@njit(cache=True)
def init_paysum(counts, paysum, pcs, pres, npres, tunit, tmode, tsp, tanc, A, selfa, price, utau, BLC, BLD, SINGLE,
                APP, PRODC, PD, KIND, NAT, CHC, CHD, UVt, publish, COSTS):
    I = counts.shape[0]
    dctr = np.zeros(NCTR, np.int64)
    for i in range(I):
        for t in range(npres[i]):
            j = pres[i, t]
            v = 0.0; c = 0.0
            for t2 in range(npres[i]):
                k = pres[i, t2]
                v += counts[i, k] * pay(j, k, tunit, tmode, tsp, A, selfa)
                if price > 0.0 and tmode[j] != MODE_H:
                    c += counts[i, k] * pair_cost(j, k, tunit, tmode, tsp, tanc, utau, BLC, BLD, SINGLE, APP, PRODC,
                                                  PD, KIND, NAT, CHC, CHD, UVt, publish, COSTS, dctr)
            paysum[i, j] = v
            pcs[i, j] = c


@njit(cache=True)
def cross_pcc(counts, pres, npres, N, tunit, tmode, tsp, A, selfa):
    """Mean over ordered island pairs (i != j) of the P(C,C) of a random individual of i against one of j."""
    I = counts.shape[0]
    num = 0.0
    for a in range(I):
        for b in range(I):
            if a == b: continue
            for t in range(npres[a]):
                x = pres[a, t]
                for t2 in range(npres[b]):
                    y = pres[b, t2]
                    num += counts[a, x] * counts[b, y] * cc_pair(x, y, tunit, tmode, tsp, A, selfa)
    return num / (N * N * I * (I - 1))
