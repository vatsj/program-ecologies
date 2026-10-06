"""The realizable language, milestone 4: certificates as code (specs/2026-10-06-certificates-as-code.md;
notes/certificates-as-code.md; frozen design in predictions/2026-10-06-certificates-as-code.md).

Built on src/lt_code.py (imported, not modified): the same language L_T^code, evaluator, cache and regress lemma.
This module appends to milestone 3's library (indices of milestone 3 unchanged) the check wrappers CHK_x, the check
cores CC_x, the check-aware self-interpreter `cstep`, the script checker `cchk` and the validator `vone`, all
L_T^code terms in the same s-expression syntax; then installs the extended library into lt_code's evaluator.

Parts:
  1. the library extension (K_T^cert in the checker term);
  2. programs: carriers, fakers, controls, held-out sources, milestone 3's searchers;
  3. the host side, independent of the checker term: decomposition with call states, formulas, the host check
     emulation (replay checker), the frozen production tactic;
  4. the catalogue builder (two-pass production) and play / check helpers.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L

N, P = L.N, L.P
C_, D_, T_, F_, TO_ = L.C_, L.D_, L.T_, L.F_, L.TO_

# ----------------------------------------------------------------------------------------------------------------
# 1. The library extension
# ----------------------------------------------------------------------------------------------------------------
# Modes: 0 sound, 5 sound copy (another library entry), 1 naive (unguarded pair), 2 self-only, 3 none, 4 sloppy.
# Formulas: (0 . 0) top; (1 . 0) bot; (6 . (conf . (f . (a . m)))) atom; (8 . (n . arg)) check box,
# arg = (V . (t . (m . (a . K)))).  Script node: (rule . (j . prems)); rules 0 Ax, 1 Run, 2 RunNeg, 3 Hyp, 25 ChkR,
# 26 EvR*.  cchk returns 0 (invalid), 1 (valid), 2 (valid and closed S != R).
CERT_SRC = r"""
; ---------------- check wrappers (each a distinct library entry) and cores ----------------
(def CHKS (arg) (if (eq (capk (fst arg) CCS arg) T) T F))
(def CHKS2 (arg) (if (eq (capk (fst arg) CCS2 arg) T) T F))
(def CHKN (arg) (if (eq (capk (fst arg) CCN arg) T) T F))
(def CHKO (arg) (if (eq (capk (fst arg) CCO arg) T) T F))
(def CHKX (arg) (if (eq (capk (fst arg) CCX arg) T) T F))
(def CHKL (arg) (if (eq (capk (fst arg) CCL arg) T) T F))
(def CCS (arg) (ccore 0 arg))
(def CCS2 (arg) (ccore 5 arg))
(def CCN (arg) (ccore 1 arg))
(def CCO (arg) (ccore 2 arg))
(def CCX (arg) (ccore 3 arg))
(def CCL (arg) (ccore 4 arg))
(def wrapid (x) (cond ((eq x 0) ID_CHKS) ((eq x 5) ID_CHKS2) ((eq x 1) ID_CHKN) ((eq x 2) ID_CHKO) ((eq x 3) ID_CHKX) (else ID_CHKL)))
(def iswrap (n) (or (eq n ID_CHKS) (or (eq n ID_CHKS2) (or (eq n ID_CHKN) (or (eq n ID_CHKO) (or (eq n ID_CHKX) (eq n ID_CHKL)))))))
(def callcheck (n ad)
  (cond ((eq n ID_CHKS) (capk (fst ad) CCS ad))
        ((eq n ID_CHKS2) (capk (fst ad) CCS2 ad))
        ((eq n ID_CHKN) (capk (fst ad) CCN ad))
        ((eq n ID_CHKO) (capk (fst ad) CCO ad))
        ((eq n ID_CHKX) (capk (fst ad) CCX ad))
        (else (capk (fst ad) CCL ad))))
(def swaparg (arg) (let ((r (snd arg)) (r2 (snd r))) (pair (fst arg) (pair (fst r2) (pair (fst r) (snd r2))))))

; ---------------- the check ----------------
(def ccore (x arg)
  (let ((n (wrapid x)) (R (pair 8 (pair n arg))) (sa (swaparg arg)) (S (pair 8 (pair n sa)))
        (r1 (vone x arg R S)))
    (if (fst r1)
        (if (and (or (eq x 0) (eq x 5)) (snd r1)) (fst (vone x sa S R)) T)
        F)))
(def vone (x arg Rb Sb)
  (let ((r (snd arg)) (t (fst r)) (m (fst (snd r))) (a (fst (snd (snd r)))) (K (snd (snd (snd r))))
        (cl (getcerts t)))
    (if (eq cl NONE) NOPE
      (if (eq x 4) (if (hasentry cl a) YEP NOPE)
        (tryents (pair x (pair Rb (pair Sb (fst arg)))) cl a (mkatom (mkconf t m) K a 0))))))
(def mkconf (t m) (pair 2 (pair (pair 2 (pair t (pair (pair 10 t) 0))) (pair (pair 10 m) 0))))
(def getcerts (t)
  (if (eq (fst t) 1)
    (let ((b1 (snd t)))
      (if (eq (fst b1) 1)
        (let ((b2 (snd b1)))
          (if (eq (fst b2) 2)
            (let ((l (snd b2)))
              (if (eq (fst (fst l)) 1) (full (fst (snd l))) NONE))
            NONE))
        NONE))
    NONE))
(def hasentry (cl a) (if (eq cl 0) F (if (eq (fst (fst cl)) a) T (hasentry (snd cl) a))))
(def tryents (cx cl a psi)
  (if (eq cl 0) NOPE
    (let ((e (fst cl)))
      (if (eq (fst e) a)
          (let ((v (cchk cx (snd e) 0 (pair psi 0))))
            (if (lt 0 v) (pair T (if (eq v 2) T F)) (tryents cx (snd cl) a psi)))
          (tryents cx (snd cl) a psi)))))

; ---------------- the script checker ----------------
(def fnth (l j) (if (eq l 0) NONE (if (eq j 0) (fst l) (fnth (snd l) (sub j 1)))))
(def cchk (cx node L R)
  (let ((rule (fst node)) (j (fst (snd node))) (ps (snd (snd node))))
    (cond ((eq rule 0) (if (caxiom L R) 1 0))
          ((eq rule 3) (chyp cx (fnth R j)))
          ((eq rule 1) (crun cx (fnth R j) 1))
          ((eq rule 2) (crun cx (fnth L j) 0))
          ((eq rule 26) (cev cx ps L R (fnth R j)))
          ((eq rule 25) (cchkr cx ps L R (fnth R j)))
          (else 0))))
(def ccommon (L R) (if (eq L 0) F (let ((x (fst L))) (if (and (or (eq (fst x) 6) (eq (fst x) 8)) (fmem x R)) T (ccommon (snd L) R)))))
(def caxiom (L R) (or (fhaskind L 1) (or (fhaskind R 0) (ccommon L R))))
(def chyp (cx b)
  (let ((x (fst cx)))
    (cond ((eq b NONE) 0)
          ((eq x 3) 0)
          ((eq b (fst (snd cx))) 1)
          ((eq x 2) 0)
          ((eq b (fst (snd (snd cx)))) 2)
          (else 0))))
(def crun (cx b want)
  (if (eq b NONE) 0
    (if (not (eq (fst b) 8)) 0
      (if (or (eq b (fst (snd cx))) (eq b (fst (snd (snd cx))))) 0
        (let ((p (snd b)) (n (fst p)) (ad (snd p)))
          (if (le (snd (snd (snd cx))) (fst ad))
              (let ((v (callcheck n ad)))
                (if (eq want 1) (if (eq v T) 1 0) (if (eq v T) 0 1)))
              0))))))
(def cev (cx ps L R x)
  (if (or (eq x NONE) (not (eq (fst x) 6))) 0
    (let ((p (snd x)) (conf (fst p)) (f (fst (snd p))) (a (fst (snd (snd p)))) (m (snd (snd (snd p))))
          (r (cstep conf)))
      (if (and (lt 0 f) (eq (fst r) 2))
          (cchk cx (fst ps) L (fadd (evfrom r f a m) (fdel x R)))
          0))))
(def evfrom (r f a m)
  (let ((d (snd r)))
    (if (and (eq m 1) (eq (snd d) 1)) BOTF (evstar (fst d) (sub f 1) a m))))
(def evstar (conf f a m)
  (let ((r (cstep conf)) (rk (fst r)))
    (cond ((eq rk 0) (if (eq (full conf) a) TOPF BOTF))
          ((eq rk 1) BOTF)
          ((eq f 0) BOTF)
          ((eq rk 2) (evfrom r f a m))
          (else (mkatom conf f a m)))))
(def creading (conf f a)
  (let ((r (cstep conf)) (rk (fst r)))
    (cond ((eq rk 0) (if (eq (full conf) a) TOPF BOTF))
          ((eq rk 1) BOTF)
          ((eq f 0) BOTF)
          (else (mkatom conf f a 1)))))
(def cargok (arg) (and (eq (fst arg) 5) (isnat (fst (snd arg)))))
(def chkstate (conf f a)
  (if (eq f 0) 0
    (let ((r (cstep conf)))
      (if (eq (fst r) 3)
          (let ((s (snd r)) (n (fst s)) (arg (fst (snd s))) (frames (snd (snd s))))
            (if (and (iswrap n) (cargok arg))
                (let ((ad (full arg)) (u (add (fst ad) 6)))
                  (if (and (le u f) (allfit frames u))
                      (pair (pair 8 (pair n ad))
                            (pair (creading (plug frames TENC u) (sub f u) a)
                                  (creading (plug frames FENC u) (sub f u) a)))
                      0))
                0))
          0))))
(def cchkr (cx ps L R x)
  (if (or (eq x NONE) (not (eq (fst x) 6))) 0
    (let ((p (snd x)) (s (chkstate (fst p) (fst (snd p)) (fst (snd (snd p))))))
      (if (eq s 0) 0
        (let ((B (fst s)) (Rx (fdel x R))
              (v1 (cchk cx (fst ps) (fadd B L) (fadd (fst (snd s)) Rx))))
          (if (eq v1 0) 0
            (let ((v2 (cchk cx (fst (snd ps)) L (fadd B (fadd (snd (snd s)) Rx)))))
              (if (eq v2 0) 0 (if (lt v1 v2) v2 v1)))))))))

; ---------------- the check-aware self-interpreter (milestone 3's step, check wrappers as call states) ----------------
(def cstep (e)
  (let ((t (fst e)))
    (cond ((valtag t) RVAL)
          ((eq t 5) (cstepl t (snd e) 0))
          ((eq t 0) RSTUCK)
          ((eq t 8) (cstepif (snd e)))
          ((eq t 16) (cstepsim (snd e)))
          ((eq t 13) (cstepop (snd e)))
          (else (cstepl t (snd e) 1)))))
(def cstepl (t l c)
  (let ((i (firstnv l 0)))
    (if (eq i NONE)
        (if (eq c 0) RVAL (if (eq t 2) (ccontractapp (fst l) (fst (snd l))) (contract t l)))
        (wrapr (cstep (nth l i)) (pair 0 (pair t (pair i l)))))))
(def cstepif (p)
  (let ((c (fst p)))
    (if (isval c)
        (let ((cv (full c)))
          (cond ((eq cv T) (det (fst (snd p)) 0))
                ((eq cv F) (det (fst (snd (snd p))) 0))
                (else RSTUCK)))
        (wrapr (cstep c) (pair 2 (pair (fst (snd p)) (fst (snd (snd p)))))))))
(def cstepsim (p)
  (let ((k (fst p)) (inner (snd p)))
    (if (isval inner) (det inner 0)
      (if (eq k 0) (det TOENC 1)
        (let ((r (cstep inner)) (rk (fst r)))
          (cond ((eq rk 1) (det TOENC 1))
                ((eq rk 2) (let ((q (snd r))) (det (pair 16 (pair (sub k 1) (fst q))) (snd q))))
                (else (let ((q (snd r))) (pair 3 (pair (fst q) (pair (fst (snd q)) (pair (pair 3 k) (snd (snd q))))))))))))))
(def cstepop (p)
  (let ((l (snd p)) (i (firstnv l 0)))
    (if (eq i NONE) (contractop (fst p) l)
        (wrapr (cstep (nth l i)) (pair 1 (pair (fst p) (pair i l)))))))
(def ccontractapp (f a)
  (let ((tf (fst f)))
    (cond ((eq tf 1) (det (subst (snd f) a 0) 0))
          ((eq tf 9) (det (mkapp (subst (snd f) f 0) a) 0))
          ((eq tf 12) (let ((n (snd f)))
                        (if (or (lt n 3) (iswrap n)) (pair 3 (pair n (pair a 0)))
                            (if (lt n NLIB) (det (subst (snd (libsrc n)) a 0) 0) RSTUCK))))
          (else RSTUCK))))
"""

WRAP_NAMES = ['CHKS', 'CHKS2', 'CHKN', 'CHKO', 'CHKX', 'CHKL']
CORE_NAMES = {'CCS': 0, 'CCS2': 5, 'CCN': 1, 'CCO': 2, 'CCX': 3, 'CCL': 4}
MODE_WRAP = {0: 'CHKS', 5: 'CHKS2', 1: 'CHKN', 2: 'CHKO', 3: 'CHKX', 4: 'CHKL'}
MODE_CORE = {v: k for k, v in CORE_NAMES.items()}
CERT_CONSTS = {'NOPE': ['pair', 'F', 'F'], 'YEP': ['pair', 'T', 'F']}
ID = {}
WRAPS = set()
CC_MODE = {}            # lib index of a check core -> mode
WRAP_MODE = {}          # lib index of a wrapper -> mode
CORE_ID_BASE = 10       # core ids registered in lt_code.CORE_LIBS: 10 + mode


def build_library():
    comp = L.SxCompiler()
    for k, v in L.LIB_CONSTS.items(): comp.consts[k] = v
    for k, v in CERT_CONSTS.items(): comp.consts[k] = v
    comp.load(L.LIBRARY_SRC)
    comp.load(CERT_SRC)
    for nm in WRAP_NAMES: comp.consts['ID_' + nm] = comp.order.index(nm)
    comp.consts['NLIB'] = len(comp.order)
    terms = comp.build(0)
    L.LIB[:] = terms
    L.LIBNAME.clear(); L.LIBNAME.update({i: n for i, n in enumerate(comp.order)})
    L.LIBIDX.clear(); L.LIBIDX.update(comp.index)
    L.SEARCH_LIBS.clear(); L.SEARCH_LIBS.update({L.LIBIDX['SEARCH%d' % i]: i for i in range(3)})
    L.CORE_LIBS.clear(); L.CORE_LIBS.update({L.LIBIDX['CORE%d' % i]: i for i in range(3)})
    for nm, mode in CORE_NAMES.items(): L.CORE_LIBS[L.LIBIDX[nm]] = CORE_ID_BASE + mode
    assert [L.LIBIDX['SEARCH%d' % i] for i in range(3)] == [0, 1, 2]
    L.LIBCODE[:] = [L.compile_term(t[1]) for t in terms]
    L._compiled.clear()
    L.LIBCODE[:] = [L.compile_term(t[1]) for t in terms]
    L.CACHE.clear()
    ID.clear(); ID.update({nm: L.LIBIDX[nm] for nm in WRAP_NAMES})
    WRAPS.clear(); WRAPS.update(ID.values())
    CC_MODE.clear(); CC_MODE.update({L.LIBIDX[nm]: mode for nm, mode in CORE_NAMES.items()})
    WRAP_MODE.clear(); WRAP_MODE.update({L.LIBIDX[MODE_WRAP[m]]: m for m in MODE_WRAP})
    return comp


_COMP = build_library()
NLIB = len(L.LIB)


# ----------------------------------------------------------------------------------------------------------------
# 2. Programs
# ----------------------------------------------------------------------------------------------------------------
# Scripts in Python: node = (rule, (j, prems)), prems a cons list (p1, (p2, 0)) or 0.  Cert lists likewise:
# ((a, script), (...)) with a in {'C', 'D'}.
AX, RUN, RUNNEG, HYP, CHKR, EVS = 0, 1, 2, 3, 25, 26
RULE_NAME = {AX: 'Ax', RUN: 'Run', RUNNEG: 'RunNeg', HYP: 'Hyp', CHKR: 'ChkR', EVS: 'EvR*'}


def cons(xs):
    out = 0
    for x in reversed(xs): out = (x, out)
    return out


def uncons(l):
    out = []
    while l != 0:
        out.append(l[0]); l = l[1]
    return out


def node(rule, j, *prems): return (rule, (j, cons(list(prems))))


def data_term(d):
    """Python data (ints, constructor strings, pairs) -> an L_T value term."""
    if isinstance(d, bool): raise ValueError(d)
    if isinstance(d, int): return ('nat', d)
    if isinstance(d, str): return ('con', d)
    return ('pair', data_term(d[0]), data_term(d[1]))


def script_nodes(s):
    return 1 + sum(script_nodes(p) for p in uncons(s[1][1]))


def show_script(s):
    r, (j, ps) = s
    ps = uncons(ps)
    nm = RULE_NAME.get(r, str(r))
    if j: nm += '@%d' % j
    if not ps: return nm
    if r == EVS: return nm + '; ' + show_script(ps[0])
    return nm + '[' + ' · '.join(show_script(p) for p in ps) + ']'


ME3, THEM3 = ('v', 2), ('v', 1)        # inside the let body: certs = v0, them = v1, me = v2


def ARG(V, x, y, a, K): return P(N(V), P(x, P(y, P(('con', a), N(K)))))


def CALL(mode, V, x, y, a, K): return ('app', ('lib', ID[MODE_WRAP[mode]]), ARG(V, x, y, a, K))


def carrier(body, certs):
    """λme.λthem.(λcerts. body) CERTS."""
    return L.L2(('app', ('lam', body), data_term(certs)))


QD = ('quote', L.PROG_D)


def body_CB(mode, V, K): return ('if', CALL(mode, V, THEM3, ME3, 'C', K), C_, D_)
def body_CB1(mode, V, K): return ('if', CALL(mode, V, THEM3, ME3, 'C', K), ('if', CALL(mode, V, ME3, THEM3, 'C', K), C_, D_), D_)
def body_CBP(mode, V, K): return ('if', CALL(mode, V, THEM3, ME3, 'C', K), ('if', CALL(mode, V, THEM3, QD, 'D', K), C_, D_), D_)
def body_CBlet(mode, V, K):
    return ('app', ('lam', ('if', ('app', ('lib', ID[MODE_WRAP[mode]]), ('v', 0)), C_, D_)), ARG(V, THEM3, ME3, 'C', K))
def body_CBwrap(mode, V, K): return ('app', ('lam', ('v', 0)), body_CB(mode, V, K))
def body_CBdef(mode, V, K): return ('if', CALL(mode, V, THEM3, ME3, 'C', K), D_, C_)
def body_LobC(mode, V, K): return ('if', CALL(mode, V, ME3, THEM3, 'C', K), C_, D_)
def body_C(mode, V, K): return C_
def body_D(mode, V, K): return D_
def body_SFc(k): return ('if', ('eq', ('run', N(k), THEM3, ME3), C_), C_, D_)
# held-out spellings
def body_CBlet2(mode, V, K):        # the fuel bound in a second let: inside λk, them = v2, me = v3
    return ('app', ('lam', ('if', ('app', ('lib', ID[MODE_WRAP[mode]]),
                                   P(N(V), P(('v', 2), P(('v', 3), P(C_, ('v', 0)))))), C_, D_)), N(K))
def body_CBw2(mode, V, K):          # a different checker wrapping: (λf. if f(arg) then C else D) (lib CHK)
    return ('app', ('lam', ('if', ('app', ('v', 0), ARG(V, ('v', 2), ('v', 3), 'C', K)), C_, D_)),
            ('lib', ID[MODE_WRAP[mode]]))
def body_CB1h(mode, V, K):          # FB1-shaped respelled: the first argument let-bound
    lib = ('lib', ID[MODE_WRAP[mode]])
    return ('app', ('lam', ('if', ('app', lib, ('v', 0)), ('if', ('app', lib, ARG(V, ('v', 3), ('v', 2), 'C', K)), C_, D_), D_)),
            ARG(V, THEM3, ME3, 'C', K))
def body_CB1r(mode, V, K):          # FB1-shaped, the two calls in the other order
    return ('if', CALL(mode, V, ME3, THEM3, 'C', K), ('if', CALL(mode, V, THEM3, ME3, 'C', K), C_, D_), D_)
def body_CBPh(mode, V, K):          # PB-shaped respelled: the D quote let-bound (inside λd: them = v2, me = v3)
    return ('app', ('lam', ('if', CALL(mode, V, ('v', 2), ('v', 3), 'C', K),
                            ('if', CALL(mode, V, ('v', 2), ('v', 0), 'D', K), C_, D_), D_)), QD)
def body_CBPr(mode, V, K):          # PB-shaped, the D check first
    return ('if', CALL(mode, V, THEM3, QD, 'D', K), ('if', CALL(mode, V, THEM3, ME3, 'C', K), C_, D_), D_)


# ----------------------------------------------------------------------------------------------------------------
# 3. Host side (independent of the checker term): decomposition, formulas, check emulation, production
# ----------------------------------------------------------------------------------------------------------------
TOPH, BOTH = ('top',), ('bot',)


def hdecompose(t):
    """lt_code.decompose with call states: an application of lib n with n < 3 (search) or n a check wrapper, both
    sides values, is kind 'call' with payload (n, argument value)."""
    ctx = []
    while True:
        tag = t[0]
        if tag in L.VALUE_TAGS: return ctx, 'value', t, 0
        if tag == 'v': return ctx, 'stuck', None, 0
        if tag == 'sim':
            k, inner = t[1], t[2]
            if L.is_value(inner): return ctx, 'det', inner, 0
            if k == 0: return ctx, 'det', TO_, 1
            ictx, ikind, ipay, ito = hdecompose(inner)
            if ikind == 'stuck': return ctx, 'det', TO_, 1
            ctx.append(('sim', k)); ctx.extend(ictx)
            return ctx, ikind, ipay, ito
        if tag == 'if':
            if not L.is_value(t[1]):
                ctx.append(('hole', t, 1)); t = t[1]; continue
            out = L.contract(t)
            return (ctx, 'stuck', None, 0) if out is L.STUCK else (ctx, 'det', out, 0)
        start = 2 if tag == 'op' else 1
        for i in range(start, len(t)):
            if not L.is_value(t[i]):
                ctx.append(('hole', t, i)); t = t[i]; break
        else:
            if tag == 'pair': return ctx, 'value', t, 0
            if tag == 'app' and t[1][0] == 'lib' and (t[1][1] < 3 or t[1][1] in WRAPS):
                return ctx, 'call', (t[1][1], t[2]), 0
            out = L.contract(t)
            if out is L.STUCK: return ctx, 'stuck', None, 0
            return ctx, 'det', out, 0


def h_read(t, f, a, m):
    ctx, kind, pay, ito = hdecompose(t)
    if kind == 'value': return TOPH if t == ('con', a) else BOTH
    if kind == 'stuck': return BOTH
    if f == 0: return BOTH
    return ('atom', t, f, a, m)


class HostAbort(Exception):
    """The host replay exceeded its step budget or met a regress: the term's root check times out."""


HOST_STEP_COST = 20     # an interpreted step at context depth d costs the checker term >= 20 (1 + d) steps (tested)


def h_evstar(phi, budget=None):
    """EvR*: iterate deterministic steps; returns (formula, steps) or None if the first step is not deterministic.
    budget: cap / HOST_STEP_COST; the host charges 1 + (context depth) per step, a lower bound on the term's cost in
    units of HOST_STEP_COST, so exceeding the budget means the term's check would have timed out: HostAbort."""
    _, t, f, a, m = phi
    if f < 1: return None
    ctx, kind, pay, ito = hdecompose(t)
    if kind != 'det': return None
    n = 0
    w = 0
    while True:
        n += 1
        w += 1 + len(ctx)
        if budget is not None and w > budget: raise HostAbort()
        if m == 1 and ito: return BOTH, n
        t = L.plug(ctx, pay); f -= 1
        ctx, kind, pay, ito = hdecompose(t)
        if kind == 'value': return (TOPH if t == ('con', a) else BOTH), n
        if kind == 'stuck' or f == 0: return BOTH, n
        if kind != 'det': return ('atom', t, f, a, m), n


def parse_carg(v):
    """A check call's argument value -> (V, value) if it is a pair whose first component is a natural."""
    if v[0] == 'pair' and v[1][0] == 'nat': return v[1][1]
    return None


def h_chkstate(phi):
    """ChkR: (box, rhoT, rhoF) or None."""
    _, t, f, a, m = phi
    if f == 0: return None
    ctx, kind, pay, ito = hdecompose(t)
    if kind != 'call': return None
    n, v = pay
    if n not in WRAPS: return None
    V = parse_carg(v)
    if V is None: return None
    u = V + 6
    fuels = [fr[1] for fr in ctx if fr[0] == 'sim']
    if not (u <= f and all(k >= u for k in fuels)): return None
    fr = f - u
    return (('cbox', n, v), h_read(L.plug(ctx, T_, u), fr, a, 1), h_read(L.plug(ctx, F_, u), fr, a, 1))


def term_data(t):
    """An L_T value term (pairs, nats, constructors) -> Python data."""
    if t[0] == 'nat': return t[1]
    if t[0] == 'con': return t[1]
    if t[0] == 'pair': return (term_data(t[1]), term_data(t[2]))
    raise ValueError('not data: %r' % (t[0],))


def h_getcerts(prog):
    """The program term (not its quote) -> its certificate list as data, or None."""
    try:
        if prog[0] == 'lam' and prog[1][0] == 'lam' and prog[1][1][0] == 'app' and prog[1][1][1][0] == 'lam':
            return term_data(prog[1][1][2])
    except Exception:
        return None
    return None


def h_argfields(v):
    """Check argument value pair(V, pair(quote t, pair(quote m, pair(con a, nat K)))) -> (V, t, m, a, K) or None."""
    try:
        V = v[1][1]; r = v[2]; t = r[1]; r2 = r[2]; m = r2[1]; r3 = r2[2]; a = r3[1]; K = r3[2]
        assert v[1][0] == 'nat' and t[0] == 'quote' and m[0] == 'quote' and a[0] == 'con' and K[0] == 'nat'
        return V, t[1], m[1], a[1], K[1]
    except Exception:
        return None


def mk_arg(V, t, m, a, K):
    return P(N(V), P(('quote', t), P(('quote', m), P(('con', a), N(K)))))


def swap_arg(v):
    V, t, m, a, K = h_argfields(v)
    return mk_arg(V, m, t, a, K)


def root_atom(t, m, a, K):
    return ('atom', L.initial(t, m), K, a, 0)


class Regress(HostAbort):
    pass


class HostCheck:
    """Independent host emulation of ccore (the replay checker): the rule table of notes §1.5 in Python, over the
    reference stepper with call states.  Nested Run/RunNeg checks are emulated recursively; a check whose key is on
    the stack raises Regress, which makes the outermost check TO (cap monotonicity: the root dies).  No fuel is
    counted: outcomes are compared with the term where the term finished."""

    def __init__(self):
        self.memo = {}
        self.stack = []
        self.maxdepth = 0
        self.log = []          # (mode, key) of every check emulated

    def check(self, n, v):
        """Value of the clean run of capk(V, CC_mode(n), v): 'T' | 'F' | 'TO' (regress)."""
        key = (n, v)
        if key in self.memo: return self.memo[key]
        if key in self.stack: raise Regress()
        self.stack.append(key)
        self.maxdepth = max(self.maxdepth, len(self.stack))
        try:
            res = self._ccore(WRAP_MODE[n], v)
        except HostAbort:
            self.stack.pop()
            if self.stack: raise
            self.memo[key] = 'TO'
            return 'TO'
        self.stack.pop()
        self.memo[key] = res
        return res

    def _ccore(self, mode, v):
        n = ID[MODE_WRAP[mode]]
        Rb = ('cbox', n, v); sv = swap_arg(v) if h_argfields(v) else None
        Sb = ('cbox', n, sv) if sv is not None else None
        ok, usesS, _ = self.vone(mode, v, Rb, Sb)
        if not ok: return 'F'
        if mode in (0, 5) and usesS:
            ok2, _, _ = self.vone(mode, sv, Sb, Rb)
            return 'T' if ok2 else 'F'
        return 'T'

    def vone(self, mode, v, Rb, Sb):
        """(ok, usesS, index of the accepted entry).  Called outside any check (stack empty), a host abort (budget or
        regress) is reported as (False, False, 'abort')."""
        if self.stack: return self._vone(mode, v, Rb, Sb)
        try:
            return self._vone(mode, v, Rb, Sb)
        except HostAbort:
            return False, False, 'abort'

    def _vone(self, mode, v, Rb, Sb):
        fs = h_argfields(v)
        if fs is None: return False, False, None
        V, t, m, a, K = fs
        cl = h_getcerts(t)
        if cl is None: return False, False, None
        ents = uncons(cl) if cl != 0 else []
        if mode == 4:
            ok = any(isinstance(e, tuple) and e[0] == a for e in ents)
            return ok, False, None
        psi = root_atom(t, m, a, K)
        for i, e in enumerate(ents):
            if not isinstance(e, tuple) or e[0] != a: continue
            r = self.cchk(mode, Rb, Sb, V, e[1], (), (psi,))
            if r: return True, r == 2, i
        return False, False, None

    def cchk(self, mode, Rb, Sb, V, nd, Lf, Rf):
        try:
            rule, (j, ps) = nd
            ps = uncons(ps)
        except Exception:
            return 0

        def at(lst, j):
            return lst[j] if isinstance(j, int) and 0 <= j < len(lst) else None
        if rule == AX:
            if BOTH in Lf or TOPH in Rf or any(x in Rf and x[0] in ('atom', 'cbox') for x in Lf): return 1
            return 0
        if rule == HYP:
            b = at(Rf, j)
            if b is None or mode == 3: return 0
            if b == Rb: return 1
            if mode == 2: return 0
            if b == Sb: return 2
            return 0
        if rule in (RUN, RUNNEG):
            b = at(Rf if rule == RUN else Lf, j)
            if b is None or b[0] != 'cbox' or b == Rb or b == Sb: return 0
            Vb = parse_carg(b[2])
            if Vb is None or Vb < V: return 0
            res = self.check(b[1], b[2])
            return 1 if (res == 'T') == (rule == RUN) else 0
        if rule == EVS:
            x = at(Rf, j)
            if x is None or x[0] != 'atom' or not ps: return 0
            s = h_evstar(x, V // HOST_STEP_COST)
            if s is None: return 0
            return self.cchk(mode, Rb, Sb, V, ps[0], Lf, fadd(s[0], fdel(x, Rf)))
        if rule == CHKR:
            x = at(Rf, j)
            if x is None or x[0] != 'atom' or len(ps) < 2: return 0
            s = h_chkstate(x)
            if s is None: return 0
            B, rT, rF = s
            Rx = fdel(x, Rf)
            v1 = self.cchk(mode, Rb, Sb, V, ps[0], fadd(B, Lf), fadd(rT, Rx))
            if not v1: return 0
            v2 = self.cchk(mode, Rb, Sb, V, ps[1], Lf, fadd(B, fadd(rF, Rx)))
            if not v2: return 0
            return max(v1, v2)
        return 0


def fadd(x, lst):
    """The library's fadd: prepend if absent (lists as Python tuples, head first)."""
    return lst if x in lst else (x,) + tuple(lst)


def fdel(x, lst):
    out = list(lst)
    if x in out: out.remove(x)
    return tuple(out)


def expanded_size(prog_t, prog_m, a, K, script):
    """Expanded size of a script on a root (EvR* counted by its steps); None if it does not replay."""
    h = HostCheck()
    tot = [0]

    def walk(nd, Lf, Rf):
        rule, (j, ps) = nd
        ps = uncons(ps)
        if rule == EVS:
            x = Rf[j]; s = h_evstar(x); tot[0] += s[1]
            walk(ps[0], Lf, fadd(s[0], fdel(x, Rf)))
        elif rule == CHKR:
            x = Rf[j]; B, rT, rF = h_chkstate(x); tot[0] += 1
            Rx = fdel(x, Rf)
            walk(ps[0], fadd(B, Lf), fadd(rT, Rx)); walk(ps[1], Lf, fadd(B, fadd(rF, Rx)))
        else:
            tot[0] += 1
    try:
        walk(script, (), (root_atom(prog_t, prog_m, a, K),))
    except Exception:
        return None
    return tot[0]


class Producer:
    """The frozen production tactic (notes §1.9): deterministic, no backtracking, bound 64 nodes."""
    BOUND = 64

    def __init__(self, host=None):
        self.host = host or HostCheck()
        self.work = 0

    def produce(self, mode, prog, probe, a, K, V):
        v = mk_arg(V, prog, probe, a, K)
        n = ID[MODE_WRAP[mode]]
        Rb = ('cbox', n, v)
        Sb = ('cbox', n, swap_arg(v))
        self.count = 0
        self.V = V
        try:
            return self.tac(mode, Rb, Sb, V, (), (root_atom(prog, probe, a, K),))
        except (HostAbort, RecursionError):
            return None

    def tac(self, mode, Rb, Sb, V, Lf, Rf):
        self.count += 1; self.work += 1
        if self.count > self.BOUND: return None
        if BOTH in Lf or TOPH in Rf or any(x in Rf and x[0] in ('atom', 'cbox') for x in Lf): return node(AX, 0)
        hyps = [] if mode == 3 else ([Rb] if mode == 2 else [Rb, Sb])
        for j, b in enumerate(Rf):
            if b[0] == 'cbox' and b in hyps: return node(HYP, j)
        for j, b in enumerate(Lf):
            if self.runnable(b, Rb, Sb, V) and self.host.check(b[1], b[2]) != 'T': return node(RUNNEG, j)
        for j, b in enumerate(Rf):
            if self.runnable(b, Rb, Sb, V) and self.host.check(b[1], b[2]) == 'T': return node(RUN, j)
        for j, x in enumerate(Rf):
            if x[0] != 'atom': continue
            s = h_evstar(x, V // HOST_STEP_COST)
            if s is not None:
                p = self.tac(mode, Rb, Sb, V, Lf, fadd(s[0], fdel(x, Rf)))
                return None if p is None else node(EVS, j, p)
            c = h_chkstate(x)
            if c is not None:
                B, rT, rF = c
                Rx = fdel(x, Rf)
                p1 = self.tac(mode, Rb, Sb, V, fadd(B, Lf), fadd(rT, Rx))
                if p1 is None: return None
                p2 = self.tac(mode, Rb, Sb, V, Lf, fadd(B, fadd(rF, Rx)))
                if p2 is None: return None
                return node(CHKR, j, p1, p2)
            return None
        return None

    @staticmethod
    def runnable(b, Rb, Sb, V):
        if b[0] != 'cbox' or b == Rb or b == Sb: return False
        Vb = parse_carg(b[2])
        return Vb is not None and Vb >= V


# ----------------------------------------------------------------------------------------------------------------
# 4. Catalogue (two-pass production), plays, checks
# ----------------------------------------------------------------------------------------------------------------
CARRIER_BODIES = {'CB': body_CB, 'CB1': body_CB1, 'CBP': body_CBP, 'CBlet': body_CBlet, 'CBwrap': body_CBwrap}
HELDOUT_BODIES = {'CBlet2': body_CBlet2, 'CBw2': body_CBw2, 'CB1h': body_CB1h, 'CB1r': body_CB1r,
                  'CBPh': body_CBPh, 'CBPr': body_CBPr}
HELDOUT_CLASS = {'CBlet2': 'CB', 'CBw2': 'CB', 'CB1h': 'CB1', 'CB1r': 'CB1', 'CBPh': 'CBP', 'CBPr': 'CBP'}
SEARCH_B = 16


def dcert_list():
    """Dcert's bogus scripts rooted at the C question: Hyp at the root; EvR* then Hyp; Ax; EvR* then ChkR."""
    return cons([('C', node(HYP, 0)), ('C', node(EVS, 0, node(HYP, 0))), ('C', node(AX, 0)),
                 ('C', node(EVS, 0, node(CHKR, 0, node(AX, 0), node(HYP, 0))))])


def produce_list(prod, mode, mkprog, probes, K, V, want_D=True, D_probe=None):
    """Two-pass production for one program: its D script against ⌜D⌝ (built with an empty list), then its C scripts
    against the probes.  mkprog(certs) builds the program term with a given list.  Returns (list data, info)."""
    info = {'C': [], 'D': None}
    dlist = []
    if want_D:
        p0 = mkprog(0)
        s = prod.produce(mode, p0, L.PROG_D, 'D', K, V)
        if s is not None:
            dlist = [('D', s)]; info['D'] = s
    p1 = mkprog(cons(dlist))
    cs = []
    for pname, pr in probes:
        s = prod.produce(mode, p1, pr, 'C', K, V)
        info['C'].append((pname, s))
        if s is not None and s not in cs: cs.append(s)
    return cons([('C', s) for s in cs] + dlist), info


def build_arm(K, arm='S', V=None, k=None):
    """The catalogue of one arm at fuel K.  Returns (programs dict name -> term, production info)."""
    V = K // 4 if V is None else V
    k = K // 2 if k is None else k
    mode = {'S': 0, 'O': 2, 'X': 3}[arm]
    prod = Producer()
    progs, info = {}, {}
    progs['C'] = L.PROG_C
    progs['D'] = L.PROG_D

    def mk(bodyf, md):
        return lambda certs: carrier(bodyf(md, V, K), certs)
    # pass 1: D scripts of the probe carriers; pass 2: their C scripts against the D-only probes; the probes used for
    # every program's production (pass 3, below) carry both
    probe_d = {}
    for nm in ('CB', 'CB1', 'CBP'):
        p0 = mk(CARRIER_BODIES[nm], mode)(0)
        s = prod.produce(mode, p0, L.PROG_D, 'D', K, V)
        probe_d[nm] = s
    probes0 = [(nm, mk(CARRIER_BODIES[nm], mode)(cons([('D', probe_d[nm])] if probe_d[nm] else [])))
               for nm in ('CB', 'CB1', 'CBP')]
    probes = []
    for nm in ('CB', 'CB1', 'CBP'):
        lst, _ = produce_list(prod, mode, mk(CARRIER_BODIES[nm], mode), probes0, K, V)
        probes.append((nm, mk(CARRIER_BODIES[nm], mode)(lst)))
    info['_probes'] = {nm: h_getcerts(p) for nm, p in probes}
    # pass 3: every carrier's list
    for nm, bf in CARRIER_BODIES.items():
        lst, inf = produce_list(prod, mode, mk(bf, mode), probes, K, V)
        progs[nm] = mk(bf, mode)(lst); info[nm] = inf
    progs['CB0'] = mk(body_CB, mode)(0)
    lst, inf = produce_list(prod, mode, lambda c: carrier(C_, c), probes, K, V)
    progs['Ccert'] = carrier(C_, lst); info['Ccert'] = inf
    progs['Dcert'] = carrier(D_, dcert_list())
    progs['SF'] = L.SF(k)
    lst, inf = produce_list(prod, mode, lambda c: carrier(body_SFc(k), c), probes, K, V)
    progs['SFc'] = carrier(body_SFc(k), lst); info['SFc'] = inf
    if arm == 'S':
        cb_list = h_getcerts(progs['CB'])
        progs['CBfake'] = carrier(D_, cb_list)
        progs['CBdef'] = mk(body_CBdef, 0)(cb_list)
        cbp_c = [e for e in uncons(h_getcerts(progs['CBP'])) if e[0] == 'C'][0]
        cb_c = [e for e in uncons(cb_list) if e[0] == 'C'][0]
        progs['CBmut'] = mk(body_CB, 0)(cons([cbp_c, cb_c]))
        lst, inf = produce_list(prod, 0, mk(body_LobC, 0), probes, K, V)
        progs['LobC'] = mk(body_LobC, 0)(lst); info['LobC'] = inf
        lst, inf = produce_list(prod, 0, mk(body_CB, 4), probes, K, V)
        progs['CBsloppy'] = mk(body_CB, 4)(lst); info['CBsloppy'] = inf
        # naive and copy-checker carriers: production with their own modes, probes of their own family
        for nm, md in (('CBN', 1), ('CBS2', 5)):
            pd = prod.produce(md, mk(body_CB, md)(0), L.PROG_D, 'D', K, V)
            probe = mk(body_CB, md)(cons([('D', pd)] if pd else []))
            lst, inf = produce_list(prod, md, mk(body_CB, md), [('CB_' + nm, probe)], K, V)
            progs[nm] = mk(body_CB, md)(lst); info[nm] = inf
        progs['CBN0'] = mk(body_CB, 1)(0)
        U = K // 4
        progs['FB_code'] = L.FB(SEARCH_B, U, K)
        progs['FB1_code'] = L.FB1(SEARCH_B, U, K)
        progs['PB_code'] = L.PB(SEARCH_B, U, K)
        progs['G_code'] = L.G(SEARCH_B, U, K)
        # held-out: carry the production-set script of the shape class if it validates, else a fresh production
        for nm, bf in HELDOUT_BODIES.items():
            cls_list = h_getcerts(progs[HELDOUT_CLASS[nm]])
            lst_fresh, inf = produce_list(prod, mode, mk(bf, mode), probes, K, V)
            info[nm] = inf
            info[nm]['class_list'] = cls_list
            info[nm]['fresh_list'] = lst_fresh
            progs[nm] = mk(bf, mode)(cls_list)
            progs[nm + '_fresh'] = mk(bf, mode)(lst_fresh)
    info['_production_work'] = prod.work
    return progs, info


def play(p, q, K, events=None):
    return L.play(p, q, K, events)


def check_value(mode, V, t, m, a, K):
    """Clean run of capk(V, CC_mode, (V, (t, (m, (a, K))))): (result 'T'/'F'/'TO', record total steps)."""
    n = L.LIBIDX[MODE_CORE[mode]]
    arg = L.tval_to_rt(mk_arg(V, t, m, a, K))
    key = (n, V, arg)
    rec = L.CACHE.get(key)
    if rec is None:
        v, steps = L.evaluate(('capk', N(V), ('lib', n), mk_arg(V, t, m, a, K)))
        rec = L.CACHE.get(key)
        if rec is None: rec = (v, steps - 1)
    return rec


def wrapper_call_cost(mode, V, t, m, a, K):
    """Steps of the full wrapper call app(lib CHK_mode, arg) from a fresh context (the u(V) bound's subject)."""
    v, steps = L.evaluate(('app', ('lib', ID[MODE_WRAP[mode]]), mk_arg(V, t, m, a, K)))
    return v, steps


def rt_arg_fields(arg):
    """Runtime check argument (V, (Q t, (Q m, (a, K)))) -> (V, t term, m term, a, K)."""
    V, (t, (m, (a, K))) = arg
    return V, t.t if isinstance(t, L.Q) else L.term_of_enc(L.canon_rt(t)), \
        m.t if isinstance(m, L.Q) else L.term_of_enc(L.canon_rt(m)), a, K
