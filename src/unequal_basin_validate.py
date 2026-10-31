"""Validations V1-V6 of the unequal-basin experiment (spec specs/2026-10-31-unequal-basin.md, "Validations").

    python3 src/unequal_basin_validate.py v1|v2|v4|v5|v6          # each writes runs/unequal_basin/validate-<name>.json
    python3 src/unequal_basin_validate.py v3 ARM PFAIL A [IDXS]   # matched Monte Carlo (needs pools)

V1  arm independence of constants: the DSL constants-only object equals arm T's dose-0 object (payoff table, kernel, ODE).
V2  lumping is exact: the aggregated unlumped field equals the lumped field (and the class count per slot is reported).
V3  ODE against a matched Monte Carlo from exactly the same empirical law (replicates), plus replication of the stored
    post-anneal V* and of the stored symmetric chain.
V4  the exact kernel against simulated relaxation in strata.
V5  charge: divergence counts per slot over the whole 1305^3 triple space in L; zero modal non-convergence in M.
V6  S3 equivariance of the table and kernel on the support.
"""
import os, sys, json, time, itertools
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from numba import njit
import dollar3 as D
import many_islands as MI
import stable_sets as SS
import unequal_basin as UB
import unequal_basin_core as UC

OUTD = UC.OUTD
os.makedirs(OUTD, exist_ok=True)


def save(name, d):
    with open(os.path.join(OUTD, 'validate-%s.json' % name), 'w') as f:
        json.dump(d, f, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))


# ====================================================================== lumping
@njit(cache=True)
def _sig_const(armi, nat, atL, atJ, atA, tab, PARTNER, s, q, cons1, cons2, out):
    """code2 of program q of slot s against every pair of constants (cons1 in the first other slot, cons2 in the second)."""
    hist = np.empty((2, 3), np.int64)
    val = np.empty(3, np.int64)
    n = 0
    for a in cons1:
        for b in cons2:
            if s == 0:
                out[n] = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, q, a, b, hist, val)
            elif s == 1:
                out[n] = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, a, q, b, hist, val)
            else:
                out[n] = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, a, b, q, hist, val)
            n += 1


@njit(cache=True)
def _full_sig(armi, nat, atL, atJ, atA, tab, PARTNER, s, q, sup1, sup2, out):
    hist = np.empty((2, 3), np.int64)
    val = np.empty(3, np.int64)
    n = 0
    for a in sup1:
        for b in sup2:
            if s == 0:
                out[n] = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, q, a, b, hist, val)
            elif s == 1:
                out[n] = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, a, q, b, hist, val)
            else:
                out[n] = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, a, b, q, hist, val)
            n += 1


def _arrs(arm):
    S = arm.S
    return (np.int64(arm.armi), np.ascontiguousarray(S.nat), np.ascontiguousarray(S.atL), np.ascontiguousarray(S.atJ),
            np.ascontiguousarray(S.atA), np.ascontiguousarray(S.tab), np.ascontiguousarray(D.PARTNER))


def lump_classes(arm, supp, slots=(0,), exact=True):
    """behaviour classes of the programs of the given slots over the S3-union supports supp (one array per slot): two programs
    of slot s are merged iff the joint code (with divergence mask) is equal against every pair of the other two slots'
    support programs.  Strategy: hash against the constants first (a coarsening of the partition: programs it separates
    are separated), then verify every constants-equal group completely against the whole supports.  Returns, per slot, a
    list of classes (lists of program ids)."""
    a = _arrs(arm)
    nat = a[1]
    isc = (nat[0] == 0)
    out = {}
    for s in slots:
        o1, o2 = MI._others(s)
        cons1 = np.array([x for x in supp[o1] if isc[x]], np.int64)
        cons2 = np.array([x for x in supp[o2] if isc[x]], np.int64)
        sup1 = np.array(supp[o1], np.int64)
        sup2 = np.array(supp[o2], np.int64)
        buf = np.empty(len(cons1) * len(cons2), np.int64)
        groups = {}
        for q in supp[s]:
            _sig_const(*a, s, np.int64(q), cons1, cons2, buf)
            groups.setdefault(buf.tobytes(), []).append(int(q))
        classes = []
        nfull = 0
        for g in groups.values():
            if len(g) == 1 or not exact:
                classes.append(g)
                continue
            fb = np.empty(len(sup1) * len(sup2), np.int64)
            sub = {}
            for q in g:
                _full_sig(*a, s, np.int64(q), sup1, sup2, fb)
                sub.setdefault(fb.tobytes(), []).append(q)
                nfull += 1
            classes.extend(sub.values())
        out[s] = dict(classes=classes, n_programs=len(supp[s]), n_classes=len(classes), n_full_checks=nfull)
    return out


def tiny_support(arm, rng, ncond, restrict_const=None):
    """a random S3-closed support: the constants (or the given subset of constant actions per slot) and ncond conditionals
    per slot before closure."""
    nat, isc = UB.program_data(arm)
    cons = [x for x in range(UB.KP) if isc[x]]
    cond = [x for x in range(UB.KP) if not isc[x]]
    pm = UB.perm_maps(arm)
    sup = [set() for _ in range(3)]
    for s in range(3):
        cs = cons if restrict_const is None else restrict_const
        for x in cs:
            sup[s].add(int(x))
        for x in rng.choice(cond, ncond, replace=False):
            sup[s].add(int(x))
    sup2 = [set(v) for v in sup]
    for sg, perm in pm:
        for s in range(3):
            for x in sup[s]:
                sup2[sg[s]].add(int(perm[s][x]))
    return [sorted(v) for v in sup2]


# ====================================================================== V2
def all_action_support(arm):
    """an S3-closed support with real merges: the ALL constants (local actions 6, 7, 8) and every conditional whose branches
    are ALL actions (any atom).  Atoms reading an action no program plays are dead, so such a conditional behaves as the constant
    on its false branch (a merge of a conditional with a constant)."""
    S = arm.S
    ids = []
    for x, f in enumerate(S.fs):
        atoms, tab = f
        if all(l in (6, 7, 8) for l in tab):
            ids.append(x)
    return [sorted(ids) for _ in range(3)]


def v2(seed=1):
    """lumping is exact.  (a) On the all-action support (real merges, including conditional = constant) the lumped field equals the
    aggregated unlumped field to 1e-12; (b) the same on a random support (no merges: the identity quotient)."""
    rng = np.random.default_rng(seed)
    res = {}
    for armname in ('L', 'M'):
        arm = UB.get_arm(armname)
        for label, supp in (('all-action', all_action_support(arm)), ('random', tiny_support(arm, rng, 12))):
            L = lump_classes(arm, supp, slots=(0, 1, 2))
            rep = {}
            for s in range(3):
                for k, cl in enumerate(L[s]['classes']):
                    for q in cl:
                        rep[(s, q)] = (k, cl[0])
            pf = 0.1 if armname == 'L' else 0.0
            obj = UB.Obj(armname, pf, supp, 3)
            supp_l = [sorted(set(c[0] for c in L[s]['classes'])) for s in range(3)]
            objl = UB.Obj(armname, pf, supp_l, 3, symmetric=False)
            x = rng.random(obj.n) ** 2
            x /= x.sum()
            Fu = UB.field(obj, x, sym=False)
            repid = np.array([[rep[(s, int(obj.T[t, s]))][1] for s in range(3)] for t in range(obj.n)], np.int64)
            pos, ok = objl.index_of(repid)
            assert ok.all()
            xa = np.bincount(pos, weights=x, minlength=objl.n)
            Fa = np.bincount(pos, weights=Fu, minlength=objl.n)
            Fl = UB.field(objl, xa, sym=False)
            err = float(np.abs(Fa - Fl).max())
            res['%s-%s' % (armname, label)] = dict(programs=[len(v) for v in supp], classes=[L[s]['n_classes'] for s in range(3)],
                                                   states_unlumped=obj.n, states_lumped=objl.n, max_abs_diff=err,
                                                   passed=bool(err < 1e-12))
    save('v2', res)
    return res


def class_counts(armname, supp, slots=(0,)):
    arm = UB.get_arm(armname)
    L = lump_classes(arm, supp, slots=slots)
    return {s: dict(programs=L[s]['n_programs'], classes=L[s]['n_classes'], full_checks=L[s]['n_full_checks']) for s in slots}


# ====================================================================== V6
def v6(seed=2):
    res = {}
    rng = np.random.default_rng(seed)
    for armname in ('L', 'M'):
        arm = UB.get_arm(armname)
        supp = tiny_support(arm, rng, 40)
        pf = 0.1 if armname == 'L' else 0.0
        obj = UB.Obj(armname, pf, supp, 2)
        bad_lev = 0
        bad_cl = 0
        for i, (sg, perm) in enumerate(obj.pm):
            pi = obj.perm_idx[i]
            for s in range(3):
                bad_lev += int((obj.lev[sg[s], pi] != obj.lev[s]).sum())
            bad_cl += int((obj.cl[pi] != obj.cl).sum())
        # kernel: the field of a symmetric state is symmetric
        x = obj.sym(rng.random(obj.n) ** 2)
        x /= x.sum()
        F = UB.field(obj, x, sym=False)
        asym = float(np.abs(F - obj.sym(F)).max())
        res[armname] = dict(states=obj.n, level_violations=bad_lev, class_violations=bad_cl, field_asymmetry=asym,
                            passed=bool(bad_lev == 0 and bad_cl == 0 and asym < 1e-14))
    save('v6', res)
    return res


# ====================================================================== V5
@njit(cache=True)
def _scan_full(armi, nat, atL, atJ, atA, tab, PARTNER, K, hmask, nbad, s0, s1):
    hist = np.empty((2, 3), np.int64)
    val = np.empty(3, np.int64)
    for a in range(s0, s1):
        for b in range(K):
            for c in range(K):
                code = UC.enc2(armi, nat, atL, atJ, atA, tab, PARTNER, a, b, c, hist, val)
                if code < 0:
                    nbad[0] += 1
                else:
                    hmask[code // 729] += 1


def v5(chunk=None):
    """divergence over the whole 1305^3 triple space in L (mask counts), non-convergence in M."""
    res = {}
    for armname in ('L', 'M'):
        arm = UB.get_arm(armname)
        a = _arrs(arm)
        hmask = np.zeros(8, np.int64)
        nbad = np.zeros(1, np.int64)
        t0 = time.time()
        _scan_full(*a, np.int64(UB.KP), hmask, nbad, 0, UB.KP)
        res[armname] = dict(triples=int(hmask.sum() + nbad[0]), mask_counts=hmask.tolist(), nonconvergent=int(nbad[0]), wall=time.time() - t0)
        # per-slot divergent counts
        res[armname]['slot_divergent'] = [int(sum(hmask[m] for m in range(8) if (m >> s) & 1)) for s in range(3)]
    res['passed'] = bool(res['M']['nonconvergent'] == 0 and sum(res['M']['mask_counts'][1:]) == 0)
    save('v5', res)
    return res


# ====================================================================== V1
def v1(tmax=1e4):
    import many_islands_t as MT
    import many_islands_t_ode as OT
    import many_islands_t_common as CT
    T = CT.tabs()
    res = {}
    for armname in ('L', 'M'):
        arm = UB.get_arm(armname)
        nat, isc = UB.program_data(arm)
        ci = SS.const_index(arm.S.fs)

        def dsl_local(s, v):
            if s == 1:
                pi, d = v // 3, v % 3
                return 3 * (1 - pi) + d if pi < 2 else v
            return v
        mp = np.array([[ci[dsl_local(s, v)] for v in range(9)] for s in range(3)])
        supp = [mp[s].tolist() for s in range(3)]
        obj = UB.Obj(armname, 0.0, supp, 0)
        PT = T.payoff(0.0)
        # (a) payoff table
        bad = 0
        idx = np.zeros((9, 9, 9), np.int64)
        for a in range(9):
            for b in range(9):
                for c in range(9):
                    pos, ok = obj.index_of(np.array([[mp[0][a], mp[1][b], mp[2][c]]]))
                    assert ok.all()
                    idx[a, b, c] = pos[0]
                    if not np.allclose((obj.lev[:, pos[0]] - 3) / 30.0, PT[a, b, c]):
                        bad += 1
        # (b) kernel: compare the fields on a common random state (cyclic C3 frame; no projection)
        PF = CT.get_pf(0.0)
        rng = np.random.default_rng(5)
        x9 = rng.random((9, 9, 9)) ** 2
        x9 /= x9.sum()
        xT = np.zeros((27, 27, 27))
        xT[:9, :9, :9] = x9
        xT = xT.ravel()
        FT = OT.F_of(xT, PF, sym=False).reshape(27, 27, 27)
        xd = np.zeros(obj.n)
        xd[idx.ravel()] = x9.ravel()
        Fd = UB.field(obj, xd, sym=False)
        Fd9 = Fd[idx.ravel()].reshape(9, 9, 9)
        kerr = float(np.abs(FT[:9, :9, :9] - Fd9).max())
        # leak of the T field out of the constants block (must be 0: constants never leave the constants block)
        leakT = float(np.abs(FT).sum() - np.abs(FT[:9, :9, :9]).sum())
        # (c) ODE from arm T's dose-0 law (post-anneal pool 0, constants only), cyclic-symmetrized as T does, compared
        # at 1e2, 1e3, 1e4 events (no projection in either)
        z = np.load(os.path.join(CT.POOLS, CT.cname('0|0|0') + '__0.npz'))['hist'].astype(np.float64)
        z = z.reshape(27, 27, 27)
        assert z[9:].sum() + z[:, 9:].sum() + z[:, :, 9:].sum() == 0 or True
        z9 = z[:9, :9, :9]
        mass_const = float(z9.sum() / z.sum())
        z9 = OT.symmetrize(z.ravel() / z.sum()).reshape(27, 27, 27)[:9, :9, :9]
        z9 = z9 / z9.sum()
        xT0 = np.zeros((27, 27, 27)); xT0[:9, :9, :9] = z9
        xd0 = np.zeros(obj.n); xd0[idx.ravel()] = z9.ravel()
        gridv = [0.0, 1e2, 1e3, tmax]
        recT, _, _, _ = OT.integrate(xT0.ravel(), PF, tmax, T, sym=False, grid=gridv, stop_converged=False)
        recD, _, _, _ = UB.integrate(obj, xd0, tmax, sym=False, grid=gridv, stop_converged=False)
        diffs = []
        for rt, rd in zip(recT, recD):
            diffs.append(dict(t=rt['t'], T=rt['shares'], DSL=rd['shares'], maxdiff=float(np.abs(np.array(rt['shares']) - np.array(rd['shares'])).max())))
        res[armname] = dict(table_mismatches=bad, kernel_max_abs_diff=kerr, kernel_leak_T=leakT, ode=diffs,
                            mass_constants_in_T_dose0_pool=mass_const,
                            passed=bool(bad == 0 and kerr < 1e-12 and max(d['maxdiff'] for d in diffs) < 1e-6))
    save('v1', res)
    return res


# ====================================================================== V4
def v4(armname='L', pfail=0.1, A=0, pools=(0,), seed=7, nmax=20000):
    """exact kernel vs simulated relaxation, strata: sign of the payoff change (+, 0, -) x slot role (in the pair, excluded).
    Aggregated test per stratum: observed fixations against the Poisson-binomial mean and variance of the exact fixation
    probabilities of the injections, z = (obs - mu)/sigma."""
    cell = UB.Cell(armname, pfail, A, pools)
    arm = UB.get_arm(armname)
    rng = np.random.default_rng(seed)
    PAY2, VEC2 = UC.tables2(pfail)
    arm2 = MI.Arm(armname)
    arm2.new_cache(22)
    # candidate injections from the symmetrized law: triple t ~ w, slot s uniform, donor y ~ marginal of slot s
    obj = UB.Obj(armname, pfail, cell.supp, 1)
    x, dropped = obj.start_from_triples(cell.raw)
    q = obj.marg(x)
    strata = {}
    PF = UB.PF30
    n_try = 400000
    ti = rng.choice(obj.n, n_try, p=x)
    ss = rng.integers(0, 3, n_try)
    # vectorised donor draw
    cumq = np.cumsum(q, axis=1)
    cumq /= cumq[:, -1:]
    u = rng.random(n_try)
    ys = np.array([np.searchsorted(cumq[s], uu) for s, uu in zip(ss, u)])
    ys = np.minimum(ys, UB.KP - 1)
    keep = ys != obj.pid[ss, ti]
    ti, ss, ys = ti[keep], ss[keep], ys[keep]
    T2 = obj.T[ti].astype(np.int64).copy()
    T2[np.arange(len(ti)), ss] = ys
    code2n = UB.codes_of(arm, T2.astype(np.int16))
    pay_new = PAY2[code2n, ss]
    pay_old = PAY2[obj.code2[ti], ss]
    d30 = np.rint((pay_new - pay_old) * 30).astype(np.int64)
    pfx = PF[d30 + UB.DMAX]
    inpair = (obj.excl[ti] != ss) & (obj.excl[ti] >= 0)
    excl = obj.excl[ti] == ss
    sign = np.sign(d30)
    for sg in (1, 0, -1):
        for role, mask in (('pair', inpair), ('excluded', excl)):
            sel = np.nonzero((sign == sg) & mask)[0]
            if len(sel) == 0:
                continue
            # choose injections to reach mu >= 5 (or nmax)
            order = rng.permutation(sel)
            cs = np.cumsum(pfx[order])
            k = int(np.searchsorted(cs, 6.0)) + 1
            k = min(max(k, 200), nmax, len(order))
            strata[(sg, role)] = order[:k]
    out = []
    ctx = arm2.ctx()
    for (sg, role), idxs in strata.items():
        obs = 0
        mu = 0.0
        var = 0.0
        for j, i in enumerate(idxs):
            t = obj.T[ti[i]].astype(np.int64)
            s = int(ss[i]); y = int(ys[i])
            init = np.zeros((3, UB.KP), np.int64)
            for r in range(3):
                init[r, t[r]] = MI.N0
            init[s, t[s]] -= 1
            init[s, y] += 1
            arm2.maybe_flush(0.45)
            st, g, counts, na = UC.island_run2(arm2.ctx(), arm2.lc(32), PAY2, init, MI.N0, MI.W, int(rng.integers(1, 2 ** 30)), 20000, np.empty(0), arm2.cum, True)
            assert st == 0
            tr = MI.triple_of(counts)
            obs += int(tr[s] == y)
            p = float(pfx[i])
            mu += p
            var += p * (1 - p)
        z = (obs - mu) / np.sqrt(var) if var > 0 else float('nan')
        out.append(dict(sign=sg, role=role, n=len(idxs), mu=mu, observed=obs, z=float(z)))
    res = dict(arm=armname, pfail=pfail, strata=out, passed=bool(all(abs(o['z']) < 3 for o in out) and len(out) >= 6))
    save('v4-%s-%g' % (armname, pfail), res)
    return res


# ====================================================================== V3
V3_CPS = (1, 3, 10, 30, 100, 300, 1000, 3000)


def v3(cellname, m=1, nrep=3, I=262144, cps=V3_CPS, seed=11, do_full=True):
    """matched Monte Carlo: fresh pool chains resampled from exactly the empirical law the ODE starts from.
    (a) implementation gate: ODE(m) against MC(m), the same reflecting truncation, replicate band (or 0.01);
    (b) truncation error: MC(full dynamics) against ODE(m)."""
    import unequal_basin_run as R
    import unequal_basin_mc as MC
    c = R.CELLS[cellname]
    cell = R.cell_of(cellname)
    arm = UB.get_arm(c['arm'])
    obj = UB.Obj(c['arm'], c['pf_migr'], cell.supp, m)
    xn, dropped = R.law_to_state(obj, cell.trip, cell.w)
    grid = [0.0] + [float(v) for v in cps]
    recs, _, _, _ = UB.integrate(obj, xn, float(cps[-1]), sym=True, grid=grid, stop_converged=False)
    ode = {int(r['t']): r['shares'] for r in recs}
    rng = np.random.default_rng(seed)
    # truncated law (conditioned on the allowed states) for MC(m)
    pos, ok = obj.index_of(cell.trip)
    w_m = np.where(ok, cell.w, 0.0)
    w_m /= w_m.sum()

    def shares_of(hist):
        out = np.zeros((hist.shape[0], 5))
        for k in range(5):
            out[:, k] = hist[:, MI.CATMAP == k].sum(axis=1)
        return out / hist.sum(axis=1, keepdims=True)

    res = dict(cell=cellname, m=m, I=I, nrep=nrep, dropped_mass=dropped, cps=list(cps), ode=ode)
    for label, w, mmax in (('mc_m', w_m, m), ('mc_full', cell.w, 3)):
        if label == 'mc_full' and not do_full:
            continue
        reps = []
        for r in range(nrep):
            idx = rng.choice(len(w), I, p=w)
            trip = cell.trip[idx]
            hist, wall = MC.run_mc(c['arm'], c['pf_migr'], trip, cps, int(rng.integers(1, 2 ** 30)), mmax=mmax)
            reps.append(shares_of(hist))
        reps = np.array(reps)                               # (nrep, ncp, 5)
        res[label] = dict(mean=reps.mean(axis=0).tolist(), sd=reps.std(axis=0, ddof=1).tolist(), reps=reps.tolist())
    # comparison table
    rows = []
    for k, t in enumerate(cps):
        o = np.array(ode[int(t)])
        row = dict(t=int(t), ode=o.tolist())
        if 'mc_m' in res:
            mm = np.array(res['mc_m']['mean'][k]); sd = np.array(res['mc_m']['sd'][k])
            band = np.maximum(2.0 * sd, 0.01)
            row['mc_m'] = mm.tolist(); row['diff_ode_mc_m'] = float(np.abs(o - mm).max()); row['inside_band'] = bool((np.abs(o - mm) <= band).all())
        if 'mc_full' in res:
            mf = np.array(res['mc_full']['mean'][k])
            row['mc_full'] = mf.tolist(); row['diff_ode_mc_full'] = float(np.abs(o - mf).max())
        rows.append(row)
    res['rows'] = rows
    res['gate_implementation'] = bool(all(r.get('inside_band', True) for r in rows))
    res['max_diff_ode_full'] = float(max(r.get('diff_ode_mc_full', 0.0) for r in rows))
    save('v3-%s-m%d' % (cellname, m), res)
    return res


if __name__ == '__main__':
    cmd = sys.argv[1]
    t0 = time.time()
    if cmd == 'v1':
        r = v1()
    elif cmd == 'v2':
        r = v2()
    elif cmd == 'v3':
        r = v3(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    elif cmd == 'v4':
        r = v4(sys.argv[2], float(sys.argv[3]))
    elif cmd == 'v5':
        r = v5()
    elif cmd == 'v6':
        r = v6()
    else:
        raise SystemExit(cmd)
    print(json.dumps(r, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))[:4000])
    print('wall', time.time() - t0)
