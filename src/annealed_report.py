"""Report for annealed mutation (notes/annealed.md §1.6): summary JSON and tables.

    python3 src/annealed_report.py            # reads runs/annealed/cells_*.json and assay_*.json
"""
import glob
import json
import math
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'annealed')
NS = (200, 400, 800, 1600)
END = 12000


def wilson(k, n, z=1.96):
    if n == 0: return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


def boot_ci(vals, f=np.mean, B=2000, seed=0):
    vals = np.asarray(vals, float)
    if len(vals) == 0: return (None, None)
    r = np.random.default_rng(seed)
    bs = [f(vals[r.integers(len(vals), size=len(vals))]) for _ in range(B)]
    return (round(float(np.percentile(bs, 2.5)), 4), round(float(np.percentile(bs, 97.5)), 4))


def load_rows():
    rows = []
    for p in sorted(glob.glob(os.path.join(OUT, 'cells_*.json'))):
        rows += json.load(open(p))
    seen = {}
    for r in rows:
        seen[(r['cell'], r['rep'])] = r
    return list(seen.values())


def drift_events(r, include_migrant=False):
    ev = [c for c in r['colonizations'] if c['cls'] != 'selected']
    return ev


def snap(r, g):
    s = r['snaps'].get(str(g))
    if s is None and g == END: s = r['snaps'].get(str(r['gens']))
    return s


def per_run(r):
    """Per-run statistics."""
    I = r['I']
    dr = drift_events(r)
    sel = [c for c in r['colonizations'] if c['cls'] == 'selected']
    s = snap(r, END) or {}
    s10 = snap(r, 10000) or {}
    s2 = snap(r, 2000) or {}
    labs = s.get('labels', [])
    fb = None
    if r['arm'] == 'F':
        fb = [c for c in dr if c['island'] != 0]
    idt = r['identity_takeovers']
    return dict(
        drift=len(dr), drift_target=sum(1 for c in dr if c['status_at_arrival'] == 1),
        drift_rival=sum(1 for c in dr if c['status_at_arrival'] == 2),
        drift_unheld=sum(1 for c in dr if c['status_at_arrival'] in (0, -1)),
        selected=len(sel), selected_rival=sum(1 for c in sel if c['status_at_arrival'] == 2),
        migrant_col=len(r['migrant_colonizations']),
        drift_fixed=sum(1 for c in dr if c.get('fate') == 'fixed'),
        drift_held_end=sum(1 for c in dr if c.get('fate') in ('fixed', 'held')),
        drift_unresolved=sum(1 for c in dr if c.get('fate') in ('held', 'minority')),
        drift_fb=len(fb) if fb is not None else None,
        uot=bool(s.get('uot')), uo=bool(s.get('uo')), uot10=bool(s10.get('uot')), uot2=bool(s2.get('uot')),
        identity=s.get('identity', 0) / I, target=s.get('target', 0) / I, exploitable=s.get('exploitable', 0) / I,
        closed_open=s.get('closed_open', 0) / I, unheld=s.get('unheld', 0) / I, eff=s.get('eff', 0) / I,
        eff10=s10.get('eff', 0) / I, identity2=s2.get('identity', 0) / I,
        idt_all=len(idt) / I, idt_late=sum(1 for z in idt if z['start'] >= 2000) / I,
        idt_perm=sum(1 for z in idt if z['permanent']) / I,
        secondary=len(r['secondary']) / I,
        secondary_identity=sum(1 for z in r['secondary'] if z['kind'] == 'identity') / I,
        arrivals=r['arrivals_total'] / I, arrivals10=r['arrivals_by_10k'] / I,
        cures=r['cures'], time_s=r['time_s'])


def poisson_slope(Ns, counts, expo):
    """MLE slope b of log E[count] = a + b log N + log expo (Newton)."""
    x = np.log(np.asarray(Ns, float)); y = np.asarray(counts, float); off = np.log(np.asarray(expo, float))
    if y.sum() == 0: return None
    a, b = math.log(max(y.sum(), 1e-9) / np.exp(off).sum()), 0.0
    for _ in range(100):
        mu = np.exp(a + b * x + off)
        g = np.array([np.sum(y - mu), np.sum((y - mu) * x)])
        H = np.array([[np.sum(mu), np.sum(mu * x)], [np.sum(mu * x), np.sum(mu * x * x)]])
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            return None
        a += step[0]; b += step[1]
        if abs(step).max() < 1e-10: break
    return float(b)


def slope_with_ci(runs_by_N, key='drift', B=2000, seed=1):
    Ns, cs, ex = [], [], []
    for N, rs in runs_by_N.items():
        for p in rs:
            Ns.append(N); cs.append(p[key]); ex.append(8)
    b = poisson_slope(Ns, cs, ex)
    r = np.random.default_rng(seed)
    bs = []
    for _ in range(B):
        N2, c2, e2 = [], [], []
        for N, rs in runs_by_N.items():
            idx = r.integers(len(rs), size=len(rs))
            for k in idx:
                N2.append(N); c2.append(rs[k][key]); e2.append(8)
        v = poisson_slope(N2, c2, e2)
        if v is not None and abs(v) < 20: bs.append(v)
    ci = (round(float(np.percentile(bs, 2.5)), 3), round(float(np.percentile(bs, 97.5)), 3)) if bs else (None, None)
    return (round(b, 3) if b is not None else None), ci


def summarize_cells(rows):
    by = defaultdict(list)
    for r in rows: by[r['cell']].append(r)
    out = {}
    for cell, rs in sorted(by.items()):
        rs = sorted(rs, key=lambda r: r['rep'])
        ps = [per_run(r) for r in rs]
        n = len(ps); I = rs[0]['I']
        d = dict(cell=cell, N=rs[0]['N'], I=I, arm=rs[0]['arm'], K=rs[0]['K'], sched=rs[0]['sched'], cls=rs[0]['cls'],
                 runs=n, reps=[r['rep'] for r in rs])
        for k in ('drift', 'drift_target', 'drift_rival', 'drift_unheld', 'selected', 'selected_rival', 'migrant_col',
                  'drift_fixed', 'drift_held_end', 'drift_unresolved'):
            d[k] = int(sum(p[k] for p in ps))
        d['drift_per_island'] = d['drift'] / (n * I)
        d['drift_per_island_ci'] = boot_ci([p['drift'] / I for p in ps])
        d['drift_free'] = sum(1 for p in ps if p['drift'] == 0)
        d['drift_free_frac'] = d['drift_free'] / n
        d['drift_free_wilson'] = wilson(d['drift_free'], n)
        if rs[0]['arm'] == 'F':
            d['drift_fb'] = int(sum(p['drift_fb'] for p in ps))
            d['drift_fb_per_island'] = d['drift_fb'] / (n * (I - 1))
        for k in ('uot', 'uo', 'uot10', 'uot2'):
            d[k] = int(sum(p[k] for p in ps))
        for k in ('identity', 'target', 'exploitable', 'closed_open', 'unheld', 'eff', 'eff10', 'identity2', 'idt_all',
                  'idt_late', 'idt_perm', 'secondary', 'secondary_identity', 'arrivals', 'arrivals10'):
            d[k] = round(float(np.mean([p[k] for p in ps])), 4)
        d['identity_ci'] = boot_ci([p['identity'] for p in ps])
        cures = [c for p in ps for c in p['cures']]
        lab = defaultdict(lambda: [0, 0])
        via = defaultdict(int)
        for c in cures:
            lab[c['label']][0] += 1
            if c['resolved']:
                lab[c['label']][1] += 1
                if c['label'] == 'exploitable': via[c.get('via', '?')] += 1
        d['rivals_onset'] = {k: dict(n=v[0], resolved=v[1]) for k, v in lab.items()}
        d['exploitable_via'] = dict(via)
        times = [c['g'] - 200 for c in cures if c['label'] == 'exploitable' and c['resolved']]
        d['cure_time_median'] = float(np.median(times)) if times else None
        d['time_s'] = round(float(np.sum([p['time_s'] for p in ps])), 1)
        d['_runs'] = ps
        out[cell] = d
    return out


def assays():
    res = {}
    import gzip
    files = sorted(glob.glob(os.path.join(OUT, 'assay_*.json')))
    files += [f for f in sorted(glob.glob(os.path.join(OUT, 'assay_*.json.gz'))) if f[:-3] not in files]
    for p in files:
        for r in json.load(gzip.open(p) if p.endswith('.gz') else open(p)):
            if 'sp' in r:
                key = 'neutral|%s|%d' % (r['sp'], r['N'])
            else:
                key = 'predator|%s|%d' % (r['cls'], r['N'])
            res.setdefault(key, dict(N=r['N'], rows=[], meta={k: v for k, v in r.items() if k not in ('rows', 'time_s', 'msg', 'k0', 'k1')}, time_s=0.0))
            res[key]['rows'] += r['rows']; res[key]['time_s'] += r['time_s']
    out = {}
    for key, v in sorted(res.items()):
        N = v['N']; rows = v['rows']; n = len(rows)
        if key.startswith('neutral'):
            col5 = sum(1 for z in rows if z[1] >= 0); colany = sum(1 for z in rows if z[2] >= 0)
            fix = sum(1 for z in rows if z[3] >= 0)
            cens = sum(1 for z in rows if z[3] < 0 and z[4] < 0)
            tf = [z[3] for z in rows if z[3] >= 0]
            out[key] = dict(N=N, sp=v['meta']['sp'], reps=n, col5=col5, col5_p=col5 / n, col5_ratio_2overN=col5 / n / (2 / N),
                            col5_wilson=wilson(col5, n), colany=colany, fix=fix, fix_p=fix / n,
                            fix_ratio_1overN=fix / n / (1 / N), fix_wilson=wilson(fix, n), censored=cens,
                            t_fix_median=float(np.median(tf)) if tf else None, time_s=round(v['time_s'], 1))
        else:
            est = [z for z in rows if z[1] >= 0]; done = [z for z in rows if z[2] >= 0]
            cens = sum(1 for z in rows if z[2] < 0 and z[3] < 0)
            out[key] = dict(N=N, cls=v['meta']['cls'], pred=v['meta']['pred'], pred_mu=v['meta']['pred_mu'], reps=n,
                            established=len(est), est_p=len(est) / n, est_wilson=wilson(len(est), n),
                            completed=len(done), completed_given_est=(len(done) / len(est)) if est else None,
                            t_est_median=float(np.median([z[1] for z in est])) if est else None,
                            t_done_median=float(np.median([z[2] for z in done])) if done else None,
                            t_done_q90=float(np.percentile([z[2] for z in done], 90)) if done else None,
                            censored=cens, time_s=round(v['time_s'], 1))
    return out


def paired_diff(cA, cB, key, cells):
    """Mean over shared replicates of (B - A) of a per-run statistic, with a bootstrap interval."""
    if cA not in cells or cB not in cells: return None
    a = {r: p for r, p in zip(cells[cA]['reps'], cells[cA]['_runs'])}
    b = {r: p for r, p in zip(cells[cB]['reps'], cells[cB]['_runs'])}
    common = sorted(set(a) & set(b))
    v = [b[k][key] - a[k][key] for k in common]
    if not v: return None
    return dict(n=len(v), mean=round(float(np.mean(v)), 4), ci=boot_ci(v))


def main():
    rows = load_rows()
    cells = summarize_cells(rows)
    out = dict(cells={k: {kk: vv for kk, vv in v.items() if kk != '_runs'} for k, v in cells.items()})
    # drift slopes
    sl = {}
    for arm in ('i', 'ii', 'iv'):
        rb = {N: cells['an_%s_%d' % (arm, N)]['_runs'] for N in NS if 'an_%s_%d' % (arm, N) in cells}
        if len(rb) >= 2: sl[arm] = slope_with_ci(rb)
    rbF = defaultdict(list)
    for cls in ('AP', 'DET'):
        for N in NS:
            c = 'anF_%s_%d_K3' % (cls, N)
            if c in cells:
                rbF[N] += [dict(p, drift=p['drift_fb']) for p in cells[c]['_runs']]
    if len(rbF) >= 2: sl['F_fairbot_islands'] = slope_with_ci(dict(rbF))
    pooled = defaultdict(list)
    for arm in ('i', 'ii', 'iv'):
        for N in NS:
            c = 'an_%s_%d' % (arm, N)
            if c in cells: pooled[N] += cells[c]['_runs']
    if len(pooled) >= 2: sl['pooled_i_ii_iv'] = slope_with_ci(dict(pooled))
    out['slopes'] = sl
    # paired comparisons
    pc = {}
    for N in NS:
        pc['identity_i_minus_iiiS_%d' % N] = paired_diff('an_iiiS_%d' % N, 'an_i_%d' % N, 'identity', cells)
        pc['identity_ii_minus_iiiP_%d' % N] = paired_diff('an_iiiP_%d' % N, 'an_ii_%d' % N, 'identity', cells)
        pc['uot_i_minus_iiiS_%d' % N] = paired_diff('an_iiiS_%d' % N, 'an_i_%d' % N, 'uot', cells)
        pc['uot_ii_minus_iiiP_%d' % N] = paired_diff('an_iiiP_%d' % N, 'an_ii_%d' % N, 'uot', cells)
        for k in ('idt_late', 'idt_all', 'secondary', 'drift', 'identity', 'uot', 'exploitable'):
            pc['%s_iv_minus_i_%d' % (k, N)] = paired_diff('an_i_%d' % N, 'an_iv_%d' % N, k, cells)
    # pooled N >= 400 (iv - i)
    for k in ('idt_late', 'secondary'):
        v = []
        for N in (400, 800, 1600):
            a, b = 'an_i_%d' % N, 'an_iv_%d' % N
            if a in cells and b in cells:
                A_ = dict(zip(cells[a]['reps'], cells[a]['_runs'])); B_ = dict(zip(cells[b]['reps'], cells[b]['_runs']))
                v += [B_[r][k] - A_[r][k] for r in sorted(set(A_) & set(B_))]
        pc['%s_iv_minus_i_pooled_N400plus' % k] = dict(n=len(v), mean=round(float(np.mean(v)), 4) if v else None,
                                                        ci=boot_ci(v))
    out['paired'] = pc
    # Part F cures
    fc = {}
    for c, d in cells.items():
        if d['arm'] != 'F': continue
        cs = [cc for p in d['_runs'] for cc in p['cures'] if cc['island'] == 0]
        res = sum(1 for cc in cs if cc['resolved'])
        via = defaultdict(int)
        for cc in cs:
            if cc['resolved']: via[cc.get('via', '?')] += 1
        tm = [cc['g'] - 200 for cc in cs if cc['resolved']]
        fc[c] = dict(N=d['N'], cls=d['cls'], K=d['K'], eligible=len(cs), cured=res, cure=res / len(cs) if cs else None,
                     wilson=wilson(res, len(cs)), via=dict(via), t_median=float(np.median(tm)) if tm else None,
                     labels_at_onset=sorted(set(cc['label'] for cc in cs)))
    out['partF'] = fc
    mix = {}
    for N in NS:
        a, b = fc.get('anF_AP_%d_K3' % N), fc.get('anF_DET_%d_K3' % N)
        if a and b and a['cure'] is not None and b['cure'] is not None:
            mix[N] = round(0.52 * a['cure'] + 0.48 * b['cure'], 3)
    out['partF_mix'] = mix
    # hazards per arrival (pooled over N) and the original-path extrapolation (Gemini)
    hz = {}
    for cls in ('AP', 'DET'):
        cur = [fc[c] for c in fc if fc[c]['cls'] == cls and fc[c]['K'] == 3 and fc[c]['cure'] is not None]
        if cur:
            p = np.mean([z['cure'] for z in cur])
            arr = np.mean([cells[c]['arrivals'] for c in fc if fc[c]['cls'] == cls and fc[c]['K'] == 3])
            h = -math.log(max(1e-6, 1 - min(p, 0.9999))) / arr
            hz[cls] = dict(cure=round(float(p), 3), arrivals=round(float(arr), 1), hazard_per_arrival=h,
                           formula=0.2592 * (0.0741 if cls == 'AP' else 0.00568),
                           extrap_12=1 - math.exp(-12 * h), extrap_2=1 - math.exp(-2 * h))
    if 'AP' in hz and 'DET' in hz:
        hz['mix_extrap_12'] = 0.52 * hz['AP']['extrap_12'] + 0.48 * hz['DET']['extrap_12']
    out['hazards'] = hz
    # natural exploitable rivals pooled
    nat = defaultdict(lambda: [0, 0])
    for c, d in cells.items():
        if d['arm'] in ('i', 'ii', 'iv') and d['K'] == 3:
            for lab, v in d['rivals_onset'].items():
                nat[lab][0] += v['n']; nat[lab][1] += v['resolved']
    out['natural_rivals_onset_pooled_rain'] = {k: dict(n=v[0], resolved=v[1]) for k, v in nat.items()}
    nat0 = defaultdict(lambda: [0, 0])
    for c, d in cells.items():
        if d['arm'] in ('iiiS', 'iiiP'):
            for lab, v in d['rivals_onset'].items():
                nat0[lab][0] += v['n']; nat0[lab][1] += v['resolved']
    out['natural_rivals_onset_pooled_eps0'] = {k: dict(n=v[0], resolved=v[1]) for k, v in nat0.items()}
    out['assays'] = assays()
    vp = os.path.join(ROOT, 'runs', 'annealed-validate.json')
    if os.path.exists(vp): out['validate'] = json.load(open(vp))
    json.dump(out, open(os.path.join(ROOT, 'runs', 'annealed.json'), 'w'), indent=1, default=str)
    # tables
    print('cell | runs | arrivals/isl (by 10k) | drift/isl [CI] | target/rival/unheld | sel | drift-free | uot2/10/12 | uo | identity | idt late | sec | eff | expl | c-o')
    for c, d in out['cells'].items():
        print('%s | %d | %.1f (%.1f) | %.4f %s | %d/%d/%d | %d | %d %s | %d/%d/%d | %d | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f' % (
            c, d['runs'], d['arrivals'], d['arrivals10'], d['drift_per_island'], d['drift_per_island_ci'], d['drift_target'],
            d['drift_rival'], d['drift_unheld'], d['selected'], d['drift_free'], d['drift_free_wilson'], d['uot2'], d['uot10'],
            d['uot'], d['uo'], d['identity'], d['idt_late'], d['secondary'], d['eff'], d['exploitable'], d['closed_open']))
    print('slopes', json.dumps(sl))
    print('partF', json.dumps(fc, default=str))
    print('mix', mix, 'hazards', json.dumps(hz))
    print('paired', json.dumps({k: v for k, v in pc.items() if v}, default=str))
    print('assays', json.dumps(out['assays'], default=str))
    print('natural rivals', dict(out['natural_rivals_onset_pooled_rain']), dict(out['natural_rivals_onset_pooled_eps0']))


if __name__ == '__main__':
    main()
