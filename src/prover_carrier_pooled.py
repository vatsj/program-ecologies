"""Pooled statistics for the prover-carrier seed runs (success by f0, paired sigma comparison, extinction, lineage,
swap and transition counts).  Prints text; the RESULTS draft quotes it.

    python3 src/prover_carrier_pooled.py
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from prover_carrier_report import wilson

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(ROOT, 'runs', 'prover_carrier_seed_rows.json')))


def ok(r):
    return (r['pcc'] or 0) >= 0.9 if not r['lottery'] else r['outcome'] == 'efficient'


def main():
    print('pooled success by f0')
    for st in ('main', 'twins', 'ctl_inf', 'twins_ctl'):
        for f0 in (0.001, 0.003, 0.01, 0.03, 0.1):
            rs = [r for r in R if r['set'] == st and r['f0'] == f0 and r['b'] == ('inf' if 'ctl' in st else '0') and r['ctl'] == 'on']
            if not rs: continue
            k = sum(ok(r) for r in rs); lo, hi = wilson(k, len(rs))
            sub = {'%s,s%g' % (s, sg): '%d/%d' % (sum(ok(r) for r in rs if r['seed'] == s and r['sigma'] == sg), sum(1 for r in rs if r['seed'] == s and r['sigma'] == sg))
                   for s in ('mix', 'fb') for sg in (0.0, 1.0)}
            print(' ', st, f0, '%d/%d [%.2f, %.2f]' % (k, len(rs), lo, hi), sub)
    for st in ('main', 'twins'):
        for sg in (0.0, 1.0):
            rs = [r for r in R if r['set'] == st and r['sigma'] == sg]
            print(' ', st, 'sigma', sg, '%d/%d' % (sum(ok(r) for r in rs), len(rs)))
        d = {}
        for r in R:
            if r['set'] == st: d.setdefault((r['seed'], r['f0'], r['rep']), {})[r['sigma']] = ok(r)
        print('  paired', st, 'sigma0 only', sum(1 for v in d.values() if v.get(0.0) and not v.get(1.0)),
              'sigma1 only', sum(1 for v in d.values() if v.get(1.0) and not v.get(0.0)),
              'both', sum(1 for v in d.values() if v.get(0.0) and v.get(1.0)), 'pairs', len(d))
    print('extinction and early growth (main)')
    for f0 in (0.001, 0.003, 0.01, 0.03, 0.1):
        rs = [r for r in R if r['set'] == 'main' and r['f0'] == f0]
        ext = [r['carrier_ext_gen'] for r in rs if r['carrier_ext_gen']]
        g = [r['growth_200'] for r in rs if r['growth_200'] is not None and r['carrier_ext_gen'] is None]
        minc = [r['carrier_min_500'] / r['k0'] for r in rs if r['carrier_ext_gen'] is None]
        print('  f0', f0, 'k0', rs[0]['k0'], 'extinct %d/%d' % (len(ext), len(rs)),
              'ext gen median %s max %s' % (np.median(ext) if ext else None, max(ext) if ext else None),
              'survivors: growth200 median %s, min count/k0 in first 500 gens median %s' % (
                  '%.4f' % np.median(g) if g else None, '%.2f' % np.median(minc) if minc else None),
              'unsuccessful survivors', sum(1 for r in rs if r['carrier_ext_gen'] is None and not ok(r)))
    print('lineage (successful runs)')
    for st in ('main', 'twins', 'nsweep', 'nsweep_twins', 'lottery', 'long'):
        for sg in (0.0, 1.0):
            rs = [r for r in R if r['set'] == st and r['sigma'] == sg and ok(r) and 'final_carriers_contract_from_other_lineage' in r and r['ctl'] == 'on' and r['b'] == '0']
            if not rs: continue
            cl = [r['final_carriers_contract_from_other_lineage'] for r in rs]
            fs = [r['final_carriers_from_seed_carrier_founder'] for r in rs]
            fo = [r['final_carriers_founders'] for r in rs]
            print('  %s sigma %g: n %d; cross-lineage contract share median %.3f mean %.3f (>0.05: %d, >0.5: %d, all: %d); from-seed-founder share min %.3f mean %.3f; founders median %g max %d' % (
                st, sg, len(rs), np.median(cl), np.mean(cl), sum(c > 0.05 for c in cl), sum(c > 0.5 for c in cl), sum(c > 0.999 for c in cl),
                min(fs), np.mean(fs), np.median(fo), max(fo)))
    print('swaps (sigma = 1)')
    for st in ('main', 'twins', 'lottery', 'nsweep', 'long'):
        rs = [r for r in R if r['set'] == st and r['sigma'] == 1.0]
        B = sum(r['births'] for r in rs)
        S = {k: sum(r['swaps'][k] for r in rs) for k in rs[0]['swaps']}
        mx = max(rs, key=lambda r: r['swaps']['accepted_onto_none'] / r['births'])
        print('  %s births %.3g accepted %d (%.2g/birth), onto none %d (%.2g/birth), cross-lineage %d, rejected %d (%.2g), same %d, donor none %d; max per-run onto-none %.2g (f0 %g k %s rep %d)' % (
            st, B, S['accepted'], S['accepted'] / B, S['accepted_onto_none'], S['accepted_onto_none'] / B, S['accepted_cross_lineage'], S['rejected'],
            S['rejected'] / B, S['same'], S['donor_none'], mx['swaps']['accepted_onto_none'] / mx['births'], mx['f0'], mx.get('k'), mx['rep']))
    print('transitions (main, successful runs)')
    rs = [r for r in R if r['set'] == 'main' and ok(r)]
    T = {k: sum(r['transitions'][k] for r in rs) for k in rs[0]['transitions']}
    B = sum(r['births'] for r in rs)
    print('  ', T, 'births %.3g' % B, 'kept fraction of carrier mutations %.4f' % (T['kept_valid'] / T['mut_of_carriers']))
    print('composition of successful main runs (mean second-half source shares)')
    acc = {}
    for r in rs:
        for p, v in r['top_sources']: acc[p] = acc.get(p, 0) + v / len(rs)
    print('  ', sorted(((p, round(v, 3)) for p, v in acc.items()), key=lambda kv: -kv[1])[:10])
    acc = {}
    for r in rs:
        for p, v in r['top_contracts']: acc[p] = acc.get(p, 0) + v / len(rs)
    print('  contracts', sorted(((p, round(v, 3)) for p, v in acc.items()), key=lambda kv: -kv[1])[:8])
    print('  src ALLC load %.3f; carrier fraction %.3f' % (np.mean([r['src_allc_load'] for r in rs]), np.mean([r['carrier'] for r in rs])))
    print('lottery placement: k=16 on (100,4) efficient vs islands with a prover-family seed')
    lot = [r for r in R if r['set'] == 'lottery' and r['k'] in (1, 3) and r['I'] == 4]
    print('  (100,4) k=1,3 by outcome, stop gen median', {o: float(np.median([r['stop_gen'] for r in lot if r['outcome'] == o])) for o in ('efficient', 'defecting')})


if __name__ == '__main__':
    main()
