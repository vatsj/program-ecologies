"""Hooks, Part W2: report (runs/hooks-w2.md, runs/hooks-w2.json) from runs/hooks_w2/*.json (and Part W's stored
rows runs/hooks_w/*.json.gz for the inert, baseline and strict-ablation references).

    python3 src/hooks_w2_report.py
"""
import json, os, sys, gzip, math
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import hooks_w2 as H

ROOT = H.ROOT
OUT = os.path.join(ROOT, 'runs', 'hooks_w2')
STORED = os.path.join(ROOT, 'runs', 'hooks_w')
NI_SOG = 30 * 16                      # workers per slot at (30, 16)


def load(cell, prefix='', stored=False):
    d = STORED if stored else OUT
    p = os.path.join(d, '%s%s.json' % (prefix, cell))
    if os.path.exists(p):
        return [r for r in json.load(open(p)) if 'error' not in r]
    if os.path.exists(p + '.gz'):
        return [r for r in json.load(gzip.open(p + '.gz')) if 'error' not in r]
    return []


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


def region(d):
    if d <= -0.2:
        return 'down'
    if d >= 0.2:
        return 'up'
    if abs(d) <= 0.1:
        return 'flat'
    return 'grey'


def paired_at(a, b, key, at):
    da = {r['rep']: r for r in a}; db = {r['rep']: r for r in b}
    reps = sorted(set(da) & set(db))
    v = [float(da[r]['at'][at][key]) - float(db[r]['at'][at][key]) for r in reps if at in da[r]['at'] and at in db[r]['at']]
    return boot_mean(v) + (len(v),)


def paired_key(a, b, key):
    da = {r['rep']: r for r in a}; db = {r['rep']: r for r in b}
    reps = sorted(set(da) & set(db))
    v = [float(da[r][key]) - float(db[r][key]) for r in reps]
    return boot_mean(v) + (len(v),)


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
    g = int(at)
    ts = [[x for x in r['ts'] if x['gen'] == g][0] for r in rr]
    out['open_holders'] = [float(np.mean([x['open_holders'][j] for x in ts])) for j in range(4)] if 'open_holders' in ts[0] else None
    out['fills_per'] = float(np.mean([x['fills_per'] for x in ts]))
    out['types'] = float(np.mean([x['types'] for x in ts]))
    held = np.array([x['held'] for x in ts], float).sum(0)
    tot = held.sum()
    SC = H.SCOPES
    out['held_by_scope'] = {SC[s]: float(held[[c * 32 + s * 8 + o * 2 + a for c in (0, 1) for o in range(4) for a in (0, 1)]].sum() / tot) if tot else 0.0 for s in range(4)}
    from collections import Counter
    cnt = Counter()
    for a in A:
        for m in a['majority']:
            cnt[a['types'][str(m)]['base']] += 1
    out['majority_bases'] = cnt.most_common(5)
    # contract survival on winning islands
    eff_i = sum(sum(1 for p in a['island_pcc'] if p >= 0.95) for a in A)
    if 'island_openc' in A[0]:
        out['win_openc'] = sum(sum(1 for p, o in zip(a['island_pcc'], a['island_openc']) if p >= 0.95 and o) for a in A) / eff_i if eff_i else float('nan')
        out['win_fb'] = sum(sum(1 for p, o in zip(a['island_pcc'], a['island_fb']) if p >= 0.95 and o) for a in A) / eff_i if eff_i else float('nan')
        out['win_open_self'] = sum(sum(1 for p, o in zip(a['island_pcc'], a['island_open_self']) if p >= 0.95 and o) for a in A) / eff_i if eff_i else float('nan')
    c = np.array([r['counters'] for r in rr], float).sum(0)
    enc = c[0]
    out['per_encounter'] = dict(grudge=c[1] / enc, thanks=c[2] / enc, copies=c[5] / enc, attempts=c[6] / enc,
                                candidates=c[11] / enc, accepted=c[7] / enc, open_writes=c[17] / enc,
                                changed=c[9] / enc) if enc else {}
    out['accept_per_attempt'] = float(c[7] / c[6]) if c[6] else float('nan')
    out['sucker_open'] = (float(c[14] / c[13]) if c[13] else float('nan'), int(c[13]), int(c[14]))
    out['sucker_lineage'] = (float(c[16] / c[15]) if c[15] else float('nan'), int(c[15]), int(c[16]))
    es = np.array([r['enc_stats'] for r in rr], float).sum(0)            # level, scope, origin
    act = {}
    for nm, sc in (('open contract', 3), ('lineage contract', 2)):
        held_ = es[0, sc, 3]
        act[nm] = dict(held=held_ / enc, selected=es[2, sc, 3] / held_ if held_ else float('nan'),
                       applicable=es[1, sc, 3] / held_ if held_ else float('nan'),
                       executed=es[3, sc, 3] / held_ if held_ else float('nan'))
    out['activation'] = act
    return out


# ------------------------------------------------------------------ union game
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
    out['runs_with_fair'] = float(np.mean([r['fair'] > 0 for r in rows]))
    out['worker'] = boot_mean([r['worker'] for r in rows]); out['boss'] = boot_mean([r['boss'] for r in rows])
    out['wage'] = [float(np.mean([r['wage'][w] for r in rows])) for w in range(3)]
    c = np.array([r['counters'] for r in rows], float).sum(0)
    out['per_encounter'] = dict(grudge=c[1] / c[0], thanks=c[2] / c[0], copies=c[5] / c[0], bw_attempts=c[6] / c[0],
                                bw_contracts=c[7] / c[0], blocked=c[18] / c[0]) if c[0] else {}
    thr = np.array([r['threat'] for r in rows], float).sum(0)
    out['threat'] = {['boss', 'W1', 'W2'][s]: dict(held=thr[s, 0], challenged=thr[s, 2], executed=thr[s, 3],
                                                   exec_rate=(thr[s, 3] / thr[s, 0]) if thr[s, 0] else float('nan'))
                     for s in range(3)}
    if rows[0].get('ustat') is not None and sum(rows[0]['ustat']) + sum(sum(r['ustat']) for r in rows[1:]) > 0:
        u = np.array([r['ustat'] for r in rows], float).sum(0)
        enc = c[0]
        d = dict(attempts=u[0], attempts_per_enc=u[0] / enc, candidates=u[1], acc_q=u[2], acc_h=u[3],
                 adoption_per_enc=(u[2] + u[3]) / enc, adoption_per_attempt=(u[2] + u[3]) / u[0] if u[0] else float('nan'),
                 boss_response=u[4], raises=u[5], tamings=u[6], raises_const_boss=u[7], accepted_const_boss=u[8],
                 pred_wage=[u[9], u[10], u[11]], pre_wage=[u[12], u[13], u[14]])
        for j, nm in ((0, '1/4'), (1, '1/2')):
            ch = u[15 + j]
            d['s=' + nm] = dict(challenges=ch, executions=u[17 + j], exec_rate=u[17 + j] / ch if ch else float('nan'),
                                demand_met=u[19 + j] / ch if ch else float('nan'),
                                realized_wage=[u[21 + 3 * j + w] for w in range(3)])
        uh = np.array([r['union_held'] for r in rows], float).mean(0)       # slot, s
        d['held_union_share'] = {'s=1/4': float((uh[1, 0] + uh[2, 0]) / (2 * NI_SOG)), 's=1/2': float((uh[1, 1] + uh[2, 1]) / (2 * NI_SOG))}
        out['union'] = d
    return out


def fmt(m):
    if isinstance(m, tuple) and len(m) >= 3 and not isinstance(m[1], tuple):
        return '%.3f [%.3f, %.3f]' % m[:3]
    if isinstance(m, tuple) and isinstance(m[1], tuple):
        return '%.3f [%.2f, %.2f]' % (m[0], m[1][0], m[1][1])
    return str(m)


PD_CELLS = ['lineage-max', 'open-max', 'open-contract', 'open-history', 'open-max-nocontract-strict', 'open-writes-only',
           'open-grudge-only', 'open-thanks-only']
FF_CELLS = ['ff-lineage-max', 'ff-open-max']
SOG_CELLS = ['myopic-ref', 'union-M', 'union-C', 'bw-only-C', 'union-C-role']


def main():
    pd = {}
    for c in PD_CELLS:
        rows = load(c)
        if rows:
            pd[c] = pd_cell(rows, '1000')
    for c in FF_CELLS:
        rows = load(c)
        if rows:
            pd[c] = pd_cell(rows, '600')
    for c in ('inert', 'baseline', 'no-contract-strict', 'maximal'):
        rows = load(c, stored=True)
        if rows:
            pd['W:' + c] = pd_cell(rows, '1000')
    for c in ('ff-baseline', 'ff-inert', 'ff-maximal'):
        rows = load(c, stored=True)
        if rows:
            pd['W:' + c] = pd_cell(rows, '600')
    sog = {}
    for c in SOG_CELLS:
        rows = load(c, 'sog-')
        if rows:
            sog[c] = sog_cell(rows)
    for c in ('inert', 'baseline', 'maximal', 'no-contract-strict'):
        rows = load(c, 'sog-', stored=True)
        if rows and 'threat' in rows[0] or (rows and c == 'baseline'):
            try:
                sog['W:' + c] = sog_cell(rows) if 'threat' in rows[0] else dict(n=len(rows), **{k: boot_mean([r[k] for r in rows]) for k in ('fair', 'intermediate', 'zero')})
            except Exception:
                pass
    comps = {}
    ref = load('lineage-max')
    for c in ('open-max', 'open-contract', 'open-history', 'open-max-nocontract-strict', 'open-writes-only', 'open-grudge-only', 'open-thanks-only'):
        rows = load(c)
        if rows and ref:
            comps['%s - lineage-max' % c] = {k: paired_at(rows, ref, k, '1000') for k in ('universal_open', 'universal_current', 'eff_islands', 'lineage_closed', 'pcc')}
    if load('open-contract') and load('open-history'):
        comps['open-contract - open-history'] = {k: paired_at(load('open-contract'), load('open-history'), k, '1000') for k in ('universal_open', 'eff_islands')}
    for c, rf in (('ff-open-max', 'ff-lineage-max'),):
        if load(c) and load(rf):
            comps['%s - %s' % (c, rf)] = {k: paired_at(load(c), load(rf), k, '600') for k in ('universal_open', 'eff_islands', 'lineage_closed')}
    sogc = {}
    sref = load('myopic-ref', 'sog-')
    for c in ('union-M', 'union-C', 'union-C-role', 'bw-only-C'):
        rows = load(c, 'sog-')
        if rows and sref:
            sogc['%s - myopic-ref' % c] = {k: paired_key(rows, sref, k) for k in ('fair', 'intermediate', 'zero', 'worker')}
    for a_, b_ in (('union-C-role', 'union-C'), ('union-C', 'union-M')):
        if load(a_, 'sog-') and load(b_, 'sog-'):
            sogc['%s - %s' % (a_, b_)] = {k: paired_key(load(a_, 'sog-'), load(b_, 'sog-'), k) for k in ('fair', 'intermediate', 'zero', 'worker')}
    repro = {}
    for name, new, old, at, kind in (('lineage-max vs Part W maximal', load('lineage-max'), load('maximal', stored=True), '1000', 'pd'),
                                      ('ff-lineage-max vs Part W ff-maximal', load('ff-lineage-max'), load('ff-maximal', stored=True), '600', 'pd'),
                                      ('myopic-ref vs Part W sog-maximal', load('myopic-ref', 'sog-'), load('maximal', 'sog-', stored=True), None, 'sog')):
        d_old = {r['rep']: r for r in old}
        same = 0; tot = 0
        for r in new:
            if r['rep'] not in d_old:
                continue
            o_ = d_old[r['rep']]; tot += 1
            if kind == 'pd':
                same += int(r['at'][at]['island_pcc'] == o_['at'][at]['island_pcc'] and r['at'][at]['majority'] == o_['at'][at]['majority'])
            else:
                same += int(r['labels'] == o_['labels'] and r['counters'][:11] == o_['counters'][:11])
        repro[name] = dict(runs=tot, identical=same)
    out = dict(pd=pd, sog=sog, pd_paired=comps, sog_paired=sogc, reproduction=repro)
    json.dump(out, open(os.path.join(ROOT, 'runs', 'hooks-w2.json'), 'w'), indent=1, default=float)
    write_md(out)


def write_md(o):
    L = []
    w = L.append
    SC = H.SCOPES
    w('# Hooks, Part W2: run report (generated by src/hooks_w2_report.py)\n')
    w('PD islands (100, 64), mN = 1, 40 runs, compared at generation 1,000; fission-fusion 32 x 100 merged at 200, '
      'horizon 600, 20 runs; union game (30, 16), mN = 1, horizon 1,000, 40 runs.  Rows prefixed `W:` are Part W\'s '
      'stored rows (same founders, fills and seeds).  Means with bootstrap or Wilson 95% intervals.  Every number is an '
      'eps = 0 lottery statistic at finite (N, I, horizon).\n')
    w('## Reproduction of Part W (same founders, fills and seeds, open flags off)\n')
    for k, d in o['reproduction'].items():
        w('- %s: %d of %d runs identical (island states / labels and counters)' % (k, d['identical'], d['runs']))
    w('')
    w('## PD cells\n')
    w('| cell | n | efficient runs | universal-open | universal-target | universal-current | island eff. | P(C,C) | lineage-closed | rival |')
    w('|---|---|---|---|---|---|---|---|---|---|')
    for c, x in o['pd'].items():
        w('| %s | %d | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            c, x['n'], fmt(x['efficient_run']), fmt(x['universal_open']), fmt(x['universal_target']),
            fmt(x['universal_current']), fmt(x['eff_islands']), fmt(x['pcc']), fmt(x['lineage_closed']), fmt(x['rival'])))
    w('\n### Open fills, contract survival, majority bases (generation 1,000; fission-fusion 600)\n')
    w('| cell | individuals holding: open fill / open contract / lineage contract / open written | winning islands: majority holds open contract / is FairBot-compatible / open to itself | majority bases | types | fills per program |')
    w('|---|---|---|---|---|---|')
    for c, x in o['pd'].items():
        oh = x['open_holders']
        w('| %s | %s | %s | %s | %.0f | %.2f |' % (
            c, '-' if oh is None else ' / '.join('%.3f' % v for v in oh),
            '-' if 'win_openc' not in x else '%.3f / %.3f / %.3f' % (x['win_openc'], x['win_fb'], x['win_open_self']),
            '; '.join('%s %d' % b for b in x['majority_bases'][:3]), x['types'], x['fills_per']))
    w('\n### Contract technology: attempts, candidates, accepted per sampled encounter; sucker rates; activation of contract fills\n')
    w('| cell | attempts | candidates | accepted | accepted per attempt | sucker rate, open-contract holders (n, events) | sucker rate, lineage-contract holders (n, events) | open contract fills: held per encounter / selected / executed (per held) | lineage contract fills: same |')
    w('|---|---|---|---|---|---|---|---|---|')
    for c, x in o['pd'].items():
        pe = x['per_encounter']
        if not pe:
            continue
        a1 = x['activation']['open contract']; a2 = x['activation']['lineage contract']
        w('| %s | %.4f | %.4f | %.5f | %.3f | %.4f (%d, %d) | %.4f (%d, %d) | %.4f / %.3f / %.3f | %.4f / %.3f / %.3f |' % (
            c, pe['attempts'], pe['candidates'], pe['accepted'], x['accept_per_attempt'], *x['sucker_open'], *x['sucker_lineage'],
            a1['held'], a1['selected'], a1['executed'], a2['held'], a2['selected'], a2['executed']))
    w('\n### Paired run-level differences (generation 1,000; fission-fusion 600; mean [95%], n)\n')
    w('| comparison | universal-open | universal-current | island eff. | lineage-closed | P(C,C) |')
    w('|---|---|---|---|---|---|')
    for k, d in o['pd_paired'].items():
        w('| %s | %s |' % (k, ' | '.join('%.3f [%.3f, %.3f] (%d) %s' % (d[s] + (region(d[s][0]),)) if s in d else '-' for s in ('universal_open', 'universal_current', 'eff_islands', 'lineage_closed', 'pcc'))))
    w('\n## Union game cells\n')
    w('| cell | n | fair | intermediate (1/4) | zero wage | strike | scab split | runs with a fair island | worker payoff | boss payoff |')
    w('|---|---|---|---|---|---|---|---|---|---|')
    for c, x in o['sog'].items():
        w('| %s | %d | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            c, x['n'], fmt(x['fair']), fmt(x['intermediate']), fmt(x['zero']), fmt(x.get('strike', ('nan',) * 3)) if 'strike' in x else '-',
            fmt(x['scab split']) if 'scab split' in x else '-', '%.3f' % x['runs_with_fair'] if 'runs_with_fair' in x else '-',
            fmt(x['worker']) if 'worker' in x else '-', fmt(x['boss']) if 'boss' in x else '-'))
    w('\n### Union contracts: adoption, acceptance, execution (whole run, summed over runs)\n')
    w('| cell | attempts (both workers hooked) per encounter | adopted per encounter (s = 1/4, 1/2) | adopted per attempt | boss responded with a fill | raises / tamings | raises against constant bosses / accepted against constant bosses | predicted wage at acceptance (0, 1/4, 1/2) | pre-contract wage (0, 1/4, 1/2) | held demand share of workers at horizon (1/4, 1/2) |')
    w('|---|---|---|---|---|---|---|---|---|---|')
    for c, x in o['sog'].items():
        u = x.get('union')
        if not u:
            continue
        w('| %s | %.4f | %.5f (%d, %d) | %.4f | %d | %d / %d | %d / %d | %s | %s | %.3f, %.3f |' % (
            c, u['attempts_per_enc'], u['adoption_per_enc'], u['acc_q'], u['acc_h'], u['adoption_per_attempt'], u['boss_response'],
            u['raises'], u['tamings'], u['raises_const_boss'], u['accepted_const_boss'],
            ', '.join('%d' % v for v in u['pred_wage']), ', '.join('%d' % v for v in u['pre_wage']),
            u['held_union_share']['s=1/4'], u['held_union_share']['s=1/2']))
    w('\n### Union fills on path: challenges, executions (strike played), demand met, realized wage (0, 1/4, 1/2)\n')
    w('| cell | s | challenges | executions | execution rate | demand met | realized wage under challenge |')
    w('|---|---|---|---|---|---|---|')
    for c, x in o['sog'].items():
        u = x.get('union')
        if not u:
            continue
        for s in ('s=1/4', 's=1/2'):
            d = u[s]
            w('| %s | %s | %d | %d | %.4f | %.3f | %s |' % (c, s, d['challenges'], d['executions'], d['exec_rate'], d['demand_met'],
                                                           ', '.join('%d' % v for v in d['realized_wage'])))
    w('\n### Threat fills (Part W definitions: worker strike fills, boss whack fills) and fill activity\n')
    w('| cell | boss held / challenged / executed (rate) | W1 | W2 | grudge, thanks per enc. | copies | bw contracts (attempts) | writes blocked by protection |')
    w('|---|---|---|---|---|---|---|---|')
    for c, x in o['sog'].items():
        if 'threat' not in x:
            continue
        t = x['threat']; pe = x['per_encounter']
        w('| %s | %s | %.3f, %.3f | %.4f | %.5f (%.4f) | %.5f |' % (
            c, ' | '.join('%d / %d / %d (%.2g)' % (t[s]['held'], t[s]['challenged'], t[s]['executed'], t[s]['exec_rate']) for s in ('boss', 'W1', 'W2')),
            pe['grudge'], pe['thanks'], pe['copies'], pe['bw_contracts'], pe['bw_attempts'], pe['blocked']))
    w('\n### Union-game paired differences (mean [95%], n)\n')
    w('| comparison | fair | intermediate | zero wage | worker payoff |')
    w('|---|---|---|---|---|')
    for k, d in o['sog_paired'].items():
        w('| %s | %s |' % (k, ' | '.join('%.3f [%.3f, %.3f] (%d) %s' % (d[s] + (region(d[s][0]),)) for s in ('fair', 'intermediate', 'zero', 'worker'))))
    open(os.path.join(ROOT, 'runs', 'hooks-w2.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
