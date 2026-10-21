"""Tables and prediction verdicts for the coalition-proof auctions run (reads runs/auctions/*.json, writes runs/auctions/summary.json,
small CSVs, and prints a verdict digest).  The pre-registered scoring conventions are in predictions/2026-10-21-coalition-proof-auctions.md.

    python3 src/auctions_report.py
"""
import csv, glob, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'auctions')
FAMS = ('AM', 'AMplus', 'subs', 'twopk')
VARS = ('R1_strict', 'R1_weak', 'R1_weak_literal', 'R2_strict', 'R2_weak')


def jl(name):
    p = os.path.join(OUT, name)
    return json.load(open(p)) if os.path.exists(p) else None


def cell(key):
    p = os.path.join(OUT, 'cells', key + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def write_csv(name, header, rows):
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def part_a():
    v = {}
    st = {f: jl('static_%s.json' % f) for f in FAMS}
    wide = jl('static_wide_AM.json'); bw = jl('static_bw_AM.json'); ring = jl('static_ring.json')
    rows = []
    for f in FAMS:
        if st[f] is None: continue
        for rule in ('vcg', 'surcharge'):
            r = st[f]['rules'][rule]
            for var in VARS:
                d = r['variants'][var]
                ib = d['instances_with_break_by_class']
                rows.append([f, rule, var, st[f]['n_instances_evaluated'], round(d['robust_frac'], 4), round(d['unresolved_instances'], 4),
                             round(ib['singleton'], 4), round(ib['losers'], 4), round(ib['winners'], 4), round(ib['mixed'], 4)])
    write_csv('table_A_robust.csv', ['family', 'rule', 'variant', 'instances', 'robust_frac', 'unresolved_instances', 'break_singleton', 'break_losers', 'break_winners', 'break_mixed'], rows)
    rows = []
    for f in FAMS:
        if st[f] is None: continue
        s = st[f]
        rows.append([f, s['n_instances_evaluated'], round(s['P_vcg_in_core'], 4), round(s['mean_surcharge_total'], 4), round(s['share_positive_surcharge'], 4),
                     round(s['mean_surcharge_when_positive'], 4), round(s['efficient_welfare'], 4)] +
                    [round(s['revenue_at_truth'][r], 4) for r in ('vcg', 'surcharge', 'fp')] + [round(s['bidder_welfare_at_truth'][r], 4) for r in ('vcg', 'surcharge', 'fp')])
    write_csv('table_A_core_revenue.csv', ['family', 'instances', 'P_vcg_in_core', 'mean_surcharge', 'share_positive_surcharge', 'mean_surcharge_when_positive', 'efficient_welfare',
                                           'rev_vcg', 'rev_surcharge', 'rev_fp', 'bidder_welfare_vcg', 'bidder_welfare_surcharge', 'bidder_welfare_fp'], rows)
    rows = []
    for f in FAMS:
        if st[f] is None: continue
        for rule in ('vcg', 'surcharge'):
            sp = st[f]['rules'][rule]['spite']
            for lab, d in sp.items():
                rows.append([f, rule, lab, d['strict_broken_instances'], d['deterred_only_instances'], round(d['share_instances'], 4), d['strict_break_events'],
                             d['deterred_only_events'], round(d['share_events'], 4), d['weak_not_strict_events']])
    write_csv('table_A_spite.csv', ['family', 'rule', 'tie_pair', 'strict_broken_instances', 'deterred_only_instances', 'share_instances', 'strict_break_events',
                                    'deterred_only_events', 'share_events', 'weak_not_strict_events'], rows)
    if wide:
        rows = []
        for rule in ('vcg', 'surcharge'):
            r = wide['rules'][rule]
            for var in VARS:
                d = r['variants'][var]; ib = d['instances_with_break_by_class']
                rows.append([rule, var, round(d['robust_frac'], 4), round(ib['singleton'], 4), round(ib['losers'], 4), round(ib['winners'], 4), round(ib['mixed'], 4)])
            for lab, d in r['spite'].items():
                rows.append([rule, 'spite_' + lab, d['share_instances'], d['share_events'], d['deterred_only_events'], d['strict_break_events'], ''])
        write_csv('table_A_wide.csv', ['rule', 'variant_or_spite', 'robust_frac_or_share_instances', 'singleton_or_share_events', 'losers_or_deterred_events', 'winners_or_strict_events', 'mixed'], rows)
    # verdicts
    A_ = st['AM']
    if A_:
        v['p1'] = dict(subs_vcg_in_core=st['subs']['P_vcg_in_core'] if st['subs'] else None,
                       subs_vcg_robust={var: st['subs']['rules']['vcg']['variants'][var]['robust_frac'] for var in VARS} if st['subs'] else None,
                       subs_vcg_breaks_by_coalition=st['subs']['rules']['vcg']['variants']['R1_strict']['by_coalition'] if st['subs'] else None)
        v['p1']['verdict'] = 'held' if (st['subs'] and st['subs']['P_vcg_in_core'] == 1.0 and all(x == 1.0 for x in v['p1']['subs_vcg_robust'].values())) else 'failed'
        mm = A_['rules']['vcg']['pred2_mismatch']
        v['p2'] = dict(mismatch=mm, n=A_['n_instances_evaluated'], verdict='held' if mm <= 0.01 * A_['n_instances_evaluated'] else 'failed')
        p3 = A_['rules']['surcharge']['pred3']
        v['p3'] = dict(p3, verdict='held' if (p3['pair_AB_break_overall'] == 0 and p3['singleton_break_on_positive'] >= 0.8) else 'failed')
        # losers' collusion under surcharge: class 'losers' break share (instances where A,B are truthful losers)
        v['p3']['losers_class_break_share_R1_strict'] = A_['rules']['surcharge']['variants']['R1_strict']['instances_with_break_by_class']['losers']
        sv = A_['rules']['vcg']['spite']['R1']; ss = A_['rules']['surcharge']['spite']['R1']
        v['p4'] = dict(vcg_instances=sv['share_instances'], vcg_events=sv['share_events'], surcharge_instances=ss['share_instances'], surcharge_events=ss['share_events'])
        if wide:
            wv = wide['rules']['vcg']['spite']['R1']; ws = wide['rules']['surcharge']['spite']['R1']
            v['p4']['wide_vcg_instances'] = wv['share_instances']; v['p4']['wide_vcg_events'] = wv['share_events']
            v['p4']['wide_surcharge_instances'] = ws['share_instances']; v['p4']['wide_surcharge_events'] = ws['share_events']
        shares = [sv['share_instances'], sv['share_events'], ss['share_instances'], ss['share_events']]
        v['p4']['verdict'] = 'held' if min(shares) >= 0.8 else ('failed' if max(shares) < 0.5 else 'partial')
    if bw:
        r2 = [bw['variants']['R2_strict']['nonempty_frac'], bw['variants']['R2_weak']['nonempty_frac']]
        v['p5'] = dict(nonempty_frac_R2_strict=r2[0], nonempty_frac_R2_weak=r2[1], share_leader_value_exceeds_marginal=bw['variants']['R2_strict'].get('share_leader_value_exceeds_marginal_contribution'),
                       verdict='held' if max(r2) <= 0.5 else 'failed')
        b6 = bw['variants']['R1_weak']
        v['p6'] = dict(nonempty=b6['nonempty_frac'], all_within_1_tick=b6['all_within_1_tick'], some_within_1_tick=b6['some_within_1_tick'], mean_max_dist=b6['mean_max_dist'],
                       share_with_zero_revenue_profile=b6.get('share_with_zero_revenue_profile'), mean_revenue_in_set=b6['mean_revenue_in_set'],
                       mean_vcg_revenue=b6['mean_vcg_revenue_same_instances'], mean_bidder_welfare_in_set=b6['mean_bidder_welfare_in_set'],
                       mean_vcg_bidder_welfare=b6['mean_vcg_bidder_welfare_same_instances'],
                       verdict='held' if b6['all_within_1_tick'] >= 0.9 else ('failed' if b6['all_within_1_tick'] < 0.7 else 'partial'))
    v['ring'] = ring
    return v


def part_b():
    v = {}
    g = lambda *a: cell('%s_%s_%s_%s_N%d_mN%g' % a)
    # prediction 7: collusion, VCG, no audit, prior U
    c = g('vcg', 'collusion', 'U', 'open', 100, 0)
    if c:
        v['p7'] = dict(pair=c['class_share']['pair'], pair_enforced=c['pair_enforced_share'], pair_unenforced=c['pair_unenforced_share'], policed=c['policed_share'],
                       censored=c['censored_share'], run_sd_pair=c['run_sd']['pair'], run_sd_policed=c['run_sd']['policed'],
                       verdict='held' if (c['class_share']['pair'] >= 0.3 and c['policed_share'] >= 0.2) else ('failed' if (c['class_share']['pair'] < 0.1 or c['policed_share'] < 0.05) else 'partial'))
    # prediction 8
    np_ = cell('vcg_collusion_U-noPOL_open_N100_mN0')
    if c and np_:
        ratio = np_['class_share']['pair'] / max(1e-12, c['class_share']['pair'])
        v['p8'] = dict(n_policed=c['n_policed'], policed_never_tested=c['policed_never_tested'], policed_tested_after_fix=c['policed_tested_after_fix'],
                       founding_exposure_share=c['founding_exposure_share'],
                       pair_U=c['class_share']['pair'], pair_noPOL=np_['class_share']['pair'], ratio=ratio)
        a = (c['policed_never_tested'] is not None and c['policed_never_tested'] > 0.5); b = ratio >= 1.5
        v['p8']['verdict'] = 'held' if (a and b) else ('failed' if (not a and not b) else 'partial')
    # prediction 9
    cs = g('surcharge', 'collusion', 'U', 'open', 100, 0); ts = g('surcharge', 'threshold', 'U', 'open', 100, 0)
    if cs and ts:
        v['p9'] = dict(collusion_pair=cs['class_share']['pair'], threshold_items_dev_behaviour=ts['items_dev_behaviour_share'], threshold_items_label_dev=ts['items_label_dev_share'],
                       threshold_pair=ts['class_share']['pair'])
        ok1 = cs['class_share']['pair'] < 0.02; ok2 = ts['items_dev_behaviour_share'] >= 0.4
        bad = cs['class_share']['pair'] >= 0.05 or ts['items_dev_behaviour_share'] < 0.2
        v['p9']['verdict'] = 'held' if (ok1 and ok2) else ('failed' if bad else 'partial')
    # prediction 10
    ca = g('vcg', 'collusion', 'U', 'audit', 100, 0)
    if c and ca:
        v['p10'] = dict(rev_open=c['mean_rev'], rev_audit=ca['mean_rev'], pair_audit=ca['class_share']['pair'], policed_audit=ca['policed_share'],
                        pair_enforced_audit=ca['pair_enforced_share'], eff_open=c['mean_eff'], eff_audit=ca['mean_eff'],
                        run_rev_diff_mean=float(np.mean(np.array(ca['run_rev_means']) - np.array(c['run_rev_means']))),
                        threshold_vcg_rev_open=(g('vcg', 'threshold', 'U', 'open', 100, 0) or {}).get('mean_rev'), threshold_vcg_rev_audit=(g('vcg', 'threshold', 'U', 'audit', 100, 0) or {}).get('mean_rev'))
        v['p10']['verdict'] = 'held' if (ca['class_share']['pair'] == 0 or ca['pair_enforced_share'] == 0) and ca['policed_share'] == 0 and ca['mean_rev'] >= c['mean_rev'] - 1e-9 else 'failed'
    # prediction 11
    cm = g('vcg', 'collusion', 'M', 'open', 100, 0)
    if c and cm:
        ratio = cm['class_share']['pair'] / max(1e-12, c['class_share']['pair'])
        v['p11'] = dict(pair_U=c['class_share']['pair'], pair_M=cm['class_share']['pair'], ratio=ratio, n_founded_M=cm['n_pol_and_pair_founded'], driven_out_M=cm['pair_driven_out_share'],
                        joint_zero_M=cm['pair_joint_zero_share'], driven_out_U=c['pair_driven_out_share'], n_founded_U=c['n_pol_and_pair_founded'])
        a = ratio >= 1.5; b = cm['pair_driven_out_share'] is not None and cm['pair_driven_out_share'] >= 0.7
        v['p11']['verdict'] = 'held' if (a and b) else ('failed' if (ratio < 1.5 and (cm['pair_driven_out_share'] or 0) < 0.5) else 'partial')
    # prediction 12
    ps = jl('partB_static.json')
    if ps:
        t = ps['tremble']['vcg/collusion']
        v['p12'] = dict(E_uP_POL=t['tremble']['POL']['E_uP'], E_uP_T=t['tremble']['T']['E_uP'], E_uP_SH=t['tremble']['SH']['E_uP'], no_tremble_POL=t['no_tremble']['POL']['uP'], no_tremble_T=t['no_tremble']['T']['uP'],
                        verdict='held' if t['tremble']['POL']['E_uP'] < t['tremble']['T']['E_uP'] else 'failed')
    # the big table
    rows = []
    for p in sorted(glob.glob(os.path.join(OUT, 'cells', '*.json'))):
        d = json.load(open(p)); cs_ = d['class_share']
        rows.append([d['key'], d['params']['rule'], d['params']['inst'], d['params']['prior'], d['params']['audit'], d['params']['N'], d['params']['mN'], d['params']['noPOL'], d['n_runs'],
                     round(cs_['pair'], 4), round(cs_['items_dev'], 4), round(cs_['p_dev'], 4), round(cs_['truthful'], 4), round(cs_['mixed'], 4),
                     round(d['pair_enforced_share'], 4), round(d['pair_unenforced_share'], 4), round(d['policed_share'], 4), round(d['items_dev_behaviour_share'], 4),
                     round(d['mean_eff'], 4), round(d['mean_rev'], 4), round(d['censored_share'], 4), d['n_policed'],
                     d['policed_never_tested'] if d['policed_never_tested'] is None else round(d['policed_never_tested'], 4),
                     d['pair_driven_out_share'] if d['pair_driven_out_share'] is None else round(d['pair_driven_out_share'], 4),
                     d['fixed_gen_quantiles'][1] if d['fixed_gen_quantiles'] else None])
    write_csv('table_B_cells.csv', ['key', 'rule', 'inst', 'prior', 'audit', 'N', 'mN', 'noPOL', 'runs', 'pair', 'items_dev', 'p_dev', 'truthful', 'mixed', 'pair_enforced', 'pair_unenforced',
                                    'policed', 'items_dev_behaviour', 'mean_eff', 'mean_rev', 'censored', 'n_policed', 'policed_never_tested', 'pair_driven_out', 'median_fixed_gen'], rows)
    return v


def main():
    out = dict(part_a=part_a(), part_b=part_b())
    json.dump(out, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1, default=float)
    for part in ('part_a', 'part_b'):
        for k, d in out[part].items():
            if k == 'ring':
                continue
            print(k, d)


if __name__ == '__main__':
    main()
