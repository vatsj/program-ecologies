"""Aggregate the per-job records of the churn-in-the-primary-object experiment into runs/churn-primary.{md,json} and
runs/churn_primary/ (small per-cell files), and score the predictions by the rules of
predictions/2026-10-25-churn-primary.md.

    python3 src/churn_primary_report.py [--scratch DIR]
"""
import argparse, glob, json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCR = os.environ.get('CP_SCRATCH', '/private/tmp/claude-501/-Users-jstav-code-program-ecologies/'
                     'eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/churn/out')
MNS = (0, 0.01, 0.1, 1)
RNG = np.random.default_rng(20261025)
NB = 2000


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))


def boot_mean(x, nb=NB):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (float('nan'),) * 3
    idx = RNG.integers(0, len(x), (nb, len(x)))
    m = x[idx].mean(1)
    return (float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def boot_ratio(a, b, nb=NB):
    """ratio of means (a over b) with independent run-bootstrap intervals."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    ia = RNG.integers(0, len(a), (nb, len(a))); ib = RNG.integers(0, len(b), (nb, len(b)))
    ma = a[ia].mean(1); mb = b[ib].mean(1)
    with np.errstate(divide='ignore', invalid='ignore'):
        r = ma / mb
    r = r[np.isfinite(r)]
    pt = a.mean() / b.mean() if b.mean() > 0 else float('inf')
    if len(r) == 0:
        return (pt, float('nan'), float('nan'))
    return (float(pt), float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5)))


def boot_hazard(flips, expo, nb=NB):
    f = np.asarray(flips, float); e = np.asarray(expo, float)
    idx = RNG.integers(0, len(f), (nb, len(f)))
    h = f[idx].sum(1) / np.maximum(e[idx].sum(1), 1)
    pt = f.sum() / max(e.sum(), 1)
    return (1e4 * pt, 1e4 * float(np.percentile(h, 2.5)), 1e4 * float(np.percentile(h, 97.5)))


# ---------------------------------------------------------------- loading
def load_lottery(scr):
    """cells[(spec, price)][mN] -> list of per-run records."""
    cells = {}
    for f in sorted(glob.glob(os.path.join(scr, 'L__*.json'))):
        d = json.load(open(f))
        for rec in d['recs']:
            key = (rec['spec'], 'c0' if rec.get('price', 0) else 'c0=0')
            cells.setdefault(key, {}).setdefault(rec['mN'], []).append(rec)
    return cells


def load_balanced(scr):
    cells = {}
    for f in sorted(glob.glob(os.path.join(scr, 'B__*.json'))):
        d = json.load(open(f))
        for rec in d['recs']:
            cells.setdefault((rec['spec'], rec['kind']), {}).setdefault(rec['mN'], []).append(rec)
    return cells


def load_probes(scr):
    out = {}
    for f in sorted(glob.glob(os.path.join(scr, 'P__*.json'))):
        d = json.load(open(f))
        out[d['name']] = d
    return out


# ---------------------------------------------------------------- per-cell statistics
def cell_stats(recs, H=10000):
    n = len(recs)
    g = lambda r: r['snap'][str(H)]
    mm = [r['flips']['mm'] for r in recs]
    expo = [r['flips']['expo'] for r in recs]
    st = dict(n=n)
    st['mm'] = boot_mean(mm); st['mo'] = boot_mean([r['flips']['mo'] for r in recs])
    st['om'] = boot_mean([r['flips']['om'] for r in recs]); st['oo'] = boot_mean([r['flips']['oo'] for r in recs])
    st['hazard'] = boot_hazard(mm, expo)
    cov = [g(r)['nm'] == 3 for r in recs]
    st['cov'] = (float(np.mean(cov)), wilson(int(sum(cov)), n))
    st['cov_avg'] = boot_mean([r['cov_avg'] for r in recs])
    st['vstar'] = boot_mean([g(r)['F'] / 64.0 for r in recs])
    st['cons'] = float(np.mean([g(r)['cons'] for r in recs]))
    st['ts'] = float(np.mean([g(r)['ts'] for r in recs])); st['tv'] = float(np.mean([g(r)['tv'] for r in recs]))
    st['eff'] = boot_mean([1 - g(r)['inef'] for r in recs])
    st['stop'] = float(np.mean([r['stop'] for r in recs]))
    st['closed'] = float(np.mean([r['status'] in (1, 5) for r in recs]))
    rt = {k: int(sum(r['routes'][k] for r in recs)) for k in ('redirect', 'resident', 'reader')}
    st['routes'] = rt
    tot = max(sum(rt.values()), 1)
    st['route_share'] = {k: round(v / tot, 3) for k, v in rt.items()}
    st['K'] = float(np.mean([np.mean(r['K']) for r in recs])) if 'K' in recs[0] else None
    st['mm_runs'] = mm
    return st


def lottery_tables(cells):
    out = {}
    for key, bym in cells.items():
        out[key] = {}
        for mN, recs in sorted(bym.items()):
            out[key][mN] = cell_stats(sorted(recs, key=lambda r: r['run']))
    return out


# ---------------------------------------------------------------- the gate
def gate(cells):
    """B6w against the stored migration-window rows (M-base-N100-m*)."""
    res = {}
    bw = cells.get(('B6w', 'c0=0'), {})
    for mN in MNS:
        name = {0: '0', 0.01: '0.01', 0.1: '0.1', 1: '1'}[mN]
        p = os.path.join(ROOT, 'runs', 'migration_window', 'M-base-N100-m%s.json' % name)
        if not os.path.exists(p) or mN not in bw:
            continue
        sto = json.load(open(p)); sf = sto['snap_fields']
        stored = {r['run']: dict(zip(sf, r['snap']['10000'])) for r in sto['runs']}
        ok = 0; bad = []
        for r in bw[mN]:
            s = stored.get(r['run'])
            if s is None:
                continue
            m = r['snap']['10000']
            same = (m['nm'] == s['nm'] and m['F'] == s['F'] and m['cons'] == s['cons'] and m['U'] == s['U']
                    and abs(m['inef'] - s['inef']) < 1e-4)
            ok += same
            if not same:
                bad.append(r['run'])
        res[mN] = dict(n=len(bw[mN]), same=ok, bad=bad)
    return res


# ---------------------------------------------------------------- verdicts
def ratio_rule(arm, base, mN):
    """returns (ok3, pt, lo, hi, absdiff) for the 'within 3x' rule."""
    a = arm[mN]['mm_runs']; b = base[mN]['mm_runs']
    pt, lo, hi = boot_ratio(a, b)
    bm = float(np.mean(b)); am = float(np.mean(a))
    if bm < 1:
        ok = (am - bm) < 3
    else:
        ok = pt <= 3
    return dict(ok3=bool(ok), ratio=pt, lo=lo, hi=hi, am=am, bm=bm, absdiff=am - bm)


def score_p1(tabs, spec, base_spec='B6w', price='c0=0'):
    arm = tabs.get((spec, price)); base = tabs.get((base_spec, 'c0=0'))
    if arm is None or base is None:
        return None
    rr = {m: ratio_rule(arm, base, m) for m in (0.01, 0.1, 1) if m in arm and m in base}
    cov1 = arm[1]['cov'][0] if 1 in arm else float('nan')
    allok = all(v['ok3'] for v in rr.values())
    r1 = rr.get(1)
    failed = bool(r1 and (r1['ratio'] >= 10 or (r1['bm'] < 1 and r1['absdiff'] >= 10)) and cov1 >= 0.5)
    if failed:
        v = 'failed'
    elif allok and cov1 < 0.3:
        v = 'held'
    else:
        lab = []
        if not allok:
            big = any((x['ratio'] >= 10) for x in rr.values())
            lab.append('flips >= 10x without coverage >= 0.5' if big else 'flips 3-10x')
        if cov1 >= 0.3:
            lab.append('coverage %.2f at mN = 1' % cov1)
        v = 'partial (' + '; '.join(lab) + ')'
    return dict(verdict=v, ratios={str(m): x for m, x in rr.items()}, cov1=cov1)


def score_p4(tabs):
    out = {}
    verdict = 'held'
    rise = False
    for spec in ('E10m', 'E10w', 'T-main'):
        t = tabs.get((spec, 'c0=0'))
        if t is None:
            continue
        cv = {m: t[m]['cov'][0] for m in MNS if m in t}
        ok = cv.get(0, 0) >= 0.8 and cv.get(0.01, 0) >= 0.8 and cv.get(1, 1) <= cv.get(0.01, 0) - 0.3
        bad = cv.get(1, 0) >= cv.get(0.01, 0) - 0.05
        out[spec] = dict(cov=cv, held=bool(ok), failed=bool(bad))
        if bad:
            verdict = 'failed'
        elif not ok and verdict != 'failed':
            verdict = 'partial'
    for spec in ('B6w', 'B6m', 'E10m', 'E10w', 'T-main', 'T-lo', 'T-hi', 'Emin-main-m', 'Emin-hi-m', 'Emin-lo-m', 'Emin-main-w', 'Emin-hi-w', 'Emin-lo-w'):
        t = tabs.get((spec, 'c0=0'))
        if t is None:
            continue
        ms = [m for m in MNS if m in t]
        for a, b in zip(ms, ms[1:]):
            if t[b]['cov'][0] - t[a]['cov'][0] > 0.10:
                rise = True
    return dict(per_arm=out, verdict=verdict, gpt_counter_held=bool(rise))


def probe_summary(P):
    """pooled rates per probe configuration (and per slot) and hom-cell scans."""
    out = {}
    for name, d in P.items():
        if 'cfg' in d and d['cfg']:
            cfg = d['cfg']
            rows = cfg['rows']
            pooled = {}
            for lab, sl in (('all', None), ('s0', (0,)), ('s1', (1,)), ('s2', (2,))):
                ks = [k for k in rows if sl is None or int(k.split(':')[0]) in sl]
                n = sum(rows[k]['n'] for k in ks); sw = sum(rows[k]['sw'] for k in ks); left = sum(rows[k]['left'] for k in ks)
                tk = sum(rows[k]['takeover'] for k in ks); dr = sum(rows[k]['drift'] for k in ks); rd = sum(rows[k]['redirect'] for k in ks)
                unres = sum(rows[k]['unres'] for k in ks)
                pooled[lab] = dict(n=n, sw=sw, left=left, rate=sw / n if n else float('nan'), ci=wilson(sw, n), takeover=tk,
                                   drift=dr, redirect=rd, unres=unres)
            out[name] = dict(pooled=pooled, resident_ok=cfg['resident_ok'], accept=cfg.get('accept'), N=cfg['N'], rows=rows,
                             traces=cfg.get('traces', []))
        elif 'hom' in d:
            fr = {}
            for f, cfg in d['hom'].items():
                rows = cfg['rows']
                n = sum(r['n'] for r in rows.values()); sw = sum(r['sw'] for r in rows.values()); left = sum(r['left'] for r in rows.values())
                redirs = [r['redir0'] for r in rows.values() if r['redir0'] is not None]
                fr[f] = dict(n=n, sw=sw, left=left, rate=sw / n if n else float('nan'), ci=wilson(sw, n),
                             mean_redirect0=float(np.mean(redirs)) if redirs else float('nan'),
                             resident_ok=cfg['resident_ok'])
            out[name] = dict(hom=fr, rows={f: cfg['rows'] for f, cfg in d['hom'].items()},
                             traces={f: cfg.get('traces', []) for f, cfg in d['hom'].items()})
    return out


def score_p3(ps):
    """pooled switching rate in stratum (a) of the churn-capable readers (switch, two), immigrants into slot 1 (the
    member j), in each grammar; held < 5% in both, failed >= 20% in either."""
    res = {}
    for g in ('dm', 'dw', 't'):
        n = sw = 0
        for kind in ('switch', 'two'):
            d = ps.get('P-%s-%s-a-single' % (g, kind))
            if d:
                n += d['pooled']['s1']['n']; sw += d['pooled']['s1']['sw']
        res[g] = dict(n=n, sw=sw, rate=sw / n if n else float('nan'), ci=wilson(sw, n))
    rates = [res[g]['rate'] for g in ('dm', 't') if res[g]['n']]
    if not rates:
        return dict(verdict='not run', by=res)
    if any(r >= 0.20 for r in rates):
        v = 'failed'
    elif all(r < 0.05 for r in rates):
        v = 'held'
    else:
        v = 'partial'
    return dict(verdict=v, by=res)


def f3(x):
    return '%.3f' % x if isinstance(x, float) and not math.isnan(x) else str(x)


def ci3(t):
    return '%.2f [%.2f, %.2f]' % t if t[0] == t[0] else 'n/a'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scratch', default=SCR)
    ap.add_argument('--out', default=os.path.join(ROOT, 'runs', 'churn-primary'))
    a = ap.parse_args()
    cells = load_lottery(a.scratch)
    tabs = lottery_tables(cells)
    bal = load_balanced(a.scratch)
    baltabs = {k: {m: cell_stats(sorted(v, key=lambda r: r['run'])) for m, v in sorted(bm.items())} for k, bm in bal.items()}
    probes = load_probes(a.scratch)
    ps = probe_summary(probes)
    G = gate(cells)
    verdicts = {}
    for spec in ('E10m', 'E10w', 'B6m', 'Emin-lo-m', 'Emin-main-m', 'Emin-hi-m', 'Emin-lo-w', 'Emin-main-w', 'Emin-hi-w',
                 'T-lo', 'T-main', 'T-hi'):
        verdicts['P1/P2 ' + spec] = score_p1(tabs, spec)
    for spec in ('T-main', 'T-hi'):
        verdicts['c0 ' + spec] = score_p1(tabs, spec, price='c0')
    verdicts['P4'] = score_p4(tabs)
    verdicts['P3'] = score_p3(ps)
    # gemini-4-argon's counter-prediction: T-hi R >= 3 at mN in {0.1, 1} and R(T-hi) >= 2 R(T-lo)
    gem = {}
    if ('T-hi', 'c0=0') in tabs and ('T-lo', 'c0=0') in tabs and ('B6w', 'c0=0') in tabs:
        for m in (0.1, 1):
            rh = ratio_rule(tabs[('T-hi', 'c0=0')], tabs[('B6w', 'c0=0')], m); rl = ratio_rule(tabs[('T-lo', 'c0=0')], tabs[('B6w', 'c0=0')], m)
            gem[str(m)] = dict(R_hi=rh['ratio'], R_lo=rl['ratio'], held=bool(rh['ratio'] >= 3 and rh['ratio'] >= 2 * rl['ratio']))
    verdicts['gemini counter (P2)'] = dict(by_mN=gem, held=any(v['held'] for v in gem.values()) if gem else None)
    # gpt counter on P2: redirect share > 0.2 while switching < 0.2 in the homogeneous cell
    for name in ('H-dm', 'H-dw', 'H-t'):
        if name in ps:
            fr = ps[name]['hom']
            ok = any(fr[f]['mean_redirect0'] > 0.2 and fr[f]['rate'] < 0.2 for f in fr)
            verdicts['gpt counter (P2) ' + name] = dict(held=bool(ok), cells={f: (round(fr[f]['mean_redirect0'], 3), round(fr[f]['rate'], 3)) for f in fr})
    # thresholds in the hom cell
    thr = {}
    for name in ('H-dm', 'H-dw', 'H-t'):
        if name in ps:
            fr = ps[name]['hom']
            t = None
            for f in sorted(fr, key=float):
                if fr[f]['rate'] >= 0.5:
                    t = float(f); break
            thr[name] = t
    verdicts['hom threshold (switching >= 0.5)'] = thr
    # write json
    os.makedirs(os.path.join(ROOT, 'runs', 'churn_primary'), exist_ok=True)
    js = dict(gate=G, verdicts=verdicts, lottery={'%s|%s' % k: {str(m): {kk: vv for kk, vv in v.items() if kk != 'mm_runs'} for m, v in t.items()}
                                                 for k, t in tabs.items()},
              balanced={'%s|%s' % k: {str(m): {kk: vv for kk, vv in v.items() if kk != 'mm_runs'} for m, v in t.items()} for k, t in baltabs.items()},
              probes={k: {kk: vv for kk, vv in v.items() if kk != 'rows'} for k, v in ps.items()})
    json.dump(js, open(a.out + '.json', 'w'), default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o), indent=1)
    # per-cell small files
    for key, bym in cells.items():
        spec, price = key
        d = {str(m): [dict(run=r['run'], mm=r['flips']['mm'], mo=r['flips']['mo'], om=r['flips']['om'], oo=r['flips']['oo'],
                           expo=r['flips']['expo'], stop=r['stop'], status=r['status'], nm=r['snap']['10000']['nm'],
                           F=r['snap']['10000']['F'], cons=r['snap']['10000']['cons'], routes=r['routes']) for r in sorted(recs, key=lambda x: x['run'])]
             for m, recs in bym.items()}
        json.dump(d, open(os.path.join(ROOT, 'runs', 'churn_primary', '%s__%s.json' % (spec, price)), 'w'))
    # markdown
    L = []
    P = L.append
    P('# Does churn among the fair pairs happen in the primary object? (run report, 2026-10-25)\n')
    P('Spec `specs/2026-10-25-churn-primary.md`, predictions `predictions/2026-10-25-churn-primary.md`, notes `notes/churn-primary.md`. '
      'Code `src/churn_primary*.py`. Per-run summaries `runs/churn_primary/`. All cells: eps = 0, N = 100, I = 64, 10,000 generations, '
      '40 runs, founders common across mN.\n')
    P('## Gate: B6w against the stored `M-base-N100` rows (coverage, consensus, class counts, inefficiency at generation 10,000)\n')
    for m, v in G.items():
        P('- mN = %g: %d of %d runs identical%s' % (m, v['same'], v['n'], '' if not v['bad'] else ' (differing runs %s)' % v['bad']))
    P('')
    P('## Lottery cells: member-to-member flips per run, hazard, coverage\n')
    P('Flips are debounced (25 generations) changes of an island\'s modal outcome from one fair pair to another (m>m); '
      'hazard = m>m flips per 10^4 fair-pair island-generations up to the stop generation. Coverage = the three fair pairs are each the '
      'modal outcome of at least one island at generation 10,000. Ratio = m>m flips per run over B6w\'s at the same mN '
      '(independent run bootstrap). Intervals are 95%.\n')
    order = ['B6w', 'B6m', 'E10m', 'E10w', 'Emin-lo-m', 'Emin-main-m', 'Emin-hi-m', 'Emin-lo-w', 'Emin-main-w', 'Emin-hi-w', 'T-lo', 'T-main', 'T-hi']
    base = tabs.get(('B6w', 'c0=0'))
    P('| cell | mN | runs | m>m flips/run | ratio to B6w | hazard /10^4 | coverage | V* share | consensus | closed | routes (redirect / resident / reader) |')
    P('|---|---|---|---|---|---|---|---|---|---|---|')
    abl = ['Emin-abS-m', 'Emin-abZ-m', 'Emin-abD-m', 'T-abS', 'T-abZ', 'T-abD']
    for spec, price in [(x, 'c0=0') for x in order + abl] + [('T-main', 'c0'), ('T-hi', 'c0')]:
        if True:
            t = tabs.get((spec, price))
            if t is None:
                continue
            nm_ = spec if price == 'c0=0' else spec + '@c0'
            for m in MNS:
                if m not in t:
                    continue
                s = t[m]
                ratio = ''
                if base and m in base and m > 0 and not (spec == 'B6w' and price == 'c0=0'):
                    pt, lo, hi = boot_ratio(s['mm_runs'], base[m]['mm_runs'])
                    ratio = '%.2f [%.2f, %.2f]' % (pt, lo, hi)
                rt = s['routes']
                P('| %s | %g | %d | %s | %s | %s | %s | %s | %.2f | %.2f | %d / %d / %d |' % (
                    nm_, m, s['n'], ci3(s['mm']), ratio, ci3(s['hazard']), '%.2f %s' % (s['cov'][0], s['cov'][1]),
                    ci3(s['vstar']), s['cons'], s['closed'], rt['redirect'], rt['resident'], rt['reader']))
    P('')
    P('## Balanced start with resident readers (extension)\n')
    P('| catalogue | pair slots | mN | runs | m>m flips/run | hazard /10^4 | coverage | V* share | consensus |')
    P('|---|---|---|---|---|---|---|---|---|')
    for (spec, kind), t in sorted(baltabs.items()):
        for m, s in sorted(t.items()):
            P('| %s | %s | %g | %d | %s | %s | %s | %s | %.2f |' % (spec, kind, m, s['n'], ci3(s['mm']), ci3(s['hazard']),
                                                                     '%.2f %s' % (s['cov'][0], s['cov'][1]), ci3(s['vstar']), s['cons']))
    P('')
    P('## Probe (single immigrants; switch = final modal outcome is a different fair pair)\n')
    P('| configuration | N | resident outcome ok | pooled n | switches | rate [Wilson] | left {0,1} | takeover / drift / redirect | slot 1 only | slot 2 only |')
    P('|---|---|---|---|---|---|---|---|---|---|')
    for name in sorted(ps):
        v = ps[name]
        if 'pooled' not in v:
            continue
        p = v['pooled']['all']
        P('| %s | %d | %s | %d | %d | %.3f %s | %d | %d / %d / %d | %.3f | %.3f |' % (
            name, v['N'], v['resident_ok'], p['n'], p['sw'], p['rate'], p['ci'], p['left'], p['takeover'], p['drift'], p['redirect'],
            v['pooled']['s1']['rate'], v['pooled']['s2']['rate']))
    P('')
    P('## Homogeneous-reader cell (immigrants into slot 1; rate = switching to another fair pair)\n')
    for name in ('H-dm', 'H-dw', 'H-t'):
        if name in ps:
            P('**%s**\n' % name)
            P('| fraction | n | switches | rate [Wilson] | left {0,1} | mean encounter redirect share at injection |')
            P('|---|---|---|---|---|---|')
            for f in sorted(ps[name]['hom'], key=float):
                x = ps[name]['hom'][f]
                P('| %s | %d | %d | %.3f %s | %d | %.3f |' % (f, x['n'], x['sw'], x['rate'], x['ci'], x['left'], x['mean_redirect0']))
            P('')
    P('## Verdicts\n')
    for k, v in verdicts.items():
        P('- **%s**: %s' % (k, json.dumps(v, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))[:900]))
    open(a.out + '.md', 'w').write('\n'.join(L) + '\n')
    print('wrote', a.out + '.md', 'and .json')


if __name__ == '__main__':
    main()
