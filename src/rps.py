"""Rock-paper-scissors and mixed actions (spec specs/2026-10-23-rps-mixed.md; notes notes/rps.md; predictions
predictions/2026-10-23-rps.md).

Library: the RPS program grammar and its arms, the exact depth-capped evaluator over {R, P, S, forfeit}, behavioural
classes, the class-level statistics (exploitability, individual mixing, forfeit shares), the chain provider for
`chain_log.LogChain`, and the eps = 0 island lottery kernel (numba).

Programs are A-sort expressions (hash-consed); a program is identified with its body, because without `eq` behaviour
depends on the body only.  G_d(a, b) is the distribution over (R, P, S, F) of a's action against opponent b with d
levels of application left; an application met at depth 0 forfeits (F), or plays uniformly in the exact-uniform arm.
The payoff u(a, b) is the expectation over the product of G_D(a, b) and G_D(b, a) (independent coins); F loses to every
action and ties with F.  See notes/rps.md for the hand derivations the tests check.
"""
import math, os, sys, hashlib, zlib
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import tempfile
CACHE = os.environ.get('RPS_CACHE', os.path.join(tempfile.gettempdir(), 'rps_cache'))

# ---------------------------------------------------------------- opcodes
OP_R, OP_P, OP_S, OP_X, OP_NEXT, OP_NEXT2, OP_CR, OP_COIN, OP_APP = range(9)
K_ME, K_THEM, K_UP = range(3)
F = 3
# PAY[x][y]: payoff to the row action x against the column action y, actions (R, P, S, F)
PAY = np.array([[0, -1, 1, 1],
                [1, 0, -1, 1],
                [-1, 1, 0, 1],
                [-1, -1, -1, 0]], float)
UNI4 = np.array([1 / 3, 1 / 3, 1 / 3, 0.0])
W = 0.3
TIE = 1e-9

ARMS = {
    # name: atoms, unary slots (opcode per slot), coin, app, semantics flags
    'constants': dict(atoms=(OP_R, OP_P, OP_S), unary=(), coin=False, app=False, cap='forfeit', cr='cr'),
    'constx': dict(atoms=(OP_R, OP_P, OP_S, OP_X), unary=(), coin=False, app=False, cap='forfeit', cr='cr'),
    'pure': dict(atoms=(OP_R, OP_P, OP_S), unary=(OP_NEXT,), coin=False, app=True, cap='forfeit', cr='cr'),
    'sample': dict(atoms=(OP_R, OP_P, OP_S, OP_X), unary=(OP_NEXT,), coin=True, app=True, cap='forfeit', cr='cr'),
    'exact': dict(atoms=(OP_R, OP_P, OP_S, OP_X), unary=(OP_NEXT, OP_CR), coin=True, app=True, cap='forfeit', cr='cr'),
    'matched': dict(atoms=(OP_R, OP_P, OP_S, OP_X), unary=(OP_NEXT, OP_NEXT2), coin=True, app=True, cap='forfeit', cr='cr'),
    'exact_uniform': dict(atoms=(OP_R, OP_P, OP_S, OP_X), unary=(OP_NEXT, OP_CR), coin=True, app=True, cap='uniform', cr='cr'),
    'exact_br': dict(atoms=(OP_R, OP_P, OP_S, OP_X), unary=(OP_NEXT, OP_CR), coin=True, app=True, cap='forfeit', cr='br'),
}
ACTNAME = ('R', 'P', 'S', 'F')


# ---------------------------------------------------------------- language
class Lang:
    """Hash-consed A-sort expressions up to n nodes under an arm's grammar (weak-arm stripping: application is always
    `THEM(Q)` with Q in {ME, THEM, up(B)}; `ME(..)` and `(up A)(..)` are not enumerated)."""

    def __init__(self, arm, n=6):
        g = ARMS[arm]
        self.arm, self.n, self.g = arm, n, g
        self.op, self.l, self.r, self.k, self.size = [], [], [], [], []
        self.key = {}
        self.by_size = {s: [] for s in range(1, n + 1)}
        for s in range(1, n + 1):
            if s == 1:
                for o in g['atoms']:
                    self.add(o, -1, -1, -1, 1)
            else:
                for o in g['unary']:
                    for c in list(self.by_size[s - 1]):
                        self.add(o, c, -1, -1, s)
                if g['coin']:
                    for i in range(1, s - 1):
                        j = s - 1 - i
                        for a in list(self.by_size[i]):
                            for b in list(self.by_size[j]):
                                self.add(OP_COIN, a, b, -1, s)
                if g['app']:
                    if s == 3:
                        self.add(OP_APP, -1, -1, K_ME, 3)
                        self.add(OP_APP, -1, -1, K_THEM, 3)
                    if s >= 4:
                        for b in list(self.by_size[s - 3]):
                            self.add(OP_APP, -1, b, K_UP, s)
        self.S = len(self.op)
        self.op = np.array(self.op, np.int64); self.l = np.array(self.l, np.int64)
        self.r = np.array(self.r, np.int64); self.k = np.array(self.k, np.int64)
        self.size = np.array(self.size, np.int64)
        self.counts = np.bincount(self.size, minlength=n + 1)
        self._src = {}
        self._build_prior()
        self._build_tapes()

    def add(self, o, l, r, k, s):
        key = (o, l, r, k)
        if key in self.key:
            return self.key[key]
        e = len(self.op)
        self.op.append(o); self.l.append(l); self.r.append(r); self.k.append(k); self.size.append(s)
        self.key[key] = e
        self.by_size[s].append(e)
        return e

    # ---- prior
    def _build_prior(self):
        """mu(p) = 2^-bits, bits = log2 a(|p|) + 2 log2 |p| + 1 (the weak arm's length prior); mu_nodes = 2^-nodes."""
        sz = self.size
        a = self.counts
        bits = np.log2(a[sz]) + 2 * np.log2(sz) + 1
        mu = 2.0 ** (-bits)
        self.bits = bits
        self.mu = mu / mu.sum()
        mn = 2.0 ** (-sz.astype(float))
        self.mu_nodes = mn / mn.sum()

    # ---- tapes
    def _tape(self, e, out):
        o = self.op[e]
        if o in (OP_R, OP_P, OP_S, OP_X):
            out.append((o, -1, -1, -1)); return len(out) - 1
        if o in (OP_NEXT, OP_NEXT2, OP_CR):
            c = self._tape(self.l[e], out); out.append((o, c, -1, -1)); return len(out) - 1
        if o == OP_COIN:
            a = self._tape(self.l[e], out); b = self._tape(self.r[e], out)
            out.append((o, a, b, -1)); return len(out) - 1
        if o == OP_APP:
            out.append((o, -1, self.r[e], self.k[e])); return len(out) - 1
        raise ValueError(o)

    def _build_tapes(self):
        T = max(self.n, 1)
        S = self.S
        self.t_op = np.zeros((S, T), np.int64); self.t_l = np.zeros((S, T), np.int64)
        self.t_r = np.zeros((S, T), np.int64); self.t_k = np.zeros((S, T), np.int64)
        self.t_len = np.zeros(S, np.int64)
        self.reads_me = np.zeros(S, bool)
        for e in range(S):
            tp = []
            self._tape(e, tp)
            assert len(tp) <= T, (e, len(tp))
            self.t_len[e] = len(tp)
            for i, (o, a, b, k) in enumerate(tp):
                self.t_op[e, i], self.t_l[e, i], self.t_r[e, i], self.t_k[e, i] = o, a, b, k
                if o == OP_APP and k == K_ME:
                    self.reads_me[e] = True

    # ---- printing and lookup
    def src(self, e):
        if e in self._src:
            return self._src[e]
        o = self.op[e]
        if o == OP_R: s = 'R'
        elif o == OP_P: s = 'P'
        elif o == OP_S: s = 'S'
        elif o == OP_X: s = 'X'
        elif o == OP_NEXT: s = 'next(%s)' % self.src(self.l[e])
        elif o == OP_NEXT2: s = 'next2(%s)' % self.src(self.l[e])
        elif o == OP_CR: s = 'cr(%s)' % self.src(self.l[e])
        elif o == OP_COIN: s = 'coin(%s,%s)' % (self.src(self.l[e]), self.src(self.r[e]))
        elif o == OP_APP:
            k = self.k[e]
            s = 'THEM(ME)' if k == K_ME else ('THEM(THEM)' if k == K_THEM else 'THEM(^%s)' % self.src(self.r[e]))
        else:
            raise ValueError(o)
        self._src[e] = s
        return s

    def find(self, s):
        if not hasattr(self, '_rev'):
            self._rev = {self.src(e): e for e in range(self.S)}
        return self._rev[s]

    # ---- cyclic relabeling R -> P -> S -> R
    def relabel_map(self, shift=1):
        """sigma[e] = id of the expression with every atom R, P, S cyclically relabeled by `shift` (X fixed)."""
        sig = np.full(self.S, -1, np.int64)
        for e in range(self.S):           # children precede parents in id order (sizes ascend, children smaller)
            o = self.op[e]
            if o in (OP_R, OP_P, OP_S):
                sig[e] = self.key[((o + shift) % 3, -1, -1, -1)]
            elif o == OP_X:
                sig[e] = e
            elif o in (OP_NEXT, OP_NEXT2, OP_CR):
                sig[e] = self.key[(o, sig[self.l[e]], -1, -1)]
            elif o == OP_COIN:
                sig[e] = self.key[(o, sig[self.l[e]], sig[self.r[e]], -1)]
            else:
                k = self.k[e]
                sig[e] = self.key[(o, -1, sig[self.r[e]] if k == K_UP else -1, k)]
        return sig


# ---------------------------------------------------------------- evaluator
@njit(cache=True)
def _eval_depth(t_op, t_l, t_r, t_k, t_len, Gprev, Gout, d, cap_uniform, br_mode, tie):
    S = t_op.shape[0]
    T = t_op.shape[1]
    vals = np.empty((T, 4))
    for a in range(S):
        L = t_len[a]
        for b in range(S):
            for t in range(L):
                o = t_op[a, t]
                if o == 0:
                    vals[t, 0] = 1.0; vals[t, 1] = 0.0; vals[t, 2] = 0.0; vals[t, 3] = 0.0
                elif o == 1:
                    vals[t, 0] = 0.0; vals[t, 1] = 1.0; vals[t, 2] = 0.0; vals[t, 3] = 0.0
                elif o == 2:
                    vals[t, 0] = 0.0; vals[t, 1] = 0.0; vals[t, 2] = 1.0; vals[t, 3] = 0.0
                elif o == 3:
                    vals[t, 0] = 1.0 / 3; vals[t, 1] = 1.0 / 3; vals[t, 2] = 1.0 / 3; vals[t, 3] = 0.0
                elif o == 4 or o == 5:
                    c = t_l[a, t]
                    vals[t, 0] = vals[c, 2]; vals[t, 1] = vals[c, 0]; vals[t, 2] = vals[c, 1]; vals[t, 3] = vals[c, 3]
                elif o == 7:
                    c1 = t_l[a, t]; c2 = t_r[a, t]
                    for x in range(4):
                        vals[t, x] = 0.5 * (vals[c1, x] + vals[c2, x])
                elif o == 6:
                    c = t_l[a, t]
                    pf = vals[c, 3]
                    if pf >= 1.0 - 1e-15:
                        if br_mode == 1:
                            vals[t, 0] = 1.0 / 3; vals[t, 1] = 1.0 / 3; vals[t, 2] = 1.0 / 3; vals[t, 3] = 0.0
                        else:
                            vals[t, 0] = 0.0; vals[t, 1] = 0.0; vals[t, 2] = 0.0; vals[t, 3] = 1.0
                    else:
                        z = 1.0 - pf
                        dr = vals[c, 0] / z; dp = vals[c, 1] / z; ds = vals[c, 2] / z
                        u0 = ds - dp; u1 = dr - ds; u2 = dp - dr
                        mx = max(u0, max(u1, u2))
                        n0 = 1.0 if u0 >= mx - tie else 0.0
                        n1 = 1.0 if u1 >= mx - tie else 0.0
                        n2 = 1.0 if u2 >= mx - tie else 0.0
                        nn = n0 + n1 + n2
                        sc = 1.0 if br_mode == 1 else z
                        vals[t, 0] = sc * n0 / nn; vals[t, 1] = sc * n1 / nn; vals[t, 2] = sc * n2 / nn
                        vals[t, 3] = 0.0 if br_mode == 1 else pf
                else:  # application THEM(arg)
                    if d == 0:
                        if cap_uniform == 1:
                            vals[t, 0] = 1.0 / 3; vals[t, 1] = 1.0 / 3; vals[t, 2] = 1.0 / 3; vals[t, 3] = 0.0
                        else:
                            vals[t, 0] = 0.0; vals[t, 1] = 0.0; vals[t, 2] = 0.0; vals[t, 3] = 1.0
                    else:
                        k = t_k[a, t]
                        arg = a if k == 0 else (b if k == 1 else t_r[a, t])
                        for x in range(4):
                            vals[t, x] = Gprev[b, arg, x]
            for x in range(4):
                Gout[a, b, x] = vals[L - 1, x]


@njit(cache=True)
def _payoff(G, pay):
    S = G.shape[0]
    U = np.empty((S, S))
    for a in range(S):
        for b in range(S):
            s = 0.0
            for x in range(4):
                gx = G[a, b, x]
                if gx == 0.0:
                    continue
                for y in range(4):
                    s += gx * G[b, a, y] * pay[x, y]
            U[a, b] = s
    return U


def evaluate(lang, D, sweep=(), keep_prev=True):
    """Iterate G_0 .. G_D.  Returns (G_D, G_{D-1} or None, {d: U_d for d in sweep + (D,)}).  Memory: two (S,S,4)
    float64 arrays."""
    g = lang.g
    cap_u = 1 if g['cap'] == 'uniform' else 0
    br = 1 if g['cr'] == 'br' else 0
    S = lang.S
    Ga = np.zeros((S, S, 4)); Gb = np.zeros((S, S, 4))
    want = set(sweep) | {D}
    Us = {}
    _eval_depth(lang.t_op, lang.t_l, lang.t_r, lang.t_k, lang.t_len, Gb, Ga, 0, cap_u, br, TIE)
    cur, prev = Ga, Gb
    if 0 in want:
        Us[0] = _payoff(cur, PAY)
    for d in range(1, D + 1):
        cur, prev = prev, cur                      # prev := G_{d-1}; cur is overwritten with G_d
        _eval_depth(lang.t_op, lang.t_l, lang.t_r, lang.t_k, lang.t_len, prev, cur, d, cap_u, br, TIE)
        if d in want:
            Us[d] = _payoff(cur, PAY)
    return cur, (prev if keep_prev else None), Us


def evaluate_ref(lang, a, b, d, memo=None):
    """Slow recursive reference of G_d(a, b) (pure python; the oracle for the tests)."""
    if memo is None:
        memo = {}
    key = (a, b, d)
    if key in memo:
        return memo[key]
    g = lang.g

    def ev(e):
        o = lang.op[e]
        if o == OP_R: return np.array([1., 0, 0, 0])
        if o == OP_P: return np.array([0., 1, 0, 0])
        if o == OP_S: return np.array([0., 0, 1, 0])
        if o == OP_X: return UNI4.copy()
        if o in (OP_NEXT, OP_NEXT2):
            v = ev(lang.l[e]); return np.array([v[2], v[0], v[1], v[3]])
        if o == OP_COIN:
            return 0.5 * (ev(lang.l[e]) + ev(lang.r[e]))
        if o == OP_CR:
            v = ev(lang.l[e]); pf = v[3]
            if pf >= 1 - 1e-15:
                return UNI4.copy() if g['cr'] == 'br' else np.array([0., 0, 0, 1])
            c = v[:3] / (1 - pf)
            u = np.array([c[2] - c[1], c[0] - c[2], c[1] - c[0]])
            best = u >= u.max() - TIE
            tie = best / best.sum()
            if g['cr'] == 'br':
                return np.array([tie[0], tie[1], tie[2], 0.0])
            return np.array([(1 - pf) * tie[0], (1 - pf) * tie[1], (1 - pf) * tie[2], pf])
        if o == OP_APP:
            if d == 0:
                return UNI4.copy() if g['cap'] == 'uniform' else np.array([0., 0, 0, 1])
            k = lang.k[e]
            arg = a if k == K_ME else (b if k == K_THEM else lang.r[e])
            return evaluate_ref(lang, b, arg, d - 1, memo)
        raise ValueError(o)
    # NB: ev must see a's own tree; recursion on e uses (a, b) of this call
    out = ev(a)
    memo[key] = out
    return out


def payoff_ref(lang, a, b, D):
    ga = evaluate_ref(lang, a, b, D); gb = evaluate_ref(lang, b, a, D)
    return float(ga @ PAY @ gb)


# ---------------------------------------------------------------- classes and the arm object
class Arm:
    """Class-level data of one arm at (n, D): everything the chain, the lottery and the statistics need."""
    pass


def _tv(p, q):
    return 0.5 * np.abs(p - q).sum(-1)


def build_arm(arm, n=6, D=12, sweep=(), mu_kind='bits', verbose=False, sig_dec=6):
    """Evaluate the full program table and collapse to behavioural classes (identical payoff rows and columns)."""
    import time
    t0 = time.time()
    lang = Lang(arm, n)
    sw = {}
    for d in sweep:                      # other caps, one evaluation each (only their payoff tables are kept)
        if d == D:
            continue
        Gd, _, Ud = evaluate(lang, d, keep_prev=False)
        sw[d] = Ud[d]
        del Gd
    G, Gprev, Us = evaluate(lang, D)
    U = Us[D]
    Us.update(sw)
    if verbose:
        print('[%s n=%d D=%d] S=%d programs evaluated (%.0fs)' % (arm, n, D, lang.S, time.time() - t0), flush=True)
    mu = lang.mu if mu_kind == 'bits' else lang.mu_nodes
    A = Arm()
    A.arm, A.n, A.D, A.lang, A.mu_kind = arm, n, D, lang, mu_kind
    A.antisym_err = float(np.abs(U + U.T).max())
    A.diag_err = float(np.abs(np.diag(U)).max())
    # classes by payoff rows and columns (rounded)
    R = np.round(U, sig_dec) + 0.0
    sig = {}
    hb = lambda v: hashlib.blake2b(np.ascontiguousarray(v).tobytes(), digest_size=16).digest()
    for p in range(lang.S):
        sig.setdefault((hb(R[p]), hb(R[:, p])), []).append(p)
    classes = []
    for members in sig.values():
        rep = min(members, key=lambda p: (lang.size[p], p))
        classes.append((rep, members, float(mu[members].sum())))
    classes.sort(key=lambda c: (-c[2], c[0]))
    K = len(classes)
    A.K = K
    A.rep = np.array([c[0] for c in classes], np.int64)
    A.members = [c[1] for c in classes]
    A.mass = np.array([c[2] for c in classes])
    A.mass /= A.mass.sum()
    A.cls_of = np.empty(lang.S, np.int64)
    for c, m in enumerate(A.members):
        A.cls_of[m] = c
    A.names = [lang.src(r) for r in A.rep]
    A.U = np.round(U[np.ix_(A.rep, A.rep)], 12)
    A.Gcl = G[np.ix_(A.rep, A.rep)].copy()
    A.Gcl_prev = Gprev[np.ix_(A.rep, A.rep)].copy() if Gprev is not None else None
    # audit: members' action distributions against the representatives vs the representative's own
    dev = 0.0
    n_split = 0
    for c, m in enumerate(A.members):
        if len(m) == 1:
            continue
        sub = G[np.ix_(m, A.rep)] - A.Gcl[c][None, :, :]
        dev = max(dev, float(np.abs(sub).max()))
        if np.abs(sub).max() > 1e-9:
            n_split += 1
    A.member_dist_dev = dev
    A.n_classes_dist_split = n_split
    # a robustness look at the class signature rounding
    R5 = np.round(U, 5) + 0.0
    sig5 = set((hb(R5[p]), hb(R5[:, p])) for p in range(lang.S))
    A.K_dec5 = len(sig5)
    A.sweep_U = {d: u for d, u in Us.items() if d != D}
    A.U_full = U
    A.G_full_forfeit_mass = float(G[:, :, 3].mean())
    A.class_of_name = {}
    A.build_time = time.time() - t0
    del G, Gprev
    return A


def save_arm(A, path):
    flat = np.concatenate([np.array(m, np.int64) for m in A.members])
    off = np.cumsum([0] + [len(m) for m in A.members])
    np.savez(path, rep=A.rep, flat=flat, off=off, mass=A.mass, U=A.U, Gcl=A.Gcl,
             Gcl_prev=A.Gcl_prev if A.Gcl_prev is not None else np.zeros(0),
             scal=np.array([A.antisym_err, A.diag_err, A.member_dist_dev, A.n_classes_dist_split, A.K_dec5,
                            A.G_full_forfeit_mass, A.build_time]))


def load_arm(arm, n, D, mu_kind, path):
    z = np.load(path)
    lang = Lang(arm, n)
    A = Arm()
    A.arm, A.n, A.D, A.lang, A.mu_kind = arm, n, D, lang, mu_kind
    A.rep = z['rep']; A.mass = z['mass']; A.U = z['U']; A.Gcl = z['Gcl']
    A.Gcl_prev = z['Gcl_prev'] if z['Gcl_prev'].size else None
    off = z['off']; flat = z['flat']
    A.members = [flat[off[i]:off[i + 1]].tolist() for i in range(len(off) - 1)]
    A.K = len(A.rep)
    A.cls_of = np.empty(lang.S, np.int64)
    for c, m in enumerate(A.members):
        A.cls_of[m] = c
    A.names = [lang.src(r) for r in A.rep]
    sc = z['scal']
    A.antisym_err, A.diag_err, A.member_dist_dev, A.n_classes_dist_split, A.K_dec5, A.G_full_forfeit_mass, A.build_time = \
        sc[0], sc[1], sc[2], int(sc[3]), int(sc[4]), sc[5], sc[6]
    A.U_full = None
    A.sweep_U = {}
    return A


def get_arm(arm, n=6, D=12, mu_kind='bits', full=False):
    """Class-level arm data, cached in CACHE (the full program table is rebuilt only when full=True)."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, '%s_n%d_D%d_%s.npz' % (arm, n, D, mu_kind))
    if not full and os.path.exists(path):
        return load_arm(arm, n, D, mu_kind, path)
    if n >= 7:
        import rps_n7
        A = rps_n7.build_arm_blocked(arm, n, D, mu_kind=mu_kind, verbose=True)
    else:
        A = build_arm(arm, n, D, mu_kind=mu_kind)
    save_arm(A, path + '.tmp.npz')
    os.replace(path + '.tmp.npz', path)
    if not full:
        A.U_full = None
    return A


# ---------------------------------------------------------------- class-level statistics
def class_index(A, spec):
    """class id of the program with source string `spec`."""
    return int(A.cls_of[A.lang.find(spec)])


NAMED = {
    'R': 'R', 'P': 'P', 'S': 'S', 'X': 'X',
    'TM': 'THEM(ME)', 'N': 'next(THEM(ME))', 'N2': 'next(next(THEM(ME)))', 'C': 'cr(THEM(ME))',
    'GN': 'coin(X,next(THEM(ME)))', 'GC': 'coin(X,cr(THEM(ME)))', 'M': 'coin(R,P)',
    'TT': 'THEM(THEM)',
}


def named_classes(A):
    out = {}
    for k, s in NAMED.items():
        try:
            out[k] = class_index(A, s)
        except KeyError:
            pass
    return out


def const_mask(A):
    m = np.zeros(A.K, bool)
    for s in ('R', 'P', 'S'):
        m[class_index(A, s)] = True
    return m


def state_stats(A, ids, x, nm=None, Aex=None, emap=None):
    """Statistics of a class-level population (ids, x): all in-population quantities of the spec."""
    ids = np.asarray(ids, int); x = np.asarray(x, float)
    x = x / x.sum()
    U = A.U; G = A.Gcl
    ux = U[:, ids] @ x                                 # payoff of every class against the population
    e_prog = float(ux.max())
    arg_e = int(ux.argmax())
    Dpop = np.einsum('b,abk->ak', x, G[np.ix_(ids, ids)].reshape(len(ids), len(ids), 4))   # (m, 4): action dist vs population
    Q = x @ Dpop                                       # population play marginal over (R, P, S, F)
    self_dist = G[ids, ids]                            # (m, 4)
    resid_pay = ux[ids]
    out = dict(
        e_prog=e_prog, e_prog_arg=arg_e,
        regret=float(x @ (e_prog - resid_pay)),
        max_regret=float((e_prog - resid_pay).max()),
        forfeit_plays=float(Q[3]),
        forfeit_self=float(x @ self_dist[:, 3]),
        mix_pop=float(x @ (_tv(Dpop, UNI4) <= 0.05)),
        mix_self=float(x @ (_tv(self_dist, UNI4) <= 0.05)),
        tv_marg=float(_tv(Q, UNI4)),
    )
    # action exploitability (forfeit counted as a win for the constant) and its conditional-on-action version
    qa = Q[:3]
    ca = np.array([qa[2] - qa[1] + Q[3], qa[0] - qa[2] + Q[3], qa[1] - qa[0] + Q[3]])
    out['e_act'] = float(ca.max())
    if Q[3] < 1 - 1e-12:
        qc = qa / (1 - Q[3])
        out['e_act_cond'] = float(max(qc[2] - qc[1], qc[0] - qc[2], qc[1] - qc[0]))
        out['freq'] = [float(v) for v in qc]
    else:
        out['e_act_cond'] = float('nan'); out['freq'] = [float('nan')] * 3
    out['tv_self_play_uniform'] = float(x @ _tv(self_dist, UNI4))
    if Aex is not None:
        # exploiter set held fixed: the best any class of the exact grammar earns against this population
        out['e_exset'] = float((Aex.U[:, emap[ids]] @ x).max())
    if nm is not None:
        for k, c in nm.items():
            out['share_' + k] = float(x[ids == c].sum())
        cm = const_mask(A)
        out['share_consts'] = float(x[cm[ids]].sum())
    return out


def embed_classes(A, Aex):
    """class of the exact arm that has the same behaviour as each class of A's representative (next2 read as next)."""
    m = np.empty(A.K, np.int64)
    for c in range(A.K):
        m[c] = Aex.cls_of[Aex.lang.find(A.names[c].replace('next2(', 'next('))]
    return m


# ---------------------------------------------------------------- chain provider
class ClassProvider:
    """chain.Chain provider over the class-level payoff matrix (as fixed_role_chicken.ClassProvider)."""

    def __init__(self, U, mu):
        self.Ufull = np.round(np.asarray(U, float), 9)
        K = len(mu)
        self.classes = sorted([(c, [c], float(mu[c])) for c in range(K)], key=lambda c: -c[2])
        self._R = np.array([c[0] for c in self.classes])
        self._b = {}

    def prepare(self, support):
        pass

    def U(self, ids, sup=None):
        ids = [int(p) for p in ids]
        return self.Ufull[np.ix_(ids, ids)]

    def mutant_classes(self, support):
        return self.classes

    def blocks_for(self, support):
        sup = tuple(int(p) for p in support)
        b = self._b.get(sup)
        if b is None:
            si = np.array(sup, int); R = self._R
            b = (self.Ufull[np.ix_(R, si)], self.Ufull[np.ix_(si, R)], self.Ufull[R, R], self.Ufull[np.ix_(si, si)])
            self._b[sup] = b
        return b


# ---------------------------------------------------------------- the eps = 0 lottery
def length_prior_sizes(lang):
    """P(size = s) under the length prior (proportional to 1 / (2 s^2) over sizes present)."""
    a = lang.counts.astype(float)
    p = np.zeros(len(a))
    for s in range(1, len(a)):
        if a[s] > 0:
            p[s] = 1.0 / (2 * s * s)
    return p / p.sum()


def draw_founders(lang, cls_of, K, I, N, seed):
    """(I, K) founder counts.  Common random numbers: each slot draws a size (length prior) and a uniform u for the
    position inside the size class in canonical enumeration order, so arms sharing an enumeration order are paired."""
    rng = np.random.default_rng(seed)
    u1 = rng.random(I * N); u2 = rng.random(I * N)
    ps = length_prior_sizes(lang)
    cdf = np.cumsum(ps)
    sz = np.minimum(np.searchsorted(cdf, u1, side='right'), len(ps) - 1)
    sz = np.where(ps[sz] > 0, sz, 1)
    prog = np.empty(I * N, np.int64)
    for s in range(1, len(ps)):
        sel = np.nonzero(sz == s)[0]
        if len(sel) == 0:
            continue
        lst = np.array(lang.by_size[s], np.int64)
        prog[sel] = lst[np.minimum((u2[sel] * len(lst)).astype(np.int64), len(lst) - 1)]
    cl = cls_of[prog].reshape(I, N)
    init = np.zeros((I, K), np.int64)
    for i in range(I):
        init[i] = np.bincount(cl[i], minlength=K)
    return init


@njit(cache=True)
def _sample_parent(counts, paysum, U, pres, npres, isl, N, w):
    m = -1e300
    for t in range(npres[isl]):
        k = pres[isl, t]
        f = (paysum[isl, k] - U[k, k]) / (N - 1)
        if f > m: m = f
    tot = 0.0
    for t in range(npres[isl]):
        k = pres[isl, t]
        f = (paysum[isl, k] - U[k, k]) / (N - 1)
        tot += counts[isl, k] * np.exp(w * (f - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[isl]):
        k = pres[isl, t]
        f = (paysum[isl, k] - U[k, k]) / (N - 1)
        acc += counts[isl, k] * np.exp(w * (f - m))
        if u <= acc:
            return k
    return pres[isl, npres[isl] - 1]


@njit(cache=True)
def lottery_kernel(U, init, N, w, m, seed, cps, win0, win1, win_every):
    """eps = 0 islands on the complete graph (islands.py's kernel): each event a uniform victim on a uniform island is
    replaced by the offspring of a parent drawn (prob. proportional to count * exp(w * mean payoff against the other
    N - 1)) from its own island, or with probability m from a uniformly chosen other island.  A generation is I*N
    events.  cps: sorted checkpoint generations (counts recorded after that many generations).  Window statistics
    over generations in [win0, win1) every win_every generations: per-island sums of the number of classes alive and
    of the homozygosity sum (count/N)^2.  Returns (counts at checkpoints (ncp, I, K), nalive_sum (I), homo_sum (I),
    nwin)."""
    np.random.seed(seed)
    I, K = init.shape
    UT = np.ascontiguousarray(U.T)
    counts = init.copy()
    paysum = np.zeros((I, K))
    pres = np.zeros((I, K), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, K), np.int64)
    for i in range(I):
        for k in range(K):
            if counts[i, k] > 0:
                pres[i, npres[i]] = k; pos[i, k] = npres[i]; npres[i] += 1
                for j in range(K):
                    paysum[i, j] += counts[i, k] * U[j, k]
    ncp = len(cps)
    out = np.zeros((ncp, I, K), np.int64)
    nalive = np.zeros(I); homo = np.zeros(I); nwin = 0
    gens = cps[ncp - 1]
    ci = 0
    events_per_gen = I * N
    for g in range(gens):
        for e in range(events_per_gen):
            i = np.random.randint(I)
            src = i
            if np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i:
                    src += 1
            child = _sample_parent(counts, paysum, U, pres, npres, src, N, w)
            u = np.random.randint(N); acc = 0; victim = pres[i, 0]
            for t in range(npres[i]):
                k = pres[i, t]; acc += counts[i, k]
                if u < acc:
                    victim = k; break
            if victim == child:
                continue
            counts[i, victim] -= 1
            if counts[i, victim] == 0:
                p = pos[i, victim]; last = pres[i, npres[i] - 1]
                pres[i, p] = last; pos[i, last] = p; pos[i, victim] = -1; npres[i] -= 1
            if counts[i, child] == 0:
                pres[i, npres[i]] = child; pos[i, child] = npres[i]; npres[i] += 1
            counts[i, child] += 1
            for j in range(K):
                paysum[i, j] += UT[child, j] - UT[victim, j]
        gg = g + 1
        if gg >= win0 and gg < win1 and (gg - win0) % win_every == 0:
            for i in range(I):
                nalive[i] += npres[i]
                h = 0.0
                for t in range(npres[i]):
                    c = counts[i, pres[i, t]] / N
                    h += c * c
                homo[i] += h
            nwin += 1
        while ci < ncp and gg == cps[ci]:
            for i in range(I):
                for k in range(K):
                    out[ci, i, k] = counts[i, k]
            ci += 1
    return out, nalive, homo, nwin


def compress_run(init):
    """Restrict a run to the classes present among its founders: returns (idx of classes, init_local)."""
    idx = np.nonzero(init.sum(0) > 0)[0]
    return idx, np.ascontiguousarray(init[:, idx])


def run_seed(base, r):
    return zlib.crc32(('rps|%s|%d' % (base, r)).encode()) & 0x7fffffff


def island_stats(A, counts, N, nm=None, Aex=None, emap=None):
    """Per-island statistics at one checkpoint.  counts: (I, K) class counts.  Returns a dict of arrays over islands."""
    I = counts.shape[0]
    keys = ['e_prog', 'e_act', 'e_act_cond', 'forfeit_plays', 'forfeit_self', 'mix_pop', 'mix_self', 'regret', 'nclass', 'homo',
            'tv_marg', 'max_regret'] + (['e_exset'] if Aex is not None else [])
    out = {k: np.zeros(I) for k in keys}
    out['freqR'] = np.zeros(I); out['freqP'] = np.zeros(I); out['freqS'] = np.zeros(I)
    if nm is not None:
        for k in list(nm) + ['consts']:
            out['share_' + k] = np.zeros(I)
    for i in range(I):
        ids = np.nonzero(counts[i] > 0)[0]
        x = counts[i, ids] / counts[i].sum()
        st = state_stats(A, ids, x, nm, Aex, emap)
        for k in keys:
            if k in st:
                out[k][i] = st[k]
        out['nclass'][i] = len(ids); out['homo'][i] = float((x * x).sum())
        out['freqR'][i], out['freqP'][i], out['freqS'][i] = st['freq']
        if nm is not None:
            for k in list(nm) + ['consts']:
                out['share_' + k][i] = st['share_' + k]
    return out


# ---------------------------------------------------------------- cyclic symmetry checks
def symmetry_errors(A, shift=1):
    """Max |U[sigma a, sigma b] - U[a, b]| over the full program table, and the class-level action tensor error."""
    lang = A.lang
    sig = lang.relabel_map(shift)
    U = A.U_full
    err_U = float(np.abs(U[np.ix_(sig, sig)] - U).max())
    return err_U, sig


def class_perm(A, sig):
    """class-level permutation induced by a program relabeling (classes map to classes)."""
    perm = np.empty(A.K, np.int64)
    for c in range(A.K):
        img = set(int(A.cls_of[sig[p]]) for p in A.members[c])
        assert len(img) == 1, ('relabeling splits class', c, img)
        perm[c] = img.pop()
    return perm
