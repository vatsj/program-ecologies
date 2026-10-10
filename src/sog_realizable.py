"""The social organization game over the realizable language (specs/2026-10-10-sog-realizable.md;
notes/sog-realizable.md; predictions/2026-10-10-sog-realizable.md).

Built on src/lt_code.py, src/lt_cert.py and src/carrier_populations.py (imported, not modified).

Parts:
  1. the library extension K_3 (three-quote check wrappers CHK3 / CHK3N, the closure core, the script checker
     with outcome sets), installed into lt_code's evaluator; milestone 4's `iswrap` redefined in place so the
     check-aware self-interpreter stops at the new calls;
  2. programs: boss and worker templates compiled to L_T^code carriers with three abstractions (workers per slot),
     the probe constants, named programs;
  3. the host replay (HostCheck3, an ExactHost with the K_3 rules and the closure) and the path tactic (production);
  4. the abstract evaluator (the host replay over recorded access programs: exact semantics, fast);
  5. tables: worker-pair encounter tables E_beta, probe codes, boss maps, lumping, payoffs;
  6. whole-run plays (the term evaluator) and composition.
"""
import os
import sys
import itertools
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C
import carrier_populations as CP

N, P = L.N, L.P
C_, D_, T_, F_, TO_ = L.C_, L.D_, L.T_, L.F_, L.TO_

# ----------------------------------------------------------------------------------------------------------------
# 1. The library extension K_3
# ----------------------------------------------------------------------------------------------------------------
M_CAP = 8           # closure capacity (notes §1.1.3)
CERT3_SRC = r"""
; ---------------- K_3: three-quote check wrappers and cores ----------------
(def CHK3 (arg) (if (eq (capk (fst arg) CC3 arg) T) T F))
(def CHK3N (arg) (if (eq (capk (fst arg) CC3N arg) T) T F))
(def CC3 (arg) (ccore3 0 arg))
(def CC3N (arg) (ccore3 1 arg))
(def iswrap3 (n) (or (eq n ID_CHK3) (eq n ID_CHK3N)))
(def callcheck3 (n ad) (if (eq n ID_CHK3) (capk (fst ad) CC3 ad) (capk (fst ad) CC3N ad)))
(def lapp (a b) (if (eq a 0) b (pair (fst a) (lapp (snd a) b))))
(def amem (v l) (if (eq l 0) F (if (eq (fst l) v) T (amem v (snd l)))))
(def subjq (enc j) (cond ((eq j 0) (fst enc)) ((eq j 1) (fst (snd enc))) (else (snd (snd enc)))))
(def app3 (f x y z) (mkapp (mkapp (mkapp f (pair 10 x)) (pair 10 y)) (pair 10 z)))
(def mkconf3 (enc j)
  (let ((b (fst enc)) (w1 (fst (snd enc))) (w2 (snd (snd enc))))
    (cond ((eq j 0) (app3 b b w1 w2))
          ((eq j 1) (app3 w1 w1 b w2))
          (else (app3 w2 w2 b w1)))))
(def getcerts3 (t)
  (if (eq (fst t) 1)
    (let ((b1 (snd t)))
      (if (eq (fst b1) 1)
        (let ((b2 (snd b1)))
          (if (eq (fst b2) 1)
            (let ((b3 (snd b2)))
              (if (eq (fst b3) 2)
                (let ((l (snd b3)))
                  (if (eq (fst (fst l)) 1) (full (fst (snd l))) NONE))
                NONE))
            NONE))
        NONE))
    NONE))

; ---------------- the check: root validation, then the uniform-cost closure ----------------
(def ccore3 (x arg)
  (let ((n (if (eq x 0) ID_CHK3 ID_CHK3N)) (r1 (vone3 n arg)))
    (if (eq r1 0) F
      (if (eq x 1) T
        (clos3 n (snd r1) (setnth DONE0 0 arg) 1)))))
(def clos3 (n todo done cnt)
  (if (eq todo 0) T
    (let ((y (fst todo)) (rest (snd todo)))
      (if (scanm y done F)
          (clos3 n rest done cnt)
          (if (eq cnt MCAP) F
              (let ((r (vone3 n y)))
                (if (eq r 0) F
                    (clos3 n (lapp (snd r) rest) (setnth done cnt y) (add cnt 1)))))))))
(def scanm (y d acc) (if (eq d 0) acc (scanm y (snd d) (if (eq (fst d) y) T acc))))
(def vone3 (n x)
  (let ((r (snd x)) (enc (fst r)) (j (fst (snd r))) (A (fst (snd (snd r)))) (K (snd (snd (snd r))))
        (cl (getcerts3 (subjq enc j))))
    (if (eq cl NONE) 0
      (tryents3 (pair n (pair (pair 8 (pair n x)) x)) cl A (mkatom (mkconf3 enc j) K A 0)))))
(def tryents3 (cx cl A psi)
  (if (eq cl 0) 0
    (let ((e (fst cl)))
      (if (eq (fst e) A)
          (let ((v (cchk3 cx (snd e) 0 (pair psi 0))))
            (if (eq v 0) (tryents3 cx (snd cl) A psi) v))
          (tryents3 cx (snd cl) A psi)))))

; ---------------- the script checker; returns 0 (invalid) or (1 . used encounter-box arguments) ----------------
(def cchk3 (cx node L R)
  (let ((rule (fst node)) (j (fst (snd node))) (ps (snd (snd node))))
    (cond ((eq rule 0) (if (caxiom L R) VALID0 0))
          ((eq rule 3) (chyp3 cx (fnth R j)))
          ((eq rule 1) (crun3 cx (fnth R j) 1))
          ((eq rule 2) (crun3 cx (fnth L j) 0))
          ((eq rule 26) (cev3 cx ps L R (fnth R j)))
          ((eq rule 25) (cchkr3 cx ps L R (fnth R j)))
          (else 0))))
(def isenc (cx b)
  (if (eq b NONE) F
    (if (not (eq (fst b) 8)) F
      (let ((p (snd b)) (x (snd (snd cx))) (ad (snd p)))
        (and (eq (fst p) (fst cx))
             (and (eq (fst ad) (fst x))
                  (and (eq (fst (snd ad)) (fst (snd x)))
                       (eq (snd (snd (snd (snd ad)))) (snd (snd (snd (snd x))))))))))))
(def chyp3 (cx b) (if (isenc cx b) (pair 1 (pair (snd (snd b)) 0)) 0))
(def crun3 (cx b want)
  (if (eq b NONE) 0
    (if (not (eq (fst b) 8)) 0
      (if (eq b (fst (snd cx))) 0
        (let ((p (snd b)) (n (fst p)) (ad (snd p)))
          (if (and (iswrap3 n) (le (fst (snd (snd cx))) (fst ad)))
              (let ((v (callcheck3 n ad)))
                (if (eq want 1) (if (eq v T) VALID0 0) (if (eq v T) 0 VALID0)))
              0))))))
(def cev3 (cx ps L R x)
  (if (or (eq x NONE) (not (eq (fst x) 6))) 0
    (let ((p (snd x)) (conf (fst p)) (f (fst (snd p))) (a (fst (snd (snd p)))) (m (snd (snd (snd p))))
          (r (cstep conf)))
      (if (and (lt 0 f) (eq (fst r) 2))
          (cchk3 cx (fst ps) L (fadd (evfrom3 r f a m) (fdel x R)))
          0))))
(def evfrom3 (r f a m)
  (let ((d (snd r)))
    (if (and (eq m 1) (eq (snd d) 1)) BOTF (evstar3 (fst d) (sub f 1) a m))))
(def evstar3 (conf f a m)
  (let ((r (cstep conf)) (rk (fst r)))
    (cond ((eq rk 0) (if (amem (full conf) a) TOPF BOTF))
          ((eq rk 1) BOTF)
          ((eq f 0) BOTF)
          ((eq rk 2) (evfrom3 r f a m))
          (else (mkatom conf f a m)))))
(def creading3 (conf f a)
  (let ((r (cstep conf)) (rk (fst r)))
    (cond ((eq rk 0) (if (amem (full conf) a) TOPF BOTF))
          ((eq rk 1) BOTF)
          ((eq f 0) BOTF)
          (else (mkatom conf f a 1)))))
(def chkstate3 (conf f a)
  (if (eq f 0) 0
    (let ((r (cstep conf)))
      (if (eq (fst r) 3)
          (let ((s (snd r)) (n (fst s)) (arg (fst (snd s))) (frames (snd (snd s))))
            (if (and (iswrap3 n) (cargok arg))
                (let ((ad (full arg)) (u (add (fst ad) 6)))
                  (if (and (le u f) (allfit frames u))
                      (pair (pair 8 (pair n ad))
                            (pair (creading3 (plug frames TENC u) (sub f u) a)
                                  (creading3 (plug frames FENC u) (sub f u) a)))
                      0))
                0))
          0))))
(def cchkr3 (cx ps L R x)
  (if (or (eq x NONE) (not (eq (fst x) 6))) 0
    (let ((p (snd x)) (s (chkstate3 (fst p) (fst (snd p)) (fst (snd (snd p))))))
      (if (eq s 0) 0
        (let ((B (fst s)) (Rx (fdel x R))
              (v1 (cchk3 cx (fst ps) (fadd B L) (fadd (fst (snd s)) Rx))))
          (if (eq v1 0) 0
            (let ((v2 (cchk3 cx (fst (snd ps)) L (fadd B (fadd (snd (snd s)) Rx)))))
              (if (eq v2 0) 0 (pair 1 (lapp (snd v1) (snd v2)))))))))))
"""

ISWRAP_OLD = "(def iswrap (n) (or (eq n ID_CHKS) (or (eq n ID_CHKS2) (or (eq n ID_CHKN) (or (eq n ID_CHKO) (or (eq n ID_CHKX) (eq n ID_CHKL)))))))"
ISWRAP_NEW = ("(def iswrap (n) (or (eq n ID_CHKS) (or (eq n ID_CHKS2) (or (eq n ID_CHKN) (or (eq n ID_CHKO) (or (eq n ID_CHKX) "
              "(or (eq n ID_CHKL) (or (eq n ID_CHK3) (eq n ID_CHK3N)))))))))")
CERT3_CONSTS = {'VALID0': ['pair', 1, 0], 'MCAP': M_CAP, 'DONE0': ['list'] + ['NONE'] * M_CAP}
MODE3, MODE3N = 30, 31
ID3 = {}


def build_library3():
    assert ISWRAP_OLD in C.CERT_SRC
    comp = L.SxCompiler()
    for k, v in L.LIB_CONSTS.items(): comp.consts[k] = v
    for k, v in C.CERT_CONSTS.items(): comp.consts[k] = v
    for k, v in CERT3_CONSTS.items(): comp.consts[k] = v
    comp.load(L.LIBRARY_SRC)
    comp.load(C.CERT_SRC.replace(ISWRAP_OLD, ISWRAP_NEW))
    comp.load(CERT3_SRC)
    for nm in C.WRAP_NAMES + ['CHK3', 'CHK3N']: comp.consts['ID_' + nm] = comp.order.index(nm)
    comp.consts['NLIB'] = len(comp.order)
    terms = comp.build(0)
    L.LIB[:] = terms
    L.LIBNAME.clear(); L.LIBNAME.update({i: n for i, n in enumerate(comp.order)})
    L.LIBIDX.clear(); L.LIBIDX.update(comp.index)
    L.SEARCH_LIBS.clear(); L.SEARCH_LIBS.update({L.LIBIDX['SEARCH%d' % i]: i for i in range(3)})
    L.CORE_LIBS.clear(); L.CORE_LIBS.update({L.LIBIDX['CORE%d' % i]: i for i in range(3)})
    for nm, mode in C.CORE_NAMES.items(): L.CORE_LIBS[L.LIBIDX[nm]] = C.CORE_ID_BASE + mode
    L.CORE_LIBS[L.LIBIDX['CC3']] = 40
    L.CORE_LIBS[L.LIBIDX['CC3N']] = 41
    L._compiled.clear()
    L.LIBCODE[:] = [L.compile_term(t[1]) for t in terms]
    L.CACHE.clear()
    C.ID.clear(); C.ID.update({nm: L.LIBIDX[nm] for nm in C.WRAP_NAMES})
    C.WRAPS.clear(); C.WRAPS.update(C.ID.values())
    C.CC_MODE.clear(); C.CC_MODE.update({L.LIBIDX[nm]: mode for nm, mode in C.CORE_NAMES.items()})
    C.WRAP_MODE.clear(); C.WRAP_MODE.update({L.LIBIDX[C.MODE_WRAP[m]]: m for m in C.MODE_WRAP})
    ID3.clear(); ID3.update({'CHK3': L.LIBIDX['CHK3'], 'CHK3N': L.LIBIDX['CHK3N'],
                             'CC3': L.LIBIDX['CC3'], 'CC3N': L.LIBIDX['CC3N']})
    C.WRAPS.update([ID3['CHK3'], ID3['CHK3N']])
    C.WRAP_MODE[ID3['CHK3']] = MODE3
    C.WRAP_MODE[ID3['CHK3N']] = MODE3N
    return comp


_COMP3 = build_library3()
WRAP3 = {MODE3: ID3['CHK3'], MODE3N: ID3['CHK3N']}
CORE3 = {MODE3: ID3['CC3'], MODE3N: ID3['CC3N']}
assert L.LIBIDX['CHKS'] == C.ID['CHKS']

# ----------------------------------------------------------------------------------------------------------------
# 2. Programs
# ----------------------------------------------------------------------------------------------------------------
K_MAIN = 10 ** 6
WAGE = [0.0, 0.25, 0.5]
HN = ['strike', 'none', 'source']
A_GE14 = tuple(range(3, 9))      # wage >= 1/4
A_EQ12 = (6, 7, 8)               # wage = 1/2
A_LE14 = tuple(range(0, 6))      # wage <= 1/4
A_WORK, A_STRIKE = ('C',), ('D',)
BOSS_Q = [A_GE14, A_EQ12, A_LE14]          # the boss question family (notes §1.1.1)
WORKER_Q = [A_WORK, A_STRIKE]
ANAME = {A_GE14: '>=1/4', A_EQ12: '=1/2', A_LE14: '<=1/4', A_WORK: 'work', A_STRIKE: 'strike'}


def bcode(si, hi): return 3 * si + hi
def bname(b): return 'pay(%s,%s)' % (['0', '1/4', '1/2'][b // 3], HN[b % 3])


def cons(xs): return C.cons(list(xs))


def a_term(A):
    """An outcome set (tuple of codes / constructor names) -> its literal data term (a cons list)."""
    return C.data_term(cons(A))


def carrier3(body, certs):
    """lam me. lam x. lam y. (lam certs. body) CERTS."""
    return ('lam', ('lam', ('lam', ('app', ('lam', body), C.data_term(certs)))))


# inside BODY: certs = v0, y = v1, x = v2, me = v3
ME, VX, VY = ('v', 3), ('v', 2), ('v', 1)


def ARG3(V, enc, j, A, K):
    return P(N(V), P(enc, P(N(j), P(a_term(A), N(K)))))


def CALL3(V, enc, j, A, K, naive=False):
    return ('app', ('lib', ID3['CHK3N' if naive else 'CHK3']), ARG3(V, enc, j, A, K))


def initial3(p, x, y):
    return ('app', ('app', ('app', p, ('quote', p)), ('quote', x)), ('quote', y))


def conf_term(enc, j):
    b, w1, w2 = enc
    if j == 0: return initial3(b, w1, w2)
    if j == 1: return initial3(w1, b, w2)
    return initial3(w2, b, w1)


def mk_arg3(V, enc, j, A, K):
    """The term-level argument value of a check about subject j of the encounter enc = (b, w1, w2) (program terms)."""
    b, w1, w2 = enc
    return P(N(V), P(P(('quote', b), P(('quote', w1), ('quote', w2))), P(N(j), P(a_term(A), N(K)))))


# ---- templates.  Worker atoms: ('B', A) about the boss; ('O', A) about the other worker.  Boss atoms:
#      ('P', j, s', A) probe of worker j against pay(s', none).  Leaves: workers 'W'/'S'; bosses int codes.
WORKER_ATOMS = [('B', A_GE14), ('B', A_EQ12), ('B', A_LE14), ('O', A_STRIKE), ('O', A_WORK)]
BOSS_ATOMS = [('P', j, s, A) for j in (1, 2) for s in (0, 1) for A in (A_WORK, A_STRIKE)]   # s: 0 -> 0, 1 -> 1/4
PROBE_S = {0: 0, 1: 1}     # probe wage index -> quoted constant boss pay(s, none) code index si


def atom_name(at):
    if at[0] == 'B': return 'B%s' % {A_GE14: '>=1/4', A_EQ12: '=1/2', A_LE14: '<=1/4'}[at[1]]
    if at[0] == 'O': return 'O:%s' % ('S' if at[1] == A_STRIKE else 'W')
    if at[0] == 'C': return 'W%d:%s' % (at[1], 'S' if at[2] == A_STRIKE else 'W')
    return 'P%d^%s:%s' % (at[1], ['0', '1/4'][at[2]], 'S' if at[3] == A_STRIKE else 'W')


def leaf_name(l):
    if l == 'W': return 'work'
    if l == 'S': return 'strike'
    return bname(l)


def show(x):
    t = x[0]
    if t == 'L': return leaf_name(x[1])
    if t == 'A': return atom_name(x[1])
    if t == 'not': return 'not(%s)' % show(x[1])
    if t in ('and', 'or'): return '%s(%s,%s)' % (t, show(x[1]), show(x[2]))
    return 'if(%s,%s,%s)' % (show(x[1]), show(x[2]), show(x[3]))


def enumerate_templates(nmax, atoms, leaves):
    """All actions with <= nmax nodes: {n: [templates]}; conditions ('A', atom) | ('not', B) | ('and'|'or', B, B);
    actions ('L', leaf) | ('if', B, A, A)."""
    B, A = {}, {}
    for n in range(1, nmax + 1):
        if n == 1:
            B[n] = [('A', a) for a in atoms]; continue
        out = [('not', b) for b in B[n - 1]]
        for i in range(1, n - 1):
            for b1 in B[i]:
                for b2 in B[n - 1 - i]:
                    out.append(('and', b1, b2)); out.append(('or', b1, b2))
        B[n] = out
    for n in range(1, nmax + 1):
        if n == 1:
            A[n] = [('L', l) for l in leaves]; continue
        out = []
        for i in range(1, n):
            for j in range(1, n):
                k = n - 1 - i - j
                if k < 1: continue
                for b in B.get(i, []):
                    for x in A.get(j, []):
                        for y in A.get(k, []):
                            out.append(('if', b, x, y))
        A[n] = out
    return A


def nodes(x):
    t = x[0]
    if t in ('L', 'A'): return 1
    return 1 + sum(nodes(c) for c in x[1:])


def _bt(b, t, f):
    if b[0] == 'A': return (b[1], t, f)
    if b[0] == 'not': return _bt(b[1], f, t)
    if b[0] == 'and': return _bt(b[1], _bt(b[2], t, f), f)
    return _bt(b[1], t, _bt(b[2], t, f))


def dt(x):
    """The run tree: (atom, T-subtree, F-subtree) or a leaf value."""
    if x[0] == 'L': return x[1]
    return _bt(x[1], dt(x[2]), dt(x[3]))


def dt_atoms(t):
    if not isinstance(t, tuple): return []
    out = [t[0]]
    for c in (t[1], t[2]):
        for a in dt_atoms(c):
            if a not in out: out.append(a)
    return out


def dt_eval(t, val):
    while isinstance(t, tuple):
        t = t[1] if val(t[0]) else t[2]
    return t


def show_dt(t):
    if not isinstance(t, tuple): return leaf_name(t)
    return '%s?%s:%s' % (atom_name(t[0]), show_dt(t[1]), show_dt(t[2]))


def tagged(t):
    return any(a[0] == 'O' for a in dt_atoms(t))


# ---- compilation
LEAFVAL = {'W': 'C', 'S': 'D'}       # worker leaves as output values


def leaf_term(l):
    if l == 'W': return C_
    if l == 'S': return D_
    return N(l)


def worker_enc(slot):
    return P(VX, P(ME, VY)) if slot == 1 else P(VX, P(VY, ME))


def atom_term(at, role, slot, V, K, naive=False, misorder=False):
    """misorder (corrupted instance 1): a worker that builds its encounters as if it were in slot 1."""
    if role == 'W':
        bs = 1 if misorder else slot
        enc = worker_enc(bs)
        if at[0] == 'B':
            return CALL3(V, enc, 0, at[1], K, naive)
        return CALL3(V, enc, 2 if bs == 1 else 1, at[1], K, naive)
    if at[0] == 'C':          # current-encounter boss atom (out of grammar: C1, corrupted instances)
        return CALL3(V, P(ME, P(VX, VY)), at[1], at[2], K, naive)
    _, j, s, A = at
    enc = P(('quote', probe_const(s, V, K)), P(VX, VY))
    return CALL3(V, enc, j, A, K, naive)


def cond_term(b, role, slot, V, K, **kw):
    if b[0] == 'A': return atom_term(b[1], role, slot, V, K, **kw)
    if b[0] == 'not': return ('if', cond_term(b[1], role, slot, V, K, **kw), F_, T_)
    if b[0] == 'and': return ('if', cond_term(b[1], role, slot, V, K, **kw), cond_term(b[2], role, slot, V, K, **kw), F_)
    return ('if', cond_term(b[1], role, slot, V, K, **kw), T_, cond_term(b[2], role, slot, V, K, **kw))


def body_term(x, role, slot, V, K, **kw):
    if x[0] == 'L': return leaf_term(x[1])
    return ('if', cond_term(x[1], role, slot, V, K, **kw), body_term(x[2], role, slot, V, K, **kw),
            body_term(x[3], role, slot, V, K, **kw))


_PROBE_CONST = {}


def probe_const(s, V, K):
    """The quoted constant boss pay(s, none) (s: 0 -> wage 0, 1 -> 1/4) with its produced list."""
    key = (s, V, K)
    p = _PROBE_CONST.get(key)
    if p is None:
        code = bcode(PROBE_S[s], 1)
        lst = constant_list(code)
        p = carrier3(N(code), lst)
        _PROBE_CONST[key] = p
    return p


SCRIPT_CONST = C.node(C.EVS, 0, C.node(C.AX, 0))


def constant_list(code):
    """A constant boss's list: EvR*; Ax for every question set containing its code (what the path tactic produces
    for a program without calls; checked against the tactic in the tests)."""
    return cons([(cons(A), SCRIPT_CONST) for A in BOSS_Q if code in A])


# ----------------------------------------------------------------------------------------------------------------
# 3. Host replay (HostCheck3) and the path tactic
# ----------------------------------------------------------------------------------------------------------------
WRAPS3 = {ID3['CHK3'], ID3['CHK3N']}


def valdata(t):
    if t[0] == 'nat': return t[1]
    if t[0] == 'con': return t[1]
    return None


def aset(A):
    return set(C.uncons(A)) if A != 0 else set()


def h_read3(t, f, A, m):
    ctx, kind, pay, ito = C.hdecompose(t)
    if kind == 'value': return C.TOPH if valdata(t) in aset(A) else C.BOTH
    if kind == 'stuck': return C.BOTH
    if f == 0: return C.BOTH
    return ('atom', t, f, A, m)


def h_evstar3(phi, budget=None):
    """EvR* with outcome sets (milestone 4's h_evstar otherwise)."""
    _, t, f, A, m = phi
    if f < 1: return None
    ctx, kind, pay, ito = C.hdecompose(t)
    if kind != 'det': return None
    n = 0; w = 0
    while True:
        n += 1
        w += 1 + len(ctx)
        if budget is not None and w > budget: raise C.HostAbort()
        if m == 1 and ito: return C.BOTH, n
        t = L.plug(ctx, pay); f -= 1
        ctx, kind, pay, ito = C.hdecompose(t)
        if kind == 'value': return (C.TOPH if valdata(t) in aset(A) else C.BOTH), n
        if kind == 'stuck' or f == 0: return C.BOTH, n
        if kind != 'det': return ('atom', t, f, A, m), n


def h_chkstate3(phi):
    _, t, f, A, m = phi
    if f == 0: return None
    ctx, kind, pay, ito = C.hdecompose(t)
    if kind != 'call': return None
    n, v = pay
    if n not in WRAPS3: return None
    Vc = C.parse_carg(v)
    if Vc is None: return None
    u = Vc + 6
    fuels = [fr[1] for fr in ctx if fr[0] == 'sim']
    if not (u <= f and all(k >= u for k in fuels)): return None
    fr = f - u
    return (('cbox', n, v), h_read3(L.plug(ctx, T_, u), fr, A, 1), h_read3(L.plug(ctx, F_, u), fr, A, 1))


def parse_arg3(v):
    """Argument value -> (V, ENC term, (b, w1, w2) program terms, j, A data, K) or None."""
    try:
        assert v[0] == 'pair' and v[1][0] == 'nat'
        V = v[1][1]; r = v[2]; ENC = r[1]; r2 = r[2]; j = r2[1]; r3 = r2[2]; At = r3[1]; Kt = r3[2]
        assert j[0] == 'nat' and Kt[0] == 'nat'
        qb = ENC[1]; qw1 = ENC[2][1]; qw2 = ENC[2][2]
        assert qb[0] == 'quote' and qw1[0] == 'quote' and qw2[0] == 'quote'
        return V, ENC, (qb[1], qw1[1], qw2[1]), j[1], C.term_data(At), Kt[1]
    except Exception:
        return None


def h_getcerts3(prog):
    try:
        if prog[0] == 'lam' and prog[1][0] == 'lam' and prog[1][1][0] == 'lam' and prog[1][1][1][0] == 'app' \
                and prog[1][1][1][1][0] == 'lam':
            return C.term_data(prog[1][1][1][2])
    except Exception:
        return None
    return None


class HostCheck3(CP.ExactHost):
    """milestone 4's host replay with milestone 2's exact memo (ExactHost), extended by the K_3 rules of notes
    §1.1.3: three-quote roots, outcome sets, Hyp on encounter boxes with the closure, Run/RunNeg on any box but the
    own root.  ideal=True removes the EvR* step budget (the ideal-verification table); `seed` pre-sets clean values of
    given boxes (used for the boss-view columns of the encounter tables: notes §1.3.2)."""

    def __init__(self, ideal=True):
        super().__init__()
        self.ideal = ideal

    def seed(self, n, v, val):
        self.memo[(n, v)] = val
        self.deps[(n, v)] = set()

    def _ccore(self, mode, v):
        if mode not in (MODE3, MODE3N):
            return super()._ccore(mode, v)
        n = WRAP3[mode]
        r = self._vone3(n, v)
        if r is None: return 'F'
        if mode == MODE3N: return 'T'
        done = [v]
        todo = list(r)
        while todo:
            y = todo.pop(0)
            if y in done: continue
            if len(done) >= M_CAP: return 'F'
            ry = self._vone3(n, y)
            if ry is None: return 'F'
            todo = list(ry) + todo
            done.append(y)
        return 'T'

    def _vone3(self, n, v):
        fs = parse_arg3(v)
        if fs is None: return None
        V, ENC, enc, j, A, K = fs
        if j not in (0, 1, 2): return None
        cl = h_getcerts3(enc[j])
        if cl is None: return None
        ents = C.uncons(cl) if cl != 0 else []
        psi = ('atom', conf_term(enc, j), K, A, 0)
        Rb = ('cbox', n, v)
        xf = (n, V, ENC, K)
        for e in ents:
            if not isinstance(e, tuple) or e[0] != A: continue
            r = self.cchk3(n, Rb, xf, V, e[1], (), (psi,))
            if r is not None: return r
        return None

    @staticmethod
    def isenc(xf, b):
        if b is None or b[0] != 'cbox' or b[1] != xf[0]: return False
        fs = parse_arg3(b[2])
        if fs is None: return False
        return fs[0] == xf[1] and fs[1] == xf[2] and fs[5] == xf[3]

    def cchk3(self, n, Rb, xf, V, nd, Lf, Rf):
        try:
            rule, (j, ps) = nd
            ps = C.uncons(ps)
        except Exception:
            return None

        def at(lst, j):
            return lst[j] if isinstance(j, int) and 0 <= j < len(lst) else None
        if rule == C.AX:
            if C.BOTH in Lf or C.TOPH in Rf or any(x in Rf and x[0] in ('atom', 'cbox') for x in Lf): return []
            return None
        if rule == C.HYP:
            b = at(Rf, j)
            return [b[2]] if self.isenc(xf, b) else None
        if rule in (C.RUN, C.RUNNEG):
            b = at(Rf if rule == C.RUN else Lf, j)
            if b is None or b[0] != 'cbox' or b == Rb or b[1] not in WRAPS3: return None
            Vb = C.parse_carg(b[2])
            if Vb is None or Vb < V: return None
            res = self.check(b[1], b[2])
            return [] if (res == 'T') == (rule == C.RUN) else None
        if rule == C.EVS:
            x = at(Rf, j)
            if x is None or x[0] != 'atom' or not ps: return None
            s = h_evstar3(x, None if self.ideal else V // C.HOST_STEP_COST)
            if s is None: return None
            return self.cchk3(n, Rb, xf, V, ps[0], Lf, C.fadd(s[0], C.fdel(x, Rf)))
        if rule == C.CHKR:
            x = at(Rf, j)
            if x is None or x[0] != 'atom' or len(ps) < 2: return None
            s = h_chkstate3(x)
            if s is None: return None
            B, rT, rF = s
            Rx = C.fdel(x, Rf)
            v1 = self.cchk3(n, Rb, xf, V, ps[0], C.fadd(B, Lf), C.fadd(rT, Rx))
            if v1 is None: return None
            v2 = self.cchk3(n, Rb, xf, V, ps[1], Lf, C.fadd(B, C.fadd(rF, Rx)))
            if v2 is None: return None
            return v1 + v2
        return None

    def check3(self, enc, j, A, V, K, mode=MODE3):
        """Clean value of the check about subject j of encounter enc (program terms): 'T' | 'F' | 'TO'."""
        return self.check(WRAP3[mode], mk_arg3(V, enc, j, A, K))


# ---- the path tactic on the host (notes §1.1.4)
DUMMY_B = carrier3(N(1), 998)
DUMMY_W1 = carrier3(C_, 997)
DUMMY_W2 = carrier3(C_, 999)


def production_encounter(prog0, role, slot):
    if role == 'B': return (prog0, DUMMY_W1, DUMMY_W2), 0
    if slot == 1: return (DUMMY_B, prog0, DUMMY_W2), 1
    return (DUMMY_B, DUMMY_W1, prog0), 2


def atom_box(at, enc, j, V, K, role, naive=False):
    """The box (host form) of a template atom asked by subject j of the encounter enc."""
    n = ID3['CHK3N' if naive else 'CHK3']
    if role == 'W':
        if at[0] == 'B': return ('cbox', n, mk_arg3(V, enc, 0, at[1], K))
        return ('cbox', n, mk_arg3(V, enc, 2 if j == 1 else 1, at[1], K))
    if at[0] == 'C': return ('cbox', n, mk_arg3(V, enc, at[1], at[2], K))
    _, jj, s, A = at
    return ('cbox', n, mk_arg3(V, (probe_const(s, V, K), enc[1], enc[2]), jj, A, K))


class PathProducer:
    """The path tactic: the frozen tactic driven by an assignment (notes §1.1.4).  Returns the script and its
    access program (the Run / RunNeg / Hyp leaves in the checker's evaluation order)."""
    BOUND = 64

    def __init__(self, naive=False):
        self.naive = naive

    def produce(self, prog0, role, slot, A, alpha_atoms, V, K):
        enc, j = production_encounter(prog0, role, slot)
        self.alpha = {atom_box(at, enc, j, V, K, role, self.naive): val for at, val in alpha_atoms.items()}
        self.box_atom = {atom_box(at, enc, j, V, K, role, self.naive): at for at in alpha_atoms}
        self.enc = enc; self.j = j; self.role = role
        self.count = 0
        root = ('atom', conf_term(enc, j), K, cons(A), 0)
        acc = []
        try:
            s = self.tac((), (root,), acc)
        except (C.HostAbort, RecursionError):
            return None, None
        return s, (None if s is None else acc)

    def worker_enc_box(self, b):
        fs = parse_arg3(b[2])
        return fs is not None and fs[2] == self.enc and fs[3] in (1, 2)

    def tac(self, Lf, Rf, acc):
        self.count += 1
        if self.count > self.BOUND: return None
        if C.BOTH in Lf or C.TOPH in Rf or any(x in Rf and x[0] in ('atom', 'cbox') for x in Lf): return C.node(C.AX, 0)
        for jj, b in enumerate(Rf):
            if b[0] == 'cbox' and self.alpha.get(b) is True:
                if self.worker_enc_box(b):
                    acc.append(('H', self.box_atom[b])); return C.node(C.HYP, jj)
                acc.append(('R', self.box_atom[b])); return C.node(C.RUN, jj)
        for jj, b in enumerate(Lf):
            if b[0] == 'cbox' and self.alpha.get(b) is False:
                acc.append(('N', self.box_atom[b])); return C.node(C.RUNNEG, jj)
        for jj, x in enumerate(Rf):
            if x[0] != 'atom': continue
            s = h_evstar3(x)
            if s is not None:
                p = self.tac(Lf, C.fadd(s[0], C.fdel(x, Rf)), acc)
                return None if p is None else C.node(C.EVS, jj, p)
            c = h_chkstate3(x)
            if c is not None:
                B, rT, rF = c
                if B not in self.alpha: return None
                Rx = C.fdel(x, Rf)
                p1 = self.tac(C.fadd(B, Lf), C.fadd(rT, Rx), acc)
                if p1 is None: return None
                p2 = self.tac(Lf, C.fadd(B, C.fadd(rF, Rx)), acc)
                if p2 is None: return None
                return C.node(C.CHKR, jj, p1, p2)
            return None
        return None


# ---- the same tactic on the run tree (symbolic formulas; validated against PathProducer: tests, notes §1.x)
TOPS, BOTS = ('top',), ('bot',)


def sym_produce(t, role, A, alpha):
    """Path tactic over the run tree t with formulas ('pre', path) / ('call', path) / ('box', atom) / top / bot.
    alpha: dict atom -> bool.  Returns (script, access program) or (None, None)."""
    Aset_ = set(A)
    count = [0]

    def node_at(path):
        x = t
        for br in path:
            x = x[1] if br else x[2]
        return x

    def evstar(phi):
        k, path = phi
        if k != 'pre': return None
        x = node_at(path)
        if not isinstance(x, tuple): return TOPS if LEAFVAL.get(x, x) in Aset_ else BOTS
        return ('call', path)

    def tac(Lf, Rf, acc):
        count[0] += 1
        if count[0] > PathProducer.BOUND: return None
        if BOTS in Lf or TOPS in Rf or any(x in Rf and x[0] in ('pre', 'call', 'box') for x in Lf): return C.node(C.AX, 0)
        for jj, b in enumerate(Rf):
            if b[0] == 'box' and alpha.get(b[1]) is True:
                at = b[1]
                if (role == 'W' and at[0] == 'O') or at[0] == 'C':
                    acc.append(('H', at)); return C.node(C.HYP, jj)
                acc.append(('R', at)); return C.node(C.RUN, jj)
        for jj, b in enumerate(Lf):
            if b[0] == 'box' and alpha.get(b[1]) is False:
                acc.append(('N', b[1])); return C.node(C.RUNNEG, jj)
        for jj, x in enumerate(Rf):
            if x[0] not in ('pre', 'call'): continue
            s = evstar(x)
            if s is not None:
                p = tac(Lf, C.fadd(s, C.fdel(x, Rf)), acc)
                return None if p is None else C.node(C.EVS, jj, p)
            path = x[1]
            nd = node_at(path)
            B = ('box', nd[0])
            if nd[0] not in alpha: return None
            rT, rF = ('pre', path + (True,)), ('pre', path + (False,))
            Rx = C.fdel(x, Rf)
            p1 = tac(C.fadd(B, Lf), C.fadd(rT, Rx), acc)
            if p1 is None: return None
            p2 = tac(Lf, C.fadd(B, C.fadd(rF, Rx)), acc)
            if p2 is None: return None
            return C.node(C.CHKR, jj, p1, p2)
        return None
    acc = []
    s = tac((), (('pre', ()),), acc)
    return s, (None if s is None else acc)


def assignments(t):
    ats = dt_atoms(t)
    for bits in itertools.product([True, False], repeat=len(ats)):
        yield dict(zip(ats, bits))


def produce_lists(t, role, producer=None, prog0=None, slot=None, V=None, K=None):
    """The list (data) and access programs of a run tree.  producer None: symbolic (sym_produce); otherwise the
    host PathProducer on the compiled program prog0.  Returns (list data, {A: [(script, access program), ...]})."""
    fam = WORKER_Q if role == 'W' else BOSS_Q
    out = {}
    entries = []
    for A in fam:
        found = []
        for k, alpha in enumerate(assignments(t)):
            if producer is None:
                s, acc = sym_produce(t, role, A, alpha)
            else:
                s, acc = producer.produce(prog0, role, slot, A, alpha, V, K)
            if s is None: continue
            if any(s == f[0] for f in found): continue
            nh = sum(1 for a in acc if a[0] == 'H')
            found.append((s, acc, nh, k))
        found.sort(key=lambda r: (r[2], r[3]))
        out[A] = [(s, acc) for s, acc, _, _ in found]
        entries += [(cons(A), s) for s, _, _, _ in found]
    return cons(entries), out


def dt_template(t):
    """A canonical template spelling of a run tree (nested ifs)."""
    if not isinstance(t, tuple): return ('L', t)
    return ('if', ('A', t[0]), dt_template(t[1]), dt_template(t[2]))


def compile_program(x, role, slot, V, K, lst, **kw):
    """Compile a template x with the list lst."""
    return carrier3(body_term(x, role, slot, V, K, **kw), lst)


# ----------------------------------------------------------------------------------------------------------------
# 4. The abstract evaluator: the host replay's semantics (ExactHost memo, regress, closure) over recorded access
#    programs.  Validated against HostCheck3 on whole programs (tests; notes §1.x).
# ----------------------------------------------------------------------------------------------------------------
class AbsAbort(Exception):
    pass


BETA_IDX = {A_GE14: 0, A_EQ12: 1, A_LE14: 2}
WIDX = {A_WORK: 0, A_STRIKE: 1}


def beta_of_code(code):
    """The boss view of a certifiable boss with action code: ('T'|'F') per question set (>=1/4, =1/2, <=1/4)."""
    return tuple('T' if code in A else 'F' for A in BOSS_Q)


class AbsEval:
    """Encounters: ('E', beta, x, y): worker run trees x (slot 1) and y (slot 2) beside a boss whose three wage boxes
    have the clean values beta; ('B', bk, code): boss run tree bk whose probe boxes have the values code (a dict
    atom -> 'T'|'F'|'TO').  Boxes: (enc, j, A).  `acc[tk][A]` gives the access programs of run tree tk."""

    def __init__(self, wacc, bacc=None):
        self.wacc, self.bacc = wacc, bacc
        self.clear()

    def clear(self):
        self.memo, self.deps, self.stack, self.dstack = {}, {}, [], []

    def seeded(self, key):
        enc, j, A = key
        if enc[0] == 'E' and j == 0: return enc[1][BETA_IDX[A]]
        if enc[0] == 'P': return enc[1][BOSS_ATOMS.index(A)]
        return None

    def check(self, key):
        s = self.seeded(key)
        if s is not None:
            if self.stack and s == 'TO': raise AbsAbort()
            return s
        if key in self.memo:
            res = self.memo[key]
            if self.stack:
                if res == 'TO': raise AbsAbort()
                d = self.deps[key]
                if d and not d.isdisjoint(self.stack): raise AbsAbort()
                self.dstack[-1] |= d; self.dstack[-1].add(key)
            return res
        if key in self.stack: raise AbsAbort()
        self.stack.append(key); self.dstack.append(set())
        try:
            res = self._ccore(key)
        except AbsAbort:
            self.stack.pop(); self.dstack.pop()
            if self.stack: raise
            self.memo[key] = 'TO'; self.deps[key] = set()
            return 'TO'
        self.stack.pop(); d = self.dstack.pop()
        self.memo[key] = res; self.deps[key] = d
        if self.dstack:
            self.dstack[-1] |= d; self.dstack[-1].add(key)
        return res

    def _ccore(self, key):
        r = self._vone(key)
        if r is None: return 'F'
        done = [key]
        todo = list(r)
        while todo:
            y = todo.pop(0)
            if y in done: continue
            if len(done) >= M_CAP: return 'F'
            ry = self._vone(y)
            if ry is None: return 'F'
            todo = list(ry) + todo
            done.append(y)
        return 'T'

    def boxmap(self, key, atom):
        enc, j, A = key
        if enc[0] == 'E':
            if atom[0] == 'B': return (enc, 0, atom[1])
            return (enc, 2 if j == 1 else 1, atom[1])
        return (('P', enc[2]), 0, atom)            # a probe box (another encounter), seeded by the code

    def _vone(self, key):
        enc, j, A = key
        if enc[0] == 'E':
            tk = enc[2] if j == 1 else enc[3]
            progs = self.wacc[tk].get(A, [])
        else:
            progs = self.bacc[enc[1]].get(A, [])
        for _, acc in progs:
            used = []
            ok = True
            for kind, atom in acc:
                box = self.boxmap(key, atom)
                if kind == 'H':
                    used.append(box)
                    continue
                if box == key:
                    ok = False; break
                res = self.check(box)
                if (res == 'T') != (kind == 'R'):
                    ok = False; break
            if ok: return used
        return None

    # ---- encounters
    def worker_pair(self, beta, x, y, wdt):
        """(a1, a2, c1W, c1S, c2W, c2S): actions ('C'|'D') of the slot-1 tree x and slot-2 tree y beside a boss with
        view beta, and the clean values of their certification boxes."""
        enc = ('E', beta, x, y)
        c = {}
        for j in (1, 2):
            for A in WORKER_Q:
                c[(j, A)] = self.check((enc, j, A))

        def val1(at):
            if at[0] == 'B': return beta[BETA_IDX[at[1]]] == 'T'
            return c[(2, at[1])] == 'T'

        def val2(at):
            if at[0] == 'B': return beta[BETA_IDX[at[1]]] == 'T'
            return c[(1, at[1])] == 'T'
        a1 = LEAFVAL[dt_eval(wdt[x], val1)]
        a2 = LEAFVAL[dt_eval(wdt[y], val2)]
        return (a1, a2, c[(1, A_WORK)], c[(1, A_STRIKE)], c[(2, A_WORK)], c[(2, A_STRIKE)])

    def boss_view(self, bk, code, bdt):
        """(action, beta) of boss tree bk when its probe atoms have the values code (tuple over BOSS_ATOMS)."""
        enc = ('B', bk, code)
        beta = tuple(self.check((enc, 0, A)) for A in BOSS_Q)
        act = dt_eval(bdt[bk], lambda at: code[BOSS_ATOMS.index(at)] == 'T')
        return act, beta


# ----------------------------------------------------------------------------------------------------------------
# 5. The catalogue: spellings, run trees, lists, masses, expanded node counts
# ----------------------------------------------------------------------------------------------------------------
def term_nodes(t, expand_wrapper=True):
    """Node count of an L_T term (one per constructor); with expand_wrapper, an application of lib CHK3 counts as the
    wrapper's inlined body `(lam arg. if eq(capk(fst arg, lib CC3, arg), T) then T else F) ARG` (12 + ARG)."""
    tag = t[0]
    if tag in ('v', 'nat', 'con', 'lib'): return 1
    if tag == 'quote': return 1 + term_nodes(t[1], expand_wrapper)
    if expand_wrapper and tag == 'app' and t[1][0] == 'lib' and t[1][1] in WRAPS3:
        return 12 + term_nodes(t[2], expand_wrapper)
    if tag == 'sim': return 1 + term_nodes(t[2], expand_wrapper)
    if tag == 'op': return 1 + term_nodes(t[2], expand_wrapper) + term_nodes(t[3], expand_wrapper)
    return 1 + sum(term_nodes(c, expand_wrapper) for c in t[1:])


ATOM_EXPANDED = {}


def expanded_nodes(x, role, V, K):
    """Expanded-syntax node count of a template (notes §1.3.5), from the template structure: atoms at their
    measured expanded sizes, not 3, and/or 2, if 1, leaves 1.  Equal to term_nodes of the compiled body
    (checked in the tests)."""
    t = x[0]
    if t == 'L': return 1
    if t == 'A':
        k = (x[1], role)
        if k not in ATOM_EXPANDED:
            ATOM_EXPANDED[k] = term_nodes(atom_term(x[1], role, 1, V, K))
        return ATOM_EXPANDED[k]
    if t == 'not': return 3 + expanded_nodes(x[1], role, V, K)
    if t in ('and', 'or'): return 2 + expanded_nodes(x[1], role, V, K) + expanded_nodes(x[2], role, V, K)
    return 1 + sum(expanded_nodes(c, role, V, K) for c in x[1:])


class Catalogue:
    """Both roles' template catalogues at cutoff nmax: spellings, run trees (tau), lists and access programs (symbolic
    path tactic), spelling masses under L and the expanded syntax."""

    def __init__(self, nmax=7, K=K_MAIN, verbose=False):
        self.nmax, self.K, self.V = nmax, K, K // 4
        self.roles = {}
        for role, atoms, leaves in (('W', WORKER_ATOMS, ['W', 'S']), ('B', BOSS_ATOMS, list(range(9)))):
            G = enumerate_templates(nmax, atoms, leaves)
            sp = [x for n in range(1, nmax + 1) for x in G[n]]
            nd = np.array([nodes(x) for x in sp])
            dts = [dt(x) for x in sp]
            tau_of, members = {}, []
            tau = np.zeros(len(sp), np.int64)
            for k, d in enumerate(dts):
                t = tau_of.get(d)
                if t is None:
                    t = len(members); tau_of[d] = t; members.append([])
                tau[k] = t; members[t].append(k)
            tdt = [dts[m[0]] for m in members]
            info = dict(spellings=sp, nodes=nd, tau=tau, members=members, dt=tdt, tau_of=tau_of,
                        counts={n: len(G[n]) for n in G})
            self.roles[role] = info
            if verbose:
                print('%s: %d spellings, %d run trees' % (role, len(sp), len(members)), flush=True)
        # access programs per run tree (symbolic path tactic)
        for role in ('W', 'B'):
            r = self.roles[role]
            r['acc'] = []
            r['lists'] = []
            for d in r['dt']:
                lst, acc = produce_lists(d, role)
                r['acc'].append(acc); r['lists'].append(lst)
        w = self.roles['W']
        w['tag'] = np.array([tagged(d) for d in w['dt']])

    def spelling_mass(self, role, prior='L'):
        r = self.roles[role]
        if prior == 'L':
            w = 2.0 ** (-r['nodes'].astype(float))
        elif prior == 'X':
            if 'xnodes' not in r:
                r['xnodes'] = np.array([expanded_nodes(x, role, self.V, self.K) for x in r['spellings']])
            lw = -r['xnodes'].astype(float) * np.log(2.0)
            w = np.exp(lw - lw.max())
        else:
            raise ValueError(prior)
        return w / w.sum()

    def tau_mass(self, role, prior='L'):
        r = self.roles[role]
        return np.bincount(r['tau'], weights=self.spelling_mass(role, prior), minlength=len(r['members']))

    def tau_repr_nodes(self, role):
        r = self.roles[role]
        return np.array([min(r['nodes'][m]) for m in r['members']])

    def program(self, role, tk, slot=1, V=None, K=None, spelling=None, **kw):
        """Compile a run tree's representative spelling (or a given spelling index) with its list."""
        r = self.roles[role]
        V = self.V if V is None else V; K = self.K if K is None else K
        x = r['spellings'][r['members'][tk][0] if spelling is None else spelling]
        if spelling is not None: assert r['tau'][spelling] == tk
        return compile_program(x, role, slot, V, K, r['lists'][tk], **kw)


# ----------------------------------------------------------------------------------------------------------------
# 6. Whole runs (the term evaluator), composition helpers
# ----------------------------------------------------------------------------------------------------------------
def run_value(p, x, y, K):
    v, n = L.run_big(L.evaluate, initial3(p, x, y), K)
    return v, n


def play3(b, w1, w2, K):
    """The actual plays: (boss value, worker 1 value, worker 2 value) after defaults, and the step counts."""
    vb, nb = run_value(b, w1, w2, K)
    v1, n1 = run_value(w1, b, w2, K)
    v2, n2 = run_value(w2, b, w1, K)
    db = vb if isinstance(vb, int) and 0 <= vb < 9 else 1
    d1 = v1 if v1 in ('C', 'D') else 'C'
    d2 = v2 if v2 in ('C', 'D') else 'C'
    return (db, d1, d2), (nb, n1, n2), (vb, v1, v2)


def term_check(enc, j, A, V, K, mode=MODE3):
    """Clean run of capk(V, CC3, arg) by the checker term: (value 'T'|'F'|'TO', inner steps)."""
    n = CORE3[mode]
    arg = mk_arg3(V, enc, j, A, K)
    key = (n, V, L.tval_to_rt(arg))
    rec = L.CACHE.get(key)
    if rec is None:
        v, steps = L.run_big(L.evaluate, ('capk', N(V), ('lib', n), arg))
        rec = L.CACHE.get(key)
        if rec is None: rec = (v, steps - 1)
    return rec


# ----------------------------------------------------------------------------------------------------------------
# 7. Tables (notes §1.3.2): worker-pair tables E_beta, realized probe codes, boss maps, lumping
# ----------------------------------------------------------------------------------------------------------------
VCODE = {'T': 1, 'F': 0, 'TO': 2}
VNAME = {1: 'T', 0: 'F', 2: 'TO'}
ACODE = {'C': 0, 'D': 1}                 # 0 work, 1 strike (union.py's a)
BETA_CERT = [beta_of_code(c) for c in (1, 4, 7)]      # the certifiable views at s = 0, 1/4, 1/2
# probe atom -> (beta index of its quoted constant, column of the pair row)
PROBE_COL = {}
for _at in BOSS_ATOMS:
    _, _j, _s, _A = _at
    PROBE_COL[_at] = (_s, (2 if _j == 1 else 4) + WIDX[_A])


def pair_rows(cat, beta, xs, ys):
    """int8 array (len(xs), len(ys), 6): (a1, a2, c1W, c1S, c2W, c2S) for slot-1 trees xs and slot-2 trees ys."""
    w = cat.roles['W']
    ae = AbsEval(w['acc'])
    out = np.zeros((len(xs), len(ys), 6), np.int8)
    for ii, x in enumerate(xs):
        ae.clear()
        for jj, y in enumerate(ys):
            a1, a2, c1w, c1s, c2w, c2s = ae.worker_pair(beta, x, y, w['dt'])
            out[ii, jj] = (ACODE[a1], ACODE[a2], VCODE[c1w], VCODE[c1s], VCODE[c2w], VCODE[c2s])
    return out


def probe_codes(E0, E14):
    """Ternary probe codes (n1, n2, 8) over BOSS_ATOMS from the pair tables at the s = 0 and s = 1/4 views."""
    Es = (E0, E14)
    cols = []
    for at in BOSS_ATOMS:
        s, col = PROBE_COL[at]
        cols.append(Es[s][:, :, col])
    return np.stack(cols, axis=-1).astype(np.int8)


def boss_view_table(cat, codes, bks=None):
    """For each boss run tree: (action, beta) on every realized code (codes: array (ncodes, 8) of 0/1/2).
    Returns act (nb, ncodes) int8, beta (nb, ncodes, 3) int8."""
    b = cat.roles['B']
    bks = range(len(b['dt'])) if bks is None else bks
    ae = AbsEval(None, b['acc'])
    nc = len(codes)
    act = np.zeros((len(bks), nc), np.int8)
    bet = np.zeros((len(bks), nc, 3), np.int8)
    aidx = {at: i for i, at in enumerate(BOSS_ATOMS)}
    for ii, bk in enumerate(bks):
        ats = dt_atoms(b['dt'][bk])
        ix = [aidx[a] for a in ats]
        sub = {}
        ae.clear()
        for c in range(nc):
            key = tuple(codes[c, ix])
            r = sub.get(key)
            if r is None:
                full = ['F'] * 8
                for k, i in enumerate(ix): full[i] = VNAME[int(key[k])]
                a, be = ae.boss_view(bk, tuple(full), b['dt'])
                r = (a, tuple(VCODE[v] for v in be))
                sub[key] = r
            act[ii, c] = r[0]; bet[ii, c] = r[1]
    return act, bet


def group_rows(keys):
    """Exact grouping of byte keys: returns (class index per item, representative item per class)."""
    idx = {}
    cls = np.zeros(len(keys), np.int64)
    reps = []
    for i, k in enumerate(keys):
        c = idx.get(k)
        if c is None:
            c = len(reps); idx[k] = c; reps.append(i)
        cls[i] = c
    return cls, np.array(reps, np.int64)


# ---- named templates (notes §1.3.3)
def _A(at): return ('A', at)
def _if(b, x, y): return ('if', b, x, y)
def _L(v): return ('L', v)


P1_14S = _A(('P', 1, 1, A_STRIKE)); P1_0S = _A(('P', 1, 0, A_STRIKE)); P2_14S = _A(('P', 2, 1, A_STRIKE))
P2_0S = _A(('P', 2, 0, A_STRIKE)); P1_0W = _A(('P', 1, 0, A_WORK))
NAMED_B = {
    'D0': _if(P1_0S, _L(7), _L(1)),
    'D0q': _if(P1_0S, _L(4), _L(1)),
    'D14': _if(P1_14S, _L(7), _L(1)),
    'D*': _if(P1_14S, _L(7), _if(P1_0S, _L(4), _L(1))),
    'D14_2': _if(('and', P1_14S, P2_14S), _L(7), _L(1)),
    'WF': _if(P1_0W, _L(7), _L(1)),
}
for _c in range(9): NAMED_B[bname(_c)] = _L(_c)
NAMED_B_OUT = {'D*_2': _if(('and', P1_14S, P2_14S), _L(7), _if(('and', P1_0S, P2_0S), _L(4), _L(1)))}   # 11 nodes
B12, B14, BL14 = _A(('B', A_EQ12)), _A(('B', A_GE14)), _A(('B', A_LE14))
OS, OW = _A(('O', A_STRIKE)), _A(('O', A_WORK))
NAMED_W = {
    'scab': _L('W'), 'striker': _L('S'),
    'T1': _if(B12, _L('W'), _L('S')), 'T0': _if(B14, _L('W'), _L('S')), 'R': _if(BL14, _L('S'), _L('W')),
    'Q': _if(OS, _L('S'), _L('W')), 'U': _if(B12, _L('W'), _if(OS, _L('S'), _L('W'))),
    'Qw': _if(OW, _L('W'), _L('S')),
}


def build_tables(cat, extra_boss_dts=(), verbose=True):
    """The exact class tables of notes §1.3.2.  Returns a dict with: worker classes per slot (cls1, cls2 over run
    trees), boss classes over run trees (+ extra out-of-catalogue trees appended), realized codes, betas, and the
    class-level arrays PV (n1c, n2c) code index, EA (nbeta, n1c, n2c) 2*a1 + a2, CERT (nbeta, n1c, n2c, 4),
    FBA (nbc, ncode) action, FBB (nbc, ncode) beta index, tag1, tag2."""
    import time
    t0 = time.time()
    w = cat.roles['W']; b = cat.roles['B']
    nW = len(w['members'])
    xs = list(range(nW))
    betas = list(BETA_CERT)
    E = {be: pair_rows(cat, be, xs, xs) for be in betas}
    if verbose: print('pair tables (3 views): %.1fs' % (time.time() - t0), flush=True)
    CODE = probe_codes(E[BETA_CERT[0]], E[BETA_CERT[1]])           # (nW, nW, 8)
    flat = CODE.reshape(-1, 8)
    ucodes, code_of = np.unique(flat, axis=0, return_inverse=True)
    code_of = code_of.reshape(nW, nW)
    if verbose: print('realized probe codes: %d' % len(ucodes), flush=True)
    # bosses: catalogue trees plus extras
    bdt_all = list(b['dt']) + list(extra_boss_dts)
    bacc_all = list(b['acc']) + [produce_lists(d, 'B')[1] for d in extra_boss_dts]
    saved = (b['dt'], b['acc'])
    b['dt'], b['acc'] = bdt_all, bacc_all
    try:
        act, bet = boss_view_table(cat, ucodes)
    finally:
        b['dt'], b['acc'] = saved
    if verbose: print('boss views (%d trees x %d codes): %.1fs' % (len(bdt_all), len(ucodes), time.time() - t0), flush=True)
    bet_tuples = [tuple(VNAME[int(v)] for v in r) for r in np.unique(bet.reshape(-1, 3), axis=0)]
    for be in bet_tuples:
        if be not in E:
            betas.append(be)
            E[be] = pair_rows(cat, be, xs, xs)
    beta_id = {be: i for i, be in enumerate(betas)}
    if verbose: print('views occurring: %d (%s); %.1fs' % (len(betas), betas, time.time() - t0), flush=True)
    Earr = np.stack([E[be] for be in betas])                      # (nbeta, nW, nW, 6)
    # worker lumping: slot 1 by rows, slot 2 by columns, tags kept apart
    tag = w['tag']
    k1 = [bytes([int(tag[x])]) + Earr[:, x, :, :].tobytes() for x in xs]
    k2 = [bytes([int(tag[y])]) + np.ascontiguousarray(Earr[:, :, y, :]).tobytes() for y in xs]
    cls1, rep1 = group_rows(k1)
    cls2, rep2 = group_rows(k2)
    # boss lumping by (action, view) on every realized code
    bid = np.zeros(bet.shape[:2], np.int64)
    for be, i in beta_id.items():
        m = np.all(bet == np.array([VCODE[v] for v in be], np.int8), axis=2)
        bid[m] = i
    kb = [act[i].tobytes() + bid[i].astype(np.int8).tobytes() for i in range(len(bdt_all))]
    clsb, repb = group_rows(kb)
    # class-level arrays
    PV = code_of[np.ix_(rep1, rep2)]
    EA = (2 * Earr[:, rep1][:, :, rep2, 0] + Earr[:, rep1][:, :, rep2, 1]).astype(np.int8)
    CERT = Earr[:, rep1][:, :, rep2, 2:6].astype(np.int8)
    FBA = act[repb].astype(np.int8)
    FBB = bid[repb].astype(np.int8)
    out = dict(betas=betas, beta_id=beta_id, ucodes=ucodes, code_of=code_of, E=Earr, act=act, bid=bid,
               cls1=cls1, rep1=rep1, cls2=cls2, rep2=rep2, clsb=clsb, repb=repb,
               PV=PV, EA=EA, CERT=CERT, FBA=FBA, FBB=FBB,
               tag1=tag[rep1].astype(np.int64), tag2=tag[rep2].astype(np.int64),
               n_extra=len(extra_boss_dts), nb_cat=len(b['dt']))
    if verbose:
        print('classes: W1 %d, W2 %d, B %d (incl. %d extra trees); %.1fs' % (len(rep1), len(rep2), len(repb),
              len(extra_boss_dts), time.time() - t0), flush=True)
    return out


def joint_code(T, b, x, y):
    """Joint action code 4 * boss action + 2 * a1 + a2 of boss class b, slot-1 class x, slot-2 class y."""
    c = T['PV'][x, y]
    return 4 * int(T['FBA'][b, c]) + int(T['EA'][T['FBB'][b, c], x, y])


# ----------------------------------------------------------------------------------------------------------------
# 8. The seed-lottery kernel (src/sog_lottery.py's kern with the factorized table J of Lemma F_3 computed on the fly;
#    one worker class space for both slots, local boss ids per run)
# ----------------------------------------------------------------------------------------------------------------
from abm import njit

NSUM = 7          # union.SUMM: fair, intermediate, zero wage, strike, scab split, repression:strike, repression:source


@njit(cache=True)
def _jc(JM, FBA, FBB, PV, EA, b, x, y):
    c = PV[x, y]
    return JM[4 * FBA[b, c] + EA[FBB[b, c], x, y]]


@njit(cache=True)
def _summ(j, t1, t2):
    b = j // 4; a1 = (j // 2) % 2; a2 = j % 2
    h = b % 3
    if h == 0 and (a1 == 1 or a2 == 1):
        return 5
    if h == 2 and (t1 == 1 or t2 == 1):
        return 6
    if a1 == 1 and a2 == 1:
        return 3
    if a1 == 1 or a2 == 1:
        return 4
    return 2 - (b // 3)


@njit(cache=True)
def _payk(JM, FBA, FBB, PV, EA, tag, PAY, s, k, p, q):
    if s == 0:
        b = k; x = p; y = q
    elif s == 1:
        b = p; x = k; y = q
    else:
        b = p; x = q; y = k
    return PAY[_jc(JM, FBA, FBB, PV, EA, b, x, y), tag[x], tag[y], s]


@njit(cache=True)
def _others(s):
    if s == 0:
        return 1, 2
    if s == 1:
        return 0, 2
    return 0, 1


@njit(cache=True)
def _fit_full(JM, FBA, FBB, PV, EA, tag, PAY, counts, pres, npres, i, s, k):
    o1, o2 = _others(s)
    v = 0.0
    for t1 in range(npres[i, o1]):
        p = pres[i, o1, t1]
        for t2 in range(npres[i, o2]):
            q = pres[i, o2, t2]
            v += counts[i, o1, p] * counts[i, o2, q] * _payk(JM, FBA, FBB, PV, EA, tag, PAY, s, k, p, q)
    return v


@njit(cache=True)
def _parent(F, counts, pres, npres, i, s, N2, w):
    m = -1e300
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        f = F[i, s, k] / N2
        if f > m: m = f
    tot = 0.0
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        tot += counts[i, s, k] * np.exp(w * (F[i, s, k] / N2 - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[i, s]):
        k = pres[i, s, t]
        acc += counts[i, s, k] * np.exp(w * (F[i, s, k] / N2 - m))
        if u <= acc:
            return k
    return pres[i, s, npres[i, s] - 1]


@njit(cache=True)
def _island_stats(JM, FBA, FBB, PV, EA, tag, PAY, MB, MW, counts, pres, npres, i, N, out):
    """out[0:7] summary shares, out[7:10] mean payoffs (B, W1, W2), out[10:10+nb] boss-mask shares,
    then worker-mask shares (slot 1, slot 2 interleaved per mask)."""
    for z in range(out.shape[0]):
        out[z] = 0.0
    N3 = float(N) * N * N
    for ta in range(npres[i, 0]):
        b = pres[i, 0, ta]
        for tb in range(npres[i, 1]):
            x = pres[i, 1, tb]
            for tc in range(npres[i, 2]):
                y = pres[i, 2, tc]
                p = counts[i, 0, b] * counts[i, 1, x] * counts[i, 2, y] / N3
                j = _jc(JM, FBA, FBB, PV, EA, b, x, y)
                out[_summ(j, tag[x], tag[y])] += p
                for s in range(3):
                    out[7 + s] += p * PAY[j, tag[x], tag[y], s]
    nb = MB.shape[0]
    for ta in range(npres[i, 0]):
        b = pres[i, 0, ta]
        for z in range(nb):
            if MB[z, b]:
                out[10 + z] += counts[i, 0, b] / N
    for s in (1, 2):
        for ta in range(npres[i, s]):
            x = pres[i, s, ta]
            for z in range(MW.shape[0]):
                if MW[z, x]:
                    out[10 + nb + 2 * z + (s - 1)] += counts[i, s, x] / N


@njit(cache=True)
def _closed(JM, FBA, FBB, PV, EA, tag, KEYT, cls0, n0, cls1, n1, cls2, n2):
    for tb in range(n1):
        x = cls1[tb]
        for tc in range(n2):
            y = cls2[tc]
            k0 = KEYT[_jc(JM, FBA, FBB, PV, EA, cls0[0], x, y), tag[x], tag[y]]
            for ta in range(1, n0):
                if KEYT[_jc(JM, FBA, FBB, PV, EA, cls0[ta], x, y), tag[x], tag[y]] != k0:
                    return False
    for ta in range(n0):
        b = cls0[ta]
        for tc in range(n2):
            y = cls2[tc]
            k0 = KEYT[_jc(JM, FBA, FBB, PV, EA, b, cls1[0], y), tag[cls1[0]], tag[y]]
            for tb in range(1, n1):
                x = cls1[tb]
                if KEYT[_jc(JM, FBA, FBB, PV, EA, b, x, y), tag[x], tag[y]] != k0:
                    return False
        for tb in range(n1):
            x = cls1[tb]
            k0 = KEYT[_jc(JM, FBA, FBB, PV, EA, b, x, cls2[0]), tag[x], tag[cls2[0]]]
            for tc in range(1, n2):
                y = cls2[tc]
                if KEYT[_jc(JM, FBA, FBB, PV, EA, b, x, y), tag[x], tag[y]] != k0:
                    return False
    return True


@njit(cache=True)
def _setact(u, a, act, apos, nact):
    p = apos[u]
    if a and p >= nact:
        j = act[nact]; act[nact] = u; act[p] = j; apos[u] = nact; apos[j] = p; nact += 1
    elif (not a) and p < nact:
        nact -= 1; j = act[nact]; act[nact] = u; act[p] = j; apos[u] = nact; apos[j] = p
    return nact


@njit(cache=True)
def kern3(JM, FBA, FBB, PV, EA, tag, PAY, KEYT, MB, MW, init, N, w, m, seed, checks, nstat):
    """init[i, s, k]: initial counts (bosses by local id, workers by class).  Returns status (1 globally closed,
    4 horizon), stop generation, final counts, per-check per-island statistics (nchk, I, nstat), per-check modal
    class per slot (nchk, I, 3) and its count, the number of migrant births, and the number of checks done."""
    np.random.seed(seed)
    I = init.shape[0]; K = init.shape[2]
    counts = init.copy()
    pres = np.zeros((I, 3, K), np.int64); npres = np.zeros((I, 3), np.int64); pos = -np.ones((I, 3, K), np.int64)
    glob = np.zeros((3, K), np.int64)
    F = np.zeros((I, 3, K))
    for i in range(I):
        for s in range(3):
            for k in range(K):
                if counts[i, s, k] > 0:
                    pres[i, s, npres[i, s]] = k; pos[i, s, k] = npres[i, s]; npres[i, s] += 1
                    glob[s, k] += counts[i, s, k]
    for i in range(I):
        for s in range(3):
            for t in range(npres[i, s]):
                k = pres[i, s, t]
                F[i, s, k] = _fit_full(JM, FBA, FBB, PV, EA, tag, PAY, counts, pres, npres, i, s, k)
    NU = 3 * I
    act = np.arange(NU); apos = np.arange(NU); nact = 0
    for u in range(NU):
        if npres[u // 3, u % 3] > 1:
            nact = _setact(u, True, act, apos, nact)
    nchk = len(checks)
    stats = np.zeros((nchk + 1, I, nstat))
    modal = np.zeros((nchk + 1, I, 3), np.int64); modalc = np.zeros((nchk + 1, I, 3), np.int64)
    tmp = np.zeros(nstat)
    N2 = float(N) * N
    UN = NU * N
    total = checks[nchk - 1] * UN
    mm = m if I > 1 else 0.0
    b = 0
    ci = 0
    nextchk = checks[0] * UN
    status = 4; stop_gen = checks[nchk - 1]
    nmig = 0
    for i in range(I):
        _island_stats(JM, FBA, FBB, PV, EA, tag, PAY, MB, MW, counts, pres, npres, i, N, tmp)
        for z in range(nstat):
            stats[0, i, z] = tmp[z]
        for s in range(3):
            best = -1; bc = -1
            for t in range(npres[i, s]):
                k = pres[i, s, t]
                if counts[i, s, k] > bc:
                    bc = counts[i, s, k]; best = k
            modal[0, i, s] = best; modalc[0, i, s] = bc
    cls0 = np.zeros(K, np.int64); cls1 = np.zeros(K, np.int64); cls2 = np.zeros(K, np.int64)
    while True:
        pa = (nact + (NU - nact) * mm) / NU
        if pa <= 0.0:
            G = total + 1
        elif pa >= 1.0:
            G = 0
        else:
            uu = np.random.random()
            G = int(np.log(1.0 - uu) / np.log(1.0 - pa))
        if b + G >= nextchk:
            b = nextchk
            ci += 1
            for i in range(I):
                _island_stats(JM, FBA, FBB, PV, EA, tag, PAY, MB, MW, counts, pres, npres, i, N, tmp)
                for z in range(nstat):
                    stats[ci, i, z] = tmp[z]
                for s in range(3):
                    best = -1; bc = -1
                    for t in range(npres[i, s]):
                        k = pres[i, s, t]
                        if counts[i, s, k] > bc:
                            bc = counts[i, s, k]; best = k
                    modal[ci, i, s] = best; modalc[ci, i, s] = bc
            g = checks[ci - 1]
            if mm > 0.0:
                n0 = 0; n1 = 0; n2 = 0
                for k in range(K):
                    if glob[0, k] > 0:
                        cls0[n0] = k; n0 += 1
                    if glob[1, k] > 0:
                        cls1[n1] = k; n1 += 1
                    if glob[2, k] > 0:
                        cls2[n2] = k; n2 += 1
                if _closed(JM, FBA, FBB, PV, EA, tag, KEYT, cls0, n0, cls1, n1, cls2, n2):
                    status = 1; stop_gen = g; break
            if ci >= nchk:
                break
            nextchk = checks[ci] * UN
            continue
        b = b + G + 1
        if np.random.random() * pa * NU < nact:
            u = act[np.random.randint(nact)]
            mig = mm > 0.0 and np.random.random() < mm
        else:
            u = act[nact + np.random.randint(NU - nact)]
            mig = True
        i = u // 3; s = u % 3
        src = i
        if mig:
            src = np.random.randint(I - 1)
            if src >= i: src += 1
            nmig += 1
        child = _parent(F, counts, pres, npres, src, s, N2, w)
        r = np.random.randint(N); acc = 0; victim = pres[i, s, 0]
        for t in range(npres[i, s]):
            k = pres[i, s, t]; acc += counts[i, s, k]
            if r < acc:
                victim = k; break
        if victim == child:
            continue
        counts[i, s, victim] -= 1; glob[s, victim] -= 1
        if counts[i, s, victim] == 0:
            p = pos[i, s, victim]; last = pres[i, s, npres[i, s] - 1]
            pres[i, s, p] = last; pos[i, s, last] = p; pos[i, s, victim] = -1; npres[i, s] -= 1
        new = counts[i, s, child] == 0
        if new:
            pres[i, s, npres[i, s]] = child; pos[i, s, child] = npres[i, s]; npres[i, s] += 1
        counts[i, s, child] += 1; glob[s, child] += 1
        o1, o2 = _others(s)
        for sa in (o1, o2):
            sb = o1 + o2 - sa
            for ta in range(npres[i, sa]):
                k = pres[i, sa, ta]
                v = 0.0
                for tb in range(npres[i, sb]):
                    q = pres[i, sb, tb]
                    if s < sb:
                        v += counts[i, sb, q] * (_payk(JM, FBA, FBB, PV, EA, tag, PAY, sa, k, child, q) - _payk(JM, FBA, FBB, PV, EA, tag, PAY, sa, k, victim, q))
                    else:
                        v += counts[i, sb, q] * (_payk(JM, FBA, FBB, PV, EA, tag, PAY, sa, k, q, child) - _payk(JM, FBA, FBB, PV, EA, tag, PAY, sa, k, q, victim))
                F[i, sa, k] += v
        if new:
            F[i, s, child] = _fit_full(JM, FBA, FBB, PV, EA, tag, PAY, counts, pres, npres, i, s, child)
        nact = _setact(u, npres[i, s] > 1, act, apos, nact)
    return status, stop_gen, counts, stats[:ci + 1], modal[:ci + 1], modalc[:ci + 1], nmig, ci
