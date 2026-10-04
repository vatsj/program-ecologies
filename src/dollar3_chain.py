"""epsilon -> 0 chain over monomorphic triples for the three-player dollar.

State: (a, b, c), one payoff class per slot.  A mutation event picks a slot
uniformly, draws a mutant class q from that slot's prior, and q fixes with the
exact constant-selection Moran probability (frequency independence: a
slot-s program's payoff depends only on the two other residents)

    rho = (1 - 1/r) / (1 - r^-N),  r = exp(w (u_q - u_res)),  rho = 1/N if r = 1.

pi is the stationary distribution of this chain.  The state space (K^3) is
explored from the 729 constant triples by inflow: a state is added when the
pi-weighted flow into it exceeds theta; transitions to unexplored states are
folded into the self-loop (reflecting boundary), and their total pi-weighted
flow is reported as the cut flow.
"""
import os, sys, time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
sys.path.insert(0, os.path.dirname(__file__))
import dollar3 as D
from abm import njit


@njit(cache=True)
def log_rho(dw, N):
    """log fixation probability of a single mutant, selection dw = w (u_q - u_res)."""
    if abs(dw) < 1e-12:
        return -np.log(N)
    # rho = (1 - e^-dw) / (1 - e^-N dw)
    if dw > 0:
        return np.log(-np.expm1(-dw)) - np.log(-np.expm1(-N * dw))
    # dw < 0: rho = (e^-dw - 1) / (e^-N dw - 1) = (e^|dw| - 1) e^{-N|dw|} / (1 - e^{-N|dw|})
    a = -dw
    return np.log(np.expm1(a)) - N * a - np.log(-np.expm1(-N * a))


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
def _rows(arm, nat, atL, atJ, atA, tab, PARTNER, reps, logm, states, K, N, w, pi, theta_edge, mode):
    """For each state (sorted codes `states`):
    mode 0: edges to states inside the set (src index, dst index, prob), the
            total leaving probability, payoffs and outcome type;
    mode 1: edges leaving the set with pi[src] * prob > theta_edge (src, dst
            code, flow), and the total flow leaving the set."""
    S = states.shape[0]
    Kc = reps.shape[1]
    cap = S * 16 + 1024
    src = np.empty(cap, np.int64); dst = np.empty(cap, np.int64); pr = np.empty(cap, np.float64)
    out_tot = np.zeros(S); pay = np.zeros((S, 3), np.int64); typ = np.zeros(S, np.int64)
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64); u = np.empty(3, np.int64)
    ne = 0
    cut = 0.0
    for i in range(S):
        code = states[i]
        c0 = code // (K * K); c1 = (code // K) % K; c2 = code % K
        x0 = reps[0, c0]; x1 = reps[1, c1]; x2 = reps[2, c2]
        t = D.enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, x0, x1, x2, hist, val, u)
        r0 = u[0]; r1 = u[1]; r2 = u[2]
        pay[i, 0] = u[0]; pay[i, 1] = u[1]; pay[i, 2] = u[2]; typ[i] = t
        for s in range(3):
            res = c0 if s == 0 else (c1 if s == 1 else c2)
            ures = r0 if s == 0 else (r1 if s == 1 else r2)
            for q in range(Kc):
                if q == res or logm[s, q] < -1e300:
                    continue
                xq = reps[s, q]
                if s == 0:
                    D.enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, xq, x1, x2, hist, val, u)
                    dcode = q * K * K + c1 * K + c2
                elif s == 1:
                    D.enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, x0, xq, x2, hist, val, u)
                    dcode = c0 * K * K + q * K + c2
                else:
                    D.enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, x0, x1, xq, hist, val, u)
                    dcode = c0 * K * K + c1 * K + q
                dw = w * (u[s] - ures) / 6.0
                p = np.exp(logm[s, q] + log_rho(dw, N))
                out_tot[i] += p
                jx = _bsearch(states, dcode)
                if mode == 0:
                    if jx < 0:
                        continue
                    val_store = p; d_store = jx
                else:
                    if jx >= 0:
                        continue
                    fl = pi[i] * p
                    cut += fl
                    if fl <= theta_edge:
                        continue
                    val_store = fl; d_store = dcode
                if ne >= cap:
                    cap2 = cap * 2
                    src2 = np.empty(cap2, np.int64); dst2 = np.empty(cap2, np.int64); pr2 = np.empty(cap2, np.float64)
                    src2[:ne] = src[:ne]; dst2[:ne] = dst[:ne]; pr2[:ne] = pr[:ne]
                    src, dst, pr, cap = src2, dst2, pr2, cap2
                src[ne] = i; dst[ne] = d_store; pr[ne] = val_store; ne += 1
    return src[:ne], dst[:ne], pr[:ne], out_tot, pay, typ, cut


class Chain3:
    def __init__(self, arm, S, classes, mu, N, w=0.3, theta=1e-9, pmin=1e-16, max_states=400000, max_rounds=40,
                 workers=1, verbose=True, constants_only=False):
        """classes: payoff class id per program (slot 0; other slots by
        relabeling, which the invariance test shows is exact).  mu: normalized
        prior over programs."""
        self.arm, self.S, self.N, self.w = arm, S, N, w
        self.theta, self.pmin, self.max_states, self.max_rounds, self.verbose = theta, pmin, max_states, max_rounds, verbose
        self.A = D.arrays(S); self.ia = D.ARM[arm]
        K = S.K
        # classes per slot: slot 0 given; slots 1, 2 by the permutation (0 s)
        reps = []; cls_all = []; mass = []
        Kc = int(classes.max() + 1)
        for s in range(3):
            if s == 0:
                cl = classes.copy()
            else:
                sigma = [0, 1, 2]; sigma[0], sigma[s] = s, 0
                P = S.permute(tuple(sigma))[0]       # slot-0 program x -> slot-s program P[x]
                cl = np.empty(K, np.int64); cl[P] = classes
            m = np.bincount(cl, weights=mu, minlength=Kc)
            rep = np.full(Kc, -1, np.int64)
            # representative: shortest/most massive member
            order = np.argsort(-mu, kind='stable')
            for x in order:
                if rep[cl[x]] < 0: rep[cl[x]] = x
            reps.append(rep); cls_all.append(cl); mass.append(m)
        self.reps = np.array(reps); self.cls = np.array(cls_all); self.mass = np.array(mass)
        if constants_only:
            keep = np.zeros(Kc, bool)
            for s in range(3):
                for l in range(9):
                    keep[self.cls[s, S.index[s][((), (l,))]]] = True
            for s in range(3):
                self.mass[s][:] = 0.0
                self.mass[s][self.cls[s, [S.index[s][((), (l,))] for l in range(9)]]] = 1.0 / 9   # uniform over the 9 constants
        with np.errstate(divide='ignore'):
            self.logm = np.where(self.mass > 0, np.log(self.mass) - np.log(3.0), -np.inf)
        self.Kc = Kc
        self.const_class = np.array([[self.cls[s, S.index[s][((), (l,))]] for l in range(9)] for s in range(3)])

    # ---- codes
    def code(self, a, b, c):
        return (int(a) * self.Kc + int(b)) * self.Kc + int(c)

    def decode(self, code):
        K = self.Kc
        return code // (K * K), (code // K) % K, code % K

    def rows(self, codes, pi=None, theta_edge=0.0, mode=0):
        codes = np.asarray(codes, np.int64)
        if pi is None: pi = np.zeros(len(codes))
        return _rows(self.ia, *self.A, self.reps, self.logm, codes, self.Kc, float(self.N), self.w, pi, theta_edge, mode)

    # ---- exploration
    def explore(self, seeds=None):
        if seeds is None:
            seeds = [self.code(a, b, c) for a in self.const_class[0] for b in self.const_class[1] for c in self.const_class[2]]
        codes = np.unique(np.array(seeds, np.int64))
        self.log = []
        t0 = time.time()
        for rnd in range(self.max_rounds):
            src, dst, pr, out_tot, pay, typ, _ = self.rows(codes, mode=0)
            pi = self._solve(len(codes), src, dst, pr)
            csrc, cdst, cfl, _, _, _, cut = self.rows(codes, pi, self.theta / 10, mode=1)
            ud, inv = np.unique(cdst, return_inverse=True)
            fl = np.bincount(inv, weights=cfl)
            cand = ud[fl > self.theta]
            self.log.append(dict(round=rnd, states=len(codes), cut_flow=float(cut), candidates=len(cand), time_s=time.time() - t0))
            if self.verbose:
                print('  [%s N=%g] round %d: %d states, cut flow %.2e, %d candidates, %.0fs' % (self.arm, self.N, rnd, len(codes), cut, len(cand), time.time() - t0), flush=True)
            if len(cand) == 0 or len(codes) >= self.max_states:
                break
            if len(codes) + len(cand) > self.max_states:
                cand = ud[np.argsort(-fl)[:self.max_states - len(codes)]]
            codes = np.union1d(codes, cand)
        self.codes, self.pi, self.cut_flow = codes, pi, float(cut)
        self.src, self.dst_idx, self.pr, self.out_tot, self.pay, self.typ = src, dst, pr, out_tot, pay, typ
        return self

    def _solve(self, n, i, j, p):
        # generator Q (rates per mutation event among kept states); self-loops drop out
        Q = sp.csr_matrix((p, (i, j)), shape=(n, n))
        d = np.asarray(Q.sum(axis=1)).ravel()
        Q = (Q - sp.diags(d)).T.tocsr()
        # replace the last equation by normalization
        Q = Q.tolil(); Q[n - 1, :] = 1.0
        b = np.zeros(n); b[n - 1] = 1.0
        pi = spla.spsolve(Q.tocsc(), b)
        pi = np.clip(pi, 0, None)
        return pi / pi.sum()
