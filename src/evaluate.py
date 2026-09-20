"""Batched value iteration over a flat tape of (pair, subterm) entries.

A *pair* is (i, j, r): program i, in role r, against program j.  With ROLE
off, r is always 0.  Pairs are encoded as int64 keys (i*S + j)*2 + r.

For every pair we track (P, f): the distribution over the k levels of the
returned action (P[l] = probability of level l and no floor hit) and the
probability f of hitting the budget floor.  Budget b+1 values of applications
read the budget b values of the pair they refer to; everything else is
computed within the same budget.  V_0 = floor everywhere.  Iterate until stall.

Value used downstream: V = P + f * onehot(minimax level of the role).
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
        k = L.k
        # static values
        c0 = np.zeros((E, k)); f0 = np.zeros(E)
        m = op == CONST
        c0[np.nonzero(m)[0], L.lhs[tid[m]]] = 1.0
        c0[op == X] = 1.0 / k
        m = op == ROLE
        c0[np.nonzero(m)[0], np.where(rp[m] == 0, 0, k - 1)] = 1.0
        m = op == EQ
        if m.any():
            a = L.lhs[tid[m]]; b = L.rhs[tid[m]]
            ra = np.where(a == ME, ip[m], np.where(a == THEM, jp[m], a))
            rb = np.where(b == ME, ip[m], np.where(b == THEM, jp[m], b))
            c0[np.nonzero(m)[0], np.where(ra == rb, k - 1, 0)] = 1.0
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
        self.k = k
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
        k = self.k
        lhs, rhs, dep = self.lhs, self.rhs, self.dep
        Vc = np.zeros((self.K, k)); Vf = np.ones(self.K)
        groups = [(op, s, lhs[s], rhs[s], dep[s]) for op, s in self.groups if op in (NOT, AND, OR, APP)]
        deltas = []
        for b in range(1, bmax + 1):
            for op, s, l, rr, d in groups:
                if op == NOT:
                    c[s] = c[l][:, ::-1]; f[s] = f[l]
                elif op == AND:
                    # min, short-circuit on level 0: P(min >= m) = P(L >= m) P(R >= m) for m >= 1
                    cl, cr = c[l], c[rr]
                    SL = np.cumsum(cl[:, ::-1], axis=1)[:, ::-1]     # SL[:, m] = P(L >= m, terminated)
                    SR = np.cumsum(cr[:, ::-1], axis=1)[:, ::-1]
                    S = SL * SR                                        # valid for m >= 1
                    out = np.empty_like(cl)
                    out[:, 1:k - 1] = S[:, 1:k - 1] - S[:, 2:k]
                    out[:, k - 1] = S[:, k - 1]
                    out[:, 0] = cl[:, 0] + SL[:, 1] * cr[:, 0]
                    c[s] = out; f[s] = f[l] + SL[:, 1] * f[rr]
                elif op == OR:
                    # max, short-circuit on level k-1: P(max <= m) = P(L <= m) P(R <= m) for m <= k-2
                    cl, cr = c[l], c[rr]
                    CL = np.cumsum(cl, axis=1)                         # CL[:, m] = P(L <= m, terminated)
                    CR = np.cumsum(cr, axis=1)
                    S = CL * CR
                    out = np.empty_like(cl)
                    out[:, 1:k - 1] = S[:, 1:k - 1] - S[:, 0:k - 2]
                    out[:, 0] = S[:, 0]
                    out[:, k - 1] = cl[:, k - 1] + CL[:, k - 2] * cr[:, k - 1]
                    c[s] = out; f[s] = f[l] + CL[:, k - 2] * f[rr]
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
    """Evaluated pair set.  V[index(i,j,r)] is the level distribution
    (k,) of program i in role r against j, with floor mass on the minimax
    level of the role."""
    def __init__(self, lang, game, keys, Vc, Vf, iters, delta):
        self.lang, self.game = lang, game
        self.keys, self.Vc, self.Vf = keys, Vc, Vf
        self.iters, self.delta = iters, delta
        S = lang.count
        i, j, r = unkey(S, keys)
        self.i, self.j, self.r = i, j, r
        self.V = Vc.copy()
        mm = game.minimax[r]
        self.V[np.arange(len(keys)), mm] += Vf
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


def square_chunked(lang, game, ids=None, rows=400, tol=1e-11, verbose=False):
    """Full program x program matrix of role-averaged payoffs U (S x S) and
    the value array V[i, j, r] (S x S x R x k), evaluated in row blocks so
    the tape never holds more than ~2*rows*S pairs (for languages too large
    for one square evaluation)."""
    ids = lang.ids() if ids is None else np.asarray(ids)
    S = len(ids); R = game.nroles; k = game.k
    Vfull = np.zeros((S, S, R, k))
    div = 0; tot = 0
    pos = {int(p): a for a, p in enumerate(ids)}
    for c0 in range(0, S, rows):
        blk = ids[c0:c0 + rows]
        res = evaluate(lang, game, pair_keys(lang, blk, ids, game.role), tol=tol)
        div += int(res.div.sum()); tot += len(res.keys)
        I, J = np.meshgrid(blk, ids, indexing='ij')
        for r in range(R):
            Vfull[c0:c0 + len(blk), :, r] = res.V[res.index(I.ravel(), J.ravel(), r)].reshape(len(blk), S, k)
            Vfull[:, c0:c0 + len(blk), r] = res.V[res.index(J.ravel(), I.ravel(), r)].reshape(len(blk), S, k).transpose(1, 0, 2)
        if verbose:
            print('  block %d/%d: %d pairs' % (c0 // rows + 1, (S + rows - 1) // rows, len(res.keys)), flush=True)
    if game.role:
        U = 0.5 * (np.einsum('ija,ab,jib->ij', Vfull[:, :, 0], game.pay[0], Vfull[:, :, 1])
                   + np.einsum('ija,ab,jib->ij', Vfull[:, :, 1], game.pay[1], Vfull[:, :, 0]))
    else:
        U = np.einsum('ija,ab,jib->ij', Vfull[:, :, 0], game.pay[0], Vfull[:, :, 0])
    return U, Vfull, div / max(tot, 1)
