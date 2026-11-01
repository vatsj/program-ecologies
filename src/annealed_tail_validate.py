"""Validations of the annealed-tail experiment (spec: V1 Lam = 0 reproduces queue 70 / 69, V2 linearity and mass, V3 the tail kernel
against Monte Carlo, V4 single-arrival assay, cell-8 numerical and symmetry checks).

    python3 src/annealed_tail_validate.py v1|v2|v3|v4|v8a|v8b ...
"""
import os, sys, json, time, glob
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import many_islands as MI
import unequal_basin as UB
import unequal_basin_core as UC
import annealed_tail as A

VD = os.path.join(A.OUTD, 'validation')
os.makedirs(VD, exist_ok=True)


def save(name, d):
    json.dump(d, open(os.path.join(VD, name + '.json'), 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))


# ---------------------------------------------------------------------------------------------------------------- V1
def stored_endpoint(cell, start):
    """queue 70's stored object-P row (pilot_L core, m = 3, full pools, no ablation) for (cell, start): the last record."""
    out = []
    for f in glob.glob(os.path.join(UC.OUTD, 'rows', '%s_m3_%s_full_*.json' % (cell, start.replace(':', '')))):
        r = json.load(open(f))
        if r['spec'].get('core') == 'pilot_L' and r.get('states') in (474849, 475335) and r.get('status') == 'converged' and not r['spec'].get('raw') \
                and not r['spec'].get('tag') and not r['spec'].get('pools'):
            out.append((f, r))
    return out


def v1():
    res = {}
    for cell, start in (('M0', 'nat'), ('L0', 'nat'), ('M0', 'u:0.6'), ('L0', 'u:0.6')):
        spec = dict(kind='late0' if (cell, start) == ('M0', 'nat') else 'dsl', cell=cell, start=start, sched=dict(kind='anneal', Lam=0))
        row = A.load_row(spec)
        st = stored_endpoint(cell, start)
        if row is None or not st:
            res['%s %s' % (cell, start)] = dict(available=False, mine=row is not None, stored=len(st))
            continue
        f, r = st[0]
        mine = np.array(row['shares'])
        theirs = np.array(r['records'][-1]['shares'])
        # trajectory at common times
        diffs = []
        for rec in row['records']:
            for rr in r['records']:
                if abs(rr['t'] - rec['t']) <= 1e-6 * max(1, rec['t']) and rec['t'] in (100.0, 1000.0, 10000.0):
                    diffs.append(float(np.abs(np.array(rec['shares']) - np.array(rr['shares'])).max()))
        res['%s %s' % (cell, start)] = dict(mine=mine.tolist(), stored=theirs.tolist(), endpoint_maxdiff=float(np.abs(mine - theirs).max()),
                                            traj_maxdiff=max(diffs) if diffs else None, class_mine=row['class'], class_stored=r['endpoint'],
                                            stored_file=os.path.basename(f))
    # arm T natural, pool 0, both charges
    import many_islands_t_common as CT
    for cellT, pm in (('main|0.1|0', 0.1), ('main|0|0', 0.0)):
        for start, sname in (('nat', 'nat'), ('u:0.8', None)):
            if sname is None:
                continue
            Sy, T, _ = A.armT_system(cellT, pm)
            x0, info = A.armT_start(cellT, start)
            r, xe, _ = A.run_cell(Sy, x0, A.Sched('anneal', 0.0), tmax=1e8)
            st = CT.ode_result(cellT, '%.1f' % pm if False else str(float(pm)), 'nat', 0)
            key = 'armT %s %s' % (cellT, start)
            entry = dict(mine=r['shares'], status=r['status'], cls=r['class'])
            if st is not None:
                # stored result format: records / final shares
                fs = st.get('final_shares') or (st['records'][-1]['shares'] if 'records' in st else None)
                if fs is not None:
                    entry['stored'] = fs
                    entry['maxdiff'] = float(np.abs(np.array(fs) - np.array(r['shares'])).max())
            res[key] = entry
    save('v1', res)
    return res


# ---------------------------------------------------------------------------------------------------------------- V2
def v2():
    cell, obj, xn, dropped = A.dsl_base('M0')
    S = A.DSL(obj, cell.arm.laws)
    x0, _ = A.dsl_start(obj, xn, 'nat')
    rng = np.random.default_rng(1)
    q1 = np.abs(rng.standard_normal(cell.arm.laws.shape)) * (cell.arm.laws > 0)
    q1 /= q1.sum(axis=1, keepdims=True)
    q2 = obj.marg(x0)
    a, b = 0.37, 1.9
    g12 = S._flux(x0, a * q1 + b * q2)
    lin = float(np.abs(g12 - a * S._flux(x0, q1) - b * S._flux(x0, q2)).max())
    cons = {}
    for e in (0.0, 1.0, 30.0, 300.0):
        f = S.F(x0) + e * S.G(x0)
        cons[str(e)] = float(abs(f.sum()))
    # equivariance of the tail field (S3): G(sigma x) = sigma G(x)
    Gx = S.G(x0)
    sym_err = 0.0
    for pi in obj.perm_idx[1:]:
        sym_err = max(sym_err, float(np.abs(Gx[pi] - Gx).max()))
    # arm T
    SyT, T, CT = A.armT_system('main|0.1|0', 0.1)
    xT, _ = A.armT_start('main|0.1|0', 'nat')
    rng = np.random.default_rng(2)
    pT = np.abs(rng.standard_normal(27)); pT /= pT.sum()
    O = SyT.O
    qT = SyT.qof(xT)
    def GT(q):
        out = np.zeros_like(xT)
        O._rhs_bi(xT, np.tile(q, (3, 1)) if q.ndim == 1 else q, SyT.PF, out)
        return out
    linT = float(np.abs(GT(a * pT + b * qT[0]) - a * GT(pT) - b * GT(qT[0])).max()) if False else None
    consT = {str(e): float(abs((SyT.F(xT) + e * SyT.G(xT)).sum())) for e in (1.0, 300.0)}
    res = dict(linearity_max_abs=lin, linearity_scale=float(np.abs(g12).max()), mass_conservation=cons, tail_field_S3_equivariance=sym_err,
               armT_mass_conservation=consT, restricted_prior_S3_error='see static.json')
    save('v2', res)
    return res


# ---------------------------------------------------------------------------------------------------------------- V3
def v3(Lam=10.0, t0=100.0, I=4096, nworld=4, cps=(1, 3, 10, 30, 100, 300, 1000, 3000, 10000), seed=21, cellname='M0'):
    import annealed_tail_mc as MC
    cell, obj, xn, dropped = A.dsl_base(cellname)
    S = A.DSL(obj, cell.arm.laws)
    x0, _ = A.dsl_start(obj, xn, 'nat')
    sched = A.Sched('anneal', Lam, t0)
    grid = [0.0] + [float(c) for c in cps]
    recs, x, st, _ = A.integrate(S, x0, sched, 0.0, float(cps[-1]), float(cps[-1]), explicit_grid=grid, stop_stationary=False)
    ode = {int(r['t']): r['shares'] for r in recs}
    rng = np.random.default_rng(seed)
    reps = []
    info = []
    c = UB.get_arm('M' if cellname.startswith('M') else 'L')
    pf = 0.0
    for w in range(nworld):
        idx = rng.choice(len(cell.w), I, p=cell.w)
        trip = cell.trip[idx]
        hist, inf = MC.run_mc_tail('M' if cellname.startswith('M') else 'L', pf, trip, cps, int(rng.integers(1, 2 ** 30)), Lam, t0)
        sh = np.zeros((len(cps), 5))
        for k in range(5):
            sh[:, k] = hist[:, MI.CATMAP == k].sum(axis=1)
        reps.append(sh / hist.sum(axis=1, keepdims=True))
        info.append(inf)
    reps = np.array(reps)
    mean, sd = reps.mean(axis=0), reps.std(axis=0, ddof=1)
    rows = []
    for k, t in enumerate(cps):
        o = np.array(ode[int(t)])
        d = np.abs(o - mean[k])
        rows.append(dict(t=int(t), ode=o.tolist(), mc=mean[k].tolist(), mc_sd=sd[k].tolist(), maxdiff=float(d.max()), vstar_diff=float(o[0] - mean[k][0])))
    res = dict(cell=cellname, Lam=Lam, t0=t0, I=I, nworld=nworld, rows=rows, mc_info=info,
               gate_0p02=bool(all(r['maxdiff'] < 0.02 for r in rows if r['t'] in (100, 1000, 10000))),
               max_diff_at_gate_times=float(max(r['maxdiff'] for r in rows if r['t'] in (100, 1000, 10000))))
    save('v3_%s_L%g_t%g' % (cellname, Lam, t0), res)
    return res


# ---------------------------------------------------------------------------------------------------------------- V4
def v4(armname='M', nmax=100000, seed=17):
    """single-arrival assay: prior arrivals into two key triples of M's endpoint support (a U triple and a fair triple), fixation by the
    closed-form kernel against direct Moran simulation of the island, strata by (triple, slot role, payoff change)."""
    cell, obj, xn, dropped = A.dsl_base('M0')
    z = np.load(os.path.join(A.XSD, 'late_M0_N100.npz'))
    xe = z['x_end']
    cl = obj.cl
    iu = int(np.argmax(np.where(cl == 1, xe, -1)))
    ifr = int(np.argmax(np.where(cl == 0, xe, -1)))
    arm = cell.arm
    PAY2, VEC2 = UC.tables2(0.0)
    arm2 = MI.Arm(armname)
    arm2.new_cache(22)
    rng = np.random.default_rng(seed)
    p = arm.laws
    PF = UB.PF30
    out = []
    for name, ti in (('U', iu), ('F', ifr)):
        trip = obj.T[ti].astype(np.int64)
        base_code2 = obj.code2[ti]
        cand = []
        for s in range(3):
            for y in cell.supp[s]:
                if p[s][y] <= 0 or y == trip[s]:
                    continue
                t2 = trip.copy(); t2[s] = y
                if obj.index_of(t2[None, :])[1][0] is False:
                    pass
                code2n = UB.codes_of(arm, t2[None, :].astype(np.int16))[0]
                d30 = int(np.rint((PAY2[code2n, s] - PAY2[base_code2, s]) * 30))
                role = 'excluded' if obj.excl[ti] == s else 'pair'
                cand.append((s, int(y), d30, role, float(p[s][y]) / 3.0))
        cand_arr = cand
        by = {}
        for c in cand_arr:
            sign = int(np.sign(c[2]))
            by.setdefault((sign, c[3]), []).append(c)
        for (sg, role), lst in by.items():
            w = np.array([c[4] for c in lst]); pfx = np.array([PF[c[2] + UB.DMAX] for c in lst])
            wsum = w.sum()
            pbar = float((w * pfx).sum() / wsum)
            if pbar < 3e-6:
                out.append(dict(triple=name, sign=sg, role=role, n=0, note='fixation too rare to test', mean_fix=pbar, mass=float(wsum)))
                continue
            k = int(min(max(300, np.ceil(40.0 / pbar)), nmax))
            ids = rng.choice(len(lst), k, p=w / wsum)
            obs = 0; mu = 0.0; var = 0.0
            for i in ids:
                s, y, d30, _, _ = lst[i]
                init = np.zeros((3, UB.KP), np.int64)
                for r in range(3):
                    init[r, trip[r]] = MI.N0
                init[s, trip[s]] -= 1
                init[s, y] += 1
                arm2.maybe_flush(0.45)
                stt, g, counts, na = UC.island_run2(arm2.ctx(), arm2.lc(32), PAY2, init, MI.N0, MI.W, int(rng.integers(1, 2 ** 30)), 20000, np.empty(0), arm2.cum, True)
                tr = MI.triple_of(counts)
                obs += int(tr[s] == y)
                pp = float(PF[d30 + UB.DMAX]); mu += pp; var += pp * (1 - pp)
            zz = (obs - mu) / np.sqrt(var) if var > 0 else float('nan')
            out.append(dict(triple=name, sign=sg, role=role, n=int(k), mu=mu, observed=obs, z=float(zz), mean_fix=pbar, mass=float(wsum),
                            d30_range=[min(c[2] for c in lst), max(c[2] for c in lst)]))
    res = dict(strata=out, passed=bool(all(abs(o['z']) < 3 for o in out if 'z' in o) and sum(1 for o in out if 'z' in o) >= 4))
    save('v4', res)
    return res


if __name__ == '__main__':
    cmd = sys.argv[1]
    t0 = time.time()
    if cmd == 'v1':
        r = v1()
    elif cmd == 'v2':
        r = v2()
    elif cmd == 'v3':
        r = v3(float(sys.argv[2]) if len(sys.argv) > 2 else 10.0, float(sys.argv[3]) if len(sys.argv) > 3 else 100.0)
    elif cmd == 'v4':
        r = v4()
    else:
        raise SystemExit(cmd)
    print(json.dumps(r, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))[:5000])
    print('wall', time.time() - t0)
