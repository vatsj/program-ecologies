"""Solver audit of the published eps->0 chains with independent deep-state discovery (spec
specs/2026-10-05-solver-audit.md, reviewed by gpt-6.1-sol; predictions predictions/2026-10-05-solver-audit.md).

Per cell:
  1. discovery   candidate recurrent supports (<= 3 classes, internally stable by the Jacobian) from the class table
                 alone, classified deep / non-deep (operational definition, tolerance 1e-9), with every outside
                 mutant's invasion fitness for the deep ones;
  2. published   the published chain re-run exactly (chain.Chain, its theta / eager flags): explored set, pi, stat;
  3. rates       the same explored set and transition model in chain_log.LogChain (identical fates and k*), every
                 edge recomputed in the log domain and compared with the published linear weights;
  4. solver      the published generator solved by log-domain GTH against the published linear solve (residuals,
                 near-closed classes, statistic under each);
  5. re-solve    every monomorphic state and every enumerated candidate support seeded and expanded, log-domain
                 exploration (relative inflow > theta_log), log-domain GTH; statistic, support and transitions;
  6. twins       (dollar cells, intervention) the same re-solve with twin moves.

    python3 src/solver_audit.py cell --cell dollar5-norole --N 1000 10000 30000
    python3 src/solver_audit.py controls
    python3 src/solver_audit.py twins --cell dollar5-norole --N 10000 100000
Writes runs/solver_audit/<cell>_N<N>.json.
"""
import argparse, itertools, json, math, os, sys, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from chain import Chain, replicator
from chain_log import LogChain, linear_stationary, stationary_log, gth_log, gth_mp, order_by_exit, closed_classes, lae, NEG

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'solver_audit')
os.makedirs(OUT, exist_ok=True)
TOL = 1e-9
L10 = math.log(10)


# ================================================================ discovery
def _jac_tangent(Us, x):
    """eigenvalues of the replicator Jacobian at an interior rest point x of payoff matrix Us, restricted to the
    simplex's tangent space."""
    m = len(x)
    if m == 1:
        return np.zeros(0)
    phi = x @ Us @ x
    UTx = Us.T @ x
    J = x[:, None] * (Us - phi - UTx[None, :])
    V = np.vstack([np.eye(m - 1), -np.ones((1, m - 1))])
    M = (J @ V)[:m - 1]
    return np.linalg.eigvals(M)


def classify_rest(Us, x, tol=1e-12):
    ev = _jac_tangent(Us, x)
    if len(ev) == 0:
        return 'stable', ev
    re = ev.real
    if (re < -tol).all():
        return 'stable', ev
    if (re > tol).any():
        return 'unstable', ev
    if np.abs(ev.imag).max() > tol and (np.abs(re) <= tol).all():
        return 'center', ev
    return 'neutral', ev


def deep_test(U, ids, x, tol=TOL):
    """invasion fitness of every outside class against the resident mix; deep iff all < -tol.  Also the repo's older
    'deep with penalty' criterion (first-order-neutral mutants allowed if their second-order term is negative)."""
    ids = np.asarray(ids); x = np.asarray(x, float)
    phi = float(x @ U[np.ix_(ids, ids)] @ x)
    f = U[:, ids] @ x - phi
    out = np.ones(U.shape[0], bool); out[ids] = False
    fo = f[out]
    deep = bool((fo < -tol).all())
    # deep modulo twins: every outside class strictly deleterious or a payoff twin of a resident
    from chain_log import twin_of
    mt = not (fo > tol).any()
    if mt and not deep:
        for q in np.nonzero(out & (f >= -tol))[0]:
            if twin_of(U, list(ids), int(q)) is None:
                mt = False; break
    # deep with penalty (the repo's older criterion, at the audit's tolerance): no outside class above +tol, and every
    # first-order-neutral class (|f| <= tol) loses at second order (the lumped-resident frequency penalty) by > tol
    pen = True
    if (fo > tol).any():
        pen = False
    else:
        for q in np.nonzero(out & (np.abs(f) <= tol))[0]:
            if (U[q, q] - (U[q, ids] @ x)) - (U[ids, q] @ x - phi) >= -tol:
                pen = False; break
    return deep, pen, f, out, mt


def enumerate_candidates(U, mu, pool=None, max_types=3, chunk=200000, verbose=False):
    """Candidate recurrent supports of <= max_types classes from the class table alone.  pool: classes allowed in
    pairs and triples (default: all).  Returns list of dict(ids, x, size, status, deep, deep_pen, max_inv, n_neutral,
    n_adv, mass_sum, mass_min), plus counts."""
    K = U.shape[0]
    pool = np.arange(K) if pool is None else np.array(sorted(set(int(p) for p in pool)))
    cands = []
    counts = defaultdict(int)

    def add(ids, x, status):
        deep, pen, f, out, mt = deep_test(U, ids, x)
        fo = f[out]
        cands.append(dict(ids=[int(i) for i in ids], x=[float(v) for v in x], size=len(ids), status=status, deep=deep, deep_pen=pen, deep_mt=mt,
                          max_inv=float(fo.max()) if len(fo) else -np.inf, n_neutral=int((np.abs(fo) <= TOL).sum()),
                          n_adv=int((fo > TOL).sum()), mass_sum=float(mu[list(ids)].sum()), mass_min=float(mu[list(ids)].min())))
    for i in range(K):
        add([i], [1.0], 'stable')
    counts['singletons'] = K
    # pairs
    P = np.array(list(itertools.combinations(pool, 2))) if len(pool) >= 2 else np.zeros((0, 2), int)
    counts['pairs_tested'] = len(P)
    if len(P):
        i, j = P[:, 0], P[:, 1]
        a, b, c, e = U[i, i], U[i, j], U[j, i], U[j, j]
        ok = (c - a > 1e-12) & (b - e > 1e-12)        # each invades the other: interior, internally stable (hawk-dove)
        neutral = (np.abs(c - a) <= 1e-12) & (np.abs(b - e) <= 1e-12)
        counts['pairs_neutral_line'] = int(neutral.sum())
        counts['pairs_unstable_interior'] = int(((a - c > 1e-12) & (e - b > 1e-12)).sum())
        for r in np.nonzero(ok)[0]:
            x = (b[r] - e[r]) / ((b[r] - e[r]) + (c[r] - a[r]))
            if x > 1e-6 and 1 - x > 1e-6:
                add([i[r], j[r]], [x, 1 - x], 'stable')
                counts['pairs_stable'] += 1
    if max_types >= 3 and len(pool) >= 3:
        n3 = math.comb(len(pool), 3)
        counts['triples_tested'] = n3
        it = itertools.combinations(pool, 3)
        done = 0
        while True:
            t = np.array(list(itertools.islice(it, chunk)))
            if len(t) == 0:
                break
            n = len(t)
            A = np.zeros((n, 4, 4)); A[:, :3, :3] = U[t[:, :, None], t[:, None, :]]; A[:, :3, 3] = -1; A[:, 3, :3] = 1
            bb = np.zeros((n, 4)); bb[:, 3] = 1
            det = np.linalg.det(A)
            ok = np.abs(det) > 1e-12
            counts['triples_singular'] += int((~ok).sum())
            X = np.full((n, 4), np.nan)
            if ok.any():
                X[ok] = np.linalg.solve(A[ok], bb[ok][:, :, None])[:, :, 0]
            inter = ok & (X[:, :3] > 1e-6).all(1)
            counts['triples_interior'] += int(inter.sum())
            for r in np.nonzero(inter)[0]:
                ids = t[r]; x = X[r, :3]
                Us = U[np.ix_(ids, ids)]
                st, ev = classify_rest(Us, x)
                counts['triples_' + st] += 1
                if st == 'stable':
                    add(ids, x, 'stable')
                elif st == 'center':
                    add(ids, x, 'center')
            done += n
            if verbose:
                print('    triples %d / %d' % (done, n3), flush=True)
    return cands, dict(counts)


def enumerate_candidates_fast(U, mu, pool=None, keep_all=False, verbose=False):
    """Vectorized enumerate_candidates (same definitions and tolerances).  keep_all=False keeps full records only for
    candidates with no strictly advantageous outside mutant (n_adv == 0: the possible traps) and counts the rest."""
    K = U.shape[0]
    pool = np.arange(K) if pool is None else np.array(sorted(set(int(p) for p in pool)))
    cands = []
    counts = defaultdict(int)

    def add(ids, x, status):
        deep, pen, f, out, mt = deep_test(U, ids, x)
        fo = f[out]
        cands.append(dict(ids=[int(i) for i in ids], x=[float(v) for v in x], size=len(ids), status=status, deep=deep, deep_pen=pen, deep_mt=mt,
                          max_inv=float(fo.max()) if len(fo) else -np.inf, n_neutral=int((np.abs(fo) <= TOL).sum()),
                          n_adv=int((fo > TOL).sum()), mass_sum=float(mu[list(ids)].sum()), mass_min=float(mu[list(ids)].min())))

    def batch(T, X, status):
        """T (n, m) class ids, X (n, m) frequencies: invasion fitness of every class; keep per keep_all."""
        n, m = T.shape
        for s0 in range(0, n, 20000):
            t = T[s0:s0 + 20000]; x = X[s0:s0 + 20000]
            Us = U[t[:, :, None], t[:, None, :]]
            phi = np.einsum('ni,nij,nj->n', x, Us, x)
            F = np.einsum('kni,ni->nk', U[:, t], x) - phi[:, None]
            mem = np.zeros_like(F, bool)
            np.put_along_axis(mem, t, True, axis=1)
            F[mem] = -np.inf
            nadv = (F > TOL).sum(1)
            counts['%s_size%d' % (status, m)] += n
            counts['%s_size%d_noadv' % (status, m)] += int((nadv == 0).sum())
            sel = np.arange(len(t)) if keep_all else np.nonzero(nadv == 0)[0]
            for r in sel:
                add(t[r], x[r], status)
    batch(np.arange(K)[:, None], np.ones((K, 1)), 'stable')
    counts['singletons'] = K
    P = np.array(list(itertools.combinations(pool, 2))) if len(pool) >= 2 else np.zeros((0, 2), int)
    counts['pairs_tested'] = len(P)
    if len(P):
        i, j = P[:, 0], P[:, 1]
        a, b, c, e = U[i, i], U[i, j], U[j, i], U[j, j]
        ok = (c - a > 1e-12) & (b - e > 1e-12)
        counts['pairs_neutral_line'] = int(((np.abs(c - a) <= 1e-12) & (np.abs(b - e) <= 1e-12)).sum())
        counts['pairs_unstable_interior'] = int(((a - c > 1e-12) & (e - b > 1e-12)).sum())
        x = np.where(ok, (b - e) / np.where(ok, (b - e) + (c - a), 1.0), 0.0)
        ok &= (x > 1e-6) & (1 - x > 1e-6)
        counts['pairs_stable'] = int(ok.sum())
        if ok.any():
            batch(P[ok], np.stack([x[ok], 1 - x[ok]], 1), 'stable')
    if len(pool) >= 3:
        counts['triples_tested'] = math.comb(len(pool), 3)
        V = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]])
        for a_ in range(len(pool) - 2):
            jj, kk = np.triu_indices(len(pool) - a_ - 1, 1)
            if len(jj) == 0:
                continue
            t = np.stack([np.full(len(jj), pool[a_]), pool[a_ + 1 + jj], pool[a_ + 1 + kk]], 1)
            n = len(t)
            A = np.zeros((n, 4, 4)); A[:, :3, :3] = U[t[:, :, None], t[:, None, :]]; A[:, :3, 3] = -1; A[:, 3, :3] = 1
            det = np.linalg.det(A)
            ok = np.abs(det) > 1e-12
            counts['triples_singular'] += int((~ok).sum())
            if not ok.any():
                continue
            bb = np.zeros((int(ok.sum()), 4, 1)); bb[:, 3, 0] = 1
            X = np.linalg.solve(A[ok], bb)[:, :3, 0]
            t = t[ok]
            inter = (X > 1e-6).all(1)
            counts['triples_interior'] += int(inter.sum())
            t, X = t[inter], X[inter]
            if not len(t):
                continue
            Us = U[t[:, :, None], t[:, None, :]]
            phi = np.einsum('ni,nij,nj->n', X, Us, X)
            UTx = np.einsum('nji,nj->ni', Us, X)
            J = X[:, :, None] * (Us - phi[:, None, None] - UTx[:, None, :])
            M = (J @ V)[:, :2, :]
            tr = M[:, 0, 0] + M[:, 1, 1]; dt = M[:, 0, 0] * M[:, 1, 1] - M[:, 0, 1] * M[:, 1, 0]
            stable = (tr < -1e-12) & (dt > 1e-12)
            center = (np.abs(tr) <= 1e-12) & (dt > 1e-12)
            counts['triples_stable'] += int(stable.sum()); counts['triples_center'] += int(center.sum())
            counts['triples_unstable_or_neutral'] += int((~stable & ~center).sum())
            if stable.any():
                batch(t[stable], X[stable], 'stable')
            for r in np.nonzero(center)[0]:
                add(t[r], X[r], 'center')
            if verbose and a_ % 100 == 0:
                print('    triples: first index %d / %d, kept %d' % (a_, len(pool), len(cands)), flush=True)
    return cands, dict(counts)


def attractor_search(U, mu, n_starts=4000, seed=1, max_sub=8, verbose=False):
    """Discovery of saturated attractors of any support size: the full K-type replicator (chain.replicator) from
    random starts (random subsets of 2..max_sub classes with Dirichlet weights, half of them with every other class
    at 1e-4), rest points collected and classified (internally stable by the Jacobian on their support, deep tiers,
    n_adv).  Not exhaustive: an attractor with a tiny basin can be missed; it complements the exhaustive <= 3-class
    enumeration."""
    rng = np.random.default_rng(seed)
    K = U.shape[0]
    found = {}
    for s in range(n_starts):
        m = int(rng.integers(2, max_sub + 1))
        sub = rng.choice(K, m, replace=False)
        x0 = np.zeros(K)
        if s % 2 == 0:
            x0[:] = 1e-4
        x0[sub] += rng.dirichlet(np.ones(m))
        x0 /= x0.sum()
        x, st, _, _ = replicator(U, x0, rest_tol=1e-10)
        if st != 'rest':
            continue
        sup = np.nonzero(x > 1e-6)[0]
        key = tuple(sup.tolist())
        if key in found:
            found[key]['hits'] += 1
            continue
        xs = x[sup] / x[sup].sum()
        stat, ev = classify_rest(U[np.ix_(sup, sup)], xs) if len(sup) > 1 else ('stable', None)
        dp, pen, f, out, mt = deep_test(U, sup, xs)
        fo = f[out]
        found[key] = dict(ids=[int(i) for i in sup], x=[float(v) for v in xs], size=len(sup), status=stat, deep=dp, deep_pen=pen, deep_mt=mt,
                          max_inv=float(fo.max()) if len(fo) else -np.inf, n_neutral=int((np.abs(fo) <= TOL).sum()), n_adv=int((fo > TOL).sum()),
                          mass_sum=float(mu[sup].sum()), mass_min=float(mu[sup].min()), hits=1, source='attractor_search')
        if verbose and len(found) % 50 == 0:
            print('    attractor search: %d starts, %d rest supports' % (s + 1, len(found)), flush=True)
    return list(found.values())


def invasion_closure(U, mu, starts=None, max_nodes=30000, verbose=False, branch=None, max_steps=8000):
    """Saturated rest points of any support size reachable from the starts (default: every monomorphic state) by
    sequences of strict invasions: from a rest point, every outside class with invasion fitness > tol is added at
    frequency 1e-3 and the replicator on the enlarged support is run to its rest point; repeated until no class
    invades (saturated).  Independent of any chain probability or threshold.  Returns (saturated list, n_nodes,
    complete flag)."""
    K = U.shape[0]
    if starts is None:
        starts = [([i], [1.0]) for i in range(K)]
    seen = set()
    sat = {}
    stack = []
    for ids, x in starts:
        key = tuple(sorted(int(i) for i in ids))
        if key not in seen:
            seen.add(key); stack.append((list(ids), np.asarray(x, float)))
    n = 0
    while stack and n < max_nodes:
        ids, x = stack.pop()
        n += 1
        ids = np.asarray(ids)
        phi = float(x @ U[np.ix_(ids, ids)] @ x)
        f = U[:, ids] @ x - phi
        f[ids] = -np.inf
        adv = np.nonzero(f > TOL)[0]
        if len(adv) == 0:
            key = tuple(sorted(int(i) for i in ids))
            if key not in sat:
                o = np.argsort(ids)
                xs = x[o]; idss = ids[o]
                stat = classify_rest(U[np.ix_(idss, idss)], xs)[0] if len(idss) > 1 else 'stable'
                dp, pen, ff, out, mt = deep_test(U, idss, xs)
                fo = ff[out]
                sat[key] = dict(ids=[int(i) for i in idss], x=[float(v) for v in xs], size=len(idss), status=stat, deep=dp, deep_pen=pen,
                                deep_mt=mt, max_inv=float(fo.max()) if len(fo) else -np.inf, n_neutral=int((np.abs(fo) <= TOL).sum()),
                                n_adv=0, mass_sum=float(mu[idss].sum()), mass_min=float(mu[idss].min()), source='invasion_closure')
            continue
        if branch is not None and len(adv) > branch:
            adv = adv[np.argsort(-f[adv])[:branch]]      # the `branch` strongest invaders only
        for q in adv:
            sup = np.append(ids, q)
            x0 = np.append(x * (1 - 1e-3), 1e-3)
            xr, st, _, _ = replicator(U[np.ix_(sup, sup)], x0, rest_tol=1e-10, max_steps=max_steps)
            if st != 'rest':
                continue
            keep = xr > 1e-6
            key = tuple(sorted(int(i) for i in sup[keep]))
            if key in seen:
                continue
            seen.add(key)
            stack.append((sup[keep], xr[keep] / xr[keep].sum()))
        if verbose and n % 2000 == 0:
            print('    invasion closure: %d nodes, %d saturated, stack %d' % (n, len(sat), len(stack)), flush=True)
    return list(sat.values()), n, not stack


def deep_detail(U, names, mu, cand, top=None):
    """the full list of outside mutants of a candidate with their invasion fitnesses (sorted, closest to 0 first)."""
    deep, pen, f, out, mt = deep_test(U, cand['ids'], cand['x'])
    qs = np.nonzero(out)[0]
    order = qs[np.argsort(-f[qs])]
    if top is not None:
        order = order[:top]
    return [(names[q], float(f[q]), float(mu[q])) for q in order]


# ================================================================ cells
class Cell:
    """name, provider factory, class-level matrix U (index = class index c), mu[c], chain id of class c, stat."""
    pass


def _dollar_stat(d):
    from dollar_partitions import pop_outcome

    def stat(ids, x, N):
        cnt = np.round(np.asarray(x) * N).astype(int)
        if cnt.sum() == 0:
            cnt = np.ones(len(ids), int)
        o = pop_outcome(d, list(ids), cnt)
        return dict(eff=o['eff'], half=o.get('1/2-1/2', 0.0), third=o.get('1/3-2/3', 0.0), sixth=o.get('1/6-5/6', 0.0),
                    clash=o.get('clash', 0.0), ineff=o.get('ineff', 0.0))
    return stat


def make_cell(name, N):
    c = Cell()
    c.name = name
    c.headline = 'eff'
    if name.startswith('dollar5-') or name.startswith('dollar3-'):
        import dollar_partitions as DP
        game, arm = name.split('-')
        d = DP.data(game, 5, arm)
        c.d = d
        c.provider = lambda: DP.ClassProvider(d['U'], d['mu'])
        pr = c.provider()
        c.U = pr.Ufull; c.mu = np.asarray(d['mu'], float); c.names = list(d['names'])
        c.cid = np.arange(d['K'])
        c.stat = _dollar_stat(d)
        c.chain_kw = dict(w=0.3, theta=1e-7, max_states=30000)
        c.headlines = ('eff', 'half')
        c.twin_ok = True
    elif name == 'modal-dollar7':
        import modal_dollar as MD
        d = MD.data('modal', 7)
        c.d = d
        from dollar_partitions import ClassProvider
        c.provider = lambda: ClassProvider(d['U'], d['mu'])
        pr = c.provider()
        c.U = pr.Ufull; c.mu = np.asarray(d['mu'], float); c.names = list(d['names']); c.cid = np.arange(d['K'])
        c.stat = _dollar_stat(d)
        c.chain_kw = dict(w=0.3, theta=1e-7, max_states=30000, eager_poly=False)
        c.headlines = ('eff', 'half')
        c.twin_ok = True
    elif name in ('pd-modal9', 'pd-priced6-atoms', 'pd-priced8-atoms', 'pd-priced8-lazy', 'pd-k16'):
        import modal as M
        if name == 'pd-modal9':
            prov = M.build(9)[3]
            kw = dict(w=0.3)
        elif name == 'pd-k16':
            import k_at_n8 as K8
            prov = K8.build_prov(8, K8.load_val(8, 16))
            kw = dict(w=0.3, eager_poly=False)
        else:
            n = int(name.split('-')[1][-1]); pricing = name.split('-')[2]
            prov = M.build_priced(n, 0.01, pricing=pricing)[3]
            kw = dict(w=0.3, eager_poly=False)
        c.provider = lambda: prov
        c.U = prov.Ufull; c.mu = np.array([t[2] for t in prov.classes]); c.names = list(prov.names); c.cid = np.arange(len(prov.names))
        P = prov.PCC

        def stat(ids, x, N, P=P):
            ids = list(ids); x = np.asarray(x)
            return dict(pcc=float(x @ P[np.ix_(ids, ids)] @ x))
        c.stat = stat
        c.chain_kw = kw
        c.headlines = ('pcc',)
        c.twin_ok = False
    elif name == 'pd-weak6':
        from run import get_language, get_provider
        from game import Game
        from abm import load_or_evaluate
        game = Game.load(os.path.join(ROOT, 'games', 'pd.yaml'))
        lang = get_language('weak', 6, True, game.role, game)
        prov, div = get_provider(lang, game, 'weak', 6, True, 'square', False)
        c.provider = lambda: prov
        cls = prov.classes              # (rep program id, members, mu), sorted by -mu
        R = np.array([prov.pos[t[0]] for t in cls])
        c.U = prov.Ufull[np.ix_(R, R)]; c.mu = np.array([t[2] for t in cls]); c.names = [lang.src(t[0]) for t in cls]
        c.cid = np.array([t[0] for t in cls])
        _, aids, reps, members, _, _, PCC, _, _, _ = load_or_evaluate(game, 6, verbose=False)
        acls = {}
        for k, mem in enumerate(members):
            for a in mem:
                acls[int(aids[a])] = k

        def stat(ids, x, N, PCC=PCC, acls=acls):
            cs = [acls[int(p)] for p in ids]; x = np.asarray(x)
            return dict(pcc=float(x @ PCC[np.ix_(cs, cs)] @ x))
        c.stat = stat
        c.chain_kw = dict(w=0.3, theta=1e-6, max_states=30000)
        c.headlines = ('pcc',)
        c.twin_ok = False
    else:
        raise ValueError(name)
    c.N = N
    c.id2c = {int(p): k for k, p in enumerate(c.cid)}
    return c


PUBLISHED = {
    ('dollar5-norole', 1000): dict(eff=0.9995, half=0.9990), ('dollar5-norole', 10000): dict(eff=0.4135, half=0.0004),
    ('dollar5-norole', 30000): dict(eff=0.4132, half=0.0000),
    ('dollar5-role', 1000): dict(eff=0.9995, half=0.6928), ('dollar5-role', 10000): dict(eff=0.9682, half=0.8062),
    ('dollar5-role', 30000): dict(eff=0.4620, half=0.0740),
    ('dollar3-norole', 1000): dict(eff=0.9959, half=0.9853), ('dollar3-norole', 10000): dict(eff=0.6251, half=0.0000),
    ('dollar3-role', 1000): dict(eff=0.9992, half=0.1568), ('dollar3-role', 10000): dict(eff=0.9858, half=0.7882),
    ('dollar3-role', 30000): dict(half=0.817),
    ('pd-modal9', 10000): dict(pcc=0.622), ('pd-modal9', 30000): dict(pcc=0.727),
    ('pd-weak6', 10000): dict(pcc=0.0073),
    ('pd-priced6-atoms', 10000): dict(pcc=0.0150), ('pd-priced8-atoms', 10000): dict(pcc=0.0158),
    ('pd-priced8-lazy', 10000): dict(pcc=0.9985),
    ('pd-k16', 10000): dict(pcc=0.671),
    ('modal-dollar7', 10000): dict(eff=0.653),
}


# ================================================================ analysis helpers
def stat_of(c, ch, keys, pi):
    acc = defaultdict(float)
    for k, p in zip(keys, pi):
        if p <= 0:
            continue
        ids, x, kind = ch.states[k]
        for kk, v in c.stat(ids, x, ch.N).items():
            acc[kk] += p * v
    return dict(acc)


def desc(c, ch, k):
    ids, x, kind = ch.states[k]
    return ' + '.join('%s:%.3f' % (c.names[c.id2c[int(i)]], xi) for i, xi in zip(ids, x))


def support_and_transitions(c, ch, keys, LA, lpi, top=10, top_exits=5):
    """top states by pi with their per-event log10 exit rates and the leading exits (target, log10 rate, mutants)."""
    pos = {k: i for i, k in enumerate(keys)}
    order = np.argsort(-lpi)[:top]
    sup = []
    for i in order:
        k = keys[i]
        row = LA[i]
        fin = np.isfinite(row); fin[i] = False
        lex = float(np.logaddexp.reduce(row[fin])) if fin.any() else NEG
        ex = []
        for j in np.argsort(-np.where(fin, row, -np.inf))[:top_exits]:
            if not fin[j]:
                break
            muts = sorted(ch.lmut.get((k, keys[j]), {}).items(), key=lambda kv: -kv[1])[:3]
            ex.append(dict(to=desc(c, ch, keys[j]), log10_rate=float(row[j] / L10),
                           mutants=[(c.names[c.id2c[int(q)]], float(v / L10)) for q, v in muts]))
        sup.append(dict(state=desc(c, ch, k), pi=float(np.exp(lpi[i])), log10_pi=float(lpi[i] / L10),
                        log10_exit=float(lex / L10) if np.isfinite(lex) else None, exits=ex,
                        stat={kk: round(v, 6) for kk, v in c.stat(*ch.states[k][:2], ch.N).items()}))
    return sup


def cand_key(ch, cand, c):
    ids = [int(c.cid[i]) for i in cand['ids']]
    return ch.add_state(ids, cand['x'])


def run_cell(name, N, log_theta=math.log(1e-30), max_states=20000, verbose=True, twins=False, extra_only_deep=False,
             skip_published=False, triples=True, pool_K=None, full_seed=False, est_floor=False, closure_nodes=0, closure_starts=20000):
    t0 = time.time()
    c = make_cell(name, N)
    res = dict(cell=name, N=N, K=int(len(c.mu)), chain_kw={k: v for k, v in c.chain_kw.items()}, published=PUBLISHED.get((name, N)))
    # ---- 1. discovery
    pool = None
    if pool_K is not None and pool_K < len(c.mu):
        pool = set(np.argsort(-c.mu)[:pool_K].tolist())
    td = time.time()
    keep_all = len(c.mu) <= 250
    cands, counts = enumerate_candidates_fast(c.U, c.mu, pool=None if pool is None else sorted(pool), keep_all=keep_all, verbose=verbose)
    res['discovery_keep_all'] = keep_all
    if closure_nodes:
        tcl = time.time()
        cfn = os.path.join(OUT, 'closure_%s_%d.json' % (name, closure_nodes))
        if os.path.exists(cfn):                       # the closure is N-independent: cached per cell
            z = json.load(open(cfn)); S1, n1, comp1, S2, n2, comp2 = z['S1'], z['n1'], z['comp1'], z['S2'], z['n2'], z['comp2']
        else:
            S1, n1, comp1 = invasion_closure(c.U, c.mu, max_nodes=closure_nodes, branch=None)
            starts = [(x['ids'], x['x']) for x in cands if x['size'] > 1 and x['status'] == 'stable'][:closure_starts]
            S2, n2, comp2 = invasion_closure(c.U, c.mu, starts=[([i], [1.0]) for i in range(len(c.mu))] + starts, max_nodes=3 * closure_nodes, branch=2)
            json.dump(_jsonable(dict(S1=S1, n1=n1, comp1=comp1, S2=S2, n2=n2, comp2=comp2)), open(cfn, 'w'))
        have = set(tuple(sorted(x['ids'])) for x in cands)
        added = 0
        for x in S1 + S2:
            if x['size'] >= 2 and tuple(sorted(x['ids'])) not in have:
                have.add(tuple(sorted(x['ids']))); cands.append(x); added += 1
        counts['closure'] = dict(nodes_full=n1, complete_full=comp1, nodes_branch2=n2, complete_branch2=comp2,
                                 saturated=len(S1) + len(S2), added=added, added_by_size={str(k): sum(1 for x in cands if x.get('source') == 'invasion_closure' and x['size'] == k) for k in range(2, 9)},
                                 time_s=time.time() - tcl)
        if verbose:
            print('[%s N=%d] invasion closure: %s' % (name, N, counts['closure']), flush=True)
    for x in cands:
        x['tier'] = 'deep' if x['deep'] else ('deep_mod_twins' if x['deep_mt'] else ('deep_penalty_only' if x['deep_pen'] else 'non-deep'))
    deep = [x for x in cands if x['status'] == 'stable' and x['tier'] != 'non-deep']
    strict = [x for x in deep if x['tier'] == 'deep']
    res['discovery'] = dict(counts=counts, pool_K=pool_K or int(len(c.mu)), triples=triples, n_candidates=len(cands),
                            n_stable=sum(1 for x in cands if x['status'] == 'stable'), n_center=sum(1 for x in cands if x['status'] == 'center'),
                            n_deep=len(strict), n_deep_mod_twins=sum(1 for x in deep if x['tier'] == 'deep_mod_twins'),
                            n_deep_penalty_only=sum(1 for x in deep if x['tier'] == 'deep_penalty_only'),
                            n_deep_pen_total=sum(1 for x in cands if x['status'] == 'stable' and x['deep_pen']),
                            deep_by_size={t: {s: sum(1 for x in deep if x['size'] == s and x['tier'] == t) for s in range(1, 9)}
                                          for t in ('deep', 'deep_mod_twins', 'deep_penalty_only')},
                            deep_mass_sum_max=max([x['mass_sum'] for x in strict], default=0.0),
                            deep_any_mass_sum_max=max([x['mass_sum'] for x in deep], default=0.0), time_s=time.time() - td)
    if verbose:
        print('[%s N=%d] discovery: %d candidates (%d stable), deep strict %d / mod twins %d / penalty only %d (%s), %.0fs' % (
            name, N, len(cands), res['discovery']['n_stable'], len(strict), res['discovery']['n_deep_mod_twins'], res['discovery']['n_deep_penalty_only'],
            res['discovery']['deep_by_size'], time.time() - td), flush=True)
    # ---- 2. the published chain, re-run exactly
    if not skip_published:
        tp = time.time()
        pch = Chain(c.provider(), N=N, **c.chain_kw).explore()
        pst = stat_of(c, pch, pch.keys_list, pch.pi)
        res['published_rerun'] = dict(stat=pst, n_expanded=len(pch.trans), n_states=len(pch.states), cut_flow=float(pch.cut_flow),
                                      near_closed=int(pch.near_closed), n_terminal=len(pch.terminal), indeterminate=len(pch.indeterminate),
                                      absorb_error=float(pch.absorb_error), time_s=time.time() - tp,
                                      top=[(desc(c, pch, pch.keys_list[i]), float(pch.pi[i])) for i in np.argsort(-pch.pi)[:8]])
        if verbose:
            print('[%s N=%d] published re-run: %s near_closed %d terminal %d (%.0fs)' % (name, N, {k: round(v, 4) for k, v in pst.items()},
                                                                                     pch.near_closed, len(pch.terminal), time.time() - tp), flush=True)
        # ---- 3. identical rates in the log domain on the same explored set
        tr = time.time()
        lch = LogChain(c.provider(), N=N, Ufull=None, **c.chain_kw).explore()
        same = set(lch.trans) == set(pch.trans)
        keys = pch.keys_list
        rel = []; under = 0; denorm = 0; n_edges = 0; worst = None
        for k in keys:
            lrow = lch.ledge.get(k, {})
            for k2, p in pch.trans[k].items():
                if k2 == k:
                    continue
                n_edges += 1
                lw = lrow.get(k2)
                if lw is None:
                    continue
                if p == 0.0:
                    under += 1
                    continue
                if p < 2.2250738585072014e-308:
                    denorm += 1
                e = abs(math.log(p) - lw)
                rel.append(e)
                if worst is None or e > worst[0]:
                    worst = (e, desc(c, pch, k), desc(c, pch, k2))
        res['rates'] = dict(same_explored_set=bool(same), n_edges=n_edges, max_abs_log_err=float(max(rel)) if rel else 0.0,
                            n_underflow=under, n_denormal=denorm, worst=worst, time_s=time.time() - tr)
        # ---- 4. solver check on the published generator
        LA, out_un = lch.log_matrix(keys)
        seedw = np.array([math.log(pch.seed_weight[k]) if pch.seed_weight.get(k, 0) > 0 else NEG for k in keys])
        lpi_pub, info = stationary_log(LA, seedw)
        lin_keys, lin_pi, nc, nt, ae = linear_stationary({k: lch.trans[k] for k in keys}, lch.seed_weight, lch.states)
        assert lin_keys == keys
        st_log = stat_of(c, lch, keys, np.exp(lpi_pub))
        st_lin = stat_of(c, lch, keys, lin_pi)
        # residual of the linear pi in the log generator: max |log inflow - log outflow| over states with pi > 1e-12
        resid_lin = balance_residual(LA, lin_pi)
        resid_log = balance_residual(LA, np.exp(lpi_pub))
        res['solver'] = dict(log_gth_stat=st_log, linear_stat=st_lin, linear_near_closed=int(nc), linear_terminal=int(nt),
                             log_closed=info, tv=float(0.5 * np.abs(np.exp(lpi_pub) - lin_pi).sum()),
                             resid_linear=resid_lin, resid_log=resid_log,
                             top_log=[(desc(c, lch, keys[i]), float(np.exp(lpi_pub[i]))) for i in np.argsort(-lpi_pub)[:6]])
        if verbose:
            print('[%s N=%d] rates: same set %s, max |dlog| %.2e, underflow %d | solver on published generator: log %s vs linear %s, TV %.4f' % (
                name, N, same, res['rates']['max_abs_log_err'], under, {k: round(v, 4) for k, v in st_log.items()},
                {k: round(v, 4) for k, v in st_lin.items()}, res['solver']['tv']), flush=True)
        # ---- discovery against the published explored set
        pub_set = set(pch.trans)
        pub_ids = set(tuple(sorted(pch.states[k][0])) for k in pub_set)
        pub_rec = set(tuple(sorted(pch.states[k][0])) for k, p in zip(pch.keys_list, pch.pi) if p > 1e-6)
        missed = []
        for x in deep:
            ids = tuple(sorted(int(c.cid[i]) for i in x['ids']))
            x['in_published_explored'] = ids in pub_ids
            x['in_published_recurrent'] = ids in pub_rec
            if not x['in_published_explored']:
                missed.append(x)
        res['discovery']['deep_in_published_explored'] = sum(1 for x in deep if x['in_published_explored'])
        res['discovery']['deep_missed'] = len(missed)
        res['discovery']['deep_missed_mass_sum'] = float(sum(x['mass_sum'] for x in missed))
        # every published state with pi > 1e-6 (any size) classified by the same deep test
        prc = []
        for k, p in zip(pch.keys_list, pch.pi):
            if p <= 1e-6:
                continue
            ids, x, kind = pch.states[k]
            cl = [c.id2c[int(i)] for i in ids]
            dp, pen, f, out, mt = deep_test(c.U, cl, x)
            fo = f[out]
            prc.append(dict(state=desc(c, pch, k), size=len(ids), pi=float(p),
                            tier='deep' if dp else ('deep_mod_twins' if mt else ('deep_penalty_only' if pen else 'non-deep')),
                            max_inv=float(fo.max()), n_neutral=int((np.abs(fo) <= TOL).sum()), n_adv=int((fo > TOL).sum()),
                            neutral_mutants=[c.names[q] for q in np.nonzero(out & (np.abs(f) <= TOL))[0]][:8]))
        res['published_recurrent'] = prc
        # published recurrent states (pi > 1e-6) that are not enumerated candidates
        cset = set(tuple(sorted(int(c.cid[i]) for i in x['ids'])) for x in cands if x['status'] == 'stable')
        res['discovery']['published_recurrent_not_candidates'] = [
            (desc(c, pch, k), float(p)) for k, p in zip(pch.keys_list, pch.pi) if p > 1e-6 and tuple(sorted(pch.states[k][0])) not in cset][:20]
    # ---- 5. full re-solve
    tf = time.time()
    # seeds: every candidate with no strictly advantageous outside mutant (the possible traps; all deep tiers are among
    # them), or every stable candidate with full_seed; plus every state the published chain expanded
    sel = [x for x in cands if x['status'] == 'stable' and x['size'] > 1 and (x['n_adv'] == 0 or full_seed)]
    seeds = [(list(int(c.cid[i]) for i in x['ids']), x['x']) for x in sel]
    layer = [x['n_adv'] == 0 for x in sel]          # one layer of targets only around possible traps
    if not skip_published:
        for k in pch.trans:
            ids_, x_, kind_ = pch.states[k]
            if kind_ == 'poly':
                seeds.append((list(ids_), list(x_))); layer.append(False)
    fch = LogChain(c.provider(), N=N, Ufull=c.U if twins else None, twins=twins, est_floor=est_floor, theta=1.0, max_states=10 ** 9,
                   **{k: v for k, v in c.chain_kw.items() if k in ('w',)})
    fch.explore_log(extra_states=seeds, log_theta=log_theta, max_states=max_states + len(seeds), verbose=verbose, layer_mask=layer)
    keys_all, lpi_all, info, out_un, rec = fch.solve_sparse()
    keys = [keys_all[i] for i in rec]
    lpi = lpi_all[rec]
    LA, _ = fch.log_matrix(keys)
    info['n_expanded'] = len(keys_all); info['n_recurrent'] = len(keys)
    pi = np.exp(lpi)
    st = stat_of(c, fch, keys, pi)
    sup = support_and_transitions(c, fch, keys, LA, lpi)
    deepkeys = {}
    for x in deep:
        k = cand_key(fch, x, c)
        deepkeys[k] = x
    pos = {k: i for i, k in enumerate(keys)}
    for k, x in deepkeys.items():
        x['resolve_pi'] = float(pi[pos[k]]) if k in pos else 0.0
        x['resolve_log10_pi'] = float(lpi[pos[k]] / L10) if k in pos else None
        x['resolve_expanded'] = k in fch.trans
        x['resolve_recurrent'] = k in pos
    res['resolve'] = dict(stat=st, n_states=len(keys), n_seeded=len(seeds), n_seeded_traps=int(sum(layer)), seeds_all_stable=full_seed, log10_cut=float(fch.log_cut / L10) if np.isfinite(fch.log_cut) else None,
                          n_cand_left=fch.n_cand_left, closed=info, mass_deep=float(sum(x.get('resolve_pi') or 0 for x in strict)),
                          mass_deep_any={t: float(sum(x.get('resolve_pi') or 0 for x in deep if x['tier'] == t)) for t in ('deep', 'deep_mod_twins', 'deep_penalty_only')},
                          mass_poly=float(sum(p for k, p in zip(keys, pi) if len(fch.states[k][0]) > 1)),
                          indeterminate=len(fch.indeterminate), twin_moves=fch.n_twin_moves, twins=twins, est_floor=est_floor, n_floored=fch.n_floored,
                          support=sup, time_s=time.time() - tf, resid=balance_residual(LA, pi))
    if not skip_published:
        # missed deep states: re-solved pi and best path weight from the published top state
        topk = pch.keys_list[int(np.argmax(pch.pi))]
        res['discovery']['missed_detail'] = []
        for x in sorted(missed, key=lambda x: -(x.get('resolve_pi') or 0))[:15]:
            k = cand_key(fch, x, c)
            bp = best_path(LA, pos.get(topk), pos.get(k)) if topk in pos and k in pos else None
            res['discovery']['missed_detail'].append(dict(tier=x['tier'], state=' + '.join('%s:%.3f' % (c.names[i], xi) for i, xi in zip(x['ids'], x['x'])),
                                                          mass_sum=x['mass_sum'], resolve_pi=x.get('resolve_pi'),
                                                          log10_best_path_from_published_top=bp))
    res['deep_states'] = [dict(state=' + '.join('%s:%.4f' % (c.names[i], xi) for i, xi in zip(x['ids'], x['x'])), size=x['size'], tier=x['tier'],
                               mass_sum=x['mass_sum'], mass_min=x['mass_min'], max_inv=x['max_inv'], deep_pen=x['deep_pen'],
                               in_published_explored=x.get('in_published_explored'), in_published_recurrent=x.get('in_published_recurrent'),
                               resolve_pi=x.get('resolve_pi'), resolve_log10_pi=x.get('resolve_log10_pi'), resolve_recurrent=x.get('resolve_recurrent'),
                               stat=c.stat([int(c.cid[i]) for i in x['ids']], x['x'], N))
                         for x in sorted(deep, key=lambda x: -(x.get('resolve_pi') or 0))]
    # full mutant lists for the deep states that carry re-solved mass >= 1e-4 (and the 5 heaviest by prior)
    show = [x for x in deep if (x.get('resolve_pi') or 0) >= 1e-4] + sorted(deep, key=lambda x: -x['mass_sum'])[:5]
    seen = set(); res['deep_mutant_lists'] = []
    for x in show:
        t = tuple(x['ids'])
        if t in seen: continue
        seen.add(t)
        res['deep_mutant_lists'].append(dict(state=' + '.join('%s:%.4f' % (c.names[i], xi) for i, xi in zip(x['ids'], x['x'])),
                                             outside=deep_detail(c.U, c.names, c.mu, x)))
    pubv = PUBLISHED.get((name, N)) or {}
    res['discrepancy'] = {k: float(st.get(k, np.nan) - v) for k, v in pubv.items()}
    if not skip_published:
        res['discrepancy_vs_rerun'] = {k: float(st.get(k, np.nan) - res['published_rerun']['stat'].get(k, np.nan)) for k in c.headlines}
    res['time_s'] = time.time() - t0
    if verbose:
        print('[%s N=%d] re-solve: %s | states %d, log10 cut %s, closed %s, deep mass %.4f | top %s (%.4f) | discrepancy %s (%.0fs)' % (
            name, N, {k: round(v, 4) for k, v in st.items()}, len(keys), res['resolve']['log10_cut'], info.get('n_closed'),
            res['resolve']['mass_deep'], sup[0]['state'], sup[0]['pi'], {k: round(v, 4) for k, v in res['discrepancy'].items()}, res['time_s']), flush=True)
    return res


def balance_residual(LA, pi):
    """max over states with pi_j > 1e-12 of |log(sum_i pi_i q_ij) - log(pi_j sum_k q_jk)| (relative global balance)."""
    n = LA.shape[0]
    with np.errstate(divide='ignore'):
        lpi = np.log(np.maximum(pi, 0))
    worst = 0.0
    for j in range(n):
        if pi[j] <= 1e-12:
            continue
        row = LA[j].copy(); row[j] = NEG
        lo = lpi[j] + np.logaddexp.reduce(row[np.isfinite(row)]) if np.isfinite(row).any() else NEG
        col = LA[:, j] + lpi; col[j] = NEG
        col = col[np.isfinite(col)]
        li = np.logaddexp.reduce(col) if len(col) else NEG
        if np.isfinite(lo) and np.isfinite(li):
            worst = max(worst, abs(lo - li))
        elif np.isfinite(lo) or np.isfinite(li):
            worst = float('inf')
    return float(worst)


def best_path(LA, src, dst):
    """max-weight path src -> dst in log weights (Dijkstra on -log w); log10 weight."""
    import heapq
    if src is None or dst is None:
        return None
    n = LA.shape[0]
    dist = np.full(n, np.inf); dist[src] = 0.0
    h = [(0.0, src)]
    while h:
        dd, u = heapq.heappop(h)
        if dd > dist[u]: continue
        if u == dst:
            return float(-dd / L10)
        for v in np.nonzero(np.isfinite(LA[u]))[0]:
            if v == u: continue
            nd = dd - LA[u, v]
            if nd < dist[v]:
                dist[v] = nd; heapq.heappush(h, (nd, v))
    return None


def _jsonable(o):
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, float) and (math.isinf(o) or math.isnan(o)):
        return str(o)
    return o


def exhaustive_compare(U, mu, names, N, stat, theta=1e-7, eager_poly=True, dps=50):
    """A small exhaustive instance: every reachable state expanded; the published linear solve, log-domain GTH and
    mpmath GTH on the identical generator; plus the published lazy exploration's own answer."""
    from dollar_partitions import ClassProvider
    out = {}
    lazy = Chain(ClassProvider(U, mu), N=N, w=0.3, theta=theta, eager_poly=eager_poly).explore()
    out['lazy_published'] = dict(stat=_stat_lin(lazy, stat), n_expanded=len(lazy.trans), near_closed=int(lazy.near_closed))
    ch = LogChain(ClassProvider(U, mu), N=N, w=0.3).explore_closure(max_states=5000)
    keys = list(ch.trans)
    LA, _ = ch.log_matrix(keys)
    lpi, info = stationary_log(LA)
    lin_keys, lin_pi, nc, nt, ae = linear_stationary(ch.trans, ch.seed_weight, ch.states)
    lin_pi = np.array([dict(zip(lin_keys, lin_pi))[k] for k in keys])
    lmp = gth_mp(LA, dps) if info['n_closed'] == 1 and len(keys) <= 400 else None
    fin = np.isfinite(lpi)
    out['n_states'] = len(keys); out['closure_complete'] = bool(ch.closure_complete); out['closed'] = info
    out['underflow_edges'] = int(ch.underflow)
    out['log10_rate_range'] = [float(np.nanmin(np.where(np.isfinite(LA), LA, np.nan)) / L10), float(np.nanmax(np.where(np.isfinite(LA), LA, np.nan)) / L10)]
    st = lambda p: {kk: float(v) for kk, v in _stat_keys(ch, keys, p, stat).items()}
    out['log_gth'] = st(np.exp(lpi)); out['linear'] = st(lin_pi); out['linear_near_closed'] = int(nc)
    if lmp is not None:
        out['mpmath'] = st(np.exp(lmp))
        out['max_abs_dlogpi_log_vs_mp'] = float(np.max(np.abs(lpi[fin] - lmp[fin])))
        out['min_log10_pi'] = float(lmp[fin].min() / L10)
        out['max_abs_dpi_linear_vs_mp'] = float(np.max(np.abs(lin_pi - np.exp(lmp))))
    out['tv_linear_vs_log'] = float(0.5 * np.abs(lin_pi - np.exp(lpi)).sum())
    out['resid_log'] = balance_residual(LA, np.exp(lpi)); out['resid_linear'] = balance_residual(LA, lin_pi)
    out['states'] = [(' + '.join('%s:%.3f' % (names[i], xi) for i, xi in zip(*ch.states[k][:2])), float(np.exp(lpi[j])),
                      float(lin_pi[j]), (float(np.exp(lmp[j])) if lmp is not None else None)) for j, k in enumerate(keys)]
    return out


def _stat_lin(ch, stat):
    return _stat_keys(ch, ch.keys_list, ch.pi, stat)


def _stat_keys(ch, keys, pi, stat):
    acc = defaultdict(float)
    for k, p in zip(keys, pi):
        if p <= 0: continue
        for kk, v in stat(*ch.states[k][:2], ch.N).items():
            acc[kk] += p * v
    return dict(acc)


def cmd_controls(a):
    res = {}
    import modal as M
    prov = M.build(6)[3]
    names = list(prov.names); P = prov.PCC
    idx = {s: i for i, s in enumerate(names)}
    for label, subset in (('C+FairBot', ['C', 'BOX(THEM(ME))']), ('D+C+FairBot', ['D', 'C', 'BOX(THEM(ME))'])):
        cl = [idx[s] for s in subset]
        U = prov.Ufull[np.ix_(cl, cl)]; mu = np.array([prov.classes[i][2] for i in cl]); mu = mu / mu.sum()
        Ps = P[np.ix_(cl, cl)]
        cands, counts = enumerate_candidates(U, mu)
        stat = lambda ids, x, N, Ps=Ps: dict(pcc=float(np.asarray(x) @ Ps[np.ix_(list(ids), list(ids))] @ np.asarray(x)))
        r = dict(subset=subset, n_deep=sum(1 for x in cands if x['deep']), candidates=[(x['ids'], x['x'], x['deep'], x['max_inv']) for x in cands])
        r.update(exhaustive_compare(U, mu, subset, a.N_neg, stat))
        res['negative_' + label] = r
        print(label, json.dumps(_jsonable({k: v for k, v in r.items() if k not in ('states', 'candidates')}))[:900], flush=True)
    # the small exhaustive instance with a deep state: the modal-dollar reduced subsystem {S3, S5, A5} at N = 1e4
    import modal_dollar as MD
    d = MD.data('modal', 7)
    funcs = [MD.S['S3'], MD.S['S5'], MD.ACC5]
    if funcs is not None:
        sd = MD.subdata(d, funcs)
        r = dict(subset=sd['names'])
        cands, counts = enumerate_candidates(sd['U'], sd['mu'])
        r['candidates'] = [(x['ids'], x['x'], x['deep'], x['max_inv']) for x in cands if x['status'] == 'stable']
        r.update(exhaustive_compare(np.round(sd['U'], 9), sd['mu'], sd['names'], a.N_neg, _dollar_stat(sd)))
        res['precision_S3_S5_A5'] = r
        print('S3/S5/A5', json.dumps(_jsonable({k: v for k, v in r.items() if k not in ('states', 'candidates')}))[:900], flush=True)
    json.dump(_jsonable(res), open(os.path.join(OUT, 'controls.json'), 'w'), indent=1, default=str)


def cmd_cell(a):
    for N in a.N:
        r = run_cell(a.cell, N, log_theta=math.log(a.theta), max_states=a.max_states, twins=a.twins,
                     extra_only_deep=a.only_deep, skip_published=a.skip_published, triples=not a.no_triples, pool_K=a.pool_K,
                     full_seed=a.full_seed, est_floor=a.est_floor, closure_nodes=a.closure)
        fn = os.path.join(OUT, '%s_N%d%s%s%s%s.json' % (a.cell, N, '_twins' if a.twins else '', '_fullseed' if a.full_seed else '', '_estfloor' if a.est_floor else '', a.tag))
        r['theta_log'] = a.theta
        json.dump(_jsonable(r), open(fn, 'w'), indent=1, default=str)


# ================================================================ fixed-role chains (union, three-player dollar)
def solve_edges_log(n, src, dst, lw, dense_max=6000):
    """independent check solver: closed classes by csgraph, then dense log-domain GTH (chain_log.gth_log) on the
    closed class (or sparse log elimination beyond dense_max).  Returns (log pi, info)."""
    import scipy.sparse as sp_, scipy.sparse.csgraph as csg_
    src = np.asarray(src); dst = np.asarray(dst); lw = np.asarray(lw, float)
    m = (src != dst) & np.isfinite(lw)
    src, dst, lw = src[m], dst[m], lw[m]
    G = sp_.csr_matrix((np.ones(len(src), np.int8), (src, dst)), shape=(n, n))
    nc, lab = csg_.connected_components(G, directed=True, connection='strong')
    leaving = np.zeros(nc, bool); cr = lab[src] != lab[dst]; leaving[lab[src[cr]]] = True
    closed = [k for k in range(nc) if not leaving[k]]
    info = dict(n_components=int(nc), n_closed=len(closed), closed_sizes=sorted([int((lab == k).sum()) for k in closed], reverse=True)[:5])
    lpi = np.full(n, NEG)
    if len(closed) != 1:
        info['error'] = 'not one closed class'
        return lpi, info
    rec = np.nonzero(lab == closed[0])[0]
    loc = -np.ones(n, np.int64); loc[rec] = np.arange(len(rec))
    mm = (loc[src] >= 0) & (loc[dst] >= 0)
    if len(rec) <= dense_max:
        nr = len(rec)
        a_, b_, w_ = loc[src[mm]], loc[dst[mm]], lw[mm]
        key = a_ * nr + b_
        o = np.argsort(key, kind='stable')
        key, w_ = key[o], w_[o]
        uk, first = np.unique(key, return_index=True)
        comb = np.logaddexp.reduceat(w_, first) if len(w_) else w_
        LA = np.full((nr, nr), NEG)
        LA[uk // nr, uk % nr] = comb
        order, _ = order_by_exit(LA)
        lx = gth_log(LA[np.ix_(order, order)])
        out = np.empty(nr); out[order] = lx
        info['solver'] = 'chain_log.gth_log (dense)'
    else:
        from dollar3_solve import log_stationary
        out = log_stationary(len(rec), loc[src[mm]], loc[dst[mm]], lw[mm], core=3000)
        info['solver'] = 'dollar3_solve.log_stationary'
    lpi[rec] = out
    return lpi, info


def union_strict_ne(C, PAY, mass, tol=TOL):
    """every monomorphic (boss, worker, worker) class triple that is a strict Nash equilibrium against every
    admissible (mass > 0) single-slot mutant: the deep states of a fixed-role chain (no interior rest point of a
    multi-population replicator is asymptotically stable, so these are the only candidate traps)."""
    Jc, tg = C['Jc'], C['tagc']
    KB, KW = int(C['KcB']), int(C['KcW'])
    admB = mass[0, :KB] > 0; admW = mass[1, :KW] > 0
    U0 = np.empty((KB, KW, KW)); U1 = np.empty((KB, KW, KW)); U2 = np.empty((KB, KW, KW))
    for b in range(KB):
        J = Jc[b]
        P_ = PAY[J, tg[:, None], tg[None, :]]
        U0[b], U1[b], U2[b] = P_[..., 0], P_[..., 1], P_[..., 2]

    def top2(A, axis, adm):
        A = np.moveaxis(A, axis, 0)[adm]
        idx = np.nonzero(adm)[0]
        o = np.argsort(-A, axis=0)
        best = np.take_along_axis(A, o[:1], 0)[0]; second = np.take_along_axis(A, o[1:2], 0)[0]
        return idx[o[0]], best, second
    ib, bb, sb = top2(U0, 0, admB)                         # per (x, y)
    i1, b1, s1 = top2(U1, 1, admW)                         # per (b, y)
    i2, b2, s2 = top2(U2, 2, admW)                         # per (b, x)
    out = []
    for b in np.nonzero(admB)[0]:
        for y in np.nonzero(admW)[0]:
            if b1[b, y] - s1[b, y] <= tol: continue
            x = i1[b, y]
            if i2[b, x] != y or b2[b, x] - s2[b, x] <= tol: continue
            if ib[x, y] != b or bb[x, y] - sb[x, y] <= tol: continue
            out.append((int(b), int(x), int(y)))
    return out


def cmd_union(a):
    import union as UN, union_run as UR
    from union_chain import UChain
    t0 = time.time()
    d, C, nmw, nmb = UR.load('quorum')
    res = dict(cell='union-quorum', c=a.c, N=a.N, KcB=int(C['KcB']), KcW=int(C['KcW']))

    def summ(ch, pi):
        s = np.array([UR.state_info(int(t))['summ'] for t in ch.typ])
        return {UN.SUMM[k]: float(pi[s == k].sum()) for k in range(7)}
    ch = UChain(C, a.c, a.N, w=0.3, theta=1e-9, max_states=400000, core_max=2500, promote=1e-5, arm='quorum', verbose=False)
    ch.max_rounds = 40
    ch.explore_hybrid(UR.seeds(ch, nmw, nmb))
    res['published_rerun'] = dict(summary=summ(ch, ch.pi), states=len(ch.codes), core=int(ch.is_core.sum()), rel_cut_change=float(ch.rel_cut_change),
                                  solver='gth_scaled' if a.N <= 2000 else 'dense_log_gth', time_s=time.time() - t0)
    print('union published re-run', res['published_rerun'], flush=True)
    t1 = time.time()
    lpi2, info = solve_edges_log(len(ch.codes), ch.src, ch.dst_idx, ch.pr)
    pi2 = np.exp(lpi2)
    fin = np.isfinite(lpi2) & np.isfinite(ch.lpi)
    res['solver'] = dict(info=info, summary=summ(ch, pi2), tv=float(0.5 * np.abs(pi2 - ch.pi).sum()),
                         max_abs_dlogpi=float(np.max(np.abs(lpi2[fin] - ch.lpi[fin]))) if fin.any() else None, time_s=time.time() - t1)
    print('union solver check', res['solver'], flush=True)
    t2 = time.time()
    ne = union_strict_ne(C, ch.PAY, ch.mass)
    idx = ch.index
    res['discovery'] = dict(n_strict_ne=len(ne), in_published_explored=sum(1 for t in ne if ch.code(*t) in idx),
                            published_pi=[(UR.describe(d, C, *t), float(ch.pi[idx[ch.code(*t)]]) if ch.code(*t) in idx else None) for t in ne][:60],
                            time_s=time.time() - t2)
    print('union discovery', {k: v for k, v in res['discovery'].items() if k != 'published_pi'}, flush=True)
    t3 = time.time()
    ch2 = UChain(C, a.c, a.N, w=0.3, theta=a.theta, max_states=a.max_states, core_max=a.core_max, promote=1e-6, arm='quorum', verbose=True)
    ch2.max_rounds = 60
    seeds = list(UR.seeds(ch2, nmw, nmb)) + [ch2.code(*t) for t in ne]
    ch2.explore_hybrid(seeds)
    lpi3, info3 = solve_edges_log(len(ch2.codes), ch2.src, ch2.dst_idx, ch2.pr, dense_max=4000)
    pi3 = np.exp(lpi3)
    res['resolve'] = dict(summary_hybrid=summ(ch2, ch2.pi), summary_check=summ(ch2, pi3), check_info=info3, states=len(ch2.codes),
                          core=int(ch2.is_core.sum()), rel_cut_change=float(ch2.rel_cut_change), theta=a.theta, time_s=time.time() - t3,
                          ne_pi=[(UR.describe(d, C, *t), float(ch2.pi[ch2.index[ch2.code(*t)]]) if ch2.code(*t) in ch2.index else None) for t in ne][:60])
    order = np.argsort(-ch2.pi)[:12]
    res['resolve']['support'] = [(UR.describe(d, C, *ch2.decode(int(ch2.codes[k]))), float(ch2.pi[k])) for k in order]
    res['resolve']['transitions'] = []
    for k in order[:5]:
        ex, tot = UR.exits(ch2, int(ch2.codes[k]), top=4)
        res['resolve']['transitions'].append(dict(state=UR.describe(d, C, *ch2.decode(int(ch2.codes[k]))), exit_by_kind=tot,
                                                  top=[dict(p=e['prob'], kind=e['kind'], slot=['B', 'W1', 'W2'][e['slot']], to=e['summ_to']) for e in ex]))
    pubv = {'fair': 0.003, 'intermediate': 0.013, 'zero wage': 0.48}
    res['discrepancy_vs_published'] = {k: res['resolve']['summary_hybrid'][k] - v for k, v in pubv.items()}
    res['discrepancy_vs_rerun'] = {k: res['resolve']['summary_hybrid'][k] - res['published_rerun']['summary'][k] for k in res['published_rerun']['summary']}
    print('union re-solve', {k: v for k, v in res['resolve'].items() if k in ('summary_hybrid', 'summary_check', 'states', 'rel_cut_change')}, flush=True)
    res['time_s'] = time.time() - t0
    json.dump(_jsonable(res), open(os.path.join(OUT, 'union-quorum_c%g_N%d.json' % (a.c, a.N)), 'w'), indent=1, default=str)


def dollar3_strict_ne(ch, pool, tol=TOL):
    """strict-NE class triples among pool[s] (class ids per slot): every admissible (mass > 0) single-slot mutant
    class earns strictly less than the resident in its slot.  Returns list of (a, b, c) and the count tested."""
    import dollar3 as D3
    out = []
    n = 0
    reps = ch.reps
    adm = [np.nonzero(ch.mass[s] > 0)[0] for s in range(3)]
    for a_ in pool[0]:
        for b_ in pool[1]:
            for c_ in pool[2]:
                n += 1
                t = (int(a_), int(b_), int(c_))
                x = [reps[s, t[s]] for s in range(3)]
                ok = True
                for s in range(3):
                    U, T = D3.slot_row(ch.ia, *ch.A, s, x[0], x[1], x[2])
                    u0 = U[x[s], s]
                    q = adm[s][adm[s] != t[s]]
                    if (U[reps[s, q], s] > u0 - 1e-9).any():
                        ok = False; break
                if ok:
                    out.append(t)
    return out, n


def cmd_dollar3(a):
    import dollar3 as D3, dollar3_run as DR
    t0 = time.time()
    res = dict(cell='dollar3-' + a.arm, N=a.N)

    def mass_by_type(ch, pi):
        return {D3.OUT_NAMES[t]: float(pi[ch.typ == t].sum()) for t in range(5)}
    ch, S = DR.build_chain(a.arm, a.N, 0.3, 1e-10, 400000, core_max=2500)
    ch.verbose = True
    ch.explore_hybrid()
    res['published_rerun'] = dict(mass_by_type=mass_by_type(ch, ch.pi), states=len(ch.codes), core=int(ch.is_core.sum()),
                                  rel_cut_change=float(ch.rel_cut_change), time_s=time.time() - t0)
    print('dollar3 published re-run', res['published_rerun'], flush=True)
    t1 = time.time()
    lpi2, info = solve_edges_log(len(ch.codes), ch.src, ch.dst_idx, ch.pr, dense_max=3000)
    pi2 = np.exp(lpi2)
    fin = np.isfinite(lpi2) & np.isfinite(ch.lpi)
    res['solver'] = dict(info=info, mass_by_type=mass_by_type(ch, pi2), tv=float(0.5 * np.abs(pi2 - ch.pi).sum()),
                         max_abs_dlogpi=float(np.max(np.abs(lpi2[fin] - ch.lpi[fin]))) if fin.any() else None, time_s=time.time() - t1)
    print('dollar3 solver check', res['solver'], flush=True)
    # discovery: strict-NE triples on a pool per slot (constants, the K_c heaviest classes, published support classes)
    t2 = time.time()
    pool = []
    sup = [ch.decode(int(cd)) for cd in ch.codes[ch.pi > 1e-6]]
    for s in range(3):
        p = set(int(v) for v in ch.const_class[s])
        p |= set(int(v) for v in np.argsort(-ch.mass[s])[:a.Kc])
        p |= set(int(t[s]) for t in sup)
        pool.append(sorted(p))
    ne, n_tested = dollar3_strict_ne(ch, pool)
    idx = ch.index
    res['discovery'] = dict(pool_sizes=[len(p) for p in pool], Kc=a.Kc, n_tested=n_tested, n_strict_ne=len(ne),
                            in_published_explored=sum(1 for t in ne if ch.code(*t) in idx),
                            published_pi=[(DR.describe(ch, ch.code(*t)), float(ch.pi[idx[ch.code(*t)]]) if ch.code(*t) in idx else None) for t in ne][:60],
                            time_s=time.time() - t2)
    print('dollar3 discovery', {k: v for k, v in res['discovery'].items() if k != 'published_pi'}, flush=True)
    json.dump(_jsonable(res), open(os.path.join(OUT, 'dollar3-%s_N%d.json' % (a.arm, a.N)), 'w'), indent=1, default=str)
    # re-solve: smaller theta, larger core, strict-NE triples seeded
    t3 = time.time()
    ch2, S2 = DR.build_chain(a.arm, a.N, 0.3, a.theta, 600000, core_max=a.core_max, promote=1e-6)
    ch2.verbose = True
    seeds = [ch2.code(a_, b_, c_) for a_ in ch2.const_class[0] for b_ in ch2.const_class[1] for c_ in ch2.const_class[2]]
    seeds += [ch2.code(*t) for t in ne]
    ch2.explore_hybrid(seeds)
    lpi3, info3 = solve_edges_log(len(ch2.codes), ch2.src, ch2.dst_idx, ch2.pr, dense_max=3000)
    res['resolve'] = dict(mass_by_type=mass_by_type(ch2, ch2.pi), mass_by_type_check=mass_by_type(ch2, np.exp(lpi3)), check_info=info3,
                          states=len(ch2.codes), core=int(ch2.is_core.sum()), rel_cut_change=float(ch2.rel_cut_change), theta=a.theta,
                          core_max=a.core_max, time_s=time.time() - t3,
                          ne_pi=[(DR.describe(ch2, ch2.code(*t)), float(ch2.pi[ch2.index[ch2.code(*t)]]) if ch2.code(*t) in ch2.index else None) for t in ne][:60])
    order = np.argsort(-ch2.pi)[:12]
    res['resolve']['support'] = [(DR.describe(ch2, ch2.codes[k]), float(ch2.pi[k]), D3.OUT_NAMES[ch2.typ[k]]) for k in order]
    pubv = {'grand': 0.0161, 'fair pair': 0.366, 'unfair pair': 0.615}
    res['discrepancy_vs_published'] = {k: res['resolve']['mass_by_type'][k] - v for k, v in pubv.items()}
    res['discrepancy_vs_rerun'] = {k: res['resolve']['mass_by_type'][k] - res['published_rerun']['mass_by_type'][k] for k in pubv}
    print('dollar3 re-solve', {k: res['resolve'][k] for k in ('mass_by_type', 'mass_by_type_check', 'states', 'rel_cut_change')}, flush=True)
    res['time_s'] = time.time() - t0
    json.dump(_jsonable(res), open(os.path.join(OUT, 'dollar3-%s_N%d.json' % (a.arm, a.N)), 'w'), indent=1, default=str)


def _fmt(v, p=4):
    if v is None:
        return '–'
    if isinstance(v, str):
        return v
    if v != 0 and abs(v) < 10 ** -p:
        return '%.1e' % v
    return ('%.' + str(p) + 'f') % v


def cmd_report(a):
    """runs/solver-audit.md and runs/solver-audit.json from runs/solver_audit/*.json."""
    import glob
    cells = {}
    for f in sorted(glob.glob(os.path.join(OUT, '*.json'))):
        cells[os.path.basename(f)[:-5]] = json.load(open(f))
    json.dump(cells, open(os.path.join(ROOT, 'runs', 'solver-audit.json'), 'w'), indent=1, default=str)
    L = ['# Solver audit of the published ε→0 chains (generated by `python3 src/solver_audit.py report`)', '',
         'Spec `specs/2026-10-05-solver-audit.md`; predictions `predictions/2026-10-05-solver-audit.md`. Per cell: discovery '
         '(candidate supports of ≤ 3 classes from the class table, deep tiers), the published chain re-run, rates and solver '
         'on the published generator, the full re-solve (log domain), support and transitions, discrepancy.', '']
    order = [k for k in cells if not k.startswith(('controls', 'union', 'dollar3-modal'))]
    L += ['## One-population cells (ε→0 attractor chain)', '',
          '| cell | N | published | re-run (linear, published config) | log GTH on the published generator | full re-solve | Δ (re-solve − published) | underflowed edges | deep tiers (strict / mod twins / penalty) | missed deep tiers | re-solve states, log10 cut |',
          '|---|---|---|---|---|---|---|---|---|---|---|']
    for k in order:
        r = cells[k]
        if 'resolve' not in r:
            continue
        hs = [h for h in ('eff', 'half', 'pcc') if h in r['resolve']['stat']]
        pub = r.get('published') or {}
        pr = r.get('published_rerun', {}).get('stat', {})
        sl = r.get('solver', {}).get('log_gth_stat', {})
        rs = r['resolve']['stat']
        dd = r['discovery']
        L.append('| %s | %d | %s | %s | %s | %s | %s | %s | %s / %s / %s | %s | %d, %s |' % (
            k, r['N'], ' · '.join('%s %s' % (h, _fmt(pub.get(h))) for h in hs if h in pub) or '–',
            ' · '.join('%s %s' % (h, _fmt(pr.get(h))) for h in hs), ' · '.join('%s %s' % (h, _fmt(sl.get(h))) for h in hs),
            ' · '.join('%s %s' % (h, _fmt(rs.get(h))) for h in hs), ' · '.join('%s %+.4f' % (h, v) for h, v in r.get('discrepancy', {}).items()),
            r.get('rates', {}).get('n_underflow', '–'), dd.get('n_deep'), dd.get('n_deep_mod_twins'), dd.get('n_deep_penalty_only'),
            dd.get('deep_missed', '–'), r['resolve']['n_states'], _fmt(r['resolve'].get('log10_cut'), 1)))
    L += ['']
    for k in order:
        r = cells[k]
        if 'resolve' not in r:
            continue
        L += ['### %s, N = %d' % (k, r['N']), '']
        dd = r['discovery']
        L.append('**Discovery** (K = %d classes; triples %s; coverage: every singleton, every pair, every triple of the %s; supports of ≥ 4 classes and '
                 'non-isolated rest sets are not enumerated): counts %s. Deep strict %d, deep modulo twins %d, deep with penalty only %d. '
                 'Published explored set holds %s of the deep-tier states; missed %s.' % (
                     r['K'], 'exhaustive' if dd.get('pool_K', r['K']) >= r['K'] else 'pool %d' % dd['pool_K'], 'class table' if dd.get('pool_K', r['K']) >= r['K'] else 'pool',
                     json.dumps(dd.get('counts')), dd.get('n_deep', 0), dd.get('n_deep_mod_twins', 0), dd.get('n_deep_penalty_only', 0),
                     dd.get('deep_in_published_explored', '–'), dd.get('deep_missed', '–')))
        if dd.get('missed_detail'):
            L.append('Missed deep-tier states (re-solved π, best path from the published top state, log10): ' + '; '.join(
                '%s [%s] π %s path %s' % (m['state'], m['tier'], _fmt(m['resolve_pi'], 3), _fmt(m['log10_best_path_from_published_top'], 1))
                for m in dd['missed_detail'][:6]) + '.')
        if r.get('published_recurrent'):
            L.append('Published recurrent states (π > 10⁻⁶) by tier: ' + '; '.join('%s %s (%s)' % (p['state'][:120], _fmt(p['pi'], 4), p['tier'])
                                                                                  for p in r['published_recurrent'][:6]) + '.')
        if 'rates' in r:
            rt = r['rates']; sv = r['solver']
            L.append('**Rates** (identical transition model, same explored set: %s): %d edges, max |Δ log w| %.1e on non-underflowed edges, %d underflowed to 0, %d denormal. '
                     '**Solver** on the published generator: linear %s vs log GTH %s (TV %.4f); linear near-closed classes %d; balance residual (log units) linear %s, log %s.' % (
                         rt['same_explored_set'], rt['n_edges'], rt['max_abs_log_err'], rt['n_underflow'], rt['n_denormal'],
                         json.dumps({h: round(v, 4) for h, v in sv['linear_stat'].items() if h in ('eff', 'half', 'pcc')}),
                         json.dumps({h: round(v, 4) for h, v in sv['log_gth_stat'].items() if h in ('eff', 'half', 'pcc')}),
                         sv['tv'], sv['linear_near_closed'], _fmt(sv['resid_linear'], 3), _fmt(sv['resid_log'], 3)))
        rs = r['resolve']
        L.append('**Re-solve**: %d recurrent of %d expanded states (%d seeded, %d trap candidates with a layer of targets), log10 cut %s, closed classes %s, '
                 'polymorphic mass %.4f, deep-tier mass %s, indeterminate %d; statistic %s.' % (
                     rs['n_states'], rs['closed'].get('n_expanded', rs['n_states']), rs['n_seeded'], rs.get('n_seeded_traps', 0),
                     _fmt(rs.get('log10_cut'), 1), rs['closed'].get('n_closed'), rs['mass_poly'], json.dumps({t: float('%.3g' % v) for t, v in rs.get('mass_deep_any', {}).items()}),
                     rs['indeterminate'], json.dumps({h: round(v, 4) for h, v in rs['stat'].items()})))
        L.append('Support and transitions (π; log10 exit per mutation event; leading exits with log10 rate and mutants):')
        for s in rs['support'][:6]:
            L.append('- %s: π %s (log10 %.1f), exit %s; %s' % (s['state'], _fmt(s['pi'], 4), s['log10_pi'], _fmt(s['log10_exit'], 1),
                                                            '; '.join('→ %s at %.1f via %s' % (e['to'][:90], e['log10_rate'], ', '.join(m[0] for m in e['mutants'][:2]))
                                                                      for e in s['exits'][:3])))
        L.append('')
    if 'controls' in cells:
        L += ['## Controls and the precision instance', '']
        for k, r in cells['controls'].items():
            L.append('- **%s** (%s): %d states, closure complete %s, underflowed edges %d, log10 rate range %s; lazy published %s; linear %s; log GTH %s; mpmath %s; max |Δ log π| log vs mpmath %s; min log10 π %s; TV linear vs log %.2e; residual linear %s / log %s.' % (
                k, ', '.join(r['subset']), r['n_states'], r['closure_complete'], r['underflow_edges'], [round(v, 1) for v in r['log10_rate_range']],
                json.dumps({h: round(v, 6) for h, v in r['lazy_published']['stat'].items() if h in ('eff', 'pcc', 'half')}),
                json.dumps({h: round(v, 6) for h, v in r['linear'].items() if h in ('eff', 'pcc', 'half')}),
                json.dumps({h: round(v, 6) for h, v in r['log_gth'].items() if h in ('eff', 'pcc', 'half')}),
                json.dumps({h: round(v, 6) for h, v in r.get('mpmath', {}).items() if h in ('eff', 'pcc', 'half')}),
                _fmt(r.get('max_abs_dlogpi_log_vs_mp'), 3), _fmt(r.get('min_log10_pi'), 1), r['tv_linear_vs_log'], _fmt(r['resid_linear'], 3), _fmt(r['resid_log'], 3)))
        L.append('')
    for k in cells:
        if k.startswith(('union', 'dollar3-modal')):
            r = cells[k]
            L += ['## %s, N = %s' % (k, r['N']), '', '```', json.dumps({kk: r[kk] for kk in r if kk not in ('resolve',)}, indent=1, default=str)[:6000], '```', '']
            if 'resolve' in r:
                L += ['```', json.dumps(r['resolve'], indent=1, default=str)[:6000], '```', '']
    open(os.path.join(ROOT, 'runs', 'solver-audit-tables.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L[:60]))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    p = sub.add_parser('cell')
    p.add_argument('--cell', required=True)
    p.add_argument('--N', type=int, nargs='+', required=True)
    p.add_argument('--theta', type=float, default=1e-30)
    p.add_argument('--max_states', type=int, default=20000)
    p.add_argument('--twins', action='store_true')
    p.add_argument('--only_deep', action='store_true')
    p.add_argument('--skip_published', action='store_true')
    p.add_argument('--no_triples', action='store_true')
    p.add_argument('--pool_K', type=int, default=None)
    p.add_argument('--full_seed', action='store_true')
    p.add_argument('--tag', default='')
    p.add_argument('--est_floor', action='store_true')
    p.add_argument('--closure', type=int, default=0)
    p = sub.add_parser('union')
    p.add_argument('--c', type=float, default=0.5)
    p.add_argument('--N', type=float, default=1000)
    p.add_argument('--theta', type=float, default=1e-11)
    p.add_argument('--max_states', type=int, default=600000)
    p.add_argument('--core_max', type=int, default=4000)
    p = sub.add_parser('dollar3')
    p.add_argument('--arm', default='modalPA')
    p.add_argument('--N', type=float, default=1000)
    p.add_argument('--theta', type=float, default=1e-11)
    p.add_argument('--core_max', type=int, default=4000)
    p.add_argument('--Kc', type=int, default=30)
    p = sub.add_parser('report')
    p = sub.add_parser('controls')
    p.add_argument('--N_neg', type=int, default=10000)
    a = ap.parse_args()
    if a.cmd == 'cell':
        cmd_cell(a)
    elif a.cmd == 'controls':
        cmd_controls(a)
    elif a.cmd == 'union':
        cmd_union(a)
    elif a.cmd == 'report':
        cmd_report(a)
    elif a.cmd == 'dollar3':
        cmd_dollar3(a)
