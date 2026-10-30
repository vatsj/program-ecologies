"""Validations of the arm-T islands experiment (spec 'Validation'): run before any counted cell (tables, charge, ode) and
after the pools exist (kernel, founding, arch).  Each returns a dict with a boolean 'pass' and the numbers."""
import os, sys, math
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import time, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lt_code as L
import churn_primary_t as CT
import many_islands_t as M
import many_islands_t_ode as O
from many_islands_t_common import tabs, get_pf, load_pool, parse_cell, NPOOL

NP = M.NP
NAME = None


def idx(T, name):
    return T.names.index(name)


# ---------------------------------------------------------------- hand-built triples (notes 1.2)
def hand_rows(T):
    """(triple names, expected failed reads per slot, expected gross payoffs in dollars)."""
    h = 0.5
    return [
        (('Snoy', 'C4', 'C1'), (0, 0, 0), (h, h, 0.0)),
        (('Snoy', 'C1', 'C1'), (0, 0, 0), (h, 0.0, h)),
        (('Snoy', 'Spoy', 'C1'), (1, 1, 0), (h, h, 0.0)),
        (('Snon', 'Spon', 'C1'), (1, 1, 0), (h, 0.0, h)),
        (('Snoy', 'Snoy', 'Snoy'), (1, 1, 1), (0.0, 0.0, 0.0)),
        (('Dnfy', 'Dpfy', 'Dpfy'), (1, 1, 1), (h, h, 0.0)),
        (('Dnfn', 'Dnfn', 'Dnfn'), (2, 2, 2), (0.0, 0.0, 0.0)),
        (('Snoy', 'Snoy', 'C4'), (0, 0, 0), (0.0, h, h)),
    ]


def v_tables():
    t0 = time.time()
    T = tabs()
    out = dict(name='tables')
    # (1) the 27^3 execution tables against the stored arm-T tables (churn_primary_t.TCat.tables(), uncached rebuild)
    cat = CT.TCat()
    code0, steps0 = L.run_big(cat._build)
    out['code_mismatch'] = int((code0[:NP, :NP, :NP] != T.code).sum())
    out['steps_mismatch'] = int((steps0[:NP, :NP, :NP] != T.steps).sum())
    # (2) the joint codes against the stored joint_codes
    JT0, ST0 = cat.joint_codes()
    out['joint_mismatch'] = int((JT0[:NP, :NP, :NP] != T.JT).sum())
    out['steps_joint_mismatch'] = int((ST0[:NP, :NP, :NP] != T.ST).sum())
    # (3) payoff and outcome lookups through the stored make_J path (price 0) and the step-price path
    import churn_primary as CP
    U = [np.arange(NP)] * 3
    tv = CP.TView(cat, 'main', 'T-main')
    J, PAYs, VECs = tv.make_J(U, 0.0)
    out['stored_make_J_mismatch'] = int((J[:NP, :NP, :NP] != T.JT).sum())
    c0 = 1.2e-4
    J2, PAY2, VEC2 = tv.make_J(U, c0)
    pay_stored = PAY2[J2]                                  # (27, 27, 27, 3)
    mine = T.GROSS - c0 * T.ST
    out['step_price_max_abs_diff'] = float(np.abs(pay_stored[:NP, :NP, :NP] - mine).max())
    out['outcome_mismatch'] = int((VEC2[J2][:NP, :NP, :NP] != T.OUT).sum())
    # (4) failed reads and forfeits
    out['forfeits_total'] = int(T.fo.sum())
    out['nto_hist'] = np.bincount(T.nto.ravel()).tolist()
    fam = np.array(T.fam)
    out['nto_const_max'] = int(T.nto[fam == 'const'].max())
    out['nto_single_exploit_max'] = int(T.nto[(fam == 'single') | (fam == 'exploit')].max())
    out['nto_two_max'] = int(T.nto[fam == 'two'].max())
    # failed read => a read cycle is reachable from the root (and the converse: no cycle reachable => none)
    edges = {}
    for i, nm in enumerate(T.names):
        f = fam[i]
        if f == 'const':
            edges[i] = ()
        elif f == 'single':
            edges[i] = ('n',) if nm[1] == 'n' else ('p',)
        elif f == 'two':
            edges[i] = ('n', 'p')
        else:
            edges[i] = ('n',) if nm[1] == 'n' else ('p',)
    viol = 0
    checked = 0
    for a in range(NP):
        for b in range(NP):
            for c in range(NP):
                prog = (a, b, c)
                # read graph on slots: slot s reads s+1 (n) or s-1 (p)
                g = {s: [(s + 1) % 3 if d == 'n' else (s - 1) % 3 for d in edges[prog[s]]] for s in range(3)}
                for s in range(3):
                    # is a cycle reachable from s?
                    seen = set(); stack = [s]; reach = set()
                    while stack:
                        u = stack.pop()
                        for v in g[u]:
                            if v not in reach:
                                reach.add(v); stack.append(v)
                    # a cycle is reachable from s iff some node reachable from s (or s) lies on a cycle
                    cyc = False
                    for u in list(reach):
                        r2 = set(); st2 = [u]
                        while st2:
                            w = st2.pop()
                            for v in g[w]:
                                if v not in r2:
                                    r2.add(v); st2.append(v)
                        if u in r2:
                            cyc = True; break
                    n_ = int(T.NTO[a, b, c, s])
                    checked += 1
                    if (n_ > 0) and not cyc:
                        viol += 1
    out['cycle_violations'] = viol
    out['cycle_checked'] = checked
    # (5) hand rows
    rows = []
    ok = True
    for names, nto, gross in hand_rows(T):
        t = tuple(idx(T, n) for n in names)
        got_nto = tuple(int(T.NTO[t[0], t[1], t[2], s]) for s in range(3))
        got_gross = tuple(float(T.GROSS[t[0], t[1], t[2], s]) for s in range(3))
        net = tuple(float(T.payoff(0.1)[t[0], t[1], t[2], s]) for s in range(3))
        match = (got_nto == nto) and np.allclose(got_gross, gross)
        ok &= match
        rows.append(dict(triple=names, nto=got_nto, expected_nto=nto, gross=got_gross, expected_gross=gross, net_at_0_1=net,
                         steps=[int(T.ST[t[0], t[1], t[2], s]) for s in range(3)], match=bool(match)))
    out['hand_rows'] = rows
    out['hand_rows_match'] = bool(ok)
    # (6) rotation equivariance, exhaustive
    out.update(equivariance(T))
    out['pass'] = bool(out['code_mismatch'] == 0 and out['steps_mismatch'] == 0 and out['joint_mismatch'] == 0 and
                       out['stored_make_J_mismatch'] == 0 and out['step_price_max_abs_diff'] < 1e-9 and out['outcome_mismatch'] == 0 and
                       out['forfeits_total'] == 0 and out['nto_const_max'] == 0 and out['nto_single_exploit_max'] <= 1 and
                       out['nto_two_max'] <= 2 and out['cycle_violations'] == 0 and ok and out['equiv_total_violations'] == 0)
    out['wall'] = round(time.time() - t0, 1)
    return out


def equivariance(T):
    """(a0, a1, a2) -> (a2, a0, a1) maps slot s to slot s + 1: gross and net payoffs, failed reads, forfeits, steps, the
    excluded slot of the outcome and the fixation tensor."""
    R = O.ROT1
    res = {}
    viol = 0
    for name, arr in (('gross', T.GROSS), ('nto', T.NTO), ('fo', T.FO), ('steps', T.ST)):
        A = arr.reshape(NP ** 3, 3)
        B = np.empty_like(A)
        # B[R t, s + 1] = A[t, s]
        for s in range(3):
            B[R, (s + 1) % 3] = A[:, s]
        d = int((A != B).sum()) if A.dtype.kind in 'iu' else int((np.abs(A - B) > 1e-12).sum())
        res['equiv_' + name] = d
        viol += d
    cl = T.CL.ravel(); out_ = T.OUT.ravel()
    d = int((cl[R] != cl).sum())
    res['equiv_class'] = d; viol += d
    ex = M.EXCL[out_]
    d = int(((ex[R] != (ex + 1) % 3) & (ex >= 0)).sum())
    res['equiv_excluded_slot'] = d; viol += d
    PF = get_pf(0.1)
    P2 = PF.reshape(3, NP ** 3, NP)
    d = 0
    for s in range(3):
        B = np.empty_like(P2[0])
        B[R] = P2[s]
        d += int((np.abs(P2[(s + 1) % 3] - B) > 1e-14).sum())
    res['equiv_pf'] = d; viol += d
    res['equiv_total_violations'] = viol
    return res


# ---------------------------------------------------------------- charge counter
def counted_eval(terms, a, b, c):
    class Ad:
        pass
    ad = Ad(); ad.terms = terms; ad.init3 = CT.TCat.init3
    with M.counting():
        return L.run_big(M.f_eval_counted, ad, a, b, c)


def v_charge():
    """the charge counter's rules (one charge per failed read, a frame closed by an enclosing expiry not separately, one
    charge for a forfeit) on hand-built programs; not the library's."""
    t0 = time.time()
    prog = CT._prog
    omega = '((lambda (x) (x x)) (lambda (x) (x x)))'
    cases = []
    consts = {'c1': prog('(lambda (me n p) 1)'), 'c4': prog('(lambda (me n p) 4)')}
    # a root that loops: forfeit (fuel runs out): 0 failed reads, 1 forfeit
    loop = prog('(lambda (me n p) %s)' % omega)
    # a read that expires at cap 5 (the partner is a reader that needs more steps), the root then returns 1: 1 failed read
    rd = prog(CT.src_single('n', 'o', 'y'))
    exp5 = prog('(lambda (me n p) (let ((r (capk 5 (run 5 n p) me))) 1))')
    # an expiring read followed by looping: 1 failed read + 1 forfeit
    exp_loop = prog('(lambda (me n p) (let ((r (capk 5 (run 5 n p) me))) %s))' % omega)
    # a finishing read of a constant (cap 400): 0
    fin = prog('(lambda (me n p) (let ((r (capk 400 (run 400 n p) me))) 1))')
    # two sequential expiring reads: 2
    two = prog('(lambda (me n p) (let ((r (capk 5 (run 5 n p) me))) (let ((s (capk 5 (run 5 p n) me))) 1)))')
    terms = [loop, exp5, exp_loop, fin, two, rd, consts['c1'], consts['c4']]
    names = ['loop', 'exp5', 'exp_loop', 'fin', 'two', 'rd', 'c1', 'c4']
    ix = {n: i for i, n in enumerate(names)}
    res = {}
    exp = {('loop', 'rd', 'c1'): (0, 1), ('exp5', 'rd', 'rd'): (1, 0), ('exp_loop', 'rd', 'rd'): (1, 1), ('fin', 'c1', 'c4'): (0, 0),
           ('two', 'rd', 'rd'): (2, 0), ('c1', 'rd', 'rd'): (0, 0), ('rd', 'c1', 'c4'): (0, 0)}
    ok = True
    rows = []
    for (a, b, c), (e_nto, e_fo) in exp.items():
        code, st, nto, fo = counted_eval(terms, ix[a], ix[b], ix[c])
        m = (nto == e_nto) and (fo == e_fo)
        ok &= m
        rows.append(dict(program=a, next=b, prev=c, failed_reads=nto, forfeits=fo, expected=(e_nto, e_fo), steps=st, code=code, match=bool(m)))
    # nested: the outer read of a reader pair expires once although the inner frames are closed by it (library check)
    T = tabs()
    t = (idx(T, 'Snoy'), idx(T, 'Spoy'), idx(T, 'C1'))
    nested = int(T.NTO[t[0], t[1], t[2], 0])
    ok &= (nested == 1)
    # the charge arithmetic: A_f charges forfeits like failed reads, A does not
    g = T.payoff(0.1)[t[0], t[1], t[2]]
    ok &= bool(np.allclose(g, [0.4, 0.4, 0.0]))
    # unit: w * (0.1 dollars) = 0.03; fixation ratio against neutral
    pf_ratio = float(M.pfix(-0.1, 100.0, 0.3) / 0.01)
    ok &= abs(pf_ratio - 0.1596) < 5e-4
    return dict(name='charge', rows=rows, nested_reader_pair_failed_reads=nested, net_payoff_pair=g.tolist(),
                pfix_ratio_minus_0_1=pf_ratio, **{'pass': bool(ok)}, wall=round(time.time() - t0, 1))


# ---------------------------------------------------------------- ODE checks
def v_ode():
    t0 = time.time()
    out = dict(name='ode')
    T = tabs()
    # 3-state / 2-state analytic: selection in one slot between two programs: logistic with rate (p1 - p0) / 3
    PF = np.zeros((3, NP, NP, NP, NP))
    p1, p0 = 0.12, 0.03
    PF[0, 0, 0, 0, 1] = p1      # migrant 1 into the resident 0 of slot 0
    PF[0, 1, 0, 0, 0] = p0
    x = np.zeros(NP ** 3)
    x[O.tidx(1, 0, 0)] = 0.1; x[O.tidx(0, 0, 0)] = 0.9
    r = (p1 - p0) / 3.0
    err = 0.0
    from scipy.integrate import solve_ivp
    sol = solve_ivp(lambda t, y: O.F_of(y, PF, False), (0, 200.0), x, t_eval=[5.0, 20.0, 50.0, 100.0, 200.0], method='DOP853', rtol=1e-10, atol=1e-14)
    for k, t in enumerate(sol.t):
        ex = 1.0 / (1.0 + 9.0 * math.exp(-r * t))
        err = max(err, abs(sol.y[O.tidx(1, 0, 0), k] - ex))
    out['logistic_max_err'] = err
    # neutral (voter) case: constant
    PF2 = np.zeros_like(PF); PF2[0, 0, 0, 0, 1] = 0.01; PF2[0, 1, 0, 0, 0] = 0.01
    sol2 = solve_ivp(lambda t, y: O.F_of(y, PF2, False), (0, 500.0), x, method='DOP853', rtol=1e-10, atol=1e-14)
    out['voter_drift'] = float(abs(sol2.y[O.tidx(1, 0, 0), -1] - 0.1))
    # forward Euler agrees with the adaptive solution on the logistic system
    xe_ = x.copy(); dt = 0.05
    for _ in range(int(200.0 / dt)):
        xe_ = xe_ + dt * O.F_of(xe_, PF, False)
    out['euler_vs_adaptive'] = float(abs(xe_[O.tidx(1, 0, 0)] - sol.y[O.tidx(1, 0, 0), -1]))
    # backward Euler agrees as well
    xb = x.copy(); tt = 0.0
    for _ in range(20):
        xb, info = O.be_step(xb, 10.0, PF, sym=False)
    out['be_vs_adaptive'] = float(abs(xb[O.tidx(1, 0, 0)] - sol.y[O.tidx(1, 0, 0), -1]))
    # mass conservation and nonnegativity on the arm-T kernel from a small founding pool (main, P = 0.1), symmetric and raw
    PT = T.payoff(0.1)
    law = M.seed_law(T, 'main'); cum = M.cum_of(law)
    rng = np.random.default_rng(3)
    h = np.zeros(M.NT)
    for i in range(3000):
        r_ = M.build_island(PT, law, cum, rng, int(rng.integers(1 << 30)), A=0)
        h[O.tidx(*r_['triple'])] += 1
    x0 = O.hist_to_x(h)
    PFm = get_pf(0.1)
    recs, xe, st, _ = O.integrate(O.symmetrize(x0), PFm, 3e3, T, sym=True, stop_converged=False)
    out['mass_dev_max'] = max(abs(r_['mass'] - 1.0) for r_ in recs)
    out['min_x'] = min(r_['minx'] for r_ in recs)
    recs_raw, xr, st, _ = O.integrate(x0, PFm, 3e3, T, sym=False, stop_converged=False)
    out['mass_dev_max_raw'] = max(abs(r_['mass'] - 1.0) for r_ in recs_raw)
    out['min_x_raw'] = min(r_['minx'] for r_ in recs_raw)
    # sym integration equals raw integration of the symmetrized law for a short time (the field is equivariant)
    recs_s2, xs2, _, _ = O.integrate(O.symmetrize(x0), PFm, 300.0, T, sym=False, stop_converged=False)
    recs_s1, xs1, _, _ = O.integrate(O.symmetrize(x0), PFm, 300.0, T, sym=True, stop_converged=False)
    out['sym_vs_unprojected_300'] = float(np.abs(xs1 - xs2).sum())
    # field vs directional derivative: finite-difference check of jvp
    rng2 = np.random.default_rng(5)
    v = rng2.standard_normal(x0.size) * (x0 > 0)
    eps = 1e-6
    fd = (O.F_of(x0 + eps * v, PFm) - O.F_of(x0 - eps * v, PFm)) / (2 * eps)
    out['jvp_fd_err'] = float(np.abs(fd - O.jvp(x0, v, PFm)).max() / max(np.abs(fd).max(), 1e-300))
    out['pass'] = bool(err < 1e-6 and out['voter_drift'] < 1e-8 and out['euler_vs_adaptive'] < 5e-3 and out['be_vs_adaptive'] < 2e-2 and
                       out['mass_dev_max'] < 1e-9 and out['min_x'] > -1e-9 and out['mass_dev_max_raw'] < 1e-9 and
                       out['sym_vs_unprojected_300'] < 1e-8 and out['jvp_fd_err'] < 1e-5)
    out['wall'] = round(time.time() - t0, 1)
    return out


# ---------------------------------------------------------------- kernel against simulated relaxation
def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def simulate_injection(T, PT, cum, tr, s, y, seed):
    init = np.zeros((3, NP), np.int64)
    for q in range(3):
        init[q, tr[q]] = M.N0
    init[s, tr[s]] -= 1
    init[s, y] += 1
    status, g, counts, _ = M.island_run_t(PT, init, M.N0, M.W, int(seed) % (2 ** 31), 8000, np.zeros(0), cum, True)
    return int(status == 0 and counts[s, y] == M.N0), int(status)


def v_kernel(P=0.1, per_stratum=200, max_tries=3_000_000):
    t0 = time.time()
    T = tabs()
    PT = T.payoff(P)
    PF = get_pf(P)
    cell = 'main|%s|0' % P
    hists = [load_pool(cell, p) for p in range(NPOOL)]
    x0 = O.symmetrize(O.hist_to_x(sum(hists)))
    xs = {'post-anneal': x0}
    recs, x3, st, kept = O.integrate(x0, PF, 1e3, T, sym=True, stop_converged=False, keep_x_at=(1e3,))
    xs['ode-1e3'] = x3
    cum = M.cum_of(M.seed_law(T, 'main'))
    rng = np.random.default_rng(99)
    strata = {}
    names = []
    for sel in ('neutral', 'small+', 'small-', 'large+', 'large-'):
        for pat in ('none', 'timeout'):
            names.append((sel, pat))
    need = {k: per_stratum for k in names}
    fixed = {k: 0 for k in names}; cnt = {k: 0 for k in names}; expp = {k: 0.0 for k in names}; var = {k: 0.0 for k in names}
    src = {k: {'post-anneal': 0, 'ode-1e3': 0} for k in names}
    pools_ = {}
    for nm, xx in xs.items():
        pools_[nm] = (np.cumsum(xx) / xx.sum(), O.marginals(xx))
    tries = 0
    cm = {nm: pools_[nm][0] for nm in pools_}
    while any(cnt[k] < need[k] for k in names) and tries < max_tries:
        tries += 1
        nm = 'post-anneal' if rng.random() < 0.5 else 'ode-1e3'
        tidx_ = int(np.searchsorted(cm[nm], rng.random() * cm[nm][-1]))
        tidx_ = min(tidx_, M.NT - 1)
        tr = (tidx_ // (NP * NP), (tidx_ // NP) % NP, tidx_ % NP)
        s = int(rng.integers(3))
        q = pools_[nm][1][s]
        y = int(np.searchsorted(np.cumsum(q), rng.random() * q.sum()))
        y = min(y, NP - 1)
        if y == tr[s]:
            continue
        t2 = list(tr); t2[s] = y
        d = float(PT[t2[0], t2[1], t2[2], s] - PT[tr[0], tr[1], tr[2], s])
        a = M.W * d
        if abs(a) < 1e-12:
            sel = 'neutral'
        elif 0 < a <= 0.05 + 1e-12:
            sel = 'small+'
        elif -0.05 - 1e-12 <= a < 0:
            sel = 'small-'
        elif a > 0:
            sel = 'large+'
        else:
            sel = 'large-'
        pat = 'timeout' if (T.NTO[tr[0], tr[1], tr[2], s] > 0 or T.NTO[t2[0], t2[1], t2[2], s] > 0) else 'none'
        k = (sel, pat)
        if cnt[k] >= need[k]:
            continue
        fx, stt = simulate_injection(T, PT, cum, tr, s, y, rng.integers(1 << 31))
        p = float(PF[s, tr[0], tr[1], tr[2], y])
        cnt[k] += 1; fixed[k] += fx; expp[k] += p; var[k] += p * (1 - p); src[k][nm] += 1
    rows = []
    allok = True
    for k in names:
        n = cnt[k]
        if n == 0:
            rows.append(dict(stratum='%s/%s' % k, n=0, note='stratum not reached in %d draws' % tries)); continue
        mu = expp[k]; sd = math.sqrt(max(var[k], 1e-300))
        z = (fixed[k] - mu) / sd if sd > 1e-12 else 0.0
        lo, hi = wilson(fixed[k], n)
        ok = abs(z) < 3.0 and (lo - 0.005 <= mu / n <= hi + 0.005)
        allok &= ok
        rows.append(dict(stratum='%s/%s' % k, n=n, fixed=fixed[k], expected=mu, z=z, freq=fixed[k] / n, mean_pfix=mu / n,
                         wilson=[lo, hi], ok=bool(ok), from_post=src[k]['post-anneal'], from_ode=src[k]['ode-1e3']))
    return dict(name='kernel', P=P, rows=rows, forfeit_stratum='empty: no triple has a forfeit (E1)', draws=tries,
                **{'pass': bool(allok)}, wall=round(time.time() - t0, 1))


# ---------------------------------------------------------------- founding against the stored churn experiment
def v_founding():
    t0 = time.time()
    T = tabs()
    cell = 'main|0|0'
    shares = []
    eff = []
    for p in range(NPOOL):
        x = O.hist_to_x(load_pool(cell, p))
        sh = O.class_shares(x, T)
        shares.append(sh)
        tot = np.array([M.MI.TOT[o] for o in T.OUT.ravel()])
        eff.append(float((x * tot).sum()))
    shares = np.array(shares)
    stored = json.load(open(os.path.join(M.ROOT, 'runs', 'churn-primary.json')))['lottery']['T-main|c0=0']['0']
    vs_stored = stored['vstar']
    fm = float(shares[:, 0].mean())
    half = 4.30 * float(shares[:, 0].std(ddof=1)) / math.sqrt(NPOOL)
    return dict(name='founding', mine_vstar=fm, mine_vstar_halfwidth=half, mine_per_pool=shares[:, 0].tolist(),
                stored_vstar=vs_stored, stored_eff=stored['eff'], mine_eff=float(np.mean(eff)),
                within_stored_ci=bool(vs_stored[1] - 0.01 <= fm <= vs_stored[2] + 0.01),
                note='stored: 40 runs x 64 islands at the generation the island is locally closed (stop %.0f), V* share incl. member-mixed; '
                     'mine: 3 x 16,384 settled islands (monomorphic), geometry differs' % stored['stop'],
                **{'pass': True}, wall=round(time.time() - t0, 1))


# ---------------------------------------------------------------- ODE against the archipelago at I = 4096
def v_arch():
    import many_islands_t_worlds as WD
    t0 = time.time()
    T = tabs()
    rows = []
    allok = True
    for P in (0.0, 0.1):
        cell = 'main|0|0' if P == 0.0 else 'main|%s|0' % P
        PF = get_pf(P)
        hist = sum(load_pool(cell, p) for p in range(NPOOL))
        x0 = O.hist_to_x(hist)
        recs, x3, st, kept = O.integrate(x0, PF, 1e3, T, sym=False, stop_converged=False)
        ode_v = recs[-1]['shares'][0]
        vs = []
        for w in range(20):
            rng = np.random.default_rng([41, int(P * 1000), w])
            tri = WD.sample_world(hist, 4096, rng)
            r = WD.run_world(PF, T, tri, [10, 100, 1000], int(rng.integers(1 << 31)))
            vs.append(r['hist'][-1, 0] / 4096.0)
        d = abs(float(np.mean(vs)) - ode_v)
        ok = d < 0.02
        allok &= ok
        rows.append(dict(P=P, ode_vstar_1e3=ode_v, worlds_mean=float(np.mean(vs)), worlds_sd=float(np.std(vs, ddof=1)), diff=d, ok=bool(ok)))
    return dict(name='arch', rows=rows, **{'pass': bool(allok)}, wall=round(time.time() - t0, 1))


def v_dslcmp():
    import many_islands_t_dslcmp as DC
    return DC.run()


def run(name):
    return {'dslcmp': v_dslcmp, 'tables': v_tables, 'charge': v_charge, 'ode': v_ode, 'kernel': v_kernel, 'founding': v_founding, 'arch': v_arch}[name]()
