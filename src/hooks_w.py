"""Hooks, Part W: a first-class hook primitive in the weakly extensional wing (spec specs/2026-10-18-hooks.md,
notes notes/hooks-w.md, predictions predictions/2026-10-18-hooks-w.md).

This module: the hooked modal PD language (n = 6), fills and their resolution (scopes, keys, conflict rule, the inert
discipline), the closed-node GL evaluator for one match between two filled programs, and the ε = 0 island kernel over
types (base, fills, lineage) with sampled encounters that write, copy and contract fills.  The social organization
wing is in src/hooks_w_sog.py.  Imports src/modal.py and src/almost_all_seeds.py unchanged.

Encodings.
  Hook atoms of a canonical function: atom kind 2 = A_t ("a fill for tag t applies"), kind 3 = V_t ("the selected
  fill's action is C"); HOOK(t, C) = not A_t or V_t, HOOK(t, D) = A_t and V_t.  Box atoms are modal.py's.
  Fill code (int, 0 = empty): 1 + (action | tag << 1 | scope << 2 | origin << 4 | key << 6).
  Scopes: 0 none, 1 role, 2 history, 3 behaviour.  Origins: 0 seeded, 1 written, 2 copied, 3 contract.
  Spec of a holder in a context (int64): for tag t, bits [16 t, 16 t + 8) = applies mask over beta in 0..7 and bits
  [16 t + 8, 16 t + 16) = value mask (1 = C); beta = b0 | b1 << 1 | b2 << 2 with b0 = BOX(partner plays C vs ^C),
  b1 = BOX(partner plays C vs ^D), b2 = BOX(partner plays C vs me), all at level PA.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
from numba import njit, types
from numba.typed import Dict
import modal as M

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
W = 0.3
PDPAY = np.array([[-1.0, 1.0], [-2.0, 0.0]])       # [a][b], D = 0, C = 1
NONE, ROLE, HIST, BEH = 0, 1, 2, 3
SCOPES = ('none', 'role', 'history', 'behaviour')
SEEDED, WRITTEN, COPIED, CONTRACT = 0, 1, 2, 3
ORIGINS = ('seeded', 'written', 'copied', 'contract')
KA, KV = 2, 3                                       # hook atom kinds
POISSON = np.array([np.exp(-1) / f for f in (1, 1, 2, 6, 24)]); POISSON /= POISSON.sum()


# ------------------------------------------------------------------ the hooked modal language
class HookedModalLanguage(M.ModalLanguage):
    """modal.ModalLanguage with four one-node hook leaves HOOK(t, a0), t in {0, 1}, a0 in {C, D}.  Quoted programs
    are bare source: THEM(^A) quotes A with its hooks at default (A_t = 0).  hooks=False gives the plain grammar."""

    def __init__(self, n, kinds=((0, 0), (1, 0), (0, 1), (1, 1)), hooks=True):
        self.hooks = hooks
        super().__init__(n, kinds)

    def hook_atom(self, kind, t):
        at = (kind, t, -1, -1)
        aid = self.atom_id.get(at)
        if aid is None:
            aid = len(self.atoms); self.atom_id[at] = aid; self.atoms.append(at)
        return self._canon((aid,), 2)

    def restrict(self, c):
        """Canon of c with every A_t = 0 (hooks at default)."""
        key = ('restrict', c, None)
        if key in self._memo:
            return self._memo[key]
        atoms, tt, k = self.funcs[c]
        keep = [j for j, a in enumerate(atoms) if self.atoms[a][0] != KA]
        if len(keep) == k:
            r = c
        else:
            ntt = 0
            for i in range(1 << len(keep)):
                full = 0
                for jj, j in enumerate(keep):
                    if (i >> jj) & 1:
                        full |= 1 << j
                if (tt >> full) & 1:
                    ntt |= 1 << i
            r = self._canon(tuple(atoms[j] for j in keep), ntt)
        self._memo[key] = r
        return r

    def _src_box(self, kind, level, form, arg):
        inner = {M.TM: 'THEM(ME)', M.TT: 'THEM(THEM)'}.get(form) or 'THEM(^%s)' % self.rep[arg]
        return '%s%s(%s)' % ('BOX' if kind == M.KC else 'BOXD', '1' if level else '', inner)

    def _enumerate(self):
        from collections import defaultdict
        n = self.n
        cnt = [defaultdict(int) for _ in range(n + 1)]
        for name in ('C', 'D'):
            c = self.op(name); cnt[1][c] += 1; self._note(c, 1, name)
        if self.hooks:
            for t in (0, 1):
                A = self.hook_atom(KA, t); V = self.hook_atom(KV, t)
                hc = self.op('or', self.op('not', A), V)
                hd = self.op('and', A, V)
                cnt[1][hc] += 1; self._note(hc, 1, 'HOOK(%d,C)' % t)
                cnt[1][hd] += 1; self._note(hd, 1, 'HOOK(%d,D)' % t)
        for s in range(2, n + 1):
            for c, m in list(cnt[s - 1].items()):
                c2 = self.op('not', c); cnt[s][c2] += m; self._note(c2, s, 'not(%s)' % self.rep[c])
            for i in range(1, s - 1):
                for ca, ma in list(cnt[i].items()):
                    for cb, mb in list(cnt[s - 1 - i].items()):
                        for nm in ('and', 'or'):
                            c2 = self.op(nm, ca, cb); cnt[s][c2] += ma * mb
                            self._note(c2, s, '%s(%s,%s)' % (nm, self.rep[ca], self.rep[cb]))
            for kind, level in self.kinds:
                if s == 3:
                    for form in (M.TM, M.TT):
                        c2 = self.op((kind, level, form)); cnt[s][c2] += 1; self._note(c2, s, self._src_box(kind, level, form, -1))
                if s >= 4:
                    for ca, ma in list(cnt[s - 3].items()):
                        q = self.restrict(ca)
                        c2 = self.op((kind, level, M.TL), q); cnt[s][c2] += ma
                        self._note(c2, s, self._src_box(kind, level, M.TL, q).replace('THEM(^%s)' % self.rep[q], 'THEM(^%s)' % self.rep[ca]))
        self.a = np.array([0] + [sum(cnt[s].values()) for s in range(1, n + 1)], float)
        K = len(self.funcs)
        mu = np.zeros(K); bits_min = np.full(K, np.inf)
        for s in range(1, n + 1):
            b = np.log2(self.a[s]) + 2 * np.log2(s) + 1
            for c, m in cnt[s].items():
                mu[c] += m * 2.0 ** (-b); bits_min[c] = min(bits_min[c], b)
        self.mu_canon = mu; self.bits_canon = bits_min
        self.cnt_by_size = cnt
        self.count_canon = np.zeros(K)
        for s in range(1, n + 1):
            for c, m in cnt[s].items():
                self.count_canon[c] += m
        self.n_programs = int(self.a.sum())

    def tags(self, c):
        return sorted({self.atoms[a][1] for a in self.funcs[c][0] if self.atoms[a][0] in (KA, KV)})


class Lang:
    """Arrays for the evaluator.  Base types = canons with positive mass (programs of size <= n).
    Probe nodes = the closure of quoted canons plus ^C and ^D."""

    def __init__(self, n=6, hooks=True):
        L = HookedModalLanguage(n, hooks=hooks)
        self.L = L
        live = [c for c in range(len(L.funcs)) if L.mu_canon[c] > 0]
        self.base = np.array(live, np.int64)                 # base type index -> canon
        self.bidx = {c: i for i, c in enumerate(live)}
        self.mu = L.mu_canon[live] / L.mu_canon[live].sum()
        self.names = [L.rep[c] for c in live]
        cC, cD = L.op('C'), L.op('D')
        probes = [cC, cD]
        seen = set(probes)
        stack = [c for c in range(len(L.funcs))]
        args = set()
        for c in range(len(L.funcs)):
            for a in L.funcs[c][0]:
                at = L.atoms[a]
                if at[0] in (0, 1) and at[2] == M.TL:
                    args.add(at[3])
        frontier = list(args)
        while frontier:
            c = frontier.pop()
            if c in seen:
                continue
            seen.add(c); probes.append(c)
            for a in L.funcs[c][0]:
                at = L.atoms[a]
                if at[0] in (0, 1) and at[2] == M.TL and at[3] not in seen:
                    frontier.append(at[3])
        self.probes = probes
        self.pidx = {c: i for i, c in enumerate(probes)}
        P = len(probes)
        self.P = P
        # probe arrays (probes have no hook atoms)
        KMAX = 8
        self.p_nat = np.zeros(P, np.int64); self.p_kind = np.zeros((P, KMAX), np.int64); self.p_lev = np.zeros((P, KMAX), np.int64)
        self.p_form = np.zeros((P, KMAX), np.int64); self.p_arg = np.zeros((P, KMAX), np.int64); self.p_tt = np.zeros(P, np.int64)
        for i, c in enumerate(probes):
            self._fill(c, i, self.p_nat, self.p_kind, self.p_lev, self.p_form, self.p_arg, self.p_tt, probe=True)
        B = len(live)
        self.b_nat = np.zeros(B, np.int64); self.b_kind = np.zeros((B, KMAX), np.int64); self.b_lev = np.zeros((B, KMAX), np.int64)
        self.b_form = np.zeros((B, KMAX), np.int64); self.b_arg = np.zeros((B, KMAX), np.int64); self.b_tt = np.zeros(B, np.int64)
        self.b_tags = np.zeros(B, np.int64)
        for i, c in enumerate(live):
            self._fill(c, i, self.b_nat, self.b_kind, self.b_lev, self.b_form, self.b_arg, self.b_tt)
            for t in L.tags(c):
                self.b_tags[i] |= 1 << t
        self.b_restrict = np.array([self.bidx.get(L.restrict(c), -1) for c in live], np.int64)
        self.iC = self.pidx[cC]; self.iD = self.pidx[cD]
        self.FB = self.bidx[L.op((0, 0, M.TM))]
        self.bD = self.bidx[cD]; self.bC = self.bidx[cC]

    def _fill(self, c, i, nat, kind, lev, form, arg, tt, probe=False):
        L = self.L
        atoms, t, k = L.funcs[c]
        nat[i] = k; tt[i] = t
        for j, a in enumerate(atoms):
            at = L.atoms[a]
            if at[0] in (KA, KV):
                assert not probe
                kind[i, j] = at[0]; lev[i, j] = at[1]; form[i, j] = -1; arg[i, j] = -1
            else:
                kind[i, j] = at[0]; lev[i, j] = at[1]; form[i, j] = at[2]
                arg[i, j] = self.pidx[at[3]] if at[2] == M.TL else -1

    def arrays(self):
        return (self.p_nat, self.p_kind, self.p_lev, self.p_form, self.p_arg, self.p_tt,
                self.b_nat, self.b_kind, self.b_lev, self.b_form, self.b_arg, self.b_tt)


# ------------------------------------------------------------------ fills and specs
def fcode(action, tag, scope, origin, key):
    return 1 + (action | (tag << 1) | (scope << 2) | (origin << 4) | (key << 6))


@njit(cache=True)
def f_action(f): return (f - 1) & 1
@njit(cache=True)
def f_tag(f): return ((f - 1) >> 1) & 1
@njit(cache=True)
def f_scope(f): return ((f - 1) >> 2) & 3
@njit(cache=True)
def f_origin(f): return ((f - 1) >> 4) & 3
@njit(cache=True)
def f_key(f): return (f - 1) >> 6


@njit(cache=True)
def spec_of(fills, nf, tags, active, recency, ctx):
    """Spec (see module doc) of a holder with fills[0:nf] (oldest first) in a match whose partner lineage is ctx
    (-1: no lineage, a quoted probe or a stranger).  active[scope, origin]: fill applies only if active.  recency: 1 =
    the most recent applicable fill wins whatever its scope; 0 = the most specific scope wins, ties by recency
    (behaviour > history > role > none)."""
    out = 0
    for t in range(2):
        if not (tags >> t) & 1:
            continue
        app = 0; val = 0
        for beta in range(8):
            best = -1; bestp = -1
            for j in range(nf - 1, -1, -1):
                f = fills[j]
                if f_tag(f) != t:
                    continue
                sc = f_scope(f)
                if not active[sc, f_origin(f)]:
                    continue
                ok = False
                if sc == 0 or sc == 1:
                    ok = True
                elif sc == 2:
                    ok = ctx >= 0 and f_key(f) == ctx
                else:
                    ok = f_key(f) == beta
                if not ok:
                    continue
                if recency == 1:
                    best = j; break
                pr = 3 if sc == 3 else (2 if sc == 2 else (1 if sc == 1 else 0))
                if pr > bestp:
                    bestp = pr; best = j
            if best >= 0:
                app |= 1 << beta
                if f_action(fills[best]) == 1:
                    val |= 1 << beta
        out |= (app | (val << 8)) << (16 * t)
    return out


# ------------------------------------------------------------------ the evaluator
@njit(cache=True)
def eval_match(p_nat, p_kind, p_lev, p_form, p_arg, p_tt, b_nat, b_kind, b_lev, b_form, b_arg, b_tt,
               iC, iD, bx, sx0, sx1, sx2, by, sy0, sy1, sy2):
    """Stable plays of x (base bx) and y (base by).  sx0: x's spec against probes (no lineage), sx1: against y,
    sx2: against a copy of itself; likewise y.  Returns (x's action vs y, y's action vs x, beta of y as read by x,
    beta of x as read by y), actions 1 = C; (-1, -1, 0, 0) if the chain did not stabilize (never observed)."""
    P = p_nat.shape[0]
    K = P + 2
    X = P; Y = P + 1
    hc = np.ones((2, K, K), np.bool_)
    hd = np.ones((2, K, K), np.bool_)
    val = np.zeros((K, K), np.int8)
    for n in range(200):
        for p in range(K):
            for q in range(K):
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
                        bs = bx; sp = sx0 if q < P else (sx1 if q == Y else sx2)
                    else:
                        bs = by; sp = sy0 if q < P else (sy1 if q == X else sy2)
                    beta = -1
                    idx = 0
                    for j in range(b_nat[bs]):
                        kd = b_kind[bs, j]
                        if kd >= 2:
                            if beta < 0:
                                beta = (1 if hc[0, q, iC] else 0) | ((1 if hc[0, q, iD] else 0) << 1) | ((1 if hc[0, q, p] else 0) << 2)
                            t = b_lev[bs, j]
                            m = (sp >> (16 * t)) & 0xFFFF
                            if kd == 2:
                                bb = (m >> beta) & 1
                            else:
                                bb = (m >> (8 + beta)) & 1
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
            for p in range(K):
                for q in range(K):
                    c = val[p, q] == 1
                    if hc[L, p, q] and not c:
                        hc[L, p, q] = False; changed = True
                    if hd[L, p, q] and c:
                        hd[L, p, q] = False; changed = True
        if not changed and n >= 2:
            bx_ = (1 if hc[0, Y, iC] else 0) | ((1 if hc[0, Y, iD] else 0) << 1) | ((1 if hc[0, Y, X] else 0) << 2)
            by_ = (1 if hc[0, X, iC] else 0) | ((1 if hc[0, X, iD] else 0) << 1) | ((1 if hc[0, X, Y] else 0) << 2)
            return val[X, Y], val[Y, X], bx_, by_
    return -1, -1, 0, 0

# ------------------------------------------------------------------ types and the match cache
# Type table T = (Tb base, Tl lineage, Tf fills (cap, 4), Tn nfills, Tg tags, Ts0 spec vs no lineage, Tss spec vs own
# lineage, Th has an active history fill on a carried tag, Tgent gentle (-1 unknown), gcount (individuals of the type
# alive), meta [number of ids ever used, number of free ids], freelist).  A type whose count falls to 0 is removed from
# tdict and its id recycled (live types never exceed the population plus a few in flight).  tdict: (base<<32|lin,
# f0|f1<<21|f2<<42, f3) -> type.  ev: spec key -> match code, code = ax | ay << 1 | beta_x << 2 | beta_y << 5 (beta_x:
# the class of y as read by x).
TCAP = 200_000


def new_tables(cap=TCAP):
    T = (np.zeros(cap, np.int64), np.zeros(cap, np.int64), np.zeros((cap, 4), np.int64), np.zeros(cap, np.int64),
         np.zeros(cap, np.int64), np.zeros(cap, np.int64), np.zeros(cap, np.int64), np.zeros(cap, np.bool_),
         -np.ones(cap, np.int8), np.zeros(cap, np.int64), np.zeros(2, np.int64), np.zeros(cap, np.int64))
    tdict = Dict.empty(key_type=types.UniTuple(types.int64, 3), value_type=types.int64)
    ev = Dict.empty(key_type=types.UniTuple(types.int64, 4), value_type=types.int64)
    return T, tdict, ev


@njit(cache=True)
def _hashist(f, nf, tags, active):
    for j in range(nf):
        if f_scope(f[j]) == 2 and active[2, f_origin(f[j])] and (tags >> f_tag(f[j])) & 1:
            return True
    return False


@njit(cache=True)
def _tkey(base, lin, g):
    return (np.int64((base << 32) | lin), np.int64(g[0] | (g[1] << 21) | (g[2] << 42)), np.int64(g[3]))


@njit(cache=True)
def get_type(T, tdict, b_tags, active, recency, base, lin, f, nf):
    """The type (base, lin, f[:nf]); created (or an id recycled) if new; -1 if the table is full."""
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    g = np.zeros(4, np.int64)
    for j in range(nf):
        g[j] = f[j]
    key = _tkey(base, lin, g)
    if key in tdict:
        return tdict[key]
    if meta[1] > 0:
        meta[1] -= 1
        t = freel[meta[1]]
    else:
        t = meta[0]
        if t >= Tb.shape[0]:
            return -1
        meta[0] = t + 1
    Tb[t] = base; Tl[t] = lin; Tn[t] = nf
    for j in range(4):
        Tf[t, j] = g[j]
    tg = b_tags[base]
    Tg[t] = tg
    Ts0[t] = spec_of(g, nf, tg, active, recency, -1)
    Tss[t] = spec_of(g, nf, tg, active, recency, lin)
    Th[t] = _hashist(g, nf, tg, active)
    Tgent[t] = -1; gcount[t] = 0
    tdict[key] = t
    return t


@njit(cache=True)
def free_type(T, tdict, t):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    key = _tkey(Tb[t], Tl[t], Tf[t])
    if key in tdict and tdict[key] == t:
        tdict.pop(key)
        freel[meta[1]] = t; meta[1] += 1


@njit(cache=True)
def spec_ctx(T, active, recency, t, l):
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    if not Th[t]:
        return Ts0[t]
    if l == Tl[t]:
        return Tss[t]
    return spec_of(Tf[t], Tn[t], Tg[t], active, recency, l)


@njit(cache=True)
def swap_code(c):
    ax = c & 1; ay = (c >> 1) & 1; bx = (c >> 2) & 7; by = (c >> 5) & 7
    return ay | (ax << 1) | (by << 2) | (bx << 5)


@njit(cache=True)
def eval_code(LA, ev, iC, iD, bx, sx0, sx1, sx2, by, sy0, sy1, sy2):
    key = (np.int64((bx << 32) | sx0), np.int64((sx1 << 32) | sx2), np.int64((by << 32) | sy0), np.int64((sy1 << 32) | sy2))
    if key in ev:
        return ev[key]
    p_nat, p_kind, p_lev, p_form, p_arg, p_tt, b_nat, b_kind, b_lev, b_form, b_arg, b_tt = LA
    ax, ay, bbx, bby = eval_match(p_nat, p_kind, p_lev, p_form, p_arg, p_tt, b_nat, b_kind, b_lev, b_form, b_arg, b_tt,
                                  iC, iD, bx, sx0, sx1, sx2, by, sy0, sy1, sy2)
    code = np.int64(ax | (ay << 1) | (bbx << 2) | (bby << 5))
    ev[key] = code
    key2 = (np.int64((by << 32) | sy0), np.int64((sy1 << 32) | sy2), np.int64((bx << 32) | sx0), np.int64((sx1 << 32) | sx2))
    ev[key2] = swap_code(code)
    return code


@njit(cache=True)
def match(T, LA, ev, iC, iD, active, recency, a, b):
    """Match code of type a against type b under their fills and lineages."""
    Tb, Tl, Tf, Tn, Tg, Ts0, Tss, Th, Tgent, gcount, meta, freel = T
    return eval_code(LA, ev, iC, iD, Tb[a], Ts0[a], spec_ctx(T, active, recency, a, Tl[b]), Tss[a],
                     Tb[b], Ts0[b], spec_ctx(T, active, recency, b, Tl[a]), Tss[b])

@njit(cache=True)
def write_fill(f, nf, newf, out):
    """out <- f with newf written (in-place update if (tag, scope, key) matches, else append, FIFO beyond 4).
    Returns (new nf, evicted, in-place)."""
    mask = ~np.int64(1 | (3 << 4))
    nk = (newf - 1) & mask
    hit = -1
    for j in range(nf):
        if ((f[j] - 1) & mask) == nk:
            hit = j; break
    m = 0
    for j in range(nf):
        if j != hit:
            out[m] = f[j]; m += 1
    ev_ = 0
    if hit < 0 and nf == 4:
        for j in range(3):
            out[j] = out[j + 1]
        m = 3; ev_ = 1
    out[m] = newf; m += 1
    for j in range(m, 4):
        out[j] = 0
    return m, ev_, 1 if hit >= 0 else 0


@njit(cache=True)
def select_idx(f, nf, tags, active, recency, ctx, beta, t, need_active):
    """Index of the fill selected for tag t at class beta in context ctx (need_active=False: applicability only,
    returns the first applicable fill from the most recent, ignoring activity)."""
    if not (tags >> t) & 1:
        return -1
    best = -1; bestp = -1
    for j in range(nf - 1, -1, -1):
        g = f[j]
        if f_tag(g) != t:
            continue
        sc = f_scope(g)
        if need_active and not active[sc, f_origin(g)]:
            continue
        ok = False
        if sc == 0 or sc == 1:
            ok = True
        elif sc == 2:
            ok = ctx >= 0 and f_key(g) == ctx
        else:
            ok = f_key(g) == beta
        if not ok:
            continue
        if recency == 1 or not need_active:
            return j
        pr = 3 if sc == 3 else (2 if sc == 2 else (1 if sc == 1 else 0))
        if pr > bestp:
            bestp = pr; best = j
    return best
