"""Step 1 of queue 75 (spec specs/2026-11-08-length-prior-t.md): the length prior over L_T^code syntax for `dollar3`.

The prior is a branching-probability model on terms: every node draws its tag uniformly among the machine's tags, the arity
fixes the tree, de Bruijn indices and `nat` literals are drawn with Elias-gamma probabilities of n + 1, `con` uniformly
among the five constants, `op` among the seven operators, `lib` among the library entries, `quote` and `sim` carry a term
(and `sim` a literal).  The mass of a term is the product of its per-node probabilities; the prior is a semimeasure (the
mass of infinite trees is lost).  Only the body of the arm-T frame `lam me. lam n. lam p. body` is drawn.

Machines: R0 = the 18 tags of lt_code (reading is `(capk k (run k' n p) me)` written out); R1 = R0 plus two arity-0 tags
`readn`, `readp` that expand (macro, at the right de Bruijn depth) to the arm-T reads
`(capk 400 (run 400 n p) me)` and `(capk 400 (run 400 p me) n)`.

Pieces: machines and masses (mass, extinction probability, size distribution), the evaluator with failed-read counting
and a taint tracker (a program whose evaluation never inspects its partners' sources is partner-independent), the
behavioural classifier (output and charge signature over a probe set, exact member match, response-map family), the
exhaustive enumerator to size s0 (with exact accounting of what it does not enumerate), the Monte Carlo sampler and the
sampled-interaction check.  The targeted search is in lt_prior_search.py.  Nothing existing is edited.
"""
import os, sys, math, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lt_code as L
import churn_primary_t as CT
import tplus as TP

# ====================================================================== machines
ARITY = {'v': 0, 'lam': 1, 'app': 2, 'con': 0, 'nat': 0, 'pair': 2, 'fst': 1, 'snd': 1, 'if': 3, 'fix': 1, 'quote': 1,
         'eq': 2, 'lib': 0, 'op': 2, 'capk': 3, 'run': 3, 'sim': 1, 'libsrc': 1, 'readn': 0, 'readp': 0}
EXCLUDED_ENUM = ('lib', 'libsrc', 'sim')          # not enumerated (their mass is accounted and sampled by Monte Carlo)
NLIB = len(L.LIB)


class Machine:
    def __init__(self, name, tags):
        self.name = name
        self.tags = list(tags)
        self.T = len(tags)
        self.n_by_arity = {a: sum(1 for t in tags if ARITY[t] == a) for a in range(4)}
        self.mean_arity = sum(ARITY[t] for t in tags) / self.T

    def gf(self, q, tags=None):
        tags = self.tags if tags is None else tags
        return sum(q ** ARITY[t] for t in tags) / self.T

    def extinction(self):
        """smallest fixed point of q = f(q) (the mass of finite trees); 1 if critical or subcritical."""
        if self.mean_arity <= 1.0:
            return 1.0
        q = 0.0
        for _ in range(100000):
            q2 = self.gf(q)
            if abs(q2 - q) < 1e-16:
                break
            q = q2
        return q

    def size_masses(self, smax, tags=None):
        """m[s] = total prior mass of the terms of node count s (sub-draws sum to one): the exact finite-size masses."""
        tags = self.tags if tags is None else tags
        nb = {a: sum(1 for t in tags if ARITY[t] == a) for a in range(4)}
        T = self.T
        m = [0.0] * (smax + 1)
        m[1] = nb[0] / T
        for s in range(2, smax + 1):
            tot = nb[1] * m[s - 1]
            for a in range(1, s - 1):
                tot += nb[2] * m[a] * m[s - 1 - a]
            for a in range(1, s - 2):
                for b in range(1, s - 1 - a):
                    c = s - 1 - a - b
                    if c >= 1:
                        tot += nb[3] * m[a] * m[b] * m[c]
            m[s] = tot / T
        return m


R0 = Machine('R0', L.TAGS)
R1 = Machine('R1', L.TAGS + ['readn', 'readp'])
MACHINES = {'R0': R0, 'R1': R1}
ENUM_TAGS = {k: [t for t in m.tags if t not in EXCLUDED_ENUM] for k, m in MACHINES.items()}


def elias(n):
    """Elias-gamma probability of the natural number n >= 0 (code of n + 1)."""
    return 2.0 ** -(2 * int(math.floor(math.log2(n + 1))) + 1)


def elias_range(a, b):
    """total Elias-gamma mass of the n+1 in [a, b] (a >= 1), exact."""
    tot = 0.0
    k = int(math.floor(math.log2(a)))
    while 2 ** k <= b:
        lo, hi = max(a, 2 ** k), min(b, 2 ** (k + 1) - 1)
        tot += (hi - lo + 1) * 2.0 ** -(2 * k + 1)
        k += 1
    return tot


# literal classes of the enumeration: n + 1 in a block, behaving as the representative value
LIT_CLASSES = []          # (label, representative n, mass)
for _n in range(10):
    LIT_CLASSES.append(('%d' % _n, _n, elias(_n)))
for _lo, _hi, _rep in ((11, 15, 12), (16, 31, 23), (32, 63, 47), (64, 127, 95), (128, 255, 191), (256, 511, 383),
                       (512, 1023, 767)):
    LIT_CLASSES.append(('[%d,%d]' % (_lo - 1, _hi - 1), _rep, elias_range(_lo, _hi)))
LIT_CLASSES.append(('>=1023', 1500, 1.0 - sum(c[2] for c in LIT_CLASSES)))
assert abs(sum(c[2] for c in LIT_CLASSES) - 1.0) < 1e-12


# ====================================================================== term masses (exact literals)
def node_count(t):
    tag = t[0]
    if tag in ('v', 'nat', 'con', 'lib', 'readn', 'readp', 'oos'):
        return 1
    if tag == 'quote' or tag in ('lam', 'fst', 'snd', 'fix', 'libsrc'):
        return 1 + node_count(t[1])
    if tag == 'sim':
        return 1 + node_count(t[2])
    if tag == 'op':
        return 1 + node_count(t[2]) + node_count(t[3])
    return 1 + sum(node_count(c) for c in t[1:])


def term_mass(t, mach):
    """prior mass of the term t (literals exact) under the machine."""
    pt = 1.0 / mach.T
    tag = t[0]
    if tag == 'v':
        return pt * elias(t[1])
    if tag == 'nat':
        return pt * elias(t[1])
    if tag == 'con':
        return pt / 5
    if tag == 'lib':
        return pt / NLIB
    if tag in ('readn', 'readp'):
        return pt
    if tag == 'op':
        return pt / 7 * term_mass(t[2], mach) * term_mass(t[3], mach)
    if tag == 'sim':
        return pt * elias(t[1]) * term_mass(t[2], mach)
    m = pt
    for c in t[1:]:
        m *= term_mass(c, mach)
    return m


def mass_formula(t, mach):
    """code-length formula, written independently of term_mass: a sum of bits over nodes (log2 T per node tag, Elias bits
    per index or literal, log2 5 / log2 7 / log2 NLIB for con / op / lib), mass = 2^-bits."""
    bits = 0.0
    stack = [t]
    while stack:
        u = stack.pop()
        tag = u[0]
        bits += math.log2(mach.T)
        if tag in ('v', 'nat'):
            bits += 2 * math.floor(math.log2(u[1] + 1)) + 1
        elif tag == 'con':
            bits += math.log2(5)
        elif tag == 'lib':
            bits += math.log2(NLIB)
        elif tag == 'op':
            bits += math.log2(7); stack.extend([u[2], u[3]])
        elif tag == 'sim':
            bits += 2 * math.floor(math.log2(u[1] + 1)) + 1; stack.append(u[2])
        elif tag in ('readn', 'readp'):
            pass
        else:
            stack.extend(u[1:])
    return 2.0 ** -bits


# ====================================================================== macros and frames
def expand(t, d=0):
    """expand R1's readn / readp at binder depth d (inside d local lambdas of the body); 'oos' (an out-of-scope index of
    the enumerator) becomes a stuck term."""
    tag = t[0]
    if tag == 'readn':
        return ('capk', ('nat', 400), ('run', ('nat', 400), ('v', d + 1), ('v', d)), ('v', d + 2))
    if tag == 'readp':
        return ('capk', ('nat', 400), ('run', ('nat', 400), ('v', d), ('v', d + 2)), ('v', d + 1))
    if tag == 'oos':
        return ('fst', ('nat', 0))
    if tag in ('v', 'nat', 'con', 'lib'):
        return t
    if tag in ('lam', 'fix'):
        return (tag, expand(t[1], d + 1))
    if tag == 'quote':
        return ('quote', expand_q(t[1], d))
    if tag == 'sim':
        return ('sim', t[1], expand(t[2], d))
    if tag == 'op':
        return ('op', t[1], expand(t[2], d), expand(t[3], d))
    return (tag,) + tuple(expand(c, d) for c in t[1:])


def expand_q(t, d):
    """inside a quote: data; out-of-scope indices stay as indices."""
    tag = t[0]
    if tag == 'oos':
        return ('v', 100000)
    if tag in ('readn', 'readp'):
        return expand(t, d)
    if tag in ('v', 'nat', 'con', 'lib'):
        return t
    if tag in ('lam', 'fix'):
        return (tag, expand_q(t[1], d + 1))
    if tag == 'quote':
        return ('quote', expand_q(t[1], d))
    if tag == 'sim':
        return ('sim', t[1], expand_q(t[2], d))
    if tag == 'op':
        return ('op', t[1], expand_q(t[2], d), expand_q(t[3], d))
    return (tag,) + tuple(expand_q(c, d) for c in t[1:])


def frame(body):
    return ('lam', ('lam', ('lam', body)))


def to_sexpr(t):
    tag = t[0]
    if tag in ('v', 'nat', 'lib'):
        return '%s%d' % ({'v': '#', 'nat': '', 'lib': 'lib'}[tag], t[1])
    if tag == 'con':
        return t[1]
    if tag in ('readn', 'readp', 'oos'):
        return tag
    if tag == 'op':
        return '(%s %s %s)' % (t[1], to_sexpr(t[2]), to_sexpr(t[3]))
    if tag == 'sim':
        return '(sim %d %s)' % (t[1], to_sexpr(t[2]))
    return '(%s %s)' % (tag, ' '.join(to_sexpr(c) for c in t[1:]))


# ====================================================================== evaluator with taint
_T = {'on': False, 'n': None, 'p': None, 'hn': False, 'hp': False}


def _mark(t):
    if _T['on']:
        if t is _T['n']:
            _T['hn'] = True
        elif t is _T['p']:
            _T['hp'] = True


_orig = dict(compile_term=L.compile_term, fst=L.Q.fst, snd=L.Q.snd, canon=L.Q.canon, eq=L.Q.__eq__,
             rt_to_tval=L.rt_to_tval, enter_sim=L.enter_sim)


def _ct(t, _depth=0):
    if _T['on']:
        _mark(t)
    return _orig['compile_term'](t, _depth)


def _q_fst(self):
    if _T['on']: _mark(self.t)
    return _orig['fst'](self)


def _q_snd(self):
    if _T['on']: _mark(self.t)
    return _orig['snd'](self)


def _q_canon(self):
    if _T['on']: _mark(self.t)
    return _orig['canon'](self)


def _q_eq(self, o):
    if _T['on']:
        _mark(self.t)
        if isinstance(o, L.Q): _mark(o.t)
    return _orig['eq'](self, o)


def _rt_to_tval(v):
    if _T['on'] and type(v) is L.Q: _mark(v.t)
    return _orig['rt_to_tval'](v)


def _enter_sim(k, thunk, key=None):
    if _T['on'] and key is not None:
        for e in key:
            if isinstance(e, tuple): _mark(e)
    return TP._counted_enter_sim_inner(k, thunk, key)


def install():
    """patch lt_code once: the failed-read counter of tplus (installed on import) wrapped by the taint tracker."""
    if getattr(L, '_lt_prior_installed', False):
        return
    TP._counted_enter_sim_inner = TP._counted_enter_sim
    L.compile_term = _ct
    L.Q.fst = _q_fst; L.Q.snd = _q_snd; L.Q.canon = _q_canon; L.Q.__eq__ = _q_eq
    L.Q.__hash__ = lambda self: hash(self.canon())
    L.rt_to_tval = _rt_to_tval
    L.enter_sim = _enter_sim
    L._lt_prior_installed = True


install()


def _fresh(t):
    return (t[0],) + t[1:]            # a new tuple object, equal in value


def eval_prog(prog, b, c, taint=False):
    """prog: closed program term lam lam lam body; b, c partner programs (closed terms).  Returns (code 0-8, failed reads,
    forfeit, steps, raw value, hit) with hit = (inspected next's source, inspected prev's source) in taint mode."""
    TP._COUNT[0] = 0
    if taint:
        nb, pc = _fresh(b), _fresh(c)
        _T['on'] = True; _T['n'] = nb; _T['p'] = pc; _T['hn'] = False; _T['hp'] = False
        try:
            v, st = L.evaluate(TP.init3(prog, nb, pc), CT.KR)
        finally:
            _T['on'] = False
        hit = (_T['hn'], _T['hp'])
        _T['n'] = _T['p'] = None
    else:
        v, st = L.evaluate(TP.init3(prog, b, c), CT.KR)
        hit = None
    ok = isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 8
    return (int(v) if ok else CT.NULL), int(TP._COUNT[0]), (0 if ok else 1), int(st), v, hit


# ====================================================================== probes and member signatures
class Probes:
    """The probe partners: the 27 library programs and the two bullies (29 programs; the junk programs are members, not
    partners).  Tables of a program: (code, nto, fo) over (b, c) in 29 x 29."""

    def __init__(self):
        cat = TP.Catalogue()
        self.cat = cat
        self.names = cat.names[:29]
        self.terms = cat.terms[:29]
        self.n = 29
        self.members = cat.names                   # 31 T+ members
        self.mterm = cat.terms
        self.mfam = cat.fam
        self.sig2member = {}
        for i, term in enumerate(cat.terms):
            sig = self.signature(self.table(term))
            self.sig2member.setdefault(sig, []).append(i)

    def table(self, prog, n_limit=None):
        n = self.n
        code = np.empty((n, n), np.int8); nto = np.empty((n, n), np.int8); fo = np.empty((n, n), np.int8)
        for b in range(n):
            for c in range(n):
                cd, nt, f, _, _, _ = eval_prog(prog, self.terms[b], self.terms[c])
                code[b, c] = cd; nto[b, c] = min(nt, 100); fo[b, c] = f
        return code, nto, fo

    def table_adaptive(self, prog, first):
        """the same table as `table`, computed with fewer evaluations by the taint rule: a run that never inspects partner
        p's source is the same for every c (and likewise n / b).  `first` = the taint flags (hn, hp) of the run at
        (C0, C0).  Returns (table, number of evaluations)."""
        n = self.n
        code = np.empty((n, n), np.int8); nto = np.empty((n, n), np.int8); fo = np.empty((n, n), np.int8)
        ne = 0
        T = self.terms

        def put(b, c, r):
            code[b, c] = r[0]; nto[b, c] = min(r[1], 100); fo[b, c] = r[2]
        hn, hp = first
        if not hp:
            for b in range(n):
                r = eval_prog(prog, T[b], T[0], taint=True); ne += 1
                if not r[5][1]:
                    for c in range(n):
                        put(b, c, r)
                else:
                    for c in range(n):
                        put(b, c, eval_prog(prog, T[b], T[c])); ne += 1
        elif not hn:
            for c in range(n):
                r = eval_prog(prog, T[0], T[c], taint=True); ne += 1
                if not r[5][0]:
                    for b in range(n):
                        put(b, c, r)
                else:
                    for b in range(n):
                        put(b, c, eval_prog(prog, T[b], T[c])); ne += 1
        else:
            for b in range(n):
                for c in range(n):
                    put(b, c, eval_prog(prog, T[b], T[c])); ne += 1
        return (code, nto, fo), ne

    @staticmethod
    def signature(tab):
        return b''.join(a.tobytes() for a in tab)


PR = [None]


def probes():
    if PR[0] is None:
        PR[0] = Probes()
    return PR[0]


def const_names():
    return ['C%d' % a for a in range(9)]


# ====================================================================== static junk (sure-reached strict spine)
_BADK = {'nat': ('con', 'quote', 'lam', 'fix', 'pair', 'lib'),
         }


def _kind(t):
    tag = t[0]
    if tag == 'con':
        return 'con:' + t[1]
    if tag == 'op':
        return 'bool' if t[1] in ('le', 'lt') else 'nat'
    if tag == 'eq':
        return 'bool'
    return tag


_NOT_FN = ('nat', 'con', 'quote', 'pair')          # cannot be applied
_NOT_BOOL = ('nat', 'quote', 'lam', 'fix', 'pair', 'lib', 'con:C', 'con:D', 'con:TO')
_NOT_PAIR = ('nat', 'con:C', 'con:D', 'con:T', 'con:F', 'con:TO', 'lam', 'fix', 'lib', 'bool')
_NOT_NAT = ('con:C', 'con:D', 'con:T', 'con:F', 'con:TO', 'quote', 'lam', 'fix', 'pair', 'lib', 'bool')
_NOT_Q = ('nat', 'con:C', 'con:D', 'con:T', 'con:F', 'con:TO', 'pair', 'lam', 'fix', 'lib', 'bool')


def static_stuck(t):
    """True if the sure-reached strict spine of t certainly gets stuck (so the root forfeits): an ill-kinded child of a
    node evaluated for sure.  Conservative (False when unsure)."""
    tag = t[0]
    if tag == 'oos':
        return True
    if tag == 'app':
        if _kind(t[1]) in _NOT_FN or _kind(t[1]) in ('bool', 'nat'):
            return True
        return static_stuck(t[1]) or static_stuck(t[2])
    if tag == 'if':
        if _kind(t[1]) in _NOT_BOOL:
            return True
        return static_stuck(t[1])
    if tag in ('fst', 'snd'):
        if _kind(t[1]) in _NOT_PAIR:
            return True
        return static_stuck(t[1])
    if tag == 'op':
        o = t[1]
        for x in (t[2], t[3]):
            if _kind(x) in _NOT_NAT:
                return True
        if o in ('div', 'mod') and t[3] == ('nat', 0) and t[2][0] == 'nat':
            return True
        return static_stuck(t[2]) or static_stuck(t[3])
    if tag == 'eq':
        return static_stuck(t[1]) or static_stuck(t[2])
    if tag == 'pair':
        return static_stuck(t[1]) or static_stuck(t[2])
    if tag == 'capk':
        if _kind(t[1]) in _NOT_NAT:
            return True
        return static_stuck(t[1]) or static_stuck(t[2]) or static_stuck(t[3])
    if tag == 'run':
        if _kind(t[1]) in _NOT_NAT or _kind(t[2]) in _NOT_Q or _kind(t[3]) in _NOT_Q:
            return True
        return static_stuck(t[1]) or static_stuck(t[2]) or static_stuck(t[3])
    return False


_ROOT_NOT_CODE = ('con', 'quote', 'lam', 'fix', 'pair', 'eq')


def static_junk(t):
    """True if the root certainly forfeits without evaluating: the root is a value that is not a number (con, quote, lam,
    fix, pair, lib), a boolean (eq, le, lt), or its strict spine gets stuck."""
    tag = t[0]
    if tag in ('con', 'quote', 'lam', 'fix', 'pair', 'eq', 'lib', 'libsrc'):
        return True
    if tag == 'op' and t[1] in ('le', 'lt'):
        return True
    return static_stuck(t)


# ====================================================================== the classifier
def _const_cls(code, nto, fo):
    if fo:
        return ('junk_f', '')
    if nto > 0:
        return ('junk_r', '') if code == 8 else ('const_read:%d' % code, '')
    return ('const:%d' % code, '')


def _lab_single(R, d):
    """family label of a single-partner response map R on constants (9 codes).  d: 'n' or 'p'."""
    if d == 'n':
        a_name, a_go, f_set = 3, 4, (4, 8)
        acc, go = 4, 1
        bul, bul_hi, bul_lo = 3, 2, 4
        yld, yld_to = 5, 0
        ex1, ex1o, ex2, ex2o = 3, 2, 4, 1
    else:
        acc, go = 1, 4
        bul, bul_hi, bul_lo = 0, 5, 1
        yld, yld_to = 2, 3
        ex1, ex1o, ex2, ex2o = 0, 5, 1, 4
    rest = [R[a] for a in range(9) if a != acc]
    if R[acc] == go and len(set(rest)) == 1 and rest[0] in ((4, 8) if d == 'n' else (1, 8)):
        return 'single_fair:' + d
    if R[ex1] == ex1o and R[ex2] == ex2o and all(R[a] == 8 for a in range(9) if a not in (ex1, ex2)):
        return 'exploit:' + d
    if R[bul] == bul_hi and all(R[a] == bul_lo for a in range(9) if a != bul):
        return 'bully:' + d
    if R[yld] == yld_to:
        return 'yielder:' + d
    return 'other_cond'


def _lab_two(M):
    """M[a, b] = output with next = C_a, prev = C_b on the constants.  Library two-partner readers: first n: 1 if a == 4,
    else 4 if b == 1, else f in (1, 8); first p: 4 if b == 1, else 1 if a == 4, else f in (4, 8)."""
    for first in 'np':
        for f in ((1, 8) if first == 'n' else (4, 8)):
            ok = True
            for a in range(9):
                for b in range(9):
                    if first == 'n':
                        e = 1 if a == 4 else (4 if b == 1 else f)
                    else:
                        e = 4 if b == 1 else (1 if a == 4 else f)
                    if M[a, b] != e:
                        ok = False; break
                if not ok:
                    break
            if ok:
                return 'two_fair:' + first
    return 'other_cond'


def classify_table(tab, pr):
    """(family label, exact member name or '') from a full probe table (code, nto, fo)."""
    code, nto, fo = tab
    sig = pr.signature(tab)
    mem = pr.sig2member.get(sig)
    exact = ''
    if mem:
        exact = pr.members[mem[0]]
    ci = [pr.names.index('C%d' % a) for a in range(9)]
    dep_b = bool((code != code[:1, :]).any() or (nto != nto[:1, :]).any() or (fo != fo[:1, :]).any())
    dep_c = bool((code != code[:, :1]).any() or (nto != nto[:, :1]).any() or (fo != fo[:, :1]).any())
    code_dep = bool((code != code[0, 0]).any())
    if not dep_b and not dep_c:
        fam, _ = _const_cls(int(code[0, 0]), int(nto[0, 0]), int(fo[0, 0]))
        return fam, exact
    if not code_dep:
        # constant output, charge varies with the partners: a constant that reads
        return 'const_read:%d' % int(code[0, 0]), exact
    cb = code[np.ix_(ci, ci)]            # cb[a, b]: next = C_a, prev = C_b
    # does the response on the constants depend on b only, c only, or both?
    dn = bool((cb != cb[:, :1]).any())   # varies with prev
    dp = bool((cb != cb[:1, :]).any())   # varies with next
    if dp and not dn:
        return _lab_single([int(cb[a, 0]) for a in range(9)], 'n'), exact
    if dn and not dp:
        return _lab_single([int(cb[0, b]) for b in range(9)], 'p'), exact
    if dn and dp:
        return _lab_two(cb), exact
    return 'other_cond', exact           # responds only to non-constant partners (source or behaviour)


def classify_body(body, mach, pr=None, taint=True):
    """classify the term `body` (a body of the arm-T frame).  Returns (family label, exact member name, n_evals)."""
    pr = pr or probes()
    if static_junk(body):
        return 'junk_f', '', 0
    term = expand(body) if mach.name == 'R1' else expand(body)     # 'oos' leaves become stuck terms in both
    prog = frame(term)
    c0 = pr.terms[0]
    cd, nt, f, st, raw, hit = eval_prog(prog, c0, c0, taint=True)
    if not (hit[0] or hit[1]):
        fam, _ = _const_cls(cd, nt, f)
        return fam, '', 1
    tab, ne = pr.table_adaptive(prog, hit)
    fam, exact = classify_table(tab, pr)
    return fam, exact, 1 + ne


FAMILY_GROUPS = {
    'const': lambda f: f.startswith('const:'),
    'junk_f': lambda f: f == 'junk_f',
    'junk_r': lambda f: f == 'junk_r',
    'const_read': lambda f: f.startswith('const_read:'),
    'single': lambda f: f.startswith('single_fair'),
    'two': lambda f: f.startswith('two_fair'),
    'bully': lambda f: f.startswith('bully'),
    'exploit': lambda f: f.startswith('exploit'),
    'yielder': lambda f: f.startswith('yielder'),
    'other_cond': lambda f: f == 'other_cond',
}


def group_of(fam):
    for g, fn in FAMILY_GROUPS.items():
        if fn(fam):
            return g
    return 'other'
