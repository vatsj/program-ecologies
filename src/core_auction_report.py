"""Tables and verdict digest for the core-rediscovery run: reads runs/core_auction/cell_*.json and rows_*.csv.gz, writes
runs/core_auction/tables.json and table_cells.csv, and prints the per-cell digest.

    python3 src/core_auction_report.py [--cells NAME ...]
"""
import argparse, gzip, json, os, sys, csv, warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core_auction as C
import core_auction_run as R

OUT = C.OUT


def load(name):
    p = os.path.join(OUT, 'cell_%s.json' % name)
    if not os.path.exists(p):
        return None, None
    d = json.load(open(p))
    df = pd.read_csv(os.path.join(OUT, 'rows_%s.csv.gz' % name))
    return d, df


def tavg(samples, y):
    t = np.asarray(samples, float); y = np.asarray(y, float)
    return float(np.trapz(y, t) / (t[-1] - t[0]))


def frac_sd(df, col):
    """pooled fraction and the run-level standard deviation."""
    g = df.groupby('run')[col].mean()
    return float(df[col].mean()), float(g.std())


def cell_table(name, statics):
    d, df = load(name)
    if d is None:
        return None
    cell = d['cell']; inst = cell['inst']; v = C.INSTANCES[inst]
    ws = C.wstar(v); mr = C.min_revenue(v); vn = C.vickrey_nearest(v)
    sam = d['samples']; sm = d['series_mean']
    out = dict(name=name, group=cell['group'], inst=inst, space=cell['space'], m_pru=cell['m_pru'], kind=cell['kind'], A=cell['A'], gens=cell['gens'], N=cell['N'],
               m=cell['m'], order=cell['order'], n_runs=d['n_runs'], n_islands=int(len(df)), min_revenue=mr)
    for col in ('eroded', 'core', 'edge', 'at_vn'):
        out[col], out[col + '_sd'] = frac_sd(df, col)
    out['eff'] = float(df['eff'].mean())
    out['eff_below_60'] = None
    out['rev'] = float(df['rev'].mean()); out['rev_sd_islands'] = float(df['rev'].std())
    out['rev_minus_min'] = out['rev'] - mr
    out['fixed'] = float(df['fixed'].mean())
    out['cyc'] = float(df['cyc'].mean())
    out['rev_hist'] = {int(k): int(c) for k, c in df['rev'].round().astype(int).value_counts().sort_index().items()}
    out['one_tick_below_core'] = float(((df['rev'] >= mr - 1 - 1e-9) & (df['rev'] < mr - 1e-9) & (df['core'] == 0)).mean())
    out['ir'] = float(df['ir'].mean())
    out['core_time_avg'] = tavg(sam, sm['core']); out['eroded_time_avg'] = tavg(sam, sm['eroded'])
    # second half time average (after 2,500 generations of the horizon) as the restoration summary under re-injection
    half = [i for i, t in enumerate(sam) if t >= cell['gens'] / 2]
    out['core_time_avg_second_half'] = float(np.mean([sm['core'][i] for i in half]))
    out['core_at_samples'] = {str(sam[i]): sm['core'][i] for i in range(len(sam)) if sam[i] in (0, 100, 200, 500, 1000, 2000, 5000, 10000, 20000)}
    out['eroded_at_start'] = float(sm['eroded'][0])
    fe = df['first_erode']
    out['first_erode_never'] = float((fe < 0).mean())
    out['first_erode_at_start'] = float((fe == 0).mean())
    pos = fe[fe > 0]
    out['first_erode_median_after_start'] = float(pos.median()) if len(pos) else None
    # transfer share of the revenue shortfall among eroded islands: (bidders' total payoff above the core's maximum) / (min revenue - revenue)
    er = df[df['eroded'] == 1]
    ustar = ws - mr
    if len(er):
        gain = (er['uP'] + er['uA'] + er['uB'] - ustar).sum()
        short = (mr - er['rev']).sum()
        out['transfer_share'] = float(gain / short) if short > 0 else None
        out['welfare_loss_share'] = float(1 - gain / short) if short > 0 else None
        out['rev_eroded_mean'] = float(er['rev'].mean())
    # the losing role's surviving bids
    lr = R.losing_roles(inst)
    for r in lr:
        role = C.ROLES[r]
        out['loser_%s_med_quantiles' % role] = [float(x) for x in df['bmed' + role].quantile([0.1, 0.25, 0.5, 0.75, 0.9])]
        out['loser_%s_max_quantiles' % role] = [float(x) for x in df['bmax' + role].quantile([0.1, 0.25, 0.5, 0.75, 0.9])]
    if inst in ('threshold', 'asymmetric'):
        tot = df['bmedA'] + df['bmedB']
        out['P_med_over_winners_total'] = dict(below=float((df['bmedP'] < tot - 1e-9).mean()), at_or_above=float((df['bmedP'] >= tot - 1e-9).mean()),
                                              P_minus_total_median=float((df['bmedP'] - tot).median()))
    # founder coverage: share of islands whose founding set already contains a block (a loser bid at or above its role's value)
    out['founder_hi_mean'] = {r: float(df['founder_hi' + r].mean()) for r in ('P', 'A', 'B')}
    out['founder_lo_mean'] = {r: float(df['founder_lo' + r].mean()) for r in ('P', 'A', 'B')}
    # winners' split on the bidder-optimal edge
    if 'A' in vn and df['edge'].sum() > 0:
        e = df[df['edge'] == 1]
        pa = (v[1] - e['uA']).round().astype(int)
        out['edge_n'] = int(len(e)); out['edge_pA_hist'] = {int(k): int(c) for k, c in pa.value_counts().sort_index().items()}
        out['at_vn_given_edge'] = float(e['at_vn'].mean())
        ef = e[e['fixed'] == 1]
        out['edge_fixed_n'] = int(len(ef)); out['at_vn_given_edge_fixed'] = float(ef['at_vn'].mean()) if len(ef) else None
        b = statics['baselines']['%s/%s' % (inst, cell['space'])]['baseline']
        out['vn_baseline'] = b
        out['vn_ratio_to_baseline'] = out['at_vn_given_edge'] / b if b else None
        runs_e = e.groupby('run')['at_vn'].mean()
        out['at_vn_given_edge_run_sd'] = float(runs_e.std()) if len(runs_e) > 1 else None
    # PRU diagnostics
    if cell['m_pru'] > 0:
        out['pru_present_at_start'] = float(df['ever_pru_present'].mean())
        out['pru_ever_won_given_present'] = float(df.loc[df['ever_pru_present'] == 1, 'ever_pru_win'].mean())
        out['pru_share_P_end'] = float(df['pruP'].mean()); out['pru_share_A_end'] = float(df['pruA'].mean()); out['pru_share_B_end'] = float(df['pruB'].mean())
        for r in lr:
            role = C.ROLES[r]
            c = df[df['core'] == 1]
            out['core_islands_pru_holds_%s_majority' % role] = float((c['pru' + role] > 0.5).mean()) if len(c) else None
            out['core_islands_pru_holds_%s_any' % role] = float((c['pru' + role] > 0).mean()) if len(c) else None
            out['all_islands_pru_holds_%s_majority' % role] = float((df['pru' + role] > 0.5).mean())
        out['core_islands_n'] = int(df['core'].sum())
    # injection
    if 'inject' in d:
        inj = d['inject']
        ne = sum(x['n_eroded'] for x in inj)
        rows_i = [r for x in inj for r in x['inj']]; rows_c = [r for x in inj for r in x['ctl']]
        if ne:
            out['inject'] = dict(n_eroded=ne,
                                 establish_half=float(np.mean([r['share'] >= 0.5 for r in rows_i])), establish_fix=float(np.mean([r['share'] >= 1 - 1e-9 for r in rows_i])),
                                 end_core=float(np.mean([r['core'] for r in rows_i])), end_eroded=float(np.mean([r['eroded'] for r in rows_i])),
                                 end_rev=float(np.mean([r['rev'] for r in rows_i])), end_eff=float(np.mean([r['eff'] for r in rows_i])),
                                 control_core=float(np.mean([r['core'] for r in rows_c])), control_eroded=float(np.mean([r['eroded'] for r in rows_c])),
                                 control_rev=float(np.mean([r['rev'] for r in rows_c])), control_eff=float(np.mean([r['eff'] for r in rows_c])),
                                 establish_and_core=float(np.mean([(r['share'] >= 0.5) and r['core'] for r in rows_i])),
                                 core_given_established=float(np.mean([r['core'] for r in rows_i if r['share'] >= 0.5])) if any(r['share'] >= 0.5 for r in rows_i) else None)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cells', nargs='*', default=None)
    a = ap.parse_args()
    statics = json.load(open(os.path.join(OUT, 'statics.json')))
    sk = os.path.join(OUT, 'statics_skew.json')
    if os.path.exists(sk):
        statics['baselines'].update(json.load(open(sk))['baselines'])
    names = a.cells or list(R.CELLS)
    tabs = {}
    for n in names:
        t = cell_table(n, statics)
        if t is not None:
            tabs[n] = t
    json.dump(tabs, open(os.path.join(OUT, 'tables.json'), 'w'), indent=1, default=float)
    cols = ['name', 'inst', 'space', 'm_pru', 'kind', 'A', 'gens', 'N', 'm', 'order', 'n_runs', 'eroded', 'eroded_sd', 'core', 'core_sd', 'edge', 'at_vn', 'eff', 'rev', 'fixed', 'cyc',
            'core_time_avg', 'core_time_avg_second_half', 'transfer_share', 'at_vn_given_edge', 'vn_baseline']
    with open(os.path.join(OUT, 'table_cells.csv'), 'w') as f:
        w = csv.writer(f); w.writerow(cols)
        for n, t in tabs.items():
            w.writerow([('%.4g' % t[c] if isinstance(t.get(c), float) else t.get(c)) for c in cols])
    for n, t in tabs.items():
        print('%-34s er %.3f core %.3f edge %.3f vn %.3f eff %.3f rev %.2f fixed %.2f tavg_core %.3f | %s' % (
            n, t['eroded'], t['core'], t['edge'], t['at_vn'], t['eff'], t['rev'], t['fixed'], t['core_time_avg'],
            ('inj ' + json.dumps({k: round(v, 3) for k, v in t['inject'].items()})) if 'inject' in t else ''))


def split_by_run():
    """for the cells with item winners: the winners' split pA on the bidder-optimal edge, pooled and by run (the modal pA of each run's edge islands),
    for the skew control also the share of islands at the Vickrey-nearest, the equal-surplus and the equal-payment points."""
    res = {}
    for name, cell in R.CELLS.items():
        inst = cell['inst']
        v = C.INSTANCES[inst]
        if inst == 'collusion':
            continue
        p = os.path.join(OUT, 'rows_%s.csv.gz' % name)
        if not os.path.exists(p):
            continue
        df = pd.read_csv(p)
        e = df[df['edge'] == 1].copy()
        if not len(e):
            res[name] = dict(edge_n=0)
            continue
        e['pA'] = (v[1] - e['uA']).round().astype(int)
        e['pB'] = (v[2] - e['uB']).round().astype(int)
        g = e.groupby('run').agg(n=('pA', 'size'), pA=('pA', lambda x: x.mode()[0]))
        vn = C.vickrey_nearest(v)
        d = dict(edge_n=int(len(e)), pA_hist={int(k): int(c) for k, c in e['pA'].value_counts().sort_index().items()},
                 runs_with_edge=int(len(g)), run_modal_pA={int(k): int(c) for k, c in g['pA'].value_counts().sort_index().items()},
                 runs_total=int(df['run'].nunique()), vn_pA=vn['A'])
        if inst == 'skew':
            d['share_pA_10_VN'] = float((e['pA'] == 10).mean()); d['share_pA_11_equal_surplus'] = float((e['pA'] == 11).mean())
            d['share_pA_7_equal_payment'] = float((e['pA'] == 7).mean())
            d['mean_pA'] = float(e['pA'].mean())
        res[name] = d
    json.dump(res, open(os.path.join(OUT, 'split_by_run.json'), 'w'), indent=1)
    return res


if __name__ == '__main__':
    main()
    split_by_run()
