"""Slow recursive reference evaluator (the oracle).

value(i, j, r, b) -> (c, d, f): probability that program i, in role r,
against opponent j, with application budget b, returns action 0 (c),
action 1 (d), or hits the budget floor somewhere on its evaluation path (f).
Floor hits abort (a path that hits the floor is counted in f regardless of
what happens after).  Applications consume one unit of budget.
"""
import random
from dsl import *


class Reference:
    def __init__(self, lang, role=False):
        self.L = lang
        self.role = role
        self.memo = {}

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

    def ev(self, t, i, j, r, b):
        L = self.L
        op = L.op[t]
        if op == C: return (1.0, 0.0, 0.0)
        if op == D: return (0.0, 1.0, 0.0)
        if op == X: return (0.5, 0.5, 0.0)
        if op == ROLE: return (1.0, 0.0, 0.0) if r == 0 else (0.0, 1.0, 0.0)
        if op == NOT:
            c, d, f = self.ev(L.lhs[t], i, j, r, b)
            return (d, c, f)
        if op == AND:
            cl, dl, fl = self.ev(L.lhs[t], i, j, r, b)
            cr, dr, fr = self.ev(L.rhs[t], i, j, r, b)
            return (cl * cr, dl + cl * dr, fl + cl * fr)
        if op == OR:
            cl, dl, fl = self.ev(L.lhs[t], i, j, r, b)
            cr, dr, fr = self.ev(L.rhs[t], i, j, r, b)
            return (cl + dl * cr, dl * dr, fl + dl * fr)
        if op == APP:
            if b == 0:
                return (0.0, 0.0, 1.0)
            fn, arg = L.lhs[t], L.rhs[t]
            row = j if fn == THEM else i
            col = self.resolve(arg, i, j)
            rr = (1 - r) if (self.role and fn == THEM) else r
            return self.value(row, col, rr, b - 1)
        if op == EQ:
            a = self.resolve(L.lhs[t], i, j)
            bb = self.resolve(L.rhs[t], i, j)
            return (1.0, 0.0, 0.0) if a == bb else (0.0, 1.0, 0.0)
        raise ValueError(op)


def sample(lang, i, j, r=0, depth=64, role=False, rng=random):
    """One Monte-Carlo run of the actual stochastic process. Returns 'C', 'D'
    or None (floor hit at the depth cap)."""
    L = lang

    def ev(t, i, j, r, b):
        op = L.op[t]
        if op == C: return True
        if op == D: return False
        if op == X: return rng.random() < 0.5
        if op == ROLE: return r == 0
        if op == NOT:
            v = ev(L.lhs[t], i, j, r, b)
            return None if v is None else (not v)
        if op == AND:
            v = ev(L.lhs[t], i, j, r, b)
            if v is None or v is False: return v
            return ev(L.rhs[t], i, j, r, b)
        if op == OR:
            v = ev(L.lhs[t], i, j, r, b)
            if v is None or v is True: return v
            return ev(L.rhs[t], i, j, r, b)
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
            return a == bb
    v = ev(i, i, j, r, depth)
    return None if v is None else ('C' if v else 'D')
