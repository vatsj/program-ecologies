"""The RS's criterion (notes §1.9): selected versus drift colonizations under rain, per-arrival colonization
probabilities by class and N, and the admissible window (RE 8), from B1 branches and the B2 / B3 cells."""
import json
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import removing_rivals as RR

OUT = RR.OUT


def load(n):
    p = os.path.join(OUT, n)
    return json.load(open(p)) if os.path.exists(p) else []


def summarize(units):
    """units: list of dicts with N, I, gens, epsN, colonizations, by_class, cures (rival cures, B1 only), mu (list)."""
    out = {}
    by = defaultdict(list)
    for u in units: by[(u['epsN'], u['N'])].append(u)
    for (e, N), us in sorted(by.items()):
        ig = sum(u['I'] * u['gens'] for u in us)
        col = [c for u in us for c in u['colonizations']]
        drift = [c for c in col if c['cls'] != 'selected']
        shadow = [c for c in drift if c['status_at_arrival'] == 1]
        sel = [c for c in col if c['cls'] == 'selected']
        cls = defaultdict(lambda: [0, 0])
        for u in us:
            for k, v in u['by_class'].items():
                cls[k][0] += v[0]; cls[k][1] += v[1]
        prob = {k: dict(arrivals=v[0], colonized=v[1], p=(v[1] / v[0]) if v[0] else None) for k, v in sorted(cls.items())}
        cures = sum(u.get('cures', 0) for u in us)
        runs_window = sum(1 for u in us if u.get('cures', 0) > 0 and not any(c['cls'] != 'selected' for c in u['colonizations']))
        runs_cured = sum(1 for u in us if u.get('cures', 0) > 0)
        islands = sum(u['I'] for u in us)
        out['%g|%d' % (e, N)] = dict(
            units=len(us), island_gens=ig, colonizations=len(col), selected=len(sel), drift=len(drift),
            drift_per_isl_gen=len(drift) / ig if ig else None, drift_per_64_islands_per_10k=len(drift) / ig * 64 * 1e4,
            shadow=len(shadow), shadow_by_target_after=sum(1 for c in shadow if c['on_target_after']),
            drift_on_rival=sum(1 for c in drift if c['status_at_arrival'] == 2),
            drift_on_unheld=sum(1 for c in drift if c['status_at_arrival'] == 0),
            selected_on_rival=sum(1 for c in sel if c['status_at_arrival'] == 2),
            selected_on_target=sum(1 for c in sel if c['status_at_arrival'] == 1),
            top_drift=Counter(c['spelling'] for c in drift).most_common(5),
            top_selected=Counter(c['spelling'] for c in sel).most_common(5),
            cures=cures, runs_cured=runs_cured, runs_window=runs_window, islands=islands,
            cures_per_drift=(cures / len(drift)) if drift else None, by_class=prob)
    return out


def main():
    units = []
    ck = {(r['cell'], r['rep']): r for r in load('ckpt_rows.json')}
    for r in load('branch_main.json'):
        c = ck[(r['cell'], r['rep'])]
        for b in r['branches']:
            if b['epsN'] == 0: continue
            a = b['arrivals']
            cures = sum(1 for x in b['islands'] if x['label'] == 'exploitable' and x['resolved'])
            units.append(dict(src='B1', cell=r['cell'], rep=r['rep'], N=c['N'], I=c['I'], gens=b['g_end'] - b['g0'],
                              epsN=b['epsN'], colonizations=a.get('colonizations') or [], by_class=a.get('by_class') or {},
                              cures=cures))
    b1 = summarize(units)
    units2 = []
    for r in load('lottery_B.json'):
        a = r['arrivals']
        units2.append(dict(src=r['cell'], N=r['N'], I=r['I'], gens=r['last_gen'], epsN=r['epsN'] + (0.001 if 'spon' in r['cell'] else 0),
                           colonizations=a.get('colonizations') or [], by_class=a.get('by_class') or {}))
    b23 = summarize(units2)
    out = dict(B1=b1, B2B3=b23, note='B2B3 keys: epsN|N, sponsored+rain cells at epsN + 0.001')
    json.dump(out, open(os.path.join(RR.ROOT, 'runs', 'removing-rivals-drift.json'), 'w'), indent=1, default=str)
    for part in ('B1', 'B2B3'):
        print(part)
        for k, v in out[part].items():
            print(' ', k, {kk: vv for kk, vv in v.items() if kk not in ('by_class',)})
            for kk, vv in v['by_class'].items():
                if vv['arrivals'] >= 20: print('     ', kk, vv)


if __name__ == '__main__':
    main()
