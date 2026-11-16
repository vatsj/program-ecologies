"""Queue 80: the catalogues (script world S, skeleton world K), the forgers, the S1 check table, and execution tables at (KR', cap').

World S (A arms, U):  queue 78's 59 programs at read cap cap' (sources rewritten), then the 100 script carriers of script_offers.s_carriers()
                      (10 families x 2 directions / fallbacks x 5 spellings).  K_S = 159.
World K (K, K2):      the same 59, then queue 79's skeleton carriers (canonical: Oc, Rc, Fc on Snoy / Spoy, Bc; 8) and four non-canonical
                      spellings of each (inl, rord, guard, alias), which queue 79's check CHK rejects.  K_K = 99.
Forgers (gates only, rows only): see forgers_s().
"""
import os, sys, hashlib, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import lt_code as L
import churn_primary_t as CT
import tplus as TP
import certified_offers as CO
import script_offers as S

NBASE = 59


def base_terms(cap):
    lib = S.base_library(cap)
    return [(n, f, S.prog(s)) for n, f, s in lib]


# ---------------------------------------------------------------- world S
def library_s(cap=None):
    """[(name, family, spelling, term, meta)] for world S at read cap `cap` (default cap')."""
    cap = cap or S.CAPP
    base = base_terms(cap)
    T = {n: t for n, f, t in base}
    out = [(n, f, '-', t, dict(carrier=False)) for n, f, t in base]
    for nm, fam, sp, prm in S.s_carriers():
        body = S.body_spelling(sp, prm['fn'], prm['fp'], prm['pf'], prm['H'], prm['R'], T[prm['fb']])
        term, scr = S.build_carrier(body, S.carrier_entries(prm))
        meta = dict(prm, carrier=True, script=scr, script_nodes=S.script_nodes(scr), term_nodes=S.term_nodes(term))
        out.append((nm, fam, sp, term, meta))
    return out


def forgers_s(cap=None):
    """[(name, term, note, expected)] gate-only programs in world S.  expected: the codes a sound checker may accept ('' = none);
    a forger whose statement is true may be accepted (marked)."""
    cap = cap or S.CAPP
    lib = {n: (f, sp, t, m) for n, f, sp, t, m in library_s(cap)}
    T = {n: v[2] for n, v in lib.items()}
    scr = {n: v[3].get('script') for n, v in lib.items()}
    Bn, C1t = T['Bn'], T['C1']
    out = []
    # queue 79's eight forgers, verbatim (no packaging: rejected for every code)
    for n, t, note in CO.forgers():
        out.append(('q79' + n, t, 'queue 79 forger: ' + note, ''))
    bodyB = Bn[1][1][1]
    # a valid script attached to a different program: Ocn.canon's script on the bully's body
    out.append(('XscrBn', S.package(bodyB, scr['Ocn.canon']), "Ocn's valid script on the simulating bully's body", ''))
    # Fc+'s full script (two offers and S_nx) on Bc's body with H = 1: the offers are true of Bc, S_nx is not
    bcb = S.body_spelling('canon', 1, 1, 0, 1, 0, Bn)
    out.append(('XnxBc', S.package(bcb, scr['Fc+Snoy.canon']), "Fc+'s script (offers and S_nx) on Bc's body with H = 1", '1234'))
    # a lookalike library rule that ignores the certificate (plays the bully fallback) with Bcn's script
    fake = S._app(('lib', S.ID_FAKE), S.cert_lit(1, 1, 0, 0, 0), Bn, S.ME, S.NX_, S.PV)
    out.append(('XfakeBc', S.package(fake, scr['Bcn.canon']), "FAKEOFFER (ignores the certificate) with Bcn's script", ''))
    # swapped n and p in the canonical call, with the unswapped script
    sw = S._app(('lib', S.ID_OFFER), S.cert_lit(1, 1, 0, 0, 0), Bn, S.ME, S.PV, S.NX_)
    out.append(('XswapBc', S.package(sw, scr['Bcn.canon']), 'n and p swapped in the canonical call, unswapped script', ''))
    # S_nx on a program that names 2/3 only when fuel runs out: Oc+n whose fallback reads next with cap KR' (the read can exhaust
    # the root fuel; then the root plays 8), carrying the script derived for Oc+n's honest fallback
    fbx = S.prog('(lambda (me n p) (let ((r (capk %d (run %d n p) me))) 1))' % (S.KRP, S.KRP))
    fbh = S.prog('(lambda (me n p) (let ((r (capk %d (run %d n p) me))) 1))' % (cap, cap))
    hb = S.body_spelling('canon', 1, 0, 0, 1, 0, fbh)
    _, hscr = S.build_carrier(hb, S.carrier_entries(dict(fn=1, fp=0, pf=0, H=1, R=0, nx=True)))
    xb = S.body_spelling('canon', 1, 0, 0, 1, 0, fbx)
    out.append(('XfuelOc', S.package(xb, hscr), 'S_nx script on a program that names 2/3 only when its read exhausts the root fuel', '12'))
    # a derivation that asserts an atom (unknown node kind 3) and one that prunes (VAC) a branch where the guard can hold
    bcn = S.body_spelling('canon', 1, 1, 0, 0, 0, Bn)
    pr = (0, (0, (1, (1, 0))))
    out.append(('XassumeBc', S.package(bcn, S.cons([(1, (pr, (3, ((0, 3), (2, (0, 0))))))])), 'a tree node asserting an atom value', ''))
    out.append(('XvacBc', S.package(bcn, S.cons([(1, (pr, (1, ((2, 0), (2, 0)))))])), 'VAC on a branch where the guard can hold', ''))
    # passes S_off(next) syntactically but names prev when next is eligible and preferred (E = {next}: names prev)
    tw = ('app', ('lam', ('app', ('lam', ('if', ('v', 1), ('if', ('v', 0), ('nat', 1), ('nat', 4)), ('if', ('v', 0), ('nat', 4),
          S._app(Bn, ('v', 4), ('v', 3), ('v', 2))))),
          S._elig_inline(('v', 1), 1, 0))), S._elig_inline(('v', 1), 3, 0))
    out.append(('XwrongBc', S.package(tw, scr['Bcn.inl']), 'names prev when next is the preferred eligible partner (E = {next})', '34'))
    # malformed scripts: a requirement flag 2 in the params; a computed (op) script; a bad tree node
    out.append(('XbadR', S.package(bcn, S.cons([(1, ((2, (0, (1, (1, 0)))), (0, 0)))])), 'requirement flag 2 (malformed)', ''))
    out.append(('XopScr', ('lam', ('lam', ('lam', ('if', ('con', 'T'), bcn, ('op', 'add', ('nat', 0), ('nat', 1)))))),
                'script computed by an op term', ''))
    # self-certification and identity: the body calls CHKS on its own quote / compares n with me
    selfc = ('if', S._chks(S.ME, 5), ('nat', 1), ('nat', 4))
    out.append(('XselfC', S.package(selfc, S.cons([(3, (0, (0, 0)))])), 'calls CHKS on its own quote', '5'))
    ident = ('if', ('eq', S.NX_, S.ME), ('nat', 2), ('nat', 1))
    out.append(('XidC', S.package(ident, S.cons([(3, (0, (0, 0))), (1, ((0, (0, (1, (0, 0)))), (0, 0)))])), 'identity test eq n me', '125'))
    # a recursive body (fix) and a body that inspects the partner's quote
    fx = ('app', ('fix', ('lam', ('nat', 1))), ('nat', 0))
    out.append(('XfixC', S.package(fx, S.cons([(3, (0, (0, 0)))])), 'body uses fix', '5'))
    insp = ('if', ('eq', ('fst', S.NX_), ('nat', 1)), ('nat', 2), ('nat', 1))
    out.append(('XinspC', S.package(insp, S.cons([(3, (0, (0, 0)))])), "body inspects the partner's quote (fst n)", ''))
    # a constant that always names next at 1/2, carrying a trivial S_off(next) tree: its statement is true (may be accepted)
    out.append(('XconstC1', S.package(('nat', 1), S.cons([(1, ((0, (0, (1, (0, 0)))), (0, 0))), (3, (0, (0, 0)))])),
                'the 1/2 constant naming next with a one-leaf tree (true statements)', '125'))
    return out


# ---------------------------------------------------------------- world K
def _k_body(sp, fn, fp, pf, fb):
    me, n, p = S.ME, S.NX_, S.PV
    chk = lambda x, w: ('app', ('lib', CO.ID_CHK), ('pair', x, ('nat', w)))
    if sp == 'guard':
        skel = CO.carrier_term(fn, fp, pf, fb)[1][1][1]
        return ('if', ('con', 'T'), skel, ('nat', 0))
    if sp in ('inl', 'alias'):
        d = 1 if sp == 'alias' else 0      # alias: (let ((chk (lib CHK))) ...) -- the check through a let-bound name
        sh = lambda x, k: CO._shift(x, k, 0)
        def ck(x, w, depth):
            if sp == 'alias':
                return ('app', ('v', depth), ('pair', x, ('nat', w)))
            return chk(x, w)
        en = ck(sh(n, d), 1, 0) if fn else ('con', 'F')
        ep = ck(sh(p, d + 1), 0, 1) if fp else ('con', 'F')
        fall = S._app(fb, sh(me, d + 2), sh(n, d + 2), sh(p, d + 2))
        inner = ('if', ('v', 1), ('if', ('v', 0), ('nat', 1 if pf == 0 else 4), ('nat', 1)), ('if', ('v', 0), ('nat', 4), fall))
        body = S._let(en, S._let(ep, inner))
        return S._let(('lib', CO.ID_CHK), body) if sp == 'alias' else body
    if sp == 'rord':
        ep = chk(p, 0) if fp else ('con', 'F')
        en = chk(CO._shift(n, 1, 0), 1) if fn else ('con', 'F')
        fall = S._app(fb, CO._shift(me, 2, 0), CO._shift(n, 2, 0), CO._shift(p, 2, 0))
        inner = ('if', ('v', 1), ('if', ('v', 0), ('nat', 1 if pf == 0 else 4), ('nat', 4)), ('if', ('v', 0), ('nat', 1), fall))
        return S._let(ep, S._let(en, inner))
    raise ValueError(sp)


K_SPELLINGS = ('canon', 'inl', 'rord', 'guard', 'alias')
K_FAMS = [('Oc', 'k_open', [('n', (1, 0, 0, 'C1')), ('p', (0, 1, 1, 'C4'))]),
          ('Rc', 'k_acc', [('n', (1, 0, 0, 'C3')), ('p', (0, 1, 1, 'C0'))]),
          ('Fc', 'k_firm', [('Snoy', (1, 1, 0, 'Snoy')), ('Spoy', (1, 1, 1, 'Spoy'))]),
          ('Bc', 'k_bully', [('n', (1, 1, 0, 'Bn')), ('p', (1, 1, 1, 'Bp'))])]


def library_k(cap=None):
    cap = cap or S.CAPP
    base = base_terms(cap)
    T = {n: t for n, f, t in base}
    out = [(n, f, '-', t, dict(carrier=False)) for n, f, t in base]
    for pre, fam, dirs in K_FAMS:
        for d, (fn, fp, pf, fbn) in dirs:
            for sp in K_SPELLINGS:
                if sp == 'canon':
                    term = CO.carrier_term(fn, fp, pf, T[fbn])
                else:
                    term = ('lam', ('lam', ('lam', _k_body(sp, fn, fp, pf, T[fbn]))))
                out.append(('%s%s.%s' % (pre, d, sp), fam, sp, term,
                            dict(carrier=True, fn=fn, fp=fp, pf=pf, fb=fbn, cert=(fn, fp, pf) if sp == 'canon' else None,
                                 term_nodes=S.term_nodes(term))))
    return out


# ---------------------------------------------------------------- the S1 table
def s1_table(terms, workers=1):
    """{(canon, code): (value, S0 ticks)} for every term and code 1..5 (rejections included)."""
    out = {}
    for t in terms:
        cn = L.canon_term(t)
        for c in range(1, 6):
            v, cost = S.core_s0(t, c)
            if v not in ('T', 'F'):
                v = 'BOT'
            out[(cn, c)] = (v, int(cost))
    return out


def install_s1(table):
    S.S1TAB.clear(); S.S1TAB.update(table); S._S1ID.clear()


# ---------------------------------------------------------------- execution tables
class Cat:
    def __init__(self, world, cap=None, forg=False):
        cap = cap or S.CAPP
        lib = library_s(cap) if world == 'S' else library_k(cap)
        self.world = world
        self.cap = cap
        self.names = [x[0] for x in lib]
        self.fam = [x[1] for x in lib]
        self.spell = [x[2] for x in lib]
        self.terms = [x[3] for x in lib]
        self.meta = [x[4] for x in lib]
        self.K = len(lib)
        self.nforg = 0
        if forg:
            assert world == 'S'
            for n, t, note, exp in forgers_s(cap):
                self.names.append(n); self.fam.append('forger'); self.spell.append('-'); self.terms.append(t)
                self.meta.append(dict(carrier=False, note=note, expected=exp))
                self.nforg += 1
        self.Kc = self.K
        self.K = len(self.names)
        self.idx = {n: i for i, n in enumerate(self.names)}

    def key(self, machine, fuel, extra=''):
        h = hashlib.md5()
        h.update(('|'.join(self.names) + '|%s|%d|%d|%s|%s|%s' % (self.world, self.cap, fuel, machine, 'on', extra)).encode())
        h.update(S.CHK_SRC.encode()); h.update(CO.CO_SRC.encode())
        h.update(('%d|%d|%d' % (S.KCHK, S.WCHK, S.KRP)).encode())
        for t in self.terms:
            h.update(repr(t).encode())
        return h.hexdigest()[:12]

    def eval_row(self, p, cols, fuel):
        K = len(cols)
        code = np.zeros((K, K), np.int8); steps = np.zeros((K, K), np.int32)
        nto = np.zeros((K, K), np.int8); fo = np.zeros((K, K), np.int8)
        if self.fam[p] in ('const', 'junk_f', 'junk_r'):
            c, s, n, f, _ = TP.f_eval(self.terms[p], self.terms[0], self.terms[0], fuel)
            code[:] = c; steps[:] = s; nto[:] = n; fo[:] = f
            return code, steps, nto, fo
        for i, n_ in enumerate(cols):
            for j, v_ in enumerate(cols):
                c, s, n, f, _ = TP.f_eval(self.terms[p], self.terms[n_], self.terms[v_], fuel)
                code[i, j] = c; steps[i, j] = s; nto[i, j] = min(n, 127); fo[i, j] = f
        return code, steps, nto, fo


_W = {}


def _init_worker(world, cap, forg, machine, s1tab, regress, fuel):
    TP.install_counter()
    S.set_regress(regress)
    if s1tab is not None:
        install_s1(s1tab)
    _W['cat'] = Cat(world, cap, forg)
    _W['fuel'] = fuel
    if world == 'S':
        S.set_machine(machine)
    else:
        S.set_machine('S1' if s1tab is not None else 'S0')
        CO.set_machine('C1')


def _row_job(arg):
    rows, cols = arg
    cat = _W['cat']
    out = {}
    t0 = time.time()

    def go():
        for p in rows:
            out[p] = cat.eval_row(p, cols, _W['fuel'])
    L.run_big(go)
    return out, time.time() - t0


def build_tables(world, machine='S1', cap=None, fuel=None, forg=False, workers=3, s1tab=None, regress=True, rows=None,
                 cols=None, nchunks=None, log=None):
    """execution tables (code, steps, nto, fo) [rows x cols x cols] for the catalogue of `world` (forgers as rows only)."""
    cap = cap or S.CAPP
    fuel = fuel or 3 * cap
    cat = Cat(world, cap, forg)
    K = cat.K
    Kc = cat.Kc
    cols = list(range(Kc)) if cols is None else cols
    rows = list(range(K)) if rows is None else rows
    heavy = [p for p in rows if cat.fam[p] not in ('const', 'junk_f', 'junk_r')]
    order = heavy[::-1] + [p for p in rows if p not in heavy]
    nch = nchunks or max(1, workers * (24 if machine == 'S0' else 8))
    chunks = [(order[i::nch], cols) for i in range(nch)]
    chunks = [c for c in chunks if c[0]]
    import multiprocessing as mp
    t0 = time.time()
    parts = []
    with mp.get_context('fork').Pool(workers, initializer=_init_worker, maxtasksperchild=1,
                                      initargs=(world, cap, forg, machine, s1tab, regress, fuel)) as pool:
        for i, (d, w) in enumerate(pool.imap_unordered(_row_job, chunks)):
            parts.append(d)
            if log:
                log('chunk %d/%d done (%.0fs, wall %.0fs)' % (i + 1, len(chunks), w, time.time() - t0))
    Kr = K
    code = np.zeros((Kr, len(cols), len(cols)), np.int8); steps = np.zeros(code.shape, np.int32)
    nto = np.zeros(code.shape, np.int8); fo = np.zeros(code.shape, np.int8)
    for d in parts:
        for p, (c, s, n, f) in d.items():
            code[p] = c; steps[p] = s; nto[p] = n; fo[p] = f
    return cat, code, steps, nto, fo
