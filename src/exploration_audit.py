"""Exploration-cap audit helpers (spec specs/2026-10-24-exploration-audit.md; notes/exploration-audit.md).

This module imports the existing solvers and changes none of them.  It provides:

* `record(cell, stage, data)`: append one stage of one audited cell to runs/exploration_audit/<cell>.json (small json only);
* the mixed2 adapter (`TwoPopChain`): capped exploration with every restriction as an argument, the whole-state-space solve,
  statistics under pi, the frontier-outflow diagnostic of the spec, and the solver checks (log GTH vs jump-chain GTH vs a
  dense continuous-time generator solve on identical state sets and rates);
* the stage vocabulary of the spec: (a) reproduce, (b) enlarge every active restriction together, (c) full monomorphic space,
  (d) polymorphic additions, (e) twin-expanded.

Everything here is an eps -> 0 object; nothing is a lottery.
"""
import json, math, os, sys, time, resource
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
OUTDIR = os.path.join(ROOT, 'runs', 'exploration_audit')
os.makedirs(OUTDIR, exist_ok=True)


def rss_mb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e6 if sys.platform == 'darwin' else r / 1e3


def _default(o):
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating,)): return None if not np.isfinite(o) else float(o)
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_,)): return bool(o)
    raise TypeError(type(o))


def record(cell, stage, data, path=None):
    """Merge `data` under key `stage` into runs/exploration_audit/<cell>.json (atomic replace)."""
    p = path or os.path.join(OUTDIR, cell + '.json')
    cur = {}
    if os.path.exists(p):
        with open(p) as f:
            cur = json.load(f)
    cur[stage] = data
    tmp = p + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(cur, f, default=_default, indent=1, sort_keys=True)
    os.replace(tmp, p)
    return p


def load(cell):
    p = os.path.join(OUTDIR, cell + '.json')
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {}


def log(*a):
    print(*a, flush=True)


# ====================================================================== mixed2 (TwoPopChain) adapter
def m2():
    import mixed2 as M
    return M


NMAX = {'insp': 8, 'end': 7}


def m2_arm(game, arm, c):
    return m2().get_arm(game, arm, NMAX[game], c)


def top_pairs(A, m=10):
    o0 = np.argsort(-A.mass[0])[:m]; o1 = np.argsort(-A.mass[1])[:m]
    return [int(a) * A.K[1] + int(b) for a in o0 for b in o1]


def published_seeds(A):
    import mixed2_run as R
    return sorted(set(top_pairs(A, 10) + R.ladder_seeds(A)))


def random_seeds(A, k, seed):
    rng = np.random.default_rng(seed)
    return sorted(set(int(s) for s in rng.integers(0, A.K[0] * A.K[1], size=k)))


def stats_under_pi(A, states, lpi):
    """Island-statistic means under pi (the same statistics mixed2_run.chain_cell reports, without the weak-graph classes)."""
    M = m2()
    pi = np.exp(lpi - np.logaddexp.reduce(lpi[np.isfinite(lpi)]))
    K0, K1 = A.K
    states = np.asarray(states)
    sa, sb = states // K1, states % K1
    agg = {}
    wsum = {}
    n = len(states)
    for lo in range(0, n, 200):
        hi = min(n, lo + 200)
        X0 = np.zeros((hi - lo, K0)); X1 = np.zeros((hi - lo, K1))
        X0[np.arange(hi - lo), sa[lo:hi]] = 1; X1[np.arange(hi - lo), sb[lo:hi]] = 1
        st = M.island_stats(A, X0, X1)
        w = pi[lo:hi]
        for k, v in st.items():
            if k == 'J':
                continue
            vv = np.asarray(v, float)
            ok = np.isfinite(vv)
            agg[k] = agg.get(k, 0.0) + float((w * np.where(ok, vv, 0.0)).sum())
            wsum[k] = wsum.get(k, 0.0) + float((w * ok).sum())
    stat = {k: (agg[k] / wsum[k] if wsum[k] > 0 else None) for k in agg}
    sh0 = np.zeros(K0); sh1 = np.zeros(K1)
    np.add.at(sh0, sa, pi); np.add.at(sh1, sb, pi)
    order = np.argsort(-pi)[:8]
    top = [dict(pi=float(pi[i]), s0=A.names[0][sa[i]], s1=A.names[1][sb[i]], u0g=float(A.UAg[sa[i], sb[i]]),
                u1g=float(A.UBg[sb[i], sa[i]])) for i in order]
    cum = np.cumsum(np.sort(pi)[::-1])
    return dict(stat=stat, top_states=top, n_states_for_099=int(np.searchsorted(cum, 0.99) + 1),
                n_support_1e6=int((pi > 1e-6).sum()))


def frontier_mass(ch, log_theta=math.log(1e-10)):
    """Spec 'frontier outflow': pi-mass of explored states with an outgoing transition into an unexplored target that the
    exploration criterion would still add (relative inflow above theta: the targets left when the cap, not theta, stopped
    the exploration), computed on the explored set of a TwoPopChain after explore().  Also returned: the relative flux
    leaving the explored set ('unexplored_flux', the chain's own log_unexplored) and the strict count of states with any
    unexpanded out-rate share above 1e-6 (in these chains almost every state, so not used as the flag)."""
    K0, K1 = ch.K0, ch.K1
    pi = np.exp(ch.lpi - np.logaddexp.reduce(ch.lpi[np.isfinite(ch.lpi)]))
    linf, lflux = ch.inflows(ch.lpi)
    cand = (linf - lflux) > log_theta
    mass = 0.0
    strict = 0.0
    for i, s in enumerate(ch.states):
        a, b = divmod(s, K1)
        L1, L2 = ch.R[s]
        idx1 = np.arange(K0) * K1 + b
        idx2 = a * K1 + np.arange(K1)
        m1 = (ch.pos[idx1] < 0) & np.isfinite(L1)
        m2_ = (ch.pos[idx2] < 0) & np.isfinite(L2)
        if (m1 & cand[idx1]).any() or (m2_ & cand[idx2]).any():
            mass += pi[i]
        allL = np.concatenate([L1[np.isfinite(L1)], L2[np.isfinite(L2)]])
        un = np.concatenate([L1[m1], L2[m2_]])
        if len(un) and math.exp(np.logaddexp.reduce(un) - np.logaddexp.reduce(allL)) > 1e-6:
            strict += pi[i]
    return dict(frontier_mass=float(mass), strict_unexpanded_mass=float(strict), n_candidates_left=int(cand.sum()))


def m2_capped(A, N, max_states=1500, max_add=400, log_theta=math.log(1e-10), seeds=None, verbose=False):
    """Stage (a)/(b) for a TwoPopChain cell: the published exploration with chosen restrictions."""
    M = m2()
    t0 = time.time()
    ch = M.TwoPopChain(A, N)
    if seeds is None:
        seeds = published_seeds(A)
    ch.explore(seeds, log_theta=log_theta, max_states=max_states, max_add=max_add, verbose=verbose)
    out = stats_under_pi(A, ch.states, ch.lpi)
    out.update(N=N, n_states=len(ch.states), capped=bool(ch.capped), max_states=max_states, max_add=max_add,
               log10_theta=log_theta / math.log(10),
               log10_cut=float(ch.log_cut / math.log(10)) if np.isfinite(ch.log_cut) else None,
               log10_unexplored=float(ch.log_unexplored / math.log(10)) if np.isfinite(ch.log_unexplored) else None,
               n_seeds=len(seeds), solver=ch.info.get('solver', 'log_gth'), time_s=time.time() - t0, rss_mb=rss_mb())
    out.update(frontier_mass(ch, log_theta))
    return out, ch


def m2_full(A, N):
    """Stage (c): the whole K0 x K1 monomorphic state space, jump-chain GTH with the holding-time correction."""
    M = m2()
    t0 = time.time()
    ch = M.TwoPopChain(A, N)
    ch.solve_full()
    out = stats_under_pi(A, ch.states, ch.lpi)
    out.update(N=N, n_states=len(ch.states), capped=False, solver='full_linear_jump_gth', time_s=time.time() - t0, rss_mb=rss_mb(),
               frontier_mass=0.0)
    return out, ch


def generator_solve(A, N, states=None):
    """Independent check of the holding-time correction: stationary distribution of the continuous-time generator Q on the
    given state set (default all pairs, small instances only), by a dense linear solve with the normalisation row.  Q has
    off-diagonal rates exp(L) (rates per mutation event), diagonal minus the row sum restricted to the state set."""
    M = m2()
    ch = M.TwoPopChain(A, N)
    K0, K1 = A.K
    S = K0 * K1 if states is None else len(states)
    if states is None:
        states = list(range(K0 * K1))
    pos = -np.ones(K0 * K1, np.int64); pos[states] = np.arange(len(states))
    Q = np.zeros((S, S))
    for i, s in enumerate(states):
        a, b = divmod(s, K1)
        L1, L2 = ch.rates(s)
        t1 = pos[np.arange(K0) * K1 + b]; t2 = pos[a * K1 + np.arange(K1)]
        ok1 = (t1 >= 0) & np.isfinite(L1); ok2 = (t2 >= 0) & np.isfinite(L2)
        np.add.at(Q[i], t1[ok1], np.exp(L1[ok1])); np.add.at(Q[i], t2[ok2], np.exp(L2[ok2]))
        Q[i, i] = 0.0
        Q[i, i] = -Q[i].sum()
    Aeq = Q.T.copy(); Aeq[-1, :] = 1.0
    rhs = np.zeros(S); rhs[-1] = 1.0
    pi = np.linalg.solve(Aeq, rhs)
    return np.asarray(states), pi


def tv(p, q):
    return 0.5 * float(np.abs(p - q).sum())


# ====================================================================== monomorphic-complete cells: solver_audit pipeline
SCRATCH = os.environ.get('EA_SCRATCH', os.path.join(os.environ.get('TMPDIR', '/tmp'), 'exploration_audit'))
os.makedirs(SCRATCH, exist_ok=True)


def kval(b, n=8):
    """K play table at global budget b (rebuilt on a miss; cached in SCRATCH, never in the repo)."""
    import k_at_n8 as K8
    if b == 'free':
        return K8.load_val(n, 'free')
    p = os.path.join(SCRATCH, 'kval_n%d_b%s.npy' % (n, b))
    if os.path.exists(p):
        return np.load(p)
    val, meta, K, g = K8.ktable(n, int(b), filter_first=True, ustar_limit=40)
    np.save(p, val)
    return val


def _pd_cell(c, prov, kw, name):
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
    c.name = name; c.headline = 'pcc'


_SA_ORIG = None


def make_cell(name, N):
    """solver_audit.make_cell plus the cells of this audit.  Names: pd-modal6, pd-modal8 (free modal arm, published
    eager_poly=True), pd-kb<b> (K at n = 8, budget b, eager_poly=False), pd-weakdollar7 / dollar-weak7 (weak n = 7 dollar)."""
    import solver_audit as SA
    if name in ('pd-modal6', 'pd-modal8'):
        import modal as MM
        c = SA.Cell()
        # published modal_limN cells used eager_poly=True (hours at n = 8); priced_limN c = 0 (eager_poly=False) agrees to 1e-5
        _pd_cell(c, MM.build(int(name[-1]))[3], dict(w=0.3, eager_poly=(name == 'pd-modal6')), name)
    elif name.startswith('pd-pr') and '-c' in name:          # pd-pr8-lazy-c0.1: priced arm, n = 8, lazy pricing, c = 0.1
        import modal as MM
        _, nn, pricing, cc = name.split('-')
        c = SA.Cell()
        _pd_cell(c, MM.build_priced(int(nn[2:]), float(cc[1:]), pricing=pricing)[3], dict(w=0.3, eager_poly=False), name)
    elif name.startswith('pd-fr-'):                            # pd-fr-mu-n8-d0.01: drift-closure fringe (src/fringe.py)
        import fringe as FR
        _, _, kind, nn, dd = name.split('-')
        c = SA.Cell()
        _pd_cell(c, FR.build_variant(int(nn[1:]), float(dd[1:]), kind, None, ())[1], dict(w=0.3, eager_poly=False), name)
    elif name.startswith('pd-cert-'):                          # pd-cert-lazycert0-n8-c0.01
        import cert_priced as CP
        _, _, pricing, nn, cc = name.split('-')
        c = SA.Cell()
        _pd_cell(c, CP.build_cert(int(nn[1:]), float(cc[1:]), pricing=pricing)[3], dict(w=0.3, eager_poly=False), name)
    elif name.startswith('pd-kb'):
        import k_at_n8 as K8
        c = SA.Cell()
        _pd_cell(c, K8.build_prov(8, kval(int(name[5:]))), dict(w=0.3, eager_poly=False), name)
    elif name in ('dollar-weak7', 'dollar-modal7'):
        import modal_dollar as MD
        from dollar_partitions import ClassProvider
        c = SA.Cell()
        d = MD.data('weak' if name == 'dollar-weak7' else 'modal', 7)
        c.d = d; c.name = name; c.headline = 'eff'
        c.provider = lambda: ClassProvider(d['U'], d['mu'])
        pr = c.provider()
        c.U = pr.Ufull; c.mu = np.asarray(d['mu'], float); c.names = list(d['names']); c.cid = np.arange(d['K'])
        c.stat = SA._dollar_stat(d)
        c.chain_kw = dict(w=0.3, theta=1e-7, max_states=30000, eager_poly=False)
        c.headlines = ('eff', 'half'); c.twin_ok = True
    else:
        return _SA_ORIG(name, N)
    c.N = N
    c.id2c = {int(p): k for k, p in enumerate(c.cid)}
    return c


def sa_run(name, N, log_theta=math.log(1e-14), max_states=20000, twins=False, closure_nodes=0, verbose=False, skip_published=False):
    """Stages (a), (b), (d) and optionally (e) of an M-status cell via solver_audit.run_cell (published configuration
    re-run exactly, then a closure-seeded log-domain re-solve), with this module's cell list."""
    import solver_audit as SA
    global _SA_ORIG
    old_make, old_out = SA.make_cell, SA.OUT
    _SA_ORIG = old_make
    SA.make_cell = make_cell
    SA.OUT = SCRATCH
    try:
        res = SA.run_cell(name, N, log_theta=log_theta, max_states=max_states, verbose=verbose, twins=twins,
                          closure_nodes=closure_nodes, skip_published=skip_published)
    finally:
        SA.make_cell, SA.OUT = old_make, old_out
    return res


def sa_bounded(name, N, log_theta=math.log(1e-14), max_states=20000, twins=False, verbose=False):
    """Stages (a), (b) and the bounded (d) of the spec for an M-status cell, without the all-pairs/all-triples enumeration of
    solver_audit.run_cell (which costs an hour at K ~ 600): (a) the published Chain re-run; (b) the LogChain on the same
    construction at log_theta (every monomorphic class expanded, their targets, then inflow rounds up to max_states), seeded
    with the published chain's polymorphic states; (d) the polymorphic states reached from the recurrent monomorphic classes are
    exactly the targets that expansion creates, each tested against every admissible invader by the same expansion."""
    import solver_audit as SA
    from chain import Chain
    from chain_log import LogChain
    t0 = time.time()
    global _SA_ORIG
    if _SA_ORIG is None:
        _SA_ORIG = SA.make_cell
    c = make_cell(name, N)
    pch = Chain(c.provider(), N=N, **c.chain_kw).explore()
    pst = SA.stat_of(c, pch, pch.keys_list, pch.pi)
    seeds = []
    for k in pch.trans:
        ids_, x_, kind_ = pch.states[k]
        if kind_ == 'poly':
            seeds.append((list(ids_), list(x_)))
    fch = LogChain(c.provider(), N=N, Ufull=c.U if twins else None, twins=twins, theta=1.0, max_states=10 ** 9,
                   **{k: v for k, v in c.chain_kw.items() if k in ('w',)})
    fch.explore_log(extra_states=seeds, log_theta=log_theta, max_states=max_states + len(seeds), verbose=verbose, layer_mask=[False] * len(seeds))
    keys_all, lpi_all, info, out_un, rec = fch.solve_sparse()
    keys = [keys_all[i] for i in rec]
    lpi = lpi_all[rec]
    pi = np.exp(lpi)
    st = SA.stat_of(c, fch, keys, pi)
    npoly = sum(1 for k in keys if len(fch.states[k][0]) > 1)
    return dict(cell=name, N=N, K=int(len(c.mu)), published=SA.PUBLISHED.get((name, N)), rerun_stat=pst, rerun_n_expanded=len(pch.trans),
                rerun_n_states=len(pch.states), rerun_cut_flow=float(pch.cut_flow), rerun_indeterminate=len(pch.indeterminate),
                rerun_n_terminal=len(pch.terminal), resolve_stat=st, resolve_n_states=len(keys), resolve_n_expanded=len(fch.trans),
                resolve_n_seeded=len(seeds), resolve_log10_cut=float(fch.log_cut / math.log(10)) if np.isfinite(fch.log_cut) else None,
                resolve_n_cand_left=int(fch.n_cand_left), resolve_mass_poly=float(sum(p for k, p in zip(keys, pi) if len(fch.states[k][0]) > 1)),
                resolve_n_recurrent_poly=npoly, twins=twins, twin_moves=int(fch.n_twin_moves), resolve_closed=info,
                resolve_top=[(SA.desc(c, fch, keys[i]), float(pi[i])) for i in np.argsort(-pi)[:5]],
                log10_theta=log_theta / math.log(10), max_states=max_states, time_s=time.time() - t0, rss_mb=rss_mb())


def sa_summary(res):
    """The few numbers worth keeping from a solver_audit.run_cell result."""
    pub = res.get('published_rerun', {})
    rs = res['resolve']
    return dict(cell=res['cell'], N=res['N'], K=res['K'], published_stat=res.get('published'),
                rerun_stat=pub.get('stat'), rerun_n_expanded=pub.get('n_expanded'), rerun_n_states=pub.get('n_states'),
                rerun_cut_flow=pub.get('cut_flow'), rerun_indeterminate=pub.get('indeterminate'),
                resolve_stat=rs['stat'], resolve_n_states=rs['n_states'], resolve_n_seeded=rs['n_seeded'],
                resolve_log10_cut=rs['log10_cut'], resolve_n_cand_left=rs['n_cand_left'], resolve_mass_poly=rs['mass_poly'],
                resolve_mass_deep=rs['mass_deep'], twins=rs['twins'], twin_moves=rs['twin_moves'], resolve_resid=rs['resid'],
                resolve_top=[(s['state'], s['pi']) for s in rs['support'][:5]],
                solver_tv=res.get('solver', {}).get('tv'), rates_same_set=res.get('rates', {}).get('same_explored_set'),
                n_deep=res['discovery']['n_deep'], n_deep_mod_twins=res['discovery']['n_deep_mod_twins'],
                n_candidates=res['discovery']['n_candidates'], discrepancy_vs_rerun=res.get('discrepancy_vs_rerun'),
                discrepancy_vs_published=res.get('discrepancy'), time_s=res['time_s'], rss_mb=rss_mb())


# ====================================================================== three-player dollar (Chain3.explore_hybrid)
def d3_cell(arm, N, theta, max_states=400000, core_max=2500, promote=1e-5, max_rounds=40, w=0.3, drop_rel=1e-5):
    """Inventory I-22 / I-46: build_chain + explore_hybrid of src/dollar3_run.py with explicit restrictions.  Published:
    theta = 1e-7 / N (1e-9 at N = 100), core_max 2500, promote 1e-5, max_states 400k, 4-5 rounds actually used."""
    import dollar3_run as R
    t0 = time.time()
    ch, S = R.build_chain(arm, N, w, theta, max_states, core_max=core_max, drop_rel=drop_rel, promote=promote)
    ch.max_rounds = max_rounds
    ch.verbose = True
    ch.explore_hybrid()
    pi = ch.pi
    lab = np.array([R.coalition(ch.pay[i], ch.typ[i]) for i in range(len(ch.codes))])
    p6 = ch.pay / 6.0
    out = dict(arm=arm, N=N, theta=theta, core_max=core_max, promote=promote, max_states=max_states, states=int(len(ch.codes)),
               core=int(ch.is_core.sum()), ring=int((~ch.is_core).sum()), rounds=len(ch.log), rel_cut=float(ch.rel_cut),
               rel_cut_change=float(ch.rel_cut_change), cut_flow=float(ch.cut_flow), Kc=int(ch.Kc),
               mass_by_coalition={c: float(pi[lab == c].sum()) for c in R.COAL},
               efficiency=float(pi @ p6.sum(1)), E_max_share=float(pi @ p6.max(1)), P_pair=float(pi[np.isin(ch.typ, [1, 2, 3])].sum()),
               P_some_slot_zero=float(pi @ (p6.min(1) == 0)), core_at_max=bool(int(ch.is_core.sum()) >= core_max),
               time_s=time.time() - t0, rss_mb=rss_mb())
    return out, ch


# ====================================================================== union / enforcement (UChain.explore_hybrid)
ENF_SCRATCH = os.path.join(SCRATCH, 'enforcement')


def enf_partC(arm, pool, c, N, tie, theta, core_max=2500, promote=1e-5, max_rounds=40):
    """Inventory I-24C.  Calls union_enforcement_run.run_part_c with its output directory redirected to scratch (the
    tracked runs/enforcement files are never touched).  classes_CC.npz is copied from the main checkout's gitignored cache
    into ENF_SCRATCH before the first call (or recomputed by union_enforcement.load_base if absent)."""
    import argparse
    import union_enforcement as E
    import union_enforcement_run as R
    os.makedirs(ENF_SCRATCH, exist_ok=True)
    E.OUT = ENF_SCRATCH; R.OUT = ENF_SCRATCH
    args = argparse.Namespace(arm=arm, pool=pool, c=c, N=N, tie=tie, theta=theta)
    t0 = time.time()
    R.run_part_c(args)
    tag = '%s_pool%d_c%g_N%d_%s' % (arm, pool, c, N, tie)
    with open(os.path.join(ENF_SCRATCH, 'partC_%s.json' % tag)) as f:
        out = json.load(f)
    keep = {k: out.get(k) for k in ('states', 'rel_cut_change', 'rel_cut', 'summary', 'efficiency', 'total_surplus', 'mean_payoff',
                                    'strike_incidence', 'repression_given_strike', 'class_counts', 'cut_flow', 'theta', 'time_s')}
    keep['wall_s'] = time.time() - t0; keep['rss_mb'] = rss_mb(); keep['theta_arg'] = theta
    return keep


UNION_SCRATCH = os.path.join(SCRATCH, 'union')


def union_cell(arm, c, N, theta, core_max=2500, promote=1e-5, max_rounds=40, max_states=400000):
    """Inventory I-23.  union_run.run_chain with its output directory redirected to scratch.  classes_<arm>.npz must be in
    UNION_SCRATCH (the enforcement run's classes_CC.npz is the quorum arm's class lumping and is copied there; checked by
    reproducing the published cell)."""
    import argparse
    import union_run as UR
    os.makedirs(UNION_SCRATCH, exist_ok=True)
    UR.OUT = UNION_SCRATCH
    args = argparse.Namespace(arm=arm, c=c, N=float(N), w=0.3, theta=theta, max_states=max_states, core_max=core_max, promote=promote,
                              max_rounds=max_rounds, timing=False)
    t0 = time.time()
    UR.run_chain(args)
    with open(os.path.join(UNION_SCRATCH, '%s_c%g_N%d.json' % (arm, c, N))) as f:
        out = json.load(f)
    keep = {k: out.get(k) for k in ('states', 'core', 'rel_cut_change', 'rel_cut', 'summary', 'efficiency', 'mean_payoff', 'theta', 'wage_offered')}
    keep['wall_s'] = time.time() - t0; keep['rss_mb'] = rss_mb(); keep['theta_arg'] = theta; keep['core_max'] = core_max
    return keep


def glob_lang(d):
    import glob
    return sorted(glob.glob(os.path.join(d, 'lang_*.json')))


def conc_cell(arm, N, theta, enf='CC', pool=0, c=0.5):
    """Inventory I-36.  concessions.run_cell(save=False) with the language build forced to one process (the module's
    build_language pools three processes by default; this audit runs one process per job)."""
    import concessions as CC
    import shutil
    # the module writes its language caches and a lang_*.json into CC.OUT (a tracked directory): redirect to scratch and seed it
    # with a copy of the tracked json, so that no stored result is touched
    scratch = os.path.join(SCRATCH, 'conc')
    os.makedirs(scratch, exist_ok=True)
    for fn in glob_lang(CC.OUT):
        dst = os.path.join(scratch, os.path.basename(fn))
        if not os.path.exists(dst):
            shutil.copy(fn, dst)
    CC.OUT = scratch
    _orig = CC.build_language
    CC.build_language = lambda a, e, p, cc, procs=1, verbose=True: _orig(a, e, p, cc, procs=1, verbose=verbose)
    t0 = time.time()
    out, ch, C = CC.run_cell(arm, enf=enf, pool=pool, c=c, N=float(N), theta=theta, save=False)
    keep = {k: out.get(k) for k in ('states', 'core', 'rel_cut_change', 'summary', 'wage_offered', 'wage_paid_both_work', 'efficiency',
                                    'full_production', 'theta', 'support_size_99', 'solver_check')}
    keep['support_top'] = [(s['state'], s['pi']) for s in out['support'][:6]]
    keep['wall_s'] = time.time() - t0; keep['rss_mb'] = rss_mb(); keep['theta_arg'] = theta
    return keep


def rps_cell(arm, N, n=6, D=12, mu='bits', log10theta=-14.0, closure_nodes=6000, max_states=20000, twins=True):
    """Inventory I-48: rps_run.chain_cell (published: log10 theta -14, closure 6000 nodes, max_states 20000, twins)."""
    import rps as RP
    import rps_run as RR
    t0 = time.time()
    A = RP.get_arm(arm, n, D, mu)
    res, _ = RR.chain_cell(A, N, log_theta=log10theta * math.log(10), twins=twins, max_states=max_states, closure_nodes=closure_nodes)
    st = res['pi_stat']
    keep = dict(arm=arm, N=N, n=n, D=D, K=res['K'], log10_theta=res['log10_theta'], n_candidates=res['n_candidates'], n_seeded=res['n_seeded'],
                closure_nodes=res['closure_nodes'], closure_complete=res['closure_complete'], n_expanded=res['n_expanded'],
                n_recurrent=res['n_recurrent'], log10_cut=res['log10_cut'], n_cand_left=res['n_cand_left'], n_twin_moves=res['n_twin_moves'],
                e_prog=st.get('e_prog'), e_act=st.get('e_act'), mix_pop=st.get('mix_pop'), forfeit_self=st.get('forfeit_self'),
                share_X=st.get('share_X'), pi_mass_X=res['pi_mass_X'], top=[(s['state'], s['pi']) for s in res['top_states'][:4]],
                time_s=time.time() - t0, rss_mb=rss_mb())
    return keep


def rps_priced_cell(arm, c, kind, N, D=12, log10theta=-8.0, closure_nodes=6000, branch=8, att_starts=1000, att_sub=6, max_states=40000, twins=True):
    """Inventory I-49: rps_priced_run.discover + chain_cell_p (published: log10 theta -8, closure 6000 nodes branch 8,
    1000-start attractor search of support <= 6, max_states 40000, twins)."""
    import rps as RP
    import rps_priced as PP
    import rps_priced_run as RPP
    t0 = time.time()
    b = PP.load_base(arm, 6, D)
    A = PP.make_arm(b, c, kind)
    Aex = emap = None
    if arm in ('pure', 'sample', 'matched', 'exact'):
        Aex = PP.get_aex(c, kind, D)
        emap = PP.embed_priced(A, Aex)
    disc = RPP.discover(A, att_starts=att_starts, att_sub=att_sub, closure_nodes=closure_nodes, branch=branch)
    res = RPP.chain_cell_p(A, N, Aex, emap, disc, log_theta=log10theta * math.log(10), twins=twins, max_states=max_states)
    st = res['pi_stat']
    keep = dict(arm=arm, c=c, kind=kind, N=N, D=D, K=res['K'], log10_theta=res['log10_theta'], n_seeded=disc['info']['n_seeded'],
                closure_complete=disc['info']['closure_complete'], closure_nodes=disc['info']['closure_nodes'],
                n_attractor_new=disc['info']['n_attractor_search_new'], n_expanded=res['n_expanded'], n_recurrent=res['n_recurrent'],
                log10_cut=res['log10_cut'], n_cand_left=res['n_cand_left'], n_twin_moves=res['n_twin_moves'],
                e_prog=st.get('e_prog'), e_gross=st.get('e_gross'), mix_pop=st.get('mix_pop'), forfeit_self=st.get('forfeit_self'),
                share_X=st.get('share_X'), share_readers=st.get('share_readers'), poly_mass=res['pi_polymorphic_mass'],
                top=[(s['state'], s['pi']) for s in res['top_states'][:4]], time_s=time.time() - t0, rss_mb=rss_mb())
    return keep


def md_limN(arm, N, theta, twins=False, deep_types=3):
    """Inventory I-29/I-30: modal_dollar.limN_run (the published seeded log-domain chain: all K monomorphic classes, the
    <= 3-class deep states plus one layer, log_theta = ln theta; published theta 1e-7 and 1e-9, twins off)."""
    import modal_dollar as MD
    t0 = time.time()
    d = MD.data(arm, 7)
    deep = MD.deep_states(d, deep_types)
    r = MD.limN_run(arm, N, math.log(theta), deep=deep, twins=twins)
    keep = {k: r.get(k) for k in ('arm', 'N', 'twins', 'log10_theta', 'n_states', 'log10_cut', 'n_deep', 'P_efficient', 'E_max', 'mean_pay')}
    for nm_ in ('effset', 'greedy', 'deep'):
        keep[nm_ + '_mass'] = r[nm_].get('mass')
    keep['top_states'] = [(s['state'], s['pi']) for s in r['top_states'][:4]]
    keep['wall_s'] = time.time() - t0; keep['rss_mb'] = rss_mb()
    return keep


def chk_onepop(arm, game, N, max_states, log_theta=math.log(1e-14), twins=True):
    """Inventory I-42: fixed_role_chicken.onepop_chain with an explicit max_states (published 3000 + seeds)."""
    import fixed_role_chicken as F
    t0 = time.time()
    r = F.onepop_chain(arm, game, N, log_theta=log_theta, twins=twins, max_states=max_states)
    keep = {k: r.get(k) for k in ('arm', 'game', 'N', 'twins', 'log10_theta', 'n_candidates', 'n_seeded', 'closure_nodes', 'closure_complete',
                                  'n_states', 'log10_cut', 'n_cand_left', 'pay_per_player', 'efficiency', 'StSt', 'asym', 'SwSw',
                                  'pi_by_class', 'top_exit_log10')}
    keep['support_top'] = [(s['state'], s['pi']) for s in r['support'][:4]]
    keep['max_states'] = max_states; keep['time_s'] = time.time() - t0; keep['rss_mb'] = rss_mb()
    return keep


# ====================================================================== modal dollar, fixed roles (modal_dollar.fixed_chain_lazy)
def md_fixed(arm, N, theta=1e-12, max_states=8000, rel_drop=1e-25, verbose=False, lazy2=False):
    """Inventory I-32.  Stage (a): theta 1e-12, max_states 8000, rel_drop 1e-25 (the published call);  (b): a larger
    max_states and/or lower theta;  the weak arm is complete (5,929 states) and is run with fixed_chain_full(method='gth')."""
    import modal_dollar as MD
    from dollar_partitions import fixed_summary
    d = MD.data(arm, 7)
    t0 = time.time()
    if d['K'] <= 80:
        ch = MD.fixed_chain_full(d, N, method='gth')
    elif lazy2:
        ch = md_fixed_lazy2(d, N, max_states, theta=theta, rel_drop=rel_drop, verbose=verbose)
    else:
        ch = MD.fixed_chain_lazy(d, N, theta=theta, rel_drop=rel_drop, max_states=max_states, verbose=verbose)
    r = fixed_summary(d, ch)
    o = r['outcome']
    return dict(arm=arm, N=N, K=d['K'], space=d['K'] ** 2, theta=theta, max_states=max_states, n_states=ch['n_states'], cut=float(ch['cut']),
                rounds=ch.get('rounds'), n_cand_left=ch.get('n_cand_left'), lazy2=lazy2, label_mass=r['ordered_label_mass'], eff=o['eff'], E_max_pay=o['E_max_pay'],
                mass_constant_pairs=r['mass_constant_pairs'], time_s=time.time() - t0, rss_mb=rss_mb()), ch, d


def md_fixed_lazy2(d, N, max_states, theta=1e-12, w=0.3, rel_drop=1e-25, verbose=False):
    """The same chain as modal_dollar.fixed_chain_lazy (rates, constant-pair seeds, reflecting boundary, candidate rule
    'unexpanded inflow > theta, largest first, up to max_states'), assembled with vector operations and solved by the
    in-place numba GTH of mixed2 (one dense copy, 8 n^2 bytes) so that larger explored sets fit in memory.  Used for the
    stage (b) enlargements of I-32; at max_states = 8000 it reproduces fixed_chain_lazy (checked in the run)."""
    import mixed2 as M
    from dollar_partitions import lrho_vec
    U, mu, K = d['U'], d['mu'], d['K']
    lmu = np.log(0.5 * mu)
    L1 = lrho_vec(U.T[None, :, :] - U[:, :, None], N, w) + lmu[None, None, :]
    L2 = lrho_vec(U.T[:, None, :] - U.T[:, :, None], N, w) + lmu[None, None, :]
    idx = np.arange(K)
    L1[idx, :, idx] = -np.inf
    L2[:, idx, idx] = -np.inf
    mm = np.maximum(L1.max(axis=2), L2.max(axis=2))
    R = mm + np.log(np.exp(L1 - mm[:, :, None]).sum(axis=2) + np.exp(L2 - mm[:, :, None]).sum(axis=2))
    P1 = np.exp(L1 - R[:, :, None]); P2 = np.exp(L2 - R[:, :, None])
    del L1, L2
    P1[P1 < rel_drop] = 0.0; P2[P2 < rel_drop] = 0.0
    const = [c for c in range(K) if d['kinds'][c] == 'constant']
    E = np.array([a * K + b for a in const for b in const], np.int64)
    S = K * K
    cut = None
    for rnd in range(200):
        n = len(E)
        pos = -np.ones(S, np.int64); pos[E] = np.arange(n)
        P = np.zeros((n, n))
        inflow_rows = []                       # (target code array, prob array, source index) for unexpanded targets
        a_, b_ = np.divmod(E, K)
        for i in range(n):
            a, b = int(a_[i]), int(b_[i])
            t1 = idx * K + b; p1 = P1[a, b]
            t2 = a * K + idx; p2 = P2[a, b]
            j1 = pos[t1]; j2 = pos[t2]
            ok = (j1 >= 0) & (p1 > 0)
            np.add.at(P[i], j1[ok], p1[ok])
            ok = (j2 >= 0) & (p2 > 0)
            np.add.at(P[i], j2[ok], p2[ok])
            un1 = (j1 < 0) & (p1 > 0); un2 = (j2 < 0) & (p2 > 0)
            if un1.any(): inflow_rows.append((t1[un1], p1[un1], i))
            if un2.any(): inflow_rows.append((t2[un2], p2[un2], i))
            P[i, i] += max(0.0, 1.0 - P[i].sum())
        x = M._gth_inplace(P)
        del P
        inflow = np.zeros(S)
        for t, p, i in inflow_rows:
            np.add.at(inflow, t, x[i] * p)
        cand = np.nonzero(inflow > theta)[0]
        cut = float(inflow[inflow <= theta].sum())
        if verbose:
            log('  round %d: %d states, %d candidates, cut %.2e, rss %.0fMB' % (rnd, n, len(cand), cut, rss_mb()))
        if len(cand) == 0 or n >= max_states:
            cut = float(inflow.sum())
            break
        cand = cand[np.argsort(-inflow[cand])][:max(1, max_states - n)]
        E = np.concatenate([E, cand])
    lpi = np.full(S, -np.inf)
    lpi[E] = np.log(np.maximum(x, 1e-320)) - R.ravel()[E]
    lpi -= lpi.max()
    pi = np.exp(lpi); pi /= pi.sum()
    n_cand_left = int((inflow > theta).sum() - 0) if cut is not None else None
    return dict(pi=pi.reshape(K, K), logR=R, P1=P1, P2=P2, cut=cut, n_states=len(E), rounds=rnd + 1, n_cand_left=int((inflow > theta).sum()))


# ====================================================================== ultimatum two-population chain (twopop.TwoPop)
def ult_cell(game_name, arm, N=100, w=0.1, n=5, stage='a', verbose=False):
    """Inventory I-05 / I-06.  stage 'a': published (seeds top-12 x top-12, theta 1e-6, max_states 20000, max_rounds 60);
    'b': theta 1e-10, max_states 200000, max_rounds 600 (seeds unchanged); 'c': every pair of classes seeded and expanded."""
    import twopop
    from game import Game
    game = Game.load(os.path.join(ROOT, 'games', game_name + '.yaml'))
    game.role = False; game.nroles = 1          # the published ultimatum rows predate ROLE becoming first-class (commit 7f2aac6)
    t0 = time.time()
    kw = {}
    if stage == 'b':
        kw = dict(theta=1e-10, max_states=200000, max_rounds=600)
    # twopop.build builds Language(...) with the default role=True (ROLE first-class since 7f2aac6); the published rows used
    # role=False (902 programs, 44 classes), so the build is repeated here with the override, solver and TwoPop unchanged.
    from dsl import Language
    full = Language('weak', n, role=False, k=game.k, names=game.actions)
    P_ids = full.ids(); muP = {int(p): float(full.mu[p]) for p in P_ids}
    if arm == 'mutual':
        R_ids = P_ids; muR = muP
    else:
        blind = Language('blind', n, role=False, k=game.k, names=game.actions)
        R_ids = twopop.map_language(blind, full)
        muR = {int(r): float(blind.mu[i]) for i, r in enumerate(R_ids)}
    tp = twopop.TwoPop(game, full, P_ids, R_ids, muP, muR, N, w, verbose=verbose, **kw)
    if stage == 'c':
        seeds = [(tp.key(p, q), mp * mq) for p, _, mp in tp.Pc for q, _, mq in tp.Rc]
        tp.max_states = 10 ** 7
        tp.explore(seeds)
    else:
        tp.explore()
    pi = dict(zip(tp.keys_list, tp.pi))
    rej = sum(pi[k] * tp.state_stats(k)['reject'] for k in pi)
    sP = sum(pi[k] * tp.state_stats(k)['share_P'] for k in pi); sR = sum(pi[k] * tp.state_stats(k)['share_R'] for k in pi)
    outc = {}
    for k, p in pi.items():
        st = tp.state_stats(k)
        key = '(%.3f,%.3f,rej%.3f)' % (st['share_P'], st['share_R'], st['reject'])
        outc[key] = outc.get(key, 0.0) + p
    top = sorted(outc.items(), key=lambda kv: -kv[1])[:8]
    sup = [(tp.describe(k), float(p)) for k, p in tp.support(1e-3)[:8]]
    out = dict(stage=stage, n_P_classes=len(tp.Pc), n_R_classes=len(tp.Rc), n_pairs=len(tp.Pc) * len(tp.Rc), n_expanded=len(tp.trans),
               cut_flow=float(tp.cut_flow), reject=float(rej), share_P=float(sP), share_R=float(sR), top_outcomes=top, support=sup,
               time_s=time.time() - t0, rss_mb=rss_mb())
    # frontier: pi-mass of expanded states with an edge into an unexpanded target whose total stationary inflow exceeds theta
    inflow = {}
    for k, p in pi.items():
        for b, v in tp.trans[k].items():
            if b not in tp.trans:
                inflow[b] = inflow.get(b, 0.0) + p * v
    candt = {b for b, f in inflow.items() if f > tp.theta}
    fr = sum(p for k, p in pi.items() if any((b in candt) for b in tp.trans[k] if b not in tp.trans))
    out['frontier_mass'] = float(fr); out['n_candidates_left'] = len(candt)
    return out, tp
