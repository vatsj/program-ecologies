"""Step 3 report of queue 76: aggregates the rows of runs/br_rows/* (and queue 75's stored F-arm rows of runs/lpt_rows/*) into cells,
threshold tables, controls and the verdict inputs.

    python3 src/bully_resist_report.py OUT.json [OUT.md]
"""
import os, sys, json, glob, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import bully_resist_run as BRR
import length_prior_t_run as LR

DELTAS = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4]            # descending
PAIRS = 3


def spec_key(row):
    """(arm, beta, delta, extras) of a row (queue 75 stored F rows: arm F)."""
    s = row['spec']
    parts = s.split(':')
    kv = {p.split('=')[0]: p.split('=')[1] for p in parts[1:] if '=' in p}
    if parts[0] == '2a':
        return ('F', float(kv['b']), float(kv['d']), '')
    if parts[0] == 'br':
        ex = ''.join(':%s=%s' % (k, kv[k]) for k in ('seed', 'pf', 'tab') if k in kv)
        return (kv['arm'], float(kv['b']), float(kv['d']), ex)
    if parts[0] == 'lp':
        return ('lp:%s:%s' % (parts[1], parts[2]), None, float(kv['d']), '')
    raise ValueError(s)


def load_rows():
    rows = {}
    for d in glob.glob(os.path.join(ROOT, 'runs', 'br_rows', '*')):
        rows.update(BRR.load_rows(d))
    stored = {}
    for d in glob.glob(os.path.join(ROOT, 'runs', 'lpt_rows', '*')):
        stored.update(LR.load_rows(d))
    return rows, stored


def boot(x, B=2000, seed=0):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (None, None)
    rng = np.random.default_rng(seed)
    m = x[rng.integers(0, len(x), (B, len(x)))].mean(1)
    return (float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def cell_stats(rs):
    v = np.array([r['vstar'] for r in rs])
    lo, hi = boot(v)
    pairs = np.zeros(3)
    npairs = []
    for r in rs:
        pairs += np.array(r['snap120']['pair_modal'], float)
        npairs.append(r['snap120']['npairs_modal'])
    ch = {}
    for r in rs:
        c = r.get('charges', {}).get('120N')
        if not c:
            continue
        for f, x in c.items():
            if f == 'all':
                ch.setdefault('all', []).append(x)
            elif x[0] is not None and x[1] > 0:
                ch.setdefault(f, []).append((x[0], x[1]))
    chm = {}
    for f, lst in ch.items():
        if f == 'all':
            chm['all'] = float(np.mean(lst))
        else:
            w = np.array([t[1] for t in lst]); c_ = np.array([t[0] for t in lst])
            chm[f] = [float((c_ * w).sum() / w.sum()), float(w.mean())]
    fp = [int(r['cons_modal']['fair_pair']) for r in rs]
    tr = {}
    for win in ('tail|d25', 'chase|d25'):
        M = np.zeros((5, 5)); occ = np.zeros(5); ff = 0
        for r in rs:
            t = r['trans'][win]
            M += np.array(t['M']); occ += np.array(t['occ']); ff += t['ff']
        tr[win] = dict(F_to_U=float(M[0, 1] / occ[0]) if occ[0] else None, U_to_F=float(M[1, 0] / occ[1]) if occ[1] else None,
                       F_to_other=float(M[0, 2:].sum() / occ[0]) if occ[0] else None, FF_flips=float(ff / occ[0]) if occ[0] else None,
                       occ_F=float(occ[0]), occ_U=float(occ[1]), n_FU=int(M[0, 1]), n_UF=int(M[1, 0]))
    return dict(trans=tr, n=len(rs), mean=float(v.mean()), ci=[lo, hi], all_fair=float((v >= 1.0 - 1e-9).mean()), fair_pair_islands=(pairs / max(pairs.sum(), 1)).tolist(),
                unequal_consensus=int(sum(1 for r in rs if r['cons_modal']['unequal'] >= 0)), charges=chm,
                v120=float(v.mean()), v_by_run=[float(x) for x in v])


def build():
    rows, stored = load_rows()
    cells = {}
    for src, rr in (('br', rows), ('q75', stored)):
        for jid, r in rr.items():
            if src == 'q75' and not jid.startswith('2a|'):
                continue
            if src == 'q75' and r['spec'].startswith('2a:') and ':s1' in r['spec']:
                continue
            try:
                k = spec_key(r)
            except ValueError:
                continue
            if src == 'q75' and (k[1] not in (0.0, 1.0, 3.0)):
                continue
            key = (k[0], k[1], r['N'], r['I'], k[2], k[3], bool(r['long']))
            cells.setdefault(key, {})[r['r']] = r
    out = {}
    for key, d in cells.items():
        out[key] = cell_stats([d[r] for r in sorted(d)])
    return out


def delta_star(cs, arm, beta, N, I, thr=0.9):
    """(status, lower, upper, nonmonotone, per-delta means)."""
    means = {}
    for d in DELTAS:
        c = cs.get((arm, beta, N, I, d, '', False))
        means[d] = c['mean'] if c else None
    ds = [d for d in DELTAS if means[d] is not None]
    if len(ds) < len(DELTAS):
        return dict(status='incomplete', means=means)
    passing = [means[d] >= thr for d in DELTAS]          # descending delta
    # largest prefix (from the largest delta) of passing deltas: the threshold is the smallest delta such that it and all larger pass
    k = 0
    while k < len(DELTAS) and passing[k]:
        k += 1
    nonmono = any(passing[k:])
    if k == 0:
        return dict(status='none', means=means, isolated=[d for d, p in zip(DELTAS, passing) if p], nonmonotone=nonmono)
    lower = DELTAS[k] if k < len(DELTAS) else None
    return dict(status='bracket', lower=lower, upper=DELTAS[k - 1], means=means, nonmonotone=nonmono,
                isolated=[d for d, p in zip(DELTAS[k:], passing[k:]) if p])


def table_md(cs, arms, betas, Ns, Is):
    L = []
    for I in Is:
        for N in Ns:
            for beta in betas:
                L.append('N = %d, I = %d, beta = %s: V* (mean over 20 runs [95%% bootstrap]; all-islands-fair share), by delta' % (N, I, beta))
                L.append('')
                L.append('| arm | ' + ' | '.join('%g' % d for d in DELTAS) + ' | delta* |')
                L.append('|---|' + '---|' * (len(DELTAS) + 1))
                for arm in arms:
                    cells = [cs.get((arm, beta, N, I, d, '', False)) for d in DELTAS]
                    if not any(cells):
                        continue
                    ds = delta_star(cs, arm, beta, N, I)
                    st = ds['status'] if ds['status'] != 'bracket' else '(%s, %g]%s' % ('%g' % ds['lower'] if ds['lower'] else '< 3e-4', ds['upper'], ' non-monotone' if ds.get('nonmonotone') else '')
                    if ds['status'] == 'none':
                        st = 'none' + (' (isolated pass at %s)' % ds['isolated'] if ds.get('isolated') else '')
                    L.append('| %s | ' % arm + ' | '.join(('%.2f [%.2f, %.2f]; %.2f' % (c['mean'], c['ci'][0], c['ci'][1], c['all_fair'])) if c else '-' for c in cells) + ' | %s |' % st)
                L.append('')
    return L


if __name__ == '__main__':
    cs = build()
    ser = {json.dumps(list(k)): v for k, v in cs.items()}
    json.dump(ser, open(sys.argv[1], 'w'))
    print(len(cs), 'cells')
    if len(sys.argv) > 2:
        L = table_md(cs, ['F', 'P', 'O', 'PO', 'FPO'], [1.0, 3.0], [100, 200, 400], [64])
        open(sys.argv[2], 'w').write('\n'.join(L) + '\n')
        print('\n'.join(L[:40]))


def v1_check():
    """V1: the F arm of this queue (stage v1, K = 55 catalogue) against queue 75's stored rows (same seeds, same law): vshare_ts, class and pair counts,
    consensus flags and transition counts must be identical."""
    rows, stored = load_rows()
    n = same = 0
    bad = []
    for jid_, r in rows.items():
        if r['series'] != 'v1':
            continue
        spec = r['spec'].replace('br:arm=F:', '2a:')
        old = stored.get('2a|%s|%d|%d|%d|0' % (spec, r['N'], r['I'], r['r']))
        if old is None:
            continue
        n += 1
        ok = (r['vshare_ts'] == old['vshare_ts'] and r['snap120']['cls_modal'] == old['snap120']['cls_modal'] and r['snap120']['pair_modal'] == old['snap120']['pair_modal']
              and r['cons_modal'] == old['cons_modal'] and r['trans'] == old['trans'])
        same += ok
        if not ok:
            bad.append(jid_)
    return dict(compared=n, identical=same, mismatches=bad[:10])
