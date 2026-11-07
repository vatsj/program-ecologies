"""Aggregation and verdicts for the majority-division experiment (spec specs/2026-11-07-majority-current-object.md).

    python3 src/majority_tail_report.py ROWS_DIR [--out runs/majority-current-object]

Reads every *.jsonl.gz of ROWS_DIR, writes OUT.json (all cell statistics, validations, verdicts) and OUT.md.
Importable without side effects.
"""
import glob, gzip, json, math, os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import chi2 as C2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLS = ['F', 'U', 'G', 'W', 'D']
BOOT = 2000


def load(rows_dir):
    recs = []
    for f in sorted(glob.glob(os.path.join(rows_dir, '*.jsonl.gz'))):
        with gzip.open(f, 'rt') as fh:
            for line in fh:
                recs.append(json.loads(line))
    return recs


def key_of(r):
    return (r['arm'], r['variant'], r['N'], r['lam'], r['mN'])


def snapv(r, g, name):
    return r['snap'][str(g)][name]


def val(r, name, g=None):
    N = r['N']; I = 64
    g = 120 * N if g is None else g
    s = r['snap'][str(g)]
    if name == 'V':
        return s['cls_modal'][0] / I
    if name == 'Vmajo':
        return s['cls_majo'][0] / I
    if name in CLS:
        return s['cls_modal'][CLS.index(name)] / I
    if name == 'fair_enc':
        return s['fair_enc']
    if name == 'surplus':
        return s['surplus']
    if name == 'npairs':
        return s['npairs_modal']
    if name == 'ties':
        return s['ties'] / I
    raise KeyError(name)


def boot(x, rng, B=BOOT):
    x = np.asarray(x, float)
    n = len(x)
    if n == 0:
        return (float('nan'),) * 3
    idx = rng.integers(0, n, (B, n))
    m = x[idx].mean(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def fmt(t, d=3):
    return '%.*f [%.*f, %.*f]' % (d, t[0], d, t[1], d, t[2])


def exact_multinomial_p(counts):
    """exact multinomial test of uniformity: probability of outcomes no more likely than the observed."""
    n = int(sum(counts)); k = len(counts)
    lf = [math.lgamma(i + 1) for i in range(n + 2)]
    def lp(c):
        return lf[n] - sum(lf[x] for x in c) - n * math.log(k)
    obs = lp(counts)
    p = 0.0
    def rec(prefix, left, j):
        nonlocal p
        if j == k - 1:
            c = prefix + [left]
            l = lp(c)
            if l <= obs + 1e-12:
                p += math.exp(l)
            return
        for x in range(left + 1):
            rec(prefix + [x], left - x, j + 1)
    rec([], n, 0)
    return min(1.0, p)


def goodman(counts, alpha=0.05):
    """simultaneous Goodman intervals for multinomial proportions."""
    n = sum(counts); k = len(counts)
    q = C2.ppf(1 - alpha / k, 1)
    out = []
    for c in counts:
        p = c / n
        lo = (q + 2 * c - math.sqrt(q * (q + 4 * c * (n - c) / n))) / (2 * (n + q))
        hi = (q + 2 * c + math.sqrt(q * (q + 4 * c * (n - c) / n))) / (2 * (n + q))
        out.append((round(lo, 3), round(hi, 3)))
    return out


def group(recs):
    g = {}
    for r in recs:
        g.setdefault(key_of(r), {})[r['run']] = r
    return g


def cell_stats(runs, rng):
    """statistics of one cell (dict run -> record)."""
    rs = [runs[k] for k in sorted(runs)]
    N = rs[0]['N']
    out = dict(n=len(rs))
    for nm in ('V', 'Vmajo', 'fair_enc', 'surplus', 'F', 'U', 'G', 'W', 'D', 'npairs', 'ties'):
        out[nm] = boot([val(r, nm) for r in rs], rng)
    # snapshots of V and fair_enc at every snapshot
    vv = [val(r, 'V') for r in rs]
    out['runs_allfair'] = int(sum(1 for v in vv if v >= 1 - 1e-9)); out['runs_nofair'] = int(sum(1 for v in vv if v <= 1e-9)); out['runs_mixed'] = len(vv) - out['runs_allfair'] - out['runs_nofair']
    out['V_by_snap'] = {}
    for g in (2 * N, 10 * N, 30 * N, 100 * N, 120 * N):
        out['V_by_snap'][str(g)] = boot([val(r, 'V', g) for r in rs], rng)[0]
    out['cls_by_snap'] = {str(g): [float(np.mean([r['snap'][str(g)]['cls_modal'][c] / 64 for r in rs])) for c in range(5)] for g in (2 * N, 10 * N, 30 * N, 100 * N, 120 * N)}
    # consensus
    fair = [r['cons_modal']['fair_pair'] for r in rs]; uneq = [r['cons_modal']['unequal'] for r in rs]
    pc = [sum(1 for f in fair if f == p) for p in range(3)]
    out['cons_fair'] = int(sum(pc)); out['cons_fair_pairs'] = pc
    out['cons_unequal'] = int(sum(1 for u in uneq if u >= 0))
    ou = {}
    for u in uneq:
        if u >= 0:
            ou[str(u)] = ou.get(str(u), 0) + 1
    out['cons_unequal_ids'] = ou
    out['cons_majo_fair'] = int(sum(1 for r in rs if r['cons_majo']['fair_pair'] >= 0))
    if sum(pc) >= 2:
        out['pair_p_exact'] = exact_multinomial_p(pc) if sum(pc) <= 80 else None
        out['pair_goodman'] = goodman(pc)
    out['status'] = {str(s): sum(1 for r in rs if r['status'] == s) for s in sorted({r['status'] for r in rs})}
    out['wall_mean'] = float(np.mean([r['wall'] for r in rs]))
    # transitions: summed matrices
    tr = {}
    for k in rs[0]['trans']:
        M = np.zeros((5, 5)); ff = 0; expo = 0; occ = np.zeros(5)
        for r in rs:
            t = r['trans'].get(k)
            if t is None:
                continue
            M += np.array(t['M']); ff += t['ff']; expo += t['expo']; occ += np.array(t['occ'])
        tr[k] = dict(M=M.tolist(), ff=int(ff), expo=int(expo), occ=occ.tolist(), rate_ff=ff / max(expo, 1))
    out['trans'] = tr
    # tail accounting
    if rs[0]['tail'] is not None:
        nf = len(rs[0]['tail']['early'])
        e = np.zeros((nf, 4)); l = np.zeros((nf, 4)); sched = 0; logged = 0
        for r in rs:
            e += np.array(r['tail']['early']); l += np.array(r['tail']['late']); sched += r['tail']['sched']; logged += r['tail']['logged']
        out['tail'] = dict(early=e.tolist(), late=l.tolist(), per_island_scheduled=sched / (64 * len(rs)), per_island_logged=logged / (64 * len(rs)), fam_names=rs[0]['fam_names'])
    # who holds at 120N
    hold = {'F': {}, 'U': {}}
    for r in rs:
        h = r['snap'][str(120 * N)]['hold']
        for lab in ('F', 'U'):
            for f, c in h[lab].items():
                hold[lab][f] = hold[lab].get(f, 0) + c
    out['hold'] = hold
    out['fam_names'] = rs[0]['fam_names']
    # long chase
    lr = [r for r in rs if r.get('long')]
    if lr:
        out['long'] = dict(n=len(lr), V120=boot([val(r, 'V', 120 * N) for r in lr], rng), V240=boot([val(r, 'V', 240 * N) for r in lr], rng),
                           cons240_fair=sum(1 for r in lr if r['cons_modal_240']['fair_pair'] >= 0),
                           cons240_unequal=sum(1 for r in lr if r['cons_modal_240']['unequal'] >= 0),
                           changed_class=sum(1 for r in lr if r['snap'][str(120 * N)]['cls_modal'] != r['snap'][str(240 * N)]['cls_modal']))
    return out


def paired(a, b, name, rng, g=None):
    """paired (CRN by run index) contrast a - b of a per-run value; a, b dict run -> rec."""
    ks = sorted(set(a) & set(b))
    d = [val(a[k], name, g) - val(b[k], name, g) for k in ks]
    return boot(d, rng) + (len(ks),)


def lands(t):
    return t[0] >= 0.95 and t[1] >= 0.90


def verdicts(G, cs, rng):
    """the prediction table.  G: grouped records, cs: cell statistics."""
    V = []
    def cs_get(arm, var, N, lam, mN):
        return cs.get(key_of(dict(arm=arm, variant=var, N=N, lam=lam, mN=mN)))
    def add(pid, verdict, text, numbers):
        V.append(dict(id=pid, verdict=verdict, rule=text, numbers=numbers))
    # RE 1
    cells = [(N, lam) for N in (100, 200) for lam in (10, 100)]
    vals = {'%d/%g' % c: cs_get('T', 'main', c[0], c[1], 1)['V'] for c in cells if cs_get('T', 'main', c[0], c[1], 1)}
    ok = all(v[0] >= 0.9 for v in vals.values()) and len(vals) == 4
    add('RE 1', 'held' if ok else 'failed', 'T, mN = 1, Lambda 10 and 100, N 100 and 200: V* >= 0.9 in all four', {k: fmt(v) for k, v in vals.items()})
    # RE 2
    c = cs_get('T', 'main', 400, 10, 1)
    if c:
        add('RE 2', 'held' if c['V'][0] >= 0.8 else 'failed', 'T, mN = 1, N = 400, Lambda = 10: V* >= 0.8', {'V': fmt(c['V'])})
    # RE 3
    nums = {}; fail = False; unk = False
    for N in (100, 200, 400):
        for lam in (0, 10, 100):
            c = cs_get('M', 'main', N, lam, 1)
            if c:
                nums['%d/%g' % (N, lam)] = fmt(c['V']); fail |= lands(c['V'])
    c4 = cs_get('M', 'main', 400, 100, 1)
    c4s = [cs_get('M', 'main', 400, lam, 1) for lam in (0, 10, 100)]
    for cc in c4s:
        if cc:
            fail |= cc['V'][0] >= 0.5
    modalU = all((cc['U'][0] >= max(cc['F'][0], cc['G'][0], cc['W'][0], cc['D'][0])) for cc in c4s if cc)
    nums['U_modal_at_400'] = bool(modalU)
    add('RE 3', 'failed' if fail else ('held' if modalU else 'partial'),
        'M does not land in V* at mN = 1 for any N, Lambda; V* at N = 400 below 0.5 with U the modal class (falsifier: lands anywhere, or V* >= 0.5 at N = 400)', nums)
    # RE 4
    nums = {}; worst = None; failed = False; heldall = True
    for N in (100, 200, 400):
        a = G.get(('M', 'main', N, 100, 1)); b = G.get(('M', 'main', N, 0, 1))
        if a and b:
            t = paired(a, b, 'V', rng)
            nums[str(N)] = '%s (n=%d)' % (fmt(t[:3]), t[3])
            if t[0] > 0.10 and t[1] > 0:
                failed = True
            if t[0] > 0.05:
                heldall = False
    add('RE 4', 'failed' if failed else ('held' if heldall else 'partial'), 'M, mN = 1: V*(100) - V*(0) <= +0.05 at every N (falsifier: > +0.10 with interval excluding 0)', nums)
    # RE 5, sol (ii)
    nums = {}; red = {}
    for arm in ('M', 'T'):
        a = G.get((arm, 'main', 100, 100, 0)); b = G.get((arm, 'main', 100, 0, 0))
        if a and b:
            t = paired(b, a, 'W', rng)           # W(0) - W(100) = reduction
            red[arm] = t[0]; nums[arm] = '%s (n=%d), W at Lambda 0 %.3f, at 100 %.3f' % (fmt(t[:3]), t[3], np.mean([val(r, 'W') for r in b.values()]), np.mean([val(r, 'W') for r in a.values()]))
    if len(red) == 2:
        v5 = 'held' if all(x >= 0.10 for x in red.values()) else ('failed' if any(x < 0.05 for x in red.values()) else 'partial')
        add('RE 5', v5, 'mN = 0, N = 100: W share at 120N lower at Lambda = 100 than at 0 by >= 0.10 in both arms (falsifier: < 0.05 in either)', nums)
        add('sol (ii)', 'held' if any(x < 0.10 for x in red.values()) else 'failed', "RE 5's common bound fails in at least one arm (reduction < 0.10 in M or T)", nums)
    # RE 6
    mx = {}
    for (arm, var, N, lam, mN), c in cs.items():
        if var == 'main' and mN == 0 and lam <= 100:
            mx['%s/%d/%g' % (arm, N, lam)] = c['V'][0]
    if mx:
        byarm = {a: max(v for k, v in mx.items() if k.startswith(a + '/')) for a in ('M', 'L', 'T')}
        add('RE 6', 'failed' if any(v >= 0.6 for v in mx.values()) else 'held', 'mN = 0: no arm reaches V* >= 0.6 at any N and Lambda <= 100 (falsifier: any cell >= 0.6)',
            dict(max_by_arm={a: round(v, 3) for a, v in byarm.items()}, cells={k: round(v, 3) for k, v in sorted(mx.items())}))
    # RE 7
    nums = {}; v7 = 'held'; any_scored = False
    for N in (100, 200, 400):
        c = cs_get('T', 'main', N, 100, 1)
        if not c:
            continue
        n = c['cons_fair']
        nums[str(N)] = dict(counts=c['cons_fair_pairs'], p=c.get('pair_p_exact'), goodman=c.get('pair_goodman'))
        if n >= 20:
            any_scored = True
            if c.get('pair_p_exact') is not None and c['pair_p_exact'] < 0.01:
                v7 = 'failed'
    add('RE 7', ('unscored' if not any_scored else v7), "T, mN = 1, Lambda = 100: fair-consensus runs uniform over the pairs (exact multinomial p > 0.01; unscored with < 20 consensus runs)", nums)
    # RE 8 / 8b, counters
    gains = {}
    for N in (100, 200):
        a = G.get(('M', 'D1', N, 100, 1)); b = G.get(('M', 'main', N, 100, 1))
        if a and b:
            t = paired(a, b, 'V', rng)
            gains[N] = t
    if 100 in gains:
        g = gains[100]
        add('RE 8', 'held' if g[0] >= 0.15 else ('failed' if g[0] < 0.05 else 'partial'), 'D1 raises M V* at N = 100, mN = 1 by >= 0.15 over the full tail (falsifier: < 0.05)', {'gain': '%s (n=%d)' % (fmt(g[:3]), g[3])})
    if 200 in gains:
        g = gains[200]
        add('RE 8b', 'held' if g[0] >= 0.15 else ('failed' if g[0] < 0.05 else 'partial'), 'the same at N = 200 (>= 0.15; falsifier < 0.05)', {'gain': '%s (n=%d)' % (fmt(g[:3]), g[3])})
    if 100 in gains and 200 in gains:
        add('argon counter', 'held' if (gains[100][0] < 0.10 and gains[200][0] < 0.10) else 'failed', 'RE 8 fails (gain < 0.10), and fails at N = 200 (scored on the numbers; the timing mechanism was refuted analytically before the run)',
            {'N100': fmt(gains[100][:3]), 'N200': fmt(gains[200][:3])})
        add('sol (i)', 'held' if (gains[200][0] < gains[100][0] and gains[200][0] < 0.05) else 'failed', 'gain at N = 200 < gain at N = 100 and < 0.05', {'N100': fmt(gains[100][:3]), 'N200': fmt(gains[200][:3])})
    # RS, per arm
    rs = {}
    for arm in ('M', 'T', 'L'):
        Nmax = max([k[2] for k in cs if k[0] == arm and k[1] == 'main'] or [0])
        if not Nmax:
            continue
        land = [lam for lam in (10, 100) if cs_get(arm, 'main', Nmax, lam, 1) and lands(cs_get(arm, 'main', Nmax, lam, 1)['V'])]
        rs[arm] = dict(Nmax=Nmax, V={str(lam): fmt(cs_get(arm, 'main', Nmax, lam, 1)['V']) for lam in (10, 100) if cs_get(arm, 'main', Nmax, lam, 1)},
                       lands_in=land, verdict=('failed' if land else 'held'))
    if rs:
        add("RS's recorded prediction", ' / '.join('%s %s' % (a, v['verdict']) for a, v in rs.items()),
            'holds for an arm if it does not land (V* >= 0.95, lower bound >= 0.90) in the mN = 1, Lambda > 0 cells at the largest N run', rs)
    # engineer's
    Vm = {N: (cs_get('M', 'main', N, 100, 1) or {}).get('V') for N in (100, 200, 400)}
    if all(Vm.values()):
        mono = Vm[100][0] > Vm[200][0] > Vm[400][0] and Vm[400][0] < Vm[100][0] - 0.3
        add('E1', 'held' if mono else 'failed', "M's V* at mN = 1, Lambda = 100 strictly falls in N with mean(400) < mean(100) - 0.3", {str(N): fmt(v) for N, v in Vm.items()})
    # E4
    a = cs_get('T', 'T0', 400, 100, 1); b = cs_get('T', 'main', 400, 100, 1)
    if a and b:
        add('E4', 'held' if a['cons_unequal'] - b['cons_unequal'] >= 2 else 'failed', 'N = 400, mN = 1, Lambda = 100: unequal-consensus runs T0 - T >= 2', {'T0': a['cons_unequal'], 'T': b['cons_unequal'], 'n_T0': a['n'], 'n_T': b['n']})
    # E5
    nums = {}
    a = G.get(('M', 'D2', 200, 100, 1)); b = G.get(('M', 'main', 200, 100, 1))
    d4 = [G.get(('M', 'D4:%d' % d, 200, 100, 1)) for d in range(3)]
    if a and b and all(d4):
        g2 = paired(a, b, 'V', rng)[0]
        g4 = [paired(x, b, 'V', rng)[0] for x in d4]
        nums = dict(D2_gain=round(g2, 3), D4_gains=[round(x, 3) for x in g4], D4_mean=round(float(np.mean(g4)), 3))
        add('E5', 'held' if g2 - np.mean(g4) >= 0.10 else 'failed', 'N = 200, mN = 1, Lambda = 100: D2 gain - mean D4 gain >= 0.10', nums)
    # E6
    a = G.get(('M', 'main', 100, 100, 1)); b = G.get(('M', 'main', 100, 0, 1))
    if a and b:
        t = paired(a, b, 'V', rng)
        add('E6', 'held' if (t[0] > 0.10 and t[1] > 0) else 'failed', 'M, N = 100, mN = 1: V*(Lambda = 100) - V*(0) > +0.10 with interval excluding 0', {'contrast': '%s (n=%d)' % (fmt(t[:3]), t[3])})
    return V


def main():
    rows_dir = sys.argv[1]
    out = os.path.join(ROOT, 'runs', 'majority-current-object')
    if '--out' in sys.argv:
        out = sys.argv[sys.argv.index('--out') + 1]
    recs = load(rows_dir)
    rng = np.random.default_rng(20261107)
    G = group(recs)
    cs = {k: cell_stats(v, rng) for k, v in G.items()}
    # D4 pooled over draws
    pool = {}
    for (arm, var, N, lam, mN), runs in G.items():
        if var.startswith('D4'):
            d = int(var.split(':')[1])
            for r, rec in runs.items():
                pool.setdefault((arm, 'D4', N, lam, mN), {})[d * 1000 + r] = rec
    for k, v in pool.items():
        cs[k] = cell_stats(v, rng)
    ver = verdicts(G, cs, rng)
    # contrasts
    contrasts = {}
    for (arm, var, N, lam, mN), runs in G.items():
        if var == 'main' and lam > 0:
            b = G.get((arm, 'main', N, 0, mN))
            if b:
                contrasts['%s|N%d|mN%g|lam%g-lam0' % (arm, N, mN, lam)] = paired(runs, b, 'V', rng)
    for (arm, var, N, lam, mN), runs in G.items():
        if arm == 'T' and var == 'main':
            m = G.get(('M', 'main', N, lam, mN))
            if m:
                contrasts['T-M|N%d|mN%g|lam%g' % (N, mN, lam)] = paired(runs, m, 'V', rng)
        if arm == 'L' and var == 'main':
            m = G.get(('M', 'main', N, lam, mN))
            if m:
                contrasts['M-L|N%d|mN%g|lam%g' % (N, mN, lam)] = paired(m, runs, 'V', rng)
        if arm == 'T' and var == 'T0':
            m = G.get(('T', 'main', N, lam, mN))
            if m:
                contrasts['T-T0|N%d|mN%g|lam%g' % (N, mN, lam)] = paired(m, runs, 'V', rng)
        if arm == 'M' and var != 'main' and not var.startswith('D4'):
            m = G.get(('M', 'main', N, lam, mN))
            if m:
                contrasts['%s-main|N%d|mN%g|lam%g' % (var, N, mN, lam)] = paired(runs, m, 'V', rng)
        if arm == 'M' and var.startswith('D4'):
            m = G.get(('M', 'main', N, lam, mN))
            if m:
                contrasts['%s-main|N%d|mN%g|lam%g' % (var, N, mN, lam)] = paired(runs, m, 'V', rng)
    valid = {}
    vp = os.path.join(ROOT, 'runs', 'majority_tail', 'validation.json')
    if os.path.exists(vp):
        valid = json.load(open(vp))
    d4 = d4_composition()
    res = dict(d4_removed=d4, cells={'|'.join(str(x) for x in k): v for k, v in cs.items()}, contrasts={k: dict(mean=v[0], lo=v[1], hi=v[2], n=v[3]) for k, v in contrasts.items()},
               verdicts=ver, validation=valid)
    json.dump(res, open(out + '.json', 'w'), indent=1, default=float)
    write_md(out + '.md', cs, contrasts, ver, valid)


def d4_composition():
    import majority_tail as MT
    cat = MT.get_cat('M')
    p = MT.base_laws('M')
    out = {}
    for d in range(3):
        fl, tl = MT.variant_laws('M', 'D4:%d' % d)
        per = []
        for sl in range(3):
            rem = np.nonzero((fl[sl] == 0) & (p[sl] > 0))[0]
            rem = sorted(rem, key=lambda x: -p[sl][x])
            per.append(dict(mass=float(p[sl][rem].sum()), n=len(rem), top=[(cat.S.src(sl, int(x)), round(float(p[sl][x]), 4)) for x in rem[:8]]))
        out['D4:%d' % d] = per
    return out


def write_md(path, cs, contrasts, ver, valid):
    L = ['# Majority division in the current object: run record (queue 74)', '',
         'Generated by `src/majority_tail_report.py` from `runs/majority_tail/rows/`. Every number is a **finite-schedule** statement (g = 120N, I = 64, one component); none is pi. Intervals are percentile bootstrap 95% over runs.', '']
    L.append('## Validations'); L.append('')
    for g, v in valid.items():
        L.append('- %s: %s (%s)' % (g, 'PASS' if v.get('passed') else 'FAIL', ', '.join('%s=%s' % (k, v[k]) for k in v if k in ('n', 'wall'))))
    L.append('')
    L.append('## Key table: V* share at 120N (modal outcome is a fair pair), fair encounter probability, consensus counts'); L.append('')
    L.append('| arm | variant | N | Lam | mN | runs | V* | V* (maj. triple) | fair enc. | surplus | F/U/G/W/D | fair consensus (pairs) | unequal consensus | runs all-fair / mixed / none fair |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for k in sorted(cs, key=lambda k: (k[0], k[1], k[2], k[4], k[3])):
        c = cs[k]
        L.append('| %s | %s | %d | %g | %g | %d | %s | %s | %s | %.3f | %s | %d (%s) | %d |' % (k[0], k[1], k[2], k[3], k[4], c['n'], fmt(c['V']), fmt(c['Vmajo'], 2), fmt(c['fair_enc'], 2), c['surplus'][0],
                  '/'.join('%.2f' % c[x][0] for x in CLS), c['cons_fair'], '/'.join(str(x) for x in c['cons_fair_pairs']), c['cons_unequal']) + ' %d / %d / %d |' % (c['runs_allfair'], c['runs_mixed'], c['runs_nofair']))
    L.append('')
    L.append('## V* share along the run (mean over runs of the share of islands whose modal outcome is a fair pair)'); L.append('')
    L.append('| arm | variant | N | Lam | mN | 2N | 10N | 30N | 100N | 120N | ties at 120N |'); L.append('|---|---|---|---|---|---|---|---|---|---|---|')
    for k in sorted(cs, key=lambda k: (k[0], k[1], k[2], k[4], k[3])):
        c = cs[k]; N = k[2]
        L.append('| %s | %s | %d | %g | %g | %s | %.3f | %.4f |' % (k[0], k[1], N, k[3], k[4], ' | '.join('%.3f' % c['V_by_snap'][str(g)] for g in (2 * N, 10 * N, 30 * N, 100 * N)), c['V'][0], c['ties'][0]))
    L.append('')
    L.append('## Transition structure (debounced island-level class transitions; rates per 1,000 island-generations; d25 = 25-generation debounce, dq = round(N/4))'); L.append('')
    L.append('Exit rate of F (F to any other class), entry rate to F (any class to F, per island-generation outside F), fair-to-fair flip rate (per island-generation on F); full 5 x 5 count matrices (rows from, columns to; order F U G W D) are in the JSON.'); L.append('')
    L.append('| arm | variant | N | Lam | mN | window | debounce | F exit | entry to F | F-to-F flips | F occupancy |'); L.append('|---|---|---|---|---|---|---|---|---|---|---|')
    for k in sorted(cs, key=lambda k: (k[0], k[1], k[2], k[4], k[3])):
        c = cs[k]
        for tk in sorted(c['trans']):
            if tk.startswith('chase2'):
                continue
            t = c['trans'][tk]; M = np.array(t['M']); occ = np.array(t['occ']); expo = t['expo']
            if expo == 0:
                continue
            fexit = (M[0].sum() - M[0, 0]) / max(occ[0], 1) * 1000
            entry = (M[:, 0].sum() - M[0, 0]) / max(expo - occ[0], 1) * 1000
            L.append('| %s | %s | %d | %g | %g | %s | %s | %.3f | %.3f | %.3f | %.3f |' % (k[0], k[1], k[2], k[3], k[4], tk.split('|')[0], tk.split('|')[1], fexit, entry, t['rate_ff'] * 1000 * expo / max(occ[0], 1), occ[0] / expo))
    L.append('')
    L.append('## Who holds the islands at 120N (dominant program per slot on F and U islands, by family; counts over runs, islands and slots)'); L.append('')
    for k in sorted(cs, key=lambda k: (k[0], k[1], k[2], k[4], k[3])):
        c = cs[k]
        if k[1] != 'main' or k[4] != 1 or k[3] != 100:
            continue
        names = c['fam_names']
        L.append('- %s N = %d (mN = 1, Lam = 100): F islands %s; U islands %s' % (k[0], k[2], ', '.join('%s %d' % (names[int(f)], n) for f, n in sorted(c['hold']['F'].items(), key=lambda x: -x[1])) or '-', ', '.join('%s %d' % (names[int(f)], n) for f, n in sorted(c['hold']['U'].items(), key=lambda x: -x[1])) or '-'))
    L.append('')
    L.append('## Tail accounting (arrivals by family: delivered / applied / established (an arrival\'s presence episode crosses N/2) / established and the island class changed within 5N), early (g <= 15N) and late')
    L.append('')
    for k in sorted(cs, key=lambda k: (k[0], k[1], k[2], k[4], k[3])):
        c = cs[k]
        if 'tail' not in c or k[3] != 100 or k[4] != 1 or k[1] not in ('main', 'D1', 'D2', 'D3'):
            continue
        t = c['tail']; names = t['fam_names']
        e = np.array(t['early']); l = np.array(t['late'])
        L.append('- %s %s N = %d: delivered per island %.2f (scheduled %.2f); early / late total %d / %d; ' % (k[0], k[1], k[2], t['per_island_logged'], t['per_island_scheduled'], e[:, 0].sum(), l[:, 0].sum()) +
                 '; '.join('%s e %d/%d/%d/%d l %d/%d/%d/%d' % (names[i], *e[i], *l[i]) for i in range(len(names)) if e[i, 0] + l[i, 0] > 0))
    L.append('')
    L.append('## Long chase (runs 0-9 at mN = 1, Lam = 100 continue tail-free to 240N)'); L.append('')
    for k in sorted(cs):
        c = cs[k]
        if 'long' in c:
            lg = c['long']
            L.append('- %s N = %d: V* at 120N %s, at 240N %s; fair consensus at 240N %d, unequal consensus %d of %d runs; island class mix changed between 120N and 240N in %d runs' % (k[0], k[2], fmt(lg['V120']), fmt(lg['V240']), lg['cons240_fair'], lg['cons240_unequal'], lg['n'], lg['changed_class']))
    L.append('')
    L.append('## Without migration (mN = 0): class shares at the founding snapshot 2N and at 120N'); L.append('')
    L.append('| arm | N | Lam | W at 2N | W at 120N | F/U/G/W/D at 120N |'); L.append('|---|---|---|---|---|---|')
    for k in sorted(cs, key=lambda k: (k[0], k[2], k[3])):
        c = cs[k]; N = k[2]
        if k[1] != 'main' or k[4] != 0:
            continue
        L.append('| %s | %d | %g | %.3f | %.3f | %s |' % (k[0], N, k[3], c['cls_by_snap'][str(2 * N)][3], c['cls_by_snap'][str(120 * N)][3], '/'.join('%.2f' % x for x in c['cls_by_snap'][str(120 * N)])))
    L.append('')
    L.append('## Fair-consensus pair counts (runs with >= 0.99 of islands on one fair pair at 120N), by dose and pooled; the uniformity test is exact multinomial (see the prediction table for RE 7)')
    L.append('')
    L.append('| arm | variant | N | mN | Lam 0 | Lam 10 | Lam 100 | pooled over the three Lam (F0/F1/F2; not tested, runs share founders across Lam) |'); L.append('|---|---|---|---|---|---|---|---|')
    seen = set()
    for k in sorted(cs, key=lambda k: (k[0], k[1], k[2], k[4])):
        kk = (k[0], k[1], k[2], k[4])
        if kk in seen or k[4] != 1 or k[1] not in ('main', 'T0'):
            continue
        seen.add(kk)
        row = []; tot = np.zeros(3, int)
        for lam in (0, 10, 100):
            c = cs.get((k[0], k[1], k[2], lam, k[4]))
            if c:
                row.append('%d (%s)' % (c['cons_fair'], '/'.join(str(x) for x in c['cons_fair_pairs']))); tot += np.array(c['cons_fair_pairs'])
            else:
                row.append('-')
        L.append('| %s | %s | %d | %g | %s | %s |' % (k[0], k[1], k[2], k[4], ' | '.join(row), '/'.join(str(x) for x in tot)))
    L.append('')
    L.append('## Paired contrasts on V* (CRN by run index; mean [95% bootstrap], n runs)'); L.append('')
    for k in sorted(contrasts):
        t = contrasts[k]
        L.append('- %s: %s (n = %d)' % (k, fmt(t[:3]), t[3]))
    L.append('')
    L.append('## Prediction table'); L.append('')
    L.append('| id | verdict | rule | numbers |'); L.append('|---|---|---|---|')
    for v in ver:
        L.append('| %s | **%s** | %s | %s |' % (v['id'], v['verdict'], v['rule'], json.dumps(v['numbers'], default=float)))
    open(path, 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
