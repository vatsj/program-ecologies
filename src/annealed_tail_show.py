"""Quick table of the tail rows: python3 src/annealed_tail_show.py [filter substring of the job json]"""
import os, sys, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = os.path.join(os.path.dirname(HERE), 'runs', 'annealed_tail', 'rows')


def rows():
    out = []
    for f in glob.glob(os.path.join(ROWS, '*.json')):
        try:
            r = json.load(open(f))
        except Exception:
            continue
        out.append(r)
    return out


if __name__ == '__main__':
    flt = sys.argv[1] if len(sys.argv) > 1 else ''
    L = []
    for r in rows():
        s = r['spec']
        if s['kind'] in ('bisect', 'attr', 'late0') or 'sched' not in s:
            continue
        if flt and flt not in json.dumps(s, sort_keys=True):
            continue
        sc = s['sched']
        key = (s['kind'], s['cell'], s['start'], s.get('tail', 'full'), s.get('N', 100), s.get('obj', 'P'), sc['kind'], sc.get('t0', sc.get('T')), sc['Lam'])
        L.append((key, r))
    L.sort(key=lambda z: tuple(str(v) for v in z[0][:8]) + (z[0][8],))
    for key, r in L:
        sh = r.get('shares') or [float('nan')] * 5
        print(' '.join(str(v) for v in key), r.get('class'), r.get('protocol'), 'V*=%.4f U=%.4f WD=%.4f' % (sh[0], sh[1], sh[3] + sh[4]),
              'tau=%.3g' % r.get('tau_end', 0), 'wall=%d' % r.get('wall', 0))
