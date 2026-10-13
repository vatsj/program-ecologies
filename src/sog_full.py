"""The social organization game, fully realizable (specs/2026-10-13-sog-fully-realizable.md;
notes/sog-fully-realizable.md; predictions/2026-10-13-sog-fully-realizable.md).

Built on src/lt_code.py, src/lt_cert.py, src/carrier_populations.py and src/sog_realizable.py (imported, not
modified).  Importing sog_realizable installs its K_3 library; this module then installs its own build K_3'
(notes §1.1): four-abstraction carriers with the public slot label, `vone4` as a one-argument entry (instrumented for
step counts), the source-identity primitive EQS, and PROD3 / PCORE3 (the tactic as code).  Nothing of
sog_realizable that depends on library indices is used after the rebuild; its index-free helpers are (templates,
run trees).

Parts:
  1. the library K_3' and its installation;
  2. templates (with identity atoms), compilation to four-abstraction carriers, named programs;
  3. the host replay (HostCheck4) and whole runs by the term;
  4. the symbolic layer over run trees: H lists (the path tactic over assignments, identity values included),
     the symbolic script checker (the term's traversal, with the order of nested calls), the symbolic PROD3;
  5. the abstract evaluator with inventories, relation bits, traces and composed costs (notes §1.7).
"""
import os
import sys
import itertools

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import sog_realizable as S          # installs K_3; rebuilt below
import lt_code as L
import lt_cert as C
import carrier_populations as CP

N, P = L.N, L.P
C_, D_, T_, F_, TO_ = L.C_, L.D_, L.T_, L.F_, L.TO_

# ----------------------------------------------------------------------------------------------------------------
# 1. The library K_3'
# ----------------------------------------------------------------------------------------------------------------
M_CAP = S.M_CAP
CERT4_SRC = r"""
; ---------------- K_3': three-quote checks over four-abstraction carriers ----------------
(def CHK3 (arg) (if (eq (capk (fst arg) CC3 arg) T) T F))
(def CHK3N (arg) (if (eq (capk (fst arg) CC3N arg) T) T F))
(def CC3 (arg) (ccore3 0 arg))
(def CC3N (arg) (ccore3 1 arg))
(def iswrap3 (n) (or (eq n ID_CHK3) (eq n ID_CHK3N)))
(def callcheck3 (n ad) (if (eq n ID_CHK3) (capk (fst ad) CC3 ad) (capk (fst ad) CC3N ad)))
(def lapp (a b) (if (eq a 0) b (pair (fst a) (lapp (snd a) b))))
(def amem (v l) (if (eq l 0) F (if (eq (fst l) v) T (amem v (snd l)))))
(def subjq (enc j) (cond ((eq j 0) (fst enc)) ((eq j 1) (fst (snd enc))) (else (snd (snd enc)))))
(def app4 (f x y z s) (mkapp (mkapp (mkapp (mkapp f (pair 10 x)) (pair 10 y)) (pair 10 z)) (pair 4 s)))
(def mkconf4 (enc j)
  (let ((b (fst enc)) (w1 (fst (snd enc))) (w2 (snd (snd enc))))
    (cond ((eq j 0) (app4 b b w1 w2 0))
          ((eq j 1) (app4 w1 w1 b w2 1))
          (else (app4 w2 w2 b w1 2)))))
(def getcerts4 (t)
  (if (eq (fst t) 1)
    (let ((b1 (snd t)))
      (if (eq (fst b1) 1)
        (let ((b2 (snd b1)))
          (if (eq (fst b2) 1)
            (let ((b3 (snd b2)))
              (if (eq (fst b3) 1)
                (let ((b4 (snd b3)))
                  (if (eq (fst b4) 2)
                    (let ((l (snd b4)))
                      (if (eq (fst (fst l)) 1) (full (fst (snd l))) NONE))
                    NONE))
                NONE))
            NONE))
        NONE))
    NONE))

; ---------------- source identity ----------------
(def srcof (q) (fst (snd (snd (snd (snd (snd q)))))))
(def EQS (p) (if (eq (srcof (fst p)) (srcof (snd p))) T F))
(def SHAMS (p) (if (eq (srcof (fst p)) (srcof (snd p))) F F))

; ---------------- the check: root validation, then the uniform-cost closure ----------------
(def ccore3 (x arg)
  (let ((n (if (eq x 0) ID_CHK3 ID_CHK3N)) (r1 (vone4 (pair n arg))))
    (if (eq r1 0) F
      (if (eq x 1) T
        (clos3 n (snd r1) (setnth DONE0 0 arg) 1)))))
(def clos3 (n todo done cnt)
  (if (eq todo 0) T
    (let ((y (fst todo)) (rest (snd todo)))
      (if (scanm y done F)
          (clos3 n rest done cnt)
          (if (eq cnt MCAP) F
              (let ((r (vone4 (pair n y))))
                (if (eq r 0) F
                    (clos3 n (lapp (snd r) rest) (setnth done cnt y) (add cnt 1)))))))))
(def scanm (y d acc) (if (eq d 0) acc (scanm y (snd d) (if (eq (fst d) y) T acc))))
(def vone4 (nx)
  (let ((n (fst nx)) (x (snd nx)) (r (snd x)) (enc (fst r)) (j (fst (snd r))) (A (fst (snd (snd r))))
        (K (snd (snd (snd r)))) (cl (getcerts4 (subjq enc j))))
    (if (eq cl NONE) 0
      (tryents3 (pair n (pair (pair 8 (pair n x)) x)) cl A (mkatom (mkconf4 enc j) K A 0)))))
(def tryents3 (cx cl A psi)
  (if (eq cl 0) 0
    (let ((e (fst cl)))
      (if (eq (fst e) A)
          (let ((v (cchk3 (pair cx (pair (snd e) (pair 0 (pair psi 0)))))))
            (if (eq v 0) (tryents3 cx (snd cl) A psi) v))
          (tryents3 cx (snd cl) A psi)))))

; ---------------- the script checker; returns 0 (invalid) or (1 . used encounter-box arguments) ----------------
(def cchk3 (q)
  (let ((cx (fst q)) (node (fst (snd q))) (L (fst (snd (snd q)))) (R (snd (snd (snd q))))
        (rule (fst node)) (j (fst (snd node))) (ps (snd (snd node))))
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
          (cchk3 (pair cx (pair (fst ps) (pair L (fadd (evfrom3 r f a m) (fdel x R))))))
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
              (v1 (cchk3 (pair cx (pair (fst ps) (pair (fadd B L) (fadd (fst (snd s)) Rx)))))))
          (if (eq v1 0) 0
            (let ((v2 (cchk3 (pair cx (pair (fst (snd ps)) (pair L (fadd B (fadd (snd (snd s)) Rx))))))))
              (if (eq v2 0) 0 (pair 1 (lapp (snd v1) (snd v2)))))))))))

; ---------------- PROD3: the endogenous tactic as code (notes §1.1.5) ----------------
; PROD3 arg = (P . ad), ad = the producer's own box argument (V . (enc . (j . (A . K)))).  ptac returns
; (node-or-NONE . count).  al: the assignment met so far, a list of (box . 1|0).
(def PROD3 (arg) (capk (fst arg) PCORE3 (snd arg)))
(def PCORE3 (ad)
  (let ((r (snd ad)) (enc (fst r)) (j (fst (snd r))) (A (fst (snd (snd r)))) (K (snd (snd (snd r))))
        (cx (pair (pair 8 (pair ID_CHK3 ad)) ad))
        (res (ptac cx 0 0 (pair (mkatom (mkconf4 enc j) K A 0) 0) 0)))
    (fst res)))
(def mknd (r j ps) (pair r (pair j ps)))
(def alook (b al) (if (eq al 0) 2 (if (eq (fst (fst al)) b) (snd (fst al)) (alook b (snd al)))))
(def phypable (cx B)
  (let ((x (snd cx)) (p (snd B)) (ad (snd p)) (sj (fst (snd (snd ad)))))
    (and (eq (fst p) ID_CHK3)
      (and (eq (fst ad) (fst x))
        (and (eq (fst (snd ad)) (fst (snd x)))
          (and (eq (snd (snd (snd (snd ad)))) (snd (snd (snd (snd x)))))
            (and (lt 0 sj) (not (eq sj (fst (snd (snd x))))))))))))
(def ptpos (cx al l j)
  (if (eq l 0) NONE
    (let ((b (fst l)))
      (if (and (eq (fst b) 8) (eq (alook b al) 1))
          (pair (if (phypable cx b) 3 1) j)
          (ptpos cx al (snd l) (add j 1))))))
(def ptneg (al l j)
  (if (eq l 0) NONE
    (let ((b (fst l)))
      (if (and (eq (fst b) 8) (eq (alook b al) 0)) j (ptneg al (snd l) (add j 1))))))
(def ptac (cx al L R c)
  (if (lt 63 c) (pair NONE (add c 1))
    (let ((c1 (add c 1)))
      (if (caxiom L R) (pair (mknd 0 0 0) c1)
        (let ((h (ptpos cx al R 0)))
          (if (not (eq h NONE)) (pair (mknd (fst h) (snd h) 0) c1)
            (let ((g (ptneg al L 0)))
              (if (not (eq g NONE)) (pair (mknd 2 g 0) c1)
                (patom cx al L R R 0 c1)))))))))
(def patom (cx al L R l j c)
  (if (eq l 0) (pair NONE c)
    (let ((x (fst l)))
      (if (not (eq (fst x) 6)) (patom cx al L R (snd l) (add j 1) c)
        (let ((p (snd x)) (conf (fst p)) (f (fst (snd p))) (a (fst (snd (snd p)))) (m (snd (snd (snd p))))
              (r (cstep conf)))
          (if (and (lt 0 f) (eq (fst r) 2))
              (let ((q (ptac cx al L (fadd (evfrom3 r f a m) (fdel x R)) c)))
                (if (eq (fst q) NONE) q (pair (mknd 26 j (pair (fst q) 0)) (snd q))))
              (let ((s (chkstate3 conf f a)))
                (if (eq s 0) (pair NONE c)
                  (pchk cx al L (fdel x R) j s c)))))))))
(def tcheck3 (b) (let ((p (snd b))) (callcheck3 (fst p) (snd p))))
(def pchk (cx al L Rx j s c)
  (let ((B (fst s)) (v (alook B al)))
    (if (eq v 2)
      (if (phypable cx B)
          (let ((q (pbranch cx (pair (pair B 1) al) L Rx j s c)))
            (if (not (eq (fst q) NONE)) q
              (if (eq (tcheck3 B) T) (pair NONE c)
                  (pbranch cx (pair (pair B 0) al) L Rx j s c))))
          (pbranch cx (pair (pair B (if (eq (tcheck3 B) T) 1 0)) al) L Rx j s c))
      (pbranch cx al L Rx j s c))))
(def pbranch (cx al L Rx j s c)
  (let ((B (fst s)) (q1 (ptac cx al (fadd B L) (fadd (fst (snd s)) Rx) c)))
    (if (eq (fst q1) NONE) q1
      (let ((q2 (ptac cx al L (fadd B (fadd (snd (snd s)) Rx)) (snd q1))))
        (if (eq (fst q2) NONE) q2
          (pair (mknd 25 j (pair (fst q1) (pair (fst q2) 0))) (snd q2)))))))
"""

ISWRAP_OLD = S.ISWRAP_OLD
ISWRAP_NEW = S.ISWRAP_NEW
CERT4_CONSTS = dict(S.CERT3_CONSTS)
MODE3, MODE3N = S.MODE3, S.MODE3N
ID4 = {}
PROD3_ID_CODE = 45          # PCORE3's id in lt_code.CORE_LIBS (deterministic: cached clean runs)


def build_library4():
    assert ISWRAP_OLD in C.CERT_SRC
    comp = L.SxCompiler()
    for k, v in L.LIB_CONSTS.items(): comp.consts[k] = v
    for k, v in C.CERT_CONSTS.items(): comp.consts[k] = v
    for k, v in CERT4_CONSTS.items(): comp.consts[k] = v
    comp.load(L.LIBRARY_SRC)
    comp.load(C.CERT_SRC.replace(ISWRAP_OLD, ISWRAP_NEW))
    comp.load(CERT4_SRC)
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
    L.CORE_LIBS[L.LIBIDX['PCORE3']] = PROD3_ID_CODE
    L._compiled.clear()
    L.LIBCODE[:] = [L.compile_term(t[1]) for t in terms]
    L.CACHE.clear()
    C.ID.clear(); C.ID.update({nm: L.LIBIDX[nm] for nm in C.WRAP_NAMES})
    C.WRAPS.clear(); C.WRAPS.update(C.ID.values())
    C.CC_MODE.clear(); C.CC_MODE.update({L.LIBIDX[nm]: mode for nm, mode in C.CORE_NAMES.items()})
    C.WRAP_MODE.clear(); C.WRAP_MODE.update({L.LIBIDX[C.MODE_WRAP[m]]: m for m in C.MODE_WRAP})
    ID4.clear()
    for nm in ('CHK3', 'CHK3N', 'CC3', 'CC3N', 'EQS', 'SHAMS', 'PROD3', 'PCORE3', 'vone4', 'cchk3'):
        ID4[nm] = L.LIBIDX[nm]
    C.WRAPS.update([ID4['CHK3'], ID4['CHK3N']])
    C.WRAP_MODE[ID4['CHK3']] = MODE3
    C.WRAP_MODE[ID4['CHK3N']] = MODE3N
    return comp


_COMP4 = build_library4()
WRAP4 = {MODE3: ID4['CHK3'], MODE3N: ID4['CHK3N']}
CORE4 = {MODE3: ID4['CC3'], MODE3N: ID4['CC3N']}
WRAPS4 = {ID4['CHK3'], ID4['CHK3N']}
assert L.LIBIDX['CHKS'] == C.ID['CHKS']

# ----------------------------------------------------------------------------------------------------------------
# 2. Templates, compilation, named programs
# ----------------------------------------------------------------------------------------------------------------
K_MAIN = S.K_MAIN
V_MAIN = K_MAIN // 4
A_GE14, A_EQ12, A_LE14, A_WORK, A_STRIKE = S.A_GE14, S.A_EQ12, S.A_LE14, S.A_WORK, S.A_STRIKE
BOSS_Q = S.BOSS_Q
WORKER_Q = S.WORKER_Q
ANAME = S.ANAME
bcode, bname = S.bcode, S.bname
cons = S.cons
a_term = S.a_term
enumerate_templates, nodes, dt, dt_atoms, dt_eval = S.enumerate_templates, S.nodes, S._bt, S.dt_atoms, S.dt_eval
dt = S.dt
_A, _if, _L = S._A, S._if, S._L

# identity atoms: ('E', name).  Worker: EQ (identity) / SW (sham).  Boss: N1, N2 (named quote T1), EQW (w1 vs w2);
# shams S1, S2, S3.
EQ_W = ('E', 'EQ')
N1, N2, EQW = ('E', 'N1'), ('E', 'N2'), ('E', 'EQW')
WORKER_ATOMS0 = list(S.WORKER_ATOMS)
BOSS_ATOMS0 = list(S.BOSS_ATOMS)
PROBE_ATOMS = list(S.BOSS_ATOMS)
# Grammars: 'noeq' (the realizable run's atoms) and 'id' (plus EQ for workers, N1, N2, EQW for bosses).  The arms of
# the id grammar share every spelling; an arm only says which identity atoms are live (compiled to EQS) and which are
# shams (compiled to SHAMS: the same term shape and step count, always false) -- notes §1.0 items 4-5.
ARMS = {
    'noeq': ('noeq', frozenset()),
    'eq': ('id', frozenset(['EQ', 'N1', 'N2', 'EQW'])),
    'sham': ('id', frozenset()),
    'eqnoT': ('id', frozenset(['EQ', 'EQW'])),
}


def grammar_atoms(gram):
    if gram == 'noeq': return WORKER_ATOMS0, BOSS_ATOMS0
    return WORKER_ATOMS0 + [EQ_W], BOSS_ATOMS0 + [N1, N2, EQW]


def arm_atoms(arm):
    return grammar_atoms(ARMS[arm][0])


def live_of(arm):
    return ARMS[arm][1]


def atom_name(at):
    if at[0] == 'E': return at[1]
    return S.atom_name(at)


def leaf_name(l): return S.leaf_name(l)


def show(x):
    t = x[0]
    if t == 'L': return leaf_name(x[1])
    if t == 'A': return atom_name(x[1])
    if t == 'not': return 'not(%s)' % show(x[1])
    if t in ('and', 'or'): return '%s(%s,%s)' % (t, show(x[1]), show(x[2]))
    return 'if(%s,%s,%s)' % (show(x[1]), show(x[2]), show(x[3]))


def show_dt(t):
    if not isinstance(t, tuple): return leaf_name(t)
    return '%s?%s:%s' % (atom_name(t[0]), show_dt(t[1]), show_dt(t[2]))


def tagged(t):
    return any(a[0] == 'O' or a == EQ_W for a in dt_atoms(t))


LEAFVAL = S.LEAFVAL


def leaf_term(l): return S.leaf_term(l)


def carrier4(body, certs):
    """lam me. lam x. lam y. lam s. (lam certs. body) CERTS."""
    return ('lam', ('lam', ('lam', ('lam', ('app', ('lam', body), C.data_term(certs))))))


# inside BODY: certs = v0, s = v1, y = v2, x = v3, me = v4
ME, VX, VY, VS = ('v', 4), ('v', 3), ('v', 2), ('v', 1)
IS1 = ('eq', VS, N(1))
WORKER_ENC = ('if', IS1, P(VX, P(ME, VY)), P(VX, P(VY, ME)))
WORKER_OTHER = ('if', IS1, N(2), N(1))


def ARG4(V, enc, j, A, K):
    return P(N(V), P(enc, P(j, P(a_term(A), N(K)))))


def CALL4(V, enc, j, A, K):
    return ('app', ('lib', ID4['CHK3']), ARG4(V, enc, j, A, K))


def initial4(p, x, y, s):
    return ('app', ('app', ('app', ('app', p, ('quote', p)), ('quote', x)), ('quote', y)), N(s))


def conf_term(enc, j):
    b, w1, w2 = enc
    if j == 0: return initial4(b, w1, w2, 0)
    if j == 1: return initial4(w1, b, w2, 1)
    return initial4(w2, b, w1, 2)


def mk_arg4(V, enc, j, A, K):
    b, w1, w2 = enc
    return P(N(V), P(P(('quote', b), P(('quote', w1), ('quote', w2))), P(N(j), P(a_term(A), N(K)))))




def probe_const4(s, K=K_MAIN):
    """The quoted constant boss pay(s, none) (s: 0 -> wage 0, 1 -> 1/4) with its constant list."""
    key = (s, K)
    p = _PROBE.get(key)
    if p is None:
        code = bcode(S.PROBE_S[s], 1)
        p = carrier4(N(code), S.constant_list(code))
        _PROBE[key] = p
    return p


_PROBE = {}
T1_TEMPLATE = _if(_A(('B', A_EQ12)), _L('W'), _L('S'))


def atom_term(at, role, V, K, slot_override=None, live=frozenset(['EQ', 'N1', 'N2', 'EQW'])):
    """live: the identity atoms compiled to EQS (the others to SHAMS).  slot_override (corrupted instance): a worker
    that reads a fixed slot label instead of the evaluator's."""
    if at[0] == 'E':
        nm = at[1]
        lib = ID4['EQS'] if nm in live else ID4['SHAMS']
        if nm == 'EQ': a, b = ME, VY
        elif nm == 'N1': a, b = VX, ('quote', t1_source())
        elif nm == 'N2': a, b = VY, ('quote', t1_source())
        elif nm == 'EQW': a, b = VX, VY
        else: raise ValueError(at)
        return ('app', ('lib', lib), P(a, b))
    if role == 'W':
        if slot_override is None:
            enc, other = WORKER_ENC, WORKER_OTHER
        else:
            enc = P(VX, P(ME, VY)) if slot_override == 1 else P(VX, P(VY, ME))
            other = N(2 if slot_override == 1 else 1)
        if at[0] == 'B':
            return CALL4(V, enc, N(0), at[1], K)
        return CALL4(V, enc, other, at[1], K)
    _, j, s, A = at
    enc = P(('quote', probe_const4(s, K)), P(VX, VY))
    return CALL4(V, enc, N(j), A, K)


def cond_term(b, role, V, K, **kw):
    if b[0] == 'A': return atom_term(b[1], role, V, K, **kw)
    if b[0] == 'not': return ('if', cond_term(b[1], role, V, K, **kw), F_, T_)
    if b[0] == 'and': return ('if', cond_term(b[1], role, V, K, **kw), cond_term(b[2], role, V, K, **kw), F_)
    return ('if', cond_term(b[1], role, V, K, **kw), T_, cond_term(b[2], role, V, K, **kw))


def body_term(x, role, V, K, **kw):
    if x[0] == 'L': return leaf_term(x[1])
    return ('if', cond_term(x[1], role, V, K, **kw), body_term(x[2], role, V, K, **kw),
            body_term(x[3], role, V, K, **kw))


_T1SRC = {}


def t1_source(K=K_MAIN):
    """T1's carrier with the empty list: the named quote (EQS strips the list, so only its code matters)."""
    if K not in _T1SRC:
        _T1SRC[K] = carrier4(body_term(T1_TEMPLATE, 'W', K // 4, K), 0)
    return _T1SRC[K]


def compile_program(x, role, lst, V=V_MAIN, K=K_MAIN, **kw):
    return carrier4(body_term(x, role, V, K, **kw), lst)


def run_value(p, x, y, s, K):
    v, n = L.run_big(L.evaluate, initial4(p, x, y, s), K)
    return v, n


def play3(b, w1, w2, K=K_MAIN):
    """Whole plays by the term: (boss code, a1, a2) after defaults, step counts, raw values."""
    vb, nb = run_value(b, w1, w2, 0, K)
    v1, n1 = run_value(w1, b, w2, 1, K)
    v2, n2 = run_value(w2, b, w1, 2, K)
    db = vb if isinstance(vb, int) and 0 <= vb < 9 else 1
    d1 = v1 if v1 in ('C', 'D') else 'C'
    d2 = v2 if v2 in ('C', 'D') else 'C'
    return (db, d1, d2), (nb, n1, n2), (vb, v1, v2)


def term_check(enc, j, A, V=V_MAIN, K=K_MAIN, mode=MODE3):
    """Clean run of capk(V, CC3, arg) by the checker term: (value, inner steps)."""
    n = CORE4[mode]
    arg = mk_arg4(V, enc, j, A, K)
    key = (n, V, L.tval_to_rt(arg))
    rec = L.CACHE.get(key)
    if rec is None:
        v, steps = L.run_big(L.evaluate, ('capk', N(V), ('lib', n), arg))
        rec = L.CACHE.get(key)
        if rec is None: rec = (v, steps - 1)
    return rec


def term_prod(enc, j, A, Pcap=V_MAIN, V=V_MAIN, K=K_MAIN, fuel=None):
    """PROD3 by the term at the producer's own box: (script data | None, steps, outcome)."""
    arg = P(N(Pcap), mk_arg4(V, enc, j, A, K))
    tm = ('app', ('lib', ID4['PROD3']), arg)
    v, n = L.run_big(L.evaluate, tm, fuel if fuel is not None else 10 ** 9)
    if v == 'BOT': return None, n, 'fuelTO'
    if v == 'TO': return None, n, 'capTO'
    if v == L.LIB_CONSTS['NONE']: return None, n, 'none'
    return v, n, 'found'


# ---- named templates (notes §1.3)
P1_14S, P1_0S, P2_14S, P2_0S, P1_0W = S.P1_14S, S.P1_0S, S.P2_14S, S.P2_0S, S.P1_0W
B12, B14, BL14, OS, OW = S.B12, S.B14, S.BL14, S.OS, S.OW
EQa, N1a, EQWa = _A(EQ_W), _A(N1), _A(EQW)
NAMED_B = dict(S.NAMED_B)
NAMED_B.update({'B_eq': _if(N1a, _L(7), _L(1)), 'B_id': _if(EQWa, _L(7), _L(1))})
NAMED_W = dict(S.NAMED_W)
NAMED_W.update({
    'U_eq': _if(EQa, _if(B12, _L('W'), _L('S')), _L('W')),
    'XM': _if(('and', B12, EQa), _L('W'), _L('S')),
    'T1p': _if(('not', B12), _L('S'), _L('W')),
})


# ----------------------------------------------------------------------------------------------------------------
# 3. The host replay (an ExactHost with K_3' roots) -- validation of the symbolic layer
# ----------------------------------------------------------------------------------------------------------------
def parse_arg4(v):
    return S.parse_arg3(v)


def h_getcerts4(prog):
    try:
        b = prog
        for _ in range(4):
            assert b[0] == 'lam'; b = b[1]
        if b[0] == 'app' and b[1][0] == 'lam':
            return C.term_data(b[2])
    except Exception:
        return None
    return None


def h_chkstate4(phi):
    _, t, f, A, m = phi
    if f == 0: return None
    ctx, kind, pay, ito = C.hdecompose(t)
    if kind != 'call': return None
    n, v = pay
    if n not in WRAPS4: return None
    Vc = C.parse_carg(v)
    if Vc is None: return None
    u = Vc + 6
    fuels = [fr[1] for fr in ctx if fr[0] == 'sim']
    if not (u <= f and all(k >= u for k in fuels)): return None
    fr = f - u
    return (('cbox', n, v), S.h_read3(L.plug(ctx, T_, u), fr, A, 1), S.h_read3(L.plug(ctx, F_, u), fr, A, 1))


class HostCheck4(CP.ExactHost):
    """The realizable run's HostCheck3 over K_3' (four-abstraction roots); ideal (no EvR* budget)."""

    def __init__(self):
        super().__init__()

    def _ccore(self, mode, v):
        if mode not in (MODE3, MODE3N):
            return super()._ccore(mode, v)
        n = WRAP4[mode]
        r = self._vone(n, v)
        if r is None: return 'F'
        if mode == MODE3N: return 'T'
        done = [v]
        todo = list(r)
        while todo:
            y = todo.pop(0)
            if y in done: continue
            if len(done) >= M_CAP: return 'F'
            ry = self._vone(n, y)
            if ry is None: return 'F'
            todo = list(ry) + todo
            done.append(y)
        return 'T'

    def _vone(self, n, v):
        fs = parse_arg4(v)
        if fs is None: return None
        V, ENC, enc, j, A, K = fs
        if j not in (0, 1, 2): return None
        cl = h_getcerts4(enc[j])
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
        fs = parse_arg4(b[2])
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
            if b is None or b[0] != 'cbox' or b == Rb or b[1] not in WRAPS4: return None
            Vb = C.parse_carg(b[2])
            if Vb is None or Vb < V: return None
            res = self.check(b[1], b[2])
            return [] if (res == 'T') == (rule == C.RUN) else None
        if rule == C.EVS:
            x = at(Rf, j)
            if x is None or x[0] != 'atom' or not ps: return None
            s = S.h_evstar3(x, None)
            if s is None: return None
            return self.cchk3(n, Rb, xf, V, ps[0], Lf, C.fadd(s[0], C.fdel(x, Rf)))
        if rule == C.CHKR:
            x = at(Rf, j)
            if x is None or x[0] != 'atom' or len(ps) < 2: return None
            s = h_chkstate4(x)
            if s is None: return None
            B, rT, rF = s
            Rx = C.fdel(x, Rf)
            v1 = self.cchk3(n, Rb, xf, V, ps[0], C.fadd(B, Lf), C.fadd(rT, Rx))
            if v1 is None: return None
            v2 = self.cchk3(n, Rb, xf, V, ps[1], Lf, C.fadd(B, C.fadd(rF, Rx)))
            if v2 is None: return None
            return v1 + v2
        return None

    def check4(self, enc, j, A, V=V_MAIN, K=K_MAIN, mode=MODE3):
        return self.check(WRAP4[mode], mk_arg4(V, enc, j, A, K))


def script_from_rt(v):
    """A runtime script value (as returned by PROD3) -> host data (nested tuples)."""
    return L.rt_to_tval(v) if not isinstance(v, (tuple, int, str)) else _rt_data(v)


def _rt_data(v):
    if isinstance(v, tuple): return (_rt_data(v[0]), _rt_data(v[1]))
    return v


# ----------------------------------------------------------------------------------------------------------------
# 4. The symbolic layer over run trees
# ----------------------------------------------------------------------------------------------------------------
TOPS, BOTS = ('top',), ('bot',)


def node_at(t, path):
    x = t
    for br in path:
        x = x[1] if br else x[2]
    return x


def idval_fn(ctx):
    """ctx: identity values at a root, dict name -> bool (shams absent = False)."""
    return lambda nm: bool(ctx.get(nm, False))


def sym_evstar(t, path, Aset, idv):
    """EvR* from the state before node `path`: pass identity atoms by their values; stop at a call or a value."""
    while True:
        x = node_at(t, path)
        if not isinstance(x, tuple):
            return TOPS if LEAFVAL.get(x, x) in Aset else BOTS
        if x[0][0] == 'E':
            path = path + (idv(x[0][1]),)
            continue
        return ('call', path)


def hypable(role, at):
    return role == 'W' and at[0] == 'O'


def sym_produce(t, role, A, alpha, idv):
    """The path tactic (H) on run tree t with assignment alpha (box atoms -> bool) and identity values idv."""
    Aset_ = set(A)
    count = [0]

    def tac(Lf, Rf, acc):
        count[0] += 1
        if count[0] > S.PathProducer.BOUND: return None
        if BOTS in Lf or TOPS in Rf or any(x in Rf and x[0] in ('pre', 'call', 'box') for x in Lf): return C.node(C.AX, 0)
        for jj, b in enumerate(Rf):
            if b[0] == 'box' and alpha.get(b[1]) is True:
                at = b[1]
                if hypable(role, at):
                    acc.append(('H', at)); return C.node(C.HYP, jj)
                acc.append(('R', at)); return C.node(C.RUN, jj)
        for jj, b in enumerate(Lf):
            if b[0] == 'box' and alpha.get(b[1]) is False:
                acc.append(('N', b[1])); return C.node(C.RUNNEG, jj)
        for jj, x in enumerate(Rf):
            if x[0] not in ('pre', 'call'): continue
            if x[0] == 'pre':
                s = sym_evstar(t, x[1], Aset_, idv)
                p = tac(Lf, C.fadd(s, C.fdel(x, Rf)), acc)
                return None if p is None else C.node(C.EVS, jj, p)
            path = x[1]
            nd = node_at(t, path)
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


def id_atoms(t):
    return [a for a in dt_atoms(t) if a[0] == 'E']


def box_atoms(t):
    return [a for a in dt_atoms(t) if a[0] != 'E']


def h_list(t, role):
    """The H list of run tree t: [(A, script)] in order (notes §1.1.4).  Returns (entries, {A: [script, ...]})."""
    fam = WORKER_Q if role == 'W' else BOSS_Q
    ats = dt_atoms(t)
    entries, per = [], {}
    for A in fam:
        found = []
        for k, bits in enumerate(itertools.product([True, False], repeat=len(ats))):
            al = dict(zip(ats, bits))
            idv = (lambda al: (lambda nm: al.get(('E', nm), False)))(al)
            alpha = {a: v for a, v in al.items() if a[0] != 'E'}
            s, acc = sym_produce(t, role, A, alpha, idv)
            if s is None: continue
            if any(s == f[0] for f in found): continue
            nh = sum(1 for a in acc if a[0] == 'H')
            found.append((s, nh, k))
        found.sort(key=lambda r: (r[1], r[2]))
        per[A] = [s for s, _, _ in found]
        entries += [(A, s) for s in per[A]]
    return entries, per


def sym_check(t, role, A, script, idv, boxval):
    """The term's script check (cchk3) symbolically on run tree t at a root with identity values idv.  boxval(atom)
    returns 'T' | 'F' | 'TO' (it may raise the evaluator's regress).  Returns (used Hyp atoms | None, calls) where
    calls lists (atom, value) for every Run/RunNeg in the order the term makes them."""
    Aset_ = set(A)
    calls = []

    def at(lst, j):
        return lst[j] if isinstance(j, int) and 0 <= j < len(lst) else None

    def chk(nd, Lf, Rf):
        try:
            rule, (j, ps) = nd
            ps = C.uncons(ps)
        except Exception:
            return None
        if rule == C.AX:
            if BOTS in Lf or TOPS in Rf or any(x in Rf and x[0] in ('pre', 'call', 'box') for x in Lf): return []
            return None
        if rule == C.HYP:
            b = at(Rf, j)
            if b is None or b[0] != 'box': return None
            a = b[1]
            # isenc: an encounter box (same wrapper, V, encounter, K): worker B and O atoms; never a probe
            if role == 'W': return [a]
            return None
        if rule in (C.RUN, C.RUNNEG):
            b = at(Rf if rule == C.RUN else Lf, j)
            if b is None or b[0] != 'box': return None
            v = boxval(b[1])
            calls.append((b[1], v))
            return [] if (v == 'T') == (rule == C.RUN) else None
        if rule == C.EVS:
            x = at(Rf, j)
            if x is None or x[0] != 'pre' or not ps: return None
            s = sym_evstar(t, x[1], Aset_, idv)
            return chk(ps[0], Lf, C.fadd(s, C.fdel(x, Rf)))
        if rule == C.CHKR:
            x = at(Rf, j)
            if x is None or x[0] != 'call' or len(ps) < 2: return None
            path = x[1]
            nd2 = node_at(t, path)
            B = ('box', nd2[0])
            rT, rF = ('pre', path + (True,)), ('pre', path + (False,))
            Rx = C.fdel(x, Rf)
            v1 = chk(ps[0], C.fadd(B, Lf), C.fadd(rT, Rx))
            if v1 is None: return None
            v2 = chk(ps[1], Lf, C.fadd(B, C.fadd(rF, Rx)))
            if v2 is None: return None
            return v1 + v2
        return None
    r = chk(script, (), (('pre', ()),))
    return r, calls


def sym_prod3(t, role, A, idv, boxval, log=None):
    """PROD3 symbolically: the path tactic on actual values with Hyp-first backtracking on Hyp-able boxes.  boxval(atom)
    -> 'T'|'F'|'TO' (the nested check the tactic calls).  Returns (script | None, calls) with calls the (atom, value)
    the tactic computed, in order.  log (optional list) receives the visit events used by the cost model."""
    Aset_ = set(A)
    calls = []

    def lg(*e):
        if log is not None: log.append(e)

    def ptac(al, Lf, Rf, c):
        if c > 63:
            lg('bound'); return None, c + 1
        c1 = c + 1
        if BOTS in Lf or TOPS in Rf or any(x in Rf and x[0] in ('pre', 'call', 'box') for x in Lf):
            lg('ax', Lf, Rf, len(al)); return C.node(C.AX, 0), c1
        for jj, b in enumerate(Rf):
            if b[0] == 'box' and al.get(b[1]) is True:
                lg('pos', Lf, Rf, len(al), jj); return C.node(C.HYP if hypable(role, b[1]) else C.RUN, jj), c1
        for jj, b in enumerate(Lf):
            if b[0] == 'box' and al.get(b[1]) is False:
                lg('neg', Lf, Rf, len(al), jj); return C.node(C.RUNNEG, jj), c1
        for jj, x in enumerate(Rf):
            if x[0] not in ('pre', 'call'): continue
            if x[0] == 'pre':
                s = sym_evstar(t, x[1], Aset_, idv)
                if log is not None:
                    pth = x[1]
                    while True:
                        y = node_at(t, pth)
                        if isinstance(y, tuple) and y[0][0] == 'E':
                            pth = pth + (idv(y[0][1]),); continue
                        break
                    lg('ev', Lf, Rf, len(al), jj, x[1], None if isinstance(y, tuple) else LEAFVAL.get(y, y))
                q, cc = ptac(al, Lf, C.fadd(s, C.fdel(x, Rf)), c1)
                return (None if q is None else C.node(C.EVS, jj, q)), cc
            path = x[1]
            nd = node_at(t, path)
            B = ('box', nd[0])
            Rx = C.fdel(x, Rf)
            v = al.get(nd[0])
            lg('ck', Lf, Rf, len(al), jj, path, v is None, hypable(role, nd[0]))

            def branch(al2, cc):
                q1, cc1 = ptac(al2, C.fadd(B, Lf), C.fadd(('pre', path + (True,)), Rx), cc)
                if q1 is None:
                    lg('br1fail'); return None, cc1
                q2, cc2 = ptac(al2, Lf, C.fadd(B, C.fadd(('pre', path + (False,)), Rx)), cc1)
                if q2 is None:
                    lg('br2fail'); return None, cc2
                lg('brok'); return C.node(C.CHKR, jj, q1, q2), cc2
            if v is None:
                if hypable(role, nd[0]):
                    al2 = dict(al); al2[nd[0]] = True
                    q, cc = branch(al2, c1)
                    if q is not None: return q, cc
                    bv = boxval(nd[0]); calls.append((nd[0], bv))
                    lg('call', bv)
                    if bv == 'T':
                        lg('hypdead'); return None, c1
                    al2 = dict(al); al2[nd[0]] = False
                    lg('retry')
                    return branch(al2, c1)
                bv = boxval(nd[0]); calls.append((nd[0], bv))
                lg('call', bv)
                al2 = dict(al); al2[nd[0]] = (bv == 'T')
                return branch(al2, c1)
            return branch(al, c1)
        lg('noatom', Lf, Rf, len(al))
        return None, c1
    q, _ = ptac({}, (), (('pre', ()),), 0)
    return q, calls


# ----------------------------------------------------------------------------------------------------------------
# 5. Step-count instrumentation (notes §1.7): vone4 windows and nested replay charges
# ----------------------------------------------------------------------------------------------------------------
class Probe:
    """Records, while active, every vone4 call and every script-node call (cchk3) as windows: (kind, argument,
    inclusive steps in its own context, nested replay charges made directly inside it, the inclusive steps of its
    direct child windows, context depth, result).  own = inclusive - replays - children."""

    def __init__(self):
        self.windows = []
        self.replays = []
        self._stack = []

    def __enter__(self):
        self.windows.clear(); self.replays.clear(); self._stack.clear()
        _PROBE_STACK.append(self)
        return self

    def __exit__(self, *a):
        _PROBE_STACK.pop()
        return False


_PROBE_STACK = []
_ORIG = {}


def _wrap_lib(name, kind):
    i = ID4[name]
    orig = L.LIBCODE[i]
    _ORIG[name] = orig

    def wrapped(env):
        if not _PROBE_STACK:
            return orig(env)
        pr = _PROBE_STACK[-1]
        d = L.CLEAN_DEPTH[0]
        rec = [L.ST[0], 0, 0, d, len(pr.windows)]
        parent = None
        for w in reversed(pr._stack):
            if w[3] == d:
                parent = w; break
        pr._stack.append(rec)
        pr.windows.append(None)
        res = 'EXC'
        try:
            res = orig(env)
            return res
        finally:
            pr._stack.pop()
            incl = L.ST[0] - rec[0]
            if parent is not None: parent[2] += incl
            pr.windows[rec[4]] = (kind, env[0], incl, rec[1], rec[2], d, res)
    L.LIBCODE[i] = wrapped


def _install_probe():
    if _ORIG: return
    _wrap_lib('vone4', 'vone')
    _wrap_lib('cchk3', 'node')
    orig_replay = L.replay_cached
    _ORIG['replay'] = orig_replay

    def replay_wrapped(rec, key):
        if _PROBE_STACK:
            pr = _PROBE_STACK[-1]
            d = L.CLEAN_DEPTH[0]
            for w in reversed(pr._stack):
                if w[3] == d:
                    w[1] += rec[1]; break
            pr.replays.append((key, rec[0], rec[1], d))
        return orig_replay(rec, key)
    L.replay_cached = replay_wrapped


def win_own(w):
    return w[2] - w[3] - w[4]


_install_probe()


# ----------------------------------------------------------------------------------------------------------------
# 6. Own-step measurement by the term with forced nested values (notes §1.7)
# ----------------------------------------------------------------------------------------------------------------
DUMMY_B = carrier4(N(998), 0)                       # a boss quote that is no catalogue source
DUMMY_W = (carrier4(N(997), 0), carrier4(N(996), 0))  # two distinct worker quotes, no catalogue sources


def list_data(entries):
    """[(A, script)] -> the certificate list data (canonical order is the caller's)."""
    return cons([(cons(A), s) for A, s in entries])


def worker_roles(role, slot, prog, idctx):
    """A measurement encounter for subject `prog` in its slot with the identity relations idctx; returns (enc, j).
    Worker idctx: {'EQ': bool} (the other worker is a copy of the subject's source); the copy carries an empty list.
    Boss idctx: {'N1', 'N2', 'EQW'}."""
    if role == 'W':
        other = idctx['copy'] if idctx.get('EQ') else DUMMY_W[0]
        if slot == 1: return (DUMMY_B, prog, other), 1
        return (DUMMY_B, other, prog), 2
    n1, n2, ew = idctx.get('N1', False), idctx.get('N2', False), idctx.get('EQW', False)
    t1 = t1_source()
    w1 = t1 if n1 else DUMMY_W[0]
    if n2: w2 = t1
    elif ew: w2 = w1
    else: w2 = DUMMY_W[1]
    assert (w1 is w2) == bool(ew) or (n1 and n2), (n1, n2, ew)
    return (prog, w1, w2), 0


def atom_box_arg(at, role, enc, j, V=V_MAIN, K=K_MAIN):
    """The check argument (term) of the box a template atom of subject j names at encounter enc."""
    if role == 'W':
        if at[0] == 'B': return mk_arg4(V, enc, 0, at[1], K)
        return mk_arg4(V, enc, 2 if j == 1 else 1, at[1], K)
    _, jj, s, A = at
    return mk_arg4(V, (probe_const4(s, K), enc[1], enc[2]), jj, A, K)


def force_boxes(boxes):
    """Pre-cache nested checks with forced values at zero cost: {arg term: 'T'|'F'}."""
    n = CORE4[MODE3]
    for arg, v in boxes.items():
        L.CACHE[(n, V_MAIN, L.tval_to_rt(arg))] = (v, 0)


def measure_vone(role, slot, prog, A, idctx, forced_atoms, tree):
    """Own steps of the subject's root vone4 window (nested checks forced at zero cost)."""
    L.CACHE.clear()
    enc, j = worker_roles(role, slot, prog, idctx)
    boxes = {atom_box_arg(a, role, enc, j): v for a, v in forced_atoms.items()}
    force_boxes(boxes)
    n = CORE4[MODE3]
    arg = mk_arg4(V_MAIN, enc, j, A, K_MAIN)
    with Probe() as pr:
        L.run_big(L.evaluate, ('capk', N(V_MAIN), ('lib', n), arg))
    top = [w for w in pr.windows if w[0] == 'vone' and w[5] == 1]
    w = top[0]
    return w[2] - w[3], w[3], w[6]


def measure_prod(role, slot, prog, A, idctx, forced_atoms):
    """Own steps of PROD3 at the subject's root (nested checks forced at zero cost): (steps, outcome, script)."""
    L.CACHE.clear()
    enc, j = worker_roles(role, slot, prog, idctx)
    boxes = {atom_box_arg(a, role, enc, j): v for a, v in forced_atoms.items()}
    force_boxes(boxes)
    sc, steps, out = term_prod(enc, j, A)
    return steps, out, (_rt_data(sc) if sc is not None else None)


def measure_play(role, slot, prog, idctx, forced_atoms):
    """The subject's own run steps with its calls forced at zero cost (wrapper overheads included)."""
    L.CACHE.clear()
    enc, j = worker_roles(role, slot, prog, idctx)
    boxes = {atom_box_arg(a, role, enc, j): v for a, v in forced_atoms.items()}
    force_boxes(boxes)
    b, w1, w2 = enc
    if j == 0: v, n = run_value(b, w1, w2, 0, K_MAIN)
    elif j == 1: v, n = run_value(w1, b, w2, 1, K_MAIN)
    else: v, n = run_value(w2, b, w1, 2, K_MAIN)
    return n, v


# ----------------------------------------------------------------------------------------------------------------
# 7. Symbolic traces aligned with the term's node windows (for the cost model)
# ----------------------------------------------------------------------------------------------------------------
def sym_check_trace(t, role, A, script, idv, boxval):
    """sym_check with a record per visited node, in the term's visiting order: (rule, Lf, Rf, info) where info is,
    for EvR*: ('ok', start path, leaf value at the end or None) or ('bad',); for ChkR: ('ok'|'p1'|'p2', call path,
    len(v1)) or ('bad',); for Ax: ok; for Run/RunNeg/Hyp: ok.  Returns (used | None, calls, nodes)."""
    Aset_ = set(A)
    calls, nodes_ = [], []

    def at(lst, j):
        return lst[j] if isinstance(j, int) and 0 <= j < len(lst) else None

    def leaf_after(path):
        while True:
            y = node_at(t, path)
            if isinstance(y, tuple) and y[0][0] == 'E':
                path = path + (idv(y[0][1]),); continue
            return None if isinstance(y, tuple) else LEAFVAL.get(y, y)

    def chk(nd, Lf, Rf):
        try:
            rule, (j, ps) = nd
            ps = C.uncons(ps)
        except Exception:
            return None
        rec = [rule, Lf, Rf, None]
        nodes_.append(rec)
        if rule == C.AX:
            ok = BOTS in Lf or TOPS in Rf or any(x in Rf and x[0] in ('pre', 'call', 'box') for x in Lf)
            rec[3] = ok
            return [] if ok else None
        if rule == C.HYP:
            b = at(Rf, j)
            ok = b is not None and b[0] == 'box' and role == 'W'
            rec[3] = ok
            return [b[1]] if ok else None
        if rule in (C.RUN, C.RUNNEG):
            b = at(Rf if rule == C.RUN else Lf, j)
            if b is None or b[0] != 'box':
                rec[3] = False; return None
            v = boxval(b[1])
            calls.append((b[1], v))
            ok = (v == 'T') == (rule == C.RUN)
            rec[3] = ok
            return [] if ok else None
        if rule == C.EVS:
            x = at(Rf, j)
            if x is None or x[0] != 'pre' or not ps:
                rec[3] = ('bad',); return None
            rec[3] = ('ok', x[1], leaf_after(x[1]))
            s = sym_evstar(t, x[1], Aset_, idv)
            return chk(ps[0], Lf, C.fadd(s, C.fdel(x, Rf)))
        if rule == C.CHKR:
            x = at(Rf, j)
            if x is None or x[0] != 'call' or len(ps) < 2:
                rec[3] = ('bad',); return None
            path = x[1]
            B = ('box', node_at(t, path)[0])
            Rx = C.fdel(x, Rf)
            v1 = chk(ps[0], C.fadd(B, Lf), C.fadd(('pre', path + (True,)), Rx))
            if v1 is None:
                rec[3] = ('p1', path, 0); return None
            v2 = chk(ps[1], Lf, C.fadd(B, C.fadd(('pre', path + (False,)), Rx)))
            if v2 is None:
                rec[3] = ('p2', path, len(v1)); return None
            rec[3] = ('ok', path, len(v1))
            return v1 + v2
        rec[3] = False
        return None
    r = chk(script, (), (('pre', ()),))
    return r, calls, nodes_


def term_tagcount(t, c):
    """Tag counts of a term, not descending into quotes."""
    tag = t[0]
    c[tag] = c.get(tag, 0) + 1
    if tag in ('v', 'nat', 'con', 'lib', 'quote'): return c
    if tag == 'op':
        term_tagcount(t[2], c); term_tagcount(t[3], c); return c
    if tag == 'sim':
        term_tagcount(t[2], c); return c
    for x in t[1:]:
        if isinstance(x, tuple): term_tagcount(x, c)
    return c


def data_count(d):
    """(pairs, nats, constructors) of a data value."""
    if isinstance(d, tuple):
        a = data_count(d[0]); b = data_count(d[1])
        return (1 + a[0] + b[0], a[1] + b[1], a[2] + b[2])
    if isinstance(d, str): return (0, 0, 1)
    return (0, 1, 0)


def measure_nodes(role, slot, prog, A, idctx, forced_atoms):
    """Instrumented root validation: [(kind, own steps, ok)] for the vone window then each node window, in order."""
    L.CACHE.clear()
    enc, j = worker_roles(role, slot, prog, idctx)
    force_boxes({atom_box_arg(a, role, enc, j): v for a, v in forced_atoms.items()})
    arg = mk_arg4(V_MAIN, enc, j, A, K_MAIN)
    with Probe() as pr:
        L.run_big(L.evaluate, ('capk', N(V_MAIN), ('lib', CORE4[MODE3]), arg))
    out = []
    started = False
    for w in pr.windows:
        if w[5] != 1: continue
        if w[0] == 'vone':
            if started: break                       # closure members: not this window's
            started = True
            out.append(('VONE', win_own(w), w[6]))
        else:
            q = w[1]
            out.append((q[1][0][0], win_own(w), w[6]))
    return out


# ----------------------------------------------------------------------------------------------------------------
# 8. Full-tree measurement (notes §1.7): a crafted list entry whose script traverses every node of the run tree at
#    the given identity values, with no Run/RunNeg/Hyp, under the outcome set of all leaf values; one term run gives
#    the own steps of every EvR* segment (keyed by its start path), every ChkR (keyed by its call path) and every Ax.
# ----------------------------------------------------------------------------------------------------------------
A_ALL = {'W': ('C', 'D'), 'B': tuple(range(9))}


def full_tree_script(t, role, idv):
    """Returns (script, visit) with visit the preorder list of (rule, key): EvR* key = start path, ChkR key = call path,
    Ax key = None."""
    Aset_ = set(A_ALL[role])
    visit = []

    def build(Lf, Rf):
        if BOTS in Lf or TOPS in Rf or any(x in Rf and x[0] in ('pre', 'call', 'box') for x in Lf):
            visit.append((C.AX, None))
            return C.node(C.AX, 0)
        for jj, x in enumerate(Rf):
            if x[0] == 'pre':
                visit.append((C.EVS, x[1]))
                s = sym_evstar(t, x[1], Aset_, idv)
                return C.node(C.EVS, jj, build(Lf, C.fadd(s, C.fdel(x, Rf))))
            if x[0] == 'call':
                path = x[1]
                visit.append((C.CHKR, path))
                nd = node_at(t, path)
                B = ('box', nd[0])
                Rx = C.fdel(x, Rf)
                p1 = build(C.fadd(B, Lf), C.fadd(('pre', path + (True,)), Rx))
                p2 = build(Lf, C.fadd(B, C.fadd(('pre', path + (False,)), Rx)))
                return C.node(C.CHKR, jj, p1, p2)
        raise AssertionError('no atom')
    s = build((), (('pre', ()),))
    return s, visit


def measure_full_tree(x, role, slot, idctx, idv, live):
    """Own steps per visited node of the full-tree script of template x (notes §1.7).  Returns (vone own, [(rule, key,
    own)], list data counts of the measurement list)."""
    t = dt(x)
    sc, visit = full_tree_script(t, role, idv)
    lst = list_data([(A_ALL[role], sc)])
    prog = compile_program(x, role, lst, live=live)
    ic = dict(idctx)
    if role == 'W' and ic.get('EQ'):
        ic['copy'] = compile_program(x, role, 0, live=live)
    L.CACHE.clear()
    enc, j = worker_roles(role, slot, prog, ic)
    arg = mk_arg4(V_MAIN, enc, j, A_ALL[role], K_MAIN)
    with Probe() as pr:
        L.run_big(L.evaluate, ('capk', N(V_MAIN), ('lib', CORE4[MODE3]), arg))
    ws = [w for w in pr.windows if w[5] == 1]
    vone = ws[0]
    assert vone[0] == 'vone' and vone[6] != 0, ('full tree did not validate', show(x))
    nodes = [w for w in ws[1:] if w[0] == 'node']
    assert len(nodes) == len(visit), (len(nodes), len(visit))
    out = []
    for (rule, key), w in zip(visit, nodes):
        assert w[1][1][0][0] == rule
        out.append((rule, key, win_own(w)))
    return win_own(vone), out, data_count(lst)


# ----------------------------------------------------------------------------------------------------------------
# 9. The registry of programs (spelling, inventory) and the cost model (notes §1.7)
# ----------------------------------------------------------------------------------------------------------------
FAM = {'W': WORKER_Q, 'B': BOSS_Q}
BOSS_ID_COMBOS = [(False, False, False), (False, False, True), (True, False, False), (False, True, False), (True, True, True)]


class Grammar:
    """One grammar's catalogue ('noeq' or 'id'): spellings per role, run trees, H lists (per run tree), masses."""

    def __init__(self, gram, nmax=7):
        self.gram = gram
        watoms, batoms = grammar_atoms(gram)
        self.roles = {}
        for role, atoms, leaves in (('W', watoms, ['W', 'S']), ('B', batoms, list(range(9)))):
            G = enumerate_templates(nmax, atoms, leaves)
            sp = [x for n in range(1, nmax + 1) for x in G[n]]
            nd = np.array([nodes(x) for x in sp])
            tau_of, members, tau = {}, [], np.zeros(len(sp), np.int64)
            for k, x in enumerate(sp):
                d = dt(x)
                tk = tau_of.get(d)
                if tk is None:
                    tk = len(members); tau_of[d] = tk; members.append([])
                tau[k] = tk; members[tk].append(k)
            self.roles[role] = dict(spellings=sp, nodes=nd, tau=tau, members=members, tau_of=tau_of,
                                    dts=[dt(sp[m[0]]) for m in members], counts={n: len(G[n]) for n in G})
        self._hl = {}
        w = self.roles['W']
        t1 = dt(T1_TEMPLATE)
        self.t1_spelling = w['spellings'].index(T1_TEMPLATE)

    def spelling_index(self, role, x):
        return self.roles[role]['spellings'].index(x)

    def hlist(self, role, tk):
        """H list of run tree tk: (entries [(A, script)], per {A: [scripts]})."""
        key = (role, tk)
        r = self._hl.get(key)
        if r is None:
            r = h_list(self.roles[role]['dts'][tk], role)
            self._hl[key] = r
        return r

    def mass(self, role, prior='L'):
        r = self.roles[role]
        w = 2.0 ** (-r['nodes'].astype(float))
        return w / w.sum()


def inv_entries(grammar, role, tk, inv):
    """Inventory -> list entries in canonical order (family order, then H order within a set).  inv: tuple over the
    family of tuples of script indices into the run tree's H list for that set."""
    _, per = grammar.hlist(role, tk)
    out = []
    for A, idx in zip(FAM[role], inv):
        for i in idx:
            out.append((A, per[A][i]))
    return out


def full_inv(grammar, role, tk):
    _, per = grammar.hlist(role, tk)
    return tuple(tuple(range(len(per[A]))) for A in FAM[role])


def empty_inv(role):
    return tuple(() for _ in FAM[role])


class Prog:
    """A registered program: role, grammar spelling index, inventory."""
    __slots__ = ('role', 'sp', 'tk', 'inv', 'entries', 'dc', 'lc', 'isT1', 'pid')

    def __init__(self, grammar, role, sp, inv, pid):
        r = grammar.roles[role]
        self.role, self.sp, self.inv, self.pid = role, sp, inv, pid
        self.tk = int(r['tau'][sp])
        self.entries = inv_entries(grammar, role, self.tk, inv)
        self.lc = list_counts(self.entries)
        self.dc = self.lc[:3]
        self.isT1 = (role == 'W' and sp == grammar.t1_spelling)


class Registry:
    def __init__(self, grammar):
        self.g = grammar
        self.progs = []
        self.index = {}

    def get(self, role, sp, inv):
        key = (role, sp, inv)
        pid = self.index.get(key)
        if pid is None:
            pid = len(self.progs)
            self.progs.append(Prog(self.g, role, sp, inv, pid))
            self.index[key] = pid
        return pid

    def __getitem__(self, pid):
        return self.progs[pid]


def ident_key(role, t, idv):
    """The identity values of the identity atoms of run tree t, as a sorted tuple of (name, bool)."""
    return tuple(sorted((a[1], bool(idv(a[1]))) for a in id_atoms(t)))


class CostModel:
    """Own-step tables by full-tree measurement (per spelling, slot, identity values) plus global constants fitted by
    calibration (notes §1.7).  The constants are set by `calibrate` (sog_full_run.py) and stored in COSTC."""

    def __init__(self, grammar, live, consts):
        self.g, self.live, self.c = grammar, live, consts
        self.ft = {}

    def ft_table(self, role, sp, slot, ik):
        key = (role, sp, slot, ik)
        r = self.ft.get(key)
        if r is None:
            x = self.g.roles[role]['spellings'][sp]
            d = dict(ik)
            idv = lambda nm: d.get(nm, False)
            if role == 'B':
                idctx = None
                for c in BOSS_ID_COMBOS:
                    cd = dict(zip(('N1', 'N2', 'EQW'), c))
                    if all(cd[k] == v for k, v in d.items()):
                        idctx = cd; break
                assert idctx is not None, d
            else:
                idctx = {'EQ': d.get('EQ', False)}
            vone, nodes_, dcl = measure_full_tree(x, role, slot, idctx, idv, frozenset(['EQ', 'N1', 'N2', 'EQW']))
            tab = {}
            for rule, key2, own in nodes_:
                if rule == C.EVS: tab[('E', key2)] = own
                elif rule == C.CHKR: tab[('K', key2)] = own
            r = (tab, dcl)
            self.ft[key] = r
        return r


# ----------------------------------------------------------------------------------------------------------------
# 10. Node costs (constants calibrated against the term: notes §1.x) and the abstract evaluator with costs
# ----------------------------------------------------------------------------------------------------------------
AbsAbort = S.AbsAbort
COSTC = dict(RUN=74, RUNNEG=76, HYP=75, CKBAD=51, CK_P1=-36, CK_P1_R=-16, CK_P2=-6, CK_USED=6,
             LIST_P=271, LIST_CON=-10, AMEM=8, AMEM_IN=-5,
             VONE=None,          # per role: coefficients over (1, pairs, nC, nD, scanned, attempts, ok, entries)
             BK=None)            # closure bookkeeping: see bk_steps


def amem_scan(v, A):
    A = list(A)
    return (A.index(v) + 1, 1) if v in A else (len(A), 0)


def ax_steps(Lf, Rf):
    """The Ax node's own steps from its sequent (caxiom: BOT in L, TOP in R, then a common formula; calibrated)."""
    c = 31
    if BOTS in Lf:
        return c + 9 * (Lf.index(BOTS) + 1)
    c += 9 * len(Lf)
    if TOPS in Rf:
        return c + 9 * (Rf.index(TOPS) + 1)
    c += 9 * len(Rf) + 9
    for x in Lf:
        if x in Rf and x[0] in ('pre', 'call', 'box'):
            return c + 16 + 8 * Rf.index(x)
        c += 26 + 8 * (len(Rf) - 1)
    return c


def list_counts(entries):
    """(pairs, nats, constructors, C constructors, D constructors) of a list's data."""
    p, n, k = data_count(list_data(entries))
    nC = sum(1 for A, _ in entries for a in A if a == 'C')
    nD = sum(1 for A, _ in entries for a in A if a == 'D')
    return p, n, k, nC, nD


def vone_steps(role, lc, scanned, att, ok, nents):
    c = COSTC['VONE'][role]
    f = (1, lc[0], lc[3], lc[4], scanned, att, int(ok), nents)
    return int(round(sum(a * b for a, b in zip(c, f))))


def bk_steps_feat(f, b):
    return sum(f[k] * b[k] for k in f)


def bk_steps(pops, ok):
    """Closure bookkeeping of ccore3/clos3 from the closure trace (calibrated: COSTC['BK'])."""
    b = COSTC['BK']
    if not pops and not ok:
        return b['F0']
    s = b['T0'] if ok else b['F1']
    for p in pops:
        if p[0] == 'hit': s += b['hit']
        elif p[0] == 'ins': s += b['ins'] + b['ins_cnt'] * p[1] + b['ins_len'] * p[2]
        elif p[0] == 'fail': s += b['fail'] + b['fail_cnt'] * p[1]
        else: s += b['cap']
    return s


def node_steps(t, role, A, rec, tab, dlist):
    rule, Lf, Rf, info = rec
    if rule == C.EVS:
        if info[0] == 'bad': raise ValueError('EvR* on a non-pre formula (not calibrated)')
        start, leaf = info[1], info[2]
        s = tab[('E', start)]
        if start == ():
            s += COSTC['LIST_P'] * dlist[0] + COSTC['LIST_CON'] * dlist[1]
        if leaf is not None:
            sa = amem_scan(leaf, A); sl = amem_scan(leaf, A_ALL[role])
            s += COSTC['AMEM'] * (sa[0] - sl[0]) + COSTC['AMEM_IN'] * (sa[1] - sl[1])
        return s
    if rule == C.CHKR:
        if info[0] == 'bad': return COSTC['CKBAD']
        s = tab[('K', info[1])]
        if info[0] == 'ok': return s + COSTC['CK_USED'] * info[2]
        if info[0] == 'p1': return s + COSTC['CK_P1'] + COSTC['CK_P1_R'] * (len(Rf) - 1)
        return s + COSTC['CK_P2']
    if rule == C.AX: return ax_steps(Lf, Rf)
    if rule == C.RUN: return COSTC['RUN']
    if rule == C.RUNNEG: return COSTC['RUNNEG']
    if rule == C.HYP: return COSTC['HYP']
    raise ValueError(rule)


class AbsEval4:
    """The abstract evaluator over registered programs (notes §1.4, §1.7).  Encounters:
      ('E', bview, x, y): worker pids x (slot 1), y (slot 2) beside a boss whose three wage boxes have the values
         bview (seeded; their costs are symbolic: cost vectors carry their multiplicities in positions 1..3);
      ('B', b, code): boss pid b; code[0:8] the values of its 8 probe boxes (seeded, symbolic costs in positions
         1..8), code[8:11] the identity relations (w1 is T1, w2 is T1, w1 and w2 one source).
    check(key) -> 'T'|'F'|'TO' (ideal, ExactHost regress semantics); cost(key) -> required-cost vector or None."""

    def __init__(self, reg, cm, live):
        self.reg, self.cm, self.live = reg, cm, frozenset(live)
        self.vtrie = {}
        self.clear()

    def clear(self):
        self.memo, self.deps, self.stack, self.dstack, self.costs = {}, {}, [], [], {}
        self.pops = {}
        self.eq_read = False

    def idv_worker(self, enc):
        rel = enc[4] if len(enc) > 4 else (self.reg[enc[2]].sp == self.reg[enc[3]].sp)
        on = 'EQ' in self.live and bool(rel)

        def f(nm):
            if nm == 'EQ':
                self.eq_read = True
                return on
            return False
        return f

    def idv_boss(self, code):
        live = self.live
        d = {'N1': bool(code[8]) and 'N1' in live, 'N2': bool(code[9]) and 'N2' in live,
             'EQW': bool(code[10]) and 'EQW' in live}
        return lambda nm: d.get(nm, False)

    @staticmethod
    def seeded(key):
        enc, j, A = key
        if enc[0] == 'E' and j == 0:
            i = BOSS_Q.index(A)
            return enc[1][i], i + 1
        if enc[0] == 'B' and A[0] == 'P':
            i = PROBE_ATOMS.index(A)
            return enc[2][i], i + 1
        return None, None

    @staticmethod
    def nvec(enc):
        return 4 if enc[0] == 'E' else 9

    def check(self, key):
        s, ix = self.seeded(key)
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
            res, cost = self._ccore(key)
        except AbsAbort:
            self.stack.pop(); self.dstack.pop()
            if self.stack: raise
            self.memo[key] = 'TO'; self.deps[key] = set(); self.costs[key] = None
            return 'TO'
        self.stack.pop(); d = self.dstack.pop()
        self.memo[key] = res; self.deps[key] = d; self.costs[key] = cost
        if self.dstack:
            self.dstack[-1] |= d; self.dstack[-1].add(key)
        return res

    def cost(self, key):
        s, ix = self.seeded(key)
        if s is not None:
            v = [0] * self.nvec(key[0]); v[ix] = 1
            return tuple(v)
        if key not in self.memo:
            if self.stack: raise RuntimeError('cost of an unevaluated key inside a check')
            self.check(key)
        return self.costs.get(key)

    def _ccore(self, key):
        n = self.nvec(key[0])
        r, c = self._vone(key)
        cost = list(c)
        if r is None:
            cost[0] += bk_steps((), False)
            self.pops[key] = ((), False)
            return 'F', tuple(cost)
        done = [key]
        todo = list(r)
        pops = []
        while todo:
            y = todo.pop(0)
            if y in done:
                pops.append(('hit',)); continue
            if len(done) >= M_CAP:
                pops.append(('cap',))
                cost[0] += bk_steps(tuple(pops), False)
                self.pops[key] = (tuple(pops), False)
                return 'F', tuple(cost)
            ry, cy = self._vone(y)
            for i in range(n): cost[i] += cy[i]
            if ry is None:
                pops.append(('fail', len(done)))
                cost[0] += bk_steps(tuple(pops), False)
                self.pops[key] = (tuple(pops), False)
                return 'F', tuple(cost)
            pops.append(('ins', len(done), len(ry)))
            todo = list(ry) + todo
            done.append(y)
        cost[0] += bk_steps(tuple(pops), True)
        self.pops[key] = (tuple(pops), True)
        return 'T', tuple(cost)

    @staticmethod
    def boxkey(key, atom):
        enc, j, A = key
        if enc[0] == 'E':
            if atom[0] == 'B': return (enc, 0, atom[1])
            return (enc, 2 if j == 1 else 1, atom[1])
        return (enc, 0, atom)                     # a probe box: seeded by the code

    def subject(self, key):
        enc, j, A = key
        if enc[0] == 'E':
            return (enc[2] if j == 1 else enc[3]), self.idv_worker(enc), j
        return enc[1], self.idv_boss(enc[2]), 0

    def _vone(self, key):
        """(used encounter boxes | None, cost vector) of one vone4 validation.  The traversal is memoized as a trie
        over the values of the nested boxes it queries (VTRIE: subject program, slot, set, identity values); a miss
        runs the symbolic traversal with a recording oracle and inserts its path."""
        enc, j, A = key
        n = self.nvec(enc)
        pid, idv, slot = self.subject(key)
        pr = self.reg[pid]
        role = pr.role
        t = self.reg.g.roles[role]['dts'][pr.tk]
        ik = ident_key(role, t, idv)
        tkey = (pid, slot, A, ik)
        VT_ = self.vtrie
        node = VT_.get(tkey)
        nested = []
        if node is not None:
            # walk: node = ('q', atom, {value: node}) | ('r', used atoms | None, steps)
            path_ok = True
            while node[0] == 'q':
                atom = node[1]
                bk = self.boxkey(key, atom)
                v = self.check(bk)
                nested.append(bk)
                nxt = node[2].get(v)
                if nxt is None:
                    path_ok = False; break
                node = nxt
            if path_ok:
                used, steps = node[1], node[2]
                res = None if used is None else [self.boxkey(key, a) for a in used]
                return res, self._vcost(key, n, steps, nested)
            nested = []
        # slow path: the symbolic traversal with a recording oracle
        tab, dcl = self.cm.ft_table(role, pr.sp, slot, ik)
        dlist = (pr.dc[0] - dcl[0], pr.dc[2] - dcl[2])
        seq = []

        def boxval(atom):
            bk = self.boxkey(key, atom)
            v = self.check(bk)
            nested.append(bk)
            seq.append((atom, v))
            return v
        steps = 0
        att = 0
        used = None
        scanned = len(pr.entries)
        for i, (A2, sc) in enumerate(pr.entries):
            if A2 != A: continue
            att += 1
            r, calls, nodes_ = sym_check_trace(t, role, A, sc, idv, boxval)
            for rec in nodes_:
                steps += node_steps(t, role, A, rec, tab, dlist)
            if r is not None:
                used = list(r)
                scanned = i + 1
                break
        steps += vone_steps(role, pr.lc, scanned, att, used is not None, len(pr.entries))
        # insert the path
        leaf = ('r', None if used is None else tuple(used), steps)
        if not seq:
            VT_[tkey] = leaf
        else:
            root = VT_.get(tkey)
            if root is None or root[0] != 'q':
                root = ('q', seq[0][0], {})
                VT_[tkey] = root
            nd = root
            for q, (atom, v) in enumerate(seq):
                assert nd[1] == atom
                if q + 1 < len(seq):
                    nx = nd[2].get(v)
                    if nx is None:
                        nx = ('q', seq[q + 1][0], {})
                        nd[2][v] = nx
                    nd = nx
                else:
                    nd[2][v] = leaf
        res = None if used is None else [self.boxkey(key, a) for a in used]
        return res, self._vcost(key, n, steps, nested)

    def _vcost(self, key, n, steps, nested):
        cost = [0] * n
        cost[0] = steps
        for bk in nested:
            c = self.costs.get(bk) if self.seeded(bk)[0] is None else self.cost(bk)
            if c is None: raise AbsAbort()
            for i in range(n): cost[i] += c[i]
        return tuple(cost)


VTRIE = {}


# ----------------------------------------------------------------------------------------------------------------
# 11. PROD3 own steps (calibrated linear model on the visit log; notes §1.7) and the evaluation layer
# ----------------------------------------------------------------------------------------------------------------
PROD_EVENTS = ('ax', 'pos', 'neg', 'ev', 'ck', 'noatom')


def prod_features(log, tab, dlist, A, role):
    """(base from the full-tree tables, feature dict) of a PROD3 visit log."""
    f = {}
    base = 0

    def add(k, v=1):
        f[k] = f.get(k, 0) + v
    for e in log:
        k = e[0]
        add('n_' + k)
        if k in PROD_EVENTS:
            Lf, Rf, nal = e[1], e[2], e[3]
            add(k + '_L', len(Lf)); add(k + '_R', len(Rf)); add(k + '_al', nal)
            add(k + '_axs', ax_steps(Lf, Rf))
            if k in ('pos', 'neg', 'ev', 'ck'): add(k + '_j', e[4])
        if k == 'ev':
            start = e[5]
            base += tab[('E', start)]
            if start == (): base += COSTC['LIST_P'] * dlist[0] + COSTC['LIST_CON'] * dlist[1]
            leaf = e[6]
            if leaf is not None:
                sa = amem_scan(leaf, A); sl = amem_scan(leaf, A_ALL[role])
                base += COSTC['AMEM'] * (sa[0] - sl[0]) + COSTC['AMEM_IN'] * (sa[1] - sl[1])
        if k == 'ck':
            base += tab[('K', e[5])]
            add('ck_new', int(e[6])); add('ck_hyp', int(e[6] and e[7]))
        if k == 'call':
            add('call_T', int(e[1] == 'T'))
    return base, f


def prod_steps(role, base, f, found):
    m = COSTC['PROD'][role]
    v = base + m['1'] + m.get('out_found' if found else 'out_none', 0)
    for k, c in f.items():
        v += c * m.get(k, 0.0)
    return int(round(v))


VPLUS = 1          # a check (or production) under cap k returns iff its total <= k + VPLUS (calibrated)
TO_CHARGE = 2      # a timed-out clean run under cap k charges k + TO_CHARGE when replayed
PROD_W = 4         # the PROD3 call's own steps around its PCORE3 clean run (calibrated)


def v3(v):
    return {'F': 0, 'T': 1, 'TO': 2}[v]


class Evaluator:
    """Executable values of encounters for one cell: grammar, arm (live identity atoms), production mode, K."""

    def __init__(self, gram, arm, prod_mode, K=K_MAIN, live=None):
        self.g = gram
        self.arm = arm
        self.live = live_of(arm) if live is None else live
        self.mode = prod_mode
        self.K, self.V, self.P = K, K // 4, K // 4
        self.reg = Registry(gram)
        self.cm = CostModel(gram, self.live, COSTC)
        self.ae = AbsEval4(self.reg, self.cm, self.live)
        self.const_cost = {}
        for s in (0, 1):
            code = bcode(S.PROBE_S[s], 1)
            prog = probe_const4(s, K)
            L.CACHE.clear()
            enc = (prog, DUMMY_W[0], DUMMY_W[1])
            self.const_cost[s] = tuple(term_check(enc, 0, A, self.V, K)[1] for A in BOSS_Q)
            self.const_view = getattr(self, 'const_view', {})
            self.const_view[s] = tuple('T' if code in A else 'F' for A in BOSS_Q)
        self._probe, self._boss, self._wrow, self._wact, self._prod = {}, {}, {}, {}, {}
        self._deps, self._wc, self._breads, self._canon, self._wci = {}, {}, {}, {}, {}
        self._probe_ideal = {}

    def maybe_clear(self, cap=400000):
        if len(self.ae.memo) > cap: self.ae.clear()

    # ---- pair level: probes
    def canon(self, pid):
        """The canonical program of pid's class (run tree, inventory, is T1): costs are computed on it (notes §1.x:
        respellings differ in own steps by a few percent; the approximation is measured by whole replays)."""
        c = self._canon.get(pid)
        if c is None:
            pr = self.reg[pid]
            r = self.g.roles[pr.role]
            if pr.isT1:
                c = pid
            else:
                ms = r['members'][pr.tk]
                csp = ms[0]
                if pr.role == 'W' and csp == self.g.t1_spelling:
                    csp = ms[1] if len(ms) > 1 else csp
                c = self.reg.get(pr.role, csp, pr.inv)
            self._canon[pid] = c
        return c

    def deps(self, pid):
        """(tagged, reads EQ) of a worker: whether a check about it depends on the co-worker's quote / identity."""
        r = self._deps.get(pid)
        if r is None:
            pr = self.reg[pid]
            t = self.g.roles[pr.role]['dts'][pr.tk]
            ats = dt_atoms(t)
            r = (any(a[0] == 'O' for a in ats), any(a == EQ_W for a in ats) and 'EQ' in self.live)
            self._deps[pid] = r
        return r

    def wcheck(self, subj, j, A, bview, other, rel):
        """(ideal value, cost vector, touched) of the check about worker subj (slot j; canonical pid) for set A beside
        co-worker `other` (canonical pid) with identity relation rel, under a seeded boss view.  touched: the evaluation
        consulted the co-worker (one of its boxes, a closure over it, or EQ); an untouched result holds for every
        co-worker and is cached independently of it."""
        ik = (subj, j, A, bview)
        r = self._wci.get(ik)
        if r is not None: return r
        key = (subj, j, A, bview, other, bool(rel))
        r = self._wc.get(key)
        if r is not None: return r
        self.maybe_clear()
        x, y = (subj, other) if j == 1 else (other, subj)
        k = (('E', bview, x, y, bool(rel)), j, A)
        fresh = k not in self.ae.memo
        self.ae.eq_read = False
        v = self.ae.check(k)
        c = self.ae.cost(k)
        if fresh:
            touched = self.ae.eq_read or bool(self.ae.pops.get(k, ((), False))[0])
            if not touched:
                for d in self.ae.deps.get(k, ()):
                    if d[0][0] == 'E' and d[1] != j:
                        touched = True; break
            if v == 'TO':
                touched = True          # a regress may involve the co-worker: keep it pair-specific
        else:
            touched = True
        r = (v, c if c is not None else (0, 0, 0, 0), touched)
        if touched:
            self._wc[key] = r
        else:
            self._wci[ik] = r
        return r

    def probe(self, x, y):
        key = (x, y)
        r = self._probe.get(key)
        if r is not None: return r
        px, py = self.reg[x], self.reg[y]
        rel = px.sp == py.sp
        cx, cy = self.canon(x), self.canon(y)
        vals, costs = [], []
        ideal_vals = []
        for at in PROBE_ATOMS:
            _, j, s, A = at
            subj, other = (cx, cy) if j == 1 else (cy, cx)
            v, c, _ = self.wcheck(subj, j, A, self.const_view[s], other, rel)
            ideal_vals.append(v)
            if v == 'TO':
                vals.append('TO'); costs.append(self.V + TO_CHARGE)
            else:
                tot = c[0] + sum(c[i + 1] * self.const_cost[s][i] for i in range(3))
                if tot > self.V + VPLUS:
                    vals.append('TO'); costs.append(self.V + TO_CHARGE)
                else:
                    vals.append(v); costs.append(tot)
        ids = (px.isT1, py.isT1, rel)
        r = (tuple(vals), tuple(costs), ids)
        self._probe[key] = r
        self._probe_ideal[key] = tuple(ideal_vals)
        return r

    # ---- boss rows
    def boss_reads(self, b):
        r = self._breads.get(b)
        if r is None:
            pr = self.reg[b]
            t = self.g.roles['B']['dts'][pr.tk]
            ats = dt_atoms(t)
            r = (tuple(i for i, a in enumerate(PROBE_ATOMS) if a in ats),
                 tuple(8 + i for i, a in enumerate((N1, N2, EQW)) if a in ats))
            self._breads[b] = r
        return r

    def boss_row(self, b, code):
        """code = (8 exec probe values, 3 identity bits).  Returns (action, ideal values (3), cost vectors (3 x 9));
        cached on the components the boss's run tree reads."""
        b = self.canon(b)
        pi, ii = self.boss_reads(b)
        rkey = (b, tuple(code[i] for i in pi), tuple(code[i] for i in ii))
        r = self._boss.get(rkey)
        if r is not None: return r
        # canonical code: unread probes F, unread identity bits False
        code = tuple(code[i] if i in pi else 'F' for i in range(8)) + tuple(code[i] if i in ii else False
                                                                            for i in range(8, 11))
        self.maybe_clear()
        pr = self.reg[b]
        t = self.g.roles['B']['dts'][pr.tk]
        idv = self.ae.idv_boss(code)
        vals = dict(zip(PROBE_ATOMS, code[:8]))
        act = dt_eval(t, lambda at: (idv(at[1]) if at[0] == 'E' else vals[at] == 'T'))
        enc = ('B', b, code)
        ideal, cv = [], []
        for A in BOSS_Q:
            k = (enc, 0, A)
            v = self.ae.check(k)
            c = self.ae.cost(k)
            ideal.append(v)
            cv.append(c if c is not None else (0,) * 9)
        r = (act, tuple(ideal), tuple(cv))
        self._boss[rkey] = r
        return r

    def boss_exec(self, b, x, y):
        """(action, exec values (3), required costs (3), code, probe costs) for boss b against workers x, y."""
        pv, pc, ids = self.probe(x, y)
        code = pv + ids
        act, ideal, cv = self.boss_row(b, code)
        ex, costs = [], []
        for i in range(3):
            c = cv[i]
            tot = c[0] + sum(c[k + 1] * pc[k] for k in range(8))
            if ideal[i] == 'TO' or tot > self.V + VPLUS:
                ex.append('TO'); costs.append(tot if ideal[i] != 'TO' else None)
            else:
                ex.append(ideal[i]); costs.append(tot)
        return act, tuple(ex), tuple(costs), code, pc

    # ---- worker rows
    def worker_row(self, x, y, bex):
        key = (x, y, bex)
        r = self._wrow.get(key)
        if r is not None: return r
        rel = self.reg[x].sp == self.reg[y].sp
        cx, cy = self.canon(x), self.canon(y)
        ideal, cv = [], []
        for j, subj, other in ((1, cx, cy), (2, cy, cx)):
            for A in WORKER_Q:
                v, c, _ = self.wcheck(subj, j, A, bex, other, rel)
                ideal.append(v); cv.append(c)
        r = (tuple(ideal), tuple(cv))
        self._wrow[key] = r
        return r

    def worker_act(self, x, bits):
        """Action of worker x given (B>=1/4, B=1/2, B<=1/4, O:S, O:W, EQ) truth values."""
        pr = self.reg[x]
        t = self.g.roles['W']['dts'][pr.tk]
        d = {('B', A_GE14): bits[0], ('B', A_EQ12): bits[1], ('B', A_LE14): bits[2],
             ('O', A_STRIKE): bits[3], ('O', A_WORK): bits[4]}
        return LEAFVAL[dt_eval(t, lambda at: (bits[5] if at[0] == 'E' else d[at]))]

    def triple(self, b, x, y):
        """The executable encounter: dict with actions, exec values and costs of every check read."""
        act, bex, bcost, code, pc = self.boss_exec(b, x, y)
        ideal, cv = self.worker_row(x, y, bex)
        bc = [c if c is not None else self.V + TO_CHARGE for c in bcost]
        wex, wcost = [], []
        for k in range(4):
            c = cv[k]
            tot = c[0] + sum(c[i + 1] * bc[i] for i in range(3))
            if ideal[k] == 'TO' or tot > self.V + VPLUS:
                wex.append('TO'); wcost.append(tot if ideal[k] != 'TO' else None)
            else:
                wex.append(ideal[k]); wcost.append(tot)
        rel = self.reg[x].sp == self.reg[y].sp
        eqv = rel and 'EQ' in self.live
        bT = [v == 'T' for v in bex]
        a1 = self.worker_act(x, (bT[0], bT[1], bT[2], wex[3] == 'T', wex[2] == 'T', eqv))
        a2 = self.worker_act(y, (bT[0], bT[1], bT[2], wex[1] == 'T', wex[0] == 'T', eqv))
        # play paths: calls made and identity atoms evaluated, for the play's step count; a call is charged its
        # required cost if it returns, else the cap's charge
        bchg = tuple(self.V + TO_CHARGE if v == 'TO' else c for v, c in zip(bex, bcost))
        wchg = tuple(self.V + TO_CHARGE if v == 'TO' else c for v, c in zip(wex, wcost))
        CH = lambda c: c
        pb = self.reg[b]; tb = self.g.roles['B']['dts'][pb.tk]
        idvb = self.ae.idv_boss(code)
        pvals = dict(zip(PROBE_ATOMS, code[:8]))
        bcalls, bnid = [], 0
        node = tb
        while isinstance(node, tuple):
            a = node[0]
            if a[0] == 'E':
                bnid += 1; node = node[1] if idvb(a[1]) else node[2]
            else:
                bcalls.append(pc[PROBE_ATOMS.index(a)]); node = node[1] if pvals[a] == 'T' else node[2]
        wplays = []
        for jj, pid, ocx, ocy in ((1, x, 2, 3), (2, y, 0, 1)):
            tw = self.g.roles['W']['dts'][self.reg[pid].tk]
            calls, nid = [], 0
            node = tw
            while isinstance(node, tuple):
                a = node[0]
                if a[0] == 'E':
                    nid += 1; node = node[1] if eqv else node[2]
                elif a[0] == 'B':
                    i = BOSS_Q.index(a[1]); calls.append(bchg[i]); node = node[1] if bex[i] == 'T' else node[2]
                else:
                    i = ocx if a[1] == A_WORK else ocy
                    calls.append(wchg[i]); node = node[1] if wex[i] == 'T' else node[2]
            wplays.append(self.play_steps('W', len(calls), nid, calls))
        bsteps = self.play_steps('B', len(bcalls), bnid, bcalls)
        # the ideal play of the same triple (every check at its ideal value, no caps) and the timeout flag
        pr_ideal = self._probe_ideal.get((x, y))
        _, ideal_b, _ = self.boss_row(b, pr_ideal + code[8:]) if pr_ideal is not None else (None, None, None)
        todiff = any(v == 'TO' for v in code[:8]) or any(e == 'TO' and i != 'TO' for e, i in zip(bex, ideal_b or bex)) \
            or any(e == 'TO' and i != 'TO' for e, i in zip(wex, ideal))
        iact = self.boss_row(b, pr_ideal + code[8:])[0] if pr_ideal is not None else act
        ib = tuple(ideal_b) if ideal_b is not None else bex
        iw, _ = self.worker_row(x, y, ib)
        ibT = [v == 'T' for v in ib]
        ia1 = self.worker_act(x, (ibT[0], ibT[1], ibT[2], iw[3] == 'T', iw[2] == 'T', eqv))
        ia2 = self.worker_act(y, (ibT[0], ibT[1], ibT[2], iw[1] == 'T', iw[0] == 'T', eqv))
        return dict(boss=act, a1=a1, a2=a2, bex=bex, bcost=tuple(bcost), wex=tuple(wex), wcost=tuple(wcost),
                    bchg=bchg, wchg=wchg, code=code, pcost=pc, rel=rel, steps=(bsteps, wplays[0], wplays[1]),
                    ideal=(iact, ia1, ia2), todiff=bool(todiff))

    def productions(self, b, x, y, tr=None, gate=True):
        """S-nonself_3 after the play of (b, x, y): [(pid, new pid, record)] for the three participants."""
        tr = tr or self.triple(b, x, y)
        out = []
        att = self.prod_boss(b, tr['code'])
        nb, rec = self.produce(b, att, list(tr['pcost']), tr['steps'][0])
        out.append((b, nb, rec))
        for jj, pid, oc, od in ((1, x, 2, 3), (2, y, 0, 1)):
            if tr['rel'] and gate:
                out.append((pid, pid, [('refused',)])); continue
            oex = (tr['wex'][oc], tr['wex'][od])
            att = self.prod_worker(pid, jj, tr['bex'], oex, bool(tr['rel']))
            cc = list(tr['bchg']) + [tr['wchg'][oc], tr['wchg'][od]]
            np_, rec = self.produce(pid, att, cc, tr['steps'][jj])
            out.append((pid, np_, rec))
        return out

    # ---- production contexts (S-nonself_3, notes §1.2)
    def prod_boss(self, b, code):
        """Attempts of boss b at probe code: [(set index, script index | None, own steps, probe call indices)]."""
        b = self.canon(b)
        pi, ii = self.boss_reads(b)
        key = ('B', b, tuple(code[i] for i in pi), tuple(code[i] for i in ii))
        r = self._prod.get(key)
        if r is not None: return r
        pr = self.reg[b]
        t = self.g.roles['B']['dts'][pr.tk]
        idv = self.ae.idv_boss(code)
        vals = dict(zip(PROBE_ATOMS, code[:8]))
        ik = ident_key('B', t, idv)
        tab, dcl = self.cm.ft_table('B', pr.sp, 0, ik)
        dlist = (pr.dc[0] - dcl[0], pr.dc[2] - dcl[2])
        _, per = self.g.hlist('B', pr.tk)
        out = []
        for si, A in enumerate(BOSS_Q):
            if pr.inv[si]: continue
            log = []
            sc, calls = sym_prod3(t, 'B', A, idv, lambda at: vals[at], log)
            base, f = prod_features(log, tab, dlist, A, 'B')
            own = prod_steps('B', base, f, sc is not None)
            idx = per[A].index(sc) if sc is not None else None
            out.append((si, idx, own, tuple(PROBE_ATOMS.index(a) for a, v in calls)))
        self._prod[key] = out
        return out

    def prod_worker(self, x, j, bex, oex, rel):
        """Attempts of worker x in slot j: bex the boss boxes' exec values, oex the other worker's exec cert values
        ([C], [D]).  [(set index, script index | None, own steps, call ids)] with call ids 0..2 boss boxes, 3 the
        other's [C], 4 the other's [D]."""
        x = self.canon(x)
        key = ('W', x, j, bex, oex, rel)
        r = self._prod.get(key)
        if r is not None: return r
        pr = self.reg[x]
        t = self.g.roles['W']['dts'][pr.tk]
        eqv = rel and 'EQ' in self.live
        idv = lambda nm: eqv if nm == 'EQ' else False
        ik = ident_key('W', t, idv)
        tab, dcl = self.cm.ft_table('W', pr.sp, j, ik)
        dlist = (pr.dc[0] - dcl[0], pr.dc[2] - dcl[2])
        _, per = self.g.hlist('W', pr.tk)

        def bv(at):
            if at[0] == 'B': return bex[BOSS_Q.index(at[1])]
            return oex[0] if at[1] == A_WORK else oex[1]

        def cid(at):
            if at[0] == 'B': return BOSS_Q.index(at[1])
            return 3 if at[1] == A_WORK else 4
        out = []
        for si, A in enumerate(WORKER_Q):
            if pr.inv[si]: continue
            log = []
            sc, calls = sym_prod3(t, 'W', A, idv, bv, log)
            base, f = prod_features(log, tab, dlist, A, 'W')
            own = prod_steps('W', base, f, sc is not None)
            idx = per[A].index(sc) if sc is not None else None
            out.append((si, idx, own, tuple(cid(a) for a, v in calls)))
        self._prod[key] = out
        return out

    def produce(self, pid, attempts, call_costs, play_steps, refused=False):
        """Apply S-nonself_3 production after a play: returns (new pid, record) where record lists per attempt
        (set index, outcome 'found'|'none'|'capTO'|'fuelTO', required steps, charged steps).  An attempt's charged
        steps are PROD3's own steps (the PROD3 call included: PROD_W) plus its nested checks; it returns iff its PCORE3
        total (charged - PROD_W) is <= P + VPLUS; a cap timeout charges P + VPLUS + PROD_W."""
        pr = self.reg[pid]
        if refused:
            return pid, [('refused',)]
        rem = self.K - play_steps
        inv = list(pr.inv)
        rec = []
        for si, idx, own, calls in attempts:
            req = own + sum(call_costs[c] for c in calls)
            if rem <= 0:
                rec.append((si, 'fuelTO', req, 0)); continue
            if req - PROD_W > self.P + VPLUS:
                charged = self.P + VPLUS + PROD_W
                if charged > rem:
                    rec.append((si, 'fuelTO', req, rem)); rem = 0; continue
                rem -= charged
                rec.append((si, 'capTO', req, charged)); continue
            if req > rem:
                rec.append((si, 'fuelTO', req, rem)); rem = 0; continue
            rem -= req
            if idx is None:
                rec.append((si, 'none', req, req)); continue
            inv[si] = (idx,)
            rec.append((si, 'found', req, req))
        newpid = self.reg.get(pr.role, pr.sp, tuple(inv))
        return newpid, rec

    def play_steps(self, role, ncall, nid, call_costs):
        c = COSTC['PLAY'][role]
        return int(round(c[0] + c[1] * ncall + c[2] * nid)) + sum(call_costs)


# ----------------------------------------------------------------------------------------------------------------
# 12. Validation decision tables (VT) for the numba worker-pair evaluator (sog_full_kern.eval_pair)
# ----------------------------------------------------------------------------------------------------------------
VT_ATOM = {('B', A_GE14): 0, ('B', A_EQ12): 1, ('B', A_LE14): 2, ('O', A_WORK): 3, ('O', A_STRIKE): 4}


def build_vt(ev, cpid, slot, A, eqval):
    """The decision trie of one validation (vone4) of worker class cpid in slot (1|2) for set A with EQ value eqval:
    nodes as tuples ('q', atom code, {0: node, 1: node}) | ('r', ok, used atom codes, own steps).  Built by running the
    symbolic traversal under every T/F assignment of the run tree's box atoms."""
    pr = ev.reg[cpid]
    t = ev.g.roles['W']['dts'][pr.tk]
    idv = lambda nm: eqval if nm == 'EQ' else False
    ik = ident_key('W', t, idv)
    tab, dcl = ev.cm.ft_table('W', pr.sp, slot, ik)
    dlist = (pr.dc[0] - dcl[0], pr.dc[2] - dcl[2])
    ats = [a for a in dt_atoms(t) if a[0] != 'E']
    root = None
    for bits in itertools.product((True, False), repeat=len(ats)):
        val = dict(zip(ats, bits))
        seq = []

        def boxval(atom):
            v = 'T' if val[atom] else 'F'
            seq.append((VT_ATOM[atom], 1 if val[atom] else 0))
            return v
        steps = 0; att = 0; used = None; scanned = len(pr.entries)
        for i, (A2, sc) in enumerate(pr.entries):
            if A2 != A: continue
            att += 1
            r, calls, nodes_ = sym_check_trace(t, 'W', A, sc, idv, boxval)
            for rec in nodes_:
                steps += node_steps(t, 'W', A, rec, tab, dlist)
            if r is not None:
                used = list(r); scanned = i + 1; break
        steps += vone_steps('W', pr.lc, scanned, att, used is not None, len(pr.entries))
        leaf = ('r', used is not None, tuple(VT_ATOM[a] for a in (used or ())), steps)
        if not seq:
            if root is None: root = leaf
            continue
        if root is None: root = ('q', seq[0][0], {})
        nd = root
        for q, (a, v) in enumerate(seq):
            assert nd[0] == 'q' and nd[1] == a
            if q + 1 < len(seq):
                nx = nd[2].get(v)
                if nx is None:
                    nx = ('q', seq[q + 1][0], {}); nd[2][v] = nx
                nd = nx
            else:
                if v in nd[2]: assert nd[2][v] == leaf, (nd[2][v], leaf)
                nd[2][v] = leaf
    return root


class VTStore:
    """Flattened validation decision tables for the numba pair evaluator, per worker class id (local to a Run or a
    test): VTR[c, slot0, A, eq] -> root node; node arrays VK (0 query, 1 leaf), VA, VC[n, 2], VOK, VSTEPS, VUSED[n, 4],
    VNU; READS_EQ[c]."""

    def __init__(self, cap_cls=1024, cap_nodes=65536):
        self.VTR = np.full((cap_cls, 2, 2, 2), -1, np.int64)
        self.READS_EQ = np.zeros(cap_cls, np.int64)
        self.VK = np.zeros(cap_nodes, np.int64); self.VA = np.zeros(cap_nodes, np.int64)
        self.VC = np.full((cap_nodes, 2), -1, np.int64); self.VOK = np.zeros(cap_nodes, np.int64)
        self.VSTEPS = np.zeros(cap_nodes, np.int64); self.VUSED = np.full((cap_nodes, 4), -1, np.int64)
        self.VNU = np.zeros(cap_nodes, np.int64)
        self.n = 0

    def _grow_nodes(self, need):
        if need <= len(self.VK): return
        cap = max(need, 2 * len(self.VK))
        for nm, fill in (('VK', 0), ('VA', 0), ('VC', -1), ('VOK', 0), ('VSTEPS', 0), ('VUSED', -1), ('VNU', 0)):
            a = getattr(self, nm)
            b = np.full((cap,) + a.shape[1:], fill, a.dtype)
            b[:len(a)] = a
            setattr(self, nm, b)

    def _grow_cls(self, c):
        if c < len(self.READS_EQ): return
        cap = max(c + 1, 2 * len(self.READS_EQ))
        b = np.full((cap, 2, 2, 2), -1, np.int64); b[:len(self.VTR)] = self.VTR; self.VTR = b
        b = np.zeros(cap, np.int64); b[:len(self.READS_EQ)] = self.READS_EQ; self.READS_EQ = b

    def _flatten(self, nd):
        i = self.n
        self.n += 1
        self._grow_nodes(self.n)
        if nd[0] == 'r':
            self.VK[i] = 1
            self.VOK[i] = 1 if nd[1] else 0
            self.VNU[i] = len(nd[2])
            for q, a in enumerate(nd[2][:4]):
                self.VUSED[i, q] = a
            assert len(nd[2]) <= 4
            self.VSTEPS[i] = nd[3]
            return i
        self.VK[i] = 0
        self.VA[i] = nd[1]
        for v in (0, 1):
            ch = nd[2].get(v)
            if ch is not None:
                self.VC[i, v] = self._flatten(ch)
        return i

    def add_class(self, ev, c, cpid):
        self._grow_cls(c)
        tg, re = ev.deps(cpid)
        self.READS_EQ[c] = 1 if re else 0
        for s0 in (0, 1):
            for ai, A in enumerate(WORKER_Q):
                for eq in ((0, 1) if re else (0,)):
                    root = build_vt(ev, cpid, s0 + 1, A, bool(eq))
                    self.VTR[c, s0, ai, eq] = self._flatten(root)

    def arrays(self):
        return (self.READS_EQ, self.VTR, self.VK, self.VA, self.VC, self.VOK, self.VSTEPS, self.VUSED, self.VNU)


def bk_array():
    b = COSTC['BK']
    return np.array([b['F0'], b['T0'], b['F1'], b['hit'], b['ins'], b['ins_cnt'], b['ins_len'], b['fail'],
                     b['fail_cnt'], b['cap']], np.int64)
