"""Aggregate the Step 0 per-run records into runs/immigrant-rejection.{md,json} and runs/immigrant_rejection/.

    python3 src/immigrant_rejection_report.py [--scratch DIR]

Applies the attribution rule and the gate of predictions/2026-10-25-immigrant-rejection.md.
"""
import argparse, glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import immigrant_rejection_run as RUN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs')
KEEP = ('run', 'status', 'stop', 'nmig', 'ncev', 'ncev_overflow', 'tc', 'ge', 'tl', 'lw', 'flips', 'inst', 'fate', 'alive',
        'cnt', 'wall', 'rss_gb')
RNG = np.random.default_rng(20261025)
NB = 4000


def load(scratch):
    cells = {}
    for d in sorted(glob.glob(os.path.join(scratch, '*-m*'))):
        name = os.path.basename(d)
        recs = []
        for f in sorted(glob.glob(os.path.join(d, 'r*.json')), key=lambda p: int(os.path.basename(p)[1:-5])):
            recs.append(json.load(open(f)))
        if recs:
            cells[name] = recs
    return cells


def ci(x, stat=np.mean, nb=NB):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (float('nan'),) * 3
    idx = RNG.integers(0, len(x), (nb, len(x)))
    bs = np.array([stat(x[i]) for i in idx])
    return float(stat(x)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def pair_ci(f, A, B, nb=NB):
    """paired run-clustered bootstrap of f(A_resampled, B_resampled); A, B aligned by run."""
    A = np.asarray(A, float); B = np.asarray(B, float)
    n = min(len(A), len(B)); A = A[:n]; B = B[:n]
    est = f(A, B)
    idx = RNG.integers(0, n, (nb, n))
    bs = []
    for i in idx:
        try:
            bs.append(f(A[i], B[i]))
        except ZeroDivisionError:
            continue
    bs = np.array([b for b in bs if np.isfinite(b)])
    if len(bs) == 0:
        return float(est), float('nan'), float('nan')
    return float(est), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def col(recs, f):
    return np.array([f(r) for r in recs], float)


def runs_by_index(recs):
    return {r['run']: r for r in recs}


def paired(ca, cb, fa, fb=None):
    fb = fb or fa
    da = runs_by_index(ca); db = runs_by_index(cb)
    ks = sorted(set(da) & set(db))
    return np.array([fa(da[k]) for k in ks], float), np.array([fb(db[k]) for k in ks], float)


F_MM = lambda r: r['flips']['mm']
F_MED = lambda r: r['flips']['mm_med']
F_TS = lambda r: r['snap']['10000']['ts']
F_TV = lambda r: r['snap']['10000']['tv']
F_COV = lambda r: int(r['snap']['10000']['nm'] == 3)
F_CONS = lambda r: r['snap']['10000']['cons']


def fate_totals(recs):
    f = np.zeros((2, 2, 2, 3), np.int64); a = np.zeros((2, 2, 2), np.int64)
    for r in recs:
        f += np.array(r['fate'], np.int64); a += np.array(r['alive'], np.int64)
    return f, a


def fate_rows(recs):
    f, a = fate_totals(recs)
    rows = []
    for o, on in ((0, 'local'), (1, 'migrant')):
        for ro, rn in ((0, 'excluded'), (1, 'included')):
            for m, mn in ((0, 'mismatched'), (1, 'matched')):
                lost, maj, ovw = (int(v) for v in f[o, ro, m]); al = int(a[o, ro, m])
                tot = lost + maj + ovw + al
                rows.append(dict(origin=on, role=rn, match=mn, arrivals=tot, lost=lost, majority=maj, overwritten=ovw,
                                 alive=al, p_majority=(maj / tot if tot else None)))
    return rows


def fmt(x, p=3):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return 'n/a'
    return ('%.' + str(p) + 'f') % x


def cellstats(recs):
    mm = col(recs, F_MM)
    d = dict(n=len(recs), mm=ci(mm), mo=ci(col(recs, lambda r: r['flips']['mo'])), om=ci(col(recs, lambda r: r['flips']['om'])),
             oo=ci(col(recs, lambda r: r['flips']['oo'])), mm_med=ci(col(recs, F_MED)),
             ts=ci(col(recs, F_TS)), tv=ci(col(recs, F_TV)), cov=ci(col(recs, F_COV)), cons=ci(col(recs, F_CONS)),
             status=sorted(set(r['status'] for r in recs)), wall=float(np.mean(col(recs, lambda r: r['wall']))),
             rss=float(np.max(col(recs, lambda r: r['rss_gb']))))
    inst = {}
    for k in recs[0]['inst']:
        inst[k] = float(np.mean(col(recs, lambda r, k=k: r['inst'][k])))
    d['inst'] = inst
    d['win'] = np.mean([r['flips']['mm_win'] for r in recs], axis=0).tolist()
    d['fate'] = fate_rows(recs)
    d['overflow'] = int(sum(1 for r in recs if r['ncev_overflow']))
    return d


def build(scratch):
    cells = load(scratch)
    st = {n: cellstats(r) for n, r in cells.items()}
    return cells, st


def cname(arm, m):
    return RUN.cell(arm, m)


def verdicts(cells, st):
    V = {}
    MN = RUN.MNS

    def has(*names):
        return all(n in cells for n in names)

    # ---- flips: B vs gV
    flipsBV = {}
    for m in MN:
        b, v = cname('B', m), cname('gV', m)
        if has(b, v):
            fb, fv = paired(cells[b], cells[v], F_MM)
            flipsBV[m] = dict(b=ci(fb), v=ci(fv), ratio=pair_ci(lambda x, y: y.mean() / max(x.mean(), 1e-9), fb, fv),
                              diff=pair_ci(lambda x, y: y.mean() - x.mean(), fb, fv))
    V['flips_B_gV'] = flipsBV
    # ---- branch
    branch = None
    if 0.1 in flipsBV and 1.0 in flipsBV:
        blocks = all(flipsBV[m]['v'][0] <= 0.75 * flipsBV[m]['b'][0] for m in (0.1, 1.0))
        branch = 'a' if blocks else 'b'
    V['branch'] = branch
    # ---- branch (b) quantities
    b = {}
    for m in MN:
        gv, gs, bb = cname('gV', m), cname('gVs', m), cname('B', m)
        e = {}
        if has(gv):
            mm = sum(r['flips']['mm'] for r in cells[gv]); med = sum(r['flips']['mm_med'] for r in cells[gv])
            e['c'] = med / mm if mm else None
            ins = st[gv]['inst']
            tot_mem = ins['inst_mem_fair33'] + ins['inst_mem_other']
            e['frac_inst_mem_fair33'] = ins['inst_mem_fair33'] / tot_mem if tot_mem else None
        if has(gv, gs, bb):
            tgv, tgs = paired(cells[gv], cells[gs], F_TS)
            tgv2, tb = paired(cells[gv], cells[bb], F_TS)
            lead = tgv2.mean() - tb.mean()
            e['ts'] = dict(gV=float(tgv.mean()), gVs=float(tgs.mean()), B=float(tb.mean()))
            e['lead'] = float(lead)
            if lead > 0.1:
                e['delta'] = pair_ci(lambda x, y: (x.mean() - y.mean()) / lead, tgv, tgs)
            else:
                e['delta'] = None
        if has(gs):
            f = st[gs]['fate']
            row = [x for x in f if x['origin'] == 'migrant' and x['role'] == 'included' and x['match'] == 'mismatched'][0]
            e['gVs_incl_mismatch_p_majority'] = row['p_majority']
        b[m] = e
    V['branch_b'] = b
    # ---- mechanism
    mech = None
    if branch == 'b' and all(m in b and 'c' in b[m] and b[m].get('delta') is not None for m in (0.1, 1.0)):
        contract = all(b[m]['c'] is not None and b[m]['c'] > 0.5 and b[m]['delta'][0] > 0.5 for m in (0.1, 1.0))
        immig = all(b[m]['delta'][0] <= 0.5 and (b[m].get('gVs_incl_mismatch_p_majority') or 1) < 0.05 for m in (0.1, 1.0))
        mech = 'contract channel' if contract else ('immigrant selection' if immig else 'mixed')
    V['mechanism'] = mech
    # ---- branch (a) shares
    sh = {}
    for m in MN:
        bb = cname('B', m)
        e = {}
        if has(bb, cname('FI', m)):
            x, y = paired(cells[bb], cells[cname('FI', m)], F_MM)
            e['s_I'] = pair_ci(lambda a, c: 1 - c.mean() / max(a.mean(), 1e-9), x, y)
        if has(bb, cname('FPL', m)):
            x, y = paired(cells[bb], cells[cname('FPL', m)], F_MM)
            e['s_T'] = pair_ci(lambda a, c: 1 - c.mean() / max(a.mean(), 1e-9), x, y)
        for nm in ('FX', 'FP', 'FXP', 'FI', 'FPL'):
            if has(bb, cname(nm, m)):
                x, y = paired(cells[bb], cells[cname(nm, m)], F_MM)
                e['removed_' + nm] = pair_ci(lambda a, c: 1 - c.mean() / max(a.mean(), 1e-9), x, y)
        if has(cname('g0', m), cname('gV', m)):
            g0m = sum(r['flips']['mm'] for r in cells[cname('g0', m)]); g0med = sum(r['flips']['mm_med'] for r in cells[cname('g0', m)])
            gvmed = sum(r['flips']['mm_med'] for r in cells[cname('gV', m)])
            n0 = len(cells[cname('g0', m)]); nv = len(cells[cname('gV', m)])
            e['s_R'] = (g0med / n0 - gvmed / nv) / (g0m / n0) if g0m else None
        sh[m] = e
    V['shares'] = sh
    return V


def write_md(cells, st, V, path):
    L = []
    P = L.append
    P('# Immigrant rejection, Step 0: how the hand-written veto gV keeps coverage (2026-10-25)\n')
    P('Spec `specs/2026-10-25-immigrant-rejection.md`, predictions `predictions/2026-10-25-immigrant-rejection.md` (the '
      'attribution rule and gate are there), notes `notes/immigrant-rejection.md`. Object: three-player majority division '
      'in sixths, length prior, Moran w = 0.3, eps = 0, N = 100, I = 64 islands in one connected component, horizon '
      '10,000 generations, founders `L1`, 40 paired runs per cell. Flips are debounced (25 generations) changes of an '
      'island\'s modal outcome; m->m = between two distinct fair pairs.\n')
    P('## Flips per run (mean [95% run-bootstrap interval])\n')
    P('| mN | arm | m->m | of which contract-mediated | m->other | other->m | other->other | installs on member islands (3,3) / other | refusals on member islands | cons. at 10,000 |')
    P('|---|---|---|---|---|---|---|---|---|---|')
    for m in RUN.MNS:
        for arm in ('B', 'FX', 'FP', 'FXP', 'FI', 'FPL', 'g0', 'gV', 'gVs', 'gKRw'):
            n = cname(arm, m)
            if n not in st:
                continue
            s = st[n]
            f = lambda t: '%s [%s, %s]' % tuple(fmt(v, 1) for v in t)
            ins = s['inst']
            P('| %g | %s | %s | %s | %s | %s | %s | %s / %s | %s | %s |' % (
                m, arm, f(s['mm']), fmt(s['mm_med'][0], 1), fmt(s['mo'][0], 1), fmt(s['om'][0], 1), fmt(s['oo'][0], 1),
                fmt(ins['inst_mem_fair33'], 1), fmt(ins['inst_mem_other'], 1),
                fmt(ins['ref_mem_fair33'] + ins['ref_mem_other'], 1), fmt(s['cons'][0], 2)))
    P('\n## Coverage at generation 10,000 (share of runs [95% interval])\n')
    P('| mN | arm | target (as stated) | target (V*) | all three members present | status codes | runs | mean wall (s) |')
    P('|---|---|---|---|---|---|---|---|')
    for m in RUN.MNS:
        for arm in ('B', 'FX', 'FP', 'FXP', 'FI', 'FPL', 'g0', 'gV', 'gVs', 'gKRw'):
            n = cname(arm, m)
            if n not in st:
                continue
            s = st[n]
            f = lambda t: '%s [%s, %s]' % tuple(fmt(v, 2) for v in t)
            P('| %g | %s | %s | %s | %s | %s | %d | %.0f |' % (m, arm, f(s['ts']), f(s['tv']), f(s['cov']), s['status'],
                                                              s['n'], s['wall']))
    P('\n## Immigrant fates on member islands (all runs pooled; novel play classes; migrant births are the only source of '
      'novelty at eps = 0)\n')
    P('| mN | arm | role | match | arrivals | lost | majority | overwritten | alive | P(majority) |')
    P('|---|---|---|---|---|---|---|---|---|---|')
    for m in RUN.MNS:
        for arm in ('B', 'gV', 'gVs', 'gKRw', 'g0'):
            n = cname(arm, m)
            if n not in st:
                continue
            for x in st[n]['fate']:
                if x['origin'] != 'migrant':
                    continue
                P('| %g | %s | %s | %s | %d | %d | %d | %d | %d | %s |' % (m, arm, x['role'], x['match'], x['arrivals'], x['lost'],
                                                                      x['majority'], x['overwritten'], x['alive'],
                                                                      fmt(x['p_majority'], 4)))
    P('\n## Attribution (preregistered rule)\n')
    P('Flips per run, B against gV (paired): ')
    for m, e in V['flips_B_gV'].items():
        P('- mN = %g: B %s [%s, %s], gV %s [%s, %s], ratio gV/B %s [%s, %s]' % ((m,) + tuple(fmt(v, 1) for v in e['b']) +
                                                                                tuple(fmt(v, 1) for v in e['v']) +
                                                                                tuple(fmt(v, 1) for v in e['ratio'])))
    P('\nBranch: **%s**' % V['branch'])
    P('\nBranch (b) quantities:')
    for m, e in V['branch_b'].items():
        P('- mN = %g: c (contract-mediated share of gV m->m flips) = %s; share of member-island installs that are (3,3) = %s; '
          'target (as stated) gV / gVs / B = %s; lead %s; Delta = %s; gVs mismatched included-slot arrivals reaching a majority = %s' % (
              m, fmt(e.get('c')), fmt(e.get('frac_inst_mem_fair33')),
              ' / '.join(fmt(e['ts'][k], 2) for k in ('gV', 'gVs', 'B')) if 'ts' in e else 'n/a', fmt(e.get('lead'), 2),
              ('%s [%s, %s]' % tuple(fmt(v, 2) for v in e['delta'])) if e.get('delta') else 'n/a',
              fmt(e.get('gVs_incl_mismatch_p_majority'), 4)))
    P('\nMechanism by the rule: **%s**' % V['mechanism'])
    P('\nFreeze diagnostics (fraction of B\'s m->m flips removed, paired):')
    for m, e in V['shares'].items():
        P('- mN = %g: ' % m + '; '.join('%s %s' % (k, ('%s [%s, %s]' % tuple(fmt(v, 2) for v in e[k])) if isinstance(e[k], tuple) else fmt(e[k], 2))
                                         for k in sorted(e)))
    open(path, 'w').write('\n'.join(L) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scratch', default=RUN.SCR)
    a = ap.parse_args()
    cells, st = build(a.scratch)
    V = verdicts(cells, st)
    os.makedirs(os.path.join(OUT, 'immigrant_rejection'), exist_ok=True)
    for n, recs in cells.items():
        json.dump([{k: r[k] for k in KEEP} | {'ts': r['snap']['10000']['ts'], 'tv': r['snap']['10000']['tv'],
                                              'nm': r['snap']['10000']['nm'], 'cons': r['snap']['10000']['cons']}
                   for r in recs], open(os.path.join(OUT, 'immigrant_rejection', n + '.json'), 'w'), separators=(',', ':'))
    out = dict(cells=st, verdicts=V)
    json.dump(out, open(os.path.join(OUT, 'immigrant-rejection.json'), 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    write_md(cells, st, V, os.path.join(OUT, 'immigrant-rejection.md'))
    print('wrote runs/immigrant-rejection.{md,json}; cells', len(cells))


if __name__ == '__main__':
    main()
