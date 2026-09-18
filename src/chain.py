"""Attractor chain: rest points of the replicator, single-mutant transitions,
stationary distribution.

State = (support ids, frequencies).  Neutral states (payoff matrix constant
down each column on the support) live on the 1/N grid; other polymorphic
rest points keep their continuous frequencies.  A mutant q perturbs a state
by replacing one random agent (type t with probability x_t); selection then
runs to a rest point.  P(A->B) is proportional to sum_q mu(q) * P[settle at B].
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.csgraph as csg
from collections import defaultdict
from itertools import product
from dsl import *
from evaluate import pair_keys, evaluate, close_pairs, keys_of


# ---------------------------------------------------------------- replicator
def replicator(U, x0, rest_tol=1e-8, ext_tol=1e-9, atol=1e-5, max_steps=50000, keep_traj=64):
    """Deterministic replicator from x0 on payoff matrix U, integrated with a
    midpoint scheme under step-doubling error control.  Returns
    (x, status, traj); status in {'rest', 'cycle'}."""
    x = np.array(x0, float)
    x[x < ext_tol] = 0.0
    x /= x.sum()
    traj = []
    dt = 0.1

    def g(x):
        fit = U @ x
        return fit - x @ fit

    def step(x, h):
        # exponential midpoint: positivity-preserving, exact for constant fitness
        xm = x * np.exp(np.clip(0.5 * h * g(x), -50, 50)); xm /= xm.sum()
        xn = x * np.exp(np.clip(h * g(xm), -50, 50)); xn /= xn.sum()
        return xn

    for it in range(max_steps):
        fit = U @ x
        fbar = x @ fit
        m = (np.abs(fit - fbar) * (x > 0)).max()
        if m < rest_tol:
            return x, 'rest', traj
        if m < 1e-3 and (x > 0).sum() > 1:
            # polish: solve for the interior rest point on the current support
            sup = np.nonzero(x > 0)[0]
            Us = U[np.ix_(sup, sup)]
            A = np.vstack([np.hstack([Us, -np.ones((len(sup), 1))]), np.append(np.ones(len(sup)), 0.0)])
            bvec = np.append(np.zeros(len(sup)), 1.0)
            sol = np.linalg.lstsq(A, bvec, rcond=None)[0]
            xs = sol[:-1]
            if np.all(xs > 0) and np.abs(A @ sol - bvec).max() < 1e-10 and np.abs(xs - x[sup]).max() < 1e-2:
                xn = np.zeros_like(x); xn[sup] = xs / xs.sum()
                return xn, 'rest', traj
        while True:
            x1 = step(x, dt)
            x2 = step(step(x, 0.5 * dt), 0.5 * dt)
            err = np.abs(x1 - x2).max()
            if err <= atol or dt < 1e-12:
                break
            dt *= 0.5
        x = x2
        x[x < ext_tol] = 0.0
        x /= x.sum()
        if err < 0.1 * atol:
            dt = min(dt * 2.0, 1e6)
        if it % max(1, max_steps // keep_traj) == 0:
            traj.append(x.copy())
    return x, 'cycle', traj


# ---------------------------------------------------------------- providers
class SquareProvider:
    """Payoffs from a full square evaluation; classes are exact within L_n."""
    def __init__(self, lang, result, ids, dedup=True, round_dec=9):
        self.lang, self.res = lang, result
        ids = np.asarray(ids)
        self.ids = ids
        self.pos = {int(p): k for k, p in enumerate(ids)}
        self.Ufull = np.round(result.matrix(ids), round_dec)
        # divergence / values for reports
        mu = lang.mu[ids]
        if dedup and lang.arm != 'source':
            sig = defaultdict(list)
            R = np.round(self.Ufull, 6)
            for k, p in enumerate(ids):
                sig[(R[k].tobytes(), R[:, k].tobytes())].append(int(p))
            classes = []
            for members in sig.values():
                rep = min(members, key=lambda p: (lang.bits[p], p))
                classes.append((rep, members, float(mu[[self.pos[m] for m in members]].sum())))
        else:
            classes = [(int(p), [int(p)], float(mu[k])) for k, p in enumerate(ids)]
        classes.sort(key=lambda c: -c[2])
        self.classes = classes

    def prepare(self, support):
        pass

    def U(self, ids):
        idx = [self.pos[int(p)] for p in ids]
        return self.Ufull[np.ix_(idx, idx)]

    def mutant_classes(self, support):
        return self.classes


class SparseProvider:
    """Program x attractor evaluation on demand (the incremental path).

    Behavioural classes need a signature that separates programs which are
    neutral against the current support but differ elsewhere (they create
    distinct neutral extensions), so every program is also evaluated against
    a fixed probe set (all programs of size <= probe_upto) once at init; the
    class signature for a support is (probe block, support block).
    """
    def __init__(self, lang, game, ids, dedup=True, round_dec=9, tol=1e-11, probe_upto=4, chunk=40000, verbose=False):
        self.lang, self.game = lang, game
        self.ids = np.asarray(ids)
        self.mu = lang.mu[self.ids]
        self.pos = {int(p): k for k, p in enumerate(self.ids)}
        self.dedup = dedup and lang.arm != 'source'
        self.round_dec = round_dec
        self.tol = tol
        self.verbose = verbose
        self.chunk = chunk
        self.blocks = {}       # support tuple -> (rows K x m, cols m x K, diag K, inner m x m, classes)
        self.n_pairs = 0
        self.div_count = 0; self.div_total = 0
        self.probe = tuple(int(p) for p in lang.ids(probe_upto))
        self._block(self.probe)
        self.probe_sig = self._sig(self.probe)
        self.classes = self._classes(self.probe_sig)

    def _block(self, sup):
        L, g = self.lang, self.game
        S = np.array(sup)
        K, m = len(self.ids), len(S)
        rows = np.zeros((K, m)); cols = np.zeros((m, K)); diag = np.zeros(K)
        for c0 in range(0, K, self.chunk):
            ids = self.ids[c0:c0 + self.chunk]
            keys = pair_keys(L, ids, S, g.role)
            diagk = [keys_of(L.count, ids, ids, 0)]
            if g.role:
                diagk.append(keys_of(L.count, ids, ids, 1))
            keys = np.union1d(keys, np.concatenate(diagk))
            res = evaluate(L, g, keys, tol=self.tol)
            self.n_pairs += len(res.keys)
            self.div_count += int(res.div.sum()); self.div_total += len(res.keys)
            if m:
                I, J = np.meshgrid(ids, S, indexing='ij')
                rows[c0:c0 + len(ids)] = res.payoff(I.ravel(), J.ravel()).reshape(len(ids), m)
                cols[:, c0:c0 + len(ids)] = res.payoff(J.ravel(), I.ravel()).reshape(len(ids), m).T
            diag[c0:c0 + len(ids)] = res.payoff(ids, ids)
            if c0 == 0 and m:
                inner = np.round(res.matrix(S), self.round_dec)
            elif c0 == 0:
                inner = np.zeros((0, 0))
        rows = np.round(rows, self.round_dec); cols = np.round(cols, self.round_dec); diag = np.round(diag, self.round_dec)
        self.blocks[sup] = [rows, cols, diag, inner, None]
        if self.verbose:
            print('  prepared support %s: %d programs' % ([self.lang.src(p) for p in sup][:6], K), flush=True)

    def _sig(self, sup):
        rows, cols, diag, inner, _ = self.blocks[sup]
        return np.concatenate([np.round(rows, 6), np.round(cols.T, 6), np.round(diag, 6)[:, None]], axis=1)

    def _classes(self, sig):
        if not self.dedup:
            return [(int(p), [int(p)], float(self.mu[k])) for k, p in enumerate(self.ids)]
        groups = defaultdict(list)
        for k in range(len(self.ids)):
            groups[sig[k].tobytes()].append(int(self.ids[k]))
        classes = []
        for members in groups.values():
            rep = min(members, key=lambda p: (self.lang.bits[p], p))
            classes.append((rep, members, float(self.mu[[self.pos[q] for q in members]].sum())))
        classes.sort(key=lambda c: -c[2])
        return classes

    def prepare(self, support):
        sup = tuple(sorted(int(p) for p in support))
        if sup in self.blocks and self.blocks[sup][4] is not None:
            return
        if sup not in self.blocks:
            self._block(sup)
        sig = np.concatenate([self.probe_sig, self._sig(sup)], axis=1)
        self.blocks[sup][4] = self._classes(sig)

    def U(self, ids):
        """Payoff among ids; ids must be a prepared support plus at most one extra."""
        ids = [int(p) for p in ids]
        idset = set(ids)
        best = None
        for sup in self.blocks:
            if len(idset - set(sup)) <= 1 and (best is None or len(set(sup) & idset) > len(set(best) & idset)):
                best = sup
        if best is None:
            raise KeyError('support not prepared: %s' % ids)
        sup = best
        rows, cols, diag, inner, _ = self.blocks[sup]
        m = len(ids)
        Um = np.zeros((m, m))
        for a_i, a in enumerate(ids):
            for b_i, b in enumerate(ids):
                if a in sup and b in sup:
                    Um[a_i, b_i] = inner[sup.index(a), sup.index(b)]
                elif a in sup:
                    Um[a_i, b_i] = cols[sup.index(a), self.pos[b]]
                elif b in sup:
                    Um[a_i, b_i] = rows[self.pos[a], sup.index(b)]
                else:
                    Um[a_i, b_i] = diag[self.pos[a]]
        return Um

    def mutant_classes(self, support):
        if len(support) == 0:
            return self.classes
        sup = tuple(sorted(int(p) for p in support))
        self.prepare(sup)
        return self.blocks[sup][4]


# ---------------------------------------------------------------- chain
class Chain:
    """Lazy, flow-pruned attractor chain.

    States are expanded (their single-mutant transitions computed) only when
    the stationary flow into them exceeds `theta`; dominant edges (jump
    probability >= p_eager) are followed eagerly so long neutral walks are
    traversed in one pass.  Edges into unexpanded states are dropped and the
    source row renormalised (reflecting boundary); the total dropped flow is
    reported as `cut_flow`.
    """
    def __init__(self, provider, N, seeds=None, rest_tol=1e-8, fit_tol=1e-9, theta=1e-6,
                 p_eager=0.3, max_states=8000, max_rounds=60, verbose=False, key_dec=8):
        self.P = provider
        self.N = N
        self.rest_tol, self.fit_tol = rest_tol, fit_tol
        self.theta, self.p_eager = theta, p_eager
        self.max_states, self.max_rounds = max_states, max_rounds   # max_states caps expanded states
        self.verbose = verbose
        self.key_dec = key_dec
        self.states = {}                 # key -> (ids, x, kind)
        self.trans = {}                  # key -> {key2: prob}  (expanded states only)
        self.trans_mut = defaultdict(lambda: defaultdict(float))
        self.indeterminate = []
        self.seed_weight = {}
        self.seeds = seeds
        self._kind = {}

    # -- state helpers
    def key(self, ids, x):
        return (tuple(int(p) for p in ids), tuple(np.round(x, self.key_dec).tolist()))

    @staticmethod
    def is_neutral(U):
        return bool(np.all(np.abs(U - U[0:1, :]) < 1e-7))

    def kind_of(self, ids):
        ids = tuple(int(p) for p in ids)
        k = self._kind.get(ids)
        if k is None:
            k = 'mono' if len(ids) == 1 else ('neutral' if self.is_neutral(self.P.U(ids)) else 'poly')
            self._kind[ids] = k
        return k

    def add_state(self, ids, x):
        ids = np.asarray(ids); x = np.asarray(x, float)
        order = np.argsort(ids)
        ids, x = ids[order], x[order]
        k = self.key(ids, x)
        if k not in self.states:
            self.states[k] = (tuple(int(p) for p in ids), tuple(x.tolist()), self.kind_of(ids))
        return k

    def grid_state(self, ids, n):
        """State from integer counts n on support ids (drop zero counts)."""
        n = np.asarray(n)
        keep = n > 0
        return self.add_state(np.asarray(ids)[keep], n[keep] / self.N)

    def snap_outcomes(self, ids, x):
        """Randomised rounding of a neutral rest point onto the 1/N grid."""
        N = self.N
        x = np.asarray(x, float)
        n = np.floor(x * N + 1e-9).astype(int)
        k = N - n.sum()
        if k <= 0:
            return [(1.0, self.grid_state(ids, n))]
        m = len(ids)
        agg = defaultdict(float)
        if m ** k <= 512:
            for fill in product(range(m), repeat=k):
                pr = float(np.prod(x[list(fill)]))
                if pr <= 0: continue
                nn = n.copy()
                for s in fill: nn[s] += 1
                agg[self.grid_state(ids, nn)] += pr
        else:
            nn = n.copy(); nn[np.argmax(x)] += k
            agg[self.grid_state(ids, nn)] += 1.0
        z = sum(agg.values())
        return [(pr / z, kk) for kk, pr in agg.items()]

    def dead_outcomes(self, key, ids, x, ti):
        """Mutant died: the vacated slot is refilled by a random survivor."""
        ids_, x_, kind = self.states[key]
        if kind != 'neutral':
            return [(1.0, key)]
        n = np.round(np.asarray(x) * self.N).astype(int)
        n[ti] -= 1
        z = n.sum()
        outs = []
        for si in range(len(ids)):
            if n[si] <= 0: continue
            nn = n.copy(); nn[si] += 1
            outs.append((n[si] / z, self.grid_state(ids, nn)))
        return outs

    def integrate(self, ids, x0, from_key, q):
        ids = np.asarray(ids)
        U = self.P.U(ids)
        x, status, traj = replicator(U, x0, rest_tol=self.rest_tol)
        if status != 'rest':
            self.indeterminate.append((from_key, int(q), [(tuple(ids.tolist()), t) for t in traj]))
            return []
        keep = x > 0
        ids2, x2 = ids[keep], x[keep] / x[keep].sum()
        if len(ids2) > 1 and self.is_neutral(U[np.ix_(keep, keep)]):
            return self.snap_outcomes(ids2, x2)
        return [(1.0, self.add_state(ids2, x2))]

    # -- transitions of one state
    def expand(self, key):
        if key in self.trans:
            return
        ids, x, kind = self.states[key]
        ids = np.array(ids); x = np.array(x)
        N = self.N
        self.P.prepare(ids)
        classes = self.P.mutant_classes(ids)
        out = defaultdict(float)
        muts = defaultdict(lambda: defaultdict(float))
        idl = list(ids)
        for q, members, w in classes:
            if q in idl:
                qi = idl.index(q)
                for ti, t in enumerate(ids):
                    wt = w * x[ti]
                    if wt <= 0: continue
                    if q == t or kind != 'neutral':
                        out[key] += wt; muts[key][q] += wt
                    else:
                        n = np.round(x * N).astype(int); n[ti] -= 1; n[qi] += 1
                        k2 = self.grid_state(ids, n)
                        out[k2] += wt; muts[k2][q] += wt
                continue
            ids2 = np.append(ids, q)
            Uq = self.P.U(ids2)
            neutral_ext = self.is_neutral(Uq)
            for ti, t in enumerate(ids):
                wt = w * x[ti]
                if wt <= 0: continue
                x0 = np.append(x, 0.0); x0[ti] -= 1.0 / N; x0[-1] += 1.0 / N
                fit = Uq @ x0; fbar = x0 @ fit
                dq = fit[-1] - fbar
                if dq < -self.fit_tol:
                    res = self.dead_outcomes(key, ids, x, ti)
                elif neutral_ext and abs(dq) <= self.fit_tol:
                    n = np.append(np.round(x * N).astype(int), 0); n[ti] -= 1; n[-1] += 1
                    res = [(1.0, self.grid_state(ids2, n))]
                else:
                    res = self.integrate(ids2, x0, key, q)
                for pr, k2 in res:
                    out[k2] += wt * pr; muts[k2][q] += wt * pr
        z = sum(out.values())
        self.trans[key] = {k2: v / z for k2, v in out.items()}
        for k2, d in muts.items():
            for q, v in d.items():
                self.trans_mut[(key, k2)][q] += v / z

    # -- exploration
    def explore(self):
        if self.seeds is None:
            self.seeds = [(rep, w) for rep, members, w in self.P.mutant_classes(())]
        queue = []
        for rep, w in self.seeds:
            k = self.add_state([rep], [1.0])
            self.seed_weight[k] = self.seed_weight.get(k, 0) + w
            queue.append(k)
        self.cut_flow = 0.0
        for rnd in range(self.max_rounds):
            # eager phase
            while queue and len(self.trans) < self.max_states:
                k = queue.pop()
                if k in self.trans: continue
                self.expand(k)
                row = self.trans[k]
                nonself = [(v, b) for b, v in row.items() if b != k]
                if not nonself: continue
                z = sum(v for v, b in nonself)
                top = max(nonself)
                for v, b in nonself:
                    if b not in self.trans and (v / z >= self.p_eager or b == top[1]):
                        queue.append(b)
            pi = self.stationary()
            flow = defaultdict(float)
            for k, p in zip(self.keys_list, pi):
                for b, v in self.trans[k].items():
                    if b not in self.trans:
                        flow[b] += p * v
            cand = [b for b, f in flow.items() if f > self.theta]
            self.cut_flow = sum(f for b, f in flow.items() if f <= self.theta)
            if self.verbose:
                print('  round %d: %d expanded, %d states, %d candidates, cut flow %.2e' % (
                    rnd, len(self.trans), len(self.states), len(cand), self.cut_flow), flush=True)
            if not cand or len(self.trans) >= self.max_states:
                break
            queue = sorted(cand, key=lambda b: flow[b])
        self.explored = set(self.trans)
        return self

    # -- stationary distribution on the expanded set (reflecting boundary)
    def stationary(self):
        keys = list(self.trans)
        idx = {k: n for n, k in enumerate(keys)}
        n = len(keys)
        rows, cols, vals = [], [], []
        for a in keys:
            out = self.trans[a]
            kept = {b: v for b, v in out.items() if b in idx}
            z = sum(kept.values())
            if z <= 0:
                kept = {a: 1.0}; z = 1.0
            for b, v in kept.items():
                rows.append(idx[a]); cols.append(idx[b]); vals.append(v / z)
        P = sp.csr_matrix((vals, (rows, cols)), shape=(n, n))
        ncomp, labels = csg.connected_components(P, directed=True, connection='strong')
        leaving = np.zeros(ncomp, bool)
        Pc = P.tocoo()
        for a, b in zip(Pc.row, Pc.col):
            if labels[a] != labels[b]:
                leaving[labels[a]] = True
        terminal = [c for c in range(ncomp) if not leaving[c]]
        pis = {}
        for c in terminal:
            members = np.nonzero(labels == c)[0]
            if len(members) == 1:
                pis[c] = (members, np.array([1.0])); continue
            Pm = P[members][:, members]
            if len(members) <= 3000:
                A = Pm.toarray().T - np.eye(len(members))
                A[-1, :] = 1.0
                bvec = np.zeros(len(members)); bvec[-1] = 1.0
                v = np.linalg.lstsq(A, bvec, rcond=None)[0]
            else:
                A = (Pm.T - sp.eye(len(members))).tolil()
                A[-1, :] = 1.0
                bvec = np.zeros(len(members)); bvec[-1] = 1.0
                v = sp.linalg.spsolve(A.tocsc(), bvec)
            v = np.clip(v, 0, None); v /= v.sum()
            pis[c] = (members, v)
        init = np.zeros(n)
        for k, w in self.seed_weight.items():
            if k in idx: init[idx[k]] += w
        init /= init.sum()
        term_mask = np.isin(labels, terminal)
        absorb = {}
        trans = np.nonzero(~term_mask)[0]
        if len(trans):
            Q = P[trans][:, trans]
            I_Q = (sp.eye(len(trans)) - Q).tocsc()
            lu = sp.linalg.splu(I_Q)
            for c in terminal:
                tgt = np.nonzero(labels == c)[0]
                Rt = np.asarray(P[trans][:, tgt].sum(axis=1)).ravel()
                h = lu.solve(Rt)
                absorb[c] = float(init[trans] @ h) + float(init[tgt].sum())
        else:
            for c in terminal:
                absorb[c] = float(init[labels == c].sum())
        pi = np.zeros(n)
        for c in terminal:
            members, v = pis[c]
            pi[members] += absorb[c] * v
        self.keys_list, self.pi, self.terminal, self.absorb, self.labels, self.Pmat = keys, pi, terminal, absorb, labels, P
        return pi

    # -- reporting helpers
    def describe_state(self, key, lang):
        ids, x, kind = self.states[key]
        parts = ['%s:%.3g' % (lang.src(p), xi) for p, xi in zip(ids, x)]
        return kind + ' {' + ', '.join(parts) + '}'

    def support(self, thresh=1e-4):
        order = np.argsort(-self.pi)
        return [(self.keys_list[k], self.pi[k]) for k in order if self.pi[k] > thresh]

    def out_transitions(self, key, top=6):
        out = self.trans.get(key, {})
        items = sorted(((w, b) for b, w in out.items() if b != key), reverse=True)[:top]
        res = []
        for w, b in items:
            muts = sorted(self.trans_mut[(key, b)].items(), key=lambda kv: -kv[1])[:4]
            res.append((w, b, muts))
        return res
