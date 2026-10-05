"""Static invasion diagnostics for the prover-carrier seed at b = 0 (specs/2026-10-05-prover-carrier-seed.md).

Type-level payoffs from the b = 0 gate (runs/contracts_types_b0.npz).  Dynamics are the Moran-replicator per generation
with fitness exp(w * payoff): x' = x * F / Fbar, plus mutation x' = (1 - eps) * y + eps * M(y), where a mutated
child's source is a mu-draw and its contract is kept iff valid for the new source (s = 0).

    python3 src/prover_carrier_static.py
Writes runs/prover_carrier_static.json.
"""
import json, os, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import contracts_abm as A
from prover_carrier_seed import establishers

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
W = 0.3
PD = np.array([[-1.0, 1.0], [-2.0, 0.0]])


def setup():
    d = A.data('0')
    val = np.load(os.path.join(RUNS, 'contracts_types_b0.npz'))['val_0'].astype(int)
    U = PD[val, val.T]
    K = d['K']; NT = len(d['tsrc'])
    mu = d['mu'] / d['mu'].sum()
    est = establishers(d)
    return d, val, U, K, NT, mu, est


def step(x, U, eps, mut):
    F = np.exp(W * (U @ x))
    y = x * F / (x @ F)
    if eps > 0:
        y = (1 - eps) * y + eps * mut(y)
    return y


def make_mut(d, mu, NT, K):
    tcon = d['tcon']; tsrc = d['tsrc']; valid = d['valid'].astype(float); NC = d['NC']
    type_of = d['type_of']
    # contract-carrying types: index arrays
    car = np.nonzero(tcon >= 0)[0]
    def mut(y):
        out = np.zeros(NT)
        ycon = np.bincount(tcon[car], weights=y[car], minlength=NC)          # mass per contract
        none_mass = y[:K].sum()
        # kept: (q, c) gets mu_q * ycon[c] if valid
        out[car] += mu[tsrc[car]] * ycon[tcon[car]]
        lost = (1 - valid) @ ycon                                              # per q: mass of contracts invalid for q
        out[:K] += mu * (none_mass + lost)
        return out
    return mut


def flow(x0, U, eps, mut, gens, d, PCCt=None, rec=None):
    x = x0.copy()
    for g in range(gens):
        x = step(x, U, eps, mut)
        if rec is not None and rec(g + 1, x):
            break
    return x, g + 1


def main():
    t0 = time.time()
    d, val, U, K, NT, mu, est = setup()
    nm = d['names']; cn = d['cname']; tsrc = d['tsrc']; tcon = d['tcon']; own = d['own_type']
    iC, iD, iFB = d['iC'], d['iD'], d['iFB']
    mut = make_mut(d, mu, NT, K)
    out = {}
    pe = mu[est] / mu[est].sum()
    ct = own[est]                                   # seeded carrier types
    mixv = np.zeros(NT); mixv[ct] = pe
    fbv = np.zeros(NT); fbv[own[iFB]] = 1.0
    bg_mu = np.zeros(NT); bg_mu[:K] = mu
    # ---------------------------------------------------------------- pairwise matrices
    top = list(np.argsort(-pe)[:10])
    for nmx in ('and(BOX(THEM(ME)),BOXD1(THEM(^D)))', 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))'):
        if nmx in nm and nm.index(nmx) in est:
            j = int(np.nonzero(est == nm.index(nmx))[0][0])
            if j not in top: top.append(j)
    labs = [nm[est[j]] for j in top]
    tt = [int(ct[j]) for j in top]
    out['carrier_action_matrix'] = dict(types=labs, action=val[np.ix_(tt, tt)].tolist(),
                                        note='row carrier action (1 = C) against column carrier; all carriers carry their own signature')
    # whole seeded mixture: mu-weighted mutual cooperation
    mc = (val[np.ix_(ct, ct)] * val[np.ix_(ct, ct)].T)
    out['mix_internal_pcc'] = float(pe @ mc @ pe)
    out['mix_pairs_not_mutual'] = int((mc == 0).sum())
    out['mix_mass_not_mutual'] = float(pe @ (1 - mc) @ pe)
    bad = [(nm[est[a]], nm[est[b]], float(pe[a] * pe[b])) for a, b in zip(*np.nonzero(mc == 0)) if a < b]
    out['mix_not_mutual_top'] = sorted(bad, key=lambda z: -z[2])[:10]
    # against the background
    rows = []
    for j in range(len(est)):
        t = int(ct[j])
        rows.append(dict(source=nm[est[j]], share_of_seed=float(pe[j]),
                         coop_with_bg=float(mu @ val[t, :K]), bg_coop_with_it=float(mu @ val[:K, t]),
                         mutual_with_bg=float(mu @ (val[t, :K] * val[:K, t])),
                         pay_vs_bg=float(mu @ U[t, :K]), pay_vs_C=float(U[t, iC]), pay_vs_D=float(U[t, iD]),
                         pay_vs_FB_noncarrier=float(U[t, iFB]), FB_noncarrier_vs_it=float(U[iFB, t])))
    out['carrier_vs_mu_background'] = sorted(rows, key=lambda r: -r['share_of_seed'])[:14]
    out['bg_mu_pay'] = dict(D=float(mu @ U[iD, :K]), C=float(mu @ U[iC, :K]), FB_noncarrier=float(mu @ U[iFB, :K]),
                            mean=float(mu @ U[:K, :K] @ mu))
    # ---------------------------------------------------------------- backgrounds
    bgs = {}
    bgs['mu'] = bg_mu
    hist = []
    def rec(g, x):
        hist.append((g, float(x[iC]), float(x[iD])))
        return x[iC] < 1e-3
    xA, gA = flow(bg_mu, U, 0.0, mut, 5000, d, rec=rec)
    bgs['post_ALLC'] = xA
    out['allc_below_1e-3_gen'] = gA
    xE, _ = flow(bg_mu, U, 0.0, mut, 3000, d)
    bgs['eps0_endpoint'] = xE
    xM = bg_mu.copy()
    for g in range(20000):
        xn = step(xM, U, 1e-3, mut)
        if np.abs(xn - xM).max() < 1e-13:
            break
        xM = xn
    bgs['eps1e-3_equilibrium'] = xM
    out['backgrounds'] = {}
    for k_, x in bgs.items():
        o = np.argsort(-x[:K])[:6]
        out['backgrounds'][k_] = dict(ALLC=float(x[iC]), D=float(x[iD]), top=[(nm[p], float(x[p])) for p in o],
                                      mean_pay=float(x @ U @ x), pcc=float(x @ (val * val.T) @ x))
    # ---------------------------------------------------------------- rare-carrier growth and f*
    keep = {}
    for c in set(tcon[ct].tolist()):
        keep[c] = float(mu @ d['valid'][:, c])
    def growth(bg, carv, f, eps):
        x = (1 - f) * bg + f * carv
        F = np.exp(W * (U @ x)); Fb = x @ F
        car_idx = np.nonzero(carv)[0]
        Fc = (carv[car_idx] @ F[car_idx])                 # carrier group's mean fitness (composition fixed)
        kp = carv[car_idx] @ np.array([keep.get(int(tcon[t]), 0.0) for t in car_idx])
        bgF = (bg @ F) if bg.sum() > 0 else Fb
        g_sel = Fc / Fb - 1
        g_net = (1 - eps * (1 - kp)) * Fc / Fb - 1
        return g_sel, g_net, Fc / bgF - 1
    out['rare_growth'] = {}
    for k_, bg in bgs.items():
        eps = 1e-3 if k_ == 'eps1e-3_equilibrium' else 0.0
        per = []
        for j in np.argsort(-pe)[:12]:
            v = np.zeros(NT); v[ct[j]] = 1
            gs, gn, gb = growth(bg, v, 1e-3, eps)
            per.append((nm[est[j]], gs, gn))
        gs, gn, gb = growth(bg, mixv, 1e-3, eps)
        gsf, gnf, gbf = growth(bg, fbv, 1e-3, eps)
        out['rare_growth'][k_] = dict(eps=eps, mix_sel=gs, mix_net=gn, fb_sel=gsf, fb_net=gnf, per_type=per,
                                      n_types_positive_sel=int(sum(1 for j in range(len(est)) if growth(bg, np.eye(1, NT, ct[j])[0], 1e-3, eps)[0] > 0)))
    fgrid = np.unique(np.concatenate([np.logspace(-6, np.log10(0.5), 400)]))
    print('rare growth done %.0fs' % (time.time() - t0), flush=True)
    out['fstar'] = {}
    for k_, bg in bgs.items():
        eps = 1e-3 if k_ == 'eps1e-3_equilibrium' else 0.0
        res = {}
        for lab, carv in (('mix', mixv), ('fb', fbv)):
            sel = np.array([growth(bg, carv, f, eps)[2] for f in fgrid])       # carrier fitness vs background mean fitness
            net = np.array([growth(bg, carv, f, eps)[1] for f in fgrid])       # replicator growth incl. mutation loss
            def first_pos(a):
                if a[0] > 0: return 0.0
                h = np.nonzero(a > 0)[0]
                return float(fgrid[h[0]]) if len(h) else None
            res[lab] = dict(fstar_vs_bg_fitness=first_pos(sel), fstar_net_growth=first_pos(net),
                            growth_at=[(float(f), float(net[np.argmin(np.abs(fgrid - f))])) for f in (1e-3, 3e-3, 1e-2, 3e-2, 0.1)])
        out['fstar'][k_] = res
    # ---------------------------------------------------------------- deterministic flow from the seeded state
    f0s = np.array([1e-4, 3e-4, 1e-3, 2e-3, 3e-3, 5e-3, 7e-3, 1e-2, 1.5e-2, 2e-2, 3e-2, 5e-2, 0.1, 0.2])
    PCCm = (val * val.T).astype(float)
    det = {}
    for lab, carv in (('mix', mixv), ('fb', fbv)):
        for eps in (0.0, 1e-3):
            rr = []
            for f0 in f0s:
                x = (1 - f0) * bg_mu + f0 * carv
                mn = (f0, 0)
                traj = []
                for g in range(1, 4001):
                    x = step(x, U, eps, mut)
                    c = x[K:].sum()
                    if c < mn[0]: mn = (c, g)
                    if g in (20, 50, 100, 200, 500, 1000, 2000, 4000): traj.append((g, float(c)))
                rr.append(dict(f0=float(f0), final_carrier=float(x[K:].sum()), final_pcc=float(x @ PCCm @ x), min_carrier=float(mn[0]),
                               min_gen=int(mn[1]), traj=traj))
            thr = [r['f0'] for r in rr if r['final_carrier'] > 0.5]
            det['%s_eps%g' % (lab, eps)] = dict(runs=rr, threshold=min(thr) if thr else None)
            print('flow', lab, eps, det['%s_eps%g' % (lab, eps)]['threshold'], '%.0fs' % (time.time() - t0), flush=True)
    out['deterministic_flow'] = det
    out['establishers'] = dict(n=len(est), mu=float(d['mu'][est].sum() / d['mu'].sum()), n_classes=len(set(d['cls'][est].tolist())))
    out['keep_fraction'] = {cn[c]: v for c, v in sorted(keep.items(), key=lambda kv: -kv[1])[:10]}
    out['keep_fraction_FB'] = keep[int(tcon[own[iFB]])]
    out['time_s'] = time.time() - t0
    json.dump(out, open(os.path.join(RUNS, 'prover_carrier_static.json'), 'w'), indent=1)
    print(json.dumps({k: out[k] for k in ('mix_internal_pcc', 'mix_mass_not_mutual', 'allc_below_1e-3_gen', 'backgrounds', 'fstar')}, indent=1))
    for k_, v in det.items():
        print(k_, 'threshold', v['threshold'], [(r['f0'], round(r['final_carrier'], 3), round(r['min_carrier'], 5), r['min_gen']) for r in v['runs']])
    print('%.0fs' % out['time_s'])


if __name__ == '__main__':
    main()
