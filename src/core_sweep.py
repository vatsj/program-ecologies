"""Where does the leader-value core exist?  A parametric sweep (specs/2026-10-14-core-existence-sweep.md;
definitions in notes/core-existence-sweep.md §1; predictions in predictions/2026-10-14-core-existence-sweep.md).

A static computation, no ecology.  For a coalition S the complement C responds to S's commitment a_S by
  'ind'   the pure Nash equilibria of the complement subgame (the gamma-convention, default), or
  'coord' the complement as one player maximizing its sum (panel variant);
'pess' / 'opt' select the worst / best element of the response set for S.

TU: v(S) = sup_{a_S} sel_{a_C in E_C(a_S)} sum_S u;  core by the least-core LP, empty cases certified by the
Bondareva-Shapley dual (a balanced collection re-checked in exact rationals).
NTU: a profile is blocked by S iff some commitment makes every member strictly better under the selected
response; the NTU core is the set of unblocked profiles (no transfers).

Sections: A. LP utilities.  B. Finite games (the catalogue).  C. Cournot.  D. Homogeneous Bertrand.
E. Public goods.  F. Quadratic games (linear-quadratic supermodular; differentiated Bertrand).
G. Allocation games (exchange economies).  H. Generic per-point evaluation.  I. Sweep driver.
"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import itertools
import json
import math
import os
import sys
import time
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog, minimize, minimize_scalar, brentq

TOL = 1e-9


# =============================================================== A. LP utilities
def members(mask, n):
    return [i for i in range(n) if mask >> i & 1]


def proper(n):
    return list(range(1, (1 << n) - 1))


def full(n):
    return (1 << n) - 1


def popcount(m):
    return bin(m).count('1')


def tu_core(v, n, tol=TOL):
    """v: dict mask -> value including the full mask.  Returns verdict, least-core value eps*, the least-core
    allocation, the Bondareva-Shapley gap (max balanced sum - v(N)) and, if empty, the balanced collection."""
    F = full(n)
    Ss = proper(n)
    scale = max(abs(v[F]), 1.0)
    A = [[-1.0 if m >> i & 1 else 0.0 for i in range(n)] + [1.0] for m in Ss]
    b = [-v[m] for m in Ss]
    r = linprog(c=[0.0] * n + [-1.0], A_ub=A, b_ub=b, A_eq=[[1.0] * n + [0.0]], b_eq=[v[F]],
                bounds=[(None, None)] * (n + 1), method='highs')
    assert r.status == 0, r.message
    x = r.x[:n]
    eps = r.x[-1]
    r2 = linprog(c=[-v[m] for m in Ss], A_eq=[[1.0 if m >> i & 1 else 0.0 for m in Ss] for i in range(n)],
                 b_eq=[1.0] * n, bounds=[(0, None)] * len(Ss), method='highs')
    assert r2.status == 0, r2.message
    beta = -r2.fun
    gap = beta - v[F]
    if eps >= tol * scale:
        verdict = 'nonempty'
    elif eps > -tol * scale:
        verdict = 'tight'
    else:
        verdict = 'empty'
    out = dict(verdict=verdict, eps=float(eps), scale=scale, alloc=[float(t) for t in x],
               min_slack=float(min(sum(x[i] for i in members(m, n)) - v[m] for m in Ss)), gap=float(gap))
    if verdict == 'empty':
        coll = []
        for m, lam in zip(Ss, r2.x):
            if lam > 1e-9:
                coll.append((m, Fraction(lam).limit_denominator(1000)))
        exact = all(sum((lam for m, lam in coll if m >> i & 1), Fraction(0)) == 1 for i in range(n))
        gap_exact = sum(float(lam) * v[m] for m, lam in coll) - v[F]
        out['collection'] = [[members(m, n), str(lam)] for m, lam in coll]
        out['collection_balanced_exact'] = bool(exact)
        out['collection_gap'] = float(gap_exact)
    return out


def symmetric_equal_split_ok(v, n, tol=TOL):
    """Symmetric games: the core is nonempty iff the equal split meets every constraint."""
    F = full(n)
    return min(popcount(m) * v[F] / n - v[m] for m in proper(n))


# =============================================================== B. Finite games
class FiniteGame:
    """n-player pure normal form.  acts[i] = list of action labels; pay(profile tuple of indices) -> payoffs."""

    def __init__(self, name, acts, pay):
        self.name = name
        self.n = len(acts)
        self.acts = acts
        self.k = [len(a) for a in acts]
        self.U = np.zeros(tuple(self.k) + (self.n,))
        for prof in itertools.product(*[range(k) for k in self.k]):
            self.U[prof] = pay(prof)

    def u(self, prof):
        return self.U[tuple(prof)]

    def _profiles(self, idx):
        return itertools.product(*[range(self.k[i]) for i in idx])

    def responses(self, S, aS, mode='ind'):
        """Response set of the complement to S's commitment aS (dict i -> action index)."""
        C = [i for i in range(self.n) if not S >> i & 1]
        out = []
        cand = list(self._profiles(C))
        def prof_of(aC):
            p = [0] * self.n
            for i, a in aS.items():
                p[i] = a
            for i, a in zip(C, aC):
                p[i] = a
            return p
        if mode == 'coord':
            vals = [sum(self.u(prof_of(aC))[j] for j in C) for aC in cand]
            best = max(vals)
            return [prof_of(aC) for aC, val in zip(cand, vals) if val >= best - 1e-12]
        for aC in cand:
            p = prof_of(aC)
            ok = True
            for pos, j in enumerate(C):
                uj = self.u(p)[j]
                for b in range(self.k[j]):
                    q = list(p)
                    q[j] = b
                    if self.u(q)[j] > uj + 1e-12:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                out.append(p)
        return out

    def leader(self, S, mode='ind', sel='pess'):
        """TU leader value with the realizing outcome(s)."""
        Sm = members(S, self.n)
        best, arg, noresp = -np.inf, [], 0
        for aS in self._profiles(Sm):
            d = dict(zip(Sm, aS))
            R = self.responses(S, d, mode)
            if not R:
                noresp += 1
                continue
            vals = [sum(self.u(p)[i] for i in Sm) for p in R]
            val = min(vals) if sel == 'pess' else max(vals)
            outs = [p for p, x in zip(R, vals) if abs(x - val) < 1e-12]
            if val > best + 1e-12:
                best, arg = val, outs
            elif abs(val - best) <= 1e-12:
                arg = arg + outs
        return dict(v=float(best), outcomes=arg, no_response=noresp)

    def blocks(self, S, z, mode='ind', sel='pess'):
        Sm = members(S, self.n)
        for aS in self._profiles(Sm):
            R = self.responses(S, dict(zip(Sm, aS)), mode)
            if not R:
                continue
            good = [all(self.u(p)[i] > z[i] + 1e-12 for i in Sm) for p in R]
            if (sel == 'pess' and all(good)) or (sel == 'opt' and any(good)):
                return True
        return False

    def tu(self, mode='ind', sel='pess'):
        n = self.n
        v = {S: self.leader(S, mode, sel)['v'] for S in proper(n)}
        v[full(n)] = float(max(self.U.sum(axis=-1).ravel()))
        return v

    def ntu_core(self, mode='ind', sel='pess'):
        n = self.n
        core = []
        for prof in self._profiles(range(n)):
            z = self.u(prof)
            if any((self.U.reshape(-1, n) > z + 1e-12).all(axis=1)):
                continue
            if any(self.blocks(S, z, mode, sel) for S in proper(n)):
                continue
            core.append(tuple(prof))
        return core

    def sim(self, S, sel='pess'):
        """Simultaneous partition: S as one player against singletons; pure equilibria; S's sum (pess/opt)."""
        n = self.n
        Sm = members(S, n)
        C = [i for i in range(n) if not S >> i & 1]
        vals = []
        for prof in self._profiles(range(n)):
            u = self.u(prof)
            uS = sum(u[i] for i in Sm)
            ok = True
            for aS in self._profiles(Sm):
                q = list(prof)
                for i, a in zip(Sm, aS):
                    q[i] = a
                if sum(self.u(q)[i] for i in Sm) > uS + 1e-12:
                    ok = False
                    break
            if ok:
                for j in C:
                    for b in range(self.k[j]):
                        q = list(prof)
                        q[j] = b
                        if self.u(q)[j] > u[j] + 1e-12:
                            ok = False
                            break
                    if not ok:
                        break
            if ok:
                vals.append(uS)
        if not vals:
            return None
        return float(min(vals) if sel == 'pess' else max(vals))

    def follower_value(self, S, mode='ind', sel='pess'):
        """v_F(S): S's payoff at the outcome realizing v(C) with C leading (ties in S's favour)."""
        C = full(self.n) ^ S
        L = self.leader(C, mode, sel)
        Sm = members(S, self.n)
        return float(max(sum(self.u(p)[i] for i in Sm) for p in L['outcomes']))


def two_player(name, acts, table):
    """table[a][b] = (u1, u2)."""
    return FiniteGame(name, [acts, acts], lambda p: table[p[0]][p[1]])


def symmetric_2x2(name, acts, row):
    """row[a][b] = row player's payoff; symmetric game."""
    return two_player(name, acts, [[(row[a][b], row[b][a]) for b in range(len(acts))] for a in range(len(acts))])


def catalogue():
    g = {}
    # PD: actions [C, D]; C/C 0, C/D -2, D/C 1, D/D -1
    g['PD'] = symmetric_2x2('PD', ['C', 'D'], [[0, -2], [1, -1]])
    # chicken: [Straight, Swerve]; St/St -10, St/Sw 2, Sw/St -1, Sw/Sw 0
    g['chicken'] = symmetric_2x2('chicken', ['St', 'Sw'], [[-10, 2], [-1, 0]])
    g['hd3'] = symmetric_2x2('hd3', ['H', 'D'], [[-0.5, 2], [0, 1]])
    g['hd6'] = symmetric_2x2('hd6', ['H', 'D'], [[-2, 2], [0, 1]])
    dem = [Fraction(k, 6) for k in range(1, 6)]
    g['dollar5'] = two_player('dollar5', [str(d) for d in dem],
                              [[(float(a), float(b)) if a + b <= 1 else (0.0, 0.0) for b in dem] for a in dem])
    # SOG one-shot: boss wage in {0, 1/4, 1/2}; worker work / strike; work -> (1 - s, s), strike -> (0, 0)
    wages = [0.0, 0.25, 0.5]
    g['SOG'] = FiniteGame('SOG', [['0', '1/4', '1/2'], ['work', 'strike']],
                          lambda p: (1 - wages[p[0]], wages[p[0]]) if p[1] == 0 else (0.0, 0.0))
    g['dollar3'] = FiniteGame('dollar3', [list(range(9))] * 3, dollar3_payoff)
    return g


def dollar3_payoff(prof):
    """Three-player majority divide-the-dollar as in src/dollar3.py (payoffs as fractions of 1).
    Local action l = 3*pi + d: pi in {0, 1} the slot's two others in increasing order, 2 = ALL; d -> demand 2,3,4 sixths."""
    ALL = 3
    ps, ds = [], []
    for s, l in enumerate(prof):
        others = [t for t in range(3) if t != s]
        pi = l // 3
        ps.append(others[pi] if pi < 2 else ALL)
        ds.append(2 + l % 3)
    u = [0, 0, 0]
    if all(p == ALL for p in ps):
        if sum(ds) <= 6:
            u = list(ds)
        return tuple(x / 6 for x in u)
    for s in range(3):
        t = ps[s]
        if t != ALL and t > s and ps[t] == s:
            if ds[s] + ds[t] <= 6:
                u[s], u[t] = ds[s], ds[t]
            return tuple(x / 6 for x in u)
    return (0.0, 0.0, 0.0)


def catalogue_report():
    out = {}
    for name, G in catalogue().items():
        rec = {}
        for sel in ('pess', 'opt'):
            v = G.tu('ind', sel)
            core = G.ntu_core('ind', sel)
            tu = tu_core(v, G.n)
            fma = {}
            for S in proper(G.n):
                fma[str(members(S, G.n))] = v[S] - G.follower_value(S, 'ind', sel)
            rec[sel] = dict(v={str(members(S, G.n)): v[S] for S in v}, tu=tu,
                            ntu_core=[[G.acts[i][a] for i, a in enumerate(p)] for p in core],
                            fma=fma, any_fma=any(x > TOL for x in fma.values()))
        out[name] = rec
    return out


# =============================================================== C. Cournot (p = a - Q, constant marginal costs)
class Unit:
    """A producing unit (one firm, or a merged coalition acting as one) with merit-order costs and capacities.
    G(p): the unit's Cournot best-response quantity written as a function of the market price p, from
    p - q = MC(q) (valid for one firm and for a merged unit, since both maximize q(p_res - q) - Cost(q))."""

    def __init__(self, costs, caps, idx):
        o = np.argsort(costs, kind='stable')
        self.idx = [idx[i] for i in o]
        self.c = [float(costs[i]) for i in o]
        self.k = [float(caps[i]) for i in o]
        self.K = np.cumsum([0.0] + self.k)

    def G(self, p):
        for l, c in enumerate(self.c):
            lo, hi = self.K[l], self.K[l + 1]
            if p <= lo + c:
                return lo
            if p <= hi + c:
                return p - c
        return self.K[-1]

    def kinks(self):
        out = []
        for l, c in enumerate(self.c):
            if not np.isfinite(self.K[l]):
                break
            out.append(self.K[l] + c)
            if np.isfinite(self.K[l + 1]):
                out.append(self.K[l + 1] + c)
        return out

    def cost(self, Q):
        """Merit-order cost of producing Q, and the allocation over members (equal-cost members share)."""
        rem, tot, alloc = Q, 0.0, {}
        cs = self.c
        l = 0
        while rem > 1e-15 and l < len(cs):
            same = [j for j in range(l, len(cs)) if abs(cs[j] - cs[l]) < 1e-15]
            capg = sum(self.k[j] for j in same)
            take = min(rem, capg)
            for j in same:
                share = self.k[j] / capg if np.isfinite(capg) else 1.0 / len(same)
                alloc[self.idx[j]] = alloc.get(self.idx[j], 0.0) + take * share
            tot += take * cs[l]
            rem -= take
            l = same[-1] + 1
        return tot, alloc


class Cournot:
    def __init__(self, costs, caps=None, a=1.0):
        self.n = len(costs)
        self.c = np.array(costs, float)
        self.k = np.full(self.n, np.inf) if caps is None else np.array(caps, float)
        self.a = a
        self.name = 'cournot'

    def units(self, idx, mode):
        if not idx:
            return []
        if mode == 'coord':
            return [Unit(self.c[idx], self.k[idx], idx)]
        return [Unit(self.c[[i]], self.k[[i]], [i]) for i in idx]

    def price_fn(self, followers):
        """Exact piecewise-linear p(Q_S): solves p + sum_u G_u(p) = a - Q_S."""
        kinks = sorted(set(k for u in followers for k in u.kinks()))
        pts = [-10.0] + kinks + [self.a + 10.0]
        Fv = [p + sum(u.G(p) for u in followers) for p in pts]
        def price(QS):
            y = self.a - QS
            if y <= Fv[0]:
                return pts[0] + (y - Fv[0])
            for j in range(len(pts) - 1):
                f0, f1 = Fv[j], Fv[j + 1]
                if f0 <= y <= f1:
                    return pts[j] + (y - f0) * (pts[j + 1] - pts[j]) / (f1 - f0) if f1 > f0 else pts[j]
            return pts[-1] + (y - Fv[-1])
        Qkinks = [self.a - f for f in Fv[1:-1]]
        return price, Qkinks

    def leader(self, S, mode='ind', sel='pess'):
        """Exact: S's joint profit is concave quadratic on each piece between price and cost kinks."""
        n = self.n
        Sm = members(S, n)
        Cm = [i for i in range(n) if not S >> i & 1]
        fol = self.units(Cm, mode)
        price, Qk = self.price_fn(fol)
        uS = Unit(self.c[Sm], self.k[Sm], Sm)
        Qmax = min(uS.K[-1], self.a + 1.0)
        bps = sorted(set([0.0, Qmax] + [q for q in Qk if 0 < q < Qmax] + [x for x in uS.K[1:-1] if 0 < x < Qmax]))
        best, bestQ = -np.inf, 0.0
        for q0, q1 in zip(bps, bps[1:]):
            cands = [q0, q1]
            p0, p1 = price(q0), price(q1)
            s = (p1 - p0) / (q1 - q0)
            mc = (uS.cost(q1)[0] - uS.cost(q0)[0]) / (q1 - q0)
            if s < -1e-15:
                qv = (mc - p0 + s * q0) / (2 * s)
                if q0 < qv < q1:
                    cands.append(qv)
            for q in cands:
                r = q * price(q) - uS.cost(q)[0]
                if r > best + 1e-15:
                    best, bestQ = r, q
        x = self.outcome(bestQ, uS, fol, price)
        return dict(v=float(best), x=x, u=self.payoffs(x), QS=bestQ)

    def outcome(self, QS, uS, fol, price):
        p = price(QS)
        x = np.zeros(self.n)
        for i, q in uS.cost(QS)[1].items():
            x[i] = q
        for u in fol:
            for i, q in u.cost(u.G(p))[1].items():
                x[i] = q
        return x

    def payoffs(self, x):
        x = np.asarray(x, float)
        Q = x.sum(axis=-1, keepdims=True)
        return x * (self.a - Q - self.c)

    def vN(self):
        return self.leader(full(self.n))

    def sim(self, S, sel='pess'):
        """S as one merged firm vs singletons, simultaneous Cournot (unique equilibrium)."""
        Sm = members(S, self.n)
        Cm = [i for i in range(self.n) if not S >> i & 1]
        uS = Unit(self.c[Sm], self.k[Sm], Sm)
        allu = [uS] + self.units(Cm, 'ind')
        F = lambda p: p + sum(u.G(p) for u in allu) - self.a
        p = brentq(F, -10, self.a + 10, xtol=1e-15, rtol=1e-15)
        q = uS.G(p)
        return float(q * p - uS.cost(q)[0])

    # ---- NTU (uncapacitated)
    def block_margin(self, S, z, mode='ind', ngrid=4000):
        """B_S(z) = max over Q_S of max-min_i (pi_i - z_i) = max_Q (Q - sum z/m)/sum(1/m), m_i = p(Q) - c_i."""
        Sm = members(S, self.n)
        if len(Sm) == 1:
            return self.leader(S, mode)['v'] - z[Sm[0]]
        Cm = [i for i in range(self.n) if not S >> i & 1]
        price, Qk = self.price_fn(self.units(Cm, mode))
        zS, cS = np.asarray(z)[Sm], self.c[Sm]
        def t(Q):
            m = price(Q) - cS
            if np.any(m <= 0):
                return -np.inf
            return (Q - np.sum(zS / m)) / np.sum(1.0 / m)
        Qs = np.linspace(0, self.a, ngrid)
        vals = np.array([t(Q) for Q in Qs])
        j = int(np.argmax(vals))
        if not np.isfinite(vals[j]):
            return -np.inf
        lo, hi = Qs[max(j - 1, 0)], Qs[min(j + 1, ngrid - 1)]
        r = minimize_scalar(lambda Q: -t(Q), bounds=(lo, hi), method='bounded', options=dict(xatol=1e-13))
        return float(max(vals[j], -r.fun))

    def ntu_core(self, mode='ind', nQS=200, depth=40, tol=1e-10):
        """Exact-relaxation method (notes §4.1): at grand total Q the candidate payoff vectors are z >= 0 with
        sum z_i/mu_i(Q) = Q, mu_i = a - c_i - Q, and non-blocking by S is linear in z for each Q_S.  An interval
        relaxation in Q plus a Q_S grid gives certified emptiness; a found z is verified with exact B_S."""
        n = self.n
        vs = np.array([self.leader(1 << i, mode)['v'] for i in range(n)])
        rows = []
        for S in proper(n):
            Sm = members(S, n)
            if len(Sm) < 2:
                continue
            Cm = [i for i in range(n) if not S >> i & 1]
            price, _ = self.price_fn(self.units(Cm, mode))
            for QS in np.linspace(0, self.a, nQS):
                m = price(QS) - self.c[Sm]
                if np.all(m > 0):
                    r = np.zeros(n + 1)
                    r[Sm] = -1.0 / m
                    r[-1] = np.sum(1.0 / m)
                    rows.append((r, -QS))
        base_A = [np.r_[-np.eye(n)[i], 1.0] for i in range(n)] + [r for r, _ in rows]
        base_b = [-vs[i] for i in range(n)] + [b for _, b in rows]
        def lp(Qa, Qb):
            mua, mub = self.a - self.c - Qa, self.a - self.c - Qb
            mua = np.where(mua > 1e-9, mua, 0.0)
            mub = np.where(mub > 1e-9, mub, 0.0)
            if np.all(mua <= 0):
                return -np.inf, None
            A, b = list(base_A), list(base_b)
            bounds = [(0, 0) if mua[i] <= 0 else (0, None) for i in range(n)] + [(None, 1.0)]
            ia = np.where(mua > 0, 1.0 / np.maximum(mua, 1e-300), 0.0)
            Aeq = beq = None
            if Qa == Qb:
                Aeq, beq = [list(ia) + [0.0]], [Qa]
            else:
                A.append(np.r_[ia, 0.0]); b.append(Qb)                  # sum z/mu(Qa) <= Q <= Qb
                if not np.any((mua > 0) & (mub <= 0)):                    # else 1/mu(Qb) = inf: drop (relaxes)
                    ib = 1.0 / np.maximum(mub, 1e-300) * (mub > 0)
                    A.append(np.r_[-ib, 0.0]); b.append(-Qa)              # sum z/mu(Qb) >= Q >= Qa
            r = linprog(np.r_[np.zeros(n), -1.0], A_ub=np.array(A), b_ub=np.array(b), A_eq=Aeq, b_eq=beq,
                        bounds=bounds, method='highs')
            if r.status == 2:
                return -np.inf, None
            assert r.status == 0, r.message
            return -r.fun, r.x[:n]
        brk = sorted(set([0.0, self.a] + [float(self.a - c) for c in self.c if 0 < self.a - c < self.a]))
        best = [-np.inf, None, None]
        cnt = [0]
        def point(q):
            cnt[0] += 1
            s_pt, zpt = lp(q, q)
            if zpt is not None and s_pt > best[0]:
                best[:] = [s_pt, q, zpt]
            return s_pt
        def verify():
            if best[0] < -tol or best[2] is None:
                return None
            z = best[2]
            marg = [vs[i] - z[i] for i in range(n)] + \
                   [self.block_margin(S, z, mode) for S in proper(n) if popcount(S) >= 2]
            if max(marg) <= 1e-9:
                return dict(verdict='nonempty' if max(marg) < -1e-9 else 'tight', Q=best[1],
                            z=[float(t) for t in z], max_margin=float(max(marg)), nlp=cnt[0])
            return None
        # 1. direct maximization of the point slack on each base interval
        for q0, q1 in zip(brk, brk[1:]):
            for q in np.linspace(q0, q1, 41)[1:-1]:
                point(q)
            if best[1] is not None and q0 < best[1] < q1:
                h = (q1 - q0) / 40
                lo, hi = max(q0, best[1] - h), min(q1, best[1] + h)
                minimize_scalar(lambda q: -max(point(q), -1e9), bounds=(lo, hi), method='bounded',
                                options=dict(xatol=1e-14))
        out = verify()
        if out:
            return out
        # 2. certification by best-first interval bisection
        import heapq
        heap = []
        for q0, q1 in zip(brk, brk[1:]):
            s_rel, _ = lp(q0, q1)
            cnt[0] += 1
            if s_rel >= -tol:
                heapq.heappush(heap, (-s_rel, q0, q1, 0))
        unresolved = 0
        while heap:
            _, q0, q1, d = heapq.heappop(heap)
            qm = 0.5 * (q0 + q1)
            point(qm)
            out = verify()
            if out:
                return out
            if d >= depth or cnt[0] > 20000:
                unresolved += 1
                continue
            for a_, b_ in ((q0, qm), (qm, q1)):
                s_rel, _ = lp(a_, b_)
                cnt[0] += 1
                if s_rel >= -tol:
                    heapq.heappush(heap, (-s_rel, a_, b_, d + 1))
        nlp = cnt[0]
        sb = bool(vs.sum() > self.vN()['v'] + 1e-12)
        if unresolved:
            return dict(verdict='unresolved', best_point_slack=float(best[0]), nlp=nlp,
                        unresolved_intervals=unresolved, singleton_bound=sb)
        return dict(verdict='empty', best_point_slack=float(best[0]), nlp=nlp, singleton_bound=sb)


# =============================================================== D. Homogeneous Bertrand
class HomBertrand:
    """Demand 1 - p; the lowest price serves the whole market; ties split equally.  Continuous prices: a
    complement firm facing a higher leader price undercuts by an arbitrarily small amount, so its best reply is
    not attained; leader values are suprema (the limit of a price grid with tick -> 0), flagged 'unattained'."""

    def __init__(self, costs, a=1.0):
        self.n = len(costs)
        self.c = np.array(costs, float)
        self.a = a
        self.name = 'hombertrand'

    def limit(self, cS, cC):
        if cS >= cC - 1e-15:
            return 0.0, True
        pm = (self.a + cS) / 2
        p = min(pm, cC)
        return (p - cS) * (self.a - p), pm < cC

    def leader(self, S, mode='ind', sel='pess'):
        Sm = members(S, self.n)
        Cm = [i for i in range(self.n) if not S >> i & 1]
        cS = self.c[Sm].min()
        if not Cm:
            v, att = (self.a - cS) ** 2 / 4, True
            p = (self.a + cS) / 2
        else:
            cC = self.c[Cm].min()
            v, att = self.limit(cS, cC)
            if sel == 'opt' and cS < cC:
                att = True       # the indifferent complement firm prices above: the supremum is attained
            p = min((self.a + cS) / 2, cC)
        x = np.zeros(self.n)
        win = [i for i in Sm if self.c[i] <= cS + 1e-15]
        u = np.zeros(self.n)
        if v > 0:
            for i in win:
                u[i] = v / len(win)
        return dict(v=float(v), u=u, attained=bool(att), price=float(p))

    def vN(self):
        return self.leader(full(self.n))

    def sim(self, S, sel='pess'):
        Sm = members(S, self.n)
        Cm = [i for i in range(self.n) if not S >> i & 1]
        return float(self.limit(self.c[Sm].min(), self.c[Cm].min())[0])

    def ntu_core(self, mode='ind', sel='pess'):
        """Analytic certificate (notes §4.2): the min-cost firms price at the monopoly price and share; every
        coalition either lacks a min-cost firm (leader value 0 under pess) or contains all of them (its total is
        at most the monopoly profit they already share)."""
        cmin = self.c.min()
        tied = [i for i in range(self.n) if self.c[i] <= cmin + 1e-15]
        z = np.zeros(self.n)
        z[tied] = (self.a - cmin) ** 2 / 4 / len(tied)
        worst = -np.inf
        for S in proper(self.n):
            Sm = members(S, self.n)
            L = self.leader(S, mode, sel)
            # S blocks only if its total can exceed z(S) and every member can get strictly more; a member that
            # is not among S's cheapest earns 0 in any outcome where S's cheapest sells (it would undercut).
            if L['v'] <= z[Sm].sum() + 1e-15:
                continue
            worst = max(worst, L['v'] - z[Sm].sum())
        return dict(verdict='nonempty' if worst == -np.inf else 'check', z=[float(t) for t in z])


# =============================================================== E. Public goods
PG_F = {
    'sqrt': (lambda G: 2 * np.sqrt(G), lambda th: th ** 2),
    'log': (lambda G: np.log1p(G), lambda th: max(0.0, th - 1.0)),
    'crra05': (lambda G: 2 * (np.sqrt(1 + G) - 1), lambda th: max(0.0, th ** 2 - 1.0)),
    'crra2': (lambda G: 1 - 1 / (1 + G), lambda th: max(0.0, math.sqrt(th) - 1.0)),
}


class PublicGoods:
    """u_i = theta_i f(G) - g_i, g_i >= 0.  Given S's total G_S the complement's equilibrium total is
    max(G_S, G*(theta_top)) (only its largest valuation, or under 'coord' its summed valuation, tops up)."""

    def __init__(self, theta, f):
        self.n = len(theta)
        self.th = np.array(theta, float)
        self.fname = f
        self.f, self.Gs = PG_F[f]
        self.name = 'pg'

    def take(self, thS, GC):
        G = max(self.Gs(thS), GC)
        return thS * self.f(G) - G, G

    def GC(self, Cm, mode):
        if not Cm:
            return 0.0
        thc = self.th[Cm].sum() if mode == 'coord' else self.th[Cm].max()
        return self.Gs(thc)

    def leader(self, S, mode='ind', sel='pess'):
        Sm = members(S, self.n)
        Cm = [i for i in range(self.n) if not S >> i & 1]
        thS = self.th[Sm].sum()
        GC = self.GC(Cm, mode)
        ride = thS * self.f(GC) if Cm else -np.inf
        tk, Gt = self.take(thS, GC)
        g = np.zeros(self.n)
        if Cm and ride >= tk:
            v, G = ride, GC
            if GC > 0:
                if mode == 'coord':
                    g[Cm] = GC / len(Cm)
                else:
                    top = [j for j in Cm if self.th[j] >= self.th[Cm].max() - 1e-15]
                    g[top] = GC / len(top)
            kind = 'ride'
        else:
            v, G = tk, Gt
            g[Sm] = G / len(Sm)
            kind = 'take'
        return dict(v=float(v), x=g, u=self.payoffs(g), kind=kind, G=float(G))

    def payoffs(self, g):
        g = np.asarray(g, float)
        G = g.sum(axis=-1, keepdims=True)
        return self.th * self.f(G) - g

    def vN(self):
        return self.leader(full(self.n))

    def sim(self, S, sel='pess'):
        Sm = members(S, self.n)
        Cm = [i for i in range(self.n) if not S >> i & 1]
        thS, thC = self.th[Sm].sum(), self.th[Cm].max()
        top = max(thS, thC)
        G = self.Gs(top)
        if thS > thC + 1e-12:
            return float(thS * self.f(G) - G)
        if thS < thC - 1e-12:
            return float(thS * self.f(G))
        return float(thS * self.f(G) - G) if sel == 'pess' else float(thS * self.f(G))

    def block_margin(self, S, z, mode='ind', ngrid=3000):
        """B_S(z): max over S's total G_S of the water-filling max-min margin (vectorized over a G_S grid,
        then refined).  For a given G_S the members' margins a_i = theta_i f(G) - z_i are filled to the level
        tau = max_k (sum of the k largest a - G_S)/k, capped by min a (contributions are nonnegative)."""
        Sm = members(S, self.n)
        Cm = [i for i in range(self.n) if not S >> i & 1]
        zS, thS = np.asarray(z, float)[Sm], self.th[Sm]
        GC = self.GC(Cm, mode)
        Gmax = self.Gs(self.th.sum()) * 4 + 10
        def tvec(GS):
            GS = np.atleast_1d(np.asarray(GS, float))
            G = np.maximum(GS, GC)
            a = thS[None, :] * self.f(G)[:, None] - zS[None, :]
            srt = -np.sort(-a, axis=1)
            cs = np.cumsum(srt, axis=1)
            k = np.arange(1, len(Sm) + 1)[None, :]
            tau = ((cs - GS[:, None]) / k).max(axis=1)
            return np.minimum(a.min(axis=1), tau)
        Gs = np.unique(np.r_[0.0, np.linspace(0, Gmax, ngrid), GC, np.geomspace(1e-6, Gmax, 400)])
        vals = tvec(Gs)
        j = int(np.argmax(vals))
        best = vals[j]
        lo, hi = Gs[max(j - 1, 0)], Gs[min(j + 1, len(Gs) - 1)]
        if hi > lo:
            r = minimize_scalar(lambda x: -tvec(x)[0], bounds=(lo, hi), method='bounded', options=dict(xatol=1e-13))
            best = max(best, -r.fun)
        return float(best)

    def tu_profile(self, v, ngrid=200):
        """Search for a profile whose payoff vector meets every TU leader value (implies NTU nonempty).
        For fixed G the slack is an LP; its value is concave in G (notes §4.3), maximized by golden section."""
        n = self.n
        Ss = proper(n)
        def lpG(G):
            W = self.th.sum() * self.f(G) - G
            cap = self.th * self.f(G)
            A = [np.r_[-np.array([1.0 if S >> i & 1 else 0.0 for i in range(n)]), 1.0] for S in Ss]
            b = [-v[S] for S in Ss]
            A.append(np.r_[np.ones(n), 0.0]); b.append(W)
            r = linprog(np.r_[np.zeros(n), -1.0], A_ub=np.array(A), b_ub=np.array(b),
                        bounds=[(None, cap[i]) for i in range(n)] + [(None, None)], method='highs')
            if r.status != 0:
                return -np.inf, None
            return -r.fun, r.x[:n]
        GN = self.Gs(self.th.sum())
        hi = max(4 * GN, 1.0)
        Gg = np.linspace(0, hi, ngrid)
        vals = [lpG(G)[0] for G in Gg]
        j = int(np.argmax(vals))
        r = minimize_scalar(lambda G: -lpG(G)[0], bounds=(Gg[max(j - 1, 0)], Gg[min(j + 1, ngrid - 1)]),
                            method='bounded', options=dict(xatol=1e-12))
        Gb = r.x if -r.fun > vals[j] else Gg[j]
        s, z = lpG(Gb)
        return float(s), Gb, z


# =============================================================== F. Quadratic games
class QuadGame:
    """u_i(x) = x'H_i x/2 + g_i'x + k_i, lower bounds lb (-inf = none).  Every block (a player or a coalition
    acting as one) maximizes its summed payoff over its own variables; equilibria by KKT with active-set
    enumeration (exact for block-concave games).  Leader values are exact when the followers' response has a
    fixed active set (always interior here under 'ind'); otherwise a numerical fallback is used and flagged."""

    def __init__(self, H, g, k, lb, name):
        self.H = np.array(H, float)
        self.g = np.array(g, float)
        self.k = np.array(k, float)
        self.lb = np.array(lb, float)
        self.n = len(k)
        self.name = name
        self.flags = set()

    def payoffs(self, x):
        x = np.asarray(x, float)
        quad = 0.5 * np.einsum('...a,iab,...b->...i', x, self.H, x)
        return quad + x @ self.g.T + self.k

    def _rows(self, blocks):
        rows, rhs = {}, {}
        for B in blocks:
            Hb = self.H[B].sum(axis=0)
            gb = self.g[B].sum(axis=0)
            for j in B:
                rows[j] = Hb[j]
                rhs[j] = -gb[j]
        return rows, rhs

    def equilibrium(self, blocks, fixed=None):
        """All KKT points with the variables of `fixed` (dict idx -> value) held."""
        fixed = fixed or {}
        n = self.n
        rows, rhs = self._rows(blocks)
        free = sorted(rows)
        bnd = [j for j in free if np.isfinite(self.lb[j])]
        sols = []
        for r in range(len(bnd) + 1):
            for A in itertools.combinations(bnd, r):
                M = np.zeros((n, n))
                y = np.zeros(n)
                for j in range(n):
                    if j in fixed:
                        M[j, j] = 1; y[j] = fixed[j]
                    elif j in A:
                        M[j, j] = 1; y[j] = self.lb[j]
                    else:
                        M[j] = rows[j]; y[j] = rhs[j]
                try:
                    x = np.linalg.solve(M, y)
                except np.linalg.LinAlgError:
                    continue
                ok = True
                for j in free:
                    if j in A:
                        if rows[j] @ x - rhs[j] > 1e-10:
                            ok = False
                    elif x[j] < self.lb[j] - 1e-10:
                        ok = False
                if ok:
                    sols.append(x)
        return sols

    def affine_response(self, S, mode):
        """x_C = R x_S + r for the interior follower response (no follower at a bound)."""
        n = self.n
        Sm = members(S, n)
        Cm = [i for i in range(n) if not S >> i & 1]
        blocks = [Cm] if mode == 'coord' else [[j] for j in Cm]
        rows, rhs = self._rows(blocks)
        A = np.array([rows[j][Cm] for j in Cm])
        Bm = np.array([rows[j][Sm] for j in Cm])
        b = np.array([rhs[j] for j in Cm])
        Ainv = np.linalg.inv(A)
        R = -Ainv @ Bm
        r = Ainv @ b
        P = np.zeros((n, len(Sm)))
        p0 = np.zeros(n)
        for a, i in enumerate(Sm):
            P[i, a] = 1
        for a, j in enumerate(Cm):
            P[j] = R[a]
            p0[j] = r[a]
        return P, p0

    def induced(self, S, mode, who=None):
        """S's summed payoff (or member list `who`) as a quadratic in x_S under the affine response."""
        P, p0 = self.affine_response(S, mode)
        idx = members(S, self.n) if who is None else who
        Hs = self.H[idx].sum(axis=0)
        gs = self.g[idx].sum(axis=0)
        Q = P.T @ Hs @ P
        q = P.T @ (Hs @ p0 + gs)
        c0 = 0.5 * p0 @ Hs @ p0 + gs @ p0 + self.k[idx].sum()
        return Q, q, c0, P, p0

    def leader(self, S, mode='ind', sel='pess'):
        n = self.n
        Sm = members(S, n)
        if S == full(n):
            sols = self.equilibrium([list(range(n))])
            best = max(sols, key=lambda x: self.payoffs(x).sum())
            return dict(v=float(self.payoffs(best).sum()), x=best, u=self.payoffs(best), exact=True)
        Q, q, c0, P, p0 = self.induced(S, mode)
        Q = 0.5 * (Q + Q.T)
        lbS = self.lb[Sm]
        if np.max(np.linalg.eigvalsh(Q)) >= -1e-12:
            self.flags.add('nonconcave_leader')
        best, bx = -np.inf, None
        bnd = [a for a in range(len(Sm)) if np.isfinite(lbS[a])]
        for r in range(len(bnd) + 1):
            for A in itertools.combinations(bnd, r):
                fr = [a for a in range(len(Sm)) if a not in A]
                xs = np.zeros(len(Sm))
                for a in A:
                    xs[a] = lbS[a]
                if fr:
                    try:
                        xs[fr] = np.linalg.solve(Q[np.ix_(fr, fr)], -(q[fr] + Q[np.ix_(fr, list(A))] @ xs[list(A)]))
                    except np.linalg.LinAlgError:
                        continue
                if np.any(xs < lbS - 1e-10):
                    continue
                grad = Q @ xs + q
                if any(grad[a] > 1e-10 for a in A):
                    continue
                val = 0.5 * xs @ Q @ xs + q @ xs + c0
                if val > best:
                    best, bx = val, xs
        x = P @ bx + p0
        valid = all(x[j] >= self.lb[j] - 1e-10 for j in range(n) if not S >> j & 1)
        if not valid:
            return self.leader_numeric(S, mode)
        return dict(v=float(best), x=x, u=self.payoffs(x), exact=True)

    def response(self, S, xS, mode):
        n = self.n
        Sm = members(S, n)
        Cm = [i for i in range(n) if not S >> i & 1]
        blocks = [Cm] if mode == 'coord' else [[j] for j in Cm]
        sols = self.equilibrium(blocks, fixed=dict(zip(Sm, xS)))
        return sols

    def leader_numeric(self, S, mode, starts=12, seed=0):
        """Fallback: maximize S's sum over x_S >= lb with the exact KKT response (flagged)."""
        self.flags.add('numeric_leader')
        n = self.n
        Sm = members(S, n)
        rng = np.random.default_rng(seed)
        def val(xS):
            xS = np.maximum(xS, np.where(np.isfinite(self.lb[Sm]), self.lb[Sm], -np.inf))
            sols = self.response(S, xS, mode)
            if not sols:
                return 1e9, None
            vals = [self.payoffs(x)[Sm].sum() for x in sols]
            return -min(vals), sols[int(np.argmin(vals))]
        best = (np.inf, None)
        for s in range(starts):
            x0 = rng.uniform(0, 2, len(Sm))
            r = minimize(lambda y: val(y)[0], x0, method='Nelder-Mead',
                         options=dict(xatol=1e-10, fatol=1e-12, maxiter=4000))
            if r.fun < best[0]:
                best = (r.fun, r.x)
        f, x = val(best[1])
        return dict(v=float(-f), x=x, u=self.payoffs(x), exact=False)

    def vN(self):
        return self.leader(full(self.n))

    def sim(self, S, sel='pess'):
        Sm = members(S, self.n)
        Cm = [i for i in range(self.n) if not S >> i & 1]
        sols = self.equilibrium([Sm] + [[j] for j in Cm])
        if not sols:
            return None
        vals = [self.payoffs(x)[Sm].sum() for x in sols]
        if len(sols) > 1:
            self.flags.add('sim_multiple')
        return float(min(vals) if sel == 'pess' else max(vals))

    def block_margin(self, S, z, mode='ind', starts=8, seed=0):
        """B_S(z) = max over x_S >= lb of min_{i in S}(u_i - z_i) under the affine response (SLSQP, multi-start)."""
        Sm = members(S, self.n)
        P, p0 = self.affine_response(S, mode)
        lbS = self.lb[Sm]
        def u_of(xS):
            return self.payoffs(P @ xS + p0)[Sm] - np.asarray(z)[Sm]
        rng = np.random.default_rng(seed)
        best = -np.inf
        L = self.leader(S, mode)
        x0s = [L['x'][Sm]] + [rng.uniform(0, 2, len(Sm)) for _ in range(starts)]
        bnds = [(lbS[a] if np.isfinite(lbS[a]) else None, None) for a in range(len(Sm))] + [(None, None)]
        for x0 in x0s:
            y0 = np.r_[x0, u_of(x0).min()]
            cons = [dict(type='ineq', fun=lambda y, a=a: u_of(y[:-1])[a] - y[-1]) for a in range(len(Sm))]
            r = minimize(lambda y: -y[-1], y0, method='SLSQP', bounds=bnds, constraints=cons,
                         options=dict(ftol=1e-13, maxiter=500))
            xs = r.x[:-1]
            if np.all(xs >= np.where(np.isfinite(lbS), lbS, -np.inf) - 1e-9):
                best = max(best, u_of(xs).min())
        return float(best)

    def tu_profile(self, v, starts=12, seed=0):
        """Search x with u_S(x) >= v(S) for every proper S (implies the NTU core is nonempty)."""
        n = self.n
        Ss = proper(n)
        Mmat = np.array([[1.0 if S >> i & 1 else 0.0 for i in range(n)] for S in Ss])
        vv = np.array([v[S] for S in Ss])
        rng = np.random.default_rng(seed)
        xN = self.vN()['x']
        best = (-np.inf, None)
        bnds = [(self.lb[i] if np.isfinite(self.lb[i]) else None, None) for i in range(n)] + [(None, None)]
        for s in range(starts):
            x0 = xN if s == 0 else xN * rng.uniform(0.6, 1.4, n)
            y0 = np.r_[x0, (Mmat @ self.payoffs(x0) - vv).min()]
            cons = [dict(type='ineq', fun=lambda y: Mmat @ self.payoffs(y[:-1]) - vv - y[-1])]
            r = minimize(lambda y: -y[-1], y0, method='SLSQP', bounds=bnds, constraints=cons,
                         options=dict(ftol=1e-14, maxiter=1000))
            sl = (Mmat @ self.payoffs(r.x[:-1]) - vv).min()
            if sl > best[0]:
                best = (sl, r.x[:-1])
        return float(best[0]), best[1]


def lq_game(b, gamma, sigma):
    n = len(b)
    H = np.zeros((n, n, n))
    g = np.zeros((n, n))
    for i in range(n):
        H[i, i, i] = -1.0
        for j in range(n):
            if j != i:
                H[i, i, j] = H[i, j, i] = gamma
                g[i, j] = sigma
        g[i, i] = b[i]
    G = QuadGame(H, g, np.zeros(n), np.zeros(n), 'lq')
    G.params = dict(b=list(b), gamma=gamma, sigma=sigma)
    return G


def bertrand_game(c, gsum):
    """q_i = 1 - p_i + (gsum/(n-1)) sum_{j != i} p_j; profit (p_i - c_i) q_i; prices unbounded."""
    n = len(c)
    gp = gsum / (n - 1)
    H = np.zeros((n, n, n))
    g = np.zeros((n, n))
    for i in range(n):
        H[i, i, i] = -2.0
        for j in range(n):
            if j != i:
                H[i, i, j] = H[i, j, i] = gp
                g[i, j] = -c[i] * gp
        g[i, i] = 1 + c[i]
    G = QuadGame(H, g, -np.array(c, float), np.full(n, -np.inf), 'bertrand')
    G.params = dict(c=list(c), g=gsum)
    G.quantities = lambda p: 1 - np.asarray(p) + gp * (np.sum(p, axis=-1, keepdims=True) - np.asarray(p))
    return G


# =============================================================== G. Allocation games (exchange economies)
class Exchange:
    """The RS's allocation games: each player owns goods and chooses who gets them; utilities depend on the own
    bundle only, with nonnegative marginal utility.  An outsider's credible response to anything is to keep
    (giving away never raises its utility); under 'opt' an outsider indifferent about a good (zero weight)
    gifts it to S.  So v(S) is S's best use of its own endowment (plus, under opt, the complement's worthless
    goods), and the NTU leader-value core is the classical core (pess)."""

    def __init__(self, alpha, omega, util='cd', r=None):
        self.alpha = np.array(alpha, float)
        self.omega = np.array(omega, float)
        self.n, self.m = self.alpha.shape
        self.util = util
        self.r = r
        self.name = 'exchange'

    def u(self, i, x):
        x = np.maximum(np.asarray(x, float), 0.0)
        a = self.alpha[i]
        if self.util == 'cd':
            return float(np.prod(np.where(a > 0, x ** a, 1.0)))
        s = np.sum(np.where(a > 0, a * np.where(x > 0, x, 1e-300) ** self.r, 0.0))
        return float(s ** (1.0 / self.r)) if s > 0 else 0.0

    def resources(self, S, sel):
        Sm = members(S, self.n)
        R = self.omega[Sm].sum(axis=0)
        if sel == 'opt':
            for j in range(self.n):
                if not S >> j & 1:
                    R = R + self.omega[j] * (self.alpha[j] == 0)
        return R

    def best_sum(self, idx, R, weights=None, starts=4, seed=0):
        """max sum_i u_i(y_i) s.t. sum y_i = R, y >= 0 (a concave program; SLSQP from several starts)."""
        k, m = len(idx), self.m
        if k == 1:
            return self.u(idx[0], R), R[None, :]
        rng = np.random.default_rng(seed)
        def unpack(y):
            Y = y.reshape(k - 1, m)
            return np.vstack([Y, R - Y.sum(axis=0)])
        def f(y):
            Y = unpack(y)
            return -sum(self.u(i, Y[a]) for a, i in enumerate(idx))
        cons = [dict(type='ineq', fun=lambda y: unpack(y)[-1] - 1e-12)]
        best = (np.inf, None)
        for s in range(starts):
            w = rng.dirichlet(np.ones(k)) if s else np.full(k, 1.0 / k)
            y0 = (w[:, None] * R[None, :])[:-1].ravel()
            r = minimize(f, y0, method='SLSQP', bounds=[(1e-12, None)] * len(y0), constraints=cons,
                         options=dict(ftol=1e-14, maxiter=2000))
            if r.fun < best[0]:
                best = (r.fun, unpack(r.x))
        return -best[0], best[1]

    def leader(self, S, mode='ind', sel='pess'):
        Sm = members(S, self.n)
        v, Y = self.best_sum(Sm, self.resources(S, sel))
        return dict(v=float(v), alloc=Y)

    def vN(self):
        return self.leader(full(self.n))

    def equilibrium(self):
        """Competitive equilibrium (Walras) of the exchange economy."""
        a, w = self.alpha, self.omega
        Om = w.sum(axis=0)
        if self.util == 'cd':
            M = (a.T @ w) / Om[:, None]                  # p_k Om_k = sum_i a_ik p.w_i
            vals, vecs = np.linalg.eig(M)
            j = int(np.argmin(np.abs(vals - 1)))
            p = np.abs(np.real(vecs[:, j]))
            p = p / p.sum()
        else:
            sig = 1.0 / (1.0 - self.r)
            def excess(lp):
                p = np.exp(np.r_[lp, 0.0])
                inc = w @ p
                D = np.where(a > 0, a, 0.0) ** sig * p[None, :] ** (-sig)
                X = D * (inc / (D * p[None, :]).sum(axis=1))[:, None]
                return (X.sum(axis=0) - Om)[:-1]
            from scipy.optimize import root
            sol = root(excess, np.zeros(self.m - 1), tol=1e-14)
            p = np.exp(np.r_[sol.x, 0.0])
            p = p / p.sum()
        inc = w @ p
        if self.util == 'cd':
            X = a * inc[:, None] / p[None, :]
        else:
            sig = 1.0 / (1.0 - self.r)
            D = np.where(a > 0, a, 0.0) ** sig * p[None, :] ** (-sig)
            X = D * (inc / (D * p[None, :]).sum(axis=1))[:, None]
        return p, X

    def block_margin(self, S, z, sel='pess', starts=3, seed=0):
        """max t s.t. u_i(y_i) >= z_i + t (i in S), sum y = resources(S)."""
        Sm = members(S, self.n)
        R = self.resources(S, sel)
        k, m = len(Sm), self.m
        if k == 1:
            return self.u(Sm[0], R) - z[Sm[0]]
        rng = np.random.default_rng(seed)
        def unpack(y):
            Y = y[:-1].reshape(k - 1, m)
            return np.vstack([Y, R - Y.sum(axis=0)])
        cons = [dict(type='ineq', fun=lambda y: unpack(y)[-1] - 1e-12)] + \
               [dict(type='ineq', fun=lambda y, a=a, i=i: self.u(i, unpack(y)[a]) - z[i] - y[-1])
                for a, i in enumerate(Sm)]
        best = -np.inf
        for s in range(starts):
            w = rng.dirichlet(np.ones(k)) if s else np.full(k, 1.0 / k)
            Y0 = w[:, None] * R[None, :]
            t0 = min(self.u(i, Y0[a]) - z[i] for a, i in enumerate(Sm))
            r = minimize(lambda y: -y[-1], np.r_[Y0[:-1].ravel(), t0], method='SLSQP',
                         bounds=[(1e-12, None)] * ((k - 1) * m) + [(None, None)], constraints=cons,
                         options=dict(ftol=1e-14, maxiter=3000))
            Y = unpack(r.x)
            if np.all(Y >= -1e-9):
                best = max(best, min(self.u(i, Y[a]) - z[i] for a, i in enumerate(Sm)))
        return float(best)

    def tu_profile(self, v, starts=6, seed=0):
        """Search an allocation whose utilities meet every v(S) (implies an NTU core point)."""
        n, m = self.n, self.m
        Ss = proper(n)
        Om = self.omega.sum(axis=0)
        Mmat = np.array([[1.0 if S >> i & 1 else 0.0 for i in range(n)] for S in Ss])
        vv = np.array([v[S] for S in Ss])
        def unpack(y):
            Y = y[:-1].reshape(n - 1, m)
            return np.vstack([Y, Om - Y.sum(axis=0)])
        def us(Y):
            return np.array([self.u(i, Y[i]) for i in range(n)])
        rng = np.random.default_rng(seed)
        best = (-np.inf, None)
        for s in range(starts):
            Y0 = self.equilibrium()[1] if s == 0 else rng.dirichlet(np.ones(n), m).T * Om[None, :]
            t0 = (Mmat @ us(Y0) - vv).min()
            cons = [dict(type='ineq', fun=lambda y: unpack(y)[-1] - 1e-12),
                    dict(type='ineq', fun=lambda y: Mmat @ us(unpack(y)) - vv - y[-1])]
            r = minimize(lambda y: -y[-1], np.r_[Y0[:-1].ravel(), t0], method='SLSQP',
                         bounds=[(1e-12, None)] * ((n - 1) * m) + [(None, None)], constraints=cons,
                         options=dict(ftol=1e-14, maxiter=3000))
            Y = unpack(r.x)
            if np.all(Y >= -1e-9):
                sl = (Mmat @ us(Y) - vv).min()
                if sl > best[0]:
                    best = (sl, Y)
        return float(best[0]), best[1]


# =============================================================== H. Per-point evaluation
def tu_table(G, mode='ind', sel='pess'):
    n = G.n
    L = {S: G.leader(S, mode, sel) for S in proper(n)}
    L[full(n)] = G.vN()
    v = {S: L[S]['v'] for S in L}
    return v, L


def fma_and_dominance(G, v, L):
    """FMA(S) = v(S) - v_F(S) with v_F read off C's leader outcome; follower dominance at S's outcome."""
    n = G.n
    fma, dom = {}, {}
    for S in proper(n):
        C = full(n) ^ S
        Sm, Cm = members(S, n), members(C, n)
        if 'u' in L[C]:
            fma[S] = float(v[S] - L[C]['u'][Sm].sum())
        if 'u' in L[S]:
            uS = L[S]['u']
            dom[S] = bool(np.mean(uS[Cm]) >= np.mean(uS[Sm]) - 1e-12)
    return fma, dom


def evaluate(G, mode='ind', sel='pess', do_sim=True):
    n = G.n
    v, L = tu_table(G, mode, sel)
    rec = dict(n=n, tu=tu_core(v, n), v={str(members(S, n)): v[S] for S in v})
    fma, dom = fma_and_dominance(G, v, L)
    rec['fma'] = {str(members(S, n)): fma[S] for S in fma}
    rec['any_fma'] = bool(any(x > TOL * rec['tu']['scale'] for x in fma.values()))
    rec['follower_dominance'] = {str(members(S, n)): dom[S] for S in dom}
    rec['all_dominance'] = bool(all(dom.values())) if dom else None
    if do_sim and mode == 'ind':
        vs = {S: G.sim(S, sel) for S in proper(n)}
        if all(x is not None for x in vs.values()):
            vs[full(n)] = v[full(n)]
            rec['sim'] = tu_core(vs, n)
            rec['leader_ge_sim'] = bool(all(v[S] >= vs[S] - 1e-9 for S in proper(n)))
    sing = sum(v[1 << i] for i in range(n))
    rec['singleton_bound'] = bool(sing > v[full(n)] + TOL * rec['tu']['scale'])
    return rec, v, L


def ntu_search(G, v, mode, x0s, lb, maxiter=400):
    """Direct search for an unblocked profile: minimize the largest blocking margin (Nelder-Mead from several
    starts).  Finding max margin <= 0 certifies nonemptiness; failure is 'unresolved', never 'empty'."""
    n = G.n
    def worst(x):
        x = np.maximum(x, lb)
        z = G.payoffs(x)
        m = [v[1 << i] - z[i] for i in range(n)]
        if max(m) > 0.05:
            return max(m)
        m += [G.block_margin(S, z, mode) for S in proper(n) if popcount(S) >= 2]
        return max(m)
    best = (np.inf, None)
    for x0 in x0s:
        r = minimize(worst, x0, method='Nelder-Mead', options=dict(maxiter=maxiter, xatol=1e-10, fatol=1e-12))
        if r.fun < best[0]:
            best = (r.fun, np.maximum(r.x, lb))
        if best[0] < -1e-9:
            break
    return float(best[0]), best[1]


def ntu_dispatch(G, rec, v, L, mode='ind', sel='pess', search=True):
    if isinstance(G, Cournot):
        if rec['singleton_bound']:
            return dict(verdict='empty', method='singleton bound')
        out = G.ntu_core(mode)
        out['method'] = 'interval LP (exact relaxation)'
        return out
    if isinstance(G, HomBertrand):
        out = G.ntu_core(mode, sel)
        out['method'] = 'analytic certificate'
        return out
    if rec['singleton_bound']:
        return dict(verdict='empty', method='singleton bound')
    if rec['tu']['verdict'] != 'empty':
        sl, *_ = G.tu_profile(v)
        if sl >= 1e-9:
            return dict(verdict='nonempty', method='TU-core profile', slack=sl)
        if sl > -1e-9:
            return dict(verdict='tight', method='TU-core profile', slack=sl)
    if not search:
        return dict(verdict='unresolved', method='none')
    n = G.n
    if isinstance(G, PublicGoods):
        lb = np.zeros(n)
        x0s = [L[full(n)]['x']] + [L[S]['x'] for S in proper(n)][:6]
    elif isinstance(G, QuadGame):
        lb = np.where(np.isfinite(G.lb), G.lb, -1e9)
        x0s = [L[full(n)]['x']] + [L[S]['x'] for S in proper(n)][:4]
    else:
        return dict(verdict='unresolved', method='none')
    w, x = ntu_search(G, v, mode, x0s, lb)
    if w <= 1e-9:
        return dict(verdict='nonempty' if w < -1e-9 else 'tight', method='direct search', max_margin=w,
                    x=[float(t) for t in x])
    return dict(verdict='unresolved', method='direct search', best_max_margin=w)


# =============================================================== I. Sweep driver
C_GRID = [round(x, 4) for x in np.arange(0, 0.5001, 0.025)]
C_GRID_NTU = [round(x, 4) for x in np.arange(0, 0.5001, 0.05)]
PG_THETA = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
LQ_B = [0.5, 1.0, 1.5, 2.0]
LQ_GN = [0.1, 0.2, 0.3, 0.4]
LQ_SIGMA = [-1.0, -0.5, -0.25, 0.0, 0.25, 0.5]
BE_G = [0.2, 0.4, 0.6, 0.8]
BE_C = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]


def cost_profiles(n, grid):
    return [(0.0,) + c for c in itertools.combinations_with_replacement(grid, n - 1)]


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(x) for k, x in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(x) for x in o]
    if isinstance(o, np.ndarray):
        return [_clean(x) for x in o.tolist()]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def violating_singletons(rec, n):
    coll = rec['tu'].get('collection')
    if not coll:
        return None
    return sorted(len(c[0]) for c in coll) == [1] * n


def job(args):
    """One grid point (top-level for the worker pool)."""
    fam, prm, opts = args
    t0 = time.time()
    if fam == 'cournot':
        G = Cournot(prm['c'], prm.get('k'))
    elif fam == 'hombertrand':
        G = HomBertrand(prm['c'])
    elif fam == 'pg':
        G = PublicGoods(prm['theta'], prm['f'])
    elif fam == 'lq':
        G = lq_game(prm['b'], prm['gamma'], prm['sigma'])
    elif fam == 'bertrand':
        G = bertrand_game(prm['c'], prm['g'])
    elif fam == 'exchange':
        G = Exchange(prm['alpha'], prm['omega'], prm['util'], prm.get('r'))
    else:
        raise ValueError(fam)
    mode, sel = opts.get('mode', 'ind'), opts.get('sel', 'pess')
    rec, v, L = evaluate(G, mode, sel, do_sim=opts.get('sim', True) and fam != 'exchange')
    rec['family'] = fam
    rec['params'] = prm
    rec['mode'], rec['sel'] = mode, sel
    n = G.n
    if rec['tu']['verdict'] == 'empty':
        rec['singleton_collection'] = violating_singletons(rec, n)
    if fam == 'pg':
        rec['kinds'] = {str(members(S, n)): L[S]['kind'] for S in proper(n)}
        if rec['tu']['verdict'] == 'empty':
            rides = []
            for c in rec['tu']['collection']:
                S = sum(1 << i for i in c[0])
                Cm = [i for i in range(n) if not S >> i & 1]
                rides.append(L[S]['kind'] == 'ride' and G.GC(Cm, mode) > 0)
            rec['collection_has_free_rider'] = bool(any(rides))
    if fam == 'lq':
        xs = [L[S]['x'] for S in L] + []
        xmax = float(max(np.max(x) for x in xs))
        g, s = prm['gamma'], prm['sigma']
        rec['spill_class'] = 'positive' if s >= 0 else ('negative' if g * xmax + s <= 0 else 'mixed')
        rec['symmetric'] = len(set(prm['b'])) == 1
        rec['flags'] = sorted(G.flags)
    if fam == 'bertrand':
        qs = [G.quantities(L[S]['x']) for S in L]
        rec['min_quantity'] = float(min(np.min(q) for q in qs))
        rec['excluded'] = rec['min_quantity'] < -1e-9
        rec['symmetric'] = len(set(prm['c'])) == 1
        rec['flags'] = sorted(G.flags)
    if fam == 'hombertrand':
        rec['unattained'] = [str(members(S, n)) for S in proper(n) if not L[S]['attained']]
    if fam == 'exchange':
        rec['scarf'] = dict(concave=True, positive_endowments=bool(np.all(G.omega.sum(axis=1) > 0)),
                            all_goods_present=bool(np.all(G.omega.sum(axis=0) > 0)),
                            zero_weights=bool(np.any(G.alpha == 0)))
    if opts.get('ntu', True) and not rec.get('excluded'):
        if fam == 'exchange':
            if sel == 'pess':
                p, X = G.equilibrium()
                z = np.array([G.u(i, X[i]) for i in range(n)])
                marg = [G.block_margin(S, z, sel) for S in proper(n)]
                rec['ntu'] = dict(verdict='nonempty' if max(marg) <= 1e-7 else 'unresolved',
                                  method='competitive allocation', max_margin=float(max(marg)))
            else:
                if rec['singleton_bound']:
                    rec['ntu'] = dict(verdict='empty', method='singleton bound')
                else:
                    sl, Y = G.tu_profile(v)
                    if sl >= -1e-9:
                        rec['ntu'] = dict(verdict='nonempty' if sl >= 1e-9 else 'tight', method='TU-core profile', slack=sl)
                    else:
                        p, X = G.equilibrium()
                        z = np.array([G.u(i, X[i]) for i in range(n)])
                        marg = [G.block_margin(S, z, sel) for S in proper(n)]
                        rec['ntu'] = dict(verdict='nonempty' if max(marg) <= 1e-7 else 'unresolved',
                                          method='competitive allocation (opt check)', max_margin=float(max(marg)))
        else:
            rec['ntu'] = ntu_dispatch(G, rec, v, L, mode, sel, search=opts.get('search', True))
    rec['secs'] = round(time.time() - t0, 3)
    return _clean(rec)


def grid_jobs():
    J = {}
    J['cournot'] = [('cournot', dict(c=list(c)), dict(ntu=False)) for n in (2, 3, 4) for c in cost_profiles(n, C_GRID)]
    J['cournot_ntu'] = [('cournot', dict(c=list(c)), dict(sim=False)) for n in (2, 3, 4)
                        for c in cost_profiles(n, C_GRID_NTU)]
    J['cournot_cap'] = [('cournot', dict(c=list(c), k=[k] * n), dict(ntu=False)) for n in (2, 3, 4)
                        for k in (0.1, 0.2, 0.3, 0.4) for c in cost_profiles(n, [0.0, 0.1, 0.2, 0.3, 0.4, 0.5])]
    J['hombertrand'] = [('hombertrand', dict(c=list(c)), {}) for n in (2, 3, 4) for c in cost_profiles(n, C_GRID_NTU)]
    J['pg'] = [('pg', dict(theta=list(t), f=f), {}) for f in PG_F for n in (2, 3, 4, 5)
               for t in itertools.combinations_with_replacement(PG_THETA, n)]
    J['lq'] = [('lq', dict(b=list(b), gamma=gn / (n - 1), sigma=s, gn=gn), {}) for n in (2, 3, 4)
               for gn in LQ_GN for s in LQ_SIGMA for b in itertools.combinations_with_replacement(LQ_B, n)]
    J['bertrand'] = [('bertrand', dict(c=list(c), g=g), {}) for n in (2, 3, 4) for g in BE_G
                     for c in cost_profiles(n, BE_C)]
    rng = np.random.default_rng(20261014)
    ex = []
    for util, r in (('cd', None), ('ces', -1.0), ('ces', 0.5)):
        for n in (3, 4):
            for m in (2, 3):
                for _ in range(50):
                    a = rng.dirichlet(np.ones(m), n)
                    w = rng.uniform(0.1, 1.0, (n, m))
                    ex.append(('exchange', dict(alpha=a.tolist(), omega=w.tolist(), util=util, r=r, variant='random'), {}))
    for n in (3, 4):
        for m in (2, 3):
            for _ in range(50):
                a = rng.dirichlet(np.ones(m), n)
                for i in range(n):
                    if rng.random() < 0.5:
                        a[i, rng.integers(m)] = 0.0
                        a[i] = a[i] / a[i].sum()
                w = rng.uniform(0.1, 1.0, (n, m))
                for sel in ('pess', 'opt'):
                    ex.append(('exchange', dict(alpha=a.tolist(), omega=w.tolist(), util='cd', r=None, variant='zero-weight'),
                               dict(sel=sel)))
    J['exchange'] = ex
    return J


PANEL_POINTS = [
    ('cournot', dict(c=[0.0, 0.0, 0.0])), ('cournot', dict(c=[0.0, 0.0, 0.2])), ('cournot', dict(c=[0.0, 0.1, 0.3])),
    ('pg', dict(theta=[1.0, 1.0, 1.0], f='log')), ('pg', dict(theta=[2.0, 2.0, 0.5], f='log')),
    ('pg', dict(theta=[2.0, 2.0, 2.0], f='crra2')), ('pg', dict(theta=[2.0, 2.0], f='log')),
    ('lq', dict(b=[1.0, 1.0, 1.0], gamma=0.15, sigma=0.25)), ('lq', dict(b=[0.5, 1.0, 2.0], gamma=0.15, sigma=-1.0)),
    ('bertrand', dict(c=[0.0, 0.0, 0.0], g=0.6)), ('bertrand', dict(c=[0.0, 0.2, 0.4], g=0.6)),
    ('hombertrand', dict(c=[0.0, 0.0, 0.2])),
]


def panel_jobs():
    return [(f, p, dict(mode=m, sel=s, search=False)) for f, p in PANEL_POINTS for m in ('ind', 'coord') for s in ('pess', 'opt')]


def run_all(out_json, workers=2, only=None):
    from multiprocessing import Pool
    J = grid_jobs()
    J['panel'] = panel_jobs()
    res = {}
    if os.path.exists(out_json):
        with open(out_json) as f:
            res = json.load(f)
    with Pool(workers) as pool:
        for name, jobs in J.items():
            if only and name not in only:
                continue
            t0 = time.time()
            res[name] = pool.map(job, jobs, chunksize=1)
            print('%-12s %5d points  %.0fs' % (name, len(jobs), time.time() - t0), flush=True)
            with open(out_json, 'w') as f:
                json.dump(res, f)
    res['catalogue'] = _clean(catalogue_report())
    with open(out_json, 'w') as f:
        json.dump(res, f)
    return res


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'runs',
                                                             'core-existence-sweep.json')
    only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
    run_all(out, workers=2, only=only)

