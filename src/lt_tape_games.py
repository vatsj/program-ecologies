"""Grammar, arms, static tables, island statistics and lotteries for the private-tape experiment
(specs/2026-10-24-realizable-randomizer.md; notes/lt-tape.md; predictions/2026-10-24-realizable-randomizer.md).

Games: RPS (one population; r = 3 tape digits) and the inspection game (fixed roles; r = 2).  Templates are L_T^tape
programs; every capability can be disabled in place (the template keeps its prior mass and plays the stated default).
Imports the DSL lottery kernels (rps.lottery_kernel, mixed2.lottery2) so the selection dynamics are the ones of the DSL runs.
"""
import math
import os
import sys
import zlib
from dataclasses import dataclass, field
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lt_tape as T
from lt_tape import (con, nat, L2, TP, EQ, IF, PL, HQ, PAIR, THEM, ME, size, carrier, make_certs, produce_cert)

W_SEL = 0.3                                  # selection intensity of the DSL runs (rps.W, mixed2.W)
PROVE_B = 8                                  # budget of every prove
ENUM_CAP = 400                               # work cap b_e of every prp
SIM_FUELS = (20, 100)

FAMILIES = ('const', 'mixer', 'carrier', 'hash', 'sim', 'prover', 'rim', 'enum', 'check', 'pcr')
READER_FAMILIES = ('hash', 'sim', 'prover', 'rim', 'enum', 'check', 'pcr')
PROVER_CAP_FAMILIES = ('prover', 'rim', 'enum', 'check', 'pcr', 'carrier')       # "provers and carriers" of the no-prover arm
ROUTE_OF = {'prover': 'search', 'rim': 'search', 'enum': 'enum', 'check': 'check', 'pcr': 'check'}


@dataclass
class Template:
    name: str
    role: int
    family: str
    uses_tape: bool
    build: object                 # build(variant) -> term; variant in {'tape', 'hash'}
    meta: dict = field(default_factory=dict)


# ----------------------------------------------------------------------------------------------------------------
# Building blocks
# ----------------------------------------------------------------------------------------------------------------
def digit_tape(r):
    return lambda i: TP(i)


def digit_hash(r):
    """Hash digit i: hq r (i, <opponent>)  (a function of the opponent's source: predictable by simulation)."""
    return lambda i: HQ(r, PAIR(nat(i), THEM))


def mix_tree(m, j, A, B, digit):
    """Shortest decision tree over m binary digits: A iff v = 4 d0 + 2 d1 + d2 < j (A with probability j / 2**m)."""
    def node(lo, hi, d):
        if hi <= j: return A
        if lo >= j: return B
        mid = (lo + hi) // 2
        return IF(EQ(digit(d), nat(0)), node(lo, mid, d + 1), node(mid, hi, d + 1))
    return node(0, 2 ** m, 0)


def let(arg, body):
    """(\\v. body) arg ; body written with v0 = the bound value and ME, THEM shifted by one."""
    return ('app', ('lam', body), arg)


def hash_case_inspection(h, a_hit, a_miss):
    return let(HQ(2, THEM), IF(EQ(('v', 0), nat(h)), con(a_hit), con(a_miss)))


def act_cases(order, discr):
    """if discr = 0 then order[0] else if discr = 1 then order[1] else order[2]."""
    return IF(EQ(discr, nat(0)), con(order[0]), IF(EQ(discr, nat(1)), con(order[1]), con(order[2])))


BEAT = {'R': 'P', 'P': 'S', 'S': 'R'}


def beat_case(v, default):
    """The action that beats the value v (R, P or S); `default` (a term) on anything else (TO)."""
    return IF(EQ(v, con('R')), con('P'), IF(EQ(v, con('P')), con('S'), IF(EQ(v, con('S')), con('R'), default)))


# ----------------------------------------------------------------------------------------------------------------
# Games
# ----------------------------------------------------------------------------------------------------------------
class RPS:
    name = 'rps'; r = 3; m = 3; roles = 1
    acts = (('R', 'P', 'S'),)
    UNI = np.array([1 / 3, 1 / 3, 1 / 3, 0.0])

    @staticmethod
    def u(a, b):
        if a == b: return 0.0
        return 1.0 if BEAT[b] == a else -1.0


class INSP:
    name = 'insp'; r = 2; m = 3; roles = 2
    acts = (('I', 'N'), ('C', 'K'))
    P0 = np.array([[-1.0, -1.0], [0.0, -4.0]])        # inspector: rows I, N; columns C, K
    P1 = np.array([[0.0, -3.0], [0.0, 1.0]])          # inspectee


# ----------------------------------------------------------------------------------------------------------------
# Catalogues
# ----------------------------------------------------------------------------------------------------------------
def _mixer_factory(game_m, j, A, B, r=2):
    def build(variant):
        dg = digit_tape(r) if variant == 'tape' else digit_hash(r)
        return L2(mix_tree(game_m, j, con(A), con(B), dg))
    return build


def _carrier_factory(game_m, j, A, B, K, r=2, act=None):
    """Carrier of the mixer M_j: tape variant carries its true certificate for `act`; the hash variant carries the same
    (now false) certificate, so the pseudo-random-only arm contains junk carriers the checker must reject."""
    act = act or A

    def build(variant):
        body = mix_tree(game_m, j, con(A), con(B), digit_tape(r))
        plain = L2(body)
        eng = _cert_engine(r, game_m, K)
        pre = produce_cert(eng, plain, act)
        certs = make_certs(K, [(act, pre)])
        if variant == 'tape':
            return carrier(body, certs)
        hbody = mix_tree(game_m, j, con(A), con(B), digit_hash(r))
        return carrier(hbody, certs)
    return build


_CERT_ENG = {}


def _cert_engine(r, m, K):
    key = (r, m, K)
    if key not in _CERT_ENG:
        _CERT_ENG[key] = T.Engine(T.TProver(r, limit=1000), K=K, r=r, m=m)
    return _CERT_ENG[key]


def catalogue_insp(K, m=3):
    """22 inspector templates (role 0) and 24 inspectee templates (role 1)."""
    r = 2
    sc = 2 ** (m - 3)                     # probabilities stay on the 1/8 grid of m = 3; m = 4 adds the odd multiples of 1/16
    ins, ee = [], []
    ins.append(Template('I0', 0, 'const', False, lambda v: L2(con('I'))))
    ins.append(Template('N0', 0, 'const', False, lambda v: L2(con('N'))))
    nj = 2 ** m
    for j in range(1, nj):
        ins.append(Template('M%d' % j, 0, 'mixer', True, _mixer_factory(m, j, 'I', 'N'), dict(p=Fraction(j, nj))))
    for j in (1, 2, 3, 4, 6):
        ins.append(Template('CARR%d' % j, 0, 'carrier', True, _carrier_factory(m, j * sc, 'I', 'N', K), dict(p=Fraction(j, 8))))
    for h in (0, 1):
        ins.append(Template('HI%d' % h, 0, 'hash', False, (lambda h: lambda v: L2(hash_case_inspection(h, 'I', 'N')))(h)))
    for k in SIM_FUELS:
        ins.append(Template('SI%dn' % k, 0, 'sim', False,
                            (lambda k: lambda v: L2(IF(EQ(('run', nat(k), THEM, ME), con('K')), con('I'), con('N'))))(k)))
        ins.append(Template('SI%di' % k, 0, 'sim', False,
                            (lambda k: lambda v: L2(IF(EQ(('run', nat(k), THEM, ME), con('C')), con('N'), con('I'))))(k)))
    ins.append(Template('RI', 0, 'prover', False,
                        lambda v: L2(IF(('prove', nat(PROVE_B), PL(THEM, ME, 'C')), con('N'), con('I')))))
    ins.append(Template('RIM', 0, 'rim', True,
                        lambda v: L2(IF(('prove', nat(PROVE_B), PL(THEM, ME, 'C')), con('N'),
                                        IF(EQ((TP(0) if v == 'tape' else HQ(2, PAIR(nat(0), THEM))), nat(0)), con('I'), con('N'))))))
    ee.append(Template('C0', 1, 'const', False, lambda v: L2(con('C'))))
    ee.append(Template('K0', 1, 'const', False, lambda v: L2(con('K'))))
    for j in range(1, nj):
        ee.append(Template('Mc%d' % j, 1, 'mixer', True, _mixer_factory(m, j, 'K', 'C'), dict(q=Fraction(j, nj))))
    for h in (0, 1):
        ee.append(Template('HE%d' % h, 1, 'hash', False, (lambda h: lambda v: L2(hash_case_inspection(h, 'K', 'C')))(h)))
    for k in SIM_FUELS:
        ee.append(Template('SE%dk' % k, 1, 'sim', False,
                           (lambda k: lambda v: L2(IF(EQ(('run', nat(k), THEM, ME), con('I')), con('C'), con('K'))))(k)))
        ee.append(Template('SE%dc' % k, 1, 'sim', False,
                           (lambda k: lambda v: L2(IF(EQ(('run', nat(k), THEM, ME), con('N')), con('K'), con('C'))))(k)))
    ee.append(Template('PE', 1, 'prover', False,
                       lambda v: L2(IF(('prove', nat(PROVE_B), PL(THEM, ME, 'N')), con('K'), con('C')))))
    ee.append(Template('PEC', 1, 'prover', False,
                       lambda v: L2(IF(('prove', nat(PROVE_B), PL(THEM, ME, 'I')), con('C'), con('K')))))
    den = r ** m
    for k in (2, 3, 4):
        ee.append(Template('PR%d' % k, 1, 'enum', False,
                           (lambda k: lambda v: L2(IF(('prp', nat(ENUM_CAP), THEM, ME, con('I'), nat(k * sc)), con('C'), con('K'))))(k),
                           dict(k=k)))
    for k in (2, 3, 4):
        ee.append(Template('CR%d' % k, 1, 'check', False,
                           (lambda k: lambda v: L2(IF(('chk', THEM, ME, con('I'), nat(k * sc)), con('C'), con('K'))))(k), dict(k=k)))
    ee.append(Template('PCR3', 1, 'pcr', False,
                       lambda v: L2(IF(('chk', THEM, ME, con('I'), nat(3 * sc)), con('C'),
                                       IF(('prp', nat(ENUM_CAP), THEM, ME, con('I'), nat(3 * sc)), con('C'), con('K')))), dict(k=3)))
    return ins, ee


def catalogue_rps(K, m=3):
    r = 3
    T_ = []
    for a in 'RPS':
        T_.append(Template(a + '0', 0, 'const', False, (lambda a: lambda v: L2(con(a)))(a)))

    def ubody(variant):
        d = digit_tape(r) if variant == 'tape' else digit_hash(r)
        return IF(EQ(d(0), nat(0)), con('R'), IF(EQ(d(0), nat(1)), con('P'), con('S')))

    T_.append(Template('U', 0, 'mixer', True, lambda v: L2(ubody(v))))
    pairs = [(a, b) for a in 'RPS' for b in 'RPS' if a != b]

    def bbody(a1, a2, variant):
        d = digit_tape(r) if variant == 'tape' else digit_hash(r)
        return IF(EQ(d(0), nat(2)), con(a2), con(a1))

    for (a1, a2) in pairs:
        T_.append(Template('B_%s%s' % (a1, a2), 0, 'mixer', True,
                           (lambda a1, a2: lambda v: L2(bbody(a1, a2, v)))(a1, a2), dict(major=a1, minor=a2)))
    for (a1, a2) in pairs:
        def mk(a1=a1, a2=a2):
            def build(variant):
                plain = L2(bbody(a1, a2, 'tape'))
                eng = _cert_engine(r, m, K)
                pre = produce_cert(eng, plain, a1)
                certs = make_certs(K, [(a1, pre)])
                return carrier(bbody(a1, a2, variant), certs)
            return build
        T_.append(Template('CB_%s%s' % (a1, a2), 0, 'carrier', True, mk(), dict(major=a1, minor=a2)))
    for j in range(3):
        order = 'RPS'[j:] + 'RPS'[:j]
        T_.append(Template('H%d' % j, 0, 'hash', False,
                           (lambda order: lambda v: L2(let(HQ(3, THEM), act_cases(order, ('v', 0)))))(order)))
    for k in SIM_FUELS:
        for d in 'RPS':
            T_.append(Template('SIM%d%s' % (k, d), 0, 'sim', False,
                               (lambda k, d: lambda v: L2(let(('run', nat(k), THEM, ME), beat_case(('v', 0), con(d)))))(k, d)))
        T_.append(Template('SIM%du' % k, 0, 'sim', True,
                           (lambda k: lambda v: L2(let(('run', nat(k), THEM, ME), beat_case(('v', 0), ubody(v)))))(k)))

    def fallback(variant):
        return ubody(variant)

    def pbody(variant):
        return IF(('prove', nat(PROVE_B), PL(THEM, ME, 'R')), con('P'),
                  IF(('prove', nat(PROVE_B), PL(THEM, ME, 'P')), con('S'),
                     IF(('prove', nat(PROVE_B), PL(THEM, ME, 'S')), con('R'), fallback(variant))))
    T_.append(Template('PB', 0, 'prover', True, lambda v: L2(pbody(v))))

    def rbody(op, variant):
        def test(a):
            if op == 'prp': return ('prp', nat(ENUM_CAP), THEM, ME, con(a), nat(12))
            return ('chk', THEM, ME, con(a), nat(12))
        return IF(test('R'), con('P'), IF(test('P'), con('S'), IF(test('S'), con('R'), fallback(variant))))
    T_.append(Template('PRR', 0, 'enum', True, lambda v: L2(rbody('prp', v))))
    T_.append(Template('CRR', 0, 'check', True, lambda v: L2(rbody('chk', v))))
    return [T_]


# ----------------------------------------------------------------------------------------------------------------
# Arms: which templates are disabled / replaced, and the defaults
# ----------------------------------------------------------------------------------------------------------------
RPS_ARMS = ('full', 'noprover', 'notape', 'prand')
INSP_ARMS = ('full', 'noprover', 'notape', 'prand', 'insp_only', 'ee_only')


def arm_disabled(game, arm, t):
    """Is template t disabled in this arm?"""
    if arm in ('full', 'prand'): return False
    if arm == 'noprover': return t.family in PROVER_CAP_FAMILIES
    if arm == 'notape': return t.uses_tape or t.family == 'carrier'
    if game == 'insp':
        if arm == 'insp_only':          # only the inspector reads: inspectee readers disabled
            return t.role == 1 and t.family in READER_FAMILIES
        if arm == 'ee_only':            # only the inspectee reads: inspector readers disabled
            return t.role == 0 and t.family in READER_FAMILIES
    raise ValueError(arm)


def arm_terms(game, tpls, arm, renorm=False):
    """Effective program terms per role for the arm.  tpls: list per role of Template lists.  Returns (terms, keep) with
    terms[role][i] the effective term of template i (a default constant if disabled), keep[role][i] False if renormalized away."""
    out = []; keep = []
    for role, lst in enumerate(tpls):
        terms = []; kp = []
        dis_idx = 0
        for t in lst:
            if arm_disabled(game, arm, t):
                if game == 'rps':
                    a = 'RPS'[dis_idx % 3]; dis_idx += 1
                else:
                    a = 'N' if role == 0 else 'C'
                terms.append(L2(con(a))); kp.append(not renorm)
            else:
                v = 'hash' if arm == 'prand' else 'tape'
                terms.append(t.build(v)); kp.append(True)
        out.append(terms); keep.append(kp)
    return out, keep


# ----------------------------------------------------------------------------------------------------------------
# Prior: the repo's length prior over template spellings (rps.length_prior_sizes): P(size = s) ~ 1 / (2 s^2) over the
# sizes present, uniform among the templates of that size.
# ----------------------------------------------------------------------------------------------------------------
def template_sizes(tpls_role):
    return np.array([size(t.build('tape')) for t in tpls_role])


def prior_masses(sizes, mask=None):
    sizes = np.asarray(sizes)
    if mask is None: mask = np.ones(len(sizes), bool)
    ss = sorted(set(int(s) for s in sizes[mask]))
    z = sum(1.0 / (2 * s * s) for s in ss)
    p = np.zeros(len(sizes))
    for s in ss:
        sel = np.nonzero((sizes == s) & mask)[0]
        p[sel] = (1.0 / (2 * s * s)) / z / len(sel)
    return p


def draw_founders(sizes, mask, I, N, seed):
    """(I, n) founder counts.  Common random numbers: each slot draws a size (length prior over the sizes present) and a
    uniform quantile among the templates of that size, in catalogue order; arms with the same sizes are paired slot by slot
    (with `mask` = the full arm's all-True mask, a renormalized arm draws from its own sizes)."""
    sizes = np.asarray(sizes)
    n = len(sizes)
    rng = np.random.default_rng(seed)
    u1 = rng.random(I * N); u2 = rng.random(I * N)
    ss = sorted(set(int(s) for s in sizes[mask]))
    z = sum(1.0 / (2 * s * s) for s in ss)
    cdf = np.cumsum([(1.0 / (2 * s * s)) / z for s in ss])
    pick = np.minimum(np.searchsorted(cdf, u1, side='right'), len(ss) - 1)
    prog = np.empty(I * N, np.int64)
    for si, s in enumerate(ss):
        sel = np.nonzero(pick == si)[0]
        if len(sel) == 0: continue
        lst = np.nonzero((sizes == s) & mask)[0]
        prog[sel] = lst[np.minimum((u2[sel] * len(lst)).astype(np.int64), len(lst) - 1)]
    cl = prog.reshape(I, N)
    init = np.zeros((I, n), np.int64)
    for i in range(I):
        init[i] = np.bincount(cl[i], minlength=n)
    return init


def run_seed(base, r):
    return zlib.crc32(('lt_tape|%s|%d' % (base, r)).encode()) & 0x7fffffff


# ----------------------------------------------------------------------------------------------------------------
# Static tables
# ----------------------------------------------------------------------------------------------------------------
def rps_tables(terms, engine):
    """G (n, n, 4) action distributions of x against y over (R, P, S, BOT), STEPS (n, n), ROUTE (n, n, 5), FUEL (n, n),
    exact values as floats (the engine's Fractions are exact)."""
    n = len(terms)
    G = np.zeros((n, n, 4)); S = np.zeros((n, n)); RT = np.zeros((n, n, 5)); FU = np.zeros((n, n))
    idx = {'R': 0, 'P': 1, 'S': 2}
    memo = {}
    for i, x in enumerate(terms):
        for j, y in enumerate(terms):
            d = engine.dist(x, y)
            for a, w in d['dist'].items():
                G[i, j, idx.get(a, 3)] += float(w)
            S[i, j] = float(d['steps']); FU[i, j] = float(d['fuel'])
            RT[i, j] = [float(d['route'][k]) for k in T.ROUTES]
    return G, S, RT, FU


def rps_payoffs(G, S, c):
    """Game payoff U_g[x, y] to x and net U = U_g - c S[x, y]."""
    n = G.shape[0]
    u = np.zeros((4, 4))
    for a, na in enumerate('RPS'):
        for b, nb in enumerate('RPS'):
            u[a, b] = RPS.u(na, nb)
    for a in range(3): u[a, 3] = 1.0; u[3, a] = -1.0
    u[3, 3] = 0.0
    Ug = np.einsum('xya,yxb,ab->xy', G, G, u)
    return Ug, Ug - c * S


def insp_tables(terms0, terms1, engine):
    """G0 (n0, n1, 3): inspector's (I, N, BOT) against each inspectee; G1 (n1, n0, 3): inspectee's (C, K, BOT);
    steps S0 (n0, n1), S1 (n1, n0); routes; fuel exhaustion."""
    n0, n1 = len(terms0), len(terms1)
    G0 = np.zeros((n0, n1, 3)); G1 = np.zeros((n1, n0, 3))
    S0 = np.zeros((n0, n1)); S1 = np.zeros((n1, n0))
    RT0 = np.zeros((n0, n1, 5)); RT1 = np.zeros((n1, n0, 5))
    FU0 = np.zeros((n0, n1)); FU1 = np.zeros((n1, n0))
    i0 = {'I': 0, 'N': 1}; i1 = {'C': 0, 'K': 1}
    for a, x in enumerate(terms0):
        for b, y in enumerate(terms1):
            d = engine.dist(x, y)
            for act, w in d['dist'].items(): G0[a, b, i0.get(act, 2)] += float(w)
            S0[a, b] = float(d['steps']); FU0[a, b] = float(d['fuel'])
            RT0[a, b] = [float(d['route'][k]) for k in T.ROUTES]
            d = engine.dist(y, x)
            for act, w in d['dist'].items(): G1[b, a, i1.get(act, 2)] += float(w)
            S1[b, a] = float(d['steps']); FU1[b, a] = float(d['fuel'])
            RT1[b, a] = [float(d['route'][k]) for k in T.ROUTES]
    return G0, G1, S0, S1, RT0, RT1, FU0, FU1


def insp_payoff_tensors():
    """Per-profile payoffs with forfeits: V0[x, y], V1[x, y] for x in (I, N, BOT), y in (C, K, BOT) (mixed2 convention: a
    forfeiter plays its worst action against the realized opposing action; both forfeit: each its worst table entry)."""
    P0, P1 = INSP.P0, INSP.P1
    V0 = np.zeros((3, 3)); V1 = np.zeros((3, 3))
    for x in range(2):
        for y in range(2):
            V0[x, y] = P0[x, y]; V1[x, y] = P1[x, y]
    for y in range(2):                                    # inspector forfeits against realized y
        col = P0[:, y]; mn = col.min(); tied = np.nonzero(col <= mn + 1e-9)[0]
        V0[2, y] = mn; V1[2, y] = np.mean([P1[x, y] for x in tied])
    for x in range(2):                                    # inspectee forfeits against realized x
        row = P1[x, :]; mn = row.min(); tied = np.nonzero(row <= mn + 1e-9)[0]
        V1[x, 2] = mn; V0[x, 2] = np.mean([P0[x, y] for y in tied])
    V0[2, 2] = P0.min(); V1[2, 2] = P1.min()
    return V0, V1


def insp_payoffs(G0, G1, S0, S1, c):
    """UA[a, b], UB[b, a] (game) and net."""
    V0, V1 = insp_payoff_tensors()
    UAg = np.einsum('abx,bay,xy->ab', G0, G1, V0)
    UBg = np.einsum('abx,bay,xy->ba', G0, G1, V1)
    return UAg, UBg, UAg - c * S0, UBg - c * S1
