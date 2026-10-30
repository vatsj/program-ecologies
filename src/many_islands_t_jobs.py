"""Jacobian / perturbation job and kernel-analysis job of the arm-T islands experiment."""
import os, sys
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import many_islands_t as M
import many_islands_t_ode as O
import many_islands_t_jac as JA
import many_islands_t_analysis as AN
from many_islands_t_common import (parse_cell, tabs, get_pf, load_pool, xstar_path, ode_result, NPOOL)


def _fit_rate(ts, Ns, lo, hi):
    ts = np.asarray(ts); Ns = np.asarray(Ns)
    m = (Ns >= lo) & (Ns <= hi) & (Ns > 0)
    if m.sum() < 3:
        return None
    return float(np.polyfit(ts[m], np.log(Ns[m]), 1)[0])


def growth_run(x, PF, tabs_, xp, T_end, n_grid=40):
    """integrate the unprojected equation from xp and record the non-invariant norm."""
    from scipy.integrate import solve_ivp
    grid = np.unique(np.concatenate([[0.0], np.geomspace(10.0, T_end, n_grid)]))
    xs = xp.copy()
    ts = [0.0]; Ns = [JA.nonsym_norm(xs)]; V = []
    sh, pairs = O.class_shares(xs, tabs_, True)
    V.append(pairs.tolist())
    fun = lambda t, y: O.F_of(y, PF, False)
    for i in range(1, len(grid)):
        sol = solve_ivp(fun, (grid[i - 1], grid[i]), xs, method='DOP853', rtol=1e-9, atol=1e-16)
        xs = sol.y[:, -1]
        ts.append(float(grid[i])); Ns.append(JA.nonsym_norm(xs))
        V.append(O.class_shares(xs, tabs_, True)[1].tolist())
        if Ns[-1] > 0.5:
            break
    return ts, Ns, V


def run_jac(cell, pm, pool):
    t0 = time.time()
    T = tabs()
    PF = get_pf(pm)
    x = np.load(xstar_path(cell, pm, 'nat', pool))
    odr = ode_result(cell, pm, 'nat', pool)
    out = dict(cell=cell, pm=pm, pool=pool, ode_status=odr['status'], ode_t_end=odr['t_end'], ode_resid=odr['resid_end'],
               shares_at_x=O.class_shares(x, T).tolist())
    rep = None
    for thr in (1e-9, 1e-8, 1e-7, 1e-6):
        idx = JA.support(x, thr)
        if len(idx) <= 6000:
            break
    rep, (idx, Tm, evec, order, ev) = JA.spectrum_report(x, PF, T, thr=thr)
    out['spectrum'] = rep
    # sensitivity to the support threshold
    sens = []
    for thr2 in (thr * 10, thr * 100):
        try:
            r2, _ = JA.spectrum_report(x, PF, T, thr=thr2, k_top=2)
            sens.append(dict(thr=thr2, support=r2['support'], noninv_max=r2['noninv_max'], leak_rate=r2['leak_rate']))
        except Exception as e:                                           # pragma: no cover
            sens.append(dict(thr=thr2, error=repr(e)))
    out['support_sensitivity'] = sens
    # full-space Arnoldi in the sector
    try:
        ev_full, conv = JA.arnoldi_top(x, PF, k=6)
        out['arnoldi_full'] = [[float(e.real), float(e.imag)] for e in ev_full]
        out['arnoldi_converged'] = bool(conv)
    except Exception as e:                                               # pragma: no cover
        out['arnoldi_full'] = repr(e)
    # controlled perturbations
    lam = rep['noninv_max']
    kk = order[0]
    v = (Tm @ evec[:, kk])
    lead = np.real(v)
    rng = np.random.default_rng(7)
    r = np.zeros(x.size); r[idx] = rng.standard_normal(len(idx))
    r = r - O.symmetrize(r)
    rand = r[idx]
    pert = []
    for kind, vec in (('lead', lead), ('random', rand)):
        for eps in (1e-6, 1e-4, 1e-2):
            xp, u = JA.perturbation(x, idx, vec, eps)
            N0 = JA.nonsym_norm(xp)
            if lam > 1e-6:
                Tend = float(min(2e5, max(3000.0, np.log(0.2 / N0) / lam * 1.3)))
            else:
                Tend = 2e4
            ts, Ns, V = growth_run(x, PF, T, xp, Tend)
            rate = _fit_rate(ts, Ns, 3 * N0, 0.05)
            rate_early = _fit_rate(ts, Ns, N0 * 0.5, N0 * 1e6) if rate is None else None
            pert.append(dict(kind=kind, eps=eps, N0=N0, lam_jac=lam, T_end=ts[-1], rate_fit=rate, rate_early=rate_early,
                             ts=ts, Ns=Ns, pairs=V))
    out['perturbations'] = pert
    out['wall'] = round(time.time() - t0, 1)
    return out


def run_analysis(cell, pm):
    t0 = time.time()
    T = tabs()
    PF = get_pf(pm)
    dose, P, A = parse_cell(cell)
    laws = []
    supp = []
    hists = [load_pool(cell, p) for p in range(NPOOL)]
    for h in hists:
        supp.append(int((h > 0).sum()))
    union = int((sum(hists) > 0).sum())
    xs = [O.symmetrize(O.hist_to_x(h)) for h in hists]
    x0 = np.mean(xs, axis=0)
    law = M.seed_law(T, dose)
    xf = AN.founding_x(T, law)
    out = dict(cell=cell, pm=pm, support_per_pool=supp, support_union=union)
    out['charges_founding'] = AN.charge_stats(xf, T)
    out['charges_post'] = AN.charge_stats(x0, T)
    out['conv_post'] = AN.conversion_rates(x0, PF, T)
    out['ka_post'] = AN.kappa_alpha(x0, PF, T)
    out['class_rates_post'] = AN.sum_flux_classes(x0, PF, T).tolist()
    xl = xstar_path(cell, pm, 'nat', 0)
    if os.path.exists(xl):
        xv = np.load(xl)
        out['charges_limit'] = AN.charge_stats(xv, T)
        out['conv_limit'] = AN.conversion_rates(xv, PF, T)
        out['ka_limit'] = AN.kappa_alpha(xv, PF, T)
    out['wall'] = round(time.time() - t0, 1)
    return out
