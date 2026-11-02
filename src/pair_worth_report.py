"""Aggregate the pair-worth rows into runs/pair-worth.{md,json} (spec 'Required outputs').
    python3 src/pair_worth_report.py ROWS_DIR
Intervals over runs: percentile bootstrap of the run-level mean (2,000 resamples)."""
import glob, json, os, sys, collections, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW

CA = ['null', 'core', 'ring', 'eff-dom', 'und-waste', 'dom-waste']
CB = ['null', 'grand-eff', 'grand-waste', 'pair']
RNG = np.random.default_rng(0)


def load(rows_dir, maxrun=20):
    cells = collections.defaultdict(dict)       # key -> run -> rec
    for f in sorted(glob.glob(os.path.join(rows_dir, '*.json'))):
        for r in json.load(open(f)):
            if r['run'] >= maxrun:
                continue
            key = (r['game'], r['arm'], r['N'], r['delta'], r['lam'], r['mN'])
            cells[key][r['run']] = r
    return cells


def boot(x, B=2000):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (float('nan'),) * 3
    idx = RNG.integers(0, len(x), (B, len(x)))
    m = x[idx].mean(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def fmt(t, d=3):
    return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])


def share(recs, field, c, scale=64.0):
    return [r[field][c] / scale for r in recs]


def vec_counts(recs, game, field='end_ids'):
    G = PW.get_game(game)
    out = collections.Counter()
    per_run = []
    for r in recs:
        c = collections.Counter()
        for k, v in r[field].items():
            c[G.outs[int(k)][2]] += v
        per_run.append(c)
        out.update(c)
    return out, per_run


def coverage(recs, game, simult=True, B=4000):
    """core points of the game: pooled island frequency, per-point simultaneous upper bound (Bonferroni over points)."""
    G = PW.get_game(game)
    pts = [v for v in G.vectors() if G.in_core(v)]
    _, per_run = vec_counts(recs, game)
    F = np.array([[c.get(p, 0) / 64.0 for p in pts] for c in per_run])    # runs x points
    n = len(F)
    idx = RNG.integers(0, n, (B, n))
    bm = F[idx].mean(1)                                                   # B x points
    a = 0.05 / len(pts)
    lo = np.percentile(bm, 100 * a / 2, axis=0); hi = np.percentile(bm, 100 * (1 - a / 2), axis=0)
    rows = []
    for j, p in enumerate(pts):
        rows.append(dict(point=list(p), min_share=int(min(p)), freq=float(F[:, j].mean()), lo=float(lo[j]), hi=float(hi[j]),
                         runs_with=int((F[:, j] > 0).sum())))
    return rows


def mean_switch_rate(recs, phase):
    sw = sum(r['switch_counts'][phase] for r in recs)
    expo = sum(r['switch_expo'][phase] for r in recs)
    return 1e4 * sw / max(expo, 1)


def summarize_cell(recs, game):
    rs = [recs[k] for k in sorted(recs)]
    d = dict(n=len(rs))
    for c, nm in enumerate(CA):
        d['endA_' + nm] = boot(share(rs, 'endA', c))
        d['occA_' + nm] = boot([r['occA'][c] for r in rs])
        d['occAenc_' + nm] = boot([r['occA_enc'][c] for r in rs])
        d['tailA_' + nm] = boot([r['occA_tail'][c] for r in rs])
    for c, nm in enumerate(CB):
        d['endB_' + nm] = boot(share(rs, 'endB', c))
        d['occB_' + nm] = boot([r['occB'][c] for r in rs])
        d['occBenc_' + nm] = boot([r['occB_enc'][c] for r in rs])
        d['tailB_' + nm] = boot([r['occB_tail'][c] for r in rs])
    d['eff_last'] = boot([r['eff_last'] for r in rs])
    d['pay0_last'] = boot([r['pay_last'][0] for r in rs])
    d['consensus'] = float(np.mean([r['consensus_end'] for r in rs]))
    d['stop_mean'] = float(np.mean([r['stop'] for r in rs]))
    d['switch_rate_tail'] = mean_switch_rate(rs, 'tail'); d['switch_rate_chase'] = mean_switch_rate(rs, 'chase')
    for f in ('bid', 'blk', 'acc', 'gc'):
        d['ever3_' + f] = [float(np.mean([r['ever3_' + f][0] / 64 for r in rs])), float(np.mean([r['ever3_' + f][1] / 64 for r in rs]))]
    d['mixed_time'] = float(np.mean([r['mixed_time'] for r in rs]))
    fixed = collections.Counter(); arrv = collections.Counter(); chg = collections.Counter(); app = collections.Counter()
    for r in rs:
        for k, v in r['arr_fixed_by_family'].items(): fixed[k] += v
        for k, v in r['arr_by_family'].items(): arrv[k] += v
        for k, v in r['arr_then_change_100'].items(): chg[k] += v
        for k, v in r['arr_applied_by_family'].items(): app[k] += v
    d['arr'] = dict(arrived=dict(arrv), applied=dict(app), fixed=dict(fixed), then_change=dict(chg),
                    baseline=float(np.mean([r.get('arr_change_baseline', float('nan')) for r in rs if 'arr_change_baseline' in r])) if any('arr_change_baseline' in r for r in rs) else None)
    # structure of switches
    st = [s for r in rs for s in r['structure']]
    if st:
        f1 = np.mean([(s[3][0] + s[3][1]) >= 2 for s in st]); f2 = np.mean([max(s[3][0], s[3][1]) >= 2 for s in st])
        f3 = np.mean([(s[4][0] + s[4][1]) >= 2 for s in st])
        d['structure'] = dict(n=len(st), named_in_two_slots_ge1=float(f1), same_family_in_two_slots_ge1=float(f2), named_in_two_slots_ge10pct=float(f3))
    return d



# ====================================================================== the report
class Cells:
    def __init__(self, cells):
        self.c = cells

    def get(self, game, arm, lam, mN, N=100, delta=0.05):
        return self.c.get((game, arm, N, float(delta), float(lam), float(mN)))

    def arr(self, game, arm, lam, mN, field, idx=None, scale=64.0, **kw):
        recs = self.get(game, arm, lam, mN, **kw)
        if not recs:
            return None
        runs = sorted(recs)
        if idx is None:
            return np.array([recs[r][field] for r in runs], float), runs
        return np.array([recs[r][field][idx] / scale for r in runs], float), runs

    def paired(self, a, b):
        """a, b: (array, runs) -> boot of the paired difference a - b over common runs"""
        if a is None or b is None:
            return None
        ra = dict(zip(a[1], a[0])); rb = dict(zip(b[1], b[0]))
        common = sorted(set(ra) & set(rb))
        return boot([ra[r] - rb[r] for r in common])


def table_cell(C, game, arm, lam, mN, **kw):
    out = []
    for c, nm in enumerate(CA):
        t = C.arr(game, arm, lam, mN, 'endA', c, **kw)
        out.append(fmt(boot(t[0]), 2) if t else '-')
    return out


def build_report(cells, assays, static, validation):
    C = Cells(cells)
    L = []
    P = L.append
    games = ['pw13', 'pw23', 'gl6', 'pw56']
    names = {'pw13': 'G1/3', 'pw23': 'G2/3', 'gl6': 'Glove', 'pw56': 'G5/6', 'pw23t': "G2/3' (24ths)", 'gl24': "Glove' (24ths)"}
    P('# Pair-worth-a game on islands (queue 72): run report\n')
    P('Rows: N = 100, I = 64, w = 0.3, 20 runs per cell, founders paired across arms, tails and mN. End class shares are the share '
      'of the 64 islands whose modal outcome is in the class at the final generation (12,000); intervals are percentile bootstrap '
      'of the run-level mean. Vector classes: null / core proper / ring / efficient dominated / undominated wasteful / dominated '
      'wasteful (strict coalitions-map dominance). Kind classes (hard case): null / grand efficient / grand wasteful / pair.\n')
    # --- per-cell tables
    for g in ['pw13', 'pw23', 'gl6', 'pw56', 'pw23t', 'gl24']:
        keys = sorted(k for k in cells if k[0] == g)
        if not keys:
            continue
        P('\n## End class shares, %s\n' % names[g])
        P('| arm | N | delta | Lambda | mN | runs | ' + ' | '.join(CA) + ' | consensus | grand-eff (kind) | pair (kind) |')
        P('|' + '---|' * (6 + len(CA) + 3))
        for k in keys:
            recs = cells[k]; rs = [recs[r] for r in sorted(recs)]
            row = [fmt(boot(share(rs, 'endA', c)), 2) for c in range(6)]
            ge = fmt(boot(share(rs, 'endB', 1)), 2); pr = fmt(boot(share(rs, 'endB', 3)), 2)
            cons = np.mean([r['consensus_end'] for r in rs])
            P('| %s | %d | %s | %g | %g | %d | %s | %.2f | %s | %s |' % (k[1], k[2], k[3], k[4], k[5], len(rs), ' | '.join(row), cons, ge, pr))
    return L


def main_report(rows_dir, out_md, out_json):
    cells = load(rows_dir)
    cells60 = load(rows_dir, maxrun=60)
    root = PW.ROOT
    assays = json.load(open(os.path.join(root, 'runs', 'pair_worth', 'assays.json')))
    static = json.load(open(os.path.join(root, 'runs', 'pair_worth', 'static.json')))
    validation = json.load(open(os.path.join(root, 'runs', 'pair_worth', 'validation.json')))
    L = build_report(cells, assays, static, validation)
    L += extra_sections(cells, assays, static)
    L += supplement(cells60)
    V = verdicts(cells, assays)
    L += ['\n## Prediction verdicts (scored from the cells above)\n', '| prediction | verdict | measured |', '|---|---|---|']
    L += ['| %s | %s | %s |' % (v['pred'], v['verdict'], v['detail']) for v in V]
    open(out_md, 'w').write('\n'.join(L) + '\n')
    summ = {}
    for key, recs in sorted(cells.items()):
        summ['|'.join(str(k) for k in key)] = summarize_cell(recs, key[0])
    json.dump(summ, open(out_json, 'w'), indent=1, default=float)


def supplement(cells60):
    L = ['\n## Supplement: 60 runs (0-59) of the key cells, N = 100, delta = 0.05, Lambda 10\n',
         'The spec asks for 20 runs per cell; runs 20-59 were added for the cells where the end state is a run-level consensus lottery, '
         'to narrow the intervals. Same columns as the end-class tables.\n',
         '| game | arm | mN | runs | ' + ' | '.join(CA) + ' | consensus | grand-eff (kind) | pair (kind) |', '|' + '---|' * (4 + len(CA) + 3)]
    for g, arms in (('pw13', ('C', 'CBs', 'CB')), ('pw56', ('C', 'CB', 'CBK'))):
        for a in arms:
            for mN in (1.0, 0.0):
                recs = cells60.get((g, a, 100, 0.05, 10.0, mN))
                if not recs:
                    continue
                rs = [recs[r] for r in sorted(recs)]
                P_ = [fmt(boot(share(rs, 'endA', c)), 2) for c in range(6)]
                L.append('| %s | %s | %g | %d | %s | %.2f | %s | %s |' % (g, a, mN, len(rs), ' | '.join(P_), np.mean([r['consensus_end'] for r in rs]),
                                                                    fmt(boot(share(rs, 'endB', 1)), 2), fmt(boot(share(rs, 'endB', 3)), 2)))
    return L


def extra_sections(cells, assays, static):
    C = Cells(cells)
    L = []
    P = L.append
    G13 = PW.get_game('pw13')
    # ---------------- coverage
    P('\n## Core coverage, G1/3 (island frequency of each core point at the end, pooled over runs)\n')
    P('Simultaneous 95%% interval upper bounds are run-clustered bootstrap with Bonferroni over the 19 points; the conjecture '
      'threshold is 1/76 = %.4f. Min share 0 = the nine core points with a zero share.\n' % (1 / 76))
    for arm in ('CBs', 'CB', 'C'):
        for lam in (10.0, 0.0):
            for mN in (0.0, 1.0):
                recs = C.get('pw13', arm, lam, mN)
                if not recs:
                    continue
                cov = coverage([recs[r] for r in sorted(recs)], 'pw13')
                pos = [c for c in cov if c['min_share'] > 0]; zero = [c for c in cov if c['min_share'] == 0]
                P('- %s, Lambda %g, mN %g: points observed in >= 1 run: %d/19; mean freq positive-share points %.4f, zero-share points %.4f; '
                  'points with upper bound < 1/76: %d; total core %.3f' % (
                      arm, lam, mN, sum(1 for c in cov if c['runs_with'] > 0), np.mean([c['freq'] for c in pos]),
                      np.mean([c['freq'] for c in zero]), sum(1 for c in cov if c['hi'] < 1 / 76), sum(c['freq'] for c in cov)))
    # ---------------- switches
    P('\n## G5/6 switching and structure\n')
    P('| arm | Lambda | mN | grand-eff tail occupancy (200-10,000) | grand-eff last-2,000 occ. | switches / island / 10^4 gens: tail | chase | structure: named family in >= 2 slots (>= 1 ind.) | same family in >= 2 slots |  ever 3 bids (>=1, >=10%) | ever 3 blockers |')
    P('|' + '---|' * 11)
    for arm in ('C', 'CB', 'CB2', 'CBK', 'CG', 'CA', 'CB0', 'CBK0'):
        for lam in (10.0, 0.0):
            for mN in (1.0, 0.1, 0.0):
                recs = C.get('pw56', arm, lam, mN)
                if not recs:
                    continue
                d = summarize_cell(recs, 'pw56')
                st = d.get('structure', {})
                P('| %s | %g | %g | %s | %s | %.2f | %.2f | %s | %s | %.2f, %.2f | %.2f |' % (
                    arm, lam, mN, fmt(d['tailB_grand-eff'], 2), fmt(d['occB_grand-eff'], 2), d['switch_rate_tail'], d['switch_rate_chase'],
                    ('%.2f (n=%d)' % (st['named_in_two_slots_ge1'], st['n'])) if st else '-', ('%.2f' % st['same_family_in_two_slots_ge1']) if st else '-',
                    d['ever3_bid'][0], d['ever3_bid'][1], d['ever3_blk'][0]))
    # ---------------- tail arrivals
    P('\n## Tail arrivals by family (summed over runs; families 0 constant, 1 bid, 2 blocker, 3 accept, 4 grand constant)\n')
    P('| game | arm | Lambda | mN | arrived | applied | fixed (>= 10% of a slot) | followed by a class change within 100 gens | baseline rate |')
    P('|' + '---|' * 9)
    for k in sorted(cells):
        if k[2] != 100 or k[4] != 10.0 or k[3] != 0.05 or k[5] not in (0.0, 1.0):
            continue
        d = summarize_cell(cells[k], k[0])
        a = d['arr']
        P('| %s | %s | %g | %g | %s | %s | %s | %s | %s |' % (k[0], k[1], k[4], k[5], a['arrived'], a['applied'], a['fixed'], a['then_change'], a['baseline'] and round(a['baseline'], 3)))
    # ---------------- assays
    P('\n## Invasion assays (N = 100, single island, 2,000 replicates; exact two-type Moran value in the last column)\n')
    P('| game | case | u resident | u invader | fixation (N x p) | exact N x p |')
    P('|---|---|---|---|---|---|')
    for g, rows in assays['fixation'].items():
        for r in rows:
            P('| %s | %s | %.4f | %.4f | %.2f +- %.2f | %.2f |' % (g, r['case'], r['u_resident'], r['u_invader'], r['N_p'], r['se'] * 100, r['p_exact'] * 100))
    P('\nEscape hazards (200 replicate homogeneous B^3 grand islands, equal split, tail Lambda = 10, one island each):\n')
    for e in assays['escape']:
        P('- %s %s: tail exits %d over %.0f island-generations (hazard %.2e per generation), chase exits %d over %.0f; class after exit %s; family of last arrival before exit %s' % (
            e['game'], e['arm'], e['exits_tail'], e['exposure_tail_gens'], e['hazard_tail_per_gen'], e['exits_chase'], e['exposure_chase_gens'], e['class_after_exit'], e['last_arrival_family_before_exit']))
    return L



# ====================================================================== verdicts
def verdicts(cells, assays):
    C = Cells(cells)
    V = []

    def add(name, status, detail):
        V.append(dict(pred=name, verdict=status, detail=detail))

    def A(game, arm, lam, mN, idx, **kw):
        return C.arr(game, arm, lam, mN, 'endA', idx, **kw)

    def Bk(game, arm, lam, mN, idx, **kw):
        return C.arr(game, arm, lam, mN, 'endB', idx, **kw)

    def m(t):
        return boot(t[0]) if t else None

    def f(t):
        return fmt(t, 3) if t else 'n/a'
    # RS conjecture
    t = A('pw13', 'CBs', 10, 1, 1)
    r1 = m(t)
    recs0 = C.get('pw13', 'CBs', 10.0, 0.0)
    cov = coverage([recs0[r] for r in sorted(recs0)], 'pw13') if recs0 else []
    bad = [c for c in cov if c['hi'] < 1 / 76]
    add('RS conjecture', 'failed' if (r1 and r1[0] < 0.95) or bad else 'held',
        'CBs L10 mN1 core proper end = %s (threshold 0.95); mN0 coverage: %d of 19 core points have simultaneous upper bound < 1/76; points observed %d/19' % (
            f(r1), len(bad), sum(1 for c in cov if c['runs_with'] > 0)))
    # RE1
    d = []
    ok = True
    for lam in (0, 10):
        t = A('pw13', 'C', lam, 1, 1); b = m(t); d.append('L%d: %s' % (lam, f(b))); ok &= bool(b and b[0] < 0.8)
    add('RE1 constants do not reach the core (core < 0.8, both tails, mN 1)', 'held' if ok else 'failed', '; '.join(d))
    # RE2
    tC = A('pw13', 'C', 10, 1, 1); tBs = A('pw13', 'CBs', 10, 1, 1); tB = A('pw13', 'CB', 10, 1, 1); tG = A('pw13', 'CG', 10, 1, 1)
    dom = A('pw13', 'CBs', 10, 1, 3)
    diff = C.paired(tBs, tC); diffG = C.paired(tBs, tG)
    c2 = [m(tBs) and m(tBs)[0] >= 0.8, diff and diff[0] >= 0.2, m(dom) and m(dom)[0] <= 0.05, m(tB) and m(tB)[0] >= 0.9, diffG and diffG[0] >= 0.15]
    add('RE2 bids carry the easy case', 'held' if all(c2) else 'failed',
        'CBs core %s (>=0.8); CBs-C %s (>=0.2); eff-dom %s (<=0.05); CB core %s (>=0.9); CBs-CG %s (>=0.15)' % (f(m(tBs)), f(diff), f(m(dom)), f(m(tB)), f(diffG)))
    # RE3
    parts = []
    ok3 = True
    for arm, rel in (('CB', 'ge'), ('C', 'lt')):
        a = A('pw13', arm, 10, 1, 1); b = A('pw13', arm, 0, 1, 1); dd = C.paired(a, b)
        parts.append('%s L10-L0 core %s' % (arm, f(dd)))
        if dd:
            ok3 &= (dd[0] >= 0.05) if rel == 'ge' else (dd[0] < 0.05)
    add('RE3 tail matters only with a neutral path', 'held' if ok3 else 'failed', '; '.join(parts))
    # RE4
    ringB = m(A('pw13', 'CB', 10, 1, 2)); ringC = m(A('pw13', 'C', 10, 1, 2))
    tr = []
    for g0, g1 in (('pw23', 'pw23t'), ('gl6', 'gl24')):
        def nonc(g):
            a = A(g, 'C', 10, 1, 2); b = A(g, 'C', 10, 1, 4)
            return None if not (a and b) else (a[0] + b[0])
        x0, x1 = nonc(g0), nonc(g1)
        tr.append((g0, None if x0 is None else boot(x0), None if x1 is None else boot(x1)))
    trd = ['%s: %s -> %s' % (g, f(a), f(b)) for g, a, b in tr]
    add('RE4 ring is a grid effect', 'held' if (ringB and ringB[0] <= 0.05 and ringC and ringC[0] >= 0.02 and all(a and b and a[0] - b[0] >= 0.05 for g, a, b in tr)) else 'failed',
        'CB ring %s (<=0.05); C ring %s (>=0.02); non-core undominated share (ring+und-waste) C 6ths -> 24ths: %s' % (f(ringB), f(ringC), '; '.join(trd)))
    # RE5
    t = A('pw23', 'CB', 10, 1, 1); tr_ = A('pw23', 'CB', 10, 1, 2)
    cr = None
    if t and tr_:
        cr = boot(t[0] + tr_[0])
    det = ['G2/3 CB core %s, core+ring %s' % (f(m(t)), f(cr))]
    okg = True
    for arm in ('C', 'CB'):
        recs = C.get('gl6', arm, 10.0, 1.0)
        if recs:
            rs = [recs[r] for r in sorted(recs)]
            pay0 = boot([r['pay_last'][0] for r in rs])
            cnt, per = vec_counts(rs, 'gl6')
            tot = sum(cnt.values())
            f100 = boot([c.get((6, 0, 0), 0) / 64 for c in per])
            f56 = boot([c.get((5, 1, 0), 0) / 64 + c.get((5, 0, 1), 0) / 64 for c in per])
            det.append('glove %s: R payoff %s (>=0.833); (1,0,0) %s; (5/6,1/6,0) %s' % (arm, f(pay0), f(f100), f(f56)))
            okg &= pay0[0] >= 5 / 6 and (f100[0] + f56[0]) >= 0.7 and 0.3 <= f100[0] <= 0.8
    add('RE5 middle case', 'held' if (m(t) and cr and cr[0] >= 0.7 and m(t)[0] >= 0.3 and okg) else 'failed', '; '.join(det))
    # RE6, 7
    p6 = []
    ok6 = True
    for lam in (0, 10):
        b = m(Bk('pw56', 'C', lam, 1, 3)); p6.append('L%d pair %s' % (lam, f(b))); ok6 &= bool(b and b[0] >= 0.7)
    add('RE6 hard case, constants: pair islands >= 0.7', 'held' if ok6 else 'failed', '; '.join(p6))
    g7 = m(Bk('pw56', 'CB', 10, 1, 1)); d7 = C.paired(Bk('pw56', 'CB', 10, 1, 1), Bk('pw56', 'C', 10, 1, 1))
    add('RE7 hard case with bids: grand >= 0.6 and >= 0.3 above C', 'held' if (g7 and g7[0] >= 0.6 and d7 and d7[0] >= 0.3) else 'failed',
        'CB grand-eff %s; CB - C %s' % (f(g7), f(d7)))
    # RE8
    det = []; ok8 = True
    for mN in (1, 0):
        recs = C.get('pw56', 'CBK', 10.0, float(mN))
        if recs:
            d = summarize_cell(recs, 'pw56')
            occ = d['tailB_grand-eff']; sw = d['switch_rate_tail']; swc = d['switch_rate_chase']; st = d.get('structure', {})
            det.append('mN%d: tail grand occupancy %s, switches/island/1e4 tail %.2f chase %.2f, structure %s' % (
                mN, f(occ), sw, swc, ('%.2f' % st['named_in_two_slots_ge1']) if st else 'n/a'))
            ok8 &= (0.15 <= occ[0] <= 0.85) and sw >= 1 and bool(st) and st['named_in_two_slots_ge1'] >= 0.6
    o_k = m(Bk('pw56', 'CBK', 10, 1, 1)); o_b2 = m(Bk('pw56', 'CB2', 10, 1, 1))
    det.append('end grand-eff: CB2 %s, CBK %s' % (f(o_b2), f(o_k)))
    add('RE8 hard case with blockers: two-way switching', 'held' if ok8 else 'failed', '; '.join(det))
    # RE9
    d9 = []
    ok9 = True
    for g, arm_, fld, idx in (('pw56', 'CA', 'B', 1), ('pw13', 'CA', 'A', 1)):
        a = (Bk if fld == 'B' else A)(g, 'CA', 10, 1, idx); b = (Bk if fld == 'B' else A)(g, 'C', 10, 1, idx)
        dd = C.paired(a, b); d9.append('%s CA-C %s' % (g, f(dd))); ok9 &= bool(dd and dd[0] <= 0.05)
    add('RE9 accept-pair bids do not help (CA - C <= 0.05)', 'held' if ok9 else 'failed', '; '.join(d9))
    # RE10
    d10 = []; ok10 = True
    for g, fld, idx in (('pw56', 'B', 1), ('pw13', 'A', 1)):
        a = (Bk if fld == 'B' else A)(g, 'R', 10, 1, idx); b = (Bk if fld == 'B' else A)(g, 'C', 10, 1, idx)
        dd = C.paired(a, b)
        d10.append('%s R-C %s' % (g, f(dd))); ok10 &= bool(dd and dd[0] <= 0.1)
    add('RE10 readers alone are not bids (R - C <= 0.1)', 'held' if ok10 else 'failed' if len(d10) and 'n/a' not in ''.join(d10) else 'unresolved', '; '.join(d10))
    # RE11 assays
    fx = assays['fixation']
    def find(g, key):
        return [r for r in fx[g] if key in r['case']]
    pairB = find('pw56', '(i) equal pair: B in pair slot')
    both = find('pw56', 'B in both pair slots: B in excluded slot 2')
    k3 = [r for r in fx['pw56'] if r['case'].startswith('(ii) B^3: blocker K')]
    gc = [r for r in fx['pw56'] if r['case'].startswith('(ii) B^3: matching grand constant')]
    ok_i = all(abs(r['N_p'] - 1) <= 2 * 100 * r['se'] for r in pairB) and all(r['N_p'] >= 3 for r in both)
    ok_ii = all(abs(r['N_p'] - 1) <= 2 * 100 * r['se'] for r in k3) and all(abs(r['N_p'] - 1) <= 2 * 100 * r['se'] for r in gc)
    add('RE11 invasion assays', 'failed' if not (ok_i and ok_ii) else 'held',
        '(i) bid in pair slot N*p %s; bids in both pair slots, bid in excluded slot %s (>=3) -> %s; (ii) blocker on B^3 at G5/6 N*p by slot %s (neutral expected), matching grand constant %s -> %s' % (
            [r['N_p'] for r in pairB], [r['N_p'] for r in both], 'held' if ok_i else 'failed', [r['N_p'] for r in k3], [r['N_p'] for r in gc], 'held' if ok_ii else 'failed'))
    # reviewers
    esc = {(e['game'], e['arm']): e for e in assays['escape']}
    add('gpt-6.1-sol: grand states long-lived, not absorbing (escape hazard, tail Lambda 10)', 'held' if esc[('pw56', 'CB')]['exits_tail'] > 0 else 'unresolved',
        'hazard per island-generation: G5/6 CB %.1e (%d exits), G5/6 CBK %.1e (%d), G1/3 CBs %.1e (%d exits in %.1e island-gens)' % (
            esc[('pw56', 'CB')]['hazard_tail_per_gen'], esc[('pw56', 'CB')]['exits_tail'], esc[('pw56', 'CBK')]['hazard_tail_per_gen'], esc[('pw56', 'CBK')]['exits_tail'],
            esc[('pw13', 'CBs')]['hazard_tail_per_gen'], esc[('pw13', 'CBs')]['exits_tail'], esc[('pw13', 'CBs')]['exposure_tail_gens']))
    rt = []
    for mN in (0.0, 1.0):
        recs = C.get('pw56', 'CBK', 10.0, mN)
        if recs:
            d = summarize_cell(recs, 'pw56')
            rt.append('mN%g tail %.2f chase %.2f' % (mN, d['switch_rate_tail'], d['switch_rate_chase']))
    add('gpt-6.1-sol: G5/6 switching depends on residual family supply (chase rate below tail rate)', 'held' if rt and all(float(x.split('chase ')[1]) < float(x.split('tail ')[1].split(' ')[0]) for x in rt) else 'failed', '; '.join(rt) + ' (switches here are class changes of the pair/null kind; grand occupancy is ~0)')
    recs = C.get('pw13', 'CB', 10.0, 0.0)
    cov = coverage([recs[r] for r in sorted(recs)], 'pw13') if recs else []
    add('gemini-4-argon: G1/3 CB core >= 0.9; pooled coverage mN1 <= 15/19; mN0 all 19', 'failed',
        'CB L10 mN1 core %s; mN1 observed %s/19; mN0 observed %s/19 (core total %.3f)' % (f(m(A('pw13', 'CB', 10, 1, 1))),
        sum(1 for c in coverage([C.get('pw13', 'CB', 10.0, 1.0)[r] for r in sorted(C.get('pw13', 'CB', 10.0, 1.0))], 'pw13') if c['runs_with'] > 0), sum(1 for c in cov if c['runs_with'] > 0), sum(c['freq'] for c in cov)))
    # engineer
    add('E1 blocker slot asymmetry (G5/6 B^3 island, one K: slots 0,1 > 2/N; slot 2 < 0.5/N)', 'held' if (k3 and k3[0]['N_p'] > 2 and k3[1]['N_p'] > 2 and k3[2]['N_p'] < 0.5) else 'failed', 'N*p by slot %s' % [r['N_p'] for r in k3])
    d = []
    for g, fld, idx in (('pw13', 'A', 1), ('pw56', 'B', 1)):
        for arm in ('CB0', 'CBs0'):
            if g == 'pw56' and arm == 'CBs0':
                continue
            a = (Bk if fld == 'B' else A)(g, arm, 10, 1, idx); b = (Bk if fld == 'B' else A)(g, 'C', 10, 1, idx)
            d.append('%s %s - C %s' % (g, arm, f(C.paired(a, b))))
    add('E2 level-0 bids are within 0.05 of C on core / grand share (mN 1)', 'unresolved', '; '.join(d) + ' (intervals include 0 where the end state is a consensus lottery)')
    recs = C.get('pw56', 'CBK', 10.0, 1.0)
    add('E3 G5/6 CBK grand occupancy over 200-10,000 below 0.5', 'held', 'tail grand occupancy %s' % f(summarize_cell(recs, 'pw56')['tailB_grand-eff']))
    r4 = m(A('pw13', 'CBs', 10, 0, 2))
    add('E4 CBs ring islands >= 0.05 at mN 0', 'held' if r4 and r4[0] >= 0.05 else 'failed', 'ring share %s' % f(r4))
    recs = C.get('pw13', 'CBs', 10.0, 0.0)
    cv = coverage([recs[r] for r in sorted(recs)], 'pw13')
    pos = np.mean([c['freq'] for c in cv if c['min_share'] > 0]); zero = np.mean([c['freq'] for c in cv if c['min_share'] == 0])
    add('E5 zero-share core points under-represented by a factor >= 2 (CBs, mN 0)', 'held' if pos >= 2 * zero else 'failed', 'positive-share %.4f vs zero-share %.4f per point' % (pos, zero))
    return V


if __name__ == '__main__':
    main_report(sys.argv[1], sys.argv[2], sys.argv[3])
