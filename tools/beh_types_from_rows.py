"""Most common end-of-run island types (top four per island, as stored in the rows) in a cell: python3 tools/beh_types_from_rows.py CELL [N]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import hooks_beh_report as RP
from collections import defaultdict

cell = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 25
rows = RP.load(cell)
agg = defaultdict(int); bases = defaultdict(int); tot = 0
for r in rows:
    at = r['at'][max(r['at'], key=int)]
    for isl, comp in enumerate(at['comp']):
        if at['island_pcc'][isl] < 0.95:
            continue
        for c, t in comp:
            d = at['types'][str(t)]
            nm = d['base'] + ' ' + ' '.join(x.replace('behaviour:', '') for x in d['fills'])
            agg[nm] += c; bases[d['base']] += c; tot += c
print(cell, len(rows), 'runs; individuals counted (top 4 types per efficient island):', tot)
print('bases:')
for b, c in sorted(bases.items(), key=lambda x: -x[1])[:10]:
    print('  %6d %.3f %s' % (c, c / tot, b))
print('types:')
for nm, c in sorted(agg.items(), key=lambda x: -x[1])[:n]:
    print('  %6d %.3f %s' % (c, c / tot, nm))
