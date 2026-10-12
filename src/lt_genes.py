"""The realizable language, milestone 5: certificates as genes (specs/2026-10-11-certificates-as-genes.md;
notes/certificates-as-genes.md; predictions/2026-10-11-certificates-as-genes.md).

Built on src/lt_code.py, src/lt_cert.py and src/carrier_populations.py (imported, not modified).

Parts:
  1. the library extension: PROD / PCORE, the frozen production tactic of milestone 4 §1.9 written in L_T^code
     (appended after milestone 4's entries; every earlier index unchanged);
  2. programs as gene triples (code, mode, list): the mode as a no-op marker in the quote, canonical lists;
  3. the production modes H, S, C, CS and the encounter (play, then production in the residual budget), executed
     by the term with exact step counts; the pre-play and reserved allocations (tests and single-pair tables only);
  4. the named single-pair catalogue.
The population tables over units (dt, Cseq, Dseq) are in src/lt_genes_pop.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C

N, P = L.N, L.P
C_, D_, T_, F_, TO_ = L.C_, L.D_, L.T_, L.F_, L.TO_

# ----------------------------------------------------------------------------------------------------------------
# 1. The library extension: the production tactic as code
# ----------------------------------------------------------------------------------------------------------------
# PROD arg = (P . ad), ad = (V . (t . (m . (a . K)))) as a check argument.  PCORE runs milestone 4's frozen tactic on
# the root ψ = <t ⌜t⌝ ⌜m⌝, K>⇓a with hypothesis boxes R = (8 . (CHK_S . ad)), S = (8 . (CHK_S . swap ad)).  tac returns
# (node-or-NONE . count); the count threads the 64-node bound exactly as the host Producer's global counter.
GENE_SRC = r"""
(def PROD (arg) (capk (fst arg) PCORE (snd arg)))
(def PCORE (ad) (pcore 0 ad))
(def pcore (x ad)
  (let ((n (wrapid x)) (R (pair 8 (pair n ad))) (S (pair 8 (pair n (swaparg ad))))
        (r (snd ad)) (t (fst r)) (m (fst (snd r))) (a (fst (snd (snd r)))) (K (snd (snd (snd r))))
        (cx (pair x (pair R (pair S (fst ad)))))
        (res (tac cx 0 (pair (mkatom (mkconf t m) K a 0) 0) 0)))
    (fst res)))
(def mknode (r j ps) (pair r (pair j ps)))
(def tac (cx L R c)
  (if (lt 63 c) (pair NONE (add c 1))
    (let ((c1 (add c 1)))
      (if (caxiom L R) (pair (mknode 0 0 0) c1)
        (let ((h (thyp cx R 0)))
          (if (not (eq h NONE)) (pair (mknode 3 h 0) c1)
            (let ((rn (tneg cx L 0)))
              (if (not (eq rn NONE)) (pair (mknode 2 rn 0) c1)
                (let ((ru (tpos cx R 0)))
                  (if (not (eq ru NONE)) (pair (mknode 1 ru 0) c1)
                    (tatom cx L R R 0 c1)))))))))))
(def thypok (cx b)
  (let ((x (fst cx)))
    (cond ((eq x 3) F)
          ((eq b (fst (snd cx))) T)
          ((eq x 2) F)
          (else (eq b (fst (snd (snd cx))))))))
(def thyp (cx l j)
  (if (eq l 0) NONE
    (let ((b (fst l)))
      (if (and (eq (fst b) 8) (thypok cx b)) j (thyp cx (snd l) (add j 1))))))
(def trunnable (cx b)
  (and (eq (fst b) 8)
       (and (not (eq b (fst (snd cx))))
            (and (not (eq b (fst (snd (snd cx)))))
                 (le (snd (snd (snd cx))) (fst (snd (snd b))))))))
(def tcheck (b) (let ((p (snd b))) (callcheck (fst p) (snd p))))
(def tneg (cx l j)
  (if (eq l 0) NONE
    (let ((b (fst l)))
      (if (and (trunnable cx b) (not (eq (tcheck b) T))) j (tneg cx (snd l) (add j 1))))))
(def tpos (cx l j)
  (if (eq l 0) NONE
    (let ((b (fst l)))
      (if (and (trunnable cx b) (eq (tcheck b) T)) j (tpos cx (snd l) (add j 1))))))
(def tatom (cx L R l j c)
  (if (eq l 0) (pair NONE c)
    (let ((x (fst l)))
      (if (not (eq (fst x) 6)) (tatom cx L R (snd l) (add j 1) c)
        (let ((p (snd x)) (conf (fst p)) (f (fst (snd p))) (a (fst (snd (snd p)))) (m (snd (snd (snd p))))
              (r (cstep conf)))
          (if (and (lt 0 f) (eq (fst r) 2))
              (let ((q (tac cx L (fadd (evfrom r f a m) (fdel x R)) c)))
                (if (eq (fst q) NONE) q (pair (mknode 26 j (pair (fst q) 0)) (snd q))))
              (let ((s (chkstate conf f a)))
                (if (eq s 0) (pair NONE c)
                  (let ((B (fst s)) (Rx (fdel x R))
                        (q1 (tac cx (fadd B L) (fadd (fst (snd s)) Rx) c)))
                    (if (eq (fst q1) NONE) q1
                      (let ((q2 (tac cx L (fadd B (fadd (snd (snd s)) Rx)) (snd q1))))
                        (if (eq (fst q2) NONE) q2
                          (pair (mknode 25 j (pair (fst q1) (pair (fst q2) 0))) (snd q2))))))))))))))
"""
PCORE_ID_CODE = 30          # id under which PCORE is registered in lt_code.CORE_LIBS (deterministic: cached runs)
NONE_V = L.LIB_CONSTS['NONE']


def build_gene_library():
    """lt_cert.build_library with GENE_SRC appended: milestone 3's and 4's indices unchanged (asserted)."""
    before = dict(L.LIBIDX)
    comp = L.SxCompiler()
    for k, v in L.LIB_CONSTS.items(): comp.consts[k] = v
    for k, v in C.CERT_CONSTS.items(): comp.consts[k] = v
    comp.load(L.LIBRARY_SRC)
    comp.load(C.CERT_SRC)
    comp.load(GENE_SRC)
    for nm in C.WRAP_NAMES: comp.consts['ID_' + nm] = comp.order.index(nm)
    comp.consts['NLIB'] = len(comp.order)
    terms = comp.build(0)
    L.LIB[:] = terms
    L.LIBNAME.clear(); L.LIBNAME.update({i: n for i, n in enumerate(comp.order)})
    L.LIBIDX.clear(); L.LIBIDX.update(comp.index)
    for nm, i in before.items():
        assert L.LIBIDX[nm] == i, nm
    L.SEARCH_LIBS.clear(); L.SEARCH_LIBS.update({L.LIBIDX['SEARCH%d' % i]: i for i in range(3)})
    L.CORE_LIBS.clear(); L.CORE_LIBS.update({L.LIBIDX['CORE%d' % i]: i for i in range(3)})
    for nm, mode in C.CORE_NAMES.items(): L.CORE_LIBS[L.LIBIDX[nm]] = C.CORE_ID_BASE + mode
    L.CORE_LIBS[L.LIBIDX['PCORE']] = PCORE_ID_CODE
    L._compiled.clear()
    L.LIBCODE[:] = [L.compile_term(t[1]) for t in terms]
    L.CACHE.clear()
    C.ID.clear(); C.ID.update({nm: L.LIBIDX[nm] for nm in C.WRAP_NAMES})
    C.WRAPS.clear(); C.WRAPS.update(C.ID.values())
    C.CC_MODE.clear(); C.CC_MODE.update({L.LIBIDX[nm]: mode for nm, mode in C.CORE_NAMES.items()})
    C.WRAP_MODE.clear(); C.WRAP_MODE.update({L.LIBIDX[C.MODE_WRAP[m]]: m for m in C.MODE_WRAP})
    return comp


_COMP = build_gene_library()
PROD_ID = L.LIBIDX['PROD']
PCORE_LIB = L.LIBIDX['PCORE']

# ----------------------------------------------------------------------------------------------------------------
# 2. Programs as gene triples
# ----------------------------------------------------------------------------------------------------------------
MODES = ('H', 'S', 'C', 'CS')
MODE_NUM = {m: i for i, m in enumerate(MODES)}
MODE_BASE = 9100
TAG_BASE = 9000          # the identity run's tag markers (⟨9000 + t⟩)


def shift(t, d=1, c=0):
    """Shift the free de Bruijn variables (index >= c) of a term by d.  Quotes and data are closed."""
    tag = t[0]
    if tag == 'v': return ('v', t[1] + d) if t[1] >= c else t
    if tag in ('con', 'nat', 'quote', 'lib'): return t
    if tag in ('lam', 'fix'): return (tag, shift(t[1], d, c + 1))
    if tag == 'op': return ('op', t[1], shift(t[2], d, c), shift(t[3], d, c))
    if tag == 'sim': return ('sim', t[1], shift(t[2], d, c))
    return (tag,) + tuple(shift(a, d, c) for a in t[1:])


def mark(body, n):
    """A no-op marker let around a body (inside λme.λthem.λcerts): (λ_. body↑) ⟨n⟩."""
    return ('app', ('lam', shift(body, 1)), ('nat', n))


def marked_body(body, mode=None, tags=()):
    """The body with tag markers (inner) and the mode marker (outermost)."""
    b = body
    for t in sorted(tags, reverse=True):
        b = mark(b, TAG_BASE + t)
    if mode is not None:
        b = mark(b, MODE_BASE + MODE_NUM[mode])
    return b


def canon_list(cseq, dseq):
    """The canonical certificate list: the C block then the D block (each in acquisition order)."""
    return C.cons([('C', s) for s in cseq] + [('D', s) for s in dseq])


def split_list(lst):
    ents = C.uncons(lst) if lst != 0 else []
    return tuple(e[1] for e in ents if e[0] == 'C'), tuple(e[1] for e in ents if e[0] == 'D')


class Prog:
    """A gene triple.  body: the unmarked carrier body (inside λme.λthem.λcerts, them = v1, me = v2); mode in MODES;
    cseq, dseq: the blocks (scripts as host data); anc: ancestry tags per entry ('host' | 'search'), parallel to
    cseq + dseq; tags: identity-run tag markers carried by the source; name for reports."""
    __slots__ = ('name', 'body', 'mode', 'cseq', 'dseq', 'anc', 'tags', '_term')

    def __init__(self, name, body, mode, cseq=(), dseq=(), anc=None, tags=()):
        self.name, self.body, self.mode = name, body, mode
        self.cseq, self.dseq = tuple(cseq), tuple(dseq)
        self.anc = tuple(anc) if anc is not None else tuple(['host'] * (len(self.cseq) + len(self.dseq)))
        self.tags = tuple(tags)
        self._term = None

    def term(self):
        if self._term is None:
            self._term = C.carrier(marked_body(self.body, self.mode, self.tags), canon_list(self.cseq, self.dseq))
        return self._term

    def with_list(self, cseq, dseq, anc=None):
        return Prog(self.name, self.body, self.mode, cseq, dseq, anc, self.tags)

    def single(self, a, s):
        """x_s: this code and mode carrying only (a, s)."""
        return Prog(self.name + '_s', self.body, self.mode, (s,) if a == 'C' else (), (s,) if a == 'D' else (),
                    None, self.tags)

    def holds(self, a, s):
        return s in (self.cseq if a == 'C' else self.dseq)

    def entries(self):
        return [('C', s) for s in self.cseq] + [('D', s) for s in self.dseq]

    def __repr__(self):
        return '%s[%s|%dC,%dD]' % (self.name, self.mode, len(self.cseq), len(self.dseq))


def data_size(d):
    """Encoded nodes of a data value (pairs, naturals, constructors): the quote-surgery charge of a new list."""
    if isinstance(d, tuple): return 1 + data_size(d[0]) + data_size(d[1])
    return 1


# ----------------------------------------------------------------------------------------------------------------
# 3. Production acts, executed by the term, and the encounter
# ----------------------------------------------------------------------------------------------------------------
def run_wrapper(tm, fuel):
    """Evaluate a closed wrapper call from a fresh context with global fuel `fuel`: (value, steps, timed_out)."""
    v, n = L.evaluate(tm, fuel)
    if v == 'BOT': return None, n, True
    return v, n, False


def chk_call(t_term, q_term, a, V, K):
    return ('app', ('lib', C.ID['CHKS']), C.mk_arg(V, t_term, q_term, a, K))


def prod_call(t_term, q_term, a, V, K, Pcap):
    return ('app', ('lib', PROD_ID), P(N(Pcap), C.mk_arg(V, t_term, q_term, a, K)))


def check_term(t_term, q_term, a, V, K, fuel):
    """A sound check call CHK(t, q, a): ('T' | 'F' | None on fuel exhaustion, steps)."""
    v, n, to = run_wrapper(chk_call(t_term, q_term, a, V, K), fuel)
    return (None if to else v), n


def produce_term(t_term, q_term, a, V, K, Pcap, fuel):
    """PROD(P; t, q, a) by the term: (script data | None, steps, outcome) outcome in {'found', 'none', 'capTO',
    'fuelTO'}."""
    v, n, to = run_wrapper(prod_call(t_term, q_term, a, V, K, Pcap), fuel)
    if to: return None, n, 'fuelTO'
    if v == 'TO': return None, n, 'capTO'
    if v == NONE_V: return None, n, 'none'
    return v, n, 'found'


class Acct:
    """Steps and events of one side's production in one encounter."""
    def __init__(self):
        self.steps = {'gate': 0, 'prodC': 0, 'prodD': 0, 'ac': 0, 'surgery': 0}
        self.events = []          # (kind, outcome, steps, detail)
        self.adopted = []         # (a, script, how)
        self.timeouts = 0

    def total(self):
        return sum(self.steps.values())


def produce_side(x, y, mode, K, V, Pcap, fuel, publish=True, negcache=None, acct=None, rule='lack'):
    """x's mode procedure after a play against y (quotes as of the encounter).  Returns (new Prog, Acct).
    negcache: optional set of (a, script, y-term-id) refused before (single-pair tables only; the dynamics do not
    cache)."""
    acct = acct or Acct()
    cseq, dseq, anc = list(x.cseq), list(x.dseq), list(x.anc)
    xt, yt = x.term(), y.term()
    rem = fuel

    def charge(kind, n):
        nonlocal rem
        acct.steps[kind] += n; rem -= n

    cur = x
    adopted_out = set()
    if mode in ('C', 'CS') and publish:
        yanc = dict(zip(y.entries(), y.anc))
        for (a, s) in y.entries():
            if a in adopted_out or (s in (cseq if a == 'C' else dseq)):
                continue
            if rule == 'lack' and (cseq if a == 'C' else dseq):
                continue
            key = (a, s, id(yt) if a == 'C' else 'D')
            if negcache is not None and key in negcache:
                acct.events.append(('ac', 'cached', 0, a)); continue
            xs = x.single(a, s)
            sc = data_size(canon_list(xs.cseq, xs.dseq)) + 5
            charge('surgery', sc)
            if rem <= 0:
                acct.timeouts += 1; acct.events.append(('ac', 'fuelTO', 0, a)); break
            q = yt if a == 'C' else L.PROG_D
            v, n = check_term(xs.term(), q, a, V, K, rem)
            charge('ac', n)
            if v is None:
                acct.timeouts += 1; acct.events.append(('ac', 'fuelTO', n, a)); break
            acct.events.append(('ac', v, n, a))
            if v == 'T':
                if a == 'C': cseq.append(s); anc.insert(len(cseq) - 1, yanc.get((a, s), 'host'))
                else: dseq.append(s); anc.append(yanc.get((a, s), 'host'))
                adopted_out.add(a); acct.adopted.append((a, s, 'copy'))
            elif negcache is not None:
                negcache.add(key)
        cur = x.with_list(cseq, dseq, anc)
    if mode in ('S', 'CS'):
        xt = cur.term()
        if rule == 'lack':
            v = 'T' if cseq else 'F'
        else:
            v, n = check_term(xt, yt, 'C', V, K, rem)
            charge('gate', n)
            if v is None:
                acct.timeouts += 1; acct.events.append(('gate', 'fuelTO', n, 'C'))
                return cur, acct
            acct.events.append(('gate', v, n, 'C'))
        if v != 'T':
            s, n, oc = produce_term(xt, yt, 'C', V, K, Pcap, rem)
            charge('prodC', n)
            acct.events.append(('prodC', oc, n, 'C'))
            if oc == 'fuelTO': acct.timeouts += 1
            if s is not None and s not in cseq:
                cseq.append(s); anc.insert(len(cseq) - 1, 'search'); acct.adopted.append(('C', s, 'search'))
            cur = cur.with_list(cseq, dseq, anc)
        if not dseq and rem > 0:
            xt = cur.term()
            s, n, oc = produce_term(xt, L.PROG_D, 'D', V, K, Pcap, rem)
            charge('prodD', n)
            acct.events.append(('prodD', oc, n, 'D'))
            if oc == 'fuelTO': acct.timeouts += 1
            if s is not None:
                dseq.append(s); anc.append('search'); acct.adopted.append(('D', s, 'search'))
            cur = cur.with_list(cseq, dseq, anc)
    return cur, acct


def play_side(x, y, K):
    a, n = L.play(x.term(), y.term(), K)
    return ('D' if a == 'BOT' else a), n, a == 'BOT'


def encounter(x, y, K, V, Pcap, alloc='post', publish=True, negcache=(None, None), self_play=False, reserve=0, rule='lack'):
    """One encounter.  alloc 'post' (main): plays at fuel K, then each side's production in its residual; 'pre'
    (F0 demonstration): production first in K, then the play at the remaining fuel.  Returns dict with actions, play
    steps, Accts and the updated programs.  self_play: x and y are the same individual's quote (one production)."""
    out = {}
    if alloc == 'post':
        ax, wx, bx = play_side(x, y, K)
        ay, wy, by = (ax, wx, bx) if self_play else play_side(y, x, K)
        nx, accx = produce_side(x, y, x.mode, K, V, Pcap, K - wx, publish, negcache[0], rule=rule)
        if self_play:
            ny, accy = nx, accx
        else:
            ny, accy = produce_side(y, x, y.mode, K, V, Pcap, K - wy, publish, negcache[1], rule=rule)
    elif alloc == 'pre':
        nx, accx = produce_side(x, y, x.mode, K, V, Pcap, K, publish, negcache[0], rule=rule)
        ny, accy = (nx, accx) if self_play else produce_side(y, x, y.mode, K, V, Pcap, K, publish, negcache[1], rule=rule)
        ax, wx, bx = play_side(x, y, K - accx.total())
        ay, wy, by = (ax, wx, bx) if self_play else play_side(y, x, K - accy.total())
    elif alloc == 'reserved':
        # sources and checks are at K (= K_play); production first with its own reserve R, the play gets
        # K + (R - production steps) >= K, so every accepted atom about the fuel-K play holds (notes §1.2)
        nx, accx = produce_side(x, y, x.mode, K, V, Pcap, reserve, publish, negcache[0], rule=rule)
        ny, accy = (nx, accx) if self_play else produce_side(y, x, y.mode, K, V, Pcap, reserve, publish, negcache[1], rule=rule)
        ax, wx, bx = play_side(x, y, K + reserve - accx.total())
        ay, wy, by = (ax, wx, bx) if self_play else play_side(y, x, K + reserve - accy.total())
    else:
        raise ValueError(alloc)
    out.update(ax=ax, ay=ay, wx=wx, wy=wy, botx=bx, boty=by, accx=accx, accy=accy, nx=nx, ny=ny)
    return out


# ----------------------------------------------------------------------------------------------------------------
# 4. The named single-pair catalogue
# ----------------------------------------------------------------------------------------------------------------
def named_bodies(V, K, k=None):
    k = K // 2 if k is None else k
    b = {nm: f(0, V, K) for nm, f in C.CARRIER_BODIES.items()}
    for nm in ('CB1r', 'CBPh', 'CBPr', 'CBlet2', 'CBw2', 'CB1h'):
        b[nm] = C.HELDOUT_BODIES[nm](0, V, K)
    b['LobC'] = C.body_LobC(0, V, K)
    b['CBdef'] = C.body_CBdef(0, V, K)
    b['Cc'] = C.C_
    b['Dc'] = C.D_
    b['SFc'] = C.body_SFc(k)
    return b


_PROBES = {}


def probes(K, V):
    """Milestone 2's production probes (milestone 4's CB, CB1, CBP with their own lists), unmarked."""
    key = (K, V)
    if key not in _PROBES:
        import carrier_populations as CP
        prod = C.Producer(host=CP.ExactHost())
        _PROBES[key] = (prod, CP.make_probes(prod, 0, K, V))
    return _PROBES[key]


def host_list(body, K, V, mode='H', tags=()):
    """The H list of a body: milestone 2's frozen production (D script vs ⌜D⌝, C scripts vs the probes), produced
    for the marked program (mode marker and tags)."""
    prod, pr = probes(K, V)
    mk = lambda certs: C.carrier(marked_body(body, mode, tags), certs)
    lst, _ = C.produce_list(prod, 0, mk, pr, K, V)
    return split_list(lst)


def named_catalogue(K, V, k=None):
    """Named programs (bodies with their H lists).  Returns {name: (body, cseq, dseq, tags, kind)} where kind is
    'carrier' or 'faker' (fixed lists that are not their own production)."""
    bodies = named_bodies(V, K, k)
    out = {}
    for nm, b in bodies.items():
        cs, ds = host_list(b, K, V)
        out[nm] = (b, cs, ds, (), 'carrier')
    cs, ds = host_list(bodies['CB'], K, V, tags=(1,))
    out['MC1'] = (bodies['CB'], cs, ds, (1,), 'carrier')
    cbC, cbD = out['CB'][1], out['CB'][2]
    cbpC = out['CBP'][1]
    out['CBfake'] = (C.D_, cbC, cbD, (), 'faker')
    out['CBmut'] = (bodies['CB'], tuple(cbpC) + tuple(cbC), (), (), 'faker')
    dcert = [e[1] for e in C.uncons(C.dcert_list())]
    out['Dcert'] = (C.D_, tuple(dcert), (), (), 'faker')
    sl_body = C.body_CB(4, V, K)
    prod, pr = probes(K, V)
    mk = lambda certs: C.carrier(marked_body(sl_body, 'H'), certs)
    lst, _ = C.produce_list(prod, 0, mk, pr, K, V)
    cs, ds = split_list(lst)
    out['CBsloppy'] = (sl_body, cs, ds, (), 'faker')
    out['CF'] = (C.D_, (), (), (), 'copier-faker')
    return out


def make_prog(cat, name, mode, start='mode'):
    """A program of the catalogue in a mode.  start: 'mode' (H gets its list, S/C/CS empty), 'host' (every mode starts
    with the H list: the identical-inventory control and C⁺), 'empty'.  Fakers keep their fixed lists in every mode
    except under 'empty'; CF is always empty."""
    body, cs, ds, tags, kind = cat[name]
    if kind == 'copier-faker' or start == 'empty' or (start == 'mode' and mode != 'H' and kind == 'carrier'):
        cs, ds = (), ()
    return Prog(name, body, mode, cs, ds, None, tags)
