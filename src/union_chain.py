"""epsilon -> 0 chain of the union game over monomorphic (B, W1, W2) class triples.

A mutation event picks a slot uniformly, draws a mutant class from that slot's
prior over behavioural classes, and the mutant fixes with the constant-selection
Moran probability (one member of each slot per encounter, so a slot-s mutant's
payoff depends only on the two other residents; tests/test_union.py checks this
at every intermediate mutant count).  Rates span far beyond double range at
large N, so the solver is dollar3_chain's hybrid exploration: a core solved by
log-scaled GTH and a ring eliminated exactly as a stochastic complement.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import union as U
from abm import njit
from dollar3_chain import Chain3, log_rho, gth_scaled
from dollar3_solve import dense_log_gth


@njit(cache=True)
def _bsearch(arr, v):
    lo = 0; hi = arr.shape[0]
    while lo < hi:
        m = (lo + hi) // 2
        if arr[m] < v:
            lo = m + 1
        else:
            hi = m
    if lo < arr.shape[0] and arr[lo] == v:
        return lo
    return -1


@njit(cache=True)
def _rows_u(Jc, tagc, PAY, logm, states, members, KcB, KcW, N, w, pi, theta_edge, mode):
    """As dollar3_chain._rows: mode 0 edges into `members` (dst = index),
    mode 1 edges leaving `members` with log flow > theta_edge (dst = code).
    pay: float payoffs; typ: joint code * 4 + 2 t1 + t2 (tags)."""
    S = states.shape[0]
    cap = S * 16 + 1024
    src = np.empty(cap, np.int64); dst = np.empty(cap, np.int64); pr = np.empty(cap, np.float64)
    chg = np.empty(cap, np.bool_)
    out_chg = np.zeros(S); cut_chg = 0.0
    out_tot = np.zeros(S); pay = np.zeros((S, 3)); typ = np.zeros(S, np.int64)
    ne = 0
    cut = 0.0
    KK = KcW * KcW
    for i in range(S):
        code = states[i]
        b = code // KK; x = (code // KcW) % KcW; y = code % KcW
        j0 = Jc[b, x, y]
        t1 = tagc[x]; t2 = tagc[y]
        r0 = PAY[j0, t1, t2, 0]; r1 = PAY[j0, t1, t2, 1]; r2 = PAY[j0, t1, t2, 2]
        pay[i, 0] = r0; pay[i, 1] = r1; pay[i, 2] = r2; typ[i] = j0 * 4 + t1 * 2 + t2
        for s in range(3):
            Kq = KcB if s == 0 else KcW
            res = b if s == 0 else (x if s == 1 else y)
            ures = r0 if s == 0 else (r1 if s == 1 else r2)
            for q in range(Kq):
                if q == res or logm[s, q] < -1e300:
                    continue
                if s == 0:
                    j = Jc[q, x, y]; tq1 = t1; tq2 = t2
                    dcode = q * KK + x * KcW + y
                elif s == 1:
                    j = Jc[b, q, y]; tq1 = tagc[q]; tq2 = t2
                    dcode = b * KK + q * KcW + y
                else:
                    j = Jc[b, x, q]; tq1 = t1; tq2 = tagc[q]
                    dcode = b * KK + x * KcW + q
                u0 = PAY[j, tq1, tq2, 0]; u1 = PAY[j, tq1, tq2, 1]; u2 = PAY[j, tq1, tq2, 2]
                us = u0 if s == 0 else (u1 if s == 1 else u2)
                dw = w * (us - ures)
                lp = logm[s, q] + log_rho(dw, N)
                ep = np.exp(lp)
                out_tot[i] += ep
                ch = j != j0 or abs(u0 - r0) > 1e-12 or abs(u1 - r1) > 1e-12 or abs(u2 - r2) > 1e-12
                if ch:
                    out_chg[i] += ep
                jx = _bsearch(members, dcode)
                if mode == 0:
                    if jx < 0:
                        continue
                    val_store = lp; d_store = jx
                else:
                    if jx >= 0:
                        continue
                    fl = pi[i] + lp
                    cut += np.exp(fl)
                    if ch:
                        cut_chg += np.exp(fl)
                    if fl <= theta_edge:
                        continue
                    val_store = fl; d_store = dcode
                if ne >= cap:
                    cap2 = cap * 2
                    src2 = np.empty(cap2, np.int64); dst2 = np.empty(cap2, np.int64); pr2 = np.empty(cap2, np.float64)
                    chg2 = np.empty(cap2, np.bool_)
                    src2[:ne] = src[:ne]; dst2[:ne] = dst[:ne]; pr2[:ne] = pr[:ne]; chg2[:ne] = chg[:ne]
                    src, dst, pr, chg, cap = src2, dst2, pr2, chg2, cap2
                src[ne] = i; dst[ne] = d_store; pr[ne] = val_store; chg[ne] = ch; ne += 1
    return src[:ne], dst[:ne], pr[:ne], out_tot, pay, typ, cut, chg[:ne], out_chg, cut_chg


class UChain(Chain3):
    def __init__(self, C, c, N, w=0.3, theta=1e-9, max_states=400000, max_rounds=40, verbose=True,
                 core_max=2500, promote=1e-5, massB=None, massW=None, arm='quorum'):
        self.arm, self.N, self.w, self.c = arm, N, w, c
        self.theta, self.max_states, self.max_rounds, self.verbose = theta, max_states, max_rounds, verbose
        self.core_max, self.promote, self.drop_rel = core_max, promote, 1e-5
        self.gth = dense_log_gth if N > 2000 else gth_scaled
        self.C = C
        self.Jc, self.tagc = C['Jc'], C['tagc']
        self.KcB, self.KcW = C['KcB'], C['KcW']
        self.Kc = self.KcW                      # Chain3.code/decode are replaced below
        mB = C['massB'] if massB is None else massB
        mW = C['massW'] if massW is None else massW
        Km = max(self.KcB, self.KcW)
        mass = np.zeros((3, Km)); mass[0, :self.KcB] = mB; mass[1, :self.KcW] = mW; mass[2, :self.KcW] = mW
        self.mass = mass
        with np.errstate(divide='ignore'):
            self.logm = np.where(mass > 0, np.log(mass) - np.log(3.0), -np.inf)
        self.PAY = U.payoff_table(c)

    def code(self, b, x, y):
        return (int(b) * self.KcW + int(x)) * self.KcW + int(y)

    def decode(self, code):
        K = self.KcW
        return code // (K * K), (code // K) % K, code % K

    def rows(self, codes, members=None, lpi=None, theta_edge=0.0, mode=0):
        codes = np.asarray(codes, np.int64)
        members = codes if members is None else np.asarray(members, np.int64)
        if lpi is None: lpi = np.zeros(len(codes))
        return _rows_u(self.Jc, self.tagc, self.PAY, self.logm, codes, members, self.KcB, self.KcW, float(self.N), self.w, lpi,
                       np.log(theta_edge) if theta_edge > 0 else -np.inf, mode)


def dense_chain(Jc, tagc, PAY, Bs, Ws, mB, mW, N, w):
    """Exact chain over the product Bs x Ws x Ws of class lists (mutation
    restricted to these lists with masses mB, mW).  Returns states, log pi,
    log rate matrix."""
    states = [(b, x, y) for b in Bs for x in Ws for y in Ws]
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    A = np.full((n, n), -np.inf)
    lmB = np.log(np.asarray(mB) / np.sum(mB) / 3); lmW = np.log(np.asarray(mW) / np.sum(mW) / 3)
    for i, (b, x, y) in enumerate(states):
        r = PAY[Jc[b, x, y], tagc[x], tagc[y]]
        for s in range(3):
            pool = Bs if s == 0 else Ws
            lm = lmB if s == 0 else lmW
            for k, q in enumerate(pool):
                t = [b, x, y]
                if t[s] == q: continue
                t[s] = q
                u = PAY[Jc[t[0], t[1], t[2]], tagc[t[1]], tagc[t[2]]]
                A[i, idx[tuple(t)]] = np.logaddexp(A[i, idx[tuple(t)]], lm[k] + log_rho(w * (u[s] - r[s]), float(N)))
    lpi = dense_log_gth(A)
    return states, lpi, A
