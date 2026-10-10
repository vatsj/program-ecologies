"""Report for the identity-and-tags experiment: runs/identity-tags.md and runs/identity-tags.json.

    python3 src/identity_tags_report.py
"""
import json, math, os, sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'identity_tags')


def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def fmt(x, d=4):
    if x is None: return '–'
    if isinstance(x, (int, np.integer)): return str(int(x))
    if x == 0: return '0'
    if abs(x) < 10 ** -(d - 1) or abs(x) >= 10 ** 5: return '%.2e' % x
    return ('%.' + str(d) + 'g') % x


def load(fn):
    p = os.path.join(OUT, fn)
    return json.load(open(p)) if os.path.exists(p) else None


CELL_ORDER = ['L', 'L_N200', 'L_I256', 'U', 'T1a', 'T1b', 'T1c', 'T2', 'T3', 'abl_identity', 'abl_tags', 'abl_cbq']
CELL_DESC = {'L': 'L (100, 64)', 'L_N200': 'L (200, 64)', 'L_I256': 'L (100, 256)', 'U': 'U (100, 64)',
             'T1a': 'T1a: M on EQ', 'T1b': 'T1b: M/10 on ten EQ spellings', 'T1c': 'T1c: M/10 on ten CB spellings, family removed',
             'T2': 'T2: M on TC1¹', 'T3': 'T3: M on XC', 'abl_identity': 'ablation: identity only',
             'abl_tags': 'ablation: tags only', 'abl_cbq': 'ablation: ⌜CB⌝ only'}


def summarize_cell(rows):
    n = len(rows)
    I = rows[0]['I']; N = rows[0]['N']
    pairs = I * (I - 1) / 2
    out = dict(n=n, N=N, I=I)
    for tag in ('h2000', 'end'):
        oc = Counter(r[tag]['outcome'] for r in rows)
        out[tag] = dict(outcomes=dict(oc), universal_open=oc.get('universal-open', 0), universal_other=oc.get('universal-other', 0),
                        patchwork=oc.get('patchwork', 0), failed=oc.get('failed', 0), unresolved=oc.get('unresolved', 0),
                        clique_wins=sum(1 for r in rows if r[tag]['clique_win']),
                        separated=sum(1 for r in rows if r[tag]['separated']),
                        cross_pcc=float(np.mean([r[tag]['cross_pcc'] for r in rows])),
                        island_pcc=float(np.mean([r[tag]['island_pcc'] for r in rows])),
                        occupancy=float(np.mean([r[tag]['occupancy'] for r in rows])),
                        wilson_universal_open=wilson(oc.get('universal-open', 0), n))
    out['E3'] = dict(Counter(r['E3'] for r in rows))
    eg = [r['establish_gen'] for r in rows if r['establish_gen'] >= 0]
    ag = [r['all_established_gen'] for r in rows if r['all_established_gen'] >= 0]
    out['establish_gen_median'] = float(np.median(eg)) if eg else None
    out['all_established_gen_median'] = float(np.median(ag)) if ag else None
    out['n_all_established'] = len(ag)
    ever = [r for r in rows if r['first_sep'] >= 0]
    out['ever_separated'] = len(ever)
    p = len(ever) / n
    out['h_sep_per_pair'] = (-math.log(1 - p) / pairs) if p < 1 else float('inf')
    sep_gen = sum(r['n_sep_checks'] * 10 for r in rows)
    out['resolution_events'] = sum(r['n_resolutions'] for r in rows)
    out['separated_run_generations'] = sep_gen
    out['h_res_per_run_gen'] = out['resolution_events'] / sep_gen if sep_gen else None
    flips = sum(r['n_flips'] for r in rows); exp = sum(r['sep_island_checks'] * 10 for r in rows)
    out['flips'] = flips; out['flip_rate_per_island_gen'] = flips / exp if exp else None
    out['first_sep_median'] = float(np.median([r['first_sep'] for r in ever])) if ever else None
    sep2000 = [r for r in rows if r['h2000']['separated']]
    out['separated_at_2000'] = len(sep2000)
    out['separated_2000_resolved_by_end'] = sum(1 for r in sep2000 if not r['end']['separated'])
    out['separated_2000_end_outcomes'] = dict(Counter(r['end']['outcome'] for r in sep2000))
    # patchwork naming
    pw = Counter()
    for r in rows:
        if r['h2000']['outcome'] == 'patchwork':
            pw[' / '.join(sorted(k for k in r['h2000']['labels']))] += 1
    out['patchwork_labels_2000'] = dict(pw)
    lab2000 = Counter(); labend = Counter()
    for r in rows:
        lab2000.update(r['h2000']['labels']); labend.update(r['end']['labels'])
    out['island_labels_2000'] = {k: v / (n * I) for k, v in lab2000.items()}
    out['island_labels_end'] = {k: v / (n * I) for k, v in labend.items()}
    hold = Counter()
    for r in rows:
        for h, c in r['end']['holders']: hold[h] += c
    out['top_holders_end'] = hold.most_common(6)
    # tracked groups
    tr = {}
    for g in rows[0]['track']:
        rs = [r['track'][g] for r in rows]
        seeded = [x['seeded'] for x in rs]
        ext = [x.get('extinct_gen', -1) for x in rs if x.get('seeded', 0) > 0]
        tr[g] = dict(runs_seeded=sum(1 for s in seeded if s > 0), mean_seeded=float(np.mean(seeded)),
                     extinct=sum(1 for e in ext if e >= 0), median_extinction=float(np.median([e for e in ext if e >= 0])) if any(e >= 0 for e in ext) else None,
                     ever_held_island=sum(1 for x in rs if x.get('max_islands', 0) > 0),
                     alive_at_first_sep=sum(1 for x in rs if x.get('alive_at_first_sep')),
                     alive_at_first_sep_n=sum(1 for x in rs if x.get('alive_at_first_sep') is not None))
    out['track'] = tr
    # pooling
    pc = {}
    for tag in ('h2000', 'end'):
        dec = [r['pooling'][tag] for r in rows if r.get('pooling') and r['pooling'][tag]['decided']]
        bs = sum(1 for d in dec if d['best_seed_won'])
        be = [d['best_est_won'] for d in dec if d['best_est_won'] is not None]
        pc[tag] = dict(decided=len(dec), best_seed_won=bs, best_est_won=sum(be), best_est_n=len(be))
    pc['n_sets_median'] = float(np.median([r['pooling']['n_sets'] for r in rows if r.get('pooling')]))
    pc['incomplete'] = sum(1 for r in rows if r.get('pooling') and not r['pooling']['complete'])
    out['pooling'] = pc
    # seeded label counts (pooling by raw counts)
    slc = defaultdict(list)
    for r in rows:
        for k, v in r['seeded_label_counts'].items(): slc[k].append(v)
    out['seeded_counts_mean'] = {k: float(np.sum(v) / n) for k, v in slc.items()}
    out['time_s_mean'] = float(np.mean([r['time_s'] for r in rows]))
    out['K_present_mean'] = float(np.mean([r['K_present'] for r in rows]))
    return out


def main():
    st = load('static_n7.json'); an = load('static_analysis.json'); va = load('validate.json')
    lot = load('lottery_main.json') or []
    ch = load('chain.json') or []
    by = defaultdict(list)
    for r in lot: by[r['cell']].append(r)
    cells = {c: summarize_cell(by[c]) for c in CELL_ORDER if by.get(c)}
    js = dict(static=st, analysis=an, validate=va, lottery=cells, chain=ch)
    json.dump(js, open(os.path.join(ROOT, 'runs', 'identity-tags.json'), 'w'), indent=1, default=str)
    return js, cells


if __name__ == '__main__':
    js, cells = main()
    for c, s in cells.items():
        h = s['h2000']; e = s['end']
        print('%-14s n=%d univ-open %d other %d patch %d fail %d unres %d | sep2000 %d resolved-by-end %d | end univ-open %d patch %d | cross %.3f / %.3f clique wins %d' % (
            c, s['n'], h['universal_open'], h['universal_other'], h['patchwork'], h['failed'], h['unresolved'], s['separated_at_2000'],
            s['separated_2000_resolved_by_end'], e['universal_open'], e['patchwork'], h['cross_pcc'], e['cross_pcc'], h['clique_wins']))
