"""Behavioural hooks (spec specs/2026-10-21-behavioural-hooks.md; predictions predictions/2026-10-21-behavioural-hooks.md).

Part A, the key family.  A key is a *modalized* formula over the partner's play: atoms a (the partner plays C against me),
c (against the probe ^C), d (against ^D); connectives not, and, or and box; every atom under a box; modal depth <= 2;
size <= 7 nodes (atoms, connectives and boxes each one node).  Box semantics: Kripke semantics on finite linear GL
frames, box phi at world n iff phi at every m < n (vacuously true at world 0); the play of a program at world n is its
value there and the outcome is the stabilized value.  Keys are quotiented by equivalence *on finite linear frames* before
the prior is assigned (coarser than GL-equivalence: GL.3; pairs that are GL-equivalent are always merged) and each class
carries the weight of its shortest member under the arm's length prior bits(s) = log2 a(s) + 2 log2 s + 1, a(s) the
number of spellings of size s in the key language (modal.py's prior).  Constant keys are dropped.

Part B, the evaluator.  hooks_w2.eval_match generalized: a hook fill's key is a program over a *registry* of boxed
subformulas; the registry state of the pair (holder, partner) is advanced world by world from the partner's play against the
holder, against ^C and against ^D (letters), so every key is evaluated jointly with both parties' fills in force.
Everything else (the closed node set, the probes, the stabilized fixed point) is hooks_w2's.

Key ids: 0-7 Part W's behaviour classes (beta exact: b0 = box c, b1 = box d, b2 = box a), 8 = not box a, 9 = box a (the
open keys of hooks_w2), 10.. the family classes (full, then the a-free family).  UNC (4095) marks an unconditional entry.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
from collections import defaultdict
from numba import njit
import hooks_w2 as H

NODES_MAX = 7
DEPTH_MAX = 2
UNC = 4095
ATOMS = ('a', 'c', 'd')
LETTER_BIT = {'a': 0, 'c': 1, 'd': 2}            # letter bit of an atom (a: partner vs me, c: vs ^C, d: vs ^D)
# postfix tokens
T_END, T_A, T_C, T_D, T_NOT, T_AND, T_OR, T_REG = 0, 1, 2, 3, 4, 5, 6, 16
ATOM_TOKEN = {'a': T_A, 'c': T_C, 'd': T_D}


# ------------------------------------------------------------------ point space and truth tables
class PointSpace:
    """All nonempty words over the letter alphabet of length <= L; a formula's truth table is its value at the last
    position of each word (world n = len(word) - 1, atoms read the last letter, box reads the strict prefixes)."""

    def __init__(self, natoms, L):
        self.natoms = natoms; self.nl = 1 << natoms; self.L = L
        nl = self.nl
        self.offs = [0]
        for n in range(1, L + 1):
            self.offs.append(self.offs[-1] + nl ** n)
        self.tot = self.offs[-1]
        self.last = np.concatenate([np.tile(np.arange(nl), nl ** (n - 1)) for n in range(1, L + 1)])
        self.memo = {}

    def atom(self, i):
        return ((self.last >> i) & 1).astype(np.uint8)

    def box(self, f):
        out = np.ones(self.tot, np.uint8)
        offs = self.offs
        for n in range(2, self.L + 1):
            prev = f[offs[n - 2]:offs[n - 1]]
            pb = out[offs[n - 2]:offs[n - 1]]
            out[offs[n - 1]:offs[n]] = np.repeat(pb & prev, self.nl)
        return out

    def box1(self, f):
        """Level-1 box (PA + Con): phi at every world m with 1 <= m < n (ignores world 0)."""
        out = np.ones(self.tot, np.uint8)
        offs = self.offs
        for n in range(3, self.L + 1):
            prev = f[offs[n - 2]:offs[n - 1]]
            pb = out[offs[n - 2]:offs[n - 1]]
            out[offs[n - 1]:offs[n]] = np.repeat(pb & prev, self.nl)
        return out

    def tt(self, form, atoms):
        """Truth table of a formula given as nested tuples ('a'|'c'|'d' | ('not', f) | ('and', f, g) | ('or', f, g) |
        ('box', f)); atoms: the atom names in letter-bit order."""
        key = (form, atoms)
        r = self.memo.get(key)
        if r is not None:
            return r
        if isinstance(form, str):
            r = self.atom(atoms.index(form))
        elif form[0] == 'not':
            r = 1 - self.tt(form[1], atoms)
        elif form[0] == 'and':
            r = self.tt(form[1], atoms) & self.tt(form[2], atoms)
        elif form[0] == 'or':
            r = self.tt(form[1], atoms) | self.tt(form[2], atoms)
        elif form[0] == 'box':
            r = self.box(self.tt(form[1], atoms))
        elif form[0] == 'box1':
            r = self.box1(self.tt(form[1], atoms))
        else:
            raise ValueError(form)
        self.memo[key] = r
        return r


def fsize(form):
    if isinstance(form, str):
        return 1
    return 1 + sum(fsize(f) for f in form[1:])


def fdepth(form):
    if isinstance(form, str):
        return 0
    if form[0] in ('box', 'box1'):
        return 1 + fdepth(form[1])
    return max(fdepth(f) for f in form[1:])


def fname(form):
    if isinstance(form, str):
        return form
    if form[0] == 'not':
        return '~' + fname(form[1])
    if form[0] == 'box':
        return '[]' + fname(form[1])
    if form[0] == 'box1':
        return '[1]' + fname(form[1])
    return '(%s %s %s)' % (fname(form[1]), '&' if form[0] == 'and' else '|', fname(form[2]))


def modalized(form, under=False):
    """Every atom under a box."""
    if isinstance(form, str):
        return under
    if form[0] in ('box', 'box1'):
        return modalized(form[1], True)
    return all(modalized(f, under) for f in form[1:])


def eval_word(form, word, atoms=ATOMS):
    """Direct Kripke semantics (reference): the value of form at the last world of word (letters, bit i = atom i)."""
    n = len(word) - 1

    def ev(f, m):
        if isinstance(f, str):
            return (word[m] >> atoms.index(f)) & 1
        if f[0] == 'not':
            return 1 - ev(f[1], m)
        if f[0] == 'and':
            return ev(f[1], m) & ev(f[2], m)
        if f[0] == 'or':
            return ev(f[1], m) | ev(f[2], m)
        if f[0] == 'box1':          # one level up (BOX1: PA + Con): ignores world 0
            return int(all(ev(f[1], k) for k in range(1, m)))
        return int(all(ev(f[1], k) for k in range(m)))
    return ev(form, n)


# ------------------------------------------------------------------ the family
class Family:
    """The modalized key family over `atoms`: classes (shortest member, size, depth, weight), the spelling counts a(s)."""

    def __init__(self, atoms=ATOMS, L=6, maxsize=NODES_MAX, maxdepth=DEPTH_MAX, level1=True):
        self.atoms = tuple(atoms)
        self.level1 = level1
        ps = PointSpace(len(atoms), L)
        self.ps = ps
        natoms = len(atoms)
        cls = [dict() for _ in range(maxsize + 1)]
        seen = {}

        def add(size, tt, depth, mod, form):
            key = (tt.tobytes(), depth, mod)
            if key in seen:
                return
            seen[key] = size
            cls[size][key] = (tt, depth, mod, form)
        for i in range(natoms):
            add(1, ps.atom(i), 0, False, self.atoms[i])
        synt = [defaultdict(int) for _ in range(maxsize + 1)]
        synt[1][(0, False)] = natoms
        for s in range(2, maxsize + 1):
            for k, (tt, d, m, f) in list(cls[s - 1].items()):
                add(s, 1 - tt, d, m, ('not', f))
            for (d, m), c in synt[s - 1].items():
                synt[s][(d, m)] += c
            for k, (tt, d, m, f) in list(cls[s - 1].items()):
                if d + 1 <= maxdepth:
                    add(s, ps.box(tt), d + 1, True, ('box', f))
                    if level1:
                        add(s, ps.box1(tt), d + 1, True, ('box1', f))
            for (d, m), c in synt[s - 1].items():
                if d + 1 <= maxdepth:
                    synt[s][(d + 1, True)] += c * (2 if level1 else 1)
            for i in range(1, s - 1):
                j = s - 1 - i
                for k1, (t1, d1, m1, f1) in list(cls[i].items()):
                    for k2, (t2, d2, m2, f2) in list(cls[j].items()):
                        d = max(d1, d2); m = m1 and m2
                        add(s, t1 & t2, d, m, ('and', f1, f2))
                        add(s, t1 | t2, d, m, ('or', f1, f2))
                for (d1, m1), c1 in synt[i].items():
                    for (d2, m2), c2 in synt[j].items():
                        synt[s][(max(d1, d2), m1 and m2)] += 2 * c1 * c2
        # a(s): spellings of size s that are modalized with depth <= maxdepth
        self.a = np.array([0] + [sum(c for (d, m), c in synt[s].items() if m and d <= maxdepth) for s in range(1, maxsize + 1)], float)
        by_tt = {}
        self.n_mod_syntactic_classes = 0
        for s in range(1, maxsize + 1):
            for key, (tt, d, m, f) in cls[s].items():
                if not m:
                    continue
                self.n_mod_syntactic_classes += 1
                k2 = tt.tobytes()
                if k2 not in by_tt:                       # shortest first; ties by depth then discovery order
                    by_tt[k2] = dict(form=f, size=s, depth=d, tt=tt)
        self.constants = [v for v in by_tt.values() if v['tt'].min() == v['tt'].max()]
        self.classes = [v for v in by_tt.values() if v['tt'].min() != v['tt'].max()]
        for v in self.classes:
            s = v['size']
            v['bits'] = math.log2(self.a[s]) + 2 * math.log2(s) + 1
            v['name'] = fname(v['form'])
        w = np.array([2.0 ** (-v['bits']) for v in self.classes])
        self.weight = w / w.sum()
        for v, x in zip(self.classes, self.weight):
            v['weight'] = float(x)


# ------------------------------------------------------------------ registry and key table
class KeyTable:
    """All key programs: legacy keys 0-9, the full family, the a-free family; the registry of boxed subformulas."""

    def __init__(self, L_reg=5, fam_full=None, fam_noa=None, verbose=False, level1=True):
        self.ps = PointSpace(3, L_reg)
        self.reg = {}                 # truth table bytes of the box -> registry index
        self.reg_form = []            # the boxed formula
        self.reg_body = []            # postfix of the box's body
        self.reg_level = []           # 0 = box, 1 = box1 (ignores world 0)
        self.keys = []                # dicts: id, name, form, prog, family
        self.fam_full = fam_full or Family(ATOMS, level1=level1)
        self.fam_noa = fam_noa or Family(('c', 'd'), level1=level1)
        beta_form = lambda b: ('and', ('and', ('box', 'c') if b & 1 else ('not', ('box', 'c')), ('box', 'd') if b & 2 else ('not', ('box', 'd'))),
                               ('box', 'a') if b & 4 else ('not', ('box', 'a')))
        for b in range(8):
            self._add_key('beta%d' % b, beta_form(b), 'legacy')
        self._add_key('not[]a', ('not', ('box', 'a')), 'legacy')       # open key 8: p = 0
        self._add_key('[]a', ('box', 'a'), 'legacy')                    # open key 9: p = 1
        self.n_legacy = len(self.keys)
        self.full_ids = []; self.noa_ids = []
        for v in self.fam_full.classes:
            self.full_ids.append(self._add_key(v['name'], v['form'], 'full', v))
        for v in self.fam_noa.classes:
            self.noa_ids.append(self._add_key(v['name'], v['form'], 'noa', v))
        assert len(self.keys) < UNC
        self.R = len(self.reg_form)
        self._arrays()
        self.prior_full = np.zeros(len(self.keys)); self.prior_noa = np.zeros(len(self.keys))
        for i, v in zip(self.full_ids, self.fam_full.classes):
            self.prior_full[i] = v['weight']
        for i, v in zip(self.noa_ids, self.fam_noa.classes):
            self.prior_noa[i] = v['weight']
        self.by_name = {}
        for k in self.keys:
            self.by_name.setdefault((k['family'], k['name']), k['id'])

    # -- compilation
    def _reg_of(self, box_form):
        tt = self.ps.tt(box_form, ATOMS).tobytes()
        j = self.reg.get(tt)
        if j is not None:
            return j
        body = self._compile(box_form[1])
        j = len(self.reg_form)
        self.reg[tt] = j; self.reg_form.append(box_form); self.reg_body.append(body)
        self.reg_level.append(1 if box_form[0] == 'box1' else 0)
        return j

    def _compile(self, form):
        if isinstance(form, str):
            return [ATOM_TOKEN[form]]
        if form[0] == 'not':
            return self._compile(form[1]) + [T_NOT]
        if form[0] == 'and':
            return self._compile(form[1]) + self._compile(form[2]) + [T_AND]
        if form[0] == 'or':
            return self._compile(form[1]) + self._compile(form[2]) + [T_OR]
        return [T_REG + self._reg_of(form)]            # box or box1

    def _add_key(self, name, form, family, info=None):
        prog = self._compile(form)
        kid = len(self.keys)
        self.keys.append(dict(id=kid, name=name, form=form, prog=prog, family=family, size=fsize(form), depth=fdepth(form)))
        return kid

    def _arrays(self):
        nk = len(self.keys)
        mp = max(len(k['prog']) for k in self.keys) + 1
        mb = max(len(b) for b in self.reg_body) + 1
        self.key_prog = np.zeros((nk + 1, mp), np.int32)        # row UNC unused; indexed by id (<= nk)
        for k in self.keys:
            self.key_prog[k['id'], :len(k['prog'])] = k['prog']
        self.reg_lvl = np.array(self.reg_level, np.int32)
        self.reg_prog = np.zeros((self.R, mb), np.int32)
        for j, b in enumerate(self.reg_body):
            self.reg_prog[j, :len(b)] = b
        # requirement closure: registry boxes needed to evaluate a key (its own refs plus their bodies' refs)
        refs = []
        for j, b in enumerate(self.reg_body):
            refs.append({t - T_REG for t in b if t >= T_REG})

        def closure(js):
            out = set(); st = list(js)
            while st:
                x = st.pop()
                if x in out:
                    continue
                out.add(x); st.extend(refs[x])
            return out
        self.key_req = -np.ones((nk + 1, 40), np.int32)
        self.max_req = 0
        for k in self.keys:
            js = closure({t - T_REG for t in k['prog'] if t >= T_REG})
            self.max_req = max(self.max_req, len(js))
            assert len(js) <= 40
            for i, j in enumerate(sorted(js)):
                self.key_req[k['id'], i] = j
        self.reg_req = -np.ones((self.R, 40), np.int32)
        for j in range(self.R):
            js = closure({j})
            for i, x in enumerate(sorted(js)):
                self.reg_req[j, i] = x

    def arrays(self):
        return (self.key_prog, self.reg_prog, self.key_req, self.reg_lvl)

    def id_of(self, form, family=None):
        """Key id of the class of `form` (by truth table) within a family ('full', 'noa' or 'legacy'); -1 if absent."""
        tt = self.ps.tt(form, ATOMS).tobytes()
        for k in self.keys:
            if family is not None and k['family'] != family:
                continue
            if self.ps.tt(k['form'], ATOMS).tobytes() == tt:
                return k['id']
        return -1


# ------------------------------------------------------------------ spec packing (entries: 1 + (key << 2 | tag << 1 | action))
@njit(cache=True)
def entry(key, tag, act):
    return 1 + ((key << 2) | (tag << 1) | act)


@njit(cache=True)
def en_key(e): return (e - 1) >> 2
@njit(cache=True)
def en_tag(e): return ((e - 1) >> 1) & 1
@njit(cache=True)
def en_act(e): return (e - 1) & 1
EBITS = 15
WMAX = 14                    # letters kept per reading word (stabilization by world 14; counted when exceeded)
TAIL = 6


@njit(cache=True)
def spec_of_beh(fills, nf, tags, active, recency, ctx):
    """Packed spec of a holder with fills[0:nf] (oldest first) in a match whose partner lineage is ctx (-1: none).  Per carried
    tag, in resolution order: the behaviour-scope entries (newest first; applicable when their key holds) and then at most
    one unconditional entry (the best applicable non-behaviour fill: history > role > none, ties newest).  recency = 1: the
    newest applicable fill of any scope wins (entries newest first, truncated after the first unconditional one).
    Entry word: 1 + (key << 2 | tag << 1 | action), key = UNC for an unconditional entry; four entries of 14 bits."""
    out = np.int64(0); ne = 0
    for t in range(2):
        if not (tags >> t) & 1:
            continue
        if recency == 1:
            for j in range(nf - 1, -1, -1):
                f = fills[j]
                if H.f_tag(f) != t:
                    continue
                sc = H.f_scope(f)
                if not active[sc, H.f_origin(f)]:
                    continue
                if sc == 3:
                    out |= np.int64(entry(H.f_key(f) & 4095, t, H.f_action(f))) << (EBITS * ne); ne += 1
                    continue
                if sc == 2 and not (ctx >= 0 and H.f_key(f) == ctx):
                    continue
                out |= np.int64(entry(UNC, t, H.f_action(f))) << (EBITS * ne); ne += 1
                break
        else:
            for j in range(nf - 1, -1, -1):
                f = fills[j]
                if H.f_tag(f) != t or H.f_scope(f) != 3 or not active[3, H.f_origin(f)]:
                    continue
                out |= np.int64(entry(H.f_key(f) & 4095, t, H.f_action(f))) << (EBITS * ne); ne += 1
            best = -1; bestp = -1
            for j in range(nf - 1, -1, -1):
                f = fills[j]
                if H.f_tag(f) != t:
                    continue
                sc = H.f_scope(f)
                if sc == 3 or not active[sc, H.f_origin(f)]:
                    continue
                if sc == 2 and not (ctx >= 0 and H.f_key(f) == ctx):
                    continue
                if sc > bestp:
                    bestp = sc; best = j
            if best >= 0:
                out |= np.int64(entry(UNC, t, H.f_action(fills[best]))) << (EBITS * ne); ne += 1
    return out


# ------------------------------------------------------------------ the evaluator
@njit(cache=True)
def _run_prog(prog, ncode, letter, B, stack):
    """Evaluate a postfix program: letter = the three atom bits of the current world, B = registry values at this world."""
    sp = 0
    for i in range(ncode):
        t = prog[i]
        if t == 0:
            break
        if t == 1:
            stack[sp] = letter & 1; sp += 1
        elif t == 2:
            stack[sp] = (letter >> 1) & 1; sp += 1
        elif t == 3:
            stack[sp] = (letter >> 2) & 1; sp += 1
        elif t == 4:
            stack[sp - 1] = 1 - stack[sp - 1]
        elif t == 5:
            sp -= 1; stack[sp - 1] = stack[sp - 1] & stack[sp]
        elif t == 6:
            sp -= 1; stack[sp - 1] = stack[sp - 1] | stack[sp]
        else:
            stack[sp] = 1 if B[t - 16] else 0; sp += 1
    return stack[sp - 1]


@njit(cache=True)
def key_true(kid, key_prog, B):
    """Value of key kid at the world whose registry state is B (no atom is read: every atom is under a box)."""
    stack = np.zeros(32, np.int64)
    return _run_prog(key_prog[kid], key_prog.shape[1], 0, B, stack) == 1


@njit(cache=True)
def _decide(sp, t, key_prog, B, stack):
    """Hook tag t's (applies, action) for the packed spec sp at the registry state B."""
    for e in range(4):
        w = (sp >> (EBITS * e)) & ((1 << EBITS) - 1)
        if w == 0:
            break
        if en_tag(w) != t:
            continue
        k = en_key(w)
        if k == UNC or _run_prog(key_prog[k], key_prog.shape[1], 0, B, stack) == 1:
            return 1, en_act(w)
    return 0, 0


@njit(cache=True)
def _mark_need(sp, key_req, need):
    for e in range(4):
        w = (sp >> (EBITS * e)) & ((1 << EBITS) - 1)
        if w == 0:
            break
        k = en_key(w)
        if k == UNC:
            continue
        for i in range(key_req.shape[1]):
            j = key_req[k, i]
            if j < 0:
                break
            need[j] = True


@njit(cache=True)
def eval_match_beh(p_nat, p_kind, p_lev, p_form, p_arg, p_tt, b_nat, b_kind, b_lev, b_form, b_arg, b_tt,
                   iC, iD, key_prog, reg_prog, key_req, reg_lvl, full, bx, sx0, sx1, sx2, by, sy0, sy1, sy2, rs_out):
    """hooks_w2.eval_match with behavioural keys.  Specs are packed entry words (spec_of_beh).  Returns (x's action vs y, y's
    action vs x, 0, 0); when `full`, rs_out (int64[4]) = the letter words (3 bits per world: the partner's play against the
    reader, ^C, ^D) of x reading y and of y reading x up to the stabilized world plus TAIL copies of the last letter, the word
    length, and the stabilization world n (fold_state turns a word into the registry state); (-1, -1, 0, 0) if the chain did
    not stabilize (never observed).  Only the node pairs the outcome depends on are evaluated (the closure of the references of
    the two programs' atoms, hook letters included); a pair outside the closure is never read, so the result is the full
    evaluation's."""
    P = p_nat.shape[0]
    K = P + 2
    X = P; Y = P + 1
    R = reg_prog.shape[0]
    hc = np.ones((2, K, K), np.bool_)
    hd = np.ones((2, K, K), np.bool_)
    val = np.zeros((K, K), np.int8)
    Bst = np.ones((2, K, R), np.bool_)
    need = np.zeros(R, np.bool_)
    _mark_need(sx0, key_req, need); _mark_need(sx1, key_req, need); _mark_need(sx2, key_req, need)
    _mark_need(sy0, key_req, need); _mark_need(sy1, key_req, need); _mark_need(sy2, key_req, need)
    nlist = np.zeros(R, np.int64); nn = 0
    for j in range(R):
        if need[j]:
            nlist[nn] = j; nn += 1
    # ---- the closure of needed (p, q) pairs
    act = np.zeros((K, K), np.bool_)
    stack_p = np.zeros(K * K, np.int64); stack_q = np.zeros(K * K, np.int64); ns = 0
    act[X, Y] = True; act[Y, X] = True
    stack_p[0] = X; stack_q[0] = Y; stack_p[1] = Y; stack_q[1] = X; ns = 2
    if full:
        for (a_, b_) in ((X, iC), (X, iD), (Y, iC), (Y, iD)):
            if not act[a_, b_]:
                act[a_, b_] = True; stack_p[ns] = a_; stack_q[ns] = b_; ns += 1
    while ns > 0:
        ns -= 1
        p = stack_p[ns]; q = stack_q[ns]
        if p < P:
            nat = p_nat[p]
        else:
            if p == X:
                bs = bx; sp = sx0 if q < P else (sx1 if q == Y else sx2)
            else:
                bs = by; sp = sy0 if q < P else (sy1 if q == X else sy2)
            nat = b_nat[bs]
            if sp != 0:                                     # the registry letters of the pair: q's play against p, ^C, ^D
                for (a_, b_) in ((q, p), (q, iC), (q, iD)):
                    if not act[a_, b_]:
                        act[a_, b_] = True; stack_p[ns] = a_; stack_q[ns] = b_; ns += 1
        for j in range(nat):
            if p < P:
                kd = p_kind[p, j]; f = p_form[p, j]; ar = p_arg[p, j]
            else:
                kd = b_kind[bs, j]; f = b_form[bs, j]; ar = b_arg[bs, j]
            if kd >= 2:
                continue
            if f == 0:
                a_, b_ = q, p
            elif f == 1:
                a_, b_ = q, q
            else:
                a_, b_ = q, ar
            if not act[a_, b_]:
                act[a_, b_] = True; stack_p[ns] = a_; stack_q[ns] = b_; ns += 1
    np_ = 0
    pl = np.zeros(K * K, np.int64); ql = np.zeros(K * K, np.int64)
    for p in range(K):
        for q in range(K):
            if act[p, q]:
                pl[np_] = p; ql[np_] = q; np_ += 1
    bv = np.zeros(R, np.bool_)
    stack = np.zeros(32, np.int64)
    wx = np.int64(0); wy = np.int64(0)
    for n in range(200):
        for u in range(np_):
            p = pl[u]; q = ql[u]
            if p < P:
                idx = 0
                for j in range(p_nat[p]):
                    f = p_form[p, j]
                    if f == 0:
                        a, b = q, p
                    elif f == 1:
                        a, b = q, q
                    else:
                        a, b = q, p_arg[p, j]
                    L = p_lev[p, j]
                    bb = hc[L, a, b] if p_kind[p, j] == 0 else hd[L, a, b]
                    if bb: idx |= 1 << j
                val[p, q] = (p_tt[p] >> idx) & 1
            else:
                if p == X:
                    bs = bx; sp = sx0 if q < P else (sx1 if q == Y else sx2); pi = 0
                else:
                    bs = by; sp = sy0 if q < P else (sy1 if q == X else sy2); pi = 1
                idx = 0
                for j in range(b_nat[bs]):
                    kd = b_kind[bs, j]
                    if kd >= 2:
                        t = b_lev[bs, j]
                        ap, av = _decide(sp, t, key_prog, Bst[pi, q], stack)
                        bb = ap if kd == 2 else av
                        if bb: idx |= 1 << j
                        continue
                    f = b_form[bs, j]
                    if f == 0:
                        a, b = q, p
                    elif f == 1:
                        a, b = q, q
                    else:
                        a, b = q, b_arg[bs, j]
                    L = b_lev[bs, j]
                    bb2 = hc[L, a, b] if kd == 0 else hd[L, a, b]
                    if bb2: idx |= 1 << j
                val[p, q] = (b_tt[bs] >> idx) & 1
        changed = False
        for L in range(2):
            if n < L:
                continue
            for u in range(np_):
                p = pl[u]; q = ql[u]
                c = val[p, q] == 1
                if hc[L, p, q] and not c:
                    hc[L, p, q] = False; changed = True
                if hd[L, p, q] and c:
                    hd[L, p, q] = False; changed = True
        for u in range(np_):
            p = pl[u]; q = ql[u]
            if p < P:
                continue
            pi = p - X
            letter = val[q, p] | (val[q, iC] << 1) | (val[q, iD] << 2)
            for i in range(nn):
                j = nlist[i]
                bv[j] = True if (reg_lvl[j] == 1 and n == 0) else (_run_prog(reg_prog[j], reg_prog.shape[1], letter, Bst[pi, q], stack) == 1)
            for i in range(nn):
                j = nlist[i]
                if Bst[pi, q, j] and not bv[j]:
                    Bst[pi, q, j] = False; changed = True
        if full and n <= WMAX:                                  # the reading pairs' letters: X reads Y, Y reads X
            wx |= np.int64(val[Y, X] | (val[Y, iC] << 1) | (val[Y, iD] << 2)) << (3 * n)
            wy |= np.int64(val[X, Y] | (val[X, iC] << 1) | (val[X, iD] << 2)) << (3 * n)
        if not changed and n >= 2:
            if full:
                lx = (wx >> (3 * n)) & 7; ly = (wy >> (3 * n)) & 7
                for k in range(1, TAIL + 1):                    # the registry reaches its fixed point within depth + 1 constant letters
                    if n + k <= WMAX + TAIL:
                        wx |= lx << (3 * (n + k)); wy |= ly << (3 * (n + k))
                rs_out[0] = wx; rs_out[1] = wy; rs_out[2] = min(n + 1 + TAIL, WMAX + 1 + TAIL); rs_out[3] = n
            return val[X, Y], val[Y, X], 0, 0
    return -1, -1, 0, 0


@njit(cache=True)
def fold_state(word, length, reg_prog, reg_lvl):
    """Registry state after the letter word (letter m = bits 3m..3m+2): box states are conjunctions over the past."""
    R = reg_prog.shape[0]
    B = np.ones(R, np.bool_)
    bv = np.zeros(R, np.bool_)
    stack = np.zeros(32, np.int64)
    for m in range(length):
        letter = (word >> (3 * m)) & 7
        for j in range(R):
            bv[j] = True if (reg_lvl[j] == 1 and m == 0) else (_run_prog(reg_prog[j], reg_prog.shape[1], letter, B, stack) == 1)
        for j in range(R):
            if not bv[j]:
                B[j] = False
    return B


# ------------------------------------------------------------------ named programs, the reference evaluator, the gate
class Beh:
    """Lang + KeyTable + convenience evaluators (no kernel)."""

    def __init__(self, level1=True):
        self.Lx = H.Lang(6)
        self.KT = KeyTable(level1=level1)
        self.LA = self.Lx.arrays()
        self.R = self.KT.R

    def base(self, name):
        return self.Lx.names.index(name)

    def spec(self, fills, tags, ctx=-1, recency=0):
        """Packed spec of a list of fill codes."""
        f = np.zeros(4, np.int64); f[:len(fills)] = fills
        act = np.ones((4, 4), np.bool_)
        return int(spec_of_beh(f, len(fills), tags, act, recency, ctx))

    def play(self, bx, sx, by, sy, full=False):
        """Stabilized plays of x (base bx, packed spec sx in every context) against y; with full, also the registry states
        (x reading y, y reading x) at the stabilized world."""
        rs = np.zeros(4, np.int64)
        L = self.Lx
        ax, ay, _, _ = eval_match_beh(*self.LA, L.iC, L.iD, *self.KT.arrays(), full, bx, sx, sx, sx, by, sy, sy, sy, rs)
        if not full:
            return int(ax), int(ay), None
        KT = self.KT
        return int(ax), int(ay), (fold_state(rs[0], rs[2], KT.reg_prog, KT.reg_lvl), fold_state(rs[1], rs[2], KT.reg_prog, KT.reg_lvl))


def named_programs(B):
    """The spec's named members as (base type, packed spec): each a base hook with one fill."""
    KT = B.KT
    kid = lambda form: KT.id_of(form, 'full')
    box = lambda f: ('box', f)
    ka = box('a'); kna = box(('not', 'a'))
    kprud_pa = ('and', box('a'), box(('not', 'd')))
    kprud = ('and', box('a'), ('box1', ('not', 'd'))) if B.KT.fam_full.level1 else kprud_pa      # the standard PrudentBot
    fc = lambda tag, key, act: H.fcode(act, tag, H.BEH, H.SEEDED, key)
    out = {}
    hd = B.base('HOOK(0,D)'); hc_ = B.base('HOOK(0,C)')
    out['FairBot'] = (hd, B.spec([fc(0, kid(ka), 1)], 1))
    out['TrustingBot'] = (hc_, B.spec([fc(0, kid(kna), 0)], 1))
    out['PrudentBot'] = (hd, B.spec([fc(0, kid(kprud), 1)], 1))
    if B.KT.fam_full.level1:
        out['PrudentBotPA'] = (hd, B.spec([fc(0, kid(kprud_pa), 1)], 1))        # the level-PA reading (the gate's failed entry)
    out['GodelPredator'] = (hc_, B.spec([fc(0, kid(ka), 0)], 1))
    out['CooperateBot'] = (B.Lx.bC, 0)
    out['DefectBot'] = (B.Lx.bD, 0)
    return out


def ref_match(prog_x, prog_y, nworld=40, letters=False):
    """Independent pure-Python Kripke reference (no registry, no numba): programs are (default, [(key form, action)]) with the
    fills newest first; nodes X, Y and the constant probes C, D.  Returns the action sequences (x vs y, y vs x)."""
    nodes = {'X': prog_x, 'Y': prog_y, 'C': ('C', []), 'D': ('D', [])}
    act = {}                                   # (p, q) -> list of actions (1 = C) by world
    for p in nodes:
        for q in nodes:
            act[(p, q)] = []
    for n in range(nworld):
        new = {}
        for p in ('X', 'Y'):
            for q in nodes:
                if q == p:
                    continue
                dflt, fills = nodes[p]
                # letters of the partner q at worlds 0..n-1 (and the current world is irrelevant: atoms are under boxes)
                word = []
                for m in range(n):
                    word.append(act[(q, p)][m] | (act[(q, 'C')][m] << 1) | (act[(q, 'D')][m] << 2) if q in ('X', 'Y') else
                                (1 if nodes[q][0] == 'C' else 0) * 7)
                word.append(0)                  # current world's letter: never read by a modalized key
                v = 1 if dflt == 'C' else 0
                for form, a in fills:
                    if eval_word(form, word):
                        v = a
                        break
                new[(p, q)] = v
        for p in nodes:
            for q in nodes:
                if (p, q) in new:
                    act[(p, q)].append(new[(p, q)])
                elif p in ('C', 'D'):
                    act[(p, q)].append(1 if nodes[p][0] == 'C' else 0)
                else:
                    act[(p, q)].append(0)
    if letters:
        lx = [act[('Y', 'X')][m] | (act[('Y', 'C')][m] << 1) | (act[('Y', 'D')][m] << 2) for m in range(nworld)]
        ly = [act[('X', 'Y')][m] | (act[('X', 'C')][m] << 1) | (act[('X', 'D')][m] << 2) for m in range(nworld)]
        return act[('X', 'Y')], act[('Y', 'X')], lx, ly
    return act[('X', 'Y')], act[('Y', 'X')]
