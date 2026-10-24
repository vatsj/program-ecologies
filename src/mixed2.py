"""Mixed actions in two-role games: the inspection game and Basic Endgame (spec specs/2026-10-23-two-role-mixed.md;
notes notes/mixed2.md; predictions predictions/2026-10-23-two-role-mixed.md).

Library: the typed two-role program grammar (canonical enumeration with spelling multiplicities), the exact depth-capped
evaluator with hidden cards and the serial depth price, payoffs with the forfeit convention, behavioural classes, class
level statistics, and the two-population epsilon -> 0 chain and epsilon = 0 island lottery.

Roles: 0 = inspector / player I, 1 = inspectee / player II.  A node has a context role r (the role of the program it
sits in) and a type t (whose action it denotes).  `THEM(arg)` in context r has type 1 - r; `cr`, `sr`, `sr_k` map a
type 1 - t expression to a type t one; `if Q = act0 then A else B` (Q an application) keeps the type of A and B;
`card A B` exists only for Endgame I.  Values are 6-vectors (card W: a0, a1, F; card L: a0, a1, F); a card-free value
repeats its three numbers.  An application met at depth 0 forfeits (F).  See notes/mixed2.md for the semantics.
"""
import math, os, sys, hashlib, zlib
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import tempfile
CACHE = os.environ.get('MIXED2_CACHE', os.path.join(tempfile.gettempdir(), 'mixed2_cache'))

W = 0.3
TIE = 1e-9
PW = 1.0 / 3.0          # P(card wins) in Endgame

# ---------------------------------------------------------------- opcodes
OP_C0, OP_C1, OP_X, OP_COIN, OP_CR, OP_SR, OP_SRK, OP_CARD, OP_IF, OP_APP = range(10)
APP_ME, APP_UP = 0, 1

# ---------------------------------------------------------------- the games
# Pay0[c][x][y] / Pay1[c][x][y]: payoff to role 0 / role 1 when role 0 plays x and role 1 plays y, role 0's card c
# (c = 0 winner, 1 loser; the inspection game has no card, both slices equal).  Actions: inspection role 0 (I, N),
# role 1 (C, K); Endgame role 0 (BET, CHECK), role 1 (CALL, FOLD).
GAMES = {}


def _mk_game(name, pay0_by_card, weights):
    P0 = np.array(pay0_by_card, float)               # (2, 2, 2)
    return dict(name=name, Pay0=P0, weights=np.array(weights, float))


_insp = np.array([[-1, -1], [0, -4]], float)         # inspector: (I,C) -1, (I,K) -1, (N,C) 0, (N,K) -4
_insp1 = np.array([[0, -3], [0, 1]], float)          # inspectee
GAMES['insp'] = dict(name='insp', Pay0=np.stack([_insp, _insp]), Pay1=np.stack([_insp1, _insp1]),
                     weights=np.array([1.0, 0.0]), card=False,
                     act=(('I', 'N'), ('C', 'K')))
_endW = np.array([[3, 1], [1, 1]], float)            # winner: bet-call +3, bet-fold +1, check +1
_endL = np.array([[-3, 1], [-1, -1]], float)         # loser: bet-call -3, bet-fold +1, check -1
GAMES['end'] = dict(name='end', Pay0=np.stack([_endW, _endL]), Pay1=-np.stack([_endW, _endL]),
                    weights=np.array([PW, 1 - PW]), card=True,
                    act=(('BET', 'CHECK'), ('CALL', 'FOLD')))

ARMS = {
    'blind':   dict(app=False, unary=None),
    'sample':  dict(app=True, unary=None),
    'exact':   dict(app=True, unary=OP_CR),
    'matched': dict(app=True, unary=OP_SR),
    'sr4':     dict(app=True, unary=OP_SRK, k=4),
    'sr16':    dict(app=True, unary=OP_SRK, k=16),
}


def game_tensors(gname):
    """T[t][oc][a][cc][y]: responder's payoff, responder type t with own card oc playing a, opponent card cc playing y;
    forfeit-payoff tables FI (role 0 forfeits) / FII (role 1 forfeits) / FF (both)."""
    g = GAMES[gname]
    P0, P1 = g['Pay0'], g['Pay1']
    T = np.zeros((2, 2, 2, 2, 2))
    for oc in range(2):
        for a in range(2):
            for cc in range(2):
                for y in range(2):
                    T[0, oc, a, cc, y] = P0[oc, a, y]          # role 0: own card oc, own action a, opponent action y
                    T[1, oc, a, cc, y] = P1[cc, y, a]          # role 1: opponent (role 0) card cc, action y; own action a
    # role 0 forfeits (card c) against role 1's realized action y: worst action x for role 0
    FI0 = np.zeros((2, 2)); FI1 = np.zeros((2, 2))
    for c in range(2):
        for y in range(2):
            col = P0[c, :, y]
            mn = col.min()
            tied = np.nonzero(col <= mn + TIE)[0]
            FI0[c, y] = mn
            FI1[c, y] = np.mean([P1[c, x, y] for x in tied])
    # role 1 forfeits against (c, x): worst action y for role 1
    FII0 = np.zeros((2, 2)); FII1 = np.zeros((2, 2))
    for c in range(2):
        for x in range(2):
            row = P1[c, x, :]
            mn = row.min()
            tied = np.nonzero(row <= mn + TIE)[0]
            FII1[c, x] = mn
            FII0[c, x] = np.mean([P0[c, x, y] for y in tied])
    FF = np.array([P0.min(), P1.min()])
    return T, FI0, FI1, FII0, FII1, FF


# ---------------------------------------------------------------- language
class Lang2:
    """Canonical typed enumeration up to n nodes for one game and arm.  Nodes are hash-consed; `coin` is commutative
    and `if` has its alpha fixed to the first action of the test's type (the branches swap), so a node carries a
    multiplicity: the number of spellings it stands for.  Programs of role r are the nodes of context r and type r."""

    def __init__(self, game, arm, n):
        self.game, self.arm, self.n = game, arm, n
        self.g = GAMES[game]
        self.a_ = ARMS[arm]
        self.op, self.A, self.B, self.C, self.K = [], [], [], [], []
        self.ctx, self.typ, self.size, self.mult = [], [], [], []
        self.key = {}
        self.by = {(r, t, s): [] for r in (0, 1) for t in (0, 1) for s in range(1, n + 1)}
        self._enumerate()
        self._programs()
        self._prior()
        self._tapes()
        self._src = {}

    def _add(self, key, op, A, B, C, K, r, t, s, mult):
        e = self.key.get(key)
        if e is not None:
            self.mult[e] += mult
            return e
        e = len(self.op)
        self.key[key] = e
        self.op.append(op); self.A.append(A); self.B.append(B); self.C.append(C); self.K.append(K)
        self.ctx.append(r); self.typ.append(t); self.size.append(s); self.mult.append(mult)
        self.by[(r, t, s)].append(e)
        return e

    def _enumerate(self):
        n, card, a_ = self.n, self.g['card'], self.a_
        by, mult = self.by, self.mult
        for s in range(1, n + 1):
            for r in (0, 1):
                if a_['app']:
                    if s == 3:
                        self._add(('app', r, APP_ME, -1), OP_APP, -1, -1, -1, APP_ME, r, 1 - r, 3, 1)
                    if s >= 4:
                        for b in by[(r, r, s - 3)]:
                            self._add(('app', r, APP_UP, b), OP_APP, -1, b, -1, APP_UP, r, 1 - r, s, mult[b])
            for r in (0, 1):
                for t in (0, 1):
                    if s == 1:
                        self._add(('c0', r, t), OP_C0, -1, -1, -1, 0, r, t, 1, 1)
                        self._add(('c1', r, t), OP_C1, -1, -1, -1, 0, r, t, 1, 1)
                        self._add(('x', r, t), OP_X, -1, -1, -1, 0, r, t, 1, 1)
                        continue
                    if a_['unary'] is not None:
                        for c in by[(r, 1 - t, s - 1)]:
                            k = a_.get('k', 0)
                            self._add(('u', a_['unary'], r, t, c), a_['unary'], c, -1, -1, k, r, t, s, mult[c])
                    for i in range(1, s - 1):
                        j = s - 1 - i
                        if j < i:
                            continue
                        for x in by[(r, t, i)]:
                            for y in by[(r, t, j)]:
                                if i == j and y < x:
                                    continue
                                m = mult[x] ** 2 if x == y else 2 * mult[x] * mult[y]
                                self._add(('coin', r, t, x, y), OP_COIN, x, y, -1, 0, r, t, s, m)
                    if card and r == 0 and t == 0:
                        for i in range(1, s - 1):
                            j = s - 1 - i
                            for x in by[(r, t, i)]:
                                for y in by[(r, t, j)]:
                                    self._add(('card', x, y), OP_CARD, x, y, -1, 0, r, t, s, mult[x] * mult[y])
                    if a_['app']:
                        for q in range(3, s - 2):
                            for a in range(1, s - q - 1):
                                b = s - 1 - q - a
                                if b < 1:
                                    continue
                                for Q in by[(r, 1 - r, q)]:
                                    if self.op[Q] != OP_APP:
                                        continue
                                    for x in by[(r, t, a)]:
                                        for y in by[(r, t, b)]:
                                            self._add(('if', r, t, Q, x, y), OP_IF, x, y, Q, 0, r, t, s, 2 * mult[Q] * mult[x] * mult[y])
        for k in ('op', 'A', 'B', 'C', 'K', 'ctx', 'typ', 'size'):
            setattr(self, k, np.array(getattr(self, k), np.int64))
        self.mult = np.array(self.mult, float)
        self.S = len(self.op)

    def _programs(self):
        self.progs = []                     # per role: array of node ids (ascending)
        self.pidx = np.full(self.S, -1, np.int64)
        for r in (0, 1):
            ids = np.nonzero((self.ctx == r) & (self.typ == r))[0]
            self.progs.append(ids)
            self.pidx[ids] = np.arange(len(ids))
        self.S0, self.S1 = len(self.progs[0]), len(self.progs[1])

    def _prior(self):
        """mu(p) = mult(p) / (a(|p|) * 2 |p|^2), normalised: the length prior of the weak arm (bits = log2 a(|p|) + 2 log2 |p| + 1)
        over spellings; a(s) is the number of spellings of size s."""
        self.mu, self.size_prog, self.a_size = [], [], []
        for r in (0, 1):
            ids = self.progs[r]
            sz = self.size[ids]
            a = np.zeros(self.n + 1)
            np.add.at(a, sz, self.mult[ids])
            w = self.mult[ids] / (a[sz] * 2.0 * sz * sz)
            self.mu.append(w / w.sum())
            self.a_size.append(a)
            self.size_prog.append(sz)

    def _tape_one(self, e, out):
        o = self.op[e]
        if o in (OP_C0, OP_C1, OP_X):
            out.append((o, -1, -1, -1, 0, self.typ[e])); return len(out) - 1
        if o in (OP_CR, OP_SR, OP_SRK):
            c = self._tape_one(self.A[e], out)
            out.append((o, c, -1, -1, self.K[e], self.typ[e])); return len(out) - 1
        if o == OP_COIN or o == OP_CARD:
            x = self._tape_one(self.A[e], out); y = self._tape_one(self.B[e], out)
            out.append((o, x, y, -1, 0, self.typ[e])); return len(out) - 1
        if o == OP_IF:
            q = self._tape_one(self.C[e], out); x = self._tape_one(self.A[e], out); y = self._tape_one(self.B[e], out)
            out.append((o, x, y, q, 0, self.typ[e])); return len(out) - 1
        if o == OP_APP:
            arg = -1 if self.K[e] == APP_ME else int(self.pidx[self.B[e]])
            out.append((o, -1, -1, -1, arg, self.typ[e])); return len(out) - 1
        raise ValueError(o)

    def _tapes(self):
        T = self.n
        self.tape = []
        for r in (0, 1):
            ids = self.progs[r]
            S = len(ids)
            ta = np.zeros((S, T, 6), np.int64)
            tl = np.zeros(S, np.int64)
            for i, e in enumerate(ids):
                tp = []
                self._tape_one(e, tp)
                assert len(tp) <= T
                tl[i] = len(tp)
                for j, row in enumerate(tp):
                    ta[i, j] = row
            self.tape.append((np.ascontiguousarray(ta), tl))
        # syntactic flags per program
        self.has_app = [np.zeros(len(self.progs[r]), bool) for r in (0, 1)]
        self.has_cr = [np.zeros(len(self.progs[r]), bool) for r in (0, 1)]
        self.has_if = [np.zeros(len(self.progs[r]), bool) for r in (0, 1)]
        self.has_sr = [np.zeros(len(self.progs[r]), bool) for r in (0, 1)]
        for r in (0, 1):
            ta, tl = self.tape[r]
            for i in range(len(tl)):
                ops = ta[i, :tl[i], 0]
                self.has_app[r][i] = (ops == OP_APP).any()
                self.has_cr[r][i] = (ops == OP_CR).any()
                self.has_if[r][i] = (ops == OP_IF).any()
                self.has_sr[r][i] = ((ops == OP_SR) | (ops == OP_SRK)).any()

    # ---- printing and lookup
    def src(self, e):
        if e in self._src:
            return self._src[e]
        o = self.op[e]; t = self.typ[e]; r = self.ctx[e]
        act = self.g['act'][t]
        if o == OP_C0: s = act[0]
        elif o == OP_C1: s = act[1]
        elif o == OP_X: s = 'X'
        elif o == OP_COIN: s = 'coin(%s,%s)' % (self.src(self.A[e]), self.src(self.B[e]))
        elif o == OP_CR: s = 'cr(%s)' % self.src(self.A[e])
        elif o == OP_SR: s = 'sr(%s)' % self.src(self.A[e])
        elif o == OP_SRK: s = 'sr%d(%s)' % (self.K[e], self.src(self.A[e]))
        elif o == OP_CARD: s = 'card(%s,%s)' % (self.src(self.A[e]), self.src(self.B[e]))
        elif o == OP_IF:
            q_act = self.g['act'][1 - r][0]
            s = 'if(%s=%s,%s,%s)' % (self.src(self.C[e]), q_act, self.src(self.A[e]), self.src(self.B[e]))
        elif o == OP_APP:
            s = 'THEM(ME)' if self.K[e] == APP_ME else 'THEM(^%s)' % self.src(self.B[e])
        else:
            raise ValueError(o)
        self._src[e] = s
        return s

    def prog_names(self, r):
        return [self.src(e) for e in self.progs[r]]

    def find(self, r, s):
        if not hasattr(self, '_rev'):
            self._rev = [{self.src(e): i for i, e in enumerate(self.progs[rr])} for rr in (0, 1)]
        return self._rev[r][s]


# ---------------------------------------------------------------- evaluator kernel
@njit(cache=True)
def _binom_pmf(k, n, q):
    if q <= 0.0:
        return 1.0 if n == 0 else 0.0
    if q >= 1.0:
        return 1.0 if n == k else 0.0
    return math.exp(math.lgamma(k + 1.0) - math.lgamma(n + 1.0) - math.lgamma(k - n + 1.0) + n * math.log(q) + (k - n) * math.log(1.0 - q))


@njit(cache=True)
def _br2(u0, u1, tie):
    """best response over two actions with the reader's own fair coin on ties: returns (p0, p1)."""
    if abs(u0 - u1) <= tie:
        return 0.5, 0.5
    if u0 > u1:
        return 1.0, 0.0
    return 0.0, 1.0


@njit(cache=True)
def _eval_role(ta, tl, S, Sopp, Gopp, Eopp, Mopp, Wopp, d, Gout, Eout, Mout, Wout, T, wts, workmode):
    """One level for the programs of one role against the programs of the other.  ta: (S, Tmax, 6) tape rows
    (op, a, b, c, k, type); Gopp[b, arg] is the opponent's value at level d - 1 (width Wopp); outputs Gout[a, b]."""
    Tmax = ta.shape[1]
    vals = np.empty((Tmax, 6))
    ev = np.empty(Tmax)
    mv = np.empty(Tmax)
    for a in range(S):
        L = tl[a]
        for b in range(Sopp):
            for t in range(L):
                o = ta[a, t, 0]
                tp = ta[a, t, 5]
                if o == 0 or o == 1:
                    for c in range(2):
                        vals[t, 3 * c + 0] = 1.0 if o == 0 else 0.0
                        vals[t, 3 * c + 1] = 1.0 if o == 1 else 0.0
                        vals[t, 3 * c + 2] = 0.0
                    ev[t] = 0.0; mv[t] = 0.0
                elif o == 2:
                    for c in range(2):
                        vals[t, 3 * c + 0] = 0.5; vals[t, 3 * c + 1] = 0.5; vals[t, 3 * c + 2] = 0.0
                    ev[t] = 0.0; mv[t] = 0.0
                elif o == 3:       # coin
                    x = ta[a, t, 1]; y = ta[a, t, 2]
                    for j in range(6):
                        vals[t, j] = 0.5 * (vals[x, j] + vals[y, j])
                    ev[t] = 0.5 * (ev[x] + ev[y]); mv[t] = (mv[x] + mv[y]) if workmode == 1 else max(mv[x], mv[y])
                elif o == 7:       # card A B: winner slice of A, loser slice of B
                    x = ta[a, t, 1]; y = ta[a, t, 2]
                    for j in range(3):
                        vals[t, j] = vals[x, j]
                        vals[t, 3 + j] = vals[y, 3 + j]
                    ev[t] = wts[0] * ev[x] + wts[1] * ev[y]; mv[t] = (mv[x] + mv[y]) if workmode == 1 else max(mv[x], mv[y])
                elif o == 8:       # if Q = act0 then A else B
                    x = ta[a, t, 1]; y = ta[a, t, 2]; q = ta[a, t, 3]
                    p0 = wts[0] * vals[q, 0] + wts[1] * vals[q, 3]
                    p1 = wts[0] * vals[q, 1] + wts[1] * vals[q, 4]
                    pf = wts[0] * vals[q, 2] + wts[1] * vals[q, 5]
                    for c in range(2):
                        vals[t, 3 * c + 0] = p0 * vals[x, 3 * c + 0] + p1 * vals[y, 3 * c + 0]
                        vals[t, 3 * c + 1] = p0 * vals[x, 3 * c + 1] + p1 * vals[y, 3 * c + 1]
                        vals[t, 3 * c + 2] = p0 * vals[x, 3 * c + 2] + p1 * vals[y, 3 * c + 2] + pf
                    ev[t] = ev[q] + p0 * ev[x] + p1 * ev[y]
                    mv[t] = mv[q] + ((mv[x] + mv[y]) if workmode == 1 else max(mv[x], mv[y]))
                elif o == 9:       # application THEM(arg)
                    if d == 0:
                        vals[t, 0] = 0.0; vals[t, 1] = 0.0; vals[t, 2] = 1.0
                        vals[t, 3] = 0.0; vals[t, 4] = 0.0; vals[t, 5] = 1.0
                        ev[t] = 0.0; mv[t] = 0.0
                    else:
                        arg = ta[a, t, 4]
                        if arg < 0:
                            arg = a
                        if Wopp == 6:
                            for j in range(6):
                                vals[t, j] = Gopp[b, arg, j]
                        else:
                            for j in range(3):
                                vals[t, j] = Gopp[b, arg, j]
                                vals[t, 3 + j] = Gopp[b, arg, j]
                        ev[t] = 1.0 + Eopp[b, arg]
                        mv[t] = 1.0 + Mopp[b, arg]
                else:              # 4 cr, 5 sr, 6 srk: responder of type tp reads the child (type 1 - tp)
                    x = ta[a, t, 1]
                    k = ta[a, t, 4]
                    # card-weighted joint of the child: m[cc, y]
                    m00 = wts[0] * vals[x, 0]; m01 = wts[0] * vals[x, 1]
                    m10 = wts[1] * vals[x, 3]; m11 = wts[1] * vals[x, 4]
                    pf = wts[0] * vals[x, 2] + wts[1] * vals[x, 5]
                    z = 1.0 - pf
                    nout = 2          # number of own-card slices computed
                    if z < 1e-15:
                        for j in range(6):
                            vals[t, j] = 0.0
                        vals[t, 2] = 1.0; vals[t, 5] = 1.0
                    else:
                        for oc in range(2):
                            if o == 4:
                                u0 = (m00 * T[tp, oc, 0, 0, 0] + m01 * T[tp, oc, 0, 0, 1] + m10 * T[tp, oc, 0, 1, 0] + m11 * T[tp, oc, 0, 1, 1]) / z
                                u1 = (m00 * T[tp, oc, 1, 0, 0] + m01 * T[tp, oc, 1, 0, 1] + m10 * T[tp, oc, 1, 1, 0] + m11 * T[tp, oc, 1, 1, 1]) / z
                                p0, p1 = _br2(u0, u1, 1e-9)
                                vals[t, 3 * oc + 0] = z * p0; vals[t, 3 * oc + 1] = z * p1; vals[t, 3 * oc + 2] = pf
                            elif o == 5:
                                # one full draw (cc, y) with its card, best response to that draw
                                r0 = 0.0; r1 = 0.0
                                for cc in range(2):
                                    for y in range(2):
                                        if cc == 0:
                                            mm = m00 if y == 0 else m01
                                        else:
                                            mm = m10 if y == 0 else m11
                                        p0, p1 = _br2(T[tp, oc, 0, cc, y], T[tp, oc, 1, cc, y], 1e-9)
                                        r0 += mm * p0; r1 += mm * p1
                                vals[t, 3 * oc + 0] = r0; vals[t, 3 * oc + 1] = r1; vals[t, 3 * oc + 2] = pf
                            else:
                                # k draws (card-free games): empirical frequency of opponent action 1 among k draws
                                qq = (m01 + m11) / z
                                zk = z ** k
                                r0 = 0.0; r1 = 0.0
                                for nn in range(k + 1):
                                    pm = _binom_pmf(k, nn, qq)
                                    f1 = nn / k
                                    uu0 = (1.0 - f1) * T[tp, oc, 0, 0, 0] + f1 * T[tp, oc, 0, 0, 1]
                                    uu1 = (1.0 - f1) * T[tp, oc, 1, 0, 0] + f1 * T[tp, oc, 1, 0, 1]
                                    p0, p1 = _br2(uu0, uu1, 1e-9)
                                    r0 += pm * p0; r1 += pm * p1
                                vals[t, 3 * oc + 0] = zk * r0; vals[t, 3 * oc + 1] = zk * r1; vals[t, 3 * oc + 2] = 1.0 - zk
                    if o == 6:
                        ev[t] = k * ev[x]; mv[t] = k * mv[x]
                    elif o == 5:
                        ev[t] = ev[x]; mv[t] = mv[x]
                    else:
                        ev[t] = mv[x]; mv[t] = mv[x]
            L1 = L - 1
            if Wout == 6:
                for j in range(6):
                    Gout[a, b, j] = vals[L1, j]
            else:
                for j in range(3):
                    Gout[a, b, j] = vals[L1, j]
            Eout[a, b] = ev[L1]
            Mout[a, b] = mv[L1]


@njit(cache=True)
def _payoffs(G0, G1, Wd0, wts, Pay0, Pay1, FI0, FI1, FII0, FII1, FF, U0, U1, F0, F1):
    """U0[a, b], U1[b, a]: game payoffs with the forfeit convention; F0, F1: forfeit probabilities of a and b."""
    S0 = G0.shape[0]; S1 = G0.shape[1]
    for a in range(S0):
        for b in range(S1):
            u0 = 0.0; u1 = 0.0
            g1 = G1[b, a]
            f1 = g1[2]
            fa = 0.0
            for c in range(2):
                wc = wts[c]
                if wc == 0.0:
                    continue
                if Wd0 == 6:
                    g = G0[a, b, 3 * c:3 * c + 3]
                else:
                    g = G0[a, b, 0:3]
                fa += wc * g[2]
                for x in range(2):
                    gx = g[x]
                    if gx != 0.0:
                        for y in range(2):
                            gy = g1[y]
                            if gy != 0.0:
                                u0 += wc * gx * gy * Pay0[c, x, y]
                                u1 += wc * gx * gy * Pay1[c, x, y]
                        if f1 != 0.0:
                            u0 += wc * gx * f1 * FII0[c, x]
                            u1 += wc * gx * f1 * FII1[c, x]
                if g[2] != 0.0:
                    for y in range(2):
                        gy = g1[y]
                        if gy != 0.0:
                            u0 += wc * g[2] * gy * FI0[c, y]
                            u1 += wc * g[2] * gy * FI1[c, y]
                    if f1 != 0.0:
                        u0 += wc * g[2] * f1 * FF[0]
                        u1 += wc * g[2] * f1 * FF[1]
            U0[a, b] = u0
            U1[b, a] = u1
            F0[a, b] = fa
            F1[b, a] = f1


class Arm2:
    pass


def evaluate(lang, D, keep_prev=True, workmode=0):
    """Iterate levels 0..D for both roles; returns dict with G0 (S0, S1, W0), G1 (S1, S0, 3), E/M costs at D and the
    level D - 1 distributions (for the bounded-cr audit), and the game payoffs U0 (S0, S1), U1 (S1, S0)."""
    game = lang.game
    T, FI0, FI1, FII0, FII1, FF = game_tensors(game)
    g = GAMES[game]
    wts = g['weights']
    S0, S1 = lang.S0, lang.S1
    W0 = 6 if g['card'] else 3
    W1 = 3
    ta0, tl0 = lang.tape[0]; ta1, tl1 = lang.tape[1]
    G0 = [np.zeros((S0, S1, W0)), np.zeros((S0, S1, W0))]
    G1 = [np.zeros((S1, S0, W1)), np.zeros((S1, S0, W1))]
    E0 = [np.zeros((S0, S1)), np.zeros((S0, S1))]; M0 = [np.zeros((S0, S1)), np.zeros((S0, S1))]
    E1 = [np.zeros((S1, S0)), np.zeros((S1, S0))]; M1 = [np.zeros((S1, S0)), np.zeros((S1, S0))]
    cur = 0
    prev_G0 = prev_G1 = None
    for d in range(0, D + 1):
        nxt = 1 - cur
        # level d reads level d - 1 stored in slot `cur` (for d == 0 the slot is unused: applications forfeit)
        _eval_role(ta0, tl0, S0, S1, G1[cur], E1[cur], M1[cur], W1, d, G0[nxt], E0[nxt], M0[nxt], W0, T, wts, workmode)
        _eval_role(ta1, tl1, S1, S0, G0[cur], E0[cur], M0[cur], W0, d, G1[nxt], E1[nxt], M1[nxt], W1, T, wts, workmode)
        if d == D - 1:
            prev_G0 = G0[nxt].copy() if keep_prev else None
            prev_G1 = G1[nxt].copy() if keep_prev else None
        cur = nxt
    U0 = np.zeros((S0, S1)); U1 = np.zeros((S1, S0)); F0 = np.zeros((S0, S1)); F1 = np.zeros((S1, S0))
    _payoffs(G0[cur], G1[cur], W0, wts, g['Pay0'], g['Pay1'], FI0, FI1, FII0, FII1, FF, U0, U1, F0, F1)
    return dict(G0=G0[cur], G1=G1[cur], E0=E0[cur], E1=E1[cur], M0=M0[cur], M1=M1[cur], U0=U0, U1=U1, F0=F0, F1=F1,
                prevG0=prev_G0, prevG1=prev_G1)


# ---------------------------------------------------------------- arm: priced payoffs and behavioural classes
def _rows_hash(M, dec=9):
    R = np.round(M, dec) + 0.0
    hb = lambda v: hashlib.blake2b(np.ascontiguousarray(v).tobytes(), digest_size=16).digest()
    return [hb(R[i]) for i in range(R.shape[0])]


def collapse(lang, ev, c, dec=9):
    """Behavioural classes of both roles for the price c: programs with equal net-payoff rows and columns."""
    U0n = ev['U0'] - c * ev['E0']
    U1n = ev['U1'] - c * ev['E1']
    A = Arm2()
    A.lang, A.c = lang, c
    A.members, A.rep, A.mass, A.cls_of, A.K = [], [], [], [], []
    h0 = [a + b for a, b in zip(_rows_hash(U0n, dec), _rows_hash(U1n.T, dec))]
    h1 = [a + b for a, b in zip(_rows_hash(U1n, dec), _rows_hash(U0n.T, dec))]
    for r, h in ((0, h0), (1, h1)):
        d = {}
        for i, key in enumerate(h):
            d.setdefault(key, []).append(i)
        cl = []
        for members in d.values():
            rep = min(members, key=lambda p: (lang.size[lang.progs[r][p]], p))
            cl.append((rep, members, float(lang.mu[r][members].sum())))
        cl.sort(key=lambda t: (-t[2], t[0]))
        A.rep.append(np.array([t[0] for t in cl], np.int64))
        A.members.append([t[1] for t in cl])
        m = np.array([t[2] for t in cl]); A.mass.append(m / m.sum())
        co = np.empty(len(h), np.int64)
        for k, t in enumerate(cl):
            co[t[1]] = k
        A.cls_of.append(co)
        A.K.append(len(cl))
    r0, r1 = A.rep
    A.UA = np.round(U0n[np.ix_(r0, r1)], 12)
    A.UB = np.round(U1n[np.ix_(r1, r0)], 12)
    A.UAg = np.round(ev['U0'][np.ix_(r0, r1)], 12)
    A.UBg = np.round(ev['U1'][np.ix_(r1, r0)], 12)
    A.CA = ev['E0'][np.ix_(r0, r1)].copy()
    A.CB = ev['E1'][np.ix_(r1, r0)].copy()
    A.F0 = ev['F0'][np.ix_(r0, r1)].copy()
    A.F1 = ev['F1'][np.ix_(r1, r0)].copy()
    A.G0 = ev['G0'][np.ix_(r0, r1)].copy()
    A.G1 = ev['G1'][np.ix_(r1, r0)].copy()
    # bounded-cr audit: a program with `cr` reads its opponent on D - 1 levels; Dcr is 1 where that differs from the actual play
    d0 = np.abs(ev['prevG1'] - ev['G1']).max(-1) > 1e-9              # (S1, S0): b's distribution against a, level D - 1 vs D
    d1 = np.abs(ev['prevG0'] - ev['G0']).max(-1) > 1e-9              # (S0, S1)
    A.Dcr0 = (lang.has_cr[0][r0][:, None] & d0[np.ix_(r1, r0)].T).astype(np.float64)       # (K0, K1)
    A.Dcr1 = (lang.has_cr[1][r1][:, None] & d1[np.ix_(r0, r1)].T).astype(np.float64)       # (K1, K0)
    A.names = [[lang.src(lang.progs[r][p]) for p in A.rep[r]] for r in (0, 1)]
    A.sizes = [lang.size[lang.progs[r][A.rep[r]]] for r in (0, 1)]
    A.reader = [lang.has_app[r][A.rep[r]] for r in (0, 1)]
    A.exact_reader = [lang.has_cr[r][A.rep[r]] for r in (0, 1)]
    A.samp_reader = [(lang.has_if[r] | lang.has_sr[r])[A.rep[r]] for r in (0, 1)]
    return A


def build_arm(game, arm, n, D=12, prices=(0.0, 0.01), verbose=False, keep_ev=False):
    """Evaluate the program tables once, return {c: Arm2} plus the evaluation (program-level) when keep_ev."""
    import time
    t0 = time.time()
    lang = Lang2(game, arm, n)
    ev = evaluate(lang, D)
    if verbose:
        print('[%s %s n=%d] S0=%d S1=%d evaluated (%.0fs)' % (game, arm, n, lang.S0, lang.S1, time.time() - t0), flush=True)
    out = {}
    for c in prices:
        A = collapse(lang, ev, c)
        A.game, A.arm, A.n, A.D = game, arm, n, D
        out[c] = A
    return (out, ev, lang) if keep_ev else (out, None, lang)


# ---------------------------------------------------------------- lookup of programs by structure
def node_of(lang, r, t, spec):
    """Node id of an expression in context r and type t given as nested tuples: 'c0' 'c1' 'x';
    ('coin', a, b) ('card', a, b) ('cr', a) ('sr', a) ('srk', a) ('if', Q, A, B[, alpha]) with Q = ('me',) or ('up', B);
    the children carry their own type implicitly (a unary operator's child has type 1 - t, an `if`'s Q type 1 - r)."""
    if isinstance(spec, str):
        return lang.key[(spec, r, t)]
    h = spec[0]
    if h == 'coin':
        x = node_of(lang, r, t, spec[1]); y = node_of(lang, r, t, spec[2])
        if y < x:
            x, y = y, x
        return lang.key[('coin', r, t, x, y)]
    if h == 'card':
        return lang.key[('card', node_of(lang, r, t, spec[1]), node_of(lang, r, t, spec[2]))]
    if h in ('cr', 'sr', 'srk'):
        op = {'cr': OP_CR, 'sr': OP_SR, 'srk': OP_SRK}[h]
        return lang.key[('u', op, r, t, node_of(lang, r, 1 - t, spec[1]))]
    if h == 'me':
        return lang.key[('app', r, APP_ME, -1)]
    if h == 'up':
        return lang.key[('app', r, APP_UP, node_of(lang, r, r, spec[1]))]
    if h == 'if':
        Q = node_of(lang, r, 1 - r, spec[1]); x = node_of(lang, r, t, spec[2]); y = node_of(lang, r, t, spec[3])
        if len(spec) > 4 and spec[4] == 1:
            x, y = y, x
        return lang.key[('if', r, t, Q, x, y)]
    raise ValueError(spec)


def prog_of(lang, r, spec):
    """program index (within role r) of the program given by `spec` (see node_of)."""
    return int(lang.pidx[node_of(lang, r, r, spec)])


# the named programs of notes/mixed2.md section 1
APPME = ('me',)
NAMED_INSP = {
    0: {'I': 'c0', 'N': 'c1', 'X': 'x', 'P14': ('coin', 'c1', 'x'), 'P38': ('coin', 'x', ('coin', 'c1', 'x')),
        'P516': ('coin', 'x', ('coin', 'c1', ('coin', 'c1', 'x'))), 'P34': ('coin', 'c0', 'x'),
        'RI': ('if', APPME, 'c1', 'c0'),            # if THEM(ME) = C then N else I (inspect iff a sampled inspectee cheats)
        'CRI': ('cr', APPME)},
    1: {'C': 'c0', 'K': 'c1', 'X': 'x', 'CRC': ('cr', APPME), 'RC': ('if', APPME, 'c0', 'c1')},   # if THEM(ME) = I then C else K
}
NAMED_END = {
    0: {'BET': 'c0', 'CHECK': 'c1', 'XI': 'x', 'HON': ('card', 'c0', 'c1'), 'BL': ('card', 'c0', 'c0'),
        'EQ': ('card', 'c0', ('coin', 'x', 'c1')), 'EQ7': ('card', 'c0', ('coin', ('coin', 'c0', 'c1'), 'c1')),
        'EXP': ('card', 'c0', ('cr', APPME)), 'CRI': ('cr', APPME)},
    1: {'CALL': 'c0', 'FOLD': 'c1', 'X': 'x', 'CRII': ('cr', APPME), 'RII': ('if', APPME, 'c0', 'c1'),
        'SRII': ('sr', APPME)},
}


# ---------------------------------------------------------------- cached class tables
def _arm_path(game, arm, n, c, D):
    return os.path.join(CACHE, '%s_%s_n%d_D%d_c%g.npz' % (game, arm, n, D, c))


def save_arm(A, path):
    fl0 = np.concatenate([np.array(m, np.int64) for m in A.members[0]]); of0 = np.cumsum([0] + [len(m) for m in A.members[0]])
    fl1 = np.concatenate([np.array(m, np.int64) for m in A.members[1]]); of1 = np.cumsum([0] + [len(m) for m in A.members[1]])
    np.savez(path, rep0=A.rep[0], rep1=A.rep[1], fl0=fl0, of0=of0, fl1=fl1, of1=of1, mass0=A.mass[0], mass1=A.mass[1],
             UA=A.UA, UB=A.UB, UAg=A.UAg, UBg=A.UBg, CA=A.CA, CB=A.CB, F0=A.F0, F1=A.F1, G0=A.G0, G1=A.G1, Dcr0=A.Dcr0, Dcr1=A.Dcr1)


def load_arm(game, arm, n, c, D, path):
    z = np.load(path)
    lang = Lang2(game, arm, n)
    A = Arm2()
    A.lang, A.c, A.game, A.arm, A.n, A.D = lang, c, game, arm, n, D
    A.rep = [z['rep0'], z['rep1']]
    A.mass = [z['mass0'], z['mass1']]
    A.members = [[z['fl0'][z['of0'][i]:z['of0'][i + 1]].tolist() for i in range(len(z['of0']) - 1)],
                 [z['fl1'][z['of1'][i]:z['of1'][i + 1]].tolist() for i in range(len(z['of1']) - 1)]]
    A.K = [len(A.rep[0]), len(A.rep[1])]
    A.cls_of = []
    for r in (0, 1):
        co = np.empty(lang.S0 if r == 0 else lang.S1, np.int64)
        for k, m in enumerate(A.members[r]):
            co[m] = k
        A.cls_of.append(co)
    for k in ('UA', 'UB', 'UAg', 'UBg', 'CA', 'CB', 'F0', 'F1', 'G0', 'G1', 'Dcr0', 'Dcr1'):
        setattr(A, k, z[k])
    A.names = [[lang.src(lang.progs[r][p]) for p in A.rep[r]] for r in (0, 1)]
    A.sizes = [lang.size[lang.progs[r][A.rep[r]]] for r in (0, 1)]
    A.reader = [lang.has_app[r][A.rep[r]] for r in (0, 1)]
    A.exact_reader = [lang.has_cr[r][A.rep[r]] for r in (0, 1)]
    A.samp_reader = [(lang.has_if[r] | lang.has_sr[r])[A.rep[r]] for r in (0, 1)]
    return A


def get_arm(game, arm, n, c, D=12):
    """Class-level table of one cell, cached (the program-level evaluation is rebuilt only on a miss; a miss builds every
    price of the panel so that one evaluation serves all)."""
    os.makedirs(CACHE, exist_ok=True)
    path = _arm_path(game, arm, n, c, D)
    if os.path.exists(path):
        return load_arm(game, arm, n, c, D, path)
    prices = (0.0, 0.01, 0.001, 0.05)
    arms, _, _ = build_arm(game, arm, n, D, prices=prices)
    for pc, A in arms.items():
        pth = _arm_path(game, arm, n, pc, D)
        save_arm(A, pth + '.tmp.npz')
        os.replace(pth + '.tmp.npz', pth)
    return load_arm(game, arm, n, c, D, path)


# ---------------------------------------------------------------- class-level statistics
def named_idx(A):
    """class index of every named program (notes/mixed2.md section 1) present in the arm's grammar."""
    if getattr(A, '_named', None) is not None:
        return A._named
    lang = A.lang
    tabs = NAMED_INSP if A.game == 'insp' else NAMED_END
    out = {}
    for r in (0, 1):
        for k, spec in tabs[r].items():
            try:
                p = prog_of(lang, r, spec)
            except KeyError:
                continue
            out['%d:%s' % (r, k)] = int(A.cls_of[r][p])
    A._named = out
    return out


def _div(num, den):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(den > 1e-12, num / np.maximum(den, 1e-300), np.nan)


def island_stats(A, X0, X1, eq_p=(5 / 16, 3 / 8, 1 / 2)):
    """Statistics of populations X0 (I, K0), X1 (I, K1) (rows summing to one).  Returns a dict of arrays over rows."""
    I = X0.shape[0]
    card = GAMES[A.game]['card']
    out = {}
    UAx = X1 @ A.UA.T                       # (I, K0): net payoff of each role-0 class against the island's role-1 population
    UBx = X0 @ A.UB.T                       # (I, K1)
    out['u0'] = (X0 * UAx).sum(1); out['u1'] = (X1 * UBx).sum(1)
    out['u0g'] = (X0 * (X1 @ A.UAg.T)).sum(1); out['u1g'] = (X1 * (X0 @ A.UBg.T)).sum(1)
    out['cost0'] = out['u0g'] - out['u0']; out['cost1'] = out['u1g'] - out['u1']
    out['e0'] = UAx.max(1); out['e1'] = UBx.max(1)                       # net exploitability of the role-1 / role-0 population
    out['e0g'] = (X1 @ A.UAg.T).max(1); out['e1g'] = (X0 @ A.UBg.T).max(1)
    out['f0'] = (X0 * (X1 @ A.F0.T)).sum(1); out['f1'] = (X1 * (X0 @ A.F1.T)).sum(1)
    out['homo0'] = (X0 ** 2).sum(1); out['homo1'] = (X1 ** 2).sum(1)
    out['dis0'] = np.einsum('ia,ab,ib->i', X0, A.Dcr0, X1); out['dis1'] = np.einsum('ib,ba,ia->i', X1, A.Dcr1, X0)
    out['n0'] = (X0 > 0).sum(1).astype(float); out['n1'] = (X1 > 0).sum(1).astype(float)
    out['sup0'] = (X0 >= 0.05).sum(1).astype(float); out['sup1'] = (X1 >= 0.05).sum(1).astype(float)
    # action probabilities of every class against the island's other population (conditional on acting)
    G0, G1 = A.G0, A.G1
    d0 = X1 @ (1 - A.F0).T                  # (I, K0)
    d1 = X0 @ (1 - A.F1).T                  # (I, K1)
    if not card:
        p0 = _div(X1 @ G0[:, :, 0].T, d0)   # inspection: P(inspect)
        q1 = _div(X0 @ G1[:, :, 1].T, d1)   # P(cheat)
        key0, key1 = 'p_insp', 'q_cheat'
        win0 = None
    else:
        p0 = _div(X1 @ G0[:, :, 3].T, X1 @ (1 - G0[:, :, 5]).T)     # bluff probability with a loser
        win0 = _div(X1 @ G0[:, :, 0].T, X1 @ (1 - G0[:, :, 2]).T)   # bet probability with a winner
        q1 = _div(X0 @ G1[:, :, 0].T, d1)   # P(call)
        key0, key1 = 'bluff', 'call'
    w0 = np.where(np.isnan(p0), 0.0, X0); w0s = w0.sum(1)
    w1 = np.where(np.isnan(q1), 0.0, X1); w1s = w1.sum(1)
    out[key0] = _div((w0 * np.nan_to_num(p0)).sum(1), w0s); out[key1] = _div((w1 * np.nan_to_num(q1)).sum(1), w1s)
    if card:
        out['winbet'] = _div((w0 * np.nan_to_num(win0)).sum(1), w0s)
    p0n = np.nan_to_num(p0, nan=0.5); q1n = np.nan_to_num(q1, nan=0.5)
    out['mix0'] = (X0 * ((p0n > 0.02) & (p0n < 0.98))).sum(1)         # individual mixing (non-degenerate probability)
    out['mix1'] = (X1 * ((q1n > 0.02) & (q1n < 0.98))).sum(1)
    if not card:
        for nm, v in (('516', 5 / 16), ('38', 3 / 8), ('12', 1 / 2)):
            out['m_p' + nm] = (X0 * (np.abs(p0n - v) <= 5e-3)).sum(1)
        out['m_above'] = (X0 * (p0n > 0.25 + 5e-3)).sum(1); out['m_at'] = (X0 * (np.abs(p0n - 0.25) <= 5e-3)).sum(1)
        out['m_below'] = (X0 * (p0n < 0.25 - 5e-3)).sum(1)
        out['q_comply'] = (X1 * (q1n <= 0.02)).sum(1); out['q_cheater'] = (X1 * (q1n >= 0.98)).sum(1)
    else:
        out['m_bluff_eq'] = (X0 * (np.abs(p0n - 0.25) <= 0.1)).sum(1)
        out['m_call_eq'] = (X1 * (np.abs(q1n - 0.5) <= 0.1)).sum(1)
    # readers
    for r, X in ((0, X0), (1, X1)):
        out['rd%d' % r] = X @ A.reader[r].astype(float)
        out['rdx%d' % r] = X @ A.exact_reader[r].astype(float)
        out['rds%d' % r] = X @ A.samp_reader[r].astype(float)
    # behavioural reading: the class's action distribution varies across the opposing classes present (> 1e-6 in TV)
    for r, X, Xo, G in ((0, X0, X1, G0), (1, X1, X0, G1)):
        Kr = G.shape[0]
        beh = np.zeros(I)
        for i in range(I):
            po = np.nonzero(Xo[i] > 0)[0]
            if len(po) < 2:
                continue
            Gs = G[:, po, :]
            ref = Gs[:, :1, :]
            tv = 0.5 * np.abs(Gs - ref).sum(-1).max(1)
            beh[i] = X[i] @ (tv > 1e-6)
        out['reads%d' % r] = beh
    nm = named_idx(A)
    for k, c in nm.items():
        r = int(k[0])
        out['sh_' + k] = (X0 if r == 0 else X1)[:, c]
    # joint action table
    if not card:
        Jt = np.zeros((I, 2, 2))
        for x in range(2):
            for y in range(2):
                M = G0[:, :, x] * G1[:, :, y].T
                Jt[:, x, y] = np.einsum('ia,ab,ib->i', X0, M, X1)
        out['J'] = Jt
    else:
        Jt = np.zeros((I, 2, 2, 2))
        wts = GAMES['end']['weights']
        for c in range(2):
            for x in range(2):
                for y in range(2):
                    M = wts[c] * G0[:, :, 3 * c + x] * G1[:, :, y].T
                    Jt[:, c, x, y] = np.einsum('ia,ab,ib->i', X0, M, X1)
        out['J'] = Jt
    return out


def island_phase(st, game):
    """discrete phase label of each row: (inspector zone, inspectee zone, inspectee readers) for inspection."""
    if game != 'insp':
        return np.zeros(len(st['u0']), int)
    p = np.nan_to_num(st['p_insp'], nan=0.5); q = np.nan_to_num(st['q_cheat'], nan=0.5)
    zp = np.where(p > 0.30, 2, np.where(p < 0.15, 0, 1))
    zq = np.where(q < 0.1, 0, np.where(q > 0.5, 2, 1))
    rd = (st['rd1'] >= 0.5).astype(int)
    return zp * 6 + zq * 2 + rd


# ---------------------------------------------------------------- founders and the epsilon = 0 lottery
def length_prior_sizes(lang, r):
    a = lang.a_size[r]
    p = np.zeros(len(a))
    for s in range(1, len(a)):
        if a[s] > 0:
            p[s] = 1.0 / (2 * s * s)
    return p / p.sum()


def draw_founders(lang, r, cls_of, K, I, N, seed):
    """(I, K) founder class counts for role r.  Common random numbers: each slot draws a size (length prior) and a uniform
    quantile inside the size class (cumulative spelling multiplicity in canonical enumeration order)."""
    rng = np.random.default_rng(seed)
    u1 = rng.random(I * N); u2 = rng.random(I * N)
    ps = length_prior_sizes(lang, r)
    cdf = np.cumsum(ps)
    sz = np.minimum(np.searchsorted(cdf, u1, side='right'), len(ps) - 1)
    sz = np.where(ps[sz] > 0, sz, np.nonzero(ps)[0][0])
    prog = np.empty(I * N, np.int64)
    ids = lang.progs[r]
    for s in range(1, len(ps)):
        sel = np.nonzero(sz == s)[0]
        if len(sel) == 0:
            continue
        lst = np.nonzero(lang.size[ids] == s)[0]
        cm = np.cumsum(lang.mult[ids[lst]]); cm = cm / cm[-1]
        prog[sel] = lst[np.minimum(np.searchsorted(cm, u2[sel], side='right'), len(lst) - 1)]
    cl = cls_of[prog].reshape(I, N)
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        init[i] = np.bincount(cl[i], minlength=K)
    return init


@njit(cache=True)
def _sample2(counts, pay, i, p, pres, npres, N, w):
    m = -1e300
    for t in range(npres[i, p]):
        k = pres[i, p, t]
        f = pay[i, p, k] / N
        if f > m:
            m = f
    tot = 0.0
    for t in range(npres[i, p]):
        k = pres[i, p, t]
        tot += counts[i, p, k] * np.exp(w * (pay[i, p, k] / N - m))
    u = np.random.random() * tot
    acc = 0.0
    for t in range(npres[i, p]):
        k = pres[i, p, t]
        acc += counts[i, p, k] * np.exp(w * (pay[i, p, k] / N - m))
        if u <= acc:
            return k
    return pres[i, p, npres[i, p] - 1]


@njit(cache=True)
def lottery2(UA, UB, init0, init1, N, w, m, seed, cps):
    """eps = 0 islands, complete graph, two populations per island (fixed roles).  An event picks an island i and a role
    p; the child is drawn from the island's population p (or, with probability m, from a uniformly chosen other island)
    with weights count * exp(w * mean payoff against the other population); the victim is uniform in island i's
    population p.  A generation is 2 * I * N events.  Returns counts at the checkpoint generations cps."""
    np.random.seed(seed)
    I, K0 = init0.shape
    K1 = init1.shape[1]
    KM = max(K0, K1)
    counts = np.zeros((I, 2, KM), np.int64)
    pay = np.zeros((I, 2, KM))
    pres = np.zeros((I, 2, KM), np.int64); npres = np.zeros((I, 2), np.int64); pos = -np.ones((I, 2, KM), np.int64)
    for i in range(I):
        for k in range(K0):
            counts[i, 0, k] = init0[i, k]
        for k in range(K1):
            counts[i, 1, k] = init1[i, k]
        for p in range(2):
            Kp = K0 if p == 0 else K1
            for k in range(Kp):
                if counts[i, p, k] > 0:
                    pres[i, p, npres[i, p]] = k; pos[i, p, k] = npres[i, p]; npres[i, p] += 1
        for k in range(K0):
            s = 0.0
            for j in range(K1):
                s += counts[i, 1, j] * UA[k, j]
            pay[i, 0, k] = s
        for k in range(K1):
            s = 0.0
            for j in range(K0):
                s += counts[i, 0, j] * UB[k, j]
            pay[i, 1, k] = s
    ncp = len(cps)
    out0 = np.zeros((ncp, I, K0), np.int16)
    out1 = np.zeros((ncp, I, K1), np.int16)
    gens = cps[ncp - 1]
    ci = 0
    for g in range(gens):
        for e in range(2 * I * N):
            i = np.random.randint(I)
            p = np.random.randint(2)
            src = i
            if m > 0.0 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i:
                    src += 1
            child = _sample2(counts, pay, src, p, pres, npres, N, w)
            u = np.random.randint(N); acc = 0; victim = pres[i, p, 0]
            for t in range(npres[i, p]):
                k = pres[i, p, t]
                acc += counts[i, p, k]
                if u < acc:
                    victim = k
                    break
            if victim == child:
                continue
            counts[i, p, victim] -= 1
            if counts[i, p, victim] == 0:
                q = pos[i, p, victim]; last = pres[i, p, npres[i, p] - 1]
                pres[i, p, q] = last; pos[i, p, last] = q; pos[i, p, victim] = -1; npres[i, p] -= 1
            if counts[i, p, child] == 0:
                pres[i, p, npres[i, p]] = child; pos[i, p, child] = npres[i, p]; npres[i, p] += 1
            counts[i, p, child] += 1
            if p == 0:
                for k in range(K1):
                    pay[i, 1, k] += UB[k, child] - UB[k, victim]
            else:
                for k in range(K0):
                    pay[i, 0, k] += UA[k, child] - UA[k, victim]
        gg = g + 1
        while ci < ncp and gg == cps[ci]:
            for i in range(I):
                for k in range(K0):
                    out0[ci, i, k] = counts[i, 0, k]
                for k in range(K1):
                    out1[ci, i, k] = counts[i, 1, k]
            ci += 1
    return out0, out1


def run_seed(base, r):
    return zlib.crc32(('mixed2|%s|%d' % (base, r)).encode()) & 0x7fffffff


# ---------------------------------------------------------------- the epsilon -> 0 chain over pairs of monomorphic classes
def lrho(du, N, w=W):
    """log Moran fixation probability of one mutant under constant selection, fitness ratio exp(w du); vectorized."""
    dw = w * np.asarray(du, float)
    out = np.full(dw.shape, -math.log(N))
    pos = dw > 1e-12; neg = dw < -1e-12
    out[pos] = np.log(-np.expm1(-dw[pos])) - np.log(-np.expm1(-N * dw[pos]))
    a = -dw[neg]
    out[neg] = np.log(np.expm1(a)) - N * a - np.log(-np.expm1(-N * a))
    return out


def weak_graph_classes(UA, UB, tol=1e-9):
    """Closed communicating classes of the graph of weakly improving single-mutant moves on pairs (a, b); returns
    (label of every state, list of class dicts with kind in {'rest', 'drift', 'cycle'}, size)."""
    import scipy.sparse as sp, scipy.sparse.csgraph as csg
    K0, K1 = UA.shape
    S = K0 * K1
    rows, cols, strict = [], [], []
    ia = np.arange(K0)
    for b in range(K1):
        d1 = UA[:, b][None, :] - UA[:, b][:, None]                 # [a, q] = UA[q, b] - UA[a, b]
        a_, q_ = np.nonzero(d1 >= -tol)
        keep = a_ != q_
        a_, q_ = a_[keep], q_[keep]
        rows.append(a_ * K1 + b); cols.append(q_ * K1 + b); strict.append(d1[a_, q_] > tol)
    for a in range(K0):
        d2 = UB[:, a][None, :] - UB[:, a][:, None]                 # [b, q] = UB[q, a] - UB[b, a]
        b_, q_ = np.nonzero(d2 >= -tol)
        keep = b_ != q_
        b_, q_ = b_[keep], q_[keep]
        rows.append(a * K1 + b_); cols.append(a * K1 + q_); strict.append(d2[b_, q_] > tol)
    r = np.concatenate(rows); c = np.concatenate(cols); st = np.concatenate(strict)
    G = sp.csr_matrix((np.ones(len(r), np.int8), (r, c)), shape=(S, S))
    nc, lab = csg.connected_components(G, directed=True, connection='strong')
    leaving = np.zeros(nc, bool)
    cross = lab[r] != lab[c]
    leaving[lab[r[cross]]] = True
    inner_strict = np.zeros(nc, bool)
    ins = (~cross) & st
    inner_strict[lab[r[ins]]] = True
    size = np.bincount(lab, minlength=nc)
    classes = []
    for k in np.nonzero(~leaving)[0]:
        kind = 'cycle' if inner_strict[k] else ('rest' if size[k] == 1 else 'drift')
        classes.append(dict(label=int(k), size=int(size[k]), kind=kind))
    return lab, classes


class TwoPopChain:
    """Pruned log-domain chain on the K0 x K1 pairs of monomorphic role classes.  A pair (a, b) moves to (q, b) at rate
    mu0(q)/2 * rho(UA[q, b] - UA[a, b]) and to (a, q) at rate mu1(q)/2 * rho(UB[q, a] - UB[b, a]) per mutation event."""

    def __init__(self, A, N, w=W):
        self.A, self.N, self.w = A, N, w
        self.K0, self.K1 = A.K
        self.UA, self.UB = A.UA, A.UB
        self.lmu0 = np.log(0.5 * A.mass[0]); self.lmu1 = np.log(0.5 * A.mass[1])
        self.lm = np.add.outer(np.log(A.mass[0]), np.log(A.mass[1]))
        self.states = []
        self.pos = -np.ones(self.K0 * self.K1, np.int64)
        self.R = {}                       # state -> (L1 (K0), L2 (K1))

    def rates(self, s):
        a, b = divmod(s, self.K1)
        L1 = self.lmu0 + lrho(self.UA[:, b] - self.UA[a, b], self.N, self.w); L1[a] = -np.inf
        L2 = self.lmu1 + lrho(self.UB[:, a] - self.UB[b, a], self.N, self.w); L2[b] = -np.inf
        return L1, L2

    def add(self, s):
        if self.pos[s] < 0:
            self.pos[s] = len(self.states); self.states.append(int(s))
            self.R[int(s)] = self.rates(int(s))

    def solve(self):
        from chain_log import stationary_log
        n = len(self.states)
        LA = np.full((n, n), -np.inf)
        K1 = self.K1
        for i, s in enumerate(self.states):
            a, b = divmod(s, K1)
            L1, L2 = self.R[s]
            t1 = self.pos[np.arange(self.K0) * K1 + b]
            ok = (t1 >= 0) & np.isfinite(L1)
            LA[i, t1[ok]] = L1[ok]
            t2 = self.pos[a * K1 + np.arange(K1)]
            ok = (t2 >= 0) & np.isfinite(L2)
            LA[i, t2[ok]] = np.logaddexp(LA[i, t2[ok]], L2[ok])
        seed = np.array([self.lm[divmod(s, K1)] for s in self.states])
        lpi, info = stationary_log(LA, seed)
        return LA, lpi, info

    def inflows(self, lpi):
        """log flux from the explored states into every unexplored state, and the total log flux Sum_i pi_i R_i."""
        K0, K1 = self.K0, self.K1
        linf = np.full(K0 * K1, -np.inf)
        lflux = -np.inf
        for i, s in enumerate(self.states):
            if not np.isfinite(lpi[i]):
                continue
            a, b = divmod(s, K1)
            L1, L2 = self.R[s]
            lflux = np.logaddexp(lflux, lpi[i] + np.logaddexp.reduce(np.concatenate([L1[np.isfinite(L1)], L2[np.isfinite(L2)]])))
            idx1 = np.arange(K0) * K1 + b
            m1 = (self.pos[idx1] < 0) & np.isfinite(L1)
            linf[idx1[m1]] = np.logaddexp(linf[idx1[m1]], lpi[i] + L1[m1])
            idx2 = a * K1 + np.arange(K1)
            m2 = (self.pos[idx2] < 0) & np.isfinite(L2)
            linf[idx2[m2]] = np.logaddexp(linf[idx2[m2]], lpi[i] + L2[m2])
        return linf, lflux

    def explore(self, seeds, log_theta=math.log(1e-10), max_states=1500, max_add=400, verbose=False):
        for s in seeds:
            self.add(s)
        self.capped = False
        for rnd in range(200):
            LA, lpi, info = self.solve()
            n = len(self.states)
            linf, lflux = self.inflows(lpi)
            rel = linf - lflux
            cand = np.nonzero(rel > log_theta)[0]
            small = rel[(rel <= log_theta) & np.isfinite(rel)]
            self.log_cut = float(np.logaddexp.reduce(small)) if len(small) else -np.inf
            if verbose:
                print('    round %d: %d states, %d candidates, log10 cut %.1f, closed %d' % (
                    rnd, n, len(cand), self.log_cut / math.log(10) if np.isfinite(self.log_cut) else -999, info.get('n_closed', -1)), flush=True)
            if len(cand) == 0:
                break
            if n >= max_states:
                self.capped = True
                break
            cand = cand[np.argsort(-rel[cand])][:min(max_add, max_states - n)]
            for s in cand:
                self.add(int(s))
        LA, lpi, info = self.solve()
        self.LA, self.lpi, self.info = LA, lpi, info
        linf, lflux = self.inflows(lpi)
        fin = np.isfinite(linf)
        self.log_unexplored = float(np.logaddexp.reduce(linf[fin] - lflux)) if fin.any() else -np.inf     # relative flux leaving the explored set
        # circulation index: net flux around cycles over total flux, on the explored set (0 = detailed balance)
        n = len(self.states)
        Jf = np.exp(np.where(np.isfinite(LA), LA + lpi[:, None], -np.inf)) if n <= 3000 else None
        if Jf is not None:
            np.fill_diagonal(Jf, 0.0)
            tot = Jf.sum()
            self.circulation = float(np.abs(Jf - Jf.T).sum() / (2 * tot)) if tot > 0 else 0.0
        else:
            self.circulation = None
        return self
