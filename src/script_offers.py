"""Queue 80 (spec specs/2026-11-16-script-checked-offers.md): script-checked offers in majority division (arm T).

A carrier is any program together with a script.  Packaging (the gene convention): the program's body is
    (if T B SCRIPT)
under the frame's three lambdas: the root evaluation takes the T branch (one tick) and never evaluates SCRIPT, a data literal
(nested `pair` / `nat`).  B is any L_T^code term; nothing constrains its spelling.

The shared checker CHKS (library; written in L_T^code; notes/script-checked-offers.md section 1 has the soundness argument):

  CHKS (x . c)   the wrapper:  (if (eq (capk KCHK CCORE (x . c)) T) T F)   -- always T or F, at most KCHK + 5 ticks
  CCORE (x . c)  accepts iff x is lam lam lam (if T B SCR), SCR holds an entry for the statement asked by code c, and the entry's
                 tree is a valid derivation: a case tree over the open atoms, each leaf checked by symbolic evaluation of the body
                 (`sev`) under the evaluation rules of L_T^code with the partners' quotes opaque.

Statement codes (asked about the checked program x):
  1 / 2   x holds an offer toward its next whose requirement is within h = 0 ({}) / h = 1 ({S_nx})        -- S_off(next; R), R <= h
  3 / 4   the same toward its prev
  5       x holds S_nx: in no profile does x name anyone at 2/3 (codes 2, 5, 8; a timeout or a non-code value plays 8)
Script entries (data): (kind . (params . tree)); kind 1 = S_off toward next, 2 = toward prev (params (R . (H . (fn . (fp . pref))))),
3 = S_nx (params 0).  Tree: (0 . 0) LEAF, (1 . (tT . tF)) SPLIT, (2 . 0) VAC.
Open atoms: the value of `CHKS (s . c')` with s a partner's quote (s = 0 next, 1 prev) and c' a literal code; and, inside a
partner read, `eq h v` with h the (unknown) value of a read and v a concrete nat / constant.

The eligibility predicate (the amendment's, verbatim in code, statement and proof): x's partner s is in E_x iff
  O_x contains s's side  and  CHKS(s, OFF(toward x, h = H_x)) = T  and  (R_x = {S_nx}  ->  CHKS(s, S_nx) = T),
i.e. s holds an offer toward x's slot whose requirement x holds (H_x is x's declared holding of S_nx) and s holds every
statement in x's requirement.  S_off(d; R): if d is x's preferred member of E_x (d in E_x and (pref = d or the other not in E_x)),
x names d at 1/2.

Machines.  S0: CCORE is the L_T^code term (charged step by step).  S1: CCORE is a primitive returning S0's value after charging
S0's exact step count for that (quote, code), precomputed on the catalogue (rejections included); a check whose remaining fuel is
below its count is interrupted exactly as S0 is (the replay rule of lt_code.replay_cached).
"""
import os, sys, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
import churn_primary_t as CT
import tplus as TP
import bully_resist as BR
import patient_accepter as PA
import certified_offers as CO          # installs queue 79's CARRY / CHK (the K arms) first; its machine stays C1

# ---------------------------------------------------------------- fuel (recorded in notes/script-checked-offers.md before the gates)
KCHK = int(os.environ.get('SCO_KCHK', 16000))       # CHKS's internal cap (>= the worst catalogue check cost, rejections included)
WCHK = KCHK + 5                                    # ticks a CHKS call can take at root (wrapper + capk + core)
CAPP = int(os.environ.get('SCO_CAP', 128000))       # read cap' (>= 8 * the worst accepted cost)
KRP = 3 * CAPP                                     # root fuel KR' = 3 cap'
REJCODE = 999999

CHK_SRC = r"""
(def CHKS (arg) (if (eq (capk KCHK CCORE arg) T) T F))
(def CCORE (arg)
  (let ((x (fst arg)) (c (snd arg)) (b0 (body3 x)))
    (if (eq (fst b0) 8)
        (let ((l (snd b0)) (cnd (fst l)))
          (if (and (eq (fst cnd) 3) (eq (snd cnd) 2))
              (centry x b0 (dat (fst (snd (snd l)))) c)
              F))
        F)))
(def body3 (x)
  (if (eq (fst x) 1)
      (let ((a (snd x)))
        (if (eq (fst a) 1)
            (let ((b (snd a))) (if (eq (fst b) 1) (snd b) NOQ))
            NOQ))
      NOQ))
(def dat (t)
  (let ((g (fst t)))
    (cond ((eq g 4) (snd t))
          ((eq g 5) (let ((l (snd t))) (pair (dat (fst l)) (dat (fst (snd l))))))
          (else BAD))))
(def centry (x b0 scr c)
  (let ((kw (cond ((lt c 3) 1) ((lt c 5) 2) (else 3)))
        (h (if (or (eq c 2) (eq c 4)) 1 0))
        (e (efind scr kw)))
    (if (eq e 0) F
      (let ((pr (fst (snd e))) (tr (snd (snd e))))
        (if (eq kw 3)
            (walk x b0 tr kw pr 0)
            (if (and (le (fst pr) h) (eq (if (eq kw 1) (fst (snd (snd pr))) (fst (snd (snd (snd pr))))) 1))
                (walk x b0 tr kw pr 0)
                F))))))
(def efind (l kw) (if (eq l 0) 0 (if (eq (fst (fst l)) kw) (fst l) (efind (snd l) kw))))
(def walk (x b0 tr kw pr lits)
  (wres (sev b0 (pair PTNP (pair PTNN (pair (pair 4 x) 0))) (pair 3 (pair 0 0)) topk) tr kw pr))
(def topk (v st) (pair 0 (pair v st)))
(def wres (r tr kw pr)
  (let ((k (fst r)) (tt (fst tr)))
    (cond ((eq k 8)
             (let ((q (snd r)))
               (cond ((eq tt 1) (let ((s (snd tr)) (kf (fst (snd q))))
                                  (if (wres (kf 2) (fst s) kw pr) (wres (kf 3) (snd s) kw pr) F)))
                     ((eq tt 2) (eq (guard kw pr (snd (snd q))) 0))
                     (else F))))
          ((eq k 9) F)
          (else (let ((st (snd (snd r))) (g (guard kw pr (snd (snd st)))))
                  (cond ((eq tt 0) (or (eq g 0) (and (le (fst st) FUEL) (inmask kw (fst (snd r))))))
                        ((eq tt 2) (eq g 0))
                        (else F)))))))
(def inmask (kw v)
  (if (eq (fst v) 0)
      (let ((n (snd v)))
        (cond ((eq kw 1) (eq n 1))
              ((eq kw 2) (eq n 4))
              (else (and (lt n 9) (not (eq (mod n 3) 2))))))
      F))
(def lk (key lits) (if (eq lits 0) 0 (let ((e (fst lits))) (if (eq (fst e) key) (snd e) (lk key (snd lits))))))
(def k3 (key lits) (let ((b (lk key lits))) (cond ((eq b 2) 1) ((eq b 3) 0) (else 2))))
(def kand (a b) (cond ((or (eq a 0) (eq b 0)) 0) ((and (eq a 1) (eq b 1)) 1) (else 2)))
(def knot (a) (if (eq a 2) 2 (sub 1 a)))
(def kor (a b) (knot (kand (knot a) (knot b))))
(def kb (b) (if b 1 0))
(def emem (s on hh R lits)
  (kand (kb (eq on 1)) (kand (k3 (pair s (add (if (eq s 0) 3 1) hh)) lits) (if (eq R 1) (k3 (pair s 5) lits) 1))))
(def guard (kw pr lits)
  (if (eq kw 3) 1
    (let ((R (fst pr)) (q1 (snd pr)) (hh (fst q1)) (q2 (snd q1)) (fn (fst q2)) (q3 (snd q2)) (fp (fst q3)) (pf (snd q3))
          (en (emem 0 fn hh R lits)) (ep (emem 1 fp hh R lits)))
      (if (eq kw 1) (kand en (kor (kb (eq pf 0)) (knot ep)))
                    (kand ep (kor (kb (eq pf 1)) (knot en)))))))
(def tk (st n) (pair (add (fst st) n) (snd st)))
(def addlit (st key b) (let ((r (snd st))) (pair (fst st) (pair (fst r) (pair (pair key b) (snd r))))))
(def nthv (e i) (if (eq i 0) (fst e) (nthv (snd e) (sub i 1))))
; continuation-passing symbolic evaluation: (sev t env st k); st = (steps . (havoc count . literals)); a result is
; (0 . (v . st)) from topk, (8 . (key . (resume . literals))) a need, or REJ = (9 . 0)
(def sev (t env st k)
  (let ((g (fst t)))
    (cond ((eq g 0) (k (nthv env (snd t)) st))
          ((eq g 2) (let ((p (snd t)))
                      (sev (fst p) env st (lambda (f s1) (sev (fst (snd p)) env s1 (lambda (a s2) (sapply f a s2 k)))))))
          ((eq g 4) (k (pair 0 (snd t)) st))
          ((eq g 8) (let ((p (snd t))) (sev (fst p) env st (lambda (c s1) (sif c p env s1 k)))))
          ((eq g 1) (k (pair 3 (pair (snd t) env)) st))
          ((eq g 3) (k (pair 1 (snd t)) st))
          ((eq g 12) (k (pair 5 (snd t)) st))
          ((eq g 11) (let ((p (snd t)))
                       (sev (fst p) env st (lambda (a s1) (sev (fst (snd p)) env s1 (lambda (b s2) (seqv a b (tk s2 1) k)))))))
          ((eq g 5) (let ((p (snd t)))
                      (sev (fst p) env st (lambda (a s1) (sev (fst (snd p)) env s1 (lambda (b s2) (k (pair 2 (pair a b)) s2)))))))
          ((eq g 10) (k (pair 4 (snd t)) st))
          ((eq g 6) (sev (fst (snd t)) env st (lambda (a s1) (if (eq (fst a) 2) (k (fst (snd a)) (tk s1 1)) REJ))))
          ((eq g 7) (sev (fst (snd t)) env st (lambda (a s1) (if (eq (fst a) 2) (k (snd (snd a)) (tk s1 1)) REJ))))
          ((eq g 13) (let ((p (snd t)) (l (snd p)))
                       (sev (fst l) env st (lambda (a s1) (sev (fst (snd l)) env s1 (lambda (b s2) (sop (fst p) a b s2 k)))))))
          ((eq g 14) (let ((l (snd t)))
                       (sev (fst l) env st (lambda (q s1) (sev (fst (snd l)) env s1 (lambda (f s2)
                         (sev (fst (snd (snd l))) env s2 (lambda (v s3)
                           (if (and (eq (fst q) 0) (eq (fst f) 7)) (havoc s3 (snd q) k) REJ)))))))))
          ((eq g 15) (let ((l (snd t)))
                       (sev (fst l) env st (lambda (q s1) (sev (fst (snd l)) env s1 (lambda (x s2)
                         (sev (fst (snd (snd l))) env s2 (lambda (y s3)
                           (if (and (eq (fst q) 0) (and (eq (fst x) 6) (or (eq (fst y) 6) (eq (fst y) 4))))
                               (havoc s3 (snd q) k) REJ)))))))))
          (else REJ))))
(def sapply (f a st k)
  (let ((g (fst f)))
    (cond ((eq g 3) (let ((c (snd f))) (sev (fst c) (pair a (snd c)) (tk st 1) k)))
          ((eq g 5) (let ((n (snd f)))
                      (if (eq n ID_CHKS) (satom a st k) (sev (snd (libsrc n)) (pair a 0) (tk st 1) k))))
          (else REJ))))
(def satom (a st k)
  (if (eq (fst a) 2)
      (let ((q (snd a)) (x (fst q)) (c (snd q)))
        (if (and (eq (fst x) 6) (eq (fst c) 0))
            (askk (pair (snd x) (snd c)) (tk st WCHK) k)
            REJ))
      REJ))
(def askk (key st k)
  (let ((L (snd (snd st))) (b (lk key L)))
    (if (eq b 0)
        (pair 8 (pair key (pair (lambda (bb) (k (pair 1 bb) (addlit st key bb))) L)))
        (k (pair 1 b) st))))
(def sif (c p env st k)
  (if (eq (fst c) 1)
      (let ((cv (snd c)))
        (cond ((eq cv 2) (sev (fst (snd p)) env (tk st 1) k))
              ((eq cv 3) (sev (fst (snd (snd p))) env (tk st 1) k))
              (else REJ)))
      REJ))
(def basic (v) (lt (fst v) 2))
(def seqv (a b st k)
  (let ((ka (fst a)) (kq (fst b)))
    (cond ((and (basic a) (basic b)) (k (pair 1 (if (eq a b) 2 3)) st))
          ((and (eq ka 4) (eq kq 4)) (k (pair 1 (if (eq (snd a) (snd b)) 2 3)) st))
          ((and (eq ka 7) (basic b)) (askk (pair (add (snd a) 2) b) st k))
          ((and (eq kq 7) (basic a)) (askk (pair (add (snd b) 2) a) st k))
          (else REJ))))
(def sop (o a b st k)
  (if (and (eq (fst a) 0) (eq (fst b) 0))
      (let ((x (snd a)) (y (snd b)) (s3 (tk st 1)))
        (cond ((eq o 0) (k (pair 0 (add x y)) s3))
              ((eq o 1) (k (pair 0 (sub x y)) s3))
              ((eq o 2) (k (pair 0 (mul x y)) s3))
              ((eq o 3) (if (eq y 0) REJ (k (pair 0 (div x y)) s3)))
              ((eq o 4) (if (eq y 0) REJ (k (pair 0 (mod x y)) s3)))
              ((eq o 5) (k (pair 1 (if (le x y) 2 3)) s3))
              (else (k (pair 1 (if (lt x y) 2 3)) s3))))
      REJ))
(def havoc (st q k) (let ((r (snd st)) (h (fst r))) (k (pair 7 h) (pair (add (fst st) (add q 2)) (pair (add h 1) (snd r))))))

; ---------------- the shared offer rule (the canonical spelling calls it) ----------------
(def OFFER (cert fb me n p)
  (let ((r3 (snd (snd (snd cert))))
        (en (if (eq (fst cert) 1) (ELIG n (add 3 (fst r3)) (snd r3)) F))
        (ep (if (eq (fst (snd cert)) 1) (ELIG p (add 1 (fst r3)) (snd r3)) F)))
    (if en (if ep (if (eq (fst (snd (snd cert))) 0) 1 4) 1) (if ep 4 (fb me n p)))))
(def ELIG (x c R) (if (CHKS (pair x c)) (if (eq R 1) (CHKS (pair x 5)) T) F))
(def FAKEOFFER (cert fb me n p) (fb me n p))
"""

_LIB = {}


def _bind(vs, expr, body):
    v, s = vs
    return ['let', [['r_', expr]], ['let', [[v, ['fst', 'r_']], [s, ['snd', 'r_']]], ['if', ['lt', 7, ['fst', v]], 'r_', body]]]


def install():
    """append the library entries once (after queue 79's); returns {name: index}."""
    if _LIB:
        return _LIB
    base = len(L.LIB)
    comp = L.SxCompiler()
    comp.load(CHK_SRC)
    consts = dict(KCHK=KCHK, WCHK=WCHK, FUEL=KRP, NOQ=['pair', 0, 0], BAD=REJCODE, REJ=['pair', 9, 0],
                  PTNN=['pair', 6, 0], PTNP=['pair', 6, 1])
    for k, v in consts.items():
        comp.consts[k] = v
    comp.consts['ID_CHKS'] = base + comp.order.index('CHKS')
    terms = comp.build(base)
    L.LIB.extend(terms)
    for i, n in enumerate(comp.order):
        L.LIBNAME[base + i] = n
        L.LIBIDX[n] = base + i
    L.LIBCODE.extend([L.compile_term(t[1]) for t in terms])
    _LIB.update({n: base + i for i, n in enumerate(comp.order)})
    return _LIB


install()
ID_CHKS, ID_CCORE, ID_OFFER, ID_ELIG, ID_FAKE = (_LIB[n] for n in ('CHKS', 'CCORE', 'OFFER', 'ELIG', 'FAKEOFFER'))
S0CODE = L.LIBCODE[ID_CCORE]


# ---------------------------------------------------------------- the capk-closure regress key (an exact fast-forward; notes 2)
_orig_do_capk = L.do_capk


def _key_rt(v):
    """a type-aware structural key (a quote and an explicit pair encoding with the same canonical form are told apart)."""
    tv = type(v)
    if tv is int or tv is str:
        return v
    if tv is tuple:
        return ('P', _key_rt(v[0]), _key_rt(v[1]))
    if tv is L.Q:
        return ('Q', v.canon())
    if tv is L.Clo or tv is L.FixV:
        # (the body's canonical form, the environment's values): determines the closure's behaviour; no new term is built
        # (canon_rt would substitute the environment and cache a fresh term per call)
        env = []
        e = v.env
        while e is not None:
            env.append(_key_rt(e[0])); e = e[1]
        return (tv.__name__, L.canon_term(v.body), tuple(env))
    if tv is L.LibV:
        return ('LibV', v.n)
    return (tv.__name__, L.canon_rt(v))


def do_capk_keyed(k, f, v):
    """lt_code.do_capk, with a regress key for closures too: (canonical closure, k, canonical argument).  Milestone 3's regress lemma
    (a frame whose key is active in an enclosing frame cannot return before some enclosing deadline; the run is fast-forwarded to
    the first deadline) applies unchanged; the fast-forward is exact (same tick count, same frame times out)."""
    if type(f) is L.Clo:
        try:
            key = ('clo', k, _key_rt(f), _key_rt(v))
            hash(key)
        except Exception:
            key = None
        return L.enter_sim(k, lambda: L.apply(f, v), key)
    return _orig_do_capk(k, f, v)


REGRESS = ['off']


def set_regress(on):
    """install / remove the closure regress key (the compiled capk calls L.do_capk by global lookup)."""
    L.do_capk = do_capk_keyed if on else _orig_do_capk
    L._compiled.clear()
    REGRESS[0] = 'on' if on else 'off'


# ---------------------------------------------------------------- machines S0 / S1
S1TAB = {}          # (canonical encoding of x, code) -> (value 'T' / 'F', S0 ticks inside CCORE's body)
_S1ID = {}
MACHINE = ['S0']


def _ccore_s1(env):
    a = env[0]
    if type(a) is not tuple or type(a[0]) is not L.Q or type(a[1]) is not int:
        raise RuntimeError('S1: argument outside the catalogue table: %r' % (a,))
    q = a[0]
    t = q.t
    e = _S1ID.get(id(t))
    if e is None or e[0] is not t:
        key = (q.canon(), a[1])
        rec = S1TAB.get(key)
        if rec is None:
            raise RuntimeError('S1: (quote, code) not tabulated')
        _S1ID[id(t)] = e = (t, q.canon())
    rec = S1TAB.get((e[1], a[1]))
    if rec is None:
        raise RuntimeError('S1: (quote, code) not tabulated')
    val, cost = rec
    u = L.ST[0]
    tfail = min(L.ST[1], L.ST[2]) - u + 1
    if tfail <= cost:
        L.ST[0] = u + tfail - 1
        L.tick()
        raise AssertionError('S1: tick did not fail')
    L.ST[0] = u + cost
    if val == 'BOT':
        raise L.Stuck()
    return val


def set_machine(m):
    assert m in ('S0', 'S1')
    L.LIBCODE[ID_CCORE] = S0CODE if m == 'S0' else _ccore_s1
    L._compiled.clear()
    MACHINE[0] = m


def core_s0(x_term, code):
    """run CCORE in S0 on (quote x, code) from a fresh context: (value, ticks inside CCORE's body)."""
    set_machine('S0')
    t = ('app', ('lib', ID_CCORE), ('pair', ('quote', x_term), ('nat', code)))
    v, st = L.run_big(L.evaluate, t, 10 ** 8)
    return v, st - 1          # minus the application tick


def chks_root(x_term, code, fuel=10 ** 8):
    """the value and ticks of CHKS (x . code) at root (the wrapper included)."""
    t = ('app', ('lib', ID_CHKS), ('pair', ('quote', x_term), ('nat', code)))
    return L.run_big(L.evaluate, t, fuel)


# ---------------------------------------------------------------- programs
PCOMP = L.SxCompiler()


def prog(src):
    PCOMP.index = dict(L.LIBIDX)
    return PCOMP.expr(L.sx_parse(src)[0], [])


def data_term(d):
    if isinstance(d, bool):
        raise ValueError(d)
    if isinstance(d, int):
        return ('nat', d)
    return ('pair', data_term(d[0]), data_term(d[1]))


def cons(xs):
    out = 0
    for x in reversed(xs):
        out = (x, out)
    return out


def recap(src, cap):
    """the source with every read cap 400 (KS) replaced by cap."""
    return src.replace('capk %d ' % CT.KS, 'capk %d ' % cap).replace('run %d ' % CT.KS, 'run %d ' % cap)


def base_library(cap):
    """queue 78's 59 programs at read cap `cap` (sources rewritten; names, families and order unchanged)."""
    return [(n, f, recap(s, cap)) for n, f, s in PA.library_pa()]


def _shift(t, d, c=0):
    return CO._shift(t, d, c)


def package(body, script):
    """lam me n p. (if T body SCRIPT); `body` is a term under the three lambdas (me = v2, n = v1, p = v0)."""
    return ('lam', ('lam', ('lam', ('if', ('con', 'T'), body, data_term(script)))))


def fb_body(fb_term):
    """the fallback program's term (closed lam^3)."""
    assert fb_term[0] == 'lam' and fb_term[1][0] == 'lam' and fb_term[1][1][0] == 'lam'
    return fb_term


ME, NX_, PV = ('v', 2), ('v', 1), ('v', 0)


def cert_lit(fn, fp, pf, H, R):
    return ('pair', ('nat', fn), ('pair', ('nat', fp), ('pair', ('nat', pf), ('pair', ('nat', H), ('nat', R)))))


def _app(*xs):
    t = xs[0]
    for a in xs[1:]:
        t = ('app', t, a)
    return t


def _let(val, body):
    """(let ((x val)) body): body sees x as v0 and everything else shifted by one."""
    return ('app', ('lam', body), val)


def _chks(x, c):
    return ('app', ('lib', ID_CHKS), ('pair', x, ('nat', c)))


def _elig_inline(x, c, R):
    """(if (CHKS (x . c)) (if R (CHKS (x . 5)) T) F) with R a constant."""
    return ('if', _chks(x, c), _chks(x, 5) if R == 1 else ('con', 'T'), ('con', 'F'))


def _elig_lib(x, c, R):
    return _app(('lib', ID_ELIG), x, ('nat', c), ('nat', R))


def body_spelling(sp, fn, fp, pf, H, R, fb, depth=0):
    """the body (under me n p, plus `depth` enclosing binders) of a carrier with rule parameters (fn, fp, pf, H, R) and fallback
    program fb, in spelling sp:
      canon   ((((((lib OFFER) CERT) FB) me) n) p)            the shared library rule
      inl     OFFER's body inlined (constants folded), eligibility through lib ELIG
      rord    inlined with the reads and the branches in the other order
      guard   (if T canon 0)                                   the canonical call under a trivially true guard
      noelig  inlined, eligibility written with direct CHKS calls (no ELIG)"""
    me, n, p = ('v', 2 + depth), ('v', 1 + depth), ('v', 0 + depth)
    if sp == 'canon':
        return _app(('lib', ID_OFFER), cert_lit(fn, fp, pf, H, R), fb, me, n, p)
    if sp == 'guard':
        return ('if', ('con', 'T'), body_spelling('canon', fn, fp, pf, H, R, fb, depth), ('nat', 0))
    el = _elig_lib if sp in ('inl', 'rord') else _elig_inline
    if sp in ('inl', 'noelig'):
        # (let ((en E_n)) (let ((ep E_p)) (if en (if ep PREF 1) (if ep 4 (fb me n p)))))
        en = el(n, 3 + H, R) if fn == 1 else ('con', 'F')
        ep = el(_shift(p, 1), 1 + H, R) if fp == 1 else ('con', 'F')
        me2, n2, p2 = (_shift(x, 2) for x in (me, n, p))
        fall = _app(_shift(fb, 2), me2, n2, p2)
        inner = ('if', ('v', 1), ('if', ('v', 0), ('nat', 1 if pf == 0 else 4), ('nat', 1)), ('if', ('v', 0), ('nat', 4), fall))
        return _let(en, _let(ep, inner))
    if sp == 'rord':
        # (let ((ep E_p)) (let ((en E_n)) (if ep (if en PREF 4) (if en 1 (fb me n p)))))
        ep = el(p, 1 + H, R) if fp == 1 else ('con', 'F')
        en = el(_shift(n, 1), 3 + H, R) if fn == 1 else ('con', 'F')
        me2, n2, p2 = (_shift(x, 2) for x in (me, n, p))
        fall = _app(_shift(fb, 2), me2, n2, p2)
        inner = ('if', ('v', 1), ('if', ('v', 0), ('nat', 1 if pf == 0 else 4), ('nat', 4)), ('if', ('v', 0), ('nat', 1), fall))
        return _let(ep, _let(en, inner))
    raise ValueError(sp)


SPELLINGS = ('canon', 'inl', 'rord', 'guard', 'noelig')

# families: (name prefix, family tag, H, R, nx held, directions -> (fn, fp, pf, fallback name))
FAM_SPECS = [
    ('Oc', 's_open', 0, 0, False, [('n', (1, 0, 0, 'C1')), ('p', (0, 1, 1, 'C4'))]),
    ('Rc', 's_acc', 0, 0, False, [('n', (1, 0, 0, 'C3')), ('p', (0, 1, 1, 'C0'))]),
    ('Fc', 's_firm', 0, 0, False, None),
    ('Bc', 's_bully', 0, 0, False, [('n', (1, 1, 0, 'Bn')), ('p', (1, 1, 1, 'Bp'))]),
    ('Oc+', 's_open+', 1, 0, True, [('n', (1, 0, 0, 'C1')), ('p', (0, 1, 1, 'C4'))]),
    ('Rc+', 's_acc+', 1, 0, True, [('n', (1, 0, 0, 'C3')), ('p', (0, 1, 1, 'C0'))]),
    ('Fc+', 's_firm+', 1, 0, True, None),
    ('Pc+', 's_prud+', 1, 1, True, None),
    ('OcR+', 's_openR+', 1, 1, True, [('n', (1, 0, 0, 'C1')), ('p', (0, 1, 1, 'C4'))]),
    ('RcR+', 's_accR+', 1, 1, True, [('n', (1, 0, 0, 'C3')), ('p', (0, 1, 1, 'C0'))]),
]
FIRM_FB = ('Snoy', 'Spoy')          # the two firm-reader fallbacks (fallback o, S_nx derivable), the same in every arm
FAM_S = [f[1] for f in FAM_SPECS]


def _dirs(spec):
    if spec[5] is not None:
        return spec[5]
    return [(fb[1], (1, 1, 0 if fb[1] == 'n' else 1, fb)) for fb in FIRM_FB]


def s_carriers():
    """[(name, family, spelling, params dict)] of the script carriers, in catalogue order."""
    out = []
    for pre, fam, H, R, nx, _ in FAM_SPECS:
        for d, (fn, fp, pf, fbn) in _dirs((pre, fam, H, R, nx, _)):
            for sp in SPELLINGS:
                nm = '%s%s.%s' % (pre, fbn if fam in ('s_firm', 's_firm+', 's_prud+') else d, sp)
                out.append((nm, fam, sp, dict(fn=fn, fp=fp, pf=pf, H=H, R=R, nx=nx, fb=fbn)))
    return out


# ---------------------------------------------------------------- the host reference checker (independent of the CCORE term)
class Need(Exception):
    def __init__(self, key):
        self.key = key


class Rej(Exception):
    pass


def _canon_val(v):
    return v


class HostEval:
    """the same rules as `sev`, on Python terms; values ('nat', n) ('con', code) ('pair', a, b) ('clo', body, env) ('quote', t)
    ('lib', n) ('ptn', s) ('hav', h)."""

    def __init__(self, lits):
        self.lits = lits
        self.steps = 3
        self.h = 0

    def ev(self, t, env):
        g = t[0]
        if g == 'v':
            e = env
            for _ in range(t[1]):
                e = e[1]
            return e[0]
        if g == 'nat':
            return ('nat', t[1])
        if g == 'con':
            return ('con', L.CONCODE[t[1]])
        if g == 'lam':
            return ('clo', t[1], env)
        if g == 'lib':
            return ('lib', t[1])
        if g == 'quote':
            return ('quote', t[1])
        if g == 'pair':
            a = self.ev(t[1], env); b = self.ev(t[2], env)
            return ('pair', a, b)
        if g == 'app':
            f = self.ev(t[1], env); a = self.ev(t[2], env)
            return self.apply(f, a)
        if g == 'if':
            c = self.ev(t[1], env)
            if c == ('con', 2):
                self.steps += 1; return self.ev(t[2], env)
            if c == ('con', 3):
                self.steps += 1; return self.ev(t[3], env)
            raise Rej()
        if g in ('fst', 'snd'):
            a = self.ev(t[1], env)
            if a[0] != 'pair':
                raise Rej()
            self.steps += 1
            return a[1] if g == 'fst' else a[2]
        if g == 'eq':
            a = self.ev(t[1], env); b = self.ev(t[2], env)
            self.steps += 1
            basic = ('nat', 'con')
            if a[0] in basic and b[0] in basic:
                return ('con', 2 if a == b else 3)
            if a[0] == 'quote' and b[0] == 'quote':
                return ('con', 2 if L.canon_term(a[1]) == L.canon_term(b[1]) else 3)
            if a[0] == 'hav' and b[0] in basic:
                return self.lit((a[1] + 2, b))
            if b[0] == 'hav' and a[0] in basic:
                return self.lit((b[1] + 2, a))
            raise Rej()
        if g == 'op':
            a = self.ev(t[2], env); b = self.ev(t[3], env)
            if a[0] != 'nat' or b[0] != 'nat':
                raise Rej()
            self.steps += 1
            x, y = a[1], b[1]
            o = t[1]
            if o in ('div', 'mod') and y == 0:
                raise Rej()
            if o in ('le', 'lt'):
                return ('con', 2 if (x <= y if o == 'le' else x < y) else 3)
            return ('nat', {'add': x + y, 'sub': max(0, x - y), 'mul': x * y, 'div': x // max(y, 1), 'mod': x % max(y, 1)}[o])
        if g == 'capk':
            k = self.ev(t[1], env); f = self.ev(t[2], env); v = self.ev(t[3], env)
            if k[0] != 'nat' or f[0] != 'hav':
                raise Rej()
            return self.havoc(k[1])
        if g == 'run':
            k = self.ev(t[1], env); x = self.ev(t[2], env); y = self.ev(t[3], env)
            if k[0] != 'nat' or x[0] != 'ptn' or y[0] not in ('ptn', 'quote'):
                raise Rej()
            return self.havoc(k[1])
        raise Rej()

    def havoc(self, k):
        h = self.h
        self.h += 1
        self.steps += k + 2
        return ('hav', h)

    def lit(self, key):
        b = self.lits.get(key)
        if b is None:
            raise Need(key)
        return ('con', b)

    def apply(self, f, a):
        if f[0] == 'clo':
            self.steps += 1
            return self.ev(f[1], (a, f[2]))
        if f[0] == 'lib':
            n = f[1]
            if n == ID_CHKS:
                if a[0] != 'pair' or a[1][0] != 'ptn' or a[2][0] != 'nat':
                    raise Rej()
                key = (a[1][1], a[2][1])
                b = self.lits.get(key)
                if b is None:
                    raise Need(key)
                self.steps += WCHK
                return ('con', b)
            self.steps += 1
            return self.ev(L.LIB[n][1], (a, 0))
        raise Rej()


def host_body(x_term):
    """(body0, script data) of a packaged program, or None."""
    try:
        b0 = x_term[1][1][1]
        if x_term[0] != 'lam' or x_term[1][0] != 'lam' or x_term[1][1][0] != 'lam':
            return None
        if b0[0] != 'if' or b0[1] != ('con', 'T'):
            return None
        return b0, host_dat(b0[3])
    except (IndexError, TypeError):
        return None


def host_dat(t):
    if t[0] == 'nat':
        return t[1]
    if t[0] == 'pair':
        return (host_dat(t[1]), host_dat(t[2]))
    return REJCODE


def host_guard(kw, pr, lits):
    if kw == 3:
        return 1

    def k3(key):
        b = lits.get(key)
        return 2 if b is None else (1 if b == 2 else 0)

    def kand(a, b):
        return 0 if (a == 0 or b == 0) else (1 if a == 1 and b == 1 else 2)

    def knot(a):
        return 2 if a == 2 else 1 - a

    def kor(a, b):
        return knot(kand(knot(a), knot(b)))
    R, (H, (fn, (fp, pf))) = pr

    def emem(s, on):
        return kand(1 if on == 1 else 0, kand(k3((s, (3 if s == 0 else 1) + H)), k3((s, 5)) if R == 1 else 1))
    en, ep = emem(0, fn), emem(1, fp)
    if kw == 1:
        return kand(en, kor(1 if pf == 0 else 0, knot(ep)))
    return kand(ep, kor(1 if pf == 1 else 0, knot(en)))


def host_inmask(kw, v):
    if v[0] != 'nat':
        return False
    n = v[1]
    if kw == 1:
        return n == 1
    if kw == 2:
        return n == 4
    return n < 9 and n % 3 != 2


def _run_path(x_term, b0, lits):
    env = (('ptn', 1), (('ptn', 0), (('quote', x_term), 0)))
    he = HostEval(lits)
    try:
        v = he.ev(b0, env)
        return 'value', v, he.steps
    except Need as e:
        return 'need', e.key, he.steps
    except Rej:
        return 'rej', None, he.steps
    except RecursionError:
        return 'rej', None, he.steps


def host_walk(x_term, b0, tr, kw, pr, lits):
    try:
        tt = tr[0]
    except TypeError:
        return False
    kind, v, steps = _run_path(x_term, b0, lits)
    if kind == 'need':
        if tt == 1:
            s = tr[1]
            try:
                sT, sF = s
            except (TypeError, ValueError):
                return False
            return host_walk(x_term, b0, sT, kw, pr, {**lits, v: 2}) and host_walk(x_term, b0, sF, kw, pr, {**lits, v: 3})
        if tt == 2:
            return host_guard(kw, pr, lits) == 0
        return False
    if kind == 'rej':
        return False
    if tt == 0:
        return host_guard(kw, pr, lits) == 0 or (steps <= KRP and host_inmask(kw, v))
    if tt == 2:
        return host_guard(kw, pr, lits) == 0
    return False


def _kw_h(c):
    return (1 if c < 3 else (2 if c < 5 else 3)), (1 if c in (2, 4) else 0)


def host_check(x_term, c):
    """the host reference of CCORE's decision (True / False)."""
    hb = host_body(x_term)
    if hb is None:
        return False
    b0, scr = hb
    kw, h = _kw_h(c)
    l = scr
    e = None
    try:
        while l != 0:
            if l[0][0] == kw:
                e = l[0]; break
            l = l[1]
    except (TypeError, IndexError):
        return False
    if e is None:
        return False
    try:
        pr, tr = e[1]
    except (TypeError, ValueError):
        return False
    if kw != 3:
        try:
            R, (H, (fn, (fp, pf))) = pr
        except (TypeError, ValueError):
            return False
        if not (R <= h and (fn if kw == 1 else fp) == 1):
            return False
    return host_walk(x_term, b0, tr, kw, pr, {})


def tactic(x_term_unpacked_body, kw, pr, x_term_for_me):
    """the case tree for statement kw on a body (searched by the host evaluator): SPLIT at every need, VAC where the guard is false,
    LEAF at values.  Returns the tree (data) or None if some leaf fails."""
    def go(lits):
        g = host_guard(kw, pr, lits)
        kind, v, steps = _run_path(x_term_for_me, x_term_unpacked_body, lits)
        if kind == 'need':
            if g == 0:
                return (2, 0)
            a = go({**lits, v: 2}); b = go({**lits, v: 3})
            if a is None or b is None:
                return None
            return (1, (a, b))
        if kind == 'rej':
            return (2, 0) if g == 0 else None
        if g == 0:
            return (2, 0)
        if steps <= KRP and host_inmask(kw, v):
            return (0, 0)
        return None
    return go({})


def build_carrier(body, entries_fn):
    """two-pass build: the script's trees are found on the packaged term with a placeholder script (the tree does not depend on the
    script literal, which the root evaluation never reads); returns the packaged term with its script."""
    tmp = package(body, 0)
    b0 = tmp[1][1][1]
    script = entries_fn(b0, tmp)
    return package(body, script), script


def carrier_entries(prm):
    """script entries for a carrier with params prm: S_off toward each offered side, and S_nx if held.  Built by the tactic."""
    pr = (prm['R'], (prm['H'], (prm['fn'], (prm['fp'], prm['pf']))))

    def f(b0, tmp):
        ents = []
        for kw, on in ((1, prm['fn']), (2, prm['fp'])):
            if on:
                tr = tactic(b0, kw, pr, tmp)
                if tr is None:
                    raise RuntimeError('no derivation for kind %d' % kw)
                ents.append((kw, (pr, tr)))
        if prm['nx']:
            tr = tactic(b0, 3, 0, tmp)
            if tr is None:
                raise RuntimeError('no S_nx derivation')
            ents.append((3, (0, tr)))
        return cons(ents)
    return f


def script_nodes(d):
    """node count of a script as data (each pair and each nat a node)."""
    if isinstance(d, int):
        return 1
    return 1 + script_nodes(d[0]) + script_nodes(d[1])


def term_nodes(t):
    tag = t[0]
    if tag in ('v', 'nat', 'con', 'lib'):
        return 1
    if tag in ('lam', 'fix', 'quote'):
        return 1 + term_nodes(t[1])
    if tag == 'op':
        return 1 + term_nodes(t[2]) + term_nodes(t[3])
    if tag == 'sim':
        return 1 + term_nodes(t[2])
    return 1 + sum(term_nodes(a) for a in t[1:])
