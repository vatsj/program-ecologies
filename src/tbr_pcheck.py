"""Queue 81: arm P's lump-free stage-1 runs against the published cells (bridgeless_rivals rows), statistically.
Writes runs/tbr/extra.md (a table included in the run record).

Compared per forced rival and for the natural cell: mean island P(C,C) at the horizon, the share of runs separated at
the horizon (two certified-looking holders, i.e. settled islands at >= 0.95, whose classes mutually defect) against
the published 'horizon separated' (sep_end_tag for forced rivals, n_sep_end > 0 for natural runs), and status.
"""
import glob, gzip, json, os, sys
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    import tbr_p as TP
    import bridgeless_rivals as BR
    d = TP._d(); V = np.asarray(d['V']).astype(bool)
    pub = {}
    for exp in ('dense', 'nat'):
        for r in BR.load(exp):
            pub.setdefault((exp, r['rival']), []).append(r)
    mine = {}
    for f in glob.glob(os.path.join(ROOT, 'runs', 'tbr_rows', 'p', '*_1.091_*.json.gz')):
        r = json.load(gzip.open(f, 'rt'))
        mine.setdefault((r['exp'], r['rival']), []).append(r)
    L = ['### Arm P: lump-free runs (this record) against the published cells (`bridgeless_rivals`)\n',
         '| cell | runs (here / published) | island P(C,C) here / published | separated at horizon here / published | status here |',
         '|---|---|---|---|---|']
    for key in sorted(mine, key=lambda k: (k[0], k[1] or '')):
        rs = mine[key]; ps = pub.get(key, [])
        sep = 0
        for r in rs:
            hc = sorted({c['p'] for c in r['snaps']['100']['cases'] if c['set095']})
            if any((not V[a, b]) and (not V[b, a]) for i, a in enumerate(hc) for b in hc[i + 1:]):
                sep += 1
        if key[1] is None:
            psep = np.mean([x['n_sep_end'] > 0 for x in ps]) if ps else None
        else:
            psep = np.mean([bool(x.get('sep_end_tag')) for x in ps]) if ps else None
        L.append('| %s %s | %d / %d | %.3f / %.3f | %.2f / %s | %s |' % (
            key[0], key[1] or 'natural', len(rs), len(ps), np.mean([r['pcc'] for r in rs]),
            np.mean([x['pcc'] for x in ps]) if ps else float('nan'), sep / len(rs),
            '%.2f' % psep if psep is not None else '–', dict(Counter(r['status'] for r in rs))))
    L.append('\nStatus codes: 1 frozen, 3 horizon-certified, 4 unresolved (rival_islands.STATUS). "Separated here" uses '
             'settled holders (>= 0.95) whose classes mutually defect; the published statistic uses certified holders '
             'and network tags, so the two agree only approximately.\n')
    open(os.path.join(ROOT, 'runs', 'tbr', 'extra.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
