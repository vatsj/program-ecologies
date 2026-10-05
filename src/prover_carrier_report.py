"""Tables for the prover-carrier seed runs: runs/prover-carrier-seed.json (cell summaries) and the tables part of
runs/prover-carrier-seed.md (verdicts are appended by hand below the generated block).

    python3 src/prover_carrier_report.py
"""
import json, os, sys
import numpy as np
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def ci(k, n):
    lo, hi = wilson(k, n)
    return '%d/%d [%.2f, %.2f]' % (k, n, lo, hi)


def med(a):
    a = [x for x in a if x is not None]
    return float(np.median(a)) if a else None


def finite_summary(rs):
    n = len(rs)
    pc = np.array([r['pcc'] for r in rs])
    succ = int((pc >= 0.9).sum())
    births = sum(r['births'] for r in rs)
    T = defaultdict(int); Sw = defaultdict(int)
    for r in rs:
        for k, v in r['transitions'].items(): T[k] += v
        for k, v in r['swaps'].items(): Sw[k] += v
    good = [r for r in rs if r['pcc'] >= 0.9]
    con = defaultdict(float); src = defaultdict(float)
    for r in rs:
        for c, v in r['top_contracts']: con[c] += v / n
        for p, v in r['top_sources']: src[p] += v / n
    return dict(n=n, success=succ, success_ci=wilson(succ, n), pcc_mean=float(pc.mean()), pcc_min=float(pc.min()), pcc_max=float(pc.max()),
                pcc_success_mean=float(np.mean([r['pcc'] for r in good])) if good else None,
                carrier_mean=float(np.mean([r['carrier'] for r in rs])),
                carrier_pcc_mean=med([r['carrier_pcc'] for r in good]) if good else None,
                extinct=sum(r['carrier_ext_gen'] is not None for r in rs),
                ext_gen_median=med([r['carrier_ext_gen'] for r in rs]),
                t10_median=med([r['t10'] for r in rs]), t50_median=med([r['t50'] for r in rs]),
                t50_max=max([r['t50'] for r in rs if r['t50'] is not None], default=None),
                growth200_median=med([r['growth_200'] for r in rs]),
                carrier_at_median={g: med([r['carrier_at'].get(g) for r in rs]) for g in ('10', '50', '200', '1000', '10000', '100000')},
                births=births,
                rate_lost_invalid=T['lost_invalid'] / births, rate_mut_carrier=T['mut_of_carriers'] / births,
                kept_valid=T['kept_valid'], lost_invalid=T['lost_invalid'], created=T['created'],
                swaps=dict(Sw), rate_accept=Sw['accepted'] / births, rate_accept_onto_none=Sw['accepted_onto_none'] / births,
                rate_reject=Sw['rejected'] / births,
                founders_median=med([r.get('final_carriers_founders') for r in good]),
                from_seed_min=min([r.get('final_carriers_from_seed_carrier_founder', 1) for r in good], default=None),
                cross_lineage_max=max([r.get('final_carriers_contract_from_other_lineage', 0) for r in good], default=None),
                top_contracts=sorted(con.items(), key=lambda kv: -kv[1])[:5], top_sources=sorted(src.items(), key=lambda kv: -kv[1])[:6],
                fb_con_share=float(np.mean([r['fb_con_share'] for r in rs])), src_allc_load=float(np.mean([r['src_allc_load'] for r in rs])),
                pcc_list=[round(float(x), 3) for x in pc])


def lottery_summary(rs):
    n = len(rs)
    oc = defaultdict(int); st = defaultdict(int)
    for r in rs:
        oc[r['outcome']] += 1; st[r['status']] += 1
    resolved = [r for r in rs if r['status'] == 'frozen']
    k = oc['efficient']; nres = len(resolved)
    T = defaultdict(int); Sw = defaultdict(int); births = 0
    for r in rs:
        births += r['births']
        for kk, v in r['transitions'].items(): T[kk] += v
        for kk, v in r['swaps'].items(): Sw[kk] += v
    eff = [r for r in rs if r['outcome'] == 'efficient']
    return dict(n=n, efficient=k, efficient_ci=wilson(k, n), resolved=nres, efficient_of_resolved_ci=wilson(sum(r['outcome'] == 'efficient' for r in resolved), nres),
                outcomes=dict(oc), status=dict(st), stop_gen_median=med([r['stop_gen'] for r in rs]),
                stop_gen_max=max(r['stop_gen'] for r in rs),
                carrier_extinct=sum(r['carrier_ext_gen'] is not None for r in rs),
                final_carrier_eff=med([r['final_carrier'] for r in eff]),
                founders_median=med([r.get('final_carriers_founders') for r in eff]),
                cross_lineage_max=max([r.get('final_carriers_contract_from_other_lineage', 0) for r in eff], default=None),
                swaps=dict(Sw), births=births, rate_accept_onto_none=Sw['accepted_onto_none'] / max(births, 1))


def main():
    rows = json.load(open(os.path.join(RUNS, 'prover_carrier_seed_rows.json')))
    st = json.load(open(os.path.join(RUNS, 'prover_carrier_static.json')))
    groups = defaultdict(list)
    for r in rows:
        key = (r['set'], r['seed'], r['b'], r['ctl'], r['f0'], r.get('k'), r['sigma'], r['N'], r['I'], r['eps'])
        groups[key].append(r)
    summ = {}
    for key, rs in sorted(groups.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        s = finite_summary(rs) if not rs[0]['lottery'] else lottery_summary(rs)
        summ['|'.join(str(x) for x in key)] = dict(key=dict(zip(('set', 'seed', 'b', 'ctl', 'f0', 'k', 'sigma', 'N', 'I', 'eps'), key)), **s)
    json.dump(dict(static=st, cells=summ), open(os.path.join(RUNS, 'prover-carrier-seed.json'), 'w'), indent=1)
    L = []
    def fin_table(title, sets, by=('seed', 'f0', 'sigma')):
        L.append('### ' + title); L.append('')
        L.append('| set | seed | b | ctl | N | f₀ | σ | success (P(C,C) ≥ 0.9) | mean P(C,C) [min, max] | carriers | carrier P(C,C) | extinct | t₁₀ / t₅₀ med (max t₅₀) | growth₂₀₀ | lost-invalid / birth | accepted swaps (onto none) / birth | founders (med) | cross-lineage max |')
        L.append('|' + '---|' * 18)
        for k, s in summ.items():
            kk = s['key']
            if kk['set'] not in sets or s['key']['eps'] == 0: continue
            L.append('| %s | %s | %s | %s | %d | %g | %g | %s | %.3f [%.3f, %.3f] | %.3f | %s | %d | %s / %s (%s) | %s | %.1e | %.1e (%.1e) | %s | %s |' % (
                kk['set'], kk['seed'], kk['b'], kk['ctl'], kk['N'], kk['f0'], kk['sigma'], ci(s['success'], s['n']), s['pcc_mean'], s['pcc_min'], s['pcc_max'],
                s['carrier_mean'], '%.3f' % s['carrier_pcc_mean'] if s['carrier_pcc_mean'] is not None else '–', s['extinct'],
                s['t10_median'], s['t50_median'], s['t50_max'], '%.4f' % s['growth200_median'] if s['growth200_median'] is not None else '–',
                s['rate_lost_invalid'], s['rate_accept'], s['rate_accept_onto_none'], s['founders_median'], s['cross_lineage_max']))
        L.append('')
    def lot_table(title, sets):
        L.append('### ' + title); L.append('')
        L.append('| set | seed | b | ctl | N | I | f₀ / k | σ | efficient | outcomes | status | stop gen med (max) | carriers extinct | founders (med, eff.) | accepted onto none / birth |')
        L.append('|' + '---|' * 15)
        for k, s in summ.items():
            kk = s['key']
            if kk['set'] not in sets: continue
            L.append('| %s | %s | %s | %s | %d | %d | %s | %g | %s | %s | %s | %s (%d) | %d | %s | %.1e |' % (
                kk['set'], kk['seed'], kk['b'], kk['ctl'], kk['N'], kk['I'], ('k=%d' % kk['k']) if kk['k'] is not None else '%g' % kk['f0'], kk['sigma'],
                ci(s['efficient'], s['n']), ', '.join('%s %d' % kv for kv in sorted(s['outcomes'].items())), ', '.join('%s %d' % kv for kv in sorted(s['status'].items())),
                s['stop_gen_median'], s['stop_gen_max'], s['carrier_extinct'], s['founders_median'], s['rate_accept_onto_none']))
        L.append('')
    fin_table('Finite ε (10⁻³), b = 0 main grid and controls, N = 6,400 unless stated', ('main', 'ctl_off', 'ctl_inf', 'ctl_mu', 'nsweep'))
    lot_table('ε = 0 twins (well-mixed, I = 1, run to the freeze)', ('twins', 'twins_ctl', 'nsweep_twins'))
    lot_table('ε = 0 lottery on islands (mN = 1)', ('lottery',))
    # composition and lineage details for the main grid
    L.append('### Composition (main grid, mean second-half shares)'); L.append('')
    for k, s in summ.items():
        kk = s['key']
        if kk['set'] in ('main', 'nsweep') and kk['eps'] > 0:
            L.append('- %s %s f₀ = %g σ = %g N = %d: contracts %s; sources %s; FairBot-contract share %.3f; source-ALLC load %.3f; P(C,C) by seed %s' % (
                kk['set'], kk['seed'], kk['f0'], kk['sigma'], kk['N'], ', '.join('`%s` %.2f' % kv for kv in s['top_contracts'][:3]),
                ', '.join('`%s` %.2f' % kv for kv in s['top_sources'][:4]), s['fb_con_share'], s['src_allc_load'], s['pcc_list']))
    L.append('')
    gen = '\n'.join(L)
    path = os.path.join(RUNS, 'prover-carrier-seed.md')
    head = '<!-- generated tables: src/prover_carrier_report.py -->\n'
    tail = '<!-- end generated -->\n'
    old = open(path).read() if os.path.exists(path) else ''
    if head in old and tail in old:
        new = old[:old.index(head)] + head + gen + '\n' + tail + old[old.index(tail) + len(tail):]
    else:
        new = '# Prover-carrier seed at b = 0 (2026-10-05)\n\n' + head + gen + '\n' + tail
    open(path, 'w').write(new)
    print(gen)


if __name__ == '__main__':
    main()
