"""Tables for runs/certificates-as-genes.md from runs/lt_genes/*.json.

    python3 src/lt_genes_report.py            # prints markdown sections and writes runs/certificates-as-genes.json
"""
import json
import math
import os
import sys
from collections import defaultdict

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'lt_genes')


def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def load(name):
    p = os.path.join(OUT, name)
    return json.load(open(p)) if os.path.exists(p) else None


# ------------------------------------------------------------------ single pairs
KEY_PAIRS = [('CB', 'CB'), ('CB', 'CBlet'), ('CB', 'MC1'), ('CB1', 'CB1r'), ('CBP', 'CBPh'), ('CB', 'CB1'),
             ('CB1', 'CB'), ('CB', 'CBP'), ('CBP', 'CB'), ('CB1', 'CBP'), ('CBP', 'CBPr'), ('LobC', 'CB'),
             ('Cc', 'CB'), ('Dc', 'CB'), ('CBdef', 'CB'), ('SFc', 'CB'), ('CB', 'SFc')]


def pairs_tables(rows, rule='lack'):
    rows = [r for r in rows if r.get('rule', 'lack') == rule or (r['setting'] == 'HH' and r['alloc'] == 'post')]
    out = {}
    main = [r for r in rows if r['K'] == 10 ** 6 and r['P'] == 250000 and r['alloc'] == 'post' and not r['negcache']]
    idx = {(r['x'], r['y'], r['setting']): r for r in main}
    lines = ['| x, y | ' + ' | '.join(['HH', 'CH', 'SH', 'CSH', 'CC', 'CC+', 'SS', 'CSCS']) + ' |',
             '|---|' + '---|' * 8]
    for x, y in KEY_PAIRS:
        cells = []
        for st in ['HH', 'CH', 'SH', 'CSH', 'CC', 'CC+', 'SS', 'CSCS']:
            r = idx.get((x, y, st))
            if r is None: cells.append('–'); continue
            e1, e2 = r['encs'][0]['act'], r['encs'][1]['act']
            sc = r['steady_cc']
            cells.append('%s→%s%s' % (e1, e2, (' (st %d, %s)' % (sc, '%.1fk' % (r['cost_x_last'] / 1000))) if sc else ''))
        lines.append('| %s, %s | %s |' % (x, y, ' | '.join(cells)))
    out['main_table'] = '\n'.join(lines)
    # RE 1 at the named level: (C, H) carrier pairs: adopted a C script (an edge) vs (C, C) at encounter 2
    on = off = on_ok = off_coop = 0
    ex_on, ex_off = [], []
    ratios = []
    for (x, y, st), r in idx.items():
        if st != 'CH' or x == y: continue
        hh = idx.get((x, y, 'HH'))
        if hh is None or hh['encs'][0]['act'] != 'CC': continue
        edge = any(a == 'C' and how == 'copy' for a, s_, how in r['encs'][0]['adx'])
        coop2 = r['encs'][1]['act'] == 'CC'
        if edge:
            on += 1; on_ok += coop2
            if not coop2: ex_on.append((x, y))
            if r['steady_cc']:
                ratios.append((x, y, r['cost_x_last'] / max(1, hh['cost_x_last'])))
        else:
            off += 1; off_coop += coop2
            if coop2: ex_off.append((x, y))
    out['re1_named'] = dict(on_graph=on, on_graph_coop_enc2=on_ok, off_graph=off, off_graph_coop_enc2=off_coop,
                            on_fail=ex_on, off_coop_examples=ex_off,
                            steady_cost_ratio=dict(max=max(r[2] for r in ratios) if ratios else None,
                                                   min=min(r[2] for r in ratios) if ratios else None,
                                                   examples=sorted(ratios, key=lambda z: -z[2])[:8]))
    # S restores every HH-cooperating carrier pair?
    sres = {}
    for st in ('SH', 'SS', 'CSH', 'CSCS', 'CC', 'CC+'):
        n = k2 = k3 = never = 0
        firsts = defaultdict(int)
        for (x, y, s), r in idx.items():
            if s != st: continue
            hh = idx.get((x, y, 'HH'))
            if hh is None or hh['encs'][0]['act'] != 'CC' or x == y and st in ('SS', 'CSCS', 'CC'): pass
            if hh is None or hh['encs'][0]['act'] != 'CC': continue
            n += 1
            fc = r['first_cc']
            firsts[fc] += 1
            if fc is not None and fc <= 2: k2 += 1
            if fc is not None and fc <= 3: k3 += 1
            if fc is None: never += 1
        sres[st] = dict(pairs=n, by_enc2=k2, by_enc3=k3, never=never, first_cc=dict(firsts))
    out['restoration'] = sres
    # costs of production
    prod = defaultdict(list)
    for r in main:
        for e in r['encs']:
            for k, v, n_, d in e['evx']:
                prod[(k, v)].append(n_)
    out['act_costs'] = {'%s:%s' % k: dict(n=len(v), median=float(np.median(v)), max=int(max(v)), min=int(min(v)))
                        for k, v in prod.items()}
    # caps
    caps = defaultdict(lambda: dict(seqs=0, capTO=0, found=0, coop_by3=0))
    for r in rows:
        if r['alloc'] != 'post' or r['setting'] not in ('SH', 'CSH', 'SS') or r['negcache']: continue
        key = '%s K=%g P=%g' % (r['setting'], r['K'], r['P'])
        c = caps[key]
        c['seqs'] += 1
        for e in r['encs']:
            for k, v, n_, d in e['evx']:
                if k in ('prodC', 'prodD') and v == 'capTO': c['capTO'] += 1
                if k in ('prodC', 'prodD') and v == 'found': c['found'] += 1
        if r['first_cc'] is not None and r['first_cc'] <= 3: c['coop_by3'] += 1
    out['caps'] = dict(caps)
    # reserved
    res = defaultdict(lambda: dict(seqs=0, coop_last=0, bot=0))
    for r in rows:
        if r['alloc'] != 'reserved': continue
        key = '%s Kplay=%g R=%g' % (r['setting'], r['K'], r['reserve'])
        c = res[key]
        c['seqs'] += 1
        c['coop_last'] += r['encs'][-1]['act'] == 'CC'
        c['bot'] += sum(e['botx'] or e['boty'] for e in r['encs'])
    out['reserved'] = dict(res)
    # fakers
    fk = {}
    for r in rows:
        if r['x'] == 'CF' and r['K'] == 10 ** 6 and not r['negcache']:
            fk['%s %s' % (r['y'], r['setting'])] = dict(adopted=[a for e in r['encs'] for a in e['adx']],
                                                        refusal_steps_enc1=sum(r['encs'][0]['px'].values()),
                                                        acts=[e['act'] for e in r['encs']])
    out['CF'] = fk
    cfC = sum(1 for v in fk.values() for a in v['adopted'] if a[0] == 'C')
    out['CF_C_adoptions'] = cfC
    # negative cache
    nc = []
    for r in rows:
        if r['negcache'] and r['setting'] == 'CH':
            base = idx.get((r['x'], r['y'], 'CH'))
            if base:
                nc.append((r['x'], r['y'], base['prod_x_last'], r['prod_x_last']))
    out['negcache'] = dict(n=len(nc), mean_uncached=float(np.mean([z[2] for z in nc])) if nc else None,
                           mean_cached=float(np.mean([z[3] for z in nc])) if nc else None,
                           examples=sorted(nc, key=lambda z: -z[2])[:8])
    return out


# ------------------------------------------------------------------ lottery
def lottery_tables(rows):
    cells = defaultdict(list)
    for r in rows: cells[r['cell']].append(r)
    out = {}
    for c, rs in cells.items():
        n = len(rs)
        est = [r['establish_gen'] for r in rs]
        ne = sum(1 for e in est if e >= 0)
        times = sorted([e if e >= 0 else 10 ** 9 for e in est])
        med = times[n // 2] if ne * 2 > n else None
        q25 = times[n // 4] if ne * 4 > n else None
        e3 = sum(1 for r in rs if r['E3'] == 'success')
        e3f = sum(1 for r in rs if r['E3'] == 'fail')
        fin = [r['final'] for r in rs]
        oc = defaultdict(int)
        for f in fin: oc[f['outcome']] += 1
        uo = sum(1 for f in fin if f['universal_open'])
        modes = {s: np.mean([r['snaps'][str(s)]['mode_coop'] for r in rs if str(s) in r['snaps']], axis=0).tolist()
                 for s in (10, 50, 200, 1000, 2000) if any(str(s) in r['snaps'] for r in rs)}
        ctr = np.sum([r['ctr'] for r in rs], axis=0)
        steps = np.sum([r['steps_mode'] for r in rs], axis=0)
        enc = ctr[:, 0]
        per_match = (steps / np.maximum(enc, 1)).tolist()
        pers = [r['persistence'] for r in rs if r.get('persistence') is not None]
        out[c] = dict(
            runs=n, established=ne, est_ci=wilson(ne, n), est_median=med, est_q25=q25,
            E3_success=e3, E3_fail=e3f, E3_ci=wilson(e3, n),
            outcomes=dict(oc), universal_open=uo, uo_ci=wilson(uo, n),
            pcc=float(np.mean([f['pcc'] for f in fin])), held=float(np.mean([f['held'] for f in fin])),
            identity_islands=float(np.mean([f['identity_islands'] for f in fin])) / 64,
            open_islands=float(np.mean([f['open_islands'] for f in fin])) / 64,
            cross_pcc=float(np.mean([f['cross_pcc'] for f in fin if f['cross_pcc'] is not None])),
            persistence=float(np.mean(pers)) if pers else None,
            modes_coop=modes,
            per_match_prod_steps=per_match,
            counters=dict(enc=enc.tolist(), gate=ctr[:, 1].tolist(), gate_T=ctr[:, 2].tolist(),
                          prodC=ctr[:, 3].tolist(), prodC_ok=ctr[:, 4].tolist(), prodD=ctr[:, 5].tolist(),
                          prodD_ok=ctr[:, 6].tolist(), ac=ctr[:, 7].tolist(), ac_ok=ctr[:, 8].tolist(),
                          ac_screen0=ctr[:, 9].tolist(), transfer_fail=ctr[:, 10].tolist(), births=ctr[:, 11].tolist(),
                          changes=ctr[:, 12].tolist(), transfer_unknown=ctr[:, 14].tolist(), prod_timeouts=ctr[:, 15].tolist()),
            scripts_held=dict(mean=float(np.mean([f['scripts_held'] for f in fin])), max=int(max(f['scripts_held'] for f in fin))),
            inst_search_frac=float(np.sum([f['inst_search'] for f in fin]) / max(1, np.sum([f['inst_host'] + f['inst_search'] for f in fin]))),
            hostfree_distinct=[f['hostfree_distinct_coop'] for f in fin],
            n_types=float(np.mean([r['n_types'] for r in rs])), time_s=float(np.mean([r['time_s'] for r in rs])))
    return out


def main():
    rep = {}
    for nm in ('validate.json', 'graph.json', 'costs.json'):
        rep[nm[:-5]] = load(nm)
    pr = load('pairs.json')
    if pr:
        rep['pairs'] = pairs_tables(pr, 'lack')
        rep['pairs_gate'] = pairs_tables([r for r in pr if r.get('rule') == 'gate' or r['setting'] == 'HH'], 'gate')
    lot = []
    for fn in sorted(os.listdir(OUT)):
        if fn.startswith('lottery_') and fn.endswith('.json'):
            lot.extend(json.load(open(os.path.join(OUT, fn))))
    if lot: rep['lottery'] = lottery_tables(lot)
    json.dump(rep, open(os.path.join(ROOT, 'runs', 'certificates-as-genes.json'), 'w'), indent=1, default=str)
    if 'pairs' in rep:
        print(rep['pairs']['main_table'])
        print(json.dumps({k: v for k, v in rep['pairs'].items() if k != 'main_table'}, indent=1, default=str)[:6000])
    if 'lottery' in rep:
        for c, v in rep['lottery'].items():
            print(c, json.dumps({k: v[k] for k in ('runs', 'established', 'est_median', 'E3_success', 'outcomes', 'universal_open',
                                                  'pcc', 'identity_islands', 'persistence', 'per_match_prod_steps')}, default=str))


if __name__ == '__main__':
    main()
