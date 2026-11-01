"""Report of the annealed-tail experiment: tables from the rows in runs/annealed_tail/rows -> runs/annealed-tail.md and .json.

    python3 src/annealed_tail_report.py
"""
import os, sys, json, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RD = os.path.join(ROOT, 'runs', 'annealed_tail')
ROWS = os.path.join(RD, 'rows')
VAL = os.path.join(RD, 'validation')
CLS = ['F', 'U', 'G', 'W', 'D']
LAMS = [0.0, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1e3, 1e4, 1e5]


def load_rows():
    out = []
    for f in sorted(glob.glob(os.path.join(ROWS, '*.json'))):
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
                rtol=s.get('rtol'), spd=s.get('spd'), keep_x=s.get('keep_x'))


def pick(rows, kinds=('dsl', 'armT', 'late0'), **flt):
    out = {}
    for r in rows:
        if r['spec']['kind'] not in kinds:
            continue
        k = skey(r)
        if all(k.get(a) == b for a, b in flt.items()):
            if r.get('shares') is None:
                continue
            out[k['Lam']] = r
    return out


def tag(r):
    p = r.get('protocol')
    c = r.get('class')
    return c + ('' if p == 'direct' else ('*' if p in ('burst', 'censored') else '?'))


def lam_star(ser, mode='rescue'):
    for l in sorted(ser):
        v = ser[l]['shares'][0]
        if (mode == 'rescue' and v >= 0.5) or (mode == 'harm' and v < 0.5):
            return l
    return None


def decreases(ser, tol=0.01):
    ls = sorted(ser)
    return [(a, b, ser[a]['shares'][0], ser[b]['shares'][0]) for a, b in zip(ls[:-1], ls[1:]) if ser[b]['shares'][0] < ser[a]['shares'][0] - tol]


def jl(name):
    p = os.path.join(VAL, name + '.json')
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    rows = load_rows()
    out = dict(n_rows=len(rows))
    md = []

    def H(t, lvl=2):
        md.append('#' * lvl + ' ' + t)
        md.append('')

    def table(title, series_list, lams=None):
        lams = lams or LAMS
        md.append('**%s**' % title)
        md.append('')
        md.append('| series | ' + ' | '.join(('%g' % l) for l in lams) + ' |')
        md.append('|---|' + '---|' * len(lams))
        for name, ser in series_list:
            cells = []
            for l in lams:
                cells.append(('%.4f %s' % (ser[l]['shares'][0], tag(ser[l]))) if l in ser else '-')
            md.append('| %s | %s |' % (name, ' | '.join(cells)))
        md.append('')

    # ------------------------------------------------------------------ main grid
    H('Main grid: endpoint V* by (arm, start, t0, Lam)')
    md.append('Cells are V* (the F share) and the class of the endpoint (F = V*-dominated, U = unequal-dominated); a star marks the burst or censored')
    md.append('protocol (the tail was still delivering more than 1e-4 arrivals per island when criterion (a) held, or the cap bound), "-" = not run.')
    md.append('Lam = 0 is the tail-free object (V1).')
    md.append('')
    series = {}
    for cell, start in (('M0', 'nat'), ('L0', 'nat'), ('M0', 'u:0.6'), ('L0', 'u:0.6')):
        sl = []
        for t0 in (1.0, 100.0, 1e4):
            ser = pick(rows, kinds=('dsl',), cell=cell, start=start, sk='anneal', t0=t0, tail='full', N=100, obj='P', rtol=None, spd=None, keep_x=None)
            base = pick(rows, kinds=('dsl', 'late0'), cell=cell, start=start if start != 'nat' or cell != 'M0' else 'nat', Lam=0.0, tail='full', N=100, obj='P',
                        rtol=None, spd=None, keep_x=None)
            if 0.0 in base:
                ser[0.0] = base[0.0]
            elif cell == 'L0' and start == 'nat':
                b2 = pick(rows, kinds=('dsl',), cell=cell, start=start, Lam=0.0, N=100, obj='P', keep_x=True)
                if 0.0 in b2:
                    ser[0.0] = b2[0.0]
            sl.append(('t0=%g' % t0, ser))
            series[(cell, start, t0)] = ser
        table('%s %s' % (cell, start), sl)
    out['lam_star_rescue'] = {}
    out['harm'] = {}
    md.append('**Thresholds (first Lam on the grid, ascending, whose endpoint crosses V* = 0.5)**')
    md.append('')
    md.append('| arm, start | t0 | rescue Lam* (V* >= 0.5 from a start below) | harm Lam (V* < 0.5 from a start above) | max Lam tested |')
    md.append('|---|---|---|---|---|')
    for (cell, start, t0), ser in series.items():
        if not ser:
            continue
        v0 = ser.get(0.0, None)
        v_first = ser[min(ser)]['shares'][0]
        rs = lam_star(ser, 'rescue') if v_first < 0.5 else None
        hm = lam_star(ser, 'harm') if v_first >= 0.5 else None
        mx = max(ser)
        out['lam_star_rescue']['%s %s t0=%g' % (cell, start, t0)] = rs
        md.append('| %s %s | %g | %s | %s | %g |' % (cell, start, t0, 'none' if (v_first < 0.5 and rs is None) else ('-' if v_first >= 0.5 else '%g' % rs),
                                                      'none' if (v_first >= 0.5 and hm is None) else ('-' if v_first < 0.5 else '%g' % hm), mx))
    md.append('')
    # monotonicity
    md.append('**Non-monotone series (a decrease of endpoint V* by more than 0.01 between adjacent grid points)**')
    md.append('')
    nm = []
    for key, ser in series.items():
        d = decreases(ser)
        if d:
            nm.append((key, d))
    if nm:
        for key, d in nm:
            md.append('- %s: %s' % (key, '; '.join('%g -> %g: %.4f -> %.4f' % x for x in d)))
    else:
        md.append('- none')
    md.append('')
    out['non_monotone'] = [(str(k), d) for k, d in nm]

    # harm bisection
    for r in rows:
        if r['spec']['kind'] == 'bisect':
            md.append('**Bisection** (mode %s, series %s): Lam* = %s, bracket %s, evaluations %s' % (r.get('mode'), json.dumps(r['series']['cell']) + ' ' + r['series']['start'] +
                                                                                              ' t0=' + str(r['series']['sched'].get('t0')), r.get('lam_star'), r.get('bracket'), r.get('evals')))
            md.append('')
            out.setdefault('bisect', []).append(dict(series=r['series'], mode=r.get('mode'), lam_star=r.get('lam_star'), bracket=r.get('bracket'), evals=r.get('evals'), grid=r.get('grid')))

    # ------------------------------------------------------------------ late tail
    H('Late tail: from M\'s tail-free state at tau = t_s = 1e6')
    late0 = [r for r in rows if r['spec']['kind'] == 'late0' and r['spec'].get('N', 100) == 100]
    if late0:
        r = late0[0]
        md.append('Tail-free state at t_s: class shares F/U/G/W/D = %s; donor marginal mass of the nine constants in slot 0 (action index 0..8):' % [round(v, 6) for v in r['shares_late']])
        md.append('')
        md.append('`%s`' % [float('%.2e' % v) for v in r['donor_const'][0]])
        md.append('')
        md.append('Offering constants (name the underpaid member at 1/3 or 1/2) and the exit constant (names the excluded slot at 1/2) are at 1e-17 or below;')
        md.append('the baseline donor supply is zero, so the baseline-zero rerun is vacuous (same state).')
        md.append('')
        out['donor_const_slot0'] = r['donor_const'][0]
    sl = []
    for t0 in (1.0, 100.0, 1e4):
        ser = pick(rows, kinds=('dsl',), cell='M0', start='late', sk='anneal', t0=t0, tail='full', N=100, obj='P', rtol=None, spd=None, keep_x=None)
        if late0:
            ser[0.0] = late0[0]
        sl.append(('late t0=%g' % t0, ser))
        series[('M0', 'late', t0)] = ser
    table('M0 late (V*)', sl)
    # exponent of the rescued mass: V*(Lam) - V*(0) vs Lam for Lam in 0.01..0.3
    md.append('**Small-Lam response of the late tail** (endpoint V* minus the tail-free V*, Lam in 0.01, 0.03, 0.1, 0.3):')
    md.append('')
    expo = {}
    for t0 in (1.0, 100.0, 1e4):
        ser = series[('M0', 'late', t0)]
        v0 = ser[0.0]['shares'][0] if 0.0 in ser else None
        pts = [(l, ser[l]['shares'][0] - v0) for l in (0.01, 0.03, 0.1, 0.3) if l in ser and v0 is not None]
        md.append('- t0=%g: %s' % (t0, ', '.join('%g: %.2e' % p for p in pts)))
        expo[str(t0)] = pts
    md.append('')
    out['late_small_lam'] = expo

    # ------------------------------------------------------------------ constant rain
    H('Constant rain: eps = Lam/1e4 on [0, 1e4], M natural')
    ser = pick(rows, kinds=('dsl',), cell='M0', start='nat', sk='const', tail='full', N=100, obj='P')
    if ser:
        table('M0 nat, constant rain', [('rain T=1e4', ser)])
        out['rain'] = {str(l): r['shares'][0] for l, r in ser.items()}

    # ------------------------------------------------------------------ arm T
    H('Arm T (27 programs), main dose')
    sl = []
    mins = {}
    for cell in ('main|0.1|0', 'main|0|0'):
        for start in ('nat', 'u:0.8'):
            for t0 in (1.0, 100.0, 1e4):
                ser = pick(rows, kinds=('armT',), cell=cell, start=start, sk='anneal', t0=t0)
                if ser:
                    sl.append(('%s %s t0=%g' % (cell, start, t0), ser))
                    mins['%s %s t0=%g' % (cell, start, t0)] = min(r['shares'][0] for r in ser.values())
    table('arm T endpoint V*', sl, lams=[0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1e3, 1e4])
    md.append('Minimum endpoint V* per series: %s' % json.dumps({k: float('%.6f' % v) for k, v in mins.items()}))
    md.append('')
    out['armT_min_vstar'] = mins

    # ------------------------------------------------------------------ attribution
    H('Attribution (M natural, t0 = 100)')
    for r in rows:
        if r['spec']['kind'] != 'attr':
            continue
        Lam = r['spec']['sched']['Lam']
        names = r.get('famnames', [])
        md.append('**Lam = %g** (status %s, V* at the end of the integration %.4f)' % (Lam, r['status'], r['shares_end'][0]))
        md.append('')
        for snap in ('1000', '10000', '100000'):
            if snap not in r['snaps']:
                continue
            tail = r['snaps'][snap]['tail']
            mig = r['snaps'][snap]['mig']

            def agg(entries, keyfun, filt=lambda e: True):
                d = {}
                for e in entries:
                    if filt(e):
                        d[keyfun(e)] = d.get(keyfun(e), 0.0) + e[-1]
                return d
            ca = lambda e: '%s->%s' % (CLS[e[0]], CLS[e[1]])
            md.append('- integrated to tau = %s. direct tail flux by class transition: %s' % (snap, {k: float('%.3e' % v) for k, v in sorted(agg(tail, ca).items(), key=lambda kv: -kv[1])[:8]}))
            md.append('  migrant flux by class transition: %s' % ({k: float('%.3e' % v) for k, v in sorted(agg(mig, ca).items(), key=lambda kv: -kv[1])[:8]}))
            for tr in ((1, 0), (0, 1), (0, 3), (3, 1)):
                fam = agg(tail, lambda e: names[e[2]], lambda e: (e[0], e[1]) == tr)
                famm = agg(mig, lambda e: names[e[2]], lambda e: (e[0], e[1]) == tr)
                if fam or famm:
                    md.append('  %s->%s by arriving family: tail %s; migrants %s' % (CLS[tr[0]], CLS[tr[1]],
                              {k: float('%.2e' % v) for k, v in sorted(fam.items(), key=lambda kv: -kv[1])[:5]},
                              {k: float('%.2e' % v) for k, v in sorted(famm.items(), key=lambda kv: -kv[1])[:5]}))
            # U->F by source category (E holds an offering constant) for tail and migrants
            for who, ent in (('tail', tail), ('migrants', mig)):
                c = agg(ent, lambda e: 'E-offers' if e[4] == 1 else 'E-other', lambda e: (e[0], e[1]) == (1, 0))
                if c:
                    md.append('  U->F %s flux by source category: %s' % (who, {k: float('%.2e' % v) for k, v in c.items()}))
        md.append('')
        out.setdefault('attr', {})[str(Lam)] = dict(status=r['status'], shares_end=r['shares_end'])

    # ------------------------------------------------------------------ ablations
    H('Tail-composition ablations (M natural, t0 = 100; the removed prior mass becomes null events unless renorm)')
    sl = []
    for tail in ('full', 'bully', 'victim', 'bully+victim', 'cond'):
        for ren in (False, True):
            ser = pick(rows, kinds=('dsl',), cell='M0', start='nat', sk='anneal', t0=100.0, tail=tail, renorm=ren, N=100, obj='P', rtol=None, spd=None, keep_x=None)
            if tail == 'full':
                if ren:
                    continue
                ser = {l: r for l, r in ser.items() if l in (100.0, 1e4)}
            if ser:
                sl.append(('tail=%s%s' % (tail, ' (renorm)' if ren else ''), ser))
    table('ablations', sl, lams=[100.0, 1e4])

    # ------------------------------------------------------------------ N scaling
    H('N scaling of the tail (hybrid object: fixation kernel at N, founding law of N = 100)')
    for N in (100, 200, 400):
        late = [r for r in rows if r['spec']['kind'] == 'late0' and r['spec'].get('N', 100) == N]
        l0 = late[0]['shares'] if late else None
        s1 = pick(rows, kinds=('dsl',), cell='M0', start='nat', sk='anneal', t0=100.0, tail='full', N=N, obj='P', rtol=None, spd=None, keep_x=None)
        s2 = pick(rows, kinds=('dsl',), cell='M0', start='late', sk='anneal', t0=1.0, tail='full', N=N, obj='P', rtol=None, spd=None, keep_x=None)
        md.append('- N=%d: tail-free endpoint (late0 row) F/U = %s; natural t0=100: %s; late t0=1: %s' % (
            N, ('%.4f / %.4f' % (l0[0], l0[1])) if l0 else 'n/a',
            ', '.join('%g: %.4f' % (l, r['shares'][0]) for l, r in sorted(s1.items())) or 'n/a',
            ', '.join('%g: %.4f' % (l, r['shares'][0]) for l, r in sorted(s2.items())) or 'n/a'))
    md.append('')
    md.append('Single-island neutral entry probability per arrival at N: 1/N = %s' % ', '.join('%g (N=%d)' % (1.0 / n, n) for n in (100, 200, 400)))
    md.append('')

    # ------------------------------------------------------------------ objects, numerics, asym
    H('Object variants (6b), numerics and symmetry checks')
    for objv in ('P', 'm1core', 'm1full'):
        ser = pick(rows, kinds=('dsl',), cell='M0', start='nat', sk='anneal', t0=100.0, tail='full', N=100, obj=objv, rtol=None, spd=None, keep_x=None)
        if objv != 'P':
            if ser:
                md.append('- obj %s: %s' % (objv, ', '.join('%g: V*=%.4f U=%.4f (%s)' % (l, r['shares'][0], r['shares'][1], r['class']) for l, r in sorted(ser.items()))))
    for r in rows:
        if r['spec']['kind'] == 'asym':
            md.append('- asymmetric perturbation delta=%g of the L natural endpoint, unprojected, to tau=%g: V*=%.6f, pairs %s' % (
                r['spec']['delta'], r['tau_end'], r['shares'][0], [round(v, 6) for v in r['pairs']]))
    md.append('')
    return rows, out, md


if __name__ == '__main__':
    rows, out, md = main()
    open(os.path.join(ROOT, 'runs', 'annealed-tail-tables.md'), 'w').write('\n'.join(md))
    json.dump(out, open(os.path.join(ROOT, 'runs', 'annealed-tail.json'), 'w'), indent=1, default=str)
    print('\n'.join(md))
