"""Aggregation and scoring of queue 73 (spec specs/2026-11-03-pair-worth-n.md; predictions/2026-11-03-pair-worth-n.md).
    python3 src/pair_worth_n_report.py ROWS_DIR OUT_MD OUT_JSON
Intervals are percentile bootstrap (2,000 resamples) of run-level means; at mN = 1 islands synchronize so the sample is runs."""
import glob, gzip, json, math, os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pair_worth as PW
import pair_worth_report as PRP

ROOT = PW.ROOT
RNG = np.random.default_rng(73)
G = PW.get_game('pw13')
ARMNAME = {'C': 'C', 'CBs': 'C+B*', 'CB': 'C+B', 'CG': 'C+G', 'CF': 'C+F', 'CF4': 'C+F4', 'CFm': 'C+F-', 'CBk1': 'C+B*_1', 'CBk4': 'C+B*_4'}


# ------------------------------------------------------------------ loading
def load(rows_dir):
    new = {}
    for f in sorted(glob.glob(os.path.join(rows_dir, '*.json'))):
        for r in json.load(open(f)):
            new[(r['arm'], r['N'], r['delta'], r['lam'], r['mN'], r['run'], r.get('chase', 20))] = r
    stored = {}
    p = os.path.join(ROOT, 'runs', 'pair_worth', 'rows.jsonl.gz')
    for l in gzip.open(p, 'rt'):
        r = json.loads(l)
        if r['game'] == 'pw13':
            stored[(r['arm'], r['N'], r['delta'], r['lam'], r['mN'], r['run'], 20)] = r
    return new, stored


class Data:
    def __init__(self, new, stored):
        self.new, self.stored = new, stored
        self.idx = collections.defaultdict(dict)
        for src, d in (('stored', stored), ('new', new)):
            for k, r in d.items():
                self.idx[(k[0], k[1], k[2], k[3], k[4], k[6])][k[5]] = (r, src)

    def cell(self, arm, N, delta=0.05, lam=10.0, mN=1.0, runs=None, chase=20, sources=('new', 'stored')):
        d = self.idx.get((arm, N, float(delta), float(lam), float(mN), chase), {})
        out = {}
        for r, (rec, src) in d.items():
            if src in sources and (runs is None or r in runs):
                out[r] = rec
        return out


# ------------------------------------------------------------------ statistics
def boot(x, B=2000):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (float('nan'),) * 3
    idx = RNG.integers(0, len(x), (B, len(x)))
    m = x[idx].mean(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def fmt(t, d=2):
    if t is None or (isinstance(t, tuple) and math.isnan(t[0])):
        return '-'
    return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])


F = dict(core=lambda r: r['endA'][1] / 64.0, null=lambda r: r['endA'][0] / 64.0, ring=lambda r: r['endA'][2] / 64.0,
         effdom=lambda r: r['endA'][3] / 64.0, undw=lambda r: r['endA'][4] / 64.0, domw=lambda r: r['endA'][5] / 64.0,
         grand=lambda r: r['endB'][1] / 64.0, gwaste=lambda r: r['endB'][2] / 64.0, pair=lambda r: r['endB'][3] / 64.0,
         core90=lambda r: float(r['endA'][1] / 64.0 >= 0.9), consensus=lambda r: float(r['consensus_end']),
         core_last=lambda r: r['occA'][1])


def vals(cell, f='core'):
    return {r: F[f](rec) for r, rec in cell.items()}


def pdiff(a, b):
    common = sorted(set(a) & set(b))
    if not common:
        return None
    return boot([a[r] - b[r] for r in common]) + (len(common),)


def mean_of(d):
    return boot(list(d.values()))


def point(d):
    return float(np.mean(list(d.values()))) if d else float('nan')


def fmtd(t):
    if t is None:
        return 'n/a'
    return '%+.2f [%+.2f, %+.2f] (n=%d)' % t


# ------------------------------------------------------------------ report pieces
def end_table(D, cells, title, runs=None):
    L = ['\n### %s\n' % title]
    L.append('| cell | N | delta | Lambda | mN | runs | core | null | ring | eff-dominated | und. wasteful | dom. wasteful | grand-eff (kind) | pair (kind) | consensus | runs with >= 0.9 core |')
    L.append('|' + '---|' * 16)
    for (arm, N, d, lam, mN, rr, src) in cells:
        c = D.cell(arm, N, d, lam, mN, runs=rr, sources=src)
        if not c:
            continue
        row = [fmt(mean_of(vals(c, f))) for f in ('core', 'null', 'ring', 'effdom', 'undw', 'domw', 'grand', 'pair')]
        L.append('| %s | %d | %g | %g | %g | %d | %s | %.2f | %.2f |' % (ARMNAME[arm], N, d, lam, mN, len(c), ' | '.join(row),
                                                                        point(vals(c, 'consensus')), point(vals(c, 'core90'))))
    return L


def hazards(D, arm, N, lam=10.0, mN=1.0, delta=0.05, runs=None, phase='tail'):
    c = D.cell(arm, N, delta, lam, mN, runs=runs, sources=('new',))
    ex = []; ex_in = []
    for r, rec in sorted(c.items()):
        t = rec['core_transitions']
        ex.append(sum(t['events'][phase]['exit'])); ex_in.append(t['exposure'][phase]['in_core'])
    return np.array(ex, float), np.array(ex_in, float)


def hazard_slope(D, arm, Ns, **kw):
    """log-log slope of the pooled core-exit hazard (tail) against N, run-level bootstrap."""
    data = {N: hazards(D, arm, N, **kw) for N in Ns}
    data = {N: v for N, v in data.items() if len(v[0]) > 0}
    if len(data) < 2:
        return None
    def slope(res):
        xs = []; ys = []
        for N, (e, x) in res.items():
            if e.sum() <= 0 or x.sum() <= 0:
                return float('nan')
            xs.append(math.log(N)); ys.append(math.log(e.sum() / x.sum()))
        return float(np.polyfit(xs, ys, 1)[0])
    s0 = slope(data)
    bs = []
    for _ in range(1000):
        res = {}
        for N, (e, x) in data.items():
            i = RNG.integers(0, len(e), len(e))
            res[N] = (e[i], x[i])
        bs.append(slope(res))
    bs = np.array([b for b in bs if not math.isnan(b)])
    rates = {N: (float(e.sum() / x.sum()) if x.sum() > 0 else float('nan'), int(e.sum()), float(x.sum())) for N, (e, x) in data.items()}
    return dict(slope=s0, lo=float(np.percentile(bs, 2.5)) if len(bs) else float('nan'), hi=float(np.percentile(bs, 97.5)) if len(bs) else float('nan'),
                rates=rates, n_boot=len(bs))


def auc(score, outcome):
    score = np.asarray(score, float); outcome = np.asarray(outcome, bool)
    pos = score[outcome]; neg = score[~outcome]
    if len(pos) == 0 or len(neg) == 0:
        return float('nan')
    r = np.argsort(np.argsort(np.concatenate([pos, neg]))) + 1
    # average ranks for ties
    allv = np.concatenate([pos, neg])
    order = np.argsort(allv, kind='mergesort')
    ranks = np.empty(len(allv)); ranks[order] = np.arange(1, len(allv) + 1)
    for v in np.unique(allv):
        m = allv == v
        ranks[m] = ranks[m].mean()
    return float((ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def supply_arrays(c):
    named = []; minab = []; cnt = []; est = []
    for r, rec in sorted(c.items()):
        s = rec['supply']
        named += s['named_eff']; minab += s['minab_named_eff']; cnt += s['nind_named_eff']; est += [int(e >= 0) for e in rec['est_grand']]
    return np.array(named, bool), np.array(minab, float), np.array(cnt, float), np.array(est, bool)


def founding_supply_share(N, runs, arm='CBs', delta=0.05):
    """share of islands with a named-only efficient founding support, computed from the founders alone (no kernel)."""
    import pair_worth_n_run as NR
    k = 0; tot = 0
    for r in runs:
        prep = NR.prepare_n(arm, N, r, delta, [0.0])
        J = prep['J']; loc = prep['loc']; FAM = prep['table'].FAM
        TOT = G.VEC.sum(1)
        for i in range(prep['I']):
            pa = np.nonzero(loc[i, 0])[0]; pb = np.nonzero(loc[i, 1])[0]; pc = np.nonzero(loc[i, 2])[0]
            sub = J[np.ix_(pa, pb, pc)]
            ef = (G.KIND[sub] == 1) & (TOT[sub] == G.Gd)
            named = (FAM[0, pa] > 0)[:, None, None] & (FAM[1, pb] > 0)[None, :, None] & (FAM[2, pc] > 0)[None, None, :]
            k += int((ef & named).any()); tot += 1
    return k / tot, tot


# ------------------------------------------------------------------ the report
def build(D, assays, static, valid):
    L = []
    P = L.append
    V = []

    def add(name, status, detail):
        V.append(dict(pred=name, verdict=status, detail=detail))
        return status

    # ---------------- cell lists
    R2059 = set(range(20, 60)); R2039 = set(range(20, 40))
    P('# The pair-worth easy case along N (queue 73): run report\n')
    P('Rows: I = 64 islands, w = 0.3, G1/3, annealed tail, paired founders. End class shares are the share of the 64 islands whose modal outcome is in the class at the '
      'final generation, intervals percentile bootstrap of the run-level mean. Core = core proper. Stored rows (queue 72) are labelled stored; the N = 200 and 400 stored '
      'rows are runs 0-19 (exploratory) and are shown separately from the confirmatory runs 20-59.\n')
    # headline table: core share per arm and N
    P('\n## Headline: core share per arm and N (Lambda = 10, mN = 1, delta = 0.05)\n')
    P('| arm | N = 100 (runs 0-59) | N = 200 (runs 20-59 / 20-39) | N = 400 (runs 20-59 / 20-39) | N = 800 (runs 20-29) |')
    P('|---|---|---|---|---|')
    head = {}
    for arm in ('C', 'CBs', 'CB', 'CG', 'CF', 'CF4', 'CFm'):
        row = []
        for N in (100, 200, 400, 800):
            runs = None if N == 100 else (R2059 if arm in ('C', 'CBs', 'CG') and N in (200, 400) else R2039 if N in (200, 400) else set(range(20, 30)))
            c = D.cell(arm, N, 0.05, 10.0, 1.0, runs=runs)
            head[(arm, N)] = c
            row.append(('%s (n=%d)' % (fmt(mean_of(vals(c, 'core'))), len(c))) if c else '-')
        P('| %s | %s |' % (ARMNAME[arm], ' | '.join(row)))
    P('\nExploratory stored runs 0-19 (queue 72): C+B* N = 200: %s; N = 400: %s; C N = 200: %s; N = 400: %s.\n' % (
        fmt(mean_of(vals(D.cell('CBs', 200, runs=set(range(20)), sources=('stored',)), 'core'))),
        fmt(mean_of(vals(D.cell('CBs', 400, runs=set(range(20)), sources=('stored',)), 'core'))),
        fmt(mean_of(vals(D.cell('C', 200, runs=set(range(20)), sources=('stored',)), 'core'))),
        fmt(mean_of(vals(D.cell('C', 400, runs=set(range(20)), sources=('stored',)), 'core')))))
    # end-state tables
    cells = []
    for N, rr in ((100, None), (200, R2059), (400, R2059)):
        for arm in ('C', 'CBs', 'CG'):
            cells.append((arm, N, 0.05, 10.0, 1.0, rr, ('new', 'stored') if N == 100 else ('new',)))
    for N in (100, 200, 400):
        for arm in ('CB', 'CF', 'CF4', 'CFm'):
            cells.append((arm, N, 0.05, 10.0, 1.0, None if N == 100 else R2039, ('new', 'stored')))
    cells += [('C', 800, 0.05, 10.0, 1.0, None, ('new',)), ('CBs', 800, 0.05, 10.0, 1.0, None, ('new',)), ('CG', 800, 0.05, 10.0, 1.0, None, ('new',))]
    L += end_table(D, cells, 'End class shares, delta = 0.05, Lambda = 10, mN = 1')
    cells = []
    for N, rr in ((100, None), (200, R2059), (400, R2059)):
        for arm in ('C', 'CBs', 'CG', 'CB', 'CF'):
            rr2 = rr if (arm in ('C', 'CBs', 'CG') or N == 100) else R2039
            cells.append((arm, N, 0.05, 10.0, 0.0, rr2, ('new', 'stored')))
    L += end_table(D, cells, 'End class shares at mN = 0 (Lambda = 10)')
    cells = [(arm, N, 0.05, 0.0, mN, None, ('new', 'stored')) for N in (100, 200) for mN in (1.0, 0.0) for arm in ('C', 'CBs', 'CG', 'CF')]
    L += end_table(D, cells, 'Tail-free reference (Lambda = 0), N = 100 and 200')
    # ---------------- dose response
    P('\n## Dose response, C+B* (Lambda = 10, mN = 1; N = 100 from the stored cells, labelled stored)\n')
    P('| N | delta | T (28 n^3) | runs | core | pair (kind) | eff-dominated | grand-eff (kind) | paired with delta = 0.05: core diff | minus C (paired) |')
    P('|---|---|---|---|---|---|---|---|---|---|')
    dose_rows = {}
    for N, ds in ((100, (0.01, 0.05, 0.15, 0.3, 0.5)), (200, (0.025, 0.05, 0.15, 0.5)), (400, (0.0125, 0.05, 0.15, 0.5))):
        base = D.cell('CBs', N, 0.05, 10.0, 1.0, runs=None if N == 100 else R2039)
        for d in ds:
            runs = None if N == 100 else R2039
            c = D.cell('CBs', N, d, 10.0, 1.0, runs=runs)
            if not c:
                continue
            dose_rows[(N, d)] = c
            dd = pdiff(vals(c, 'core'), vals(base, 'core')) if d != 0.05 else None
            dC = pdiff(vals(c, 'core'), vals(D.cell('C', N, 0.05, 10.0, 1.0, runs=runs), 'core'))
            P('| %d%s | %g | %.3g | %d | %s | %s | %s | %s | %s | %s |' % (N, ' (stored)' if N == 100 else '', d, 28 * (d * N / 28) ** 3, len(c),
              fmt(mean_of(vals(c, 'core'))), fmt(mean_of(vals(c, 'pair'))), fmt(mean_of(vals(c, 'effdom'))), fmt(mean_of(vals(c, 'grand'))), fmtd(dd), fmtd(dC)))
    # ---------------- inoculation
    P('\n## Fixed-count inoculation C+B*_k and the F- control (Lambda = 10)\n')
    P('| cell | N | mN | runs | core | pair (kind) | null | establishment: islands that ever hold a grand state (25 gens) |')
    P('|---|---|---|---|---|---|---|---|')
    for arm in ('CBk1', 'CBk4', 'CFm'):
        for N in (100, 200, 400):
            for mN in (1.0, 0.0):
                c = D.cell(arm, N, 0.05, 10.0, mN)
                if not c:
                    continue
                est = np.mean([np.mean([e >= 0 for e in rec['est_grand']]) for rec in c.values()])
                P('| %s | %d | %g | %d | %s | %s | %.2f | %.2f |' % (ARMNAME[arm], N, mN, len(c), fmt(mean_of(vals(c, 'core'))), fmt(mean_of(vals(c, 'pair'))),
                                                                  point(vals(c, 'null')), est))
    # ---------------- paired differences
    P('\n## Paired differences on shared founders (run-level bootstrap; Lambda = 10, mN = 1 unless stated)\n')
    P('| N | contrast | core diff | pair-kind diff |')
    P('|---|---|---|---|')
    pd = {}
    def contrast(N, a, b, name, runs, mN=1.0, da=0.05, db=0.05):
        ca = D.cell(a, N, da, 10.0, mN, runs=runs); cb = D.cell(b, N, db, 10.0, mN, runs=runs)
        x = pdiff(vals(ca, 'core'), vals(cb, 'core')); y = pdiff(vals(ca, 'pair'), vals(cb, 'pair'))
        pd[(N, name, mN)] = (x, y)
        if x:
            P('| %d%s | %s | %s | %s |' % (N, '' if mN == 1.0 else ' (mN %g)' % mN, name, fmtd(x), fmtd(y)))
    for N in (100, 200, 400):
        r5 = None if N == 100 else R2059; r3 = None if N == 100 else R2039
        contrast(N, 'CBs', 'C', 'C+B* - C', r5); contrast(N, 'CG', 'C', 'C+G - C', r5); contrast(N, 'CG', 'CBs', 'C+G - C+B*', r5)
        contrast(N, 'CF', 'CG', 'C+F - C+G', r3 if N > 100 else None); contrast(N, 'CF', 'CBs', 'C+F - C+B*', r3 if N > 100 else None)
        contrast(N, 'CB', 'CBs', 'C+B - C+B*', r3 if N > 100 else None)
        contrast(N, 'CF', 'CFm', 'C+F - C+F-', set(range(20)) if N == 100 else r3)
        contrast(N, 'CF4', 'CF', 'C+F4 - C+F', r3)
        contrast(N, 'CBs', 'C', 'C+B* - C', r5 if N > 100 else None, mN=0.0)
        contrast(N, 'CG', 'C', 'C+G - C', r5 if N > 100 else None, mN=0.0)
    # ---------------- coverage mN = 0
    P('\n## Core coverage at mN = 0, C+B* (Lambda = 10): the 19 core points\n')
    cov_res = {}
    for N, rr in ((100, None), (200, R2059), (400, R2039)):
        c = D.cell('CBs', N, 0.05, 10.0, 0.0, runs=rr)
        if not c or len(c) < 5:
            continue
        cov = PRP.coverage([c[r] for r in sorted(c)], 'pw13')
        bad = [x for x in cov if x['hi'] < 1 / 76]
        cov_res[(N, len(c))] = dict(n=len(c), observed=sum(1 for x in cov if x['runs_with'] > 0), n_bad=len(bad), total=sum(x['freq'] for x in cov))
        P('- N = %d (%d runs): core points observed in >= 1 run: %d/19; points with simultaneous upper bound < 1/76: %d; total core share %.3f; frequencies (min share > 0 points %.4f, zero-share points %.4f)' % (
            N, len(c), cov_res[(N, len(c))]['observed'], len(bad), cov_res[(N, len(c))]['total'],
            np.mean([x['freq'] for x in cov if x['min_share'] > 0]), np.mean([x['freq'] for x in cov if x['min_share'] == 0])))
    # consensus at mN = 1
    P('\nMetapopulation consensus at mN = 1 (share of runs in which all 64 islands share one modal outcome) is in the end tables (column consensus).\n')
    # ---------------- supply realized
    P('\n## Supply realized at founding and establishment (new cells)\n')
    P('| cell | N | mN | islands with any compatible grand support | named-only efficient support | mean min abundance of the best named support (with support) | mean count of named compatible triples | establishment: with named support | without | all islands |')
    P('|---|---|---|---|---|---|---|---|---|---|')
    for (arm, N, d, mN, rr) in [('CBs', 200, 0.05, 1.0, R2059), ('CBs', 200, 0.05, 0.0, R2059), ('CBs', 400, 0.05, 1.0, R2059), ('CBs', 400, 0.05, 0.0, R2039),
                                ('CBs', 400, 0.0125, 1.0, R2039), ('CBs', 400, 0.0125, 0.0, R2039), ('CBs', 200, 0.025, 1.0, R2039), ('CBs', 400, 0.5, 1.0, R2039),
                                ('CG', 200, 0.05, 1.0, R2059), ('CG', 400, 0.05, 1.0, R2059), ('CF', 200, 0.05, 1.0, R2039), ('CF', 400, 0.05, 1.0, R2039), ('CF', 100, 0.05, 1.0, None)]:
        c = D.cell(arm, N, d, 10.0, mN, runs=rr, sources=('new',))
        if not c:
            continue
        named, minab, cnt, est = supply_arrays(c)
        anyg = np.mean([x for rec in c.values() for x in rec['supply']['any']])
        P('| %s d=%g | %d | %g | %.3f | %.3f | %.1f | %.1f | %s | %s | %.2f |' % (ARMNAME[arm], d, N, mN, anyg, named.mean(),
          minab[named].mean() if named.any() else float('nan'), cnt[named].mean() if named.any() else float('nan'),
          ('%.2f' % est[named].mean()) if named.any() else '-', ('%.2f' % est[~named].mean()) if (~named).any() else '-', est.mean()))
    # ---------------- transitions
    P('\n## Core entry and exit (finite-schedule rates, debounced 25 generations; not epsilon-free)\n')
    P('Exposure = island-generations; hazards per island-generation. Ancestry = what reached 10% of a slot on that island in the previous 200 generations: arrival (a tail mutant), migrant (a type new to the island, born without an arrival) or resident.\n')
    P('| cell | N | mN | phase | exits | in-core exposure | exit hazard | entries | out-of-core exposure | entry hazard | exit ancestry (res / mig / arr) | entry ancestry |')
    P('|---|---|---|---|---|---|---|---|---|---|---|---|')
    haz_cells = [('CBs', 200, 0.05, 1.0, R2059), ('CG', 200, 0.05, 1.0, R2059), ('CF', 200, 0.05, 1.0, R2039), ('CBs', 400, 0.05, 1.0, R2059), ('CG', 400, 0.05, 1.0, R2059),
                 ('CF', 400, 0.05, 1.0, R2039), ('CG', 100, 0.05, 1.0, set(range(20, 60))), ('CF', 100, 0.05, 1.0, None), ('CBs', 400, 0.05, 0.0, R2039), ('CG', 400, 0.05, 0.0, R2039)]
    for (arm, N, d, mN, rr) in haz_cells:
        c = D.cell(arm, N, d, 10.0, mN, runs=rr, sources=('new',))
        if not c:
            continue
        for ph in ('tail', 'chase'):
            ex = np.zeros(3); en = np.zeros(3); xin = 0; xout = 0
            for rec in c.values():
                t = rec['core_transitions']
                ex += t['events'][ph]['exit']; en += t['events'][ph]['entry']
                xin += t['exposure'][ph]['in_core']; xout += t['exposure'][ph]['out_core']
            P('| %s | %d | %g | %s | %d | %.3g | %.2e | %d | %.3g | %.2e | %s | %s |' % (ARMNAME[arm], N, mN, ph, ex.sum(), xin, ex.sum() / max(xin, 1), en.sum(), xout,
              en.sum() / max(xout, 1), ' / '.join('%d' % x for x in ex), ' / '.join('%d' % x for x in en)))
    # ---------------- holders
    P('\n## Who holds the core (core islands at the end; Lambda = 10, mN = 1)\n')
    P('| cell | N | core islands | majority programs: other constant / grand constant / bid / F | islands with all three majorities grand constants | islands with a reader in the majority |')
    P('|---|---|---|---|---|---|')
    for (arm, N, d, rr) in [('CBs', 200, 0.05, R2059), ('CBs', 400, 0.05, R2059), ('CG', 200, 0.05, R2059), ('CG', 400, 0.05, R2059), ('CF', 200, 0.05, R2039), ('CF', 400, 0.05, R2039),
                            ('CB', 400, 0.05, R2039), ('CBs', 400, 0.5, R2039), ('CBk4', 400, 0.05, R2039), ('CBk4', 100, 0.05, None)]:
        c = D.cell(arm, N, d, 10.0, 1.0, runs=rr, sources=('new',))
        if not c:
            continue
        mj = np.zeros(4); n = 0; a3 = 0; ar = 0
        for rec in c.values():
            h = rec['holders']; mj += h['majority_program_class']; n += h['n_core_islands']; a3 += h['all3_grand_constants']; ar += h['any_reader_majority']
        P('| %s | %d | %d | %s | %d | %d |' % (ARMNAME[arm], N, n, ' / '.join('%d' % x for x in mj), a3, ar))
    # ---------------- assays
    P('\n## Invasion assays (cell F; single island, no migration, no tail, 2,000 replicates; exact two-type value alongside)\n')
    P('| N | resident | slot | entrant | u resident | u entrant | N p (MC) | N p (exact) | z against neutral |')
    P('|---|---|---|---|---|---|---|---|---|')
    for r in assays['rows']:
        P('| %d | %s | %d | %s | %.3f | %.3f | %.2f | %.3f | %+.2f |' % (r['N'], r['resident'], r['slot'], r['invader'], r['u_resident'], r['u_invader'], r['Np_mc'], r['Np_exact'], r['z_vs_neutral']))
    # ---------------- G, D
    P('\n## Cell G (longer chase, 60 N) and cell D (N = 800)\n')
    for arm in ('CBs', 'CG'):
        c20 = D.cell(arm, 400, 0.05, 10.0, 1.0, runs=set(range(20, 25)), chase=20)
        c60 = D.cell(arm, 400, 0.05, 10.0, 1.0, runs=set(range(20, 25)), chase=60)
        if c60:
            P('- %s N = 400, runs 20-24: core at chase 20N %s; at chase 60N %s (same runs and founders)' % (ARMNAME[arm], fmt(mean_of(vals(c20, 'core'))), fmt(mean_of(vals(c60, 'core')))))
    # ================================================================== verdicts
    def Dc(arm, N, delta=0.05, mN=1.0, runs=None, lam=10.0):
        return D.cell(arm, N, delta, lam, mN, runs=runs)
    # RS conjecture
    cl1 = []
    for (arm, d) in (('C', 0.05), ('CBs', 0.05), ('CB', 0.05), ('CG', 0.05), ('CF', 0.05), ('CBs', 0.0125), ('CBs', 0.15), ('CBs', 0.5), ('CBk1', 0.05), ('CBk4', 0.05)):
        runs = R2059 if (arm in ('C', 'CBs', 'CG') and d == 0.05) else R2039
        c = Dc(arm, 400, d, runs=runs)
        if c:
            cl1.append((ARMNAME[arm] + (' d=%g' % d if d != 0.05 else ''), point(vals(c, 'core')), len(c)))
    best = max(cl1, key=lambda x: x[1]) if cl1 else None
    cl2 = [v for k, v in cov_res.items() if k[0] == 400]
    cov400 = None
    if cl2:
        cov400 = max(cl2, key=lambda v: v['n'])
    clause1 = (best is not None and best[1] >= 0.95)
    clause2 = (cov400 is not None and cov400['n_bad'] == 0)
    if best is None:
        st = 'unresolved'
    elif not clause1:
        st = 'failed'
    elif cov400 is None:
        st = 'unresolved'
    else:
        st = 'held' if (clause1 and clause2) else 'failed'
    add('RS conjecture re-scored at N = 400', st, 'best arm at N = 400, mN = 1: %s (%s, %d runs; threshold 0.95); coverage mN = 0 C+B*: %s' % (
        best[0] if best else '-', ('%.3f' % best[1]) if best else '-', best[2] if best else 0,
        ('%d of 19 core points observed, %d with simultaneous upper bound < 1/76' % (cov400['observed'], cov400['n_bad'])) if cov400 else 'not run'))
    # RE1
    c_C = Dc('C', 400, runs=R2059); c_B = Dc('CBs', 400, runs=R2059)
    d1a = pdiff(vals(c_B, 'core'), vals(c_C, 'core'))
    c_lo = Dc('CBs', 400, 0.0125, runs=R2039); d1b = pdiff(vals(c_lo, 'core'), vals(Dc('C', 400, runs=R2039), 'core'))
    c_2 = Dc('CBs', 200, 0.025, runs=R2039); d1c = pdiff(vals(c_2, 'core'), vals(Dc('C', 200, runs=R2039), 'core'))
    parts = []
    if c_B and d1a:
        parts.append(point(vals(c_B, 'core')) >= 0.7 and d1a[0] >= 0.3)
    if d1b:
        parts.append(abs(d1b[0]) <= 0.15)
    if d1c:
        parts.append(abs(d1c[0]) <= 0.15)
    full = len(parts) == 3
    st = ('held' if all(parts) else 'failed') if full else ('failed' if (parts and not all(parts)) else 'unresolved')
    add('RE1 supply, not N or dose, is the lever for bids', st, 'N = 400 C+B* core %s, minus C %s (>= 0.7, >= 0.3); d = 0.0125 minus C %s (|.| <= 0.15); N = 200 d = 0.025 minus C %s (|.| <= 0.15)' % (
        fmt(mean_of(vals(c_B, 'core'))) if c_B else '-', fmtd(d1a), fmtd(d1b), fmtd(d1c)))
    # RE2
    hi = Dc('CBs', 400, 0.5, runs=R2039); base = Dc('CBs', 400, 0.05, runs=R2039)
    g2a = pdiff(vals(hi, 'core'), vals(base, 'core')); g2b = pdiff(vals(hi, 'pair'), vals(base, 'pair'))
    if g2a and g2b:
        st = 'held' if (g2a[0] <= -0.15 and g2b[0] >= 0.15) else 'failed'
    else:
        st = 'unresolved'
    add('RE2 dose is non-monotone at large N', st, 'N = 400 d = 0.5 minus d = 0.05: core %s (<= -0.15), pair-kind %s (>= +0.15)' % (fmtd(g2a), fmtd(g2b)))
    # RE3
    p3 = []
    d3 = {}
    for N in (200, 400):
        d3[N] = pdiff(vals(Dc('CG', N, runs=R2059), 'core'), vals(Dc('CBs', N, runs=R2059), 'core'))
        if d3[N]:
            p3.append(d3[N][0] >= -0.05)
    g400 = Dc('CG', 400, runs=R2059)
    if g400:
        p3.append(point(vals(g400, 'core')) >= 0.8)
    add('RE3 constants coordinate better than bids at every N', ('held' if all(p3) else 'failed') if len(p3) == 3 else ('failed' if p3 and not all(p3) else 'unresolved'),
        'C+G - C+B*: N = 200 %s, N = 400 %s (>= -0.05); C+G core at N = 400 %s (>= 0.8)' % (fmtd(d3[200]), fmtd(d3[400]), fmt(mean_of(vals(g400, 'core'))) if g400 else '-'))
    # RE4
    p4 = []; det = []
    for N in (100, 200, 400):
        r_ = None if N == 100 else R2039
        x = pdiff(vals(Dc('CF', N, runs=r_), 'core'), vals(Dc('CG', N, runs=r_), 'core'))
        det.append('N = %d C+F - C+G %s' % (N, fmtd(x)))
        if x:
            p4.append(abs(x[0]) <= 0.15)
    x = pdiff(vals(Dc('CF', 100), 'core'), vals(Dc('CBs', 100), 'core'))
    det.append('N = 100 C+F - C+B* %s (>= 0.3)' % fmtd(x))
    if x:
        p4.append(x[0] >= 0.3)
    add('RE4 a flexible bid is a constant with a fallback', ('held' if all(p4) else 'failed') if len(p4) == 4 else ('failed' if p4 and not all(p4) else 'unresolved'), '; '.join(det))
    # RE5
    c5 = {a: Dc(a, 400, mN=0.0, runs=R2039) for a in ('CBs', 'CG')}
    if all(c5.values()):
        ok = all(point(vals(c, 'core')) >= 0.5 and point(vals(c, 'null')) <= 0.2 for c in c5.values())
        add('RE5 local supply is enough without migration at N = 400', 'held' if ok else 'failed',
            'mN = 0, N = 400: core / null: ' + '; '.join('%s %s / %.2f' % (ARMNAME[a], fmt(mean_of(vals(c, 'core'))), point(vals(c, 'null'))) for a, c in c5.items()))
    else:
        add('RE5 local supply is enough without migration at N = 400', 'unscored (cell cut)', 'mN = 0 cells at N = 400 absent')
    # RE6
    arms400 = []
    for (arm, d) in (('C', 0.05), ('CBs', 0.05), ('CB', 0.05), ('CG', 0.05), ('CF', 0.05), ('CBs', 0.0125), ('CBs', 0.15), ('CBs', 0.5), ('CBk1', 0.05), ('CBk4', 0.05)):
        runs = R2059 if (arm in ('C', 'CBs', 'CG') and d == 0.05) else R2039
        c = Dc(arm, 400, d, runs=runs)
        if c:
            m = mean_of(vals(c, 'core'))
            arms400.append((ARMNAME[arm] + (' d=%g' % d if d != 0.05 else ''), m))
    if arms400:
        bestm = max(arms400, key=lambda x: x[1][0])
        viol = [a for a in arms400 if a[1][0] >= 0.95 and a[1][1] >= 0.9]
        st = 'failed' if viol else ('held' if bestm[1][0] <= 0.9 else 'unresolved')
        add('RE6 the RS conjecture still fails at N = 400 on the core clause', st, 'best arm %s core %s; arms: %s' % (bestm[0], fmt(bestm[1]), '; '.join('%s %.2f' % (a, m[0]) for a, m in arms400)))
    # RE7
    rows = assays['rows']
    b3 = [r for r in rows if r['resident'] == 'B*^3' and r['invader'] == 'matching grand constant']
    g3 = [r for r in rows if r['resident'] == 'G^3' and r['neutral']]
    sel = [r for r in rows if not r['neutral']]
    ok_b3 = all(abs(r['z_vs_neutral']) <= 2 for r in b3)
    ok_sel = all(r['Np_mc'] < 0.5 and r['Np_exact'] < 0.5 for r in sel)
    g3_flag = [r for r in g3 if abs(r['z_vs_neutral']) > 2]
    g3_bad = [r for r in g3 if abs(r['z_vs_neutral']) > 3]
    add('RE7 entry is the bind, exit is neutral drift (assays)', 'held' if (ok_b3 and ok_sel and not g3_bad) else 'failed',
        'B*^3 matching constant: max |z| %.2f over %d cells (<= 2); selected entrants: max N p (MC / exact) %.2f / %.3f (< 0.5); G^3 neutral cells: %d with |z| in (2, 3), %d beyond 3' % (
            max(abs(r['z_vs_neutral']) for r in b3), len(b3), max(r['Np_mc'] for r in sel), max(r['Np_exact'] for r in sel), len(g3_flag) - len(g3_bad), len(g3_bad)))
    # RE8
    a4 = Dc('CBk4', 400, runs=R2039); a1 = Dc('CBk4', 100)
    if a4 and a1:
        dd = point(vals(a4, 'core')) - point(vals(a1, 'core'))
        add('RE8 fixed count isolates N', 'held' if dd < 0.15 else 'failed', 'C+B*_4 core: N = 400 %s, N = 100 %s, difference %+.2f (< 0.15)' % (fmt(mean_of(vals(a4, 'core'))), fmt(mean_of(vals(a1, 'core'))), dd))
    else:
        add('RE8 fixed count isolates N', 'unscored (cell cut)', 'C+B*_4 at N = 400 absent')
    # argon (i)
    lo1 = Dc('CBs', 400, 0.0125, runs=R2039); lo0 = Dc('CBs', 400, 0.0125, mN=0.0, runs=R2039); cC = Dc('C', 400, runs=R2039)
    dd = pdiff(vals(lo1, 'core'), vals(cC, 'core'))
    if lo1 and lo0 and dd:
        ok = point(vals(lo1, 'core')) >= 0.5 and dd[0] > 0.15 and point(vals(lo0, 'core')) <= point(vals(lo1, 'core')) - 0.30
        add('argon (i) metapopulation supply I T is the lever at mN = 1', 'held' if ok else 'failed',
            'N = 400 d = 0.0125: core mN = 1 %s, minus C %s, core mN = 0 %s' % (fmt(mean_of(vals(lo1, 'core'))), fmtd(dd), fmt(mean_of(vals(lo0, 'core')))))
    elif lo1 and dd:
        ok = not (point(vals(lo1, 'core')) >= 0.5 and dd[0] > 0.15)
        add('argon (i) metapopulation supply I T is the lever at mN = 1', 'failed' if ok else 'unresolved', 'mN = 1 clauses: core %s, minus C %s (mN = 0 cell cut)' % (fmt(mean_of(vals(lo1, 'core'))), fmtd(dd)))
    else:
        add('argon (i) metapopulation supply I T is the lever at mN = 1', 'unscored (cell cut)', 'N = 400 d = 0.0125 absent')
    # argon (ii)
    cf = Dc('CF', 200, runs=R2039); cf4 = Dc('CF4', 200, runs=R2039)
    if cf:
        v = point(vals(cf, 'effdom'))
        add('argon (ii) C+F has an efficient-dominated share > 0.15', 'held' if v > 0.15 else 'failed',
            'N = 200: C+F %s, C+F4 %s; N = 100: %s; N = 400: %s' % (fmt(mean_of(vals(cf, 'effdom'))), fmt(mean_of(vals(cf4, 'effdom'))) if cf4 else '-',
            fmt(mean_of(vals(Dc('CF', 100), 'effdom'))), fmt(mean_of(vals(Dc('CF', 400, runs=R2039), 'effdom'))) if Dc('CF', 400, runs=R2039) else '-'))
    # sol (iii)
    sl = {}
    for arm, Ns in (('CG', (100, 200, 400)), ('CBs', (200, 400))):
        def hz(arm, N):
            rr = set(range(20, 60)) if arm in ('CG', 'CBs') and N != 100 else set(range(20, 60))
            return rr
        sl[arm] = hazard_slope(D, arm, Ns, runs=None)
    txt = []
    oks = []
    for arm, s in sl.items():
        if s:
            txt.append('%s slope %.2f [%.2f, %.2f], hazards %s' % (ARMNAME[arm], s['slope'], s['lo'], s['hi'], {N: '%.2e (%d exits)' % (v[0], v[1]) for N, v in s['rates'].items()}))
            oks.append(not (s['lo'] <= -1 <= s['hi']))
    if oks:
        st3 = 'held' if all(oks) else ('unresolved' if any(oks) else 'failed')
        add('sol (iii) raw exit rates do not follow 1/N', st3, '; '.join(txt) + ' [held iff every arm\'s interval excludes -1; unresolved when some do and some include -1]')
    # sol (iv)
    p = []; det = []
    for N in (100, 200):
        r_ = None if N == 100 else R2039
        cF = Dc('CF', N, runs=r_); cG = Dc('CG', N, runs=r_); cm = Dc('CFm', N, runs=set(range(20)) if N == 100 else r_)
        a = pdiff(vals(cF, 'pair'), vals(cG, 'pair')); b = pdiff(vals(cF, 'core'), vals(cG, 'core')); c_ = pdiff(vals(cF, 'pair'), vals(cm, 'pair'))
        det.append('N = %d: pair C+F - C+G %s; core C+F - C+G %s; pair C+F - C+F- %s' % (N, fmtd(a), fmtd(b), fmtd(c_)))
        if a and b and c_:
            p.append(a[0] >= 0.05 and abs(b[0]) <= 0.15 and c_[0] >= 0.05)
    add('sol (iv) C+F differs from C+G through a pair excess, not a reading premium', ('held' if all(p) else 'failed') if len(p) == 2 else 'unresolved', '; '.join(det))
    # sol (v)
    det = []; res_a = []
    for N, rr in ((200, R2059), (400, R2039)):
        c = D.cell('CBs', N, 0.05, 10.0, 0.0, runs=rr, sources=('new',))
        if c:
            named, minab, cnt, est = supply_arrays(c)
            m = named
            if m.sum() > 5 and est[m].any() and (~est[m]).any():
                a1_, a2_ = auc(minab[m], est[m]), auc(cnt[m], est[m])
                det.append('mN = 0 N = %d (%d islands with support, %.2f established): AUC min abundance %.3f, AUC count %.3f' % (N, m.sum(), est[m].mean(), a1_, a2_))
                res_a.append(a1_ >= a2_)
            else:
                det.append('mN = 0 N = %d: %d islands with named support, establishment %s (AUC undefined)' % (N, int(m.sum()), est[m].mean() if m.sum() else '-'))
    c = D.cell('CBs', 400, 0.0125, 10.0, 1.0, runs=R2039, sources=('new',))
    resb = None
    if c:
        named, minab, cnt, est = supply_arrays(c)
        if named.any() and (~named).any():
            rw, rn = est[named].mean(), est[~named].mean()
            det.append('mN = 1 N = 400 d = 0.0125: establishment with named support %.2f (%d islands), without %.2f (%d islands)' % (rw, named.sum(), rn, (~named).sum()))
            resb = rn >= 0.5 * rw
    if res_a and resb is not None:
        add('sol (v) rescue depends on lineage survival and assembly, not triple count', 'held' if (all(res_a) and resb) else 'failed', '; '.join(det) + ' [the registered inequality holds trivially: both areas are at chance, founding support does not predict establishment]')
    else:
        add('sol (v) rescue depends on lineage survival and assembly, not triple count', 'unresolved', '; '.join(det) or 'cells absent')
    # E1
    det = []; ok = []
    for N, runs in ((100, list(range(0, 60))), (200, list(range(20, 60))), (400, list(range(20, 60)))):
        share, n = founding_supply_share(N, runs)
        exp = {100: 0.116, 200: 0.537, 400: 0.982}[N]
        det.append('N = %d: %.3f over %d islands (predicted %.3f)' % (N, share, n, exp))
        ok.append(abs(share - exp) <= 0.05)
    add('E1 founding supply as counted', 'held' if all(ok) else 'failed', '; '.join(det))
    # E2
    p = []; det = []
    for N in (100, 200):
        x = pdiff(vals(Dc('CF', N, runs=set(range(20)) if N == 100 else R2039), 'core'), vals(Dc('CFm', N, runs=set(range(20)) if N == 100 else R2039), 'core'))
        det.append('N = %d C+F - C+F- %s' % (N, fmtd(x)))
        if x:
            p.append(abs(x[0]) < 0.10)
    add('E2 the pair fallback does not change the core share', ('held' if all(p) else 'failed') if len(p) == 2 else 'unresolved', '; '.join(det))
    # E3
    g200 = Dc('CG', 200, runs=R2059)
    if g200:
        add('E3 constants carry the easy case once supply exists (C+G core >= 0.5 at N = 200)', 'held' if point(vals(g200, 'core')) >= 0.5 else 'failed', 'C+G N = 200 core %s' % fmt(mean_of(vals(g200, 'core'))))
    P('\n## Cost\n')
    byN = collections.defaultdict(lambda: [0, 0.0])
    for k, r in D.new.items():
        byN[k[1]][0] += 1; byN[k[1]][1] += r['kern_wall'] + r['prep_wall'] / max(1, len([1])) 
    P('| N | records | kernel core-hours (preparation counted once per job below) |'); P('|---|---|---|')
    prep = collections.defaultdict(float)
    seen = set()
    for k, r in D.new.items():
        jk = (k[0], k[1], k[2], k[5], k[6])
        if jk not in seen:
            seen.add(jk); prep[k[1]] += r['prep_wall']
    for N in sorted(byN):
        P('| %d | %d | kernel %.1f + preparation %.1f |' % (N, byN[N][0], sum(r['kern_wall'] for k, r in D.new.items() if k[1] == N) / 3600.0, prep[N] / 3600.0))
    P('\n## Prediction verdicts\n')
    P('| prediction | verdict | measured |')
    P('|---|---|---|')
    for v in V:
        P('| %s | %s | %s |' % (v['pred'], v['verdict'], v['detail']))
    return L, V


def main(rows_dir, out_md, out_json):
    new, stored = load(rows_dir)
    D = Data(new, stored)
    assays = json.load(open(os.path.join(ROOT, 'runs', 'pair_worth_n', 'assays.json')))
    static = json.load(open(os.path.join(ROOT, 'runs', 'pair_worth_n', 'static.json')))
    L, V = build(D, assays, static, None)
    open(out_md, 'w').write('\n'.join(L) + '\n')
    summ = {}
    for key, recs in sorted(D.idx.items()):
        c = {r: rec for r, (rec, src) in recs.items()}
        summ['|'.join(str(k) for k in key)] = dict(runs=sorted(c), core=boot([F['core'](x) for x in c.values()]), pair=boot([F['pair'](x) for x in c.values()]),
                                                     null=boot([F['null'](x) for x in c.values()]), effdom=boot([F['effdom'](x) for x in c.values()]))
    json.dump(dict(cells=summ, verdicts=V), open(out_json, 'w'), indent=1, default=float)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
