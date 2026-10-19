"""Hooks, Part W: report (runs/hooks-w.md, runs/hooks-w.json) from runs/hooks_w/*.json.

    python3 src/hooks_w_report.py
"""
import json, os, sys, glob, math
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import hooks_w as H
import hooks_w_run as R

ROOT = H.ROOT
OUT = os.path.join(ROOT, 'runs', 'hooks_w')
SC = H.SCOPES
OG = H.ORIGINS


def load(cell, prefix=''):
    p = os.path.join(OUT, '%s%s.json' % (prefix, cell))
    if not os.path.exists(p):
        return []
    return [r for r in json.load(open(p)) if 'error' not in r]


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def boot_mean(v, B=4000, seed=0):
    v = np.asarray(v, float)
    if len(v) == 0:
        return (float('nan'), float('nan'), float('nan'))
    rng = np.random.default_rng(seed)
    bs = rng.choice(v, size=(B, len(v))).mean(1)
    return (float(v.mean()), float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975)))


def paired(a, b, key, at):
    """Paired run-level difference a - b of statistic key at generation `at` (rows matched by rep)."""
    da = {r['rep']: r for r in a}; db = {r['rep']: r for r in b}
    reps = sorted(set(da) & set(db))
    v = [float(da[r]['at'][at][key]) - float(db[r]['at'][at][key]) for r in reps if at in da[r]['at'] and at in db[r]['at']]
    return boot_mean(v) + (len(v),)


def region(d):
    if d <= -0.2:
        return 'down'
    if d >= 0.2:
        return 'up'
    if abs(d) <= 0.1:
        return 'flat'
    return 'grey'


# ------------------------------------------------------------------ PD
def pd_cell(rows, at='1000'):
    rr = [r for r in rows if at in r['at']]
    n = len(rr)
    if n == 0:
        return None
    A = [r['at'][at] for r in rr]
    out = dict(n=n)
    for k in ('efficient_run', 'universal_open', 'universal_target', 'universal_current'):
        k_ = sum(bool(a[k]) for a in A)
        out[k] = (k_ / n, wilson(k_, n))
    for k in ('eff_islands', 'pcc', 'lineage_closed', 'rival'):
        out[k] = boot_mean([a[k] for a in A])
    # time-averaged island efficiency over the checkpoints in [500, at]
    g = int(at)
    out['eff_tavg'] = boot_mean([np.mean([x['eff'] for x in r['ts'] if g // 2 <= x['gen'] <= g]) for r in rr])
    ts = [[x for x in r['ts'] if x['gen'] == g][0] for r in rr]
    out['gentle'] = boot_mean([x['gentle'] for x in ts])
    out['gentle_holder'] = boot_mean([x['gentle_holder'] for x in ts])
    held = np.array([x['held'] for x in ts], float).sum(0)          # carried*32 + scope*8 + origin*2 + action
    tot = held.sum()
    out['held_total_per_program'] = float(np.mean([x['fills_per'] for x in ts]))
    out['held_by_scope'] = {SC[s]: float(held[[c * 32 + s * 8 + o * 2 + a for c in (0, 1) for o in range(4) for a in (0, 1)]].sum() / tot) if tot else 0.0 for s in range(4)}
    out['held_by_origin'] = {OG[o]: float(held[[c * 32 + s * 8 + o * 2 + a for c in (0, 1) for s in range(4) for a in (0, 1)]].sum() / tot) if tot else 0.0 for o in range(4)}
    out['held_carried'] = float(held[32:].sum() / tot) if tot else 0.0
    # base programs of island majorities
    from collections import Counter
    cnt = Counter()
    for a in A:
        for m in a['majority']:
            cnt[a['types'][str(m)]['base']] += 1
    out['majority_bases'] = cnt.most_common(6)
    # encounter levels per scope (whole run), per encounter
    es = np.array([r['enc_stats'] for r in rr], float).sum(0)       # level, scope, origin
    enc = sum(r['counters'][0] for r in rr)
    out['enc'] = {SC[s]: [float(es[l, s].sum() / enc) for l in range(4)] for s in range(4)}
    out['enc_origin'] = {OG[o]: [float(es[l, :, o].sum() / enc) for l in range(4)] for o in range(4)}
    c = np.array([r['counters'] for r in rr], float).sum(0)
    out['per_encounter'] = dict(grudge=c[1] / c[0], thanks=c[2] / c[0], inplace=c[3] / c[0], evict=c[4] / c[0],
                                copies=c[5] / c[0], contract_attempts=c[6] / c[0], contracts=c[7] / c[0],
                                changed=c[9] / c[0]) if c[0] else {}
    out['overflow_runs'] = sum(1 for r in rr if r.get('overflow'))
    out['seeded_by_scope'] = {SC[s]: int(np.sum([r['seeded'][s] for r in rr])) for s in range(4)}
    return out


def gentle_by_island(rows, cell, at='1000'):
    """Island-level gentle-holder share from the four largest types of each island (post hoc: types rebuilt from
    their descriptors and evaluated as strangers against DefectBot under the cell's activity)."""
    Lx = R.lang(True)
    active = R.CELLS[cell]['active']
    recency = R.CELLS[cell].get('recency', 0)
    LA = Lx.arrays()
    out = {}
    cache = {}
    for r in rows:
        if at not in r['at']:
            continue
        a = r['at'][at]
        vals = []
        for isl in a['comp']:
            g = 0; tot = 0
            for c_, t in isl:
                d = a['types'][str(t)]
                key = (d['base'], tuple(d['fills']))
                if key not in cache:
                    b = Lx.names.index(d['base'])
                    fl = []
                    for s in d['fills']:
                        sc, og, act, k, tg = s.split(':')
                        fl.append(H.fcode(1 if act == 'C' else 0, int(tg[1:]), SC.index(sc), OG.index(og), int(k)))
                    f = np.zeros(4, np.int64); f[:len(fl)] = fl
                    sp = int(H.spec_of(f, len(fl), Lx.b_tags[b], active, recency, -1))
                    ax, ay, _, _ = H.eval_match(*LA, Lx.iC, Lx.iD, b, sp, sp, sp, Lx.bD, 0, 0, 0)
                    holder = any(s.startswith('history') for s in d['fills'])
                    cache[key] = (ax == 1, holder)
                gt, ho = cache[key]
                tot += c_
                if gt and ho:
                    g += c_
            vals.append(g / tot if tot else 0.0)
        out[r['rep']] = (vals, r['island_conc'])
    return out


def re2(rows_m, rows_off, cell_off, at='1000'):
    gm = gentle_by_island(rows_m, 'maximal', at); go = gentle_by_island(rows_off, cell_off, at)
    reps = sorted(set(gm) & set(go))
    d_run = [np.mean(gm[r][0]) - np.mean(go[r][0]) for r in reps]
    # by tertile of the island repeat-encounter rate (lineage concentration in the maximal run)
    conc = np.concatenate([gm[r][1] for r in reps]); dd = np.concatenate([np.array(gm[r][0]) - np.array(go[r][0]) for r in reps])
    q = np.quantile(conc, [1 / 3, 2 / 3]) if len(conc) else [0, 0]
    terc = []
    for lo, hi in ((-1, q[0]), (q[0], q[1]), (q[1], 2)):
        m = (conc > lo) & (conc <= hi)
        terc.append(boot_mean(dd[m]) + (int(m.sum()),))
    return dict(run=boot_mean(d_run) + (len(d_run),), tertiles=terc, conc_cuts=[float(x) for x in q])


# ------------------------------------------------------------------ SOG
def sog_cell(rows):
    n = len(rows)
    if n == 0:
        return None
    out = dict(n=n)
    for k in ('fair', 'intermediate', 'zero'):
        out[k] = boot_mean([r[k] for r in rows])
    out['strike'] = boot_mean([r['shares']['strike'] for r in rows])
    out['scab split'] = boot_mean([r['shares']['scab split'] for r in rows])
    out['repression'] = boot_mean([r['shares']['repression:strike'] + r['shares']['repression:source'] for r in rows])
    if 'threat' in rows[0]:
        thr = np.array([r['threat'] for r in rows], float).sum(0)          # slot, (held, held active, challenged, executed)
        out['threat'] = {['boss', 'W1', 'W2'][s]: dict(held=thr[s, 0], held_active=thr[s, 1], challenged=thr[s, 2],
                                                       executed=thr[s, 3],
                                                       exec_rate=(thr[s, 3] / thr[s, 0]) if thr[s, 0] else float('nan'),
                                                       exec_rate_active=(thr[s, 3] / thr[s, 1]) if thr[s, 1] else float('nan'))
                         for s in range(3)}
        c = np.array([r['counters'] for r in rows], float).sum(0)
        out['per_encounter'] = dict(grudge=c[1] / c[0], thanks=c[2] / c[0], copies=c[5] / c[0],
                                    contract_attempts=c[6] / c[0], contracts=c[7] / c[0], changed=c[9] / c[0]) if c[0] else {}
        es = np.array([r['enc_stats'] for r in rows], float).sum(0)
        out['enc'] = {SC[s]: [float(es[l, s].sum() / c[0]) for l in range(3)] for s in range(4)} if c[0] else {}
        held = np.array([r['held'] for r in rows], float).sum(0)            # slot, scope, origin, threat
        out['held_by_scope'] = {SC[s]: float(held[:, s].sum() / held.sum()) for s in range(4)} if held.sum() else {}
        out['threat_held_share'] = {['boss', 'W1', 'W2'][s]: float(held[s, :, :, 1].sum() / held[s].sum()) if held[s].sum() else 0.0 for s in range(3)}
        out['boss'] = boot_mean([r['boss'] for r in rows]); out['worker'] = boot_mean([r['worker'] for r in rows])
        out['whack'] = boot_mean([r['whack'] for r in rows])
        out['wage'] = [float(np.mean([r['wage'][w] for r in rows])) for w in range(3)]
    return out


def sog_paired(a, b, key):
    da = {r['rep']: r for r in a}; db = {r['rep']: r for r in b}
    reps = sorted(set(da) & set(db))
    v = [da[r][key] - db[r][key] for r in reps]
    return boot_mean(v) + (len(v),)


def fmt(m):
    if isinstance(m, tuple) and len(m) >= 3 and not isinstance(m[1], tuple):
        return '%.3f [%.3f, %.3f]' % m[:3]
    if isinstance(m, tuple) and isinstance(m[1], tuple):
        return '%.3f [%.2f, %.2f]' % (m[0], m[1][0], m[1][1])
    return str(m)


def main():
    pd = {}
    for c in R.ORDER_PD + R.ORDER_FF:
        rows = load(c)
        if not rows:
            continue
        at = '600' if c.startswith('ff-') else '1000'
        pd[c] = dict(at1000=pd_cell(rows, at))
        if c in ('baseline', 'inert', 'maximal'):
            pd[c]['at2000'] = pd_cell(rows, '2000')
    sog = {}
    for c in ['baseline', 'plain', 'inert', 'maximal', 'seeding-only', 'grudge-only', 'no-contract', 'no-history',
              'no-behaviour', 'no-role']:
        rows = load(c, 'sog-')
        if rows:
            sog[c] = sog_cell(rows)
    # paired comparisons (PD at 1,000; FF at 600)
    comps = {}
    ref = {'maximal': load('maximal'), 'inert': load('inert'), 'baseline': load('baseline')}
    for c in pd:
        if c.startswith('ff-'):
            continue
        rows = load(c)
        for rn, rrows in ref.items():
            if c == rn:
                continue
            comps['%s-%s' % (c, rn)] = {k: paired(rows, rrows, k, '1000') for k in ('universal_open', 'universal_current', 'eff_islands', 'lineage_closed', 'pcc')}
    ffref = load('ff-inert')
    for c in ('ff-baseline', 'ff-maximal', 'ff-grudge-only'):
        rows = load(c)
        if rows and ffref:
            comps['%s-ff-inert' % c] = {k: paired(rows, ffref, k, '600') for k in ('universal_open', 'eff_islands', 'lineage_closed')}
    sogc = {}
    for c in sog:
        for rn in ('inert', 'baseline', 'maximal'):
            if c != rn and rn in sog:
                sogc['%s-%s' % (c, rn)] = {k: sog_paired(load(c, 'sog-'), load(rn, 'sog-'), k) for k in ('fair', 'intermediate', 'zero')}
    extra = {}
    if load('maximal') and load('no-writes'):
        extra['re2_no_writes'] = re2(load('maximal'), load('no-writes'), 'no-writes')
    if load('maximal') and load('no-history'):
        extra['re2_no_history'] = re2(load('maximal'), load('no-history'), 'no-history')
    out = dict(pd=pd, sog=sog, pd_paired=comps, sog_paired=sogc, extra=extra)
    json.dump(out, open(os.path.join(ROOT, 'runs', 'hooks-w.json'), 'w'), indent=1, default=float)
    write_md(out)


def write_md(o):
    L = []
    w = L.append
    w('# Hooks, Part W: run report (generated by src/hooks_w_report.py)\n')
    w('PD islands (100, 64), mN = 1, 40 runs, compared at generation 1,000 (baseline, inert, maximal also at 2,000); '
      'fission-fusion 32 x 100 merged at 200, horizon 600, 20 runs; social organization (30, 16), mN = 1, horizon '
      '1,000, 40 runs.  Means with bootstrap or Wilson 95% intervals.  Every number is an eps = 0 lottery statistic at '
      'finite (N, I, horizon).\n')
    w('## PD cells\n')
    w('| cell | n | efficient runs | universal-open | universal-target | universal-current | island eff. | island eff. (time avg) | P(C,C) | lineage-closed | rival |')
    w('|---|---|---|---|---|---|---|---|---|---|---|')
    for c, d in o['pd'].items():
        for lab in ('at1000', 'at2000'):
            x = d.get(lab)
            if not x:
                continue
            w('| %s%s | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                c, '' if lab == 'at1000' else ' (2,000)', x['n'], fmt(x['efficient_run']), fmt(x['universal_open']),
                fmt(x['universal_target']), fmt(x['universal_current']), fmt(x['eff_islands']), fmt(x['eff_tavg']),
                fmt(x['pcc']), fmt(x['lineage_closed']), fmt(x['rival'])))
    w('\n### Held fills, gentle programs and majority bases (generation 1,000; fission-fusion 600)\n')
    w('| cell | fills / program | held by scope (none, role, history, behaviour) | held by origin (seeded, written, copied, contract) | carried | gentle | gentle holders | majority bases |')
    w('|---|---|---|---|---|---|---|---|')
    for c, d in o['pd'].items():
        x = d['at1000']
        w('| %s | %.2f | %s | %s | %.2f | %.4f | %.4f | %s |' % (
            c, x['held_total_per_program'], ', '.join('%.2f' % x['held_by_scope'][s] for s in SC),
            ', '.join('%.2f' % x['held_by_origin'][g] for g in OG), x['held_carried'], x['gentle'][0], x['gentle_holder'][0],
            '; '.join('%s %d' % b for b in x['majority_bases'][:3])))
    w('\n### Fill levels per sampled encounter (whole run): held / applicable / selected / executed\n')
    w('| cell | none | role | history | behaviour | writes (grudge, thanks) | copies | contracts (attempts) | outcome changed by a fill |')
    w('|---|---|---|---|---|---|---|---|---|')
    for c, d in o['pd'].items():
        x = d['at1000']
        pe = x['per_encounter']
        if not pe:
            continue
        w('| %s | %s | %s | %s | %s | %.3f, %.3f | %.4f | %.4f (%.3f) | %.3f |' % (
            c, *['/'.join('%.3f' % v for v in x['enc'][s]) for s in SC], pe['grudge'], pe['thanks'], pe['copies'],
            pe['contracts'], pe['contract_attempts'], pe['changed']))
    w('\n### Paired run-level differences (generation 1,000; mean [95%], n)\n')
    w('| comparison | universal-open | universal-current | island eff. | lineage-closed | P(C,C) |')
    w('|---|---|---|---|---|---|')
    for k, d in o['pd_paired'].items():
        w('| %s | %s |' % (k, ' | '.join('%.3f [%.3f, %.3f] (%d)' % d[s] if s in d else '-' for s in ('universal_open', 'universal_current', 'eff_islands', 'lineage_closed', 'pcc'))))
    if o['extra']:
        w('\n### RE 2: gentle-holder share, maximal minus control, by island repeat-encounter tertile\n')
        for k, d in o['extra'].items():
            w('- %s: run-level %.4f [%.4f, %.4f] (n %d); tertiles (low, mid, high concentration; cuts %s): %s' % (
                k, *d['run'], ', '.join('%.3f' % c for c in d['conc_cuts']),
                '; '.join('%.4f [%.4f, %.4f] (%d islands)' % t for t in d['tertiles'])))
    w('\n## Social organization cells\n')
    w('| cell | n | fair | intermediate | zero wage | strike | scab split | repression | boss payoff | worker payoff | whack rate |')
    w('|---|---|---|---|---|---|---|---|---|---|---|')
    for c, x in o['sog'].items():
        w('| %s | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            c, x['n'], fmt(x['fair']), fmt(x['intermediate']), fmt(x['zero']), fmt(x['strike']), fmt(x['scab split']),
            fmt(x['repression']), fmt(x['boss']) if 'boss' in x else '-', fmt(x['worker']) if 'worker' in x else '-',
            fmt(x['whack']) if 'whack' in x else '-'))
    w('\n### Threat fills (whole run): held fill-encounters, challenged (selected on path), executed, execution rate\n')
    w('| cell | boss held / challenged / executed (rate) | W1 | W2 | threat share of held fills (boss, W1, W2) |')
    w('|---|---|---|---|---|')
    for c, x in o['sog'].items():
        if 'threat' not in x:
            continue
        t = x['threat']
        w('| %s | %s | %s | %s | %s |' % (c, *['%d / %d / %d (%.2g)' % (t[s]['held'], t[s]['challenged'], t[s]['executed'], t[s]['exec_rate']) for s in ('boss', 'W1', 'W2')],
                                          ', '.join('%.2f' % x['threat_held_share'][s] for s in ('boss', 'W1', 'W2'))))
    w('\n### Social organization: per-encounter fill activity and held kinds\n')
    w('| cell | writes (grudge, thanks) | copies | contracts (attempts) | outcome changed | held by scope (none, role, history, behaviour) | wage paid when someone works (0, 1/4, 1/2) |')
    w('|---|---|---|---|---|---|---|')
    for c, x in o['sog'].items():
        if 'per_encounter' not in x or not x['per_encounter']:
            continue
        pe = x['per_encounter']
        w('| %s | %.3f, %.3f | %.4f | %.4f (%.3f) | %.3f | %s | %s |' % (c, pe['grudge'], pe['thanks'], pe['copies'], pe['contracts'],
                                                                     pe['contract_attempts'], pe['changed'],
                                                                     ', '.join('%.2f' % x['held_by_scope'].get(s, 0) for s in SC),
                                                                     ', '.join('%.3f' % v for v in x['wage'])))
    w('\n### Social organization paired differences (mean [95%], n)\n')
    w('| comparison | fair | intermediate | zero wage |')
    w('|---|---|---|---|')
    for k, d in o['sog_paired'].items():
        w('| %s | %s |' % (k, ' | '.join('%.3f [%.3f, %.3f] (%d)' % d[s] for s in ('fair', 'intermediate', 'zero'))))
    open(os.path.join(ROOT, 'runs', 'hooks-w.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
