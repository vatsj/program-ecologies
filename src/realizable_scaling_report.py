"""Report for the realizable-scaling run: runs/realizable-scaling.md and .json (notes/realizable-scaling.md §1.5)."""
import json
import math
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import realizable_scaling as RS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'realizable_scaling')


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def mcnemar_exact(b, c):
    n = b + c
    if n == 0: return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def boot(x, nb=4000, seed=1):
    x = np.asarray(x, float)
    if len(x) == 0: return (float('nan'), float('nan'))
    rng = np.random.default_rng(seed)
    m = rng.choice(x, size=(nb, len(x)), replace=True).mean(1)
    return (float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975)))


def at(r, g, key='snaps'):
    """Snapshot (or island record with key='isl') at generation g; the frozen state after freezing; the 2,000 value
    for a run not extended (universal-open at 2,000 with E3 decided); None if censored."""
    s = r[key].get(str(g))
    if s is not None: return s
    fin = r['final'] if key == 'snaps' else r['final_isl']
    if r.get('frozen_at', -1) > 0 and g >= r['last_gen']: return fin
    # T_ext is not a multiple of the 10-generation step: the run ends at T_ext rounded up and its final state is T_ext's
    if g == r.get('T_ext') and r['horizon'] == g and r['last_gen'] - g < 10 and r.get('ext_cut', -1) < 0: return fin
    if g > r['gens'] and r['horizon'] <= r['gens']:
        if r.get('noext'): return None                  # not extended by the drop order: censored after 2,000
        return r[key].get(str(r['gens'])) or fin
    if g == r['last_gen']: return fin
    return None


def score_g(r):
    """Main cells at T_ext; cells run without extensions (drop-order step 1) at 2,000; the rest at 10,000."""
    if r['main']: return r['T_ext']
    return 2000 if r.get('noext') else 10000


def load_rows(names):
    rows = []
    for n in names:
        p = os.path.join(OUT, 'lottery_%s.json' % n)
        if os.path.exists(p): rows += json.load(open(p))
    return rows


def cell_stats(rows, g):
    I = rows[0]['I']
    ss = [(r, at(r, g), at(r, g, 'isl')) for r in rows]
    ok = [(r, s, i) for r, s, i in ss if s is not None and i is not None]
    n = len(ok)
    out = dict(runs=len(rows), censored=len(rows) - n, g=g)
    if n == 0: return out
    uo = sum(1 for r, s, i in ok if s['universal_open'])
    out['uo'] = uo; out['uo_frac'] = uo / n; out['uo_wilson'] = wilson(uo, n)
    eff = [i['eff'] / I for r, s, i in ok]
    out['eff_mean'] = float(np.mean(eff)); out['q'] = 1 - out['eff_mean']; out['q_ci'] = tuple(1 - x for x in boot(eff)[::-1])
    alle = sum(1 for r, s, i in ok if i['eff'] == I)
    out['all_eff'] = alle; out['all_eff_wilson'] = wilson(alle, n)
    out['pcc'] = float(np.mean([s['pcc'] for r, s, i in ok]))
    out['eff90_mean'] = float(np.mean([np.mean(np.asarray(i['cc']) >= 0.9) for r, s, i in ok]))
    out['held_mean'] = float(np.mean([np.mean(i['held']) for r, s, i in ok]))
    # inefficient islands (P(C,C) < 0.95) by their label: on a failing (rival / identity) island, or held by the main
    # network next to one (migrant load), or in a universal run
    lab = Counter()
    for r, s, i in ok:
        for c_, f_ in zip(i['cc'], i['fail']):
            if c_ < 0.95:
                lab[(f_ or 'main') + ('' if not i['universal_open'] else '/universal')] += 1
    out['ineff_by_label'] = dict(lab)
    out['ident_islands'] = float(np.mean([s['identity_islands'] / I for r, s, i in ok]))
    out['runs_with_ident'] = sum(1 for r, s, i in ok if s['identity_islands'] > 0)
    out['cause'] = dict(Counter(i['cause'] for r, s, i in ok if not i['universal_open']))
    out['fail_islands'] = dict(Counter(f for r, s, i in ok for f in i['fail'] if f))
    out['held_frac'] = float(np.mean([s['held'] / I for r, s, i in ok]))
    out['cross_pcc'] = float(np.mean([s['cross_pcc'] for r, s, i in ok]))
    out['seeded_Q'] = float(np.mean([r['seeded_Q'] for r in rows]))
    out['E3'] = dict(Counter(r['E3'] for r in rows))
    return out


def static_stats(rows):
    lab = Counter(r['static']['label'] for r in rows)
    per = Counter((p['fail'], p['kind']) for r in rows for p in r['static']['per'])
    dead = sum(1 for r in rows for p in r['static']['per'] if p['kind'] == 'absorbing' and p['dead_prior_bridges'] > 0)
    return dict(labels=dict(lab), per_island={'%s/%s' % k: v for k, v in per.items()}, absorbing_with_dead_prior_bridge=dead)


def resolution(rows, g):
    """Among runs not universal-open at 2,000: the fraction universal-open at g; first-universal times."""
    base = [r for r in rows if at(r, 2000) is not None and not at(r, 2000)['universal_open']]
    late = [r for r in base if at(r, g) is not None and at(r, g)['universal_open']]
    t = [r['uo_first'] for r in rows if r['uo_first'] >= 0]
    return dict(not_uo_2000=len(base), resolved_by_g=len(late), g=g,
                uo_first_median=float(np.median(t)) if t else None,
                uo_first_q90=float(np.quantile(t, 0.9)) if t else None)


def clustering(rows):
    """Per seeded copy: islands ever held by an identity holder whose seed had k copies, by k (1, >= 2)."""
    est = defaultdict(lambda: [0, 0])          # k -> [islands ever identity-held, islands seeded with k]
    copies = defaultdict(int)
    for r in rows:
        c = r['clus']
        for qi, ev in zip(c['q_isl'], c['ident_ever']):
            k = min(qi, 2)
            est[k][0] += ev; est[k][1] += 1
            copies[k] += qi
    out = {str(k): dict(islands=v[1], ever_identity=v[0], per_island=v[0] / max(1, v[1]),
                        per_copy=v[0] / max(1, copies[k]) if k > 0 else None) for k, v in sorted(est.items())}
    out['seeded_per_run'] = float(np.mean([r['clus']['seeded'] for r in rows]))
    out['occupied_per_run'] = float(np.mean([r['clus']['occupied'] for r in rows]))
    out['multi_per_run'] = float(np.mean([r['clus']['multi'] for r in rows]))
    nfin = sum(sum(r['clus']['ident_final']) for r in rows)
    out['identity_final_islands'] = nfin
    out['identity_final_seeded_spelling'] = sum(r['clus']['ident_final_seeded_sp'] for r in rows)
    ev = sum(sum(r['clus']['ident_ever']) for r in rows); sd = sum(r['clus']['seeded'] for r in rows)
    out['establishment_per_seeded_copy'] = ev / max(1, sd)
    return out


def logit_ll(x, y):
    """Log-likelihood of a one-covariate logistic regression (Newton)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    X = np.c_[np.ones_like(x), x]
    b = np.zeros(2)
    for _ in range(50):
        p = 1 / (1 + np.exp(-X @ b))
        Wd = p * (1 - p) + 1e-9
        H = X.T @ (X * Wd[:, None]) + 1e-6 * np.eye(2)
        b = b + np.linalg.solve(H, X.T @ (y - p))
    p = np.clip(1 / (1 + np.exp(-X @ b)), 1e-12, 1 - 1e-12)
    return float((y * np.log(p) + (1 - y) * np.log(1 - p)).sum()), b.tolist()


def paired(A, B, g=None):
    """A - B on universal-open, paired by replicate, at the earlier of the two cells' scoring horizons (or g)."""
    if g is None: g = min(score_g(A[0]), score_g(B[0]))
    a = {r['rep']: at(r, g) for r in A}; b = {r['rep']: at(r, g) for r in B}
    reps = sorted(k for k in a if k in b and a[k] is not None and b[k] is not None)
    if not reps: return None
    x = np.array([int(a[k]['universal_open']) - int(b[k]['universal_open']) for k in reps])
    bb = int((x == 1).sum()); cc = int((x == -1).sum())
    return dict(n=len(reps), diff=float(x.mean()), ci=boot(x), up=bb, down=cc, p=mcnemar_exact(bb, cc))


def fit_qc(cs, f, f0):
    """f = f0 exp(-q c) by least squares in q on the panel points with c > 0."""
    cs = np.asarray(cs, float); f = np.asarray(f, float)
    best = None
    for q in np.linspace(0, 0.5, 5001):
        e = float(((f - f0 * np.exp(-q * cs)) ** 2).sum())
        if best is None or e < best[0]: best = (e, q)
    return float(best[1])


def crossing(cs, f, level=0.5):
    for k in range(1, len(cs)):
        if f[k - 1] >= level > f[k]:
            return float(cs[k - 1] + (f[k - 1] - level) / (f[k - 1] - f[k]) * (cs[k] - cs[k - 1]))
    return None


def costs(rows):
    t = [r['time_s'] for r in rows]
    return dict(worker_s=float(sum(t)), mean_s=float(np.mean(t)), max_s=float(max(t)))


# ------------------------------------------------------------------------------------------------ calibration
def calib_summary():
    p = os.path.join(OUT, 'calib_rows.json')
    if not os.path.exists(p): return None
    rows = json.load(open(p))
    out = {}
    for rule in ('Snon', 'abl', 'Cdon'):
        for N in (50, 100, 200, 400):
            rs = [r for r in rows if r['rule'] == rule and r['N'] == N]
            if not rs: continue
            per = [np.array([t for t in r['t_est'] if t >= 0], float) for r in rs]
            ts = np.concatenate(per) if per else np.array([])
            nis = sum(r['I'] for r in rs)
            T = float(np.median(ts)) if len(ts) else None
            rng = np.random.default_rng(1)
            bs = []
            for _ in range(2000):
                idx = rng.integers(0, len(per), len(per))
                v = np.concatenate([per[i] for i in idx])
                if len(v): bs.append(np.median(v))
            first = [r['first'] for r in rs if r['first'] >= 0]
            d = dict(runs=len(rs), islands=nis, nucleated=int(len(ts)), p=float(len(ts) / nis), T_nuc=T,
                     T_ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if bs else None,
                     q25_75=[float(np.percentile(ts, 25)), float(np.percentile(ts, 75))] if len(ts) else None,
                     first_median=float(np.median(first)) if first else None, time_s=float(sum(r['time_s'] for r in rs)))
            if T:
                d['x_m1'] = T / N; d['x_cal'] = RS.mN_cal(N) * T / N
            out['%s_%d' % (rule, N)] = d
        Ns = [N for N in (50, 100, 200, 400) if out.get('%s_%d' % (rule, N), {}).get('T_nuc')]
        if len(Ns) >= 2:
            out['%s_exponent' % rule] = float(np.polyfit(np.log(Ns), np.log([out['%s_%d' % (rule, N)]['T_nuc'] for N in Ns]), 1)[0])
    return out


def fmt(x, d=2):
    if x is None: return '–'
    if isinstance(x, float) and math.isnan(x): return '–'
    return ('%.' + str(d) + 'f') % x


def fw(k, n, w):
    return '%d/%d [%.2f, %.2f]' % (k, n, w[0], w[1])


# drop-order step 2 (notes §2 addendum): cells dropped after launch; their finished replicates are not reported
DROPPED = {'rs_Cdon_400_64_m1', 'rs_Cdense_400_64_m1', 'rs_Cdense_400_64_cal'}

PATHS = {'P1': [(50, 64), (100, 64), (200, 64), (400, 64)], 'P2': [(100, 32), (100, 64), (100, 128), (100, 256)],
         'P3': [(50, 32), (100, 64), (200, 128)]}


def main():
    names = [f[len('lottery_'):-5] for f in os.listdir(OUT) if f.startswith('lottery_') and f.endswith('.json')]
    rows = load_rows(names)
    by = defaultdict(list)
    for r in rows:
        if r['cell'] not in DROPPED: by[r['cell']].append(r)
    J = dict(calib=calib_summary(), cells={}, paths={}, panel={}, contrasts={}, clustering={}, costs={})
    vp = os.path.join(ROOT, 'runs', 'realizable-scaling-validate.json')
    J['validate'] = {k: v for k, v in json.load(open(vp)).items() if k != 'rows'} if os.path.exists(vp) else None
    md = ['# The realizable lottery along paths in (N, I, mN): run report', '',
          'Spec `specs/2026-10-14-realizable-scaling.md`; notes `notes/realizable-scaling.md`; predictions '
          '`predictions/2026-10-14-realizable-scaling.md`. ε = 0 lottery statistics at finite (N, I, horizon), never π. '
          'Generated by `src/realizable_scaling_report.py`.', '']
    C = J['calib']
    if C:
        md += ['## T_nuc calibration (m = 0, I = 64, replicates 500–519)', '',
               '| rule | N | islands nucleated / all (p) | T_nuc median [95%] | IQR | run-level first (median) | x at mN = 1 | x calibrated | worker-s |',
               '|---|---|---|---|---|---|---|---|---|']
        for rule in ('Snon', 'abl', 'Cdon'):
            for N in (50, 100, 200, 400):
                d = C.get('%s_%d' % (rule, N))
                if not d: continue
                md.append('| %s | %d | %d / %d (%.2f) | %s [%s, %s] | %s | %s | %s | %s | %.0f |' % (
                    rule, N, d['nucleated'], d['islands'], d['p'], fmt(d['T_nuc'], 0),
                    fmt(d['T_ci'][0], 0) if d['T_ci'] else '–', fmt(d['T_ci'][1], 0) if d['T_ci'] else '–',
                    '–' if not d['q25_75'] else '%.0f–%.0f' % tuple(d['q25_75']), fmt(d['first_median'], 0),
                    fmt(d.get('x_m1')), fmt(d.get('x_cal')), d['time_s']))
            if '%s_exponent' % rule in C:
                md.append('| %s | exponent | | N^%.2f | | | | | |' % (rule, C['%s_exponent' % rule]))
        md.append('')
    if J['validate']:
        v = J['validate']
        md += ['## Validation (draw for draw against stored provenance rows)', '',
               '%d stored runs compared, %d with any difference; %d common trace points; classifier vs provenance '
               'universal-open mismatches %d.' % (v['n_compared'], v['n_bad'], v['trace_points'], v['n_classifier_mismatch']), '']
    md += ['## Cells', '',
           'uo = universal-open runs [Wilson]; ē = mean fraction of islands with P(C,C) ≥ 0.95 at the scoring horizon; '
           'q = 1 − ē [run bootstrap]; all-eff = runs with every island efficient; ident = mean identity-island fraction; '
           'causes of non-universal runs (identity / rival / inefficient); static = the absorbing check on the final support.', '',
           '| cell | N | I | mN | runs | seeded copies | uo 2,000 | uo 10,000 | uo T_ext | ē | q [95%] | all-eff | ident islands | causes | static labels | worker-h |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    order = RS.ALL['A'] + RS.ALL['B'] + RS.ALL['C'] + RS.ALL['D']
    f = lambda s: fw(s['uo'], s['runs'] - s['censored'], s['uo_wilson']) if s and 'uo' in s else '–'
    for c in order:
        rs = by.get(c)
        if not rs: continue
        inf = RS.CELL_INFO[c]
        s2 = cell_stats(rs, 2000); s10 = cell_stats(rs, 10000)
        sT = cell_stats(rs, inf['T_ext']) if inf['main'] else None
        sg = sT if inf['main'] else s10
        st = static_stats(rs)
        J['cells'][c] = dict(info=inf, s2000=s2, s10000=s10, sT=sT, static=st, resolution=resolution(rs, score_g(rs[0])),
                             costs=costs(rs), clustering=clustering(rs))
        md.append('| %s | %d | %d | %.2f | %d | %.1f | %s | %s | %s | %s | %s [%s, %s] | %d | %s | %s | %s | %.2f |' % (
            c[3:], inf['N'], inf['I'], inf['mN'], len(rs), s2['seeded_Q'], f(s2), f(s10), f(sT) if sT else '–',
            fmt(sg.get('eff_mean'), 3), fmt(sg.get('q'), 3), fmt(sg['q_ci'][0], 3) if 'q_ci' in sg else '–',
            fmt(sg['q_ci'][1], 3) if 'q_ci' in sg else '–', sg.get('all_eff', 0), fmt(sg.get('ident_islands'), 3),
            ' / '.join(str(sg.get('cause', {}).get(k, 0)) for k in ('identity', 'rival', 'inefficient')),
            ', '.join('%s %d' % kv for kv in sorted(st['labels'].items())), costs(rs)['worker_s'] / 3600))
    md.append('')
    md += ['## Paths (universal-open fraction at the scoring horizon; mean efficient-island fraction ē)', '']
    for pn, gs in PATHS.items():
        md += ['**%s**' % pn, '', '| rule | arm | ' + ' | '.join('(%d, %d)' % g for g in gs) + ' |',
               '|---|---|' + '---|' * len(gs)]
        for rule in ('Snon', 'prop', 'abl', 'Cdon', 'Cdense'):
            for arm in ('m1', 'cal'):
                if rule == 'prop' and arm == 'm1': continue
                cells_ = [RS.cell_name(rule, N, I, 'cal' if N == 100 else arm) for (N, I) in gs]
                if not any(c in by for c in cells_): continue
                ent = []
                for c in cells_:
                    rs = by.get(c)
                    if not rs: ent.append('–'); continue
                    s = cell_stats(rs, score_g(rs[0]))
                    ent.append('%.2f (ē %.3f)' % (s['uo_frac'], s['eff_mean']) if 'uo' in s else '–')
                J['paths'].setdefault(pn, {})['%s_%s' % (rule, arm)] = ent
                md.append('| %s | %s | %s |' % (rule, arm, ' | '.join(ent)))
        md.append('')
    md += ['## Crossed panel (S-nonself, calibrated mN; c = TwinD copies per run; c = 0 is the proportional control)', '',
           '| geometry | f(0) | f(4) | f(8) | f(16) | f at 2,000 | q_c fit | 50% crossing (copies) | islands ever identity-held per seeded copy, incl. colonized (c = 4 / 8 / 16) | own-island establishment per copy (c = 4 / 8 / 16) |',
           '|---|---|---|---|---|---|---|---|---|---|']
    for (N, I) in RS.PANEL_GEOMS:
        cs = [RS.cell_name('prop', N, I, 'cal')] + [RS.cell_name('cross%d' % c, N, I, 'cal') for c in RS.PANEL_C[1:]]
        if not all(c in by for c in cs): continue
        fs, ns = [], []
        for c in cs:
            s = cell_stats(by[c], score_g(by[c][0])); fs.append(s['uo_frac']); ns.append(s['uo'])
        f0 = fs[0]
        q = fit_qc(list(RS.PANEL_C[1:]), fs[1:], f0)
        cr = crossing(list(RS.PANEL_C), fs) if f0 >= 0.5 else None
        est = [clustering(by[c])['establishment_per_seeded_copy'] for c in cs[1:]]
        own = []
        for c in cs[1:]:
            cl_ = clustering(by[c]); n1 = cl_.get('1', {}); n2 = cl_.get('2', {})
            ev = n1.get('ever_identity', 0) + n2.get('ever_identity', 0)
            cp = sum(min(q, 99) for r in by[c] for q in r['clus']['q_isl'] if q > 0)
            own.append(ev / max(1, cp))
        f2 = [cell_stats(by[c], 2000)['uo_frac'] for c in cs]
        J['panel']['%d_%d' % (N, I)] = dict(f=fs, uo=ns, q_c=q, crossing=cr, est_per_copy=est, own_island_per_copy=own, f2000=f2)
        md.append('| (%d, %d) | %s | %s | %.4f | %s | %s | %s |' % (
            N, I, ' | '.join('%.2f' % x for x in fs), ' / '.join('%.2f' % x for x in f2), q,
            fmt(cr, 1) if cr else ('none (f₀ < 0.5)' if f0 < 0.5 else 'none'), ' / '.join('%.3f' % x for x in est),
            ' / '.join('%.3f' % x for x in own)))
    md.append('')
    md += ['## Paired contrasts (universal-open at the earlier of the two cells\' scoring horizons)', '',
           '| contrast | n | diff [95%] | up / down | McNemar p |', '|---|---|---|---|---|']

    def add(lbl, a, b):
        if a in by and b in by:
            p = paired(by[a], by[b])
            if p:
                J['contrasts'][lbl] = p
                md.append('| %s | %d | %+.2f [%+.2f, %+.2f] | %d / %d | %.3f |' % (lbl, p['n'], p['diff'], p['ci'][0], p['ci'][1],
                                                                              p['up'], p['down'], p['p']))
    for (N, I) in RS.GEOMS:
        if N != 100:
            for rule in ('Snon', 'abl', 'Cdon'):
                add('%s (%d,%d): cal − m1' % (rule, N, I), RS.cell_name(rule, N, I, 'cal'), RS.cell_name(rule, N, I, 'm1'))
        add('(%d,%d) cal: ablation − proportional' % (N, I), RS.cell_name('abl', N, I, 'cal'), RS.cell_name('prop', N, I, 'cal'))
        add('(%d,%d) cal: proportional − S-nonself' % (N, I), RS.cell_name('prop', N, I, 'cal'), RS.cell_name('Snon', N, I, 'cal'))
    for (N, I) in [(200, 64), (400, 64)]:
        for arm in ('m1', 'cal'):
            add('(%d,%d) %s: dense − one donor' % (N, I, arm), RS.cell_name('Cdense', N, I, arm), RS.cell_name('Cdon', N, I, arm))
    md.append('')
    snon = [r for c, rs in by.items() if RS.CELL_INFO[c]['rule'] == 'Snon' for r in rs]
    if snon:
        cl = clustering(snon)
        x1 = [r['clus']['seeded'] for r in snon]; x2 = [r['clus']['multi'] for r in snon]
        y = [int(sum(r['clus']['ident_final']) > 0) for r in snon]
        ll1, b1 = logit_ll(x1, y); ll2, b2 = logit_ll(x2, y)
        cl['logit_total'] = dict(ll=ll1, b=b1); cl['logit_multi'] = dict(ll=ll2, b=b2)
        J['clustering']['Snon_pooled'] = cl
        md += ['## Clustering (pooled S-nonself cells, both arms)', '',
               'Islands ever held by an identity holder, by the number of TwinD copies seeded on that island: ' +
               '; '.join('%s copies: %d of %d islands (per island %.3f%s)' % (
                   k, v['ever_identity'], v['islands'], v['per_island'], '' if v['per_copy'] is None else ', per copy %.3f' % v['per_copy'])
                         for k, v in cl.items() if k in ('0', '1', '2')) + '.',
               '', 'Establishment per seeded copy %.3f; identity islands at the end %d, of which held by a seeded (Q) spelling %d. '
               'Logistic "any identity island at the end": on total copies ll %.1f, on multi-copy islands ll %.1f.' % (
                   cl['establishment_per_seeded_copy'], cl['identity_final_islands'], cl['identity_final_seeded_spelling'], ll1, ll2), '']
    md += ['## Natural cells: universal-open by seeded copies per run (S-nonself, scoring horizon)', '',
           '| arm | 0–4 | 5–9 | 10–14 | 15–19 | 20–29 | ≥ 30 |', '|---|---|---|---|---|---|---|']
    bins = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 29), (30, 10 ** 6)]
    for arm in ('m1', 'cal'):
        cnt = [[0, 0] for _ in bins]
        for c, rs in by.items():
            inf = RS.CELL_INFO[c]
            if inf['rule'] != 'Snon' or not (inf['arm'] == arm or (inf['N'] == 100 and arm == 'm1')): continue
            for r in rs:
                s = at(r, score_g(r))
                if s is None: continue
                for k, (lo, hi) in enumerate(bins):
                    if lo <= r['seeded_Q'] <= hi: cnt[k][0] += int(s['universal_open']); cnt[k][1] += 1
        J['clustering']['bins_%s' % arm] = cnt
        md.append('| %s | %s |' % (arm, ' | '.join('%d/%d' % tuple(x) if x[1] else '–' for x in cnt)))
    md.append('')
    tot = sum(r['time_s'] for r in rows)
    J['costs']['total_worker_h'] = tot / 3600
    md.append('Total lottery worker-hours: %.1f.' % (tot / 3600))
    open(os.path.join(ROOT, 'runs', 'realizable-scaling.md'), 'w').write('\n'.join(md) + '\n')
    json.dump(J, open(os.path.join(ROOT, 'runs', 'realizable-scaling.json'), 'w'), indent=1, default=str)
    print('\n'.join(md))


if __name__ == '__main__':
    main()
