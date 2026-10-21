"""Driver for the core-rediscovery run (spec specs/2026-10-21-core-rediscovery.md).

    python3 src/core_auction_run.py statics                       # Part A: pure Nash equilibria, core checks, Vickrey-nearest baselines
    python3 src/core_auction_run.py cells --cells NAME ... [--runs 40] [--workers 1]
Outputs go to runs/core_auction/.
"""
import argparse, gzip, json, os, sys, time, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core_auction as C

OUT = C.OUT
os.makedirs(OUT, exist_ok=True)
SPACES = ('unrestricted', 'no-overbid')


def log(*a):
    print(*a, flush=True)


def statics():
    res = dict(instances=C.INSTANCES, nash={}, baselines={}, hand={})
    for inst, v in C.INSTANCES.items():
        res['hand'][inst] = dict(v=v, min_revenue=C.min_revenue(v), wstar=C.wstar(v),
                                 core_bounds={''.join(C.ROLES[i] for i in S): b for S, b in C.core_inequalities(v).items()},
                                 vcg=C.vcg_payments(v), vickrey_nearest=C.vickrey_nearest(v))
        for space in SPACES:
            rep = C.nash_report(inst, space)
            summ = C.summarize_nash(rep)
            tally = {}
            rows_out = []
            for r in rep['rows']:
                viol = C.core_violations(v, r['u'], r['rev'])
                for x in viol:
                    tally[x] = tally.get(x, 0) + 1
                rows_out.append([*r['bids'], *[round(x, 3) for x in r['u']], round(r['rev'], 3), round(r['eff'], 3), round(r['core'], 3),
                                 int(r['mean_core']), ' '.join(viol)])
            summ['violation_tally'] = tally
            vn = C.vickrey_nearest(v)
            if 'A' in vn:
                near = 0; edge = 0
                for r in rep['rows']:
                    if r['eff'] > 1 - 1e-9 and r['mean_core'] and r['rev'] <= C.min_revenue(v) + 1 + 1e-9:
                        edge += 1
                        pa = v[1] - r['u'][1]; pb = v[2] - r['u'][2]
                        if abs(pa - vn['A']) <= 1 + 1e-9 and abs(pb - vn['B']) <= 1 + 1e-9:
                            near += 1
                summ['edge_equilibria_in_core'] = edge; summ['edge_equilibria_within_one_tick_of_VN'] = near
            res['nash']['%s/%s' % (inst, space)] = summ
            with gzip.open(os.path.join(OUT, 'nash_%s_%s.csv.gz' % (inst, space)), 'wt') as f:
                w = csv.writer(f)
                w.writerow(['bP', 'bA', 'bB', 'uP', 'uA', 'uB', 'rev', 'eff', 'core_realized', 'core_mean', 'violations'])
                w.writerows(rows_out)
            log(inst, space, {k: summ[k] for k in ('n_nash', 'n_efficient', 'n_in_core_mean', 'revenue_min', 'revenue_max',
                                                    'n_efficient_below_core', 'n_efficient_above_min_plus2')})
        for space in SPACES:
            b = C.edge_baseline(inst, space)
            b.pop('edge', None)
            res['baselines']['%s/%s' % (inst, space)] = b
    json.dump(res, open(os.path.join(OUT, 'statics.json'), 'w'), indent=1, default=str)
    return res


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    a = ap.parse_args()
    if a.cmd == 'statics':
        statics()
