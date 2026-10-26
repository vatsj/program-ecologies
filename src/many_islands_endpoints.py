"""Where do finite pools end?  For every finished pool / archipelago run, the class of the consolidated state at 100,000 events per
island (or the last checkpoint): fair-pair endpoint (V* >= 0.9), unequal-pair endpoint (U >= 0.9), or mixed.  Writes
runs/many_islands/endpoints.json and prints a table.   python3 src/many_islands_endpoints.py"""
import os, sys, json, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import many_islands as MI
import many_islands_run as MR

V = list(MI.V)


def classify(h):
    s = np.asarray(h, float); s = s / s.sum()
    v = float(s[V].sum()); u = float(s[MI.CATMAP == 1].sum())
    p = s[V] / max(v, 1e-12)
    if v >= 0.9:
        return 'F-%d' % int(p.argmax()) if p.max() >= 0.6 else 'F-mixed'
    if u >= 0.9:
        return 'U'
    return 'mixed'


def run():
    out = {}
    for arm in ('L', 'M', 'R'):
        for A in (0, 150):
            rows = {}
            for k in range(3):
                f = os.path.join(MR.OUT, 'chain_%s_A%d_p%d.json' % (arm, A, k))
                if os.path.exists(f):
                    c = json.load(open(f))
                    cp = 100000 if 100000 in c['cps'] else c['cps'][-1]
                    rows.setdefault('pool 16384', []).append(classify(c['hist'][c['cps'].index(cp)]))
            f = os.path.join(MR.OUT, 'union_%s_A%d.json' % (arm, A))
            if os.path.exists(f):
                u = json.load(open(f))
                for lab, v in u.items():
                    cp = 100000 if 100000 in v['cps'] else v['cps'][-1]
                    rows.setdefault('pool %d' % v['I'], []).append(classify(v['hist'][v['cps'].index(cp)]))
            f = os.path.join(MR.OUT, 'rs_%s_A%d_rs.json' % (arm, A))
            if os.path.exists(f):
                r = json.load(open(f))
                cp = 30000 if 30000 in r['cps'] else r['cps'][-1]
                rows.setdefault('resampled 262144 (30000)', []).append(classify(r['hist'][r['cps'].index(cp)]))
            f = os.path.join(MR.OUT, 'ia_%s_A%d.json' % (arm, A))
            if os.path.exists(f):
                for rr in json.load(open(f)):
                    cps = rr['cps']
                    cp = 100000 if 100000 in cps else cps[-1]
                    rows.setdefault('archipelago I=%d (%d)' % (rr['I'], cp), []).append(classify(rr['hist'][cps.index(cp)]))
            f = os.path.join(MR.OUT, 'comp_%s_A%d.json' % (arm, A))
            if os.path.exists(f):
                for rr in json.load(open(f)):
                    cps = rr['cps']
                    cp = 100000 if 100000 in cps else cps[-1]
                    rows.setdefault('1024 islands in C=%d components (%d)' % (rr['C'], cp), []).append(classify(rr['hist'][cps.index(cp)]))
            out['%s A=%d' % (arm, A)] = {k: dict(n=len(v), F=sum(1 for x in v if x.startswith('F')), U=sum(1 for x in v if x == 'U'),
                                                 mixed=sum(1 for x in v if x == 'mixed'), detail=v if len(v) <= 6 else None) for k, v in rows.items()}
    with open(os.path.join(MR.OUT, 'endpoints.json'), 'w') as f:
        json.dump(out, f)
    for cell, rows in out.items():
        print(cell)
        for k, v in rows.items():
            print('   %-48s n=%2d  F %2d  U %2d  mixed %2d  %s' % (k, v['n'], v['F'], v['U'], v['mixed'], v['detail'] or ''))


if __name__ == '__main__':
    run()
