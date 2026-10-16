"""Bounds on C-donor's universal-on-target at 2,000 from the stored holder spellings (notes §2.3)."""
import gzip
import json
import os
import sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance_run as PR
import removing_rivals as RR

ROOT = RR.ROOT


def main():
    LS = PR.lot_static(); S = RR.static(LS)
    utau = np.asarray(LS['st']['utau']); tau = LS['tau']
    st = defaultdict(lambda: [0, 0])
    for u in np.nonzero(S['sa'] == 1)[0]:
        st[int(utau[u])][int(S['T'][u])] += 1
    def tree_status(s):
        v = st[int(tau[s])]
        return 'T' if v[0] == 0 and v[1] > 0 else ('N' if v[1] == 0 else 'M')
    rows = []
    for f in ('lottery_cdon', 'lottery_cdon400'):
        rows += json.load(gzip.open(os.path.join(ROOT, 'runs', 'realizable_scaling', f + '.json.gz')))
    out = {}
    for cell in ('rs_Cdon_200_64_cal', 'rs_Cdon_400_64_cal', 'rs_Cdon_200_128_cal', 'rs_Cdon_100_256_cal'):
        rs = [r for r in rows if r['cell'] == cell]
        lo = hi = 0; uo = 0
        for r in rs:
            isl = r['isl'].get('2000') or r['final_isl']
            if not isl['universal_open']: continue
            uo += 1
            ss = set(tree_status(s) for s in isl['holder_sp'])
            if ss == {'T'}: lo += 1; hi += 1
            elif 'N' not in ss: hi += 1
        out[cell] = dict(runs=len(rs), universal_open=uo, uot_lower=lo, uot_upper=hi)
    json.dump(out, open(os.path.join(ROOT, 'runs', 'removing_rivals', 'cdonor_bounds.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
