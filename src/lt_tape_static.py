"""STATIC checks (exact tables) for the private-tape experiment: predictions 1 (b, c), 5, S2, S3 and the route ranking of prediction 6."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lt_tape_run as RUN
import lt_tape_games as G


def static_checks():
    out = {}
    tbi = RUN.Tables('insp', 'full', RUN.K0, 0.0)
    tbr = RUN.Tables('rps', 'full', RUN.K0, 0.0)
    n0, n1 = tbi.names
    I0 = {n: i for i, n in enumerate(n0)}; I1 = {n: i for i, n in enumerate(n1)}
    nr = tbr.names[0]; R_ = {n: i for i, n in enumerate(nr)}
    Ug = tbr.Ug
    out['sim100_vs_hash'] = {s + '_vs_' + h: float(Ug[R_[s], R_[h]]) for s in ('SIM100R', 'SIM100P', 'SIM100S', 'SIM100u') for h in ('H0', 'H1', 'H2')}
    out['sim100_vs_U'] = {s: float(Ug[R_[s], R_['U']]) for s in ('SIM100R', 'SIM100P', 'SIM100S', 'SIM100u')}
    out['U_row_max_abs'] = float(np.abs(Ug[R_['U']]).max())
    out['sim100_vs_B'] = {b: float(Ug[R_['SIM100R'], R_[b]]) for b in nr if b.startswith('B_')}
    out['best_response_to_B'] = {b: float(max(Ug[R_[a], R_[b]] for a in ('R0', 'P0', 'S0'))) for b in nr if b.startswith('B_')}
    out['sim20_vs_hash'] = {'SIM20R_vs_' + h: float(Ug[R_['SIM20R'], R_[h]]) for h in ('H0', 'H1', 'H2')}
    out['PRR_vs_B'] = {b: float(Ug[R_['PRR'], R_[b]]) for b in nr if b.startswith('B_')}
    out['PRR_vs_U'] = float(Ug[R_['PRR'], R_['U']])
    out['CRR_vs_CB'] = {b: float(Ug[R_['CRR'], R_[b]]) for b in nr if b.startswith('CB_')}
    out['CRR_vs_B'] = {b: float(Ug[R_['CRR'], R_[b]]) for b in nr if b.startswith('B_')}
    S1 = tbi.S1; S0 = tbi.S0
    out['steps_RI_vs_C0'] = float(S0[I0['RI'], I1['C0']])
    out['steps_CR3_vs_CARR3'] = float(S1[I1['CR3'], I0['CARR3']])
    out['hand_ratio_check_over_proof'] = 27 / 12
    out['measured_static_ratio'] = out['steps_CR3_vs_CARR3'] / out['steps_RI_vs_C0']
    out['route_table'] = {}
    for j in (2, 3, 4, 6):
        out['route_table']['CARR%d' % j] = dict(PR=float(S1[I1['PR3'], I0['CARR%d' % j]]), CR=float(S1[I1['CR3'], I0['CARR%d' % j]]),
                                                 PR_plain=float(S1[I1['PR3'], I0['M%d' % j]]))
    out['CR_on_plain_steps'] = float(S1[I1['CR3'], I0['M3']])
    th = tbi.prover.th
    W = {}
    for b_, y in zip(n1, tbi.terms[1]):
        q = tbi.prover.query(th.plays(y, tbi.terms[0][I0['RI']], 'C'), 8)
        W[b_] = (int(q['W']), bool(q['found']), bool(q['complete']))
    out['RI_W'] = W
    refuted = [w for (w, f, c) in W.values() if (not f) and c]
    out['RI_refuted_W_min'] = min(refuted) if refuted else None
    p0 = G.prior_masses(tbi.sizes[0]); p1 = G.prior_masses(tbi.sizes[1])
    route_cost = {}
    for name in n1: route_cost[name] = float(S1[I1[name]] @ p0)
    for name in n0: route_cost[name] = float(S0[I0[name]] @ p1)
    out['mean_steps_vs_prior'] = route_cost
    return out


if __name__ == '__main__':
    import json
    r = static_checks()
    print(json.dumps(r, indent=1)[:4000])
