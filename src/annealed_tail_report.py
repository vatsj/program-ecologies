"""Report of the annealed-tail experiment: tables from the rows in runs/annealed_tail/rows -> runs/annealed-tail.md and .json.

    python3 src/annealed_tail_report.py
"""
import os, sys, json, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RD = os.path.join(ROOT, 'runs', 'annealed_tail')
ROWS = os.path.join(RD, 'rows')
CLS = ['F', 'U', 'G', 'W', 'D']


def load_rows():
    out = []
    for f in glob.glob(os.path.join(ROWS, '*.json')):
        try:
            out.append(json.load(open(f)))
        except Exception:
            pass
    return out


def skey(r):
    s = r['spec']
    sc = s.get('sched', {})
    return dict(kind=s['kind'], cell=s['cell'], start=s.get('start'), tail=s.get('tail', 'full'), renorm=bool(s.get('renorm', False)),
                N=s.get('N', 100), obj=s.get('obj', 'P'), sk=sc.get('kind'), t0=sc.get('t0', sc.get('T')), Lam=sc.get('Lam'),
                rtol=s.get('rtol'), spd=s.get('spd'))


def pick(rows, **flt):
    out = {}
    for r in rows:
        if r['spec']['kind'] in ('bisect', 'attr', 'asym'):
            continue
        k = skey(r)
        if all(k.get(a) == b for a, b in flt.items()):
            if r.get('shares') is None:
                continue
            out[k['Lam']] = r
    return out


def fmt(r):
    sh = r['shares']
    return '%.4f / %.4f / %.4f' % (sh[0], sh[1], sh[3] + sh[4])


def tag(r):
    p = r.get('protocol')
    c = r.get('class')
    return c + ('*' if p not in ('direct',) else '')


def lam_star(ser, mode='rescue'):
    """first Lam (ascending) whose endpoint crosses V* = 0.5; None if none."""
    for l in sorted(ser):
        v = ser[l]['shares'][0]
        if (mode == 'rescue' and v >= 0.5) or (mode == 'harm' and v < 0.5):
            return l
    return None


def vstar_monotone(ser, tol=0.01):
    ls = sorted(ser)
    bad = []
    for a, b in zip(ls[:-1], ls[1:]):
        if ser[b]['shares'][0] < ser[a]['shares'][0] - tol:
            bad.append((a, b, ser[a]['shares'][0], ser[b]['shares'][0]))
    return bad


def main():
    rows = load_rows()
    out = dict(n_rows=len(rows))
    md = []
    LAMS = [0.0, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1e3, 1e4, 1e5]

    def table(title, series_list):
        md.append('### ' + title)
        md.append('')
        md.append('| series | ' + ' | '.join(('%g' % l) for l in LAMS) + ' |')
        md.append('|---|' + '---|' * len(LAMS))
        for name, ser in series_list:
            cells = []
            for l in LAMS:
                if l in ser:
                    cells.append('%.4f %s' % (ser[l]['shares'][0], tag(ser[l])))
                else:
                    cells.append('-')
            md.append('| %s | %s |' % (name, ' | '.join(cells)))
        md.append('')

    # main DSL tables: V* by Lam; Lam = 0 from the V1 row
    for cell, start in (('M0', 'nat'), ('L0', 'nat'), ('M0', 'u:0.6'), ('L0', 'u:0.6')):
        base = pick(rows, kind='dsl', cell=cell, start=start, sk='anneal', Lam=0.0, tail='full', N=100, obj='P')
        sl = []
        for t0 in (1.0, 100.0, 1e4):
            ser = pick(rows, kind='dsl', cell=cell, start=start, sk='anneal', t0=t0, tail='full', N=100, obj='P', rtol=None, spd=None)
            if 0.0 in base:
                ser[0.0] = list(base.values())[0]
            sl.append(('t0=%g' % t0, ser))
        table('%s %s: endpoint V* (class; * = censored or tail-pending protocol)' % (cell, start), sl)
    md_main = md
    return rows, out, md


if __name__ == '__main__':
    rows, out, md = main()
    print('\n'.join(md))
