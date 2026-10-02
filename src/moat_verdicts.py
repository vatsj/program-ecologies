"""Score runs/drift_closure.json against predictions/2026-10-02-drift-closure.md.  Prints a compact table per arm
and the verdict checks; writes nothing.

    python3 src/moat_verdicts.py
"""
import json, os, math
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'runs', 'drift_closure.json')))
rows = D['rows']


def key(r):
    return (r['arm'], r['n'], 0.0 if r['arm'] == 'Dpath' else r['delta'])


G = defaultdict(dict)
TH = {}
for r in rows:
    if r.get('theta', 1e-6) != 1e-6:
        TH[(r['arm'], r['n'], r['delta'], r['N'])] = r
    else:
        G[key(r)][r['N']] = r


def fam(r):
    c = r['FBfam'] + r['prudent'] + r['rival']
    return (r['FBfam'] / c, r['prudent'] / c, r['rival'] / c) if c > 0 else (0, 0, 0)


def odds(r):
    return r['pcc'] / max(1 - r['pcc'], 1e-300)


def sl(a, b, f):
    return math.log(f(b) / f(a)) / math.log(b['N'] / a['N'])


for k in sorted(G):
    rs = [G[k][N] for N in sorted(G[k])]
    print('%-10s n=%d δ=%-6g' % k)
    for i, r in enumerate(rs):
        f = fam(r)
        ex = '' if i == 0 else 'odds sl %.2f, exit sl %.2f' % (sl(rs[i - 1], r, odds), sl(rs[i - 1], r, lambda x: x['net_exit']))
        print('   N=%-7d P %.5f 1-P %.2e exit %.2e FB/pr/riv %.3f/%.3f/%.3f X %.3f term %d nc %d kept %.3f poly %.1e cut %.1e ind %d abs %.0e | %s | top %s' % (
            r['N'], r['pcc'], 1 - r['pcc'], r['net_exit'], f[0], f[1], f[2], r['universality'], r['n_terminal'], r['near_closed'],
            r['kept_exit_share'], r['poly_flow'], r['cut_flow'], r['indeterminate'], r['absorb_error'], ex, r['top_coop']))
print('theta repeats:')
for k, r in TH.items():
    b = G[(k[0], k[1], k[2])][k[3]]
    print('  ', k, '1-P %.3e vs %.3e; fam %s vs %s' % (1 - r['pcc'], 1 - b['pcc'], ['%.3f' % x for x in fam(r)], ['%.3f' % x for x in fam(b)]))
