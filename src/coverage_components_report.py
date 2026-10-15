"""Report for the coverage-components run: runs/coverage-components.json and runs/coverage-components.md.

  python3 src/coverage_components_report.py
"""
import os
import sys
import json
import glob
from collections import defaultdict, Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage_components as CC

OUT = CC.OUT
ROOT = CC.ROOT
STORED = os.path.join(ROOT, 'runs', 'founding_legibility')
ORDER = ['Hfull', 'S3', 'minus_a', 'minus_b', 'minus_c', 'minus_d', 'plus_a', 'plus_b', 'plus_c', 'plus_d',
         'plus_ab', 'plus_cd', 'rminus_a', 'rminus_b', 'rminus_d', 'rminus_c', 'rplus_a', 'rplus_b', 'rplus_d',
         'rplus_c']


def load(cell, root=OUT):
    d = os.path.join(root, 'cell_' + cell)
    out = {}
    for f in sorted(glob.glob(os.path.join(d, 'rep_*.json'))):
        if '.tmp' in f: continue
        a = json.load(open(f))
        out[a['rep']] = a
    return out


def fair(a, end=True):
    if end:
        return a['summary_ext']['end']['persistence'] if 'summary_ext' in a else None
    return a['summary']['h']['persistence']


def wage(a, end=True):
    return a['summary_ext']['end']['wage'] if end else a['summary']['h']['wage']


def boot(x, n=2000, seed=0):
    x = np.asarray(x, float)
    if len(x) == 0: return (None, None)
    rng = np.random.default_rng(seed)
    m = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return (float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975)))


def wilson(k, n, z=1.96):
    if n == 0: return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (float(c - h), float(c + h))


def mcnemar(a, b):
    """Exact two-sided McNemar p for paired binary outcomes."""
    from math import comb
    n10 = sum(1 for x, y in zip(a, b) if x and not y)
    n01 = sum(1 for x, y in zip(a, b) if y and not x)
    n = n10 + n01
    if n == 0: return 1.0
    k = min(n10, n01)
    p = sum(comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return float(min(1.0, 2 * p))


def reference_S3():
    """S3 per replicate: this run's empty-mask cell where present, else the stored S3 + eq ideal run (identical
    dynamics, validated)."""
    mine = load('S3')
    st = load('Ni', STORED)
    out = {}
    for r in range(60):
        if r in mine: out[r] = ('mine', mine[r])
        elif r in st: out[r] = ('stored', st[r])
    return out


def cell_stats(runs):
    reps = sorted(runs)
    f10 = [fair(runs[r]) for r in reps]; f2 = [fair(runs[r], False) for r in reps]
    f10 = [x for x in f10 if x is not None]
    st = dict(n=len(reps), reps=reps,
              fair_10000=float(np.mean(f10)) if f10 else None, fair_10000_ci=boot(f10),
              fair_2000=float(np.mean(f2)), fair_2000_ci=boot(f2),
              runs_any_10000=int(sum(x > 0 for x in f10)), runs_any_2000=int(sum(x > 0 for x in f2)),
              runs_half_10000=int(sum(x >= 0.5 for x in f10)),
              runs_any_10000_wilson=wilson(int(sum(x > 0 for x in f10)), len(f10)),
              zero_wage_10000=float(np.mean([wage(runs[r])[0] for r in reps if 'summary_ext' in runs[r]])) if f10 else None,
              quarter_wage_10000=float(np.mean([wage(runs[r])[1] for r in reps if 'summary_ext' in runs[r]])) if f10 else None,
              zero_wage_2000=float(np.mean([wage(runs[r], False)[0] for r in reps])),
              prodeff_10000=float(np.mean([runs[r]['summary_ext']['end']['prodeff'] for r in reps
                                           if 'summary_ext' in runs[r]])) if f10 else None)
    traj = defaultdict(list)
    for r in reps:
        t = runs[r].get('cc', {}).get('traj')
        if t is None:      # a stored run: fair_t of the summary (every check) and the extension (every 10th)
            ft = runs[r]['summary']['fair_t']
            t = {str(g): ft[g // 10] for g in (0, 10, 20, 200, 2000)}
            t['10000'] = runs[r]['summary_ext']['end']['persistence']
        for k, v in t.items(): traj[k].append(v)
    st['traj'] = {k: float(np.mean(v)) for k, v in traj.items()}
    # held scripts at the endpoint, regrowth, production log
    held = defaultdict(lambda: defaultdict(list))
    for r in reps:
        h = runs[r].get('cc', {}).get('held_10000')
        if not h: continue
        for role, d in h.items():
            for k, v in d.items(): held[role][k].append(v)
    st['held_10000'] = {role: {k: float(np.mean(v)) for k, v in d.items()} for role, d in held.items()}
    rg = []
    for r in reps:
        g_ = runs[r].get('cc', {}).get('regrowth')
        if g_: rg.append((r, g_))
    st['regrowing_runs'] = [r for r, g_ in rg if g_['regrows']]
    piv = Counter(); tim = Counter(); holders = Counter(); nuclei = []
    for r, g_ in rg:
        if not g_['regrows'] or not g_['nuclei']: continue
        nu = g_['nuclei'][0]
        if 'members' not in nu: continue
        holders[' / '.join(m['spelling'] for m in nu['members'])] += 1
        for p in nu['pivotal']:
            piv['%s:%s:%s' % ('B' if p['slot'] == 0 else 'W', p['label'], p['prov'])] += 1
            if p['prov'] == 'granted':
                tim['%s:%s' % (p['label'], p['timing'])] += 1
        nuclei.append(dict(rep=r, gen=nu['gen'], members=[(m['spelling'], m['holder']) for m in nu['members']],
                           pivotal=[(p['slot'], p['set'], p['label'], p['prov'], p.get('timing'), p['S3'])
                                    for p in nu['pivotal']]))
    st['nucleus_members'] = dict(holders); st['pivotal'] = dict(piv); st['timing'] = dict(tim); st['nuclei'] = nuclei
    plog = defaultdict(Counter)
    for r in reps:
        for g_, c in runs[r].get('cc', {}).get('prod_log', {}).items():
            plog[g_].update(c)
    st['prod_log'] = {g_: dict(c) for g_, c in plog.items()}
    tm = [sum(v for k, v in runs[r]['time'].items()) / 60 for r in reps if 'time' in runs[r]]
    st['minutes_median'] = float(np.median(tm)) if tm else None
    return st


def paired(a, b, end=True):
    reps = sorted(set(a) & set(b))
    fa = [fair(a[r], end) for r in reps]; fb = [fair(b[r], end) for r in reps]
    ok = [(x, y) for x, y in zip(fa, fb) if x is not None and y is not None]
    if not ok: return None
    d = [x - y for x, y in ok]
    return dict(n=len(ok), diff=float(np.mean(d)), ci=boot(d),
                mcnemar_any=mcnemar([x > 0 for x, _ in ok], [y > 0 for _, y in ok]),
                runs_differ=int(sum(abs(z) > 1e-9 for z in d)))


def main():
    cells = {}
    for c in ORDER:
        r = load(c)
        if r: cells[c] = r
    s3ref = {r: v[1] for r, v in reference_S3().items()}
    res = dict(cells={}, contrasts={}, mediation={})
    for c, runs in cells.items():
        res['cells'][c] = cell_stats(runs)
    res['cells']['S3_reference'] = cell_stats({r: v for r, v in s3ref.items() if r < 20})
    H = cells.get('Hfull', {})
    for c, runs in cells.items():
        if c != 'Hfull' and H: res['contrasts'][c + ' - Hfull'] = paired(runs, H)
        if c != 'S3': res['contrasts'][c + ' - S3'] = paired(runs, s3ref)
    for x in ('a', 'b', 'c', 'd'):
        for kind, rk in (('plus_', 'rplus_'), ('minus_', 'rminus_')):
            if kind + x in cells and rk + x in cells:
                res['contrasts'][kind + x + ' - ' + rk + x] = paired(cells[kind + x], cells[rk + x])
    if 'plus_a' in cells and 'plus_b' in cells:
        res['contrasts']['plus_b - plus_a'] = paired(cells['plus_b'], cells['plus_a'])
    for c in list(cells):
        med = load(c + '_med')
        if med:
            res['mediation'][c] = [dict(rep=r, original=fair(cells[c][r]), replay=fair(med[r]),
                                        replay_2000=fair(med[r], False), withheld=med[r]['cc']['mask']['withhold'])
                                   for r in sorted(med)]
    st_f = os.path.join(ROOT, 'runs', 'coverage-components-static.json')
    if os.path.exists(st_f):
        st = json.load(open(st_f))
        res['static'] = {k: v for k, v in st.items() if k != 'named'}
        res['static']['named'] = st.get('named')
    va = os.path.join(ROOT, 'runs', 'coverage-components-validate.json')
    if os.path.exists(va):
        res['validate'] = json.load(open(va))
    json.dump(res, open(os.path.join(ROOT, 'runs', 'coverage-components.json'), 'w'), indent=1, default=str)
    md = ['# Coverage components: run summary (generated by src/coverage_components_report.py)', '',
          'Fair share = fraction of islands fair; 10,000 is the primary endpoint. [95%] bootstrap over runs. ε = 0 lottery '
          'at (100, 64), mN = 1, ideal table; finite (N, I, horizon).', '',
          '| cell | runs | fair 10,000 [95%] | fair 2,000 | runs any fair (10,000) | runs ≥ ½ | zero wage | ¼ wage | '
          'fair at 0 / 10 / 20 / 200 | min/run |', '|---|---|---|---|---|---|---|---|---|---|']
    for c in ORDER + ['S3_reference']:
        s = res['cells'].get(c)
        if not s: continue
        ci = s['fair_10000_ci']
        t = s['traj']
        md.append('| %s | %d | %.3f [%.2f, %.2f] | %.3f | %d | %d | %.2f | %.2f | %.2f / %.2f / %.2f / %.2f | %s |' % (
            c, s['n'], s['fair_10000'] or 0, ci[0] or 0, ci[1] or 0, s['fair_2000'], s['runs_any_10000'],
            s['runs_half_10000'], s['zero_wage_10000'] or 0, s['quarter_wage_10000'] or 0,
            t.get('0', 0), t.get('10', 0), t.get('20', 0), t.get('200', 0),
            '%.1f' % s['minutes_median'] if s['minutes_median'] else '-'))
    md += ['', '## Paired contrasts (fair share at 10,000)', '', '| contrast | n | Δ [95%] | runs differing | McNemar p (any fair) |',
           '|---|---|---|---|---|']
    for k, v in res['contrasts'].items():
        if v is None: continue
        md.append('| %s | %d | %+.3f [%+.2f, %+.2f] | %d | %.3f |' % (k, v['n'], v['diff'], v['ci'][0], v['ci'][1],
                                                                    v['runs_differ'], v['mcnemar_any']))
    md += ['', '## Held scripts at 10,000 (share of individuals holding ≥ 1 script of the class)', '']
    for c in ORDER:
        s = res['cells'].get(c)
        if not s or not s['held_10000']: continue
        for role, d in s['held_10000'].items():
            md.append('- %s %s: %s' % (c, role, ', '.join('%s %.2f' % (k, v) for k, v in sorted(d.items())
                                                          if ':' not in k)))
    md += ['', '## Regrowth nuclei, pivotal scripts, timing', '']
    for c in ORDER:
        s = res['cells'].get(c)
        if not s or not s['regrowing_runs']: continue
        md.append('- **%s**: regrowing runs %s; pivotal %s; timing of pivotal granted scripts %s; nuclei %s' % (
            c, s['regrowing_runs'], s['pivotal'], s['timing'], s['nucleus_members']))
    if res['mediation']:
        md += ['', '## Mediation replays', '']
        for c, rows in res['mediation'].items():
            for r in rows:
                md.append('- %s rep %d: original %.3f, replay %.3f (2,000: %.3f), withheld %d scripts' % (
                    c, r['rep'], r['original'] or 0, r['replay'] or 0, r['replay_2000'] or 0, len(r['withheld'])))
    open(os.path.join(ROOT, 'runs', 'coverage-components.md'), 'w').write('\n'.join(md) + '\n')
    print('\n'.join(md))


if __name__ == '__main__':
    main()
