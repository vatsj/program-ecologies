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


def _fmt_row(r):
    sp = r['spec']
    return '| %s | %d | %s | %s | %s | %s | %.2g | %d | %s |' % (sp['cell'], sp['m'], core_label(sp), sp['start'], r['status'], r['endpoint'], r['t_end'], r['states'],
                                                                 ' | '.join(trajectory_line(r)))


HEAD = ['| cell | m | core | start | status | endpoint | t_end | states | 0 | 10^2 | 10^3 | 10^4 | 10^5 | limit |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']


def main_tables():
    R = rows()
    base = [r for r in R if not r['spec'].get('abl') and not r['spec'].get('pools') and not r['spec'].get('raw') and 'records' in r
            and r['spec']['start'] in ('nat', 'fair', 'wd', 'u:0.6') and r['spec'].get('core') in (None, 'pilot_L')]
    lines = list(HEAD)
    for r in sorted(base, key=lambda r: (r['spec']['cell'], r['spec']['m'], str(r['spec'].get('core')), r['spec']['start'])):
        lines.append(_fmt_row(r))
    return '\n'.join(lines)


def other_tables():
    R = rows()
    out = []
    pert = [r for r in R if 'records' in r and (str(r['spec']['start']).startswith(('pert', 'asym', 'mix')))]
    out.append('### Perturbations and self-consistency (start from the saved unequal endpoint)\n')
    out.extend(HEAD)
    for r in sorted(pert, key=lambda r: (r['spec']['cell'], r['spec']['start'])):
        out.append(_fmt_row(r))
    raw = [r for r in R if 'records' in r and (r['spec'].get('raw') or r['spec'].get('pools'))]
    out.append('\n### One pool (support sensitivity) and the raw unsymmetrized pool law (unprojected field)\n')
    out.extend(HEAD)
    for r in sorted(raw, key=lambda r: (r['spec']['cell'], bool(r['spec'].get('raw')), r['spec']['start'])):
        if str(r['spec']['start']) in ('nat', 'u:0.6'):
            out.append(_fmt_row(r) + (' raw' if r['spec'].get('raw') else ' pool 0'))
    return '\n'.join(out)


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


def ladder_table():
    ex = json.load(open(os.path.join(OUTD, 'extras.json')))
    lines = ['| cell | pools | start | m | core | states | endpoint | V*/U/G/W/D at the end | t_end |', '|---|---|---|---|---|---|---|---|---|']
    for r in ex['ladder']:
        lines.append('| %s | %s | %s | %d | %s | %d | %s | %s | %.2g |' % (r['cell'], r['pools'], r['start'], r['m'], r['core'], r['states'], r['endpoint'],
                                                                            '/'.join(fmt(v) for v in r['final']), r['t_end']))
    return '\n'.join(lines)


def validation_table():
    v = validations()
    lines = ['| validation | result |', '|---|---|']
    for k, d in v.items():
        if k.startswith('v3'):
            lines.append('| %s | gate (ODE vs matched MC, replicate band or 0.01): %s; max |ODE - MC(m)| %.4f; max |ODE - MC(full)| %s |' % (
                k, d['gate_implementation'], max(r['diff_ode_mc_m'] for r in d['rows']), ('%.4f' % d['max_diff_ode_full']) if 'mc_full' in d else 'n/a'))
        elif k.startswith('v4'):
            lines.append('| %s | %d strata, |z| max %.2f, passed (>=6 strata or 5 where the sixth does not exist): %s |' % (
                k, len(d['strata']), max(abs(s['z']) for s in d['strata']), d['passed']))
        elif k == 'v1':
            lines.append('| v1 | L: %s, M: %s (table, kernel 1e-12, ODE 1e-6 against arm T dose 0 at 1e2, 1e3, 1e4; max ODE diff L %.1e) |' % (
                d['L']['passed'], d['M']['passed'], max(x['maxdiff'] for x in d['L']['ode'])))
        elif k == 'v2':
            lines.append('| v2 | %s |' % '; '.join('%s: %s -> %s classes, field diff %.1e' % (kk, vv['programs'][0], vv['classes'][0], vv['max_abs_diff']) for kk, vv in d.items()))
        elif k == 'v5':
            lines.append('| v5 | L: %d of %d triples with a divergent slot (all-conditional triples 1296^3 are divergent in every slot); M: %d non-convergent, %d divergent |' % (
                d['L']['triples'] - d['L']['mask_counts'][0], d['L']['triples'], d['M']['nonconvergent'], sum(d['M']['mask_counts'][1:])))
        elif k == 'v6':
            lines.append('| v6 | %s |' % '; '.join('%s: %d states, %d level violations, field asymmetry %.1e' % (kk, vv['states'], vv['level_violations'], vv['field_asymmetry']) for kk, vv in d.items()))
    return '\n'.join(lines)


def endpoint_summary():
    lines = []
    for f in sorted(glob.glob(os.path.join(OUTD, 'endpoint-*.json'))):
        d = json.load(open(f))
        sp = d['spec']
        lines.append('### %s (%s m=%s %s abl=%s core=%s) shares %s' % (d['key'], sp['cell'], sp['m'], sp['start'], sp.get('abl'), sp.get('core'),
                                                                     [round(v, 4) for v in d['shares']]))
        lines.append('')
        lines.append('| program (slot-0 frame) | conditional | mass | high | low | excluded | in F | other |')
        lines.append('|---|---|---|---|---|---|---|---|')
        for z in d['top_classes_slot0']:
            lines.append('| %s | %s | %.4f | %.4f | %.4f | %.4f | %.4f | %.4f |' % (z['src'], z['conditional'], z['mass'], z['high'], z['low'], z['excl'], z['in_F'], z['other']))
        lines.append('')
        lines.append('class flux per event per island (rows from, columns to; F U G W D): ' + json.dumps([[float('%.3g' % v) for v in row] for row in d['class_flux']]))
        lines.append('')
        lines.append('blocked (truncation) flux fraction %.2e; leak into absent states %.2e; support states %s' % (d['blocked_flux']['fraction'],
                                                                                                                  d['leak']['into_absent'], d['support_states']))
        j = d['jacobian']
        for mode in ('invariant', 'transverse', 'full'):
            x = j[mode]
            lines.append('- Jacobian %s (dim %d): neutral %s, positive %s, negative %s; class-changing leading: %s; leading overall: %s' % (
                mode, x['dim'], x.get('n_neutral_abs_1e-9'), x.get('n_positive_re_gt_1e-9'), x.get('n_negative_re_lt_-1e-9'),
                [(float('%.3g' % c['re']), float('%.2g' % c['proj'])) for c in x.get('class_changing', [])[:4]],
                [float('%.3g' % c['re']) for c in x['leading'][:3]]))
        lines.append('- full-space leading real parts: %s' % (j.get('full_space_leading_re'),))
        for e in d['rescue'][:1]:
            lines.append('- dominant unequal state %s (roles %s, actions %s, payoffs %s): %d moves to a fair pair, flux %.3g of total outflow %.3g' % (
                e['state'], e['roles'], e['actions'], e['payoffs'], e['n_moves_to_fair'], e['flux_to_fair'], e['flux_total_out']))
        lines.append('')
    return '\n'.join(lines)


def random_table():
    ex = json.load(open(os.path.join(OUTD, 'extras.json')))
    lines = ['| cell | removal | endpoint at u = 0.6 | V*/U/G/W/D |', '|---|---|---|---|']
    for r in ex['random_knockouts']:
        lines.append('| %s | %s | %s | %s |' % (r['cell'], r['abl'], r['endpoint'], '/'.join(fmt(v) for v in r['final'])))
    return '\n'.join(lines)


def armt_table():
    f = os.path.join(OUTD, 'armT_dose0_tilt_scan.json')
    if not os.path.exists(f):
        return ''
    d = json.load(open(f))
    lines = ['| unequal tilt u | status | V*/U/G/W/D at the end |', '|---|---|---|']
    for u, r in d.items():
        lines.append('| %s | %s | %s |' % (u, r['status'], '/'.join(fmt(v) for v in r['shares'])))
    return '\n'.join(lines)


def write():
    md = ['# Where the unequal basin comes from (queue 70): run report', '',
          'Spec specs/2026-10-31-unequal-basin.md, notes notes/unequal-basin.md (section 2 lists every deviation; the object computed is a',
          'reflecting m-conditional truncation of the dense ODE, see notes 2.1), predictions predictions/2026-10-31-unequal-basin.md.', '',
          '## Validations', '', validation_table(), '',
          '## Trajectories (V*/U/G/W+D) per cell and start', '', main_tables(), '',
          '## u* and the tilt scans (class at each scanned u; e = early classification)', '', scan_table(), '',
          other_tables(), '',
          '## Ladder in the truncation (natural and u = 0.6 starts)', '', ladder_table(), '',
          '## Matched-abundance random knockouts', '', random_table(), '',
          '## Arm T dose 0 (constants only, arm T code) under the unequal tilt scan', '', armt_table(), '',
          '## Endpoints: classes by role, flux, blocked flux, Jacobian', '', endpoint_summary(), '']
    open(os.path.join(ROOT, 'runs', 'unequal-basin.md'), 'w').write('\n'.join(md))
    ex = json.load(open(os.path.join(OUTD, 'extras.json')))
    js = dict(rows=[{k: v for k, v in r.items() if k not in ('records',)} for r in rows()], scans=scans(), validations=validations(), extras=ex)
    json.dump(js, open(os.path.join(ROOT, 'runs', 'unequal-basin.json'), 'w'), default=str)


if __name__ == '__main__':
    write()
