"""Slow recursive reference evaluator (the oracle), k-ary.

value(i, j, r, b) -> (P, f): P is the length-k distribution over the level
returned by program i (role r, opponent j, application budget b) counting
only terminated paths; f is the probability of hitting the budget floor
somewhere on the path.  Floor hits abort (a path that hits the floor is
counted in f regardless of what happens after).  Applications consume one
unit of budget.  min/max are computed by explicit enumeration over level
pairs, independently of the survival-function trick in evaluate.py.
"""
import random
import numpy as np
from dsl import *


class Reference:
    def __init__(self, lang, role=False):
        self.L = lang
        self.role = role
        self.memo = {}
        self.k = lang.k

    def resolve(self, code, i, j):
        if code == ME: return i
        if code == THEM: return j
        return code

    def value(self, i, j, r, b):
        key = (i, j, r, b)
        if key in self.memo:
            return self.memo[key]
        v = self.ev(i, i, j, r, b)
        self.memo[key] = v
        return v

    def onehot(self, lv):
        p = np.zeros(self.k); p[lv] = 1.0
        return (p, 0.0)

    def ev(self, t, i, j, r, b):
        L = self.L; k = self.k
        op = L.op[t]
        if op == CONST: return self.onehot(int(L.lhs[t]))
        if op == X: return (np.full(k, 1.0 / k), 0.0)
        if op == ROLE: return self.onehot(0 if r == 0 else k - 1)
        if op == NOT:
            p, f = self.ev(L.lhs[t], i, j, r, b)
            return (p[::-1].copy(), f)
        if op in (AND, OR):
            pl, fl = self.ev(L.lhs[t], i, j, r, b)
            pr, fr = self.ev(L.rhs[t], i, j, r, b)
            out = np.zeros(k)
            sc = 0 if op == AND else k - 1          # short-circuit level
            out[sc] += pl[sc]
            f = fl
            for a in range(k):
                if a == sc: continue
                f += pl[a] * fr
                for c in range(k):
                    m = min(a, c) if op == AND else max(a, c)
                    out[m] += pl[a] * pr[c]
            return (out, f)
        if op == APP:
            if b == 0:
                return (np.zeros(k), 1.0)
            fn, arg = L.lhs[t], L.rhs[t]
            row = j if fn == THEM else i
            col = self.resolve(arg, i, j)
            rr = (1 - r) if (self.role and fn == THEM) else r
            return self.value(row, col, rr, b - 1)
        if op == EQ:
            a = self.resolve(L.lhs[t], i, j)
            bb = self.resolve(L.rhs[t], i, j)
            return self.onehot(k - 1 if a == bb else 0)
        raise ValueError(op)

    def final(self, i, j, r, b, game):
        """Distribution with floor mass on the role's minimax level."""
        p, f = self.value(i, j, r, b)
        p = p.copy(); p[game.minimax[r]] += f
        return p


def sample(lang, i, j, r=0, depth=64, role=False, rng=random):
    """One Monte-Carlo run of the actual stochastic process. Returns the
    level (int) or None (floor hit at the depth cap)."""
    L = lang; k = lang.k

    def ev(t, i, j, r, b):
        op = L.op[t]
        if op == CONST: return int(L.lhs[t])
        if op == X: return rng.randrange(k)
        if op == ROLE: return 0 if r == 0 else k - 1
        if op == NOT:
            v = ev(L.lhs[t], i, j, r, b)
            return None if v is None else (k - 1 - v)
        if op in (AND, OR):
            sc = 0 if op == AND else k - 1
            v = ev(L.lhs[t], i, j, r, b)
            if v is None or v == sc: return v
            u = ev(L.rhs[t], i, j, r, b)
            if u is None: return None
            return min(v, u) if op == AND else max(v, u)
        if op == APP:
            if b == 0: return None
            fn, arg = L.lhs[t], L.rhs[t]
            row = j if fn == THEM else i
            col = i if arg == ME else j if arg == THEM else arg
            rr = (1 - r) if (role and fn == THEM) else r
            return ev(row, row, col, rr, b - 1)
        if op == EQ:
            a = i if L.lhs[t] == ME else j if L.lhs[t] == THEM else L.lhs[t]
            bb = i if L.rhs[t] == ME else j if L.rhs[t] == THEM else L.rhs[t]
            return k - 1 if a == bb else 0
    return ev(i, i, j, r, depth)
