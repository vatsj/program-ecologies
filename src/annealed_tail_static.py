"""Static numbers of the annealed-tail experiment (spec specs/2026-11-01-annealed-tail-dollar3.md): the tail's prior law p per slot,
its mass on the state set of object P, the offering / victim / bully masses, S3 invariance of p.  No ODE is run here.

    python3 src/annealed_tail_static.py            # writes runs/annealed_tail/static.json
"""
import os, sys, json
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import unequal_basin as UB
import unequal_basin_run as R
import unequal_basin_jobs as J

OUT = os.path.join(UB.UC.ROOT, 'runs', 'annealed_tail')
os.makedirs(OUT, exist_ok=True)

FAMS = ['exploiter-fair', 'exploiter', 'yielder', 'fair-reader', 'A1']


def static_dsl(cellname='M0', corelabel='pilot_L'):
    cell = R.cell_of(cellname)
    arm = cell.arm
    isc = cell.isc
    p = arm.laws                                         # (3, KP) the founding prior, the tail's arrival law
    core = J.load_core(corelabel)
    out = dict(cell=cellname, core=corelabel)
    # S3 invariance of p and of the support / core sets (the restricted law is S3-invariant iff the sets are closed)
    pm = UB.perm_maps(arm)
    err_p = 0.0
    closed_supp = True
    closed_core = True
    err_restricted = 0.0
    supp_sets = [set(cell.supp[s]) for s in range(3)]
    for sg, perm in pm:
        for s in range(3):
            for x in range(UB.KP):
                if p[s][x] > 0:
                    err_p = max(err_p, abs(p[s][x] - p[sg[s]][perm[s][x]]))
            for x in cell.supp[s]:
                if perm[s][x] >= 0 and int(perm[s][x]) not in supp_sets[sg[s]]:
                    closed_supp = False
            for x in core[s]:
                if perm[s][x] >= 0 and int(perm[s][x]) not in core[sg[s]]:
                    closed_core = False
    # restricted law (state-set programs of the slot, by indicator), symmetry error to 1e-12
    pr = np.zeros_like(p)
    for s in range(3):
        pr[s][cell.supp[s]] = p[s][cell.supp[s]]
    for sg, perm in pm:
        for s in range(3):
            for x in range(UB.KP):
                if pr[s][x] > 0 and perm[s][x] >= 0:
                    err_restricted = max(err_restricted, abs(pr[s][x] - pr[sg[s]][perm[s][x]]))
    out['S3_error_prior'] = err_p
    out['S3_error_restricted'] = err_restricted
    out['supp_closed'] = closed_supp
    out['core_closed'] = closed_core
    # restricted mass per slot
    cons = np.array([x for x in range(UB.KP) if isc[x]])
    out['mass_constants'] = [float(p[s][cons].sum()) for s in range(3)]
    out['mass_in_supp'] = [float(p[s][cell.supp[s]].sum()) for s in range(3)]
    out['mass_outside_supp'] = [float(1.0 - p[s][cell.supp[s]].sum()) for s in range(3)]
    out['n_cond_in_supp'] = [int(sum(1 for x in cell.supp[s] if not isc[x])) for s in range(3)]
    out['mass_cond_in_supp'] = [float(sum(p[s][x] for x in cell.supp[s] if not isc[x])) for s in range(3)]
    out['mass_cond_in_core'] = [float(sum(p[s][x] for x in core[s])) for s in range(3)]
    out['mass_cond_outside_core_in_supp'] = [out['mass_cond_in_supp'][s] - out['mass_cond_in_core'][s] for s in range(3)]
    out['prior_mass_per_conditional'] = float(p[0][[x for x in range(UB.KP) if not isc[x]][0]])
    out['mass_per_constant'] = float(p[0][cons[0]])
    # constants by action: slot s names (partner, demand)
    acts = {}
    for s in range(3):
        acts[s] = [dict(prog=int(x), name=arm.name_of(s, int(x)), mass=float(p[s][x])) for x in cons]
    out['constants_slot0'] = acts[0]
    # roles, in a U triple (H, Lw, E): the excluded slot E's offering constants name Lw at demand <= 1/2; the victim Lw names H at 1/3
    def named_partner(s, l):
        from dollar3 import partner_abs
        return partner_abs(s, l)
    role = {}
    for s in range(3):
        lst = []
        for x in cons:
            # the constant x of slot s: local action index = its table value; constants are indexed 0..8 = local actions
            l = int(arm.S.fs[x][1][0])
            lst.append((int(x), l, named_partner(s, l), l % 3))
        role[s] = lst
    # per (E, Lw) pair: offering constants of slot E toward Lw (<= 1/2): masses
    off = []
    vic = []
    for E in range(3):
        for Lw in range(3):
            if Lw == E:
                continue
            m_off = sum(p[E][x] for (x, l, pa, d) in role[E] if pa == Lw and d <= 1)
            off.append(dict(E=E, Lw=Lw, mass=float(m_off), n=int(sum(1 for (x, l, pa, d) in role[E] if pa == Lw and d <= 1))))
    for s in range(3):
        m_v = sum(p[s][x] for (x, l, pa, d) in role[s] if pa != 3 and d == 0)
        n_v = sum(1 for (x, l, pa, d) in role[s] if pa != 3 and d == 0)
        vic.append(dict(slot=s, mass=float(m_v), n=int(n_v)))
    # the underpaid member's exit constant: Lw names E at 1/2
    exitc = []
    for Lw in range(3):
        for E in range(3):
            if E == Lw:
                continue
            m_e = sum(p[Lw][x] for (x, l, pa, d) in role[Lw] if pa == E and d == 1)
            exitc.append(dict(Lw=Lw, E=E, mass=float(m_e)))
    out['offering_constants_E_to_Lw'] = off
    out['victim_constants_per_slot'] = vic
    out['exit_constant_Lw_to_E'] = exitc
    fam = {}
    for nm in FAMS:
        m = R.family_mask(arm, nm)
        fam[nm] = dict(n_per_slot=m.sum(axis=1).tolist(), mass=[float(p[s][m[s]].sum()) for s in range(3)],
                       in_core=[int(sum(1 for x in np.nonzero(m[s])[0] if x in core[s])) for s in range(3)],
                       in_supp=[int(sum(1 for x in np.nonzero(m[s])[0] if x in supp_sets[s])) for s in range(3)])
    out['families'] = fam
    # ratios the spec quotes
    bully = fam['exploiter-fair']['mass'][0]
    out['ratio_constant_to_bully'] = out['mass_per_constant'] / bully
    out['ratio_victim_to_bully'] = vic[0]['mass'] / bully
    return out


def static_armT(dose='main'):
    import many_islands_t as M
    T = M.Tabs()
    w = M.seed_law(T, dose)
    out = dict(dose=dose, n_programs=len(w), mass_in_state_set=float(w.sum()), restricted_mass_outside=0.0)
    out['by_family'] = {}
    for f in sorted(set(T.fam)):
        out['by_family'][f] = float(sum(w[i] for i in range(len(w)) if T.fam[i] == f))
    out['names'] = [dict(i=i, name=T.names[i], fam=T.fam[i], mass=float(w[i])) for i in range(len(w))]
    return out


if __name__ == '__main__':
    res = dict(M0=static_dsl('M0'), L0=static_dsl('L0'), armT_main=static_armT('main'), armT_0=static_armT('0'))
    json.dump(res, open(os.path.join(OUT, 'static.json'), 'w'), indent=1)
    m = res['M0']
    print('prior mass: constants %.4f, conditionals in supp %.5f (%d), in core %.6f, outside supp %.2e' % (
        m['mass_constants'][0], m['mass_cond_in_supp'][0], m['n_cond_in_supp'][0], m['mass_cond_in_core'][0], m['mass_outside_supp'][0]))
    print('S3 error prior %.2e restricted %.2e supp closed %s core closed %s' % (m['S3_error_prior'], m['S3_error_restricted'], m['supp_closed'], m['core_closed']))
    print('per constant %.5f; bully family %.3e; ratio const:bully %.0f; victims per slot %s' % (
        m['mass_per_constant'], m['families']['exploiter-fair']['mass'][0], m['ratio_constant_to_bully'], m['victim_constants_per_slot'][0]))
    print('offering (E=0, Lw=1) %s' % [o for o in m['offering_constants_E_to_Lw'] if o['E'] == 0 and o['Lw'] == 1])
    print('exit constant (Lw=1, E=0) %s' % [o for o in m['exit_constant_Lw_to_E'] if o['E'] == 0 and o['Lw'] == 1])
    print('families', {k: v['mass'][0] for k, v in m['families'].items()})
    print('L0 mass in supp', res['L0']['mass_in_supp'], 'cond in core', res['L0']['mass_cond_in_core'])
