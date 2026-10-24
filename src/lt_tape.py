"""A private random tape in the realizable language (specs/2026-10-24-realizable-randomizer.md; notes/lt-tape.md).

L_T^tape = L_T (src/lt.py, milestone 1: untyped call-by-value de Bruijn lambda-calculus, one step per contraction,
search-charged `prove`) plus
  * `tape i`      : digit i of the evaluating invocation's private tape (fresh per root evaluation and per `run`);
  * `hq m q`      : a deterministic hash of the quoted value q, mod m, at a cost of one step per node of q;
  * `prp b x y a k`: counted-probability proof by ENUMERATION: Pr[x(<x>,<y>) plays a] >= k/den, replayed leaf by leaf;
  * `chk x y a k` : the same atom CHECKED from a certificate the carrier x carries in its own source;
  * `poison`      : a value that fails the replay if any operation touches it (opponent-generic certificates).
K_T^tape = K_T plus TapeR/TapeL (the for-all-tapes atoms); `prp`/`chk` redexes inside idealized atoms are opaque.

Parts: 1 terms; 2 contraction/decomposition; 3 K_T^tape (Theory, Search, Prover); 4 the exact engine (play, prp, chk);
5 certificates; 6 truth and the soundness audit.  Nothing under src/lt*.py is edited; this module subclasses lt.Theory,
lt.Search and lt.Prover and copies the parts of lt.py's small-step machinery that must know about tapes.
"""
import os
import sys
import zlib
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt as L

sys.setrecursionlimit(200000)
INF = L.INF

# ----------------------------------------------------------------------------------------------------------------
# 1. Terms
# ----------------------------------------------------------------------------------------------------------------
VALUE_TAGS = ('lam', 'con', 'nat', 'quote', 'fix', 'fv', 'poison')
ACTIONS = ('R', 'P', 'S', 'I', 'N', 'C', 'K')
T_, F_, TO_ = ('con', 'T'), ('con', 'F'), ('con', 'TO')
POISON = ('poison',)
ME, THEM = ('v', 1), ('v', 0)


def con(n): return ('con', n)
def nat(i): return ('nat', i)
def L2(body): return ('lam', ('lam', body))
def TP(i): return ('tape', nat(i))
def EQ(a, b): return ('eq', a, b)
def IF(c, a, b): return ('if', c, a, b)
def PL(x, y, a): return ('mk', 'plays', x, y, con(a))
def HQ(m, v): return ('hq', nat(m), v)
def PAIR(a, b): return ('pair', a, b)


def is_value(t):
    tag = t[0]
    if tag in VALUE_TAGS: return True
    if tag == 'pair': return is_value(t[1]) and is_value(t[2])
    return False


def subst(t, v, d=0):
    """t[d := v] for a closed value v; free variables above d are decremented; never enters quotes or formula values."""
    tag = t[0]
    if tag == 'v':
        i = t[1]
        if i == d: return v
        if i > d: return ('v', i - 1)
        return t
    if tag in ('con', 'nat', 'quote', 'fv', 'poison'): return t
    if tag in ('lam', 'fix'): return (tag, subst(t[1], v, d + 1))
    if tag == 'mk': return ('mk', t[1]) + tuple(subst(a, v, d) for a in t[2:])
    if tag == 'sim': return ('sim', t[1], t[2], subst(t[3], v, d))
    return (tag,) + tuple(subst(a, v, d) for a in t[1:])


def shift(t, d=1, cut=0):
    """Free variables >= cut are increased by d (to put a closed-in-ME/THEM body under extra binders)."""
    tag = t[0]
    if tag == 'v': return ('v', t[1] + d) if t[1] >= cut else t
    if tag in ('con', 'nat', 'quote', 'fv', 'poison'): return t
    if tag in ('lam', 'fix'): return (tag, shift(t[1], d, cut + 1))
    if tag == 'mk': return ('mk', t[1]) + tuple(shift(a, d, cut) for a in t[2:])
    if tag == 'sim': return ('sim', t[1], t[2], shift(t[3], d, cut))
    return (tag,) + tuple(shift(a, d, cut) for a in t[1:])


_size_cache = {}


def size(t):
    """Node count: every tuple is a node; a quote counts 1 + the quoted term; `mk` counts its operands, not its kind."""
    r = _size_cache.get(t)
    if r is not None: return r
    tag = t[0]
    if tag in ('v', 'con', 'nat', 'fv', 'poison'): r = 1
    elif tag in ('lam', 'fix'): r = 1 + size(t[1])
    elif tag == 'quote': r = 1 + size(t[1])
    elif tag == 'mk': r = 1 + sum(size(a) for a in t[2:])
    elif tag == 'sim': r = 1 + size(t[3])
    else: r = 1 + sum(size(a) for a in t[1:])
    _size_cache[t] = r
    return r


def qnodes(v):
    """Cost basis of `hq`: nodes of the hashed value (a quote costs the size of its term; a pair 1 + both sides)."""
    tag = v[0]
    if tag == 'quote': return size(v[1])
    if tag == 'pair': return 1 + qnodes(v[1]) + qnodes(v[2])
    return 1


def hash_value(v, m):
    return zlib.crc32(repr(v).encode()) % m


def plist(xs):
    out = nat(0)
    for x in reversed(xs): out = PAIR(x, out)
    return out


def parse_plist(v):
    """Python list from a nested-pair list ending in nat 0; None if malformed."""
    out = []
    while v != nat(0):
        if v[0] != 'pair': return None
        out.append(v[1]); v = v[2]
        if len(out) > 100000: return None
    return out


def mk_formula(kind, args):
    if kind == 'plays':
        x, y, a = args
        if x[0] != 'quote' or y[0] != 'quote' or a[0] != 'con' or a[1] not in ACTIONS: return None
        return ('fv', ('plays', x[1], y[1], a[1]))
    if kind == 'bot': return ('fv', ('bot',))
    if kind == 'top': return ('fv', ('top',))
    if kind == 'not':
        if args[0][0] != 'fv': return None
        return ('fv', ('not', args[0][1]))
    if kind in ('and', 'or', 'imp'):
        if args[0][0] != 'fv' or args[1][0] != 'fv': return None
        return ('fv', (kind, args[0][1], args[1][1]))
    if kind == 'box':
        n, f = args
        if n[0] != 'nat' or f[0] != 'fv': return None
        return ('fv', ('box', n[1], f[1]))
    return None


# ----------------------------------------------------------------------------------------------------------------
# 2. Contraction and decomposition (tapes, sims with their own invocation ids, hash, enumeration/check redexes)
# ----------------------------------------------------------------------------------------------------------------
MARKERS = ('TAPE', 'PROVE', 'RUN', 'HQ', 'PRP', 'CHK')
STUCK = 'stuck'
POISON_READ = ('POISON',)


def _poisoned(v):
    if v[0] == 'poison': return True
    if v[0] == 'pair': return _poisoned(v[1]) or _poisoned(v[2])
    return False


def _has_poison(r, lo=1):
    for s in r[lo:]:
        if isinstance(s, tuple) and s and _poisoned(s): return True
    return False


def contract(r):
    """Contract a redex whose immediate subterms are values.  Returns the contractum, STUCK, POISON_READ (the replay's
    wildcard opponent was touched), or a redex marker ('TAPE', i) | ('PROVE', c, fv) | ('RUN', k, x, y) | ('HQ', m, v) |
    ('PRP', b, x, y, a, k) | ('CHK', x, y, a, k)."""
    tag = r[0]
    if tag == 'app':
        f, a = r[1], r[2]
        if f[0] == 'poison': return POISON_READ
        if f[0] == 'lam': return subst(f[1], a)
        if f[0] == 'fix': return ('app', subst(f[1], f), a)
        return STUCK
    if tag == 'if':
        if r[1][0] == 'poison': return POISON_READ
        c = r[1]
        if c == T_: return r[2]
        if c == F_: return r[3]
        return STUCK
    if tag != 'mk' and tag != 'pair' and _has_poison(r):
        return POISON_READ
    if tag in ('fst', 'snd'):
        p = r[1]
        if p[0] == 'pair': return p[1] if tag == 'fst' else p[2]
        return STUCK
    if tag == 'eq': return T_ if r[1] == r[2] else F_
    if tag == 'mk':
        if _has_poison(r, 2): return POISON_READ
        out = mk_formula(r[1], r[2:])
        return STUCK if out is None else out
    if tag == 'tape':
        if r[1][0] != 'nat': return STUCK
        return ('TAPE', r[1][1])
    if tag == 'hq':
        if r[1][0] != 'nat' or r[1][1] < 1: return STUCK
        return ('HQ', r[1][1], r[2])
    if tag == 'prove':
        n, f = r[1], r[2]
        if n[0] != 'nat' or f[0] != 'fv': return STUCK
        return ('PROVE', n[1], f[1])
    if tag == 'run':
        k, x, y = r[1], r[2], r[3]
        if k[0] != 'nat' or x[0] != 'quote' or y[0] != 'quote': return STUCK
        return ('RUN', k[1], x, y)
    if tag == 'prp':
        b, x, y, a, k = r[1:6]
        if b[0] != 'nat' or x[0] != 'quote' or y[0] != 'quote' or a[0] != 'con' or k[0] != 'nat': return STUCK
        return ('PRP', b[1], x, y, a[1], k[1])
    if tag == 'chk':
        x, y, a, k = r[1:5]
        if x[0] != 'quote' or y[0] != 'quote' or a[0] != 'con' or k[0] != 'nat': return STUCK
        return ('CHK', x, y, a[1], k[1])
    return STUCK


def decompose(t):
    """(ctx, kind, payload) with kind in value | stuck | poison | det (payload = contractum) | redex (payload = marker)."""
    ctx = []
    while True:
        tag = t[0]
        if tag in VALUE_TAGS: return ctx, 'value', t
        if tag == 'v': return ctx, 'stuck', None
        if tag == 'sim':
            k, tid, inner = t[1], t[2], t[3]
            if is_value(inner): return ctx, 'det', inner
            if k <= 0: return ctx, 'det', TO_
            ictx, ikind, ipay = decompose(inner)
            if ikind == 'stuck': return ctx, 'det', TO_
            ctx.append(('sim', k, tid))
            ctx.extend(ictx)
            return ctx, ikind, ipay
        if tag == 'if':
            if not is_value(t[1]):
                ctx.append(('hole', t, 1)); t = t[1]; continue
            out = contract(t)
            if out is STUCK: return ctx, 'stuck', None
            if out is POISON_READ: return ctx, 'poison', None
            return ctx, 'det', out
        start = 2 if tag == 'mk' else 1
        for i in range(start, len(t)):
            if not is_value(t[i]):
                ctx.append(('hole', t, i)); t = t[i]; break
        else:
            if tag == 'pair': return ctx, 'value', t
            out = contract(t)
            if out is STUCK: return ctx, 'stuck', None
            if out is POISON_READ: return ctx, 'poison', None
            if out[0] in MARKERS:
                return ctx, 'redex', out
            return ctx, 'det', out
        continue


def plug(ctx, x, dec=1):
    """Rebuild the term from frames, plugging x; every sim frame's fuel is decreased by `dec`."""
    for fr in reversed(ctx):
        if fr[0] == 'sim':
            x = ('sim', fr[1] - dec, fr[2], x)
        else:
            node, i = fr[1], fr[2]
            x = node[:i] + (x,) + node[i + 1:]
    return x


def innermost_tid(ctx):
    for fr in reversed(ctx):
        if fr[0] == 'sim': return fr[2]
    return 0


def initial(p, q):
    return ('app', ('app', p, ('quote', p)), ('quote', q))


EMPTY_STORE = (0, ())


def istate(p, q):
    return (initial(p, q), EMPTY_STORE)


def store_get(store, key):
    for k2, d in store[1]:
        if k2 == key: return d
    return None


def store_put(store, key, d):
    return (store[0], tuple(sorted(store[1] + ((key, d),))))


# ----------------------------------------------------------------------------------------------------------------
# 3. K_T^tape: Theory, Search, Prover
# ----------------------------------------------------------------------------------------------------------------
class TTheory(L.Theory):
    """Interning of K_T^tape formulas.  A state is (term, store); atoms are <state> => a.  The state step is
    ('value', v) | ('stuck',) | ('det', state) | ('prove', c, fv, stateT, stateF) | ('tape', [state_d]) | ('opaque',)."""

    def __init__(self, r):
        super().__init__()
        self.r = r
        self._ts = {}

    def state_step(self, state):
        r = self._ts.get(state)
        if r is None:
            r = self._ts[state] = self._tstep(state)
        return r

    def _tstep(self, state):
        t, store = state
        ctx, kind, pay = decompose(t)
        if kind == 'value': return ('value', t)
        if kind in ('stuck', 'poison'): return ('stuck',)
        if kind == 'det': return ('det', (plug(ctx, pay), store))
        tag = pay[0]
        if tag == 'PROVE':
            return ('prove', pay[1], pay[2], (plug(ctx, T_), store), (plug(ctx, F_), store))
        if tag == 'RUN':
            ctr, digs = store
            tid = ctr + 1
            term = ('sim', pay[1], tid, ('app', ('app', pay[2][1], pay[2]), pay[3]))
            return ('det', (plug(ctx, term), (tid, digs)))
        if tag == 'TAPE':
            i = pay[1]
            tid = innermost_tid(ctx)
            d = store_get(store, (tid, i))
            if d is not None: return ('det', (plug(ctx, nat(d)), store))
            return ('tape', [(plug(ctx, nat(d)), store_put(store, (tid, i), d)) for d in range(self.r)])
        if tag == 'HQ':
            cost = qnodes(pay[2])
            fuels = [fr[1] for fr in ctx if fr[0] == 'sim']
            exceeded = [i for i, v in enumerate(fuels) if v < cost]
            if not exceeded:
                return ('det', (plug(ctx, nat(hash_value(pay[2], pay[1])), dec=cost), store))
            # the hash costs more than an enclosing sim has left: that sim times out (as in actual play)
            mv = min(fuels[i] for i in exceeded)
            i0 = min(i for i in exceeded if fuels[i] == mv)
            nsim = 0; cut = None
            for j, fr in enumerate(ctx):
                if fr[0] == 'sim':
                    if nsim == i0: cut = j; break
                    nsim += 1
            return ('det', (plug(ctx[:cut], TO_, dec=mv + 1), store))
        return ('opaque',)

    def from_fv(self, fv):
        i = self._fv.get(fv)
        if i is not None: return i
        k = fv[0]
        if k == 'plays': i = self.reading(istate(fv[1], fv[2]), fv[3])
        elif k == 'bot': i = self.BOT
        elif k == 'top': i = self.TOP
        elif k == 'not': i = self.f(('not', self.from_fv(fv[1])))
        elif k == 'box': i = self.f(('box', fv[1], self.from_fv(fv[2])))
        else: i = self.f((k, self.from_fv(fv[1]), self.from_fv(fv[2])))
        self._fv[fv] = i
        return i

    def plays(self, p, q, a): return self.reading(istate(p, q), a)

    def reading(self, state, a):
        r = self.state_step(state)
        if r[0] == 'value': return self.TOP if r[1] == ('con', a) else self.BOT
        if r[0] == 'stuck': return self.BOT
        return self.f(('atom', state, a))

    def _atom_step(self, x):
        _, state, a = self.F[x]
        r = self.state_step(state)
        if r[0] == 'det': return ('det', self.reading(r[1], a))
        if r[0] == 'prove':
            c, fv = r[1], r[2]
            psi = self.from_fv(fv)
            return ('prove', c, psi, self.box(c, psi), self.reading(r[3], a), self.reading(r[4], a))
        if r[0] == 'tape': return ('tape', [self.reading(s, a) for s in r[1]])
        if r[0] == 'opaque': return ('opaque',)
        raise ValueError('atom with terminal state')

    def show(self, i):
        t = self.F[i]
        if t[0] == 'atom':
            return '<%s>=>%s' % (_short(t[1][0]), t[2])
        return super().show(i)


def _short(t, depth=0):
    if len(repr(t)) < 60: return repr(t)
    return repr(t)[:57] + '...'


class TSearch(L.Search):
    """lt.Search with TapeL/TapeR; `ms` is lt.Search.ms with these rules added (the rest is inherited)."""

    def _succ(self, x):
        th = self.th; t = th.F[x]; k = t[0]
        if k == 'atom':
            s = th.atom_step(x)
            if s[0] == 'det': return [s[1]]
            if s[0] == 'prove': return [s[3], s[4], s[5]]
            if s[0] == 'tape': return list(s[1])
            return []
        if k == 'box': return [t[2]]
        if k == 'not': return [t[1]]
        if k in ('and', 'or', 'imp'): return [t[1], t[2]]
        return []

    def ms(self, L_, R, cap):
        if cap < 1: return 1
        key = (L_, R)
        e = self.memo.get(key)
        if e is not None:
            v, exact = e
            if exact or v > cap: return v
        self.work += 1
        if self.work > self.limit: raise L.WorkExceeded()
        ax = self.axiom(L_, R)
        if ax is not None:
            self.memo[key] = (1, True); self.arg[key] = ax
            return 1
        best = INF; arg = None
        lb = INF
        th = self.th; F = th.F
        c = cap

        def one(P, tag, x):
            nonlocal best, arg, lb
            lim = min(c, best - 1) - 1
            s = self.ms(P[0], P[1], lim)
            if s <= lim:
                best, arg = 1 + s, (tag, x, [P])
            else:
                lb = min(lb, 1 + s)

        def many(Ps, tag, x):
            nonlocal best, arg, lb
            lim = min(c, best - 1)
            tot = 1; n = len(Ps)
            for idx, P in enumerate(Ps):
                after = n - idx - 1
                rem = lim - tot - after
                s = self.ms(P[0], P[1], rem)
                if s > rem:
                    lb = min(lb, tot + s + after); return
                tot += s
            best, arg = tot, (tag, x, list(Ps))

        for x in self.srt(L_):
            t = F[x]; k = t[0]
            Lx = L_ - {x}
            if k == 'not': one((Lx, R | {t[1]}), 'notL', x)
            elif k == 'and': one((Lx | {t[1], t[2]}, R), 'andL', x)
            elif k == 'or': many([(Lx | {t[1]}, R), (Lx | {t[2]}, R)], 'orL', x)
            elif k == 'imp': many([(Lx, R | {t[1]}), (Lx | {t[2]}, R)], 'impL', x)
            elif k == 'atom':
                s0 = th.atom_step(x)
                if s0[0] == 'det': one((Lx | {s0[1]}, R), 'EvL', x)
                elif s0[0] == 'prove':
                    _, cc, psi, bx, rT, rF = s0
                    many([(Lx | {bx, rT}, R), (Lx | {rF}, R | {bx})], 'PrvL', x)
                elif s0[0] == 'tape':
                    one((Lx | set(s0[1]), R), 'TapeL', x)
        for x in self.srt(R):
            t = F[x]; k = t[0]
            Rx = R - {x}
            if k == 'not': one((L_ | {t[1]}, Rx), 'notR', x)
            elif k == 'or': one((L_, Rx | {t[1], t[2]}), 'orR', x)
            elif k == 'imp': one((L_ | {t[1]}, Rx | {t[2]}), 'impR', x)
            elif k == 'and': many([(L_, Rx | {t[1]}), (L_, Rx | {t[2]})], 'andR', x)
            elif k == 'atom':
                s0 = th.atom_step(x)
                if s0[0] == 'det': one((L_, Rx | {s0[1]}), 'EvR', x)
                elif s0[0] == 'prove':
                    _, cc, psi, bx, rT, rF = s0
                    many([(L_ | {bx}, Rx | {rT}), (L_, Rx | {bx, rF})], 'PrvR', x)
                elif s0[0] == 'tape':
                    many([(L_, Rx | {rid}) for rid in s0[1]], 'TapeR', x)
            elif k == 'box':
                bc, A = t[1], t[2]
                lim = min(bc, min(c, best - 1) - 1)
                P = (frozenset(), frozenset([A]))
                s = self.ms(P[0], P[1], lim)
                if s <= lim:
                    best, arg = 1 + s, ('Nec', x, [P])
                elif s <= bc:
                    lb = min(lb, 1 + s)
            if self.jlob and k not in ('top', 'bot'):
                lim = min(c, best - 1)
                j = self.J(x, lim)
                if j <= lim:
                    best, arg = j, ('JLob', x, [])
                else:
                    lb = min(lb, j)
        if best <= cap:
            self.memo[key] = (best, True); self.arg[key] = arg
            return best
        v = max(lb, cap + 1)
        old = self.memo.get(key)
        if old is None or (not old[1] and old[0] < v):
            self.memo[key] = (v, False)
        return v


class TProver(L.Prover):
    def __init__(self, r, limit=None, jlob=True):
        super().__init__(th=TTheory(r), jlob=jlob, limit=limit)
        self.r = r

    def query(self, psi, c):
        key = (psi, c)
        r = self.cache.get(key)
        if r is not None: return r
        try:
            s = TSearch(self.th, psi, jlob=self.jlob, mem=self.mem, limit=self.limit)
            try:
                found, sz = s.prove(c)
                r = {'found': found, 'size': sz, 'W': s.work, 'complete': True, 'merges': s.merges,
                     'closure': len(s.closure)}
            except L.WorkExceeded:
                r = {'found': None, 'size': None, 'W': s.work, 'complete': False, 'merges': s.merges,
                     'closure': len(s.closure)}
            r['search'] = s if r.get('found') else None
        except RuntimeError:
            r = {'found': None, 'size': None, 'W': INF, 'complete': False, 'merges': 0, 'closure': INF, 'search': None}
        self.cache[key] = r
        return r

    def witness(self, psi, c):
        r = self.query(psi, c)
        if not r.get('found'): return None
        return r['search'].witness(frozenset(), frozenset([psi]))


# ----------------------------------------------------------------------------------------------------------------
# 4. The exact engine: actual play over the finite random decision tree, search-charged
# ----------------------------------------------------------------------------------------------------------------
ROUTES = ('plain', 'search', 'enum', 'check', 'sim')


class EnumCap(Exception):
    pass


class Engine:
    """Exact evaluation of `x <x> <y>` under fuel K with search-charged `prove`, a tape alphabet of r digits, threshold
    denominator den = r**m.  Every tape read branches over the unassigned (invocation, position) digit; leaf weights are
    exact Fractions.  `dist(x, y)` returns the exact distribution of x's play against y (the two roots are independent)."""

    def __init__(self, prover, K, r, m, enum_cap_default=400):
        self.prover = prover; self.th = prover.th
        self.K = K; self.r = r; self.m = m; self.den = r ** m
        self.in_enum = 0
        self.cache = {}
        self.stats = dict(prove=0, prp=0, chk=0, chk_rej=0)

    # -- one evaluation, exploring the tape tree ---------------------------------------------------------------
    def explore(self, t, store, used, rt, w, emit, mode=None):
        """mode: None (branch on fresh tape reads) | ['orc', digits, pos] (forced digits in order of first read) |
        ['assign', dict] (a complete assignment (invocation, position) -> digit, the padded-space reference)."""
        K = self.K
        th = self.th
        while True:
            ctx, kind, pay = decompose(t)
            if kind == 'value':
                if mode is not None and mode[0] == 'orc' and mode[2] < len(mode[1]):
                    emit(w, 'LONG', used, rt, 'long'); return
                out = t[1] if (t[0] == 'con' and t[1] in ACTIONS) else 'BOT'
                emit(w, out, used, rt, 'value' if out != 'BOT' else 'other-value'); return
            if kind == 'stuck':
                emit(w, 'BOT', used, rt, 'stuck'); return
            if kind == 'poison':
                emit(w, 'POISON', used, rt, 'poison'); return
            if used >= K:
                emit(w, 'BOT', used, rt, 'K'); return
            insim = any(fr[0] == 'sim' for fr in ctx)
            if kind == 'det':
                t = plug(ctx, pay); used += 1
                rt = _addrt(rt, 4 if insim else 0, 1)
                continue
            tag = pay[0]
            if tag == 'RUN':
                ctr, digs = store
                tid = ctr + 1
                term = ('sim', pay[1], tid, ('app', ('app', pay[2][1], pay[2]), pay[3]))
                t = plug(ctx, term); used += 1; store = (tid, digs)
                rt = _addrt(rt, 4 if insim else 0, 1)
                continue
            if tag == 'TAPE':
                i = pay[1]
                tid = innermost_tid(ctx)
                d = store_get(store, (tid, i))
                rt = _addrt(rt, 4 if insim else 0, 1)
                used += 1
                if d is not None:
                    t = plug(ctx, nat(d)); continue
                if mode is None:
                    for d in range(self.r):
                        self.explore(plug(ctx, nat(d)), store_put(store, (tid, i), d), used, rt, w / self.r, emit, None)
                    return
                if mode[0] == 'orc':
                    if mode[2] >= len(mode[1]):
                        emit(w, 'SHORT', used, rt, 'short'); return
                    d = mode[1][mode[2]]; mode[2] += 1
                    if not (isinstance(d, int) and 0 <= d < self.r):
                        emit(w, 'BADDIGIT', used, rt, 'bad'); return
                else:
                    d = mode[1][(tid, i)]
                store = store_put(store, (tid, i), d)
                t = plug(ctx, nat(d)); continue
            # multi-step primitives: cost, result
            if tag == 'PROVE':
                psi = th.from_fv(pay[2])
                q = self.prover.query(psi, pay[1])
                self.stats['prove'] += 1
                W = q['W'] if q['complete'] else INF
                res = T_ if q['found'] else F_
                cost, route = W, 1
            elif tag == 'HQ':
                cost = qnodes(pay[2]); res = nat(hash_value(pay[2], pay[1])); route = 4 if insim else 0
            elif tag == 'PRP':
                ok, cost = self.do_prp(pay[1], pay[2], pay[3], pay[4], pay[5])
                res = T_ if ok else F_; route = 2
            else:   # CHK
                ok, cost = self.do_chk(pay[1], pay[2], pay[3], pay[4])
                res = T_ if ok else F_; route = 3
            G = K - used
            fuels = [fr[1] for fr in ctx if fr[0] == 'sim']
            counters = [G] + fuels
            exceeded = [i for i, v in enumerate(counters) if v < cost]
            if not exceeded:
                t = plug(ctx, res, dec=cost); used += cost
                rt = _addrt(rt, route, cost)
                continue
            mv = min(counters[i] for i in exceeded)
            i0 = min(i for i in exceeded if counters[i] == mv)
            if i0 == 0:
                rt = _addrt(rt, route, K - used)
                emit(w, 'BOT', K, rt, 'K-search'); return
            nsim = 0; cut = None
            for j, fr in enumerate(ctx):
                if fr[0] == 'sim':
                    nsim += 1
                    if nsim == i0: cut = j; break
            t = plug(ctx[:cut], TO_, dec=mv + 1); used += mv + 1
            rt = _addrt(rt, route, mv + 1)

    # -- distributions ---------------------------------------------------------------------------------------------
    def dist(self, x, y):
        """Exact distribution of x's play against y: dict(dist, steps, route, fuel, leaves)."""
        key = (x, y)
        r = self.cache.get(key)
        if r is not None: return r
        acc = {}; steps = [Fraction(0)]; route = [Fraction(0)] * 5; fuel = [Fraction(0)]; leaves = [0]

        def emit(w, out, used, rt, reason):
            acc[out] = acc.get(out, Fraction(0)) + w
            steps[0] += w * used
            for i in range(5): route[i] += w * rt[i]
            if reason in ('K', 'K-search'): fuel[0] += w
            leaves[0] += 1

        self.explore(initial(x, y), EMPTY_STORE, 0, (0, 0, 0, 0, 0), Fraction(1), emit)
        r = dict(dist=acc, steps=steps[0], route=dict(zip(ROUTES, route)), fuel=fuel[0], leaves=leaves[0])
        self.cache[key] = r
        return r

    def leaves_of(self, x_term, y_val, cap=None):
        """All leaves of x(<x>, y_val) as (weight, outcome, steps), aborting with EnumCap past `cap` total charge."""
        out = []; tot = [1]

        def emit(w, o, used, rt, reason):
            out.append((w, o, used)); tot[0] += 1 + used
            if cap is not None and tot[0] > cap: raise EnumCap()

        self.explore(('app', ('app', x_term, ('quote', x_term)), y_val), EMPTY_STORE, 0, (0, 0, 0, 0, 0), Fraction(1), emit)
        return out

    # -- counted probability: enumeration --------------------------------------------------------------------------
    def do_prp(self, b, xq, yq, a, k):
        """Returns (result, charge).  Enumeration replays every leaf; charge = 1 + sum(1 + steps), capped at b.  A prp
        reached inside an enumeration returns F for 1 step."""
        self.stats['prp'] += 1
        if self.in_enum: return False, 1
        self.in_enum += 1
        try:
            try:
                leaves = self.leaves_of(xq[1], yq, cap=b)
            except EnumCap:
                return False, b
        finally:
            self.in_enum -= 1
        charge = 1 + sum(1 + u for (_, _, u) in leaves)
        p = sum((w for (w, o, _) in leaves if o == a), Fraction(0))
        return p >= Fraction(k, self.den), charge

    # -- counted probability: certificate check --------------------------------------------------------------------
    def do_chk(self, xq, yq, a, k):
        """Returns (accepted, charge); charge = 1 + sum over replayed prefixes of (1 + steps)."""
        self.stats['chk'] += 1
        ok, charge, why = self.check_cert(xq[1], a, k)
        if not ok: self.stats['chk_rej'] += 1
        return ok, charge

    def check_cert(self, x, a, k, K=None):
        K = self.K if K is None else K
        cert = parse_cert(x)
        if cert is None: return False, 1, 'no-cert'
        stamp, entries = cert
        if stamp != K: return False, 1, 'stamp'
        mine = [pf for (act, pf) in entries if act == a]
        if len(mine) != 1: return False, 1, 'entry'
        prefixes = mine[0]
        for p in prefixes:
            if not all(isinstance(d, int) and 0 <= d < self.r for d in p): return False, 1, 'digit'
        tp = [tuple(p) for p in prefixes]
        if len(set(tp)) != len(tp): return False, 1, 'duplicate'
        for i in range(len(tp)):
            for j in range(len(tp)):
                if i != j and tp[j][:len(tp[i])] == tp[i]: return False, 1, 'overlap'
        charge = 1; weight = Fraction(0)
        for p in tp:
            res = []

            def emit(w, o, used, rt, reason, res=res):
                res.append((o, used))

            mode = ['orc', list(p), 0]
            self.in_enum += 1
            try:
                self.explore(('app', ('app', x, ('quote', x)), POISON), EMPTY_STORE, 0, (0, 0, 0, 0, 0), Fraction(1), emit, mode)
            finally:
                self.in_enum -= 1
            (o, used) = res[0]
            charge += 1 + used
            if o != a: return False, charge, 'wrong-outcome:%s' % o
            weight += Fraction(1, self.r ** len(p))
        if weight < Fraction(k, self.den): return False, charge, 'weight'
        return True, charge, 'ok'

    # -- the padded-space reference ------------------------------------------------------------------------------
    def dist_padded(self, x, y, ninv=2):
        """Reference semantics: enumerate every complete assignment of m digits for each of the first `ninv` invocations
        (invocation 0 = root, 1.. = successive `run`s), uniform weight r**(-m ninv).  Equals `dist` when the evaluation
        creates at most ninv-1 sims and reads at most m digits per invocation."""
        import itertools
        acc = {}; steps = Fraction(0)
        ndig = self.m * ninv
        total = self.r ** ndig
        for digs in itertools.product(range(self.r), repeat=ndig):
            assign = {(tid, i): digs[tid * self.m + i] for tid in range(ninv) for i in range(self.m)}
            res = []

            def emit(w, o, used, rt, reason, res=res):
                res.append((o, used))

            self.explore(initial(x, y), EMPTY_STORE, 0, (0, 0, 0, 0, 0), Fraction(1), emit, ['assign', assign])
            o, used = res[0]
            acc[o] = acc.get(o, Fraction(0)) + Fraction(1, total)
            steps += Fraction(used, total)
        return dict(dist=acc, steps=steps)


def _addrt(rt, i, n):
    l = list(rt); l[i] += n
    return tuple(l)


# ----------------------------------------------------------------------------------------------------------------
# 5. Certificates (count certificates carried in the source)
# ----------------------------------------------------------------------------------------------------------------
def parse_cert(x):
    """(stamp, [(action, [prefix digit lists])]) from a carrier `\\me.\\them. (\\certs. BODY) CERTS`, else None."""
    if x[0] != 'lam' or x[1][0] != 'lam': return None
    b = x[1][1]
    if b[0] != 'app' or b[1][0] != 'lam': return None
    certs = b[2]
    if not is_value(certs) or certs[0] != 'pair': return None
    st, ents = certs[1], certs[2]
    if st[0] != 'nat': return None
    lst = parse_plist(ents)
    if lst is None: return None
    out = []
    for e in lst:
        if e[0] != 'pair' or e[1][0] != 'con': return None
        pl = parse_plist(e[2])
        if pl is None: return None
        pre = []
        for p in pl:
            digs = parse_plist(p)
            if digs is None or any(d[0] != 'nat' for d in digs): return None
            pre.append([d[1] for d in digs])
        out.append((e[1][1], pre))
    return st[1], out


def make_certs(stamp, entries):
    """CERTS literal: (stamp, list of (action, list of prefixes))."""
    ents = [PAIR(con(a), plist([plist([nat(d) for d in p]) for p in pres])) for (a, pres) in entries]
    return PAIR(nat(stamp), plist(ents))


def carrier(body, certs):
    """`\\me.\\them. (\\certs. BODY) CERTS`; BODY is written for the two-binder scope and is shifted under the third."""
    return L2(('app', ('lam', shift(body, 1)), certs))


def produce_cert(engine, x_plain, a):
    """Host tactic (not charged to matches): the a-producing leaves of x's decision tree against a wildcard opponent, as
    disjoint prefixes in order of first read.  Returns None if the replay reads the opponent or the tree is not closed."""
    out = []; bad = []

    def rec(prefix):
        res = []

        def emit(w, o, used, rt, reason):
            res.append((o, used))

        mode = ['orc', list(prefix), 0]
        engine.in_enum += 1
        try:
            engine.explore(('app', ('app', x_plain, ('quote', x_plain)), POISON), EMPTY_STORE, 0, (0, 0, 0, 0, 0),
                           Fraction(1), emit, mode)
        finally:
            engine.in_enum -= 1
        o = res[0][0]
        if o == 'SHORT':
            for d in range(engine.r): rec(prefix + [d])
        elif o == a: out.append(list(prefix))
        elif o in ('POISON', 'BADDIGIT'): bad.append(o)

    rec([])
    if bad: return None
    return out


# ----------------------------------------------------------------------------------------------------------------
# 6. Truth for the soundness audit
# ----------------------------------------------------------------------------------------------------------------
class AuditError(Exception):
    pass


def ideal_all(prover, engine, state, a, cap=2000000):
    """For-all-tapes idealized truth of the atom <state> => a (prove steps resolved by box truth; opaque redexes by the
    same enumeration/check as actual play, run at the engine's fuel)."""
    th = prover.th
    n = 0
    while True:
        n += 1
        if n > cap: raise AuditError('non-terminating idealized evaluation')
        r = th.state_step(state)
        if r[0] == 'value': return r[1] == ('con', a)
        if r[0] == 'stuck': return False
        if r[0] == 'det': state = r[1]; continue
        if r[0] == 'prove':
            q = prover.query(th.from_fv(r[2]), r[1])
            if not q['complete']: raise AuditError('incomplete search in truth')
            state = r[3] if q['found'] else r[4]; continue
        if r[0] == 'tape':
            return all(ideal_all(prover, engine, s, a) for s in r[1])
        if r[0] == 'opaque':
            t, store = state
            ctx, kind, pay = decompose(t)
            if pay[0] == 'PRP': ok, _ = engine.do_prp(INF, pay[2], pay[3], pay[4], pay[5])
            else: ok, _ = engine.do_chk(pay[1], pay[2], pay[3], pay[4])
            state = (plug(ctx, T_ if ok else F_), store); continue
        raise AuditError('unknown step')


def ttruth(prover, engine, x):
    th = prover.th; t = th.F[x]; k = t[0]
    if k == 'top': return True
    if k == 'bot': return False
    if k == 'not': return not ttruth(prover, engine, t[1])
    if k == 'and': return ttruth(prover, engine, t[1]) and ttruth(prover, engine, t[2])
    if k == 'or': return ttruth(prover, engine, t[1]) or ttruth(prover, engine, t[2])
    if k == 'imp': return (not ttruth(prover, engine, t[1])) or ttruth(prover, engine, t[2])
    if k == 'box':
        q = prover.query(t[2], t[1])
        if not q['complete']: raise AuditError('incomplete search in truth')
        return bool(q['found'])
    return ideal_all(prover, engine, t[1], t[2])


def sequent_true(prover, engine, Ls, Rs):
    return (not all(ttruth(prover, engine, x) for x in Ls)) or any(ttruth(prover, engine, y) for y in Rs)


def soundness_audit(prover, engine):
    """Every found box in the cache: its content is true (for all tapes) and every sequent of its witness is true."""
    nbox = nseq = 0; bad = []; skipped = 0
    for (psi, c), r in list(prover.cache.items()):
        if not r.get('found'): continue
        nbox += 1
        try:
            if not ttruth(prover, engine, psi): bad.append(('box', psi, c))
            w = prover.witness(psi, c)
            for node in L.wnodes(w):
                nseq += 1
                if not sequent_true(prover, engine, node['L'], node['R']): bad.append(('seq', psi, c, node['rule']))
        except AuditError:
            skipped += 1
    return nbox, nseq, bad, skipped
