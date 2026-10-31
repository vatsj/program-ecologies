"""Aggregates the rows of the unequal-basin experiment into runs/unequal-basin.md and .json (spec "Required outputs").

    python3 src/unequal_basin_report.py
Reads runs/unequal_basin/rows/*.json (rows and scans), validate-*.json, prep-*.json, endpoint-*.json."""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import unequal_basin_core as UC

OUTD = UC.OUTD
ROWS = os.path.join(OUTD, 'rows')
ROOT = UC.ROOT
CPS = (0, 100, 1000, 10000, 100000)


def rows():
    out = []
    for f in sorted(glob.glob(os.path.join(ROWS, '*.json'))):
        if os.path.basename(f).startswith('scan_'):
            continue
        r = json.load(open(f))
        if 'spec' in r:
            out.append(r)
    return out


def scans():
    out = []
    for f in sorted(glob.glob(os.path.join(ROWS, 'scan_*.json'))):
        out.append(json.load(open(f)))
    return out


def at(r, t):
    best = None
    for x in r.get('records', []):
        if abs(x['t'] - t) <= 1e-9 * max(1.0, t):
            best = x
    return best['shares'] if best else None


def fmt(v):
    return '%.4f' % v if abs(v) >= 5e-5 or v == 0 else '%.1e' % v


def trajectory_line(r):
    cells = []
    for t in CPS:
        sh = at(r, t)
        cells.append('-' if sh is None else '%s/%s/%s/%s' % (fmt(sh[0]), fmt(sh[1]), fmt(sh[2]), fmt(sh[3] + sh[4])))
    fin = r['records'][-1]['shares']
    cells.append('%s/%s/%s/%s' % (fmt(fin[0]), fmt(fin[1]), fmt(fin[2]), fmt(fin[3] + fin[4])))
    return cells


def core_label(sp):
    return sp.get('core') or '-'


def main_tables():
    R = rows()
    lines = []
    sel = [r for r in R if not r['spec'].get('abl') and not r['spec'].get('pools') and not r['spec'].get('raw') and not str(r['spec']['start']).startswith('mix')
           and not str(r['spec']['start']).startswith('u:') or (r['spec']['start'] == 'u:0.6' and not r['spec'].get('abl') and not r['spec'].get('pools'))]
    lines.append('| cell | m | core | start | status | endpoint | t_end | states | 0 | 10^2 | 10^3 | 10^4 | 10^5 | limit |')
    lines.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for r in sorted(sel, key=lambda r: (r['spec']['cell'], r['spec']['m'], str(r['spec'].get('core')), r['spec']['start'])):
        sp = r['spec']
        if 'records' not in r:
            continue
        lines.append('| %s | %d | %s | %s | %s | %s | %.2g | %d | %s |' % (sp['cell'], sp['m'], core_label(sp), sp['start'], r['status'], r['endpoint'],
                                                                         r['t_end'], r['states'], ' | '.join(trajectory_line(r))))
    return '\n'.join(lines)


def scan_table():
    lines = ['| cell | m | core | ablation | u* | range | endpoint class by scanned u (status e = early) |', '|---|---|---|---|---|---|---|']
    for d in scans():
        j, res = d['job'], d['result']
        tab = res['table']
        cls = ', '.join('%s:%s%s' % (u, v[1], 'e' if v[0] == 'early' else '') for u, v in sorted(tab.items(), key=lambda kv: float(kv[0])))
        lines.append('| %s | %s | %s | %s | %s | %s | %s |' % (j['cell'], j.get('m'), j.get('core'), j.get('abl') or 'full',
                                                              res['ustar'] if res['ustar'] is not None else 'none', res['range'], cls))
    return '\n'.join(lines)


def validations():
    out = {}
    for f in sorted(glob.glob(os.path.join(OUTD, 'validate-*.json'))):
        out[os.path.basename(f)[9:-5]] = json.load(open(f))
    return out


def write():
    md = ['# Where the unequal basin comes from (queue 70): run report', '', 'See notes/unequal-basin.md and specs/2026-10-31-unequal-basin.md.',
          '', '## Trajectories (V*/U/G/W+D)', '', main_tables(), '', '## u* and the tilt scans', '', scan_table(), '']
    open(os.path.join(ROOT, 'runs', 'unequal-basin.md'), 'w').write('\n'.join(md))
    js = dict(rows=[{k: v for k, v in r.items() if k not in ('records',)} for r in rows()], scans=scans(), validations=validations())
    json.dump(js, open(os.path.join(ROOT, 'runs', 'unequal-basin.json'), 'w'), default=str)


if __name__ == '__main__':
    write()
