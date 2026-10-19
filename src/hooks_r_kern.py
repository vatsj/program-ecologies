"""The island kernel with hooked types (notes/hooks-r.md §1.4-1.6).

World K's annealed island kernel (src/annealed_kern.py with an all-zero schedule, itself provenance's `segment`),
rewritten over *hooked types* k = (spelling, block, fill list):
  - block b: the C and D script sequences (world K's unit blocks, script ids), interned;
  - fill list f: up to 4 fills (tag, scope, key, action, source), interned;
  - per type, cached: the P run trees at the ⌜C⌝, ⌜D⌝ and self roots (from the fills by the conflict rule), the
    behaviour class (certified C against ⌜C⌝, ⌜D⌝, itself), the self-play atom values, and whether one resolution
    holds at every root ("fixed") with its universe unit.
A pair's atom values come from world K's tables when the pair is *uniform on its touched roots* and both effective
units are universe units (Lemma T), and otherwise from the composite cache, whose misses are computed by host replay
of the baked carriers (Lemma H) through `objmode` callbacks into src/hooks_r.py.  With no hooked type present and no
fill operation, every draw, type id, payoff sum and birth is the annealed kernel's (validated).

All state lives in one jitclass instance `st` (static tables and dynamic type tables), so a call costs one reference
count whatever the number of arrays.

Draws: production encounters and births use provenance's event-indexed stream (draws 0-7 and 8 + 5q ...); fill
operations use a separate counter stream fseed (draw index 16 q + j), so they consume nothing of the production
stream and are identical across the hook cells of a replicate.
"""
import os
import sys

import numpy as np
from numba import njit, objmode, types
from numba.experimental import jitclass
from numba.typed import Dict

sys.path.insert(0, os.path.dirname(__file__))
from provenance import ri, ru

PAYM = np.array([[-1.0, 1.0], [-2.0, 0.0]])      # [my action][their action], D = 0, C = 1
LMAX = 6
FMAX = 4
NCT = 48
(CT_ENC, CT_FENC, CT_PRODC, CT_PRODC_OK, CT_PRODD, CT_PRODD_OK, CT_GRUDGE, CT_THANKS, CT_UPD, CT_NOOP, CT_EVICT,
 CT_COPY_TRY, CT_COPY_OK, CT_CONTRACT, CT_WRITE_SELFSKIP, CT_NOSITE, CT_BIRTH, CT_CHANGE, CT_MISS_PAIR,
 CT_MISS_PRODC, CT_MISS_PD, CT_MISS_CLS, CT_MISS_SELF, CT_GC, CT_UNIFORM, CT_COMPOSITE, CT_EXEC_HOOK,
 CT_EXEC_FILLED, CT_TRIG_GRUDGE, CT_TRIG_THANKS, CT_SHUF, CT_STRIP, CT_LFGC, CT_NEWTYPE) = range(34)
CT_EXS = 36          # executed gene sites by the winner's scope (6)
CT_EXR = 42          # ... by the winner's source (4)
KEY12 = types.UniTuple(types.int64, 12)
KEY6 = types.UniTuple(types.int64, 6)
KEY3 = types.UniTuple(types.int64, 3)
KEY2 = types.UniTuple(types.int64, 2)
RANKS = np.array([1, 2, 4, 3, 6, 5], np.int64)

i8_1, i8_2 = types.int8[::1], types.int8[:, ::1]
i64_1, i64_2, i64_3 = types.int64[::1], types.int64[:, ::1], types.int64[:, :, ::1]
b_1, b_2 = types.boolean[::1], types.boolean[:, ::1]
SPEC = [
    # static
    ('RES', i64_2), ('TAUP', i64_1), ('NTAGS', i64_1), ('INERT', b_2), ('recency', types.boolean),
    ('AMASK', i64_1), ('KIND', i64_3), ('NAT', i64_1), ('CHC', i8_2), ('CHD', i8_2), ('UVt', i8_2),
    ('BLC', i64_2), ('BLD', i64_2), ('A', i8_2), ('selfa', i8_1), ('inO', b_1), ('PRODC', i64_2), ('PD', i64_1),
    ('ACTT', i64_2), ('LEAFT', i64_2), ('FUT', i8_2), ('CLEAF', b_1),
    # dictionaries
    ('tdict', types.DictType(KEY3, types.int64)), ('uid', types.DictType(KEY3, types.int64)),
    ('bdict', types.DictType(KEY2, types.int64)), ('fdict', types.DictType(KEY3, types.int64)),
    ('pairc', types.DictType(KEY12, types.int64)), ('prodcc', types.DictType(KEY12, types.int64)),
    ('pdc', types.DictType(KEY6, types.int64)), ('clsc', types.DictType(KEY6, types.int64)),
    ('selfc', types.DictType(KEY6, types.int64)),
    # types
    ('tsp', i64_1), ('tblk', i64_1), ('tfl', i64_1), ('tT', i64_2), ('tcls', i64_1), ('tsv', i64_1),
    ('tgc', i64_1), ('ntv', i64_1), ('TFREE', i64_1), ('TST', i64_1), ('tfix', b_1), ('tu0', i64_1),
    ('tset', b_1), ('tuc', i64_2), ('tcs', i64_1), ('tds', i64_1),
    # blocks and fill lists
    ('BKC', i64_2), ('BKD', i64_2), ('nbk', i64_1), ('FN', i64_1), ('FP', i64_2), ('nfl', i64_1),
    ('LFREE', i64_1), ('LST', i64_1), ('tmp', i64_1), ('ctr', i64_1),
    ('tstamp', i64_1), ('PCK', i64_1), ('PCS', i64_1), ('PCV', i64_1), ('mark', b_1), ('ngc', i64_1),
]


@jitclass(SPEC)
class KState:
    def __init__(self):
        pass


def new_dicts():
    return dict(
        pair=Dict.empty(key_type=KEY12, value_type=types.int64),
        prodc=Dict.empty(key_type=KEY12, value_type=types.int64),
        pd=Dict.empty(key_type=KEY6, value_type=types.int64),
        cls=Dict.empty(key_type=KEY6, value_type=types.int64),
        selfv=Dict.empty(key_type=KEY6, value_type=types.int64),
        uid=Dict.empty(key_type=KEY3, value_type=types.int64),
        tdict=Dict.empty(key_type=KEY3, value_type=types.int64),
        bdict=Dict.empty(key_type=KEY2, value_type=types.int64),
        fdict=Dict.empty(key_type=KEY3, value_type=types.int64))


# ------------------------------------------------------------------------------------------------ host callbacks
HOSTFN = {}


def _cb_pair(key): return HOSTFN['pair'](key)


def _cb_prodc(key): return HOSTFN['prodc'](key)


def _cb_pd(key): return HOSTFN['pd'](key)


def _cb_cls(key): return HOSTFN['cls'](key)


def _cb_self(key): return HOSTFN['self'](key)


@njit(cache=False)
def host_pair(key):
    with objmode(v='int64'):
        v = _cb_pair(key)
    return v


@njit(cache=False)
def host_prodc(key):
    with objmode(v='int64'):
        v = _cb_prodc(key)
    return v


@njit(cache=False)
def host_pd(key):
    with objmode(v='int64'):
        v = _cb_pd(key)
    return v


@njit(cache=False)
def host_cls(key):
    with objmode(v='int64'):
        v = _cb_cls(key)
    return v


@njit(cache=False)
def host_self(key):
    with objmode(v='int64'):
        v = _cb_self(key)
    return v


# ------------------------------------------------------------------------------------------------ blocks
@njit(cache=False)
def pack6(row):
    p = 0
    for i in range(row.shape[0]):
        s = row[i]
        if s < 0: break
        p |= (s + 1) << (8 * i)
    return p


@njit(cache=False)
def block_of(st, csp, dsp):
    key = (csp, dsp)
    if key in st.bdict: return st.bdict[key]
    b = st.nbk[0]
    st.nbk[0] = b + 1
    q = csp; i = 0
    while q:
        st.BKC[b, i] = (q & 255) - 1; q >>= 8; i += 1
    q = dsp; i = 0
    while q:
        st.BKD[b, i] = (q & 255) - 1; q >>= 8; i += 1
    st.bdict[key] = b
    return b


@njit(cache=False)
def blen(BK, b):
    n = 0
    for i in range(BK.shape[1]):
        if BK[b, i] < 0: break
        n += 1
    return n


@njit(cache=False)
def bholds(BK, b, s):
    for i in range(BK.shape[1]):
        if BK[b, i] < 0: return False
        if BK[b, i] == s: return True
    return False


@njit(cache=False)
def block_append(st, b, blk, sid):
    """blk 0: C block, 1: D block."""
    csp = pack6(st.BKC[b]); dsp = pack6(st.BKD[b])
    if blk == 0:
        n = blen(st.BKC, b)
        if n >= LMAX: return b
        csp |= (sid + 1) << (8 * n)
    else:
        n = blen(st.BKD, b)
        if n >= LMAX: return b
        dsp |= (sid + 1) << (8 * n)
    return block_of(st, csp, dsp)


# ------------------------------------------------------------------------------------------------ fill lists
# a fill packed: tag (2) | scope (3) << 2 | act (1) << 5 | src (2) << 6 | (key + 3) << 8
@njit(cache=False)
def fpack(tag, sc, key, act, src):
    return tag | (sc << 2) | (act << 5) | (src << 6) | ((key + 3) << 8)


@njit(cache=False)
def ftag(p): return p & 3


@njit(cache=False)
def fsc(p): return (p >> 2) & 7


@njit(cache=False)
def fact(p): return (p >> 5) & 1


@njit(cache=False)
def fsrc(p): return (p >> 6) & 3


@njit(cache=False)
def fkey(p): return (p >> 8) - 3


@njit(cache=False)
def fl_of(st, n, P):
    """The id of the fill list P[:n] (packed fills, oldest first); interned; -1 when the table is full."""
    a = 0; b = 0
    for i in range(n):
        if i < 2: a |= P[i] << (32 * i)
        else: b |= P[i] << (32 * (i - 2))
    key = (n, a, b)
    if key in st.fdict: return st.fdict[key]
    if st.LST[0] > 0:
        st.LST[0] -= 1
        f = st.LFREE[st.LST[0]]
    else:
        f = st.nfl[0]
        if f >= st.FN.shape[0]: return -1
        st.nfl[0] = f + 1
    st.FN[f] = n
    for i in range(FMAX):
        st.FP[f, i] = P[i] if i < n else 0
    st.fdict[key] = f
    return f


@njit(cache=False)
def fl_add(st, f, tag, sc, key, act, src):
    """The write rule: a held (tag, scope, key) is updated in place (action and source; moved to the end) unless the
    action is unchanged (a no-op, declared deviation); otherwise appended, FIFO beyond 4."""
    n = st.FN[f]
    tmp = st.tmp
    for i in range(n):
        p = st.FP[f, i]
        if ftag(p) == tag and fsc(p) == sc and fkey(p) == key:
            if fact(p) == act:
                st.ctr[CT_NOOP] += 1
                return f
            m = 0
            for j in range(n):
                if j != i:
                    tmp[m] = st.FP[f, j]; m += 1
            tmp[m] = fpack(tag, sc, key, act, src); m += 1
            st.ctr[CT_UPD] += 1
            return fl_of(st, m, tmp)
    m = 0
    start = 1 if n >= FMAX else 0
    if start: st.ctr[CT_EVICT] += 1
    for j in range(start, n):
        tmp[m] = st.FP[f, j]; m += 1
    tmp[m] = fpack(tag, sc, key, act, src); m += 1
    return fl_of(st, m, tmp)


@njit(cache=False)
def fl_strip_writes(st, f):
    n = st.FN[f]; m = 0
    tmp = st.tmp
    for i in range(n):
        p = st.FP[f, i]
        if fsrc(p) != 1:
            tmp[m] = p; m += 1
    if m == n: return f
    return fl_of(st, m, tmp)


# ------------------------------------------------------------------------------------------------ resolution
@njit(cache=False)
def key_holds(sc, key, kind, opp_sp, opp_cls, own_sp):
    if sc <= 1: return True
    if sc == 2: return kind != 2 and key == opp_cls
    if sc == 3: return key == opp_sp
    if sc == 4:
        if key == -2: return opp_sp == own_sp
        return key == opp_sp
    return key == kind


@njit(cache=False)
def resolve_code(st, f, sp, kind, opp_sp, opp_cls):
    """The resolution code h1 + 3 h2 (0 unfilled, 1 C, 2 D) of a type's gene sites at one root
    (kinds: 0 ⌜C⌝, 1 ⌜D⌝, 2 self, 3 partner)."""
    nt = st.NTAGS[sp]
    if nt == 0: return 0
    n = st.FN[f]
    if n == 0: return 0
    code = 0
    for tag in range(1, nt + 1):
        best = -1; br = -1
        for i in range(n):
            p = st.FP[f, i]
            if ftag(p) != tag: continue
            sc = fsc(p)
            if st.INERT[fsrc(p), sc]: continue
            if not key_holds(sc, fkey(p), kind, opp_sp, opp_cls, sp): continue
            rk = 1 if st.recency else RANKS[sc]
            if rk >= br:
                best = i; br = rk
        if best >= 0:
            h = 1 if fact(st.FP[f, best]) == 1 else 2
            code += h * (1 if tag == 1 else 3)
    return code


@njit(cache=False)
def winner_info(st, f, sp, tag, kind, opp_sp, opp_cls):
    """(scope, source) of the conflict winner at a gene site of the given tag, or (-1, -1)."""
    best = -1; br = -1
    for i in range(st.FN[f]):
        p = st.FP[f, i]
        if ftag(p) != tag: continue
        sc = fsc(p)
        if st.INERT[fsrc(p), sc]: continue
        if not key_holds(sc, fkey(p), kind, opp_sp, opp_cls, sp): continue
        rk = 1 if st.recency else RANKS[sc]
        if rk >= br:
            best = i; br = rk
    if best < 0: return -1, -1
    return fsc(st.FP[f, best]), fsrc(st.FP[f, best])


# ------------------------------------------------------------------------------------------------ touched roots
# root kinds: bit 0 ⌜C⌝, bit 1 ⌜D⌝, bit 2 self, bit 3 partner
@njit(cache=False)
def _tstep(T, To, m, r):
    if m & 1: T |= 4
    if m & 2: T |= 1
    if m & 4: T |= 2
    if r == 3:
        if m & 8: To |= 8
        if m & 16: To |= 4
        if m & 32: To |= 1
        if m & 64: To |= 2
    elif r == 2:
        if m & 24: T |= 4
        if m & 32: T |= 1
        if m & 64: T |= 2
    return T, To


@njit(cache=False)
def touched2(kC, kD, kS, kP, jC, jD, jS, jP, AMASK):
    """The roots of k and of j a pair's evaluation touches (the fixpoint of their trees' atom kinds)."""
    Tk = 8; Tj = 8
    while True:
        ok, oj = Tk, Tj
        if Tk & 1: Tk, Tj = _tstep(Tk, Tj, AMASK[kC], 0)
        if Tk & 2: Tk, Tj = _tstep(Tk, Tj, AMASK[kD], 1)
        if Tk & 4: Tk, Tj = _tstep(Tk, Tj, AMASK[kS], 2)
        if Tk & 8: Tk, Tj = _tstep(Tk, Tj, AMASK[kP], 3)
        if Tj & 1: Tj, Tk = _tstep(Tj, Tk, AMASK[jC], 0)
        if Tj & 2: Tj, Tk = _tstep(Tj, Tk, AMASK[jD], 1)
        if Tj & 4: Tj, Tk = _tstep(Tj, Tk, AMASK[jS], 2)
        if Tj & 8: Tj, Tk = _tstep(Tj, Tk, AMASK[jP], 3)
        if Tk == ok and Tj == oj: break
    return Tk, Tj


@njit(cache=False)
def touched1(c, d, s, start, AMASK):
    """The roots of one program that a check at one of its own roots (start bit) touches."""
    T = start
    while True:
        o = T
        dummy = 0
        if T & 1: T, dummy = _tstep(T, 0, AMASK[c], 0)
        if T & 2: T, dummy = _tstep(T, 0, AMASK[d], 1)
        if T & 4: T, dummy = _tstep(T, 0, AMASK[s], 2)
        if T == o: break
    return T


@njit(cache=False)
def uni4(c, d, s, p, T):
    if (T & 1) and c != p: return False
    if (T & 2) and d != p: return False
    if (T & 4) and s != p: return False
    return True


# ------------------------------------------------------------------------------------------------ table values
@njit(cache=False)
def uvr(st, u, col):
    if (col % 2) == 0:
        if st.BLC[u, 0] < 0: return 0
    else:
        if st.BLD[u, 0] < 0: return 0
    v = st.UVt[u, col]
    return v if v >= 0 else 0


@njit(cache=False)
def tab_vals(st, t, uk, uj):
    """Valcode of tree t (k's) against j with universe units uk, uj (distinct quotes); -1 if a needed entry is
    missing."""
    vc = 0
    for i in range(st.NAT[t]):
        k_ = st.KIND[t, i, 0]; ai = st.KIND[t, i, 1]; qi = st.KIND[t, i, 2]
        v = 0
        if k_ == 0:
            has = st.BLC[uj, 0] >= 0 if ai == 0 else st.BLD[uj, 0] >= 0
            if has:
                c = st.CHC[uj, uk] if ai == 0 else st.CHD[uj, uk]
                if c < 0: return -1
                v = 1 if c == 1 else 0
        elif k_ == 1:
            has = st.BLC[uk, 0] >= 0 if ai == 0 else st.BLD[uk, 0] >= 0
            if has:
                c = st.CHC[uk, uj] if ai == 0 else st.CHD[uk, uj]
                if c < 0: return -1
                v = 1 if c == 1 else 0
        elif k_ == 2:
            v = 1 if uvr(st, uj, ai) == 1 else 0
        elif k_ == 3:
            v = 1 if uvr(st, uk, ai) == 1 else 0
        elif k_ == 4:
            v = 1 if uvr(st, uj, (2 if qi == 0 else 4) + ai) == 1 else 0
        else:
            v = 1 if uvr(st, uk, (2 if qi == 0 else 4) + ai) == 1 else 0
        vc |= v << i
    return vc


@njit(cache=False)
def tab_selfvals(st, t, u):
    vc = 0
    for i in range(st.NAT[t]):
        k_ = st.KIND[t, i, 0]; ai = st.KIND[t, i, 1]; qi = st.KIND[t, i, 2]
        if k_ <= 3:
            v = 1 if uvr(st, u, ai) == 1 else 0
        else:
            v = 1 if uvr(st, u, (2 if qi == 0 else 4) + ai) == 1 else 0
        vc |= v << i
    return vc


@njit(cache=False)
def v3(x):
    if x == 1: return 1
    if x == 2: return 4
    return 0


@njit(cache=False)
def sig_code(st, u, v, rel, t):
    """lt_genes_kern.sig_code with the producer's effective tree t given."""
    code = 25 if rel == 2 else 0
    for i in range(st.NAT[t]):
        k = st.KIND[t, i, 0]; ai = st.KIND[t, i, 1]; qi = st.KIND[t, i, 2]
        c = 0
        if rel == 2 and k <= 3:
            if ai == 0: c = 2
            else: c = v3(uvr(st, u, 1))
        elif rel == 2 and k == 4:
            c = v3(uvr(st, u, (2 if qi == 0 else 4) + ai))
        elif k == 0:
            if ai == 0: c = 3
            else: c = v3(st.CHD[v, u]) if st.BLD[v, 0] >= 0 else 0
        elif k == 1:
            if ai == 0: c = 2
            else: c = v3(st.CHD[u, v]) if st.BLD[u, 0] >= 0 else 0
        elif k == 2:
            c = v3(uvr(st, v, ai))
        elif k == 3:
            c = v3(uvr(st, u, ai))
        elif k == 4:
            c = v3(uvr(st, v, (2 if qi == 0 else 4) + ai))
        else:
            c = v3(uvr(st, u, (2 if qi == 0 else 4) + ai))
        code += c * (5 if i == 0 else 1)
    return code


# ------------------------------------------------------------------------------------------------ units
@njit(cache=False)
def unit_tb(st, t, csp, dsp):
    """The universe unit (t, blocks) if it exists and is reachable (in O), else -1."""
    key = (t, csp, dsp)
    if key in st.uid:
        u = st.uid[key]
        return u if st.inO[u] else -1
    return -1


@njit(cache=False)
def unit_code(st, k, code, tP):
    """Type k's universe unit on the tree tP of its resolution code (cached per type)."""
    u = st.tuc[k, code]
    if u != -2: return u
    u = unit_tb(st, tP, st.tcs[k], st.tds[k])
    st.tuc[k, code] = u
    return u


# ------------------------------------------------------------------------------------------------ type creation
@njit(cache=False)
def type_class(st, k):
    """Behaviour class: 4 [C vs ⌜C⌝] + 2 [C vs ⌜D⌝] + [C vs itself] (certified cooperation)."""
    tC = st.tT[k, 0]; tD = st.tT[k, 1]; tS = st.tT[k, 2]
    if tC == tD and tD == tS:
        u = unit_tb(st, tS, st.tcs[k], st.tds[k])
        if u >= 0:
            c = 0
            if uvr(st, u, 2) == 1: c += 4
            if uvr(st, u, 4) == 1: c += 2
            if uvr(st, u, 0) == 1: c += 1
            return c
    key = (tS, tC, tD, tS, st.tcs[k], st.tds[k])
    if key in st.clsc: return st.clsc[key]
    st.ctr[CT_MISS_CLS] += 1
    c = host_cls(key)
    st.clsc[key] = c
    return c


@njit(cache=False)
def make_type(st, sp, b, f):
    """The type (sp, b, f): existing, recycled or new (intrinsic data computed).  -1 if full."""
    key = (sp, b, f)
    if key in st.tdict: return st.tdict[key]
    if st.TST[0] > 0:
        st.TST[0] -= 1
        k = st.TFREE[st.TST[0]]
    else:
        k = st.ntv[0]
        if k >= st.tsp.shape[0]: return -1
        st.ntv[0] = k + 1
    st.ctr[CT_NEWTYPE] += 1
    st.tstamp[k] += 1
    st.tsp[k] = sp; st.tblk[k] = b; st.tfl[k] = f; st.tgc[k] = 0
    st.tcs[k] = pack6(st.BKC[b]); st.tds[k] = pack6(st.BKD[b])
    for c in range(9): st.tuc[k, c] = -2
    for r in range(3):
        st.tT[k, r] = st.TAUP[st.RES[sp, resolve_code(st, f, sp, r, -1 if r < 2 else sp, 0)]]
    # fixed: every active fill has scope none or role (or there is none): one resolution at every root
    fix = True
    if st.NTAGS[sp] > 0:
        for i in range(st.FN[f]):
            p = st.FP[f, i]
            if not st.INERT[fsrc(p), fsc(p)] and fsc(p) > 1:
                fix = False
                break
    st.tfix[k] = fix
    st.tT[k, 3] = st.tT[k, 2] if fix else -1
    st.tu0[k] = unit_tb(st, st.tT[k, 2], st.tcs[k], st.tds[k]) if fix else -1
    st.tcls[k] = type_class(st, k)
    st.tsv[k] = -1
    # settled (production can change nothing): a C entry or C-futile, and a D entry or D-futile.  C-futile: no C leaf
    # in any resolution (structural), or a fixed universe unit whose tree has no C script at any signature of the P
    # closure (provenance's FUT, S-nonself codes); D-futile: a fixed universe unit with PD[u] = u or a cap timeout.
    hasC = st.BKC[b, 0] >= 0; hasD = st.BKD[b, 0] >= 0
    cdone = hasC
    if not cdone:
        cdone = True
        for c in range(9):
            if st.CLEAF[st.TAUP[st.RES[sp, c]]]:
                cdone = False
                break
    ddone = hasD
    if not ddone:
        # the D step is a function of the type alone (the ⌜D⌝ root): futile if it writes nothing
        ddone = prod_d(st, k) < 0
    st.tset[k] = cdone and ddone
    st.tdict[key] = k
    return k


# ------------------------------------------------------------------------------------------------ pair values
@njit(cache=False)
def self_vals(st, k):
    """(valcode, tree) of type k against its own quote (the self root)."""
    tS = st.tT[k, 2]
    if st.tsv[k] >= 0: return st.tsv[k], tS
    if st.tu0[k] >= 0:
        st.tsv[k] = tab_selfvals(st, tS, st.tu0[k])
        return st.tsv[k], tS
    c = st.tT[k, 0]; d = st.tT[k, 1]
    T = touched1(c, d, tS, 4, st.AMASK)
    vc = -1
    if uni4(c, d, tS, tS, T):
        u = unit_tb(st, tS, st.tcs[k], st.tds[k])
        if u >= 0:
            vc = tab_selfvals(st, tS, u)
    if vc < 0:
        key = (tS, c if (T & 1) else -1, d if (T & 2) else -1, tS, st.tcs[k], st.tds[k])
        if key in st.selfc:
            vc = st.selfc[key]
        else:
            st.ctr[CT_MISS_SELF] += 1
            vc = host_self(key)
            st.selfc[key] = vc
    st.tsv[k] = vc
    return vc, tS


@njit(cache=False)
def pair_vals(st, k, j):
    """(vk, vj, tk, tj): atom valcodes and effective partner-root trees of k against j and j against k (k != j:
    distinct quotes)."""
    uk0 = st.tu0[k]; uj0 = st.tu0[j]
    if uk0 >= 0 and uj0 >= 0:
        tk0 = st.tT[k, 2]; tj0 = st.tT[j, 2]
        vk = tab_vals(st, tk0, uk0, uj0)
        vj = tab_vals(st, tj0, uj0, uk0)
        if vk >= 0 and vj >= 0:
            st.ctr[CT_UNIFORM] += 1
            return vk, vj, tk0, tj0
    spk = st.tsp[k]; spj = st.tsp[j]
    ck = resolve_code(st, st.tfl[k], spk, 3, spj, st.tcls[j])
    cj = resolve_code(st, st.tfl[j], spj, 3, spk, st.tcls[k])
    tPk = st.TAUP[st.RES[spk, ck]]
    tPj = st.TAUP[st.RES[spj, cj]]
    kC = st.tT[k, 0]; kD = st.tT[k, 1]; kS = st.tT[k, 2]; jC = st.tT[j, 0]; jD = st.tT[j, 1]; jS = st.tT[j, 2]
    Tk, Tj = touched2(kC, kD, kS, tPk, jC, jD, jS, tPj, st.AMASK)
    if uni4(kC, kD, kS, tPk, Tk) and uni4(jC, jD, jS, tPj, Tj):
        uk = unit_code(st, k, ck, tPk); uj = unit_code(st, j, cj, tPj)
        if uk >= 0 and uj >= 0:
            vk = tab_vals(st, tPk, uk, uj)
            vj = tab_vals(st, tPj, uj, uk)
            if vk >= 0 and vj >= 0:
                st.ctr[CT_UNIFORM] += 1
                return vk, vj, tPk, tPj
    st.ctr[CT_COMPOSITE] += 1
    key = (tPk, kC if (Tk & 1) else -1, kD if (Tk & 2) else -1, kS if (Tk & 4) else -1, st.tcs[k], st.tds[k],
           tPj, jC if (Tj & 1) else -1, jD if (Tj & 2) else -1, jS if (Tj & 4) else -1, st.tcs[j], st.tds[j])
    if key in st.pairc:
        v = st.pairc[key]
    else:
        st.ctr[CT_MISS_PAIR] += 1
        v = host_pair(key)
        st.pairc[key] = v
    return v & 15, v >> 4, tPk, tPj


@njit(cache=False)
def acts(st, k, j):
    """(a_kj, a_jk) with 1 = C."""
    uk = st.tu0[k]; uj = st.tu0[j]
    if uk >= 0 and uj >= 0:
        if k == j:
            a = st.selfa[uk]
            return a, a
        return st.A[uk, uj], st.A[uj, uk]
    if k == j:
        vc, t = self_vals(st, k)
        a = st.ACTT[t, vc]
        return a, a
    # the pair cache: direct-mapped, keyed by both types and their creation stamps (types are recycled)
    lo = k if k < j else j
    hi = j if k < j else k
    key = lo * 1048576 + hi
    stp = st.tstamp[lo] * 4294967296 + st.tstamp[hi]
    h = ((lo * 2654435761) ^ (hi * 40503) ^ (st.tstamp[lo] * 97) ^ (st.tstamp[hi] * 31)) & (st.PCK.shape[0] - 1)
    if st.PCK[h] == key and st.PCS[h] == stp:
        v = st.PCV[h]
        x = v & 1; y = (v >> 1) & 1
        if k == lo: return x, y
        return y, x
    vk, vj, tk, tj = pair_vals(st, k, j)
    ak = st.ACTT[tk, vk]; aj = st.ACTT[tj, vj]
    st.PCK[h] = key; st.PCS[h] = stp
    st.PCV[h] = (ak | (aj << 1)) if k == lo else (aj | (ak << 1))
    return ak, aj


@njit(cache=False)
def pay(st, k, j):
    a, b = acts(st, k, j)
    return PAYM[a, b]


# ------------------------------------------------------------------------------------------------ production
@njit(cache=False)
def prod_c(st, k, j):
    """The S-nonself C step of k at the root (k, j, C): the script id, -1 none, -3 cap timeout."""
    uk0 = st.tu0[k]; uj0 = st.tu0[j]
    if uk0 >= 0 and uj0 >= 0:
        rel0 = 1 if uk0 == uj0 else 0
        t0_ = st.tT[k, 2]
        s0 = st.PRODC[t0_, sig_code(st, uk0, uj0, rel0, t0_)]
        if s0 != -2: return s0
    spk = st.tsp[k]; spj = st.tsp[j]
    ck = resolve_code(st, st.tfl[k], spk, 3, spj, st.tcls[j])
    cj = resolve_code(st, st.tfl[j], spj, 3, spk, st.tcls[k])
    tPk = st.TAUP[st.RES[spk, ck]]
    tPj = st.TAUP[st.RES[spj, cj]]
    kC = st.tT[k, 0]; kD = st.tT[k, 1]; kS = st.tT[k, 2]; jC = st.tT[j, 0]; jD = st.tT[j, 1]; jS = st.tT[j, 2]
    Tk, Tj = touched2(kC, kD, kS, tPk, jC, jD, jS, tPj, st.AMASK)
    if uni4(kC, kD, kS, tPk, Tk) and uni4(jC, jD, jS, tPj, Tj):
        uk = unit_code(st, k, ck, tPk); uj = unit_code(st, j, cj, tPj)
        if uk >= 0 and uj >= 0:
            rel = 1 if uk == uj else 0
            s = st.PRODC[tPk, sig_code(st, uk, uj, rel, tPk)]
            if s != -2: return s
    key = (tPk, kC if (Tk & 1) else -1, kD if (Tk & 2) else -1, kS if (Tk & 4) else -1, st.tcs[k], st.tds[k],
           tPj, jC if (Tj & 1) else -1, jD if (Tj & 2) else -1, jS if (Tj & 4) else -1, st.tcs[j], st.tds[j])
    if key in st.prodcc: return st.prodcc[key]
    st.ctr[CT_MISS_PRODC] += 1
    s = host_prodc(key)
    st.prodcc[key] = s
    return s


@njit(cache=False)
def pd_from_unit(st, u):
    u2 = st.PD[u]
    if u2 == -3: return -3
    if u2 == -2: return -2
    if u2 == u: return -1
    n = 0
    for i in range(st.BLD.shape[1]):
        if st.BLD[u2, i] < 0: break
        n += 1
    return st.BLD[u2, n - 1]


@njit(cache=False)
def prod_d(st, k):
    """The D step of k (against ⌜D⌝): the new D script id, -1 none, -3 cap timeout."""
    if st.tu0[k] >= 0:
        s = pd_from_unit(st, st.tu0[k])
        if s != -2: return s
    c = st.tT[k, 0]; d = st.tT[k, 1]; s_ = st.tT[k, 2]
    T = touched1(c, d, s_, 2, st.AMASK)
    if uni4(c, d, s_, d, T):
        u = unit_tb(st, d, st.tcs[k], st.tds[k])
        if u >= 0:
            s = pd_from_unit(st, u)
            if s != -2: return s
    key = (d, c if (T & 1) else -1, d, s_ if (T & 4) else -1, st.tcs[k], st.tds[k])
    if key in st.pdc: return st.pdc[key]
    st.ctr[CT_MISS_PD] += 1
    s = host_pd(key)
    st.pdc[key] = s
    return s


@njit(cache=False)
def side_prod(st, k, j):
    """World K's S-nonself step of k after an encounter with j: the C step (while no C entry and the spellings
    differ), then the D step (while no D entry).  Returns the new type (or k; -1 when full)."""
    b = st.tblk[k]
    b0 = b
    if st.BKC[b, 0] < 0 and st.tsp[k] != st.tsp[j]:
        st.ctr[CT_PRODC] += 1
        s = prod_c(st, k, j)
        if s >= 0 and not bholds(st.BKC, b, s):
            b = block_append(st, b, 0, s)
            st.ctr[CT_PRODC_OK] += 1
    if st.BKD[b, 0] < 0:
        kk = k
        if b != b0:
            kk = make_type(st, st.tsp[k], b, st.tfl[k])
            if kk < 0: return -1
        st.ctr[CT_PRODD] += 1
        s = prod_d(st, kk)
        if s >= 0 and not bholds(st.BKD, b, s):
            b = block_append(st, b, 1, s)
            st.ctr[CT_PRODD_OK] += 1
    if b == b0: return k
    return make_type(st, st.tsp[k], b, st.tfl[k])


# ------------------------------------------------------------------------------------------------ island bookkeeping
@njit(cache=False)
def change(st, i, a, b, counts, paysum, pres, npres, pos):
    counts[i, a] -= 1
    st.tgc[a] -= 1
    if counts[i, a] == 0:
        p = pos[i, a]; last = pres[i, npres[i] - 1]
        pres[i, p] = last; pos[i, last] = p; pos[i, a] = -1; npres[i] -= 1
    new = counts[i, b] == 0
    if new:
        pres[i, npres[i]] = b; pos[i, b] = npres[i]; npres[i] += 1
    counts[i, b] += 1
    st.tgc[b] += 1
    vv = 0.0
    for tt in range(npres[i]):
        j = pres[i, tt]
        if new and j == b: continue
        x, y = acts(st, j, b)
        paysum[i, j] += PAYM[x, y] - pay(st, j, a)
        if new: vv += counts[i, j] * PAYM[y, x]
    if new:
        vv += counts[i, b] * pay(st, b, b)
        paysum[i, b] = vv


@njit(cache=False)
def init_paysum(st, counts, paysum, pres, npres):
    I = counts.shape[0]
    for i in range(I):
        for tt in range(npres[i]):
            j = pres[i, tt]
            vv = 0.0
            for t2 in range(npres[i]):
                kk = pres[i, t2]
                vv += counts[i, kk] * pay(st, j, kk)
            paysum[i, j] = vv


# ------------------------------------------------------------------------------------------------ fill operations
@njit(cache=False)
def write_fill(st, k, tag, sc, key, act, src):
    """The type k becomes after a fill (tag, scope, key, action, source) is written; -1 if a table is full."""
    f2 = fl_add(st, st.tfl[k], tag, sc, key, act, src)
    if f2 < 0: return -1
    if f2 == st.tfl[k]: return k
    return make_type(st, st.tsp[k], st.tblk[k], f2)


@njit(cache=False)
def fill_ops(st, i, kf, kp, nf, np_, af, ap, lf, lp, slots, fseed, ev, q, P):
    """The fill operation of each side of a fill encounter (pre-encounter plays af, ap; reached-leaf tags lf, lp, 0 =
    no gene site), applied to the post-production types nf, np_.  P = (p_copy, p_contract, grudge_only, shuffle,
    clone_ok, hooks_on, not_inherited).  Returns the two new types (-1 when a table is full)."""
    p_copy, p_ctr, grudge_only, shuffle, clone_ok = P[0], P[1], P[2], P[3], P[4]
    N = slots.shape[1]
    spf = st.tsp[kf]; spp = st.tsp[kp]
    same = spf == spp
    done_f = False; done_p = False
    b0 = 16 * q
    # pair contract (both or neither)
    if lf > 0 and lp > 0 and not (af == 1 and ap == 1) and (clone_ok > 0.5 or not same):
        if ru(fseed, ev, b0) < p_ctr:
            a2 = write_fill(st, nf, lf, 4, spp, 1, 3)
            if a2 < 0: return -1, -1
            b2 = write_fill(st, np_, lp, 4, spf, 1, 3)
            if b2 < 0: return -1, -1
            nf, np_ = a2, b2
            st.ctr[CT_CONTRACT] += 1
            done_f = True; done_p = True
    # history writes
    for side in range(2):
        if (side == 0 and done_f) or (side == 1 and done_p): continue
        lv = lf if side == 0 else lp
        mine = af if side == 0 else ap
        theirs = ap if side == 0 else af
        if mine != 1: continue
        if theirs == 0:
            st.ctr[CT_TRIG_GRUDGE] += 1
        else:
            st.ctr[CT_TRIG_THANKS] += 1
            if grudge_only > 0.5: continue
        if lv == 0:
            st.ctr[CT_NOSITE] += 1
            continue
        if same and clone_ok < 0.5:
            st.ctr[CT_WRITE_SELFSKIP] += 1
            continue
        key = spp if side == 0 else spf
        if shuffle > 0.5:
            r = ri(fseed, ev, b0 + 1 + side, N)
            key = st.tsp[slots[i, r]]
            st.ctr[CT_SHUF] += 1
        cur = nf if side == 0 else np_
        nk = write_fill(st, cur, lv, 3, key, 1 if theirs == 1 else 0, 1)
        if nk < 0: return -1, -1
        if theirs == 0: st.ctr[CT_GRUDGE] += 1
        else: st.ctr[CT_THANKS] += 1
        if side == 0:
            nf = nk; done_f = True
        else:
            np_ = nk; done_p = True
    # copying
    for side in range(2):
        if (side == 0 and done_f) or (side == 1 and done_p): continue
        cur = nf if side == 0 else np_
        don = kp if side == 0 else kf
        ntc = st.NTAGS[st.tsp[cur]]
        if ntc == 0: continue
        fd = st.tfl[don]
        nd = st.FN[fd]
        if nd == 0: continue
        if ru(fseed, ev, b0 + 3 + side) >= p_copy: continue
        st.ctr[CT_COPY_TRY] += 1
        pk = st.FP[fd, ri(fseed, ev, b0 + 5 + side, nd)]
        tg = pk & 3
        if tg > ntc: continue
        nk = write_fill(st, cur, tg, (pk >> 2) & 7, (pk >> 8) - 3, (pk >> 5) & 1, 2)
        if nk < 0: return -1, -1
        if nk != cur: st.ctr[CT_COPY_OK] += 1
        if side == 0: nf = nk
        else: np_ = nk
    return nf, np_


# ------------------------------------------------------------------------------------------------ the segment
@njit(cache=False)
def segment(st, g0, gens, seed, fseed, N, w, m, r, rf, slots, counts, paysum, pres, npres, pos, spcount, lin, track,
            P, err, uns, scope_ex, src_ex):
    """Generations g0 .. g0 + gens - 1 (I*N Moran events each; r encounters per event, the first rf of them also
    fill encounters).  Births and production as the annealed kernel; fill operations as notes §1.5."""
    I = slots.shape[0]
    fs = np.empty(N)
    hooks_on = P[5] > 0.5
    tcap = st.tsp.shape[0]; fcap = st.FN.shape[0]
    for g in range(g0, g0 + gens):
        for e in range(I * N):
            ev = g * I * N + e
            # garbage collection between Moran events (no transient type is referenced here)
            if st.ntv[0] - st.TST[0] > 0.85 * tcap or st.nfl[0] - st.LST[0] > 0.85 * fcap:
                gc_types(st)
                gc_lists(st, st.mark)
                st.ngc[0] += 1
            for q in range(r):
                b0 = 8 + 5 * q
                fenc = hooks_on and q < rf
                i = ri(seed, ev, b0, I)
                if (not fenc) and uns[i] == 0:
                    continue
                f = ri(seed, ev, b0 + 1, N)
                p = ri(seed, ev, b0 + 2, N - 1)
                if p >= f: p += 1
                kf = slots[i, f]; kp = slots[i, p]
                sf = st.tset[kf]; sp_ = st.tset[kp]
                if (not fenc) and sf and sp_:
                    continue
                st.ctr[CT_ENC] += 1
                af = 0; ap = 0; lf = 0; lp = 0
                if fenc:
                    st.ctr[CT_FENC] += 1
                    if kf == kp:
                        vc, t = self_vals(st, kf)
                        af = st.ACTT[t, vc]; ap = af
                        lf = st.LEAFT[st.tsp[kf], vc]; lp = lf
                    else:
                        vf, vp, tf, tp = pair_vals(st, kf, kp)
                        af = st.ACTT[tf, vf]; ap = st.ACTT[tp, vp]
                        lf = st.LEAFT[st.tsp[kf], vf]; lp = st.LEAFT[st.tsp[kp], vp]
                    kind = 2 if kf == kp else 3
                    if lf > 0:
                        st.ctr[CT_EXEC_HOOK] += 1
                        sc, so = winner_info(st, st.tfl[kf], st.tsp[kf], lf, kind, st.tsp[kp], st.tcls[kp])
                        if sc >= 0:
                            st.ctr[CT_EXEC_FILLED] += 1; scope_ex[sc] += 1; src_ex[so] += 1
                    if lp > 0:
                        st.ctr[CT_EXEC_HOOK] += 1
                        sc, so = winner_info(st, st.tfl[kp], st.tsp[kp], lp, kind, st.tsp[kf], st.tcls[kf])
                        if sc >= 0:
                            st.ctr[CT_EXEC_FILLED] += 1; scope_ex[sc] += 1; src_ex[so] += 1
                nf = kf; np_ = kp
                if not sf:
                    nf = side_prod(st, kf, kp)
                    if nf < 0:
                        err[0] = 2
                        return g
                if not sp_:
                    np_ = side_prod(st, kp, kf)
                    if np_ < 0:
                        err[0] = 2
                        return g
                if fenc:
                    nf, np_ = fill_ops(st, i, kf, kp, nf, np_, af, ap, lf, lp, slots, fseed, ev, q, P)
                    if nf < 0 or np_ < 0:
                        err[0] = 3
                        return g
                if nf != kf:
                    slots[i, f] = nf; st.ctr[CT_CHANGE] += 1
                    uns[i] += (0 if st.tset[nf] else 1) - (0 if sf else 1)
                    change(st, i, kf, nf, counts, paysum, pres, npres, pos)
                if np_ != kp:
                    slots[i, p] = np_; st.ctr[CT_CHANGE] += 1
                    uns[i] += (0 if st.tset[np_] else 1) - (0 if sp_ else 1)
                    change(st, i, kp, np_, counts, paysum, pres, npres, pos)
            # birth-death, event-indexed draws 0-4 (7: the lineage)
            i = ri(seed, ev, 0, I)
            src = i
            if m > 0.0 and I > 1 and ru(seed, ev, 1) < m:
                src = ri(seed, ev, 2, I - 1)
                if src >= i: src += 1
            nps = npres[src]
            mx = -1e300
            for tt in range(nps):
                kk = pres[src, tt]
                fv = (paysum[src, kk] - pay(st, kk, kk)) / (N - 1)
                fs[tt] = fv
                if fv > mx: mx = fv
            tot = 0.0
            for tt in range(nps):
                tot += counts[src, pres[src, tt]] * np.exp(w * (fs[tt] - mx))
            uu = ru(seed, ev, 3) * tot
            acc = 0.0
            child = pres[src, nps - 1]
            for tt in range(nps):
                kk = pres[src, tt]
                acc += counts[src, kk] * np.exp(w * (fs[tt] - mx))
                if uu <= acc:
                    child = kk
                    break
            vs = ri(seed, ev, 4, N)
            kv = slots[i, vs]
            if track:
                mc = counts[src, child]
                pick = ri(seed, ev, 7, mc)
                c = 0
                for jj in range(N):
                    if slots[src, jj] == child:
                        if c == pick:
                            lin[i, vs] = lin[src, jj]
                            break
                        c += 1
            st.ctr[CT_BIRTH] += 1
            if P[6] > 0.5:
                # learned but not inherited: the newborn drops the parent's written fills
                f2 = fl_strip_writes(st, st.tfl[child])
                if f2 < 0:
                    err[0] = 3
                    return g
                if f2 != st.tfl[child]:
                    c2 = make_type(st, st.tsp[child], st.tblk[child], f2)
                    if c2 < 0:
                        err[0] = 2
                        return g
                    child = c2
                    st.ctr[CT_STRIP] += 1
            spcount[i, st.tsp[kv]] -= 1
            spcount[i, st.tsp[child]] += 1
            if kv == child: continue
            uns[i] += (0 if st.tset[child] else 1) - (0 if st.tset[kv] else 1)
            slots[i, vs] = child
            change(st, i, kv, child, counts, paysum, pres, npres, pos)
    return g0 + gens


# ------------------------------------------------------------------------------------------------ statistics
@njit(cache=False)
def island_stats(st, counts, pres, npres, N, maj_k, maj_n):
    """Per island: P(C,C) over ordered pairs of distinct individuals; the majority type and its count."""
    I = counts.shape[0]
    out = np.zeros(I)
    for i in range(I):
        num = 0.0
        bn = -1; bk = -1
        for t1 in range(npres[i]):
            a = pres[i, t1]
            ca = counts[i, a]
            if ca > bn:
                bn = ca; bk = a
            for t2 in range(npres[i]):
                b = pres[i, t2]
                cb = counts[i, b]
                n = ca * (cb - 1) if a == b else ca * cb
                if n == 0: continue
                x, y = acts(st, a, b)
                if x == 1 and y == 1: num += n
        out[i] = num / (N * (N - 1))
        maj_k[i] = bk; maj_n[i] = bn
    return out


@njit(cache=False)
def gc_types(st):
    """Free every type with zero global count; returns the number freed."""
    nf = 0
    for k in range(st.ntv[0]):
        if st.tgc[k] == 0 and st.tsp[k] >= 0:
            key = (st.tsp[k], st.tblk[k], st.tfl[k])
            if key in st.tdict and st.tdict[key] == k:
                st.tdict.pop(key)
                st.TFREE[st.TST[0]] = k
                st.TST[0] += 1
                st.tsp[k] = -1
                nf += 1
    return nf


@njit(cache=False)
def gc_lists(st, mark):
    """Free every fill list referenced by no live type (list 0, the empty list, is never freed)."""
    for f in range(st.nfl[0]): mark[f] = False
    mark[0] = True
    for k in range(st.ntv[0]):
        if st.tsp[k] >= 0: mark[st.tfl[k]] = True
    for q in range(st.LST[0]): mark[st.LFREE[q]] = True
    nfr = 0
    for f in range(st.nfl[0]):
        if not mark[f]:
            n = st.FN[f]
            a = 0; b = 0
            for i in range(n):
                if i < 2: a |= st.FP[f, i] << (32 * i)
                else: b |= st.FP[f, i] << (32 * (i - 2))
            key = (n, a, b)
            if key in st.fdict and st.fdict[key] == f:
                st.fdict.pop(key)
            st.LFREE[st.LST[0]] = f
            st.LST[0] += 1
            nfr += 1
    return nfr


@njit(cache=False)
def mutual_types(st, K, ref):
    """M[a, b]: types K[a], K[b] cooperate with each other (a == b: self-play); R[a, r]: K[a] mutual with ref[r]."""
    n = K.shape[0]
    M = np.zeros((n, n), np.bool_)
    for a in range(n):
        for b in range(a, n):
            x, y = acts(st, K[a], K[b])
            v = x == 1 and y == 1
            M[a, b] = v; M[b, a] = v
    R = np.zeros((n, ref.shape[0]), np.bool_)
    for a in range(n):
        for r in range(ref.shape[0]):
            x, y = acts(st, K[a], ref[r])
            R[a, r] = x == 1 and y == 1
    return M, R


@njit(cache=False)
def _wins(st, f, sp, tag, kind, osp, ocl, q):
    best = -1; br = -1
    for i in range(st.FN[f]):
        p = st.FP[f, i]
        if ftag(p) != tag: continue
        sc = fsc(p)
        if st.INERT[fsrc(p), sc]: continue
        if not key_holds(sc, fkey(p), kind, osp, ocl, sp): continue
        rk = 1 if st.recency else RANKS[sc]
        if rk >= br:
            best = i; br = rk
    return best == q


@njit(cache=False)
def fill_stats(st, counts, pres, npres):
    """Held fills by scope and source (individual-weighted); applicable and selected by scope: a fill's key holds /
    it wins the conflict at the root of some co-resident, or at its holder's ⌜C⌝, ⌜D⌝ or self root."""
    held = np.zeros((6, 4)); appl = np.zeros(6); sel = np.zeros(6)
    inert_held = 0.0
    I = counts.shape[0]
    for i in range(I):
        n = npres[i]
        for t1 in range(n):
            k = pres[i, t1]
            f = st.tfl[k]; nf = st.FN[f]
            if nf == 0: continue
            cnt = counts[i, k]
            sp = st.tsp[k]
            for q in range(nf):
                p = st.FP[f, q]
                sc = fsc(p); src = fsrc(p)
                held[sc, src] += cnt
                if st.INERT[src, sc]:
                    inert_held += cnt
                    continue
                key = fkey(p); tag = ftag(p)
                ap = False; wn = False
                for r in range(3):
                    osp = -1 if r < 2 else sp
                    if key_holds(sc, key, r, osp, 0, sp):
                        ap = True
                        if _wins(st, f, sp, tag, r, osp, 0, q): wn = True
                for t2 in range(n):
                    if wn: break
                    j = pres[i, t2]
                    if j == k: continue
                    if key_holds(sc, key, 3, st.tsp[j], st.tcls[j], sp):
                        ap = True
                        if _wins(st, f, sp, tag, 3, st.tsp[j], st.tcls[j], q): wn = True
                if ap: appl[sc] += cnt
                if wn: sel[sc] += cnt
    return held, appl, sel, inert_held
