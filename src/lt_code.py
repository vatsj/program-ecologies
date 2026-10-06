"""The realizable language, milestone 3: the prover as code (specs/2026-10-06-prover-as-code.md; notes/prover-as-code.md;
frozen design in predictions/2026-10-06-prover-as-code.md).

L_T^code: L_T without the prove primitive and formula values, plus arithmetic, capk (bounded call), a public library
(lib n / libsrc i).  The checker, the self-interpreter and the search are L_T^code terms in the library (written in a
small s-expression surface syntax compiled to de Bruijn terms by `compile_library`).

Parts:
  1. terms, quote encodings, canonical (full) encodings;
  2. the reference small-step stepper (substitution semantics, one step per contraction) -- the definition;
  3. a fast evaluator (closure compilation) with exact step accounting, sim frames, and a cache of core runs
     (a deterministic function of its argument, replayed with exact charging);
  4. the s-expression compiler and the library source (self-interpreter, core search, checker, wrappers);
  5. the catalogue of programs;
  6. the host oracle: the same search algorithm in Python over the reference stepper;
  7. the independent replay checker.
"""
import sys
import threading

sys.setrecursionlimit(2000000)

INF = 10 ** 15

# ----------------------------------------------------------------------------------------------------------------
# 1. Terms and encodings
# ----------------------------------------------------------------------------------------------------------------
TAGS = ['v', 'lam', 'app', 'con', 'nat', 'pair', 'fst', 'snd', 'if', 'fix', 'quote', 'eq', 'lib', 'op', 'capk',
        'run', 'sim', 'libsrc']
TAGCODE = {t: i for i, t in enumerate(TAGS)}
CONS = ['C', 'D', 'T', 'F', 'TO']
CONCODE = {c: i for i, c in enumerate(CONS)}
OPS = ['add', 'sub', 'mul', 'div', 'mod', 'le', 'lt']
OPCODE = {o: i for i, o in enumerate(OPS)}
VALUE_TAGS = ('lam', 'con', 'nat', 'quote', 'fix', 'lib')

C_, D_, T_, F_, TO_ = (('con', c) for c in CONS)


def is_value(t):
    tag = t[0]
    if tag in VALUE_TAGS: return True
    if tag == 'pair': return is_value(t[1]) and is_value(t[2])
    return False


def plist(xs):
    out = ('nat', 0)
    for x in reversed(xs): out = ('pair', x, out)
    return out


def quote_payload(t):
    """Payload (as a term-level value) of the nested-pair encoding of t: quote(t) behaves as pair(nat tag, payload)."""
    tag = t[0]
    Q = lambda s: ('quote', s)
    if tag in ('v', 'nat', 'lib'): return ('nat', t[1])
    if tag in ('lam', 'fix', 'quote'): return Q(t[1])
    if tag == 'con': return ('nat', CONCODE[t[1]])
    if tag == 'op': return ('pair', ('nat', OPCODE[t[1]]), plist([Q(t[2]), Q(t[3])]))
    if tag == 'sim': return ('pair', ('nat', t[1]), Q(t[2]))
    return plist([Q(a) for a in t[1:]])


_canon_cache = {}


def canon_term(t):
    """Canonical full encoding of the term t (nested Python tuples of ints): (tagcode, canon(payload))."""
    k = id(t)
    e = _canon_cache.get(k)
    if e is not None and e[0] is t: return e[1]
    c = (TAGCODE[t[0]], canon_tval(quote_payload(t)))
    _canon_cache[k] = (t, c)
    return c


def canon_tval(v):
    """Canonical full encoding of a term-level value."""
    tag = v[0]
    if tag == 'nat': return v[1]
    if tag == 'con': return v[1]
    if tag == 'pair': return (canon_tval(v[1]), canon_tval(v[2]))
    if tag == 'quote': return canon_term(v[1])
    return canon_term(v)          # function values compare as their own term's encoding


def values_equal(a, b):
    if a == b: return True
    return canon_tval(a) == canon_tval(b)


def term_of_enc(e):
    """Decode a canonical encoding (ints/tuples) back into a term (inverse of canon_term)."""
    tag = TAGS[e[0]]
    p = e[1]
    def lst(x):
        out = []
        while x != 0:
            out.append(x[0]); x = x[1]
        return out
    if tag in ('v', 'nat', 'lib'): return (tag, p)
    if tag in ('lam', 'fix', 'quote'): return (tag, term_of_enc(p))
    if tag == 'con': return ('con', CONS[p])
    if tag == 'op':
        ch = lst(p[1]); return ('op', OPS[p[0]], term_of_enc(ch[0]), term_of_enc(ch[1]))
    if tag == 'sim': return ('sim', p[0], term_of_enc(p[1]))
    return (tag,) + tuple(term_of_enc(c) for c in lst(p))


# ----------------------------------------------------------------------------------------------------------------
# 2. Reference stepper (the definition of the semantics)
# ----------------------------------------------------------------------------------------------------------------
LIB = []                 # library terms (each a ('lam', body)); filled by compile_library
LIBNAME = {}
SEARCH_LIBS = {}         # lib index -> core id i, for SEARCH_i
CORE_LIBS = {}           # lib index -> core id i, for CORE_i (and CORE_W variants map to -1-i)


def subst(t, v, d=0):
    tag = t[0]
    if tag == 'v':
        i = t[1]
        if i == d: return v
        if i > d: return ('v', i - 1)
        return t
    if tag in ('con', 'nat', 'quote', 'lib'): return t
    if tag in ('lam', 'fix'): return (tag, subst(t[1], v, d + 1))
    if tag == 'op': return ('op', t[1], subst(t[2], v, d), subst(t[3], v, d))
    if tag == 'sim': return ('sim', t[1], subst(t[2], v, d))
    return (tag,) + tuple(subst(a, v, d) for a in t[1:])


STUCK = 'stuck'
_OPF = {'add': lambda a, b: a + b, 'sub': lambda a, b: max(0, a - b), 'mul': lambda a, b: a * b,
        'div': lambda a, b: a // b if b else None, 'mod': lambda a, b: a % b if b else None,
        'le': lambda a, b: a <= b, 'lt': lambda a, b: a < b}


def contract(r):
    """Contract a redex whose evaluated subterms are values: contractum, STUCK, or ('SEARCH', i, v)."""
    tag = r[0]
    if tag == 'app':
        f, a = r[1], r[2]
        if f[0] == 'lam': return subst(f[1], a)
        if f[0] == 'fix': return ('app', subst(f[1], f), a)
        if f[0] == 'lib':
            n = f[1]
            if n in SEARCH_LIBS: return ('SEARCH', SEARCH_LIBS[n], a)
            if 0 <= n < len(LIB): return subst(LIB[n][1], a)
        return STUCK
    if tag == 'if':
        c = r[1]
        if c == T_: return r[2]
        if c == F_: return r[3]
        return STUCK
    if tag in ('fst', 'snd'):
        p = r[1]
        if p[0] == 'pair': return p[1] if tag == 'fst' else p[2]
        if p[0] == 'quote':
            return ('nat', TAGCODE[p[1][0]]) if tag == 'fst' else quote_payload(p[1])
        return STUCK
    if tag == 'eq': return T_ if values_equal(r[1], r[2]) else F_
    if tag == 'op':
        a, b = r[2], r[3]
        if a[0] != 'nat' or b[0] != 'nat': return STUCK
        x = _OPF[r[1]](a[1], b[1])
        if x is None: return STUCK
        if isinstance(x, bool): return T_ if x else F_
        return ('nat', x)
    if tag == 'capk':
        k, f, v = r[1], r[2], r[3]
        if k[0] != 'nat': return STUCK
        return ('sim', k[1], ('app', f, v))
    if tag == 'run':
        k, x, y = r[1], r[2], r[3]
        if k[0] != 'nat' or x[0] != 'quote' or y[0] != 'quote': return STUCK
        return ('sim', k[1], ('app', ('app', x[1], x), y))
    if tag == 'libsrc':
        i = r[1]
        if i[0] != 'nat' or not (0 <= i[1] < len(LIB)): return STUCK
        return ('quote', LIB[i[1]])
    return STUCK


def decompose(t):
    """(ctx, kind, payload, isTO): kind 'value' | 'stuck' | 'det' (payload contractum) | 'search' (payload (i, v)).
    ctx: frames outermost first; a frame is ('hole', node, index) or ('sim', k)."""
    ctx = []
    while True:
        tag = t[0]
        if tag in VALUE_TAGS: return ctx, 'value', t, 0
        if tag == 'v': return ctx, 'stuck', None, 0
        if tag == 'sim':
            k, inner = t[1], t[2]
            if is_value(inner): return ctx, 'det', inner, 0
            if k == 0: return ctx, 'det', TO_, 1
            ictx, ikind, ipay, ito = decompose(inner)
            if ikind == 'stuck': return ctx, 'det', TO_, 1
            ctx.append(('sim', k)); ctx.extend(ictx)
            return ctx, ikind, ipay, ito
        if tag == 'if':
            if not is_value(t[1]):
                ctx.append(('hole', t, 1)); t = t[1]; continue
            out = contract(t)
            return (ctx, 'stuck', None, 0) if out is STUCK else (ctx, 'det', out, 0)
        start = 2 if tag == 'op' else 1
        for i in range(start, len(t)):
            if not is_value(t[i]):
                ctx.append(('hole', t, i)); t = t[i]; break
        else:
            if tag == 'pair': return ctx, 'value', t, 0
            out = contract(t)
            if out is STUCK: return ctx, 'stuck', None, 0
            if out[0] == 'SEARCH': return ctx, 'search', (out[1], out[2]), 0
            return ctx, 'det', out, 0


def plug(ctx, x, dec=1):
    for fr in reversed(ctx):
        if fr[0] == 'sim':
            x = ('sim', max(0, fr[1] - dec), x)
        else:
            node, i = fr[1], fr[2]
            x = node[:i] + (x,) + node[i + 1:]
    return x


def step(t):
    """('value',) | ('stuck',) | ('det', t', isTO) | ('search', i, v, ctx)."""
    ctx, kind, pay, ito = decompose(t)
    if kind == 'value': return ('value',)
    if kind == 'stuck': return ('stuck',)
    if kind == 'det': return ('det', plug(ctx, pay), ito)
    return ('search', pay[0], pay[1], ctx)


def ref_run(t, K, search_oracle=None, trace=None):
    """Run t with global fuel K under the reference semantics, stepping into search calls (so the whole library
    runs step by step).  Returns (value-or-'BOT', steps)."""
    used = 0
    while True:
        if trace is not None: trace.append(t)
        ctx, kind, pay, ito = decompose(t)
        if kind == 'value': return t, used
        if kind == 'stuck': return 'BOT', used
        if used >= K: return 'BOT', used
        if kind == 'det':
            t = plug(ctx, pay); used += 1; continue
        # search call: it is an ordinary application of lib SEARCH_i
        i, v = pay
        n = [k for k, j in SEARCH_LIBS.items() if j == i][0]
        t = plug(ctx, subst(LIB[n][1], v)); used += 1


# ----------------------------------------------------------------------------------------------------------------
# 3. The fast evaluator (closure compilation) with exact step accounting
# ----------------------------------------------------------------------------------------------------------------
class OutOfFuel(Exception):
    pass


class Stuck(Exception):
    pass


class SimTO(Exception):
    def __init__(self, idx):
        self.idx = idx


class Q:
    """A quote value.  Equality and hashing by canonical encoding (so a quote equals its explicit encoding)."""
    __slots__ = ('t', '_c', '_p')

    def __init__(self, t):
        self.t = t; self._c = None; self._p = None

    def canon(self):
        if self._c is None: self._c = canon_term(self.t)
        return self._c

    def fst(self): return TAGCODE[self.t[0]]

    def snd(self):
        if self._p is None: self._p = tval_to_rt(quote_payload(self.t))
        return self._p

    def __eq__(self, o):
        if isinstance(o, Q): return self.t == o.t or self.canon() == o.canon()
        if isinstance(o, (tuple, Clo, FixV, LibV)): return self.canon() == canon_rt(o)
        return False

    def __hash__(self): return hash(self.canon())

    def __repr__(self): return 'Q(%s)' % (self.t[0],)


class Clo:
    __slots__ = ('code', 'env', 'body')

    def __init__(self, code, env, body):
        self.code = code; self.env = env; self.body = body

    def term(self): return ('lam', subst_env(self.body, self.env, 1))

    def __eq__(self, o):
        if isinstance(o, (int, str)): return False
        return canon_rt(self) == canon_rt(o)

    def __hash__(self): return hash(canon_rt(self))


class FixV:
    __slots__ = ('code', 'env', 'body')

    def __init__(self, code, env, body):
        self.code = code; self.env = env; self.body = body

    def term(self): return ('fix', subst_env(self.body, self.env, 1))

    def __eq__(self, o):
        if isinstance(o, (int, str)): return False
        return canon_rt(self) == canon_rt(o)

    def __hash__(self): return hash(canon_rt(self))


class LibV:
    __slots__ = ('n',)

    def __init__(self, n): self.n = n

    def term(self): return ('lib', self.n)

    def __eq__(self, o):
        if isinstance(o, LibV): return self.n == o.n
        if isinstance(o, (int, str)): return False
        return canon_rt(self) == canon_rt(o)

    def __hash__(self): return hash(canon_rt(self))


def canon_rt(v):
    if type(v) is int or type(v) is str: return v
    if type(v) is tuple: return (canon_rt(v[0]), canon_rt(v[1]))
    if type(v) is Q: return v.canon()
    return canon_term(v.term())


def tval_to_rt(v):
    """Term-level value -> runtime value."""
    tag = v[0]
    if tag == 'nat': return v[1]
    if tag == 'con': return v[1]
    if tag == 'pair': return (tval_to_rt(v[1]), tval_to_rt(v[2]))
    if tag == 'quote': return Q(v[1])
    if tag == 'lib': return LibV(v[1])
    if tag == 'lam': return Clo(compile_term(v[1], 1), None, v[1]) if False else _closed_lam(v)
    if tag == 'fix': return _closed_fix(v)
    raise ValueError(v)


def rt_to_tval(v):
    """Runtime value -> term-level value."""
    if type(v) is int: return ('nat', v)
    if type(v) is str: return ('con', v)
    if type(v) is tuple: return ('pair', rt_to_tval(v[0]), rt_to_tval(v[1]))
    if type(v) is Q: return ('quote', v.t)
    return v.term()


def subst_env(t, env, depth):
    """Replace free variables of t (index >= depth) by the runtime values of env (index depth -> env[0])."""
    tag = t[0]
    if tag == 'v':
        i = t[1]
        if i < depth: return t
        e = env
        for _ in range(i - depth): e = e[1]
        return rt_to_tval(e[0])
    if tag in ('con', 'nat', 'quote', 'lib'): return t
    if tag in ('lam', 'fix'): return (tag, subst_env(t[1], env, depth + 1))
    if tag == 'op': return ('op', t[1], subst_env(t[2], env, depth), subst_env(t[3], env, depth))
    if tag == 'sim': return ('sim', t[1], subst_env(t[2], env, depth))
    return (tag,) + tuple(subst_env(a, env, depth) for a in t[1:])


# machine state (module globals for speed)
ST = [0, INF, INF]        # used, K, NEXTD (smallest sim deadline)
SIMS = []                 # sim deadlines, outermost first
MINS = []                 # prefix minima of SIMS
KEYS = []                 # call key of each sim frame (None for literal sims)
KEYCOUNT = {}
CACHE = {}                # (core lib n, k, arg) -> (result, total steps after the capk contraction)
ACTIVE = set()
EVENTS = None             # list collecting core-run events during a play, or None
STATS = {'regress': 0, 'clean': 0}
CLEAN_DEPTH = [0]


def tick():
    u = ST[0]
    if u >= ST[1]: raise OutOfFuel()
    if u >= ST[2]:
        for i, d in enumerate(SIMS):
            if d <= u:
                ST[0] = u + 1
                raise SimTO(i)
    ST[0] = u + 1


def _push(d, key):
    SIMS.append(d)
    m = d if not MINS or d < MINS[-1] else MINS[-1]
    MINS.append(m); ST[2] = m
    KEYS.append(key)
    if key is not None: KEYCOUNT[key] = KEYCOUNT.get(key, 0) + 1


def _popto(idx):
    for key in KEYS[idx:]:
        if key is not None:
            c = KEYCOUNT[key] - 1
            if c: KEYCOUNT[key] = c
            else: del KEYCOUNT[key]
    del SIMS[idx:]; del MINS[idx:]; del KEYS[idx:]
    ST[2] = MINS[-1] if MINS else INF


def enter_sim(k, thunk, key=None):
    """Evaluate sim(k, <thunk>) (the contraction that created it has been charged).  Regress lemma (notes §2): a
    call with the same key as an enclosing frame repeats that frame's computation from its start, so no level
    returns before some enclosing counter is exhausted; the run is fast-forwarded to that point."""
    if key is not None and key in KEYCOUNT:
        STATS['regress'] += 1
        ST[0] = min(ST[1], ST[2])
        tick()
        raise AssertionError('regress: tick did not fail')
    idx = len(SIMS)
    _push(ST[0] + k, key)
    try:
        v = thunk()
    except SimTO as e:
        if e.idx != idx: raise
        _popto(idx)
        return 'TO'
    except Stuck:
        _popto(idx)
        tick()
        return 'TO'
    _popto(idx)
    tick()
    return v


def apply(f, a):
    tf = type(f)
    if tf is Clo:
        tick(); return f.code((a, f.env))
    if tf is LibV:
        tick(); return LIBCODE[f.n]((a, None))
    if tf is FixV:
        tick(); g = f.code((f, f.env)); return apply(g, a)
    raise Stuck()


def do_capk(k, f, v):
    """The capk contraction has been charged by the caller; evaluate sim(k, app(f, v))."""
    key = None
    if type(f) is LibV:
        try:
            key = (f.n, k, v)
            hash(key)
        except Exception:
            key = None
    if key is not None and f.n in CORE_LIBS:
        rec = CACHE.get(key)
        if rec is None and key not in ACTIVE:
            rec = clean_run(k, f, v, key)
        if rec is not None:
            return replay_cached(rec, key)
    return enter_sim(k, lambda: apply(f, v), key)


def _save():
    return (ST[0], ST[1], ST[2], SIMS[:], MINS[:], KEYS[:], dict(KEYCOUNT))


def _restore(s):
    ST[0], ST[1], ST[2] = s[0], s[1], s[2]
    SIMS[:] = s[3]; MINS[:] = s[4]; KEYS[:] = s[5]
    KEYCOUNT.clear(); KEYCOUNT.update(s[6])


def _reset(K):
    ST[0], ST[1], ST[2] = 0, K, INF
    del SIMS[:]; del MINS[:]; del KEYS[:]; KEYCOUNT.clear()


def clean_run(k, f, v, key):
    saved = _save()
    ACTIVE.add(key)
    STATS['clean'] += 1
    _reset(INF)
    CLEAN_DEPTH[0] += 1
    try:
        res = enter_sim(k, lambda: apply(f, v), key)
        total = ST[0]
    finally:
        _restore(saved)
        ACTIVE.discard(key)
        CLEAN_DEPTH[0] -= 1
    rec = (res, total)
    CACHE[key] = rec
    return rec


def replay_cached(rec, key):
    res, total = rec
    u = ST[0]
    tfail = min(ST[1], ST[2]) - u + 1
    if EVENTS is not None and CLEAN_DEPTH[0] == 0:
        EVENTS.append((key, res, total, len(SIMS), tfail <= total))
    if tfail <= total:
        ST[0] = u + tfail - 1
        tick()
        raise AssertionError('replay: tick did not fail')
    ST[0] = u + total
    return res


def _mkvar(i):
    if i == 0: return lambda e: e[0]
    if i == 1: return lambda e: e[1][0]
    if i == 2: return lambda e: e[1][1][0]
    if i == 3: return lambda e: e[1][1][1][0]
    if i == 4: return lambda e: e[1][1][1][1][0]

    def f(e):
        for _ in range(i): e = e[1]
        return e[0]
    return f


_compiled = {}


def compile_term(t, _depth=0):
    """Compile a term into a Python closure env -> runtime value (exact contraction counting)."""
    key = id(t)
    hit = _compiled.get(key)
    if hit is not None and hit[0] is t: return hit[1]
    f = _compile(t)
    _compiled[key] = (t, f)
    return f


def _compile(t):
    tag = t[0]
    if tag == 'v':
        return _mkvar(t[1])
    if tag == 'nat':
        n = t[1]; return lambda e: n
    if tag == 'con':
        c = t[1]; return lambda e: c
    if tag == 'quote':
        q = Q(t[1]); return lambda e: q
    if tag == 'lib':
        lv = LibV(t[1]); return lambda e: lv
    if tag == 'lam':
        body = t[1]; bc = compile_term(body)
        return lambda e: Clo(bc, e, body)
    if tag == 'fix':
        body = t[1]; bc = compile_term(body)
        return lambda e: FixV(bc, e, body)
    if tag == 'pair':
        a = compile_term(t[1]); b = compile_term(t[2])
        return lambda e: (a(e), b(e))
    if tag == 'app':
        fc = compile_term(t[1]); ac = compile_term(t[2])

        def app(e):
            f = fc(e); a = ac(e)
            tf = type(f)
            if tf is Clo:
                tick(); return f.code((a, f.env))
            if tf is LibV:
                tick(); return LIBCODE[f.n]((a, None))
            return apply(f, a)
        return app
    if tag == 'if':
        cc = compile_term(t[1]); tc = compile_term(t[2]); ec = compile_term(t[3])

        def iff(e):
            c = cc(e)
            if c == 'T':
                tick(); return tc(e)
            if c == 'F':
                tick(); return ec(e)
            raise Stuck()
        return iff
    if tag in ('fst', 'snd'):
        ac = compile_term(t[1]); first = tag == 'fst'

        def fs(e):
            p = ac(e)
            tp = type(p)
            if tp is tuple:
                tick(); return p[0] if first else p[1]
            if tp is Q:
                tick(); return p.fst() if first else p.snd()
            raise Stuck()
        return fs
    if tag == 'eq':
        ac = compile_term(t[1]); bc = compile_term(t[2])

        def eqf(e):
            a = ac(e); b = bc(e)
            tick()
            if type(a) is int and type(b) is int: return 'T' if a == b else 'F'
            return 'T' if a == b else 'F'
        return eqf
    if tag == 'op':
        o = t[1]; ac = compile_term(t[2]); bc = compile_term(t[3])
        if o == 'add':
            def f(e):
                a = ac(e); b = bc(e)
                if type(a) is not int or type(b) is not int: raise Stuck()
                tick(); return a + b
        elif o == 'sub':
            def f(e):
                a = ac(e); b = bc(e)
                if type(a) is not int or type(b) is not int: raise Stuck()
                tick(); return a - b if a > b else 0
        elif o == 'mul':
            def f(e):
                a = ac(e); b = bc(e)
                if type(a) is not int or type(b) is not int: raise Stuck()
                tick(); return a * b
        elif o == 'div':
            def f(e):
                a = ac(e); b = bc(e)
                if type(a) is not int or type(b) is not int or b == 0: raise Stuck()
                tick(); return a // b
        elif o == 'mod':
            def f(e):
                a = ac(e); b = bc(e)
                if type(a) is not int or type(b) is not int or b == 0: raise Stuck()
                tick(); return a % b
        elif o == 'le':
            def f(e):
                a = ac(e); b = bc(e)
                if type(a) is not int or type(b) is not int: raise Stuck()
                tick(); return 'T' if a <= b else 'F'
        else:
            def f(e):
                a = ac(e); b = bc(e)
                if type(a) is not int or type(b) is not int: raise Stuck()
                tick(); return 'T' if a < b else 'F'
        return f
    if tag == 'capk':
        kc = compile_term(t[1]); fc = compile_term(t[2]); vc = compile_term(t[3])

        def capk(e):
            k = kc(e); f = fc(e); v = vc(e)
            if type(k) is not int: raise Stuck()
            tick()
            return do_capk(k, f, v)
        return capk
    if tag == 'run':
        kc = compile_term(t[1]); xc = compile_term(t[2]); yc = compile_term(t[3])

        def run(e):
            k = kc(e); x = xc(e); y = yc(e)
            if type(k) is not int or type(x) is not Q or type(y) is not Q: raise Stuck()
            tick()
            prog = compile_term(x.t)

            def inner():
                pv = prog(None)
                g = apply(pv, x)
                return apply(g, y)
            return enter_sim(k, inner, ('run', k, x.t, y.t))
        return run
    if tag == 'sim':
        k = t[1]; ic = compile_term(t[2])
        return lambda e: enter_sim(k, lambda: ic(e))
    if tag == 'libsrc':
        ac = compile_term(t[1])

        def ls(e):
            i = ac(e)
            if type(i) is not int or not (0 <= i < len(LIB)): raise Stuck()
            tick(); return Q(LIB[i])
        return ls
    raise ValueError('cannot compile ' + str(tag))


def _closed_lam(v):
    body = v[1]; return Clo(compile_term(body), None, body)


def _closed_fix(v):
    body = v[1]; return FixV(compile_term(body), None, body)


LIBCODE = []


def evaluate(t, K=INF, events=None):
    """Evaluate a closed term with global fuel K from a fresh context.  Returns (runtime value | 'BOT', steps)."""
    global EVENTS
    _reset(K)
    EVENTS = events
    try:
        v = compile_term(t)(None)
        return v, ST[0]
    except OutOfFuel:
        return 'BOT', ST[0]
    except Stuck:
        return 'BOT', ST[0]
    finally:
        EVENTS = None


def run_big(fn, *args, stack_mb=1024):
    """Run fn(*args) in a thread with a large stack (deep L_T recursion maps to Python recursion)."""
    out = {}

    def target():
        try:
            out['r'] = fn(*args)
        except BaseException as ex:          # pragma: no cover
            out['e'] = ex
    threading.stack_size(stack_mb * 1024 * 1024)
    th = threading.Thread(target=target)
    th.start(); th.join()
    if 'e' in out: raise out['e']
    return out['r']


# ----------------------------------------------------------------------------------------------------------------
# 4a. The s-expression surface syntax, compiled to de Bruijn L_T^code terms
# ----------------------------------------------------------------------------------------------------------------
def sx_parse(src):
    toks = src.replace('(', ' ( ').replace(')', ' ) ').split()
    out = []; stack = [out]
    for tk in toks:
        if tk == '(':
            stack[-1].append([]); stack.append(stack[-1][-1])
        elif tk == ')':
            stack.pop()
        else:
            stack[-1].append(int(tk) if tk.isdigit() else tk)
    assert len(stack) == 1, 'unbalanced'
    return out


def _strip_comments(src):
    return '\n'.join(l.split(';')[0] for l in src.split('\n'))


CONST_SYMS = {'C': C_, 'D': D_, 'T': T_, 'F': F_, 'TO': TO_}
PRIM2 = {'add', 'sub', 'mul', 'div', 'mod', 'le', 'lt'}


class SxCompiler:
    def __init__(self):
        self.defs = {}          # name -> (params, body)
        self.order = []
        self.consts = {}        # name -> sexpr (inlined)
        self.macros = {}        # name -> python fn(*args) -> sexpr
        self.index = {}

    def load(self, src):
        for form in sx_parse(_strip_comments(src)):
            if form[0] == 'def':
                name, params, body = form[1], form[2], form[3]
                assert name not in self.defs, name
                self.defs[name] = (params, body); self.order.append(name)
            elif form[0] == 'defconst':
                self.consts[form[1]] = form[2]
            else:
                raise ValueError('top-level form ' + str(form[0]))

    def expr(self, x, env):
        if isinstance(x, int): return ('nat', x)
        if isinstance(x, str):
            if x in env:
                return ('v', env[::-1].index(x))
            if x in CONST_SYMS: return CONST_SYMS[x]
            if x in self.consts: return self.expr(self.consts[x], env)
            if x in self.index: return ('lib', self.index[x])
            raise NameError(x)
        assert isinstance(x, list) and x, x
        h = x[0]
        if isinstance(h, str):
            if h in self.macros: return self.expr(self.macros[h](*x[1:]), env)
            if h == 'lambda':
                params, body = x[1], x[2]
                t = self.expr(body, env + params)
                for _ in params: t = ('lam', t)
                return t
            if h == 'let':
                binds, body = x[1], x[2]
                if not binds: return self.expr(body, env)
                (n, e), rest = binds[0], binds[1:]
                return ('app', ('lam', self.expr(['let', rest, body], env + [n])), self.expr(e, env))
            if h == 'if':
                return ('if', self.expr(x[1], env), self.expr(x[2], env), self.expr(x[3], env))
            if h == 'cond':
                clauses = x[1:]
                c0 = clauses[0]
                if c0[0] == 'else': return self.expr(c0[1], env)
                return ('if', self.expr(c0[0], env), self.expr(c0[1], env), self.expr(['cond'] + clauses[1:], env))
            if h == 'and':
                if len(x) == 2: return self.expr(x[1], env)
                return ('if', self.expr(x[1], env), self.expr(['and'] + x[2:], env), F_)
            if h == 'or':
                if len(x) == 2: return self.expr(x[1], env)
                return ('if', self.expr(x[1], env), T_, self.expr(['or'] + x[2:], env))
            if h == 'not':
                return ('if', self.expr(x[1], env), F_, T_)
            if h == 'list':
                out = ('nat', 0)
                for a in reversed(x[1:]): out = ('pair', self.expr(a, env), out)
                return out
            if h == 'pair': return ('pair', self.expr(x[1], env), self.expr(x[2], env))
            if h in ('fst', 'snd', 'libsrc'): return (h, self.expr(x[1], env))
            if h == 'eq': return ('eq', self.expr(x[1], env), self.expr(x[2], env))
            if h in PRIM2: return ('op', h, self.expr(x[1], env), self.expr(x[2], env))
            if h in ('capk', 'run'): return (h,) + tuple(self.expr(a, env) for a in x[1:])
            if h == 'lib': return ('lib', self.index[x[1]])
        t = self.expr(h, env)
        for a in x[1:]: t = ('app', t, self.expr(a, env))
        return t

    def build(self, start_index=0):
        for i, n in enumerate(self.order): self.index[n] = start_index + i
        terms = []
        for n in self.order:
            params, body = self.defs[n]
            assert params, 'library entries take at least one argument: ' + n
            t = self.expr(body, list(params))
            for _ in params: t = ('lam', t)
            terms.append(t)
        return terms


# ----------------------------------------------------------------------------------------------------------------
# 4b. The library source: wrappers, cores, self-interpreter, formulas, the search, the checker
# ----------------------------------------------------------------------------------------------------------------
# Encodings: a term t is represented by its nested-pair encoding (tag, payload) -- a quote or explicit pairs.
# Step results: (0 . 0) value; (1 . 0) stuck; (2 . (e' . isTO)) deterministic step; (3 . (i . (arg . frames)))
# a search call of SEARCH_i with argument encoding arg, frames outermost first.
# Frames: (0 . (tag . (idx . list))) strict; (1 . (opcode . (idx . list))) op; (2 . (then . else)) if; (3 . k) sim.
# Formulas: (0 . 0) top; (1 . 0) bot; (2 . A) not; (3|4|5 . (A . B)) and|or|imp; (6 . (conf . (f . (a . m)))) atom;
# (7 . (i . (c . (U . psi)))) box.
LIBRARY_SRC = r"""
; ---------------- wrappers (lib indices 0..2 are the search entry points) ----------------
(def SEARCH0 (arg) (if (eq (capk (snd (snd arg)) CORE0 arg) T) T F))
(def SEARCH1 (arg) (if (eq (capk (snd (snd arg)) CORE1 arg) T) T F))
(def SEARCH2 (arg) (if (eq (capk (snd (snd arg)) CORE2 arg) T) T F))
(def CORE0 (arg) (core 0 arg))
(def CORE1 (arg) (core 1 arg))
(def CORE2 (arg) (core 2 arg))
(def COREW0 (arg) (corew 0 arg))
(def COREW1 (arg) (corew 1 arg))
(def COREW2 (arg) (corew 2 arg))
(def CHECK0 (x) (check 0 (fst x) (snd x)))
(def CHECK1 (x) (check 1 (fst x) (snd x)))
(def CHECK2 (x) (check 2 (fst x) (snd x)))

; ---------------- small helpers ----------------
(def min (a b) (if (lt a b) a b))
(def nth (l i) (if (eq i 0) (fst l) (nth (snd l) (sub i 1))))
(def setnth (l i x) (if (eq i 0) (pair x (snd l)) (pair (fst l) (setnth (snd l) (sub i 1) x))))

; ---------------- self-interpreter ----------------
(def valtag (t) (or (eq t 1) (eq t 3) (eq t 4) (eq t 9) (eq t 10) (eq t 12)))
(def isval (e)
  (let ((t (fst e)))
    (if (valtag t) T
      (if (eq t 5) (let ((p (snd e))) (if (isval (fst p)) (isval (fst (snd p))) F)) F))))
(def firstnv (l i) (if (eq l 0) NONE (if (isval (fst l)) (firstnv (snd l) (add i 1)) i)))
(def subst (e v d)
  (let ((t (fst e)))
    (cond ((eq t 0) (let ((i (snd e))) (if (eq i d) v (if (lt d i) (pair 0 (sub i 1)) e))))
          ((or (eq t 1) (eq t 9)) (pair t (subst (snd e) v (add d 1))))
          ((or (eq t 3) (or (eq t 4) (or (eq t 10) (eq t 12)))) e)
          ((eq t 16) (let ((p (snd e))) (pair 16 (pair (fst p) (subst (snd p) v d)))))
          ((eq t 13) (let ((p (snd e))) (pair 13 (pair (fst p) (substl (snd p) v d)))))
          (else (pair t (substl (snd e) v d))))))
(def substl (l v d) (if (eq l 0) 0 (pair (subst (fst l) v d) (substl (snd l) v d))))
(def concode (n) (cond ((eq n 0) C) ((eq n 1) D) ((eq n 2) T) ((eq n 3) F) (else TO)))
(def full (e)
  (let ((t (fst e)))
    (cond ((eq t 5) (let ((p (snd e))) (pair (full (fst p)) (full (fst (snd p))))))
          ((eq t 4) (snd e))
          ((eq t 3) (concode (snd e)))
          ((eq t 10) (snd e))
          (else e))))
(def mkapp (f a) (pair 2 (pair f (pair a 0))))
(def qlistenc (l) (if (eq l 0) (pair 4 0) (pair 5 (pair (pair 10 (fst l)) (pair (qlistenc (snd l)) 0)))))
(def payenc (et)
  (let ((tg (fst et)) (p (snd et)))
    (cond ((or (eq tg 0) (or (eq tg 3) (or (eq tg 4) (eq tg 12)))) (pair 4 p))
          ((or (eq tg 1) (or (eq tg 9) (eq tg 10))) (pair 10 p))
          ((eq tg 13) (pair 5 (pair (pair 4 (fst p)) (pair (qlistenc (snd p)) 0))))
          ((eq tg 16) (pair 5 (pair (pair 4 (fst p)) (pair (pair 10 (snd p)) 0))))
          (else (qlistenc p)))))
(def det (e to) (pair 2 (pair e to)))
(def wrapr (r fr)
  (let ((k (fst r)))
    (cond ((eq k 2) (let ((q (snd r))) (det (plug1 fr (fst q) 1) (snd q))))
          ((eq k 3) (let ((q (snd r))) (pair 3 (pair (fst q) (pair (fst (snd q)) (pair fr (snd (snd q))))))))
          (else RSTUCK))))
(def plug1 (fr x dec)
  (let ((k (fst fr)) (p (snd fr)))
    (cond ((eq k 0) (pair (fst p) (setnth (snd (snd p)) (fst (snd p)) x)))
          ((eq k 1) (pair 13 (pair (fst p) (setnth (snd (snd p)) (fst (snd p)) x))))
          ((eq k 2) (pair 8 (pair x (pair (fst p) (pair (snd p) 0)))))
          (else (pair 16 (pair (sub p dec) x))))))
(def plug (frs x dec) (if (eq frs 0) x (plug1 (fst frs) (plug (snd frs) x dec) dec)))
(def step (e)
  (let ((t (fst e)))
    (cond ((valtag t) RVAL)
          ((eq t 5) (stepl t (snd e) 0))
          ((eq t 0) RSTUCK)
          ((eq t 8) (stepif (snd e)))
          ((eq t 16) (stepsim (snd e)))
          ((eq t 13) (stepop (snd e)))
          (else (stepl t (snd e) 1)))))
(def stepl (t l c)
  (let ((i (firstnv l 0)))
    (if (eq i NONE)
        (if (eq c 0) RVAL (contract t l))
        (wrapr (step (nth l i)) (pair 0 (pair t (pair i l)))))))
(def stepif (p)
  (let ((c (fst p)))
    (if (isval c)
        (let ((cv (full c)))
          (cond ((eq cv T) (det (fst (snd p)) 0))
                ((eq cv F) (det (fst (snd (snd p))) 0))
                (else RSTUCK)))
        (wrapr (step c) (pair 2 (pair (fst (snd p)) (fst (snd (snd p)))))))))
(def stepsim (p)
  (let ((k (fst p)) (inner (snd p)))
    (if (isval inner) (det inner 0)
      (if (eq k 0) (det TOENC 1)
        (let ((r (step inner)) (rk (fst r)))
          (cond ((eq rk 1) (det TOENC 1))
                ((eq rk 2) (let ((q (snd r))) (det (pair 16 (pair (sub k 1) (fst q))) (snd q))))
                (else (let ((q (snd r))) (pair 3 (pair (fst q) (pair (fst (snd q)) (pair (pair 3 k) (snd (snd q))))))))))))))
(def stepop (p)
  (let ((l (snd p)) (i (firstnv l 0)))
    (if (eq i NONE) (contractop (fst p) l)
        (wrapr (step (nth l i)) (pair 1 (pair (fst p) (pair i l)))))))
(def isnat (e) (eq (fst e) 4))
(def contractop (o l)
  (let ((a (fst l)) (b (fst (snd l))))
    (if (and (isnat a) (isnat b))
        (let ((x (snd a)) (y (snd b)))
          (cond ((eq o 0) (det (pair 4 (add x y)) 0))
                ((eq o 1) (det (pair 4 (sub x y)) 0))
                ((eq o 2) (det (pair 4 (mul x y)) 0))
                ((eq o 3) (if (eq y 0) RSTUCK (det (pair 4 (div x y)) 0)))
                ((eq o 4) (if (eq y 0) RSTUCK (det (pair 4 (mod x y)) 0)))
                ((eq o 5) (det (if (le x y) TENC FENC) 0))
                ((eq o 6) (det (if (lt x y) TENC FENC) 0))
                (else RSTUCK)))
        RSTUCK)))
(def contract (t l)
  (cond ((eq t 2) (contractapp (fst l) (fst (snd l))))
        ((or (eq t 6) (eq t 7))
           (let ((x (fst l)) (tx (fst x)))
             (cond ((eq tx 5) (det (if (eq t 6) (fst (snd x)) (fst (snd (snd x)))) 0))
                   ((eq tx 10) (det (if (eq t 6) (pair 4 (fst (snd x))) (payenc (snd x))) 0))
                   (else RSTUCK))))
        ((eq t 11) (det (if (eq (full (fst l)) (full (fst (snd l)))) TENC FENC) 0))
        ((eq t 14) (let ((k (fst l))) (if (isnat k) (det (pair 16 (pair (snd k) (mkapp (fst (snd l)) (fst (snd (snd l)))))) 0) RSTUCK)))
        ((eq t 15) (let ((k (fst l)) (x (fst (snd l))) (y (fst (snd (snd l)))))
                     (if (and (isnat k) (and (eq (fst x) 10) (eq (fst y) 10)))
                         (det (pair 16 (pair (snd k) (mkapp (mkapp (snd x) x) y))) 0) RSTUCK)))
        ((eq t 17) (let ((i (fst l))) (if (and (isnat i) (lt (snd i) NLIB)) (det (pair 10 (libsrc (snd i))) 0) RSTUCK)))
        (else RSTUCK)))
(def contractapp (f a)
  (let ((tf (fst f)))
    (cond ((eq tf 1) (det (subst (snd f) a 0) 0))
          ((eq tf 9) (det (mkapp (subst (snd f) f 0) a) 0))
          ((eq tf 12) (let ((n (snd f)))
                        (if (lt n 3) (pair 3 (pair n (pair a 0)))
                            (if (lt n NLIB) (det (subst (snd (libsrc n)) a 0) 0) RSTUCK))))
          (else RSTUCK))))

; ---------------- formulas, readings, the successor of an atom ----------------
(def mkatom (conf f a m) (pair 6 (pair conf (pair f (pair a m)))))
(def mkbox (i c u psi) (pair 7 (pair i (pair c (pair u psi)))))
(def reading (conf f a m)
  (let ((r (step conf)) (rk (fst r)))
    (cond ((eq rk 0) (if (eq (full conf) a) TOPF BOTF))
          ((eq rk 1) BOTF)
          ((eq f 0) BOTF)
          (else (mkatom conf f a m)))))
(def allfit (fr u) (if (eq fr 0) T (let ((x (fst fr))) (if (and (eq (fst x) 3) (lt (snd x) u)) F (allfit (snd fr) u)))))
(def argok (arg)
  (and (eq (fst arg) 5)
       (let ((p (snd arg)))
         (and (isnat (fst p))
              (let ((r (fst (snd p))))
                (and (eq (fst r) 5) (isnat (fst (snd (snd r))))))))))
(def srch (s f a mode)
  (let ((i (fst s)) (arg (fst (snd s))) (frames (snd (snd s))))
    (if (argok arg)
        (let ((p (snd arg)) (c (snd (fst p))) (r (snd (fst (snd p)))) (psi (full (fst r))) (bu (snd (fst (snd r)))) (u (add bu 7)))
          (if (or (eq mode 1) (and (le u f) (allfit frames u)))
              (pair 2 (pair (mkbox i c bu psi)
                            (pair (reading (plug frames TENC u) (sub f u) a 1) (reading (plug frames FENC u) (sub f u) a 1))))
              0))
        0)))
(def asucc (p mode)
  (let ((conf (fst p)) (q (snd p)) (f (fst q)) (a (fst (snd q))) (m (snd (snd q))))
    (if (eq f 0) 0
      (let ((r (step conf)) (rk (fst r)))
        (cond ((eq rk 2) (let ((d (snd r))) (pair 1 (if (and (eq m 1) (eq (snd d) 1)) BOTF (reading (fst d) (sub f 1) a m)))))
              ((eq rk 3) (srch (snd r) f a mode))
              (else 0))))))

; ---------------- tries (depth 16) and the formula table ----------------
(def tget (tr key d) (if (eq tr 0) 0 (if (eq d 0) tr (if (eq (mod key 2) 0) (tget (fst tr) (div key 2) (sub d 1)) (tget (snd tr) (div key 2) (sub d 1))))))
(def tput (tr key d val)
  (if (eq d 0) val
    (let ((n (if (eq tr 0) (pair 0 0) tr)))
      (if (eq (mod key 2) 0)
          (pair (tput (fst n) (div key 2) (sub d 1) val) (snd n))
          (pair (fst n) (tput (snd n) (div key 2) (sub d 1) val))))))
(def acode (a) (if (eq a C) 0 1))
(def fhash (phi)
  (let ((k (fst phi)) (p (snd phi)))
    (cond ((lt k 2) (add k 1))
          ((eq k 2) (mod (add 3 (mul 7 (fhash p))) HM))
          ((lt k 6) (mod (add k (add (mul 7 (fhash (fst p))) (mul 13 (fhash (snd p))))) HM))
          ((eq k 6) (let ((q (snd p))) (mod (add 6 (add (mul 5 (fst q)) (add (mul 2 (acode (fst (snd q)))) (mul 3 (snd (snd q)))))) HM)))
          (else (let ((q (snd p))) (mod (add 7 (add (fst p) (add (mul 3 (fst q)) (add (mul 5 (fst (snd q))) (mul 11 (fhash (snd (snd q)))))))) HM))))))
(def bfind (bk phi) (if (eq bk 0) NONE (if (eq (fst (fst bk)) phi) (snd (fst bk)) (bfind (snd bk) phi))))
(def intern (ft phi)
  (let ((h (fhash phi)) (seen (fst ft)) (bk (tget seen h 16)) (hit (bfind bk phi)))
    (if (eq hit NONE)
        (let ((id (snd (snd ft))))
          (pair id (pair (tput seen h 16 (pair (pair phi id) bk)) (pair (tput (fst (snd ft)) id 16 (pair phi 0)) (add id 1)))))
        (pair hit ft))))
(def setinfo (ft j phi info) (pair (fst ft) (pair (tput (fst (snd ft)) j 16 (pair phi info)) (snd (snd ft)))))
(def closure (ft j mode)
  (if (eq j (snd (snd ft))) ft
    (let ((phi (fst (tget (fst (snd ft)) j 16))) (r (mkinfo ft phi mode)))
      (closure (setinfo (snd r) j phi (fst r)) (add j 1) mode))))
(def mkinfo (ft phi mode)
  (let ((k (fst phi)) (p (snd phi)))
    (cond ((lt k 2) (pair (pair k 0) ft))
          ((eq k 2) (let ((r (intern ft p))) (pair (pair 2 (fst r)) (snd r))))
          ((lt k 6) (let ((r1 (intern ft (fst p))) (r2 (intern (snd r1) (snd p)))) (pair (pair k (pair (fst r1) (fst r2))) (snd r2))))
          ((eq k 6) (atominfo ft (asucc p mode)))
          (else (pair (pair 7 0) ft)))))
(def atominfo (ft s)
  (if (eq s 0) (pair (pair 6 0) ft)
    (if (eq (fst s) 1)
        (let ((r (intern ft (snd s)))) (pair (pair 6 (pair 1 (fst r))) (snd r)))
        (let ((q (snd s)) (r1 (intern ft (fst q))) (r2 (intern (snd r1) (fst (snd q)))) (r3 (intern (snd r2) (snd (snd q)))))
          (pair (pair 6 (pair 2 (pair (fst r1) (pair (fst r2) (fst r3))))) (snd r3))))))
(def chain (ids x)
  (let ((inf (snd (tget ids x 16))))
    (if (and (eq (fst inf) 6) (not (eq (snd inf) 0)))
        (let ((p (snd inf)))
          (if (eq (fst p) 1)
              (let ((s (snd p)))
                (if (eq (fst (snd (tget ids s 16))) 6) (pair x (chain ids s)) (pair x 0)))
              (pair x 0)))
        (pair x 0))))
(def setup (mode b psi u)
  (let ((r0 (intern (pair 0 (pair 0 0)) psi))
        (ft1 (closure (snd r0) 0 mode))
        (n1 (snd (snd ft1)))
        (rh (intern ft1 (mkbox mode b u psi)))
        (ft2 (closure (snd rh) n1 mode))
        (ids (fst (snd ft2))))
    (pair ids (pair (fst rh) (pair mode (pair b (pair u (chain ids 0))))))))

; ---------------- sorted id lists, sequent hashing, memo ----------------
(def ins (x l) (if (eq l 0) (pair x 0) (let ((y (fst l))) (if (lt x y) (pair x l) (if (eq x y) l (pair y (ins x (snd l))))))))
(def del (x l) (if (eq l 0) 0 (let ((y (fst l))) (if (eq x y) (snd l) (pair y (del x (snd l)))))))
(def mem (x l) (if (eq l 0) F (if (eq (fst l) x) T (mem x (snd l)))))
(def lhash (l h) (if (eq l 0) h (lhash (snd l) (mod (add (mul h 31) (add (fst l) 1)) HM))))
(def seqhash (L R) (lhash R (mod (add (mul (lhash L 7) 17) 3) HM)))
(def mfind (bk key) (if (eq bk 0) 0 (if (eq (fst (fst bk)) key) (snd (fst bk)) (mfind (snd bk) key))))
(def mremove (bk key) (if (eq bk 0) 0 (if (eq (fst (fst bk)) key) (snd bk) (pair (fst bk) (mremove (snd bk) key)))))
(def memoset (st h key v ex arg)
  (let ((m (fst st))) (pair (tput m h 16 (pair (pair key (pair v (pair ex arg))) (mremove (tget m h 16) key))) (snd st))))
(def memofail (st h key v)
  (let ((old (mfind (tget (fst st) h 16) key)))
    (if (or (eq old 0) (and (eq (fst (snd old)) 0) (lt (fst old) v))) (memoset st h key v 0 0) st)))
(def stwork (st) (let ((q (snd st)) (r (snd q))) (pair (fst st) (pair (fst q) (pair (add (fst r) 1) (snd r))))))
(def stinst (st) (let ((q (snd st)) (r (snd q))) (pair (fst st) (pair (fst q) (pair (fst r) (add (snd r) 1))))))
(def finfo (E x) (snd (tget (fst E) x 16)))
(def fform (E x) (fst (tget (fst E) x 16)))

; ---------------- the search: minimal size with memo ----------------
(def ms (E st L R cap)
  (if (lt cap 1) (pair 1 st)
    (let ((key (pair L R)) (h (seqhash L R)) (ent (mfind (tget (fst st) h 16) key)))
      (if (and (not (eq ent 0)) (or (eq (fst (snd ent)) 1) (lt cap (fst ent))))
          (pair (fst ent) st)
          (expand E (stwork st) L R cap key h)))))
(def expand (E st L R cap key h)
  (if (axiom E L R) (pair 1 (memoset st h key 1 1 (pair 0 0)))
    (let ((rr (runleaf E st L R)))
      (if (not (eq (fst rr) 0)) (pair 1 (memoset (snd rr) h key 1 1 (fst rr)))
        (let ((acc (tryR E (tryL E (pair INFV (pair 0 (snd rr))) L R L cap) L R R cap))
              (best (fst acc)) (arg (fst (snd acc))) (st2 (snd (snd acc))))
          (if (le best cap) (pair best (memoset st2 h key best 1 arg))
              (pair (add cap 1) (memofail st2 h key (add cap 1)))))))))
(def haskind (E l k) (if (eq l 0) F (if (eq (fst (finfo E (fst l))) k) T (haskind E (snd l) k))))
(def common (E L R)
  (if (eq L 0) F
    (let ((x (fst L)) (kk (fst (finfo E x))))
      (if (and (or (eq kk 6) (eq kk 7)) (mem x R)) T (common E (snd L) R)))))
(def axiom (E L R) (or (haskind E L 1) (or (haskind E R 0) (common E L R))))
(def runbox (E st x)
  (let ((rc (fst (snd st))) (hit (tget rc x 16)))
    (if (not (eq hit 0)) (pair hit st)
      (let ((phi (fform E x)) (p (snd phi)) (q (snd p))
            (v (if (eq (callcore (fst p) (fst q) (fst (snd q)) (snd (snd q))) T) T F)))
        (pair v (pair (fst st) (pair (tput rc x 16 v) (snd (snd st)))))))))
(def callcore (i c u psi)
  (let ((arg (pair c (pair psi u))))
    (cond ((eq i 0) (capk u CORE0 arg)) ((eq i 1) (capk u CORE1 arg)) ((eq i 2) (capk u CORE2 arg)) (else F))))
(def runleaf (E st L R) (let ((r (runR E st R))) (if (eq (fst r) 0) (runL E (snd r) L) r)))
(def runR (E st l)
  (if (eq l 0) (pair 0 st)
    (let ((x (fst l)))
      (if (eq (fst (finfo E x)) 7)
          (if (eq (fst (snd (snd E))) 1) (pair (pair 1 x) st)
            (if (eq x (fst (snd E))) (runR E st (snd l))
              (let ((b (runbox E st x))) (if (eq (fst b) T) (pair (pair 1 x) (snd b)) (runR E (snd b) (snd l))))))
          (runR E st (snd l))))))
(def runL (E st l)
  (if (eq l 0) (pair 0 st)
    (let ((x (fst l)))
      (if (eq (fst (finfo E x)) 7)
          (if (eq (fst (snd (snd E))) 1) (pair (pair 2 x) st)
            (if (eq x (fst (snd E))) (runL E st (snd l))
              (let ((b (runbox E st x))) (if (eq (fst b) F) (pair (pair 2 x) (snd b)) (runL E (snd b) (snd l))))))
          (runL E st (snd l))))))
(def one (E acc PL PR cap tag x)
  (let ((best (fst acc)) (lim (sub (min cap (sub best 1)) 1)) (r (ms E (stinst (snd (snd acc))) PL PR lim)))
    (if (le (fst r) lim)
        (pair (add (fst r) 1) (pair (pair 3 (pair tag (pair x (pair (pair PL PR) 0)))) (snd r)))
        (pair best (pair (fst (snd acc)) (snd r))))))
(def two (E acc AL AR BL BR cap tag x)
  (let ((best (fst acc)) (lim (min cap (sub best 1))) (r1 (ms E (stinst (snd (snd acc))) AL AR (sub lim 2))))
    (if (lt (sub lim 2) (fst r1)) (pair best (pair (fst (snd acc)) (snd r1)))
      (let ((s1 (fst r1)) (lim2 (sub (sub lim 1) s1)) (r2 (ms E (snd r1) BL BR lim2)))
        (if (lt lim2 (fst r2)) (pair best (pair (fst (snd acc)) (snd r2)))
          (pair (add 1 (add s1 (fst r2)))
                (pair (pair 3 (pair tag (pair x (pair (pair AL AR) (pair (pair BL BR) 0))))) (snd r2))))))))
(def tryL (E acc L R l cap) (if (eq l 0) acc (tryL E (tryL1 E acc L R (fst l) cap) L R (snd l) cap)))
(def tryL1 (E acc L R x cap)
  (let ((inf (finfo E x)) (k (fst inf)) (p (snd inf)) (Lx (del x L)))
    (cond ((eq k 2) (one E acc Lx (ins p R) cap 10 x))
          ((eq k 3) (one E acc (ins (snd p) (ins (fst p) Lx)) R cap 11 x))
          ((eq k 4) (two E acc (ins (fst p) Lx) R (ins (snd p) Lx) R cap 12 x))
          ((eq k 5) (two E acc Lx (ins (fst p) R) (ins (snd p) Lx) R cap 13 x))
          ((eq k 6) (if (eq p 0) acc (if (eq (fst p) 1) (one E acc (ins (snd p) Lx) R cap 14 x) acc)))
          (else acc))))
(def tryR (E acc L R l cap) (if (eq l 0) acc (tryR E (tryR1 E acc L R (fst l) cap) L R (snd l) cap)))
(def tryR1 (E acc L R x cap)
  (let ((inf (finfo E x)) (k (fst inf)) (p (snd inf)) (Rx (del x R))
        (acc2 (cond ((eq k 2) (one E acc (ins p L) Rx cap 20 x))
                    ((eq k 4) (one E acc L (ins (snd p) (ins (fst p) Rx)) cap 21 x))
                    ((eq k 5) (one E acc (ins (fst p) L) (ins (snd p) Rx) cap 22 x))
                    ((eq k 3) (two E acc L (ins (fst p) Rx) L (ins (snd p) Rx) cap 23 x))
                    ((eq k 6) (if (eq p 0) acc
                                (if (eq (fst p) 1) (one E acc L (ins (snd p) Rx) cap 24 x)
                                  (let ((q (snd p)) (bx (fst q)))
                                    (two E acc (ins bx L) (ins (fst (snd q)) Rx) L (ins (snd (snd q)) (ins bx Rx)) cap 25 x)))))
                    (else acc))))
    (if (lt k 2) acc2 (jlob E acc2 x k cap))))
(def eligible (E x k)
  (let ((mode (fst (snd (snd E)))))
    (cond ((eq mode 0) (mem x (snd (snd (snd (snd (snd E)))))))
          ((eq mode 1) T)
          (else F))))
(def jlob (E acc x k cap)
  (if (eligible E x k)
      (let ((best (fst acc)) (lim (min cap (sub best 1))) (r (ms E (stinst (snd (snd acc))) (pair (fst (snd E)) 0) (pair 0 0) (sub lim 1))))
        (if (le (fst r) (sub lim 1))
            (pair (add (fst r) 1) (pair (pair 4 x) (snd r)))
            (pair best (pair (fst (snd acc)) (snd r)))))
      acc))
(def deepen (E st n b)
  (if (lt b n) (pair F st)
    (let ((r (ms E st 0 (pair 0 0) n)))
      (if (le (fst r) n) (pair T (snd r)) (deepen E (snd r) (add n 1) b)))))
(def core (mode arg)
  (let ((b (fst arg)) (E (setup mode b (fst (snd arg)) (snd (snd arg)))))
    (fst (deepen E (pair 0 (pair 0 (pair 0 0))) 1 b))))

; ---------------- witness (audit entry) ----------------
(def corew (mode arg)
  (let ((b (fst arg)) (E (setup mode b (fst (snd arg)) (snd (snd arg)))) (r (deepen E (pair 0 (pair 0 (pair 0 0))) 1 b)))
    (if (eq (fst r) T)
        (pair T (pair (wit E (fst (snd r)) 0 (pair 0 0)) (snd (snd (snd r)))))
        (pair F (pair 0 (snd (snd (snd r))))))))
(def forms (E l) (if (eq l 0) 0 (pair (fform E (fst l)) (forms E (snd l)))))
(def wit (E memo L R)
  (let ((ent (mfind (tget memo (seqhash L R) 16) (pair L R))) (size (fst ent)) (arg (snd (snd ent))) (tag (fst arg)))
    (cond ((eq tag 0) (pair 0 (pair (forms E L) (pair (forms E R) (pair 0 (pair size 0))))))
          ((lt tag 3) (pair tag (pair (forms E L) (pair (forms E R) (pair (fform E (snd arg)) (pair size 0))))))
          ((eq tag 4) (pair 4 (pair (forms E L) (pair (forms E R) (pair (fform E (snd arg))
                         (pair size (pair (wit E memo (pair (fst (snd E)) 0) (pair 0 0)) 0)))))))
          (else (let ((q (snd arg)))
                  (pair (fst q) (pair (forms E L) (pair (forms E R) (pair (fform E (fst (snd q)))
                         (pair size (wits E memo (snd (snd q)))))))))))))
(def wits (E memo ps) (if (eq ps 0) 0 (pair (wit E memo (fst (fst ps)) (snd (fst ps))) (wits E memo (snd ps)))))

; ---------------- the checker (a supplied derivation, formulas as data) ----------------
(def fmem (x l) (if (eq l 0) F (if (eq (fst l) x) T (fmem x (snd l)))))
(def fsub (a b) (if (eq a 0) T (if (fmem (fst a) b) (fsub (snd a) b) F)))
(def fseteq (a b) (and (fsub a b) (fsub b a)))
(def fdel (x l) (if (eq l 0) 0 (if (eq (fst l) x) (snd l) (pair (fst l) (fdel x (snd l))))))
(def fadd (x l) (if (fmem x l) l (pair x l)))
(def fhaskind (l k) (if (eq l 0) F (if (eq (fst (fst l)) k) T (fhaskind (snd l) k))))
(def fcommon (L R) (if (eq L 0) F (let ((x (fst L))) (if (and (or (eq (fst x) 6) (eq (fst x) 7)) (fmem x R)) T (fcommon (snd L) R)))))
(def fchain (phi)
  (if (eq (fst phi) 6)
      (let ((s (asucc (snd phi) 0)))
        (if (and (not (eq s 0)) (and (eq (fst s) 1) (eq (fst (snd s)) 6))) (pair phi (fchain (snd s))) (pair phi 0)))
      (pair phi 0)))
(def seqok (n L R) (and (fseteq (fst (snd n)) L) (fseteq (fst (snd (snd n))) R)))
(def chkprems (cx ps acc) (if (eq ps 0) acc (let ((s (chk cx (fst ps)))) (if (eq s 0) 0 (chkprems cx (snd ps) (add acc s))))))
(def check (mode arg D)
  (let ((b (fst arg)) (psi0 (fst (snd arg))) (u (snd (snd arg))) (H (mkbox mode b u psi0))
        (cx (pair mode (pair H (pair (if (eq mode 0) (fchain psi0) 0) (pair psi0 (pair b u))))))
        (s (chk cx D)))
    (and (not (eq s 0)) (and (le s b) (and (eq (fst (snd D)) 0) (fseteq (fst (snd (snd D))) (pair psi0 0)))))))
(def chk (cx n)
  (let ((rule (fst n)) (L (fst (snd n))) (R (fst (snd (snd n)))) (x (fst (snd (snd (snd n)))))
        (ps (snd (snd (snd (snd (snd n)))))) (mode (fst cx)) (H (fst (snd cx)))
        (ok (chkrule cx rule L R x ps mode H)))
    (if ok (if (lt rule 3) 1 (let ((s (chkprems cx ps 0))) (if (eq s 0) 0 (add s 1)))) 0)))
(def runform (x)
  (let ((p (snd x)) (q (snd p))) (eq (callcore (fst p) (fst q) (fst (snd q)) (snd (snd q))) T)))
(def chkrule (cx rule L R x ps mode H)
  (cond ((eq rule 0) (or (fhaskind L 1) (or (fhaskind R 0) (fcommon L R))))
        ((eq rule 1) (and (fmem x R) (and (eq (fst x) 7) (or (eq mode 1) (and (not (eq x H)) (runform x))))))
        ((eq rule 2) (and (fmem x L) (and (eq (fst x) 7) (or (eq mode 1) (and (not (eq x H)) (not (runform x)))))))
        ((eq rule 4) (and (fmem x R)
                          (and (cond ((eq mode 0) (fmem x (fst (snd (snd cx))))) ((eq mode 1) (lt 1 (fst x))) (else F))
                               (seqok (fst ps) (pair H 0) (pair (fst (snd (snd (snd cx)))) 0)))))
        ((lt rule 20) (and (fmem x L) (chkleft rule (fdel x L) R x ps mode)))
        (else (and (fmem x R) (chkright rule L (fdel x R) x ps mode)))))
(def chkleft (rule Lx R x ps mode)
  (let ((k (fst x)) (p (snd x)))
    (cond ((eq rule 10) (and (eq k 2) (seqok (fst ps) Lx (fadd p R))))
          ((eq rule 11) (and (eq k 3) (seqok (fst ps) (fadd (snd p) (fadd (fst p) Lx)) R)))
          ((eq rule 12) (and (eq k 4) (and (seqok (fst ps) (fadd (fst p) Lx) R) (seqok (fst (snd ps)) (fadd (snd p) Lx) R))))
          ((eq rule 13) (and (eq k 5) (and (seqok (fst ps) Lx (fadd (fst p) R)) (seqok (fst (snd ps)) (fadd (snd p) Lx) R))))
          ((eq rule 14) (and (eq k 6) (let ((s (asucc p mode))) (and (not (eq s 0)) (and (eq (fst s) 1) (seqok (fst ps) (fadd (snd s) Lx) R))))))
          (else F))))
(def chkright (rule L Rx x ps mode)
  (let ((k (fst x)) (p (snd x)))
    (cond ((eq rule 20) (and (eq k 2) (seqok (fst ps) (fadd p L) Rx)))
          ((eq rule 21) (and (eq k 4) (seqok (fst ps) L (fadd (snd p) (fadd (fst p) Rx)))))
          ((eq rule 22) (and (eq k 5) (seqok (fst ps) (fadd (fst p) L) (fadd (snd p) Rx))))
          ((eq rule 23) (and (eq k 3) (and (seqok (fst ps) L (fadd (fst p) Rx)) (seqok (fst (snd ps)) L (fadd (snd p) Rx)))))
          ((eq rule 24) (and (eq k 6) (let ((s (asucc p mode))) (and (not (eq s 0)) (and (eq (fst s) 1) (seqok (fst ps) L (fadd (snd s) Rx)))))))
          ((eq rule 25) (and (eq k 6) (let ((s (asucc p mode)))
                          (and (not (eq s 0)) (and (eq (fst s) 2)
                            (let ((q (snd s)) (bx (fst q)))
                              (and (seqok (fst ps) (fadd bx L) (fadd (fst (snd q)) Rx))
                                   (seqok (fst (snd ps)) L (fadd (snd (snd q)) (fadd bx Rx))))))))))
          (else F))))
"""

LIB_CONSTS = {
    'NONE': 1000000, 'INFV': 1000000, 'HM': 65536,
    'RVAL': ['pair', 0, 0], 'RSTUCK': ['pair', 1, 0],
    'TENC': ['pair', 3, 2], 'FENC': ['pair', 3, 3], 'TOENC': ['pair', 3, 4],
    'TOPF': ['pair', 0, 0], 'BOTF': ['pair', 1, 0],
}

# lib indices
LIBIDX = {}
RULE_NAMES = {0: 'Ax', 1: 'Run', 2: 'RunNeg', 4: 'JLob', 10: 'notL', 11: 'andL', 12: 'orL', 13: 'impL', 14: 'EvL',
              20: 'notR', 21: 'orR', 22: 'impR', 23: 'andR', 24: 'EvR', 25: 'SrchR'}


def compile_library():
    comp = SxCompiler()
    for k, v in LIB_CONSTS.items(): comp.consts[k] = v
    comp.load(LIBRARY_SRC)
    comp.consts['NLIB'] = len(comp.order)
    terms = comp.build(0)
    LIB[:] = terms
    LIBNAME.clear(); LIBNAME.update({i: n for i, n in enumerate(comp.order)})
    LIBIDX.clear(); LIBIDX.update(comp.index)
    SEARCH_LIBS.clear(); SEARCH_LIBS.update({LIBIDX['SEARCH%d' % i]: i for i in range(3)})
    CORE_LIBS.clear(); CORE_LIBS.update({LIBIDX['CORE%d' % i]: i for i in range(3)})
    assert [LIBIDX['SEARCH%d' % i] for i in range(3)] == [0, 1, 2]
    LIBCODE[:] = [compile_term(t[1]) for t in terms]
    return comp


_COMP = compile_library()


def lib(name): return ('lib', LIBIDX[name])


def call(name, *args):
    t = lib(name)
    for a in args: t = ('app', t, a)
    return t


# ----------------------------------------------------------------------------------------------------------------
# 5. The catalogue (predictions file, design 6)
# ----------------------------------------------------------------------------------------------------------------
ME, THEM = ('v', 1), ('v', 0)
N = lambda n: ('nat', n)
P = lambda a, b: ('pair', a, b)


def L2(body): return ('lam', ('lam', body))


def CONF(x, y):
    """Encoding (built by the program) of the configuration app(app(x, quote x), quote y), x, y quote values."""
    return P(N(2), P(P(N(2), P(x, P(P(N(10), x), N(0)))), P(P(N(10), y), N(0))))


def PLAYS(x, y, a, K): return P(N(6), P(CONF(x, y), P(N(K), P(a, N(0)))))
def BOX(i, c, U, psi): return P(N(7), P(N(i), P(N(c), P(N(U), psi))))
BOTF_T = P(N(1), N(0))
def NOT(a): return P(N(2), a)
def IMP(a, b): return P(N(5), P(a, b))
def CON(i, b, U): return NOT(BOX(i, b, U, BOTF_T))
def SRCH(i, b, psi, U): return ('app', ('lib', i), P(N(b), P(psi, N(U))))


PROG_C = L2(C_)
PROG_D = L2(D_)


def FB(b, U, K, i=0): return L2(('if', SRCH(i, b, PLAYS(THEM, ME, C_, K), U), C_, D_))
def FB1(b, U, K, i=0): return L2(('if', SRCH(i, b, IMP(CON(i, b, U), PLAYS(THEM, ME, C_, K)), U), C_, D_))
def PB(b, U, K, i=0):
    q2 = IMP(CON(i, b, U), PLAYS(THEM, ('quote', PROG_D), D_, K))
    return L2(('if', SRCH(i, b, PLAYS(THEM, ME, C_, K), U), ('if', SRCH(i, b, q2, U), C_, D_), D_))
def G(b, U, K, i=0): return L2(('if', SRCH(i, b, PLAYS(THEM, ME, C_, K), U), D_, C_))
def PSTAR(b, U, K, i=0):
    return L2(('if', SRCH(i, b, IMP(CON(i, b, U), PLAYS(THEM, ME, C_, K)), U),
               ('if', SRCH(i, b, PLAYS(THEM, ME, C_, K), U), D_, C_), D_))
def SF(k): return L2(('if', ('eq', ('run', N(k), THEM, ME), C_), C_, D_))
def SC(b, U, K): return FB(b, U, K, i=1)
def VLET(b, U, K, i=0):
    return L2(('app', ('lam', ('if', SRCH(i, b, ('v', 0), U), C_, D_)), PLAYS(THEM, ME, C_, K)))
def VWRAP(b, U, K, i=0): return L2(('app', ('lam', ('v', 0)), ('app', ('app', FB(b, U, K, i), ME), THEM)))
def FB2(b, U, K, i=0):
    q = PLAYS(THEM, ME, C_, K)
    return L2(('if', SRCH(i, b, q, U), ('if', SRCH(i, b, q, U), C_, D_), D_))
def FBX(b, U, K, i=0, factor=10): return FB(b, U, factor * K, i)


SOUND_READERS = ['FB', 'FB1', 'PB', 'Vlet', 'Vwrap', 'FB2', 'FBx']


def catalogue(K, b, k=None, i=0, U=None):
    """The named catalogue at cell (K, b): U = K // 4, SF with k = K // 2 by default; i = 2 gives the control."""
    U = K // 4 if U is None else U
    k = K // 2 if k is None else k
    return {'C': PROG_C, 'D': PROG_D, 'FB': FB(b, U, K, i), 'FB1': FB1(b, U, K, i), 'PB': PB(b, U, K, i),
            'G': G(b, U, K, i), 'P*': PSTAR(b, U, K, i), 'SF': SF(k), 'SC': SC(b, U, K), 'Vlet': VLET(b, U, K, i),
            'Vwrap': VWRAP(b, U, K, i), 'FB2': FB2(b, U, K, i), 'FBx': FBX(b, U, K, i)}


def initial(p, q):
    return ('app', ('app', p, ('quote', p)), ('quote', q))


def play(p, q, K, events=None):
    """The actual play of p against q with global fuel K: ('C' | 'D' | 'BOT', steps)."""
    v, n = evaluate(initial(p, q), K, events)
    return (v if v in ('C', 'D') else 'BOT'), n


# ----------------------------------------------------------------------------------------------------------------
# 6. Formula conversions and box truth
# ----------------------------------------------------------------------------------------------------------------
TOPH, BOTH = ('top',), ('bot',)
KINDS = {0: 'top', 1: 'bot', 2: 'not', 3: 'and', 4: 'or', 5: 'imp', 6: 'atom', 7: 'box'}


def rt_to_formula(v):
    """Formula data (runtime value) -> host formula."""
    k, p = v
    if k == 0: return TOPH
    if k == 1: return BOTH
    if k == 2: return ('not', rt_to_formula(p))
    if k in (3, 4, 5): return (KINDS[k], rt_to_formula(p[0]), rt_to_formula(p[1]))
    if k == 6:
        conf, (f, (a, m)) = p
        return ('atom', term_of_enc(canon_rt(conf)), f, a, m)
    if k == 7:
        i, (c, (U, psi)) = p
        return ('box', i, c, U, rt_to_formula(psi))
    raise ValueError('not a formula: %r' % (k,))


def formula_to_rt(phi):
    k = phi[0]
    if k == 'top': return (0, 0)
    if k == 'bot': return (1, 0)
    if k == 'not': return (2, formula_to_rt(phi[1]))
    if k in ('and', 'or', 'imp'): return ({'and': 3, 'or': 4, 'imp': 5}[k], (formula_to_rt(phi[1]), formula_to_rt(phi[2])))
    if k == 'atom': return (6, (Q(phi[1]), (phi[2], (phi[3], phi[4]))))
    return (7, (phi[1], (phi[2], (phi[3], formula_to_rt(phi[4])))))


def show_formula(phi, names=None):
    names = names or {}
    k = phi[0]
    if k == 'top': return 'T'
    if k == 'bot': return 'F'
    if k == 'not': return '~' + show_formula(phi[1], names)
    if k in ('and', 'or', 'imp'):
        return '(%s %s %s)' % (show_formula(phi[1], names), {'and': '&', 'or': '|', 'imp': '->'}[k],
                               show_formula(phi[2], names))
    if k == 'atom':
        c = phi[1]
        if c[0] == 'app' and c[1][0] == 'app' and c[1][2][0] == 'quote' and c[2][0] == 'quote':
            s = 'plays(%s,%s)' % (names.get(c[1][1], '?'), names.get(c[2][1], '?'))
        else:
            s = '<%s..>' % c[0]
        return '%s@%d=>%s%s' % (s, phi[2], phi[3], '+' if phi[4] else '')
    return '[%d|%d,U%d]%s' % (phi[1], phi[2], phi[3], show_formula(phi[4], names))


def core_arg(c, psi_rt, U):
    return (c, (psi_rt, U))


def box_truth(i, c, U, psi_rt):
    """Truth of the box [i, c, U] psi: the clean run of capk(U, CORE_i, (c, (psi, U))) returns T.  Returns
    (result value 'T'/'F'/'TO', steps after the capk contraction)."""
    if i not in (0, 1, 2) or not isinstance(U, int) or not isinstance(c, int): return ('F', 0)
    n = LIBIDX['CORE%d' % i]
    arg = core_arg(c, psi_rt, U)
    key = (n, U, arg)
    rec = CACHE.get(key)
    if rec is None:
        v, steps = evaluate(('capk', N(U), ('lib', n), rt_to_tval(arg)))
        rec = CACHE.get(key)
        if rec is None: rec = (v, steps - 1)
    return rec


def witness_arg(c, psi_rt, U): return core_arg(c, psi_rt, U)


def core_witness(i, c, psi_rt, U):
    """Run COREW_i in a clean frame of fuel U (the audit entry): (result, witness data or None, (work, inst), steps)."""
    arg = core_arg(c, psi_rt, U)
    v, steps = evaluate(('capk', N(U), lib('COREW%d' % i), rt_to_tval(arg)))
    if v == 'TO': return 'TO', None, None, steps
    return v[0], (v[1][0] if v[0] == 'T' else None), v[1][1], steps


# ----------------------------------------------------------------------------------------------------------------
# 7. The host oracle: the frozen search algorithm in Python over the reference stepper
# ----------------------------------------------------------------------------------------------------------------
def parse_arg(v):
    """Term-level value of a search call's argument -> (c, psi host formula, U) or None (L_T's argok)."""
    if v[0] != 'pair' or v[1][0] != 'nat': return None
    r = v[2]
    if r[0] != 'pair' or r[2][0] != 'nat': return None
    return v[1][1], rt_to_formula(tval_to_rt(r[1])), r[2][1]


def h_reading(t, f, a, m):
    r = step(t)
    if r[0] == 'value': return TOPH if t == ('con', a) else BOTH
    if r[0] == 'stuck': return BOTH
    if f == 0: return BOTH
    return ('atom', t, f, a, m)


def h_asucc(phi, mode):
    """None (no rule) | ('det', successor) | ('srch', box, rhoT, rhoF)."""
    _, conf, f, a, m = phi
    if f == 0: return None
    r = step(conf)
    if r[0] == 'det':
        if m == 1 and r[2] == 1: return ('det', BOTH)
        return ('det', h_reading(r[1], f - 1, a, m))
    if r[0] == 'search':
        i, v, ctx = r[1], r[2], r[3]
        pa = parse_arg(v)
        if pa is None: return None
        c, psi, U = pa
        u = U + 7
        fuels = [fr[1] for fr in ctx if fr[0] == 'sim']
        if mode == 1 or (u <= f and all(k >= u for k in fuels)):
            fr = max(0, f - u)
            return ('srch', ('box', i, c, U, psi), h_reading(plug(ctx, T_, u), fr, a, 1),
                    h_reading(plug(ctx, F_, u), fr, a, 1))
    return None


class HostSearch:
    """The frozen core algorithm (predictions design 4) in Python: same closure order, same instance order, same
    memo rule; Run/RunNeg side conditions from box_truth (the semantics)."""
    INFV = 1000000

    def __init__(self, mode, b, psi, U):
        self.mode, self.b, self.U = mode, b, U
        self.F = []; self.fid = {}; self.info = []
        self.root = self.intern(psi)
        j = 0
        while j < len(self.F):
            self.info[j] = self.mkinfo(self.F[j]); j += 1
        self.H = self.intern(('box', mode, b, U, psi))
        while j < len(self.F):
            self.info[j] = self.mkinfo(self.F[j]); j += 1
        ch = [self.root]; x = self.root
        while True:
            inf = self.info[x]
            if inf[0] == 'atom' and inf[1] is not None and inf[1][0] == 'det' and self.F[inf[1][1]][0] == 'atom':
                x = inf[1][1]; ch.append(x)
            else: break
        self.chain = set(ch)
        self.memo = {}; self.rc = {}; self.work = 0; self.inst = 0

    def intern(self, phi):
        i = self.fid.get(phi)
        if i is None:
            i = len(self.F); self.fid[phi] = i; self.F.append(phi); self.info.append(None)
        return i

    def mkinfo(self, phi):
        k = phi[0]
        if k in ('top', 'bot', 'box'): return (k, None)
        if k == 'not': return (k, self.intern(phi[1]))
        if k in ('and', 'or', 'imp'):
            a = self.intern(phi[1]); b = self.intern(phi[2]); return (k, (a, b))
        s = h_asucc(phi, self.mode)
        if s is None: return ('atom', None)
        if s[0] == 'det': return ('atom', ('det', self.intern(s[1])))
        bx = self.intern(s[1]); rt = self.intern(s[2]); rf = self.intern(s[3])
        return ('atom', ('srch', bx, rt, rf))

    @staticmethod
    def ins(x, l): return tuple(sorted(set(l) | {x}))

    @staticmethod
    def dele(x, l): return tuple(y for y in l if y != x)

    def kind(self, x): return self.info[x][0]

    def axiom(self, L, R):
        if any(self.kind(x) == 'bot' for x in L): return True
        if any(self.kind(x) == 'top' for x in R): return True
        return any(self.kind(x) in ('atom', 'box') and x in R for x in L)

    def runbox(self, x):
        v = self.rc.get(x)
        if v is None:
            _, i, c, U, psi = self.F[x]
            v = box_truth(i, c, U, formula_to_rt(psi))[0] == 'T'
            self.rc[x] = v
        return v

    def runleaf(self, L, R):
        for y in R:
            if self.kind(y) == 'box':
                if self.mode == 1: return ('run', y)
                if y != self.H and self.runbox(y): return ('run', y)
        for x in L:
            if self.kind(x) == 'box':
                if self.mode == 1: return ('runneg', x)
                if x != self.H and not self.runbox(x): return ('runneg', x)
        return None

    def ms(self, L, R, cap):
        if cap < 1: return 1
        key = (L, R)
        e = self.memo.get(key)
        if e is not None and (e[1] or cap < e[0]): return e[0]
        self.work += 1
        if self.axiom(L, R):
            self.memo[key] = (1, True, ('ax',)); return 1
        rr = self.runleaf(L, R)
        if rr is not None:
            self.memo[key] = (1, True, rr); return 1
        acc = [self.INFV, None]
        for x in L: self.tryL1(acc, L, R, x, cap)
        for x in R:
            self.tryR1(acc, L, R, x, cap)
            if self.kind(x) not in ('top', 'bot') and self.eligible(x): self.jlob(acc, x, cap)
        best, arg = acc
        if best <= cap:
            self.memo[key] = (best, True, arg); return best
        v = cap + 1
        old = self.memo.get(key)
        if old is None or (not old[1] and old[0] < v): self.memo[key] = (v, False, None)
        return v

    def eligible(self, x):
        if self.mode == 0: return x in self.chain
        return self.mode == 1

    def one(self, acc, PL, PR, cap, tag, x):
        lim = max(0, min(cap, acc[0] - 1) - 1)
        self.inst += 1
        s = self.ms(PL, PR, lim)
        if s <= lim: acc[0], acc[1] = s + 1, (tag, x, [(PL, PR)])

    def two(self, acc, AL, AR, BL, BR, cap, tag, x):
        lim = min(cap, acc[0] - 1)
        self.inst += 1
        l1 = max(0, lim - 2)
        s1 = self.ms(AL, AR, l1)
        if l1 < s1: return
        lim2 = max(0, max(0, lim - 1) - s1)
        s2 = self.ms(BL, BR, lim2)
        if lim2 < s2: return
        acc[0], acc[1] = 1 + s1 + s2, (tag, x, [(AL, AR), (BL, BR)])

    def jlob(self, acc, x, cap):
        lim = min(cap, acc[0] - 1)
        self.inst += 1
        l1 = max(0, lim - 1)
        s = self.ms((self.H,), (self.root,), l1)
        if s <= l1: acc[0], acc[1] = s + 1, ('jlob', x, [((self.H,), (self.root,))])

    def tryL1(self, acc, L, R, x, cap):
        k, p = self.info[x]
        Lx = self.dele(x, L)
        if k == 'not': self.one(acc, Lx, self.ins(p, R), cap, 10, x)
        elif k == 'and': self.one(acc, self.ins(p[1], self.ins(p[0], Lx)), R, cap, 11, x)
        elif k == 'or': self.two(acc, self.ins(p[0], Lx), R, self.ins(p[1], Lx), R, cap, 12, x)
        elif k == 'imp': self.two(acc, Lx, self.ins(p[0], R), self.ins(p[1], Lx), R, cap, 13, x)
        elif k == 'atom' and p is not None and p[0] == 'det': self.one(acc, self.ins(p[1], Lx), R, cap, 14, x)

    def tryR1(self, acc, L, R, x, cap):
        k, p = self.info[x]
        Rx = self.dele(x, R)
        if k == 'not': self.one(acc, self.ins(p, L), Rx, cap, 20, x)
        elif k == 'or': self.one(acc, L, self.ins(p[1], self.ins(p[0], Rx)), cap, 21, x)
        elif k == 'imp': self.one(acc, self.ins(p[0], L), self.ins(p[1], Rx), cap, 22, x)
        elif k == 'and': self.two(acc, L, self.ins(p[0], Rx), L, self.ins(p[1], Rx), cap, 23, x)
        elif k == 'atom' and p is not None:
            if p[0] == 'det': self.one(acc, L, self.ins(p[1], Rx), cap, 24, x)
            else:
                bx, rt, rf = p[1], p[2], p[3]
                self.two(acc, self.ins(bx, L), self.ins(rt, Rx), L, self.ins(rf, self.ins(bx, Rx)), cap, 25, x)

    def search(self):
        for n in range(1, self.b + 1):
            s = self.ms((), (self.root,), n)
            if s <= n: return True, s
        return False, None

    def witness(self, L=(), R=None):
        R = (self.root,) if R is None else R
        v, ex, arg = self.memo[(L, R)]
        assert ex
        node = {'rule': arg[0] if arg[0] in ('ax', 'run', 'runneg', 'jlob') else RULE_NAMES[arg[0]], 'size': v,
                'L': [self.F[x] for x in L], 'R': [self.F[x] for x in R]}
        if arg[0] == 'ax': node['x'] = None; node['prem'] = []; return node
        node['x'] = self.F[arg[1]]
        if arg[0] in ('run', 'runneg'): node['prem'] = []; return node
        node['prem'] = [self.witness(*pk) for pk in arg[2]]
        return node


def host_query(mode, c, psi_rt, U):
    """The host oracle on a query (mode, c, psi, U): dict(found, size, work, inst, search)."""
    s = HostSearch(mode, c, rt_to_formula(psi_rt), U)
    found, size = s.search()
    return {'found': found, 'size': size, 'work': s.work, 'inst': s.inst, 'closure': len(s.F), 'search': s}


# ----------------------------------------------------------------------------------------------------------------
# 8. The independent replay checker (written from the rule table of notes §1.5, not from the search code)
# ----------------------------------------------------------------------------------------------------------------
class ReplayError(Exception):
    pass


def _succ_indep(phi, mode):
    """Independent successor computation: its own decomposition of the configuration via the reference `step`."""
    _, conf, f, a, m = phi
    if f <= 0: return None
    r = step(conf)

    def read(t, g, mm):
        rr = step(t)
        if rr[0] == 'value': return TOPH if t == ('con', a) else BOTH
        if rr[0] == 'stuck' or g == 0: return BOTH
        return ('atom', t, g, a, mm)
    if r[0] == 'det':
        return ('det', BOTH if (m == 1 and r[2]) else read(r[1], f - 1, m))
    if r[0] != 'search': return None
    v = r[2]
    try:
        c, psi, U = v[1][1], rt_to_formula(tval_to_rt(v[2][1])), v[2][2][1]
        assert v[0] == 'pair' and v[1][0] == 'nat' and v[2][0] == 'pair' and v[2][2][0] == 'nat'
    except Exception:
        return None
    u = U + 7
    sims = [fr[1] for fr in r[3] if fr[0] == 'sim']
    if mode != 1 and not (f >= u and min(sims + [u]) >= u): return None
    g = f - u if f > u else 0
    return ('srch', ('box', r[1], c, U, psi), read(plug(r[3], T_, u), g, 1), read(plug(r[3], F_, u), g, 1))


def replay(node, mode, b, U, root, root_found, stats=None):
    """Check a witness tree (host formulas) relative to the root call (mode, b, root, U).  root_found: the recorded
    outcome of the run that produced it (JLob^self's hypothesis).  Returns the size; raises ReplayError."""
    H = ('box', mode, b, U, root)
    chain = [root]
    while chain[-1][0] == 'atom':
        s = _succ_indep(chain[-1], 0)
        if s is None or s[0] != 'det' or s[1][0] != 'atom': break
        chain.append(s[1])

    def same(A, B): return set(A) == set(B)

    def rec(nd):
        if stats is not None: stats['nodes'] = stats.get('nodes', 0) + 1
        L, R, x, rule, ps = nd['L'], nd['R'], nd.get('x'), nd['rule'], nd['prem']
        if rule == 'ax':
            if not (BOTH in L or TOPH in R or any(y in R and y[0] in ('atom', 'box') for y in L)):
                raise ReplayError('ax')
            return 1
        if rule in ('run', 'runneg'):
            side = R if rule == 'run' else L
            if x not in side or x[0] != 'box': raise ReplayError(rule + ' shape')
            if mode != 1:
                if x == H: raise ReplayError(rule + ' on the root call')
                t = box_truth(x[1], x[2], x[3], formula_to_rt(x[4]))[0] == 'T'
                if t != (rule == 'run'): raise ReplayError(rule + ' side condition false')
            return 1
        if rule == 'jlob':
            if x not in R: raise ReplayError('jlob shape')
            if mode == 0 and x not in chain: raise ReplayError('jlob member not the root or downstream')
            if mode == 2: raise ReplayError('jlob in the control')
            if mode == 1 and x[0] in ('top', 'bot'): raise ReplayError('jlob on top/bot')
            if len(ps) != 1 or not (same(ps[0]['L'], [H]) and same(ps[0]['R'], [root])):
                raise ReplayError('jlob premise is not  H |- root')
            if mode != 1 and not root_found: raise ReplayError('jlob hypothesis false (root call did not succeed)')
            return 1 + rec(ps[0])
        left = rule in ('notL', 'andL', 'orL', 'impL', 'EvL')
        side = L if left else R
        if x not in side: raise ReplayError(rule + ' principal formula absent')
        Lx = [y for y in L if y != x]; Rx = [y for y in R if y != x]
        exp = None
        if rule == 'notL' and x[0] == 'not': exp = [(Lx, R + [x[1]])]
        elif rule == 'andL' and x[0] == 'and': exp = [(Lx + [x[1], x[2]], R)]
        elif rule == 'orL' and x[0] == 'or': exp = [(Lx + [x[1]], R), (Lx + [x[2]], R)]
        elif rule == 'impL' and x[0] == 'imp': exp = [(Lx, R + [x[1]]), (Lx + [x[2]], R)]
        elif rule == 'notR' and x[0] == 'not': exp = [(L + [x[1]], Rx)]
        elif rule == 'orR' and x[0] == 'or': exp = [(L, Rx + [x[1], x[2]])]
        elif rule == 'impR' and x[0] == 'imp': exp = [(L + [x[1]], Rx + [x[2]])]
        elif rule == 'andR' and x[0] == 'and': exp = [(L, Rx + [x[1]]), (L, Rx + [x[2]])]
        elif rule in ('EvL', 'EvR', 'SrchR') and x[0] == 'atom':
            s = _succ_indep(x, mode)
            if rule == 'EvL' and s and s[0] == 'det': exp = [(Lx + [s[1]], R)]
            if rule == 'EvR' and s and s[0] == 'det': exp = [(L, Rx + [s[1]])]
            if rule == 'SrchR' and s and s[0] == 'srch':
                exp = [(L + [s[1]], Rx + [s[2]]), (L, Rx + [s[1], s[3]])]
        if exp is None or len(exp) != len(ps): raise ReplayError(rule + ' shape or side condition')
        tot = 1
        for (eL, eR), p in zip(exp, ps):
            if not (same(eL, p['L']) and same(eR, p['R'])): raise ReplayError(rule + ' premise mismatch')
            tot += rec(p)
        return tot
    if node['L'] or node['R'] != [root]: raise ReplayError('root sequent')
    n = rec(node)
    if n > b: raise ReplayError('size %d > b' % n)
    return n


def witness_from_rt(w):
    """Witness data returned by COREW -> host witness tree (dicts with host formulas)."""
    rule, (Ls, (Rs, (x, (size, ps)))) = w

    def lst(v):
        out = []
        while v != 0: out.append(v[0]); v = v[1]
        return out
    name = {0: 'ax', 1: 'run', 2: 'runneg', 4: 'jlob'}.get(rule) or RULE_NAMES[rule]
    return {'rule': name, 'size': size, 'L': [rt_to_formula(f) for f in lst(Ls)], 'R': [rt_to_formula(f) for f in lst(Rs)],
            'x': None if x == 0 else rt_to_formula(x), 'prem': [witness_from_rt(p) for p in lst(ps)]}


def witness_to_rt(nd):
    """Host witness tree -> witness data (for the checker term CHECK_i)."""
    code = {'ax': 0, 'run': 1, 'runneg': 2, 'jlob': 4}.get(nd['rule'])
    if code is None: code = {v: k for k, v in RULE_NAMES.items()}[nd['rule']]

    def mk(xs):
        out = 0
        for x in reversed(xs): out = (x, out)
        return out
    x = 0 if nd.get('x') is None else formula_to_rt(nd['x'])
    return (code, (mk([formula_to_rt(f) for f in nd['L']]), (mk([formula_to_rt(f) for f in nd['R']]),
            (x, (nd['size'], mk([witness_to_rt(p) for p in nd['prem']]))))))


def term_check(mode, c, psi_rt, U, witness_rt, K=INF):
    """Run the checker term CHECK_mode on a supplied derivation: (result 'T'/'F'/..., steps)."""
    x = (core_arg(c, psi_rt, U), witness_rt)
    v, n = evaluate(('app', lib('CHECK%d' % mode), rt_to_tval(x)), K)
    return v, n


# ----------------------------------------------------------------------------------------------------------------
# 9. An independent brute-force prover for small budgets (no memo lower bounds, no instance order; sets of
#    formulas; successors from the replay checker's own successor function)
# ----------------------------------------------------------------------------------------------------------------
class Brute:
    def __init__(self, mode, b, root, U):
        self.mode, self.b, self.root, self.U = mode, b, root, U
        self.H = ('box', mode, b, U, root)
        self.chain = [root]
        while self.chain[-1][0] == 'atom':
            s = _succ_indep(self.chain[-1], 0)
            if s is None or s[0] != 'det' or s[1][0] != 'atom': break
            self.chain.append(s[1])
        self.memo = {}
        self.boxes = {}

    def truth(self, x):
        v = self.boxes.get(x)
        if v is None:
            v = box_truth(x[1], x[2], x[3], formula_to_rt(x[4]))[0] == 'T'
            self.boxes[x] = v
        return v

    def der(self, L, R, n):
        """Is L |- R derivable with at most n sequents?"""
        if n < 1: return False
        key = (L, R)
        lo_true, hi_false = self.memo.get(key, (None, 0))
        if lo_true is not None and lo_true <= n: return True
        if n <= hi_false: return False
        ok = self._der(L, R, n)
        lo_true, hi_false = self.memo.get(key, (None, 0))
        if ok: self.memo[key] = (n if lo_true is None else min(lo_true, n), hi_false)
        else: self.memo[key] = (lo_true, max(hi_false, n))
        return ok

    def _der(self, L, R, n):
        if BOTH in L or TOPH in R or any(x in R and x[0] in ('atom', 'box') for x in L): return True
        for y in R:
            if y[0] == 'box' and (self.mode == 1 or (y != self.H and self.truth(y))): return True
        for x in L:
            if x[0] == 'box' and (self.mode == 1 or (x != self.H and not self.truth(x))): return True

        def splits(a, b_):
            for s1 in range(1, n - 1):
                if self.der(a[0], a[1], s1) and self.der(b_[0], b_[1], n - 1 - s1): return True
            return False
        for x in L:
            Lx = L - {x}
            k = x[0]
            if k == 'not' and self.der(Lx, R | {x[1]}, n - 1): return True
            if k == 'and' and self.der(Lx | {x[1], x[2]}, R, n - 1): return True
            if k == 'or' and splits((Lx | {x[1]}, R), (Lx | {x[2]}, R)): return True
            if k == 'imp' and splits((Lx, R | {x[1]}), (Lx | {x[2]}, R)): return True
            if k == 'atom':
                s = _succ_indep(x, self.mode)
                if s and s[0] == 'det' and self.der(Lx | {s[1]}, R, n - 1): return True
        for x in R:
            Rx = R - {x}
            k = x[0]
            if k == 'not' and self.der(L | {x[1]}, Rx, n - 1): return True
            if k == 'or' and self.der(L, Rx | {x[1], x[2]}, n - 1): return True
            if k == 'imp' and self.der(L | {x[1]}, Rx | {x[2]}, n - 1): return True
            if k == 'and' and splits((L, Rx | {x[1]}), (L, Rx | {x[2]})): return True
            if k == 'atom':
                s = _succ_indep(x, self.mode)
                if s and s[0] == 'det' and self.der(L, Rx | {s[1]}, n - 1): return True
                if s and s[0] == 'srch' and splits((L | {s[1]}, Rx | {s[2]}), (L, Rx | {s[1], s[3]})): return True
            elig = (self.mode == 0 and x in self.chain) or (self.mode == 1 and k not in ('top', 'bot'))
            if elig and self.der(frozenset([self.H]), frozenset([self.root]), n - 1): return True
        return False

    def minsize(self):
        for n in range(1, self.b + 1):
            if self.der(frozenset(), frozenset([self.root]), n): return n
        return None
