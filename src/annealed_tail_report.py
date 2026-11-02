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


def head_md(rows):
    md = []
    md.append('# An annealed mutation tail on the unequal basin of majority division (queue 71): run report')
    md.append('')
    md.append('**Question and design (reminder).** Queue 70 found the length-prior arms L (weak evaluator) and M (modalPA) bistable in the tail-free')
    md.append("islands-to-infinity chain: M's natural start ends unequal (V* 0.1004, U 0.8996) because its boundary u* = 0.425 sits just under the natural")
    md.append('unequal share 0.429; two Trojan-bully programs per slot pull the boundary down, and each outcome is a ratchet that depletes the programs that could')
    md.append('leave it. The ratchet is an eps = 0 statement. This run adds the annealed prior tail the object keeps: after founding, prior arrivals at rate')
    md.append('eps(t) = (Lam/t0)(1 + t/t0)^-2 per island per migrant event (Lam = total arrivals per island, t0 = how early), uniformly random slot, program drawn from')
    md.append("the slot's founding prior, fixing with the migrant kernel: dx/dt = F(x) + eps(t) G(x; p). N = 100, w = 0.3, object P (the reflecting m = 3 truncation on")
    md.append("queue 70's 48-conditional core), arms L and M; arm T (27 programs) on its own ODE. RS 2026-11-01: \"Go ahead w the annealing run\". Spec")
    md.append('`specs/2026-11-01-annealed-tail-dollar3.md`, predictions `predictions/2026-11-01-annealed-tail.md` (committed before any counted cell), notes')
    md.append('`notes/annealed-tail.md`, code `src/annealed_tail*.py`, rows `runs/annealed_tail/`.')
    md.append('')
    md.append('## Validations')
    md.append('')
    v1 = jl('v1'); v2 = jl('v2'); v4 = jl('v4')
    if v1:
        md.append('- **V1 (Lam = 0 reproduces queue 70 / 69).** Maximum endpoint difference to the stored rows: %s; trajectories (1e2, 1e3, 1e4 events) within 5e-8. Arm T natural endpoints (P_fail 0.1 and 0) within 6.2e-12 of the stored ODE.' % (
            ', '.join('%s %.1e' % (k, v['endpoint_maxdiff']) for k, v in v1.items() if 'endpoint_maxdiff' in v)))
    if v2:
        md.append('- **V2.** Linearity of the field in the donor law: max abs deviation %.1e on a field of scale %.1e; mass conservation of F + eps G: <= %.1e at eps up to 300; S3 equivariance of G: %.1e; arm T mass conservation <= %.1e. Prior law and the restricted prior S3-invariant to 0.0 (static.json).' % (
            v2['linearity_max_abs'], v2['linearity_scale'], max(v2['mass_conservation'].values()), v2['tail_field_S3_equivariance'], max(v2['armT_mass_conservation'].values())))
    for nm, lab in (('v3_M0_L10_t100', 'Lam = 10'), ('v3_M0_L100_t100', 'Lam = 100'), ('v3_M0_L0_t100', 'Lam = 0 control'), ('v3_M0_L10_t100_I16384', 'Lam = 10, I = 16,384')):
        v = jl(nm)
        if v:
            rr = {x['t']: x for x in v['rows']}
            md.append('- **V3 (%s, t0 = 100, M natural, I = %d, %d worlds).** max |ODE - MC| over the five classes: %s; at 1e4 events %.3f.' % (
                lab, v['I'], v['nworld'], ', '.join('%d: %.4f' % (t, rr[t]['maxdiff']) for t in (100, 1000, 3000) if t in rr), rr[10000]['maxdiff']))
    md.append('  The gate times 1e2 and 1e3 pass (<= 0.012 at I = 4,096, <= 0.001 at I = 16,384). The 1e4 gate is **not informative and fails even at Lam = 0**: M natural passes through a sharp F -> U transition at about 1.2e4 events in the ODE (V* 0.98 -> 0.27 in 3e3 events) and the full-dynamics chain makes it earlier (V* at 1e4: 0.36 at I = 4,096, 0.26 at I = 16,384, tail-free), so any comparison at 1e4 measures transition timing, not the tail kernel. Lam = 100 at I = 4,096 agrees at 1e4 (0.015) by coincidence of timing.')
    for fpath in sorted(glob.glob(os.path.join(VAL, 'v3b_*.json'))):
        v = json.load(open(fpath))
        fin = v['cps'][-1]
        md.append('- **V3b (the central contrast against the full-dynamics chain, no truncation).** tail = %s, Lam = %g, t0 = %g, I = %d: V*/U at %d events: ODE %.3f / %.3f; MC worlds %s.' % (
            v['tail'], v['Lam'], v['t0'], v['I'], fin, v['ode'][str(fin)][0], v['ode'][str(fin)][1], '; '.join('%.3f / %.3f' % (w[-1][0], w[-1][1]) for w in v['mc_worlds'])))
    if v4:
        md.append("- **V4 (single-arrival assay, prior arrivals into M's endpoint triples, direct Moran simulation of the island).** %d strata with a testable fixation probability, |z| max %.2f: %s." % (
            sum(1 for o in v4['strata'] if 'z' in o), max(abs(o['z']) for o in v4['strata'] if 'z' in o), 'passed' if v4['passed'] else 'FAILED'))
    md.append('')
    st = json.load(open(os.path.join(RD, 'static.json')))
    m = st['M0']
    md.append('## Static numbers')
    md.append('')
    md.append('- Prior mass per slot: nine constants %.4f (%.5f each), conditionals in the S3-union support %.5f (1,240 of 1,296), of them %.2e in the 48-core; mass outside the union support (always a null event) %.2e; mass restricted to the state set %.5f.' % (
        m['mass_constants'][0], m['mass_per_constant'], m['mass_cond_in_supp'][0], m['mass_cond_in_core'][0], m['mass_outside_supp'][0], m['mass_in_supp'][0]))
    md.append('- Offering constants (E toward Lw at 1/3 or 1/2): %.4f; exit constant (Lw toward E at 1/2): %.4f; victim constants (name a slot partner at 1/3, either partner): %.4f; Trojan bullies: %.3e; ratio offering : bullies = %.0f : 1.' % (
        m['offering_constants_E_to_Lw'][0]['mass'], m['exit_constant_Lw_to_E'][0]['mass'], m['victim_constants_per_slot'][0]['mass'], m['families']['exploiter-fair']['mass'][0],
        m['offering_constants_E_to_Lw'][0]['mass'] / m['families']['exploiter-fair']['mass'][0]))
    for r in rows:
        if r['spec']['kind'] == 'blocked':
            o = r['spec'].get('obj', 'P')
            st0 = r['start']
            md.append('- Blocked flux (null events of the reflecting truncation), object %s, at the natural start: migrants %.2e of their flux, tail %.2e of its flux%s.' % (
                o, st0['frac_migrant'], st0['frac_tail'], ('; at the tail-free endpoint: migrants %.1e, tail %.3f' % (r['tail_free_endpoint']['frac_migrant'], r['tail_free_endpoint']['frac_tail'])) if 'tail_free_endpoint' in r else ''))
    md.append('')
    return md


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
        zero = pick(rows, kinds=('dsl',), cell='M0', start='late', Lam=0.0, tail='full', N=100, obj='P', rtol=None, spd=None, keep_x=None)
        if 0.0 in zero:
            ser[0.0] = zero[0.0]
        elif late0:
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
        fit = ''
        if len(pts) >= 2 and all(abs(v) > 1e-13 for _, v in pts) and all(v > 0 for _, v in pts):
            import math as _m
            sl_ = (_m.log(pts[-1][1]) - _m.log(pts[0][1])) / (_m.log(pts[-1][0]) - _m.log(pts[0][0]))
            fit = '; log-log slope %.3f (response %.2e per arrival)' % (sl_, pts[0][1] / pts[0][0])
        md.append('- t0=%g: %s%s' % (t0, ', '.join('%g: %.2e' % p for p in pts), fit))
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
    # ------------------------------------------------------------------ Lam* of the ablated tails
    H('Lam* of the composition-ablated tails (matched dose; M natural, t0 = 100, N = 100 unless the series says otherwise)')
    abl = {}
    abl_rows = {}
    for r in rows:
        if r['spec']['kind'] != 'bisect' or r.get('mode') != 'rescue':
            continue
        b = r['series']
        key = '%s %s %s N=%d t0=%g' % (b['cell'], b['start'], b.get('tail', 'full'), b.get('N', 100), b['sched'].get('t0', 0))
        if key in abl and abl[key]['lam_star'] is not None and r.get('lam_star') is None:
            continue
        abl[key] = dict(lam_star=r.get('lam_star'), bracket=r.get('bracket'))
        abl_rows[key] = r
    md.append('| series (cell, start, tail, N, t0) | grid / evaluations (Lam: endpoint V*) | Lam* (smallest Lam with V* >= 0.5) | bracket |')
    md.append('|---|---|---|---|')
    for key in sorted(abl_rows):
        r = abl_rows[key]
        ev = {**r.get('grid', {}), **(r.get('evals') or {}), **(r.get('grid2') or {})}
        ev = {float(k): v for k, v in ev.items() if v is not None}
        md.append('| %s | %s | %s | %s |' % (key, ', '.join('%.4g: %.3f' % (k, ev[k]) for k in sorted(ev)),
                                         ('%.4g' % r['lam_star']) if r.get('lam_star') else 'none',
                                         ('(%.4g, %.4g]' % tuple(r['bracket'])) if r.get('bracket') else '-'))
    md.append('')
    md.append('Full tail: no Lam* up to 1e5 (M natural, t0 = 1 and 100). Ablated endpoints reproduce at 10x tighter tolerance and half the backward-Euler step at both bracket points (validation table).')
    md.append('')
    out['ablated_lam_star'] = abl
    # numerics check rows
    num = []
    for r in rows:
        sp = r['spec']
        if sp['kind'] == 'dsl' and sp.get('rtol') is not None:
            base = pick(rows, kinds=('dsl',), cell=sp['cell'], start=sp['start'], sk='anneal', t0=sp['sched'].get('t0'), tail=sp.get('tail', 'full'), N=sp.get('N', 100), obj=sp.get('obj', 'P'), rtol=None, spd=None, keep_x=None)
            b = base.get(sp['sched']['Lam'])
            if b is None:
                for l, rr in base.items():
                    if abs(l - sp['sched']['Lam']) < 1e-9 * max(1, l):
                        b = rr
            num.append((sp.get('tail'), sp['sched']['Lam'], r['class'], r['shares'][0], b['class'] if b else None, b['shares'][0] if b else None))
    out['numerics_check'] = num
    if num:
        md.append('**Numerics check (rtol 1e-10, backward-Euler step halved) at the bracket points**')
        md.append('')
        md.append('| tail | Lam | class (tight) | V* (tight) | class (base) | V* (base) |')
        md.append('|---|---|---|---|---|---|')
        for t in sorted(num, key=lambda z: (str(z[0]), z[1])):
            md.append('| %s | %.4g | %s | %.6f | %s | %s |' % (t[0], t[1], t[2], t[3], t[4], ('%.6f' % t[5]) if t[5] is not None else '-'))
        md.append('')

    # ------------------------------------------------------------------ endpoint structure
    H('Endpoint support and transition structure (M natural, t0 = 100)')
    dg = []
    for r in rows:
        sp = r['spec']
        if sp['kind'] == 'dsl' and sp.get('diag') and 'endpoint_diag' in r:
            dg.append((sp.get('tail', 'full'), sp['sched']['Lam'], r))
    for tail, Lam, r in sorted(dg, key=lambda z: (z[0], z[1])):
        d = r['endpoint_diag']
        cf = d['migrant_class_flux']
        fl = ', '.join('%s>%s %.3g' % (d['classes'][a], d['classes'][b], cf[a][b]) for a in range(5) for b in range(5) if cf[a][b] > 1e-12)
        md.append('- tail=%s, Lam=%.4g: endpoint class %s, F/U = %.5f / %.5f; programs with donor mass > 1e-9 per slot: %s (> 1e-12: %s); pairs %s; leading donors (slot 0): %s; migrants\' class flux per event: %s.' % (
            tail, Lam, r['class'], r['shares'][0], r['shares'][1], d['support'], d['support12'], [round(v, 4) for v in d['pairs']],
            '; '.join('%s %.3g' % (n.replace('if(BOX', 'if(BOX'), q) for n, q in d['top_donor_names'][0][:5]), fl))
    md.append('')
    # ------------------------------------------------------------------ verdicts
    H('Prediction verdicts')
    V = []

    def add(pid, claim, verdict, number):
        V.append((pid, claim, verdict, number))
    M1, M100 = series.get(('M0', 'nat', 1.0), {}), series.get(('M0', 'nat', 100.0), {})
    maxv_le30 = max([r['shares'][0] for l, r in list(M1.items()) + list(M100.items()) if 0 < l <= 30] or [float('nan')])
    maxv_all = max([r['shares'][0] for l, r in list(M1.items()) + list(M100.items()) if l > 0] or [float('nan')])
    add('RE1', 'M natural: some Lam <= 30 reaches V* >= 0.99 at t0 = 1 and 100, V* non-decreasing', 'FAILED',
        'max V* over Lam <= 30: %.4f; over every Lam tested (to 1e5 at t0 = 100, to 1e4 at t0 = 1): %.4f; M nat endpoint is the tail-free 0.1004 at every Lam' % (maxv_le30, maxv_all))
    cl1, cl100, cl1e4 = [abl.get('M0 nat bully+victim N=100 t0=%s' % t, {}).get('bracket') for t in ('1', '100', '10000')]
    late_clean = [r['shares'][0] for r in rows if r['spec']['kind'] == 'dsl' and r['spec'].get('start') == 'late' and r['spec'].get('tail') in ('victim', 'bully+victim') and r['spec'].get('N', 100) == 100 and r['spec']['sched']['Lam'] > 0]
    add('RE2', 'Lam*(late) >= 10 Lam*(t0 = 1)', 'UNSCORED for the full tail (neither flips); HELD for the clean tail',
        'full tail: no Lam* early or late; victim+bully-less tail: early Lam*(t0 = 1) in %s, Lam*(t0 = 100) in %s, Lam*(t0 = 1e4) in %s, settled-ratchet late tail (t_s = 1e6) does not flip at any Lam tested (max V* %.4f, Lam up to 1e4), ratio > 250' % (cl1, cl100, cl1e4, max(late_clean) if late_clean else float('nan')))
    add('RE3', 'constant rain and t0 = 100 annealed within a factor 3 in Lam*', 'UNSCORED (vacuous)', 'constant rain: V* = 0.1004 at every Lam <= 300; no Lam* either way')
    minL = min([r['shares'][0] for (c, st, t0), ser in series.items() if c == 'L0' and st == 'nat' for l, r in ser.items() if l <= 300] or [float('nan')])
    minT = min(out['armT_min_vstar'].values()) if out.get('armT_min_vstar') else float('nan')
    add('RE4', 'L natural and arm T keep V* >= 0.999 at every Lam, t0 on the grid (Lam <= 300), cell 7 included', 'HELD on the spec grid; FAILS in extension (L natural)',
        'min V* on the grid: L natural %.4f, arm T %.6f; extension: L natural t0 = 100 falls to U at Lam in (2.4e4, 3.2e4] (V* 0.9997 -> 0), t0 = 1 holds to 1e5' % (minL, minT))
    # P5 pieces from attribution
    p5 = 'see attribution'
    for r in rows:
        if r['spec']['kind'] == 'attr' and r['spec']['sched']['Lam'] == 100.0 and r['spec'].get('tail', 'full') == 'full' and '10000' in r.get('snaps', {}):
            tail = r['snaps']['10000']['tail']
            uf = {1: 0.0, 2: 0.0}
            for e in tail:
                if (e[0], e[1]) == (1, 0):
                    uf[e[4]] = uf.get(e[4], 0.0) + e[-1]
            share_off = uf.get(1, 0.0) / max(sum(uf.values()), 1e-300)
            fu = {}
            for e in tail:
                if (e[0], e[1]) == (0, 1):
                    fu[e[2]] = fu.get(e[2], 0.0) + e[-1]
            tot = sum(fu.values())
            vict = (fu.get(0, 0) + fu.get(3, 0) + fu.get(9, 0)) / max(tot, 1e-300)
            p5 = 'direct tail flux at Lam = 100, tau = 1e4: U->F through sources whose excluded slot holds an offering constant %.3f of the U->F flux; F->U carried by the 1/3 constants (c0, c3) and bullies: %.3f (the 2/3 constants c2, c5: %.3f)' % (
                share_off, vict, (fu.get(2, 0) + fu.get(5, 0)) / max(tot, 1e-300))
    lb = abl.get('M0 nat bully N=100 t0=100', {}).get('bracket'); lv = abl.get('M0 nat victim N=100 t0=100', {}).get('bracket')
    add('RE5', 'rescue carried by excluded-slot offering constants (>= 0.7) and by victims with bullies (>= 0.7); bully ablation < 1.25x; victim ablation >= 1.5x', 'FAILED (bully clause and second share)',
        '%s; bully-less tail Lam* in %s against none for the full tail (moves it by far more than 1.25x); victim-less tail Lam* in %s (lowers it)' % (p5, lb, lv))
    vs = {n: abl.get('M0 nat victim N=%d t0=100' % n, {}) for n in (100, 200, 400)}
    br = {n: vs[n].get('bracket') for n in vs}
    ratio_lo = (br[400][0] / br[100][1]) if br[400] and br[100] else None
    ratio_hi = (br[400][1] / br[100][0]) if br[400] and br[100] else None
    r12 = ((br[200][0] / br[100][1]), (br[200][1] / br[100][0])) if br[200] and br[100] else None
    r23 = ((br[400][0] / br[200][1]), (br[400][1] / br[200][0])) if br[400] and br[200] else None
    add('RE6', 'Lam*(400)/Lam*(100) in [2.5, 6] at t0 = 100', 'FAILED', 'full tail: no Lam* at any N; victim-less tail (the series that has one): Lam* in %s, %s, %s at N = 100, 200, 400, ratio 400/100 in [%.0f, %.0f]' % (br[100], br[200], br[400], ratio_lo or 0, ratio_hi or 0))
    add('RE7', 'L at u = 0.6 flips to V* at Lam* <= 10 for t0 = 1', 'FAILED', 'full tail: L u = 0.6 stays at U 0.9949 at every Lam <= 300 and every t0 (V* = 0.0000); clean tail: Lam* in %s at t0 = 1' % (abl.get('L0 u:0.6 bully+victim N=100 t0=1', {}).get('bracket'),))
    add('argon a', 'bully tail ablation < 1.05x; victim ablation >= 1.5x', 'FAILED / HELD', 'bully ablation: none -> (274, 316]; victim ablation: none -> (75, 87] (held)')
    add('argon b', 'Lam*(400)/Lam*(100) < 2.5 for the early tail', 'FAILED (on the victim-less tail)', 'ratio 400/100 in [%.0f, %.0f]; the full tail has no Lam*' % (ratio_lo or 0, ratio_hi or 0))
    dm1 = abl.get('M0 u:0.6 bully+victim N=100 t0=1', {}).get('bracket')
    dm100 = abl.get('M0 u:0.6 bully+victim N=100 t0=100', {}).get('bracket')
    dl1 = abl.get('L0 u:0.6 bully+victim N=100 t0=1', {}).get('bracket')
    dl100 = abl.get('L0 u:0.6 bully+victim N=100 t0=100', {}).get('bracket')
    nm1 = abl.get('M0 nat bully+victim N=100 t0=1', {}).get('bracket')
    add('sol c', 'early M-natural rescue substantially easier than deep-U rescue (M u = 0.6, late arm); the prior\'s constant share alone will not predict the latter', 'HELD (for the clean tail; the full tail rescues nothing)',
        'clean tail, t0 = 1: M natural Lam* in %s; M u = 0.6 in %s (ratio %s); L u = 0.6 in %s; t0 = 100: M u = 0.6 in %s, L u = 0.6 in %s; settled late tail: no flip to 1e4; constants-only tail flips early at (750, 866] and has no late flip tested' % (
            nm1, dm1, ('%.0f-%.0f' % (dm1[0] / nm1[1], dm1[1] / nm1[0])) if dm1 and nm1 else 'n/a', dl1, dm100, dl100))
    add('sol d', 'no clean proportional scaling of Lam* across N', 'HELD', 'victim-less tail: 100 -> 200 multiplies Lam* by [%.0f, %.0f], 200 -> 400 by [%.1f, %.1f]; not a power law in N, and nowhere near proportional' % (r12[0], r12[1], r23[0], r23[1]))
    add('sol e', 'V* non-monotone in Lam somewhere', 'HELD (extension only)', 'L natural, t0 = 100: V* 0.9997 -> 0 between Lam 2.4e4 and 3.2e4; no decrease > 0.01 on the spec grid')
    add('E1', 'Lam*(M nat, t0 = 1) <= 3 and Lam*(t0 = 100) <= 10', 'FAILED', 'none to 1e5 (t0 = 100), to 1e4 (t0 = 1)')
    add('E2', 'no late Lam <= 300 has V* >= 0.5', 'HELD', 'late V* = 0.1004 at every Lam to 1e5 (t0 = 1, 100), to 300 (t0 = 1e4), and for the victim-less and victim+bully-less tails at 1e2-1e4')
    add('E3', 'victim ablation moves Lam* by < 1.25x', 'FAILED', 'victim-less tail Lam* in (75, 87] against none; the 1/3 constants carry the full tail\'s block')
    add('E4', 'constants-only tail has Lam* within 1.25x of the full tail', 'FAILED', 'constants-only Lam* in (750, 866] against none')
    n200 = [r for r in rows if r['spec']['kind'] == 'late0' and r['spec'].get('N', 100) == 200]
    n400 = [r for r in rows if r['spec']['kind'] == 'late0' and r['spec'].get('N', 100) == 400]
    add('E5', 'M natural tail-free hybrid endpoint is U-dominated at N = 200 and 400', 'HELD' if (n200 and n400 and n200[0]['shares'][0] < 0.5 and n400[0]['shares'][0] < 0.5) else 'CHECK',
        'tail-free V*: N = 200: %s, N = 400: %s' % (('%.4f' % n200[0]['shares'][0]) if n200 else 'n/a', ('%.4f' % n400[0]['shares'][0]) if n400 else 'n/a'))
    add('E6', 'monotone to within 0.01 on every series with a Lam* in the grid', 'HELD (vacuous for the full tail)', 'no full-tail series has a Lam*; the ablated bisection series are monotone (step functions)')
    cell7 = [mins for k, mins in out['armT_min_vstar'].items() if 't0=1' in k and k.endswith('t0=1')]
    add('E7', 'arm T at Lam = 300, t0 = 1: V* >= 0.999', 'HELD', 'min V* over the four arm-T series at Lam = 300, t0 = 1: %s' % (min(cell7) if cell7 else 'n/a'))
    md.append('| prediction | claim | verdict | number that scores it |')
    md.append('|---|---|---|---|')
    for pid, claim, verdict, number in V:
        md.append('| %s | %s | %s | %s |' % (pid, claim, verdict, number.replace('|', '/')))
    md.append('')
    out['verdicts'] = [dict(id=a, claim=b, verdict=c, number=d) for a, b, c, d in V]
    return rows, out, md


if __name__ == '__main__':
    rows, out, md = main()
    md = head_md(rows) + md
    open(os.path.join(ROOT, 'runs', 'annealed-tail.md'), 'w').write('\n'.join(md))
    json.dump(out, open(os.path.join(ROOT, 'runs', 'annealed-tail.json'), 'w'), indent=1, default=str)
    print('\n'.join(md))
