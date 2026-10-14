"""Dominance contracts and refusal on islands (spec specs/2026-10-14-dominance-contracts.md, reviewed by gpt-6.1-sol
and gemini-4-argon; notes notes/dominance-contracts.md; predictions predictions/2026-10-14-dominance-contracts.md).

Imports the stable-sets machinery (src/stable_sets.py) and does not edit it.

Static part: the 27 pair contracts on dollar3, the exact proposal generator on the realizable outcomes R and its
stationary distribution, the uniform-successor walk (the spec's 0.235 anchor), the walk with refusal at V*, and the
coordination thresholds beta*_static and beta*_flow of every dominating edge under the kernel's fitness map.

Dynamic part: the eps = 0 island lottery of stable_sets.kern with individual genotypes (program k, installed override o,
refusal bit r, carried contract c), play classes (k, or the override's constant action), and contract events at
generation boundaries (rate nu per island per generation; menu F or G; proposal against slot-mean payoffs; consent
none / public / private / blind; installation of a fraction beta in place).  With nu = 0 and one type per program the
kernel consumes the same random numbers as stable_sets.kern and reproduces it draw for draw.
"""
import itertools, os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numba import njit
import stable_sets as SS
import dollar3 as D

ROOT = SS.ROOT
W = SS.W
PAIRS = SS.PAIRS
NCON = 27
NKEY_O = 10       # override: none + 9 actions
NKEY_C = 28       # carried contract: none + 27


# ====================================================================== contracts
def contracts():
    """list of (S, d0, d1) in sixths, index = 9 * pair + 3 * (d0 - 2) + (d1 - 2)."""
    out = []
    for S in PAIRS:
        for d0 in (2, 3, 4):
            for d1 in (2, 3, 4):
                out.append((S, d0, d1))
    return out


CONTRACTS = contracts()


def contract_arrays():
    CS = np.zeros((NCON, 2), np.int64); CD = np.zeros((NCON, 2), np.int64); CACT = np.zeros((NCON, 2), np.int64)
    for k, (S, d0, d1) in enumerate(CONTRACTS):
        CS[k] = S; CD[k] = (d0, d1)
        CACT[k, 0] = D.local_of(S[0], S[1], d0 - 2)
        CACT[k, 1] = D.local_of(S[1], S[0], d1 - 2)
    return CS, CD, CACT


def contract_label(k):
    S, d0, d1 = CONTRACTS[k]
    return '{%d,%d}:%d|%d' % (S[0] + 1, S[1] + 1, d0, d1)


def contract_x(k):
    S, d0, d1 = CONTRACTS[k]
    x = [0, 0, 0]; x[S[0]] = d0; x[S[1]] = d1
    return tuple(x)


def proposed(k, y):
    """the proposal rule on payoff vectors (sixths): both members of S strictly better at x than at y."""
    S, d0, d1 = CONTRACTS[k]
    if d0 + d1 > 6:
        return False
    return d0 > y[S[0]] and d1 > y[S[1]]


# ====================================================================== static: walks on R
def generator(X):
    """exact proposal generator: Q[y, x] = (number of contracts proposed at y leading to x) / 27, null draws on the
    diagonal; also n(y) and the multiplicity table."""
    idx = {x: k for k, x in enumerate(X)}
    n = len(X)
    Q = np.zeros((n, n)); nprop = np.zeros(n, np.int64); mult = np.zeros((n, n), np.int64)
    for y in range(n):
        for k in range(NCON):
            if proposed(k, X[y]):
                x = idx[contract_x(k)]
                Q[y, x] += 1.0 / NCON; nprop[y] += 1; mult[y, x] += 1
        Q[y, y] = 1.0 - Q[y].sum()
    return Q, nprop, mult


def stationary(P):
    w, v = np.linalg.eig(P.T)
    k = int(np.argmin(np.abs(w - 1)))
    p = np.real(v[:, k])
    return p / p.sum()


def uniform_successor(X, M):
    n = len(X)
    P = np.zeros((n, n))
    for y in range(n):
        d = np.nonzero(M[:, y])[0]
        P[y, d] = 1.0 / len(d)
    return P


def hitting_times(Q, target):
    n = Q.shape[0]
    T = [k for k in range(n) if k not in target]
    A = np.eye(len(T)) - Q[np.ix_(T, T)]
    h = np.linalg.solve(A, np.ones(len(T)))
    return dict(zip(T, h))


def same_member_return(Q, V):
    n = Q.shape[0]; V = sorted(V)
    T = [k for k in range(n) if k not in V]
    A = np.eye(len(T)) - Q[np.ix_(T, T)]
    H = np.linalg.solve(A, Q[np.ix_(T, V)])
    out = {}
    for a, m in enumerate(V):
        row = Q[m].copy(); row[m] = 0; row /= row.sum()
        p = np.zeros(len(V))
        for j, t in enumerate(T):
            p += row[t] * H[j]
        out[m] = p[a]
    return out


# ====================================================================== static: coordination thresholds
def _fits(pay, a, S, c, p):
    """expected payoff (sixths) of installed (action c[s]) and resident (a[s]) individuals of each S slot, installed
    fractions p[s]; the complement is fixed at a."""
    out = {}
    for s in S:
        o = [t for t in range(3) if t != s]
        res = {}
        for mine in (0, 1):
            v = 0.0
            for t1 in (0, 1):
                for t2 in (0, 1):
                    prof = [0, 0, 0]; prof[s] = c[s] if mine else a[s]
                    wt = 1.0
                    for t, tt in ((o[0], t1), (o[1], t2)):
                        if t in S:
                            prof[t] = c[t] if tt else a[t]
                            wt *= p[t] if tt else 1 - p[t]
                        else:
                            prof[t] = a[t]
                            wt *= 0.0 if tt else 1.0
                    if wt:
                        v += wt * pay[tuple(prof)][s]
            res[mine] = v
        out[s] = res
    return out


def _flow_reaches(pay, a, S, c, beta, w=W, T=6000, dt=0.5):
    p = {S[0]: beta, S[1]: beta}
    reached = lambda: all(p[s] > 0.999 or a[s] == c[s] for s in S)
    for _ in range(int(T / dt)):
        f = _fits(pay, a, S, c, p)
        for s in S:
            d = (f[s][1] - f[s][0]) / 6.0
            p[s] = min(max(p[s] + dt * w * p[s] * (1 - p[s]) * d, 0.0), 1.0)
        if reached():
            return True
        if any(p[s] < 1e-3 and a[s] != c[s] for s in S):
            return False
    return reached()


def thresholds(pay, a, k):
    """(beta*_static, beta*_flow) for contract k installed at the constant profile a; None = never on [0, 1]."""
    S, d0, d1 = CONTRACTS[k]
    CS, CD, CACT = contract_arrays()
    c = {S[0]: int(CACT[k, 0]), S[1]: int(CACT[k, 1])}
    bst = None
    for b in np.arange(0.0, 1.0001, 0.01):
        f = _fits(pay, a, S, c, {S[0]: b, S[1]: b})
        if all(f[s][1] > f[s][0] + 1e-12 for s in S):
            bst = round(float(b), 2); break
    if _flow_reaches(pay, a, S, c, 0.001):
        bfl = 0.0
    elif not _flow_reaches(pay, a, S, c, 0.999):
        bfl = None
    else:
        lo, hi = 0.0, 1.0
        for _ in range(14):
            m = (lo + hi) / 2
            if _flow_reaches(pay, a, S, c, m): hi = m
            else: lo = m
        bfl = hi
    return bst, bfl


# ====================================================================== the kernel
@njit(cache=True)
def _typeid(s, k, o, r, c, Kmax, TK, TO, TR, TC, TPC, TMAP, ntypes):
    key = ((k * 10 + (o + 1)) * 2 + r) * 28 + (c + 1)
    t = TMAP[s, key]
    if t >= 0:
        return t
    t = ntypes[s]
    if t >= TK.shape[1]:
        return -1
    TMAP[s, key] = t
    TK[s, t] = k; TO[s, t] = o; TR[s, t] = r; TC[s, t] = c
    TPC[s, t] = k if o < 0 else Kmax + o
    ntypes[s] = t + 1
    return t


@njit(cache=True)
def _tadd(i, s, t, n, tcount, tpres, tnpres, tpos):
    if n == 0:
        return
    if tcount[i, s, t] == 0:
        tpres[i, s, tnpres[i, s]] = t; tpos[i, s, t] = tnpres[i, s]; tnpres[i, s] += 1
    tcount[i, s, t] += n


@njit(cache=True)
def _tsub(i, s, t, n, tcount, tpres, tnpres, tpos):
    if n == 0:
        return
    tcount[i, s, t] -= n
    if tcount[i, s, t] == 0:
        p = tpos[i, s, t]; last = tpres[i, s, tnpres[i, s] - 1]
        tpres[i, s, p] = last; tpos[i, s, last] = p; tpos[i, s, t] = -1; tnpres[i, s] -= 1


@njit(cache=True)
def _padd(i, s, pc, n, pcount, ppres, pnpres, ppos, glob, introg, introc, g, cause):
    if n == 0:
        return
    if pcount[i, s, pc] == 0:
        ppres[i, s, pnpres[i, s]] = pc; ppos[i, s, pc] = pnpres[i, s]; pnpres[i, s] += 1
        introg[i, s, pc] = g; introc[i, s, pc] = cause
    pcount[i, s, pc] += n; glob[s, pc] += n


@njit(cache=True)
def _psub(i, s, pc, n, pcount, ppres, pnpres, ppos, glob, introg):
    if n == 0:
        return
    pcount[i, s, pc] -= n; glob[s, pc] -= n
    if pcount[i, s, pc] == 0:
        p = ppos[i, s, pc]; last = ppres[i, s, pnpres[i, s] - 1]
        ppres[i, s, p] = last; ppos[i, s, last] = p; ppos[i, s, pc] = -1; pnpres[i, s] -= 1
        introg[i, s, pc] = -2


@njit(cache=True)
def _slot_mean(Fp, pcount, ppres, pnpres, i, s, N, N2):
    v = 0.0
    for t in range(pnpres[i, s]):
        pc = ppres[i, s, t]
        v += pcount[i, s, pc] * Fp[i, s, pc]
    return v / (N * N2)


@njit(cache=True)
def _nplay(pcount, ppres, pnpres, PCACT, i, s, a):
    n = 0
    for t in range(pnpres[i, s]):
        pc = ppres[i, s, t]
        if PCACT[s, pc] == a:
            n += pcount[i, s, pc]
    return n


@njit(cache=True)
def dkern(J, PAY, VEC, ISMEM, TOT, PCACT, tcount0, TK, TO, TR, TC, TPC, TMAP, ntypes, Kmax, N, w, m, seed, H,
          close_every, hrec, nu, menu_g, binst, consent, CS, CD, CACT, stop_closed, rec_every, evcap, cevcap, pendcap):
    """eps = 0 island lottery with genotypes and contract events.  Births, migration, classification and closure as
    stable_sets.kern (types = genotypes; fitness by play class).  At each generation boundary, after classification,
    each island has a contract event with probability nu (no random number is drawn when nu = 0).
    consent: 0 none, 1 public (one drawn individual per S slot; a drawn carrier vetoes when the guard fires), 2 private
    (no veto; carriers whose guard fires keep their demand), 3 blind (r inert).  binst >= N: atomic installation.
    Returns a tuple (see the end)."""
    np.random.seed(seed)
    I = tcount0.shape[0]; Tcap = tcount0.shape[2]; PCn = J.shape[0]
    nout = ISMEM.shape[0]
    tcount = tcount0.copy()
    tpres = np.zeros((I, 3, Tcap), np.int64); tnpres = np.zeros((I, 3), np.int64); tpos = -np.ones((I, 3, Tcap), np.int64)
    pcount = np.zeros((I, 3, PCn), np.int64); ppres = np.zeros((I, 3, PCn), np.int64)
    pnpres = np.zeros((I, 3), np.int64); ppos = -np.ones((I, 3, PCn), np.int64)
    glob = np.zeros((3, PCn), np.int64)
    Fp = np.zeros((I, 3, PCn))
    introg = np.full((I, 3, PCn), -2, np.int64); introc = np.zeros((I, 3, PCn), np.int64)
    for i in range(I):
        for s in range(3):
            for t in range(Tcap):
                if tcount[i, s, t] > 0:
                    tpres[i, s, tnpres[i, s]] = t; tpos[i, s, t] = tnpres[i, s]; tnpres[i, s] += 1
                    pcount[i, s, TPC[s, t]] += tcount[i, s, t]
            for pc in range(PCn):
                if pcount[i, s, pc] > 0:
                    ppres[i, s, pnpres[i, s]] = pc; ppos[i, s, pc] = pnpres[i, s]; pnpres[i, s] += 1
                    glob[s, pc] += pcount[i, s, pc]
                    introg[i, s, pc] = -1; introc[i, s, pc] = 0
    for i in range(I):
        for s in range(3):
            for t in range(pnpres[i, s]):
                pc = ppres[i, s, t]
                Fp[i, s, pc] = SS._fit_full(J, PAY, pcount, ppres, pnpres, i, s, pc)
    NU = 3 * I
    act = np.arange(NU); apos = np.arange(NU); nact = 0
    for u in range(NU):
        if tnpres[u // 3, u % 3] > 1:
            nact = SS._setact(u, True, act, apos, nact)
    cls = np.zeros((H + 1, I), np.int16)
    nh = hrec.shape[0]
    effrec = np.zeros((nh, I)); distrec = np.zeros((nh, I, nout))
    dist = np.zeros(nout)
    dom = -np.ones((I, 3), np.int64)
    ev = np.zeros((evcap, 8)); nev = 0
    cev = np.zeros((cevcap, 20)); ncev = 0
    cnt = np.zeros((I, 8), np.int64)      # draws, null, empty menu, guarded proposals, refused, installed, infeasible, overflow
    nrec = H // rec_every + 1
    rfreq = np.zeros((nrec, I, 3), np.float32)
    menus = np.zeros((nrec, I), np.int64)
    pend = -np.ones((pendcap, 10), np.int64); npend = 0
    N2 = float(N) * N
    UN = NU * N
    mm = m if I > 1 else 0.0
    overflow = False
    for i in range(I):
        c, e = SS._classify(J, VEC, ISMEM, TOT, pcount, ppres, pnpres, i, N, dist, nout)
        cls[0, i] = c
        for s in range(3):
            for t in range(pnpres[i, s]):
                pc = ppres[i, s, t]
                if 2 * pcount[i, s, pc] > N:
                    dom[i, s] = pc
            if dom[i, s] >= 0 and nev < evcap:
                ev[nev, 0] = 0; ev[nev, 1] = i; ev[nev, 2] = s; ev[nev, 3] = -1; ev[nev, 4] = dom[i, s]
                ev[nev, 5] = -1; ev[nev, 6] = 0; ev[nev, 7] = np.nan
                nev += 1
    for i in range(I):
        for s in range(3):
            v = 0.0
            for t in range(tnpres[i, s]):
                tt = tpres[i, s, t]
                v += tcount[i, s, tt] * TR[s, tt]
            rfreq[0, i, s] = v / N
        if menu_g:
            mk = 0
            for s in range(3):
                for t in range(tnpres[i, s]):
                    tt = tpres[i, s, t]
                    if TC[s, tt] >= 0:
                        mk |= 1 << TC[s, tt]
            menus[0, i] = mk
    b = 0
    g = 0
    hi = 0
    nextchk = UN
    status = 4; stop_gen = H
    nmig = 0
    total = H * UN
    cls0 = np.zeros(PCn, np.int64); cls1 = np.zeros(PCn, np.int64); cls2 = np.zeros(PCn, np.int64)
    mvt = np.zeros(Tcap, np.int64); mvn = np.zeros(Tcap, np.int64); tmpc = np.zeros(Tcap, np.int64)
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
                c, e = SS._classify(J, VEC, ISMEM, TOT, pcount, ppres, pnpres, i, N, dist, nout)
                cls[g, i] = c
                if hi < nh and hrec[hi] == g:
                    effrec[hi, i] = e
                    for z in range(nout):
                        distrec[hi, i, z] = dist[z]
                for s in range(3):
                    nd = -1
                    for t in range(pnpres[i, s]):
                        pc = ppres[i, s, t]
                        if 2 * pcount[i, s, pc] > N:
                            nd = pc
                    if nd >= 0 and nd != dom[i, s]:
                        if nev < evcap:
                            ev[nev, 0] = g; ev[nev, 1] = i; ev[nev, 2] = s; ev[nev, 3] = dom[i, s]; ev[nev, 4] = nd
                            ev[nev, 5] = introg[i, s, nd]; ev[nev, 6] = introc[i, s, nd]
                            if dom[i, s] >= 0:
                                ev[nev, 7] = (SS._fit_full(J, PAY, pcount, ppres, pnpres, i, s, nd)
                                              - SS._fit_full(J, PAY, pcount, ppres, pnpres, i, s, dom[i, s])) / N2
                            else:
                                ev[nev, 7] = np.nan
                        nev += 1
                        dom[i, s] = nd
            if hi < nh and hrec[hi] == g:
                hi += 1
            # pending fates of beta < 1 installations
            for q in range(npend):
                if pend[q, 7] != 0:
                    continue
                i = pend[q, 1]
                n0 = _nplay(pcount, ppres, pnpres, PCACT, i, pend[q, 2], pend[q, 4])
                n1 = _nplay(pcount, ppres, pnpres, PCACT, i, pend[q, 3], pend[q, 5])
                st = 0
                if n0 == N and n1 == N:
                    st = 1
                elif n0 == 0 and n1 == 0:
                    st = 2
                elif (n0 == N and n1 == 0) or (n0 == 0 and n1 == N):
                    st = 3
                elif g - pend[q, 6] > 3000:
                    st = 4
                if st > 0:
                    pend[q, 7] = st; pend[q, 8] = g
            # trajectories
            if g % rec_every == 0:
                rr_ = g // rec_every
                for i in range(I):
                    for s in range(3):
                        v = 0.0
                        for t in range(tnpres[i, s]):
                            tt = tpres[i, s, t]
                            v += tcount[i, s, tt] * TR[s, tt]
                        rfreq[rr_, i, s] = v / N
                    if menu_g:
                        mk = 0
                        for s in range(3):
                            for t in range(tnpres[i, s]):
                                tt = tpres[i, s, t]
                                if TC[s, tt] >= 0:
                                    mk |= 1 << TC[s, tt]
                        menus[rr_, i] = mk
            # contract events
            if nu > 0.0 and g < H:
                for i in range(I):
                    if np.random.random() >= nu:
                        continue
                    cnt[i, 0] += 1
                    if menu_g:
                        mk = 0
                        for s in range(3):
                            for t in range(tnpres[i, s]):
                                tt = tpres[i, s, t]
                                if TC[s, tt] >= 0:
                                    mk |= 1 << TC[s, tt]
                        if mk == 0:
                            cnt[i, 2] += 1
                            continue
                        nb_ = 0
                        for kk in range(NCON):
                            if (mk >> kk) & 1:
                                nb_ += 1
                        rk = np.random.randint(nb_)
                        kap = -1
                        for kk in range(NCON):
                            if (mk >> kk) & 1:
                                if rk == 0:
                                    kap = kk; break
                                rk -= 1
                    else:
                        kap = np.random.randint(NCON)
                    s0 = CS[kap, 0]; s1 = CS[kap, 1]; d0 = CD[kap, 0]; d1 = CD[kap, 1]
                    if d0 + d1 > 6:
                        cnt[i, 6] += 1; cnt[i, 1] += 1
                        continue
                    y0 = _slot_mean(Fp, pcount, ppres, pnpres, i, s0, N, N2)
                    y1 = _slot_mean(Fp, pcount, ppres, pnpres, i, s1, N, N2)
                    if not (d0 / 6.0 > y0 + 1e-9 and d1 / 6.0 > y1 + 1e-9):
                        cnt[i, 1] += 1
                        continue
                    cc_, e_ = SS._classify(J, VEC, ISMEM, TOT, pcount, ppres, pnpres, i, N, dist, nout)
                    modal = 0; mx = -1.0
                    for z in range(nout):
                        if dist[z] > mx:
                            mx = dist[z]; modal = z
                    guard = ISMEM[modal] and not (d0 == 3 and d1 == 3)
                    if guard:
                        cnt[i, 3] += 1
                    rc0 = 0; rc1 = 0
                    for t in range(tnpres[i, s0]):
                        tt = tpres[i, s0, t]
                        rc0 += tcount[i, s0, tt] * TR[s0, tt]
                    for t in range(tnpres[i, s1]):
                        tt = tpres[i, s1, t]
                        rc1 += tcount[i, s1, tt] * TR[s1, tt]
                    rd0 = -1; rd1 = -1
                    refused = False
                    if consent == 1 and guard:
                        for z in range(2):
                            sz = s0 if z == 0 else s1
                            r_ = np.random.randint(N); acc = 0; tv = tpres[i, sz, 0]
                            for t in range(tnpres[i, sz]):
                                tt = tpres[i, sz, t]; acc += tcount[i, sz, tt]
                                if r_ < acc:
                                    tv = tt; break
                            if z == 0:
                                rd0 = TR[sz, tv]
                            else:
                                rd1 = TR[sz, tv]
                        if rd0 == 1 or rd1 == 1:
                            refused = True
                    row = ncev
                    if ncev < cevcap:
                        cev[row, 0] = g; cev[row, 1] = i; cev[row, 2] = kap; cev[row, 4] = cc_; cev[row, 5] = modal
                        cev[row, 6] = y0; cev[row, 7] = y1; cev[row, 8] = rd0; cev[row, 9] = rd1; cev[row, 10] = 1.0 if guard else 0.0
                        cev[row, 17] = rc0; cev[row, 18] = rc1
                    ncev += 1
                    if refused:
                        cnt[i, 4] += 1
                        if row < cevcap:
                            cev[row, 3] = 1
                        continue
                    # install in place
                    for z in range(2):
                        sz = s0 if z == 0 else s1
                        az = CACT[kap, z]
                        ne = 0; nm = 0
                        for t in range(tnpres[i, sz]):
                            tt = tpres[i, sz, t]
                            if consent == 2 and guard and TR[sz, tt] == 1:
                                continue
                            mvt[nm] = tt; tmpc[nm] = tcount[i, sz, tt]; mvn[nm] = 0; ne += tcount[i, sz, tt]; nm += 1
                        nkept = N - ne
                        if binst >= N or binst >= ne:
                            for q in range(nm):
                                mvn[q] = tmpc[q]
                            ninst = ne
                        else:
                            rem = ne
                            for j in range(binst):
                                r_ = np.random.randint(rem); acc = 0
                                for q in range(nm):
                                    acc += tmpc[q]
                                    if r_ < acc:
                                        tmpc[q] -= 1; mvn[q] += 1; break
                                rem -= 1
                            ninst = binst
                        for q in range(nm):
                            if mvn[q] == 0:
                                continue
                            tt = mvt[q]
                            nt = _typeid(sz, TK[sz, tt], az, TR[sz, tt], TC[sz, tt], Kmax, TK, TO, TR, TC, TPC, TMAP, ntypes)
                            if nt < 0:
                                overflow = True
                                break
                            if nt == tt:
                                continue
                            _tsub(i, sz, tt, mvn[q], tcount, tpres, tnpres, tpos)
                            _tadd(i, sz, nt, mvn[q], tcount, tpres, tnpres, tpos)
                            pco = TPC[sz, tt]; pcn = TPC[sz, nt]
                            if pco != pcn:
                                _psub(i, sz, pco, mvn[q], pcount, ppres, pnpres, ppos, glob, introg)
                                _padd(i, sz, pcn, mvn[q], pcount, ppres, pnpres, ppos, glob, introg, introc, g, 2)
                        if row < cevcap:
                            cev[row, 11 + z] = ninst; cev[row, 13 + z] = nkept
                        nact = SS._setact(3 * i + sz, tnpres[i, sz] > 1, act, apos, nact)
                    if overflow:
                        cnt[i, 7] += 1
                        break
                    for s in range(3):
                        for t in range(pnpres[i, s]):
                            pc = ppres[i, s, t]
                            Fp[i, s, pc] = SS._fit_full(J, PAY, pcount, ppres, pnpres, i, s, pc)
                    cnt[i, 5] += 1
                    if row < cevcap:
                        cev[row, 3] = 2
                        cev[row, 15] = _slot_mean(Fp, pcount, ppres, pnpres, i, s0, N, N2)
                        cev[row, 16] = _slot_mean(Fp, pcount, ppres, pnpres, i, s1, N, N2)
                        cev[row, 19] = row
                    # supersede open pending entries of this island; open a new one if beta < 1
                    for q in range(npend):
                        if pend[q, 1] == i and pend[q, 7] == 0:
                            pend[q, 7] = 5; pend[q, 8] = g
                    if binst < N and npend < pendcap:
                        pend[npend, 0] = row; pend[npend, 1] = i; pend[npend, 2] = s0; pend[npend, 3] = s1
                        pend[npend, 4] = CACT[kap, 0]; pend[npend, 5] = CACT[kap, 1]; pend[npend, 6] = g
                        pend[npend, 7] = 0; pend[npend, 9] = cc_
                        npend += 1
                if overflow:
                    status = 9; stop_gen = g
                    break
            done = False
            if stop_closed and (g % close_every == 0 or g == H):
                if mm > 0.0:
                    n0 = 0; n1 = 0; n2 = 0
                    for k in range(PCn):
                        if glob[0, k] > 0:
                            cls0[n0] = k; n0 += 1
                        if glob[1, k] > 0:
                            cls1[n1] = k; n1 += 1
                        if glob[2, k] > 0:
                            cls2[n2] = k; n2 += 1
                    if SS._closed(J, cls0, n0, cls1, n1, cls2, n2):
                        status = 1; stop_gen = g; done = True
                else:
                    allc = True
                    for i in range(I):
                        if not SS._closed(J, ppres[i, 0], pnpres[i, 0], ppres[i, 1], pnpres[i, 1], ppres[i, 2], pnpres[i, 2]):
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
        # parent among the source unit's types, weight count * exp(w f(play class))
        mx = -1e300
        for t in range(tnpres[src, s]):
            tt = tpres[src, s, t]
            f = Fp[src, s, TPC[s, tt]] / N2
            if f > mx: mx = f
        tot = 0.0
        for t in range(tnpres[src, s]):
            tt = tpres[src, s, t]
            tot += tcount[src, s, tt] * np.exp(w * (Fp[src, s, TPC[s, tt]] / N2 - mx))
        uu = np.random.random() * tot; acc2 = 0.0
        child = tpres[src, s, tnpres[src, s] - 1]
        for t in range(tnpres[src, s]):
            tt = tpres[src, s, t]
            acc2 += tcount[src, s, tt] * np.exp(w * (Fp[src, s, TPC[s, tt]] / N2 - mx))
            if uu <= acc2:
                child = tt; break
        r = np.random.randint(N); acc = 0; victim = tpres[i, s, 0]
        for t in range(tnpres[i, s]):
            tt = tpres[i, s, t]; acc += tcount[i, s, tt]
            if r < acc:
                victim = tt; break
        if victim == child:
            continue
        _tsub(i, s, victim, 1, tcount, tpres, tnpres, tpos)
        _tadd(i, s, child, 1, tcount, tpres, tnpres, tpos)
        pv = TPC[s, victim]; pcc = TPC[s, child]
        if pv != pcc:
            _psub(i, s, pv, 1, pcount, ppres, pnpres, ppos, glob, introg)
            new = pcount[i, s, pcc] == 0
            _padd(i, s, pcc, 1, pcount, ppres, pnpres, ppos, glob, introg, introc, g + 1, 1 if mig else 0)
            o1, o2 = SS._others(s)
            for sa in (o1, o2):
                sb = o1 + o2 - sa
                for ta in range(pnpres[i, sa]):
                    k = ppres[i, sa, ta]
                    v = 0.0
                    for tb in range(pnpres[i, sb]):
                        q = ppres[i, sb, tb]
                        if s < sb:
                            v += pcount[i, sb, q] * (PAY[SS._code(J, sa, k, pcc, q), sa] - PAY[SS._code(J, sa, k, pv, q), sa])
                        else:
                            v += pcount[i, sb, q] * (PAY[SS._code(J, sa, k, q, pcc), sa] - PAY[SS._code(J, sa, k, q, pv), sa])
                    Fp[i, sa, k] += v
            if new:
                Fp[i, s, pcc] = SS._fit_full(J, PAY, pcount, ppres, pnpres, i, s, pcc)
        nact = SS._setact(u, tnpres[i, s] > 1, act, apos, nact)
    for gg in range(stop_gen + 1, H + 1):
        for i in range(I):
            cls[gg, i] = cls[stop_gen, i]
    for z in range(hi, nh):
        if hrec[z] > stop_gen:
            for i in range(I):
                c, e = SS._classify(J, VEC, ISMEM, TOT, pcount, ppres, pnpres, i, N, dist, nout)
                effrec[z, i] = e
                for zz in range(nout):
                    distrec[z, i, zz] = dist[zz]
    return (status, stop_gen, tcount, cls, effrec, distrec, ev[:min(nev, evcap)], nev, nmig, cev[:min(ncev, cevcap)],
            ncev, cnt, rfreq, menus, pend[:npend], pcount)


# ====================================================================== run setup
class Setup:
    """per-run tables: the extended play-class universe (base programs padded to Kmax, then the nine constants of each
    slot as override classes), the joint table, the type tables and the initial type counts."""

    def __init__(self, init, U, fr=0.0, pcar=0.0, rng=None, Tcap=None, arm='weak'):
        S, mu = SS.arm_data(arm)
        I = init.shape[0]
        self.U = U
        Kmax = max(len(u) for u in U)
        self.Kmax = Kmax
        ci = SS.const_index(S.fs)
        Up = []
        for s in range(3):
            u = np.concatenate([U[s], np.full(Kmax - len(U[s]), U[s][0])]).astype(np.int64)
            Up.append(np.concatenate([u, np.array([ci[l] for l in range(9)], np.int64)]))
        self.Uext = Up
        self.J = SS.joint_for(arm, Up)
        PCn = Kmax + 9
        self.PCACT = -np.ones((3, PCn), np.int64)
        self.COND = np.zeros((3, PCn), np.bool_)
        for s in range(3):
            for pc in range(PCn):
                x = Up[s][pc]
                atoms, tab = S.fs[x]
                if not atoms:
                    self.PCACT[s, pc] = tab[0]
                else:
                    self.COND[s, pc] = True
        if Tcap is None:
            Tcap = Kmax * NKEY_O * 2 if pcar == 0.0 else 16384
        Tcap = max(Tcap, Kmax)
        self.TK = np.zeros((3, Tcap), np.int64); self.TO = -np.ones((3, Tcap), np.int64)
        self.TR = np.zeros((3, Tcap), np.int64); self.TC = -np.ones((3, Tcap), np.int64)
        self.TPC = np.zeros((3, Tcap), np.int64)
        self.TMAP = -np.ones((3, Kmax * NKEY_O * 2 * NKEY_C), np.int64)
        self.ntypes = np.zeros(3, np.int64)
        for s in range(3):
            for k in range(Kmax):
                t = self.tid(s, k, -1, 0, -1)
                assert t == k
        tc = np.zeros((I, 3, Tcap), np.int64)
        tc[:, :, :init.shape[2]] = init[:, :, :Kmax]
        # refusal bits and carried contracts, drawn after the founders from the run's generator
        if fr > 0.0 or pcar > 0.0:
            naming = [[k for k in range(NCON) if s in CONTRACTS[k][0]] for s in range(3)]
            new = np.zeros_like(tc)
            for i in range(I):
                for s in range(3):
                    for k in np.nonzero(tc[i, s, :Kmax])[0]:
                        n = int(tc[i, s, k])
                        rb = (rng.random(n) < fr).astype(int) if fr < 1.0 else np.ones(n, int)
                        cc = np.full(n, -1)
                        if pcar > 0.0:
                            car = rng.random(n) < pcar
                            cc[car] = rng.choice(naming[s], car.sum())
                        for r_, c_ in zip(rb, cc):
                            t = self.tid(s, k, -1, int(r_), int(c_))
                            new[i, s, t] += 1
            tc = new
        self.tc0 = tc
        self.Tcap = Tcap

    def tid(self, s, k, o, r, c):
        key = ((k * NKEY_O + (o + 1)) * 2 + r) * NKEY_C + (c + 1)
        t = self.TMAP[s, key]
        if t >= 0:
            return int(t)
        t = int(self.ntypes[s])
        if t >= self.TK.shape[1]:
            raise RuntimeError('type capacity')
        self.TMAP[s, key] = t
        self.TK[s, t] = k; self.TO[s, t] = o; self.TR[s, t] = r; self.TC[s, t] = c
        self.TPC[s, t] = k if o < 0 else self.Kmax + o
        self.ntypes[s] = t + 1
        return t


def tables():
    st = SS.Tables(SS.dollar3_game())
    return st


def run_kernel(setup, T, N, mN, seed, H, hrec, nu=0.0, menu_g=False, beta=1.0, consent=0, stop_closed=None,
               close_every=10, rec_every=10, evcap=2000000, cevcap=400000, pendcap=200000):
    CS, CD, CACT = contract_arrays()
    binst = N if beta >= 1.0 else int(round(beta * N))
    if stop_closed is None:
        stop_closed = (nu == 0.0)
    return dkern(setup.J, T.PAY, T.VEC, T.ISMEM, T.TOT, setup.PCACT, setup.tc0, setup.TK, setup.TO, setup.TR, setup.TC,
                 setup.TPC, setup.TMAP, setup.ntypes, setup.Kmax, N, W, mN / N, seed, H, close_every,
                 np.asarray(hrec, np.int64), float(nu), bool(menu_g), binst, consent, CS, CD, CACT, bool(stop_closed),
                 rec_every, evcap, cevcap, pendcap)


CONSENT = dict(none=0, public=1, private=2, blind=3)
