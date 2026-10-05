"""GLS+Def: a cut-free G3-style sequent calculus for GL with definitional constants P_{xy}, on the DSL's frozen
syntax (specs/2026-10-05-proof-length.md, Part A; notes/proof-length.md §1).

Programs are parsed from the evaluator's source syntax (src/conj4.py's parser: C, D, not, and, or, BOX[k](App),
BOXD[k](App), App = THEM(ME) | THEM(THEM) | THEM(^A)).  P_{xy} is "x plays C against y"; its definition is x's source
read against y:
    BOX(THEM(ME)) -> []P_{yx},  BOX(THEM(THEM)) -> []P_{yy},  BOX(THEM(^A)) -> []P_{yA},
    BOXD(App) -> []~P_App,      BOXk(App) -> [](~[]^k F -> P_App),  BOXDk(App) -> [](~[]^k F -> ~P_App).

Derivation size = number of sequents.  Provability: `Oracle` (the standard terminating decision procedure).
Exact minimal (size, Loeb count): `MinSearch` (iterative deepening on size with a transposition table of exact values
and lower bounds, on the normal-form graph of notes/proof-length.md, unprovable sequents pruned), which is the
production method; `Graph` (Knuth's generalized Dijkstra over the full backward-reachable AND-OR graph) is the
reference it is tested against.  A capped search reports an upper bound, flagged uncertified.
"""
import heapq, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from conj4 import parse, src as psrc, size as psize

# formula kinds
FP, FBOT, FTOP, FNOT, FAND, FOR, FIMP, FBOX = range(8)
KNAME = {FP: 'P', FBOT: 'F', FTOP: 'T', FNOT: '~', FAND: '&', FOR: '|', FIMP: '->', FBOX: '[]'}


class Theory:
    """Program table, formula table and definitions."""

    def __init__(self):
        self.progs = []          # id -> parsed tree
        self.prog_id = {}        # source -> id
        self.forms = []          # id -> tuple
        self.form_id = {}
        self.defn = {}           # P formula id -> definition formula id
        self.BOT = self.f((FBOT,))
        self.TOP = self.f((FTOP,))

    # -- programs ------------------------------------------------------------
    def prog(self, s):
        t = parse(s) if isinstance(s, str) else s
        key = psrc(t)
        i = self.prog_id.get(key)
        if i is None:
            i = len(self.progs); self.prog_id[key] = i; self.progs.append(t)
        return i

    # -- formulas ------------------------------------------------------------
    def f(self, t):
        i = self.form_id.get(t)
        if i is None:
            i = len(self.forms); self.form_id[t] = i; self.forms.append(t)
        return i

    def P(self, x, y): return self.f((FP, x, y))
    def neg(self, a): return self.f((FNOT, a))
    def box(self, a): return self.f((FBOX, a))
    def imp(self, a, b): return self.f((FIMP, a, b))

    def boxk_bot(self, k):
        a = self.BOT
        for _ in range(k): a = self.box(a)
        return a

    def con_guard(self, k, s):
        """~[]^k F -> s  (k >= 1)."""
        return self.imp(self.neg(self.boxk_bot(k)), s)

    def phi(self, x, y):
        """Definition of P_{xy}: x's source read against y."""
        def tr(t):
            k = t[0]
            if k == 'C': return self.TOP
            if k == 'D': return self.BOT
            if k == 'not': return self.neg(tr(t[1]))
            if k == 'and': return self.f((FAND, tr(t[1]), tr(t[2])))
            if k == 'or': return self.f((FOR, tr(t[1]), tr(t[2])))
            _, kind, lev, form, arg = t
            if form == 'ME': p, q = y, x
            elif form == 'THEM': p, q = y, y
            else: p, q = y, self.prog(arg)
            s = self.P(p, q)
            if kind: s = self.neg(s)
            if lev: s = self.con_guard(lev, s)
            return self.box(s)
        return tr(self.progs[x])

    def unfold(self, pf):
        d = self.defn.get(pf)
        if d is None:
            _, x, y = self.forms[pf]
            d = self.phi(x, y); self.defn[pf] = d
        return d

    # -- printing ------------------------------------------------------------
    def show(self, i, names=None):
        t = self.forms[i]; k = t[0]
        if k == FP:
            nm = names or {}
            return 'P[%s,%s]' % (nm.get(t[1], 'p%d' % t[1]), nm.get(t[2], 'p%d' % t[2]))
        if k == FBOT: return 'F'
        if k == FTOP: return 'T'
        if k == FNOT: return '~' + self.show(t[1], names)
        if k == FBOX: return '[]' + self.show(t[1], names)
        return '(%s %s %s)' % (self.show(t[1], names), KNAME[k], self.show(t[2], names))

    def symbols(self, i):
        """Formula-symbol size (tree)."""
        t = self.forms[i]
        return 1 + sum(self.symbols(a) for a in t[1:]) if t[0] not in (FP, FBOT, FTOP) else 1

    def show_seq(self, s, names=None):
        L, R = s
        return '%s |- %s' % (', '.join(sorted(self.show(a, names) for a in L)), ', '.join(sorted(self.show(a, names) for a in R)))


# ---------------------------------------------------------------------------- the calculus
def is_axiom(th, L, R):
    F = th.forms
    if th.BOT in L or th.TOP in R:
        return True
    for a in L:
        if a in R and F[a][0] in (FP, FBOX):
            return True
    return False


def single_premise(th, seq):
    """Canonical (smallest-id) single-premise propositional formula of the sequent: ~A either side, A&B left,
    A|B right, A->B right.  Returns (side, formula) or None."""
    L, R = seq
    F = th.forms
    best = None
    for a in L:
        if F[a][0] in (FNOT, FAND) and (best is None or a < best[1]): best = (0, a)
    for a in R:
        if F[a][0] in (FNOT, FOR, FIMP) and (best is None or a < best[1]): best = (1, a)
    return best


def expand_nf(th, seq):
    """Normal-form expansion (exact for minimal size and for Loeb count; notes §1 'Normal form'): if the sequent has a
    single-premise propositional formula f (canonical choice), the only options are to decompose f now or to delete
    it (weight 0: f is then unused, and strengthening is exact for an unused compound formula).  Otherwise every rule."""
    sp = single_premise(th, seq)
    if sp is None:
        return expand(th, seq)
    L, R = seq
    side, a = sp
    t = th.forms[a]; k = t[0]
    if side == 0:
        dele = ((L - {a}, R),)
        dec = (((L - {a}), R | {t[1]}),) if k == FNOT else (((L - {a}) | {t[1], t[2]}, R),)
        lab = '~L' if k == FNOT else '&L'
    else:
        dele = ((L, R - {a}),)
        if k == FNOT: dec = ((L | {t[1]}, R - {a}),); lab = '~R'
        elif k == FOR: dec = ((L, (R - {a}) | {t[1], t[2]}),); lab = '|R'
        else: dec = ((L | {t[1]}, (R - {a}) | {t[2]}),); lab = '->R'
    return [(dec, 0, lab), (dele, 0, 'Del')]


def expand(th, seq):
    """All backward rule instances: list of (premises tuple, is_glr, label)."""
    L, R = seq
    F = th.forms
    out = []
    for a in L:
        t = F[a]; k = t[0]
        if k == FNOT:
            out.append(((((L - {a}), R | {t[1]}),), 0, '~L'))
        elif k == FAND:
            out.append(((((L - {a}) | {t[1], t[2]}, R),), 0, '&L'))
        elif k == FOR:
            Lr = L - {a}
            out.append((((Lr | {t[1]}, R), (Lr | {t[2]}, R)), 0, '|L'))
        elif k == FIMP:
            Lr = L - {a}
            out.append((((Lr, R | {t[1]}), (Lr | {t[2]}, R)), 0, '->L'))
        elif k == FP:
            out.append(((((L - {a}) | {th.unfold(a)}, R),), 0, 'UnfL'))
    boxes = None
    for a in R:
        t = F[a]; k = t[0]
        if k == FNOT:
            out.append((((L | {t[1]}, R - {a}),), 0, '~R'))
        elif k == FAND:
            Rr = R - {a}
            out.append((((L, Rr | {t[1]}), (L, Rr | {t[2]})), 0, '&R'))
        elif k == FOR:
            out.append((((L, (R - {a}) | {t[1], t[2]}),), 0, '|R'))
        elif k == FIMP:
            out.append((((L | {t[1]}, (R - {a}) | {t[2]}),), 0, '->R'))
        elif k == FP:
            out.append((((L, (R - {a}) | {th.unfold(a)}),), 0, 'UnfR'))
        elif k == FBOX:
            if boxes is None:
                boxes = frozenset(b for b in L if F[b][0] == FBOX)
                gam = frozenset(F[b][1] for b in boxes)
            out.append(((((boxes | gam | {a}), frozenset([t[1]])),), 1, 'GLR'))
    return out


def cut_closure(th, seqs):
    """Analytic cut formulas for a set of root sequents (specs/2026-10-05-k-at-n8.md, lemma sharing (a)): every boxed
    formula []B reachable from the roots by subformulas and unfolding, and its content B.  Finite."""
    F = th.forms
    seen = set(); stack = [a for L, R in seqs for a in list(L) + list(R)]
    boxes = set()
    while stack:
        a = stack.pop()
        if a in seen: continue
        seen.add(a); t = F[a]; k = t[0]
        if k == FBOX:
            boxes.add(a); stack.append(t[1])
        elif k == FP: stack.append(th.unfold(a))
        elif k == FNOT: stack.append(t[1])
        elif k in (FAND, FOR, FIMP): stack += [t[1], t[2]]
    out = set(boxes) | {F[b][1] for b in boxes}
    return sorted(out)


def expand_cut(th, seq, cuts, nf=True):
    """Backward rule instances with analytic cut: the normal-form (or all-orders) instances, plus, for every cut
    formula A not already in the sequent, Cut: (L, R + A) and (L + A, R).  The normal form stays exact with cut (cut
    shares its context like any two-premise rule, so the permutation argument of notes/proof-length.md §1 applies)."""
    out = list(expand_nf(th, seq) if nf else expand(th, seq))
    if nf and single_premise(th, seq) is not None:
        return out
    L, R = seq
    for A in cuts:
        if A in L or A in R: continue
        out.append((((L, R | {A}), (L | {A}, R)), 0, 'Cut'))
    return out


class Oracle:
    """GL+Def provability by the standard terminating decision procedure: invertible rules (every propositional
    rule and unfolding) applied eagerly in a fixed order, then an OR over GLR on each right box not already on the
    left (a box on both sides is an initial sequent).  Left boxes strictly grow along GLR, the closure is finite, so
    the search terminates.  Memoized on sequents; cross-checked against the all-orders graph."""

    def __init__(self, th):
        self.th = th
        self.memo = {}

    def prov(self, seq):
        L, R = frozenset(seq[0]), frozenset(seq[1])
        key = (L, R)
        r = self.memo.get(key)
        if r is not None:
            return r
        self.memo[key] = False            # loop guard (cannot recur: left boxes grow along GLR)
        r = self._prov(L, R)
        self.memo[key] = r
        return r

    def _prov(self, L, R):
        th = self.th; F = th.forms
        if is_axiom(th, L, R):
            return True
        for a in sorted(L):
            t = F[a]; k = t[0]
            if k == FNOT: return self.prov((L - {a}, R | {t[1]}))
            if k == FAND: return self.prov(((L - {a}) | {t[1], t[2]}, R))
            if k == FOR: return self.prov(((L - {a}) | {t[1]}, R)) and self.prov(((L - {a}) | {t[2]}, R))
            if k == FIMP: return self.prov((L - {a}, R | {t[1]})) and self.prov(((L - {a}) | {t[2]}, R))
            if k == FP: return self.prov(((L - {a}) | {th.unfold(a)}, R))
        for a in sorted(R):
            t = F[a]; k = t[0]
            if k == FNOT: return self.prov((L | {t[1]}, R - {a}))
            if k == FAND: return self.prov((L, (R - {a}) | {t[1]})) and self.prov((L, (R - {a}) | {t[2]}))
            if k == FOR: return self.prov((L, (R - {a}) | {t[1], t[2]}))
            if k == FIMP: return self.prov((L | {t[1]}, (R - {a}) | {t[2]}))
            if k == FP: return self.prov((L, (R - {a}) | {th.unfold(a)}))
        boxes = frozenset(b for b in L if F[b][0] == FBOX)
        gam = frozenset(F[b][1] for b in boxes)
        for a in sorted(R):
            if F[a][0] == FBOX and a not in L:
                if self.prov((boxes | gam | {a}, frozenset([F[a][1]]))):
                    return True
        return False


class Graph:
    """Backward-reachable AND-OR graph from a set of roots, and exact minimal (size, Loeb) costs."""

    def __init__(self, th, roots, cap=2_000_000, time_cap=None, oracle=None, nf=False, cuts=None):
        self.th = th
        self.oracle = oracle
        self.nf = nf
        self.cuts = cuts
        self.roots = [r for r in roots]
        self.id = {}
        self.seqs = []
        self.rules = []          # rule idx -> (concl, premises tuple of ids, glr, label)
        self.users = []          # seq id -> list of rule idx using it as a premise
        self.axiom = []
        self.complete = True
        t0 = time.time()
        stack = []
        for r in self.roots:
            if oracle is None or oracle.prov(r):
                self._add(r, stack)
        while stack:
            s = stack.pop()
            seq = self.seqs[s]
            if self.axiom[s]:
                continue
            rules = (expand_cut(th, seq, self.cuts, self.nf) if self.cuts is not None else
                     (expand_nf(th, seq) if self.nf else expand(th, seq)))
            for prem, glr, lab in rules:
                if self.oracle is not None and not all(self.oracle.prov(p) for p in prem):
                    continue          # a derivation never contains an unprovable sequent: exactness is kept
                pids = tuple(self._add(p, stack) for p in prem)
                ri = len(self.rules)
                self.rules.append((s, pids, glr, lab))
                for p in set(pids):
                    self.users[p].append(ri)
            if len(self.seqs) > cap or (time_cap and time.time() - t0 > time_cap):
                self.complete = False
                break
        self.build_time = time.time() - t0
        if self.complete:
            self._knuth()

    def _add(self, seq, stack):
        seq = (frozenset(seq[0]), frozenset(seq[1]))
        i = self.id.get(seq)
        if i is None:
            i = len(self.seqs); self.id[seq] = i; self.seqs.append(seq); self.users.append([])
            self.axiom.append(is_axiom(self.th, *seq))
            stack.append(i)
        return i

    def _knuth(self):
        n = len(self.seqs)
        INF = (1 << 60, 0)
        self.cost = [INF] * n
        self.best = [None] * n         # rule idx or -1 for axiom
        done = [False] * n
        rem = [len(r[1]) for r in self.rules]
        acc = [[0, 0] for _ in self.rules]
        h = []
        for i in range(n):
            if self.axiom[i]:
                self.cost[i] = (1, 0); self.best[i] = -1; heapq.heappush(h, (1, 0, i))
        while h:
            c0, c1, i = heapq.heappop(h)
            if done[i] or (c0, c1) != self.cost[i]:
                continue
            done[i] = True
            for ri in self.users[i]:
                concl, pids, glr, lab = self.rules[ri]
                if done[concl]:
                    continue
                m = pids.count(i)
                acc[ri][0] += m * c0; acc[ri][1] += m * c1; rem[ri] -= m
                if rem[ri] == 0:
                    cand = ((0 if lab == 'Del' else 1) + acc[ri][0], glr + acc[ri][1])
                    if cand < self.cost[concl]:
                        self.cost[concl] = cand; self.best[concl] = ri
                        heapq.heappush(h, (cand[0], cand[1], concl))

    def result(self, root):
        """(size, loeb) or None if not a theorem; raises if the graph is incomplete."""
        assert self.complete
        i = self.id.get((frozenset(root[0]), frozenset(root[1])))
        if i is None:
            return None
        c = self.cost[i]
        return None if c[0] >= (1 << 60) else c

    def derivation(self, root):
        """Minimal derivation as nested (seq id, label, children)."""
        i = self.id[(frozenset(root[0]), frozenset(root[1]))]
        def rec(i):
            ri = self.best[i]
            if ri == -1:
                return (i, 'Ax', [])
            concl, pids, glr, lab = self.rules[ri]
            return (i, lab, [rec(p) for p in pids])
        return rec(i)

    def stats(self, root):
        d = self.derivation(root)
        seen = set(); size = [0]; lam = [0]; depth = [0]; glr_depth = [0]
        def walk(t, dp, gd):
            i, lab, ch = t
            if lab == 'Del':
                walk(ch[0], dp, gd); return
            size[0] += 1; seen.add(i)
            if lab == 'GLR': lam[0] += 1; gd += 1
            depth[0] = max(depth[0], dp); glr_depth[0] = max(glr_depth[0], gd)
            for c in ch: walk(c, dp + 1, gd)
        walk(d, 1, 0)
        return dict(size=size[0], loeb=lam[0], dag=len(seen), height=depth[0], loeb_depth=glr_depth[0])

    def render(self, root, names=None):
        d = self.derivation(root)
        lines = []
        def walk(t, ind):
            i, lab, ch = t
            if lab == 'Del':
                walk(ch[0], ind); return
            lines.append('%s%s   [%s]' % ('  ' * ind, self.th.show_seq(self.seqs[i], names), lab))
            for c in ch: walk(c, ind + 1)
        walk(d, 0)
        return '\n'.join(lines)


# ---------------------------------------------------------------------------- roots
def roots_for(th, x, y):
    """The four provability roots for the pair (x, y): (name, sequent)."""
    p = th.P(x, y)
    nb = th.neg(th.box(th.BOT))
    return [('C0', (frozenset(), frozenset([p]))),
            ('D0', (frozenset([p]), frozenset())),
            ('C1', (frozenset(), frozenset([th.imp(nb, p)]))),
            ('D1', (frozenset(), frozenset([th.imp(nb, th.neg(p))])))]


def atom_formulas(th, x, y):
    """x's box-atom formulas against y, in source order, with their (kind, level, target pair)."""
    out = []
    def walk(t):
        k = t[0]
        if k == 'not': walk(t[1])
        elif k in ('and', 'or'): walk(t[1]); walk(t[2])
        elif k == 'box':
            _, kind, lev, form, arg = t
            if form == 'ME': p, q = y, x
            elif form == 'THEM': p, q = y, y
            else: p, q = y, th.prog(arg)
            s = th.P(p, q)
            if kind: s = th.neg(s)
            if lev: s = th.con_guard(lev, s)
            out.append((th.box(s), kind, lev, (p, q)))
    walk(th.progs[x])
    return out


def nesting_depth(t):
    k = t[0]
    if k in ('C', 'D'): return 0
    if k == 'not': return nesting_depth(t[1])
    if k in ('and', 'or'): return max(nesting_depth(t[1]), nesting_depth(t[2]))
    return 1 + (nesting_depth(t[4]) if t[3] == 'ARG' else 0)


def prove_pair(th, x, y, extra=(), cap=2_000_000, time_cap=None, oracle=None, nf=False):
    """Exact minima for the pair's four roots plus `extra` roots (list of (name, sequent)).  With an oracle the graph
    is built over provable sequents only (exact; much smaller)."""
    R = roots_for(th, x, y) + list(extra)
    g = Graph(th, [s for _, s in R], cap=cap, time_cap=time_cap, oracle=oracle, nf=nf)
    out = dict(n_seqs=len(g.seqs), n_rules=len(g.rules), complete=g.complete, build_s=g.build_time)
    if g.complete:
        for nm, s in R:
            c = g.result(s)
            out[nm] = None if c is None else dict(c=c, **g.stats(s))
    return out, g


# ---------------------------------------------------------------------------- audit against the evaluator
def box_tables(n):
    """The modal language L_n, its stable plays and the four box-fact tables at the stable world
    (bounded._evaluate_gated with every gate open is modal._evaluate plus hc/hd)."""
    import numpy as np
    import modal as M
    from bounded import _evaluate_gated
    L = M.ModalLanguage(n)
    arr = L.arrays()
    K = len(arr[0])
    val, w, last, hc, hd = _evaluate_gated(*arr, np.ones((K, K), np.bool_), 2, 300)
    assert w >= 0
    v2, w2 = M.evaluate(L)
    assert (v2 == val).all()
    return L, val, hc, hd


def audit_pair(th, pid, c, d, val, hc, hd, cap=2_000_000, time_cap=None, oracle=None, nf=False):
    """Compare GLS+Def provability of the four roots of (c, d) with the tables.  pid: canon id -> program id."""
    o, g = prove_pair(th, pid[c], pid[d], cap=cap, time_cap=time_cap, oracle=oracle, nf=nf)
    if not o['complete']:
        return o, None
    want = dict(C0=bool(hc[0, c, d]), D0=bool(hd[0, c, d]), C1=bool(hc[1, c, d]), D1=bool(hd[1, c, d]))
    bad = [k for k in want if want[k] != (o[k] is not None)]
    return o, bad


# ---------------------------------------------------------------------------- iterative deepening (the spec's method)
class Abort(Exception):
    pass


class MinSearch:
    """Exact minimal (size, Loeb) by iterative deepening on size with a transposition table of exact values and lower
    bounds (depth-first branch and bound on the normal-form AND-OR graph, unprovable sequents pruned by the oracle).
    Certifies minimality: a value is stored only when every other rule's lower bound exceeds it or it was solved
    exactly.  The memo is shared across roots (a sequent's minimum is context-free).  `cap` bounds node expansions
    per root."""

    INF = 1 << 30

    def __init__(self, th, oracle=None, cap=3_000_000, cuts=None):
        self.th = th
        self.cuts = cuts          # None: cut-free GLS+Def; a list: analytic cut on these formulas
        self.oracle = oracle or Oracle(th)
        self.exact = {}          # seq -> (size, loeb, label, premises)
        self.lb = {}
        self.cap = cap
        self.count = 0

    def _lbv(self, p):
        e = self.exact.get(p)
        return e[0] if e is not None else self.lb.get(p, 1)

    def solve(self, S, bound):
        e = self.exact.get(S)
        if e is not None:
            return e if e[0] <= bound else None
        if self.lb.get(S, 1) > bound:
            return None
        th = self.th
        if is_axiom(th, *S):
            e = (1, 0, 'Ax', ()); self.exact[S] = e
            return e if bound >= 1 else None
        if not self.oracle.prov(S):
            self.lb[S] = self.INF
            return None
        self.count += 1
        if self.count > self.cap:
            raise Abort()
        best = None; newlb = self.INF
        for prem, glr, lab in (expand_nf(th, S) if self.cuts is None else expand_cut(th, S, self.cuts)):
            prem = tuple((frozenset(p[0]), frozenset(p[1])) for p in prem)
            if not all(self.oracle.prov(p) for p in prem):
                continue
            w = 0 if lab == 'Del' else 1
            lbs = [self._lbv(p) for p in prem]
            capb = bound if best is None else best[0]
            rl = w + sum(lbs)
            if rl > capb:
                newlb = min(newlb, rl); continue
            tot = w; tl = glr; ok = True
            for i, p in enumerate(prem):
                rest = sum(lbs[i + 1:])
                r = self.solve(p, capb - tot - rest)
                if r is None:
                    ok = False
                    newlb = min(newlb, tot + self._lbv(p) + rest)
                    break
                tot += r[0]; tl += r[1]
            if ok and (best is None or (tot, tl) < best[:2]):
                best = (tot, tl, lab, prem)
        if best is not None:
            self.exact[S] = best
            return best
        self.lb[S] = max(self.lb.get(S, 1), newlb)
        return None

    def minimize(self, root, max_size=400):
        """Iterative deepening at the root.  None for a non-theorem; dict(c=(size, loeb), certified=True); or, on
        abort or a size above max_size, dict(c=upper bound, certified=False, lb=certified lower bound)."""
        S = (frozenset(root[0]), frozenset(root[1]))
        if not self.oracle.prov(S):
            return None
        self.count = 0
        bound = self._lbv(S)
        try:
            while bound <= max_size:
                r = self.solve(S, bound)
                if r is not None:
                    return dict(c=r[:2], certified=True, expansions=self.count)
                bound = max(bound + 1, self._lbv(S))
        except Abort:
            pass
        ub = self.greedy(S)
        return dict(c=ub, certified=False, lb=self._lbv(S), expansions=self.count)

    def greedy(self, S, memo=None):
        """Upper bound: size and Loeb count of the oracle's own derivation (eager invertible rules, first GLR that
        works)."""
        if memo is None: memo = {}
        if S in memo: return memo[S]
        th = self.th
        if is_axiom(th, *S):
            return (1, 0)
        out = None
        rules = [(tuple((frozenset(p[0]), frozenset(p[1])) for p in prem), glr, lab) for prem, glr, lab in expand(th, S)]
        for prem, glr, lab in rules:
            if not glr and all(self.oracle.prov(p) for p in prem):
                subs = [self.greedy(p, memo) for p in prem]
                out = (1 + sum(s[0] for s in subs), sum(s[1] for s in subs)); break
        if out is None:
            for prem, glr, lab in rules:
                if glr and self.oracle.prov(prem[0]):
                    s = self.greedy(prem[0], memo); out = (1 + s[0], 1 + s[1]); break
        memo[S] = out
        return out

    def derivation(self, root):
        S = (frozenset(root[0]), frozenset(root[1]))
        def rec(S):
            e = self.exact[S]
            if e[2] == 'Del':
                return rec(e[3][0])
            return (S, e[2], [rec(p) for p in e[3]])
        return rec(S)

    def stats(self, root):
        d = self.derivation(root)
        seen = set(); acc = dict(size=0, loeb=0, height=0, loeb_depth=0)
        def walk(t, dp, gd):
            S, lab, ch = t
            acc['size'] += 1; seen.add(S)
            if lab == 'GLR': acc['loeb'] += 1; gd += 1
            acc['height'] = max(acc['height'], dp); acc['loeb_depth'] = max(acc['loeb_depth'], gd)
            for c in ch: walk(c, dp + 1, gd)
        walk(d, 1, 0)
        acc['dag'] = len(seen)
        return acc

    def dag_sizes(self, root):
        """DAG measures of the minimal derivation (specs/2026-10-05-k-at-n8.md, lemma sharing (b)): `exact` = number of
        distinct sequents; `subsumption` = number of certified sequents when a sequent subsumed by an already certified
        one (its left side contains, and its right side contains, the certified sequent's) is a free reference,
        children certified before parents, siblings in the better of the two orders.  Both are upper bounds on the
        minimal DAG size over all derivations."""
        return dag_measures(self.derivation(root))

    def render(self, root, names=None):
        lines = []
        def walk(t, ind):
            S, lab, ch = t
            lines.append('%s%s   [%s]' % ('  ' * ind, self.th.show_seq(S, names), lab))
            for c in ch: walk(c, ind + 1)
        walk(self.derivation(root), 0)
        return '\n'.join(lines)


def _subsumes(a, b):
    """Sequent a = (L, R) subsumes b: b is a weakening of a."""
    return a[0] <= b[0] and a[1] <= b[1]


def dag_measures(d):
    """d = (seq, label, children) tree (MinSearch.derivation).  Returns dict(tree, exact, subsumption)."""
    seen = set(); n = [0]
    def walk(t):
        S, lab, ch = t
        n[0] += 1; seen.add(S)
        for c in ch: walk(c)
    walk(d)

    def subs(order):
        cert = []
        def go(t):
            S, lab, ch = t
            for c in cert:
                if _subsumes(c, S): return 0
            tot = 1 + sum(go(c) for c in (ch if order == 0 else ch[::-1]))
            cert.append(S)
            return tot
        return go(d)
    return dict(tree=n[0], exact=len(seen), subsumption=min(subs(0), subs(1)))
