"""Independent checks for the realizable-language arm (specs/2026-10-06-realizable-language.md).

1. `istep`: an independently implemented small-step evaluator for L_T (recursive, its own substitution, value test and
   contraction rules; it shares no code with src/lt.py).  Cross-checked on every reduction a witness uses and on every
   step of every play trace.
2. `replay`: an independent witness replay checker.  It reads a witness tree (formula ids resolved to structural tuples
   once, then never uses lt.py again), re-checks every node's rule, premises, sizes and side conditions with `istep`.
3. `brute`: an independent exhaustive prover (plain boolean size-bounded search, no lower bounds, members drawn from
   every atom and box content of the root closure, a superset of lt.py's Mem) for small budgets: it re-decides found /
   refuted and the minimal size.
"""
import sys
sys.setrecursionlimit(100000)

# ------------------------------------------------------------------------------------------------------------
# Independent evaluator
# ------------------------------------------------------------------------------------------------------------
_VAL = {'lam', 'con', 'nat', 'quote', 'fix', 'fv'}


def ival(t):
    if t[0] in _VAL: return True
    return t[0] == 'pair' and ival(t[1]) and ival(t[2])


def isub(t, v, depth):
    k = t[0]
    if k == 'v':
        n = t[1]
        return v if n == depth else (('v', n - 1) if n > depth else t)
    if k in ('lam', 'fix'):
        return (k, isub(t[1], v, depth + 1))
    if k in ('con', 'nat', 'quote', 'fv'):
        return t
    if k == 'mk':
        return tuple(['mk', t[1]] + [isub(a, v, depth) for a in t[2:]])
    if k == 'sim':
        return ('sim', t[1], isub(t[2], v, depth))
    return tuple([k] + [isub(a, v, depth) for a in t[1:]])


_TC = ['v', 'lam', 'app', 'con', 'nat', 'pair', 'fst', 'snd', 'if', 'fix', 'quote', 'eq', 'mk', 'prove', 'sprove',
       'run', 'sim', 'fv']
_CC = ['C', 'D', 'T', 'F', 'TO']
_MC = ['plays', 'not', 'and', 'or', 'imp', 'box', 'bot', 'top']


def _ilist(xs):
    acc = ('nat', 0)
    for x in xs[::-1]:
        acc = ('pair', x, acc)
    return acc


def ipayload(t):
    k = t[0]
    if k == 'v' or k == 'nat': return ('nat', t[1])
    if k in ('lam', 'fix', 'quote'): return ('quote', t[1])
    if k == 'con': return ('nat', _CC.index(t[1]))
    if k == 'mk': return ('pair', ('nat', _MC.index(t[1])), _ilist([('quote', a) for a in t[2:]]))
    if k == 'sim': return ('pair', ('nat', t[1]), ('quote', t[2]))
    if k == 'fv': return ('nat', 0)
    return _ilist([('quote', a) for a in t[1:]])


def ienc(v):
    if v[0] == 'quote': return ('pair', ('nat', _TC.index(v[1][0])), ienc(ipayload(v[1])))
    if v[0] == 'pair': return ('pair', ienc(v[1]), ienc(v[2]))
    return v


def _iformula(kind, a):
    if kind == 'plays':
        if a[0][0] == 'quote' and a[1][0] == 'quote' and a[2] in (('con', 'C'), ('con', 'D')):
            return ('fv', ('plays', a[0][1], a[1][1], a[2][1]))
        return None
    if kind in ('bot', 'top'): return ('fv', (kind,))
    if kind == 'not': return ('fv', ('not', a[0][1])) if a[0][0] == 'fv' else None
    if kind == 'box':
        return ('fv', ('box', a[0][1], a[1][1])) if a[0][0] == 'nat' and a[1][0] == 'fv' else None
    if kind in ('and', 'or', 'imp'):
        return ('fv', (kind, a[0][1], a[1][1])) if a[0][0] == 'fv' and a[1][0] == 'fv' else None
    return None


def istep(t):
    """('val',) | ('stuck',) | ('det', t') | ('prove', c, fv, tT, tF), recursively."""
    k = t[0]
    if ival(t): return ('val',)
    if k == 'v': return ('stuck',)
    if k == 'sim':
        n, u = t[1], t[2]
        if ival(u): return ('det', u)
        if n == 0: return ('det', ('con', 'TO'))
        r = istep(u)
        if r[0] == 'stuck': return ('det', ('con', 'TO'))
        if r[0] == 'det': return ('det', ('sim', n - 1, r[1]))
        return ('prove', r[1], r[2], ('sim', n - 1, r[3]), ('sim', n - 1, r[4]))
    if k == 'if':
        if not ival(t[1]):
            return _ctx(istep(t[1]), lambda x: ('if', x, t[2], t[3]))
        if t[1] == ('con', 'T'): return ('det', t[2])
        if t[1] == ('con', 'F'): return ('det', t[3])
        return ('stuck',)
    first = 2 if k == 'mk' else 1
    args = list(t[first:])
    for i, a in enumerate(args):
        if not ival(a):
            def mk(x, i=i):
                aa = list(args); aa[i] = x
                return tuple(list(t[:first]) + aa)
            return _ctx(istep(a), mk)
    # all arguments are values: contract
    if k == 'app':
        f, a = args
        if f[0] == 'lam': return ('det', isub(f[1], a, 0))
        if f[0] == 'fix': return ('det', ('app', isub(f[1], f, 0), a))
        return ('stuck',)
    if k in ('fst', 'snd'):
        p = args[0]
        if p[0] == 'pair': return ('det', p[1] if k == 'fst' else p[2])
        if p[0] == 'quote':
            return ('det', ('nat', _TC.index(p[1][0])) if k == 'fst' else ipayload(p[1]))
        return ('stuck',)
    if k == 'eq':
        a, b = args
        same = a == b or ienc(a) == ienc(b)
        return ('det', ('con', 'T' if same else 'F'))
    if k == 'mk':
        f = _iformula(t[1], args)
        return ('stuck',) if f is None else ('det', f)
    if k in ('prove', 'sprove'):
        n, f = args
        if n[0] != 'nat' or f[0] != 'fv': return ('stuck',)
        if k == 'sprove': return ('det', ('con', 'T' if n[1] >= 1 else 'F'))
        return ('prove', n[1], f[1], ('con', 'T'), ('con', 'F'))
    if k == 'run':
        n, x, y = args
        if n[0] != 'nat' or x[0] != 'quote' or y[0] != 'quote': return ('stuck',)
        return ('det', ('sim', n[1], ('app', ('app', x[1], x), y)))
    return ('stuck',)


def _ctx(r, mk):
    if r[0] in ('val', 'stuck'): return ('stuck',) if r[0] == 'stuck' else r
    if r[0] == 'det': return ('det', mk(r[1]))
    return ('prove', r[1], r[2], mk(r[3]), mk(r[4]))


def check_trace(trace):
    """Every consecutive pair in a play trace that is a deterministic step must agree with istep.  Returns
    (steps checked, disagreements)."""
    n = bad = 0
    for a, b in zip(trace, trace[1:]):
        r = istep(a)
        if r[0] == 'det':
            n += 1
            if r[1] != b: bad += 1
        elif r[0] == 'prove':
            n += 1
            if b != r[3] and b != r[4]:
                # search-charged prove steps decrement sim fuels by W: compare shape only
                if _strip(b) not in (_strip(r[3]), _strip(r[4])): bad += 1
        else:
            bad += 1
    return n, bad


def _strip(t):
    if not isinstance(t, tuple): return t
    if t and t[0] == 'sim': return ('sim', '*', _strip(t[2]))
    return tuple(_strip(x) for x in t)


# ------------------------------------------------------------------------------------------------------------
# Structural formulas and readings (independent of lt.py's interning)
# ------------------------------------------------------------------------------------------------------------
def ireading(state, a):
    r = istep(state)
    if r[0] == 'val': return ('top',) if state == ('con', a) else ('bot',)
    if r[0] == 'stuck': return ('bot',)
    return ('atom', state, a)


def ifv(fv):
    k = fv[0]
    if k == 'plays': return ireading(('app', ('app', fv[1], ('quote', fv[1])), ('quote', fv[2])), fv[3])
    if k in ('bot', 'top'): return (k,)
    if k == 'not': return ('not', ifv(fv[1]))
    if k == 'box': return ('box', fv[1], ifv(fv[2]))
    return (k, ifv(fv[1]), ifv(fv[2]))


def downstream(A, B):
    """k >= 1 with A >_k B (B a reading of a deterministic successor state of atom A), else None."""
    if A[0] != 'atom': return None
    st, a = A[1], A[2]
    k = 0
    while True:
        r = istep(st)
        if r[0] != 'det': return None
        k += 1
        nxt = ireading(r[1], a)
        if nxt == B: return k
        if nxt[0] != 'atom': return None
        st = r[1]
        if k > 100000: return None


def ibox_ok(a, A, c, B):
    if A == B: return a <= c
    if downstream(A, B) is not None: return a <= c
    k = downstream(B, A)
    return k is not None and a + k <= c


def ideep(th, i, memo):
    """Formula id -> structural tuple (the only use of lt.py's data: reading the interned structure)."""
    r = memo.get(i)
    if r is not None: return r
    t = th.F[i]; k = t[0]
    if k in ('atom',): r = t
    elif k in ('bot', 'top'): r = (k,)
    elif k == 'not': r = ('not', ideep(th, t[1], memo))
    elif k == 'box': r = ('box', t[1], ideep(th, t[2], memo))
    else: r = (k, ideep(th, t[1], memo), ideep(th, t[2], memo))
    memo[i] = r
    return r


def convert(th, w, memo=None):
    memo = {} if memo is None else memo
    out = {'L': frozenset(ideep(th, x, memo) for x in w['L']), 'R': frozenset(ideep(th, x, memo) for x in w['R']),
           'size': w['size'], 'rule': w['rule']}
    p = w.get('princ')
    if isinstance(p, tuple): out['princ'] = tuple(ideep(th, x, memo) for x in p)
    elif p is not None: out['princ'] = ideep(th, p, memo)
    else: out['princ'] = None
    if 'jlob' in w:
        j = w['jlob']
        out['jlob'] = {'Ai': ideep(th, j['Ai'], memo), 'S': [ideep(th, x, memo) for x in j['S']], 'm': j['m']}
    out['prem'] = [convert(th, p, memo) for p in w.get('prem', [])]
    return out


# ------------------------------------------------------------------------------------------------------------
# Replay
# ------------------------------------------------------------------------------------------------------------
class ReplayError(Exception):
    pass


def replay(node, stats=None):
    """Check a converted witness tree.  Returns its size; raises ReplayError on any failure."""
    stats = {'nodes': 0, 'steps': 0, 'jlob': 0} if stats is None else stats
    stats['nodes'] += 1
    L, R, rule, prem = node['L'], node['R'], node['rule'], node['prem']
    sizes = [replay(p, stats) for p in prem]
    size = 1 + sum(sizes)
    if size != node['size']: raise ReplayError('size %d != declared %d at %s' % (size, node['size'], rule))

    def need(cond, msg):
        if not cond: raise ReplayError(msg + ' at ' + rule)

    def prem_is(i, PL, PR):
        need(prem[i]['L'] == frozenset(PL) and prem[i]['R'] == frozenset(PR), 'premise %d mismatch' % i)

    x = node['princ']
    if rule == 'ax':
        need(len(prem) == 0, 'axiom with premises')
        ok = ('bot',) in L or ('top',) in R or any(f in R and f[0] in ('atom', 'box') for f in L)
        need(ok, 'not an axiom')
        return size
    if rule == 'boxeq':
        need(len(prem) == 0, 'boxeq with premises')
        lx, ry = x
        need(lx in L and ry in R and lx[0] == 'box' and ry[0] == 'box', 'boxeq formulas')
        need(ibox_ok(lx[1], lx[2], ry[1], ry[2]), 'boxeq side condition')
        return size
    if rule in ('notL', 'andL', 'orL', 'impL', 'EvL', 'PrvL'):
        need(x in L, 'principal not on the left')
        Lx = L - {x}
        if rule == 'notL': prem_is(0, Lx, R | {x[1]})
        elif rule == 'andL': prem_is(0, Lx | {x[1], x[2]}, R)
        elif rule == 'orL': prem_is(0, Lx | {x[1]}, R); prem_is(1, Lx | {x[2]}, R)
        elif rule == 'impL': prem_is(0, Lx, R | {x[1]}); prem_is(1, Lx | {x[2]}, R)
        else:
            need(x[0] == 'atom', 'not an atom')
            r = istep(x[1]); stats['steps'] += 1
            if rule == 'EvL':
                need(r[0] == 'det', 'EvL on a non-deterministic state')
                prem_is(0, Lx | {ireading(r[1], x[2])}, R)
            else:
                need(r[0] == 'prove', 'PrvL on a non-prove state')
                bx = ('box', r[1], ifv(r[2]))
                prem_is(0, Lx | {bx, ireading(r[3], x[2])}, R)
                prem_is(1, Lx | {ireading(r[4], x[2])}, R | {bx})
        return size
    if rule in ('notR', 'orR', 'impR', 'andR', 'EvR', 'PrvR', 'Nec'):
        need(x in R, 'principal not on the right')
        Rx = R - {x}
        if rule == 'notR': prem_is(0, L | {x[1]}, Rx)
        elif rule == 'orR': prem_is(0, L, Rx | {x[1], x[2]})
        elif rule == 'impR': prem_is(0, L | {x[1]}, Rx | {x[2]})
        elif rule == 'andR': prem_is(0, L, Rx | {x[1]}); prem_is(1, L, Rx | {x[2]})
        elif rule == 'Nec':
            need(x[0] == 'box', 'Nec on a non-box')
            prem_is(0, [], [x[2]])
            need(sizes[0] <= x[1], 'Nec side condition')
        else:
            need(x[0] == 'atom', 'not an atom')
            r = istep(x[1]); stats['steps'] += 1
            if rule == 'EvR':
                need(r[0] == 'det', 'EvR on a non-deterministic state')
                prem_is(0, L, Rx | {ireading(r[1], x[2])})
            else:
                need(r[0] == 'prove', 'PrvR on a non-prove state')
                bx = ('box', r[1], ifv(r[2]))
                prem_is(0, L | {bx}, Rx | {ireading(r[3], x[2])})
                prem_is(1, L, Rx | {bx, ireading(r[4], x[2])})
        return size
    if rule == 'JLob':
        stats['jlob'] += 1
        need(x in R, 'JLob conclusion not on the right')
        j = node['jlob']; S, m, Ai = j['S'], j['m'], j['Ai']
        need(1 <= len(S) <= 3 and len(set(S)) == len(S), '|S|')
        need(Ai in S, 'concluded member not in S')
        need(x == Ai or downstream(Ai, x) is not None, 'conclusion not a member or downstream of one')
        H = frozenset(('box', m, A) for A in S)
        need(len(prem) == len(S), 'premise count')
        for i, A in enumerate(S): prem_is(i, H, [A])
        need(m >= size, 'JLob side condition m >= 1 + sum of premise sizes')
        return size
    raise ReplayError('unknown rule ' + rule)


# ------------------------------------------------------------------------------------------------------------
# Independent brute-force prover (small budgets)
# ------------------------------------------------------------------------------------------------------------
class Brute:
    """Plain exhaustive size-bounded search over K_T (or K_T^- with jlob=False).  derivable(L, R, n): a derivation of
    size <= n exists.  Members: every atom and every box content of the root's closure (computed with istep), plus
    upstream chain states.  Independent of src/lt.py."""

    def __init__(self, root_fv=None, root=None, jlob=True):
        self.root = root if root is not None else ifv(root_fv)
        self.jlob = jlob
        self.memo = {}
        self._closure()

    def _succ(self, f):
        k = f[0]
        if k == 'atom':
            r = istep(f[1])
            if r[0] == 'det': return [ireading(r[1], f[2])]
            bx = ('box', r[1], ifv(r[2]))
            return [bx, ireading(r[3], f[2]), ireading(r[4], f[2])]
        if k == 'box': return [f[2]]
        if k == 'not': return [f[1]]
        if k in ('and', 'or', 'imp'): return [f[1], f[2]]
        return []

    def _closure(self):
        seen = set([self.root]); order = [self.root]; i = 0
        while i < len(order):
            for g in self._succ(order[i]):
                if g not in seen: seen.add(g); order.append(g)
            i += 1
        mem = []
        for f in order:
            if f[0] == 'atom' and f not in mem: mem.append(f)
            if f[0] == 'box' and f[2][0] not in ('top', 'bot') and f[2] not in mem: mem.append(f[2])
        self.mem = mem
        self.pred = {}
        for f in order:
            if f[0] == 'atom':
                r = istep(f[1])
                if r[0] == 'det':
                    g = ireading(r[1], f[2])
                    if g[0] == 'atom': self.pred.setdefault(g, []).append(f)

    def ups(self, x):
        out = []; st = list(self.pred.get(x, []))
        while st:
            y = st.pop()
            if y not in out: out.append(y); st.extend(self.pred.get(y, []))
        return out

    def axiom(self, L, R):
        if ('bot',) in L or ('top',) in R: return True
        for f in L:
            if f in R and f[0] in ('atom', 'box'): return True
            if f[0] == 'box':
                for g in R:
                    if g[0] == 'box' and ibox_ok(f[1], f[2], g[1], g[2]): return True
        return False

    def d(self, L, R, n):
        """True iff L |- R has a derivation of size <= n."""
        if n < 1: return False
        key = (L, R)
        e = self.memo.get(key)       # (largest n known false, smallest n known true)
        if e is None: e = self.memo[key] = [0, None]
        if e[1] is not None and e[1] <= n: return True
        if n <= e[0]: return False
        ok = self._d(L, R, n)
        if ok: e[1] = n if e[1] is None else min(e[1], n)
        else: e[0] = max(e[0], n)
        return ok

    def _split(self, P1, P2, n):
        for s1 in range(1, n - 1):
            if self.d(P1[0], P1[1], s1) and self.d(P2[0], P2[1], n - 1 - s1): return True
        return False

    def _d(self, L, R, n):
        if self.axiom(L, R): return True
        if n < 2: return False
        for x in L:
            Lx = L - {x}; k = x[0]
            if k == 'not' and self.d(Lx, R | {x[1]}, n - 1): return True
            if k == 'and' and self.d(Lx | {x[1], x[2]}, R, n - 1): return True
            if k == 'or' and self._split((Lx | {x[1]}, R), (Lx | {x[2]}, R), n): return True
            if k == 'imp' and self._split((Lx, R | {x[1]}), (Lx | {x[2]}, R), n): return True
            if k == 'atom':
                r = istep(x[1])
                if r[0] == 'det':
                    if self.d(Lx | {ireading(r[1], x[2])}, R, n - 1): return True
                else:
                    bx = ('box', r[1], ifv(r[2]))
                    if self._split((Lx | {bx, ireading(r[3], x[2])}, R), (Lx | {ireading(r[4], x[2])}, R | {bx}), n):
                        return True
        for x in R:
            Rx = R - {x}; k = x[0]
            if k == 'not' and self.d(L | {x[1]}, Rx, n - 1): return True
            if k == 'or' and self.d(L, Rx | {x[1], x[2]}, n - 1): return True
            if k == 'imp' and self.d(L | {x[1]}, Rx | {x[2]}, n - 1): return True
            if k == 'and' and self._split((L, Rx | {x[1]}), (L, Rx | {x[2]}), n): return True
            if k == 'atom':
                r = istep(x[1])
                if r[0] == 'det':
                    if self.d(L, Rx | {ireading(r[1], x[2])}, n - 1): return True
                else:
                    bx = ('box', r[1], ifv(r[2]))
                    if self._split((L | {bx}, Rx | {ireading(r[3], x[2])}), (L, Rx | {bx, ireading(r[4], x[2])}), n):
                        return True
            if k == 'box' and self.d(frozenset(), frozenset([x[2]]), min(x[1], n - 1)): return True
            if self.jlob and k not in ('top', 'bot') and self.jl(x, n): return True
        return False

    def jl(self, X, n):
        """A JLoeb instance of size <= n concluding X."""
        concl = [X] + (self.ups(X) if X[0] == 'atom' else [])
        for Ai in concl:
            others = [y for y in self.mem if y != Ai]
            cands = [(Ai,)] + [(Ai, y) for y in others] + \
                    [(Ai, others[i], others[j]) for i in range(len(others)) for j in range(i + 1, len(others))]
            for S in cands:
                for size in range(1 + len(S), n + 1):
                    m = size                      # the strongest hypothesis budget admitting an instance of this size
                    H = frozenset(('box', m, A) for A in S)
                    if self._fits(H, S, size - 1): return True
        return False

    def _fits(self, H, S, total):
        """Premises H |- A_j (one per member) with sizes summing to exactly <= total."""
        if not S: return total >= 0
        A = S[0]
        for s in range(1, total - len(S) + 2):
            if self.d(H, frozenset([A]), s) and self._fits(H, S[1:], total - s): return True
        return False

    def minsize(self, cap):
        R = frozenset([self.root])
        for n in range(1, cap + 1):
            if self.d(frozenset(), R, n): return n
        return None
