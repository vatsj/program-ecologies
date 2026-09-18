"""Batched value iteration over a flat tape of (pair, subterm) entries.

A *pair* is (i, j, r): program i, in role r, against program j.  With ROLE
off, r is always 0.  Pairs are encoded as int64 keys (i*S + j)*2 + r.

For every pair we track (c, f): probability of returning action 0, and of
hitting the budget floor.  Budget b+1 values of applications read the budget
b values of the pair they refer to; everything else is computed within the
same budget.  V_0 = floor everywhere.  Iterate until stall.

Value used downstream: V = c + f * [minimax action == action 0].
Divergent pair: f > DIV_TOL at convergence.
"""
import numpy as np
from dsl import *

DIV_TOL = 1e-6


def keys_of(S, i, j, r=0):
    return (np.asarray(i, np.int64) * S + np.asarray(j, np.int64)) * 2 + np.asarray(r, np.int64)


def unkey(S, k):
    r = k % 2
    ij = k // 2
    return ij // S, ij % S, r


def close_pairs(lang, keys, role):
    """Dependency closure of a set of pair keys (int64 array)."""
    S = lang.count
    keys = np.unique(np.asarray(keys, np.int64))
    frontier = keys
    while len(frontier):
        i, j, r = unkey(S, frontier)
        cnt = lang.app_count[i]
        if cnt.sum() == 0:
            break
        rep = np.repeat(np.arange(len(frontier)), cnt)
        start = np.repeat(lang.app_start[i], cnt)
        local = np.arange(len(rep)) - np.repeat(np.concatenate([[0], np.cumsum(cnt)])[:-1], cnt)
        a = start + local
        fn, arg = lang.app_fn[a], lang.app_arg[a]
        ii, jj, rr = i[rep], j[rep], r[rep]
        row = np.where(fn == THEM, jj, ii)
        col = np.where(arg == ME, ii, np.where(arg == THEM, jj, arg))
        rr2 = np.where((fn == THEM) & role, 1 - rr, rr)
        deps = np.unique(keys_of(S, row, col, rr2))
        new = deps[~np.isin(deps, keys, assume_unique=True)]
        keys = np.union1d(keys, new)
        frontier = new
    return keys


class Tape:
    def __init__(self, lang, keys, role):
        L = lang
        S = L.count
        keys = np.asarray(keys, np.int64)
        i, j, r = unkey(S, keys)
        order = np.argsort(i, kind='stable')
        keys, i, j, r = keys[order], i[order], j[order], r[order]
        self.keys, self.i, self.j, self.r = keys, i, j, r
        K = len(keys)
        cnt = L.body_count[i]
        off = np.concatenate([[0], np.cumsum(cnt)])
        E = int(off[-1])
        pair_of = np.repeat(np.arange(K), cnt)
        le = L.body_start[i][pair_of] + (np.arange(E) - np.repeat(off[:-1], cnt))
        op = L.le_op[le]
        size = L.le_size[le]
        base = np.repeat(off[:-1], cnt) - L.body_start[i][pair_of]    # entry = base + LE index
        lhs = np.where(L.le_lhs[le] >= 0, base + L.le_lhs[le], -1)
        rhs = np.where(L.le_rhs[le] >= 0, base + L.le_rhs[le], -1)
        ip, jp, rp = i[pair_of], j[pair_of], r[pair_of]
        tid = L.le_id[le]
        # static values
        c0 = np.zeros(E); f0 = np.zeros(E)
        c0[op == C] = 1.0
        c0[op == X] = 0.5
        c0[op == ROLE] = (rp[op == ROLE] == 0)
        m = op == EQ
        if m.any():
            a = L.lhs[tid[m]]; b = L.rhs[tid[m]]
            ra = np.where(a == ME, ip[m], np.where(a == THEM, jp[m], a))
            rb = np.where(b == ME, ip[m], np.where(b == THEM, jp[m], b))
            c0[m] = (ra == rb)
        # app deps -> pair index
        dep = np.full(E, -1, np.int64)
        m = op == APP
        if m.any():
            fn = L.lhs[tid[m]]; arg = L.rhs[tid[m]]
            row = np.where(fn == THEM, jp[m], ip[m])
            col = np.where(arg == ME, ip[m], np.where(arg == THEM, jp[m], arg))
            rr = np.where((fn == THEM) & role, 1 - rp[m], rp[m])
            dk = keys_of(S, row, col, rr)
            pos = np.searchsorted(keys, dk)
            pos = np.minimum(pos, K - 1)
            if not np.all(keys[pos] == dk):
                raise ValueError('pair set not closed under dependencies')
            dep[m] = pos
        body = off[1:] - 1
        # sort entries by (size, op)
        perm = np.lexsort((op, size))
        inv = np.empty(E, np.int64); inv[perm] = np.arange(E)
        self.op, self.size = op[perm], size[perm]
        self.lhs = np.where(lhs >= 0, inv[np.maximum(lhs, 0)], -1)[perm]
        self.rhs = np.where(rhs >= 0, inv[np.maximum(rhs, 0)], -1)[perm]
        self.dep = dep[perm]
        self.c0, self.f0 = c0[perm], f0[perm]
        self.body = inv[body]
        # groups
        key = self.size.astype(np.int64) * 16 + self.op
        bounds = np.flatnonzero(np.diff(key)) + 1
        starts = np.concatenate([[0], bounds]); ends = np.concatenate([bounds, [E]])
        self.groups = [(int(self.op[s]), slice(int(s), int(e))) for s, e in zip(starts, ends)]
        self.E, self.K = E, K

    def iterate(self, tol=1e-10, bmax=2000, verbose=False):
        """Returns (Vc, Vf, budget, delta): values at application budget
        `budget` (pass k computes budget k-1; budget 0 = all applications floor)."""
        bmax = bmax + 1
        c = self.c0.copy(); f = self.f0.copy()
        lhs, rhs, dep = self.lhs, self.rhs, self.dep
        Vc = np.zeros(self.K); Vf = np.ones(self.K)
        groups = [(op, s, lhs[s], rhs[s], dep[s]) for op, s in self.groups if op in (NOT, AND, OR, APP)]
        deltas = []
        for b in range(1, bmax + 1):
            for op, s, l, rr, d in groups:
                if op == NOT:
                    c[s] = 1.0 - c[l] - f[l]; f[s] = f[l]
                elif op == AND:
                    cl = c[l]
                    c[s] = cl * c[rr]; f[s] = f[l] + cl * f[rr]
                elif op == OR:
                    cl = c[l]; fl = f[l]; dl = 1.0 - cl - fl
                    c[s] = cl + dl * c[rr]; f[s] = fl + dl * f[rr]
                else:
                    c[s] = Vc[d]; f[s] = Vf[d]
            Vc2 = c[self.body]; Vf2 = f[self.body]
            delta = max(np.abs(Vc2 - Vc).max(), np.abs(Vf2 - Vf).max())
            Vc, Vf = Vc2, Vf2
            deltas.append(delta)
            if verbose and b % 20 == 0:
                print('  b=%d delta=%.3e' % (b, delta))
            if delta < tol:
                break
        np.clip(Vc, 0, 1, out=Vc); np.clip(Vf, 0, 1, out=Vf)
        return Vc, Vf, b - 1, delta   # pass b yields budget b-1 values


class Result:
    """Evaluated pair set. get(i,j,r) -> (V, f)."""
    def __init__(self, lang, game, keys, Vc, Vf, iters, delta):
        self.lang, self.game = lang, game
        self.keys, self.Vc, self.Vf = keys, Vc, Vf
        self.iters, self.delta = iters, delta
        S = lang.count
        i, j, r = unkey(S, keys)
        self.i, self.j, self.r = i, j, r
        self.V = Vc + Vf * game.minimax_C[r]
        self.div = Vf > DIV_TOL

    def index(self, i, j, r=0):
        k = keys_of(self.lang.count, i, j, r)
        pos = np.searchsorted(self.keys, k)
        pos = np.minimum(pos, len(self.keys) - 1)
        ok = self.keys[pos] == k
        if not np.all(ok):
            raise KeyError('pair not evaluated')
        return pos

    def payoff(self, i, j):
        """Expected base-game payoff of i against j, averaged over roles."""
        i = np.asarray(i); j = np.asarray(j)
        g = self.game
        if not g.role:
            return g.payoff(self.V[self.index(i, j, 0)], self.V[self.index(j, i, 0)], 0)
        u0 = g.payoff(self.V[self.index(i, j, 0)], self.V[self.index(j, i, 1)], 0)
        u1 = g.payoff(self.V[self.index(i, j, 1)], self.V[self.index(j, i, 0)], 1)
        return 0.5 * (u0 + u1)

    def matrix(self, ids):
        ids = np.asarray(ids)
        I, J = np.meshgrid(ids, ids, indexing='ij')
        return self.payoff(I.ravel(), J.ravel()).reshape(len(ids), len(ids))


def evaluate(lang, game, keys, tol=1e-10, bmax=2000, verbose=False):
    keys = close_pairs(lang, keys, game.role)
    tape = Tape(lang, keys, game.role)
    if verbose:
        print('tape: %d pairs, %d entries' % (tape.K, tape.E))
    Vc, Vf, iters, delta = tape.iterate(tol, bmax, verbose)
    return Result(lang, game, tape.keys, Vc, Vf, iters, delta)


def pair_keys(lang, rows, cols, role):
    """All (i, j, r) keys for i in rows, j in cols, both orders, all roles."""
    S = lang.count
    rows = np.asarray(rows, np.int64); cols = np.asarray(cols, np.int64)
    I, J = np.meshgrid(rows, cols, indexing='ij')
    ks = [keys_of(S, I.ravel(), J.ravel(), 0), keys_of(S, J.ravel(), I.ravel(), 0)]
    if role:
        ks += [keys_of(S, I.ravel(), J.ravel(), 1), keys_of(S, J.ravel(), I.ravel(), 1)]
    return np.unique(np.concatenate(ks))


def square(lang, game, ids=None, **kw):
    ids = lang.ids() if ids is None else np.asarray(ids)
    keys = pair_keys(lang, ids, ids, game.role)
    return evaluate(lang, game, keys, **kw)
