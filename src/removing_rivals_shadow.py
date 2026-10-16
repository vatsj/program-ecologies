"""Static check (post hoc, after the B3 diagnostic): exploitable shadows.  Fresh founders whose phenotype against a
target holder is itself a target unit (they drift neutrally inside target islands) but which some identity holder
exploits (the identity unit is cooperated with and defects).  Reports their prior mass by the target holder met."""
import json
import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import provenance_run as PR
import removing_rivals as RR


def main():
    LS = PR.lot_static(); S = RR.static(LS)
    A, T, names, mu = S['A'], S['T'], LS['names'], LS['mu']
    ck = json.load(open(os.path.join(RR.OUT, 'ckpt_rows.json')))
    rowsA = json.load(open(os.path.join(RR.OUT, 'lottery_A.json')))
    idu = set()
    tgt = Counter()
    for r in ck:
        for i, l in enumerate(r['labels']):
            if l == 'identity': idu.add(r['holder_unit'][i])
            if l == '': tgt[(r['holder_unit'][i], r['holder_sp'][i])] += 1
    for r in rowsA:
        for g, sn in r['snaps'].items():
            for i, l in enumerate(sn['labels']):
                if l == 'identity': idu.add(sn['holder_unit'][i])
    idu = np.array(sorted(idu))
    out = dict(identity_units=len(idu))
    # target units exploited by some identity holder
    ex_by = (A[np.ix_(np.nonzero(T)[0], idu)] == 1) & (A[np.ix_(idu, np.nonzero(T)[0])].T == 0)
    out['target_units_exploitable_by_identity'] = int(ex_by.any(1).sum())
    out['target_units'] = int(T.sum())
    # fresh founders against the most common target holders
    res = []
    for (u, s), n in tgt.most_common(4):
        mass = 0.0; tops = []
        tree = {}
        for sp in range(len(mu)):
            t = int(LS['tau'][sp])
            key = t if sp != s else -1
            if key not in tree:
                tree[key] = RR.phenotype(int(S['spE'][sp]), sp, u, s, LS)
            p = tree[key]
            if not T[p]: continue
            if ((A[p, idu] == 1) & (A[idu, p] == 0)).any():
                mass += mu[sp]; tops.append((names[sp], float(mu[sp])))
        tops.sort(key=lambda z: -z[1])
        res.append(dict(holder=names[s], unit=u, islands=n, shadow_mass=mass, top=tops[:4]))
    out['by_holder'] = res
    json.dump(out, open(os.path.join(RR.ROOT, 'runs', 'removing-rivals-shadow.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
