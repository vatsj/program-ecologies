"""Analysis of an endpoint state saved by unequal_basin_run (spec Questions 3 and 4): program-by-role association, the rescue
move table at the dominant unequal triples, the U -> V* flux decomposition, the three Jacobian spectra, the leak and the
blocked (truncation) flux, rare-class growth.

    python3 src/unequal_basin_endpoint.py ROWKEY            # writes runs/unequal_basin/endpoint-<ROWKEY>.json
"""
import os, sys, json, time
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dollar3 as D
import many_islands as MI
import unequal_basin as UB
import unequal_basin_run as R
import unequal_basin_jobs as J
import unequal_basin_analysis as A
import unequal_basin_jac as JAC


def load_row(key):
    row = json.load(open(os.path.join(R.ROWS, key + '.json')))
    x = np.load(os.path.join(R.XS, key + '.npz'))['x']
    spec = row['spec']
    arm = UB.get_arm(R.CELLS[spec['cell']]['arm'])
    remove = J.resolve_abl(spec.get('abl'), arm)
    core = J.load_core(spec.get('core'))
    cell, obj, xn, dropped = R.build_obj_start(spec, remove, spec.get('rule', 'reassign'), None, core)
    return row, obj, x


def action_names(obj, code):
    v = [code // 81, (code // 9) % 9, code % 9]
    return [D.act_name(s, v[s]) for s in range(3)]


def rescue_table(obj, x, ntop=4):
    """for the dominant unequal states: all moves into a fair pair (any migrant), with payoff change, P_fix, donor mass and
    flux; plus the constants' canonical rescue moves with the action table of the would-be state and the blocker."""
    q = obj.marg(x)
    r = A.roles(obj)
    out = []
    for t in A.dominant_triples(obj, x, 1, ntop):
        T = obj.T[t].astype(np.int64)
        excl = int(obj.excl[t])
        hi = [s for s in range(3) if r[s, t] == 0][0]
        lo = [s for s in range(3) if r[s, t] == 1][0]
        entry = dict(state=[obj.arm.name_of(s, int(T[s])) for s in range(3)], mass=float(x[t]), roles=dict(high=hi, low=lo, excl=excl),
                     actions=action_names(obj, int(obj.code[t])), payoffs=[(int(obj.lev[s, t]) - 3) / 30.0 for s in range(3)])
        mv = A.moves_from(obj, x, t, q)
        tof = [m for m in mv if m['new_cl'] == 0]
        tof.sort(key=lambda m: -m['flux'])
        for m in tof:
            m['prog_name'] = obj.arm.name_of(m['slot'], m['prog'])
        entry['moves_to_fair'] = tof[:12]
        entry['n_moves_to_fair'] = len(tof)
        entry['flux_to_fair'] = float(sum(m['flux'] for m in tof))
        entry['flux_total_out'] = float(sum(m['flux'] for m in mv))
        # canonical rescues with constants: low switches to a constant naming E at demand 1/2 (or 1/3); E switches to a constant
        # naming low at 1/2 (neutral move that enables the first)
        can = []
        cons = [y for y in obj.supp[0] if obj.isc[y]]
        for s, who in ((lo, 'low switches'), (excl, 'excluded switches'), (hi, 'high concedes')):
            for y in obj.supp[s]:
                if not obj.isc[y]:
                    continue
                T2 = T.copy(); T2[s] = y
                p, ok = obj.index_of(T2[None, :])
                if not ok[0]:
                    continue
                p = int(p[0])
                d = int(obj.lev[s, p]) - int(obj.lev[s, t])
                # only moves that would be rescue-like: the mover names a slot (not ALL) at 1/3..1/2 or changes class to F
                nm = obj.arm.name_of(s, int(y))
                can.append(dict(who=who, slot=s, prog=int(y), name=nm, dl=d, pfix=float(UB.PF30[d + UB.DMAX]), q=float(q[s, y]),
                                new_cl=UB.CLS[int(obj.cl[p])], actions=action_names(obj, int(obj.code[p])), fixes_to_fair=bool(obj.cl[p] == 0)))
        entry['constant_moves'] = [c for c in can if c['q'] > 1e-9 and c['dl'] >= -5][:40]
        out.append(entry)
    return out


def analyze(key, thr=1e-9, ntop=3, jac=True):
    t0 = time.time()
    row, obj, x = load_row(key)
    res = dict(key=key, spec=row['spec'], states=obj.n, endpoint=row.get('endpoint'), t_end=row.get('t_end'))
    sh, pairs = obj.class_shares(x, True)
    res['shares'] = sh.tolist()
    res['pairs'] = pairs.tolist()
    top, nclass = A.top_classes(obj, x, 0, 1e-3, 20)
    res['top_classes_slot0'] = top
    res['n_classes_ge_1e-3'] = nclass
    res['rescue'] = rescue_table(obj, x, ntop)
    F = A.flux_decomposition(obj, x, (1,), (0,))
    res['flux_U_to_F'] = dict(total=float(F.sum()), by_role=dict(zip(A.ROLE, F.sum(axis=1).tolist())),
                              top=[(int(y), obj.arm.name_of(0, int(y)), [float(F[k, y]) for k in range(3)]) for y in np.argsort(-F[:3].sum(axis=0))[:10]])
    Fb = A.flux_decomposition(obj, x, (0,), (1,))
    res['flux_F_to_U'] = dict(total=float(Fb.sum()), by_role=dict(zip(['high-of-dst?'] + A.ROLE[1:], Fb.sum(axis=1).tolist())),
                              top=[(int(y), obj.arm.name_of(0, int(y)), float(Fb[:, y].sum())) for y in np.argsort(-Fb.sum(axis=0))[:10]])
    res['class_flux'] = A.class_flux_matrix(obj, x).tolist()
    b, real, per = UB.blocked_flux(obj, x, 1e-14)
    res['blocked_flux'] = dict(blocked=b, realized=real, fraction=b / (b + real) if b + real > 0 else 0.0)
    if jac:
        idx = JAC.support_idx(obj, x, thr)
        res['support_states'] = int(len(idx))
        res['leak'] = dict(zip(['into_absent', 'support_exit'], JAC.leak_rate(obj, x, idx)))
        res['jacobian'] = {}
        for mode in ('invariant', 'transverse', 'full'):
            o_, n = JAC.leading(obj, x, idx, mode, k=12)
            res['jacobian'][mode] = o_
        # full-space Arnoldi (rare present classes, including the complement block)
        try:
            from scipy.sparse.linalg import LinearOperator, eigs
            q = obj.marg(x)
            op = LinearOperator((obj.n, obj.n), matvec=lambda v: UB.jvp(obj, x, v, q, sym=False), dtype=np.float64)
            ev = eigs(op, k=8, which='LR', tol=1e-6, maxiter=500, return_eigenvectors=False)
            res['jacobian']['full_space_leading_re'] = sorted([float(v.real) for v in ev], reverse=True)
        except Exception as e:
            res['jacobian']['full_space_leading_re'] = 'failed: %s' % e
    res['diag'] = row.get('diag')
    res['wall'] = time.time() - t0
    with open(os.path.join(UBOUT, 'endpoint-%s.json' % key), 'w') as f:
        json.dump(res, f, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    return res


UBOUT = os.path.join(R.UC.OUTD)

if __name__ == '__main__':
    r = analyze(sys.argv[1])
    print(json.dumps({k: r[k] for k in ('key', 'shares', 'flux_U_to_F', 'blocked_flux', 'leak') if k in r}, indent=1, default=str)[:3000])
