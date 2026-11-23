"""Queue 81 report: aggregate runs/tbr_rows into runs/tiered-best-response.json and the tables of
runs/tiered-best-response.md (the prose is written by hand around the generated tables in runs/tbr/tables.md).

Every population number is a finite-schedule statistic at the stated horizon (120 N for arms T and M, 10^5
generations for arm P), not pi.  Intervals: percentile bootstrap 95% over runs (2,000 resamples).
"""
import glob, gzip, json, math, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROWS = os.path.join(ROOT, 'runs', 'tbr_rows')
TOL = 1e-9
B = 2000
MIN_CASES = 100


def load_tm():
    out = []
    for f in sorted(glob.glob(os.path.join(ROWS, 'tm', '*.json.gz'))):
        out.append(json.load(gzip.open(f, 'rt')))
    return out


def load_p():
    out = []
    for f in sorted(glob.glob(os.path.join(ROWS, 'p', '*.json.gz'))):
        out.append(json.load(gzip.open(f, 'rt')))
    return out


def cell_key(r):
    if r['arm'] == 'P':
        return ('P', r['exp'], 200, None, round(r['mN'], 3))
    return (r['arm'], 'main', r['N'], r['lam'], r['mN'])


def boot(vals_per_run, stat, rng):
    """vals_per_run: list of per-run objects; stat(list) -> float or None; percentile 95% over runs."""
    n = len(vals_per_run)
    if n == 0:
        return None, None, None
    est = stat(vals_per_run)
    if est is None:
        return None, None, None
    bs = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        v = stat([vals_per_run[i] for i in idx])
        if v is not None:
            bs.append(v)
    if not bs:
        return est, None, None
    return est, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


# ------------------------------------------------------------------ per-run case extraction
def sel_cases(rec, snap='100', thr='set08', natzero=False, world=None):
    """settled, non-vacuous (E and T-weighted migrant) cases of one run at a snapshot, optionally only in diverse /
    consensus worlds and only residents with zero native regret."""
    sn = rec['snaps'][snap]
    if world is not None and sn['world']['diverse'] != (world == 'diverse'):
        return []
    cs = [c for c in sn['cases'] if c[thr]]
    if natzero:
        cs = [c for c in cs if not c['natpos']]
    return cs


def nonvac(cs, which='T'):
    return [c for c in cs if not c['vacE'] and not c['vac' + which]]


def pooled_share(runs_cases, key):
    """pooled over runs: share of cases with value key <= TOL (resident) or the control's expected zero share."""
    def st(rc):
        num = 0.0; den = 0
        for cs in rc:
            for c in cs:
                v = key(c)
                if v is None:
                    continue
                num += v; den += 1
        return num / den if den else None
    return st


def zero_res(which):
    return lambda c: 1.0 if c['reg' + which] <= TOL else 0.0


def mean_res(which):
    return lambda c: c['reg' + which]


def ctl(name, which, idx):
    return lambda c: (c.get(name + which) or [None, None])[idx] if c.get(name + which) is not None else None


def block(runs, which, rng, snap='100', thr='set08', natzero=True, world=None, controls=('pm', 'fd', 'ar')):
    rc = [nonvac(sel_cases(r, snap, thr, natzero, world), which) for r in runs]
    n = sum(len(x) for x in rc)
    out = dict(n_cases=n, n_runs=len(runs), n_runs_with_cases=sum(1 for x in rc if x))
    out['res_zero'] = boot(rc, pooled_share(rc, zero_res(which)), rng)
    out['res_mean'] = boot(rc, pooled_share(rc, mean_res(which)), rng)
    for cn in controls:
        k0 = ctl(cn, which, 0); k1 = ctl(cn, which, 1)
        out[cn + '_zero'] = boot(rc, pooled_share(rc, k0), rng)
        out[cn + '_mean'] = boot(rc, pooled_share(rc, k1), rng)
        out[cn + '_empty'] = int(sum(1 for x in rc for c in x if c.get(cn + which) is None))
        # paired excess of residents over the control (same cases)
        def ex(rcs, k0=k0):
            num = 0.0; den = 0
            for cs in rcs:
                for c in cs:
                    v = k0(c)
                    if v is None:
                        continue
                    num += (1.0 if c['reg' + which] <= TOL else 0.0) - v; den += 1
            return num / den if den else None
        out[cn + '_excess'] = boot(rc, ex, rng)
    return out


def counts_block(runs, snap='100'):
    """unconditional joint table and vacuous counts."""
    nw = len(runs)
    div = [r['snaps'][snap]['world']['diverse'] for r in runs]
    s08 = [r['snaps'][snap]['world']['settled08'] for r in runs]
    s095 = [r['snaps'][snap]['world']['settled095'] for r in runs]
    allc = [c for r in runs for c in r['snaps'][snap]['cases']]
    setc = [c for c in allc if c['set08']]
    out = dict(worlds=nw, diverse=float(np.mean(div)) if nw else None, n_diverse=int(sum(div)),
               settled08=float(np.mean(s08)) if nw else None, settled095=float(np.mean(s095)) if nw else None,
               cases=len(allc), settled_cases=len(setc),
               nonemptyE=float(np.mean([not c['vacE'] for c in setc])) if setc else None,
               vacE=int(sum(c['vacE'] for c in setc)), vacA=int(sum((not c['vacE']) and c['vacA'] for c in setc)),
               vacT=int(sum((not c['vacE']) and c['vacT'] for c in setc)),
               natpos=float(np.mean([c['natpos'] for c in setc])) if setc else None)
    if allc and 'natc' in allc[0]:
        out['natpos_comp'] = float(np.mean([c['natc'] > TOL for c in setc])) if setc else None
        out['Ecomp_eq_E'] = float(np.mean([c['nEc'] == c['nE'] for c in setc])) if setc else None
    return out


def prior_block(runs, rng, world='consensus', thr='set08'):
    """tier 3 inside tier 2, T- and arrival-weighted, residents with zero migrant regret (in the respective weighting),
    non-vacuous prior statistic; prior-matched control drawn from the migrant-argmax set."""
    out = {}
    for which in ('T', 'A'):
        rc = []
        for r in runs:
            sn = r['snaps']['100']
            if world is not None and sn['world']['diverse'] != (world == 'diverse'):
                rc.append([]); continue
            cs = [c for c in sn['cases'] if c[thr] and not c['vacE'] and c.get('pr%s_in' % which) is not None
                  and not c['vacP%s' % which] and not c['natpos']]
            rc.append(cs)
        n = sum(len(x) for x in rc)
        z = pooled_share(rc, lambda c, w=which: 1.0 if c['pr%s_in' % w] <= TOL else 0.0)
        m = pooled_share(rc, lambda c, w=which: c['pr%s_in' % w])
        cz = pooled_share(rc, lambda c, w=which: c['pmpr%s' % w][0] if c['pmpr%s' % w] else None)
        cm = pooled_share(rc, lambda c, w=which: c['pmpr%s' % w][1] if c['pmpr%s' % w] else None)
        zu = pooled_share(rc, lambda c, w=which: 1.0 if c['pr%s_unc' % w] <= TOL else 0.0)

        def ex(rcs, w=which):
            num = 0.0; den = 0
            for cs in rcs:
                for c in cs:
                    if not c['pmpr%s' % w]:
                        continue
                    num += (1.0 if c['pr%s_in' % w] <= TOL else 0.0) - c['pmpr%s' % w][0]; den += 1
            return num / den if den else None
        out[which] = dict(n_cases=n, res_zero=boot(rc, z, rng), res_mean=boot(rc, m, rng), pm_zero=boot(rc, cz, rng),
                          pm_mean=boot(rc, cm, rng), excess=boot(rc, ex, rng), res_zero_unc=boot(rc, zu, rng))
    return out


def time_block(runs, rng, which='T'):
    """paired change in residents' mean T-regret on settled non-vacuous islands of worlds diverse at both 25% and 100%."""
    diffs = []
    for r in runs:
        if not (r['snaps']['25']['world']['diverse'] and r['snaps']['100']['world']['diverse']):
            continue
        a = nonvac(sel_cases(r, '25'), which); b = nonvac(sel_cases(r, '100'), which)
        if not a or not b:
            continue
        diffs.append(np.mean([c['reg' + which] for c in b]) - np.mean([c['reg' + which] for c in a]))
    return diffs


def route_block(runs):
    c = Counter(); org = Counter()
    for r in runs:
        for x in r['routes']:
            if x['natpos']:
                continue
            c[x['route']] += 1
            if x['route'] == 'c':
                org[x['origin']] += 1
    n = sum(c.values())
    return dict(n=n, counts=dict(c), shares={k: v / n for k, v in c.items()} if n else {}, c_origin=dict(org))


def main():
    rng = np.random.default_rng(81)
    tm = load_tm(); pp = load_p()
    allr = tm + pp
    cells = defaultdict(list)
    for r in allr:
        cells[cell_key(r)].append(r)
    out = dict(cells={})
    for k in sorted(cells, key=lambda x: (x[0], x[1], x[2], x[3] if x[3] is not None else -1, x[4])):
        runs = sorted(cells[k], key=lambda r: (r.get('rival') or '', r['run']))
        ck = '|'.join(str(x) for x in k)
        e = dict(key=list(k), counts=counts_block(runs), counts25=counts_block(runs, '25'),
                 repro=[r.get('repro') for r in runs])
        for world in ('diverse', 'consensus', None):
            wk = world or 'all'
            e['mig_' + wk] = {w: block(runs, w, rng, world=world, controls=('pm', 'fd', 'ar') if k[0] != 'P' else ('pm', 'fd'))
                              for w in ('T', 'A')}
            e['mig_' + wk + '_allres'] = {w: block(runs, w, rng, world=world, natzero=False,
                                                   controls=('pm',)) for w in ('T',)}
        e['mig_diverse_095'] = {'T': block(runs, 'T', rng, world='diverse', thr='set095',
                                            controls=('pm',))}
        e['mig_diverse_25'] = {'T': block(runs, 'T', rng, snap='25', world='diverse', controls=('pm',))}
        e['mig_diverse_50'] = {'T': block(runs, 'T', rng, snap='50', world='diverse', controls=('pm',))} \
            if k[0] != 'P' else None
        if k[0] != 'P':
            e['prior_consensus'] = prior_block(runs, rng, 'consensus')
            e['prior_diverse'] = prior_block(runs, rng, 'diverse')
            e['arr_late'] = float(np.mean([r['arr_late'] for r in runs if r.get('arr_late') is not None])) \
                if any(r.get('arr_late') is not None for r in runs) else None
        e['time_diffs'] = time_block(runs, rng)
        e['routes'] = route_block(runs)
        e['examples_pos'] = [dict(run=r['run'], rival=r.get('rival'), i=c['i'], j=c['j'], p=c['p'], **c['ex'])
                             for r in runs for c in r['snaps']['100']['cases'] if c.get('ex') and c['set08'] and not c['natpos']][:12]
        e['examples_threat'] = [dict(run=r['run'], i=c['i'], j=c['j'], p=c['p'], regT=c['regT'], **c['threat'])
                                for r in runs for c in r['snaps']['100']['cases']
                                if c.get('threat') and c['set08'] and not c['natpos'] and not c['vacE']][:12]
        out['cells'][ck] = e
    json.dump(out, open(os.path.join(ROOT, 'runs', 'tbr', 'agg.json'), 'w'), indent=1, default=float)
    print('cells', len(out['cells']))


if __name__ == '__main__':
    main()
