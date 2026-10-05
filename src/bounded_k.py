"""The bounded calculus K (specs/2026-10-05-proof-length.md, Part B; notes/proof-length.md §3).

Boxes carry budgets: [](A, b).  A budgeted program x_b reads with budget b; its quoted arguments ^A are A_b.
Truth of [](A, b): K derives |- A (empty context) in at most b sequents.  So a budgeted program's play is a function
of budgets and sources.  Rules: G3 propositional + unfolding (as GLS+Def), initial sequents (P, F, T and BoxEq),
Nec (|- A of size s <= c gives [](A, c) on the right, size s + 1) and the joint bounded Loeb rule JLoeb(S, b)
(premises [](S, b) |- A_j for each A_j in S, |S| <= 3; conclusion A_i, or phi(A_i) for a constant; size 1 + sum s_j,
side condition b >= 1 + sum s_j).  No GLR context, no cut: K is sound by construction (notes §3) and strictly
weaker than GL.

Minimal sizes are the greatest fixed point below infinity of the Bellman equations, reached by Gauss-Seidel passes
from infinity: every value found is witnessed by a real derivation, and after k passes every derivation of
JLoeb/Nec nesting depth <= k is found, so the iteration converges to the exact minima (capped at `cap`).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from conj4 import parse, src as psrc
from gl_proofs import FP, FBOT, FTOP, FNOT, FAND, FOR, FIMP, FBOX, KNAME

INF = 1 << 30


def has_box(t):
    k = t[0]
    if k in ('C', 'D'): return False
    if k == 'not': return has_box(t[1])
    if k in ('and', 'or'): return has_box(t[1]) or has_box(t[2])
    return True


class KTheory:
    def __init__(self, cap=60, arity=3, prune=None, ustar_limit=40, filter_first=False):
        """prune(A) -> False when A's budget erasure is known not to be a GL theorem (then K cannot derive |- A:
        every K rule is GL-sound after erasing budgets, notes/proof-length.md §3; specs/2026-10-05-k-at-n8.md), None
        when unknown.  A pruning only: it removes derivations that cannot exist.  ustar_limit / filter_first: the JLoeb
        candidate set is the reachable box-content closure truncated at ustar_limit elements (the n = 6 run's rule);
        with filter_first the prune is applied before truncation (src/k_at_n8.py)."""
        self.cap = cap; self.arity = arity
        self.prune = prune; self._dead = {}; self.ustar_limit = ustar_limit; self.filter_first = filter_first
        self.trees = []; self.tree_id = {}
        self.genos = []; self.geno_id = {}
        self.forms = []; self.form_id = {}
        self.defn = {}; self.inv = {}
        self.BOT = self.f((FBOT,)); self.TOP = self.f((FTOP,))
        self.T = {}; self.J = {}          # formula -> current best value
        self.Tw = {}; self.Jw = {}        # witnesses: T: ('seq', ...) ; J: (S, b, total)
        self.U1 = {}; self.Ustar = {}
        self.goalsT = set(); self.goalsJ = set()

    # -- programs ------------------------------------------------------------
    def tree(self, s):
        t = parse(s) if isinstance(s, str) else s
        k = psrc(t)
        i = self.tree_id.get(k)
        if i is None:
            i = len(self.trees); self.tree_id[k] = i; self.trees.append(t)
        return i

    def geno(self, s, b):
        ti = self.tree(s)
        if not has_box(self.trees[ti]): b = 0
        key = (ti, b)
        g = self.geno_id.get(key)
        if g is None:
            g = len(self.genos); self.geno_id[key] = g; self.genos.append(key)
        return g

    def name(self, g):
        ti, b = self.genos[g]
        s = psrc(self.trees[ti])
        return s if b == 0 else '%s@%d' % (s, b)

    # -- formulas ------------------------------------------------------------
    def f(self, t):
        i = self.form_id.get(t)
        if i is None:
            i = len(self.forms); self.form_id[t] = i; self.forms.append(t)
        return i

    def P(self, gx, gy): return self.f((FP, gx, gy))
    def neg(self, a): return self.f((FNOT, a))
    def box(self, a, b): return self.f((FBOX, a, b))

    def phi(self, gx, gy):
        ti, b = self.genos[gx]
        def tr(t):
            k = t[0]
            if k == 'C': return self.TOP
            if k == 'D': return self.BOT
            if k == 'not': return self.neg(tr(t[1]))
            if k == 'and': return self.f((FAND, tr(t[1]), tr(t[2])))
            if k == 'or': return self.f((FOR, tr(t[1]), tr(t[2])))
            _, kind, lev, form, arg = t
            if form == 'ME': p, q = gy, gx
            elif form == 'THEM': p, q = gy, gy
            else: p, q = gy, self.geno(arg, b)
            s = self.P(p, q)
            if kind: s = self.neg(s)
            if lev:
                bb = self.BOT
                for _ in range(lev): bb = self.box(bb, b)
                s = self.f((FIMP, self.neg(bb), s))
            return self.box(s, b)
        return tr(self.trees[ti])

    def unfold(self, pf):
        d = self.defn.get(pf)
        if d is None:
            _, x, y = self.forms[pf]
            d = self.phi(x, y); self.defn[pf] = d
            self.inv.setdefault(d, []).append(pf)
        return d

    def show(self, i):
        t = self.forms[i]; k = t[0]
        if k == FP: return 'P[%s,%s]' % (self.name(t[1]), self.name(t[2]))
        if k == FBOT: return 'F'
        if k == FTOP: return 'T'
        if k == FNOT: return '~' + self.show(t[1])
        if k == FBOX: return '[%d]%s' % (t[2], self.show(t[1]))
        return '(%s %s %s)' % (self.show(t[1]), KNAME[k], self.show(t[2]))

    # -- the calculus --------------------------------------------------------
    def boxeq(self, L, R):
        F = self.forms
        lb = [(F[a][1], F[a][2]) for a in L if F[a][0] == FBOX]
        if not lb: return False
        for c in R:
            t = F[c]
            if t[0] != FBOX: continue
            B, cc = t[1], t[2]
            for A, a in lb:
                if A == B and a <= cc: return True
                if F[A][0] == FP and self.unfold(A) == B and a <= cc: return True
                if F[B][0] == FP and self.unfold(B) == A and a + 1 <= cc: return True
        return False

    def axiom(self, L, R):
        F = self.forms
        if self.BOT in L or self.TOP in R: return True
        for a in L:
            if a in R and F[a][0] in (FP, FBOX): return True
        return self.boxeq(L, R)

    def _leafJ(self, A):
        """JLoeb leaf for a right formula A (also via phi^-1)."""
        best = self.J.get(A, INF); self.goalsJ.add(A)
        for P in self.inv.get(A, ()):
            self.goalsJ.add(P); best = min(best, self.J.get(P, INF))
        return best

    def m(self, L, R, memo):
        """Minimal size of L |- R given the current T and J values (one phase: no rule reopens a context)."""
        key = (L, R)
        if key in memo: return memo[key]
        memo[key] = INF               # no cycles inside a phase; guard anyway
        F = self.forms
        if self.axiom(L, R):
            memo[key] = 1; return 1
        best = INF
        # canonical single-premise formula (normal form): decompose, delete, or close by a JLoeb leaf on it
        sp = None
        for a in L:
            if F[a][0] in (FNOT, FAND) and (sp is None or a < sp[1]): sp = (0, a)
        for a in R:
            if F[a][0] in (FNOT, FOR, FIMP) and (sp is None or a < sp[1]): sp = (1, a)
        if sp is not None:
            side, a = sp; t = F[a]; k = t[0]
            if side == 0:
                best = min(best, self.m(L - {a}, R, memo))
                if k == FNOT: best = min(best, 1 + self.m(L - {a}, R | {t[1]}, memo))
                else: best = min(best, 1 + self.m((L - {a}) | {t[1], t[2]}, R, memo))
            else:
                best = min(best, self.m(L, R - {a}, memo), self._leafJ(a))
                if k == FNOT: best = min(best, 1 + self.m(L | {t[1]}, R - {a}, memo))
                elif k == FOR: best = min(best, 1 + self.m(L, (R - {a}) | {t[1], t[2]}, memo))
                else: best = min(best, 1 + self.m(L | {t[1]}, (R - {a}) | {t[2]}, memo))
            memo[key] = min(best, self.cap + 1) if best <= self.cap else INF
            return memo[key]
        for a in L:
            t = F[a]; k = t[0]
            if k == FOR:
                best = min(best, 1 + self.m((L - {a}) | {t[1]}, R, memo) + self.m((L - {a}) | {t[2]}, R, memo))
            elif k == FIMP:
                best = min(best, 1 + self.m(L - {a}, R | {t[1]}, memo) + self.m((L - {a}) | {t[2]}, R, memo))
            elif k == FP:
                best = min(best, 1 + self.m((L - {a}) | {self.unfold(a)}, R, memo))
        for a in R:
            t = F[a]; k = t[0]
            best = min(best, self._leafJ(a))
            if k == FAND:
                best = min(best, 1 + self.m(L, (R - {a}) | {t[1]}, memo) + self.m(L, (R - {a}) | {t[2]}, memo))
            elif k == FP:
                best = min(best, 1 + self.m(L, (R - {a}) | {self.unfold(a)}, memo))
            elif k == FBOX:
                A, c = t[1], t[2]
                self.goalsT.add(A)
                s = self.T.get(A, INF)
                if s <= c: best = min(best, s + 1)
        memo[key] = best if best <= self.cap else INF
        return memo[key]

    # -- closures for JLoeb ----------------------------------------------------
    def one_phase(self, A):
        """Right-box contents (and their phi counterparts) in the phase of |- A."""
        if A in self.U1: return self.U1[A]
        F = self.forms
        seen = set(); out = set(); stack = [A]
        while stack:
            a = stack.pop()
            if a in seen: continue
            seen.add(a); t = F[a]; k = t[0]
            if k == FBOX:
                B = t[1]; out.add(B)
                if F[B][0] == FP: out.add(self.unfold(B))
                for P in self.inv.get(B, ()): out.add(P)
            elif k == FP: stack.append(self.unfold(a))
            elif k in (FNOT,): stack.append(t[1])
            elif k in (FAND, FOR, FIMP): stack += [t[1], t[2]]
        self.U1[A] = out
        return out

    def dead(self, A):
        """True when the prune hook rules out any K derivation of |- A."""
        if self.prune is None: return False
        d = self._dead.get(A)
        if d is None:
            d = self._dead[A] = (self.prune(A) is False)
        return d

    def ustar(self, A, limit=None):
        if A in self.Ustar: return self.Ustar[A]
        limit = self.ustar_limit if limit is None else limit
        seen = set(); stack = [A]; kept = set()
        while stack and len(kept if self.filter_first else seen) < limit:
            a = stack.pop()
            for b in self.one_phase(a):
                if b not in seen and b != A:
                    seen.add(b); stack.append(b)
                    if not self.dead(b): kept.add(b)
        out = sorted(kept if self.filter_first else [u for u in seen if not self.dead(u)])
        self.Ustar[A] = out
        return out

    def j_value(self, A, memo):
        best = INF; wit = None
        if self.dead(A): return best, wit
        U = self.ustar(A)
        cands = [()] + [(u,) for u in U]
        if self.arity >= 3:
            cands += [(U[i], U[j]) for i in range(len(U)) for j in range(i + 1, len(U))]
        for extra in cands:
            S = (A,) + extra
            b = 1
            while b <= self.cap:
                L = frozenset(self.box(s, b) for s in S)
                tot = 1
                for s in S:
                    tot += self.m(L, frozenset([s]), memo)
                    if tot > self.cap: break
                if tot > self.cap: break
                if tot <= b:
                    if tot < best: best, wit = tot, (S, b)
                    break
                b = tot
        return best, wit

    def solve(self, targets, max_passes=200):
        """Exact minimal T for every target formula (and everything they depend on)."""
        for A in targets: self.goalsT.add(A)
        for it in range(max_passes):
            changed = False
            memo = {}
            for A in sorted(self.goalsJ):
                v, w = self.j_value(A, memo)
                if v < self.J.get(A, INF):
                    self.J[A] = v; self.Jw[A] = w; changed = True; memo = {}
            for A in sorted(self.goalsT):
                if self.dead(A): continue
                v = self.m(frozenset(), frozenset([A]), memo)
                if v < self.T.get(A, INF):
                    self.T[A] = v; changed = True; memo = {}
            ng = len(self.goalsT) + len(self.goalsJ)
            if not changed and ng == getattr(self, '_ng', -1):
                return it + 1
            self._ng = ng
        raise RuntimeError('K fixpoint did not converge')

    # -- play ------------------------------------------------------------------
    def atoms(self, gx, gy):
        """x's box atoms against y as (box formula id) in source order."""
        out = []
        def walk(f):
            t = self.forms[f]; k = t[0]
            if k == FNOT: walk(t[1])
            elif k in (FAND, FOR): walk(t[1]); walk(t[2])
            elif k == FBOX: out.append(f)
        walk(self.phi(gx, gy))
        return out

    def truth(self, f, play):
        """Truth in the standard model given `play(gx, gy)` and the current T values."""
        t = self.forms[f]; k = t[0]
        if k == FP: return play(t[1], t[2])
        if k == FBOT: return False
        if k == FTOP: return True
        if k == FNOT: return not self.truth(t[1], play)
        if k == FAND: return self.truth(t[1], play) and self.truth(t[2], play)
        if k == FOR: return self.truth(t[1], play) or self.truth(t[2], play)
        if k == FIMP: return (not self.truth(t[1], play)) or self.truth(t[2], play)
        return self.T.get(t[1], INF) <= t[2]

    def play_fn(self):
        cache = {}
        def play(gx, gy):
            key = (gx, gy)
            if key not in cache:
                cache[key] = self.truth(self.phi(gx, gy), play)
            return cache[key]
        return play

    def soundness_check(self):
        """Every K-derived closed formula (finite T) and every JLoeb conclusion is true in the computed model."""
        play = self.play_fn()
        bad = [A for A, v in self.T.items() if v < INF and not self.truth(A, play)]
        bad += [A for A, v in self.J.items() if v < INF and not self.truth(A, play)]
        return len([v for v in self.T.values() if v < INF]) + len([v for v in self.J.values() if v < INF]), bad
