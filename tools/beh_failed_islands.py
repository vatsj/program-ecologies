"""Class composition (at the last record) of efficient and non-efficient islands per cell: python3 tools/beh_failed_islands.py CELL..."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
import numpy as np
import hooks_beh_report as RP
from collections import Counter

for cell in sys.argv[1:]:
    rows = RP.load(cell)
    maj_f = Counter(); maj_w = Counter(); sh_f = np.zeros(8); sh_w = np.zeros(8); nf = nw = 0
    for r in rows:
        t = RP.ts_at(r, r['gens'])
        if t is None or t.get('cls') is None:
            continue
        c = np.array(t['cls']); isl = np.array(t['isl_pcc'])
        for i in range(len(isl)):
            share = c[i] / c[i].sum()
            if isl[i] < 0.95:
                maj_f[RP.CL[int(np.argmax(c[i]))]] += 1; sh_f += share; nf += 1
            else:
                maj_w[RP.CL[int(np.argmax(c[i]))]] += 1; sh_w += share; nw += 1
    print(cell, 'efficient islands', nw, 'non-efficient', nf)
    print('  efficient: majority class', dict(maj_w), ' mean shares', {RP.CL[k]: round(sh_w[k] / max(nw, 1), 3) for k in range(8) if sh_w[k] > 0})
    print('  non-efficient: majority class', dict(maj_f), ' mean shares', {RP.CL[k]: round(sh_f[k] / max(nf, 1), 3) for k in range(8) if sh_f[k] > 0})
