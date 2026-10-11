"""Identity and tags in the carrier grammar: the pooling test (specs/2026-10-10-identity-and-tags.md;
notes/identity-tags.md; predictions/2026-10-10-identity-and-tags.md).

Built on src/lt_code.py, src/lt_cert.py and src/carrier_populations.py (imported, not modified).

Parts:
  1. the extended grammar: check atoms with q in {me, them, ^C, ^D, ^CB}, eq(me, them), tag_t(them); marker sets;
  2. compilation: markers as no-op lets around the body, eq as L_T's eq, tags as a guarded quote walk, ^CB literal;
  3. production with the extended probe list (CB, CB1, CBP, CB^1, CB^2, CB^12, XC);
  4. the catalogue: spellings (body, marker set), tau'-units (dt, M, cb), lists per (dt, M & tags(dt));
  5. checks on reduced keys (Lemma R), unit values, composition of the unit-level action table;
  6. identity-aware lumping;
  7. families: compatibility graph, maximal cliques, components, bridges, labels.
"""
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C
import carrier_populations as CP

T_, F_ = L.T_, L.F_
K_DEF = 10 ** 6
QC = ('quote', L.PROG_C)
QD = ('quote', L.PROG_D)
MARK_BASE = 9000
MSETS = [0, 1, 2, 3]            # marker sets as bitmasks: bit 0 = marker 1, bit 1 = marker 2
MS_NAME = {0: '', 1: '^1', 2: '^2', 3: '^12'}


def mcount(M): return (M & 1) + ((M >> 1) & 1)


# ----------------------------------------------------------------------------------------------------------------
# 1. Grammar
# ----------------------------------------------------------------------------------------------------------------
def atom_alphabet(eq=True, tags=True, cbq=True):
    qs = ('me', 'them', 'C', 'D') + (('CB',) if cbq else ())
    at = [('chk', p, q, a) for p in ('them', 'me') for q in qs for a in ('C', 'D')]
    if eq: at.append(('eq',))
    if tags: at += [('tag', 1), ('tag', 2)]
    return at


def enumerate_grammar(nmax, atoms):
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


nodes = CP.nodes
dt = CP.dt                       # generic in the atom


def atoms_of(x):
    t = x[0]
    if t in ('C', 'D'): return []
    if t == 'A': return [x[1]]
    return [a for c in x[1:] for a in atoms_of(c)]


def dt_atoms(t):
    if isinstance(t, str): return set()
    return {t[0]} | dt_atoms(t[1]) | dt_atoms(t[2])


def tagbits_of(atoms):
    b = 0
    for a in atoms:
        if a[0] == 'tag': b |= (1 << (a[1] - 1))
    return b


def show_atom(at):
    if at[0] == 'eq': return 'eq'
    if at[0] == 'tag': return 'tag%d' % at[1]
    _, p, q, a = at
    qn = {'me': 'me', 'them': 'them', 'C': '^C', 'D': '^D', 'CB': '^CB'}[q]
    return 'CHK(%s,%s,%s)' % (p, qn, a)


def show(x):
    t = x[0]
    if t in ('C', 'D'): return t
    if t == 'A': return show_atom(x[1])
    if t == 'not': return 'not(%s)' % show(x[1])
    if t in ('and', 'or'): return '%s(%s,%s)' % (t, show(x[1]), show(x[2]))
    return 'if(%s,%s,%s)' % (show(x[1]), show(x[2]), show(x[3]))


def show_dt(t):
    if isinstance(t, str): return t
    return '%s?%s:%s' % (show_atom(t[0]), show_dt(t[1]), show_dt(t[2]))


def s_guarded(t):
    """Every root-to-C path passes the T branch of an S atom CHK(them, me, C) (Lemma G)."""
    def rec(t, ok):
        if isinstance(t, str): return ok if t == 'C' else True
        a = t[0]
        s = (a == ('chk', 'them', 'me', 'C'))
        return rec(t[1], ok or s) and rec(t[2], ok)
    return rec(t, False)


# ----------------------------------------------------------------------------------------------------------------
# 2. Compilation
# ----------------------------------------------------------------------------------------------------------------
def _isT(x, tag): return ('eq', ('fst', x), ('nat', L.TAGCODE[tag]))
def _and(c, d): return ('if', c, d, F_)
def _mark(t): return ('quote', ('nat', MARK_BASE + t))


def tag_term(t, them):
    """tag_t(them): a guarded walk of the opponent's quote (carrier shape lam, lam, app(lam B, certs)); T iff the body B
    carries marker t (marker 1 outermost)."""
    x1 = ('snd', them)
    x2 = ('snd', x1)
    x3 = ('fst', ('snd', x2))
    x4 = ('snd', x3)
    argof = lambda q: ('fst', ('snd', ('snd', q)))
    inner = ('snd', ('fst', ('snd', x4)))
    if t == 1:
        test = _and(_isT(x4, 'app'), ('eq', argof(x4), _mark(1)))
    else:
        test = _and(_isT(x4, 'app'),
                    ('if', ('eq', argof(x4), _mark(2)), T_,
                     _and(('eq', argof(x4), _mark(1)),
                          _and(_isT(('fst', ('snd', x4)), 'lam'),
                               _and(_isT(inner, 'app'), ('eq', argof(inner), _mark(2)))))))
    return _and(_isT(them, 'lam'), _and(_isT(x1, 'lam'), _and(_isT(x2, 'app'), _and(_isT(x3, 'lam'), test))))


class Compiler:
    def __init__(self, V, K, cb_term):
        self.V, self.K = V, K
        self.QCB = ('quote', cb_term) if cb_term is not None else None

    def roles(self, off):
        return {'me': ('v', 2 + off), 'them': ('v', 1 + off), 'C': QC, 'D': QD, 'CB': self.QCB}

    def bterm(self, b, R):
        if b[0] == 'A':
            at = b[1]
            if at[0] == 'eq': return ('eq', R['me'], R['them'])
            if at[0] == 'tag': return tag_term(at[1], R['them'])
            _, p, q, a = at
            return C.CALL(0, self.V, R[p], R[q], a, self.K)
        if b[0] == 'not': return ('if', self.bterm(b[1], R), F_, T_)
        if b[0] == 'and': return ('if', self.bterm(b[1], R), self.bterm(b[2], R), F_)
        return ('if', self.bterm(b[1], R), T_, self.bterm(b[2], R))

    def body(self, x, R):
        if x[0] == 'C': return L.C_
        if x[0] == 'D': return L.D_
        return ('if', self.bterm(x[1], R), self.body(x[2], R), self.body(x[3], R))

    def marked_body(self, x, M):
        off = mcount(M)
        b = self.body(x, self.roles(off))
        if M & 2:
            b = ('app', ('lam', b), ('nat', MARK_BASE + 2))
        if M & 1:
            b = ('app', ('lam', b), ('nat', MARK_BASE + 1))
        return b

    def program(self, x, M, certs):
        return C.carrier(self.marked_body(x, M), certs)


# named bodies
def A_(at): return ('A', at)
S_C = ('chk', 'them', 'me', 'C')
YCB_D = ('chk', 'them', 'CB', 'D')
EQA = ('eq',)
CB_X = ('if', A_(S_C), ('C',), ('D',))
CB1_X = ('if', A_(S_C), ('if', A_(('chk', 'me', 'them', 'C')), ('C',), ('D',)), ('D',))
CBP_X = ('if', A_(S_C), ('if', A_(('chk', 'them', 'D', 'D')), ('C',), ('D',)), ('D',))
XC_X = ('if', ('and', A_(S_C), A_(YCB_D)), ('C',), ('D',))
XC2_X = ('if', ('and', A_(YCB_D), A_(S_C)), ('C',), ('D',))
EQ_X = ('if', A_(EQA), ('C',), ('D',))
EQ2_X = ('if', ('not', A_(EQA)), ('D',), ('C',))
TC1_X = ('if', A_(('tag', 1)), ('C',), ('D',))
TC2_X = ('if', A_(('tag', 2)), ('C',), ('D',))
AF1_X = ('if', ('and', A_(('tag', 1)), A_(S_C)), ('C',), ('D',))
OF1_X = ('if', ('or', A_(('tag', 1)), A_(S_C)), ('C',), ('D',))
TWIND_X = ('if', ('or', A_(('chk', 'me', 'me', 'D')), A_(('chk', 'me', 'them', 'D'))), ('D',), ('C',))
NAMED = {   # name -> (body, marker set)
    'Cc': (('C',), 0), 'D': (('D',), 0), 'D^1': (('D',), 1), 'CB': (CB_X, 0), 'MC^1': (CB_X, 1),
    'TC1': (TC1_X, 0), 'TC1^1': (TC1_X, 1), 'AF^1': (AF1_X, 1), 'OF^1': (OF1_X, 1),
    'EQ': (EQ_X, 0), "EQ'": (EQ2_X, 0), 'TwinD': (TWIND_X, 0), 'XC': (XC_X, 0), "XC'": (XC2_X, 0),
}
NAMED_ORDER = ['Cc', 'D', 'D^1', 'CB', 'MC^1', 'TC1', 'TC1^1', 'AF^1', 'OF^1', 'EQ', "EQ'", 'TwinD', 'XC', "XC'"]
HAND = {  # notes §1.6: row's action against column, columns in NAMED_ORDER
    'Cc':    'CCCCCCCCCCCCCC',
    'D':     'DDDDDDDDDDDDDD',
    'D^1':   'DDDDDDDDDDDDDD',
    'CB':    'CDDCCDDDCDDDDD',
    'MC^1':  'CDDCCCCCCDDDDD',
    'TC1':   'DDCDCDCCCDDDDD',
    'TC1^1': 'DDCDCDCCCDDDDD',
    'AF^1':  'DDDDCDCCCDDDDD',
    'OF^1':  'CDCCCCCCCDDDDD',
    'EQ':    'DDDDDDDDDCDDDD',
    "EQ'":   'DDDDDDDDDDCDDD',
    'TwinD': 'DDDDDDDDDDDCDD',
    'XC':    'DDDDDDDDDDDDCC',
    "XC'":   'DDDDDDDDDDDDCC',
}


# ----------------------------------------------------------------------------------------------------------------
# 3. Production
# ----------------------------------------------------------------------------------------------------------------
def build_probes(prod, K, V):
    """CB, CB1, CBP (milestone 4), CB^1, CB^2, CB^12 (CB with markers), XC (two passes).  Returns (probes, cb_term)."""
    base = CP.make_probes(prod, 0, K, V)                 # [(name, term)] with full lists
    cb_term = dict(base)['CB']
    comp = Compiler(V, K, cb_term)
    probes = list(base)
    for M in (1, 2, 3):
        mk = lambda c, M=M: comp.program(CB_X, M, c)
        lst, _ = C.produce_list(prod, 0, mk, base, K, V)
        probes.append(('CB' + MS_NAME[M], mk(lst)))
    mkx = lambda c: comp.program(XC_X, 0, c)
    d = prod.produce(0, mkx(0), L.PROG_D, 'D', K, V)
    xc0 = mkx(C.cons([('D', d)] if d else []))
    lst, _ = C.produce_list(prod, 0, mkx, probes + [('XC', xc0)], K, V)
    probes.append(('XC', mkx(lst)))
    return probes, cb_term, comp


# ----------------------------------------------------------------------------------------------------------------
# 4. The catalogue
# ----------------------------------------------------------------------------------------------------------------
class Catalogue:
    """Spellings (body, marker set) with nodes(body) + |M| <= nmax; tau'-units (dt, M, cb); lists produced once per
    (dt, M & tags(dt)) (notes §1.3).  sub: atom-alphabet restriction (eq, tags, cbq) for small test catalogues."""

    def __init__(self, nmax=7, K=K_DEF, eq=True, tags=True, cbq=True, verbose=False, lists=None):
        self.nmax, self.K = nmax, K
        self.V = V = K // 4
        self.alphabet = atom_alphabet(eq, tags, cbq)
        G = enumerate_grammar(nmax, self.alphabet)
        self.sexprs = [x for n in range(1, nmax + 1) for x in G[n]]
        self.sx_index = {x: i for i, x in enumerate(self.sexprs)}
        self.prod = C.Producer(host=CP.ExactHost())
        self.probes, self.cb_term, self.comp = build_probes(self.prod, K, V)
        # dts
        dts = {}
        self.sx_dt = np.zeros(len(self.sexprs), np.int64)
        self.dt_list = []
        for i, x in enumerate(self.sexprs):
            d = dt(x)
            j = dts.get(d)
            if j is None:
                j = len(self.dt_list); dts[d] = j; self.dt_list.append(d)
            self.sx_dt[i] = j
        self.dt_index = dts
        self.dt_tags = np.array([tagbits_of(dt_atoms(d)) for d in self.dt_list], np.int64)
        self.dt_atomsets = [dt_atoms(d) for d in self.dt_list]
        # spellings
        sp = []
        cb_i = self.sx_index[CB_X]
        for i, x in enumerate(self.sexprs):
            n = nodes(x)
            for M in MSETS:
                if n + mcount(M) <= nmax:
                    sp.append((i, M, n + mcount(M), int(i == cb_i and M == 0)))
        self.sp_sx = np.array([s[0] for s in sp], np.int64)
        self.sp_M = np.array([s[1] for s in sp], np.int64)
        self.sp_nodes = np.array([s[2] for s in sp], np.int64)
        self.sp_cb = np.array([s[3] for s in sp], np.int64)
        self.sp_dt = self.sx_dt[self.sp_sx]
        self.nsp = len(sp)
        # units (dt, M, cb)
        ukey = {}
        self.sp_unit = np.zeros(self.nsp, np.int64)
        members = []
        for k in range(self.nsp):
            key = (int(self.sp_dt[k]), int(self.sp_M[k]), int(self.sp_cb[k]))
            u = ukey.get(key)
            if u is None:
                u = len(members); ukey[key] = u; members.append([])
            self.sp_unit[k] = u
            members[u].append(k)
        for m in members:
            m.sort(key=lambda k: (self.sp_nodes[k], k))
        self.members = members
        self.unit_key = ukey
        self.NU = len(members)
        self.u_dt = np.array([0] * self.NU, np.int64); self.u_M = np.zeros(self.NU, np.int64); self.u_cb = np.zeros(self.NU, np.int64)
        for key, u in ukey.items():
            self.u_dt[u], self.u_M[u], self.u_cb[u] = key
        self.u_tags = self.dt_tags[self.u_dt]
        # projections proj[u, G] = unit (dt_u, M_u & G, cb_u)
        self.proj = np.zeros((self.NU, 4), np.int64)
        for u in range(self.NU):
            for g in range(4):
                self.proj[u, g] = ukey[(int(self.u_dt[u]), int(self.u_M[u]) & g, int(self.u_cb[u]))]
        # lists per (dt, M & tags(dt))
        if lists is None:
            lists = self.produce_all(verbose)
        self.lists = lists                                   # dict (dt, Mrel) -> list data
        self.u_list = [lists[(int(self.u_dt[u]), int(self.u_M[u]) & int(self.u_tags[u]))] for u in range(self.NU)]
        self.u_hasC = np.array([self._has(l, 'C') for l in self.u_list])
        self.u_hasD = np.array([self._has(l, 'D') for l in self.u_list])
        self._terms = {}
        if verbose:
            print('catalogue n<=%d: %d bodies, %d spellings, %d dts, %d units' % (nmax, len(self.sexprs), self.nsp, len(self.dt_list), self.NU), flush=True)

    @staticmethod
    def _has(l, a):
        return l != 0 and any(e[0] == a for e in C.uncons(l))

    def produce_all(self, verbose=False):
        out = {}
        # one representative body per (dt, Mrel): the lightest spelling of that dt (any marker set works for the run of
        # the program against the probes; the marker set Mrel is used)
        rep_sx = {}
        for i in range(len(self.sexprs)):
            j = int(self.sx_dt[i])
            if j not in rep_sx or nodes(self.sexprs[i]) < nodes(self.sexprs[rep_sx[j]]): rep_sx[j] = i
        todo = []
        for j in range(len(self.dt_list)):
            tg = int(self.dt_tags[j])
            for M in MSETS:
                if (M & tg) == M and (j, M) not in out:
                    todo.append((j, M))
        import time
        t0 = time.time()
        for n_, (j, M) in enumerate(todo):
            x = self.sexprs[rep_sx[j]]
            mk = lambda c, x=x, M=M: self.comp.program(x, M, c)
            lst, _ = C.produce_list(self.prod, 0, mk, self.probes, self.K, self.V)
            out[(j, M)] = lst
            if verbose and n_ % 2000 == 0:
                print('  production %d / %d (%.0fs)' % (n_, len(todo), time.time() - t0), flush=True)
        return out

    def produce_spelling(self, k):
        """Direct production for one spelling (for the validation of 'lists depend on (dt, M & tags) only')."""
        x = self.sexprs[int(self.sp_sx[k])]; M = int(self.sp_M[k])
        mk = lambda c: self.comp.program(x, M, c)
        lst, _ = C.produce_list(self.prod, 0, mk, self.probes, self.K, self.V)
        return lst

    def term(self, k):
        t = self._terms.get(k)
        if t is None:
            u = int(self.sp_unit[k])
            t = self.comp.program(self.sexprs[int(self.sp_sx[k])], int(self.sp_M[k]), self.u_list[u])
            self._terms[k] = t
        return t

    def name(self, k):
        return show(self.sexprs[int(self.sp_sx[k])]) + MS_NAME[int(self.sp_M[k])]

    def spelling_of(self, x, M):
        i = self.sx_index[x]
        ks = np.nonzero((self.sp_sx == i) & (self.sp_M == M))[0]
        return int(ks[0])

    def rep(self, u, which=0):
        m = self.members[u]
        return m[min(which, len(m) - 1)]

    def spelling_weights(self, mask=None):
        """L: 2^-(nodes + |M|) per spelling (unnormalized; restricted to mask if given)."""
        w = 2.0 ** (-self.sp_nodes.astype(float))
        if mask is not None: w = w * mask
        return w

    def sub_mask(self, kind):
        """Spelling masks for the ablations (notes §1.8)."""
        has = lambda pred: np.array([any(pred(a) for a in atoms_of(self.sexprs[i])) for i in range(len(self.sexprs))])
        eqb = has(lambda a: a[0] == 'eq')[self.sp_sx]
        tgb = has(lambda a: a[0] == 'tag')[self.sp_sx]
        cbb = has(lambda a: a[0] == 'chk' and a[2] == 'CB')[self.sp_sx]
        mk = self.sp_M > 0
        if kind == 'identity': return (~tgb) & (~mk) & (~cbb)
        if kind == 'tags': return (~eqb) & (~cbb)
        if kind == 'cbq': return (~eqb) & (~tgb) & (~mk)
        if kind == 'm2': return (~eqb) & (~tgb) & (~mk) & (~cbb)
        raise ValueError(kind)


# ----------------------------------------------------------------------------------------------------------------
# 5. Checks on reduced keys, unit values, composition
# ----------------------------------------------------------------------------------------------------------------
def twin_instance(cat, c, t=None, m=None):
    """Two distinct spellings that both reduce to unit c (for the twin value of c)."""
    if len(cat.members[c]) >= 2: return cat.members[c][0], cat.members[c][1]
    if t is not None and m is not None and t != m: return cat.rep(t), cat.rep(m)
    # siblings: the same dt and cb, a marker set equal to M_c on tags(dt), different outside
    d, M, cb = int(cat.u_dt[c]), int(cat.u_M[c]), int(cat.u_cb[c])
    tg = int(cat.dt_tags[d])
    sib = [cat.unit_key[(d, M2, cb)] for M2 in MSETS if (d, M2, cb) in cat.unit_key and (M2 & tg) == (M & tg) and M2 != M]
    if sib: return cat.members[c][0], cat.rep(sib[0])
    return None


def asker_masks(cat):
    """Per unit: S_a askers (CHK(them, me, a)) and R_a askers (CHK(me, them, a))."""
    S = {a: np.zeros(cat.NU, bool) for a in 'CD'}
    R = {a: np.zeros(cat.NU, bool) for a in 'CD'}
    for u in range(cat.NU):
        ats = cat.dt_atomsets[int(cat.u_dt[u])]
        for a in 'CD':
            if ('chk', 'them', 'me', a) in ats: S[a][u] = True
            if ('chk', 'me', 'them', a) in ats: R[a][u] = True
    return S, R


def needed_keys(cat, a, chunk=500):
    """The reduced keys (ct * NU + cm) needed for outcome a, with an instance (spelling pair) each.  Targets without an
    a-entry are skipped (F by the code's empty-selection branch)."""
    NU = cat.NU
    S, R = asker_masks(cat)
    has = cat.u_hasC if a == 'C' else cat.u_hasD
    sask = np.nonzero(S[a])[0]
    allu = np.arange(NU)
    parts = []
    tg = cat.u_tags
    for s0 in range(0, NU, chunk):
        ks = []
        for t in range(s0, min(NU, s0 + chunk)):
            if not has[t]: continue
            ms = allu if R[a][t] else sask
            if not len(ms): continue
            G = tg[t] | tg[ms]
            ct = cat.proj[t, G]; cm = cat.proj[ms, G]
            key = ct * NU + cm
            # remember an original pair for twin keys of single-spelling units
            ks.append(np.stack([key, np.full(len(ms), t), ms], 1))
        if ks:
            arr = np.concatenate(ks)
            _, idx = np.unique(arr[:, 0], return_index=True)
            parts.append(arr[idx])
    if not parts: return np.zeros((0, 3), np.int64)
    arr = np.concatenate(parts)
    _, idx = np.unique(arr[:, 0], return_index=True)
    return arr[idx]


def key_instances(cat, keys):
    """keys: rows (key, t, m).  Returns rows (key, ct, spelling_t, spelling_m) (instance -1 if none: not needed)."""
    NU = cat.NU
    out = np.zeros((len(keys), 4), np.int64)
    for r, (key, t, m) in enumerate(keys):
        ct, cm = divmod(int(key), NU)
        if ct != cm:
            out[r] = (key, ct, cat.rep(ct), cat.rep(cm))
        else:
            ti = twin_instance(cat, ct, int(t), int(m))
            out[r] = (key, ct, ti[0], ti[1]) if ti else (key, ct, -1, -1)
    return out


def fill_dense(cat, a, keys_sorted, vals, S, R):
    """CH_a[t, m] over units for every asked entry (0 elsewhere): the value of the reduced key."""
    NU = cat.NU
    has = cat.u_hasC if a == 'C' else cat.u_hasD
    CH = np.zeros((NU, NU), np.int8)
    sask = np.nonzero(S[a])[0]
    allu = np.arange(NU)
    tg = cat.u_tags
    for t in range(NU):
        if not has[t]: continue
        ms = allu if R[a][t] else sask
        if not len(ms): continue
        G = tg[t] | tg[ms]
        key = cat.proj[t, G] * NU + cat.proj[ms, G]
        pos = np.searchsorted(keys_sorted, key)
        CH[t, ms] = vals[pos]
    return CH


UV_KINDS = ('self', 'C', 'D', 'CB')


def unit_value_keys(cat):
    """Canonical unit for unit values: (dt, M & tags(dt), cb)."""
    return np.array([cat.proj[u, int(cat.u_tags[u])] for u in range(cat.NU)], np.int64)


def eval_dt(t, val):
    if isinstance(t, str): return 1 if t == 'C' else 0
    v = val(t[0])
    a, b = eval_dt(t[1], val), eval_dt(t[2], val)
    if isinstance(v, np.ndarray):
        return np.where(v, a, b)
    return a if v else b


def compose(cat, CH, UV):
    """The unit-level action table A[x, y] (x against a distinct spelling of y; the diagonal is the twin play) and the
    self action.  CH[a]: dense (NU, NU) int8 pair checks; UV[(kind, a)]: (NU,) int8 unit values."""
    NU = cat.NU
    A = np.zeros((NU, NU), np.int8)
    selfa = np.zeros(NU, np.int8)
    Mbits = cat.u_M
    for x in range(NU):
        d = cat.dt_list[int(cat.u_dt[x])]

        def val(at, x=x):
            if at[0] == 'eq':
                return np.zeros(NU, bool)
            if at[0] == 'tag':
                return (Mbits & (1 << (at[1] - 1))) > 0
            _, p, q, a = at
            if p == 'them' and q == 'me': return CH[a][:, x].astype(bool)
            if p == 'me' and q == 'them': return CH[a][x, :].astype(bool)
            if p == 'them' and q == 'them': return UV[('self', a)].astype(bool)
            if p == 'them': return UV[(q, a)].astype(bool)
            if p == 'me' and q == 'me': return np.full(NU, bool(UV[('self', a)][x]))
            return np.full(NU, bool(UV[(q, a)][x]))
        r = eval_dt(d, val)
        if not isinstance(r, np.ndarray): r = np.full(NU, r)
        A[x] = r

        def sval(at, x=x):
            if at[0] == 'eq': return True
            if at[0] == 'tag': return bool(Mbits[x] & (1 << (at[1] - 1)))
            _, p, q, a = at
            if q in ('me', 'them'): return bool(UV[('self', a)][x])
            return bool(UV[(q, a)][x])
        selfa[x] = eval_dt(d, sval)
    return A, selfa


def pay_matrix(A):
    return CP.pay_matrix(A)


def serial_tables(cat, kind='ideal'):
    """The unit-level action table computed serially (small catalogues and tests): unit values, reduced-key pair
    checks, composition.  Returns (A_u, self_u)."""
    S, R = asker_masks(cat)
    chk = CP.Checker(kind, cat.V, cat.K)
    QM = {'C': L.PROG_C, 'D': L.PROG_D, 'CB': cat.cb_term}
    canon = unit_value_keys(cat)
    UVc = {}
    for c in np.unique(canon):
        t = cat.term(cat.rep(int(c))); res = []
        for kd in UV_KINDS:
            for a in 'CD':
                has = cat.u_hasC[c] if a == 'C' else cat.u_hasD[c]
                if not has:
                    res.append(0); continue
                m = t if kd == 'self' else QM[kd]
                res.append(1 if chk(0, t, m, a)[0] == 'T' else 0)
        UVc[int(c)] = res
    UV = {}; j = 0
    for kd in UV_KINDS:
        for a in 'CD':
            UV[(kd, a)] = np.array([UVc[int(canon[u])][j] for u in range(cat.NU)], np.int8); j += 1
    CH = {}
    for a in 'CD':
        inst = key_instances(cat, needed_keys(cat, a))
        vals = np.zeros(len(inst), np.int8)
        for r, (key, ct, st, sm) in enumerate(inst):
            if st < 0: continue
            vals[r] = chk(0, cat.term(int(st)), cat.term(int(sm)), a)[0] == 'T'
        CH[a] = fill_dense(cat, a, inst[:, 0], vals, S, R)
    return compose(cat, CH, UV)


# ----------------------------------------------------------------------------------------------------------------
# 6. Identity-aware lumping
# ----------------------------------------------------------------------------------------------------------------
def lump(cat, A_u, self_u, w_spell):
    """Classes of spellings (milestone 2's criterion on the tau'-expanded matrix).  A_u[t1, t2]: action of a spelling
    of t1 against a distinct spelling of t2 (diagonal: twins); self_u[t]: against itself.  Units with >= 2 spellings
    whose twin play differs from self play split into singleton classes."""
    T = cat.NU
    sizes = np.array([len(m) for m in cat.members])
    split = (sizes >= 2) & (np.diag(A_u) != self_u)
    Ad = A_u.copy()
    Ad[np.arange(T), np.arange(T)] = self_u
    groups = defaultdict(list)
    for t in range(T):
        if split[t]: continue
        r = 2 * Ad[t].astype(np.int8) + Ad[:, t]
        c = 2 * Ad[:, t].astype(np.int8) + Ad[t]
        groups[(hash(r.tobytes()), hash(np.ascontiguousarray(c).tobytes()))].append(t)
    exact = []
    for ts in groups.values():
        rest = list(ts)
        while rest:
            t0 = rest[0]
            r0 = Ad[t0]; c0 = Ad[:, t0]
            same = [t for t in rest if np.array_equal(Ad[t], r0) and np.array_equal(Ad[:, t], c0)]
            exact.append(same)
            ss = set(same)
            rest = [t for t in rest if t not in ss]
    classes = []
    for ts in exact:
        sp = [k for t in ts for k in cat.members[t]]
        classes.append(dict(types=sorted(ts), spellings=sorted(sp), split=False))
    for t in np.nonzero(split)[0]:
        for k in cat.members[t]:
            classes.append(dict(types=[int(t)], spellings=[k], split=True))
    nc = len(classes)
    rep_t = np.array([c['types'][0] for c in classes])
    A = Ad[np.ix_(rep_t, rep_t)].copy()
    for i in range(nc):
        A[i, i] = self_u[rep_t[i]]
    by_type = defaultdict(list)
    for i, c in enumerate(classes):
        if c['split']: by_type[c['types'][0]].append(i)
    for t, idx in by_type.items():
        for i in idx:
            for j in idx:
                if i != j: A[i, j] = A_u[t, t]
    for c in classes:
        c['rep'] = min(c['spellings'], key=lambda k: (cat.sp_nodes[k], k))
    mass = np.array([w_spell[c['spellings']].sum() for c in classes])
    order = np.argsort(-mass, kind='stable')
    classes = [classes[i] for i in order]
    A = A[np.ix_(order, order)]
    return dict(classes=classes, A=A, n_split_units=int(split.sum()), n_split_classes=int(sum(1 for c in classes if c['split'])))


def class_of_spelling(classes, n):
    out = np.full(n, -1, np.int64)
    for i, c in enumerate(classes):
        out[c['spellings']] = i
    return out


# ----------------------------------------------------------------------------------------------------------------
# 7. Families
# ----------------------------------------------------------------------------------------------------------------
def props(A):
    """Class properties from the class action table A (A[i, j] = 1 if i plays C against j)."""
    nc = A.shape[0]
    selfc = A[np.arange(nc), np.arange(nc)] == 1
    return selfc


def compat_graph(A, est):
    mutual = (A == 1) & (A.T == 1)
    idx = np.nonzero(est)[0]
    return mutual, idx


def maximal_cliques(A, nodes_, limit=200000):
    """Maximal cliques of the mutual-cooperation graph restricted to nodes_ (networkx Bron-Kerbosch with pivoting)."""
    import networkx as nx
    mutual = (A == 1) & (A.T == 1)
    G = nx.Graph()
    G.add_nodes_from(int(i) for i in nodes_)
    sub = mutual[np.ix_(nodes_, nodes_)]
    ii, jj = np.nonzero(np.triu(sub, 1))
    G.add_edges_from((int(nodes_[i]), int(nodes_[j])) for i, j in zip(ii, jj))
    out = []
    complete = True
    for c in nx.find_cliques(G):
        out.append(sorted(c))
        if len(out) >= limit:
            complete = False
            break
    comps = [sorted(c) for c in nx.connected_components(G)]
    return out, complete, comps


def strict_invaders(U, b):
    return np.nonzero(U[:, b] > U[b, b] + 1e-9)[0]
