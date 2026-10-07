"""K with cut and distribution under a box (specs/2026-10-05-k-cut.md; predictions/2026-10-05-k-cut.md;
notes/k-cut.md).

    python3 src/k_cut.py repro                       # option off reproduces the K tables exactly
    python3 src/k_cut.py certify --n 8 --budgets 16 54 [--goff 0]
    python3 src/k_cut.py ktables --n 8 --budgets 4 8 16 24 54 --cut c [--goff 0] [--four mono]
    python3 src/k_cut.py sweep ...  |  static  |  chain  |  graft  |  factorial  |  lottery  |  report

The calculus option itself is `cut` in `src/bounded_k.py` (None / 'c' / 'c4'); everything else lives here:
  * KTheoryC: KTheory with the guard offset (k_four.KTheoryG) and a GL-oracle prune for Dist premises;
  * certify: the extension-model certificate of notes/k-cut.md §1.7 (structural failure at every size);
  * extract / check / replay: derivation extraction from a solved search and an independent checker that rebuilds
    every Dist instance's Lemma C witness (the k cuts) and checks it from scratch.
"""
import argparse, itertools, json, os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
import bounded_k as BK
import gl_proofs as G
import k_four as K4
from gl_proofs import FP, FBOT, FTOP, FNOT, FAND, FOR, FIMP, FBOX
from conj4 import parse, src as psrc

INF = BK.INF
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
KDIR8 = os.path.join(RUNS, 'k-at-n8')
K4DIR = os.path.join(RUNS, 'k-four')
KCDIR = os.path.join(RUNS, 'k-cut')
os.makedirs(KCDIR, exist_ok=True)

FB = K4.FB; PB = K4.PB; PSTAR = K4.PSTAR; P2 = K4.P2; P12B = K4.P12B; PS1B = K4.PS1B; PB2 = K4.PB2


# ====================================================================== the calculus with its GL prune
class KTheoryC(K4.KTheoryG):
    """KTheory with the guard offset goff, the cut option, and a GL-oracle prune on Dist premises (every K_c sequent
    erases to a GL-valid sequent, notes/k-cut.md §1.6).  The closed-goal prune is the base prune unchanged, so the
    JLoeb candidate sets are exactly K's."""

    def __init__(self, *a, gl_prune=True, **kw):
        super().__init__(*a, **kw)
        self.th = G.Theory(); self.orc = G.Oracle(self.th); self._em = {}; self._sp = {}
        if gl_prune and self.cut is not None:
            self.seq_prune = self._seq_prune

    def erase(self, f):
        return K4.erase(self, f, self.th, self._em)

    def _seq_prune(self, Pi, B):
        key = (Pi, B)
        r = self._sp.get(key)
        if r is None:
            if len(self.orc.memo) > 400_000:          # memory: the oracle memo is a cache, not state
                self.orc.memo.clear()
            r = self._sp[key] = self.orc.prov((frozenset(self.erase(a) for a in Pi), frozenset([self.erase(B)])))
        return r

    def mp_value(self, B, memo):
        """As KTheory.mp_value, but skips registered premises whose hypotheses have no closed derivation yet (their
        lemma cuts cannot be formed) before searching the premise."""
        best = INF; wit = None
        for Pi, H, choice in list(self.mp.get(B, ())):
            if any(self.T.get(A, INF) >= INF for a, A, x in H): continue
            sv = self.m(Pi, frozenset([B]), memo)
            if sv >= INF: continue
            tot = sv
            for (a, A, x), ch in zip(H, choice):
                t = self.T.get(A, INF)
                if A in ch: tot += t + 1
                if x in ch: tot += (t + 2) if t <= a else INF          # Nec on |- A needs T(A) <= a
            if tot < best: best, wit = tot, (Pi, H, choice)
        return (best if best <= self.cap else INF), wit


# ====================================================================== the extension-model certificate (§1.7)
class Certifier:
    """Structural-failure certificates for closed goals |- A at program budget b (notes/k-cut.md §1.7).

    Three-valued truth in the extension model I_E: a box [](Y, e) is true if E's closure contains (Y, e) (Lemma E1,
    exact at budgets <= b + 1) or the reference search derived |- Y within e (K or K_c: a lower bound on Std);
    false if GL+Def does not prove erase(Y) or Y is certified structural; unknown otherwise.  A goal is certified
    when it is false under Kleene's strong three-valued logic for some E (singletons and pairs of budget-b contents
    occurring in its unfolding closure).  four=True closes E under 4m too (valid for K_c + 4m as well; weaker)."""

    def __init__(self, K, b, four=True):
        self.K = K; self.b = b; self.four = four
        self.th = G.Theory(); self.orc = G.Oracle(self.th); self._em = {}; self._gl = {}
        self.struct = {}            # content -> certificate (E tuple)

    def gltrue(self, Y):
        r = self._gl.get(Y)
        if r is None:
            r = self._gl[Y] = self.orc.prov((frozenset(), frozenset([K4.erase(self.K, Y, self.th, self._em)])))
        return r

    def ecl(self, E, Y, d):
        K = self.K; F = K.forms; b0 = self.b
        if d < b0 or not E: return False
        base = set()
        for X in E:
            base.add(X)
            if F[X][0] == FP: base.add(K.unfold(X))
        if Y in base: return True
        if d >= b0 + 1:
            if F[Y][0] == FP and K.unfold(Y) in base: return True
            if self.four and F[Y][0] == FBOX and F[Y][1] in base and F[Y][2] >= b0: return True
        return False

    def std(self, Y, d):
        if Y in self.struct or not self.gltrue(Y): return False
        if self.K.T.get(Y, INF) <= d: return True
        return None

    def truth(self, f, E):
        K = self.K; t = K.forms[f]; k = t[0]
        if k == FP: return self.truth(K.unfold(f), E)
        if k == FBOT: return False
        if k == FTOP: return True
        if k == FNOT:
            a = self.truth(t[1], E); return None if a is None else (not a)
        if k in (FAND, FOR, FIMP):
            a = self.truth(t[1], E)
            if k == FIMP: a = None if a is None else (not a)
            c = self.truth(t[2], E)
            if k == FAND:
                if a is False or c is False: return False
                return None if (a is None or c is None) else True
            if a is True or c is True: return True
            return None if (a is None or c is None) else False
        if t[2] > self.b + 1: raise ValueError('query above b + 1')
        if self.ecl(E, t[1], t[2]): return True
        return self.std(t[1], t[2])

    def boxes(self, f, out=None, seen=None):
        K = self.K
        if out is None: out = set(); seen = set()
        if f in seen: return out
        seen.add(f); t = K.forms[f]; k = t[0]
        if k == FP: self.boxes(K.unfold(f), out, seen)
        elif k == FNOT: self.boxes(t[1], out, seen)
        elif k in (FAND, FOR, FIMP): self.boxes(t[1], out, seen); self.boxes(t[2], out, seen)
        elif k == FBOX: out.add(f)
        return out

    def certify_one(self, A):
        """None, or the E that refutes |- A."""
        K = self.K; F = K.forms
        try:
            if self.truth(A, ()) is False: return ()
            cand = sorted({F[c][1] for c in self.boxes(A) if F[c][2] == self.b and self.std(F[c][1], self.b) is not True})
            for X in cand:
                if self.truth(A, (X,)) is False: return (X,)
            for X, Y in itertools.combinations(cand, 2):
                if self.truth(A, (X, Y)) is False: return (X, Y)
        except ValueError:
            return None
        return None

    def closure(self, goals):
        """Every box content reachable from the goals (descending into contents)."""
        K = self.K; out = set(); st = list(goals)
        while st:
            f = st.pop()
            if f in out: continue
            out.add(f)
            st += [K.forms[c][1] for c in self.boxes(f)]
        return out

    def run(self, goals, rounds=12):
        """Iterate certification over the goals' content closure.  Returns {goal: E or None}."""
        allc = self.closure(goals)
        for _ in range(rounds):
            new = 0
            for A in sorted(allc):
                if A in self.struct or not self.gltrue(A) or self.K.T.get(A, INF) <= self.b + 1: continue
                r = self.certify_one(A)
                if r is not None:
                    self.struct[A] = r; new += 1
            if not new: break
        return {A: self.struct.get(A) for A in goals}


# ====================================================================== derivation extraction and the checker
class Extract:
    """Rebuild one minimal derivation (as the search valued it) from a solved KTheory.  Nodes are dicts:
    rule, L, R (frozensets of formula ids), kids, and rule data.  Uses the converged T/J/M values."""

    def __init__(self, K):
        self.K = K; self.F = K.forms

    def closed(self, A):
        return self.seq(frozenset(), frozenset([A]))

    def leafJ(self, L, R, a):
        K = self.K
        cands = [(K.J.get(a, INF), 'JLoeb', a)] + [(K.J.get(P, INF), 'JLoeb', P) for P in K.inv.get(a, ())]
        if K.cut is not None: cands.append((K.M.get(a, INF), 'MP', a))
        return min(cands)

    def jloeb(self, L, R, A, concl):
        K = self.K; S, b = K.Jw[A]
        Lb = frozenset(K.box(s, b) for s in S)
        kids = [self.seq(Lb, frozenset([s])) for s in S]
        return dict(rule='JLoeb', L=L, R=R, S=S, b=b, concl=concl, kids=kids)

    def mp(self, L, R, A):
        K = self.K; Pi, H, choice = K.Mw[A]
        prem = self.seq(Pi, frozenset([A]))
        lem = []
        for (a, Ai, x), ch in zip(H, choice):
            if Ai in ch: lem.append(('content', Ai, self.closed(Ai)))
            if x in ch: lem.append(('box', x, self.closed(Ai)))
        return dict(rule='MP', L=L, R=R, concl=A, Pi=Pi, kids=[prem], lemmas=lem)

    def seq(self, L, R):
        K = self.K; F = self.F
        v = K.m(L, R, {})
        if v >= INF: raise ValueError('not derivable: %s' % self.show(L, R))
        if K.axiom(L, R): return dict(rule='Ax', L=L, R=R, kids=[])
        memo = {}
        sp = None
        for a in L:
            if F[a][0] in (FNOT, FAND) and (sp is None or a < sp[1]): sp = (0, a)
        for a in R:
            if F[a][0] in (FNOT, FOR, FIMP) and (sp is None or a < sp[1]): sp = (1, a)
        opts = []
        if sp is not None:
            side, a = sp; t = F[a]; k = t[0]
            if side == 0:
                opts.append((K.m(L - {a}, R, memo), 'Del', [(L - {a}, R)], {}))
                if k == FNOT: opts.append((1 + K.m(L - {a}, R | {t[1]}, memo), '~L', [(L - {a}, R | {t[1]})], {}))
                else: opts.append((1 + K.m((L - {a}) | {t[1], t[2]}, R, memo), '&L', [((L - {a}) | {t[1], t[2]}, R)], {}))
            else:
                opts.append((K.m(L, R - {a}, memo), 'Del', [(L, R - {a})], {}))
                lv, lr, la = self.leafJ(L, R, a)
                opts.append((lv, lr, [], dict(target=la, concl=a)))
                if k == FNOT: opts.append((1 + K.m(L | {t[1]}, R - {a}, memo), '~R', [(L | {t[1]}, R - {a})], {}))
                elif k == FOR: opts.append((1 + K.m(L, (R - {a}) | {t[1], t[2]}, memo), '|R', [(L, (R - {a}) | {t[1], t[2]})], {}))
                else: opts.append((1 + K.m(L | {t[1]}, (R - {a}) | {t[2]}, memo), '->R', [(L | {t[1]}, (R - {a}) | {t[2]})], {}))
        else:
            for a in L:
                t = F[a]; k = t[0]
                if k == FOR:
                    p = [((L - {a}) | {t[1]}, R), ((L - {a}) | {t[2]}, R)]
                    opts.append((1 + sum(K.m(x, y, memo) for x, y in p), '|L', p, {}))
                elif k == FIMP:
                    p = [(L - {a}, R | {t[1]}), ((L - {a}) | {t[2]}, R)]
                    opts.append((1 + sum(K.m(x, y, memo) for x, y in p), '->L', p, {}))
                elif k == FP:
                    p = [((L - {a}) | {K.unfold(a)}, R)]
                    opts.append((1 + K.m(*p[0], memo), 'UnfL', p, {}))
            for a in R:
                t = F[a]; k = t[0]
                lv, lr, la = self.leafJ(L, R, a)
                opts.append((lv, lr, [], dict(target=la, concl=a)))
                if k == FAND:
                    p = [(L, (R - {a}) | {t[1]}), (L, (R - {a}) | {t[2]})]
                    opts.append((1 + sum(K.m(x, y, memo) for x, y in p), '&R', p, {}))
                elif k == FP:
                    p = [(L, (R - {a}) | {K.unfold(a)})]
                    opts.append((1 + K.m(*p[0], memo), 'UnfR', p, {}))
                elif k == FBOX:
                    A, c = t[1], t[2]
                    s = K.T.get(A, INF)
                    if s <= c: opts.append((s + 1, 'Nec', None, dict(content=A, box=a)))
                    if K.cut is not None:
                        d = self.dist_opt(L, A, c)
                        if d is not None: opts.append((d[0], 'Dist', None, dict(box=a, **d[1])))
        opts = [o for o in opts if o[0] < INF]
        best = min(o[0] for o in opts)
        assert best == v, (best, v, self.show(L, R))
        val, rule, prem, info = next(o for o in opts if o[0] == best)
        if rule == 'Del':
            node = self.seq(*prem[0]); node = dict(node); node['weakened_to'] = (L, R)
            return dict(rule='Del', L=L, R=R, kids=[node])
        if rule == 'JLoeb':
            return self.jloeb(L, R, info['target'], info['target'])
        if rule == 'MP':
            return self.mp(L, R, info['target'])
        if rule == 'Nec':
            return dict(rule='Nec', L=L, R=R, box=info['box'], kids=[self.closed(info['content'])])
        if rule == 'Dist':
            return dict(rule='Dist', L=L, R=R, box=info['box'], H=info['H'], choice=info['choice'],
                        kids=[self.seq(info['Pi'], frozenset([self.F[info['box']][1]]))])
        return dict(rule=rule, L=L, R=R, kids=[self.seq(x, y) for x, y in prem])

    def dist_opt(self, L, B, c):
        K = self.K; F = self.F
        lb = sorted((F[x][2], F[x][1], x) for x in L if F[x][0] == FBOX)
        best = None
        for k in range(1, min(K.dist_arity, len(lb)) + 1):
            for H in itertools.combinations(lb, k):
                if sum(a for a, _, _ in H) + k + 1 > c: continue
                opts = [((A,),) if K.cut == 'c' else ((A,), (x,), (A, x)) for a, A, x in H]
                for choice in itertools.product(*opts):
                    Pi = frozenset(f for ch in choice for f in ch)
                    charge = 0
                    for (a, A, x), ch in zip(H, choice):
                        if A in ch: charge += a + 1
                        if x in ch: charge += a + 2
                    if K.cut == 'c': charge = sum(a for a, _, _ in H) + k
                    if charge + 1 > c: continue
                    if K.seq_prune is not None and K.seq_prune(Pi, B) is False: continue
                    sv = K.m(Pi, frozenset([B]), {})
                    if sv >= INF or sv + charge > c: continue
                    if best is None or 1 + sv < best[0]:
                        best = (1 + sv, dict(H=H, choice=choice, Pi=Pi, charge=charge))
        return best

    def show(self, L, R):
        K = self.K
        return '%s |- %s' % (', '.join(sorted(K.show(a) for a in L)), ', '.join(sorted(K.show(a) for a in R)))


class Checker:
    """Independent check of an extracted derivation: every node's rule, premises, side conditions and size are
    recomputed from the tree alone (no table of the search is consulted).  Weakening: a premise may derive a
    subsequent of what the rule requires.  Returns the size; raises AssertionError on any violation."""

    def __init__(self, K):
        self.K = K; self.F = K.forms; self.n_nodes = 0; self.n_dist = 0; self.n_replay = 0; self.n_cut = 0

    def sub(self, node, L, R):
        assert node['L'] <= L and node['R'] <= R, 'premise is not a weakening'

    def axiom(self, L, R):
        K = self.K; F = self.F
        if K.BOT in L or K.TOP in R: return True
        for a in L:
            if a in R and F[a][0] in (FP, FBOX): return True
            if K.cut is not None and F[a][0] == FP and K.unfold(a) in R: return True
        for a in L:
            if F[a][0] != FBOX: continue
            A, aa = F[a][1], F[a][2]
            for c in R:
                if F[c][0] != FBOX: continue
                B, cc = F[c][1], F[c][2]
                if A == B and aa <= cc: return True
                if F[A][0] == FP and K.unfold(A) == B and aa <= cc: return True
                if F[B][0] == FP and K.unfold(B) == A and aa + 1 <= cc: return True
        if K.four is not None:
            return K.four_ax(L, R)
        return False

    def size(self, n):
        self.n_nodes += 1
        K = self.K; F = self.F; L, R = n['L'], n['R']; r = n['rule']; kids = n['kids']
        if r == 'Ax':
            assert self.axiom(L, R), 'not an initial sequent'
            return 1
        if r == 'Del':
            self.sub(kids[0], L, R); return self.size(kids[0])
        if r in ('~L', '&L', '|L', '->L', 'UnfL'):
            cands = [a for a in L if F[a][0] == {'~L': FNOT, '&L': FAND, '|L': FOR, '->L': FIMP, 'UnfL': FP}[r]]
            for a in cands:
                t = F[a]; Lr = L - {a}
                if r == '~L': need = [(Lr, R | {t[1]})]
                elif r == '&L': need = [(Lr | {t[1], t[2]}, R)]
                elif r == '|L': need = [(Lr | {t[1]}, R), (Lr | {t[2]}, R)]
                elif r == '->L': need = [(Lr, R | {t[1]}), (Lr | {t[2]}, R)]
                else: need = [(Lr | {K.unfold(a)}, R)]
                if all(k['L'] <= x and k['R'] <= y for k, (x, y) in zip(kids, need)) and len(kids) == len(need):
                    return 1 + sum(self.size(k) for k in kids)
            raise AssertionError('bad left rule %s' % r)
        if r in ('~R', '&R', '|R', '->R', 'UnfR'):
            cands = [a for a in R if F[a][0] == {'~R': FNOT, '&R': FAND, '|R': FOR, '->R': FIMP, 'UnfR': FP}[r]]
            for a in cands:
                t = F[a]; Rr = R - {a}
                if r == '~R': need = [(L | {t[1]}, Rr)]
                elif r == '&R': need = [(L, Rr | {t[1]}), (L, Rr | {t[2]})]
                elif r == '|R': need = [(L, Rr | {t[1], t[2]})]
                elif r == '->R': need = [(L | {t[1]}, Rr | {t[2]})]
                else: need = [(L, Rr | {K.unfold(a)})]
                if all(k['L'] <= x and k['R'] <= y for k, (x, y) in zip(kids, need)) and len(kids) == len(need):
                    return 1 + sum(self.size(k) for k in kids)
            raise AssertionError('bad right rule %s' % r)
        if r == 'Nec':
            box = n['box']; assert box in R and F[box][0] == FBOX
            k = kids[0]; assert k['L'] == frozenset() and k['R'] <= frozenset([F[box][1]])
            s = self.size(k); assert s <= F[box][2], 'Nec side condition'
            return 1 + s
        if r == 'JLoeb':
            S, b = n['S'], n['b']; Lb = frozenset(K.box(s, b) for s in S)
            assert 1 <= len(S) <= 3 and len(kids) == len(S)
            tot = 1
            for s, k in zip(S, kids):
                assert k['L'] <= Lb and k['R'] <= frozenset([s]), 'JLoeb premise'
                tot += self.size(k)
            assert b >= tot, 'JLoeb side condition'
            c = n['concl']; assert c in S
            assert any(x == c or (F[c][0] == FP and x == K.unfold(c)) for x in R), 'JLoeb conclusion'
            return tot
        if r == 'MP':
            # Lemma C: lemma cuts on the premise's left formulas, each discharged by a closed derivation
            A = n['concl']; assert A in R
            prem = kids[0]; assert prem['R'] <= frozenset([A])
            tot = self.size(prem); left = set(prem['L'])
            for kind, f, der in n['lemmas']:
                assert der['L'] == frozenset()
                s = self.size(der)
                if kind == 'content':
                    assert der['R'] <= frozenset([f]); tot += s + 1; left.discard(f)
                else:
                    assert der['R'] <= frozenset([F[f][1]]) and s <= F[f][2]; tot += s + 2; left.discard(f)
                self.n_cut += 1
            assert not left, 'MP premise uses an undischarged formula'
            return tot
        if r == 'Dist':
            self.n_dist += 1
            box = n['box']; assert box in R and F[box][0] == FBOX
            B, d = F[box][1], F[box][2]
            prem = kids[0]; assert prem['R'] <= frozenset([B])
            charge = 0; allowed = set()
            for (a, A, x), ch in zip(n['H'], n['choice']):
                assert x in L and F[x][0] == FBOX and F[x][1] == A and F[x][2] == a
                if K.cut == 'c': assert ch == (A,)
                if A in ch: charge += a + 1; allowed.add(A)
                if x in ch: charge += a + 2; allowed.add(x)
            assert prem['L'] <= allowed, 'Dist premise context'
            s = self.size(prem)
            assert d >= s + charge, 'Dist side condition'
            return 1 + s
        raise AssertionError('unknown rule %s' % r)

    def replay(self, n, ex):
        """Witness replay: for every Dist node whose hypotheses are true in the computed model, build the Lemma C
        witness (closed derivations of the hypotheses' contents, cut against the premise) and check its size <= d."""
        K = self.K; F = self.F
        if n['rule'] == 'Dist':
            box = n['box']; d = F[box][2]
            if all(K.T.get(A, INF) <= a for a, A, x in n['H']):
                s = self.size(n['kids'][0]); tot = s
                for (a, A, x), ch in zip(n['H'], n['choice']):
                    der = ex.closed(A); sa = self.size(der)
                    assert sa <= a, 'hypothesis witness exceeds its budget'
                    if A in ch: tot += sa + 1
                    if x in ch: tot += sa + 2
                assert tot <= d, 'Lemma C witness exceeds d'
                self.n_replay += 1
        for k in n['kids']:
            self.replay(k, ex)
        for _, _, der in n.get('lemmas', ()):
            self.replay(der, ex)


def check_goal(K, A, replay=True):
    """Extract the derivation of |- A, check it independently, replay its Dist witnesses.  Returns (size, stats)."""
    ex = Extract(K); ck = Checker(K)
    d = ex.closed(A)
    s = ck.size(d)
    if replay:
        ck.replay(d, ex)
    return s, dict(nodes=ck.n_nodes, dist=ck.n_dist, replayed=ck.n_replay, cuts=ck.n_cut)


# ====================================================================== tables
def ktable_c(n, b, cut, four=None, goff=0, ustar_limit=40, certify=True, check=False):
    """K / K_c play matrix of L_n at global budget b (k_at_n8.ktable's construction: same prune, same JLoeb candidate
    rule), with the soundness check, the GL-true/derived atom counts, and (optionally) the structural certificates
    of every GL-true atom content the search does not derive within b."""
    import k_at_n8 as KN
    L, val_free, hc, hd = KN.tables(n)
    t = time.time()
    K = KTheoryC(cap=max(b + goff, 1), ustar_limit=ustar_limit, filter_first=True, four=four, goff=goff, cut=cut)
    K.prune = KN.make_prune(K, L, hc, hd)
    g = [K.geno(s, b) for s in L.rep]
    contents = set(); atoms = {}
    for i, x in enumerate(g):
        for j, y in enumerate(g):
            for a in K.atoms(x, y):
                c = K.forms[a][1]; contents.add(c); atoms.setdefault(c, []).append((i, j))
    passes = K.solve(sorted(contents))
    t_solve = time.time() - t
    play = K.play_fn()
    val = np.array([[int(play(x, y)) for y in g] for x in g], np.int8)
    nchk, bad = K.soundness_check()
    if bad: nchk, bad = K4.closure_check(K)
    mu = L.mu_canon / L.mu_canon.sum()
    gl_true = [c for c in contents if K.prune(c)]
    der = [c for c in gl_true if K.T.get(c, INF) <= b]
    w = lambda cs: float(sum(mu[i] * mu[j] for c in cs for i, j in atoms[c]))
    meta = dict(n=n, b=b, cut=cut, four=four, goff=goff, passes=passes, n_contents=len(contents), sound_checked=nchk,
                sound_bad=len(bad), t_solve=t_solve, diff_vs_free=int((val != val_free).sum()),
                gl_true_contents=len(gl_true), derived_contents=len(der),
                gl_true_atoms=sum(len(atoms[c]) for c in gl_true), derived_atoms=sum(len(atoms[c]) for c in der),
                gl_true_w=w(gl_true), derived_w=w(der),
                n_mp=len(K.M), n_dist_premises=sum(len(v) for v in K.mp.values()))
    if certify and goff <= 1:
        tc = time.time()
        cert = Certifier(K, b, four=(four is not None))
        miss = [c for c in gl_true if K.T.get(c, INF) > b]
        res = cert.run(miss)
        unc = [c for c in miss if res[c] is None]
        meta.update(missing_contents=len(miss), certified_contents=len(miss) - len(unc), uncertified_contents=len(unc),
                    missing_atoms=sum(len(atoms[c]) for c in miss), uncertified_atoms=sum(len(atoms[c]) for c in unc),
                    uncertified_w=w(unc), t_cert=time.time() - tc,
                    uncertified_examples=[K.show(c) for c in unc[:30]])
    if check:
        tc = time.time(); tot = dict(goals=0, nodes=0, dist=0, replayed=0, cuts=0, size_mismatch=0)
        for c in sorted(der):
            s, st = check_goal(K, c)
            tot['goals'] += 1; tot['size_mismatch'] += int(s != K.T[c])
            for k in st: tot[k] += st[k]
        meta['checker'] = tot; meta['t_check'] = time.time() - tc
    meta['t'] = time.time() - t
    return val, meta, K, g


def ktable_targeted(n, b, cut, four=None, goff=0, ustar_limit=40, check_sample=2000):
    """The K_c (search) table computed exactly without a full K_c closure (notes §1.7, Corollary T): K ⊆ K_c, so every
    content K derives within b stays derived; every K miss certified structural stays underived in *every* sound
    calculus of the class; only the uncertified misses are searched in K_c (a closure over their dependencies only;
    a goal's searched minimum does not depend on which other goals are solved).  Plays are recomputed with the
    patched box truths.  Valid for goff <= 1 (the certificate's range)."""
    import k_at_n8 as KN
    assert goff <= 1
    L, val_free, hc, hd = KN.tables(n)
    t = time.time()
    K = KTheoryC(cap=max(b + goff, 1), ustar_limit=ustar_limit, filter_first=True, four=four, goff=goff, cut=None)
    K.prune = KN.make_prune(K, L, hc, hd)
    g = [K.geno(s, b) for s in L.rep]
    contents = set(); atoms = {}
    for i, x in enumerate(g):
        for j, y in enumerate(g):
            for a in K.atoms(x, y):
                c = K.forms[a][1]; contents.add(c); atoms.setdefault(c, []).append((i, j))
    K.solve(sorted(contents))
    t_K = time.time() - t
    vK = np.array([[int(K.play_fn()(x, y)) for y in g] for x in g], np.int8)
    mu = L.mu_canon / L.mu_canon.sum()
    gl_true = [c for c in contents if K.prune(c)]
    miss = [c for c in gl_true if K.T.get(c, INF) > b]
    cert = Certifier(K, b, four=(four is not None))
    res = cert.run(miss)
    unc = [c for c in miss if res[c] is None]
    t_cert = time.time() - t - t_K
    # K_c on the uncertified contents only (same genotype order, contents matched by their printed form)
    Kc = KTheoryC(cap=max(b + goff, 1), ustar_limit=ustar_limit, filter_first=True, four=four, goff=goff, cut=cut)
    Kc.prune = KN.make_prune(Kc, L, hc, hd)
    gc = [Kc.geno(s, b) for s in L.rep]
    want = {K.show(c) for c in unc}
    cmap = {}
    for x in gc:
        for y in gc:
            for a in Kc.atoms(x, y):
                c = Kc.forms[a][1]; s = Kc.show(c)
                if s in want: cmap[s] = c
    Kc.solve(sorted(cmap.values()))
    newly = {s for s, c in cmap.items() if Kc.T.get(c, INF) <= b}
    t_Kc = time.time() - t - t_K - t_cert
    # patched table: recompute plays touching a newly derived content
    Tpatch = dict(K.T)
    for c in unc:
        s = K.show(c)
        if s in newly: Tpatch[c] = Kc.T[cmap[s]]
    val = vK.copy()
    touched = {(i, j) for c in unc if K.show(c) in newly for i, j in atoms[c]}
    if touched:
        saveT = K.T; K.T = Tpatch
        play = K.play_fn()
        for i, j in touched: val[i, j] = int(play(g[i], g[j]))
        # plays are functions of box truths only; others are unchanged, but recheck every play once for safety
        full = np.array([[int(play(x, y)) for y in g] for x in g], np.int8)
        assert (full == val).all()
        K.T = saveT
    nchk, bad = Kc.soundness_check()
    if bad: nchk, bad = K4.closure_check(Kc)
    der_unc = [c for c in unc if K.show(c) in newly]
    w = lambda cs: float(sum(mu[i] * mu[j] for c in cs for i, j in atoms[c]))
    meta = dict(n=n, b=b, cut=cut, four=four, goff=goff, method='targeted', n_contents=len(contents),
                gl_true_contents=len(gl_true), K_derived_contents=len(gl_true) - len(miss),
                missing_contents=len(miss), certified_contents=len(miss) - len(unc), uncertified_contents=len(unc),
                uncertified_w=w(unc), uncertified_examples=[K.show(c) for c in unc[:30]],
                newly_derived_contents=len(der_unc), newly_derived_w=w(der_unc),
                newly_derived_examples=sorted(newly)[:30],
                derived_contents=len(gl_true) - len(miss) + len(der_unc),
                gl_true_atoms=sum(len(atoms[c]) for c in gl_true),
                derived_atoms=sum(len(atoms[c]) for c in gl_true if K.T.get(c, INF) <= b) + sum(len(atoms[c]) for c in der_unc),
                gl_true_w=w(gl_true), derived_w=w([c for c in gl_true if K.T.get(c, INF) <= b]) + w(der_unc),
                Kc_goals=len(cmap), Kc_sound_checked=nchk, sound_bad=len(bad), diff_vs_K=int((val != vK).sum()),
                diff_vs_free=int((val != val_free).sum()), t_K=t_K, t_cert=t_cert, t_Kc=t_Kc)
    # independent checker on a sample of the K_c-searched contents (and every newly derived one)
    rng = np.random.default_rng(b)
    pool_ = [c for c in cmap.values() if Kc.T.get(c, INF) <= Kc.cap]
    samp = list(rng.choice(pool_, min(check_sample, len(pool_)), replace=False)) if pool_ else []
    samp += [cmap[s] for s in newly]
    ck = dict(goals=0, size_mismatch=0, dist=0, replayed=0, fail=0)
    for c in dict.fromkeys(samp):
        try:
            s, st = check_goal(Kc, int(c)); ck['goals'] += 1; ck['size_mismatch'] += int(s != Kc.T[int(c)])
            ck['dist'] += st['dist']; ck['replayed'] += st['replayed']
        except (AssertionError, ValueError) as e:
            ck['fail'] += 1
    meta['checker'] = ck
    meta['t'] = time.time() - t
    return val, meta


def tag(cut, four, goff):
    return '%s%s_g%d' % ({None: 'K', 'c': 'Kc', 'c4': 'Kc4'}[cut], '4m' if four == 'mono' else '', goff)


def kpath(n, b, cut, four=None, goff=0):
    return os.path.join(KCDIR, '%s_n%d_b%d.npy' % (tag(cut, four, goff), n, b))


def _ktable_job(j):
    n, b, cut, four, goff, check = j[:6]
    if len(j) > 6 and j[6]:
        val, meta = ktable_targeted(n, b, cut, four, goff)
    else:
        val, meta, K, g = ktable_c(n, b, cut, four, goff, check=check)
    np.save(kpath(n, b, cut, four, goff), val)
    json.dump(meta, open(kpath(n, b, cut, four, goff).replace('.npy', '.json'), 'w'), indent=1)
    return meta


def load_c(n, b, cut, four=None, goff=0):
    """Published K tables where they exist (n = 8 from runs/k-at-n8, n = 6 from runs/k-four), else this run's."""
    if cut is None and four is None and goff == 0:
        p8 = os.path.join(KDIR8, 'kval_n%d_b%d.npy' % (n, b)); p6 = os.path.join(K4DIR, 'K_g0_n%d_b%d.npy' % (n, b))
        for p in (p8, p6):
            if os.path.exists(p): return np.load(p)
    if cut is None and four is None and goff == 1:
        p = os.path.join(K4DIR, 'K_g1_n%d_b%d.npy' % (n, b))
        if os.path.exists(p): return np.load(p)
    return np.load(kpath(n, b, cut, four, goff))


def cmd_repro(a):
    """With the option off, KTheoryC reproduces the published K tables exactly."""
    out = []
    jobs = [(8, b, None, None, 0, False) for b in a.budgets8] + [(6, b, None, None, 0, False) for b in a.budgets6]
    jobs.sort(key=lambda j: -j[1] * j[0])
    with Pool(a.workers) as pool:
        for m in pool.imap_unordered(_ktable_job, jobs):
            n, b = m['n'], m['b']
            ref = (np.load(os.path.join(KDIR8, 'kval_n8_b%d.npy' % b)) if n == 8 else np.load(os.path.join(K4DIR, 'K_g0_n6_b%d.npy' % b)))
            v = np.load(kpath(n, b, None))
            m['identical_to_published'] = bool((v == ref).all()); m['n_diff'] = int((v != ref).sum())
            out.append({k: m[k] for k in ('n', 'b', 'identical_to_published', 'n_diff', 'sound_bad', 'sound_checked', 't')})
            print(out[-1], flush=True)
    json.dump(out, open(os.path.join(KCDIR, 'repro.json'), 'w'), indent=1)


def goff_of(spec, b):
    """Guard offset: an integer, or 'L' = the long guard read at 2b + 8 (notes §1.9)."""
    return b + 8 if spec == 'L' else int(spec)


def cmd_ktables(a):
    cut = None if a.cut == 'K' else a.cut
    four = None if a.four == 'none' else a.four
    jobs = [(a.n, b, cut, four, goff_of(a.goff, b), a.check, a.targeted) for b in a.budgets]
    jobs.sort(key=lambda j: -j[1])
    with Pool(a.workers) as pool:
        for m in pool.imap_unordered(_ktable_job, jobs):
            print({k: v for k, v in m.items() if k != 'uncertified_examples'}, flush=True)


# ====================================================================== dense sweeps on the named family
PANEL = [FB, 'BOX1(THEM(ME))', PB, PSTAR, 'BOX(THEM(THEM))']
NAMED = [PSTAR, P2, P12B, PS1B, PB2, PB, FB, 'BOX1(THEM(ME))', 'BOX(THEM(THEM))', 'BOX1(THEM(THEM))', 'C', 'D']
ARMS = {'K': (None, None, '0'), 'Kc': ('c', None, '0'), 'Kc4m': ('c', 'mono', '0'), 'K_g1': (None, None, '1'),
        'Kc_g1': ('c', None, '1'), 'Kc4m_g1': ('c', 'mono', '1'), 'Kc4_L': ('c4', None, 'L'), 'K_L': (None, None, 'L')}


def faker_sets():
    """Goedel set = the 21 Goedel-flagged K-disarmed classes of 'K at n = 8'; Con set = its other 16 (predictions,
    design choice 3); each with its free-arm victims."""
    fk = json.load(open(os.path.join(RUNS, 'k-at-n8-fakers.json')))
    godel = sorted(z for z, g in fk['godel'].items() if g)
    con = sorted(z for z, g in fk['godel'].items() if not g)
    return godel, con, fk['fakers']


def sweep_progs():
    godel, con, fk = faker_sets()
    victims = sorted({x for z in godel + con for x in fk[z]})
    return list(dict.fromkeys(NAMED + PANEL + godel + con + victims)), godel, con


def family_c(progs, b, arm, W=60, check=True):
    """Plays among the family at global budget b in an arm (trace-pruned as k_at_n8.family_table); soundness checks;
    the witness (minimal searched size) of every self-play atom content, independently checked; certificates for the
    self-play contents not derived (g <= 1)."""
    import k_at_n8 as KN
    cut, four, gs = ARMS[arm]; goff = goff_of(gs, b)
    t = time.time()
    K = KTheoryC(cap=max(b + goff, 1), filter_first=True, four=four, goff=goff, cut=cut)
    K.prune = KN.make_prune_trace(K, W)
    g = [K.geno(s, b) for s in progs]
    contents = set()
    for x in g:
        for y in g:
            for a in K.atoms(x, y): contents.add(K.forms[a][1])
    K.solve(sorted(contents))
    play = K.play_fn()
    val = np.array([[int(play(x, y)) for y in g] for x in g], np.int8)
    nchk, bad = K.soundness_check()
    if bad: nchk, bad = K4.closure_check(K)
    wit = {}; ck = dict(goals=0, mismatch=0, dist=0, replayed=0, fail=0)
    cert = Certifier(K, b, four=(four is not None)) if goff <= 1 else None
    for s, x in zip(progs, g):
        if s not in NAMED and s not in PANEL: continue
        row = []
        for a in K.atoms(x, x):
            A = K.forms[a][1]; T = K.T.get(A, INF)
            r = dict(atom=K.show(a), T=int(min(T, 10 ** 6)))
            if T <= K.forms[a][2] and check:
                try:
                    sz, st = check_goal(K, A); ck['goals'] += 1; ck['mismatch'] += int(sz != T)
                    ck['dist'] += st['dist']; ck['replayed'] += st['replayed']; r['checked'] = sz
                except (AssertionError, ValueError) as e:
                    ck['fail'] += 1; r['check_error'] = str(e)[:200]
            elif cert is not None and T > b and cert.gltrue(A):
                r['certificate'] = None if cert.run([A])[A] is None else 'structural'
            row.append(r)
        wit[s] = row
    meta = dict(b=b, arm=arm, goff=goff, sound_checked=nchk, sound_bad=len(bad), n_contents=len(contents),
                checker=ck, t=time.time() - t)
    return val, meta, wit


def _sweep_job(j):
    progs, b, arm = j
    val, meta, wit = family_c(progs, b, arm)
    return b, arm, val.tolist(), meta, wit


def cmd_sweep(a):
    import modal as M
    progs, godel, con = sweep_progs()
    _, _, fk = faker_sets()
    idx = {s: i for i, s in enumerate(progs)}
    path = os.path.join(KCDIR, a.out)
    out = json.load(open(path)) if os.path.exists(path) else dict(progs=progs, godel=godel, con=con, cells={})
    jobs = [(progs, b, arm) for arm in a.arms for b in (a.blist or range(a.bmin, a.bmax + 1, a.step)) if '%s/%d' % (arm, b) not in out['cells']]
    jobs.sort(key=lambda j: (j[1] if a.asc else -j[1]))
    with Pool(a.workers) as pool:
        for b, arm, val, meta, wit in pool.imap_unordered(_sweep_job, jobs):
            v = np.array(val); U, _ = M.pd_payoffs(v, M.PD)
            selfc = {s: int(v[idx[s], idx[s]]) for s in NAMED}
            inv = {z: [x for x in PANEL if U[idx[z], idx[x]] > U[idx[x], idx[x]] + 1e-12] for z in godel + con}
            endo = {z: [x for x in fk[z] if x in idx and U[idx[z], idx[x]] > U[idx[x], idx[x]] + 1e-12] for z in godel + con}
            out['cells']['%s/%d' % (arm, b)] = dict(meta=meta, self=selfc, inv_panel={z: x for z, x in inv.items() if x},
                                                    inv_free_victims={z: x for z, x in endo.items() if x},
                                                    panel_self={x: int(v[idx[x], idx[x]]) for x in PANEL}, witness=wit, val=val)
            json.dump(out, open(path, 'w'))
            print('%-8s b=%-3d sound %d/%d self %s inv-panel G %d C %d check %s %.0fs' % (
                arm, b, meta['sound_bad'], meta['sound_checked'], ''.join(str(selfc[s]) for s in NAMED),
                sum(1 for z in godel if inv[z]), sum(1 for z in con if inv[z]), meta['checker'], meta['t']), flush=True)


def cmd_structural(a):
    """Every named self-play content not derivable at b, certified at each b in [bmin, bmax] (a certificate covers
    every size at that b; no search beyond the family's K closure at cap b is needed)."""
    import k_at_n8 as KN
    progs = [PSTAR, P2, P12B, PS1B, PB2, PB]
    out = {}
    for arm, (cut, four, gs) in [(k, ARMS[k]) for k in a.arms]:
        rows = {}
        for b in range(a.bmin, a.bmax + 1):
            goff = goff_of(gs, b)
            if goff > 1: continue
            K = KTheoryC(cap=max(b + goff, 1), filter_first=True, four=four, goff=goff, cut=cut)
            K.prune = KN.make_prune_trace(K, 60)
            cert = Certifier(K, b, four=(four is not None))
            for s in progs:
                x = K.geno(s, b)
                for ai, a_ in enumerate(K.atoms(x, x)):
                    A = K.forms[a_][1]
                    if not cert.gltrue(A): continue
                    r = cert.run([A])[A]
                    key = '%s|atom%d' % (s, ai)
                    out.setdefault(arm, {}).setdefault(key, {})[b] = 'structural' if r is not None else 'uncertified'
        print(arm, {k: (sum(1 for v in d.values() if v == 'structural'), len(d)) for k, d in out.get(arm, {}).items()}, flush=True)
    json.dump(out, open(os.path.join(KCDIR, 'structural.json'), 'w'), indent=1)


# ====================================================================== chains (seeded log-domain, audited)
def _d_of(val, keep=None):
    import k_at_n8 as KN
    prov = KN.build_prov(8, val, keep)
    mu = np.array([c[2] for c in prov.classes])
    return prov, dict(U=prov.Ufull, mu=mu, K=len(mu))


def moran_log_rho(uqq, uqa, uaq, uaa, N, w, kstar):
    """Rate validation: the chain's fixation formula recomputed independently in mpmath (product form)."""
    import mpmath as mp
    mp.mp.dps = 40
    s = mp.mpf(0); prod = mp.mpf(1)
    for k in range(1, int(kstar)):
        pq = mp.mpf(k - 1) / (N - 1) * uqq + mp.mpf(N - k) / (N - 1) * uqa
        pa = mp.mpf(k) / (N - 1) * uaq + mp.mpf(N - k - 1) / (N - 1) * uaa
        prod *= mp.e ** (w * (pa - pq))
        s += prod
    return float(mp.log(1 / (1 + s)))


def chain_log(label, val, N, keep=None, twins=False, lazy=True, deep3=False, log_theta=-27.6):
    """Seeded log-domain chain (modal_dollar.seeded_chain on chain.Chain's transition model) on an n = 8 PD table:
    every monomorphic state and every deep polymorphism seeded and expanded; log-domain GTH.  Audit outputs: the
    lazy linear-domain chain on the same table and its state set (independent discovery), residual of pi against
    the explored generator, twin drift as an intervention (twins=True), and the dominant entry/exit rates
    recomputed by an independent mpmath Moran sum."""
    import modal_dollar as MD
    import k_at_n8 as KN
    t = time.time()
    prov, d = _d_of(val, keep)
    U = d['U']; P = prov.PCC; names = prov.names
    deep = MD.deep_states(d, max_types=3 if deep3 else 2)
    extra = [s for s in deep if len(s[0]) > 1]
    res = MD.seeded_chain(d, N, extra_states=extra, log_theta=log_theta, twins=twins)
    ch, keys, lpi, LA = res['ch'], res['keys'], res['lpi'], res['LA']
    pi = np.exp(lpi)
    pcc = 0.0; mono = {}; poly = 0.0; supp = []
    for k, p in zip(keys, pi):
        ids, x, kind = ch.states[k]; ids = list(ids); x = np.asarray(x)
        pcc += p * float(x @ P[np.ix_(ids, ids)] @ x)
        if len(ids) == 1: mono[ids[0]] = mono.get(ids[0], 0.0) + p
        else: poly += p
        if p >= 1e-3: supp.append((' + '.join('%s %.2f' % (names[i], xi) for i, xi in zip(ids, x)), float(p)))
    # residual of pi on the explored generator (linear domain, scaled)
    A = np.exp(LA - LA[np.isfinite(LA)].max()); A[~np.isfinite(LA)] = 0.0
    out_rate = A.sum(1); flow_in = pi @ A
    resid = float(np.abs(flow_in - pi * out_rate).sum() / max((pi * out_rate).sum(), 1e-300))
    iD = names.index('D'); iC = names.index('C')
    coop = [(v, q) for q, v in mono.items() if P[q, q] == 1 and q != iC]
    row = dict(label=label, N=N, n_classes=d['K'], pcc=float(pcc), pi_D=float(mono.get(iD, 0.0)), poly=float(poly),
               n_states=len(keys), n_deep=len(deep), n_deep_poly=len(extra), log10_cut=res['log10_cut'], residual=resid,
               twins=twins, support=sorted(supp, key=lambda s: -s[1])[:10],
               pi_mono={names[q]: float(v) for q, v in sorted(mono.items(), key=lambda kv: -kv[1]) if v >= 1e-4})
    if coop:
        v, top = max(coop); ktop = ch.mono(top); kD = ch.mono(iD)
        row.update(top_coop=names[top], pi_top=float(v))
        # dominant exit and entry with rate validation
        ex = []
        for (k1, k2, q), (rho, kstar, tk) in ch.edge_rho.items():
            if k1 == ktop and k2 != ktop:
                ex.append((d['mu'][q] * rho, q, k2, rho, kstar))
        ex.sort(reverse=True)
        tot = sum(e[0] for e in ex)
        row['exit_total'] = float(tot); row['N_exit'] = float(N * tot)
        row['exits'] = []
        for wgt, q, k2, rho, kstar in ex[:4]:
            uaa = U[top, top]
            lr = moran_log_rho(U[q, q], U[q, top], U[top, q], uaa, N, 0.3, kstar)
            row['exits'].append(dict(mutant=names[q], weight=float(wgt), rho=float(rho), N_rho=float(N * rho),
                                     kind='strict' if U[q, top] > uaa + 1e-12 else ('neutral' if abs(U[q, top] - uaa) < 1e-12 and abs(U[top, q] - uaa) < 1e-12 and abs(U[q, q] - uaa) < 1e-12 else 'other'),
                                     mp_log_rho=lr, chain_log_rho=float(np.log(max(rho, 1e-300))), mp_abs_err=float(abs(np.exp(lr) - rho))))
        ent = [(d['mu'][q] * rho, q, rho, kstar) for (k1, k2, q), (rho, kstar, tk) in ch.edge_rho.items() if k1 == kD and k2 == ktop]
        if ent:
            wgt, q, rho, kstar = max(ent)
            lr = moran_log_rho(U[q, q], U[q, iD], U[iD, q], U[iD, iD], N, 0.3, kstar)
            row['entry'] = dict(mutant=names[q], weight=float(wgt), rho=float(rho), N_rho=float(N * rho), mp_log_rho=lr,
                                chain_log_rho=float(np.log(max(rho, 1e-300))))
    row['strict_invaders_of_top'] = []
    if coop:
        uaa = U[top, top]
        row['strict_invaders_of_top'] = [names[z] for z in range(d['K']) if U[z, top] > uaa + 1e-12][:20]
    if lazy:
        from chain import Chain
        lch = Chain(prov, N=N, w=0.3, verbose=False, eager_poly=False).explore()
        lp = 0.0
        for key, wgt in zip(lch.keys_list, lch.pi):
            ids, x, kd = lch.states[key]; ids = list(ids); x = np.asarray(x)
            lp += wgt * float(x @ P[np.ix_(ids, ids)] @ x)
        sk = set(keys); lk = set(lch.keys_list)
        lpi = dict(zip(lch.keys_list, lch.pi)); spi = dict(zip(keys, pi))
        row['lazy'] = dict(pcc=float(lp), n_states=len(lk), only_seeded=len(sk - lk), only_lazy=len(lk - sk),
                           pi_only_seeded=float(sum(spi[k] for k in sk - lk)), pi_only_lazy=float(sum(lpi[k] for k in lk - sk)),
                           cut_flow=float(lch.cut_flow))
    row['t'] = time.time() - t
    return row


def _chain_job(j):
    label, n, b, cut, four, goff, N, keep, twins = j
    val = load_c(n, b, cut, four, goff) if label != 'free' else None
    if label == 'free':
        import k_at_n8 as KN
        val = KN.load_val(8, 'free')
    return chain_log(label, val, N, keep=keep, twins=twins)


def cmd_chain(a):
    path = os.path.join(KCDIR, 'chain.json')
    rows = json.load(open(path)) if os.path.exists(path) else []
    done = {(r['label'], r['N'], r['twins']) for r in rows}
    jobs = []
    for spec in a.cells:
        arm, b = spec.split('@'); b = int(b) if b != 'free' else 0
        if arm == 'free':
            lab = 'free'; cut = four = None; goff = 0
        else:
            cut, four, gs = ARMS[arm]; goff = goff_of(gs, b); lab = '%s b=%d' % (arm, b)
        for N in a.Ns:
            for tw in ([False, True] if a.twins else [False]):
                if (lab, N, tw) not in done:
                    jobs.append((lab, 8, b, cut, four, goff, N, None, tw))
    jobs.sort(key=lambda j: -j[6])
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(_chain_job, jobs):
            rows.append(r); json.dump(rows, open(path, 'w'), indent=1, default=str)
            print('%-16s N=%-6d tw=%d P(C,C) %.4f pi(D) %.3f top %s %.3f states %d deep %d resid %.1e lazy %s (%.0fs)' % (
                r['label'], r['N'], r['twins'], r['pcc'], r['pi_D'], r.get('top_coop'), r.get('pi_top', 0), r['n_states'],
                r['n_deep_poly'], r['residual'], r.get('lazy', {}).get('pcc'), r['t']), flush=True)


# ====================================================================== static analysis, grafts, factorial, lottery
def restored(v, vk, idx_victims, names):
    """Restored cooperators (self-cooperating in v, not vk) and restored exploiters against the given victims
    (strict invasion in v, not in vk), as {invader: [victims]}."""
    import modal as M
    U, _ = M.pd_payoffs(v, M.PD); Uk, _ = M.pd_payoffs(vk, M.PD)
    rc = [i for i in range(len(v)) if v[i, i] == 1 and vk[i, i] == 0]
    rex = {}
    for x in idx_victims:
        for z in range(len(v)):
            if U[z, x] > U[x, x] + 1e-12 and not (Uk[z, x] > Uk[x, x] + 1e-12):
                rex.setdefault(z, []).append(x)
    return rc, rex


def cmd_static(a):
    import k_at_n8 as KN
    L, vf, hc, hd = KN.tables(8); vf = vf.astype(np.int8)
    idx = {s: i for i, s in enumerate(L.rep)}; mu = L.mu_canon / L.mu_canon.sum()
    panel = [idx[s] for s in PANEL if s in idx]
    sup = [idx[s] for s in json.load(open(os.path.join(RUNS, 'k-at-n8-fakers.json')))['supported_selfcoop'] if s in idx]
    godel, con, _ = faker_sets()
    path = os.path.join(KCDIR, 'static.json')
    out = json.load(open(path)) if os.path.exists(path) else {}
    for spec in a.cells:
        arm, b = spec.split('@'); b = int(b); cut, four, gs = ARMS[arm]; goff = goff_of(gs, b)
        p = kpath(8, b, cut, four, goff)
        if not os.path.exists(p): continue
        v = np.load(p); m = json.load(open(p.replace('.npy', '.json')))
        vk = load_c(8, b, None, None, 0)
        ch = np.argwhere(v != vk)
        toward = int(sum(1 for i, j in ch if v[i, j] == vf[i, j]))
        rc, rex = restored(v, vk, panel, L.rep)
        _, rexs = restored(v, vk, sup, L.rep)
        lt = KN.leak_test(v)
        r = dict(meta={k: m[k] for k in m if k != 'uncertified_examples'}, uncertified_examples=m.get('uncertified_examples', [])[:10],
                 diff_vs_K=int(len(ch)), toward_free=toward, changed_mu2=float(sum(mu[i] * mu[j] for i, j in ch)),
                 diff_vs_free=int((v != vf).sum()), selfcoop=int(np.trace(v)), leak_closed=lt['n_closed'],
                 changed_examples=[(L.rep[i], L.rep[j], int(vk[i, j]), int(v[i, j])) for i, j in ch[:30]],
                 restored_coop=[L.rep[i] for i in rc], restored_coop_mu=float(mu[rc].sum()) if rc else 0.0,
                 restored_expl_panel={L.rep[z]: [L.rep[x] for x in xs] for z, xs in rex.items()},
                 restored_expl_panel_mu=float(sum(mu[z] for z in rex)),
                 restored_expl_supported={L.rep[z]: [L.rep[x] for x in xs] for z, xs in rexs.items()},
                 godel_restored=[z for z in godel if idx.get(z) in rex], con_restored=[z for z in con if idx.get(z) in rex],
                 panel_self={s: int(v[idx[s], idx[s]]) for s in PANEL if s in idx},
                 split_merge_vs_K=K4.split_merge(vk, v, mu, L.rep))
        out[spec] = r
        print(spec, {k: r[k] for k in ('diff_vs_K', 'toward_free', 'changed_mu2', 'selfcoop', 'leak_closed', 'restored_coop_mu')},
              'rc', len(rc), 'rex', len(rex), 'G', len(r['godel_restored']), 'C', len(r['con_restored']), flush=True)
        json.dump(out, open(path, 'w'), indent=1, default=str)


def cmd_catalogue(a):
    """Leak test on the cross-budget catalogue {4, 16} for an arm (K_c by default)."""
    import k_at_n8 as KN
    cut, four, gs = ARMS[a.arm]
    B = a.budgets
    L, vf, hc, hd = KN.tables(8)
    blocks = {}
    for bx in B:
        blocks[(bx, bx)] = load_c(8, bx, cut, four, goff_of(gs, bx))
    for i in range(len(B)):
        for k in range(i + 1, len(B)):
            bx, by = B[i], B[k]
            t = time.time()
            K = KTheoryC(cap=max(bx, by), filter_first=True, four=four, cut=cut)
            K.prune = KN.make_prune(K, L, hc, hd)
            gx = [K.geno(s, bx) for s in L.rep]; gy = [K.geno(s, by) for s in L.rep]
            contents = set()
            for x in gx:
                for y in gy:
                    for a_ in K.atoms(x, y) + K.atoms(y, x): contents.add(K.forms[a_][1])
            K.solve(sorted(contents))
            play = K.play_fn()
            blocks[(bx, by)] = np.array([[int(play(x, y)) for y in gy] for x in gx], np.int8)
            blocks[(by, bx)] = np.array([[int(play(y, x)) for x in gx] for y in gy], np.int8)
            nchk, bad = K.soundness_check()
            print('cross (%d, %d): sound bad %d / %d, %.0fs' % (bx, by, len(bad), nchk, time.time() - t), flush=True)
    nat = L.arrays()[0]
    const = [c for c in range(len(nat)) if nat[c] == 0]; nonc = [c for c in range(len(nat)) if nat[c] > 0]
    geno = [(c, 0) for c in const] + [(c, b) for b in B for c in nonc]
    G_ = len(geno); val = np.zeros((G_, G_), np.int8)
    for i, (ci, bi) in enumerate(geno):
        for j, (cj, bj) in enumerate(geno):
            val[i, j] = blocks[(bi or B[0], bj or B[0])][ci, cj]
    diffK = {}
    for (bx, by), blk in blocks.items():
        kp = os.path.join(KDIR8, 'kcross_n8_%d_%d.npy' % (bx, by)) if bx != by else None
        ref = np.load(kp) if kp and os.path.exists(kp) else (load_c(8, bx, None) if bx == by else None)
        if ref is not None: diffK['%d_%d' % (bx, by)] = int((ref != blk).sum())
    lt = KN.leak_test(val)
    out = dict(arm=a.arm, budgets=B, n_genotypes=G_, n_selfcoop=lt['n_selfcoop'], n_components=lt['n_components'],
               n_closed=lt['n_closed'], diff_vs_K_blocks=diffK)
    json.dump(out, open(os.path.join(KCDIR, 'catalogue_%s.json' % a.arm), 'w'), indent=1)
    print(out)


def graft_tables(b=16):
    """The frozen 2x2 restoration design (predictions, design choice 7)."""
    import k_at_n8 as KN
    L = KN.tables(8)[0]
    idx = {s: i for i, s in enumerate(L.rep)}
    vk = load_c(8, b, None); vc = load_c(8, b, 'c')
    panel = [idx[s] for s in PANEL if s in idx]
    rc, rex = restored(vc, vk, panel, L.rep)
    Rcoop = set(rc); Rexpl = set(rex)
    src = {}
    def build(coop, expl):
        v = vk.copy(); s = np.zeros(v.shape, np.int8)       # 0 = K, 1 = K_c
        if coop:
            for i in Rcoop:
                v[i, :] = vc[i, :]; v[:, i] = vc[:, i]; s[i, :] = 1; s[:, i] = 1
        if expl:
            for z, xs in rex.items():
                for x in xs:
                    v[z, x] = vc[z, x]; v[x, z] = vc[x, z]; s[z, x] = 1; s[x, z] = 1
        # consistency: every entry from exactly one source table
        assert ((s == 1) | (s == 0)).all()
        assert (v[s == 1] == vc[s == 1]).all() and (v[s == 0] == vk[s == 0]).all()
        return v, int(s.sum())
    cells = {(c, e): build(c, e) for c in (0, 1) for e in (0, 1)}
    return dict(Rcoop=[L.rep[i] for i in sorted(Rcoop)], Rexpl={L.rep[z]: [L.rep[x] for x in xs] for z, xs in rex.items()},
                overlap=[L.rep[i] for i in sorted(Rcoop & Rexpl)],
                Rcoop_mu=float(L.mu_canon[sorted(Rcoop)].sum() / L.mu_canon.sum()) if Rcoop else 0.0,
                Rexpl_mu=float(L.mu_canon[sorted(Rexpl)].sum() / L.mu_canon.sum()) if Rexpl else 0.0), cells


def _graft_job(j):
    lab, v, N = j
    return chain_log(lab, v, N, lazy=False)


def cmd_graft(a):
    info, cells = graft_tables(a.b)
    print({k: v for k, v in info.items()}, flush=True)
    # identical hybrid tables are one chain (same matrix, same pi); solve each distinct table once
    uniq = {}
    for ce, (v, ns) in cells.items():
        uniq.setdefault(v.tobytes(), []).append(ce)
    jobs = [('graft ' + '+'.join('coop=%d expl=%d' % ce for ce in ces), cells[ces[0]][0], a.N) for ces in uniq.values()]
    out = dict(info=info, n_grafted_entries={'%d%d' % ce: ns for ce, (v, ns) in cells.items()}, n_distinct_tables=len(uniq),
               identical_to_K=[('%d%d' % ce) for ce, (v, ns) in cells.items() if (v == load_c(8, a.b, None)).all()], rows=[])
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(_graft_job, jobs):
            out['rows'].append(r); print(r['label'], r['pcc'], flush=True)
    p = {}
    for r in out['rows']:
        for part in r['label'][len('graft '):].split('+'):
            p['graft ' + part] = r['pcc']
    g = lambda c, e: p['graft coop=%d expl=%d' % (c, e)]
    out['main_coop'] = g(1, 0) - g(0, 0); out['main_expl'] = g(0, 1) - g(0, 0)
    out['interaction'] = g(1, 1) - g(1, 0) - g(0, 1) + g(0, 0)
    json.dump(out, open(os.path.join(KCDIR, 'graft.json'), 'w'), indent=1, default=str)
    print({k: out[k] for k in ('main_coop', 'main_expl', 'interaction')})


def cmd_longgraft(a):
    """Exploratory: the 2x2 restoration design in the long-guard arm, where it is not degenerate.  The full n = 8
    long-guard table is not computed (a K_c4 closure at cap 2b + 8 does not fit); the donor is the long-guard family
    table at b (src/k_cut.py sweep_long.json), restricted to family members in L_8, grafted into K's n = 8 table at b
    (family-vs-nonfamily plays stay K's).  R_coop = family classes self-cooperating in the donor and not in K;
    R_expl = family classes strictly invading a fixed-panel victim or one of their free-arm victims in the donor and
    not in K."""
    import k_at_n8 as KN, modal as M
    L = KN.tables(8)[0]; idx8 = {s: i for i, s in enumerate(L.rep)}
    sw = json.load(open(os.path.join(KCDIR, 'sweep_long.json')))
    progs = sw['progs']; cell = sw['cells']['Kc4_L/%d' % a.b]; vD = np.array(cell['val'])
    fam = [(k, idx8[s]) for k, s in enumerate(progs) if s in idx8]
    vK = load_c(8, a.b, None)
    sub = np.array([[vK[i, j] for _, j in fam] for _, i in fam])
    don = np.array([[vD[k, l] for l, _ in fam] for k, _ in fam])
    U, _ = M.pd_payoffs(don, M.PD); Uk, _ = M.pd_payoffs(sub, M.PD)
    _, _, fk = faker_sets()
    loc = {progs[k]: m for m, (k, _) in enumerate(fam)}
    rc = [m for m in range(len(fam)) if don[m, m] == 1 and sub[m, m] == 0]
    rex = {}
    for z in range(len(fam)):
        vict = set(PANEL) | set(fk.get(progs[fam[z][0]], []))
        for x in [loc[v] for v in vict if v in loc]:
            if U[z, x] > U[x, x] + 1e-12 and not (Uk[z, x] > Uk[x, x] + 1e-12):
                rex.setdefault(z, []).append(x)
    def build(coop, expl):
        v = vK.copy(); src = np.zeros(v.shape, np.int8)
        def put(m, n_):
            i, j = fam[m][1], fam[n_][1]; v[i, j] = don[m, n_]; src[i, j] = 1
        if coop:
            for m in rc:
                for n_ in range(len(fam)): put(m, n_); put(n_, m)
        if expl:
            for z, xs in rex.items():
                for x in xs: put(z, x); put(x, z)
        return v
    names = lambda ms: [progs[fam[m][0]] for m in ms]
    info = dict(b=a.b, n_family_in_L8=len(fam), Rcoop=names(rc), Rexpl={progs[fam[z][0]]: names(xs) for z, xs in rex.items()},
                family_plays_differing_from_K=int((don != sub).sum()))
    print(info, flush=True)
    jobs = [('longgraft coop=%d expl=%d' % (c, e), build(c, e), a.N) for c in (0, 1) for e in (0, 1)]
    jobs.append(('longgraft all family plays', None, a.N))
    vall = vK.copy()
    for m in range(len(fam)):
        for n_ in range(len(fam)): vall[fam[m][1], fam[n_][1]] = don[m, n_]
    jobs[-1] = ('longgraft all family plays', vall, a.N)
    out = dict(info=info, rows=[])
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(_graft_job, jobs):
            out['rows'].append(r); print(r['label'], r['pcc'], r.get('top_coop'), r.get('pi_mono', {}).get('and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'), flush=True)
    p = {r['label']: r['pcc'] for r in out['rows']}
    g = lambda c, e: p['longgraft coop=%d expl=%d' % (c, e)]
    out['main_coop'] = g(1, 0) - g(0, 0); out['main_expl'] = g(0, 1) - g(0, 0)
    out['interaction'] = g(1, 1) - g(1, 0) - g(0, 1) + g(0, 0)
    json.dump(out, open(os.path.join(KCDIR, 'longgraft_b%d.json' % a.b), 'w'), indent=1, default=str)
    print({k: out[k] for k in ('main_coop', 'main_expl', 'interaction')})


def cmd_lottery(a):
    import k_at_n8 as KN, almost_all_seeds as AS
    arms = [(spec, load_c(8, int(spec.split('@')[1]), *ARMS[spec.split('@')[0]][:2], goff_of(ARMS[spec.split('@')[0]][2], int(spec.split('@')[1]))))
            for spec in a.cells]
    jobs = [(lab, 8, v, 100, 64, rep) for lab, v in arms for rep in range(a.reps)]
    rows = []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(KN.lottery_job, jobs, chunksize=1):
            rows.append(r); print(r['label'], r['rep'], r['outcome'], r['status'], '%.0fs' % r['t'], flush=True)
    summ = []
    for lab, _ in arms:
        R = [r for r in rows if r['label'] == lab]
        res = [r for r in R if r['outcome'] not in ('unresolved', None)]
        k = sum(1 for r in res if r['outcome'] == 'efficient')
        lo, hi = AS.wilson(k, len(res))
        summ.append(dict(label=lab, n=len(res), efficient=k, wilson=[lo, hi], censored=len(R) - len(res)))
        print(summ[-1])
    json.dump(dict(rows=rows, summary=summ), open(os.path.join(KCDIR, 'lottery.json'), 'w'), default=str, indent=1)


def cmd_collect(a):
    """runs/k-cut.json: every table meta, static row, sweep summary, structural table, chain row, graft, lottery."""
    out = dict(tables={}, repro=None)
    for f in sorted(os.listdir(KCDIR)):
        p = os.path.join(KCDIR, f)
        if f.endswith('.json') and ('_n6_' in f or '_n8_' in f):
            out['tables'][f[:-5]] = json.load(open(p))
    for k in ('repro', 'static', 'structural', 'chain', 'graft', 'lottery', 'catalogue_Kc', 'catalogue_Kc4_L'):
        p = os.path.join(KCDIR, k + '.json')
        if os.path.exists(p): out[k] = json.load(open(p))
    p = os.path.join(KCDIR, 'sweep.json')
    if os.path.exists(p):
        sw = json.load(open(p))
        out['sweep'] = dict(progs=sw['progs'], godel=sw['godel'], con=sw['con'],
                            cells={k: {kk: vv for kk, vv in v.items() if kk != 'val'} for k, v in sw['cells'].items()})
    json.dump(out, open(os.path.join(RUNS, 'k-cut.json'), 'w'), indent=1, default=str)
    print('wrote runs/k-cut.json', list(out))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    p = sub.add_parser('repro'); p.add_argument('--budgets8', type=int, nargs='+', default=[4, 8, 16])
    p.add_argument('--budgets6', type=int, nargs='+', default=[4, 16, 40]); p.add_argument('--workers', type=int, default=3)
    p = sub.add_parser('ktables'); p.add_argument('--n', type=int, default=8); p.add_argument('--budgets', type=int, nargs='+')
    p.add_argument('--cut', default='c'); p.add_argument('--four', default='none'); p.add_argument('--goff', default='0')
    p.add_argument('--check', action='store_true'); p.add_argument('--targeted', action='store_true')
    p.add_argument('--workers', type=int, default=3)
    p = sub.add_parser('sweep'); p.add_argument('--arms', nargs='+', default=['K', 'Kc']); p.add_argument('--bmin', type=int, default=4)
    p.add_argument('--bmax', type=int, default=54); p.add_argument('--step', type=int, default=1); p.add_argument('--workers', type=int, default=3); p.add_argument('--out', default='sweep.json'); p.add_argument('--asc', action='store_true'); p.add_argument('--blist', type=int, nargs='+')
    p = sub.add_parser('structural'); p.add_argument('--arms', nargs='+', default=['Kc', 'Kc4m', 'Kc_g1', 'Kc4m_g1'])
    p.add_argument('--bmin', type=int, default=4); p.add_argument('--bmax', type=int, default=200)
    p = sub.add_parser('chain'); p.add_argument('--cells', nargs='+'); p.add_argument('--Ns', type=int, nargs='+', default=[1000, 10000, 30000])
    p.add_argument('--twins', action='store_true'); p.add_argument('--workers', type=int, default=3)
    p = sub.add_parser('static'); p.add_argument('--cells', nargs='+')
    p = sub.add_parser('collect')
    p = sub.add_parser('catalogue'); p.add_argument('--arm', default='Kc'); p.add_argument('--budgets', type=int, nargs='+', default=[4, 16])
    p = sub.add_parser('graft'); p.add_argument('--b', type=int, default=16); p.add_argument('--N', type=int, default=10000)
    p.add_argument('--workers', type=int, default=3)
    p = sub.add_parser('longgraft'); p.add_argument('--b', type=int, default=16); p.add_argument('--N', type=int, default=10000)
    p.add_argument('--workers', type=int, default=2)
    p = sub.add_parser('lottery'); p.add_argument('--cells', nargs='+', default=['Kc@16']); p.add_argument('--reps', type=int, default=20)
    p.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    globals()['cmd_' + a.cmd](a)


if __name__ == '__main__':
    main()
