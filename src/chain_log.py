"""Log-domain attractor chain (the generalized seeded log-domain solver of the solver audit,
specs/2026-10-05-solver-audit.md).

`LogChain` is `chain.Chain` with the same transition model (the same replicator fates, the same targets, the same
truncation k* and the same lumped-resident Moran fixation formula), but every edge weight is also kept in the log
domain, so that no rate underflows, and the stationary distribution is computed by log-domain GTH (no subtractions)
on the closed class of the explored set.  Its `expand` fills `self.trans` exactly as `Chain.expand` does (the linear
weights), so the published linear solve of the *same* generator is available on the same object (identical rates).

Exploration modes:
  explore()          inherited: the published lazy linear-domain exploration (theta on linear stationary inflow)
  explore_log(...)   seeded: every monomorphic state and every given extra state (candidate supports) expanded,
                     one layer of targets of the extra states, then rounds on log-domain relative inflow > log_theta
  explore_closure()  every state reachable from the seeds (cap max_states)

Twin drift (an intervention, off by default): in a polymorphic state, a mutant q that is a payoff twin of resident r
(same payoffs against every resident and itself, both directions) replaces r at rate mu(q) / (x_r N), a complete
transition, instead of the chain's lumped-resident fate.

Solvers: `gth_log` (dense log-domain GTH, numba), `gth_mp` (the same elimination in mpmath at a given precision, for
validation), `stationary_log` (closed classes found first; GTH on each), `linear_stationary` (chain.Chain.stationary
on a given generator: the published linear solve).
"""
import math
from collections import defaultdict
import numpy as np
import scipy.sparse as sp
import scipy.sparse.csgraph as csg
from chain import Chain, fixation, njit

NEG = -np.inf


# ---------------------------------------------------------------- log fixation
@njit(cache=True)
def log_fixation(uqq, uqa, uaq, uaa, N, w, kstar):
    """log of chain.fixation (identical formula: Moran fixation of a single q against the lumped resident, f =
    exp(w payoff), truncated at kstar copies), computed without underflow."""
    if kstar <= 1:
        return 0.0
    acc = 0.0
    lmax = -1e300
    logs = np.empty(kstar - 1)
    for k in range(1, kstar):
        pq = (k - 1) / (N - 1) * uqq + (N - k) / (N - 1) * uqa
        pa = k / (N - 1) * uaq + (N - k - 1) / (N - 1) * uaa
        acc += w * (pa - pq)
        logs[k - 1] = acc
        if acc > lmax:
            lmax = acc
    s = 0.0
    for k in range(kstar - 1):
        s += np.exp(logs[k] - lmax)
    ls = lmax + np.log(s)
    # rho = 1 / (1 + e^ls)
    if ls > 0:
        return -(ls + np.log1p(np.exp(-ls)))
    return -np.log1p(np.exp(ls))


def lae(a, b):
    if a == NEG: return b
    if b == NEG: return a
    if a > b: return a + math.log1p(math.exp(b - a))
    return b + math.log1p(math.exp(a - b))


@njit(cache=True)
def _lae(a, b):
    if a == -np.inf: return b
    if b == -np.inf: return a
    if a > b: return a + np.log1p(np.exp(b - a))
    return b + np.log1p(np.exp(a - b))


# ---------------------------------------------------------------- GTH
@njit(cache=True)
def gth_log(LA):
    """Stationary log pi of an irreducible chain with log off-diagonal rates LA (-inf = no edge; diagonal ignored),
    by Grassmann-Taksar-Heyman state reduction in the log domain.  States are eliminated from the last index down;
    index 0 is eliminated last (put the most stable state there)."""
    n = LA.shape[0]
    A = LA.copy()
    for i in range(n):
        A[i, i] = -np.inf
    s = np.full(n, -np.inf)
    for k in range(n - 1, 0, -1):
        sk = -np.inf
        for j in range(k):
            sk = _lae(sk, A[k, j])
        if sk == -np.inf:
            sk = -1e300
        s[k] = sk
        for i in range(k):
            aik = A[i, k]
            if aik == -np.inf:
                continue
            f = aik - sk
            for j in range(k):
                if j == i:
                    continue
                if A[k, j] != -np.inf:
                    A[i, j] = _lae(A[i, j], f + A[k, j])
    x = np.full(n, -np.inf)
    x[0] = 0.0
    for k in range(1, n):
        v = -np.inf
        for i in range(k):
            if A[i, k] != -np.inf and x[i] != -np.inf:
                v = _lae(v, x[i] + A[i, k])
        x[k] = v - s[k]
    m = x.max()
    z = 0.0
    for i in range(n):
        if x[i] != -np.inf:
            z += np.exp(x[i] - m)
    return x - m - np.log(z)


def gth_mp(LA, dps=50):
    """The same GTH elimination in mpmath at `dps` digits (exact up to dps for any exponent range).  Returns log pi
    as floats (mpf logs)."""
    import mpmath as mp
    mp.mp.dps = dps
    n = LA.shape[0]
    A = [[mp.mpf(0) if (i == j or not np.isfinite(LA[i, j])) else mp.exp(mp.mpf(float(LA[i, j]))) for j in range(n)] for i in range(n)]
    s = [mp.mpf(0)] * n
    for k in range(n - 1, 0, -1):
        sk = mp.fsum(A[k][j] for j in range(k))
        s[k] = sk
        for i in range(k):
            aik = A[i][k]
            if aik == 0:
                continue
            f = aik / sk
            for j in range(k):
                if j != i and A[k][j] != 0:
                    A[i][j] += f * A[k][j]
    x = [mp.mpf(0)] * n
    x[0] = mp.mpf(1)
    for k in range(1, n):
        x[k] = mp.fsum(x[i] * A[i][k] for i in range(k)) / s[k]
    z = mp.fsum(x)
    return np.array([float(mp.log(v / z)) if v > 0 else -np.inf for v in x])


def order_by_exit(LA):
    """indices sorted by total log exit rate, smallest first (eliminated last in GTH)."""
    n = LA.shape[0]
    lex = np.full(n, -1e300)
    for i in range(n):
        r = LA[i][np.isfinite(LA[i])]
        r = r[np.arange(len(r))]  # copy
        if len(r):
            lex[i] = np.logaddexp.reduce(r)
    return np.argsort(lex, kind='stable'), lex


def closed_classes(LA):
    """strongly connected components of the finite-edge graph, and which are closed (no edge leaving)."""
    n = LA.shape[0]
    fin = np.isfinite(LA)
    np.fill_diagonal(fin, False)
    G = sp.csr_matrix(fin.astype(np.int8))
    nc, lab = csg.connected_components(G, directed=True, connection='strong')
    r, c = np.nonzero(fin)
    leaving = np.zeros(nc, bool)
    leaving[lab[r[lab[r] != lab[c]]]] = True
    return nc, lab, [k for k in range(nc) if not leaving[k]]


def stationary_log(LA, seed_logw=None):
    """log pi for a chain with log rates LA.  If the finite-edge graph has one closed class, GTH on it (transient
    states get -inf).  If several, each is solved separately and weighted by the absorption probability from the
    seed distribution (computed in the log domain by GTH on the chain with closed classes collapsed to absorbing
    states is not needed: absorption is done by linear solves in a scaled form); the result is flagged."""
    n = LA.shape[0]
    nc, lab, closed = closed_classes(LA)
    lpi = np.full(n, NEG)
    info = dict(n_components=int(nc), n_closed=len(closed))
    if len(closed) == 1:
        mem = np.nonzero(lab == closed[0])[0]
        sub = LA[np.ix_(mem, mem)]
        order, _ = order_by_exit(sub)
        lx = gth_log(sub[np.ix_(order, order)])
        out = np.empty(len(mem)); out[order] = lx
        lpi[mem] = out
        return lpi, info
    # several closed classes: absorption from the seed distribution (scaled per row), then GTH inside each
    info['multiple_closed'] = True
    trans = np.nonzero(~np.isin(lab, closed))[0]
    W = np.zeros(len(closed))
    if seed_logw is None:
        seed_logw = np.zeros(n)
    seed = np.exp(seed_logw - np.max(seed_logw))
    # rows scaled by their total exit: jump chain
    tot = np.array([np.logaddexp.reduce(LA[i][np.isfinite(LA[i])]) if np.isfinite(LA[i]).any() else NEG for i in range(n)])
    P = np.zeros((n, n))
    for i in range(n):
        if np.isfinite(tot[i]):
            fi = np.isfinite(LA[i]); fi[i] = False
            P[i, fi] = np.exp(LA[i, fi] - tot[i])
    T = trans
    H = np.zeros((n, len(closed)))
    for ci, c in enumerate(closed):
        H[lab == c, ci] = 1.0
    if len(T):
        A = np.eye(len(T)) - P[np.ix_(T, T)]
        B = np.zeros((len(T), len(closed)))
        for ci, c in enumerate(closed):
            m = lab == c
            B[:, ci] = P[np.ix_(T, np.nonzero(m)[0])].sum(axis=1)
        H[T] = np.linalg.solve(A, B)
    W = seed @ H
    W /= W.sum()
    for ci, c in enumerate(closed):
        mem = np.nonzero(lab == c)[0]
        sub = LA[np.ix_(mem, mem)]
        order, _ = order_by_exit(sub)
        lx = gth_log(sub[np.ix_(order, order)]) if len(mem) > 1 else np.array([0.0])
        out = np.empty(len(mem)); out[order] = lx
        lpi[mem] = out + (math.log(W[ci]) if W[ci] > 0 else NEG)
    info['closed_weights'] = W.tolist()
    return lpi, info


def linear_stationary(trans, seed_weight, states):
    """The published linear solve (chain.Chain.stationary) on a given generator: trans {key: {key2: prob}} over the
    expanded set, seed weights {key: w}, states {key: (ids, x, kind)}.  Returns (keys, pi, near_closed, terminal
    count, absorb_error)."""
    obj = Chain.__new__(Chain)
    obj.trans = trans
    obj.seed_weight = seed_weight
    obj.states = states
    pi = Chain.stationary(obj)
    return obj.keys_list, pi, obj.near_closed, len(obj.terminal), obj.absorb_error


def residual_log(LA, lpi):
    """max over states of |log(inflow) - log(outflow)| for the stationary balance pi_j sum_i q_ji = sum_i pi_i q_ij,
    on states with finite log pi (relative balance residual)."""
    n = LA.shape[0]
    res = 0.0
    for j in range(n):
        if not np.isfinite(lpi[j]):
            continue
        o = LA[j][np.isfinite(LA[j])]
        o = o[np.arange(len(o))]
        lo = lpi[j] + np.logaddexp.reduce(np.delete(LA[j], j)[np.isfinite(np.delete(LA[j], j))]) if len(o) else NEG
        col = LA[:, j] + lpi
        col[j] = NEG
        col = col[np.isfinite(col)]
        li = np.logaddexp.reduce(col) if len(col) else NEG
        if np.isfinite(lo) and np.isfinite(li):
            res = max(res, abs(lo - li))
        elif np.isfinite(lo) != np.isfinite(li):
            res = max(res, np.inf)
    return res


def twin_of(U, ids, q, tol=1e-9):
    """the resident r of support ids of which q is a payoff twin (same payoffs against every resident, both
    directions, and U[q,q] = U[q,r] = U[r,q] = U[r,r]), or None."""
    for r in ids:
        if q == r:
            continue
        if not (abs(U[q, q] - U[r, r]) < tol and abs(U[q, r] - U[r, r]) < tol and abs(U[r, q] - U[r, r]) < tol):
            continue
        ok = True
        for j in ids:
            if j == r:
                continue
            if abs(U[q, j] - U[r, j]) > tol or abs(U[j, q] - U[j, r]) > tol:
                ok = False
                break
        if ok:
            return r
    return None


# ---------------------------------------------------------------- the chain
class LogChain(Chain):
    """chain.Chain with every edge also kept as a log weight (identical transition model)."""

    def __init__(self, provider, N, w=1.0, twins=False, Ufull=None, **kw):
        super().__init__(provider, N=N, w=w, **kw)
        self.ledge = {}                       # key -> {key2: log weight per mutation event}
        self.lmut = defaultdict(dict)         # (key, key2) -> {q: log weight}
        self.twins = twins
        self.Ufull = Ufull                    # class-level payoff matrix (needed for twin detection)
        self.n_twin_moves = 0
        self.underflow = 0                    # edges whose linear weight is 0 but log weight finite

    def expand(self, key):
        if key in self.trans:
            return
        ids, x, kind = self.states[key]
        ids = np.array(ids); x = np.array(x)
        N = self.N; m = len(ids); w = self.w
        self.P.prepare(ids)
        classes = self.P.mutant_classes(ids)
        reps = np.array([c[0] for c in classes]); mu = np.array([c[2] for c in classes])
        rows, cols, diag, inner = self.P.blocks_for(ids)
        K = len(reps)
        in_sup = np.isin(reps, ids)
        if kind == 'poly':
            neutral_ext = np.zeros(K, bool)
        else:
            neutral_ext = (np.abs(rows - inner[0:1, :]) < 1e-7).all(axis=1) & (np.abs(cols - diag[None, :]) < 1e-7).all(axis=0)
        uaa = float(x @ inner @ x)
        uqa = rows @ x
        uaq = cols.T @ x
        out = defaultdict(float)
        muts = defaultdict(lambda: defaultdict(float))
        lout = {}
        lmuts = defaultdict(dict)
        for qi in range(K):
            q = int(reps[qi]); m_q = mu[qi]
            if in_sup[qi]:
                out[key] += m_q; muts[key][q] += m_q
                continue
            if self.twins and kind == 'poly' and self.Ufull is not None:
                r = twin_of(self.Ufull, list(ids), q)
                if r is not None:
                    xr = float(x[list(ids).index(r)])
                    ids2 = [q if j == r else int(j) for j in ids]
                    k3 = self.add_state(ids2, x)
                    pr = m_q / max(xr * N, 1.0)
                    lw = math.log(m_q) - math.log(max(xr * N, 1.0))
                    self.n_twin_moves += 1
                    if k3 != key:
                        out[k3] += pr; muts[k3][q] += pr
                        lout[k3] = lae(lout.get(k3, NEG), lw); lmuts[k3][q] = lae(lmuts[k3].get(q, NEG), lw)
                        self.edge_rho[(key, k3, q)] = (1.0 / max(xr * N, 1.0), -1, 'twin')
                    out[key] += m_q - pr; muts[key][q] += m_q - pr
                    continue
            if neutral_ext[qi]:
                fl = [(1.0, self.mono(q), N)]
            else:
                Uq = np.empty((m + 1, m + 1)); Uq[:m, :m] = inner; Uq[m, :m] = rows[qi]; Uq[:m, m] = cols[:, qi]; Uq[m, m] = diag[qi]
                fl = self.fates(key, ids, x, q, Uq)
            if not fl:
                continue
            stay = m_q
            for share, k2, kstar in fl:
                rho = fixation(float(diag[qi]), float(uqa[qi]), float(uaq[qi]), uaa, N, w, int(kstar))
                if k2 == key:
                    continue
                wgt = m_q * share * rho
                out[k2] += wgt; muts[k2][q] += wgt
                stay -= wgt
                self.edge_rho[(key, k2, q)] = (rho, int(kstar), self.states[k2][2])
                if share > 0:
                    lr = log_fixation(float(diag[qi]), float(uqa[qi]), float(uaq[qi]), uaa, N, w, int(kstar))
                    lw = math.log(m_q) + math.log(share) + lr
                    lout[k2] = lae(lout.get(k2, NEG), lw)
                    lmuts[k2][q] = lae(lmuts[k2].get(q, NEG), lw)
                    if wgt == 0.0 and np.isfinite(lw):
                        self.underflow += 1
            out[key] += max(stay, 0.0); muts[key][q] += max(stay, 0.0)
        z = sum(out.values())
        self.trans[key] = {k2: v / z for k2, v in out.items()}
        for k2, d in muts.items():
            for q, v in d.items():
                self.trans_mut[(key, k2)][q] += v / z
        lz = math.log(z)
        self.ledge[key] = {k2: v - lz for k2, v in lout.items()}
        for k2, d in lmuts.items():
            for q, v in d.items():
                self.lmut[(key, k2)][q] = v - lz

    # -- log matrices
    def log_matrix(self, keys):
        pos = {k: i for i, k in enumerate(keys)}
        n = len(keys)
        LA = np.full((n, n), NEG)
        out_un = defaultdict(list)
        for k in keys:
            i = pos[k]
            for k2, lw in self.ledge.get(k, {}).items():
                j = pos.get(k2)
                if j is None:
                    out_un[k2].append((i, lw))
                elif j != i:
                    LA[i, j] = lae(LA[i, j], lw)
        return LA, out_un

    def solve(self, keys=None, seed_logw=None):
        keys = list(self.trans) if keys is None else keys
        LA, out_un = self.log_matrix(keys)
        lpi, info = stationary_log(LA, seed_logw)
        return keys, LA, lpi, info, out_un

    # -- exploration
    def explore_log(self, extra_states=(), log_theta=math.log(1e-30), max_states=20000, max_rounds=200, mono=True,
                    one_layer=True, verbose=False):
        if mono:
            for rep, members, wt in self.P.mutant_classes(()):
                k = self.mono(rep)
                self.seed_weight[k] = self.seed_weight.get(k, 0.0) + wt
                self.expand(k)
        seeded = []
        for ids, x in extra_states:
            k = self.add_state(ids, x)
            self.expand(k)
            seeded.append(k)
        if one_layer:
            for k in seeded:
                for k2 in list(self.trans[k]):
                    if k2 not in self.trans:
                        self.expand(k2)
        lcut = NEG
        cand = []
        for rnd in range(max_rounds):
            keys = list(self.trans)
            LA, out_un = self.log_matrix(keys)
            lpi, info = stationary_log(LA)
            inflow = {k2: np.logaddexp.reduce([lpi[i] + lw for i, lw in lst]) for k2, lst in out_un.items()}
            cand = [k for k, f in inflow.items() if f > log_theta]
            small = [f for f in inflow.values() if f <= log_theta and np.isfinite(f)]
            lcut = float(np.logaddexp.reduce(small)) if small else NEG
            if verbose:
                print('    log round %d: %d expanded, %d candidates, log10 cut %.1f, closed %d' % (
                    rnd, len(keys), len(cand), lcut / math.log(10) if np.isfinite(lcut) else -999, info['n_closed']), flush=True)
            if not cand or len(keys) >= max_states:
                break
            for k in sorted(cand, key=lambda k: -inflow[k])[:max(1, max_states - len(keys))]:
                self.expand(k)
        self.log_cut = lcut
        self.n_cand_left = len(cand)
        self.explored = set(self.trans)
        return self

    def explore_closure(self, seeds=None, max_states=20000):
        if seeds is None:
            seeds = [(rep, wt) for rep, members, wt in self.P.mutant_classes(())]
        queue = []
        for rep, wt in seeds:
            k = self.mono(rep)
            self.seed_weight[k] = self.seed_weight.get(k, 0.0) + wt
            queue.append(k)
        while queue and len(self.trans) < max_states:
            k = queue.pop()
            if k in self.trans:
                continue
            self.expand(k)
            for k2 in self.trans[k]:
                if k2 not in self.trans:
                    queue.append(k2)
        self.closure_complete = not queue
        self.explored = set(self.trans)
        return self
