"""Queue 80: the verdicts, scored by the registered rules (predictions/2026-11-16-script-checked-offers.md).

    python3 src/script_offers_verdicts.py          # writes runs/script-checked-offers.json
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'runs', 'script_offers')


def static_verdicts():
    """RE 1, RE 10, RE 11 and the E-series from the gates, step 0 and step 1."""
    g = json.load(open(os.path.join(D, 'gates.json')))
    s0 = json.load(open(os.path.join(D, 'step0.json')))
    s1 = json.load(open(os.path.join(D, 'step1.json')))
    V = {}
    a = g['G1']['false']['S1'] == 0 and g['G1']['false']['S0'] == 0 and all(f['ok'] for f in g['G1']['forgers'])
    b = g['G2']['accept_mismatch'] == 0
    c = 1e3 <= g['kappa_S'] <= 1e5
    V['RE 1'] = dict(holds=bool(a and b and c), falsifier=not (a and b),
                     detail=dict(false=g['G1']['false'], kappa_S=g['kappa_S'], accept_mismatch=g['G2']['accept_mismatch'],
                                 first_evaluator_worst=166456))
    fam = s1['families']
    r_sc = {f: v['M1_best_to_fair_reader_log10'] for f, v in fam.items()}
    r_free = {f: v['M1free_best_to_fair_reader_log10'] for f, v in fam.items()}
    c1 = all(x < -10 for x in r_sc.values()); c2 = any(x >= 0 for x in r_free.values())
    V['RE 10'] = dict(holds=bool(c1 and c2), clause1=c1, clause2=c2, falsifier=any(x >= -3 for x in r_sc.values()),
                      detail=dict(log10_ratio_script=r_sc, log10_ratio_script_free=r_free))
    b2 = s0['b2']
    pm, fm = b2['s_prud+ into e of Bc on 2/3']['median'], b2['s_firm+ into e of Bc on 2/3']['median']
    V['RE 11'] = dict(holds=bool(0.5 <= pm <= 2 and fm >= 20), falsifier=pm > 5, detail=dict(Pc_plus=pm, Fc_plus=fm))
    s1d = s0['s1']
    e1 = all(v['min'] >= 0.99 and v['max'] <= 1.01 for v in s1d.values())
    V['E1'] = dict(holds=e1, falsifier=not e1, detail={k: (v['min'], v['max']) for k, v in s1d.items()})
    meds = {k: v['median'] for k, v in s0['s2'].items()}
    pairs = [(meds[k], meds[k.replace('|same', '|cross')]) for k in meds if k.endswith('|same')]
    e2 = (all(abs(c - s) <= 0.01 * s for s, c in pairs) and all(abs(v - 9.75) < 0.1 for k, v in meds.items() if k.startswith('Rc into v'))
          and all(abs(v - 27.9) < 0.2 for k, v in meds.items() if 'into e' in k))
    V['E2'] = dict(holds=bool(e2), falsifier=any(c < 0.5 * s for s, c in pairs), detail=meds)
    b1 = s0['b1']
    p, x = b1['Bc into pair of (s_firm+, s_firm+)'], b1['Bc into excl of (s_firm+, s_firm+)']
    V['E3'] = dict(holds=bool(abs(p['median'] - 1) < 1e-9 and 1 <= x['median'] <= 30 and x['share_gt3'] >= 0.4),
                   falsifier=not (0.9 <= p['median'] <= 1.1), detail=dict(pair=p['median'], excl=x['median'], excl_gt3=x['share_gt3']))
    p, x = b1['Bc into pair of (s_prud+, s_prud+)'], b1['Bc into excl of (s_prud+, s_prud+)']
    V['E4'] = dict(holds=bool(p['median'] < 1 / 3 and 0.9 <= x['median'] <= 1.1), falsifier=p['median'] >= 1,
                   detail=dict(pair=p['median'], excl=x['median']))
    m = {k.split(' into')[0]: v['median'] for k, v in b2.items()}
    V['E5'] = dict(holds=bool(m['s_firm+'] >= 20 and m['s_firm'] >= 20 and m['s_open+'] >= 20 and 0.5 <= m['s_openR+'] <= 2),
                   falsifier=m['s_openR+'] > 5, detail=m)
    b3 = s0['b3']
    mx = max(v['median'] for v in b3.values())
    V['E6'] = dict(holds=bool(mx <= 1e-10), falsifier=mx > 1e-3,
                   detail=dict(registered={k: v['median'] for k, v in b3.items()},
                               posthoc_all_thirds={k: v['median'] for k, v in s0.get('b3_all_thirds_posthoc', {}).items()}))
    b4 = s0['b4']
    V['E7'] = dict(holds=all(0.9 <= v['median'] <= 1.1 for v in b4.values()), falsifier=None, detail={k: v['median'] for k, v in b4.items()})
    V['E8'] = dict(holds=s0['jump_chain']['max_abs_z'] < 4, falsifier=None, detail=s0['jump_chain'])
    V['E9'] = dict(holds=all(x < -20 for x in r_free.values()), falsifier=any(x >= -10 for x in r_free.values()), detail=r_free)
    shares = {f: v['script_share_min'] for f, v in fam.items()}
    V['E10'] = dict(holds=all(x < -40 for x in r_sc.values()) and all(s >= 1 / 3 for s in shares.values()),
                    falsifier=any(x > -20 for x in r_sc.values()), detail=dict(ratio=r_sc, script_share_min=shares))
    return V


def label(v):
    if v['holds']:
        return 'holds'
    if v.get('falsifier'):
        return 'falsified'
    if v.get('falsifier') is None:
        return 'fails (no falsifier registered)'
    return 'fails, falsifier not fired'


if __name__ == '__main__':
    V = static_verdicts()
    p2 = os.path.join(D, 'verdicts_step2.json')
    if os.path.exists(p2):
        V.update(json.load(open(p2)))
    for k, v in V.items():
        v['verdict'] = label(v)
    order = ['RE %d' % i for i in range(1, 13)] + ['E%d' % i for i in range(1, 11)]
    V = {k: V[k] for k in order if k in V}
    json.dump(V, open(os.path.join(ROOT, 'runs', 'script-checked-offers.json'), 'w'), indent=1, default=str)
    for k, v in V.items():
        print(k, v['verdict'])
