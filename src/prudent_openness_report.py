"""Summaries and tables for the prudent-openness run (runs/prudent-openness.md, .json).

    python3 src/prudent_openness_report.py            # writes runs/prudent-openness.json and runs/prudent_openness/tables.md
"""
import json, os, sys
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import prudent_openness as PO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs', 'prudent_openness')
CK = [str(t) for t in PO.CKPTS]
PART1 = ['L', 'P1', 'P2', 'P3', 'P4', "P4'", 'P5', 'P1p', 'P2n', 'P3p', 'P4p', 'P4n', 'P5p']
DESC = {'L': 'L', 'P1': 'P1: F_P at M', 'P2': 'P2: ten CB spellings (T1c)', 'P3': 'P3: F_P at M, identity removed',
        'P4': 'P4: F_P at M, cooperators removed', "P4'": "P4′: P2, cooperators removed", 'P5': 'P5: F_P at M/2 + ten EQ at M/20',
        'P1p': 'P1p: core at M', 'P2n': 'P2n: nice part at M', 'P3p': 'P3p: core at M, identity removed',
        'P4p': 'P4p: core at M, cooperators removed', 'P4n': 'P4n: nice at M, cooperators removed', 'P5p': 'P5p: core at M/2 + ten EQ at M/20'}
OUTCOMES = ['universal-open', 'universal-other', 'patchwork', 'unresolved', 'failed']


def load(fn):
    p = os.path.join(OUT, fn)
    return json.load(open(p)) if os.path.exists(p) else []


def by_cell(rows):
    d = defaultdict(list)
    for r in rows:
        d[r['cell']].append(r)
    for c in d:
        d[c].sort(key=lambda r: r['rep'])
    return d


def mean(xs):
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else None


def cell_summary(rows):
    n = len(rows)
    I = rows[0]['I']
    s = dict(n=n, I=I, N=rows[0]['N'])
    for T in CK:
        ck = [r['ck'][T] for r in rows]
        oc = Counter(c['outcome'] for c in ck)
        s[T] = dict(outcomes={o: oc.get(o, 0) for o in OUTCOMES},
                    univ={f: sum(c['univ'][f] for c in ck) for f in PO.FAMS},
                    held={f: mean([c['held'][f] / I for c in ck]) for f in PO.FAMS},
                    held_XB=mean([c['held_XB'] / I for c in ck]),
                    cross=mean([c['cross_pcc'] for c in ck]), cross_readers=mean([c['cross_readers'] for c in ck]),
                    cross_FP_islands=mean([c['cross_FP_islands'] for c in ck]),
                    n_cross_FP_islands=sum(1 for c in ck if c['cross_FP_islands'] is not None),
                    island_pcc=mean([c['island_pcc'] for c in ck]),
                    separated=sum(c['separated'] for c in ck))
    st = {}
    for f in PO.FAMS:
        ss = [r['stages'][f] for r in rows]
        occ = sum(x['occupied'] for x in ss); n0 = sum(x['n0'] for x in ss)
        et = [t for x in ss for t in x['est_times']]
        d = dict(n0_per_run=n0 / n, occupied_per_run=occ / n, est_time_median=float(np.median(et)) if et else None,
                 est_time_q90=float(np.quantile(et, 0.9)) if et else None)
        for T in CK:
            Ti = int(T)
            se = sum(x[Ti]['seeded_est'] if Ti in x else x[T]['seeded_est'] for x in ss)
            g = lambda k: sum((x[Ti] if Ti in x else x[T])[k] for x in ss)
            d[T] = dict(est_per_occupied=se / occ if occ else None, extinct_prob=g('extinct') / occ if occ else None,
                        persistence=g('persist') / se if se else None, spread_per_run=g('spread') / n,
                        held_per_run=g('held') / n, islands_per_copy=g('held') / n0 if n0 else None,
                        seeded_est_per_run=se / n)
        st[f] = d
    s['stages'] = st
    pool = {}
    for T in ('2000', '10000'):
        ps = [r['pooling'].get(T) for r in rows if r['pooling'].get(T)]
        dec = [p for p in ps if p['decided']]
        pool[T] = dict(decided=len(dec), best_est_won=sum(1 for p in dec if p['best_est_won']), best_seed_won=sum(1 for p in dec if p['best_seed_won']))
    s['pooling'] = pool
    tr = {}
    for k in rows[0]['track']:
        xs = [r['track'][k] for r in rows]
        tr[k] = dict(seeded_runs=sum(1 for x in xs if x.get('seeded', 0) > 0),
                     alive_at_first_sep=sum(1 for x in xs if x.get('alive_at_first_sep')),
                     ever_held_runs=sum(1 for x in xs if x.get('max_isl', 0) > 0),
                     extinct_runs=sum(1 for x in xs if x.get('seeded', 0) > 0 and x.get('ext', -1) >= 0))
    s['track'] = tr
    s['consistency'] = all(all(r['consistency'].values()) for r in rows)
    s['frozen'] = sum(1 for r in rows if r['frozen_gen'] >= 0)
    s['E3_success'] = sum(1 for r in rows if r['E3'] == 'success')
    s['seeded_identity_classes'] = mean([r['seeded_identity_classes'] for r in rows])
    s['seeded'] = {f: mean([r['seeded'][f] for r in rows]) for f in PO.FAMS}
    return s


def scan_points(cells, prefix, m_L):
    """[(m, rows)] sorted by m: the eight scan points plus refinement points scanXm_<m>; scanA at m_L is the L cell."""
    pts = []
    for i, m in enumerate(PO.SCAN_M):
        rows = cells.get('%s_%d' % (prefix, i)) or (cells.get('L') if (prefix == 'scanA' and i == 6) else None)
        if rows is not None:
            pts.append((m if m is not None else m_L, rows, '%s_%d' % (prefix, i)))
    for c, rows in cells.items():
        if c.startswith(prefix + 'm_'):
            pts.append((float(c.split('_')[1]), rows, c))
    return sorted(pts, key=lambda t: t[0])


def scan_summary(cells, m_L):
    out = {}
    base_ms = [m if m is not None else m_L for m in PO.SCAN_M]
    for pre in ('scanA', 'scanB'):
        pts = scan_points(cells, pre, m_L)
        if len(pts) < len(PO.SCAN_M):
            continue
        ms = [p[0] for p in pts]
        d = dict(ms=ms, copies=[6400 * m for m in ms], cells=[p[2] for p in pts], refined=[p[2] for p in pts if 'm_' in p[2]])
        for T in CK:
            X = np.array([[1.0 if r['ck'][T]['outcome'] == 'universal-open' else 0.0 for r in p[1]] for p in pts])
            f = X.mean(1)
            m0, fl, lo, hi, smp = PO.bootstrap_crossing(ms, X, B=2000, seed=11)
            low = np.array(ms) <= 1e-3
            f1 = PO.fit_exp(np.array(ms)[low], f[low], prefactor=False)
            f2 = PO.fit_exp(np.array(ms)[low], f[low], prefactor=True)
            res1 = (f - np.exp(-6400 * np.array(ms) * f1['q'])).tolist()
            res2 = (f - f2['f0'] * np.exp(-6400 * np.array(ms) * f2['q'])).tolist()
            # the crossing on the eight preregistered points only (before refinement)
            Xb = np.array([[1.0 if r['ck'][T]['outcome'] == 'universal-open' else 0.0 for r in p[1]] for p in pts if 'm_' not in p[2]])
            mb = PO.crossing(base_ms, Xb.mean(1))
            d[T] = dict(f=f.tolist(), k=X.sum(1).astype(int).tolist(), crossing=m0, flag=fl, lo=lo, hi=hi,
                        boundary_frac=float(np.mean((smp <= ms[0]) | (smp >= ms[-1]))), crossing_unrefined=mb[0],
                        fit1=f1, res1=res1, fit2=f2, res2=res2)
        d['identity_islands'] = {T: [mean([r['ck'][T]['held']['identity'] / r['I'] for r in p[1]]) for p in pts] for T in CK}
        d['cross'] = {T: [mean([r['ck'][T]['cross_pcc'] for r in p[1]]) for p in pts] for T in CK}
        d['univ_FP'] = {T: [sum(r['ck'][T]['univ']['FP'] for r in p[1]) for p in pts] for T in CK}
        d['identity_seeded'] = [mean([r['seeded']['identity'] for r in p[1]]) for p in pts]
        d['identity_est_per_occupied'] = {T: [cell_summary(p[1])['stages']['identity'][T]['est_per_occupied'] for p in pts] for T in ('2000', '10000')}
        d['identity_held_per_run'] = {T: [cell_summary(p[1])['stages']['identity'][T]['held_per_run'] for p in pts] for T in ('2000', '10000')}
        out[pre] = d
    if 'scanA' in out and 'scanB' in out:
        out['shift_10000'] = out['scanB']['10000']['crossing'] / out['scanA']['10000']['crossing']
        out['shift_10000_unrefined'] = out['scanB']['10000']['crossing_unrefined'] / out['scanA']['10000']['crossing_unrefined']
        # paired bootstrap of the shift (replicate indices shared across both curves)
        pa, pb = scan_points(cells, 'scanA', m_L), scan_points(cells, 'scanB', m_L)
        XA = np.array([[1.0 if r['ck']['10000']['outcome'] == 'universal-open' else 0.0 for r in p[1]] for p in pa])
        XB = np.array([[1.0 if r['ck']['10000']['outcome'] == 'universal-open' else 0.0 for r in p[1]] for p in pb])
        ma, mb = [p[0] for p in pa], [p[0] for p in pb]
        rng = np.random.default_rng(7)
        sh = []
        for _ in range(2000):
            idx = rng.integers(0, XA.shape[1], XA.shape[1])
            a = PO.crossing(ma, XA[:, idx].mean(1))[0]; b = PO.crossing(mb, XB[:, idx].mean(1))[0]
            sh.append(b / a if a > 0 else np.inf)
        out['shift_10000_ci'] = [float(np.quantile(sh, 0.025)), float(np.quantile(sh, 0.975))]
    return out


def panel_summary(panel_cells, main_cells, ms_pts):
    """panel_cells: cell names like scanA_3@50,64.  Crossing between the two bracketing scan points per (N, I)."""
    out = {}
    groups = defaultdict(dict)
    for c, rows in panel_cells.items():
        base, ni = c.split('@')
        groups[ni][base] = rows
    groups['100,64'] = {b: main_cells[b] if b in main_cells else main_cells['L'] for b in ms_pts}
    for ni, d in groups.items():
        pts = sorted(d.keys(), key=lambda b: int(b.split('_')[1]))
        res = {}
        N, I = (int(x) for x in ni.split(','))
        ms = [PO.SCAN_M[int(b.split('_')[1])] for b in pts]
        for T in ('2000', '10000'):
            f = [float(np.mean([r['ck'][T]['outcome'] == 'universal-open' for r in d[b]])) for b in pts]
            ident = [float(np.mean([r['ck'][T]['held']['identity'] / r['I'] for r in d[b]])) for b in pts]
            m, fl = PO.crossing(ms, f)
            res[T] = dict(points=pts, ms=ms, f=f, identity_islands=ident, crossing=m, flag=fl, copies_at_crossing=N * I * m,
                          k=[int(sum(r['ck'][T]['outcome'] == 'universal-open' for r in d[b])) for b in pts])
        out[ni] = res
    return out


def fmt(x, d=3):
    if x is None:
        return '–'
    if isinstance(x, float):
        if x != 0 and (abs(x) < 1e-3 or abs(x) >= 1e4):
            return '%.2e' % x
        return ('%.' + str(d) + 'f') % x
    return str(x)


def tables(S):
    L = []
    p1 = S['part1']
    L.append('### Outcomes at the common checkpoints (40 runs per cell; universal-open / F_P-universal / core-universal / patchwork / unresolved / failed)\n')
    L.append('| cell | ' + ' | '.join('@%s' % T for T in CK) + ' |')
    L.append('|---|' + '---|' * len(CK))
    for c in PART1:
        if c not in p1: continue
        s = p1[c]
        L.append('| %s | ' % DESC[c] + ' | '.join('%d / %d / %d / %d / %d / %d' % (s[T]['outcomes']['universal-open'], s[T]['univ']['FP'], s[T]['univ']['core'],
                                                                               s[T]['outcomes']['patchwork'], s[T]['outcomes']['unresolved'], s[T]['outcomes']['failed']) for T in CK) + ' |')
    L.append('\n### Island shares at 2,000 → 10,000 (fraction of island-runs held)\n')
    L.append('| cell | F_P | core | nice | CB set | open | identity | ten EQ | XC (F_X) | XB |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for c in PART1:
        if c not in p1: continue
        s = p1[c]
        L.append('| %s | ' % DESC[c] + ' | '.join('%s → %s' % (fmt(s['2000']['held'][f], 2), fmt(s['10000']['held'][f], 2)) for f in PO.FAMS) +
                 ' | %s → %s |' % (fmt(s['2000']['held_XB'], 3), fmt(s['10000']['held_XB'], 3)))
    L.append('\n### Cross-island P(C,C) at 2,000 → 10,000 (overall; among readers; over island pairs both held by F_P, with the number of runs having ≥ 2 such islands at 10,000)\n')
    L.append('| cell | overall | readers | F_P-held island pairs | island P(C,C) @10,000 | E3 success | frozen |')
    L.append('|---|---|---|---|---|---|---|')
    for c in PART1:
        if c not in p1: continue
        s = p1[c]
        L.append('| %s | %s → %s | %s → %s | %s → %s (%d) | %s | %d | %d |' % (DESC[c], fmt(s['2000']['cross']), fmt(s['10000']['cross']),
                 fmt(s['2000']['cross_readers']), fmt(s['10000']['cross_readers']), fmt(s['2000']['cross_FP_islands']),
                 fmt(s['10000']['cross_FP_islands']), s['10000']['n_cross_FP_islands'], fmt(s['10000']['island_pcc']), s['E3_success'], s['frozen']))
    L.append('\n### Stages (pooled over runs; @10,000 unless marked)\n')
    L.append('| cell | family | copies / run | seed islands occupied / run | est. per occupied @2,000 / @10,000 | extinction prob. | median est. gen (q90) | persistence @10,000 | spread / run @10,000 | held / run @10,000 | islands per copy @2,000 / @10,000 |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|')
    fams_of = {'L': ['FP', 'core', 'nice', 'identity'], 'P1': ['FP', 'core', 'nice', 'identity'], 'P2': ['CBset', 'identity'],
               'P3': ['FP', 'core', 'nice'], 'P4': ['FP', 'core', 'nice', 'identity'], "P4'": ['CBset', 'identity'],
               'P5': ['FP', 'EQten', 'identity'], 'P1p': ['core', 'identity'], 'P2n': ['nice', 'identity'], 'P3p': ['core'],
               'P4p': ['core', 'identity'], 'P4n': ['nice', 'identity'], 'P5p': ['core', 'EQten', 'identity']}
    for c in PART1:
        if c not in p1: continue
        for f in fams_of[c]:
            d = p1[c]['stages'][f]
            L.append('| %s | %s | %s | %s | %s / %s | %s | %s (%s) | %s | %s | %s | %s / %s |' % (
                c, f, fmt(d['n0_per_run'], 1), fmt(d['occupied_per_run'], 1), fmt(d['2000']['est_per_occupied']), fmt(d['10000']['est_per_occupied']),
                fmt(d['10000']['extinct_prob']), fmt(d['est_time_median'], 0), fmt(d['est_time_q90'], 0), fmt(d['10000']['persistence']),
                fmt(d['10000']['spread_per_run'], 1), fmt(d['10000']['held_per_run'], 1), fmt(d['2000']['islands_per_copy']), fmt(d['10000']['islands_per_copy'])))
    L.append('\n### Largest-established-set predictor and tracked classes\n')
    L.append('| cell | decided @2,000 / @10,000 | largest-established won | largest-seeded won | XB seeded (runs) / alive at first separation / ever held | CBP seeded / ever held |')
    L.append('|---|---|---|---|---|---|')
    for c in PART1:
        if c not in p1: continue
        s = p1[c]; pl = s['pooling']; tr = s['track']
        L.append('| %s | %d / %d | %d / %d | %d / %d | %d / %d / %d | %d / %d |' % (DESC[c], pl['2000']['decided'], pl['10000']['decided'],
                 pl['2000']['best_est_won'], pl['10000']['best_est_won'], pl['2000']['best_seed_won'], pl['10000']['best_seed_won'],
                 tr['XB']['seeded_runs'], tr['XB']['alive_at_first_sep'], tr['XB']['ever_held_runs'], tr['CBP']['seeded_runs'], tr['CBP']['ever_held_runs']))
    sc = S.get('scan')
    if sc:
        L.append('\n### The identity abundance scan (universal-open runs of 40 at 2,000 / 10,000; A = without F_P at M, B = with F_P at M)\n')
        for pre in ('scanA', 'scanB'):
            if pre not in sc: continue
            d = sc[pre]
            L.append('\n**%s**%s\n' % (pre, ' (refinement points: %s)' % ', '.join(d['refined']) if d['refined'] else ''))
            L.append('| m | copies / run | universal-open @2,000 | @10,000 | F_P-universal @10,000 | identity islands @10,000 | identity islands per run @10,000 | cross P(C,C) @10,000 | identity est. per occupied seed island |')
            L.append('|---|---|---|---|---|---|---|---|---|')
            for i, m in enumerate(d['ms']):
                L.append('| %s | %.1f | %d | %d | %d | %s | %s | %s | %s |' % ('%.3g' % m, d['copies'][i], d['2000']['k'][i], d['10000']['k'][i], d['univ_FP']['10000'][i],
                         fmt(d['identity_islands']['10000'][i]), fmt(d['identity_held_per_run']['10000'][i], 1), fmt(d['cross']['10000'][i]),
                         fmt(d['identity_est_per_occupied']['10000'][i])))
        L.append('\n**Crossings** (50% of runs universal-open; paired bootstrap 95% interval; fraction of resamples at a scan boundary):\n')
        for pre in ('scanA', 'scanB'):
            for T in ('2000', '10000'):
                if T in sc.get(pre, {}):
                    d = sc[pre][T]
                    L.append('- %s @%s: m* = %s [%s, %s] (%s; boundary %.2f; on the eight preregistered points %s); copies per run %.1f; fit f = e^(−6400 m q) on m ≤ 10⁻³: q = %.4f, residuals %s; fit f = f₀ e^(−6400 m q): f₀ = %.3f, q = %.4f, residuals %s' % (
                        pre, T, '%.3g' % d['crossing'], '%.3g' % d['lo'], '%.3g' % d['hi'], d['flag'], d['boundary_frac'], '%.3g' % d['crossing_unrefined'],
                        6400 * d['crossing'], d['fit1']['q'], [round(x, 2) for x in d['res1']], d['fit2']['f0'], d['fit2']['q'], [round(x, 2) for x in d['res2']]))
        if 'shift_10000' in sc:
            L.append('- shift factor m*_B / m*_A @10,000 = %.2f (unrefined %.2f), paired bootstrap [%.2f, %.2f]' % (sc['shift_10000'], sc['shift_10000_unrefined'], *sc['shift_10000_ci']))
    pn = S.get('panel')
    if pn:
        L.append('\n### Scaling panel (universal-open fraction at the two bracketing scan points)\n')
        L.append('| (N, I) | m points | universal-open @2,000 | universal-open @10,000 | identity islands @10,000 | m* @10,000 (flag) | copies per run N·I·m* |')
        L.append('|---|---|---|---|---|---|---|')
        for ni, d in sorted(pn.items()):
            e = d['10000']
            L.append('| (%s) | %s | %s | %s | %s | %.3g (%s) | %.1f |' % (ni, e['ms'], d['2000']['k'], e['k'], [round(x, 3) for x in e['identity_islands']],
                     e['crossing'], e['flag'], e['copies_at_crossing']))
    return '\n'.join(L)


def main():
    rows = load('lottery_main.json')
    cells = by_cell(rows)
    S = dict(part1={c: cell_summary(cells[c]) for c in PART1 if c in cells})
    st = json.load(open(os.path.join(OUT, 'static.json')))
    if any(c.startswith('scan') for c in cells):
        S['scan'] = scan_summary(cells, st['m_L'])
    prow = load('lottery_panel.json')
    if prow:
        pc = by_cell(prow)
        pts = sorted({c.split('@')[0] for c in pc}, key=lambda b: int(b.split('_')[1]))
        S['panel'] = panel_summary(pc, cells, pts)
        S['panel_cells'] = {c: cell_summary(v) for c, v in pc.items()}
    ch = load('chain.json')
    if ch:
        S['chain'] = ch
    S['scan_cells'] = {c: {T: dict(outcomes=v[T]['outcomes'], univ=v[T]['univ'], held=v[T]['held']) for T in CK}
                       for c, v in ((c, cell_summary(cells[c])) for c in cells if c.startswith('scan'))}
    json.dump(S, open(os.path.join(ROOT, 'runs', 'prudent-openness.json'), 'w'), indent=1, default=str)
    open(os.path.join(OUT, 'tables.md'), 'w').write(tables(S))
    print(tables(S))


if __name__ == '__main__':
    main()
