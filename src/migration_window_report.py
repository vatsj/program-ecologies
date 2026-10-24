"""Aggregation, scoring and report for the migration-window experiment.

    python3 src/migration_window_report.py [--scratch DIR]

Reads the per-run records in $MW_SCRATCH/<cell>/r<k>.json and writes runs/migration-window.json, runs/migration-window.md
and the compact per-cell files runs/migration_window/<cell>.json.  Intervals are percentile bootstraps over runs
(runs are the clusters; component archipelagos are resampled with their run)."""
import argparse, glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migration_window_run as R

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'runs')
RNG = np.random.default_rng(20261024)
B = 4000
GENS = (1000, 2000, 5000, 10000, 20000)
H = 20000


def load(cell):
    fs = sorted(glob.glob(os.path.join(R.SCR, cell, 'r*.json')), key=lambda f: int(os.path.basename(f)[1:-5]))
    return [json.load(open(f)) for f in fs]


def boot_mean(x, B=B):
    x = np.asarray(x, float)
    n = len(x)
    if n == 0:
        return (float('nan'),) * 3
    idx = RNG.integers(0, n, (B, n))
    m = x[idx].mean(1)
    return float(x.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def boot_diff(a, b, paired=True, B=B):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if paired:
        n = min(len(a), len(b)); d = a[:n] - b[:n]
        idx = RNG.integers(0, n, (B, n)); m = d[idx].mean(1)
        return float(d.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))
    ia = RNG.integers(0, len(a), (B, len(a))); ib = RNG.integers(0, len(b), (B, len(b)))
    m = a[ia].mean(1) - b[ib].mean(1)
    return float(a.mean() - b.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def km_median(t, ev, horizon=H):
    """Kaplan-Meier median of event times t (ev = 1 observed, 0 censored at `t`); nan if the curve stays above 0.5."""
    t = np.asarray(t, float); ev = np.asarray(ev, int)
    if len(t) == 0:
        return float('nan')
    order = np.argsort(t, kind='stable')
    t = t[order]; ev = ev[order]
    n = len(t); S = 1.0
    i = 0
    while i < n:
        tt = t[i]; j = i; d = 0
        while j < n and t[j] == tt:
            d += ev[j]; j += 1
        if d:
            S *= 1 - d / (n - i)
            if S <= 0.5:
                return float(tt)
        i = j
    return float('nan')


def km_boot(t, ev, B=1000):
    t = np.asarray(t, float); ev = np.asarray(ev, int); n = len(t)
    if n == 0:
        return float('nan'), float('nan'), float('nan')
    m0 = km_median(t, ev)
    meds = []
    for _ in range(B):
        ix = RNG.integers(0, n, n)
        meds.append(km_median(t[ix], ev[ix]))
    meds = np.array(meds)
    ok = ~np.isnan(meds)
    if ok.mean() < 0.975:
        return m0, float('nan'), float('nan')
    return m0, float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))


def passage(recs, H=H):
    """KM medians of waste cleared and coverage lost (censored at H), counts."""
    tc, ec = [], []
    tl, el = [], []
    never = 0
    for r in recs:
        if r['t_clear'] >= 0:
            tc.append(r['t_clear']); ec.append(1)
        else:
            tc.append(H); ec.append(0)
        if r['g_est'] < 0:
            never += 1
            continue
        if r['t_lost'] >= 0:
            tl.append(r['t_lost']); el.append(1)
        else:
            tl.append(H); el.append(0)
    return dict(clear=km_boot(tc, ec), clear_events=int(sum(ec)), clear_n=len(tc),
                lost=km_boot(tl, el), lost_events=int(sum(el)), lost_n=len(tl), never_established=never,
                clear_raw=(tc, ec), lost_raw=(tl, el))


def snapstats(recs, g):
    key = str(g)
    rs = [r['snap'][key] for r in recs if key in r['snap']]
    if not rs:
        return None
    I = recs[0]['I']
    d = dict(n=len(rs))
    for k in ('ts', 'tv', 'hps', 'hpv'):
        d[k] = boot_mean([x[k] for x in rs])
    d['nm3'] = float(np.mean([x['nm'] == 3 for x in rs]))
    d['cons'] = float(np.mean([x['cons'] for x in rs]))
    d['occ'] = float(np.mean([x['occ'] for x in rs]))
    for k in ('F', 'U', 'G', 'W', 'D'):
        d['isl_' + k] = float(np.mean([x[k] for x in rs]) / I)
    d['inef'] = float(np.mean([x['inef'] for x in rs]))
    d['arr'] = {k: [x[k] for x in rs] for k in ('ts', 'tv')}
    return d


def episodes_summary(recs, name='ts'):
    e = [r['ep_' + name] for r in recs]
    entered = [x for x in e if x['first'] >= 0]
    return dict(ever=float(len(entered) / len(e)),
                first_median=float(np.median([x['first'] for x in entered])) if entered else float('nan'),
                cum_mean=float(np.mean([x['cum'] for x in e])),
                n25_mean=float(np.mean([x['n25'] for x in e])),
                longest_median=float(np.median([x['longest'] for x in e])),
                final=float(np.mean([x['final'] for x in e])))


def trans_summary(recs):
    tot = {}
    for r in recs:
        for k, v in r['trans'].items():
            tot[k] = tot.get(k, 0) + v
    return tot


def trans_classes(tot):
    """F*>F* (member to a different member), F>U, F>other, F>? and so on, colonization vs local."""
    out = {}
    for k, v in tot.items():
        a, rest = k.split('>'); b, how = rest.split(':')
        fa = a[0]; fb = b[0]
        key = ('F' if fa == 'F' else a) + '>' + ('F' if fb == 'F' else b) + (':same' if (a == b) else '')
        key = '%s>%s' % ('F' if fa == 'F' else a, 'F' if fb == 'F' else b)
        if fa == 'F' and fb == 'F':
            key = 'Fk>Fj'
        out[key] = out.get(key, 0) + v
        out[key + ':' + how] = out.get(key + ':' + how, 0) + v
    return out


def cellstats(recs):
    if not recs:
        return None
    d = dict(n=len(recs), I=recs[0]['I'])
    d['snap'] = {str(g): snapstats(recs, g) for g in GENS}
    d['pass'] = passage(recs)
    d['ep_ts'] = episodes_summary(recs, 'ts'); d['ep_tv'] = episodes_summary(recs, 'tv')
    d['ep_hps'] = episodes_summary(recs, 'hps')
    d['mean_inef'] = float(np.mean([r['mean_inef'] for r in recs]))
    d['trans'] = trans_classes(trans_summary(recs))
    full = [r for r in recs if all(s == 4 for s in r['status'])]
    d['migrant_exposure'] = (float(np.mean([r['nmig'] / (r['I'] * 3 * H) for r in full])) if full else None)
    d['n_full_horizon'] = len(full)
    d['last_waste'] = [r['last_waste'] for r in recs]
    d['wall_mean'] = float(np.mean([r['wall'] for r in recs]))
    d['rss_max'] = float(max(r['rss_mb'] for r in recs))
    d['comps'] = recs[0].get('comps')
    return d


# ---------------------------------------------------------------------- cells to aggregate
def cell_recs(cell, prefix=None):
    recs = load(cell)
    if prefix:
        recs = [r[prefix] for r in recs]
    return recs


def share(recs, g=10000, key='ts'):
    return [r['snap'][str(g)][key] for r in recs if str(g) in r['snap']]


def fmt(m, ci=True, nd=2):
    if m is None or (isinstance(m, float) and np.isnan(m)):
        return 'n/a'
    if isinstance(m, tuple):
        if np.isnan(m[0]):
            return 'n/a'
        return ('%.' + str(nd) + 'f [%.' + str(nd) + 'f, %.' + str(nd) + 'f]') % m if ci else ('%.' + str(nd) + 'f') % m[0]
    return ('%.' + str(nd) + 'f') % m


def fmed(m):
    if isinstance(m, tuple):
        if np.isnan(m[0]):
            return '>%d' % H if True else 'n/a'
        lo, hi = m[1], m[2]
        return '%d [%s, %s]' % (m[0], 'n/a' if np.isnan(lo) else '%d' % lo, 'n/a' if np.isnan(hi) else '%d' % hi)
    return str(m)


# ---------------------------------------------------------------------- re-verification of stored cells
def verify():
    out = {}
    for g, stored_rel in (('base', 'runs/stable_sets/L1.json'), ('gKR', 'runs/farsighted_refusal/UKR99-1.json'),
                          ('gV', 'runs/farsighted_refusal/R2r-1.json')):
        cell = 'VER-%s-N100-m1' % g
        recs = load(cell)
        if not recs:
            continue
        st = json.load(open(os.path.join(ROOT, stored_rel)))['runs']
        same_status = 0; same_labels = 0; same_occ = 0; same_cons = 0; same_cov = 0; n = 0
        for r in recs:
            s = st[r['run']]; n += 1
            if (r['status'][0], r['stop'][0], r['nmig'], r['nev']) == (s['status'], s['stop_gen'], s['nmig'], s['nev']):
                same_status += 1
            h = s['horizons']['10000']; m = r['snap']['10000']
            if g == 'base':
                # the stored base labels are the 0.95 classes; compare the fair-class share and consensus
                same_occ += abs(m['occ'] - h['cats'].get('fair', 0.0)) < 1e-3
                same_cons += 1 if bool(m['cons']) == bool(h['consensus']) else 0
            else:
                lab = h['modal_labels']
                same_labels += (dict(m['labels']) == lab)
                same_occ += abs(m['F'] / r['I'] - h['modal_occupancy']) < 1e-9
                same_cons += 1 if bool(m['cons']) == bool(h['consensus']) else 0
                same_cov += 1 if bool(m['nm'] == 3) == bool(h['coverage']) else 0
        out[cell] = dict(n=n, same_status_stop_nmig_nev=same_status,
                         same_modal_labels=None if g == 'base' else same_labels,
                         same_occupancy=int(same_occ), same_consensus=same_cons,
                         same_coverage=None if g == 'base' else same_cov)
        if g == 'gV':
            out[cell].update(consensus_runs=int(sum(r['snap']['10000']['cons'] for r in recs)),
                             all_three_runs=int(sum(r['snap']['10000']['nm'] == 3 for r in recs)),
                             modal_occupancy=float(np.mean([r['snap']['10000']['F'] / r['I'] for r in recs])),
                             target_ts=float(np.mean([r['snap']['10000']['ts'] for r in recs])),
                             target_tv=float(np.mean([r['snap']['10000']['tv'] for r in recs])))
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('what', nargs='?', default='all')
    a = ap.parse_args()
    if a.what == 'verify':
        print(json.dumps(verify(), indent=1))
