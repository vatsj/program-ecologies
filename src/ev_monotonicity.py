"""EV-monotonicity and weight responsiveness in arm T under islands -> infinity before time (queue 69 machinery).

Predictions: predictions/2026-11-08-ev-monotonicity.md.  Report: runs/ev-monotonicity.{md,json}.

Outcome payoffs are modified in dollars before the A_f charge (net = modified gross - P_fail * (failed reads + forfeits)),
and the exact Moran kernel PF is rebuilt from the modified table; everything else is many_islands_t / _ode / _worlds.

  penalty c : every outcome whose class is U (unequal pair), G (grand split) or W (wasteful) loses c for every player
              whose gross amount there is positive; fair pairs (F) and disagreement (D) unchanged.
  bonus   b : the fair pair F0 = (1/2, 1/2, 0) (slots 0 and 1 named each other) pays b more to slots 0 and 1.

A penalty is rotation-equivariant (the symmetric ODE applies); a bonus is not (the ODE is integrated unsymmetrized from
the symmetric natural start).

    python3 src/ev_monotonicity.py pools                  recompute the main-dose P_fail 0.1 pools (3 x 16,384 islands)
    python3 src/ev_monotonicity.py job mf:<c>:<b>:<pool>[:raw]
    python3 src/ev_monotonicity.py job w:<c>:<b>:<I>:<nworlds>
    python3 src/ev_monotonicity.py batch JOBS --workers 3
    python3 src/ev_monotonicity.py report
"""
import os, sys, json, time, subprocess
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import many_islands_t as M
import many_islands_t_ode as O
from many_islands_t_common import SCR, NPOOL, tabs, load_pool, pool_path, DOSEID

ROOT = os.path.dirname(HERE)
CELL = 'main|0.1|0'
PFAIL = 0.1
EVOUT = os.path.join(SCR, 'evout')
CPS = (1, 3, 10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000)
CLS_U, CLS_G, CLS_W = 1, 2, 3
_PF = {}


def modified_payoff(T, p_fail, c=0.0, b=0.0):
    """net payoff table (27,27,27,3) in dollars with the penalty c and the F0 bonus b (before the A_f charge)."""
    G = T.GROSS.copy()
    if c:
        cls = T.CL[..., None]
        bad = np.isin(cls, (CLS_U, CLS_G, CLS_W)) & (G > 1e-12)
        G = G - c * bad
    if b:
        f0 = (T.PAIR == 0)
        G[f0, 0] += b
        G[f0, 1] += b
    return G - p_fail * T.NTO - p_fail * T.FO


def get_pf(c, b, p_fail=PFAIL):
    k = (round(c, 6), round(b, 6), p_fail)
    if k not in _PF:
        _PF[k] = M.make_pf(modified_payoff(tabs(), p_fail, c, b))
    return _PF[k]


def nat_start(pool, raw=False):
    x = O.hist_to_x(load_pool(CELL, pool))
    return x if raw else O.symmetrize(x)


def run_mf(c, b, pool, raw=False, tmax_end=1e7):
    """mean-field ODE from the pool's natural start.  Symmetric subspace iff c-only (rotation-equivariant) and not raw."""
    t0 = time.time()
    T = tabs()
    PF = get_pf(c, b)
    sym = (b == 0.0) and not raw
    x0 = nat_start(pool, raw)
    recs, x, st, _ = O.integrate(x0, PF, 1e5, T, sym=sym, stop_converged=True)
    status = st
    if status != 'converged':
        recs, x, status = O.integrate_be(x, 1e5, PF, T, tmax_end if sym else 1e6 if raw else tmax_end, sym=sym, steps_per_decade=8, recs=recs)
    return dict(c=c, b=b, pool=pool, raw=raw, sym=sym, status=status, recs=recs, t_end=recs[-1]['t'], resid_end=recs[-1]['resid'],
                final_shares=recs[-1]['shares'], final_pairs=recs[-1]['pairs'], min_x=min(r['minx'] for r in recs),
                mass_dev=max(abs(r['mass'] - 1.0) for r in recs), wall=round(time.time() - t0, 1))


def run_worlds(c, b, I, nworlds, tmax=100000, seed_tag=None):
    """finite worlds as in many_islands_t_run.run_world_job (same seeds, same pooled raw founding histogram), kernel modified."""
    import many_islands_t_worlds as WD
    T = tabs()
    PF = get_pf(c, b)
    hist = sum(load_pool(CELL, p) for p in range(NPOOL))
    cps = np.array([t for t in CPS if t <= tmax], np.int64)
    rows = []
    t0 = time.time()
    for w in range(nworlds):
        rng = np.random.default_rng([31, DOSEID['main'], int(round(PFAIL * 1000)), 0, I, w])    # the queue-69 seeds
        tri = WD.sample_world(hist, I, rng)
        r = WD.run_world(PF, T, tri, cps, int(rng.integers(1 << 31)))
        rows.append(dict(w=w, hist=r['hist'].tolist(), pairs=r['pairs'].tolist(), first_loss=r['first_loss'].tolist(), events=r['events']))
    return dict(c=c, b=b, I=I, cps=cps.tolist(), worlds=rows, wall=round(time.time() - t0, 1))


def jname(j):
    return j.replace(':', '_')


def jpath(j):
    return os.path.join(EVOUT, jname(j) + '.json')


def _default(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def run_job(j):
    p = j.split(':')
    if p[0] == 'mf':
        return dict(job=j, **run_mf(float(p[1]), float(p[2]), int(p[3]), raw=len(p) > 4 and p[4] == 'raw'))
    if p[0] == 'w':
        return dict(job=j, **run_worlds(float(p[1]), float(p[2]), int(p[3]), int(p[4])))
    raise ValueError(j)


def worker(jobfile):
    os.makedirs(EVOUT, exist_ok=True)
    for j in [l.strip() for l in open(jobfile) if l.strip() and not l.startswith('#')]:
        if os.path.exists(jpath(j)):
            continue
        claim = jpath(j) + '.claim'
        try:
            fd = os.open(claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.close(fd)
        except FileExistsError:
            continue
        t0 = time.time()
        rec = run_job(j)
        json.dump(rec, open(jpath(j) + '.tmp', 'w'), default=_default)
        os.replace(jpath(j) + '.tmp', jpath(j))
        print('done', j, 'wall %.0f' % (time.time() - t0), flush=True)


def batch(jobfile, workers):
    ps = [subprocess.Popen([sys.executable, os.path.abspath(__file__), 'worker', jobfile]) for _ in range(workers)]
    for p in ps:
        p.wait()


PEN = (0.05, 0.1)
BON = (1 / 12, 1 / 6)


def make_jobs(path):
    js = []
    for pool in range(NPOOL):
        js.append('mf:0.0:0.0:%d' % pool)                       # validation + control
    for c in PEN:
        for pool in range(NPOOL):
            js.append('mf:%r:0.0:%d' % (c, pool))
    for b in BON:
        for pool in range(NPOOL):
            js.append('mf:0.0:%r:%d' % (b, pool))
    for (c, b) in [(0.0, 0.0)] + [(c, 0.0) for c in PEN] + [(0.0, b) for b in BON]:
        js.append('w:%r:%r:1024:20' % (c, b))
    open(path, 'w').write('\n'.join(js) + '\n')
    return js


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'pools':
        import many_islands_t_run as R
        for p in range(NPOOL):
            print(R.run_pool(CELL, p))
    elif a[0] == 'job':
        print(json.dumps(run_job(a[1]), default=_default)[:2000])
    elif a[0] == 'jobs':
        print(len(make_jobs(a[1])), 'jobs')
    elif a[0] == 'worker':
        worker(a[1])
    elif a[0] == 'batch':
        batch(a[1], int(a[2]) if len(a) > 2 else 3)


# ====================================================================== report
def _load(j):
    p = jpath(j)
    return json.load(open(p)) if os.path.exists(p) else None


def _rec_at(recs, t):
    for r in recs:
        if abs(r['t'] - t) < 1e-9 * max(t, 1):
            return r
    return None


def mf_table(c, b, raw=False):
    """pool-mean pairs / V* at 10^3, 10^4, 10^5 and at the end, plus per-pool end values and statuses."""
    rows = []
    out = dict(c=c, b=b, pools=[])
    for pool in range(NPOOL):
        d = _load('mf:%r:%r:%d' % (c, b, pool) + (':raw' if raw else ''))
        if d is None:
            return None
        out['pools'].append(dict(status=d['status'], t_end=d['t_end'], resid=d['resid_end'], pairs_end=d['final_pairs'],
                                 shares_end=d['final_shares'], min_x=d['min_x'], mass_dev=d['mass_dev']))
        rows.append(d)
    for lab, t in (('0', 0.0), ('1e3', 1e3), ('1e4', 1e4), ('1e5', 1e5), ('end', None)):
        ps, ss = [], []
        for d in rows:
            r = d['recs'][-1] if t is None else _rec_at(d['recs'], t)
            if r is None:                      # converged before t: carry the last record
                r = d['recs'][-1]
            ps.append(r['pairs']); ss.append(r['shares'])
        out[lab] = dict(pairs=np.mean(ps, axis=0).tolist(), shares=np.mean(ss, axis=0).tolist(), vstar=float(np.mean(ss, axis=0)[0]))
    return out


def world_summary(c, b, I=1024):
    d = _load('w:%r:%r:%d:20' % (c, b, I))
    if d is None:
        return None
    rows = d['worlds']
    pr = np.array([np.array(x['pairs']) for x in rows])            # (worlds, cps, 3)
    hs = np.array([np.array(x['hist']) for x in rows])             # (worlds, cps, 5)
    fin = pr[:, -1, :]
    fair = fin.sum(axis=1) / I
    single = (fair >= 0.99) & (fin.max(axis=1) / np.maximum(fin.sum(axis=1), 1) >= 0.95)
    dom = np.where(single, fin.argmax(axis=1), -1)
    cps = d['cps']
    sh = {}
    for t in (1000, 10000, 100000):
        k = cps.index(t)
        sh[str(t)] = dict(pair_mean=(pr[:, k, :].mean(axis=0) / I).tolist(), vstar_mean=float(hs[:, k, 0].mean() / I))
    return dict(c=c, b=b, I=I, n=len(rows), cons99=int((fair >= 0.99).sum()), single=int(single.sum()),
                dom_counts=[int((dom == q).sum()) for q in range(3)], unequal99=int((hs[:, -1, 1] / I >= 0.99).sum()),
                keep3=int(((fin / I) >= 0.05).all(axis=1).sum()), pair_mean_end=(fin.mean(axis=0) / I).tolist(),
                vstar_mean_end=float(fair.mean()), by_t=sh, fin=fin.tolist(), wall=d['wall'])


def validate_control():
    """c = 0, b = 0: pool-level and pool-mean trajectories against runs/many_islands_t/ode.json (to 1e-6), and the control
    worlds against runs/many_islands_t/worlds.json (identical seeds, so identical final pair counts)."""
    ref = json.load(open(os.path.join(ROOT, 'runs', 'many_islands_t', 'ode.json')))['main|0.1|0|nat']
    out = {}
    mine = mf_table(0.0, 0.0)
    if mine is None:
        return None
    dmax = 0.0
    rows = []
    for k, lab in (('0', '0'), ('100', None), ('1000', '1e3'), ('10000', '1e4'), ('100000', '1e5'), ('end', 'end')):
        rows.append(k)
    traj = ref['trajectory_mean_over_pools']
    cmp = {}
    for k, lab in (('0', '0'), ('1000', '1e3'), ('10000', '1e4'), ('100000', '1e5'), ('end', 'end')):
        a = np.array(traj[k]['shares']); m = np.array(mine[lab]['shares'])
        cmp[k] = float(np.abs(a - m).max())
    ends = []
    for i in range(NPOOL):
        a = np.array(ref['pools'][i]['shares_end']); m = np.array(mine['pools'][i]['shares_end'])
        ends.append(float(np.abs(a - m).max()))
    out['mf_max_abs_diff_mean_traj'] = cmp
    out['mf_max_abs_diff_pool_end'] = ends
    out['vstar_traj_stored'] = ref['vstar_traj']
    out['vstar_traj_mine'] = [mine[l]['vstar'] for l in ('0', '1e3', '1e4', '1e5', 'end')]
    w = world_summary(0.0, 0.0)
    if w is not None:
        sref = json.load(open(os.path.join(ROOT, 'runs', 'many_islands_t', 'worlds.json')))['main|0.1|0|1024']
        out['worlds_fin_identical'] = bool(np.array_equal(np.array(w['fin']), np.array(sref['fin'])))
        out['worlds_fin_max_abs_diff_counts'] = float(np.abs(np.array(w['fin']) - np.array(sref['fin'])).max())
    return out


def chi2_uniform(counts):
    from scipy.stats import chisquare
    n = sum(counts)
    if n < 3:
        return None
    return float(chisquare(counts).pvalue)


def report():
    js = dict(validation=validate_control(), mf={}, worlds={})
    md = ['# EV-monotonicity and weight responsiveness in arm T (2026-11-08)\n']
    md.append('Predictions `predictions/2026-11-08-ev-monotonicity.md`. Object: arm T, `dollar3`, main dose, A_f charge P_fail = 0.1, natural start '
              '(symmetrized post-anneal law; 3 recomputed pools of 16,384 islands), mean-field ODE (time = migrant events per island) and finite worlds '
              '(I = 1,024, 20 worlds, 10^5 events per island; finite-I, finite-time). Payoff modifications in dollars before the A_f charge.\n')
    v = js['validation']
    if v:
        md.append('## Validation (c = 0, b = 0)\n')
        md.append('Pool-mean class-share trajectory vs the stored `ode.json` (max abs difference over the five class shares): ' +
                  ', '.join('%s: %.2e' % (k, x) for k, x in v['mf_max_abs_diff_mean_traj'].items()) + '.\n')
        md.append('Per-pool end shares vs stored: ' + ', '.join('%.2e' % x for x in v['mf_max_abs_diff_pool_end']) + '.\n')
        md.append('V* trajectory (0, 10^3, 10^4, 10^5, end), mine: ' + ', '.join('%.6f' % x for x in v['vstar_traj_mine']) + '; stored (0, 10, 10^2, 10^3, 10^4, 10^5 and end checkpoints): ' +
                  ', '.join('%.6f' % x for x in v['vstar_traj_stored']) + '.\n')
        if 'worlds_fin_identical' in v:
            md.append('Control worlds (I = 1,024, queue-69 seeds): final pair counts identical to the stored worlds: %s (max abs diff %g).\n' % (v['worlds_fin_identical'], v['worlds_fin_max_abs_diff_counts']))
    md.append('## Mean field (pool mean of 3 natural-start trajectories)\n')
    md.append('| condition | t | V* | F0 (1/2,1/2,0) | F1 | F2 | status per pool |')
    md.append('|---|---|---|---|---|---|---|')
    conds = [('control c=0, b=0', 0.0, 0.0)] + [('penalty c=%g' % c, c, 0.0) for c in PEN] + [('bonus b=%.4g' % b, 0.0, b) for b in BON]
    for name, c, b in conds:
        t = mf_table(c, b)
        js['mf'][name] = t
        if t is None:
            continue
        for lab in ('1e3', '1e4', '1e5', 'end'):
            p = t[lab]['pairs']
            md.append('| %s | %s | %.6f | %.6f | %.6f | %.6f | %s |' % (name, lab if lab != 'end' else 'end (t = %s)' % ', '.join('%.2g' % q['t_end'] if 't_end' in q else '' for q in t['pools']),
                                                                      t[lab]['vstar'], p[0], p[1], p[2], ', '.join(q['status'] for q in t['pools']) if lab == 'end' else ''))
    md.append('\n## Finite worlds (I = 1,024, 20 worlds, to 10^5 events per island)\n')
    md.append('| condition | worlds >= 0.99 on fair pairs | single-pair worlds | consensus F0 / F1 / F2 | unequal consensus | all three pairs >= 0.05 | mean share F0 / F1 / F2 at 10^5 | mean V* at 10^5 | mean F0 share at 10^3 / 10^4 |')
    md.append('|---|---|---|---|---|---|---|---|---|')
    for name, c, b in conds:
        w = world_summary(c, b)
        js['worlds'][name] = w
        if w is None:
            continue
        pm = w['pair_mean_end']
        md.append('| %s | %d/20 | %d | %d / %d / %d | %d | %d | %.3f / %.3f / %.3f | %.4f | %.3f / %.3f |' % (
            name, w['cons99'], w['single'], *w['dom_counts'], w['unequal99'], w['keep3'], *pm, w['vstar_mean_end'],
            w['by_t']['1000']['pair_mean'][0], w['by_t']['10000']['pair_mean'][0]))
    pooled = np.zeros(3, int)
    for name, c, b in conds[1:3]:
        w = js['worlds'].get(name)
        if w:
            pooled += np.array(w['dom_counts'])
    js['penalty_pooled_dom_counts'] = pooled.tolist()
    js['penalty_pooled_chi2_p'] = chi2_uniform(pooled.tolist())
    md.append('\nPenalty single-pair worlds pooled over c: %s, chi-square p against uniform = %s.\n' % (pooled.tolist(), js['penalty_pooled_chi2_p']))
    os.makedirs(os.path.join(ROOT, 'runs'), exist_ok=True)
    json.dump(js, open(os.path.join(ROOT, 'runs', 'ev-monotonicity.json'), 'w'), default=_default)
    open(os.path.join(ROOT, 'runs', 'ev-monotonicity.md'), 'w').write('\n'.join(md) + '\n')
    print('\n'.join(md))


if __name__ == '__main__' and sys.argv[1] == 'report':
    report()
