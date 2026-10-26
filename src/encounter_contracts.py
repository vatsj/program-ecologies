"""Contracts that form in encounters, with the responders' programs answering (spec specs/2026-10-25-encounter-contracts.md;
notes notes/encounter-contracts.md; predictions predictions/2026-10-25-encounter-contracts.md).

Three-player majority division (dollar3), weak (simulation) arm.  An individual is a program together with an ordered list
of contract entries (key p = the override-free action profile of the encounter, fill = the carrier's own action,
bundle code).  The island is a population of types (slot, program, entry list); births are the stored kernel's Moran
birth-death with fitness exp(w * expected stage-2 payoff).  Genesis proposes, at rate nu per island per generation, a
contract for a coalition S on a random encounter triple, tests it against the responders' answers, and installs it on the
signers' individuals (one individual per signing slot) when every signer strictly gains.

Evaluation of an encounter.  Stage 1: the three programs play (least fixed point of the weak evaluator,
`dollar3._weak_into`).  Stage 2: slots with an entry whose key equals the stage-1 profile are carriers and play their fills;
the others re-run their programs against the fixed carrier actions (`eval_fixed`; the substitution applies at every
simulation depth because the fixed slots hold values from the start of the iteration).

Parameters of the arms (vector P): acceptance mode (R / NR / BR), execution mode (programs / best replies), hook mode
(none / H / H-top), copy fraction q (arm C), broadcast count (arm B), filter on/off (arm S off), entry cap.  Arm 0 and H-inert are
nu = 0.

Importable without side effects; drivers are in encounter_contracts_run.py.
"""
import os, sys, math
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from numba import njit
import dollar3 as D
import stable_sets as SS
import many_islands as MI

ROOT = SS.ROOT
W = SS.W
N0 = 100
NOUT = MI.NOUT
TM = 160                       # type slots per player slot
CW = 16                        # entry capacity (array width); the cap itself is a parameter <= CW
PAY = np.ascontiguousarray(MI.PAY)                   # (729, 3) dollars
PAY6 = np.ascontiguousarray(np.rint(MI.PAY * 6).astype(np.int64))
VEC = np.ascontiguousarray(MI.VEC)
CATMAP = MI.CATMAP             # outcome id -> category 0 F, 1 U, 2 G, 3 W(asteful), 4 D
V = MI.V
MI_V = np.array(V, np.int64)

# --- parameters (float64 vector P)
P_N, P_W, P_NU, P_ACC, P_EXE, P_HOOK, P_COPY, P_BCAST, P_FILT, P_CAP = range(10)
ACC_R, ACC_NR, ACC_BR = 0, 1, 2
EXE_PROG, EXE_BR = 0, 1
HOOK_NONE, HOOK_H, HOOK_TOP = 0, 1, 2

# --- STAT layout (int64 vector)
ST_ATT_S = 0          # attempts by |S|-1 (3)
ST_ACC_S = 3          # accepted by |S|-1 (3)
ST_BLK_S = 6          # blocked by missing hook by |S|-1 (3)
ST_ATT_C = 9          # attempts by current-class category (7: F U G W D mixed none)
ST_ACC_C = 16
ST_BR_NOEQ = 30
ST_BR_FAIL = 31
ST_COPY_ATT = 32
ST_COPY_ACC = 33
ST_UNI_ATT = 34
ST_UNI_ACC = 35
ST_UNMATCHED = 36
ST_EVICT = 37
ST_TABFULL = 38
ST_BC_INST = 39
ST_BC_WANT = 40
ST_MIG = 41
ST_MIGFAIL = 42
ST_NOCHANGE = 43
ST_ATT_SC = 44        # attempts by settled-class category (7)
ST_ACC_SC = 51
ST_INST_S = 58        # installs by |S|-1 (3)
ST_NTRACKFULL = 61
ST_LEN = 64
STF_GEN_C = 0         # float accumulators: island-generations by current category (7)
STF_GEN_SC = 7        # by settled category (7)
STF_LEN = 16

# --- state meta
MI_NEXTSER, MI_CLS, MI_SETTLED, MI_NEUTRAL, MI_FVALID, MI_NTRACK, MI_DIRTY = range(7)
MF_CLSSINCE, MF_SETSINCE, MF_LASTMIG, MF_LASTACC, MF_LASTTOUCH = range(5)
NTRK = 12
TRK_W = 24
EV_W = 21
CEV_W = 8


# ====================================================================== arms and tables
class CArm:
    """Program catalogue + seed laws for one grammar: plain L (n <= 6) or the hooked grammar."""

    def __init__(self, hooked=False, n=6, bits1=22, bits2=17):
        self.hooked = hooked
        if not hooked:
            S, mu = SS.arm_data('weak')
            self.S = S
            self.K = len(S.fs)
            self.mu = mu / mu.sum()
            self.hk = -np.ones((3, self.K, 4), np.int64)
        else:
            L = HookLang(n)
            fs, mu, cnt, size = L.canon()
            self.S = HookSlots(fs)
            self.K = len(fs)
            self.mu = mu / mu.sum()
            self.hk = self.S.hk
            self.size = size
        S = self.S
        self.nat = np.ascontiguousarray(S.nat); self.atL = np.ascontiguousarray(S.atL)
        self.atJ = np.ascontiguousarray(S.atJ); self.atA = np.ascontiguousarray(S.atA)
        self.tab = np.ascontiguousarray(S.tab); self.hk = np.ascontiguousarray(self.hk)
        self.laws = np.array([self.mu for _ in range(3)])
        self.cum = np.cumsum(self.laws, axis=1); self.cum /= self.cum[:, -1:]
        self.c1 = (np.zeros(1 << bits1, np.uint64), np.zeros(1 << bits1, np.int16), np.zeros(2, np.int64), np.int64(bits1))
        self.c2 = (np.zeros(1 << bits2, np.uint64), np.zeros(1 << bits2, np.int16), np.zeros(2, np.int64), np.int64(bits2))

    def A(self):
        return (self.nat, self.atL, self.atJ, self.atA, self.tab, self.hk, np.ascontiguousarray(D.PARTNER), PAY, PAY6, VEC,
                np.int64(self.K))

    def clear_c2(self):
        k, v, m, b = self.c2
        k[:] = 0; m[:] = 0

    def maybe_flush_c1(self, frac=0.6):
        k, v, m, b = self.c1
        if m[0] > frac * (1 << int(b)):
            k[:] = 0; m[:] = 0

    def name_of(self, s, x):
        return self.S.src(s, x)


class HookLang(D.Lang):
    """The weak grammar with the leaf HOOK(t, a0): tag t in {0, 1}, default a0 one of nine actions.  A leaf is stored as the
    code v = a0 (constant) or 9 + 9 t + a0 (hook); the canonical reduction compares codes, so a hooked and an unhooked
    function with the same behaviour are different programs."""

    def __init__(self, n, levels=(0,)):
        super().__init__(n, levels)

    def _enumerate(self, n):
        for a in self.atoms:
            if n >= 3:
                self.cntB[3][((a,), (0, 1))] += 1
        for s in range(4, n + 1):
            for f, m in self.cntB[s - 1].items():
                g = self._reduce(f[0], tuple(1 - v for v in f[1])); self.cntB[s][g] += m
            for i in range(3, s - 3):
                j = s - 1 - i
                for fa, ma in self.cntB[i].items():
                    for fb, mb in self.cntB[j].items():
                        U = sorted(set(fa[0]) | set(fb[0]))
                        ta, tb = self._expand(fa, U), self._expand(fb, U)
                        self.cntB[s][self._reduce(U, [x & y for x, y in zip(ta, tb)])] += ma * mb
                        self.cntB[s][self._reduce(U, [x | y for x, y in zip(ta, tb)])] += ma * mb
        for l in range(27):
            self.cntA[1][((), (l,))] += 1
        for s in range(2, n + 1):
            for ib in range(3, s - 2):
                for ia in range(1, s - ib - 1):
                    ic = s - 1 - ib - ia
                    if ic < 1: continue
                    for fb, mb in self.cntB[ib].items():
                        for fa, ma in self.cntA[ia].items():
                            for fc, mc in self.cntA[ic].items():
                                U = sorted(set(fb[0]) | set(fa[0]) | set(fc[0]))
                                tb, ta, tc = self._expand(fb, U), self._expand(fa, U), self._expand(fc, U)
                                self.cntA[s][self._reduce(U, [x if c else y for c, x, y in zip(tb, ta, tc)])] += mb * ma * mc


class HookSlots(D.Slots):
    """Slots for the hooked grammar: tab holds actions (v % 9), hk holds the hook tag of the leaf (or -1)."""

    def __init__(self, fs):
        self.fs = fs
        K = len(fs); self.K = K
        kmax = max(len(f[0]) for f in fs)
        assert kmax <= 2
        self.nat = np.zeros((3, K), np.int64)
        self.atL = np.zeros((3, K, 2), np.int64); self.atJ = np.zeros((3, K, 2), np.int64); self.atA = np.zeros((3, K, 2), np.int64)
        self.tab = np.zeros((3, K, 4), np.int64)
        self.hk = -np.ones((3, K, 4), np.int64)
        self.index = [dict() for _ in range(3)]
        for s in range(3):
            for x, f in enumerate(fs):
                atoms, tab = f
                self.nat[s, x] = len(atoms)
                for t, (L, jr, al) in enumerate(atoms):
                    self.atL[s, x, t] = L; self.atJ[s, x, t] = D.others(s)[jr]; self.atA[s, x, t] = al
                for v, l in enumerate(tab):
                    self.tab[s, x, v] = l % 9
                    self.hk[s, x, v] = (l - 9) // 9 if l >= 9 else -1
                self.index[s][f] = x

    def src(self, s, x):
        atoms, tab = self.fs[x]

        def leaf(l):
            a = D.act_name(s, l % 9)
            return a if l < 9 else 'HOOK%d%s' % ((l - 9) // 9, a)
        if not atoms:
            return leaf(tab[0])
        if len(atoms) == 1:
            L, jr, al = atoms[0]; j = D.others(s)[jr]
            return 'if(BOX(%d=%s),%s,%s)' % (j + 1, D.act_name(j, al), leaf(tab[1]), leaf(tab[0]))
        return 'f%s:%s' % ([(L, D.others(s)[jr] + 1, D.act_name(D.others(s)[jr], al)) for L, jr, al in atoms], [leaf(l) for l in tab])


# ====================================================================== evaluation primitives
@njit(cache=True)
def _others(s):
    if s == 0:
        return 1, 2
    if s == 1:
        return 0, 2
    return 0, 1


@njit(cache=True)
def stage1(A, C1, x0, x1, x2):
    """stage-1 joint code of the program triple (a0*81 + a1*9 + a2) through the 64-bit hash cache."""
    nat, atL, atJ, atA, tab, hk, PARTNER, PAYf, PAYi, VECt, K = A
    keys, vals, meta, bits = C1
    key = np.uint64(((x0 * K + x1) * K + x2) + 1)
    h = (key * np.uint64(0x9E3779B97F4A7C15)) >> np.uint64(64 - bits)
    mask = (np.int64(1) << bits) - 1
    p = np.int64(h)
    while True:
        kk = keys[p]
        if kk == key:
            return np.int64(vals[p])
        if kk == 0:
            hist = np.empty((2, 3), np.int64); val = np.empty(3, np.int64)
            D._weak_into(nat, atL, atJ, atA, tab, x0, x1, x2, hist, val)
            code = val[0] * 81 + val[1] * 9 + val[2]
            if meta[0] * 10 < ((np.int64(1) << bits) * 7):
                keys[p] = key; vals[p] = code; meta[0] += 1
            return code
        p = (p + 1) & mask


@njit(cache=True)
def eval_fixed(A, x0, x1, x2, fixmask, fixval):
    """Stage 2: slots in fixmask hold their fixed actions from the start; the others iterate their programs to the least
    fixed point (budget iteration from bottom, null action for a slot that stays bottom).  Returns the joint code."""
    nat, atL, atJ, atA, tab, hk, PARTNER, PAYf, PAYi, VECt, K = A
    val = -np.ones(3, np.int64)
    new = np.empty(3, np.int64)
    xs = (x0, x1, x2)
    for s in range(3):
        if fixmask[s]:
            val[s] = fixval[s]
    for it in range(16):
        same = True
        for s in range(3):
            if fixmask[s]:
                new[s] = fixval[s]
                continue
            x = xs[s]; k = nat[s, x]
            if k == 0:
                new[s] = tab[s, x, 0]
            else:
                idx = 0; bot = False
                for t in range(k):
                    v = val[atJ[s, x, t]]
                    if v < 0:
                        bot = True; break
                    if v == atA[s, x, t]:
                        idx |= 1 << t
                new[s] = -1 if bot else tab[s, x, idx]
        for s in range(3):
            if new[s] != val[s]:
                same = False
            val[s] = new[s]
        if same and it > 0:
            break
    for s in range(3):
        if val[s] < 0:
            val[s] = 8
    return val[0] * 81 + val[1] * 9 + val[2]


@njit(cache=True)
def leaf_hook(A, s, x, code):
    """hook tag (0/1) of the leaf the program x of slot s reaches when the encounter's stage-1 profile is `code`; -1 if the
    leaf is not a hook."""
    nat, atL, atJ, atA, tab, hk, PARTNER, PAYf, PAYi, VECt, K = A
    a0 = code // 81; a1 = (code // 9) % 9; a2 = code % 9
    idx = 0
    for t in range(nat[s, x]):
        j = atJ[s, x, t]
        v = a0 if j == 0 else (a1 if j == 1 else a2)
        if v == atA[s, x, t]:
            idx |= 1 << t
    return hk[s, x, idx]


@njit(cache=True)
def act_of(code, s):
    if s == 0:
        return code // 81
    if s == 1:
        return (code // 9) % 9
    return code % 9


@njit(cache=True)
def lookup_fill(ST, s, t, p):
    """fill of the type's entry with key p, or -1."""
    tn = ST[2]; tkey = ST[3]; tfil = ST[4]
    for e in range(tn[s, t]):
        if tkey[s, t, e] == p:
            return tfil[s, t, e]
    return -1


@njit(cache=True)
def best_reply_code(A, fixmask, fixval, wcar):
    """Execution-consistent best reply for the free slots (one or two): the pure best reply (one free slot) or the pure
    Nash equilibrium (two) that is worst for the carriers (min total payoff of the slots in wcar), ties by lowest action
    index.  Returns the joint code, or -1 if there is no pure equilibrium."""
    PAYi = A[8]
    nf = 0
    f0 = -1; f1 = -1
    for s in range(3):
        if not fixmask[s]:
            if nf == 0: f0 = s
            else: f1 = s
            nf += 1
    v = np.zeros(3, np.int64)
    for s in range(3):
        if fixmask[s]:
            v[s] = fixval[s]
    if nf == 1:
        bestp = -1000
        for a in range(9):
            v[f0] = a
            code = v[0] * 81 + v[1] * 9 + v[2]
            if PAYi[code, f0] > bestp:
                bestp = PAYi[code, f0]
        bestc = -1; bestcar = 1 << 30
        for a in range(9):
            v[f0] = a
            code = v[0] * 81 + v[1] * 9 + v[2]
            if PAYi[code, f0] == bestp:
                car = 0
                for s in range(3):
                    if wcar[s]:
                        car += PAYi[code, s]
                if car < bestcar:
                    bestcar = car; bestc = code
        return bestc
    bestc = -1; bestcar = 1 << 30
    for a in range(9):
        for b in range(9):
            v[f0] = a; v[f1] = b
            code = v[0] * 81 + v[1] * 9 + v[2]
            pa = PAYi[code, f0]; pb = PAYi[code, f1]
            ok = True
            for a2 in range(9):
                v[f0] = a2; v[f1] = b
                c2 = v[0] * 81 + v[1] * 9 + v[2]
                if PAYi[c2, f0] > pa:
                    ok = False; break
            if ok:
                for b2 in range(9):
                    v[f0] = a; v[f1] = b2
                    c2 = v[0] * 81 + v[1] * 9 + v[2]
                    if PAYi[c2, f1] > pb:
                        ok = False; break
            if ok:
                car = 0
                for s in range(3):
                    if wcar[s]:
                        car += PAYi[code, s]
                if car < bestcar:
                    bestcar = car; bestc = code
    return bestc


@njit(cache=True)
def enc2_compute(A, C1, ST, P, t0, t1, t2):
    """stage-2 joint code of the type triple, with the execution semantics of the arm."""
    tprog = ST[1]
    x0 = tprog[0, t0]; x1 = tprog[1, t1]; x2 = tprog[2, t2]
    p = stage1(A, C1, x0, x1, x2)
    f0 = lookup_fill(ST, 0, t0, p); f1 = lookup_fill(ST, 1, t1, p); f2 = lookup_fill(ST, 2, t2, p)
    if f0 < 0 and f1 < 0 and f2 < 0:
        return p
    fm = np.zeros(3, np.bool_); fv = np.zeros(3, np.int64)
    if f0 >= 0:
        fm[0] = True; fv[0] = f0
    if f1 >= 0:
        fm[1] = True; fv[1] = f1
    if f2 >= 0:
        fm[2] = True; fv[2] = f2
    if P[P_EXE] == EXE_BR and (not (fm[0] and fm[1] and fm[2])):
        c = best_reply_code(A, fm, fv, fm)
        if c >= 0:
            return c
    return eval_fixed(A, x0, x1, x2, fm, fv)


@njit(cache=True)
def tcode(A, C1, C2, ST, P, t0, t1, t2):
    """cached stage-2 joint code of the type triple (keys from the types' serial numbers)."""
    ser = ST[9]
    keys, vals, meta, bits = C2
    key = (np.uint64(ser[0, t0]) << np.uint64(42)) | (np.uint64(ser[1, t1]) << np.uint64(21)) | np.uint64(ser[2, t2])
    key = key + np.uint64(1)
    h = (key * np.uint64(0x9E3779B97F4A7C15)) >> np.uint64(64 - bits)
    mask = (np.int64(1) << bits) - 1
    p = np.int64(h)
    while True:
        kk = keys[p]
        if kk == key:
            return np.int64(vals[p])
        if kk == 0:
            code = enc2_compute(A, C1, ST, P, t0, t1, t2)
            if meta[0] * 10 < ((np.int64(1) << bits) * 5):
                keys[p] = key; vals[p] = code; meta[0] += 1
            return code
        p = (p + 1) & mask


@njit(cache=True)
def tcod(A, C1, C2, ST, P, s, k, p, q):
    if s == 0:
        return tcode(A, C1, C2, ST, P, k, p, q)
    if s == 1:
        return tcode(A, C1, C2, ST, P, p, k, q)
    return tcode(A, C1, C2, ST, P, p, q, k)


# ====================================================================== state container (numba tuple)
def new_state():
    cnt = np.zeros((3, TM), np.int64)
    tprog = -np.ones((3, TM), np.int64)
    tn = np.zeros((3, TM), np.int64)
    tkey = np.zeros((3, TM, CW), np.int64)
    tfil = np.zeros((3, TM, CW), np.int64)
    tbun = np.zeros((3, TM, CW), np.int64)
    pres = np.zeros((3, TM), np.int64)
    npres = np.zeros(3, np.int64)
    pos = -np.ones((3, TM), np.int64)
    ser = np.zeros((3, TM), np.int64)
    F = np.zeros((3, TM))
    mi = np.zeros(16, np.int64)       # see MI_*
    mf = np.zeros(16)                 # see MF_*; absolute generations
    return (cnt, tprog, tn, tkey, tfil, tbun, pres, npres, pos, ser, F, mi, mf)


def init_state_from_counts(counts):
    """counts (3, K) program counts -> state with bare-program types in increasing program order (the stored kernel's
    presence order)."""
    ST = new_state()
    cnt, tprog, tn, tkey, tfil, tbun, pres, npres, pos, ser, F, mi, mf = ST
    for s in range(3):
        for k in np.nonzero(counts[s])[0]:
            t = int(npres[s])
            tprog[s, t] = k; cnt[s, t] = counts[s, k]; pres[s, t] = t; pos[s, t] = t; npres[s] += 1
            ser[s, t] = mi[MI_NEXTSER]; mi[MI_NEXTSER] += 1
    mi[MI_CLS] = -1; mi[MI_SETTLED] = -1
    return ST


def new_trk():
    return np.zeros((NTRK, TRK_W))


# ====================================================================== type table operations
@njit(cache=True)
def find_type(ST, s, prog, nent, ekey, efil, ebun):
    """id of a live type of slot s with this program and exactly this entry list, or -1."""
    tprog = ST[1]; tn = ST[2]; tkey = ST[3]; tfil = ST[4]; tbun = ST[5]; pres = ST[6]; npres = ST[7]
    for i in range(npres[s]):
        t = pres[s, i]
        if tprog[s, t] != prog or tn[s, t] != nent:
            continue
        ok = True
        for e in range(nent):
            if tkey[s, t, e] != ekey[e] or tfil[s, t, e] != efil[e] or tbun[s, t, e] != ebun[e]:
                ok = False; break
        if ok:
            return t
    return -1


@njit(cache=True)
def alloc_type(ST, s, prog, nent, ekey, efil, ebun):
    cnt = ST[0]; tprog = ST[1]; tn = ST[2]; tkey = ST[3]; tfil = ST[4]; tbun = ST[5]; ser = ST[9]; mi = ST[11]
    for t in range(TM):
        if tprog[s, t] < 0:
            tprog[s, t] = prog; tn[s, t] = nent
            for e in range(nent):
                tkey[s, t, e] = ekey[e]; tfil[s, t, e] = efil[e]; tbun[s, t, e] = ebun[e]
            ser[s, t] = mi[MI_NEXTSER]; mi[MI_NEXTSER] += 1
            cnt[s, t] = 0
            return t
    return -1


@njit(cache=True)
def get_or_make(ST, s, prog, nent, ekey, efil, ebun):
    t = find_type(ST, s, prog, nent, ekey, efil, ebun)
    if t >= 0:
        return t
    return alloc_type(ST, s, prog, nent, ekey, efil, ebun)


@njit(cache=True)
def with_entry(ST, s, t, p, fill, bun, cap):
    """entry list of type t of slot s with the entry (p, fill, bun) appended after removing any entry with key p; the
    oldest is evicted past the cap.  Returns (nent, ekey, efil, ebun, evicted)."""
    tn = ST[2]; tkey = ST[3]; tfil = ST[4]; tbun = ST[5]
    ekey = np.zeros(CW + 1, np.int64); efil = np.zeros(CW + 1, np.int64); ebun = np.zeros(CW + 1, np.int64)
    m = 0
    for e in range(tn[s, t]):
        if tkey[s, t, e] != p:
            ekey[m] = tkey[s, t, e]; efil[m] = tfil[s, t, e]; ebun[m] = tbun[s, t, e]; m += 1
    ekey[m] = p; efil[m] = fill; ebun[m] = bun; m += 1
    ev = 0
    if m > cap:
        for e in range(1, m):
            ekey[e - 1] = ekey[e]; efil[e - 1] = efil[e]; ebun[e - 1] = ebun[e]
        m -= 1; ev = 1
    return m, ekey, efil, ebun, ev


# ====================================================================== fitness and replacement (the stored kernel's update)
@njit(cache=True)
def fit_type(A, C1, C2, ST, P, s, k):
    cnt = ST[0]; pres = ST[6]; npres = ST[7]
    PAYf = A[7]
    o1, o2 = _others(s)
    v = 0.0
    for t1 in range(npres[o1]):
        p = pres[o1, t1]
        for t2 in range(npres[o2]):
            q = pres[o2, t2]
            v += cnt[o1, p] * cnt[o2, q] * PAYf[tcod(A, C1, C2, ST, P, s, k, p, q), s]
    return v


@njit(cache=True)
def full_F(A, C1, C2, ST, P):
    pres = ST[6]; npres = ST[7]; F = ST[10]; mi = ST[11]
    for s in range(3):
        for i in range(npres[s]):
            k = pres[s, i]
            F[s, k] = fit_type(A, C1, C2, ST, P, s, k)
    mi[MI_FVALID] = 1


@njit(cache=True)
def check_neutral(A, C1, C2, ST, P):
    """1 if every present type triple yields the same payoff vector (no frequency dependence at all), else 0."""
    pres = ST[6]; npres = ST[7]
    PAYi = A[8]
    if npres[0] * npres[1] * npres[2] > 600:
        return 0
    first = True
    r0 = 0; r1 = 0; r2 = 0
    for i0 in range(npres[0]):
        for i1 in range(npres[1]):
            for i2 in range(npres[2]):
                c = tcode(A, C1, C2, ST, P, pres[0, i0], pres[1, i1], pres[2, i2])
                if first:
                    r0 = PAYi[c, 0]; r1 = PAYi[c, 1]; r2 = PAYi[c, 2]; first = False
                elif PAYi[c, 0] != r0 or PAYi[c, 1] != r1 or PAYi[c, 2] != r2:
                    return 0
    return 1


@njit(cache=True)
def set_active(u, a, act, apos, nact):
    p = apos[u]
    if a and p >= nact:
        j = act[nact]; act[nact] = u; act[p] = j; apos[u] = nact; apos[j] = p; nact += 1
    elif (not a) and p < nact:
        nact -= 1; j = act[nact]; act[nact] = u; act[p] = j; apos[u] = nact; apos[j] = p
    return nact


@njit(cache=True)
def replace1(A, C1, C2, ST, P, act, apos, nact, s, child, victim):
    """one birth-death replacement in slot s (victim type -> child type, victim != child); the stored kernel's update with
    the neutral fast path.  Returns the new nact."""
    cnt = ST[0]; tprog = ST[1]; tn = ST[2]; pres = ST[6]; npres = ST[7]; pos = ST[8]; F = ST[10]; mi = ST[11]
    PAYf = A[7]
    was_neutral = mi[MI_NEUTRAL] == 1
    struct = False
    cnt[s, victim] -= 1
    died = False
    if cnt[s, victim] == 0:
        p = pos[s, victim]; last = pres[s, npres[s] - 1]
        pres[s, p] = last; pos[s, last] = p; pos[s, victim] = -1; npres[s] -= 1
        died = True; struct = True
    new = cnt[s, child] == 0
    if new:
        pres[s, npres[s]] = child; pos[s, child] = npres[s]; npres[s] += 1
        struct = True
    cnt[s, child] += 1
    mi[MI_DIRTY] = 1
    nn = was_neutral
    if struct:
        nn = check_neutral(A, C1, C2, ST, P) == 1
    if nn:
        mi[MI_NEUTRAL] = 1; mi[MI_FVALID] = 0
    else:
        mi[MI_NEUTRAL] = 0
        if was_neutral or mi[MI_FVALID] == 0:
            full_F(A, C1, C2, ST, P)
        else:
            o1, o2 = _others(s)
            for sa in (o1, o2):
                sb = o1 + o2 - sa
                for ta in range(npres[sa]):
                    k = pres[sa, ta]
                    v = 0.0
                    for tb in range(npres[sb]):
                        q = pres[sb, tb]
                        if s < sb:
                            v += cnt[sb, q] * (PAYf[tcod(A, C1, C2, ST, P, sa, k, child, q), sa] - PAYf[tcod(A, C1, C2, ST, P, sa, k, victim, q), sa])
                        else:
                            v += cnt[sb, q] * (PAYf[tcod(A, C1, C2, ST, P, sa, k, q, child), sa] - PAYf[tcod(A, C1, C2, ST, P, sa, k, q, victim), sa])
                    F[sa, k] += v
            if new:
                F[s, child] = fit_type(A, C1, C2, ST, P, s, child)
    if died:
        tprog[s, victim] = -1; tn[s, victim] = 0
    return set_active(s, npres[s] > 1, act, apos, nact)


@njit(cache=True)
def pick_parent(ST, s, N2, w, neutral):
    cnt = ST[0]; pres = ST[6]; npres = ST[7]; F = ST[10]
    if neutral:
        tot = 0.0
        for t in range(npres[s]):
            tot += cnt[s, pres[s, t]]
        u = np.random.random() * tot; acc = 0.0
        for t in range(npres[s]):
            k = pres[s, t]
            acc += cnt[s, k]
            if u <= acc:
                return k
        return pres[s, npres[s] - 1]
    m = -1e300
    for t in range(npres[s]):
        k = pres[s, t]
        f = F[s, k] / N2
        if f > m: m = f
    tot = 0.0
    for t in range(npres[s]):
        k = pres[s, t]
        tot += cnt[s, k] * np.exp(w * (F[s, k] / N2 - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[s]):
        k = pres[s, t]
        acc += cnt[s, k] * np.exp(w * (F[s, k] / N2 - m))
        if u <= acc:
            return k
    return pres[s, npres[s] - 1]


@njit(cache=True)
def pick_individual(ST, s, N):
    """type id of a uniformly drawn individual of slot s."""
    cnt = ST[0]; pres = ST[6]; npres = ST[7]
    r = np.random.randint(N); acc = 0; v = pres[s, 0]
    for t in range(npres[s]):
        k = pres[s, t]; acc += cnt[s, k]
        if r < acc:
            v = k; break
    return v


# ====================================================================== classification
CATC = np.zeros(NOUT + 2, np.int64)       # class id -> category 0..5 (F U G W D mixed/other)
for _o in range(NOUT):
    CATC[_o] = CATMAP[_o]
CATC[NOUT] = 5
CATC[NOUT + 1] = 5


@njit(cache=True)
def class_of(A, C1, C2, ST, P, N):
    """stored `_classify`: outcome id with >= 0.95 of the encounter mass, NOUT (member-mixed: fair pairs jointly >= 0.95) or
    NOUT + 1 (other, also when the state is too polymorphic to classify cheaply)."""
    cnt = ST[0]; pres = ST[6]; npres = ST[7]
    VECt = A[9]
    if npres[0] * npres[1] * npres[2] > 3000:
        return NOUT + 1
    dist = np.zeros(NOUT)
    N3 = float(N) ** 3
    for i0 in range(npres[0]):
        a = pres[0, i0]
        for i1 in range(npres[1]):
            b = pres[1, i1]
            for i2 in range(npres[2]):
                c = pres[2, i2]
                code = tcode(A, C1, C2, ST, P, a, b, c)
                dist[VECt[code]] += cnt[0, a] * cnt[1, b] * cnt[2, c] / N3
    mx = 0.0; arg = 0
    for o in range(NOUT):
        if dist[o] > mx:
            mx = dist[o]; arg = o
    if mx >= 0.95:
        return arg
    mem = 0.0
    for o in range(MI_V.shape[0]):
        mem += dist[MI_V[o]]
    if mem >= 0.95:
        return NOUT
    return NOUT + 1


@njit(cache=True)
def cat_of(cls):
    if cls < 0:
        return 6
    if cls < NOUT:
        return CATC[cls]
    return 5


# ====================================================================== proposal test
@njit(cache=True)
def test_proposal(A, ST, P, ts0, ts1, ts2, Smask, newa, p, fills, pay_before, stat):
    """Does every member of S strictly gain?  The types of the encounter triple are ts, newa[s] the proposal for s in S, p the
    stage-1 code, fills[s] the type's entry for p (-1 if none), pay_before[s] the stage-2 payoff (sixths) with the contracts
    in force.  Responders by the acceptance mode."""
    tprog = ST[1]
    PAYi = A[8]
    x0 = tprog[0, ts0]; x1 = tprog[1, ts1]; x2 = tprog[2, ts2]
    acc = int(P[P_ACC])
    fm = np.zeros(3, np.bool_); fv = np.zeros(3, np.int64)
    nU = 0
    for s in range(3):
        if (Smask >> s) & 1:
            fm[s] = True; fv[s] = newa[s]
        elif fills[s] >= 0:
            fm[s] = True; fv[s] = fills[s]
        else:
            nU += 1
    if acc == ACC_NR:
        for s in range(3):
            if not fm[s]:
                fm[s] = True; fv[s] = act_of(p, s)
        code = fv[0] * 81 + fv[1] * 9 + fv[2]
        for s in range(3):
            if (Smask >> s) & 1:
                if PAYi[code, s] <= pay_before[s]:
                    return 0
        return 1
    if acc == ACC_BR and nU > 0:
        fu = np.zeros(3, np.int64)
        for s in range(3):
            fu[s] = fv[s] if fm[s] else 0
        if nU == 1:
            f0 = 0
            for s in range(3):
                if not fm[s]: f0 = s
            bestp = -1000
            for a in range(9):
                fu[f0] = a
                c = fu[0] * 81 + fu[1] * 9 + fu[2]
                if PAYi[c, f0] > bestp: bestp = PAYi[c, f0]
            for a in range(9):
                fu[f0] = a
                c = fu[0] * 81 + fu[1] * 9 + fu[2]
                if PAYi[c, f0] == bestp:
                    for s in range(3):
                        if (Smask >> s) & 1 and PAYi[c, s] <= pay_before[s]:
                            stat[ST_BR_FAIL] += 1
                            return 0
            return 1
        f0 = -1; f1 = -1
        for s in range(3):
            if not fm[s]:
                if f0 < 0: f0 = s
                else: f1 = s
        neq = 0
        for a in range(9):
            for b in range(9):
                fu[f0] = a; fu[f1] = b
                c = fu[0] * 81 + fu[1] * 9 + fu[2]
                pa = PAYi[c, f0]; pb = PAYi[c, f1]
                ok = True
                for a2 in range(9):
                    fu[f0] = a2; fu[f1] = b
                    c2 = fu[0] * 81 + fu[1] * 9 + fu[2]
                    if PAYi[c2, f0] > pa:
                        ok = False; break
                if ok:
                    for b2 in range(9):
                        fu[f0] = a; fu[f1] = b2
                        c2 = fu[0] * 81 + fu[1] * 9 + fu[2]
                        if PAYi[c2, f1] > pb:
                            ok = False; break
                if ok:
                    neq += 1
                    for s in range(3):
                        if (Smask >> s) & 1 and PAYi[c, s] <= pay_before[s]:
                            stat[ST_BR_FAIL] += 1
                            return 0
        if neq == 0:
            stat[ST_BR_NOEQ] += 1
            return 0
        return 1
    if nU > 0:
        code = eval_fixed(A, x0, x1, x2, fm, fv)
    else:
        code = fv[0] * 81 + fv[1] * 9 + fv[2]
    for s in range(3):
        if (Smask >> s) & 1:
            if PAYi[code, s] <= pay_before[s]:
                return 0
    return 1


# ====================================================================== bundle codes
@njit(cache=True)
def bundle_code(p, smask, newa):
    c = p * 8 + smask
    for s in range(3):
        v = newa[s] + 1 if (smask >> s) & 1 else 0
        c = c * 10 + v
    return c


@njit(cache=True)
def bundle_decode(c, newa):
    for s in range(2, -1, -1):
        v = c % 10; c //= 10
        newa[s] = v - 1
    smask = c % 8; c //= 8
    return c, smask


# ====================================================================== genesis
@njit(cache=True)
def half_gain(A, C1, ST, P, s, t, p, fill, bun, N):
    """fitness change (dollars) of a lone carrier of the entry (p, fill) of type t in slot s against the island's current
    populations (the carrier's own effect on the others is not counted): the signer's gain without the other signer present."""
    cnt = ST[0]; tprog = ST[1]; tn = ST[2]; tkey = ST[3]; tfil = ST[4]; tbun = ST[5]; pres = ST[6]; npres = ST[7]
    PAYf = A[7]
    o1, o2 = _others(s)
    cap = int(P[P_CAP])
    nent, ekey, efil, ebun, ev = with_entry(ST, s, t, p, fill, bun, cap)
    sn = tn[s, t]
    sk = tkey[s, t].copy(); sf = tfil[s, t].copy(); sb = tbun[s, t].copy()
    base = 0.0
    for i1 in range(npres[o1]):
        q1 = pres[o1, i1]
        for i2 in range(npres[o2]):
            q2 = pres[o2, i2]
            if s == 0:
                c = enc2_compute(A, C1, ST, P, t, q1, q2)
            elif s == 1:
                c = enc2_compute(A, C1, ST, P, q1, t, q2)
            else:
                c = enc2_compute(A, C1, ST, P, q1, q2, t)
            base += cnt[o1, q1] * cnt[o2, q2] * PAYf[c, s]
    tn[s, t] = nent
    for e in range(CW):
        tkey[s, t, e] = ekey[e]; tfil[s, t, e] = efil[e]; tbun[s, t, e] = ebun[e]
    new = 0.0
    for i1 in range(npres[o1]):
        q1 = pres[o1, i1]
        for i2 in range(npres[o2]):
            q2 = pres[o2, i2]
            if s == 0:
                c = enc2_compute(A, C1, ST, P, t, q1, q2)
            elif s == 1:
                c = enc2_compute(A, C1, ST, P, q1, t, q2)
            else:
                c = enc2_compute(A, C1, ST, P, q1, q2, t)
            new += cnt[o1, q1] * cnt[o2, q2] * PAYf[c, s]
    tn[s, t] = sn
    for e in range(CW):
        tkey[s, t, e] = sk[e]; tfil[s, t, e] = sf[e]; tbun[s, t, e] = sb[e]
    return (new - base) / (float(N) * N)


@njit(cache=True)
def install_one(A, C1, C2, ST, P, act, apos, nact, s, t, p, fill, bun, stat):
    """install the entry (p, fill, bun) on one individual of type t in slot s; returns (nact, ok)."""
    tprog = ST[1]
    cap = int(P[P_CAP])
    nent, ekey, efil, ebun, ev = with_entry(ST, s, t, p, fill, bun, cap)
    prog = tprog[s, t]
    child = get_or_make(ST, s, prog, nent, ekey, efil, ebun)
    if child < 0:
        stat[ST_TABFULL] += 1
        return nact, False
    if ev:
        stat[ST_EVICT] += 1
    if child == t:
        return nact, True
    nact = replace1(A, C1, C2, ST, P, act, apos, nact, s, child, t)
    return nact, True


@njit(cache=True)
def pick_other_with_prog(ST, s, prog, taken):
    """a uniformly drawn individual of slot s with program prog among those not yet taken (taken counts by type id)."""
    cnt = ST[0]; tprog = ST[1]; pres = ST[6]; npres = ST[7]
    tot = 0
    for i in range(npres[s]):
        k = pres[s, i]
        if tprog[s, k] == prog:
            tot += cnt[s, k] - taken[k]
    if tot <= 0:
        return -1
    r = np.random.randint(tot); acc = 0
    for i in range(npres[s]):
        k = pres[s, i]
        if tprog[s, k] == prog:
            acc += cnt[s, k] - taken[k]
            if r < acc:
                return k
    return -1


@njit(cache=True)
def pick_copy(A, C1, ST, N, newa, ts, stat):
    """arm C: choose a surviving bundle by the frequency of its carriers, then an encounter among the island's present type
    triples whose stage-1 profile is the bundle's key (by frequency).  Returns (smask, ok); on ok, newa holds the bundle's
    fills and ts the encounter triple."""
    cnt = ST[0]; tprog = ST[1]; tn = ST[2]; tbun = ST[5]; pres = ST[6]; npres = ST[7]
    nb = 0
    codes = np.zeros(64, np.int64); wts = np.zeros(64, np.int64)
    for s in range(3):
        for i in range(npres[s]):
            t = pres[s, i]
            for e in range(tn[s, t]):
                b = tbun[s, t, e]
                if b == 0:
                    continue
                j = -1
                for q in range(nb):
                    if codes[q] == b:
                        j = q; break
                if j < 0 and nb < 64:
                    codes[nb] = b; wts[nb] = 0; j = nb; nb += 1
                if j >= 0:
                    wts[j] += cnt[s, t]
    tot = 0
    for q in range(nb):
        tot += wts[q]
    if tot <= 0:
        stat[ST_UNMATCHED] += 1
        return 0, False
    r = np.random.randint(tot); acc = 0; qb = 0
    for q in range(nb):
        acc += wts[q]
        if r < acc:
            qb = q; break
    b = codes[qb]
    key, smask = bundle_decode(b, newa)
    wsum = 0.0
    for i0 in range(npres[0]):
        for i1 in range(npres[1]):
            for i2 in range(npres[2]):
                t0 = pres[0, i0]; t1 = pres[1, i1]; t2 = pres[2, i2]
                if stage1(A, C1, tprog[0, t0], tprog[1, t1], tprog[2, t2]) == key:
                    wsum += cnt[0, t0] * cnt[1, t1] * cnt[2, t2]
    if wsum <= 0:
        stat[ST_UNMATCHED] += 1
        return 0, False
    u = np.random.random() * wsum; accf = 0.0
    for i0 in range(npres[0]):
        for i1 in range(npres[1]):
            for i2 in range(npres[2]):
                t0 = pres[0, i0]; t1 = pres[1, i1]; t2 = pres[2, i2]
                if stage1(A, C1, tprog[0, t0], tprog[1, t1], tprog[2, t2]) == key:
                    accf += cnt[0, t0] * cnt[1, t1] * cnt[2, t2]
                    if u <= accf:
                        ts[0] = t0; ts[1] = t1; ts[2] = t2
                        return smask, True
    return 0, False


@njit(cache=True)
def genesis_attempt(A, C1, C2, ST, P, act, apos, nact, N, stat, trk, now_abs, copied):
    """One genesis attempt (a uniform proposal, or, for arm C, a copied bundle).  Returns the new nact."""
    tprog = ST[1]; mi = ST[11]; mf = ST[12]
    PAYi = A[8]
    ts = np.zeros(3, np.int64)
    newa = np.zeros(3, np.int64)
    cur_cat = cat_of(mi[MI_CLS]); set_cat = cat_of(mi[MI_SETTLED])
    smask = 0
    if copied:
        smask, ok = pick_copy(A, C1, ST, N, newa, ts, stat)
        if not ok:
            return nact
        stat[ST_COPY_ATT] += 1
    else:
        for s in range(3):
            ts[s] = pick_individual(ST, s, N)
        smask = 1 + np.random.randint(7)
        stat[ST_UNI_ATT] += 1
    p = stage1(A, C1, tprog[0, ts[0]], tprog[1, ts[1]], tprog[2, ts[2]])
    fills = np.empty(3, np.int64)
    for s in range(3):
        fills[s] = lookup_fill(ST, s, ts[s], p)
    c2 = tcode(A, C1, C2, ST, P, ts[0], ts[1], ts[2])
    pay_before = np.empty(3, np.int64)
    for s in range(3):
        pay_before[s] = PAYi[c2, s]
    k = 0
    for s in range(3):
        if (smask >> s) & 1:
            k += 1
    stat[ST_ATT_S + k - 1] += 1
    stat[ST_ATT_C + cur_cat] += 1; stat[ST_ATT_SC + set_cat] += 1
    if not copied:
        nprof = 1
        for i in range(k):
            nprof *= 9
        nprof -= 1
        r = np.random.randint(nprof)
        curidx = 0
        for s in range(3):
            if (smask >> s) & 1:
                curidx = curidx * 9 + act_of(c2, s)
        if r >= curidx:
            r += 1
        for s in range(2, -1, -1):
            if (smask >> s) & 1:
                newa[s] = r % 9; r //= 9
    else:
        same = True
        for s in range(3):
            if (smask >> s) & 1 and newa[s] != act_of(c2, s):
                same = False
        if same:
            stat[ST_NOCHANGE] += 1
            return nact
    if int(P[P_HOOK]) == HOOK_H:
        for s in range(3):
            if (smask >> s) & 1:
                if leaf_hook(A, s, tprog[s, ts[s]], p) < 0:
                    stat[ST_BLK_S + k - 1] += 1
                    return nact
    if P[P_FILT] < 0.5:
        accepted = True
    else:
        accepted = test_proposal(A, ST, P, ts[0], ts[1], ts[2], smask, newa, p, fills, pay_before, stat) == 1
    if not accepted:
        return nact
    stat[ST_ACC_S + k - 1] += 1
    stat[ST_ACC_C + cur_cat] += 1; stat[ST_ACC_SC + set_cat] += 1
    if copied:
        stat[ST_COPY_ACC] += 1
    else:
        stat[ST_UNI_ACC] += 1
    mf[MF_LASTACC] = now_abs
    bun = bundle_code(p, smask, newa)
    nbc = int(P[P_BCAST])
    gains = np.zeros(3)
    for s in range(3):
        if (smask >> s) & 1:
            gains[s] = half_gain(A, C1, ST, P, s, ts[s], p, newa[s], bun, N)
    progs = np.zeros(3, np.int64)
    for s in range(3):
        progs[s] = tprog[s, ts[s]]
    for s in range(3):
        if (smask >> s) & 1:
            t = ts[s]
            nact, ok = install_one(A, C1, C2, ST, P, act, apos, nact, s, t, p, newa[s], bun, stat)
            stat[ST_INST_S + k - 1] += 1
            if nbc > 0 and ok:
                taken = np.zeros(TM, np.int64)
                for j in range(nbc):
                    stat[ST_BC_WANT] += 1
                    tt = pick_other_with_prog(ST, s, progs[s], taken)
                    if tt < 0:
                        break
                    # take one individual of type tt: install the entry on it (its type changes)
                    nact, ok2 = install_one(A, C1, C2, ST, P, act, apos, nact, s, tt, p, newa[s], bun, stat)
                    if ok2:
                        stat[ST_BC_INST] += 1
    for i in range(trk.shape[0]):
        if trk[i, 0] == 0:
            trk[i, 0] = 1; trk[i, 1] = bun; trk[i, 2] = now_abs; trk[i, 3] = smask; trk[i, 4] = cur_cat
            trk[i, 5] = 0; trk[i, 6] = 0; trk[i, 7] = 0
            trk[i, 8] = now_abs; trk[i, 9] = now_abs; trk[i, 10] = now_abs
            trk[i, 11] = 0; trk[i, 12] = p
            for s in range(3):
                trk[i, 13 + s] = newa[s] if (smask >> s) & 1 else -1
            trk[i, 16] = set_cat
            trk[i, 17] = 1.0 if copied else 0.0
            for s in range(3):
                trk[i, 18 + s] = gains[s]
            mi[MI_NTRACK] += 1
            return nact
    stat[ST_NTRACKFULL] += 1
    return nact


# ====================================================================== the exhaustive oracle
@njit(cache=True)
def oracle(A, C1, C2, ST, P, N, out, maxprod):
    """Exhaustive search for improving contracts on the island state: every present type triple, coalition and action
    profile (differing from S's stage-2 actions).  out[0:3] = expected acceptance probability mass per genesis draw by |S|
    (frequency of the triple x 1/7 x accepted proposals / (9^k - 1)), out[3:6] = counts of accepted (triple, S, profile),
    out[6] = number of triples examined, out[7] = 1 if the search was skipped (too many triples), out[8] = accepted by
    hook-blocked proposals (not counted)."""
    cnt = ST[0]; tprog = ST[1]; pres = ST[6]; npres = ST[7]
    PAYi = A[8]
    if npres[0] * npres[1] * npres[2] > maxprod:
        out[7] = 1.0
        return
    stat = np.zeros(ST_LEN, np.int64)
    N3 = float(N) ** 3
    for i0 in range(npres[0]):
        t0 = pres[0, i0]
        for i1 in range(npres[1]):
            t1 = pres[1, i1]
            for i2 in range(npres[2]):
                t2 = pres[2, i2]
                wt = cnt[0, t0] * cnt[1, t1] * cnt[2, t2] / N3
                out[6] += 1.0
                p = stage1(A, C1, tprog[0, t0], tprog[1, t1], tprog[2, t2])
                fills = np.empty(3, np.int64)
                fills[0] = lookup_fill(ST, 0, t0, p); fills[1] = lookup_fill(ST, 1, t1, p); fills[2] = lookup_fill(ST, 2, t2, p)
                c2 = tcode(A, C1, C2, ST, P, t0, t1, t2)
                pay_before = np.empty(3, np.int64)
                for s in range(3):
                    pay_before[s] = PAYi[c2, s]
                for smask in range(1, 8):
                    k = 0
                    for s in range(3):
                        if (smask >> s) & 1:
                            k += 1
                    blocked = False
                    if int(P[P_HOOK]) == HOOK_H:
                        for s in range(3):
                            ts_ = t0 if s == 0 else (t1 if s == 1 else t2)
                            if (smask >> s) & 1:
                                if leaf_hook(A, s, tprog[s, ts_], p) < 0:
                                    blocked = True
                    if blocked:
                        continue
                    nprof = 1
                    for i in range(k):
                        nprof *= 9
                    curidx = 0
                    for s in range(3):
                        if (smask >> s) & 1:
                            curidx = curidx * 9 + act_of(c2, s)
                    na = np.zeros(3, np.int64)
                    nacc = 0
                    for r0 in range(nprof):
                        if r0 == curidx:
                            continue
                        r = r0
                        for s in range(2, -1, -1):
                            if (smask >> s) & 1:
                                na[s] = r % 9; r //= 9
                        if P[P_FILT] < 0.5 or test_proposal(A, ST, P, t0, t1, t2, smask, na, p, fills, pay_before, stat) == 1:
                            nacc += 1
                    out[3 + k - 1] += nacc
                    out[k - 1] += wt * (1.0 / 7.0) * nacc / (nprof - 1)


def acceptance_profile(R, isl, maxprod=64):
    R.arm.clear_c2()
    out = np.zeros(10)
    oracle(R.A, R.arm.c1, R.arm.c2, isl.ST, R.P, int(R.P[P_N]), out, maxprod)
    return out


# ====================================================================== bundle tracking
@njit(cache=True)
def track_update(ST, trk, now_abs, N, ev, nev):
    """update the tracked bundles' carrier counts; emit a record when all signer halves are extinct or 2,000 generations
    have passed.  Returns the new nev."""
    cnt = ST[0]; tn = ST[2]; tbun = ST[5]; pres = ST[6]; npres = ST[7]; mi = ST[11]
    for i in range(trk.shape[0]):
        if trk[i, 0] == 0:
            continue
        bun = int(trk[i, 1]); smask = int(trk[i, 3])
        alive_any = False
        simult = True
        for s in range(3):
            if not ((smask >> s) & 1):
                continue
            c = 0
            for j in range(npres[s]):
                t = pres[s, j]
                for e in range(tn[s, t]):
                    if tbun[s, t, e] == bun:
                        c += cnt[s, t]; break
            if c > trk[i, 5 + s]:
                trk[i, 5 + s] = c
            if c > 0:
                alive_any = True
                trk[i, 8 + s] = now_abs
            if 2 * c <= N:
                simult = False
        if simult:
            trk[i, 11] = 1
        done = (not alive_any) or (now_abs - trk[i, 2] >= 2000.0)
        if done:
            if nev < ev.shape[0]:
                ev[nev, 0] = trk[i, 2]
                ev[nev, 1] = smask; ev[nev, 2] = trk[i, 4]; ev[nev, 3] = trk[i, 12]
                ev[nev, 4] = trk[i, 13]; ev[nev, 5] = trk[i, 14]; ev[nev, 6] = trk[i, 15]
                ev[nev, 7] = trk[i, 5]; ev[nev, 8] = trk[i, 6]; ev[nev, 9] = trk[i, 7]
                ev[nev, 10] = trk[i, 8] - trk[i, 2]; ev[nev, 11] = trk[i, 9] - trk[i, 2]; ev[nev, 12] = trk[i, 10] - trk[i, 2]
                ev[nev, 13] = trk[i, 11]; ev[nev, 14] = 1.0 if alive_any else 0.0
                ev[nev, 15] = trk[i, 16]; ev[nev, 16] = trk[i, 17]; ev[nev, 17] = now_abs
                ev[nev, 18] = trk[i, 18]; ev[nev, 19] = trk[i, 19]; ev[nev, 20] = trk[i, 20]
                nev += 1
            trk[i, 0] = 0
            mi[MI_NTRACK] -= 1
    return nev


# ====================================================================== class bookkeeping
@njit(cache=True)
def touch(A, C1, C2, ST, P, N, now_abs, cev, STATF):
    """Class bookkeeping at absolute time now_abs (generations): accumulate island-generations by category, declare the class
    settled after 500 generations, and refresh the instantaneous class if the state changed."""
    mi = ST[11]; mf = ST[12]
    dt = now_abs - mf[MF_LASTTOUCH]
    if dt > 0.0:
        STATF[STF_GEN_C + cat_of(mi[MI_CLS])] += dt
        STATF[STF_GEN_SC + cat_of(mi[MI_SETTLED])] += dt
        mf[MF_LASTTOUCH] = now_abs
    if mi[MI_CLS] != mi[MI_SETTLED] and mi[MI_CLS] >= 0:
        held = now_abs - mf[MF_CLSSINCE]
        if held >= 500.0:
            old = mi[MI_SETTLED]
            mi[MI_SETTLED] = mi[MI_CLS]
            mf[MF_SETSINCE] = mf[MF_CLSSINCE] + 500.0
            n = int(cev[0, 0])
            if n + 1 < cev.shape[0]:
                cev[n + 1, 0] = mf[MF_CLSSINCE] + 500.0
                cev[n + 1, 1] = old; cev[n + 1, 2] = mi[MI_SETTLED]
                cev[n + 1, 3] = mf[MF_LASTMIG]
                cev[n + 1, 4] = mf[MF_LASTACC]
                cev[n + 1, 5] = mf[MF_CLSSINCE]
                cev[0, 0] = n + 1
    if mi[MI_DIRTY] != 0:
        nc = class_of(A, C1, C2, ST, P, N)
        mi[MI_DIRTY] = 0
        if nc != mi[MI_CLS]:
            mi[MI_CLS] = nc
            mf[MF_CLSSINCE] = now_abs


@njit(cache=True)
def init_class(A, C1, C2, ST, P, N, now_abs):
    mi = ST[11]; mf = ST[12]
    mi[MI_CLS] = class_of(A, C1, C2, ST, P, N)
    mi[MI_SETTLED] = -1
    mi[MI_DIRTY] = 0
    mf[MF_CLSSINCE] = now_abs; mf[MF_LASTTOUCH] = now_abs
    mf[MF_LASTMIG] = -1e18; mf[MF_LASTACC] = -1e18


# ====================================================================== the island run
@njit(cache=True)
def advance(A, C1, C2, ST, P, X, nx, Hgen, seed, cum, STAT, STATF, trk, ev, cev, nevs, abs_g0):
    """Run one island for Hgen generations (a generation is 3N slot-events) with genesis at rate nu per generation and the
    exogenous events X (rows: time in generations from the call start, kind 0 annealing arrival / 1 migrant, slot, program,
    nent, then (key, fill, bundle) x CW).  With nu = 0 and only annealing arrivals the random-number order is that of
    `many_islands.island_run`.  Returns (status, generations run): status 0 = settled (all slots monomorphic in types, nothing
    can change), 1 = ran to Hgen."""
    cnt = ST[0]; pres = ST[6]; npres = ST[7]; mi = ST[11]; mf = ST[12]
    np.random.seed(seed)
    N = int(P[P_N]); w = P[P_W]; nu = P[P_NU]
    NU = 3
    UN = float(NU * N)
    N2 = float(N) * N
    act = np.arange(NU); apos = np.arange(NU); nact = 0
    for u in range(NU):
        if npres[u] > 1:
            nact = set_active(u, True, act, apos, nact)
    mi[MI_NEUTRAL] = check_neutral(A, C1, C2, ST, P)
    if mi[MI_NEUTRAL] == 0:
        full_F(A, C1, C2, ST, P)
    b = 0.0
    g = 0
    nextchk = UN
    total = float(Hgen) * UN
    ix = 0
    nevc = 0
    status = 1
    tg = 1e300
    if nu > 0.0:
        tg = -math.log(1.0 - np.random.random()) * UN / nu
    now0 = abs_g0
    mf[MF_LASTTOUCH] = abs_g0
    mi[MI_DIRTY] = 1
    touch(A, C1, C2, ST, P, N, abs_g0, cev, STATF)
    while True:
        pa = nact / NU
        if pa <= 0.0:
            G = total + 1.0
        elif pa >= 1.0:
            G = 0.0
        else:
            uu = np.random.random()
            G = float(int(np.log(1.0 - uu) / np.log(1.0 - pa)))
        tx = 1e300
        if ix < nx:
            tx = X[ix, 0] * UN
        be = tx if tx < tg else tg
        if be < 1e299:
            doit = False
            if nact == 0:
                doit = True
                if be > b:
                    b = float(int(be))
                    g = int(b // UN)
                    nextchk = float((g + 1) * UN)
                if g >= Hgen:
                    break
            elif be <= min(b + G + 1.0, nextchk):
                doit = True
                if be > b:
                    b = float(int(be))
            if doit:
                touch(A, C1, C2, ST, P, N, now0 + b / UN, cev, STATF)
                if tx <= tg and ix < nx:
                    kind = int(X[ix, 1])
                    if kind == 0:
                        s = np.random.randint(3)
                        y = np.searchsorted(cum[s], np.random.random())
                        r = np.random.randint(N); acc = 0; victim = pres[s, 0]
                        for t in range(npres[s]):
                            k = pres[s, t]; acc += cnt[s, k]
                            if r < acc:
                                victim = k; break
                        if y >= cum.shape[1]:
                            y = cum.shape[1] - 1
                        ekey = np.zeros(CW + 1, np.int64)
                        child = get_or_make(ST, s, y, 0, ekey, ekey, ekey)
                        if child >= 0 and child != victim:
                            nact = replace1(A, C1, C2, ST, P, act, apos, nact, s, child, victim)
                    else:
                        s = int(X[ix, 2]); prog = int(X[ix, 3]); nent = int(X[ix, 4])
                        ekey = np.zeros(CW + 1, np.int64); efil = np.zeros(CW + 1, np.int64); ebun = np.zeros(CW + 1, np.int64)
                        for e in range(nent):
                            ekey[e] = int(X[ix, 5 + 3 * e]); efil[e] = int(X[ix, 6 + 3 * e]); ebun[e] = int(X[ix, 7 + 3 * e])
                        r = np.random.randint(N); acc = 0; victim = pres[s, 0]
                        for t in range(npres[s]):
                            k = pres[s, t]; acc += cnt[s, k]
                            if r < acc:
                                victim = k; break
                        child = get_or_make(ST, s, prog, nent, ekey, efil, ebun)
                        STAT[ST_MIG] += 1
                        mf[MF_LASTMIG] = now0 + b / UN
                        if child < 0:
                            STAT[ST_MIGFAIL] += 1
                        elif child != victim:
                            nact = replace1(A, C1, C2, ST, P, act, apos, nact, s, child, victim)
                    ix += 1
                else:
                    copied = False
                    if P[P_COPY] > 0.0:
                        copied = np.random.random() < P[P_COPY]
                    nact = genesis_attempt(A, C1, C2, ST, P, act, apos, nact, N, STAT, trk, now0 + b / UN, copied)
                    tg = b + (-math.log(1.0 - np.random.random()) * UN / nu)
                touch(A, C1, C2, ST, P, N, now0 + b / UN, cev, STATF)
                continue
        elif nact == 0:
            status = 0
            break
        if b + G >= nextchk:
            b = nextchk
            g += 1
            if g >= Hgen:
                break
            nextchk = float((g + 1) * UN)
            touch(A, C1, C2, ST, P, N, now0 + b / UN, cev, STATF)
            if mi[MI_NTRACK] > 0 and (g % 4 == 0):
                nevc = track_update(ST, trk, now0 + b / UN, N, ev, nevc)
            continue
        b = b + G + 1.0
        if np.random.random() * pa * NU < nact:
            u = act[np.random.randint(nact)]
        else:
            u = act[nact + np.random.randint(NU - nact)]
        s = u
        child = pick_parent(ST, s, N2, w, mi[MI_NEUTRAL] == 1)
        r = np.random.randint(N); acc = 0; victim = pres[s, 0]
        for t in range(npres[s]):
            k = pres[s, t]; acc += cnt[s, k]
            if r < acc:
                victim = k; break
        if victim == child:
            continue
        nact = replace1(A, C1, C2, ST, P, act, apos, nact, s, child, victim)
    tend = now0 + min(b, total) / UN
    if status == 0:
        tend = now0 + float(Hgen)
    touch(A, C1, C2, ST, P, N, tend, cev, STATF)
    if mi[MI_NTRACK] > 0:
        nevc = track_update(ST, trk, tend, N, ev, nevc)
    nevs[0] = nevc
    return status, g


# ====================================================================== Python layer
def make_P(N=N0, w=W, nu=0.0, acc=ACC_R, exe=EXE_PROG, hook=HOOK_NONE, copy=0.0, bcast=0, filt=1, cap=8):
    P = np.zeros(16)
    P[P_N] = N; P[P_W] = w; P[P_NU] = nu; P[P_ACC] = acc; P[P_EXE] = exe; P[P_HOOK] = hook; P[P_COPY] = copy
    P[P_BCAST] = bcast; P[P_FILT] = filt; P[P_CAP] = cap
    return P


class Island:
    """one island: the numba state tuple plus the tracked-bundle table."""
    __slots__ = ('ST', 'trk')

    def __init__(self, ST, trk=None):
        self.ST = ST
        self.trk = new_trk() if trk is None else trk

    def counts_by_program(self, K):
        cnt, tprog, tn, tkey, tfil, tbun, pres, npres = self.ST[:8]
        out = np.zeros((3, K), np.int64)
        for s in range(3):
            for i in range(npres[s]):
                t = pres[s, i]
                out[s, tprog[s, t]] += cnt[s, t]
        return out

    def types(self):
        """list per slot of (program, count, entries[(key, fill, bun)])"""
        cnt, tprog, tn, tkey, tfil, tbun, pres, npres = self.ST[:8]
        out = []
        for s in range(3):
            row = []
            for i in range(npres[s]):
                t = pres[s, i]
                row.append((int(tprog[s, t]), int(cnt[s, t]),
                            [(int(tkey[s, t, e]), int(tfil[s, t, e]), int(tbun[s, t, e])) for e in range(int(tn[s, t]))]))
            out.append(row)
        return out

    def copy(self):
        return Island(tuple(a.copy() for a in self.ST), self.trk.copy())


def renumber_serials(ST, limit=1 << 20):
    mi = ST[11]
    if mi[MI_NEXTSER] < limit:
        return
    ser = ST[9]; pres = ST[6]; npres = ST[7]
    n = 0
    for s in range(3):
        for i in range(npres[s]):
            ser[s, pres[s, i]] = n; n += 1
    mi[MI_NEXTSER] = n


class Runner:
    """binds an arm, a parameter vector and the caches; runs islands."""

    def __init__(self, arm, P):
        self.arm = arm; self.P = P
        self.A = arm.A()
        self.stat = np.zeros(ST_LEN, np.int64)
        self.statf = np.zeros(STF_LEN)
        self.ev = np.zeros((4096, EV_W))
        self.nevs = np.zeros(1, np.int64)
        self.events = []        # tracked-bundle records
        self.cevents = []       # settled-class changes

    def xrow(self, t, kind, slot=0, prog=0, entries=()):
        row = np.zeros(5 + 3 * CW)
        row[0] = t; row[1] = kind; row[2] = slot; row[3] = prog; row[4] = len(entries)
        for e, (k, f, b) in enumerate(entries):
            row[5 + 3 * e] = k; row[6 + 3 * e] = f; row[7 + 3 * e] = b
        return row

    def run(self, isl, H, seed, abs_g0, xrows=(), cum=None, island_id=-1):
        ST = isl.ST
        renumber_serials(ST)
        self.arm.clear_c2()
        self.arm.maybe_flush_c1()
        nx = len(xrows)
        X = np.array(xrows) if nx else np.zeros((1, 5 + 3 * CW))
        cev = np.zeros((64, CEV_W))
        self.nevs[0] = 0
        c = self.arm.cum if cum is None else cum
        status, g = advance(self.A, self.arm.c1, self.arm.c2, ST, self.P, X, nx, int(H), int(seed) % (2 ** 31), c, self.stat,
                            self.statf, isl.trk, self.ev, cev, self.nevs, float(abs_g0))
        nce = int(cev[0, 0])
        for i in range(nce):
            self.cevents.append((island_id,) + tuple(cev[1 + i]))
        for i in range(int(self.nevs[0])):
            self.events.append((island_id,) + tuple(self.ev[i]))
        return int(status), int(g)

    def init_island(self, counts, abs_g0=0.0):
        ST = init_state_from_counts(counts)
        isl = Island(ST)
        init_class(self.A, self.arm.c1, self.arm.c2, ST, self.P, int(self.P[P_N]), float(abs_g0))
        return isl


# ---------------------------------------------------------------- Python helpers for tests, replays and the oracle
def encounter(R, isl, ts):
    """(stage-1 code, stage-2 code) of the type triple ts."""
    ST = isl.ST
    arm = R.arm
    arm.clear_c2()
    p = stage1(R.A, arm.c1, ST[1][0, ts[0]], ST[1][1, ts[1]], ST[1][2, ts[2]])
    c2 = tcode(R.A, arm.c1, arm.c2, ST, R.P, ts[0], ts[1], ts[2])
    return int(p), int(c2)


def propose_check(R, isl, ts, smask, newa):
    """(accepted, code_after, p, fills, pay_before) for the proposal newa (dict slot -> action) of coalition mask smask on
    the encounter triple of types ts, under the arm's acceptance mode."""
    ST = isl.ST; arm = R.arm
    arm.clear_c2()
    tprog = ST[1]
    p = int(stage1(R.A, arm.c1, tprog[0, ts[0]], tprog[1, ts[1]], tprog[2, ts[2]]))
    fills = np.array([lookup_fill(ST, s, ts[s], p) for s in range(3)], np.int64)
    c2 = int(tcode(R.A, arm.c1, arm.c2, ST, R.P, ts[0], ts[1], ts[2]))
    pay_before = np.array([PAY6[c2, s] for s in range(3)], np.int64)
    na = np.zeros(3, np.int64)
    for s, a in newa.items():
        na[s] = a
    stat = np.zeros(ST_LEN, np.int64)
    acc = test_proposal(R.A, ST, R.P, ts[0], ts[1], ts[2], smask, na, p, fills, pay_before, stat)
    return bool(acc), p, fills, pay_before, stat


def install_python(R, isl, ts, smask, newa, p):
    """install the accepted contract exactly as genesis does (one individual per signing slot); returns the new type ids."""
    ST = isl.ST; arm = R.arm
    arm.clear_c2()
    act = np.arange(3); apos = np.arange(3); nact = 0
    for u in range(3):
        if ST[7][u] > 1:
            nact = set_active(u, True, act, apos, nact)
    na = np.zeros(3, np.int64)
    for s, a in newa.items():
        na[s] = a
    bun = bundle_code(p, smask, na)
    stat = np.zeros(ST_LEN, np.int64)
    out = {}
    for s in range(3):
        if (smask >> s) & 1:
            nact, ok = install_one(R.A, arm.c1, arm.c2, ST, R.P, act, apos, nact, s, ts[s], p, newa[s], bun, stat)
            out[s] = ok
    return out


def inject(R, isl, s, prog, entries=(), victim=None):
    """place one individual of the given program (and entries) into slot s, replacing one individual of the slot's first type
    (or of type `victim`); returns the new type id.  For tests and for building configurations by hand."""
    ST = isl.ST; arm = R.arm
    arm.clear_c2()
    act = np.arange(3); apos = np.arange(3); nact = 0
    for u in range(3):
        if ST[7][u] > 1:
            nact = set_active(u, True, act, apos, nact)
    ekey = np.zeros(CW + 1, np.int64); efil = np.zeros(CW + 1, np.int64); ebun = np.zeros(CW + 1, np.int64)
    for e, (k, f, b) in enumerate(entries):
        ekey[e] = k; efil[e] = f; ebun[e] = b
    child = get_or_make(ST, s, prog, len(entries), ekey, efil, ebun)
    v = int(ST[6][s, 0]) if victim is None else victim
    replace1(R.A, arm.c1, arm.c2, ST, R.P, act, apos, nact, s, child, v)
    return int(child)
