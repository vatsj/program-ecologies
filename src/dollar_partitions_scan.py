"""Addendum scan for specs/2026-10-05-dollar-partitions.md: where between N = 10^2 and 10^3 the fixed-role chain moves
from the middle splits to the endpoints, and where the one-population chains move from S3 to the greedy polymorphism.

    python3 src/dollar_partitions_scan.py fixed|onepop
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import dollar_partitions as P

if __name__ == '__main__':
    which = sys.argv[1]
    out = {}
    if which == 'fixed':
        for game in ('dollar5', 'dollar3'):
            d = P.data(game, 5, 'fixed')
            for N in (150, 200, 300, 500, 700):
                r = P.fixed_summary(d, P.fixed_chain(d, N))
                out['%s_N%d' % (game, N)] = dict(outcome=r['outcome'], ordered_label_mass=r['ordered_label_mass'])
                o = r['outcome']
                print(game, N, ', '.join('%s %.4f' % (k, o[k]) for k in sorted(o) if k.startswith('o:')), 'Emax %.3f' % o['E_max_pay'], flush=True)
    else:
        for game, arm, Ns in (('dollar5', 'norole', (5000, 7000)), ('dollar5', 'role', (20000, 100000)), ('dollar3', 'role', (30000,)), ('dollar3', 'norole', (3000, 5000))):
            d = P.data(game, 5, arm)
            for N in Ns:
                ch, prov = P.onepop_chain(d, N)
                r = P.onepop_summary(d, ch)
                out['%s_%s_N%d' % (game, arm, N)] = dict(outcome=r['outcome'], support=r['support'][:6], mass_polymorphic=r['mass_polymorphic'])
                o = r['outcome']
                print(game, arm, N, ', '.join('%s %.4f' % (k, o[k]) for k in sorted(o) if '-' in k or k in ('ineff', 'clash')), 'eff %.4f' % o['eff'],
                      '| top:', '; '.join('%s %.3f' % (s['state'], s['pi']) for s in r['support'][:3]), flush=True)
    json.dump(out, open(os.path.join(P.OUT, 'scan_%s.json' % which), 'w'), indent=1, default=str)
