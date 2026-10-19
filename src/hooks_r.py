"""Hooks, Part R: a first-class hook primitive with maximal fills in the realizable language (spec
specs/2026-10-18-hooks.md; notes notes/hooks-r.md; predictions predictions/2026-10-18-hooks-r.md).

Imports milestone 4's checker, milestone 5's genes and universe, the detectors run's Key rule and world K, and the
world-K island machinery unchanged, and adds:
  1. grammar H: grammar P with the action leaves HOOK(t, a0) (one node each), its prior and resolution tables;
  2. fills (tag, scope, key, action, source) and the conflict rule (host side, used by the populations);
  3. the gene-site check at the term level: a new library wrapper CHKH with its core (the six Key scopes, the self
     guard, the conflict rule, Hyp^self closing the gene-site box), hooked carriers, and the host replay of CHKH;
  4. Lemma H: baked composite carriers and host-computed values (plays, productions, behaviour classes) for the
     populations' cache misses;
  5. founders and the gene prior.
"""
import fcntl
import json
import os
import pickle
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C
import lt_genes as G
import lt_genes_pop as GP
import carrier_populations as CP
import detectors as DT

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'hooks_r')
os.makedirs(OUT, exist_ok=True)
K = DT.K
V = DT.V
PCAP = DT.PCAP

# ------------------------------------------------------------------------------------------------------------ 1
# Grammar H
# ------------------------------------------------------------------------------------------------------------
LEAVES_H = [('C',), ('D',), ('H', 1, 'C'), ('H', 1, 'D'), ('H', 2, 'C'), ('H', 2, 'D')]


def enumerate_H(nmax=7):
    """All actions of grammar H with <= nmax nodes, {n: [sexpr]} (P's construction with the hook leaves)."""
    atoms = CP.atom_alphabet()
    B, A = {}, {}
    for n in range(1, nmax + 1):
        if n == 1:
            B[n] = [('A', x) for x in atoms]
            continue
        out = [('not', b) for b in B[n - 1]]
        for i in range(1, n - 1):
            for b1 in B[i]:
                for b2 in B[n - 1 - i]:
                    out.append(('and', b1, b2)); out.append(('or', b1, b2))
        B[n] = out
    for n in range(1, nmax + 1):
        if n == 1:
            A[n] = list(LEAVES_H)
            continue
        out = []
        for i in range(1, n):
            for j in range(1, n):
                k = n - 1 - i - j
                if k < 1: continue
                for b in B[i]:
                    for x in A[j]:
                        for y in A[k]:
                            out.append(('if', b, x, y))
        A[n] = out
    return A


def hook_leaves(x):
    """Hook leaves in left-to-right order: [(t, a0)]."""
    if x[0] == 'H': return [(x[1], x[2])]
    if x[0] in ('C', 'D'): return []
    return hook_leaves(x[2]) + hook_leaves(x[3])


def canonical(x):
    hs = hook_leaves(x)
    return not hs or hs[0][0] == 1


def nodes_H(x):
    if x[0] in ('C', 'D', 'H'): return 1
    if x[0] == 'if': return 1 + CP.nodes(x[1]) + nodes_H(x[2]) + nodes_H(x[3])
    raise ValueError(x)


def resolve(x, h):
    """x[h]: every hook leaf of tag t replaced by h[t] ('C' | 'D'), or by its own default where h[t] is None."""
    if x[0] == 'H':
        v = h.get(x[1])
        return (v if v is not None else x[2],)
    if x[0] in ('C', 'D'): return x
    return ('if', x[1], resolve(x[2], h), resolve(x[3], h))


def show_H(x):
    t = x[0]
    if t == 'H': return 'HOOK(%d,%s)' % (x[1], x[2])
    if t in ('C', 'D'): return t
    return 'if(%s,%s,%s)' % (CP.show(x[1]), show_H(x[2]), show_H(x[3]))


HCODE_U, HCODE_C, HCODE_D = 0, 1, 2


def hcode(h1, h2):
    """Resolution code of a tag assignment (0 unfilled, 1 C, 2 D per tag): h1 + 3 h2."""
    return h1 + 3 * h2


class GrammarH:
    """Spellings of H: indices 0 .. NP-1 are grammar P's spellings in the P catalogue's order (so P's tables apply);
    hooked spellings follow in enumeration order.  RES[s, code]: the P spelling of s[h] (code = h1 + 3 h2)."""

    def __init__(self, cat):
        self.cat = cat
        NP = len(cat.spell)
        assert all(cat.spell[k]['i'] == k for k in range(NP))
        pidx = {cat.sexprs[k]: k for k in range(NP)}
        A = enumerate_H(7)
        hooked = []
        for n in range(1, 8):
            for x in A[n]:
                hs = hook_leaves(x)
                if hs and canonical(x):
                    hooked.append(x)
        self.sexprs = list(cat.sexprs[:NP]) + hooked
        self.NP = NP
        S = len(self.sexprs)
        self.S = S
        self.nodes = np.array([CP.nodes(x) if k < NP else nodes_H(x) for k, x in enumerate(self.sexprs)], np.int64)
        self.ntags = np.zeros(S, np.int64)
        self.RES = np.zeros((S, 9), np.int64)
        for k in range(S):
            x = self.sexprs[k]
            if k < NP:
                self.RES[k, :] = k
                continue
            tags = sorted(set(t for t, _ in hook_leaves(x)))
            self.ntags[k] = len(tags)
            for h1 in range(3):
                for h2 in range(3):
                    h = {1: (None, 'C', 'D')[h1], 2: (None, 'C', 'D')[h2]}
                    self.RES[k, hcode(h1, h2)] = pidx[resolve(x, h)]
        w = 2.0 ** (-self.nodes.astype(float))
        self.mu = w / w.sum()

    def name(self, k):
        return self.cat.name(k) if k < self.NP else show_H(self.sexprs[k])


# ------------------------------------------------------------------------------------------------------------ 2
# Fills and the conflict rule (host side)
# ------------------------------------------------------------------------------------------------------------
SC_NONE, SC_ROLE, SC_BEH, SC_HIST, SC_SRC, SC_ROOT = range(6)
SCOPES = ['none', 'role', 'behaviour', 'history', 'source', 'root']
RANK = np.array([1, 2, 4, 3, 6, 5], np.int64)        # source > root > behaviour > history > role > none
SRC_SEED, SRC_WRITE, SRC_COPY, SRC_CONTRACT = range(4)
SOURCES = ['seed', 'write', 'copy', 'contract']
SELF_KEY = -2                                         # the token SELF (source scope)
RK_C, RK_D, RK_SELF, RK_OTHER = range(4)              # root keys; also the root kinds of Lemma H
KIND_P, KIND_C, KIND_D, KIND_S = RK_OTHER, RK_C, RK_D, RK_SELF
FMAX = 4                                              # fills per program (FIFO beyond)


def key_holds(scope, key, kind, opp_sp, opp_class, own_sp):
    """A fill's Key side condition at a gene-site root of the given kind (KIND_*) with the opponent's spelling and
    behaviour class (probes: spelling -1, class 0).  The self guard: behaviour never holds at the self root."""
    if scope <= SC_ROLE: return True
    if scope == SC_BEH: return kind != KIND_S and key == opp_class
    if scope == SC_HIST: return key == opp_sp
    if scope == SC_SRC:
        if key == SELF_KEY: return opp_sp == own_sp
        return key == opp_sp
    return key == kind


def winner(fills, tag, kind, opp_sp, opp_class, own_sp, inert=None, recency=False):
    """The conflict rule: among the tag's applicable fills (keys hold, not inert) the highest rank wins, ties to the
    later position; recency=True: the latest applicable wins.  Returns the fill's index or -1."""
    best, br = -1, -1
    for i, f in enumerate(fills):
        t, sc, key, act, src = f
        if t != tag: continue
        if inert is not None and inert[src, sc]: continue
        if not key_holds(sc, key, kind, opp_sp, opp_class, own_sp): continue
        rk = 1 if recency else int(RANK[sc])
        if rk >= br:
            best, br = i, rk
    return best


# ------------------------------------------------------------------------------------------------------------ 3
# The gene-site check at the term level
# ------------------------------------------------------------------------------------------------------------
FILL = 28
SELF_TOK = 9          # the SELF token in the term's key data (a natural; every bare-source encoding is a pair)


def enc_const(e):
    """A canonical encoding (nested ints / 2-tuples) as SxCompiler constant syntax."""
    if isinstance(e, int): return e
    return ['pair', enc_const(e[0]), enc_const(e[1])]


QCENC = L.canon_term(L.PROG_C)
QDENC = L.canon_term(L.PROG_D)

_ISWRAP_OLD = ("(def iswrap (n) (or (eq n ID_CHKS) (or (eq n ID_CHKS2) (or (eq n ID_CHKN) (or (eq n ID_CHKO) "
               "(or (eq n ID_CHKX) (eq n ID_CHKL)))))))")
_ISWRAP_NEW = ("(def iswrap (n) (or (eq n ID_CHKS) (or (eq n ID_CHKS2) (or (eq n ID_CHKN) (or (eq n ID_CHKO) "
               "(or (eq n ID_CHKX) (or (eq n ID_CHKL) (eq n ID_CHKH))))))))")
_CALLC_OLD = "        ((eq n ID_CHKX) (capk (fst ad) CCX ad))\n        (else (capk (fst ad) CCL ad))))"
_CALLC_NEW = ("        ((eq n ID_CHKX) (capk (fst ad) CCX ad))\n        ((eq n ID_CHKH) (capk (fst ad) CCH ad))\n"
              "        (else (capk (fst ad) CCL ad))))")

HOOK_SRC_TMPL = r"""
; ---------------- the gene-site check (notes/hooks-r.md §1.2-1.3) ----------------
(def CHKH (arg) (if (eq (capk (fst arg) CCH arg) T) T F))
(def CCH (arg) (hcore arg))
(def hcore (arg)
  (let ((r (snd arg)) (t (fst r)) (m (fst (snd r))) (a (fst (snd (snd r)))) (kt (snd (snd (snd r))))
        (tag (mod kt 4)) (KK (div kt 4)) (VV (fst arg)) (cl (getcerts t)))
    (if (eq cl NONE) F
      (let ((w (hbest cl tag t m VV KK NONE 0)))
        (if (eq w NONE) F
          (if (eq (fst w) a)
              (let ((Rb (pair 8 (pair ID_CHKH arg))))
                (if (lt 0 (cchk (pair 0 (pair Rb (pair NONE VV))) (fst (snd (snd (snd w)))) 0 (pair Rb 0))) T F))
              F))))))
(def isfill (s tag) (and (eq (fst s) 28) (eq (fst (fst (snd s))) tag)))
(def hbest (cl tag t m VV KK best brank)
  (if (eq cl 0) best
    (let ((e (fst cl)) (s (snd e)))
      (if (isfill s tag)
          (let ((j (fst (snd s))) (sc (fst (snd j))) (k (snd (snd j))))
            (if (hkey sc k t m VV KK)
                (let ((rk (hrank sc)))
                  (if (le brank rk) (hbest (snd cl) tag t m VV KK e rk) (hbest (snd cl) tag t m VV KK best brank)))
                (hbest (snd cl) tag t m VV KK best brank)))
          (hbest (snd cl) tag t m VV KK best brank)))))
(def hrank (sc) %(HRANK)s)
(def hkey (sc k t m VV KK)
  (cond ((lt sc 2) T)
        ((eq sc 2) (if (eq m t) F (eq k (bclass m VV KK))))
        ((eq sc 3) (eq k (bareof m)))
        ((eq sc 4) (if (eq k SELFTOK) (eq (bareof m) (bareof t)) (eq k (bareof m))))
        (else (eq k (rclass m t)))))
(def rclass (m t) (cond ((eq m QCENC) 0) ((eq m QDENC) 1) ((eq m t) 2) (else 3)))
(def bclass (m VV KK) (add (hbit m QCENC VV KK 4) (add (hbit m QDENC VV KK 2) (hbit m m VV KK 1))))
(def hbit (m q VV KK wt) (if (eq (callcheck ID_CHKS (pair VV (pair m (pair q (pair C KK))))) T) wt 0))
"""
HRANK_CONFLICT = "(cond ((eq sc 4) 6) ((eq sc 5) 5) ((eq sc 2) 4) ((eq sc 3) 3) ((eq sc 1) 2) (else 1))"
HRANK_RECENCY = "1"
LIB_H = {'which': None, 'ID_CHKH': None, 'MODE_H': 7}


def install_hook_library(recency=False):
    """Milestone 5's library with the detectors run's Key clause, iswrap/callcheck redefined in place to recognize
    CHKH (appended last in each), KEY_SRC, and the hook source appended after every existing entry (indices of every
    earlier entry unchanged, asserted).  Registers CHKH as a wrapper for the host replay (mode 7)."""
    which = 'recency' if recency else 'conflict'
    if LIB_H['which'] == which: return
    leave_hook_library()
    DT.install_library('base')
    before = dict(L.LIBIDX)
    src = DT.CERT_SRC_K
    assert src.count(_ISWRAP_OLD) == 1 and src.count(_CALLC_OLD) == 1
    src = src.replace(_ISWRAP_OLD, _ISWRAP_NEW).replace(_CALLC_OLD, _CALLC_NEW)
    comp = L.SxCompiler()
    for k, v in L.LIB_CONSTS.items(): comp.consts[k] = v
    for k, v in C.CERT_CONSTS.items(): comp.consts[k] = v
    comp.consts['QCENC'] = enc_const(QCENC)
    comp.consts['QDENC'] = enc_const(QDENC)
    comp.consts['SELFTOK'] = SELF_TOK
    comp.load(L.LIBRARY_SRC)
    comp.load(src)
    comp.load(G.GENE_SRC)
    comp.load(DT.KEY_SRC)
    comp.load(HOOK_SRC_TMPL % {'HRANK': HRANK_RECENCY if recency else HRANK_CONFLICT})
    for nm in C.WRAP_NAMES + ['CHKH']: comp.consts['ID_' + nm] = comp.order.index(nm)
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
    L.CORE_LIBS[L.LIBIDX['PCORE']] = G.PCORE_ID_CODE
    L.CORE_LIBS[L.LIBIDX['CCH']] = C.CORE_ID_BASE + LIB_H['MODE_H']
    L._compiled.clear()
    L.LIBCODE[:] = [L.compile_term(t[1]) for t in terms]
    L.CACHE.clear()
    C.ID.clear(); C.ID.update({nm: L.LIBIDX[nm] for nm in C.WRAP_NAMES})
    nh = L.LIBIDX['CHKH']
    C.WRAPS.clear(); C.WRAPS.update(C.ID.values()); C.WRAPS.add(nh)
    C.CC_MODE.clear(); C.CC_MODE.update({L.LIBIDX[nm]: mode for nm, mode in C.CORE_NAMES.items()})
    C.WRAP_MODE.clear(); C.WRAP_MODE.update({L.LIBIDX[C.MODE_WRAP[m]]: m for m in C.MODE_WRAP})
    C.WRAP_MODE[nh] = LIB_H['MODE_H']
    LIB_H['which'] = which; LIB_H['ID_CHKH'] = nh
    LIB_H['names'] = [nm for nm in L.LIBIDX if nm not in before]
    DT.LIB_STATE['which'] = 'hooks'
    _HookCore.RECENCY = recency


def leave_hook_library(to=None):
    """Forget the hook library's names (so the parents' rebuilds, which assert their own indices, can run), then
    optionally install a parent library ('base' | 'key')."""
    if LIB_H.get('names'):
        for nm in LIB_H['names']:
            L.LIBIDX.pop(nm, None)
        LIB_H['names'] = None
        LIB_H['which'] = None
        DT.LIB_STATE['which'] = None
    if DT.LIB_STATE['which'] == 'key' and to != 'key':
        for nm in ('bareof', 'ckey'):
            L.LIBIDX.pop(nm, None)
        DT.LIB_STATE['which'] = None
    if to is not None:
        DT.install_library(to)


def hook_arg(V_, x, y, a, K_, tag):
    """The gene-site call's argument: milestone 4's shape with the fuel field 4K + tag."""
    return C.P(C.N(V_), C.P(x, C.P(y, C.P(('con', a), C.N(4 * K_ + tag)))))


def hook_call(tag, a, V_=V, K_=K):
    return ('app', ('lib', LIB_H['ID_CHKH']), hook_arg(V_, C.ME3, C.THEM3, a, K_, tag))


def hook_body(x, V_=V, K_=K):
    """Grammar H's sexpr compiled: a hook leaf HOOK(t, a0) -> if CHKH(me, them, not a0; t) then not a0 else a0."""
    if x[0] == 'C': return L.C_
    if x[0] == 'D': return L.D_
    if x[0] == 'H':
        t, a0 = x[1], x[2]
        na = 'D' if a0 == 'C' else 'C'
        return ('if', hook_call(t, na, V_, K_), L.C_ if na == 'C' else L.D_, L.C_ if a0 == 'C' else L.D_)
    return ('if', CP.bterm(x[1], V_, K_), hook_body(x[2], V_, K_), hook_body(x[3], V_, K_))


def fill_script(tag, scope, keydata):
    """Fill_{t,s,k}[Hyp]: node (28, ((tag . (scope . key)), [Hyp at 0]))."""
    return (FILL, ((tag, (scope, keydata)), C.cons([C.node(C.HYP, 0)])))


def key_data(scope, key, bare_of_sp=None):
    """Host fill key -> term key data: spelling keys become the spelling's bare-source encoding."""
    if scope in (SC_HIST, SC_SRC):
        if key == SELF_KEY: return SELF_TOK
        return bare_of_sp(key)
    if scope in (SC_NONE, SC_ROLE): return 0
    return int(key)


def fill_entries(fills, bare_of_sp):
    """Certificate-list entries of a fill list (in list order)."""
    out = []
    for (t, sc, key, act, src) in fills:
        out.append((act, fill_script(t, sc, key_data(sc, key, bare_of_sp))))
    return out


# --- the host replay of CHKH (mode 7) ----------------------------------------------------------------------------
class _HookCore:
    """The gene-site core (mode 7) for a host replay checker; every other mode is the parent's."""
    RECENCY = False

    def _ccore(self, mode, v):
        if mode != LIB_H['MODE_H']:
            return super()._ccore(mode, v)
        return self.hcore(v)

    def hcore(self, v):
        try:
            V_ = v[1][1]; r = v[2]; t = r[1][1]; m = r[2][1][1]; a = r[2][2][1][1]; kt = r[2][2][2][1]
        except Exception:
            return 'F'
        tag, K_ = kt % 4, kt // 4
        cl = C.h_getcerts(t)
        if cl is None: return 'F'
        ents = C.uncons(cl) if cl != 0 else []
        best, br = None, 0
        for e in ents:
            if not isinstance(e, tuple) or len(e) != 2: continue
            s = e[1]
            try:
                if s[0] != FILL or s[1][0][0] != tag: continue
                sc, kd = s[1][0][1]
            except Exception:
                continue
            if not self.hkey(sc, kd, t, m, V_, K_): continue
            rk = 1 if self.RECENCY else int(RANK[sc]) if 0 <= sc < 6 else 0
            if rk >= br and rk > 0:
                best, br = e, rk
        if best is None or best[0] != a: return 'F'
        Rb = ('cbox', LIB_H['ID_CHKH'], v)
        try:
            ps = C.uncons(best[1][1][1])
        except Exception:
            return 'F'
        if not ps: return 'F'
        ok = self.cchk(0, Rb, None, V_, ps[0], (), (Rb,))
        return 'T' if ok else 'F'

    def hkey(self, sc, kd, t, m, V_, K_):
        if sc in (0, 1): return True
        if sc == 2:
            if L.canon_term(m) == L.canon_term(t): return False
            return kd == self.bclass(m, V_, K_)
        if sc == 3: return kd == L.canon_term(DT.bare(m))
        if sc == 4:
            if kd == SELF_TOK: return L.canon_term(DT.bare(m)) == L.canon_term(DT.bare(t))
            return kd == L.canon_term(DT.bare(m))
        if sc == 5: return kd == self.rclass(m, t)
        return False

    @staticmethod
    def rclass(m, t):
        cm = L.canon_term(m)
        if cm == QCENC: return 0
        if cm == QDENC: return 1
        if cm == L.canon_term(t): return 2
        return 3

    def bclass(self, m, V_, K_):
        n0 = C.ID['CHKS']
        b = 0
        for q, wt in ((L.PROG_C, 4), (L.PROG_D, 2), (m, 1)):
            if self.check(n0, C.mk_arg(V_, m, q, 'C', K_)) == 'T': b += wt
        return b

    def hook_check(self, x, m, a, tag, V_=V, K_=K):
        """The gene-site check CHKH(x, m, a; tag) from outside."""
        return self.check(LIB_H['ID_CHKH'], hook_arg(V_, ('quote', x), ('quote', m), a, K_, tag))


class HostH(_HookCore, CP.IdealCheck):
    """The ideal host replay checker (no step cost) with the gene-site core."""


class HostHE(_HookCore, CP.ExactHost):
    """The exact-memo host replay checker (the production tactic's) with the gene-site core."""


def hooked_carrier(x, cseq, dseq, fill_ents, marker='H'):
    """A hooked program's term (world K's keyed reading of hypothesis-closed D scripts; fills after the blocks)."""
    body = G.marked_body(hook_body(x), marker)
    dl = [DT.keyed(s, DT.KEY_D) if DT.has_hyp(s) else s for s in dseq]
    ents = [('C', s) for s in cseq] + [('D', s) for s in dl] + list(fill_ents)
    return C.carrier(body, C.cons(ents))


# ------------------------------------------------------------------------------------------------------------ 4
# Lemma H: baked composite carriers and host values
# ------------------------------------------------------------------------------------------------------------
QC_T, QD_T = ('quote', L.PROG_C), ('quote', L.PROG_D)


def baked_body(bP, bC, bD, bS):
    """Dispatch on the opponent's quote: ⌜C⌝, ⌜D⌝, the program itself, anything else."""
    return ('if', ('eq', C.THEM3, QC_T), bC, ('if', ('eq', C.THEM3, QD_T), bD, ('if', ('eq', C.THEM3, C.ME3), bS, bP)))


class Host:
    """Host values for the kernel's cache misses (notes §1.4): one per process.  Profiles are tuples
    (tP, tC, tD, tS, csp, dsp) of P run trees (tau ids, -1 = untouched: replaced by tP) and packed script blocks."""

    def __init__(self, U, LS):
        self.U = U
        self.LS = LS
        self.h = HostH()
        self.prod = C.Producer(host=CP.ExactHost())
        self.terms = {}
        self.n_calls = {'pair': 0, 'prodC': 0, 'pd': 0, 'cls': 0, 'self': 0}
        self.t_calls = {'pair': 0.0, 'prodC': 0.0, 'pd': 0.0, 'cls': 0.0, 'self': 0.0}

    # blocks -----------------------------------------------------------------
    @staticmethod
    def unpack(p):
        out = []
        while p:
            out.append((p & 255) - 1); p >>= 8
        return out

    def body(self, t):
        return self.U.bodies[t]

    def term(self, prof, marker):
        key = (prof, marker)
        tm = self.terms.get(key)
        if tm is None:
            tP, tC, tD, tS, csp, dsp = prof
            tC = tP if tC < 0 else tC; tD = tP if tD < 0 else tD; tS = tP if tS < 0 else tS
            if tC == tP and tD == tP and tS == tP:
                b = self.body(tP)
            else:
                b = baked_body(self.body(tP), self.body(tC), self.body(tD), self.body(tS))
            b = G.marked_body(b, marker)
            cs = [self.U.scripts[i][1] for i in self.unpack(csp)]
            ds = [self.U.scripts[i][1] for i in self.unpack(dsp)]
            ds = [DT.keyed(s, DT.KEY_D) if DT.has_hyp(s) else s for s in ds]
            tm = C.carrier(b, G.canon_list(cs, ds))
            if len(self.terms) > 60000: self.terms.clear()
            self.terms[key] = tm
        return tm

    def _clear(self):
        if len(self.h.memo) > 120000: self.h.clear()
        if len(self.prod.host.memo) > 120000: self.prod.host.clear()

    def chk(self, x, m, a):
        return self.h.check(C.ID['CHKS'], C.mk_arg(V, x, m, a, K)) == 'T'

    def act(self, tP, xt, mt):
        """x's action at the partner root against m (the P branch tree tP), atoms by host checks."""
        def val(at):
            k_, ai, qi = GP.atom_box_kind(at)
            a = 'C' if ai == 0 else 'D'
            q = L.PROG_C if qi == 0 else L.PROG_D
            if k_ == 0: return self.chk(mt, xt, a)
            if k_ == 1: return self.chk(xt, mt, a)
            if k_ == 2: return self.chk(mt, mt, a)
            if k_ == 3: return self.chk(xt, xt, a)
            if k_ == 4: return self.chk(mt, q, a)
            return self.chk(xt, q, a)
        return int(CP.eval_dt(self.U.tau_dt[tP], val))

    def pair(self, px, pm):
        """(a_xm, a_mx) for two distinct quotes (1 = C)."""
        t0 = time.time()
        self._clear()
        xt = self.term(px, 'H')
        mt = self.term(pm, 'C' if self.term(pm, 'H') == xt else 'H')
        r = (self.act(px[0], xt, mt), self.act(pm[0], mt, xt))
        self.n_calls['pair'] += 1; self.t_calls['pair'] += time.time() - t0
        return r

    def selfplay(self, px):
        """x's action against its own quote (the self root: the S branch)."""
        t0 = time.time()
        self._clear()
        xt = self.term(px, 'H')
        tS = px[3] if px[3] >= 0 else px[0]
        r = self.act(tS, xt, xt)
        self.n_calls['self'] += 1; self.t_calls['self'] += time.time() - t0
        return r

    def prodC(self, px, pm):
        """The tactic's C script for x at the root (x, m, C): global script id, -1 none."""
        t0 = time.time()
        self._clear()
        xt = self.term(px, 'H')
        mt = self.term(pm, 'C' if self.term(pm, 'H') == xt else 'H')
        s = self.prod.produce(0, xt, mt, 'C', K, V)
        self.n_calls['prodC'] += 1; self.t_calls['prodC'] += time.time() - t0
        return -1 if s is None else self.sid('C', s)

    def prodD(self, px):
        t0 = time.time()
        self._clear()
        xt = self.term(px, 'H')
        s = self.prod.produce(0, xt, L.PROG_D, 'D', K, V)
        self.n_calls['pd'] += 1; self.t_calls['pd'] += time.time() - t0
        return -1 if s is None else self.sid('D', s)

    def bclass(self, px):
        """Behaviour class 4 [C vs ⌜C⌝] + 2 [C vs ⌜D⌝] + [C vs itself] of a program (certified cooperation)."""
        t0 = time.time()
        self._clear()
        xt = self.term(px, 'H')
        b = 4 * self.chk(xt, L.PROG_C, 'C') + 2 * self.chk(xt, L.PROG_D, 'C') + self.chk(xt, xt, 'C')
        self.n_calls['cls'] += 1; self.t_calls['cls'] += time.time() - t0
        return int(b)

    def sid(self, a, s):
        return script_id(self.U, a, s)


# --- the script registry (shared by processes) ---------------------------------------------------------------
REG = os.path.join(OUT, 'scripts.pkl')


def script_id(U, a, s):
    k = (a, s)
    i = U.sid.get(k)
    if i is not None: return i
    with open(REG + '.lock', 'w') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        extra = pickle.load(open(REG, 'rb')) if os.path.exists(REG) else []
        for kk in extra[len(U.scripts) - U.n_base_scripts:]:
            U.sid[kk] = len(U.scripts); U.scripts.append(kk)
        i = U.sid.get(k)
        if i is None:
            i = len(U.scripts); U.sid[k] = i; U.scripts.append(k)
            extra = U.scripts[U.n_base_scripts:]
            with open(REG + '.tmp', 'wb') as f: pickle.dump(extra, f)
            os.replace(REG + '.tmp', REG)
        fcntl.flock(lk, fcntl.LOCK_UN)
    return i


def load_universe(LS):
    """World K's universe (scripts, units, bodies) plus the shared registry of scripts found by composite
    production."""
    meta = LS['meta']
    U = GP.Universe(K, PCAP)
    U.scripts = list(meta['scripts']); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.units = list(meta['units']); U.uid = {k: i for i, k in enumerate(U.units)}
    U.n_base_scripts = len(U.scripts)
    if os.path.exists(REG):
        for kk in pickle.load(open(REG, 'rb')):
            if kk not in U.sid:
                U.sid[kk] = len(U.scripts); U.scripts.append(kk)
    return U


def pack_block(seq):
    p = 0
    for i, s in enumerate(seq):
        assert 0 <= s < 255 and i < 7
        p |= (s + 1) << (8 * i)
    return p


# ------------------------------------------------------------------------------------------------------------ 5
# Statics for the kernel, founders, the gene prior, the run object
# ------------------------------------------------------------------------------------------------------------
import hooks_r_kern as HK                                     # noqa: E402
import world_k as WK                                          # noqa: E402
import provenance_run as PR                                   # noqa: E402
import realizable_scaling as RS                               # noqa: E402

SALT_H = 20261018
_STAT = {}


def _bt_leaf(b, t, f):
    return CP._bt(b, t, f)


def dt_leaf(x):
    """Run tree with leaves 0 (C or D) or the hook tag (1, 2)."""
    if x[0] == 'H': return x[1]
    if x[0] in ('C', 'D'): return 0
    return CP._bt(x[1], dt_leaf(x[2]), dt_leaf(x[3]))


def atoms_leaf(t):
    if isinstance(t, int): return set()
    return {t[0]} | atoms_leaf(t[1]) | atoms_leaf(t[2])


def eval_leaf(t, val):
    while not isinstance(t, int):
        t = t[1] if val(t[0]) else t[2]
    return t


def statics():
    """World K's tables and universe, grammar H and the kernel's static arrays (cached per process)."""
    if _STAT: return _STAT
    sys.setrecursionlimit(1000000)
    LS = WK.use_world('K')
    DT.set_world('K')
    st = LS['st']
    cat = LS['cat']
    U = load_universe(LS)
    gh = GrammarH(cat)
    T = cat.T
    KIND = np.asarray(st['KIND']); NAT = np.asarray(st['NAT'])
    AMASK = np.zeros(T, np.int64)
    ACTT = np.zeros((T, 4), np.int64)
    for t in range(T):
        ats = U.tau_atoms[t]
        assert NAT[t] == len(ats)
        m = 0
        for i, at in enumerate(ats):
            kk = GP.atom_box_kind(at)
            assert tuple(KIND[t, i]) == kk, (t, i)
            k_, ai, qi = kk
            if k_ == 3: m |= 1
            elif k_ == 5: m |= 2 if qi == 0 else 4
            elif k_ == 0: m |= 8
            elif k_ == 2: m |= 16
            elif k_ == 4: m |= 32 if qi == 0 else 64
        AMASK[t] = m
        for vc in range(4):
            ACTT[t, vc] = CP.eval_dt(U.tau_dt[t], lambda at, vc=vc: bool((vc >> ats.index(at)) & 1))
    TAUP = np.asarray(LS['tau'], np.int64)
    LEAFT = np.zeros((gh.S, 4), np.int64)
    for s in range(gh.NP, gh.S):
        x = gh.sexprs[s]
        dl = dt_leaf(x)
        ats = sorted(atoms_leaf(dl))
        t0 = TAUP[gh.RES[s, 0]]
        assert ats == U.tau_atoms[t0], s
        for vc in range(4):
            LEAFT[s, vc] = eval_leaf(dl, lambda at, vc=vc: bool((vc >> ats.index(at)) & 1))
    O = np.asarray(st['O'])
    inO = np.zeros(len(U.units), np.bool_); inO[O] = True
    uid_py = {}
    for u, (t, cs, ds) in enumerate(meta_units(LS)):
        uid_py[(int(t), pack_block(cs), pack_block(ds))] = u
    CLEAF = np.array([('C' in str(U.tau_dt[t])) for t in range(T)], np.bool_)
    CLEAF = np.array([_has_c_leaf(U.tau_dt[t]) for t in range(T)], np.bool_)
    _STAT.update(FUT=np.asarray(LS['FUT']), CLEAF=CLEAF, LS=LS, st=st, cat=cat, U=U, gh=gh, KIND=KIND, NAT=NAT, AMASK=AMASK, ACTT=ACTT, TAUP=TAUP,
                 LEAFT=LEAFT, inO=inO, uid_py=uid_py, A=np.asarray(st['A']), selfa=np.asarray(st['selfa']),
                 CHC=np.asarray(st['CHC']), CHD=np.asarray(st['CHD']), UVt=np.asarray(st['UVt']),
                 BLC=np.asarray(st['BLC']), BLD=np.asarray(st['BLD']), PRODC=np.asarray(LS['PRODC']),
                 PD=np.asarray(LS['PD']))
    return _STAT


def _has_c_leaf(t):
    if isinstance(t, str): return t == 'C'
    return _has_c_leaf(t[1]) or _has_c_leaf(t[2])


def meta_units(LS):
    return LS['meta']['units']


# --- the gene prior -----------------------------------------------------------------------------------------
import math  # noqa: E402
PK = np.array([np.exp(-1.0) / math.factorial(k) for k in range(5)])
PK = PK / PK.sum()


def draw_fills(rng, ntags, src_keys, hist_keys, scope_p=None):
    """One founder's fills (seeded): k ~ Poisson(1) | k <= 4; tag, scope, key, action uniform (notes §1.5).  The
    draws are consumed whatever ntags (coupling); founders without tags return []."""
    k = int(rng.choice(5, p=PK))
    out = []
    for _ in range(k):
        u = rng.random(5)
        tag = 1 + int(u[0] * max(ntags, 1)) if ntags else 1
        if scope_p is None:
            sc = int(u[1] * 6)
        else:
            sc = int(np.searchsorted(np.cumsum(scope_p), u[1] * scope_p.sum(), side='right'))
            sc = min(sc, 5)
        if sc in (SC_NONE, SC_ROLE): key = 0
        elif sc == SC_BEH: key = int(u[2] * 8)
        elif sc == SC_ROOT: key = int(u[2] * 4)
        elif sc == SC_HIST: key = int(hist_keys[int(u[2] * len(hist_keys))])
        else:
            j = int(u[2] * (len(src_keys) + 1))
            key = SELF_KEY if j == len(src_keys) else int(src_keys[j])
        act = 1 if u[3] < 0.5 else 0
        out.append((tag, sc, key, act, SRC_SEED))
    return out if ntags else []


def founders_H(N, I, rep, renorm_no_source=False):
    """Grammar-H founders (spellings from prior L over H) and their seeded fills; one stream per replicate."""
    S_ = statics()
    gh = S_['gh']
    rng = np.random.default_rng([N, I, rep, SALT_H])
    sp = rng.choice(gh.S, size=(I, N), p=gh.mu)
    keys = np.unique(sp)
    rf = np.random.default_rng([N, I, rep, SALT_H, 1])
    scope_p = np.array([1, 1, 1, 1, 0, 1], float) if renorm_no_source else None
    fills = [[draw_fills(rf, int(gh.ntags[sp[i, j]]), keys, keys, scope_p) for j in range(N)] for i in range(I)]
    return sp, fills


# --- host callbacks ------------------------------------------------------------------------------------------
_HOST = {}


def _prof(key6):
    return tuple(int(x) for x in key6)


def _cb_pair(key):
    h = _HOST['h']
    px, pm = _prof(key[:6]), _prof(key[6:])
    a, b = h.pair_vals(px, pm)
    return a | (b << 4)


def _cb_self(key):
    return _HOST['h'].self_vals(_prof(key))


def _cb_cls(key):
    return _HOST['h'].bclass(_prof(key))


def _cb_prodc(key):
    return _HOST['h'].prodC(_prof(key[:6]), _prof(key[6:]))


def _cb_pd(key):
    return _HOST['h'].prodD(_prof(key))


def install_callbacks():
    S_ = statics()
    if 'h' not in _HOST:
        _HOST['h'] = HostV(S_['U'], S_['LS'])
    HK.HOSTFN.update(pair=_cb_pair, self=_cb_self, cls=_cb_cls, prodc=_cb_prodc, pd=_cb_pd)


class HostV(Host):
    """Host values as atom valcodes (the kernel evaluates actions and reached leaves from them)."""

    def vals(self, tP, xt, mt):
        ats = self.U.tau_atoms[tP]
        vc = 0
        for i, at in enumerate(ats):
            k_, ai, qi = GP.atom_box_kind(at)
            a = 'C' if ai == 0 else 'D'
            q = L.PROG_C if qi == 0 else L.PROG_D
            if k_ == 0: v = self.chk(mt, xt, a)
            elif k_ == 1: v = self.chk(xt, mt, a)
            elif k_ == 2: v = self.chk(mt, mt, a)
            elif k_ == 3: v = self.chk(xt, xt, a)
            elif k_ == 4: v = self.chk(mt, q, a)
            else: v = self.chk(xt, q, a)
            vc |= int(v) << i
        return vc

    def pair_vals(self, px, pm):
        t0 = time.time()
        self._clear()
        xt = self.term(px, 'H')
        mt = self.term(pm, 'C' if self.term(pm, 'H') == xt else 'H')
        r = (self.vals(px[0], xt, mt), self.vals(pm[0], mt, xt))
        self.n_calls['pair'] += 1; self.t_calls['pair'] += time.time() - t0
        return r

    def self_vals(self, px):
        t0 = time.time()
        self._clear()
        xt = self.term(px, 'H')
        tS = px[3] if px[3] >= 0 else px[0]
        r = self.vals(tS, xt, xt)
        self.n_calls['self'] += 1; self.t_calls['self'] += time.time() - t0
        return r


# --- cells -----------------------------------------------------------------------------------------------------
def inert_map(kind):
    """INERT[source, scope] for a cell's ablation kind."""
    M = np.zeros((4, 6), np.bool_)
    if kind == 'max' or kind is None: return M
    if kind == 'inert': M[:, :] = True; return M
    if kind.startswith('scope-'):
        M[:, SCOPES.index(kind[6:])] = True; return M
    if kind == 'seedonly': M[1:, :] = True; return M
    if kind == 'nowrite': M[SRC_WRITE, :] = True; return M
    if kind == 'nocopy': M[SRC_COPY, :] = True; return M
    if kind == 'nocontract': M[SRC_CONTRACT, :] = True; return M
    if kind == 'idroutes':
        M[:, SC_SRC] = True; M[:, SC_HIST] = True; M[SRC_CONTRACT, :] = True; return M
    raise ValueError(kind)


# name -> dict(N, I, grammar 'P'|'H', inert kind, flags, ff)
CELLS = {}


def reg(name, N=200, I=64, grammar='H', inert='max', recency=False, grudge_only=False, shuffle=False, clone=False,
        noinherit=False, renorm=False, ff=False, p_copy=0.05, p_contract=0.05, rf=10):
    CELLS[name] = dict(N=N, I=I, grammar=grammar, inert=inert, recency=recency, grudge_only=grudge_only,
                       shuffle=shuffle, clone=clone, noinherit=noinherit, renorm=renorm, ff=ff, p_copy=p_copy,
                       p_contract=p_contract, rf=rf)
    return name


reg('B', grammar='P'); reg('I', inert='inert'); reg('M')
for _s in SCOPES: reg('M-' + _s, inert='scope-' + _s)
reg('seedonly', inert='seedonly'); reg('nowrite', inert='nowrite'); reg('nocopy', inert='nocopy')
reg('nocontract', inert='nocontract'); reg('recency', recency=True); reg('shuffle', shuffle=True)
reg('noinherit', noinherit=True); reg('grudgeonly', grudge_only=True); reg('idroutes', inert='idroutes')
reg('renorm', renorm=True); reg('clone', clone=True)
reg('B-ff', N=100, I=128, grammar='P', ff=True); reg('I-ff', N=100, I=128, inert='inert', ff=True)
reg('M-ff', N=100, I=128, ff=True)
reg('B-400', N=400, grammar='P'); reg('I-400', N=400, inert='inert'); reg('M-400', N=400)
reg('audM', I=8); reg('audclone', I=8, clone=True); reg('audrec', I=8, recency=True)   # Lemma H audit cells (8 islands)
MERGE_AT = 200
KCAP_DEF = 200000


# --- caches persisted across jobs ---------------------------------------------------------------------------
CDIR = os.path.join(OUT, 'cache')
CACHE_NAMES = ('pair', 'prodc', 'pd', 'cls', 'selfv')


def load_caches(dd):
    """Fill the kernel's typed dicts from every shard (shards are written by finished jobs)."""
    os.makedirs(CDIR, exist_ok=True)
    n = 0
    for fn in sorted(os.listdir(CDIR)):
        if not fn.endswith('.pkl'): continue
        try:
            data = pickle.load(open(os.path.join(CDIR, fn), 'rb'))
        except Exception:
            continue
        for nm in CACHE_NAMES:
            d = dd[nm]
            for k, v in data.get(nm, {}).items():
                d[k] = v; n += 1
    return n


def save_caches(dd, tag, known):
    """Write this job's new entries (keys not in `known`) as one shard."""
    os.makedirs(CDIR, exist_ok=True)
    data = {}
    tot = 0
    for nm in CACHE_NAMES:
        kn = known.get(nm, set())
        data[nm] = {k: v for k, v in dd[nm].items() if k not in kn}
        tot += len(data[nm])
    if tot == 0: return 0
    path = os.path.join(CDIR, '%s_%d_%d.pkl' % (tag, os.getpid(), int(time.time())))
    with open(path + '.tmp', 'wb') as f: pickle.dump(data, f)
    os.replace(path + '.tmp', path)
    for nm in CACHE_NAMES:
        known.setdefault(nm, set()).update(data[nm].keys())
    return tot


class HRun:
    """One run: the island (or fission-fusion) lottery with hooked types."""

    def __init__(self, cell, rep, kcap=KCAP_DEF):
        install_callbacks()
        S_ = statics()
        c = CELLS[cell]
        self.cell, self.rep, self.c = cell, rep, c
        N, I = c['N'], c['I']
        self.N, self.I, self.r, self.rf = N, I, 100, c['rf']
        self.mN = RS.mN_cal(N) if not c['ff'] else 1.0
        self.seed = PR.kernel_seed(N, I, rep)
        self.fseed = int((self.seed * 2862933555777941757 + 3037000493) % (2 ** 62))
        self.g = 0
        gh = S_['gh']
        if c['grammar'] == 'P':
            LS = S_['LS']
            sp = RS._base_sp(N, I, rep, LS)
            fills = [[[] for _ in range(N)] for _ in range(I)]
        else:
            sp, fills = founders_H(N, I, rep, renorm_no_source=c['renorm'])
        self.sp0, self.fills0 = sp, fills
        dd = HK.new_dicts()
        self.dd = dd
        for k, v in S_['uid_py'].items(): dd['uid'][k] = v
        self.n_loaded = 0                      # caches are per job (no persistence across jobs: notes §2)
        self.tsp = -np.ones(kcap, np.int64); self.tblk = np.zeros(kcap, np.int64); self.tfl = np.zeros(kcap, np.int64)
        self.tT = np.zeros((kcap, 4), np.int64); self.tcls = np.zeros(kcap, np.int64)
        self.tsv = -np.ones(kcap, np.int64); self.tgc = np.zeros(kcap, np.int64)
        self.ntv = np.zeros(1, np.int64); self.TFREE = np.zeros(kcap, np.int64); self.TST = np.zeros(1, np.int64)
        self.tuc = -2 * np.ones((kcap, 9), np.int64); self.tcs = np.zeros(kcap, np.int64); self.tds = np.zeros(kcap, np.int64)
        self.tfix = np.zeros(kcap, np.bool_); self.tu0 = -np.ones(kcap, np.int64); self.tset = np.zeros(kcap, np.bool_)
        BCAP = 200000
        self.BKC = -np.ones((BCAP, 6), np.int64); self.BKD = -np.ones((BCAP, 6), np.int64)
        self.nbk = np.zeros(1, np.int64)
        FCAP = 2000000
        self.FN = np.zeros(FCAP, np.int64); self.FP = np.zeros((FCAP, 4), np.int64)
        self.nfl = np.zeros(1, np.int64); self.LFREE = np.zeros(FCAP, np.int64); self.LST = np.zeros(1, np.int64)
        self.inert = inert_map(c['inert'])
        st = HK.KState()
        for nm, arr in (('RES', gh.RES), ('TAUP', S_['TAUP']), ('NTAGS', gh.ntags), ('INERT', self.inert),
                        ('AMASK', S_['AMASK']), ('KIND', S_['KIND']), ('NAT', S_['NAT']), ('CHC', S_['CHC']),
                        ('CHD', S_['CHD']), ('UVt', S_['UVt']), ('BLC', S_['BLC']), ('BLD', S_['BLD']),
                        ('A', S_['A']), ('selfa', S_['selfa']), ('inO', S_['inO']), ('PRODC', S_['PRODC']),
                        ('PD', S_['PD']), ('ACTT', S_['ACTT']), ('LEAFT', S_['LEAFT']), ('FUT', S_['FUT']),
                        ('CLEAF', S_['CLEAF'])):
            setattr(st, nm, np.ascontiguousarray(arr))
        st.recency = bool(c['recency'])
        st.tdict = dd['tdict']; st.uid = dd['uid']; st.bdict = dd['bdict']; st.fdict = dd['fdict']
        st.pairc = dd['pair']; st.prodcc = dd['prodc']; st.pdc = dd['pd']; st.clsc = dd['cls']; st.selfc = dd['selfv']
        for nm in ('tsp', 'tblk', 'tfl', 'tT', 'tcls', 'tsv', 'tgc', 'ntv', 'TFREE', 'TST', 'tfix', 'tu0', 'tset',
                   'tuc', 'tcs', 'tds', 'BKC', 'BKD', 'nbk', 'FN', 'FP', 'nfl', 'LFREE', 'LST'):
            setattr(st, nm, getattr(self, nm))
        self.ctr = np.zeros(HK.NCT, np.int64)
        st.tmp = np.zeros(8, np.int64); st.ctr = self.ctr
        st.tstamp = np.zeros(kcap, np.int64); st.PCK = -np.ones(1 << 21, np.int64)
        st.PCV = np.zeros(1 << 21, np.int64); st.PCS = np.zeros(1 << 21, np.int64)
        self.st = st
        HK.block_of(st, 0, 0)
        HK.fl_of(st, 0, np.zeros(8, np.int64))
        self.P = np.array([c['p_copy'], c['p_contract'], float(c['grudge_only']), float(c['shuffle']),
                           float(c['clone']), 1.0 if c['grammar'] == 'H' else 0.0, float(c['noinherit'])])
        self.err = np.zeros(1, np.int64)
        self.scope_ex = np.zeros(6, np.int64); self.src_ex = np.zeros(4, np.int64)
        self.slots = np.zeros((I, N), np.int64)
        for i in range(I):
            for j in range(N):
                fl = self.fill_list(fills[i][j])
                k = HK.make_type(st, int(sp[i, j]), 0, fl)
                assert k >= 0
                self.slots[i, j] = k
        # the reference panel (pinned): FairBot-, PrudentBot-, CooperateBot-, DefectBot-, AP-H units as P types
        self.panel = {}
        names = S_['LS']['names']
        for nm, spn in [('FB', 'if(CHK(them,me,C),C,D)'), ('PB', 'if(CHK(them,me,C),if(CHK(them,^D,D),C,D),D)'),
                        ('CB', 'C'), ('DB', 'D'), ('AP', 'if(CHK(them,^D,D),D,C)')]:
            k_sp = names.index(spn)
            u = int(S_['LS']['Hu'][S_['LS']['tau'][k_sp]])
            _, cs, ds = S_['U'].units[u]
            b = HK.block_of(st, pack_block(cs), pack_block(ds))
            k = HK.make_type(st, k_sp, b, 0)
            self.panel[nm] = k
            self.tgc[k] += 10 ** 12
        self.counts = np.zeros((I, kcap), np.int64)
        for i in range(I):
            np.add.at(self.counts[i], self.slots[i], 1)
        np.add.at(self.tgc, self.slots.ravel(), 1)
        self.pres = np.zeros((I, N), np.int64); self.npres = np.zeros(I, np.int64)
        self.pos = -np.ones((I, kcap), np.int64)
        for i in range(I):
            ks = np.nonzero(self.counts[i])[0]
            for tt, k in enumerate(ks):
                self.pres[i, tt] = k; self.pos[i, k] = tt
            self.npres[i] = len(ks)
        self.paysum = np.zeros((I, kcap))
        HK.init_paysum(self.st, self.counts, self.paysum, self.pres, self.npres)
        self.spcount = np.zeros((I, gh.S), np.int64)
        for i in range(I):
            np.add.at(self.spcount[i], sp[i], 1)
        self.uns = np.array([sum(0 if self.tset[int(k)] else 1 for k in self.slots[i]) for i in range(I)],
                            np.int64)
        self.lin = (np.arange(I)[:, None] * N + np.arange(N)[None, :] + 1).astype(np.int64)
        self.maj_k = np.zeros(I, np.int64); self.maj_n = np.zeros(I, np.int64)
        self.merged = False
        self.mark = np.zeros(self.FN.shape[0], np.bool_)
        self.n_gc = 0

    def fill_list(self, fl):
        tmp = np.zeros(8, np.int64)
        for q, (t, sc, key, act, src) in enumerate(fl):
            tmp[q] = HK.fpack(t, sc, key, act, src)
        return HK.fl_of(self.st, len(fl), tmp)

    def gc(self):
        """Free types with no individual (and not pinned), then fill lists no type references."""
        n1 = HK.gc_types(self.st)
        n2 = HK.gc_lists(self.st, self.mark)
        self.n_gc += 1
        return n1, n2

    def advance(self, gens):
        for _ in range(gens):
            if self.ntv[0] - self.TST[0] > 0.8 * self.tsp.shape[0] or \
                    self.nfl[0] - self.LST[0] > 0.8 * self.FN.shape[0]:
                self.gc()
            m = 0.0 if self.merged else self.mN / self.N
            self.g = HK.segment(self.st, self.g, 1, self.seed, self.fseed, self.N, RS.W, m, self.r, self.rf,
                                self.slots, self.counts, self.paysum, self.pres, self.npres, self.pos, self.spcount,
                                self.lin, True, self.P, self.err, self.uns, self.scope_ex, self.src_ex)
            if self.err[0] != 0:
                raise RuntimeError('kernel error %d in %s rep %d at generation %d (types %d)' % (
                    self.err[0], self.cell, self.rep, self.g, self.ntv[0]))

    def merge(self):
        """Fission-fusion: all islands into one population (as the Pangaea run's merge; migration off; the event
        index continues; the seed changes to the Pangaea run's merge seed)."""
        import pangaea as PG
        I, N = self.I, self.N
        T = I * N
        kcap = self.tsp.shape[0]
        self.slots = self.slots.reshape(1, T).copy()
        self.lin = self.lin.reshape(1, T).copy()
        self.N, self.I = T, 1
        self.counts = np.zeros((1, kcap), np.int64)
        np.add.at(self.counts[0], self.slots[0], 1)
        ks = np.nonzero(self.counts[0])[0]
        self.pres = np.zeros((1, T), np.int64); self.npres = np.array([len(ks)], np.int64)
        self.pos = -np.ones((1, kcap), np.int64)
        for tt, k in enumerate(ks):
            self.pres[0, tt] = k; self.pos[0, k] = tt
        self.paysum = np.zeros((1, kcap))
        HK.init_paysum(self.st, self.counts, self.paysum, self.pres, self.npres)
        self.spcount = self.spcount.sum(0, keepdims=True)
        self.uns = np.array([sum(0 if self.tset[int(k)] else 1 for k in self.slots[0])], np.int64)
        self.maj_k = np.zeros(1, np.int64); self.maj_n = np.zeros(1, np.int64)
        self.seed = PG.kernel_seed_pg(T, 1, self.rep) ^ 0x5DEECE66D
        self.merged = True

    # -------------------------------------------------------------------------------- statistics
    def acts(self, a, b):
        return HK.acts(self.st, int(a), int(b))

    def mutual(self, a, b):
        x, y = self.acts(a, b)
        return x == 1 and y == 1

    def island_stats(self):
        return HK.island_stats(self.st, self.counts, self.pres, self.npres, self.N, self.maj_k,
                               self.maj_n)

    def living(self):
        nt = int(self.ntv[0])
        gc = self.counts[:, :nt].sum(0)
        K = np.nonzero(gc)[0]
        return K, gc[K]

    def is_identity(self, x, living):
        """Held identity (spelling level): self-cooperating, mutual with no panel unit, and every living type mutual
        with it has its spelling."""
        if not self.mutual(x, x): return False
        for nm, k in self.panel.items():
            if self.mutual(x, k): return False
        spx = self.tsp[x]
        for j in living:
            if j != x and self.tsp[j] != spx and self.mutual(x, j): return False
        return True

    def classify(self, cc):
        """World K's island classifier with the hooked holders' open / identity bits."""
        I = self.I
        H = sorted(set(int(k) for k in self.maj_k.tolist()))
        hix = {k: n for n, k in enumerate(H)}
        nh = len(H)
        mutual = np.zeros((nh, nh), bool)
        for a in range(nh):
            for b in range(a, nh):
                v = self.mutual(H[a], H[b])
                mutual[a, b] = mutual[b, a] = v
        K, gcnt = self.living()
        openv = np.array([self.mutual(h, self.panel['FB']) for h in H])
        target = np.array([self.mutual(h, self.panel['PB']) for h in H])
        ident = np.array([self.is_identity(h, K) for h in H])
        selfc = np.array([mutual[n, n] for n in range(nh)])
        hol = [hix[int(k)] for k in self.maj_k.tolist()]
        held = np.array([selfc[hol[i]] and cc[i] >= 0.5 for i in range(I)])
        cl = RS.classify(hol, held, mutual, openv, ident)
        hooked = np.array([self.tsp[h] >= statics()['gh'].NP for h in H])
        uot = bool(cl['universal_open'] and all(target[hol[i]] for i in range(I) if held[i]))
        return dict(H=H, hol=hol, held=held, cl=cl, openv=openv, ident=ident, hooked=hooked, target=target, uot=uot)

    def network(self):
        """A merged population's dominant network (the Pangaea run's decomposition, with the hooked pair values)."""
        import pangaea_kern as PGK
        K, c = self.living()
        n = len(K)
        M = np.zeros((n, n), np.bool_)
        for a in range(n):
            for b in range(a, n):
                v = self.mutual(K[a], K[b])
                M[a, b] = M[b, a] = v
        selfc = np.diag(M).copy()
        S = np.nonzero(selfc)[0].astype(np.int64)
        cf = c.astype(float); tot = cf.sum()
        out = dict(n_types=int(n), coop=float(cf[S].sum() / tot))
        if len(S):
            net = PGK.dominant_network(M, S, cf, K.astype(np.int64))
            hk = int(K[net[0]])
            inM = np.zeros(n, bool); inM[net] = True
            idm = sum(cf[a] for a in range(n) if selfc[a] and self.is_identity(K[a], K))
            out.update(M=float(cf[inM].sum() / tot), h_open=bool(self.mutual(hk, self.panel['FB'])),
                       h_target=bool(self.mutual(hk, self.panel['PB'])), h_sp=int(self.tsp[hk]),
                       ident=float(idm / tot))
        else:
            out.update(M=0.0, h_open=False, h_target=False, h_sp=-1, ident=0.0)
        out['universal_open'] = bool(out['M'] >= 0.95 and out['h_open'])
        return out

    def fill_stats(self):
        """Held fills by scope and source; applicable and selected by scope (hooks_r_kern.fill_stats)."""
        held, appl, sel, ih = HK.fill_stats(self.st, self.counts, self.pres, self.npres)
        return dict(held=held.tolist(), applicable=appl.tolist(), selected=sel.tolist(), inert_held=float(ih))

    def _is_win(self, f, sp, tag, kind, osp, ocl, q):
        best = -1; br = -1
        for i in range(self.FN[f]):
            p = int(self.FP[f, i])
            if p & 3 != tag: continue
            sc = (p >> 2) & 7
            if self.inert[(p >> 6) & 3, sc]: continue
            if not HK.key_holds(sc, (p >> 8) - 3, kind, osp, ocl, sp): continue
            rk = 1 if self.c['recency'] else int(RANK[sc])
            if rk >= br: best, br = i, rk
        return best == q

    def save(self):
        return 0

    # -------------------------------------------------------------------------------- the mass-based classifier
    def net_stats(self, cc=None):
        """Island classification by cooperation mass (notes §2: fill lists fragment islands into many types of one
        spelling, so world K's majority-type classifier does not apply).  Per island: held (within-island P(C,C) >=
        0.5), open share (residents mutual with FairBot-H), target share (mutual with PrudentBot-H), own-spelling
        share of its residents' mutual cooperation; between islands: the mutual-cooperation mass of resident pairs.
        Classes: open (held, open share >= 0.5, in the main network), identity (held, not open, >= 0.95 of its
        residents' mutual cooperation with their own spelling), rival (held, otherwise), unheld.  Universal-open: every
        island open and every island pair's cross mutual mass >= 0.5.  A merged population: universal-open iff its
        P(C,C) >= 0.9 and open share >= 0.9."""
        if cc is None: cc = self.island_stats()
        K, gcnt = self.living()
        K = K.astype(np.int64)
        ref = np.array([self.panel[nm] for nm in ('FB', 'PB', 'CB', 'DB', 'AP')], np.int64)
        M, Rr = HK.mutual_types(self.st, K, ref)
        Cm = self.counts[:, K].astype(float)               # I x T
        N = self.N
        sp = self.tsp[K]
        I = self.I
        fbs = (Cm @ Rr[:, 0]) / N; pbs = (Cm @ Rr[:, 1]) / N
        out = dict(pcc=float(np.mean(cc)), open_share=fbs.tolist(), target_share=pbs.tolist())
        if I == 1:
            out['uo'] = bool(cc[0] >= 0.9 and fbs[0] >= 0.9)
            out['uot'] = bool(out['uo'] and pbs[0] >= 0.9)
            out['n_types'] = int(len(K))
            # spelling-confined cooperation mass (identity) over the population
            same = sp[:, None] == sp[None, :]
            mm = M & ~np.eye(len(K), dtype=bool)
            w = Cm[0]
            tot = w @ mm @ w; own = w @ (mm & same) @ w
            out['own_share'] = float(own / tot) if tot > 0 else None
            out['lost'] = bool(cc[0] < 0.05)
            return out
        Mf = M.astype(np.float32)
        CM = Cm.astype(np.float32) @ Mf                       # I x T: each island's mutual mass with each type
        X = (CM @ Cm.T.astype(np.float32)).astype(float) / float(N * N)   # cross-island mutual mass
        wtot = Cm.sum(0)
        tot_mut = CM.astype(float) @ wtot                   # each island's residents' mutual mass with everyone
        # the part with their own spelling: sum over spellings s of (island mass of s) x (mutual of s with s-typed)
        own_mut = np.zeros(I)
        for s_ in np.unique(sp):
            idx = np.nonzero(sp == s_)[0]
            if len(idx) == 0: continue
            sub = Mf[np.ix_(idx, idx)].astype(float) @ wtot[idx]
            own_mut += Cm[:, idx] @ sub
        own_share = np.where(tot_mut > 0, own_mut / np.maximum(tot_mut, 1e-12), 0.0)
        held = cc >= 0.5
        openi = held & (fbs >= 0.5)
        cls = []
        # main network: open islands connected to the largest open block by cross mass >= 0.5 with all its members
        idx = [i for i in range(I) if openi[i]]
        main = []
        if idx:
            hub = max(idx, key=lambda i: (sum(1 for j in idx if X[i, j] >= 0.5), -i))
            main = [i for i in idx if X[i, hub] >= 0.5 and X[hub, i] >= 0.5]
        ms = set(main)
        for i in range(I):
            if not held[i]: cls.append('u')
            elif i in ms: cls.append('o')
            elif (fbs[i] < 0.5) and own_share[i] >= 0.95: cls.append('i')
            else: cls.append('r')
        pairwise = all(X[i, j] >= 0.5 for i in main for j in main)
        uo = all(c == 'o' for c in cls) and pairwise
        out.update(cls=''.join(cls), uo=bool(uo), uot=bool(uo and all(pbs[i] >= 0.5 for i in range(I))),
                   n_ident=cls.count('i'), n_rival=cls.count('r'), n_unheld=cls.count('u'),
                   own_share=[round(float(x), 4) for x in own_share], n_types=int(len(K)),
                   cross_min=float(min((X[i, j] for i in main for j in main), default=0.0)),
                   lost=bool(not held.any()))
        maj_sp = []
        for i in range(I):
            ks = self.pres[i, :self.npres[i]]
            spc = {}
            for k in ks: spc[int(self.tsp[k])] = spc.get(int(self.tsp[k]), 0) + int(self.counts[i, k])
            s0 = max(spc, key=spc.get)
            maj_sp.append((s0, spc[s0] / N))
        out['maj_sp'] = [m[0] for m in maj_sp]; out['maj_sp_share'] = [round(m[1], 3) for m in maj_sp]
        gh = statics()['gh']
        out['maj_hooked'] = [bool(m[0] >= gh.NP) for m in maj_sp]
        return out
