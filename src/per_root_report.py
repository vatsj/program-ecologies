"""Report for the per-root run: runs/per-root.json and runs/per-root.md.

  python3 src/per_root_report.py
"""
import os
import sys
import json
import glob
import gzip
from collections import defaultdict, Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import per_root as PR

OUT = PR.OUT
ROOT = PR.ROOT
FLD = os.path.join(ROOT, 'runs', 'founding_legibility')
CCD = os.path.join(ROOT, 'runs', 'coverage_components')
SFD = os.path.join(ROOT, 'runs', 'sog_full')
DEV, CONF, CONF2 = list(range(20)), list(range(20, 40)), list(range(40, 60))


def load(cell, root=OUT):
    out = {}
    for f in sorted(glob.glob(os.path.join(root, 'cell_' + cell, 'rep_*.json'))):
        if '.tmp' in f: continue
        a = json.load(open(f))
        out[a['rep']] = a
    return out


def cell_runs(name):
    """{rep: run json} for a reported cell, merging stored references: R0_i = reruns + stored Ni; Hfull_i = stored
    CC Hfull (60); Hfull_6 = stored parent H_eq (0-39) + reruns."""
    if name == 'R0_i':
        d = {r: a for r, a in load('Ni', FLD).items()}
        d.update(load('R0_i'))
        return d
    if name == 'Hfull_i':
        return load('Hfull', CCD)
    if name == 'Hfull_6':
        d = load('H_eq', SFD)
        d.update(load('Hfull_6'))
        return d
    return load(name)


def fair(a, gen='end'):
    if gen == 'end':
        return a['summary_ext'].get('at_10000', a['summary_ext']['end'])['persistence'] \
            if 'at_10000' in a['summary_ext'] else a['summary_ext']['end']['persistence']
    return a['summary']['h']['persistence']


def wage(a):
    s = a['summary_ext']
    return s['at_10000']['wage'] if 'at_10000' in s else s['end']['wage']


def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def boot(x, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    if len(x) == 0: return (None, None)
    m = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(n)]
    return (float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def mcnemar(a, b):
    """Exact two-sided McNemar p on paired binary outcomes."""
    from math import comb
    n01 = sum(1 for x, y in zip(a, b) if x and not y)
    n10 = sum(1 for x, y in zip(a, b) if y and not x)
    n = n01 + n10
    if n == 0: return 1.0
    k = min(n01, n10)
    p = 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, p)


def summarize_cell(runs, reps):
    rs = [r for r in reps if r in runs]
    if not rs: return None
    fe = [fair(runs[r]) for r in rs]
    f2 = [fair(runs[r], 2000) for r in rs]
    w = np.array([wage(runs[r]) for r in rs])
    anyf = [x > 0 for x in fe]
    out = dict(n=len(rs), fair_end=float(np.mean(fe)), fair_end_ci=boot(fe), fair_2000=float(np.mean(f2)),
               runs_any_fair=int(sum(anyf)), runs_any_fair_wilson=wilson(sum(anyf), len(rs)),
               runs_half_fair=int(sum(x >= 0.5 for x in fe)),
               zero_wage=float(w[:, 0].mean()), quarter_wage=float(w[:, 1].mean()), half_wage=float(w[:, 2].mean()))
    ws = [runs[r]['pr']['wage_states'] for r in rs if 'pr' in runs[r]]
    if ws:
        out['occupancy'] = np.mean([x['occupancy'] for x in ws], axis=0).round(4).tolist()
        out['transitions'] = np.sum([x['transitions'] for x in ws], axis=0).tolist()
        out['losses'] = int(sum(x['losses'] for x in ws)); out['regrowths'] = int(sum(x['regrowths'] for x in ws))
        out['mean_0_end'] = float(np.mean([x['mean_0_end'] for x in ws]))
        out['mean_2000_end'] = float(np.mean([x['mean_2000_end'] for x in ws]))
        ff = [x['first_half_after20'] for x in ws if x['first_half_after20'] is not None]
        out['first_half_after20_median'] = float(np.median(ff)) if ff else None
    tr = [runs[r]['pr']['traj'] for r in rs if 'pr' in runs[r]]
    if tr:
        out['traj'] = {k: float(np.mean([t[k] for t in tr if k in t])) for k in tr[0]}
    return out


def contrast(ra, rb, reps):
    rs = [r for r in reps if r in ra and r in rb]
    if not rs: return None
    d = [fair(ra[r]) - fair(rb[r]) for r in rs]
    a = [fair(ra[r]) > 0 for r in rs]; b = [fair(rb[r]) > 0 for r in rs]
    return dict(n=len(rs), diff=float(np.mean(d)), ci=boot(d), mcnemar_p=mcnemar(a, b),
                identical=int(sum(1 for r in rs if fair(ra[r]) == fair(rb[r]))))


def prod_stats(runs, reps):
    rs = [r for r in reps if r in runs and runs[r].get('pr', {}).get('kernel_end')]
    if not rs: return None
    out = {}
    for role in ('boss', 'worker'):
        agg = Counter()
        for r in rs:
            agg.update(runs[r]['pr']['kernel_end'][role])
        ex = sum(runs[r]['pr']['kernel_end']['executed_encounters'] for r in rs)
        out[role] = {k: v / len(rs) for k, v in agg.items()}
        out[role + '_per_executed_encounter'] = {k: agg[k] / max(ex, 1) for k in ('attempts', 'found', 'none',
                                                                                'valid', 'invalid', 'valTO',
                                                                                'marked', 'found_alt')}
    out['executed_encounters'] = float(np.mean([runs[r]['pr']['kernel_end']['executed_encounters'] for r in rs]))
    out['mark'] = {k: float(np.mean([runs[r]['pr']['kernel_end']['mark'][k] for r in rs]))
                   for k in runs[rs[0]]['pr']['kernel_end']['mark']}
    for tag in ('held_200', 'held_2000', 'held_end'):
        h = [runs[r]['pr'][tag] for r in rs if runs[r]['pr'].get(tag)]
        if h:
            out[tag] = {role: dict(scripts_per_set=np.mean([x[role]['scripts_per_set'] for x in h], axis=0).round(3).tolist(),
                                   holding={k: float(np.mean([x[role]['holding'].get(k, 0) for x in h]))
                                            for k in ('first', 'perroot', 'alt')}) for role in ('B', 'W')}
    c = [runs[r]['pr']['cost_end'] for r in rs if runs[r]['pr'].get('cost_end', {}).get('n')]
    if c:
        out['cost'] = {}
        for tag in ('all', 'after50', 'before50'):
            cc = [x[tag] for x in c if tag in x]
            if cc:
                out['cost'][tag] = {k: float(np.median([x[k] for x in cc])) for k in ('median', 'p90', 'p99',
                                                                                       'cumulative', 'val_share_nonplay')}
    acq = [runs[r]['pr'].get('acquisition', {}) for r in rs]
    out['acquisition_median'] = {k: float(np.median([a[k] for a in acq if k in a])) for k in
                                 ('W:perroot', 'W:alt', 'B:perroot', 'B:alt') if any(k in a for a in acq)}
    out['acquisition_by_gen10'] = {k: int(sum(1 for a in acq if k in a and a[k] <= 10)) for k in
                                   ('W:perroot', 'W:alt', 'B:perroot')}
    out['runs'] = len(rs)
    out['ntypes'] = np.mean([runs[r]['pr']['ntypes'] for r in rs], axis=0).tolist()
    out['minutes'] = float(np.median([sum(runs[r]['time'].values()) / 60 for r in rs]))
    return out


def fairboss(runs, reps):
    rs = [r for r in reps if r in runs and 'pr' in runs[r]]
    if not rs: return None
    gens = list(runs[rs[0]]['pr']['fair_bosses'].keys())
    ext = []
    for r in rs:
        fb = runs[r]['pr']['fair_bosses']
        e = next((int(g) for g in gens if int(g) >= 10 and fb[g] == 0), None)
        ext.append(e)
    return dict(mean_islands={g: float(np.mean([runs[r]['pr']['fair_bosses'][g] for r in rs])) for g in gens},
                extinct_by_200=int(sum(1 for e in ext if e is not None and e <= 200)),
                extinction_gen=ext, runs=len(rs))


def nuclei_stats(runs, reps):
    rs = [r for r in reps if r in runs]
    out = dict(regrowing=0, nuclei=0, with_perroot=0, with_alt=0, with_both=0, with_neither=0, pivotal=Counter(),
               examples=[])
    for r in rs:
        a = runs[r]
        nu = a['pr']['nuclei'] if 'pr' in a else a.get('cc', {}).get('regrowth')
        if not nu or not nu.get('regrows'): continue
        out['regrowing'] += 1
        if not nu['nuclei'] or 'pivotal' not in nu['nuclei'][0]: continue
        n0 = nu['nuclei'][0]
        out['nuclei'] += 1
        cls = set(p.get('prov', p.get('label')) for p in n0['pivotal'])
        pr_, al = 'perroot' in cls, 'alt' in cls
        out['with_perroot'] += pr_ and not al; out['with_alt'] += al and not pr_
        out['with_both'] += pr_ and al; out['with_neither'] += not (pr_ or al)
        for p in n0['pivotal']:
            out['pivotal'][(p.get('prov', '-'), p.get('label'), p.get('role', '?'))] += 1
        if len(out['examples']) < 4:
            out['examples'].append(dict(rep=r, gen=n0['gen'], members=[(m['spelling'], m['holder']) for m in n0['members']],
                                        pivotal=[(p['role'], p['set'], p['pos'] if 'pos' in p else None,
                                                  p.get('prov'), p.get('label')) for p in n0['pivotal']]))
    out['pivotal'] = {'%s|%s|%s' % k: v for k, v in out['pivotal'].items()}
    return out


REPORT_CELLS = ['R0_i', 'R0alt_i', 'R1_i', 'R2_i', 'R3k2_i', 'R3k3_i', 'R3k2f_i', 'Hfull_i',
                'R0_3', 'R2_3', 'R2d_3', 'R3k2_3', 'R3k3_3', 'R3k2f_3', 'Hfull_3',
                'R0_6', 'R2_6', 'R3k2_6', 'R3k3_6', 'R3k2f_6', 'Hfull_6', 'R2_i_N200', 'R2b_i', 'R2w_i']


def main():
    out = dict(cells={}, contrasts={}, production={}, nuclei={}, fair_bosses={}, replays={})
    runs = {c: cell_runs(c) for c in REPORT_CELLS}
    runs = {c: v for c, v in runs.items() if v}
    for c, rr in runs.items():
        for tag, reps in (('dev', DEV), ('conf', CONF), ('conf40-59', CONF2), ('conf20-59', CONF + CONF2), ('all', DEV + CONF + CONF2)):
            s = summarize_cell(rr, reps)
            if s: out['cells']['%s|%s' % (c, tag)] = s
        for tag, reps in (('dev', DEV), ('conf', CONF)):
            p = prod_stats(rr, reps)
            if p: out['production']['%s|%s' % (c, tag)] = p
            n = nuclei_stats(rr, reps)
            if n['regrowing']: out['nuclei']['%s|%s' % (c, tag)] = n
            fb = fairboss(rr, reps)
            if fb: out['fair_bosses']['%s|%s' % (c, tag)] = fb
    pairs = [('R2_i', 'R0_i'), ('R2_i', 'Hfull_i'), ('R1_i', 'R0_i'), ('R2_i', 'R1_i'), ('R0alt_i', 'R0_i'),
             ('R3k2_i', 'R2_i'), ('R3k3_i', 'R2_i'), ('R3k2f_i', 'R2_i'), ('R3k2f_i', 'R3k2_i'),
             ('R2_3', 'R0_3'), ('R2_3', 'Hfull_3'), ('R2d_3', 'R2_3'), ('R3k2_3', 'R2_3'),
             ('R2_6', 'R0_6'), ('R2_6', 'Hfull_6'), ('R2_3', 'R2_i'), ('Hfull_3', 'Hfull_i')]
    for a, b in pairs:
        if a in runs and b in runs:
            for tag, reps in (('dev', DEV), ('conf', CONF), ('conf40-59', CONF2), ('conf20-59', CONF + CONF2)):
                c = contrast(runs[a], runs[b], reps)
                if c and c['n']: out['contrasts']['%s - %s|%s' % (a, b, tag)] = c
    # interaction of the factorial (per run): (R2 - R1) - (R0alt - R0)
    if all(c in runs for c in ('R2_i', 'R1_i', 'R0alt_i', 'R0_i')):
        for tag, reps in (('dev', DEV), ('conf', CONF)):
            rs = [r for r in reps if all(r in runs[c] for c in ('R2_i', 'R1_i', 'R0alt_i', 'R0_i'))]
            if rs:
                d = [fair(runs['R2_i'][r]) - fair(runs['R1_i'][r]) - fair(runs['R0alt_i'][r]) + fair(runs['R0_i'][r])
                     for r in rs]
                out['contrasts']['interaction|' + tag] = dict(n=len(rs), diff=float(np.mean(d)), ci=boot(d))
    # role-split diagnostics on the seven streams where R2 was fair, against R2 on the same streams
    diag = (3, 5, 9, 14, 15, 16, 18)
    for c in ('R2b_i', 'R2w_i', 'R2_i', 'R1_i', 'Hfull_i'):
        if c in runs:
            v = {r: fair(runs[c][r]) for r in diag if r in runs[c]}
            out.setdefault('diagnostics', {})[c] = dict(fair=v, n_half=sum(1 for x in v.values() if x >= 0.5))
    # 20,000-generation extensions
    for c in ('R2_i_ext20k', 'Hfull_i_ext20k'):
        rr = load(c)
        out.setdefault('extensions', {})[c] = {r: dict(at_10000=a['summary_ext']['at_10000']['persistence'],
                                                       at_20000=a['summary_ext']['end']['persistence'])
                                              for r, a in rr.items()}
    # replays
    for d in sorted(glob.glob(os.path.join(OUT, 'cell_*_bar_*'))):
        tag = os.path.basename(d)[5:]
        base = tag.split('_bar_')[0]
        rr = load(tag)
        orig = runs.get(base, {})
        out['replays'][tag] = [dict(rep=r, fair_end=fair(a), orig_fair_end=fair(orig[r]) if r in orig else None,
                                    regrows=a['pr']['nuclei']['regrows'], barred=a['pr']['cfg'].get('barred'))
                               for r, a in rr.items()]
    for f, k in (('per-root-static.json', 'static'), ('per-root-traces.json', 'traces'),
                 ('per-root-audit.json', 'audit'), ('per-root-validate.json', 'validate')):
        p = os.path.join(ROOT, 'runs', f)
        if os.path.exists(p): out[k] = json.load(open(p))
    json.dump(out, open(os.path.join(ROOT, 'runs', 'per-root.json'), 'w'), indent=1, default=str)
    write_md(out)


def fmt(x, nd=3):
    if x is None: return '–'
    if isinstance(x, float): return ('%.' + str(nd) + 'f') % x
    return str(x)


def write_md(out):
    L = ['# Per-root production: run summary (`src/per_root_report.py`)', '',
         'Fair share = fraction of islands fair at generation 10,000 (terminal); runs = runs with any fair island; '
         'development = streams 0–19, confirmation = 20–39 (and 40–59 where run). ε = 0 lottery at (100, 64), mN = 1, finite horizon.', '',
         '| cell | streams | n | fair (10,000) [95%] | runs > 0 | runs ≥ ½ | fair (2,000) | mean 2,000–10,000 | zero wage | ¼ wage |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for k, s in out['cells'].items():
        c, tag = k.split('|')
        if tag == 'all': continue
        ci = s['fair_end_ci']
        L.append('| %s | %s | %d | %s [%s, %s] | %d | %d | %s | %s | %s | %s |' % (
            c, tag, s['n'], fmt(s['fair_end']), fmt(ci[0], 2), fmt(ci[1], 2), s['runs_any_fair'], s['runs_half_fair'],
            fmt(s['fair_2000']), fmt(s.get('mean_2000_end')), fmt(s['zero_wage'], 2), fmt(s['quarter_wage'], 2)))
    L += ['', '## Paired contrasts (fair share at 10,000)', '', '| contrast | streams | n | Δ [95%] | McNemar p | identical runs |',
          '|---|---|---|---|---|---|']
    for k, c in out['contrasts'].items():
        nm, tag = k.split('|')
        L.append('| %s | %s | %d | %s [%s, %s] | %s | %s |' % (nm, tag, c['n'], fmt(c['diff']), fmt(c['ci'][0], 2),
                                                               fmt(c['ci'][1], 2), fmt(c.get('mcnemar_p'), 3),
                                                               c.get('identical', '–')))
    L += ['', '## Production and cost', '']
    for k, p in out['production'].items():
        L.append('- **%s**: executed encounters %.3g; minutes %.1f; worker per executed encounter %s; boss %s; '
                 'mark %s; cost %s; held at 10,000 %s; acquisition %s (by gen 10: %s)' % (
                     k, p['executed_encounters'], p['minutes'],
                     {a: round(b, 3) for a, b in p['worker_per_executed_encounter'].items()},
                     {a: round(b, 3) for a, b in p['boss_per_executed_encounter'].items()},
                     {a: round(b) for a, b in p['mark'].items()}, json.dumps(p.get('cost', {})),
                     json.dumps(p.get('held_end', {})), p['acquisition_median'], p['acquisition_by_gen10']))
    L += ['', '## Nuclei', '']
    for k, n in out['nuclei'].items():
        L.append('- **%s**: regrowing %d, nuclei %d; per-root only %d, alternative only %d, both %d, neither %d; '
                 'pivotal %s' % (k, n['regrowing'], n['nuclei'], n['with_perroot'], n['with_alt'], n['with_both'],
                                 n['with_neither'], n['pivotal']))
        for e in n['examples']:
            L.append('  - rep %d gen %d: %s; pivotal %s' % (e['rep'], e['gen'], e['members'], e['pivotal']))
    L += ['', '## Fair bosses (islands with a present boss paying ½ to the modal worker pair)', '']
    for k, fb in out['fair_bosses'].items():
        L.append('- **%s**: %s; extinct by 200 in %d/%d runs' % (k, {a: round(b, 1) for a, b in fb['mean_islands'].items()},
                                                                fb['extinct_by_200'], fb['runs']))
    if out['replays']:
        L += ['', '## Replays', '']
        for k, v in out['replays'].items():
            L.append('- **%s**: %s' % (k, [(x['rep'], x['orig_fair_end'], x['fair_end'], x['regrows']) for x in v]))
    if out.get('diagnostics'):
        L += ['', '## Role-split diagnostics (streams 3, 5, 9, 14, 15, 16, 18)', '']
        for c, d in out['diagnostics'].items():
            L.append('- **%s**: runs ≥ ½ fair %d/7; %s' % (c, d['n_half'], {k: round(v, 2) for k, v in d['fair'].items()}))
    if out.get('extensions'):
        L += ['', '## Extensions to 20,000', '']
        for c, d in out['extensions'].items():
            L.append('- **%s**: %s' % (c, {k: (round(v['at_10000'], 2), round(v['at_20000'], 2)) for k, v in d.items()}))
    open(os.path.join(ROOT, 'runs', 'per-root.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
