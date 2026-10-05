"""epsilon -> 0 chain over monomorphic triples for the three-player dollar.

State: (a, b, c), one payoff class per slot.  A mutation event picks a slot
uniformly, draws a mutant class q from that slot's prior, and q fixes with the
exact constant-selection Moran probability (frequency independence: a
slot-s program's payoff depends only on the two other residents)

    rho = (1 - 1/r) / (1 - r^-N),  r = exp(w (u_q - u_res)),  rho = 1/N if r = 1.

pi is the stationary distribution of this chain.  The state space (K^3) is
too large to solve whole.  A core (from the 729 constant triples, grown by
promotion) is solved exactly by dense GTH in log-scaled form (rates span far
beyond double range at large N); a ring of one-step excursions out of the core,
selected by pi-weighted inflow > theta, is folded into the core rates exactly
(stochastic complement of a ring state whose only kept moves return to the
core).  Moves from the ring to anything but the core, and from the core to
states outside core and ring, are dropped (reflecting boundary) and reported as
the cut flow.
"""
import os, sys, time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
sys.path.insert(0, os.path.dirname(__file__))
import dollar3 as D
from abm import njit
from dollar3_solve import dense_log_gth


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
def _rows(arm, nat, atL, atJ, atA, tab, PARTNER, reps, logm, states, members, K, N, w, pi, theta_edge, mode):
    """For each state (sorted codes `states`):
    mode 0: edges to states inside the set (src index, dst index, log prob),
            the total leaving probability, payoffs and outcome type;
    mode 1: edges leaving the set with log pi[src] + log prob > log theta_edge
            (src, dst code, log flow), and the total flow leaving the set.
    `pi` holds log pi."""
    S = states.shape[0]
    Kc = reps.shape[1]
    cap = S * 16 + 1024
    src = np.empty(cap, np.int64); dst = np.empty(cap, np.int64); pr = np.empty(cap, np.float64)
    chg = np.empty(cap, np.bool_)
    out_chg = np.zeros(S); cut_chg = 0.0
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
                lp = logm[s, q] + log_rho(dw, N)
                ep = np.exp(lp)
                out_tot[i] += ep
                ch = u[0] != r0 or u[1] != r1 or u[2] != r2
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


class Chain3:
    def __init__(self, arm, S, classes, mu, N, w=0.3, theta=1e-9, pmin=1e-16, max_states=400000, max_rounds=40,
                 workers=1, verbose=True, constants_only=False, core=2000, core_max=2500, max_ring=300000, promote=1e-5):
        """classes: payoff class id per program (slot 0; other slots by
        relabeling, which the invariance test shows is exact).  mu: normalized
        prior over programs."""
        self.arm, self.S, self.N, self.w = arm, S, N, w
        self.theta, self.pmin, self.max_states, self.max_rounds, self.verbose = theta, pmin, max_states, max_rounds, verbose
        self.A = D.arrays(S); self.ia = D.ARM[arm]; self.core = core
        self.core_max, self.max_ring, self.promote = core_max, max_ring, promote
        self.drop_rel = 1e-5
        # Row-scaled linear GTH is exact while every rate is within double range of its row max (N <= 10^3 here:
        # e^-200 at worst).  Beyond that, log-space GTH: a rate negligible within its row can still be the only
        # bridge between two closed classes (checked on the constants chain at N = 10^4).
        self.gth = dense_log_gth if N > 2000 else gth_scaled
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

    def rows(self, codes, members=None, lpi=None, theta_edge=0.0, mode=0):
        """mode 0: edges from `codes` into the sorted set `members` (default
        codes itself; dst = index in members, log prob).  mode 1: edges leaving
        `members` with log pi + log prob > log theta_edge (dst = code, log flow)."""
        codes = np.asarray(codes, np.int64)
        members = codes if members is None else np.asarray(members, np.int64)
        if lpi is None: lpi = np.zeros(len(codes))
        return _rows(self.ia, *self.A, self.reps, self.logm, codes, members, self.Kc, float(self.N), self.w, lpi,
                     np.log(theta_edge) if theta_edge > 0 else -np.inf, mode)

    # ---- exploration: a core solved exactly, plus a ring of one-step excursions
    def explore(self, seeds=None):
        if seeds is None:
            seeds = [self.code(a, b, c) for a in self.const_class[0] for b in self.const_class[1] for c in self.const_class[2]]
        core = np.unique(np.array(seeds, np.int64))
        self.log = []
        t0 = time.time()
        src, dst, lp, out_c, pay_c, typ_c, _, _, _, _ = self.rows(core, mode=0)
        lpi_c = self.gth(_assemble(len(core), src, dst, lp))
        for rnd in range(self.max_rounds):
            csrc, cdst, cfl, _, _, _, _, _, _, _ = self.rows(core, core, lpi_c, self.theta / 10, mode=1)
            ud, inv = np.unique(cdst, return_inverse=True)
            fl = np.bincount(inv, weights=np.exp(cfl))
            ring = ud[fl > self.theta]
            if len(ring) > self.max_ring:
                ring = np.sort(ud[np.argsort(-fl)[:self.max_ring]])
            allset = np.union1d(core, ring)
            ci = np.searchsorted(allset, core); ri = np.searchsorted(allset, ring)
            src, dst, lp, out_c, pay_c, typ_c, _, chg_c, outchg_c, _ = self.rows(core, allset, mode=0)
            rsrc, rdst, rlp, out_r, pay_r, typ_r, _, chg_r, outchg_r, _ = self.rows(ring, allset, mode=0)
            loc = -np.ones(len(allset), np.int64); loc[ci] = np.arange(len(core))
            rloc = -np.ones(len(allset), np.int64); rloc[ri] = np.arange(len(ring))
            d_core = loc[dst]; d_ring = rloc[dst]
            cc = d_core >= 0; cr = d_ring >= 0
            rc = loc[rdst] >= 0
            lpi_c, lpi_r = solve_with_ring(len(core), len(ring), src[cc], d_core[cc], lp[cc], src[cr], d_ring[cr], lp[cr],
                                           rsrc[rc], loc[rdst[rc]], rlp[rc], gth=self.gth)
            _, _, _, _, _, _, cut_c, _, _, cutchg_c = self.rows(core, allset, lpi_c, 1e300, mode=1)
            to_core = np.bincount(rsrc[rc], weights=np.exp(rlp[rc]), minlength=len(ring))
            to_core_chg = np.bincount(rsrc[rc & chg_r], weights=np.exp(rlp[rc & chg_r]), minlength=len(ring))
            cutchg_r = float(np.exp(lpi_r) @ np.maximum(outchg_r - to_core_chg, 0)) if len(ring) else 0.0
            chg_flow = float(np.exp(lpi_c) @ outchg_c + (np.exp(lpi_r) @ outchg_r if len(ring) else 0.0))
            cut_r = float(np.exp(lpi_r) @ np.maximum(out_r - to_core, 0)) if len(ring) else 0.0
            total_flow = float(np.exp(lpi_c) @ out_c + (np.exp(lpi_r) @ out_r if len(ring) else 0.0))
            cut = cut_c + cut_r
            dropped = np.exp(lpi_r) * np.maximum(outchg_r - to_core_chg, 0) if len(ring) else np.zeros(0)
            score = np.maximum(np.exp(lpi_r) / self.promote, dropped / (self.drop_rel * chg_flow)) if len(ring) else np.zeros(0)
            # promote ring states that carry mass, or whose dropped (non-returning) flow is large

            promote = ring[score > 1] if len(ring) else ring
            room = self.core_max - len(core)
            if len(promote) > room:
                promote = ring[np.argsort(-score)[:max(room, 0)]]
            self.log.append(dict(round=rnd, core=len(core), ring=len(ring), cut_flow=cut, cut_core=cut_c, cut_ring=cut_r,
                                 cut_change=cutchg_c + cutchg_r, change_flow=chg_flow, rel_cut_change=(cutchg_c + cutchg_r) / chg_flow,
                                 total_flow=total_flow, rel_cut=cut / total_flow,
                                 ring_mass=float(np.exp(lpi_r).sum()) if len(ring) else 0.0,
                                 promoted=len(promote), time_s=time.time() - t0))
            if self.verbose:
                print('  [%s N=%g] round %d: core %d, ring %d (mass %.3e), cut %.2e (rel %.2e), outcome-changing cut rel %.2e, promote %d, %.0fs' % (
                    self.arm, self.N, rnd, len(core), len(ring), self.log[-1]['ring_mass'], cut, cut / total_flow,
                    self.log[-1]['rel_cut_change'], len(promote), time.time() - t0), flush=True)
            if len(promote) == 0:
                break
            core = np.union1d(core, promote)
            src, dst, lp, out_c, pay_c, typ_c, _, _, _, _ = self.rows(core, mode=0)
            lpi_c = self.gth(_assemble(len(core), src, dst, lp))
        n_c = len(core)
        self.codes = np.concatenate([core, ring])
        self.is_core = np.concatenate([np.ones(n_c, bool), np.zeros(len(ring), bool)])
        self.lpi = np.concatenate([lpi_c, lpi_r]); self.pi = np.exp(self.lpi)
        self.pay = np.concatenate([pay_c, pay_r]); self.typ = np.concatenate([typ_c, typ_r])
        self.out_tot = np.concatenate([out_c, out_r])
        self.src = np.concatenate([src[cc], src[cr], rsrc[rc] + n_c])
        self.dst_idx = np.concatenate([d_core[cc], d_ring[cr] + n_c, loc[rdst[rc]]])
        self.pr = np.concatenate([lp[cc], lp[cr], rlp[rc]])
        self.cut_flow, self.rel_cut = cut, cut / total_flow
        self.rel_cut_change = self.log[-1]['rel_cut_change']
        self.index = {int(c): k for k, c in enumerate(self.codes)}
        return self

    # ---- full exploration (every kept edge, sparse LU): valid while all rates are within double range and LU does
    # not cancel, which holds at N = 100 (checked against GTH on the constants chain), not at N >= 10^3
    def explore_full(self, seeds=None):
        if seeds is None:
            seeds = [self.code(a, b, c) for a in self.const_class[0] for b in self.const_class[1] for c in self.const_class[2]]
        codes = np.unique(np.array(seeds, np.int64))
        self.log = []
        t0 = time.time()
        for rnd in range(self.max_rounds):
            src, dst, lp, out_t, pay, typ, _, chg, out_chg, _ = self.rows(codes, mode=0)
            n = len(codes)
            Q = sp.csr_matrix((np.exp(lp), (src, dst)), shape=(n, n))
            Q.setdiag(0); Q.eliminate_zeros()
            d = np.asarray(Q.sum(axis=1)).ravel()
            Qt = (Q - sp.diags(d)).T.tolil(); Qt[n - 1, :] = 1.0
            b = np.zeros(n); b[n - 1] = 1.0
            pi = np.clip(spla.spsolve(Qt.tocsc(), b), 0, None); pi /= pi.sum()
            lpi = np.log(np.maximum(pi, 1e-320))
            csrc, cdst, cfl, _, _, _, cut, _, _, cutchg = self.rows(codes, codes, lpi, self.theta / 10, mode=1)
            ud, inv = np.unique(cdst, return_inverse=True)
            fl = np.bincount(inv, weights=np.exp(cfl))
            cand = ud[fl > self.theta]
            total_flow = float(pi @ out_t); chg_flow = float(pi @ out_chg)
            self.log.append(dict(round=rnd, states=n, cut_flow=float(cut), rel_cut=float(cut) / total_flow, cut_change=float(cutchg),
                                 rel_cut_change=float(cutchg) / chg_flow, candidates=len(cand), time_s=time.time() - t0))
            if self.verbose:
                print('  [%s N=%g full] round %d: %d states, cut rel %.2e, outcome-changing cut rel %.2e, %d candidates, %.0fs' % (
                    self.arm, self.N, rnd, n, cut / total_flow, cutchg / chg_flow, len(cand), time.time() - t0), flush=True)
            if len(cand) == 0 or n >= self.max_states:
                break
            if n + len(cand) > self.max_states:
                cand = ud[np.argsort(-fl)[:self.max_states - n]]
            codes = np.union1d(codes, cand)
        self.codes, self.pi, self.lpi = codes, pi, lpi
        self.is_core = np.ones(len(codes), bool)
        self.pay, self.typ, self.out_tot = pay, typ, out_t
        self.src, self.dst_idx, self.pr = src, dst, lp
        self.cut_flow, self.rel_cut = float(cut), float(cut) / total_flow
        self.rel_cut_change = float(cutchg) / chg_flow
        self.index = {int(c): k for k, c in enumerate(codes)}
        return self

    # ---- hybrid exploration: core by dense GTH, ring censored out by sparse LU on the ring's jump chain
    def explore_hybrid(self, seeds=None):
        """The explored set is core + ring, with every edge between explored
        states kept.  The ring is eliminated exactly by its stochastic
        complement: core rates R'_cc = R_cc + R_cr (D_r - R_rr)^-1 R_rc, with
        (D_r - R_rr) = D_r (I - P_rr) factored by sparse LU in jump-chain form
        (no holding-time disparity, and I - P_rr is diagonally dominant by
        the ring's direct return to the core).  The core is solved by GTH in
        log-scaled form, which handles rates beyond double range.  New ring
        states: pi-weighted inflow > theta from any explored state.  Ring
        states with pi > promote move into the core (up to core_max)."""
        if seeds is None:
            seeds = [self.code(a, b, c) for a in self.const_class[0] for b in self.const_class[1] for c in self.const_class[2]]
        core = np.unique(np.array(seeds, np.int64)); ring = np.zeros(0, np.int64)
        self.log = []
        t0 = time.time()
        src, dst, lp = self.rows(core, mode=0)[:3]
        lpi = self.gth(_assemble(len(core), src, dst, lp))
        allset = core; is_core = np.ones(len(core), bool)
        for rnd in range(self.max_rounds):
            _, cdst, cfl, _, _, _, cut, _, _, cutchg = self.rows(allset, allset, lpi, self.theta / 10, mode=1)
            ud, inv = np.unique(cdst, return_inverse=True)
            fl = np.bincount(inv, weights=np.exp(cfl))
            cand = ud[fl > self.theta]
            if rnd > 0:
                prev = self.log[-1]
                # flows can underflow to 0 at N = 10^4 when pi sits on states whose exits are all ~e^-1000
                prev.update(cut_flow=float(cut), rel_cut=float(cut) / prev['total_flow'] if prev['total_flow'] > 0 else float('nan'),
                            cut_change=float(cutchg),
                            rel_cut_change=float(cutchg) / prev['change_flow'] if prev['change_flow'] > 0 else float('nan'),
                            new_candidates=len(cand))
                if self.verbose:
                    print('  [%s N=%g hybrid] round %d: core %d, ring %d, ring mass %.3e, cut rel %.2e, outcome-changing cut rel %.2e, promoted %d, new %d, %.0fs' % (
                        self.arm, self.N, rnd - 1, prev['core'], prev['ring'], prev['ring_mass'], prev['rel_cut'], prev['rel_cut_change'],
                        prev['promoted'], len(cand), time.time() - t0), flush=True)
                # stop when nothing is promoted and the new candidates are under 1% of the set with outcome cut < 2%
                small = len(cand) < 0.01 * len(allset) and prev['rel_cut_change'] == prev['rel_cut_change'] and prev['rel_cut_change'] < 0.02
                if prev['promoted'] == 0 and (len(cand) == 0 or small):
                    break
            if len(allset) + len(cand) > self.max_states:
                cand = ud[np.argsort(-fl)[:max(self.max_states - len(allset), 0)]]
            ring = np.union1d(ring, cand)
            allset = np.union1d(core, ring); is_core = np.isin(allset, core)
            src, dst, lp, out_t, pay, typ, _, chg, out_chg, _ = self.rows(allset, mode=0)
            lpi = solve_censored(len(allset), is_core, src, dst, lp, self.gth)
            pi = np.exp(lpi)
            total_flow = float(pi @ out_t); chg_flow = float(pi @ out_chg)
            rmask = ~is_core
            promote = allset[rmask][lpi[rmask] > np.log(self.promote)]
            room = self.core_max - len(core)
            if len(promote) > room:
                order = np.argsort(-lpi[rmask])
                promote = allset[rmask][order[:max(room, 0)]]
            self.log.append(dict(round=rnd, core=len(core), ring=len(ring), ring_mass=float(pi[rmask].sum()), total_flow=total_flow,
                                 change_flow=chg_flow, promoted=len(promote), time_s=time.time() - t0))
            if len(promote):
                core = np.union1d(core, promote); ring = np.setdiff1d(ring, promote)
                allset = np.union1d(core, ring); is_core = np.isin(allset, core)
                lpi = solve_censored(len(allset), is_core, src, dst, lp, self.gth)
        self.codes, self.lpi, self.pi = allset, lpi, np.exp(lpi)
        self.is_core = is_core
        self.pay, self.typ, self.out_tot = pay, typ, out_t
        self.src, self.dst_idx, self.pr = src, dst, lp
        last = self.log[-1]
        if 'cut_flow' not in last:          # stopped by max_rounds: measure the cut of the final set
            _, _, _, _, _, _, cut, _, _, cutchg = self.rows(allset, allset, lpi, 1e300, mode=1)
            last.update(cut_flow=float(cut), rel_cut=float(cut) / last['total_flow'] if last['total_flow'] > 0 else float('nan'),
                        cut_change=float(cutchg),
                        rel_cut_change=float(cutchg) / last['change_flow'] if last['change_flow'] > 0 else float('nan'))
        self.cut_flow, self.rel_cut, self.rel_cut_change = last.get('cut_flow', np.nan), last.get('rel_cut', np.nan), last.get('rel_cut_change', np.nan)
        self.index = {int(c): k for k, c in enumerate(allset)}
        return self


@njit(cache=True)
def _lae(a, b):
    if a == -np.inf: return b
    if b == -np.inf: return a
    if a > b: return a + np.log1p(np.exp(b - a))
    return b + np.log1p(np.exp(a - b))


@njit(cache=True)
def gth_scaled(Alog):
    """Stationary log pi of the chain with log rates Alog (diagonal ignored).
    Rows are scaled by their max (holding times change, pi_i -> pi_i e^{M_i}),
    which brings every row into double range; then linear GTH (no
    subtractions)."""
    K = Alog.shape[0]
    M = np.empty(K)
    A = np.zeros((K, K))
    for i in range(K):
        m = -np.inf
        for j in range(K):
            if j != i and Alog[i, j] > m: m = Alog[i, j]
        if m == -np.inf: m = 0.0
        M[i] = m
        for j in range(K):
            if j != i and Alog[i, j] > -np.inf:
                A[i, j] = np.exp(Alog[i, j] - m)
    for k in range(K - 1, 0, -1):
        s = 0.0
        for j in range(k):
            s += A[k, j]
        if s <= 0: s = 1e-300
        for i in range(k):
            A[i, k] /= s
        for i in range(k):
            a = A[i, k]
            if a == 0.0: continue
            for j in range(k):
                A[i, j] += a * A[k, j]
            A[i, i] = 0.0
    p = np.zeros(K); p[0] = 1.0
    for k in range(1, K):
        v = 0.0
        for i in range(k):
            v += p[i] * A[i, k]
        p[k] = v
    lp = np.empty(K)
    for i in range(K):
        lp[i] = (np.log(p[i]) if p[i] > 0 else -np.inf) - M[i]
    mx = lp.max(); z = 0.0
    for i in range(K): z += np.exp(lp[i] - mx)
    return lp - mx - np.log(z)


@njit(cache=True)
def _assemble(n, src, dst, lp):
    A = np.full((n, n), -np.inf)
    for e in range(src.shape[0]):
        i = src[e]; j = dst[e]
        if i != j:
            A[i, j] = _lae(A[i, j], lp[e])
    return A


@njit(cache=True)
def _eliminate_ring(A, nr, in_r, in_c, in_l, out_r, out_c, out_l):
    """Fold excursions core i -> ring r -> core j into A[i, j] (log space).
    in_*: core -> ring edges sorted by ring; out_*: ring -> core, sorted by
    ring.  Returns log s_r, the total ring -> core rate."""
    s = np.full(nr, -np.inf)
    for e in range(out_r.shape[0]):
        s[out_r[e]] = _lae(s[out_r[e]], out_l[e])
    ia = np.searchsorted(in_r, np.arange(nr + 1))
    oa = np.searchsorted(out_r, np.arange(nr + 1))
    for r in range(nr):
        if s[r] == -np.inf:
            continue
        for e in range(ia[r], ia[r + 1]):
            i = in_c[e]; li = in_l[e] - s[r]
            for f in range(oa[r], oa[r + 1]):
                j = out_c[f]
                if j == i: continue
                A[i, j] = _lae(A[i, j], li + out_l[f])
    return s


def solve_with_ring(nc, nr, cs, cd, cl, crs, crd, crl, rcs, rcd, rcl, gth=None):
    A = _assemble(nc, cs, cd, cl)
    o = np.argsort(crd, kind='stable'); in_r, in_c, in_l = crd[o], crs[o], crl[o]
    o = np.argsort(rcs, kind='stable'); out_r, out_c, out_l = rcs[o], rcd[o], rcl[o]
    s = _eliminate_ring(A, nr, in_r, in_c, in_l, out_r, out_c, out_l)
    lpi_c = gth(A)
    lpi_r = np.full(nr, -np.inf)
    if nr:
        v = lpi_c[in_c] + in_l
        order = np.argsort(in_r, kind='stable')
        np.logaddexp.at(lpi_r, in_r, v)
        lpi_r = lpi_r - s
    z = np.logaddexp(np.logaddexp.reduce(lpi_c), np.logaddexp.reduce(lpi_r) if nr else -np.inf)
    return lpi_c - z, lpi_r - z


@njit(cache=True)
def _has_exit(arm, nat, atL, atJ, atA, tab, PARTNER, reps, logm, y0, y1, y2, u0, t0, hist, val, u):
    """1 if the triple of programs (y0, y1, y2), with payoffs u0 and type t0, has
    a strict exit (a mutant with higher payoff) or an outcome-changing neutral
    exit; 0 otherwise."""
    Kc = reps.shape[1]
    for s in range(3):
        for q in range(Kc):
            if logm[s, q] < -1e300:
                continue
            xq = reps[s, q]
            if s == 0:
                t = D.enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, xq, y1, y2, hist, val, u)
            elif s == 1:
                t = D.enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, y0, xq, y2, hist, val, u)
            else:
                t = D.enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, y0, y1, xq, hist, val, u)
            if u[s] > u0[s]:
                return 1
            if u[s] == u0[s] and (t != t0 or u[0] != u0[0] or u[1] != u0[1] or u[2] != u0[2]):
                return 2
    return 0


@njit(cache=True)
def bridge_scan(arm, nat, atL, atJ, atA, tab, PARTNER, reps, logm, c0, c1, c2):
    """Exit decomposition of the triple of classes (c0, c1, c2) by prior mass per
    mutation event: [strict, neutral-change, neutral-keep, deleterious], and
    the bridge mass: outcome-keeping neutral entrants after which a strict or
    outcome-changing neutral exit exists.  Returns (dec, bridge_mass,
    n_bridges, bridge list (slot, class) up to 64)."""
    Kc = reps.shape[1]
    hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64); u = np.empty(3, np.int64)
    u0 = np.empty(3, np.int64); u1 = np.empty(3, np.int64)
    cc = (c0, c1, c2)
    x = np.array([reps[0, c0], reps[1, c1], reps[2, c2]])
    t0 = D.enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, x[0], x[1], x[2], hist, val, u)
    u0[:] = u
    dec = np.zeros(4)
    bmass = 0.0; nb = 0
    blist = -np.ones((64, 2), np.int64)
    for s in range(3):
        for q in range(Kc):
            if q == cc[s] or logm[s, q] < -1e300:
                continue
            m = np.exp(logm[s, q])
            y = x.copy(); y[s] = reps[s, q]
            t = D.enc_into(arm, nat, atL, atJ, atA, tab, PARTNER, y[0], y[1], y[2], hist, val, u)
            if u[s] > u0[s]:
                dec[0] += m
            elif u[s] < u0[s]:
                dec[3] += m
            elif t != t0 or u[0] != u0[0] or u[1] != u0[1] or u[2] != u0[2]:
                dec[1] += m
            else:
                dec[2] += m
                u1[:] = u
                if _has_exit(arm, nat, atL, atJ, atA, tab, PARTNER, reps, logm, y[0], y[1], y[2], u1, t, hist, val, u) > 0:
                    bmass += m
                    if nb < 64:
                        blist[nb, 0] = s; blist[nb, 1] = q
                    nb += 1
    return dec, bmass, nb, blist



def src_remap(src, dst, _):
    return src, dst


def solve_censored(n, is_core, src, dst, lp, gth, batch=256):
    """log pi over n states (core mask is_core) from edges (src, dst, log rate)."""
    keep = src != dst
    src, dst, lp = src[keep], dst[keep], lp[keep]
    ci = np.nonzero(is_core)[0]; ri = np.nonzero(~is_core)[0]
    nc, nr = len(ci), len(ri)
    loc = np.empty(n, np.int64); loc[ci] = np.arange(nc); loc[ri] = np.arange(nr)
    sc, dc = is_core[src], is_core[dst]
    # core -> core in log
    e = sc & dc
    A = _assemble(nc, loc[src[e]], loc[dst[e]], lp[e])
    if nr == 0:
        return gth(A)
    # ring jump chain
    ld = np.full(n, -np.inf); np.logaddexp.at(ld, src, lp)
    e = (~sc) & (~dc)
    Prr = sp.csr_matrix((np.exp(lp[e] - ld[src[e]]), (loc[src[e]], loc[dst[e]])), shape=(nr, nr))
    e = (~sc) & dc
    Prc = sp.csr_matrix((np.exp(lp[e] - ld[src[e]]), (loc[src[e]], loc[dst[e]])), shape=(nr, nc))
    M = (sp.eye(nr) - Prr).tocsc()
    lu = spla.splu(M, permc_spec='COLAMD')
    # core -> ring rates, scaled per core row by the row max over all its out-rates
    rowmax = np.full(nc, -np.inf)
    e_all = sc
    np.maximum.at(rowmax, loc[src[e_all]], lp[e_all])
    rowmax[rowmax == -np.inf] = 0.0
    e = sc & (~dc)
    Rcr = sp.csr_matrix((np.exp(lp[e] - rowmax[loc[src[e]]]), (loc[src[e]], loc[dst[e]])), shape=(nc, nr))
    PrcT = Prc.T.tocsr()
    # W = Rcr (I - Prr)^-1 Prc   (scaled rows), batched over core rows
    W = np.zeros((nc, nc))
    rows_with = np.nonzero(np.diff(Rcr.indptr))[0]
    for b0 in range(0, len(rows_with), batch):
        rb = rows_with[b0:b0 + batch]
        rhs = Rcr[rb].toarray().T                      # nr x b
        z = lu.solve(rhs, trans='T')                   # (I - Prr)^-T rhs
        W[rb] = (PrcT @ z).T                           # b x nc
    with np.errstate(divide='ignore'):
        Wl = np.log(np.maximum(W, 0.0)) + rowmax[:, None]
    Wl[W <= 0] = -np.inf
    A = np.logaddexp(A, Wl)
    np.fill_diagonal(A, -np.inf)
    lpc = gth(A)
    # ring: pi_r = [pi_c R_cr (I - Prr)^-1]_r / d_r
    lv = lpc[:, None]  # use scaled rows: pi_c R_cr = sum_i pi_i e^{rowmax_i} Rcr_scaled[i]
    w = lpc + rowmax
    wm = w.max()
    v = Rcr.T @ np.exp(w - wm)                         # nr, scaled by e^{wm}
    x = lu.solve(v, trans='T')
    with np.errstate(divide='ignore'):
        lpr = np.log(np.maximum(x, 0.0)) + wm - ld[ri]
    out = np.empty(n)
    out[ci] = lpc; out[ri] = lpr
    m = out.max()
    return out - (m + np.log(np.exp(out - m).sum()))
