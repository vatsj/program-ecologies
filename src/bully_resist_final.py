"""Assembles runs/bully-resistance.md and runs/bully-resistance.json (queue 76) from the pieces: step-1 gates, step 0, step 2, step 3 rows.

    python3 src/bully_resist_final.py [--out runs/bully-resistance]

Tolerates missing parts (prints what it has).  Verdict inputs follow the scoring rules of predictions/2026-11-08-bully-resistance.md.
"""
import os, sys, json, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import bully_resist_report as RPT

DELTAS = RPT.DELTAS


def cell(cs, arm, beta, N, I, d, extra='', long=False):
    return cs.get((arm, beta, N, I, d, extra, long))


def fm(c):
    return '%.2f [%.2f, %.2f]' % (c['mean'], c['ci'][0], c['ci'][1]) if c else '-'


def dstar_text(ds):
    if ds['status'] == 'incomplete':
        return 'incomplete'
    if ds['status'] == 'none':
        return 'none' + (' (isolated pass at %s)' % ', '.join('%g' % x for x in ds['isolated']) if ds.get('isolated') else '')
    return '(%s, %g]%s' % ('%g' % ds['lower'] if ds['lower'] else '< 3e-4', ds['upper'], ' non-monotone' if ds.get('nonmonotone') else '')


def series_table(cs, arms, betas, N, I, extra=''):
    L = []
    for beta in betas:
        L.append('N = %d, I = %d, beta = %s: V* share at 120N (mean over 20 runs [95%% bootstrap over runs]; share of runs with every island fair)' % (N, I, beta))
        L.append('')
        L.append('| arm | ' + ' | '.join('%g' % d for d in DELTAS) + ' | delta* |')
        L.append('|---|' + '---|' * (len(DELTAS) + 1))
        for arm in arms:
            cells = [cell(cs, arm, beta, N, I, d, extra) for d in DELTAS]
            if not any(cells):
                continue
            ds = RPT.delta_star({k: v for k, v in cs.items()}, arm, beta, N, I) if not extra else dict(status='incomplete')
            L.append('| %s | ' % arm + ' | '.join(('%s; %.2f' % (fm(c), c['all_fair'])) if c else '-' for c in cells) + ' | %s |' % dstar_text(ds))
        L.append('')
    return L


def build_verdict_inputs(cs, step0, step2rep, lps):
    v = {}
    # --- RE 2, RE 3, E2
    def ds(arm, beta, N, I=64):
        return RPT.delta_star(cs, arm, beta, N, I)
    v['dstar'] = {}
    for arm in ('F', 'P', 'O', 'PO', 'FPO'):
        for beta in (1.0, 3.0):
            for N in (100, 200, 400):
                d = ds(arm, beta, N)
                if d['status'] != 'incomplete':
                    v['dstar']['%s|%s|%d|64' % (arm, beta, N)] = d
    for arm in ('F', 'P', 'PO'):
        for beta in (1.0, 3.0):
            d = RPT.delta_star(cs, arm, beta, 200, 256)
            if d['status'] != 'incomplete':
                v['dstar']['%s|%s|200|256' % (arm, beta)] = d
    g = lambda a, b, n: v['dstar'].get('%s|%s|%d|64' % (a, b, n))
    if g('P', 3.0, 200):
        v['RE2_holds'] = g('P', 3.0, 200)['status'] == 'bracket'
    if g('O', 3.0, 200):
        v['RE3_holds'] = g('O', 3.0, 200)['status'] == 'none'
    if all(g('P', 3.0, n) for n in (100, 200, 400)):
        v['E2_holds'] = all(g('P', 3.0, n)['status'] == 'none' for n in (100, 200, 400))
    # --- E3: Q vs P at beta 3, N = 200
    qs = [(cell(cs, 'Q', 3.0, 200, 64, d), cell(cs, 'P', 3.0, 200, 64, d)) for d in DELTAS]
    if all(a and b for a, b in qs):
        below = sum(1 for a, b in qs if a['mean'] < b['mean'])
        v['E3'] = dict(q_below_p=below, q_at_or_above_p=6 - below, holds=below >= 4)
    # --- E8: F2 vs F at beta 0
    fs = [(cell(cs, 'F2', 0.0, 200, 64, d), cell(cs, 'F', 0.0, 200, 64, d)) for d in DELTAS]
    if all(a and b for a, b in fs):
        gaps = [abs(a['mean'] - b['mean']) for a, b in fs]
        v['E8'] = dict(gaps=gaps, n_above=sum(1 for x in gaps if x > 0.1), holds=sum(1 for x in gaps if x > 0.1) < 2)
    # --- seeded starts
    seeds = {}
    for arm in ('F', 'P', 'O', 'PO'):
        un = cell(cs, arm, 3.0, 200, 64, 0.03, ':seed=unequal')
        f0 = cell(cs, arm, 0.0, 200, 64, 0.03, ':seed=fair')
        f3 = cell(cs, arm, 3.0, 200, 64, 0.03, ':seed=fair')
        if un and f0 and f3:
            seeds[arm] = dict(entry_hazard=un['mean'], entry_ci=un['ci'], exit_hazard_beta0=1 - f0['mean'], hold_beta0=f0['mean'], hold_beta0_ci=f0['ci'],
                              exit_hazard_beta3=1 - f3['mean'], hold_beta3=f3['mean'])
    v['seeds'] = seeds
    if all(a in seeds for a in ('F', 'P', 'O')):
        v['E7'] = dict(max_entry=max(seeds[a]['entry_hazard'] for a in ('F', 'P', 'O')), min_hold_beta0=min(seeds[a]['hold_beta0'] for a in ('F', 'P', 'O')),
                       holds=max(seeds[a]['entry_hazard'] for a in ('F', 'P', 'O')) < 0.25 and min(seeds[a]['hold_beta0'] for a in ('F', 'P', 'O')) >= 0.8)
        if 'RE2_holds' in v:
            v['sol_a'] = dict(no_threshold=not v['RE2_holds'], entry_hazard_P=seeds['P']['entry_hazard'], hold_beta3_P=seeds['P']['hold_beta3'],
                              value=(not v['RE2_holds']) and seeds['P']['entry_hazard'] < 0.25,
                              establishment_is_channel=(not v['RE2_holds']) and seeds['P']['entry_hazard'] < 0.25 and (1 - seeds['P']['hold_beta3']) < 0.25)
            ub = step0['verdicts'] if step0 else None
            pz_ub = step0['item2_summary']['Pz']['UB']['all']['median'] if step0 else None
            v['argon_b'] = dict(no_threshold=not v['RE2_holds'], P_UB_median=pz_ub, entry_hazard_P=seeds['P']['entry_hazard'],
                                value=(not v['RE2_holds']) and (pz_ub is not None and pz_ub <= 1) and seeds['P']['entry_hazard'] < 0.25)
    # --- RE4 / E5 / E6 from step 2
    if step2rep:
        r0, r2 = step2rep.get('R0'), step2rep.get('R2')
        if r0 and r2:
            v['RE4'] = dict(R0_gap=r0['gap_prudent_any'], R2_gap=r2['gap_prudent_any'], R0_gap_P_z=r0['gap_prudent_z'], R2_gap_P_z=r2['gap_prudent_z'],
                            holds_full=(r0['gap_prudent_any'] >= 10 and r2['gap_prudent_any'] <= 3),
                            falsifier=(r0['gap_prudent_any'] < 6 or r2['gap_prudent_any'] > 6))
            v['E5'] = dict(R2_P_gap=r2['gap_prudent_any'], R2_O_gap=r2['gap_opener'],
                           holds=(5 <= r2['gap_prudent_any'] <= 8) and r2['gap_opener'] >= 12)
        v['E6_masses'] = {mn: dict(P_z=r['prudent_z']['ratio_to_single'], O=r['opener']['ratio_to_single']) for mn, r in step2rep.items()}
    if lps:
        best = max(lps, key=lambda x: x['mean'])
        v['RE5'] = dict(max_cell=best, holds=best['mean'] < 0.9)
        v['E6'] = dict(max_cell=best['mean'], holds=best['mean'] <= 0.6 and all((r['prudent_z']['ratio_to_single'] or 0) < 1 and (r['opener']['ratio_to_single'] or 0) < 1 for r in step2rep.values()) if step2rep else None)
    return v


def lps_cells(cs):
    out = []
    for k, c in cs.items():
        if isinstance(k[0], str) and k[0].startswith('lp:'):
            out.append(dict(machine=k[0].split(':')[1], alloc=k[0].split(':')[2], N=k[2], I=k[3], delta=k[4], mean=c['mean'], ci=c['ci'], all_fair=c['all_fair'], long=k[6]))
    return out


def lps_md(L, lps):
    for mach in ('R0', 'R1', 'R2'):
        for alloc in ('const', 'junk'):
            rows = [c for c in lps if c['machine'] == mach and c['alloc'] == alloc and not c['long']]
            if not rows:
                continue
            for N in (200, 400):
                rr = sorted([c for c in rows if c['N'] == N], key=lambda c: -c['delta'])
                if not rr:
                    continue
                L.append('%s, allocation of unclassified mass to %s, N = %d, I = 64: ' % (mach, 'constants' if alloc == 'const' else 'junk', N) +
                         '; '.join('delta %g: %.2f [%.2f, %.2f]' % (c['delta'], c['mean'], c['ci'][0], c['ci'][1]) for c in rr))
            L.append('')


def main():
    outp = os.path.join(ROOT, 'runs', 'bully-resistance')
    if '--out' in sys.argv:
        outp = sys.argv[sys.argv.index('--out') + 1]
    cs = RPT.build()
    step0 = json.load(open(os.path.join(ROOT, 'runs', 'bully_resist', 'step0_report.json'))) if os.path.exists(os.path.join(ROOT, 'runs', 'bully_resist', 'step0_report.json')) else None
    p2 = os.path.join(ROOT, 'runs', 'bully_resist', 'step2_report.json')
    step2rep = json.load(open(p2)) if os.path.exists(p2) else None
    lps = lps_cells(cs)
    V = build_verdict_inputs(cs, step0, step2rep, lps)
    L = ['# Queue 76: bully-resistant readers in arm T (generated)', '',
         'Finite schedules throughout (mN = 1, Lambda = 100, 100N + 20N generations, 20 runs per cell); thresholds are finite-schedule statistics, not pi.', '']
    p0 = os.path.join(ROOT, 'runs', 'bully_resist', 'step0_report.md')
    if os.path.exists(p0):
        L += open(p0).read().split('\n')
    pm = os.path.join(ROOT, 'runs', 'bully_resist', 'step2_report.md')
    if os.path.exists(pm):
        L += ['', '# Step 2', ''] + open(pm).read().split('\n')
    L += ['', '# Step 3: dynamics', '']
    for N in (100, 200, 400):
        L += series_table(cs, ['F', 'P', 'O', 'PO', 'FPO'], [1.0, 3.0], N, 64)
    L += ['## I = 256, N = 200', '']
    L += series_table(cs, ['F', 'P', 'PO'], [1.0, 3.0], 200, 256)
    L += ['## Variants and controls (N = 200 unless stated)', '']
    L += series_table(cs, ['F', 'F2', 'P', 'O', 'PO'], [0.0], 200, 64)
    L += series_table(cs, ['F2', 'Po', 'Q'], [1.0, 3.0], 200, 64)
    for N in (100, 400):
        L += series_table(cs, ['Q'], [3.0], N, 64)
    L += ['', '## Seeded starts (N = 200, I = 64, delta = 0.03)', '']
    if V.get('seeds'):
        L.append('| arm | entry hazard (seeded unequal, beta 3) [95%] | fair share held, beta 0 | exit hazard, beta 0 | fair share held, beta 3 |')
        L.append('|---|---|---|---|---|')
        for a, s in V['seeds'].items():
            L.append('| %s | %.2f [%.2f, %.2f] | %.2f [%.2f, %.2f] | %.2f | %.2f |' % (a, s['entry_hazard'], s['entry_ci'][0], s['entry_ci'][1], s['hold_beta0'], s['hold_beta0_ci'][0], s['hold_beta0_ci'][1], s['exit_hazard_beta0'], s['hold_beta3']))
    L += ['', '## Charge-suppressed replay (pf = 0, same actions and schedule) and idealized uncapped table (diagnostics), N = 200, I = 64, beta = 3', '']
    for tag, extra in (('A_f charges suppressed', ':pf=0.0'), ('idealized uncapped table', ':tab=ideal')):
        L.append('%s: V* (delta 0.01 / 0.1) against the charged capped cell' % tag)
        L.append('')
        L.append('| arm | beta | V* diagnostic, delta 0.01 | charged capped, 0.01 | V* diagnostic, delta 0.1 | charged capped, 0.1 |')
        L.append('|---|---|---|---|---|---|')
        for arm in ('F', 'P', 'O', 'PO'):
            for beta in (0.0, 3.0):
                a = [cell(cs, arm, beta, 200, 64, d, extra) for d in (1e-2, 1e-1)]
                b = [cell(cs, arm, beta, 200, 64, d) for d in (1e-2, 1e-1)]
                if any(a):
                    L.append('| %s | %s | %s | %s | %s | %s |' % (arm, beta, fm(a[0]), fm(b[0]), fm(a[1]), fm(b[1])))
        L.append('')
    L += ['## Mean A_f charge per capita by family (120N snapshot), N = 200, I = 64, delta = 0.1', '']
    L.append('| arm | beta | reader families present: mean charge [share of capita] |')
    L.append('|---|---|---|')
    for arm in ('P', 'O', 'PO', 'F2'):
        for beta in (0.0, 3.0):
            c = cell(cs, arm, beta, 200, 64, 0.1)
            if c and c.get('charges'):
                L.append('| %s | %s | %s |' % (arm, beta, '; '.join('%s %.3f [%.4f]' % (f, x[0], x[1]) for f, x in c['charges'].items() if f != 'all' and x[1] > 1e-6 and f not in ('c_third', 'c_half', 'c_two3', 'c_grand')) + '; all %.3f' % c['charges']['all']))
    L += ['', '## Transition rates among classes (per island-generation spent in the class), N = 200, I = 64, beta = 3, delta = 0.01', '']
    L.append('| arm | window | F to U | U to F | n F>U | n U>F | fair-pair flips (per fair island-generation) |')
    L.append('|---|---|---|---|---|---|---|')
    for arm in ('F', 'P', 'O', 'PO', 'FPO'):
        c = cell(cs, arm, 3.0, 200, 64, 1e-2)
        if c:
            for win in ('tail|d25', 'chase|d25'):
                t = c['trans'][win]
                L.append('| %s | %s | %.2e | %.2e | %d | %d | %.2e |' % (arm, win, t['F_to_U'] or 0, t['U_to_F'] or 0, t['n_FU'], t['n_UF'], t['FF_flips'] or 0))
    L += ['', '## Length-prior-shaped series (grammar-conditioned projections onto T+ u P u O; both allocations)', '']
    lps_md(L, lps)
    L += ['', '## Verdict inputs', '', '```', json.dumps(V, indent=1, default=str), '```']
    open(outp + '.md', 'w').write('\n'.join(L) + '\n')
    ser = {json.dumps(list(k)): v for k, v in cs.items()}
    json.dump(dict(verdict_inputs=V, cells={k: {kk: vv for kk, vv in c.items() if kk != 'v_by_run'} for k, c in ser.items()}), open(outp + '.json', 'w'), default=str)
    print('\n'.join(L[-60:]))


if __name__ == '__main__':
    main()
