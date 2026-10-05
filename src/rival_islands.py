"""Rival networks across islands along I >> N, and the mN scaling rule.
Spec specs/2026-10-05-rival-islands.md (reviewed, reviews/2026-10-05-rival-islands-gpt-6.1-sol.md);
predictions predictions/2026-10-05-rival-islands.md.

Modal arm, PD, w = 0.3, eps = 0, iid seeds from the length prior at cutoff n (class data from
spoiler_conditioned.cdata: the modal language evaluated once at n = 12, sub-blocks for n = 6, 9), complete island
graph, uniform replacement, time in generations of I*N births.  The dynamics are those of seeds_in_n._run (Moran
birth-death, parent drawn with weight exp(w * mean payoff) on the source island, a migrant parent drawn from a
uniformly chosen other island with probability m = mN/N, victim uniform on the target island), with four changes:

  1. Migration continues after certification; separation is never a stopping rule.  A run stops only when it is
     globally outcome-frozen (every present class pairwise payoff-identical; nothing can change any payoff again) or,
     with m = 0, when every island is locally frozen; otherwise it runs to the horizon.
  2. Exact event skipping.  A birth on an island that is monomorphic, with labels settled (below), and not drawing a
     migrant changes nothing; the number of such births before the next possibly-effective birth is geometric, so it is
     drawn in one step.  The law of the process is unchanged (memorylessness); the random stream is not.
  3. Exact lumping.  Classes that are payoff-identical on the current global support (identical rows and columns of U
     restricted to present classes), with the same cooperative flag and the same network tag, are merged; a Moran
     process is lumpable over such classes.  This is what makes a separated patchwork cheap to run to the horizon.
  4. Ancestry labels.  Each individual on an island not yet established carries a label: local (lineage on this
     island since the seed) or immigrant.  Labels are inherited within the island, immigrant on a migrant birth, and
     the victim's label is drawn in proportion within its class (classes are exchangeable).  At establishment the
     island's immigrant share and the winner's local share are recorded; labels are frozen afterwards.

Definitions.  Establisher: self-cooperates, defects on D, not ALLC.  Cooperative class (coopmask): self-cooperates,
not ALLC (as seeds_in_n).  Island *established* (certified cooperative): locally frozen (present classes pairwise
payoff-identical) and every present class cooperative.  Holder: the largest class on an island.  Network tags for a
pair (A, B) of mutually-defecting establishers: 1 = self-cooperating, mutually cooperates with A and not with B (A's
network); 2 = the same with A and B swapped; 3 = mutually cooperates with both (bridge); 0 = other.  A network is
*lost* when its last individual dies (absorbing at eps = 0); *held* islands are those whose holder carries the tag.

    python3 src/rival_islands.py static              # item 1 -> runs/rival-islands-static.json
    python3 src/rival_islands.py time                # timing (separate salt; outcomes not used)
    python3 src/rival_islands.py run --exp E [--procs 3]   # E in sep, ctrl, nat, rule, merge
    python3 src/rival_islands.py report              # runs/rival-islands.md and runs/rival-islands.json
"""
import argparse, json, math, os, sys, time
from collections import Counter, defaultdict
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from numba import njit
import spoiler_conditioned as SC
import almost_all_seeds as AS
from chain import fixation

ROOT = SC.ROOT
RUNS = SC.RUNS
CACHE = SC.CACHE
W = 0.3
PDP = SC.PDP
GENS = 100000
SALT = 20261005
LUMPMAX = 400
CAP_S = 7200                 # administrative cap per cell, wall seconds on 3 workers (projected)

# predeclared pairs (n = 9): the heaviest pair for each of the three heaviest rivals of BOX1(THEM(ME))
PAIRS = [('BOX1(THEM(ME))', 'BOX1(THEM(^not(BOX(THEM(ME)))))'),
         ('BOX1(THEM(ME))', 'BOX1(THEM(^not(BOX(THEM(THEM)))))'),
         ('BOX1(THEM(ME))', 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))')]


def checks_schedule(gens):
    c = list(range(5, min(gens, 2000) + 1, 5)) + list(range(2025, min(gens, 10000) + 1, 25)) + \
        list(range(10100, gens + 1, 100))
    if not c or c[-1] != gens:
        c.append(gens)
    return np.array(c, np.int64)


# ------------------------------------------------------------------ class data
_D = {}


def cls(n):
    """V (memmap for n = 12), mu, names, flags."""
    if n in _D:
        return _D[n]
    p = os.path.join(CACHE, 'rival-V%d.npy' % n)
    if not os.path.exists(p):
        d = SC.cdata(n)
        np.save(p, np.ascontiguousarray(d['V']))
        np.save(os.path.join(CACHE, 'rival-mu%d.npy' % n), d['mu'])
        json.dump(d['names'], open(os.path.join(CACHE, 'rival-names%d.json' % n), 'w'))
        SC._C.pop(n, None)
    V = np.load(p, mmap_mode='r')
    mu = np.load(os.path.join(CACHE, 'rival-mu%d.npy' % n))
    names = json.load(open(os.path.join(CACHE, 'rival-names%d.json' % n)))
    selfc = np.array([V[k, k] for k in range(len(names))], bool)
    iC = names.index('C'); iD = names.index('D')
    allc = np.zeros(len(names), bool); allc[iC] = True
    vD = np.asarray(V[:, iD]).astype(bool)
    out = dict(n=n, V=V, mu=mu / mu.sum(), names=names, idx={x: i for i, x in enumerate(names)}, selfc=selfc,
               iC=iC, iD=iD, est=selfc & ~vD & ~allc, coop=selfc & ~allc)
    _D[n] = out
    return out


def tags_for(d, sup, A, B):
    """Network tag per support class for the pair (A, B) (global indices), 0 if no pair."""
    t = np.zeros(len(sup), np.int64)
    if A is None:
        return t
    V = d['V']
    vA = np.asarray(V[sup, A]).astype(bool); Av = np.asarray(V[A, sup]).astype(bool)
    vB = np.asarray(V[sup, B]).astype(bool); Bv = np.asarray(V[B, sup]).astype(bool)
    sc = d['coop'][sup]
    mA = vA & Av; mB = vB & Bv
    t[sc & mA & ~mB] = 1; t[sc & mB & ~mA] = 2; t[sc & mA & mB] = 3
    return t


# ------------------------------------------------------------------ kernel
@njit(cache=True)
def _setact(i, a, act, apos, nact):
    p = apos[i]
    if a and p >= nact:
        j = act[nact]; act[nact] = i; act[p] = j; apos[i] = nact; apos[j] = p; nact += 1
    elif (not a) and p < nact:
        nact -= 1; j = act[nact]; act[nact] = i; act[p] = j; apos[i] = nact; apos[j] = p
    return nact


@njit(cache=True)
def _repay(i, counts, paysum, U, pres, npres):
    for t in range(npres[i]):
        j = pres[i, t]; v = 0.0
        for t2 in range(npres[i]):
            k = pres[i, t2]
            v += counts[i, k] * U[j, k]
        paysum[i, j] = v


@njit(cache=True)
def _isactive(i, npres, est, locsum, N):
    return npres[i] > 1 or (est[i] == 0 and locsum[i] > 0 and locsum[i] < N)


@njit(cache=True)
def _kern(U, PCC, coopmask, tag, init, N, w, m, seed, checks, lump, iD, r1, r2, preest, kprop):
    """kprop = 1: the single-migrant kernel (draw for draw as before).  kprop > 1: propagule migration
    (src/island_path.py): a migration event happens with probability m/kprop per birth instead of m, draws kprop
    offspring without replacement from one uniformly chosen other island (fitness-weighted per individual, as the
    single-migrant parent) and replaces kprop uniformly chosen residents of the recipient simultaneously."""
    np.random.seed(seed)
    I, K = init.shape
    counts = init.copy(); loc = init.copy()
    locsum = np.zeros(I, np.int64)
    paysum = np.zeros((I, K))
    pres = np.zeros((I, K), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, K), np.int64)
    glob = np.zeros(K, np.int64)
    for i in range(I):
        for k in range(K):
            if counts[i, k] > 0:
                pres[i, npres[i]] = k; pos[i, k] = npres[i]; npres[i] += 1
                glob[k] += counts[i, k]; locsum[i] += counts[i, k]
        _repay(i, counts, paysum, U, pres, npres)
    gtag = np.zeros(4, np.int64)
    for k in range(K): gtag[tag[k]] += glob[k]
    t_ext = -np.ones(4)
    for t in range(4):
        if gtag[t] == 0: t_ext[t] = 0.0
    parent = np.arange(K)
    est = np.zeros(I, np.int64)
    # per-island records
    t_est = -np.ones(I, np.int64); e_arr = np.zeros(I, np.int64); e_arrC = np.zeros(I, np.int64); e_arrD = np.zeros(I, np.int64)
    e_imm = -np.ones(I); e_hold = -np.ones(I, np.int64); e_hloc = -np.ones(I)
    t90 = -np.ones(I, np.int64); a90 = np.zeros(I, np.int64); imm90 = -np.ones(I); h90 = -np.ones(I, np.int64); hl90 = -np.ones(I)
    arr = np.zeros(I, np.int64); arrC = np.zeros(I, np.int64); arrD = np.zeros(I, np.int64); arr_all = np.zeros(I, np.int64)
    strong = np.zeros(I, np.int64)
    nloss = 0; loss_log = np.zeros((2000, 4), np.int64)       # gen, island, holder before (last strong check), holder after
    lasthold = -np.ones(I, np.int64)
    nchk = len(checks)
    trace = np.zeros((nchk, 14))
    # strong-holder transitions (class with >= 0.9 of an island; additions for island_path, no effect on dynamics)
    shold = -np.ones(I, np.int64); ntr = 0; tr_log = np.zeros((50000, 4), np.int64)   # gen, island, old cls, new cls
    mig_ct = np.zeros((4, 5), np.int64)        # migrant individuals by (child tag, recipient strong-holder tag; 4 = none)
    prem = np.zeros(K, np.int64); pvic = np.zeros(K, np.int64); pch = np.zeros(K, np.int64)
    first_sep = -1; sep_a = -1; sep_b = -1; nsepchk = 0
    held_zero = -np.ones(4, np.int64)
    act = np.arange(I); apos = np.arange(I); nact = 0
    for i in range(I):
        if preest[i] == 1:
            est[i] = 1; t_est[i] = 0
            h = pres[i, 0]
            e_hold[i] = h; e_hloc[i] = 1.0; e_imm[i] = 0.0; t90[i] = 0; h90[i] = h; hl90[i] = 1.0; imm90[i] = 0.0
        if _isactive(i, npres, est, locsum, N):
            nact = _setact(i, True, act, apos, nact)
        for t in range(npres[i]):
            if 10 * counts[i, pres[i, t]] >= 9 * N: shold[i] = pres[i, t]
    IN = I * N
    total = checks[nchk - 1] * IN
    mm = m if I > 1 else 0.0
    mm = mm / kprop
    b = 0
    ci = 0
    nextchk = checks[0] * IN
    status = 0; stop_gen = checks[nchk - 1]
    lastP = -1
    while True:
        pa = (nact + (I - nact) * mm) / I
        if pa <= 0.0:
            G = total + 1
        elif pa >= 1.0:
            G = 0
        else:
            uu = np.random.random()
            G = int(np.log(1.0 - uu) / np.log(1.0 - pa))
        if b + G >= nextchk:
            b = nextchk
            g = checks[ci]
            # ---------------- check
            ncert = 0; cc_tot = 0.0
            held = np.zeros(4, np.int64); heldc = np.zeros(4, np.int64)
            hl = np.zeros(I, np.int64); nh = 0
            for i in range(I):
                co = 0; allco = True; big = pres[i, 0]
                for t in range(npres[i]):
                    k = pres[i, t]
                    if coopmask[k]: co += counts[i, k]
                    else: allco = False
                    if counts[i, k] > counts[i, big]: big = k
                lo = 1e300; hi = -1e300
                for t in range(npres[i]):
                    a = pres[i, t]
                    for t2 in range(npres[i]):
                        q = pres[i, t2]
                        if U[a, q] < lo: lo = U[a, q]
                        if U[a, q] > hi: hi = U[a, q]
                fz = hi - lo < 1e-12
                cert = fz and allco
                held[tag[big]] += 1
                if cert:
                    ncert += 1; heldc[tag[big]] += 1
                    new = True
                    for u in range(nh):
                        if hl[u] == big: new = False; break
                    if new:
                        hl[nh] = big; nh += 1
                cc, pay = AS._island_cc(counts, PCC, U, pres, npres, paysum, i, N)
                cc_tot += cc
                if t90[i] < 0 and 10 * co >= 9 * N:
                    hb = -1
                    for t in range(npres[i]):
                        k = pres[i, t]
                        if coopmask[k] and (hb < 0 or counts[i, k] > counts[i, hb]): hb = k
                    t90[i] = g; a90[i] = arr[i]; imm90[i] = 1.0 - locsum[i] / N; h90[i] = hb; hl90[i] = loc[i, hb] / counts[i, hb]
                if cert and est[i] == 0:
                    est[i] = 1; t_est[i] = g; e_arr[i] = arr[i]; e_arrC[i] = arrC[i]; e_arrD[i] = arrD[i]
                    e_imm[i] = 1.0 - locsum[i] / N; e_hold[i] = big; e_hloc[i] = loc[i, big] / counts[i, big]
                    nact = _setact(i, _isactive(i, npres, est, locsum, N), act, apos, nact)
                if strong[i] == 1 and 2 * co < N:
                    if nloss < 2000:
                        loss_log[nloss, 0] = g; loss_log[nloss, 1] = i; loss_log[nloss, 2] = lasthold[i]; loss_log[nloss, 3] = big
                    nloss += 1
                if 10 * co >= 9 * N:
                    strong[i] = 1; lasthold[i] = big
                elif 2 * co < N:
                    strong[i] = 0
            sepf = 0
            for u in range(nh):
                for v in range(u + 1, nh):
                    a = hl[u]; q = hl[v]
                    if U[a, q] < -0.5 and U[q, a] < -0.5 and U[a, q] > -1.5 and U[q, a] > -1.5:
                        sepf = 1
                        if first_sep < 0:
                            first_sep = g; sep_a = a; sep_b = q
            nsepchk += sepf
            for t in range(1, 4):
                if held[t] == 0 and held_zero[t] < 0: held_zero[t] = g
            nP = 0
            for k in range(K):
                if glob[k] > 0: nP += 1
            trace[ci, 0] = g; trace[ci, 1] = gtag[1]; trace[ci, 2] = gtag[2]; trace[ci, 3] = held[1]; trace[ci, 4] = held[2]
            trace[ci, 5] = heldc[1]; trace[ci, 6] = heldc[2]; trace[ci, 7] = ncert; trace[ci, 8] = sepf; trace[ci, 9] = cc_tot / I
            trace[ci, 10] = nact; trace[ci, 11] = nP; trace[ci, 12] = held[3]; trace[ci, 13] = heldc[3]
            for i in range(I):
                for t in range(npres[i]):
                    k = pres[i, t]
                    if 10 * counts[i, k] >= 9 * N and shold[i] != k:
                        if ntr < 50000:
                            tr_log[ntr, 0] = g; tr_log[ntr, 1] = i; tr_log[ntr, 2] = shold[i]; tr_log[ntr, 3] = k
                        ntr += 1
                        shold[i] = k
            ci += 1
            # ---------------- stopping
            if mm > 0.0:
                Pl = np.zeros(nP, np.int64); z = 0
                for k in range(K):
                    if glob[k] > 0:
                        Pl[z] = k; z += 1
                lo = 1e300; hi = -1e300
                for x in range(nP):
                    a = Pl[x]
                    for y in range(nP):
                        q = Pl[y]
                        if U[a, q] < lo: lo = U[a, q]
                        if U[a, q] > hi: hi = U[a, q]
                    if hi - lo >= 1e-12: break
                if hi - lo < 1e-12:
                    status = 1; stop_gen = g; break
            else:
                allf = True
                for i in range(I):
                    lo = 1e300; hi = -1e300
                    for t in range(npres[i]):
                        a = pres[i, t]
                        for t2 in range(npres[i]):
                            q = pres[i, t2]
                            if U[a, q] < lo: lo = U[a, q]
                            if U[a, q] > hi: hi = U[a, q]
                    if hi - lo >= 1e-12:
                        allf = False; break
                if allf:
                    status = 5; stop_gen = g; break
            if ci >= nchk:
                break
            nextchk = checks[ci] * IN
            # ---------------- lumping
            if lump and nP <= LUMPMAX and nP != lastP:
                P = np.zeros(nP, np.int64); h = np.zeros(nP); z = 0
                for k in range(K):
                    if glob[k] > 0:
                        P[z] = k; z += 1
                for z in range(nP):
                    a = P[z]; v = 0.0
                    for z2 in range(nP):
                        q = P[z2]
                        v += U[a, q] * r1[q] + U[q, a] * r2[q]
                    h[z] = v + 1000.0 * tag[a] + 10000.0 * coopmask[a]
                order = np.argsort(h)
                for x in range(nP):
                    a = P[order[x]]
                    if glob[a] == 0: continue
                    y = x + 1
                    while y < nP and abs(h[order[y]] - h[order[x]]) < 1e-9:
                        q = P[order[y]]
                        y += 1
                        if glob[q] == 0: continue
                        if tag[a] != tag[q] or coopmask[a] != coopmask[q]: continue
                        same = True
                        for z in range(nP):
                            c = P[z]
                            if glob[c] == 0: continue
                            if U[a, c] != U[q, c] or U[c, a] != U[c, q]:
                                same = False; break
                        if not same: continue
                        # merge q into a
                        parent[q] = a
                        for i in range(I):
                            if counts[i, q] == 0: continue
                            if counts[i, a] == 0:
                                pres[i, npres[i]] = a; pos[i, a] = npres[i]; npres[i] += 1
                            counts[i, a] += counts[i, q]; loc[i, a] += loc[i, q]; counts[i, q] = 0; loc[i, q] = 0
                            p = pos[i, q]; last = pres[i, npres[i] - 1]
                            pres[i, p] = last; pos[i, last] = p; pos[i, q] = -1; npres[i] -= 1
                            _repay(i, counts, paysum, U, pres, npres)
                            if lasthold[i] == q: lasthold[i] = a
                            if shold[i] == q: shold[i] = a
                            nact = _setact(i, _isactive(i, npres, est, locsum, N), act, apos, nact)
                        glob[a] += glob[q]; glob[q] = 0
                nP2 = 0
                for k in range(K):
                    if glob[k] > 0: nP2 += 1
                lastP = nP2
            continue
        # ---------------- one possibly-effective birth
        b = b + G + 1
        if np.random.random() * pa * I < nact:
            i = act[np.random.randint(nact)]
            mig = mm > 0.0 and np.random.random() < mm
        else:
            i = act[nact + np.random.randint(I - nact)]
            mig = True
        src = i
        if mig:
            src = np.random.randint(I - 1)
            if src >= i: src += 1
        if mig and kprop > 1:
            # ---------------- propagule event: kprop offspring from src replace kprop residents of i at once
            fm = -1e300
            for t in range(npres[src]):
                k = pres[src, t]
                f = (paysum[src, k] - U[k, k]) / (N - 1)
                if f > fm: fm = f
            for t in range(npres[src]):
                k = pres[src, t]; prem[k] = counts[src, k]
            for t in range(npres[i]):
                k = pres[i, t]; pvic[k] = 0
            for x in range(kprop):
                tot = 0.0
                for t in range(npres[src]):
                    k = pres[src, t]
                    tot += prem[k] * np.exp(w * ((paysum[src, k] - U[k, k]) / (N - 1) - fm))
                u = np.random.random() * tot; acc = 0.0; ch = -1
                for t in range(npres[src]):
                    if prem[pres[src, t]] > 0: ch = pres[src, t]          # fallback: last class with copies left
                for t in range(npres[src]):
                    k = pres[src, t]
                    acc += prem[k] * np.exp(w * ((paysum[src, k] - U[k, k]) / (N - 1) - fm))
                    if u <= acc and prem[k] > 0:
                        ch = k; break
                prem[ch] -= 1; pch[ch] += 1
            nleft = N
            for x in range(kprop):
                u2 = np.random.randint(nleft); acc2 = 0; vc = pres[i, 0]
                for t in range(npres[i]):
                    k = pres[i, t]; acc2 += counts[i, k] - pvic[k]
                    if u2 < acc2:
                        vc = k; break
                pvic[vc] += 1; nleft -= 1
            arr_all[i] += kprop
            hs = shold[i]
            hst = 4 if hs < 0 else tag[hs]
            # removals first (victim labels drawn among the pre-event residents of their class), then additions
            for t in range(npres[i]):
                k = pres[i, t]
                for x in range(pvic[k]):
                    if est[i] == 0:
                        vl = 1 if np.random.random() * (counts[i, k] - x) < loc[i, k] else 0
                        loc[i, k] -= vl; locsum[i] -= vl
            nt = npres[i]
            t = 0
            while t < nt:
                k = pres[i, t]
                if pvic[k] > 0:
                    counts[i, k] -= pvic[k]; glob[k] -= pvic[k]; gtag[tag[k]] -= pvic[k]
                    pvic[k] = 0
                if counts[i, k] == 0:
                    p = pos[i, k]; last = pres[i, npres[i] - 1]
                    pres[i, p] = last; pos[i, last] = p; pos[i, k] = -1; npres[i] -= 1; nt -= 1
                    continue
                t += 1
            for t in range(npres[src]):
                k = pres[src, t]
                if pch[k] == 0: continue
                c = pch[k]; pch[k] = 0
                mig_ct[tag[k], hst] += c
                if est[i] == 0:
                    arr[i] += c
                    if coopmask[k]: arrC[i] += c
                    if k == iD: arrD[i] += c
                if counts[i, k] == 0:
                    pres[i, npres[i]] = k; pos[i, k] = npres[i]; npres[i] += 1
                counts[i, k] += c; glob[k] += c; gtag[tag[k]] += c
            for t in range(4):
                if gtag[t] == 0 and t_ext[t] < 0: t_ext[t] = b / IN
            _repay(i, counts, paysum, U, pres, npres)
            nact = _setact(i, _isactive(i, npres, est, locsum, N), act, apos, nact)
            continue
        child = AS._sample_parent(counts, paysum, U, pres, npres, src, N, w)
        u = np.random.randint(N); acc = 0; victim = pres[i, 0]
        for t in range(npres[i]):
            k = pres[i, t]; acc += counts[i, k]
            if u < acc:
                victim = k; break
        if mig:
            arr_all[i] += 1
            mig_ct[tag[child], 4 if shold[i] < 0 else tag[shold[i]]] += 1
        if est[i] == 0:
            if mig:
                cl = 0
                arr[i] += 1
                if coopmask[child]: arrC[i] += 1
                if child == iD: arrD[i] += 1
            else:
                cl = 1 if np.random.random() * counts[i, child] < loc[i, child] else 0
            vl = 1 if np.random.random() * counts[i, victim] < loc[i, victim] else 0
            loc[i, victim] -= vl; loc[i, child] += cl; locsum[i] += cl - vl
        if victim != child:
            counts[i, victim] -= 1; glob[victim] -= 1
            gtag[tag[victim]] -= 1
            if gtag[tag[victim]] == 0 and t_ext[tag[victim]] < 0:
                t_ext[tag[victim]] = b / IN
            if counts[i, victim] == 0:
                p = pos[i, victim]; last = pres[i, npres[i] - 1]
                pres[i, p] = last; pos[i, last] = p; pos[i, victim] = -1; npres[i] -= 1
            new = counts[i, child] == 0
            if new:
                pres[i, npres[i]] = child; pos[i, child] = npres[i]; npres[i] += 1
            counts[i, child] += 1; glob[child] += 1; gtag[tag[child]] += 1
            for t in range(npres[i]):
                j = pres[i, t]
                if new and j == child:
                    continue
                paysum[i, j] += U[j, child] - U[j, victim]
            if new:
                v = 0.0
                for t in range(npres[i]):
                    k = pres[i, t]
                    v += counts[i, k] * U[child, k]
                paysum[i, child] = v
        nact = _setact(i, _isactive(i, npres, est, locsum, N), act, apos, nact)
    if status == 0:
        allf = True
        for i in range(I):
            lo = 1e300; hi = -1e300
            for t in range(npres[i]):
                a = pres[i, t]
                for t2 in range(npres[i]):
                    q = pres[i, t2]
                    if U[a, q] < lo: lo = U[a, q]
                    if U[a, q] > hi: hi = U[a, q]
            if hi - lo >= 1e-12:
                allf = False
        status = 3 if allf else 4
    isl_cc = np.zeros(I); isl_pay = np.zeros(I)
    for i in range(I):
        isl_cc[i], isl_pay[i] = AS._island_cc(counts, PCC, U, pres, npres, paysum, i, N)
    return (status, stop_gen, counts, isl_cc, isl_pay, trace[:ci], t_ext, held_zero, parent,
            t_est, e_arr, e_arrC, e_arrD, e_imm, e_hold, e_hloc, t90, a90, imm90, h90, hl90, arr_all,
            loss_log[:min(nloss, 2000)], nloss, first_sep, sep_a, sep_b, nsepchk, tr_log[:min(ntr, 50000)], ntr, mig_ct)


STATUS = {1: 'frozen', 3: 'horizon-certified', 4: 'unresolved', 5: 'local-frozen'}


# ------------------------------------------------------------------ one run
PRESETS = ('iid', 'AB', 'A', 'halfAB', 'minorB')


def seeds(exp, n, N, I, mN, rep, pair, preset):
    code = {'sep': 1, 'ctrl': 2, 'nat': 3, 'rule': 4, 'time': 9, 'val': 8}[exp]
    pc = PRESETS.index(preset)
    rs = [SALT, code, n, N, I, int(round(mN * 100)), rep, 99 if pair is None else pair, pc]
    ss = (1000003 * rep + 7919 * code + 104729 * pc + 13 * N + 17 * I + int(round(mN * 1000)) + 31 * n
          + 101 * (0 if pair is None else pair + 1) + SALT) % (2 ** 31 - 1)
    return rs, ss


def build_init(d, N, I, pair, preset, rng):
    K = len(d['mu'])
    A = B = None
    if pair is not None:
        A = d['idx'][PAIRS[pair][0]]; B = d['idx'][PAIRS[pair][1]]
    init = np.zeros((I, K), np.int64)
    pre = np.zeros(I, np.int64)
    if preset in ('iid', 'AB', 'A'):
        for i in range(I):
            init[i] = rng.multinomial(N, d['mu'])
    if preset == 'AB':
        init[0] = 0; init[0, A] = N; init[1] = 0; init[1, B] = N; pre[:2] = 1
    elif preset == 'A':
        init[0] = 0; init[0, A] = N; pre[0] = 1
    elif preset == 'halfAB':
        init[:I // 2, A] = N; init[I // 2:, B] = N; pre[:] = 1
    elif preset == 'minorB':
        init[0, B] = N; init[1:, A] = N; pre[:] = 1
    return init, pre, A, B


def restrict(d, init, A, B):
    sup = np.nonzero(init.sum(0) > 0)[0]
    extra = [x for x in (A, B) if x is not None and x not in set(sup.tolist())]
    if extra:
        sup = np.sort(np.concatenate([sup, np.array(extra, np.int64)]))
    Vs = np.asarray(d['V'][np.ix_(sup, sup)]).astype(np.int64)
    U = np.ascontiguousarray(PDP[Vs, Vs.T])
    PCC = np.ascontiguousarray((Vs * Vs.T).astype(float))
    coop = d['coop'][sup].copy()
    tag = tags_for(d, sup, A, B)
    return sup, U, PCC, coop, tag


def simulate(d, init, pre, A, B, N, mN, seed, gens, lump=True):
    sup, U, PCC, coop, tag = restrict(d, init, A, B)
    loc_init = np.ascontiguousarray(init[:, sup])
    K = len(sup)
    rr = np.random.default_rng(seed)
    r1 = rr.random(K); r2 = rr.random(K)
    iDl = int(np.searchsorted(sup, d['iD'])) if d['iD'] in set(sup.tolist()) else -1
    out = _kern(U, PCC, coop, tag, loc_init, N, W, mN / N, seed, checks_schedule(gens), lump, iDl, r1, r2, pre, 1)
    return sup, U, PCC, coop, tag, out


def holder(counts_i):
    nz = np.nonzero(counts_i)[0]
    return int(nz[np.argmax(counts_i[nz])])


def job(j):
    exp, n, N, I, mN, rep, gens, pair, preset = j
    d = cls(n); nm = d['names']
    rs, ss = seeds(exp, n, N, I, mN, rep, pair, preset)
    rng = np.random.default_rng(rs)
    init, pre, A, B = build_init(d, N, I, pair, preset, rng)
    t0 = time.time()
    sup, U, PCC, coop, tag, o = simulate(d, init, pre, A, B, N, mN, ss, gens)
    (st, sg, counts, isl_cc, isl_pay, trace, t_ext, held_zero, parent, t_est, e_arr, e_arrC, e_arrD, e_imm, e_hold, e_hloc,
     t90, a90, imm90, h90, hl90, arr_all, loss_log, nloss, first_sep, sep_a, sep_b, nsepchk) = o[:28]
    G = lambda k: nm[int(sup[k])] if k >= 0 else None
    glob = counts.sum(0)
    hold = [holder(counts[i]) for i in range(I)]
    root = np.arange(len(sup))
    for k in range(len(sup)):
        r = k
        while parent[r] != r: r = parent[r]
        root[k] = r
    groups = defaultdict(list)
    for k in range(len(sup)):
        if root[k] != k: groups[int(root[k])].append(G(k))
    final = {G(k): int(v) for k, v in enumerate(glob) if v > 0}
    held_final = Counter(int(tag[h]) for h in hold)
    heldc_final = Counter(int(tag[h]) for i, h in enumerate(hold) if isl_cc[i] >= 0.95)
    # counterfactual cross-island P(C,C) under uniform mixing (a counterfactual, not realized efficiency)
    x = glob / glob.sum(); pr = np.nonzero(x)[0]
    cf = float(x[pr] @ PCC[np.ix_(pr, pr)] @ x[pr])
    cc = float(isl_cc.mean()); pay = float(isl_pay.mean())
    hc = sorted({h for i, h in enumerate(hold) if isl_cc[i] >= 0.95 and coop[h]})
    sep_end = [(G(a), G(b)) for ai, a in enumerate(hc) for b in hc[ai + 1:] if U[a, b] == -1 and U[b, a] == -1]
    r = dict(exp=exp, n=n, N=N, I=I, mN=mN, rep=rep, gens=gens, pair=pair, preset=preset,
             A=None if A is None else nm[A], B=None if B is None else nm[B],
             status=STATUS[int(st)], stop_gen=int(sg), pcc=cc, pay=pay,
             outcome=AS.outcome(cc, pay) if st in (1, 3, 5) else 'unresolved',
             n_support=int(len(sup)), final_top=sorted(final.items(), key=lambda kv: -kv[1])[:8], n_final=len(final),
             groups={G(k): v[:6] for k, v in groups.items() if glob[k] > 0},
             holders=Counter(G(h) for h in hold).most_common(12),
             held_final={str(k): v for k, v in held_final.items()}, heldc_final={str(k): v for k, v in heldc_final.items()},
             tag_final={str(t): int(glob[tag == t].sum()) for t in range(4)},
             t_ext=[float(v) for v in t_ext], held_zero=[int(v) for v in held_zero],
             cf_cross_pcc=cf, isl_out=dict(Counter(AS.outcome(c, p) for c, p in zip(isl_cc, isl_pay))),
             first_sep=int(first_sep), first_sep_pair=(G(sep_a), G(sep_b)) if first_sep >= 0 else None,
             n_sep_checks=int(nsepchk), sep_end=sep_end[:10], n_sep_end_pairs=len(sep_end),
             sep_end_holders=[(G(h), int(sum(1 for i, hh in enumerate(hold) if hh == h and isl_cc[i] >= 0.95))) for h in hc] if sep_end else None,
             n_loss=int(nloss), losses=[(int(a), int(b_), G(int(c)), G(int(e))) for a, b_, c, e in loss_log[:30]],
             time_s=time.time() - t0)
    # rival flags relative to the FairBot pair (natural runs): cooperative, mutually defecting with FairBot or BOX1(THEM(ME))
    V = d['V']
    refs = [d['idx']['BOX(THEM(ME))'], d['idx']['BOX1(THEM(ME))']]
    vr = np.zeros(len(sup), bool)
    for ref in refs:
        vr |= (np.asarray(V[sup, ref]) == 0) & (np.asarray(V[ref, sup]) == 0)
    riv = coop & vr
    mainnet = coop & (np.asarray(V[sup, refs[1]]) == 1) & (np.asarray(V[refs[1], sup]) == 1)
    local = e_hloc >= 0.5
    estd = t_est >= 0
    bg = pre == 0
    # establishment summary over background islands: (category of holder at establishment) x ancestry
    def cat(k):
        if k < 0: return 'none'
        if tag[k] in (1, 2, 3): return 'tag%d' % tag[k]
        if riv[k]: return 'rival'
        if mainnet[k]: return 'main'
        return 'other'
    es = Counter()
    for i in range(I):
        if bg[i]:
            es[cat(int(e_hold[i])) + ('/local' if (estd[i] and local[i]) else ('/imm' if estd[i] else ''))] += 1
    r['est_summary'] = dict(es)
    # first immigrant-founded establishment (background islands) and local establishments by tag before it
    order = sorted([i for i in range(I) if bg[i] and estd[i]], key=lambda i: t_est[i])
    fimm = next((int(t_est[i]) for i in order if not local[i]), -1)
    before = Counter(cat(int(e_hold[i])) for i in order if local[i] and (fimm < 0 or t_est[i] < fimm))
    r['first_imm_est'] = fimm; r['local_before_first_imm'] = dict(before)
    first_est = next((i for i in order), None)
    r['first_est_cat'] = cat(int(e_hold[first_est])) if first_est is not None else None
    r['first_est_t'] = int(t_est[first_est]) if first_est is not None else -1
    r['n_local_est'] = int(sum(1 for i in range(I) if bg[i] and estd[i] and local[i]))
    r['n_bg'] = int(bg.sum())
    if exp != 'nat' or sep_end:
        r.update(t_est=t_est.tolist(), e_arr=e_arr.tolist(), e_arrC=e_arrC.tolist(), e_arrD=e_arrD.tolist(),
                 e_imm=[round(float(v), 3) for v in e_imm], e_cat=[cat(int(k)) for k in e_hold],
                 e_hloc=[round(float(v), 3) for v in e_hloc], t90=t90.tolist(), a90=a90.tolist(),
                 imm90=[round(float(v), 3) for v in imm90], hl90=[round(float(v), 3) for v in hl90], arr_all=arr_all.tolist())
    else:
        ok = bg & estd
        r['est_stats'] = dict(n=int(ok.sum()), t_med=float(np.median(t_est[ok])) if ok.any() else None,
                              arr_mean=float(e_arr[ok].mean()) if ok.any() else None, imm_mean=float(e_imm[ok].mean()) if ok.any() else None)
    if exp in ('sep', 'ctrl'):
        g = trace[:, 0]
        grid = sorted(set(int(np.searchsorted(g, x)) for x in np.unique(np.round(np.logspace(1, 5, 60)))))
        grid = [k for k in grid if k < len(trace)]
        r['trace'] = trace[grid][:, [0, 1, 2, 3, 4, 7, 8, 9]].round(3).tolist()   # g, nA, nB, heldA, heldB, ncert, sep, cc
    if exp in ('sep', 'ctrl', 'nat', 'time') and mN > 0 and st in (3, 4):
        r['end_counts'] = {G(k): counts[:, k].tolist() for k in np.nonzero(glob)[0]}      # for the merge test
        r['end_tag'] = {G(k): int(tag[k]) for k in np.nonzero(glob)[0]}
    return r


# ------------------------------------------------------------------ cells and runner
def cells(exp):
    """(exp, n, N, I, mN, reps, pair, preset)."""
    out = []
    if exp == 'sep':
        for p in range(3):
            for I in (16, 64, 256):
                for mN in (0.1, 1.0, 10.0):
                    out.append(('sep', 9, 100, I, mN, 40, p, 'AB'))
    elif exp == 'ctrl':
        for p in range(3):
            for I in (16, 64, 256):
                out.append(('ctrl', 9, 100, I, 0.0, 40, p, 'AB'))
        for preset in ('A', 'halfAB', 'minorB'):
            for I in (16, 64, 256):
                for mN in (0.1, 1.0, 10.0):
                    out.append(('ctrl', 9, 100, I, mN, 40, 0, preset))
        for preset in ('halfAB', 'minorB'):          # addendum S4: N = 200
            for mN in (1.0, 10.0):
                out.append(('ctrl', 9, 200, 64, mN, 40, 0, preset))
    elif exp == 'nat':
        for n in (9, 12):
            for I in (64, 256, 1024):
                for mN in (0.1, 1.0):
                    out.append(('nat', n, 100, I, mN, 100, None, 'iid'))
    elif exp == 'nat2':           # extra replication at rare cells (decided from the first 100)
        rows = load('nat')
        for c in cells('nat'):
            rs = [r for r in rows if ckey(r) == c[:5] + c[6:]]
            if len(rs) >= 100 and sum(1 for r in rs if r['sep_end']) / len(rs) < 0.05:
                out.append(c[:5] + (300,) + c[6:])
    elif exp == 'rule':
        for N, I in ((100, 16), (100, 64), (400, 16), (400, 64), (100, 256)):
            for mN in (0.03, 0.1, 0.3, 1.0, 3.0, 10.0):
                out.append(('rule', 9, N, I, mN, 40, None, 'iid'))
        for N in (100, 400):
            out.append(('rule', 9, N, 16, 0.0, 40, None, 'iid'))
    return out


def rows_path(exp):
    return os.path.join(RUNS, 'rival-islands-rows-%s.json.gz' % exp)


def load(exp):
    import gzip
    p = rows_path(exp)
    return json.load(gzip.open(p, 'rt')) if os.path.exists(p) else []


def save(exp, rows):
    import gzip
    json.dump(rows, gzip.open(rows_path(exp), 'wt'))


def ckey(r):
    return (r['exp'], r['n'], r['N'], r['I'], r['mN'], r['pair'], r['preset'])


def warm():
    d = cls(9)
    job(('time', 9, 20, 4, 1.0, 0, 50, 0, 'AB'))


def run_main(a):
    exp = a.exp
    store = 'nat' if exp == 'nat2' else exp
    rows = load(store)
    done = Counter(ckey(r) for r in rows)
    jobs = []
    for c in cells(exp):
        e, n, N, I, mN, reps, pair, preset = c
        k = (e, n, N, I, mN, pair, preset)
        for rep in range(done[k], reps):
            jobs.append((e, n, N, I, mN, rep, a.gens, pair, preset))
    jobs.sort(key=lambda j: -j[2] * j[3] * (1 + j[4]))
    print('%d jobs' % len(jobs), flush=True)
    t0 = time.time()
    cell_t = Counter(); censored = set()
    with Pool(a.procs, initializer=warm) as pool:
        for r in pool.imap_unordered(job, jobs):
            rows.append(r)
            k = ckey(r); cell_t[k] += r['time_s']
            if cell_t[k] > 3 * CAP_S:
                censored.add(k)
            print('%s n=%d N=%d I=%d mN=%g pair=%s %s rep %d: %s gen %d %s held %s ext %s sep %s (%.1fs; %.0fs total)' % (
                r['exp'], r['n'], r['N'], r['I'], r['mN'], r['pair'], r['preset'], r['rep'], r['status'], r['stop_gen'],
                r['outcome'], r['held_final'], [round(x) for x in r['t_ext'][1:3]], r['n_sep_end_pairs'], r['time_s'],
                time.time() - t0), flush=True)
            if len(rows) % 50 == 0:
                save(store, rows)
    save(store, rows)
    if censored:
        print('CELLS OVER CAP:', censored)


# ------------------------------------------------------------------ merge test (item 5)
def merge_one(r):
    """Merge a run's end state into one well-mixed island of I*N at eps = 0 and run to local freezing."""
    n = r['n']; d = cls(n)
    names = list(r['end_counts'].keys())
    gi = np.array([d['idx'][x] for x in names], np.int64)
    o = np.argsort(gi); gi = gi[o]; names = [names[k] for k in o]
    tot = np.array([sum(r['end_counts'][x]) for x in names], np.int64)
    NN = int(tot.sum())
    Vs = np.asarray(d['V'][np.ix_(gi, gi)]).astype(np.int64)
    U = np.ascontiguousarray(PDP[Vs, Vs.T]); PCC = np.ascontiguousarray((Vs * Vs.T).astype(float))
    coop = d['coop'][gi].copy()
    tag = np.array([r['end_tag'][x] for x in names], np.int64)
    init = tot.reshape(1, -1).copy()
    K = len(names)
    seed = (int(r['rep']) * 7 + int(r['I']) * 13 + int(round(r['mN'] * 100)) + 99991) % (2 ** 31 - 1)
    rr = np.random.default_rng(seed)
    t0 = time.time()
    out = _kern(U, PCC, coop, tag, init, NN, W, 0.0, seed, checks_schedule(GENS), True, -1, rr.random(K), rr.random(K),
                np.ones(1, np.int64), 1)
    st, sg, counts = out[0], out[1], out[2]
    fin = counts[0]
    # clean two-type merge: two largest classes >= 0.98 of the population and mutually defecting
    top = np.argsort(-tot)[:2]
    clean = len(top) == 2 and tot[top].sum() >= 0.98 * NN and U[top[0], top[1]] == -1 and U[top[1], top[0]] == -1
    # network shares before (by tag if tagged, else by mutual-cooperation component of the cooperative classes)
    pre = {str(t): int(tot[tag == t].sum()) for t in range(4)}
    post = {str(t): int(fin[tag == t].sum()) for t in range(4)}
    win = [names[k] for k in np.nonzero(fin)[0]]
    larger = names[top[0]]; smaller = names[top[1]] if len(top) > 1 else None
    larger_won = bool(fin[top[0]] > 0 and (len(top) < 2 or fin[top[1]] == 0))
    minority_won = bool(len(top) == 2 and fin[top[1]] > 0 and fin[top[0]] == 0)
    return dict(exp=r['exp'], n=n, N=r['N'], I=r['I'], mN=r['mN'], pair=r['pair'], preset=r['preset'], rep=r['rep'],
                NN=NN, status=STATUS[int(st)], gens_to_freeze=int(sg), clean=bool(clean),
                top2=[(names[k], int(tot[k])) for k in top], share_larger=float(tot[top[0]] / tot[top].sum()) if len(top) == 2 else 1.0,
                pre_tags=pre, post_tags=post, winners=win[:6], larger_won=larger_won, minority_won=minority_won,
                time_s=time.time() - t0)


def merge_main(a):
    src = []
    for e in ('sep', 'ctrl', 'nat'):
        src += [r for r in load(e) if 'end_counts' in r and (r['n_sep_end_pairs'] > 0 or
                (r.get('held_final', {}).get('1', 0) > 0 and r.get('held_final', {}).get('2', 0) > 0))]
    print('%d separated end states to merge' % len(src), flush=True)
    out = []
    with Pool(a.procs) as pool:
        for m in pool.imap_unordered(merge_one, src):
            out.append(m)
            print('%s I=%d mN=%g %s rep %d: clean %s share %.3f -> %s, %s in %d gens' % (
                m['exp'], m['I'], m['mN'], m['preset'], m['rep'], m['clean'], m['share_larger'], m['winners'][:2],
                'larger won' if m['larger_won'] else ('MINORITY WON' if m['minority_won'] else 'mixed'), m['gens_to_freeze']), flush=True)
    import gzip
    json.dump(out, gzip.open(os.path.join(RUNS, 'rival-islands-merge.json.gz'), 'wt'))


# ------------------------------------------------------------------ static (item 1)
def fix_k(N, w, k, uqq=0.0, uqa=-1.0, uaq=-1.0, uaa=0.0):
    """P(k copies of q reach N before 0) against resident a (Moran, exp fitness)."""
    logs = np.zeros(N)
    acc = 0.0
    for j in range(1, N):
        pq = (j - 1) / (N - 1) * uqq + (N - j) / (N - 1) * uqa
        pa = j / (N - 1) * uaq + (N - j - 1) / (N - 1) * uaa
        acc += w * (pa - pq); logs[j] = acc
    lm = logs.max()
    s = np.exp(logs - lm)
    return float(s[:k].sum() / s.sum())


def static_main(a):
    from compatibility import coseed
    out = {}
    out['rho'] = {str(N): dict(dd_migrant=fixation(0, -1, -1, 0, N, W, N), D_into_FairBot=fixation(-1, -1, -1, 0, N, W, N),
                               est_into_D=fixation(0, -1, -1, -1, N, W, N),
                               dd_k={str(k): fix_k(N, W, k) for k in (1, 2, 5, 10, 20, 30, 40)})
                  for N in (100, 200, 400)}
    for n in (9, 12):
        d = cls(n); V = d['V']; mu = d['mu']; nm = d['names']
        E = np.nonzero(d['est'])[0]
        Ve = np.asarray(V[np.ix_(E, E)]).astype(bool)
        DD = ~Ve & ~Ve.T; np.fill_diagonal(DD, False)
        iu = np.argwhere(np.triu(DD, 1)); pm = mu[E[iu[:, 0]]] * mu[E[iu[:, 1]]]
        top = np.argsort(-pm)[:20]
        rows = []
        for k in top:
            x, y = E[iu[k]]
            if mu[x] < mu[y]: x, y = y, x
            rows.append(dict(x=nm[x], y=nm[y], mu_x=float(mu[x]), mu_y=float(mu[y]), prod=float(mu[x] * mu[y]),
                             co100=coseed(mu[x], mu[y], 100), co400=coseed(mu[x], mu[y], 400)))
        # mass of all establishers that mutually defect with the FairBot pair (rivals) and expected seeds per run
        refs = [d['idx']['BOX(THEM(ME))'], d['idx']['BOX1(THEM(ME))']]
        rv = np.zeros(len(mu), bool)
        for ref in refs:
            rv |= (np.asarray(V[:, ref]) == 0) & (np.asarray(V[ref, :]) == 0)
        rv &= d['coop']
        rv_est = rv & d['est']
        out[str(n)] = dict(n_dd_pairs=int(len(iu)), dd_pair_mass=float(pm.sum()), top_pairs=rows,
                           mu_rival_coop=float(mu[rv].sum()), mu_rival_est=float(mu[rv_est].sum()), n_rival_est=int(rv_est.sum()),
                           rival_seeds_per_run={str(I): float(I * 100 * mu[rv_est].sum()) for I in (64, 256, 1024)},
                           top_rivals=[(nm[k], float(mu[k])) for k in np.argsort(-np.where(rv_est, mu, 0))[:10]])
        if n == 9:
            heavy = [k for k in range(len(mu)) if mu[k] >= 1e-4]
            pairs = []
            for p, (an, bn) in enumerate(PAIRS):
                A = d['idx'][an]; B = d['idx'][bn]
                sup = np.array(sorted(set(heavy) | {A, B}))
                tg = tags_for(d, sup, A, B)
                allsup = np.arange(len(mu)); tga = tags_for(d, allsup, A, B)
                rel = []
                for k in sup:
                    rel.append(dict(name=nm[k], mu=float(mu[k]), tag=int(tg[list(sup).index(k)]),
                                    k_vs_A=int(V[k, A]), A_vs_k=int(V[A, k]), k_vs_B=int(V[k, B]), B_vs_k=int(V[B, k])))
                pairs.append(dict(A=an, B=bn, mu_A=float(mu[A]), mu_B=float(mu[B]), co100=coseed(mu[A], mu[B], 100),
                                  net_mass={str(t): float(mu[tga == t].sum()) for t in range(4)},
                                  net_est_mass={str(t): float(mu[(tga == t) & d['est']].sum()) for t in range(4)},
                                  B_fakers_mass=float(mu[(np.asarray(V[:, B]) == 0) & (np.asarray(V[B, :]) == 1)].sum()),
                                  A_fakers_mass=float(mu[(np.asarray(V[:, A]) == 0) & (np.asarray(V[A, :]) == 1)].sum()),
                                  heavy_relations=rel))
            out['pairs'] = pairs
    json.dump(out, open(os.path.join(RUNS, 'rival-islands-static.json'), 'w'), indent=1)
    for N, v in out['rho'].items():
        print('N=%s: rho_DD %.3g, rho(D|FB) %.3g, rho(est|D) %.4f; k-copy %s' % (N, v['dd_migrant'], v['D_into_FairBot'], v['est_into_D'],
              {k: '%.3g' % x for k, x in v['dd_k'].items()}))
    for n in ('9', '12'):
        v = out[n]
        print('n=%s: %d DD pairs mass %.3g; rival est mass %.3g (%d classes); rival seeds per run %s' % (
            n, v['n_dd_pairs'], v['dd_pair_mass'], v['mu_rival_est'], v['n_rival_est'], v['rival_seeds_per_run']))
        for p in v['top_pairs'][:6]:
            print('   %s x %s  %.3g %.3g co100 %.2e' % (p['x'], p['y'], p['mu_x'], p['mu_y'], p['co100']))
    for p in out['pairs']:
        print(p['A'], 'x', p['B'], 'net mass', {k: '%.3g' % v for k, v in p['net_mass'].items()}, 'fakers of B %.3g, of A %.3g' % (p['B_fakers_mass'], p['A_fakers_mass']))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['static', 'run', 'merge', 'report'])
    ap.add_argument('--exp', default='sep')
    ap.add_argument('--procs', type=int, default=3)
    ap.add_argument('--gens', type=int, default=GENS)
    a = ap.parse_args()
    if a.what == 'static': static_main(a)
    elif a.what == 'run': run_main(a)
    elif a.what == 'merge': merge_main(a)
    elif a.what == 'report':
        import rival_islands_report as RR
        RR.main()
