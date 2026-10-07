"""The realizable language, milestone 2: populations of carriers (specs/2026-10-06-carrier-populations.md;
notes/carrier-populations.md; predictions/2026-10-06-carrier-populations.md).

Built on src/lt_cert.py and src/lt_code.py (imported, not modified).

Parts:
  1. the template grammar (two sorts, check atoms, node counting), enumeration, compilation to L_T^code carriers;
  2. run trees dt(x) and tau-types (dt, list) (notes §1.3, Lemma T);
  3. production (milestone 4's frozen tactic; P, O, E);
  4. the catalogue: spellings, tau-types, representatives, prior masses;
  5. check values: ideal (host replay, no step cost) and executable (the checker term at K), and composition of plays;
  6. lumping (rows and columns against every spelling, self and cross-twin cells included) and class tables.
"""
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C

T_, F_ = L.T_, L.F_
QC = ('quote', L.PROG_C)
QD = ('quote', L.PROG_D)
ROLE = {'me': C.ME3, 'them': C.THEM3, 'C': QC, 'D': QD}
PD_PAY = {('C', 'C'): 0.0, ('C', 'D'): -2.0, ('D', 'C'): 1.0, ('D', 'D'): -1.0}
MODE_OF_ENTRY = {0: 0, 5: 5}


# ----------------------------------------------------------------------------------------------------------------
# 1. Grammar
# ----------------------------------------------------------------------------------------------------------------
def atom_alphabet(entries=(0,)):
    return [(e, p, q, a) for e in entries for p in ('them', 'me') for q in ('me', 'them', 'C', 'D') for a in ('C', 'D')]


def enumerate_grammar(nmax, entries=(0,)):
    """All actions with <= nmax nodes.  Conditions: ('A', atom) | ('not', B) | ('and', B, B) | ('or', B, B);
    actions: ('C',) | ('D',) | ('if', B, A, A).  Returns {n: [actions with exactly n nodes]}."""
    atoms = atom_alphabet(entries)
    B, A = {}, {}
    for n in range(1, nmax + 1):
        if n == 1:
            B[n] = [('A', x) for x in atoms]
            continue
        out = [('not', b) for b in B[n - 1]]
        for i in range(1, n - 1):
            for b1 in B[i]:
                for b2 in B[n - 1 - i]:
                    out.append(('and', b1, b2)); out.append(('or', b1, b2))
        B[n] = out
    for n in range(1, nmax + 1):
        if n == 1:
            A[n] = [('C',), ('D',)]
            continue
        out = []
        for i in range(1, n):
            for j in range(1, n):
                k = n - 1 - i - j
                if k < 1: continue
                for b in B[i]:
                    for x in A[j]:
                        for y in A[k]:
                            out.append(('if', b, x, y))
        A[n] = out
    return A


def count_by_hand(nmax, k):
    """The recurrences of notes §1.1."""
    b = {1: k}
    for n in range(2, nmax + 1):
        b[n] = b[n - 1] + 2 * sum(b[i] * b[n - 1 - i] for i in range(1, n - 1))
    a = {1: 2}
    for n in range(2, nmax + 1):
        a[n] = sum(b[i] * a[j] * a[n - 1 - i - j] for i in range(1, n) for j in range(1, n) if n - 1 - i - j >= 1)
    return a


def nodes(x):
    t = x[0]
    if t in ('C', 'D'): return 1
    if t == 'A': return 1
    if t == 'not': return 1 + nodes(x[1])
    if t in ('and', 'or'): return 1 + nodes(x[1]) + nodes(x[2])
    return 1 + nodes(x[1]) + nodes(x[2]) + nodes(x[3])


def atoms_of(x):
    t = x[0]
    if t in ('C', 'D'): return []
    if t == 'A': return [x[1]]
    return [a for c in x[1:] for a in atoms_of(c)]


def show_atom(at):
    e, p, q, a = at
    qn = {'me': 'me', 'them': 'them', 'C': '^C', 'D': '^D'}[q]
    return 'CHK%s(%s,%s,%s)' % ('' if e == 0 else '_5', p, qn, a)


def show(x):
    t = x[0]
    if t in ('C', 'D'): return t
    if t == 'A': return show_atom(x[1])
    if t == 'not': return 'not(%s)' % show(x[1])
    if t in ('and', 'or'): return '%s(%s,%s)' % (t, show(x[1]), show(x[2]))
    return 'if(%s,%s,%s)' % (show(x[1]), show(x[2]), show(x[3]))


# ----------------------------------------------------------------------------------------------------------------
# 2. Run trees
# ----------------------------------------------------------------------------------------------------------------
def _bt(b, t, f):
    if b[0] == 'A': return (b[1], t, f)
    if b[0] == 'not': return _bt(b[1], f, t)
    if b[0] == 'and': return _bt(b[1], _bt(b[2], t, f), f)
    return _bt(b[1], t, _bt(b[2], t, f))


def dt(x):
    """The run tree: the order and branching of the check calls the compiled run makes (notes §1.3)."""
    if x[0] in ('C', 'D'): return x[0]
    return _bt(x[1], dt(x[2]), dt(x[3]))


def dt_atoms(t):
    if isinstance(t, str): return set()
    return {t[0]} | dt_atoms(t[1]) | dt_atoms(t[2])


def show_dt(t):
    if isinstance(t, str): return t
    return '%s?%s:%s' % (show_atom(t[0]), show_dt(t[1]), show_dt(t[2]))


def s_guarded(t):
    """Every root-to-C-leaf path passes the T-branch of an S_C atom (them, me, C) (notes §1.7, Lemma G)."""
    def rec(t, ok):
        if isinstance(t, str): return ok if t == 'C' else True
        e, p, q, a = t[0]
        s = (p == 'them' and q == 'me' and a == 'C')
        return rec(t[1], ok or s) and rec(t[2], ok)
    return rec(t, False)


# ----------------------------------------------------------------------------------------------------------------
# 3. Compilation and production
# ----------------------------------------------------------------------------------------------------------------
def bterm(b, V, K):
    if b[0] == 'A':
        e, p, q, a = b[1]
        return C.CALL(MODE_OF_ENTRY[e], V, ROLE[p], ROLE[q], a, K)
    if b[0] == 'not': return ('if', bterm(b[1], V, K), F_, T_)
    if b[0] == 'and': return ('if', bterm(b[1], V, K), bterm(b[2], V, K), F_)
    return ('if', bterm(b[1], V, K), T_, bterm(b[2], V, K))


def body_term(x, V, K):
    if x[0] == 'C': return L.C_
    if x[0] == 'D': return L.D_
    return ('if', bterm(x[1], V, K), body_term(x[2], V, K), body_term(x[3], V, K))


def program(x, certs, V, K):
    return C.carrier(body_term(x, V, K), certs)


def make_probes(prod, mode, K, V):
    """Milestone 4's build_arm probe passes for one checker mode: CB, CB1, CBP with their own C and D scripts."""
    mk = lambda bf: (lambda certs: C.carrier(bf(mode, V, K), certs))
    probe_d = {nm: prod.produce(mode, mk(C.CARRIER_BODIES[nm])(0), L.PROG_D, 'D', K, V) for nm in ('CB', 'CB1', 'CBP')}
    probes0 = [(nm, mk(C.CARRIER_BODIES[nm])(C.cons([('D', probe_d[nm])] if probe_d[nm] else []))) for nm in ('CB', 'CB1', 'CBP')]
    probes = []
    for nm in ('CB', 'CB1', 'CBP'):
        lst, _ = C.produce_list(prod, mode, mk(C.CARRIER_BODIES[nm]), probes0, K, V)
        probes.append((nm, mk(C.CARRIER_BODIES[nm])(lst)))
    return probes


def produce_multi(prod, modes, mkprog, probes_by_mode, K, V):
    """produce_list generalized to several checker modes (E): D scripts (empty list, each mode, distinct), then C
    scripts against each mode's probes (the program carrying its D scripts), distinct, in mode order."""
    dl = []
    for md in modes:
        s = prod.produce(md, mkprog(0), L.PROG_D, 'D', K, V)
        if s is not None and s not in dl: dl.append(s)
    p1 = mkprog(C.cons([('D', s) for s in dl]))
    cs = []
    for md in modes:
        for pname, pr in probes_by_mode[md]:
            s = prod.produce(md, p1, pr, 'C', K, V)
            if s is not None and s not in cs: cs.append(s)
    return C.cons([('C', s) for s in cs] + [('D', s) for s in dl])


# ----------------------------------------------------------------------------------------------------------------
# 4. The catalogue
# ----------------------------------------------------------------------------------------------------------------
class Catalogue:
    """arm: 'P' (lists free), 'O' (none | produced), 'E' (entries 0 and 5, lists free).  Spellings are distinct
    terms; under O a spelling whose produced list is empty is one program reached by two derivations (its weight is
    the sum)."""

    def __init__(self, nmax=7, arm='P', K=10 ** 6, verbose=False):
        self.nmax, self.arm, self.K = nmax, arm, K
        self.V = V = K // 4
        entries = (0, 5) if arm == 'E' else (0,)
        modes = [MODE_OF_ENTRY[e] for e in entries]
        G = enumerate_grammar(nmax, entries)
        self.sexprs = [x for n in range(1, nmax + 1) for x in G[n]]
        prod = C.Producer(host=ExactHost())
        self.prod = prod
        probes_by_mode = {md: make_probes(prod, md, K, V) for md in modes}
        self.probes = probes_by_mode
        lists = []
        for x in self.sexprs:
            body = body_term(x, V, K)
            mkp = lambda c, body=body: C.carrier(body, c)
            if arm == 'E':
                lst = produce_multi(prod, modes, mkp, probes_by_mode, K, V)
            else:
                lst, _ = C.produce_list(prod, 0, mkp, probes_by_mode[0], K, V)
            lists.append(lst)
        self.produced = lists
        # spellings: (sexpr index, list choice)
        sp = []
        for i, x in enumerate(self.sexprs):
            nd = nodes(x)
            n5 = sum(1 for at in atoms_of(x) if at[0] == 5)
            na = len(atoms_of(x))
            if arm == 'O':
                if lists[i] == 0:
                    sp.append(dict(i=i, lst=0, choice='both', nodes=nd, n5=n5, na=na, w_bits=nd + 1, mult=2))
                else:
                    sp.append(dict(i=i, lst=0, choice='none', nodes=nd, n5=n5, na=na, w_bits=nd + 1, mult=1))
                    sp.append(dict(i=i, lst=lists[i], choice='produced', nodes=nd, n5=n5, na=na, w_bits=nd + 1, mult=1))
            else:
                sp.append(dict(i=i, lst=lists[i], choice='produced', nodes=nd, n5=n5, na=na, w_bits=nd, mult=1))
        self.spell = sp
        self.dts = [dt(x) for x in self.sexprs]
        # tau types
        tau_of = {}
        self.tau = np.zeros(len(sp), np.int64)
        members = []
        for k, s in enumerate(sp):
            key = (self.dts[s['i']], s['lst'])
            t = tau_of.get(key)
            if t is None:
                t = len(members); tau_of[key] = t; members.append([])
            self.tau[k] = t
            members[t].append(k)
        for m in members:
            m.sort(key=lambda k: (sp[k]['nodes'], k))
        self.members = members
        self.T = len(members)
        self.tau_dt = [self.dts[sp[m[0]]['i']] for m in members]
        self.tau_list = [sp[m[0]]['lst'] for m in members]
        self.tau_atoms = [dt_atoms(d) for d in self.tau_dt]
        self._terms = {}
        if verbose:
            print('catalogue %s n<=%d: %d sexprs, %d spellings, %d tau-types' % (arm, nmax, len(self.sexprs), len(sp), self.T), flush=True)

    # -- terms
    def term(self, k):
        t = self._terms.get(k)
        if t is None:
            s = self.spell[k]
            t = program(self.sexprs[s['i']], s['lst'], self.V, self.K)
            self._terms[k] = t
        return t

    def rep(self, t, which=0):
        m = self.members[t]
        return m[min(which, len(m) - 1)]

    def name(self, k):
        s = self.spell[k]
        nm = show(self.sexprs[s['i']])
        if self.arm == 'O' and s['choice'] == 'none': nm += '[none]'
        return nm

    def has_entry(self, t, a):
        lst = self.tau_list[t]
        return lst != 0 and any(e[0] == a for e in C.uncons(lst))

    # -- prior masses (unnormalized, per spelling)
    def spelling_mass(self, prior):
        w = np.zeros(len(self.spell))
        for k, s in enumerate(self.spell):
            n = s['w_bits']
            if prior == 'L':
                w[k] = s['mult'] * 2.0 ** (-(n + (s['n5'] if self.arm == 'E' else 0)))
            elif prior == 'Leq':
                w[k] = s['mult'] * 2.0 ** (-(n + s['na']))
            elif prior == 'Lstd':
                w[k] = s['mult'] * 2.0 ** (-n)    # replaced below
            else:
                raise ValueError(prior)
        if prior == 'Lstd':
            # Elias-gamma length prior of dsl.py: uniform within a node count, 1 / (2 |p|^2) per length (bits counted
            # on the grammar's nodes; the O choice node and the E label count as one extra node, as under L)
            cnt = defaultdict(float)
            ln = [s['w_bits'] + (s['n5'] if self.arm == 'E' else 0) for s in self.spell]
            for k, s in enumerate(self.spell): cnt[ln[k]] += s['mult']
            for k, s in enumerate(self.spell):
                w[k] = s['mult'] / (2.0 * ln[k] ** 2) / cnt[ln[k]]
        return w / w.sum()


# ----------------------------------------------------------------------------------------------------------------
# 5. Check values and composition
# ----------------------------------------------------------------------------------------------------------------
class ExactHost(C.HostCheck):
    """milestone 4's host replay checker with an exact memo.  HostCheck memoizes the *clean* value of every check and
    returns it when the same check recurs nested inside another; but in context a nested check whose clean run
    called (transitively) a key now on the stack, or whose clean value is TO, does not return its clean value: its
    run reaches that call and regresses, which kills the root (Lemma N; the regress lemma).  ExactHost records the
    keys every memoized check called and raises the regress in exactly those cases, so its values are independent
    of the order in which checks are computed (found in validation: notes §1.10)."""

    def __init__(self):
        super().__init__()
        self.deps = {}
        self.dstack = []

    def clear(self):
        self.memo.clear(); self.deps.clear()

    def check(self, n, v):
        key = (n, v)
        if key in self.memo:
            res = self.memo[key]
            if self.stack:
                if res == 'TO': raise C.Regress()
                d = self.deps[key]
                if d and not d.isdisjoint(self.stack): raise C.Regress()
                self.dstack[-1] |= d; self.dstack[-1].add(key)
            return res
        if key in self.stack: raise C.Regress()
        self.stack.append(key); self.dstack.append(set())
        self.maxdepth = max(self.maxdepth, len(self.stack))
        try:
            res = self._ccore(C.WRAP_MODE[n], v)
        except C.HostAbort:
            self.stack.pop(); self.dstack.pop()
            if self.stack: raise
            self.memo[key] = 'TO'; self.deps[key] = set()
            return 'TO'
        self.stack.pop(); d = self.dstack.pop()
        self.memo[key] = res; self.deps[key] = d
        if self.dstack:
            self.dstack[-1] |= d; self.dstack[-1].add(key)
        return res


class IdealCheck(ExactHost):
    """The host replay checker with no step cost (EvR* unbounded): the matched ideal-verification control."""

    def cchk(self, mode, Rb, Sb, V, nd, Lf, Rf):
        try:
            rule, (j, ps) = nd
            ps = C.uncons(ps)
        except Exception:
            return 0
        if rule == C.EVS:
            x = Rf[j] if isinstance(j, int) and 0 <= j < len(Rf) else None
            if x is None or x[0] != 'atom' or not ps: return 0
            s = C.h_evstar(x, None)
            if s is None: return 0
            return self.cchk(mode, Rb, Sb, V, ps[0], Lf, C.fadd(s[0], C.fdel(x, Rf)))
        return ExactHost.cchk(self, mode, Rb, Sb, V, nd, Lf, Rf)


class Checker:
    """Clean check values chk_a^mode(t, m): 'ideal' (IdealCheck) or 'exec' (the checker term at K).  Returns
    (value in {'T','F','TO'}, inner steps or None)."""

    def __init__(self, kind, V, K, memo_cap=300000):
        self.kind, self.V, self.K = kind, V, K
        self.host = IdealCheck() if kind == 'ideal' else None
        self.memo_cap = memo_cap
        self.n = 0

    def __call__(self, mode, t, m, a):
        self.n += 1
        if self.kind == 'ideal':
            if len(self.host.memo) > self.memo_cap:
                self.host.clear()
            v = self.host.check(C.ID[C.MODE_WRAP[mode]], C.mk_arg(self.V, t, m, a, self.K))
            return v, None
        if len(L.CACHE) > self.memo_cap:
            L.CACHE.clear()
        res, total = C.check_value(mode, self.V, t, m, a, self.K)
        return res, total - 1


def eval_dt(t, val):
    """Evaluate a run tree; val(atom) -> bool or a numpy bool array.  Returns 1 for C, 0 for D (array or int)."""
    if isinstance(t, str): return 1 if t == 'C' else 0
    v = val(t[0])
    a, b = eval_dt(t[1], val), eval_dt(t[2], val)
    if isinstance(v, np.ndarray):
        return np.where(v, a, b)
    return a if v else b


def path_atoms(t, val):
    """Atoms actually called along the run (scalar val)."""
    out = []
    while not isinstance(t, str):
        out.append(t[0])
        t = t[1] if val(t[0]) else t[2]
    return out


def needed_pairs(atoms_by_unit, n_units):
    """For each (mode, a): the asker units for S (them, me) and R (me, them) atoms."""
    S, R = defaultdict(list), defaultdict(list)
    for u in range(n_units):
        for (e, p, q, a) in atoms_by_unit[u]:
            md = MODE_OF_ENTRY[e]
            if p == 'them' and q == 'me': S[(md, a)].append(u)
            if p == 'me' and q == 'them': R[(md, a)].append(u)
    return {k: sorted(set(v)) for k, v in S.items()}, {k: sorted(set(v)) for k, v in R.items()}


def unit_values(units_terms, atoms_by_unit, has_entry, checker, needed_self=True):
    """Per-unit (tau-type or class) self-type values: chk(x, x), chk(x, ^C), chk(x, ^D) for every (mode, a) asked by
    anyone about anyone (them/me atoms on self, ^C, ^D).  units_terms[u] = term of u's representative spelling."""
    n = len(units_terms)
    keys = set()
    for u in range(n):
        for (e, p, q, a) in atoms_by_unit[u]:
            if q in ('me', 'them') and p == q: keys.add(('self', MODE_OF_ENTRY[e], a))
            if q in ('C', 'D'): keys.add((q, MODE_OF_ENTRY[e], a))
            if (p, q) in (('them', 'me'), ('me', 'them')): keys.add(('self', MODE_OF_ENTRY[e], a))   # self-play
    out = {}
    for kind, md, a in keys:
        arr = np.zeros(n, np.int8); st = np.full(n, -1, np.int64); raw = [None] * n
        for u in range(n):
            if not has_entry(u, a):
                arr[u] = 0; raw[u] = 'F0'
                continue
            t = units_terms[u]
            m = t if kind == 'self' else (L.PROG_C if kind == 'C' else L.PROG_D)
            v, s = checker(md, t, m, a)
            arr[u] = 1 if v == 'T' else 0; raw[u] = v
            if s is not None: st[u] = s
        out[(kind, md, a)] = dict(val=arr, steps=st, raw=raw)
    return out


def pair_matrix_entries(S, R, n_units, has_entry):
    """The (t, m) entries of chk_a^md(t, m) that some unit asks: S askers m ask chk(y, m) for every y (target y);
    R askers x ask chk(x, y) for every y.  Returns {(md, a): set of (t, m)} restricted to targets with an a-entry
    (the others are F by the code's empty-selection branch)."""
    need = defaultdict(set)
    for (md, a), us in S.items():
        tg = [t for t in range(n_units) if has_entry(t, a)]
        for m in us:
            for t in tg: need[(md, a)].add((t, m))
    for (md, a), us in R.items():
        for x in us:
            if not has_entry(x, a): continue
            for m in range(n_units): need[(md, a)].add((x, m))
    return need


def compose_row(x, units_dt, CH, UV, n_units):
    """Actions of unit x against every unit y (x != y uses the pair matrices; the diagonal entry is the distinct-
    twin play G(x, x)).  CH[(md, a)] is a dense int8 (n, n) array (t, m); UV the unit values."""
    def val(at):
        e, p, q, a = at
        md = MODE_OF_ENTRY[e]
        if p == 'them' and q == 'me': return CH[(md, a)][:, x].astype(bool)
        if p == 'me' and q == 'them': return CH[(md, a)][x, :].astype(bool)
        if p == 'them' and q == 'them': return UV[('self', md, a)]['val'].astype(bool)
        if p == 'them': return UV[(q, md, a)]['val'].astype(bool)
        if p == 'me' and q == 'me': return np.full(n_units, bool(UV[('self', md, a)]['val'][x]))
        return np.full(n_units, bool(UV[(q, md, a)]['val'][x]))
    r = eval_dt(units_dt[x], val)
    if not isinstance(r, np.ndarray): r = np.full(n_units, r)
    return r.astype(np.int8)


def self_action(x, units_dt, UV):
    def val(at):
        e, p, q, a = at
        md = MODE_OF_ENTRY[e]
        if q in ('me', 'them'): return bool(UV[('self', md, a)]['val'][x])
        return bool(UV[(q, md, a)]['val'][x])
    return eval_dt(units_dt[x], val)


def pay_matrix(A):
    """A[x, y] = 1 if x plays C against y.  U[x, y] = PD payoff of x."""
    a = A.astype(int); b = A.T.astype(int)
    P = np.array([[-1.0, 1.0], [-2.0, 0.0]])     # pay[my level][their level], level D=0, C=1
    return P[a, b], (a * b).astype(float)


# ----------------------------------------------------------------------------------------------------------------
# 6. Lumping
# ----------------------------------------------------------------------------------------------------------------
def lump(cat, A_tau, self_tau, w_spell):
    """Classes of spellings.  A_tau[t1, t2]: action of a spelling of t1 against a *distinct* spelling of t2
    (diagonal = distinct twins); self_tau[t]: against itself.  A type is *split* when it has >= 2 spellings and its
    twin play differs from its self play (as an action pair: the twin pair is symmetric by Lemma T); its spellings
    become singleton classes.  Clean types are merged by equal rows and columns of the type-level payoff matrix with
    the diagonal = self (equivalent to the spelling-level criterion; notes §1.5).  Returns a dict."""
    T = cat.T
    sizes = np.array([len(m) for m in cat.members])
    split = np.array([(sizes[t] >= 2 and A_tau[t, t] != self_tau[t]) for t in range(T)])
    Ad = A_tau.copy()
    Ad[np.arange(T), np.arange(T)] = self_tau
    R = (2 * Ad + Ad.T).astype(np.int8)          # the action pair (PD payoffs are injective in it)
    groups = defaultdict(list)
    for t in range(T):
        if split[t]:
            continue
        groups[(hash(R[t].tobytes()), hash(np.ascontiguousarray(R[:, t]).tobytes()))].append(t)
    # memory-light keys (hashes); every group is verified exactly against its first member, splitting on mismatch
    exact = []
    for ts in groups.values():
        rest = list(ts)
        while rest:
            t0 = rest[0]
            same = [t for t in rest if np.array_equal(R[t], R[t0]) and np.array_equal(R[:, t], R[:, t0])]
            exact.append(same)
            rest = [t for t in rest if t not in set(same)]
    classes = []      # each: dict(types=[...], spellings=[...])
    for ts in exact:
        sp = [k for t in ts for k in cat.members[t]]
        classes.append(dict(types=sorted(ts), spellings=sorted(sp), split=False))
    for t in np.nonzero(split)[0]:
        for k in cat.members[t]:
            classes.append(dict(types=[int(t)], spellings=[k], split=True))
    # class-level action matrix
    nc = len(classes)
    rep_t = np.array([c['types'][0] for c in classes])
    A = Ad[np.ix_(rep_t, rep_t)].copy()
    for i, c in enumerate(classes):
        A[i, i] = self_tau[rep_t[i]]
    # split singletons of the same type: twin play
    by_type = defaultdict(list)
    for i, c in enumerate(classes):
        if c['split']: by_type[c['types'][0]].append(i)
    for t, idx in by_type.items():
        for i in idx:
            for j in idx:
                if i != j: A[i, j] = A_tau[t, t]
    for c in classes:
        c['rep'] = min(c['spellings'], key=lambda k: (cat.spell[k]['nodes'], k))
    mass = np.array([w_spell[c['spellings']].sum() for c in classes])
    order = np.argsort(-mass, kind='stable')
    classes = [classes[i] for i in order]
    A = A[np.ix_(order, order)]
    return dict(classes=classes, A=A, n_split_types=int(split.sum()), n_split_classes=int(sum(1 for c in classes if c['split'])))


def spelling_matrix(cat, A_tau, self_tau, ks):
    """The spelling-level action matrix on a subset of spellings ks (Lemma T expansion)."""
    tau = cat.tau[np.asarray(ks)]
    A = A_tau[np.ix_(tau, tau)].copy()
    for i in range(len(ks)):
        A[i, i] = self_tau[tau[i]]
    return A
