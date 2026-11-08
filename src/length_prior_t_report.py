"""Report of series 2a / 2b and the step-3 join of queue 75 (spec specs/2026-11-08-length-prior-t.md).

    python3 src/length_prior_t_report.py ROWS_DIR [ROWS_DIR ...] --step1 runs/lt-prior.json --out runs/length-prior-t

Reads every rows_*.jsonl under the given directories (recursively), builds the cell table (V* share at 120N with the
bootstrap-over-runs interval, consensus counts, transition counts), the delta* tables with brackets, c*, the matched-count
cells, the slices, the verdicts on the registered predictions and the join.
"""
import os, sys, json, glob, math, argparse
import numpy as np

DELTAS = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 2e-1]       # ascending
THR = 0.9
LAM = 100


def load(dirs):
    rows = {}
    for d in dirs:
        for f in glob.glob(os.path.join(d, '**', 'rows_*.jsonl'), recursive=True):
            for line in open(f):
                line = line.strip()
                if line:
                    try:
                        r = json.loads(line)
                    except ValueError:
                        continue
                    rows[r['id']] = r
    return list(rows.values())


def boot(x, B=2000, seed=1):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (float('nan'),) * 3
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(B, len(x)))
    m = x[idx].mean(1)
    return float(x.mean()), float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def cells(rows, long=False):
    """{(series, spec, N, I): list of rows} (long rows kept apart)."""
    out = {}
    for r in rows:
        if bool(r.get('long')) != long:
            continue
        out.setdefault((r['series'], r['spec'], r['N'], r['I']), []).append(r)
    return out


def cell_stats(rs, long=False):
    N = rs[0]['N']
    g = 240 * N if long else 120 * N
    v = [r['vshare_ts'][g // N] if long else r['vstar'] for r in rs]
    m, lo, hi = boot(v)
    cons = dict(fair=sum(1 for r in rs if r['cons_modal']['fair_pair'] >= 0), unequal=sum(1 for r in rs if r['cons_modal']['unequal'] >= 0))
    pairs = [0, 0, 0]
    for r in rs:
        if r['cons_modal']['fair_pair'] >= 0:
            pairs[r['cons_modal']['fair_pair']] += 1
    # transitions at the 0.25 N debounce: class-to-class counts (5 x 5), fair-to-fair flips, exposure
    tr = {}
    for w in ('tail|dq', 'chase|dq'):
        M = np.zeros((5, 5)); ff = 0; expo = 0
        for r in rs:
            t = r['trans'][w]
            M += np.array(t['M']); ff += t['ff']; expo += t['expo']
        tr[w] = dict(rate_per_island_gen=float(M.sum() / max(expo, 1)), ff_per_island_gen=float(ff / max(expo, 1)), expo=int(expo))
    return dict(n=len(rs), vstar=m, lo=lo, hi=hi, runs_vstar=v, consensus=cons, consensus_pairs=pairs, trans=tr)


def delta_star(vmeans):
    """vmeans: {delta: mean V*} on the grid.  Returns dict(kind, lower, upper, interp, monotone): the largest-to-smallest scan
    for the smallest delta such that every delta' >= delta has mean >= THR; the bracket is (that delta's lower grid neighbour
    (fails), that delta (passes)); interpolation in log delta where the bracket is monotone."""
    ds = sorted(vmeans)
    ok = [vmeans[d] >= THR for d in ds]
    # robust threshold: smallest index i such that all j >= i pass
    i = len(ds)
    while i > 0 and ok[i - 1]:
        i -= 1
    # monotone check: inversions > 0.1 between a lower and a higher delta
    inv = [(ds[a], ds[b]) for a in range(len(ds)) for b in range(a + 1, len(ds)) if vmeans[ds[a]] > vmeans[ds[b]] + 0.1]
    if i == len(ds):
        return dict(kind='beyond_grid', lower=ds[-1], upper=None, interp=None, monotone=not inv, inversions=inv)
    if i == 0:
        return dict(kind='below_grid', lower=None, upper=ds[0], interp=None, monotone=not inv, inversions=inv)
    lo, hi = ds[i - 1], ds[i]
    v0, v1 = vmeans[lo], vmeans[hi]
    mono = not inv
    interp = None
    if v1 > v0:
        f = (THR - v0) / (v1 - v0)
        interp = math.exp(math.log(lo) + f * (math.log(hi) - math.log(lo)))
    return dict(kind='bracket', lower=lo, upper=hi, interp=interp, monotone=mono, inversions=inv)


def fmt_ds(d):
    if d['kind'] == 'beyond_grid':
        return '> %.3g (beyond grid)' % d['lower']
    if d['kind'] == 'below_grid':
        return '< %.3g (below grid)' % d['upper']
    s = '(%.3g, %.3g]' % (d['lower'], d['upper'])
    if d['interp']:
        s += ' ~%.3g' % d['interp']
    if not d['monotone']:
        s += ' [non-monotone]'
    return s


def point(d):
    """a scalar for ratios: the interpolation, else the bracket's geometric mean, else None."""
    if d['kind'] == 'bracket':
        return d['interp'] or math.sqrt(d['lower'] * d['upper'])
    return None


def parse_spec(spec):
    kv = {}
    for p in spec.split(':')[1:]:
        if '=' in p:
            k, v = p.split('=', 1)
            try:
                kv[k] = float(v)
            except ValueError:
                kv[k] = v
    kv['_flags'] = [p for p in spec.split(':')[1:] if '=' not in p]
    return kv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dirs', nargs='+'); ap.add_argument('--step1'); ap.add_argument('--out', required=True)
    ns = ap.parse_args()
    rows = load(ns.dirs)
    C = cells(rows); CL = cells(rows, long=True)
    S = {k: cell_stats(v) for k, v in C.items()}
    SL = {k: cell_stats(v, long=True) for k, v in CL.items()}
    R = dict(n_rows=len(rows), n_cells=len(S))
    # ---- series 2a: delta* per (N, I, beta)
    t2a = {}
    for N in (100, 200, 400):
        for I in (64, 256):
            for b in (0.0, 0.3, 1.0, 3.0):
                vm = {}
                nruns = {}
                for d in DELTAS:
                    k = ('2a', '2a:d=%r:b=%r' % (float(d), float(b)), N, I)
                    if k in S:
                        vm[d] = S[k]['vstar']; nruns[d] = S[k]['n']
                if len(vm) >= 2:
                    ds = delta_star(vm)
                    ds['vmeans'] = {str(d): vm[d] for d in vm}; ds['nruns'] = {str(d): nruns[d] for d in nruns}
                    ds['complete'] = (len(vm) == len(DELTAS) and all(nruns[d] == 20 for d in nruns))
                    ds['c_founder'] = (I * N * point(ds)) if point(ds) else None
                    ds['c_tail'] = (I * LAM * point(ds)) if point(ds) else None
                    t2a['%d|%d|%r' % (N, I, b)] = ds
    R['delta_star_2a'] = t2a
    # ---- slice 1 (singles only), series 2b
    sl1 = {}
    vm = {}
    for d in DELTAS:
        k = ('slice1', '2a:d=%r:b=0.0:s1' % float(d), 200, 64)
        if k in S:
            vm[d] = S[k]['vstar']
    if len(vm) >= 2:
        sl1 = delta_star(vm); sl1['vmeans'] = {str(d): vm[d] for d in vm}
    R['slice1_singles_only'] = sl1
    t2b = {}
    for mach in ('R0', 'R1'):
        for N in (200, 400):
            vm = {}
            for d in DELTAS:
                k = ('2b', '2b:%s:d=%r' % (mach, float(d)), N, 64)
                if k in S:
                    vm[d] = S[k]['vstar']
            if len(vm) >= 2:
                ds = delta_star(vm); ds['vmeans'] = {str(d): vm[d] for d in vm}
                ds['c_founder'] = (64 * N * point(ds)) if point(ds) else None
                t2b['%s|%d' % (mach, N)] = ds
    R['delta_star_2b'] = t2b
    # ---- matched copy counts and independent doses
    matched = {}
    for k, v in S.items():
        if k[0] == 'matched':
            kv = parse_spec(k[1])
            c = round(kv['d'] * k[2] * k[3])
            matched.setdefault(str(c), {})['%d|%d' % (k[2], k[3])] = dict(vstar=v['vstar'], lo=v['lo'], hi=v['hi'], n=v['n'])
    for c, d in matched.items():
        vals = [x['vstar'] for x in d.values()]
        d['_spread'] = (max(vals) - min(vals)) if vals else None
    R['matched'] = matched
    indep = {}
    for k, v in S.items():
        if k[0] == 'indep':
            kv = parse_spec(k[1])
            cf = round(kv['df'] * k[2] * k[3]); ct = round(kv['dt'] * k[3] * LAM)
            indep.setdefault('%d|%d' % (k[2], k[3]), {})['f%d_t%d' % (cf, ct)] = dict(vstar=v['vstar'], lo=v['lo'], hi=v['hi'], n=v['n'])
    R['independent_doses_c64'] = indep
    s2 = {}
    for k, v in S.items():
        if k[0] == 'slice2':
            s2[k[1]] = dict(vstar=v['vstar'], lo=v['lo'], hi=v['hi'], n=v['n'])
    R['slice2'] = s2
    # ---- long continuations
    R['long_240N'] = {'%s|%s|%d|%d' % k: dict(vstar_240=v['vstar'], lo=v['lo'], hi=v['hi'], n=v['n']) for k, v in SL.items()}
    # ---- cell table (compact)
    R['cells'] = {'%s|%s|%d|%d' % k: {kk: vv for kk, vv in v.items() if kk != 'runs_vstar'} for k, v in S.items()}
    json.dump(R, open(ns.out + '.json', 'w'), indent=1, default=float)
    # ---- markdown
    out = ['# Length prior over L_T: series 2a / 2b (generated)', '', 'rows: %d, cells: %d' % (len(rows), len(S)), '',
           '## delta* (series 2a; V* share >= 0.9 at 120N), bracket and log-interpolation', '',
           '| N | I | beta | delta* | c* founder = I N delta* | c* tail = I Lambda delta* | complete |', '|---|---|---|---|---|---|---|']
    for k, v in sorted(t2a.items(), key=lambda x: (int(x[0].split('|')[1]), float(x[0].split('|')[2]), int(x[0].split('|')[0]))):
        N, I, b = k.split('|')
        out.append('| %s | %s | %s | %s | %s | %s | %s |' % (N, I, b, fmt_ds(v), ('%.3g' % v['c_founder']) if v['c_founder'] else '-',
                                                          ('%.3g' % v['c_tail']) if v['c_tail'] else '-', v['complete']))
    out += ['', '## V* by delta (series 2a, mean of the 20 runs)', '']
    for k, v in sorted(t2a.items()):
        out.append('- %s: %s' % (k, ', '.join('%s: %.2f' % (d, x) for d, x in sorted(v['vmeans'].items(), key=lambda a: float(a[0])))))
    out += ['', '## series 2b', '']
    for k, v in sorted(t2b.items()):
        out.append('- %s: delta* %s; V*: %s' % (k, fmt_ds(v), ', '.join('%s: %.2f' % (d, x) for d, x in sorted(v['vmeans'].items(), key=lambda a: float(a[0])))))
    out += ['', '## matched copy counts (beta = 0)', '']
    for c, d in sorted(matched.items(), key=lambda a: int(a[0])):
        out.append('- c = %s: %s; spread %.3f' % (c, ', '.join('%s: %.2f [%.2f, %.2f]' % (k, x['vstar'], x['lo'], x['hi']) for k, x in d.items() if k != '_spread'), d['_spread']))
    open(ns.out + '.md', 'w').write('\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
