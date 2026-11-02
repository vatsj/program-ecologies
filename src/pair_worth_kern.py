"""The island kernel with an annealed tail (notes/pair-worth.md 1.7).

kern_pw is a copy of migration_window_kernels.kern_mw (itself generated from stable_sets.kern; both unedited here) with

  - an arrival schedule (arr_g, arr_i, arr_s, arr_u, arr_k): at the boundary that opens generation g, every arrival
    scheduled for g replaces one individual of slot arr_s on island arr_i (the victim found from the uniform arr_u by
    the slot's cumulative counts) by program arr_k of the run's universe.  Arrivals consume nothing of the kernel's
    random stream, so with no arrivals kern_pw is draw-for-draw kern_mw;
  - no closure stop while arrivals are pending;
  - per-generation, per-island records: modal outcome (kern_mw's `modal`), the majority-triple outcome, the top
    outcome probability, efficiency sum(dist * total payoff), the exact encounter-weighted class distribution under
    two class tables (concatenated), mean payoff per slot, a bitmask of the named families present, a crossing log
    (first generation a program reaches 10% of a slot) and an arrival log.

Importable without side effects.
"""
import numpy as np
from numba import njit
import stable_sets as SS
from stable_sets import _fit_full, _setact, _parent, _closed, _code, _others


@njit(cache=True)
def _record(J, PAY, VEC, ISMEM, TOT, OPAY, CLA, CLB, nA, FAM, counts, pres, npres, i, N, dist, nout, g,
            cls, modal, majo, ptop, effm, cd, payr, famr, famc):
    for z in range(nout):
        dist[z] = 0.0
    N3 = float(N) * N * N
    for ta in range(npres[i, 0]):
        a = pres[i, 0, ta]
        for tb in range(npres[i, 1]):
            b = pres[i, 1, tb]
            for tc in range(npres[i, 2]):
                c = pres[i, 2, tc]
                dist[VEC[J[a, b, c]]] += counts[i, 0, a] * counts[i, 1, b] * counts[i, 2, c] / N3
    mx = -1.0; arg = 0; mem = 0.0; eff = 0.0
    for z in range(nout):
        if dist[z] > mx:
            mx = dist[z]; arg = z
        if ISMEM[z]:
            mem += dist[z]
        eff += dist[z] * TOT[z]
    if mx >= 0.95:
        cls[g, i] = arg
    elif mem >= 0.95:
        cls[g, i] = nout
    else:
        cls[g, i] = nout + 1
    modal[g, i] = arg; ptop[g, i] = mx; effm[g, i] = eff
    for z in range(nout):
        d = dist[z]
        if d > 0.0:
            cd[g, i, CLA[z]] += d
            cd[g, i, nA + CLB[z]] += d
            for s in range(3):
                payr[g, i, s] += d * OPAY[z, s]
    # majority triple
    mj0 = 0; mj1 = 0; mj2 = 0
    best = -1
    for t in range(npres[i, 0]):
        k = pres[i, 0, t]
        if counts[i, 0, k] > best:
            best = counts[i, 0, k]; mj0 = k
    best = -1
    for t in range(npres[i, 1]):
        k = pres[i, 1, t]
        if counts[i, 1, k] > best:
            best = counts[i, 1, k]; mj1 = k
    best = -1
    for t in range(npres[i, 2]):
        k = pres[i, 2, t]
        if counts[i, 2, k] > best:
            best = counts[i, 2, k]; mj2 = k
    majo[g, i] = VEC[J[mj0, mj1, mj2]]
    bits = 0
    for s in range(3):
        for f in range(5):
            famc[f] = 0
        for t in range(npres[i, s]):
            k = pres[i, s, t]
            famc[FAM[s, k]] += counts[i, s, k]
        for f in range(1, 5):
            if famc[f] >= 1:
                bits |= 1 << (s * 8 + (f - 1) * 2)
            if famc[f] * 10 >= N:
                bits |= 1 << (s * 8 + (f - 1) * 2 + 1)
    famr[g, i] = bits


@njit(cache=True)
def _apply_arrival(J, PAY, F, counts, pres, npres, pos, glob, intro, t10, arrf, i, s, vu, child, g, N, act, apos, nact):
    """one arrival: replace the victim (from the uniform vu) of slot s on island i by `child`.  Returns (nact,
    victim, applied)."""
    r = int(vu * N)
    if r >= N:
        r = N - 1
    acc = 0; victim = pres[i, s, 0]
    for t in range(npres[i, s]):
        k = pres[i, s, t]; acc += counts[i, s, k]
        if r < acc:
            victim = k; break
    if victim == child:
        return nact, victim, 0
    counts[i, s, victim] -= 1; glob[s, victim] -= 1
    if counts[i, s, victim] == 0:
        p = pos[i, s, victim]; last = pres[i, s, npres[i, s] - 1]
        pres[i, s, p] = last; pos[i, s, last] = p; pos[i, s, victim] = -1; npres[i, s] -= 1
        intro[i, s, victim] = -2; t10[i, s, victim] = -1; arrf[i, s, victim] = 0
    new = counts[i, s, child] == 0
    if new:
        pres[i, s, npres[i, s]] = child; pos[i, s, child] = npres[i, s]; npres[i, s] += 1
        intro[i, s, child] = g; arrf[i, s, child] = 1
    counts[i, s, child] += 1; glob[s, child] += 1
    o1, o2 = _others(s)
    for sa in (o1, o2):
        sb = o1 + o2 - sa
        for ta in range(npres[i, sa]):
            k = pres[i, sa, ta]
            v = 0.0
            for tb in range(npres[i, sb]):
                q = pres[i, sb, tb]
                if s < sb:
                    v += counts[i, sb, q] * (PAY[_code(J, sa, k, child, q), sa] - PAY[_code(J, sa, k, victim, q), sa])
                else:
                    v += counts[i, sb, q] * (PAY[_code(J, sa, k, q, child), sa] - PAY[_code(J, sa, k, q, victim), sa])
            F[i, sa, k] += v
    if new:
        F[i, s, child] = _fit_full(J, PAY, counts, pres, npres, i, s, child)
    nact = _setact(i * 3 + s, npres[i, s] > 1, act, apos, nact)
    return nact, victim, 1


@njit(cache=True)
def kern_pw(J, PAY, VEC, ISMEM, TOT, OPAY, CLA, CLB, nA, nB, FAM, init, N, w, m, seed, H, close_every,
            arr_g, arr_i, arr_s, arr_u, arr_k, xcap, acap):
    np.random.seed(seed)
    I = init.shape[0]; K = init.shape[2]
    nout = ISMEM.shape[0]
    counts = init.copy()
    pres = np.zeros((I, 3, K), np.int64); npres = np.zeros((I, 3), np.int64); pos = -np.ones((I, 3, K), np.int64)
    glob = np.zeros((3, K), np.int64)
    F = np.zeros((I, 3, K))
    intro = np.full((I, 3, K), -2, np.int64)
    t10 = np.full((I, 3, K), -1, np.int64)
    arrf = np.zeros((I, 3, K), np.int64)
    for i in range(I):
        for s in range(3):
            for k in range(K):
                if counts[i, s, k] > 0:
                    pres[i, s, npres[i, s]] = k; pos[i, s, k] = npres[i, s]; npres[i, s] += 1
                    glob[s, k] += counts[i, s, k]
                    intro[i, s, k] = -1
                    if counts[i, s, k] * 10 >= N:
                        t10[i, s, k] = 0
    for i in range(I):
        for s in range(3):
            for t in range(npres[i, s]):
                k = pres[i, s, t]
                F[i, s, k] = _fit_full(J, PAY, counts, pres, npres, i, s, k)
    NU = 3 * I
    act = np.arange(NU); apos = np.arange(NU); nact = 0
    for u in range(NU):
        if npres[u // 3, u % 3] > 1:
            nact = _setact(u, True, act, apos, nact)
    nc = nA + nB
    cls = np.zeros((H + 1, I), np.int16)
    modal = np.zeros((H + 1, I), np.int16); majo = np.zeros((H + 1, I), np.int16)
    ptop = np.zeros((H + 1, I), np.float32); effm = np.zeros((H + 1, I), np.float32)
    cd = np.zeros((H + 1, I, nc), np.float32); payr = np.zeros((H + 1, I, 3), np.float32)
    famr = np.zeros((H + 1, I), np.int32)
    famc = np.zeros(5, np.int64)
    dist = np.zeros(nout)
    xlog = np.zeros((xcap, 6), np.int64); nx = 0
    alog = np.zeros((acap, 7), np.int64); na = 0
    narr = arr_g.shape[0]; ai = 0
    N2 = float(N) * N
    UN = NU * N
    mm = m if I > 1 else 0.0
    for i in range(I):
        _record(J, PAY, VEC, ISMEM, TOT, OPAY, CLA, CLB, nA, FAM, counts, pres, npres, i, N, dist, nout, 0,
                cls, modal, majo, ptop, effm, cd, payr, famr, famc)
    b = 0
    g = 0
    nextchk = UN
    status = 4; stop_gen = H
    nmig = 0
    total = H * UN
    cls0 = np.zeros(K, np.int64); cls1 = np.zeros(K, np.int64); cls2 = np.zeros(K, np.int64)
    while ai < narr and arr_g[ai] <= 0:
        i = arr_i[ai]; s = arr_s[ai]
        nact, vk, ap = _apply_arrival(J, PAY, F, counts, pres, npres, pos, glob, intro, t10, arrf, i, s, arr_u[ai],
                                      arr_k[ai], 0, N, act, apos, nact)
        if na < acap:
            alog[na, 0] = 0; alog[na, 1] = i; alog[na, 2] = s; alog[na, 3] = arr_k[ai]; alog[na, 4] = vk
            alog[na, 5] = ap; na += 1
        ai += 1
    while True:
        pa = (nact + (NU - nact) * mm) / NU
        if pa <= 0.0:
            G = total + 1
        elif pa >= 1.0:
            G = 0
        else:
            uu = np.random.random()
            G = int(np.log(1.0 - uu) / np.log(1.0 - pa))
        if b + G >= nextchk:
            b = nextchk
            g += 1
            for i in range(I):
                _record(J, PAY, VEC, ISMEM, TOT, OPAY, CLA, CLB, nA, FAM, counts, pres, npres, i, N, dist, nout, g,
                        cls, modal, majo, ptop, effm, cd, payr, famr, famc)
                for s in range(3):
                    for t in range(npres[i, s]):
                        k = pres[i, s, t]
                        if t10[i, s, k] < 0 and counts[i, s, k] * 10 >= N:
                            t10[i, s, k] = g
                            if nx < xcap:
                                xlog[nx, 0] = g; xlog[nx, 1] = i; xlog[nx, 2] = s; xlog[nx, 3] = k
                                xlog[nx, 4] = arrf[i, s, k]; xlog[nx, 5] = intro[i, s, k]
                                nx += 1
            while ai < narr and arr_g[ai] <= g:
                i = arr_i[ai]; s = arr_s[ai]
                nact, vk, ap = _apply_arrival(J, PAY, F, counts, pres, npres, pos, glob, intro, t10, arrf, i, s,
                                              arr_u[ai], arr_k[ai], g, N, act, apos, nact)
                if na < acap:
                    alog[na, 0] = g; alog[na, 1] = i; alog[na, 2] = s; alog[na, 3] = arr_k[ai]; alog[na, 4] = vk
                    alog[na, 5] = ap; na += 1
                ai += 1
            done = False
            if (g % close_every == 0 or g == H) and ai >= narr:
                if mm > 0.0:
                    n0 = 0; n1 = 0; n2 = 0
                    for k in range(K):
                        if glob[0, k] > 0:
                            cls0[n0] = k; n0 += 1
                        if glob[1, k] > 0:
                            cls1[n1] = k; n1 += 1
                        if glob[2, k] > 0:
                            cls2[n2] = k; n2 += 1
                    if _closed(J, cls0, n0, cls1, n1, cls2, n2):
                        status = 1; stop_gen = g; done = True
                else:
                    allc = True
                    for i in range(I):
                        if not _closed(J, pres[i, 0], npres[i, 0], pres[i, 1], npres[i, 1], pres[i, 2], npres[i, 2]):
                            allc = False; break
                    if allc:
                        status = 5; stop_gen = g; done = True
            if done or g >= H:
                break
            nextchk = (g + 1) * UN
            continue
        b = b + G + 1
        if np.random.random() * pa * NU < nact:
            u = act[np.random.randint(nact)]
            mig = mm > 0.0 and np.random.random() < mm
        else:
            u = act[nact + np.random.randint(NU - nact)]
            mig = True
        i = u // 3; s = u % 3
        src = i
        if mig:
            src = np.random.randint(I - 1)
            if src >= i: src += 1
            nmig += 1
        child = _parent(F, counts, pres, npres, src, s, N2, w)
        r = np.random.randint(N); acc = 0; victim = pres[i, s, 0]
        for t in range(npres[i, s]):
            k = pres[i, s, t]; acc += counts[i, s, k]
            if r < acc:
                victim = k; break
        if victim == child:
            continue
        counts[i, s, victim] -= 1; glob[s, victim] -= 1
        if counts[i, s, victim] == 0:
            p = pos[i, s, victim]; last = pres[i, s, npres[i, s] - 1]
            pres[i, s, p] = last; pos[i, s, last] = p; pos[i, s, victim] = -1; npres[i, s] -= 1
            intro[i, s, victim] = -2; t10[i, s, victim] = -1; arrf[i, s, victim] = 0
        new = counts[i, s, child] == 0
        if new:
            pres[i, s, npres[i, s]] = child; pos[i, s, child] = npres[i, s]; npres[i, s] += 1
            intro[i, s, child] = g + 1; arrf[i, s, child] = 0
        counts[i, s, child] += 1; glob[s, child] += 1
        o1, o2 = _others(s)
        for sa in (o1, o2):
            sb = o1 + o2 - sa
            for ta in range(npres[i, sa]):
                k = pres[i, sa, ta]
                v = 0.0
                for tb in range(npres[i, sb]):
                    q = pres[i, sb, tb]
                    if s < sb:
                        v += counts[i, sb, q] * (PAY[_code(J, sa, k, child, q), sa] - PAY[_code(J, sa, k, victim, q), sa])
                    else:
                        v += counts[i, sb, q] * (PAY[_code(J, sa, k, q, child), sa] - PAY[_code(J, sa, k, q, victim), sa])
                F[i, sa, k] += v
        if new:
            F[i, s, child] = _fit_full(J, PAY, counts, pres, npres, i, s, child)
        nact = _setact(u, npres[i, s] > 1, act, apos, nact)
    for gg in range(stop_gen + 1, H + 1):
        for i in range(I):
            cls[gg, i] = cls[stop_gen, i]; modal[gg, i] = modal[stop_gen, i]; majo[gg, i] = majo[stop_gen, i]
            ptop[gg, i] = ptop[stop_gen, i]; effm[gg, i] = effm[stop_gen, i]; famr[gg, i] = famr[stop_gen, i]
            for c in range(nc):
                cd[gg, i, c] = cd[stop_gen, i, c]
            for s in range(3):
                payr[gg, i, s] = payr[stop_gen, i, s]
    return (status, stop_gen, counts, cls, modal, majo, ptop, effm, cd, payr, famr, xlog[:min(nx, xcap)], nx,
            alog[:min(na, acap)], na, nmig)
