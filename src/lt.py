"""The realizable language L_T and the bounded calculus K_T (specs/2026-10-06-realizable-language.md; notes/realizable-
language.md §1; frozen design in predictions/2026-10-06-realizable-language.md).

L_T: an untyped call-by-value lambda-calculus (de Bruijn) with constructors, naturals, pairs, if, fix, quoted terms as
data, formula builders, `prove`, `sprove` (the sloppy checker's primitive), `run` (bounded simulation) and sim frames.
Small-step substitution semantics on closed terms; one step per contraction.

K_T: G3 + evaluation rules (EvR/EvL one deterministic step; PrvR/PrvL a prove step with its box obligation) + BoxEq
(along deterministic chains) + Nec + JLoeb(S, m), no cut.  Truth in the standard model: a box is true iff K_T derives
its content within its budget; an atom <s>=>a is true iff the idealized evaluation of s reaches a.

The prover: iterative deepening n = 1..b over `minsize`, a memoized search over all rule instances; its work W is the
number of expansions (memo misses).  Deterministic given (formula, budget): every iteration is in a per-search
discovery order, never in hash order.
"""
import sys
sys.setrecursionlimit(100000)

INF = 1 << 30

# ----------------------------------------------------------------------------------------------------------------
# Terms
# ----------------------------------------------------------------------------------------------------------------
VALUE_TAGS = ('lam', 'con', 'nat', 'quote', 'fix', 'fv')
CON = {n: ('con', n) for n in ('C', 'D', 'T', 'F', 'TO')}
C_, D_, T_, F_, TO_ = CON['C'], CON['D'], CON['T'], CON['F'], CON['TO']


def is_value(t):
    tag = t[0]
    if tag in VALUE_TAGS: return True
    if tag == 'pair': return is_value(t[1]) and is_value(t[2])
    return False


def subst(t, v, d=0):
    """t[d := v] for a closed value v; free variables above d are decremented.  Never enters quotes or formula values."""
    tag = t[0]
    if tag == 'v':
        i = t[1]
        if i == d: return v
        if i > d: return ('v', i - 1)
        return t
    if tag in ('con', 'nat', 'quote', 'fv'): return t
    if tag == 'lam': return ('lam', subst(t[1], v, d + 1))
    if tag == 'fix': return ('fix', subst(t[1], v, d + 1))
    if tag == 'mk': return ('mk', t[1]) + tuple(subst(a, v, d) for a in t[2:])
    if tag == 'sim': return ('sim', t[1], subst(t[2], v, d))
    return (tag,) + tuple(subst(a, v, d) for a in t[1:])


TAGCODE = {'v': 0, 'lam': 1, 'app': 2, 'con': 3, 'nat': 4, 'pair': 5, 'fst': 6, 'snd': 7, 'if': 8, 'fix': 9,
           'quote': 10, 'eq': 11, 'mk': 12, 'prove': 13, 'sprove': 14, 'run': 15, 'sim': 16, 'fv': 17}
CONCODE = {'C': 0, 'D': 1, 'T': 2, 'F': 3, 'TO': 4}
MKCODE = {'plays': 0, 'not': 1, 'and': 2, 'or': 3, 'imp': 4, 'box': 5, 'bot': 6, 'top': 7}


def _plist(xs):
    out = ('nat', 0)
    for x in reversed(xs): out = ('pair', x, out)
    return out


def quote_payload(t):
    """The payload of the nested-pair encoding of t: quote(t) behaves as pair(nat tag, payload)."""
    tag = t[0]
    Q = lambda s: ('quote', s)
    if tag == 'v': return ('nat', t[1])
    if tag in ('lam', 'fix'): return Q(t[1])
    if tag == 'con': return ('nat', CONCODE[t[1]])
    if tag == 'nat': return ('nat', t[1])
    if tag == 'quote': return Q(t[1])
    if tag == 'mk': return ('pair', ('nat', MKCODE[t[1]]), _plist([Q(a) for a in t[2:]]))
    if tag == 'sim': return ('pair', ('nat', t[1]), Q(t[2]))
    if tag == 'fv': return ('nat', 0)
    return _plist([Q(a) for a in t[1:]])


def enc_full(v):
    """Full nested-pair encoding of a value (for eq between a quote and an explicit encoding)."""
    if v[0] == 'quote':
        return ('pair', ('nat', TAGCODE[v[1][0]]), enc_full(quote_payload(v[1])))
    if v[0] == 'pair': return ('pair', enc_full(v[1]), enc_full(v[2]))
    return v


def values_equal(a, b):
    if a == b: return True
    if a[0] == 'quote' or b[0] == 'quote' or a[0] == 'pair' or b[0] == 'pair':
        return enc_full(a) == enc_full(b)
    return False


# formula values (data): ('plays', x, y, a) with x, y closed program terms; ('not', f); ('and'|'or'|'imp', f, g);
# ('box', c, f); ('bot',); ('top',)
def mk_formula(kind, args):
    if kind == 'plays':
        x, y, a = args
        if x[0] != 'quote' or y[0] != 'quote' or a not in (C_, D_): return None
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


STUCK = 'stuck'


def contract(r):
    """Contract a redex whose immediate subterms are values.  Returns the contractum, STUCK, or ('PROVE', c, fv)."""
    tag = r[0]
    if tag == 'app':
        f, a = r[1], r[2]
        if f[0] == 'lam': return subst(f[1], a)
        if f[0] == 'fix': return ('app', subst(f[1], f), a)
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
    if tag == 'mk':
        out = mk_formula(r[1], r[2:])
        return STUCK if out is None else out
    if tag == 'prove':
        n, f = r[1], r[2]
        if n[0] != 'nat' or f[0] != 'fv': return STUCK
        return ('PROVE', n[1], f[1])
    if tag == 'sprove':
        n, f = r[1], r[2]
        if n[0] != 'nat' or f[0] != 'fv': return STUCK
        return T_ if n[1] >= 1 else F_
    if tag == 'run':
        k, x, y = r[1], r[2], r[3]
        if k[0] != 'nat' or x[0] != 'quote' or y[0] != 'quote': return STUCK
        return ('sim', k[1], ('app', ('app', x[1], x), y))
    return STUCK


# evaluation-context frames: (kind, index of the hole, the node with the hole) ; sim frames ('sim', k)
def decompose(t):
    """Returns (ctx, kind, payload): kind 'value' (t is a value), 'stuck', 'det' (payload = contractum),
    'prove' (payload = (c, fv)), with ctx the list of frames from outermost to innermost."""
    ctx = []
    while True:
        tag = t[0]
        if tag in VALUE_TAGS:
            return ctx, 'value', t
        if tag == 'v':
            return ctx, 'stuck', None
        if tag == 'sim':
            k, inner = t[1], t[2]
            if is_value(inner): return ctx, 'det', inner
            if k == 0: return ctx, 'det', TO_
            ictx, ikind, ipay = decompose(inner)
            if ikind == 'stuck': return ctx, 'det', TO_
            ctx.append(('sim', k))
            ctx.extend(ictx)
            return ctx, ikind, ipay
        if tag == 'if':
            if not is_value(t[1]):
                ctx.append(('hole', t, 1)); t = t[1]; continue
            out = contract(t)
            return (ctx, 'stuck', None) if out is STUCK else (ctx, 'det', out)
        # strict forms: evaluate subterms left to right
        start = 2 if tag == 'mk' else 1
        for i in range(start, len(t)):
            if not is_value(t[i]):
                ctx.append(('hole', t, i)); t = t[i]; break
        else:
            if tag == 'pair': return ctx, 'value', t
            out = contract(t)
            if out is STUCK: return ctx, 'stuck', None
            if out[0] == 'PROVE': return ctx, 'prove', (out[1], out[2])
            return ctx, 'det', out
        continue


def plug(ctx, x, dec=1):
    """Rebuild the term from frames, plugging x; every sim frame's fuel is decreased by `dec`."""
    for fr in reversed(ctx):
        if fr[0] == 'sim':
            x = ('sim', fr[1] - dec, x)
        else:
            node, i = fr[1], fr[2]
            x = node[:i] + (x,) + node[i + 1:]
    return x


def step(t):
    """One step of the idealized/primitive-assisted semantics.
    Returns ('value', v) | ('stuck',) | ('det', t') | ('prove', c, fv, tT, tF)."""
    ctx, kind, pay = decompose(t)
    if kind == 'value': return ('value', t)
    if kind == 'stuck': return ('stuck',)
    if kind == 'det': return ('det', plug(ctx, pay))
    c, fv = pay
    return ('prove', c, fv, plug(ctx, T_), plug(ctx, F_))


def sim_fuels(t):
    """Fuels of the sim frames enclosing the next redex (outermost first)."""
    ctx, kind, pay = decompose(t)
    return [fr[1] for fr in ctx if fr[0] == 'sim'], ctx


def initial(p, q):
    return ('app', ('app', p, ('quote', p)), ('quote', q))


# ----------------------------------------------------------------------------------------------------------------
# Frozen named programs (predictions/2026-10-06-realizable-language.md)
# ----------------------------------------------------------------------------------------------------------------
ME, THEM = ('v', 1), ('v', 0)


def L2(body): return ('lam', ('lam', body))


def PL(x, y, a): return ('mk', 'plays', x, y, a)


def CONb(b): return ('mk', 'not', ('mk', 'box', ('nat', b), ('mk', 'bot')))


PROG_C = L2(C_)
PROG_D = L2(D_)


def FB(b): return L2(('if', ('prove', ('nat', b), PL(THEM, ME, C_)), C_, D_))
def FB1(b): return L2(('if', ('prove', ('nat', b), ('mk', 'imp', CONb(b), PL(THEM, ME, C_))), C_, D_))
def PB(b): return L2(('if', ('prove', ('nat', b), PL(THEM, ME, C_)),
                      ('if', ('prove', ('nat', b), ('mk', 'imp', CONb(b), PL(THEM, ('quote', PROG_D), D_))), C_, D_),
                      D_))
def G(b): return L2(('if', ('prove', ('nat', b), PL(THEM, ME, C_)), D_, C_))
def PSTAR(b): return L2(('if', ('prove', ('nat', b), ('mk', 'imp', CONb(b), PL(THEM, ME, C_))),
                         ('if', ('prove', ('nat', b), PL(THEM, ME, C_)), D_, C_), D_))
def SF(k): return L2(('if', ('eq', ('run', ('nat', k), THEM, ME), C_), C_, D_))
def SC(b): return L2(('if', ('sprove', ('nat', b), PL(THEM, ME, C_)), C_, D_))
def VLET(b): return L2(('app', ('lam', ('if', ('prove', ('nat', b), ('v', 0)), C_, D_)), PL(THEM, ME, C_)))
def VWRAP(b): return L2(('app', ('lam', ('v', 0)), ('app', ('app', FB(b), ME), THEM)))
def VRENAME(b): return FB(b)          # de Bruijn: a renamed spelling is the same term


def catalogue(b, k=None):
    """The eleven named programs at budget b (SF with fuel k, default k = b)."""
    k = b if k is None else k
    return {'C': PROG_C, 'D': PROG_D, 'FB': FB(b), 'FB1': FB1(b), 'PB': PB(b), 'G': G(b), 'P*': PSTAR(b),
            'SF': SF(k), 'SC': SC(b), 'Vlet': VLET(b), 'Vwrap': VWRAP(b)}


def show_term(t):
    tag = t[0]
    if tag == 'v': return 'v%d' % t[1]
    if tag == 'con': return t[1]
    if tag == 'nat': return str(t[1])
    if tag == 'lam': return '\\.' + show_term(t[1])
    if tag == 'quote': return '<' + NAMES.get(t[1], '..') + '>'
    if tag == 'fv': return '{' + show_fv(t[1]) + '}'
    if tag == 'mk': return 'mk_%s(%s)' % (t[1], ','.join(show_term(a) for a in t[2:]))
    if tag == 'sim': return 'sim[%d](%s)' % (t[1], show_term(t[2]))
    if t in NAMES: return NAMES[t]
    return '%s(%s)' % (tag, ','.join(show_term(a) if isinstance(a, tuple) else str(a) for a in t[1:]))


NAMES = {}


def register_names(cat):
    for n, p in cat.items(): NAMES[p] = n


def show_fv(f):
    k = f[0]
    if k == 'plays': return 'plays(%s,%s,%s)' % (NAMES.get(f[1], '?'), NAMES.get(f[2], '?'), f[3])
    if k == 'bot': return 'F'
    if k == 'top': return 'T'
    if k == 'not': return '~' + show_fv(f[1])
    if k == 'box': return '[%d]%s' % (f[1], show_fv(f[2]))
    return '(%s %s %s)' % (show_fv(f[1]), {'and': '&', 'or': '|', 'imp': '->'}[k], show_fv(f[2]))


# ----------------------------------------------------------------------------------------------------------------
# The calculus K_T: formulas
# ----------------------------------------------------------------------------------------------------------------
class Theory:
    """Interning of K_T formulas and the evaluation structure of atoms.  Formula ids are global (history-dependent);
    the prover never iterates in id order (see Search.idx)."""

    def __init__(self):
        self.F = []; self.fid = {}
        self.BOT = self.f(('bot',)); self.TOP = self.f(('top',))
        self._step = {}       # atom state -> step result
        self._fv = {}
        self._astep = {}

    def f(self, t):
        i = self.fid.get(t)
        if i is None:
            i = len(self.F); self.fid[t] = i; self.F.append(t)
        return i

    def reading(self, state, a):
        """rho(state, a): TOP / BOT for terminal states, else the atom."""
        r = self.state_step(state)
        if r[0] == 'value': return self.TOP if r[1] == ('con', a) else self.BOT
        if r[0] == 'stuck': return self.BOT
        return self.f(('atom', state, a))

    def state_step(self, state):
        r = self._step.get(state)
        if r is None:
            r = step(state); self._step[state] = r
        return r

    def from_fv(self, fv):
        """Formula value (data) -> formula id."""
        i = self._fv.get(fv)
        if i is not None: return i
        k = fv[0]
        if k == 'plays': i = self.reading(initial(fv[1], fv[2]), fv[3])
        elif k == 'bot': i = self.BOT
        elif k == 'top': i = self.TOP
        elif k == 'not': i = self.f(('not', self.from_fv(fv[1])))
        elif k == 'box': i = self.f(('box', fv[1], self.from_fv(fv[2])))
        else: i = self.f((k, self.from_fv(fv[1]), self.from_fv(fv[2])))
        self._fv[fv] = i
        return i

    def box(self, c, a): return self.f(('box', c, a))
    def plays(self, p, q, a): return self.reading(initial(p, q), a)

    def atom_step(self, x):
        """For an atom id: ('det', next reading id) or ('prove', c, psi id, box id, rhoT id, rhoF id)."""
        r = self._astep.get(x)
        if r is None:
            r = self._astep[x] = self._atom_step(x)
        return r

    def _atom_step(self, x):
        _, state, a = self.F[x]
        r = self.state_step(state)
        if r[0] == 'det': return ('det', self.reading(r[1], a))
        if r[0] == 'prove':
            c, fv = r[1], r[2]
            psi = self.from_fv(fv)
            return ('prove', c, psi, self.box(c, psi), self.reading(r[3], a), self.reading(r[4], a))
        raise ValueError('atom with terminal state')

    def show(self, i):
        t = self.F[i]; k = t[0]
        if k == 'atom':
            st = t[1]
            if st[0] == 'app' and st[1][0] == 'app' and st[1][2][0] == 'quote' and st[2][0] == 'quote' \
                    and st[1][1] == st[1][2][1]:
                return 'plays(%s,%s,%s)' % (NAMES.get(st[1][1], '?'), NAMES.get(st[2][1], '?'), t[2])
            return '<%s>=>%s' % (show_term(st), t[2])
        if k == 'bot': return 'F'
        if k == 'top': return 'T'
        if k == 'not': return '~' + self.show(t[1])
        if k == 'box': return '[%d]%s' % (t[1], self.show(t[2]))
        return '(%s %s %s)' % (self.show(t[1]), {'and': '&', 'or': '|', 'imp': '->'}[k], self.show(t[2]))


# ----------------------------------------------------------------------------------------------------------------
# The prover
# ----------------------------------------------------------------------------------------------------------------
class WorkExceeded(Exception):
    pass


class Search:
    """One prove call: iterative deepening on |- root up to cap b, fresh memo.  `jlob=False` is the control K_T^-.
    mem='closure' (the frozen rule: members from Mem(A_i), notes §1.7) or 'full' (every atom and box content of the
    root closure; the empirical check that the restriction is not binding)."""

    def __init__(self, th, root, jlob=True, mem='closure', limit=None, closure_cap=20000):
        self.th = th; self.root = root; self.jlob = jlob; self.mem = mem
        self.limit = limit if limit is not None else INF
        self.work = 0
        self.memo = {}; self.arg = {}
        self.jmemo = {}; self.jarg = {}
        self.idx = {}
        self.closure_cap = closure_cap
        self._build_closure()
        self._memc = {}

    # -- deterministic discovery order ---------------------------------------------------------------------------
    def ix(self, f):
        i = self.idx.get(f)
        if i is None:
            i = len(self.idx); self.idx[f] = i
        return i

    def srt(self, fs):
        return sorted(fs, key=self.ix)

    # -- closure, members, upstream ---------------------------------------------------------------------------
    def _succ(self, x):
        """Closure successors of formula x, in a fixed order."""
        th = self.th; t = th.F[x]; k = t[0]
        if k == 'atom':
            s = th.atom_step(x)
            if s[0] == 'det': return [s[1]]
            return [s[3], s[4], s[5]]           # box, rhoT, rhoF
        if k == 'box': return [t[2]]
        if k == 'not': return [t[1]]
        if k in ('and', 'or', 'imp'): return [t[1], t[2]]
        return []

    def _closure_from(self, x):
        seen = {x: None}; order = [x]; i = 0
        while i < len(order):
            y = order[i]; i += 1
            for z in self._succ(y):
                if z not in seen:
                    seen[z] = None; order.append(z)
                    if len(order) > self.closure_cap: raise RuntimeError('closure cap exceeded')
        return order

    def _build_closure(self):
        th = self.th
        order = self._closure_from(self.root)
        for y in order: self.ix(y)
        self.closure = order
        self.pred = {}
        for y in order:
            if th.F[y][0] == 'atom':
                s = th.atom_step(y)
                if s[0] == 'det' and th.F[s[1]][0] == 'atom':
                    self.pred.setdefault(s[1], []).append(y)
        self.merges = sum(1 for v in self.pred.values() if len(v) > 1)

    def upstream(self, x):
        out = []; stack = list(self.pred.get(x, ()))
        seen = set()
        while stack:
            y = stack.pop()
            if y in seen: continue
            seen.add(y); out.append(y)
            stack.extend(self.pred.get(y, ()))
        return sorted(out, key=self.ix)

    def members(self, a):
        """Mem(a): atoms and box contents of closure(a), plus a's upstream chain (notes §1.7)."""
        m = self._memc.get(a)
        if m is not None: return m
        th = self.th
        if self.mem == 'full':
            src = self.closure
        else:
            src = self._closure_from(a)
        out = []
        seen = set()
        for y in src:
            t = th.F[y]
            if t[0] == 'atom' and y not in seen:
                seen.add(y); out.append(y)
            if t[0] == 'box' and t[2] not in seen and th.F[t[2]][0] not in ('top', 'bot'):
                seen.add(t[2]); out.append(t[2])
        for y in self.upstream(a):
            if y not in seen: seen.add(y); out.append(y)
        out = sorted(out, key=self.ix)
        self._memc[a] = out
        return out

    # -- axioms ------------------------------------------------------------------------------------------------
    def boxeq(self, a, A, c, B):
        """Gamma, [a]A |- [c]B by Ax/BoxEq (i)-(iii)."""
        if A == B: return a <= c
        th = self.th
        if th.F[A][0] != 'atom': return False
        # B downstream of A (ii): a <= c ; A downstream of B (iii): a + k <= c
        k = self.dist(A, B)
        if k is not None: return a <= c
        if th.F[B][0] != 'atom': return False
        k = self.dist(B, A)
        if k is not None: return a + k <= c
        return False

    def dist(self, A, B):
        """k >= 1 with A >_k B (B a downstream reading of atom A along deterministic steps), else None."""
        th = self.th
        x = A; k = 0
        while th.F[x][0] == 'atom':
            s = th.atom_step(x)
            if s[0] != 'det': return None
            x = s[1]; k += 1
            if x == B: return k
            if k > 100000: return None
        return None

    def axiom(self, L, R):
        th = self.th; F = th.F
        if th.BOT in L or th.TOP in R: return ('ax',)
        for x in L:
            if x in R and F[x][0] in ('atom', 'box'): return ('ax', x)
        lb = [x for x in L if F[x][0] == 'box']
        if lb:
            for y in R:
                if F[y][0] != 'box': continue
                for x in lb:
                    if self.boxeq(F[x][1], F[x][2], F[y][1], F[y][2]): return ('boxeq', x, y)
        return None

    # -- minimal size --------------------------------------------------------------------------------------------
    def ms(self, L, R, cap):
        """Minimal size of L |- R if <= cap (exact); otherwise a lower bound > cap (INF: no derivation at any size).
        Lower bounds are the minimum over all rule instances of the instance's lower bound (notes §1.6)."""
        if cap < 1: return 1
        key = (L, R)
        e = self.memo.get(key)
        if e is not None:
            v, exact = e
            if exact or v > cap: return v
        self.work += 1
        if self.work > self.limit: raise WorkExceeded()
        ax = self.axiom(L, R)
        if ax is not None:
            self.memo[key] = (1, True); self.arg[key] = ax
            return 1
        best = INF; arg = None          # best exact value found (<= cap)
        lb = INF                         # min lower bound over instances not achieving <= cap
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

        def two(P1, P2, tag, x):
            nonlocal best, arg, lb
            lim = min(c, best - 1)
            s1 = self.ms(P1[0], P1[1], lim - 2)
            if s1 > lim - 2:
                lb = min(lb, 1 + s1 + 1); return
            s2 = self.ms(P2[0], P2[1], lim - 1 - s1)
            if s2 > lim - 1 - s1:
                lb = min(lb, 1 + s1 + s2); return
            best, arg = 1 + s1 + s2, (tag, x, [P1, P2])

        for x in self.srt(L):
            t = F[x]; k = t[0]
            Lx = L - {x}
            if k == 'not': one((Lx, R | {t[1]}), 'notL', x)
            elif k == 'and': one((Lx | {t[1], t[2]}, R), 'andL', x)
            elif k == 'or': two((Lx | {t[1]}, R), (Lx | {t[2]}, R), 'orL', x)
            elif k == 'imp': two((Lx, R | {t[1]}), (Lx | {t[2]}, R), 'impL', x)
            elif k == 'atom':
                s0 = th.atom_step(x)
                if s0[0] == 'det': one((Lx | {s0[1]}, R), 'EvL', x)
                else:
                    _, cc, psi, bx, rT, rF = s0
                    two((Lx | {bx, rT}, R), (Lx | {rF}, R | {bx}), 'PrvL', x)
        for x in self.srt(R):
            t = F[x]; k = t[0]
            Rx = R - {x}
            if k == 'not': one((L | {t[1]}, Rx), 'notR', x)
            elif k == 'or': one((L, Rx | {t[1], t[2]}), 'orR', x)
            elif k == 'imp': one((L | {t[1]}, Rx | {t[2]}), 'impR', x)
            elif k == 'and': two((L, Rx | {t[1]}), (L, Rx | {t[2]}), 'andR', x)
            elif k == 'atom':
                s0 = th.atom_step(x)
                if s0[0] == 'det': one((L, Rx | {s0[1]}), 'EvR', x)
                else:
                    _, cc, psi, bx, rT, rF = s0
                    two((L | {bx}, Rx | {rT}), (L, Rx | {bx, rF}), 'PrvR', x)
            elif k == 'box':
                bc, A = t[1], t[2]
                lim = min(bc, min(c, best - 1) - 1)
                P = (frozenset(), frozenset([A]))
                s = self.ms(P[0], P[1], lim)
                if s <= lim:
                    best, arg = 1 + s, ('Nec', x, [P])
                elif s <= bc:
                    lb = min(lb, 1 + s)          # Nec possible only above the current cap
                # s > bc: Nec impossible at any size
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

    # -- JLoeb ----------------------------------------------------------------------------------------------------
    def J(self, X, cap):
        """Minimal JLoeb instance concluding X (a member, or a downstream reduct of a member) if <= cap (exact),
        else a lower bound > cap (INF: none at any size)."""
        if cap < 2: return 2
        e = self.jmemo.get(X)
        if e is not None:
            v, exact = e
            if exact or v > cap: return v
        self.work += 1
        if self.work > self.limit: raise WorkExceeded()
        th = self.th
        best = INF; arg = None; lb = INF
        concl = [X] + (self.upstream(X) if th.F[X][0] == 'atom' else [])
        for Ai in concl:
            mem = [y for y in self.members(Ai) if y != Ai]
            cands = [(Ai,)]
            cands += [(Ai, y) for y in mem]
            for i in range(len(mem)):
                for j in range(i + 1, len(mem)):
                    cands.append((Ai, mem[i], mem[j]))
            for S in cands:
                lim = min(cap, best - 1)
                v, m, keys = self._jinst(S, lim)
                if v <= lim:
                    best, arg = v, (Ai, S, m, keys)
                else:
                    lb = min(lb, v)
        if best <= cap:
            self.jmemo[X] = (best, True); self.jarg[X] = arg
            return best
        v = max(lb, cap + 1)
        old = self.jmemo.get(X)
        if old is None or (not old[1] and old[0] < v):
            self.jmemo[X] = (v, False)
        return v

    def _jinst(self, S, cap):
        """Smallest JLoeb(S, m) instance: m from 1 + |S| upward, jumping to the instance size.  Returns
        (size, m, premise keys) with size <= cap, or (lower bound > cap, None, None).  Premise sizes are
        non-decreasing in m (a larger m is a weaker hypothesis), so a bound at m bounds every larger m."""
        th = self.th
        m = 1 + len(S)
        if m > cap: return m, None, None
        while True:
            H = frozenset(th.box(m, A) for A in S)
            tot = 1; keys = []
            for idx, A in enumerate(S):
                rem = cap - tot - (len(S) - idx - 1)
                s = self.ms(H, frozenset([A]), rem)
                if s > rem:
                    return (INF if s >= INF else max(cap + 1, tot + s + (len(S) - idx - 1))), None, None
                tot += s; keys.append((H, frozenset([A])))
            if tot <= m: return tot, m, keys
            m = tot
            if m > cap: return m, None, None

    # -- iterative deepening ---------------------------------------------------------------------------------
    def prove(self, b):
        """Iterative deepening n = 1..b.  Returns (found: bool, minimal size or None)."""
        R = frozenset([self.root])
        for n in range(1, b + 1):
            s = self.ms(frozenset(), R, n)
            if s <= n: return True, s
        return False, None

    # -- witness ------------------------------------------------------------------------------------------------
    def witness(self, L, R):
        """The argmin derivation of L |- R as a nested dict (requires an exact memo entry)."""
        v, exact = self.memo[(L, R)]
        assert exact
        a = self.arg[(L, R)]
        node = {'L': sorted(L, key=self.ix), 'R': sorted(R, key=self.ix), 'size': v, 'rule': a[0]}
        if a[0] == 'ax':
            node['princ'] = a[1] if len(a) > 1 else None
            return node
        if a[0] == 'boxeq':
            node['princ'] = (a[1], a[2]); return node
        node['princ'] = a[1]
        if a[0] == 'JLob':
            X = a[1]
            Ai, S, m, keys = self.jarg[X]
            node['jlob'] = {'Ai': Ai, 'S': list(S), 'm': m}
            node['prem'] = [self.witness(*k) for k in keys]
            return node
        node['prem'] = [self.witness(*k) for k in a[2]]
        return node


def wsize(w):
    if w['rule'] == 'JLob': return 1 + sum(wsize(p) for p in w['prem'])
    return 1 + sum(wsize(p) for p in w.get('prem', []))


def wlambda(w):
    return (1 if w['rule'] == 'JLob' else 0) + sum(wlambda(p) for p in w.get('prem', []))


def wnodes(w):
    yield w
    for p in w.get('prem', []):
        yield from wnodes(p)


# ----------------------------------------------------------------------------------------------------------------
# Prover service with a host cache (a cache of a deterministic function; W is the per-call work)
# ----------------------------------------------------------------------------------------------------------------
class Prover:
    def __init__(self, th=None, jlob=True, mem='closure', limit=None):
        self.th = th or Theory(); self.jlob = jlob; self.mem = mem
        self.limit = limit
        self.cache = {}

    def query(self, psi, c):
        """Box truth of [c]psi with the search's outcome: dict(found, size, W, lam, merges, witness search)."""
        key = (psi, c)
        r = self.cache.get(key)
        if r is not None: return r
        s = Search(self.th, psi, jlob=self.jlob, mem=self.mem, limit=self.limit)
        try:
            found, size = s.prove(c)
            r = {'found': found, 'size': size, 'W': s.work, 'complete': True, 'merges': s.merges,
                 'closure': len(s.closure)}
        except WorkExceeded:
            r = {'found': None, 'size': None, 'W': s.work, 'complete': False, 'merges': s.merges,
                 'closure': len(s.closure)}
        r['search'] = s if (r.get('found')) else None
        self.cache[key] = r
        return r

    def witness(self, psi, c):
        r = self.query(psi, c)
        if not r.get('found'): return None
        s = r['search']
        return s.witness(frozenset(), frozenset([psi]))


# ----------------------------------------------------------------------------------------------------------------
# Actual evaluation (plays)
# ----------------------------------------------------------------------------------------------------------------
def run_play(prover, p, q, K, semantics='prim', trace=None):
    """eval_K(p <p> <q>).  semantics 'prim' (prove = 1 step) or 'search' (prove = W steps, charged to every frame).
    Returns dict(play in {'C','D','BOT'}, steps, proves=[(psi id, c, outcome, W, in_sim)], reason)."""
    th = prover.th
    t = initial(p, q)
    used = 0
    proves = []
    while True:
        if trace is not None: trace.append(t)
        ctx, kind, pay = decompose(t)
        if kind == 'value':
            v = t
            play = v[1] if v in (C_, D_) else 'BOT'
            return {'play': play, 'steps': used, 'proves': proves, 'reason': 'value' if play != 'BOT' else 'other-value'}
        if kind == 'stuck':
            return {'play': 'BOT', 'steps': used, 'proves': proves, 'reason': 'stuck'}
        if used >= K:
            return {'play': 'BOT', 'steps': used, 'proves': proves, 'reason': 'K'}
        if kind == 'det':
            t = plug(ctx, pay); used += 1
            continue
        c, fv = pay
        psi = th.from_fv(fv)
        fuels = [fr[1] for fr in ctx if fr[0] == 'sim']
        insim = len(fuels) > 0
        if semantics == 'prim':
            r = prover.query(psi, c)
            if not r['complete']: raise RuntimeError('host search incomplete under primitive-assisted charging')
            proves.append((psi, c, 'found' if r['found'] else 'refuted', r['W'], insim))
            t = plug(ctx, T_ if r['found'] else F_); used += 1
            continue
        # search-charged
        r = prover.query(psi, c)
        W = r['W'] if r['complete'] else INF
        G = K - used
        counters = [G] + fuels          # outermost first
        exceeded = [i for i, v in enumerate(counters) if v < W]
        if not exceeded:
            out = 'found' if r['found'] else 'refuted'
            proves.append((psi, c, out, W, insim))
            t = plug(ctx, T_ if r['found'] else F_, dec=W); used += W
            continue
        mv = min(counters[i] for i in exceeded)
        i0 = min(i for i in exceeded if counters[i] == mv)
        proves.append((psi, c, 'timeout', W, insim))
        if i0 == 0:
            return {'play': 'BOT', 'steps': K, 'proves': proves, 'reason': 'K-search'}
        # sim frame number i0 (1-based among sims) times out: replace that frame by TO, charge mv + 1 outside it
        nsim = 0; cut = None
        for j, fr in enumerate(ctx):
            if fr[0] == 'sim':
                nsim += 1
                if nsim == i0: cut = j; break
        t = plug(ctx[:cut], TO_, dec=mv + 1); used += mv + 1
        continue


def idealized_value(prover, t, cap=10 ** 6):
    """Idealized evaluation of a state: returns the terminal value (or 'stuck' / None if cap exceeded)."""
    th = prover.th
    n = 0
    while n < cap:
        r = th.state_step(t)
        if r[0] == 'value': return r[1]
        if r[0] == 'stuck': return 'stuck'
        if r[0] == 'det': t = r[1]
        else:
            q = prover.query(th.from_fv(r[2]), r[1])
            if not q['complete']: return None
            t = r[3] if q['found'] else r[4]
        n += 1
    return None


def truth(prover, x, _cache=None):
    """Truth of formula id x in the standard model (box truth by the exhaustive search)."""
    th = prover.th; t = th.F[x]; k = t[0]
    if k == 'top': return True
    if k == 'bot': return False
    if k == 'not': return not truth(prover, t[1])
    if k == 'and': return truth(prover, t[1]) and truth(prover, t[2])
    if k == 'or': return truth(prover, t[1]) or truth(prover, t[2])
    if k == 'imp': return (not truth(prover, t[1])) or truth(prover, t[2])
    if k == 'box':
        q = prover.query(t[2], t[1])
        if not q['complete']: raise RuntimeError('incomplete search in truth')
        return bool(q['found'])
    v = idealized_value(prover, t[1])
    if v is None: raise RuntimeError('idealized evaluation did not terminate within cap')
    return v == ('con', t[2])


def sequent_true(prover, L, R):
    return (not all(truth(prover, x) for x in L)) or any(truth(prover, y) for y in R)


def soundness_check(prover):
    """Every found box in the cache: its content is true; every sequent of its witness is true."""
    nbox = nseq = 0; bad = []
    for (psi, c), r in list(prover.cache.items()):
        if not r.get('found'): continue
        nbox += 1
        if not truth(prover, psi): bad.append(('box', psi, c))
        w = prover.witness(psi, c)
        for node in wnodes(w):
            nseq += 1
            if not sequent_true(prover, node['L'], node['R']): bad.append(('seq', psi, c, node['rule']))
    return nbox, nseq, bad


def render(th, w, indent=0, out=None):
    """Text rendering of a witness derivation."""
    out = [] if out is None else out
    L = ', '.join(th.show(x) for x in w['L']); R = ', '.join(th.show(x) for x in w['R'])
    extra = ''
    if w['rule'] == 'JLob':
        j = w['jlob']; extra = ' S={%s} m=%d' % (', '.join(th.show(x) for x in j['S']), j['m'])
    out.append('%s%s |- %s   [%s%s] (%d)' % ('  ' * indent, L, R, w['rule'], extra, w['size']))
    for p in w.get('prem', []):
        render(th, p, indent + 1, out)
    return out
