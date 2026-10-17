"""Post-hoc diagnostic (annealed mutation, run report): identity predators of target holders.  For a target holder
(unit t, spelling st), the identity-predator mass is the prior mass of TwinD-family spellings (provenance's Q) whose
fresh phenotype against t exploits it (A[t, p] = 1, A[p, t] = 0) and is an identity unit; such an arrival is
*selected* under the drift classifier.  Reported for the holders of target islands at generations 2,000 and at the end
of the natural cells, with the expected selected identity arrivals per island over the schedule (A * mass)."""
import glob
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
import provenance_run as PR
import removing_rivals as RR
import annealed as AN


def main():
    LS = PR.lot_static(); S = RR.static(LS)
    A, ident = S['A'], S['ident']
    Q = [int(q) for q in LS['Q']]
    mu = LS['mu']
    cache = {}

    def prey_mass(t, st):
        if (t, st) in cache: return cache[(t, st)]
        m = 0.0; tops = []
        for q in Q:
            p = RR.phen_cached(q, t, st, LS)
            if A[t, p] == 1 and A[p, t] == 0 and ident[p]:
                m += mu[q]; tops.append(LS['names'][q])
        cache[(t, st)] = (m, tops[:3])
        return cache[(t, st)]

    import annealed_report as AREP
    rows = AREP.load_rows()
    out = defaultdict(lambda: dict(islands=0, prey=0, mass=0.0))
    holders = defaultdict(int)
    for r in rows:
        if r['arm'] == 'F': continue
        for g in ('2000', str(r['gens'])):
            s = r['snaps'].get(g)
            if not s: continue
            for lab, u, sp in zip(s['labels'], s['holder_unit'], s['holder_sp']):
                if lab != '': continue
                m, tops = prey_mass(int(u), int(sp))
                k = '%s|%d|%s' % (r['arm'] + ('' if r['K'] in (0, 3) else '_K1'), r['N'], 'end' if g != '2000' else '2000')
                out[k]['islands'] += 1; out[k]['prey'] += int(m > 0); out[k]['mass'] += m
                if m > 0: holders[(LS['names'][int(sp)], int(u), round(m, 5), tuple(tops))] += 1
    res = {k: dict(v, prey_frac=v['prey'] / v['islands'] if v['islands'] else None,
                   mean_mass=v['mass'] / v['islands'] if v['islands'] else None,
                   expected_selected_identity_arrivals_per_island=AN.arrivals_A(3) * v['mass'] / v['islands']
                   if v['islands'] else None)
           for k, v in sorted(out.items())}
    top = sorted(holders.items(), key=lambda kv: -kv[1])[:10]
    json.dump(dict(cells=res, top_prey_holders=[dict(holder=h[0], unit=h[1], mass=h[2], top=list(h[3]), islands=n)
                                                for h, n in top]),
              open(os.path.join(AN.ROOT, 'runs', 'annealed-idprey.json'), 'w'), indent=1)
    for k, v in res.items(): print(k, v)
    for t in top: print(t)


if __name__ == '__main__':
    main()
