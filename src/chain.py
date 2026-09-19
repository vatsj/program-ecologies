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
try:
    from numba import njit
except ImportError:  # pragma: no cover
    def njit(*a, **k):
        def deco(f): return f
        return deco if not a or not callable(a[0]) else a[0]


@njit(cache=True)
def _rep_step(U, x, h, out):
    n = len(x)
    fit = U @ x
    fbar = 0.0
    for i in range(n): fbar += x[i] * fit[i]
    xm = np.empty(n)
    z = 0.0
    for i in range(n):
        e = 0.5 * h * (fit[i] - fbar)
        if e > 50: e = 50
        if e < -50: e = -50
        xm[i] = x[i] * np.exp(e); z += xm[i]
    for i in range(n): xm[i] /= z
    fitm = U @ xm
    fbarm = 0.0
    for i in range(n): fbarm += xm[i] * fitm[i]
    z = 0.0
    for i in range(n):
        e = h * (fitm[i] - fbarm)
        if e > 50: e = 50
        if e < -50: e = -50
        out[i] = x[i] * np.exp(e); z += out[i]
    for i in range(n): out[i] /= z


@njit(cache=True)
def _replicator_nb(U, x0, rest_tol, ext_tol, atol, max_steps, polish_thresh, dt0):
    """Returns (x, status, dt): status 0 = rest, 1 = step cap, 2 = near rest (polish)."""
    n = len(x0)
    x = x0.copy()
    for i in range(n):
        if x[i] < ext_tol: x[i] = 0.0
    z = 0.0
    for i in range(n): z += x[i]
    for i in range(n): x[i] /= z
    dt = dt0
    x1 = np.empty(n); xh = np.empty(n); x2 = np.empty(n)
    for it in range(max_steps):
        fit = U @ x
        fbar = 0.0
        for i in range(n): fbar += x[i] * fit[i]
        m = 0.0; npos = 0
        for i in range(n):
            if x[i] > 0:
                npos += 1
                d = abs(fit[i] - fbar)
                if d > m: m = d
        if m < rest_tol:
            return x, 0, dt
        if m < polish_thresh and npos > 1:
            return x, 2, dt
        err = 0.0
        while True:
            _rep_step(U, x, dt, x1)
            _rep_step(U, x, 0.5 * dt, xh)
            _rep_step(U, xh, 0.5 * dt, x2)
            err = 0.0
            for i in range(n):
                d = abs(x1[i] - x2[i])
                if d > err: err = d
            if err <= atol or dt < 1e-12:
                break
            dt *= 0.5
        z = 0.0
        for i in range(n):
            x[i] = x2[i]
            if x[i] < ext_tol: x[i] = 0.0
            z += x[i]
        for i in range(n): x[i] /= z
        if err < 0.1 * atol:
            dt = min(dt * 2.0, 1e6)
    return x, 1, dt


def _polish(U, x):
    """Project x onto the affine set of rest points on its support (equal
    fitness for all present types, sum 1): the nearest solution, so neutral
    directions (behaviourally identical types) are handled."""
    sup = np.nonzero(x > 0)[0]
    Us = U[np.ix_(sup, sup)]
    A = np.vstack([np.hstack([Us, -np.ones((len(sup), 1))]), np.append(np.ones(len(sup)), 0.0)])
    bvec = np.append(np.zeros(len(sup)), 1.0)
    cur = np.append(x[sup], x[sup] @ Us @ x[sup])
    delta = np.linalg.lstsq(A, bvec - A @ cur, rcond=None)[0]
    sol = cur + delta
    xs = sol[:-1]
    if np.all(xs > 0) and np.abs(A @ sol - bvec).max() < 1e-10 and np.abs(xs - x[sup]).max() < 1e-2:
        xn = np.zeros_like(x); xn[sup] = xs / xs.sum()
        return xn
    return None


def replicator(U, x0, rest_tol=1e-8, ext_tol=1e-9, atol=1e-5, max_steps=50000, keep_traj=64):
    """Deterministic replicator from x0 on payoff matrix U (exponential
    midpoint steps under step-doubling error control; interior rest points
    are polished by a linear solve).  Returns (x, status, traj) with status in
    {'rest', 'cycle'}; traj holds samples only for cycles."""
    U = np.ascontiguousarray(U, dtype=np.float64); x = np.ascontiguousarray(x0, dtype=np.float64)
    x, st, dt = _replicator_nb(U, x, rest_tol, ext_tol, atol, max_steps, 1e-3, 0.1)
    if st == 0:
        return x, 'rest', []
    if st == 2:
        xp = _polish(U, x)
        if xp is not None:
            return xp, 'rest', []
        x, st, dt = _replicator_nb(U, x, rest_tol, ext_tol, atol, max_steps, 0.0, dt)
        if st == 0:
            return x, 'rest', []
    # step cap hit: sample a trajectory for the record
    traj = [x.copy()]
    for _ in range(keep_traj - 1):
        x, st, dt = _replicator_nb(U, x, rest_tol, ext_tol, atol, max(1, max_steps // keep_traj), 0.0, dt)
        traj.append(x.copy())
        if st == 0:
            return x, 'rest', []
    T = np.array(traj)
    if np.abs(T - T[-1]).max() < 1e-3:
        # not moving: a slowly-certified rest point, not a cycle.  Types that
        # are still (very slowly) dying are dropped before the projection.
        x = x.copy(); x[x < 1e-4] = 0.0; x /= x.sum()
        xp = _polish(U, x)
        return (xp if xp is not None else x), 'rest', []
    return x, 'cycle', traj


# ---------------------------------------------------------------- providers
class SquareProvider:
    """Payoffs from a full square evaluation.  Classes merge programs with
    identical rows and columns of the payoff matrix: interchangeable within
    L_n in every arm (in the source arm no program of L_n separates them, so
    the merge is sound at this truncation, though it may split at n+1)."""
    def __init__(self, lang, result, ids, dedup=True, round_dec=9):
        self.lang, self.res = lang, result
        ids = np.asarray(ids)
        self.ids = ids
        self.pos = {int(p): k for k, p in enumerate(ids)}
        self.Ufull = np.round(result.matrix(ids), round_dec)
        # divergence / values for reports
        mu = lang.mu[ids]
        if dedup:
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

    def U(self, ids, sup=None):
        idx = [self.pos[int(p)] for p in ids]
        return self.Ufull[np.ix_(idx, idx)]

    def mutant_classes(self, support):
        return self.classes

    def blocks_for(self, support):
        """(rows K x m, cols m x K, diag K, inner m x m) over class reps."""
        if not hasattr(self, '_rep_idx'):
            self._rep_idx = np.array([self.pos[c[0]] for c in self.classes])
            self._bcache = {}
        sup = tuple(int(p) for p in support)
        b = self._bcache.get(sup)
        if b is None:
            si = np.array([self.pos[p] for p in sup], int)
            R = self._rep_idx
            b = (self.Ufull[np.ix_(R, si)], self.Ufull[np.ix_(si, R)], self.Ufull[R, R], self.Ufull[np.ix_(si, si)])
            self._bcache[sup] = b
        return b


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

    def U(self, ids, sup=None):
        """Payoff among ids; ids must be a prepared support plus at most one extra."""
        ids = [int(p) for p in ids]
        if sup is None:
            idset = set(ids)
            best = None
            for cand in self.blocks:
                if len(idset - set(cand)) <= 1 and (best is None or len(set(cand) & idset) > len(set(best) & idset)):
                    best = cand
            if best is None:
                raise KeyError('support not prepared: %s' % ids)
            sup = best
        else:
            sup = tuple(sorted(int(p) for p in sup))
            if sup not in self.blocks:
                self._block(sup)
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

    def blocks_for(self, support):
        sup = tuple(sorted(int(p) for p in support))
        self.prepare(sup)
        rows, cols, diag, inner, classes = self.blocks[sup]
        R = np.array([self.pos[c[0]] for c in classes])
        return rows[R], cols[:, R], diag[R], inner


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
                 p_eager=0.3, max_states=30000, max_rounds=60, verbose=False, key_dec=8):
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
        keep = x > 1e-6          # remnants of (second-order) dying types are dropped
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
        N = self.N; m = len(ids)
        self.P.prepare(ids)
        classes = self.P.mutant_classes(ids)
        reps = np.array([c[0] for c in classes]); w = np.array([c[2] for c in classes])
        rows, cols, diag, inner = self.P.blocks_for(ids)
        K = len(reps)
        idl = [int(p) for p in ids]
        in_sup = np.isin(reps, ids)
        if kind == 'poly':
            neutral_ext = np.zeros(K, bool)
        else:
            neutral_ext = (np.abs(rows - inner[0:1, :]) < 1e-7).all(axis=1) & (np.abs(cols - diag[None, :]) < 1e-7).all(axis=0)
        out = defaultdict(float)
        muts = defaultdict(lambda: defaultdict(float))
        sup_tuple = tuple(idl)
        for ti, t in enumerate(ids):
            xt = x[ti]
            if xt <= 0: continue
            wt = w * xt
            # mutants of incumbent types
            for qi in np.nonzero(in_sup)[0]:
                q = int(reps[qi]); pos_q = idl.index(q)
                if q == int(t) or kind != 'neutral':
                    out[key] += wt[qi]; muts[key][q] += wt[qi]
                else:
                    n = np.round(x * N).astype(int); n[ti] -= 1; n[pos_q] += 1
                    k2 = self.grid_state(ids, n)
                    out[k2] += wt[qi]; muts[k2][q] += wt[qi]
            # outside mutants: first-order fitness test, vectorised over classes
            x0 = x.copy(); x0[ti] -= 1.0 / N
            fit_q = rows @ x0 + diag / N                       # K
            fit_s = (inner @ x0)[None, :] + cols.T / N         # K x m
            fbar = fit_s @ x0 + fit_q / N
            dq = fit_q - fbar
            dead = (dq < -self.fit_tol) & ~in_sup
            neut = neutral_ext & (np.abs(dq) <= self.fit_tol) & ~dead & ~in_sup
            integ = ~dead & ~neut & ~in_sup
            if dead.any():
                res = self.dead_outcomes(key, ids, x, ti)
                tot = wt[dead].sum()
                for pr, k2 in res:
                    out[k2] += tot * pr
                    d = muts[k2]
                    for qi in np.nonzero(dead)[0]:
                        d[int(reps[qi])] += wt[qi] * pr
            for qi in np.nonzero(neut)[0]:
                q = int(reps[qi])
                n = np.append(np.round(x * N).astype(int), 0); n[ti] -= 1; n[-1] += 1
                k2 = self.grid_state(np.append(ids, q), n)
                out[k2] += wt[qi]; muts[k2][q] += wt[qi]
            for qi in np.nonzero(integ)[0]:
                q = int(reps[qi])
                ids2 = np.append(ids, q)
                Uq = np.empty((m + 1, m + 1)); Uq[:m, :m] = inner; Uq[m, :m] = rows[qi]; Uq[:m, m] = cols[:, qi]; Uq[m, m] = diag[qi]
                x0q = np.append(x0, 1.0 / N)
                for pr, k2 in self.integrate_U(ids2, Uq, x0q, key, q):
                    out[k2] += wt[qi] * pr; muts[k2][q] += wt[qi] * pr
        z = sum(out.values())
        self.trans[key] = {k2: v / z for k2, v in out.items()}
        for k2, d in muts.items():
            for q, v in d.items():
                self.trans_mut[(key, k2)][q] += v / z

    def integrate_U(self, ids, U, x0, from_key, q):
        ids = np.asarray(ids)
        x, status, traj = replicator(U, x0, rest_tol=self.rest_tol)
        if status != 'rest':
            self.indeterminate.append((from_key, int(q), [(tuple(ids.tolist()), t) for t in traj]))
            return []
        keep = x > 1e-6          # remnants of (second-order) dying types are dropped
        ids2, x2 = ids[keep], x[keep] / x[keep].sum()
        if len(ids2) > 1 and self.is_neutral(U[np.ix_(keep, keep)]):
            return self.snap_outcomes(ids2, x2)
        return [(1.0, self.add_state(ids2, x2))]

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
        """pi on the expanded states.  Closed classes are found by processing
        the condensation DAG sink-first: a class whose absorption solve fails
        the row-sum identity (numerically closed) becomes a closed class of
        its own.  pi = sum over closed classes of (absorption probability from
        the seed distribution) x (stationary distribution inside the class)."""
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
        Pc = P.tocoo()
        cross = labels[Pc.row] != labels[Pc.col]
        # condensation DAG, topological order (Kahn)
        src, dst = labels[Pc.row[cross]], labels[Pc.col[cross]]
        succ = defaultdict(set)
        indeg = np.zeros(ncomp, int)
        for a, b in set(zip(src.tolist(), dst.tolist())):
            succ[a].add(b); indeg[b] += 1
        order = [c for c in range(ncomp) if indeg[c] == 0]
        topo = []
        while order:
            c = order.pop(); topo.append(c)
            for d in succ[c]:
                indeg[d] -= 1
                if indeg[d] == 0: order.append(d)
        members_of = [np.nonzero(labels == c)[0] for c in range(ncomp)]
        # edges grouped by source class
        eorder = np.argsort(labels[Pc.row], kind='stable')
        er, ec, ed = Pc.row[eorder], Pc.col[eorder], Pc.data[eorder]
        ebounds = np.searchsorted(labels[er], np.arange(ncomp + 1))
        terminal = []           # closed class ids
        H = {}                  # class -> (members, matrix members x len(terminal at the time))
        pis = {}
        self.near_closed = 0

        def stat_dist(Pm):
            m = Pm.shape[0]
            if m == 1: return np.array([1.0])
            rs = Pm.sum(axis=1)
            Pm = Pm / rs[:, None]
            A = Pm.T - np.eye(m); A[-1, :] = 1.0
            b = np.zeros(m); b[-1] = 1.0
            try:
                v = np.linalg.solve(A, b)
            except Exception:
                v = np.linalg.lstsq(A, b, rcond=None)[0]
            v = np.clip(v, 0, None); return v / v.sum()

        for c in reversed(topo):
            mem = members_of[c]
            m = len(mem)
            sl = slice(ebounds[c], ebounds[c + 1])
            rr, cc, dd = er[sl], ec[sl], ed[sl]
            lr = np.searchsorted(mem, rr)
            internal = labels[cc] == c
            Pm = np.zeros((m, m))
            np.add.at(Pm, (lr[internal], np.searchsorted(mem, cc[internal])), dd[internal])
            closed = not (~internal).any()
            if not closed:
                B = np.zeros((m, len(terminal)))
                outside = ~internal
                for d in np.unique(labels[cc[outside]]):
                    sel = outside & (labels[cc] == d)
                    mem_d, Hd = H[d]
                    pos = np.searchsorted(mem_d, cc[sel])
                    np.add.at(B[:, :Hd.shape[1]], lr[sel], dd[sel][:, None] * Hd[pos])
                if m == 1:
                    Hc = B / max(1.0 - Pm[0, 0], 1e-300)
                else:
                    try:
                        Hc = np.linalg.solve(np.eye(m) - Pm, B)
                    except Exception:
                        Hc = None
                if Hc is None or np.abs(Hc.sum(axis=1) - 1).max() > 1e-6 or Hc.min() < -1e-6:
                    closed = True
                    self.near_closed += 1
                else:
                    H[c] = (mem, np.clip(Hc, 0, None))
            if closed:
                terminal.append(c)
                pis[c] = stat_dist(Pm)
                Hc = np.zeros((m, len(terminal))); Hc[:, -1] = 1.0
                H[c] = (mem, Hc)
        init = np.zeros(n)
        for k, w in self.seed_weight.items():
            if k in idx: init[idx[k]] += w
        init /= init.sum()
        absorb = defaultdict(float)
        for c in range(ncomp):
            mem, Hc = H[c]
            wts = init[mem] @ Hc
            for ci, t in enumerate(terminal[:Hc.shape[1]]):
                absorb[t] += float(wts[ci])
        pi = np.zeros(n)
        for c in terminal:
            pi[members_of[c]] += absorb[c] * pis[c]
        self.absorb_error = float(abs(pi.sum() - 1.0))
        self.keys_list, self.pi, self.terminal, self.absorb, self.labels, self.Pmat = keys, pi, terminal, dict(absorb), labels, P
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
