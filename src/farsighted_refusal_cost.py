"""Executable cost benchmark for the farsighted guards (notes/farsighted-refusal.md §1.8; amendment 4 of the spec).

The 20-state value solve of the contract process, written in the realizable evaluator's surface syntax
(src/lt_code.py: naturals with add / sub / mul / div / lt, pairs, recursion through library entries) as fraction-free
Gauss-Jordan (Bareiss) elimination on the integer system

    [27 N^2 (q - p) + p sum_k A_k(y)] W(y) - p sum_k A_k(y) W(x_k) = 27 N^2 (q - p) u(y),

with A_k(y) = c_{s0} c_{s1} the product of the two member slots' consenting counts (an M-matrix: off-diagonal
magnitudes, diagonals and right-hand sides stay natural numbers through elimination, so the program needs no signs
and no rounding).  Measured with lt_code.evaluate's exact step accounting:
  * reader decision: build the system from the island's guard composition, solve for the reader's player, compare
    W(x) with W(y);
  * derivation: the frozen default-selection rule (simultaneous best responses from the myopic policy, then
    asynchronous) run as code, with 3 right-hand sides per solve.
Every result is checked against the host computation.  Out-of-fuel behaviour: evaluate returns BOT.

    python3 src/farsighted_refusal_cost.py            # -> runs/farsighted-refusal-cost.json
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lt_code as L
import farsighted_refusal as F

ROOT = F.ROOT

SRC = r"""
(def fnth (l i) (if (eq i 0) (fst l) (fnth (snd l) (sub i 1))))
(def fset (l i x) (if (eq i 0) (pair x (snd l)) (pair (fst l) (fset (snd l) (sub i 1) x))))
(def fadd (l i x) (if (eq i 0) (pair (add x (fst l)) (snd l)) (pair (fst l) (fadd (snd l) (sub i 1) x))))
(def dot (a b) (if (eq a 0) 0 (add (mul (fst a) (fst b)) (dot (snd a) (snd b)))))
(def ntail (l j n) (if (eq j n) l (pair 0 (ntail l (add j 1) n))))
(def zrow (j n y d rhs) (if (eq j n) rhs (pair (if (eq j y) d 0) (zrow (add j 1) n y d rhs))))
(def mulall (c l) (if (eq l 0) 0 (pair (mul c (fst l)) (mulall c (snd l)))))
(def initm (y us d c) (if (eq us 0) 0 (pair (zrow 0 20 y d (mulall c (fst us))) (initm (add y 1) (snd us) d c))))
(def addto (M y x a) (if (eq a 0) M (fset M y (fadd (fadd (fnth M y) y a) x a))))
(def ecount (e gc)
  (let ((s0 (fst (snd (snd e)))))
    (let ((s1 (fst (snd (snd (snd e))))))
      (let ((bb (snd (snd (snd (snd e))))))
        (mul (dot (fnth gc s0) (fst bb)) (dot (fnth gc s1) (snd bb)))))))
(def buildc (M es gc p) (if (eq es 0) M
   (buildc (addto M (fst (fst es)) (fst (snd (fst es))) (mul p (ecount (fst es) gc))) (snd es) gc p)))
(def builda (M es A p) (if (eq es 0) M
   (builda (addto M (fst (fst es)) (fst (snd (fst es))) (mul p (fst A))) (snd es) (snd A) p)))
(def elimrow (ri rk k i piv prev mik j)
  (if (eq ri 0) 0
    (pair (cond ((eq j k) 0)
                ((eq j i) (div (sub (mul piv (fst ri)) (mul mik (fst rk))) prev))
                (else (div (add (mul piv (fst ri)) (mul mik (fst rk))) prev)))
          (elimrow (snd ri) (snd rk) k i piv prev mik (add j 1)))))
(def elim (rows rk k i piv prev)
  (if (eq rows 0) 0
    (pair (if (eq i k) (fst rows) (elimrow (fst rows) rk k i piv prev (fnth (fst rows) k) 0))
          (elim (snd rows) rk k (add i 1) piv prev))))
(def gj (M k prev)
  (if (eq k 20) M
    (let ((rk (fnth M k)))
      (let ((piv (fnth rk k)))
        (gj (elim M rk k 0 piv prev) (add k 1) piv)))))
(def wv (M y s) (fnth (fnth M y) (add 20 s)))
; reader: arg = (gc . (es . (us . (p . (c . (d . (s . (y . x))))))))
(def reader (arg)
  (let ((gc (fst arg)))
   (let ((es (fst (snd arg))))
    (let ((us (fst (snd (snd arg)))))
     (let ((p (fst (snd (snd (snd arg))))))
      (let ((c (fst (snd (snd (snd (snd arg)))))))
       (let ((d (fst (snd (snd (snd (snd (snd arg))))))))
        (let ((r (snd (snd (snd (snd (snd (snd arg))))))))
         (let ((M (gj (buildc (initm 0 us d c) es gc p) 0 1)))
           (if (lt (wv M (fst (snd r)) 0) (wv M (snd (snd r)) 0)) T F))))))))))
; best response of a table: es entries (y . (x . (s0 . (s1 . bits)))); 1 iff both members strictly gain
(def brl (M es)
  (if (eq es 0) 0
    (let ((e (fst es)))
      (let ((y (fst e)))
        (let ((x (fst (snd e))))
          (let ((s0 (fst (snd (snd e)))))
            (let ((s1 (fst (snd (snd (snd e))))))
              (pair (if (and (lt (wv M y s0) (wv M x s0)) (lt (wv M y s1) (wv M x s1))) 1 0) (brl M (snd es))))))))))
(def solveA (A es us p c d) (gj (builda (initm 0 us d c) es A p) 0 1))
(def br (A es us p c d) (brl (solveA A es us p c d) es))
(def member (A l) (if (eq l 0) F (if (eq A (fst l)) T (member A (snd l)))))
(def firstdiff (A B) (if (eq A 0) 0 (if (eq (fst A) (fst B)) (pair (fst A) (firstdiff (snd A) (snd B))) (pair (fst B) (snd A)))))
(def asyn (A es us p c d n)
  (let ((B (br A es us p c d)))
    (if (eq A B) (pair A n) (asyn (firstdiff A B) es us p c d (add n 1)))))
(def simul (A A0 seen es us p c d n)
  (let ((B (br A es us p c d)))
    (if (eq A B) (pair A n)
      (if (member B seen) (asyn A0 es us p c d 0) (simul B A0 (pair B seen) es us p c d (add n 1))))))
; derive: arg = (A0 . (es . (us . (p . (c . d)))))
(def derive (arg)
  (let ((A0 (fst arg)))
   (let ((es (fst (snd arg))))
    (let ((us (fst (snd (snd arg)))))
     (let ((p (fst (snd (snd (snd arg))))))
      (let ((c (fst (snd (snd (snd (snd arg)))))))
       (let ((d (snd (snd (snd (snd (snd arg)))))))
         (simul A0 A0 (pair A0 0) es us p c d 0))))))))
"""

_IDX = {}


def load():
    if _IDX:
        return _IDX
    comp = L.SxCompiler()
    comp.load(SRC)
    start = len(L.LIB)
    terms = comp.build(start)
    L.LIB.extend(terms)
    L.LIBCODE.extend([L.compile_term(t[1]) for t in terms])
    _IDX.update(comp.index)
    return _IDX


def nat(n): return ('nat', int(n))
def plist(xs): return L.plist(list(xs))
def pr(a, b): return ('pair', a, b)


def rt_to_py(v):
    if isinstance(v, int): return v
    if isinstance(v, str): return v
    if isinstance(v, tuple): return (rt_to_py(v[0]), rt_to_py(v[1]))
    return v


def py_list(v):
    out = []
    while v != 0:
        out.append(rt_to_py(v[0])); v = v[1]
    return out


def entries_term(gtabs):
    """proposal entries (y . (x . (s0 . (s1 . (bits0 . bits1))))) with per-guard consent bits of each member."""
    es = []
    for j in range(F.NP):
        y, k = int(F.PY[j]), int(F.PK[j])
        b0 = plist([nat(int(T[y, k, 0])) for T in gtabs]); b1 = plist([nat(int(T[y, k, 1])) for T in gtabs])
        es.append(pr(nat(y), pr(nat(int(F.CX[k])), pr(nat(int(F.CS_[k, 0])), pr(nat(int(F.CS_[k, 1])), pr(b0, b1))))))
    return plist(es)


def entries_plain():
    es = []
    for j in range(F.NP):
        k = int(F.PK[j])
        es.append(pr(nat(int(F.PY[j])), pr(nat(int(F.CX[k])), pr(nat(int(F.CS_[k, 0])), pr(nat(int(F.CS_[k, 1])), nat(0))))))
    return plist(es)


def coeffs(delta, N):
    d = F.dfrac(delta); p, q = d.numerator, d.denominator
    c = 27 * N * N * (q - p)
    return p, q, c


def reader_case(delta, gc, gtabs, s, y, x, N=100, K=10 ** 9):
    idx = load()
    p, q, c = coeffs(delta, N)
    us = plist([plist([nat(F.X[yy][s])]) for yy in range(F.NX)])
    gct = plist([plist([nat(v) for v in gc[t]]) for t in range(3)])
    arg = pr(gct, pr(entries_term(gtabs), pr(us, pr(nat(p), pr(nat(c), pr(nat(c), pr(nat(0), pr(nat(y), nat(x)))))))))
    # note: c serves both as the diagonal base (27 N^2 (q - p)) and the right-hand-side scale
    t = ('app', ('lib', idx['reader']), arg)
    t0 = time.time()
    v, steps = L.run_big(L.evaluate, t, K)
    wall = time.time() - t0
    # host check: the same decision from the float solve of the plug-in process
    M = np.zeros((F.NX, F.NX)); M[np.arange(F.NX), np.arange(F.NX)] = 1 - delta
    for j in range(F.NP):
        yy, k = int(F.PY[j]), int(F.PK[j])
        a = 1.0
        for z in range(2):
            sl = int(F.CS_[k, z])
            a *= sum(gc[sl][g] * int(gtabs[g][yy, k, z]) for g in range(len(gtabs))) / N
        M[yy, yy] += delta * a / 27; M[yy, F.CX[k]] -= delta * a / 27
    W = np.linalg.solve(M, (1 - delta) * F.UPAY[:, s])
    host = bool(W[x] > W[y])
    return dict(steps=int(steps), wall=wall, value=v if isinstance(v, str) else str(v), host=host,
                agree=(v == ('T' if host else 'F')), margin=float(W[x] - W[y]))


def bits_of_system(delta, N=100):
    p, q, c = coeffs(delta, N)
    acc = [1] * F.NP
    Mat, rhs = F.int_matrix(acc, delta)
    det, nums = F.bareiss_solve([[v * N * N for v in r] for r in Mat], [[v * N * N for v in r] for r in rhs])
    return int(det.bit_length())


def derive_case(delta, K=10 ** 10):
    idx = load()
    p, q, c = coeffs(delta, 1)
    us = plist([plist([nat(v) for v in F.X[yy]]) for yy in range(F.NX)])
    A0 = plist([nat(1)] * F.NP)
    arg = pr(A0, pr(entries_plain(), pr(us, pr(nat(p), pr(nat(c), nat(c))))))
    t = ('app', ('lib', idx['derive']), arg)
    t0 = time.time()
    v, steps = L.run_big(L.evaluate, t, K)
    wall = time.time() - t0
    if v == 'BOT':
        return dict(steps=int(steps), wall=wall, value='BOT')
    A = [int(b) for b in py_list(v[0])]
    n = int(v[1])
    host = F.default_policy(delta)
    return dict(steps=int(steps), wall=wall, iterations=n, agree=bool(A == [int(b) for b in host['A']]),
                host_rule=host['rule'], host_iterations=host.get('iterations'), host_flips=host.get('flips'))


def main():
    import farsighted_refusal_run as R
    out = dict(reader=[], derive={}, fuel={})
    T99, d99, W99, acc99 = R.kr_table('0.99')
    g0 = F.table_g0(); gV = F.table_gV()
    rng = np.random.default_rng(3)
    cases = []
    # monomorphic gKR-like island (the reader treats gKR / gKR-read copies as the default table)
    cases.append(('monomorphic', [[0, 100], [0, 100], [0, 100]], [g0, T99]))
    # three guards at about a third each (C3-read composition): g0, gKR, reader(=gKR table)
    cases.append(('C3-read thirds', [[34, 33, 33], [33, 34, 33], [33, 33, 34]], [g0, T99, T99]))
    cases.append(('half g0', [[50, 50], [50, 50], [50, 50]], [g0, T99]))
    cases.append(('gV, gKR, g0 thirds', [[34, 33, 33], [33, 34, 33], [33, 33, 34]], [g0, gV, T99]))
    for k in range(6):
        gc = []
        for s in range(3):
            a = rng.integers(0, 101); b = rng.integers(0, 101 - a)
            gc.append([int(a), int(b), int(100 - a - b)])
        cases.append(('random%d' % k, gc, [g0, T99, T99]))
    for lab, gc, tabs in cases:
        # a member exit from (3,3,0) offered to the buyer (slot 0) via {1,3}: kappa = (4,0,2)
        for (s, y, x) in ((0, F.RIDX[(3, 3, 0)], F.RIDX[(4, 0, 2)]), (1, F.RIDX[(4, 2, 0)], F.RIDX[(0, 3, 3)])):
            r = reader_case(0.99, gc, tabs, s, y, x)
            r.update(case=lab, s=s, y=F.LAB[y], x=F.LAB[x])
            out['reader'].append(r)
            print(lab, F.LAB[y], '->', F.LAB[x], r['steps'], r['value'], 'agree', r['agree'], '%.1fs' % r['wall'], flush=True)
    for d in (0.9, 0.95, 0.99):
        r = derive_case(d)
        out['derive'][str(d)] = r
        print('derive', d, r, flush=True)
    # fuel failure: the reader with a cap below its need returns BOT
    need = out['reader'][2]['steps']
    for frac in (0.5, 0.9, 0.999):
        r = reader_case(0.99, cases[1][1], cases[1][2], 0, F.RIDX[(3, 3, 0)], F.RIDX[(4, 0, 2)], K=int(need * frac))
        out['fuel'][str(frac)] = dict(K=int(need * frac), value=r['value'])
    out['bits_det_N100'] = {str(d): bits_of_system(d) for d in (0.9, 0.99)}
    st = [r['steps'] for r in out['reader']]
    out['reader_summary'] = dict(median=float(np.median(st)), max=int(max(st)), min=int(min(st)),
                                 all_agree=bool(all(r['agree'] for r in out['reader'])))
    json.dump(out, open(os.path.join(ROOT, 'runs', 'farsighted-refusal-cost.json'), 'w'), indent=1)
    print(out['reader_summary'], out['bits_det_N100'], out['fuel'])


if __name__ == '__main__':
    main()
