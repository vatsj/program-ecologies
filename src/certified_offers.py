"""Queue 79 (spec specs/2026-11-15-certified-offers.md): certified offers in majority division (arm T).

Certificates as a shared library combinator plus a skeleton check (notes/certified-offers.md section 1 has the soundness argument).

Library (appended to lt_code's library; milestone 3's indices unchanged; nothing existing is edited):

  CARRY cert fb me n p   the certified rule.  cert = (fn . (fp . pref)), three bits: fn = 1 offers toward next, fp = 1 toward prev,
                         pref 0 = next, 1 = prev.  E = {next if fn and CHK(n, 1)} u {prev if fp and CHK(p, 0)}; if E has two members
                         name the preferred one at 1/2, if one name it at 1/2 (code 1 next, 4 prev); otherwise play fb me n p.
  CHK (x . w)            the check: x is a quote; T iff x is a carrier (the skeleton below, cert well formed) whose flag toward my side
                         is 1 (w = 1: x's fp, I am x's prev... x is my next, so I am x's prev; w = 0: x's fn).
  skeleton               lam me. lam n. lam p. (((((lib CARRY) CERT) FB) me) n) p, with CERT a literal pair (nat b, (nat b, nat b)),
                         b in {0, 1}, FB a lambda (a value), and me n p the three bound variables in order (v2 v1 v0).

Machines.  C0: CHK is the L_T^code term below (a walk of the quote by fst / snd / eq), charged step by step.  C1: CHK is a primitive
with the same input-output map and a fixed cost KAPPA ticks (plus the application tick).  The quotes are identical in both machines
(the same library index), so C1 and C0 differ only in the cost of a check (V3 compares their tables).

Programs (appended after queue 78's 59; the first 59 unchanged):
  Ocn / Ocp      certified opener: offer toward next / prev only, fallback the 1/2 constant naming that partner (C1 / C4)
  Fc<F>          certified firm reader: offers toward both partners, preference = the first-read direction of its fallback F, fallback
                 the firm reader F (T's 16 single and two-partner readers, so Fc and F differ only by the certificate)
  Rcn / Rcp      certified patient accepter (pure): offer toward next / prev only, fallback the 1/3 constant naming the other partner
                 (C3 / C0); it reads no one
  Rcsn / Rcsp    hybrid: as Rc, fallback queue 78's R (Rnn / Rpn), which reads the offer slot by simulation
  Bcn / Bcp      certified Trojan bully: offers toward both partners (preference n / p), fallback the simulating bully Bn / Bp
  Pc<P>          certified prudent reader: offers toward both, preference = P's read direction, fallback P (the four P_z)
Forgers (gate catalogue only; never in the dynamics): see FORGERS.
"""
import os, sys, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
import churn_primary_t as CT
import tplus as TP
import bully_resist as BR
import patient_accepter as PA

KAPPA = 50                 # C1: ticks charged by one check (recorded in notes/certified-offers.md before the gates); cap / 8 = 50
NOC = 99                   # 'no certificate' value of skel

CO_SRC = r"""
(def CARRY (cert fb me n p)
  (let ((en (if (eq (fst cert) 1) (CHK (pair n 1)) F)))
    (let ((ep (if (eq (fst (snd cert)) 1) (CHK (pair p 0)) F)))
      (if en (if ep (if (eq (snd (snd cert)) 0) 1 4) 1)
          (if ep 4 (fb me n p))))))
(def CHK (arg)
  (let ((c (skel (fst arg))))
    (if (eq c 99) F
        (if (eq (snd arg) 0) (eq (fst c) 1) (eq (fst (snd c)) 1)))))
(def skel (x)
  (if (eq (fst x) 1)
      (let ((b1 (snd x)))
        (if (eq (fst b1) 1)
            (let ((b2 (snd b1)))
              (if (eq (fst b2) 1) (skelb (snd b2)) 99))
            99))
      99))
(def appf (t) (fst (snd t)))
(def appa (t) (fst (snd (snd t))))
(def isv (t i) (and (eq (fst t) 0) (eq (snd t) i)))
(def skelb (b)
  (if (eq (fst b) 2)
      (let ((f1 (appf b)))
        (if (and (isv (appa b) 0) (eq (fst f1) 2))
            (let ((f2 (appf f1)))
              (if (and (isv (appa f1) 1) (eq (fst f2) 2))
                  (let ((f3 (appf f2)))
                    (if (and (isv (appa f2) 2) (eq (fst f3) 2))
                        (let ((f4 (appf f3)))
                          (if (and (eq (fst (appa f3)) 1) (and (eq (fst f4) 2) (and (eq (fst (appf f4)) 12) (eq (snd (appf f4)) ID_CARRY))))
                              (certof (appa f4))
                              99))
                        99))
                  99))
            99))
      99))
(def bit (q) (if (eq (fst q) 4) (if (lt (snd q) 2) (snd q) 99) 99))
(def certof (c)
  (if (eq (fst c) 5)
      (let ((fn (bit (fst (snd c)))))
        (let ((r (fst (snd (snd c)))))
          (if (and (eq (fst r) 5) (lt fn 2))
              (let ((fp (bit (fst (snd r)))))
                (let ((pr (bit (fst (snd (snd r))))))
                  (if (and (lt fp 2) (lt pr 2)) (pair fn (pair fp pr)) 99)))
              99)))
      99))
(def FAKECARRY (cert fb me n p) (fb me n p))
"""

_LIB = {}


def install():
    """append the library entries once (idempotent); returns {name: index}."""
    if _LIB:
        return _LIB
    base = len(L.LIB)
    comp = L.SxCompiler()
    comp.load(CO_SRC)
    comp.consts['ID_CARRY'] = base + comp.order.index('CARRY')
    terms = comp.build(base)
    L.LIB.extend(terms)
    for i, n in enumerate(comp.order):
        L.LIBNAME[base + i] = n
        L.LIBIDX[n] = base + i
    L.LIBCODE.extend([L.compile_term(t[1]) for t in terms])
    _LIB.update({n: base + i for i, n in enumerate(comp.order)})
    _LIB['_c0code'] = L.LIBCODE[_LIB['CHK']]
    return _LIB


install()
ID_CARRY, ID_CHK, ID_FAKE = _LIB['CARRY'], _LIB['CHK'], _LIB['FAKECARRY']


# ---------------------------------------------------------------- host reference of the skeleton check (the C1 primitive's map)
def host_skel(t):
    """the certificate of the program term t, (fn, fp, pref), or None: the same map as the L_T^code `skel`."""
    try:
        if t[0] != 'lam' or t[1][0] != 'lam' or t[1][1][0] != 'lam':
            return None
        b = t[1][1][1]
        if b[0] != 'app' or b[2] != ('v', 0):
            return None
        f1 = b[1]
        if f1[0] != 'app' or f1[2] != ('v', 1):
            return None
        f2 = f1[1]
        if f2[0] != 'app' or f2[2] != ('v', 2):
            return None
        f3 = f2[1]
        if f3[0] != 'app' or f3[2][0] != 'lam':
            return None
        f4 = f3[1]
        if f4[0] != 'app' or f4[1] != ('lib', ID_CARRY):
            return None
        c = f4[2]
        if c[0] != 'pair' or c[1][0] != 'nat' or c[2][0] != 'pair' or c[2][1][0] != 'nat' or c[2][2][0] != 'nat':
            return None
        fn, fp, pr = c[1][1], c[2][1][1], c[2][2][1]
        if not all(type(v) is int and 0 <= v < 2 for v in (fn, fp, pr)):
            return None
        return (fn, fp, pr)
    except (IndexError, TypeError):
        return None


_HS = {}


def host_skel_cached(t):
    k = id(t)
    e = _HS.get(k)
    if e is not None and e[0] is t:
        return e[1]
    r = host_skel(t)
    _HS[k] = (t, r)
    return r


def _chk_c1(env):
    """C1 primitive: KAPPA ticks, then the skeleton map (same value as the C0 term)."""
    a = env[0]
    for _ in range(KAPPA):
        L.tick()
    if type(a) is not tuple or type(a[0]) is not L.Q:
        raise L.Stuck()
    c = host_skel_cached(a[0].t)
    if c is None:
        return 'F'
    return 'T' if (c[0] if a[1] == 0 else c[1]) == 1 else 'F'


MACHINE = ['C1']


def set_machine(m):
    """'C1' (fixed-cost primitive check) or 'C0' (the check written out in L_T^code)."""
    assert m in ('C1', 'C0')
    L.LIBCODE[ID_CHK] = _chk_c1 if m == 'C1' else _LIB['_c0code']
    L._compiled.clear()
    MACHINE[0] = m


set_machine('C1')


# ---------------------------------------------------------------- programs
def cert_term(fn, fp, pr):
    return ('pair', ('nat', fn), ('pair', ('nat', fp), ('nat', pr)))


def carrier_term(fn, fp, pr, fb_term, lib=None, swap=False):
    """lam me. lam n. lam p. (((((lib CARRY) CERT) FB) me) n) p."""
    head = ('app', ('app', ('lib', ID_CARRY if lib is None else lib), cert_term(fn, fp, pr)), fb_term)
    a, b, c = (('v', 2), ('v', 0), ('v', 1)) if swap else (('v', 2), ('v', 1), ('v', 0))
    body = ('app', ('app', ('app', head, a), b), c)
    return ('lam', ('lam', ('lam', body)))


def _base():
    cat = PA.CataloguePA()
    return cat


def library_co():
    """[(name, family, term, meta)] of the extended catalogue: queue 78's 59 programs (terms compiled from their sources) then the
    carriers.  meta = dict(cert=(fn, fp, pref) or None, fb=name of the fallback program or None)."""
    base = PA.library_pa()
    out = [(n, f, CT._prog(s), dict(cert=None, fb=None)) for n, f, s in base]
    T = {n: t for n, f, t, m in out}
    add = []
    add.append(('Ocn', 'c_open', (1, 0, 0), 'C1'))
    add.append(('Ocp', 'c_open', (0, 1, 1), 'C4'))
    firm = [n for n, f, s in base if f in ('single', 'two')]
    for fbn in firm:
        d = fbn[1]
        add.append(('Fc' + fbn, 'c_firm', (1, 1, 0 if d == 'n' else 1), fbn))
    add.append(('Rcn', 'c_acc', (1, 0, 0), 'C3'))
    add.append(('Rcp', 'c_acc', (0, 1, 1), 'C0'))
    add.append(('Rcsn', 'c_accs', (1, 0, 0), 'Rnn'))
    add.append(('Rcsp', 'c_accs', (0, 1, 1), 'Rpn'))
    add.append(('Bcn', 'c_bully', (1, 1, 0), 'Bn'))
    add.append(('Bcp', 'c_bully', (1, 1, 1), 'Bp'))
    for fbn in ('Pnzy', 'Pnzn', 'Ppzy', 'Ppzn'):
        add.append(('Pc' + fbn, 'c_prud', (1, 1, 0 if fbn[1] == 'n' else 1), fbn))
    for n, f, c, fbn in add:
        out.append((n, f, carrier_term(c[0], c[1], c[2], T[fbn]), dict(cert=c, fb=fbn)))
    return out


def forgers():
    """gate-only programs that try to pass as carriers.  [(name, term, note)]."""
    T = {n: t for n, f, t, m in library_co()}
    Bn = T['Bn']
    body_bn = Bn[1][1][1]
    out = []
    # milestone 4's carrier shape: (lam certs. BODY) CERTS, with the bully's body and Ocp's certificate data
    out.append(('XmBn', ('lam', ('lam', ('lam', ('app', ('lam', _shift(body_bn, 1, 0)), cert_term(0, 1, 1))))),
                'bully body with Ocp certificate data in milestone-4 shape'))
    out.append(('XfakeBn', carrier_term(0, 1, 1, Bn, lib=ID_FAKE), 'skeleton calling a lookalike combinator (ignores cert) with Ocp cert, bully fallback'))
    out.append(('XswapBn', carrier_term(1, 1, 0, Bn, swap=True), 'skeleton with n and p swapped'))
    out.append(('XappBn', carrier_term(1, 1, 0, ('app', ('lam', ('v', 0)), Bn)), 'fallback an application (not a value)'))
    bad = ('lam', ('lam', ('lam', ('app', ('app', ('app', ('app', ('app', ('lib', ID_CARRY), ('pair', ('nat', 2), ('pair', ('nat', 1), ('nat', 0)))), Bn),
                                                         ('v', 2)), ('v', 1)), ('v', 0)))))
    out.append(('XbitBn', bad, 'certificate flag 2 (malformed)'))
    opc = ('lam', ('lam', ('lam', ('app', ('app', ('app', ('app', ('app', ('lib', ID_CARRY),
                                                                 ('pair', ('op', 'add', ('nat', 0), ('nat', 1)), ('pair', ('nat', 1), ('nat', 0)))), Bn),
                                                         ('v', 2)), ('v', 1)), ('v', 0)))))
    out.append(('XopBn', opc, 'certificate computed (op), not a literal'))
    wrapped = ('lam', ('lam', ('lam', ('if', ('con', 'T'), carrier_term(1, 1, 0, Bn)[1][1][1], body_bn))))
    out.append(('XifBn', wrapped, 'skeleton under an if (semantically the carrier)'))
    out.append(('Xconst', ('lam', ('lam', ('lam', cert_term(1, 1, 0)))), 'returns certificate data as its value'))
    return out


def _shift(t, d, c):
    """shift free variables >= c of t by d."""
    tag = t[0]
    if tag == 'v':
        return ('v', t[1] + d) if t[1] >= c else t
    if tag in ('con', 'nat', 'quote', 'lib'):
        return t
    if tag in ('lam', 'fix'):
        return (tag, _shift(t[1], d, c + 1))
    if tag == 'op':
        return ('op', t[1], _shift(t[2], d, c), _shift(t[3], d, c))
    if tag == 'sim':
        return ('sim', t[1], _shift(t[2], d, c))
    return (tag,) + tuple(_shift(a, d, c) for a in t[1:])


FAM_CERT = ('c_open', 'c_firm', 'c_acc', 'c_accs', 'c_bully', 'c_prud')
FAMC = PA.FAMP + list(FAM_CERT)


class CatalogueCO(TP.Catalogue):
    def __init__(self, extra=None):
        lib = library_co()
        self.names = [x[0] for x in lib]
        self.fam = [x[1] for x in lib]
        self.terms = [x[2] for x in lib]
        self.meta = [x[3] for x in lib]
        if extra:
            for n, t, note in extra:
                self.names.append(n); self.fam.append('forger'); self.terms.append(t); self.meta.append(dict(cert=None, fb=None, note=note))
        self.K = len(self.names)
        self.idx = {n: i for i, n in enumerate(self.names)}

    def build_rows(self, rows, cols=None, fuel=CT.KR):
        """execution tables of programs `rows` against (next, prev) in cols x cols (default all)."""
        K = self.K
        cols = list(range(K)) if cols is None else cols
        out = {}
        for p in rows:
            code = np.zeros((K, K), np.int8); steps = np.zeros((K, K), np.int16)
            nto = np.zeros((K, K), np.int8); fo = np.zeros((K, K), np.int8); reg = np.zeros((K, K), np.int8)
            if self.fam[p] in ('const', 'junk_f', 'junk_r'):
                c, s, n, f, _ = TP.f_eval(self.terms[p], self.terms[0], self.terms[0], fuel)
                code[:] = c; steps[:] = s; nto[:] = n; fo[:] = f
            else:
                for n_ in cols:
                    for v_ in cols:
                        r0 = L.STATS['regress']
                        c, s, n, f, _ = TP.f_eval(self.terms[p], self.terms[n_], self.terms[v_], fuel)
                        code[n_, v_] = c; steps[n_, v_] = min(s, 32767); nto[n_, v_] = n; fo[n_, v_] = f
                        reg[n_, v_] = min(L.STATS['regress'] - r0, 127)
            out[p] = (code, steps, nto, fo, reg)
        return out


def _rows_job(arg):
    rows, machine, nforg = arg
    TP.install_counter()
    set_machine(machine)
    cat = CatalogueCO(extra=forgers()[:nforg] if nforg else None)
    return L.run_big(cat.build_rows, rows)


def build_tables_parallel(machine, workers=3, nforg=0):
    cat = CatalogueCO(extra=forgers()[:nforg] if nforg else None)
    K = cat.K
    heavy = [p for p in range(K) if cat.fam[p] not in ('const', 'junk_f', 'junk_r')]
    order = heavy[::-1] + [p for p in range(K) if p not in heavy]
    nch = max(1, workers * 6)
    chunks = [(order[i::nch], machine, nforg) for i in range(nch)]
    code = np.empty((K, K, K), np.int8); steps = np.empty((K, K, K), np.int16)
    nto = np.empty((K, K, K), np.int8); fo = np.empty((K, K, K), np.int8); reg = np.empty((K, K, K), np.int8)
    if workers > 1:
        import multiprocessing as mp
        with mp.get_context('fork').Pool(workers) as pool:
            parts = pool.map(_rows_job, chunks, chunksize=1)
    else:
        parts = [_rows_job(c) for c in chunks]
    for d in parts:
        for p, (c, s, n, f, g) in d.items():
            code[p] = c; steps[p] = s; nto[p] = n; fo[p] = f; reg[p] = g
    return code, steps, nto, fo, reg


def table_key(machine, nforg=0):
    cat = CatalogueCO(extra=forgers()[:nforg] if nforg else None)
    h = hashlib.md5()
    h.update(('|'.join(cat.names) + str(CT.KS) + str(CT.KR) + machine + str(KAPPA) + CO_SRC + 'co1').encode())
    for t in cat.terms:
        h.update(repr(t).encode())
    return h.hexdigest()[:12]


class TabsCO(TP.TabsPlus):
    """Execution tables of the extended catalogue under machine C1 (dynamics) or C0 (static checks) and the joint tables."""

    def __init__(self, cache_dir=None, machine='C1', workers=None, nforg=0):
        set_machine(machine)
        self.machine = machine
        self.cat = CatalogueCO(extra=forgers()[:nforg] if nforg else None)
        self.names = self.cat.names
        self.fam = self.cat.fam
        self.K = self.cat.K
        path = None
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
            path = os.path.join(cache_dir, 'co_%s_%s.npz' % (machine, table_key(machine, nforg)))
        if path and os.path.exists(path):
            z = np.load(path)
            self.code, self.steps, self.nto, self.fo, self.reg = z['code'], z['steps'], z['nto'], z['fo'], z['reg']
        else:
            nw = workers or int(os.environ.get('DAYTONA_CPUS', min(3, os.cpu_count() or 1)))
            self.code, self.steps, self.nto, self.fo, self.reg = build_tables_parallel(machine, nw, nforg)
            if path:
                tmp = path + '.%d.tmp.npz' % os.getpid()
                np.savez_compressed(tmp, code=self.code, steps=self.steps, nto=self.nto, fo=self.fo, reg=self.reg)
                os.replace(tmp, path)
        self._joint()


def check_value(machine, x_term, w):
    """evaluate CHK on (quote x, w) in the given machine: (value, steps)."""
    set_machine(machine)
    t = ('app', ('lib', ID_CHK), ('pair', ('quote', x_term), ('nat', w)))
    return L.run_big(L.evaluate, t, 10 ** 6)
