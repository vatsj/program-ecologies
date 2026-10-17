"""Legitimate detectors: a grudge rule for gentle source-readers (spec specs/2026-10-17-legitimate-detectors.md,
notes notes/detectors.md, predictions predictions/2026-10-17-legitimate-detectors.md).

Imports milestone 4's checker, milestone 5's genes and tables, provenance and the later population machinery
unchanged, and adds:
  1. the Key rule (script node 27): the checker term gains one `cond` clause after every existing clause (so every
     existing check runs the identical computation), the host replay checker the same clause;
  2. world K: every hypothesis-closed D script is keyed to the bare source of the partner it was produced against
     (the D step's partner is ⌜D⌝); terms of population units are built with that reading (`key_term_K`);
  3. grudge certificates Key_{bare(P)}[δ] (a keyed copy of the holder's own D-step script) and the term-level gate
     battery (notes §1.2);
  4. builders of the K tables (the milestone-5 closure under the keyed reading) and of the grudge pair tables W, AG1,
     AG2 (host replay with explicit keyed lists).
"""
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lt_code as L
import lt_cert as C
import lt_genes as G
import lt_genes_pop as GP
import carrier_populations as CP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'detectors')
os.makedirs(OUT, exist_ok=True)
K = 10 ** 6
V = K // 4
PCAP = K // 4
KEY = 27
DET_SP = 'if(or(CHK(them,them,D),CHK(me,them,D)),D,C)'

# ----------------------------------------------------------------------------------------------------------------
# 1. The Key rule
# ----------------------------------------------------------------------------------------------------------------
_CCHK_OLD = "((eq rule 25) (cchkr cx ps L R (fnth R j)))\n          (else 0))))"
_CCHK_NEW = ("((eq rule 25) (cchkr cx ps L R (fnth R j)))\n          ((eq rule 27) (ckey cx j ps L R))\n"
             "          (else 0))))")
assert C.CERT_SRC.count(_CCHK_OLD) == 1
CERT_SRC_K = C.CERT_SRC.replace(_CCHK_OLD, _CCHK_NEW)
KEY_SRC = r"""
; ---------------- the Key rule (code 27): node (27 . (k . (p . 0))), valid iff k = bare(m) and p is valid ----------------
(def bareof (t)
  (if (eq (fst t) 1)
    (let ((b1 (snd t)))
      (if (eq (fst b1) 1)
        (let ((b2 (snd b1)))
          (if (eq (fst b2) 2)
            (let ((l (snd b2)))
              (if (eq (fst (fst l)) 1) (snd (fst l)) t))
            t))
        t))
    t))
(def ckey (cx k ps L R)
  (let ((arg (snd (snd (fst (snd cx))))) (m (fst (snd (snd arg)))))
    (if (eq k (bareof m)) (cchk cx (fst ps) L R) 0)))
"""
LIB_STATE = {'which': 'base'}


def install_library(which='key'):
    """Rebuild lt_code's library: 'key' = milestone 5's library with the Key clause in cchk and KEY_SRC appended
    (every earlier index unchanged, asserted); 'base' = lt_genes.build_gene_library() (the stored library)."""
    if LIB_STATE['which'] == which: return
    if which == 'base':
        G.build_gene_library()
        LIB_STATE['which'] = 'base'
        return
    before = dict(L.LIBIDX)
    comp = L.SxCompiler()
    for k, v in L.LIB_CONSTS.items(): comp.consts[k] = v
    for k, v in C.CERT_CONSTS.items(): comp.consts[k] = v
    comp.load(L.LIBRARY_SRC)
    comp.load(CERT_SRC_K)
    comp.load(G.GENE_SRC)
    comp.load(KEY_SRC)
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
    L.CORE_LIBS[L.LIBIDX['PCORE']] = G.PCORE_ID_CODE
    L._compiled.clear()
    L.LIBCODE[:] = [L.compile_term(t[1]) for t in terms]
    L.CACHE.clear()
    C.ID.clear(); C.ID.update({nm: L.LIBIDX[nm] for nm in C.WRAP_NAMES})
    C.WRAPS.clear(); C.WRAPS.update(C.ID.values())
    C.CC_MODE.clear(); C.CC_MODE.update({L.LIBIDX[nm]: mode for nm, mode in C.CORE_NAMES.items()})
    C.WRAP_MODE.clear(); C.WRAP_MODE.update({L.LIBIDX[C.MODE_WRAP[m]]: m for m in C.MODE_WRAP})
    LIB_STATE['which'] = 'key'


def bare(q):
    """The bare source of a program term: a carrier's body (list stripped), else the term itself."""
    try:
        if q[0] == 'lam' and q[1][0] == 'lam' and q[1][1][0] == 'app' and q[1][1][1][0] == 'lam':
            return q[1][1][1][1]
    except Exception:
        pass
    return q


def key_of(q):
    """The key datum of a program term: the canonical encoding of its bare source (nested ints, as `eq` compares)."""
    return L.canon_term(bare(q))


KEY_D = key_of(L.PROG_D)


def keyed(script, k):
    return (KEY, (k, (script, 0)))


def unkey(script):
    return script[1][1][0] if script[0] == KEY else script


_HOST_CCHK = C.HostCheck.cchk


def _host_cchk_k(self, mode, Rb, Sb, V_, nd, Lf, Rf):
    try:
        rule, (j, ps) = nd
    except Exception:
        return 0
    if rule == KEY:
        fs = C.h_argfields(Rb[2]) if (Rb is not None and Rb[0] == 'cbox') else None
        if fs is None: return 0
        if j != key_of(fs[2]): return 0
        ps = C.uncons(ps)
        if not ps: return 0
        return self.cchk(mode, Rb, Sb, V_, ps[0], Lf, Rf)
    return _HOST_CCHK(self, mode, Rb, Sb, V_, nd, Lf, Rf)


C.HostCheck.cchk = _host_cchk_k          # the host replay checker with the Key clause (a no-op on keyless lists)


def has_hyp(s):
    r, (j, ps) = s
    if r == C.HYP: return True
    if r == KEY: return has_hyp(ps[0])
    return any(has_hyp(p) for p in C.uncons(ps))


# ----------------------------------------------------------------------------------------------------------------
# 2. World K
# ----------------------------------------------------------------------------------------------------------------
WORLD = {'w': 'L'}
_KEY_TERM_L = GP.key_term


def key_term_K(U, key, marker):
    """A unit's term in world K: hypothesis-closed D scripts keyed to ⌜D⌝ (the D step's partner)."""
    t, cs, ds = key
    body = G.marked_body(U.bodies[t], marker)
    dl = [U.scripts[i][1] for i in ds]
    dl = [keyed(s, KEY_D) if has_hyp(s) else s for s in dl]
    return C.carrier(body, G.canon_list([U.scripts[i][1] for i in cs], dl))


def set_world(w):
    WORLD['w'] = w
    GP.key_term = key_term_K if w == 'K' else _KEY_TERM_L


def grudge_term(U, u, marker, keys, sham=False):
    """Unit u's term (world K reading) with grudges Key_k[δ_u] appended to its D block for each key datum k (δ_u: the
    unit's hypothesis-closed D script).  sham: the entries carry a key no quote has (checking disabled)."""
    t, cs, ds = U.units[u]
    body = G.marked_body(U.bodies[t], marker)
    dl0 = [U.scripts[i][1] for i in ds]
    hyp = [s for s in dl0 if has_hyp(s)]
    assert hyp, 'not a writer unit'
    dl = [keyed(s, KEY_D) if has_hyp(s) else s for s in dl0]
    for k in keys:
        dl.append(keyed(hyp[0], SHAM_KEY if sham else k))
    return C.carrier(body, G.canon_list([U.scripts[i][1] for i in cs], dl))


SHAM_KEY = 0             # a natural: no bare source encodes to a bare natural (canon_term is always a pair)


def _winit_K(K_, P_, sync_dir=None):
    """Pool initializer: the stored worker state under the world-K reading (spawned workers re-import modules)."""
    set_world('K')
    GP._winit(K_, P_, sync_dir)


# ----------------------------------------------------------------------------------------------------------------
# 3. The gate (notes §1.2): executed at the term level with the extended library
# ----------------------------------------------------------------------------------------------------------------
def catalogue():
    cat = CP.Catalogue(7, 'P', K)
    names = [cat.name(k) for k in range(len(cat.spell))]
    return cat, names


def prog(cat, names, sp, certs=()):
    """The program term of a grammar spelling with an explicit list [(a, script), ...] (unmarked body)."""
    k = names.index(sp)
    return CP.program(cat.sexprs[cat.spell[k]['i']], C.cons(list(certs)) if certs else 0, V, K)


def synonyms(cat, names, sp):
    k = names.index(sp)
    t = int(cat.tau[k])
    return [names[j] for j in cat.members[t] if names[j] != sp]


def chk(t, m, a):
    """Executed sound check: (value, inner steps)."""
    return C.check_value(0, V, t, m, a, K)


def play(p, q):
    return L.play(p, q, K)[0]


def host_chk(t, m, a):
    h = CP.IdealCheck()
    return h.check(C.ID['CHKS'], C.mk_arg(V, t, m, a, K))


def gate(n_sample=240, seed=20261017, log=print):
    """The go/no-go battery (notes §1.2).  Returns a JSON-able report; report['go'] is the verdict."""
    t0 = time.time()
    sys.setrecursionlimit(1000000)
    cat, names = catalogue()
    rep = {'checks': []}
    bad = []

    def record(tag, t, m, a, expect=None):
        L.CACHE.clear()
        v, n = chk(t, m, a)
        hv = host_chk(t, m, a)
        atom = None
        if v == 'T':
            atom = play(t, m) == a
            if not atom: bad.append(tag + ' (false atom)')
        if hv != v: bad.append(tag + ' (host %s != term %s)' % (hv, v))
        row = dict(tag=tag, a=a, value=v, host=hv, steps=n, atom_true=atom, expect=expect,
                   as_expected=(None if expect is None else v == expect))
        rep['checks'].append(row)
        if expect is not None and v != expect: bad.append(tag + ' (unexpected %s)' % v)
        log('  %-62s %s %-2s host %-2s steps %7d atom %s' % (tag, a, v, hv, n, atom))
        return v

    # ---- g1: conservativeness on a sample of stored checks (base library, then the Key library)
    install_library('base')
    import provenance_run as PR
    st, meta = GP.load_static(os.path.join(PR.OUT, 'static'))
    U = GP.Universe(K, PCAP)
    U.scripts = list(meta['scripts']); U.units = list(meta['units'])
    O = np.asarray(st['O'])
    rng = np.random.default_rng(seed)
    samp = []
    while len(samp) < n_sample:
        u = int(rng.choice(O)); m = int(rng.choice(O))
        t_, cs, ds = U.units[u]
        a = 'C' if (cs and (not ds or rng.random() < 0.5)) else ('D' if ds else None)
        if a is None: continue
        samp.append((u, m, a))
    terms = {}

    def uterm(u, mk):
        if (u, mk) not in terms: terms[(u, mk)] = _KEY_TERM_L(U, U.units[u], mk)
        return terms[(u, mk)]
    base_vals = []
    for u, m, a in samp:
        L.CACHE.clear()
        base_vals.append(chk(uterm(u, 'H'), uterm(m, 'H' if m != u else 'C'), a))
    install_library('key')
    diff = 0
    for (u, m, a), b in zip(samp, base_vals):
        L.CACHE.clear()
        k_ = chk(uterm(u, 'H'), uterm(m, 'H' if m != u else 'C'), a)
        if k_ != b: diff += 1
    vals = [v for v, n in base_vals]
    rep['g1'] = dict(n=len(samp), differences=diff, T=vals.count('T'), F=vals.count('F'), TO=vals.count('TO'),
                     median_steps=float(np.median([n for v, n in base_vals])))
    log('g1: %d sampled stored checks (T %d, F %d, TO %d), %d differences in value or steps' % (
        len(samp), vals.count('T'), vals.count('F'), vals.count('TO'), diff))
    if diff: bad.append('g1')

    # ---- programs
    prod = C.Producer(host=CP.ExactHost())
    det0 = prog(cat, names, DET_SP)
    delta = prod.produce(0, det0, L.PROG_D, 'D', K, V)
    rep['delta'] = C.show_script(delta)
    rep['delta_is_stored_script_10'] = bool(delta == U.scripts[10][1])
    fb = _KEY_TERM_L(U, U.units[3], 'H')                     # FairBot-H (unit 3)
    pbsp = 'if(CHK(them,me,C),if(CHK(them,^D,D),C,D),D)'
    pbt = int(cat.tau[names.index(pbsp)])
    pbH = _KEY_TERM_L(U, U.units[int(meta['H_unit'][pbt])], 'H')
    sigC = prod.produce(0, det0, fb, 'C', K, V)
    rep['sigma_C'] = C.show_script(sigC) if sigC else None
    log('δ = %s (stored script 10: %s); σ_C (det, empty list, vs FairBot-H) = %s' % (
        rep['delta'], rep['delta_is_stored_script_10'], rep['sigma_C']))
    PSP = 'if(CHK(them,me,C),D,C)'                           # defects against certified cooperators
    P = prog(cat, names, PSP)                                # (empty list: not a certified self-defector)
    syn = synonyms(cat, names, PSP)
    Psyn = prog(cat, names, syn[0])                          # a respelling of it (a fresh source)
    rep['P'] = PSP + ' (empty list)'; rep['P_syn'] = syn[0]
    Pcert = prog(cat, names, PSP, [('C', C.node(C.EVS, 0, C.node(C.AX, 0)))])   # P carrying a certificate
    Cb = prog(cat, names, 'C')
    kP = key_of(P)
    assert key_of(Pcert) == kP and key_of(Psyn) != kP

    # ---- the L detector (unkeyed δ) by execution
    detL = prog(cat, names, DET_SP, [('D', delta)])
    rep['L_detector'] = dict(vs_C=play(detL, Cb), vs_self=play(detL, detL), vs_FB=play(detL, fb), vs_PB=play(detL, pbH))
    log('L detector [δ] plays: vs CooperateBot %(vs_C)s, own quote %(vs_self)s, FairBot-H %(vs_FB)s, '
        'PrudentBot-H %(vs_PB)s' % rep['L_detector'])
    if rep['L_detector']['vs_C'] != 'D': bad.append('L detector gentle')
    record('L det [δ] vs CooperateBot (generic self-hypothesis D)', detL, Cb, 'D', 'T')

    # ---- world K detector: σ_C and Key_⌜D⌝[δ]
    detK = prog(cat, names, DET_SP, [('C', sigC), ('D', keyed(delta, KEY_D))])
    log('K detector and grudges (g2-g4)')
    record('K det vs ⌜D⌝: Key_⌜D⌝[δ] matches', detK, L.PROG_D, 'D', 'T')
    record('K det vs P, no grudge', detK, P, 'D', 'F')
    rep['K_det_vs_P_nogrudge'] = (play(detK, P), play(P, detK))
    detG = prog(cat, names, DET_SP, [('C', sigC), ('D', keyed(delta, KEY_D)), ('D', keyed(delta, kP))])
    record('g2 det+Key_P[δ] vs P', detG, P, 'D', 'T')
    rep['g2_play'] = (play(detG, P), play(P, detG))
    record('g3 det+Key_P[δ] vs respelled P', detG, Psyn, 'D', 'F')
    rep['g3_play_syn'] = play(detG, Psyn)
    record('g3 det+Key_P[δ] vs CooperateBot', detG, Cb, 'D', 'F')
    rep['g3_play_C'] = play(detG, Cb)
    record('g3 det+Key_P[δ] C-cert vs CooperateBot', detG, Cb, 'C', 'T')
    record('g3 det+Key_P[δ] C-cert vs P (RunNeg on own D box fails)', detG, P, 'C', 'F')
    record('g4 det+Key_P[δ] vs P carrying a certificate', detG, Pcert, 'D', 'T')
    rep['g4_play'] = play(detG, Pcert)
    for nm, x in (('FairBot-H', fb), ('PrudentBot-H', pbH)):
        record('K det C-cert vs %s' % nm, detK, x, 'C', 'T')
        rep['K_det_vs_' + nm] = (play(detK, x), play(x, detK))
        log('    plays K det vs %s: %s / %s' % (nm, rep['K_det_vs_' + nm][0], rep['K_det_vs_' + nm][1]))
    # ---- g5: forged grudges on non-readers and negated readers
    log('g5: forged grudges')
    Cf = prog(cat, names, 'C', [('D', keyed(delta, kP))])
    record('g5 CooperateBot + Key_P[δ] vs P', Cf, P, 'D', 'F')
    fbf = prog(cat, names, 'if(CHK(them,me,C),C,D)', [('D', keyed(delta, kP))])
    rep['g5_fb'] = dict(value=record('g5 FairBot + Key_P[δ] vs P (FairBot plays D anyway)', fbf, P, 'D'),
                        play=play(fbf, P))
    neg = 'if(CHK(me,them,D),C,D)'
    hyp5 = C.node(C.EVS, 0, C.node(C.CHKR, 0, C.node(C.EVS, 0, C.node(C.AX, 0)), C.node(C.HYP, 0)))
    forged = (('δ', delta), ('EvR*; ChkR[EvR*; Ax · Hyp]', hyp5), ('Hyp', C.node(C.HYP, 0)),
              ('EvR*; ChkR[Hyp · Hyp]', C.node(C.EVS, 0, C.node(C.CHKR, 0, C.node(C.HYP, 0), C.node(C.HYP, 0)))),
              ('EvR*; ChkR[Ax · Hyp]', C.node(C.EVS, 0, C.node(C.CHKR, 0, C.node(C.AX, 0), C.node(C.HYP, 0)))))
    for nm_s, s in forged:
        ng = prog(cat, names, neg, [('D', keyed(s, kP))])
        record('g5 negated reader + Key_P[%s] vs P' % nm_s, ng, P, 'D', 'F')
        rep.setdefault('g5_neg_play', []).append(play(ng, P))
    eff1 = 'if(CHK(me,them,D),D,C)'
    e0 = prog(cat, names, eff1)
    hypE = prod.produce(0, e0, L.PROG_D, 'D', K, V)
    rep['delta_eff1'] = C.show_script(hypE)
    # ---- g6: mutual grudges between two own-D readers
    log('g6: mutual grudges (the detector and %s)' % eff1)
    detM = prog(cat, names, DET_SP, [('C', sigC), ('D', keyed(delta, KEY_D)), ('D', keyed(delta, key_of(e0)))])
    effM = prog(cat, names, eff1, [('D', keyed(hypE, KEY_D)), ('D', keyed(hypE, key_of(det0)))])
    record('g6 det(grudge vs eff) vs eff(grudge vs det)', detM, effM, 'D', 'T')
    record('g6 eff(grudge vs det) vs det(grudge vs eff)', effM, detM, 'D', 'T')
    rep['g6_plays'] = (play(detM, effM), play(effM, detM))
    effK = prog(cat, names, eff1, [('D', keyed(hypE, KEY_D))])
    record('K %s (keyed δ) vs CooperateBot: sucker without grudges' % eff1, effK, Cb, 'D', 'F')
    rep['K_eff1_vs_C'] = play(effK, Cb)
    # ---- g8: verification cost against list length
    others = [prog(cat, names, s) for s in names[2:40]]
    cost = {}
    for g in (0, 1, 3, 16):
        keys = ([key_of(x) for x in others[:g - 1]] + [kP]) if g else []
        dl = [('C', sigC), ('D', keyed(delta, KEY_D))] + [('D', keyed(delta, k)) for k in keys]
        dg = prog(cat, names, DET_SP, dl)
        L.CACHE.clear(); vC, nC = chk(dg, Cb, 'D')
        L.CACHE.clear(); vP, nP = chk(dg, P, 'D')
        L.CACHE.clear(); vCC, nCC = chk(dg, Cb, 'C')
        L.CACHE.clear(); pv, pn = L.play(dg, Cb, K)
        cost[g] = dict(chkD_vs_C=[vC, nC], chkD_vs_P=[vP, nP], chkC_vs_C=[vCC, nCC], play_vs_C=[pv, pn])
        log('g8: %2d grudges: CHK(det,C,D) %s %6d; CHK(det,P,D) %s %6d; CHK(det,C,C) %s %6d; play vs C %s %6d steps'
            % (g, vC, nC, vP, nP, vCC, nCC, pv, pn))
    rep['g8'] = cost
    rep['bad'] = bad
    rep['go'] = not any(('false atom' in b) or b == 'g1' or ('host' in b) for b in bad)
    rep['unexpected'] = [b for b in bad if 'unexpected' in b]
    rep['time_s'] = time.time() - t0
    return rep


# ----------------------------------------------------------------------------------------------------------------
# 4. World K's tables beyond the closure, and the grudge pair tables
# ----------------------------------------------------------------------------------------------------------------
KDIR = os.path.join(OUT, 'K')
RD_ATOM = (0, 'me', 'them', 'D')


def eff_trees(cat):
    """Own-D readers: run trees with a CHK(me,them,D) atom such that, for some value of the other atoms, the run plays
    C with the atom F and D with it T."""
    import itertools
    out = []
    for t in range(cat.T):
        ats = sorted(set(cat.tau_atoms[t]))
        if RD_ATOM not in ats: continue
        others = [x for x in ats if x != RD_ATOM]
        hit = False
        for vals in itertools.product([False, True], repeat=len(others)):
            m = dict(zip(others, vals))
            fF = CP.eval_dt(cat.tau_dt[t], lambda at: False if at == RD_ATOM else m[at])
            fT = CP.eval_dt(cat.tau_dt[t], lambda at: True if at == RD_ATOM else m[at])
            if fF == 1 and fT == 0: hit = True
        if hit: out.append(t)
    return out


def lot_static_K():
    """provenance_run.lot_static read from runs/detectors/K (world K's static, prod_exec, sets, OSV, SPO)."""
    import provenance_run as PR
    if 'K' in PR._LS: return PR._LS['K']
    old_out, old_ls = PR.OUT, dict(PR._LS)
    PR.OUT = KDIR
    PR._LS.clear()
    try:
        LS = PR.lot_static('ext')
    finally:
        PR.OUT = old_out
        PR._LS.clear(); PR._LS.update(old_ls)
    PR._LS['K'] = LS
    return LS


def lot_static_L():
    import provenance_run as PR
    return PR.lot_static('ext')


_GW = {}


def _ginit(units, scripts):
    sys.setrecursionlimit(1000000)
    set_world('K')
    U = GP.Universe(K, PCAP)
    U.scripts = list(scripts); U.sid = {k: i for i, k in enumerate(U.scripts)}
    U.units = list(units); U.uid = {k: i for i, k in enumerate(U.units)}
    _GW['U'] = U
    _GW['h'] = CP.IdealCheck()
    _GW['terms'] = {}


def _uterm(u, mk):
    tm = _GW['terms'].get((u, mk))
    if tm is None:
        tm = key_term_K(_GW['U'], _GW['U'].units[u], mk)
        if len(_GW['terms']) > 50000: _GW['terms'].clear()
        _GW['terms'][(u, mk)] = tm
    return tm


def _pair_acts(U, h, tx, x_tau, tx_term, ty, y_tau, ty_term, UVt):
    """Actions (x vs y, y vs x) with explicit terms (kinds 0/1 by host checks, kinds 2-5 from the base UVt of the
    units tx, ty, which the keyed grudge entries do not touch: a grudge's key never matches a self, ⌜C⌝ or ⌜D⌝ root)."""
    n = C.ID['CHKS']
    memo = {}

    def box(t_term, m_term, a):
        key = (id(t_term), id(m_term), a)
        if key not in memo:
            memo[key] = h.check(n, C.mk_arg(V, t_term, m_term, a, K)) == 'T'
        return memo[key]

    def act(t_unit, t_tau, t_term, m_unit, m_term):
        def val(at):
            k_, ai, qi = GP.atom_box_kind(at)
            a = 'C' if ai == 0 else 'D'
            q = '^C' if qi == 0 else '^D'
            if k_ == 0: return box(m_term, t_term, a)
            if k_ == 1: return box(t_term, m_term, a)
            if k_ == 2: return UVt[m_unit, GP.UVI[(a, 'self')]] == 1
            if k_ == 3: return UVt[t_unit, GP.UVI[(a, 'self')]] == 1
            if k_ == 4: return UVt[m_unit, GP.UVI[(a, q)]] == 1
            return UVt[t_unit, GP.UVI[(a, q)]] == 1
        return CP.eval_dt(U.tau_dt[t_tau], val)
    return act(tx, x_tau, tx_term, ty, ty_term), act(ty, y_tau, ty_term, tx, tx_term), box


def _uvt():
    if 'UVt' not in _GW:
        _GW['UVt'] = np.load(os.path.join(KDIR, 'static', 'UVt.npy'), mmap_mode='r')
    return _GW['UVt']


def _grudge_job(job):
    """job = (w, [v...]) -> rows (w, v, W, AG1 code) for the writer unit w against units v (v == w: the twin)."""
    w, vs = job
    U, h = _GW['U'], _GW['h']
    UVt = _uvt()
    out = []
    tw = U.units[w][0]
    for v in vs:
        h.clear()
        v_term = _uterm(v, 'C' if v == w else 'H')
        wg = grudge_term(U, w, 'H', [key_of(v_term)])
        a_wv, a_vw, box = _pair_acts(U, h, w, tw, wg, v, U.units[v][0], v_term, UVt)
        Wv = box(wg, v_term, 'D')
        out.append((w, v, int(Wv), int(a_wv) + 2 * int(a_vw)))
    return out


def _grudge2_job(job):
    """job = (w1, [w2...]) -> rows (w1, w2, AG2 code): both hold a grudge against the other."""
    w1, ws = job
    U, h = _GW['U'], _GW['h']
    UVt = _uvt()
    out = []
    t1 = U.units[w1][0]
    for w2 in ws:
        h.clear()
        m2 = 'C' if w2 == w1 else 'H'
        b1 = key_of(_uterm(w1, 'H')); b2 = key_of(_uterm(w2, m2))
        g1 = grudge_term(U, w1, 'H', [b2])
        g2 = grudge_term(U, w2, m2, [b1])
        a12, a21, _ = _pair_acts(U, h, w1, t1, g1, w2, U.units[w2][0], g2, UVt)
        out.append((w1, w2, int(a12) + 2 * int(a21)))
    return out


def _sham_job(job):
    """Audit: a writer with a sham grudge (a key no quote has) plays the base table against v."""
    w, vs = job
    U, h = _GW['U'], _GW['h']
    UVt = _uvt()
    out = []
    for v in vs:
        h.clear()
        v_term = _uterm(v, 'C' if v == w else 'H')
        ws_ = grudge_term(U, w, 'H', [None], sham=True)
        a_wv, a_vw, _ = _pair_acts(U, h, w, U.units[w][0], ws_, v, U.units[v][0], v_term, UVt)
        out.append((w, v, int(a_wv) + 2 * int(a_vw)))
    return out


# ----------------------------------------------------------------------------------------------------------------
# 5. Worlds, classes (notes §1.5) and the run object
# ----------------------------------------------------------------------------------------------------------------
FB_SP = 'if(CHK(them,me,C),C,D)'
PB_SP = 'if(CHK(them,me,C),if(CHK(them,^D,D),C,D),D)'
_WS = {}


def with_rr(LS, fn, *args):
    """Call a removing-rivals helper on another world's tables (its module cache is per world)."""
    import removing_rivals as RR
    saved = (dict(RR._SC), dict(RR._PH))
    RR._SC.clear(); RR._PH.clear()
    try:
        return fn(*args)
    finally:
        RR._SC.clear(); RR._SC.update(saved[0]); RR._PH.clear(); RR._PH.update(saved[1])


def world(w):
    """Statics of world w ('L' or 'K'): tables, grudge tables, natural units, DET, PBN, reference units."""
    if w in _WS: return _WS[w]
    import removing_rivals as RR
    LS = lot_static_K() if w == 'K' else lot_static_L()
    st = LS['st']
    A = np.asarray(st['A']); sa = np.asarray(st['selfa'])
    names, tau, Hu, Eu, mu = LS['names'], LS['tau'], LS['Hu'], LS['Eu'], LS['mu']
    cat = LS['cat']
    n = A.shape[0]
    uC = int(Hu[tau[names.index('C')]]); uD = int(LS['u_d']); uFB = int(Hu[tau[names.index(FB_SP)]])
    uPB = int(Hu[tau[names.index(PB_SP)]])
    kFB = names.index(FB_SP); kPB = names.index(PB_SP)
    # natural units: E unit, S-nonself C step then D step against FairBot-H (PrudentBot-H for FairBot's own spelling)
    def allnat():
        nat = np.zeros(len(names), np.int64)
        cache = {}
        for s in range(len(names)):
            t = int(tau[s])
            if s == kFB:
                nat[s] = RR.phenotype(int(Eu[t]), s, uPB, kPB, LS)
                continue
            if t not in cache:
                cache[t] = RR.phenotype(int(Eu[t]), s, uFB, kFB, LS)
            nat[s] = cache[t]
        return nat
    nat = with_rr(LS, allnat)
    eff = set(eff_trees(cat))
    effsp = np.array([int(tau[s]) in eff for s in range(len(names))])
    gentle = (sa[nat] == 1) & (A[nat, uD] == 0) & (A[nat, uC] == 1)
    T = (sa == 1) & (A[:, uPB] == 1) & (A[uPB, :] == 1)
    DET = effsp & gentle
    PBN = T[nat] & ~DET
    openu = np.asarray(LS['openu']); ident = np.asarray(LS['ident'])
    sucker = (A[:, uD] == 1).astype(np.int8)
    natu = (np.asarray(st['BLC'])[:, 0] >= 0).astype(np.int8)
    if w == 'K':
        z = np.load(os.path.join(KDIR, 'grudge.npz'))
        G_ = dict(widx=z['widx'].astype(np.int64), AG1=z['AG1'], AG2=z['AG2'], PW=z['PW'], W=z['W'],
                  wdel=z['wdel'].astype(np.int64), writers=z['writers'])
    else:
        G_ = dict(widx=-np.ones(n, np.int64), AG1=-np.ones((1, 1), np.int8), AG2=-np.ones((1, 1), np.int8),
                  PW=np.zeros((1, 1), np.int8), W=np.zeros((1, 1), np.int8), wdel=np.zeros(1, np.int64),
                  writers=np.zeros(0, np.int64))
    out = dict(w=w, LS=LS, A=A, sa=sa, names=names, tau=tau, mu=mu, Hu=Hu, Eu=Eu, nat=nat, uC=uC, uD=uD, uFB=uFB,
               uPB=uPB, kFB=kFB, kPB=kPB, effsp=effsp, DET=DET, PBN=PBN, T=T, openu=openu, ident=ident,
               sucker=sucker, natu=natu, cumL=np.cumsum(mu).astype(np.float64), spE=Eu[tau].astype(np.int64), **G_)
    _WS[w] = out
    return out


KCAP_B = 200000
KCAP_G = 60000
GMAX = 4000000
ARRCAP = 400000
GLOGCAP = 600000


class DRun:
    """One run: base types (provenance's), grudge types, the kernel state.  founders: (sp, rule, unit[, gid lists])
    arrays (I, N)."""

    def __init__(self, w, sp, rule, unit, seed, r=100, mN=1.0, gmode=0, gcap=3, epsg=None, pairmode=1, fseed=None,
                 glists=None):
        import detectors_kern as KG
        import provenance as PV
        from numba.typed import Dict
        from numba import types
        self.W = W = world(w)
        LS = self.LS = W['LS']
        st = LS['st']
        self.I, self.N = sp.shape
        I, N = self.I, self.N
        self.r, self.mN, self.gmode, self.gcap = int(r), float(mN), int(gmode), int(gcap)
        self.seed = int(seed)
        self.fseed = int((self.seed * 6364136223846793005 + 1442695040888963407) % (2 ** 62)) if fseed is None else fseed
        self.pairmode = int(pairmode)
        self.epsg = np.zeros(1) if epsg is None else np.ascontiguousarray(epsg, dtype=np.float64)
        self.d = Dict.empty(key_type=types.int64, value_type=types.int64)
        self.gdict2 = Dict.empty(key_type=types.int64, value_type=types.int64)
        self.gdict = Dict.empty(key_type=types.int64, value_type=types.int64)
        self.tunit = np.zeros(KCAP_B, np.int64); self.trule = np.zeros(KCAP_B, np.int64)
        self.tsp = np.zeros(KCAP_B, np.int64); self.tanc = np.zeros(KCAP_B, np.int64)
        self.gbase = np.zeros(KCAP_G, np.int64); self.gg = np.zeros(KCAP_G, np.int64)
        self.GS = -np.ones((GMAX, KG.GCAP_MAX), np.int64); self.GN = np.zeros(GMAX, np.int64)
        self.ngv = np.zeros(1, np.int64); self.ngt = np.zeros(1, np.int64)
        self.freel = np.zeros(KCAP_G, np.int64); self.nfree = np.zeros(1, np.int64)
        self.gcount = np.zeros(KCAP_G, np.int64)
        tmp = np.zeros(KG.GCAP_MAX + 2, np.int64)
        g0 = KG.gintern(self.gdict, self.GS, self.GN, self.ngv, tmp, 0)
        assert g0 == 0
        nt = 0
        self.slots = np.zeros((I, N), np.int64)
        bslots = np.zeros((I, N), np.int64)
        for i in range(I):
            for j in range(N):
                kb, nt = PV.make_type(self.d, self.tunit, self.trule, self.tsp, self.tanc, nt, int(unit[i, j]),
                                      int(rule[i, j]), int(sp[i, j]), 0)
                gid = 0
                if glists is not None and glists[i][j]:
                    lst = glists[i][j]
                    tmp[:len(lst)] = lst
                    gid = KG.gintern(self.gdict, self.GS, self.GN, self.ngv, tmp, len(lst))
                self.slots[i, j] = KG.gmake(self.gdict2, self.gbase, self.gg, self.ngt, kb, gid, self.freel,
                                            self.nfree)
                bslots[i, j] = kb
        self.ntv = np.array([nt], np.int64)
        np.add.at(self.gcount, self.slots.ravel(), 1)
        self.counts = np.zeros((I, KCAP_G), np.int64)
        for i in range(I):
            np.add.at(self.counts[i], self.slots[i], 1)
        self.pres = np.zeros((I, N), np.int64); self.npres = np.zeros(I, np.int64)
        self.pos = -np.ones((I, KCAP_G), np.int64)
        for i in range(I):
            ks = np.nonzero(self.counts[i])[0]
            for tt, k in enumerate(ks):
                self.pres[i, tt] = k; self.pos[i, k] = tt
            self.npres[i] = len(ks)
        self.A, self.selfa = st['A'], st['selfa']
        self.widx, self.AG1, self.AG2, self.PW, self.Wt, self.wdel = (W['widx'], W['AG1'], W['AG2'], W['PW'], W['W'],
                                                                       W['wdel'])
        self.paysum = np.zeros((I, KCAP_G))
        KG.ginit_paysum(self.counts, self.paysum, self.pres, self.npres, self.gbase, self.gg, self.GS, self.GN,
                        self.tunit, self.tsp, self.A, self.selfa, self.widx, self.AG1, self.AG2, self.PW, self.gmode)
        nsp = len(LS['mu'])
        self.spcount = np.zeros((I, nsp), np.int64)
        for i in range(I):
            np.add.at(self.spcount[i], sp[i], 1)
        self.ctr = np.zeros((PV.NRULE, PV.NCTR), np.int64)
        self.steps_rule = np.zeros(PV.NRULE)
        self.wn = np.zeros((I, N), np.int64); self.wenc = np.zeros((I, N), np.int64)
        self.wsp = np.zeros((I, N, 3), np.int64); self.wcode = np.zeros((I, N, 3), np.int64)
        self.wsid = np.zeros((I, N, 3), np.int64)
        self.ckey = np.zeros((I, N, PV.CACHE_CAP), np.int64); self.cval = np.zeros((I, N, PV.CACHE_CAP), np.int64)
        self.ncache = np.zeros((I, N), np.int64)
        self.plog = -np.ones((I, N, 5), np.int64)
        BLC = st['BLC']
        for i in range(I):
            for j in range(N):
                PV.plog_open(i, j, bslots[i, j], self.tunit, self.trule, BLC, self.plog)
        self.hist_wait = np.zeros((PV.NRULE, 2, 4, PV.NEB), np.int64)
        self.hist_acq = np.zeros((PV.NRULE, 2, PV.NEB), np.int64)
        self.hist_steps = np.zeros((PV.NRULE, PV.NSB), np.int64)
        self.hist_cens = np.zeros((PV.NRULE, 2, 2, PV.NEB), np.int64)
        self.nprod = np.zeros((PV.NRULE, 2, 4), np.int64)
        self.err = np.zeros(1, np.int64)
        self.tset = -np.ones(KCAP_B, np.int64)
        self.uns = np.zeros(I, np.int64)
        self.rulecount = np.zeros(PV.NRULE, np.int64)
        self.enc_exp = np.zeros(PV.NRULE)
        self.fcount = np.zeros(PV.NRULE, np.int64)
        self.enc_futile = np.zeros(PV.NRULE)
        PV.init_uns(bslots, self.tunit, self.trule, self.tset, st['BLC'], st['BLD'], LS['PD'], st['utau'], LS['FUT'],
                    self.uns, self.rulecount, self.fcount)
        self.skip = True
        self.g = 0
        self.rcount = np.zeros(I, np.int64)
        self.arr = np.zeros((ARRCAP, 3), np.int64); self.narr = np.zeros(1, np.int64)
        self.gctr = np.zeros(KG.NGC, np.int64)
        self.glog = np.zeros((GLOGCAP, 8), np.int64); self.nglog = np.zeros(1, np.int64)
        self.gdirty = np.ones(I, np.int64); self.glive = np.zeros(I, np.int64)
        self.isl_sucker_gen = np.zeros(2)
        self.maj_k = np.zeros(I, np.int64); self.maj_n = np.zeros(I, np.int64)

    def advance(self, gens):
        import detectors_kern as KG
        import provenance as PV
        LS, st, W = self.LS, self.LS['st'], self.W
        self.g = KG.segment_g(
            self.g, gens, self.seed, self.N, 0.3, self.mN / self.N, self.r, self.slots, self.counts, self.paysum,
            self.pres, self.npres, self.pos, self.spcount, self.d, self.tunit, self.trule, self.tsp, self.tanc,
            self.ntv, st['utau'], st['BLC'], st['BLD'], st['SINGLE'], st['APP'], LS['PRODC'], LS['PD'], st['KIND'],
            st['NAT'], st['CHC'], st['CHD'], st['UVt'], self.A, self.selfa, LS['OSV'], LS['SPO'], LS['capable'],
            LS['COSTS'], self.ctr, self.steps_rule, self.wn, self.wenc, self.wsp, self.wcode, self.wsid, self.ckey,
            self.cval, self.ncache, self.plog, self.hist_wait, self.hist_acq, self.hist_steps, self.hist_cens,
            self.nprod, LS['ident'], LS['spo_unit'], self.tset, self.uns, self.rulecount, self.enc_exp, self.skip,
            LS['FUT'], self.fcount, self.enc_futile, self.err, self.epsg, self.pairmode, self.fseed, W['cumL'],
            W['spE'], PV.R_SNON, self.rcount, self.arr, self.narr,
            self.gbase, self.gg, self.gdict2, self.ngt, self.GS, self.GN, self.gdict, self.ngv, self.widx, self.AG1,
            self.AG2, self.PW, self.Wt, self.wdel, W['natu'], W['sucker'], self.gmode, self.gcap, self.gctr,
            self.glog, self.nglog, self.gdirty, self.glive, self.isl_sucker_gen, self.gcount, self.freel, self.nfree)
        if self.err[0] != 0:
            raise RuntimeError('kernel error %d at generation %d (base types %d, grudge types %d, lists %d)' % (
                self.err[0], self.g, self.ntv[0], self.ngt[0], self.ngv[0]))

    def merge(self, new_seed):
        """Fission-fusion: all islands into one population (types and per-individual logs carried)."""
        import detectors_kern as KG
        import provenance as PV
        LS, st = self.LS, self.LS['st']
        I, N = self.I, self.N
        T = I * N
        self.slots = self.slots.reshape(1, T).copy()
        self.N, self.I = T, 1
        self.counts = np.zeros((1, KCAP_G), np.int64)
        np.add.at(self.counts[0], self.slots[0], 1)
        ks = np.nonzero(self.counts[0])[0]
        ks = ks[np.lexsort((self.gg[ks], self.gbase[ks]))]      # base-type order (ids are recycled), then list
        self.pres = np.zeros((1, T), np.int64); self.npres = np.array([len(ks)], np.int64)
        self.pos = -np.ones((1, KCAP_G), np.int64)
        for tt, k in enumerate(ks):
            self.pres[0, tt] = k; self.pos[0, k] = tt
        self.paysum = np.zeros((1, KCAP_G))
        KG.ginit_paysum(self.counts, self.paysum, self.pres, self.npres, self.gbase, self.gg, self.GS, self.GN,
                        self.tunit, self.tsp, self.A, self.selfa, self.widx, self.AG1, self.AG2, self.PW, self.gmode)
        self.spcount = self.spcount.sum(0, keepdims=True)
        self.wn = np.zeros((1, T), np.int64); self.wenc = np.zeros((1, T), np.int64)
        self.wsp = np.zeros((1, T, 3), np.int64); self.wcode = np.zeros((1, T, 3), np.int64)
        self.wsid = np.zeros((1, T, 3), np.int64)
        self.ckey = np.zeros((1, T, PV.CACHE_CAP), np.int64); self.cval = np.zeros((1, T, PV.CACHE_CAP), np.int64)
        self.ncache = np.zeros((1, T), np.int64)
        self.plog = self.plog.reshape(1, T, 5).copy()
        self.uns = np.zeros(1, np.int64)
        self.rulecount[:] = 0; self.fcount[:] = 0
        bslots = self.gbase[self.slots]
        PV.init_uns(bslots, self.tunit, self.trule, self.tset, st['BLC'], st['BLD'], LS['PD'], st['utau'], LS['FUT'],
                    self.uns, self.rulecount, self.fcount)
        self.maj_k = np.zeros(1, np.int64); self.maj_n = np.zeros(1, np.int64)
        self.rcount = np.zeros(1, np.int64)
        self.gdirty = np.ones(1, np.int64); self.glive = np.zeros(1, np.int64)
        self.seed = int(new_seed)
        self.fseed = int((self.seed * 6364136223846793005 + 1442695040888963407) % (2 ** 62))
        self.mN = 0.0

    # ------------------------------------------------------------------------------------ statistics
    def island_stats(self):
        import detectors_kern as KG
        return KG.gisland_stats(self.counts, self.pres, self.npres, self.N, self.gbase, self.gg, self.GS, self.GN,
                                self.tunit, self.tsp, self.A, self.selfa, self.widx, self.AG1, self.AG2, self.PW,
                                self.gmode, self.maj_k, self.maj_n)

    def acts(self, k, j):
        import detectors_kern as KG
        return KG.acts(k, j, self.gbase, self.gg, self.GS, self.GN, self.tunit, self.tsp, self.A, self.selfa,
                       self.widx, self.AG1, self.AG2, self.PW, self.gmode)

    def check_consistency(self):
        """Present types: global counts equal the slot counts, each maps to itself in the type dictionary, no present
        type is on the free list."""
        n = int(self.ngt[0])
        cnt = np.bincount(self.slots.ravel(), minlength=n)
        assert (cnt[:n] == self.gcount[:n]).all(), 'gcount'
        assert (self.counts[:, :n].sum(0) == cnt[:n]).all(), 'counts'
        free = set(self.freel[:self.nfree[0]].tolist())
        for k in np.nonzero(cnt)[0].tolist():
            assert k not in free, 'present type freed'
            assert self.gdict2[int(self.gbase[k]) * 1048576 + int(self.gg[k])] == k, 'dict'
        return True

    def glist(self, k):
        gid = self.gg[k]
        return [int(x) for x in self.GS[gid, :self.GN[gid]]]
