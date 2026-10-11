"""The gene arm (spec specs/2026-10-11-gene-arm.md, reviewed by gpt-6.1-sol; notes notes/gene-arm.md; predictions
predictions/2026-10-11-gene-arm.md).

Parametric base strategies plus <= k special-case genes (trigger, override), the override filter (G-cred), whole-program
credibility (G-cred-whole = the RR execution rule), the declared asymmetry (G-asym), reciprocal credible genes
(G-recip, the RS's late addition), random removal, base-commitment controls; gene-stability; the SG, uniform-local and
coalition kernels; fixed-role chicken.  Semantics are frozen in notes §1.4.

SOG programs (the social organization game of src/union.py, c = 0.5, L = 1, no pool):
  worker (t, q) + genes;  boss (s, h, p) + genes.  Props: union.TT (18 rows) plus Q*(W1), Q*(W2).
Every encounter is evaluated on the linear GL chain with *all* props tracked (a box of an unused prop changing only
delays the stop; the stable play is unchanged), the per-world override of union_enforcement (CC / RC / RR), and the
probe convention of src/concessions.py (quoted encounter with a constant boss (s', none), executed play, minimum
world fv + 1).
"""
import os, sys, math, json, time, itertools
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abm import njit
import union as U
import union_enforcement as E

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'gene_arm')
NEVER = 127
C_WHACK = 0.5
W = 0.3
RULES = {'CC': (0, 0), 'RC': (1, 0), 'RR': (1, 1)}

# ------------------------------------------------------------------ props
TT2 = np.zeros((20, 36), np.bool_)
TT2[:18] = U.TT
for j in range(36):
    b, a1, a2 = j // 4, (j // 2) % 2, j % 2
    low = (b // 3) in (0, 1)
    TT2[18, j] = low and a2 == 1          # Q* owned by W1: s low and W2 strikes
    TT2[19, j] = low and a1 == 1          # Q* owned by W2
NPROP = 20

# ------------------------------------------------------------------ grammars
T_NAMES = ['0', '1/4', '1/2', 'inf']
W_BASES = [(t, q) for q in (0, 1) for t in range(4)]          # t index into T_NAMES
W_BASE_NAME = {(0, 0): 'scab', (3, 0): 'striker', (1, 0): 'T0', (2, 0): 'militant', (0, 1): 'union',
               (3, 1): 'tagged striker', (1, 1): 'T0-union', (2, 1): 'tagged militant'}
W_BASE_SIZE = {(0, 0): 1, (3, 0): 1, (1, 0): 6, (2, 0): 6, (0, 1): 6, (3, 1): 6, (1, 1): 10, (2, 1): 10}
B_BASES = [(s, h, p) for p in range(3) for s in range(3) for h in (1, 0, 2)]   # h: 0 strike, 1 none, 2 source
B_BASE_SIZE = {0: 1, 1: 6, 2: 11}
GENE_SIZE = 5

W_TRIG = ['BOX(s=0)', 'BOX(s<=1/4)', 'BOX(s=1/2)', 'BOX(h=strike)', 'BOX(h=source)', 'BOX(OTHER=work)',
          'BOX(OTHER=strike)', 'Q*']
W_OVR = ['work', 'strike']
B_TRIG = ['BOX(W1=strike)', 'BOX(W2=strike)', 'BOX(W1=work)', 'BOX(W2=work)', 'P1(0)', 'P2(0)', 'P1(1/4)', 'P2(1/4)']
B_OVR = ['wage 0', 'wage 1/4', 'wage 1/2', 'whack strike', 'whack none', 'whack source']
B_TRIG_PK = [-1, -1, -1, -1, 1, 3, 5, 7]          # probe index pk = 4 q + 2 (j - 1) + a (a = 1 strike)
B_TRIG_PROP = [13, 15, 12, 14, -1, -1, -1, -1]
NWG, NBG = len(W_TRIG) * 2, len(B_TRIG) * 6

C_TRIG = ['BOX(THEM=St)', 'BOX(THEM=Sw)']
C_OVR = ['Straight', 'Swerve']
C_BASES = [(a, b) for b in (0, 1) for a in (0, 1)]           # a: 0 Straight, 1 Swerve
C_BASE_SIZE = {(0, 0): 1, (1, 0): 1, (0, 1): 6, (1, 1): 6}
NCG = 4


def wgene(t, o):
    return 2 * t + o


def bgene(t, o):
    return 6 * t + o


def gene_lists(ng, cap):
    out = [()]
    if cap >= 1:
        out += [(g,) for g in range(ng)]
    if cap >= 2:
        out += [(g1, g2) for g1 in range(ng) for g2 in range(ng) if g1 != g2]
    return out


def wgene_name(g):
    return '(%s -> %s)' % (W_TRIG[g // 2], W_OVR[g % 2])


def bgene_name(g):
    return '(%s -> %s)' % (B_TRIG[g // 6], B_OVR[g % 6])


def cgene_name(g):
    return '(%s -> %s)' % (C_TRIG[g // 2], C_OVR[g % 2])


def bbase_name(bb):
    s, h, p = bb
    return '(%s,%s,%d)' % (U.WNAME[s], U.HNAME[h], p)


class SOG:
    """Program arrays of the SOG gene grammar at cap k (workers and bosses)."""

    def __init__(self, cap=1):
        self.cap = cap
        WL = gene_lists(NWG, cap); BL = gene_lists(NBG, cap)
        self.wprog = [(bi, gl) for bi in range(len(W_BASES)) for gl in WL]
        self.bprog = [(bi, gl) for bi in range(len(B_BASES)) for gl in BL]
        KW, KB = len(self.wprog), len(self.bprog)
        self.KW, self.KB = KW, KB
        self.wt = np.zeros(KW, np.int64); self.wq = np.zeros(KW, np.int64); self.wng = np.zeros(KW, np.int64)
        self.wtr = np.zeros((KW, 2), np.int64); self.wov = np.zeros((KW, 2), np.int64); self.wbase = np.zeros(KW, np.int64)
        self.tag = np.zeros(KW, np.int64); self.wsize = np.zeros(KW, np.int64)
        for x, (bi, gl) in enumerate(self.wprog):
            t, q = W_BASES[bi]
            self.wt[x], self.wq[x], self.wng[x], self.wbase[x] = t, q, len(gl), bi
            for i, g in enumerate(gl):
                self.wtr[x, i], self.wov[x, i] = g // 2, g % 2
            self.tag[x] = int(q == 1 or any(g // 2 == 7 for g in gl))
            self.wsize[x] = W_BASE_SIZE[(t, q)] + GENE_SIZE * len(gl)
        self.bs = np.zeros(KB, np.int64); self.bh = np.zeros(KB, np.int64); self.bp = np.zeros(KB, np.int64)
        self.bng = np.zeros(KB, np.int64); self.btr = np.zeros((KB, 2), np.int64); self.bov = np.zeros((KB, 2), np.int64)
        self.bbase = np.zeros(KB, np.int64); self.bsize = np.zeros(KB, np.int64)
        for b, (bi, gl) in enumerate(self.bprog):
            s, h, p = B_BASES[bi]
            self.bs[b], self.bh[b], self.bp[b], self.bng[b], self.bbase[b] = s, h, p, len(gl), bi
            for i, g in enumerate(gl):
                self.btr[b, i], self.bov[b, i] = g // 6, g % 6
            self.bsize[b] = B_BASE_SIZE[p] + GENE_SIZE * len(gl)
        self.windex = {v: i for i, v in enumerate(self.wprog)}
        self.bindex = {v: i for i, v in enumerate(self.bprog)}
        self.const_b = np.array([[self.bindex[(B_BASES.index((s, h, 0)), ())] for h in range(3)] for s in range(3)], np.int64)

    def warrays(self):
        return self.wt, self.wq, self.wng, self.wtr, self.wov, self.tag

    def barrays(self):
        return self.bs, self.bh, self.bp, self.bng, self.btr, self.bov

    def wname(self, x):
        bi, gl = self.wprog[x]
        return W_BASE_NAME[W_BASES[bi]] + ''.join('+' + wgene_name(g) for g in gl)

    def bname(self, b):
        bi, gl = self.bprog[b]
        return bbase_name(B_BASES[bi]) + ''.join('+' + bgene_name(g) for g in gl)

    def add_gene_w(self, x, g):
        bi, gl = self.wprog[x]
        gl2 = (gl + (g,)) if len(gl) < self.cap else (gl[:-1] + (g,))
        if len(gl2) == 2 and gl2[0] == gl2[1]:
            gl2 = gl2[:1]
        return self.windex.get((bi, gl2), -1)

    def add_gene_b(self, b, g):
        bi, gl = self.bprog[b]
        gl2 = (gl + (g,)) if len(gl) < self.cap else (gl[:-1] + (g,))
        if len(gl2) == 2 and gl2[0] == gl2[1]:
            gl2 = gl2[:1]
        return self.bindex.get((bi, gl2), -1)

    def find_w(self, base, genes=()):
        return self.windex[(W_BASES.index(base), tuple(genes))]

    def find_b(self, base, genes=()):
        return self.bindex[(B_BASES.index(base), tuple(genes))]


def length_prior(sizes):
    """bits = log2 a(|p|) + 2 log2 |p| + 1 (a(s) = number of programs of size s in the list); normalized masses."""
    sizes = np.asarray(sizes)
    a = defaultdict(int)
    for s in sizes:
        a[int(s)] += 1
    bits = np.array([math.log2(a[int(s)]) + 2 * math.log2(s) + 1 for s in sizes])
    m = 2.0 ** (-bits)
    return m / m.sum()


# ------------------------------------------------------------------ evaluator
@njit(cache=True)
def _wrec(x, slot, flag, wt, wq, wng, wtr, wov):
    """(recommended action, operative gene index or -1) of worker program x in `slot` (1 or 2)."""
    for i in range(wng[x]):
        k = wtr[x, i]
        if k == 0:
            tv = flag[0]
        elif k == 1:
            tv = flag[2]
        elif k == 2:
            tv = flag[3]
        elif k == 3:
            tv = flag[6]
        elif k == 4:
            tv = flag[9]
        elif k == 5:
            tv = flag[14] if slot == 1 else flag[12]
        elif k == 6:
            tv = flag[15] if slot == 1 else flag[13]
        else:
            tv = flag[18] if slot == 1 else flag[19]
        if tv:
            return wov[x, i], i
    t = wt[x]
    if t == 0:
        thr = False
    elif t == 1:
        thr = flag[0]
    elif t == 2:
        thr = flag[2]
    else:
        thr = True
    qq = False
    if wq[x] == 1:
        qq = flag[18] if slot == 1 else flag[19]
    return (1 if (thr or qq) else 0), -1


@njit(cache=True)
def _probe(FV, x, y, pk, n):
    return FV[x, y, pk] >= n


@njit(cache=True)
def _brec(b, x, y, n, flag, FV, bs, bh, bp, bng, btr, bov):
    """(recommended boss action index 3 s + h, operative gene index or -1)."""
    op = -1
    for i in range(bng[b]):
        k = btr[b, i]
        if k == 0:
            tv = flag[13]
        elif k == 1:
            tv = flag[15]
        elif k == 2:
            tv = flag[12]
        elif k == 3:
            tv = flag[14]
        elif k == 4:
            tv = FV[x, y, 1] >= n
        elif k == 5:
            tv = FV[x, y, 3] >= n
        elif k == 6:
            tv = FV[x, y, 5] >= n
        else:
            tv = FV[x, y, 7] >= n
        if tv:
            op = i
            break
    s = bs[b]; h = bh[b]
    if bp[b] == 1:
        if FV[x, y, 1] >= n:
            s = 2
    elif bp[b] == 2:
        if FV[x, y, 5] >= n:
            s = 2
        elif FV[x, y, 1] >= n:
            s = max(1, s)
    if op >= 0:
        o = bov[b, op]
        if o < 3:
            s = o
        else:
            h = o - 3
    return 3 * s + h, op


@njit(cache=True)
def _nmin(b, x, y, FV, bp, bng, btr):
    nm = 2
    for pk in (1, 3, 5, 7):
        used = False
        if (pk == 1 and bp[b] >= 1) or (pk == 5 and bp[b] == 2):
            used = True
        for i in range(bng[b]):
            k = btr[b, i]
            if k >= 4 and (2 * (k - 4) + 1) == pk:
                used = True
        if used:
            fv = FV[x, y, pk]
            if fv != NEVER and fv + 1 > nm:
                nm = fv + 1
    return nm


@njit(cache=True)
def encounter_g(b, x, y, FV, TT2, bs, bh, bp, bng, btr, bov, wt, wq, wng, wtr, wov, tag, rb, rw, c, flag, ops):
    """Stable implemented joint code of (boss b, W1 x, W2 y); ops[0..2] <- operative gene index per slot at the
    stable world (-1 none)."""
    for p in range(flag.shape[0]):
        flag[p] = True
    nmin = _nmin(b, x, y, FV, bp, bng, btr)
    t1 = tag[x]; t2 = tag[y]
    for n in range(64):
        vb, ob = _brec(b, x, y, n, flag, FV, bs, bh, bp, bng, btr, bov)
        v1, o1 = _wrec(x, 1, flag, wt, wq, wng, wtr, wov)
        v2, o2 = _wrec(y, 2, flag, wt, wq, wng, wtr, wov)
        b2, i1, i2 = E.override(vb, v1, v2, t1, t2, rb, rw, 0, c, 0)
        j = 4 * b2 + 2 * i1 + i2
        changed = False
        for p in range(flag.shape[0]):
            if flag[p] and not TT2[p, j]:
                flag[p] = False
                changed = True
        if not changed and n >= nmin:
            ops[0] = ob; ops[1] = o1; ops[2] = o2
            return j
    return -1


@njit(cache=True)
def quoted_tables(KW, TT2, wt, wq, wng, wtr, wov, tag, rb, rw, c):
    """FV[x, y, pk] (pk = 4 q + 2 i + a): first world at which worker i's executed action in the quoted encounter
    ((q-wage, none), x, y) differs from a (NEVER if never); QS[x, y, q, i] the stable executed action."""
    FV = np.full((KW, KW, 8), NEVER, np.int8)
    QS = np.zeros((KW, KW, 2, 2), np.int8)
    flag = np.ones(TT2.shape[0], np.bool_)
    ex = np.zeros((64, 2), np.int64)
    for x in range(KW):
        for y in range(KW):
            for q in range(2):
                b0 = 3 * q + 1
                for p in range(flag.shape[0]):
                    flag[p] = True
                st = 63
                for n in range(64):
                    v1, o1 = _wrec(x, 1, flag, wt, wq, wng, wtr, wov)
                    v2, o2 = _wrec(y, 2, flag, wt, wq, wng, wtr, wov)
                    b2, i1, i2 = E.override(b0, v1, v2, tag[x], tag[y], rb, rw, 0, c, 0)
                    ex[n, 0] = i1; ex[n, 1] = i2
                    j = 4 * b2 + 2 * i1 + i2
                    changed = False
                    for p in range(flag.shape[0]):
                        if flag[p] and not TT2[p, j]:
                            flag[p] = False
                            changed = True
                    if not changed and n >= 2:
                        st = n
                        break
                for i in range(2):
                    QS[x, y, q, i] = ex[st, i]
                    for a in range(2):
                        fv = NEVER
                        for m in range(0, st + 1):
                            if ex[m, i] != a:
                                fv = m
                                break
                        FV[x, y, 4 * q + 2 * i + a] = fv
    return FV, QS


@njit(cache=True)
def tensor_g(Bs, Xs, Ys, FV, TT2, bs, bh, bp, bng, btr, bov, wt, wq, wng, wtr, wov, tag, rb, rw, c):
    """J[i, k, l] and OPS[i, k, l] = (ob + 1) + 3 (o1 + 1) + 9 (o2 + 1) over index lists."""
    J = np.empty((Bs.shape[0], Xs.shape[0], Ys.shape[0]), np.int8)
    OPS = np.empty((Bs.shape[0], Xs.shape[0], Ys.shape[0]), np.int8)
    flag = np.ones(TT2.shape[0], np.bool_)
    ops = np.zeros(3, np.int64)
    for i in range(Bs.shape[0]):
        for k in range(Xs.shape[0]):
            for l in range(Ys.shape[0]):
                j = encounter_g(Bs[i], Xs[k], Ys[l], FV, TT2, bs, bh, bp, bng, btr, bov, wt, wq, wng, wtr, wov, tag,
                                rb, rw, c, flag, ops)
                J[i, k, l] = j
                OPS[i, k, l] = (ops[0] + 1) + 3 * (ops[1] + 1) + 9 * (ops[2] + 1)
    return J, OPS


def trace_g(G, FV, b, x, y, rule='CC', K=8):
    """Independent history-based trace (no flags): per world the recommendations, implemented code and the
    operative genes; boxes recomputed from the play history."""
    rb, rw = RULES[rule]
    hist = []; out = []
    for n in range(K):
        flag = np.array([all(TT2[p, hist[m]] for m in range(n)) for p in range(NPROP)])
        vb, ob = _brec(b, x, y, n, flag, FV, *G.barrays())
        v1, o1 = _wrec(x, 1, flag, *G.warrays()[:5])
        v2, o2 = _wrec(y, 2, flag, *G.warrays()[:5])
        b2, i1, i2 = E._override_py(vb, v1, v2, int(G.tag[x]), int(G.tag[y]), rb, rw, 0, C_WHACK, 0)
        j = 4 * b2 + 2 * i1 + i2
        hist.append(j)
        out.append(dict(n=n, rec=(int(vb), int(v1), int(v2)), imp=j, play=U.joint_name(j), ops=(ob, o1, o2)))
    return out


# ------------------------------------------------------------------ payoffs, summaries
PAY = U.payoff_table(C_WHACK)
SUMM = U.SUMM


def summ(j, t1, t2):
    return U.summary(int(j), int(t1), int(t2))


def is_nash(j, t1, t2):
    """the stable play is a pure NE of the stage game (boss (s, h), workers work/strike, tags fixed)."""
    b, a1, a2 = j // 4, (j // 2) % 2, j % 2
    u = PAY[j, t1, t2]
    for b2 in range(9):
        if PAY[4 * b2 + 2 * a1 + a2, t1, t2, 0] > u[0] + 1e-12:
            return False
    if PAY[4 * b + 2 * (1 - a1) + a2, t1, t2, 1] > u[1] + 1e-12:
        return False
    if PAY[4 * b + 2 * a1 + (1 - a2), t1, t2, 2] > u[2] + 1e-12:
        return False
    return True


FRONTIER = [np.array([2.0, 0, 0]), np.array([1.5, .25, .25]), np.array([1.0, .5, .5])]


def pareto_dominated(u):
    u = np.asarray(u)
    for f in FRONTIER:
        if (f >= u - 1e-12).all() and (f > u + 1e-12).any():
            return True
    return False


# ------------------------------------------------------------------ catalogue build (one execution rule)
def build_tables(G, rule, verbose=True):
    """J, OPS over the full catalogue at G's cap under `rule`, the quoted tables.  Cached in runs/gene_arm/."""
    os.makedirs(OUT, exist_ok=True)
    f = os.path.join(OUT, 'tables_cap%d_%s.npz' % (G.cap, rule))
    if os.path.exists(f):
        z = np.load(f)
        return dict(J=z['J'], OPS=z['OPS'], FV=z['FV'], QS=z['QS'])
    rb, rw = RULES[rule]
    t0 = time.time()
    FV, QS = quoted_tables(G.KW, TT2, *G.warrays(), rb, rw, C_WHACK)
    J, OPS = tensor_g(np.arange(G.KB), np.arange(G.KW), np.arange(G.KW), FV, TT2, *G.barrays(), *G.warrays(), rb, rw, C_WHACK)
    assert (J >= 0).all(), 'unstable encounter'
    if verbose:
        print('  tables cap %d %s: %d x %d x %d in %.0fs' % (G.cap, rule, G.KB, G.KW, G.KW, time.time() - t0), flush=True)
    np.savez(f, J=J, OPS=OPS, FV=FV, QS=QS)
    return dict(J=J, OPS=OPS, FV=FV, QS=QS)


def lump(J, tag, Bsel, Wsel, massB, massW):
    """Exact behavioural classes over the sub-catalogue (Bsel bosses, Wsel workers): workers by (tag, J[:, x, :],
    J[:, :, x]); bosses by J[b].  Returns class maps (over the selected lists), representative indices (into the
    selection), class masses and the class tensor."""
    Js = J[np.ix_(Bsel, Wsel, Wsel)]
    tg = tag[Wsel]
    kw = {}; cw = np.empty(len(Wsel), np.int64)
    for k in range(len(Wsel)):
        key = (int(tg[k]), Js[:, k, :].tobytes(), Js[:, :, k].tobytes())
        cw[k] = kw.setdefault(key, len(kw))
    kb = {}; cb = np.empty(len(Bsel), np.int64)
    for i in range(len(Bsel)):
        cb[i] = kb.setdefault(Js[i].tobytes(), len(kb))
    KcW, KcB = len(kw), len(kb)
    mW = np.bincount(cw, weights=massW, minlength=KcW); mB = np.bincount(cb, weights=massB, minlength=KcB)
    repW = np.full(KcW, -1, np.int64); repB = np.full(KcB, -1, np.int64)
    for k in np.argsort(-massW, kind='stable'):
        if repW[cw[k]] < 0: repW[cw[k]] = k
    for i in np.argsort(-massB, kind='stable'):
        if repB[cb[i]] < 0: repB[cb[i]] = i
    Jc = np.ascontiguousarray(Js[repB][:, repW][:, :, repW])
    return dict(cw=cw, cb=cb, KcW=KcW, KcB=KcB, massW=mW, massB=mB, repW=repW, repB=repB, Jc=Jc, tagc=tg[repW].astype(np.int64))


# ------------------------------------------------------------------ the override filter
def cont_br_worker(j, slot, o, t1, t2):
    """is override o (0 work, 1 strike) a continuation best reply for worker `slot` at stable play j?"""
    b, a1, a2 = j // 4, (j // 2) % 2, j % 2
    alts = []
    for a in (0, 1):
        aa = [a1, a2]; aa[slot - 1] = a
        alts.append(PAY[4 * b + 2 * aa[0] + aa[1], t1, t2, slot])
    return alts[o] >= max(alts) - 1e-12


def cont_br_boss_whack(j, o, t1, t2):
    b, a1, a2 = j // 4, (j // 2) % 2, j % 2
    si = b // 3
    alts = [PAY[4 * (3 * si + h) + 2 * a1 + a2, t1, t2, 0] for h in range(3)]
    return alts[o] >= max(alts) - 1e-12


def wage_alts(Jfull, G, x, y, h, t1, t2):
    """boss payoff at each alternative wage s'' with the workers' continuation = their play against the constant boss
    (s'', h) (the probe counterfactual)."""
    return [PAY[int(Jfull[G.const_b[s, h], x, y]), t1, t2, 0] for s in range(3)]


def _witness(msk, wmass, names):
    idx = int(np.argmax(np.where(msk, wmass, -1.0)))
    return np.unravel_index(idx, msk.shape)


def filter_genes(G, Tbl, massB_prog, massW_prog, wsel=None, bsel=None):
    """Override filter (notes §1.7) against the reference catalogue (bsel, wsel: program index arrays, default all;
    Tbl under CC).  Per gene: admitted, fired / failed counts, prior mass of firing encounters, the heaviest failing and
    passing witnesses.  Worker genes are tested in slot W1 (slot W2 is the mirror, tested in tests/)."""
    J, OPS = Tbl['J'], Tbl['OPS']
    wsel = np.arange(G.KW) if wsel is None else np.asarray(wsel)
    bsel = np.arange(G.KB) if bsel is None else np.asarray(bsel)
    tg = G.tag[wsel]
    mb = massB_prog[bsel]; mw = massW_prog[wsel]
    out = {'worker': {}, 'boss': {}}
    for g in range(NWG):
        tr, ov = g // 2, g % 2
        car = [(k, [i for i in range(G.wng[x]) if G.wtr[x, i] == tr and G.wov[x, i] == ov]) for k, x in enumerate(wsel)]
        car = [(k, p[0]) for k, p in car if p]
        rec = dict(name=wgene_name(g), fired=0, failed=0, fired_mass=0.0, failed_mass=0.0)
        if car:
            ks = np.array([k for k, _ in car]); pos = np.array([p for _, p in car])
            Js = J[np.ix_(bsel, wsel[ks], wsel)].astype(np.int64)
            o1 = (OPS[np.ix_(bsel, wsel[ks], wsel)].astype(np.int64) // 3) % 3 - 1
            fires = o1 == pos[None, :, None]
            a1 = (Js // 2) % 2; a2 = Js % 2
            T1 = np.broadcast_to(tg[ks][None, :, None], Js.shape); T2 = np.broadcast_to(tg[None, None, :], Js.shape)
            own = PAY[Js, T1, T2, 1]
            alt = PAY[4 * (Js // 4) + 2 * (1 - a1) + a2, T1, T2, 1]
            ok = own >= np.maximum(own, alt) - 1e-12
            fail = fires & ~ok
            wmass = mb[:, None, None] * mw[ks][None, :, None] * mw[None, None, :]
            rec.update(fired=int(fires.sum()), failed=int(fail.sum()), fired_mass=float(wmass[fires].sum()),
                       failed_mass=float(wmass[fail].sum()))
            for key, msk in (('witness_fail', fail), ('witness_pass', fires & ok)):
                if msk.any():
                    i, k, l = _witness(msk, wmass, None)
                    rec[key] = dict(boss=G.bname(bsel[i]), W1=G.wname(wsel[ks[k]]), W2=G.wname(wsel[l]),
                                    play=U.joint_name(int(Js[i, k, l])), u_override=float(own[i, k, l]), u_alt=float(alt[i, k, l]))
        rec['admitted'] = rec['failed'] == 0
        rec['vacuous'] = rec['fired'] == 0
        out['worker'][g] = rec
    for g in range(NBG):
        tr, ov = g // 6, g % 6
        car = [(i, [q for q in range(G.bng[b]) if G.btr[b, q] == tr and G.bov[b, q] == ov]) for i, b in enumerate(bsel)]
        car = [(i, p[0]) for i, p in car if p]
        rec = dict(name=bgene_name(g), fired=0, failed=0, fired_mass=0.0, failed_mass=0.0)
        if car:
            cs = np.array([i for i, _ in car]); pos = np.array([p for _, p in car])
            Js = J[np.ix_(bsel[cs], wsel, wsel)].astype(np.int64)
            ob = OPS[np.ix_(bsel[cs], wsel, wsel)].astype(np.int64) % 3 - 1
            fires = ob == pos[:, None, None]
            wage = (Js // 4) // 3; hh = (Js // 4) % 3; a1 = (Js // 2) % 2; a2 = Js % 2
            T1 = np.broadcast_to(tg[None, :, None], Js.shape); T2 = np.broadcast_to(tg[None, None, :], Js.shape)
            own = PAY[Js, T1, T2, 0]
            if ov >= 3:
                alts = np.stack([PAY[4 * (3 * wage + h) + 2 * a1 + a2, T1, T2, 0] for h in range(3)], -1)
            else:
                alts = np.empty(Js.shape + (3,))
                for s_ in range(3):
                    cbs = G.const_b[s_][hh]
                    alts[..., s_] = PAY[J[cbs, wsel[None, :, None], wsel[None, None, :]].astype(np.int64), T1, T2, 0]
            ok = own >= alts.max(-1) - 1e-12
            fail = fires & ~ok
            wmass = mb[cs][:, None, None] * mw[None, :, None] * mw[None, None, :]
            rec.update(fired=int(fires.sum()), failed=int(fail.sum()), fired_mass=float(wmass[fires].sum()),
                       failed_mass=float(wmass[fail].sum()))
            for key, msk in (('witness_fail', fail), ('witness_pass', fires & ok)):
                if msk.any():
                    i, k, l = _witness(msk, wmass, None)
                    rec[key] = dict(boss=G.bname(bsel[cs[i]]), W1=G.wname(wsel[k]), W2=G.wname(wsel[l]),
                                    play=U.joint_name(int(Js[i, k, l])), u_override=float(own[i, k, l]),
                                    u_alts=[float(v) for v in np.atleast_1d(alts[i, k, l])])
        rec['admitted'] = rec['failed'] == 0
        rec['vacuous'] = rec['fired'] == 0
        out['boss'][g] = rec
    return out


W_RECIP = np.array([1, 1, 1, 0, 0, 1, 1, 1], bool)        # reciprocal worker triggers (notes §1.15)
B_RECIP = np.array([1, 1, 1, 1, 0, 0, 0, 0], bool)


# ------------------------------------------------------------------ arms
def arm_spec(name, G, filt=None, rr_seed=20261011):
    """Admissible gene masks, base restrictions and execution rule of an arm.  filt: the G-cred filter output."""
    gw = np.ones(NWG, bool); gb = np.ones(NBG, bool)
    bases_b = np.ones(len(B_BASES), bool)
    rule = 'CC'
    genes_on = True
    nm = name.replace('-ctl', '')
    if nm.startswith('base-'):
        genes_on = False; rule = nm.split('-')[1]
    elif nm == 'G-all':
        pass
    elif nm == 'G-all-RC':
        rule = 'RC'
    elif nm == 'G-cred':
        gw = np.array([filt['worker'][g]['admitted'] for g in range(NWG)]); gb = np.array([filt['boss'][g]['admitted'] for g in range(NBG)])
    elif nm == 'G-recip':
        gw = np.array([filt['worker'][g]['admitted'] and W_RECIP[g // 2] for g in range(NWG)])
        gb = np.array([filt['boss'][g]['admitted'] and B_RECIP[g // 6] for g in range(NBG)])
    elif nm == 'G-cred-whole':
        rule = 'RR'
    elif nm == 'G-asym':
        gb = np.array([(g % 6) not in (3, 5) for g in range(NBG)])
    elif nm == 'random':
        ad_w = sum(filt['worker'][g]['admitted'] for g in range(NWG)); ad_b = sum(filt['boss'][g]['admitted'] for g in range(NBG))
        rng = np.random.default_rng(rr_seed)
        gw = np.zeros(NWG, bool); gw[rng.choice(NWG, ad_w, replace=False)] = True
        gb = np.zeros(NBG, bool); gb[rng.choice(NBG, ad_b, replace=False)] = True
    else:
        raise ValueError(name)
    if name.endswith('-ctl'):
        bases_b = np.array([B_BASES[i][1] == 1 for i in range(len(B_BASES))])
    if not genes_on:
        gw[:] = False; gb[:] = False
    wsel = np.array([x for x, (bi, gl) in enumerate(G.wprog) if all(gw[g] for g in gl)], np.int64)
    bsel = np.array([b for b, (bi, gl) in enumerate(G.bprog) if bases_b[bi] and all(gb[g] for g in gl)], np.int64)
    return dict(name=name, rule=rule, gw=gw, gb=gb, wsel=wsel, bsel=bsel, bases_b=bases_b)


def priors(G):
    return dict(length=(length_prior(G.bsize), length_prior(G.wsize)),
                uniform=(np.ones(G.KB) / G.KB, np.ones(G.KW) / G.KW))


def base_priors(G):
    """base-only catalogues: the length prior of the base sizes and uniform over bases."""
    bs = np.array([B_BASE_SIZE[B_BASES[G.bprog[b][0]][2]] if not G.bprog[b][1] else 0 for b in range(G.KB)])
    return bs


# ------------------------------------------------------------------ gene-stability (program level)
def gene_moves(G, Tbl, arm, b, x, y):
    """every admissible single-gene mutant of each slot of (b, x, y) with its payoff change (mutant-program
    re-evaluation; Tbl under the arm's rule) and the other slots' changes."""
    J = Tbl['J']
    j0 = int(J[b, x, y]); t = (int(G.tag[x]), int(G.tag[y]))
    u0 = PAY[j0, t[0], t[1]]
    res = []
    if '_bset' not in arm:
        arm['_bset'] = set(arm['bsel'].tolist()); arm['_wset'] = set(arm['wsel'].tolist())
    bset = arm['_bset']; wset = arm['_wset']
    for g in range(NBG):
        if not arm['gb'][g]: continue
        m = G.add_gene_b(b, g)
        if m < 0 or m not in bset or m == b: continue
        j = int(J[m, x, y]); u = PAY[j, t[0], t[1]]
        res.append(dict(slot='B', gene=bgene_name(g), mutant=m, du=float(u[0] - u0[0]), u=u.tolist(), play=U.joint_name(j)))
    for slot, (xx, yy) in ((1, (x, y)), (2, (x, y))):
        r = x if slot == 1 else y
        for g in range(NWG):
            if not arm['gw'][g]: continue
            m = G.add_gene_w(r, g)
            if m < 0 or m not in wset or m == r: continue
            x2, y2 = (m, y) if slot == 1 else (x, m)
            j = int(J[b, x2, y2]); t2 = (int(G.tag[x2]), int(G.tag[y2])); u = PAY[j, t2[0], t2[1]]
            res.append(dict(slot='W%d' % slot, gene=wgene_name(g), mutant=m, du=float(u[slot] - u0[slot]), u=u.tolist(), play=U.joint_name(j)))
    return j0, u0, res


def gene_stable(G, Tbl, arm, b, x, y, weak=False):
    j0, u0, mv = gene_moves(G, Tbl, arm, b, x, y)
    for m in mv:
        if m['du'] > 1e-12:
            return False, m
        if weak and m['du'] >= -1e-12 and any(m['u'][k] > u0[k] + 1e-12 for k in range(3)):
            return False, m
    return True, None


@njit(cache=True)
def _scan_gene_stable(J, PAY, tag, bsel, wsel, inB, inW, ADDB, ADDW, gb, gw, weak, out_stab):
    """out_stab[i, k, l] = 1 iff the program triple (bsel[i], wsel[k], wsel[l]) is (weakly) gene-stable."""
    for i in range(bsel.shape[0]):
        b = bsel[i]
        for k in range(wsel.shape[0]):
            x = wsel[k]
            for l in range(wsel.shape[0]):
                y = wsel[l]
                j0 = J[b, x, y]
                u0 = PAY[j0, tag[x], tag[y]]
                st = 1
                for g in range(gb.shape[0]):
                    if not gb[g]: continue
                    m = ADDB[b, g]
                    if m < 0 or not inB[m] or m == b: continue
                    u = PAY[J[m, x, y], tag[x], tag[y]]
                    if u[0] > u0[0] + 1e-12 or (weak and u[0] >= u0[0] - 1e-12 and (u[1] > u0[1] + 1e-12 or u[2] > u0[2] + 1e-12)):
                        st = 0; break
                if st:
                    for slot in (1, 2):
                        r = x if slot == 1 else y
                        for g in range(gw.shape[0]):
                            if not gw[g]: continue
                            m = ADDW[r, g]
                            if m < 0 or not inW[m] or m == r: continue
                            if slot == 1:
                                u = PAY[J[b, m, y], tag[m], tag[y]]
                            else:
                                u = PAY[J[b, x, m], tag[x], tag[m]]
                            o = 3 - slot
                            if u[slot] > u0[slot] + 1e-12 or (weak and u[slot] >= u0[slot] - 1e-12 and (u[0] > u0[0] + 1e-12 or u[o] > u0[o] + 1e-12)):
                                st = 0; break
                        if not st: break
                out_stab[i, k, l] = st


def add_tables(G):
    ADDB = np.array([[G.add_gene_b(b, g) for g in range(NBG)] for b in range(G.KB)], np.int64)
    ADDW = np.array([[G.add_gene_w(x, g) for g in range(NWG)] for x in range(G.KW)], np.int64)
    return ADDB, ADDW


# ------------------------------------------------------------------ chain over units (classes or refined classes)
@njit(cache=True)
def _lrho(dw, N):
    if abs(dw) < 1e-12:
        return -np.log(N)
    if dw > 0:
        return np.log(-np.expm1(-dw)) - np.log(-np.expm1(-N * dw))
    a = -dw
    return np.log(np.expm1(a)) - N * a - np.log(-np.expm1(-N * a))


@njit(cache=True)
def _bsearch(arr, v):
    lo = 0; hi = arr.shape[0]
    while lo < hi:
        m = (lo + hi) // 2
        if arr[m] < v:
            lo = m + 1
        else:
            hi = m
    if lo < arr.shape[0] and arr[lo] == v:
        return lo
    return -1


@njit(cache=True)
def _trig_true_w(j, slot, k):
    wi = (j // 4) // 3; h = (j // 4) % 3; a1 = (j // 2) % 2; a2 = j % 2
    ao = a2 if slot == 1 else a1
    if k == 0: return wi == 0
    if k == 1: return wi <= 1
    if k == 2: return wi == 2
    if k == 3: return h == 0
    if k == 4: return h == 2
    if k == 5: return ao == 0
    if k == 6: return ao == 1
    return wi <= 1 and ao == 1


@njit(cache=True)
def _trig_true_b(j, k, QS, cx, cy):
    a1 = (j // 2) % 2; a2 = j % 2
    if k == 0: return a1 == 1
    if k == 1: return a2 == 1
    if k == 2: return a1 == 0
    if k == 3: return a2 == 0
    if k == 4: return QS[cx, cy, 0, 0] == 1
    if k == 5: return QS[cx, cy, 0, 1] == 1
    if k == 6: return QS[cx, cy, 1, 0] == 1
    return QS[cx, cy, 1, 1] == 1


@njit(cache=True)
def _local_cands(kernel, s, ub, ux, uy, j0, Jc, tagc, PAY, ucB, ucW, LOCB, LOCW, QSc, N, w, outq, outl):
    """local proposals of slot s at units (ub, ux, uy): fills outq (mutant unit), outl (log weight within the local
    half, i.e. log(1/|T|) or log(1/|A|)); returns the count (0 = no local proposal; the prior takes the whole event)."""
    cb = ucB[ub]; cx = ucW[ux]; cy = ucW[uy]
    n = 0
    if s == 0:
        LOC = LOCB; r = ub; nO = 6
    else:
        LOC = LOCW; r = ux if s == 1 else uy; nO = 2
    ng = LOC.shape[1]
    if kernel == 2:
        na = 0
        for g in range(ng):
            if LOC[r, g] >= -1:      # admissible genes are marked >= -1 (-2 = inadmissible); -1 = no program
                na += 1
        if na == 0:
            return 0
        for g in range(ng):
            m = LOC[r, g]
            if m >= 0:
                outq[n] = m; outl[n] = -np.log(na); n += 1
        return n
    # SG
    nt = ng // nO
    ntrue = 0
    best_m = np.empty(nt, np.int64)
    for t in range(nt):
        best_m[t] = -1
        if s == 0:
            tv = _trig_true_b(j0, t, QSc, cx, cy)
        else:
            tv = _trig_true_w(j0, s, t)
        if not tv:
            continue
        bu = -1e300; bm = -1; bcons = False
        bi = j0 // 4; wi = bi // 3; h = bi % 3; a_self = (j0 // 2) % 2 if s == 1 else j0 % 2
        anyadm = False
        for o in range(nO):
            m = LOC[r, t * nO + o]
            if m < -1:
                continue
            anyadm = True
            if m < 0:
                continue
            if s == 0:
                jj = Jc[ucB[m], cx, cy]; u = PAY[jj, tagc[cx], tagc[cy], 0]
                cons = (o < 3 and o == wi) or (o >= 3 and o - 3 == h)
            elif s == 1:
                mc = ucW[m]; jj = Jc[cb, mc, cy]; u = PAY[jj, tagc[mc], tagc[cy], 1]
                cons = o == a_self
            else:
                mc = ucW[m]; jj = Jc[cb, cx, mc]; u = PAY[jj, tagc[cx], tagc[mc], 2]
                cons = o == a_self
            if u > bu + 1e-12 or (abs(u - bu) <= 1e-12 and cons and not bcons):
                bu = u; bm = m; bcons = cons
        if anyadm:
            ntrue += 1
            best_m[t] = bm
    if ntrue == 0:
        return 0
    for t in range(nt):
        if best_m[t] >= 0:
            outq[n] = best_m[t]; outl[n] = -np.log(ntrue); n += 1
    return n


@njit(cache=True)
def _rows_g(Jc, tagc, PAY, ucB, ucW, logm, KuB, KuW, kernel, LOCB, LOCW, QSc, states, members, N, w, pi, theta_edge, mode):
    S = states.shape[0]
    cap = S * 16 + 1024
    src = np.empty(cap, np.int64); dst = np.empty(cap, np.int64); pr = np.empty(cap, np.float64)
    chg = np.empty(cap, np.bool_)
    out_chg = np.zeros(S); cut_chg = 0.0
    out_tot = np.zeros(S); pay = np.zeros((S, 3)); typ = np.zeros(S, np.int64)
    ne = 0
    cut = 0.0
    KK = KuW * KuW
    Km = max(KuB, KuW)
    candq = np.empty(Km + 64, np.int64); candl = np.empty(Km + 64)
    locq = np.empty(64, np.int64); locl = np.empty(64)
    for i in range(S):
        code = states[i]
        ub = code // KK; ux = (code // KuW) % KuW; uy = code % KuW
        cb = ucB[ub]; cx = ucW[ux]; cy = ucW[uy]
        j0 = Jc[cb, cx, cy]
        t1 = tagc[cx]; t2 = tagc[cy]
        r0 = PAY[j0, t1, t2, 0]; r1 = PAY[j0, t1, t2, 1]; r2 = PAY[j0, t1, t2, 2]
        pay[i, 0] = r0; pay[i, 1] = r1; pay[i, 2] = r2; typ[i] = j0 * 4 + t1 * 2 + t2
        for s in range(3):
            Kq = KuB if s == 0 else KuW
            res = ub if s == 0 else (ux if s == 1 else uy)
            nc = 0
            nl = 0
            if kernel > 0:
                nl = _local_cands(kernel, s, ub, ux, uy, j0, Jc, tagc, PAY, ucB, ucW, LOCB, LOCW, QSc, N, w, locq, locl)
            lf = 0.0 if nl == 0 else np.log(0.5)
            for q in range(Kq):
                if q == res or logm[s, q] < -1e300:
                    continue
                candq[nc] = q; candl[nc] = logm[s, q] + lf; nc += 1
            for k in range(nl):
                if locq[k] == res:
                    continue
                candq[nc] = locq[k]; candl[nc] = locl[k] + np.log(0.5) - np.log(3.0); nc += 1
            for k in range(nc):
                q = candq[k]
                if s == 0:
                    j = Jc[ucB[q], cx, cy]; tq1 = t1; tq2 = t2
                    dcode = q * KK + ux * KuW + uy
                elif s == 1:
                    mc = ucW[q]; j = Jc[cb, mc, cy]; tq1 = tagc[mc]; tq2 = t2
                    dcode = ub * KK + q * KuW + uy
                else:
                    mc = ucW[q]; j = Jc[cb, cx, mc]; tq1 = t1; tq2 = tagc[mc]
                    dcode = ub * KK + ux * KuW + q
                u0 = PAY[j, tq1, tq2, 0]; u1 = PAY[j, tq1, tq2, 1]; u2 = PAY[j, tq1, tq2, 2]
                us = u0 if s == 0 else (u1 if s == 1 else u2)
                ures = r0 if s == 0 else (r1 if s == 1 else r2)
                lp = candl[k] + _lrho(w * (us - ures), N)
                ep = np.exp(lp)
                out_tot[i] += ep
                ch = j != j0 or abs(u0 - r0) > 1e-12 or abs(u1 - r1) > 1e-12 or abs(u2 - r2) > 1e-12
                if ch:
                    out_chg[i] += ep
                jx = _bsearch(members, dcode)
                if mode == 0:
                    if jx < 0:
                        continue
                    vs = lp; ds = jx
                else:
                    if jx >= 0:
                        continue
                    fl = pi[i] + lp
                    cut += np.exp(fl)
                    if ch:
                        cut_chg += np.exp(fl)
                    if fl <= theta_edge:
                        continue
                    vs = fl; ds = dcode
                if ne >= cap:
                    cap2 = cap * 2
                    src2 = np.empty(cap2, np.int64); dst2 = np.empty(cap2, np.int64); pr2 = np.empty(cap2, np.float64)
                    chg2 = np.empty(cap2, np.bool_)
                    src2[:ne] = src[:ne]; dst2[:ne] = dst[:ne]; pr2[:ne] = pr[:ne]; chg2[:ne] = chg[:ne]
                    src, dst, pr, chg, cap = src2, dst2, pr2, chg2, cap2
                src[ne] = i; dst[ne] = ds; pr[ne] = vs; chg[ne] = ch; ne += 1
    return src[:ne], dst[:ne], pr[:ne], out_tot, pay, typ, cut, chg[:ne], out_chg, cut_chg


@njit(cache=True)
def _no_strict_exit(Jc, tagc, PAY, logm, KcB, KcW):
    """class triples with no strict exit (seeds)."""
    out = []
    for b in range(KcB):
        for x in range(KcW):
            for y in range(KcW):
                j0 = Jc[b, x, y]
                r = PAY[j0, tagc[x], tagc[y]]
                ok = True
                for q in range(KcB):
                    if logm[0, q] < -1e300: continue
                    if PAY[Jc[q, x, y], tagc[x], tagc[y], 0] > r[0] + 1e-12:
                        ok = False; break
                if ok:
                    for q in range(KcW):
                        if logm[1, q] < -1e300: continue
                        if PAY[Jc[b, q, y], tagc[q], tagc[y], 1] > r[1] + 1e-12:
                            ok = False; break
                        if PAY[Jc[b, x, q], tagc[x], tagc[q], 2] > r[2] + 1e-12:
                            ok = False; break
                if ok:
                    out.append((b * KcW + x) * KcW + y)
    return out


def make_units(G, L, arm, massB_prog, massW_prog, refine):
    """Units per slot: behaviour classes (refine False) or (class, base) refinements (refine True).  Returns
    unit -> class maps, unit masses (prior), unit representative program, and LOC tables (mutant unit per gene,
    -2 inadmissible, -1 no program)."""
    bsel, wsel = arm['bsel'], arm['wsel']
    if refine:
        kb = {}; ub = np.empty(len(bsel), np.int64)
        for i, b in enumerate(bsel):
            ub[i] = kb.setdefault((int(L['cb'][i]), int(G.bbase[b])), len(kb))
        kw = {}; uw = np.empty(len(wsel), np.int64)
        for k, x in enumerate(wsel):
            uw[k] = kw.setdefault((int(L['cw'][k]), int(G.wbase[x])), len(kw))
        ucB = np.array([c for (c, _), _i in sorted(kb.items(), key=lambda t: t[1])], np.int64)
        ucW = np.array([c for (c, _), _i in sorted(kw.items(), key=lambda t: t[1])], np.int64)
    else:
        ub = L['cb'].copy(); uw = L['cw'].copy()
        ucB = np.arange(L['KcB']); ucW = np.arange(L['KcW'])
    KuB, KuW = len(ucB), len(ucW)
    mB = np.bincount(ub, weights=massB_prog[bsel], minlength=KuB)
    mW = np.bincount(uw, weights=massW_prog[wsel], minlength=KuW)
    repB = np.full(KuB, -1, np.int64); repW = np.full(KuW, -1, np.int64)
    for i in np.argsort(-massB_prog[bsel], kind='stable'):
        if repB[ub[i]] < 0: repB[ub[i]] = bsel[i]
    for k in np.argsort(-massW_prog[wsel], kind='stable'):
        if repW[uw[k]] < 0: repW[uw[k]] = wsel[k]
    posB = {int(b): int(ub[i]) for i, b in enumerate(bsel)}; posW = {int(x): int(uw[k]) for k, x in enumerate(wsel)}
    LOCB = np.full((KuB, NBG), -2, np.int64); LOCW = np.full((KuW, NWG), -2, np.int64)
    for u in range(KuB):
        for g in range(NBG):
            if arm['gb'][g]:
                m = G.add_gene_b(int(repB[u]), g)
                LOCB[u, g] = posB.get(m, -1)
    for u in range(KuW):
        for g in range(NWG):
            if arm['gw'][g]:
                m = G.add_gene_w(int(repW[u]), g)
                LOCW[u, g] = posW.get(m, -1)
    return dict(ub=ub, uw=uw, ucB=ucB, ucW=ucW, KuB=KuB, KuW=KuW, massB=mB, massW=mW, repB=repB, repW=repW,
                LOCB=LOCB, LOCW=LOCW, posB=posB, posW=posW)


from dollar3_chain import Chain3, gth_scaled
from dollar3_solve import dense_log_gth


class GChain(Chain3):
    """The three-slot eps -> 0 chain over unit triples (exact under Lemma F), with a prior, SG or uniform-local
    mutation kernel.  Exploration and solve: Chain3.explore_hybrid (core by log-domain GTH, ring eliminated)."""

    def __init__(self, L, Un, QSc, kernel, N, w=W, theta=1e-9, max_states=400000, max_rounds=40, verbose=False,
                 core_max=2500, promote=1e-5, tag=''):
        self.arm, self.N, self.w = tag, N, w
        self.theta, self.max_states, self.max_rounds, self.verbose = theta, max_states, max_rounds, verbose
        self.core_max, self.promote, self.drop_rel = core_max, promote, 1e-5
        self.gth = dense_log_gth if N > 2000 else gth_scaled
        self.L, self.Un = L, Un
        self.Jc, self.tagc = L['Jc'], L['tagc']
        self.KuB, self.KuW = Un['KuB'], Un['KuW']
        self.Kc = self.KuW
        Km = max(self.KuB, self.KuW)
        mass = np.zeros((3, Km))
        mass[0, :self.KuB] = Un['massB']; mass[1, :self.KuW] = Un['massW']; mass[2, :self.KuW] = Un['massW']
        self.mass = mass
        with np.errstate(divide='ignore'):
            self.logm = np.where(mass > 0, np.log(mass) - np.log(3.0), -np.inf)
        self.kernel = kernel
        self.QSc = QSc
        self.PAY = PAY

    def code(self, b, x, y):
        return (int(b) * self.KuW + int(x)) * self.KuW + int(y)

    def decode(self, code):
        K = self.KuW
        return code // (K * K), (code // K) % K, code % K

    def rows(self, codes, members=None, lpi=None, theta_edge=0.0, mode=0):
        codes = np.asarray(codes, np.int64)
        members = codes if members is None else np.asarray(members, np.int64)
        if lpi is None: lpi = np.zeros(len(codes))
        return _rows_g(self.Jc, self.tagc, self.PAY, self.Un['ucB'], self.Un['ucW'], self.logm, self.KuB, self.KuW,
                       self.kernel, self.Un['LOCB'], self.Un['LOCW'], self.QSc, codes, members, float(self.N), self.w, lpi,
                       np.log(theta_edge) if theta_edge > 0 else -np.inf, mode)


# ------------------------------------------------------------------ chicken
@njit(cache=True)
def chicken_play(ca, cb_, ng_a, tr_a, ov_a, ng_b, tr_b, ov_b, ba, bb_a, bb_b, out_ops):
    """stable (action_1, action_2) of chicken programs (base default a, flag b; gene lists).  Atoms
    BOX(THEM = St) / BOX(THEM = Sw) on the linear GL chain.  out_ops <- operative gene index per player."""
    f = np.ones((2, 2), np.bool_)        # f[i, k]: player i's box "THEM = k" (k 0 St, 1 Sw)
    acts = np.zeros(2, np.int64)
    ops = np.zeros(2, np.int64)
    for n in range(64):
        for i in range(2):
            ng = ng_a if i == 0 else ng_b
            op = -1; act = -1
            for g in range(ng):
                t = tr_a[g] if i == 0 else tr_b[g]
                if f[i, t]:
                    op = g; act = ov_a[g] if i == 0 else ov_b[g]
                    break
            if op < 0:
                a = ca if i == 0 else cb_
                bflag = bb_a if i == 0 else bb_b
                act = 1 if (bflag == 1 and f[i, 0]) else a
            acts[i] = act; ops[i] = op
        changed = False
        for i in range(2):
            them = acts[1 - i]
            for k in range(2):
                if f[i, k] and them != k:
                    f[i, k] = False; changed = True
        if not changed and n >= 2:
            out_ops[0] = ops[0]; out_ops[1] = ops[1]
            return acts[0], acts[1]
    return -1, -1


CHICKEN = np.array([[-10.0, 2.0], [-1.0, 0.0]])


class Chicken:
    def __init__(self, cap=2):
        self.cap = cap
        GL = gene_lists(NCG, cap)
        self.prog = [(bi, gl) for bi in range(len(C_BASES)) for gl in GL]
        K = len(self.prog)
        self.K = K
        self.size = np.array([C_BASE_SIZE[C_BASES[bi]] + GENE_SIZE * len(gl) for bi, gl in self.prog])
        self.index = {v: i for i, v in enumerate(self.prog)}
        A = np.zeros((K, K), np.int64); B = np.zeros((K, K), np.int64)
        OPA = np.zeros((K, K), np.int64); OPB = np.zeros((K, K), np.int64)
        ops = np.zeros(2, np.int64)
        for a in range(K):
            for b in range(K):
                pa, pb = self.arr(a), self.arr(b)
                x, y = chicken_play(pa[0], pb[0], pa[2], pa[3], pa[4], pb[2], pb[3], pb[4], 0, pa[1], pb[1], ops)
                assert x >= 0
                A[a, b], B[a, b] = x, y
                OPA[a, b], OPB[a, b] = ops[0], ops[1]
        self.A, self.B, self.OPA, self.OPB = A, B, OPA, OPB      # A[a, b] action of role-1 a vs role-2 b
        # no ROLE and a symmetric evaluator: B[a, b] == A[b, a]
        self.U = CHICKEN[A, B]                                # role-1 payoff; role-2 payoff is U.T by symmetry

    def arr(self, i):
        bi, gl = self.prog[i]
        a, b = C_BASES[bi]
        tr = np.array([g // 2 for g in gl] + [0, 0], np.int64)[:2]
        ov = np.array([g % 2 for g in gl] + [0, 0], np.int64)[:2]
        return a, b, len(gl), tr, ov

    def name(self, i):
        bi, gl = self.prog[i]
        a, b = C_BASES[bi]
        return '(%s,%d)' % ('St' if a == 0 else 'Sw', b) + ''.join('+' + cgene_name(g) for g in gl)

    def add_gene(self, i, g):
        bi, gl = self.prog[i]
        gl2 = (gl + (g,)) if len(gl) < self.cap else (gl[:-1] + (g,))
        if len(gl2) == 2 and gl2[0] == gl2[1]:
            gl2 = gl2[:1]
        return self.index.get((bi, gl2), -1)

    def filter(self, sel=None):
        """override filter: gene admitted iff wherever it is operative (either role) its override is a best reply to
        the opponent's stable action."""
        sel = np.arange(self.K) if sel is None else np.asarray(sel)
        m = length_prior(self.size)
        out = {}
        for g in range(NCG):
            tr, ov = g // 2, g % 2
            fired = 0; failed = 0; wf = None; wp = None
            for a in sel:
                bi, gl = self.prog[a]
                if g not in gl:
                    continue
                pos = gl.index(g)
                for b in sel:
                    if self.OPA[a, b] == pos:
                        fired += 1
                        them = self.B[a, b]
                        ok = CHICKEN[ov, them] >= CHICKEN[1 - ov, them] - 1e-12
                        if not ok:
                            failed += 1
                            if wf is None or m[a] * m[b] > wf[0]:
                                wf = (m[a] * m[b], self.name(a), self.name(b), int(self.A[a, b]), int(them))
                        elif wp is None or m[a] * m[b] > wp[0]:
                            wp = (m[a] * m[b], self.name(a), self.name(b), int(self.A[a, b]), int(them))
            out[g] = dict(name=cgene_name(g), fired=fired, failed=failed, admitted=failed == 0, vacuous=fired == 0,
                          witness_fail=wf[1:] if wf else None, witness_pass=wp[1:] if wp else None)
        return out


def chicken_arm(C, name, filt, rr_seed=20261011):
    ga = np.ones(NCG, bool)
    bases = np.ones(len(C_BASES), bool)
    nm = name.replace('-ctl', '')
    if nm == 'base':
        ga[:] = False
    elif nm == 'G-all':
        pass
    elif nm in ('G-cred', 'G-recip'):
        ga = np.array([filt[g]['admitted'] for g in range(NCG)])
    elif nm == 'random':
        k = sum(filt[g]['admitted'] for g in range(NCG))
        rng = np.random.default_rng(rr_seed)
        ga = np.zeros(NCG, bool); ga[rng.choice(NCG, k, replace=False)] = True
    elif nm == 'const':
        ga[:] = False; bases = np.array([C_BASES[i][1] == 0 for i in range(len(C_BASES))])
    else:
        raise ValueError(name)
    if name.endswith('-ctl'):
        bases = np.array([C_BASES[i][0] == 1 for i in range(len(C_BASES))])
    sel = np.array([i for i, (bi, gl) in enumerate(C.prog) if bases[bi] and all(ga[g] for g in gl)], np.int64)
    return dict(name=name, ga=ga, sel=sel)


def chicken_chain_dense(Uc, logmu1, logmu2, N, w=W, local=None):
    """exact two-population chain over unit pairs (a | b) with log-domain GTH.  Uc[a, b] role-1 payoff of unit a
    against unit b (role-2 payoff Uc[b, a]).  logmu: per-role log prior over units (null = -inf).  local: optional
    (kernel, list of per-unit proposal functions) for SG / uniform-local: local(a, b, role) -> [(unit, logw)]."""
    from chain_log import gth_log, order_by_exit
    K = Uc.shape[0]
    S = K * K
    LA = np.full((S, S), -np.inf)
    for a in range(K):
        for b in range(K):
            s0 = a * K + b
            for role in (0, 1):
                cands = []
                loc = local(a, b, role) if local is not None else []
                lf = 0.0 if not loc else math.log(0.5)
                lm = logmu1 if role == 0 else logmu2
                for q in range(K):
                    if np.isfinite(lm[q]):
                        cands.append((q, lm[q] + lf + math.log(0.5)))
                for q, lw in loc:
                    cands.append((q, lw + math.log(0.5) + math.log(0.5)))
                for q, lw in cands:
                    if role == 0:
                        if q == a: continue
                        du = Uc[q, b] - Uc[a, b]; d = q * K + b
                    else:
                        if q == b: continue
                        du = Uc[q, a] - Uc[b, a]; d = a * K + q
                    LA[s0, d] = np.logaddexp(LA[s0, d], lw + _lrho(w * du, float(N)))
    np.fill_diagonal(LA, -np.inf)
    order, _ = order_by_exit(LA)
    lx = gth_log(LA[np.ix_(order, order)])
    lpi = np.empty(S); lpi[order] = lx
    return lpi.reshape(K, K), LA


# ------------------------------------------------------------------ scale guard
def scale_guard(cap=2, npairs=2000, nboss=3000, seed=11, rule='CC', verbose=True):
    """Lower bounds on the class counts at `cap` by fingerprints: bosses against `npairs` sampled worker pairs (all
    bosses); workers (W1 slot) against `nboss` sampled bosses x all W2 programs (tag included)."""
    G = SOG(cap)
    rb, rw = RULES[rule]
    t0 = time.time()
    FV, QS = quoted_tables(G.KW, TT2, *G.warrays(), rb, rw, C_WHACK)
    rng = np.random.default_rng(seed)
    X = rng.integers(0, G.KW, npairs); Y = rng.integers(0, G.KW, npairs)
    fpB = set()
    chunk = 2000
    for b0 in range(0, G.KB, chunk):
        Bs = np.arange(b0, min(G.KB, b0 + chunk))
        Jb = np.empty((len(Bs), npairs), np.int8)
        for p in range(npairs):
            Jp, _ = tensor_g(Bs, X[p:p + 1], Y[p:p + 1], FV, TT2, *G.barrays(), *G.warrays(), rb, rw, C_WHACK)
            Jb[:, p] = Jp[:, 0, 0]
        for r in Jb:
            fpB.add(r.tobytes())
    Bsamp = rng.integers(0, G.KB, nboss)
    Jw, _ = tensor_g(Bsamp, np.arange(G.KW), np.arange(G.KW)[rng.integers(0, G.KW, 60)], FV, TT2, *G.barrays(), *G.warrays(), rb, rw, C_WHACK)
    fpW = set((int(G.tag[x]), Jw[:, x, :].tobytes()) for x in range(G.KW))
    res = dict(cap=cap, rule=rule, KB_programs=G.KB, KW_programs=G.KW, boss_classes_lower_bound=len(fpB),
               worker_classes_lower_bound=len(fpW), npairs=npairs, nboss=nboss, time_s=time.time() - t0)
    if verbose:
        print(res, flush=True)
    return res


# ------------------------------------------------------------------ SG proposals at program level (diagnostics)
def trig_true_state(G, Tbl, slot, t, b, x, y):
    j = int(Tbl['J'][b, x, y])
    if slot == 0:
        a1, a2 = (j // 2) % 2, j % 2
        if t == 0: return a1 == 1
        if t == 1: return a2 == 1
        if t == 2: return a1 == 0
        if t == 3: return a2 == 0
        q = 0 if t in (4, 5) else 1
        i = 0 if t in (4, 6) else 1
        return int(Tbl['QS'][x, y, q, i]) == 1
    return bool(_trig_true_w(j, slot, t))


def sg_proposals(G, Tbl, arm, b, x, y):
    """SG's targeted proposals (notes §1.10) at the program triple (b, x, y): per slot, per true trigger with an
    admissible override, the chosen override, its payoff change and kind (strict / conservative tie / loss)."""
    J = Tbl['J']
    j0 = int(J[b, x, y]); u0 = PAY[j0, G.tag[x], G.tag[y]]
    bi = j0 // 4; wi, h = bi // 3, bi % 3
    out = {}
    for slot in (0, 1, 2):
        props = []
        nt = len(B_TRIG) if slot == 0 else len(W_TRIG)
        nO = 6 if slot == 0 else 2
        for t in range(nt):
            if not trig_true_state(G, Tbl, slot, t, b, x, y):
                continue
            best = None
            for o in range(nO):
                g = t * nO + o
                if not (arm['gb'][g] if slot == 0 else arm['gw'][g]):
                    continue
                if slot == 0:
                    m = G.add_gene_b(b, g)
                    if m < 0 or m not in set(arm['bsel'].tolist()): continue
                    jj = int(J[m, x, y]); u = PAY[jj, G.tag[x], G.tag[y]]
                    cons = (o < 3 and o == wi) or (o >= 3 and o - 3 == h)
                else:
                    r = x if slot == 1 else y
                    m = G.add_gene_w(r, g)
                    if m < 0: continue
                    xx, yy = (m, y) if slot == 1 else (x, m)
                    jj = int(J[b, xx, yy]); u = PAY[jj, G.tag[xx], G.tag[yy]]
                    a_self = (j0 // 2) % 2 if slot == 1 else j0 % 2
                    cons = o == a_self
                du = float(u[slot] - u0[slot])
                key = (du, cons)
                if best is None or du > best[0] + 1e-12 or (abs(du - best[0]) <= 1e-12 and cons and not best[1]):
                    best = (du, cons, g, jj, u.tolist())
            if best is not None:
                du, cons, g, jj, u = best
                kind = 'strict' if du > 1e-12 else ('conservative' if abs(du) <= 1e-12 else 'loss')
                props.append(dict(gene=(bgene_name(g) if slot == 0 else wgene_name(g)), du=du, kind=kind, play=U.joint_name(jj),
                                  whack=(slot == 0 and g % 6 in (3, 5))))
        out[['B', 'W1', 'W2'][slot]] = props
    return out
