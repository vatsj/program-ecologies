"""Chicken and hawk-dove with fixed roles and without `ROLE` (spec specs/2026-10-11-fixed-role-chicken.md, reviewed by
gpt-6.1-sol; notes notes/fixed-role-chicken.md; predictions predictions/2026-10-11-fixed-role-chicken.md).

Core library: the three payoff tables, the class catalogues (weak, modal, W0, M0, const), the play-based outcome
classifier, the static program-space closure on the K^2 monomorphic pairs, the exact two-population eps -> 0 chain
(Lemma F of the notes: within a role selection is constant, so the chain is monomorphic per role and exact), the
one-population modal chain (seeded log-domain solver), and the eps = 0 island lottery (numba).

Levels: A_0 = Straight (hawk), A_1 = Swerve (dove).  S[a, b] = P(a swerves against b).  A role-1 class a against a
role-2 class b earns U[a, b], b earns U[b, a] (the games are symmetric and no program can read its role).
"""
import math, os, sys, json
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abm import njit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'fixed_role_chicken')
W = 0.3
TOL = 1e-9

# pay[a][b] = row player's payoff, level order (Straight, Swerve)
GAMES = {
    'chicken': np.array([[-10.0, 2.0], [-1.0, 0.0]]),     # games/chicken.yaml
    'hd3': np.array([[-0.5, 2.0], [0.0, 1.0]]),          # V = 2, C = 3
    'hd6': np.array([[-2.0, 2.0], [0.0, 1.0]]),          # V = 2, C = 6
}
GAME_NAMES = ('chicken', 'hd3', 'hd6')
ARMS = ('weak', 'modal', 'W0', 'M0', 'const')
LABELS = ('R1', 'R2', 'crash', 'dove', 'mixed')
R1, R2, CRASH, DOVE, MIXED = range(5)
CONV_TOL = 0.95


def tsrp(game):
    p = GAMES[game]
    return dict(T=float(p[0, 1]), S=float(p[1, 0]), P=float(p[0, 0]), R=float(p[1, 1]))


def benchmark(game):
    """payoff sum of a one-sided convention (T + S)."""
    t = tsrp(game)
    return t['T'] + t['S']


def fstar(game):
    """winner-seat bridge share above which a loser's Straight beats Swerve: (S - P)/(T - P)."""
    t = tsrp(game)
    return (t['S'] - t['P']) / (t['T'] - t['P'])


def xstar(game):
    t = tsrp(game)
    return (t['T'] - t['R']) / ((t['T'] - t['R']) + (t['S'] - t['P']))


# ------------------------------------------------------------------ play, payoff, classification
def payoff(S, game):
    """U[a, b] = expected payoff of a against b (independent evaluation of the two swerve probabilities)."""
    p = GAMES[game]
    s = np.asarray(S, float); t = s.T
    return (1 - s) * (1 - t) * p[0, 0] + (1 - s) * t * p[0, 1] + s * (1 - t) * p[1, 0] + s * t * p[1, 1]


def joint(S):
    """J[a, b, :] = P over (St,St), (St,Sw), (Sw,St), (Sw,Sw) for role-1 a against role-2 b (role-1 action first)."""
    s = np.asarray(S, float); t = s.T
    return np.stack([(1 - s) * (1 - t), (1 - s) * t, s * (1 - t), s * t], axis=-1)


def classify(J):
    """outcome class by play (notes 1.6) of an encounter distribution J (..., 4)."""
    J = np.asarray(J)
    out = np.full(J.shape[:-1], MIXED, np.int8)
    out[J[..., 3] >= CONV_TOL] = DOVE
    out[J[..., 0] >= CONV_TOL] = CRASH
    out[J[..., 2] >= CONV_TOL] = R2
    out[J[..., 1] >= CONV_TOL] = R1
    return out


def classify_onepop(J):
    """one population: crash / dove / asym (either asymmetric outcome) / mixed."""
    J = np.asarray(J)
    out = np.full(J.shape[:-1], 'mixed', dtype=object)
    out[J[..., 3] >= CONV_TOL] = 'dove'
    out[J[..., 0] >= CONV_TOL] = 'crash'
    out[(J[..., 1] + J[..., 2]) >= CONV_TOL] = 'asym'
    return out


# ------------------------------------------------------------------ catalogues
def _classes_from_S(S, mu_prog, bits, names_prog):
    R = np.round(S, 9)
    grp = defaultdict(list)
    for a in range(S.shape[0]):
        grp[(R[a].tobytes(), R[:, a].tobytes())].append(a)
    mem = list(grp.values())
    mu = np.array([mu_prog[m].sum() for m in mem])
    reps = [min(m, key=lambda a: (bits[a], a)) for m in mem]
    o = np.argsort(-mu, kind='stable')
    mem = [mem[i] for i in o]; reps = [reps[i] for i in o]
    return reps, mem, mu[o] / mu[o].sum()


def _weak_programs(x_on):
    from dsl import Language
    from game import Game
    from evaluate import square_chunked
    g = Game.load(os.path.join(ROOT, 'games', 'chicken_norole.yaml'))
    g.role = False; g.nroles = 1
    L = Language('weak', 6, k=2, names=('Straight', 'Swerve'), role=False, x_on=x_on)
    ids = L.ids()
    U, V, div = square_chunked(L, g, ids, rows=400)
    S = V[:, :, 0, 1]
    return L, ids, S, div


def _modal_programs(kinds):
    import modal as M
    L = M.ModalLanguage(6, kinds)
    val, nw = M.evaluate(L)
    return L, val.astype(float), nw


def _translate_w0_to_m0(L, ids, ML):
    """map every W0 program to its M0 canonical function (THEM(P) <-> BOX(THEM(P')))."""
    from dsl import CONST, NOT, AND, OR, APP, ME, THEM
    import modal as M
    memo = {}

    def tr(i):
        if i in memo:
            return memo[i]
        op = L.op[i]
        if op == CONST:
            c = ML.op('C' if L.lhs[i] == 1 else 'D')
        elif op == NOT:
            c = ML.op('not', tr(L.lhs[i]))
        elif op in (AND, OR):
            c = ML.op('and' if op == AND else 'or', tr(L.lhs[i]), tr(L.rhs[i]))
        elif op == APP:
            assert L.lhs[i] == THEM
            a = L.rhs[i]
            if a == ME:
                c = ML.op((0, 0, M.TM))
            elif a == THEM:
                c = ML.op((0, 0, M.TT))
            else:
                c = ML.op((0, 0, M.TL), tr(a))
        else:
            raise ValueError('unexpected op in W0: %d' % op)
        memo[i] = c
        return c
    return np.array([tr(int(i)) for i in ids], np.int64)


def build_catalogue(arm):
    """dict(arm, names, mu, sizes, S, iSt, iSw, [prog_mu, prog_cls, prog_cls_M0, prog_names]) -- computed."""
    if arm == 'const':
        return dict(arm=arm, names=['Straight', 'Swerve'], mu=np.array([0.5, 0.5]), sizes=np.array([1, 1]),
                    S=np.array([[0.0, 0.0], [1.0, 1.0]]), iSt=0, iSw=1, div=0.0, n_programs=2)
    if arm in ('weak', 'W0'):
        L, ids, S, div = _weak_programs(arm == 'weak')
        mu_p = L.mu[ids] / L.mu[ids].sum()
        reps, mem, mu = _classes_from_S(S, mu_p, L.bits[ids], None)
        names = [L.src(ids[r]) for r in reps]
        Sc = S[np.ix_(reps, reps)]
        cls_of = np.zeros(len(ids), np.int64)
        for c, m in enumerate(mem):
            cls_of[m] = c
        d = dict(arm=arm, names=names, mu=mu, sizes=np.array([len(m) for m in mem]), S=Sc, div=float(div), n_programs=int(len(ids)),
                 iSt=names.index('Straight'), iSw=names.index('Swerve'), prog_mu=mu_p, prog_cls=cls_of,
                 prog_names=[L.src(i) for i in ids])
        if arm == 'W0':
            import modal as M
            ML, val, nw = _modal_programs(((0, 0),))
            canon = _translate_w0_to_m0(L, ids, ML)
            m0 = build_catalogue('M0')
            # M0 class of each canonical function
            Sm = val
            Rm = np.round(Sm, 9)
            key_of = {}
            for c, rep in enumerate(m0['canon_reps']):
                key_of[(Rm[rep].tobytes(), Rm[:, rep].tobytes())] = c
            d['prog_cls_M0'] = np.array([key_of[(Rm[k].tobytes(), Rm[:, k].tobytes())] for k in canon], np.int64)
            d['prog_canon_M0'] = canon
        return d
    if arm in ('modal', 'M0'):
        kinds = ((0, 0), (1, 0), (0, 1), (1, 1)) if arm == 'modal' else ((0, 0),)
        L, S, nw = _modal_programs(kinds)
        mu_p = L.mu_canon / L.mu_canon.sum()
        reps, mem, mu = _classes_from_S(S, mu_p, L.bits_canon, None)
        names = [L.rep[r] for r in reps]
        Sc = S[np.ix_(reps, reps)]
        return dict(arm=arm, names=names, mu=mu, sizes=np.array([int(L.count_canon[m].sum()) for m in mem]), S=Sc, div=0.0,
                    n_programs=int(L.n_programs), iSt=names.index('D'), iSw=names.index('C'), worlds=int(nw), canon_reps=reps)
    raise ValueError(arm)


_CAT = {}


def catalogue(arm):
    """cached catalogue (runs/fixed_role_chicken/cat_<arm>.npz, gitignored)."""
    if arm in _CAT:
        return _CAT[arm]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'cat_%s.npz' % arm)
    if os.path.exists(path):
        z = np.load(path, allow_pickle=True)
        d = {k: (z[k].item() if z[k].dtype == object and z[k].shape == () else z[k]) for k in z.files}
        d['names'] = list(d['names']); d['arm'] = str(d['arm'])
        for k in ('iSt', 'iSw', 'n_programs'):
            d[k] = int(d[k])
        if 'prog_names' in d:
            d['prog_names'] = list(d['prog_names'])
    else:
        d = build_catalogue(arm)
        np.savez(path, **{k: (np.array(v, dtype=object) if isinstance(v, list) and k in ('names', 'prog_names') else
                              (np.array(v, dtype=object) if v is None else v)) for k, v in d.items()})
    d['tags'] = tags_of(d)
    d['K'] = len(d['names'])
    _CAT[arm] = d
    return d


def tags_of(d):
    """firm / swerver / bridge / matcher / mixed by play against the two constants (notes 1.2)."""
    S = d['S']; a = S[:, d['iSt']]; b = S[:, d['iSw']]
    t = np.full(len(a), 'mixed', dtype=object)
    t[(a < TOL) & (b < TOL)] = 'firm'
    t[(a > 1 - TOL) & (b > 1 - TOL)] = 'swerver'
    t[(a > 1 - TOL) & (b < TOL)] = 'bridge'
    t[(a < TOL) & (b > 1 - TOL)] = 'matcher'
    return t


def display_name(d, k):
    n = d['names'][k]
    if d['arm'] in ('modal', 'M0'):
        if n == 'C': return 'Swerve'
        if n == 'D': return 'Straight'
    return n


# ------------------------------------------------------------------ static: the Delta >= 0 graph on K^2 pairs
def delta_graph(U, tol=TOL):
    """edges (a,b) -> (q,b) with U[q,b] >= U[a,b] - tol and (a,b) -> (a,q) with U[q,a] >= U[b,a] - tol, q != a / b.
    Returns (src, dst, kind) with kind 0 neutral, 1 strict; state index a*K + b."""
    K = U.shape[0]
    src, dst, kind = [], [], []
    for a in range(K):
        for b in range(K):
            s = a * K + b
            d1 = U[:, b] - U[a, b]
            for q in np.nonzero(d1 >= -tol)[0]:
                if q == a: continue
                src.append(s); dst.append(q * K + b); kind.append(1 if d1[q] > tol else 0)
            d2 = U[:, a] - U[b, a]
            for q in np.nonzero(d2 >= -tol)[0]:
                if q == b: continue
                src.append(s); dst.append(a * K + q); kind.append(1 if d2[q] > tol else 0)
    return np.array(src, np.int64), np.array(dst, np.int64), np.array(kind, np.int8)


def closed_classes_delta(U, lab):
    """closed strongly connected classes of the Delta >= 0 graph, with the outcome labels they contain."""
    import scipy.sparse as sp, scipy.sparse.csgraph as csg
    K = U.shape[0]; n = K * K
    src, dst, kind = delta_graph(U)
    G = sp.csr_matrix((np.ones(len(src), np.int8), (src, dst)), shape=(n, n))
    nc, comp = csg.connected_components(G, directed=True, connection='strong')
    leaving = np.zeros(nc, bool)
    cr = comp[src] != comp[dst]
    leaving[comp[src[cr]]] = True
    out = []
    flat = lab.ravel()
    for c in range(nc):
        if leaving[c]:
            continue
        mem = np.nonzero(comp == c)[0]
        out.append(dict(size=int(len(mem)), labels=sorted({LABELS[int(flat[m])] for m in mem}), members=mem.tolist()[:50]))
    return out, (src, dst, kind)


def bfs_path(src, dst, kind, n, start, targets):
    """shortest Delta >= 0 path from start to any target state; returns list of (state, edge kind)."""
    from collections import deque
    adj = defaultdict(list)
    for s, t, k in zip(src.tolist(), dst.tolist(), kind.tolist()):
        adj[s].append((t, k))
    prev = {start: None}
    dq = deque([start])
    tg = set(targets)
    while dq:
        s = dq.popleft()
        if s in tg:
            path = []
            while s is not None:
                p = prev[s]
                path.append((s, p[1] if p else None))
                s = p[0] if p else None
            return path[::-1]
        for t, k in adj[s]:
            if t not in prev:
                prev[t] = (s, k); dq.append(t)
    return None


def static(arm, game):
    d = catalogue(arm)
    U = payoff(d['S'], game); J = joint(d['S']); lab = classify(J)
    K = d['K']; iSt, iSw = d['iSt'], d['iSw']; tg = d['tags']; mu = d['mu']
    res = dict(arm=arm, game=game, K=K, n_programs=d['n_programs'])
    # action-space strictness of the two constant conventions
    res['strict_action'] = dict(winner_dev=float(U[iSt, iSw] - U[iSw, iSw]), loser_dev=float(U[iSw, iSt] - U[iSt, iSt]))
    # neutral neighbourhoods of (St | Sw)
    win = np.nonzero(np.abs(U[:, iSw] - U[iSt, iSw]) <= TOL)[0]
    lose = np.nonzero(np.abs(U[:, iSt] - U[iSw, iSt]) <= TOL)[0]
    res['neutral_winner_seat'] = dict(n=int(len(win)), mass=float(mu[win].sum()), classes=[display_name(d, k) for k in win])
    res['neutral_loser_seat'] = dict(n=int(len(lose)), mass=float(mu[lose].sum()), classes=[display_name(d, k) for k in lose])
    res['strict_entrants'] = dict(winner=[display_name(d, q) for q in np.nonzero(U[:, iSw] > U[iSt, iSw] + TOL)[0]],
                                  loser=[display_name(d, q) for q in np.nonzero(U[:, iSt] > U[iSw, iSt] + TOL)[0]])
    res['tag_mass'] = {t: dict(n=int((tg == t).sum()), mass=float(mu[tg == t].sum())) for t in ('firm', 'swerver', 'bridge', 'matcher', 'mixed')}
    br = np.nonzero(tg == 'bridge')[0]
    res['bridges'] = [dict(name=display_name(d, k), mu=float(mu[k]), self_play=LABELS[int(lab[k, k])],
                           vs_Straight=float(d['S'][k, iSt]), vs_Swerve=float(d['S'][k, iSw])) for k in br]
    # bridge-resident (both seats of both conventions): payoff of the bridge and of the resident
    res['bridge_resident'] = [dict(name=display_name(d, k),
                                   winner_seat_vs_Swerve=dict(play=LABELS[int(lab[k, iSw])], u_bridge=float(U[k, iSw]), u_res=float(U[iSw, k])),
                                   loser_seat_vs_Straight=dict(play=LABELS[int(lab[iSt, k])], u_bridge=float(U[k, iSt]), u_res=float(U[iSt, k])),
                                   loser_Straight_vs_bridge_winner=float(U[iSt, k] - U[iSw, k]))
                              for k in br]
    res['bridge_bridge'] = [[LABELS[int(lab[a, b])] for b in br] for a in br]
    res['bridge_bridge_S'] = [['%.2f/%.2f' % (d['S'][a, b], d['S'][b, a]) for b in br] for a in br]
    # program-space closure: closed classes of the Delta >= 0 graph
    cc, (src, dst, kind) = closed_classes_delta(U, lab)
    res['closed_classes'] = [dict(size=c['size'], labels=c['labels'],
                                  members=['%s | %s' % (display_name(d, m // K), display_name(d, m % K)) for m in c['members'][:12]]) for c in cc]
    res['n_closed'] = len(cc)
    res['closed_with_convention'] = [c['labels'] for c in cc if 'R1' in c['labels'] or 'R2' in c['labels']]
    # shortest Delta >= 0 path from (St|Sw) to any R2 state
    flat = lab.ravel()
    tgt = np.nonzero(flat == R2)[0]
    p = bfs_path(src, dst, kind, K * K, iSt * K + iSw, tgt.tolist())
    res['escape_path'] = None if p is None else [dict(state='%s | %s' % (display_name(d, s // K), display_name(d, s % K)),
                                                      label=LABELS[int(flat[s])], edge=('neutral' if k == 0 else 'strict') if k is not None else None)
                                                 for s, k in p]
    return res


# ------------------------------------------------------------------ the two-population eps -> 0 chain (Lemma F)
def lrho(du, N, w=W):
    """log Moran fixation of one mutant under constant selection with fitness ratio exp(w du); vectorized."""
    dw = w * np.asarray(du, float)
    out = np.full(dw.shape, -math.log(N))
    pos = dw > 1e-12; neg = dw < -1e-12
    out[pos] = np.log(-np.expm1(-dw[pos])) - np.log(-np.expm1(-N * dw[pos]))
    a = -dw[neg]
    out[neg] = np.log(np.expm1(a)) - N * a - np.log(-np.expm1(-N * a))
    return out


@njit(cache=True)
def gth_dense(P):
    """stationary distribution of a row-stochastic matrix by GTH (no subtractions), in place on a copy."""
    n = P.shape[0]
    A = P.copy()
    for i in range(n):
        A[i, i] = 0.0
    s = np.zeros(n)
    for k in range(n - 1, 0, -1):
        sk = 0.0
        for j in range(k):
            sk += A[k, j]
        if sk <= 0.0:
            sk = 1e-300
        s[k] = sk
        for i in range(k):
            aik = A[i, k]
            if aik == 0.0:
                continue
            f = aik / sk
            for j in range(k):
                A[i, j] += f * A[k, j]
    x = np.zeros(n)
    x[0] = 1.0
    for k in range(1, n):
        v = 0.0
        for i in range(k):
            v += x[i] * A[i, k]
        x[k] = v / s[k]
    return x / x.sum()


def chain_logrates(U, mu, N, w=W):
    """L1[a, b, q] = log rate (a|b) -> (q|b), L2[a, b, q] = log rate (a|b) -> (a|q), per mutation event (a role is
    picked with probability 1/2, q ~ mu)."""
    K = U.shape[0]
    lmu = np.log(0.5 * np.asarray(mu, float))
    du1 = U.T[None, :, :] - U[:, :, None]          # [a, b, q] = U[q, b] - U[a, b]
    du2 = U.T[:, None, :] - U.T[:, :, None]        # [a, b, q] = U[q, a] - U[b, a]
    L1 = lrho(du1, N, w) + lmu[None, None, :]
    L2 = lrho(du2, N, w) + lmu[None, None, :]
    idx = np.arange(K)
    L1[idx, :, idx] = -np.inf
    L2[:, idx, idx] = -np.inf
    return L1, L2, du1, du2


def two_pop_chain(U, mu, N, w=W, rel_drop=1e-30):
    """exact K^2 chain; jump-chain GTH (linear, no subtractions; edges below rel_drop of a row's total dropped and the
    dropped flow reported as the cut); log pi = log pi_jump - log R."""
    K = U.shape[0]
    L1, L2, du1, du2 = chain_logrates(U, mu, N, w)
    mm = np.maximum(L1.max(axis=2), L2.max(axis=2))
    R = mm + np.log(np.exp(L1 - mm[:, :, None]).sum(axis=2) + np.exp(L2 - mm[:, :, None]).sum(axis=2))
    P1 = np.exp(L1 - R[:, :, None]); P2 = np.exp(L2 - R[:, :, None])
    dropped = (P1 * (P1 < rel_drop)).sum(axis=2) + (P2 * (P2 < rel_drop)).sum(axis=2)
    P1 = np.where(P1 < rel_drop, 0.0, P1); P2 = np.where(P2 < rel_drop, 0.0, P2)
    S = K * K
    P = np.zeros((S, S))
    idx = np.arange(K)
    for a in range(K):
        for b in range(K):
            s0 = a * K + b
            P[s0, idx * K + b] += P1[a, b]
            P[s0, a * K + idx] += P2[a, b]
    P /= P.sum(axis=1, keepdims=True)
    # put the most stable states last-eliminated: order by total exit rate, smallest first
    order = np.argsort(R.ravel(), kind='stable')
    xj = np.empty(S)
    xj[order] = gth_dense(np.ascontiguousarray(P[np.ix_(order, order)]))
    with np.errstate(divide='ignore'):
        lpi = np.log(np.maximum(xj, 0.0)) - R.ravel()
    lpi -= np.max(lpi)
    lpi -= np.log(np.exp(lpi).sum())
    return dict(lpi=lpi.reshape(K, K), logR=R, L1=L1, L2=L2, du1=du1, du2=du2, cut=float((xj * dropped.ravel()).sum()), xjump=xj.reshape(K, K))


def two_pop_chain_logcheck(U, mu, N, w=W):
    """independent check: dense log-domain GTH (chain_log.gth_log) on the full log generator (no dropping)."""
    from chain_log import gth_log, order_by_exit
    K = U.shape[0]
    L1, L2, _, _ = chain_logrates(U, mu, N, w)
    S = K * K
    LA = np.full((S, S), -np.inf)
    idx = np.arange(K)
    for a in range(K):
        for b in range(K):
            s0 = a * K + b
            LA[s0, idx * K + b] = np.logaddexp(LA[s0, idx * K + b], L1[a, b])
            LA[s0, a * K + idx] = np.logaddexp(LA[s0, a * K + idx], L2[a, b])
    np.fill_diagonal(LA, -np.inf)
    order, _ = order_by_exit(LA)
    lx = gth_log(LA[np.ix_(order, order)])
    out = np.empty(S); out[order] = lx
    return out.reshape(K, K)


def chain_summary(d, game, N, ch, top=12):
    """pi by outcome class, support, lumped flux between classes, convention exits (per unit mass, N-scaled) and
    their decomposition (winner a bridge or not), decisive edges with Delta, N*Delta and N*rho."""
    K = d['K']; U = payoff(d['S'], game); lab = classify(joint(d['S']))
    lpi = ch['lpi']; pi = np.exp(lpi)
    tg = d['tags']
    out = dict(arm=d['arm'], game=game, N=N, K=K, states=K * K, cut=ch['cut'])
    out['pi_by_class'] = {LABELS[c]: float(pi[lab == c].sum()) for c in range(5)}
    out['asym_R1_minus_R2'] = float(pi[lab == R1].sum() - pi[lab == R2].sum())
    order = np.argsort(-pi.ravel())[:top]
    out['support'] = [dict(state='%s | %s' % (display_name(d, s // K), display_name(d, s % K)), pi=float(pi.ravel()[s]),
                           label=LABELS[int(lab.ravel()[s])], tags='%s | %s' % (tg[s // K], tg[s % K])) for s in order]
    # flux: pi(s) * rate(s -> t); rates exp(L)
    flux = defaultdict(float)
    ex = dict(R1=defaultdict(float))
    edges = defaultdict(float)          # (label src, label dst, src state, mutant, role) -> flux
    lab_flat = lab.ravel()
    for a in range(K):
        for b in range(K):
            p = pi[a, b]
            if p < 1e-300:
                continue
            la = lab[a, b]
            for r, Lr in ((0, ch['L1']), (1, ch['L2'])):
                rates = np.exp(Lr[a, b])
                for q in np.nonzero(rates > 0)[0]:
                    t = (q, b) if r == 0 else (a, q)
                    lb = lab[t]
                    if lb != la:
                        f = p * rates[q]
                        flux[(LABELS[la], LABELS[lb])] += f
                        edges[(LABELS[la], LABELS[lb], a, b, q, r)] += f
    out['flux'] = [dict(src=x, dst=y, flux=f) for (x, y), f in sorted(flux.items(), key=lambda kv: -kv[1])[:20]]
    # convention exits: R1 (role 1 wins); R2 is its mirror
    m1 = float(pi[lab == R1].sum())
    tot = sum(f for (x, y), f in flux.items() if x == 'R1')
    out['exit_R1_per_mass'] = tot / m1 if m1 > 0 else float('nan')
    out['N_exit_R1'] = out['exit_R1_per_mass'] * N
    via_bridge = sum(f for (x, y, a, b, q, r), f in edges.items() if x == 'R1' and tg[a] == 'bridge')
    out['exit_R1_share_bridge_winner'] = via_bridge / tot if tot > 0 else float('nan')
    # decisive edges out of R1
    dec = sorted(((f, k) for k, f in edges.items() if k[0] == 'R1'), reverse=True)[:6]
    out['decisive_exit_edges'] = []
    for f, (x, y, a, b, q, r) in dec:
        du = ch['du1'][a, b, q] if r == 0 else ch['du2'][a, b, q]
        lr = lrho(np.array([du]), N)[0]
        out['decisive_exit_edges'].append(dict(src='%s | %s' % (display_name(d, a), display_name(d, b)), to=LABELS[lab[(q, b) if r == 0 else (a, q)]],
                                               mutant=display_name(d, q), role=r + 1, Delta=float(du), N_Delta=float(N * du), N_rho=float(N * math.exp(lr)),
                                               share=f / tot))
    # the feeder (neutral step into bridge-winner R1 states): flux from non-bridge-winner R1 states into bridge-winner R1 states
    feed = 0.0; feed_nrho = []
    for a in range(K):
        if tg[a] == 'bridge':
            continue
        for b in range(K):
            if lab[a, b] != R1 or pi[a, b] < 1e-300:
                continue
            for q in np.nonzero(tg == 'bridge')[0]:
                if lab[q, b] == R1:
                    feed += pi[a, b] * math.exp(ch['L1'][a, b, q])
    out['feeder_into_bridge_winner_per_mass'] = feed / m1 if m1 > 0 else float('nan')
    out['N_feeder'] = out['feeder_into_bridge_winner_per_mass'] * N
    # mean payoff and P(outcomes)
    J = joint(d['S'])
    out['E_outcome'] = {nm: float((pi * J[:, :, i]).sum()) for i, nm in enumerate(('StSt', 'StSw', 'SwSt', 'SwSw'))}
    out['efficiency'] = float((pi * (U + U.T)).sum() / benchmark(game))
    return out


# ------------------------------------------------------------------ one population (arm c): seeded log-domain chain
class ClassProvider:
    """chain.Chain provider over a class-level payoff matrix (as dollar_partitions.ClassProvider)."""
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


def onepop_state_stats(d, game, ids, x):
    ids = list(ids); x = np.asarray(x, float)
    S = d['S'][np.ix_(ids, ids)]
    J = np.einsum('a,b,abk->k', x, x, joint(S))
    U = payoff(d['S'], game)[np.ix_(ids, ids)]
    return dict(StSt=float(J[0]), asym=float(J[1] + J[2]), SwSw=float(J[3]), pay=float(x @ U @ x), cls=str(classify_onepop(J)))


def onepop_chain(arm, game, N, log_theta=math.log(1e-14), twins=True, max_states=3000, verbose=False):
    from chain_log import LogChain
    import solver_audit as SA
    d = catalogue(arm)
    U = payoff(d['S'], game); mu = d['mu']
    cands, counts = SA.enumerate_candidates_fast(np.round(U, 9), mu, keep_all=False)
    S1, n1, comp1 = SA.invasion_closure(np.round(U, 9), mu, max_nodes=2000)
    have = set(tuple(sorted(c['ids'])) for c in cands)
    for c in S1:
        if c['size'] >= 2 and tuple(sorted(c['ids'])) not in have:
            have.add(tuple(sorted(c['ids']))); cands.append(c)
    sel = [c for c in cands if c['status'] == 'stable' and c['size'] > 1]
    seeds = [(list(c['ids']), list(c['x'])) for c in sel]
    layer = [c['n_adv'] == 0 for c in sel]
    prov = ClassProvider(U, mu)
    ch = LogChain(prov, N=N, w=W, Ufull=prov.Ufull if twins else None, twins=twins, theta=1.0, max_states=10 ** 9)
    ch.explore_log(extra_states=seeds, log_theta=log_theta, max_states=max_states + len(seeds), verbose=verbose, layer_mask=layer)
    keys_all, lpi_all, info, out_un, rec = ch.solve_sparse()
    keys = [keys_all[i] for i in rec]
    lpi = lpi_all[rec]; pi = np.exp(lpi)
    res = dict(arm=arm, game=game, N=N, twins=twins, log10_theta=log_theta / math.log(10), n_candidates=len(cands),
               n_seeded=len(seeds), n_deep=sum(1 for c in cands if c.get('deep')), closure_nodes=n1, closure_complete=bool(comp1),
               n_states=len(keys), closed=info, log10_cut=float(ch.log_cut / math.log(10)) if np.isfinite(ch.log_cut) else None,
               n_cand_left=ch.n_cand_left)
    agg = defaultdict(float); pay = 0.0; Jtot = np.zeros(3)
    sup = []
    for k, p in zip(keys, pi):
        ids, x, kind = ch.states[k]
        st = onepop_state_stats(d, game, ids, x)
        agg[st['cls']] += p; pay += p * st['pay']
        Jtot += p * np.array([st['StSt'], st['asym'], st['SwSw']])
    for i in np.argsort(-pi)[:10]:
        ids, x, kind = ch.states[keys[i]]
        sup.append(dict(state=' + '.join('%s:%.3f' % (display_name(d, c), xi) for c, xi in zip(ids, x)), pi=float(pi[i]),
                        **onepop_state_stats(d, game, ids, x)))
    res.update(pi_by_class=dict(agg), pay_per_player=float(pay), StSt=float(Jtot[0]), asym=float(Jtot[1]), SwSw=float(Jtot[2]),
               efficiency=float(2 * pay / benchmark(game)), support=sup)
    # exits of the top state: per-event log10 rates
    LA, _ = ch.log_matrix(keys)
    top = int(np.argmax(lpi))
    row = LA[top]; fin = np.isfinite(row); fin[top] = False
    res['top_exit_log10'] = float(np.logaddexp.reduce(row[fin]) / math.log(10)) if fin.any() else None
    exs = []
    for j in np.argsort(-np.where(fin, row, -np.inf))[:5]:
        if not fin[j]:
            break
        ids, x, kind = ch.states[keys[j]]
        muts = sorted(ch.lmut.get((keys[top], keys[j]), {}).items(), key=lambda kv: -kv[1])[:3]
        exs.append(dict(to=' + '.join('%s:%.3f' % (display_name(d, c), xi) for c, xi in zip(ids, x)), log10_rate=float(row[j] / math.log(10)),
                        mutants=[(display_name(d, int(q)), float(v / math.log(10))) for q, v in muts]))
    res['top_exits'] = exs
    return res


# ------------------------------------------------------------------ the eps = 0 lottery (numba)
@njit(cache=True)
def _sample(counts, pay, i, p, pres, npres, N, w):
    m = -1e300
    for t in range(npres[i, p]):
        k = pres[i, p, t]
        f = pay[i, p, k] / N
        if f > m: m = f
    tot = 0.0
    for t in range(npres[i, p]):
        k = pres[i, p, t]
        tot += counts[i, p, k] * np.exp(w * (pay[i, p, k] / N - m))
    u = np.random.random() * tot; acc = 0.0
    for t in range(npres[i, p]):
        k = pres[i, p, t]
        acc += counts[i, p, k] * np.exp(w * (pay[i, p, k] / N - m))
        if u <= acc:
            return k
    return pres[i, p, npres[i, p] - 1]


@njit(cache=True)
def _frozen(counts, UA, UB, I, K, glob):
    """within each population the present classes have identical payoffs against every present class of the other
    population (per island if glob == 0, on the global present sets otherwise)."""
    if glob == 1:
        pres0 = np.zeros(K, np.bool_); pres1 = np.zeros(K, np.bool_)
        for i in range(I):
            for k in range(K):
                if counts[i, 0, k] > 0: pres0[k] = True
                if counts[i, 1, k] > 0: pres1[k] = True
        return _frozen_sets(pres0, pres1, UA, UB, K)
    for i in range(I):
        pres0 = counts[i, 0] > 0; pres1 = counts[i, 1] > 0
        if not _frozen_sets(pres0, pres1, UA, UB, K):
            return False
    return True


@njit(cache=True)
def _frozen_sets(pres0, pres1, UA, UB, K):
    a0 = -1
    for a in range(K):
        if not pres0[a]: continue
        if a0 < 0:
            a0 = a; continue
        for b in range(K):
            if pres1[b] and abs(UA[a, b] - UA[a0, b]) > 1e-9:
                return False
    b0 = -1
    for b in range(K):
        if not pres1[b]: continue
        if b0 < 0:
            b0 = b; continue
        for a in range(K):
            if pres0[a] and abs(UB[b, a] - UB[b0, a]) > 1e-9:
                return False
    return True


@njit(cache=True)
def sim_two_pop(UA, UB, init, N, w, m, gens, every, seed, swap, stop_frozen):
    """init (I, 2, K) counts; population 0 uses UA (UA[k, j] = payoff of pop-0 class k against pop-1 class j), pop 1
    uses UB.  An event picks an island and a role r uniformly; the population acted on is p = r ^ swap.  Returns the
    count snapshots (nsamp, I, 2, K) as int16, the number of samples filled and the generation the run stopped."""
    np.random.seed(seed)
    I, _, K = init.shape
    counts = init.copy()
    pay = np.zeros((I, 2, K))
    pres = np.zeros((I, 2, K), np.int64); npres = np.zeros((I, 2), np.int64); pos = -np.ones((I, 2, K), np.int64)
    for i in range(I):
        for p in range(2):
            for k in range(K):
                if counts[i, p, k] > 0:
                    pres[i, p, npres[i, p]] = k; pos[i, p, k] = npres[i, p]; npres[i, p] += 1
        for k in range(K):
            s0 = 0.0; s1 = 0.0
            for j in range(K):
                s0 += counts[i, 1, j] * UA[k, j]
                s1 += counts[i, 0, j] * UB[k, j]
            pay[i, 0, k] = s0; pay[i, 1, k] = s1
    nsamp = gens // every
    snap = np.zeros((nsamp, I, 2, K), np.int16)
    s = 0
    stop_g = gens
    for g in range(gens):
        for e in range(2 * I * N):
            i = np.random.randint(I)
            r = np.random.randint(2)
            p = r ^ swap
            src = i
            if m > 0.0 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            child = _sample(counts, pay, src, p, pres, npres, N, w)
            u = np.random.randint(N); acc = 0; victim = pres[i, p, 0]
            for t in range(npres[i, p]):
                k = pres[i, p, t]; acc += counts[i, p, k]
                if u < acc:
                    victim = k; break
            if victim == child:
                continue
            counts[i, p, victim] -= 1
            if counts[i, p, victim] == 0:
                q = pos[i, p, victim]; last = pres[i, p, npres[i, p] - 1]
                pres[i, p, q] = last; pos[i, p, last] = q; pos[i, p, victim] = -1; npres[i, p] -= 1
            if counts[i, p, child] == 0:
                pres[i, p, npres[i, p]] = child; pos[i, p, child] = npres[i, p]; npres[i, p] += 1
            counts[i, p, child] += 1
            o = 1 - p
            if o == 0:
                for k in range(K):
                    pay[i, 0, k] += UA[k, child] - UA[k, victim]
            else:
                for k in range(K):
                    pay[i, 1, k] += UB[k, child] - UB[k, victim]
        if (g + 1) % every == 0 and s < nsamp:
            for i in range(I):
                for p in range(2):
                    for k in range(K):
                        snap[s, i, p, k] = counts[i, p, k]
            s += 1
            if stop_frozen == 1:
                if _frozen(counts, UA, UB, I, K, 1 if m > 0.0 else 0):
                    stop_g = g + 1
                    for s2 in range(s, nsamp):
                        for i in range(I):
                            for p in range(2):
                                for k in range(K):
                                    snap[s2, i, p, k] = counts[i, p, k]
                    break
    return snap, s, stop_g


@njit(cache=True)
def sim_one_pop(U, init, N, w, m, gens, every, seed, stop_frozen):
    """one population per island (arm c): fitness = mean payoff against the other N - 1 residents."""
    np.random.seed(seed)
    I, K = init.shape
    counts = init.copy()
    pay = np.zeros((I, K))
    pres = np.zeros((I, K), np.int64); npres = np.zeros(I, np.int64); pos = -np.ones((I, K), np.int64)
    for i in range(I):
        for k in range(K):
            if counts[i, k] > 0:
                pres[i, npres[i]] = k; pos[i, k] = npres[i]; npres[i] += 1
        for k in range(K):
            v = 0.0
            for j in range(K):
                v += counts[i, j] * U[k, j]
            pay[i, k] = v
    nsamp = gens // every
    snap = np.zeros((nsamp, I, K), np.int16)
    s = 0; stop_g = gens
    for g in range(gens):
        for e in range(I * N):
            i = np.random.randint(I)
            src = i
            if m > 0.0 and np.random.random() < m:
                src = np.random.randint(I - 1)
                if src >= i: src += 1
            mx = -1e300
            for t in range(npres[src]):
                k = pres[src, t]
                f = (pay[src, k] - U[k, k]) / (N - 1)
                if f > mx: mx = f
            tot = 0.0
            for t in range(npres[src]):
                k = pres[src, t]
                tot += counts[src, k] * np.exp(w * ((pay[src, k] - U[k, k]) / (N - 1) - mx))
            uu = np.random.random() * tot; acc2 = 0.0; child = pres[src, npres[src] - 1]
            for t in range(npres[src]):
                k = pres[src, t]
                acc2 += counts[src, k] * np.exp(w * ((pay[src, k] - U[k, k]) / (N - 1) - mx))
                if uu <= acc2:
                    child = k; break
            u = np.random.randint(N); acc = 0; victim = pres[i, 0]
            for t in range(npres[i]):
                k = pres[i, t]; acc += counts[i, k]
                if u < acc:
                    victim = k; break
            if victim == child:
                continue
            counts[i, victim] -= 1
            if counts[i, victim] == 0:
                q = pos[i, victim]; last = pres[i, npres[i] - 1]
                pres[i, q] = last; pos[i, last] = q; pos[i, victim] = -1; npres[i] -= 1
            if counts[i, child] == 0:
                pres[i, npres[i]] = child; pos[i, child] = npres[i]; npres[i] += 1
            counts[i, child] += 1
            for k in range(K):
                pay[i, k] += U[k, child] - U[k, victim]
        if (g + 1) % every == 0 and s < nsamp:
            for i in range(I):
                for k in range(K):
                    snap[s, i, k] = counts[i, k]
            s += 1
            if stop_frozen == 1:
                fr = True
                if m > 0.0:
                    lo = 1e300; hi = -1e300
                    pr = np.zeros(K, np.bool_)
                    for i in range(I):
                        for k in range(K):
                            if counts[i, k] > 0: pr[k] = True
                    for a in range(K):
                        if not pr[a]: continue
                        for b in range(K):
                            if not pr[b]: continue
                            if U[a, b] < lo: lo = U[a, b]
                            if U[a, b] > hi: hi = U[a, b]
                    fr = hi - lo < 1e-12
                else:
                    for i in range(I):
                        lo = 1e300; hi = -1e300
                        for t in range(npres[i]):
                            a = pres[i, t]
                            for t2 in range(npres[i]):
                                b = pres[i, t2]
                                if U[a, b] < lo: lo = U[a, b]
                                if U[a, b] > hi: hi = U[a, b]
                        if hi - lo >= 1e-12:
                            fr = False; break
                if fr:
                    stop_g = g + 1
                    for s2 in range(s, nsamp):
                        for i in range(I):
                            for k in range(K):
                                snap[s2, i, k] = counts[i, k]
                    break
    return snap, s, stop_g


@njit(cache=True)
def e3_island(cnt0, cnt1, pool0, pool1, UA, UB, labpair, K):
    """E3 (notes 1.6): close Z under 'a pool class q of role r joins Z_r if U_r[q, b] >= U_r[z, b] - 1e-9 for some
    z in Z_r, b in Z_other'; resolved at O (0..3) if every pair of Z1 x Z2 has class O, else -1."""
    Z0 = cnt0 > 0
    Z1 = cnt1 > 0
    changed = True
    while changed:
        changed = False
        for q in range(K):
            if pool0[q] and not Z0[q]:
                ok = False
                for z in range(K):
                    if not Z0[z]: continue
                    for b in range(K):
                        if Z1[b] and UA[q, b] >= UA[z, b] - 1e-9:
                            ok = True; break
                    if ok: break
                if ok:
                    Z0[q] = True; changed = True
            if pool1[q] and not Z1[q]:
                ok = False
                for z in range(K):
                    if not Z1[z]: continue
                    for a in range(K):
                        if Z0[a] and UB[q, a] >= UB[z, a] - 1e-9:
                            ok = True; break
                    if ok: break
                if ok:
                    Z1[q] = True; changed = True
    o = -1
    for a in range(K):
        if not Z0[a]: continue
        for b in range(K):
            if not Z1[b]: continue
            l = labpair[a, b]
            if l == 4:
                return -1
            if o < 0:
                o = l
            elif l != o:
                return -1
    return o


def seed_counts(mu, I, N, rng, npop=2):
    mu = np.asarray(mu, float); mu = mu / mu.sum()
    if npop == 1:
        return np.stack([rng.multinomial(N, mu) for _ in range(I)]).astype(np.int64)
    out = np.zeros((I, 2, len(mu)), np.int64)
    for i in range(I):
        out[i, 0] = rng.multinomial(N, mu)
        out[i, 1] = rng.multinomial(N, mu)
    return out


def paired_seed_counts(d_w0, d_m0, I, N, rng):
    """matched control: seeds drawn as programs from the common prior, mapped to W0 and M0 classes."""
    pm = d_w0['prog_mu']; cw = d_w0['prog_cls']; cm = d_w0['prog_cls_M0']
    a = np.zeros((I, 2, d_w0['K']), np.int64); b = np.zeros((I, 2, d_m0['K']), np.int64)
    for i in range(I):
        for r in range(2):
            draw = rng.choice(len(pm), size=N, p=pm)
            np.add.at(a[i, r], cw[draw], 1)
            np.add.at(b[i, r], cm[draw], 1)
    return a, b


def forced_counts(d, I, N, beta, rng, bridges=True):
    """islands 0..I/2-1 at (Straight | Swerve), the rest at (Swerve | Straight); a fraction beta of each seat's founders
    are bridges drawn by mu among bridge classes (or, with bridges=False, that seat's constant: matched founder mass)."""
    K = d['K']; iSt, iSw = d['iSt'], d['iSw']
    br = np.nonzero(d['tags'] == 'bridge')[0]
    pb = d['mu'][br] / d['mu'][br].sum()
    out = np.zeros((I, 2, K), np.int64)
    nb = int(round(beta * N))
    for i in range(I):
        seats = (iSt, iSw) if i < I // 2 else (iSw, iSt)
        for r in range(2):
            out[i, r, seats[r]] += N - nb
            if bridges:
                np.add.at(out[i, r], br[rng.choice(len(br), size=nb, p=pb)], 1)
            else:
                out[i, r, seats[r]] += nb
    return out
