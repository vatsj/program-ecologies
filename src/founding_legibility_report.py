"""Report for the founding-legibility run (notes/founding-legibility.md): aggregates runs/founding_legibility/ and
the parent's stored baselines (runs/sog_full/cell_S_eq, cell_S_eq_ideal) into runs/founding-legibility.json and
runs/founding-legibility.md, with run-level uncertainty and paired contrasts.

  python3 src/founding_legibility_report.py
"""
import os
import sys
import json
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sog_full_report as SR

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RUNS = os.path.join(ROOT, 'runs')
OUT = os.path.join(RUNS, 'founding_legibility')
PARENT = os.path.join(RUNS, 'sog_full')

ORDER = ['S_eq*', 'N6', 'L2_6', 'L1_6', 'L1L2_6', 'N3', 'L1_3', 'L1W_3', 'L1sham_3', 'L1_3_N200', 'S_eq_ideal*', 'Ni',
         'L1_i', 'Heq_i', 'H_noeq_ideal*']
LABEL = {'S_eq*': 'natural, 10⁶ (parent, stored)', 'N6': 'natural, 10⁶ (rerun)', 'L2_6': 'L2 (mark), 10⁶',
         'L1_6': 'L1, 10⁶', 'L1L2_6': 'L1 + L2, 10⁶', 'N3': 'natural, 3·10⁶', 'L1_3': 'L3 = L1, 3·10⁶',
         'L1W_3': 'L1-withheld (gen 10), 3·10⁶', 'L1sham_3': 'L1 + sham, 3·10⁶', 'L1_3_N200': 'L1, 3·10⁶, (200, 64)',
         'S_eq_ideal*': 'natural, ideal (parent, stored)', 'Ni': 'natural, ideal (rerun)', 'L1_i': 'L1, ideal',
         'Heq_i': 'H + eq, ideal (diagnostic)', 'H_noeq_ideal*': 'H + no eq, ideal (parent, stored)'}
PAIRS = [('S_eq*', 'L1_6'), ('S_eq*', 'L2_6'), ('S_eq*', 'L1L2_6'), ('N3', 'L1_3'), ('L1_3', 'L1W_3'),
         ('L1_3', 'L1sham_3'), ('S_eq_ideal*', 'L1_i'), ('S_eq_ideal*', 'Heq_i'), ('S_eq*', 'N3'),
         ('S_eq_ideal*', 'Ni'), ('Ni', 'L1_i'), ('N6', 'L1_6')]


def load(name):
    if name.endswith('*'):
        d = os.path.join(PARENT, 'cell_' + name[:-1])
    else:
        d = os.path.join(OUT, 'cell_' + name)
    if not os.path.isdir(d): return []
    return [json.load(open(os.path.join(d, f))) for f in sorted(os.listdir(d))
            if f.startswith('rep_') and f.endswith('.json')]


def fmt(x, nd=3):
    if x is None: return '–'
    if isinstance(x, (tuple, list)):
        return '[%s]' % ', '.join(fmt(v, 2) for v in x)
    return ('%.' + str(nd) + 'f') % x


def paired(a_reps, b_reps, rng):
    A = {r['rep']: r for r in a_reps}; Bm = {r['rep']: r for r in b_reps}
    common = sorted(set(A) & set(Bm))
    if not common: return None
    pa = [A[k]['summary']['h']['persistence'] for k in common]
    pb = [Bm[k]['summary']['h']['persistence'] for k in common]
    d = np.array(pb) - np.array(pa)
    ea = [A[k].get('summary_ext', {}).get('end', {}).get('persistence') for k in common]
    eb = [Bm[k].get('summary_ext', {}).get('end', {}).get('persistence') for k in common]
    out = dict(n=len(common), mean_a=float(np.mean(pa)), mean_b=float(np.mean(pb)), delta=float(d.mean()),
               ci=SR.boot(d, rng), mcnemar_half=SR.mcnemar([p >= 0.5 for p in pa], [p >= 0.5 for p in pb]),
               runs_half=(sum(p >= 0.5 for p in pa), sum(p >= 0.5 for p in pb)),
               runs_pos=(sum(p > 0 for p in pa), sum(p > 0 for p in pb)),
               identical_runs=sum(1 for x, y in zip(pa, pb) if x == y))
    if all(x is not None for x in ea + eb):
        de = np.array(eb) - np.array(ea)
        out['delta_10000'] = float(de.mean()); out['ci_10000'] = SR.boot(de, rng)
    return out


def fl_stats(reps):
    """The run's own statistics (composition, manipulation checks, founding pass, mark)."""
    F = [r.get('fl') for r in reps if r.get('fl')]
    if not F: return None
    out = {}
    for g in (0, 10, 50, 200):
        k = 'comp_%d' % g
        vals = [f[k] for f in F if k in f]
        if vals:
            out[k] = {c: float(np.mean([v.get(c, 0.0) for v in vals])) for c in ('unconditional', 'open', 'greenbeard')}
            out[k + '_sd'] = {c: float(np.std([v.get(c, 0.0) for v in vals])) for c in ('unconditional', 'open')}
    for g in (10, 50):
        k = 'militant_survival_%d' % g
        vals = [f[k] for f in F if k in f]
        if vals: out[k] = float(np.mean(vals))
    g0 = [f['gen0'] for f in F if f.get('gen0')]
    if g0:
        out['gen0'] = dict(militant_strike_p=float(np.mean([x['militant_strike_p'] for x in g0])),
                           worker_strike_p=float(np.mean([x['worker_strike_p'] for x in g0])),
                           coverage={s: dict(any=float(np.mean([x['coverage'][s]['any'] for x in g0])),
                                             per_set=np.mean([x['coverage'][s]['per_set'] for x in g0], axis=0).tolist())
                                     for s in ('slot0', 'slot1', 'slot2')})
        held = np.sum([x['retention']['held'] for x in g0], axis=0)
        cert = np.sum([x['retention']['certified'] for x in g0], axis=0)
        out['gen0']['retention'] = [[float(cert[s][A] / held[s][A]) if held[s][A] else None for A in range(3)]
                                    for s in range(3)]
    fo = [f['founding'] for f in F if f.get('founding')]
    if fo:
        out['founding'] = dict(
            time_s=float(np.mean([x['time'] for x in fo])),
            steps_median={s: float(np.median([x['steps_s%d' % s]['median'] for x in fo])) for s in range(3)},
            steps_mean={s: float(np.mean([x['steps_s%d' % s]['mean'] for x in fo])) for s in range(3)},
            steps_max=int(max(max(x['steps_s%d' % s]['max'] for s in range(3)) for x in fo)),
            steps_per_island=float(np.mean([x['steps_per_island_mean'] for x in fo])),
            late_worker_acquisitions=int(sum(x['late_worker_acquisitions'] for x in fo)),
            no_triple_workers=int(sum(x['no_triple_workers'] for x in fo)),
            ctr=np.sum([x['ctr'] for x in fo], axis=0).tolist())
    wh = [f['withheld'] for f in F if f.get('withheld')]
    if wh:
        out['withheld'] = dict(moved=int(sum(x['moved'] for x in wh)), examined=int(sum(x['examined'] for x in wh)),
                               runs_with_moves=sum(1 for x in wh if x['moved'] > 0),
                               max_fitness_err=float(max(x['fitness_err'] for x in wh)))
    mk = [f['mark'] for f in F if f.get('mark')]
    if mk:
        MK = np.sum([x['MK'] for x in mk], axis=0)
        out['mark'] = dict(executed_productions=int(MK[10]), skipped=int(MK[5]), skipped_steps=int(MK[6]),
                           sensitive=int(MK[7]), sensitive_bound=int(MK[8]), marks=int(MK[9]),
                           sensitive_rate=float(MK[7] / max(MK[2], 1)), bound_rate=float(MK[8] / max(MK[2], 1)),
                           executed_encounters=int(MK[2]))
        ex = [x['executed'] for x in mk if x.get('executed')]
        if ex:
            out['mark']['executed_cost'] = {k: float(np.median([e[k] for e in ex])) for k in ex[0]}
    mc = [f['mark_cost'] for f in F if f.get('mark_cost')]
    if mc:
        rows = np.array([row for m in mc for row in m['rows']], float)
        late = rows[rows[:, 0] >= 50]
        out['mark_cost'] = dict(
            all=dict(ratio_s3=float(np.median(rows[:, 1] + rows[:, 2]) / max(np.median(rows[:, 1]), 1)),
                     ratio_mark_steady=float(np.median(rows[:, 1] + rows[:, 3]) / max(np.median(rows[:, 1]), 1))),
            late=dict(ratio_s3=float(np.median(late[:, 1] + late[:, 2]) / max(np.median(late[:, 1]), 1)),
                      ratio_mark_steady=float(np.median(late[:, 1] + late[:, 3]) / max(np.median(late[:, 1]), 1))))
    rp = [f['replay'] for f in F if f.get('replay')]
    if rp:
        out['replay'] = dict(failures_recorded=sum(x['failures_recorded'] for x in rp),
                             replays=sum(x['replays'] for x in rp),
                             suppressed_successes=sum(x['suppressed_successes'] for x in rp),
                             examples=[e for x in rp for e in x['examples']][:10])
    return out


def main():
    rng = np.random.default_rng(20261014)
    res = dict(cells={}, fl={}, pairs={})
    reps = {nm: load(nm) for nm in ORDER}
    for nm in ORDER:
        if reps[nm]:
            res['cells'][nm] = SR.cell_stats(nm, reps[nm], rng)
            res['fl'][nm] = fl_stats(reps[nm])
    for a, b in PAIRS:
        if reps.get(a) and reps.get(b):
            res['pairs']['%s -> %s' % (a, b)] = paired(reps[a], reps[b], rng)
    for f in ('static_yield_K1e+06.json', 'assay_isolated_L1.json', 'compare.json', 'replay.json'):
        p = os.path.join(OUT, f)
        if os.path.exists(p):
            d = json.load(open(p))
            if 'rows' in d and isinstance(d['rows'], list) and f.startswith('assay'):
                d = {k: v for k, v in d.items() if k != 'rows'}
            if f.startswith('static'):
                d = {k: v for k, v in d.items() if k != 'reps'}
            res[f.split('.')[0]] = d
    json.dump(res, open(os.path.join(RUNS, 'founding-legibility.json'), 'w'), indent=1, default=str)

    L = ['# Legibility at founding: run report', '',
         'Generated by `src/founding_legibility_report.py` from `runs/founding_legibility/` and the parent\'s stored '
         'cells (marked *). Lottery: (N, I) = (100, 64) unless stated, mN = 1, w = 0.3, horizon 2,000 with every run '
         'extended to 10,000; S-nonself₃ + eq unless stated; ε = 0 evidence at finite (N, I, horizon). Intervals: Wilson '
         '(runs), bootstrap over runs (island fractions). Persistence is all-or-nothing by run.', '',
         '## Cells', '',
         '| cell | runs | established (first check / window) | persistence (2,000) | runs ≥ ½ / > 0 | zero wage | ¼ wage | prod. eff. | persistence (10,000) | prod. eff. (10,000) |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for nm in ORDER:
        c = res['cells'].get(nm)
        if not c: continue
        S = [r['summary'] for r in reps[nm]]
        npos = sum(1 for s in S if s['h']['persistence'] > 0)
        L.append('| %s | %d | %d / %d | %s %s | %d / %d | %s | %s | %s | %s | %s |' % (
            LABEL[nm], c['n'], c['established'], c['established_window'], fmt(c['persistence']),
            fmt(c['persistence_ci']), c['persistence_runs_ge_half'], npos, fmt(c['zero_wage']), fmt(c['quarter_wage']),
            fmt(c['prodeff']), fmt(c.get('ext', {}).get('persistence')), fmt(c.get('ext', {}).get('prodeff'))))
    L += ['', '## Paired contrasts (persistence at 2,000, b − a, same founder streams)', '',
          '| a → b | n | mean a | mean b | Δ [95%] | Δ at 10,000 | runs ≥ ½ (a, b) | runs > 0 (a, b) | McNemar p (≥ ½) | identical runs |',
          '|---|---|---|---|---|---|---|---|---|---|']
    for k, p in res['pairs'].items():
        if not p: continue
        L.append('| %s | %d | %s | %s | %s %s | %s | %s | %s | %.3f | %d |' % (
            k, p['n'], fmt(p['mean_a']), fmt(p['mean_b']), fmt(p['delta']), fmt(p['ci']), fmt(p.get('delta_10000')),
            p['runs_half'], p['runs_pos'], p['mcnemar_half'], p['identical_runs']))
    L += ['', '## The scramble: worker-slot composition (share of worker individuals by class)', '',
          '| cell | gen 0 unc / open | gen 10 unc / open | gen 50 unc / open | gen 200 unc / open | militant spellings alive at 10 / 50 |',
          '|---|---|---|---|---|---|']
    for nm in ORDER:
        f = res['fl'].get(nm)
        if not f or 'comp_10' not in f: continue
        cs = ' | '.join('%s / %s' % (fmt(f['comp_%d' % g]['unconditional']), fmt(f['comp_%d' % g]['open']))
                        if 'comp_%d' % g in f else '–' for g in (0, 10, 50, 200))
        L.append('| %s | %s | %s / %s |' % (LABEL[nm], cs, fmt(f.get('militant_survival_10')),
                                            fmt(f.get('militant_survival_50'))))
    L += ['', '## Manipulation checks at generation 0', '',
          '| cell | founders with a script (B / W1 / W2) | boss sets ≥¼, =½, ≤¼ | worker sets [C], [D] (W1) | militant strike p | worker strike p | retention (B; W1) |',
          '|---|---|---|---|---|---|---|']
    for nm in ORDER:
        f = res['fl'].get(nm)
        if not f or not f.get('gen0'): continue
        g = f['gen0']; cv = g['coverage']
        L.append('| %s | %s / %s / %s | %s | %s | %s | %s | %s; %s |' % (
            LABEL[nm], fmt(cv['slot0']['any']), fmt(cv['slot1']['any']), fmt(cv['slot2']['any']),
            fmt(cv['slot0']['per_set']), fmt(cv['slot1']['per_set']), fmt(g['militant_strike_p']),
            fmt(g['worker_strike_p']), fmt(g['retention'][0]), fmt(g['retention'][1][:2])))
    L += ['', '## The founding pass, the withheld delivery, the mark', '']
    for nm in ORDER:
        f = res['fl'].get(nm)
        if not f: continue
        if f.get('founding'):
            L.append('- **%s** founding pass: %s' % (LABEL[nm], json.dumps(f['founding'])))
        if f.get('withheld'):
            L.append('- **%s** withheld delivery: %s' % (LABEL[nm], json.dumps(f['withheld'])))
        if f.get('mark'):
            L.append('- **%s** mark: %s' % (LABEL[nm], json.dumps(f['mark'])))
        if f.get('mark_cost'):
            L.append('- **%s** cost on population-sampled encounters (median (play + production) / median play): %s'
                     % (LABEL[nm], json.dumps(f['mark_cost'])))
        if f.get('replay'):
            L.append('- **%s** in-cell bare-source replay (first version, own island only; superseded by `replay.json`, '
                     'notes §1.x): %s' % (LABEL[nm], json.dumps({k: v for k, v in f['replay'].items() if k != 'examples'})))
    L += ['', '## Production and costs (the parent\'s sampled-encounter estimator)', '',
          '| cell | TO-changed 0 / 50 / 200 / 2,000 | production outcomes (gen 0) | outcomes (gen 50) | ratio (pooled) |',
          '|---|---|---|---|---|']
    for nm in ORDER:
        c = res['cells'].get(nm)
        if not c or 'encounters' not in c: continue
        e = c['encounters']
        po = lambda g: ', '.join('%s %.2f' % (k, v) for k, v in sorted(e.get(g, {}).get('production_outcomes', {}).items()))
        L.append('| %s | %s | %s | %s | %s |' % (LABEL[nm], ' / '.join(fmt(e[g]['todiff']) if g in e else '–'
                                                                      for g in ('0', '50', '200', '2000')),
                                                 po('0'), po('50'), fmt(c.get('realized_cost', {}).get('ratio'))))
    L += ['', '## Holders of fair islands at 2,000 and exits', '']
    for nm in ORDER:
        c = res['cells'].get(nm)
        if not c: continue
        L.append('- **%s**: fair islands %d; holders %s; exits (n = %d) %s' % (
            LABEL[nm], c['fair_islands_counted'], json.dumps({k: round(v, 3) for k, v in c['holders'].items()}),
            c['exits_n'], json.dumps({k: round(v, 3) for k, v in list(c['exits'].items())[:5]})))
    for key in ('static_yield_K1e+06', 'replay', 'assay_isolated_L1', 'compare'):
        if key in res:
            L += ['', '## %s' % key, '', '```', json.dumps(res[key], default=str)[:6000], '```']
    vf = os.path.join(OUT, 'verdicts.md')
    if os.path.exists(vf):
        L += ['', open(vf).read()]
    open(os.path.join(RUNS, 'founding-legibility.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L[:60]))


if __name__ == '__main__':
    main()
