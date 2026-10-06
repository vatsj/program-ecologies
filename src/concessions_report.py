"""Markdown for the concessions run (runs/concessions.md) from runs/concessions-static.json, runs/concessions/*.json.

    python3 src/concessions_report.py named      # the named-program block for the predictions file
    python3 src/concessions_report.py all        # runs/concessions.md and runs/concessions.json
"""
import os, sys, json, glob
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
OUT = os.path.join(RUNS, 'concessions')

SHORTW = {'scab': 'scab', 'T0 (strike iff s = 0)': 'T0', 'T1 = militant (strike iff s <= 1/4)': 'T1', 'always strike': 'strike',
          'union': 'union', 'militant- (strike iff not BOX(s = 1/2))': 'mil-', 'T0- (strike iff not BOX(s in {1/4,1/2}))': 'T0-'}


def f(x, d=3):
    if x is None:
        return '–'
    if isinstance(x, str):
        return x
    if x != 0 and abs(x) < 10 ** (-d):
        return '%.1e' % x
    return ('%.' + str(d) + 'f') % x


def short_boss(k):
    return k.split(' = ')[0].split(' (')[0] if ' = ' in k or ' (' in k else k


def named_block(S, key='named_table_CC'):
    T = S[key]
    L = []
    L.append('**Named workers** (union-run grammar, level-0 boxes about the current encounter):\n')
    for k, v in T['worker_src'].items():
        L.append('- %s: `%s`' % (k, v))
    L.append('\n**Named bosses** (`W_j(^(s,none))` = worker j\'s play against the quoted constant boss (s, none) beside the current other worker):\n')
    for k, v in T['boss_src'].items():
        L.append('- %s: `%s`' % (k, v))
    L.append('\n**What the probes read** (quoted self-pair play, executed / recommended; fv = first world from which the strike probe fails, 127 = never):\n')
    L.append('| worker pair | vs (0,none) | vs (1/4,none) | fv strike@0 L0 / L1 | fv strike@1/4 L0 / L1 |')
    L.append('|---|---|---|---|---|')
    for k, v in T['quoted'].items():
        a, b = v['vs (0,none)'], v['vs (1/4,none)']
        L.append('| %s | %s / %s | %s / %s | %d / %d | %d / %d |' % (SHORTW[k], a['executed'], a['recommended'], b['executed'], b['recommended'],
                                                                 a['fv_strike_L0'], a['fv_strike_L1'], b['fv_strike_L0'], b['fv_strike_L1']))
    ws = T['workers']
    L.append('\n**Play and payoffs (boss, W1, W2) of every named boss against every named worker self-pair** (%s):\n' % key.split('_')[-1])
    L.append('| boss | ' + ' | '.join(SHORTW[w] for w in ws) + ' |')
    L.append('|---' * (len(ws) + 1) + '|')
    rows = {(r['boss'], r['W1'], r['W2']): r for r in T['rows']}
    for b in T['bosses']:
        cells = []
        for w in ws:
            r = rows[(b, w, w)]
            cells.append('%s (%s)' % (r['play'], ', '.join('%g' % v for v in r['pay'])))
        L.append('| %s | %s |' % (short_boss(b), ' | '.join(cells)))
    L.append('\n**Mixed pairs** (W1, W2) for the bosses that read W1 (probe, current-encounter and faker bosses):\n')
    mixed = [('T1 = militant (strike iff s <= 1/4)', 'scab'), ('scab', 'T1 = militant (strike iff s <= 1/4)'),
             ('T1 = militant (strike iff s <= 1/4)', 'T0 (strike iff s = 0)'), ('T0 (strike iff s = 0)', 'T1 = militant (strike iff s <= 1/4)'),
             ('T1 = militant (strike iff s <= 1/4)', 'always strike'), ('always strike', 'scab'), ('scab', 'always strike'),
             ('militant- (strike iff not BOX(s = 1/2))', 'scab')]
    L.append('| boss | ' + ' | '.join('%s, %s' % (SHORTW[a], SHORTW[b]) for a, b in mixed) + ' |')
    L.append('|---' * (len(mixed) + 1) + '|')
    for b in T['bosses']:
        if b.startswith('('):
            continue
        cells = []
        for a, c in mixed:
            r = rows[(b, a, c)]
            cells.append('%s (%s)' % (r['play'], ', '.join('%g' % v for v in r['pay'])))
        L.append('| %s | %s |' % (short_boss(b), ' | '.join(cells)))
    return '\n'.join(L)


def static_md(S):
    L = []
    L.append('### Languages (mass-preserving substitution)\n')
    L.append('| arm | grammar functions (n = 11) | included functions | boss classes | worker classes | boss mass included | merged by fingerprint | null (novel two-atom policies) | probe functions dropped (ref) | merge check failures |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for arm, I in S['languages'].items():
        L.append('| %s | %d | %d | %d | %d | %.4f | %.4f (%d) | %.4f (%d policies) | %.4f | %d / %d |' % (
            arm, I['grammar_functions'], I['included_functions'], I['KcB'], I['KcW'], I['boss_mass_included_functions'], I['boss_mass_merged'],
            I['merged_functions'], I['boss_mass_null'], I['novel_policies'], I['ref_probe_mass_dropped'], I['merge_verify_failures'], I['merge_verified']))
    L.append('')
    L.append('### Prior masses of the named classes\n')
    m = S['masses']
    keys = list(m['P01']['bosses'])
    L.append('| boss class | P01 | P0 | sham | ref |')
    L.append('|---|---|---|---|---|')
    for k in keys:
        if k.startswith('D*_'):
            continue
        L.append('| %s | %s |' % (short_boss(k), ' | '.join(f(m[a]['bosses'].get(k), 2) if m[a]['bosses'].get(k) is not None else '–' for a in ('P01', 'P0', 'sham', 'ref'))))
    L.append('| D* family (8 variants, each) | %s | – | – | – |' % f(m['P01']['bosses']['D*_1 L00'], 2))
    L.append('| all constants | %s |' % ' | '.join(f(m[a]['boss_constants'], 3) for a in ('P01', 'P0', 'sham', 'ref')))
    L.append('| all probe classes | %s |' % ' | '.join(f(m[a]['boss_probe_classes'], 3) for a in ('P01', 'P0', 'sham', 'ref')))
    L.append('\nWorker masses (all arms): ' + ', '.join('%s %s' % (SHORTW[k], f(v, 2)) for k, v in m['P01']['workers'].items()) + '.\n')
    return '\n'.join(L)


def states_md(S, arm):
    L = []
    L.append('| state | play | payoffs | strict B (mass; p/event at 10⁴) | neutral B | neutral W1 | neutral W2 | strict W | top move at N = 10⁴ | best excluded boss (gain; mass) |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for k, v in S['named_states'][arm].items():
        a = v['by_slot_kind']
        nB = a['B']['neutral-keep']['mass'] + a['B']['neutral-change']['mass']
        nW1 = a['W1']['neutral-keep']['mass'] + a['W1']['neutral-change']['mass']
        nW2 = a['W2']['neutral-keep']['mass'] + a['W2']['neutral-change']['mass']
        sW = a['W1']['strict']['mass'] + a['W2']['strict']['mass']
        t = v['top'][0]
        ea = S['excluded_audit'][arm][k]
        L.append('| %s | %s | %s | %s; %s | %s | %s | %s | %s | %s %s (%s, Δ %+g) | %s; %s |' % (
            k, v['play'], ', '.join('%g' % x for x in v['pay']), f(a['B']['strict']['mass'], 4), f(a['B']['strict']['p_N10000'], 2),
            f(nB, 3), f(nW1, 4), f(nW2, 3), f(sW, 4), t['slot'], '`%s`' % t['mutant'], t['kind'], t['du'],
            ('%+g' % ea['best_null']['gain']) if ea['best_null']['gain'] > 0 else 'none', f(ea['null_strict_mass'], 4)))
    return '\n'.join(L)


SUMM = ['fair', 'intermediate', 'zero wage', 'strike', 'scab split', 'repression:strike', 'repression:source']


def load_cells():
    cells = {}
    for fn in sorted(glob.glob(os.path.join(OUT, 'chain_*.json'))):
        d = json.load(open(fn))
        key = os.path.basename(fn)[6:-5]
        cells[key] = d
    return cells


def cell_label(k):
    return k.replace('_pool0_c0.5_c0.5', '_c0.5').replace('_pool1_c0.1_c0.1', '+pool_c0.1').replace('_pool1_c0.5_c0.5', '+pool_c0.5').replace('_pool0_c0.5', '').replace('_c0.5', ' c=0.5').replace('_c0.1', ' c=0.1').replace('_N', ' N=')


def chain_table(cells, keys):
    L = ['| cell | states (core) | fair | 1/4 | zero wage | strike | scab split | repression | efficiency | payoffs (B, W1, W2) | three-role | support 99% | outcome-changing cut | dense log-GTH check |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for k in keys:
        if k not in cells:
            continue
        d = cells[k]; s = d['summary']
        rep = s['repression:strike'] + s['repression:source']
        mp = d['mean_payoff']
        L.append('| %s | %d (%d) | %s | %s | %s | %s | %s | %s | %.3f | %.3f, %.3f, %.3f | %s | %d | %s | %s |' % (
            cell_label(k), d['states'], d['core'], f(s['fair'], 4), f(s['intermediate'], 4), f(s['zero wage']), f(s['strike']), f(s['scab split']),
            f(rep, 4), d['efficiency'], mp['boss'], mp['W1'], mp['W2'], f(d['three_role']['threshold'], 4), d['support_size_99'], f(d['rel_cut_change'], 3),
            ('TV %.1e' % d['solver_check']['tv']) if 'solver_check' in d else '–'))
    return '\n'.join(L)


def basin_table(cells, keys):
    L = ['| cell | basin | π | escape / event | residence (events) | next: fair | next: 1/4 | next: zero | next: whacking | return fraction |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for k in keys:
        if k not in cells:
            continue
        br = cells[k]['basin_rates']
        for b in ('fair', '1/4', 'zero wage', 'whacking'):
            if b not in br:
                continue
            v = br[b]
            nx = v['next_basin']
            L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                cell_label(k), b, f(v['pi'], 4), f(v['escape_rate'], 2), f(v['residence_events'], 0), f(nx.get('fair'), 3), f(nx.get('1/4'), 3),
                f(nx.get('zero wage'), 3), f(nx.get('whacking'), 3), f(v['return_fraction'], 3)))
        L.append('| %s | (outside the four basins) | %s | | | | | | | |' % (cell_label(k), f(br['_pi_outside_basins'], 3)))
    return '\n'.join(L)


def support_md(d, n=10, nt=5):
    L = ['| π | state (boss \\| W1 \\| W2) | play | summary | payoffs |', '|---|---|---|---|---|']
    for e in d['support'][:n]:
        L.append('| %s | `%s` | %s | %s | %s |' % (f(e['pi'], 4), e['state'].replace('|', '\\|'), e['play'], e['summary'], ', '.join('%g' % x for x in e['pay'])))
    L.append('')
    L.append('Transitions out of the top states (probability per mutation event):\n')
    for t in d['transitions'][:nt]:
        ek = t['exit_by_kind']
        L.append('- `%s` (π %s): strict %s, neutral-change %s, neutral-keep %s; top: %s' % (
            t['state'], f(t['pi'], 4), f(ek['strict'], 2), f(ek['neutral-change'], 2), f(ek['neutral-keep'], 2),
            '; '.join('%s %s `%s` → %s (%s, Δ %+g)' % (e['slot'], e['kind'], e['mutant'], e['to'], f(e['p'], 2), e['du']) for e in t['top'][:3])))
    return '\n'.join(L)


def fair_md(d):
    L = []
    pf = d['summary']['fair']
    L.append('Fair mass %s; by boss class: %s.' % (f(pf, 4), '; '.join('`%s` %s' % (k, f(v, 4)) for k, v in list(d['fair_boss_mass'].items())[:6])))
    L.append('By worker class (half per slot): %s.' % '; '.join('`%s` %s' % (k, f(v, 4)) for k, v in list(d['fair_worker_mass'].items())[:6]))
    L.append('Fair exits (per unit fair mass per event): %s.' % '; '.join('%s %s' % (k, f(v, 2)) for k, v in list(d['fair_exit_by_slot_kind'].items())[:6]))
    L.append('1/4 mass by boss class: %s.' % '; '.join('`%s` %s' % (k, f(v, 4)) for k, v in list(d['quarter_boss_mass'].items())[:5]))
    L.append('Probe-carrying boss present in %s of π; union in fair support %s.' % (f(d['mass_probe_boss'], 4), f(d['union_mass_in_fair'], 4)))
    return '\n'.join(L)


def pres_md(cells, keys):
    L = ['| cell | fair mass | analysed | with a demand-lowering neutral substitute | ... after which a boss strictly invades | neutral substitute mass: same / lower / higher demand |',
         '|---|---|---|---|---|---|']
    for k in keys:
        if k not in cells:
            continue
        p = cells[k]['preservation']
        if not p.get('analysed_fair_mass'):
            L.append('| %s | %s | – | – | – | – |' % (cell_label(k), f(p.get('fair_mass', 0), 4)))
            continue
        L.append('| %s | %s | %s | %s | %s | %s / %s / %s |' % (cell_label(k), f(p['fair_mass'], 4), f(p['analysed_fair_mass'], 4), f(p['with_lowering'], 3),
                                                          f(p['with_lowering_and_strict_boss'], 3), f(p['sub_mass_same'], 3), f(p['sub_mass_lower'], 3), f(p['sub_mass_higher'], 3)))
    return '\n'.join(L)


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None, None)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return p, max(0.0, c - h), min(1.0, c + h)


def lottery_summary(d):
    runs = d['runs']; R = len(runs)
    I = d['params']['I']
    out = dict(cell=d['cell'], runs=R, params=d['params'])
    st = {}
    for r in runs:
        st[{1: 'closed', 5: 'local-closed', 4: 'censored'}.get(r['status'], str(r['status']))] = st.get({1: 'closed', 5: 'local-closed', 4: 'censored'}.get(r['status'], str(r['status'])), 0) + 1
    out['status'] = st
    out['stop_gen_median'] = float(np.median([r['stop_gen'] for r in runs]))
    est = [min([g for g in r['first_fair'] if g >= 0], default=-1) for r in runs]
    for T in (500, 10000, 100000):
        k = sum(1 for g in est if 0 <= g <= T)
        out['established_by_%d' % T] = wilson(k, R)
    e = [g for g in est if g >= 0]
    out['establishment_time_median'] = float(np.median(e)) if e else None
    out['establishment_times'] = sorted(e)
    ff = np.array([np.mean(r['fair_final']) for r in runs])
    out['persistence_mean'] = float(ff.mean()); out['persistence_ci'] = float(1.96 * ff.std(ddof=1) / np.sqrt(R)) if R > 1 else 0.0
    out['runs_with_fair_at_stop'] = wilson(int((ff > 0).sum()), R)
    lab = np.array([r['label'] for r in runs])
    out['labels'] = {SUMM[k]: float((lab == k).mean()) for k in range(7)}
    fin = np.array([r['final'] for r in runs])
    out['payoff_vector'] = [float(x) for x in fin[:, :, 19:22].mean((0, 1))]
    ts = {}
    for g in runs[0]['ts']:
        v = np.array([r['ts'][g] for r in runs])
        ts[g] = dict(militant=float(v[:, :, 0].mean()), probe_boss=float(v[:, :, 1].mean()), concession_boss=float(v[:, :, 2].mean()),
                     striker=float(v[:, :, 3].mean()))
    out['ts'] = ts
    maj = {}
    nf = 0; npb = 0
    wage_isl = np.zeros(4)
    for r in runs:
        for i, m in enumerate(r['majority']):
            if r['fair_final'][i]:
                key = ' | '.join(m)
                maj[key] = maj.get(key, 0) + 1
                nf += 1
                if '(^' in m[0]:
                    npb += 1
            fi = r['final'][i]
            prod = fi[22]
            if prod >= 0.05:
                wage_isl[int(np.argmax([sum(fi[7 + 3 * w_:10 + 3 * w_]) for w_ in range(3)]))] += 1
            else:
                wage_isl[3] += 1
    out['fair_island_majorities'] = dict(sorted(maj.items(), key=lambda kv: -kv[1])[:8])
    out['fair_islands_probe_boss_majority'] = (npb / nf) if nf else None
    out['island_wage'] = dict(zip(['0', '1/4', '1/2', 'none'], (wage_isl / wage_isl.sum()).round(4).tolist()))
    return out


def lottery_md(sums):
    L = ['| cell | status | fair island by 500 | by 10⁴ | by 10⁵ (or stop) | median time to first fair island | fair islands at stop (mean ± 95%) | runs with a fair island at stop | island labels at stop (fair / 1/4 / zero / strike / split) | payoffs (B, W1, W2) |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for s in sums:
        w = lambda t: '%.2f [%.2f, %.2f]' % s[t] if s[t][0] is not None else '–'
        lb = s['labels']
        L.append('| %s | %s | %s | %s | %s | %s | %.3f ± %.3f | %s | %.3f / %.3f / %.3f / %.3f / %.3f | %s |' % (
            s['cell'], ', '.join('%s %d' % kv for kv in s['status'].items()), w('established_by_500'), w('established_by_10000'),
            w('established_by_100000'), f(s['establishment_time_median'], 0), s['persistence_mean'], s['persistence_ci'], w('runs_with_fair_at_stop'),
            lb['fair'], lb['intermediate'], lb['zero wage'], lb['strike'], lb['scab split'], ', '.join('%.3f' % x for x in s['payoff_vector'])))
    L.append('')
    L.append('| cell | island wage at stop (0 / 1/4 / 1/2 / no production) | fair islands whose majority boss carries a probe |')
    L.append('|---|---|---|')
    for s in sums:
        w = s['island_wage']
        L.append('| %s | %.3f / %.3f / %.3f / %.3f | %s |' % (s['cell'], w['0'], w['1/4'], w['1/2'], w['none'], f(s['fair_islands_probe_boss_majority'], 3)))
    L.append('')
    L.append('Island shares over time (mean over runs and islands): militant T1 / probe-carrying boss / concession boss (pays 1/2 to the militant pair, 0 to the scab pair) / constant striker.\n')
    gs = list(sums[0]['ts'])
    L.append('| cell | ' + ' | '.join('g = %s' % g for g in gs) + ' |')
    L.append('|---' * (len(gs) + 1) + '|')
    for s in sums:
        L.append('| %s | %s |' % (s['cell'], ' | '.join('%.3f / %.3f / %.3f / %.2f' % (v['militant'], v['probe_boss'], v['concession_boss'], v['striker'])
                                                       for v in s['ts'].values())))
    return '\n'.join(L)


def reduced_md(R):
    sets = ['constants', '+D0 family (P0)', '+D0 family, D14', '+D0 family, D14, D* family', '+D* family only', '+all, and wage fakers']
    L = ['| evaluator | boss set | prior | N = 10² fair / 1/4 / zero | N = 10³ | N = 10⁴ | N = 10⁵ | top state at 10⁴ (π) |', '|---|---|---|---|---|---|---|---|']
    for ev, D in R.items():
        for s in sets:
            for pr in ('uniform', 'length'):
                cells = []
                for N in (100, 1000, 10000, 100000):
                    v = D.get('%s | %s | N=%d' % (s, pr, N))
                    if v is None:
                        cells.append('–'); continue
                    m = v['summary']
                    cells.append('%.3f / %.3f / %.3f' % (m['fair'], m['intermediate'], m['zero wage']))
                t = D['%s | %s | N=10000' % (s, pr)]['top'][0]
                L.append('| %s | %s | %s | %s | `%s` (%.3f) |' % (ev, s, pr, ' | '.join(cells), t['state'], t['pi']))
    return '\n'.join(L)


def all_tables():
    S = json.load(open(os.path.join(RUNS, 'concessions-static.json')))
    cells = load_cells()
    T = {}
    T['named'] = named_block(S)
    T['named_RR'] = named_block(S, 'named_table_RR')
    T['languages'] = static_md(S)
    T['states_P01'] = states_md(S, 'P01'); T['states_P0'] = states_md(S, 'P0')
    T['fakers'] = json.dumps(S['fakers'], indent=1)
    T['loeb'] = '\n'.join('- %s: %s' % (k, ' → '.join(v)) for k, v in S['loeb_traces_CC'].items())
    main = ['P01_CC_c0.5_N100', 'P01_CC_c0.5_N1000', 'P01_CC_c0.5_N10000', 'P01_CC_c0.5_N10000_th10', 'P01_CC_c0.5_N30000', 'P01_CC_c0.5_N30000_th10',
            'P0_CC_c0.5_N1000', 'P0_CC_c0.5_N10000', 'sham_CC_c0.5_N100', 'sham_CC_c0.5_N1000', 'sham_CC_c0.5_N10000',
            'ref_CC_c0.5_N100', 'ref_CC_c0.5_N1000', 'ref_CC_c0.5_N10000', 'ref_CC_c0.5_N30000',
            'P01_CC_c0.1_N10000', 'ref_CC_c0.1_N10000', 'P01_CC_c0.5_N10000_nofaker',
            'P01_RR_pool0_c0.5_c0.5_N1000', 'P01_RR_pool0_c0.5_c0.5_N10000', 'ref_RR_pool0_c0.5_c0.5_N1000', 'ref_RR_pool0_c0.5_c0.5_N10000',
            'P01_CC_pool1_c0.1_c0.1_N1000', 'P01_CC_pool1_c0.1_c0.1_N10000', 'P01_CC_pool1_c0.5_c0.5_N1000', 'P01_CC_pool1_c0.5_c0.5_N10000']
    T['chain'] = chain_table(cells, main)
    T['basins'] = basin_table(cells, ['P01_CC_c0.5_N1000', 'P01_CC_c0.5_N10000', 'P01_CC_c0.5_N10000_th10', 'P01_CC_c0.5_N30000', 'P0_CC_c0.5_N1000', 'P0_CC_c0.5_N10000',
                                      'sham_CC_c0.5_N1000', 'sham_CC_c0.5_N10000', 'ref_CC_c0.5_N1000', 'ref_CC_c0.5_N10000'])
    T['pres'] = pres_md(cells, [k for k in main if k in cells])
    T['support'] = {k: support_md(cells[k]) + '\n\n' + fair_md(cells[k]) for k in main if k in cells}
    if os.path.exists(os.path.join(OUT, 'reduced.json')):
        T['reduced'] = reduced_md(json.load(open(os.path.join(OUT, 'reduced.json'))))
    lots = []
    for fn in sorted(glob.glob(os.path.join(OUT, 'lottery_*.json.gz'))):
        import gzip
        d = json.load(gzip.open(fn) if fn.endswith('.gz') else open(fn))
        lots.append(lottery_summary(d))
    T['lottery'] = lottery_md(lots) if lots else ''
    T['lottery_sums'] = lots
    # N-scaling: fair log-odds
    sc = []
    for arm in ('P01', 'ref', 'sham'):
        for N in (100, 1000, 10000, 30000):
            k = '%s_CC_c0.5_N%d' % (arm, N)
            if k in cells:
                p = cells[k]['summary']['fair']
                sc.append((arm, N, p, float(np.log(p / (1 - p)))))
    T['scaling'] = sc
    return T


def write_md(template):
    """runs/concessions.md from a prose template with {{key}} / {{support:cell}} placeholders, and
    runs/concessions.json (chain summaries, basin rates, preservation, lottery summaries, reduced chains)."""
    T = all_tables()
    txt = open(template).read()
    import re
    def rep(m):
        k = m.group(1)
        if k.startswith('support:'):
            return T['support'].get(k[8:], '(cell not run)')
        if k == 'scaling':
            return '\n'.join(['| arm | N | fair | log odds |', '|---|---|---|---|'] +
                             ['| %s | %d | %s | %.2f |' % (a, N, f(p, 4), lo) for a, N, p, lo in T['scaling']])
        return T.get(k, '(missing %s)' % k)
    out = re.sub(r'\{\{([^}]+)\}\}', rep, txt)
    open(os.path.join(RUNS, 'concessions.md'), 'w').write(out)
    cells = load_cells()
    J = dict(chain={k: {kk: v[kk] for kk in ('arm', 'enf', 'pool', 'c', 'N', 'theta', 'states', 'core', 'rel_cut_change', 'summary',
                                              'wage_offered', 'wage_paid_both_work', 'mean_payoff', 'efficiency', 'three_role',
                                              'support_size_99', 'basin_rates', 'preservation', 'fair_boss_mass', 'fair_worker_mass',
                                              'fair_exit_by_slot_kind', 'union_mass_in_fair', 'mass_probe_boss', 'support', 'transitions')
                        if kk in v} for k, v in cells.items()},
             lottery=T['lottery_sums'],
             reduced=json.load(open(os.path.join(OUT, 'reduced.json'))) if os.path.exists(os.path.join(OUT, 'reduced.json')) else None,
             fairshare=json.load(open(os.path.join(OUT, 'fairshare.json'))) if os.path.exists(os.path.join(OUT, 'fairshare.json')) else None,
             static='runs/concessions-static.json')
    json.dump(J, open(os.path.join(RUNS, 'concessions.json'), 'w'), indent=1, default=float)


if __name__ == '__main__':
    S = json.load(open(os.path.join(RUNS, 'concessions-static.json')))
    if sys.argv[1] == 'md':
        write_md(sys.argv[2])
    if sys.argv[1] == 'tables':
        T = all_tables()
        for k, v in T.items():
            if k in ('lottery_sums',):
                continue
            print('\n\n#### %s\n' % k)
            if isinstance(v, dict):
                for kk, vv in v.items():
                    print('\n##### %s\n\n%s' % (kk, vv))
            else:
                print(v)
    if sys.argv[1] == 'named':
        print(named_block(S))
        print()
        print(static_md(S))
        for arm in ('P01', 'P0'):
            print('\n#### Named states, %s (CC, c = 0.5)\n' % arm)
            print(states_md(S, arm))
