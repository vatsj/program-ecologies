"""Scoring of predictions 1-6 and the report writer for the migration-window experiment.

    python3 src/migration_window_score.py     # -> runs/migration-window.json, runs/migration-window.md, runs/migration_window/*.json
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migration_window_run as R
import migration_window_report as P
import migration_window as MW

ROOT = P.ROOT
MNS = R.MNS
H = P.H


def mcell(g, N, m):
    return 'M-%s-N%d-m%s' % (g, N, R.mlab(m))


RECS = {}
STATS = {}


def recs(cell):
    if cell not in RECS:
        RECS[cell] = P.load(cell)
    return RECS[cell]


def stats(cell, prefix=None):
    key = (cell, prefix)
    if key not in STATS:
        rs = recs(cell)
        if prefix:
            rs = [r[prefix] for r in rs]
        STATS[key] = P.cellstats(rs) if rs else None
    return STATS[key]


def sh(cell, g=10000, k='ts', prefix=None):
    s = stats(cell, prefix)
    if s is None or s['snap'].get(str(g)) is None:
        return None
    return s['snap'][str(g)][k]


def shv(cell, g=10000, k='ts', prefix=None):
    x = sh(cell, g, k, prefix)
    return None if x is None else x[0]


def arr(cell, g=10000, k='ts', prefix=None):
    rs = recs(cell)
    if prefix:
        rs = [r[prefix] for r in rs]
    return [r['snap'][str(g)][k] for r in rs]


def f2(x, nd=2):
    return 'n/a' if x is None else ('%.' + str(nd) + 'f') % x


def fci(t, nd=2):
    if t is None:
        return 'n/a'
    return '%s [%s, %s]' % (f2(t[0], nd), f2(t[1], nd), f2(t[2], nd))


def fmed(t):
    if t is None:
        return 'n/a'
    m, lo, hi = t
    if np.isnan(m):
        return '>%d' % H
    return '%d [%s, %s]' % (m, 'n/a' if np.isnan(lo) else '%d' % lo, 'n/a' if np.isnan(hi) else '%d' % hi)


# ---------------------------------------------------------------------- panel tables
def panel_table(g, N):
    rows = []
    hdr = ('| mN | runs | target %s | | | | | V* @10k | hp @10k | islands F/U/G/W/D @10k | wasteful runs @10k | KM waste cleared | KM coverage lost'
           ' | mean gens in target | ever in target |'
           % '(as stated) @1k, 2k, 5k, 10k, 20k')
    out = ['| mN | runs | ts@1k | ts@2k | ts@5k | ts@10k | ts@20k | V*@10k | hp@10k | F/U/G/W/D @10k | KM clear | KM lost | gens in target | ever |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for m in MNS:
        c = mcell(g, N, m)
        s = stats(c)
        if s is None:
            continue
        sn = s['snap']
        def one(gg, k='ts'):
            x = sn.get(str(gg))
            return 'n/a' if x is None else fci(x[k])
        x10 = sn['10000']
        isl = '/'.join('%.2f' % x10['isl_' + k] for k in 'FUGWD')
        ps = s['pass']
        out.append('| %s | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %.0f | %.2f |' % (
            R.mlab(m), s['n'], one(1000), one(2000), one(5000), one(10000), one(20000), one(10000, 'tv'),
            one(10000, 'hps'), isl, fmed(ps['clear']), fmed(ps['lost']), s['ep_ts']['cum_mean'], s['ep_ts']['ever']))
    return '\n'.join(out)


# ---------------------------------------------------------------------- predictions
def p1():
    best = None; rows = {}
    for m in MNS:
        v = shv(mcell('base', 100, m))
        if v is not None:
            rows[R.mlab(m)] = v
            if best is None or v > best[1]:
                best = (m, v)
    verdict = 'held' if best[1] >= 0.5 else ('failed' if best[1] < 0.25 else 'partial')
    # plateau width: the mN range with share >= 0.5 at 10,000 and at 20,000
    w10 = [R.mlab(m) for m in MNS if (shv(mcell('base', 100, m)) or 0) >= 0.5]
    w20 = [R.mlab(m) for m in MNS if (shv(mcell('base', 100, m), 20000) or 0) >= 0.5]
    return dict(verdict=verdict, best_mN=best[0], best_share=best[1], shares_10000=rows, mN_with_share_ge_half_10000=w10,
                mN_with_share_ge_half_20000=w20)


def loglog(xs, ys):
    xs = np.log(np.array(xs, float)); ys = np.log(np.array(ys, float))
    if len(xs) < 2:
        return None
    return float(np.polyfit(xs, ys, 1)[0])


def p2():
    clear = {}; lost = {}
    for m in MNS:
        if m == 0:
            continue
        s = stats(mcell('base', 100, m))
        if s is None:
            continue
        c = s['pass']['clear'][0]; l = s['pass']['lost'][0]
        clear[m] = None if np.isnan(c) else c
        lost[m] = None if np.isnan(l) else l
    uc = {m: v for m, v in clear.items() if v}
    ul = {m: v for m, v in lost.items() if v}
    sl_c = loglog(list(uc), list(uc.values()))
    sl_l = loglog(list(ul), list(ul.values()))
    r3 = [m for m in (0.03, 0.1, 0.3)]
    sl_c3 = loglog([m for m in r3 if m in uc], [uc[m] for m in r3 if m in uc])
    sl_l3 = loglog([m for m in r3 if m in ul], [ul[m] for m in r3 if m in ul])
    ratios = {R.mlab(m): ul[m] / uc[m] for m in uc if m in ul}
    lost_before = [R.mlab(m) for m in uc if m in ul and ul[m] < uc[m]]
    verdict = 'not scorable'
    if sl_c is not None and sl_l is not None:
        ok_slope = all(-1.3 <= s <= -0.7 for s in (sl_c, sl_l))
        far = any(s < -1.6 or s > -0.4 for s in (sl_c, sl_l))
        ok_ratio = ratios and all(v >= 5 for v in ratios.values())
        if ok_slope and ok_ratio and not lost_before:
            verdict = 'held'
        elif far or lost_before:
            verdict = 'failed'
        else:
            verdict = 'partial'
    # gemini: ratio < 5 with a majority of member exits to unequal pairs
    tr = {}
    for m in MNS:
        if m == 0:
            continue
        s = stats(mcell('base', 100, m))
        if s is None:
            continue
        t = s['trans']
        tr[R.mlab(m)] = dict(F_to_U=t.get('F>U', 0), Fk_to_Fj=t.get('Fk>Fj', 0), F_to_other=sum(v for k, v in t.items()
                             if k.startswith('F>') and ':' not in k and k != 'F>U'), U_to_F=t.get('U>F', 0))
    gem = {m: (v['F_to_U'] > v['Fk_to_Fj']) for m, v in tr.items()}
    resc = {R.mlab(m): (v * m) for m, v in ul.items()}
    return dict(verdict=verdict, clear_median=clear, lost_median=lost, slope_clear=sl_c, slope_lost=sl_l,
                slope_clear_003_03=sl_c3, slope_lost_003_03=sl_l3, ratio_lost_over_clear=ratios,
                lost_before_clear=lost_before, transitions_from_member=tr,
                gemini_unequal_dominates_member_exits=gem, rescaled_lost_median_x_mN=resc)


def p3():
    out = {}
    for N in (100, 200):
        best = None
        for m in MNS:
            v = shv(mcell('base', N, m))
            if v is not None and (best is None or v > best[1]):
                best = (m, v)
        out['best_N%d' % N] = best
    # unpaired difference at each N's best mN, and at the best-100 mN
    res = {}
    if out['best_N100'] and out['best_N200']:
        m1, m2 = out['best_N100'][0], out['best_N200'][0]
        d = P.boot_diff(arr(mcell('base', 200, m2)), arr(mcell('base', 100, m1)), paired=False)
        res['best_vs_best'] = d
        tvs = {}
        for N in (100, 200):
            tvs[N] = max((shv(mcell('base', N, m), 10000, 'tv') or 0) for m in MNS)
        res['best_tv'] = tvs
        res['byN_same_mN'] = {R.mlab(m): (shv(mcell('base', 100, m)), shv(mcell('base', 200, m))) for m in MNS}
        if d[0] < 0:
            verdict = 'held' if d[2] < 0 else 'partial (point estimate lower, interval contains 0)'
        else:
            verdict = 'failed'
        res['verdict'] = verdict
    out.update(res)
    return out


def p4():
    out = {'by_mN': {}}
    diffs = {}
    for m in MNS:
        cb, cg = mcell('base', 100, m), mcell('gKR', 100, m)
        if not recs(cb) or not recs(cg):
            continue
        d = P.boot_diff(arr(cg), arr(cb), paired=True)
        diffs[m] = d
        out['by_mN'][R.mlab(m)] = dict(base=shv(cb), guard=shv(cg), diff=d,
                                       guard_tv=shv(cg, 10000, 'tv'), base_tv=shv(cb, 10000, 'tv'))
    if not diffs:
        return dict(verdict='not run')
    gbest = max(diffs, key=lambda m: shv(mcell('gKR', 100, m)))
    gain_best = diffs[gbest]
    pos = {m: d for m, d in diffs.items() if m > 0}
    gbest_pos = max(pos, key=lambda m: shv(mcell('gKR', 100, m))) if pos else None
    first = all(d[0] >= 0 for d in diffs.values())
    second = gain_best[0] >= 0.2
    if gain_best[0] < 0:
        verdict = 'failed'
    elif first and second:
        verdict = 'held'
    else:
        verdict = 'partial'
    out.update(guard_best_mN=gbest, gain_at_guard_best=gain_best,
               guard_best_mN_positive=gbest_pos, gain_at_best_positive=pos[gbest_pos] if gbest_pos is not None else None,
               first_clause_all_mN=first, second_clause=second,
               mN_where_guard_below_base=[R.mlab(m) for m, d in diffs.items() if d[0] < 0],
               gemini=dict(le_at_01_03=all(diffs[m][0] <= 0 for m in (0.1, 0.3) if m in diffs),
                           gt_at_low=all(diffs[m][0] > 0 for m in (0, 0.003, 0.01, 0.03) if m in diffs and
                                         (shv(mcell('base', 100, m)) or 0) < 1.0)),
               verdict=verdict)
    return out


def p5():
    out = {'by_mN': {}}
    ok = True; below = False
    for m in MNS:
        c = mcell('gV', 100, m)
        if not recs(c):
            continue
        v = shv(c)
        nm3 = stats(c)['snap']['10000']['nm3']
        mocc = stats(c)['snap']['10000']['isl_F']
        out['by_mN'][R.mlab(m)] = dict(share=sh(c), tv=shv(c, 10000, 'tv'), three_members=nm3, modal_fair_islands=mocc)
        if m >= 0.01:
            if v < 0.9:
                ok = False
            if v < 0.7:
                below = True
    out['verdict'] = 'failed' if below else ('held' if ok else 'partial')
    return out


def p6():
    out = {}
    ref = {C: MW.p_all_three(C) for C in (1, 2, 4, 8)}
    out['reference'] = ref
    for N in (100, 200):
        c = 'C16-base-N%d-m1' % N
        if not recs(c):
            continue
        row = {}
        for C in (1, 2, 4, 8):
            row[C] = dict(ts=sh(c, 10000, 'ts', 'C%d' % C), tv=sh(c, 10000, 'tv', 'C%d' % C), ts20=sh(c, 20000, 'ts', 'C%d' % C))
        out['N%d' % N] = row
    # size panel
    sz = {}
    for k, c in (('4x4', 'Z4-base-N100-m1'), ('4x16', 'C16-base-N100-m1'), ('4x64', 'Z64-base-N100-m1')):
        if recs(c):
            pre = 'C4' if k == '4x16' else None
            sz[k] = dict(ts=sh(c, 10000, 'ts', pre), tv=sh(c, 10000, 'tv', pre))
    out['size_panel_N100_m1'] = sz
    # components' outcome distributions (for the mechanism evidence)
    comp = {}
    for k, c, pre in (('4x4', 'Z4-base-N100-m1', None), ('4x16', 'C16-base-N100-m1', 'C4'), ('4x64', 'Z64-base-N100-m1', None)):
        if not recs(c):
            continue
        rs = recs(c)
        cs = []
        for r in rs:
            rr = r[pre] if pre else r
            cs.extend(rr['comps'])
        n = len(cs)
        def cls_of(c_):
            o = c_['out10000']
            if o < 0:
                return 'mixed'
            return MW.OLAB[o][0]
        cnt = {}
        for c_ in cs:
            cnt[cls_of(c_)] = cnt.get(cls_of(c_), 0) + 1
        comp[k] = {a: b / n for a, b in cnt.items()}
    out['component_outcomes_10000'] = comp
    # verdict
    v = {}
    if 'N100' in out:
        r = out['N100']
        pts = [r[C]['ts'][0] for C in (1, 2, 4, 8)]
        rises = all(pts[i] <= pts[i + 1] for i in range(3)) and pts[3] > pts[0]
        w4 = abs(pts[2] - ref[4]) <= 0.15; w8 = abs(pts[3] - ref[8]) <= 0.15
        below8 = (ref[8] - pts[3]) > 0.15
        v['N100'] = dict(rises=rises, within_0_15_at_C4=w4, within_0_15_at_C8=w8, below_by_more_at_C8=below8,
                         verdict='held' if rises and w4 and w8 else ('failed' if below8 else 'partial'))
    if 'N200' in out:
        r = out['N200']
        pts = {C: r[C]['ts'][0] for C in (4, 8)}
        v['N200'] = dict(below_ref_C4=pts[4] < ref[4], below_ref_C8=pts[8] < ref[8],
                         verdict='held' if pts[4] < ref[4] and pts[8] < ref[8] else
                         ('failed' if pts[4] >= ref[4] and pts[8] >= ref[8] else 'partial'))
    if '4x4' in sz and '4x64' in sz:
        d = sz['4x4']['ts'][0] - sz['4x64']['ts'][0]
        v['size'] = dict(diff_4x4_minus_4x64=d, verdict='held' if d > 0 else 'failed')
    out['verdicts'] = v
    return out


def controls():
    out = {}
    for st in ('bal', 'waste'):
        for g in ('base', 'gKR', 'gV'):
            for m in (0.01, 0.1, 1):
                c = 'K%s-%s-N100-m%s' % (st, g, R.mlab(m))
                s = stats(c)
                if s is None:
                    continue
                out[c] = dict(n=s['n'], ts={k: s['snap'][k]['ts'] if s['snap'].get(k) else None for k in ('1000', '2000', '5000', '10000', '20000')},
                              tv10=s['snap']['10000']['tv'], isl={k: s['snap']['10000']['isl_' + k] for k in 'FUGWD'},
                              clear=s['pass']['clear'], lost=s['pass']['lost'], never_est=s['pass']['never_established'])
    return out


def rs_target():
    """configurations meeting the RS's target: target (as stated) in >= 0.9 of runs at 10,000 and at 20,000."""
    meet = []; near = []
    for c in R.CELLS:
        if not recs(c) or c.startswith('VER'):
            continue
        pres = [None] if R.CELLS[c].get('kind') != 'C' else ['C1', 'C2', 'C4', 'C8']
        for pre in pres:
            s = stats(c, pre)
            if s is None:
                continue
            a = s['snap'].get('10000'); b = s['snap'].get('20000')
            if not a or not b:
                continue
            name = c + ('' if pre is None else '/' + pre)
            row = dict(cell=name, ts10=a['ts'][0], ts20=b['ts'][0], tv10=a['tv'][0], tv20=b['tv'][0], hps10=a['hps'][0], hpv10=a['hpv'][0])
            if row['ts10'] >= 0.9 and row['ts20'] >= 0.9:
                meet.append(row)
            elif row['ts10'] >= 0.75:
                near.append(row)
    return dict(meets=meet, near=near)


# ---------------------------------------------------------------------- compact per-cell files
def write_compact():
    os.makedirs(P.OUT + '/migration_window', exist_ok=True)
    for c in R.CELLS:
        rs = recs(c)
        if not rs:
            continue
        cols = []
        for r in rs:
            def one(rr):
                sn = rr['snap']
                d = dict(tc=rr['t_clear'], ge=rr['g_est'], tl=rr['t_lost'], lw=rr['last_waste'],
                         st=rr['status'], sp=rr['stop'], nm=rr['nmig'], ini=rr['mean_inef'])
                for k in ('ts', 'tv', 'hps', 'hpv'):
                    e = rr['ep_' + k]
                    d['ep_' + k] = [e['first'], e['n'], e['n25'], e['cum'], e['longest'], e['final']]
                d['snap'] = {g: [sn[g][k] for k in ('ts', 'tv', 'hps', 'hpv', 'nm', 'F', 'U', 'G', 'W', 'D', 'cons')] + [sn[g]['inef']]
                             for g in sn if g in ('1000', '2000', '5000', '10000', '20000')}
                if 'comps' in rr and len(rr['comps']) > 1:
                    d['comps'] = [[cc.get('out10000'), cc.get('pres10000'), cc.get('cons_first')] for cc in rr['comps']]
                return d
            if 'C1' in r:
                x = {k: one(r[k]) for k in ('C1', 'C2', 'C4', 'C8')}
                x['run'] = r['run']
            else:
                x = one(r); x['run'] = r['run']
            cols.append(x)
        json.dump(dict(cell=c, params=R.CELLS[c], snap_fields=['ts', 'tv', 'hps', 'hpv', 'nm', 'F', 'U', 'G', 'W', 'D', 'cons', 'inef'],
                       runs=cols), open(P.OUT + '/migration_window/%s.json' % c, 'w'), separators=(',', ':'))


# ---------------------------------------------------------------------- the report
def comp_table(N, g='base'):
    out = ['| C (16-island components) | islands | reference | target (as stated) @10k | V* @10k | ts @20k | hp @10k | KM coverage lost | consensus @10k |',
           '|---|---|---|---|---|---|---|---|---|']
    c = 'C16-%s-N%d-m1' % (g, N)
    if not recs(c):
        return '(not run)'
    for C in (1, 2, 4, 8):
        s = stats(c, 'C%d' % C)
        sn = s['snap']['10000']
        out.append('| %d | %d | %.3f | %s | %s | %s | %s | %s | %.2f |' % (
            C, 16 * C, MW.p_all_three(C), fci(sn['ts']), fci(sn['tv']), fci(s['snap']['20000']['ts']), fci(sn['hps']),
            fmed(s['pass']['lost']), sn['cons']))
    return '\n'.join(out)


def simple_cell_row(c, pre=None):
    s = stats(c, pre)
    if s is None:
        return None
    sn = s['snap']['10000']
    return '| %s | %d | %s | %s | %s | %s | %s | %s |' % (
        c + ('' if pre is None else '/' + pre), s['n'], fci(sn['ts']), fci(sn['tv']), fci(s['snap']['20000']['ts']),
        '/'.join('%.2f' % sn['isl_' + k] for k in 'FUGWD'), fmed(s['pass']['clear']), fmed(s['pass']['lost']))


def main():
    res = {}
    res['verify'] = P.verify()
    res['P1'] = p1(); res['P2'] = p2(); res['P3'] = p3(); res['P4'] = p4(); res['P5'] = p5(); res['P6'] = p6()
    res['controls'] = controls()
    res['rs_target'] = rs_target()
    expo = {}
    for g in ('base', 'gKR', 'gV'):
        for N in (100, 200):
            for m in MNS:
                s = stats(mcell(g, N, m))
                if s is not None and s['migrant_exposure'] is not None:
                    expo['%s-N%d-m%s' % (g, N, R.mlab(m))] = dict(per_slot_per_gen=s['migrant_exposure'] , mN=m, n=s['n_full_horizon'])
    res['migrant_exposure'] = expo
    # compact numbers for the json
    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items() if k not in ('arr', 'clear_raw', 'lost_raw')}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, float) and np.isnan(o):
            return None
        return o
    cells = {}
    for c in R.CELLS:
        if recs(c):
            if R.CELLS[c].get('kind') == 'C':
                cells[c] = {pre: clean(stats(c, pre)) for pre in ('C1', 'C2', 'C4', 'C8')}
            else:
                cells[c] = clean(stats(c))
    res['cells'] = cells
    json.dump(clean(res), open(os.path.join(ROOT, 'runs', 'migration-window.json'), 'w'), indent=None, separators=(',', ':'))
    write_compact()
    write_md(res)


def write_md(res):
    L = []
    A = L.append
    A('# A migration window for stable sets on islands: run report (2026-10-24)')
    A('')
    A('Spec `specs/2026-10-24-migration-window.md`; notes `notes/migration-window.md`; predictions '
      '`predictions/2026-10-24-migration-window.md`. Code `src/migration_window*.py`, tests `tests/test_migration_window.py`. '
      'Per-cell compact records in `runs/migration_window/`, all aggregates in `runs/migration-window.json`.')
    A('')
    A('## 1. Re-verification of the stored cells (before any counted cell)')
    A('')
    A('Rerun of the stored founders and kernel seeds at the stored horizon (10,000) through the generated kernels; compared with the stored per-run records.')
    A('')
    A('| cell | runs | same status/stop/migrants/events | same modal outcome counts | same occupancy | same consensus flag | same coverage flag |')
    A('|---|---|---|---|---|---|---|')
    for c, v in res['verify'].items():
        A('| %s | %d | %d | %s | %d | %d | %s |' % (c, v['n'], v['same_status_stop_nmig_nev'],
                                                v['same_modal_labels'] if v['same_modal_labels'] is not None else 'n/a',
                                                v['same_occupancy'], v['same_consensus'],
                                                v['same_coverage'] if v['same_coverage'] is not None else 'n/a'))
    gv = res['verify'].get('VER-gV-N100-m1')
    if gv:
        A('')
        A('Stored gV (R2) cell at mN = 1, re-derived from the rerun: consensus in %d of 40 runs, all three members in %d of 40, modal occupancy %.3f, target (as stated) %.3f, target (V*) %.3f at generation 10,000.' % (
            gv['consensus_runs'], gv['all_three_runs'], gv['modal_occupancy'], gv['target_ts'], gv['target_tv']))
    A('')
    A('## 2. Migration panels (one connected component of 64 islands)')
    for g, nm in (('base', 'baseline (no contracts)'), ('gKR', 'U-gKR(0.99)'), ('gV', 'gV (hand-written veto)')):
        for N in (100, 200):
            if not recs(mcell(g, N, 0)) and not recs(mcell(g, N, 1)):
                continue
            A('')
            A('### %s, N = %d' % (nm, N))
            A('')
            A(panel_table(g, N))
    A('')
    A('Columns: ts = target (as stated), V* = target (V*), hp = high-purity target (as stated); share of runs with 95% intervals (run-clustered bootstrap); F/U/G/W/D = mean island shares of fair / unequal / grand / wasteful / disagreement modal outcomes at 10,000; KM = Kaplan-Meier median (generations; ">20000" = curve above 0.5 at the horizon) with bootstrap interval; gens in target = mean cumulative generations with the per-generation target indicator true; ever = share of runs that ever enter the target.')
    A('')
    A('## 3. Predictions')
    for k in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6'):
        A('')
        A('### %s' % k)
        A('')
        A('```')
        A(json.dumps(res[k], indent=1, default=str)[:6000])
        A('```')
    A('')
    A('## 4. Components')
    for N in (100, 200):
        A('')
        A('### Baseline, N = %d, mN = 1, components of 16 islands' % N)
        A('')
        A(comp_table(N))
    for g in ('gKR',):
        for N in (100, 200):
            c = 'C16-%s-N%d-m1' % (g, N)
            if recs(c):
                A('')
                A('### U-gKR(0.99), N = %d, mN = 1, components of 16 islands' % N)
                A('')
                A(comp_table(N, g))
    A('')
    A('### Other component cells (target as stated, V*, 20k, island shares, KM)')
    A('')
    A('| cell | runs | ts@10k | V*@10k | ts@20k | F/U/G/W/D | KM clear | KM lost |')
    A('|---|---|---|---|---|---|---|---|')
    for c in R.CELLS:
        if R.CELLS[c].get('kind') in ('C', 'Z') and recs(c):
            pres = ['C1', 'C2', 'C4', 'C8'] if R.CELLS[c]['kind'] == 'C' else [None]
            for pre in pres:
                row = simple_cell_row(c, pre)
                if row:
                    A(row)
    A('')
    A('## 5. Controls (60 islands, one component)')
    A('')
    A('| cell | runs | ts@10k | V*@10k | ts@20k | F/U/G/W/D | KM clear | KM lost |')
    A('|---|---|---|---|---|---|---|---|')
    for c in R.CELLS:
        if R.CELLS[c].get('kind') == 'K' and recs(c):
            row = simple_cell_row(c)
            if row:
                A(row)
    A('')
    A('## 6. Configurations meeting the RS target (target as stated in >= 0.9 of runs at 10,000 and at 20,000)')
    A('')
    A('| cell | ts@10k | ts@20k | V*@10k | V*@20k | hp@10k | hpV*@10k |')
    A('|---|---|---|---|---|---|---|')
    for row in res['rs_target']['meets']:
        A('| %(cell)s | %(ts10).2f | %(ts20).2f | %(tv10).2f | %(tv20).2f | %(hps10).2f | %(hpv10).2f |' % row)
    A('')
    A('Near misses (ts@10k >= 0.75, not both >= 0.9):')
    A('')
    for row in res['rs_target']['near']:
        A('- %(cell)s: ts@10k %(ts10).2f, ts@20k %(ts20).2f, V* %(tv10).2f' % row)
    A('')
    A('## 7. Realized migrant exposure (runs lasting the full horizon): migrant births per slot-population per generation')
    A('')
    for k, v in res['migrant_exposure'].items():
        A('- %s: %.4f (mN = %g; %d runs)' % (k, v['per_slot_per_gen'], v['mN'], v['n']))
    open(os.path.join(ROOT, 'runs', 'migration-window.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
