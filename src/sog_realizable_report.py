"""Report for the social organization game over the realizable language: aggregates runs/sog_realizable/cell_*.json,
the static, validation, gap, cost, audit and chain outputs into runs/sog-realizable.md and runs/sog-realizable.json.

    python3 src/sog_realizable_report.py
Run-level uncertainty only (notes §1.3.7): Wilson intervals on run-level outcomes, bootstrap over runs for run-level
means of island fractions.
"""
import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, 'runs')
OUT = os.path.join(RUNS, 'sog_realizable')
CELLS = ['L', 'U', 'X', 'L200', 'L256', 'RR', 'RRexec', 'Lmil', 'forcedD*', 'forcedD*2', 'L+WF*', 'Lmil+WF*', 'Lmil-ablate']
LABEL = {'L': 'L (100, 64)', 'U': 'U (100, 64)', 'X': 'expanded syntax (100, 64)', 'L200': 'L (200, 64)', 'L256': 'L (100, 256)',
         'RR': 'RR, realizable semantics', 'RRexec': 'RR, executed probes (extra)', 'Lmil': 'L, militants in numbers',
         'forcedD*': 'forced D* (Lmil workers)', 'forcedD*2': 'forced D*2 (Lmil workers)', 'L+WF*': 'L + synthetic faker WF*',
         'Lmil+WF*': 'Lmil + WF*', 'Lmil-ablate': 'Lmil, concessions ablated'}


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def boot(x, B=2000, seed=0):
    x = np.asarray(x, float)
    if len(x) == 0: return (float('nan'), float('nan'), float('nan'))
    rng = np.random.default_rng(seed)
    m = rng.choice(x, (B, len(x))).mean(1)
    return (float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def cell_summary(d):
    runs = d['runs']
    n = len(runs)
    est = [r['established'] for r in runs]
    est200 = [r['established'] and r['est_gen'] is not None and r['est_gen'] <= 200 for r in runs]
    out = dict(runs=n, closed=sum(1 for r in runs if r['status'] == 1),
               stop_gen_median=float(np.median([r['stop_gen'] for r in runs])))
    out['established'] = (sum(est), wilson(sum(est), n))
    out['established_by_200'] = (sum(est200), wilson(sum(est200), n))
    eg = [r['est_gen'] for r in runs if r['established']]
    out['est_gen_median'] = float(np.median(eg)) if eg else None
    out['persistence'] = boot([r['persistence'] for r in runs])
    out['persistence10'] = boot([r['persistence10'] for r in runs])
    for k in ('fair', 'intermediate', 'zero wage', 'strike', 'scab split', 'repression:strike', 'repression:source'):
        out['plural ' + k] = boot([r['plural_frac'][k] for r in runs])
    uni = [r['e3_universal_fair'] for r in runs]
    out['e3_universal_fair'] = (sum(uni), wilson(sum(uni), n))
    e3keys = sorted(set(k for r in runs for k in r['e3']))
    out['e3_mean'] = {k: float(np.mean([r['e3'].get(k, 0.0) for r in runs])) for k in e3keys}
    out['cross_fair'] = boot([r['cross_fair'] for r in runs])
    out['three_role'] = boot([r['three_role'] for r in runs])
    out['mean_payoffs'] = np.mean([r['mean_payoffs'] for r in runs], axis=0).round(4).tolist()
    # time series (every 100 generations)
    for key in ('boss_masks_t', 'worker_masks_t'):
        names = runs[0][key].keys()
        out[key] = {nm: np.mean([r[key][nm] for r in runs], axis=0).round(4).tolist() for nm in names}
    out['fair_t'] = np.mean([r['fair_t'] for r in runs], axis=0).round(4).tolist()
    out['zero_t'] = np.mean([r['zero_t'] for r in runs], axis=0).round(4).tolist()
    # residence and exits
    res = [x for r in runs for x in r['residence']]
    out['fair_islands_ever'] = len(res)
    out['residence_median_uncensored'] = float(np.median([t for t, c in res if not c])) if any(not c for t, c in res) else None
    out['residence_censored'] = sum(1 for t, c in res if c)
    ex = [e for r in runs for e in r['exits']]
    kinds = {}
    for e in ex:
        kinds[e['kind']] = kinds.get(e['kind'], 0) + 1
    out['exits'] = dict(n=len(ex), kinds=kinds, militant_lost=sum(1 for e in ex if e['militant_lost']))
    # occupancy decomposition
    if 'occupied' in runs[0]:
        occ = np.array([o for r in runs for o in r['occupied']]); es = np.array([e for r in runs for e in r['est_given_occ']])
        out['occupancy'] = dict(occupied_frac=float(occ.mean()), est_given_occ=float(es[occ].mean()) if occ.any() else None,
                                est_given_not_occ=float(es[~occ].mean()) if (~occ).any() else None,
                                runs_with_occupied_island=sum(1 for r in runs if any(r['occupied'])))
    out['nmig_median'] = float(np.median([r['nmig'] for r in runs]))
    return out


def fmt_ci(t, nd=3):
    if t is None: return '–'
    if isinstance(t, tuple) and len(t) == 3:
        return '%.*f [%.*f, %.*f]' % (nd, t[0], nd, t[1], nd, t[2])
    return str(t)


def main():
    out = {}
    lines = ['# The social organization game over the realizable language: run report', '',
             'Spec `specs/2026-10-10-sog-realizable.md`; notes `notes/sog-realizable.md`; predictions',
             '`predictions/2026-10-10-sog-realizable.md`. Generated by `src/sog_realizable_report.py`.', '']
    for f, key in (('sog-realizable-static.json', 'static'), ('sog-realizable-validate.json', 'validate'),
                   ('sog-realizable-gap.json', 'gap'), ('sog-realizable-costs.json', 'costs'),
                   ('sog-realizable-audit.json', 'audit'), ('sog-realizable-chain.json', 'chain'),
                   ('sog-realizable-assays.json', 'assays'), ('sog-realizable-modal.json', 'modal')):
        p = os.path.join(RUNS, f)
        if os.path.exists(p):
            out[key] = json.load(open(p))
    cells = {}
    for c in CELLS:
        p = os.path.join(OUT, 'cell_%s.json' % c.replace('*', 'star'))
        if os.path.exists(p):
            cells[c] = cell_summary(json.load(open(p)))
    out['cells'] = cells
    lines += ['## Lottery cells (40 runs each; ideal table; N per slot, I islands, mN = 1, horizon 2,000)', '',
              '| cell | established (Wilson) | by gen 200 | median est. gen | persistence (boot) | zero-wage plurality | intermediate | E3 universal fair | cross-island P(fair) | three-role |',
              '|---|---|---|---|---|---|---|---|---|---|']
    for c, s in cells.items():
        e, ci = s['established']; e2, ci2 = s['established_by_200']
        lines.append('| %s | %d/%d [%.2f, %.2f] | %d | %s | %s | %s | %s | %d/%d | %s | %s |' % (
            LABEL.get(c, c), e, s['runs'], ci[0], ci[1], e2, s['est_gen_median'], fmt_ci(s['persistence']),
            fmt_ci(s['plural zero wage']), fmt_ci(s['plural intermediate']), s['e3_universal_fair'][0], s['runs'],
            fmt_ci(s['cross_fair']), fmt_ci(s['three_role'])))
    lines += ['', '### Composition over time (run-level means; generations 0, 100, …, 2,000)', '']
    for c, s in cells.items():
        lines.append('- **%s**: fair-island fraction %s; concession bosses %s; militant class %s; scab %s; striker %s' % (
            LABEL.get(c, c), s['fair_t'], s['boss_masks_t']['concession'], s['worker_masks_t']['militant (T1 class)'],
            s['worker_masks_t']['scab'], s['worker_masks_t']['striker']))
    lines += ['', '### Occupancy, residence and exits', '']
    for c, s in cells.items():
        lines.append('- **%s**: occupancy %s; fair islands ever %d, residence median (uncensored) %s gens, censored %d; exits %s; mean payoffs (B, W1, W2) %s; closed %d/%d (median stop %s)' % (
            LABEL.get(c, c), s.get('occupancy'), s['fair_islands_ever'], s['residence_median_uncensored'], s['residence_censored'],
            s['exits'], s['mean_payoffs'], s['closed'], s['runs'], s['stop_gen_median']))
    if 'assays' in out:
        lines += ['', '## Migration-off residence assays (forced D* vs D*2)', '', '```', json.dumps(out['assays'], indent=1)[:4000], '```']
    if 'chain' in out:
        ch = out['chain']
        lines += ['', '## Diagnostic chain (N = %g, theta = %g)' % (ch['N'], ch['theta']), '',
                  '- summary: %s' % json.dumps(ch['summary']), '- wage offered: %s' % json.dumps(ch['wage_offered']),
                  '- states %d (core %d), strict NE %d, rel. cut %.3g, outcome-changing cut %.3g' % (ch['states'], ch['core'], ch['strict_ne'], ch['rel_cut'], ch['rel_cut_change']),
                  '- fair exits by slot/kind: %s' % json.dumps(ch['fair_exit_by_slot_kind']),
                  '- cut diagnostic: %s' % json.dumps(ch['cut_diagnostic']), '', 'Top support:', '']
        for z in ch['support'][:12]:
            lines.append('  - %.4f %s | %s | %s' % (z['pi'], z['summary'], z['play'], z['state']))
        lines += ['', 'Transitions of the top states:', '']
        for z in ch['transitions'][:6]:
            lines.append('  - %.4f %s: %s; outcome-changing %s' % (z['pi'], z['state'], json.dumps(z['exit_by_kind']), json.dumps(z['outcome_changing'])))
    for key in ('costs', 'audit', 'modal'):
        if key in out:
            lines += ['', '## %s' % key, '', '```', json.dumps(out[key], indent=1, default=str)[:6000], '```']
    json.dump(out, open(os.path.join(RUNS, 'sog-realizable.json'), 'w'), indent=1, default=str)
    open(os.path.join(RUNS, 'sog-realizable.md'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
