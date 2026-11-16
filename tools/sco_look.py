#!/usr/bin/env python3
"""Queue 80: quick look at the step-2 rows fetched so far (V* rows, delta*, delta-mean per arm and cell).

    python3 tools/sco_look.py [ARM ...]
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import script_offers_report as R

if __name__ == '__main__':
    arms = sys.argv[1:] or ['UF', 'UFR', 'K', 'K2', 'A1', 'A2', 'A3', 'A4', 'A5']
    rows = R.load('runs/sco_rows/*/rows_*.jsonl')
    rows = {k: v for k, v in rows.items() if v['series'] not in ('pilot', 'v1')}
    agg = R.aggregate(rows)
    print(len(rows), 'rows')
    for arm in arms:
        for N in (100, 200, 400):
            for b in (0.0, 1.0, 3.0):
                for ph in (0.0, 0.5, 1.0):
                    r = R.row(agg, arm, b, ph, N)
                    if all(v is None for v in r.values()):
                        continue
                    e = [agg.get((arm, b, ph, N, d, None)) for d in R.DELTAS]
                    bc = [x['bc_pair_share'] if x else None for x in e]
                    print('%-4s N%-3d b%g ph%-3g V* %s  d* %s  mean %s  BcPair %s' % (
                        arm, N, b, ph, ' '.join('%.2f' % v if v is not None else ' -- ' for v in r.values()), R.dstar(r), R.dmean(r),
                        ' '.join('%.2f' % v if v is not None else '--' for v in bc)))
