"""E3: finite-eps N agent-based runs of the modal arm (n = 6) vs the weak arm,
on one big island (no spatial structure) and on 64 islands with and without
payoff-weighted emigration.  A generation is I*N births; statistics over the
second half of each run; P(C,C) is interaction-weighted within islands and
averaged over islands.  Finite eps N: approach rates, not pi.

    python3 src/modal_abm.py
Writes runs/modal_abm.md/json.
"""
import json, os, sys
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from islands import run_one, _load, ROOT

CONFIGS = [  # (label, I, N, mN, seeding, epsN per island, wg)
    ('big island, eps 1e-3', 1, 6400, 0.0, 'alld', 6.4, 0.0),
    ('big island, eps 1e-3, cooperative start', 1, 6400, 0.0, 'allR', 6.4, 0.0),
    ('big island, eps 1e-4', 1, 6400, 0.0, 'alld', 0.64, 0.0),
    ('64 islands, w_g 0', 64, 100, 1.0, 'alld', 0.1, 0.0),
    ('64 islands, w_g 10', 64, 100, 1.0, 'alld', 0.1, 10.0),
]


def main(reps=3, gens=200000):
    jobs = [(arm, False, 'complete', mN, seed, r, I, N, 0.3, gens, 20, epsN, wg, label)
            for arm in ('modal6', 'pd') for (label, I, N, mN, seed, epsN, wg) in CONFIGS for r in range(reps)]
    for arm in ('modal6', 'pd'): _load(arm, False)
    out = []
    with Pool(6) as pool:
        for o in pool.imap_unordered(_one, jobs):
            out.append(o)
            print(o['arm'], o['label'], o['rep'], 'P(C,C) %.3f R %.3f ALLC %.3f' % (o['pcc_2nd'], o['R_2nd'], o['C_2nd']), flush=True)
            json.dump(out, open(os.path.join(ROOT, 'runs', 'modal_abm.json'), 'w'), indent=1)
    L = ['# E3: finite-eps N agent-based runs, modal arm (n = 6) vs weak arm (L_6 with X, ROLE); PD, w = 0.3, %d generations, second half' % gens, '',
         'R = the arm\'s reciprocator (modal: FairBot BOX(THEM(ME)); weak: THEM(^C)). Cooperative phases = samples with island-mean P(C,C) > 0.5.', '',
         '| arm | configuration | P(C,C) per replicate | mean | R share | ALLC share of population | ALLC share of population during cooperative phases |', '|---|---|---|---|---|---|---|']
    for arm in ('modal6', 'pd'):
        for (label, *_r) in CONFIGS:
            s = [o for o in out if o['arm'] == arm and o['label'] == label]
            L.append('| %s | %s | %s | %.3f | %.3f | %.3f | %s |' % ('modal n=6' if arm == 'modal6' else 'weak L_6', label,
                     ', '.join('%.2f' % o['pcc_2nd'] for o in s), np.mean([o['pcc_2nd'] for o in s]),
                     np.mean([o['R_2nd'] for o in s]), np.mean([o['C_2nd'] for o in s]),
                     '%.3f' % np.nanmean([o['allc_coop'] for o in s])))
    open(os.path.join(ROOT, 'runs', 'modal_abm.md'), 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))


def _one(job):
    *j, label = job
    r = run_one(tuple(j))
    cc, C = np.array(r['trace_cc']), np.array(r['trace_C'])
    h = len(cc) // 2; m = cc[h:] > 0.5
    r['allc_coop'] = float(C[h:][m].mean()) if m.any() else float('nan')
    for k in ('trace_pay', 'trans', 'spread_pay_pairs', 'isl_cc_hist', 'isl_dwl_hist'):
        r.pop(k, None)
    r['arm'] = j[0]; r['label'] = label
    return r


if __name__ == '__main__':
    main()
