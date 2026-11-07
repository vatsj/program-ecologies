"""The island kernel for majority division with an annealed tail (spec specs/2026-11-07-majority-current-object.md).

kern_mt is src/pair_worth_kern.kern_pw with its records changed to what the majority experiment measures; the stream
of random numbers is untouched, so with no arrivals it is draw for draw migration_window_kernels.kern_mw (checked by
validation V1 and tests/test_majority_tail.py).  Differences from kern_pw:

  - per generation and island it records the modal outcome (argmax of the encounter distribution, kern_mw's `modal`)
    and the outcome of the three modal programs (`majo`); nothing else per generation;
  - at the generations listed in snapg it copies the full counts array and the encounter-weighted outcome
    distribution of every island (snapc, snapd), so snapshots are observational and cost no random draws;
  - the crossing log fires when a program first holds more than N/2 of a slot on an island (kern_pw: 10%), with the
    flag of whether the program's current presence on that island began with an arrival (`arrf`) and the generation
    it began (`intro`).  The program-level flag is the fallback for lineage tagging allowed by the spec ("if tagging
    is infeasible in the kernel report genotype-frequency crossings"): copies of a program already present, or
    arriving later, are not credited to a later arrival, but a presence episode that began with an arrival and
    spread by reproduction or migration is credited to the arrival that began it;
  - the arrival log records (generation, island, slot, program, victim program, applied).

Importable without side effects.
"""
import numpy as np
from numba import njit
from stable_sets import _fit_full, _setact, _parent, _closed, _code, _others
from pair_worth_kern import _apply_arrival


@njit(cache=True)
def _rec(J, VEC, ISMEM, TOT, counts, pres, npres, i, N, dist, nout, g, modal, majo, effm):
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
    mx = -1.0; arg = 0
    for z in range(nout):
        if dist[z] > mx:
            mx = dist[z]; arg = z
    modal[g, i] = arg
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


@njit(cache=True)
def kern_mt(J, PAY, VEC, ISMEM, TOT, init, N, w, m, seed, H, close_every, snapg,
            arr_g, arr_i, arr_s, arr_u, arr_k, xcap, acap):
    np.random.seed(seed)
    I = init.shape[0]; K = init.shape[2]
    nout = ISMEM.shape[0]
    counts = init.copy()
    pres = np.zeros((I, 3, K), np.int64); npres = np.zeros((I, 3), np.int64); pos = -np.ones((I, 3, K), np.int64)
    glob = np.zeros((3, K), np.int64)
    F = np.zeros((I, 3, K))
    intro = np.full((I, 3, K), -2, np.int64)
    t10 = np.full((I, 3, K), -1, np.int64)       # first generation above N/2 (name kept for _apply_arrival)
    arrf = np.zeros((I, 3, K), np.int64)
    for i in range(I):
        for s in range(3):
            for k in range(K):
                if counts[i, s, k] > 0:
                    pres[i, s, npres[i, s]] = k; pos[i, s, k] = npres[i, s]; npres[i, s] += 1
                    glob[s, k] += counts[i, s, k]
                    intro[i, s, k] = -1
                    if counts[i, s, k] * 2 > N:
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
    modal = np.zeros((H + 1, I), np.int16); majo = np.zeros((H + 1, I), np.int16)
    effm = np.zeros((1, 1), np.float32)
    nsnap = snapg.shape[0]
    snapc = np.zeros((nsnap, I, 3, K), np.int32)
    snapd = np.zeros((nsnap, I, nout))
    dist = np.zeros(nout)
    xlog = np.zeros((xcap, 6), np.int64); nx = 0
    alog = np.zeros((acap, 6), np.int64); na = 0
    narr = arr_g.shape[0]; ai = 0
    N2 = float(N) * N
    UN = NU * N
    mm = m if I > 1 else 0.0
    for i in range(I):
        _rec(J, VEC, ISMEM, TOT, counts, pres, npres, i, N, dist, nout, 0, modal, majo, effm)
    si = 0
    while si < nsnap and snapg[si] <= 0:
        for i in range(I):
            for s in range(3):
                for k in range(K):
                    snapc[si, i, s, k] = counts[i, s, k]
            for z in range(nout):
                snapd[si, i, z] = 0.0
            for ta in range(npres[i, 0]):
                a = pres[i, 0, ta]
                for tb in range(npres[i, 1]):
                    b = pres[i, 1, tb]
                    for tc in range(npres[i, 2]):
                        c = pres[i, 2, tc]
                        snapd[si, i, VEC[J[a, b, c]]] += counts[i, 0, a] * counts[i, 1, b] * counts[i, 2, c] / (float(N) * N * N)
        si += 1
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
                _rec(J, VEC, ISMEM, TOT, counts, pres, npres, i, N, dist, nout, g, modal, majo, effm)
                for s in range(3):
                    for t in range(npres[i, s]):
                        k = pres[i, s, t]
                        if t10[i, s, k] < 0 and counts[i, s, k] * 2 > N:
                            t10[i, s, k] = g
                            if nx < xcap:
                                xlog[nx, 0] = g; xlog[nx, 1] = i; xlog[nx, 2] = s; xlog[nx, 3] = k
                                xlog[nx, 4] = arrf[i, s, k]; xlog[nx, 5] = intro[i, s, k]
                                nx += 1
            while si < nsnap and snapg[si] <= g:
                for i in range(I):
                    for s in range(3):
                        for k in range(K):
                            snapc[si, i, s, k] = counts[i, s, k]
                    for z in range(nout):
                        snapd[si, i, z] = 0.0
                    for ta in range(npres[i, 0]):
                        a = pres[i, 0, ta]
                        for tb in range(npres[i, 1]):
                            b2 = pres[i, 1, tb]
                            for tc in range(npres[i, 2]):
                                c = pres[i, 2, tc]
                                snapd[si, i, VEC[J[a, b2, c]]] += counts[i, 0, a] * counts[i, 1, b2] * counts[i, 2, c] / (float(N) * N * N)
                si += 1
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
    # after a closure stop the state is frozen: copy it forward
    for gg in range(stop_gen + 1, H + 1):
        for i in range(I):
            modal[gg, i] = modal[stop_gen, i]; majo[gg, i] = majo[stop_gen, i]
    while si < nsnap:
        for i in range(I):
            for s in range(3):
                for k in range(K):
                    snapc[si, i, s, k] = counts[i, s, k]
            for z in range(nout):
                snapd[si, i, z] = 0.0
            for ta in range(npres[i, 0]):
                a = pres[i, 0, ta]
                for tb in range(npres[i, 1]):
                    b2 = pres[i, 1, tb]
                    for tc in range(npres[i, 2]):
                        c = pres[i, 2, tc]
                        snapd[si, i, VEC[J[a, b2, c]]] += counts[i, 0, a] * counts[i, 1, b2] * counts[i, 2, c] / (float(N) * N * N)
        si += 1
    return (status, stop_gen, counts, modal, majo, snapc, snapd, xlog[:min(nx, xcap)], nx, alog[:min(na, acap)], na, nmig)
