"""Rock-paper-scissors with a compute price (spec specs/2026-10-23-rps-priced.md; notes notes/rps-priced.md;
predictions predictions/2026-10-23-rps-priced.md).

Library on top of `rps.py` (imported, not edited): the application-depth cost of every ordered pair of programs, the
priced payoff U_c = U - c * cost, behavioural classes recomputed from the priced payoff rows and columns, the class-level
statistics with net / gross exploitability and cost paid, the lottery kernel call with support tracking, and the
unpriced-versus-priced class split.

Cost semantics (notes §1.0).  For a body e of program a facing program b with d levels left:
    E_d(e)  application depth reached when e is played (own coins sampled; expectation over them);
    M_d(e)  application depth reached when e is evaluated exactly inside a `cr` (every coin branch explored; the deepest
            branch counts for the depth price, the sum of branches for the work price);
    THEM(arg), d >= 1: 1 + (E_{d-1} or M_{d-1}) of the opponent's body run against arg;  d = 0: 0 (a forfeit).
The depth cost of a against b is H(a, b) = E_D(body a; a, b); the work cost HW is the same with the sum over coin branches
in exact mode.  The forfeit-only cost is D * P(a forfeits against b).  Payoff of a against b: U(a, b) - c * cost(a, b);
the opponent's cost does not enter.
"""
import hashlib, math, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from numba import njit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rps as RP

ROOT = RP.ROOT
PCACHE = os.environ.get('RPS_PRICED_CACHE', os.path.join(os.environ.get('TMPDIR', '/tmp'), 'rps_priced_cache'))
KINDS = ('depth', 'work', 'forfeit')


# ---------------------------------------------------------------- the cost recursion
@njit(cache=True)
def _cost_depth(t_op, t_l, t_r, t_k, t_len, Eprev, Mprev, Eout, Mout, d, work):
    """Eout[a, b] = E_d(body a; a, b), Mout[a, b] = M_d(body a; a, b) for all pairs; Eprev, Mprev at d - 1."""
    S = t_op.shape[0]
    T = t_op.shape[1]
    ve = np.empty(T)
    vm = np.empty(T)
    for a in range(S):
        L = t_len[a]
        for b in range(S):
            for t in range(L):
                o = t_op[a, t]
                if o <= 3:
                    ve[t] = 0.0; vm[t] = 0.0
                elif o == 4 or o == 5:
                    c = t_l[a, t]
                    ve[t] = ve[c]; vm[t] = vm[c]
                elif o == 6:
                    c = t_l[a, t]
                    vm[t] = vm[c]; ve[t] = vm[c]
                elif o == 7:
                    c1 = t_l[a, t]; c2 = t_r[a, t]
                    ve[t] = 0.5 * (ve[c1] + ve[c2])
                    if work == 1:
                        vm[t] = vm[c1] + vm[c2]
                    else:
                        vm[t] = max(vm[c1], vm[c2])
                else:
                    if d == 0:
                        ve[t] = 0.0; vm[t] = 0.0
                    else:
                        k = t_k[a, t]
                        arg = a if k == 0 else (b if k == 1 else t_r[a, t])
                        ve[t] = 1.0 + Eprev[b, arg]
                        vm[t] = 1.0 + Mprev[b, arg]
            Eout[a, b] = ve[L - 1]
            Mout[a, b] = vm[L - 1]


def cost_table(lang, D, work=False):
    """H (S, S): the expected application depth (work = False) or the work (work = True) paid by the row program."""
    S = lang.S
    Ea = np.zeros((S, S)); Ma = np.zeros((S, S)); Eb = np.zeros((S, S)); Mb = np.zeros((S, S))
    args = (lang.t_op, lang.t_l, lang.t_r, lang.t_k, lang.t_len)
    w = 1 if work else 0
    _cost_depth(*args, Ea, Ma, Eb, Mb, 0, w)          # d = 0: nothing executes
    prevE, prevM, curE, curM = Eb, Mb, Ea, Ma
    for d in range(1, D + 1):
        _cost_depth(*args, prevE, prevM, curE, curM, d, w)
        prevE, curE = curE, prevE; prevM, curM = curM, prevM
    return prevE.copy(), prevM.copy()


def cost_table_subset(lang, Z, D, work=False):
    """The cost tables restricted to a program set Z that is closed under lifted arguments (every `THEM(^B)` of a member
    has B in Z).  Returns (E_D, M_D) over Z x Z in the order of Z."""
    Z = np.asarray(Z, np.int64)
    pos = -np.ones(lang.S, np.int64); pos[Z] = np.arange(len(Z))
    t_op = np.ascontiguousarray(lang.t_op[Z]); t_l = np.ascontiguousarray(lang.t_l[Z]); t_k = np.ascontiguousarray(lang.t_k[Z])
    t_len = np.ascontiguousarray(lang.t_len[Z]); t_r = np.ascontiguousarray(lang.t_r[Z])
    m = (t_op == RP.OP_APP) & (t_k == RP.K_UP)
    assert (pos[t_r[m]] >= 0).all(), 'Z is not closed under lifted arguments'
    t_r[m] = pos[t_r[m]]
    n = len(Z)
    Ea = np.zeros((n, n)); Ma = np.zeros((n, n)); Eb = np.zeros((n, n)); Mb = np.zeros((n, n))
    args = (t_op, t_l, t_r, t_k, t_len)
    w = 1 if work else 0
    _cost_depth(*args, Ea, Ma, Eb, Mb, 0, w)
    prevE, prevM, curE, curM = Eb, Mb, Ea, Ma
    for d in range(1, D + 1):
        _cost_depth(*args, prevE, prevM, curE, curM, d, w)
        prevE, curE = curE, prevE; prevM, curM = curM, prevM
    return prevE.copy(), prevM.copy()



def cost_ref(lang, a, b, D, work=False):
    """Slow recursive reference (pure python) of (E_D, M_D)(body a; a, b); the oracle for the tests.  Handles any tree,
    including bodies with several applications (n >= 7)."""
    memo = {}

    def go(a, b, d):
        key = (a, b, d)
        if key in memo:
            return memo[key]

        def ev(e, mode):               # mode 'E' play, 'M' exact
            o = lang.op[e]
            if o in (RP.OP_R, RP.OP_P, RP.OP_S, RP.OP_X):
                return 0.0
            if o in (RP.OP_NEXT, RP.OP_NEXT2):
                return ev(lang.l[e], mode)
            if o == RP.OP_CR:
                return ev(lang.l[e], 'M')
            if o == RP.OP_COIN:
                x, y = ev(lang.l[e], mode), ev(lang.r[e], mode)
                if mode == 'E':
                    return 0.5 * (x + y)
                return x + y if work else max(x, y)
            if o == RP.OP_APP:
                if d == 0:
                    return 0.0
                k = lang.k[e]
                arg = a if k == RP.K_ME else (b if k == RP.K_THEM else lang.r[e])
                return 1.0 + go(b, arg, d - 1)[0 if mode == 'E' else 1]
            raise ValueError(o)
        out = (ev(a, 'E'), ev(a, 'M'))
        memo[key] = out
        return out
    return go(a, b, D)


# ---------------------------------------------------------------- the base: game payoffs and costs for the full table
class Base:
    pass


def base_path(arm, n, D):
    os.makedirs(PCACHE, exist_ok=True)
    return os.path.join(PCACHE, '%s_n%d_D%d' % (arm, n, D))


def build_base(arm, n=6, D=12, verbose=False):
    """Evaluate the game table (rps.evaluate), the depth cost, the work cost and the forfeit mass of every ordered pair of
    programs, and cache them as .npy files (outside the repo)."""
    t0 = time.time()
    lang = RP.Lang(arm, n)
    G, _, Us = RP.evaluate(lang, D, keep_prev=False)
    U = Us[D]
    F = np.ascontiguousarray(G[:, :, 3])
    pth = base_path(arm, n, D)
    np.save(pth + '_G.npy', G)
    del G
    np.save(pth + '_U.npy', U); np.save(pth + '_F.npy', F)
    del U, F
    H, _ = cost_table(lang, D, work=False)
    np.save(pth + '_H.npy', H)
    del H
    HW, _ = cost_table(lang, D, work=True)
    np.save(pth + '_HW.npy', HW)
    del HW
    if verbose:
        print('[priced base %s n=%d D=%d] S=%d (%.0fs)' % (arm, n, D, lang.S, time.time() - t0), flush=True)


def load_base(arm, n=6, D=12, mmap=True):
    pth = base_path(arm, n, D)
    if not os.path.exists(pth + '_HW.npy'):
        build_base(arm, n, D, verbose=True)
    b = Base()
    mm = 'r' if mmap else None
    b.arm, b.n, b.D = arm, n, D
    b.lang = RP.Lang(arm, n)
    b.U = np.load(pth + '_U.npy', mmap_mode=mm)
    b.H = np.load(pth + '_H.npy', mmap_mode=mm)
    b.HW = np.load(pth + '_HW.npy', mmap_mode=mm)
    b.F = np.load(pth + '_F.npy', mmap_mode=mm)
    b.G = np.load(pth + '_G.npy', mmap_mode=mm)
    return b


# ---------------------------------------------------------------- priced classes
def price_matrix(base, c, kind='depth'):
    """The cost matrix c * cost(a, b) in payoff units (S, S)."""
    if kind == 'depth':
        return c * np.asarray(base.H)
    if kind == 'work':
        return c * np.asarray(base.HW)
    if kind == 'forfeit':
        return c * base.D * np.asarray(base.F)
    raise ValueError(kind)


def _classes_from_table(Un, dec, merge_tol=1e-11):
    """Group programs with equal rows and equal columns of Un (rounded to `dec` decimals), then merge groups whose
    representatives agree within merge_tol on every row and column entry (rounding-boundary splits).  Returns a list of
    member lists."""
    S = Un.shape[0]
    R = np.round(Un, dec) + 0.0
    hb = lambda v: hashlib.blake2b(np.ascontiguousarray(v).tobytes(), digest_size=16).digest()
    sig = {}
    for p in range(S):
        sig.setdefault((hb(R[p]), hb(R[:, p])), []).append(p)
    del R
    groups = list(sig.values())
    K = len(groups)
    if K > 1:
        rep = np.array([g[0] for g in groups])
        Rr = Un[rep]                         # (K, S) rows
        Cr = Un[:, rep].T                    # (K, S) columns
        rng = np.random.default_rng(5)
        v1 = rng.random(S); v2 = rng.random(S)
        proj = Rr @ v1 + Cr @ v2
        tolp = merge_tol * (v1.sum() + v2.sum()) * 4
        parent = list(range(K))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]; i = parent[i]
            return i
        order = np.argsort(proj)
        sp = proj[order]
        for ii in range(K):
            i = order[ii]
            jj = ii + 1
            while jj < K and sp[jj] - sp[ii] <= tolp:
                j = order[jj]
                if find(i) != find(j):
                    if np.abs(Rr[i] - Rr[j]).max() <= merge_tol and np.abs(Cr[i] - Cr[j]).max() <= merge_tol:
                        parent[find(j)] = find(i)
                jj += 1
        merged = {}
        for i in range(K):
            merged.setdefault(find(i), []).extend(groups[i])
        groups = [sorted(m) for m in merged.values()]
    return groups


class PArm(RP.Arm):
    pass


def make_arm(base, c, kind='depth', dec=None, mu_kind='bits'):
    """Priced class-level arm.  Classes: identical priced payoff rows and columns (rounded to `dec` decimals, 9 by default,
    6 at c = 0 to reproduce the unpriced classes).  Fields as `rps.Arm` plus Ug (game payoffs), Hc (cost in payoff
    units), cprice, kind, and the program-level class map."""
    lang = base.lang
    U = np.asarray(base.U)
    cost = price_matrix(base, c, kind)
    Un = U - cost
    if dec is None:
        dec = 6 if c == 0 else 9
    groups = _classes_from_table(Un, dec)
    mu = lang.mu if mu_kind == 'bits' else lang.mu_nodes
    classes = []
    for members in groups:
        rep = min(members, key=lambda p: (lang.size[p], p))
        classes.append((rep, members, float(mu[members].sum())))
    classes.sort(key=lambda t: (-t[2], t[0]))
    A = PArm()
    A.arm, A.n, A.D, A.lang, A.mu_kind = base.arm, base.n, base.D, lang, mu_kind
    A.cprice, A.kind = c, kind
    A.K = len(classes)
    A.rep = np.array([t[0] for t in classes], np.int64)
    A.members = [t[1] for t in classes]
    A.mass = np.array([t[2] for t in classes]); A.mass /= A.mass.sum()
    A.cls_of = np.empty(lang.S, np.int64)
    for k, m in enumerate(A.members):
        A.cls_of[m] = k
    A.names = [lang.src(r) for r in A.rep]
    ix = np.ix_(A.rep, A.rep)
    A.U = np.round(Un[ix], 12)
    A.Ug = np.round(U[ix], 12)
    A.Hc = cost[ix].copy()
    A.Gcl = np.asarray(base.G)[ix].copy()
    A.antisym_err = float(np.abs(A.Ug + A.Ug.T).max())
    A.diag_err = float(np.abs(np.diag(A.Ug)).max())
    # members of a class agree in priced payoff rows; their game payoffs and costs may differ separately (reported)
    dev = 0.0
    for k, m in enumerate(A.members):
        if len(m) > 1:
            sub = Un[np.ix_(m, A.rep)] - A.U[k][None, :]
            dev = max(dev, float(np.abs(sub).max()))
    A.member_row_dev = dev
    A.reader = np.zeros(A.K, bool); A.guarded = np.zeros(A.K, bool); A.has_cr = np.zeros(A.K, bool)
    for k, r in enumerate(A.rep):
        ops = lang.t_op[r, :lang.t_len[r]]
        A.reader[k] = bool((ops == RP.OP_APP).any())
        A.guarded[k] = bool((ops == RP.OP_COIN).any() and (ops == RP.OP_APP).any())
        A.has_cr[k] = bool((ops == RP.OP_CR).any())
    return A


def split_report(A_price, A_unpriced):
    """How the unpriced classes split under pricing: number of unpriced classes that split, the prior mass of the split
    classes, the largest number of pieces, and the priced classes that are unions of unpriced ones (should be none)."""
    lang = A_price.lang
    pieces = []
    mass_split = 0.0
    maxp = 0
    split_names = []
    for k, m in enumerate(A_unpriced.members):
        cl = set(int(A_price.cls_of[p]) for p in m)
        pieces.append(len(cl))
        if len(cl) > 1:
            mass_split += float(A_unpriced.mass[k]); maxp = max(maxp, len(cl))
            split_names.append((A_unpriced.names[k], len(cl), float(A_unpriced.mass[k])))
    merged = 0
    for k, m in enumerate(A_price.members):
        if len(set(int(A_unpriced.cls_of[p]) for p in m)) > 1:
            merged += 1
    split_names.sort(key=lambda t: -t[2])
    return dict(K_unpriced=int(A_unpriced.K), K_priced=int(A_price.K), n_unpriced_classes_split=int(sum(1 for x in pieces if x > 1)),
                prior_mass_of_split_classes=mass_split, max_pieces=int(maxp), priced_classes_that_merge_unpriced=int(merged),
                top_split=split_names[:10])


# ---------------------------------------------------------------- statistics
def state_stats_p(A, ids, x, nm=None, Aex=None, emap=None):
    """rps.state_stats plus the priced statistics.  e_prog is the NET exploitability (U_c); e_gross the game-payoff one."""
    st = RP.state_stats(A, ids, x, nm, Aex, emap)
    ids = np.asarray(ids, int); x = np.asarray(x, float); x = x / x.sum()
    st['e_gross'] = float((A.Ug[:, ids] @ x).max())
    st['e_indiv'] = float(x @ A.U[:, ids].max(0))
    st['e_indiv_gross'] = float(x @ A.Ug[:, ids].max(0))
    st['cost_paid'] = float(x @ A.Hc[np.ix_(ids, ids)] @ x)
    st['net_payoff'] = float(x @ A.U[np.ix_(ids, ids)] @ x)
    st['share_readers'] = float(x[A.reader[ids]].sum())
    st['share_guarded'] = float(x[A.guarded[ids]].sum())
    st['n_classes'] = int(len(ids))
    return st


def island_stats_p(A, counts, N, nm=None, Aex=None, emap=None):
    """Per-island statistics at one checkpoint (as rps.island_stats, with the priced extras)."""
    I = counts.shape[0]
    keys = ['e_prog', 'e_gross', 'e_indiv', 'e_indiv_gross', 'cost_paid', 'net_payoff', 'share_readers', 'share_guarded',
            'e_act', 'e_act_cond', 'forfeit_plays', 'forfeit_self', 'mix_pop', 'mix_self', 'regret', 'tv_marg', 'max_regret'] \
        + (['e_exset'] if Aex is not None else [])
    out = {k: np.zeros(I) for k in keys}
    out['nclass'] = np.zeros(I); out['homo'] = np.zeros(I)
    out['freqR'] = np.zeros(I); out['freqP'] = np.zeros(I); out['freqS'] = np.zeros(I)
    if nm is not None:
        for k in list(nm) + ['consts']:
            out['share_' + k] = np.zeros(I)
    for i in range(I):
        ids = np.nonzero(counts[i] > 0)[0]
        x = counts[i, ids] / counts[i].sum()
        st = state_stats_p(A, ids, x, nm, Aex, emap)
        for k in keys:
            if k in st:
                out[k][i] = st[k]
        out['nclass'][i] = len(ids); out['homo'][i] = float((x * x).sum())
        out['freqR'][i], out['freqP'][i], out['freqS'][i] = st['freq']
        if nm is not None:
            for k in list(nm) + ['consts']:
                out['share_' + k][i] = st['share_' + k]
    return out


class AexLite:
    """Class-level data of the priced exact arm needed for the exploiter-set control."""
    def __init__(self, lang, U, cls_of):
        self.lang, self.U, self.cls_of = lang, U, cls_of


def aex_path(c, kind, D, arm='exact', n=6):
    os.makedirs(PCACHE, exist_ok=True)
    return os.path.join(PCACHE, 'aex_%s_n%d_D%d_%s_c%s.npz' % (arm, n, D, kind, repr(c)))


def get_aex(c, kind='depth', D=12, n=6, arm='exact'):
    pth = aex_path(c, kind, D, arm, n)
    if not os.path.exists(pth):
        b = load_base(arm, n, D)
        A = make_arm(b, c, kind)
        np.savez(pth + '.tmp.npz', U=A.U, cls_of=A.cls_of)
        os.replace(pth + '.tmp.npz', pth)
        return AexLite(A.lang, A.U, A.cls_of)
    z = np.load(pth)
    return AexLite(RP.Lang(arm, n), z['U'], z['cls_of'])


def embed_priced(A, Aex):
    m = np.empty(A.K, np.int64)
    for k in range(A.K):
        m[k] = Aex.cls_of[Aex.lang.find(A.names[k].replace('next2(', 'next('))]
    return m


# ---------------------------------------------------------------- the lottery with support tracking
def support_class(counts_seq, N, thr=0.05):
    """counts_seq: (T, K) class counts of one island at equally spaced times.  Returns 'resolved' | 'cycling' |
    'unresolved' and the number of support changes."""
    cut = thr * N - 1e-9
    sups = [frozenset(np.nonzero(c >= cut)[0].tolist()) for c in counts_seq]
    changes = sum(1 for i in range(1, len(sups)) if sups[i] != sups[i - 1])
    if changes == 0:
        return 'resolved', 0
    seen = []
    cyc = False
    for s in sups:
        if not seen or s != seen[-1]:
            if s in seen:
                cyc = True
            seen.append(s)
    return ('cycling' if cyc else 'unresolved'), changes
