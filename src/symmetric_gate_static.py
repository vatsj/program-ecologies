"""Static diagnostics for the symmetric gate on identical frozen backgrounds (specs/2026-10-05-symmetric-gate.md).

Backgrounds are non-carrier states (the non-carrier block is rule-independent at b = 0, checked): mu; the eps = 0
non-carrier flow when ALLC first falls below 1e-3 ('post_scramble'); the eps = 1e-3 non-carrier equilibrium.  For each
access rule: block action/payoff tables (carrier-carrier, carrier->background, background->carrier, background-
background) for the mix carrier group, rare-carrier growth at f = 1e-3 (as src/prover_carrier_static.py), f*, the
deterministic flow threshold, and the fringe-to-D intervention on the asymmetric table holding every other action and
the composition fixed.

    python3 src/symmetric_gate_static.py      # writes runs/symmetric_gate_static.json
"""
import json, os, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import contracts_abm as A
import symmetric_gate as SG
from prover_carrier_seed import establishers
from prover_carrier_static import make_mut

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
W = 0.3
PD = np.array([[-1.0, 1.0], [-2.0, 0.0]])


def tables(rules_q=(0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9)):
    z = np.load(SG.TYPES)
    V = {r: z['val_0_' + r].astype(int) for r in SG.RULES}
    V['inf_asym'] = z['val_inf_asym'].astype(int); V['inf_sym'] = z['val_inf_sym'].astype(int)
    C = SG.setup()
    for q in rules_q:
        V['q%g' % q] = SG.evaluate(C, 0, 'q%g' % q)[0].astype(int)
    return V, C


def data_from_val(val, base):
    """A contracts_abm.data dict with the payoff tables rebuilt from val (same class construction)."""
    U = PD[val.astype(int), val.T.astype(int)]
    key = {}; pc = np.zeros(len(U), np.int64)
    for t in range(len(U)):
        pc[t] = key.setdefault((U[t].tobytes(), U[:, t].tobytes()), len(key))
    NP = len(key)
    rep = np.zeros(NP, np.int64)
    for t in range(len(U) - 1, -1, -1):
        rep[pc[t]] = t
    d = dict(base)
    d.update(pc=pc, NP=NP, U=np.ascontiguousarray(U[np.ix_(rep, rep)]),
             PCC=np.ascontiguousarray((val * val.T)[np.ix_(rep, rep)].astype(np.float64)))
    return d


def main():
    t0 = time.time()
    V, C = tables()
    d = A.data('0')
    K = d['K']; NT = len(d['tsrc']); tsrc = d['tsrc']; tcon = d['tcon']; own = d['own_type']; nm = d['names']
    mu = d['mu'] / d['mu'].sum()
    iC, iD, iFB = d['iC'], d['iD'], d['iFB']
    est = establishers(d)
    pe = mu[est] / mu[est].sum()
    ct = own[est]
    mixv = np.zeros(NT); mixv[ct] = pe
    fbv = np.zeros(NT); fbv[own[iFB]] = 1.0
    car = tcon >= 0
    out = dict(time_note='static, b = 0, n = 8, PD, w = 0.3')
    # ---------------------------------------------------------------- where the rules differ
    a = V['asym']
    out['changed_entries'] = {}
    for r in ('sym', 'q0.5', 'q0.25', 'inf_sym'):
        ref = V['inf_asym'] if r.startswith('inf') else a
        D = ref != V[r]
        out['changed_entries'][r] = dict(total=int(D.sum()), carrier_carrier=int(D[np.ix_(car, car)].sum()),
                                         carrier_to_nc=int(D[np.ix_(car, ~car)].sum()), nc_to_carrier=int(D[np.ix_(~car, car)].sum()),
                                         nc_nc=int(D[np.ix_(~car, ~car)].sum()),
                                         nc_to_carrier_C_to_D=int(((ref == 1) & (V[r] == 0))[np.ix_(~car, car)].sum()),
                                         nc_to_carrier_D_to_C=int(((ref == 0) & (V[r] == 1))[np.ix_(~car, car)].sum()))
    # b = inf baseline: payoff-table equality
    Ua = PD[V['inf_asym'], V['inf_asym'].T]; Us = PD[V['inf_sym'], V['inf_sym'].T]
    Dinf = (Ua != Us)
    out['b_inf_baseline'] = dict(exact_equal=bool(not Dinf.any()), payoff_entries_differing=int(Dinf.sum()),
                                 mu_mass_nc_vs_own_carriers=float(mu @ (V['inf_asym'] != V['inf_sym'])[np.ix_(np.arange(K), own)] @ mu),
                                 mu_mass_own_carriers_vs_nc=float(mu @ (V['inf_asym'] != V['inf_sym'])[np.ix_(own, np.arange(K))] @ mu),
                                 mix_vs_mu_payoff_asym=float(mixv @ Ua[:, :K] @ mu), mix_vs_mu_payoff_sym=float(mixv @ Us[:, :K] @ mu),
                                 mu_vs_mix_payoff_asym=float(mu @ Ua[:K] @ mixv), mu_vs_mix_payoff_sym=float(mu @ Us[:K] @ mixv),
                                 top_readers_differing=[(nm[p], float(mu[p])) for p in sorted(set(np.nonzero((V['inf_asym'] != V['inf_sym'])[:K][:, own].any(1))[0].tolist()), key=lambda p: -mu[p])[:10]])
    # ---------------------------------------------------------------- frozen backgrounds (rule-independent nc block)
    for r in SG.RULES:
        assert (V[r][:K, :K] == a[:K, :K]).all()
    Ua0 = PD[a, a.T]
    mut = make_mut(d, mu, NT, K)
    def step(x, U, eps):
        F = np.exp(W * (U @ x)); y = x * F / (x @ F)
        return (1 - eps) * y + eps * mut(y) if eps > 0 else y
    bgs = {'mu': np.concatenate([mu, np.zeros(NT - K)])}
    x = bgs['mu'].copy()
    for g in range(1, 5001):
        x = step(x, Ua0, 0.0)
        if x[iC] < 1e-3:
            break
    bgs['post_scramble'] = x; out['allc_below_1e-3_gen'] = g
    x = bgs['mu'].copy()
    for g in range(20000):
        xn = step(x, Ua0, 1e-3)
        if np.abs(xn - x).max() < 1e-13: break
        x = xn
    bgs['eps_equilibrium'] = x
    out['backgrounds'] = {k: dict(ALLC=float(x[iC]), D=float(x[iD]), top=[(nm[p], float(x[p])) for p in np.argsort(-x[:K])[:8]],
                                  carriers=float(x[K:].sum())) for k, x in bgs.items()}
    keep = {c: float(mu @ d['valid'][:, c]) for c in set(tcon[ct].tolist())}
    kp_mix = float(pe @ np.array([keep[int(tcon[t])] for t in ct]))
    # ---------------------------------------------------------------- fringe and the intervention tables
    s = V['sym']
    ncm = np.zeros((NT, NT), bool); ncm[np.ix_(~car, car)] = True
    fr = ncm & (a == 1) & (s == 0) & (a.T == 0)                  # fringe pairs: nc t cooperates with carrier u only by reading, u defects on t
    lost_mutual = ncm & (a == 1) & (s == 0) & (a.T == 1)         # mutual cooperation lost
    flip_dc = ncm & (a == 0) & (s == 1)                           # cooperates under illegibility, defected on reading the contract
    assert ((a != s) == (fr | lost_mutual | flip_dc)).all()
    Vint = {'asym': a}
    v1 = a.copy(); v1[fr] = 0; Vint['fringe_to_D'] = v1
    v2 = v1.copy(); v2[lost_mutual] = 0; Vint['fringe+mutual_lost_to_D'] = v2
    v3 = v2.copy(); v3[flip_dc] = 1; Vint['all_changes(=sym)'] = v3
    assert (v3 == s).all()
    # fringe mass against the mix carrier group, per background
    out['fringe'] = {}
    for k, bg in bgs.items():
        fm = (fr[:K][:, ct] * pe[None, :]).sum(1)                   # per nc source: share of mix carriers it is a fringe member against
        lm = (lost_mutual[:K][:, ct] * pe[None, :]).sum(1)
        dm = (flip_dc[:K][:, ct] * pe[None, :]).sum(1)
        out['fringe'][k] = dict(mass=float(bg[:K] @ (fm > 0)), weighted_mass=float(bg[:K] @ fm),
                                mutual_lost_weighted=float(bg[:K] @ lm), flip_DC_weighted=float(bg[:K] @ dm),
                                top=[(nm[p], float(bg[p]), float(fm[p])) for p in np.argsort(-(bg[:K] * fm))[:8] if bg[p] * fm[p] > 0],
                                top_flip_DC=[(nm[p], float(bg[p]), float(dm[p])) for p in np.argsort(-(bg[:K] * dm))[:6] if bg[p] * dm[p] > 0])
    # q coverage of the fringe mass
    out['q_fringe_coverage'] = {}
    for q in (0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
        r = SG.reads_assignment(K, q)
        cov = {}
        for k, bg in bgs.items():
            fm = (fr[:K][:, ct] * pe[None, :]).sum(1) * bg[:K]
            cov[k] = float(fm[r].sum() / fm.sum()) if fm.sum() > 0 else None
        out['q_fringe_coverage']['%g' % q] = dict(n_readers=int(r.sum()), mu_readers=float(mu[r].sum()), fringe_mass_covered=cov)
    # ---------------------------------------------------------------- block tables and growth
    def block(val, bg, carv):
        U = PD[val, val.T]
        bgn = bg / bg.sum()
        return dict(cc_action=float(carv @ val @ carv), cc_pay=float(carv @ U @ carv),
                    car_to_bg_action=float(carv @ val @ bgn), car_vs_bg_pay=float(carv @ U @ bgn),
                    bg_to_car_action=float(bgn @ val @ carv), bg_vs_car_pay=float(bgn @ U @ carv),
                    bg_bg_action=float(bgn @ val @ bgn), bg_bg_pay=float(bgn @ U @ bgn),
                    D_vs_car_pay=float(U[iD] @ carv), D_vs_bg_pay=float(U[iD] @ bgn))
    _U = {}
    def growth(val, bg, carv, f, eps):
        if id(val) not in _U: _U[id(val)] = (val, PD[val, val.T])
        U = _U[id(val)][1]
        x = (1 - f) * bg + f * carv
        F = np.exp(W * (U @ x)); Fb = x @ F
        Fc = carv @ F
        kp = kp_mix if carv is mixv else keep[int(tcon[own[iFB]])]
        return dict(sel=float(Fc / Fb - 1), net=float((1 - eps * (1 - kp)) * Fc / Fb - 1), vs_bg=float(Fc / (bg @ F / bg.sum()) - 1))
    fgrid = np.logspace(-6, np.log10(0.5), 300)
    allv = dict(V); allv.update({'int_' + k: v for k, v in Vint.items()})
    order = ['asym', 'q0.9', 'q0.8', 'q0.7', 'q0.6', 'q0.5', 'q0.4', 'q0.3', 'q0.25', 'q0.2', 'q0.1', 'sym',
             'int_fringe_to_D', 'int_fringe+mutual_lost_to_D']
    out['blocks'] = {}; out['growth'] = {}; out['fstar'] = {}
    for k, bg in bgs.items():
        eps = 1e-3 if k == 'eps_equilibrium' else 0.0
        out['blocks'][k] = {r: block(allv[r], bg, mixv) for r in ('asym', 'q0.5', 'q0.25', 'sym', 'int_fringe_to_D')}
        out['growth'][k] = {}
        out['fstar'][k] = {}
        for r in order:
            g = dict(mix=growth(allv[r], bg, mixv, 1e-3, eps), fb=growth(allv[r], bg, fbv, 1e-3, eps))
            out['growth'][k][r] = g
            gg = [growth(allv[r], bg, mixv, f, eps) for f in fgrid]
            sel = np.array([q['vs_bg'] for q in gg]); net = np.array([q['net'] for q in gg])
            def first_pos(arr):
                h = np.nonzero(arr > 0)[0]
                return 0.0 if len(h) and h[0] == 0 else (float(fgrid[h[0]]) if len(h) else None)
            out['fstar'][k][r] = dict(fstar_vs_bg=first_pos(sel), fstar_net=first_pos(net),
                                      net_at={'%g' % f: float(net[np.argmin(np.abs(fgrid - f))]) for f in (1e-3, 3e-3, 1e-2, 3e-2, 0.1)})
        print(k, {r: round(out['growth'][k][r]['mix']['net'], 5) for r in order}, '%.0fs' % (time.time() - t0), flush=True)
    # linear-advantage check: sym growth minus its f -> 0 limit, per unit f
    # ---------------------------------------------------------------- deterministic flow from the seeded state
    PCCm = {}
    det = {}
    f0s = np.array([1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.2])
    for r in ('asym', 'sym', 'q0.5', 'q0.25'):
        U = PD[V[r], V[r].T]
        for eps in (0.0, 1e-3):
            rr = []
            for f0 in f0s:
                x = (1 - f0) * bgs['mu'] + f0 * mixv
                mn = (f0, 0); traj = []
                for g in range(1, 4001):
                    x = step(x, U, eps)
                    c = x[K:].sum()
                    if c < mn[0]: mn = (c, g)
                    if g in (20, 50, 100, 200, 500, 1000, 2000, 4000): traj.append((g, float(c)))
                rr.append(dict(f0=float(f0), final_carrier=float(x[K:].sum()), min_carrier=float(mn[0]), min_gen=int(mn[1]), traj=traj))
            thr = [q['f0'] for q in rr if q['final_carrier'] > 0.5]
            det['%s_eps%g' % (r, eps)] = dict(runs=rr, threshold=min(thr) if thr else None)
            print('flow', r, eps, det['%s_eps%g' % (r, eps)]['threshold'], [(q['f0'], round(q['final_carrier'], 3), round(q['min_carrier'] / q['f0'], 3), q['min_gen']) for q in rr],
                  '%.0fs' % (time.time() - t0), flush=True)
    out['deterministic_flow'] = det
    out['kp_mix'] = kp_mix
    out['time_s'] = time.time() - t0
    json.dump(out, open(os.path.join(RUNS, 'symmetric_gate_static.json'), 'w'), indent=1)
    print(json.dumps({k: out[k] for k in ('changed_entries', 'b_inf_baseline', 'allc_below_1e-3_gen', 'fringe', 'q_fringe_coverage')}, indent=1))
    for k in bgs:
        print('BLOCKS', k, json.dumps(out['blocks'][k]))
        print('FSTAR', k, json.dumps(out['fstar'][k]))


if __name__ == '__main__':
    main()
