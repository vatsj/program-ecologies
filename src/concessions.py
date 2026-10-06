"""Concessions: a boss grammar with probes, "pay fair to those who would strike" (specs/2026-10-06-concessions.md,
reviewed in reviews/2026-10-06-concessions-gpt-6.1-sol.md; predictions in predictions/2026-10-06-concessions.md).

The social organization game of src/union.py (boss B, workers W1, W2, fixed roles, three slot populations; wage
s in {0, 1/4, 1/2}, whack policy in {strike, none, source}; c the whack cost, L = 1).  Workers are unchanged: the
union run's quorum-arm grammar (n = 10, level 0, 452 canonical functions).  The boss grammar gains probe atoms

    BOX_L(W_j(^(s', none)) = a)      s' in {0, 1/4}, j in {1, 2}, a in {work, strike}, L in {0 (PA), 1 (PA + Con)}

"worker j's play against a quoted constant boss (s', none), the other worker being the current encounter's other
worker".  The quoted encounter ((s', none), W1, W2) contains no box about the probing boss, so it is evaluated on its
own (the same linear GL Kripke chain, world by world) and the probe at world n of the main encounter holds iff the
quoted encounter's W_j action equalled a at every world m with L <= m < n (modal semantics of a box of a sentence
whose world-by-world truth is that of the quoted encounter).  We store fv = min{m >= L : action(m) != a} (NEVER if
none); the probe holds at world n iff fv >= n.

Enforcement arms (src/union_enforcement.py): CC (committed, the union run's game) or RR (both slots' stage-2 moves
ex-post rational, per world).  The quoted encounter is evaluated under the arm's rule: the probe reads the
*executed* action (after the override in RR), ties to the committed recommendation; the recommended actions are
recorded too.

Grammars (boss atom kinds 0..3 are the union run's BOX(W_j = work/strike), level 0; probe kind 4 + 4 q + 2 (j - 1)
+ a, q = 0 for s' = 0 and q = 1 for s' = 1/4):
  P0    base atoms + the zero-wage probes (8 atoms);
  P01   base atoms + probes at 0 and 1/4 (16 atoms);
  sham  P01's grammar with every probe replaced by a literal constant (true for a = work, false for a = strike) at
        every world: same normalization and syntax multiplicity as P01, no expressivity;
  ref   P01's grammar with every function that has a probe atom removed (null mutation), the others keeping their
        P01 masses (the mass-preserved reference).
The length prior per role is as in every arm (bits = log2 a(|p|) + 2 log2 |p| + 1, canonical function mass = sum
over spellings of size <= n).  D* (two probe atoms, three outcomes) needs n = 11, where the P01 grammar has 439,209
boss functions; the dense class tensor of that language does not fit the chain, so the chain language is built by
mass-preserving substitution (spec): every constant and one-atom function, plus D* and its policy duplicates, each
class carrying the mass of all n = 11 functions with its behaviour (two-atom functions are assigned to an included
class by a behavioural fingerprint over a worker-pair sample, verified exactly on a subsample); the remaining
two-atom functions (novel policies) are null mutations, and their mass and their best invasion of the named fair
states are reported.
"""
import os, sys, json, time, math, zlib
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from abm import njit
import union as U
import union_enforcement as E
from dollar3 import Lang as _L3
from sog_lottery import _fit_full, _island_stats, _closed, _setact, _parent, _pay, _others

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
OUT = os.path.join(RUNS, 'concessions')
NEVER = 127
NB, NW = U.NB, U.NW
QW = ['0', '1/4']                      # quoted wages
ANAME = ['work', 'strike']


def probe_kind(q, j, a):
    return 4 + 4 * q + 2 * (j - 1) + a


def kind_name(k, sham=False):
    if k < 4:
        return U.BK_NAMES[k]
    pk = k - 4
    q, j, a = pk // 4, (pk // 2) % 2 + 1, pk % 2
    s = 'W%d(^(%s,none))=%s' % (j, QW[q], ANAME[a])
    return ('SHAM[%s]' % s) if sham else s


def atom_name(a, sham=False):
    L, k = a
    if sham and k >= 4:
        return 'SHAM%s(%s)=%s' % ('1' if L else '', kind_name(k)[:-len(ANAME[(k - 4) % 2]) - 1], 'T' if (k - 4) % 2 == 0 else 'F')
    return 'BOX%s(%s)' % ('1' if L else '', kind_name(k))


def boss_atoms(arm):
    base = [(0, k) for k in range(4)]
    if arm == 'P0':
        return base + [(L, probe_kind(0, j, a)) for j in (1, 2) for a in (0, 1) for L in (0, 1)]
    return base + [(L, probe_kind(q, j, a)) for q in (0, 1) for j in (1, 2) for a in (0, 1) for L in (0, 1)]


# ---------------------------------------------------------------- arrays
class BossArrays:
    """Boss function arrays: nat[b], atK[b, t], atL[b, t], tab[b, 4] (bit t = atom t true)."""

    def __init__(self, fb):
        K = len(fb)
        self.fb = fb
        self.nat = np.zeros(K, np.int64)
        self.atK = np.zeros((K, 2), np.int64); self.atL = np.zeros((K, 2), np.int64)
        self.tab = np.zeros((K, 4), np.int64)
        for b, (atoms, tab) in enumerate(fb):
            assert len(atoms) <= 2
            self.nat[b] = len(atoms)
            for t, (L, k) in enumerate(atoms):
                self.atK[b, t] = k; self.atL[b, t] = L
            self.tab[b, :len(tab)] = tab

    def arrays(self):
        return self.nat, self.atK, self.atL, self.tab


def boss_src(f, sham=False):
    atoms, tab = f
    if not atoms:
        return U.bname(tab[0])
    if len(atoms) == 1:
        return 'if(%s,%s,%s)' % (atom_name(atoms[0], sham), U.bname(tab[1]), U.bname(tab[0]))
    return 'f[%s]:%s' % (','.join(atom_name(a, sham) for a in atoms), ','.join(U.bname(v) for v in tab))


# ---------------------------------------------------------------- quoted encounters (probe traces)
@njit(cache=True)
def _cf_one(natW, atPW, atLW, tabW, TT, b0, x, y, t1, t2, rb, rw, pool, c, tie, flag, ex, rec):
    """Quoted encounter (constant boss action b0, W1 = x, W2 = y) world by world.  ex[n, i] executed and
    rec[n, i] recommended action of worker i at world n; returns the stabilization world (play constant from it)."""
    for t in range(flag.shape[1]):
        flag[0, t] = True; flag[1, t] = True
    xs = (x, y)
    val = np.zeros(2, np.int64)
    stab = -1
    for n in range(64):
        for s in range(2):
            z = xs[s]; idx = 0
            for t in range(natW[s + 1, z]):
                if flag[atLW[s + 1, z, t], atPW[s + 1, z, t]]:
                    idx |= 1 << t
            val[s] = tabW[s + 1, z, idx]
        rec[n, 0] = val[0]; rec[n, 1] = val[1]
        b2, i1, i2 = E.override(b0, val[0], val[1], t1, t2, rb, rw, pool, c, tie)
        ex[n, 0] = i1; ex[n, 1] = i2
        j = 4 * b2 + 2 * i1 + i2
        changed = False
        for s in range(2):
            z = xs[s]
            for t in range(natW[s + 1, z]):
                L = atLW[s + 1, z, t]; p = atPW[s + 1, z, t]
                if n >= L and flag[L, p] and not TT[p, j]:
                    flag[L, p] = False; changed = True
        if not changed and n >= 2:
            stab = n
            break
    for m in range(stab + 1, 64):
        ex[m, 0] = ex[stab, 0]; ex[m, 1] = ex[stab, 1]; rec[m, 0] = rec[stab, 0]; rec[m, 1] = rec[stab, 1]
    return stab


@njit(cache=True)
def cf_tables(natW, atPW, atLW, tabW, TT, KW, tagw, rb, rw, pool, c, tie):
    """FV[x, y, pk, L] (pk = 4 q + 2 (j - 1) + a): first world m >= L at which worker j's executed action in the
    quoted encounter ((q-wage, none), x, y) differs from a (NEVER if none); STAB[x, y, q] its stabilization world;
    EXS[x, y, q, i] / RECS[x, y, q, i] the stable executed / recommended action of worker i."""
    FV = np.full((KW, KW, 8, 2), NEVER, np.int8)
    STAB = np.zeros((KW, KW, 2), np.int8)
    EXS = np.zeros((KW, KW, 2, 2), np.int8); RECS = np.zeros((KW, KW, 2, 2), np.int8)
    flag = np.ones((2, TT.shape[0]), np.bool_)
    ex = np.zeros((64, 2), np.int64); rec = np.zeros((64, 2), np.int64)
    for x in range(KW):
        for y in range(KW):
            for q in range(2):
                b0 = 3 * q + 1                     # (q-wage, none)
                st = _cf_one(natW, atPW, atLW, tabW, TT, b0, x, y, tagw[x], tagw[y], rb, rw, pool, c, tie, flag, ex, rec)
                STAB[x, y, q] = st
                for i in range(2):
                    EXS[x, y, q, i] = ex[st, i]; RECS[x, y, q, i] = rec[st, i]
                    for a in range(2):
                        pk = 4 * q + 2 * i + a
                        for L in range(2):
                            fv = NEVER
                            for m in range(L, max(L, st) + 1):
                                if ex[m, i] != a:
                                    fv = m
                                    break
                            FV[x, y, pk, L] = fv
    return FV, STAB, EXS, RECS


def sham_fv(KW):
    """Sham probes: a literal constant at every world (true for a = work, false for a = strike)."""
    FV = np.full((KW, KW, 8, 2), NEVER, np.int8)
    for pk in range(8):
        if pk % 2 == 1:
            FV[:, :, pk, :] = -1               # holds at no world (fv >= n fails for every n >= 0)
    return FV


# ---------------------------------------------------------------- main encounter
@njit(cache=True)
def encounter_c(natB, atKB, atLB, tabB, natW, atPW, atLW, tabW, TT, b, x, y, flag, FV, t1, t2, rb, rw, pool, c, tie):
    """Stable implemented joint code of (boss function b, W1 = x, W2 = y); boxes read implemented play, probe atoms
    read the quoted encounters' executed play (FV)."""
    for t in range(flag.shape[1]):
        flag[0, t] = True; flag[1, t] = True
    nmin = 2
    for t in range(natB[b]):
        k = atKB[b, t]
        if k >= 4:
            fv = FV[x, y, k - 4, atLB[b, t]]
            if fv != NEVER and fv + 1 > nmin:
                nmin = fv + 1
    xs = (x, y)
    val = np.zeros(3, np.int64)
    for n in range(64):
        idx = 0
        for t in range(natB[b]):
            k = atKB[b, t]; L = atLB[b, t]
            if k < 4:
                tv = flag[L, 12 + k]
            else:
                tv = FV[x, y, k - 4, L] >= n
            if tv:
                idx |= 1 << t
        val[0] = tabB[b, idx]
        for s in range(2):
            z = xs[s]; idx = 0
            for t in range(natW[s + 1, z]):
                if flag[atLW[s + 1, z, t], atPW[s + 1, z, t]]:
                    idx |= 1 << t
            val[s + 1] = tabW[s + 1, z, idx]
        b2, i1, i2 = E.override(val[0], val[1], val[2], t1, t2, rb, rw, pool, c, tie)
        j = 4 * b2 + 2 * i1 + i2
        changed = False
        for t in range(natB[b]):
            k = atKB[b, t]
            if k < 4:
                L = atLB[b, t]; p = 12 + k
                if n >= L and flag[L, p] and not TT[p, j]:
                    flag[L, p] = False; changed = True
        for s in range(2):
            z = xs[s]
            for t in range(natW[s + 1, z]):
                L = atLW[s + 1, z, t]; p = atPW[s + 1, z, t]
                if n >= L and flag[L, p] and not TT[p, j]:
                    flag[L, p] = False; changed = True
        if not changed and n >= nmin:
            return j
    return -1


@njit(cache=True)
def tensor_c(natB, atKB, atLB, tabB, natW, atPW, atLW, tabW, TT, Bs, Xs, Ys, FV, tagw, rb, rw, pool, c, tie):
    """J[i, k, l] for boss functions Bs[i], W1 = Xs[k], W2 = Ys[l]."""
    J = np.empty((Bs.shape[0], Xs.shape[0], Ys.shape[0]), np.int8)
    flag = np.ones((2, TT.shape[0]), np.bool_)
    for i in range(Bs.shape[0]):
        for k in range(Xs.shape[0]):
            x = Xs[k]
            for l in range(Ys.shape[0]):
                y = Ys[l]
                J[i, k, l] = encounter_c(natB, atKB, atLB, tabB, natW, atPW, atLW, tabW, TT, Bs[i], x, y, flag, FV,
                                         tagw[x], tagw[y], rb, rw, pool, c, tie)
    return J


@njit(cache=True)
def pairs_c(natB, atKB, atLB, tabB, natW, atPW, atLW, tabW, TT, b0, b1, PX, PY, FV, tagw, rb, rw, pool, c, tie):
    """J[i, p] for boss functions b0..b1-1 against the worker pairs (PX[p], PY[p])."""
    J = np.empty((b1 - b0, PX.shape[0]), np.int8)
    flag = np.ones((2, TT.shape[0]), np.bool_)
    for i in range(b1 - b0):
        for p in range(PX.shape[0]):
            x = PX[p]; y = PY[p]
            J[i, p] = encounter_c(natB, atKB, atLB, tabB, natW, atPW, atLW, tabW, TT, b0 + i, x, y, flag, FV,
                                  tagw[x], tagw[y], rb, rw, pool, c, tie)
    return J


def trace_c(BA, PW, FV, b, x, y, rb=0, rw=0, pool=0, c=0.5, tie=0, K=8, tagw=None):
    """History-based world-by-world trace of the main encounter (independent of the flag evaluator): per world the
    recommended (boss, a1, a2), the implemented code, and every atom's truth."""
    tagw = PW.tag.astype(int) if tagw is None else tagw
    hist = []; out = []
    for n in range(K):
        av = []; idx = 0
        for t in range(BA.nat[b]):
            k = int(BA.atK[b, t]); L = int(BA.atL[b, t])
            if k < 4:
                tv = all(U.TT[12 + k, hist[m]] for m in range(L, n))
            else:
                tv = int(FV[x, y, k - 4, L]) >= n
            av.append(tv)
            if tv: idx |= 1 << t
        vb = int(BA.tab[b, idx])
        vw = []
        for s, z in ((1, x), (2, y)):
            idx = 0
            for t in range(PW.nat[s, z]):
                L = int(PW.atL[s, z, t]); p = int(PW.atP[s, z, t])
                if all(U.TT[p, hist[m]] for m in range(L, n)):
                    idx |= 1 << t
            vw.append(int(PW.tab[s, z, idx]))
        b2, i1, i2 = E._override_py(vb, vw[0], vw[1], int(tagw[x]), int(tagw[y]), rb, rw, pool, c, tie)
        j = 4 * b2 + 2 * i1 + i2
        hist.append(j)
        out.append(dict(n=n, rec=(vb, vw[0], vw[1]), imp=j, boss_atoms=av))
    return out


# ---------------------------------------------------------------- languages
_LANG = {}


def worker_lang():
    if 'W' not in _LANG:
        LW = U.RoleLang(10, U.worker_atoms((0,)), NW, qkinds=(U.QK,))
        fw, mw, cw, sw = LW.canon()
        P = U.Programs([((), (0,))], fw)
        _LANG['W'] = dict(fw=fw, mw=mw / mw.sum(), sw=sw, P=P)
    return _LANG['W']


def boss_grammar(arm, n=11):
    """Canonical boss functions of the grammar with raw masses normalized by the grammar's total."""
    key = ('B', arm, n)
    if key not in _LANG:
        g = 'P0' if arm == 'P0' else 'P01'
        LB = U.RoleLang(n, boss_atoms(g), NB)
        fb, mb, cb, sb = LB.canon()
        _LANG[key] = dict(fb=fb, mb=mb / mb.sum(), sb=sb, a=LB.a)
    return _LANG[key]


def named_workers():
    """Abstract worker functions of the named workers (union run grammar; wage-mask kinds: mask m -> kind m - 1)."""
    W = worker_lang()
    P = W['P']
    k0, klow, kfair = 0, 2, 3            # {0}, {0,1/4}, {1/2}
    out = {
        'scab': ((), (0,)),
        'T0 (strike iff s = 0)': (((0, k0),), (0, 1)),
        'T1 = militant (strike iff s <= 1/4)': (((0, klow),), (0, 1)),
        'always strike': ((), (1,)),
        'union': (((0, klow), (0, U.QK)), (0, 0, 0, 1)),
        'militant- (strike iff not BOX(s = 1/2))': (((0, kfair),), (1, 0)),
        'T0- (strike iff not BOX(s in {1/4,1/2}))': (((0, 5),), (1, 0)),
    }
    return {k: P.index_w[v] for k, v in out.items() if v in P.index_w}


def bfn(atoms, fn):
    """Canonical boss function from atom labels and a predicate fn(dict atom->bool) -> boss action."""
    atoms = sorted(atoms)
    tab = [fn({a: bool((i >> t) & 1) for t, a in enumerate(atoms)}) for i in range(1 << len(atoms))]
    return _L3._reduce(atoms, tab)


def dstar(j=1, L4=0, L0=0, a_hi=None, a_mid=None, a_lo=None):
    """D*_j: pay 1/2 iff provably strikes against the 1/4-boss, else 1/4 iff provably strikes against the 0-boss,
    else 0 (whack 'none')."""
    hi = probe_kind(1, j, 1); lo = probe_kind(0, j, 1)
    A, B = (L4, hi), (L0, lo)
    a_hi = U.bact(2, 1) if a_hi is None else a_hi
    a_mid = U.bact(1, 1) if a_mid is None else a_mid
    a_lo = U.bact(0, 1) if a_lo is None else a_lo
    return bfn([A, B], lambda tv: a_hi if tv[A] else (a_mid if tv[B] else a_lo))


def named_bosses(arm):
    out = {}
    for b in range(NB):
        out[U.bname(b)] = ((), (b,))
    p0 = (0, probe_kind(0, 1, 1))
    out['D0 = if(BOX(W1(^0)=strike),(1/2,none),(0,none))'] = bfn([p0], lambda tv: U.bact(2, 1) if tv[p0] else U.bact(0, 1))
    out['D0q = if(BOX(W1(^0)=strike),(1/4,none),(0,none))'] = bfn([p0], lambda tv: U.bact(1, 1) if tv[p0] else U.bact(0, 1))
    p01 = (1, probe_kind(0, 1, 1))
    out['D0[L1] = if(BOX1(W1(^0)=strike),(1/2,none),(0,none))'] = bfn([p01], lambda tv: U.bact(2, 1) if tv[p01] else U.bact(0, 1))
    if arm in ('P01', 'sham'):
        p4 = (0, probe_kind(1, 1, 1))
        out['D14 = if(BOX(W1(^1/4)=strike),(1/2,none),(0,none))'] = bfn([p4], lambda tv: U.bact(2, 1) if tv[p4] else U.bact(0, 1))
        out['D* = if(BOX(W1(^1/4)=strike),(1/2,none),if(BOX(W1(^0)=strike),(1/4,none),(0,none)))'] = dstar(1, 0, 0)
        out['D*[L1] (both probes BOX1)'] = dstar(1, 1, 1)
    cur = (0, 1)        # BOX(W1 = strike)
    out['C1 = if(BOX(W1=strike),(1/2,none),(0,none)) (current-encounter concession)'] = bfn([cur], lambda tv: U.bact(2, 1) if tv[cur] else U.bact(0, 1))
    wk = (0, 0)
    out['wage faker = if(BOX(W1=work),(1/2,none),(0,none))'] = bfn([wk], lambda tv: U.bact(2, 1) if tv[wk] else U.bact(0, 1))
    out['committed whacker (0,strike)'] = ((), (U.bact(0, 0),))
    return out


# ---------------------------------------------------------------- fingerprints (mass-preserving substitution)
@njit(cache=True)
def pairs_hash(natB, atKB, atLB, tabB, natW, atPW, atLW, tabW, TT, b0, b1, PX, PY, FV, tagw, rb, rw, pool, c, tie):
    """Two 64-bit hashes of each boss function's play row over the worker pairs (PX[p], PY[p])."""
    H = np.empty((b1 - b0, 2), np.uint64)
    flag = np.ones((2, TT.shape[0]), np.bool_)
    m1 = np.uint64(1099511628211); m2 = np.uint64(6364136223846793005)
    for i in range(b1 - b0):
        h1 = np.uint64(14695981039346656037); h2 = np.uint64(1442695040888963407)
        for p in range(PX.shape[0]):
            x = PX[p]; y = PY[p]
            j = encounter_c(natB, atKB, atLB, tabB, natW, atPW, atLW, tabW, TT, b0 + i, x, y, flag, FV,
                            tagw[x], tagw[y], rb, rw, pool, c, tie)
            v = np.uint64(j + 1)
            h1 = (h1 ^ v) * m1
            h2 = (h2 ^ (v + np.uint64(p) * np.uint64(37))) * m2 + np.uint64(1)
        H[i, 0] = h1; H[i, 1] = h2
    return H


ENF = {'CC': (0, 0), 'RR': (1, 1)}


def evaluator_key(enf, pool, c):
    # in CC without the pool the evaluator never reads c
    if not pool and enf == 'CC':
        return 'CC'
    return '%s_pool%d_c%g' % (enf, pool, c)


_CF = {}


def cf_for(enf, pool, c, sham=False):
    W = worker_lang(); P = W['P']
    rb, rw = ENF[enf]
    key = (evaluator_key(enf, pool, c), sham)
    if key not in _CF:
        FV, STAB, EXS, RECS = cf_tables(P.nat, P.atP, P.atL, P.tab, U.TT, P.KW, P.tag.astype(np.int64), rb, rw, pool, c, 0)
        if sham:
            FV = sham_fv(P.KW)
        _CF[key] = dict(FV=FV, STAB=STAB, EXS=EXS, RECS=RECS)
    return _CF[key]


def sample_pairs(seed=7, core=40, extra=1400):
    """Worker-pair sample for fingerprints: every ordered pair among `core` workers (the named ones, the heaviest,
    then random) plus `extra` random ordered pairs."""
    W = worker_lang(); KW = W['P'].KW
    rng = np.random.default_rng(seed)
    S = list(dict.fromkeys(list(named_workers().values()) + [int(v) for v in np.argsort(-W['mw'])[:20]]))
    rest = [int(x) for x in rng.permutation(KW) if x not in S]
    S = (S + rest)[:core]
    PX = [x for x in S for y in S]; PY = [y for x in S for y in S]
    PX += [int(v) for v in rng.integers(0, KW, extra)]; PY += [int(v) for v in rng.integers(0, KW, extra)]
    return np.array(PX, np.int64), np.array(PY, np.int64)


def _hash_job(args):
    g, b0, b1, enf, pool, c, sham = args
    G = boss_grammar(g)
    BA = BossArrays(G['fb'])
    W = worker_lang(); P = W['P']
    rb, rw = ENF[enf]
    CF = cf_for(enf, pool, c, sham)
    PX, PY = sample_pairs()
    return pairs_hash(*BA.arrays(), P.nat, P.atP, P.atL, P.tab, U.TT, b0, b1, PX, PY, CF['FV'], P.tag.astype(np.int64),
                      rb, rw, pool, c, 0)


def grammar_hashes(arm, enf, pool, c, procs=3):
    """Fingerprint hashes of every function of the n = 11 grammar (cached)."""
    os.makedirs(OUT, exist_ok=True)
    g = 'P0' if arm == 'P0' else 'P01'
    sham = arm == 'sham'
    f = os.path.join(OUT, 'hash_%s%s_%s.npz' % (g, '_sham' if sham else '', evaluator_key(enf, pool, c)))
    if os.path.exists(f):
        return np.load(f)['H']
    G = boss_grammar(g)
    K = len(G['fb'])
    step = 15000
    jobs = [(g, b0, min(b0 + step, K), enf, pool, c, sham) for b0 in range(0, K, step)]
    t = time.time()
    if procs > 1 and len(jobs) > 1:
        from multiprocessing import Pool
        cf_for(enf, pool, c, sham)
        with Pool(procs) as pl:
            parts = pl.map(_hash_job, jobs, chunksize=1)
    else:
        parts = [_hash_job(j) for j in jobs]
    H = np.concatenate(parts)
    np.savez(f, H=H)
    print('hashes %s %s: %d functions, %.0fs' % (arm, evaluator_key(enf, pool, c), K, time.time() - t), flush=True)
    return H


def included(arm, fb):
    """Indices of the functions included in the chain language: constants and one-atom functions (probe-free only
    for 'ref')."""
    idx = []
    for i, (atoms, tab) in enumerate(fb):
        if len(atoms) > 1:
            continue
        if arm == 'ref' and any(k >= 4 for (L, k) in atoms):
            continue
        idx.append(i)
    return idx


def dstar_family():
    return {('D*_%d L%d%d' % (j, L4, L0)): dstar(j, L4, L0) for j in (1, 2) for L4 in (0, 1) for L0 in (0, 1)}


def build_language(arm, enf='CC', pool=0, c=0.5, procs=3, verbose=True):
    """Chain language of an arm under an evaluator: exact behavioural classes of the included functions over all
    452 x 452 worker pairs; boss masses by mass-preserving substitution (fingerprints over the n = 11 grammar)."""
    os.makedirs(OUT, exist_ok=True)
    ek = evaluator_key(enf, pool, c)
    f = os.path.join(OUT, 'lang_%s_%s.npz' % (arm, ek))
    fj = os.path.join(OUT, 'lang_%s_%s.json' % (arm, ek))
    W = worker_lang(); P = W['P']
    g = 'P0' if arm == 'P0' else 'P01'
    G = boss_grammar(g)
    fb = G['fb']
    if os.path.exists(f) and os.path.exists(fj):
        z = np.load(f)
        C = {k: z[k] for k in z.files}
        for k in ('KcW', 'KcB'):
            C[k] = int(C[k])
        C['info'] = json.load(open(fj))
        C['fb'] = fb
        C['enf'], C['pool'], C['c'] = enf, pool, c
        return finish(C, arm)
    t0 = time.time()
    rb, rw = ENF[enf]
    sham = arm == 'sham'
    CF = cf_for(enf, pool, c, sham)
    inc = included(arm, fb)
    fam = {}
    if arm in ('P01', 'sham'):
        index = {fx: i for i, fx in enumerate(fb)}
        for name, fx in dstar_family().items():
            fam[name] = index[fx]
        inc = sorted(set(inc) | set(fam.values()))
    inc = np.array(inc, np.int64)
    BA = BossArrays(fb)
    KW = P.KW
    allw = np.arange(KW)
    tagw = P.tag.astype(np.int64)
    J = tensor_c(*BA.arrays(), P.nat, P.atP, P.atL, P.tab, U.TT, inc, allw, allw, CF['FV'], tagw, rb, rw, pool, c, 0)
    assert (J >= 0).all(), 'unstable encounter'
    if verbose:
        print('[%s %s] tensor %s %.0fs' % (arm, ek, J.shape, time.time() - t0), flush=True)
    kw = {}; cw = np.empty(KW, np.int64)
    for x in range(KW):
        cw[x] = kw.setdefault((bool(P.tag[x]), J[:, x, :].tobytes()), len(kw))
    kb = {}; cbi = np.empty(len(inc), np.int64)
    for i in range(len(inc)):
        cbi[i] = kb.setdefault(J[i].tobytes(), len(kb))
    KcW, KcB = len(kw), len(kb)
    H = grammar_hashes(arm, enf, pool, c, procs)
    hkey = [(int(H[i, 0]), int(H[i, 1])) for i in range(len(fb))]
    cls_of_hash = {}
    collide = 0
    for i, b in enumerate(inc):
        k = hkey[b]
        if k in cls_of_hash and cls_of_hash[k] != cbi[i]:
            collide += 1
        cls_of_hash.setdefault(k, cbi[i])
    incset = set(int(b) for b in inc)
    massB = np.zeros(KcB)
    for i, b in enumerate(inc):
        massB[cbi[i]] += G['mb'][b]
    merged = 0; merged_mass = 0.0; null_mass = 0.0; null_n = 0; probe_dropped = 0.0
    novel = defaultdict(float); novel_n = defaultdict(int); novel_rep = {}
    merged_list = []
    fam_mass = defaultdict(float)
    fam_cls = {cbi[list(inc).index(v)]: k for k, v in fam.items()}
    for b in range(len(fb)):
        if b in incset:
            continue
        atoms = fb[b][0]
        if arm == 'ref' and any(k >= 4 for (L, k) in atoms):
            probe_dropped += G['mb'][b]
            continue
        k = hkey[b]
        if k in cls_of_hash:
            cl = cls_of_hash[k]
            massB[cl] += G['mb'][b]; merged += 1; merged_mass += G['mb'][b]
            merged_list.append((b, cl))
            if cl in fam_cls:
                fam_mass[fam_cls[cl]] += G['mb'][b]
        else:
            null_mass += G['mb'][b]; null_n += 1
            novel[k] += G['mb'][b]; novel_n[k] += 1
            novel_rep.setdefault(k, b)
    rep_of_cls = {}
    for i, b in enumerate(inc):
        rep_of_cls.setdefault(int(cbi[i]), i)
    # exact verification: every merge into a D* family class, and a random subsample of the others
    rng = np.random.default_rng(11)
    famm = [(b, cl) for b, cl in merged_list if cl in fam_cls]
    oth = [(b, cl) for b, cl in merged_list if cl not in fam_cls]
    sub = famm[:400] + ([oth[i] for i in rng.choice(len(oth), min(150, len(oth)), replace=False)] if oth else [])
    bad = 0; bad_fam = 0
    if sub:
        bs = np.array([b for b, _ in sub], np.int64)
        Jv = tensor_c(*BA.arrays(), P.nat, P.atP, P.atL, P.tab, U.TT, bs, allw, allw, CF['FV'], tagw, rb, rw, pool, c, 0)
        for r, (b, cl) in enumerate(sub):
            if not np.array_equal(Jv[r], J[rep_of_cls[int(cl)]]):
                bad += 1
                if cl in fam_cls: bad_fam += 1
    massW = np.bincount(cw, weights=W['mw'], minlength=KcW)
    repW = np.full(KcW, -1, np.int64)
    for x in np.argsort(-W['mw'], kind='stable'):
        if repW[cw[x]] < 0: repW[cw[x]] = x
    repB = np.full(KcB, -1, np.int64)
    for i in np.argsort(-G['mb'][inc], kind='stable'):
        if repB[cbi[i]] < 0: repB[cbi[i]] = inc[i]
    rowB = np.array([rep_of_cls[k] for k in range(KcB)])
    Jc = np.ascontiguousarray(J[rowB][:, repW][:, :, repW])
    tagc = P.tag[repW].astype(np.int64)
    nov = sorted(novel.items(), key=lambda kv: -kv[1])
    info = dict(arm=arm, evaluator=ek, grammar=g, n=11, grammar_functions=len(fb), included_functions=int(len(inc)),
                KcB=KcB, KcW=KcW, boss_mass_included_functions=float(G['mb'][inc].sum()),
                boss_mass_merged=float(merged_mass), merged_functions=merged, boss_mass_null=float(null_mass),
                null_functions=null_n, novel_policies=len(novel),
                novel_top=[dict(mass=float(v), functions=novel_n[k], example=boss_src(fb[novel_rep[k]], sham)) for k, v in nov[:12]],
                ref_probe_mass_dropped=float(probe_dropped), hash_collisions_among_included=collide,
                merge_verified=len(sub), merge_verify_failures=bad, merge_verify_failures_dstar=bad_fam,
                dstar_family={k: dict(function_mass=float(G['mb'][v]), duplicates_mass=float(fam_mass.get(k, 0.0)))
                              for k, v in fam.items()},
                boss_mass_total=float(massB.sum()), time_s=time.time() - t0)
    C = dict(Jc=Jc, tagc=tagc, KcB=KcB, KcW=KcW, massB=massB, massW=massW, repB=repB, repW=repW, cw=cw,
             inc=inc, cbi=cbi)
    np.savez(f, **C)
    json.dump(info, open(fj, 'w'), indent=1)
    if verbose:
        print('[%s %s] classes B %d W %d; boss mass included %.4f merged %.4f null %.4f (%d novel policies); merge check %d/%d bad; %.0fs'
              % (arm, ek, KcB, KcW, info['boss_mass_included_functions'], merged_mass, null_mass, len(novel), bad, len(sub),
                 time.time() - t0), flush=True)
    C['info'] = info; C['fb'] = fb
    C['enf'], C['pool'], C['c'] = enf, pool, c
    return finish(C, arm)


def finish(C, arm):
    """Named class indices and sources."""
    W = worker_lang(); P = W['P']
    fb = C['fb']
    sham = arm == 'sham'
    fidx = {fx: i for i, fx in enumerate(fb)}
    inc_pos = {int(b): i for i, b in enumerate(C['inc'])}
    C['nmw'] = {k: int(C['cw'][v]) for k, v in named_workers().items()}
    nmb = {}
    for k, fx in named_bosses('P01' if arm in ('P01', 'sham') else 'P0').items():
        b = fidx.get(fx)
        if b is not None and b in inc_pos:
            nmb[k] = int(C['cbi'][inc_pos[b]])
    if arm in ('P01', 'sham'):
        for k, fx in dstar_family().items():
            b = fidx[fx]
            nmb.setdefault(k, int(C['cbi'][inc_pos[b]]))
    C['nmb'] = nmb
    C['srcW'] = [P.src_w(int(C['repW'][x])) for x in range(C['KcW'])]
    C['srcB'] = [boss_src(fb[int(C['repB'][b])], sham) for b in range(C['KcB'])]
    C['constB'] = np.array([len(fb[int(C['repB'][b])][0]) == 0 for b in range(C['KcB'])])
    C['constW'] = np.array([P.nat[1, int(C['repW'][x])] == 0 for x in range(C['KcW'])])
    C['arm'] = arm
    return C


# ---------------------------------------------------------------- static tables
def play_str(j):
    b, a1, a2 = j // 4, (j // 2) % 2, j % 2
    return '%s %s%s' % (U.bname(b), 'WS'[a1], 'WS'[a2])


def payoff_table(enf, pool, c):
    if enf == 'CC' and not pool:
        return U.payoff_table(c)
    return E.payoff_table_e(c, pool)[0]


def named_table(enf='CC', pool=0, c=0.5, arm='P01'):
    """Every named boss against every ordered pair of named workers (function level)."""
    W = worker_lang(); P = W['P']
    rb, rw = ENF[enf]
    CF = cf_for(enf, pool, c, arm == 'sham')
    nb = named_bosses('P01' if arm != 'P0' else 'P0')
    nw = named_workers()
    bn = list(nb); wn = list(nw)
    BA = BossArrays([nb[k] for k in bn])
    Xs = np.array([nw[k] for k in wn], np.int64)
    J = tensor_c(*BA.arrays(), P.nat, P.atP, P.atL, P.tab, U.TT, np.arange(len(bn)), Xs, Xs, CF['FV'], P.tag.astype(np.int64),
                 rb, rw, pool, c, 0)
    PAY = payoff_table(enf, pool, c)
    rows = []
    for i, b in enumerate(bn):
        for k, x in enumerate(wn):
            for l, y in enumerate(wn):
                j = int(J[i, k, l])
                rows.append(dict(boss=b, W1=x, W2=y, play=play_str(j),
                                 pay=[round(float(v), 3) for v in PAY[j, int(P.tag[Xs[k]]), int(P.tag[Xs[l]])]]))
    cf = {}
    for k, x in enumerate(wn):
        z = Xs[k]
        cf[x] = {('vs (%s,none)' % QW[q]): dict(executed=''.join('WS'[int(CF['EXS'][z, z, q, i])] for i in range(2)),
                                               recommended=''.join('WS'[int(CF['RECS'][z, z, q, i])] for i in range(2)),
                                               fv_strike_L0=int(CF['FV'][z, z, 4 * q + 1, 0]), fv_strike_L1=int(CF['FV'][z, z, 4 * q + 1, 1]))
                 for q in range(2)}
    srcs = {k: boss_src(v, arm == 'sham') for k, v in nb.items()}
    wsrc = {k: P.src_w(v) for k, v in nw.items()}
    return dict(rows=rows, quoted=cf, boss_src=srcs, worker_src=wsrc, bosses=bn, workers=wn)


def loeb_traces(enf='CC', pool=0, c=0.5):
    """World-by-world traces: the current-encounter concession C1, D0, D0q, D*, D*[L1] and the wage faker against
    the militant, T0 and militant- pairs."""
    W = worker_lang(); P = W['P']
    rb, rw = ENF[enf]
    CF = cf_for(enf, pool, c)
    nb = named_bosses('P01'); nw = named_workers()
    keys = [k for k in nb if k.startswith(('C1', 'D0 =', 'D0q', 'D* =', 'D*[L1]', 'wage faker'))]
    BA = BossArrays([nb[k] for k in keys])
    out = {}
    for i, k in enumerate(keys):
        for wn in ('T1 = militant (strike iff s <= 1/4)', 'T0 (strike iff s = 0)', 'militant- (strike iff not BOX(s = 1/2))'):
            x = nw[wn]
            tr = trace_c(BA, P, CF['FV'], i, x, x, rb, rw, pool, c, 0, K=6)
            out['%s || %s pair' % (k, wn)] = ['w%d: %s  boss atoms %s' % (w['n'], play_str(w['imp']), ''.join('T' if v else 'F' for v in w['boss_atoms']))
                                              for w in tr]
    return out


def state_moves(C, PAY, b, x, y, N=(1000, 10000), w=0.3):
    """Single-mutant moves out of the monomorphic class state (b, x, y): per slot and kind, mutant mass and
    probability per mutation event (mass/3 * rho); the top entries by probability at the largest N."""
    from union_chain import log_rho
    Jc, tg = C['Jc'], C['tagc']
    j0 = int(Jc[b, x, y]); r = PAY[j0, tg[x], tg[y]]
    kinds = ('strict', 'neutral-keep', 'neutral-change', 'deleterious')
    agg = {s: {k: dict(mass=0.0, **{('p_N%d' % n): 0.0 for n in N}) for k in kinds} for s in ('B', 'W1', 'W2')}
    top = []
    for s in range(3):
        K = C['KcB'] if s == 0 else C['KcW']
        mass = C['massB'] if s == 0 else C['massW']
        for q in range(K):
            t = [b, x, y]
            if t[s] == q or mass[q] == 0: continue
            t[s] = q
            j = int(Jc[t[0], t[1], t[2]]); u = PAY[j, tg[t[1]], tg[t[2]]]
            du = float(u[s] - r[s])
            same = j == j0 and np.allclose(u, r)
            kind = 'strict' if du > 1e-12 else ('deleterious' if du < -1e-12 else ('neutral-keep' if same else 'neutral-change'))
            sl = ('B', 'W1', 'W2')[s]
            agg[sl][kind]['mass'] += float(mass[q])
            e = dict(slot=sl, mutant=(C['srcB'][q] if s == 0 else C['srcW'][q]), mass=float(mass[q]), du=round(du, 4), kind=kind,
                     to=play_str(j))
            for n in N:
                p = float(mass[q]) / 3 * float(np.exp(log_rho(w * du, float(n))))
                agg[sl][kind]['p_N%d' % n] += p
                e['p_N%d' % n] = p
            top.append(e)
    top.sort(key=lambda e: -e['p_N%d' % N[-1]])
    return dict(state='%s | %s | %s' % (C['srcB'][b], C['srcW'][x], C['srcW'][y]), play=play_str(j0),
                pay=[round(float(v), 3) for v in r], by_slot_kind=agg, top=top[:12])


def named_states(C):
    nb, nw = C['nmb'], C['nmw']
    T0, T1, SC, ST = nw['T0 (strike iff s = 0)'], nw['T1 = militant (strike iff s <= 1/4)'], nw['scab'], nw['always strike']
    Mm = nw['militant- (strike iff not BOX(s = 1/2))']
    g = lambda pre: [v for k, v in nb.items() if k.startswith(pre)]
    out = {}
    if g('D* ='):
        out['F*: D* | T1 | T1'] = (g('D* =')[0], T1, T1)
        out['D*T0: D* | T0 | T0'] = (g('D* =')[0], T0, T0)
    if g('D*[L1]'):
        out['F*-: D*[L1] | militant- | militant-'] = (g('D*[L1]')[0], Mm, Mm)
    if g('D0 ='):
        out['F0: D0 | T1 | T1'] = (g('D0 =')[0], T1, T1)
        out['R0: D0 | T0 | T0'] = (g('D0 =')[0], T0, T0)
    if g('D0q'):
        out['Q0: D0q | T0 | T0'] = (g('D0q')[0], T0, T0)
    out['Fc: (1/2,none) | T1 | T1'] = (nb['(1/2,none)'], T1, T1)
    out['Fs: (1/2,none) | scab | scab'] = (nb['(1/2,none)'], SC, SC)
    out['Z: (0,none) | scab | scab'] = (nb['(0,none)'], SC, SC)
    out['ZS: (0,none) | strike | strike'] = (nb['(0,none)'], ST, ST)
    out['ZT1: (0,none) | T1 | T1'] = (nb['(0,none)'], T1, T1)
    return out


def fakers(C, enf, pool, c):
    """Exhaustive search over the chain language's classes.
    Worker side (accommodators exposed by context): worker classes whose self-pair quoted play certifies a strike
    against the q-wage boss (the strike probe true at the stable world at level 0 or 1) while some boss class gets
    their work at a stable wage <= q in the self-pair encounter.
    Boss side (wage fakers): boss classes paying < 1/2 for work from a worker self-pair whose quoted play strikes
    against every constant low-wage boss.  Lemma 0 reference: the militant- pair."""
    CF = cf_for(enf, pool, c, C['arm'] == 'sham')
    Jc = C['Jc'].astype(np.int64); KcB, KcW = C['KcB'], C['KcW']
    rep = C['repW']
    wage = (Jc // 4) // 3
    a1 = (Jc // 2) % 2
    res = {}
    for q in range(2):
        cert = np.array([CF['FV'][rep[x], rep[x], 4 * q + 1, 0] == NEVER or CF['FV'][rep[x], rep[x], 4 * q + 1, 1] == NEVER
                         for x in range(KcW)])
        bad = []
        for x in np.nonzero(cert)[0]:
            if ((wage[:, x, x] <= q) & (a1[:, x, x] == 0)).any():
                bad.append(int(x))
        res['certified to strike at %s, working for <= %s against some boss class' % (QW[q], QW[q])] = dict(
            certified_classes=int(cert.sum()), certified_mass=float(C['massW'][cert].sum()),
            exposed_classes=len(bad), exposed_mass=float(C['massW'][bad].sum()) if bad else 0.0,
            examples=[C['srcW'][x] for x in sorted(bad, key=lambda x: -C['massW'][x])[:6]])
    refuse = np.array([all(CF['EXS'][rep[x], rep[x], q, 0] == 1 for q in range(2)) for x in range(KcW)])
    whk = (Jc // 4) % 3
    for label, hsel in (('wage fakers (no threat: stable whack policy none)', 1), ('coercers (stable whack policy strike or source)', -1)):
        fk = np.zeros(KcB, bool); hits = defaultdict(list)
        for x in np.nonzero(refuse)[0]:
            m = (wage[:, x, x] < 2) & (a1[:, x, x] == 0) & ((whk[:, x, x] == 1) if hsel == 1 else (whk[:, x, x] != 1))
            fk |= m
            for b in np.nonzero(m)[0]:
                hits[int(b)].append(int(x))
        res[label + ': boss classes paying < 1/2 for work from a self-pair that strikes at every constant low wage'] = dict(
            refusing_worker_classes=int(refuse.sum()), refusing_worker_mass=float(C['massW'][refuse].sum()),
            faker_classes=int(fk.sum()), faker_mass=float(C['massB'][fk].sum()),
            probe_faker_classes=int(sum(1 for b in np.nonzero(fk)[0] if '(^' in C['srcB'][b])),
            probe_faker_mass=float(sum(C['massB'][b] for b in np.nonzero(fk)[0] if '(^' in C['srcB'][b])),
            heaviest=[dict(src=C['srcB'][b], mass=float(C['massB'][b]), victims=len(hits[b])) for b in sorted(hits, key=lambda b: -C['massB'][b])[:8]])
    # the militant pair specifically
    T1 = C['nmw']['T1 = militant (strike iff s <= 1/4)']
    m = (wage[:, T1, T1] < 2) & (a1[:, T1, T1] == 0) & (whk[:, T1, T1] == 1)
    res['wage fakers of the militant pair (no threat)'] = dict(classes=int(m.sum()), mass=float(C['massB'][m].sum()),
                                                               probe_mass=float(sum(C['massB'][b] for b in np.nonzero(m)[0] if '(^' in C['srcB'][b])))
    Mm = C['nmw']['militant- (strike iff not BOX(s = 1/2))']
    res['Lemma 0: boss classes getting work from the militant- pair at s < 1/2'] = int(((wage[:, Mm, Mm] < 2) & (a1[:, Mm, Mm] == 0)).sum())
    return res


# ---------------------------------------------------------------- chain
BASINS = ['fair', '1/4', 'zero wage', 'whacking']


def basin_of_summ(sm):
    """Named basins by outcome summary: fair (0), intermediate = 1/4 (1), zero wage (2), whacking (5, 6); strike
    and scab-split states (3, 4) are transient for the basin-rate calculation."""
    return {0: 0, 1: 1, 2: 2, 5: 3, 6: 3}.get(int(sm), -1)


def basin_rates(ch, lab, nb=4):
    """Effective basin-to-basin rates on the explored generator (per mutation event).  For each basin A and target B
    (B = A meaning a return to A before any other basin), k[A, B] = sum_{i in A} pi_i sum_{j not in A} q_ij h_B(j) / pi_A
    with h_B the probability, from j, of hitting B before any other basin (1 on B, 0 on the other basins, solved on the
    transient states by sparse LU on the jump chain).  Also: the residence time per visit 1 / sum_{B != A} k[A, B] and
    the next-basin probabilities."""
    import scipy.sparse as sp, scipy.sparse.linalg as spla
    n = len(ch.codes)
    src, dst, lw = ch.src, ch.dst_idx, ch.pr
    m = src != dst
    src, dst, lw = src[m], dst[m], lw[m]
    lout = np.full(n, -np.inf); np.logaddexp.at(lout, src, lw)
    pj = np.exp(lw - lout[src])                       # jump-chain probabilities
    lab = np.asarray(lab)
    T = np.nonzero(lab < 0)[0]
    locT = -np.ones(n, np.int64); locT[T] = np.arange(len(T))
    H = np.zeros((n, nb))
    for B in range(nb):
        H[lab == B, B] = 1.0
    if len(T):
        eT = (lab[src] < 0) & (lab[dst] < 0)
        PTT = sp.csr_matrix((pj[eT], (locT[src[eT]], locT[dst[eT]])), shape=(len(T), len(T)))
        M = (sp.identity(len(T), format='csc') - PTT.tocsc())
        lu = spla.splu(M)
        R = np.zeros((len(T), nb))
        eB = (lab[src] < 0) & (lab[dst] >= 0)
        np.add.at(R, (locT[src[eB]], lab[dst[eB]]), pj[eB])
        HT = lu.solve(R)
        H[T] = np.clip(HT, 0, 1)
    pi = ch.pi
    K = np.zeros((nb, nb)); piA = np.zeros(nb)
    for A in range(nb):
        piA[A] = pi[lab == A].sum()
    rate = np.exp(lw)
    eA = np.nonzero((lab[src] >= 0) & (lab[dst] != lab[src]))[0]
    contrib = (pi[src[eA]] * rate[eA])[:, None] * H[dst[eA]]
    np.add.at(K, lab[src[eA]], contrib)
    out = {}
    for A in range(nb):
        if piA[A] <= 0:
            continue
        k = K[A] / piA[A]
        esc = sum(k[B] for B in range(nb) if B != A)
        out[BASINS[A]] = dict(pi=float(piA[A]), rate_to={BASINS[B]: float(k[B]) for B in range(nb) if B != A},
                              return_rate=float(k[A]), escape_rate=float(esc),
                              residence_events=float(1 / esc) if esc > 0 else float('inf'),
                              next_basin={BASINS[B]: float(k[B] / esc) for B in range(nb) if B != A and esc > 0},
                              return_fraction=float(k[A] / (k[A] + esc)) if k[A] + esc > 0 else None)
    out['_pi_outside_basins'] = float(pi[lab < 0].sum())
    return out


def demand(CF, x, y):
    """Smallest quoted wage (0, 1/4) at which worker function x works beside y in the quoted encounter, else '1/2+'."""
    for q in range(2):
        if CF['EXS'][x, y, q, 0] == 0:
            return q
    return 2


def preservation(ch, C, CF, lab_summ, PAY, top_mass=0.99, max_states=400):
    """Preservation of demands under neutral worker substitution, for the fair states carrying `top_mass` of the
    fair mass: the neutral worker substitutes in either slot, each classified by its demand against the resident
    other worker relative to the resident it replaces (same / lower / higher), and whether, once a demand-lowering
    substitute has fixed, some boss class strictly invades."""
    pi = ch.pi
    fair = np.nonzero(lab_summ == 0)[0]
    if len(fair) == 0:
        return dict(fair_mass=0.0)
    order = fair[np.argsort(-pi[fair])]
    cum = np.cumsum(pi[order]) / pi[fair].sum()
    sel = order[:min(max_states, int(np.searchsorted(cum, top_mass)) + 1)]
    Jc, tg = C['Jc'], C['tagc']
    rep = C['repW']
    tot = dict(analysed_fair_mass=0.0, with_lowering=0.0, with_lowering_and_strict_boss=0.0, sub_mass_same=0.0, sub_mass_lower=0.0,
               sub_mass_higher=0.0)
    rows = []
    for k in sel:
        b, x, y = ch.decode(int(ch.codes[k]))
        j0 = int(Jc[b, x, y]); r = PAY[j0, tg[x], tg[y]]
        lower = []; same = 0.0; lowm = 0.0; high = 0.0; strict_after = False
        for s, (res, oth) in ((1, (x, y)), (2, (y, x))):
            dres = demand(CF, rep[res], rep[oth])
            for q in range(C['KcW']):
                if q == res or C['massW'][q] == 0: continue
                t = [b, x, y]; t[s] = q
                j = int(Jc[t[0], t[1], t[2]]); u = PAY[j, tg[t[1]], tg[t[2]]]
                if abs(u[s] - r[s]) > 1e-12: continue
                dq = demand(CF, rep[q], rep[oth])
                if dq == dres:
                    same += C['massW'][q]
                elif dq > dres:
                    high += C['massW'][q]
                else:
                    lowm += C['massW'][q]
                    # does some boss strictly profit after the substitution?
                    rb_ = PAY[j, tg[t[1]], tg[t[2]], 0]
                    jj = Jc[:, t[1], t[2]].astype(np.int64)
                    ub = PAY[jj, tg[t[1]], tg[t[2]], 0]
                    adv = (ub > rb_ + 1e-12) & (C['massB'] > 0)
                    if adv.any():
                        strict_after = True
                        if len(lower) < 3:
                            bb = int(np.argmax(np.where(adv, C['massB'], -1)))
                            lower.append(dict(slot=s, substitute=C['srcW'][q], mass=float(C['massW'][q]),
                                              then_boss=C['srcB'][bb], boss_mass=float(C['massB'][bb]), boss_gain=float(ub[bb] - rb_)))
        p = float(pi[k])
        tot['analysed_fair_mass'] += p
        tot['sub_mass_same'] += p * same; tot['sub_mass_lower'] += p * lowm; tot['sub_mass_higher'] += p * high
        if lowm > 0: tot['with_lowering'] += p
        if strict_after: tot['with_lowering_and_strict_boss'] += p
        rows.append(dict(pi=p, state='%s | %s | %s' % (C['srcB'][b], C['srcW'][x], C['srcW'][y]),
                         neutral_sub_mass=dict(same=float(same), lower=float(lowm), higher=float(high)),
                         lowering_then_strict_boss=lower))
    a = tot['analysed_fair_mass']
    for key in ('with_lowering', 'with_lowering_and_strict_boss', 'sub_mass_same', 'sub_mass_lower', 'sub_mass_higher'):
        tot[key] = tot[key] / a if a > 0 else None
    tot['fair_mass'] = float(pi[fair].sum())
    tot['states'] = rows[:15]
    return tot


def make_chain(C, enf, pool, c, N, theta=1e-9, max_states=400000, promote=1e-6, core_max=2500, verbose=False):
    from union_chain import UChain
    ch = UChain(C, c, N, w=0.3, theta=theta, max_states=max_states, core_max=core_max, promote=promote,
                massB=C['massB'], massW=C['massW'], arm=C['arm'], verbose=verbose)
    ch.max_rounds = 60
    ch.PAY = payoff_table(enf, pool, c)
    return ch


def seeds_for(ch, C):
    """Named states (every named boss with every pair of named workers) and every strict-NE triple."""
    from solver_audit import union_strict_ne
    nb = [v for v in C['nmb'].values() if C['massB'][v] > 0]; nw = [v for v in C['nmw'].values() if C['massW'][v] > 0]
    s = set(ch.code(b, x, y) for b in nb for x in nw for y in nw)
    ne = union_strict_ne(C, ch.PAY, ch.mass)
    for t in ne:
        s.add(ch.code(*t))
    return sorted(s), ne


def analyse(ch, C, enf, pool, c, N):
    from union_run import exits
    pi = ch.pi; codes = ch.codes
    n = len(codes)
    typ = ch.typ
    j = typ // 4; t1 = (typ // 2) % 2; t2 = typ % 2
    summ = np.array([U.summary(int(j[k]), int(t1[k]), int(t2[k])) for k in range(n)])
    wage = (j // 4) // 3; a1 = (j // 2) % 2; a2 = j % 2
    dec = [ch.decode(int(cd)) for cd in codes]
    out = dict(N=N, c=c, enf=enf, pool=pool, states=n, core=int(ch.is_core.sum()), rel_cut_change=float(ch.rel_cut_change),
               theta=ch.theta)
    out['summary'] = {U.SUMM[k]: float(pi[summ == k].sum()) for k in range(7)}
    out['wage_offered'] = {U.WNAME[s]: float(pi[wage == s].sum()) for s in range(3)}
    out['wage_paid_both_work'] = {U.WNAME[s]: float(pi[(wage == s) & (a1 == 0) & (a2 == 0)].sum()) for s in range(3)}
    PAY = ch.PAY
    pay = ch.pay
    out['mean_payoff'] = dict(zip(['boss', 'W1', 'W2'], (pi @ pay).tolist()))
    out['efficiency'] = float(pi @ pay.sum(1))
    full = (a1 == 0) & (a2 == 0)
    out['full_production'] = float(pi[full].sum())
    # three-role distribution threshold: eligible = positive total payoff; share = min payoff / total
    totp = pay.sum(1)
    elig = totp > 1e-12
    ms = np.where(elig, pay.min(1) / np.where(elig, totp, 1), 0)
    out['three_role'] = dict(eligible=float(pi[elig].sum()),
                             threshold=float(pi[elig & (ms >= 1 / 6 - 1e-12)].sum() / pi[elig].sum()) if pi[elig].sum() > 0 else None,
                             mean_min_share=float((pi[elig] * ms[elig]).sum() / pi[elig].sum()) if pi[elig].sum() > 0 else None)
    order = np.argsort(-pi)
    desc = lambda t: '%s | %s | %s' % (C['srcB'][t[0]], C['srcW'][t[1]], C['srcW'][t[2]])
    out['support'] = [dict(pi=float(pi[k]), state=desc(dec[k]), play=play_str(int(j[k])), summary=U.SUMM[summ[k]],
                           pay=np.round(pay[k], 3).tolist()) for k in order[:30]]
    out['support_size_99'] = int(np.searchsorted(np.cumsum(pi[order]), 0.99) + 1)
    # fair support by boss class
    fb_ = defaultdict(float); fw_ = defaultdict(float)
    for k in np.nonzero(summ == 0)[0]:
        b, x, y = dec[k]
        fb_[C['srcB'][b]] += pi[k]; fw_[C['srcW'][x]] += pi[k] / 2; fw_[C['srcW'][y]] += pi[k] / 2
    out['fair_boss_mass'] = dict(sorted(fb_.items(), key=lambda kv: -kv[1])[:12])
    out['fair_worker_mass'] = dict(sorted(fw_.items(), key=lambda kv: -kv[1])[:12])
    iq = defaultdict(float)
    for k in np.nonzero(summ == 1)[0]:
        iq[C['srcB'][dec[k][0]]] += pi[k]
    out['quarter_boss_mass'] = dict(sorted(iq.items(), key=lambda kv: -kv[1])[:10])
    # named programs present
    un = C['nmw'].get('union')
    out['union_mass_in_fair'] = float(sum(pi[k] for k in np.nonzero(summ == 0)[0] if un in dec[k][1:])) / max(float(pi[summ == 0].sum()), 1e-300)
    pres = {}
    for nm_, v in C['nmw'].items():
        pres[nm_] = float(sum(pi[k] for k in range(n) if v in dec[k][1:]))
    out['named_worker_presence'] = pres
    pb = {}
    for nm_, v in C['nmb'].items():
        pb[nm_] = float(sum(pi[k] for k in range(n) if dec[k][0] == v))
    out['named_boss_presence'] = pb
    probeB = np.array(['W1(^' in s or 'W2(^' in s for s in C['srcB']])
    out['mass_probe_boss'] = float(sum(pi[k] for k in range(n) if probeB[dec[k][0]]))
    # currents and dwell among summaries
    i_ = ch.src; jd = ch.dst_idx; f = np.exp(ch.lpi[i_] + ch.pr)
    Jcur = {}
    for A in range(7):
        for B in range(7):
            if A != B:
                v = float(f[(summ[i_] == A) & (summ[jd] == B)].sum())
                if v > 0: Jcur[U.SUMM[A] + '>' + U.SUMM[B]] = v
    out['currents'] = Jcur
    dwell = {}
    for A in range(7):
        pa = float(pi[summ == A].sum())
        oa = sum(v for kk, v in Jcur.items() if kk.startswith(U.SUMM[A] + '>'))
        dwell[U.SUMM[A]] = pa / oa if oa > 0 else None
    out['dwell_events'] = dwell
    # transitions out of the top states
    trans = []
    for k in order[:10]:
        ex, tot = exits(ch, int(codes[k]), top=6)
        trans.append(dict(state=desc(dec[k]), pi=float(pi[k]), summary=U.SUMM[summ[k]], exit_by_kind=tot,
                          top=[dict(p=e['prob'], kind=e['kind'], slot=['B', 'W1', 'W2'][e['slot']], du=e['du'],
                                    mutant=(C['srcB'][e['cls']] if e['slot'] == 0 else C['srcW'][e['cls']]), to=e['summ_to']) for e in ex]))
    out['transitions'] = trans
    # exits of the fair summary by kind and slot
    ek = defaultdict(float)
    PAYc = PAY
    fair_idx = np.nonzero(summ == 0)[0]
    pf = float(pi[fair_idx].sum())
    for k in fair_idx[np.argsort(-pi[fair_idx])][:200]:
        ex, tot = exits(ch, int(codes[k]), top=10 ** 6)
        for e in ex:
            if e['summ_to'] != 'fair':
                ek['%s %s' % (['B', 'W1', 'W2'][e['slot']], e['kind'])] += pi[k] * e['prob']
    out['fair_exit_by_slot_kind'] = {kk: v / pf for kk, v in sorted(ek.items(), key=lambda kv: -kv[1])} if pf > 0 else {}
    # basin rates and preservation of demands
    lab = np.array([basin_of_summ(s) for s in summ])
    out['basin_rates'] = basin_rates(ch, lab)
    CF = cf_for(enf, pool, c, C['arm'] == 'sham')
    out['preservation'] = preservation(ch, C, CF, summ, PAY)
    return out


def faker_mask(C, enf, pool, c):
    """Boss classes that pay < 1/2, with whack policy none, for work from a worker self-pair that strikes against
    every constant low-wage boss (the no-threat wage fakers of `fakers`)."""
    CF = cf_for(enf, pool, c, C['arm'] == 'sham')
    Jc = C['Jc'].astype(np.int64); rep = C['repW']
    refuse = [x for x in range(C['KcW']) if all(CF['EXS'][rep[x], rep[x], q, 0] == 1 for q in range(2))]
    fk = np.zeros(C['KcB'], bool)
    for x in refuse:
        j = Jc[:, x, x]
        fk |= ((j // 4) // 3 < 2) & ((j // 2) % 2 == 0) & ((j // 4) % 3 == 1)
    return fk


def run_cell(arm, enf='CC', pool=0, c=0.5, N=1000, theta=1e-9, tag='', save=True):
    t = time.time()
    C = build_language(arm, enf, pool, c, procs=3)
    if 'nofaker' in tag:
        C = dict(C)
        fk = faker_mask(C, enf, pool, c)
        C['massB'] = np.where(fk, 0.0, C['massB'])
        print('nofaker: %d classes, mass %.4f set to null' % (fk.sum(), float(build_language(arm, enf, pool, c)['massB'][fk].sum())), flush=True)
    ch = make_chain(C, enf, pool, c, N, theta=theta, verbose=True)
    seeds, ne = seeds_for(ch, C)
    print('[%s %s pool%d c%g N%g] %d seeds (%d strict NE)' % (arm, enf, pool, c, N, len(seeds), len(ne)), flush=True)
    ch.explore_hybrid(seeds)
    tex = time.time() - t
    out = analyse(ch, C, enf, pool, c, N)
    out['arm'] = arm; out['strict_ne'] = len(ne)
    out['strict_ne_states'] = ['%s | %s | %s' % (C['srcB'][b], C['srcW'][x], C['srcW'][y]) for (b, x, y) in ne[:20]]
    out['language'] = {k: v for k, v in C['info'].items()}
    # independent solver check on the explored generator when small enough
    if len(ch.codes) <= 6000:
        from solver_audit import solve_edges_log
        lpi2, info = solve_edges_log(len(ch.codes), ch.src, ch.dst_idx, ch.pr)
        pi2 = np.exp(lpi2)
        out['solver_check'] = dict(info=info, tv=float(0.5 * np.abs(pi2 - ch.pi).sum()))
    out['explore_s'] = tex; out['time_s'] = time.time() - t
    if save:
        os.makedirs(OUT, exist_ok=True)
        name = '%s_%s_c%g_N%d%s' % (arm, evaluator_key(enf, pool, c) if (enf != 'CC' or pool) else 'CC', c, N, tag)
        json.dump(out, open(os.path.join(OUT, 'chain_%s.json' % name), 'w'), indent=1, default=float)
        np.savez_compressed(os.path.join(OUT, 'chain_%s.npz' % name), codes=ch.codes, lpi=ch.lpi, src=ch.src, dst=ch.dst_idx, pr=ch.pr)
    return out, ch, C


class _Saved:
    """A solved chain reloaded from runs/concessions/chain_<name>.npz (codes, log pi, edges)."""

    def __init__(self, name, C):
        z = np.load(os.path.join(OUT, 'chain_%s.npz' % name))
        self.codes, self.lpi = z['codes'], z['lpi']
        self.pi = np.exp(self.lpi)
        self.src, self.dst_idx, self.pr = z['src'], z['dst'], z['pr']
        self.KcW = C['KcW']

    def decode(self, code):
        K = self.KcW
        return code // (K * K), (code // K) % K, code % K


def reanalyse_preservation(name, arm, enf, pool, c):
    """Recompute the preservation-of-demands statistic of a saved cell (all fair states up to 0.99 of fair mass)."""
    C = build_language(arm, enf, pool, c)
    ch = _Saved(name, C)
    PAY = payoff_table(enf, pool, c)
    summ = np.empty(len(ch.codes), np.int64)
    for k, cd in enumerate(ch.codes):
        b, x, y = ch.decode(int(cd))
        summ[k] = U.summary(int(C['Jc'][b, x, y]), int(C['tagc'][x]), int(C['tagc'][y]))
    CF = cf_for(enf, pool, c, arm == 'sham')
    fn = os.path.join(OUT, 'chain_%s.json' % name)
    d = json.load(open(fn))
    d['preservation'] = preservation(ch, C, CF, summ, PAY, max_states=2000)
    json.dump(d, open(fn, 'w'), indent=1, default=float)
    return d['preservation']


def _cell_main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('arm'); ap.add_argument('--enf', default='CC'); ap.add_argument('--pool', type=int, default=0)
    ap.add_argument('--c', type=float, default=0.5); ap.add_argument('--N', type=float, default=1000)
    ap.add_argument('--theta', type=float, default=1e-9); ap.add_argument('--tag', default='')
    a = ap.parse_args(argv)
    out, ch, C = run_cell(a.arm, a.enf, a.pool, a.c, a.N, a.theta, a.tag)
    print(json.dumps({k: out[k] for k in ('arm', 'enf', 'pool', 'c', 'N', 'states', 'rel_cut_change', 'summary', 'wage_paid_both_work',
                                          'efficiency', 'mean_payoff', 'three_role', 'time_s')}, indent=1, default=float), flush=True)


def excluded_audit(C, arm, enf, pool, c, states):
    """Mass-preserving substitution audit: every function of the n = 11 grammar (included or not) against the named
    states' worker pairs; for each state the boss-slot advantage of the best excluded (null) function, the excluded
    mass with a strict advantage, and the same for the included classes."""
    W = worker_lang(); P = W['P']
    g = 'P0' if arm == 'P0' else 'P01'
    G = boss_grammar(g)
    fb = G['fb']
    BA = BossArrays(fb)
    rb, rw = ENF[enf]
    CF = cf_for(enf, pool, c, arm == 'sham')
    PAY = payoff_table(enf, pool, c)
    incset = np.zeros(len(fb), bool); incset[C['inc']] = True
    H = grammar_hashes(arm, enf, pool, c)
    hk = {(int(H[b, 0]), int(H[b, 1])) for b in C['inc']}
    merged = np.array([(int(H[b, 0]), int(H[b, 1])) in hk for b in range(len(fb))]) & ~incset
    if arm == 'ref':
        probe = np.array([any(k >= 4 for (L, k) in f[0]) for f in fb])
    else:
        probe = np.zeros(len(fb), bool)
    null = ~incset & ~merged & ~probe
    out = {}
    for name, (b, x, y) in states.items():
        xr, yr = C['repW'][x], C['repW'][y]
        Jrow = pairs_c(*BA.arrays(), P.nat, P.atP, P.atL, P.tab, U.TT, 0, len(fb), np.array([xr]), np.array([yr]), CF['FV'],
                       P.tag.astype(np.int64), rb, rw, pool, c, 0)[:, 0].astype(np.int64)
        ub = PAY[Jrow, int(P.tag[xr]), int(P.tag[yr]), 0]
        r = PAY[int(C['Jc'][b, x, y]), int(C['tagc'][x]), int(C['tagc'][y]), 0]
        adv = ub - r
        sn = null & (adv > 1e-12)
        best = int(np.argmax(np.where(null, adv, -9)))
        out[name] = dict(resident_boss_payoff=float(r), null_strict_mass=float(G['mb'][sn].sum()), null_strict_functions=int(sn.sum()),
                         best_null=dict(src=boss_src(fb[best], arm == 'sham'), gain=float(adv[best]), mass=float(G['mb'][best]),
                                        play=play_str(int(Jrow[best]))),
                         included_strict_mass=float(G['mb'][incset & (adv > 1e-12)].sum()))
    return out


# ---------------------------------------------------------------- the mutation-free lottery
@njit(cache=True)
def kern_c(Jc, tagc, PAY, T, KEYT, LB, LW, init, N, w, m, seed, checks, tsmax):
    """sog_lottery.kern (the three-slot island Moran kernel at eps = 0, exact event skipping, the verified-closed stop
    on the global support), plus fair-island tracking at every check: an island is fair when it is locally closed
    (every present class of each slot gives the same play key against every combination of the island's present
    classes of the other slots) and its play is wage 1/2 with both workers working and nobody whacked.
    Returns status, stop generation, final counts, per-check stats (nchk, I, NST), ts[g, i] = (LW[0] share, LB[0]
    share, LB[1] share, LW[1] share) for g <= tsmax, first_fair[i] (first check generation at which island i is
    fair, -1 never), fair_now[i] at the stop, nfair[ci] fair islands per check, checks done."""
    np.random.seed(seed)
    I = init.shape[0]; K = init.shape[2]
    NST = 27 + LB.shape[0] + LW.shape[0]
    counts = init.copy()
    pres = np.zeros((I, 3, K), np.int64); npres = np.zeros((I, 3), np.int64); pos = -np.ones((I, 3, K), np.int64)
    glob = np.zeros((3, K), np.int64)
    F = np.zeros((I, 3, K))
    for i in range(I):
        for s in range(3):
            for k in range(K):
                if counts[i, s, k] > 0:
                    pres[i, s, npres[i, s]] = k; pos[i, s, k] = npres[i, s]; npres[i, s] += 1
                    glob[s, k] += counts[i, s, k]
    for i in range(I):
        for s in range(3):
            for t in range(npres[i, s]):
                k = pres[i, s, t]
                F[i, s, k] = _fit_full(Jc, tagc, PAY, counts, pres, npres, i, s, k)
    NU = 3 * I
    act = np.arange(NU); apos = np.arange(NU); nact = 0
    for u in range(NU):
        if npres[u // 3, u % 3] > 1:
            nact = _setact(u, True, act, apos, nact)
    nchk = len(checks)
    stats = np.zeros((nchk, I, NST))
    ts = np.zeros((tsmax + 1, I, 4))
    nlb = LB.shape[0]
    tmp = np.zeros(NST)
    first_fair = -np.ones(I, np.int64); fair_now = np.zeros(I, np.int64); nfair = np.zeros(nchk, np.int64)
    N2 = float(N) * N
    UN = NU * N
    total = checks[nchk - 1] * UN
    mm = m if I > 1 else 0.0
    b = 0
    ci = 0
    nextchk = checks[0] * UN
    status = 4; stop_gen = checks[nchk - 1]
    for i in range(I):
        _island_stats(Jc, tagc, T, LB, LW, counts, pres, npres, i, N, tmp)
        ts[0, i, 0] = tmp[27 + nlb]; ts[0, i, 1] = tmp[27]; ts[0, i, 2] = tmp[28]; ts[0, i, 3] = tmp[27 + nlb + 1]
    cls0 = np.zeros(K, np.int64); cls1 = np.zeros(K, np.int64); cls2 = np.zeros(K, np.int64)
    while True:
        pa = (nact + (NU - nact) * mm) / NU
        if pa <= 0.0:
            G = total + 1
        elif pa >= 1.0:
            G = 0
        else:
            uu = np.random.random()
            G = int(np.log(1.0 - uu) / np.log(1.0 - pa))
        if b + G >= nextchk:
            b = nextchk
            g = checks[ci]
            nf = 0
            for i in range(I):
                _island_stats(Jc, tagc, T, LB, LW, counts, pres, npres, i, N, tmp)
                for z in range(NST):
                    stats[ci, i, z] = tmp[z]
                if g <= tsmax:
                    ts[g, i, 0] = tmp[27 + nlb]; ts[g, i, 1] = tmp[27]; ts[g, i, 2] = tmp[28]; ts[g, i, 3] = tmp[27 + nlb + 1]
                fair_now[i] = 0
                if tmp[0] > 1.0 - 1e-9:
                    if _closed(Jc, tagc, KEYT, pres[i, 0], npres[i, 0], pres[i, 1], npres[i, 1], pres[i, 2], npres[i, 2]):
                        x0 = pres[i, 1, 0]; y0 = pres[i, 2, 0]
                        if KEYT[Jc[pres[i, 0, 0], x0, y0], tagc[x0], tagc[y0]] == 2:
                            fair_now[i] = 1; nf += 1
                            if first_fair[i] < 0:
                                first_fair[i] = g
            nfair[ci] = nf
            ci += 1
            if mm > 0.0:
                n0 = 0; n1 = 0; n2 = 0
                for k in range(K):
                    if glob[0, k] > 0:
                        cls0[n0] = k; n0 += 1
                    if glob[1, k] > 0:
                        cls1[n1] = k; n1 += 1
                    if glob[2, k] > 0:
                        cls2[n2] = k; n2 += 1
                if _closed(Jc, tagc, KEYT, cls0, n0, cls1, n1, cls2, n2):
                    status = 1; stop_gen = g; break
            else:
                allc = True
                for i in range(I):
                    if not _closed(Jc, tagc, KEYT, pres[i, 0], npres[i, 0], pres[i, 1], npres[i, 1], pres[i, 2], npres[i, 2]):
                        allc = False; break
                if allc:
                    status = 5; stop_gen = g; break
            if ci >= nchk:
                break
            nextchk = checks[ci] * UN
            continue
        b = b + G + 1
        if np.random.random() * pa * NU < nact:
            u = act[np.random.randint(nact)]
            mig = mm > 0.0 and np.random.random() < mm
        else:
            u = act[nact + np.random.randint(NU - nact)]
            mig = True
        i = u // 3; s = u % 3
        src = i
        if mig:
            src = np.random.randint(I - 1)
            if src >= i: src += 1
        child = _parent(F, counts, pres, npres, src, s, N2, w)
        r = np.random.randint(N); acc = 0; victim = pres[i, s, 0]
        for t in range(npres[i, s]):
            k = pres[i, s, t]; acc += counts[i, s, k]
            if r < acc:
                victim = k; break
        if victim == child:
            continue
        counts[i, s, victim] -= 1; glob[s, victim] -= 1
        if counts[i, s, victim] == 0:
            p = pos[i, s, victim]; last = pres[i, s, npres[i, s] - 1]
            pres[i, s, p] = last; pos[i, s, last] = p; pos[i, s, victim] = -1; npres[i, s] -= 1
        new = counts[i, s, child] == 0
        if new:
            pres[i, s, npres[i, s]] = child; pos[i, s, child] = npres[i, s]; npres[i, s] += 1
        counts[i, s, child] += 1; glob[s, child] += 1
        o1, o2 = _others(s)
        for sa in (o1, o2):
            sb = o1 + o2 - sa
            for ta in range(npres[i, sa]):
                k = pres[i, sa, ta]
                v = 0.0
                for tb in range(npres[i, sb]):
                    q = pres[i, sb, tb]
                    if s < sb:
                        v += counts[i, sb, q] * (_pay(Jc, tagc, PAY, sa, k, child, q) - _pay(Jc, tagc, PAY, sa, k, victim, q))
                    else:
                        v += counts[i, sb, q] * (_pay(Jc, tagc, PAY, sa, k, q, child) - _pay(Jc, tagc, PAY, sa, k, q, victim))
                F[i, sa, k] += v
        if new:
            F[i, s, child] = _fit_full(Jc, tagc, PAY, counts, pres, npres, i, s, child)
        nact = _setact(u, npres[i, s] > 1, act, apos, nact)
    if ci < nchk:
        g_last = stop_gen
        for gg in range(g_last + 1, tsmax + 1):
            for i in range(I):
                for z in range(4):
                    ts[gg, i, z] = ts[min(g_last, tsmax), i, z]
    return status, stop_gen, counts, stats[:ci], ts, first_fair, fair_now, nfair[:ci], ci


def lottery_cell_data(arm, enf, pool=0, c=0.5):
    """Class data for the lottery: seeds iid from each slot's length prior over the chain language's classes
    (boss masses renormalized over the included classes, the null mass removed)."""
    import sog_lottery as SL
    C = build_language(arm, enf, pool, c)
    PAY, T = SL.code_tables(c, pool)
    KB, KW = C['KcB'], C['KcW']
    nm = C['nmw']
    probeB = np.array(['(^' in s for s in C['srcB']])
    # concession to the militant: pays 1/2 with both working against the militant pair
    T1 = nm['T1 = militant (strike iff s <= 1/4)']
    st, sc = nm['always strike'], nm['scab']
    # a concession: pays 1/2 to the militant pair (both working) and 0 to the scab pair
    conc = np.array([(int(C['Jc'][b, T1, T1]) // 4) // 3 == 2 and int(C['Jc'][b, T1, T1]) % 4 == 0
                     and (int(C['Jc'][b, sc, sc]) // 4) // 3 == 0 for b in range(KB)])
    sw = np.zeros(KB, bool)
    for b in range(KB):
        for x in (st, sc):
            for y in (st, sc):
                j = int(C['Jc'][b, x, y]); h = (j // 4) % 3; a1 = (j // 2) % 2; a2 = j % 2
                if h == 0 and (a1 or a2):
                    sw[b] = True
    fam = np.zeros(KB, bool)
    for k, v in C['nmb'].items():
        if k.startswith('D*'):
            fam[v] = True
    LBm = np.stack([probeB, conc, sw, fam]).astype(np.int64)
    one = lambda i: np.eye(KW, dtype=np.int64)[i]
    LWm = np.stack([one(T1), one(st), one(nm['T0 (strike iff s = 0)']), (~C['constW']).astype(np.int64), one(sc)]).astype(np.int64)
    pB = C['massB'] / C['massB'].sum(); pW = C['massW'] / C['massW'].sum()
    return C, PAY, T, LBm, LWm, pB, pW


def _lottery_job(args):
    import sog_lottery as SL
    arm, enf, pool, c, r, N, I, mN, gens = args[:9]
    swap = args[9] if len(args) > 9 else None
    C, PAY, T, LBm, LWm, pB, pW = lottery_cell_data(arm, enf, pool, c)
    if swap:
        # not preregistered: move the constant striker's prior mass onto a named wage-conditional striker
        pW = pW.copy()
        k = C['nmw'][{'militant': 'T1 = militant (strike iff s <= 1/4)', 'militant-': 'militant- (strike iff not BOX(s = 1/2))'}[swap]]
        st = C['nmw']['always strike']
        pW[k] += pW[st]; pW[st] = 0.0
    seed = (20261006 + 1009 * (zlib.crc32(('%s-%s-%d-%g%s' % (arm, enf, pool, c, ('-' + swap) if swap else '')).encode()) % 1000003) + r) % (2 ** 31)
    rng = np.random.default_rng(seed)
    init = SL.init_counts(rng, I, N, pB, pW)
    chk = SL.checks_schedule(gens)
    t0 = time.time()
    status, stop, counts, stats, ts, ff, fnow, nfair, ci = kern_c(
        np.ascontiguousarray(C['Jc']), C['tagc'].astype(np.int64), PAY, T, SL.KEYT, LBm, LWm, init, N, SL.W, mN / N,
        seed % (2 ** 31), chk, 1000)
    fin = stats[ci - 1]
    lab = [int(np.argmax(fin[i, :7])) for i in range(I)]
    maj = [[C['srcB'][int(np.argmax(counts[i, 0]))], C['srcW'][int(np.argmax(counts[i, 1]))], C['srcW'][int(np.argmax(counts[i, 2]))]]
           for i in range(I)]
    gl = chk[:ci]
    return dict(run=r, seed=int(seed), status=int(status), stop_gen=int(stop), first_fair=[int(v) for v in ff],
                fair_final=[int(v) for v in fnow], label=lab, final=fin.round(5).tolist(), majority=maj,
                nfair_ts={str(int(g)): int(nfair[k]) for k, g in enumerate(gl) if g in (10, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000) or k == ci - 1},
                ts={str(g): ts[g].round(4).tolist() for g in (0, 10, 25, 50, 100, 200, 500, 1000) if g < ts.shape[0]},
                wall=time.time() - t0)


def run_lottery(arm, enf='CC', pool=0, c=0.5, runs=40, N=100, I=16, mN=0.1, gens=100000, procs=3, swap=None):
    from multiprocessing import Pool
    lottery_cell_data(arm, enf, pool, c)
    jobs = [(arm, enf, pool, c, r, N, I, mN, gens, swap) for r in range(runs)]
    t = time.time()
    with Pool(procs) as pl:
        recs = pl.map(_lottery_job, jobs, chunksize=1)
    name = 'lottery_%s_%s%s_c%g%s' % (arm, enf, '_pool' if pool else '', c, ('_x' + swap) if swap else '')
    out = dict(cell=name, params=dict(arm=arm, enf=enf, pool=pool, c=c, runs=runs, N=N, I=I, mN=mN, gens=gens, swap=swap), runs=recs,
               wall=time.time() - t)
    json.dump(out, open(os.path.join(OUT, name + '.json'), 'w'))
    return out


def reduced_chains(enf='CC', pool=0, c=0.5, Ns=(100, 1000, 10000, 100000)):
    """Not preregistered: exact chains over named classes only (as the union run's reduced canonical chain), under a
    uniform prior over the listed programs and under their length-prior masses, for nested boss sets:
    constants | + D0 family | + D* family | + wage fakers (probe and base).  Workers: the seven named workers."""
    from union_chain import dense_chain
    C = build_language('P01', enf, pool, c)
    PAY = payoff_table(enf, pool, c)
    nb, nw = C['nmb'], C['nmw']
    consts = [nb[U.bname(b)] for b in range(NB)]
    d0 = [nb[k] for k in nb if k.startswith(('D0 =', 'D0q', 'D0[L1]'))]
    d14 = [nb[k] for k in nb if k.startswith(('D14',))]
    ds = [nb[k] for k in nb if k.startswith(('D*_',))]
    fk = [nb[k] for k in nb if k.startswith(('C1', 'wage faker'))]
    # the heaviest probe wage faker of the militant pair
    T1 = nw['T1 = militant (strike iff s <= 1/4)']
    Jc = C['Jc'].astype(np.int64)
    pf = [b for b in range(C['KcB']) if '(^' in C['srcB'][b] and (Jc[b, T1, T1] // 4) // 3 < 2 and Jc[b, T1, T1] % 4 == 0
          and (Jc[b, T1, T1] // 4) % 3 == 1]
    pf = sorted(pf, key=lambda b: -C['massB'][b])[:2]
    sets = {'constants': consts, '+D0 family (P0)': consts + d0, '+D0 family, D14': consts + d0 + d14,
            '+D0 family, D14, D* family': consts + d0 + d14 + ds, '+D* family only': consts + ds,
            '+all, and wage fakers': consts + d0 + d14 + ds + fk + pf}
    Ws = list(dict.fromkeys(nw.values()))
    out = {}
    for name, Bs in sets.items():
        Bs = list(dict.fromkeys(Bs))
        for prior in ('uniform', 'length'):
            mB = np.ones(len(Bs)) if prior == 'uniform' else C['massB'][Bs]
            mW = np.ones(len(Ws)) if prior == 'uniform' else C['massW'][Ws]
            for N in Ns:
                st, lpi, A = dense_chain(C['Jc'], C['tagc'], PAY, Bs, Ws, mB, mW, float(N), 0.3)
                pi = np.exp(lpi - lpi.max()); pi /= pi.sum()
                summ = np.zeros(7)
                for k, (b, x, y) in enumerate(st):
                    summ[U.summary(int(C['Jc'][b, x, y]), int(C['tagc'][x]), int(C['tagc'][y]))] += pi[k]
                top = [dict(pi=float(pi[k]), state='%s | %s | %s' % (C['srcB'][st[k][0]], C['srcW'][st[k][1]], C['srcW'][st[k][2]]),
                            play=play_str(int(C['Jc'][st[k]])))
                       for k in np.argsort(-pi)[:6]]
                out['%s | %s | N=%d' % (name, prior, N)] = dict(summary=dict(zip(U.SUMM, summ.tolist())), top=top, bosses=len(Bs))
    return out


def run_static(arms=('P01', 'P0', 'sham', 'ref')):
    """Static section: languages, named tables, Loeb traces, named states' moves, fakers, substitution audit."""
    res = dict(languages={}, named_states={}, fakers={}, excluded_audit={}, masses={})
    for arm in arms:
        C = build_language(arm, 'CC', 0, 0.5)
        res['languages'][arm] = C['info']
        PAY = payoff_table('CC', 0, 0.5)
        st = named_states(C)
        res['named_states'][arm] = {k: state_moves(C, PAY, *v) for k, v in st.items()}
        res['fakers'][arm] = fakers(C, 'CC', 0, 0.5)
        res['excluded_audit'][arm] = excluded_audit(C, arm, 'CC', 0, 0.5, st)
        res['masses'][arm] = dict(bosses={k: float(C['massB'][v]) for k, v in C['nmb'].items()},
                                  workers={k: float(C['massW'][v]) for k, v in C['nmw'].items()},
                                  boss_constants=float(C['massB'][C['constB']].sum()),
                                  boss_probe_classes=float(sum(C['massB'][b] for b in range(C['KcB']) if '(^' in C['srcB'][b])))
        print('static', arm, 'done', flush=True)
    res['named_table_CC'] = named_table('CC', 0, 0.5, 'P01')
    res['named_table_RR'] = named_table('RR', 0, 0.5, 'P01')
    res['loeb_traces_CC'] = loeb_traces('CC', 0, 0.5)
    res['loeb_traces_RR'] = loeb_traces('RR', 0, 0.5)
    json.dump(res, open(os.path.join(RUNS, 'concessions-static.json'), 'w'), indent=1, default=float)
    return res


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'cell':
        _cell_main(sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == 'static':
        run_static(tuple(sys.argv[2:]) if len(sys.argv) > 2 else ('P01', 'P0', 'sham', 'ref'))
    elif len(sys.argv) > 1 and sys.argv[1] == 'lang':
        for a in sys.argv[2:]:
            arm, enf, pool, c = a.split(':')
            build_language(arm, enf, int(pool), float(c), procs=int(os.environ.get('CONC_PROCS', '3')))
    elif len(sys.argv) > 1 and sys.argv[1] == 'cells':
        # arm:enf:pool:c:N[:theta[:tag]] ... run sequentially in this process
        for a in sys.argv[2:]:
            p = a.split(':')
            th = float(p[5]) if len(p) > 5 else 1e-9
            tg = p[6] if len(p) > 6 else ''
            t0 = time.time()
            out, ch, C = run_cell(p[0], p[1], int(p[2]), float(p[3]), float(p[4]), th, tg)
            print(a, 'states', out['states'], 'cut', '%.2e' % out['rel_cut_change'], {k: round(v, 4) for k, v in out['summary'].items()},
                  'eff %.3f' % out['efficiency'], '%.0fs' % (time.time() - t0), flush=True)
    elif len(sys.argv) > 1 and sys.argv[1] == 'lottery':
        for a in sys.argv[2:]:
            p = a.split(':')
            o = run_lottery(p[0], p[1], int(p[2]), float(p[3]), runs=int(p[4]) if len(p) > 4 else 40,
                            procs=int(os.environ.get('CONC_PROCS', '3')), swap=(p[5] if len(p) > 5 and p[5] else None))
            print(a, 'done %.0fs' % o['wall'], flush=True)
