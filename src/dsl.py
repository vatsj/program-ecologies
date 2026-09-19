"""Grammar, enumerator, hash-consing, program bodies, mutation prior.

    A ::= C | D | X | ROLE | not A | and A A | or A A | P P | eq P P
    P ::= ME | THEM | ^A

Every A-term is a program.  P-sort values are small integer codes:
ME = -1, THEM = -2, and ^A is the id of A (>= 0).  A-terms are hash-consed
into flat arrays indexed by id; ids are assigned bottom-up by size, so a
child's id is always smaller than its parent's.
"""
import math
import os
import re
# one BLAS thread: the dense solves are small and multi-threaded OpenBLAS is
# hundreds of times slower under load
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np

C, D, X, ROLE, NOT, AND, OR, APP, EQ = range(9)
OPNAME = ['C', 'D', 'X', 'ROLE', 'not', 'and', 'or', 'app', 'eq']
ME, THEM = -1, -2
NONE = -3


class Language:
    def __init__(self, arm='weak', n=6, x_on=True, role=False, me_app=False):
        assert arm in ('strong', 'weak', 'source')
        self.arm, self.n, self.x_on, self.role, self.me_app = arm, n, x_on, role, me_app
        self._op, self._lhs, self._rhs, self._size = [], [], [], []
        self.table = {}
        self.by_size = {}
        self._enumerate()
        self.n_enum = len(self._op)          # programs of the truncated language
        self._freeze()
        self._build_bodies()
        self._prior()

    # ---- construction -------------------------------------------------
    def intern(self, op, lhs, rhs, size):
        key = (op, lhs, rhs)
        idx = self.table.get(key)
        if idx is not None:
            return idx
        idx = len(self._op)
        self.table[key] = idx
        self._op.append(op); self._lhs.append(lhs); self._rhs.append(rhs); self._size.append(size)
        self.by_size.setdefault(size, []).append(idx)
        return idx

    def _enumerate(self):
        n, arm = self.n, self.arm
        leaves = [C, D] + ([X] if self.x_on else []) + ([ROLE] if self.role else [])
        for op in leaves:
            self.intern(op, NONE, NONE, 1)
        P = {1: [ME, THEM]}
        for s in range(2, n + 1):
            for a in list(self.by_size[s - 1]):
                self.intern(NOT, a, NONE, s)
            for i in range(1, s - 1):
                j = s - 1 - i
                for a in self.by_size[i]:
                    for b in self.by_size[j]:
                        self.intern(AND, a, b, s)
                        self.intern(OR, a, b, s)
            if s - 2 >= 1:
                args = P.get(s - 2, [])
                fns = [THEM] + ([ME] if self.me_app else [])
                if arm == 'strong':
                    args = [a for a in args if a == ME]
                    fns = [THEM]
                for fn in fns:
                    for arg in args:
                        self.intern(APP, fn, arg, s)
            if arm == 'source':
                for i in range(1, s - 1):
                    j = s - 1 - i
                    for p in P.get(i, []):
                        for q in P.get(j, []):
                            # keep eq(THEM,ME), eq(ME,THEM), eq(THEM,^A); others are constants
                            if p == q or (p >= 0 and q >= 0) or ME in (p, q) and THEM not in (p, q):
                                continue
                            self.intern(EQ, p, q, s)
            P[s] = list(self.by_size.get(s - 1, []))
            self.by_size.setdefault(s, [])

    def _freeze(self):
        self.op = np.array(self._op, np.int8)
        self.lhs = np.array(self._lhs, np.int64)
        self.rhs = np.array(self._rhs, np.int64)
        self.size = np.array(self._size, np.int32)

    def _grow(self):
        """Refresh arrays after parse() added extra programs."""
        if len(self._op) != len(self.op):
            self._freeze()
            self._build_bodies()

    @property
    def count(self):
        return len(self._op)

    # ---- bodies: unique A-subterms outside ^, children before parents ----
    def _build_bodies(self):
        n = len(self._op)
        bodies = [None] * n
        for i in range(n):
            op = self._op[i]
            if op in (NOT,):
                b = bodies[self._lhs[i]] | {i}
            elif op in (AND, OR):
                b = bodies[self._lhs[i]] | bodies[self._rhs[i]] | {i}
            else:
                b = {i}
            bodies[i] = b
        cnt = np.array([len(b) for b in bodies], np.int64)
        self.body_start = np.concatenate([[0], np.cumsum(cnt)])[:-1]
        self.body_count = cnt
        le_id = np.concatenate([np.array(sorted(b), np.int64) for b in bodies])
        self.le_id = le_id
        self.le_prog = np.repeat(np.arange(n), cnt)
        self.le_op = self.op[le_id]
        self.le_size = self.size[le_id]
        # local (global-LE) child indices for not/and/or
        pos = {}
        le_lhs = np.full(len(le_id), -1, np.int64)
        le_rhs = np.full(len(le_id), -1, np.int64)
        for e in range(len(le_id)):
            p, t = self.le_prog[e], le_id[e]
            if e == self.body_start[p]:
                pos = {}
            pos[t] = e
            op = self._op[t]
            if op in (NOT, AND, OR):
                le_lhs[e] = pos[self._lhs[t]]
            if op in (AND, OR):
                le_rhs[e] = pos[self._rhs[t]]
        self.le_lhs, self.le_rhs = le_lhs, le_rhs
        # app entries per program
        is_app = self.le_op == APP
        self.app_le = np.nonzero(is_app)[0]
        self.app_prog = self.le_prog[self.app_le]
        self.app_fn = self.lhs[le_id[self.app_le]]
        self.app_arg = self.rhs[le_id[self.app_le]]
        self.app_count = np.bincount(self.app_prog, minlength=n)
        self.app_start = np.concatenate([[0], np.cumsum(self.app_count)])[:-1]

    # ---- prior ------------------------------------------------------------
    def _prior(self):
        """bits(p) = log2 a(|p|) + 2 log2 |p| + 1: uniform within a length
        class, Elias-gamma length prefix.  mu(p) = 2^-bits, unnormalised."""
        n = self.n_enum
        sz = self.size[:n]
        a = np.bincount(sz)
        self.class_count = a
        self.bits = np.log2(a[sz]) + 2 * np.log2(sz) + 1
        self.mu = 2.0 ** (-self.bits)

    def growth_rate(self, upto=40):
        """Asymptotic ratio a(L+1)/a(L) from the counting recursion."""
        a = {1: 2 + (1 if self.x_on else 0) + (1 if self.role else 0)}
        p = {1: 2}
        for s in range(2, upto + 1):
            v = a[s - 1] + 2 * sum(a[i] * a[s - 1 - i] for i in range(1, s - 1))
            if self.arm == 'strong':
                v += 1 if s == 3 else 0
            else:
                v += (1 + (1 if self.me_app else 0)) * p.get(s - 2, 0)
            if self.arm == 'source':
                # eq(THEM,ME), eq(ME,THEM) at s=3; eq(THEM,^A) for |A| = s-3
                v += 2 if s == 3 else 0
                v += a.get(s - 3, 0)
            a[s] = v
            p[s] = a[s - 1]
        return a[upto] / a[upto - 1], a

    # ---- printing / parsing -------------------------------------------------
    def psrc(self, code):
        if code == ME: return 'ME'
        if code == THEM: return 'THEM'
        return '^' + self.src(code)

    def src(self, i):
        op = self._op[i]
        if op <= ROLE: return OPNAME[op]
        if op == NOT: return 'not(%s)' % self.src(self._lhs[i])
        if op in (AND, OR): return '%s(%s,%s)' % (OPNAME[op], self.src(self._lhs[i]), self.src(self._rhs[i]))
        if op == APP: return '%s(%s)' % (self.psrc(self._lhs[i]), self.psrc(self._rhs[i]))
        if op == EQ: return 'eq(%s,%s)' % (self.psrc(self._lhs[i]), self.psrc(self._rhs[i]))

    def parse(self, s):
        toks = re.findall(r'[A-Za-z]+|[(),^↑]', s.replace(' ', ''))
        pos = 0

        def peek(): return toks[pos] if pos < len(toks) else None

        def eat(t=None):
            nonlocal pos
            tok = toks[pos]
            if t is not None and tok != t:
                raise ValueError('expected %s got %s in %s' % (t, tok, s))
            pos += 1
            return tok

        def P():
            tok = eat()
            if tok == 'ME': return ME, 1
            if tok == 'THEM': return THEM, 1
            if tok in ('^', '↑'):
                a, sz = A()
                return a, sz + 1
            raise ValueError('bad P-term %s' % tok)

        def A():
            tok = eat()
            if tok in ('C', 'D', 'X', 'ROLE'):
                return self.intern(OPNAME.index(tok), NONE, NONE, 1), 1
            if tok == 'not':
                eat('('); a, sa = A(); eat(')')
                return self.intern(NOT, a, NONE, sa + 1), sa + 1
            if tok in ('and', 'or'):
                eat('('); a, sa = A(); eat(','); b, sb = A(); eat(')')
                return self.intern(AND if tok == 'and' else OR, a, b, sa + sb + 1), sa + sb + 1
            if tok == 'eq':
                eat('('); p, sp = P(); eat(','); q, sq = P(); eat(')')
                return self.intern(EQ, p, q, sp + sq + 1), sp + sq + 1
            if tok in ('ME', 'THEM', '^', '↑'):
                pos_save = pos
                nonlocal_pos = None
                # application  P(P)
                fn = ME if tok == 'ME' else THEM if tok == 'THEM' else None
                if fn is None:
                    raise ValueError('^A applied is stripped; not supported: %s' % s)
                eat('('); q, sq = P(); eat(')')
                return self.intern(APP, fn, q, sq + 2), sq + 2
            raise ValueError('bad token %s in %s' % (tok, s))

        i, _ = A()
        if pos != len(toks):
            raise ValueError('trailing tokens in %s' % s)
        self._grow()
        return i

    def ids(self, upto=None):
        upto = self.n if upto is None else upto
        return np.array([i for i in range(self.n_enum) if self._size[i] <= upto], np.int64)
