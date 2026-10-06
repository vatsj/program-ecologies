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
    pen = True
    if (fo > 1e-12).any():
        pen = False
    else:
        for q in np.nonzero(out & (np.abs(f) <= 1e-12))[0]:
            if (U[q, q] - (U[q, ids] @ x)) - (U[ids, q] @ x - phi) >= -1e-12:
                pen = False; break
    return deep, pen, f, out


def enumerate_candidates(U, mu, pool=None, max_types=3, chunk=200000, verbose=False):
    """Candidate recurrent supports of <= max_types classes from the class table alone.  pool: classes allowed in
    pairs and triples (default: all).  Returns list of dict(ids, x, size, status, deep, deep_pen, max_inv, n_neutral,
    n_adv, mass_sum, mass_min), plus counts."""
    K = U.shape[0]
    pool = np.arange(K) if pool is None else np.array(sorted(set(int(p) for p in pool)))
    cands = []
    counts = defaultdict(int)

    def add(ids, x, status):
        deep, pen, f, out = deep_test(U, ids, x)
        fo = f[out]
        cands.append(dict(ids=[int(i) for i in ids], x=[float(v) for v in x], size=len(ids), status=status, deep=deep, deep_pen=pen,
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


def deep_detail(U, names, mu, cand, top=None):
    """the full list of outside mutants of a candidate with their invasion fitnesses (sorted, closest to 0 first)."""
    deep, pen, f, out = deep_test(U, cand['ids'], cand['x'])
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
            n = int(name[8]); pricing = name.split('-')[2]
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
             skip_published=False, triples=True, pool_K=None):
    t0 = time.time()
    c = make_cell(name, N)
    res = dict(cell=name, N=N, K=int(len(c.mu)), chain_kw={k: v for k, v in c.chain_kw.items()}, published=PUBLISHED.get((name, N)))
    # ---- 1. discovery
    pool = None
    if pool_K is not None and pool_K < len(c.mu):
        pool = set(np.argsort(-c.mu)[:pool_K].tolist())
    td = time.time()
    cands, counts = enumerate_candidates(c.U, c.mu, pool=None if pool is None else sorted(pool), max_types=3 if triples else 2)
    deep = [x for x in cands if x['deep'] and x['status'] == 'stable']
    res['discovery'] = dict(counts=counts, pool_K=pool_K or int(len(c.mu)), triples=triples, n_candidates=len(cands),
                            n_stable=sum(1 for x in cands if x['status'] == 'stable'), n_center=sum(1 for x in cands if x['status'] == 'center'),
                            n_deep=len(deep), n_deep_pen=sum(1 for x in cands if x['deep_pen']),
                            deep_by_size={s: sum(1 for x in deep if x['size'] == s) for s in (1, 2, 3)},
                            deep_mass_sum_max=max([x['mass_sum'] for x in deep], default=0.0), time_s=time.time() - td)
    if verbose:
        print('[%s N=%d] discovery: %d candidates, %d deep (%s), %.0fs' % (name, N, len(cands), len(deep), res['discovery']['deep_by_size'], time.time() - td), flush=True)
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
        # published recurrent states (pi > 1e-6) that are not enumerated candidates
        cset = set(tuple(sorted(int(c.cid[i]) for i in x['ids'])) for x in cands if x['status'] == 'stable')
        res['discovery']['published_recurrent_not_candidates'] = [
            (desc(c, pch, k), float(p)) for k, p in zip(pch.keys_list, pch.pi) if p > 1e-6 and tuple(sorted(pch.states[k][0])) not in cset][:20]
    # ---- 5. full re-solve
    tf = time.time()
    seeds = [(list(int(c.cid[i]) for i in x['ids']), x['x']) for x in cands if x['status'] == 'stable' and x['size'] > 1
             and (x['deep'] or not extra_only_deep)]
    fch = LogChain(c.provider(), N=N, Ufull=c.U if twins else None, twins=twins, theta=1.0, max_states=10 ** 9,
                   **{k: v for k, v in c.chain_kw.items() if k in ('w',)})
    fch.explore_log(extra_states=seeds, log_theta=log_theta, max_states=max_states, verbose=verbose)
    keys, LA, lpi, info, out_un = fch.solve()
    pi = np.exp(lpi)
    st = stat_of(c, fch, keys, pi)
    sup = support_and_transitions(c, fch, keys, LA, lpi)
    deepkeys = {}
    for x in deep:
        k = cand_key(fch, x, c)
        deepkeys[k] = x
    pos = {k: i for i, k in enumerate(keys)}
    for k, x in deepkeys.items():
        x['resolve_pi'] = float(pi[pos[k]]) if k in pos else None
        x['resolve_log10_pi'] = float(lpi[pos[k]] / L10) if k in pos else None
    res['resolve'] = dict(stat=st, n_states=len(keys), n_seeded=len(seeds), log10_cut=float(fch.log_cut / L10) if np.isfinite(fch.log_cut) else None,
                          n_cand_left=fch.n_cand_left, closed=info, mass_deep=float(sum(x.get('resolve_pi') or 0 for x in deep)),
                          mass_poly=float(sum(p for k, p in zip(keys, pi) if len(fch.states[k][0]) > 1)),
                          indeterminate=len(fch.indeterminate), twin_moves=fch.n_twin_moves, twins=twins,
                          support=sup, time_s=time.time() - tf, resid=balance_residual(LA, pi))
    if not skip_published:
        # missed deep states: re-solved pi and best path weight from the published top state
        topk = pch.keys_list[int(np.argmax(pch.pi))]
        res['discovery']['missed_detail'] = []
        for x in sorted(missed, key=lambda x: -(x.get('resolve_pi') or 0))[:15]:
            k = cand_key(fch, x, c)
            bp = best_path(LA, pos.get(topk), pos.get(k)) if topk in pos and k in pos else None
            res['discovery']['missed_detail'].append(dict(state=' + '.join('%s:%.3f' % (c.names[i], xi) for i, xi in zip(x['ids'], x['x'])),
                                                          mass_sum=x['mass_sum'], resolve_pi=x.get('resolve_pi'),
                                                          log10_best_path_from_published_top=bp))
    res['deep_states'] = [dict(state=' + '.join('%s:%.4f' % (c.names[i], xi) for i, xi in zip(x['ids'], x['x'])), size=x['size'],
                               mass_sum=x['mass_sum'], mass_min=x['mass_min'], max_inv=x['max_inv'], deep_pen=x['deep_pen'],
                               in_published_explored=x.get('in_published_explored'), in_published_recurrent=x.get('in_published_recurrent'),
                               resolve_pi=x.get('resolve_pi'), resolve_log10_pi=x.get('resolve_log10_pi'),
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


def cmd_cell(a):
    for N in a.N:
        r = run_cell(a.cell, N, log_theta=math.log(a.theta), max_states=a.max_states, twins=a.twins,
                     extra_only_deep=a.only_deep, skip_published=a.skip_published, triples=not a.no_triples, pool_K=a.pool_K)
        fn = os.path.join(OUT, '%s_N%d%s.json' % (a.cell, N, '_twins' if a.twins else ''))
        json.dump(_jsonable(r), open(fn, 'w'), indent=1, default=str)


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
    a = ap.parse_args()
    if a.cmd == 'cell':
        cmd_cell(a)
